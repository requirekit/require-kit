"""
Integration tests for full review workflow.

Tests the complete workflow for full review mode with comprehensive
architectural review checkpoint and user decision handling.

Test Coverage:
    - Full review display rendering
    - User approval (A) proceeds to Phase 3
    - User modification (M) enters modification mode (stub)
    - User view (V) shows detailed plan (stub)
    - User questions (Q) enters Q&A mode (stub)
    - User cancellation (C) moves to backlog
    - Invalid input re-prompting
    - Decision metadata recording

Workflow:
    1. Display comprehensive checkpoint
    2. Prompt for user decision (A/M/V/Q/C)
    3. Handle user choice:
       - A: Approve and proceed to Phase 3
       - M: Enter modification mode (future implementation)
       - V: View full plan in pager (future implementation)
       - Q: Enter Q&A mode (future implementation)
       - C: Cancel and return to backlog
    4. Update task metadata with decision
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
    ImplementationPlan
)
from review_modes import (
    FullReviewHandler,
    FullReviewDisplay,
    FullReviewResult
)


@pytest.mark.integration
@pytest.mark.workflow
class TestFullReviewWorkflow:
    """Integration tests for full review workflow."""

    def test_full_review_display_renders_correctly(
        self,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        display_factory
    ):
        """
        Test that full review display renders comprehensive checkpoint.

        Validates display output includes:
        - Header with task info and complexity score
        - Complexity factors breakdown
        - Changes summary (files, dependencies)
        - Risk assessment
        - Implementation order/phases
        - Decision options prompt

        GIVEN a full review display with all data
        WHEN render_full_checkpoint is called
        THEN all sections should be displayed
        """
        # Arrange: Create display instance
        display = display_factory(
            plan=mock_implementation_plan,
            mode='full',
            complexity_score=mock_complexity_score,
            task_metadata=mock_task_metadata,
            escalated=False
        )

        # Act: Capture display output
        with patch('builtins.print') as mock_print:
            display.render_full_checkpoint()

        # Assert: Verify display sections
        print_calls = [str(call) for call in mock_print.call_args_list]

        assert any('IMPLEMENTATION PLAN REVIEW' in str(call) for call in print_calls), \
            "Display should show plan review header"
        assert any('COMPLEXITY BREAKDOWN' in str(call) for call in print_calls), \
            "Display should show complexity breakdown section"
        assert any('CHANGES SUMMARY' in str(call) or 'Files to Create' in str(call) for call in print_calls), \
            "Display should show changes summary"
        assert any('RISK ASSESSMENT' in str(call) for call in print_calls), \
            "Display should show risk assessment section"
        assert any('IMPLEMENTATION ORDER' in str(call) or 'DECISION OPTIONS' in str(call) for call in print_calls), \
            "Display should show implementation order or decision options"

    def test_user_approval_proceeds_to_phase_3(
        self,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        mock_task_file_path,
        handler_factory
    ):
        """
        Test that user approval (A) proceeds to Phase 3 implementation.

        Validates approval workflow:
        - User chooses 'A' (approve)
        - Handler returns approval result
        - Result indicates Phase 3 proceed
        - Metadata includes approval details
        - Approval timestamp recorded

        GIVEN a full review checkpoint
        WHEN user chooses approve (A)
        THEN should proceed to Phase 3 with approval metadata
        """
        # Arrange: Create handler
        handler = handler_factory(
            task_id="TASK-APPROVE-001",
            plan=mock_implementation_plan,
            mode='full',
            complexity_score=mock_complexity_score,
            task_metadata=mock_task_metadata,
            task_file_path=mock_task_file_path
        )

        # Mock user input: 'a' for approve
        with patch('builtins.input', return_value='a'):
            # Act: Execute
            result = handler.execute()

        # Assert: Verify approval
        assert result.action == "approve", \
            "Action should be approve"
        assert result.approved is True, \
            "Approved flag should be True"
        assert result.proceed_to_phase_3 is True, \
            "Should proceed to Phase 3"
        assert "implementation_plan" in result.metadata_updates, \
            "Metadata should include implementation plan details"
        assert result.metadata_updates["implementation_plan"]["approved"] is True, \
            "Implementation plan should be marked as approved"

    def test_user_cancellation_moves_to_backlog(
        self,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        mock_task_file_path,
        handler_factory
    ):
        """
        Test that user cancellation (C) moves task to backlog.

        Validates cancellation workflow:
        - User chooses 'C' (cancel)
        - Confirmation prompt shown
        - User confirms with 'y'
        - Handler returns cancellation result
        - Metadata indicates cancellation

        GIVEN a full review checkpoint
        WHEN user chooses cancel (C) and confirms
        THEN task should be cancelled with metadata
        """
        # Arrange: Create task file in temp directory
        import yaml
        mock_task_file_path.parent.mkdir(parents=True, exist_ok=True)

        task_content = f"""---
id: {mock_task_metadata['id']}
title: {mock_task_metadata['title']}
status: in_progress
---

# Test Task
Test content
"""
        mock_task_file_path.write_text(task_content, encoding='utf-8')

        # Create handler
        handler = handler_factory(
            task_id="TASK-CANCEL-001",
            plan=mock_implementation_plan,
            mode='full',
            complexity_score=mock_complexity_score,
            task_metadata=mock_task_metadata,
            task_file_path=mock_task_file_path
        )

        # Mock user input: 'c' then 'y' for confirmation
        with patch('builtins.input', side_effect=['c', 'y']):
            # Act: Execute
            result = handler.execute()

        # Assert: Verify cancellation
        assert result.action == "cancel", \
            "Action should be cancel"
        assert result.approved is False, \
            "Approved flag should be False"
        assert result.proceed_to_phase_3 is False, \
            "Should not proceed to Phase 3"
        assert result.metadata_updates.get("cancelled") is True, \
            "Metadata should indicate task was cancelled"
        assert result.metadata_updates.get("status") == "backlog", \
            "Status should be set to backlog"
        assert "cancelled_at" in result.metadata_updates, \
            "Metadata should include cancellation timestamp"

    def test_user_cancellation_aborted(
        self,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        mock_task_file_path,
        handler_factory
    ):
        """
        Test that cancelled cancellation returns to decision prompt.

        Validates cancellation abort:
        - User chooses 'C' (cancel)
        - User declines confirmation with 'n'
        - Handler re-prompts for decision
        - User can then choose another action

        GIVEN a full review checkpoint
        WHEN user cancels but doesn't confirm
        THEN should return to decision prompt
        """
        # Arrange: Create handler
        handler = handler_factory(
            task_id="TASK-CANCEL-ABORT-001",
            plan=mock_implementation_plan,
            mode='full',
            complexity_score=mock_complexity_score,
            task_metadata=mock_task_metadata,
            task_file_path=mock_task_file_path
        )

        # Mock user input: 'c', 'n' (abort), then 'a' (approve)
        with patch('builtins.input', side_effect=['c', 'n', 'a']):
            # Act: Execute
            result = handler.execute()

        # Assert: Verify user got to approve after aborting cancel
        assert result.action == "approve", \
            "Should allow approval after aborting cancellation"
        assert result.approved is True, \
            "Should approve after cancellation aborted"

    def test_invalid_input_reprompts(
        self,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        mock_task_file_path,
        handler_factory
    ):
        """
        Test that invalid input causes re-prompt with error message.

        Validates input validation:
        - Invalid input entered ('x', '1', etc.)
        - Error message displayed
        - Prompt shown again
        - Valid input eventually accepted

        GIVEN a full review checkpoint
        WHEN user enters invalid input
        THEN should show error and re-prompt
        """
        # Arrange: Create handler
        handler = handler_factory(
            task_id="TASK-INVALID-001",
            plan=mock_implementation_plan,
            mode='full',
            complexity_score=mock_complexity_score,
            task_metadata=mock_task_metadata,
            task_file_path=mock_task_file_path
        )

        # Mock user input: invalid inputs then valid 'a'
        with patch('builtins.input', side_effect=['x', '1', 'invalid', 'a']):
            with patch('builtins.print') as mock_print:
                # Act: Execute
                result = handler.execute()

        # Assert: Verify re-prompting occurred
        print_calls = [str(call) for call in mock_print.call_args_list]

        # Should show error messages for invalid inputs
        assert any('Invalid' in str(call) or 'invalid' in str(call) for call in print_calls), \
            "Should display error message for invalid input"

        # Should eventually accept valid input
        assert result.action == "approve", \
            "Should accept valid input after invalid attempts"

    def test_decision_metadata_recording(
        self,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        mock_task_file_path,
        handler_factory
    ):
        """
        Test that decision metadata is correctly recorded.

        Validates metadata structure for approval:
        - implementation_plan.approved: True
        - implementation_plan.approved_by: "user"
        - implementation_plan.approved_at: timestamp
        - implementation_plan.review_mode: "full_required" or "escalated"
        - implementation_plan.review_duration_seconds: integer
        - implementation_plan.complexity_score: numeric

        GIVEN an approval decision
        WHEN metadata is captured
        THEN all approval details should be recorded
        """
        # Arrange: Create handler
        handler = handler_factory(
            task_id="TASK-META-FULL-001",
            plan=mock_implementation_plan,
            mode='full',
            complexity_score=mock_complexity_score,
            task_metadata=mock_task_metadata,
            task_file_path=mock_task_file_path
        )

        # Mock approval
        with patch('builtins.input', return_value='a'):
            # Act: Execute
            result = handler.execute()

        # Assert: Verify metadata structure
        plan_metadata = result.metadata_updates.get("implementation_plan", {})

        assert plan_metadata.get("approved") is True, \
            "Plan should be marked as approved"
        assert plan_metadata.get("approved_by") == "user", \
            "Should record approval source"
        assert "approved_at" in plan_metadata, \
            "Should include approval timestamp"
        assert "review_mode" in plan_metadata, \
            "Should indicate review mode"
        assert "review_duration_seconds" in plan_metadata, \
            "Should include review duration"
        assert isinstance(plan_metadata.get("review_duration_seconds"), int), \
            "Review duration should be integer"
        assert "complexity_score" in plan_metadata, \
            "Should include complexity score"

    def test_escalated_review_flag_recorded(
        self,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        mock_task_file_path,
        handler_factory
    ):
        """
        Test that escalated review flag is recorded in metadata.

        Validates escalated review handling:
        - Handler accepts escalated=True parameter
        - Metadata indicates escalated review mode
        - Display shows escalation indicator
        - Result metadata includes escalation info

        GIVEN an escalated full review
        WHEN approval occurs
        THEN metadata should indicate escalation
        """
        # Arrange: Create handler with escalated=True
        handler = handler_factory(
            task_id="TASK-ESCALATED-001",
            plan=mock_implementation_plan,
            mode='full',
            complexity_score=mock_complexity_score,
            task_metadata=mock_task_metadata,
            task_file_path=mock_task_file_path,
            escalated=True
        )

        # Mock approval
        with patch('builtins.input', return_value='a'):
            # Act: Execute
            result = handler.execute()

        # Assert: Verify escalation recorded
        plan_metadata = result.metadata_updates.get("implementation_plan", {})
        assert plan_metadata.get("review_mode") == "escalated", \
            "Should indicate escalated review mode"

    def test_full_review_result_serialization(
        self,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        mock_task_file_path,
        handler_factory
    ):
        """
        Test that full review result can be serialized and deserialized.

        Validates result persistence:
        - Result converts to dict
        - Dict is JSON-serializable
        - All fields preserved
        - Metadata preserved

        GIVEN a full review result
        WHEN converted to dict and back
        THEN all data should be preserved
        """
        # Arrange: Create handler and get result
        handler = handler_factory(
            task_id="TASK-SERIAL-FULL-001",
            plan=mock_implementation_plan,
            mode='full',
            complexity_score=mock_complexity_score,
            task_metadata=mock_task_metadata,
            task_file_path=mock_task_file_path
        )

        with patch('builtins.input', return_value='a'):
            original_result = handler.execute()

        # Act: Serialize to dict
        result_dict = original_result.to_dict()

        # Assert: Verify serialization
        assert result_dict["action"] == original_result.action, \
            "Action should be preserved"
        assert result_dict["approved"] == original_result.approved, \
            "Approved flag should be preserved"
        assert result_dict["timestamp"] == original_result.timestamp, \
            "Timestamp should be preserved"
        assert result_dict["metadata_updates"] == original_result.metadata_updates, \
            "Metadata updates should be preserved"
        assert result_dict["proceed_to_phase_3"] == original_result.proceed_to_phase_3, \
            "Proceed flag should be preserved"
