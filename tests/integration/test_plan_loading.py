"""
Integration tests for plan loading in checkpoint_display module.

Tests actual file I/O with real plan files (JSON and markdown formats).

Part of TASK-028: Enhance Phase 2.8 Checkpoint Display with Plan Summary.
"""

import pytest
import json
import tempfile
from pathlib import Path
import sys

# Add lib directory to path for imports
lib_path = Path(__file__).parent.parent.parent / "installer" / "global" / "commands" / "lib"
sys.path.insert(0, str(lib_path))

from checkpoint_display import (
    load_plan_summary,
    PlanSummary,
    FileChange,
    Dependency,
    Risk,
    RiskLevel,
    EffortEstimate
)
from plan_persistence import save_plan


@pytest.fixture
def temp_state_dir(tmp_path, monkeypatch):
    """Create temporary state directory and monkeypatch docs/state path."""
    state_dir = tmp_path / "docs" / "state"
    state_dir.mkdir(parents=True, exist_ok=True)

    # Monkeypatch Path operations to use temp directory
    original_path = Path

    class MockPath(type(Path())):
        def __new__(cls, *args, **kwargs):
            path_str = str(args[0]) if args else "."
            if path_str.startswith("docs/state"):
                # Redirect to temp directory
                relative = path_str.replace("docs/state", "")
                return original_path(tmp_path / "docs" / "state" / relative.lstrip("/"))
            return original_path(*args, **kwargs)

    # Note: Full monkeypatching Path is complex, so we'll use explicit paths in tests
    return state_dir


class TestLoadPlanSummaryJSON:
    """Test load_plan_summary with JSON files."""

    def test_load_valid_json_plan(self, tmp_path):
        """Test loading valid JSON plan file."""
        # Create plan structure
        task_id = "TASK-TEST-001"
        plan_data = {
            "task_id": task_id,
            "saved_at": "2025-10-18T10:00:00",
            "version": 1,
            "plan": {
                "files_to_create": ["src/feature.py", "tests/test_feature.py"],
                "files_to_modify": ["src/main.py"],
                "external_dependencies": ["pytest"],
                "estimated_duration": "4 hours",
                "estimated_loc": 250,
                "complexity_score": 7,
                "test_summary": "Unit and integration tests",
                "phases": ["Phase 1", "Phase 2"],
                "risks": [
                    {
                        "description": "High complexity",
                        "level": "high",
                        "mitigation": "Break into smaller tasks"
                    }
                ]
            }
        }

        # Save to temp directory
        state_dir = tmp_path / "docs" / "state" / task_id
        state_dir.mkdir(parents=True)
        plan_path = state_dir / "implementation_plan.json"

        with open(plan_path, 'w') as f:
            json.dump(plan_data, f)

        # Load summary
        summary = load_plan_summary(task_id, plan_path=plan_path)

        # Verify
        assert summary is not None
        assert summary.task_id == task_id
        assert summary.total_files == 3  # 2 creates + 1 modify
        assert len(summary.dependencies) == 1
        assert summary.dependencies[0].name == "pytest"
        assert summary.effort is not None
        assert summary.effort.duration == "4 hours"
        assert summary.effort.lines_of_code == 250
        assert summary.effort.complexity_score == 7
        assert len(summary.risks) == 1
        assert summary.risks[0].level == RiskLevel.HIGH

    def test_load_minimal_json_plan(self, tmp_path):
        """Test loading minimal JSON plan (only required fields)."""
        task_id = "TASK-TEST-002"
        plan_data = {
            "task_id": task_id,
            "saved_at": "2025-10-18T10:00:00",
            "version": 1,
            "plan": {
                "files_to_create": ["src/simple.py"]
            }
        }

        # Save to temp directory
        state_dir = tmp_path / "docs" / "state" / task_id
        state_dir.mkdir(parents=True)
        plan_path = state_dir / "implementation_plan.json"

        with open(plan_path, 'w') as f:
            json.dump(plan_data, f)

        # Load summary
        summary = load_plan_summary(task_id, plan_path=plan_path)

        # Verify
        assert summary is not None
        assert summary.total_files == 1
        assert len(summary.dependencies) == 0
        assert len(summary.risks) == 0
        assert summary.effort is None


class TestLoadPlanSummaryErrors:
    """Test error handling in load_plan_summary."""

    def test_load_missing_file(self, tmp_path):
        """Test loading non-existent plan file returns None."""
        task_id = "TASK-MISSING"

        # Don't create file
        summary = load_plan_summary(task_id, plan_path=tmp_path / "nonexistent.json")

        assert summary is None

    def test_load_invalid_json(self, tmp_path):
        """Test loading invalid JSON returns None (graceful degradation)."""
        task_id = "TASK-INVALID"
        plan_path = tmp_path / "invalid.json"

        # Write invalid JSON
        with open(plan_path, 'w') as f:
            f.write("{ invalid json }")

        # Should return None instead of raising
        summary = load_plan_summary(task_id, plan_path=plan_path)
        assert summary is None

    def test_load_empty_plan_section(self, tmp_path):
        """Test loading plan with empty 'plan' section."""
        task_id = "TASK-EMPTY"
        plan_data = {
            "task_id": task_id,
            "saved_at": "2025-10-18T10:00:00",
            "version": 1,
            "plan": {}  # Empty plan
        }

        plan_path = tmp_path / "empty.json"
        with open(plan_path, 'w') as f:
            json.dump(plan_data, f)

        # Should return None for empty plan
        summary = load_plan_summary(task_id, plan_path=plan_path)
        assert summary is None

    def test_load_missing_plan_key(self, tmp_path):
        """Test loading plan without 'plan' key."""
        task_id = "TASK-NO-PLAN-KEY"
        plan_data = {
            "task_id": task_id,
            "saved_at": "2025-10-18T10:00:00",
            "version": 1
            # Missing 'plan' key
        }

        plan_path = tmp_path / "no_plan_key.json"
        with open(plan_path, 'w') as f:
            json.dump(plan_data, f)

        # Should return None
        summary = load_plan_summary(task_id, plan_path=plan_path)
        assert summary is None


class TestLoadPlanSummaryDependencies:
    """Test dependency parsing variations."""

    def test_dependencies_as_strings(self, tmp_path):
        """Test parsing dependencies as simple strings."""
        task_id = "TASK-DEPS-STRINGS"
        plan_data = {
            "task_id": task_id,
            "saved_at": "2025-10-18T10:00:00",
            "version": 1,
            "plan": {
                "files_to_create": ["test.py"],
                "external_dependencies": ["pytest", "requests", "pandas"]
            }
        }

        plan_path = tmp_path / "deps_strings.json"
        with open(plan_path, 'w') as f:
            json.dump(plan_data, f)

        summary = load_plan_summary(task_id, plan_path=plan_path)

        assert len(summary.dependencies) == 3
        assert all(isinstance(dep, Dependency) for dep in summary.dependencies)
        assert summary.dependencies[0].name == "pytest"

    def test_dependencies_as_dicts(self, tmp_path):
        """Test parsing dependencies as dictionaries with metadata."""
        task_id = "TASK-DEPS-DICTS"
        plan_data = {
            "task_id": task_id,
            "saved_at": "2025-10-18T10:00:00",
            "version": 1,
            "plan": {
                "files_to_create": ["test.py"],
                "external_dependencies": [
                    {
                        "name": "requests",
                        "version": "2.28.0",
                        "purpose": "HTTP client"
                    },
                    {
                        "name": "pytest",
                        "version": "7.0.0"
                    }
                ]
            }
        }

        plan_path = tmp_path / "deps_dicts.json"
        with open(plan_path, 'w') as f:
            json.dump(plan_data, f)

        summary = load_plan_summary(task_id, plan_path=plan_path)

        assert len(summary.dependencies) == 2
        assert summary.dependencies[0].name == "requests"
        assert summary.dependencies[0].version == "2.28.0"
        assert summary.dependencies[0].purpose == "HTTP client"


class TestLoadPlanSummaryRisks:
    """Test risk parsing variations."""

    def test_risks_as_strings(self, tmp_path):
        """Test parsing risks as simple strings (default to MEDIUM)."""
        task_id = "TASK-RISKS-STRINGS"
        plan_data = {
            "task_id": task_id,
            "saved_at": "2025-10-18T10:00:00",
            "version": 1,
            "plan": {
                "files_to_create": ["test.py"],
                "risks": [
                    "External API dependency",
                    "Complex business logic"
                ]
            }
        }

        plan_path = tmp_path / "risks_strings.json"
        with open(plan_path, 'w') as f:
            json.dump(plan_data, f)

        summary = load_plan_summary(task_id, plan_path=plan_path)

        assert len(summary.risks) == 2
        # All should default to MEDIUM when level not specified
        assert all(risk.level == RiskLevel.MEDIUM for risk in summary.risks)

    def test_risks_as_dicts(self, tmp_path):
        """Test parsing risks as dictionaries with full metadata."""
        task_id = "TASK-RISKS-DICTS"
        plan_data = {
            "task_id": task_id,
            "saved_at": "2025-10-18T10:00:00",
            "version": 1,
            "plan": {
                "files_to_create": ["test.py"],
                "risks": [
                    {
                        "description": "Data loss risk",
                        "level": "high",
                        "mitigation": "Add transaction rollback"
                    },
                    {
                        "description": "Minor performance concern",
                        "level": "low"
                    }
                ]
            }
        }

        plan_path = tmp_path / "risks_dicts.json"
        with open(plan_path, 'w') as f:
            json.dump(plan_data, f)

        summary = load_plan_summary(task_id, plan_path=plan_path)

        assert len(summary.risks) == 2
        assert summary.risks[0].level == RiskLevel.HIGH
        assert summary.risks[0].mitigation == "Add transaction rollback"
        assert summary.risks[1].level == RiskLevel.LOW


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
