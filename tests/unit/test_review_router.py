"""
Comprehensive unit tests for ReviewRouter (mode selector).

Tests the routing logic that translates complexity scores into actionable
review decisions. Covers all three review modes (auto-proceed, quick optional,
full required) and edge cases.

Target Coverage: ≥90% (review routing logic)
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any

# Import system under test using importlib to handle 'global' keyword
ReviewRouter = None
ReviewDecision = None
ComplexityScore = None
FactorScore = None
ReviewMode = None
ForceReviewTrigger = None
EvaluationContext = None

try:
    # Add installer lib to path temporarily
    installer_lib_path = Path(__file__).parent.parent.parent / "installer" / "global" / "commands" / "lib"
    if installer_lib_path.exists():
        sys.path.insert(0, str(installer_lib_path))

        # Import modules
        import review_router
        import complexity_models

        ReviewRouter = review_router.ReviewRouter
        ReviewDecision = complexity_models.ReviewDecision
        ComplexityScore = complexity_models.ComplexityScore
        FactorScore = complexity_models.FactorScore
        ReviewMode = complexity_models.ReviewMode
        ForceReviewTrigger = complexity_models.ForceReviewTrigger
        EvaluationContext = complexity_models.EvaluationContext

        # Clean up
        sys.path.pop(0)
except ImportError as e:
    pytest.skip(f"ReviewRouter not found: {e}", allow_module_level=True)


# Test Fixtures
@pytest.fixture
def simple_context():
    """Create simple evaluation context for testing."""
    return EvaluationContext(
        task_id="TASK-001",
        technology_stack="python",
        implementation_plan=None,
        task_metadata={"title": "Simple bug fix"}
    )


@pytest.fixture
def complex_context():
    """Create complex evaluation context for testing."""
    return EvaluationContext(
        task_id="TASK-002",
        technology_stack="python",
        implementation_plan=None,
        task_metadata={"title": "Complex architectural change"}
    )


@pytest.fixture
def auto_proceed_score():
    """Create complexity score for auto-proceed (score 1-3)."""
    return ComplexityScore(
        total_score=2,
        factor_scores=[
            FactorScore(
                factor_name="file_complexity",
                score=1,
                max_score=3,
                justification="Single file change"
            )
        ],
        forced_review_triggers=[],
        review_mode=ReviewMode.AUTO_PROCEED,
        calculation_timestamp=datetime.now(),
        metadata={}
    )


@pytest.fixture
def quick_optional_score():
    """Create complexity score for quick optional review (score 4-6)."""
    return ComplexityScore(
        total_score=5,
        factor_scores=[
            FactorScore(
                factor_name="file_complexity",
                score=2,
                max_score=3,
                justification="Moderate file changes"
            ),
            FactorScore(
                factor_name="dependency_complexity",
                score=3,
                max_score=3,
                justification="Multiple dependencies"
            )
        ],
        forced_review_triggers=[],
        review_mode=ReviewMode.QUICK_OPTIONAL,
        calculation_timestamp=datetime.now(),
        metadata={}
    )


@pytest.fixture
def full_required_score():
    """Create complexity score for full required review (score 7-10)."""
    return ComplexityScore(
        total_score=8,
        factor_scores=[
            FactorScore(
                factor_name="file_complexity",
                score=3,
                max_score=3,
                justification="Many files"
            ),
            FactorScore(
                factor_name="dependency_complexity",
                score=3,
                max_score=3,
                justification="Complex dependencies"
            ),
            FactorScore(
                factor_name="risk_factors",
                score=2,
                max_score=2,
                justification="High risk indicators"
            )
        ],
        forced_review_triggers=[],
        review_mode=ReviewMode.FULL_REQUIRED,
        calculation_timestamp=datetime.now(),
        metadata={}
    )


@pytest.fixture
def force_trigger_score():
    """Create complexity score with force-review triggers."""
    return ComplexityScore(
        total_score=3,  # Low score but forced review
        factor_scores=[
            FactorScore(
                factor_name="file_complexity",
                score=1,
                max_score=3,
                justification="Simple change"
            )
        ],
        forced_review_triggers=[ForceReviewTrigger.SECURITY_KEYWORDS],
        review_mode=ReviewMode.FULL_REQUIRED,
        calculation_timestamp=datetime.now(),
        metadata={}
    )


class TestReviewRouterInit:
    """Test ReviewRouter initialization."""

    def test_router_instantiation(self):
        """Should create router instance successfully."""
        router = ReviewRouter()
        assert router is not None

    def test_router_has_required_methods(self):
        """Should have all required routing methods."""
        router = ReviewRouter()
        assert hasattr(router, 'route')
        assert callable(router.route)


class TestAutoProceedRouting:
    """Test auto-proceed routing (score 1-3)."""

    def test_routes_to_auto_proceed_for_low_score(
        self, auto_proceed_score, simple_context
    ):
        """Should route low complexity tasks to auto-proceed."""
        router = ReviewRouter()
        decision = router.route(auto_proceed_score, simple_context)

        assert decision.action == "proceed"
        assert decision.auto_approved is True
        assert decision.routing_recommendation == "Phase 3"

    def test_auto_proceed_includes_task_id_in_summary(
        self, auto_proceed_score, simple_context
    ):
        """Should include task ID in summary message."""
        router = ReviewRouter()
        decision = router.route(auto_proceed_score, simple_context)

        assert "TASK-001" in decision.summary_message

    def test_auto_proceed_shows_complexity_score(
        self, auto_proceed_score, simple_context
    ):
        """Should display complexity score in summary."""
        router = ReviewRouter()
        decision = router.route(auto_proceed_score, simple_context)

        assert "2/10" in decision.summary_message or "Score: 2" in decision.summary_message

    def test_auto_proceed_shows_factor_breakdown(
        self, auto_proceed_score, simple_context
    ):
        """Should show breakdown of complexity factors."""
        router = ReviewRouter()
        decision = router.route(auto_proceed_score, simple_context)

        assert "file_complexity" in decision.summary_message.lower()
        assert "Factor Breakdown:" in decision.summary_message or "factor" in decision.summary_message.lower()

    def test_auto_proceed_indicates_no_review_needed(
        self, auto_proceed_score, simple_context
    ):
        """Should indicate no human review is required."""
        router = ReviewRouter()
        decision = router.route(auto_proceed_score, simple_context)

        summary_lower = decision.summary_message.lower()
        assert "no human review" in summary_lower or "auto-proceed" in summary_lower

    def test_auto_proceed_includes_timestamp(
        self, auto_proceed_score, simple_context
    ):
        """Should include timestamp in decision."""
        router = ReviewRouter()
        decision = router.route(auto_proceed_score, simple_context)

        assert decision.timestamp is not None
        assert isinstance(decision.timestamp, datetime)

    def test_auto_proceed_for_boundary_score_3(
        self, simple_context
    ):
        """Should auto-proceed for boundary score of exactly 3."""
        score = ComplexityScore(
            total_score=3,
            factor_scores=[],
            forced_review_triggers=[],
            review_mode=ReviewMode.AUTO_PROCEED,
            calculation_timestamp=datetime.now(),
            metadata={}
        )

        router = ReviewRouter()
        decision = router.route(score, simple_context)

        assert decision.action == "proceed"
        assert decision.auto_approved is True

    def test_auto_proceed_for_minimum_score_1(
        self, simple_context
    ):
        """Should auto-proceed for minimum score of 1."""
        score = ComplexityScore(
            total_score=1,
            factor_scores=[],
            forced_review_triggers=[],
            review_mode=ReviewMode.AUTO_PROCEED,
            calculation_timestamp=datetime.now(),
            metadata={}
        )

        router = ReviewRouter()
        decision = router.route(score, simple_context)

        assert decision.action == "proceed"
        assert decision.auto_approved is True


class TestQuickOptionalRouting:
    """Test quick optional routing (score 4-6)."""

    def test_routes_to_quick_optional_for_moderate_score(
        self, quick_optional_score, simple_context
    ):
        """Should route moderate complexity to quick optional."""
        router = ReviewRouter()
        decision = router.route(quick_optional_score, simple_context)

        assert decision.action == "review_required"
        assert decision.auto_approved is False
        assert "Optional" in decision.routing_recommendation

    def test_quick_optional_shows_warning_icon(
        self, quick_optional_score, simple_context
    ):
        """Should use warning icon for moderate complexity."""
        router = ReviewRouter()
        decision = router.route(quick_optional_score, simple_context)

        # Check for warning indicator
        assert "⚠" in decision.summary_message or "WARNING" in decision.summary_message.upper()

    def test_quick_optional_highlights_high_factors(
        self, quick_optional_score, simple_context
    ):
        """Should highlight factors with high scores."""
        router = ReviewRouter()
        decision = router.route(quick_optional_score, simple_context)

        # Both factors should be shown
        assert "file_complexity" in decision.summary_message.lower()
        assert "dependency_complexity" in decision.summary_message.lower()

    def test_quick_optional_shows_checkpoint_options(
        self, quick_optional_score, simple_context
    ):
        """Should show user options for optional checkpoint."""
        router = ReviewRouter()
        decision = router.route(quick_optional_score, simple_context)

        summary_lower = decision.summary_message.lower()
        # Should mention optional nature
        assert "optional" in summary_lower or "may review" in summary_lower

    def test_quick_optional_indicates_optional_nature(
        self, quick_optional_score, simple_context
    ):
        """Should clearly indicate review is optional."""
        router = ReviewRouter()
        decision = router.route(quick_optional_score, simple_context)

        assert "Optional" in decision.routing_recommendation
        assert "optional" in decision.summary_message.lower() or "not required" in decision.summary_message.lower()

    def test_quick_optional_for_boundary_score_4(
        self, simple_context
    ):
        """Should route to quick optional for boundary score of 4."""
        score = ComplexityScore(
            total_score=4,
            factor_scores=[],
            forced_review_triggers=[],
            review_mode=ReviewMode.QUICK_OPTIONAL,
            calculation_timestamp=datetime.now(),
            metadata={}
        )

        router = ReviewRouter()
        decision = router.route(score, simple_context)

        assert decision.action == "review_required"
        assert "Optional" in decision.routing_recommendation

    def test_quick_optional_for_boundary_score_6(
        self, simple_context
    ):
        """Should route to quick optional for boundary score of 6."""
        score = ComplexityScore(
            total_score=6,
            factor_scores=[],
            forced_review_triggers=[],
            review_mode=ReviewMode.QUICK_OPTIONAL,
            calculation_timestamp=datetime.now(),
            metadata={}
        )

        router = ReviewRouter()
        decision = router.route(score, simple_context)

        assert decision.action == "review_required"
        assert "Optional" in decision.routing_recommendation

    def test_quick_optional_for_middle_score_5(
        self, quick_optional_score, simple_context
    ):
        """Should route score 5 to quick optional."""
        router = ReviewRouter()
        decision = router.route(quick_optional_score, simple_context)

        assert decision.action == "review_required"
        assert quick_optional_score.total_score == 5


class TestFullRequiredRouting:
    """Test full required routing (score 7-10 or force triggers)."""

    def test_routes_to_full_required_for_high_score(
        self, full_required_score, complex_context
    ):
        """Should route high complexity to full required."""
        router = ReviewRouter()
        decision = router.route(full_required_score, complex_context)

        assert decision.action == "review_required"
        assert decision.auto_approved is False
        assert "Required" in decision.routing_recommendation

    def test_full_required_shows_critical_icon(
        self, full_required_score, complex_context
    ):
        """Should use critical icon for high complexity."""
        router = ReviewRouter()
        decision = router.route(full_required_score, complex_context)

        # Check for critical indicator
        assert "🔴" in decision.summary_message or "CRITICAL" in decision.summary_message.upper()

    def test_full_required_shows_all_factors(
        self, full_required_score, complex_context
    ):
        """Should show all complexity factors in detail."""
        router = ReviewRouter()
        decision = router.route(full_required_score, complex_context)

        # All three factors should be present
        assert "file_complexity" in decision.summary_message.lower()
        assert "dependency_complexity" in decision.summary_message.lower()
        assert "risk_factors" in decision.summary_message.lower()

    def test_full_required_indicates_mandatory_review(
        self, full_required_score, complex_context
    ):
        """Should clearly indicate review is mandatory."""
        router = ReviewRouter()
        decision = router.route(full_required_score, complex_context)

        summary_lower = decision.summary_message.lower()
        assert "mandatory" in summary_lower or "required" in summary_lower

    def test_full_required_shows_phase_2_6_routing(
        self, full_required_score, complex_context
    ):
        """Should route to Phase 2.6 checkpoint."""
        router = ReviewRouter()
        decision = router.route(full_required_score, complex_context)

        assert "2.6" in decision.routing_recommendation or "Checkpoint" in decision.routing_recommendation

    def test_full_required_for_boundary_score_7(
        self, complex_context
    ):
        """Should route to full required for boundary score of 7."""
        score = ComplexityScore(
            total_score=7,
            factor_scores=[],
            forced_review_triggers=[],
            review_mode=ReviewMode.FULL_REQUIRED,
            calculation_timestamp=datetime.now(),
            metadata={}
        )

        router = ReviewRouter()
        decision = router.route(score, complex_context)

        assert decision.action == "review_required"
        assert "Required" in decision.routing_recommendation

    def test_full_required_for_maximum_score_10(
        self, complex_context
    ):
        """Should route to full required for maximum score of 10."""
        score = ComplexityScore(
            total_score=10,
            factor_scores=[],
            forced_review_triggers=[],
            review_mode=ReviewMode.FULL_REQUIRED,
            calculation_timestamp=datetime.now(),
            metadata={}
        )

        router = ReviewRouter()
        decision = router.route(score, complex_context)

        assert decision.action == "review_required"
        assert "Required" in decision.routing_recommendation


class TestForceReviewTriggers:
    """Test force-review trigger handling."""

    def test_force_trigger_overrides_low_score(
        self, force_trigger_score, simple_context
    ):
        """Should force full review even with low score."""
        router = ReviewRouter()
        decision = router.route(force_trigger_score, simple_context)

        assert decision.action == "review_required"
        assert "Required" in decision.routing_recommendation
        assert force_trigger_score.total_score == 3  # Low score

    def test_force_trigger_shows_trigger_details(
        self, force_trigger_score, simple_context
    ):
        """Should display which triggers forced review."""
        router = ReviewRouter()
        decision = router.route(force_trigger_score, simple_context)

        summary_lower = decision.summary_message.lower()
        assert "trigger" in summary_lower or "security" in summary_lower

    def test_multiple_force_triggers_all_shown(
        self, simple_context
    ):
        """Should display all force-review triggers."""
        score = ComplexityScore(
            total_score=2,
            factor_scores=[],
            forced_review_triggers=[
                ForceReviewTrigger.SECURITY_KEYWORDS,
                ForceReviewTrigger.BREAKING_CHANGES
            ],
            review_mode=ReviewMode.FULL_REQUIRED,
            calculation_timestamp=datetime.now(),
            metadata={}
        )

        router = ReviewRouter()
        decision = router.route(score, simple_context)

        # Both triggers should be mentioned
        summary_lower = decision.summary_message.lower()
        assert "security" in summary_lower or "keyword" in summary_lower
        assert "breaking" in summary_lower or "change" in summary_lower

    def test_user_flag_trigger(
        self, simple_context
    ):
        """Should respect user flag force-review trigger."""
        score = ComplexityScore(
            total_score=1,
            factor_scores=[],
            forced_review_triggers=[ForceReviewTrigger.USER_FLAG],
            review_mode=ReviewMode.FULL_REQUIRED,
            calculation_timestamp=datetime.now(),
            metadata={}
        )

        router = ReviewRouter()
        decision = router.route(score, simple_context)

        assert decision.action == "review_required"

    def test_schema_changes_trigger(
        self, simple_context
    ):
        """Should respect schema changes force-review trigger."""
        score = ComplexityScore(
            total_score=2,
            factor_scores=[],
            forced_review_triggers=[ForceReviewTrigger.SCHEMA_CHANGES],
            review_mode=ReviewMode.FULL_REQUIRED,
            calculation_timestamp=datetime.now(),
            metadata={}
        )

        router = ReviewRouter()
        decision = router.route(score, simple_context)

        assert decision.action == "review_required"

    def test_hotfix_trigger(
        self, simple_context
    ):
        """Should respect hotfix force-review trigger."""
        score = ComplexityScore(
            total_score=2,
            factor_scores=[],
            forced_review_triggers=[ForceReviewTrigger.HOTFIX],
            review_mode=ReviewMode.FULL_REQUIRED,
            calculation_timestamp=datetime.now(),
            metadata={}
        )

        router = ReviewRouter()
        decision = router.route(score, simple_context)

        assert decision.action == "review_required"


class TestFailsafeHandling:
    """Test error handling and fail-safe mechanisms."""

    def test_failsafe_on_routing_error(
        self, auto_proceed_score, simple_context
    ):
        """Should fail-safe to full review on routing error."""
        router = ReviewRouter()

        # Mock the routing methods to raise error
        with patch.object(router, '_auto_proceed_decision', side_effect=Exception("Test error")):
            decision = router.route(auto_proceed_score, simple_context)

            # Should default to review_required for safety
            assert decision.action == "review_required"
            assert "Error Recovery" in decision.routing_recommendation or "error" in decision.summary_message.lower()

    def test_failsafe_includes_error_message(
        self, auto_proceed_score, simple_context
    ):
        """Should include error information in fail-safe decision."""
        router = ReviewRouter()

        with patch.object(router, '_auto_proceed_decision', side_effect=ValueError("Invalid state")):
            decision = router.route(auto_proceed_score, simple_context)

            assert "error" in decision.summary_message.lower()

    def test_failsafe_creates_valid_decision(
        self, auto_proceed_score, simple_context
    ):
        """Should create valid ReviewDecision on error."""
        router = ReviewRouter()

        with patch.object(router, '_quick_optional_decision', side_effect=RuntimeError("Unexpected")):
            # Create quick optional score
            score = ComplexityScore(
                total_score=5,
                factor_scores=[],
                forced_review_triggers=[],
                review_mode=ReviewMode.QUICK_OPTIONAL,
                calculation_timestamp=datetime.now(),
                metadata={}
            )

            decision = router.route(score, simple_context)

            # Decision should be valid
            assert decision.action in ["proceed", "review_required"]
            assert decision.complexity_score is not None
            assert decision.routing_recommendation is not None


class TestSummaryFormatting:
    """Test summary message formatting."""

    def test_compact_summary_format(
        self, auto_proceed_score
    ):
        """Should format compact summary correctly."""
        from review_router import format_complexity_summary_compact

        summary = format_complexity_summary_compact(auto_proceed_score)

        assert "2/10" in summary
        assert "auto_proceed" in summary
        assert "file_complexity" in summary.lower()

    def test_compact_summary_with_triggers(
        self, force_trigger_score
    ):
        """Should include triggers in compact summary."""
        from review_router import format_complexity_summary_compact

        summary = format_complexity_summary_compact(force_trigger_score)

        assert "triggers:" in summary.lower() or "security" in summary.lower()

    def test_compact_summary_with_multiple_factors(
        self, full_required_score
    ):
        """Should list all factors in compact summary."""
        from review_router import format_complexity_summary_compact

        summary = format_complexity_summary_compact(full_required_score)

        # Should contain all factor names
        assert "file_complexity" in summary.lower()
        assert "dependency_complexity" in summary.lower()
        assert "risk_factors" in summary.lower()
