# Permissions

ZMAG provides a wrapper for Strawberry's `Permission` and `Info`.

!!! note "strawberry"

    To create custom permissions or learn more about how they work, visit the official documentation [here](https://strawberry.rocks/docs/guides/permissions).

```python
# -*- coding: utf-8 -*-
"""
Permission
"""

from typing import Any

from zmag import BasePermission, InfoGraphql


class MyPermission(BasePermission):
    """Check If User Is Authorized"""

    message = "User is not authorized"  # Unauthorized

    def has_permission(
        self,
        source: Any,
        info: InfoGraphql,
        **kwargs: Any,
    ) -> bool:
        """Check GraphQL's Info Context"""

        operation = info.field_name  # info.python_name
        user = info.context.get("user")

        print("Checking Perms", operation, user)

        if user:
            return True
        return False
```
