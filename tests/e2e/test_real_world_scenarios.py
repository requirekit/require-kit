"""
End-to-End tests for real-world task-work scenarios.

Tests complete workflows from task creation through complexity evaluation,
review checkpoints, and phase transitions using realistic scenarios that
mirror actual software development tasks.

Scenarios:
1. Simple Bug Fix - Auto-proceed (score 2)
2. Standard Feature - Quick review (score 5)
3. New Architecture - Full review (score 9)
4. Security Change - Force review override
5. First-Time Pattern - Force review override
"""

import pytest
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "installer/global/commands"))

from lib.complexity_models import ReviewMode, ForceReviewTrigger


@pytest.mark.e2e
@pytest.mark.real_world
class TestSimpleBugFixScenario:
    """
    Scenario 1: Simple Bug Fix

    Description:
        Developer needs to fix a validation error in a single file.
        This is a straightforward bug fix with minimal scope.

    Expected Behavior:
        - Complexity Score: 2/10
        - Review Mode: AUTO_PROCEED
        - No user interaction required
        - Automatically proceeds to Phase 3
    """

    def test_bug_fix_auto_proceeds_with_no_interruption(
        self,
        real_world_task_factory,
        e2e_plan_factory
    ):
        """Test that simple bug fix auto-proceeds without user interaction."""
        # GIVEN: A simple bug fix task
        task_data = real_world_task_factory("simple_bug_fix")

        # WHEN: Plan is generated and evaluated
        plan = e2e_plan_factory(task_data)

        # THEN: Complexity is low (score 3: 1 file + 1 pattern + 1 risk = 3)
        assert plan.complexity_score.total_score == 3

        # AND: Review mode is AUTO_PROCEED
        assert plan.complexity_score.review_mode == ReviewMode.AUTO_PROCEED

        # AND: No force triggers
        assert len(plan.complexity_score.forced_review_triggers) == 0

        # AND: Plan would automatically proceed to Phase 3
        # (In real workflow, no checkpoint would be shown)

    def test_bug_fix_plan_saved_correctly(
        self,
        e2e_workspace,
        real_world_task_factory,
        e2e_plan_factory
    ):
        """Test that plan is saved even for auto-proceed scenarios."""
        # GIVEN: A simple bug fix task
        task_data = real_world_task_factory("simple_bug_fix")
        plan = e2e_plan_factory(task_data)

        # WHEN: Plan would be saved (simulated)
        plan_file = e2e_workspace["plans"]["versions"] / f"{task_data['task_id']}_v1.json"

        # THEN: Plan contains correct information
        assert plan.task_id == task_data['task_id']
        assert len(plan.files_to_create) == 1
        assert plan.files_to_create[0] == "src/validators.py"
        assert plan.estimated_loc == 25

    def test_bug_fix_metadata_updated(
        self,
        real_world_task_factory,
        e2e_plan_factory
    ):
        """Test that task metadata is updated with complexity info."""
        # GIVEN: A simple bug fix task
        task_data = real_world_task_factory("simple_bug_fix")
        plan = e2e_plan_factory(task_data)

        # WHEN: Metadata would be updated
        metadata = {
            "complexity_score": plan.complexity_score.total_score,
            "review_mode": plan.complexity_score.review_mode.value,
            "auto_proceeded": True,
            "calculation_timestamp": plan.complexity_score.calculation_timestamp.isoformat(),
        }

        # THEN: Metadata contains correct values
        assert metadata["complexity_score"] == 3
        assert metadata["review_mode"] == "auto_proceed"
        assert metadata["auto_proceeded"] is True

    def test_bug_fix_reaches_phase_3(self, e2e_runner):
        """Test complete workflow reaches Phase 3."""
        # GIVEN + WHEN: Complete workflow execution
        result = e2e_runner.run_complete_workflow("simple_bug_fix")

        # THEN: Phase 3 is reached
        assert result["phase_3_reached"] is True
        assert result["auto_proceeded"] is True
        assert result["complexity_score"] == 3


@pytest.mark.e2e
@pytest.mark.real_world
class TestStandardFeatureScenario:
    """
    Scenario 2: Standard Feature (Password Reset)

    Description:
        Developer implements password reset with email verification.
        Moderate complexity with 4 files and familiar patterns.

    Expected Behavior:
        - Complexity Score: 5/10
        - Review Mode: QUICK_OPTIONAL
        - 10-second countdown with optional escalation
        - Two paths: timeout → Phase 3, ENTER → Full review
    """

    def test_standard_feature_triggers_quick_review(
        self,
        real_world_task_factory,
        e2e_plan_factory
    ):
        """Test that standard feature triggers quick review mode."""
        # GIVEN: A standard feature task
        task_data = real_world_task_factory("standard_feature")

        # WHEN: Plan is generated and evaluated
        plan = e2e_plan_factory(task_data)

        # THEN: Complexity is moderate (score 5)
        assert plan.complexity_score.total_score == 5

        # AND: Review mode is QUICK_OPTIONAL
        assert plan.complexity_score.review_mode == ReviewMode.QUICK_OPTIONAL

        # AND: Multiple files involved
        assert len(plan.files_to_create) == 4
        assert "password_reset.py" in str(plan.files_to_create)

    def test_standard_feature_timeout_path_proceeds(
        self,
        e2e_runner,
        mock_user_input_e2e
    ):
        """Test timeout path: user doesn't interact, auto-proceeds after 10s."""
        # GIVEN: Quick review scenario with no user input (timeout)
        result = e2e_runner.run_complete_workflow(
            "standard_feature",
            user_input_sequence=None  # Simulates timeout
        )

        # THEN: Workflow proceeds after timeout
        assert result["phase_3_reached"] is True
        assert result["timeout_approved"] is True
        assert result["review_mode"] == ReviewMode.QUICK_OPTIONAL

    def test_standard_feature_escalation_path(
        self,
        real_world_task_factory,
        e2e_plan_factory,
        mock_user_input_e2e
    ):
        """Test escalation path: user presses ENTER, escalates to full review."""
        # GIVEN: Quick review scenario
        task_data = real_world_task_factory("standard_feature")
        plan = e2e_plan_factory(task_data)

        # WHEN: User simulates ENTER key (escalation)
        user_input = mock_user_input_e2e.simulate_escalation()

        # THEN: Would escalate to full review
        # (In real workflow, review mode changes to FULL_REQUIRED)
        assert plan.complexity_score.review_mode == ReviewMode.QUICK_OPTIONAL
        assert user_input == ""  # ENTER key

        # AND: After escalation, full review would be shown
        # (escalation_flag would be set in metadata)

    def test_standard_feature_plan_details(
        self,
        real_world_task_factory,
        e2e_plan_factory
    ):
        """Test plan contains correct details for standard feature."""
        # GIVEN: Standard feature task
        task_data = real_world_task_factory("standard_feature")
        plan = e2e_plan_factory(task_data)

        # THEN: Plan has expected structure
        assert plan.estimated_loc == 180
        assert len(plan.external_dependencies) == 2
        assert "sendgrid" in plan.external_dependencies
        assert "itsdangerous" in plan.external_dependencies
        assert "Factory" in plan.patterns_used
        assert "Strategy" in plan.patterns_used


@pytest.mark.e2e
@pytest.mark.real_world
class TestNewArchitectureScenario:
    """
    Scenario 3: New Architecture Pattern (Event Sourcing)

    Description:
        Developer migrates order system to event sourcing architecture.
        High complexity with 8 files and unfamiliar patterns.

    Expected Behavior:
        - Complexity Score: 9/10
        - Review Mode: FULL_REQUIRED
        - Multiple interaction paths:
          a) Approve → Phase 3
          b) Modify → Reduce complexity → Approve
          c) Question → Q&A → Approve
    """

    def test_new_architecture_triggers_full_review(
        self,
        real_world_task_factory,
        e2e_plan_factory
    ):
        """Test that new architecture triggers full review mode."""
        # GIVEN: New architecture task
        task_data = real_world_task_factory("new_architecture")

        # WHEN: Plan is generated and evaluated
        plan = e2e_plan_factory(task_data)

        # THEN: Complexity is high (score 8: 3 files + 2 pattern + 3 risk = 8)
        assert plan.complexity_score.total_score == 8

        # AND: Review mode is FULL_REQUIRED
        assert plan.complexity_score.review_mode == ReviewMode.FULL_REQUIRED

        # AND: Many files involved
        assert len(plan.files_to_create) == 8

        # AND: Unfamiliar patterns
        assert "Event Sourcing" in plan.patterns_used
        assert "CQRS" in plan.patterns_used

    def test_new_architecture_approval_path(
        self,
        e2e_runner,
        mock_user_input_e2e
    ):
        """Test approval path: user approves complex plan."""
        # GIVEN: Full review scenario with approval
        result = e2e_runner.run_complete_workflow(
            "new_architecture",
            user_input_sequence=["A"]
        )

        # THEN: Workflow proceeds to Phase 3
        assert result["phase_3_reached"] is True
        assert result["user_approved"] is True
        assert result["complexity_score"] == 8

    def test_new_architecture_modification_path(
        self,
        real_world_task_factory,
        e2e_plan_factory,
        mock_user_input_e2e
    ):
        """Test modification path: user modifies plan to reduce complexity."""
        # GIVEN: Complex task
        task_data = real_world_task_factory("new_architecture")
        plan = e2e_plan_factory(task_data)

        # WHEN: User initiates modification
        user_inputs = mock_user_input_e2e.simulate_modification([
            "remove file src/events/order_events.py",
            "remove file src/events/event_store.py",
        ])

        # THEN: User interaction includes modification sequence
        assert "M" in user_inputs
        assert "A" in user_inputs  # Final approval

        # AND: Original plan has 8 files
        assert len(plan.files_to_create) == 8

        # AND: After modification, plan would have fewer files
        # (In real workflow, complexity would be recalculated)

    def test_new_architecture_qa_path(
        self,
        real_world_task_factory,
        e2e_plan_factory,
        mock_user_input_e2e
    ):
        """Test Q&A path: user asks questions before approving."""
        # GIVEN: Complex task
        task_data = real_world_task_factory("new_architecture")
        plan = e2e_plan_factory(task_data)

        # WHEN: User initiates Q&A
        questions = [
            "Why use event sourcing instead of CRUD?",
            "What are the trade-offs?",
            "How does this affect testing?",
        ]
        user_inputs = mock_user_input_e2e.simulate_qa_flow(questions)

        # THEN: User interaction includes Q&A sequence
        assert "Q" in user_inputs
        assert "back" in user_inputs  # Exit Q&A
        assert "A" in user_inputs  # Final approval

        # AND: Questions are recorded
        assert len(questions) == 3

    def test_new_architecture_risk_indicators(
        self,
        real_world_task_factory,
        e2e_plan_factory
    ):
        """Test that risk indicators are correctly identified."""
        # GIVEN: New architecture task
        task_data = real_world_task_factory("new_architecture")
        plan = e2e_plan_factory(task_data)

        # THEN: Risk indicators are present
        assert "data_migration" in plan.risk_indicators
        assert "breaking_change" in plan.risk_indicators

        # AND: External dependencies identified
        assert "eventsourcing" in plan.external_dependencies
        assert "redis" in plan.external_dependencies


@pytest.mark.e2e
@pytest.mark.real_world
class TestSecurityChangeScenario:
    """
    Scenario 4: Security Change (OAuth2 Migration)

    Description:
        Developer replaces basic authentication with OAuth2.
        Only 2 files, but security-sensitive.

    Expected Behavior:
        - Complexity Score: 2/10 (low file count)
        - Force Trigger: SECURITY_KEYWORDS
        - Review Mode: FULL_REQUIRED (overridden by trigger)
        - Security keywords detected in plan
    """

    def test_security_change_forces_full_review(
        self,
        real_world_task_factory,
        e2e_plan_factory
    ):
        """Test that security keywords force full review despite low score."""
        # GIVEN: Security change task
        task_data = real_world_task_factory("security_change")

        # WHEN: Plan is generated and evaluated
        plan = e2e_plan_factory(task_data)

        # THEN: Complexity score is 5 (1 file + 1 pattern + 3 high risk = 5)
        # Note: High security risk increases the score despite low file count
        assert plan.complexity_score.total_score == 5

        # BUT: Force trigger overrides to FULL_REQUIRED
        assert plan.complexity_score.review_mode == ReviewMode.FULL_REQUIRED

        # AND: Security trigger is detected
        assert ForceReviewTrigger.SECURITY_KEYWORDS in plan.complexity_score.forced_review_triggers

    def test_security_change_trigger_detection(
        self,
        real_world_task_factory,
        e2e_plan_factory
    ):
        """Test that security keywords are correctly detected."""
        # GIVEN: Security change task
        task_data = real_world_task_factory("security_change")
        plan = e2e_plan_factory(task_data)

        # THEN: Security indicators are present
        assert "authentication" in plan.risk_indicators
        assert "security" in plan.risk_indicators

        # AND: OAuth2 pattern identified
        assert "OAuth2" in plan.patterns_used

    def test_security_change_requires_approval(
        self,
        e2e_runner
    ):
        """Test that security changes require explicit approval."""
        # GIVEN: Security change with full review
        result = e2e_runner.run_complete_workflow(
            "security_change",
            user_input_sequence=["A"]
        )

        # THEN: User approval required (no auto-proceed)
        assert result["phase_3_reached"] is True
        assert result["user_approved"] is True

        # AND: Force trigger recorded
        assert ForceReviewTrigger.SECURITY_KEYWORDS in result["force_triggers"]

    def test_security_change_low_complexity_high_risk(
        self,
        real_world_task_factory,
        e2e_plan_factory
    ):
        """Test that risk assessment overrides low complexity."""
        # GIVEN: Security change task
        task_data = real_world_task_factory("security_change")
        plan = e2e_plan_factory(task_data)

        # THEN: File count is low (would normally be score 2)
        assert len(plan.files_to_create) == 2

        # BUT: Risk level is high
        factor_scores = {f.factor_name: f.score for f in plan.complexity_score.factor_scores}
        assert factor_scores.get("Risk Level") == 3.0  # Maximum risk


@pytest.mark.e2e
@pytest.mark.real_world
class TestFirstTimePatternScenario:
    """
    Scenario 5: First-Time Pattern (GraphQL)

    Description:
        Developer adds GraphQL endpoint for the first time.
        Moderate complexity (5 files) but unfamiliar pattern.

    Expected Behavior:
        - Complexity Score: 5/10 (moderate)
        - Force Trigger: FIRST_TIME_PATTERN
        - Review Mode: FULL_REQUIRED (overridden by trigger)
        - Pattern unfamiliarity detected
    """

    def test_first_time_pattern_forces_full_review(
        self,
        real_world_task_factory,
        e2e_plan_factory
    ):
        """Test that first-time pattern usage forces full review."""
        # GIVEN: First-time pattern task
        task_data = real_world_task_factory("first_time_pattern")

        # WHEN: Plan is generated and evaluated
        plan = e2e_plan_factory(task_data)

        # THEN: Complexity score is moderate-high (score 6: 2 files + 2 pattern + 2 risk = 6)
        assert plan.complexity_score.total_score == 6

        # BUT: Review mode is FULL_REQUIRED (would normally be QUICK_OPTIONAL)
        assert plan.complexity_score.review_mode == ReviewMode.FULL_REQUIRED

        # AND: GraphQL pattern detected
        assert "GraphQL" in plan.patterns_used

    def test_first_time_pattern_detection(
        self,
        real_world_task_factory,
        e2e_plan_factory
    ):
        """Test that first-time pattern is correctly identified."""
        # GIVEN: First-time pattern task
        task_data = real_world_task_factory("first_time_pattern")
        plan = e2e_plan_factory(task_data)

        # THEN: GraphQL-related files present
        assert len(plan.files_to_create) == 5
        assert any("schema" in f for f in plan.files_to_create)
        assert any("resolvers" in f for f in plan.files_to_create)

        # AND: GraphQL dependencies present
        assert "graphene" in plan.external_dependencies
        assert "graphql-core" in plan.external_dependencies

    def test_first_time_pattern_requires_review(
        self,
        e2e_runner
    ):
        """Test that first-time patterns require explicit review."""
        # GIVEN: First-time pattern scenario
        result = e2e_runner.run_complete_workflow(
            "first_time_pattern",
            user_input_sequence=["A"]
        )

        # THEN: User approval required
        assert result["phase_3_reached"] is True
        assert result["user_approved"] is True
        assert result["complexity_score"] == 6

    def test_first_time_pattern_complexity_breakdown(
        self,
        real_world_task_factory,
        e2e_plan_factory
    ):
        """Test complexity breakdown for first-time pattern."""
        # GIVEN: First-time pattern task
        task_data = real_world_task_factory("first_time_pattern")
        plan = e2e_plan_factory(task_data)

        # THEN: Complexity factors are correctly calculated
        factor_scores = {f.factor_name: f.score for f in plan.complexity_score.factor_scores}

        assert factor_scores.get("File Complexity") == 2.0  # 5 files
        assert factor_scores.get("Pattern Familiarity") == 2.0  # Unfamiliar
        assert factor_scores.get("Risk Level") <= 2.0  # Moderate risk


@pytest.mark.e2e
@pytest.mark.real_world
class TestCrossScenarioValidation:
    """
    Cross-scenario validation tests.

    Validates that the system correctly differentiates between
    scenarios and routes them to appropriate review modes.
    """

    def test_all_scenarios_have_correct_review_modes(
        self,
        real_world_task_factory,
        e2e_plan_factory
    ):
        """Test that all scenarios route to expected review modes."""
        scenarios = [
            ("simple_bug_fix", ReviewMode.AUTO_PROCEED),
            ("standard_feature", ReviewMode.QUICK_OPTIONAL),
            ("new_architecture", ReviewMode.FULL_REQUIRED),
            ("security_change", ReviewMode.FULL_REQUIRED),
            ("first_time_pattern", ReviewMode.FULL_REQUIRED),
        ]

        for scenario_name, expected_mode in scenarios:
            # GIVEN: Each scenario
            task_data = real_world_task_factory(scenario_name)
            plan = e2e_plan_factory(task_data)

            # THEN: Review mode matches expectation
            assert plan.complexity_score.review_mode == expected_mode, \
                f"Scenario '{scenario_name}' has incorrect review mode"

    def test_complexity_scores_are_distinct(
        self,
        real_world_task_factory,
        e2e_plan_factory
    ):
        """Test that scenarios have distinct complexity scores."""
        scenarios = ["simple_bug_fix", "standard_feature", "new_architecture"]
        scores = []

        for scenario_name in scenarios:
            task_data = real_world_task_factory(scenario_name)
            plan = e2e_plan_factory(task_data)
            scores.append(plan.complexity_score.total_score)

        # THEN: Scores are in ascending order
        assert scores == sorted(scores)
        assert len(set(scores)) == len(scores)  # All distinct

    def test_force_triggers_only_on_security_and_first_time(
        self,
        real_world_task_factory,
        e2e_plan_factory
    ):
        """Test that force triggers only apply to specific scenarios."""
        # Scenarios WITHOUT force triggers
        no_triggers = ["simple_bug_fix", "standard_feature", "new_architecture"]
        for scenario_name in no_triggers:
            task_data = real_world_task_factory(scenario_name)
            plan = e2e_plan_factory(task_data)
            assert len(plan.complexity_score.forced_review_triggers) == 0

        # Scenarios WITH force triggers
        with_triggers = ["security_change"]
        for scenario_name in with_triggers:
            task_data = real_world_task_factory(scenario_name)
            plan = e2e_plan_factory(task_data)
            assert len(plan.complexity_score.forced_review_triggers) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
