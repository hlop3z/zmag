"""
This module provides utilities to transform text into various case formats
commonly used in programming, such as kebab-case, camelCase, PascalCase, and snake_case.
Additionally, it includes a function to extract a module's name.

Functions:
    - to_kebab_case(text: str) -> str: Converts a given string to `kebab-case`.
    - to_camel_case(text: str) -> str: Converts a given string to `camelCase`.
    - to_pascal_case(text: str) -> str: Converts a given string to `PascalCase`.
    - pascal_to_snake(name: str) -> str: Converts a string from `PascalCase` to `snake_case`.
"""

import re


def to_kebab_case(text: str) -> str:
    """
    Convert a string to `kebab-case`.
    """
    text = re.sub("[^0-9a-zA-Z]+", "-", str(text))
    return text.lower()


def to_camel_case(text: str) -> str:
    """
    Convert a string to `camelCase`.
    """
    text = to_kebab_case(text)
    init, *temp = text.title().split("-")
    return "".join([init.lower()] + temp)


def to_pascal_case(text: str) -> str:
    """
    Convert a string to `PascalCase`.
    """
    text = to_kebab_case(text)
    return text.title().replace("-", "")


def pascal_to_snake(name: str) -> str:
    """
    Convert a string from `PascalCase` to `snake_case`.
    """
    # Insert underscores before capital letters
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    # Handle cases like 'IOStream' -> 'io_stream'
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
    # Convert the entire string to lowercase
    return s2.lower()
