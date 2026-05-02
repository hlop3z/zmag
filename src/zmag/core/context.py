from dataclasses import dataclass
from uuid import UUID
from typing import Any

from fastapi import Request, Response

from ..db.session import DatabaseSession
from ..utils import Pagination, MAX_PAGE_SIZE


@dataclass
class Context:
    id: UUID | None
    db: DatabaseSession
    request: Request
    response: Response
    input: dict[str, Any]
    filters: list[Any]
    pagination: Pagination
    user: dict[str, Any] | None = None

    @staticmethod
    def init(
        db: DatabaseSession,
        id: UUID | None,
        input: dict[str, Any],
        pagination: dict[str, Any],
        request: Request,
        response: Response,
        filters: list[Any],
    ):
        return Context(
            db=db,
            id=id,
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
