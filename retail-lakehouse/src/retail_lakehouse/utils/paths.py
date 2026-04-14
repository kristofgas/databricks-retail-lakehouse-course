"""Helpers for building data paths from config."""

from typing import Any


def raw_file_path(config: dict[str, Any], filename: str) -> str:
    """Return the full path to a raw data file."""
    return f"{config['raw_data_path']}/{filename}"
