# -*- coding: utf-8 -*-
"""
Run the API
"""

from dataclasses import dataclass
from functools import partial
from typing import Any
from ...external import click
from ..shell import shell_print
from .utils import get_imports, shell_banner


@dataclass
class ServerConfig:
    # Debug
    base_dir: Any
    debug: bool
    host: str
    port: int
    # ZMQ
    device: str
    server: str
    client: str
    # ZMQ Options
    proxy: bool
    attach: bool
    workers: int
    thread: bool
    authentication: bool
    # Banner
    banner: Any = None

    def __post_init__(self):
        """Fix Variables"""
        # Single Server
        if not self.attach and not self.proxy:
            self.workers = 1
            self.server = self.client

        # Authentication (FOR NOW)
        # TODO: Allow Authentication with Devices
        if self.authentication:
            self.proxy = False
            self.attach = False
            self.server = self.client
            self.workers = 1

        # Attach Banner
        banner = shell_banner(self)
        self.banner = partial(
            shell_print,
            banner,
            color="magenta" if self.debug else "green",
        )


def tcp_port(port):
    """Generates a TCP address for the local host."""
    return f"tcp://127.0.0.1:{port}"


def get_workers(config, workers, attach):
    """Get number of workers"""
    if workers > 0:
        return workers
    return config.get("workers", 1) if attach else 0


@click.command()
@click.option("-s", "--server", help="Backend (ZMQ) address (tcp://localhost:5556).")
@click.option("-c", "--client", help="Frontend (ZMQ) address (tcp://localhost:5555).")
@click.option(
    "-m",
    "--mode",
    type=click.Choice(["queue", "forwarder", "streamer"]),
    help="Device Type.",
)
@click.option("-p", "--proxy", is_flag=True, default=False, help="Start proxy device.")
@click.option(
    "-a", "--attach", is_flag=True, default=False, help="Connect to proxy device."
)
@click.option(
    "-w",
    "--workers",
    default=0,
    type=int,
    help="Number of instances to attach to proxy device.",
)
@click.option(
    "-t", "--thread", is_flag=True, default=False, help="Worker(s) thread unit type."
)
@click.option("-d", "--debug", is_flag=True, default=False, help="Enable debug mode.")
@click.option(
    "-dh", "--host", default="0.0.0.0", help="Host address for the debug server."
)
@click.option(
    "-dp", "--port", default=5000, type=int, help="Port for the debug server."
)
def run(server, client, mode, proxy, attach, workers, thread, debug, host, port):
    """
    Configure the ZMQ server and debugging options.
    """

    # Imports
    Framework, Server = get_imports()

    # Initialize APP
    app = Framework()
    base_dir = app.base_dir
    zmq_config = app.spoc.get("zmq", {})
    authentication = app.spoc.get("authentication", False)

    # OPTIONS
    is_debug = app.settings.DEBUG or debug
    server_uri = server or zmq_config.get("server", tcp_port(5556))
    client_uri = client or zmq_config.get("client", tcp_port(5555))
    with_proxy = proxy or zmq_config.get("proxy", False)
    is_attach = attach or zmq_config.get("attach", False)
    total_workers = get_workers(zmq_config, workers, is_attach)

    # ZMQ Devices
    device_type = mode or zmq_config.get("device", "queue")
    use_thread = thread or zmq_config.get("thread", False)
    is_thread = True if use_thread and not is_debug else False

    server_config = ServerConfig(
        base_dir=base_dir,
        debug=is_debug,
        host=host,
        port=port,
        authentication=authentication,
        device=device_type,
        server=server_uri,
        client=client_uri,
        proxy=with_proxy,
        attach=is_attach,
        workers=total_workers,
        thread=is_thread,
    )

    # Display Banner
    # server_config.banner()

    # Server
    Server.start_server(server_config)
