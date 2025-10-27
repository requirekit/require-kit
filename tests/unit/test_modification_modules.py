"""
Unit tests for modification modules:
  - modification_session.py
  - modification_applier.py
  - modification_persistence.py
  - version_manager.py

Tests cover:
    - Session lifecycle management
    - Change application to plans
    - Session persistence and recovery
    - Plan versioning with Memento pattern
    - Edge cases and error handling
"""

import pytest
import json
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "installer/global/commands"))

from lib.complexity_models import ImplementationPlan, ComplexityScore, ReviewMode, FactorScore
from lib.change_tracker import ChangeTracker, ChangeType
from lib.modification_session import (
    SessionState,
    SessionMetadata,
    ModificationSession,
)
from lib.modification_applier import ModificationApplier
from lib.modification_persistence import ModificationPersistence
from lib.version_manager import (
    PlanVersion,
    VersionManager,
)


# Test Fixtures
@pytest.fixture
def mock_implementation_plan():
    """Create mock ImplementationPlan for testing."""
    return ImplementationPlan(
        task_id="TASK-001",
        files_to_create=["src/file1.py", "src/file2.py"],
        patterns_used=["Strategy"],
        external_dependencies=["requests"],
        estimated_loc=200,
        risk_indicators=["database"],
        raw_plan="Test plan",
        test_summary="Unit tests",
        phases=["Phase 1", "Phase 2"]
    )


@pytest.fixture
def temp_task_dir(tmp_path):
    """Create temporary task directory."""
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    return task_dir


# ==================== modification_session.py Tests ====================

class TestSessionState:
    """Test suite for SessionState enum."""

    def test_all_states_defined(self):
        """Test all session states are defined."""
        expected_states = ["IDLE", "ACTIVE", "COMPLETED", "CANCELLED", "ERROR"]

        for state_name in expected_states:
            assert hasattr(SessionState, state_name)

    def test_state_values(self):
        """Test session state enum values."""
        assert SessionState.IDLE.value == "idle"
        assert SessionState.ACTIVE.value == "active"
        assert SessionState.COMPLETED.value == "completed"
        assert SessionState.CANCELLED.value == "cancelled"
        assert SessionState.ERROR.value == "error"


class TestSessionMetadata:
    """Test suite for SessionMetadata dataclass."""

    def test_create_metadata(self):
        """Test creating session metadata."""
        start_time = datetime.utcnow()
        metadata = SessionMetadata(
            task_id="TASK-001",
            session_id="session-001",
            start_time=start_time,
            end_time=None,
            state=SessionState.ACTIVE,
            user_name="test_user",
            change_count=5
        )

        assert metadata.task_id == "TASK-001"
        assert metadata.session_id == "session-001"
        assert metadata.start_time == start_time
        assert metadata.state == SessionState.ACTIVE
        assert metadata.change_count == 5

    def test_to_dict_serialization(self):
        """Test metadata to dictionary serialization."""
        start_time = datetime(2025, 10, 9, 10, 0, 0)
        end_time = datetime(2025, 10, 9, 11, 0, 0)

        metadata = SessionMetadata(
            task_id="TASK-001",
            session_id="session-001",
            start_time=start_time,
            end_time=end_time,
            state=SessionState.COMPLETED,
            change_count=10
        )

        metadata_dict = metadata.to_dict()

        assert metadata_dict["task_id"] == "TASK-001"
        assert metadata_dict["session_id"] == "session-001"
        assert metadata_dict["state"] == "completed"
        assert metadata_dict["change_count"] == 10


class TestModificationSession:
    """Test suite for ModificationSession class."""

    def test_initialization(self, mock_implementation_plan):
        """Test session initialization."""
        session = ModificationSession(
            plan=mock_implementation_plan,
            task_id="TASK-001",
            user_name="test_user"
        )

        assert session.task_id == "TASK-001"
        assert session.user_name == "test_user"
        assert session.state == SessionState.IDLE
        assert session.is_active is False
        assert session.change_tracker.is_empty is True

    def test_start_session(self, mock_implementation_plan, capsys):
        """Test starting a session."""
        session = ModificationSession(
            plan=mock_implementation_plan,
            task_id="TASK-001"
        )

        session.start()

        assert session.state == SessionState.ACTIVE
        assert session.is_active is True

        captured = capsys.readouterr()
        assert "Starting modification session" in captured.out

    def test_start_session_twice_raises_error(self, mock_implementation_plan):
        """Test starting session twice raises RuntimeError."""
        session = ModificationSession(
            plan=mock_implementation_plan,
            task_id="TASK-001"
        )

        session.start()

        with pytest.raises(RuntimeError, match="Cannot start session"):
            session.start()

    def test_end_session(self, mock_implementation_plan, capsys):
        """Test ending a session."""
        session = ModificationSession(
            plan=mock_implementation_plan,
            task_id="TASK-001"
        )

        session.start()
        session.end(save=True)

        assert session.state == SessionState.COMPLETED
        assert session.is_completed is True

        captured = capsys.readouterr()
        assert "Ending modification session" in captured.out
        assert "Changes will be saved" in captured.out

    def test_end_session_without_save(self, mock_implementation_plan):
        """Test ending session without saving."""
        session = ModificationSession(
            plan=mock_implementation_plan,
            task_id="TASK-001"
        )

        session.start()
        session.end(save=False)

        assert session.state == SessionState.COMPLETED

    def test_end_session_when_not_active_raises_error(self, mock_implementation_plan):
        """Test ending non-active session raises RuntimeError."""
        session = ModificationSession(
            plan=mock_implementation_plan,
            task_id="TASK-001"
        )

        with pytest.raises(RuntimeError, match="Cannot end session"):
            session.end()

    def test_cancel_session(self, mock_implementation_plan, capsys):
        """Test cancelling a session."""
        session = ModificationSession(
            plan=mock_implementation_plan,
            task_id="TASK-001"
        )

        session.start()
        session.cancel(reason="User requested")

        assert session.state == SessionState.CANCELLED
        assert session.is_cancelled is True

        captured = capsys.readouterr()
        assert "Cancelling modification session" in captured.out
        assert "User requested" in captured.out

    def test_error_session(self, mock_implementation_plan, capsys):
        """Test marking session as errored."""
        session = ModificationSession(
            plan=mock_implementation_plan,
            task_id="TASK-001"
        )

        session.start()
        session.error("Test error message")

        assert session.state == SessionState.ERROR

        captured = capsys.readouterr()
        assert "Session error" in captured.out
        assert "Test error message" in captured.out

    def test_has_unsaved_changes(self, mock_implementation_plan):
        """Test has_unsaved_changes detection."""
        session = ModificationSession(
            plan=mock_implementation_plan,
            task_id="TASK-001"
        )

        session.start()

        # No changes yet
        assert session.has_unsaved_changes() is False

        # Add change
        session.change_tracker.record_file_added("new_file.py")

        # Should have unsaved changes
        assert session.has_unsaved_changes() is True

        # Complete session
        session.end()

        # No longer has unsaved changes
        assert session.has_unsaved_changes() is False

    def test_get_duration_seconds(self, mock_implementation_plan):
        """Test session duration calculation."""
        session = ModificationSession(
            plan=mock_implementation_plan,
            task_id="TASK-001"
        )

        # Not started
        assert session.get_duration_seconds() == 0.0

        session.start()

        # Active session
        duration = session.get_duration_seconds()
        assert duration >= 0.0

        session.end()

        # Completed session
        final_duration = session.get_duration_seconds()
        assert final_duration >= duration

    def test_session_metadata_property(self, mock_implementation_plan):
        """Test metadata property."""
        session = ModificationSession(
            plan=mock_implementation_plan,
            task_id="TASK-001",
            user_name="test_user"
        )

        session.start()
        session.change_tracker.record_file_added("file.py")

        metadata = session.metadata

        assert metadata.task_id == "TASK-001"
        assert metadata.user_name == "test_user"
        assert metadata.state == SessionState.ACTIVE
        assert metadata.change_count == 1


# ==================== modification_applier.py Tests ====================

class TestModificationApplier:
    """Test suite for ModificationApplier class."""

    def test_initialization(self, mock_implementation_plan):
        """Test applier initialization."""
        tracker = ChangeTracker()
        applier = ModificationApplier(mock_implementation_plan, tracker)

        assert applier.original_plan == mock_implementation_plan
        assert applier.change_tracker == tracker

    def test_apply_no_changes(self, mock_implementation_plan):
        """Test applying no changes returns identical plan."""
        tracker = ChangeTracker()
        applier = ModificationApplier(mock_implementation_plan, tracker)

        modified_plan = applier.apply()

        # Should be different object but same content
        assert modified_plan is not mock_implementation_plan
        assert modified_plan.task_id == mock_implementation_plan.task_id
        assert modified_plan.files_to_create == mock_implementation_plan.files_to_create

    def test_apply_file_added(self, mock_implementation_plan):
        """Test applying file addition change."""
        tracker = ChangeTracker()
        tracker.record_file_added("src/new_file.py", "New module")

        applier = ModificationApplier(mock_implementation_plan, tracker)
        modified_plan = applier.apply()

        assert "src/new_file.py" in modified_plan.files_to_create
        assert len(modified_plan.files_to_create) == len(mock_implementation_plan.files_to_create) + 1

    def test_apply_file_removed(self, mock_implementation_plan):
        """Test applying file removal change."""
        tracker = ChangeTracker()
        tracker.record_file_removed("src/file1.py", "No longer needed")

        applier = ModificationApplier(mock_implementation_plan, tracker)
        modified_plan = applier.apply()

        assert "src/file1.py" not in modified_plan.files_to_create
        assert len(modified_plan.files_to_create) == len(mock_implementation_plan.files_to_create) - 1

    def test_apply_dependency_added(self, mock_implementation_plan):
        """Test applying dependency addition change."""
        tracker = ChangeTracker()
        tracker.record_dependency_added("pytest", "Testing framework")

        applier = ModificationApplier(mock_implementation_plan, tracker)
        modified_plan = applier.apply()

        assert "pytest" in modified_plan.external_dependencies
        assert len(modified_plan.external_dependencies) == len(mock_implementation_plan.external_dependencies) + 1

    def test_apply_dependency_removed(self, mock_implementation_plan):
        """Test applying dependency removal change."""
        tracker = ChangeTracker()
        tracker.record_dependency_removed("requests", "Using alternative")

        applier = ModificationApplier(mock_implementation_plan, tracker)
        modified_plan = applier.apply()

        assert "requests" not in modified_plan.external_dependencies
        assert len(modified_plan.external_dependencies) == 0

    def test_apply_phase_added(self, mock_implementation_plan):
        """Test applying phase addition change."""
        tracker = ChangeTracker()
        tracker.record_phase_added("Phase 3: Deployment", position=2)

        applier = ModificationApplier(mock_implementation_plan, tracker)
        modified_plan = applier.apply()

        assert "Phase 3: Deployment" in modified_plan.phases
        assert len(modified_plan.phases) == 3

    def test_apply_phase_removed(self, mock_implementation_plan):
        """Test applying phase removal change."""
        tracker = ChangeTracker()
        tracker.record_phase_removed("Phase 1", position=0)

        applier = ModificationApplier(mock_implementation_plan, tracker)
        modified_plan = applier.apply()

        assert "Phase 1" not in modified_plan.phases
        assert len(modified_plan.phases) == 1

    def test_apply_metadata_updated(self, mock_implementation_plan):
        """Test applying metadata update change."""
        tracker = ChangeTracker()
        tracker.record_metadata_updated("estimated_loc", 200, 300)

        applier = ModificationApplier(mock_implementation_plan, tracker)
        modified_plan = applier.apply()

        assert modified_plan.estimated_loc == 300

    def test_apply_multiple_changes_in_order(self, mock_implementation_plan):
        """Test applying multiple changes in chronological order."""
        tracker = ChangeTracker()
        tracker.record_file_added("src/file3.py")
        tracker.record_file_removed("src/file1.py")
        tracker.record_dependency_added("pytest")

        applier = ModificationApplier(mock_implementation_plan, tracker)
        modified_plan = applier.apply()

        assert "src/file3.py" in modified_plan.files_to_create
        assert "src/file1.py" not in modified_plan.files_to_create
        assert "pytest" in modified_plan.external_dependencies

    def test_validate_changes_no_errors(self, mock_implementation_plan):
        """Test validation with valid changes."""
        tracker = ChangeTracker()
        tracker.record_file_added("src/new.py")

        applier = ModificationApplier(mock_implementation_plan, tracker)
        errors = applier.validate_changes()

        assert len(errors) == 0

    def test_validate_changes_conflicting_file_operations(self, mock_implementation_plan):
        """Test validation detects conflicting file operations."""
        tracker = ChangeTracker()
        # Add and remove same file - conflict
        tracker.record_file_added("src/conflict.py")
        tracker.record_file_removed("src/conflict.py")

        applier = ModificationApplier(mock_implementation_plan, tracker)
        errors = applier.validate_changes()

        assert len(errors) > 0
        assert any("conflict" in error.lower() for error in errors)

    def test_validate_changes_remove_nonexistent_file(self, mock_implementation_plan):
        """Test validation detects removing non-existent file."""
        tracker = ChangeTracker()
        tracker.record_file_removed("src/nonexistent.py")

        applier = ModificationApplier(mock_implementation_plan, tracker)
        errors = applier.validate_changes()

        assert len(errors) > 0
        assert any("nonexistent" in error.lower() for error in errors)

    def test_get_change_summary(self, mock_implementation_plan):
        """Test getting change summary."""
        tracker = ChangeTracker()
        tracker.record_file_added("file.py")

        applier = ModificationApplier(mock_implementation_plan, tracker)
        summary = applier.get_change_summary()

        assert "1 changes" in summary


# ==================== modification_persistence.py Tests ====================

class TestModificationPersistence:
    """Test suite for ModificationPersistence class."""

    def test_initialization(self, temp_task_dir):
        """Test persistence initialization."""
        persistence = ModificationPersistence(
            task_id="TASK-001",
            base_dir=temp_task_dir
        )

        assert persistence.task_id == "TASK-001"
        assert persistence.task_dir.exists()

    def test_save_session(self, temp_task_dir, mock_implementation_plan):
        """Test saving session to disk."""
        persistence = ModificationPersistence(
            task_id="TASK-001",
            base_dir=temp_task_dir
        )

        session = ModificationSession(
            plan=mock_implementation_plan,
            task_id="TASK-001"
        )
        session.start()
        session.change_tracker.record_file_added("file.py")
        session.end()

        saved_path = persistence.save_session(session)

        assert saved_path.exists()
        assert saved_path.suffix == ".json"

    def test_load_session(self, temp_task_dir, mock_implementation_plan):
        """Test loading session from disk."""
        persistence = ModificationPersistence(
            task_id="TASK-001",
            base_dir=temp_task_dir
        )

        # Create and save session
        original_session = ModificationSession(
            plan=mock_implementation_plan,
            task_id="TASK-001",
            user_name="test_user"
        )
        original_session.start()
        original_session.change_tracker.record_file_added("file.py")
        original_session.end()

        persistence.save_session(original_session)

        # Load session
        session_id = original_session.metadata.session_id
        loaded_session = persistence.load_session(session_id)

        assert loaded_session is not None
        assert loaded_session.task_id == "TASK-001"
        assert loaded_session.change_tracker.change_count == 1

    def test_load_nonexistent_session(self, temp_task_dir):
        """Test loading non-existent session returns None."""
        persistence = ModificationPersistence(
            task_id="TASK-001",
            base_dir=temp_task_dir
        )

        loaded_session = persistence.load_session("nonexistent-session")

        assert loaded_session is None

    def test_list_sessions(self, temp_task_dir, mock_implementation_plan):
        """Test listing all sessions."""
        persistence = ModificationPersistence(
            task_id="TASK-001",
            base_dir=temp_task_dir
        )

        # Create multiple sessions
        for i in range(3):
            session = ModificationSession(
                plan=mock_implementation_plan,
                task_id="TASK-001"
            )
            session.start()
            session.end()
            persistence.save_session(session)

        sessions = persistence.list_sessions()

        assert len(sessions) == 3

    def test_get_session_metadata(self, temp_task_dir, mock_implementation_plan):
        """Test getting session metadata without loading full session."""
        persistence = ModificationPersistence(
            task_id="TASK-001",
            base_dir=temp_task_dir
        )

        session = ModificationSession(
            plan=mock_implementation_plan,
            task_id="TASK-001"
        )
        session.start()
        session.end()

        persistence.save_session(session)

        session_id = session.metadata.session_id
        metadata = persistence.get_session_metadata(session_id)

        assert metadata is not None
        assert metadata["task_id"] == "TASK-001"

    def test_delete_session(self, temp_task_dir, mock_implementation_plan):
        """Test deleting session."""
        persistence = ModificationPersistence(
            task_id="TASK-001",
            base_dir=temp_task_dir
        )

        session = ModificationSession(
            plan=mock_implementation_plan,
            task_id="TASK-001"
        )
        session.start()
        session.end()

        saved_path = persistence.save_session(session)
        session_id = session.metadata.session_id

        # Verify file exists
        assert saved_path.exists()

        # Delete session
        result = persistence.delete_session(session_id)

        assert result is True
        assert not saved_path.exists()

    def test_delete_nonexistent_session(self, temp_task_dir):
        """Test deleting non-existent session returns False."""
        persistence = ModificationPersistence(
            task_id="TASK-001",
            base_dir=temp_task_dir
        )

        result = persistence.delete_session("nonexistent-session")

        assert result is False

    def test_get_latest_session_id(self, temp_task_dir, mock_implementation_plan):
        """Test getting latest session ID."""
        persistence = ModificationPersistence(
            task_id="TASK-001",
            base_dir=temp_task_dir
        )

        # Create sessions with slight delays
        session_ids = []
        for i in range(3):
            session = ModificationSession(
                plan=mock_implementation_plan,
                task_id="TASK-001"
            )
            session.start()
            session.end()
            persistence.save_session(session)
            session_ids.append(session.metadata.session_id)

        latest_id = persistence.get_latest_session_id()

        # Latest should be the last one created
        assert latest_id == session_ids[-1]


# ==================== version_manager.py Tests ====================

class TestPlanVersion:
    """Test suite for PlanVersion dataclass."""

    def test_create_version(self, mock_implementation_plan):
        """Test creating plan version."""
        timestamp = datetime.utcnow()
        version = PlanVersion(
            version_number=1,
            plan=mock_implementation_plan,
            created_at=timestamp,
            created_by="test_user",
            change_reason="Initial version",
            previous_version=None,
            metadata={"test": "data"}
        )

        assert version.version_number == 1
        assert version.plan == mock_implementation_plan
        assert version.created_by == "test_user"
        assert version.change_reason == "Initial version"
        assert version.previous_version is None

    def test_to_dict_serialization(self, mock_implementation_plan):
        """Test version to dictionary serialization."""
        timestamp = datetime(2025, 10, 9, 10, 0, 0)
        version = PlanVersion(
            version_number=1,
            plan=mock_implementation_plan,
            created_at=timestamp,
            created_by="user",
            change_reason="Test",
            metadata={"key": "value"}
        )

        version_dict = version.to_dict()

        assert version_dict["version_number"] == 1
        assert version_dict["created_by"] == "user"
        assert version_dict["change_reason"] == "Test"
        assert "plan" in version_dict
        assert version_dict["metadata"]["key"] == "value"

    def test_from_dict_deserialization(self, mock_implementation_plan):
        """Test version from dictionary deserialization."""
        version_dict = {
            "version_number": 2,
            "plan": {
                "task_id": "TASK-001",
                "files_to_create": ["file.py"],
                "patterns_used": [],
                "external_dependencies": [],
                "estimated_loc": None,
                "risk_indicators": [],
                "raw_plan": "Test plan"
            },
            "created_at": "2025-10-09T10:00:00Z",
            "created_by": "user",
            "change_reason": "Test",
            "previous_version": 1,
            "metadata": {}
        }

        version = PlanVersion.from_dict(version_dict)

        assert version.version_number == 2
        assert version.plan.task_id == "TASK-001"
        assert version.previous_version == 1

    def test_get_summary(self, mock_implementation_plan):
        """Test getting version summary."""
        version = PlanVersion(
            version_number=3,
            plan=mock_implementation_plan,
            created_at=datetime.utcnow(),
            created_by="user",
            change_reason="Added new feature",
            previous_version=2
        )

        summary = version.get_summary()

        assert "Version 3" in summary
        assert "Added new feature" in summary
        assert "Previous: v2" in summary


class TestVersionManager:
    """Test suite for VersionManager class."""

    def test_initialization(self, temp_task_dir):
        """Test version manager initialization."""
        manager = VersionManager(
            task_id="TASK-001",
            base_dir=temp_task_dir
        )

        assert manager.task_id == "TASK-001"
        assert manager.task_dir.exists()

    def test_create_version(self, temp_task_dir, mock_implementation_plan):
        """Test creating first version."""
        manager = VersionManager(
            task_id="TASK-001",
            base_dir=temp_task_dir
        )

        version = manager.create_version(
            plan=mock_implementation_plan,
            change_reason="Initial version",
            created_by="user"
        )

        assert version.version_number == 1
        assert version.plan == mock_implementation_plan
        assert version.change_reason == "Initial version"
        assert version.previous_version is None

    def test_create_multiple_versions(self, temp_task_dir, mock_implementation_plan):
        """Test creating multiple sequential versions."""
        manager = VersionManager(
            task_id="TASK-001",
            base_dir=temp_task_dir
        )

        v1 = manager.create_version(
            plan=mock_implementation_plan,
            change_reason="v1"
        )

        v2 = manager.create_version(
            plan=mock_implementation_plan,
            change_reason="v2"
        )

        v3 = manager.create_version(
            plan=mock_implementation_plan,
            change_reason="v3"
        )

        assert v1.version_number == 1
        assert v2.version_number == 2
        assert v3.version_number == 3
        assert v2.previous_version == 1
        assert v3.previous_version == 2

    def test_get_version(self, temp_task_dir, mock_implementation_plan):
        """Test retrieving specific version."""
        manager = VersionManager(
            task_id="TASK-001",
            base_dir=temp_task_dir
        )

        manager.create_version(
            plan=mock_implementation_plan,
            change_reason="v1"
        )

        retrieved = manager.get_version(1)

        assert retrieved is not None
        assert retrieved.version_number == 1

    def test_get_nonexistent_version(self, temp_task_dir):
        """Test retrieving non-existent version returns None."""
        manager = VersionManager(
            task_id="TASK-001",
            base_dir=temp_task_dir
        )

        retrieved = manager.get_version(99)

        assert retrieved is None

    def test_get_latest_version(self, temp_task_dir, mock_implementation_plan):
        """Test getting latest version."""
        manager = VersionManager(
            task_id="TASK-001",
            base_dir=temp_task_dir
        )

        manager.create_version(mock_implementation_plan, "v1")
        manager.create_version(mock_implementation_plan, "v2")
        v3 = manager.create_version(mock_implementation_plan, "v3")

        latest = manager.get_latest_version()

        assert latest.version_number == 3
        assert latest.change_reason == "v3"

    def test_get_version_history(self, temp_task_dir, mock_implementation_plan):
        """Test getting complete version history."""
        manager = VersionManager(
            task_id="TASK-001",
            base_dir=temp_task_dir
        )

        manager.create_version(mock_implementation_plan, "v1")
        manager.create_version(mock_implementation_plan, "v2")
        manager.create_version(mock_implementation_plan, "v3")

        history = manager.get_version_history()

        assert len(history) == 3
        assert history[0].version_number == 1
        assert history[1].version_number == 2
        assert history[2].version_number == 3

    def test_get_version_count(self, temp_task_dir, mock_implementation_plan):
        """Test getting version count."""
        manager = VersionManager(
            task_id="TASK-001",
            base_dir=temp_task_dir
        )

        assert manager.get_version_count() == 0

        manager.create_version(mock_implementation_plan, "v1")
        assert manager.get_version_count() == 1

        manager.create_version(mock_implementation_plan, "v2")
        assert manager.get_version_count() == 2

    def test_compare_versions(self, temp_task_dir):
        """Test comparing two versions."""
        manager = VersionManager(
            task_id="TASK-001",
            base_dir=temp_task_dir
        )

        # Create v1 with initial files
        plan_v1 = ImplementationPlan(
            task_id="TASK-001",
            files_to_create=["file1.py", "file2.py"],
            external_dependencies=["requests"],
            estimated_loc=100,
            raw_plan="v1"
        )

        # Create v2 with modifications
        plan_v2 = ImplementationPlan(
            task_id="TASK-001",
            files_to_create=["file1.py", "file3.py"],  # file2 removed, file3 added
            external_dependencies=["requests", "pytest"],  # pytest added
            estimated_loc=150,
            raw_plan="v2"
        )

        manager.create_version(plan_v1, "v1")
        manager.create_version(plan_v2, "v2")

        diff = manager.compare_versions(1, 2)

        assert "file3.py" in diff["files_added"]
        assert "file2.py" in diff["files_removed"]
        assert "file1.py" in diff["files_unchanged"]
        assert "pytest" in diff["dependencies_added"]
        assert diff["loc_change"] == 50

    def test_delete_version(self, temp_task_dir, mock_implementation_plan):
        """Test deleting specific version."""
        manager = VersionManager(
            task_id="TASK-001",
            base_dir=temp_task_dir
        )

        manager.create_version(mock_implementation_plan, "v1")
        manager.create_version(mock_implementation_plan, "v2")

        # Delete v2
        result = manager.delete_version(2)

        assert result is True
        assert manager.get_version(2) is None
        assert manager.get_version_count() == 1

    def test_cannot_delete_v1_with_other_versions(
        self,
        temp_task_dir,
        mock_implementation_plan
    ):
        """Test cannot delete version 1 if other versions exist."""
        manager = VersionManager(
            task_id="TASK-001",
            base_dir=temp_task_dir
        )

        manager.create_version(mock_implementation_plan, "v1")
        manager.create_version(mock_implementation_plan, "v2")

        with pytest.raises(ValueError, match="Cannot delete version 1"):
            manager.delete_version(1)

    def test_persistence_across_instances(
        self,
        temp_task_dir,
        mock_implementation_plan
    ):
        """Test versions persist across manager instances."""
        # Create version with first instance
        manager1 = VersionManager(
            task_id="TASK-001",
            base_dir=temp_task_dir
        )
        manager1.create_version(mock_implementation_plan, "v1")

        # Load with second instance
        manager2 = VersionManager(
            task_id="TASK-001",
            base_dir=temp_task_dir
        )

        assert manager2.get_version_count() == 1
        assert manager2.get_version(1) is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
