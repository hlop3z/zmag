"""
Generic Tools
"""

from dataclasses import field as dc_field


def field(**kwargs):
    """
    Dataclasses Field Wrapper.
    """
    return dc_field(**kwargs)


def docs(description):
    """
    Inject Documentation.
    """

    def decorator(function):
        """Decorator"""
        function.__doc__ = description
        return function

    return decorator
