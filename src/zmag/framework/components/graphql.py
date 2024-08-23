# -*- coding: utf-8 -*-
"""
Components Base
"""

import typing

from ...external import StrawberryID, StrawberryPrivate, strawberry
from ..objects import create_class
from .base import components


def graphql(cls: typing.Any = None) -> typing.Any:
    """Strawberry `GraphQL` Creator"""
    components.register("graphql", cls)
    return cls


class TypeMeta(type):
    """Type Util"""

    def __new__(mcs, name: str, bases: tuple, attrs: dict) -> "TypeMeta":
        # Root class
        if name == "Type":
            return super().__new__(mcs, name, bases, attrs)

        # Sub class
        cls = super().__new__(mcs, name, bases, attrs)
        _class = create_class(cls, Type)

        # Strawberry
        type_class = strawberry.type(_class, description=cls.__doc__ or "")

        # Spoc
        components.register("type", type_class)
        return type_class


class Type(metaclass=TypeMeta):
    """GraphQL Base Type"""

    def __init__(self, **kwargs: typing.Any) -> None:
        self.__dict__.update(kwargs)
        self.for_formatters_to_ignore_order_meta = TypeMeta


class Model:
    """GraphQL Base Model"""

    _id: StrawberryPrivate[object]  # type: ignore
    id: StrawberryID  # type: ignore
