"""
Form Creator
"""

import dataclasses as dc
import functools
import re
from types import SimpleNamespace
from typing import Any, Optional, TypeVar, get_origin

try:
    import strawberry

    STRAWBERRY_INPUT: Any = strawberry.input
    STRAWBERRY_FIELD: Any = strawberry.field
except ImportError:
    strawberry = None  # type: ignore
    STRAWBERRY_INPUT = False  # type: ignore
    STRAWBERRY_FIELD = False  # type: ignore

# Custom Typing
UNSET = TypeVar("UNSET", bool, None)


def dc_field(**kwargs):
    """DataClass Field Wrapper"""
    return dc.field(**kwargs)  # pylint: disable=invalid-field-call


@dc.dataclass
class FormField:
    """DataClass -> Field"""

    type: Any
    name: str | None = None
    default: Any = UNSET
    required: bool = False
    regex: dict = dc.field(default_factory=dict)
    rules: list = dc.field(default_factory=list)
    clean: dict = dc.field(default_factory=dict)
    deprecation_reason: str | None = None
    # fixed: bool = False


@dc.dataclass
class FormError:
    """DataClass -> Form Error"""

    field: str
    type: str
    text: str | None = None


@dc.dataclass
class Form:
    """DataClass -> Form Response"""

    data: Any = dc.field(default_factory=dict)
    errors: list = dc.field(default_factory=list)
    is_valid: bool = False
    next: Any = None


def form_field(**kwargs) -> Any:
    """Field Wrapper"""

    def field(_, kind) -> Any:
        return FormField(kind, **kwargs)

    return field


def regex_search(pattern: str, text: str):
    """Search for { Regular Expression } Pattern"""

    # regex_search("[\w\.-]+@[\w\.-]+", "admin@example.com")
    def is_regex(x):
        "Real Regex"
        return x is not None

    return is_regex(re.search(pattern, str(text)))


def regex_replace(items: list[Any], text: str):
    """Replace Text"""
    for selector, replacement in items:
        text = re.sub(selector, replacement, text)
    return text


def default_value(default):
    """Create Default Value"""
    is_callable = False
    if callable(default):
        is_callable = True
        field = dc_field(default_factory=default)
    else:
        field = dc_field(default=default)
    return is_callable, field


def custom_field_maker(info: FormField):
    """Custom Field Maker"""
    if info.default != UNSET and not info.required:
        is_callable, default = default_value(info.default)
        if is_callable:
            the_type: Any = Optional[info.type]
        else:
            the_type = info.type
        field = tuple([info.name, the_type, default])
    else:
        extra_fields = []
        if not info.required:
            the_type = Optional[info.type]
            extra_fields.extend([the_type, dc_field(default=None)])
        else:
            the_type = info.type
            extra_fields.append(the_type)
        field = tuple([info.name, *extra_fields])
    return field


class FormTools:
    """Form Tools"""

    @staticmethod
    def typing(name, setup, current_input):
        """Form Typing"""
        errors = []
        is_valid_type = False
        type_origin = get_origin(setup.type)
        # Type Origin
        if type_origin is None:
            type_to_check = setup.type
        else:
            type_to_check = type_origin
        # Strawberry
        if strawberry and type_to_check == strawberry.ID:
            is_valid_type = True
        else:
            is_valid_type = isinstance(current_input, type_to_check)
        # Error Type
        if not is_valid_type and current_input:
            the_error = FormError(
                field=name,
                type="typing",
                text=type_to_check,  # f"{type_to_check} is required."
            )
            errors.append(the_error.__dict__)
        return errors

    @staticmethod
    def required(name, setup, form, current_input):
        """Form Required"""
        errors = []
        if setup.required:
            the_error = FormError(
                field=name,
                type="required",
                text=name,  # f"{name} is required."
            )
            if name not in form.keys() or not current_input:
                errors.append(the_error.__dict__)
        return errors

    @staticmethod
    def validators(name, setup, current_input):
        """Form Validators"""
        errors = []
        if current_input:
            # Regex Validator
            for test, error_message in setup.regex.items():
                found_regex = not regex_search(test, current_input)
                if found_regex:
                    the_error = FormError(field=name, type="regex", text=error_message)
                    errors.append(the_error.__dict__)
            # Custom Rules Validator
            for test in setup.rules:
                if callable(test):
                    try:
                        found_rule = test(current_input)
                        if found_rule is not True:
                            the_error = FormError(
                                field=name, type="rule", text=found_rule
                            )
                            errors.append(the_error.__dict__)
                    except Exception:  # pylint: disable=broad-exception-caught
                        the_error = FormError(
                            field=name, type="invalid", text="invalid input"
                        )
                        errors.append(the_error.__dict__)
        return errors

    @staticmethod
    def filters(setup, current_input, errors):
        """Form Filters"""
        if len(errors) == 0:
            regex_methods = []
            new_input = current_input
            if setup.filters:
                for clean in setup.filters.get("regex", []):
                    if isinstance(clean, (list, tuple)):
                        regex_methods.append(clean)
                # Regex Methods
                if isinstance(current_input, str) and len(regex_methods) > 0:
                    new_input = regex_replace(regex_methods, current_input)
                # Rule Methods
                for clean in setup.filters.get("rules", []):
                    if callable(clean):
                        try:
                            new_input = clean(new_input)
                        except Exception:  # pylint: disable=broad-exception-caught
                            pass
            return new_input
        return current_input

    @staticmethod
    def default(setup, current_input):
        """Form Default"""
        if not current_input:
            if callable(setup.default):
                return setup.default()
            return setup.default
        return current_input


class BaseForm:
    """(Singleton) Create a Form"""

    __optionals__: Any
    __deprecated__: Any
    __annotations__: Any

    def __new__(cls):
        """Class Starter"""
        it_id = "__it__"
        it = cls.__dict__.get(it_id, None)
        if it is not None:
            return it
        it = object.__new__(cls)
        setattr(cls, it_id, it)
        it._init_only_once_for_the_whole_class(cls)
        return it

    def _init_only_once_for_the_whole_class(self, cls):
        """Class __init__ Replacement"""
        builtin_keys = [
            "Next",
            # Tools
            "_init_only_once_for_the_whole_class",
            "_validate",
        ]
        fields = [
            x for x in dir(self) if not x.startswith("__") and x not in builtin_keys
        ]
        validate = {}
        annotations = {}
        deprecated = {}
        optionals = {}
        custom_annotations: Any = {"required": [], "optional": []}
        for f_name in fields:
            pre_field = getattr(self, f_name)
            current = pre_field(self.__annotations__.get(f_name, str))
            current.name = f_name
            validate[f_name] = current
            if current.required:
                annotations[f_name] = current.type
            else:
                annotations[f_name] = Optional[current.type]
            # Custom Type Annotation
            custom_field = custom_field_maker(current)
            if not current.required:
                custom_field = (
                    custom_field[0],
                    Optional[custom_field[1]],
                    custom_field[2],
                )
                optionals[f_name] = custom_field[2]
                custom_annotations["optional"].append(custom_field)
            else:
                custom_annotations["required"].append(custom_field)
            if current.deprecation_reason:
                deprecated[f_name] = current.deprecation_reason

        self._config = validate
        cls.__optionals__ = optionals
        cls.__deprecated__ = deprecated
        cls.__annotations__ = annotations
        cls.__custom_annotations__ = custom_annotations

    def __call__(self, form: dict | None = None):
        form = form or {}
        errors = []
        args: Any = {**form}

        for name, setup in self._config.items():
            value = form.get(name)
            errors.extend(FormTools.typing(name, setup, value))
            errors.extend(FormTools.required(name, setup, form, value))
            errors.extend(FormTools.validators(name, setup, value))
            # Update Value
            value = FormTools.default(setup, value)
            args[name] = FormTools.filters(setup, value, errors)

        if "input" in args:
            del args["input"]

        obj_input = SimpleNamespace(**args)
        return Form(data=obj_input, errors=errors, is_valid=len(errors) == 0)


def run_validator(form, validator):
    """Return Custom Response to the Dataclass"""
    user_input = validator(form.__dict__)
    if hasattr(validator, "Next"):
        if hasattr(validator.Next, "run"):
            if user_input.is_valid:
                user_input.next = validator.Next.run(user_input.data)
    form.input = user_input


def make_dataclass(base_class, form_name):
    """(Custom) Make Dataclass"""
    validator = base_class()
    form_annotations = base_class.__custom_annotations__
    cleaned_data = custom_field_maker(
        FormField(name="input", type=Any, default=None, required=False)
    )
    form_annotations["optional"].append(cleaned_data)
    class_annotations = form_annotations["required"]
    class_annotations.extend(form_annotations["optional"])
    data_class = dc.make_dataclass(
        form_name,
        class_annotations,
        namespace={"__post_init__": lambda self: run_validator(self, validator)},
    )
    del data_class.__annotations__["input"]
    return data_class


def dataclass(  # pylint: disable=too-many-branches
    original_object: Any = None,
    *,
    name: str | None = None,
    prefix: str | list[str] | None = None,
    suffix: str | list[str] | None = None,
    graphql: bool = True,
    description: str | None = None,
):
    """Form To GQL Input"""

    # Starting Wrapper. . .
    if original_object is None:
        return functools.partial(
            dataclass,
            name=name,
            prefix=prefix,
            suffix=suffix,
            graphql=graphql,
            description=description,
        )

    # Configure Class
    if name:
        form_name = name
    else:
        form_name = ""
        # Class Prefix
        if prefix:
            if isinstance(prefix, list):
                for fix in prefix:
                    form_name += fix.title()
            else:
                form_name += prefix.title()
        # Class Name
        form_name += f"{original_object.__name__}"
        # Class Suffix
        if suffix:
            if isinstance(suffix, list):
                for fix in suffix:
                    form_name += fix.title()
            else:
                form_name += suffix.title()
    # Re-Create Class with Form
    custom_class: Any = type(original_object.__name__, (BaseForm, original_object), {})

    # Create Data-Class
    data_class = make_dataclass(custom_class, form_name)

    if STRAWBERRY_FIELD and graphql:
        for f_name, reason in custom_class.__deprecated__.items():
            config = custom_class.__optionals__.get(f_name)
            extras = {}
            if config:
                extras["default"] = config.default
                extras["default_factory"] = config.default_factory
            # Attach Strawberry Field
            setattr(
                data_class,
                f_name,
                STRAWBERRY_FIELD(**extras, deprecation_reason=reason),
            )
    if STRAWBERRY_INPUT and graphql:
        description = description or original_object.__doc__
        data_class = STRAWBERRY_INPUT(data_class, description=description)
    # Create Component
    return data_class


def form_cleaner(regex: Any = None, rules: Any = None) -> dict:
    """Form Filters"""
    regex = regex or []
    rules = rules or []
    return {
        "regex": regex,
        "rules": rules,
    }


def graphql_input(prefix: Any = None, suffix: Any = None):
    """GraphQL-Form(s) with a { Suffix } or { Prefix } in Common"""
    return functools.partial(dataclass, prefix=prefix, suffix=suffix, graphql=True)
