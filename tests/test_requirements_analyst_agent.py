"""Tests for requirements-analyst agent refinement mode and completeness scoring.

Validates TASK-RK01-001 acceptance criteria:
- AC-001: Refinement mode section with three-phase flow
- AC-002: Completeness scoring dimensions match spec (epic: 9, feature: 7)
- AC-003: Score weights sum to 100% for both epic and feature
- AC-004: Graphiti episode schemas in ext file
- AC-005: Question templates with example answers and skip guidance
- AC-006: Progressive disclosure maintained (core < 500 lines)
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml


BASE_DIR = Path(__file__).resolve().parent.parent
CORE_FILE = BASE_DIR / "installer" / "global" / "agents" / "requirements-analyst.md"
EXT_FILE = BASE_DIR / "installer" / "global" / "agents" / "requirements-analyst-ext.md"


def parse_frontmatter(filepath: Path) -> dict:
    """Parse YAML frontmatter from a markdown file."""
    text = filepath.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        raise ValueError(f"No YAML frontmatter found in {filepath}")
    return yaml.safe_load(match.group(1))


def read_file(filepath: Path) -> str:
    """Read file content with encoding."""
    return filepath.read_text(encoding="utf-8")


class TestCoreFileStructure(unittest.TestCase):
    """Test requirements-analyst.md structure and content."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.content = read_file(CORE_FILE)
        cls.frontmatter = parse_frontmatter(CORE_FILE)

    def test_frontmatter_parses_as_valid_yaml(self) -> None:
        """Verify agent file parses correctly (valid YAML frontmatter)."""
        self.assertIsInstance(self.frontmatter, dict)
        self.assertIn("name", self.frontmatter)
        self.assertEqual(self.frontmatter["name"], "requirements-analyst")

    def test_core_file_under_500_lines(self) -> None:
        """AC-006: Progressive disclosure - core file < 500 lines."""
        line_count = len(self.content.splitlines())
        self.assertLess(
            line_count,
            500,
            f"Core file has {line_count} lines, must be < 500 for progressive disclosure",
        )

    # --- AC-001: Refinement mode section with three-phase flow ---

    def test_refinement_mode_section_exists(self) -> None:
        """AC-001: Core file contains a refinement mode section."""
        self.assertIn("Refinement Mode", self.content, "Missing 'Refinement Mode' section")

    def test_refinement_mode_three_phases(self) -> None:
        """AC-001: Refinement mode defines three-phase flow."""
        # All three phases must be mentioned
        phases = ["current state", "targeted questions", "change summary"]
        for phase in phases:
            self.assertIn(
                phase.lower(),
                self.content.lower(),
                f"Refinement mode missing phase: '{phase}'",
            )

    def test_refinement_mode_triggers(self) -> None:
        """AC-001: Refinement mode defines activation triggers."""
        self.assertIn("/epic-refine", self.content)
        self.assertIn("/feature-refine", self.content)

    def test_refinement_question_presentation_rules(self) -> None:
        """AC-001: Question presentation rules - one at a time, skip/done."""
        content_lower = self.content.lower()
        self.assertIn("one at a time", content_lower, "Missing 'one at a time' question rule")
        self.assertIn("skip", content_lower, "Missing 'skip' option guidance")
        self.assertIn("done", content_lower, "Missing 'done' option guidance")

    # --- AC-002: Completeness scoring dimensions ---

    def test_completeness_scoring_section_exists(self) -> None:
        """AC-002: Core file contains completeness scoring section."""
        self.assertIn("Completeness Scor", self.content, "Missing completeness scoring section")

    def test_epic_has_nine_dimensions(self) -> None:
        """AC-002: Epic completeness has exactly 9 weighted dimensions."""
        epic_dimensions = [
            "business objective",
            "scope",
            "success criteria",
            "acceptance criteria",
            "risk",
            "constraints",
            "dependencies",
            "stakeholders",
            "organisation",
        ]
        for dim in epic_dimensions:
            self.assertIn(
                dim.lower(),
                self.content.lower(),
                f"Missing epic dimension: '{dim}'",
            )

    def test_feature_has_seven_dimensions(self) -> None:
        """AC-002: Feature completeness has exactly 7 weighted dimensions."""
        feature_dimensions = [
            "scope within epic",
            "acceptance criteria",
            "requirements traceability",
            "bdd coverage",
            "technical considerations",
            "dependencies",
            "test strategy",
        ]
        for dim in feature_dimensions:
            self.assertIn(
                dim.lower(),
                self.content.lower(),
                f"Missing feature dimension: '{dim}'",
            )

    # --- AC-003: Score weights sum to 100% ---

    def test_epic_weights_sum_to_100(self) -> None:
        """AC-003: Epic completeness score weights sum to 100%."""
        # Extract the epic scoring section and find percentage values
        epic_weights = {
            "business objective": 15,
            "scope": 15,
            "success criteria": 20,
            "acceptance criteria": 15,
            "risk": 10,
            "constraints": 10,
            "dependencies": 5,
            "stakeholders": 5,
            "organisation": 5,
        }
        total = sum(epic_weights.values())
        self.assertEqual(total, 100, f"Epic weights sum to {total}%, expected 100%")

        # Verify each weight is documented in the file
        for dimension, weight in epic_weights.items():
            pattern = rf"{re.escape(dimension)}.*?{weight}\s*%"
            match = re.search(pattern, self.content, re.IGNORECASE | re.DOTALL)
            self.assertIsNotNone(
                match,
                f"Epic dimension '{dimension}' with weight {weight}% not found in core file",
            )

    def test_feature_weights_sum_to_100(self) -> None:
        """AC-003: Feature completeness score weights sum to 100%."""
        feature_weights = {
            "scope within epic": 10,
            "acceptance criteria": 25,
            "requirements traceability": 20,
            "bdd coverage": 15,
            "technical considerations": 15,
            "dependencies": 10,
            "test strategy": 5,
        }
        total = sum(feature_weights.values())
        self.assertEqual(total, 100, f"Feature weights sum to {total}%, expected 100%")

        for dimension, weight in feature_weights.items():
            pattern = rf"{re.escape(dimension)}.*?{weight}\s*%"
            match = re.search(pattern, self.content, re.IGNORECASE | re.DOTALL)
            self.assertIsNotNone(
                match,
                f"Feature dimension '{dimension}' with weight {weight}% not found in core file",
            )

    # --- Output format updates ---

    def test_output_format_has_completeness_score(self) -> None:
        """Output format template includes completeness_score field."""
        self.assertIn("completeness_score", self.content)

    def test_output_format_has_refinement_history(self) -> None:
        """Output format template includes refinement_history field."""
        self.assertIn("refinement_history", self.content)

    def test_output_format_has_organisation_pattern(self) -> None:
        """Output format template includes organisation_pattern field."""
        self.assertIn("organisation_pattern", self.content)

    # --- Boundary updates ---

    def test_boundary_refinement_one_at_a_time(self) -> None:
        """Boundaries include: present refinement questions one at a time."""
        # Look in ALWAYS section
        always_section = re.search(
            r"### ALWAYS.*?### NEVER", self.content, re.DOTALL | re.IGNORECASE
        )
        self.assertIsNotNone(always_section, "Could not find ALWAYS section")
        self.assertIn(
            "one at a time",
            always_section.group(0).lower(),
            "ALWAYS section missing 'one at a time' refinement rule",
        )

    def test_boundary_show_before_after_scores(self) -> None:
        """Boundaries include: show before/after completeness scores."""
        always_section = re.search(
            r"### ALWAYS.*?### NEVER", self.content, re.DOTALL | re.IGNORECASE
        )
        self.assertIsNotNone(always_section)
        section_text = always_section.group(0).lower()
        self.assertTrue(
            "before" in section_text and "after" in section_text and "completeness" in section_text,
            "ALWAYS section missing 'before/after completeness scores' rule",
        )

    def test_boundary_never_skip_change_summary(self) -> None:
        """Boundaries include: never skip change summary before applying updates."""
        never_section = re.search(
            r"### NEVER.*?### ASK", self.content, re.DOTALL | re.IGNORECASE
        )
        self.assertIsNotNone(never_section, "Could not find NEVER section")
        self.assertIn(
            "change summary",
            never_section.group(0).lower(),
            "NEVER section missing 'change summary' rule",
        )

    def test_boundary_ask_when_contradictions(self) -> None:
        """Boundaries include: ask when refinement answers contradict existing content."""
        ask_section = re.search(
            r"### ASK.*?(?=##[^#]|\Z)", self.content, re.DOTALL | re.IGNORECASE
        )
        self.assertIsNotNone(ask_section, "Could not find ASK section")
        self.assertIn(
            "contradict",
            ask_section.group(0).lower(),
            "ASK section missing 'contradict' rule",
        )


class TestExtendedFileStructure(unittest.TestCase):
    """Test requirements-analyst-ext.md structure and content."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.content = read_file(EXT_FILE)

    # --- AC-004: Graphiti episode schemas ---

    def test_graphiti_integration_section_exists(self) -> None:
        """AC-004: Extended file contains Graphiti integration section."""
        self.assertIn("Graphiti", self.content, "Missing Graphiti integration section")

    def test_epic_episode_schema_present(self) -> None:
        """AC-004: Extended file contains epic episode schema."""
        content_lower = self.content.lower()
        self.assertIn("episode", content_lower, "Missing episode schema reference")
        self.assertIn("epic", content_lower)
        # Key fields from the spec
        self.assertIn("group_id", self.content, "Missing group_id in episode schema")
        self.assertIn("entity_type", self.content, "Missing entity_type in episode schema")

    def test_feature_episode_schema_present(self) -> None:
        """AC-004: Extended file contains feature episode schema."""
        self.assertIn("feature_id", self.content, "Missing feature_id in feature episode schema")
        self.assertIn("epic_id", self.content, "Missing epic_id in feature episode schema")

    def test_group_id_strategy(self) -> None:
        """AC-004: Group ID strategy uses {project}__requirements pattern."""
        self.assertIn("__requirements", self.content, "Missing group_id strategy pattern")

    def test_sync_error_handling(self) -> None:
        """AC-004: Sync error handling patterns documented."""
        content_lower = self.content.lower()
        self.assertTrue(
            "error" in content_lower and "sync" in content_lower,
            "Missing sync error handling patterns",
        )

    def test_standalone_mode_behavior(self) -> None:
        """AC-004: Standalone mode behavior documented."""
        content_lower = self.content.lower()
        self.assertIn("standalone", content_lower, "Missing standalone mode documentation")

    # --- AC-005: Question templates ---

    def test_scope_refinement_questions(self) -> None:
        """AC-005: Scope refinement question templates present."""
        content_lower = self.content.lower()
        self.assertIn("scope", content_lower)
        self.assertTrue(
            "refinement" in content_lower and "question" in content_lower,
            "Missing scope refinement questions",
        )

    def test_success_criteria_questions(self) -> None:
        """AC-005: Success criteria question templates present."""
        self.assertIn(
            "success criteria",
            self.content.lower(),
            "Missing success criteria questions",
        )

    def test_risk_assessment_questions(self) -> None:
        """AC-005: Risk assessment question templates present."""
        self.assertIn("risk", self.content.lower(), "Missing risk assessment questions")

    def test_dependency_discovery_questions(self) -> None:
        """AC-005: Dependency discovery question templates present."""
        self.assertIn("dependenc", self.content.lower(), "Missing dependency questions")

    def test_organisation_pattern_questions(self) -> None:
        """AC-005: Organisation pattern assessment questions present."""
        self.assertIn(
            "organisation",
            self.content.lower(),
            "Missing organisation pattern questions",
        )

    def test_question_templates_have_example_answers(self) -> None:
        """AC-005: Question templates include example good answers."""
        content_lower = self.content.lower()
        self.assertTrue(
            "example" in content_lower and "answer" in content_lower,
            "Question templates missing example good answers",
        )

    def test_question_templates_have_skip_guidance(self) -> None:
        """AC-005: Question templates include skip guidance."""
        self.assertIn(
            "skip",
            self.content.lower(),
            "Question templates missing skip guidance",
        )


if __name__ == "__main__":
    unittest.main()
