import json
import typing
from dataclasses import asdict
from types import SimpleNamespace

import strawberry
from strawberry.scalars import JSON

# GraphQL Utils
from . import base as zmag
from .tools import to_camel_case


def try_to_load_json(data):
    """For JSON Query"""
    try:
        return json.loads(data)
    except:
        return []


def request_value_error(error_message):
    """Generic Request Error"""
    error_parts = [x.strip() for x in str(error_message).split("@")]
    error_text = "INVALID INPUT"
    if len(error_parts) == 2:
        error_field = to_camel_case(error_parts[0])
        error_text = error_parts[1]
    elif len(error_parts) == 1:
        error_field = None
        error_text = error_parts[0]
    return zmag.errors(
        error=True,
        messages=[zmag.error(type="value", text=error_text, field=error_field)],
    )


def request_perm_error(error_message):
    """Generic Request Error"""
    error_text = str(error_message)
    if error_text == "":
        error_text = "UNAUTHORIZED"
    return zmag.errors(
        error=True, messages=[zmag.error(type="permission", text=error_text)]
    )


def form_to_namespace(form):
    if not form:
        return form
    if hasattr(form, "input"):
        if hasattr(form, "data"):
            return form.input.data.__dict__
    return SimpleNamespace(
        input=SimpleNamespace(
            data=SimpleNamespace(**asdict(form)),
            is_valid=True,
        )
    )


def form_input_is_relationship(value):
    """Check if the model's field is a relationship"""
    try:
        return isinstance(value.__args__[0], typing.ForwardRef)
    except:
        return False


def input_to_dict(input_form):
    data = form_to_namespace(input_form)
    return data.input.data.__dict__ if data else {}


def remove_none_values(filter_by):
    return {key: val for key, val in filter_by.items() if val != None}


def transform_search_by(search_by):
    columns = [key for key, val in search_by.items() if key != "input" and val == True]
    return (columns, search_by.get("input", ""))


def create_custom_input(
    cls,
    name,
    default_value=None,
    single_type=None,
    clear_ignore: list | None = None,
    extra_fields: dict | None = None,
):
    """Generic Input Creator For Models"""
    class_attributes = {}
    class_annotation = {}
    ignored_keys = ["_id", "id"]
    extra_fields = extra_fields or {}
    _clear_ignore = clear_ignore or []
    all_fields = {**cls.__annotations__}
    all_fields.update(extra_fields)
    for key, value in all_fields.items():
        if key in _clear_ignore:
            break
        if key not in ignored_keys and not isinstance(
            value, strawberry.annotation.StrawberryAnnotation
        ):
            if form_input_is_relationship(value):
                break
            if key in extra_fields:
                class_attributes[key] = None
            else:
                class_attributes[key] = default_value

            if key in extra_fields:
                class_annotation[key] = value
            elif single_type and not key in extra_fields:
                class_annotation[key] = single_type
            else:
                class_annotation[key] = value

    class_attributes["__annotations__"] = class_annotation
    # Create the dynamic class using type()
    inputClass = type(name(cls.__name__), (object,), class_attributes)
    return strawberry.input(inputClass)


def crud(
    manager: object,
    form: object | None = None,
    docs: typing.Dict[str, typing.Any] = None,
    clear_ignore: list[str] = None,
):
    the_model = manager.model
    model_name = the_model.__name__
    clear_ignore = clear_ignore or []
    docs = docs or {}

    # Init Forms
    form_create = getattr(form, "Create", None)
    form_update = getattr(form, "Update", None)
    form_filter_by = create_custom_input(
        the_model,
        lambda name: f"Form{name}FilterBy",
        clear_ignore=[],
    )
    form_search_by = create_custom_input(
        the_model,
        lambda name: f"Form{name}SearchBy",
        default_value=False,
        single_type=typing.Optional[bool],
        extra_fields={"input": typing.Optional[str]},
    )
    form_update_reset = create_custom_input(
        the_model,
        lambda name: f"Form{name}UpdateNULL",
        default_value=False,
        single_type=typing.Optional[bool],
        clear_ignore=clear_ignore,
    )

    if not form_create:
        form_create = create_custom_input(the_model, lambda name: f"Form{name}Create")
    if not form_update:
        form_update = create_custom_input(the_model, lambda name: f"Form{name}Update")

    # Create your API (GraphQL) here.
    @zmag.gql
    class GraphQL:
        """GraphQL API"""

        class Meta:
            """Meta-Data"""

            app = False
            model = model_name

        class Query:
            """Query"""

            @zmag.doc(f"""Blank schema of the "**{model_name}**" model""")
            async def schema(camel_case: bool = True) -> JSON:
                if camel_case:
                    model_blank_schema = {
                        to_camel_case(key): None
                        for key in the_model.__annotations__.keys()
                    }
                else:
                    model_blank_schema = {
                        key: None for key in the_model.__annotations__.keys()
                    }
                return model_blank_schema

            @zmag.doc(
                docs.get(
                    "search", f"""List or Search multiple "**{model_name}**" items"""
                )
            )
            async def search(
                info,
                pagination: zmag.pagination | None = None,
                json_query_list: str | None = None,
                filter_by: form_filter_by | None = None,
                search_by: form_search_by | None = None,
            ) -> zmag.edges(the_model):
                # Model
                table = the_model.objects
                context = info.context

                if not pagination:
                    pagination = zmag.pagination()

                # Init
                form_filter_by = input_to_dict(filter_by) or {}
                form_search_by = input_to_dict(search_by) or {}

                # Transform
                active_query = None
                search_by = transform_search_by(form_search_by)
                filter_by = remove_none_values(form_filter_by)
                json_query = try_to_load_json(json_query_list)

                # { QUERY } (1) Custom
                if len(json_query) > 0:
                    active_query = table.query_list(json_query)
                # { QUERY } (2) Search
                elif len(search_by) > 0:
                    active_query = table.Q.search(*search_by)
                # { QUERY } (3) Filter-By
                elif len(filter_by) > 0:
                    active_query = table.Q.filter_by(**filter_by)

                # Database Run
                results = await manager.search(
                    context,
                    pagination=pagination.input.data.__dict__,
                    query=active_query,
                )

                if results:
                    return zmag.page(
                        edges=[the_model(**item.__dict__) for item in results.data],
                        length=results.count,
                        pages=results.pages,
                    )
                return zmag.page(
                    edges=[],
                    length=0,
                    pages=0,
                )

            @zmag.doc(
                docs.get("detail", f"""Retrieve a single "**{model_name}**" item""")
            )
            async def detail(
                info,
                id: zmag.ID | None = None,
                filter_by: form_filter_by | None = None,
            ) -> zmag.query(the_model):
                # Model
                table = the_model.objects
                context = info.context

                item_id = the_model.objects.id_decode(id)
                filter_by = input_to_dict(filter_by)
                active_query = None

                # { QUERY } (1) By ID
                if item_id:
                    active_query = table.Q.filter_by(_id=item_id)
                # { QUERY } (2) Filter-By
                elif len(filter_by) > 0:
                    filter_by = remove_none_values(filter_by)
                    active_query = table.Q.filter_by(**filter_by)

                # Database Run
                results = await manager.detail(
                    context,
                    id=the_model.objects.id_decode(id),
                    query=active_query,
                )
                if results:
                    return the_model(**results.__dict__)
                return None

        class Mutation:
            """Mutation"""

            @zmag.doc(
                docs.get(
                    "create",
                    f"""Create single or multiple "**{model_name}**" item(s)""",
                )
            )
            async def create(
                info,
                form: form_create | None = None,
                forms: list[form_create] | None = None,
            ) -> zmag.mutation[the_model]:
                context = info.context
                form = form_to_namespace(form)

                # Response
                response = {}

                # Create Many
                if forms:
                    # Inputs
                    input_forms = []
                    for f in forms:
                        f = form_to_namespace(f)
                        if f.input.is_valid:
                            input_forms.append(
                                remove_none_values(f.input.data.__dict__)
                            )

                    # Database Run
                    try:
                        results = await manager.create(
                            context,
                            form=input_forms,
                        )
                        if results:
                            if results.error:
                                raise ValueError(
                                    f"DATABASE ERROR: {results.error_message}"
                                )
                            else:
                                response["items"] = [
                                    the_model(**item.__dict__) for item in results.data
                                ]

                    except ValueError as e:
                        response["error"] = request_value_error(e)
                    except PermissionError as e:
                        response["error"] = request_perm_error(e)
                # Create One
                else:
                    # Form Validation
                    if not form.input.is_valid:
                        errors = [zmag.error(**item) for item in form.input.errors]
                        response["error"] = zmag.errors(error=True, messages=errors)
                        return zmag.mutation(**response)

                    # Database Run
                    try:
                        results = await manager.create(
                            context,
                            form=remove_none_values(form.input.data.__dict__),
                        )
                        if results:
                            if results.error:
                                raise ValueError(
                                    f"DATABASE ERROR: {results.error_message}"
                                )
                            else:
                                response["item"] = the_model(**results.data.__dict__)
                    except ValueError as e:
                        response["error"] = request_value_error(e)
                    except PermissionError as e:
                        response["error"] = request_perm_error(e)
                # Return
                return zmag.mutation(**response)

            @zmag.doc(
                docs.get(
                    "update",
                    f"""Update single or multiple "**{model_name}**" item(s)""",
                )
            )
            async def update(
                info,
                item: zmag.item,
                form: form_update | None = None,
                clear: form_update_reset | None = None,
            ) -> zmag.mutation[the_model]:
                # Model
                context = info.context
                form = form_to_namespace(form)
                clear = {key: None for key in input_to_dict(clear).keys()}

                # Inputs
                selected = item.input.data.ids or item.input.data.id
                is_list = item.input.data.is_list

                # Response
                response = {}

                if selected:
                    # Form Validation
                    if not form.input.is_valid:
                        errors = [zmag.error(**item) for item in form.input.errors]
                        response["error"] = zmag.errors(error=True, messages=errors)
                        return zmag.mutation(**response)

                    # Database Run
                    try:
                        client_input_form = remove_none_values(form.input.data.__dict__)
                        client_input_form.update(clear)
                        results = await manager.update(
                            context,
                            selected=selected,
                            form=client_input_form,
                        )
                        if results:
                            if results.error:
                                raise ValueError(
                                    f"DATABASE ERROR: {results.error_message}"
                                )
                            else:
                                # Updated Many
                                if is_list:
                                    response["updated"] = results.count
                                # Updated One
                                elif results.data:
                                    response["item"] = the_model(
                                        **results.data.__dict__
                                    )
                    except ValueError as e:
                        response["error"] = request_value_error(e)
                    except PermissionError as e:
                        response["error"] = request_perm_error(e)

                # Return
                return zmag.mutation(**response)

            @zmag.doc(
                docs.get(
                    "delete",
                    f"""Delete single or multiple "**{model_name}**" item(s)""",
                )
            )
            async def delete(
                info,
                item: zmag.item,
            ) -> zmag.mutation[the_model]:
                # Model
                context = info.context

                # Inputs
                selectors = item.input.data.ids or item.input.data.id

                # Response
                response = {}

                # Return
                try:
                    results = await manager.delete(context, selectors)
                    if results:
                        response["deleted"] = results.count
                except ValueError as e:
                    response["error"] = request_value_error(e)
                except PermissionError as e:
                    response["error"] = request_perm_error(e)

                return response

    return GraphQL
