# Extensions

ZMAG provides a wrapper for Strawberry's `Extension`.

!!! note "strawberry"

    To create custom extensions or learn more about how they work, visit the official documentation [here](https://strawberry.rocks/docs/guides/custom-extensions).

```python
# -*- coding: utf-8 -*-
"""
Extensions
"""

from types import SimpleNamespace

from zmag import BaseExtension


class MyExtension(BaseExtension):
    """GraphQL Extension"""

    async def on_execute(self):
        """On Execute"""
        user = self.execution_context.context.get("user")
        user = SimpleNamespace(**(user or {}))

        # Set-User (Context)
        self.execution_context.context["user"] = user

        yield
```
