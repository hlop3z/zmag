# -*- coding: utf-8 -*-
"""
Components Base
"""

import functools
import typing

from ...external import StrawberryID, StrawberryPrivate, strawberry
from ...types import Callable
from .base import components
from .forms import Form, form_dataclass
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
) -> Callable:
    """
    Creates a `decorator` for `Inputs`, optionally adding a common **prefix** or **suffix**.

    Args:
        prefix (str | list[str] | None): The **prefix** to be added to each field in the class.
        suffix (str | list[str] | None): The **suffix** to be added to each field in the class.

    Returns:
        decorator: To wrap GraphQL `Input` types.

    Example:

    ```python
    import zmag

    Author = zmag.input("Author")

    @Author
    class Create(zmag.Input): ... # AuthorCreate

    @Author
    class Update(zmag.Input): ... # AuthorUpdate
    ```
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
    GraphQL Abstract `Type` for defining common fields and creating a base `class` for other types.

    Example:

    ```python

    import zmag

    # Abstract Class
    class MyBase(zmag.BaseType):
        shared_key: str

        class Meta:
            abstract = True

    # New Type - Inheritor
    class MyType(MyBase): ...
    ```
    """

    class _Meta:
        """Meta"""

        abstract = True

    def __init__(self, **kwargs: typing.Any) -> None:
        self.__dict__.update(kwargs)
        self.for_formatters_to_ignore_order_meta = TypeMeta


class Type(BaseType):
    """
    GraphQL `Type` base class.

    Example:

    ```python
    import zmag

    class Author(zmag.Type):
        first_name: str
        last_name: str

        @property
        async def full_name(self) -> str:
            return f"{self.first_name} {self.last_name}"
    ```
    """

    class Meta:
        """Meta"""

        abstract = True


class Model(BaseType):
    """
    GraphQL `Model` type with a **private `_id`** field and a **public `id`** field included.

    Example:

    ```python
    import zmag

    class Author(zmag.Type):
        @property
        async def merged_ids(self) -> str:
            return f"{self._id} and {self.id}"
    ```
    """

    class Meta:
        """Meta"""

        abstract = True

    _id: StrawberryPrivate[object]  # type: ignore
    id: StrawberryID  # type: ignore


class Input:
    """
    Base class for GraphQL `Input` types, must be used with `zmag.input` function.

    Example:

    ```python
    import zmag

    form = zmag.input()

    @form
    class Form(zmag.Input):
        name: str
        ...
    ```
    """

    input: Form
