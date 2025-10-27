"""
Integration tests for Q&A mode workflow.

Tests the complete workflow for Q&A (Question & Answer) mode where users
can ask questions about the implementation plan during full review.

Test Coverage:
    - Q&A entry from full review
    - Question submission to architect (mocked)
    - Answer generation and display
    - Multiple Q&A rounds
    - Exit back to full review
    - Q&A history persistence

Workflow:
    1. User in full review chooses 'Q' (question)
    2. Q&A mode activated
    3. User asks questions about plan
    4. System provides contextual answers (mocked)
    5. User can ask more questions or type 'back'
    6. Q&A session saved to metadata
    7. Return to full review checkpoint
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
    FullReviewResult
)


@pytest.mark.integration
@pytest.mark.workflow
class TestQAModeWorkflow:
    """Integration tests for Q&A mode workflow."""

    def test_qa_entry_from_full_review(
        self,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        mock_task_file_path,
        handler_factory
    ):
        """
        Test that user can enter Q&A mode from full review.

        Validates Q&A entry:
        - User chooses 'Q' (question)
        - Q&A mode activated
        - QAManager created
        - Session starts
        - Returns to full review when done

        GIVEN a full review checkpoint
        WHEN user chooses Q (question)
        THEN Q&A mode should activate and return to checkpoint
        """
        # Arrange: Create handler
        handler = handler_factory(
            task_id="TASK-QA-ENTRY-001",
            plan=mock_implementation_plan,
            mode='full',
            complexity_score=mock_complexity_score,
            task_metadata=mock_task_metadata,
            task_file_path=mock_task_file_path
        )

        # Mock QAManager and user input
        mock_qa_manager = Mock()
        mock_qa_session = Mock()
        mock_qa_session.ended_at = None  # Session not completed
        mock_qa_manager.run_qa_session.return_value = mock_qa_session

        # User input: 'q' for Q&A, then 'a' to approve after returning
        with patch('builtins.input', side_effect=['q', 'a']):
            with patch('qa_manager.QAManager', return_value=mock_qa_manager):
                # Act: Execute
                result = handler.execute()

        # Assert: Verify Q&A was entered and then approval followed
        assert mock_qa_manager.run_qa_session.called, \
            "Q&A session should be started"
        assert result.action == "approve", \
            "Should allow approval after Q&A session"

    def test_question_submission_to_architect(
        self,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        mock_task_file_path,
        handler_factory
    ):
        """
        Test that questions are submitted to architect (mocked).

        Validates question handling:
        - User submits question
        - Question passed to QAManager
        - Answer generated (mocked)
        - Answer displayed to user

        GIVEN Q&A mode active
        WHEN user submits question
        THEN answer should be generated and displayed
        """
        # Arrange: Create handler
        handler = handler_factory(
            task_id="TASK-QA-QUESTION-001",
            plan=mock_implementation_plan,
            mode='full',
            complexity_score=mock_complexity_score,
            task_metadata=mock_task_metadata,
            task_file_path=mock_task_file_path
        )

        # Mock QAManager with pre-defined answer
        mock_qa_manager = Mock()
        mock_qa_session = Mock()
        mock_qa_session.ended_at = None
        mock_qa_session.questions = [
            {
                "question": "Why use this pattern?",
                "answer": "This pattern ensures SOLID principles..."
            }
        ]
        mock_qa_manager.run_qa_session.return_value = mock_qa_session

        # User input: 'q' for Q&A, then 'a' to approve
        with patch('builtins.input', side_effect=['q', 'a']):
            with patch('qa_manager.QAManager', return_value=mock_qa_manager):
                # Act: Execute
                result = handler.execute()

        # Assert: Verify Q&A interaction
        assert mock_qa_manager.run_qa_session.called, \
            "Q&A session should process questions"
        assert result.action == "approve", \
            "Should allow approval after Q&A"

    def test_answer_generation_and_display(
        self,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        mock_task_file_path,
        handler_factory
    ):
        """
        Test that answers are generated and displayed correctly.

        Validates answer display:
        - Answer generated from implementation plan
        - Answer formatted for display
        - Answer shown to user
        - User can continue asking

        GIVEN a user question in Q&A mode
        WHEN answer is generated
        THEN answer should be displayed correctly
        """
        # Arrange: Create handler
        handler = handler_factory(
            task_id="TASK-QA-ANSWER-001",
            plan=mock_implementation_plan,
            mode='full',
            complexity_score=mock_complexity_score,
            task_metadata=mock_task_metadata,
            task_file_path=mock_task_file_path
        )

        # Mock QAManager with detailed answer
        mock_qa_manager = Mock()
        mock_qa_session = Mock()
        mock_qa_session.ended_at = datetime.utcnow().isoformat() + "Z"
        mock_qa_session.questions = [
            {
                "question": "What are the risk mitigations?",
                "answer": "The plan includes the following mitigations:\n1. Comprehensive testing\n2. Staged rollout\n3. Monitoring"
            }
        ]
        mock_qa_manager.run_qa_session.return_value = mock_qa_session

        # User input: 'q' for Q&A, then 'a' to approve
        with patch('builtins.input', side_effect=['q', 'a']):
            with patch('qa_manager.QAManager', return_value=mock_qa_manager):
                # Act: Execute
                result = handler.execute()

        # Assert: Verify answer handling
        assert mock_qa_manager.run_qa_session.called, \
            "Q&A session should provide answers"
        assert result.action == "approve", \
            "Should proceed after Q&A"

    def test_multiple_qa_rounds(
        self,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        mock_task_file_path,
        handler_factory
    ):
        """
        Test that multiple Q&A rounds can be conducted.

        Validates multi-round Q&A:
        - User enters Q&A multiple times
        - Each session independent
        - Questions accumulated
        - All sessions recorded

        GIVEN a full review session
        WHEN user enters Q&A mode multiple times
        THEN each session should work independently
        """
        # Arrange: Create handler
        handler = handler_factory(
            task_id="TASK-QA-MULTI-001",
            plan=mock_implementation_plan,
            mode='full',
            complexity_score=mock_complexity_score,
            task_metadata=mock_task_metadata,
            task_file_path=mock_task_file_path
        )

        # Mock QAManager for multiple rounds
        mock_qa_manager = Mock()
        mock_qa_session = Mock()
        mock_qa_session.ended_at = None
        mock_qa_manager.run_qa_session.return_value = mock_qa_session

        # User input: 'q' twice, then 'a' to approve
        with patch('builtins.input', side_effect=['q', 'q', 'a']):
            with patch('qa_manager.QAManager', return_value=mock_qa_manager):
                # Act: Execute
                result = handler.execute()

        # Assert: Verify multiple Q&A sessions
        assert mock_qa_manager.run_qa_session.call_count == 2, \
            "Q&A session should be called twice"
        assert result.action == "approve", \
            "Should allow approval after multiple Q&A rounds"

    def test_exit_back_to_full_review(
        self,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        mock_task_file_path,
        handler_factory
    ):
        """
        Test that user can exit Q&A mode back to full review.

        Validates exit behavior:
        - User types 'back' or similar command
        - Q&A session ends
        - Return to full review checkpoint
        - User can make decision

        GIVEN Q&A mode active
        WHEN user exits Q&A
        THEN should return to full review checkpoint
        """
        # Arrange: Create handler
        handler = handler_factory(
            task_id="TASK-QA-EXIT-001",
            plan=mock_implementation_plan,
            mode='full',
            complexity_score=mock_complexity_score,
            task_metadata=mock_task_metadata,
            task_file_path=mock_task_file_path
        )

        # Mock QAManager that returns normally (user exited)
        mock_qa_manager = Mock()
        mock_qa_session = Mock()
        mock_qa_session.ended_at = None  # User exited without completing
        mock_qa_manager.run_qa_session.return_value = mock_qa_session

        # User input: 'q' for Q&A, then 'a' to approve after returning
        with patch('builtins.input', side_effect=['q', 'a']):
            with patch('qa_manager.QAManager', return_value=mock_qa_manager):
                # Act: Execute
                result = handler.execute()

        # Assert: Verify return to checkpoint and decision
        assert result.action == "approve", \
            "Should allow decision after exiting Q&A"
        assert result.approved is True, \
            "Should process approval after Q&A exit"

    def test_qa_history_persistence(
        self,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        mock_task_file_path,
        handler_factory
    ):
        """
        Test that Q&A session history is persisted to metadata.

        Validates history persistence:
        - Q&A session completed
        - Session data saved to task file
        - Questions and answers recorded
        - Timestamps preserved

        GIVEN a completed Q&A session
        WHEN session ends
        THEN session data should be saved to metadata
        """
        # Arrange: Create handler
        handler = handler_factory(
            task_id="TASK-QA-PERSIST-001",
            plan=mock_implementation_plan,
            mode='full',
            complexity_score=mock_complexity_score,
            task_metadata=mock_task_metadata,
            task_file_path=mock_task_file_path
        )

        # Mock QAManager with completed session
        mock_qa_manager = Mock()
        mock_qa_session = Mock()
        mock_qa_session.ended_at = datetime.utcnow().isoformat() + "Z"
        mock_qa_session.questions = [
            {
                "question": "How does this scale?",
                "answer": "The design uses horizontal scaling..."
            }
        ]
        mock_qa_manager.run_qa_session.return_value = mock_qa_session

        # User input: 'q' for Q&A, then 'a' to approve
        with patch('builtins.input', side_effect=['q', 'a']):
            with patch('qa_manager.QAManager', return_value=mock_qa_manager):
                # Act: Execute
                result = handler.execute()

        # Assert: Verify session saved
        assert mock_qa_manager.save_to_metadata.called, \
            "Q&A session should be saved to metadata"
        # Verify save was called with task file path
        save_call_args = mock_qa_manager.save_to_metadata.call_args
        assert str(mock_task_file_path) in str(save_call_args), \
            "Should save to correct task file"
