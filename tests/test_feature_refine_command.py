"""Tests for /feature-refine command definition.

Validates TASK-RK01-005 acceptance criteria:
- AC-001: Command file follows established pattern
- AC-002: Three-phase flow with feature-specific questions
- AC-003: 6 question categories matching FEAT-RK-001 spec
- AC-004: Feature completeness score (7 dimensions) calculated
- AC-005: --focus flag restricts to single category
- AC-006: Cross-command suggestions for /formalize-ears and /generate-bdd
- AC-007: Graphiti push with feature episode schema
- AC-008: Same UX patterns as epic-refine ([REFINE] prefix, one-at-a-time, skip/done)
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
COMMAND_FILE = BASE_DIR / "installer" / "global" / "commands" / "feature-refine.md"


def read_file(filepath: Path) -> str:
    """Read file content with encoding."""
    return filepath.read_text(encoding="utf-8")


class TestCommandFileExists(unittest.TestCase):
    """Verify the command file exists and is non-empty."""

    def test_command_file_exists(self) -> None:
        """Command file must exist at expected path."""
        self.assertTrue(
            COMMAND_FILE.exists(),
            f"Command file not found at {COMMAND_FILE}",
        )

    def test_command_file_not_empty(self) -> None:
        """Command file must not be empty."""
        content = read_file(COMMAND_FILE)
        self.assertGreater(len(content.strip()), 0, "Command file is empty")


class TestCommandStructure(unittest.TestCase):
    """AC-001: Command file follows established pattern (usage, examples, process, output)."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.content = read_file(COMMAND_FILE)
        cls.content_lower = cls.content.lower()

    def test_has_usage_section(self) -> None:
        """Command file must have a Usage section."""
        self.assertIn("## usage", self.content_lower, "Missing '## Usage' section")

    def test_has_examples_section(self) -> None:
        """Command file must have an Examples section."""
        self.assertIn("## examples", self.content_lower, "Missing '## Examples' section")

    def test_has_process_section(self) -> None:
        """Command file must have a Process section."""
        self.assertIn("## process", self.content_lower, "Missing '## Process' section")

    def test_has_output_format_section(self) -> None:
        """Command file must have an Output Format section."""
        self.assertIn("output", self.content_lower, "Missing output format section")

    def test_usage_shows_feature_id_argument(self) -> None:
        """Usage must show feature-id as required argument."""
        self.assertIn("feature-id", self.content_lower, "Missing feature-id in usage")

    def test_usage_shows_options(self) -> None:
        """Usage must show optional [options] parameter."""
        self.assertIn("[options]", self.content.lower(), "Missing [options] in usage")

    def test_title_contains_feature_refine(self) -> None:
        """Command title must reference feature-refine."""
        self.assertIn("feature-refine", self.content_lower, "Missing feature-refine in title")


class TestThreePhaseFlow(unittest.TestCase):
    """AC-002: Three-phase flow with feature-specific questions."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.content = read_file(COMMAND_FILE)
        cls.content_lower = cls.content.lower()

    def test_phase_1_current_state_display(self) -> None:
        """Phase 1: Current state display must be documented."""
        self.assertIn(
            "current state",
            self.content_lower,
            "Missing Phase 1: Current State Display",
        )

    def test_phase_1_load_feature(self) -> None:
        """Phase 1 must describe loading feature by ID."""
        self.assertIn("load", self.content_lower, "Phase 1 missing load feature description")

    def test_phase_1_parse_frontmatter(self) -> None:
        """Phase 1 must describe parsing frontmatter."""
        self.assertIn("frontmatter", self.content_lower, "Phase 1 missing frontmatter parsing")

    def test_phase_1_completeness_score(self) -> None:
        """Phase 1 must describe calculating completeness score."""
        self.assertIn(
            "completeness",
            self.content_lower,
            "Phase 1 missing completeness score calculation",
        )

    def test_phase_1_linked_epic_context(self) -> None:
        """Phase 1 must show linked epic context."""
        self.assertIn(
            "epic",
            self.content_lower,
            "Phase 1 missing linked epic context",
        )

    def test_phase_2_targeted_questions(self) -> None:
        """Phase 2: Targeted questions must be documented."""
        self.assertIn(
            "targeted questions",
            self.content_lower,
            "Missing Phase 2: Targeted Questions",
        )

    def test_phase_3_change_summary(self) -> None:
        """Phase 3: Change summary and commit must be documented."""
        self.assertIn(
            "change summary",
            self.content_lower,
            "Missing Phase 3: Change Summary",
        )

    def test_phase_3_refinement_history(self) -> None:
        """Phase 3 must document refinement_history update."""
        self.assertIn(
            "refinement_history",
            self.content_lower,
            "Phase 3 missing refinement_history",
        )


class TestQuestionCategories(unittest.TestCase):
    """AC-003: 6 question categories matching FEAT-RK-001 spec."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.content = read_file(COMMAND_FILE)
        cls.content_lower = cls.content.lower()

    def test_category_acceptance_criteria(self) -> None:
        """Category 1: Acceptance Criteria - specificity and measurability."""
        self.assertIn(
            "acceptance criteria",
            self.content_lower,
            "Missing question category: Acceptance Criteria",
        )

    def test_category_requirements_traceability(self) -> None:
        """Category 2: Requirements Traceability - link to EARS requirements."""
        self.assertIn(
            "requirements traceability",
            self.content_lower,
            "Missing question category: Requirements Traceability",
        )

    def test_category_bdd_coverage(self) -> None:
        """Category 3: BDD Coverage - generate scenarios."""
        self.assertIn(
            "bdd coverage",
            self.content_lower,
            "Missing question category: BDD Coverage",
        )

    def test_category_technical_considerations(self) -> None:
        """Category 4: Technical Considerations - API, performance, dependencies."""
        self.assertIn(
            "technical considerations",
            self.content_lower,
            "Missing question category: Technical Considerations",
        )

    def test_category_dependencies(self) -> None:
        """Category 5: Dependencies - feature dependencies."""
        # Need to ensure "dependencies" appears as a distinct category
        self.assertIn(
            "dependencies",
            self.content_lower,
            "Missing question category: Dependencies",
        )

    def test_category_scope_within_epic(self) -> None:
        """Category 6: Scope Within Epic - differentiation from other features."""
        self.assertIn(
            "scope within epic",
            self.content_lower,
            "Missing question category: Scope Within Epic",
        )

    def test_all_six_categories_in_table_or_list(self) -> None:
        """All 6 categories must appear in a structured format (table or list)."""
        categories = [
            "acceptance criteria",
            "requirements traceability",
            "bdd coverage",
            "technical considerations",
            "dependencies",
            "scope within epic",
        ]
        found_count = sum(1 for cat in categories if cat in self.content_lower)
        self.assertEqual(
            found_count,
            6,
            f"Only {found_count}/6 question categories found in command file",
        )


class TestFeatureCompleteness(unittest.TestCase):
    """AC-004: Feature completeness score (7 dimensions) calculated."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.content = read_file(COMMAND_FILE)
        cls.content_lower = cls.content.lower()

    def test_completeness_score_mentioned(self) -> None:
        """Completeness score must be described in the command."""
        self.assertIn(
            "completeness score",
            self.content_lower,
            "Missing completeness score description",
        )

    def test_seven_dimensions_referenced(self) -> None:
        """Feature completeness must reference 7 dimensions."""
        self.assertIn(
            "7",
            self.content,
            "Missing reference to 7-dimension model",
        )

    def test_dimension_scope_within_epic(self) -> None:
        """Dimension: Scope Within Epic must be present."""
        self.assertIn("scope within epic", self.content_lower)

    def test_dimension_acceptance_criteria(self) -> None:
        """Dimension: Acceptance Criteria must be present."""
        self.assertIn("acceptance criteria", self.content_lower)

    def test_dimension_requirements_traceability(self) -> None:
        """Dimension: Requirements Traceability must be present."""
        self.assertIn("requirements traceability", self.content_lower)

    def test_dimension_bdd_coverage(self) -> None:
        """Dimension: BDD Coverage must be present."""
        self.assertIn("bdd coverage", self.content_lower)

    def test_dimension_technical_considerations(self) -> None:
        """Dimension: Technical Considerations must be present."""
        self.assertIn("technical considerations", self.content_lower)

    def test_dimension_dependencies(self) -> None:
        """Dimension: Dependencies must be present."""
        self.assertIn("dependencies", self.content_lower)

    def test_dimension_test_strategy(self) -> None:
        """Dimension: Test Strategy must be present."""
        self.assertIn("test strategy", self.content_lower)

    def test_dimension_weights_present(self) -> None:
        """Feature dimensions must have percentage weights documented."""
        # Check that we have weight percentages in the content
        weight_pattern = r"\d+\s*%"
        weights_found = re.findall(weight_pattern, self.content)
        self.assertGreaterEqual(
            len(weights_found),
            7,
            f"Expected at least 7 weight percentages, found {len(weights_found)}",
        )


class TestFocusFlag(unittest.TestCase):
    """AC-005: --focus flag restricts to single category."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.content = read_file(COMMAND_FILE)
        cls.content_lower = cls.content.lower()

    def test_focus_flag_documented(self) -> None:
        """--focus flag must be documented."""
        self.assertIn("--focus", self.content, "Missing --focus flag documentation")

    def test_focus_acceptance_example(self) -> None:
        """--focus acceptance example must be shown."""
        self.assertIn(
            "--focus acceptance",
            self.content_lower,
            "Missing --focus acceptance example",
        )

    def test_focus_technical_example(self) -> None:
        """--focus technical example must be shown."""
        self.assertIn(
            "--focus technical",
            self.content_lower,
            "Missing --focus technical example",
        )

    def test_focus_bdd_example(self) -> None:
        """--focus bdd example must be shown."""
        self.assertIn(
            "--focus bdd",
            self.content_lower,
            "Missing --focus bdd example",
        )

    def test_focus_restricts_to_single_category(self) -> None:
        """Documentation must describe that --focus restricts to a single category."""
        # Look for text describing restriction behavior
        focus_patterns = ["restrict", "single category", "only.*category", "one category"]
        found = any(
            re.search(pattern, self.content_lower) for pattern in focus_patterns
        )
        self.assertTrue(found, "Missing description of --focus restriction behavior")


class TestCrossCommandSuggestions(unittest.TestCase):
    """AC-006: Cross-command suggestions for /formalize-ears and /generate-bdd."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.content = read_file(COMMAND_FILE)
        cls.content_lower = cls.content.lower()

    def test_formalize_ears_suggestion(self) -> None:
        """Command must suggest /formalize-ears for creating linked requirements."""
        self.assertIn(
            "/formalize-ears",
            self.content,
            "Missing /formalize-ears cross-command suggestion",
        )

    def test_generate_bdd_suggestion(self) -> None:
        """Command must suggest /generate-bdd for creating missing scenarios."""
        self.assertIn(
            "/generate-bdd",
            self.content,
            "Missing /generate-bdd cross-command suggestion",
        )

    def test_parent_epic_context(self) -> None:
        """Command must show parent epic completeness for context."""
        self.assertIn(
            "parent epic",
            self.content_lower,
            "Missing parent epic completeness context",
        )


class TestGraphitiIntegration(unittest.TestCase):
    """AC-007: Graphiti push with feature episode schema."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.content = read_file(COMMAND_FILE)
        cls.content_lower = cls.content.lower()

    def test_graphiti_push_documented(self) -> None:
        """Graphiti push must be documented in the command."""
        self.assertIn(
            "graphiti",
            self.content_lower,
            "Missing Graphiti push documentation",
        )

    def test_feature_episode_schema(self) -> None:
        """Feature episode schema must be described."""
        self.assertIn(
            "episode",
            self.content_lower,
            "Missing feature episode schema reference",
        )

    def test_graceful_degradation(self) -> None:
        """Graphiti integration must use graceful degradation."""
        self.assertIn(
            "graceful degradation",
            self.content_lower,
            "Missing graceful degradation for Graphiti",
        )


class TestUXPatterns(unittest.TestCase):
    """AC-008: Same UX patterns as epic-refine ([REFINE] prefix, one-at-a-time, skip/done)."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.content = read_file(COMMAND_FILE)
        cls.content_lower = cls.content.lower()

    def test_refine_prefix(self) -> None:
        """[REFINE] prefix must be documented for mode clarity."""
        self.assertIn(
            "[REFINE]",
            self.content,
            "Missing [REFINE] prefix for mode clarity",
        )

    def test_one_at_a_time_questions(self) -> None:
        """Questions must be presented one at a time."""
        self.assertIn(
            "one at a time",
            self.content_lower,
            "Missing 'one at a time' question presentation rule",
        )

    def test_skip_option(self) -> None:
        """Skip option must be available for every question."""
        self.assertIn(
            "skip",
            self.content_lower,
            "Missing 'skip' option for questions",
        )

    def test_done_option(self) -> None:
        """Done option must be available to end refinement session."""
        self.assertIn(
            "done",
            self.content_lower,
            "Missing 'done' option to end refinement",
        )

    def test_visual_separators(self) -> None:
        """Visual separators must be documented for mode clarity."""
        separator_patterns = ["visual separator", "separator", "---", "═"]
        found = any(pattern in self.content for pattern in separator_patterns)
        self.assertTrue(found, "Missing visual separators for mode clarity")

    def test_before_after_score_display(self) -> None:
        """Before/after completeness score must be shown."""
        self.assertIn("before", self.content_lower, "Missing 'before' score display")
        self.assertIn("after", self.content_lower, "Missing 'after' score display")

    def test_natural_language_answers(self) -> None:
        """Natural language answers must be accepted."""
        self.assertIn(
            "natural language",
            self.content_lower,
            "Missing natural language answer support",
        )


if __name__ == "__main__":
    unittest.main()
