"""Tests for the formatters module."""

import json

import pytest
import yaml

from ai_docs_indexer.formatters import (
    IndexData,
    JsonFormatter,
    PipeFormatter,
    YamlFormatter,
    get_formatter,
)


@pytest.fixture
def sample_data():
    """Sample index data for testing."""
    return IndexData(
        name="Test Docs",
        root="./.docs",
        directories={
            "": ["README.md"],
            "01-getting-started": ["install.mdx", "config.mdx"],
            "02-guides": ["overview.md"],
        },
        instruction="Prefer retrieval-led reasoning",
    )


@pytest.fixture
def minimal_data():
    """Minimal index data without optional fields."""
    return IndexData(
        name="Minimal",
        root="./docs",
        directories={"": ["index.md"]},
    )


class TestGetFormatter:
    """Tests for get_formatter function."""

    def test_get_pipe_formatter(self):
        """Test getting pipe formatter."""
        formatter = get_formatter("pipe")
        assert isinstance(formatter, PipeFormatter)

    def test_get_json_formatter(self):
        """Test getting JSON formatter."""
        formatter = get_formatter("json")
        assert isinstance(formatter, JsonFormatter)

    def test_get_yaml_formatter(self):
        """Test getting YAML formatter."""
        formatter = get_formatter("yaml")
        assert isinstance(formatter, YamlFormatter)

    def test_unknown_formatter(self):
        """Test that unknown format raises error."""
        with pytest.raises(ValueError, match="Unknown format"):
            get_formatter("unknown")


class TestPipeFormatter:
    """Tests for PipeFormatter."""

    def test_format_full(self, sample_data):
        """Test formatting with all fields."""
        formatter = PipeFormatter()
        result = formatter.format(sample_data)

        lines = result.split("\n")
        assert lines[0] == "[Test Docs]|root: ./.docs"
        assert lines[1] == "|IMPORTANT: Prefer retrieval-led reasoning"
        assert "|.:{README.md}" in result
        assert "|01-getting-started:{install.mdx,config.mdx}" in result
        assert "|02-guides:{overview.md}" in result

    def test_format_minimal(self, minimal_data):
        """Test formatting without optional fields."""
        formatter = PipeFormatter()
        result = formatter.format(minimal_data)

        assert "[Minimal]|root: ./docs" in result
        assert "IMPORTANT" not in result
        assert "|.:{index.md}" in result

    def test_name_and_extension(self):
        """Test formatter metadata."""
        formatter = PipeFormatter()
        assert formatter.name == "pipe"
        assert formatter.file_extension == ".md"


class TestJsonFormatter:
    """Tests for JsonFormatter."""

    def test_format_full(self, sample_data):
        """Test JSON formatting with all fields."""
        formatter = JsonFormatter()
        result = formatter.format(sample_data)

        data = json.loads(result)
        assert data["name"] == "Test Docs"
        assert data["root"] == "./.docs"
        assert data["instruction"] == "Prefer retrieval-led reasoning"
        assert data["directories"]["01-getting-started"] == ["install.mdx", "config.mdx"]

    def test_format_minimal(self, minimal_data):
        """Test JSON formatting without optional fields."""
        formatter = JsonFormatter()
        result = formatter.format(minimal_data)

        data = json.loads(result)
        assert data["name"] == "Minimal"
        assert "instruction" not in data

    def test_name_and_extension(self):
        """Test formatter metadata."""
        formatter = JsonFormatter()
        assert formatter.name == "json"
        assert formatter.file_extension == ".json"


class TestYamlFormatter:
    """Tests for YamlFormatter."""

    def test_format_full(self, sample_data):
        """Test YAML formatting with all fields."""
        formatter = YamlFormatter()
        result = formatter.format(sample_data)

        data = yaml.safe_load(result)
        assert data["name"] == "Test Docs"
        assert data["root"] == "./.docs"
        assert data["instruction"] == "Prefer retrieval-led reasoning"
        assert data["directories"]["01-getting-started"] == ["install.mdx", "config.mdx"]

    def test_format_minimal(self, minimal_data):
        """Test YAML formatting without optional fields."""
        formatter = YamlFormatter()
        result = formatter.format(minimal_data)

        data = yaml.safe_load(result)
        assert data["name"] == "Minimal"
        assert "instruction" not in data

    def test_name_and_extension(self):
        """Test formatter metadata."""
        formatter = YamlFormatter()
        assert formatter.name == "yaml"
        assert formatter.file_extension == ".yaml"


class TestIndexData:
    """Tests for IndexData dataclass."""

    def test_create_with_all_fields(self):
        """Test creating IndexData with all fields."""
        data = IndexData(
            name="Test",
            root="./test",
            directories={"": ["file.md"]},
            instruction="Test instruction",
            metadata={"key": "value"},
        )

        assert data.name == "Test"
        assert data.instruction == "Test instruction"
        assert data.metadata == {"key": "value"}

    def test_defaults(self):
        """Test IndexData default values."""
        data = IndexData(
            name="Test",
            root="./test",
            directories={},
        )

        assert data.instruction is None
        assert data.metadata == {}
