"""Naming convention helpers."""

import re


def to_snake_case(name: str) -> str:
    """Convert a column name to snake_case.

    Useful when source data has camelCase or space-separated column names
    and you want to standardize them in the silver layer.
    """
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    name = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", name)
    return name.lower().replace(" ", "_").replace("-", "_")
