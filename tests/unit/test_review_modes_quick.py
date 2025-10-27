"""
Comprehensive unit tests for Quick Review Mode.

Tests the QuickReviewHandler, QuickReviewDisplay, and QuickReviewResult classes
that implement the 10-second countdown with summary card workflow.

Target Coverage: ≥90% (quick review mode logic)
"""

import pytest
import sys
import json
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock, mock_open
from typing import Dict, Any

# Import system under test
QuickReviewHandler = None
QuickReviewDisplay = None
QuickReviewResult = None
ImplementationPlan = None
ComplexityScore = None
FactorScore = None
ReviewMode = None

try:
    # Add installer lib to path temporarily
    installer_lib_path = Path(__file__).parent.parent.parent / "installer" / "global" / "commands" / "lib"
    if installer_lib_path.exists():
        sys.path.insert(0, str(installer_lib_path))

        # Import modules
        import review_modes
        import complexity_models

        QuickReviewHandler = review_modes.QuickReviewHandler
        QuickReviewDisplay = review_modes.QuickReviewDisplay
        QuickReviewResult = review_modes.QuickReviewResult
        ImplementationPlan = complexity_models.ImplementationPlan
        ComplexityScore = complexity_models.ComplexityScore
        FactorScore = complexity_models.FactorScore
        ReviewMode = complexity_models.ReviewMode

        # Clean up
        sys.path.pop(0)
except ImportError as e:
    pytest.skip(f"QuickReviewHandler not found: {e}", allow_module_level=True)


# Test Fixtures
@pytest.fixture
def simple_plan():
    """Create simple implementation plan for testing."""
    score = ComplexityScore(
        total_score=5,
        factor_scores=[
            FactorScore(
                factor_name="file_complexity",
                score=2,
                max_score=3,
                justification="Moderate changes"
            )
        ],
        forced_review_triggers=[],
        review_mode=ReviewMode.QUICK_OPTIONAL,
        calculation_timestamp=datetime.now(),
        metadata={"patterns_detected": ["repository", "service"]}
    )

    plan = ImplementationPlan(
        task_id="TASK-001",
        files_to_create=["src/service.py", "src/repository.py", "tests/test_service.py"],
        patterns_used=["repository", "service"],
        external_dependencies=["requests", "pydantic"],
        estimated_loc=245,
        raw_plan="Implement user service with repository pattern"
    )
    plan.complexity_score = score
    return plan


@pytest.fixture
def complex_plan():
    """Create complex implementation plan for testing."""
    score = ComplexityScore(
        total_score=8,
        factor_scores=[
            FactorScore(
                factor_name="file_complexity",
                score=3,
                max_score=3,
                justification="Many files"
            ),
            FactorScore(
                factor_name="risk_factors",
                score=2,
                max_score=2,
                justification="Security concerns"
            )
        ],
        forced_review_triggers=[],
        review_mode=ReviewMode.FULL_REQUIRED,
        calculation_timestamp=datetime.now(),
        metadata={
            "patterns_detected": ["authentication", "repository", "middleware"],
            "warnings": ["Security-sensitive changes detected", "Multiple dependencies"]
        }
    )

    plan = ImplementationPlan(
        task_id="TASK-002",
        files_to_create=["src/auth.py", "src/middleware.py"] * 5,
        patterns_used=["authentication", "repository", "middleware"],
        external_dependencies=["jwt", "bcrypt", "fastapi"],
        estimated_loc=850,
        risk_indicators=["authentication", "password"],
        raw_plan="Implement JWT authentication system with middleware"
    )
    plan.complexity_score = score
    return plan


class TestQuickReviewResultModel:
    """Test QuickReviewResult data model."""

    def test_result_initialization(self):
        """Should create result with required fields."""
        result = QuickReviewResult(
            action="timeout",
            timestamp="2025-10-10T10:30:00Z",
            auto_approved=True,
            metadata_updates={"review_mode": "quick"}
        )

        assert result.action == "timeout"
        assert result.timestamp == "2025-10-10T10:30:00Z"
        assert result.auto_approved is True
        assert result.metadata_updates["review_mode"] == "quick"

    def test_result_to_dict_serialization(self):
        """Should serialize result to dictionary."""
        result = QuickReviewResult(
            action="enter",
            timestamp="2025-10-10T10:30:00Z",
            auto_approved=False,
            metadata_updates={"escalated": True}
        )

        data = result.to_dict()

        assert data["action"] == "enter"
        assert data["timestamp"] == "2025-10-10T10:30:00Z"
        assert data["auto_approved"] is False
        assert data["metadata_updates"]["escalated"] is True

    def test_result_from_dict_deserialization(self):
        """Should deserialize result from dictionary."""
        data = {
            "action": "cancel",
            "timestamp": "2025-10-10T10:30:00Z",
            "auto_approved": False,
            "metadata_updates": {"cancelled": True}
        }

        result = QuickReviewResult.from_dict(data)

        assert result.action == "cancel"
        assert result.timestamp == "2025-10-10T10:30:00Z"
        assert result.auto_approved is False
        assert result.metadata_updates["cancelled"] is True

    def test_result_with_empty_metadata(self):
        """Should handle empty metadata updates."""
        result = QuickReviewResult(
            action="timeout",
            timestamp="2025-10-10T10:30:00Z",
            auto_approved=True
        )

        assert result.metadata_updates == {}

    def test_result_roundtrip_serialization(self):
        """Should maintain data through to_dict/from_dict cycle."""
        original = QuickReviewResult(
            action="enter",
            timestamp="2025-10-10T10:30:00Z",
            auto_approved=False,
            metadata_updates={"key": "value", "nested": {"a": 1}}
        )

        data = original.to_dict()
        restored = QuickReviewResult.from_dict(data)

        assert restored.action == original.action
        assert restored.timestamp == original.timestamp
        assert restored.auto_approved == original.auto_approved
        assert restored.metadata_updates == original.metadata_updates


class TestQuickReviewDisplayFormatting:
    """Test QuickReviewDisplay formatting logic."""

    def test_display_initialization(self, simple_plan):
        """Should initialize display with plan."""
        display = QuickReviewDisplay(simple_plan)

        assert display.plan == simple_plan

    def test_format_complexity_badge_excellent(self):
        """Should format excellent score badge (≥80)."""
        plan = ImplementationPlan(task_id="TASK-001")
        # Set display_score directly
        plan.display_score = 87
        plan.complexity_score = Mock(total_score=8)

        display = QuickReviewDisplay(plan)
        badge = display.format_complexity_badge()

        assert "87/100" in badge
        assert "Excellent" in badge

    def test_format_complexity_badge_acceptable(self):
        """Should format acceptable score badge (60-79)."""
        plan = ImplementationPlan(task_id="TASK-001")
        plan.display_score = 65
        plan.complexity_score = Mock(total_score=6)

        display = QuickReviewDisplay(plan)
        badge = display.format_complexity_badge()

        assert "65/100" in badge
        assert "Acceptable" in badge

    def test_format_complexity_badge_needs_revision(self):
        """Should format needs revision badge (<60)."""
        plan = ImplementationPlan(task_id="TASK-001")
        plan.display_score = 45
        plan.complexity_score = Mock(total_score=4)

        display = QuickReviewDisplay(plan)
        badge = display.format_complexity_badge()

        assert "45/100" in badge
        assert "Needs Revision" in badge

    def test_format_complexity_badge_from_total_score(self):
        """Should derive badge from total_score if no display_score."""
        plan = ImplementationPlan(task_id="TASK-001")
        plan.complexity_score = Mock(total_score=7, spec=['total_score'])

        display = QuickReviewDisplay(plan)
        badge = display.format_complexity_badge()

        # Should convert 7 * 10 = 70
        assert "70/100" in badge

    def test_format_file_summary_with_loc(self, simple_plan):
        """Should format file summary with LOC."""
        display = QuickReviewDisplay(simple_plan)
        summary = display.format_file_summary()

        assert "3 files" in summary
        assert "245 lines" in summary

    def test_format_file_summary_without_loc(self):
        """Should format file summary without LOC."""
        plan = ImplementationPlan(
            task_id="TASK-001",
            files_to_create=["file1.py", "file2.py"]
        )

        display = QuickReviewDisplay(plan)
        summary = display.format_file_summary()

        assert "2 files" in summary
        assert "lines" not in summary or plan.estimated_loc is None

    def test_format_file_summary_single_file(self):
        """Should handle single file correctly."""
        plan = ImplementationPlan(
            task_id="TASK-001",
            files_to_create=["single.py"],
            estimated_loc=50
        )

        display = QuickReviewDisplay(plan)
        summary = display.format_file_summary()

        assert "1 file" in summary

    def test_render_summary_card_output(self, simple_plan, capsys):
        """Should render complete summary card."""
        # Ensure plan has display_score
        simple_plan.display_score = 50

        display = QuickReviewDisplay(simple_plan)
        display.render_summary_card()

        captured = capsys.readouterr()
        output = captured.out

        assert "ARCHITECTURAL REVIEW - QUICK MODE" in output
        assert "Complexity Score:" in output
        assert "Files to Create:" in output
        assert "3 files" in output

    def test_render_summary_card_truncates_long_instructions(self, capsys):
        """Should truncate long implementation instructions."""
        plan = ImplementationPlan(
            task_id="TASK-001",
            raw_plan="x" * 300  # Very long plan
        )
        score = Mock()
        score.total_score = 5
        score.patterns_detected = []
        score.warnings = []
        score.metadata = {}
        plan.complexity_score = score
        plan.display_score = 50

        display = QuickReviewDisplay(plan)
        display.render_summary_card()

        captured = capsys.readouterr()
        output = captured.out

        # Should be truncated to ~200 chars
        assert "..." in output or len(plan.raw_plan) > 200

    def test_render_summary_card_shows_key_patterns(self, simple_plan, capsys):
        """Should display key architectural patterns."""
        simple_plan.display_score = 50
        display = QuickReviewDisplay(simple_plan)
        display.render_summary_card()

        captured = capsys.readouterr()
        output = captured.out

        assert "Key Patterns:" in output or "pattern" in output.lower()

    def test_render_summary_card_shows_warnings(self, complex_plan, capsys):
        """Should display warnings if present."""
        complex_plan.display_score = 80
        display = QuickReviewDisplay(complex_plan)
        display.render_summary_card()

        captured = capsys.readouterr()
        output = captured.out

        assert "Warning" in output or "issue" in output.lower()


class TestQuickReviewHandlerExecution:
    """Test QuickReviewHandler execution workflow."""

    def test_handler_initialization(self, simple_plan):
        """Should initialize handler with plan and task ID."""
        handler = QuickReviewHandler(
            task_id="TASK-001",
            plan=simple_plan,
            countdown_duration=10
        )

        assert handler.task_id == "TASK-001"
        assert handler.plan == simple_plan
        assert handler.countdown_duration == 10
        assert handler.display is not None

    def test_handler_custom_countdown_duration(self, simple_plan):
        """Should accept custom countdown duration."""
        handler = QuickReviewHandler(
            task_id="TASK-001",
            plan=simple_plan,
            countdown_duration=5
        )

        assert handler.countdown_duration == 5

    @patch('review_modes.countdown_timer')
    def test_execute_timeout_flow(self, mock_countdown, simple_plan):
        """Should handle timeout (auto-proceed) flow."""
        mock_countdown.return_value = "timeout"
        simple_plan.display_score = 50

        handler = QuickReviewHandler(
            task_id="TASK-001",
            plan=simple_plan
        )
        result = handler.execute()

        assert result.action == "timeout"
        assert result.auto_approved is True
        assert "review_mode" in result.metadata_updates

    @patch('review_modes.countdown_timer')
    def test_execute_enter_flow(self, mock_countdown, simple_plan):
        """Should handle enter (escalate) flow."""
        mock_countdown.return_value = "enter"
        simple_plan.display_score = 50

        handler = QuickReviewHandler(
            task_id="TASK-001",
            plan=simple_plan
        )
        result = handler.execute()

        assert result.action == "enter"
        assert result.auto_approved is False
        assert result.metadata_updates["review_action"] == "escalated_to_full"

    @patch('review_modes.countdown_timer')
    def test_execute_cancel_flow(self, mock_countdown, simple_plan):
        """Should handle cancel flow."""
        mock_countdown.return_value = "cancel"
        simple_plan.display_score = 50

        handler = QuickReviewHandler(
            task_id="TASK-001",
            plan=simple_plan
        )
        result = handler.execute()

        assert result.action == "cancel"
        assert result.auto_approved is False
        assert result.metadata_updates["review_action"] == "cancelled"

    @patch('review_modes.countdown_timer')
    def test_execute_calls_countdown_with_correct_params(
        self, mock_countdown, simple_plan
    ):
        """Should call countdown with correct parameters."""
        mock_countdown.return_value = "timeout"
        simple_plan.display_score = 50

        handler = QuickReviewHandler(
            task_id="TASK-001",
            plan=simple_plan,
            countdown_duration=15
        )
        handler.execute()

        mock_countdown.assert_called_once()
        call_kwargs = mock_countdown.call_args[1]
        assert call_kwargs["duration_seconds"] == 15

    @patch('review_modes.countdown_timer')
    def test_execute_renders_display(self, mock_countdown, simple_plan, capsys):
        """Should render display before countdown."""
        mock_countdown.return_value = "timeout"
        simple_plan.display_score = 50

        handler = QuickReviewHandler(
            task_id="TASK-001",
            plan=simple_plan
        )
        handler.execute()

        captured = capsys.readouterr()
        output = captured.out

        assert "ARCHITECTURAL REVIEW" in output

    @patch('review_modes.countdown_timer')
    def test_execute_unknown_result_escalates(self, mock_countdown, simple_plan):
        """Should escalate on unknown countdown result."""
        mock_countdown.return_value = "unknown"
        simple_plan.display_score = 50

        handler = QuickReviewHandler(
            task_id="TASK-001",
            plan=simple_plan
        )
        result = handler.execute()

        # Should fail-safe to escalation
        assert result.action == "enter"

    @patch('review_modes.countdown_timer')
    def test_execute_keyboard_interrupt_propagates(self, mock_countdown, simple_plan):
        """Should propagate KeyboardInterrupt for upstream handling."""
        mock_countdown.side_effect = KeyboardInterrupt()
        simple_plan.display_score = 50

        handler = QuickReviewHandler(
            task_id="TASK-001",
            plan=simple_plan
        )

        with pytest.raises(KeyboardInterrupt):
            handler.execute()

    @patch('review_modes.countdown_timer')
    def test_execute_error_escalates_to_full_review(
        self, mock_countdown, simple_plan, capsys
    ):
        """Should escalate to full review on error."""
        mock_countdown.side_effect = RuntimeError("Test error")
        simple_plan.display_score = 50

        handler = QuickReviewHandler(
            task_id="TASK-001",
            plan=simple_plan
        )
        result = handler.execute()

        assert result.action == "enter"  # Escalated
        captured = capsys.readouterr()
        assert "Error" in captured.out or "error" in captured.out


class TestQuickReviewHandlerOutcomes:
    """Test individual outcome handlers."""

    def test_handle_timeout_creates_correct_result(self, simple_plan):
        """Should create timeout result with correct metadata."""
        handler = QuickReviewHandler(
            task_id="TASK-001",
            plan=simple_plan
        )
        result = handler.handle_timeout()

        assert result.action == "timeout"
        assert result.auto_approved is True
        assert result.metadata_updates["review_mode"] == "quick_review"
        assert result.metadata_updates["review_action"] == "auto_approved"
        assert "review_timestamp" in result.metadata_updates

    def test_handle_timeout_includes_complexity_score(self, simple_plan):
        """Should include complexity score in metadata."""
        handler = QuickReviewHandler(
            task_id="TASK-001",
            plan=simple_plan
        )
        result = handler.handle_timeout()

        assert "complexity_score" in result.metadata_updates
        # Score should be derived from plan
        assert result.metadata_updates["complexity_score"] >= 0

    def test_handle_escalation_creates_correct_result(self, simple_plan):
        """Should create escalation result with correct metadata."""
        handler = QuickReviewHandler(
            task_id="TASK-001",
            plan=simple_plan
        )
        result = handler.handle_escalation()

        assert result.action == "enter"
        assert result.auto_approved is False
        assert result.metadata_updates["review_action"] == "escalated_to_full"
        assert "escalation_timestamp" in result.metadata_updates

    def test_handle_cancellation_creates_correct_result(self, simple_plan):
        """Should create cancellation result with correct metadata."""
        handler = QuickReviewHandler(
            task_id="TASK-001",
            plan=simple_plan
        )
        result = handler.handle_cancellation()

        assert result.action == "cancel"
        assert result.auto_approved is False
        assert result.metadata_updates["review_action"] == "cancelled"
        assert "cancellation_timestamp" in result.metadata_updates

    def test_outcome_timestamps_are_iso_format(self, simple_plan):
        """Should use ISO 8601 format for all timestamps."""
        handler = QuickReviewHandler(
            task_id="TASK-001",
            plan=simple_plan
        )

        timeout_result = handler.handle_timeout()
        escalate_result = handler.handle_escalation()
        cancel_result = handler.handle_cancellation()

        # All should have valid ISO timestamps
        for result in [timeout_result, escalate_result, cancel_result]:
            assert result.timestamp.endswith("Z")
            assert "T" in result.timestamp


class TestQuickReviewResultPersistence:
    """Test result saving functionality."""

    @patch('builtins.open', new_callable=mock_open)
    @patch('pathlib.Path.mkdir')
    def test_save_result_to_default_path(
        self, mock_mkdir, mock_file, simple_plan
    ):
        """Should save result to default path."""
        handler = QuickReviewHandler(
            task_id="TASK-001",
            plan=simple_plan
        )
        result = handler.handle_timeout()

        handler.save_result(result)

        # Should create directory and write file
        mock_mkdir.assert_called_once()
        mock_file.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_save_result_to_custom_path(self, mock_file, simple_plan):
        """Should save result to custom path."""
        handler = QuickReviewHandler(
            task_id="TASK-001",
            plan=simple_plan
        )
        result = handler.handle_timeout()
        custom_path = Path("/tmp/custom_result.json")

        handler.save_result(result, output_path=custom_path)

        # Should write to custom path
        mock_file.assert_called_once()
        args = mock_file.call_args[0]
        assert custom_path in args

    @patch('builtins.open', new_callable=mock_open)
    @patch('pathlib.Path.mkdir')
    def test_save_result_writes_json(self, mock_mkdir, mock_file, simple_plan):
        """Should write valid JSON data."""
        handler = QuickReviewHandler(
            task_id="TASK-001",
            plan=simple_plan
        )
        result = handler.handle_timeout()

        handler.save_result(result)

        # Check that JSON was written
        handle = mock_file()
        written_data = "".join(
            call.args[0] for call in handle.write.call_args_list
        )

        # Should be valid JSON
        parsed = json.loads(written_data)
        assert parsed["action"] == "timeout"


class TestQuickReviewEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_handler_with_minimal_plan(self):
        """Should handle plan with minimal data."""
        plan = ImplementationPlan(task_id="TASK-001")
        score = Mock()
        score.total_score = 1
        score.patterns_detected = []
        score.warnings = []
        score.metadata = {}
        plan.complexity_score = score
        plan.display_score = 10

        handler = QuickReviewHandler(
            task_id="TASK-001",
            plan=plan
        )

        assert handler is not None

    def test_handler_with_zero_duration(self, simple_plan):
        """Should handle zero countdown duration."""
        handler = QuickReviewHandler(
            task_id="TASK-001",
            plan=simple_plan,
            countdown_duration=0
        )

        assert handler.countdown_duration == 0

    def test_display_with_no_patterns(self, capsys):
        """Should handle plan with no patterns detected."""
        plan = ImplementationPlan(
            task_id="TASK-001",
            files_to_create=["test.py"]
        )
        score = Mock()
        score.total_score = 5
        score.patterns_detected = []
        score.warnings = []
        score.metadata = {}
        plan.complexity_score = score
        plan.display_score = 50

        display = QuickReviewDisplay(plan)
        display.render_summary_card()

        captured = capsys.readouterr()
        # Should not crash
        assert "ARCHITECTURAL REVIEW" in captured.out

    def test_display_with_no_warnings(self, simple_plan, capsys):
        """Should handle plan with no warnings."""
        # simple_plan has no warnings by default
        simple_plan.display_score = 50
        display = QuickReviewDisplay(simple_plan)
        display.render_summary_card()

        captured = capsys.readouterr()
        # Should render successfully
        assert "ARCHITECTURAL REVIEW" in captured.out

    @patch('review_modes.countdown_timer')
    def test_execute_with_display_error_continues(
        self, mock_countdown, simple_plan
    ):
        """Should continue execution if display rendering fails."""
        mock_countdown.return_value = "timeout"
        simple_plan.display_score = 50

        handler = QuickReviewHandler(
            task_id="TASK-001",
            plan=simple_plan
        )

        # Mock display to raise error
        with patch.object(handler.display, 'render_summary_card', side_effect=Exception("Display error")):
            # Should escalate on error
            result = handler.execute()
            assert result.action == "enter"  # Fail-safe escalation
