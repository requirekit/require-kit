"""
Plan Audit Metrics Tracker - Track audit outcomes for complexity model improvement.

Part of TASK-025: Implement Phase 5.5 Plan Audit.

This module tracks plan audit outcomes to create a feedback loop for:
- Complexity model improvement (better LOC/duration estimates)
- Scope creep pattern detection
- Estimation accuracy refinement

Metrics are stored in docs/state/plan_audit_metrics.json and used to:
1. Calculate average variances (LOC, duration)
2. Identify common scope creep patterns
3. Improve future planning accuracy

Author: Claude (Anthropic)
Created: 2025-10-18
"""

from typing import Dict, Any
from pathlib import Path
from datetime import datetime
import json

try:
    from ..git_state_helper import commit_state_files
except ImportError:
    # If git_state_helper not available (e.g., in tests), provide no-op
    def commit_state_files(task_id: str, message: str = None) -> None:
        pass


class PlanAuditMetricsTracker:
    """Track plan audit outcomes for complexity model improvement."""

    def __init__(self, metrics_file: Path = None):
        """
        Initialize metrics tracker.

        Args:
            metrics_file: Path to metrics JSON file (default: docs/state/plan_audit_metrics.json)
        """
        if metrics_file is None:
            metrics_file = Path("docs/state/plan_audit_metrics.json")

        self.metrics_file = metrics_file
        self._ensure_metrics_file()

    def record_audit(
        self,
        task_id: str,
        report: Any,  # PlanAuditReport (avoid circular import)
        decision: str
    ) -> None:
        """
        Record audit outcome to metrics file.

        Args:
            task_id: Task identifier
            report: PlanAuditReport object
            decision: Human decision ("approve", "revise", "escalate", "cancel")

        Example:
            >>> tracker = PlanAuditMetricsTracker()
            >>> tracker.record_audit("TASK-025", report, "approve")
        """
        metrics = self._load_metrics()

        audit_entry = {
            "task_id": task_id,
            "timestamp": datetime.now().isoformat(),
            "severity": report.severity,
            "discrepancies_count": len(report.discrepancies),
            "decision": decision,
            "loc_variance": self._extract_variance(report, "loc"),
            "duration_variance": self._extract_variance(report, "duration"),
            "extra_files": self._count_discrepancy_type(report, "files", "extra"),
            "extra_dependencies": self._count_discrepancy_type(report, "dependencies", "extra")
        }

        metrics["audits"].append(audit_entry)
        metrics["summary"] = self._calculate_summary(metrics["audits"])

        self._save_metrics(metrics)

    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics of all audits.

        Returns:
            Dictionary with summary statistics

        Example:
            >>> tracker = PlanAuditMetricsTracker()
            >>> summary = tracker.get_summary()
            >>> print(summary["total_audits"])
            45
        """
        metrics = self._load_metrics()
        return metrics.get("summary", {})

    def get_recent_audits(self, count: int = 10) -> list:
        """
        Get most recent audit entries.

        Args:
            count: Number of recent entries to return

        Returns:
            List of audit entries (most recent first)

        Example:
            >>> tracker = PlanAuditMetricsTracker()
            >>> recent = tracker.get_recent_audits(5)
            >>> len(recent)
            5
        """
        metrics = self._load_metrics()
        audits = metrics.get("audits", [])
        return audits[-count:][::-1]  # Last N, reversed

    def _load_metrics(self) -> Dict[str, Any]:
        """Load metrics from disk."""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                # Corrupted file, start fresh
                return {"audits": [], "summary": {}}
        else:
            return {"audits": [], "summary": {}}

    def _save_metrics(self, metrics: Dict[str, Any]) -> None:
        """Save metrics to disk."""
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.metrics_file, 'w', encoding='utf-8') as f:
            json.dump(metrics, f, indent=2)

        # Commit metrics file to git (for Conductor worktree support)
        # Note: metrics file is at docs/state/plan_audit_metrics.json (not task-specific)
        # We use a generic task_id to indicate global metrics
        try:
            commit_state_files("_global", "Update plan audit metrics")
        except Exception:
            # Don't fail save operation if git commit fails
            pass

    def _ensure_metrics_file(self) -> None:
        """Ensure metrics file exists."""
        if not self.metrics_file.exists():
            self._save_metrics({"audits": [], "summary": {}})

    def _extract_variance(self, report: Any, category: str) -> float:
        """
        Extract variance % for specific category.

        Args:
            report: PlanAuditReport
            category: "loc" or "duration"

        Returns:
            Variance percentage (0.0 if not found)
        """
        for disc in report.discrepancies:
            if disc.category == category:
                return disc.variance
        return 0.0

    def _count_discrepancy_type(self, report: Any, category: str, keyword: str) -> int:
        """
        Count discrepancies of specific type.

        Args:
            report: PlanAuditReport
            category: "files" or "dependencies"
            keyword: "extra" or "missing"

        Returns:
            Count of matching discrepancies
        """
        count = 0
        for disc in report.discrepancies:
            if disc.category == category and keyword in disc.message:
                # Get actual count from the discrepancy
                if isinstance(disc.actual, list):
                    count += len(disc.actual)
                else:
                    count += 1
        return count

    def _calculate_summary(self, audits: list) -> Dict[str, Any]:
        """
        Calculate summary statistics from all audits.

        Args:
            audits: List of audit entries

        Returns:
            Dictionary with summary statistics
        """
        if not audits:
            return {
                "total_audits": 0,
                "severity_distribution": {"low": 0, "medium": 0, "high": 0},
                "decision_distribution": {
                    "approved": 0,
                    "revised": 0,
                    "escalated": 0,
                    "cancelled": 0
                },
                "average_loc_variance": 0.0,
                "average_duration_variance": 0.0,
                "total_extra_files": 0,
                "total_extra_dependencies": 0
            }

        total = len(audits)

        # Calculate averages (excluding zeros)
        loc_variances = [a["loc_variance"] for a in audits if a["loc_variance"] > 0]
        duration_variances = [a["duration_variance"] for a in audits if a["duration_variance"] > 0]

        avg_loc = sum(loc_variances) / len(loc_variances) if loc_variances else 0.0
        avg_duration = sum(duration_variances) / len(duration_variances) if duration_variances else 0.0

        return {
            "total_audits": total,
            "severity_distribution": {
                "low": sum(1 for a in audits if a["severity"] == "low"),
                "medium": sum(1 for a in audits if a["severity"] == "medium"),
                "high": sum(1 for a in audits if a["severity"] == "high")
            },
            "decision_distribution": {
                "approved": sum(1 for a in audits if a["decision"] == "approve"),
                "revised": sum(1 for a in audits if a["decision"] == "revise"),
                "escalated": sum(1 for a in audits if a["decision"] == "escalate"),
                "cancelled": sum(1 for a in audits if a["decision"] == "cancel")
            },
            "average_loc_variance": round(avg_loc, 1),
            "average_duration_variance": round(avg_duration, 1),
            "total_extra_files": sum(a["extra_files"] for a in audits),
            "total_extra_dependencies": sum(a["extra_dependencies"] for a in audits)
        }


# Module exports
__all__ = ["PlanAuditMetricsTracker"]
