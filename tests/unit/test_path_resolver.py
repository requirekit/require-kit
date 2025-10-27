"""Unit tests for PathResolver utility."""
import os
import tempfile
from pathlib import Path

import pytest

from utils import PathResolver


class TestPathResolver:
    """Test PathResolver class."""

    def test_resolve_project_root_with_git(self):
        """Test resolve_project_root finds .git directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            git_dir = root / ".git"
            git_dir.mkdir()

            # Create nested directory
            nested = root / "a" / "b" / "c"
            nested.mkdir(parents=True)

            # Change to nested directory
            original_cwd = os.getcwd()
            try:
                os.chdir(nested)
                result = PathResolver.resolve_project_root()
                assert result.resolve() == root.resolve()
            finally:
                os.chdir(original_cwd)

    def test_resolve_project_root_without_git(self):
        """Test resolve_project_root falls back to current directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # No .git directory
            test_dir = (Path(tmpdir) / "test").resolve()
            test_dir.mkdir()

            original_cwd = os.getcwd()
            try:
                os.chdir(test_dir)
                result = PathResolver.resolve_project_root()
                assert result.resolve() == test_dir.resolve()
            finally:
                os.chdir(original_cwd)

    def test_resolve_project_root_from_various_depths(self):
        """Test resolve_project_root from different directory depths."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            git_dir = root / ".git"
            git_dir.mkdir()

            # Test from various depths
            depths = [
                root,
                root / "a",
                root / "a" / "b",
                root / "a" / "b" / "c" / "d"
            ]

            original_cwd = os.getcwd()
            try:
                for depth_dir in depths:
                    depth_dir.mkdir(parents=True, exist_ok=True)
                    os.chdir(depth_dir)
                    result = PathResolver.resolve_project_root()
                    assert result.resolve() == root.resolve(), f"Failed from depth: {depth_dir}"
            finally:
                os.chdir(original_cwd)

    def test_get_settings_path(self):
        """Test get_settings_path returns correct path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            git_dir = root / ".git"
            git_dir.mkdir()

            original_cwd = os.getcwd()
            try:
                os.chdir(root)
                result = PathResolver.get_settings_path()
                expected = root / ".claude" / "settings.json"
                assert result.resolve() == expected.resolve()
            finally:
                os.chdir(original_cwd)

    def test_get_settings_path_from_nested(self):
        """Test get_settings_path from nested directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            git_dir = root / ".git"
            git_dir.mkdir()

            nested = root / "a" / "b" / "c"
            nested.mkdir(parents=True)

            original_cwd = os.getcwd()
            try:
                os.chdir(nested)
                result = PathResolver.get_settings_path()
                expected = root / ".claude" / "settings.json"
                assert result.resolve() == expected.resolve()
            finally:
                os.chdir(original_cwd)

    def test_get_metrics_dir(self):
        """Test get_metrics_dir returns correct path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            git_dir = root / ".git"
            git_dir.mkdir()

            original_cwd = os.getcwd()
            try:
                os.chdir(root)
                result = PathResolver.get_metrics_dir()
                expected = root / "docs" / "state" / "metrics"
                assert result.resolve() == expected.resolve()
            finally:
                os.chdir(original_cwd)

    def test_get_metrics_dir_from_nested(self):
        """Test get_metrics_dir from nested directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            git_dir = root / ".git"
            git_dir.mkdir()

            nested = root / "src" / "lib"
            nested.mkdir(parents=True)

            original_cwd = os.getcwd()
            try:
                os.chdir(nested)
                result = PathResolver.get_metrics_dir()
                expected = root / "docs" / "state" / "metrics"
                assert result.resolve() == expected.resolve()
            finally:
                os.chdir(original_cwd)

    def test_get_metrics_file_default(self):
        """Test get_metrics_file with default filename."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            git_dir = root / ".git"
            git_dir.mkdir()

            original_cwd = os.getcwd()
            try:
                os.chdir(root)
                result = PathResolver.get_metrics_file()
                expected = root / "docs" / "state" / "metrics" / "plan_review_metrics.jsonl"
                assert result.resolve() == expected.resolve()
            finally:
                os.chdir(original_cwd)

    def test_get_metrics_file_custom_filename(self):
        """Test get_metrics_file with custom filename."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir).resolve()
            git_dir = root / ".git"
            git_dir.mkdir()

            original_cwd = os.getcwd()
            try:
                os.chdir(root)
                result = PathResolver.get_metrics_file("custom_metrics.jsonl")
                expected = root / "docs" / "state" / "metrics" / "custom_metrics.jsonl"
                assert result.resolve() == expected.resolve()
            finally:
                os.chdir(original_cwd)

    def test_from_env_or_default_with_env_set(self):
        """Test from_env_or_default with environment variable set."""
        env_var = "TEST_PATH_VAR"
        test_path = "/test/path"

        original_value = os.getenv(env_var)
        try:
            os.environ[env_var] = test_path
            result = PathResolver.from_env_or_default(env_var, Path("/default/path"))
            assert result == Path(test_path)
        finally:
            if original_value is None:
                os.environ.pop(env_var, None)
            else:
                os.environ[env_var] = original_value

    def test_from_env_or_default_without_env(self):
        """Test from_env_or_default without environment variable."""
        env_var = "NONEXISTENT_VAR_12345"
        default_path = Path("/default/path")

        # Ensure env var doesn't exist
        os.environ.pop(env_var, None)

        result = PathResolver.from_env_or_default(env_var, default_path)
        assert result == default_path

    def test_from_env_or_default_with_empty_env(self):
        """Test from_env_or_default with empty environment variable."""
        env_var = "TEST_EMPTY_VAR"
        default_path = Path("/default/path")

        original_value = os.getenv(env_var)
        try:
            os.environ[env_var] = ""
            result = PathResolver.from_env_or_default(env_var, default_path)
            # Empty string is falsy, should use default
            assert result == default_path
        finally:
            if original_value is None:
                os.environ.pop(env_var, None)
            else:
                os.environ[env_var] = original_value
