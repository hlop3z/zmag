# -*- coding: utf-8 -*-
"""
Forms
"""

import zmag

Author = zmag.input("Author")


@Author
class Create(zmag.Input):
    """GraphQL Form"""

    x: zmag.ID = zmag.value(required=True)  # Change Default Value
    y: float = zmag.value(default=lambda: "Some Value")  # Change Default Value

    # Deprecated
    z: int = zmag.value(deprecation_reason="3D coordinates are deprecated")

    # Complex
    email: str = zmag.value(
        regex={r"[\w\.-]+@[\w\.-]+": "invalid email address"},
        # rules=[(lambda v: v.startswith("demo") or "invalid input")],
        clean=zmag.clean(
            regex=[
                (r"^hello", "hola"),
                (r"com", "api"),
            ],  # ("^hello"...) [Won't Work]: We used { regex } to check if it startswith "hello".
            rules=[(lambda v: v.upper())],
        ),
    )
