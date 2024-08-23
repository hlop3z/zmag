# -*- coding: utf-8 -*-
"""
ZMAG Server(s)
"""

import asyncio
import logging
import os
from functools import partial
from typing import Any

from ...external import spoc, uvloop
from ...network import BackendZMQ, DeviceZMQ
from .queue import start_queue
from .publisher import start_publisher
from .pusher import start_pusher
from .watcher import start_watcher
from .debugger import DebugServer


class Device(spoc.BaseThread):
    def on_event(self, event_type: str):
        match event_type:
            case "startup":
                logging.info("Starting Device (ZMQ). . .")
            case "shutdown":
                logging.info("Stopping Device (ZMQ). . .")

    def server(self):
        """ZMQ Device"""
        node: DeviceZMQ = DeviceZMQ(
            backend=self.options.backend,
            frontend=self.options.frontend,
            mode=self.options.mode,
        )
        node.device()
        while self.active:
            pass


class ZMQBaseServer:
    agent: Any = uvloop if uvloop else asyncio

    def before_async(self) -> None:
        """Loop Policy"""
        if os.name == "nt":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    async def on_event(self, event_type: str):
        match event_type:
            case "startup":
                logging.info("Starting Server (ZMQ). . .")
            case "shutdown":
                logging.info("Stopping Server (ZMQ). . .")

    async def server(self):
        """ZMQ Server"""
        from ..framework import Framework  # pylint: disable=cyclic-import

        # My Application
        app = Framework()
        zmq_config = app.env.get("zmq", {})

        # Server Authentication
        with_auth = self.options.authentication

        # Server Node
        node: BackendZMQ = BackendZMQ(
            backend=self.options.backend,
            frontend=self.options.frontend,
            attach=self.options.attach,
            mode=self.options.mode,
            publickey=zmq_config.get("public_key") if with_auth else None,
            secretkey=zmq_config.get("secret_key") if with_auth else None,
        )

        # Start Server
        logging.info("Server ID: %s", node.name)

        # Loop
        match self.options.mode:
            case "streamer":
                await start_pusher(self, app, node)
            case "forwarder":
                await start_publisher(self, app, node)
            case "queue" | _:
                await start_queue(self, app, node)


class ZMQServerProcess(ZMQBaseServer, spoc.BaseProcess):
    """ZMQ Server with Processes"""


class ZMQServerThread(ZMQBaseServer, spoc.BaseThread):
    """ZMQ Server with Threads"""


class Server(spoc.BaseServer):
    services: list[Any] = []

    @classmethod
    def on_event(cls, event_type):
        match event_type:
            case "startup":
                logging.info("Starting Application . . .")
            case "shutdown":
                logging.info("Stopping Application . . .")

    @classmethod
    def start_server(cls, config):
        # Servers (Backend)
        server_type = ZMQServerThread if config.thread else ZMQServerProcess

        # Device
        if config.proxy:
            cls.services.append(
                partial(
                    Device,
                    mode=config.device,
                    backend=config.server,
                    frontend=config.client,
                )
            )

        # Workers
        service_class = partial(
            server_type,
            mode=config.device,
            backend=config.server,
            frontend=config.client,
            attach=config.attach or config.proxy,
            authentication=config.authentication,
        )
        # Workers Range
        for _ in range(0, config.workers):
            cls.services.append(service_class)

        # Banner
        config.banner()

        # Runner
        if config.debug:
            # Debug Mode
            cls.watcher(config.base_dir, config.banner, config.host, config.port)
        else:
            # Production
            cls.start_production()

    @classmethod
    def start_production(cls):
        """Production"""
        cls.add(*[x() for x in cls.services])
        cls.start()

    @classmethod
    def watcher(cls, path_to_watch, banner, host, port):
        """Watch For File Changes"""
        cls.services.append(partial(DebugServer, host=host, port=port))
        start_watcher(cls, path_to_watch, banner, cls.services)
