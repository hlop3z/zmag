# -*- coding: utf-8 -*-
"""
    { Manager }
"""

import zmag


# Manager your <types> here.
Author = zmag.type("author")
# Book = zmag.type("app-book")
# print("Author", Author == zmag.type("author"))
# print("Author", zmag.type("author") == zmag.type("author"))


# Computed
@Author.field("full_name")
async def resolve_full_name(obj, info):
    return obj.get("first_name", "") + " " + obj.get("last_name", "")


@Author.filter("computed")
async def dataset_computed_value(response, info):
    return {"computed_value": len(response.data)}


# Methods
@Author.after("filter")
async def after_method(response, info):
    print("after_filter")


# Forms


@Author.form("create")  # create, update
class Create:
    first_name = zmag.value(
        str,
        default=None,
        required=False,
        # rules=[(lambda v: v.lower().startswith("j") or "invalid input")],
        filters=zmag.filters(
            rules=[(lambda v: v.lower())],
        ),
    )
    last_name = zmag.value(
        str,
        required=True,
        filters=zmag.filters(
            rules=[(lambda v: v.lower())],
        ),
    )


@Author.form("update")  # create, update
class Update:
    first_name = zmag.value(
        str,
        required=False,
        filters=zmag.filters(
            rules=[(lambda v: v.lower())],
        ),
    )
    last_name = zmag.value(
        str,
        required=False,
        filters=zmag.filters(
            rules=[(lambda v: v.lower())],
        ),
    )
