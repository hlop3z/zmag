from __future__ import annotations

from dataclasses import dataclass as dc_dataclass
from dataclasses import field as dc_field
from dataclasses import fields as dc_fields
from typing import dataclass_transform  # Python 3.12+
from typing import Any, Callable, TypeVar, overload

from sqlalchemy import Column, ForeignKey, Computed
from sqlalchemy.sql.base import _NoArg
from sqlalchemy.sql.schema import _ServerDefaultArgument

from ._components import components

T = TypeVar("T", bound=type[Any])

# ---------------------------------------------------------------------------
# Utils
# ---------------------------------------------------------------------------


@dc_dataclass
class SQLMeta:
    fields: Any
    index: list[tuple[str, ...]] | None = None
    unique: list[tuple[str, ...]] | None = None
    required: list[str] | None = None
    sortable: list[str] | None = None
    form_create: list[str] | None = None
    form_update: list[str] | None = None


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


@overload
def model(
    _cls: None = None,
    *,
    is_abstract: bool = False,
    index: list[tuple[str, ...]] | None = None,
    unique: list[tuple[str, ...]] | None = None,
    required: list[str] | None = None,
    sortable: list[str] | None = None,
    form_create: list[str] | None = None,
    form_update: list[str] | None = None,
) -> Callable[[T], T]: ...


@overload
def model(
    _cls: T,
    *,
    is_abstract: bool = False,
    index: list[tuple[str, ...]] | None = None,
    unique: list[tuple[str, ...]] | None = None,
    required: list[str] | None = None,
    sortable: list[str] | None = None,
    form_create: list[str] | None = None,
    form_update: list[str] | None = None,
) -> T: ...


@dataclass_transform()
def model(
    _cls: T | None = None,
    *,
    is_abstract: bool = False,
    index: list[tuple[str, ...]] | None = None,
    unique: list[tuple[str, ...]] | None = None,
    required: list[str] | None = None,
    sortable: list[str] | None = None,
    form_create: list[str] | None = None,
    form_update: list[str] | None = None,
) -> T | Callable[[T], T]:

    def decorator(cls: T) -> T:
        dataclass_cls = dc_dataclass(cls, eq=False)
        if not is_abstract:
            __meta = SQLMeta(
                fields=dc_fields(dataclass_cls),
                index=index or [],
                unique=unique or [],
                required=required or [],
                sortable=sortable or [],
                form_create=form_create or [],
                form_update=form_update or [],
            )
            components.register("models", dataclass_cls, config={"sql": __meta})
        return dataclass_cls

    return decorator if _cls is None else decorator(_cls)


# ---------------------------------------------------------------------------
# Fields
# ---------------------------------------------------------------------------


def field(
    col_type: Any,
    m2m: bool = False,
    computed: str | None = None,
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
        with_computed = []
        if computed:
            with_computed.append(Computed(computed, persisted=True))
        if table_uri and isinstance(col_type, str):
            _col_type = ForeignKey(table_uri)
        return Column(name, _col_type, *with_computed, **column_args)

    _default = default if default is not _NoArg.NO_ARG else None
    _meta = {
        "sql": sql_column,
        "order": sort_order,
        "refs": col_type if isinstance(col_type, str) else None,
        "nullable": nullable,
        "metadata": (meta or {}),
        "many_to_many": m2m,
    }

    return (
        dc_field(default_factory=_default, metadata=_meta)
        if callable(_default)
        else dc_field(default=_default, metadata=_meta)
    )
