"""
Task splitting advisor based on complexity scores.

This module recommends task splitting strategies when complexity scores
indicate a task is too large to implement effectively in a single unit.
"""

import logging
import sys
from pathlib import Path
from typing import Optional, List

# Handle imports for both direct execution and import as module
try:
    from .complexity_models import ComplexityScore
    from .split_models import SplitRecommendation, SubtaskSuggestion
except ImportError:
    # Add lib directory to path if not already there
    lib_dir = Path(__file__).parent
    if str(lib_dir) not in sys.path:
        sys.path.insert(0, str(lib_dir))

    from complexity_models import ComplexityScore
    from split_models import SplitRecommendation, SubtaskSuggestion


logger = logging.getLogger(__name__)


class TaskSplitAdvisor:
    """Recommends task splitting based on complexity score.

    Uses simple heuristic strategies to suggest how to decompose complex
    tasks into smaller, more manageable subtasks.

    Attributes:
        split_threshold: Complexity score threshold for recommending splits (default: 7)
        max_splits: Maximum number of subtasks to recommend (default: 4)
    """

    # Split thresholds
    DEFAULT_SPLIT_THRESHOLD = 7  # Score >= 7 triggers split recommendation
    DEFAULT_MAX_SPLITS = 4  # Maximum subtasks to recommend

    # Split count by score ranges
    SPLIT_COUNT_MAP = {
        (7, 8): 2,  # Score 7-8: Split into 2-3 tasks
        (9, 10): 3,  # Score 9-10: Split into 3-4 tasks
    }

    def __init__(self, split_threshold: int = DEFAULT_SPLIT_THRESHOLD, max_splits: int = DEFAULT_MAX_SPLITS):
        """Initialize split advisor.

        Args:
            split_threshold: Minimum complexity score to recommend splitting
            max_splits: Maximum number of subtasks to recommend
        """
        self.split_threshold = split_threshold
        self.max_splits = max_splits
        logger.info(f"TaskSplitAdvisor initialized (threshold={split_threshold}, max={max_splits})")

    def recommend_split(
        self,
        complexity_score: ComplexityScore,
        requirements_text: str
    ) -> Optional[SplitRecommendation]:
        """Generate split recommendation if complexity threshold exceeded.

        Args:
            complexity_score: Complexity score from TASK-003A calculator
            requirements_text: Original requirements text

        Returns:
            SplitRecommendation if splitting recommended, None otherwise
        """
        score = complexity_score.total_score

        # Check threshold
        if score < self.split_threshold:
            logger.info(f"Score {score} below threshold {self.split_threshold}, no split needed")
            return None

        logger.info(f"Score {score} >= threshold {self.split_threshold}, generating split recommendation")

        # Determine split count
        split_count = self._determine_split_count(score)

        # Choose split strategy based on complexity factors
        strategy = self._choose_split_strategy(complexity_score)

        # Generate split suggestions
        splits = self._generate_split_suggestions(
            complexity_score,
            requirements_text,
            strategy,
            split_count
        )

        # Build reasoning
        reasoning = self._build_reasoning(complexity_score, strategy, split_count)

        return SplitRecommendation(
            should_split=True,
            recommended_task_count=split_count,
            split_strategy=strategy,
            suggested_splits=splits,
            reasoning=reasoning,
            complexity_breakdown=complexity_score
        )

    def _determine_split_count(self, score: int) -> int:
        """Determine number of subtasks based on complexity score.

        Args:
            score: Complexity score (1-10)

        Returns:
            Recommended number of subtasks (2-4)
        """
        for (min_score, max_score), count in self.SPLIT_COUNT_MAP.items():
            if min_score <= score <= max_score:
                return min(count + 1, self.max_splits)  # Add 1 for range flexibility

        # Default for extreme scores
        return min(4, self.max_splits)

    def _choose_split_strategy(self, complexity_score: ComplexityScore) -> str:
        """Choose appropriate split strategy based on complexity factors.

        Strategies:
        - "vertical": Split by feature/user story (most common)
        - "horizontal": Split by architectural layer (API, logic, data)
        - "by-risk": Split by risk level (isolate high-risk components)

        Args:
            complexity_score: Complexity score with factor breakdown

        Returns:
            Strategy name
        """
        # Check if high-risk factors present
        risk_factor = complexity_score.get_factor_score("risk_level")
        if risk_factor and risk_factor.score >= 2:
            logger.debug("Choosing by-risk strategy due to high risk score")
            return "by-risk"

        # Check if pattern complexity is high
        pattern_factor = complexity_score.get_factor_score("pattern_familiarity")
        if pattern_factor and pattern_factor.score >= 1.5:
            logger.debug("Choosing horizontal strategy due to pattern complexity")
            return "horizontal"

        # Default to vertical splits (by feature)
        logger.debug("Choosing vertical strategy (default)")
        return "vertical"

    def _generate_split_suggestions(
        self,
        complexity_score: ComplexityScore,
        requirements_text: str,
        strategy: str,
        split_count: int
    ) -> List[SubtaskSuggestion]:
        """Generate specific subtask suggestions based on strategy.

        Args:
            complexity_score: Complexity score
            requirements_text: Original requirements
            strategy: Split strategy to use
            split_count: Number of subtasks to create

        Returns:
            List of SubtaskSuggestion objects
        """
        if strategy == "vertical":
            return self._suggest_vertical_splits(requirements_text, split_count)
        elif strategy == "horizontal":
            return self._suggest_horizontal_splits(requirements_text, split_count)
        elif strategy == "by-risk":
            return self._suggest_risk_based_splits(complexity_score, requirements_text, split_count)
        else:
            # Fallback to vertical
            return self._suggest_vertical_splits(requirements_text, split_count)

    def _suggest_vertical_splits(self, text: str, count: int) -> List[SubtaskSuggestion]:
        """Suggest vertical splits by feature/user story.

        Vertical splits separate by business capability or user story.

        Args:
            text: Requirements text
            count: Number of subtasks

        Returns:
            List of subtask suggestions
        """
        # Detect potential feature boundaries from requirements
        text_lower = text.lower()
        suggestions = []

        # Common feature boundaries
        feature_keywords = {
            "authentication": "Implement authentication system",
            "authorization": "Implement authorization and permissions",
            "user": "Implement user management",
            "data": "Implement data layer and persistence",
            "api": "Implement API endpoints",
            "ui": "Implement user interface components",
            "validation": "Implement input validation",
            "testing": "Implement test suite"
        }

        # Find matching features
        found_features = [
            (keyword, title) for keyword, title in feature_keywords.items()
            if keyword in text_lower
        ]

        # Generate suggestions from found features
        for i, (keyword, title) in enumerate(found_features[:count]):
            suggestions.append(SubtaskSuggestion(
                title=title,
                description=f"Focus on {keyword}-related functionality",
                estimated_complexity=complexity_score_estimate(i, count),
                dependencies=get_dependencies(i, found_features)
            ))

        # Fill remaining slots with generic splits if needed
        while len(suggestions) < count:
            phase = len(suggestions) + 1
            suggestions.append(SubtaskSuggestion(
                title=f"Implement phase {phase} functionality",
                description=f"Phase {phase} of incremental implementation",
                estimated_complexity=5,
                dependencies=[]
            ))

        return suggestions[:count]

    def _suggest_horizontal_splits(self, text: str, count: int) -> List[SubtaskSuggestion]:
        """Suggest horizontal splits by architectural layer.

        Horizontal splits separate by technical layer (API, business logic, data, UI).

        Args:
            text: Requirements text
            count: Number of subtasks

        Returns:
            List of subtask suggestions
        """
        # Common layer splits
        layers = [
            ("Data Layer", "Implement data models, repositories, and database schema", 5, []),
            ("Business Logic", "Implement core business logic and services", 6, ["Data Layer"]),
            ("API Layer", "Implement REST API endpoints and controllers", 5, ["Business Logic"]),
            ("UI Layer", "Implement user interface components", 5, ["API Layer"])
        ]

        # Select layers based on requirements content
        text_lower = text.lower()
        selected_layers = []

        for title, desc, complexity, deps in layers:
            # Check if layer is relevant to requirements
            if any(keyword in text_lower for keyword in title.lower().split()):
                selected_layers.append(SubtaskSuggestion(
                    title=title,
                    description=desc,
                    estimated_complexity=complexity,
                    dependencies=deps
                ))

        # Return requested count (or all if less than count)
        return selected_layers[:count] if len(selected_layers) >= count else selected_layers

    def _suggest_risk_based_splits(
        self,
        complexity_score: ComplexityScore,
        text: str,
        count: int
    ) -> List[SubtaskSuggestion]:
        """Suggest risk-based splits to isolate high-risk components.

        Risk-based splits separate high-risk functionality (security, data integrity)
        from standard functionality.

        Args:
            complexity_score: Complexity score with risk indicators
            text: Requirements text
            count: Number of subtasks

        Returns:
            List of subtask suggestions
        """
        suggestions = []
        text_lower = text.lower()

        # High-risk components to isolate
        risk_components = []

        if any(keyword in text_lower for keyword in ["auth", "security", "password", "token"]):
            risk_components.append(SubtaskSuggestion(
                title="Implement security and authentication",
                description="Handle authentication, authorization, and security-critical functionality",
                estimated_complexity=7,
                dependencies=[]
            ))

        if any(keyword in text_lower for keyword in ["database", "migration", "schema"]):
            risk_components.append(SubtaskSuggestion(
                title="Implement data schema and migrations",
                description="Handle database schema, migrations, and data integrity",
                estimated_complexity=6,
                dependencies=[]
            ))

        if any(keyword in text_lower for keyword in ["api", "integration", "external"]):
            risk_components.append(SubtaskSuggestion(
                title="Implement external integrations",
                description="Handle third-party API integrations and external dependencies",
                estimated_complexity=6,
                dependencies=[]
            ))

        # Add high-risk components
        suggestions.extend(risk_components[:count - 1])

        # Add standard functionality task
        if len(suggestions) < count:
            suggestions.append(SubtaskSuggestion(
                title="Implement core functionality",
                description="Standard business logic and features",
                estimated_complexity=5,
                dependencies=[s.title for s in suggestions]
            ))

        return suggestions[:count]

    def _build_reasoning(self, complexity_score: ComplexityScore, strategy: str, count: int) -> str:
        """Build human-readable reasoning for split recommendation.

        Args:
            complexity_score: Complexity score
            strategy: Split strategy used
            count: Number of recommended subtasks

        Returns:
            Reasoning text
        """
        score = complexity_score.total_score
        mode = complexity_score.review_mode.value

        reasoning_parts = [
            f"Complexity score of {score}/10 indicates this task is too large for a single implementation.",
            f"Review mode: {mode}.",
            f"Recommended approach: Split into {count} subtasks using {strategy} strategy."
        ]

        # Add factor-specific reasoning
        for factor_score in complexity_score.factor_scores:
            if factor_score.score > factor_score.max_score * 0.7:  # High score
                reasoning_parts.append(f"{factor_score.factor_name}: {factor_score.justification}")

        # Add trigger-specific reasoning
        if complexity_score.forced_review_triggers:
            triggers = ", ".join(t.value for t in complexity_score.forced_review_triggers)
            reasoning_parts.append(f"Force-review triggers detected: {triggers}")

        return " ".join(reasoning_parts)


# Helper functions

def complexity_score_estimate(index: int, total: int) -> int:
    """Estimate complexity for a subtask based on position.

    Args:
        index: Position in split sequence (0-indexed)
        total: Total number of splits

    Returns:
        Estimated complexity score (4-6 range for subtasks)
    """
    # Earlier tasks slightly more complex (setup, infrastructure)
    # Later tasks simpler (building on established patterns)
    if index == 0:
        return 6
    elif index < total - 1:
        return 5
    else:
        return 4


def get_dependencies(index: int, features: List[tuple]) -> List[str]:
    """Get dependencies for a subtask based on position.

    Args:
        index: Position in split sequence
        features: List of (keyword, title) tuples

    Returns:
        List of dependency task titles
    """
    # Simple linear dependency: each task depends on previous one
    if index == 0:
        return []
    else:
        return [features[index - 1][1]]
