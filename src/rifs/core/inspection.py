"""Inspect a python object and iterate over the attributes and rebuild the object with the 
discovered imports and defined attributes.
"""

from collections import namedtuple as _namedtuple
from dataclasses import dataclass
from typing import Any as _Any
from typing import Generator as _Generator


def define_namedtuple(value: "_namedtuple") -> str:
    """Define a namedtuple from the object.

    Args:
        value (object): The object to define the namedtuple from.

    Returns:
        str: The namedtuple definition.
    """
    name = value.__class__.__name__
    fields = value._fields
    return f"{name} = namedtuple('{name}', {fields})"


def find_import(value: object, namespace: str) -> str:
    """Find the import for the object.

    Args:
        value (object): The object to find the import for.

    Returns:
        str: The import for the object.
    """
    name = type(value).__name__
    if not hasattr(value, "__module__"):
        if value.__class__.__module__ == "builtins":
            return ""
        value = value.__class__
        name = value.__name__

    module_name = value.__module__
    if module_name == "__main__":
        module_name = namespace

    return f"from {module_name} import {name}"


def recursive_inspect_generator(value: _Any, namespace: str = "") -> _Generator[str, str, None]:
    """Recursively inspects a value and yields a string representation of its structure.

    Args:
        value (_Any): The value to inspect.
        namespace (str, optional): The namespace of the value. Defaults to "".

    Yields:
        str: A string representation of the structure of the value.
    """
    # Skip if the value is a built-in type
    if isinstance(value, (int, float, str, bool)):
        return
    if not hasattr(value, "__iter__") and not hasattr(value, "_fields"):
        yield find_import(value, namespace)
        return
    if hasattr(value, "_fields"):
        yield define_namedtuple(value)  # Fix: Replace 'define_nametuple' with 'define_namedtuple'
        for field in value:
            yield find_import(field, namespace)
    items = value
    if isinstance(value, dict):
        yield find_import(value, namespace)
        items = value.values()
    for item in items:
        yield from recursive_inspect_generator(item, namespace)
    return


def base(kwargs: dict, namespace: str = "") -> list:
    """
    This function performs a base operation on the given kwargs and namespace.

    Args:
        kwargs (dict): A dictionary of keyword arguments.
        namespace (str): The namespace to operate on.

    Returns:
        None
    """
    imports = set()
    definitions = set()

    for _, value in kwargs.items():
        for import_ in recursive_inspect_generator(value, namespace):
            if "namedtuple" in import_:
                definitions.add(import_)
            else:
                imports.add(import_)

    # Clear empty strings in the imports
    imports = {import_ for import_ in imports if import_}
    if definitions:
        imports.add("from collections import namedtuple")

    return sorted(imports) + list(definitions)


def formatted_base(kwargs: dict, namespace: str = "") -> str:
    """Format the base operation.

    Args:
        kwargs (dict): A dictionary of keyword arguments.
        namespace (str): The namespace to operate on.

    Returns:
        str: The formatted base operation.
    """
    return "\n".join(base(kwargs, namespace))
