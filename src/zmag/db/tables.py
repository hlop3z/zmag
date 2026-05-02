from datetime import datetime, UTC
from uuid import uuid4, UUID
from typing import Any, Optional, Callable

from sqlalchemy import (
    func,
    Table,
    Column,
    DateTime,
    Uuid,
    insert,
    update,
    delete,
    select,
    Insert,
    Update,
    Delete,
    Select,
)
from sqlalchemy.sql.base import ReadOnlyColumnCollection

from ..core.decorators.models import field
from ..core.decorators.models import model

Col = ReadOnlyColumnCollection[str, Column[Any]]


FILTER_OPS: dict[str, Callable] = {
    "eq": lambda col, v: col == v,
    "ne": lambda col, v: col != v,
    "gt": lambda col, v: col > v,
    "gte": lambda col, v: col >= v,
    "lt": lambda col, v: col < v,
    "lte": lambda col, v: col <= v,
    "in": lambda col, v: col.in_(v),
    "nin": lambda col, v: col.not_in(v),
    "like": lambda col, v: col.like(v),
    "ilike": lambda col, v: col.ilike(v),
    # case-sensitive variants
    "contains": lambda col, v: col.contains(v),
    "startswith": lambda col, v: col.startswith(v),
    "endswith": lambda col, v: col.endswith(v),
    # case-insensitive variants — no manual copy/paste, just ilike + format
    "icontains": lambda col, v: col.ilike(f"%{v}%"),
    "istartswith": lambda col, v: col.ilike(f"{v}%"),
    "iendswith": lambda col, v: col.ilike(f"%{v}"),
    "isnull": lambda col, v: col.is_(None) if v else col.is_not(None),
}

FILTER_NAMES = tuple(FILTER_OPS.keys())


class M2MORM:
    table: Table  # junction table
    related_table: Table  # the table we actually SELECT from
    own_col: str  # junction col for the owning model's FK, e.g. "blog_id"
    related_col: str  # junction col linking to related_table, e.g. "user_id"

    def __init__(self, own_id):
        self._own_id = own_id

    @classmethod
    def col(cls, name: str) -> Col:
        return getattr(cls.table.c, name)

    @classmethod
    def all(cls) -> Select:
        """SELECT related.* JOIN through junction — no owner filter."""
        return select(cls.related_table).join(
            cls.table,
            getattr(cls.table.c, cls.related_col) == cls.related_table.c.id,
        )

    @classmethod
    def of(cls, own_id: str) -> Select:
        """All related records for this owner."""
        return cls.all().where(getattr(cls.table.c, cls.own_col) == own_id)

    @classmethod
    def add(cls, own_id: str, related: str):
        return insert(cls.table).values(
            **{cls.own_col: own_id, cls.related_col: related}
        )

    @classmethod
    def remove(cls, own_id: str, related: str):
        return (
            delete(cls.table)
            .where(getattr(cls.table.c, cls.own_col) == own_id)
            .where(getattr(cls.table.c, cls.related_col) == related)
        )


class ORM:
    table: Table

    _cached_cols = None

    @classmethod
    def col(cls, name: str) -> Col:
        return getattr(cls.table.c, name)

    @classmethod
    def _cols(cls) -> set[str]:
        if cls._cached_cols is None:
            cls._cached_cols = {k for k, c in cls.table.c.items() if c.computed is None}
        return cls._cached_cols

    @classmethod
    def _valid(cls, data: dict[str, Any]) -> dict[str, Any]:
        return {k: v for k, v in data.items() if k in cls._cols()}

    @classmethod
    def create(cls, data: dict[str, Any]) -> Insert:
        return insert(cls.table).values(**cls._valid(data)).returning(cls.table.c.id)

    @classmethod
    def update(cls, item_id, data: dict[str, Any]) -> Update:
        return (
            update(cls.table)
            .where(cls.table.c.id == item_id)
            .values(**cls._valid(data))
        )

    @classmethod
    def delete(cls, item_id: UUID) -> Delete:
        return delete(cls.table).where(cls.table.c.id == item_id)

    @classmethod
    def get(cls, item_id: UUID) -> Select:
        return select(cls.table).where(cls.table.c.id == item_id)

    @classmethod
    def filter(cls, conditions: list[tuple[str, str, Any]]) -> Select:
        stmt = select(cls.table)
        for field_name, op, value in conditions:
            if field_name not in cls._cols():
                continue
            col = getattr(cls.table.c, field_name)
            handler = FILTER_OPS.get(op)
            if handler:
                stmt = stmt.where(handler(col, value))
        return stmt


class Crud:
    orm: ORM
    m2m: M2MORM

    async def create(self, ctx):
        pass

    async def update(self, ctx):
        pass

    async def patch(self, ctx):
        pass

    async def delete(self, ctx):
        pass

    async def list(self, ctx):
        pass

    async def get(self, ctx):
        pass


PRIMARY_KEY = field(Uuid, primary_key=True, default=uuid4, sort_order=-100)

CREATED_AT = field(
    DateTime(timezone=True),
    default=datetime.now(UTC),
    server_default=func.now(),
    nullable=False,
    sort_order=9991,
)
UPDATED_AT = field(
    DateTime(timezone=True),
    default=datetime.now(UTC),
    server_default=func.now(),
    onupdate=func.now(),
    nullable=False,
    sort_order=9992,
)
DELETED_AT = field(
    DateTime(timezone=True),
    nullable=True,
    sort_order=9993,
)


@model(is_abstract=True)
class BaseModel:
    # d46b8b31-3163-4b5e-8646-a9ffe674775c
    id: Optional[str | UUID] = PRIMARY_KEY

    @classmethod
    def c(cls, name: str) -> Col:
        return getattr(cls.orm.table.c, name)

    class m2m(M2MORM):
        pass

    class orm(ORM):
        pass


@model(is_abstract=True)
class Model(BaseModel):
    created_at: Optional[datetime | str] = CREATED_AT
    updated_at: Optional[datetime | str] = UPDATED_AT


@model(is_abstract=True)
class FullModel(Model):
    deleted_at: Optional[datetime | str] = DELETED_AT
