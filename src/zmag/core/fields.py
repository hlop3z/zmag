"""
SQL type aliases and shorthand imports.
"""

from typing import Optional as use  # noqa: N811  (intentional alias)
from typing import TypeVar, Any
from typing import TYPE_CHECKING as typing  # noqa: N811

from sqlalchemy import (
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

from .settings import settings
from ..db.tables import BaseModel, Model, FullModel, Crud
from .decorators.models import field as col  # noqa: N811
from .decorators.models import model as type  # noqa: N811

if settings.db_engine == "postgres":
    from sqlalchemy.dialects.postgresql import JSONB as JSON
else:
    from sqlalchemy import JSON


T = TypeVar("T")

type refs[T] = list[T] | None
Dict = dict[str, Any]
List = list[Any]

int = Integer  # noqa: A001
int64 = BigInteger
str = String  # noqa: A001
text = Text
bool = Boolean  # noqa: A001
datetime = DateTime(timezone=True)
date = Date
time = Time  # noqa: A001
float = Float  # noqa: A001
numeric = Numeric
uuid = Uuid
enum = Enum
json = JSON
binary = LargeBinary

__all__ = (
    # Core
    "use",
    "col",
    "type",
    "typing",
    # Base Model
    "Model",
    "BaseModel",
    "FullModel",
    "Crud",
    # DataTypes
    "refs",
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
