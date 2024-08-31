# -*- coding: utf-8 -*-
"""
Externals
"""

from typing import Any

# Dictionary to hold the imported modules
modules: Any = {
    "spoc": None,
    "uvloop": None,
    "click": None,
    "strawberry": None,
}

# Attempt to import each module and update the dictionary
for module_name in modules:
    try:
        modules[module_name] = __import__(module_name)
    except ImportError:
        modules[module_name] = None

# Extract the modules from the dictionary for easier access
SPOC = modules["spoc"]
UVLOOP = modules["uvloop"]
CLICK = modules["click"]
STRAWBERRY = modules["strawberry"]

__all__ = (
    "SPOC",
    "UVLOOP",
    "CLICK",
    "STRAWBERRY",
)
