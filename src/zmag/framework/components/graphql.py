# -*- coding: utf-8 -*-
"""
Components Base
"""

import functools
import typing
from dataclasses import dataclass

import strawberry

from ...external import STRAWBERRY
from ...types import Callable
from .base import components
from .forms import Form, form_dataclass
from .objects import create_typed_class

STRAWBERRY_ID: typing.Any = strawberry.ID
ID: typing.TypeAlias = STRAWBERRY_ID  # type: ignore # pylint: disable=C


def graphql_decorator(cls: typing.Any = None) -> typing.Any:
    """
    This class decorator transforms a Python class into GraphQL operations.

    When applied to a class, `@zmag.gql` interprets inner classes named `Query`
    and `Mutation` as containers for GraphQL query and mutation methods, respectively.
    These methods can then be invoked as part of a GraphQL API.

    Attributes:
        Meta (class): Defines metadata for the GraphQL class,
            such as the associated `app` and `model`.
        Query (class): Contains methods that represent GraphQL queries. Each method
            should be an `async` function and can return various data types.
        Mutation (class): Contains methods that represent GraphQL mutations. Each method
            should be an `async` function and can accept input data for modifying server-side state.

    Note: **Meta** class Attributes:
        - **`app`** (`str | bool | None`): Specifies a prefix for the GraphQL field names.
        If set to `None`, the prefix is omitted, and the field names are based
        directly on the method names.

        - **`model`** (`str | type | None`): When specified, prefixes the GraphQL field names
        with the model name. This helps in creating more descriptive and
        structured GraphQL schemas.

    Tip:
        This decorator allows you to seamlessly integrate Python classes with a GraphQL API.

    Example:

    ```python
    @zmag.gql
    class Graphql:

        class Meta:
            app = True
            model = "Book"

        class Query: ...

        class Mutation: ...
    ```
    """
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

    This function extends `zmag.Input`.

    Args:
        prefix (str | list[str] | None): The **prefix** to be added to each field in the class.
        suffix (str | list[str] | None): The **suffix** to be added to each field in the class.

    Returns:
        decorator: To wrap GraphQL `Input` types.

    Example:

    ```python
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
        type_class = STRAWBERRY.type(_class, description=cls.__doc__ or "")

        # Spoc
        components.register("type", type_class)
        return type_class


class BaseType(metaclass=TypeMeta):
    """
    GraphQL Abstract `Type` for defining common fields and creating a base `class` for other types.

    Example:

    ```python
    # Abstract Class
    class MyBase(zmag.BaseType):
        shared_field: str

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


@dataclass
class Model(BaseType):
    """
    GraphQL `Model` type with a **private `_id`** field and a **public `id`** field included.

    Example:

    ```python
    class Author(zmag.Type):
        @property
        async def merged_ids(self) -> str:
            return f"{self._id} and {self.id}"
    ```
    """

    class Meta:
        """Meta"""

        abstract = True

    _id: strawberry.Private[object] = None  # type: ignore
    id: ID | None = None  # type: ignore


class Input:
    """
    Base class for GraphQL `Input` types, must be used with `zmag.input` function.

    Example:

    ```python
    input = zmag.input()

    @input
    class Form(zmag.Input):
        name: str
        ...
    ```
    """

    input: Form
    """
    Returns the processed value from `zmag.Input`.

    Example:

    ```python    
    async def mutation(form: Form):
        print(form.input)
    ```
    """
