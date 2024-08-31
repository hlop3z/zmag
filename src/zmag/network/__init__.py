# -*- coding: utf-8 -*-
"""
ZMQ Network
"""

import logging
import signal
from typing import Any

from .base import ConfigSSH, ZeroMQ, tcp_string
from .utils import Data


class DeviceZMQ(ZeroMQ):
    """ZeroMQ `Proxy` Device"""

    def __init__(
        self,
        mode: str = "queue",
        backend: str = tcp_string(5556),  # inproc://workers
        frontend: str = tcp_string(5555),  # inproc://clients
        # Authenticator
        publickey: str | None = None,
        secretkey: str | None = None,
    ):
        """
        Initialize ZeroMQ `Device`.
        """

        super().__init__(
            backend=backend,
            frontend=frontend,
            mode=mode,
            publickey=publickey,
            secretkey=secretkey,
        )

    def start(self):
        """Run Device"""
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        logging.info("Press <CTRL + C> to Quit")
        logging.info("Starting Device (ZMQ). . .")
        try:
            self.device()
        except KeyboardInterrupt:
            pass
        finally:
            logging.info("Stopping Device (ZMQ). . .")


class BackendZMQ(ZeroMQ):
    """ZeroMQ `Backend` Server"""

    app: Any
    data: Any = Data

    def __init__(
        self,
        mode: str = "queue",
        backend: str = tcp_string(5556),  # inproc://workers
        frontend: str = tcp_string(5555),  # inproc://clients
        name: str | None = None,
        attach: bool = False,
        # Authenticator
        publickey: str | None = None,
        secretkey: str | None = None,
        serverkey: str | None = None,
    ):
        """
        Initialize ZeroMQ `Backend`.
        """

        super().__init__(
            backend=backend,
            frontend=frontend,
            name=name,
            mode=mode,
            attach=attach,
            publickey=publickey,
            secretkey=secretkey,
            serverkey=serverkey,
        )
        # Backend Only
        self.socket = self.backend()

    async def recv(self):
        """
        Receive `Request` (JSON).
        """
        response = await self.socket.recv_multipart()
        return Data.recv(response)

    async def send(self, __head__: dict | None = None, **kwargs: Any):
        """
        Send `Response` (JSON).

        Args:
            __head__ (dict | None): Request headers.
            body (**kwargs): Request body.

        Example:

        ```python
        backend = zmag.Backend(...)

        backend.send({"token":"secret"}, message = "hello world")
        ```
        """
        serialized = Data(head=__head__ or {}, body=kwargs)
        message = serialized.send(command="response", node=self.name)
        await self.socket.send_multipart(message)

    async def publish(self, channel, data: Data):
        """
        Send `Pub` (JSON).

        Args:
            data (Data): _description_

        Example:

        ```python
        backend = zmag.Backend(...)

        data = zmag.Data(body={"message": "hello world"})

        backend.publish("channel", data)
        ```
        """
        message = data.send(channel, command="pub", node=self.name)
        await self.socket.send_multipart(message)

    async def push(self, data: Data):
        """
        Send `Push` Work (JSON).

        Args:
            data (Data): _description_

        Example:

        ```python
        backend = zmag.Backend(...)

        data = zmag.Data(body={"message": "hello world"})

        backend.push(data)
        ```
        """
        message = data.send(command="push", node=self.name)
        await self.socket.send_multipart(message)


class FrontendZMQ(ZeroMQ):
    """
    ZeroMQ `Frontend` Client
    """

    def __init__(
        self,
        mode: str = "queue",
        host: str = tcp_string(5555),  # inproc://clients
        timeout: int = 5000,
        is_sync: bool = False,
        # SSH
        ssh: ConfigSSH | None = None,
        # Authenticator
        publickey: str | None = None,
        secretkey: str | None = None,
        serverkey: str | None = None,
    ):
        """
        Initialize ZeroMQ `Frontend`.

        Args:
            host (str, optional): _description_.
            timeout (int, optional): _description_.
            is_sync (bool, optional): _description_.
            ssh (ConfigSSH | None, optional): _description_.
            publickey (str | None, optional): _description_.
            secretkey (str | None, optional): _description_.
            serverkey (str | None, optional): _description_.
        """
        super().__init__(
            backend=host,
            frontend=host,
            mode=mode,
            timeout=timeout,
            is_sync=is_sync,
            ssh=ssh,
            publickey=publickey,
            secretkey=secretkey,
            serverkey=serverkey,
        )

    async def __request_async(self, __head__: dict, **data: Any):
        """
        Sends an asynchronous request to the server.
        """
        response = None
        with self.connect() as request:
            # async for request in self.connect(True):
            request_data = Data(head=__head__, body=data)
            await request.send_multipart(request_data.send())
            response = await request.socket.recv_multipart()
            response = Data.recv(response)
        return response or Data()

    def __request_sync(self, __head__: dict, **data: Any):
        """
        Sends a synchronous request to the server.
        """
        response = None
        with self.connect() as request:
            request_data = Data(head=__head__, body=data)
            request.send_multipart(request_data.send())
            response = request.recv_multipart()
            response = Data.recv(response)
        return response or Data()

    def request(
        self,
        query: str | None = None,
        operation: str | None = None,
        variables: dict | None = None,
        context: dict | None = None,
    ) -> Any:
        """
        Sends a `Request` to the server.

        Args:
            query (str | None, optional): _description_.
            operation (str | None, optional): _description_.
            variables (dict | None, optional): _description_.
            context (dict | None, optional): _description_.

        Example:

        ```python
        client = zmag.Frontend(...)

        response = await client.request(...)
        print(response)
        ```
        """

        head = {
            "context": context,
        }
        kwargs = {
            "query": query,
            "variables": variables,
            "operation": operation,
        }
        if self.is_sync:
            return self.__request_sync(head, **kwargs)
        return self.__request_async(head, **kwargs)

    async def __subscribe_async(self, channel: str = "") -> Any:
        """
        Subscribes to a ZeroMQ channel asynchronously.
        """
        response = None
        with self.connect(channel) as socket:
            message = await socket.recv_multipart()
            response = Data.recv(message)
        return response

    def __subscribe_sync(self, channel: str = "") -> Any:
        """
        Subscribes to a ZeroMQ channel synchronously.
        """
        response = None
        with self.connect(channel) as socket:
            message = socket.recv_multipart()
            response = Data.recv(message)
        return response

    def subscribe(self, channel: str = "") -> Any:
        """
        Subscribes to a ZeroMQ channel to receive messages and updates in real-time.

        Args:
            channel (str): _description_.

        Example:

        ```python
        client = zmag.Frontend(...)

        while True:
            message = await client.subscribe("") # or "some_channel"
            print("Received:", message)
        ```
        """

        if self.is_sync:
            return self.__subscribe_sync(channel)
        return self.__subscribe_async(channel)

    def pull(self) -> Any:
        """
        Consumes data from a ZeroMQ producer, processing incoming workloads.

        Example:

        ```python
        client = zmag.Frontend(...)

        while True:
            work = await client.pull()
            print("Received:", work)
        ```
        """
        if self.is_sync:
            return self.__subscribe_sync("")
        return self.__subscribe_async("")
