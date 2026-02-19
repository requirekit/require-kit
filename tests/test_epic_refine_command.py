"""Tests for TASK-RK01-004: Create /epic-refine Command.

Validates that installer/global/commands/epic-refine.md contains the required
three-phase flow, question categories, refinement_history schema, --focus flag,
--quick flag, completeness scoring, and UX patterns as specified by the
acceptance criteria.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

EPIC_REFINE_PATH = (
    Path(__file__).resolve().parents[1]
    / "installer"
    / "global"
    / "commands"
    / "epic-refine.md"
)


@pytest.fixture(scope="module")
def epic_refine_content() -> str:
    """Read the full epic-refine.md file content."""
    if not EPIC_REFINE_PATH.exists():
        pytest.fail(f"epic-refine.md not found at {EPIC_REFINE_PATH}")
    return EPIC_REFINE_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def content_lower(epic_refine_content: str) -> str:
    """Lowercase version for case-insensitive matching."""
    return epic_refine_content.lower()


# ---------------------------------------------------------------------------
# AC-001: Command file follows established pattern (usage, examples, process,
#         output format)
# ---------------------------------------------------------------------------


class TestCommandStructure:
    """Verify the command file follows the established pattern."""

    def test_has_usage_section(self, epic_refine_content: str) -> None:
        """Command must have a Usage section."""
        assert re.search(r"^##\s+Usage", epic_refine_content, re.MULTILINE), (
            "epic-refine.md must have a '## Usage' section"
        )

    def test_has_examples_section(self, epic_refine_content: str) -> None:
        """Command must have an Examples section."""
        assert re.search(r"^##\s+Examples", epic_refine_content, re.MULTILINE), (
            "epic-refine.md must have an '## Examples' section"
        )

    def test_has_process_section(self, epic_refine_content: str) -> None:
        """Command must have a Process section."""
        assert re.search(r"^##\s+Process", epic_refine_content, re.MULTILINE), (
            "epic-refine.md must have a '## Process' section"
        )

    def test_has_output_format_section(self, epic_refine_content: str) -> None:
        """Command must have an Output Format section."""
        assert re.search(
            r"^##\s+Output\s+Format", epic_refine_content, re.MULTILINE
        ), "epic-refine.md must have an '## Output Format' section"

    def test_usage_shows_epic_refine_syntax(self, epic_refine_content: str) -> None:
        """Usage must show the /epic-refine command syntax."""
        assert re.search(
            r"/epic-refine\s+<epic-id>", epic_refine_content
        ), "Usage must show '/epic-refine <epic-id>' syntax"


# ---------------------------------------------------------------------------
# AC-002: Three-phase flow implemented (display → questions → summary)
# ---------------------------------------------------------------------------


class TestThreePhaseFlow:
    """Verify the three-phase refinement flow is documented."""

    def test_phase_1_current_state_display(self, content_lower: str) -> None:
        """Phase 1 must cover current state display."""
        assert any(
            phrase in content_lower
            for phrase in [
                "current state",
                "display",
                "completeness",
                "phase 1",
            ]
        ), "Phase 1 (current state display) must be documented"

    def test_phase_2_targeted_questions(self, content_lower: str) -> None:
        """Phase 2 must cover targeted questions."""
        assert any(
            phrase in content_lower
            for phrase in [
                "targeted question",
                "phase 2",
                "question",
            ]
        ), "Phase 2 (targeted questions) must be documented"

    def test_phase_3_change_summary(self, content_lower: str) -> None:
        """Phase 3 must cover change summary and commit."""
        assert any(
            phrase in content_lower
            for phrase in [
                "change summary",
                "phase 3",
                "before/after",
                "apply changes",
            ]
        ), "Phase 3 (change summary) must be documented"

    def test_three_phases_in_process(self, epic_refine_content: str) -> None:
        """The process section must describe all three phases in order."""
        process_match = re.search(
            r"##\s+Process\b(.*?)(?=\n##\s[^#]|\Z)",
            epic_refine_content,
            re.DOTALL,
        )
        assert process_match, "Process section must exist"
        process_text = process_match.group(1).lower()
        # All three concepts must appear in the process
        assert "display" in process_text or "current state" in process_text or "completeness" in process_text, (
            "Process must describe the display/assessment phase"
        )
        assert "question" in process_text, (
            "Process must describe the question phase"
        )
        assert "summary" in process_text or "apply" in process_text or "commit" in process_text, (
            "Process must describe the summary/commit phase"
        )


# ---------------------------------------------------------------------------
# AC-003: Questions presented one at a time with skip/done options
# ---------------------------------------------------------------------------


class TestQuestionPresentation:
    """Verify questions are presented one at a time with skip/done."""

    def test_one_at_a_time(self, content_lower: str) -> None:
        """Questions must be presented one at a time."""
        assert "one" in content_lower and (
            "question" in content_lower or "at a time" in content_lower
        ), "Questions must be presented one at a time"

    def test_skip_option_available(self, content_lower: str) -> None:
        """Skip option must be available during questions."""
        assert "skip" in content_lower, (
            "Skip option must be documented"
        )

    def test_done_option_available(self, content_lower: str) -> None:
        """Done option must be available during questions."""
        assert "done" in content_lower, (
            "Done option must be documented"
        )

    def test_example_good_answers(self, content_lower: str) -> None:
        """Questions should include example good answers."""
        assert "example" in content_lower, (
            "Example good answers should be included with questions"
        )


# ---------------------------------------------------------------------------
# AC-004: --focus flag restricts questions to a single category
# ---------------------------------------------------------------------------


class TestFocusFlag:
    """Verify --focus flag documentation."""

    def test_focus_flag_documented(self, epic_refine_content: str) -> None:
        """The --focus flag must be documented."""
        assert "--focus" in epic_refine_content, (
            "--focus flag must be documented"
        )

    def test_focus_scope_category(self, content_lower: str) -> None:
        """--focus must support scope category."""
        assert re.search(
            r"--focus\s+scope", content_lower
        ), "--focus scope must be documented"

    def test_focus_criteria_category(self, content_lower: str) -> None:
        """--focus must support criteria category."""
        assert re.search(
            r"--focus\s+criteria", content_lower
        ), "--focus criteria must be documented"

    def test_focus_risks_category(self, content_lower: str) -> None:
        """--focus must support risks category."""
        assert re.search(
            r"--focus\s+risks", content_lower
        ), "--focus risks must be documented"

    def test_focus_restricts_to_single_category(self, content_lower: str) -> None:
        """Documentation must state --focus restricts to a single category."""
        assert any(
            phrase in content_lower
            for phrase in [
                "restricts",
                "single category",
                "focuses on",
                "limits questions",
                "only questions",
            ]
        ), "--focus must be described as restricting to a single category"


# ---------------------------------------------------------------------------
# AC-005: --quick flag skips prompts and applies AI-suggested improvements
# ---------------------------------------------------------------------------


class TestQuickFlag:
    """Verify --quick flag documentation."""

    def test_quick_flag_documented(self, epic_refine_content: str) -> None:
        """The --quick flag must be documented."""
        assert "--quick" in epic_refine_content, (
            "--quick flag must be documented"
        )

    def test_quick_skips_prompts(self, content_lower: str) -> None:
        """--quick must skip interactive prompts."""
        # Find text near --quick that mentions skipping
        quick_idx = content_lower.find("--quick")
        assert quick_idx >= 0
        # Check within 500 chars of --quick mention
        nearby = content_lower[max(0, quick_idx - 200) : quick_idx + 300]
        assert any(
            word in nearby
            for word in ["skip", "automatic", "ai-suggested", "non-interactive", "without prompts"]
        ), "--quick must be described as skipping prompts or applying automatic improvements"


# ---------------------------------------------------------------------------
# AC-006: Completeness score calculated before and after refinement
# ---------------------------------------------------------------------------


class TestCompletenessScoring:
    """Verify completeness scoring before and after."""

    def test_completeness_score_mentioned(self, content_lower: str) -> None:
        """Completeness score must be mentioned."""
        assert "completeness" in content_lower and "score" in content_lower, (
            "Completeness score must be documented"
        )

    def test_before_and_after_scoring(self, content_lower: str) -> None:
        """Both before and after scores must be shown."""
        assert "before" in content_lower and "after" in content_lower, (
            "Before and after completeness scores must be documented"
        )

    def test_nine_dimension_model_referenced(self, content_lower: str) -> None:
        """The 9-dimension completeness model must be referenced."""
        assert any(
            phrase in content_lower
            for phrase in [
                "9-dimension",
                "9 dimension",
                "nine dimension",
                "business objective",
            ]
        ), "The 9-dimension completeness model must be referenced"

    def test_visual_indicators(self, epic_refine_content: str) -> None:
        """Visual indicators for completeness must be present."""
        assert any(
            indicator in epic_refine_content
            for indicator in ["✅", "⚠️", "❌", "✓", "⚠", "check", "warning", "cross"]
        ), "Visual indicators for completeness assessment must be present"


# ---------------------------------------------------------------------------
# AC-007: refinement_history appended to frontmatter
# ---------------------------------------------------------------------------


class TestRefinementHistory:
    """Verify refinement_history schema documentation."""

    def test_refinement_history_documented(self, content_lower: str) -> None:
        """refinement_history must be documented."""
        assert "refinement_history" in content_lower, (
            "refinement_history must be documented"
        )

    def test_refinement_history_has_date(self, content_lower: str) -> None:
        """refinement_history entries must include date."""
        assert "date" in content_lower, (
            "refinement_history must include date field"
        )

    def test_refinement_history_has_changes(self, content_lower: str) -> None:
        """refinement_history entries must include changes."""
        assert "changes" in content_lower, (
            "refinement_history must include changes field"
        )

    def test_refinement_history_has_completeness_before(
        self, content_lower: str
    ) -> None:
        """refinement_history must track completeness_before."""
        assert "completeness_before" in content_lower, (
            "refinement_history must include completeness_before"
        )

    def test_refinement_history_has_completeness_after(
        self, content_lower: str
    ) -> None:
        """refinement_history must track completeness_after."""
        assert "completeness_after" in content_lower, (
            "refinement_history must include completeness_after"
        )

    def test_refinement_history_yaml_schema(self, epic_refine_content: str) -> None:
        """refinement_history schema must be shown as YAML."""
        # Look for a YAML block containing refinement_history
        pattern = re.compile(
            r"refinement_history:\s*\n\s+-\s+date:", re.DOTALL
        )
        assert pattern.search(epic_refine_content), (
            "refinement_history must have a YAML schema example"
        )


# ---------------------------------------------------------------------------
# AC-008: Graphiti push after markdown update (graceful degradation)
# ---------------------------------------------------------------------------


class TestGraphitiPush:
    """Verify Graphiti push with graceful degradation."""

    def test_graphiti_push_documented(self, content_lower: str) -> None:
        """Graphiti push must be documented."""
        assert "graphiti" in content_lower, (
            "Graphiti push must be documented"
        )

    def test_graceful_degradation(self, content_lower: str) -> None:
        """Graphiti must degrade gracefully."""
        assert any(
            phrase in content_lower
            for phrase in [
                "graceful",
                "degradation",
                "if enabled",
                "optional",
                "unavailable",
                "not configured",
            ]
        ), "Graphiti graceful degradation must be documented"


# ---------------------------------------------------------------------------
# AC-009: [REFINE] prefix and visual separators for mode clarity
# ---------------------------------------------------------------------------


class TestModeClarity:
    """Verify REFINE prefix and visual separators."""

    def test_refine_prefix_documented(self, epic_refine_content: str) -> None:
        """[REFINE] prefix must be documented."""
        assert "[REFINE]" in epic_refine_content, (
            "[REFINE] prefix must be documented"
        )

    def test_visual_separators_mentioned(self, content_lower: str) -> None:
        """Visual separators must be mentioned."""
        assert any(
            phrase in content_lower
            for phrase in [
                "visual separator",
                "separator",
                "divider",
                "visual indicator",
                "mode indicator",
                "mode clarity",
            ]
        ), "Visual separators must be documented"


# ---------------------------------------------------------------------------
# AC-010: Works in both Claude Code and Claude Desktop
# ---------------------------------------------------------------------------


class TestPlatformCompatibility:
    """Verify platform compatibility documentation."""

    def test_claude_code_mentioned(self, content_lower: str) -> None:
        """Claude Code must be mentioned as supported."""
        assert "claude code" in content_lower, (
            "Claude Code support must be documented"
        )

    def test_claude_desktop_mentioned(self, content_lower: str) -> None:
        """Claude Desktop must be mentioned as supported."""
        assert "claude desktop" in content_lower, (
            "Claude Desktop support must be documented"
        )


# ---------------------------------------------------------------------------
# AC-011: Organisation pattern assessment included in question categories
# ---------------------------------------------------------------------------


class TestOrganisationAssessment:
    """Verify organisation pattern assessment in questions."""

    def test_organisation_category(self, content_lower: str) -> None:
        """Organisation must be a question category."""
        assert "organisation" in content_lower, (
            "Organisation pattern assessment must be in question categories"
        )

    def test_large_direct_pattern_detection(self, content_lower: str) -> None:
        """Detect large direct-pattern epics and suggest features."""
        assert any(
            phrase in content_lower
            for phrase in [
                "8+ tasks",
                "large direct",
                "suggest adding features",
                "suggest features",
            ]
        ), "Large direct-pattern detection must be documented"

    def test_single_feature_detection(self, content_lower: str) -> None:
        """Detect single-feature epics and suggest flattening."""
        assert any(
            phrase in content_lower
            for phrase in [
                "single-feature",
                "single feature",
                "flatten",
                "suggest flattening",
            ]
        ), "Single-feature epic detection must be documented"


# ---------------------------------------------------------------------------
# Test Requirements: Verify all question categories from spec are covered
# ---------------------------------------------------------------------------


class TestQuestionCategories:
    """Verify all question categories are documented."""

    CATEGORIES = [
        "scope",
        "success criteria",
        "acceptance criteria",
        "dependencies",
        "risks",
        "constraints",
        "organisation",
    ]

    @pytest.mark.parametrize("category", CATEGORIES)
    def test_category_present(self, category: str, content_lower: str) -> None:
        """Each question category must be present in the command file."""
        assert category in content_lower, (
            f"Question category '{category}' must be documented"
        )


# ---------------------------------------------------------------------------
# Test Requirements: Verify --focus flag documented for each category
# ---------------------------------------------------------------------------


class TestFocusFlagCategories:
    """Verify --focus flag is documented for key categories."""

    def test_focus_dependencies_category(self, content_lower: str) -> None:
        """--focus must support dependencies category."""
        assert re.search(
            r"--focus\s+dependencies", content_lower
        ), "--focus dependencies must be documented"

    def test_focus_constraints_category(self, content_lower: str) -> None:
        """--focus must support constraints category."""
        assert re.search(
            r"--focus\s+constraints", content_lower
        ), "--focus constraints must be documented"

    def test_focus_organisation_category(self, content_lower: str) -> None:
        """--focus must support organisation category."""
        assert re.search(
            r"--focus\s+organisation", content_lower
        ), "--focus organisation must be documented"
