"""
    Run the API
"""
import os
import asyncio
import click

try:
    import uvloop
except ImportError:
    uvloop = None


from .shell import shell_print
from .watcher import watcher


def debug_server(host, port):
    import uvicorn
    from starlette.applications import Starlette

    from .. import Framework

    app = Framework()
    debuger = Starlette(debug=True)

    debuger.mount("/", app.api.asgi_debug)

    uvicorn.run(debuger, host=host, port=port)


def debug_server_zmq(proxy, backend, frontend):
    from .. import Framework
    from ...server import ZMQ, server

    # App
    app = Framework()

    # ZMQ
    app.zmq = ZMQ(server_uri=backend, client_uri=frontend)

    # Check if is Windows
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    else:
        pass

    asyncio.run(server(proxy))


tcp_port = lambda port: f"tcp://127.0.0.1:{port}"


@click.command()
@click.option("-b", "--backend", default=tcp_port(5556), help="ZMQ Backend (tcp://)")
@click.option("-f", "--frontend", default=tcp_port(5555), help="ZMQ Frontend (tcp://)")
@click.option(
    "-p", "--proxy", default=False, is_flag=True, help="Start (ZMQ) Proxy Device."
)
@click.option("-d", "--debug", default=False, is_flag=True, help="Start Debug Server.")
@click.option("-dh", "--host", default="0.0.0.0", help="Debug Host")
@click.option("-dp", "--port", default=8000, help="Debug Port")
def run(debug, backend, frontend, proxy, host, port):
    """Start Server"""
    from .. import Framework
    from ...server import ZMQ, server

    # App
    app = Framework()

    # ZMQ
    app.zmq = ZMQ(server_uri=backend, client_uri=frontend)

    core_path = app.base_dir

    if debug:
        proxy = True
        # Banner
        banner = "[Hot-Reload]. . . (Press CTRL+C to quit)\n\n"
        if host == "0.0.0.0":
            banner += f"* Debug Server: http://localhost:{port}\n"
        else:
            banner += f"* Debug Server: http://{host}:{port}\n"
        banner += f"* ZMQ Backend : {backend}\n"
        banner += f"* ZMQ Frontend: {frontend}\n"
        # Watcher
        watcher(
            core_path,
            [
                dict(target=debug_server, args=(host, port)),
                dict(target=debug_server_zmq, args=(proxy, backend, frontend)),
            ],
            banner=banner,
        )
    else:
        banner = "Starting Server. . . (Press CTRL+C to quit)\n\n"
        banner += f"* ZMQ Backend : {backend}\n"
        banner += f"* ZMQ Frontend: {frontend}\n"
        shell_print(banner)

        # Check if is Windows
        if os.name == "nt":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        else:
            pass

        # Run
        if uvloop:
            uvloop.run(server(proxy))
        else:
            asyncio.run(server(proxy))
