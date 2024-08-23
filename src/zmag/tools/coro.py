"""
This module provides a utility to transform synchronous functions into asynchronous functions.

Functions:
    - coro(func) -> function: A decorator that transforms a regular function into an async function,
      allowing it to be run asynchronously using asyncio.
"""

import asyncio
from functools import wraps


def coro(func):
    """
    Transform a regular synchronous function into an asynchronous function.

    This decorator enables a regular function to be executed asynchronously
    by running it within an asyncio event loop.

    Args:
        func (function): The regular function to be transformed.

    Returns:
        function: An async function that runs the original function using asyncio.run().

    Example:
        >>> @coro
        ... def sync_function(x, y):
        ...     return x + y
        ...
        >>> result = sync_function(3, 4)
        >>> print(result)
        7

    Note:
        This decorator is suitable for use when you want to run a synchronous function
        within an async environment without manually handling asyncio event loops.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Wrap the original function to run it asynchronously.

        Args:
            *args: Positional arguments to pass to the original function.
            **kwargs: Keyword arguments to pass to the original function.

        Returns:
            The result of the original function executed within an asyncio event loop.
        """
        return asyncio.run(func(*args, **kwargs))

    return wrapper
