"""Unit tests for PlanReviewConfig."""
import os
import tempfile
from pathlib import Path

import pytest

from config import PlanReviewConfig, DEFAULT_CONFIG
from utils import JsonSerializer


@pytest.fixture
def clean_config():
    """Clean config singleton between tests."""
    # Reset singleton
    PlanReviewConfig._instance = None
    PlanReviewConfig._config = None
    PlanReviewConfig._cli_overrides = {}
    yield
    # Clean up after test
    PlanReviewConfig._instance = None
    PlanReviewConfig._config = None
    PlanReviewConfig._cli_overrides = {}


@pytest.fixture
def temp_project(clean_config):
    """Create temporary project structure."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        git_dir = root / ".git"
        git_dir.mkdir()

        claude_dir = root / ".claude"
        claude_dir.mkdir()

        original_cwd = os.getcwd()
        try:
            os.chdir(root)
            yield root
        finally:
            os.chdir(original_cwd)


class TestPlanReviewConfig:
    """Test PlanReviewConfig class."""

    def test_singleton_instance(self, clean_config):
        """Test that PlanReviewConfig is a singleton."""
        config1 = PlanReviewConfig()
        config2 = PlanReviewConfig()

        assert config1 is config2

    def test_default_configuration(self, temp_project):
        """Test configuration with defaults only."""
        config = PlanReviewConfig()

        assert config.is_enabled() is True
        assert config.get_mode() == "auto"
        assert config.is_metrics_enabled() is True

    def test_load_from_settings_file(self, temp_project):
        """Test loading configuration from settings.json."""
        settings_path = temp_project / ".claude" / "settings.json"
        settings_data = {
            "plan_review": {
                "enabled": False,
                "default_mode": "always",
                "metrics": {
                    "enabled": False
                }
            }
        }
        JsonSerializer.safe_save_file(settings_path, settings_data)

        config = PlanReviewConfig()

        assert config.is_enabled() is False
        assert config.get_mode() == "always"
        assert config.is_metrics_enabled() is False

    def test_environment_variable_overrides(self, temp_project):
        """Test environment variable overrides."""
        original_env = {}
        env_vars = {
            'PLAN_REVIEW_ENABLED': 'false',
            'PLAN_REVIEW_MODE': 'never',
            'PLAN_REVIEW_METRICS_ENABLED': 'false'
        }

        try:
            # Set environment variables
            for key, value in env_vars.items():
                original_env[key] = os.getenv(key)
                os.environ[key] = value

            # Force reload
            PlanReviewConfig._instance = None
            PlanReviewConfig._config = None
            config = PlanReviewConfig()

            assert config.is_enabled() is False
            assert config.get_mode() == "never"
            assert config.is_metrics_enabled() is False

        finally:
            # Restore original environment
            for key, value in original_env.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

    def test_cli_overrides_highest_priority(self, temp_project):
        """Test that CLI overrides have highest priority."""
        # Set settings file
        settings_path = temp_project / ".claude" / "settings.json"
        settings_data = {
            "plan_review": {
                "enabled": True,
                "default_mode": "auto"
            }
        }
        JsonSerializer.safe_save_file(settings_path, settings_data)

        config = PlanReviewConfig()

        # CLI override should take precedence
        config.set_cli_override('enabled', False)
        config.set_cli_override('default_mode', 'never')

        assert config.is_enabled() is False
        assert config.get_mode() == "never"

    def test_get_threshold_auto_approve(self, temp_project):
        """Test get_threshold for auto-approve scores."""
        config = PlanReviewConfig()

        decision = config.get_threshold(85)
        assert decision == "auto_approve"

    def test_get_threshold_approve_with_recommendations(self, temp_project):
        """Test get_threshold for approve with recommendations."""
        config = PlanReviewConfig()

        decision = config.get_threshold(70)
        assert decision == "approve_with_recommendations"

    def test_get_threshold_reject(self, temp_project):
        """Test get_threshold for rejection."""
        config = PlanReviewConfig()

        decision = config.get_threshold(50)
        assert decision == "reject"

    def test_get_threshold_with_stack_override(self, temp_project):
        """Test get_threshold with stack-specific overrides."""
        settings_path = temp_project / ".claude" / "settings.json"
        settings_data = {
            "plan_review": {
                "thresholds": {
                    "default": {
                        "auto_approve": 80,
                        "approve_with_recommendations": 60,
                        "reject": 0
                    },
                    "stack_overrides": {
                        "python": {
                            "auto_approve": 90,
                            "approve_with_recommendations": 70,
                            "reject": 0
                        }
                    }
                }
            }
        }
        JsonSerializer.safe_save_file(settings_path, settings_data)

        config = PlanReviewConfig()

        # Default stack
        assert config.get_threshold(85) == "auto_approve"

        # Python stack (higher threshold)
        assert config.get_threshold(85, stack="python") == "approve_with_recommendations"
        assert config.get_threshold(92, stack="python") == "auto_approve"

    def test_should_force_review_complexity(self, temp_project):
        """Test should_force_review based on complexity."""
        config = PlanReviewConfig()

        # Below threshold
        assert config.should_force_review(20) is False

        # At or above threshold (default is 30)
        assert config.should_force_review(30) is True
        assert config.should_force_review(50) is True

    def test_should_force_review_keywords(self, temp_project):
        """Test should_force_review based on keywords."""
        config = PlanReviewConfig()

        # No keywords
        assert config.should_force_review(10, keywords=[]) is False

        # Non-critical keywords
        assert config.should_force_review(10, keywords=["feature", "update"]) is False

        # Critical keywords
        assert config.should_force_review(10, keywords=["security"]) is True
        assert config.should_force_review(10, keywords=["authentication"]) is True
        assert config.should_force_review(10, keywords=["payment", "other"]) is True

    def test_get_timeout_architectural_review(self, temp_project):
        """Test get_timeout for architectural review stage."""
        config = PlanReviewConfig()

        timeout = config.get_timeout("architectural_review")
        assert timeout == 300  # Default 5 minutes

    def test_get_timeout_human_checkpoint(self, temp_project):
        """Test get_timeout for human checkpoint stage."""
        config = PlanReviewConfig()

        timeout = config.get_timeout("human_checkpoint")
        assert timeout == 1800  # Default 30 minutes

    def test_get_timeout_invalid_stage(self, temp_project):
        """Test get_timeout with invalid stage raises error."""
        config = PlanReviewConfig()

        with pytest.raises(ValueError, match="Unknown stage"):
            config.get_timeout("invalid_stage")

    def test_get_weights(self, temp_project):
        """Test get_weights returns correct values."""
        config = PlanReviewConfig()

        weights = config.get_weights()

        assert weights['solid_principles'] == 0.30
        assert weights['dry_principle'] == 0.25
        assert weights['yagni_principle'] == 0.25
        assert weights['testability'] == 0.20

        # Verify they sum to 1.0
        assert abs(sum(weights.values()) - 1.0) < 0.01

    def test_get_metrics_retention_days(self, temp_project):
        """Test get_metrics_retention_days."""
        config = PlanReviewConfig()

        retention = config.get_metrics_retention_days()
        assert retention == 90  # Default

    def test_get_metrics_output_format(self, temp_project):
        """Test get_metrics_output_format."""
        config = PlanReviewConfig()

        format = config.get_metrics_output_format()
        assert format == "terminal"

    def test_reload_configuration(self, temp_project):
        """Test reload() reloads configuration."""
        settings_path = temp_project / ".claude" / "settings.json"

        # Initial config
        config = PlanReviewConfig()
        assert config.is_enabled() is True

        # Update settings file
        settings_data = {
            "plan_review": {
                "enabled": False
            }
        }
        JsonSerializer.safe_save_file(settings_path, settings_data)

        # Reload
        config.reload()

        assert config.is_enabled() is False

    def test_reload_clears_cli_overrides(self, temp_project):
        """Test reload() clears CLI overrides."""
        config = PlanReviewConfig()

        config.set_cli_override('enabled', False)
        assert config.is_enabled() is False

        config.reload()

        # CLI override should be cleared
        assert config.is_enabled() is True  # Back to default

    def test_get_raw_config(self, temp_project):
        """Test get_raw_config returns configuration dictionary."""
        config = PlanReviewConfig()

        raw_config = config.get_raw_config()

        assert isinstance(raw_config, dict)
        assert 'enabled' in raw_config
        assert 'default_mode' in raw_config
        assert 'thresholds' in raw_config
        assert 'metrics' in raw_config

    def test_graceful_degradation_on_invalid_config(self, temp_project, capsys):
        """Test graceful degradation with invalid configuration."""
        settings_path = temp_project / ".claude" / "settings.json"
        settings_data = {
            "plan_review": {
                "enabled": "not_a_boolean",  # Invalid
                "thresholds": {
                    "default": {
                        "auto_approve": 150,  # Invalid (> 100)
                        "approve_with_recommendations": 60,
                        "reject": 0
                    }
                }
            }
        }
        JsonSerializer.safe_save_file(settings_path, settings_data)

        config = PlanReviewConfig()

        # Should fall back to defaults
        captured = capsys.readouterr()
        assert "Warning" in captured.out
        assert "Invalid configuration" in captured.out

        # Verify defaults are used
        assert config.is_enabled() is True  # Default value

    def test_env_auto_approve_threshold_override(self, temp_project):
        """Test PLAN_REVIEW_AUTO_APPROVE_THRESHOLD environment variable."""
        original_env = os.getenv('PLAN_REVIEW_AUTO_APPROVE_THRESHOLD')

        try:
            os.environ['PLAN_REVIEW_AUTO_APPROVE_THRESHOLD'] = '90'

            # Force reload
            PlanReviewConfig._instance = None
            PlanReviewConfig._config = None
            config = PlanReviewConfig()

            # Score below 90 but above default 80
            decision = config.get_threshold(85)
            assert decision == "approve_with_recommendations"  # Not auto-approved

            # Score at or above 90
            decision = config.get_threshold(90)
            assert decision == "auto_approve"

        finally:
            if original_env is None:
                os.environ.pop('PLAN_REVIEW_AUTO_APPROVE_THRESHOLD', None)
            else:
                os.environ['PLAN_REVIEW_AUTO_APPROVE_THRESHOLD'] = original_env

    def test_merge_configs_deep_merge(self, temp_project):
        """Test _merge_configs performs deep merge."""
        config = PlanReviewConfig()

        base = {
            "enabled": True,
            "thresholds": {
                "default": {
                    "auto_approve": 80
                }
            }
        }

        override = {
            "thresholds": {
                "default": {
                    "approve_with_recommendations": 60
                }
            }
        }

        result = config._merge_configs(base, override)

        # Should preserve enabled from base
        assert result["enabled"] is True
        # Should have both auto_approve and approve_with_recommendations
        assert result["thresholds"]["default"]["auto_approve"] == 80
        assert result["thresholds"]["default"]["approve_with_recommendations"] == 60
