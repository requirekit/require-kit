"""Plan review configuration manager with 4-layer precedence."""
import os
from typing import Optional, Dict, Any, Literal
from pathlib import Path

from .defaults import DEFAULT_CONFIG
from .config_schema import ConfigSchema, ThresholdConfig
from ..utils import JsonSerializer, PathResolver


class PlanReviewConfig:
    """
    Singleton configuration manager for plan review system.

    Implements 4-layer precedence:
    1. CLI arguments (highest priority)
    2. Environment variables
    3. Settings.json file
    4. Default configuration (lowest priority)
    """

    _instance: Optional['PlanReviewConfig'] = None
    _config: Optional[ConfigSchema] = None
    _cli_overrides: Dict[str, Any] = {}

    def __new__(cls) -> 'PlanReviewConfig':
        """Ensure singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize configuration (only once)."""
        if self._config is None:
            self._load_config()

    def _load_config(self) -> None:
        """Load configuration from all sources with precedence."""
        # Start with defaults
        config_dict = DEFAULT_CONFIG.copy()

        # Layer 3: Settings.json
        settings_path = PathResolver.get_settings_path()
        if settings_path.exists():
            settings = JsonSerializer.safe_load_file(settings_path)
            plan_review_settings = settings.get('plan_review', {})
            if plan_review_settings:
                config_dict = self._merge_configs(config_dict, plan_review_settings)

        # Layer 2: Environment variables
        env_overrides = self._load_env_overrides()
        if env_overrides:
            config_dict = self._merge_configs(config_dict, env_overrides)

        # Layer 1: CLI overrides (applied in get methods)
        # These are set via set_cli_override() method

        # Validate and create schema
        try:
            self._config = ConfigSchema(**config_dict)
        except Exception as e:
            print(f"Warning: Invalid configuration, using defaults: {e}")
            self._config = ConfigSchema(**DEFAULT_CONFIG)

    def _load_env_overrides(self) -> Dict[str, Any]:
        """
        Load configuration overrides from environment variables.

        Returns:
            Dictionary of environment variable overrides
        """
        overrides = {}

        # PLAN_REVIEW_ENABLED
        if 'PLAN_REVIEW_ENABLED' in os.environ:
            value = os.getenv('PLAN_REVIEW_ENABLED', '').lower()
            overrides['enabled'] = value in ('true', '1', 'yes')

        # PLAN_REVIEW_MODE
        if 'PLAN_REVIEW_MODE' in os.environ:
            mode = os.getenv('PLAN_REVIEW_MODE', '')
            if mode in ('auto', 'always', 'never'):
                overrides['default_mode'] = mode

        # PLAN_REVIEW_AUTO_APPROVE_THRESHOLD
        if 'PLAN_REVIEW_AUTO_APPROVE_THRESHOLD' in os.environ:
            try:
                threshold = int(os.getenv('PLAN_REVIEW_AUTO_APPROVE_THRESHOLD', ''))
                if 'thresholds' not in overrides:
                    overrides['thresholds'] = {'default': {}}
                overrides['thresholds']['default']['auto_approve'] = threshold
            except ValueError:
                pass

        # PLAN_REVIEW_METRICS_ENABLED
        if 'PLAN_REVIEW_METRICS_ENABLED' in os.environ:
            value = os.getenv('PLAN_REVIEW_METRICS_ENABLED', '').lower()
            if 'metrics' not in overrides:
                overrides['metrics'] = {}
            overrides['metrics']['enabled'] = value in ('true', '1', 'yes')

        return overrides

    def _merge_configs(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively merge configuration dictionaries.

        Args:
            base: Base configuration
            override: Override configuration

        Returns:
            Merged configuration
        """
        result = base.copy()

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value

        return result

    def set_cli_override(self, key: str, value: Any) -> None:
        """
        Set CLI override value (highest precedence).

        Args:
            key: Configuration key (dot notation supported, e.g., 'thresholds.default.auto_approve')
            value: Override value
        """
        self._cli_overrides[key] = value

    def _get_cli_override(self, key: str) -> Optional[Any]:
        """
        Get CLI override value if set.

        Args:
            key: Configuration key

        Returns:
            Override value or None
        """
        return self._cli_overrides.get(key)

    def is_enabled(self) -> bool:
        """
        Check if plan review system is enabled.

        Returns:
            True if enabled
        """
        cli_override = self._get_cli_override('enabled')
        if cli_override is not None:
            return bool(cli_override)
        return self._config.enabled

    def get_mode(self) -> Literal["auto", "always", "never"]:
        """
        Get default review mode.

        Returns:
            Review mode
        """
        cli_override = self._get_cli_override('default_mode')
        if cli_override is not None:
            return cli_override
        return self._config.default_mode

    def get_threshold(self, score: int, stack: Optional[str] = None) -> str:
        """
        Get decision threshold for score.

        Args:
            score: Architectural review score (0-100)
            stack: Technology stack identifier

        Returns:
            Decision: 'auto_approve', 'approve_with_recommendations', or 'reject'
        """
        # Check for CLI overrides
        cli_auto = self._get_cli_override('thresholds.auto_approve')
        cli_recommend = self._get_cli_override('thresholds.approve_with_recommendations')

        # Get thresholds for stack
        thresholds = self._config.thresholds.get_for_stack(stack)

        auto_approve = cli_auto if cli_auto is not None else thresholds.auto_approve
        approve_with_rec = cli_recommend if cli_recommend is not None else thresholds.approve_with_recommendations

        if score >= auto_approve:
            return 'auto_approve'
        elif score >= approve_with_rec:
            return 'approve_with_recommendations'
        else:
            return 'reject'

    def should_force_review(self, complexity: int, keywords: Optional[list] = None) -> bool:
        """
        Check if architectural review should be forced.

        Args:
            complexity: Complexity score
            keywords: List of keywords in task description

        Returns:
            True if review should be forced
        """
        # Check complexity threshold
        if complexity >= self._config.force_triggers.min_complexity:
            return True

        # Check critical keywords
        if keywords:
            keywords_lower = [k.lower() for k in keywords]
            for critical in self._config.force_triggers.critical_keywords:
                if critical.lower() in keywords_lower:
                    return True

        return False

    def get_timeout(self, stage: Literal["architectural_review", "human_checkpoint"]) -> int:
        """
        Get timeout for stage.

        Args:
            stage: Stage identifier

        Returns:
            Timeout in seconds
        """
        if stage == "architectural_review":
            return self._config.timeouts.architectural_review_seconds
        elif stage == "human_checkpoint":
            return self._config.timeouts.human_checkpoint_seconds
        else:
            raise ValueError(f"Unknown stage: {stage}")

    def get_weights(self) -> Dict[str, float]:
        """
        Get scoring weights.

        Returns:
            Dictionary of weights
        """
        return {
            'solid_principles': self._config.weights.solid_principles,
            'dry_principle': self._config.weights.dry_principle,
            'yagni_principle': self._config.weights.yagni_principle,
            'testability': self._config.weights.testability
        }

    def is_metrics_enabled(self) -> bool:
        """
        Check if metrics collection is enabled.

        Returns:
            True if enabled
        """
        cli_override = self._get_cli_override('metrics.enabled')
        if cli_override is not None:
            return bool(cli_override)
        return self._config.metrics.enabled

    def get_metrics_retention_days(self) -> int:
        """
        Get metrics retention period.

        Returns:
            Retention period in days
        """
        return self._config.metrics.retention_days

    def get_metrics_output_format(self) -> str:
        """
        Get metrics output format.

        Returns:
            Output format (terminal only for MVP)
        """
        return self._config.metrics.output_format

    def reload(self) -> None:
        """Reload configuration from all sources."""
        self._config = None
        self._cli_overrides = {}
        self._load_config()

    def get_raw_config(self) -> Dict[str, Any]:
        """
        Get raw configuration as dictionary.

        Returns:
            Configuration dictionary
        """
        return self._config.model_dump()
