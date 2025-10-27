"""
Unit tests for plan_persistence.py - Implementation plan persistence for design-first workflow.

Tests cover:
    - Save plan functionality
    - Load plan functionality
    - Plan existence checks
    - Delete plan functionality
    - Error handling for I/O failures
    - Plan metadata structure
    - Directory creation
    - JSON serialization/deserialization

Part of TASK-006: Add Design-First Workflow Flags to task-work Command
"""

import pytest
import json
import tempfile
import shutil
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
import sys

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "installer/global/commands/lib"))

from plan_persistence import (
    save_plan,
    load_plan,
    plan_exists,
    delete_plan,
    PlanPersistenceError,
)


@pytest.fixture
def temp_docs_dir(tmp_path):
    """Create a temporary docs/state directory for testing."""
    docs_dir = tmp_path / "docs" / "state"
    docs_dir.mkdir(parents=True)

    # Change to temp directory for tests
    original_cwd = Path.cwd()
    import os
    os.chdir(tmp_path)

    yield docs_dir

    # Restore original directory
    os.chdir(original_cwd)


@pytest.fixture
def sample_plan():
    """Sample implementation plan for testing."""
    return {
        "files_to_create": [
            "src/feature.py",
            "tests/test_feature.py"
        ],
        "files_to_modify": [
            "src/main.py"
        ],
        "external_dependencies": [
            "requests",
            "pytest"
        ],
        "estimated_duration": "4 hours",
        "estimated_loc": 250,
        "phases": [
            "Design",
            "Implementation",
            "Testing"
        ],
        "test_summary": "Unit tests with 90% coverage",
        "risks": [
            {"type": "technical", "description": "API rate limiting"}
        ]
    }


@pytest.fixture
def sample_review_result():
    """Sample architectural review result for testing."""
    return {
        "score": 85,
        "recommendations": [
            "Consider adding error handling",
            "Use dependency injection"
        ],
        "concerns": [],
        "approved": True
    }


class TestSavePlan:
    """Test suite for save_plan function."""

    def test_save_plan_creates_state_directory(self, temp_docs_dir, sample_plan):
        """Test that save_plan creates state directory if it doesn't exist."""
        task_id = "TASK-001"

        plan_path = save_plan(task_id, sample_plan)

        assert Path(plan_path).exists()
        assert Path("docs/state/TASK-001").exists()

    def test_save_plan_returns_absolute_path(self, temp_docs_dir, sample_plan):
        """Test that save_plan returns absolute path."""
        task_id = "TASK-002"

        plan_path = save_plan(task_id, sample_plan)

        assert Path(plan_path).is_absolute()
        assert "implementation_plan.json" in plan_path

    def test_save_plan_includes_metadata(self, temp_docs_dir, sample_plan):
        """Test that saved plan includes metadata."""
        task_id = "TASK-003"

        plan_path = save_plan(task_id, sample_plan)

        with open(plan_path, 'r') as f:
            saved_data = json.load(f)

        assert saved_data["task_id"] == task_id
        assert "saved_at" in saved_data
        assert "version" in saved_data
        assert saved_data["version"] == 1
        assert "plan" in saved_data

    def test_save_plan_preserves_plan_content(self, temp_docs_dir, sample_plan):
        """Test that plan content is preserved correctly."""
        task_id = "TASK-004"

        plan_path = save_plan(task_id, sample_plan)

        with open(plan_path, 'r') as f:
            saved_data = json.load(f)

        assert saved_data["plan"] == sample_plan
        assert saved_data["plan"]["files_to_create"] == sample_plan["files_to_create"]
        assert saved_data["plan"]["estimated_duration"] == sample_plan["estimated_duration"]

    def test_save_plan_with_review_result(self, temp_docs_dir, sample_plan, sample_review_result):
        """Test that architectural review result is saved when provided."""
        task_id = "TASK-005"

        plan_path = save_plan(task_id, sample_plan, review_result=sample_review_result)

        with open(plan_path, 'r') as f:
            saved_data = json.load(f)

        assert "architectural_review" in saved_data
        assert saved_data["architectural_review"] == sample_review_result

    def test_save_plan_without_review_result(self, temp_docs_dir, sample_plan):
        """Test that plan can be saved without review result."""
        task_id = "TASK-006"

        plan_path = save_plan(task_id, sample_plan)

        with open(plan_path, 'r') as f:
            saved_data = json.load(f)

        assert "architectural_review" not in saved_data

    def test_save_plan_overwrites_existing_plan(self, temp_docs_dir, sample_plan):
        """Test that save_plan overwrites existing plan."""
        task_id = "TASK-007"

        # Save first plan
        save_plan(task_id, sample_plan)

        # Modify plan
        modified_plan = sample_plan.copy()
        modified_plan["estimated_duration"] = "8 hours"

        # Save modified plan
        plan_path = save_plan(task_id, modified_plan)

        with open(plan_path, 'r') as f:
            saved_data = json.load(f)

        assert saved_data["plan"]["estimated_duration"] == "8 hours"

    def test_save_plan_json_format(self, temp_docs_dir, sample_plan):
        """Test that saved plan is valid JSON with indentation."""
        task_id = "TASK-008"

        plan_path = save_plan(task_id, sample_plan)

        # Should be valid JSON
        with open(plan_path, 'r') as f:
            content = f.read()
            json.loads(content)  # Should not raise

        # Should have indentation (pretty-printed)
        assert "\n" in content
        assert "  " in content

    def test_save_plan_handles_special_characters(self, temp_docs_dir):
        """Test that save_plan handles special characters in plan data."""
        task_id = "TASK-009"
        plan = {
            "description": "Test with 'quotes' and \"double quotes\"",
            "risks": ["Risk with unicode: 🚀"]
        }

        plan_path = save_plan(task_id, plan)

        with open(plan_path, 'r') as f:
            saved_data = json.load(f)

        assert saved_data["plan"]["description"] == plan["description"]

    def test_save_plan_io_error_raises_persistence_error(self, temp_docs_dir, sample_plan):
        """Test that I/O errors are wrapped in PlanPersistenceError."""
        task_id = "TASK-010"

        with patch("builtins.open", side_effect=IOError("Disk full")):
            with pytest.raises(PlanPersistenceError) as exc_info:
                save_plan(task_id, sample_plan)

        assert "Failed to save implementation plan" in str(exc_info.value)
        assert task_id in str(exc_info.value)


class TestLoadPlan:
    """Test suite for load_plan function."""

    def test_load_plan_returns_saved_data(self, temp_docs_dir, sample_plan):
        """Test that load_plan returns the saved plan data."""
        task_id = "TASK-011"

        save_plan(task_id, sample_plan)
        loaded_data = load_plan(task_id)

        assert loaded_data is not None
        assert loaded_data["task_id"] == task_id
        assert loaded_data["plan"] == sample_plan

    def test_load_plan_nonexistent_returns_none(self, temp_docs_dir):
        """Test that load_plan returns None for nonexistent plan."""
        task_id = "TASK-NONEXISTENT"

        loaded_data = load_plan(task_id)

        assert loaded_data is None

    def test_load_plan_includes_metadata(self, temp_docs_dir, sample_plan):
        """Test that loaded data includes all metadata."""
        task_id = "TASK-012"

        save_plan(task_id, sample_plan)
        loaded_data = load_plan(task_id)

        assert "saved_at" in loaded_data
        assert "version" in loaded_data
        assert "plan" in loaded_data

    def test_load_plan_with_review_result(self, temp_docs_dir, sample_plan, sample_review_result):
        """Test loading plan with architectural review result."""
        task_id = "TASK-013"

        save_plan(task_id, sample_plan, review_result=sample_review_result)
        loaded_data = load_plan(task_id)

        assert "architectural_review" in loaded_data
        assert loaded_data["architectural_review"]["score"] == 85

    def test_load_plan_corrupted_json_raises_error(self, temp_docs_dir):
        """Test that corrupted JSON raises PlanPersistenceError."""
        task_id = "TASK-014"

        # Create corrupted JSON file
        state_dir = Path("docs/state") / task_id
        state_dir.mkdir(parents=True, exist_ok=True)
        plan_path = state_dir / "implementation_plan.json"

        with open(plan_path, 'w') as f:
            f.write("{invalid json")

        with pytest.raises(PlanPersistenceError) as exc_info:
            load_plan(task_id)

        assert "Failed to load implementation plan" in str(exc_info.value)

    def test_load_plan_io_error_raises_persistence_error(self, temp_docs_dir, sample_plan):
        """Test that I/O errors are wrapped in PlanPersistenceError."""
        task_id = "TASK-015"

        save_plan(task_id, sample_plan)

        with patch("builtins.open", side_effect=IOError("Permission denied")):
            with pytest.raises(PlanPersistenceError) as exc_info:
                load_plan(task_id)

        assert "Failed to load" in str(exc_info.value)


class TestPlanExists:
    """Test suite for plan_exists function."""

    def test_plan_exists_returns_true_when_file_exists(self, temp_docs_dir, sample_plan):
        """Test that plan_exists returns True when plan file exists."""
        task_id = "TASK-016"

        save_plan(task_id, sample_plan)

        assert plan_exists(task_id) is True

    def test_plan_exists_returns_false_when_file_missing(self, temp_docs_dir):
        """Test that plan_exists returns False when plan file missing."""
        task_id = "TASK-MISSING"

        assert plan_exists(task_id) is False

    def test_plan_exists_returns_false_for_directory_only(self, temp_docs_dir):
        """Test that plan_exists returns False if directory exists but not file."""
        task_id = "TASK-017"

        # Create directory but not file
        state_dir = Path("docs/state") / task_id
        state_dir.mkdir(parents=True)

        assert plan_exists(task_id) is False

    def test_plan_exists_after_delete_returns_false(self, temp_docs_dir, sample_plan):
        """Test that plan_exists returns False after deletion."""
        task_id = "TASK-018"

        save_plan(task_id, sample_plan)
        assert plan_exists(task_id) is True

        delete_plan(task_id)
        assert plan_exists(task_id) is False


class TestDeletePlan:
    """Test suite for delete_plan function."""

    def test_delete_plan_removes_file(self, temp_docs_dir, sample_plan):
        """Test that delete_plan removes the plan file."""
        task_id = "TASK-019"

        plan_path = save_plan(task_id, sample_plan)
        assert Path(plan_path).exists()

        delete_plan(task_id)

        assert not Path(plan_path).exists()

    def test_delete_plan_nonexistent_is_noop(self, temp_docs_dir):
        """Test that deleting nonexistent plan is a no-op."""
        task_id = "TASK-NONEXISTENT"

        # Should not raise error
        delete_plan(task_id)

    def test_delete_plan_can_be_called_multiple_times(self, temp_docs_dir, sample_plan):
        """Test that delete_plan can be called multiple times safely."""
        task_id = "TASK-020"

        save_plan(task_id, sample_plan)

        delete_plan(task_id)
        delete_plan(task_id)  # Second call should be no-op

        assert not plan_exists(task_id)

    def test_delete_plan_io_error_raises_persistence_error(self, temp_docs_dir, sample_plan):
        """Test that I/O errors during deletion raise PlanPersistenceError."""
        task_id = "TASK-021"

        save_plan(task_id, sample_plan)

        with patch("pathlib.Path.unlink", side_effect=OSError("Permission denied")):
            with pytest.raises(PlanPersistenceError) as exc_info:
                delete_plan(task_id)

        assert "Failed to delete" in str(exc_info.value)


class TestRoundTripPersistence:
    """Test suite for round-trip save/load/delete operations."""

    def test_roundtrip_save_and_load(self, temp_docs_dir, sample_plan):
        """Test complete round-trip: save then load."""
        task_id = "TASK-022"

        # Save
        save_plan(task_id, sample_plan)

        # Load
        loaded = load_plan(task_id)

        # Verify
        assert loaded["plan"] == sample_plan

    def test_roundtrip_with_review_result(self, temp_docs_dir, sample_plan, sample_review_result):
        """Test round-trip with review result."""
        task_id = "TASK-023"

        save_plan(task_id, sample_plan, review_result=sample_review_result)
        loaded = load_plan(task_id)

        assert loaded["plan"] == sample_plan
        assert loaded["architectural_review"] == sample_review_result

    def test_roundtrip_modify_and_resave(self, temp_docs_dir, sample_plan):
        """Test modifying and re-saving a plan."""
        task_id = "TASK-024"

        # Initial save
        save_plan(task_id, sample_plan)

        # Load and modify
        loaded = load_plan(task_id)
        modified_plan = loaded["plan"].copy()
        modified_plan["estimated_duration"] = "10 hours"

        # Re-save
        save_plan(task_id, modified_plan)

        # Load again
        final = load_plan(task_id)
        assert final["plan"]["estimated_duration"] == "10 hours"

    def test_roundtrip_delete_and_check(self, temp_docs_dir, sample_plan):
        """Test complete lifecycle: save, exists, delete, not exists."""
        task_id = "TASK-025"

        # Save
        save_plan(task_id, sample_plan)
        assert plan_exists(task_id)

        # Delete
        delete_plan(task_id)
        assert not plan_exists(task_id)

        # Load should return None
        loaded = load_plan(task_id)
        assert loaded is None


class TestEdgeCases:
    """Test suite for edge cases and boundary conditions."""

    def test_save_plan_empty_plan(self, temp_docs_dir):
        """Test saving an empty plan."""
        task_id = "TASK-026"
        empty_plan = {}

        plan_path = save_plan(task_id, empty_plan)
        loaded = load_plan(task_id)

        assert loaded["plan"] == {}

    def test_save_plan_nested_structures(self, temp_docs_dir):
        """Test saving plan with deeply nested structures."""
        task_id = "TASK-027"
        complex_plan = {
            "level1": {
                "level2": {
                    "level3": {
                        "data": [1, 2, 3]
                    }
                }
            }
        }

        save_plan(task_id, complex_plan)
        loaded = load_plan(task_id)

        assert loaded["plan"]["level1"]["level2"]["level3"]["data"] == [1, 2, 3]

    def test_save_plan_with_null_values(self, temp_docs_dir):
        """Test saving plan with None/null values."""
        task_id = "TASK-028"
        plan_with_nulls = {
            "optional_field": None,
            "required_field": "value"
        }

        save_plan(task_id, plan_with_nulls)
        loaded = load_plan(task_id)

        assert loaded["plan"]["optional_field"] is None
        assert loaded["plan"]["required_field"] == "value"

    def test_save_plan_with_large_data(self, temp_docs_dir):
        """Test saving plan with large arrays."""
        task_id = "TASK-029"
        large_plan = {
            "files_to_create": [f"file_{i}.py" for i in range(1000)],
            "estimated_loc": 50000
        }

        save_plan(task_id, large_plan)
        loaded = load_plan(task_id)

        assert len(loaded["plan"]["files_to_create"]) == 1000

    def test_plan_path_construction(self, temp_docs_dir, sample_plan):
        """Test that plan path is constructed correctly."""
        task_id = "TASK-030"

        plan_path = save_plan(task_id, sample_plan)

        assert "docs/state/TASK-030/implementation_plan.json" in plan_path
        assert Path(plan_path).name == "implementation_plan.json"
        assert Path(plan_path).parent.name == "TASK-030"


class TestPlanMetadata:
    """Test suite for plan metadata structure."""

    def test_saved_at_is_iso_format(self, temp_docs_dir, sample_plan):
        """Test that saved_at timestamp is in ISO format."""
        task_id = "TASK-031"

        save_plan(task_id, sample_plan)
        loaded = load_plan(task_id)

        # Should be parseable as ISO datetime
        datetime.fromisoformat(loaded["saved_at"])

    def test_version_is_integer(self, temp_docs_dir, sample_plan):
        """Test that version is an integer."""
        task_id = "TASK-032"

        save_plan(task_id, sample_plan)
        loaded = load_plan(task_id)

        assert isinstance(loaded["version"], int)
        assert loaded["version"] == 1

    def test_task_id_matches_parameter(self, temp_docs_dir, sample_plan):
        """Test that saved task_id matches the parameter."""
        task_id = "TASK-033"

        save_plan(task_id, sample_plan)
        loaded = load_plan(task_id)

        assert loaded["task_id"] == task_id
