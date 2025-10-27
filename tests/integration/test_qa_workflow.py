"""
Integration tests for Q&A Mode workflow.

Tests complete Q&A workflow including:
    - FullReviewHandler integration with Q&A mode
    - Q&A session execution
    - Return to checkpoint after Q&A
    - Metadata persistence
"""

import pytest
import yaml
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "installer/global/commands/lib"))

from complexity_models import (
    ComplexityScore,
    FactorScore,
    ForceReviewTrigger,
    ReviewMode,
    ImplementationPlan,
)
from review_modes import (
    FullReviewHandler,
    FullReviewResult,
)
from qa_manager import QAManager


# Test Fixtures
@pytest.fixture
def mock_complexity_score():
    """Create mock ComplexityScore for testing."""
    factor_scores = [
        FactorScore(
            factor_name="File Complexity",
            score=3.0,
            max_score=3.0,
            justification="High number of files to create"
        ),
    ]

    return ComplexityScore(
        total_score=8,
        factor_scores=factor_scores,
        forced_review_triggers=[ForceReviewTrigger.SECURITY_KEYWORDS],
        review_mode=ReviewMode.FULL_REQUIRED,
        calculation_timestamp=datetime.utcnow(),
        metadata={}
    )


@pytest.fixture
def mock_implementation_plan(mock_complexity_score):
    """Create mock ImplementationPlan for testing."""
    plan = ImplementationPlan(
        task_id="TASK-001",
        files_to_create=[
            "src/auth/login.py",
            "src/auth/session.py",
            "tests/test_auth.py"
        ],
        patterns_used=["Strategy", "Factory"],
        external_dependencies=["jwt", "bcrypt"],
        estimated_loc=350,
        risk_indicators=["authentication"],
        raw_plan="Implement login system with JWT authentication",
        test_summary="Unit tests for auth logic",
        risk_details=[
            {
                "severity": "high",
                "description": "Authentication bypass vulnerability",
                "mitigation": "Use established JWT library"
            }
        ],
        phases=[
            "Phase 1: JWT token generation",
            "Phase 2: Login endpoint implementation",
        ],
        estimated_duration="2-3 hours"
    )
    plan.complexity_score = mock_complexity_score
    return plan


@pytest.fixture
def mock_task_metadata():
    """Create mock task metadata for testing."""
    return {
        "id": "TASK-001",
        "title": "Implement JWT Authentication",
        "priority": "high",
        "status": "in_progress"
    }


@pytest.fixture
def temp_task_file(tmp_path):
    """Create temporary task file for testing."""
    task_file = tmp_path / "TASK-001.md"
    task_content = """---
id: TASK-001
title: Implement JWT Authentication
status: in_progress
priority: high
---

# Task Content

Test task description.
"""
    task_file.write_text(task_content, encoding="utf-8")
    return task_file


class TestQAWorkflowIntegration:
    """Integration tests for complete Q&A workflow."""

    @patch('builtins.input', side_effect=['Why Strategy pattern?', 'back'])
    @patch('builtins.print')
    def test_qa_mode_from_full_review(
        self,
        mock_print,
        mock_input,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        temp_task_file
    ):
        """Test entering Q&A mode from full review handler."""
        handler = FullReviewHandler(
            complexity_score=mock_complexity_score,
            plan=mock_implementation_plan,
            task_metadata=mock_task_metadata,
            task_file_path=temp_task_file
        )

        # Call _handle_question directly
        result = handler._handle_question()

        # Should return None to indicate return to checkpoint
        assert result is None

        # Verify task file was updated with Q&A session
        updated_content = temp_task_file.read_text(encoding="utf-8")
        assert "qa_session:" in updated_content
        assert "exchanges:" in updated_content

    @patch('builtins.input', side_effect=[
        'q',  # Choose Q&A mode
        'Why Strategy pattern?',
        'What are the risks?',
        'back',  # Exit Q&A
        'a'  # Approve the plan
    ])
    @patch('builtins.print')
    def test_full_review_with_qa_then_approve(
        self,
        mock_print,
        mock_input,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        temp_task_file
    ):
        """Test full review workflow: Q&A → return to checkpoint → approve."""
        handler = FullReviewHandler(
            complexity_score=mock_complexity_score,
            plan=mock_implementation_plan,
            task_metadata=mock_task_metadata,
            task_file_path=temp_task_file
        )

        result = handler.execute()

        # Should eventually approve
        assert result.action == "approve"
        assert result.approved is True
        assert result.proceed_to_phase_3 is True

        # Verify Q&A session was saved
        updated_content = temp_task_file.read_text(encoding="utf-8")
        updated_yaml = yaml.safe_load(updated_content.split("---")[1])

        assert "qa_session" in updated_yaml
        assert len(updated_yaml["qa_session"]["exchanges"]) == 2

    @patch('builtins.input', side_effect=[
        'q',  # Choose Q&A mode
        'What are the risks?',
        'back',  # Exit Q&A
        'c',  # Cancel
        'y'  # Confirm cancellation
    ])
    @patch('builtins.print')
    def test_full_review_with_qa_then_cancel(
        self,
        mock_print,
        mock_input,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        temp_task_file
    ):
        """Test full review workflow: Q&A → return to checkpoint → cancel."""
        handler = FullReviewHandler(
            complexity_score=mock_complexity_score,
            plan=mock_implementation_plan,
            task_metadata=mock_task_metadata,
            task_file_path=temp_task_file
        )

        result = handler.execute()

        # Should cancel
        assert result.action == "cancel"
        assert result.approved is False

        # Q&A session should still be saved
        # Note: Task file moved to backlog, so check original location
        # (In real workflow, would check backlog location)

    @patch('builtins.input', side_effect=[
        'help',
        'Why was this approach chosen?',
        '',  # Empty question (ignored)
        'What are the phases?',
        'back'  # Exit Q&A
    ])
    @patch('builtins.print')
    def test_qa_mode_various_commands(
        self,
        mock_print,
        mock_input,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        temp_task_file
    ):
        """Test Q&A mode with various commands (help, empty, back)."""
        manager = QAManager(
            plan=mock_implementation_plan,
            task_id="TASK-001",
            task_metadata=mock_task_metadata
        )

        session = manager.run_qa_session()

        # Should have 2 exchanges (help and empty are ignored)
        assert session is not None
        assert len(session.exchanges) == 2
        assert session.exchanges[0].question == "Why was this approach chosen?"
        assert session.exchanges[1].question == "What are the phases?"
        assert session.exit_reason == "back"

    @patch('builtins.input', side_effect=[
        'Why Strategy pattern?',
        KeyboardInterrupt()
    ])
    @patch('builtins.print')
    def test_qa_mode_keyboard_interrupt(
        self,
        mock_print,
        mock_input,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        temp_task_file
    ):
        """Test Q&A mode handling of keyboard interrupt."""
        manager = QAManager(
            plan=mock_implementation_plan,
            task_id="TASK-001",
            task_metadata=mock_task_metadata
        )

        session = manager.run_qa_session()

        # Session should still complete with interrupt exit reason
        assert session is not None
        assert len(session.exchanges) == 1
        assert session.exit_reason == "interrupt"
        assert session.ended_at is not None

    @patch('builtins.input', side_effect=[
        'Why Strategy pattern?',
        'What are the risks?',
        'How complex is this?',
        'What files will be created?',
        'What dependencies are needed?',
        'back'
    ])
    @patch('builtins.print')
    def test_qa_mode_multiple_categories(
        self,
        mock_print,
        mock_input,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        temp_task_file
    ):
        """Test Q&A mode with questions from multiple categories."""
        manager = QAManager(
            plan=mock_implementation_plan,
            task_id="TASK-001",
            task_metadata=mock_task_metadata
        )

        session = manager.run_qa_session()

        assert session is not None
        assert len(session.exchanges) == 5

        # Verify different categories were matched
        questions = [ex.question for ex in session.exchanges]
        assert "Why Strategy pattern?" in questions
        assert "What are the risks?" in questions
        assert "How complex is this?" in questions
        assert "What files will be created?" in questions
        assert "What dependencies are needed?" in questions

        # Save and verify
        manager.save_to_metadata(str(temp_task_file))

        updated_content = temp_task_file.read_text(encoding="utf-8")
        updated_yaml = yaml.safe_load(updated_content.split("---")[1])

        assert len(updated_yaml["qa_session"]["exchanges"]) == 5

    def test_qa_manager_answer_content(
        self,
        mock_implementation_plan,
        mock_task_metadata
    ):
        """Test that Q&A answers contain relevant plan information."""
        manager = QAManager(
            plan=mock_implementation_plan,
            task_id="TASK-001",
            task_metadata=mock_task_metadata
        )

        # Test rationale answer
        rationale_answer = manager._generate_answer("Why Strategy pattern?")
        assert "Strategy" in rationale_answer["answer"]
        assert rationale_answer["category"] == "rationale"

        # Test risk answer
        risk_answer = manager._generate_answer("What are the risks?")
        assert "Authentication bypass" in risk_answer["answer"]
        assert risk_answer["category"] == "risks"

        # Test files answer
        files_answer = manager._generate_answer("What files will be created?")
        assert "src/auth/login.py" in files_answer["answer"]
        assert files_answer["category"] == "files"

        # Test dependencies answer
        deps_answer = manager._generate_answer("What dependencies are needed?")
        assert "jwt" in deps_answer["answer"]
        assert deps_answer["category"] == "dependencies"

        # Test general answer
        general_answer = manager._generate_answer("Tell me about the plan")
        assert "TASK-001" in general_answer["answer"]
        assert general_answer["category"] == "general"


# Performance and Edge Cases
class TestQAWorkflowEdgeCases:
    """Test edge cases and error handling in Q&A workflow."""

    @patch('builtins.input', side_effect=['Question?', 'back'])
    @patch('builtins.print')
    def test_qa_with_minimal_plan(
        self,
        mock_print,
        mock_input,
        mock_task_metadata
    ):
        """Test Q&A with minimal implementation plan (no optional fields)."""
        minimal_plan = ImplementationPlan(
            task_id="TASK-001",
            files_to_create=["src/main.py"],
        )

        manager = QAManager(
            plan=minimal_plan,
            task_id="TASK-001",
            task_metadata=mock_task_metadata
        )

        session = manager.run_qa_session()

        # Should still work with minimal plan
        assert session is not None
        assert len(session.exchanges) == 1

    @patch('builtins.input', side_effect=['back'])
    @patch('builtins.print')
    def test_qa_immediate_exit(
        self,
        mock_print,
        mock_input,
        mock_implementation_plan,
        mock_task_metadata
    ):
        """Test Q&A mode with immediate exit (no questions asked)."""
        manager = QAManager(
            plan=mock_implementation_plan,
            task_id="TASK-001",
            task_metadata=mock_task_metadata
        )

        session = manager.run_qa_session()

        # Should complete successfully with no exchanges
        assert session is not None
        assert len(session.exchanges) == 0
        assert session.exit_reason == "back"

    def test_qa_with_empty_plan(
        self,
        mock_task_metadata
    ):
        """Test Q&A with completely empty plan."""
        empty_plan = ImplementationPlan(
            task_id="TASK-001"
        )

        manager = QAManager(
            plan=empty_plan,
            task_id="TASK-001",
            task_metadata=mock_task_metadata
        )

        # Should still generate answers (with fallback content)
        answer = manager._generate_answer("What files will be created?")
        assert "answer" in answer
        assert answer["category"] == "files"
