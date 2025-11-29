"""Terminal-based dashboard for plan review metrics."""
from collections import defaultdict
from datetime import datetime
from typing import Dict, Any, List, Optional, Literal

from .metrics_storage import MetricsStorage
from ..config import PlanReviewConfig


class PlanReviewDashboard:
    """
    Terminal-based ASCII dashboard for visualizing metrics.

    Provides simple bar charts and summary statistics.
    """

    def __init__(self, storage: Optional[MetricsStorage] = None, config: Optional[PlanReviewConfig] = None):
        """
        Initialize dashboard.

        Args:
            storage: Metrics storage instance (default: creates new)
            config: Configuration instance (default: singleton)
        """
        self.storage = storage or MetricsStorage()
        self.config = config or PlanReviewConfig()

    def render(
        self,
        days: int = 30,
        format: Literal["terminal"] = "terminal"
    ) -> str:
        """
        Render dashboard in specified format.

        Args:
            days: Number of days to analyze
            format: Output format (terminal only for MVP)

        Returns:
            Rendered dashboard as string
        """
        if format != "terminal":
            raise ValueError("Only 'terminal' format supported in MVP")

        metrics = self.storage.read_recent_metrics(days)
        summary = self._aggregate_metrics(metrics)

        return self._render_terminal(summary, days)

    def _aggregate_metrics(self, metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate metrics into summary statistics.

        Args:
            metrics: List of metric dictionaries

        Returns:
            Aggregated summary
        """
        summary = {
            'total_reviews': 0,
            'decisions': defaultdict(int),
            'complexity_distribution': defaultdict(int),
            'avg_architectural_score': 0.0,
            'avg_complexity_score': 0.0,
            'avg_duration': 0.0,
            'forced_reviews': 0,
            'human_overrides': 0,
            'by_stack': defaultdict(lambda: {'count': 0, 'avg_score': 0.0}),
            'outcomes': defaultdict(int)
        }

        architectural_scores = []
        complexity_scores = []
        durations = []

        for metric in metrics:
            metric_type = metric.get('type')

            if metric_type == 'decision':
                summary['total_reviews'] += 1
                decision = metric.get('decision', 'unknown')
                summary['decisions'][decision] += 1

                arch_score = metric.get('architectural_score', 0)
                architectural_scores.append(arch_score)

                complexity = metric.get('complexity_score', 0)
                complexity_scores.append(complexity)

                # Complexity distribution buckets
                if complexity < 10:
                    bucket = '0-9'
                elif complexity < 20:
                    bucket = '10-19'
                elif complexity < 30:
                    bucket = '20-29'
                elif complexity < 40:
                    bucket = '30-39'
                else:
                    bucket = '40+'
                summary['complexity_distribution'][bucket] += 1

                if metric.get('forced', False):
                    summary['forced_reviews'] += 1

                # By stack
                stack = metric.get('stack', 'unknown')
                summary['by_stack'][stack]['count'] += 1
                summary['by_stack'][stack]['avg_score'] += arch_score

            elif metric_type == 'outcome':
                duration = metric.get('duration_seconds', 0)
                durations.append(duration)

                if metric.get('human_override', False):
                    summary['human_overrides'] += 1

                final_status = metric.get('final_status', 'unknown')
                summary['outcomes'][final_status] += 1

        # Calculate averages
        if architectural_scores:
            summary['avg_architectural_score'] = sum(architectural_scores) / len(architectural_scores)

        if complexity_scores:
            summary['avg_complexity_score'] = sum(complexity_scores) / len(complexity_scores)

        if durations:
            summary['avg_duration'] = sum(durations) / len(durations)

        # Calculate stack averages
        for stack_data in summary['by_stack'].values():
            if stack_data['count'] > 0:
                stack_data['avg_score'] /= stack_data['count']

        return summary

    def _render_terminal(self, summary: Dict[str, Any], days: int) -> str:
        """
        Render dashboard as terminal ASCII art.

        Args:
            summary: Aggregated metrics summary
            days: Number of days analyzed

        Returns:
            Terminal-formatted dashboard
        """
        lines = []

        # Header
        lines.append("=" * 80)
        lines.append(f"Plan Review Metrics Dashboard (Last {days} Days)")
        lines.append("=" * 80)
        lines.append("")

        # Overview
        lines.append("OVERVIEW")
        lines.append("-" * 80)
        lines.append(f"Total Reviews:           {summary['total_reviews']}")
        lines.append(f"Forced Reviews:          {summary['forced_reviews']}")
        lines.append(f"Human Overrides:         {summary['human_overrides']}")
        lines.append(f"Avg Architectural Score: {summary['avg_architectural_score']:.1f}/100")
        lines.append(f"Avg Complexity Score:    {summary['avg_complexity_score']:.1f}")
        lines.append(f"Avg Review Duration:     {summary['avg_duration']:.1f}s")
        lines.append("")

        # Decisions breakdown
        lines.append("DECISIONS")
        lines.append("-" * 80)
        if summary['decisions']:
            max_count = max(summary['decisions'].values())
            for decision, count in sorted(summary['decisions'].items()):
                percentage = (count / summary['total_reviews'] * 100) if summary['total_reviews'] > 0 else 0
                bar = self._render_bar(count, max_count, width=40)
                lines.append(f"{decision:30s} {bar} {count:3d} ({percentage:5.1f}%)")
        else:
            lines.append("No decisions recorded")
        lines.append("")

        # Complexity distribution
        lines.append("COMPLEXITY DISTRIBUTION")
        lines.append("-" * 80)
        if summary['complexity_distribution']:
            # Sort by bucket order
            bucket_order = ['0-9', '10-19', '20-29', '30-39', '40+']
            max_count = max(summary['complexity_distribution'].values())
            for bucket in bucket_order:
                count = summary['complexity_distribution'].get(bucket, 0)
                if count > 0 or bucket in summary['complexity_distribution']:
                    bar = self._render_bar(count, max_count, width=40)
                    lines.append(f"{bucket:10s} {bar} {count:3d}")
        else:
            lines.append("No complexity data recorded")
        lines.append("")

        # By stack
        if summary['by_stack']:
            lines.append("BY TECHNOLOGY STACK")
            lines.append("-" * 80)
            for stack, data in sorted(summary['by_stack'].items()):
                # Defensive: ensure stack, count, and avg_score are safe
                stack_name = str(stack) if stack is not None else "unknown"
                count = data.get('count', 0) if isinstance(data, dict) else 0
                avg_score = data.get('avg_score') if isinstance(data, dict) else None

                # Format safely
                if avg_score is not None and isinstance(avg_score, (int, float)) and avg_score != 0:
                    try:
                        score_str = f"{float(avg_score):.1f}/100"
                    except (TypeError, ValueError):
                        score_str = "N/A"
                else:
                    score_str = "N/A"

                lines.append(f"{stack_name:15s} Count: {count:3d}  Avg Score: {score_str}")
            lines.append("")

        # Outcomes
        if summary['outcomes']:
            lines.append("OUTCOMES")
            lines.append("-" * 80)
            max_count = max(summary['outcomes'].values()) if summary['outcomes'] else 1
            for outcome, count in sorted(summary['outcomes'].items()):
                bar = self._render_bar(count, max_count, width=40)
                lines.append(f"{outcome:15s} {bar} {count:3d}")
            lines.append("")

        lines.append("=" * 80)

        return '\n'.join(lines)

    def _render_bar(self, value: int, max_value: int, width: int = 40) -> str:
        """
        Render simple ASCII bar chart.

        Args:
            value: Current value
            max_value: Maximum value for scaling
            width: Bar width in characters

        Returns:
            ASCII bar string
        """
        if max_value == 0:
            return '█' * 0

        filled = int((value / max_value) * width)
        filled = min(filled, width)  # Ensure we don't exceed width

        # Use Unicode block characters for bars
        return '█' * filled + '░' * (width - filled)

    def print_dashboard(self, days: int = 30) -> None:
        """
        Print dashboard to console.

        Args:
            days: Number of days to analyze
        """
        dashboard = self.render(days=days)
        print(dashboard)
