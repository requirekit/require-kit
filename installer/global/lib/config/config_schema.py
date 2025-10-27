"""Pydantic schemas for configuration validation."""
from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, Field, field_validator


class ThresholdConfig(BaseModel):
    """Threshold configuration for score-based decisions."""

    auto_approve: int = Field(ge=0, le=100, description="Auto-approve threshold")
    approve_with_recommendations: int = Field(ge=0, le=100, description="Approve with recommendations threshold")
    reject: int = Field(ge=0, le=100, description="Reject threshold")

    @field_validator('approve_with_recommendations')
    @classmethod
    def validate_threshold_ordering(cls, v: int, info) -> int:
        """Validate that thresholds are in correct order."""
        # During validation, we may not have auto_approve yet
        # This will be validated in the parent model
        return v

    def validate_ordering(self) -> None:
        """Validate threshold ordering after all fields are set."""
        if not (self.auto_approve > self.approve_with_recommendations >= self.reject):
            raise ValueError(
                f"Invalid threshold ordering: auto_approve ({self.auto_approve}) must be > "
                f"approve_with_recommendations ({self.approve_with_recommendations}) must be >= "
                f"reject ({self.reject})"
            )


class ForceTriggers(BaseModel):
    """Configuration for forcing architectural review."""

    min_complexity: int = Field(ge=0, description="Minimum complexity score to force review")
    critical_keywords: List[str] = Field(description="Keywords that trigger forced review")


class Timeouts(BaseModel):
    """Timeout configuration for review stages."""

    architectural_review_seconds: int = Field(gt=0, description="Timeout for architectural review")
    human_checkpoint_seconds: int = Field(gt=0, description="Timeout for human checkpoint")


class Weights(BaseModel):
    """Weights for scoring different aspects."""

    solid_principles: float = Field(ge=0.0, le=1.0, description="Weight for SOLID principles")
    dry_principle: float = Field(ge=0.0, le=1.0, description="Weight for DRY principle")
    yagni_principle: float = Field(ge=0.0, le=1.0, description="Weight for YAGNI principle")
    testability: float = Field(ge=0.0, le=1.0, description="Weight for testability")

    @field_validator('testability')
    @classmethod
    def validate_weights_sum(cls, v: float, info) -> float:
        """Validate that weights sum to 1.0."""
        # Get all field values
        solid = info.data.get('solid_principles', 0.0)
        dry = info.data.get('dry_principle', 0.0)
        yagni = info.data.get('yagni_principle', 0.0)
        testability = v

        total = solid + dry + yagni + testability
        if abs(total - 1.0) > 0.01:  # Allow small floating point errors
            raise ValueError(f"Weights must sum to 1.0, got {total}")

        return v


class MetricsConfig(BaseModel):
    """Metrics collection configuration."""

    enabled: bool = Field(description="Enable metrics collection")
    retention_days: int = Field(gt=0, description="Number of days to retain metrics")
    output_format: Literal["terminal"] = Field(description="Output format (terminal only for MVP)")


class ThresholdsConfig(BaseModel):
    """Thresholds configuration with stack overrides."""

    default: ThresholdConfig = Field(description="Default thresholds")
    stack_overrides: Dict[str, ThresholdConfig] = Field(default_factory=dict, description="Stack-specific overrides")

    def get_for_stack(self, stack: Optional[str] = None) -> ThresholdConfig:
        """
        Get threshold configuration for specific stack.

        Args:
            stack: Technology stack identifier

        Returns:
            ThresholdConfig for stack or default
        """
        if stack and stack in self.stack_overrides:
            return self.stack_overrides[stack]
        return self.default


class ConfigSchema(BaseModel):
    """Complete configuration schema for plan review system."""

    enabled: bool = Field(description="Enable plan review system")
    default_mode: Literal["auto", "always", "never"] = Field(description="Default review mode")
    thresholds: ThresholdsConfig = Field(description="Score thresholds")
    force_triggers: ForceTriggers = Field(description="Forced review triggers")
    timeouts: Timeouts = Field(description="Timeout configuration")
    weights: Weights = Field(description="Scoring weights")
    metrics: MetricsConfig = Field(description="Metrics configuration")

    def model_post_init(self, __context) -> None:
        """Validate after all fields are set."""
        # Validate default thresholds ordering
        self.thresholds.default.validate_ordering()

        # Validate stack override thresholds ordering
        for stack_name, threshold in self.thresholds.stack_overrides.items():
            threshold.validate_ordering()
