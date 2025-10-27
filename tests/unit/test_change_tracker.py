"""
Unit tests for change_tracker.py - Change tracking for plan modifications.

Tests cover:
    - Change recording (add/remove/modify operations)
    - Change serialization/deserialization
    - Change summary generation
    - Change type filtering
    - Edge cases and error handling
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "installer/global/commands"))

from lib.change_tracker import (
    ChangeType,
    Change,
    ChangeTracker,
)


class TestChangeType:
    """Test suite for ChangeType enum."""

    def test_all_change_types_defined(self):
        """Test all expected change types are defined."""
        expected_types = [
            "FILE_ADDED",
            "FILE_REMOVED",
            "FILE_MODIFIED",
            "DEPENDENCY_ADDED",
            "DEPENDENCY_REMOVED",
            "PHASE_ADDED",
            "PHASE_REMOVED",
            "PHASE_REORDERED",
            "RISK_ADDED",
            "RISK_MODIFIED",
            "RISK_REMOVED",
            "METADATA_UPDATED",
        ]

        for type_name in expected_types:
            assert hasattr(ChangeType, type_name)

    def test_change_type_values(self):
        """Test change type enum values."""
        assert ChangeType.FILE_ADDED.value == "file_added"
        assert ChangeType.FILE_REMOVED.value == "file_removed"
        assert ChangeType.DEPENDENCY_ADDED.value == "dependency_added"


class TestChange:
    """Test suite for Change dataclass."""

    def test_create_file_added_change(self):
        """Test creating file addition change."""
        timestamp = datetime.utcnow()
        change = Change(
            change_type=ChangeType.FILE_ADDED,
            timestamp=timestamp,
            target="src/new_file.py",
            old_value=None,
            new_value="Purpose: API handler",
            metadata={"estimated_loc": 150}
        )

        assert change.change_type == ChangeType.FILE_ADDED
        assert change.target == "src/new_file.py"
        assert change.old_value is None
        assert change.new_value == "Purpose: API handler"
        assert change.metadata["estimated_loc"] == 150

    def test_create_file_removed_change(self):
        """Test creating file removal change."""
        timestamp = datetime.utcnow()
        change = Change(
            change_type=ChangeType.FILE_REMOVED,
            timestamp=timestamp,
            target="src/old_file.py",
            old_value="src/old_file.py",
            new_value=None,
            metadata={"reason": "No longer needed"}
        )

        assert change.change_type == ChangeType.FILE_REMOVED
        assert change.old_value == "src/old_file.py"
        assert change.new_value is None

    def test_to_dict_serialization(self):
        """Test Change to dictionary serialization."""
        timestamp = datetime(2025, 10, 9, 10, 30, 0)
        change = Change(
            change_type=ChangeType.FILE_ADDED,
            timestamp=timestamp,
            target="src/test.py",
            old_value=None,
            new_value="Test file",
            metadata={"loc": 100}
        )

        change_dict = change.to_dict()

        assert change_dict["change_type"] == "file_added"
        assert change_dict["timestamp"].startswith("2025-10-09")
        assert change_dict["target"] == "src/test.py"
        assert change_dict["old_value"] is None
        assert change_dict["new_value"] == "Test file"
        assert change_dict["metadata"]["loc"] == 100

    def test_from_dict_deserialization(self):
        """Test Change from dictionary deserialization."""
        change_dict = {
            "change_type": "file_added",
            "timestamp": "2025-10-09T10:30:00Z",
            "target": "src/test.py",
            "old_value": None,
            "new_value": "Test file",
            "metadata": {"loc": 100}
        }

        change = Change.from_dict(change_dict)

        assert change.change_type == ChangeType.FILE_ADDED
        assert change.target == "src/test.py"
        assert change.old_value is None
        assert change.new_value == "Test file"
        assert change.metadata["loc"] == 100

    def test_round_trip_serialization(self):
        """Test round-trip serialization (to_dict -> from_dict)."""
        original = Change(
            change_type=ChangeType.DEPENDENCY_ADDED,
            timestamp=datetime.utcnow(),
            target="requests",
            old_value=None,
            new_value="requests",
            metadata={"version": "2.28.0"}
        )

        # Round-trip
        change_dict = original.to_dict()
        restored = Change.from_dict(change_dict)

        assert restored.change_type == original.change_type
        assert restored.target == original.target
        assert restored.old_value == original.old_value
        assert restored.new_value == original.new_value
        assert restored.metadata == original.metadata

    def test_describe_file_added(self):
        """Test describe() for file addition."""
        change = Change(
            change_type=ChangeType.FILE_ADDED,
            timestamp=datetime.utcnow(),
            target="src/new.py",
        )

        description = change.describe()
        assert "Added file: src/new.py" in description

    def test_describe_file_removed(self):
        """Test describe() for file removal."""
        change = Change(
            change_type=ChangeType.FILE_REMOVED,
            timestamp=datetime.utcnow(),
            target="src/old.py",
        )

        description = change.describe()
        assert "Removed file: src/old.py" in description

    def test_describe_dependency_added(self):
        """Test describe() for dependency addition."""
        change = Change(
            change_type=ChangeType.DEPENDENCY_ADDED,
            timestamp=datetime.utcnow(),
            target="pytest",
        )

        description = change.describe()
        assert "Added dependency: pytest" in description

    def test_describe_metadata_updated(self):
        """Test describe() for metadata update."""
        change = Change(
            change_type=ChangeType.METADATA_UPDATED,
            timestamp=datetime.utcnow(),
            target="estimated_loc",
            old_value=100,
            new_value=150
        )

        description = change.describe()
        assert "Updated estimated_loc: 100 -> 150" in description

    def test_change_immutability(self):
        """Test that Change is immutable (frozen dataclass)."""
        change = Change(
            change_type=ChangeType.FILE_ADDED,
            timestamp=datetime.utcnow(),
            target="test.py"
        )

        with pytest.raises(AttributeError):
            change.target = "modified.py"  # Should raise exception


class TestChangeTracker:
    """Test suite for ChangeTracker class."""

    def test_initialization(self):
        """Test ChangeTracker initialization."""
        tracker = ChangeTracker()

        assert tracker.change_count == 0
        assert tracker.is_empty is True
        assert len(tracker.changes) == 0

    def test_record_file_added(self):
        """Test recording file addition."""
        tracker = ChangeTracker()
        tracker.record_file_added(
            "src/new_file.py",
            purpose="API handler",
            estimated_loc=150
        )

        assert tracker.change_count == 1
        assert tracker.is_empty is False

        change = tracker.changes[0]
        assert change.change_type == ChangeType.FILE_ADDED
        assert change.target == "src/new_file.py"
        assert change.new_value == "API handler"
        assert change.metadata["purpose"] == "API handler"
        assert change.metadata["estimated_loc"] == 150

    def test_record_file_added_without_optional_params(self):
        """Test recording file addition without optional parameters."""
        tracker = ChangeTracker()
        tracker.record_file_added("src/file.py")

        assert tracker.change_count == 1
        change = tracker.changes[0]
        assert change.target == "src/file.py"
        assert change.metadata == {}

    def test_record_file_removed(self):
        """Test recording file removal."""
        tracker = ChangeTracker()
        tracker.record_file_removed(
            "src/old_file.py",
            reason="No longer needed"
        )

        assert tracker.change_count == 1

        change = tracker.changes[0]
        assert change.change_type == ChangeType.FILE_REMOVED
        assert change.target == "src/old_file.py"
        assert change.old_value == "src/old_file.py"
        assert change.new_value is None
        assert change.metadata["reason"] == "No longer needed"

    def test_record_file_modified(self):
        """Test recording file modification."""
        tracker = ChangeTracker()
        tracker.record_file_modified(
            "src/existing.py",
            old_purpose="Old purpose",
            new_purpose="New purpose"
        )

        assert tracker.change_count == 1

        change = tracker.changes[0]
        assert change.change_type == ChangeType.FILE_MODIFIED
        assert change.target == "src/existing.py"
        assert change.old_value == "Old purpose"
        assert change.new_value == "New purpose"

    def test_record_dependency_added(self):
        """Test recording dependency addition."""
        tracker = ChangeTracker()
        tracker.record_dependency_added(
            "requests",
            purpose="HTTP client"
        )

        assert tracker.change_count == 1

        change = tracker.changes[0]
        assert change.change_type == ChangeType.DEPENDENCY_ADDED
        assert change.target == "requests"
        assert change.new_value == "requests"
        assert change.metadata["purpose"] == "HTTP client"

    def test_record_dependency_removed(self):
        """Test recording dependency removal."""
        tracker = ChangeTracker()
        tracker.record_dependency_removed(
            "old-library",
            reason="Deprecated"
        )

        assert tracker.change_count == 1

        change = tracker.changes[0]
        assert change.change_type == ChangeType.DEPENDENCY_REMOVED
        assert change.target == "old-library"
        assert change.old_value == "old-library"
        assert change.metadata["reason"] == "Deprecated"

    def test_record_phase_added(self):
        """Test recording phase addition."""
        tracker = ChangeTracker()
        tracker.record_phase_added("New phase description", position=2)

        assert tracker.change_count == 1

        change = tracker.changes[0]
        assert change.change_type == ChangeType.PHASE_ADDED
        assert change.target == "New phase description"
        assert change.new_value == "New phase description"
        assert change.metadata["position"] == 2

    def test_record_phase_removed(self):
        """Test recording phase removal."""
        tracker = ChangeTracker()
        tracker.record_phase_removed("Old phase", position=1)

        assert tracker.change_count == 1

        change = tracker.changes[0]
        assert change.change_type == ChangeType.PHASE_REMOVED
        assert change.target == "Old phase"
        assert change.old_value == "Old phase"
        assert change.metadata["position"] == 1

    def test_record_metadata_updated(self):
        """Test recording metadata update."""
        tracker = ChangeTracker()
        tracker.record_metadata_updated(
            "estimated_loc",
            old_value=100,
            new_value=150
        )

        assert tracker.change_count == 1

        change = tracker.changes[0]
        assert change.change_type == ChangeType.METADATA_UPDATED
        assert change.target == "estimated_loc"
        assert change.old_value == 100
        assert change.new_value == 150

    def test_multiple_changes_chronological_order(self):
        """Test multiple changes are recorded in chronological order."""
        tracker = ChangeTracker()

        tracker.record_file_added("file1.py")
        tracker.record_file_added("file2.py")
        tracker.record_dependency_added("requests")

        assert tracker.change_count == 3

        # Verify chronological order by comparing timestamps
        timestamps = [c.timestamp for c in tracker.changes]
        assert timestamps == sorted(timestamps)

    def test_get_changes_by_type(self):
        """Test filtering changes by type."""
        tracker = ChangeTracker()

        tracker.record_file_added("file1.py")
        tracker.record_file_added("file2.py")
        tracker.record_dependency_added("requests")
        tracker.record_file_removed("old.py")

        # Get only file additions
        file_additions = tracker.get_changes_by_type(ChangeType.FILE_ADDED)

        assert len(file_additions) == 2
        assert all(c.change_type == ChangeType.FILE_ADDED for c in file_additions)
        assert file_additions[0].target == "file1.py"
        assert file_additions[1].target == "file2.py"

    def test_get_changes_by_type_empty(self):
        """Test filtering for non-existent change type."""
        tracker = ChangeTracker()
        tracker.record_file_added("file.py")

        # Get changes of type that doesn't exist
        removals = tracker.get_changes_by_type(ChangeType.FILE_REMOVED)

        assert len(removals) == 0

    def test_get_summary_empty_tracker(self):
        """Test get_summary with no changes."""
        tracker = ChangeTracker()
        summary = tracker.get_summary()

        assert "No changes recorded" in summary

    def test_get_summary_with_changes(self):
        """Test get_summary with multiple changes."""
        tracker = ChangeTracker()

        tracker.record_file_added("file1.py", "API handler")
        tracker.record_file_removed("old.py", "Deprecated")
        tracker.record_dependency_added("requests")

        summary = tracker.get_summary()

        assert "Change Summary (3 changes)" in summary
        assert "File Added" in summary
        assert "file1.py" in summary
        assert "File Removed" in summary
        assert "old.py" in summary
        assert "Dependency Added" in summary
        assert "requests" in summary

    def test_to_dict_serialization(self):
        """Test ChangeTracker to dictionary serialization."""
        tracker = ChangeTracker()
        tracker.record_file_added("file.py")
        tracker.record_dependency_added("requests")

        tracker_dict = tracker.to_dict()

        assert "session_start" in tracker_dict
        assert tracker_dict["change_count"] == 2
        assert len(tracker_dict["changes"]) == 2
        assert tracker_dict["changes"][0]["change_type"] == "file_added"
        assert tracker_dict["changes"][1]["change_type"] == "dependency_added"

    def test_from_dict_deserialization(self):
        """Test ChangeTracker from dictionary deserialization."""
        tracker_dict = {
            "session_start": "2025-10-09T10:00:00Z",
            "change_count": 2,
            "changes": [
                {
                    "change_type": "file_added",
                    "timestamp": "2025-10-09T10:01:00Z",
                    "target": "file.py",
                    "old_value": None,
                    "new_value": "Test file",
                    "metadata": {}
                },
                {
                    "change_type": "dependency_added",
                    "timestamp": "2025-10-09T10:02:00Z",
                    "target": "requests",
                    "old_value": None,
                    "new_value": "requests",
                    "metadata": {}
                }
            ]
        }

        tracker = ChangeTracker.from_dict(tracker_dict)

        assert tracker.change_count == 2
        assert tracker.changes[0].change_type == ChangeType.FILE_ADDED
        assert tracker.changes[1].change_type == ChangeType.DEPENDENCY_ADDED

    def test_round_trip_serialization(self):
        """Test round-trip serialization of ChangeTracker."""
        original = ChangeTracker()
        original.record_file_added("file1.py", "Purpose 1")
        original.record_dependency_added("pytest")

        # Round-trip
        tracker_dict = original.to_dict()
        restored = ChangeTracker.from_dict(tracker_dict)

        assert restored.change_count == original.change_count
        assert len(restored.changes) == len(original.changes)

    def test_changes_property_returns_copy(self):
        """Test that changes property returns a copy (read-only)."""
        tracker = ChangeTracker()
        tracker.record_file_added("file.py")

        changes_copy = tracker.changes

        # Modifying the copy should not affect tracker
        changes_copy.append(None)

        assert tracker.change_count == 1  # Unchanged


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_file_path(self):
        """Test recording change with empty file path."""
        tracker = ChangeTracker()
        tracker.record_file_added("")

        assert tracker.change_count == 1
        assert tracker.changes[0].target == ""

    def test_file_path_with_spaces(self):
        """Test recording change with file path containing spaces."""
        tracker = ChangeTracker()
        tracker.record_file_added("path with spaces/file.py")

        assert tracker.change_count == 1
        assert tracker.changes[0].target == "path with spaces/file.py"

    def test_invalid_file_extension(self):
        """Test recording change with invalid file extension."""
        tracker = ChangeTracker()
        tracker.record_file_added("file.invalid_ext")

        assert tracker.change_count == 1
        assert tracker.changes[0].target == "file.invalid_ext"

    def test_negative_estimated_loc(self):
        """Test recording change with negative estimated LOC."""
        tracker = ChangeTracker()
        tracker.record_file_added("file.py", estimated_loc=-100)

        assert tracker.change_count == 1
        assert tracker.changes[0].metadata["estimated_loc"] == -100

    def test_very_long_file_path(self):
        """Test recording change with very long file path."""
        long_path = "a/" * 100 + "file.py"

        tracker = ChangeTracker()
        tracker.record_file_added(long_path)

        assert tracker.change_count == 1
        assert tracker.changes[0].target == long_path

    def test_unicode_in_file_paths(self):
        """Test recording changes with unicode file paths."""
        tracker = ChangeTracker()
        tracker.record_file_added("файл.py")  # Russian
        tracker.record_file_added("文件.py")  # Chinese
        tracker.record_file_added("ファイル.py")  # Japanese

        assert tracker.change_count == 3
        assert tracker.changes[0].target == "файл.py"

    def test_special_characters_in_purpose(self):
        """Test recording changes with special characters in purpose."""
        tracker = ChangeTracker()
        tracker.record_file_added(
            "file.py",
            purpose="Purpose with\nnewlines\tand\ttabs"
        )

        assert tracker.change_count == 1
        assert "\n" in tracker.changes[0].new_value

    def test_none_values_in_metadata(self):
        """Test handling None values in metadata."""
        tracker = ChangeTracker()
        tracker.record_metadata_updated(
            "test_field",
            old_value=None,
            new_value="new_value"
        )

        assert tracker.change_count == 1
        assert tracker.changes[0].old_value is None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
