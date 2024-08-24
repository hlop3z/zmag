# -*- coding: utf-8 -*-
"""
Components Base
"""

import functools
import typing

from ...external import StrawberryID, StrawberryPrivate, strawberry
from .base import components
from .forms import form_dataclass
from .objects import create_typed_class


def graphql(cls: typing.Any = None) -> typing.Any:
    """Strawberry `GraphQL` Creator"""
    components.register("graphql", cls)
    return cls


def input_middleware(cls):
    """Strawberry `GraphQL` Creator"""
    components.register("input", cls)
    return cls


def graphql_input(
    prefix: str | list[str] | None = None,
    suffix: str | list[str] | None = None,
):
    """
    Creates a partial function for a GraphQL `Input-Type` with a common prefix or suffix.

    Args:
        prefix (str | list[str] | None): The `prefix` to be added to each field in the dataclass.
        suffix (str | list[str] | None): The `suffix` to be added to each field in the dataclass.

    Returns:
        functools.partial: A partial function that creates a dataclass with the specified
        prefix, suffix, for GraphQL representation.

    Example:
    ::

        import zmag

        Author = zmag.input("Author")

        @Author
        class Create(zmag.Input): # AuthorCreate
            ...

        @Author
        class Update(zmag.Input): # AuthorUpdate
            ...
    """
    return functools.partial(
        form_dataclass,
        prefix=prefix,
        suffix=suffix,
        graphql=True,
        middleware=input_middleware,
    )


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

        import zmag

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

        import zmag

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

        import zmag

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
