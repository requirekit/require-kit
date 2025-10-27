"""Unit tests for JsonSerializer utility."""
import json
import tempfile
from pathlib import Path

import pytest

from utils import JsonSerializer


class TestJsonSerializer:
    """Test JsonSerializer class."""

    def test_serialize_valid_data(self):
        """Test serialization with valid data."""
        data = {"key": "value", "number": 42, "nested": {"a": 1}}
        result = JsonSerializer.serialize(data)

        assert isinstance(result, str)
        assert "key" in result
        assert "value" in result
        assert json.loads(result) == data

    def test_serialize_with_indent(self):
        """Test serialization with custom indentation."""
        data = {"key": "value"}
        result = JsonSerializer.serialize(data, indent=4)

        assert "\n" in result  # Should be formatted
        assert json.loads(result) == data

    def test_serialize_compact(self):
        """Test compact serialization (no indent)."""
        data = {"key": "value"}
        result = JsonSerializer.serialize(data, indent=None)

        assert "\n" not in result  # Should be compact
        assert json.loads(result) == data

    def test_serialize_invalid_data(self):
        """Test serialization with non-serializable data."""
        invalid_data = {"key": object()}  # object() is not JSON serializable

        with pytest.raises(ValueError, match="Failed to serialize object to JSON"):
            JsonSerializer.serialize(invalid_data)

    def test_deserialize_valid_json(self):
        """Test deserialization with valid JSON."""
        json_str = '{"key": "value", "number": 42}'
        result = JsonSerializer.deserialize(json_str)

        assert isinstance(result, dict)
        assert result["key"] == "value"
        assert result["number"] == 42

    def test_deserialize_invalid_json(self):
        """Test deserialization with invalid JSON."""
        invalid_json = '{"key": invalid}'

        with pytest.raises(ValueError, match="Failed to parse JSON"):
            JsonSerializer.deserialize(invalid_json)

    def test_safe_load_file_exists(self):
        """Test safe_load_file with existing file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            data = {"test": "data"}
            json.dump(data, f)
            temp_path = Path(f.name)

        try:
            result = JsonSerializer.safe_load_file(temp_path)
            assert result == data
        finally:
            temp_path.unlink()

    def test_safe_load_file_missing(self):
        """Test safe_load_file with missing file."""
        missing_path = Path("/tmp/nonexistent_file_12345.json")
        result = JsonSerializer.safe_load_file(missing_path)

        assert result == {}

    def test_safe_load_file_corrupted(self, capsys):
        """Test safe_load_file with corrupted JSON."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"invalid": json}')
            temp_path = Path(f.name)

        try:
            result = JsonSerializer.safe_load_file(temp_path)
            assert result == {}

            # Check warning was printed
            captured = capsys.readouterr()
            assert "Warning" in captured.out
            assert "Failed to load JSON" in captured.out
        finally:
            temp_path.unlink()

    def test_safe_save_file_success(self):
        """Test safe_save_file with successful write."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_path = Path(tmpdir) / "test.json"
            data = {"key": "value", "number": 42}

            result = JsonSerializer.safe_save_file(temp_path, data)

            assert result is True
            assert temp_path.exists()
            loaded_data = json.loads(temp_path.read_text())
            assert loaded_data == data

    def test_safe_save_file_failure(self, capsys):
        """Test safe_save_file with write failure."""
        # Try to write to an invalid path
        invalid_path = Path("/invalid/path/that/does/not/exist/test.json")
        data = {"key": "value"}

        result = JsonSerializer.safe_save_file(invalid_path, data)

        assert result is False
        captured = capsys.readouterr()
        assert "Warning" in captured.out
        assert "Failed to save JSON" in captured.out

    def test_safe_save_file_creates_parent_dir(self):
        """Test that safe_save_file creates parent directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            nested_path = Path(tmpdir) / "nested" / "dir" / "test.json"
            data = {"key": "value"}

            result = JsonSerializer.safe_save_file(nested_path, data)

            assert result is True
            assert nested_path.exists()
            loaded_data = json.loads(nested_path.read_text())
            assert loaded_data == data
