"""
Integration tests for auto-proceed workflow (score 1-3).

Tests the complete workflow for simple tasks that automatically proceed
to Phase 3 without human intervention.

Test Coverage:
    - Router decision making for low complexity scores
    - Display rendering for auto-proceed scenarios
    - Metadata updates and state transitions
    - Force-override scenarios
    - Edge cases (boundary scores, missing data)

Complexity Target: Score 1-3 (auto-proceed mode)
Expected Behavior: Automatic progression to Phase 3, no human checkpoint
"""

import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock
import sys

# Add installer lib to path
installer_lib_path = Path(__file__).parent.parent.parent / "installer" / "global" / "commands" / "lib"
if str(installer_lib_path) not in sys.path:
    sys.path.insert(0, str(installer_lib_path))

from complexity_models import (
    ComplexityScore,
    FactorScore,
    ReviewMode,
    EvaluationContext,
    ImplementationPlan
)
from review_router import ReviewRouter


@pytest.mark.integration
class TestAutoProceedWorkflow:
    """Integration tests for auto-proceed workflow (score 1-3)."""

    def test_simple_task_auto_proceeds_to_phase_3(
        self,
        simple_task_data,
        router_factory
    ):
        """
        Test that simple task (score 1-3) automatically proceeds to Phase 3.

        Workflow:
            1. Calculate complexity score (should be 1-3)
            2. Route decision (should be "proceed")
            3. Verify no human checkpoint triggered
            4. Verify metadata indicates auto-approval

        GIVEN a simple task with low complexity
        WHEN complexity is evaluated and routed
        THEN the task should auto-proceed to Phase 3
        AND no human checkpoint should be required
        """
        # Arrange: Create simple complexity score
        factor_scores = [
            FactorScore(
                factor_name="File Count",
                score=1,
                max_score=3,
                justification="1 file to create (very simple)"
            ),
            FactorScore(
                factor_name="Pattern Familiarity",
                score=1,
                max_score=3,
                justification="Standard validation pattern (familiar)"
            ),
            FactorScore(
                factor_name="Risk Level",
                score=0,
                max_score=4,
                justification="No risk indicators"
            )
        ]

        complexity_score = ComplexityScore(
            total_score=2,  # Auto-proceed threshold (1-3)
            factor_scores=factor_scores,
            forced_review_triggers=[],
            review_mode=ReviewMode.AUTO_PROCEED,
            calculation_timestamp=datetime.now()
        )

        # Create evaluation context
        plan = Mock(spec=ImplementationPlan)
        plan.files_to_create = simple_task_data['files_to_create']
        plan.external_dependencies = simple_task_data['external_dependencies']
        plan.has_security_keywords = simple_task_data['has_security_keywords']
        plan.has_schema_changes = simple_task_data['has_schema_changes']
        plan.raw_plan = "Simple validation fix"

        context = EvaluationContext(
            task_id=simple_task_data['task_id'],
            technology_stack='Python',
            implementation_plan=plan,
            task_metadata={'id': simple_task_data['task_id']}
        )

        # Act: Route the decision
        router = router_factory()
        decision = router.route(complexity_score, context)

        # Assert: Verify auto-proceed behavior
        assert decision.action == "proceed", "Simple task should auto-proceed"
        assert decision.auto_approved is True, "Should be auto-approved"
        assert decision.routing_recommendation == "Phase 3", \
            "Should route directly to Phase 3"
        assert "AUTO-PROCEEDING" in decision.summary_message, \
            "Summary should indicate auto-proceed"
        assert decision.complexity_score.total_score <= 3, \
            "Score should be in auto-proceed range"

    def test_boundary_score_3_still_auto_proceeds(
        self,
        boundary_low_to_medium_data,
        router_factory
    ):
        """
        Test that score exactly at boundary (3) still auto-proceeds.

        Validates boundary condition: score=3 is inclusive in auto-proceed range.

        GIVEN a task with complexity score exactly 3
        WHEN routing decision is made
        THEN the task should auto-proceed (3 is inclusive)
        """
        # Arrange: Create boundary complexity score (exactly 3)
        factor_scores = [
            FactorScore(
                factor_name="File Count",
                score=2,
                max_score=3,
                justification="2 files (low-medium)"
            ),
            FactorScore(
                factor_name="Pattern Familiarity",
                score=1,
                max_score=3,
                justification="Familiar patterns"
            ),
            FactorScore(
                factor_name="Risk Level",
                score=0,
                max_score=4,
                justification="Low risk"
            )
        ]

        complexity_score = ComplexityScore(
            total_score=3,  # Exact boundary
            factor_scores=factor_scores,
            forced_review_triggers=[],
            review_mode=ReviewMode.AUTO_PROCEED,
            calculation_timestamp=datetime.now()
        )

        plan = Mock(spec=ImplementationPlan)
        plan.files_to_create = boundary_low_to_medium_data['files_to_create']
        plan.raw_plan = "Boundary test"

        context = EvaluationContext(
            task_id=boundary_low_to_medium_data['task_id'],
            technology_stack='Python',
            implementation_plan=plan,
            task_metadata={'id': boundary_low_to_medium_data['task_id']}
        )

        # Act
        router = router_factory()
        decision = router.route(complexity_score, context)

        # Assert
        assert decision.action == "proceed", \
            "Score 3 should still auto-proceed (boundary inclusive)"
        assert decision.auto_approved is True
        assert decision.complexity_score.total_score == 3

    def test_auto_proceed_summary_contains_required_info(
        self,
        simple_task_data,
        router_factory
    ):
        """
        Test that auto-proceed summary contains all required information.

        Validates summary message includes:
        - Complexity score
        - Factor breakdown
        - Auto-proceed confirmation
        - Phase 3 routing

        GIVEN a simple task that auto-proceeds
        WHEN summary is generated
        THEN summary should contain all required information
        """
        # Arrange
        factor_scores = [
            FactorScore(
                factor_name="File Count",
                score=1,
                max_score=3,
                justification="1 file"
            )
        ]

        complexity_score = ComplexityScore(
            total_score=1,
            factor_scores=factor_scores,
            forced_review_triggers=[],
            review_mode=ReviewMode.AUTO_PROCEED,
            calculation_timestamp=datetime.now()
        )

        plan = Mock(spec=ImplementationPlan)
        plan.raw_plan = "Test"

        context = EvaluationContext(
            task_id=simple_task_data['task_id'],
            technology_stack='Python',
            implementation_plan=plan,
            task_metadata={'id': simple_task_data['task_id']}
        )

        # Act
        router = router_factory()
        decision = router.route(complexity_score, context)

        # Assert: Verify summary content
        summary = decision.summary_message
        assert simple_task_data['task_id'] in summary, \
            "Summary should contain task ID"
        assert "Score: 1/10" in summary or "score=1" in summary.lower(), \
            "Summary should show complexity score"
        assert "File Count" in summary, \
            "Summary should include factor breakdown"
        assert "AUTO-PROCEED" in summary or "auto-proceeding" in summary.lower(), \
            "Summary should confirm auto-proceed"
        assert "Phase 3" in summary, \
            "Summary should indicate Phase 3 routing"

    def test_metadata_updates_for_auto_proceed(
        self,
        simple_task_data,
        router_factory
    ):
        """
        Test that metadata is properly updated for auto-proceed workflow.

        Validates that decision contains correct metadata for task tracking:
        - Auto-approved flag
        - Complexity score
        - Review mode
        - Timestamp

        GIVEN an auto-proceed decision
        WHEN metadata is extracted
        THEN all required fields should be present
        """
        # Arrange
        complexity_score = ComplexityScore(
            total_score=2,
            factor_scores=[],
            forced_review_triggers=[],
            review_mode=ReviewMode.AUTO_PROCEED,
            calculation_timestamp=datetime.now()
        )

        plan = Mock(spec=ImplementationPlan)
        plan.raw_plan = "Test"

        context = EvaluationContext(
            task_id=simple_task_data['task_id'],
            technology_stack='Python',
            implementation_plan=plan,
            task_metadata={'id': simple_task_data['task_id']}
        )

        # Act
        router = router_factory()
        decision = router.route(complexity_score, context)

        # Assert: Verify metadata
        assert decision.auto_approved is True, \
            "Metadata should indicate auto-approval"
        assert decision.complexity_score is not None, \
            "Metadata should include complexity score"
        assert decision.complexity_score.total_score == 2, \
            "Metadata should have correct score"
        assert decision.timestamp is not None, \
            "Metadata should include timestamp"

    def test_zero_files_task_still_auto_proceeds(
        self,
        edge_case_zero_files_data,
        router_factory
    ):
        """
        Test that task with no files still auto-proceeds if score is low.

        Edge case validation: Research tasks or documentation-only tasks
        with no files should still route correctly based on complexity score.

        GIVEN a task with zero files but low complexity
        WHEN routing decision is made
        THEN the task should auto-proceed based on score
        """
        # Arrange: Zero files but simple task
        factor_scores = [
            FactorScore(
                factor_name="File Count",
                score=0,
                max_score=3,
                justification="0 files (research task)"
            ),
            FactorScore(
                factor_name="Pattern Familiarity",
                score=1,
                max_score=3,
                justification="Documentation task"
            )
        ]

        complexity_score = ComplexityScore(
            total_score=1,
            factor_scores=factor_scores,
            forced_review_triggers=[],
            review_mode=ReviewMode.AUTO_PROCEED,
            calculation_timestamp=datetime.now()
        )

        plan = Mock(spec=ImplementationPlan)
        plan.files_to_create = []  # Zero files
        plan.raw_plan = "Research task"

        context = EvaluationContext(
            task_id=edge_case_zero_files_data['task_id'],
            technology_stack='Python',
            implementation_plan=plan,
            task_metadata={'id': edge_case_zero_files_data['task_id']}
        )

        # Act
        router = router_factory()
        decision = router.route(complexity_score, context)

        # Assert
        assert decision.action == "proceed", \
            "Zero-file task with low complexity should auto-proceed"
        assert decision.auto_approved is True
        assert len(plan.files_to_create) == 0, \
            "Should handle zero files gracefully"

    @pytest.mark.parametrize("score", [1, 2, 3])
    def test_all_auto_proceed_scores_route_correctly(
        self,
        simple_task_data,
        router_factory,
        score
    ):
        """
        Test that all scores in auto-proceed range (1-3) route correctly.

        Parametrized test validating consistent behavior across entire
        auto-proceed score range.

        GIVEN scores 1, 2, and 3
        WHEN routing decisions are made
        THEN all should auto-proceed to Phase 3
        """
        # Arrange
        complexity_score = ComplexityScore(
            total_score=score,
            factor_scores=[],
            forced_review_triggers=[],
            review_mode=ReviewMode.AUTO_PROCEED,
            calculation_timestamp=datetime.now()
        )

        plan = Mock(spec=ImplementationPlan)
        plan.raw_plan = f"Test score {score}"

        context = EvaluationContext(
            task_id=f"TASK-SCORE-{score}",
            technology_stack='Python',
            implementation_plan=plan,
            task_metadata={'id': f"TASK-SCORE-{score}"}
        )

        # Act
        router = router_factory()
        decision = router.route(complexity_score, context)

        # Assert
        assert decision.action == "proceed", \
            f"Score {score} should auto-proceed"
        assert decision.auto_approved is True, \
            f"Score {score} should be auto-approved"
        assert decision.routing_recommendation == "Phase 3", \
            f"Score {score} should route to Phase 3"
