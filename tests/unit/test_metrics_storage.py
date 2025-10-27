"""Unit tests for MetricsStorage."""
import json
import os
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from metrics.metrics_storage import MetricsStorage


@pytest.fixture
def temp_metrics_dir():
    """Create temporary metrics directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        metrics_dir = Path(tmpdir) / "metrics"
        metrics_dir.mkdir()
        yield metrics_dir


@pytest.fixture
def metrics_storage(temp_metrics_dir):
    """Create MetricsStorage instance with temp file."""
    metrics_file = temp_metrics_dir / "test_metrics.jsonl"
    return MetricsStorage(metrics_file=metrics_file)


class TestMetricsStorage:
    """Test MetricsStorage class."""

    def test_init_creates_directory(self, temp_metrics_dir):
        """Test initialization creates metrics directory."""
        metrics_file = temp_metrics_dir / "new_dir" / "metrics.jsonl"
        storage = MetricsStorage(metrics_file=metrics_file)

        assert metrics_file.parent.exists()

    def test_init_creates_gitignore(self, temp_metrics_dir):
        """Test initialization creates .gitignore."""
        metrics_file = temp_metrics_dir / "metrics.jsonl"
        storage = MetricsStorage(metrics_file=metrics_file)

        gitignore_path = temp_metrics_dir / ".gitignore"
        assert gitignore_path.exists()

        content = gitignore_path.read_text()
        assert "*.jsonl" in content
        assert "*.json" in content

    def test_append_metric_creates_file(self, metrics_storage):
        """Test append_metric creates JSONL file."""
        metric = {
            "type": "test",
            "value": 42
        }

        result = metrics_storage.append_metric(metric)

        assert result is True
        assert metrics_storage.metrics_file.exists()

    def test_append_metric_adds_timestamp(self, metrics_storage):
        """Test append_metric adds timestamp if not present."""
        metric = {
            "type": "test",
            "value": 42
        }

        metrics_storage.append_metric(metric)

        # Read back the metric
        content = metrics_storage.metrics_file.read_text()
        saved_metric = json.loads(content.strip())

        assert "timestamp" in saved_metric
        assert saved_metric["timestamp"].endswith("Z")

    def test_append_metric_preserves_existing_timestamp(self, metrics_storage):
        """Test append_metric preserves existing timestamp."""
        custom_timestamp = "2024-01-01T12:00:00Z"
        metric = {
            "type": "test",
            "value": 42,
            "timestamp": custom_timestamp
        }

        metrics_storage.append_metric(metric)

        content = metrics_storage.metrics_file.read_text()
        saved_metric = json.loads(content.strip())

        assert saved_metric["timestamp"] == custom_timestamp

    def test_append_multiple_metrics(self, metrics_storage):
        """Test appending multiple metrics."""
        metrics = [
            {"type": "test1", "value": 1},
            {"type": "test2", "value": 2},
            {"type": "test3", "value": 3}
        ]

        for metric in metrics:
            result = metrics_storage.append_metric(metric)
            assert result is True

        # Verify all metrics were saved
        content = metrics_storage.metrics_file.read_text()
        lines = content.strip().split("\n")
        assert len(lines) == 3

    def test_append_metric_atomic_write(self, metrics_storage):
        """Test that append_metric doesn't leave temp files."""
        metric = {"type": "test", "value": 42}

        metrics_storage.append_metric(metric)

        # Check no .tmp files left
        tmp_files = list(metrics_storage.metrics_file.parent.glob("*.tmp"))
        assert len(tmp_files) == 0

    def test_read_all_metrics_empty_file(self, metrics_storage):
        """Test read_all_metrics with no file."""
        metrics = metrics_storage.read_all_metrics()

        assert metrics == []

    def test_read_all_metrics_single(self, metrics_storage):
        """Test read_all_metrics with single metric."""
        metric = {"type": "test", "value": 42}
        metrics_storage.append_metric(metric)

        metrics = metrics_storage.read_all_metrics()

        assert len(metrics) == 1
        assert metrics[0]["type"] == "test"
        assert metrics[0]["value"] == 42

    def test_read_all_metrics_multiple(self, metrics_storage):
        """Test read_all_metrics with multiple metrics."""
        test_metrics = [
            {"type": "test1", "value": 1},
            {"type": "test2", "value": 2},
            {"type": "test3", "value": 3}
        ]

        for metric in test_metrics:
            metrics_storage.append_metric(metric)

        metrics = metrics_storage.read_all_metrics()

        assert len(metrics) == 3
        for i, metric in enumerate(metrics):
            assert metric["type"] == f"test{i+1}"
            assert metric["value"] == i+1

    def test_read_all_metrics_skips_empty_lines(self, metrics_storage):
        """Test read_all_metrics skips empty lines."""
        # Write metrics with empty lines
        content = '{"type": "test1", "value": 1}\n\n{"type": "test2", "value": 2}\n\n\n'
        metrics_storage.metrics_file.write_text(content)

        metrics = metrics_storage.read_all_metrics()

        assert len(metrics) == 2

    def test_read_all_metrics_handles_corrupted_lines(self, metrics_storage, capsys):
        """Test read_all_metrics handles corrupted JSON lines."""
        # Write some good and bad lines
        content = (
            '{"type": "test1", "value": 1}\n'
            '{"invalid": json}\n'  # Corrupted
            '{"type": "test2", "value": 2}\n'
        )
        metrics_storage.metrics_file.write_text(content)

        metrics = metrics_storage.read_all_metrics()

        # Should get 2 valid metrics
        assert len(metrics) == 2

        # Should have printed warning
        captured = capsys.readouterr()
        assert "Warning" in captured.out
        assert "Skipping corrupted metric" in captured.out

    def test_read_recent_metrics_filters_by_date(self, metrics_storage):
        """Test read_recent_metrics filters by date."""
        now = datetime.utcnow()
        old_timestamp = (now - timedelta(days=40)).isoformat() + "Z"
        recent_timestamp = (now - timedelta(days=10)).isoformat() + "Z"

        metrics = [
            {"type": "old", "timestamp": old_timestamp},
            {"type": "recent", "timestamp": recent_timestamp}
        ]

        for metric in metrics:
            metrics_storage.append_metric(metric)

        # Get metrics from last 30 days
        recent = metrics_storage.read_recent_metrics(days=30)

        assert len(recent) == 1
        assert recent[0]["type"] == "recent"

    def test_read_recent_metrics_handles_no_timestamp(self, metrics_storage):
        """Test read_recent_metrics skips metrics without timestamp."""
        # Manually write metric without timestamp
        content = '{"type": "no_timestamp", "value": 42}\n'
        metrics_storage.metrics_file.write_text(content)

        recent = metrics_storage.read_recent_metrics(days=30)

        # Should skip metric without timestamp
        assert len(recent) == 0

    def test_read_recent_metrics_handles_invalid_timestamp(self, metrics_storage):
        """Test read_recent_metrics skips metrics with invalid timestamp."""
        metrics = [
            {"type": "valid", "timestamp": datetime.utcnow().isoformat() + "Z"},
            {"type": "invalid", "timestamp": "not-a-date"}
        ]

        for metric in metrics:
            content = json.dumps(metric) + "\n"
            metrics_storage.metrics_file.write_text(
                metrics_storage.metrics_file.read_text() if metrics_storage.metrics_file.exists() else "" + content
            )

        recent = metrics_storage.read_recent_metrics(days=30)

        # Should only get valid metric
        assert len(recent) == 1
        assert recent[0]["type"] == "valid"

    def test_count_metrics_empty(self, metrics_storage):
        """Test count_metrics with no file."""
        count = metrics_storage.count_metrics()

        assert count == 0

    def test_count_metrics_multiple(self, metrics_storage):
        """Test count_metrics with multiple metrics."""
        for i in range(5):
            metrics_storage.append_metric({"type": f"test{i}"})

        count = metrics_storage.count_metrics()

        assert count == 5

    def test_count_metrics_ignores_empty_lines(self, metrics_storage):
        """Test count_metrics ignores empty lines."""
        content = '{"type": "test1"}\n\n\n{"type": "test2"}\n\n'
        metrics_storage.metrics_file.write_text(content)

        count = metrics_storage.count_metrics()

        assert count == 2

    def test_clear_old_metrics_removes_old(self, metrics_storage):
        """Test clear_old_metrics removes old metrics."""
        now = datetime.utcnow()
        old_timestamp = (now - timedelta(days=100)).isoformat() + "Z"
        recent_timestamp = (now - timedelta(days=10)).isoformat() + "Z"

        metrics = [
            {"type": "old1", "timestamp": old_timestamp},
            {"type": "old2", "timestamp": old_timestamp},
            {"type": "recent", "timestamp": recent_timestamp}
        ]

        for metric in metrics:
            metrics_storage.append_metric(metric)

        removed = metrics_storage.clear_old_metrics(retention_days=90)

        assert removed == 2  # 2 old metrics removed

        # Verify only recent remains
        remaining = metrics_storage.read_all_metrics()
        assert len(remaining) == 1
        assert remaining[0]["type"] == "recent"

    def test_clear_old_metrics_clears_all_if_none_recent(self, metrics_storage):
        """Test clear_old_metrics clears entire file if no recent metrics."""
        now = datetime.utcnow()
        old_timestamp = (now - timedelta(days=100)).isoformat() + "Z"

        for i in range(3):
            metrics_storage.append_metric({
                "type": f"old{i}",
                "timestamp": old_timestamp
            })

        removed = metrics_storage.clear_old_metrics(retention_days=90)

        assert removed == 3

        # File should be empty
        assert metrics_storage.count_metrics() == 0

    def test_clear_old_metrics_returns_count(self, metrics_storage):
        """Test clear_old_metrics returns correct count."""
        # Add only recent metrics
        now = datetime.utcnow()
        recent_timestamp = (now - timedelta(days=10)).isoformat() + "Z"

        for i in range(5):
            metrics_storage.append_metric({
                "type": f"recent{i}",
                "timestamp": recent_timestamp
            })

        removed = metrics_storage.clear_old_metrics(retention_days=90)

        assert removed == 0  # No metrics removed

    def test_append_metric_failure_handling(self, capsys):
        """Test append_metric handles write failures gracefully."""
        # Create storage with invalid path
        invalid_path = Path("/invalid/path/metrics.jsonl")
        storage = MetricsStorage(metrics_file=invalid_path)

        metric = {"type": "test"}
        result = storage.append_metric(metric)

        assert result is False

        captured = capsys.readouterr()
        assert "Warning" in captured.out
        # safe_append prints "Failed to append to" message, not "Failed to append metric"
        assert "Failed to append to" in captured.out
