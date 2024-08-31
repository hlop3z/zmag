# -*- coding: utf-8 -*-
"""
{ Type | Model }
"""

import dataclasses as dc
import inspect
from collections import OrderedDict, namedtuple
from types import SimpleNamespace
from typing import Annotated, Any, Optional, Type, get_origin, get_type_hints

from ...external import STRAWBERRY

Field = namedtuple("Field", ["name", "type", "field"])


def is_property(field) -> bool:
    """
    Check if the given field is a property.

    Args:
        field: The field to check.

    Returns:
        bool: True if the field is a property, False otherwise.
    """
    return isinstance(field, property)


def is_complex(value: Any) -> bool:
    """
    Check if the value is a complex type, specifically an Annotated type.

    Args:
        value: The value to check.

    Returns:
        bool: True if the value is an Annotated type, False otherwise.
    """
    return get_origin(value) is Annotated


def get_annotation(field) -> Any:
    """
    Get the annotation type for a field, using Optional if it's not complex.

    Args:
        field: The field whose annotation to retrieve.

    Returns:
        Any: The annotation type.
    """
    if is_complex(field):
        return field
    return Optional[field]


def dataclass_field(**kwargs) -> Any:
    """
    Create a dataclass field with default or default factory values.

    Args:
        **kwargs: Arguments for the field, such as default and default_factory.

    Returns:
        Any: The configured dataclass field.
    """
    args = {k: v for k, v in kwargs.items() if k not in ["default", "default_factory"]}
    value = kwargs.get("default_factory", None) or kwargs.get("default", None)
    if callable(value):
        args["default_factory"] = value
    else:
        args["default"] = value
    return dc.field(**args)  # pylint: disable=invalid-field-call


def extract_model_fields_properties(cls: Type, root_class) -> SimpleNamespace:
    """
    Extract fields and properties from a class and return them in a SimpleNamespace.

    Args:
        cls: The class to inspect.

    Returns:
        SimpleNamespace: A namespace with the class name, type, fields, properties, and bases.
    """
    fields = OrderedDict()
    properties = OrderedDict()

    # Class Fields
    for name, kind in cls.__annotations__.items():
        fields[name] = Field(
            name=name,
            type=get_annotation(kind),
            field=getattr(cls, name, None),
        )

    # Inspect the class to find properties
    for name, obj in inspect.getmembers(cls, is_property):
        hints = get_type_hints(obj.fget)
        obj.fget.__annotations__["return"] = Optional[hints.get("return", str)]
        properties[name] = STRAWBERRY.field(obj.fget)

    bases = list(cls.__bases__)
    # bases.pop(0)
    return SimpleNamespace(
        name=cls.__name__,
        type=cls,
        fields=fields,
        properties=properties,
        bases=[x for x in bases if x not in [object, root_class]],
    )


def class_attributes(cls: Type, root_class) -> Any:
    """
    Create a class attributes
    """
    _class = extract_model_fields_properties(cls, root_class)
    attributes = {item.name: item.field for item in _class.fields.values()}
    attributes.update(_class.properties)
    annotations = {item.name: item.type for item in _class.fields.values()}
    return SimpleNamespace(root=_class, attributes=attributes, annotations=annotations)


def create_typed_class(cls: Type, root_class: Any) -> Any:
    """
    Create a class from a class, merging fields and properties.

    Args:
        cls: The class to convert into a dataclass.

    Returns:
        dc.dataclass: The created dataclass.
    """
    current = class_attributes(cls, root_class)
    attributes = {}
    annotations = {}

    # Bases
    for base_class in current.root.bases:
        base = class_attributes(base_class, root_class)
        attributes.update(base.attributes)
        annotations.update(base.annotations)

    # Current
    attributes.update(current.attributes)
    annotations.update(current.annotations)

    # Build Class
    the_class = type(current.root.name, (), {**attributes})
    the_class.__annotations__ = annotations

    return the_class
