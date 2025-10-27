"""
Integration Tests for Plan Markdown Workflow

Part of TASK-027: Convert Implementation Plan Storage from JSON to Markdown.

Tests the complete integration of markdown plans with the task workflow:
- Phase 2.7 saves plans as markdown
- Plans can be manually edited
- Plans load correctly in subsequent phases
- Git diffs are human-readable
- Backward compatibility with JSON

Author: Claude (Anthropic)
Created: 2025-10-18
"""

import pytest
import json
from pathlib import Path
from datetime import datetime

import sys
sys.path.insert(0, str(Path(__file__).parent))

from plan_persistence import save_plan, load_plan, plan_exists
from plan_markdown_parser import PlanMarkdownParser


class TestPhase27Integration:
    """Test integration with Phase 2.7 (implementation planning)."""

    def test_phase_27_saves_markdown(self, tmp_path, monkeypatch):
        """Test that Phase 2.7 workflow saves markdown correctly."""
        monkeypatch.chdir(tmp_path)

        # Simulate Phase 2.7 creating a plan
        implementation_plan = {
            "summary": "Implement user authentication",
            "files_to_create": [
                "src/auth/AuthService.ts",
                "tests/auth/AuthService.test.ts"
            ],
            "files_to_modify": ["src/app.ts"],
            "external_dependencies": ["jsonwebtoken ^9.0.0"],
            "estimated_duration": "4 hours",
            "estimated_loc": 245,
            "complexity_score": 5,
            "risks": [
                {
                    "description": "JWT secret management",
                    "mitigation": "Use environment variables"
                }
            ]
        }

        review_result = {
            "score": 85,
            "solid_compliance": {
                "Single Responsibility": "Good"
            },
            "warnings": ["Consider extracting validation"]
        }

        # Save plan (as Phase 2.7 would)
        plan_path = save_plan("TASK-042", implementation_plan, review_result)

        # Verify it's markdown
        assert plan_path.endswith(".md")
        assert Path(plan_path).exists()

        # Verify content is human-readable
        content = Path(plan_path).read_text()
        assert "# Implementation Plan: TASK-042" in content
        assert "user authentication" in content.lower()
        assert "AuthService.ts" in content

    def test_markdown_is_human_readable(self, tmp_path, monkeypatch):
        """Test that saved markdown can be read without tools."""
        monkeypatch.chdir(tmp_path)

        plan = {
            "summary": "Add feature X",
            "files_to_create": ["feature.py"],
            "estimated_duration": "2 hours"
        }

        plan_path = save_plan("TASK-001", plan)
        content = Path(plan_path).read_text()

        # Should be readable as plain text
        assert "## Summary" in content
        assert "Add feature X" in content
        assert "## Files to Create" in content
        assert "feature.py" in content
        assert "2 hours" in content

    def test_git_diff_clarity(self, tmp_path, monkeypatch):
        """Test that changes to plan produce clear git diffs."""
        monkeypatch.chdir(tmp_path)

        # Original plan
        plan_v1 = {
            "summary": "Implement feature",
            "estimated_duration": "2 hours",
            "estimated_loc": 100
        }

        plan_path = save_plan("TASK-001", plan_v1)
        content_v1 = Path(plan_path).read_text()

        # Modified plan (e.g., human edited)
        plan_v2 = {
            "summary": "Implement feature",
            "estimated_duration": "3 hours",  # Changed
            "estimated_loc": 150  # Changed
        }

        save_plan("TASK-001", plan_v2)
        content_v2 = Path(plan_path).read_text()

        # Changes should be in clear markdown format
        assert "2 hours" in content_v1
        assert "100" in content_v1
        assert "3 hours" in content_v2
        assert "150" in content_v2

        # Structure should be preserved (easy to diff)
        assert "## Estimated Effort" in content_v1
        assert "## Estimated Effort" in content_v2


class TestManualEditing:
    """Test that markdown plans can be manually edited."""

    def test_manual_edit_preserved(self, tmp_path, monkeypatch):
        """Test that manually edited markdown loads correctly."""
        monkeypatch.chdir(tmp_path)

        # Create initial plan
        plan = {
            "summary": "Original summary",
            "files_to_create": ["file1.py", "file2.py"]
        }

        plan_path = save_plan("TASK-001", plan)

        # Manually edit the markdown (simulate human editing)
        md_file = Path(plan_path)
        content = md_file.read_text()

        # Add a new file to the list
        modified_content = content.replace(
            "- `file2.py`",
            "- `file2.py`\n- `file3.py`"
        )

        md_file.write_text(modified_content)

        # Load plan - should include manual edit
        loaded = load_plan("TASK-001")
        files = loaded["plan"]["files_to_create"]

        assert "file1.py" in files
        assert "file2.py" in files
        assert "file3.py" in files  # Manually added

    def test_summary_edit_preserved(self, tmp_path, monkeypatch):
        """Test that summary edits are preserved."""
        monkeypatch.chdir(tmp_path)

        plan = {"summary": "Original summary"}
        plan_path = save_plan("TASK-001", plan)

        # Edit summary
        md_file = Path(plan_path)
        content = md_file.read_text()
        modified = content.replace("Original summary", "Improved summary with more detail")
        md_file.write_text(modified)

        # Reload
        loaded = load_plan("TASK-001")
        assert loaded["plan"]["summary"] == "Improved summary with more detail"


class TestBackwardCompatibility:
    """Test backward compatibility with JSON plans."""

    def test_legacy_json_still_works(self, tmp_path, monkeypatch):
        """Test that old JSON plans load correctly."""
        monkeypatch.chdir(tmp_path)

        # Create legacy JSON plan
        state_dir = Path("docs/state/TASK-LEGACY")
        state_dir.mkdir(parents=True)

        legacy_plan = {
            "task_id": "TASK-LEGACY",
            "saved_at": "2025-01-01T00:00:00Z",
            "version": 1,
            "plan": {
                "summary": "Legacy JSON plan",
                "files_to_create": ["old_code.py"],
                "estimated_duration": "1 hour"
            }
        }

        json_file = state_dir / "implementation_plan.json"
        json_file.write_text(json.dumps(legacy_plan, indent=2))

        # Should load correctly
        loaded = load_plan("TASK-LEGACY")
        assert loaded is not None
        assert loaded["task_id"] == "TASK-LEGACY"
        assert loaded["plan"]["summary"] == "Legacy JSON plan"

    def test_new_plans_save_as_markdown(self, tmp_path, monkeypatch):
        """Test that new plans save as markdown, not JSON."""
        monkeypatch.chdir(tmp_path)

        plan = {"summary": "New plan"}
        plan_path = save_plan("TASK-NEW", plan)

        # Should be markdown
        assert plan_path.endswith(".md")

        # JSON should not be created
        json_path = Path("docs/state/TASK-NEW/implementation_plan.json")
        assert not json_path.exists()

    def test_migration_from_json_to_markdown(self, tmp_path, monkeypatch):
        """Test implicit migration: load JSON, save as markdown."""
        monkeypatch.chdir(tmp_path)

        # Start with JSON plan
        state_dir = Path("docs/state/TASK-MIGRATE")
        state_dir.mkdir(parents=True)

        json_plan = {
            "task_id": "TASK-MIGRATE",
            "plan": {"summary": "Old JSON plan"}
        }

        json_file = state_dir / "implementation_plan.json"
        json_file.write_text(json.dumps(json_plan))

        # Load JSON plan
        loaded = load_plan("TASK-MIGRATE")
        assert loaded["plan"]["summary"] == "Old JSON plan"

        # Modify and save (should save as markdown)
        loaded["plan"]["summary"] = "Updated to markdown"
        new_path = save_plan("TASK-MIGRATE", loaded["plan"])

        # Should now have markdown
        assert new_path.endswith(".md")
        md_file = Path(new_path)
        assert md_file.exists()

        # Markdown should be preferred on next load
        reloaded = load_plan("TASK-MIGRATE")
        assert reloaded["plan"]["summary"] == "Updated to markdown"


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_plan_sections(self, tmp_path, monkeypatch):
        """Test that plans with empty sections render correctly."""
        monkeypatch.chdir(tmp_path)

        plan = {
            "summary": "Minimal plan",
            "files_to_create": [],  # Empty
            "files_to_modify": [],  # Empty
            "risks": []  # Empty
        }

        plan_path = save_plan("TASK-EMPTY", plan)
        content = Path(plan_path).read_text()

        # Should have sections but marked as empty
        assert "## Files to Create" in content
        assert "## Files to Modify" in content

        # Should load without errors
        loaded = load_plan("TASK-EMPTY")
        assert loaded is not None

    def test_special_characters_in_summary(self, tmp_path, monkeypatch):
        """Test that special characters are handled correctly."""
        monkeypatch.chdir(tmp_path)

        plan = {
            "summary": "Summary with **bold**, `code`, and [links](url)",
            "files_to_create": ["file.py"]
        }

        plan_path = save_plan("TASK-SPECIAL", plan)

        # Should load without breaking markdown parsing
        loaded = load_plan("TASK-SPECIAL")
        assert "**bold**" in loaded["plan"]["summary"] or "bold" in loaded["plan"]["summary"]

    def test_very_long_file_list(self, tmp_path, monkeypatch):
        """Test that plans with many files render correctly."""
        monkeypatch.chdir(tmp_path)

        # Create plan with 50 files
        files = [f"src/module{i}/file{i}.py" for i in range(50)]

        plan = {
            "summary": "Large refactoring",
            "files_to_create": files
        }

        plan_path = save_plan("TASK-LARGE", plan)

        # Should save without errors
        assert Path(plan_path).exists()

        # Should load all files
        loaded = load_plan("TASK-LARGE")
        assert len(loaded["plan"]["files_to_create"]) == 50


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
