"""
Unit tests for TASK-003E Phase 5 Day 3: Boundary Conditions.

Tests boundary validation for complexity calculation:
- File count boundaries (0, 1, 50, 100+ files)
- Dependency count boundaries (0, 1, 10, 50+ dependencies)
- Complexity score capping at maximum values
- Edge cases for minimum and maximum inputs

This is validation-only testing (no production code changes needed).
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add installer lib to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "installer" / "global" / "commands" / "lib"))

from complexity_calculator import ComplexityCalculator
from complexity_models import ImplementationPlan, EvaluationContext
from complexity_factors import DEFAULT_FACTORS

# Import boundary helpers
sys.path.insert(0, str(Path(__file__).parent.parent / "fixtures"))
from boundary_helpers import (
    minimal_task,
    single_file_task,
    large_task,
    maximum_task,
    boundary_file_count,
    boundary_dependency_count,
    create_task_with_file_count,
    create_task_with_dependency_count,
)


# ============================================================================
# Test File Count Boundaries
# ============================================================================

class TestFileCountBoundaries:
    """Test boundary conditions for file count in complexity calculation."""

    def test_file_count_boundaries(self, boundary_file_count):
        """
        Parametrized test for file count boundaries: 0, 1, 50, 100 files.

        Tests that complexity calculator handles all boundary values:
        - 0 files: Minimum complexity
        - 1 file: Edge case minimum
        - 50 files: High complexity
        - 100 files: Maximum complexity (should cap at max score)
        """
        # Create task with specific file count
        task_data = create_task_with_file_count(boundary_file_count, f"TASK-FILES-{boundary_file_count}")

        # Create ImplementationPlan
        plan = ImplementationPlan(
            task_id=task_data["task_id"],
            files_to_create=task_data["files_to_create"],
            external_dependencies=task_data["external_dependencies"],
            raw_plan=task_data["raw_plan"],
            estimated_loc=task_data["estimated_loc"]
        )

        # Create evaluation context
        context = EvaluationContext(
            task_id=task_data["task_id"],
            technology_stack="python",
            implementation_plan=plan,
            task_metadata={},
            user_flags={}
        )

        # Calculate complexity
        calculator = ComplexityCalculator()
        score = calculator.calculate(context)

        # Verify score is valid
        assert score is not None
        assert 1 <= score.total_score <= 10, f"Score {score.total_score} out of valid range for {boundary_file_count} files"
        assert len(score.factor_scores) > 0, "Should have at least one factor score"

        # Verify score increases with file count (generally)
        # Note: This is not strict since other factors contribute
        if boundary_file_count == 0:
            # 0 files should give low complexity
            assert score.total_score <= 5, "0 files should result in low-medium complexity"
        elif boundary_file_count >= 100:
            # 100+ files should give high complexity (capped)
            # File factor caps at score 3, but total can be higher with other factors
            assert score.total_score >= 3, "100+ files should result in high complexity"

    def test_zero_files_minimum_score(self, minimal_task):
        """Test that 0 files gives minimum complexity score."""
        plan = ImplementationPlan(
            task_id=minimal_task["task_id"],
            files_to_create=minimal_task["files_to_create"],  # 0 files
            external_dependencies=minimal_task["external_dependencies"],
            raw_plan=minimal_task["raw_plan"]
        )

        context = EvaluationContext(
            task_id=minimal_task["task_id"],
            technology_stack="python",
            implementation_plan=plan
        )

        calculator = ComplexityCalculator()
        score = calculator.calculate(context)

        # With 0 files, file factor should contribute minimal score
        # Find file complexity factor score
        file_factor = score.get_factor_score("file_complexity")
        if file_factor:
            assert file_factor.score <= 1, f"0 files should give minimal file complexity, got {file_factor.score}"

        # Total score should be low (1-3 range for auto-proceed)
        assert score.total_score <= 4, f"0 files task should have low total complexity, got {score.total_score}"

    def test_massive_file_count_capped(self, maximum_task):
        """Test that 100+ files caps at maximum score."""
        plan = ImplementationPlan(
            task_id=maximum_task["task_id"],
            files_to_create=maximum_task["files_to_create"],  # 120 files
            external_dependencies=maximum_task["external_dependencies"],
            raw_plan=maximum_task["raw_plan"],
            estimated_loc=maximum_task["estimated_loc"]
        )

        context = EvaluationContext(
            task_id=maximum_task["task_id"],
            technology_stack="python",
            implementation_plan=plan
        )

        calculator = ComplexityCalculator()
        score = calculator.calculate(context)

        # File factor should cap at max score (3 based on complexity_factors.py)
        file_factor = score.get_factor_score("file_complexity")
        if file_factor:
            assert file_factor.score <= file_factor.max_score, \
                f"File factor should not exceed max ({file_factor.max_score}), got {file_factor.score}"
            # With 120 files, should get maximum file complexity score
            assert file_factor.score == file_factor.max_score, \
                f"120 files should result in maximum file factor score"

        # Total score should be capped at 10
        assert score.total_score <= 10, f"Total score should never exceed 10, got {score.total_score}"


# ============================================================================
# Test Dependency Count Boundaries
# ============================================================================

class TestDependencyBoundaries:
    """Test boundary conditions for dependency count in complexity calculation."""

    def test_dependency_boundaries(self, boundary_dependency_count):
        """
        Parametrized test for dependency boundaries: 0, 1, 10, 50 dependencies.

        Tests that complexity calculator handles all dependency boundary values:
        - 0 deps: Independent task
        - 1 dep: Minimal external dependency
        - 10 deps: Medium complexity
        - 50 deps: High complexity
        """
        # Create task with specific dependency count
        task_data = create_task_with_dependency_count(
            boundary_dependency_count,
            f"TASK-DEPS-{boundary_dependency_count}"
        )

        # Create ImplementationPlan
        plan = ImplementationPlan(
            task_id=task_data["task_id"],
            files_to_create=task_data["files_to_create"],
            external_dependencies=task_data["external_dependencies"],
            raw_plan=task_data["raw_plan"]
        )

        # Create evaluation context
        context = EvaluationContext(
            task_id=task_data["task_id"],
            technology_stack="python",
            implementation_plan=plan
        )

        # Calculate complexity
        calculator = ComplexityCalculator()
        score = calculator.calculate(context)

        # Verify score is valid
        assert score is not None
        assert 1 <= score.total_score <= 10, \
            f"Score {score.total_score} out of range for {boundary_dependency_count} deps"
        assert len(score.factor_scores) > 0

        # Verify dependency factor exists and is reasonable
        # Note: Dependency factor may or may not be in DEFAULT_FACTORS
        # This test validates the calculation doesn't crash with any dependency count

    def test_zero_dependencies_independent_task(self, minimal_task):
        """Test that 0 dependencies is valid (independent task)."""
        plan = ImplementationPlan(
            task_id=minimal_task["task_id"],
            files_to_create=["README.md"],
            external_dependencies=[],  # 0 dependencies
            raw_plan=minimal_task["raw_plan"]
        )

        context = EvaluationContext(
            task_id=minimal_task["task_id"],
            technology_stack="python",
            implementation_plan=plan
        )

        calculator = ComplexityCalculator()
        score = calculator.calculate(context)

        # Should calculate successfully
        assert score is not None
        assert score.total_score >= 1

        # Task with 0 dependencies and 1 file should be low complexity
        assert score.total_score <= 5, \
            f"Independent task with 1 file should be low complexity, got {score.total_score}"

    def test_large_dependency_count_handled(self, maximum_task):
        """Test that 50+ dependencies are handled gracefully."""
        plan = ImplementationPlan(
            task_id=maximum_task["task_id"],
            files_to_create=["main.py"],
            external_dependencies=maximum_task["external_dependencies"],  # 60 dependencies
            raw_plan=maximum_task["raw_plan"]
        )

        context = EvaluationContext(
            task_id=maximum_task["task_id"],
            technology_stack="python",
            implementation_plan=plan
        )

        calculator = ComplexityCalculator()
        score = calculator.calculate(context)

        # Should handle large dependency count without crashing
        assert score is not None
        assert 1 <= score.total_score <= 10

        # Verify dependencies are stored in plan (boundary validation)
        assert len(plan.external_dependencies) == 60, \
            "Plan should preserve large dependency count"

        # NOTE: Current implementation doesn't have DependencyComplexityFactor yet
        # (marked as "Future extension (deferred)" in complexity_factors.py)
        # So dependency count doesn't affect score. This test validates that
        # large dependency counts are handled without crashing.


# ============================================================================
# Test Edge Cases
# ============================================================================

class TestBoundaryEdgeCases:
    """Test edge cases at boundaries."""

    def test_single_file_edge_case(self, single_file_task):
        """Test edge case of exactly 1 file."""
        plan = ImplementationPlan(
            task_id=single_file_task["task_id"],
            files_to_create=single_file_task["files_to_create"],
            external_dependencies=[],
            raw_plan=single_file_task["raw_plan"]
        )

        context = EvaluationContext(
            task_id=single_file_task["task_id"],
            technology_stack="python",
            implementation_plan=plan
        )

        calculator = ComplexityCalculator()
        score = calculator.calculate(context)

        # Single file should be low complexity
        assert score.total_score <= 4, \
            f"Single file task should be low complexity, got {score.total_score}"

    def test_boundary_49_vs_50_files(self):
        """Test boundary between 49 and 50 files (potential threshold)."""
        # Create two tasks: 49 files and 50 files
        task_49 = create_task_with_file_count(49, "TASK-49")
        task_50 = create_task_with_file_count(50, "TASK-50")

        plan_49 = ImplementationPlan(
            task_id=task_49["task_id"],
            files_to_create=task_49["files_to_create"],
            external_dependencies=[],
            raw_plan=task_49["raw_plan"]
        )

        plan_50 = ImplementationPlan(
            task_id=task_50["task_id"],
            files_to_create=task_50["files_to_create"],
            external_dependencies=[],
            raw_plan=task_50["raw_plan"]
        )

        context_49 = EvaluationContext(
            task_id=task_49["task_id"],
            technology_stack="python",
            implementation_plan=plan_49
        )

        context_50 = EvaluationContext(
            task_id=task_50["task_id"],
            technology_stack="python",
            implementation_plan=plan_50
        )

        calculator = ComplexityCalculator()
        score_49 = calculator.calculate(context_49)
        score_50 = calculator.calculate(context_50)

        # Both should be valid
        assert score_49.total_score >= 1
        assert score_50.total_score >= 1

        # 50 files should have equal or higher complexity than 49
        # (or both hit the same cap)
        file_factor_49 = score_49.get_factor_score("file_complexity")
        file_factor_50 = score_50.get_factor_score("file_complexity")

        if file_factor_49 and file_factor_50:
            assert file_factor_50.score >= file_factor_49.score, \
                "50 files should have >= complexity than 49 files"

    def test_boundary_99_vs_100_files(self):
        """Test boundary at 100 files where capping may occur."""
        task_99 = create_task_with_file_count(99, "TASK-99")
        task_100 = create_task_with_file_count(100, "TASK-100")

        plan_99 = ImplementationPlan(
            task_id=task_99["task_id"],
            files_to_create=task_99["files_to_create"],
            external_dependencies=[],
            raw_plan=task_99["raw_plan"]
        )

        plan_100 = ImplementationPlan(
            task_id=task_100["task_id"],
            files_to_create=task_100["files_to_create"],
            external_dependencies=[],
            raw_plan=task_100["raw_plan"]
        )

        context_99 = EvaluationContext(
            task_id=task_99["task_id"],
            technology_stack="python",
            implementation_plan=plan_99
        )

        context_100 = EvaluationContext(
            task_id=task_100["task_id"],
            technology_stack="python",
            implementation_plan=plan_100
        )

        calculator = ComplexityCalculator()
        score_99 = calculator.calculate(context_99)
        score_100 = calculator.calculate(context_100)

        # Both should hit or be near the file complexity cap
        file_factor_99 = score_99.get_factor_score("file_complexity")
        file_factor_100 = score_100.get_factor_score("file_complexity")

        if file_factor_99 and file_factor_100:
            # Both should be at or near max
            assert file_factor_99.score >= file_factor_99.max_score - 1, \
                "99 files should be near maximum file complexity"
            assert file_factor_100.score == file_factor_100.max_score, \
                "100 files should be at maximum file complexity"
