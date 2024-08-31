# -*- coding: utf-8 -*-
"""
Pre-Schema
"""

import typing

import strawberry
from graphql.validation import NoSchemaIntrospectionCustomRule
from strawberry.extensions import AddValidationRules, QueryDepthLimiter


# pylint: disable-next=function-redefined
def create_schema(  # type: ignore
    query: typing.Any = None,
    mutation: typing.Any | None = None,
    extensions: list | None = None,
    max_depth: int = 4,
    introspection: bool = True,
    **kwargs,
) -> strawberry.Schema | None:
    """Strawberry Schema Wrapper"""

    query = query or []
    mutation = mutation or []
    extensions = extensions or []

    # Apps Extensions
    api_extensions: typing.Any = [
        QueryDepthLimiter(max_depth=max_depth),
    ]
    api_extensions.extend(extensions)

    # Introspection
    if not introspection:
        no_introspection = AddValidationRules([NoSchemaIntrospectionCustomRule])
        api_extensions.append(no_introspection)

    # Query & Mutation
    items: typing.Any = {}
    if query:
        items["query"] = query
    if mutation:
        items["mutation"] = mutation

    # Return Value
    if query:
        return strawberry.Schema(
            **items,
            extensions=api_extensions,
            **kwargs,
        )
    return None
