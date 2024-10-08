# -*- coding: utf-8 -*-
"""
Extensions
"""

from types import SimpleNamespace

from zmag import BaseExtension

import logging


class MyExtension(BaseExtension):
    """GraphQL Extension"""

    async def on_execute(self):
        """On Start Executing"""
        user = self.execution_context.context.get("user")
        user = SimpleNamespace(**(user or {}))

        # Set-User (Context)
        self.execution_context.context["user"] = user

        yield
