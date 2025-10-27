"""File operations with atomic writes and error handling."""
import os
import tempfile
from pathlib import Path
from typing import Optional


class FileOperations:
    """Provides safe file operations with atomic writes."""

    @staticmethod
    def atomic_write(path: Path, content: str, encoding: str = 'utf-8') -> bool:
        """
        Atomically write content to file using temp file + rename pattern.

        Args:
            path: Destination file path
            content: Content to write
            encoding: Text encoding (default: utf-8)

        Returns:
            True if successful, False otherwise

        Note:
            Uses temp file in same directory to ensure atomic operation
        """
        try:
            # Ensure parent directory exists
            path.parent.mkdir(parents=True, exist_ok=True)

            # Create temp file in same directory as target
            fd, temp_path = tempfile.mkstemp(
                dir=path.parent,
                prefix=f".{path.name}.",
                suffix=".tmp"
            )

            try:
                # Write content to temp file
                with os.fdopen(fd, 'w', encoding=encoding) as f:
                    f.write(content)

                # Atomic rename
                os.replace(temp_path, path)
                return True
            except Exception:
                # Clean up temp file on error
                try:
                    os.unlink(temp_path)
                except Exception:
                    pass
                raise
        except Exception as e:
            print(f"Warning: Atomic write failed for {path}: {e}")
            return False

    @staticmethod
    def safe_read(path: Path, encoding: str = 'utf-8') -> Optional[str]:
        """
        Safely read file content with error handling.

        Args:
            path: File path to read
            encoding: Text encoding (default: utf-8)

        Returns:
            File content or None on error
        """
        try:
            if not path.exists():
                return None
            return path.read_text(encoding=encoding)
        except Exception as e:
            print(f"Warning: Failed to read {path}: {e}")
            return None

    @staticmethod
    def ensure_directory(path: Path) -> bool:
        """
        Ensure directory exists, creating if necessary.

        Args:
            path: Directory path to ensure

        Returns:
            True if directory exists or was created successfully
        """
        try:
            path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"Warning: Failed to create directory {path}: {e}")
            return False

    @staticmethod
    def safe_append(path: Path, content: str, encoding: str = 'utf-8') -> bool:
        """
        Safely append content to file.

        Args:
            path: File path to append to
            content: Content to append
            encoding: Text encoding (default: utf-8)

        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure parent directory exists
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, 'a', encoding=encoding) as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Warning: Failed to append to {path}: {e}")
            return False
