"""spoc Components registry"""

from ._components import components


def include_router(obj):
    components.register("api", obj)
