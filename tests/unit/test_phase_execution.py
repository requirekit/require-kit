"""
Unit tests for phase_execution.py - Phase execution orchestration for design-first workflow.

Tests cover:
    - Main execute_phases routing logic
    - Design-only workflow execution
    - Implementation-only workflow execution
    - Standard workflow execution (backward compatibility)
    - State validation for different workflows
    - Error handling and edge cases
    - Duration tracking
    - Phase execution results

Part of TASK-006: Add Design-First Workflow Flags to task-work Command
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "installer/global/commands/lib"))

from phase_execution import (
    execute_phases,
    execute_design_phases,
    execute_implementation_phases,
    execute_standard_phases,
    PhaseExecutionError,
    StateValidationError,
)


class TestExecutePhases:
    """Test suite for main execute_phases entry point."""

    def test_standard_workflow_no_flags(self):
        """Test execute_phases routes to standard workflow when no flags."""
        task_context = {
            "task_id": "TASK-006",
            "title": "Test Task",
            "status": "in_progress"
        }

        result = execute_phases("TASK-006", task_context)

        assert result["success"] is True
        assert result["workflow_mode"] == "standard"
        assert "duration_seconds" in result
        assert isinstance(result["duration_seconds"], float)
        assert result["duration_seconds"] >= 0

    def test_design_only_workflow(self):
        """Test execute_phases routes to design-only workflow."""
        task_context = {
            "task_id": "TASK-006",
            "title": "Test Task",
            "status": "backlog"
        }

        result = execute_phases("TASK-006", task_context, design_only=True)

        assert result["success"] is True
        assert result["workflow_mode"] == "design_only"
        assert result["final_state"] == "design_approved"
        assert "phases_executed" in result
        assert len(result["phases_executed"]) > 0

    def test_implement_only_workflow(self):
        """Test execute_phases routes to implementation-only workflow."""
        task_context = {
            "task_id": "TASK-006",
            "title": "Test Task",
            "status": "design_approved",
            "design": {
                "status": "approved",
                "approved_at": "2025-10-11T10:00:00",
                "approved_by": "developer"
            }
        }

        # Create mock plan file
        with patch("pathlib.Path.exists", return_value=True):
            result = execute_phases("TASK-006", task_context, implement_only=True)

        assert result["success"] is True
        assert result["workflow_mode"] == "implement_only"

    def test_mutual_exclusivity_both_flags_raises_error(self):
        """Test that using both flags raises ValueError."""
        task_context = {"task_id": "TASK-006", "status": "backlog"}

        with pytest.raises(ValueError) as exc_info:
            execute_phases("TASK-006", task_context, design_only=True, implement_only=True)

        assert "Cannot use both" in str(exc_info.value)
        assert "--design-only" in str(exc_info.value)
        assert "--implement-only" in str(exc_info.value)

    def test_duration_tracking(self):
        """Test that duration is tracked correctly."""
        task_context = {"task_id": "TASK-006", "status": "backlog"}

        result = execute_phases("TASK-006", task_context)

        assert "duration_seconds" in result
        assert result["duration_seconds"] >= 0
        assert result["duration_seconds"] < 5  # Should be very fast for mock

    def test_stack_parameter_passed_through(self):
        """Test that stack parameter is passed to workflow functions."""
        task_context = {"task_id": "TASK-006", "status": "backlog"}

        result = execute_phases("TASK-006", task_context, stack="python")

        assert result["success"] is True
        # Stack parameter should be used internally


class TestExecuteDesignPhases:
    """Test suite for execute_design_phases function."""

    def test_design_phases_from_backlog_state(self):
        """Test design phases can execute from backlog state."""
        task_context = {
            "task_id": "TASK-006",
            "title": "Test Task",
            "status": "backlog"
        }

        result = execute_design_phases("TASK-006", task_context)

        assert result["success"] is True
        assert result["final_state"] == "design_approved"
        assert result["design_approved"] is True
        assert "TASK-006" in result["plan_path"]

    def test_design_phases_from_in_progress_state(self):
        """Test design phases can execute from in_progress state."""
        task_context = {
            "task_id": "TASK-007",
            "status": "in_progress"
        }

        result = execute_design_phases("TASK-007", task_context)

        assert result["success"] is True
        assert result["final_state"] == "design_approved"

    def test_design_phases_from_blocked_state(self):
        """Test design phases can execute from blocked state."""
        task_context = {
            "task_id": "TASK-008",
            "status": "blocked"
        }

        result = execute_design_phases("TASK-008", task_context)

        assert result["success"] is True

    def test_design_phases_from_invalid_state_raises_error(self):
        """Test design phases from invalid state raises StateValidationError."""
        task_context = {
            "task_id": "TASK-009",
            "status": "completed"
        }

        with pytest.raises(StateValidationError) as exc_info:
            execute_design_phases("TASK-009", task_context)

        assert "Cannot execute design-only workflow" in str(exc_info.value)
        assert "completed" in str(exc_info.value)

    def test_design_phases_valid_states_list(self):
        """Test valid states for design phases."""
        valid_states = ["backlog", "in_progress", "blocked"]

        for state in valid_states:
            task_context = {"task_id": f"TASK-{state}", "status": state}
            result = execute_design_phases(f"TASK-{state}", task_context)
            assert result["success"] is True

    def test_design_phases_includes_all_design_phases(self):
        """Test that all design phases are included in execution."""
        task_context = {"task_id": "TASK-010", "status": "backlog"}

        result = execute_design_phases("TASK-010", task_context)

        phases = result["phases_executed"]
        assert "Phase 1: Load Task Context" in phases
        assert "Phase 2: Implementation Planning" in phases
        assert "Phase 2.5B: Architectural Review" in phases
        assert "Phase 2.7: Complexity Evaluation" in phases
        assert "Phase 2.8: Design Approval Checkpoint" in phases

    def test_design_phases_plan_path_format(self):
        """Test that plan path follows expected format."""
        task_context = {"task_id": "TASK-011", "status": "backlog"}

        result = execute_design_phases("TASK-011", task_context)

        assert result["plan_path"] == "docs/state/TASK-011/implementation_plan.json"

    def test_design_phases_includes_architectural_review(self):
        """Test that architectural review result is included."""
        task_context = {"task_id": "TASK-012", "status": "backlog"}

        result = execute_design_phases("TASK-012", task_context)

        assert "architectural_review" in result
        assert isinstance(result["architectural_review"], dict)

    def test_design_phases_includes_complexity_evaluation(self):
        """Test that complexity evaluation is included."""
        task_context = {"task_id": "TASK-013", "status": "backlog"}

        result = execute_design_phases("TASK-013", task_context)

        assert "complexity_evaluation" in result
        assert isinstance(result["complexity_evaluation"], dict)


class TestExecuteImplementationPhases:
    """Test suite for execute_implementation_phases function."""

    def test_implementation_phases_requires_design_approved_state(self):
        """Test that implementation phases require design_approved state."""
        task_context = {
            "task_id": "TASK-014",
            "status": "design_approved",
            "design": {
                "status": "approved",
                "approved_at": "2025-10-11T10:00:00"
            }
        }

        with patch("pathlib.Path.exists", return_value=True):
            result = execute_implementation_phases("TASK-014", task_context)

        assert result["success"] is True
        assert result["final_state"] == "in_review"

    def test_implementation_phases_from_backlog_raises_error(self):
        """Test that implementation phases from backlog raises StateValidationError."""
        task_context = {
            "task_id": "TASK-015",
            "status": "backlog"
        }

        with pytest.raises(StateValidationError) as exc_info:
            execute_implementation_phases("TASK-015", task_context)

        assert "Cannot execute --implement-only workflow" in str(exc_info.value)
        assert "backlog" in str(exc_info.value)
        assert "design_approved" in str(exc_info.value)

    def test_implementation_phases_from_in_progress_raises_error(self):
        """Test that implementation phases from in_progress raises error."""
        task_context = {
            "task_id": "TASK-016",
            "status": "in_progress"
        }

        with pytest.raises(StateValidationError) as exc_info:
            execute_implementation_phases("TASK-016", task_context)

        assert "Required state: design_approved" in str(exc_info.value)

    def test_implementation_phases_missing_design_metadata_raises_error(self):
        """Test missing design metadata raises PhaseExecutionError."""
        task_context = {
            "task_id": "TASK-017",
            "status": "design_approved"
            # Missing design metadata
        }

        with pytest.raises(PhaseExecutionError) as exc_info:
            execute_implementation_phases("TASK-017", task_context)

        assert "Design metadata missing" in str(exc_info.value)

    def test_implementation_phases_invalid_design_status_raises_error(self):
        """Test invalid design status raises PhaseExecutionError."""
        task_context = {
            "task_id": "TASK-018",
            "status": "design_approved",
            "design": {
                "status": "pending"  # Not approved
            }
        }

        with pytest.raises(PhaseExecutionError) as exc_info:
            execute_implementation_phases("TASK-018", task_context)

        assert "Design metadata missing or invalid" in str(exc_info.value)

    def test_implementation_phases_missing_plan_file_raises_error(self):
        """Test missing plan file raises PhaseExecutionError."""
        task_context = {
            "task_id": "TASK-019",
            "status": "design_approved",
            "design": {
                "status": "approved",
                "approved_at": "2025-10-11T10:00:00"
            }
        }

        with patch("pathlib.Path.exists", return_value=False):
            with pytest.raises(PhaseExecutionError) as exc_info:
                execute_implementation_phases("TASK-019", task_context)

        assert "Implementation plan not found" in str(exc_info.value)

    def test_implementation_phases_includes_all_phases(self):
        """Test that all implementation phases are executed."""
        task_context = {
            "task_id": "TASK-020",
            "status": "design_approved",
            "design": {
                "status": "approved",
                "approved_at": "2025-10-11T10:00:00"
            }
        }

        with patch("pathlib.Path.exists", return_value=True):
            result = execute_implementation_phases("TASK-020", task_context)

        phases = result["phases_executed"]
        assert "Phase 3: Implementation" in phases
        assert "Phase 4: Testing" in phases
        assert "Phase 4.5: Fix Loop" in phases
        assert "Phase 5: Code Review" in phases

    def test_implementation_phases_includes_test_results(self):
        """Test that test results are included in response."""
        task_context = {
            "task_id": "TASK-021",
            "status": "design_approved",
            "design": {
                "status": "approved",
                "approved_at": "2025-10-11T10:00:00"
            }
        }

        with patch("pathlib.Path.exists", return_value=True):
            result = execute_implementation_phases("TASK-021", task_context)

        assert "test_results" in result
        assert "tests_passed" in result
        assert "quality_gates" in result

    @patch("builtins.print")
    def test_implementation_phases_displays_design_context(self, mock_print):
        """Test that design context is displayed at start."""
        task_context = {
            "task_id": "TASK-022",
            "title": "Test Implementation",
            "status": "design_approved",
            "design": {
                "status": "approved",
                "approved_at": "2025-10-11T10:00:00",
                "approved_by": "developer",
                "architectural_review_score": 85,
                "complexity_score": 6
            }
        }

        with patch("pathlib.Path.exists", return_value=True):
            execute_implementation_phases("TASK-022", task_context)

        # Check that design info was printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        output = "".join(print_calls)
        assert "IMPLEMENTATION PHASE" in output or "TASK-022" in output


class TestExecuteStandardPhases:
    """Test suite for execute_standard_phases function."""

    def test_standard_phases_executes_all_phases(self):
        """Test that standard workflow executes all phases."""
        task_context = {"task_id": "TASK-023", "status": "backlog"}

        result = execute_standard_phases("TASK-023", task_context)

        assert result["success"] is True
        assert result["final_state"] == "in_review"
        assert len(result["phases_executed"]) >= 8

    def test_standard_phases_includes_design_and_implementation(self):
        """Test that standard phases include both design and implementation."""
        task_context = {"task_id": "TASK-024", "status": "in_progress"}

        result = execute_standard_phases("TASK-024", task_context)

        phases = result["phases_executed"]
        # Design phases
        assert any("Implementation Planning" in p for p in phases)
        assert any("Architectural Review" in p for p in phases)
        # Implementation phases
        assert any("Implementation" in p for p in phases)
        assert any("Testing" in p for p in phases)
        assert any("Code Review" in p for p in phases)

    def test_standard_phases_backward_compatibility(self):
        """Test that standard workflow maintains backward compatibility."""
        task_context = {"task_id": "TASK-025", "status": "backlog"}

        result = execute_standard_phases("TASK-025", task_context)

        # Should have same structure as before TASK-006
        assert "success" in result
        assert "phases_executed" in result
        assert "final_state" in result

    def test_standard_phases_with_different_stack(self):
        """Test standard phases with different technology stack."""
        task_context = {"task_id": "TASK-026", "status": "backlog"}

        result = execute_standard_phases("TASK-026", task_context, stack="react")

        assert result["success"] is True

    def test_standard_phases_workflow_note_present(self):
        """Test that workflow note is included."""
        task_context = {"task_id": "TASK-027", "status": "backlog"}

        result = execute_standard_phases("TASK-027", task_context)

        assert "workflow_note" in result
        assert "Standard workflow" in result["workflow_note"]


class TestStateValidation:
    """Test suite for state validation across workflows."""

    def test_design_only_valid_states(self):
        """Test all valid states for design-only workflow."""
        valid_states = ["backlog", "in_progress", "blocked"]

        for state in valid_states:
            task_context = {"task_id": f"TASK-{state}", "status": state}
            result = execute_design_phases(f"TASK-{state}", task_context)
            assert result["success"] is True, f"Failed for state: {state}"

    def test_design_only_invalid_states(self):
        """Test invalid states for design-only workflow."""
        invalid_states = ["completed", "in_review", "cancelled", "archived"]

        for state in invalid_states:
            task_context = {"task_id": f"TASK-{state}", "status": state}
            with pytest.raises(StateValidationError):
                execute_design_phases(f"TASK-{state}", task_context)

    def test_implement_only_requires_exact_state(self):
        """Test implement-only requires exactly design_approved state."""
        states = ["backlog", "in_progress", "blocked", "in_review", "completed"]

        for state in states:
            task_context = {"task_id": f"TASK-{state}", "status": state}
            with pytest.raises(StateValidationError):
                execute_implementation_phases(f"TASK-{state}", task_context)


class TestErrorMessages:
    """Test suite for error message quality."""

    def test_mutual_exclusivity_error_is_helpful(self):
        """Test that mutual exclusivity error provides helpful guidance."""
        task_context = {"task_id": "TASK-028", "status": "backlog"}

        with pytest.raises(ValueError) as exc_info:
            execute_phases("TASK-028", task_context, design_only=True, implement_only=True)

        error_msg = str(exc_info.value)
        assert "Choose one workflow mode" in error_msg
        assert "--design-only" in error_msg
        assert "--implement-only" in error_msg
        assert "(no flags)" in error_msg

    def test_state_validation_error_is_actionable(self):
        """Test that state validation errors provide actionable guidance."""
        task_context = {"task_id": "TASK-029", "status": "completed"}

        with pytest.raises(StateValidationError) as exc_info:
            execute_design_phases("TASK-029", task_context)

        error_msg = str(exc_info.value)
        assert "completed" in error_msg
        assert "Valid states" in error_msg or "backlog" in error_msg

    def test_missing_plan_error_provides_recovery_steps(self):
        """Test that missing plan error provides recovery steps."""
        task_context = {
            "task_id": "TASK-030",
            "status": "design_approved",
            "design": {"status": "approved"}
        }

        with patch("pathlib.Path.exists", return_value=False):
            with pytest.raises(PhaseExecutionError) as exc_info:
                execute_implementation_phases("TASK-030", task_context)

        error_msg = str(exc_info.value)
        assert "Re-run design phase" in error_msg or "--design-only" in error_msg


class TestEdgeCases:
    """Test suite for edge cases and boundary conditions."""

    def test_execute_phases_with_empty_task_context(self):
        """Test execute_phases handles empty task context gracefully."""
        task_context = {}

        result = execute_phases("TASK-031", task_context)

        # Should not crash, may have unknown state
        assert "workflow_mode" in result

    def test_execute_phases_with_missing_status(self):
        """Test execute_phases when status is missing."""
        task_context = {"task_id": "TASK-032"}

        # Should handle gracefully or raise appropriate error
        try:
            result = execute_phases("TASK-032", task_context)
            assert "workflow_mode" in result
        except (StateValidationError, KeyError):
            pass  # Acceptable to raise error for missing status

    def test_design_phases_with_unknown_stack(self):
        """Test design phases with unknown technology stack."""
        task_context = {"task_id": "TASK-033", "status": "backlog"}

        result = execute_design_phases("TASK-033", task_context, stack="unknown_stack")

        # Should handle gracefully
        assert result["success"] is True

    def test_implementation_phases_plan_path_construction(self):
        """Test that plan path is constructed correctly."""
        task_context = {
            "task_id": "TASK-034",
            "status": "design_approved",
            "design": {"status": "approved"}
        }

        with patch("pathlib.Path.exists", return_value=False):
            with pytest.raises(PhaseExecutionError) as exc_info:
                execute_implementation_phases("TASK-034", task_context)

        # Error should mention the expected path
        assert "TASK-034" in str(exc_info.value)
        assert "implementation_plan.json" in str(exc_info.value)
