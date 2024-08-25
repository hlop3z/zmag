# -*- coding: utf-8 -*-
"""
This module provides utilities for transforming text into various code case formats,
retrieving module names, and enhancing documentation.
"""

from .coro import coro
from .generic import docs, field
from .text import pascal_to_snake, to_camel_case, to_kebab_case, to_pascal_case
from .timer import time_in_seconds

__all__ = (
    "coro",
    "docs",
    "field",
    "time_in_seconds",
    "to_camel_case",
    "to_kebab_case",
    "to_pascal_case",
    "pascal_to_snake",
)
