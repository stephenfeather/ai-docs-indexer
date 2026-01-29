"""Tests for the scanner module."""

from pathlib import Path

import pytest

from ai_docs_indexer.scanner import scan_directory


FIXTURES_DIR = Path(__file__).parent / "fixtures"


class TestScanDirectory:
    """Tests for scan_directory function."""

    def test_scan_sample_docs(self):
        """Test scanning the sample docs fixture."""
        result = scan_directory(FIXTURES_DIR / "sample-docs")

        assert result.total_files == 7
        assert len(result.directories) == 4

        # Check root-level files
        assert "" in result.directories
        assert result.directories[""] == ["README.md"]

        # Check subdirectories
        assert "01-getting-started" in result.directories
        assert result.directories["01-getting-started"] == [
            "01-install.mdx",
            "02-config.mdx",
        ]

        assert "02-guides" in result.directories
        assert result.directories["02-guides"] == ["advanced.md", "overview.md"]

        assert "03-api" in result.directories
        assert result.directories["03-api"] == ["endpoints.mdx", "reference.md"]

    def test_extension_filter(self):
        """Test filtering by extension."""
        result = scan_directory(
            FIXTURES_DIR / "sample-docs",
            extensions=(".md",),
        )

        # Should only find .md files (README.md, overview.md, advanced.md, reference.md)
        assert result.total_files == 4

    def test_nonexistent_path(self):
        """Test that nonexistent path raises error."""
        with pytest.raises(ValueError, match="Path does not exist"):
            scan_directory("/nonexistent/path")

    def test_file_instead_of_directory(self, tmp_path):
        """Test that passing a file raises error."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")

        with pytest.raises(ValueError, match="Path is not a directory"):
            scan_directory(test_file)

    def test_empty_directory(self, tmp_path):
        """Test scanning an empty directory."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        result = scan_directory(empty_dir)

        assert result.total_files == 0
        assert len(result.directories) == 0

    def test_hidden_files_excluded_by_default(self, tmp_path):
        """Test that hidden files are excluded by default."""
        (tmp_path / ".hidden.md").write_text("hidden")
        (tmp_path / "visible.md").write_text("visible")

        result = scan_directory(tmp_path)

        assert result.total_files == 1
        assert result.directories[""] == ["visible.md"]

    def test_hidden_files_included(self, tmp_path):
        """Test including hidden files."""
        (tmp_path / ".hidden.md").write_text("hidden")
        (tmp_path / "visible.md").write_text("visible")

        result = scan_directory(tmp_path, include_hidden=True)

        assert result.total_files == 2
        assert ".hidden.md" in result.directories[""]
        assert "visible.md" in result.directories[""]

    def test_hidden_directories_excluded_by_default(self, tmp_path):
        """Test that hidden directories are excluded by default."""
        hidden_dir = tmp_path / ".hidden"
        hidden_dir.mkdir()
        (hidden_dir / "doc.md").write_text("doc")
        (tmp_path / "visible.md").write_text("visible")

        result = scan_directory(tmp_path)

        assert result.total_files == 1
        assert ".hidden" not in result.directories

    def test_files_sorted_alphabetically(self, tmp_path):
        """Test that files are sorted alphabetically."""
        (tmp_path / "zebra.md").write_text("")
        (tmp_path / "alpha.md").write_text("")
        (tmp_path / "beta.md").write_text("")

        result = scan_directory(tmp_path)

        assert result.directories[""] == ["alpha.md", "beta.md", "zebra.md"]
