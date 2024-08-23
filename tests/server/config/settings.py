# -*- coding: utf-8 -*-
"""
{ Settings }
"""

import pathlib

# Base Directory
BASE_DIR = pathlib.Path(__file__).parents[1]


# Installed Apps
INSTALLED_APPS = ["demo", "other"]

# EXTRAS
EXTRAS = {
    "extensions": [],
    "permissions": [],
    "on_startup": [],
    "on_shutdown": [],
}