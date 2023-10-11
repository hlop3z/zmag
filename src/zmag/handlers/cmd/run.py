"""
    Run the API
"""
import click

from .shell import shell_print
from ...tools import coro
from ...server import server, ZMQ
from ...debug_server import debug_server
from ...watcher import watcher


import os
import asyncio

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
    """Start { ZMQ-GraphQL } Server"""
    from ...framework import Framework

    # INIT
    app = Framework()
    mode = app.mode

    # ZMQ
    app.zmq = ZMQ(server_uri=backend, client_uri=frontend)

    # Message
    divider = lambda color="green": shell_print(f"{'-' * 60}", color)

    divider()
    shell_print(f"* Debug Mode...      ({ 'Yes' if debug else 'No' })")

    # Check if is Windows
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    else:
        pass

    if debug:
        color_debug = "magenta"
        divider(color_debug)

        if host == "0.0.0.0":
            shell_print(f"* Debug Server: http://localhost:{port}", color_debug)
        else:
            shell_print(f"* Debug Server: http://{host}:{port}", color_debug)

        divider(color_debug)
        # debug_server(host, port)
        # Debug Server
        asyncio.run(watcher(host, port))
    else:
        shell_print(f"* Starting Server... (Mode: { mode.title() })")
        shell_print(f"* Starting Device... ({ 'Yes' if proxy else 'No' })")

        divider()
        shell_print(f"* ZMQ Frontend: {app.zmq.uri_client}")
        shell_print(f"* ZMQ Backend : {app.zmq.uri_server}")
        divider()

        # Run Server
        asyncio.run(server(proxy))
