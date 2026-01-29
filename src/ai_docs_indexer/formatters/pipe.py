"""Pipe-delimited formatter (AGENTS.md style)."""

from __future__ import annotations

from .base import Formatter, IndexData


class PipeFormatter(Formatter):
    """
    Pipe-delimited format matching Vercel's AGENTS.md style.

    Example output:
        [Project Docs Index]|root: ./.docs
        |IMPORTANT: Prefer retrieval-led reasoning
        |01-getting-started:{01-install.mdx,02-config.mdx}
        |02-guides:{overview.md,advanced.md}
    """

    @property
    def name(self) -> str:
        return "pipe"

    @property
    def file_extension(self) -> str:
        return ".md"

    def format(self, data: IndexData) -> str:
        lines: list[str] = []

        # Header line with name and root
        header = f"[{data.name}]|root: {data.root}"
        lines.append(header)

        # Instruction line if present
        if data.instruction:
            lines.append(f"|IMPORTANT: {data.instruction}")

        # Metadata lines
        for key, value in data.metadata.items():
            lines.append(f"|{key}: {value}")

        # Directory entries
        for dir_path, files in sorted(data.directories.items()):
            files_str = ",".join(files)
            if dir_path:
                lines.append(f"|{dir_path}:{{{files_str}}}")
            else:
                # Root-level files
                lines.append(f"|.:{{{files_str}}}")

        return "\n".join(lines)
