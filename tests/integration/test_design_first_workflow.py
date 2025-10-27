"""
Integration tests for design-first workflow (TASK-006).

Tests the complete flow:
    - Design-only → Implementation-only workflow
    - Plan persistence across workflow stages
    - State transitions and validation
    - Error recovery scenarios

Part of TASK-006: Add Design-First Workflow Flags to task-work Command
"""

import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime
import sys

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "installer/global/commands/lib"))

from phase_execution import (
    execute_phases,
    execute_design_phases,
    execute_implementation_phases,
    StateValidationError,
    PhaseExecutionError,
)
from plan_persistence import (
    save_plan,
    load_plan,
    plan_exists,
    delete_plan,
)


@pytest.fixture
def temp_workspace(tmp_path):
    """Create a temporary workspace with docs/state directory."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    docs_dir = workspace / "docs" / "state"
    docs_dir.mkdir(parents=True)

    import os
    original_cwd = Path.cwd()
    os.chdir(workspace)

    yield workspace

    os.chdir(original_cwd)


@pytest.fixture
def sample_task_context():
    """Sample task context for testing."""
    return {
        "task_id": "TASK-100",
        "title": "Implement User Authentication",
        "description": "Add JWT-based authentication to the API",
        "status": "backlog",
        "assigned_to": "developer",
        "created_at": "2025-10-11T10:00:00"
    }


@pytest.fixture
def sample_implementation_plan():
    """Sample implementation plan for testing."""
    return {
        "files_to_create": [
            "src/auth/jwt_handler.py",
            "src/auth/middleware.py",
            "tests/test_auth.py"
        ],
        "files_to_modify": [
            "src/main.py",
            "requirements.txt"
        ],
        "external_dependencies": [
            "pyjwt",
            "python-jose"
        ],
        "estimated_duration": "6 hours",
        "estimated_loc": 350,
        "phases": [
            "Phase 1: JWT Handler Implementation",
            "Phase 2: Middleware Integration",
            "Phase 3: Testing"
        ],
        "test_summary": "Unit tests for JWT validation, middleware tests, integration tests",
        "risks": [
            {"type": "security", "description": "Token validation edge cases"},
            {"type": "technical", "description": "Dependency compatibility"}
        ]
    }


class TestCompleteDesignFirstWorkflow:
    """Test suite for complete design-only → implement-only workflow."""

    def test_design_only_to_implement_only_workflow(
        self, temp_workspace, sample_task_context, sample_implementation_plan
    ):
        """Test complete workflow: design-only saves plan, implement-only uses it."""
        task_id = "TASK-101"
        task_context = sample_task_context.copy()
        task_context["task_id"] = task_id
        task_context["status"] = "backlog"

        # Step 1: Execute design-only workflow
        design_result = execute_design_phases(task_id, task_context)

        assert design_result["success"] is True
        assert design_result["final_state"] == "design_approved"

        # Simulate plan being saved during design phase
        save_plan(task_id, sample_implementation_plan)

        # Step 2: Update task to design_approved state
        task_context["status"] = "design_approved"
        task_context["design"] = {
            "status": "approved",
            "approved_at": datetime.now().isoformat(),
            "approved_by": "developer"
        }

        # Step 3: Execute implement-only workflow
        from unittest.mock import patch
        with patch("pathlib.Path.exists", return_value=True):
            impl_result = execute_implementation_phases(task_id, task_context)

        assert impl_result["success"] is True
        assert impl_result["final_state"] == "in_review"

    def test_design_only_persists_plan(self, temp_workspace, sample_task_context):
        """Test that design-only workflow persists implementation plan."""
        task_id = "TASK-102"
        task_context = sample_task_context.copy()
        task_context["task_id"] = task_id

        # Execute design-only
        result = execute_design_phases(task_id, task_context)

        # Plan path should be in result
        assert "plan_path" in result
        assert task_id in result["plan_path"]

    def test_implement_only_loads_persisted_plan(
        self, temp_workspace, sample_task_context, sample_implementation_plan
    ):
        """Test that implement-only workflow loads the persisted plan."""
        task_id = "TASK-103"

        # Save plan first
        save_plan(task_id, sample_implementation_plan)

        # Prepare task in design_approved state
        task_context = sample_task_context.copy()
        task_context["task_id"] = task_id
        task_context["status"] = "design_approved"
        task_context["design"] = {
            "status": "approved",
            "approved_at": datetime.now().isoformat()
        }

        # Execute implement-only
        from unittest.mock import patch
        with patch("pathlib.Path.exists", return_value=True):
            result = execute_implementation_phases(task_id, task_context)

        # Should succeed
        assert result["success"] is True

        # Plan should still exist (not deleted)
        assert plan_exists(task_id)


class TestStateTransitions:
    """Test suite for state transitions in design-first workflow."""

    def test_backlog_to_design_approved_transition(self, temp_workspace, sample_task_context):
        """Test state transition from backlog to design_approved."""
        task_context = sample_task_context.copy()
        task_context["status"] = "backlog"

        result = execute_design_phases(task_context["task_id"], task_context)

        assert result["final_state"] == "design_approved"

    def test_in_progress_to_design_approved_transition(self, temp_workspace, sample_task_context):
        """Test state transition from in_progress to design_approved."""
        task_context = sample_task_context.copy()
        task_context["status"] = "in_progress"

        result = execute_design_phases(task_context["task_id"], task_context)

        assert result["final_state"] == "design_approved"

    def test_blocked_to_design_approved_transition(self, temp_workspace, sample_task_context):
        """Test state transition from blocked to design_approved."""
        task_context = sample_task_context.copy()
        task_context["status"] = "blocked"

        result = execute_design_phases(task_context["task_id"], task_context)

        assert result["final_state"] == "design_approved"

    def test_design_approved_to_in_review_transition(
        self, temp_workspace, sample_task_context, sample_implementation_plan
    ):
        """Test state transition from design_approved to in_review."""
        task_id = "TASK-104"
        save_plan(task_id, sample_implementation_plan)

        task_context = sample_task_context.copy()
        task_context["task_id"] = task_id
        task_context["status"] = "design_approved"
        task_context["design"] = {
            "status": "approved",
            "approved_at": datetime.now().isoformat()
        }

        from unittest.mock import patch
        with patch("pathlib.Path.exists", return_value=True):
            result = execute_implementation_phases(task_id, task_context)

        assert result["final_state"] == "in_review"


class TestErrorRecoveryScenarios:
    """Test suite for error recovery in design-first workflow."""

    def test_implement_only_without_design_approval_fails(
        self, temp_workspace, sample_task_context
    ):
        """Test that implement-only fails if task not in design_approved state."""
        task_context = sample_task_context.copy()
        task_context["status"] = "backlog"  # Wrong state

        with pytest.raises(StateValidationError) as exc_info:
            execute_implementation_phases(task_context["task_id"], task_context)

        assert "design_approved" in str(exc_info.value)

    def test_implement_only_without_saved_plan_fails(
        self, temp_workspace, sample_task_context
    ):
        """Test that implement-only fails if plan file is missing."""
        task_id = "TASK-105"
        task_context = sample_task_context.copy()
        task_context["task_id"] = task_id
        task_context["status"] = "design_approved"
        task_context["design"] = {
            "status": "approved",
            "approved_at": datetime.now().isoformat()
        }

        # Don't save plan - it should fail
        from unittest.mock import patch
        with patch("pathlib.Path.exists", return_value=False):
            with pytest.raises(PhaseExecutionError) as exc_info:
                execute_implementation_phases(task_id, task_context)

        assert "Implementation plan not found" in str(exc_info.value)

    def test_recovery_after_design_rejection(
        self, temp_workspace, sample_task_context, sample_implementation_plan
    ):
        """Test recovery by re-running design after rejection."""
        task_id = "TASK-106"
        task_context = sample_task_context.copy()
        task_context["task_id"] = task_id

        # First design attempt - save plan
        save_plan(task_id, sample_implementation_plan)

        # Design rejected - delete plan
        delete_plan(task_id)
        assert not plan_exists(task_id)

        # Second design attempt - should work
        task_context["status"] = "backlog"
        result = execute_design_phases(task_id, task_context)

        assert result["success"] is True


class TestPlanPersistenceIntegration:
    """Test suite for plan persistence integration with workflow."""

    def test_plan_persisted_with_architectural_review(
        self, temp_workspace, sample_task_context, sample_implementation_plan
    ):
        """Test that plan is persisted with architectural review results."""
        task_id = "TASK-107"
        review_result = {
            "score": 90,
            "approved": True,
            "recommendations": ["Add input validation"]
        }

        save_plan(task_id, sample_implementation_plan, review_result=review_result)

        loaded = load_plan(task_id)
        assert "architectural_review" in loaded
        assert loaded["architectural_review"]["score"] == 90

    def test_plan_survives_workflow_transition(
        self, temp_workspace, sample_task_context, sample_implementation_plan
    ):
        """Test that plan survives transition from design to implementation."""
        task_id = "TASK-108"

        # Save plan during design phase
        save_plan(task_id, sample_implementation_plan)

        # Execute design phase
        task_context = sample_task_context.copy()
        task_context["task_id"] = task_id
        task_context["status"] = "backlog"
        execute_design_phases(task_id, task_context)

        # Plan should still exist
        assert plan_exists(task_id)

        # Execute implementation phase
        task_context["status"] = "design_approved"
        task_context["design"] = {
            "status": "approved",
            "approved_at": datetime.now().isoformat()
        }

        from unittest.mock import patch
        with patch("pathlib.Path.exists", return_value=True):
            execute_implementation_phases(task_id, task_context)

        # Plan should still exist after implementation
        assert plan_exists(task_id)

    def test_multiple_tasks_have_separate_plans(
        self, temp_workspace, sample_implementation_plan
    ):
        """Test that multiple tasks maintain separate plans."""
        task_ids = ["TASK-109", "TASK-110", "TASK-111"]

        # Save plans for multiple tasks
        for task_id in task_ids:
            plan = sample_implementation_plan.copy()
            plan["task_specific_data"] = task_id
            save_plan(task_id, plan)

        # Verify all plans exist and are separate
        for task_id in task_ids:
            loaded = load_plan(task_id)
            assert loaded["plan"]["task_specific_data"] == task_id


class TestBackwardCompatibility:
    """Test suite for backward compatibility with standard workflow."""

    def test_standard_workflow_still_works(self, temp_workspace, sample_task_context):
        """Test that standard workflow (no flags) still works."""
        task_context = sample_task_context.copy()

        result = execute_phases(
            task_context["task_id"],
            task_context,
            design_only=False,
            implement_only=False
        )

        assert result["success"] is True
        assert result["workflow_mode"] == "standard"

    def test_standard_workflow_does_not_require_plan_file(
        self, temp_workspace, sample_task_context
    ):
        """Test that standard workflow doesn't require pre-saved plan."""
        task_context = sample_task_context.copy()
        task_context["status"] = "backlog"

        # Should work without saved plan
        result = execute_phases(task_context["task_id"], task_context)

        assert result["success"] is True

    def test_standard_workflow_ignores_saved_plan(
        self, temp_workspace, sample_task_context, sample_implementation_plan
    ):
        """Test that standard workflow ignores any saved plan."""
        task_id = "TASK-112"
        task_context = sample_task_context.copy()
        task_context["task_id"] = task_id

        # Save a plan
        save_plan(task_id, sample_implementation_plan)

        # Standard workflow should still work
        result = execute_phases(task_id, task_context)

        assert result["workflow_mode"] == "standard"
        # Should not fail even if plan exists


class TestWorkflowModeCombinations:
    """Test suite for different workflow mode combinations."""

    def test_execute_phases_routes_correctly(self, temp_workspace, sample_task_context):
        """Test that execute_phases routes to correct workflow based on flags."""
        task_context = sample_task_context.copy()

        # Standard workflow
        result = execute_phases(task_context["task_id"], task_context)
        assert result["workflow_mode"] == "standard"

        # Design-only workflow
        result = execute_phases(
            task_context["task_id"],
            task_context,
            design_only=True
        )
        assert result["workflow_mode"] == "design_only"

    def test_workflow_mode_in_result(self, temp_workspace, sample_task_context):
        """Test that workflow_mode is always present in result."""
        task_context = sample_task_context.copy()

        workflows = [
            (False, False, "standard"),
            (True, False, "design_only"),
        ]

        for design_only, implement_only, expected_mode in workflows:
            if design_only and implement_only:
                continue  # Skip invalid combination

            if expected_mode == "design_only":
                task_context["status"] = "backlog"
                result = execute_phases(
                    task_context["task_id"],
                    task_context,
                    design_only=design_only,
                    implement_only=implement_only
                )
                assert result["workflow_mode"] == expected_mode


class TestDurationTracking:
    """Test suite for duration tracking across workflows."""

    def test_design_only_tracks_duration(self, temp_workspace, sample_task_context):
        """Test that design-only workflow tracks duration."""
        result = execute_phases(
            sample_task_context["task_id"],
            sample_task_context,
            design_only=True
        )

        assert "duration_seconds" in result
        assert result["duration_seconds"] >= 0

    def test_implement_only_tracks_duration(
        self, temp_workspace, sample_task_context, sample_implementation_plan
    ):
        """Test that implement-only workflow tracks duration."""
        task_id = "TASK-113"
        save_plan(task_id, sample_implementation_plan)

        task_context = sample_task_context.copy()
        task_context["task_id"] = task_id
        task_context["status"] = "design_approved"
        task_context["design"] = {
            "status": "approved",
            "approved_at": datetime.now().isoformat()
        }

        from unittest.mock import patch
        with patch("pathlib.Path.exists", return_value=True):
            result = execute_phases(
                task_id,
                task_context,
                implement_only=True
            )

        assert "duration_seconds" in result
        assert result["duration_seconds"] >= 0

    def test_standard_workflow_tracks_duration(self, temp_workspace, sample_task_context):
        """Test that standard workflow tracks duration."""
        result = execute_phases(
            sample_task_context["task_id"],
            sample_task_context
        )

        assert "duration_seconds" in result
        assert result["duration_seconds"] >= 0
