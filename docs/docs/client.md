## Usage (Code)

```python
GRAPHQL_QUERY = """
fragment Fields on Book {
  id
  author
  title
  books
}

query Detail($id: ID!) {
  BookDetail(id: $id) {
    ...Fields
  }
}
"""

client = Client()

req_head = {"token": "someTokenForUser"}
req_body = {
    "query": GRAPHQL_QUERY,
    "operation": "Detail",
    "variables": {"id": "MTo6YTU1ZTUzMmVhYjAyOGI0Mg=="},
}

response = client.request_sync(req_head, **req_body)
```

## Client (Code)

```python
from types import SimpleNamespace
import json
import zlib

# ZMQ
import zmq
import zmq.asyncio

from graphql import parse

class FileGraphQL:
    def __init__(self, file_path):
        self.file_path = file_path
        self.content = self.read_file()
        self.operations = self.extract_operations()

    @property
    def ops(self):
        return self.operations

    def read_file(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return None

    def extract_operations(self):
        schema = self.content
        parsed_schema = parse(schema)
        operations = {}
        for definition in parsed_schema.definitions:
            if hasattr(definition, "operation") and definition.operation:
                operation_name = definition.name.value
                variables = []
                if definition.variable_definitions:
                    for var in definition.variable_definitions:
                        var_name = var.variable.name.value
                        variables.append(var_name)
                operations[operation_name] = variables
        return operations

    def __call__(self, __operation__, **variables):
        if __operation__ not in self.operations:
            return None

        request = {
            "query": self.content,
            "operation": __operation__,
            "variables": variables,
        }
        return request


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


class Client:
    def __init__(
        self,
        client_uri: str = "tcp://127.0.0.1:5555",
    ):
        """
        Initialize the ZMAG Manager.

        Args:
            client_uri (str): The URI for the client socket.
        """
        # URI(s)
        self.uri_client = client_uri

        # ZMQ
        self.socket = None

    async def request(self, __head__=None, **data):
        context = zmq.asyncio.Context()
        socket = context.socket(zmq.REQ)
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
                    return_value.error = SimpleNamespace(
                        type="database",
                        path=error_path,
                        message=error_message.replace("DATABASE ERROR:", "").strip(),
                    )
                    response.body.errors = []
                # Not Authorized Error
                if error_message.startswith("UNAUTHORIZED"):
                    return_value.error = SimpleNamespace(
                        type="permissions",
                        path=error_path,
                        message=error_message,
                    )
                # Operational Error
                else:
                    return_value.error = SimpleNamespace(
                        type="operation",
                        path=error_path,
                        message=error_message,
                    )

        # Return
        return return_value

    @staticmethod
    def file(file_path):
        return FileGraphQL(file_path)

```
