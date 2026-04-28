from sqlalchemy.sql.schema import _ServerDefaultArgument
from sqlalchemy.sql.base import _NoArg
from sqlalchemy import (  # noqa: F401
    # Table Utils
    Table,
    Column,
    MetaData,
    # Modifiers
    Index,
    UniqueConstraint,
    # Field Types
    ForeignKey,
    Integer,
    DateTime,
    String,
    Uuid,
    # Tools
    func,
)

from sqlalchemy import create_engine

import uuid
from dataclasses import field as dc_field
from typing import Any, Callable, overload
from dataclasses import dataclass as dc_dataclass
from dataclasses import fields
from datetime import datetime
from typing import Optional as Field


from typing import dataclass_transform  # Python 3.12+


def create_unique(table, left, right):
    return f"uq_{table}_{left}_{right}"


def create_index(table, left, right):
    return f"ix_{table}_{left}_{right}"


METADATA = MetaData()


@dc_dataclass
class SQLModel:
    columns: list[Any]
    unique: list | None = None
    index: list | None = None


@dc_dataclass
class Form:
    create: list[str]
    update: list[str]
    required: list[str]
    nullable: list[str]


@overload
def model(
    _cls: None = None,
    *,
    is_abstract: bool = False,
    index: list[tuple[str]] | None = None,
    unique: list[tuple[str]] | None = None,
    required: list[str] | None = None,
    form_create: list[str] | None = None,
    form_update: list[str] | None = None,
) -> Callable[[type[Any]], type[Any]]: ...


@overload
def model(
    _cls: type[Any],
    *,
    is_abstract: bool = False,
    index: list[tuple[str]] | None = None,
    unique: list[tuple[str]] | None = None,
    required: list[str] | None = None,
    form_create: list[str] | None = None,
    form_update: list[str] | None = None,
) -> type[Any]: ...


@dataclass_transform()
def model(
    _cls: type[Any] | None = None,
    *,
    is_abstract: bool = False,
    index: list[tuple[str]] | None = None,
    unique: list[tuple[str]] | None = None,
    required: list[str] | None = None,
    form_create: list[str] | None = None,
    form_update: list[str] | None = None,
) -> Callable[[type[Any]], type[Any]] | type[Any]:
    def wrap(cls: type[Any]) -> type[Any]:
        dataclass_cls = dc_dataclass(cls)
        dataclass_cls.__sql__ = SQLModel([], [], [])
        if not is_abstract:
            # SQL Columns
            db_cols = []
            null_cols = []
            for col in fields(dataclass_cls):
                column: Any = col.metadata.get("sql")
                if column:
                    refs_str = col.metadata.get("refs")
                    db_cols.append(
                        (col.metadata.get("order", 0), column(col.name, refs_str))
                    )
                    if col.metadata.get("nullable", False):
                        null_cols.append(col.name)
            db_cols = sorted(db_cols, key=lambda x: x[0])
            # MetaData
            dataclass_cls.__api__ = Form(
                form_create or [],
                form_update or [],
                required or [],
                null_cols,
            )
            dataclass_cls.__sql__ = SQLModel(
                columns=[col[1] for col in db_cols],
                index=index,
                unique=unique,
            )
        return dataclass_cls

    return wrap if _cls is None else wrap(_cls)


def field(
    col_type: Any = None,
    meta: dict[str, Any] | None = None,
    autoincrement: bool = False,
    default: Any = _NoArg.NO_ARG,
    index: bool = False,
    nullable: bool = False,
    onupdate: Any | None = None,
    primary_key: bool = False,
    server_default: _ServerDefaultArgument | None = None,
    unique: bool | None = None,
    sort_order: int = 0,
) -> Any:
    """Create a dataclass field with SQLAlchemy Column metadata support."""

    column_args = {
        "autoincrement": autoincrement,
        "default": default,
        "index": index,
        "nullable": nullable,
        "onupdate": onupdate,
        "primary_key": primary_key,
        "server_default": server_default,
        "unique": unique,
    }

    # remove unset values (keeps Column clean)
    column_args = {k: v for k, v in column_args.items() if v is not None}

    def sql_column(name, table_uri: str | None = None):
        _col_type = col_type
        if table_uri and isinstance(col_type, str):
            _col_type = ForeignKey(table_uri)
        return Column(name, _col_type, **column_args)

    _default = default if default is not _NoArg.NO_ARG else None
    _meta = {
        "sql": sql_column,
        "order": sort_order,
        "refs": col_type if isinstance(col_type, str) else None,
        "nullable": nullable,
        "metadata": (meta or {}),
    }

    return (
        dc_field(default_factory=_default, metadata=_meta)
        if callable(_default)
        else dc_field(default=_default, metadata=_meta)
    )


@model(is_abstract=True)
class Base:
    # d46b8b31-3163-4b5e-8646-a9ffe674775c
    id: Field[str] = field(Uuid, primary_key=True, default=uuid.uuid4, sort_order=-100)


@model(is_abstract=True)
class Mixin:
    created_at: Field[datetime] = field(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        sort_order=9991,
    )
    updated_at: Field[datetime] = field(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        sort_order=9992,
    )


# --------------------
# Models
# --------------------
@model(required=["name"], form_create=["name"], form_update=["docs"])
class User(Mixin, Base):
    name: Field[str] = field(String, index=True)
    docs: Field[str] = field(String, nullable=True)


@model
class Blog(Mixin, Base):
    name: Field[str] = field(String, index=True)
    owner_id: Field[str] = field("user.id")


users = Table("user", METADATA, *User.__sql__.columns)
blogs = Table("blog", METADATA, *Blog.__sql__.columns)

print(User.__api__)
User("d46b8b31-3163-4b5e-8646-a9ffe674775c")

# --------------------
# Engine
# --------------------
# engine = create_engine("sqlite:///app.sqlite3", echo=True)


# --------------------
# Create tables
# --------------------
# METADATA.create_all(engine)

print(type(fields(User)))
