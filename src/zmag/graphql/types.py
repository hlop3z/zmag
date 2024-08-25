# -*- coding: utf-8 -*-
"""Strawberry - GraphQL Types"""

from dataclasses import dataclass
from typing import Generic, TypeVar

from ..external import JSON, strawberry
from ..tools import field

T = TypeVar("T")


@strawberry.type
@dataclass
class PageInfo:
    """Pagination context to navigate objects with cursor-based pagination"""

    length: int = 0
    pages: int = 0
    extra: JSON = field(default_factory=dict)  # type: ignore


@strawberry.type
@dataclass
class Edge(Generic[T]):
    """An edge may contain additional information of the relationship. This is the trivial case"""

    node: T
    cursor: str


@strawberry.type
@dataclass
class Connection(Generic[T]):
    """Represents a paginated relationship between two entities"""

    edges: list["Edge[T]"]
    page_info: "PageInfo" = field(default_factory=PageInfo)


@strawberry.type
@dataclass
class ErrorMessage:
    """GraphQL Error Message"""

    # ['field', 'type', 'text']

    field: str | None = None
    type: str | None = None
    text: str | None = None


@strawberry.type
@dataclass
class Error:
    """GraphQL Error"""

    messages: list[ErrorMessage] = field(default_factory=list)
    meta: JSON = field(default_factory=dict)  # type: ignore
    error: bool = True


@strawberry.type
@dataclass
class Mutation(Generic[T]):
    """GraphQL Mutation"""

    item: T | None = None
    many: list[T] = field(default_factory=list)
    error: Error | None = None
    deleted: int = 0


def edge(
    edges: list[Edge] | None = None,
    count: int = 0,
    pages: int = 0,
    extra: dict | None = None,
) -> Connection:
    """Edges Page Response"""
    edges = edges or []
    extra = extra or {}
    items = [Edge(node=item, cursor=item.id) for item in edges]  # type: ignore
    return Connection(
        page_info=PageInfo(  # type: ignore
            length=count,
            pages=pages,
            extra=extra,
        ),
        edges=items,
    )
