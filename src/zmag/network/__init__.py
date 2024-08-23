# -*- coding: utf-8 -*-
"""
ZMQ Network
"""

# import logging
from typing import Any

from .base import ConfigSSH, ZeroMQ, tcp_string
from .utils import Data


class DeviceZMQ(ZeroMQ):
    pass


class BackendZMQ(ZeroMQ):
    """ZMQ Server"""

    app: Any
    data: Any = Data

    def __init__(
        self,
        backend: str = tcp_string(5556),  # inproc://workers
        frontend: str = tcp_string(5555),  # inproc://clients
        mode: str = "queue",
        attach: bool = False,
        # SSH
        ssh: ConfigSSH | None = None,
        # Authenticator
        publickey: str | None = None,
        secretkey: str | None = None,
    ):
        """
        Initialize ZeroMQ `Backend`.
        """

        super().__init__(
            backend=backend,
            frontend=frontend,
            mode=mode,
            attach=attach,
            ssh=ssh,
            publickey=publickey,
            secretkey=secretkey,
        )
        # Backend Only
        self.socket = self.backend()

    async def recv(self):
        """
        Receive `Request` (JSON).
        """
        response = await self.socket.recv_multipart()
        return Data.recv(response)

    async def send(self, __head__: dict, **data: Any):
        """
        Send `Response` (JSON).
        """
        serialized = Data(head=__head__, body=data)
        message = serialized.send(command="response", node=self.name)
        await self.socket.send_multipart(message)

    async def publish(self, channel, serialized: Data):
        """
        Send `Pub` (JSON).
        """
        message = serialized.send(channel, command="pub", node=self.name)
        await self.socket.send_multipart(message)

    async def push(self, serialized: Data):
        """
        Send `Push` Work (JSON).
        """
        message = serialized.send(command="push", node=self.name)
        await self.socket.send_multipart(message)


class FrontendZMQ(ZeroMQ):
    """ZMQ Client"""

    def __init__(
        self,
        host: str = tcp_string(5555),  # inproc://clients
        mode: str = "queue",
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
        Send a `Request` to the server.
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
        Subscribes to a ZMQ channel asynchronously.
        """
        response = None
        with self.connect(channel) as socket:
            message = await socket.recv_multipart()
            response = Data.recv(message)
        return response

    def __subscribe_sync(self, channel: str = "") -> Any:
        """
        Subscribes to a ZMQ channel synchronously.
        """
        response = None
        with self.connect(channel) as socket:
            message = socket.recv_multipart()
            response = Data.recv(message)
        return response

    def subscribe(self, channel: str = "") -> Any:
        """
        Subscribe to ZMQ Channel
        """
        if self.is_sync:
            return self.__subscribe_sync(channel)
        return self.__subscribe_async(channel)

    def pull(self) -> Any:
        """
        Consume from ZMQ Producer
        """
        if self.is_sync:
            return self.__subscribe_sync("")
        return self.__subscribe_async("")
