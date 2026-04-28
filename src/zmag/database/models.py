from typing import Optional as use

from sqlalchemy import (
    Integer,
    BigInteger,
    String,
    Text,
    Boolean,
    DateTime,
    Date,
    Time,
    Float,
    Numeric,
    JSON,
    Uuid,
    Enum,
    LargeBinary,
)

from ..framework.sql_model import model as type
from ..framework.sql_model import field as col

json = JSON

int = Integer
int64 = BigInteger
str = String
text = Text
bool = Boolean
datetime = DateTime(timezone=True)
date = Date
time = Time
float = Float
numeric = Numeric
uuid = Uuid
enum = Enum
binary = LargeBinary

__all__ = (
    # Utils
    "type",
    "col",
    "use",
    # Types
    "int",
    "int64",
    "str",
    "text",
    "bool",
    "datetime",
    "date",
    "time",
    "float",
    "numeric",
    "json",
    "uuid",
    "enum",
    "binary",
)
