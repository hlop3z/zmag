# -*- coding: utf-8 -*-
"""
ZMQ Core
"""

# Python
import dataclasses as dc
import logging
import uuid
from collections import namedtuple
from contextlib import contextmanager
from types import SimpleNamespace
from typing import Any, Tuple  # Literal

# ZMQ
import zmq
import zmq.asyncio
import zmq.auth
from zmq.devices import Device  # ThreadDevice

# https://pyzmq.readthedocs.io/en/latest/howto/ssh.html
from zmq.ssh.tunnel import tunnel_connection

Mesh = namedtuple("Mesh", ["device", "backend", "frontend"], module="ZeroMQ")


class CustomDevice(Device):
    """Device with Authentication"""

    def set_auth(self, auth):
        """Set Authentication Handler"""
        self.auth = auth

    def _setup_sockets(self) -> Tuple[zmq.Socket, zmq.Socket]:
        ctx: zmq.Context[zmq.Socket] = self.context_factory()  # type: ignore
        self._context = ctx

        # create the sockets
        ins = ctx.socket(self.in_type)
        self._sockets.append(ins)
        if self.out_type < 0:
            outs = ins
        else:
            outs = ctx.socket(self.out_type)
            self._sockets.append(outs)

        # set Authentication
        self.auth(ins)
        self.auth(outs)

        # set sockopts (must be done first, in case of zmq.IDENTITY)
        for opt, value in self._in_sockopts:
            ins.setsockopt(opt, value)
        for opt, value in self._out_sockopts:
            outs.setsockopt(opt, value)

        for iface in self._in_binds:
            ins.bind(iface)
        for iface in self._out_binds:
            outs.bind(iface)

        for iface in self._in_connects:
            ins.connect(iface)
        for iface in self._out_connects:
            outs.connect(iface)

        return ins, outs


@dc.dataclass
class ConfigSSH:
    """
    ZeroMQ SSH Configuration

    - https://pyzmq.readthedocs.io/en/latest/howto/ssh.html

    """

    host: Any
    keyfile: Any | None = None
    password: Any | None = None
    paramiko: Any | None = None
    timeout: int = 60


@dc.dataclass
class Authenticator:
    """ZeroMQ Authenticator"""

    # Server
    publickey: bytes | str | None = None
    secretkey: bytes | str | None = None
    serverkey: bytes | str | None = None

    def __post_init__(self):
        if self.publickey and isinstance(self.publickey, str):
            self.publickey = self.publickey.encode("utf-8")
        if self.secretkey and isinstance(self.secretkey, str):
            self.secretkey = self.secretkey.encode("utf-8")
        if self.serverkey and isinstance(self.serverkey, str):
            self.serverkey = self.serverkey.encode("utf-8")

    def backend(self, socket):
        """Attach Backend Authenticator"""
        if self.publickey and self.secretkey:
            socket.curve_publickey = self.publickey
            socket.curve_secretkey = self.secretkey
            socket.curve_server = True

    def frontend(self, socket):
        """Attach Frontend Authenticator"""
        if self.publickey and self.secretkey and self.serverkey:
            socket.curve_publickey = self.publickey
            socket.curve_secretkey = self.secretkey
            socket.curve_serverkey = self.serverkey


def tcp_string(port: int = 5555, host: str = "127.0.0.1"):
    """
    Generates a TCP Address.

    Args:
        port (int): The port number.
        host (str): The host address.

    Returns:
        str: The TCP address for the local host with the specified port.
    """
    return f"tcp://{host}:{port}"


def zmq_context(is_sync: bool = False):
    """
    Get ZeroMQ `Context`.
    """
    if is_sync:
        context = zmq.Context()
    else:
        context = zmq.asyncio.Context()  # type: ignore
    return context


def network_types(type_name: str = "queue") -> Any:
    """
    Get **ZeroMQ Types** for `Device` and `Socket`.

    Options:
        - `queue`       for (`Request` and `Response`)
        - `forwarder`   for (`Publisher` and `Subscriber`)
        - `streamer`    for (`Producer` and `Consumer`)
    """
    match type_name.lower():
        case "streamer":
            return Mesh(
                device=Mesh(zmq.STREAMER, zmq.PULL, zmq.PUSH),
                frontend=zmq.PULL,
                backend=zmq.PUSH,
            )
        case "forwarder":
            return Mesh(
                device=Mesh(zmq.FORWARDER, zmq.SUB, zmq.PUB),
                frontend=zmq.SUB,
                backend=zmq.PUB,
            )
        case "queue" | _:
            return Mesh(
                device=Mesh(zmq.QUEUE, zmq.ROUTER, zmq.DEALER),
                frontend=zmq.REQ,  # ROUTER
                backend=zmq.REP,  # DEALER
            )


class ZeroMQ:
    """ZeroMQ Manager"""

    tcp = tcp_string

    def __init__(
        self,
        backend: str = tcp_string(5556),  # inproc://workers
        frontend: str = tcp_string(5555),  # inproc://clients
        name: str | None = None,
        mode: str = "queue",
        timeout: int = 5000,
        is_sync: bool = False,
        attach: bool = False,
        # SSH
        ssh: ConfigSSH | None = None,
        # Authenticator
        publickey: Any | None = None,
        secretkey: Any | None = None,
        serverkey: Any | None = None,
    ):
        """
        Initialize ZeroMQ.
        """
        # Generate a random UUID (UUID4)
        self.name = name or str(uuid.uuid4())

        # Options
        self.timeout = timeout
        self.ssh = ssh
        self.auth = Authenticator(publickey, secretkey, serverkey)
        self.url = SimpleNamespace(backend=backend, frontend=frontend)

        # ZMQ
        self.mode = mode
        self.attach = attach
        self.is_sync = is_sync
        self.mesh = network_types(mode)
        self.context = zmq_context(is_sync)

    def get_context(self):
        """
        Context `async` or `sync`
        """
        return zmq_context(self.is_sync)

    def device(self):
        """
        Start the ZeroMQ `Device`.
        """
        proxy: Any = CustomDevice(*tuple(self.mesh.device))

        # Authentication
        proxy.set_auth(self.auth.backend)

        # Binding
        if self.mode == "queue":
            proxy.bind_in(self.url.frontend)
            proxy.bind_out(self.url.backend)
        else:
            proxy.bind_in(self.url.backend)
            proxy.bind_out(self.url.frontend)

        # Pub/Sub
        if self.mode == "forwarder":
            proxy.setsockopt_in(zmq.SUBSCRIBE, b"")

        # Start
        proxy.start()
        return proxy

    def backend(self):
        """
        ZeroMQ backend `Server` establishes a `bind` or `connection` to the ZeroMQ socket.
        """
        # Context & Socket
        context: Any = self.get_context()
        socket: Any = context.socket(self.mesh.backend)
        # Connect
        if self.attach:
            # Authentication
            self.auth.frontend(socket)
            # Connect
            socket.connect(self.url.backend)
        else:
            # Authentication
            self.auth.backend(socket)
            # Bind
            socket.bind(self.url.backend)
        # Socket
        return socket

    def __connect(
        self, socket: Any, send_timeout: bool | int, receive_timeout: bool | int
    ):
        """
        Connect to the ZeroMQ socket.
        """
        if self.ssh:
            tunnel_connection(
                socket,
                self.url.frontend,  # "tcp://locahost:5555"
                self.ssh.host,  # "myuser@remote-server-ip"
                keyfile=self.ssh.keyfile,
                password=self.ssh.password,
                paramiko=self.ssh.paramiko,
                timeout=self.ssh.timeout,
            )
        else:
            socket.connect(self.url.frontend)
        # Timeouts
        if send_timeout:
            socket.setsockopt(
                zmq.SNDTIMEO,
                self.timeout if send_timeout is True else send_timeout,
            )
        if receive_timeout:
            socket.setsockopt(
                zmq.RCVTIMEO,
                self.timeout if receive_timeout is True else receive_timeout,
            )

    @contextmanager
    def connect(
        self,
        channel: str = "",
        send_timeout: bool | int = True,
        receive_timeout: bool | int = True,
        log_errors: bool = False,
    ):
        """
        ZeroMQ `Frontend` establishes a `connection` to the ZMQ socket.
        """
        # Context & Socket
        context: Any = self.get_context()
        socket: Any = context.socket(self.mesh.frontend)
        # Authentication
        self.auth.frontend(socket)
        # Request
        try:
            self.__connect(socket, send_timeout, receive_timeout)
            if self.mode == "forwarder":
                socket.setsockopt(zmq.SUBSCRIBE, channel.encode("utf-8"))
            # Pass the Socket
            yield socket
        except zmq.Again as e:
            if log_errors:
                logging.error(e)
            socket.setsockopt(zmq.LINGER, 0)
            socket.close()
        finally:
            socket.close()
            context.term()
