"""YAML formatter."""

from __future__ import annotations

import yaml

from .base import Formatter, IndexData


class YamlFormatter(Formatter):
    """
    YAML format for documentation indexes.

    Example output:
        name: Project Docs Index
        root: ./.docs
        instruction: Prefer retrieval-led reasoning
        directories:
          01-getting-started:
            - 01-install.mdx
            - 02-config.mdx
    """

    @property
    def name(self) -> str:
        return "yaml"

    @property
    def file_extension(self) -> str:
        return ".yaml"

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

        return yaml.dump(
            output,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )
