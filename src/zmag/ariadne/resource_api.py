import re


def transform_name(input_string, sign):
    output_string = re.sub(rf"{sign}+", sign, input_string)
    output_string = re.sub(rf"[^a-zA-Z{sign}]", "", output_string)
    if output_string.startswith(f"{sign}"):
        output_string = output_string[1:]
    if output_string.endswith(f"{sign}"):
        output_string = output_string[:-1]
    return output_string


def snake_case(input_string):
    output_string = transform_name(input_string, "_")
    return output_string.lower()


def kebab_case(input_string):
    output_string = transform_name(input_string, "-")
    return output_string.lower()


class FunctionRegistry:
    def __init__(self):
        self.methods = {}

    def resolve(self, name):
        name = snake_case(name)

        def decorator(func):
            self.methods[name] = func
            return func

        return decorator


class ResourcesAPI:
    _instances = {}

    def __new__(cls, *args, name=None):
        name = kebab_case(name)
        if name not in cls._instances:
            instance = super().__new__(cls)
            instance.name = name
            instance._groups = set({})
            instance._initialize(*args)
            cls._instances[name] = instance
        return cls._instances[name]

    def _initialize(self, *args):
        if args:
            for key in args:
                if not isinstance(key, str):
                    raise ValueError("Strings Only")
                self.create_group(key)
                self._groups.add(key)

    @property
    def groups(self):
        return frozenset(self._groups)

    @property
    def keys(self):
        all_methods = set()
        for group in list(self.groups):
            private_name = f"_{group}"
            resource = getattr(self, private_name)
            if resource:
                methods = list(resource.methods.keys())
                for method in methods:
                    all_methods.add(f"{group}.{method}")
        return list(all_methods)

    def api(self, resource_name):
        group = None
        method = None
        # Get Resource Location
        resource_parts = resource_name.split(".")
        if len(resource_parts) == 2:
            group = resource_parts[0]
            method = resource_parts[1]
        # Get Resource Method
        private_name = f"_{group}"
        resource = getattr(self, private_name)
        if resource:
            return resource.methods.get(method)
        return None

    def create_group(self, public_name: str):
        private_name = f"_{public_name}"

        def resolve(*args, **kwargs):
            return getattr(self, private_name).resolve(*args, **kwargs)

        setattr(self, private_name, FunctionRegistry())
        setattr(self, public_name, resolve)
