"""
Data models for task splitting recommendations.

This module provides Pydantic models for task splitting recommendations
generated during upfront complexity evaluation.
"""

from dataclasses import dataclass, field
import sys
from pathlib import Path
from typing import List, Dict, Any

# Handle imports for both direct execution and import as module
try:
    from .complexity_models import ComplexityScore
except ImportError:
    # Add lib directory to path if not already there
    lib_dir = Path(__file__).parent
    if str(lib_dir) not in sys.path:
        sys.path.insert(0, str(lib_dir))

    from complexity_models import ComplexityScore


@dataclass(frozen=True)
class SubtaskSuggestion:
    """Suggested subtask in a split recommendation.

    Attributes:
        title: Suggested task title
        description: Brief description of subtask scope
        estimated_complexity: Estimated complexity score (1-10)
        dependencies: List of other subtask titles this depends on
    """
    title: str
    description: str
    estimated_complexity: int
    dependencies: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "title": self.title,
            "description": self.description,
            "estimated_complexity": self.estimated_complexity,
            "dependencies": self.dependencies
        }


@dataclass(frozen=True)
class SplitRecommendation:
    """Task splitting recommendation based on complexity analysis.

    Attributes:
        should_split: Whether task splitting is recommended
        recommended_task_count: Number of suggested subtasks (2-4)
        split_strategy: Strategy used ("vertical", "horizontal", "by-risk")
        suggested_splits: List of subtask suggestions with details
        reasoning: Human-readable explanation of recommendation
        complexity_breakdown: Original complexity score that triggered split
    """
    should_split: bool
    recommended_task_count: int
    split_strategy: str
    suggested_splits: List[SubtaskSuggestion]
    reasoning: str
    complexity_breakdown: ComplexityScore

    @property
    def is_critical_split(self) -> bool:
        """Check if split is critical (complexity score >= 9).

        Critical splits indicate tasks that MUST be split to be manageable.
        """
        return self.complexity_breakdown.total_score >= 9

    @property
    def split_urgency(self) -> str:
        """Get urgency level of split recommendation.

        Returns:
            "critical" (score 9-10), "recommended" (score 7-8), "optional" (score < 7)
        """
        score = self.complexity_breakdown.total_score
        if score >= 9:
            return "critical"
        elif score >= 7:
            return "recommended"
        else:
            return "optional"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization.

        Returns:
            Dictionary representation suitable for JSON output
        """
        return {
            "should_split": self.should_split,
            "recommended_task_count": self.recommended_task_count,
            "split_strategy": self.split_strategy,
            "suggested_splits": [s.to_dict() for s in self.suggested_splits],
            "reasoning": self.reasoning,
            "split_urgency": self.split_urgency,
            "is_critical": self.is_critical_split,
            "complexity_score": self.complexity_breakdown.total_score,
            "review_mode": self.complexity_breakdown.review_mode.value
        }
