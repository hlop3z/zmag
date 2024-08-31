# -*- coding: utf-8 -*-
"""
{ Debug }
"""

from typing import Any

from ...external import SPOC

if SPOC:
    import spoc

    class DebugServer(spoc.BaseProcess):
        """Debug Starlette Server"""

        def server(self):
            """HTTP Server"""
            import uvicorn
            from starlette.applications import Starlette
            from strawberry.asgi import GraphQL

            from ..framework import Framework  # pylint: disable=cyclic-import

            app = Framework()
            host = self.options.host
            port = self.options.port

            debuger = Starlette(debug=True)

            graphql_app: Any = GraphQL(app.schema)

            debuger.add_route("/", graphql_app)
            debuger.add_websocket_route("/", graphql_app)

            uvicorn.run(debuger, host=host, port=port)

        def on_event(self, event_type: str):
            """Run Event"""
