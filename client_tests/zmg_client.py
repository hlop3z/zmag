from types import SimpleNamespace
import json
import zlib


# ZMQ
import zmq
import zmq.asyncio


# https://pyzmq.readthedocs.io/en/latest/howto/ssh.html
from zmq import ssh


def api_data(body: dict = {}, head: dict = {}):
    return {"head": head, "body": body}


class JSON:
    @staticmethod
    def dumps(data):
        json_bytes = json.dumps(data).encode("utf-8")
        return zlib.compress(json_bytes)

    @staticmethod
    def loads(compressed_data):
        data = zlib.decompress(compressed_data)
        ddict = SimpleNamespace(**json.loads(data.decode("utf-8")))
        ddict.body = SimpleNamespace(**ddict.body)
        return ddict


class ZMQ:
    def __init__(
        self,
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
        self.uri_client = client_uri

        # SSH
        self.ssh_host = ssh_host
        self.ssh_keyfile = ssh_keyfile

        # ZMQ
        self.context = zmq.asyncio.Context()
        self.socket = None

    def client(self):
        """
        Configure the client socket.
        """
        self.socket = self.context.socket(zmq.REQ)
        if self.ssh_host:
            # Tunnel Connect
            ssh.tunnel_connection(
                self.socket, self.uri_client, self.ssh_host, self.ssh_keyfile
            )
        else:
            # Connect
            self.socket.connect(self.uri_client)

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

    async def request(self, __head__=None, **data: dict):
        # Request
        await self.send(__head__, **data)

        # Response
        response = await self.recv()
        response.error = None

        # Server Errors
        if response.body.errors:
            if len(response.body.errors) == 1:
                current_error = response.body.errors[0]
                error_message = current_error.get("message")
                error_path = current_error.get("path")
                if len(error_path) == 1:
                    error_path = error_path[0]
                # Database Error
                if error_message.startswith("DATABASE ERROR:"):
                    response.error = SimpleNamespace(
                        type="database",
                        path=error_path,
                        message=error_message.replace("DATABASE ERROR:", "").strip(),
                    )
                    response.body.errors = []
                # Not Authorized Error
                if error_message.startswith("UNAUTHORIZED"):
                    response.error = SimpleNamespace(
                        type="permissions",
                        path=error_path,
                        message=error_message,
                    )

        # Return
        return response
