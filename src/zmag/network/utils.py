# -*- coding: utf-8 -*-
"""
ZeroMQ Data Tools
"""

import binascii
import dataclasses as dc
import zlib
from enum import Enum
from typing import Any, List, Optional

import orjson


class Command(Enum):
    """ZeroMQ Socket Commands"""

    HEARTBEAT = b"\x01"
    PING = b"\x02"
    PONG = b"\x03"
    REQUEST = b"\x04"
    RESPONSE = b"\x05"
    PUB = b"\x06"
    PUSH = b"\x07"


COMMAND_NAME = {cmd.name: cmd.value for cmd in Command}
COMMAND_TYPE = {cmd.value: cmd.name for cmd in Command}


def checksum(data):
    """CheckSum"""
    return binascii.crc32(data) & 0xFFFFFFFF


def is_bytes(value):
    """IS Bytes"""
    return isinstance(value, bytes)


class OrJSON:
    """Wrapper for `orjson`"""

    @staticmethod
    def dumps(data: Any):
        """Dump"""
        return orjson.dumps(data)  # pylint: disable=maybe-no-member

    @staticmethod
    def loads(data: Any):
        """Load"""
        return orjson.loads(data)  # pylint: disable=maybe-no-member


class SerializerJSON:
    """
    Serializes and Deserializes to a JSON byte string.
    """

    _serializer: Any = OrJSON

    @classmethod
    def load_meta(cls, meta: Any) -> Any:
        """
        Decompresses and deserializes a JSON byte string.
        """
        try:
            return cls._serializer.loads(meta.decode("utf-8"))
        except (zlib.error, Exception) as e:
            raise ValueError(f"Error deserializing data: {e}") from e

    @classmethod
    def dumps(cls, meta: Any, head: Any, body: Any) -> Any:
        """
        Serializes and compresses to a JSON byte string.
        """

        try:
            # Head & Body
            _body = cls._serializer.dumps(body)
            _head = cls._serializer.dumps(head)
            _body = _body if is_bytes(_body) else _body.encode("utf-8")
            _head = _head if is_bytes(_head) else _head.encode("utf-8")
            # Compress
            _body = zlib.compress(_body)
            # Meta
            meta["checksum"] = checksum(_body)
            _meta = cls._serializer.dumps(meta)
            _meta = _meta if is_bytes(_meta) else _meta.encode("utf-8")
            return [_meta, _head, _body]
        except (TypeError, Exception) as e:
            raise ValueError(f"Error serializing data: {e}") from e

    @classmethod
    def loads(cls, meta: bytes, head: bytes, body: bytes) -> Any:
        """
        Decompresses and deserializes a JSON byte string.
        """

        try:
            # Meta
            _meta = cls._serializer.loads(meta.decode("utf-8"))
            # Head & Body
            if checksum(body) == _meta.get("checksum"):
                _body = cls._serializer.loads(zlib.decompress(body).decode("utf-8"))
                _head = cls._serializer.loads(head.decode("utf-8"))
                return [_meta, _head, _body]
            raise ValueError("Checksum verification failed")
        except (zlib.error, Exception) as e:
            raise ValueError(f"Error deserializing data: {e}") from e


class Serializer:
    """
    Serializes and Deserializes to a JSON byte string.
    """

    _serializer: Any = SerializerJSON

    @classmethod
    def set_serializer(cls, serializer: Any) -> Any:
        """Set Custom Serializer."""
        cls._serializer = serializer

    @classmethod
    def load_meta(cls, meta: Any) -> Any:
        """Decompresses and deserializes a JSON byte string."""
        return cls._serializer.load_meta(meta)

    @classmethod
    def dumps(cls, meta: Any, head: Any, body: Any) -> Any:
        """
        Serializes and compresses to a JSON byte string.
        """
        return cls._serializer.dumps(meta, head, body)

    @classmethod
    def loads(cls, meta: bytes, head: bytes, body: bytes) -> Any:
        """Decompresses and deserializes a JSON byte string."""
        return cls._serializer.loads(meta, head, body)


@dc.dataclass
class Data:
    """
    A utility class for handling JSON serialization and compression for ZMQ communication.
    """

    meta: dict = dc.field(default_factory=dict)
    head: dict = dc.field(default_factory=dict)
    body: dict = dc.field(default_factory=dict)

    def __post_init__(self):
        self.meta = self.meta or {}
        self.head = self.head or {}
        self.body = self.body or {}

    @classmethod
    def set_serializer(cls, serializer: Any) -> Any:
        """
        Set Custom Serializer
        """
        Serializer.set_serializer(serializer)

    @classmethod
    def recv(cls, message: Optional[List[bytes]]) -> Any:
        """
        Receives and deserializes a ZeroMQ message.
        """
        # Data(meta, head, body)
        # message.pop(0)
        if message and isinstance(message, (list, tuple)):
            try:
                command = COMMAND_TYPE.get(message[1])
                if command in ["HEARTBEAT", "PING", "PONG"]:
                    data = cls(Serializer.load_meta(message[2]))
                    return data
                return cls(*Serializer.loads(*message[2:]))
            except IndexError:
                pass
        return cls()

    def send(
        self,
        channel: str = "",
        command: str = "request",
        node: str = "",
    ) -> List[bytes]:
        """
        Serializes and compresses data to send as a ZeroMQ message.
        """
        command_name = command.upper()
        command_type = COMMAND_NAME.get(command_name, COMMAND_NAME.get("REQUEST"))
        self.meta["command"] = command_name
        self.meta["channel"] = channel.lower()
        self.meta["node"] = node.lower()
        return [
            self.meta["channel"].encode("utf-8"),  # Frame 0: Channel or Empty
            command_type,  # Frame 2: Command-Type (e.g: `x01` for Heartbeat)
        ] + Serializer.dumps(self.meta, self.head, self.body)
