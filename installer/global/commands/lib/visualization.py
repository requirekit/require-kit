"""
Terminal visualization and formatting module.

This module provides color-coded terminal output for complexity scores,
breakdown results, and task statistics.

Key Features:
- Color-coded complexity indicators (green/yellow/red)
- Formatted task breakdown reports
- Statistics calculations and visualization
- Terminal-friendly output with emoji indicators

Usage:
    from visualization import TerminalFormatter

    formatter = TerminalFormatter()
    formatter.format_complexity_score(complexity_score)
    formatter.format_breakdown_result(breakdown_result)
"""

import logging
from typing import Dict, Any, List, Optional, TYPE_CHECKING
from dataclasses import dataclass

try:
    from .complexity_models import ComplexityScore
except ImportError:
    from complexity_models import ComplexityScore

# Avoid circular import - only import type hints
if TYPE_CHECKING:
    try:
        from .task_breakdown import TaskBreakdownResult
    except ImportError:
        from task_breakdown import TaskBreakdownResult


logger = logging.getLogger(__name__)


class Colors:
    """ANSI color codes for terminal output."""
    RED = "\033[91m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    RESET = "\033[0m"
    GRAY = "\033[90m"


class Emojis:
    """Emoji indicators for visual feedback."""
    GREEN_CIRCLE = "🟢"  # Low complexity
    YELLOW_CIRCLE = "🟡"  # Medium complexity
    RED_CIRCLE = "🔴"  # High complexity
    CHECK = "✅"
    WARNING = "⚠️"
    ERROR = "❌"
    INFO = "ℹ️"
    ROCKET = "🚀"
    CHART = "📊"
    TASK = "📋"
    CLOCK = "⏱️"
    FILES = "📁"
    GEAR = "⚙️"


@dataclass
class ComplexityVisualization:
    """Visual representation of complexity score.

    Attributes:
        color_indicator: Emoji indicator (green/yellow/red circle)
        color_code: ANSI color code
        label: Complexity label (Low/Medium/High/Critical)
        description: Human-readable description
    """
    color_indicator: str
    color_code: str
    label: str
    description: str


class TerminalFormatter:
    """Formats and displays complexity and breakdown information in terminal.

    This formatter provides color-coded, emoji-enhanced output for better
    visual communication of complexity levels and breakdown results.
    """

    def __init__(self, use_color: bool = True, use_emoji: bool = True):
        """Initialize formatter.

        Args:
            use_color: Whether to use ANSI colors (default: True)
            use_emoji: Whether to use emoji indicators (default: True)
        """
        self.use_color = use_color
        self.use_emoji = use_emoji
        logger.info(f"TerminalFormatter initialized (color={use_color}, emoji={use_emoji})")

    def format_complexity_score(self, score: ComplexityScore) -> str:
        """Format complexity score for terminal display.

        Args:
            score: ComplexityScore object

        Returns:
            Formatted string with color and emoji indicators
        """
        viz = self._get_complexity_visualization(score.total_score)

        lines = []

        # Header
        lines.append(self._format_header("Complexity Evaluation"))
        lines.append("")

        # Score line with indicator
        score_line = f"{viz.color_indicator} Complexity Score: {score.total_score}/10 - {viz.label}"
        if self.use_color:
            score_line = f"{viz.color_code}{score_line}{Colors.RESET}"
        lines.append(score_line)
        lines.append("")

        # Factor breakdown
        lines.append(self._format_subheader("Factor Breakdown"))
        for factor_score in score.factor_scores:
            factor_line = self._format_factor_score(factor_score)
            lines.append(factor_line)
        lines.append("")

        # Review mode
        lines.append(self._format_subheader("Review Recommendation"))
        review_line = f"Mode: {score.review_mode.value.upper()}"
        if score.has_forced_triggers:
            review_line += f" (Forced: {', '.join(t.value for t in score.forced_review_triggers)})"
        lines.append(review_line)

        return "\n".join(lines)

    def format_breakdown_result(self, result: Any) -> str:
        """Format breakdown result for terminal display.

        Args:
            result: TaskBreakdownResult object

        Returns:
            Formatted string with breakdown details
        """
        lines = []

        # Header
        lines.append(self._format_header("Task Breakdown Result"))
        lines.append("")

        # Status
        if result.success:
            status_icon = Emojis.CHECK if self.use_emoji else "[OK]"
            status_line = f"{status_icon} Breakdown completed successfully"
            if self.use_color:
                status_line = f"{Colors.GREEN}{status_line}{Colors.RESET}"
        else:
            status_icon = Emojis.ERROR if self.use_emoji else "[ERROR]"
            status_line = f"{status_icon} Breakdown failed"
            if self.use_color:
                status_line = f"{Colors.RED}{status_line}{Colors.RESET}"
        lines.append(status_line)
        lines.append("")

        # Original task
        lines.append(self._format_subheader("Original Task"))
        lines.append(f"ID: {result.original_task.get('id', 'UNKNOWN')}")
        lines.append(f"Title: {result.original_task.get('title', 'N/A')}")
        lines.append(f"Strategy: {result.strategy_used}")
        lines.append(f"Reason: {result.breakdown_reason}")
        lines.append("")

        # Subtasks
        if result.requires_breakdown:
            lines.append(self._format_subheader(f"Generated Subtasks ({result.subtask_count})"))
            for i, subtask in enumerate(result.subtasks, 1):
                lines.append(self._format_subtask(i, subtask))
            lines.append("")

            # Statistics
            lines.append(self._format_subheader("Statistics"))
            stats = result.statistics
            lines.append(f"{Emojis.CHART if self.use_emoji else '[STATS]'} Total subtasks: {stats.get('subtask_count', 0)}")
            lines.append(f"{Emojis.CLOCK if self.use_emoji else '[TIME]'} Estimated time: {stats.get('estimated_total_time', 0)} hours")

            # Complexity distribution
            dist = stats.get('complexity_distribution', {})
            if dist:
                lines.append(f"Complexity distribution:")
                for complexity, count in dist.items():
                    viz = self._get_complexity_visualization_by_label(complexity)
                    lines.append(f"  {viz.color_indicator} {complexity.capitalize()}: {count}")
        else:
            lines.append(self._format_subheader("No Breakdown Required"))
            lines.append(f"{Emojis.INFO if self.use_emoji else '[INFO]'} Task is simple enough to implement as-is")

        # Errors
        if result.errors:
            lines.append("")
            lines.append(self._format_subheader("Errors"))
            for error in result.errors:
                lines.append(f"{Emojis.ERROR if self.use_emoji else '[ERROR]'} {error}")

        return "\n".join(lines)

    def format_statistics(self, stats: Dict[str, Any]) -> str:
        """Format breakdown statistics.

        Args:
            stats: Statistics dictionary

        Returns:
            Formatted statistics string
        """
        lines = []

        lines.append(self._format_header("Breakdown Statistics"))
        lines.append("")

        # Key metrics
        lines.append(f"{Emojis.TASK if self.use_emoji else '[TASKS]'} Total tasks: {stats.get('total_tasks', 0)}")
        lines.append(f"{Emojis.TASK if self.use_emoji else '[SUBTASKS]'} Total subtasks: {stats.get('total_subtasks', 0)}")
        lines.append(f"{Emojis.CLOCK if self.use_emoji else '[TIME]'} Total estimated time: {stats.get('total_hours', 0)} hours")
        lines.append("")

        # Complexity distribution
        if 'complexity_distribution' in stats:
            lines.append(self._format_subheader("Complexity Distribution"))
            dist = stats['complexity_distribution']
            for level, count in dist.items():
                viz = self._get_complexity_visualization_by_label(level)
                percentage = (count / stats['total_tasks']) * 100 if stats['total_tasks'] > 0 else 0
                lines.append(f"{viz.color_indicator} {level.capitalize()}: {count} ({percentage:.1f}%)")
            lines.append("")

        # Average complexity
        avg = stats.get('average_complexity', 0)
        avg_viz = self._get_complexity_visualization(int(avg))
        lines.append(f"Average complexity: {avg:.1f}/10 {avg_viz.color_indicator}")

        return "\n".join(lines)

    def _format_header(self, text: str) -> str:
        """Format a main header.

        Args:
            text: Header text

        Returns:
            Formatted header
        """
        separator = "=" * len(text)
        if self.use_color:
            return f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.RESET}\n{separator}"
        return f"{text}\n{separator}"

    def _format_subheader(self, text: str) -> str:
        """Format a subheader.

        Args:
            text: Subheader text

        Returns:
            Formatted subheader
        """
        if self.use_color:
            return f"{Colors.BOLD}{text}{Colors.RESET}"
        return text

    def _format_factor_score(self, factor_score: Any) -> str:
        """Format a single factor score.

        Args:
            factor_score: FactorScore object

        Returns:
            Formatted factor line
        """
        name = factor_score.factor_name.replace("_", " ").title()
        score = factor_score.score
        max_score = factor_score.max_score
        justification = factor_score.justification

        # Calculate percentage
        percentage = (score / max_score * 100) if max_score > 0 else 0

        # Color based on percentage
        if percentage <= 33:
            color = Colors.GREEN
            indicator = Emojis.GREEN_CIRCLE
        elif percentage <= 66:
            color = Colors.YELLOW
            indicator = Emojis.YELLOW_CIRCLE
        else:
            color = Colors.RED
            indicator = Emojis.RED_CIRCLE

        line = f"  {indicator if self.use_emoji else '•'} {name}: {score}/{max_score}"

        if self.use_color:
            line = f"{color}{line}{Colors.RESET}"

        line += f" - {justification}"

        return line

    def _format_subtask(self, index: int, subtask: Dict[str, Any]) -> str:
        """Format a single subtask.

        Args:
            index: Subtask number
            subtask: Subtask dictionary

        Returns:
            Formatted subtask line
        """
        task_id = subtask.get('id', 'N/A')
        title = subtask.get('title', 'Untitled')
        complexity = subtask.get('complexity', 'medium')
        hours = subtask.get('estimated_hours', 0)

        viz = self._get_complexity_visualization_by_label(complexity)

        line = f"  {index}. {viz.color_indicator} {task_id}: {title}"
        line += f" ({hours}h)"

        return line

    def _get_complexity_visualization(self, score: int) -> ComplexityVisualization:
        """Get visualization for complexity score.

        Args:
            score: Complexity score (1-10)

        Returns:
            ComplexityVisualization object
        """
        if score <= 3:
            return ComplexityVisualization(
                color_indicator=Emojis.GREEN_CIRCLE,
                color_code=Colors.GREEN,
                label="Low",
                description="Simple task, no breakdown needed"
            )
        elif score <= 6:
            return ComplexityVisualization(
                color_indicator=Emojis.YELLOW_CIRCLE,
                color_code=Colors.YELLOW,
                label="Medium",
                description="Moderate complexity, logical breakdown recommended"
            )
        elif score <= 8:
            return ComplexityVisualization(
                color_indicator=Emojis.RED_CIRCLE,
                color_code=Colors.RED,
                label="High",
                description="High complexity, file-based breakdown required"
            )
        else:
            return ComplexityVisualization(
                color_indicator=Emojis.RED_CIRCLE,
                color_code=Colors.RED,
                label="Critical",
                description="Very high complexity, phase-based breakdown required"
            )

    def _get_complexity_visualization_by_label(self, label: str) -> ComplexityVisualization:
        """Get visualization by complexity label.

        Args:
            label: Complexity label (low/medium/high/critical)

        Returns:
            ComplexityVisualization object
        """
        label_lower = label.lower()

        if label_lower in ["low", "simple"]:
            score = 2
        elif label_lower in ["medium", "moderate"]:
            score = 5
        elif label_lower in ["high", "complex"]:
            score = 7
        else:
            score = 9

        return self._get_complexity_visualization(score)
