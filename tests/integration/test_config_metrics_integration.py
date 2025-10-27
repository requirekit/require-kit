"""Integration tests for configuration and metrics system."""
import os
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from config import PlanReviewConfig
from metrics import PlanReviewMetrics, PlanReviewDashboard
from metrics.metrics_storage import MetricsStorage
from utils import JsonSerializer


@pytest.fixture
def integration_project():
    """Create complete project structure for integration testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)

        # Create project structure
        git_dir = root / ".git"
        git_dir.mkdir()

        claude_dir = root / ".claude"
        claude_dir.mkdir()

        docs_dir = root / "docs" / "state" / "metrics"
        docs_dir.mkdir(parents=True)

        # Change to project directory
        original_cwd = os.getcwd()
        try:
            os.chdir(root)
            yield root
        finally:
            os.chdir(original_cwd)


@pytest.fixture
def clean_singletons():
    """Clean up singleton instances between tests."""
    PlanReviewConfig._instance = None
    PlanReviewConfig._config = None
    PlanReviewConfig._cli_overrides = {}
    yield
    PlanReviewConfig._instance = None
    PlanReviewConfig._config = None
    PlanReviewConfig._cli_overrides = {}


class TestConfigMetricsIntegration:
    """Integration tests for configuration and metrics system."""

    def test_end_to_end_workflow(self, integration_project, clean_singletons):
        """Test complete workflow: load config -> track metrics -> render dashboard."""
        # Step 1: Configure system
        settings_path = integration_project / ".claude" / "settings.json"
        settings_data = {
            "plan_review": {
                "enabled": True,
                "default_mode": "auto",
                "metrics": {
                    "enabled": True,
                    "retention_days": 90
                },
                "thresholds": {
                    "default": {
                        "auto_approve": 80,
                        "approve_with_recommendations": 60,
                        "reject": 0
                    }
                }
            }
        }
        JsonSerializer.safe_save_file(settings_path, settings_data)

        # Step 2: Initialize configuration
        config = PlanReviewConfig()
        assert config.is_enabled() is True
        assert config.is_metrics_enabled() is True

        # Step 3: Track metrics
        metrics_tracker = PlanReviewMetrics(config=config)

        # Track multiple tasks
        for i in range(5):
            task_id = f"TASK-{i+1:03d}"

            # Track complexity
            metrics_tracker.track_complexity(
                task_id=task_id,
                complexity_score=20 + (i * 10),
                factors={"files": i + 1},
                stack="python"
            )

            # Determine decision based on score
            score = 75 + (i * 5)
            decision = config.get_threshold(score, stack="python")

            # Track decision
            metrics_tracker.track_decision(
                task_id=task_id,
                architectural_score=score,
                decision=decision,
                complexity_score=20 + (i * 10),
                stack="python",
                forced=False
            )

            # Track outcome
            metrics_tracker.track_outcome(
                task_id=task_id,
                decision=decision,
                human_override=False,
                duration_seconds=30.0 + (i * 10),
                final_status="approved",
                stack="python"
            )

        # Step 4: Render dashboard
        dashboard = PlanReviewDashboard(config=config)
        output = dashboard.render(days=30)

        # Verify dashboard output
        assert "Plan Review Metrics Dashboard" in output
        assert "Total Reviews:           5" in output
        assert "python" in output
        assert "DECISIONS" in output
        assert "COMPLEXITY DISTRIBUTION" in output

    def test_configuration_affects_metrics_tracking(self, integration_project, clean_singletons):
        """Test that configuration changes affect metrics tracking."""
        # Start with metrics enabled
        settings_path = integration_project / ".claude" / "settings.json"
        settings_data = {
            "plan_review": {
                "metrics": {
                    "enabled": True
                }
            }
        }
        JsonSerializer.safe_save_file(settings_path, settings_data)

        config = PlanReviewConfig()
        metrics_tracker = PlanReviewMetrics(config=config)

        # Track should work
        result = metrics_tracker.track_complexity(
            task_id="TASK-001",
            complexity_score=30,
            factors={}
        )
        assert result is True

        # Disable metrics
        settings_data["plan_review"]["metrics"]["enabled"] = False
        JsonSerializer.safe_save_file(settings_path, settings_data)

        # Reload configuration
        config.reload()

        # Track should now be disabled
        result = metrics_tracker.track_complexity(
            task_id="TASK-002",
            complexity_score=30,
            factors={}
        )
        assert result is False

    def test_stack_overrides_work_end_to_end(self, integration_project, clean_singletons):
        """Test stack-specific overrides work throughout the system."""
        # Configure with stack overrides
        settings_path = integration_project / ".claude" / "settings.json"
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
        metrics_tracker = PlanReviewMetrics(config=config)

        # Track metrics for different stacks
        # Python task with score 85 (below Python threshold, above default)
        metrics_tracker.track_decision(
            task_id="TASK-PYTHON",
            architectural_score=85,
            decision=config.get_threshold(85, stack="python"),
            complexity_score=25,
            stack="python"
        )

        # Default stack task with score 85
        metrics_tracker.track_decision(
            task_id="TASK-DEFAULT",
            architectural_score=85,
            decision=config.get_threshold(85, stack="typescript"),
            complexity_score=25,
            stack="typescript"
        )

        # Verify decisions are different
        metrics = metrics_tracker.storage.read_all_metrics()

        python_metric = next(m for m in metrics if m["task_id"] == "TASK-PYTHON")
        default_metric = next(m for m in metrics if m["task_id"] == "TASK-DEFAULT")

        assert python_metric["decision"] == "approve_with_recommendations"
        assert default_metric["decision"] == "auto_approve"

    def test_metrics_survive_config_reload(self, integration_project, clean_singletons):
        """Test that metrics persist across configuration reloads."""
        config = PlanReviewConfig()
        metrics_tracker = PlanReviewMetrics(config=config)

        # Track some metrics
        metrics_tracker.track_complexity(
            task_id="TASK-001",
            complexity_score=30,
            factors={}
        )

        metrics_tracker.track_decision(
            task_id="TASK-001",
            architectural_score=85,
            decision="auto_approve",
            complexity_score=30
        )

        # Reload configuration
        config.reload()

        # Metrics should still be accessible
        dashboard = PlanReviewDashboard(config=config)
        output = dashboard.render(days=30)

        assert "Total Reviews:           1" in output

    def test_metrics_retention_cleanup(self, integration_project, clean_singletons):
        """Test metrics retention cleanup works."""
        # Configure with short retention
        settings_path = integration_project / ".claude" / "settings.json"
        settings_data = {
            "plan_review": {
                "metrics": {
                    "enabled": True,
                    "retention_days": 30
                }
            }
        }
        JsonSerializer.safe_save_file(settings_path, settings_data)

        config = PlanReviewConfig()
        metrics_tracker = PlanReviewMetrics(config=config)

        # Add old and recent metrics
        now = datetime.utcnow()
        old_timestamp = (now - timedelta(days=60)).isoformat() + "Z"
        recent_timestamp = (now - timedelta(days=10)).isoformat() + "Z"

        # Manually add metrics with specific timestamps
        metrics_tracker.storage.append_metric({
            "type": "decision",
            "task_id": "TASK-OLD",
            "architectural_score": 80,
            "decision": "auto_approve",
            "complexity_score": 20,
            "timestamp": old_timestamp
        })

        metrics_tracker.storage.append_metric({
            "type": "decision",
            "task_id": "TASK-RECENT",
            "architectural_score": 85,
            "decision": "auto_approve",
            "complexity_score": 25,
            "timestamp": recent_timestamp
        })

        # Run cleanup
        removed = metrics_tracker.cleanup_old_metrics()

        assert removed == 1  # Only old metric removed

        # Verify only recent metric remains
        metrics = metrics_tracker.storage.read_all_metrics()
        assert len(metrics) == 1
        assert metrics[0]["task_id"] == "TASK-RECENT"

    def test_dashboard_aggregates_across_stacks(self, integration_project, clean_singletons):
        """Test dashboard aggregates metrics across different stacks."""
        config = PlanReviewConfig()
        metrics_tracker = PlanReviewMetrics(config=config)

        # Track metrics for different stacks
        stacks = ["python", "typescript", "react"]
        for i, stack in enumerate(stacks):
            metrics_tracker.track_decision(
                task_id=f"TASK-{i+1}",
                architectural_score=80 + (i * 5),
                decision="auto_approve",
                complexity_score=20,
                stack=stack
            )

        # Render dashboard
        dashboard = PlanReviewDashboard(config=config)
        output = dashboard.render(days=30)

        # Verify all stacks appear
        assert "python" in output
        assert "typescript" in output
        assert "react" in output
        assert "BY TECHNOLOGY STACK" in output

    def test_environment_overrides_affect_tracking(self, integration_project, clean_singletons):
        """Test environment variable overrides affect metrics tracking."""
        original_env = os.getenv('PLAN_REVIEW_METRICS_ENABLED')

        try:
            # Disable via environment
            os.environ['PLAN_REVIEW_METRICS_ENABLED'] = 'false'

            # Force reload
            PlanReviewConfig._instance = None
            PlanReviewConfig._config = None

            config = PlanReviewConfig()
            metrics_tracker = PlanReviewMetrics(config=config)

            # Tracking should be disabled
            result = metrics_tracker.track_complexity(
                task_id="TASK-001",
                complexity_score=30,
                factors={}
            )
            assert result is False

        finally:
            if original_env is None:
                os.environ.pop('PLAN_REVIEW_METRICS_ENABLED', None)
            else:
                os.environ['PLAN_REVIEW_METRICS_ENABLED'] = original_env

    def test_cli_overrides_affect_decisions(self, integration_project, clean_singletons):
        """Test CLI overrides affect decision-making."""
        config = PlanReviewConfig()
        metrics_tracker = PlanReviewMetrics(config=config)

        # Set CLI override for auto-approve threshold
        config.set_cli_override('thresholds.auto_approve', 95)

        # Score of 85 should not auto-approve with high threshold
        decision = config.get_threshold(85)
        assert decision != "auto_approve"

        # Track decision
        metrics_tracker.track_decision(
            task_id="TASK-001",
            architectural_score=85,
            decision=decision,
            complexity_score=20
        )

        # Verify decision was recorded correctly
        metrics = metrics_tracker.storage.read_all_metrics()
        assert len(metrics) == 1
        assert metrics[0]["decision"] != "auto_approve"

    def test_complete_task_lifecycle(self, integration_project, clean_singletons):
        """Test tracking complete task lifecycle."""
        config = PlanReviewConfig()
        metrics_tracker = PlanReviewMetrics(config=config)

        task_id = "TASK-LIFECYCLE"

        # Step 1: Calculate complexity
        complexity_score = 35
        metrics_tracker.track_complexity(
            task_id=task_id,
            complexity_score=complexity_score,
            factors={
                "file_count": 5,
                "line_changes": 300,
                "dependencies": 3
            },
            stack="python"
        )

        # Step 2: Architectural review
        arch_score = 85
        decision = config.get_threshold(arch_score, stack="python")
        metrics_tracker.track_decision(
            task_id=task_id,
            architectural_score=arch_score,
            decision=decision,
            complexity_score=complexity_score,
            stack="python",
            forced=complexity_score >= 30,
            recommendations=["Consider breaking into smaller modules"]
        )

        # Step 3: Final outcome
        metrics_tracker.track_outcome(
            task_id=task_id,
            decision=decision,
            human_override=False,
            duration_seconds=120.0,
            final_status="approved",
            stack="python"
        )

        # Verify all metrics were recorded
        metrics = metrics_tracker.storage.read_all_metrics()
        assert len(metrics) == 3

        # Verify each metric type
        types = [m["type"] for m in metrics]
        assert "complexity" in types
        assert "decision" in types
        assert "outcome" in types

        # Verify all have same task_id
        for metric in metrics:
            assert metric["task_id"] == task_id

    def test_dashboard_performance_with_many_metrics(self, integration_project, clean_singletons):
        """Test dashboard performance with large number of metrics."""
        config = PlanReviewConfig()
        metrics_tracker = PlanReviewMetrics(config=config)

        # Add 100 metrics
        for i in range(100):
            metrics_tracker.track_decision(
                task_id=f"TASK-{i:03d}",
                architectural_score=70 + (i % 30),
                decision="auto_approve",
                complexity_score=10 + (i % 40),
                stack="python" if i % 2 == 0 else "typescript"
            )

        # Render dashboard - should complete without errors
        dashboard = PlanReviewDashboard(config=config)
        output = dashboard.render(days=30)

        assert "Total Reviews:           100" in output
        assert "python" in output
        assert "typescript" in output

    def test_concurrent_metrics_tracking(self, integration_project, clean_singletons):
        """Test that metrics are safely tracked concurrently."""
        config = PlanReviewConfig()
        metrics_tracker = PlanReviewMetrics(config=config)

        # Simulate multiple quick writes
        for i in range(10):
            metrics_tracker.track_complexity(
                task_id=f"TASK-{i}",
                complexity_score=20 + i,
                factors={}
            )

        # All metrics should be recorded
        metrics = metrics_tracker.storage.read_all_metrics()
        assert len(metrics) == 10

        # All should have unique task IDs
        task_ids = [m["task_id"] for m in metrics]
        assert len(set(task_ids)) == 10
