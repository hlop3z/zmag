# -*- coding: utf-8 -*-
"""
GraphQL Types
"""

import zmag


# Create your <types> here.
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
