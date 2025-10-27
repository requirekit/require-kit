"""
Integration tests for force-override workflow.

Tests scenarios where force-review triggers override the complexity score,
requiring full review regardless of low/medium complexity.

Test Coverage:
    - Security keyword triggers (passwords, tokens, auth)
    - Schema change triggers (migrations, database changes)
    - Hotfix triggers (production fixes, critical bugs)
    - Multiple simultaneous triggers
    - Override behavior validation

Force Triggers:
    - has_security_keywords: True → Full review required
    - has_schema_changes: True → Full review required
    - is_hotfix: True → Full review required
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
    ForceReviewTrigger,
    EvaluationContext,
    ImplementationPlan
)
from review_router import ReviewRouter


@pytest.mark.integration
class TestForceOverrideWorkflow:
    """Integration tests for force-override workflow."""

    def test_security_keyword_forces_full_review_despite_low_score(
        self,
        force_trigger_security_data,
        router_factory
    ):
        """
        Test that security keywords trigger full review even for simple tasks.

        Security-sensitive changes require human review regardless of complexity
        score to prevent security vulnerabilities.

        GIVEN a simple task (score 2) with security keywords
        WHEN routing decision is made
        THEN full review should be required despite low score
        """
        # Arrange: Low complexity but security trigger
        factor_scores = [
            FactorScore(
                factor_name="File Count",
                score=1,
                max_score=3,
                justification="1 file only"
            ),
            FactorScore(
                factor_name="Pattern Familiarity",
                score=1,
                max_score=3,
                justification="Standard auth pattern"
            )
        ]

        # Despite low score, security trigger forces full review
        complexity_score = ComplexityScore(
            total_score=2,  # Would normally auto-proceed
            factor_scores=factor_scores,
            forced_review_triggers=[ForceReviewTrigger.SECURITY_KEYWORDS],
            review_mode=ReviewMode.FULL_REQUIRED,  # Overridden
            calculation_timestamp=datetime.now()
        )

        plan = Mock(spec=ImplementationPlan)
        plan.files_to_create = force_trigger_security_data['files_to_create']
        plan.has_security_keywords = True  # Trigger condition
        plan.raw_plan = "Update JWT token expiration"

        context = EvaluationContext(
            task_id=force_trigger_security_data['task_id'],
            technology_stack='Python',
            implementation_plan=plan,
            task_metadata={'id': force_trigger_security_data['task_id']}
        )

        # Act
        router = router_factory()
        decision = router.route(complexity_score, context)

        # Assert: Full review required despite low score
        assert decision.action == "review_required", \
            "Security keywords should force review"
        assert decision.auto_approved is False, \
            "Should not be auto-approved due to security"
        assert "Phase 2.6 Checkpoint (Required)" in decision.routing_recommendation, \
            "Should require Phase 2.6 checkpoint"
        assert ForceReviewTrigger.SECURITY_KEYWORDS in complexity_score.forced_review_triggers, \
            "Should flag security trigger"

        # Verify summary mentions security
        assert "security" in decision.summary_message.lower() or \
               "force" in decision.summary_message.lower(), \
            "Summary should mention security trigger"

    def test_schema_changes_force_full_review(
        self,
        force_trigger_schema_data,
        router_factory
    ):
        """
        Test that database schema changes trigger full review.

        Schema changes require careful review to prevent data loss and
        ensure migration safety.

        GIVEN a task with schema changes
        WHEN routing decision is made
        THEN full review should be required
        """
        # Arrange: Medium complexity with schema trigger
        factor_scores = [
            FactorScore(
                factor_name="File Count",
                score=2,
                max_score=3,
                justification="2 files (migration + model)"
            ),
            FactorScore(
                factor_name="Risk Level",
                score=2,
                max_score=4,
                justification="Schema changes require caution"
            )
        ]

        complexity_score = ComplexityScore(
            total_score=4,  # Would normally be quick optional
            factor_scores=factor_scores,
            forced_review_triggers=[ForceReviewTrigger.SCHEMA_CHANGES],
            review_mode=ReviewMode.FULL_REQUIRED,  # Overridden
            calculation_timestamp=datetime.now()
        )

        plan = Mock(spec=ImplementationPlan)
        plan.files_to_create = force_trigger_schema_data['files_to_create']
        plan.has_schema_changes = True  # Trigger condition
        plan.raw_plan = "Add user_roles table migration"

        context = EvaluationContext(
            task_id=force_trigger_schema_data['task_id'],
            technology_stack='Python',
            implementation_plan=plan,
            task_metadata={'id': force_trigger_schema_data['task_id']}
        )

        # Act
        router = router_factory()
        decision = router.route(complexity_score, context)

        # Assert
        assert decision.action == "review_required", \
            "Schema changes should force review"
        assert decision.auto_approved is False
        assert ForceReviewTrigger.SCHEMA_CHANGES in complexity_score.forced_review_triggers
        assert "Required" in decision.routing_recommendation, \
            "Should be required review, not optional"

    def test_hotfix_forces_full_review_regardless_of_simplicity(
        self,
        force_trigger_hotfix_data,
        router_factory
    ):
        """
        Test that production hotfixes require full review.

        Hotfixes are critical and require careful review to prevent
        introducing new issues in production.

        GIVEN a simple hotfix task (score 1)
        WHEN routing decision is made
        THEN full review should be required despite simplicity
        """
        # Arrange: Very simple task but hotfix trigger
        factor_scores = [
            FactorScore(
                factor_name="File Count",
                score=1,
                max_score=3,
                justification="1 file (simple fix)"
            )
        ]

        complexity_score = ComplexityScore(
            total_score=1,  # Would normally auto-proceed
            factor_scores=factor_scores,
            forced_review_triggers=[ForceReviewTrigger.HOTFIX],
            review_mode=ReviewMode.FULL_REQUIRED,  # Overridden
            calculation_timestamp=datetime.now()
        )

        plan = Mock(spec=ImplementationPlan)
        plan.files_to_create = force_trigger_hotfix_data['files_to_create']
        plan.raw_plan = "Fix critical payment processing bug"

        context = EvaluationContext(
            task_id=force_trigger_hotfix_data['task_id'],
            technology_stack='Python',
            implementation_plan=plan,
            task_metadata={
                'id': force_trigger_hotfix_data['task_id'],
                'is_hotfix': True  # Trigger condition
            }
        )

        # Act
        router = router_factory()
        decision = router.route(complexity_score, context)

        # Assert
        assert decision.action == "review_required", \
            "Hotfix should force review"
        assert decision.auto_approved is False, \
            "Hotfixes should never auto-approve"
        assert ForceReviewTrigger.HOTFIX in complexity_score.forced_review_triggers
        assert complexity_score.total_score == 1, \
            "Score should remain 1 (not inflated)"

    def test_multiple_force_triggers_all_recorded(
        self,
        router_factory
    ):
        """
        Test that multiple force triggers are all properly recorded.

        When multiple triggers are present (e.g., security + schema changes),
        all should be documented for audit purposes.

        GIVEN a task with multiple force triggers
        WHEN routing decision is made
        THEN all triggers should be recorded
        """
        # Arrange: Multiple triggers
        factor_scores = [
            FactorScore(
                factor_name="File Count",
                score=2,
                max_score=3,
                justification="2 files"
            )
        ]

        complexity_score = ComplexityScore(
            total_score=2,
            factor_scores=factor_scores,
            forced_review_triggers=[
                ForceReviewTrigger.SECURITY_KEYWORDS,
                ForceReviewTrigger.SCHEMA_CHANGES,
                ForceReviewTrigger.HOTFIX
            ],
            review_mode=ReviewMode.FULL_REQUIRED,
            calculation_timestamp=datetime.now()
        )

        plan = Mock(spec=ImplementationPlan)
        plan.files_to_create = ['migration.sql', 'auth.py']
        plan.has_security_keywords = True
        plan.has_schema_changes = True
        plan.raw_plan = "Critical security patch with schema changes"

        context = EvaluationContext(
            task_id="TASK-MULTI-TRIGGER-001",
            technology_stack='Python',
            implementation_plan=plan,
            task_metadata={
                'id': "TASK-MULTI-TRIGGER-001",
                'is_hotfix': True
            }
        )

        # Act
        router = router_factory()
        decision = router.route(complexity_score, context)

        # Assert: All triggers recorded
        triggers = complexity_score.forced_review_triggers
        assert len(triggers) == 3, \
            "All three triggers should be recorded"
        assert ForceReviewTrigger.SECURITY_KEYWORDS in triggers
        assert ForceReviewTrigger.SCHEMA_CHANGES in triggers
        assert ForceReviewTrigger.HOTFIX in triggers

        # Summary should mention triggers
        summary = decision.summary_message.lower()
        assert "force" in summary or "trigger" in summary, \
            "Summary should mention force triggers"

    @pytest.mark.parametrize("trigger,data_key", [
        (ForceReviewTrigger.SECURITY_KEYWORDS, 'force_trigger_security_data'),
        (ForceReviewTrigger.SCHEMA_CHANGES, 'force_trigger_schema_data'),
        (ForceReviewTrigger.HOTFIX, 'force_trigger_hotfix_data'),
    ])
    def test_each_force_trigger_overrides_auto_proceed(
        self,
        request,
        router_factory,
        trigger,
        data_key
    ):
        """
        Parametrized test: Each force trigger overrides auto-proceed.

        Validates that each individual trigger type properly overrides
        low complexity scores.

        GIVEN each type of force trigger
        WHEN applied to a low-complexity task
        THEN full review should be required
        """
        # Get fixture data by name
        task_data = request.getfixturevalue(data_key)

        # Arrange: Low score with specific trigger
        complexity_score = ComplexityScore(
            total_score=2,  # Would normally auto-proceed
            factor_scores=[],
            forced_review_triggers=[trigger],
            review_mode=ReviewMode.FULL_REQUIRED,
            calculation_timestamp=datetime.now()
        )

        plan = Mock(spec=ImplementationPlan)
        plan.files_to_create = task_data['files_to_create']
        plan.raw_plan = task_data['title']

        context = EvaluationContext(
            task_id=task_data['task_id'],
            technology_stack='Python',
            implementation_plan=plan,
            task_metadata={'id': task_data['task_id']}
        )

        # Act
        router = router_factory()
        decision = router.route(complexity_score, context)

        # Assert
        assert decision.action == "review_required", \
            f"{trigger.value} should force review"
        assert decision.auto_approved is False, \
            f"{trigger.value} should prevent auto-approval"
        assert trigger in complexity_score.forced_review_triggers, \
            f"{trigger.value} should be recorded"
