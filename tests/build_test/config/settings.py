# -*- coding: utf-8 -*-
"""
    { Settings }
"""
import pathlib

# Base Directory
BASE_DIR = pathlib.Path(__file__).parents[1]

# Installed Apps
INSTALLED_APPS = ["demo"]

# Database(s)
DATABASES = {
    "sql": {"default": "sqlite:///example.db"},  # Example:
    "mongo": {"default": None},  # Example: mongodb://localhost:27017/example
}
