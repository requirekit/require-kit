"""JSONL-based metrics storage with atomic writes."""
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional

from ..utils import FileOperations, PathResolver


class MetricsStorage:
    """Handles persistent storage of metrics in JSONL format."""

    def __init__(self, metrics_file: Optional[Path] = None):
        """
        Initialize metrics storage.

        Args:
            metrics_file: Path to metrics file (default: from PathResolver)
        """
        self.metrics_file = metrics_file or PathResolver.get_metrics_file()
        self._ensure_storage()

    def _ensure_storage(self) -> None:
        """Ensure metrics directory and .gitignore exist."""
        metrics_dir = self.metrics_file.parent

        # Create directory
        FileOperations.ensure_directory(metrics_dir)

        # Create .gitignore if it doesn't exist
        gitignore_path = metrics_dir / '.gitignore'
        if not gitignore_path.exists():
            gitignore_content = "# Ignore metrics data files\n*.jsonl\n*.json\n"
            FileOperations.atomic_write(gitignore_path, gitignore_content)

    def append_metric(self, metric: Dict[str, Any]) -> bool:
        """
        Append metric to JSONL file.

        Args:
            metric: Metric dictionary to append

        Returns:
            True if successful, False otherwise
        """
        # Add timestamp if not present
        if 'timestamp' not in metric:
            metric['timestamp'] = datetime.utcnow().isoformat() + 'Z'

        # Serialize to JSON line
        try:
            json_line = json.dumps(metric, ensure_ascii=False) + '\n'
            return FileOperations.safe_append(self.metrics_file, json_line)
        except Exception as e:
            print(f"Warning: Failed to append metric: {e}")
            return False

    def read_all_metrics(self) -> List[Dict[str, Any]]:
        """
        Read all metrics from file.

        Returns:
            List of metric dictionaries
        """
        if not self.metrics_file.exists():
            return []

        metrics = []
        content = FileOperations.safe_read(self.metrics_file)

        if not content:
            return []

        for line_num, line in enumerate(content.strip().split('\n'), 1):
            if not line.strip():
                continue

            try:
                metric = json.loads(line)
                metrics.append(metric)
            except json.JSONDecodeError as e:
                # Skip corrupted lines with detailed logging (TASK-003E Phase 5 Day 2)
                print(f"Warning: Skipping corrupted metric at line {line_num}: {e}")
                print(f"         Line content: {line[:80]}{'...' if len(line) > 80 else ''}")
                continue

        return metrics

    def read_recent_metrics(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Read metrics from the last N days.

        Args:
            days: Number of days to look back

        Returns:
            List of recent metric dictionaries
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        all_metrics = self.read_all_metrics()

        recent_metrics = []
        for metric in all_metrics:
            try:
                timestamp_str = metric.get('timestamp', '')
                # Handle both with and without 'Z' suffix
                timestamp_str = timestamp_str.rstrip('Z')
                metric_date = datetime.fromisoformat(timestamp_str)

                if metric_date >= cutoff_date:
                    recent_metrics.append(metric)
            except (ValueError, TypeError):
                # Skip metrics with invalid timestamps
                continue

        return recent_metrics

    def count_metrics(self) -> int:
        """
        Count total number of metrics.

        Returns:
            Total metric count
        """
        if not self.metrics_file.exists():
            return 0

        content = FileOperations.safe_read(self.metrics_file)
        if not content:
            return 0

        return len([line for line in content.strip().split('\n') if line.strip()])

    def clear_old_metrics(self, retention_days: int) -> int:
        """
        Clear metrics older than retention period.

        Args:
            retention_days: Number of days to retain

        Returns:
            Number of metrics removed
        """
        recent_metrics = self.read_recent_metrics(retention_days)
        original_count = self.count_metrics()

        if not recent_metrics:
            # Clear entire file
            FileOperations.atomic_write(self.metrics_file, '')
            return original_count

        # Rewrite file with only recent metrics
        lines = []
        for metric in recent_metrics:
            try:
                line = json.dumps(metric, ensure_ascii=False) + '\n'
                lines.append(line)
            except Exception:
                continue

        content = ''.join(lines)
        FileOperations.atomic_write(self.metrics_file, content)

        return original_count - len(recent_metrics)
