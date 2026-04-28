from typing import Callable, Any
import inspect
import dataclasses as dc

HttpMethod = str


class Router:
    def __init__(self, prefix: str = "", tags: list | None = None):
        self.tags = tags
        self.prefix = prefix.rstrip("/")
        self.routes: dict[str, dict[HttpMethod, Callable]] = {}

    def _full_path(self, path: str) -> str:
        path = path if path.startswith("/") else f"/{path}"
        return f"{self.prefix}{path}" if self.prefix else path

    def route(self, method: HttpMethod, path: str):
        method = method.upper()
        full_path = self._full_path(path)

        def decorator(func: Callable):
            self.routes.setdefault(full_path, {})[method] = func
            return func

        return decorator

    def get(self, path: str):
        return self.route("GET", path)

    def post(self, path: str):
        return self.route("POST", path)

    def put(self, path: str):
        return self.route("PUT", path)

    def patch(self, path: str):
        return self.route("PATCH", path)

    def delete(self, path: str):
        return self.route("DELETE", path)

    def include_router(self, router: "Router"):
        for path, methods in router.routes.items():
            self.routes.setdefault(path, {}).update(methods)


class App:
    def __init__(self):
        self.routes: dict[str, dict[str, Callable]] = {}

    def include_router(self, router: Router):
        for path, methods in router.routes.items():
            self.routes.setdefault(path, {}).update(methods)

    async def resolve(self, method: str, path: str):
        return self.routes.get(path, {}).get(method.upper())

    async def run_handler(self, handler: Callable, ctx, data: dict):
        params = list(inspect.signature(handler).parameters.items())
        if params:
            _, first = params[0]
            if first.annotation is not inspect.Parameter.empty:
                ctx = first.annotation(**ctx)
        kwargs = {
            name: param.annotation(data[name])
            for name, param in params[1:]
            if param.annotation is not inspect.Parameter.empty and name in data
        }
        result = handler(ctx, **kwargs)

        if inspect.isawaitable(result):
            return await result

        return result

    async def dispatch(self, method: str, path: str, ctx, data: dict):
        handler = self.routes.get(path, {}).get(method.upper())

        if handler is None:
            return None

        return await self.run_handler(handler, ctx, data)


# ---------------------------------------------------------------------------
# USAGE:
# ---------------------------------------------------------------------------
api = Router()
app = App()


@dc.dataclass
class App:
    label: str = ""
    model: str = ""
    method: str = ""
    action: str = ""


@dc.dataclass
class Context:
    app: App = dc.field(default_factory=lambda: App())
    user: dict = dc.field(default_factory=dict)
    query: dict = dc.field(default_factory=dict)
    request: Any = None
    db: Any = None


@api.get("/")
def root(ctx: Context, key_one: bool, key_two: int):
    print(ctx, key_one, key_two)
    return {"hello world"}


app.include_router(api)


# ---------------------------------------------------------------------------
# Test:
# ---------------------------------------------------------------------------
async def test():
    ctx = {
        "app": App(label="auth", model="user", method="GET"),
        "user": {
            "username": "johndoe",
            "email": "johndoe@example.com",
            "full_name": "John Doe",
            "disabled": False,
            "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",
        },
    }
    data = {"key_one": True, "key_two": 1}
    response = await app.dispatch("GET", "/", ctx, data)
    print(response)


if __name__ == "__main__":
    import asyncio

    asyncio.run(test())
