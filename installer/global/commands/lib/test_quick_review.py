#!/usr/bin/env python3
"""
Test suite for Quick Review Mode implementation.

Tests:
1. Platform-specific input strategies (Unix/Windows)
2. Countdown timer with user interactions
3. Quick review display rendering
4. Quick review handler workflow
5. Error handling and fail-safe behavior

Run: python test_quick_review.py
"""

import sys
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

# Add parent directory to path to import as package
lib_path = Path(__file__).parent
parent_path = lib_path.parent
sys.path.insert(0, str(parent_path))

from lib.user_interaction import (
    UnixInputStrategy,
    WindowsInputStrategy,
    create_input_strategy,
    countdown_timer,
)
from lib.review_modes import (
    QuickReviewResult,
    QuickReviewDisplay,
    QuickReviewHandler,
)
from lib.complexity_models import (
    ImplementationPlan,
    ComplexityScore,
    ReviewMode,
    FactorScore,
)


def create_test_plan(score: int = 87, num_files: int = 3) -> ImplementationPlan:
    """Create a test implementation plan."""
    from datetime import datetime, timezone

    files = [f"src/module_{i}.py" for i in range(num_files)]

    factor_scores = [
        FactorScore(
            factor_name="file_complexity",
            score=2.0,
            max_score=3.0,
            justification="3 files to create"
        ),
        FactorScore(
            factor_name="dependency_complexity",
            score=1.0,
            max_score=2.0,
            justification="No external dependencies"
        ),
    ]

    # Map score (0-100) to total_score (1-10)
    total_score = max(1, min(10, int(score / 10)))

    complexity_score = ComplexityScore(
        total_score=total_score,
        factor_scores=factor_scores,
        forced_review_triggers=[],
        review_mode=ReviewMode.QUICK_OPTIONAL if score >= 60 else ReviewMode.FULL_REQUIRED,
        calculation_timestamp=datetime.now(timezone.utc),
        metadata={
            "patterns_detected": ["Strategy Pattern", "Context Manager", "Factory"],
            "warnings": ["Consider adding more error handling"] if score < 80 else [],
        }
    )

    # Create plan that matches actual ImplementationPlan structure
    plan = ImplementationPlan(
        task_id="TASK-001",
        files_to_create=files,
        patterns_used=["Strategy Pattern", "Context Manager"],
        external_dependencies=[],
        estimated_loc=num_files * 100,
        risk_indicators=[],
        raw_plan="Implement feature following approved architecture"
    )

    # Attach complexity score and additional attributes for display compatibility
    plan.complexity_score = complexity_score
    plan.implementation_instructions = "Implement feature following approved architecture"

    # Add overall_score as a separate attribute on the plan for display (0-100 scale)
    plan.display_score = score

    return plan


def test_unix_input_strategy():
    """Test Unix input strategy (select-based)."""
    print("=" * 80)
    print("TEST 1: Unix Input Strategy")
    print("=" * 80)

    if sys.platform == "win32":
        print("⏭️  Skipped on Windows platform\n")
        return

    if not sys.stdin.isatty():
        print("⏭️  Skipped (not a TTY - stdin not interactive)\n")
        return

    strategy = UnixInputStrategy()

    # Test setup
    strategy.setup()
    print("✅ Setup completed without errors")

    # Test check_input (should return None with no input)
    result = strategy.check_input()
    assert result is None, "Expected None when no input available"
    print("✅ check_input returns None when no input")

    # Test cleanup
    strategy.cleanup()
    print("✅ Cleanup completed without errors")

    # Test multiple cleanup calls (should be safe)
    strategy.cleanup()
    print("✅ Multiple cleanup calls safe")

    print("✅ Test 1 PASSED\n")


def test_windows_input_strategy():
    """Test Windows input strategy (msvcrt-based)."""
    print("=" * 80)
    print("TEST 2: Windows Input Strategy")
    print("=" * 80)

    if sys.platform != "win32":
        print("⏭️  Skipped on Unix platform\n")
        return

    strategy = WindowsInputStrategy()

    # Test setup (no-op)
    strategy.setup()
    print("✅ Setup completed (no-op on Windows)")

    # Test check_input
    result = strategy.check_input()
    assert result is None, "Expected None when no input available"
    print("✅ check_input returns None when no input")

    # Test cleanup (no-op)
    strategy.cleanup()
    print("✅ Cleanup completed (no-op on Windows)")

    print("✅ Test 2 PASSED\n")


def test_input_strategy_factory():
    """Test input strategy factory function."""
    print("=" * 80)
    print("TEST 3: Input Strategy Factory")
    print("=" * 80)

    strategy = create_input_strategy()

    if sys.platform == "win32":
        assert isinstance(strategy, WindowsInputStrategy), "Expected WindowsInputStrategy"
        print("✅ Created WindowsInputStrategy on Windows")
    else:
        assert isinstance(strategy, UnixInputStrategy), "Expected UnixInputStrategy"
        print("✅ Created UnixInputStrategy on Unix")

    print("✅ Test 3 PASSED\n")


def test_countdown_timer_timeout():
    """Test countdown timer with timeout (no user input)."""
    print("=" * 80)
    print("TEST 4: Countdown Timer - Timeout")
    print("=" * 80)

    # Mock the input strategy to return None (no input)
    mock_strategy = Mock()
    mock_strategy.check_input = Mock(return_value=None)
    mock_strategy.setup = Mock()
    mock_strategy.cleanup = Mock()

    with patch('lib.user_interaction.create_input_strategy', return_value=mock_strategy):
        start_time = time.monotonic()
        result = countdown_timer(
            duration_seconds=1,  # Short duration for testing
            message="Test countdown",
            options="Options here"
        )
        elapsed = time.monotonic() - start_time

        assert result == "timeout", f"Expected 'timeout', got '{result}'"
        assert 0.9 <= elapsed <= 1.2, f"Expected ~1s, got {elapsed:.2f}s"
        print(f"✅ Countdown timed out after {elapsed:.2f}s")

        # Verify cleanup was called
        mock_strategy.cleanup.assert_called_once()
        print("✅ Cleanup called on exit")

    print("✅ Test 4 PASSED\n")


def test_countdown_timer_enter_key():
    """Test countdown timer with Enter key press."""
    print("=" * 80)
    print("TEST 5: Countdown Timer - Enter Key")
    print("=" * 80)

    # Mock the input strategy to return Enter key
    mock_strategy = Mock()
    call_count = [0]

    def mock_check_input():
        call_count[0] += 1
        # Return Enter on 3rd call (simulate user pressing Enter)
        if call_count[0] == 3:
            return '\n'
        return None

    mock_strategy.check_input = mock_check_input
    mock_strategy.setup = Mock()
    mock_strategy.cleanup = Mock()

    with patch('lib.user_interaction.create_input_strategy', return_value=mock_strategy):
        start_time = time.monotonic()
        result = countdown_timer(
            duration_seconds=10,
            message="Test countdown",
            options="Options here"
        )
        elapsed = time.monotonic() - start_time

        assert result == "enter", f"Expected 'enter', got '{result}'"
        assert elapsed < 1.0, f"Expected quick response, got {elapsed:.2f}s"
        print(f"✅ Enter key detected after {elapsed:.2f}s")

        # Verify cleanup was called
        mock_strategy.cleanup.assert_called_once()
        print("✅ Cleanup called on exit")

    print("✅ Test 5 PASSED\n")


def test_countdown_timer_cancel_key():
    """Test countdown timer with cancel key press."""
    print("=" * 80)
    print("TEST 6: Countdown Timer - Cancel Key")
    print("=" * 80)

    # Mock the input strategy to return 'c' key
    mock_strategy = Mock()
    call_count = [0]

    def mock_check_input():
        call_count[0] += 1
        # Return 'c' on 2nd call
        if call_count[0] == 2:
            return 'c'
        return None

    mock_strategy.check_input = mock_check_input
    mock_strategy.setup = Mock()
    mock_strategy.cleanup = Mock()

    with patch('lib.user_interaction.create_input_strategy', return_value=mock_strategy):
        start_time = time.monotonic()
        result = countdown_timer(
            duration_seconds=10,
            message="Test countdown",
            options="Options here",
            cancel_key="c"
        )
        elapsed = time.monotonic() - start_time

        assert result == "cancel", f"Expected 'cancel', got '{result}'"
        assert elapsed < 1.0, f"Expected quick response, got {elapsed:.2f}s"
        print(f"✅ Cancel key detected after {elapsed:.2f}s")

    print("✅ Test 6 PASSED\n")


def test_countdown_timer_invalid_duration():
    """Test countdown timer with invalid duration."""
    print("=" * 80)
    print("TEST 7: Countdown Timer - Invalid Duration")
    print("=" * 80)

    try:
        countdown_timer(
            duration_seconds=0,
            message="Test",
            options="Options"
        )
        assert False, "Expected ValueError"
    except ValueError as e:
        print(f"✅ ValueError raised: {e}")

    try:
        countdown_timer(
            duration_seconds=-5,
            message="Test",
            options="Options"
        )
        assert False, "Expected ValueError"
    except ValueError as e:
        print(f"✅ ValueError raised: {e}")

    print("✅ Test 7 PASSED\n")


def test_quick_review_display():
    """Test quick review display rendering."""
    print("=" * 80)
    print("TEST 8: Quick Review Display")
    print("=" * 80)

    plan = create_test_plan(score=87, num_files=3)
    display = QuickReviewDisplay(plan)

    # Test complexity badge
    badge = display.format_complexity_badge()
    assert "87/100" in badge, f"Expected score in badge: {badge}"
    assert "Excellent" in badge, f"Expected 'Excellent' label: {badge}"
    print(f"✅ Complexity badge: {badge}")

    # Test file summary
    summary = display.format_file_summary()
    assert "3 files" in summary, f"Expected '3 files': {summary}"
    # Note: estimated_loc might be formatted differently, just check files are counted
    print(f"✅ File summary: {summary}")

    # Test full render (check it doesn't crash)
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        display.render_summary_card()
        output = mock_stdout.getvalue()
        assert "ARCHITECTURAL REVIEW" in output, "Expected header in output"
        assert "87/100" in output, "Expected score in output"
        print("✅ Summary card rendered successfully")

    print("✅ Test 8 PASSED\n")


def test_quick_review_handler_timeout():
    """Test quick review handler with timeout."""
    print("=" * 80)
    print("TEST 9: Quick Review Handler - Timeout")
    print("=" * 80)

    plan = create_test_plan(score=87, num_files=3)
    handler = QuickReviewHandler(
        task_id="TASK-001",
        plan=plan,
        countdown_duration=1
    )

    # Mock countdown_timer to return timeout
    with patch('lib.review_modes.countdown_timer', return_value="timeout"):
        result = handler.execute()

        assert result.action == "timeout", f"Expected 'timeout', got '{result.action}'"
        assert result.auto_approved is True, "Expected auto_approved=True"
        assert "review_mode" in result.metadata_updates, "Expected review_mode in metadata"
        assert result.metadata_updates["review_action"] == "auto_approved"
        print(f"✅ Handler returned timeout result")
        print(f"   Auto-approved: {result.auto_approved}")
        print(f"   Timestamp: {result.timestamp}")

    print("✅ Test 9 PASSED\n")


def test_quick_review_handler_escalation():
    """Test quick review handler with escalation."""
    print("=" * 80)
    print("TEST 10: Quick Review Handler - Escalation")
    print("=" * 80)

    plan = create_test_plan(score=75, num_files=5)
    handler = QuickReviewHandler(
        task_id="TASK-002",
        plan=plan,
        countdown_duration=1
    )

    # Mock countdown_timer to return enter
    with patch('lib.review_modes.countdown_timer', return_value="enter"):
        result = handler.execute()

        assert result.action == "enter", f"Expected 'enter', got '{result.action}'"
        assert result.auto_approved is False, "Expected auto_approved=False"
        assert result.metadata_updates["review_action"] == "escalated_to_full"
        print(f"✅ Handler returned escalation result")
        print(f"   Action: {result.action}")
        print(f"   Escalation timestamp: {result.metadata_updates.get('escalation_timestamp')}")

    print("✅ Test 10 PASSED\n")


def test_quick_review_handler_cancellation():
    """Test quick review handler with cancellation."""
    print("=" * 80)
    print("TEST 11: Quick Review Handler - Cancellation")
    print("=" * 80)

    plan = create_test_plan(score=65, num_files=2)
    handler = QuickReviewHandler(
        task_id="TASK-003",
        plan=plan,
        countdown_duration=1
    )

    # Mock countdown_timer to return cancel
    with patch('lib.review_modes.countdown_timer', return_value="cancel"):
        result = handler.execute()

        assert result.action == "cancel", f"Expected 'cancel', got '{result.action}'"
        assert result.auto_approved is False, "Expected auto_approved=False"
        assert result.metadata_updates["review_action"] == "cancelled"
        print(f"✅ Handler returned cancellation result")
        print(f"   Action: {result.action}")
        print(f"   Cancellation timestamp: {result.metadata_updates.get('cancellation_timestamp')}")

    print("✅ Test 11 PASSED\n")


def test_quick_review_handler_error_failsafe():
    """Test quick review handler fail-safe on errors."""
    print("=" * 80)
    print("TEST 12: Quick Review Handler - Error Fail-Safe")
    print("=" * 80)

    plan = create_test_plan(score=85, num_files=3)
    handler = QuickReviewHandler(
        task_id="TASK-004",
        plan=plan,
        countdown_duration=1
    )

    # Mock countdown_timer to raise exception
    with patch('lib.review_modes.countdown_timer', side_effect=RuntimeError("Test error")):
        result = handler.execute()

        # Should escalate to full review on error
        assert result.action == "enter", f"Expected 'enter' (escalation), got '{result.action}'"
        assert result.auto_approved is False, "Expected auto_approved=False"
        print(f"✅ Handler escalated on error (fail-safe)")
        print(f"   Action: {result.action}")

    print("✅ Test 12 PASSED\n")


def test_quick_review_result_serialization():
    """Test QuickReviewResult serialization/deserialization."""
    print("=" * 80)
    print("TEST 13: QuickReviewResult Serialization")
    print("=" * 80)

    original = QuickReviewResult(
        action="timeout",
        timestamp="2025-10-09T10:30:00Z",
        auto_approved=True,
        metadata_updates={"review_mode": "quick", "score": 87}
    )

    # Serialize to dict
    data = original.to_dict()
    assert data["action"] == "timeout"
    assert data["auto_approved"] is True
    print("✅ Serialization to dict successful")

    # Deserialize from dict
    restored = QuickReviewResult.from_dict(data)
    assert restored.action == original.action
    assert restored.timestamp == original.timestamp
    assert restored.auto_approved == original.auto_approved
    assert restored.metadata_updates == original.metadata_updates
    print("✅ Deserialization from dict successful")

    print("✅ Test 13 PASSED\n")


def test_quick_review_handler_save_result(tmp_path):
    """Test saving review result to file."""
    print("=" * 80)
    print("TEST 14: Save Review Result")
    print("=" * 80)

    plan = create_test_plan(score=90, num_files=2)
    handler = QuickReviewHandler(
        task_id="TASK-005",
        plan=plan,
        countdown_duration=1
    )

    result = QuickReviewResult(
        action="timeout",
        timestamp="2025-10-09T10:30:00Z",
        auto_approved=True,
        metadata_updates={"review_mode": "quick"}
    )

    # Save to temp file
    output_file = tmp_path / "result.json"
    handler.save_result(result, output_path=output_file)

    assert output_file.exists(), "Result file not created"
    print(f"✅ Result saved to {output_file}")

    # Verify content
    import json
    with open(output_file, 'r') as f:
        data = json.load(f)
        assert data["action"] == "timeout"
        assert data["auto_approved"] is True
        print("✅ Result file contains expected data")

    print("✅ Test 14 PASSED\n")


def run_all_tests():
    """Run all test suites."""
    print("\n" + "=" * 80)
    print("QUICK REVIEW MODE - TEST SUITE")
    print("=" * 80 + "\n")

    # Import tmp_path fixture manually for test 14
    import tempfile
    tmp_path = Path(tempfile.mkdtemp())

    try:
        # Input strategy tests
        test_unix_input_strategy()
        test_windows_input_strategy()
        test_input_strategy_factory()

        # Countdown timer tests
        test_countdown_timer_timeout()
        test_countdown_timer_enter_key()
        test_countdown_timer_cancel_key()
        test_countdown_timer_invalid_duration()

        # Display tests
        test_quick_review_display()

        # Handler tests
        test_quick_review_handler_timeout()
        test_quick_review_handler_escalation()
        test_quick_review_handler_cancellation()
        test_quick_review_handler_error_failsafe()

        # Serialization tests
        test_quick_review_result_serialization()
        test_quick_review_handler_save_result(tmp_path)

        print("=" * 80)
        print("ALL TESTS PASSED ✅")
        print("=" * 80)
        return 0

    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        # Cleanup temp directory
        import shutil
        shutil.rmtree(tmp_path, ignore_errors=True)


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
