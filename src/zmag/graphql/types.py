# -*- coding: utf-8 -*-
"""Strawberry - GraphQL Types"""

from dataclasses import dataclass
from typing import Any, Generic, TypeAlias, TypeVar

import strawberry
from strawberry.scalars import JSON

from ..tools import field

T = TypeVar("T")
S = TypeVar("S")


@strawberry.type
@dataclass
class Record(Generic[T]):
    """Represents a `single` object or an `list` of possible multiple objects."""

    item: T | None = None
    items: list[T | None] = field(default_factory=list)
    is_many: bool = False


@strawberry.type
@dataclass
class PageInfo:
    """Pagination context to navigate objects with cursor-based pagination"""

    length: int = 0
    pages: int = 0
    has_next: bool = False
    has_previous: bool = False


@strawberry.type
@dataclass
class Edge(Generic[T]):
    """An edge may contain additional information of the relationship."""

    node: T
    cursor: str


@strawberry.type
@dataclass
class Connection(Generic[T, S]):
    """Represents paginated objects"""

    edges: list[Edge[T]]
    page_info: PageInfo = field(default_factory=PageInfo)
    computed: S | None = None


@strawberry.type
@dataclass
class ErrorMessage:
    """A structured format for GraphQL error messages to be used in `Errors` responses."""

    # ['field', 'type', 'text']

    field: str | None = None
    type: str | None = None
    text: str | None = None


@strawberry.type
@dataclass
class Error:
    """
    A comprehensive response object for handling multiple GraphQL `Errors`.

    Example:

    ```python
    Errors(
        meta={"note": "reset form."}
        messages=[
            Error(field="username", type="invalid", text="username must be lowercase."),
        ],
    )
    ```
    """

    messages: list[ErrorMessage] = field(default_factory=list)
    meta: JSON = field(default_factory=dict)  # type: ignore
    error: bool = True


@strawberry.type
@dataclass
class Mutation(Generic[T]):
    """
    Represents a GraphQL `Mutation` response, handling the outcome of mutation operations.

    Example:

    ```python
    async def create(self) -> zmag.Mutation[types.Book]:
        data = form.input.dict(True)
        return zmag.Mutation(
            item=types.Book(title=data.get("title")),
        )
    ```
    """

    item: T | None = None
    many: list[T] = field(default_factory=list)
    error: Error | None = None
    deleted: int = 0


#################################################
# Generic Connection                            #
#################################################

GenericEdge: TypeAlias = Connection[T, JSON]  # type: ignore

#################################################
# Wrappers                                      #
#################################################


def edge(
    edges: Any | None = None,
    count: int = 0,
    pages: int = 0,
    has_next: bool = False,
    has_previous: bool = False,
    computed: Any | None = None,
) -> Connection[Any, Any]:
    """
    Extends `Edges` used to return a `Page` response.

    Example:

    ```python
    async def search(self) -> zmag.Edge[types.Book]:
        return zmag.edge(
            count=1,
            pages=1,
            edges=[
                types.Book(
                    id=1,
                    title="The Great Gatsby",
                ),
            ],
            computed={
                "someComputedValue": 100,
            },
        )
    ```
    """
    edges = edges or []
    computed = computed or {}
    items = [Edge(node=item, cursor=item.id) for item in edges]  # type: ignore
    return Connection(
        computed=computed,  # type: ignore
        page_info=PageInfo(  # type: ignore
            length=count,
            pages=pages,
            has_next=has_next,
            has_previous=has_previous,
        ),
        edges=items,
    )


def input_error(messages: list[dict], meta: dict | None = None) -> Mutation:
    """
    A simplified error handler for mutation `Errors`.

    Returns:
        response: GraphQL Mutation

    ```python
    async def create(self, form: inputs.Create) -> zmag.Mutation[types.Book]:
        # Not Valid
        if not form.input.is_valid:
            return zmag.input_error(form.input.errors)

        # Is Valid
        ...
    ```
    """
    error_messages = messages or []
    return Mutation(
        error=Error(
            meta=meta or {},  # type: ignore
            messages=[ErrorMessage(**e) for e in error_messages],
        ),
    )
