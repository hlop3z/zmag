# -*- coding: utf-8 -*-
"""
    { Controller } for the Database(s)
"""

import zmag

# GraphQL Tools
from . import types


# Create your <managers> here.
@zmag.manager
class Book(zmag.BaseManager):
    """Book Manager"""

    model = types.Book
