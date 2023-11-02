import json
import pathlib
from types import SimpleNamespace
from functools import wraps


def import_tool(namespace_keys):
    """
    Load Python Module
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                result["INIT"] = True
            except ImportError:
                result = {key: None for key in namespace_keys}
                result["INIT"] = False
            return SimpleNamespace(**result)

        return wrapper

    return decorator


def load_json(path):
    """
    Load JSON from a file and return the parsed data.
    """
    file_path = pathlib.Path(path)
    with open(file_path) as file:
        try:
            return json.loads(file.read())
        except:
            return {}
