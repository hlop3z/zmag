from sqlalchemy import func
from datetime import datetime
from uuid import uuid4

from . import models as m
from ..framework.sql_model import model


@model(is_abstract=True)
class BaseModel:
    # d46b8b31-3163-4b5e-8646-a9ffe674775c
    id: m.use[str] = m.col(m.uuid, primary_key=True, default=uuid4, sort_order=-100)


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
