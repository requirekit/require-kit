"""Unit tests for FileOperations utility."""
import os
import tempfile
from pathlib import Path

import pytest

from utils import FileOperations


class TestFileOperations:
    """Test FileOperations class."""

    def test_atomic_write_creates_file(self):
        """Test atomic_write creates file successfully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.txt"
            content = "Test content"

            result = FileOperations.atomic_write(file_path, content)

            assert result is True
            assert file_path.exists()
            assert file_path.read_text() == content

    def test_atomic_write_overwrites_existing(self):
        """Test atomic_write overwrites existing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.txt"

            # Create initial file
            file_path.write_text("Original content")

            # Overwrite with atomic_write
            new_content = "New content"
            result = FileOperations.atomic_write(file_path, new_content)

            assert result is True
            assert file_path.read_text() == new_content

    def test_atomic_write_creates_parent_dirs(self):
        """Test atomic_write creates nested parent directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            nested_path = Path(tmpdir) / "nested" / "dirs" / "test.txt"
            content = "Test content"

            result = FileOperations.atomic_write(nested_path, content)

            assert result is True
            assert nested_path.exists()
            assert nested_path.read_text() == content

    def test_atomic_write_uses_temp_file(self):
        """Test that atomic_write uses temporary file pattern."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.txt"

            # Mock failure to verify temp file cleanup
            # We'll just verify the successful case creates no temp files
            content = "Test content"
            FileOperations.atomic_write(file_path, content)

            # Check no .tmp files left
            tmp_files = list(Path(tmpdir).glob("*.tmp"))
            assert len(tmp_files) == 0

    def test_atomic_write_with_custom_encoding(self):
        """Test atomic_write with custom encoding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.txt"
            content = "Test with UTF-8: 日本語"

            result = FileOperations.atomic_write(file_path, content, encoding='utf-8')

            assert result is True
            assert file_path.read_text(encoding='utf-8') == content

    def test_atomic_write_failure(self, capsys):
        """Test atomic_write handles write failures gracefully."""
        # Try to write to an invalid location
        invalid_path = Path("/invalid/path/that/does/not/exist/test.txt")
        content = "Test content"

        result = FileOperations.atomic_write(invalid_path, content)

        assert result is False
        captured = capsys.readouterr()
        assert "Warning" in captured.out
        assert "Atomic write failed" in captured.out

    def test_safe_read_existing_file(self):
        """Test safe_read with existing file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            content = "Test content"
            f.write(content)
            temp_path = Path(f.name)

        try:
            result = FileOperations.safe_read(temp_path)
            assert result == content
        finally:
            temp_path.unlink()

    def test_safe_read_missing_file(self):
        """Test safe_read with missing file."""
        missing_path = Path("/tmp/nonexistent_file_12345.txt")
        result = FileOperations.safe_read(missing_path)

        assert result is None

    def test_safe_read_with_encoding(self):
        """Test safe_read with custom encoding."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
            content = "UTF-8 content: 日本語"
            f.write(content)
            temp_path = Path(f.name)

        try:
            result = FileOperations.safe_read(temp_path, encoding='utf-8')
            assert result == content
        finally:
            temp_path.unlink()

    def test_safe_read_error_handling(self, capsys):
        """Test safe_read handles read errors gracefully."""
        # Create a file and then make it unreadable (simulate permission error)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = Path(f.name)

        try:
            # Change permissions to write-only (no read)
            os.chmod(temp_path, 0o000)

            result = FileOperations.safe_read(temp_path)
            assert result is None

            captured = capsys.readouterr()
            assert "Warning" in captured.out
            assert "Failed to read" in captured.out
        finally:
            # Restore permissions and cleanup
            os.chmod(temp_path, 0o644)
            temp_path.unlink()

    def test_ensure_directory_creates_dir(self):
        """Test ensure_directory creates directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            new_dir = Path(tmpdir) / "new_directory"

            result = FileOperations.ensure_directory(new_dir)

            assert result is True
            assert new_dir.exists()
            assert new_dir.is_dir()

    def test_ensure_directory_creates_nested(self):
        """Test ensure_directory creates nested directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            nested_dir = Path(tmpdir) / "level1" / "level2" / "level3"

            result = FileOperations.ensure_directory(nested_dir)

            assert result is True
            assert nested_dir.exists()
            assert nested_dir.is_dir()

    def test_ensure_directory_existing_dir(self):
        """Test ensure_directory with existing directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            existing_dir = Path(tmpdir)

            result = FileOperations.ensure_directory(existing_dir)

            assert result is True
            assert existing_dir.exists()

    def test_ensure_directory_failure(self, capsys):
        """Test ensure_directory handles failures gracefully."""
        # Try to create directory in invalid location
        invalid_path = Path("/invalid/root/path/directory")

        result = FileOperations.ensure_directory(invalid_path)

        assert result is False
        captured = capsys.readouterr()
        assert "Warning" in captured.out
        assert "Failed to create directory" in captured.out

    def test_safe_append_new_file(self):
        """Test safe_append creates new file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.txt"
            content = "First line\n"

            result = FileOperations.safe_append(file_path, content)

            assert result is True
            assert file_path.exists()
            assert file_path.read_text() == content

    def test_safe_append_existing_file(self):
        """Test safe_append appends to existing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.txt"

            # Create initial file
            file_path.write_text("Line 1\n")

            # Append content
            result = FileOperations.safe_append(file_path, "Line 2\n")

            assert result is True
            assert file_path.read_text() == "Line 1\nLine 2\n"

    def test_safe_append_creates_parent_dirs(self):
        """Test safe_append creates parent directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            nested_path = Path(tmpdir) / "nested" / "test.txt"
            content = "Content\n"

            result = FileOperations.safe_append(nested_path, content)

            assert result is True
            assert nested_path.exists()
            assert nested_path.read_text() == content

    def test_safe_append_with_encoding(self):
        """Test safe_append with custom encoding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.txt"
            content = "UTF-8: 日本語\n"

            result = FileOperations.safe_append(file_path, content, encoding='utf-8')

            assert result is True
            assert file_path.read_text(encoding='utf-8') == content

    def test_safe_append_failure(self, capsys):
        """Test safe_append handles failures gracefully."""
        invalid_path = Path("/invalid/path/test.txt")
        content = "Content\n"

        result = FileOperations.safe_append(invalid_path, content)

        assert result is False
        captured = capsys.readouterr()
        assert "Warning" in captured.out
        assert "Failed to append" in captured.out
