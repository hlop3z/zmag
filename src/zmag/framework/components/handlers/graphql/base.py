# -*- coding: utf-8 -*-
"""
Schema Basics
"""

import functools
import typing
from collections import namedtuple

from .....external import SPOC, STRAWBERRY
from .....tools.text import pascal_to_snake
from ....components import components
from .schema import create_schema

if STRAWBERRY:
    from strawberry.types import Info

    INFO: typing.Any = Info
else:
    INFO = typing.Any

GraphQL = namedtuple("GraphQL", ["schema", "info", "operations"])
GraphQLInfo = namedtuple("GraphQLInfo", ["query", "mutation"])
Operation = namedtuple("Operation", ["name", "annotations"])


def get_module_name(model: object) -> str:
    """Get class-module's name."""
    parts = model.__module__.split(".")
    return parts[1] if parts[0] == "apps" else parts[0] or "main"


def get_model_name(model: typing.Any) -> str | None:
    """Get model name."""
    model_name = None
    if model:
        model_name = (
            model if isinstance(model, str) else pascal_to_snake(model.__name__)
        )
    return model_name


def create_name(
    method: typing.Any,
    app: str | None = None,
    model: str | None = None,
) -> str:
    """GraphQL resolver's name."""
    method_name = f"{model}_{method.__name__}" if model else method.__name__
    return f"{app}_{method_name}" if app else method_name


def operation_annotations(annotations: dict) -> dict:
    """GraphQL Operations."""
    method: dict = {"inputs": {}}
    for key, val in annotations.items():
        if key == "return":
            method["return"] = [
                item.__name__
                for item in typing.get_args(val)
                if hasattr(item, "__name__")
            ]
        elif hasattr(val, "__spoc__") and hasattr(val, "__name__"):
            method["inputs"][key] = val.__name__
    return method


def create_operation(name: str, annotations: dict) -> Operation:
    """Create operations namedtuple."""
    return Operation(name=name, annotations=operation_annotations(annotations))


def collect_operations(
    active: typing.Any,
    gql_schema: dict,
    permission_classes: list,
    root_app: typing.Any,
    root_model: typing.Any,
    gql_type: str,
):
    """Collect Query & Mutation."""
    app_operations = []
    cls_method = getattr(active.object, gql_type)
    cls_method_fields = SPOC.get_fields(cls_method)
    for current in cls_method_fields:
        resolver_func = getattr(cls_method, current)
        resolver_name = create_name(resolver_func, app=root_app, model=root_model)
        op = functools.partial(
            create_operation, resolver_name, resolver_func.__annotations__
        )
        app_operations.append(op)
        resolver_func.__annotations__["info"] = INFO
        gql_schema[gql_type][resolver_name] = STRAWBERRY.field(
            resolver=resolver_func,
            description=(resolver_func.__doc__ or "").strip(),
            permission_classes=permission_classes,
        )
    return app_operations


def graphql(schemas: list, permissions: list | None = None) -> GraphQL:
    """Collect (GraphQL) Strawberry."""
    gql_schema: dict = {"Query": {}, "Mutation": {}}
    app_operations = []
    permission_classes = permissions or []

    for current in schemas:
        is_component = components.is_component("graphql", current)
        if is_component:
            root_model, root_app = None, get_module_name(current.object)
            # Metadata
            if hasattr(current.object, "Meta"):
                meta = current.object.Meta
                app_name = getattr(meta, "app", root_app)
                if app_name is not True:
                    root_app = app_name
                root_model = getattr(meta, "model", None)
                if root_model:
                    root_model = get_model_name(root_model)
            # Collect Operations
            cls_fields = SPOC.get_fields(current.object)
            for gql_type in ["Query", "Mutation"]:
                if gql_type in cls_fields:
                    app_operations.extend(
                        collect_operations(
                            current,
                            gql_schema,
                            permission_classes,
                            root_app,
                            root_model,
                            gql_type,
                        )
                    )

    gql_query, gql_mutation = None, None
    if gql_schema["Query"]:
        gql_query = STRAWBERRY.type(type("Query", (object,), gql_schema["Query"]))
    if gql_schema["Mutation"]:
        gql_mutation = STRAWBERRY.type(
            type("Mutation", (object,), gql_schema["Mutation"])
        )

    return GraphQL(
        operations=app_operations,
        info=GraphQLInfo(
            query=frozenset(gql_schema["Query"].keys()),
            mutation=frozenset(gql_schema["Mutation"].keys()),
        ),
        schema=functools.partial(create_schema, query=gql_query, mutation=gql_mutation),
    )
