"""Folder scanning logic for documentation indexing."""

from __future__ import annotations

import os
from pathlib import Path
from typing import NamedTuple


class ScanResult(NamedTuple):
    """Result of scanning a documentation directory."""

    directories: dict[str, list[str]]
    """Mapping of directory relative paths to list of matching files."""

    total_files: int
    """Total number of files found."""

    root_path: Path
    """The root path that was scanned."""


def scan_directory(
    path: str | Path,
    extensions: tuple[str, ...] = (".md", ".mdx"),
    include_hidden: bool = False,
    follow_symlinks: bool = False,
) -> ScanResult:
    """
    Recursively scan a directory for documentation files.

    Args:
        path: The directory path to scan.
        extensions: File extensions to include (with leading dot).
        include_hidden: Whether to include hidden files/directories.
        follow_symlinks: Whether to follow symbolic links.

    Returns:
        ScanResult with directories mapping and metadata.

    Raises:
        ValueError: If path doesn't exist or isn't a directory.
    """
    root = Path(path).resolve()

    if not root.exists():
        raise ValueError(f"Path does not exist: {root}")
    if not root.is_dir():
        raise ValueError(f"Path is not a directory: {root}")

    directories: dict[str, list[str]] = {}
    total_files = 0

    for dirpath, dirnames, filenames in os.walk(
        root, followlinks=follow_symlinks
    ):
        current = Path(dirpath)
        rel_dir = current.relative_to(root)

        # Filter hidden directories if needed
        if not include_hidden:
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]

        # Filter and collect matching files
        matching_files = []
        for filename in sorted(filenames):
            # Skip hidden files unless included
            if not include_hidden and filename.startswith("."):
                continue

            # Check extension
            if any(filename.endswith(ext) for ext in extensions):
                matching_files.append(filename)

        # Only add directories that have matching files
        if matching_files:
            dir_key = str(rel_dir) if str(rel_dir) != "." else ""
            directories[dir_key] = matching_files
            total_files += len(matching_files)

    return ScanResult(
        directories=directories,
        total_files=total_files,
        root_path=root,
    )


def get_gitignore_patterns(root: Path) -> list[str]:
    """
    Read .gitignore patterns from a directory.

    Args:
        root: The root directory to check for .gitignore.

    Returns:
        List of gitignore patterns (not yet used, placeholder for future).
    """
    gitignore_path = root / ".gitignore"
    if not gitignore_path.exists():
        return []

    patterns = []
    with open(gitignore_path) as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if line and not line.startswith("#"):
                patterns.append(line)

    return patterns
