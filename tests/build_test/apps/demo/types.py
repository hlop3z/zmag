# -*- coding: utf-8 -*-
"""
    { Types } for GraphQL
"""

from typing import Optional

import zmag


# Create your <types> here.
@zmag.sql.model
class Author:
    name: str


# Create your <types> here.
@zmag.sql.model(ignore=["books"])
class Book:
    title: str
    author: str
    user_id: int

    async def books(self) -> int:
        # print(self._id)
        # print(self.objects)
        return self._id
