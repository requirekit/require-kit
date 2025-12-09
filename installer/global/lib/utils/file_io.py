"""
Shared file I/O utilities with consistent error handling.

Provides safe_read_file() and safe_write_file() functions that handle
common file I/O errors consistently across all commands.

Usage:
    from utils.file_io import safe_read_file, safe_write_file

    # Reading
    success, content = safe_read_file(path)
    if not success:
        logger.error(f"Failed to read: {content}")  # content is error msg
        return

    # Writing
    success, error_msg = safe_write_file(path, content)
    if not success:
        logger.error(f"Failed to write: {error_msg}")
        return
"""

from pathlib import Path
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


def safe_read_file(
    file_path: Path,
    encoding: str = 'utf-8'
) -> Tuple[bool, str]:
    """
    Safely read file with comprehensive error handling.

    Args:
        file_path: Path to file
        encoding: Text encoding (default: utf-8)

    Returns:
        Tuple of (success: bool, content_or_error: str)
        - On success: (True, file_content)
        - On failure: (False, error_message)

    Errors Handled:
        - FileNotFoundError: File doesn't exist
        - PermissionError: No read permission
        - UnicodeDecodeError: Encoding issues
        - OSError: I/O errors (disk, network, etc.)
    """
    try:
        content = file_path.read_text(encoding=encoding)
        return (True, content)

    except FileNotFoundError:
        error_msg = f"File not found: {file_path}"
        logger.error(error_msg)
        return (False, error_msg)

    except PermissionError:
        error_msg = f"Permission denied reading {file_path}"
        logger.error(error_msg)
        return (False, error_msg)

    except UnicodeDecodeError as e:
        error_msg = f"Encoding error in {file_path}: {e}"
        logger.error(error_msg)
        return (False, error_msg)

    except OSError as e:
        error_msg = f"I/O error reading {file_path}: {e}"
        logger.error(error_msg)
        return (False, error_msg)

    except Exception as e:
        error_msg = f"Unexpected error reading {file_path}: {e}"
        logger.error(error_msg)
        return (False, error_msg)


def safe_write_file(
    file_path: Path,
    content: str,
    encoding: str = 'utf-8'
) -> Tuple[bool, Optional[str]]:
    """
    Safely write file with comprehensive error handling.

    Args:
        file_path: Path to file
        content: Content to write
        encoding: Text encoding (default: utf-8)

    Returns:
        Tuple of (success: bool, error_message: Optional[str])
        - On success: (True, None)
        - On failure: (False, error_message)

    Errors Handled:
        - PermissionError: No write permission
        - OSError (ENOSPC): Disk full
        - OSError (ENAMETOOLONG): Path too long
        - UnicodeEncodeError: Encoding issues
        - OSError: Other I/O errors
    """
    try:
        file_path.write_text(content, encoding=encoding)
        return (True, None)

    except PermissionError:
        error_msg = f"Permission denied writing to {file_path}"
        logger.error(error_msg)
        return (False, error_msg)

    except UnicodeEncodeError as e:
        error_msg = f"Encoding error writing {file_path}: {e}"
        logger.error(error_msg)
        return (False, error_msg)

    except OSError as e:
        # Disk full, path too long, etc.
        error_msg = f"I/O error writing {file_path}: {e}"
        logger.error(error_msg)
        return (False, error_msg)

    except Exception as e:
        error_msg = f"Unexpected error writing {file_path}: {e}"
        logger.error(error_msg)
        return (False, error_msg)
