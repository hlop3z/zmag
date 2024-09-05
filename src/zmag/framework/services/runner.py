# -*- coding: utf-8 -*-
"""
ZMAG Server(s)
"""

import asyncio
import inspect
import logging
import os
from functools import partial
from typing import Any

import spoc
import zmq

from ...external import UVLOOP
from ...network import BackendZMQ, DeviceZMQ
from .debugger import DebugServer
from .pub_push import start_publisher, start_pusher
from .queue import start_queue
from .watcher import start_watcher


class Device(spoc.BaseProcess):
    """Device Service"""

    options: Any

    def on_event(self, event_type: str):
        """Device Events"""
        match event_type:
            case "startup":
                logging.info("Starting Device (ZMQ). . .")
            case "shutdown":
                logging.info("Stopping Device (ZMQ). . .")

    def server(self):
        """ZMQ Device"""
        node: DeviceZMQ = DeviceZMQ(
            backend=self.options.server,
            frontend=self.options.client,
            mode=self.options.device,
            publickey=self.options.publickey,
            secretkey=self.options.secretkey,
        )
        try:
            node.device()
        except zmq.error.ZMQError as e:
            logging.critical(e)
            raise e from e


class ZMQBaseServer:
    """Base ZMQ Server"""

    agent: Any = UVLOOP if UVLOOP else asyncio
    options: Any
    app: Any
    node: BackendZMQ

    def before(self) -> None:
        """Loop Policy"""
        if os.name == "nt":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        from ..framework import Framework  # pylint: disable=cyclic-import

        # My Application
        self.app = Framework()

        # ZMQ Settings
        node_name = self.app.spoc.get("zmq", {}).get("node")

        # Server Node
        try:
            self.node = BackendZMQ(
                name=node_name,
                backend=self.options.server,
                frontend=self.options.client,
                mode=self.options.device,
                attach=self.options.attach,
                publickey=self.options.publickey,
                secretkey=self.options.secretkey,
                serverkey=self.options.serverkey or self.options.publickey,
            )
        except zmq.error.ZMQError as e:
            logging.critical(e)
            raise e from e

    async def on_event(self, event_type: str):
        """App Events"""
        match event_type:
            case "startup":
                logging.info("Starting Server (ZMQ). . .")
                logging.info("Server ID: %s", self.node.name)
                # Events
                await self.run_hooks(
                    self.app.context,
                    self.app.events.startup,
                )
            case "shutdown":
                logging.info("Stopping Server (ZMQ). . .")
                # Events
                await self.run_hooks(
                    self.app.context,
                    self.app.events.shutdown,
                )

    async def run_hooks(self, context, items):
        """Run Event Methods"""
        for method in items:
            if inspect.iscoroutinefunction(method):
                await method(context)
            else:
                method(context)

    async def server(self):
        """ZMQ Server"""

        app = self.app
        node = self.node

        # Start Server (Loop)
        match node.mode:
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
    """Main Server"""

    services: list[Any] = []

    @classmethod
    def on_event(cls, event_type):
        """Main Server Events"""
        match event_type:
            case "startup":
                logging.info("Starting Application . . .")
            case "shutdown":
                logging.info("Stopping Application . . .")
            case "before_shutdown":
                logging.info("Waiting for Application to Shut Down. . .")

    @classmethod
    def start_server(cls, config: Any):
        """Start Main Server"""
        # Servers (Backend)
        server_type = ZMQServerThread if config.thread else ZMQServerProcess

        # Device
        if config.proxy:
            cls.services.append(partial(Device, **config.__dict__))

        # Workers
        service_class = partial(
            server_type,
            **{k: v for k, v in config.__dict__.items() if k not in ["attach"]},
            attach=config.attach or config.proxy,
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
