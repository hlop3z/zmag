# -*- coding: utf-8 -*-
"""
{ Types }
"""

import zmag


# Create your <types> here.
class Author(zmag.Type):  # zmag.BaseType
    first_name: str
    last_name: str

    @property
    async def name(self):
        return f"{self.first_name} {self.last_name}"


class Book(zmag.Model):
    """(Type) Read The Docs"""

    title: str = zmag.field(default="Hello World")
    author: Author
