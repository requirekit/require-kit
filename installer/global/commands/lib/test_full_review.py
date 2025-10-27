#!/usr/bin/env python3
"""
Test suite for Full Review Mode implementation (TASK-003B-2).

Tests comprehensive coverage of:
1. FullReviewDisplay rendering methods (6 sections)
2. FullReviewHandler approval/cancel workflows
3. FileOperations atomic write operations
4. ImplementationPlan extended fields
5. User interaction edge cases
6. State management and metadata updates

Run with pytest:
    pytest test_full_review.py -v --cov=. --cov-report=term
"""

import json
import os
import re
import sys
import tempfile
import yaml
from datetime import datetime
from io import StringIO
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call

# Add parent directory to path for imports
lib_path = Path(__file__).parent
parent_path = lib_path.parent
sys.path.insert(0, str(parent_path))

from lib.complexity_models import (
    ComplexityScore,
    FactorScore,
    ForceReviewTrigger,
    ImplementationPlan,
    ReviewMode,
)
from lib.review_modes import (
    FullReviewDisplay,
    FullReviewHandler,
    FullReviewResult,
)
from lib.user_interaction import FileOperations


# ============================================================================
# Test Fixtures
# ============================================================================

def create_test_complexity_score(
    total_score: int = 8,
    triggers: list = None
) -> ComplexityScore:
    """Create a test ComplexityScore object."""
    factor_scores = [
        FactorScore(
            factor_name="file_complexity",
            score=3.0,
            max_score=3.0,
            justification="5 files to create/modify"
        ),
        FactorScore(
            factor_name="dependency_complexity",
            score=2.0,
            max_score=2.0,
            justification="Database and external API dependencies"
        ),
        FactorScore(
            factor_name="architectural_complexity",
            score=3.0,
            max_score=5.0,
            justification="Uses Factory and Strategy patterns"
        ),
    ]

    return ComplexityScore(
        total_score=total_score,
        factor_scores=factor_scores,
        forced_review_triggers=triggers or [],
        review_mode=ReviewMode.FULL_REQUIRED,
        calculation_timestamp=datetime.utcnow(),
        metadata={
            "patterns_detected": ["Factory", "Strategy", "Repository"],
            "warnings": ["Authentication logic requires security review"]
        }
    )


def create_test_implementation_plan(
    task_id: str = "TASK-003B-2",
    include_extended_fields: bool = True
) -> ImplementationPlan:
    """Create a test ImplementationPlan with optional extended fields."""
    plan = ImplementationPlan(
        task_id=task_id,
        files_to_create=[
            "src/auth/handler.py",
            "src/auth/validator.py",
            "src/api/endpoints.py",
            "tests/test_auth.py",
            "tests/test_api.py",
        ],
        patterns_used=["Factory", "Strategy", "Repository"],
        external_dependencies=["PostgreSQL", "Redis", "Auth0 API"],
        estimated_loc=450,
        risk_indicators=["authentication", "token validation"],
        raw_plan="Implement OAuth2 authentication with token validation",
    )

    if include_extended_fields:
        plan.test_summary = "Unit tests for auth handler, integration tests for API endpoints"
        plan.risk_details = [
            {
                "severity": "high",
                "description": "Token validation bypass vulnerability",
                "mitigation": "Use well-tested JWT library, implement rate limiting"
            },
            {
                "severity": "medium",
                "description": "Database connection leaks",
                "mitigation": "Use connection pooling and context managers"
            }
        ]
        plan.phases = [
            "Phase 1: Implement authentication handler (2 hours)",
            "Phase 2: Create API endpoints (1.5 hours)",
            "Phase 3: Write comprehensive tests (1 hour)",
            "Phase 4: Security review and hardening (30 mins)"
        ]
        plan.implementation_instructions = "Follow OWASP guidelines for authentication"
        plan.estimated_duration = "4-5 hours"
        plan.complexity_score = create_test_complexity_score()

    return plan


def create_test_task_metadata(task_id: str = "TASK-003B-2") -> dict:
    """Create test task metadata."""
    return {
        "id": task_id,
        "title": "Implement OAuth2 Authentication",
        "status": "in_progress",
        "priority": "high",
        "created": "2025-10-09T10:00:00Z",
        "updated": "2025-10-09T10:30:00Z",
    }


# ============================================================================
# FullReviewDisplay Tests
# ============================================================================

class TestFullReviewDisplay:
    """Test suite for FullReviewDisplay rendering."""

    def test_display_initialization(self):
        """Test FullReviewDisplay initializes correctly."""
        score = create_test_complexity_score()
        plan = create_test_implementation_plan()
        metadata = create_test_task_metadata()

        display = FullReviewDisplay(
            complexity_score=score,
            plan=plan,
            task_metadata=metadata,
            escalated=True
        )

        assert display.complexity_score == score
        assert display.plan == plan
        assert display.task_metadata == metadata
        assert display.escalated is True

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_header_renders_correctly(self, mock_stdout):
        """Test _display_header renders task info and complexity."""
        score = create_test_complexity_score(total_score=8)
        plan = create_test_implementation_plan()
        metadata = create_test_task_metadata()

        display = FullReviewDisplay(score, plan, metadata, escalated=True)
        display._display_header()

        output = mock_stdout.getvalue()

        # Check task info
        assert "TASK-003B-2" in output
        assert "Implement OAuth2 Authentication" in output

        # Check complexity score
        assert "8/10" in output

        # Check escalation indicator
        assert "Escalated" in output or "⬆" in output

        # Check estimated duration
        assert "4-5 hours" in output

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_complexity_breakdown(self, mock_stdout):
        """Test _display_complexity_breakdown shows all factors."""
        score = create_test_complexity_score()
        plan = create_test_implementation_plan()
        metadata = create_test_task_metadata()

        display = FullReviewDisplay(score, plan, metadata)
        display._display_complexity_breakdown()

        output = mock_stdout.getvalue()

        # Check all factor names appear
        assert "file_complexity" in output
        assert "dependency_complexity" in output
        assert "architectural_complexity" in output

        # Check scores and justifications
        assert "3.0/3.0" in output or "3/3" in output
        assert "5 files to create/modify" in output
        assert "Database and external API dependencies" in output

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_complexity_with_force_triggers(self, mock_stdout):
        """Test complexity breakdown shows force-review triggers."""
        triggers = [ForceReviewTrigger.SECURITY_KEYWORDS, ForceReviewTrigger.BREAKING_CHANGES]
        score = create_test_complexity_score(triggers=triggers)
        plan = create_test_implementation_plan()
        metadata = create_test_task_metadata()

        display = FullReviewDisplay(score, plan, metadata)
        display._display_complexity_breakdown()

        output = mock_stdout.getvalue()

        # Check trigger section appears
        assert "FORCE-REVIEW TRIGGERS" in output or "TRIGGER" in output
        assert "Security" in output or "SECURITY" in output
        assert "Breaking" in output or "BREAKING" in output

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_changes_summary(self, mock_stdout):
        """Test _display_changes_summary shows files and dependencies."""
        score = create_test_complexity_score()
        plan = create_test_implementation_plan()
        metadata = create_test_task_metadata()

        display = FullReviewDisplay(score, plan, metadata)
        display._display_changes_summary()

        output = mock_stdout.getvalue()

        # Check file count
        assert "5" in output  # 5 files

        # Check at least some files listed
        assert "auth/handler.py" in output or "handler.py" in output
        assert "test_auth.py" in output or "auth" in output

        # Check dependencies
        assert "PostgreSQL" in output or "Redis" in output

        # Check test summary
        assert "Unit tests" in output or "integration tests" in output

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_changes_summary_handles_many_files(self, mock_stdout):
        """Test changes summary truncates long file lists."""
        score = create_test_complexity_score()
        plan = create_test_implementation_plan()
        # Add many files
        plan.files_to_create = [f"src/module_{i}.py" for i in range(15)]
        metadata = create_test_task_metadata()

        display = FullReviewDisplay(score, plan, metadata)
        display._display_changes_summary()

        output = mock_stdout.getvalue()

        # Check it indicates more files
        assert "15" in output  # Total count
        assert "more" in output or "..." in output  # Truncation indicator

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_risk_assessment_with_details(self, mock_stdout):
        """Test _display_risk_assessment shows risk details."""
        score = create_test_complexity_score()
        plan = create_test_implementation_plan()
        metadata = create_test_task_metadata()

        display = FullReviewDisplay(score, plan, metadata)
        display._display_risk_assessment()

        output = mock_stdout.getvalue()

        # Check risk details appear
        assert "Token validation bypass" in output
        assert "high" in output.lower() or "HIGH" in output

        # Check mitigations appear
        assert "JWT library" in output or "mitigation" in output.lower()

        # Check medium risk also shown
        assert "medium" in output.lower() or "MEDIUM" in output
        assert "Database connection leaks" in output

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_risk_assessment_fallback_to_indicators(self, mock_stdout):
        """Test risk assessment falls back to risk_indicators if no details."""
        score = create_test_complexity_score()
        plan = create_test_implementation_plan(include_extended_fields=False)
        plan.risk_indicators = ["authentication", "token validation"]
        metadata = create_test_task_metadata()

        display = FullReviewDisplay(score, plan, metadata)
        display._display_risk_assessment()

        output = mock_stdout.getvalue()

        # Check risk indicators shown as fallback
        assert "authentication" in output
        assert "token validation" in output

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_implementation_order(self, mock_stdout):
        """Test _display_implementation_order shows phases."""
        score = create_test_complexity_score()
        plan = create_test_implementation_plan()
        metadata = create_test_task_metadata()

        display = FullReviewDisplay(score, plan, metadata)
        display._display_implementation_order()

        output = mock_stdout.getvalue()

        # Check phases appear
        assert "Phase 1" in output
        assert "authentication handler" in output

        # Check estimated LOC
        assert "450" in output

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_decision_options(self, mock_stdout):
        """Test _display_decision_options shows all actions."""
        score = create_test_complexity_score()
        plan = create_test_implementation_plan()
        metadata = create_test_task_metadata()

        display = FullReviewDisplay(score, plan, metadata)
        display._display_decision_options()

        output = mock_stdout.getvalue()

        # Check all options present
        assert "[A]" in output and "Approve" in output
        assert "[M]" in output and "Modify" in output
        assert "[V]" in output and "View" in output
        assert "[Q]" in output and "Question" in output
        assert "[C]" in output and "Cancel" in output

        # Check coming soon indicators
        assert "TASK-003B-3" in output
        assert "TASK-003B-4" in output

    @patch('sys.stdout', new_callable=StringIO)
    @patch('os.get_terminal_size')
    def test_render_full_checkpoint_complete(self, mock_term_size, mock_stdout):
        """Test render_full_checkpoint renders all sections."""
        mock_term_size.return_value = MagicMock(columns=100)

        score = create_test_complexity_score()
        plan = create_test_implementation_plan()
        metadata = create_test_task_metadata()

        display = FullReviewDisplay(score, plan, metadata)
        display.render_full_checkpoint()

        output = mock_stdout.getvalue()

        # Check all major sections present
        assert "IMPLEMENTATION PLAN REVIEW" in output
        assert "COMPLEXITY BREAKDOWN" in output or "📊" in output
        assert "CHANGES SUMMARY" in output or "📁" in output
        assert "RISK ASSESSMENT" in output or "⚠" in output
        assert "IMPLEMENTATION ORDER" in output or "📋" in output
        assert "DECISION OPTIONS" in output

    @patch('sys.stdout', new_callable=StringIO)
    @patch('os.get_terminal_size')
    def test_terminal_width_detection_with_fallback(self, mock_term_size, mock_stdout):
        """Test terminal width detection with exception fallback."""
        # Simulate terminal size unavailable
        mock_term_size.side_effect = Exception("No terminal")

        score = create_test_complexity_score()
        plan = create_test_implementation_plan()
        metadata = create_test_task_metadata()

        display = FullReviewDisplay(score, plan, metadata)
        display.render_full_checkpoint()

        # Should not raise exception, uses default width
        output = mock_stdout.getvalue()
        assert "IMPLEMENTATION PLAN REVIEW" in output


# ============================================================================
# FullReviewHandler Tests
# ============================================================================

class TestFullReviewHandler:
    """Test suite for FullReviewHandler workflow."""

    def setup_handler(self, task_id="TASK-003B-2", escalated=False):
        """Setup test handler with mocked task file."""
        score = create_test_complexity_score()
        plan = create_test_implementation_plan(task_id)
        metadata = create_test_task_metadata(task_id)

        # Create temp task file
        task_dir = Path(tempfile.mkdtemp()) / "tasks" / "in_progress"
        task_dir.mkdir(parents=True, exist_ok=True)
        task_file = task_dir / f"{task_id}.md"

        # Write task file with frontmatter
        content = f"""---
id: {task_id}
title: Test Task
status: in_progress
---

# Task Content
"""
        task_file.write_text(content)

        handler = FullReviewHandler(
            complexity_score=score,
            plan=plan,
            task_metadata=metadata,
            task_file_path=task_file,
            escalated=escalated
        )

        return handler, task_file

    def test_handler_initialization(self):
        """Test FullReviewHandler initializes correctly."""
        handler, task_file = self.setup_handler()

        assert handler.task_metadata["id"] == "TASK-003B-2"
        assert handler.task_file_path == task_file
        assert handler.escalated is False
        assert isinstance(handler.display, FullReviewDisplay)

        # Cleanup
        task_file.unlink()

    @patch('builtins.input', return_value='a')
    @patch('sys.stdout', new_callable=StringIO)
    def test_approval_workflow(self, mock_stdout, mock_input):
        """Test approval workflow sets correct metadata."""
        handler, task_file = self.setup_handler()

        result = handler.execute()

        # Check result
        assert result.action == "approve"
        assert result.approved is True
        assert result.proceed_to_phase_3 is True

        # Check metadata
        assert "implementation_plan" in result.metadata_updates
        assert result.metadata_updates["implementation_plan"]["approved"] is True
        assert result.metadata_updates["implementation_plan"]["approved_by"] == "user"

        # Check timestamp
        assert "Z" in result.timestamp

        # Cleanup
        task_file.unlink()

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_cancellation_workflow_with_confirmation(self, mock_stdout, mock_input):
        """Test cancellation workflow with user confirmation."""
        handler, task_file = self.setup_handler()

        # First input 'c' for cancel, second 'y' for confirmation
        mock_input.side_effect = ['c', 'y']

        result = handler.execute()

        # Check result
        assert result.action == "cancel"
        assert result.approved is False
        assert result.proceed_to_phase_3 is False

        # Check metadata
        assert result.metadata_updates["status"] == "backlog"
        assert result.metadata_updates["cancelled"] is True

        # Check file moved to backlog (using hardcoded path from implementation)
        backlog_file = Path("tasks/backlog") / task_file.name
        assert backlog_file.exists(), f"Expected backlog file at {backlog_file}"
        assert not task_file.exists()

        # Cleanup
        backlog_file.unlink()

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_cancellation_abort(self, mock_stdout, mock_input):
        """Test cancellation can be aborted."""
        handler, task_file = self.setup_handler()

        # First 'c' for cancel, 'n' to abort, then 'a' to approve
        mock_input.side_effect = ['c', 'n', 'a']

        result = handler.execute()

        # Should end up with approval
        assert result.action == "approve"

        # Task file should still be in in_progress
        assert task_file.exists()

        # Cleanup
        task_file.unlink()

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_modify_stub_displays_message(self, mock_stdout, mock_input):
        """Test modify action displays coming soon message."""
        handler, task_file = self.setup_handler()

        # Try modify, then approve
        mock_input.side_effect = ['m', 'a']

        result = handler.execute()

        output = mock_stdout.getvalue()

        # Check stub message
        assert "Modify mode coming soon" in output or "TASK-003B-3" in output

        # Eventually approves
        assert result.action == "approve"

        # Cleanup
        task_file.unlink()

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_view_stub_displays_message(self, mock_stdout, mock_input):
        """Test view action displays coming soon message."""
        handler, task_file = self.setup_handler()

        # Try view, then approve
        mock_input.side_effect = ['v', 'a']

        result = handler.execute()

        output = mock_stdout.getvalue()

        # Check stub message
        assert "View mode coming soon" in output or "TASK-003B-3" in output

        # Eventually approves
        assert result.action == "approve"

        # Cleanup
        task_file.unlink()

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_question_stub_displays_message(self, mock_stdout, mock_input):
        """Test question action displays coming soon message."""
        handler, task_file = self.setup_handler()

        # Try question, then approve
        mock_input.side_effect = ['q', 'a']

        result = handler.execute()

        output = mock_stdout.getvalue()

        # Check stub message
        assert "Q&A mode coming soon" in output or "TASK-003B-4" in output

        # Eventually approves
        assert result.action == "approve"

        # Cleanup
        task_file.unlink()

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_input_handling(self, mock_stdout, mock_input):
        """Test invalid input shows error and retries."""
        handler, task_file = self.setup_handler()

        # Invalid inputs, then valid
        mock_input.side_effect = ['x', 'z', 'a']

        result = handler.execute()

        output = mock_stdout.getvalue()

        # Check error messages
        assert "Invalid choice" in output or "invalid" in output.lower()

        # Eventually succeeds
        assert result.action == "approve"

        # Cleanup
        task_file.unlink()

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_empty_input_handling(self, mock_stdout, mock_input):
        """Test empty input is handled gracefully."""
        handler, task_file = self.setup_handler()

        # Empty input, then valid
        mock_input.side_effect = ['', '   ', 'a']

        result = handler.execute()

        output = mock_stdout.getvalue()

        # Should prompt for input
        assert "choice" in output.lower() or "please enter" in output.lower()

        # Eventually succeeds
        assert result.action == "approve"

        # Cleanup
        task_file.unlink()

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_max_retries_warning(self, mock_stdout, mock_input):
        """Test max retries shows warning."""
        handler, task_file = self.setup_handler()

        # Multiple invalid inputs (trigger warning), then valid
        mock_input.side_effect = ['x', 'y', 'z', 'a']

        result = handler.execute()

        output = mock_stdout.getvalue()

        # Check for retry warning (after 3 invalid attempts)
        assert "invalid attempts" in output.lower() or "review options" in output.lower()

        # Cleanup
        task_file.unlink()

    @patch('builtins.input', side_effect=KeyboardInterrupt())
    @patch('sys.stdout', new_callable=StringIO)
    def test_keyboard_interrupt_handled_as_cancellation(self, mock_stdout, mock_input):
        """Test Ctrl+C is treated as cancellation."""
        handler, task_file = self.setup_handler()

        result = handler.execute()

        # Should be cancelled
        assert result.action == "cancel"

        output = mock_stdout.getvalue()
        assert "Interrupt" in output or "cancelled" in output.lower()

        # Cleanup (file may or may not exist depending on timing)
        if task_file.exists():
            task_file.unlink()

        # Cleanup backlog file if created
        backlog_file = Path("tasks/backlog") / task_file.name
        if backlog_file.exists():
            backlog_file.unlink()


# ============================================================================
# FileOperations Tests
# ============================================================================

class TestFileOperations:
    """Test suite for FileOperations utility."""

    def test_atomic_write_success(self):
        """Test atomic write creates file with correct content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.txt"
            content = "Test content\nLine 2\nLine 3"

            FileOperations.atomic_write(file_path, content)

            # Check file exists and has correct content
            assert file_path.exists()
            assert file_path.read_text() == content

    def test_atomic_write_creates_parent_dirs(self):
        """Test atomic write creates parent directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "subdir" / "nested" / "test.txt"
            content = "Nested file content"

            FileOperations.atomic_write(file_path, content)

            # Check file exists
            assert file_path.exists()
            assert file_path.read_text() == content

    def test_atomic_write_overwrites_existing(self):
        """Test atomic write overwrites existing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.txt"

            # Write initial content
            file_path.write_text("Initial content")

            # Overwrite with atomic write
            new_content = "Updated content"
            FileOperations.atomic_write(file_path, new_content)

            # Check content updated
            assert file_path.read_text() == new_content

    def test_atomic_write_encoding(self):
        """Test atomic write respects encoding parameter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "unicode.txt"
            content = "Unicode content: 你好 🎉"

            FileOperations.atomic_write(file_path, content, encoding="utf-8")

            # Read back with same encoding
            assert file_path.read_text(encoding="utf-8") == content

    def test_atomic_write_invalid_path_type(self):
        """Test atomic write raises error for non-Path input."""
        try:
            FileOperations.atomic_write("not_a_path_object", "content")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Path object" in str(e)


# ============================================================================
# ImplementationPlan Extended Fields Tests
# ============================================================================

class TestImplementationPlanExtensions:
    """Test suite for ImplementationPlan extended fields."""

    def test_plan_with_all_extended_fields(self):
        """Test ImplementationPlan supports all extended fields."""
        plan = create_test_implementation_plan(include_extended_fields=True)

        # Check extended fields present
        assert plan.test_summary is not None
        assert plan.risk_details is not None
        assert plan.phases is not None
        assert plan.implementation_instructions is not None
        assert plan.estimated_duration is not None
        assert plan.complexity_score is not None

    def test_plan_without_extended_fields(self):
        """Test ImplementationPlan works without extended fields."""
        plan = create_test_implementation_plan(include_extended_fields=False)

        # Check extended fields are None/empty
        assert plan.test_summary is None
        assert plan.risk_details is None
        assert plan.phases is None
        assert plan.implementation_instructions is None
        assert plan.estimated_duration is None
        assert plan.complexity_score is None

    def test_plan_backward_compatibility(self):
        """Test ImplementationPlan maintains backward compatibility."""
        # Create plan with only original fields
        plan = ImplementationPlan(
            task_id="TASK-OLD",
            files_to_create=["file1.py"],
            patterns_used=["Factory"],
            external_dependencies=["API"],
            estimated_loc=100,
            risk_indicators=["security"],
            raw_plan="Old plan format"
        )

        # Check original fields work
        assert plan.task_id == "TASK-OLD"
        assert plan.file_count == 1
        assert plan.dependency_count == 1

        # Check extended fields default to None
        assert plan.test_summary is None
        assert plan.risk_details is None

    def test_plan_property_methods(self):
        """Test ImplementationPlan property methods work."""
        plan = create_test_implementation_plan()

        # Check file_count
        assert plan.file_count == 5

        # Check dependency_count
        assert plan.dependency_count == 3

        # Check has_security_keywords
        assert plan.has_security_keywords is True

        # Check has_schema_changes
        assert plan.has_schema_changes is False


# ============================================================================
# Integration Tests
# ============================================================================

class TestFullReviewIntegration:
    """Integration tests for complete workflows."""

    @patch('builtins.input', return_value='a')
    @patch('sys.stdout', new_callable=StringIO)
    def test_full_approve_workflow_end_to_end(self, mock_stdout, mock_input):
        """Test complete approval workflow from display to result."""
        # Setup
        score = create_test_complexity_score()
        plan = create_test_implementation_plan()
        metadata = create_test_task_metadata()

        task_dir = Path(tempfile.mkdtemp()) / "tasks" / "in_progress"
        task_dir.mkdir(parents=True, exist_ok=True)
        task_file = task_dir / "TASK-003B-2.md"
        task_file.write_text("---\nid: TASK-003B-2\n---\n\nContent")

        # Execute
        handler = FullReviewHandler(score, plan, metadata, task_file)
        result = handler.execute()

        output = mock_stdout.getvalue()

        # Verify display rendered
        assert "IMPLEMENTATION PLAN REVIEW" in output
        assert "COMPLEXITY BREAKDOWN" in output or "📊" in output

        # Verify result
        assert result.action == "approve"
        assert result.approved is True
        assert result.proceed_to_phase_3 is True

        # Cleanup
        task_file.unlink()

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_full_cancel_workflow_end_to_end(self, mock_stdout, mock_input):
        """Test complete cancellation workflow with file move."""
        # Setup
        score = create_test_complexity_score()
        plan = create_test_implementation_plan()
        metadata = create_test_task_metadata()

        task_dir = Path(tempfile.mkdtemp()) / "tasks" / "in_progress"
        task_dir.mkdir(parents=True, exist_ok=True)
        task_file = task_dir / "TASK-003B-2.md"
        task_file.write_text("---\nid: TASK-003B-2\n---\n\nContent")

        # Execute (cancel + confirm)
        mock_input.side_effect = ['c', 'y']

        handler = FullReviewHandler(score, plan, metadata, task_file)
        result = handler.execute()

        # Verify result
        assert result.action == "cancel"
        assert result.metadata_updates["status"] == "backlog"

        # Verify file moved (using hardcoded path from implementation)
        backlog_file = Path("tasks/backlog") / "TASK-003B-2.md"
        assert backlog_file.exists(), f"Expected backlog file at {backlog_file}"
        assert not task_file.exists()

        # Verify frontmatter updated
        content = backlog_file.read_text()
        assert "status: backlog" in content

        # Cleanup
        backlog_file.unlink()


# ============================================================================
# Main Test Runner
# ============================================================================

if __name__ == "__main__":
    import pytest

    # Run tests with coverage
    exit_code = pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "-k", "test_",
    ])

    sys.exit(exit_code)
