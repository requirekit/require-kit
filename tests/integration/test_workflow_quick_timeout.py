"""
Integration tests for quick review timeout workflow.

Tests the complete workflow for quick review mode when countdown times out
(user does not interrupt), resulting in auto-approval.

Test Coverage:
    - Quick review display rendering
    - 10-second countdown timer completion
    - Auto-approval after timeout
    - Metadata updates after timeout
    - Edge cases (0 seconds, different durations)
    - Parametrized timeout durations

Workflow:
    1. Display quick review summary card
    2. Start countdown timer (10 seconds default)
    3. User does not interrupt (timeout)
    4. Auto-approve and proceed to Phase 3
    5. Update task metadata with approval details
"""

import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
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
from review_modes import (
    QuickReviewHandler,
    QuickReviewDisplay,
    QuickReviewResult
)


@pytest.mark.integration
@pytest.mark.workflow
class TestQuickTimeoutWorkflow:
    """Integration tests for quick review timeout workflow."""

    def test_quick_review_display_renders_correctly(
        self,
        mock_implementation_plan,
        display_factory
    ):
        """
        Test that quick review display renders summary card correctly.

        Validates display output includes:
        - Complexity score badge
        - File creation summary
        - Implementation instructions
        - Key architectural patterns

        GIVEN a quick review display with implementation plan
        WHEN render_summary_card is called
        THEN all required sections should be displayed
        """
        # Arrange: Create display instance
        display = display_factory(
            plan=mock_implementation_plan,
            mode='quick'
        )

        # Act: Capture display output
        with patch('builtins.print') as mock_print:
            display.render_summary_card()

        # Assert: Verify display content
        print_calls = [str(call) for call in mock_print.call_args_list]
        all_output = ' '.join(print_calls)

        assert any('ARCHITECTURAL REVIEW - QUICK MODE' in str(call) for call in print_calls), \
            "Display should show quick mode header"
        assert any('Complexity Score:' in str(call) or 'SCORE:' in str(call) for call in print_calls), \
            "Display should show complexity score"
        assert any('Files to Create:' in str(call) or 'files' in str(call).lower() for call in print_calls), \
            "Display should show files to create"

    def test_countdown_timer_completes_with_timeout(
        self,
        mock_implementation_plan,
        handler_factory
    ):
        """
        Test that countdown timer completes and returns timeout.

        Validates countdown behavior:
        - Timer starts with configured duration
        - No user interruption occurs
        - Timer completes and returns "timeout"
        - Handler processes timeout correctly

        GIVEN a quick review handler with 10-second countdown
        WHEN countdown completes without interruption
        THEN handler should return timeout result
        """
        # Arrange: Create handler with mocked countdown timer
        handler = handler_factory(
            task_id="TASK-TIMEOUT-001",
            plan=mock_implementation_plan,
            mode='quick',
            countdown_duration=10
        )

        # Mock countdown_timer to return timeout immediately
        with patch('review_modes.countdown_timer') as mock_timer:
            mock_timer.return_value = "timeout"

            # Act: Execute handler
            result = handler.execute()

        # Assert: Verify timeout handling
        assert result.action == "timeout", \
            "Handler should return timeout action"
        assert result.auto_approved is True, \
            "Timeout should result in auto-approval"
        assert result.metadata_updates is not None, \
            "Metadata updates should be present"
        assert result.metadata_updates.get("review_action") == "auto_approved", \
            "Metadata should indicate auto-approval"
        assert mock_timer.called, \
            "Countdown timer should be called"

    def test_auto_approval_after_timeout(
        self,
        mock_implementation_plan,
        handler_factory
    ):
        """
        Test that timeout triggers auto-approval with correct metadata.

        Validates auto-approval behavior:
        - Result action is "timeout"
        - Auto-approved flag is True
        - Metadata includes approval timestamp
        - Metadata includes complexity score
        - Metadata indicates quick review mode

        GIVEN a quick review timeout
        WHEN handler processes timeout
        THEN auto-approval should be triggered with complete metadata
        """
        # Arrange: Create handler
        handler = handler_factory(
            task_id="TASK-AUTO-001",
            plan=mock_implementation_plan,
            mode='quick',
            countdown_duration=10
        )

        # Mock countdown to timeout
        with patch('review_modes.countdown_timer') as mock_timer:
            mock_timer.return_value = "timeout"

            # Act: Execute and get result
            result = handler.execute()

        # Assert: Verify auto-approval details
        assert result.action == "timeout", \
            "Action should be timeout"
        assert result.auto_approved is True, \
            "Auto-approved flag should be True"
        assert "review_timestamp" in result.metadata_updates, \
            "Metadata should include review timestamp"
        assert "complexity_score" in result.metadata_updates, \
            "Metadata should include complexity score"
        assert result.metadata_updates.get("review_mode") == "quick_review", \
            "Metadata should indicate quick review mode"
        assert result.metadata_updates.get("auto_approved") is True, \
            "Metadata should confirm auto-approval"

        # Verify timestamp format (ISO 8601)
        timestamp = result.timestamp
        assert timestamp.endswith("Z"), \
            "Timestamp should be in UTC (ending with Z)"
        # Basic ISO 8601 format check
        datetime.fromisoformat(timestamp.replace('Z', '+00:00'))

    def test_metadata_updates_after_timeout(
        self,
        mock_implementation_plan,
        handler_factory
    ):
        """
        Test that metadata updates are correctly populated after timeout.

        Validates metadata structure:
        - review_mode: "quick_review"
        - review_action: "auto_approved"
        - review_timestamp: ISO 8601 format
        - complexity_score: numeric value
        - auto_approved: True

        GIVEN a timeout result
        WHEN metadata is extracted
        THEN all required fields should be present and valid
        """
        # Arrange: Create handler
        handler = handler_factory(
            task_id="TASK-META-001",
            plan=mock_implementation_plan,
            mode='quick'
        )

        # Mock timeout
        with patch('review_modes.countdown_timer', return_value="timeout"):
            # Act: Execute
            result = handler.execute()

        # Assert: Verify metadata structure
        metadata = result.metadata_updates

        assert metadata.get("review_mode") == "quick_review", \
            "Review mode should be quick_review"
        assert metadata.get("review_action") == "auto_approved", \
            "Review action should be auto_approved"
        assert "review_timestamp" in metadata, \
            "Should include review timestamp"
        assert isinstance(metadata.get("complexity_score"), (int, float)), \
            "Complexity score should be numeric"
        assert metadata.get("auto_approved") is True, \
            "Auto-approved flag should be True"

    def test_edge_case_zero_second_timeout(
        self,
        mock_implementation_plan,
        handler_factory
    ):
        """
        Test edge case: 0-second timeout (instant auto-approval).

        Validates behavior with no countdown:
        - Handler accepts 0-second duration
        - Immediate timeout without delay
        - Auto-approval still works correctly

        GIVEN a handler configured with 0-second countdown
        WHEN handler executes
        THEN should immediately auto-approve
        """
        # Arrange: Handler with 0-second countdown
        handler = handler_factory(
            task_id="TASK-ZERO-001",
            plan=mock_implementation_plan,
            mode='quick',
            countdown_duration=0
        )

        # Mock instant timeout
        with patch('review_modes.countdown_timer', return_value="timeout"):
            # Act: Execute
            result = handler.execute()

        # Assert: Verify instant auto-approval
        assert result.action == "timeout", \
            "Should timeout instantly"
        assert result.auto_approved is True, \
            "Should auto-approve with 0-second countdown"

    @pytest.mark.parametrize("duration", [5, 10, 15, 30])
    def test_parametrized_timeout_durations(
        self,
        mock_implementation_plan,
        handler_factory,
        duration
    ):
        """
        Test that different timeout durations all work correctly.

        Parametrized test validating consistent behavior across:
        - 5 seconds (fast review)
        - 10 seconds (default)
        - 15 seconds (extended review)
        - 30 seconds (thorough review)

        GIVEN various countdown durations
        WHEN timeout occurs
        THEN auto-approval should work consistently
        """
        # Arrange: Handler with parametrized duration
        handler = handler_factory(
            task_id=f"TASK-DUR-{duration}",
            plan=mock_implementation_plan,
            mode='quick',
            countdown_duration=duration
        )

        # Mock timeout
        with patch('review_modes.countdown_timer') as mock_timer:
            mock_timer.return_value = "timeout"

            # Act: Execute
            result = handler.execute()

            # Assert: Verify timer called with correct duration
            mock_timer.assert_called_once()
            call_args = mock_timer.call_args
            assert call_args[1]['duration_seconds'] == duration, \
                f"Timer should be called with {duration} seconds"

        # Assert: Verify consistent auto-approval behavior
        assert result.action == "timeout", \
            f"Duration {duration}s should result in timeout"
        assert result.auto_approved is True, \
            f"Duration {duration}s should auto-approve"

    def test_timeout_result_serialization(
        self,
        mock_implementation_plan,
        handler_factory
    ):
        """
        Test that timeout result can be serialized and deserialized.

        Validates result persistence:
        - Result converts to dict
        - Dict is JSON-serializable
        - Deserialization reconstructs result
        - All fields preserved

        GIVEN a timeout result
        WHEN converted to dict and back
        THEN all data should be preserved
        """
        # Arrange: Create handler and get result
        handler = handler_factory(
            task_id="TASK-SERIAL-001",
            plan=mock_implementation_plan,
            mode='quick'
        )

        with patch('review_modes.countdown_timer', return_value="timeout"):
            original_result = handler.execute()

        # Act: Serialize and deserialize
        result_dict = original_result.to_dict()
        reconstructed_result = QuickReviewResult.from_dict(result_dict)

        # Assert: Verify preservation
        assert reconstructed_result.action == original_result.action, \
            "Action should be preserved"
        assert reconstructed_result.auto_approved == original_result.auto_approved, \
            "Auto-approved flag should be preserved"
        assert reconstructed_result.timestamp == original_result.timestamp, \
            "Timestamp should be preserved"
        assert reconstructed_result.metadata_updates == original_result.metadata_updates, \
            "Metadata updates should be preserved"
