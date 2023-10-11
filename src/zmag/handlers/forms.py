"""
    Types
"""

try:
    import dbcontroller as dbc
except ImportError:
    dbc = None


def get_attributes(obj):
    return [attr for attr in dir(obj) if not attr.startswith("__")]


def forms(models: list):
    """Collect (GraphQL) Input-Forms"""
    all_forms: dict = {}
    if dbc:
        for current in models:
            if hasattr(current.object, "__spoc__"):
                if (
                    current.object.__spoc__.metadata.get("engine")
                    == "graphql-form-admin"
                ):
                    for key in get_attributes(current.object):
                        active = getattr(current.object, key)
                        is_component = dbc.is_form(active)
                        if is_component:
                            name = active.__name__.replace("_", "")
                            found = all_forms.get(name)
                        if found and found != active:
                            app = current.app
                            err = f"""\n* <Form: { name }> is already in use by the <App: { app }>"""
                            err += """\n* <Forms> must have UNIQUE names."""
                            raise ValueError(err)
                        all_forms[name] = active
    return all_forms
