from typing import Any

from starlette.datastructures import QueryParams

from .db.pagination import MAX_PAGE_SIZE as MAX_PAGE_SIZE
from .db.pagination import Page as Page
from .db.pagination import Pagination as Pagination
from .db.tables import FILTER_NAMES, TRUTHY


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
                    value = str(value).lower() in TRUTHY
                filters.setdefault(field, {})[op] = value
                continue
        meta[key] = value
    return meta, filters


def parse_query(params: QueryParams) -> tuple[dict[str, Any], list[Any]]:
    meta, filters = _parse_query(params)
    return meta, [(f, o, v) for f, ops in filters.items() for o, v in ops.items()]
