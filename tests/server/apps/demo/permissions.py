# -*- coding: utf-8 -*-
"""
Permission
"""

import typing

from strawberry.types import Info

from zmag import BasePermission


class MyPermission(BasePermission):
    """Check If User Is Authorized"""

    message = "User is not authorized"  # Unauthorized

    async def has_permission(
        self, source: typing.Any, info: Info, **kwargs: typing.Any
    ) -> bool:
        """Check GraphQL's Info Context"""

        operation = info.field_name  # info.python_name
        user = info.context.get("user")

        print("Checking PERMS", operation, user)
        if user:
            return True
        return False
