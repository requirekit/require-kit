"""
Comprehensive unit tests for complexity calculation engine.

Tests all aspects of the ComplexityCalculator including:
- Factor evaluation
- Score aggregation
- Force trigger detection
- Review mode routing
- Error handling and fail-safes

Target Coverage: ≥95% (core calculation logic)
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any

# Import system under test using importlib to handle 'global' keyword
ComplexityCalculator = None
ComplexityScore = None
FactorScore = None
ReviewMode = None
ForceReviewTrigger = None
EvaluationContext = None
ImplementationPlan = None
ComplexityFactor = None

try:
    # Add installer lib to path temporarily
    installer_lib_path = Path(__file__).parent.parent.parent / "installer" / "global" / "commands" / "lib"
    if installer_lib_path.exists():
        sys.path.insert(0, str(installer_lib_path))
        
        # Import modules
        import complexity_calculator
        import complexity_models
        import complexity_factors
        
        ComplexityCalculator = complexity_calculator.ComplexityCalculator
        ComplexityScore = complexity_models.ComplexityScore
        FactorScore = complexity_models.FactorScore
        ReviewMode = complexity_models.ReviewMode
        ForceReviewTrigger = complexity_models.ForceReviewTrigger
        EvaluationContext = complexity_models.EvaluationContext
        ImplementationPlan = complexity_models.ImplementationPlan
        ComplexityFactor = complexity_factors.ComplexityFactor
        
        # Clean up
        sys.path.pop(0)
except ImportError as e:
    pytest.skip(f"ComplexityCalculator not found: {e}", allow_module_level=True)


class TestComplexityCalculatorInit:
    """Test ComplexityCalculator initialization."""

    def test_init_with_default_factors(self):
        """Should initialize with default factors."""
        calculator = ComplexityCalculator()

        assert calculator is not None
        assert len(calculator.factors) > 0
        assert calculator.MAX_TOTAL_SCORE == 10
        assert calculator.AUTO_PROCEED_THRESHOLD == 3
        assert calculator.QUICK_OPTIONAL_THRESHOLD == 6

    def test_init_with_custom_factors(self):
        """Should initialize with custom factors."""
        custom_factors = [Mock(spec=ComplexityFactor)]
        calculator = ComplexityCalculator(factors=custom_factors)

        assert calculator.factors == custom_factors
        assert len(calculator.factors) == 1

    def test_init_with_empty_factors_list(self):
        """Should handle empty factors list."""
        calculator = ComplexityCalculator(factors=[])

        assert calculator.factors == []
        assert calculator is not None


class TestScoreAggregation:
    """Test score aggregation logic."""

    def test_aggregate_simple_scores(self):
        """Should sum factor scores correctly."""
        calculator = ComplexityCalculator(factors=[])

        factor_scores = [
            FactorScore(
                factor_name="Factor1",
                score=2,
                max_score=3,
                justification="test",
            ),
            FactorScore(
                factor_name="Factor2",
                score=3,
                max_score=3,
                justification="test",
            ),
        ]

        total = calculator._aggregate_scores(factor_scores)

        assert total == 5  # 2 + 3

    def test_aggregate_capped_at_maximum(self):
        """Should cap total score at MAX_TOTAL_SCORE."""
        calculator = ComplexityCalculator(factors=[])

        factor_scores = [
            FactorScore(
                factor_name=f"Factor{i}",
                score=3,
                max_score=3,
                justification="test",
            )
            for i in range(5)  # 5 factors * 3 = 15
        ]

        total = calculator._aggregate_scores(factor_scores)

        assert total == calculator.MAX_TOTAL_SCORE  # Capped at 10
        assert total <= 10

    def test_aggregate_with_zero_scores(self):
        """Should handle all zero scores."""
        calculator = ComplexityCalculator(factors=[])

        factor_scores = [
            FactorScore(
                factor_name="Factor1",
                score=0,
                max_score=3,
                justification="test",
            ),
        ]

        total = calculator._aggregate_scores(factor_scores)

        assert total == 1  # Minimum score is 1

    def test_aggregate_empty_factor_list(self):
        """Should return default score for empty factor list."""
        calculator = ComplexityCalculator(factors=[])

        total = calculator._aggregate_scores([])

        assert total == 5  # Default to moderate complexity

    def test_aggregate_rounds_to_integer(self):
        """Should round aggregated score to integer."""
        calculator = ComplexityCalculator(factors=[])

        factor_scores = [
            FactorScore(
                factor_name="Factor1",
                score=1,
                max_score=3,
                justification="test",
            ),
        ]

        total = calculator._aggregate_scores(factor_scores)

        assert isinstance(total, int)
        assert total >= 1


class TestReviewModeRouting:
    """Test review mode determination logic."""

    def test_auto_proceed_for_score_1(self):
        """Should route to AUTO_PROCEED for score 1."""
        calculator = ComplexityCalculator()

        mode = calculator._determine_review_mode(1, [])

        assert mode == ReviewMode.AUTO_PROCEED

    def test_auto_proceed_for_score_3(self):
        """Should route to AUTO_PROCEED for score 3 (boundary)."""
        calculator = ComplexityCalculator()

        mode = calculator._determine_review_mode(3, [])

        assert mode == ReviewMode.AUTO_PROCEED

    def test_quick_optional_for_score_4(self):
        """Should route to QUICK_OPTIONAL for score 4 (boundary)."""
        calculator = ComplexityCalculator()

        mode = calculator._determine_review_mode(4, [])

        assert mode == ReviewMode.QUICK_OPTIONAL

    def test_quick_optional_for_score_5(self):
        """Should route to QUICK_OPTIONAL for score 5."""
        calculator = ComplexityCalculator()

        mode = calculator._determine_review_mode(5, [])

        assert mode == ReviewMode.QUICK_OPTIONAL

    def test_quick_optional_for_score_6(self):
        """Should route to QUICK_OPTIONAL for score 6 (boundary)."""
        calculator = ComplexityCalculator()

        mode = calculator._determine_review_mode(6, [])

        assert mode == ReviewMode.QUICK_OPTIONAL

    def test_full_required_for_score_7(self):
        """Should route to FULL_REQUIRED for score 7 (boundary)."""
        calculator = ComplexityCalculator()

        mode = calculator._determine_review_mode(7, [])

        assert mode == ReviewMode.FULL_REQUIRED

    def test_full_required_for_score_10(self):
        """Should route to FULL_REQUIRED for score 10 (maximum)."""
        calculator = ComplexityCalculator()

        mode = calculator._determine_review_mode(10, [])

        assert mode == ReviewMode.FULL_REQUIRED

    def test_force_trigger_overrides_low_score(self):
        """Force triggers should override low complexity score."""
        calculator = ComplexityCalculator()

        mode = calculator._determine_review_mode(
            2,  # Low score (would be AUTO_PROCEED)
            [ForceReviewTrigger.SECURITY_KEYWORDS]
        )

        assert mode == ReviewMode.FULL_REQUIRED

    def test_multiple_force_triggers(self):
        """Multiple force triggers should still route to FULL_REQUIRED."""
        calculator = ComplexityCalculator()

        mode = calculator._determine_review_mode(
            1,
            [
                ForceReviewTrigger.SECURITY_KEYWORDS,
                ForceReviewTrigger.SCHEMA_CHANGES,
                ForceReviewTrigger.HOTFIX
            ]
        )

        assert mode == ReviewMode.FULL_REQUIRED


class TestForceTriggerDetection:
    """Test force-review trigger detection."""

    def test_detects_user_flag_trigger(self):
        """Should detect user-requested review flag."""
        calculator = ComplexityCalculator()

        context = Mock(spec=EvaluationContext)
        context.user_requested_review = True
        context.is_hotfix = False
        context.implementation_plan = Mock()
        context.implementation_plan.has_security_keywords = False
        context.implementation_plan.has_schema_changes = False
        context.implementation_plan.raw_plan = "Normal plan"

        triggers = calculator._detect_forced_triggers(context)

        assert ForceReviewTrigger.USER_FLAG in triggers

    def test_detects_security_keywords_trigger(self):
        """Should detect security-sensitive functionality."""
        calculator = ComplexityCalculator()

        context = Mock(spec=EvaluationContext)
        context.user_requested_review = False
        context.is_hotfix = False
        context.implementation_plan = Mock()
        context.implementation_plan.has_security_keywords = True
        context.implementation_plan.has_schema_changes = False
        context.implementation_plan.raw_plan = "Authentication changes"

        triggers = calculator._detect_forced_triggers(context)

        assert ForceReviewTrigger.SECURITY_KEYWORDS in triggers

    def test_detects_schema_changes_trigger(self):
        """Should detect database schema modifications."""
        calculator = ComplexityCalculator()

        context = Mock(spec=EvaluationContext)
        context.user_requested_review = False
        context.is_hotfix = False
        context.implementation_plan = Mock()
        context.implementation_plan.has_security_keywords = False
        context.implementation_plan.has_schema_changes = True
        context.implementation_plan.raw_plan = "Database migration"

        triggers = calculator._detect_forced_triggers(context)

        assert ForceReviewTrigger.SCHEMA_CHANGES in triggers

    def test_detects_hotfix_trigger(self):
        """Should detect production hotfix flag."""
        calculator = ComplexityCalculator()

        context = Mock(spec=EvaluationContext)
        context.user_requested_review = False
        context.is_hotfix = True
        context.implementation_plan = Mock()
        context.implementation_plan.has_security_keywords = False
        context.implementation_plan.has_schema_changes = False
        context.implementation_plan.raw_plan = "Hotfix"

        triggers = calculator._detect_forced_triggers(context)

        assert ForceReviewTrigger.HOTFIX in triggers

    def test_detects_breaking_changes_trigger(self):
        """Should detect breaking API changes from plan text."""
        calculator = ComplexityCalculator()

        context = Mock(spec=EvaluationContext)
        context.user_requested_review = False
        context.is_hotfix = False
        context.implementation_plan = Mock()
        context.implementation_plan.has_security_keywords = False
        context.implementation_plan.has_schema_changes = False
        context.implementation_plan.raw_plan = "This is a breaking change to the API"

        triggers = calculator._detect_forced_triggers(context)

        assert ForceReviewTrigger.BREAKING_CHANGES in triggers

    def test_detects_multiple_triggers(self):
        """Should detect multiple force triggers simultaneously."""
        calculator = ComplexityCalculator()

        context = Mock(spec=EvaluationContext)
        context.user_requested_review = True
        context.is_hotfix = True
        context.implementation_plan = Mock()
        context.implementation_plan.has_security_keywords = True
        context.implementation_plan.has_schema_changes = True
        context.implementation_plan.raw_plan = "Breaking change"

        triggers = calculator._detect_forced_triggers(context)

        assert len(triggers) == 5  # All triggers detected
        assert ForceReviewTrigger.USER_FLAG in triggers
        assert ForceReviewTrigger.SECURITY_KEYWORDS in triggers
        assert ForceReviewTrigger.SCHEMA_CHANGES in triggers
        assert ForceReviewTrigger.HOTFIX in triggers
        assert ForceReviewTrigger.BREAKING_CHANGES in triggers

    def test_no_triggers_detected(self):
        """Should return empty list when no triggers present."""
        calculator = ComplexityCalculator()

        context = Mock(spec=EvaluationContext)
        context.user_requested_review = False
        context.is_hotfix = False
        context.implementation_plan = Mock()
        context.implementation_plan.has_security_keywords = False
        context.implementation_plan.has_schema_changes = False
        context.implementation_plan.raw_plan = "Normal implementation"

        triggers = calculator._detect_forced_triggers(context)

        assert triggers == []


class TestBreakingChangeDetection:
    """Test breaking change detection from plan text."""

    @pytest.mark.parametrize("keyword", [
        "breaking change",
        "breaking api",
        "remove endpoint",
        "delete endpoint",
        "rename endpoint",
        "change contract",
        "modify response",
        "modify request",
        "api version"
    ])
    def test_detects_breaking_change_keywords(self, keyword):
        """Should detect various breaking change keywords."""
        calculator = ComplexityCalculator()

        plan_text = f"Implementation plan includes {keyword} for users API"

        result = calculator._has_breaking_changes(plan_text)

        assert result is True

    def test_case_insensitive_detection(self):
        """Should detect breaking changes case-insensitively."""
        calculator = ComplexityCalculator()

        plan_text = "BREAKING CHANGE to authentication"

        result = calculator._has_breaking_changes(plan_text)

        assert result is True

    def test_no_breaking_changes(self):
        """Should return False when no breaking changes."""
        calculator = ComplexityCalculator()

        plan_text = "Standard implementation with backward compatibility"

        result = calculator._has_breaking_changes(plan_text)

        assert result is False


class TestFactorEvaluation:
    """Test factor evaluation orchestration."""

    def test_evaluates_all_factors(self):
        """Should evaluate all configured factors."""
        # Create mock factors
        factor1 = Mock(spec=ComplexityFactor)
        factor1.evaluate.return_value = FactorScore(
            factor_name="Factor1",
            score=2,
            max_score=3,
            justification="test1",
        )

        factor2 = Mock(spec=ComplexityFactor)
        factor2.evaluate.return_value = FactorScore(
            factor_name="Factor2",
            score=1,
            max_score=3,
            justification="test2",
        )

        calculator = ComplexityCalculator(factors=[factor1, factor2])
        context = Mock(spec=EvaluationContext)

        factor_scores = calculator._evaluate_factors(context)

        assert len(factor_scores) == 2
        assert factor1.evaluate.called
        assert factor2.evaluate.called

    def test_handles_factor_evaluation_error(self):
        """Should continue evaluation if a factor fails."""
        # Create one good factor and one failing factor
        good_factor = Mock(spec=ComplexityFactor)
        good_factor.evaluate.return_value = FactorScore(
            factor_name="GoodFactor",
            score=2,
            max_score=3,
            justification="success",
        )

        bad_factor = Mock(spec=ComplexityFactor)
        bad_factor.evaluate.side_effect = Exception("Factor error")

        calculator = ComplexityCalculator(factors=[good_factor, bad_factor])
        context = Mock(spec=EvaluationContext)

        factor_scores = calculator._evaluate_factors(context)

        # Should only have the good factor's score
        assert len(factor_scores) == 1
        assert factor_scores[0].factor_name == "GoodFactor"

    def test_empty_factors_list(self):
        """Should handle empty factors list gracefully."""
        calculator = ComplexityCalculator(factors=[])
        context = Mock(spec=EvaluationContext)

        factor_scores = calculator._evaluate_factors(context)

        assert factor_scores == []


class TestCompleteCalculation:
    """Test end-to-end calculation workflow."""

    def test_successful_calculation_flow(self):
        """Should complete full calculation successfully."""
        # Create mock factor
        factor = Mock(spec=ComplexityFactor)
        factor.evaluate.return_value = FactorScore(
            factor_name="TestFactor",
            score=5,
            max_score=10,
            justification="test",
        )

        calculator = ComplexityCalculator(factors=[factor])

        # Create mock context
        context = Mock(spec=EvaluationContext)
        context.task_id = "TASK-001"
        context.technology_stack = "Python"
        context.user_requested_review = False
        context.is_hotfix = False
        context.implementation_plan = Mock()
        context.implementation_plan.has_security_keywords = False
        context.implementation_plan.has_schema_changes = False
        context.implementation_plan.raw_plan = "Normal plan"

        result = calculator.calculate(context)

        assert isinstance(result, ComplexityScore)
        assert result.total_score == 5
        assert len(result.factor_scores) == 1
        assert result.forced_review_triggers == []
        assert result.review_mode == ReviewMode.QUICK_OPTIONAL
        assert result.metadata['task_id'] == "TASK-001"

    def test_calculation_with_force_triggers(self):
        """Should include force triggers in result."""
        factor = Mock(spec=ComplexityFactor)
        factor.evaluate.return_value = FactorScore(
            factor_name="TestFactor",
            score=2,
            max_score=10,
            justification="test",
        )

        calculator = ComplexityCalculator(factors=[factor])

        context = Mock(spec=EvaluationContext)
        context.task_id = "TASK-002"
        context.technology_stack = "Python"
        context.user_requested_review = True  # Force trigger
        context.is_hotfix = False
        context.implementation_plan = Mock()
        context.implementation_plan.has_security_keywords = False
        context.implementation_plan.has_schema_changes = False
        context.implementation_plan.raw_plan = "Normal plan"

        result = calculator.calculate(context)

        assert result.total_score == 2  # Low score
        assert ForceReviewTrigger.USER_FLAG in result.forced_review_triggers
        assert result.review_mode == ReviewMode.FULL_REQUIRED  # Overridden by trigger


class TestFailsafeHandling:
    """Test fail-safe error handling."""

    def test_creates_failsafe_score_on_error(self):
        """Should create fail-safe score when calculation fails."""
        # Create factor that raises exception
        bad_factor = Mock(spec=ComplexityFactor)
        bad_factor.evaluate.side_effect = Exception("Fatal error")

        calculator = ComplexityCalculator(factors=[bad_factor])

        context = Mock(spec=EvaluationContext)
        context.task_id = "TASK-003"
        context.technology_stack = "Python"

        # Should not raise exception - returns fail-safe
        result = calculator.calculate(context)

        assert isinstance(result, ComplexityScore)
        assert result.total_score == calculator.MAX_TOTAL_SCORE  # Maximum complexity
        assert result.review_mode == ReviewMode.FULL_REQUIRED
        assert result.metadata['failsafe'] is True
        assert 'error' in result.metadata

    def test_failsafe_score_structure(self):
        """Fail-safe score should have correct structure."""
        calculator = ComplexityCalculator(factors=[])

        context = Mock(spec=EvaluationContext)
        context.task_id = "TASK-004"
        context.technology_stack = "Python"

        error_message = "Test error"
        result = calculator._create_failsafe_score(context, error_message)

        assert result.total_score == 10
        assert result.factor_scores == []
        assert result.forced_review_triggers == []
        assert result.review_mode == ReviewMode.FULL_REQUIRED
        assert result.metadata['failsafe'] is True
        assert result.metadata['error'] == error_message
        assert result.metadata['task_id'] == "TASK-004"


class TestBoundaryConditions:
    """Test boundary conditions and edge cases."""

    def test_score_exactly_at_thresholds(self):
        """Test exact threshold values."""
        calculator = ComplexityCalculator()

        # Exact boundary tests
        assert calculator._determine_review_mode(3, []) == ReviewMode.AUTO_PROCEED
        assert calculator._determine_review_mode(4, []) == ReviewMode.QUICK_OPTIONAL
        assert calculator._determine_review_mode(6, []) == ReviewMode.QUICK_OPTIONAL
        assert calculator._determine_review_mode(7, []) == ReviewMode.FULL_REQUIRED

    def test_minimum_score_enforced(self):
        """Should enforce minimum score of 1."""
        calculator = ComplexityCalculator(factors=[])

        factor_scores = [
            FactorScore(
                factor_name="ZeroFactor",
                score=0,
                max_score=10,
                justification="zero",
            )
        ]

        total = calculator._aggregate_scores(factor_scores)

        assert total >= 1

    def test_maximum_score_enforced(self):
        """Should cap score at maximum."""
        calculator = ComplexityCalculator(factors=[])

        factor_scores = [
            FactorScore(
                factor_name=f"Factor{i}",
                score=10,
                max_score=10,
                justification="max",
            )
            for i in range(5)  # Would sum to 50
        ]

        total = calculator._aggregate_scores(factor_scores)

        assert total == calculator.MAX_TOTAL_SCORE
        assert total == 10


class TestMetadata:
    """Test metadata inclusion in results."""

    def test_includes_task_metadata(self):
        """Should include task metadata in result."""
        factor = Mock(spec=ComplexityFactor)
        factor.evaluate.return_value = FactorScore(
            factor_name="TestFactor",
            score=3,
            max_score=10,
            justification="test",
        )

        calculator = ComplexityCalculator(factors=[factor])

        context = Mock(spec=EvaluationContext)
        context.task_id = "TASK-META-001"
        context.technology_stack = "TypeScript"
        context.user_requested_review = False
        context.is_hotfix = False
        context.implementation_plan = Mock()
        context.implementation_plan.has_security_keywords = False
        context.implementation_plan.has_schema_changes = False
        context.implementation_plan.raw_plan = "Plan"

        result = calculator.calculate(context)

        assert result.metadata['task_id'] == "TASK-META-001"
        assert result.metadata['technology_stack'] == "TypeScript"
        assert 'factors_evaluated' in result.metadata

    def test_includes_timestamp(self):
        """Should include calculation timestamp."""
        factor = Mock(spec=ComplexityFactor)
        factor.evaluate.return_value = FactorScore(
            factor_name="TestFactor",
            score=3,
            max_score=10,
            justification="test",
        )

        calculator = ComplexityCalculator(factors=[factor])

        context = Mock(spec=EvaluationContext)
        context.task_id = "TASK-TIME-001"
        context.technology_stack = "Python"
        context.user_requested_review = False
        context.is_hotfix = False
        context.implementation_plan = Mock()
        context.implementation_plan.has_security_keywords = False
        context.implementation_plan.has_schema_changes = False
        context.implementation_plan.raw_plan = "Plan"

        before = datetime.now()
        result = calculator.calculate(context)
        after = datetime.now()

        assert before <= result.calculation_timestamp <= after


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
