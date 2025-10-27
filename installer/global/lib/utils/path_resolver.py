"""Path resolution utilities for configuration and metrics."""
import os
from pathlib import Path
from typing import Optional


class PathResolver:
    """Resolves paths for settings and metrics consistently."""

    @staticmethod
    def resolve_project_root() -> Path:
        """
        Resolve project root directory.

        Returns:
            Path to project root

        Note:
            Looks for .git directory or uses current working directory
        """
        current = Path.cwd()

        # Walk up looking for .git directory
        for parent in [current] + list(current.parents):
            if (parent / '.git').exists():
                return parent

        # Fallback to current directory
        return current

    @staticmethod
    def get_settings_path() -> Path:
        """
        Get path to settings.json file.

        Returns:
            Path to .claude/settings.json
        """
        root = PathResolver.resolve_project_root()
        return root / '.claude' / 'settings.json'

    @staticmethod
    def get_metrics_dir() -> Path:
        """
        Get path to metrics directory.

        Returns:
            Path to docs/state/metrics/
        """
        root = PathResolver.resolve_project_root()
        return root / 'docs' / 'state' / 'metrics'

    @staticmethod
    def get_metrics_file(filename: str = 'plan_review_metrics.jsonl') -> Path:
        """
        Get path to metrics file.

        Args:
            filename: Metrics filename (default: plan_review_metrics.jsonl)

        Returns:
            Full path to metrics file
        """
        return PathResolver.get_metrics_dir() / filename

    @staticmethod
    def from_env_or_default(env_var: str, default: Path) -> Path:
        """
        Get path from environment variable or use default.

        Args:
            env_var: Environment variable name
            default: Default path if env var not set

        Returns:
            Path from environment or default
        """
        env_value = os.getenv(env_var)
        if env_value:
            return Path(env_value)
        return default
