# -*- coding: utf-8 -*-
"""
Extensions
"""

from types import SimpleNamespace

from zmag import BaseExtension


class MyExtension(BaseExtension):
    """GraphQL Extension"""

    async def on_executing_start(self):
        """On Start Executing"""
        user = self.execution_context.context.get("user")
        user = SimpleNamespace(**(user or {}))

        # Set-User (Context)
        self.execution_context.context["user"] = user
