# -*- coding: utf-8 -*-
"""
Run the API
"""

import json as py_json
from dataclasses import dataclass
from functools import partial
from typing import Any

import click

from .shell import shell_print
from .utils import get_imports, shell_banner

# import logging
# import os
# import tomllib
# from pathlib import Path


IS_FLAG: Any = {"is_flag": True, "default": False}
DEVICE_TYPES = click.Choice(["queue", "forwarder", "streamer"])


@dataclass
class ServerConfig:
    """Server Settings"""

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
    proxy: bool = False
    attach: bool = False
    workers: int = 1
    thread: bool = False
    # ZMQ Authentication
    authentication: bool = False
    publickey: str | None = None
    secretkey: str | None = None
    serverkey: str | None = None
    # Banner
    banner: Any = None

    def __post_init__(self):
        """Fix Variables"""
        # Single Server
        if not self.attach and not self.proxy:
            self.workers = 1
            self.server = self.client

        # Authentication (FOR NOW)
        # if self.authentication:
        #    self.proxy = False
        #    self.attach = False
        #    self.server = self.client
        #    self.workers = 1

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
@click.option("-m", "--mode", type=DEVICE_TYPES, help="Device Type.")
@click.option("-p", "--proxy", **IS_FLAG, help="Start proxy device.")
@click.option("-a", "--attach", **IS_FLAG, help="Connect to proxy device.")
@click.option("-t", "--thread", **IS_FLAG, help="Worker(s) thread unit type.")
@click.option(
    "-w",
    "--workers",
    default=0,
    type=int,
    help="Number of instances to attach to proxy device.",
)
@click.option("-d", "--debug", **IS_FLAG, help="Enable debug mode.")
@click.option(
    "-dh", "--host", default="0.0.0.0", help="Host address for the debug server."
)
@click.option(
    "-dp", "--port", default=5000, type=int, help="Port for the debug server."
)
def runserver(
    server, client, mode, proxy, attach, thread, workers, debug, host, port
) -> None:
    """
    Start the ZMAG <Server> and optionally a <Device>
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
    is_thread = use_thread and not is_debug

    # ZMQ Settings
    env_config = app.env.get("zmq", {})

    # Server Authentication
    publickey = env_config.get("public_key") if authentication else None
    secretkey = env_config.get("secret_key") if authentication else None
    serverkey = env_config.get("server_key") if authentication else None

    server_config = ServerConfig(
        # Debug
        base_dir=base_dir,
        debug=is_debug,
        host=host,
        port=port,
        # ZMQ
        device=device_type,
        server=server_uri,
        client=client_uri,
        # ZMQ Options
        proxy=with_proxy,
        attach=is_attach,
        workers=total_workers,
        thread=is_thread,
        # ZMQ Authentication
        authentication=authentication,
        publickey=publickey,
        secretkey=secretkey,
        serverkey=serverkey,
    )

    # Server
    Server.start_server(server_config)


# pylint: disable-next=pointless-string-statement
'''
@click.command()
@click.option("-m", "--mode", type=DEVICE_TYPES, help="Device Type.", required=True)
def device(mode) -> None:
    """
    Start ZMAG <Device>
    """

    # Imports
    Framework, Server = get_imports()

    # Initialize APP
    app = Framework()
    current_dir = Path(os.getcwd())

    # TOML
    with open(current_dir / "device.toml", "rb") as f:
        toml_data = tomllib.load(f)

    # ZMQ Settings
    toml_data = app.env.get("zmq", {})

    # OPTIONS
    is_debug = False
    server_uri = toml_data.get("server") or tcp_port(5556)
    client_uri = toml_data.get("client") or tcp_port(5555)
    with_proxy = True
    is_attach = False
    total_workers = 0

    # ZMQ Devices
    device_type = mode
    is_thread = False

    # Literals
    base_dir = None
    host = ""
    port = 0

    # Server Authentication
    publickey = toml_data.get("public_key")
    secretkey = toml_data.get("secret_key")
    authentication = publickey and secretkey

    server_config = ServerConfig(
        # Debug
        base_dir=base_dir,
        debug=is_debug,
        host=host,
        port=port,
        # ZMQ
        device=device_type,
        server=server_uri,
        client=client_uri,
        # ZMQ Options
        proxy=with_proxy,
        attach=is_attach,
        workers=total_workers,
        thread=is_thread,
        # ZMQ Authentication
        authentication=authentication,
        publickey=publickey,
        secretkey=secretkey,
    )

    logging.info(publickey)
    logging.info(secretkey)
    # Device
    # Server.start_server(server_config)
'''


@click.command()
@click.option("-j", "--json", is_flag=True, help="JSON format")
def channels(json) -> None:
    """
    Print all ZeroMQ (Pub/Sub) channels
    """

    # Imports
    Framework, _ = get_imports()
    app = Framework()
    all_channels = sorted(list(app.get_channels()))

    if json:
        click.echo(py_json.dumps(all_channels, indent=4))
    else:
        click.echo("\n".join([f"— {x}" for x in all_channels]))


@click.command()
@click.option("-j", "--json", is_flag=True, help="JSON format")
def tasks(json) -> None:
    """
    Print all ZeroMQ (Push/Pull) tasks
    """

    # Imports
    Framework, _ = get_imports()
    app = Framework()
    all_tasks = sorted(list(app.get_tasks()))

    if json:
        click.echo(py_json.dumps(all_tasks, indent=4))
    else:
        click.echo("\n".join([f"— {x}" for x in all_tasks]))
