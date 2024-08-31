"""
This module provides a utility to transform synchronous functions into asynchronous functions.

Functions:
    - coro(func) -> function: A decorator that transforms a regular function into an async function,
      allowing it to be run asynchronously using asyncio.
"""

import asyncio
from functools import wraps
from typing import Any

from ..types import Callable, Coroutine


def coro(function: Coroutine) -> Callable:
    """
    Transform an **asynchronous** function into a **synchronous** function.

    Args:
        function (Coroutine): The regular function to be transformed.

    Returns:
        function: An async function that runs the original function using `asyncio.run()`.

    Tip: CLI
        Wrap your commands with `coro` to run async commands with click.

    Example:

    ```python
    @zmag.coro
    async def async_function(x, y):
            return x + y

    result = async_function(3, 4)
    print(result)
    ```
    """

    @wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """
        Wrap the original function to run it asynchronously.
        """
        return asyncio.run(function(*args, **kwargs))

    return wrapper
