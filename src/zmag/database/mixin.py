from datetime import datetime
from uuid import uuid4

from sqlalchemy import func, Table, insert, update, delete, select

from . import models as m
from ..framework.sql_model import model


@model(is_abstract=True)
class BaseModel:
    # d46b8b31-3163-4b5e-8646-a9ffe674775c
    id: m.use[str] = m.col(m.uuid, primary_key=True, default=uuid4, sort_order=-100)

    class orm:
        table: Table

        @classmethod
        def create(cls, session, data):
            return session.execute(insert(cls.table).values(**data))

        @classmethod
        def get(cls, session, id_value):
            return (
                session.execute(select(cls.table).where(cls.table.c.id == id_value))
                .mappings()
                .first()
            )

        @classmethod
        def update(cls, session, id_value, data):
            return session.execute(
                update(cls.table).where(cls.table.c.id == id_value).values(**data)
            )

        @classmethod
        def delete(cls, session, id_value):
            return session.execute(delete(cls.table).where(cls.table.c.id == id_value))

        @classmethod
        def filter(cls, session, conditions: list):
            stmt = select(cls.table)

            for field, op, value in conditions:
                col = getattr(cls.table.c, field)

                if op == "eq":
                    stmt = stmt.where(col == value)
                elif op == "ne":
                    stmt = stmt.where(col != value)
                elif op == "gt":
                    stmt = stmt.where(col > value)
                elif op == "gte":
                    stmt = stmt.where(col >= value)
                elif op == "lt":
                    stmt = stmt.where(col < value)
                elif op == "lte":
                    stmt = stmt.where(col <= value)
                elif op == "in":
                    stmt = stmt.where(col.in_(value))
                elif op == "nin":
                    stmt = stmt.where(col.not_in(value))
                elif op == "like":
                    stmt = stmt.where(col.like(value))
                elif op == "ilike":
                    stmt = stmt.where(col.ilike(value))
                elif op == "contains":
                    stmt = stmt.where(col.contains(value))
                elif op == "icontains":
                    stmt = stmt.where(col.ilike(f"%{value}%"))
                elif op == "startswith":
                    stmt = stmt.where(col.startswith(value))
                elif op == "istartswith":
                    stmt = stmt.where(col.ilike(f"{value}%"))
                elif op == "endswith":
                    stmt = stmt.where(col.endswith(value))
                elif op == "iendswith":
                    stmt = stmt.where(col.ilike(f"%{value}"))
                elif op == "isnull":
                    stmt = stmt.where(col.is_(None) if value else col.is_not(None))

            return session.execute(stmt).mappings().all()


@model(is_abstract=True)
class Model(BaseModel):
    created_at: m.use[datetime] = m.col(
        m.datetime,
        server_default=func.now(),
        nullable=False,
        sort_order=9991,
    )
    updated_at: m.use[datetime] = m.col(
        m.datetime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        sort_order=9992,
    )


@model(is_abstract=True)
class FullModel(Model):
    deleted_at: m.use[datetime] = m.col(
        m.datetime,
        nullable=True,
        sort_order=9993,
    )
