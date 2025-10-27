"""
Integration tests for complete modification workflow.

Tests cover:
    - Complete modification loop (view → modify → save → recalculate)
    - Session persistence and recovery
    - Plan versioning workflow
    - Review mode change scenarios
    - Error recovery and edge cases
"""

import pytest
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "installer/global/commands"))

from lib.complexity_models import (
    ImplementationPlan,
    ComplexityScore,
    ReviewMode,
    FactorScore,
    EvaluationContext,
)
from lib.change_tracker import ChangeTracker
from lib.modification_session import ModificationSession, SessionState
from lib.modification_applier import ModificationApplier
from lib.modification_persistence import ModificationPersistence
from lib.version_manager import VersionManager
from lib.pager_display import PagerDisplay


# Test Fixtures
@pytest.fixture
def temp_workspace(tmp_path):
    """Create temporary workspace for integration tests."""
    workspace = {
        "base": tmp_path,
        "tasks": tmp_path / "tasks",
        "versions": tmp_path / "tasks" / "versions",
        "modifications": tmp_path / "tasks" / "modifications",
    }

    for dir_path in workspace.values():
        if isinstance(dir_path, Path):
            dir_path.mkdir(parents=True, exist_ok=True)

    return workspace


@pytest.fixture
def sample_plan():
    """Create sample implementation plan."""
    complexity_score = ComplexityScore(
        total_score=5,
        factor_scores=[
            FactorScore(
                factor_name="File Complexity",
                score=1.5,
                max_score=3.0,
                justification="3 files (low complexity)"
            )
        ],
        forced_review_triggers=[],
        review_mode=ReviewMode.QUICK_OPTIONAL,
        calculation_timestamp=datetime.utcnow(),
        metadata={}
    )

    return ImplementationPlan(
        task_id="TASK-INT-001",
        files_to_create=[
            "src/repository.py",
            "src/models.py",
            "tests/test_repository.py"
        ],
        patterns_used=["Repository", "Factory"],
        external_dependencies=["sqlalchemy"],
        estimated_loc=150,
        risk_indicators=["database"],
        raw_plan="Implement repository pattern for data access",
        test_summary="Unit tests: 10, Integration tests: 5",
        risk_details=[
            {
                "severity": "medium",
                "description": "Database connection management",
                "mitigation": "Use connection pooling"
            }
        ],
        phases=[
            "Phase 1: Define repository interface",
            "Phase 2: Implement concrete repository",
            "Phase 3: Write tests"
        ],
        implementation_instructions="Implement repository with SQLAlchemy",
        estimated_duration="2 hours",
        complexity_score=complexity_score
    )


class TestCompleteModificationWorkflow:
    """Test complete modification workflow end-to-end."""

    def test_view_and_modify_workflow(self, temp_workspace, sample_plan):
        """Test complete view → modify → save workflow."""
        # Step 1: View plan in pager
        display = PagerDisplay()
        formatted_content = display._format_plan(sample_plan)

        assert "TASK-INT-001" in formatted_content
        assert "src/repository.py" in formatted_content

        # Step 2: Start modification session
        session = ModificationSession(
            plan=sample_plan,
            task_id="TASK-INT-001",
            user_name="integration_test"
        )
        session.start()

        assert session.is_active

        # Step 3: Make modifications
        session.change_tracker.record_file_added(
            "src/connection_pool.py",
            purpose="Connection pooling",
            estimated_loc=50
        )
        session.change_tracker.record_dependency_added(
            "psycopg2",
            purpose="PostgreSQL adapter"
        )
        session.change_tracker.record_metadata_updated(
            "estimated_loc",
            old_value=150,
            new_value=200
        )

        assert session.change_tracker.change_count == 3

        # Step 4: Apply changes
        applier = ModificationApplier(sample_plan, session.change_tracker)
        modified_plan = applier.apply()

        assert "src/connection_pool.py" in modified_plan.files_to_create
        assert "psycopg2" in modified_plan.external_dependencies
        assert modified_plan.estimated_loc == 200

        # Step 5: Save session
        persistence = ModificationPersistence(
            task_id="TASK-INT-001",
            base_dir=temp_workspace["modifications"]
        )
        session.end(save=True)
        saved_path = persistence.save_session(session)

        assert saved_path.exists()

        # Step 6: Create new version
        version_manager = VersionManager(
            task_id="TASK-INT-001",
            base_dir=temp_workspace["versions"]
        )
        version = version_manager.create_version(
            plan=modified_plan,
            change_reason="Added connection pooling and PostgreSQL support",
            created_by="integration_test"
        )

        assert version.version_number == 1
        assert version.plan.file_count == 4

    def test_session_recovery_after_error(self, temp_workspace, sample_plan):
        """Test session can be recovered after error."""
        # Start session and make changes
        session = ModificationSession(
            plan=sample_plan,
            task_id="TASK-INT-001"
        )
        session.start()
        session.change_tracker.record_file_added("src/new_file.py")

        # Save session
        persistence = ModificationPersistence(
            task_id="TASK-INT-001",
            base_dir=temp_workspace["modifications"]
        )
        session.end()
        persistence.save_session(session)

        # Simulate crash/restart - load session
        session_id = session.metadata.session_id
        recovered_session = persistence.load_session(session_id)

        assert recovered_session is not None
        assert recovered_session.change_tracker.change_count == 1
        assert recovered_session.task_id == "TASK-INT-001"

    def test_version_evolution_workflow(self, temp_workspace, sample_plan):
        """Test plan evolution through multiple versions."""
        version_manager = VersionManager(
            task_id="TASK-INT-001",
            base_dir=temp_workspace["versions"]
        )

        # Version 1: Initial plan
        v1 = version_manager.create_version(
            plan=sample_plan,
            change_reason="Initial implementation plan"
        )

        assert v1.version_number == 1

        # Version 2: Add error handling
        tracker = ChangeTracker()
        tracker.record_file_added("src/error_handler.py", "Error handling")

        applier = ModificationApplier(sample_plan, tracker)
        plan_v2 = applier.apply()

        v2 = version_manager.create_version(
            plan=plan_v2,
            change_reason="Added error handling"
        )

        assert v2.version_number == 2
        assert v2.previous_version == 1

        # Version 3: Add logging
        tracker2 = ChangeTracker()
        tracker2.record_file_added("src/logger.py", "Logging")
        tracker2.record_dependency_added("loguru", "Logging library")

        applier2 = ModificationApplier(plan_v2, tracker2)
        plan_v3 = applier2.apply()

        v3 = version_manager.create_version(
            plan=plan_v3,
            change_reason="Added logging"
        )

        assert v3.version_number == 3
        assert v3.previous_version == 2

        # Verify version history
        history = version_manager.get_version_history()

        assert len(history) == 3
        assert history[0].change_reason == "Initial implementation plan"
        assert history[1].change_reason == "Added error handling"
        assert history[2].change_reason == "Added logging"

        # Compare versions
        diff = version_manager.compare_versions(1, 3)

        assert "src/error_handler.py" in diff["files_added"]
        assert "src/logger.py" in diff["files_added"]
        assert "loguru" in diff["dependencies_added"]

    def test_review_mode_change_scenario(self, temp_workspace, sample_plan):
        """Test scenario where modifications change review mode."""
        # Original plan has QUICK_OPTIONAL mode (score 5)
        assert sample_plan.complexity_score.review_mode == ReviewMode.QUICK_OPTIONAL

        # Make significant modifications that increase complexity
        tracker = ChangeTracker()

        # Add many files (increases file complexity)
        for i in range(10):
            tracker.record_file_added(f"src/module_{i}.py", f"Module {i}")

        # Add security-related changes (triggers force review)
        tracker.record_file_added("src/auth.py", "Authentication")
        tracker.record_file_added("src/crypto.py", "Encryption")

        # Apply changes
        applier = ModificationApplier(sample_plan, tracker)
        modified_plan = applier.apply()

        # Verify changes applied
        assert len(modified_plan.files_to_create) > len(sample_plan.files_to_create)
        assert "src/auth.py" in modified_plan.files_to_create

        # In real workflow, complexity would be recalculated here
        # This would potentially change review mode to FULL_REQUIRED

    def test_concurrent_sessions_isolation(self, temp_workspace, sample_plan):
        """Test that concurrent sessions are isolated."""
        # Create two sessions for different tasks
        session1 = ModificationSession(
            plan=sample_plan,
            task_id="TASK-001",
            user_name="user1"
        )

        session2 = ModificationSession(
            plan=sample_plan,
            task_id="TASK-002",
            user_name="user2"
        )

        session1.start()
        session2.start()

        # Make different changes in each session
        session1.change_tracker.record_file_added("src/task1_file.py")
        session2.change_tracker.record_file_added("src/task2_file.py")

        # Sessions should be independent
        assert session1.change_tracker.change_count == 1
        assert session2.change_tracker.change_count == 1

        # End both sessions
        session1.end()
        session2.end()

        # Save both sessions
        persistence1 = ModificationPersistence(
            task_id="TASK-001",
            base_dir=temp_workspace["modifications"]
        )
        persistence2 = ModificationPersistence(
            task_id="TASK-002",
            base_dir=temp_workspace["modifications"]
        )

        persistence1.save_session(session1)
        persistence2.save_session(session2)

        # Verify sessions saved to different directories
        assert persistence1.task_dir != persistence2.task_dir

    def test_empty_plan_modification(self, temp_workspace):
        """Test modifying an empty plan."""
        empty_plan = ImplementationPlan(
            task_id="TASK-EMPTY",
            raw_plan="Empty plan for testing"
        )

        session = ModificationSession(
            plan=empty_plan,
            task_id="TASK-EMPTY"
        )
        session.start()

        # Add first files
        session.change_tracker.record_file_added("src/first_file.py")
        session.change_tracker.record_dependency_added("requests")

        applier = ModificationApplier(empty_plan, session.change_tracker)
        modified_plan = applier.apply()

        assert len(modified_plan.files_to_create) == 1
        assert len(modified_plan.external_dependencies) == 1

        session.end()

    def test_corrupted_session_handling(self, temp_workspace, sample_plan):
        """Test handling of corrupted session data."""
        persistence = ModificationPersistence(
            task_id="TASK-INT-001",
            base_dir=temp_workspace["modifications"]
        )

        # Create valid session
        session = ModificationSession(
            plan=sample_plan,
            task_id="TASK-INT-001"
        )
        session.start()
        session.end()

        saved_path = persistence.save_session(session)

        # Corrupt the session file
        with open(saved_path, 'w') as f:
            f.write("{ invalid json }")

        # Try to load corrupted session
        session_id = session.metadata.session_id
        loaded_session = persistence.load_session(session_id)

        # Should return None for corrupted data
        assert loaded_session is None

    def test_cancel_session_with_unsaved_changes(
        self,
        temp_workspace,
        sample_plan,
        capsys
    ):
        """Test cancelling session with unsaved changes."""
        session = ModificationSession(
            plan=sample_plan,
            task_id="TASK-INT-001"
        )
        session.start()

        # Make changes
        session.change_tracker.record_file_added("src/file.py")
        session.change_tracker.record_dependency_added("pytest")

        assert session.has_unsaved_changes()

        # Cancel session
        session.cancel("User cancelled")

        assert session.is_cancelled
        assert not session.is_completed

        captured = capsys.readouterr()
        assert "not saved" in captured.out.lower()

    def test_large_plan_modification(self, temp_workspace):
        """Test modifying plan with many files."""
        # Create plan with many files
        large_plan = ImplementationPlan(
            task_id="TASK-LARGE",
            files_to_create=[f"src/module_{i}.py" for i in range(100)],
            external_dependencies=[f"lib_{i}" for i in range(50)],
            estimated_loc=10000,
            raw_plan="Large implementation plan"
        )

        session = ModificationSession(
            plan=large_plan,
            task_id="TASK-LARGE"
        )
        session.start()

        # Add more files
        for i in range(100, 150):
            session.change_tracker.record_file_added(f"src/module_{i}.py")

        # Remove some files
        for i in range(10):
            session.change_tracker.record_file_removed(f"src/module_{i}.py")

        applier = ModificationApplier(large_plan, session.change_tracker)
        modified_plan = applier.apply()

        # Verify changes: 100 original - 10 removed + 50 added = 140 files
        assert len(modified_plan.files_to_create) == 140

        session.end()

    def test_ctrl_c_during_modification(self, temp_workspace, sample_plan):
        """Test Ctrl+C handling during modification session."""
        session = ModificationSession(
            plan=sample_plan,
            task_id="TASK-INT-001"
        )
        session.start()

        # Simulate Ctrl+C
        try:
            raise KeyboardInterrupt("Simulated Ctrl+C")
        except KeyboardInterrupt:
            # Graceful cancellation
            session.cancel("Interrupted by user")

        assert session.is_cancelled

        # Session should be saveable for recovery
        persistence = ModificationPersistence(
            task_id="TASK-INT-001",
            base_dir=temp_workspace["modifications"]
        )
        saved_path = persistence.save_session(session)

        assert saved_path.exists()


class TestValidationWorkflows:
    """Test validation scenarios in modification workflows."""

    def test_apply_changes_with_validation_errors(self, sample_plan):
        """Test applying changes with validation errors."""
        tracker = ChangeTracker()

        # Create conflicting changes
        tracker.record_file_added("src/conflict.py")
        tracker.record_file_removed("src/conflict.py")

        applier = ModificationApplier(sample_plan, tracker)

        # Validation should detect errors
        errors = applier.validate_changes()

        assert len(errors) > 0
        assert any("conflict" in err.lower() for err in errors)

    def test_remove_nonexistent_file_validation(self, sample_plan):
        """Test validation catches removing non-existent file."""
        tracker = ChangeTracker()
        tracker.record_file_removed("src/nonexistent.py")

        applier = ModificationApplier(sample_plan, tracker)
        errors = applier.validate_changes()

        assert len(errors) > 0
        assert any("not in plan" in err.lower() for err in errors)

    def test_remove_nonexistent_dependency_validation(self, sample_plan):
        """Test validation catches removing non-existent dependency."""
        tracker = ChangeTracker()
        tracker.record_dependency_removed("nonexistent_lib")

        applier = ModificationApplier(sample_plan, tracker)
        errors = applier.validate_changes()

        assert len(errors) > 0


class TestPersistenceRecovery:
    """Test persistence and recovery scenarios."""

    def test_session_persistence_across_restarts(
        self,
        temp_workspace,
        sample_plan
    ):
        """Test sessions persist across application restarts."""
        # First "application run"
        persistence1 = ModificationPersistence(
            task_id="TASK-INT-001",
            base_dir=temp_workspace["modifications"]
        )

        session = ModificationSession(
            plan=sample_plan,
            task_id="TASK-INT-001"
        )
        session.start()
        session.change_tracker.record_file_added("file.py")
        session.end()

        session_id = session.metadata.session_id
        persistence1.save_session(session)

        # Simulate application restart - new persistence instance
        persistence2 = ModificationPersistence(
            task_id="TASK-INT-001",
            base_dir=temp_workspace["modifications"]
        )

        # Load session from disk
        recovered_session = persistence2.load_session(session_id)

        assert recovered_session is not None
        assert recovered_session.task_id == "TASK-INT-001"
        assert recovered_session.change_tracker.change_count == 1

    def test_version_persistence_across_restarts(
        self,
        temp_workspace,
        sample_plan
    ):
        """Test versions persist across application restarts."""
        # First "application run"
        manager1 = VersionManager(
            task_id="TASK-INT-001",
            base_dir=temp_workspace["versions"]
        )

        manager1.create_version(sample_plan, "v1")
        manager1.create_version(sample_plan, "v2")

        # Simulate application restart - new manager instance
        manager2 = VersionManager(
            task_id="TASK-INT-001",
            base_dir=temp_workspace["versions"]
        )

        # Verify versions loaded from disk
        assert manager2.get_version_count() == 2
        assert manager2.get_version(1) is not None
        assert manager2.get_version(2) is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
