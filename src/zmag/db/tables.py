from datetime import datetime, UTC
from math import ceil
from uuid import uuid4, UUID
from typing import Any, Optional, Callable

from sqlalchemy import (
    func,
    Table,
    Column,
    Boolean,
    DateTime,
    Float,
    Integer,
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
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.decorators.models import field
from ..core.decorators.models import model
from .pagination import Page, Pagination
from .utils import apply_sort

Col = ReadOnlyColumnCollection[str, Column[Any]]
Filters = list[tuple[str, str, Any]]

TRUTHY = {"1", "true", "yes", "on"}

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

    @classmethod
    def col(cls, name: str) -> Col:
        return getattr(cls.table.c, name)

    # ------------------------------------------------------------------
    # Statement builders
    # ------------------------------------------------------------------

    @classmethod
    def all_stmt(cls) -> Select:
        return select(cls.related_table).join(
            cls.table,
            getattr(cls.table.c, cls.related_col) == cls.related_table.c.id,
        )

    @classmethod
    def of_stmt(cls, own_id: str) -> Select:
        return cls.all_stmt().where(getattr(cls.table.c, cls.own_col) == own_id)

    @classmethod
    def add_stmt(cls, own_id: str, related_id: str) -> Insert:
        return insert(cls.table).values(
            **{cls.own_col: own_id, cls.related_col: related_id}
        )

    @classmethod
    def remove_stmt(cls, own_id: str, related_id: str) -> Delete:
        return (
            delete(cls.table)
            .where(getattr(cls.table.c, cls.own_col) == own_id)
            .where(getattr(cls.table.c, cls.related_col) == related_id)
        )

    # ------------------------------------------------------------------
    # Async execution methods  (primary API)
    # ------------------------------------------------------------------

    @classmethod
    async def all(cls, db: AsyncSession) -> Any:
        result = await db.execute(cls.all_stmt())
        return result.mappings().all()

    @classmethod
    async def of(
        cls, db: AsyncSession, own_id: str, pagination: Pagination | None = None
    ) -> Any:
        base = cls.of_stmt(own_id)
        if pagination is None:
            result = await db.execute(base)
            return result.mappings().all()

        total: int = (
            await db.execute(select(func.count()).select_from(base.subquery()))
        ).scalar() or 0

        stmt = base.offset(pagination.offset).limit(pagination.limit)
        rows = (await db.execute(stmt)).mappings().all()

        pages = max(1, ceil(total / pagination.limit))
        return Page(
            items=list(rows),
            total=total,
            page=pagination.page,
            limit=pagination.limit,
            pages=pages,
            has_next=pagination.page < pages,
            has_prev=pagination.page > 1,
            next_page=pagination.page + 1 if pagination.page < pages else None,
            prev_page=pagination.page - 1 if pagination.page > 1 else None,
        )

    @classmethod
    async def add(cls, db: AsyncSession, own_id: str, related_id: str) -> None:
        await db.execute(cls.add_stmt(own_id, related_id))

    @classmethod
    async def remove(cls, db: AsyncSession, own_id: str, related_id: str) -> None:
        await db.execute(cls.remove_stmt(own_id, related_id))


class ORM:
    table: Table
    sortable: list[str] | None = None

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
    def _coerce(cls, col_name: str, value: Any) -> Any:
        if not isinstance(value, str):
            return value
        col_type = getattr(cls.table.c, col_name).type
        if isinstance(col_type, DateTime):
            return datetime.fromisoformat(value)
        if isinstance(col_type, Uuid):
            return UUID(value)
        if isinstance(col_type, Integer):
            return int(value)
        if isinstance(col_type, Float):
            return float(value)
        if isinstance(col_type, Boolean):
            return value.lower() in TRUTHY
        return value

    @classmethod
    def _valid(cls, data: dict[str, Any]) -> dict[str, Any]:
        return {
            k: cls._coerce(k, v)
            for k, v in data.items()
            if k in cls._cols() and not cls.table.c[k].primary_key
        }

    # ------------------------------------------------------------------
    # Statement builders  (use these when you need to compose further)
    # ------------------------------------------------------------------

    @classmethod
    def create_stmt(cls, data: dict[str, Any]) -> Insert:
        return insert(cls.table).values(**cls._valid(data)).returning(cls.table.c.id)

    @classmethod
    def _apply_conditions(cls, stmt, conditions: Filters):
        for field_name, op, value in conditions:
            if field_name not in cls._cols():
                continue
            col = getattr(cls.table.c, field_name)
            handler = FILTER_OPS.get(op)
            if handler:
                coerced = (
                    [cls._coerce(field_name, v) for v in value]
                    if isinstance(value, list)
                    else cls._coerce(field_name, value)
                )
                stmt = stmt.where(handler(col, coerced))
        return stmt

    @classmethod
    def update_stmt(
        cls, item_id, data: dict[str, Any], conditions: Filters | None = None
    ) -> Update:
        stmt = (
            update(cls.table)
            .where(cls.table.c.id == item_id)
            .values(**cls._valid(data))
        )
        return cls._apply_conditions(stmt, conditions) if conditions else stmt

    @classmethod
    def delete_stmt(cls, item_id: UUID, conditions: Filters | None = None) -> Delete:
        stmt = delete(cls.table).where(cls.table.c.id == item_id)
        return cls._apply_conditions(stmt, conditions) if conditions else stmt

    @classmethod
    def get_stmt(cls, item_id: UUID, conditions: Filters | None = None) -> Select:
        stmt = select(cls.table).where(cls.table.c.id == item_id)
        return cls._apply_conditions(stmt, conditions) if conditions else stmt

    @classmethod
    def filter_stmt(cls, conditions: Filters, query: Select | None = None) -> Select:
        return cls._apply_conditions(query or select(cls.table), conditions)

    @classmethod
    def sort(cls, query: Select, sort_by: list[str]) -> Select:
        return apply_sort(cls.table, query, sort_by, cls.sortable)

    # ------------------------------------------------------------------
    # Async execution methods  (primary API)
    # ------------------------------------------------------------------

    @classmethod
    async def create(cls, db: AsyncSession, data: dict[str, Any]) -> Any:
        result = await db.execute(cls.create_stmt(data))
        return result.mappings().first()

    @classmethod
    async def update(
        cls,
        db: AsyncSession,
        item_id: UUID | None,
        data: dict[str, Any],
        conditions: Filters | None = None,
    ) -> None:
        if not item_id:
            return None
        await db.execute(cls.update_stmt(item_id, data, conditions))

    @classmethod
    async def delete(
        cls, db: AsyncSession, item_id: UUID | None, conditions: Filters | None = None
    ) -> None:
        if not item_id:
            return None
        await db.execute(cls.delete_stmt(item_id, conditions))

    @classmethod
    async def get(
        cls, db: AsyncSession, item_id: UUID | None, conditions: Filters | None = None
    ) -> Any:
        if not item_id:
            return None
        result = await db.execute(cls.get_stmt(item_id, conditions))
        return result.mappings().first()

    @classmethod
    async def filter(
        cls,
        db: AsyncSession,
        conditions: Filters,
        query: Select | None = None,
    ) -> Any:
        result = await db.execute(cls.filter_stmt(conditions, query))
        return result.mappings().all()

    @classmethod
    async def list(
        cls,
        db: AsyncSession,
        pagination: Pagination,
        conditions: Filters | None = None,
        query: Select | None = None,
    ) -> Page:
        base = query or select(cls.table)
        if conditions:
            base = cls._apply_conditions(base, conditions)

        total: int = (
            await db.execute(select(func.count()).select_from(base.subquery()))
        ).scalar() or 0

        stmt = base.offset(pagination.offset).limit(pagination.limit)
        if pagination.sort_by:
            stmt = cls.sort(stmt, pagination.sort_by)

        rows = (await db.execute(stmt)).mappings().all()

        pages = max(1, ceil(total / pagination.limit))
        return Page(
            items=list(rows),
            total=total,
            page=pagination.page,
            limit=pagination.limit,
            pages=pages,
            has_next=pagination.page < pages,
            has_prev=pagination.page > 1,
            next_page=pagination.page + 1 if pagination.page < pages else None,
            prev_page=pagination.page - 1 if pagination.page > 1 else None,
        )


class CRUD:
    orm: ORM
    m2m: M2MORM

    async def create(self, ctx):
        return await self.orm.create(ctx.db, ctx.input)

    async def update(self, ctx):
        await self.orm.update(ctx.db, ctx.id, ctx.input)
        return await self.orm.get(ctx.db, ctx.id)

    async def patch(self, ctx):
        await self.orm.update(ctx.db, ctx.id, ctx.input)
        return await self.orm.get(ctx.db, ctx.id)

    async def delete(self, ctx):
        await self.orm.delete(ctx.db, ctx.id)

    async def list(self, ctx):
        return await self.orm.list(ctx.db, ctx.pagination, ctx.filters)

    async def get(self, ctx):
        return await self.orm.get(ctx.db, ctx.id)


PRIMARY_KEY = field(Uuid, primary_key=True, default=uuid4, sort_order=-100)
ID = field(Uuid, primary_key=True, default=uuid4, sort_order=-10)

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
