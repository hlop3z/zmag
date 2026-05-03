from dataclasses import dataclass, field
from typing import Any

MAX_PAGE_SIZE = 20


@dataclass
class Pagination:
    page: int = 1
    limit: int = 10
    sort_by: list[str] = field(default_factory=list)

    def __post_init__(self):
        self.page = max(1, int(self.page))
        self.limit = max(1, min(int(self.limit), MAX_PAGE_SIZE))

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


@dataclass
class Page:
    items: list[Any]
    total: int
    page: int
    limit: int
    pages: int
    has_next: bool
    has_prev: bool
    next_page: int | None = None
    prev_page: int | None = None
