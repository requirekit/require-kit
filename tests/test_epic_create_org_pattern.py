"""Tests for TASK-RK01-002: Organisation Pattern Schema in Epic Create Command.

Validates that installer/global/commands/epic-create.md contains the required
organisation pattern schema fields, documentation, validation rules, and examples
as specified by the acceptance criteria.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

EPIC_CREATE_PATH = (
    Path(__file__).resolve().parents[1]
    / "installer"
    / "global"
    / "commands"
    / "epic-create.md"
)


@pytest.fixture(scope="module")
def epic_create_content() -> str:
    """Read the full epic-create.md file content."""
    if not EPIC_CREATE_PATH.exists():
        pytest.fail(f"epic-create.md not found at {EPIC_CREATE_PATH}")
    return EPIC_CREATE_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def frontmatter_yaml_blocks(epic_create_content: str) -> list[str]:
    """Extract all YAML code blocks from the epic-create.md file."""
    # Match ```yaml ... ``` or ```yml ... ``` blocks
    pattern = re.compile(r"```ya?ml\s*\n(.*?)```", re.DOTALL)
    return pattern.findall(epic_create_content)


@pytest.fixture(scope="module")
def epic_structure_yaml(epic_create_content: str) -> str:
    """Extract the Epic Structure frontmatter YAML block (the one with id: EPIC-XXX)."""
    pattern = re.compile(r"---\s*\n(id:\s*EPIC-.*?)---", re.DOTALL)
    matches = pattern.findall(epic_create_content)
    if not matches:
        pytest.fail("No epic structure frontmatter block found in epic-create.md")
    # Return the longest match (most complete frontmatter)
    return max(matches, key=len)


# ---------------------------------------------------------------------------
# AC-001: Epic frontmatter includes organisation_pattern, direct_tasks,
#         graphiti_synced fields
# ---------------------------------------------------------------------------


class TestFrontmatterFields:
    """Verify the epic frontmatter template includes required new fields."""

    def test_organisation_pattern_field_in_frontmatter(
        self, epic_structure_yaml: str
    ) -> None:
        """The frontmatter template must include an organisation_pattern field."""
        assert "organisation_pattern" in epic_structure_yaml, (
            "Frontmatter template must include 'organisation_pattern' field"
        )

    def test_direct_tasks_field_in_frontmatter(
        self, epic_structure_yaml: str
    ) -> None:
        """The frontmatter template must include a direct_tasks field."""
        assert "direct_tasks" in epic_structure_yaml, (
            "Frontmatter template must include 'direct_tasks' field"
        )

    def test_graphiti_synced_field_in_frontmatter(
        self, epic_structure_yaml: str
    ) -> None:
        """The frontmatter template must include a graphiti_synced field."""
        assert "graphiti_synced" in epic_structure_yaml, (
            "Frontmatter template must include 'graphiti_synced' field"
        )

    def test_last_graphiti_sync_field_in_frontmatter(
        self, epic_structure_yaml: str
    ) -> None:
        """The frontmatter template must include a last_graphiti_sync field."""
        assert "last_graphiti_sync" in epic_structure_yaml, (
            "Frontmatter template must include 'last_graphiti_sync' field"
        )

    def test_completeness_score_field_in_frontmatter(
        self, epic_structure_yaml: str
    ) -> None:
        """The frontmatter template must include a completeness_score field."""
        assert "completeness_score" in epic_structure_yaml, (
            "Frontmatter template must include 'completeness_score' field"
        )

    def test_frontmatter_is_valid_yaml(self, epic_structure_yaml: str) -> None:
        """The frontmatter template must be parseable as valid YAML."""
        try:
            parsed = yaml.safe_load(epic_structure_yaml)
        except yaml.YAMLError as exc:
            pytest.fail(f"Frontmatter is not valid YAML: {exc}")
        assert isinstance(parsed, dict), "Parsed frontmatter must be a dict"


# ---------------------------------------------------------------------------
# AC-002: Default organisation_pattern is 'features' (backward compatible)
# ---------------------------------------------------------------------------


class TestDefaultPattern:
    """Verify default organisation_pattern is 'features'."""

    def test_default_pattern_is_features(self, epic_structure_yaml: str) -> None:
        """The default value for organisation_pattern must be 'features'."""
        parsed = yaml.safe_load(epic_structure_yaml)
        assert parsed is not None
        assert parsed.get("organisation_pattern") == "features", (
            "Default organisation_pattern must be 'features' for backward compatibility"
        )


# ---------------------------------------------------------------------------
# AC-003: Three patterns documented with when-to-use guidance
# ---------------------------------------------------------------------------


class TestPatternDocumentation:
    """Verify all three organisation patterns are documented."""

    def test_direct_pattern_documented(self, epic_create_content: str) -> None:
        """The 'direct' pattern must be documented."""
        # Look for 'direct' pattern described in context of organisation
        assert re.search(
            r"(?i)\bdirect\b.*pattern|pattern.*\bdirect\b", epic_create_content
        ), "The 'direct' organisation pattern must be documented"

    def test_features_pattern_documented(self, epic_create_content: str) -> None:
        """The 'features' pattern must be documented."""
        assert re.search(
            r"(?i)\bfeatures?\b.*pattern|pattern.*\bfeatures?\b", epic_create_content
        ), "The 'features' organisation pattern must be documented"

    def test_mixed_pattern_documented(self, epic_create_content: str) -> None:
        """The 'mixed' pattern must be documented."""
        assert re.search(
            r"(?i)\bmixed\b.*pattern|pattern.*\bmixed\b", epic_create_content
        ), "The 'mixed' organisation pattern must be documented"

    def test_when_to_use_direct(self, epic_create_content: str) -> None:
        """Guidance for when to use 'direct' pattern must be present."""
        # Direct should mention small epics or 3-5 tasks
        lower = epic_create_content.lower()
        assert any(
            phrase in lower
            for phrase in ["3-5 tasks", "small epic", "bug fix", "technical debt"]
        ), "When-to-use guidance for 'direct' pattern must be present"

    def test_when_to_use_features(self, epic_create_content: str) -> None:
        """Guidance for when to use 'features' pattern must be present."""
        lower = epic_create_content.lower()
        assert any(
            phrase in lower
            for phrase in ["10+ tasks", "large epic", "complex", "team coordination"]
        ), "When-to-use guidance for 'features' pattern must be present"

    def test_when_to_use_mixed(self, epic_create_content: str) -> None:
        """Guidance for when to use 'mixed' pattern must be present."""
        lower = epic_create_content.lower()
        assert any(
            phrase in lower
            for phrase in ["evolving", "both features and", "miscellaneous", "mixed"]
        ), "When-to-use guidance for 'mixed' pattern must be present"


# ---------------------------------------------------------------------------
# AC-004: Validation rejects invalid pattern values
# ---------------------------------------------------------------------------


class TestValidationRules:
    """Verify validation rules are documented."""

    def test_valid_patterns_specified(self, epic_create_content: str) -> None:
        """Validation must specify the valid pattern values: direct, features, mixed."""
        lower = epic_create_content.lower()
        # All three valid values must appear in a validation context
        assert "direct" in lower, "Validation must mention 'direct' as valid value"
        assert "features" in lower, "Validation must mention 'features' as valid value"
        assert "mixed" in lower, "Validation must mention 'mixed' as valid value"

    def test_validation_section_exists(self, epic_create_content: str) -> None:
        """A validation section must exist documenting pattern validation."""
        assert re.search(
            r"(?i)valid.*organisation_pattern|organisation_pattern.*valid",
            epic_create_content,
        ), "Validation rules for organisation_pattern must be documented"


# ---------------------------------------------------------------------------
# AC-005: Mixed pattern produces a warning
# ---------------------------------------------------------------------------


class TestMixedPatternWarning:
    """Verify mixed pattern warning is documented."""

    def test_mixed_pattern_warning_documented(self, epic_create_content: str) -> None:
        """Documentation must mention a warning for mixed pattern selection."""
        lower = epic_create_content.lower()
        # Must mention warning in relation to mixed pattern
        assert any(
            phrase in lower
            for phrase in [
                "warn",
                "warning",
                "⚠",
                "caution",
            ]
        ) and "mixed" in lower, (
            "A warning for mixed pattern selection must be documented"
        )


# ---------------------------------------------------------------------------
# AC-006: Graphiti push step documented with graceful degradation
# ---------------------------------------------------------------------------


class TestGraphitiPushStep:
    """Verify Graphiti push step is documented."""

    def test_graphiti_push_step_present(self, epic_create_content: str) -> None:
        """A Graphiti push step must be documented in the creation process."""
        lower = epic_create_content.lower()
        assert "graphiti" in lower, (
            "Graphiti push step must be documented"
        )

    def test_graphiti_graceful_degradation(self, epic_create_content: str) -> None:
        """Graphiti integration must document graceful failure handling."""
        lower = epic_create_content.lower()
        assert any(
            phrase in lower
            for phrase in [
                "graceful",
                "markdown always saved",
                "fallback",
                "optional",
                "if enabled",
            ]
        ), "Graphiti integration must document graceful failure/degradation"


# ---------------------------------------------------------------------------
# AC-007: Examples section includes --pattern usage
# ---------------------------------------------------------------------------


class TestPatternExamples:
    """Verify examples include --pattern flag usage."""

    def test_pattern_flag_in_examples(self, epic_create_content: str) -> None:
        """Examples must include --pattern flag usage."""
        assert "--pattern" in epic_create_content, (
            "Examples must include '--pattern' flag usage"
        )

    def test_pattern_direct_example(self, epic_create_content: str) -> None:
        """An example using --pattern direct must be present."""
        assert re.search(
            r"--pattern\s+direct", epic_create_content
        ), "An example with '--pattern direct' must be present"

    def test_epic_create_with_pattern_example(self, epic_create_content: str) -> None:
        """An /epic-create example using --pattern must be present."""
        assert re.search(
            r"/epic-create.*--pattern|epic-create.*--pattern",
            epic_create_content,
        ), "An /epic-create example using --pattern must be present"


# ---------------------------------------------------------------------------
# Test Requirements: Verify frontmatter template generates valid YAML
# ---------------------------------------------------------------------------


class TestYAMLValidity:
    """Ensure all YAML blocks in the document are valid."""

    def test_at_least_one_yaml_block(self, frontmatter_yaml_blocks: list[str]) -> None:
        """The document must contain at least one YAML code block."""
        assert len(frontmatter_yaml_blocks) > 0, (
            "epic-create.md must contain at least one YAML code block"
        )

    def test_yaml_blocks_are_parseable(
        self, frontmatter_yaml_blocks: list[str]
    ) -> None:
        """All YAML code blocks must be parseable."""
        for i, block in enumerate(frontmatter_yaml_blocks):
            try:
                yaml.safe_load(block)
            except yaml.YAMLError as exc:
                pytest.fail(f"YAML block {i} is not valid YAML: {exc}")


# ---------------------------------------------------------------------------
# Test Requirements: Verify all three patterns documented
# ---------------------------------------------------------------------------


class TestAllPatternsComplete:
    """Comprehensive check that all three patterns have full documentation."""

    def test_direct_pattern_has_example_hierarchy(
        self, epic_create_content: str
    ) -> None:
        """Direct pattern must show example hierarchy (EPIC → TASK)."""
        assert re.search(
            r"EPIC.*→.*TASK|EPIC.*task.*direct|direct.*EPIC.*TASK",
            epic_create_content,
            re.IGNORECASE,
        ), "Direct pattern must show EPIC → TASK hierarchy example"

    def test_features_pattern_has_example_hierarchy(
        self, epic_create_content: str
    ) -> None:
        """Features pattern must show example hierarchy (EPIC → FEATURE → TASK)."""
        assert re.search(
            r"EPIC.*→.*FEATURE.*→.*TASK|EPIC.*FEAT.*TASK",
            epic_create_content,
            re.IGNORECASE,
        ), "Features pattern must show EPIC → FEATURE → TASK hierarchy example"

    def test_pm_tool_mapping_for_patterns(self, epic_create_content: str) -> None:
        """PM tool mapping must cover organisation patterns."""
        lower = epic_create_content.lower()
        # Must mention PM tool mapping in context of patterns
        assert "jira" in lower, "PM tool mapping for Jira must be present"
        assert "linear" in lower, "PM tool mapping for Linear must be present"
