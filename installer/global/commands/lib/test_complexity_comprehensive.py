#!/usr/bin/env python3
"""
Comprehensive test suite for TASK-003A complexity evaluation system.

Coverage:
1. ComplexityCalculator Tests (file count, patterns, risk, aggregation, error handling)
2. ReviewRouter Tests (auto-proceed, quick optional, full required, force triggers)
3. Force Trigger Detection (user flag, security, breaking changes, schema, hotfix)
4. Integration Tests (end-to-end flows)
5. Agent Utils (parsing, formatting, context building)

Run: python3 test_complexity_comprehensive.py
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import as package
lib_path = Path(__file__).parent
parent_path = lib_path.parent
sys.path.insert(0, str(parent_path))

from lib.complexity_models import (
    EvaluationContext,
    ImplementationPlan,
    ReviewMode,
    ForceReviewTrigger,
    ComplexityScore,
    FactorScore
)
from lib.complexity_calculator import ComplexityCalculator
from lib.review_router import ReviewRouter
from lib.complexity_factors import (
    FileComplexityFactor,
    PatternFamiliarityFactor,
    RiskLevelFactor
)
from lib.agent_utils import (
    parse_implementation_plan,
    build_evaluation_context,
    format_decision_for_display,
    format_decision_for_metadata
)


# ============================================================================
# UNIT TESTS - ComplexityCalculator
# ============================================================================

class TestComplexityCalculator:
    """Tests for ComplexityCalculator class."""

    def setup_method(self):
        """Setup test fixtures."""
        self.calculator = ComplexityCalculator()

    def test_file_count_scoring_0_2_files(self):
        """Test file complexity: 0-2 files = 0 points."""
        plan = ImplementationPlan(
            task_id="TEST-001",
            files_to_create=["file1.py"],
            raw_plan="Simple single file change"
        )
        context = EvaluationContext(
            task_id="TEST-001",
            technology_stack="python",
            implementation_plan=plan
        )

        factor = FileComplexityFactor()
        score = factor.evaluate(context)

        assert score.score == 0, f"Expected score 0 for 1 file, got {score.score}"
        assert score.max_score == 3
        assert "simple" in score.justification.lower()

    def test_file_count_scoring_3_5_files(self):
        """Test file complexity: 3-5 files = 1 point."""
        plan = ImplementationPlan(
            task_id="TEST-002",
            files_to_create=["file1.py", "file2.py", "file3.py", "file4.py"],
            raw_plan="Multi-file change"
        )
        context = EvaluationContext(
            task_id="TEST-002",
            technology_stack="python",
            implementation_plan=plan
        )

        factor = FileComplexityFactor()
        score = factor.evaluate(context)

        assert score.score == 1, f"Expected score 1 for 4 files, got {score.score}"
        assert "moderate" in score.justification.lower()

    def test_file_count_scoring_6_8_files(self):
        """Test file complexity: 6-8 files = 2 points."""
        plan = ImplementationPlan(
            task_id="TEST-003",
            files_to_create=[f"file{i}.py" for i in range(1, 8)],
            raw_plan="Complex multi-file change"
        )
        context = EvaluationContext(
            task_id="TEST-003",
            technology_stack="python",
            implementation_plan=plan
        )

        factor = FileComplexityFactor()
        score = factor.evaluate(context)

        assert score.score == 2, f"Expected score 2 for 7 files, got {score.score}"
        assert "complex" in score.justification.lower()

    def test_file_count_scoring_9_plus_files(self):
        """Test file complexity: 9+ files = 3 points."""
        plan = ImplementationPlan(
            task_id="TEST-004",
            files_to_create=[f"file{i}.py" for i in range(1, 11)],
            raw_plan="Very complex cross-cutting change"
        )
        context = EvaluationContext(
            task_id="TEST-004",
            technology_stack="python",
            implementation_plan=plan
        )

        factor = FileComplexityFactor()
        score = factor.evaluate(context)

        assert score.score == 3, f"Expected score 3 for 10 files, got {score.score}"
        assert "very complex" in score.justification.lower()

    def test_pattern_familiarity_no_patterns(self):
        """Test pattern familiarity: no patterns = 0 points."""
        plan = ImplementationPlan(
            task_id="TEST-005",
            patterns_used=[],
            raw_plan="Simple straightforward implementation"
        )
        context = EvaluationContext(
            task_id="TEST-005",
            technology_stack="python",
            implementation_plan=plan
        )

        factor = PatternFamiliarityFactor()
        score = factor.evaluate(context)

        assert score.score == 0
        assert "straightforward" in score.justification.lower()

    def test_pattern_familiarity_moderate_patterns(self):
        """Test pattern familiarity: moderate patterns = 1 point."""
        plan = ImplementationPlan(
            task_id="TEST-006",
            patterns_used=["Strategy", "Observer"],
            raw_plan="Using Strategy and Observer patterns"
        )
        context = EvaluationContext(
            task_id="TEST-006",
            technology_stack="python",
            implementation_plan=plan
        )

        factor = PatternFamiliarityFactor()
        score = factor.evaluate(context)

        assert score.score == 1
        assert "moderate" in score.justification.lower()

    def test_pattern_familiarity_advanced_patterns(self):
        """Test pattern familiarity: advanced patterns = 2 points."""
        plan = ImplementationPlan(
            task_id="TEST-007",
            patterns_used=["CQRS", "Event Sourcing"],
            raw_plan="Using CQRS and Event Sourcing patterns"
        )
        context = EvaluationContext(
            task_id="TEST-007",
            technology_stack="python",
            implementation_plan=plan
        )

        factor = PatternFamiliarityFactor()
        score = factor.evaluate(context)

        assert score.score == 2
        assert "advanced" in score.justification.lower()

    def test_risk_level_no_risk(self):
        """Test risk level: no risk indicators = 0 points."""
        plan = ImplementationPlan(
            task_id="TEST-008",
            raw_plan="Simple utility function with basic logic"
        )
        context = EvaluationContext(
            task_id="TEST-008",
            technology_stack="python",
            implementation_plan=plan
        )

        factor = RiskLevelFactor()
        score = factor.evaluate(context)

        assert score.score == 0
        assert "low risk" in score.justification.lower()

    def test_risk_level_moderate_risk(self):
        """Test risk level: 1-2 risk categories = 1 point."""
        plan = ImplementationPlan(
            task_id="TEST-009",
            raw_plan="API integration with external REST service for data retrieval"
        )
        context = EvaluationContext(
            task_id="TEST-009",
            technology_stack="python",
            implementation_plan=plan
        )

        factor = RiskLevelFactor()
        score = factor.evaluate(context)

        assert score.score == 1
        assert "moderate" in score.justification.lower()

    def test_risk_level_high_risk(self):
        """Test risk level: 3-4 risk categories = 2 points."""
        plan = ImplementationPlan(
            task_id="TEST-010",
            raw_plan="""
            OAuth2 authentication with JWT tokens
            External API integration with GitHub and Google
            Database migration to add user_sessions table
            Performance optimization with caching
            """
        )
        context = EvaluationContext(
            task_id="TEST-010",
            technology_stack="python",
            implementation_plan=plan
        )

        factor = RiskLevelFactor()
        score = factor.evaluate(context)

        assert score.score >= 2
        assert "high" in score.justification.lower() or "critical" in score.justification.lower()

    def test_score_aggregation_simple_task(self):
        """Test total score aggregation for simple task."""
        plan = ImplementationPlan(
            task_id="TEST-011",
            files_to_create=["utils.py"],
            patterns_used=[],
            raw_plan="Simple utility function"
        )
        context = EvaluationContext(
            task_id="TEST-011",
            technology_stack="python",
            implementation_plan=plan
        )

        complexity_score = self.calculator.calculate(context)

        assert 1 <= complexity_score.total_score <= 3
        assert complexity_score.review_mode == ReviewMode.AUTO_PROCEED

    def test_score_aggregation_moderate_task(self):
        """Test total score aggregation for moderate task."""
            task_id="TEST-012",
            files_to_create=["service.py", "repository.py", "model.py", "validator.py", "tests.py", "config.py"],
            patterns_used=["Repository", "Strategy"],
            raw_plan="Service layer with repository pattern, external API integration, and performance caching"
            task_id="TEST-012",
            files_to_create=["service.py", "repository.py", "model.py", "validator.py", "tests.py", "config.py"],
            patterns_used=["Repository", "Strategy"],
            raw_plan="Service layer with repository pattern, external API integration, and performance caching"
            task_id="TEST-012",
            files_to_create=["service.py", "repository.py", "model.py", "validator.py", "tests.py", "config.py"],
            patterns_used=["Repository", "Strategy"],
            raw_plan="Service layer with repository pattern, external API integration, and performance caching"
            task_id="TEST-012",
            files_to_create=["service.py", "repository.py", "model.py", "validator.py", "tests.py", "config.py"],
            patterns_used=["Repository", "Strategy"],
            raw_plan="Service layer with repository pattern, external API integration, and performance caching"
            task_id="TEST-012",
            files_to_create=["service.py", "repository.py", "model.py", "validator.py", "tests.py", "config.py"],
            patterns_used=["Repository", "Strategy"],
            raw_plan="Service layer with repository pattern, external API integration, and performance caching"
            task_id="TEST-012",
            files_to_create=["service.py", "repository.py", "model.py", "validator.py", "tests.py", "config.py"],
            patterns_used=["Repository", "Strategy"],
            raw_plan="Service layer with repository pattern, external API integration, and performance caching"
        context = EvaluationContext(
            task_id="TEST-012",
            technology_stack="python",
            implementation_plan=plan
        )

        complexity_score = self.calculator.calculate(context)

        assert 4 <= complexity_score.total_score <= 6
        assert complexity_score.review_mode == ReviewMode.QUICK_OPTIONAL

    def test_score_aggregation_complex_task(self):
        """Test total score aggregation for complex task."""
        plan = ImplementationPlan(
            task_id="TEST-013",
            files_to_create=[f"module{i}.py" for i in range(1, 10)],
            patterns_used=["CQRS", "Event Sourcing", "Saga"],
            raw_plan="""
            OAuth2 authentication system with JWT tokens
            Multiple external API integrations
            Database schema migration
            Performance optimization with caching
            Security encryption and authorization
            """
        )
        context = EvaluationContext(
            task_id="TEST-013",
            technology_stack="python",
            implementation_plan=plan
        )

        complexity_score = self.calculator.calculate(context)

        assert complexity_score.total_score >= 7
        assert complexity_score.review_mode == ReviewMode.FULL_REQUIRED

    def test_score_capping_at_10(self):
        """Test that score caps at maximum of 10."""
        plan = ImplementationPlan(
            task_id="TEST-014",
            files_to_create=[f"file{i}.py" for i in range(1, 50)],  # Way too many files
            patterns_used=["CQRS", "Event Sourcing", "Saga", "Mediator"],
            raw_plan="""
            Extremely complex system with authentication, authorization,
            encryption, security, database migration, schema changes,
            external API integration, performance optimization, caching,
            real-time streaming, and more...
            """
        )
        context = EvaluationContext(
            task_id="TEST-014",
            technology_stack="python",
            implementation_plan=plan
        )

        complexity_score = self.calculator.calculate(context)

        assert complexity_score.total_score <= 10, "Score should be capped at 10"

    def test_error_handling_malformed_plan(self):
        """Test error handling with malformed implementation plan."""
        # Create a plan that might cause issues
        plan = ImplementationPlan(
            task_id="TEST-015",
            files_to_create=[],
            raw_plan=""
        )
        context = EvaluationContext(
            task_id="TEST-015",
            technology_stack="python",
            implementation_plan=plan
        )

        # Should not crash, should return fail-safe score
        complexity_score = self.calculator.calculate(context)

        assert complexity_score is not None
        assert isinstance(complexity_score.total_score, int)
        assert 1 <= complexity_score.total_score <= 10


# ============================================================================
# UNIT TESTS - ReviewRouter
# ============================================================================

class TestReviewRouter:
    """Tests for ReviewRouter class."""

    def setup_method(self):
        """Setup test fixtures."""
        self.router = ReviewRouter()

    def test_auto_proceed_routing_score_1(self):
        """Test routing for score 1 (auto-proceed)."""
        complexity_score = ComplexityScore(
            total_score=1,
            factor_scores=[],
            forced_review_triggers=[],
            review_mode=ReviewMode.AUTO_PROCEED,
            calculation_timestamp=datetime.now()
        )
        plan = ImplementationPlan(task_id="TEST-016", raw_plan="Simple task")
        context = EvaluationContext(
            task_id="TEST-016",
            technology_stack="python",
            implementation_plan=plan
        )

        decision = self.router.route(complexity_score, context)

        assert decision.action == "proceed"
        assert decision.routing_recommendation == "Phase 3"
        assert decision.auto_approved is True

    def test_auto_proceed_routing_score_3(self):
        """Test routing for score 3 (auto-proceed boundary)."""
        complexity_score = ComplexityScore(
            total_score=3,
            factor_scores=[],
            forced_review_triggers=[],
            review_mode=ReviewMode.AUTO_PROCEED,
            calculation_timestamp=datetime.now()
        )
        plan = ImplementationPlan(task_id="TEST-017", raw_plan="Simple task")
        context = EvaluationContext(
            task_id="TEST-017",
            technology_stack="python",
            implementation_plan=plan
        )

        decision = self.router.route(complexity_score, context)

        assert decision.action == "proceed"
        assert decision.auto_approved is True

    def test_quick_optional_routing_score_4(self):
        """Test routing for score 4 (quick optional lower boundary)."""
        complexity_score = ComplexityScore(
            total_score=4,
            factor_scores=[],
            forced_review_triggers=[],
            review_mode=ReviewMode.QUICK_OPTIONAL,
            calculation_timestamp=datetime.now()
        )
        plan = ImplementationPlan(task_id="TEST-018", raw_plan="Moderate task")
        context = EvaluationContext(
            task_id="TEST-018",
            technology_stack="python",
            implementation_plan=plan
        )

        decision = self.router.route(complexity_score, context)

        assert decision.action == "review_required"
        assert "Optional" in decision.routing_recommendation
        assert decision.auto_approved is False

    def test_quick_optional_routing_score_6(self):
        """Test routing for score 6 (quick optional upper boundary)."""
        complexity_score = ComplexityScore(
            total_score=6,
            factor_scores=[],
            forced_review_triggers=[],
            review_mode=ReviewMode.QUICK_OPTIONAL,
            calculation_timestamp=datetime.now()
        )
        plan = ImplementationPlan(task_id="TEST-019", raw_plan="Moderate task")
        context = EvaluationContext(
            task_id="TEST-019",
            technology_stack="python",
            implementation_plan=plan
        )

        decision = self.router.route(complexity_score, context)

        assert decision.action == "review_required"
        assert "Optional" in decision.routing_recommendation

    def test_full_required_routing_score_7(self):
        """Test routing for score 7 (full required lower boundary)."""
        complexity_score = ComplexityScore(
            total_score=7,
            factor_scores=[],
            forced_review_triggers=[],
            review_mode=ReviewMode.FULL_REQUIRED,
            calculation_timestamp=datetime.now()
        )
        plan = ImplementationPlan(task_id="TEST-020", raw_plan="Complex task")
        context = EvaluationContext(
            task_id="TEST-020",
            technology_stack="python",
            implementation_plan=plan
        )

        decision = self.router.route(complexity_score, context)

        assert decision.action == "review_required"
        assert "Required" in decision.routing_recommendation
        assert decision.auto_approved is False

    def test_full_required_routing_score_10(self):
        """Test routing for score 10 (full required maximum)."""
        complexity_score = ComplexityScore(
            total_score=10,
            factor_scores=[],
            forced_review_triggers=[],
            review_mode=ReviewMode.FULL_REQUIRED,
            calculation_timestamp=datetime.now()
        )
        plan = ImplementationPlan(task_id="TEST-021", raw_plan="Very complex task")
        context = EvaluationContext(
            task_id="TEST-021",
            technology_stack="python",
            implementation_plan=plan
        )

        decision = self.router.route(complexity_score, context)

        assert decision.action == "review_required"
        assert "Required" in decision.routing_recommendation

    def test_force_trigger_overrides_low_score(self):
        """Test that force trigger overrides low complexity score."""
        complexity_score = ComplexityScore(
            total_score=2,  # Would normally auto-proceed
            factor_scores=[],
            forced_review_triggers=[ForceReviewTrigger.SECURITY_KEYWORDS],
            review_mode=ReviewMode.FULL_REQUIRED,  # Overridden by trigger
            calculation_timestamp=datetime.now()
        )
        plan = ImplementationPlan(task_id="TEST-022", raw_plan="Security-related task")
        context = EvaluationContext(
            task_id="TEST-022",
            technology_stack="python",
            implementation_plan=plan
        )

        decision = self.router.route(complexity_score, context)

        assert decision.action == "review_required"
        assert "Required" in decision.routing_recommendation
        assert decision.auto_approved is False

    def test_routing_decision_generation(self):
        """Test that routing decision includes proper summary message."""
        complexity_score = ComplexityScore(
            total_score=5,
            factor_scores=[
                FactorScore(
                    factor_name="file_complexity",
                    score=1,
                    max_score=3,
                    justification="Moderate file count"
                )
            ],
            forced_review_triggers=[],
            review_mode=ReviewMode.QUICK_OPTIONAL,
            calculation_timestamp=datetime.now()
        )
        plan = ImplementationPlan(task_id="TEST-023", raw_plan="Moderate task")
        context = EvaluationContext(
            task_id="TEST-023",
            technology_stack="python",
            implementation_plan=plan
        )

        decision = self.router.route(complexity_score, context)

        assert len(decision.summary_message) > 0
        assert "TEST-023" in decision.summary_message
        assert str(complexity_score.total_score) in decision.summary_message


# ============================================================================
# UNIT TESTS - Force Trigger Detection
# ============================================================================

class TestForceTriggerDetection:
    """Tests for force-review trigger detection."""

    def setup_method(self):
        """Setup test fixtures."""
        self.calculator = ComplexityCalculator()

    def test_user_flag_detection(self):
        """Test detection of user --review flag."""
        plan = ImplementationPlan(task_id="TEST-024", raw_plan="Simple task")
        context = EvaluationContext(
            task_id="TEST-024",
            technology_stack="python",
            implementation_plan=plan,
            user_flags={"review": True}
        )

        complexity_score = self.calculator.calculate(context)

        assert ForceReviewTrigger.USER_FLAG in complexity_score.forced_review_triggers
        assert complexity_score.review_mode == ReviewMode.FULL_REQUIRED

    def test_security_keyword_detection(self):
        """Test detection of security-sensitive keywords."""
        plan = ImplementationPlan(
            task_id="TEST-025",
            raw_plan="Implement JWT token authentication with OAuth2 and encryption"
        )
        context = EvaluationContext(
            task_id="TEST-025",
            technology_stack="python",
            implementation_plan=plan
        )

        complexity_score = self.calculator.calculate(context)

        assert ForceReviewTrigger.SECURITY_KEYWORDS in complexity_score.forced_review_triggers
        assert complexity_score.review_mode == ReviewMode.FULL_REQUIRED

    def test_breaking_changes_detection(self):
        """Test detection of breaking API changes."""
        plan = ImplementationPlan(
            task_id="TEST-026",
            raw_plan="This is a breaking change that removes the old endpoint API"
        )
        context = EvaluationContext(
            task_id="TEST-026",
            technology_stack="python",
            implementation_plan=plan
        )

        complexity_score = self.calculator.calculate(context)

        assert ForceReviewTrigger.BREAKING_CHANGES in complexity_score.forced_review_triggers
        assert complexity_score.review_mode == ReviewMode.FULL_REQUIRED

    def test_schema_changes_detection(self):
        """Test detection of database schema modifications."""
        plan = ImplementationPlan(
            task_id="TEST-027",
            raw_plan="Database migration to alter table structure and add new schema"
        )
        context = EvaluationContext(
            task_id="TEST-027",
            technology_stack="python",
            implementation_plan=plan
        )

        complexity_score = self.calculator.calculate(context)

        assert ForceReviewTrigger.SCHEMA_CHANGES in complexity_score.forced_review_triggers
        assert complexity_score.review_mode == ReviewMode.FULL_REQUIRED

    def test_hotfix_detection(self):
        """Test detection of production hotfix."""
        plan = ImplementationPlan(task_id="TEST-028", raw_plan="Urgent bug fix")
        context = EvaluationContext(
            task_id="TEST-028",
            technology_stack="python",
            implementation_plan=plan,
            task_metadata={"is_hotfix": True}
        )

        complexity_score = self.calculator.calculate(context)

        assert ForceReviewTrigger.HOTFIX in complexity_score.forced_review_triggers
        assert complexity_score.review_mode == ReviewMode.FULL_REQUIRED

    def test_multiple_triggers(self):
        """Test detection of multiple force-review triggers."""
        plan = ImplementationPlan(
            task_id="TEST-029",
            raw_plan="""
            Breaking change to authentication API
            Database schema migration
            Security encryption updates
            """
        )
        context = EvaluationContext(
            task_id="TEST-029",
            technology_stack="python",
            implementation_plan=plan,
            user_flags={"review": True}
        )

        complexity_score = self.calculator.calculate(context)

        assert len(complexity_score.forced_review_triggers) >= 2
        assert complexity_score.review_mode == ReviewMode.FULL_REQUIRED


# ============================================================================
# INTEGRATION TESTS - End-to-End Flows
# ============================================================================

class TestIntegrationFlows:
    """End-to-end integration tests."""

    def test_end_to_end_simple_task(self):
        """Test complete flow: simple task (score 2) → auto_proceed."""
        plan_text = """
        Simple bug fix in email validator
        Files: src/validators/email.py
        """

        plan = parse_implementation_plan(plan_text, "TASK-E2E-001")
        context = build_evaluation_context(
            task_id="TASK-E2E-001",
            technology_stack="python",
            implementation_plan=plan
        )

        calculator = ComplexityCalculator()
        complexity_score = calculator.calculate(context)

        router = ReviewRouter()
        decision = router.route(complexity_score, context)

        assert complexity_score.total_score <= 3
        assert decision.action == "proceed"
        assert decision.routing_recommendation == "Phase 3"

    def test_end_to_end_medium_task(self):
        """Test complete flow: medium task (score 5) → quick_optional."""
        plan_text = """
        User profile service implementation

        Files:
        - src/services/user_service.py
        - src/repositories/user_repository.py
        - src/models/user.py
        - src/validators/profile_validator.py

        Patterns: Repository pattern
        External API integration for user data
        """

        plan = parse_implementation_plan(plan_text, "TASK-E2E-002")
        context = build_evaluation_context(
            task_id="TASK-E2E-002",
            technology_stack="python",
            implementation_plan=plan
        )

        calculator = ComplexityCalculator()
        complexity_score = calculator.calculate(context)

        router = ReviewRouter()
        decision = router.route(complexity_score, context)

        assert 4 <= complexity_score.total_score <= 6
        assert decision.action == "review_required"
        assert "Optional" in decision.routing_recommendation

    def test_end_to_end_complex_task(self):
        """Test complete flow: complex task (score 8) → full_required."""
        plan_text = """
        OAuth2 Authentication System

        Files:
        - src/auth/oauth_service.py
        - src/auth/token_manager.py
        - src/auth/jwt_handler.py
        - src/auth/provider_factory.py
        - src/middleware/auth_middleware.py
        - src/models/user_session.py
        - src/repositories/session_repository.py
        - tests/test_oauth.py

        Patterns: Strategy, Factory, Circuit Breaker

        External dependencies:
        - Google OAuth API
        - GitHub OAuth API
        - PostgreSQL database

        Security: JWT encryption, OAuth2 validation
        Database migration: Create user_sessions table
        """

        plan = parse_implementation_plan(plan_text, "TASK-E2E-003")
        context = build_evaluation_context(
            task_id="TASK-E2E-003",
            technology_stack="python",
            implementation_plan=plan
        )

        calculator = ComplexityCalculator()
        complexity_score = calculator.calculate(context)

        router = ReviewRouter()
        decision = router.route(complexity_score, context)

        assert complexity_score.total_score >= 7 or complexity_score.has_forced_triggers
        assert decision.action == "review_required"
        assert "Required" in decision.routing_recommendation

    def test_end_to_end_triggered_task(self):
        """Test complete flow: triggered task (score 3 + security) → full_required."""
        plan_text = """
        Simple password reset utility

        Files:
        - src/auth/password_reset.py

        Implements password hashing and token generation
        """

        plan = parse_implementation_plan(plan_text, "TASK-E2E-004")
        context = build_evaluation_context(
            task_id="TASK-E2E-004",
            technology_stack="python",
            implementation_plan=plan
        )

        calculator = ComplexityCalculator()
        complexity_score = calculator.calculate(context)

        router = ReviewRouter()
        decision = router.route(complexity_score, context)

        # Low file score but security trigger should force full review
        assert complexity_score.has_forced_triggers
        assert ForceReviewTrigger.SECURITY_KEYWORDS in complexity_score.forced_review_triggers
        assert decision.action == "review_required"
        assert "Required" in decision.routing_recommendation


# ============================================================================
# UNIT TESTS - Agent Utils
# ============================================================================

class TestAgentUtils:
    """Tests for agent utility functions."""

    def test_parse_implementation_plan_with_files(self):
        """Test parsing files from implementation plan."""
        plan_text = """
        Files to create:
        - src/services/user_service.py
        - src/models/user.py
        - `src/repositories/user_repository.py`
        """

        plan = parse_implementation_plan(plan_text, "TASK-UTILS-001")

        assert len(plan.files_to_create) >= 2
        assert plan.task_id == "TASK-UTILS-001"

    def test_parse_implementation_plan_with_patterns(self):
        """Test parsing design patterns from plan."""
        plan_text = """
        Using Repository pattern for data access
        Factory pattern for object creation
        Strategy pattern for validation
        """

        plan = parse_implementation_plan(plan_text, "TASK-UTILS-002")

        assert len(plan.patterns_used) >= 2
        assert any("Repository" in p for p in plan.patterns_used)

    def test_parse_implementation_plan_with_dependencies(self):
        """Test parsing external dependencies from plan."""
        plan_text = """
        External API: https://api.example.com
        Database: PostgreSQL
        Third-party service: Stripe
        """

        plan = parse_implementation_plan(plan_text, "TASK-UTILS-003")

        assert len(plan.external_dependencies) > 0

    def test_build_evaluation_context(self):
        """Test building evaluation context."""
        plan = ImplementationPlan(task_id="TEST-CTX", raw_plan="Test plan")

        context = build_evaluation_context(
            task_id="TEST-CTX",
            technology_stack="python",
            implementation_plan=plan,
            task_metadata={"priority": "high"},
            user_flags={"review": True}
        )

        assert context.task_id == "TEST-CTX"
        assert context.technology_stack == "python"
        assert context.user_requested_review is True

    def test_format_decision_for_display(self):
        """Test formatting decision for terminal display."""
        complexity_score = ComplexityScore(
            total_score=5,
            factor_scores=[],
            forced_review_triggers=[],
            review_mode=ReviewMode.QUICK_OPTIONAL,
            calculation_timestamp=datetime.now()
        )
        plan = ImplementationPlan(task_id="TEST-FMT", raw_plan="Test")
        context = EvaluationContext(
            task_id="TEST-FMT",
            technology_stack="python",
            implementation_plan=plan
        )

        from lib.review_router import ReviewDecision
        decision = ReviewDecision(
            action="review_required",
            complexity_score=complexity_score,
            routing_recommendation="Phase 2.6 Checkpoint (Optional)",
            summary_message="Test summary",
            auto_approved=False,
            timestamp=datetime.now()
        )

        formatted = format_decision_for_display(decision)

        assert len(formatted) > 0
        assert "COMPLEXITY EVALUATION" in formatted.upper()

    def test_format_decision_for_metadata(self):
        """Test formatting decision for task metadata."""
        complexity_score = ComplexityScore(
            total_score=5,
            factor_scores=[
                FactorScore(
                    factor_name="file_complexity",
                    score=1,
                    max_score=3,
                    justification="Test"
                )
            ],
            forced_review_triggers=[],
            review_mode=ReviewMode.QUICK_OPTIONAL,
            calculation_timestamp=datetime.now()
        )
        plan = ImplementationPlan(task_id="TEST-META", raw_plan="Test")
        context = EvaluationContext(
            task_id="TEST-META",
            technology_stack="python",
            implementation_plan=plan
        )

        from lib.review_router import ReviewDecision
        decision = ReviewDecision(
            action="review_required",
            complexity_score=complexity_score,
            routing_recommendation="Phase 2.6",
            summary_message="Test",
            auto_approved=False,
            timestamp=datetime.now()
        )

        metadata = format_decision_for_metadata(decision)

        assert "complexity_evaluation" in metadata
        assert metadata["complexity_evaluation"]["score"] == 5
        assert len(metadata["complexity_evaluation"]["factors"]) == 1


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def main():
    """Run all tests without pytest."""
    print("\n" + "=" * 80)
    print("COMPREHENSIVE TEST SUITE - TASK-003A Complexity Evaluation")
    print("=" * 80 + "\n")

    test_classes = [
        TestComplexityCalculator,
        TestReviewRouter,
        TestForceTriggerDetection,
        TestIntegrationFlows,
        TestAgentUtils
    ]

    total_tests = 0
    passed_tests = 0
    failed_tests = []

    for test_class in test_classes:
        print(f"\nRunning {test_class.__name__}...")
        print("-" * 80)

        test_instance = test_class()
        test_methods = [m for m in dir(test_instance) if m.startswith("test_")]

        for method_name in test_methods:
            total_tests += 1
            try:
                if hasattr(test_instance, 'setup_method'):
                    test_instance.setup_method()

                method = getattr(test_instance, method_name)
                method()

                print(f"  ✓ {method_name}")
                passed_tests += 1

            except AssertionError as e:
                print(f"  ✗ {method_name}: {e}")
                failed_tests.append((test_class.__name__, method_name, str(e)))
            except Exception as e:
                print(f"  ✗ {method_name}: Unexpected error: {e}")
                failed_tests.append((test_class.__name__, method_name, str(e)))

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {len(failed_tests)}")

    if failed_tests:
        print("\nFailed Tests:")
        for test_class, method, error in failed_tests:
            print(f"  - {test_class}.{method}: {error}")
        return 1
    else:
        print("\n✅ ALL TESTS PASSED")
        return 0


if __name__ == "__main__":
    sys.exit(main())
