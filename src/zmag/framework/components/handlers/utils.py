# -*- coding: utf-8 -*-
"""
Utils for Handlers
"""

# from ...external import spoc
from ...components import components


def error_message(group, one, two):
    """Error Message"""

    msg = f"""\n* <{group}: { one.name }> is already in use by the <App: { one.app }>"""
    msg += f"""\n* <{group}> must have UNIQUE names."""
    msg += f"""\n* Rename it in either <App: { one.app }> or <App: { two.app }>."""
    return msg


def generic_collector(component_name: str, models: list):
    """Collect Components"""
    single_name: dict = {}
    for current in models:
        is_component = components.is_component(component_name, current)
        if is_component:
            name = current.object.__name__
            # Generic
            # if generics and name == "generic":
            #    name = current.key.replace(".", "__")
            # UNIQUE names
            found = single_name.get(name)
            if found and found.object != current.object:  #  and not generics
                message = error_message(component_name, found, current)
                raise ValueError(message)
            single_name[name] = current
    return single_name
