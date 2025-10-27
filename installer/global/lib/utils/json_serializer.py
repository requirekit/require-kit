"""JSON serialization utilities with robust error handling."""
import json
from pathlib import Path
from typing import Any, Dict, Optional


class JsonSerializer:
    """Handles JSON serialization and deserialization with error handling."""

    @staticmethod
    def serialize(obj: Any, indent: Optional[int] = 2) -> str:
        """
        Serialize object to JSON string.

        Args:
            obj: Object to serialize
            indent: Indentation level (None for compact)

        Returns:
            JSON string representation

        Raises:
            ValueError: If object cannot be serialized
        """
        try:
            return json.dumps(obj, indent=indent, ensure_ascii=False)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to serialize object to JSON: {e}") from e

    @staticmethod
    def deserialize(json_str: str) -> Dict[str, Any]:
        """
        Deserialize JSON string to dictionary.

        Args:
            json_str: JSON string to parse

        Returns:
            Parsed dictionary

        Raises:
            ValueError: If JSON is invalid
        """
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON: {e}") from e

    @staticmethod
    def safe_load_file(path: Path) -> Dict[str, Any]:
        """
        Safely load JSON from file with error handling.

        Args:
            path: Path to JSON file

        Returns:
            Parsed dictionary or empty dict on error

        Note:
            Returns empty dict on any error for graceful degradation
        """
        try:
            if not path.exists():
                return {}

            content = path.read_text(encoding='utf-8')
            return JsonSerializer.deserialize(content)
        except Exception as e:
            # Log error but return empty dict for graceful degradation
            print(f"Warning: Failed to load JSON from {path}: {e}")
            return {}

    @staticmethod
    def safe_save_file(path: Path, data: Dict[str, Any], indent: Optional[int] = 2) -> bool:
        """
        Safely save dictionary to JSON file.
        Creates parent directories if they don't exist.

        Args:
            path: Path to save file
            data: Dictionary to save
            indent: Indentation level

        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure parent directory exists
            path.parent.mkdir(parents=True, exist_ok=True)

            json_str = JsonSerializer.serialize(data, indent=indent)
            path.write_text(json_str, encoding='utf-8')
            return True
        except Exception as e:
            print(f"Warning: Failed to save JSON to {path}: {e}")
            return False
