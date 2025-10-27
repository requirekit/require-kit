"""Unit tests for PlanReviewMetrics."""
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from metrics import PlanReviewMetrics
from metrics.metrics_storage import MetricsStorage
from config import PlanReviewConfig


@pytest.fixture
def temp_metrics_file():
    """Create temporary metrics file."""
    with tempfile.NamedTemporaryFile(suffix='.jsonl', delete=False) as f:
        metrics_file = Path(f.name)
    yield metrics_file
    if metrics_file.exists():
        metrics_file.unlink()


@pytest.fixture
def mock_config():
    """Create mock configuration."""
    config = Mock(spec=PlanReviewConfig)
    config.is_metrics_enabled.return_value = True
    config.get_metrics_retention_days.return_value = 90
    return config


@pytest.fixture
def metrics_tracker(temp_metrics_file, mock_config):
    """Create PlanReviewMetrics instance."""
    storage = MetricsStorage(metrics_file=temp_metrics_file)
    return PlanReviewMetrics(storage=storage, config=mock_config)


class TestPlanReviewMetrics:
    """Test PlanReviewMetrics class."""

    def test_track_complexity_writes_metric(self, metrics_tracker, temp_metrics_file):
        """Test track_complexity writes correct metric."""
        result = metrics_tracker.track_complexity(
            task_id="TASK-001",
            complexity_score=35,
            factors={
                "file_count": 3,
                "line_changes": 200,
                "dependencies": 5
            },
            stack="python"
        )

        assert result is True

        # Read back metric
        metrics = metrics_tracker.storage.read_all_metrics()
        assert len(metrics) == 1

        metric = metrics[0]
        assert metric["type"] == "complexity"
        assert metric["task_id"] == "TASK-001"
        assert metric["complexity_score"] == 35
        assert metric["stack"] == "python"
        assert "timestamp" in metric

    def test_track_complexity_disabled(self, temp_metrics_file, mock_config):
        """Test track_complexity when metrics disabled."""
        mock_config.is_metrics_enabled.return_value = False
        storage = MetricsStorage(metrics_file=temp_metrics_file)
        tracker = PlanReviewMetrics(storage=storage, config=mock_config)

        result = tracker.track_complexity(
            task_id="TASK-001",
            complexity_score=35,
            factors={}
        )

        assert result is False

        # Verify nothing was written
        metrics = storage.read_all_metrics()
        assert len(metrics) == 0

    def test_track_decision_writes_metric(self, metrics_tracker):
        """Test track_decision writes correct metric."""
        result = metrics_tracker.track_decision(
            task_id="TASK-001",
            architectural_score=85,
            decision="auto_approve",
            complexity_score=25,
            stack="python",
            forced=False,
            recommendations=["Use dependency injection"]
        )

        assert result is True

        metrics = metrics_tracker.storage.read_all_metrics()
        assert len(metrics) == 1

        metric = metrics[0]
        assert metric["type"] == "decision"
        assert metric["task_id"] == "TASK-001"
        assert metric["architectural_score"] == 85
        assert metric["decision"] == "auto_approve"
        assert metric["complexity_score"] == 25
        assert metric["stack"] == "python"
        assert metric["forced"] is False
        assert len(metric["recommendations"]) == 1

    def test_track_decision_without_recommendations(self, metrics_tracker):
        """Test track_decision with no recommendations."""
        result = metrics_tracker.track_decision(
            task_id="TASK-001",
            architectural_score=85,
            decision="auto_approve",
            complexity_score=25
        )

        assert result is True

        metrics = metrics_tracker.storage.read_all_metrics()
        metric = metrics[0]
        assert metric["recommendations"] == []

    def test_track_decision_disabled(self, temp_metrics_file, mock_config):
        """Test track_decision when metrics disabled."""
        mock_config.is_metrics_enabled.return_value = False
        storage = MetricsStorage(metrics_file=temp_metrics_file)
        tracker = PlanReviewMetrics(storage=storage, config=mock_config)

        result = tracker.track_decision(
            task_id="TASK-001",
            architectural_score=85,
            decision="auto_approve",
            complexity_score=25
        )

        assert result is False

        metrics = storage.read_all_metrics()
        assert len(metrics) == 0

    def test_track_outcome_writes_metric(self, metrics_tracker):
        """Test track_outcome writes correct metric."""
        result = metrics_tracker.track_outcome(
            task_id="TASK-001",
            decision="auto_approve",
            human_override=False,
            duration_seconds=45.5,
            final_status="approved",
            stack="python"
        )

        assert result is True

        metrics = metrics_tracker.storage.read_all_metrics()
        assert len(metrics) == 1

        metric = metrics[0]
        assert metric["type"] == "outcome"
        assert metric["task_id"] == "TASK-001"
        assert metric["decision"] == "auto_approve"
        assert metric["human_override"] is False
        assert metric["duration_seconds"] == 45.5
        assert metric["final_status"] == "approved"
        assert metric["stack"] == "python"

    def test_track_outcome_with_override(self, metrics_tracker):
        """Test track_outcome with human override."""
        result = metrics_tracker.track_outcome(
            task_id="TASK-001",
            decision="reject",
            human_override=True,
            duration_seconds=120.0,
            final_status="approved"
        )

        assert result is True

        metrics = metrics_tracker.storage.read_all_metrics()
        metric = metrics[0]
        assert metric["human_override"] is True

    def test_track_outcome_disabled(self, temp_metrics_file, mock_config):
        """Test track_outcome when metrics disabled."""
        mock_config.is_metrics_enabled.return_value = False
        storage = MetricsStorage(metrics_file=temp_metrics_file)
        tracker = PlanReviewMetrics(storage=storage, config=mock_config)

        result = tracker.track_outcome(
            task_id="TASK-001",
            decision="auto_approve",
            human_override=False,
            duration_seconds=45.5,
            final_status="approved"
        )

        assert result is False

        metrics = storage.read_all_metrics()
        assert len(metrics) == 0

    def test_track_threshold_adjustment_writes_metric(self, metrics_tracker):
        """Test track_threshold_adjustment writes correct metric."""
        result = metrics_tracker.track_threshold_adjustment(
            old_threshold=80,
            new_threshold=85,
            threshold_type="auto_approve",
            reason="Improved code quality over time",
            stack="python"
        )

        assert result is True

        metrics = metrics_tracker.storage.read_all_metrics()
        assert len(metrics) == 1

        metric = metrics[0]
        assert metric["type"] == "threshold_adjustment"
        assert metric["old_threshold"] == 80
        assert metric["new_threshold"] == 85
        assert metric["threshold_type"] == "auto_approve"
        assert metric["reason"] == "Improved code quality over time"
        assert metric["stack"] == "python"

    def test_track_threshold_adjustment_global(self, metrics_tracker):
        """Test track_threshold_adjustment for global threshold."""
        result = metrics_tracker.track_threshold_adjustment(
            old_threshold=60,
            new_threshold=65,
            threshold_type="approve_with_recommendations",
            reason="Stricter quality standards",
            stack=None
        )

        assert result is True

        metrics = metrics_tracker.storage.read_all_metrics()
        metric = metrics[0]
        assert metric["stack"] is None

    def test_get_recent_metrics(self, metrics_tracker):
        """Test get_recent_metrics retrieves metrics."""
        # Add some metrics
        for i in range(5):
            metrics_tracker.track_complexity(
                task_id=f"TASK-{i:03d}",
                complexity_score=20 + i,
                factors={}
            )

        recent = metrics_tracker.get_recent_metrics(days=30)

        assert len(recent) == 5

    def test_get_recent_metrics_filters_by_date(self, metrics_tracker):
        """Test get_recent_metrics filters by date."""
        # This test would require mocking datetime or using time manipulation
        # For now, just verify it delegates to storage
        with patch.object(metrics_tracker.storage, 'read_recent_metrics') as mock_read:
            mock_read.return_value = []

            result = metrics_tracker.get_recent_metrics(days=7)

            mock_read.assert_called_once_with(7)

    def test_cleanup_old_metrics(self, metrics_tracker, mock_config):
        """Test cleanup_old_metrics removes old data."""
        mock_config.get_metrics_retention_days.return_value = 90

        with patch.object(metrics_tracker.storage, 'clear_old_metrics') as mock_clear:
            mock_clear.return_value = 5

            removed = metrics_tracker.cleanup_old_metrics()

            assert removed == 5
            mock_clear.assert_called_once_with(90)

    def test_multiple_metric_types(self, metrics_tracker):
        """Test tracking multiple metric types."""
        # Track different metric types
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

        metrics_tracker.track_outcome(
            task_id="TASK-001",
            decision="auto_approve",
            human_override=False,
            duration_seconds=60.0,
            final_status="approved"
        )

        metrics = metrics_tracker.storage.read_all_metrics()
        assert len(metrics) == 3

        types = [m["type"] for m in metrics]
        assert "complexity" in types
        assert "decision" in types
        assert "outcome" in types

    def test_integration_with_storage(self, temp_metrics_file, mock_config):
        """Test integration with MetricsStorage."""
        storage = MetricsStorage(metrics_file=temp_metrics_file)
        tracker = PlanReviewMetrics(storage=storage, config=mock_config)

        # Track a metric
        tracker.track_complexity(
            task_id="TASK-001",
            complexity_score=40,
            factors={"files": 5}
        )

        # Verify it was written to file
        assert temp_metrics_file.exists()
        content = temp_metrics_file.read_text()
        assert "TASK-001" in content
        assert "complexity" in content

    def test_default_initialization(self):
        """Test PlanReviewMetrics can initialize with defaults."""
        # This should not raise an error
        tracker = PlanReviewMetrics()

        assert tracker.storage is not None
        assert tracker.config is not None
