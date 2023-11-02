"""
    Run the API
"""

# Python | (JSON + ZLIB)
import json
import zlib
from types import SimpleNamespace
import threading

# Create thread-local storage for the request data
thread_local = threading.local()

# ZMQ
import zmq
import zmq.asyncio
from zmq.devices import ProcessDevice

# https://pyzmq.readthedocs.io/en/latest/howto/ssh.html
from zmq import ssh


def api_data(body: dict = {}, head: dict = {}):
    return {"head": head, "body": body}


async def server(device=False):
    """Start { ZMQ-GraphQL } Server"""
    from .framework import Framework

    app = Framework()

    proxy = app.zmq

    if device:
        # Device
        proxy.device()

    # Server
    proxy.server()

    # Run Server
    while True:
        # Request
        request = await proxy.recv()
        client_request_body = request.body

        # Store the request data in the thread-local storage
        thread_local.request = request

        # GraphQL
        response = await app.execute(
            client_request_body.get("query"),
            variables=client_request_body.get("variables"),
            operation=client_request_body.get("operation"),
            context=client_request_body.get("context"),
        )

        # Response
        await proxy.send(**response)


class JSON:
    @staticmethod
    def dumps(data):
        json_bytes = json.dumps(data).encode("utf-8")
        return zlib.compress(json_bytes)

    @staticmethod
    def loads(compressed_data):
        data = zlib.decompress(compressed_data)
        return SimpleNamespace(**json.loads(data.decode("utf-8")))


class ZMQ:
    def __init__(
        self,
        server_uri: str = "tcp://127.0.0.1:5556",
        client_uri: str = "tcp://127.0.0.1:5555",
        ssh_host: str | None = None,
        ssh_keyfile: str | None = None,
    ):
        """
        Initialize the ManagerZMQ.

        Args:
            server_uri (str): The URI for the server socket.
            client_uri (str): The URI for the client socket.
            ssh_host (str): The Host for the remote-server.
            ssh_keyfile (str): The Path for `keyfile` the remote-server.
        """
        # URI(s)
        self.uri_server = server_uri
        self.uri_client = client_uri

        # SSH
        self.ssh_host = ssh_host
        self.ssh_keyfile = ssh_keyfile

        # ZMQ
        self.context = zmq.asyncio.Context()
        self.socket = None

    def device(self):
        """
        Configure and start the ZeroMQ device.
        """
        proxy = ProcessDevice(zmq.FORWARDER, zmq.ROUTER, zmq.DEALER)
        proxy.bind_in(self.uri_client)
        proxy.bind_out(self.uri_server)
        proxy.start()

    def server(self):
        """
        Configure and start the server socket.
        """
        self.socket = self.context.socket(zmq.REP)
        self.socket.connect(self.uri_server)

    async def recv(self):
        """
        Receive Request (JSON).
        """
        if self.socket:
            message = await self.socket.recv_multipart()
            if len(message) > 0:
                return JSON.loads(message[0])
        return SimpleNamespace()

    async def send(self, __head__=None, **data: dict):
        """
        Send Response (JSON).
        """
        if self.socket:
            compressed = JSON.dumps(api_data(data, __head__))
            await self.socket.send_multipart([compressed])
