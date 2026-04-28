from typing import Optional as use

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Enum,
    Float,
    Integer,
    LargeBinary,
    Numeric,
    String,
    Text,
    Time,
    Uuid,
)

from ..framework.sql_model import field as col
from ..framework.sql_model import model as type
from ..framework.sql_settings import DB_ENGINE

if DB_ENGINE == "sqlite":
    json = JSON
else:
    json = JSONB

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
