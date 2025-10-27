#!/usr/bin/env python3
"""
Test script for complexity evaluation system.

This script verifies that all components work correctly:
1. Parsing implementation plans
2. Calculating complexity scores
3. Routing to review modes
4. Formatting decisions

Run: python test_complexity.py
"""

import sys
from pathlib import Path

# Add parent directory to path to import as package
lib_path = Path(__file__).parent
parent_path = lib_path.parent
sys.path.insert(0, str(parent_path))

from lib.complexity_models import EvaluationContext
from lib.complexity_calculator import ComplexityCalculator
from lib.review_router import ReviewRouter
from lib.agent_utils import (
    parse_implementation_plan,
    build_evaluation_context,
    format_decision_for_display
)


def test_simple_task():
    """Test simple task (score 1-3, auto-proceed)."""
    print("=" * 80)
    print("TEST 1: Simple Task (Auto-Proceed)")
    print("=" * 80)

    plan_text = """
    Implementation Plan for TASK-001: Add email validation

    Files to create:
    - src/validators/email_validator.py

    No external dependencies.
    Simple validation logic using regex.
    """

    task_id = "TASK-001"
    stack = "python"

    # Parse plan
    plan = parse_implementation_plan(plan_text, task_id)
    print(f"Parsed {len(plan.files_to_create)} files")

    # Build context
    context = build_evaluation_context(
        task_id=task_id,
        technology_stack=stack,
        implementation_plan=plan
    )

    # Calculate complexity
    calculator = ComplexityCalculator()
    complexity_score = calculator.calculate(context)
    print(f"Complexity Score: {complexity_score.total_score}/10")
    print(f"Review Mode: {complexity_score.review_mode.value}")

    # Route
    router = ReviewRouter()
    decision = router.route(complexity_score, context)
    print(f"Action: {decision.action}")
    print(f"Routing: {decision.routing_recommendation}")

    # Display
    print(format_decision_for_display(decision))

    assert complexity_score.total_score <= 3, "Expected simple task (score <= 3)"
    assert decision.action == "proceed", "Expected auto-proceed"
    print("✅ Test 1 PASSED\n")


def test_moderate_task():
    """Test moderate task (score 4-6, optional review)."""
    print("=" * 80)
    print("TEST 2: Moderate Task (Optional Review)")
    print("=" * 80)

    plan_text = """
    Implementation Plan for TASK-002: User Profile Service

    Files to create:
    - src/services/user_service.py
    - src/repositories/user_repository.py
    - src/models/user.py
    - src/models/profile.py
    - src/validators/profile_validator.py
    - tests/test_user_service.py

    Design patterns:
    - Repository pattern for data access
    - Strategy pattern for profile validation

    External dependencies:
    - REST API endpoint for user data
    - Third-party image storage (S3)

    Performance considerations:
    - Profile data caching for high-traffic endpoints
    """

    task_id = "TASK-002"
    stack = "python"

    plan = parse_implementation_plan(plan_text, task_id)
    print(f"Parsed {len(plan.files_to_create)} files")

    context = build_evaluation_context(
        task_id=task_id,
        technology_stack=stack,
        implementation_plan=plan
    )

    calculator = ComplexityCalculator()
    complexity_score = calculator.calculate(context)
    print(f"Complexity Score: {complexity_score.total_score}/10")
    print(f"Review Mode: {complexity_score.review_mode.value}")

    router = ReviewRouter()
    decision = router.route(complexity_score, context)
    print(f"Action: {decision.action}")
    print(f"Routing: {decision.routing_recommendation}")

    print(format_decision_for_display(decision))

    assert 4 <= complexity_score.total_score <= 6, "Expected moderate task (score 4-6)"
    assert decision.action == "review_required", "Expected optional review"
    print("✅ Test 2 PASSED\n")


def test_complex_task():
    """Test complex task (score 7-10, full review)."""
    print("=" * 80)
    print("TEST 3: Complex Task (Full Review Required)")
    print("=" * 80)

    plan_text = """
    Implementation Plan for TASK-003: OAuth2 Authentication System

    Files to create:
    - src/auth/oauth_service.py
    - src/auth/token_manager.py
    - src/auth/jwt_handler.py
    - src/auth/provider_factory.py
    - src/middleware/auth_middleware.py
    - src/models/user_session.py
    - src/repositories/session_repository.py
    - tests/test_oauth_service.py
    - tests/test_token_manager.py

    Design patterns:
    - Strategy pattern for multiple OAuth providers
    - Factory pattern for provider instantiation
    - Circuit Breaker for external API resilience

    External dependencies:
    - Google OAuth API
    - GitHub OAuth API
    - PostgreSQL for session storage
    - Redis for token caching

    Security considerations:
    - JWT token encryption
    - OAuth2 state validation
    - PKCE implementation
    - Token refresh mechanism

    Database schema changes:
    - Create user_sessions table
    - Add oauth_providers table
    - Migration for token storage
    """

    task_id = "TASK-003"
    stack = "python"

    plan = parse_implementation_plan(plan_text, task_id)
    print(f"Parsed {len(plan.files_to_create)} files")
    print(f"Patterns: {plan.patterns_used}")

    context = build_evaluation_context(
        task_id=task_id,
        technology_stack=stack,
        implementation_plan=plan
    )

    calculator = ComplexityCalculator()
    complexity_score = calculator.calculate(context)
    print(f"Complexity Score: {complexity_score.total_score}/10")
    print(f"Review Mode: {complexity_score.review_mode.value}")
    print(f"Force Triggers: {[t.value for t in complexity_score.forced_review_triggers]}")

    router = ReviewRouter()
    decision = router.route(complexity_score, context)
    print(f"Action: {decision.action}")
    print(f"Routing: {decision.routing_recommendation}")

    print(format_decision_for_display(decision))

    assert complexity_score.total_score >= 7 or complexity_score.has_forced_triggers, \
        "Expected complex task or forced triggers"
    assert decision.action == "review_required", "Expected full review"
    print("✅ Test 3 PASSED\n")


def test_forced_trigger():
    """Test forced review trigger (user flag)."""
    print("=" * 80)
    print("TEST 4: Forced Review Trigger (User Flag)")
    print("=" * 80)

    plan_text = """
    Simple bug fix in utility function.

    Files to modify:
    - src/utils/string_helper.py
    """

    task_id = "TASK-004"
    stack = "python"

    plan = parse_implementation_plan(plan_text, task_id)

    context = build_evaluation_context(
        task_id=task_id,
        technology_stack=stack,
        implementation_plan=plan,
        user_flags={"review": True}  # User explicitly requested review
    )

    calculator = ComplexityCalculator()
    complexity_score = calculator.calculate(context)
    print(f"Complexity Score: {complexity_score.total_score}/10")
    print(f"Review Mode: {complexity_score.review_mode.value}")
    print(f"Force Triggers: {[t.value for t in complexity_score.forced_review_triggers]}")

    router = ReviewRouter()
    decision = router.route(complexity_score, context)
    print(f"Action: {decision.action}")
    print(f"Routing: {decision.routing_recommendation}")

    print(format_decision_for_display(decision))

    assert complexity_score.has_forced_triggers, "Expected forced trigger"
    assert decision.action == "review_required", "Expected forced review"
    print("✅ Test 4 PASSED\n")


def test_error_handling():
    """Test error handling (fail-safe to score=10)."""
    print("=" * 80)
    print("TEST 5: Error Handling (Fail-Safe)")
    print("=" * 80)

    # Intentionally malformed data to trigger error
    plan_text = ""  # Empty plan

    task_id = "TASK-005"
    stack = "python"

    plan = parse_implementation_plan(plan_text, task_id)
    context = build_evaluation_context(
        task_id=task_id,
        technology_stack=stack,
        implementation_plan=plan
    )

    calculator = ComplexityCalculator()
    complexity_score = calculator.calculate(context)
    print(f"Complexity Score: {complexity_score.total_score}/10")
    print(f"Review Mode: {complexity_score.review_mode.value}")

    # Should handle gracefully (not crash)
    router = ReviewRouter()
    decision = router.route(complexity_score, context)
    print(f"Action: {decision.action}")
    print(f"Routing: {decision.routing_recommendation}")

    print("✅ Test 5 PASSED (no crash)\n")


def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("COMPLEXITY EVALUATION SYSTEM - TEST SUITE")
    print("=" * 80 + "\n")

    try:
        test_simple_task()
        test_moderate_task()
        test_complex_task()
        test_forced_trigger()
        test_error_handling()

        print("=" * 80)
        print("ALL TESTS PASSED ✅")
        print("=" * 80)
        return 0

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
