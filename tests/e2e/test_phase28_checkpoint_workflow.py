"""
End-to-End tests for Phase 2.8 Checkpoint workflow (TASK-028).

Tests the complete workflow from plan creation through checkpoint display,
simulating real-world usage scenarios.

Focus: Complete workflows, user experience, real file system operations.
"""

import pytest
from pathlib import Path
import sys
import tempfile
import shutil
import time

# Add lib directory to path for imports
lib_path = Path(__file__).parent.parent.parent / "installer" / "global" / "commands" / "lib"
sys.path.insert(0, str(lib_path))

from checkpoint_display import (
    display_phase28_checkpoint,
    load_plan_summary,
    format_plan_summary
)
from plan_persistence import (
    save_plan,
    load_plan,
    plan_exists,
    get_plan_path,
    delete_plan
)


@pytest.fixture
def project_workspace():
    """Create a complete project workspace for E2E testing."""
    temp_dir = tempfile.mkdtemp()
    original_cwd = Path.cwd()

    # Create complete project structure
    workspace = Path(temp_dir)
    (workspace / "docs" / "state").mkdir(parents=True)
    (workspace / "src").mkdir(parents=True)
    (workspace / "tests").mkdir(parents=True)

    # Change to workspace
    import os
    os.chdir(workspace)

    yield workspace

    # Cleanup
    os.chdir(original_cwd)
    shutil.rmtree(temp_dir, ignore_errors=True)


class TestCompleteWorkflow:
    """E2E tests for complete Phase 2.8 checkpoint workflow."""

    def test_simple_task_workflow(self, project_workspace, capsys):
        """
        E2E Test: Simple task workflow (complexity 1-3).

        Workflow:
        1. Create task with simple implementation plan
        2. Save plan to disk
        3. Display checkpoint (should auto-proceed)
        4. Verify plan can be loaded later
        """
        task_id = "TASK-SIMPLE-001"

        # Step 1: Create simple plan
        plan = {
            "files_to_create": ["src/utils.py"],
            "files_to_modify": [],
            "external_dependencies": [],
            "estimated_duration": "1 hour",
            "estimated_loc": 50,
            "complexity_score": 2,
            "test_summary": "Basic unit tests"
        }

        # Step 2: Save plan
        plan_path = save_plan(task_id, plan)
        assert Path(plan_path).exists()

        # Step 3: Display checkpoint
        display_phase28_checkpoint(task_id, 2)
        captured = capsys.readouterr()

        # Verify output
        assert "TASK-SIMPLE-001" in captured.out
        assert "2/10 (Simple - auto-proceed)" in captured.out
        assert "src/utils.py" in captured.out
        assert "1 hour" in captured.out

        # Step 4: Verify plan can be reloaded
        summary = load_plan_summary(task_id)
        assert summary is not None
        assert summary.effort.duration == "1 hour"

    def test_medium_task_workflow(self, project_workspace, capsys):
        """
        E2E Test: Medium task workflow (complexity 4-6).

        Workflow:
        1. Create medium complexity plan with dependencies
        2. Save and display checkpoint (quick review)
        3. Verify all data displayed correctly
        """
        task_id = "TASK-MEDIUM-001"

        # Step 1: Create medium complexity plan
        plan = {
            "files_to_create": [
                "src/api/endpoints.py",
                "src/models/user.py"
            ],
            "files_to_modify": ["src/main.py"],
            "external_dependencies": [
                {"name": "fastapi", "version": "0.95.0", "purpose": "API framework"},
                {"name": "pydantic", "version": "1.10.0"}
            ],
            "risks": [
                {"description": "API changes may break clients", "level": "medium"}
            ],
            "estimated_duration": "4 hours",
            "estimated_loc": 200,
            "complexity_score": 5,
            "test_summary": "Unit tests for endpoints, integration tests for API"
        }

        # Step 2: Save and display
        save_plan(task_id, plan)
        display_phase28_checkpoint(task_id, 5)
        captured = capsys.readouterr()

        # Step 3: Verify complete output
        assert "5/10 (Medium - quick review)" in captured.out
        assert "Files to Change (3)" in captured.out
        assert "src/api/endpoints.py (create)" in captured.out
        assert "src/main.py (modify)" in captured.out
        assert "Dependencies (2)" in captured.out
        assert "fastapi (0.95.0)" in captured.out
        assert "Risks (1)" in captured.out
        assert "🟡 MEDIUM: API changes may break clients" in captured.out
        assert "Effort Estimate:" in captured.out
        assert "4 hours" in captured.out
        assert "~200" in captured.out
        assert "Testing Approach:" in captured.out

    def test_complex_task_workflow(self, project_workspace, capsys):
        """
        E2E Test: Complex task workflow (complexity 7-10).

        Workflow:
        1. Create complex plan with multiple risks and phases
        2. Save plan with architectural review
        3. Display checkpoint (requires full review)
        4. Verify warning shown for complex tasks
        """
        task_id = "TASK-COMPLEX-001"

        # Step 1: Create complex plan
        plan = {
            "files_to_create": [
                "src/domain/entities.py",
                "src/domain/repositories.py",
                "src/application/use_cases.py",
                "src/infrastructure/database.py"
            ],
            "files_to_modify": [
                "src/main.py",
                "src/config.py"
            ],
            "external_dependencies": [
                {"name": "sqlalchemy", "version": "2.0.0", "purpose": "ORM"},
                {"name": "alembic", "version": "1.10.0", "purpose": "Migrations"},
                {"name": "redis", "version": "4.5.0", "purpose": "Caching"}
            ],
            "risks": [
                {
                    "description": "Database migration may fail in production",
                    "level": "high",
                    "mitigation": "Test migrations on staging first"
                },
                {
                    "description": "Performance impact of new ORM queries",
                    "level": "medium",
                    "mitigation": "Add query profiling"
                },
                "Cache invalidation complexity"
            ],
            "estimated_duration": "2 days",
            "estimated_loc": 600,
            "complexity_score": 9,
            "test_summary": "Unit tests for domain, integration for repositories, E2E for use cases",
            "phases": [
                "Phase 1: Domain model design",
                "Phase 2: Repository implementation",
                "Phase 3: Use case implementation",
                "Phase 4: Database migrations"
            ]
        }

        review_result = {
            "score": 82,
            "passed": True,
            "recommendations": [
                "Consider using Repository pattern",
                "Add caching layer"
            ]
        }

        # Step 2: Save plan with review
        save_plan(task_id, plan, review_result)

        # Step 3: Display checkpoint
        display_phase28_checkpoint(task_id, 9)
        captured = capsys.readouterr()

        # Step 4: Verify complete display
        assert "9/10 (Complex - requires full review)" in captured.out
        assert "Files to Change (6)" in captured.out
        assert "Dependencies (3)" in captured.out
        assert "Risks (3)" in captured.out
        assert "🔴 HIGH: Database migration may fail" in captured.out
        assert "Mitigation: Test migrations on staging first" in captured.out
        assert "🟡 MEDIUM: Performance impact" in captured.out
        assert "Effort Estimate:" in captured.out
        assert "2 days" in captured.out
        assert "~600" in captured.out
        assert "9/10" in captured.out

    def test_checkpoint_without_saved_plan(self, project_workspace, capsys):
        """
        E2E Test: Checkpoint display without saved plan.

        Workflow:
        1. Attempt to display checkpoint for task without plan
        2. Verify warning message displayed
        3. Verify checkpoint options still shown
        """
        task_id = "TASK-NO-PLAN"

        display_phase28_checkpoint(task_id, 5)
        captured = capsys.readouterr()

        assert "TASK-NO-PLAN" in captured.out
        assert "⚠️  No implementation plan found" in captured.out
        assert "[A]pprove" in captured.out
        assert "[M]odify" in captured.out
        assert "[C]ancel" in captured.out

    def test_checkpoint_complex_task_no_plan(self, project_workspace, capsys):
        """
        E2E Test: Complex task checkpoint without saved plan (should warn).

        Workflow:
        1. Display checkpoint for complex task without plan
        2. Verify warning about missing plan for complex task
        """
        display_phase28_checkpoint("TASK-COMPLEX-NO-PLAN", 8)
        captured = capsys.readouterr()

        assert "⚠️  No implementation plan found" in captured.out
        assert "WARNING: Complex task without saved plan" in captured.out
        assert "--design-only" in captured.out


class TestPlanLifecycle:
    """E2E tests for complete plan lifecycle."""

    def test_plan_create_modify_delete_lifecycle(self, project_workspace):
        """
        E2E Test: Complete plan lifecycle.

        Workflow:
        1. Create and save plan
        2. Verify plan exists
        3. Load and modify plan
        4. Delete plan
        5. Verify plan no longer exists
        """
        task_id = "TASK-LIFECYCLE"

        # Step 1: Create plan
        plan_v1 = {
            "files_to_create": ["file1.py"],
            "estimated_duration": "2 hours"
        }
        save_plan(task_id, plan_v1)

        # Step 2: Verify exists
        assert plan_exists(task_id)
        path = get_plan_path(task_id)
        assert path is not None
        assert path.exists()

        # Step 3: Load and verify
        loaded = load_plan(task_id)
        assert loaded["plan"]["estimated_duration"] == "2 hours"

        # Step 4: Delete plan
        delete_plan(task_id)

        # Step 5: Verify deleted
        assert not plan_exists(task_id)
        assert get_plan_path(task_id) is None

    def test_plan_versioning_workflow(self, project_workspace):
        """
        E2E Test: Plan versioning (save, modify, save again).

        Workflow:
        1. Save initial plan
        2. Load and modify
        3. Save updated plan
        4. Verify updates persisted
        """
        task_id = "TASK-VERSION"

        # Version 1
        plan_v1 = {
            "files_to_create": ["initial.py"],
            "estimated_duration": "1 hour"
        }
        save_plan(task_id, plan_v1)

        summary_v1 = load_plan_summary(task_id)
        assert len(summary_v1.files_to_change) == 1

        # Version 2 (updated)
        plan_v2 = {
            "files_to_create": ["initial.py", "additional.py"],
            "estimated_duration": "3 hours"
        }
        save_plan(task_id, plan_v2)

        summary_v2 = load_plan_summary(task_id)
        assert len(summary_v2.files_to_change) == 2
        assert summary_v2.effort.duration == "3 hours"


class TestRealWorldScenarios:
    """E2E tests for real-world usage scenarios."""

    def test_feature_development_workflow(self, project_workspace, capsys):
        """
        E2E Test: Complete feature development workflow.

        Scenario: Adding user authentication feature
        """
        task_id = "TASK-AUTH-FEATURE"

        # Realistic authentication feature plan
        plan = {
            "files_to_create": [
                "src/auth/jwt_handler.py",
                "src/auth/password_hasher.py",
                "src/auth/middleware.py",
                "tests/unit/test_jwt_handler.py",
                "tests/unit/test_password_hasher.py",
                "tests/integration/test_auth_flow.py"
            ],
            "files_to_modify": [
                "src/main.py",
                "src/config.py",
                "requirements.txt"
            ],
            "external_dependencies": [
                {"name": "pyjwt", "version": "2.6.0", "purpose": "JWT tokens"},
                {"name": "passlib", "version": "1.7.4", "purpose": "Password hashing"},
                {"name": "python-multipart", "version": "0.0.6", "purpose": "Form data"}
            ],
            "risks": [
                {
                    "description": "JWT secret key security",
                    "level": "high",
                    "mitigation": "Use environment variables, rotate keys"
                },
                {
                    "description": "Password hashing performance",
                    "level": "medium",
                    "mitigation": "Use bcrypt with appropriate rounds"
                }
            ],
            "estimated_duration": "1 day",
            "estimated_loc": 350,
            "complexity_score": 7,
            "test_summary": "Unit tests for handlers, integration tests for auth flow, security tests",
            "phases": [
                "Phase 1: JWT handler implementation",
                "Phase 2: Password hashing",
                "Phase 3: Middleware integration",
                "Phase 4: Testing and security review"
            ]
        }

        save_plan(task_id, plan)
        display_phase28_checkpoint(task_id, 7)
        captured = capsys.readouterr()

        # Verify realistic output
        assert "TASK-AUTH-FEATURE" in captured.out
        assert "Files to Change (9)" in captured.out
        assert "src/auth/jwt_handler.py" in captured.out
        assert "tests/unit/test_jwt_handler.py" in captured.out
        assert "Dependencies (3)" in captured.out
        assert "pyjwt (2.6.0)" in captured.out
        assert "Risks (2)" in captured.out
        assert "🔴 HIGH: JWT secret key security" in captured.out
        assert "Use environment variables" in captured.out

    def test_bug_fix_workflow(self, project_workspace, capsys):
        """
        E2E Test: Bug fix workflow (typically simpler).

        Scenario: Fixing validation bug
        """
        task_id = "TASK-BUG-FIX"

        plan = {
            "files_to_create": [
                "tests/unit/test_validation_fix.py"
            ],
            "files_to_modify": [
                "src/validators.py"
            ],
            "external_dependencies": [],
            "risks": [
                {"description": "May affect other validations", "level": "low"}
            ],
            "estimated_duration": "2 hours",
            "estimated_loc": 30,
            "complexity_score": 3,
            "test_summary": "Regression test for bug, unit tests for fix"
        }

        save_plan(task_id, plan)
        display_phase28_checkpoint(task_id, 3)
        captured = capsys.readouterr()

        assert "3/10 (Simple - auto-proceed)" in captured.out
        assert "Files to Change (2)" in captured.out
        assert "~30" in captured.out

    def test_refactoring_workflow(self, project_workspace, capsys):
        """
        E2E Test: Code refactoring workflow.

        Scenario: Extract service layer from controller
        """
        task_id = "TASK-REFACTOR"

        plan = {
            "files_to_create": [
                "src/services/user_service.py",
                "src/services/order_service.py",
                "tests/unit/test_user_service.py",
                "tests/unit/test_order_service.py"
            ],
            "files_to_modify": [
                "src/controllers/user_controller.py",
                "src/controllers/order_controller.py"
            ],
            "external_dependencies": [],
            "risks": [
                {
                    "description": "Breaking existing controller logic",
                    "level": "medium",
                    "mitigation": "Comprehensive regression testing"
                }
            ],
            "estimated_duration": "6 hours",
            "estimated_loc": 400,
            "complexity_score": 6,
            "test_summary": "Unit tests for services, integration tests for controllers",
            "phases": [
                "Phase 1: Extract user service",
                "Phase 2: Extract order service",
                "Phase 3: Update controllers",
                "Phase 4: Run regression tests"
            ]
        }

        save_plan(task_id, plan)
        display_phase28_checkpoint(task_id, 6)
        captured = capsys.readouterr()

        assert "6/10 (Medium - quick review)" in captured.out
        assert "Files to Change (6)" in captured.out
        assert "Risks (1)" in captured.out


class TestErrorRecovery:
    """E2E tests for error scenarios and recovery."""

    def test_recover_from_missing_plan(self, project_workspace, capsys):
        """
        E2E Test: Recover from missing plan scenario.

        Workflow:
        1. Try to display checkpoint without plan
        2. Create plan after error
        3. Successfully display checkpoint
        """
        task_id = "TASK-RECOVER"

        # Step 1: No plan exists
        display_phase28_checkpoint(task_id, 5)
        captured = capsys.readouterr()
        assert "⚠️  No implementation plan found" in captured.out

        # Step 2: Create plan
        plan = {
            "files_to_create": ["recovery.py"],
            "estimated_duration": "1 hour"
        }
        save_plan(task_id, plan)

        # Step 3: Successfully display
        display_phase28_checkpoint(task_id, 5)
        captured = capsys.readouterr()
        assert "Files to Change" in captured.out
        assert "recovery.py" in captured.out

    def test_handle_plan_update_during_workflow(self, project_workspace):
        """
        E2E Test: Handle plan updates during active workflow.

        Workflow:
        1. Save initial plan
        2. Load summary
        3. Update plan (simulate human modification)
        4. Load summary again
        5. Verify updated data loaded
        """
        task_id = "TASK-UPDATE"

        # Initial plan
        plan_v1 = {
            "files_to_create": ["v1.py"],
            "estimated_duration": "2 hours"
        }
        save_plan(task_id, plan_v1)

        summary_v1 = load_plan_summary(task_id)
        assert len(summary_v1.files_to_change) == 1

        # Simulate human updating plan
        time.sleep(0.1)  # Ensure timestamp difference
        plan_v2 = {
            "files_to_create": ["v1.py", "v2.py"],
            "estimated_duration": "4 hours"
        }
        save_plan(task_id, plan_v2)

        # Load updated plan
        summary_v2 = load_plan_summary(task_id)
        assert len(summary_v2.files_to_change) == 2
        assert summary_v2.effort.duration == "4 hours"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
