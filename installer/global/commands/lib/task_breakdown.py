"""
Task breakdown orchestration module.

This module provides the main entry point for automatic task breakdown based on
complexity evaluation. It selects the appropriate breakdown strategy and coordinates
the entire breakdown workflow.

Key Features:
- Integration with existing complexity evaluation (TASK-005/006)
- Automatic breakdown for tasks with complexity >= 7
- Strategy selection based on complexity score
- Duplicate detection across all task directories
- Comprehensive error handling

Usage:
    from task_breakdown import breakdown_feature_tasks

    result = breakdown_feature_tasks(
        feature_data={
            "id": "FEAT-001",
            "title": "User Authentication",
            "requirements": ["REQ-001", "REQ-002"],
            "acceptance_criteria": [...]
        }
    )
"""

import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime

try:
    from .complexity_calculator import ComplexityCalculator
    from .complexity_models import ComplexityScore, EvaluationContext, ImplementationPlan
    from .breakdown_strategies import (
        BreakdownStrategy,
        NoBreakdownStrategy,
        LogicalBreakdownStrategy,
        FileBasedBreakdownStrategy,
        PhaseBasedBreakdownStrategy
    )
    from .duplicate_detector import DuplicateDetector
    from .visualization import TerminalFormatter
except ImportError:
    from complexity_calculator import ComplexityCalculator
    from complexity_models import ComplexityScore, EvaluationContext, ImplementationPlan
    from breakdown_strategies import (
        BreakdownStrategy,
        NoBreakdownStrategy,
        LogicalBreakdownStrategy,
        FileBasedBreakdownStrategy,
        PhaseBasedBreakdownStrategy
    )
    from duplicate_detector import DuplicateDetector
    from visualization import TerminalFormatter


logger = logging.getLogger(__name__)


@dataclass
class TaskBreakdownResult:
    """Result of task breakdown operation.

    Attributes:
        success: Whether breakdown completed successfully
        original_task: Original task data
        subtasks: List of generated subtasks (empty if no breakdown)
        complexity_score: Calculated complexity score
        strategy_used: Name of breakdown strategy used
        breakdown_reason: Human-readable reason for breakdown decision
        statistics: Breakdown statistics (count, estimated time, etc.)
        errors: List of errors encountered (if any)
        timestamp: When breakdown was performed
    """
    success: bool
    original_task: Dict[str, Any]
    subtasks: List[Dict[str, Any]] = field(default_factory=list)
    complexity_score: Optional[ComplexityScore] = None
    strategy_used: str = ""
    breakdown_reason: str = ""
    statistics: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def requires_breakdown(self) -> bool:
        """Check if task required breakdown."""
        return len(self.subtasks) > 0

    @property
    def subtask_count(self) -> int:
        """Number of subtasks generated."""
        return len(self.subtasks)


class TaskBreakdownOrchestrator:
    """Main orchestrator for task breakdown workflow.

    This class coordinates all aspects of task breakdown:
    1. Complexity evaluation using existing modules
    2. Strategy selection based on complexity score
    3. Duplicate detection
    4. Subtask generation
    5. Result formatting and visualization
    """

    # Complexity thresholds for breakdown
    NO_BREAKDOWN_THRESHOLD = 3  # Score 1-3: No breakdown needed
    LOGICAL_BREAKDOWN_THRESHOLD = 6  # Score 4-6: Logical breakdown
    FILE_BASED_THRESHOLD = 8  # Score 7-8: File-based breakdown
    # Score 9-10: Phase-based breakdown

    def __init__(
        self,
        complexity_calculator: Optional[ComplexityCalculator] = None,
        duplicate_detector: Optional[DuplicateDetector] = None,
        formatter: Optional[TerminalFormatter] = None
    ):
        """Initialize orchestrator with dependencies.

        Args:
            complexity_calculator: Calculator for complexity evaluation (default: new instance)
            duplicate_detector: Detector for duplicate tasks (default: new instance)
            formatter: Terminal formatter for visualization (default: new instance)
        """
        self.complexity_calculator = complexity_calculator or ComplexityCalculator()
        self.duplicate_detector = duplicate_detector or DuplicateDetector()
        self.formatter = formatter or TerminalFormatter()

        # Strategy registry
        self.strategies = {
            "none": NoBreakdownStrategy(),
            "logical": LogicalBreakdownStrategy(),
            "file_based": FileBasedBreakdownStrategy(),
            "phase_based": PhaseBasedBreakdownStrategy()
        }

        logger.info("TaskBreakdownOrchestrator initialized")

    def breakdown_task(
        self,
        task_data: Dict[str, Any],
        threshold_override: Optional[int] = None,
        interactive: bool = False
    ) -> TaskBreakdownResult:
        """Break down a task based on complexity evaluation.

        Main workflow:
        1. Parse task data
        2. Evaluate complexity
        3. Select strategy
        4. Check for duplicates
        5. Generate subtasks
        6. Format results

        Args:
            task_data: Task data dictionary with title, requirements, etc.
            threshold_override: Optional custom threshold for breakdown decision
            interactive: Whether to prompt user for confirmation

        Returns:
            TaskBreakdownResult with subtasks and metadata

        Raises:
            ValueError: If task_data is missing required fields
        """
        try:
            logger.info(f"Starting breakdown for task: {task_data.get('id', 'UNKNOWN')}")

            # Step 1: Validate task data
            self._validate_task_data(task_data)

            # Step 2: Create evaluation context
            context = self._create_evaluation_context(task_data)

            # Step 3: Evaluate complexity
            complexity_score = self.complexity_calculator.calculate(context)
            logger.info(
                f"Complexity evaluated: score={complexity_score.total_score}, "
                f"mode={complexity_score.review_mode.value}"
            )

            # Step 4: Select breakdown strategy
            threshold = threshold_override or 7  # Default threshold for auto-breakdown
            strategy = self._select_strategy(complexity_score, threshold)
            logger.info(f"Selected strategy: {strategy.__class__.__name__}")

            # Step 5: Execute breakdown
            subtasks = strategy.breakdown(task_data, complexity_score)

            # Step 6: Check for duplicates
            if subtasks:
                subtasks = self._filter_duplicates(subtasks)

            # Step 7: Build result
            result = TaskBreakdownResult(
                success=True,
                original_task=task_data,
                subtasks=subtasks,
                complexity_score=complexity_score,
                strategy_used=strategy.__class__.__name__,
                breakdown_reason=self._get_breakdown_reason(complexity_score, threshold),
                statistics=self._calculate_statistics(subtasks),
                timestamp=datetime.now()
            )

            logger.info(
                f"Breakdown complete: {result.subtask_count} subtasks generated "
                f"using {result.strategy_used}"
            )

            return result

        except Exception as e:
            logger.error(f"Error during task breakdown: {e}", exc_info=True)
            return TaskBreakdownResult(
                success=False,
                original_task=task_data,
                errors=[str(e)],
                breakdown_reason=f"Breakdown failed: {e}",
                timestamp=datetime.now()
            )

    def _validate_task_data(self, task_data: Dict[str, Any]) -> None:
        """Validate required fields in task data.

        Args:
            task_data: Task data to validate

        Raises:
            ValueError: If required fields are missing
        """
        required_fields = ["id", "title", "feature_id", "epic_id"]
        missing = [f for f in required_fields if f not in task_data]

        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")

    def _create_evaluation_context(self, task_data: Dict[str, Any]) -> EvaluationContext:
        """Create evaluation context from task data.

        Args:
            task_data: Task data dictionary

        Returns:
            EvaluationContext for complexity calculation
        """
        # Create implementation plan from task data
        plan = ImplementationPlan(
            task_id=task_data["id"],
            files_to_create=task_data.get("files", []),
            patterns_used=task_data.get("patterns", []),
            external_dependencies=task_data.get("dependencies", []),
            estimated_loc=task_data.get("estimated_loc"),
            raw_plan=task_data.get("description", "")
        )

        # Create context
        context = EvaluationContext(
            task_id=task_data["id"],
            technology_stack=task_data.get("stack", "unknown"),
            implementation_plan=plan,
            task_metadata={
                "feature_id": task_data.get("feature_id"),
                "epic_id": task_data.get("epic_id"),
                "priority": task_data.get("priority", "medium")
            }
        )

        return context

    def _select_strategy(
        self,
        complexity_score: ComplexityScore,
        threshold: int
    ) -> BreakdownStrategy:
        """Select appropriate breakdown strategy based on complexity.

        Strategy selection logic:
        - Score 1-3: No breakdown (NoBreakdownStrategy)
        - Score 4-6: Logical breakdown (LogicalBreakdownStrategy)
        - Score 7-8: File-based breakdown (FileBasedBreakdownStrategy)
        - Score 9-10: Phase-based breakdown (PhaseBasedBreakdownStrategy)

        Args:
            complexity_score: Calculated complexity score
            threshold: Custom threshold for breakdown decision

        Returns:
            Selected BreakdownStrategy instance
        """
        score = complexity_score.total_score

        if score <= self.NO_BREAKDOWN_THRESHOLD:
            return self.strategies["none"]
        elif score <= self.LOGICAL_BREAKDOWN_THRESHOLD:
            return self.strategies["logical"]
        elif score <= self.FILE_BASED_THRESHOLD:
            return self.strategies["file_based"]
        else:
            return self.strategies["phase_based"]

    def _filter_duplicates(self, subtasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter out duplicate subtasks.

        Args:
            subtasks: List of subtasks to check

        Returns:
            Filtered list with duplicates removed
        """
        filtered = []

        for subtask in subtasks:
            duplicates = self.duplicate_detector.find_duplicates(subtask)
            if not duplicates:
                filtered.append(subtask)
            else:
                logger.warning(
                    f"Skipping duplicate subtask: {subtask['title']} "
                    f"(similar to {duplicates[0]['id']})"
                )

        return filtered

    def _get_breakdown_reason(self, complexity_score: ComplexityScore, threshold: int) -> str:
        """Generate human-readable breakdown reason.

        Args:
            complexity_score: Calculated complexity score
            threshold: Breakdown threshold used

        Returns:
            Explanation string
        """
        score = complexity_score.total_score

        if score < threshold:
            return f"Complexity score ({score}) below threshold ({threshold}) - no breakdown needed"
        elif score <= 6:
            return f"Moderate complexity ({score}) - logical breakdown applied"
        elif score <= 8:
            return f"High complexity ({score}) - file-based breakdown applied"
        else:
            return f"Very high complexity ({score}) - phase-based breakdown applied"

    def _calculate_statistics(self, subtasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate breakdown statistics.

        Args:
            subtasks: Generated subtasks

        Returns:
            Statistics dictionary
        """
        if not subtasks:
            return {
                "subtask_count": 0,
                "estimated_total_time": 0,
                "complexity_distribution": {}
            }

        # Calculate complexity distribution
        complexity_dist = {}
        total_time = 0

        for subtask in subtasks:
            complexity = subtask.get("complexity", "medium")
            complexity_dist[complexity] = complexity_dist.get(complexity, 0) + 1
            total_time += subtask.get("estimated_hours", 4)

        return {
            "subtask_count": len(subtasks),
            "estimated_total_time": total_time,
            "complexity_distribution": complexity_dist,
            "average_complexity": sum(
                {"low": 1, "medium": 2, "high": 3}.get(c, 2) * count
                for c, count in complexity_dist.items()
            ) / len(subtasks) if subtasks else 0
        }


# Public API function
def breakdown_feature_tasks(
    feature_data: Dict[str, Any],
    threshold_override: Optional[int] = None,
    interactive: bool = False
) -> TaskBreakdownResult:
    """Break down feature tasks based on complexity evaluation.

    This is the main entry point for task breakdown. It automatically:
    1. Evaluates complexity for the feature
    2. Selects appropriate breakdown strategy
    3. Generates subtasks if needed
    4. Checks for duplicates
    5. Returns formatted results

    Args:
        feature_data: Feature data with tasks, requirements, etc.
        threshold_override: Optional custom complexity threshold (default: 7)
        interactive: Whether to prompt user for confirmations

    Returns:
        TaskBreakdownResult with subtasks and metadata

    Example:
        >>> result = breakdown_feature_tasks({
        ...     "id": "FEAT-001",
        ...     "title": "User Authentication",
        ...     "tasks": [{
        ...         "id": "TASK-001",
        ...         "title": "Implement auth system",
        ...         "files": ["auth.py", "user.py", "session.py", ...],
        ...         "patterns": ["Strategy", "Repository"],
        ...         "estimated_loc": 500
        ...     }]
        ... })
        >>> print(f"Generated {result.subtask_count} subtasks")
    """
    orchestrator = TaskBreakdownOrchestrator()

    # Process each task in feature
    tasks = feature_data.get("tasks", [])
    all_results = []

    for task in tasks:
        # Merge feature context into task
        task_with_context = {
            **task,
            "feature_id": feature_data["id"],
            "epic_id": feature_data.get("epic_id"),
            "stack": feature_data.get("technology_stack", "unknown")
        }

        result = orchestrator.breakdown_task(
            task_with_context,
            threshold_override=threshold_override,
            interactive=interactive
        )
        all_results.append(result)

    # Aggregate results (stub - would combine multiple task results)
    if all_results:
        return all_results[0]  # Simplified for stub
    else:
        return TaskBreakdownResult(
            success=True,
            original_task=feature_data,
            breakdown_reason="No tasks found in feature",
            timestamp=datetime.now()
        )
