import json
import zlib
from string import Template
from types import SimpleNamespace
from pathlib import Path

# ZMQ
import zmq
import zmq.asyncio


CURRENT_PATH = Path(__file__).parent


QUERY_INFO = """
query {
  info {
    models
    fields
    query
    mutation
    forms
    objects
  }
}
"""


def tcp_port(port):
    return f"tcp://127.0.0.1:{port}"


class Data:
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

    @classmethod
    def recv(cls, message):
        if len(message) > 0:
            return cls.loads(message[0])
        return SimpleNamespace()

    @classmethod
    def send(cls, __head__=None, **data: dict):
        compressed = cls.dumps(cls.api_config(data, __head__))
        return [compressed]

    @staticmethod
    def api_config(body: dict = {}, head: dict = {}):
        return {"head": head, "body": body}


class ClientZMQ:
    def __init__(
        self,
        client_uri: str = "tcp://127.0.0.1:5555",
        timeout: int = 5000,
    ):
        """
        Initialize the ZMAG Manager.

        Args:
            client_uri (str): The URI for the client socket.
        """
        # URI(s)
        self.uri_client = client_uri
        self.timeout = timeout

        # ZMQ
        self.socket = None

    async def request(self, __head__=None, **data):
        context = zmq.asyncio.Context()
        socket = context.socket(zmq.REQ)
        socket.setsockopt(zmq.RCVTIMEO, self.timeout)

        socket.connect(self.uri_client)
        return_value = SimpleNamespace(error=None, data=None)

        try:
            # Asynchronous Request
            await socket.send_multipart(Data.send(__head__=__head__, **data))
            response = await socket.recv_multipart()
            response = Data.recv(response)
            return_value = self.transform_response(response)

        finally:
            socket.close()
            context.term()
            return return_value

    def request_sync(self, __head__=None, **data):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect(self.uri_client)
        return_value = SimpleNamespace(error=None, data=None)

        try:
            # Synchronous Request
            socket.send_multipart(Data.send(__head__=__head__, **data))
            response = socket.recv_multipart()
            response = Data.recv(response)
            return_value = self.transform_response(response)

        finally:
            socket.close()
            context.term()
            return return_value

    def transform_response(self, response):
        return_value = SimpleNamespace()
        return_value.error = None
        return_value.data = response.body.data

        # Return
        return return_value


class Operations:
    def __init__(self, base_dir: Path, fragments: dict = None):
        self.base_dir = base_dir
        self.model = {}
        self.load_template(CURRENT_PATH / "operations.graphql")
        if fragments:
            self.load_fragments(fragments)

    def load_template(self, operations_file):
        with open(operations_file, "r", encoding="utf-8") as file:
            self.operations = Template(file.read())

    def load_fragments(self, fragments):
        for key, val in fragments.items():
            self.fragment(key, val)

    def fragment(self, model: str, fragments_file: Path):
        query = self.operations.safe_substitute({"MODEL": f"{model}"})
        with open(self.base_dir / fragments_file, "r", encoding="utf-8") as file:
            query += file.read()
        # Register
        self.model[model] = query


class Client:
    def __init__(
        self,
        host: str = None,
        base_dir: Path = None,
        fragments: dict = None,
        sync: bool = True,
    ):
        self.sync = sync
        self.client = ClientZMQ(host or tcp_port(5555))
        self.graphql = Operations(
            base_dir=base_dir,
            fragments=fragments,
        )

    def request(self, query=None, operation=None, variables=None, context=None):
        if self.sync:
            return self.client.request_sync(
                query=query,
                variables=variables,
                operation=operation,
                context=context,
            )
        # Async
        return self.client.request(
            query=query,
            variables=variables,
            operation=operation,
            context=context,
        )

    # Info
    def info(
        self,
        context: dict | None = None,
    ):
        return self.request(
            query=QUERY_INFO, operation=None, variables=None, context=context
        )

    # Mutation
    def create(
        self,
        model: str,
        form: dict,
        context: dict | None = None,
    ):
        graphql_query = self.graphql.model.get(model)
        operation = "Create"
        variables = {
            "form": form,
        }
        return self.request(
            query=graphql_query,
            operation=operation,
            variables=variables,
            context=context,
        )

    def update(
        self,
        model: str,
        form: dict,
        context: dict | None = None,
    ):
        graphql_query = self.graphql.model.get(model)
        operation = "Update"
        variables = {
            "form": form,
        }
        return self.request(
            query=graphql_query,
            operation=operation,
            variables=variables,
            context=context,
        )

    def delete(
        self,
        model: str,
        ids: list[str],
        context: dict | None = None,
    ):
        graphql_query = self.graphql.model.get(model)
        operation = "Delete"
        variables = {
            "ids": ids,
        }
        return self.request(
            query=graphql_query,
            operation=operation,
            variables=variables,
            context=context,
        )

    def create_many(
        self,
        model: str,
        forms: list[dict],
        context: dict | None = None,
    ):
        graphql_query = self.graphql.model.get(model)
        operation = "CreateMany"
        variables = {
            "forms": forms,
        }
        return self.request(
            query=graphql_query,
            operation=operation,
            variables=variables,
            context=context,
        )

    def update_many(
        self,
        model: str,
        ids: list[str],
        form: dict,
        context: dict | None = None,
    ):
        graphql_query = self.graphql.model.get(model)
        operation = "UpdateMany"
        variables = {
            "ids": ids,
            "form": form,
        }
        return self.request(
            query=graphql_query,
            operation=operation,
            variables=variables,
            context=context,
        )

    # Query
    def detail(
        self,
        model: str,
        id: str,
        context: dict | None = None,
    ):
        graphql_query = self.graphql.model.get(model)
        operation = "Detail"
        variables = {
            "id": id,
        }
        return self.request(
            query=graphql_query,
            operation=operation,
            variables=variables,
            context=context,
        )

    def filter(
        self,
        model: str,
        query: list | None = None,
        page: int = 1,
        limit: int = 100,
        sort: str = "-id",
        all: bool = False,
        context: dict | None = None,
    ):
        graphql_query = self.graphql.model.get(model)
        operation = "Filter"
        variables = {
            "page": page,
            "limit": limit,
            "sort": sort,
            "all": all,
        }
        if query:
            variables["query"] = query
        return self.request(
            query=graphql_query,
            operation=operation,
            variables=variables,
            context=context,
        )
