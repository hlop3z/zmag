import pathlib
import re
from types import SimpleNamespace

import dbcontroller as dbc

from .external import ariadne
from .import_tool import load_json

CURRENT_PATH = pathlib.Path(__file__).parent

TYPE_DEFS = ariadne.load_schema_from_path(CURRENT_PATH / "core_graphql")
FIELDS = load_json(CURRENT_PATH / "fields.json")


def api_scalar_types():
    output = {}
    # Scalars
    output["id"] = dbc.ID
    output["string"] = str
    output["text"] = dbc.text
    output["datetime"] = dbc.datetime
    output["date"] = dbc.date
    output["time"] = dbc.time
    output["decimal"] = dbc.decimal
    output["integer"] = int
    output["float"] = float
    output["boolean"] = bool
    output["list"] = dbc.json
    output["dict"] = dbc.json
    return output


def api_methods_types():
    obj_dict = {}
    # CUD
    obj_dict["create"] = None
    obj_dict["update"] = None
    obj_dict["delete"] = None
    # Read
    obj_dict["detail"] = None
    obj_dict["filter"] = None
    return obj_dict


def api_return_types():
    output = {}
    output["editor"] = {
        "error": "Error",
    }
    output["edit_many"] = {
        "error": "Error",
        "extra": "JSON",
    }
    output["delete"] = {
        "ids": "[ID]",
    }
    output["detail"] = None
    output["filter"] = {
        "page": "Page",
        "computed": "JSON",
    }
    return SimpleNamespace(**output)


def create_database_model(database, model):
    allowed_keys = [
        "table_name",
        "primary_key",
        "required",
        "index",
        "unique",
        "unique_together",
        "ignore",
    ]
    # dbcontroller_config_fixer
    db_config = {}
    for key, val in (model.config or {}).items():
        if key in allowed_keys:
            db_config[key] = val
    # Build Model
    return database.model(model.dataclass, **db_config)


class Util:
    @staticmethod
    def slugify(input_string):
        # Replace multiple hyphens with a single hyphen
        cleaned_string = re.sub(r"-+", "-", input_string)

        # Remove any characters that are not letters or hyphens
        cleaned_string = re.sub(r"[^a-zA-Z-]", "", cleaned_string)

        # IF Starts with hyphen
        if cleaned_string.startswith("-"):
            cleaned_string = cleaned_string[1:]
        # IF Ends with hyphen
        if cleaned_string.endswith("-"):
            cleaned_string = cleaned_string[:-1]
        return cleaned_string.lower()

    @staticmethod
    def snake_to_camel(snake_case_string):
        words = snake_case_string.split("_")
        camel_words = [words[0]] + [word.capitalize() for word in words[1:]]
        camel_case_string = "".join(camel_words)
        return camel_case_string

    @staticmethod
    def camel_to_snake(camel_case_string):
        snake_case_string = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", camel_case_string)
        return snake_case_string.lower()

    @staticmethod
    def camel_to_snake(camel_case_string):
        # Use a regular expression to find uppercase letters following lowercase letters
        # and replace them with an underscore followed by the lowercase version of the letter.
        snake_case_string = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", camel_case_string)
        # Also, convert the string to lowercase.
        return snake_case_string.lower()

    @classmethod
    def parse_class_name(cls, text):
        return cls.slugify(text).title().replace("-", "")

    @classmethod
    def create_graphql_field(cls, property_name, property_data):
        field_type = property_data["graphql_type"]
        is_list = property_data["is_list"]

        if is_list:
            field_type = f"[{field_type}!]"

        return f"{cls.snake_to_camel(property_name)}: {field_type}"

    @classmethod
    def create_graphql_type(cls, model):
        type_defs = ""
        type_defs += f"  type {model.class_name} {{\n"
        current_id_type = "Int" if model.engine == "sql" else "String"
        type_defs += f"    xid: {current_id_type}\n"
        type_defs += "    id: String\n"
        for field_name, setup in model.schema.items():
            type_defs += f"    {cls.create_graphql_field(field_name, setup)}\n"
        type_defs += "}\n"
        return type_defs.strip()

    @staticmethod
    def create_return_type(name, items: dict = {}, extra_types: dict | None = None):
        def return_type_base(key, val):
            return f"{key}: {val}"

        code_text = f"type {name}Response" + " {\n"
        # Database Models
        for key, val in items.items():
            code_text += "    " + return_type_base(key, val) + "\n"
        # API (TYPES)
        if extra_types:
            for key, val in extra_types.items():
                code_text += "    " + return_type_base(key, val) + "\n"
        # Finish
        code_text = code_text.strip()
        code_text += "\n}"
        return code_text

    @staticmethod
    def create_dataclass(model):
        db_config = {}
        for item in model.schema.values():
            item = SimpleNamespace(**item)
            ignored_items = model.config.get("ignore", [])
            ignored_items = ignored_items or []
            if not item.is_model and item.name not in ignored_items:
                if item.is_list:
                    db_config[item.name] = list[item.python_type]
                else:
                    db_config[item.name] = item.python_type
        the_class = type(model.class_name, (object,), {"__annotations__": db_config})
        return the_class

    @classmethod
    def init_schema(cls, model):
        model["name"] = model.get("name", "demo-table")
        model["engine"] = model.get("engine", "mongo")
        model["schema"] = model.get("schema", {})
        model["config"] = model.get("config", {})
        # Fix Name
        model["name"] = cls.slugify(model["name"])
        # Class Name
        model["class_name"] = cls.parse_class_name(model["name"])
        model["return_name"] = model["name"].replace("-", "_")
        return model

    @classmethod
    def parse_resource_path(cls, resolver_name):
        parts = resolver_name.split(".")
        parts_dict = {"type": None, "field": None}
        if len(parts) == 2:
            parts_dict["type"] = cls.parse_class_name(parts[0])
            parts_dict["field"] = cls.snake_to_camel(parts[1])
        return SimpleNamespace(**parts_dict)

    @classmethod
    def create_resolver(cls, api):
        def resolver(resolver_name):
            resource = cls.parse_resource_path(resolver_name)
            resource_found = api.types.get(resource.type)
            if resource_found:
                return resource_found.type.field(resource.field)
            else:
                return lambda *args, **kwarg: [args, kwarg]

        return resolver


class JSQL:
    def __init__(self, fields=None, scalars=None, return_tools=None):
        self.fields = fields or {}
        self.js_helper = {key: f"${key}" for key in fields.keys()}
        self.scalars = scalars or {}
        self.return_tools = return_tools or {}
        self.api_dict = {
            "one": {},
            "many": {},
            "models": {},
            "graphql": set(),
            "control": {},
        }

    def process_object(self, schema):
        fields_setup = {}
        for key, value in schema.items():
            is_list = False
            is_model = False
            graphql_type = None
            output = {
                "name": None,
                "field_type": None,
                "is_list": False,
                "is_model": False,
            }
            # IF List
            if isinstance(value, list) and len(value) > 0:
                value = value[0]
                is_list = True
            # Get Field
            field_name = value.lstrip("$")
            is_model = not value.startswith("$")
            field_type = field_name

            if is_model:
                field_type = Util.parse_class_name(field_name)
                graphql_type = field_type
            else:
                if field_type not in ["dict", "list"]:
                    graphql_type = self.fields.get(field_type, {}).get(
                        "graphql", "String"
                    )
                else:
                    graphql_type = "JSON"

            # Build
            output.update(
                {
                    "name": key,
                    "field_name": field_name,
                    "field_type": field_type,
                    "is_list": is_list,
                    "is_model": is_model,
                    "python_type": self.scalars.get(field_type, field_type),
                    "graphql_type": graphql_type,
                }
            )
            fields_setup[key] = output
        return fields_setup

    def process_return(self, value):
        is_list = False
        is_model = False
        graphql_type = None
        # IF List
        if isinstance(value, list) and len(value) > 0:
            value = value[0]
            is_list = True
        # Get Field
        field_name = value.lstrip("$")
        is_model = not value.startswith("$")
        field_type = field_name
        if is_model:
            field_type = Util.parse_class_name(field_name)
            graphql_type = field_type
        else:
            if field_type not in ["dict", "list"]:
                graphql_type = self.fields.get(field_type, {}).get("graphql", "String")
            else:
                graphql_type = "JSON"

        return {
            "field_name": field_name,
            "field_type": field_type,
            "is_model": is_model,
            "is_list": is_list,
            "python_type": self.scalars.get(field_type, field_type),
            "graphql_type": graphql_type,
        }

    def build_model(self, model_schema):
        model_json = {**model_schema}
        model_json["schema"] = self.process_object(model_json.get("schema"))
        model = SimpleNamespace(**Util.init_schema(model_json))
        model.graphql = Util.create_graphql_type(model)
        model.dataclass = Util.create_dataclass(model)
        model.database = None
        model.type = None
        return model

    def register_models(self, all_models, database=None):
        for schema in all_models:
            if database:
                schema["engine"] = database.engine
            model = self.build_model(schema)
            self.api_dict["one"][model.class_name] = model.class_name
            self.api_dict["many"][model.class_name] = f"[{model.class_name}!]"
            self.api_dict["graphql"].add(model.graphql)

            if ariadne.INIT:
                gql_admin = ariadne.ObjectType(model.class_name)
                model.type = gql_admin

            if database:
                model.database = create_database_model(database, model)

            # Register
            self.api_dict["models"][model.class_name] = model

    def register_control_api(self, resources_control_list, api_obj):
        for item in resources_control_list:
            self.api_dict["control"][Util.parse_class_name(item.name)] = item
            # Process Fields
            for key, val in item._field.methods.items():
                resource_name = f"{item.name}.{key}"
                api_obj.resolve(resource_name)(val)

    def build_api(self, database=None, resources_control_list=None):
        pre_made_schema = TYPE_DEFS
        single_return_type = self.api_dict["one"]
        multip_return_type = self.api_dict["many"]
        database_models = self.api_dict["models"]
        database_graphql_types = self.api_dict["graphql"]

        graphql_types = []

        # Database Loader
        database_loader = []
        object_types = []
        for model in database_models.values():
            if model.type:
                object_types.append(model.type)
            if model.database:
                database_loader.append(model.database)
            else:
                if database:
                    if model.engine != "virtual":
                        model.database = create_database_model(database, model)
                        model.engine = database.engine
                        self.api_dict["models"][model.class_name] = model
                        database_loader.append(model.database)

        # Delete
        graphql_types.append(
            Util.create_return_type("Delete", {}, extra_types=self.return_tools.delete)
        )

        # Create / Update
        graphql_types.append(
            Util.create_return_type(
                "Editor", single_return_type, extra_types=self.return_tools.editor
            )
        )

        # CreateMany
        graphql_types.append(
            Util.create_return_type(
                "EditMany", multip_return_type, extra_types=self.return_tools.edit_many
            )
        )

        # Detail
        graphql_types.append(
            Util.create_return_type("Detail", single_return_type, extra_types={})
        )

        # Filter
        graphql_types.append(
            Util.create_return_type(
                "Filter", multip_return_type, extra_types=self.return_tools.filter
            )
        )

        # Database Types
        graphql_types.append("\n".join(database_graphql_types))

        # Finally
        graphql_final_build_types = "\n".join(graphql_types)

        # Config
        dbc.load(database_loader)
        api_config = {
            "types": database_models,
            "ariadne": object_types,
            "graphql": (pre_made_schema or "") + "\n" + graphql_final_build_types,
            "query": None,
            "mutation": None,
            "control": self.api_dict["control"],
        }

        if ariadne.INIT:
            api_config["query"] = ariadne.ObjectType("Query")
            api_config["mutation"] = ariadne.ObjectType("Mutation")

        # Create Resolver
        api_obj = SimpleNamespace(**api_config)
        api_obj.resolve = Util.create_resolver(api_obj)
        # api_obj.model = lambda name: api_obj.types.get(Util.parse_class_name(name))
        if resources_control_list:
            self.register_control_api(resources_control_list, api_obj)
        return api_obj


jsql = JSQL(
    fields=FIELDS,
    scalars=api_scalar_types(),
    return_tools=api_return_types(),
)
