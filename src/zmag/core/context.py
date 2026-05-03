from dataclasses import dataclass, field
from uuid import UUID
from typing import Any
from types import SimpleNamespace

from fastapi import Request, Response

from ..db.session import DatabaseSession
from ..utils import Pagination, MAX_PAGE_SIZE
from .response import Error


@dataclass
class Context:
    id: UUID | None
    db: DatabaseSession
    request: Request
    response: Response
    input: dict[str, Any]
    filters: list[Any]
    pagination: Pagination
    user: SimpleNamespace | None = None
    errors: list[Error | None] = field(default_factory=list)

    def error(self, code: str, message: str, field: str | None = None):
        self.errors.append(Error(code=code, message=message, field=field))

    @staticmethod
    def init(
        db: DatabaseSession,
        id: UUID | None,
        input: dict[str, Any],
        pagination: dict[str, Any],
        request: Request,
        response: Response,
        filters: list[Any],
        user: dict[str, Any] | None = None,
    ):
        return Context(
            db=db,
            id=id,
            user=SimpleNamespace(**user) if user else None,
            input=input,
            pagination=Pagination(
                page=pagination.get("page", 1),
                limit=pagination.get("limit", MAX_PAGE_SIZE),
                sort_by=pagination.get("sort_by", []),
            ),
            filters=filters,
            request=request,
            response=response,
        )
