# -*- coding: utf-8 -*-
"""
Externals
"""

import typing

try:
    import spoc
except ImportError as e:
    raise e

try:
    import uvloop  # type: ignore
except ImportError:
    uvloop = None

try:
    import click
except ImportError:
    click = None  # type: ignore


try:
    import strawberry
except ImportError:
    strawberry = None  # type: ignore


if strawberry:
    from strawberry.scalars import JSON

    StrawberryID = strawberry.ID
    StrawberryPrivate = strawberry.Private
else:
    JSON = typing.Any  # type: ignore
    StrawberryID = typing.Any  # type: ignore
    StrawberryPrivate = typing.Any  # type: ignore

__all__ = (
    "spoc",
    "uvloop",
    "click",
    "strawberry",
    "JSON",
    "StrawberryID",
    "StrawberryPrivate",
)
