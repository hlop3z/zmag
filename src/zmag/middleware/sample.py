from starlette.types import ASGIApp, Receive, Scope, Send


class RejectBadTokenMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            headers = dict(scope.get("headers", []))
            token = headers.get(b"x-secret-token", b"").decode()
            print(headers)
            if token == "bad":
                from starlette.responses import JSONResponse

                response = JSONResponse({"detail": "bad token"}, status_code=403)
                await response(scope, receive, send)
                return
        await self.app(scope, receive, send)
