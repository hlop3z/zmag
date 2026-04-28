from datetime import datetime, timezone

from jinja2 import Template
from starlette.datastructures import QueryParams


def utc_now():
    return datetime.now(timezone.utc)


_OPERATORS = {
    "eq",
    "ne",
    "gt",
    "gte",
    "lt",
    "lte",
    "in",
    "nin",
    "like",
    "ilike",
    "contains",
    "icontains",
    "startswith",
    "istartswith",
    "endswith",
    "iendswith",
    "isnull",
}

_TRUTHY = {"1", "true", "yes", "on"}


def parse_query(params: QueryParams) -> tuple[dict, dict]:
    raw = {
        k: v if len(v) > 1 else v[0]
        for k, v in {k: params.getlist(k) for k in dict.fromkeys(params)}.items()
    }
    meta, filters = {}, {}
    for key, value in raw.items():
        if "__" in key:
            field, _, op = key.partition("__")
            if op in _OPERATORS:
                if op == "isnull":
                    value = str(value).lower() in _TRUTHY
                filters.setdefault(field, {})[op] = value
                continue
        meta[key] = value
    return meta, filters


def load_template(path: str) -> Template:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return Template(content)
