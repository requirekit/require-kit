"""
Integration tests for checkpoint display with plan loading (TASK-028).

Tests the integration between checkpoint_display and plan_persistence modules,
ensuring plans can be loaded from disk and displayed correctly.

Focus: File I/O, plan persistence integration, real plan loading scenarios.
"""

import pytest
from pathlib import Path
import sys
import tempfile
import json
import shutil

# Add lib directory to path for imports
lib_path = Path(__file__).parent.parent.parent / "installer" / "global" / "commands" / "lib"
sys.path.insert(0, str(lib_path))

from checkpoint_display import (
    load_plan_summary,
    display_phase28_checkpoint,
    PlanSummary,
    RiskLevel
)
from plan_persistence import save_plan, plan_exists, get_plan_path


@pytest.fixture
def temp_state_dir():
    """Create temporary state directory for testing."""
    temp_dir = tempfile.mkdtemp()
    original_cwd = Path.cwd()

    # Create docs/state structure
    state_dir = Path(temp_dir) / "docs" / "state"
    state_dir.mkdir(parents=True)

    # Change to temp directory
    import os
    os.chdir(temp_dir)

    yield temp_dir

    # Cleanup
    os.chdir(original_cwd)
    shutil.rmtree(temp_dir, ignore_errors=True)


class TestPlanLoadingIntegration:
    """Integration tests for loading saved plans."""

    def test_load_plan_summary_from_saved_markdown(self, temp_state_dir):
        """Test loading plan summary from saved markdown file."""
        task_id = "TASK-028"
        plan = {
            "files_to_create": ["src/checkpoint.py", "tests/test_checkpoint.py"],
            "files_to_modify": ["src/existing.py"],
            "external_dependencies": ["pytest"],
            "estimated_duration": "4 hours",
            "estimated_loc": 250,
            "complexity_score": 7,
            "risks": [
                {"description": "Complex logic", "level": "medium"}
            ],
            "test_summary": "Comprehensive unit tests"
        }

        # Save plan using plan_persistence
        save_plan(task_id, plan)

        # Load using checkpoint_display
        summary = load_plan_summary(task_id)

        assert summary is not None
        assert summary.task_id == task_id
        assert len(summary.files_to_change) == 3
        assert summary.files_to_change[0].change_type == "create"
        assert summary.files_to_change[2].change_type == "modify"
        assert len(summary.dependencies) == 1
        assert summary.dependencies[0].name == "pytest"
        assert summary.effort.duration == "4 hours"
        assert summary.effort.lines_of_code == 250
        assert len(summary.risks) == 1
        assert summary.test_summary == "Comprehensive unit tests"

    def test_load_plan_summary_with_complete_data(self, temp_state_dir):
        """Test loading plan with all fields populated."""
        task_id = "TASK-INTEGRATION-001"
        plan = {
            "files_to_create": ["file1.py", "file2.py"],
            "files_to_modify": ["file3.py"],
            "external_dependencies": [
                {"name": "requests", "version": "2.28.0", "purpose": "HTTP client"},
                {"name": "fastapi", "version": "0.95.0"}
            ],
            "risks": [
                {"description": "High risk item", "level": "high", "mitigation": "Add validation"},
                "String risk defaults to medium"
            ],
            "estimated_duration": "2 days",
            "estimated_loc": 500,
            "complexity_score": 8,
            "test_summary": "Unit, integration, and E2E tests",
            "phases": ["Phase 1: Setup", "Phase 2: Implementation", "Phase 3: Testing"]
        }

        save_plan(task_id, plan)
        summary = load_plan_summary(task_id)

        assert summary is not None
        assert len(summary.files_to_change) == 3
        assert len(summary.dependencies) == 2
        assert summary.dependencies[0].version == "2.28.0"
        assert summary.dependencies[0].purpose == "HTTP client"
        assert len(summary.risks) == 2
        assert summary.risks[0].level == RiskLevel.HIGH
        assert summary.risks[0].mitigation == "Add validation"
        assert summary.risks[1].level == RiskLevel.MEDIUM
        assert len(summary.phases) == 3

    def test_load_nonexistent_plan(self, temp_state_dir):
        """Test loading plan that doesn't exist."""
        summary = load_plan_summary("TASK-NONEXISTENT")
        assert summary is None

    def test_load_plan_with_minimal_data(self, temp_state_dir):
        """Test loading plan with minimal data."""
        task_id = "TASK-MINIMAL"
        plan = {
            "files_to_create": ["single_file.py"]
        }

        save_plan(task_id, plan)
        summary = load_plan_summary(task_id)

        assert summary is not None
        assert len(summary.files_to_change) == 1
        assert summary.dependencies == []
        assert summary.risks == []
        assert summary.effort is None
        assert summary.test_summary is None

    def test_load_plan_with_empty_lists(self, temp_state_dir):
        """Test loading plan with empty lists."""
        task_id = "TASK-EMPTY"
        plan = {
            "files_to_create": [],
            "files_to_modify": [],
            "external_dependencies": [],
            "risks": []
        }

        save_plan(task_id, plan)
        summary = load_plan_summary(task_id)

        assert summary is not None
        assert summary.files_to_change == []
        assert summary.dependencies == []
        assert summary.risks == []


class TestCheckpointDisplayIntegration:
    """Integration tests for complete checkpoint display workflow."""

    def test_display_checkpoint_with_saved_plan(self, temp_state_dir, capsys):
        """Test full checkpoint display with saved plan."""
        task_id = "TASK-DISPLAY-001"
        plan = {
            "files_to_create": ["src/feature.py"],
            "estimated_duration": "3 hours",
            "complexity_score": 6
        }

        save_plan(task_id, plan)
        display_phase28_checkpoint(task_id, 6)

        captured = capsys.readouterr()
        assert "PHASE 2.8: IMPLEMENTATION PLAN CHECKPOINT" in captured.out
        assert "TASK-DISPLAY-001" in captured.out
        assert "6/10" in captured.out
        assert "Files to Change" in captured.out
        assert "src/feature.py" in captured.out

    def test_display_checkpoint_without_plan(self, temp_state_dir, capsys):
        """Test checkpoint display when plan doesn't exist."""
        display_phase28_checkpoint("TASK-NO-PLAN", 5)

        captured = capsys.readouterr()
        assert "⚠️  No implementation plan found" in captured.out

    def test_display_checkpoint_all_complexity_levels(self, temp_state_dir, capsys):
        """Test checkpoint display at all complexity levels."""
        task_id = "TASK-COMPLEXITY"
        plan = {"files_to_create": ["test.py"]}
        save_plan(task_id, plan)

        # Test AUTO_PROCEED (complexity 3)
        display_phase28_checkpoint(task_id, 3)
        captured = capsys.readouterr()
        assert "Simple - auto-proceed" in captured.out

        # Test QUICK_OPTIONAL (complexity 5)
        display_phase28_checkpoint(task_id, 5)
        captured = capsys.readouterr()
        assert "Medium - quick review" in captured.out

        # Test FULL_REQUIRED (complexity 8)
        display_phase28_checkpoint(task_id, 8)
        captured = capsys.readouterr()
        assert "Complex - requires full review" in captured.out


class TestPlanPersistenceIntegration:
    """Integration tests for plan persistence with checkpoint display."""

    def test_plan_exists_after_save(self, temp_state_dir):
        """Test plan_exists returns True after saving."""
        task_id = "TASK-EXISTS"
        plan = {"files_to_create": ["test.py"]}

        assert not plan_exists(task_id)
        save_plan(task_id, plan)
        assert plan_exists(task_id)

    def test_get_plan_path_after_save(self, temp_state_dir):
        """Test get_plan_path returns correct path after saving."""
        task_id = "TASK-PATH"
        plan = {"files_to_create": ["test.py"]}

        assert get_plan_path(task_id) is None
        save_plan(task_id, plan)

        path = get_plan_path(task_id)
        assert path is not None
        assert path.exists()
        assert path.name == "implementation_plan.md"

    def test_load_plan_with_architectural_review(self, temp_state_dir):
        """Test loading plan with architectural review results."""
        task_id = "TASK-REVIEW"
        plan = {"files_to_create": ["test.py"]}
        review_result = {
            "score": 85,
            "passed": True,
            "recommendations": ["Use dependency injection"]
        }

        save_plan(task_id, plan, review_result)
        summary = load_plan_summary(task_id)

        assert summary is not None
        # Review results stored but not displayed in summary


class TestEdgeCasesIntegration:
    """Integration tests for edge cases and error scenarios."""

    def test_load_plan_with_malformed_data(self, temp_state_dir):
        """Test loading plan with malformed data gracefully."""
        task_id = "TASK-MALFORMED"
        state_dir = Path("docs/state") / task_id
        state_dir.mkdir(parents=True, exist_ok=True)

        # Write malformed JSON manually
        plan_file = state_dir / "implementation_plan.json"
        with open(plan_file, 'w') as f:
            f.write("{invalid json")

        # Should handle gracefully
        from plan_persistence import PlanPersistenceError
        with pytest.raises(PlanPersistenceError):
            load_plan_summary(task_id)

    def test_load_plan_with_missing_required_fields(self, temp_state_dir):
        """Test loading plan with missing required fields."""
        task_id = "TASK-MISSING-FIELDS"
        plan = {}  # Empty plan

        save_plan(task_id, plan)
        summary = load_plan_summary(task_id)

        # Should return None for empty plan section
        assert summary is None

    def test_display_checkpoint_with_very_large_plan(self, temp_state_dir, capsys):
        """Test checkpoint display with large number of files."""
        task_id = "TASK-LARGE"
        plan = {
            "files_to_create": [f"file{i}.py" for i in range(50)],
            "external_dependencies": [f"pkg{i}" for i in range(20)]
        }

        save_plan(task_id, plan)
        display_phase28_checkpoint(task_id, 8)

        captured = capsys.readouterr()
        assert "Files to Change (50)" in captured.out
        assert "Dependencies (20)" in captured.out
        assert "... and" in captured.out  # Truncation indicator


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
