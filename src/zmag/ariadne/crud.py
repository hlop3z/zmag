from types import SimpleNamespace
import json
import functools


import dbcontroller as dbc
from dbcontroller.forms import ISNULL

from .external import ariadne
from .jsql import jsql, Util, FIELDS
from .scalars import SCALARS
from .database_manager import DatabaseManager
from .unique_fields import unique_object, unique_object_many
from .query_depth_limiter import QueryDepthLimiter


input_form = dbc.form.group("Model")


def get_model_core_objects(model_name, table):
    engine = "sql"
    real_database = getattr(table.database.objects, "database", None)
    model_columns = []

    if not real_database:
        engine = "mongo"
        real_database = table.database.objects.crud.collection
    if table.database:
        model_columns = table.database.objects.columns
    return SimpleNamespace(
        name=model_name,
        table=table.database.objects,
        type=table,
        database=real_database,
        columns=model_columns,
        engine=engine,
    )


def get_model_inputs(table):
    model_columns = []
    form_fields = {}
    if table.database:
        related_columns = table.config.get("related", {})
        model_columns = table.database.objects.columns
        auto_list = table.config.get("auto", [])
        cols_inputs = [col for col in model_columns if col not in auto_list]
        for col in cols_inputs:
            field = table.schema.get(col)
            if field:
                field_name = field.get("name")
                field_name = Util.snake_to_camel(field_name)
                if related_columns.get(field.get("name")):
                    form_fields[field_name] = "string"
                else:
                    field_type = field.get("field_type")
                    form_fields[field_name] = field_type
    return form_fields


def get_model_fields(table):
    form_fields = {}
    for config in table.schema.values():
        field_name = config.get("name")
        field_name = Util.snake_to_camel(field_name)
        field_type = config.get("field_type")
        is_list = config.get("is_list")
        is_model = config.get("is_model")
        form_fields[field_name] = {
            "type": field_type,
            "is_list": is_list,
            "is_model": is_model,
        }
    return form_fields


def query_input_to_snake_case(api, table, client_query):
    table_config = table.config
    related_config = table_config.get("related", {})
    if client_query and len(client_query) > 0:
        for item in client_query:
            if isinstance(item, list) and len(item) == 3:
                query_key = Util.camel_to_snake(item[0])
                query_value = item[2]
                item[0] = query_key
                related_class = related_config.get(query_key)
                if related_class:
                    related_name = Util.parse_class_name(related_class)
                    related_type = api.types.get(related_name)
                    if related_type.database:
                        related_table = related_type.database.objects
                        if query_value and isinstance(query_value, list):
                            item[2] = [related_table.id_decode(x) for x in query_value]
                        elif query_value and isinstance(query_value, str):
                            item[2] = related_table.id_decode(query_value)


def all_api_forms(core_api):
    all_models = list(core_api.types.keys())
    all_forms = {}
    all_objs = {}
    for model_name in all_models:
        table = core_api.types.get(model_name)
        all_forms[model_name] = get_model_inputs(table)
        all_objs[model_name] = get_model_fields(table)

    return {
        "models": all_models,
        "fields": list(FIELDS.keys()),
        "query": [
            "info",
            "detail",
            "filter",
        ],
        "mutation": [
            "create",
            "update",
            "createMany",
            "updateMany",
            "delete",
        ],
        "objects": all_objs,
        "forms": all_forms,
    }


def get_model_control(admin, control_path):
    try:
        return admin.api(control_path)
    except:  # noqa: E722
        return None


def process_request_form(table, admin, form_name: str, client_form: dict):
    model_form = get_model_control(admin, f"form.{form_name}")
    if model_form:
        model_form = input_form(model_form)
        model_fields = model_form.__annotations__.keys()
        client_form = {
            key: val for key, val in client_form.items() if key in model_fields
        }
        clean_form = model_form(**client_form).input
        del_keys = []
        for key, val in clean_form.data.__dict__.items():
            if val == ISNULL:
                del_keys.append(key)
        for key in del_keys:
            del clean_form.data.__dict__[key]
        if not clean_form.is_valid:
            for item in clean_form.errors:
                if item.get("field"):
                    item["field"] = Util.snake_to_camel(item["field"])
        return clean_form
    else:
        model_fields = table.database.objects.columns
        client_form = {
            key: val for key, val in client_form.items() if key in model_fields
        }
        return SimpleNamespace(
            data=SimpleNamespace(**client_form), errors=None, is_valid=True, next=None
        )


def process_request_variables(variables):
    if variables.get("form"):
        variables["form"] = json.dumps(variables["form"])
    if variables.get("forms"):
        variables["forms"] = [json.dumps(form) for form in variables["forms"]]
    if variables.get("query"):
        variables["query"] = json.dumps(variables["query"])
    return variables


def create_graphql_app(
    database=None,
    json_models: list = None,
    class_models: list = None,
    max_depth: int = 4,
    max_limit: int = 10,
):
    jsql.register_models(json_models)

    API = jsql.build_api(
        database=database,
        resources_control_list=class_models,
    )

    ############################################
    # Create
    ############################################
    async def resolve_create(_, info, **kwargs):
        model_name = kwargs.get("model")
        table = API.types.get(model_name)
        admin = API.control.get(model_name)
        client_form = kwargs.get("form", {})
        results = {}

        if table and table.database:
            # Clean Form
            form = process_request_form(table, admin, "create", client_form)
            if not form.is_valid:
                return {"error": {"messages": form.errors}}
            else:
                client_form = form.data.__dict__
            # Check Unique
            unique_errors = await unique_object(table, client_form)
            if unique_errors:
                return unique_errors
            # Database Hit
            database = DatabaseManager(table.database.objects)
            results = await database.create(client_form)
            if results:
                results["xid"] = results["_id"]
            # After Method
            model_core = get_model_core_objects(model_name, table)
            computed_api = SimpleNamespace(model=model_core, data=results)
            after_util = get_model_control(admin, "after.create")
            if after_util:
                await after_util(computed_api, info)

        if table and table.return_name:
            return {table.return_name: results}

    ############################################
    # Update
    ############################################
    async def resolve_update(_, info, **kwargs):
        selected_id = []
        model_name = kwargs.get("model")
        client_form = kwargs.get("form", {})
        client_form_keys = client_form.keys()
        admin = API.control.get(model_name)
        table = API.types.get(model_name)
        results = {}
        perms_method = None
        clean_form = {}

        if table and table.database:
            database = DatabaseManager(table.database.objects)

            check_object_perms = get_model_control(admin, "perms.update")
            if check_object_perms:

                def perms_method(object):
                    return check_object_perms(object, info)

            item_id = client_form.get("id")
            if item_id:
                selected_id = [item_id]
                del client_form["id"]

                # Clean Form
                form = process_request_form(table, admin, "update", client_form)
                if not form.is_valid:
                    return {"error": {"messages": form.errors}}
                else:
                    client_form = form.data.__dict__

                # Remove None Values if not in "client_form"
                for key in client_form.keys():
                    if key in client_form_keys:
                        clean_form[key] = client_form.get(key)
                client_form = clean_form

                # Check Unique
                unique_errors = await unique_object(table, client_form)
                if unique_errors:
                    return unique_errors

                # Database Hit
                results = await database.update(selected_id, client_form, perms_method)
                if results:
                    results["xid"] = results["_id"]
            # After Method
            model_core = get_model_core_objects(model_name, table)
            computed_api = SimpleNamespace(model=model_core, data=results)
            after_util = get_model_control(admin, "after.update")
            if after_util:
                await after_util(computed_api, info)

        if table and table.return_name:
            return {table.return_name: results}

    ############################################
    # Delete
    ############################################
    async def resolve_delete(_, info, **kwargs):
        model_name = kwargs.get("model")
        selected_id = kwargs.get("ids")
        admin = API.control.get(model_name)
        table = API.types.get(model_name)
        results = []
        perms_method = None

        if table and table.database:
            database = DatabaseManager(table.database.objects)

            check_object_perms = get_model_control(admin, "perms.delete")
            if check_object_perms:

                def perms_method(object):
                    return check_object_perms(object, info)

            results = await database.delete(selected_id, perms_method)
            # After Method
            model_core = get_model_core_objects(model_name, table)
            computed_api = SimpleNamespace(model=model_core, data=results)
            after_util = get_model_control(admin, "after.delete")
            if after_util:
                await after_util(computed_api, info)

        return {"ids": results}

    ############################################
    # Create Many
    ############################################
    async def resolve_create_many(_, info, **kwargs):
        model_name = kwargs.get("model")
        client_forms = kwargs.get("forms", [])
        table = API.types.get(model_name)
        admin = API.control.get(model_name)
        results = []
        clean_forms = []

        if table and table.database:
            # Clean Form
            check_form = functools.partial(process_request_form, table, admin, "create")
            for dirty_form in client_forms:
                form = check_form(dirty_form)
                if not form.is_valid:
                    return {
                        "error": {
                            "messages": form.errors,
                            "meta": {
                                Util.snake_to_camel(key): val
                                for key, val in form.data.__dict__.items()
                            },
                        },
                    }
                else:
                    clean_forms.append(form.data.__dict__)

            if clean_forms:
                # Check Unique
                unique_errors = await unique_object_many(table, clean_forms)
                if unique_errors:
                    return unique_errors

                # Database Hit
                database = DatabaseManager(table.database.objects)
                results = await database.create(clean_forms)
                if results and len(results) > 0:
                    for item in results:
                        item["xid"] = item["_id"]
                # After Method
                model_core = get_model_core_objects(model_name, table)
                computed_api = SimpleNamespace(model=model_core, data=results)
                after_util = get_model_control(admin, "after.create")
                if after_util:
                    await after_util(computed_api, info)
        if table and table.return_name:
            return {table.return_name: results}

    ############################################
    # Update Many
    ############################################
    async def resolve_update_many(_, info, **kwargs):
        selected_id = []
        model_name = kwargs.get("model")
        client_form = kwargs.get("form", {})
        client_form_keys = client_form.keys()
        selected_id = kwargs.get("ids", [])
        admin = API.control.get(model_name)
        table = API.types.get(model_name)
        results = []
        perms_method = None
        clean_form = {}

        if table and table.database:
            # Clean Form
            form = process_request_form(table, admin, "update", client_form)
            if not form.is_valid:
                return {"error": {"messages": form.errors}}
            else:
                client_form = form.data.__dict__
            # Remove None Values if not in "client_form"
            for key in client_form.keys():
                if key in client_form_keys:
                    clean_form[key] = client_form.get(key)
            client_form = clean_form
            ############################################
            # TODO
            ############################################
            # Check Unique
            unique_errors = await unique_object(table, client_form)
            if unique_errors:
                return unique_errors

            # Database Hit
            database = DatabaseManager(table.database.objects)

            check_object_perms = get_model_control(admin, "perms.update")
            if check_object_perms:

                def perms_method(object):
                    return check_object_perms(object, info)

            results = await database.update(
                selected_id, client_form, perms_method, is_many=True
            )
            if results and len(results) > 0:
                for item in results:
                    item["xid"] = item["_id"]
            # After Method
            model_core = get_model_core_objects(model_name, table)
            computed_api = SimpleNamespace(model=model_core, data=results)
            after_util = get_model_control(admin, "after.update")
            if after_util:
                await after_util(computed_api, info)
        if table and table.return_name:
            return {table.return_name: results}

    ############################################
    # Detail
    ############################################
    async def resolve_detail(_, info, **kwargs):
        model_name = kwargs.get("model")
        item_id = kwargs.get("id")
        admin = API.control.get(model_name)
        table = API.types.get(model_name)
        results = {}
        perms_method = None

        if table and table.database:
            database = DatabaseManager(table.database.objects)
            check_object_perms = get_model_control(admin, "perms.detail")
            if check_object_perms:

                def perms_method(object):
                    return check_object_perms(object, info)

            results = await database.detail(item_id, perms_method)
            if results:
                results["xid"] = results["_id"]
            # After Method
            model_core = get_model_core_objects(model_name, table)
            computed_api = SimpleNamespace(model=model_core, data=results)
            after_util = get_model_control(admin, "after.detail")
            if after_util:
                await after_util(computed_api, info)
        if table and table.return_name:
            return {table.return_name: results}

    ############################################
    # Filter
    ############################################
    async def resolve_filter(_, info, **kwargs):
        model_name = kwargs.get("model")
        client_query = kwargs.get("query")
        client_page = kwargs.get("page", 1)
        client_limit = kwargs.get("limit", 10)
        client_sort = kwargs.get("sort", "-id")
        client_all = kwargs.get("all", False)

        admin = API.control.get(model_name)
        table = API.types.get(model_name)
        extra = {}
        results = []
        perms_method = None
        perms_filter = None

        # Fix Page
        if client_page <= 1:
            client_page = 1

        # Fix Limit
        if client_limit > max_limit:
            client_limit = max_limit

        # Pagination
        page = {
            "number": client_page,
            "count": 0,
            "pages": 0,
            "has_prev": False,
            "has_next": False,
        }

        if table and table.database:
            database = DatabaseManager(table.database.objects)
            check_object_perms = get_model_control(admin, "perms.filter")
            check_filter_perms = get_model_control(admin, "filter.query")
            if check_object_perms:

                def perms_method(object):
                    return check_object_perms(object, info)

            if check_filter_perms:

                def perms_filter(object):
                    return check_filter_perms(object, info)

            # Parse Query
            query_input_to_snake_case(API, table, client_query)

            # Database Run
            db_results = await database.filter(
                client_query,
                perms_queryset=perms_filter,
                object_perms_method=perms_method,
                page=client_page,
                limit=client_limit,
                sort_by=client_sort,
                get_all=client_all,
            )
            results = db_results.data

            # Pagination Update
            page["count"] = db_results.count
            page["pages"] = db_results.pages

            # Next & Prev
            if page["number"] < page["pages"]:
                page["has_next"] = True
            else:
                page["has_next"] = False

            if page["number"] > 1:
                page["has_prev"] = True
            else:
                page["has_prev"] = False
            # Fix ID
            # Fix ID
            if results and len(results) > 0:
                for item in results:
                    item["xid"] = item["_id"]

            # Computed Values
            model_core = get_model_core_objects(model_name, table)
            computed_api = SimpleNamespace(model=model_core, data=results)
            extra_util = get_model_control(admin, "filter.computed")
            if extra_util:
                extra = await extra_util(computed_api, info)
                if extra:
                    extra = {
                        Util.snake_to_camel(key): value for key, value in extra.items()
                    }
            # After Method
            after_util = get_model_control(admin, "after.filter")
            if after_util:
                await after_util(computed_api, info)
        if table and table.return_name:
            return {table.return_name: results, "page": page, "computed": extra}

    ############################################
    # Info (API)
    ############################################
    API_INFO_DICT = all_api_forms(API)

    async def resolve_info(_, info, **kwargs):
        return API_INFO_DICT

    # CUD
    API.mutation.set_field("create", resolve_create)
    API.mutation.set_field("update", resolve_update)
    API.mutation.set_field("delete", resolve_delete)
    API.mutation.set_field("createMany", resolve_create_many)
    API.mutation.set_field("updateMany", resolve_update_many)
    # READ
    API.query.set_field("detail", resolve_detail)
    API.query.set_field("filter", resolve_filter)
    # Tools
    API.query.set_field("info", resolve_info)

    executable_schema = None
    if len(API.types) > 0:
        executable_schema = ariadne.make_executable_schema(
            API.graphql,
            *SCALARS,
            *API.ariadne,
            API.query,
            API.mutation,
            convert_names_case=True,
        )

    model_database_objects = {}
    for key, table in API.types.items():
        if table.database:
            model_database_objects[key] = table.database.objects

    def process_execute(query, operation, variables, context):
        request = {"query": query}
        # Context
        context = context or {}
        context["database"] = model_database_objects
        # Variables
        if variables:
            variables = process_request_variables(variables)
            request["variables"] = variables
        if operation:
            request["operationName"] = operation
        # Execute
        return request, context

    async def execute(
        query: str = None,
        variables: dict = None,
        operation: str = None,
        context: dict = None,
    ):
        request, context = process_execute(query, operation, variables, context)
        # Execute
        success, response = await ariadne.graphql(
            executable_schema,
            request,
            context_value=context,
            validation_rules=[QueryDepthLimiter(max_depth=max_depth)],
        )
        return response

    async def get_context_value(request, _):
        return {
            "request": request,
            "database": API.models,
        }

    API.fields = FIELDS
    API.models = model_database_objects
    API.schema = executable_schema
    API.execute = execute
    API.asgi_debug = ariadne.GraphQL(
        API.schema,
        context_value=get_context_value,
        debug=True,
    )
    return API
