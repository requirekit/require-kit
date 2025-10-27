"""High-level metrics tracking API for plan review system."""
from datetime import datetime
from typing import Dict, Any, Optional, Literal

from .metrics_storage import MetricsStorage
from config import PlanReviewConfig


class PlanReviewMetrics:
    """
    High-level API for tracking plan review metrics.

    Handles metric collection with automatic configuration checking.
    """

    def __init__(self, storage: Optional[MetricsStorage] = None, config: Optional[PlanReviewConfig] = None):
        """
        Initialize metrics tracker.

        Args:
            storage: Metrics storage instance (default: creates new)
            config: Configuration instance (default: singleton)
        """
        self.storage = storage or MetricsStorage()
        self.config = config or PlanReviewConfig()

    def track_complexity(
        self,
        task_id: str,
        complexity_score: int,
        factors: Dict[str, Any],
        stack: Optional[str] = None
    ) -> bool:
        """
        Track complexity calculation.

        Args:
            task_id: Task identifier
            complexity_score: Calculated complexity score
            factors: Complexity factors breakdown
            stack: Technology stack

        Returns:
            True if tracked successfully
        """
        if not self.config.is_metrics_enabled():
            return False

        metric = {
            'type': 'complexity',
            'task_id': task_id,
            'complexity_score': complexity_score,
            'factors': factors,
            'stack': stack,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }

        return self.storage.append_metric(metric)

    def track_decision(
        self,
        task_id: str,
        architectural_score: int,
        decision: Literal['auto_approve', 'approve_with_recommendations', 'reject'],
        complexity_score: int,
        stack: Optional[str] = None,
        forced: bool = False,
        recommendations: Optional[list] = None
    ) -> bool:
        """
        Track architectural review decision.

        Args:
            task_id: Task identifier
            architectural_score: Architectural review score (0-100)
            decision: Review decision
            complexity_score: Complexity score
            stack: Technology stack
            forced: Whether review was forced
            recommendations: List of recommendations

        Returns:
            True if tracked successfully
        """
        if not self.config.is_metrics_enabled():
            return False

        metric = {
            'type': 'decision',
            'task_id': task_id,
            'architectural_score': architectural_score,
            'decision': decision,
            'complexity_score': complexity_score,
            'stack': stack,
            'forced': forced,
            'recommendations': recommendations or [],
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }

        return self.storage.append_metric(metric)

    def track_outcome(
        self,
        task_id: str,
        decision: str,
        human_override: bool,
        duration_seconds: float,
        final_status: Literal['approved', 'rejected', 'timeout'],
        stack: Optional[str] = None
    ) -> bool:
        """
        Track final outcome of review process.

        Args:
            task_id: Task identifier
            decision: Initial decision
            human_override: Whether human overrode decision
            duration_seconds: Total review duration
            final_status: Final outcome status
            stack: Technology stack

        Returns:
            True if tracked successfully
        """
        if not self.config.is_metrics_enabled():
            return False

        metric = {
            'type': 'outcome',
            'task_id': task_id,
            'decision': decision,
            'human_override': human_override,
            'duration_seconds': duration_seconds,
            'final_status': final_status,
            'stack': stack,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }

        return self.storage.append_metric(metric)

    def track_threshold_adjustment(
        self,
        old_threshold: int,
        new_threshold: int,
        threshold_type: Literal['auto_approve', 'approve_with_recommendations'],
        reason: str,
        stack: Optional[str] = None
    ) -> bool:
        """
        Track threshold configuration changes.

        Args:
            old_threshold: Previous threshold value
            new_threshold: New threshold value
            threshold_type: Type of threshold adjusted
            reason: Reason for adjustment
            stack: Technology stack (None for global)

        Returns:
            True if tracked successfully
        """
        if not self.config.is_metrics_enabled():
            return False

        metric = {
            'type': 'threshold_adjustment',
            'old_threshold': old_threshold,
            'new_threshold': new_threshold,
            'threshold_type': threshold_type,
            'reason': reason,
            'stack': stack,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }

        return self.storage.append_metric(metric)

    def get_recent_metrics(self, days: int = 30) -> list:
        """
        Get recent metrics.

        Args:
            days: Number of days to look back

        Returns:
            List of recent metrics
        """
        return self.storage.read_recent_metrics(days)

    def cleanup_old_metrics(self) -> int:
        """
        Clean up metrics older than retention period.

        Returns:
            Number of metrics removed
        """
        retention_days = self.config.get_metrics_retention_days()
        return self.storage.clear_old_metrics(retention_days)
