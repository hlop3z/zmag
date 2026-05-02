from dataclasses import dataclass, field
from typing import Any

from starlette.datastructures import QueryParams

from .db.tables import FILTER_NAMES

_TRUTHY = {"1", "true", "yes", "on"}

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


def _parse_query(params: QueryParams) -> tuple[dict, dict]:
    raw = {
        k: v if len(v) > 1 else v[0]
        for k, v in {k: params.getlist(k) for k in dict.fromkeys(params)}.items()
    }
    meta, filters = {}, {}
    for key, value in raw.items():
        if "__" in key:
            field, _, op = key.partition("__")
            if op in FILTER_NAMES:
                if op == "isnull":
                    value = str(value).lower() in _TRUTHY
                filters.setdefault(field, {})[op] = value
                continue
        meta[key] = value
    return meta, filters


def parse_query(params: QueryParams) -> tuple[dict[str, Any], list[Any]]:
    meta, filters = _parse_query(params)
    return meta, [(f, o, v) for f, ops in filters.items() for o, v in ops.items()]
