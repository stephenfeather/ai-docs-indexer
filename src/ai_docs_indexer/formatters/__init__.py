"""Output formatters for documentation indexes."""

from .base import Formatter, IndexData
from .json import JsonFormatter
from .pipe import PipeFormatter
from .yaml import YamlFormatter

__all__ = [
    "Formatter",
    "IndexData",
    "PipeFormatter",
    "JsonFormatter",
    "YamlFormatter",
]


def get_formatter(format_name: str) -> Formatter:
    """
    Get a formatter by name.

    Args:
        format_name: The format name (pipe, json, yaml).

    Returns:
        A Formatter instance.

    Raises:
        ValueError: If the format is not supported.
    """
    formatters = {
        "pipe": PipeFormatter,
        "json": JsonFormatter,
        "yaml": YamlFormatter,
    }

    if format_name not in formatters:
        valid = ", ".join(formatters.keys())
        raise ValueError(f"Unknown format '{format_name}'. Valid formats: {valid}")

    return formatters[format_name]()
