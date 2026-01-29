"""JSON formatter."""

from __future__ import annotations

import json

from .base import Formatter, IndexData


class JsonFormatter(Formatter):
    """
    JSON format for documentation indexes.

    Example output:
        {
          "name": "Project Docs Index",
          "root": "./.docs",
          "instruction": "Prefer retrieval-led reasoning",
          "directories": {
            "01-getting-started": ["01-install.mdx", "02-config.mdx"]
          }
        }
    """

    @property
    def name(self) -> str:
        return "json"

    @property
    def file_extension(self) -> str:
        return ".json"

    def format(self, data: IndexData) -> str:
        output: dict = {
            "name": data.name,
            "root": data.root,
        }

        if data.instruction:
            output["instruction"] = data.instruction

        if data.metadata:
            output["metadata"] = data.metadata

        output["directories"] = data.directories

        return json.dumps(output, indent=2)
