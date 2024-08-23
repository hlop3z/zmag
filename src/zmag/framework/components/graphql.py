# -*- coding: utf-8 -*-
"""
Components Base
"""

import typing

from ...external import StrawberryID, StrawberryPrivate, strawberry
from .base import components
from .objects import create_typed_class


def graphql(cls: typing.Any = None) -> typing.Any:
    """Strawberry `GraphQL` Creator"""
    components.register("graphql", cls)
    return cls


class TypeMeta(type):
    """Type Util"""

    def __new__(mcs, name: str, bases: tuple, attrs: dict) -> "TypeMeta":
        if "_Meta" in attrs:
            attrs["Meta"] = attrs.pop("_Meta")

        # Root class
        class_meta = attrs.get("Meta", None)
        if class_meta and getattr(class_meta, "abstract", False):
            return super().__new__(mcs, name, bases, attrs)

        # Sub class
        cls = super().__new__(mcs, name, bases, attrs)
        _class = create_typed_class(cls, BaseType)

        # Strawberry
        type_class = strawberry.type(_class, description=cls.__doc__ or "")

        # Spoc
        components.register("type", type_class)
        return type_class


class BaseType(metaclass=TypeMeta):
    """
    GraphQL Abstract `Type` to create common fields.

    Example:
    ::

        # Abstract Class
        class MyBase(zmag.BaseType):
            shared_key: str

            class Meta:
                abstract = True

        # New Type
        class MyType(MyBase):
            ...
    """

    class _Meta:
        """Meta"""

        abstract = True

    def __init__(self, **kwargs: typing.Any) -> None:
        self.__dict__.update(kwargs)
        self.for_formatters_to_ignore_order_meta = TypeMeta


class Type(BaseType):
    """
    GraphQL `Type` base.

    Example:
    ::

        class Author(zmag.Type):
            first_name: str
            last_name: str

            @property
            async def full_name(self):
                return f"{self.first_name} {self.last_name}"
    """

    class Meta:
        """Meta"""

        abstract = True


class Model(BaseType):
    """
    GraphQL `Model` type that includes both a **private** `_id` field and a **public** `id` field.

    Example:
    ::

        class Author(zmag.Type):
            first_name: str
            last_name: str

            @property
            async def full_name(self):
                return f"{self.first_name} {self.last_name}"
    """

    class Meta:
        """Meta"""

        abstract = True

    _id: StrawberryPrivate[object]  # type: ignore
    id: StrawberryID  # type: ignore
