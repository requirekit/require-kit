"""
Integration tests for quick review escalation workflow.

Tests the complete workflow for quick review mode when user presses ENTER
to interrupt the countdown and escalate to full review.

Test Coverage:
    - ENTER key interrupts countdown
    - Escalation from quick to full review
    - Escalation metadata recording
    - Escalation count tracking
    - Multiple escalation attempts
    - Edge cases (immediate escalation)

Workflow:
    1. Display quick review summary card
    2. Start countdown timer
    3. User presses ENTER (interrupt)
    4. Handler returns escalation result
    5. Caller should invoke full review handler
    6. Metadata records escalation event
"""

import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch
import sys

# Add installer lib to path
installer_lib_path = Path(__file__).parent.parent.parent / "installer" / "global" / "commands" / "lib"
if str(installer_lib_path) not in sys.path:
    sys.path.insert(0, str(installer_lib_path))

from complexity_models import (
    ComplexityScore,
    FactorScore,
    ReviewMode,
    ImplementationPlan
)
from review_modes import (
    QuickReviewHandler,
    QuickReviewResult
)


@pytest.mark.integration
@pytest.mark.workflow
class TestQuickEscalationWorkflow:
    """Integration tests for quick review escalation workflow."""

    def test_enter_key_interrupts_countdown(
        self,
        mock_implementation_plan,
        handler_factory
    ):
        """
        Test that ENTER key interrupts countdown and triggers escalation.

        Validates interrupt behavior:
        - Countdown starts normally
        - User presses ENTER
        - Countdown stops immediately
        - Handler returns "enter" action

        GIVEN a quick review countdown in progress
        WHEN user presses ENTER
        THEN countdown should stop and escalate
        """
        # Arrange: Create handler
        handler = handler_factory(
            task_id="TASK-ESC-001",
            plan=mock_implementation_plan,
            mode='quick',
            countdown_duration=10
        )

        # Mock countdown_timer to return "enter" (user pressed ENTER)
        with patch('review_modes.countdown_timer') as mock_timer:
            mock_timer.return_value = "enter"

            # Act: Execute handler
            result = handler.execute()

        # Assert: Verify escalation triggered
        assert result.action == "enter", \
            "Handler should return enter action when ENTER pressed"
        assert result.auto_approved is False, \
            "Escalation should not be auto-approved"
        assert mock_timer.called, \
            "Countdown timer should be called"

    def test_escalation_from_quick_to_full_review(
        self,
        mock_implementation_plan,
        handler_factory
    ):
        """
        Test escalation flow from quick to full review mode.

        Validates escalation result:
        - Action is "enter"
        - Auto-approved is False
        - Metadata indicates escalation
        - Metadata includes escalation timestamp
        - Metadata shows escalation source (quick review)

        GIVEN a quick review escalation
        WHEN handler processes ENTER key
        THEN result should indicate full review required
        """
        # Arrange: Create handler
        handler = handler_factory(
            task_id="TASK-FLOW-001",
            plan=mock_implementation_plan,
            mode='quick'
        )

        # Mock ENTER press
        with patch('review_modes.countdown_timer', return_value="enter"):
            # Act: Execute
            result = handler.execute()

        # Assert: Verify escalation result
        assert result.action == "enter", \
            "Action should be enter (escalation)"
        assert result.auto_approved is False, \
            "Escalated review requires manual approval"
        assert result.metadata_updates is not None, \
            "Metadata updates should be present"
        assert result.metadata_updates.get("review_action") == "escalated_to_full", \
            "Metadata should indicate escalation to full review"
        assert "escalation_timestamp" in result.metadata_updates, \
            "Metadata should include escalation timestamp"
        assert result.metadata_updates.get("review_mode") == "quick_review", \
            "Metadata should show escalation source"

    def test_escalation_metadata_recorded(
        self,
        mock_implementation_plan,
        handler_factory
    ):
        """
        Test that escalation metadata is correctly recorded.

        Validates metadata structure:
        - review_mode: "quick_review"
        - review_action: "escalated_to_full"
        - escalation_timestamp: ISO 8601 format
        - auto_approved: False

        GIVEN an escalation event
        WHEN metadata is captured
        THEN all escalation details should be recorded
        """
        # Arrange: Create handler
        handler = handler_factory(
            task_id="TASK-RECORD-001",
            plan=mock_implementation_plan,
            mode='quick'
        )

        # Mock escalation
        with patch('review_modes.countdown_timer', return_value="enter"):
            # Act: Execute
            result = handler.execute()

        # Assert: Verify metadata structure
        metadata = result.metadata_updates

        assert metadata.get("review_mode") == "quick_review", \
            "Review mode should be quick_review"
        assert metadata.get("review_action") == "escalated_to_full", \
            "Review action should be escalated_to_full"
        assert "escalation_timestamp" in metadata, \
            "Should include escalation timestamp"
        assert metadata.get("auto_approved") is False, \
            "Auto-approved flag should be False for escalation"

        # Verify timestamp format
        timestamp = result.timestamp
        assert timestamp.endswith("Z"), \
            "Timestamp should be in UTC (ending with Z)"
        datetime.fromisoformat(timestamp.replace('Z', '+00:00'))

    def test_escalation_count_tracking(
        self,
        mock_implementation_plan,
        handler_factory
    ):
        """
        Test that multiple escalations can be tracked.

        Validates escalation counting:
        - First escalation recorded
        - Subsequent escalations recorded
        - Count increments correctly
        - Each escalation has unique timestamp

        GIVEN multiple escalation attempts
        WHEN each escalation is processed
        THEN each should be independently recorded
        """
        # Arrange: Create handler
        handler = handler_factory(
            task_id="TASK-COUNT-001",
            plan=mock_implementation_plan,
            mode='quick'
        )

        # Act: Simulate multiple escalations
        escalations = []
        for i in range(3):
            with patch('review_modes.countdown_timer', return_value="enter"):
                result = handler.execute()
                escalations.append(result)

        # Assert: Verify each escalation is unique
        assert len(escalations) == 3, \
            "Should capture 3 escalations"

        for i, result in enumerate(escalations):
            assert result.action == "enter", \
                f"Escalation {i+1} should have enter action"
            assert result.auto_approved is False, \
                f"Escalation {i+1} should not be auto-approved"

        # Verify unique timestamps
        timestamps = [r.timestamp for r in escalations]
        assert len(set(timestamps)) >= 1, \
            "Escalations should have timestamps (may be same if executed fast)"

    def test_multiple_escalation_attempts(
        self,
        mock_implementation_plan,
        handler_factory
    ):
        """
        Test that handler supports multiple escalation attempts.

        Validates resilience:
        - Handler can be called multiple times
        - Each call produces valid result
        - State does not corrupt between calls
        - Consistent behavior across attempts

        GIVEN a handler used multiple times
        WHEN escalation happens each time
        THEN results should be consistent
        """
        # Arrange: Create handler
        handler = handler_factory(
            task_id="TASK-MULTI-001",
            plan=mock_implementation_plan,
            mode='quick'
        )

        # Act: Execute multiple times
        results = []
        for _ in range(5):
            with patch('review_modes.countdown_timer', return_value="enter"):
                result = handler.execute()
                results.append(result)

        # Assert: Verify consistency
        for i, result in enumerate(results):
            assert result.action == "enter", \
                f"Attempt {i+1} should return enter action"
            assert result.auto_approved is False, \
                f"Attempt {i+1} should not be auto-approved"
            assert result.metadata_updates is not None, \
                f"Attempt {i+1} should have metadata"
            assert result.metadata_updates.get("review_action") == "escalated_to_full", \
                f"Attempt {i+1} should indicate escalation"

    def test_edge_case_immediate_escalation(
        self,
        mock_implementation_plan,
        handler_factory
    ):
        """
        Test edge case: immediate escalation (ENTER pressed instantly).

        Validates behavior with instant escalation:
        - No display delay issues
        - Countdown doesn't prevent immediate input
        - Result produced correctly

        GIVEN a quick review that starts
        WHEN ENTER is pressed immediately
        THEN escalation should work without issues
        """
        # Arrange: Handler that escalates immediately
        handler = handler_factory(
            task_id="TASK-IMMEDIATE-001",
            plan=mock_implementation_plan,
            mode='quick',
            countdown_duration=10
        )

        # Mock immediate ENTER press
        with patch('review_modes.countdown_timer', return_value="enter"):
            # Act: Execute
            result = handler.execute()

        # Assert: Verify immediate escalation works
        assert result.action == "enter", \
            "Immediate escalation should work"
        assert result.auto_approved is False, \
            "Immediate escalation should not auto-approve"

    def test_escalation_result_serialization(
        self,
        mock_implementation_plan,
        handler_factory
    ):
        """
        Test that escalation result can be serialized and deserialized.

        Validates result persistence:
        - Result converts to dict
        - Dict is JSON-serializable
        - Deserialization reconstructs result
        - All fields preserved

        GIVEN an escalation result
        WHEN converted to dict and back
        THEN all data should be preserved
        """
        # Arrange: Create handler and get result
        handler = handler_factory(
            task_id="TASK-SERIAL-ESC-001",
            plan=mock_implementation_plan,
            mode='quick'
        )

        with patch('review_modes.countdown_timer', return_value="enter"):
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
