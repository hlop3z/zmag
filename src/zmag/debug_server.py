def debug_server(host: str = "0.0.0.0", port: int = 8000):
    from starlette.applications import Starlette
    from strawberry.asgi import GraphQL
    import uvicorn

    from .framework import Framework as App

    api = App()
    schema = api.graphql.schema()

    graphql_app = GraphQL(schema)

    app = Starlette(debug=True)
    app.add_route("/", graphql_app)
    app.add_websocket_route("/", graphql_app)

    uvicorn.run(app, host=host, port=port)
