"""Base formatter interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class IndexData:
    """Data structure for a documentation index."""

    name: str
    """Name of the index (e.g., "Project Docs Index")."""

    root: str
    """Root path for the documentation."""

    directories: dict[str, list[str]]
    """Mapping of directory paths to file lists."""

    instruction: str | None = None
    """Optional instruction for AI agents."""

    metadata: dict[str, str] = field(default_factory=dict)
    """Additional metadata key-value pairs."""


class Formatter(ABC):
    """Abstract base class for output formatters."""

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of this format."""
        ...

    @property
    @abstractmethod
    def file_extension(self) -> str:
        """The default file extension for this format."""
        ...

    @abstractmethod
    def format(self, data: IndexData) -> str:
        """
        Format the index data as a string.

        Args:
            data: The index data to format.

        Returns:
            The formatted string.
        """
        ...
