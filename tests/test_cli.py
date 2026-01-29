"""Tests for the CLI module."""

import tempfile
from pathlib import Path

import pytest
from click.testing import CliRunner

from ai_docs_indexer.cli import main


@pytest.fixture
def runner():
    """Create a CLI test runner."""
    return CliRunner()


@pytest.fixture
def temp_docs():
    """Create a temporary directory with sample docs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        docs_dir = Path(tmpdir) / "docs"
        docs_dir.mkdir()
        (docs_dir / "README.md").write_text("# README")
        (docs_dir / "guide.md").write_text("# Guide")

        subdir = docs_dir / "getting-started"
        subdir.mkdir()
        (subdir / "install.md").write_text("# Install")

        yield docs_dir


class TestScanCommand:
    """Tests for the scan command."""

    def test_scan_basic(self, runner, temp_docs):
        """Test basic scan command."""
        result = runner.invoke(main, ["scan", str(temp_docs), "--quiet"])
        assert result.exit_code == 0
        assert "[Documentation Index]" in result.output

    def test_scan_with_name(self, runner, temp_docs):
        """Test scan with custom name."""
        result = runner.invoke(main, ["scan", str(temp_docs), "--name", "My Docs", "--quiet"])
        assert result.exit_code == 0
        assert "[My Docs]" in result.output

    def test_scan_compress_removes_newlines(self, runner, temp_docs):
        """Test that --compress outputs on a single line."""
        result = runner.invoke(main, ["scan", str(temp_docs), "--quiet", "--compress"])
        assert result.exit_code == 0
        # Output should be on a single line (only the trailing newline from echo)
        lines = result.output.strip().split("\n")
        assert len(lines) == 1
        # Should still contain the expected content
        assert "[Documentation Index]" in result.output
        assert "README.md" in result.output

    def test_scan_without_compress_has_newlines(self, runner, temp_docs):
        """Test that output without --compress has multiple lines."""
        result = runner.invoke(main, ["scan", str(temp_docs), "--quiet"])
        assert result.exit_code == 0
        lines = result.output.strip().split("\n")
        # Should have multiple lines (header, directories, etc.)
        assert len(lines) > 1

    def test_scan_compress_short_flag(self, runner, temp_docs):
        """Test -c short flag for compress."""
        result = runner.invoke(main, ["scan", str(temp_docs), "--quiet", "-c"])
        assert result.exit_code == 0
        lines = result.output.strip().split("\n")
        assert len(lines) == 1


class TestFormatsCommand:
    """Tests for the formats command."""

    def test_formats_list(self, runner):
        """Test listing available formats."""
        result = runner.invoke(main, ["formats"])
        assert result.exit_code == 0
        assert "pipe" in result.output
        assert "json" in result.output
        assert "yaml" in result.output
