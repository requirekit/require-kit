"""
Unit Tests for Plan Markdown Renderer and Parser

Part of TASK-027: Convert Implementation Plan Storage from JSON to Markdown.

Tests the complete markdown save/load cycle including:
- Rendering plans to markdown with frontmatter
- Parsing markdown back to structured data
- Backward compatibility with JSON format
- Round-trip preservation of data

Author: Claude (Anthropic)
Created: 2025-10-18
"""

import pytest
import tempfile
import json
import sys
from pathlib import Path
from datetime import datetime

# Add lib directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

import plan_markdown_renderer
import plan_markdown_parser
import plan_persistence

from plan_markdown_renderer import PlanMarkdownRenderer, PlanMarkdownRendererError
from plan_markdown_parser import PlanMarkdownParser, PlanMarkdownParserError
from plan_persistence import save_plan, load_plan, plan_exists, delete_plan


class TestPlanMarkdownRenderer:
    """Test suite for PlanMarkdownRenderer."""

    def test_renderer_initialization(self):
        """Test that renderer initializes correctly."""
        renderer = PlanMarkdownRenderer()
        assert renderer is not None
        assert renderer.template is not None

    def test_render_minimal_plan(self):
        """Test rendering a minimal plan."""
        plan = {
            "task_id": "TASK-001",
            "saved_at": "2025-10-18T10:00:00Z",
            "version": 1,
            "plan": {
                "summary": "Test plan",
                "files_to_create": ["src/test.py"],
                "estimated_duration": "2 hours"
            }
        }

        renderer = PlanMarkdownRenderer()
        markdown = renderer.render(plan)

        # Verify frontmatter
        assert "task_id: TASK-001" in markdown
        assert "saved_at: '2025-10-18T10:00:00Z'" in markdown

        # Verify content
        assert "# Implementation Plan: TASK-001" in markdown
        assert "Test plan" in markdown
        assert "src/test.py" in markdown
        assert "2 hours" in markdown

    def test_render_full_plan(self):
        """Test rendering a complete plan with all fields."""
        plan = {
            "task_id": "TASK-042",
            "saved_at": "2025-10-18T10:00:00Z",
            "version": 1,
            "plan": {
                "summary": "Implement authentication system",
                "files_to_create": [
                    {"path": "src/auth/AuthService.ts", "description": "Main auth service"},
                    {"path": "tests/auth.test.ts", "description": "Auth tests"}
                ],
                "files_to_modify": ["src/app.ts"],
                "external_dependencies": [
                    {"name": "jsonwebtoken", "version": "^9.0.0", "purpose": "JWT handling"}
                ],
                "estimated_duration": "4 hours",
                "estimated_loc": 245,
                "complexity_score": 5,
                "risks": [
                    {
                        "description": "JWT secret management",
                        "mitigation": "Use environment variables"
                    }
                ],
                "implementation_notes": [
                    "Start with TokenManager",
                    "Implement AuthService",
                    "Write tests"
                ]
            },
            "architectural_review": {
                "score": 85,
                "solid_compliance": {
                    "Single Responsibility": {
                        "status": "pass",
                        "description": "Each class has one purpose"
                    }
                },
                "warnings": ["Consider extracting validation"]
            }
        }

        renderer = PlanMarkdownRenderer()
        markdown = renderer.render(plan)

        # Verify all sections present
        assert "## Summary" in markdown
        assert "## Files to Create" in markdown
        assert "## Dependencies" in markdown
        assert "## Risks & Mitigation" in markdown
        assert "## Architectural Review" in markdown
        assert "**Score**: 85/100" in markdown

    def test_save_markdown(self, tmp_path):
        """Test saving markdown to file."""
        plan = {
            "task_id": "TASK-001",
            "saved_at": "2025-10-18T10:00:00Z",
            "version": 1,
            "plan": {"summary": "Test"}
        }

        renderer = PlanMarkdownRenderer()
        output_path = tmp_path / "test_plan.md"
        renderer.save_markdown(plan, output_path)

        assert output_path.exists()
        content = output_path.read_text()
        assert "TASK-001" in content


class TestPlanMarkdownParser:
    """Test suite for PlanMarkdownParser."""

    def test_parser_initialization(self):
        """Test that parser initializes correctly."""
        parser = PlanMarkdownParser()
        assert parser is not None

    def test_parse_minimal_markdown(self, tmp_path):
        """Test parsing minimal markdown plan."""
        markdown_content = """---
task_id: TASK-001
saved_at: '2025-10-18T10:00:00Z'
version: 1
---

# Implementation Plan: TASK-001

## Summary
Test plan for authentication

## Files to Create
- `src/auth.py`
- `tests/test_auth.py`

## Estimated Effort
- **Duration**: 2 hours
- **Lines of Code**: 100
- **Complexity**: 3/10 (Simple)
"""

        md_file = tmp_path / "plan.md"
        md_file.write_text(markdown_content)

        parser = PlanMarkdownParser()
        plan = parser.parse_file(md_file)

        assert plan["task_id"] == "TASK-001"
        assert plan["plan"]["summary"] == "Test plan for authentication"
        assert "src/auth.py" in plan["plan"]["files_to_create"]
        assert plan["plan"]["estimated_duration"] == "2 hours"
        assert plan["plan"]["estimated_loc"] == 100
        assert plan["plan"]["complexity_score"] == 3

    def test_parse_with_risks(self, tmp_path):
        """Test parsing risks and mitigation."""
        markdown_content = """---
task_id: TASK-001
---

# Implementation Plan: TASK-001

## Risks & Mitigation
- **Risk**: JWT secret exposure
  - **Mitigation**: Use environment variables
- **Risk**: Token expiration
  - **Mitigation**: Implement refresh tokens
"""

        md_file = tmp_path / "plan.md"
        md_file.write_text(markdown_content)

        parser = PlanMarkdownParser()
        plan = parser.parse_file(md_file)

        risks = plan["plan"]["risks"]
        assert len(risks) == 2
        assert risks[0]["description"] == "JWT secret exposure"
        assert risks[0]["mitigation"] == "Use environment variables"

    def test_parse_json_fallback(self, tmp_path):
        """Test that parser falls back to JSON for legacy plans."""
        json_data = {
            "task_id": "TASK-001",
            "plan": {"summary": "Legacy plan"}
        }

        json_file = tmp_path / "plan.json"
        json_file.write_text(json.dumps(json_data))

        parser = PlanMarkdownParser()
        # Request .md but only .json exists - should fallback
        md_path = tmp_path / "plan.md"
        plan = parser.parse_file(md_path)

        assert plan["task_id"] == "TASK-001"
        assert plan["plan"]["summary"] == "Legacy plan"

    def test_parse_file_not_found(self, tmp_path):
        """Test error when neither markdown nor JSON exists."""
        parser = PlanMarkdownParser()
        md_path = tmp_path / "nonexistent.md"

        with pytest.raises(FileNotFoundError):
            parser.parse_file(md_path)


class TestRoundTripConversion:
    """Test that data survives the save -> load cycle."""

    def test_round_trip_preservation(self, tmp_path):
        """Test that plan data is preserved through save and load."""
        original_plan = {
            "task_id": "TASK-042",
            "saved_at": "2025-10-18T10:00:00Z",
            "version": 1,
            "plan": {
                "summary": "Implement feature X",
                "files_to_create": ["src/feature.py", "tests/test_feature.py"],
                "files_to_modify": ["src/app.py"],
                "external_dependencies": ["pytest ^7.0.0"],
                "estimated_duration": "3 hours",
                "estimated_loc": 150,
                "complexity_score": 4,
                "risks": [
                    {
                        "description": "External API dependency",
                        "mitigation": "Mock in tests"
                    }
                ]
            }
        }

        # Save as markdown
        md_file = tmp_path / "plan.md"
        renderer = PlanMarkdownRenderer()
        renderer.save_markdown(original_plan, md_file)

        # Load back
        parser = PlanMarkdownParser()
        loaded_plan = parser.parse_file(md_file)

        # Verify critical data preserved
        assert loaded_plan["task_id"] == original_plan["task_id"]
        assert loaded_plan["plan"]["summary"] == original_plan["plan"]["summary"]
        assert set(loaded_plan["plan"]["files_to_create"]) == set(original_plan["plan"]["files_to_create"])
        assert loaded_plan["plan"]["estimated_duration"] == original_plan["plan"]["estimated_duration"]
        assert loaded_plan["plan"]["complexity_score"] == original_plan["plan"]["complexity_score"]


class TestPlanPersistence:
    """Test the high-level plan persistence functions."""

    def test_save_and_load_plan(self, tmp_path, monkeypatch):
        """Test save_plan and load_plan integration."""
        # Change to temp directory
        monkeypatch.chdir(tmp_path)

        plan = {
            "summary": "Test implementation",
            "files_to_create": ["src/test.py"],
            "estimated_duration": "1 hour"
        }

        # Save plan
        plan_path = save_plan("TASK-001", plan)
        assert plan_path.endswith("implementation_plan.md")
        assert Path(plan_path).exists()

        # Load plan
        loaded = load_plan("TASK-001")
        assert loaded is not None
        assert loaded["task_id"] == "TASK-001"
        assert loaded["plan"]["summary"] == "Test implementation"

    def test_plan_exists(self, tmp_path, monkeypatch):
        """Test plan_exists function."""
        monkeypatch.chdir(tmp_path)

        assert not plan_exists("TASK-999")

        save_plan("TASK-001", {"summary": "Test"})
        assert plan_exists("TASK-001")

    def test_delete_plan(self, tmp_path, monkeypatch):
        """Test delete_plan function."""
        monkeypatch.chdir(tmp_path)

        save_plan("TASK-001", {"summary": "Test"})
        assert plan_exists("TASK-001")

        delete_plan("TASK-001")
        assert not plan_exists("TASK-001")

    def test_backward_compatibility_json(self, tmp_path, monkeypatch):
        """Test that legacy JSON plans still load correctly."""
        monkeypatch.chdir(tmp_path)

        # Manually create legacy JSON plan
        state_dir = Path("docs/state/TASK-OLD")
        state_dir.mkdir(parents=True)

        json_plan = {
            "task_id": "TASK-OLD",
            "plan": {
                "summary": "Legacy plan from JSON",
                "files_to_create": ["old.py"]
            }
        }

        json_file = state_dir / "implementation_plan.json"
        json_file.write_text(json.dumps(json_plan))

        # Load should work
        loaded = load_plan("TASK-OLD")
        assert loaded is not None
        assert loaded["plan"]["summary"] == "Legacy plan from JSON"

    def test_markdown_preferred_over_json(self, tmp_path, monkeypatch):
        """Test that markdown is preferred when both formats exist."""
        monkeypatch.chdir(tmp_path)

        state_dir = Path("docs/state/TASK-BOTH")
        state_dir.mkdir(parents=True)

        # Create both markdown and JSON
        md_plan = {
            "task_id": "TASK-BOTH",
            "saved_at": "2025-10-18T10:00:00Z",
            "version": 1,
            "plan": {"summary": "From markdown"}
        }

        json_plan = {
            "task_id": "TASK-BOTH",
            "plan": {"summary": "From JSON"}
        }

        renderer = PlanMarkdownRenderer()
        renderer.save_markdown(md_plan, state_dir / "implementation_plan.md")

        with open(state_dir / "implementation_plan.json", 'w') as f:
            json.dump(json_plan, f)

        # Load should prefer markdown
        loaded = load_plan("TASK-BOTH")
        assert loaded["plan"]["summary"] == "From markdown"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
