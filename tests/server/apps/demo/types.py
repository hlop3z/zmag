# -*- coding: utf-8 -*-
"""
GraphQL Types
"""

import dataclasses as dc
from typing import Annotated, TypeAlias, TypeVar

import zmag

T = TypeVar("T")
Ref: TypeAlias = Annotated[T, zmag.lazy_type(".types")]


# Create your <types> here.
@dc.dataclass
class Book(zmag.Model):
    title: str | None = None
    author: Ref["Author"] | None = None


@dc.dataclass
class Author(zmag.Type):
    first_name: str | None = None
    last_name: str | None = None
    books: list[Book] | None = None

    @property
    async def full_name(self) -> str:
        """Full Name"""
        return f"{self.first_name or ''} {self.last_name or ''}"


'''
class Author(zmag.Type):  # zmag.BaseType
    """(Type) Read The Docs"""

    first_name: str
    last_name: str

    @property
    async def name(self):
        """Full Name"""
        return f"{self.first_name} {self.last_name}"


class Book(zmag.Model):
    """(Type) Read The Docs"""

    title: str
    author: Author
'''
