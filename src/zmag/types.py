# -*- coding: utf-8 -*-
"""
Generic Types
"""

from typing import Any
from typing import Callable as PythonCallable
from typing import Coroutine as PythonCoroutine

# Type alias for any generic callable object
Callable = PythonCallable[..., Any]

# Type alias for any generic asynchronous function
Coroutine = PythonCallable[..., PythonCoroutine[Any, Any, Any]]
