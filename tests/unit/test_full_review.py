"""
Unit tests for Full Review Mode implementation.

Tests cover:
    - FullReviewDisplay rendering methods
    - FullReviewHandler decision handling
    - Input validation and error handling
    - Metadata update generation
    - State transitions (approve/cancel)
"""

import pytest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any

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
    FullReviewDisplay,
    FullReviewHandler,
    FullReviewResult,
)


# Test Fixtures
@pytest.fixture
def mock_complexity_score():
    """Create mock ComplexityScore for testing."""
    factor_scores = [
        FactorScore(
            factor_name="File Complexity",
            score=2.0,
            max_score=3.0,
            justification="6 files to create/modify (moderate scope)"
        ),
        FactorScore(
            factor_name="Pattern Familiarity",
            score=1.0,
            max_score=2.0,
            justification="Uses Strategy pattern (familiar)"
        ),
        FactorScore(
            factor_name="Risk Level",
            score=3.0,
            max_score=3.0,
            justification="High risk: Authentication changes"
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
def mock_implementation_plan():
    """Create mock ImplementationPlan for testing."""
    return ImplementationPlan(
        task_id="TASK-001",
        files_to_create=[
            "src/auth/login.py",
            "src/auth/session.py",
            "tests/test_auth.py"
        ],
        patterns_used=["Strategy", "Factory"],
        external_dependencies=["jwt", "bcrypt"],
        estimated_loc=350,
        risk_indicators=["authentication", "password"],
        raw_plan="Implement login system with JWT authentication",
        test_summary="Unit tests for auth logic, integration tests for API",
        risk_details=[
            {
                "severity": "high",
                "description": "Authentication bypass vulnerability",
                "mitigation": "Use established JWT library, security review"
            },
            {
                "severity": "medium",
                "description": "Session handling complexity",
                "mitigation": "Follow stateless JWT pattern"
            }
        ],
        phases=[
            "Phase 1: JWT token generation (~30 min)",
            "Phase 2: Login endpoint implementation (~45 min)",
            "Phase 3: Session middleware (~30 min)",
            "Phase 4: Testing and validation (~60 min)"
        ],
        implementation_instructions="Implement JWT-based authentication with bcrypt password hashing",
        estimated_duration="2-3 hours"
    )


@pytest.fixture
def mock_task_metadata():
    """Create mock task metadata for testing."""
    return {
        "id": "TASK-001",
        "title": "Implement JWT Authentication",
        "status": "in_progress",
        "priority": "high"
    }


@pytest.fixture
def mock_task_file_path(tmp_path):
    """Create mock task file path for testing."""
    task_file = tmp_path / "tasks" / "in_progress" / "TASK-001.md"
    task_file.parent.mkdir(parents=True, exist_ok=True)

    # Create minimal task file content
    content = """---
id: TASK-001
title: Implement JWT Authentication
status: in_progress
priority: high
---

# TASK-001: Implement JWT Authentication

Test task for full review mode.
"""
    task_file.write_text(content)
    return task_file


class TestFullReviewDisplay:
    """Test suite for FullReviewDisplay class."""

    def test_render_full_checkpoint(
        self,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        capsys
    ):
        """Test full checkpoint rendering."""
        display = FullReviewDisplay(
            complexity_score=mock_complexity_score,
            plan=mock_implementation_plan,
            task_metadata=mock_task_metadata,
            escalated=False
        )

        display.render_full_checkpoint()

        captured = capsys.readouterr()
        output = captured.out

        # Verify header content
        assert "IMPLEMENTATION PLAN REVIEW" in output
        assert "TASK-001" in output
        assert "Implement JWT Authentication" in output
        assert "8/10" in output  # Complexity score

        # Verify complexity breakdown
        assert "COMPLEXITY BREAKDOWN" in output
        assert "File Complexity" in output
        assert "Pattern Familiarity" in output
        assert "Risk Level" in output

        # Verify changes summary
        assert "CHANGES SUMMARY" in output
        assert "src/auth/login.py" in output

        # Verify risk assessment
        assert "RISK ASSESSMENT" in output
        assert "Authentication bypass" in output

        # Verify implementation order
        assert "IMPLEMENTATION ORDER" in output
        assert "Phase 1" in output

        # Verify decision options
        assert "DECISION OPTIONS" in output
        assert "[A] Approve" in output
        assert "[C] Cancel" in output

    def test_display_header_with_escalation(
        self,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        capsys
    ):
        """Test header display with escalation flag."""
        display = FullReviewDisplay(
            complexity_score=mock_complexity_score,
            plan=mock_implementation_plan,
            task_metadata=mock_task_metadata,
            escalated=True
        )

        display._display_header()

        captured = capsys.readouterr()
        assert "⬆️ Escalated from quick review" in captured.out

    def test_display_complexity_breakdown_with_triggers(
        self,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        capsys
    ):
        """Test complexity breakdown includes force-review triggers."""
        display = FullReviewDisplay(
            complexity_score=mock_complexity_score,
            plan=mock_implementation_plan,
            task_metadata=mock_task_metadata
        )

        display._display_complexity_breakdown()

        captured = capsys.readouterr()
        output = captured.out

        assert "FORCE-REVIEW TRIGGERS" in output
        assert "Security Keywords" in output

    def test_display_risk_assessment_with_details(
        self,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        capsys
    ):
        """Test risk assessment displays detailed risks."""
        display = FullReviewDisplay(
            complexity_score=mock_complexity_score,
            plan=mock_implementation_plan,
            task_metadata=mock_task_metadata
        )

        display._display_risk_assessment()

        captured = capsys.readouterr()
        output = captured.out

        assert "HIGH: Authentication bypass vulnerability" in output
        assert "Mitigation: Use established JWT library" in output
        assert "MEDIUM: Session handling complexity" in output

    def test_display_implementation_order_with_phases(
        self,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        capsys
    ):
        """Test implementation order displays phases."""
        display = FullReviewDisplay(
            complexity_score=mock_complexity_score,
            plan=mock_implementation_plan,
            task_metadata=mock_task_metadata
        )

        display._display_implementation_order()

        captured = capsys.readouterr()
        output = captured.out

        assert "Phase 1: JWT token generation" in output
        assert "Phase 2: Login endpoint implementation" in output
        assert "Estimated Lines of Code: ~350" in output


class TestFullReviewHandler:
    """Test suite for FullReviewHandler class."""

    def test_handle_approval(
        self,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        mock_task_file_path
    ):
        """Test approval handler."""
        handler = FullReviewHandler(
            complexity_score=mock_complexity_score,
            plan=mock_implementation_plan,
            task_metadata=mock_task_metadata,
            task_file_path=mock_task_file_path,
            escalated=False
        )

        result = handler._handle_approval()

        assert result.action == "approve"
        assert result.approved is True
        assert result.proceed_to_phase_3 is True
        assert "implementation_plan" in result.metadata_updates
        assert result.metadata_updates["implementation_plan"]["approved"] is True
        assert result.metadata_updates["implementation_plan"]["review_mode"] == "full_required"

    def test_handle_approval_escalated(
        self,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        mock_task_file_path
    ):
        """Test approval handler for escalated review."""
        handler = FullReviewHandler(
            complexity_score=mock_complexity_score,
            plan=mock_implementation_plan,
            task_metadata=mock_task_metadata,
            task_file_path=mock_task_file_path,
            escalated=True
        )

        result = handler._handle_approval()

        assert result.metadata_updates["implementation_plan"]["review_mode"] == "escalated"

    @patch('builtins.input', return_value='y')
    def test_handle_cancellation_confirmed(
        self,
        mock_input,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        mock_task_file_path
    ):
        """Test cancellation handler with confirmation."""
        handler = FullReviewHandler(
            complexity_score=mock_complexity_score,
            plan=mock_implementation_plan,
            task_metadata=mock_task_metadata,
            task_file_path=mock_task_file_path
        )

        result = handler._handle_cancellation()

        assert result is not None
        assert result.action == "cancel"
        assert result.approved is False
        assert result.proceed_to_phase_3 is False
        assert result.metadata_updates["status"] == "backlog"
        assert result.metadata_updates["cancelled"] is True

    @patch('builtins.input', return_value='n')
    def test_handle_cancellation_aborted(
        self,
        mock_input,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        mock_task_file_path
    ):
        """Test cancellation handler when user aborts."""
        handler = FullReviewHandler(
            complexity_score=mock_complexity_score,
            plan=mock_implementation_plan,
            task_metadata=mock_task_metadata,
            task_file_path=mock_task_file_path
        )

        result = handler._handle_cancellation()

        assert result is None  # Aborted, return to prompt

    def test_handle_cancellation_forced(
        self,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        mock_task_file_path
    ):
        """Test forced cancellation (Ctrl+C)."""
        handler = FullReviewHandler(
            complexity_score=mock_complexity_score,
            plan=mock_implementation_plan,
            task_metadata=mock_task_metadata,
            task_file_path=mock_task_file_path
        )

        result = handler._handle_cancellation(force=True)

        assert result is not None
        assert result.action == "cancel"

    @patch('builtins.input', side_effect=['a'])
    def test_execute_approve_flow(
        self,
        mock_input,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        mock_task_file_path
    ):
        """Test complete approval flow through execute()."""
        handler = FullReviewHandler(
            complexity_score=mock_complexity_score,
            plan=mock_implementation_plan,
            task_metadata=mock_task_metadata,
            task_file_path=mock_task_file_path
        )

        result = handler.execute()

        assert result.action == "approve"
        assert result.proceed_to_phase_3 is True

    @patch('builtins.input', side_effect=['m', 'a'])
    def test_execute_modify_stub(
        self,
        mock_input,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        mock_task_file_path,
        capsys
    ):
        """Test modify mode enters modification session and returns to checkpoint."""
        # Mock the _handle_modify method to return None (simulating return to checkpoint)
        handler = FullReviewHandler(
            complexity_score=mock_complexity_score,
            plan=mock_implementation_plan,
            task_metadata=mock_task_metadata,
            task_file_path=mock_task_file_path
        )

        # Replace _handle_modify with a mock that prints expected message and returns None
        original_handle_modify = handler._handle_modify
        def mock_handle_modify():
            print("\n🔧 Entering modification mode...\n")
            # Simulate user returning to checkpoint
            return None

        handler._handle_modify = mock_handle_modify

        result = handler.execute()

        captured = capsys.readouterr()
        assert "🔧 Entering modification mode..." in captured.out
        assert result.action == "approve"  # Eventually approved after returning from modify

    @patch('builtins.input', side_effect=['v', 'a'])
    def test_execute_view_stub(
        self,
        mock_input,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        mock_task_file_path,
        capsys
    ):
        """Test view mode opens pager and returns to checkpoint."""
        handler = FullReviewHandler(
            complexity_score=mock_complexity_score,
            plan=mock_implementation_plan,
            task_metadata=mock_task_metadata,
            task_file_path=mock_task_file_path
        )

        # Replace _handle_view with a mock that prints expected message
        def mock_handle_view():
            print("\n📖 Opening implementation plan in pager...")
            # Simulate pager opening and closing, user returns to checkpoint
            return None

        handler._handle_view = mock_handle_view

        result = handler.execute()

        captured = capsys.readouterr()
        assert "📖 Opening implementation plan in pager..." in captured.out
        assert result.action == "approve"

    @patch('builtins.input', side_effect=['q', 'a'])
    def test_execute_question_stub(
        self,
        mock_input,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        mock_task_file_path,
        capsys
    ):
        """Test question mode enters Q&A session and returns to checkpoint."""
        handler = FullReviewHandler(
            complexity_score=mock_complexity_score,
            plan=mock_implementation_plan,
            task_metadata=mock_task_metadata,
            task_file_path=mock_task_file_path
        )

        # Replace _handle_question with a mock that simulates Q&A session
        def mock_handle_question():
            # Simulate entering Q&A mode and user returning to checkpoint
            return None

        handler._handle_question = mock_handle_question

        result = handler.execute()

        # Q&A session should have been triggered (we called 'q')
        # and then user approved (we called 'a')
        assert result.action == "approve"  # Eventually approved after returning from Q&A

    @patch('builtins.input', side_effect=['x', 'z', 'invalid', 'a'])
    def test_execute_invalid_input_retry(
        self,
        mock_input,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        mock_task_file_path,
        capsys
    ):
        """Test invalid input handling with retry."""
        handler = FullReviewHandler(
            complexity_score=mock_complexity_score,
            plan=mock_implementation_plan,
            task_metadata=mock_task_metadata,
            task_file_path=mock_task_file_path
        )

        result = handler.execute()

        captured = capsys.readouterr()
        output = captured.out

        # Should show invalid input errors
        assert "❌ Invalid choice: 'x'" in output
        assert "❌ Invalid choice: 'z'" in output
        assert "❌ Invalid choice: 'i'" in output  # First char of 'invalid'

        # Should show warning after 3 attempts
        assert "3 invalid attempts" in output

        # Eventually succeeds
        assert result.action == "approve"

    @patch('builtins.input', side_effect=['', 'a'])
    def test_execute_empty_input(
        self,
        mock_input,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        mock_task_file_path,
        capsys
    ):
        """Test empty input handling."""
        handler = FullReviewHandler(
            complexity_score=mock_complexity_score,
            plan=mock_implementation_plan,
            task_metadata=mock_task_metadata,
            task_file_path=mock_task_file_path
        )

        result = handler.execute()

        captured = capsys.readouterr()
        assert "Please enter a choice" in captured.out


class TestFullReviewResult:
    """Test suite for FullReviewResult dataclass."""

    def test_to_dict(self):
        """Test conversion to dictionary."""
        result = FullReviewResult(
            action="approve",
            timestamp="2025-10-09T10:30:00Z",
            approved=True,
            metadata_updates={"test": "data"},
            proceed_to_phase_3=True
        )

        result_dict = result.to_dict()

        assert result_dict["action"] == "approve"
        assert result_dict["timestamp"] == "2025-10-09T10:30:00Z"
        assert result_dict["approved"] is True
        assert result_dict["metadata_updates"] == {"test": "data"}
        assert result_dict["proceed_to_phase_3"] is True


class TestFileOperations:
    """Test suite for FileOperations utility."""

    def test_move_task_to_backlog(
        self,
        mock_complexity_score,
        mock_implementation_plan,
        mock_task_metadata,
        mock_task_file_path
    ):
        """Test task file move to backlog."""
        handler = FullReviewHandler(
            complexity_score=mock_complexity_score,
            plan=mock_implementation_plan,
            task_metadata=mock_task_metadata,
            task_file_path=mock_task_file_path
        )

        # Verify original file exists
        assert mock_task_file_path.exists()

        # Move to backlog
        handler._move_task_to_backlog()

        # Verify file moved
        assert not mock_task_file_path.exists()

        # backlog is at tasks/backlog, not at root/backlog
        backlog_path = mock_task_file_path.parent.parent / "backlog" / mock_task_file_path.name
        assert backlog_path.exists()

        # Verify content updated
        content = backlog_path.read_text()
        assert "status: backlog" in content
        assert "cancelled: true" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
