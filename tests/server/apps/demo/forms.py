from typing import Any

import zmag

form = zmag.input("Form")


@form
class Point2D:
    input: Any
    x: zmag.ID = zmag.value(
        default=None,
        required=True,
    )
    y: float = zmag.value(
        default=None,
        required=False,
    )
    z: int = zmag.value(
        default=None,
        required=False,
        deprecation_reason="3D coordinates are deprecated",
    )
    email: str = zmag.value(
        default=None,
        regex={r"[\w\.-]+@[\w\.-]+": "invalid email address"},
        rules=[(lambda v: v.startswith("demo") or "invalid input")],
        clean=zmag.clean(
            regex=[
                ("^hello", "hola"),
                ("com", "api"),
            ],  # ("^hello"...) [Won't Work]: We used { regex } to check if it startswith "hello".
            rules=[(lambda v: v.upper())],
        ),
    )
