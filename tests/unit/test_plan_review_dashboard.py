"""Unit tests for PlanReviewDashboard."""
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import Mock

import pytest

from metrics import PlanReviewDashboard
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
    return config


@pytest.fixture
def dashboard(temp_metrics_file, mock_config):
    """Create PlanReviewDashboard instance."""
    storage = MetricsStorage(metrics_file=temp_metrics_file)
    return PlanReviewDashboard(storage=storage, config=mock_config)


@pytest.fixture
def sample_metrics(temp_metrics_file):
    """Create sample metrics for testing."""
    storage = MetricsStorage(metrics_file=temp_metrics_file)

    now = datetime.utcnow()

    # Add complexity metrics
    storage.append_metric({
        "type": "complexity",
        "task_id": "TASK-001",
        "complexity_score": 15,
        "timestamp": (now - timedelta(days=5)).isoformat() + "Z"
    })

    storage.append_metric({
        "type": "complexity",
        "task_id": "TASK-002",
        "complexity_score": 35,
        "timestamp": (now - timedelta(days=4)).isoformat() + "Z"
    })

    # Add decision metrics
    storage.append_metric({
        "type": "decision",
        "task_id": "TASK-001",
        "architectural_score": 90,
        "decision": "auto_approve",
        "complexity_score": 15,
        "stack": "python",
        "forced": False,
        "recommendations": [],
        "timestamp": (now - timedelta(days=5)).isoformat() + "Z"
    })

    storage.append_metric({
        "type": "decision",
        "task_id": "TASK-002",
        "architectural_score": 65,
        "decision": "approve_with_recommendations",
        "complexity_score": 35,
        "stack": "python",
        "forced": True,
        "recommendations": ["Improve modularity"],
        "timestamp": (now - timedelta(days=4)).isoformat() + "Z"
    })

    # Add outcome metrics
    storage.append_metric({
        "type": "outcome",
        "task_id": "TASK-001",
        "decision": "auto_approve",
        "human_override": False,
        "duration_seconds": 45.0,
        "final_status": "approved",
        "stack": "python",
        "timestamp": (now - timedelta(days=5)).isoformat() + "Z"
    })

    storage.append_metric({
        "type": "outcome",
        "task_id": "TASK-002",
        "decision": "approve_with_recommendations",
        "human_override": True,
        "duration_seconds": 120.0,
        "final_status": "approved",
        "stack": "python",
        "timestamp": (now - timedelta(days=4)).isoformat() + "Z"
    })

    return storage


class TestPlanReviewDashboard:
    """Test PlanReviewDashboard class."""

    def test_render_empty_data(self, dashboard):
        """Test render with no data."""
        output = dashboard.render(days=30)

        assert "Plan Review Metrics Dashboard" in output
        assert "Total Reviews:           0" in output
        assert "No decisions recorded" in output

    def test_render_with_data(self, temp_metrics_file, mock_config, sample_metrics):
        """Test render with sample data."""
        dashboard = PlanReviewDashboard(storage=sample_metrics, config=mock_config)

        output = dashboard.render(days=30)

        # Check header
        assert "Plan Review Metrics Dashboard" in output
        assert "Last 30 Days" in output

        # Check overview
        assert "OVERVIEW" in output
        assert "Total Reviews:" in output

        # Check sections
        assert "DECISIONS" in output
        assert "COMPLEXITY DISTRIBUTION" in output
        assert "BY TECHNOLOGY STACK" in output
        assert "OUTCOMES" in output

    def test_render_invalid_format(self, dashboard):
        """Test render with invalid format raises error."""
        with pytest.raises(ValueError, match="Only 'terminal' format supported"):
            dashboard.render(format="html")

    def test_aggregate_metrics_empty(self, dashboard):
        """Test _aggregate_metrics with empty list."""
        summary = dashboard._aggregate_metrics([])

        assert summary["total_reviews"] == 0
        assert summary["avg_architectural_score"] == 0.0
        assert summary["forced_reviews"] == 0
        assert summary["human_overrides"] == 0

    def test_aggregate_metrics_complexity_distribution(self, temp_metrics_file, mock_config, sample_metrics):
        """Test complexity distribution aggregation."""
        dashboard = PlanReviewDashboard(storage=sample_metrics, config=mock_config)

        metrics = sample_metrics.read_all_metrics()
        summary = dashboard._aggregate_metrics(metrics)

        # Should have 2 decisions with complexity scores 15 and 35
        assert summary["complexity_distribution"]["10-19"] == 1
        assert summary["complexity_distribution"]["30-39"] == 1

    def test_aggregate_metrics_decisions(self, temp_metrics_file, mock_config, sample_metrics):
        """Test decision counts aggregation."""
        dashboard = PlanReviewDashboard(storage=sample_metrics, config=mock_config)

        metrics = sample_metrics.read_all_metrics()
        summary = dashboard._aggregate_metrics(metrics)

        assert summary["total_reviews"] == 2
        assert summary["decisions"]["auto_approve"] == 1
        assert summary["decisions"]["approve_with_recommendations"] == 1

    def test_aggregate_metrics_averages(self, temp_metrics_file, mock_config, sample_metrics):
        """Test average calculations."""
        dashboard = PlanReviewDashboard(storage=sample_metrics, config=mock_config)

        metrics = sample_metrics.read_all_metrics()
        summary = dashboard._aggregate_metrics(metrics)

        # Architectural scores: 90, 65 -> avg 77.5
        assert summary["avg_architectural_score"] == 77.5

        # Complexity scores: 15, 35 -> avg 25
        assert summary["avg_complexity_score"] == 25.0

        # Durations: 45, 120 -> avg 82.5
        assert summary["avg_duration"] == 82.5

    def test_aggregate_metrics_forced_reviews(self, temp_metrics_file, mock_config, sample_metrics):
        """Test forced reviews count."""
        dashboard = PlanReviewDashboard(storage=sample_metrics, config=mock_config)

        metrics = sample_metrics.read_all_metrics()
        summary = dashboard._aggregate_metrics(metrics)

        assert summary["forced_reviews"] == 1  # TASK-002 was forced

    def test_aggregate_metrics_human_overrides(self, temp_metrics_file, mock_config, sample_metrics):
        """Test human overrides count."""
        dashboard = PlanReviewDashboard(storage=sample_metrics, config=mock_config)

        metrics = sample_metrics.read_all_metrics()
        summary = dashboard._aggregate_metrics(metrics)

        assert summary["human_overrides"] == 1  # TASK-002 had override

    def test_aggregate_metrics_by_stack(self, temp_metrics_file, mock_config, sample_metrics):
        """Test by-stack aggregation."""
        dashboard = PlanReviewDashboard(storage=sample_metrics, config=mock_config)

        metrics = sample_metrics.read_all_metrics()
        summary = dashboard._aggregate_metrics(metrics)

        assert "python" in summary["by_stack"]
        assert summary["by_stack"]["python"]["count"] == 2
        assert summary["by_stack"]["python"]["avg_score"] == 77.5  # (90 + 65) / 2

    def test_aggregate_metrics_outcomes(self, temp_metrics_file, mock_config, sample_metrics):
        """Test outcomes aggregation."""
        dashboard = PlanReviewDashboard(storage=sample_metrics, config=mock_config)

        metrics = sample_metrics.read_all_metrics()
        summary = dashboard._aggregate_metrics(metrics)

        assert summary["outcomes"]["approved"] == 2

    def test_complexity_buckets(self, dashboard):
        """Test complexity distribution buckets."""
        metrics = [
            {"type": "decision", "architectural_score": 80, "complexity_score": 5, "decision": "auto_approve"},
            {"type": "decision", "architectural_score": 80, "complexity_score": 15, "decision": "auto_approve"},
            {"type": "decision", "architectural_score": 80, "complexity_score": 25, "decision": "auto_approve"},
            {"type": "decision", "architectural_score": 80, "complexity_score": 35, "decision": "auto_approve"},
            {"type": "decision", "architectural_score": 80, "complexity_score": 45, "decision": "auto_approve"},
        ]

        summary = dashboard._aggregate_metrics(metrics)

        assert summary["complexity_distribution"]["0-9"] == 1
        assert summary["complexity_distribution"]["10-19"] == 1
        assert summary["complexity_distribution"]["20-29"] == 1
        assert summary["complexity_distribution"]["30-39"] == 1
        assert summary["complexity_distribution"]["40+"] == 1

    def test_render_bar_zero_max(self, dashboard):
        """Test _render_bar with zero max value."""
        bar = dashboard._render_bar(0, 0, width=10)

        assert len(bar) == 0  # Should return empty bar

    def test_render_bar_scaling(self, dashboard):
        """Test _render_bar scales correctly."""
        # Half full
        bar = dashboard._render_bar(5, 10, width=10)
        filled_count = bar.count('█')
        assert filled_count == 5

        # Full
        bar = dashboard._render_bar(10, 10, width=10)
        filled_count = bar.count('█')
        assert filled_count == 10

        # Empty
        bar = dashboard._render_bar(0, 10, width=10)
        filled_count = bar.count('█')
        assert filled_count == 0

    def test_render_bar_width(self, dashboard):
        """Test _render_bar respects width."""
        bar = dashboard._render_bar(5, 10, width=20)

        # Total length should be 20
        assert len(bar) == 20

    def test_render_bar_overflow_protection(self, dashboard):
        """Test _render_bar handles overflow."""
        # Value greater than max (edge case)
        bar = dashboard._render_bar(15, 10, width=10)

        # Should not exceed width
        assert len(bar) == 10

    def test_render_terminal_header(self, dashboard):
        """Test terminal output header."""
        output = dashboard._render_terminal({
            'total_reviews': 0,
            'decisions': {},
            'complexity_distribution': {},
            'avg_architectural_score': 0.0,
            'avg_complexity_score': 0.0,
            'avg_duration': 0.0,
            'forced_reviews': 0,
            'human_overrides': 0,
            'by_stack': {},
            'outcomes': {}
        }, days=30)

        assert "=" * 80 in output
        assert "Plan Review Metrics Dashboard (Last 30 Days)" in output

    def test_render_terminal_decisions_section(self, temp_metrics_file, mock_config, sample_metrics):
        """Test terminal output decisions section."""
        dashboard = PlanReviewDashboard(storage=sample_metrics, config=mock_config)

        metrics = sample_metrics.read_all_metrics()
        summary = dashboard._aggregate_metrics(metrics)
        output = dashboard._render_terminal(summary, days=30)

        assert "DECISIONS" in output
        assert "auto_approve" in output
        assert "approve_with_recommendations" in output
        assert "█" in output  # Should have bar charts

    def test_render_terminal_complexity_section(self, temp_metrics_file, mock_config, sample_metrics):
        """Test terminal output complexity section."""
        dashboard = PlanReviewDashboard(storage=sample_metrics, config=mock_config)

        metrics = sample_metrics.read_all_metrics()
        summary = dashboard._aggregate_metrics(metrics)
        output = dashboard._render_terminal(summary, days=30)

        assert "COMPLEXITY DISTRIBUTION" in output
        assert "10-19" in output
        assert "30-39" in output

    def test_render_terminal_by_stack_section(self, temp_metrics_file, mock_config, sample_metrics):
        """Test terminal output by-stack section."""
        dashboard = PlanReviewDashboard(storage=sample_metrics, config=mock_config)

        metrics = sample_metrics.read_all_metrics()
        summary = dashboard._aggregate_metrics(metrics)
        output = dashboard._render_terminal(summary, days=30)

        assert "BY TECHNOLOGY STACK" in output
        assert "python" in output
        assert "Count:" in output
        assert "Avg Score:" in output

    def test_render_terminal_outcomes_section(self, temp_metrics_file, mock_config, sample_metrics):
        """Test terminal output outcomes section."""
        dashboard = PlanReviewDashboard(storage=sample_metrics, config=mock_config)

        metrics = sample_metrics.read_all_metrics()
        summary = dashboard._aggregate_metrics(metrics)
        output = dashboard._render_terminal(summary, days=30)

        assert "OUTCOMES" in output
        assert "approved" in output

    def test_print_dashboard(self, dashboard, capsys):
        """Test print_dashboard prints to console."""
        dashboard.print_dashboard(days=30)

        captured = capsys.readouterr()
        assert "Plan Review Metrics Dashboard" in captured.out

    def test_render_with_custom_days(self, temp_metrics_file, mock_config, sample_metrics):
        """Test render with custom days parameter."""
        dashboard = PlanReviewDashboard(storage=sample_metrics, config=mock_config)

        output = dashboard.render(days=7)

        assert "Last 7 Days" in output

    def test_default_initialization(self):
        """Test PlanReviewDashboard can initialize with defaults."""
        # This should not raise an error
        dashboard = PlanReviewDashboard()

        assert dashboard.storage is not None
        assert dashboard.config is not None
