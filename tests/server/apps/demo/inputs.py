# -*- coding: utf-8 -*-
"""
Forms
"""

import zmag

Book = zmag.input("Book")


def validator(value):
    return value.startswith("x") or "value must start with `x`."


@Book
class Create(zmag.Input):
    """GraphQL Form"""

    title: str = zmag.value(rules=[validator])
