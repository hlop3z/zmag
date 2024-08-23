# -*- coding: utf-8 -*-
"""
This module provides utilities for transforming text into various code case formats,
retrieving module names, and enhancing documentation.
"""

from dataclasses import field as dc_field

from .coro import coro
from .text import pascal_to_snake, to_camel_case, to_kebab_case, to_pascal_case
from .timer import time_in_seconds


def field(**kwargs):
    """
    Dataclasses Field Wrapper.
    """
    return dc_field(**kwargs)


def docs(description):
    """
    Inject Documentation.
    """

    def decorator(function):
        """Decorator"""
        function.__doc__ = description
        return function

    return decorator


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
