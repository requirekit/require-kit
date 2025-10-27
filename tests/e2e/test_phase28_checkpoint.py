"""
End-to-end tests for Phase 2.8 checkpoint display.

Tests the complete display_phase28_checkpoint function including
stdout output and user interaction scenarios.

Part of TASK-028: Enhance Phase 2.8 Checkpoint Display with Plan Summary.
"""

import pytest
import json
from pathlib import Path
import sys
from io import StringIO
from unittest.mock import patch

# Add lib directory to path for imports
lib_path = Path(__file__).parent.parent.parent / "installer" / "global" / "commands" / "lib"
sys.path.insert(0, str(lib_path))

from checkpoint_display import (
    display_phase28_checkpoint,
    PlanSummary,
    FileChange,
    Dependency,
    Risk,
    RiskLevel,
    EffortEstimate
)


class TestDisplayPhase28CheckpointWithPlan:
    """Test display_phase28_checkpoint with saved plan."""

    def test_display_simple_plan_complexity_5(self, tmp_path, capsys):
        """Test display with simple plan at medium complexity."""
        # Create plan file
        task_id = "TASK-E2E-001"
        plan_data = {
            "task_id": task_id,
            "saved_at": "2025-10-18T10:00:00",
            "version": 1,
            "plan": {
                "files_to_create": ["src/feature.py", "tests/test_feature.py"],
                "external_dependencies": ["pytest"],
                "estimated_duration": "2 hours",
                "estimated_loc": 100,
                "complexity_score": 5,
                "test_summary": "Unit tests for all functions",
                "risks": [
                    {
                        "description": "Moderate complexity",
                        "level": "medium"
                    }
                ]
            }
        }

        plan_path = tmp_path / "plan.json"
        with open(plan_path, 'w') as f:
            json.dump(plan_data, f)

        # Display checkpoint
        display_phase28_checkpoint(task_id, complexity_score=5, plan_path=plan_path)

        # Capture output
        captured = capsys.readouterr()
        output = captured.out

        # Verify key sections
        assert "PHASE 2.8: IMPLEMENTATION PLAN CHECKPOINT" in output
        assert "Task: TASK-E2E-001" in output
        assert "Complexity: 5/10 (Medium - quick review)" in output
        assert "IMPLEMENTATION PLAN SUMMARY" in output
        assert "Files to Change (2)" in output
        assert "src/feature.py (create)" in output
        assert "Dependencies (1)" in output
        assert "pytest" in output
        assert "Risks (1)" in output
        assert "🟡 MEDIUM: Moderate complexity" in output
        assert "Effort Estimate:" in output
        assert "Duration: 2 hours" in output
        assert "Testing Approach:" in output
        assert "CHECKPOINT: Review implementation plan" in output
        assert "[A]pprove" in output
        assert "[M]odify" in output
        assert "[C]ancel" in output

    def test_display_complex_plan_complexity_8(self, tmp_path, capsys):
        """Test display with complex plan at high complexity."""
        task_id = "TASK-E2E-002"
        plan_data = {
            "task_id": task_id,
            "saved_at": "2025-10-18T10:00:00",
            "version": 1,
            "plan": {
                "files_to_create": [
                    "src/module1.py",
                    "src/module2.py",
                    "src/module3.py",
                    "tests/test_module1.py",
                    "tests/test_module2.py",
                    "tests/test_module3.py"
                ],
                "files_to_modify": ["src/main.py", "src/config.py"],
                "external_dependencies": [
                    {"name": "requests", "version": "2.28.0"},
                    {"name": "sqlalchemy", "version": "1.4.0"},
                    {"name": "pytest", "version": "7.0.0"}
                ],
                "estimated_duration": "8 hours",
                "estimated_loc": 500,
                "complexity_score": 8,
                "test_summary": "Comprehensive unit and integration tests",
                "risks": [
                    {
                        "description": "Database schema changes",
                        "level": "high",
                        "mitigation": "Run migrations in transaction"
                    },
                    {
                        "description": "External API dependency",
                        "level": "medium",
                        "mitigation": "Add retry logic"
                    }
                ]
            }
        }

        plan_path = tmp_path / "plan_complex.json"
        with open(plan_path, 'w') as f:
            json.dump(plan_data, f)

        # Display checkpoint
        display_phase28_checkpoint(task_id, complexity_score=8, plan_path=plan_path)

        # Capture output
        captured = capsys.readouterr()
        output = captured.out

        # Verify complexity level
        assert "Complexity: 8/10 (Complex - requires full review)" in output

        # Verify file count (should show truncation if > 5)
        assert "Files to Change (8)" in output

        # Verify dependencies
        assert "Dependencies (3)" in output
        assert "requests (2.28.0)" in output

        # Verify risks with icons
        assert "Risks (2)" in output
        assert "🔴 HIGH: Database schema changes" in output
        assert "Mitigation: Run migrations in transaction" in output
        assert "🟡 MEDIUM: External API dependency" in output


class TestDisplayPhase28CheckpointWithoutPlan:
    """Test display_phase28_checkpoint without saved plan."""

    def test_display_without_plan_low_complexity(self, capsys):
        """Test display without plan at low complexity (no warning)."""
        task_id = "TASK-NO-PLAN-001"

        # Display checkpoint (no plan file)
        display_phase28_checkpoint(task_id, complexity_score=3)

        # Capture output
        captured = capsys.readouterr()
        output = captured.out

        # Should show basic checkpoint info
        assert "PHASE 2.8: IMPLEMENTATION PLAN CHECKPOINT" in output
        assert "Task: TASK-NO-PLAN-001" in output
        assert "Complexity: 3/10 (Simple - auto-proceed)" in output

        # Should show missing plan message
        assert "⚠️  No implementation plan found" in output

        # Should NOT show warning for low complexity
        assert "WARNING" not in output

    def test_display_without_plan_high_complexity(self, capsys):
        """Test display without plan at high complexity (shows warning)."""
        task_id = "TASK-NO-PLAN-002"

        # Display checkpoint (no plan file)
        display_phase28_checkpoint(task_id, complexity_score=8)

        # Capture output
        captured = capsys.readouterr()
        output = captured.out

        # Should show warning for high complexity without plan
        assert "⚠️  No implementation plan found" in output
        assert "WARNING: Complex task without saved plan" in output
        assert "--design-only" in output


class TestDisplayPhase28CheckpointFileLocation:
    """Test display of plan file location."""

    def test_display_shows_plan_file_location(self, tmp_path, capsys):
        """Test that plan file location is displayed."""
        task_id = "TASK-FILE-LOC"
        plan_data = {
            "task_id": task_id,
            "saved_at": "2025-10-18T10:00:00",
            "version": 1,
            "plan": {
                "files_to_create": ["test.py"]
            }
        }

        plan_path = tmp_path / "test_plan.json"
        with open(plan_path, 'w') as f:
            json.dump(plan_data, f)

        # Display checkpoint
        display_phase28_checkpoint(task_id, complexity_score=5, plan_path=plan_path)

        # Capture output
        captured = capsys.readouterr()
        output = captured.out

        # Should show plan file path
        assert f"Plan file: {plan_path}" in output

    def test_display_shows_view_command(self, tmp_path, capsys):
        """Test that view command is displayed for plan file."""
        task_id = "TASK-VIEW-CMD"
        plan_data = {
            "task_id": task_id,
            "saved_at": "2025-10-18T10:00:00",
            "version": 1,
            "plan": {
                "files_to_create": ["test.py"]
            }
        }

        plan_path = tmp_path / "view_plan.json"
        with open(plan_path, 'w') as f:
            json.dump(plan_data, f)

        # Display checkpoint
        display_phase28_checkpoint(task_id, complexity_score=5, plan_path=plan_path)

        # Capture output
        captured = capsys.readouterr()
        output = captured.out

        # Should show cat command (when not using explicit path, shows standard location)
        # Note: When plan_path is explicit, shows that path, but cat command shows standard location
        assert "View with: cat" in output


class TestDisplayPhase28CheckpointTruncation:
    """Test truncation behavior in display."""

    def test_display_truncates_long_file_list(self, tmp_path, capsys):
        """Test that long file lists are truncated."""
        task_id = "TASK-TRUNCATE"
        plan_data = {
            "task_id": task_id,
            "saved_at": "2025-10-18T10:00:00",
            "version": 1,
            "plan": {
                "files_to_create": [f"file{i}.py" for i in range(10)]
            }
        }

        plan_path = tmp_path / "truncate_plan.json"
        with open(plan_path, 'w') as f:
            json.dump(plan_data, f)

        # Display checkpoint
        display_phase28_checkpoint(task_id, complexity_score=5, plan_path=plan_path)

        # Capture output
        captured = capsys.readouterr()
        output = captured.out

        # Should show total count
        assert "Files to Change (10)" in output

        # Should show first files
        assert "file0.py" in output

        # Should show truncation message
        assert "... and 5 more" in output

        # Should NOT show last files
        assert "file9.py" not in output


class TestDisplayPhase28CheckpointReviewModes:
    """Test different review modes display correctly."""

    def test_auto_proceed_mode_complexity_1(self, capsys):
        """Test AUTO_PROCEED mode display."""
        display_phase28_checkpoint("TASK-AUTO", complexity_score=1)

        captured = capsys.readouterr()
        assert "Complexity: 1/10 (Simple - auto-proceed)" in captured.out

    def test_quick_optional_mode_complexity_5(self, capsys):
        """Test QUICK_OPTIONAL mode display."""
        display_phase28_checkpoint("TASK-QUICK", complexity_score=5)

        captured = capsys.readouterr()
        assert "Complexity: 5/10 (Medium - quick review)" in captured.out

    def test_full_required_mode_complexity_9(self, capsys):
        """Test FULL_REQUIRED mode display."""
        display_phase28_checkpoint("TASK-FULL", complexity_score=9)

        captured = capsys.readouterr()
        assert "Complexity: 9/10 (Complex - requires full review)" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
