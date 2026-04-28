from functools import wraps
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def my_decorator(cls: Callable[P, R]) -> Callable[P, R]:
    @wraps(cls)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print("before")
        return cls(*args, **kwargs)

    return wrapper
