"""Pytest configuration and fixtures."""
import os
import sys
from pathlib import Path

# Add installer/global/lib to Python path
lib_path = Path(__file__).parent.parent / "installer" / "global" / "lib"
sys.path.insert(0, str(lib_path))

# Also add commands/lib for plan_modifier imports
commands_lib_path = Path(__file__).parent.parent / "installer" / "global" / "commands" / "lib"
if str(commands_lib_path) not in sys.path:
    sys.path.insert(0, str(commands_lib_path))


def normalize_path(path):
    """
    Normalize path for cross-platform comparison.

    Uses os.path.realpath() to resolve symlinks (e.g., macOS /private/var).

    Args:
        path: Path-like object to normalize

    Returns:
        Path: Normalized path object
    """
    return Path(os.path.realpath(path))


def paths_equal(path1, path2):
    """
    Compare two paths for equality after normalization.

    Args:
        path1: First path to compare
        path2: Second path to compare

    Returns:
        bool: True if paths are equal after normalization
    """
    return normalize_path(path1) == normalize_path(path2)
