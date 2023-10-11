"""
    Strawberry - GraphQL (Connection, PageInfo, Edges)
"""

from dataclasses import field
from typing import Generic, TypeVar

import strawberry
from strawberry.scalars import JSON

GenericType = TypeVar("GenericType")


@strawberry.type
class Connection(Generic[GenericType]):
    """Represents a paginated relationship between two entities"""

    page_info: "PageInfo"
    edges: list["Edge[GenericType]"]


@strawberry.type
class PageInfo:
    """Pagination context to navigate objects with cursor-based pagination"""

    length: int
    pages: int
    extra: JSON = field(default_factory=dict)


@strawberry.type
class Edge(Generic[GenericType]):
    """An edge may contain additional information of the relationship. This is the trivial case"""

    node: GenericType
    cursor: str


@strawberry.type
class ErrorMessage:
    """GraphQL Error Message"""

    # ['field', 'type', 'text']

    field: str | None = None
    type: str | None = None
    text: str | None = None


@strawberry.type
class Error:
    """GraphQL Error"""

    messages: list[ErrorMessage] = field(default_factory=list)
    meta: JSON = field(default_factory=dict)
    error: bool = False


@strawberry.type
class Mutation(Generic[GenericType]):
    """Model Mutation Response"""

    item: GenericType | None = None
    items: list[GenericType] = field(default_factory=list)
    updated: int = 0
    deleted: int = 0
    error: Error = field(default_factory=Error)
