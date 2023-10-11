# -*- coding: utf-8 -*-
"""
    { CRUD } GraphQL(s)
"""

import zmag

# GraphQL Tools
from . import forms, manager

# Create your <CRUDs> here.

Books = zmag.crud(
    manager=manager.Book,
    # form=forms.Book,
    clear_ignore=["author"],
    docs={},
)
