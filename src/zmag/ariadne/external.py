from .import_tool import import_tool


@import_tool(
    [
        "ObjectType",
        "graphql",
        "graphql_sync",
        "load_schema_from_path",
        "make_executable_schema",
    ]
)
def import_ariadne():
    from ariadne import (
        ObjectType,
        graphql_sync,
        graphql,
        load_schema_from_path,
        make_executable_schema,
    )
    from ariadne.asgi import GraphQL

    # Use the library if available
    return {
        "GraphQL": GraphQL,
        "ObjectType": ObjectType,
        "graphql": graphql,
        "graphql_sync": graphql_sync,
        "load_schema_from_path": load_schema_from_path,
        "make_executable_schema": make_executable_schema,
    }


ariadne = import_ariadne()
