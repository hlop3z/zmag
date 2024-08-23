# -*- coding: utf-8 -*-
"""
{ Types }
"""

import zmag

# from zmag import settings


# Create your <types> here.
class Author(*zmag.model):
    """(Type) Read The Docs"""

    name: str


class Book(*zmag.model):
    """(Type) Read The Docs"""

    title: str = zmag.field(default="Hello World")
    author: Author
