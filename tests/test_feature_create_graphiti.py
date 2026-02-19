"""Tests for TASK-RK01-009: Update Feature Create with Graphiti Push and Completeness Fields.

Validates that installer/global/commands/feature-create.md contains the required
Graphiti integration fields, process documentation, output format, and validation rules
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

FEATURE_CREATE_PATH = (
    Path(__file__).resolve().parents[1]
    / "installer"
    / "global"
    / "commands"
    / "feature-create.md"
)


@pytest.fixture(scope="module")
def feature_create_content() -> str:
    """Read the full feature-create.md file content."""
    if not FEATURE_CREATE_PATH.exists():
        pytest.fail(f"feature-create.md not found at {FEATURE_CREATE_PATH}")
    return FEATURE_CREATE_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def feature_structure_yaml(feature_create_content: str) -> str:
    """Extract the Feature Structure frontmatter YAML block (the one with id: FEAT-XXX)."""
    pattern = re.compile(r"---\s*\n(id:\s*FEAT-.*?)---", re.DOTALL)
    matches = pattern.findall(feature_create_content)
    if not matches:
        pytest.fail("No feature structure frontmatter block found in feature-create.md")
    # Return the longest match (most complete frontmatter)
    return max(matches, key=len)


# ---------------------------------------------------------------------------
# AC-001: Frontmatter template includes graphiti_synced, last_graphiti_sync,
#         completeness_score
# ---------------------------------------------------------------------------

def test_frontmatter_has_graphiti_synced_field(feature_structure_yaml: str):
    """Verify that the feature frontmatter template includes graphiti_synced field."""
    assert "graphiti_synced:" in feature_structure_yaml, (
        "Feature frontmatter template must include 'graphiti_synced' field"
    )
    # Verify the field has the correct default value
    assert "graphiti_synced: false" in feature_structure_yaml, (
        "graphiti_synced field must default to 'false'"
    )


def test_frontmatter_has_last_graphiti_sync_field(feature_structure_yaml: str):
    """Verify that the feature frontmatter template includes last_graphiti_sync field."""
    assert "last_graphiti_sync:" in feature_structure_yaml, (
        "Feature frontmatter template must include 'last_graphiti_sync' field"
    )
    # Verify the field has the correct default value
    assert "last_graphiti_sync: null" in feature_structure_yaml, (
        "last_graphiti_sync field must default to 'null'"
    )


def test_frontmatter_has_completeness_score_field(feature_structure_yaml: str):
    """Verify that the feature frontmatter template includes completeness_score field."""
    assert "completeness_score:" in feature_structure_yaml, (
        "Feature frontmatter template must include 'completeness_score' field"
    )
    # Verify the field has the correct default value
    assert "completeness_score: 0" in feature_structure_yaml, (
        "completeness_score field must default to '0'"
    )


def test_frontmatter_yaml_is_valid(feature_structure_yaml: str):
    """Verify that the frontmatter YAML is valid and parseable."""
    try:
        parsed = yaml.safe_load(feature_structure_yaml)
        assert parsed is not None, "Frontmatter YAML should not be empty"
        assert isinstance(parsed, dict), "Frontmatter YAML should be a dictionary"
    except yaml.YAMLError as e:
        pytest.fail(f"Frontmatter YAML is invalid: {e}")


def test_frontmatter_graphiti_fields_structure(feature_structure_yaml: str):
    """Verify the structure and types of Graphiti-related fields in frontmatter."""
    parsed = yaml.safe_load(feature_structure_yaml)

    # Check graphiti_synced
    assert "graphiti_synced" in parsed, "Missing graphiti_synced field"
    assert isinstance(parsed["graphiti_synced"], bool), (
        "graphiti_synced should be a boolean"
    )
    assert parsed["graphiti_synced"] is False, (
        "graphiti_synced should default to False"
    )

    # Check last_graphiti_sync
    assert "last_graphiti_sync" in parsed, "Missing last_graphiti_sync field"
    assert parsed["last_graphiti_sync"] is None, (
        "last_graphiti_sync should default to None/null"
    )

    # Check completeness_score
    assert "completeness_score" in parsed, "Missing completeness_score field"
    assert isinstance(parsed["completeness_score"], int), (
        "completeness_score should be an integer"
    )
    assert parsed["completeness_score"] == 0, (
        "completeness_score should default to 0"
    )


# ---------------------------------------------------------------------------
# AC-002: Process section includes Graphiti push step with graceful degradation
# ---------------------------------------------------------------------------

def test_process_section_exists(feature_create_content: str):
    """Verify that the Process section exists in the documentation."""
    assert "## Process" in feature_create_content, (
        "feature-create.md must have a '## Process' section"
    )


def test_process_includes_graphiti_push_step(feature_create_content: str):
    """Verify that the Process section includes a Graphiti push step."""
    # Find the Process section
    process_match = re.search(
        r"## Process\s*\n(.*?)(?=\n##|\Z)",
        feature_create_content,
        re.DOTALL
    )
    assert process_match, "Could not find Process section"
    process_section = process_match.group(1)

    # Check for Graphiti push step
    assert "Graphiti Push" in process_section, (
        "Process section must include 'Graphiti Push' step"
    )
    assert "if enabled" in process_section, (
        "Graphiti Push step should be conditional (if enabled)"
    )


def test_graphiti_push_has_graceful_degradation(feature_create_content: str):
    """Verify that Graphiti push step documents graceful degradation."""
    # Find the Process section
    process_match = re.search(
        r"## Process\s*\n(.*?)(?=\n##|\Z)",
        feature_create_content,
        re.DOTALL
    )
    assert process_match, "Could not find Process section"
    process_section = process_match.group(1)

    # Check for graceful degradation language
    assert "graceful degradation" in process_section.lower(), (
        "Graphiti Push step must mention 'graceful degradation'"
    )
    assert "markdown is still saved" in process_section.lower() or \
           "markdown always saved" in process_section.lower(), (
        "Must document that markdown is saved regardless of Graphiti status"
    )
    assert "creation succeeds" in process_section.lower(), (
        "Must document that creation succeeds even if Graphiti fails"
    )


def test_graphiti_step_documents_error_handling(feature_create_content: str):
    """Verify that error handling for Graphiti push is documented."""
    # Find the Process section
    process_match = re.search(
        r"## Process\s*\n(.*?)(?=\n##|\Z)",
        feature_create_content,
        re.DOTALL
    )
    assert process_match, "Could not find Process section"
    process_section = process_match.group(1)

    # Check for error handling documentation
    assert "unavailable" in process_section.lower() or \
           "not configured" in process_section.lower(), (
        "Must document behavior when Graphiti is unavailable or not configured"
    )


def test_creation_step_documents_markdown_always_saved(feature_create_content: str):
    """Verify that the Creation step documents that markdown is always saved."""
    # Find the Process section
    process_match = re.search(
        r"## Process\s*\n(.*?)(?=\n##|\Z)",
        feature_create_content,
        re.DOTALL
    )
    assert process_match, "Could not find Process section"
    process_section = process_match.group(1)

    # The Creation step should mention that markdown is always saved
    creation_match = re.search(
        r"\*\*Creation\*\*:.*?(?=\n\d+\.|\Z)",
        process_section,
        re.DOTALL
    )
    assert creation_match, "Could not find Creation step in Process section"
    creation_step = creation_match.group(0)

    assert "markdown always saved" in creation_step.lower() or \
           "always saved regardless" in creation_step.lower(), (
        "Creation step must document that markdown is always saved"
    )


# ---------------------------------------------------------------------------
# AC-003: Output format shows Graphiti status
# ---------------------------------------------------------------------------

def test_output_format_section_exists(feature_create_content: str):
    """Verify that the Output Format section exists."""
    assert "## Output Format" in feature_create_content, (
        "feature-create.md must have an '## Output Format' section"
    )


def test_output_format_includes_graphiti_status(feature_create_content: str):
    """Verify that the Output Format section includes Graphiti status."""
    # Find the Output Format section
    output_match = re.search(
        r"## Output Format\s*\n(.*?)(?=\n##|\Z)",
        feature_create_content,
        re.DOTALL
    )
    assert output_match, "Could not find Output Format section"
    output_section = output_match.group(1)

    # Check for Graphiti status in output
    assert "Graphiti Status" in output_section or \
           "Graphiti Integration" in output_section, (
        "Output Format must include Graphiti status display"
    )


def test_output_format_shows_completeness_score(feature_create_content: str):
    """Verify that the Output Format section shows completeness score."""
    # Find the Output Format section
    output_match = re.search(
        r"## Output Format\s*\n(.*?)(?=\n##|\Z)",
        feature_create_content,
        re.DOTALL
    )
    assert output_match, "Could not find Output Format section"
    output_section = output_match.group(1)

    # Check for completeness score display
    assert "Completeness Score" in output_section or \
           "completeness" in output_section.lower(), (
        "Output Format must display completeness score"
    )


def test_output_format_graphiti_examples(feature_create_content: str):
    """Verify that Output Format includes examples with Graphiti status."""
    # Find the Output Format section
    output_match = re.search(
        r"## Output Format\s*\n(.*?)(?=\n##|\Z)",
        feature_create_content,
        re.DOTALL
    )
    assert output_match, "Could not find Output Format section"
    output_section = output_match.group(1)

    # Look for emoji or marker for Graphiti section in example output
    graphiti_markers = ["🔮", "Graphiti"]
    has_marker = any(marker in output_section for marker in graphiti_markers)
    assert has_marker, (
        "Output Format examples should include Graphiti status marker"
    )


# ---------------------------------------------------------------------------
# AC-004: Validation rules documented for epic association
# ---------------------------------------------------------------------------

def test_validation_section_exists(feature_create_content: str):
    """Verify that the Validation section exists."""
    assert "## Validation" in feature_create_content, (
        "feature-create.md must have a '## Validation' section"
    )


def test_validation_requires_epic(feature_create_content: str):
    """Verify that validation documents epic requirement."""
    # Find the Validation section
    validation_match = re.search(
        r"## Validation\s*\n(.*?)(?=\n##|\Z)",
        feature_create_content,
        re.DOTALL
    )
    assert validation_match, "Could not find Validation section"
    validation_section = validation_match.group(1)

    # Check that epic is required
    assert "Epic must exist" in validation_section or \
           "epic must exist" in validation_section.lower(), (
        "Validation must document that epic must exist"
    )


def test_validation_documents_epic_always_required(feature_create_content: str):
    """Verify that validation documents features always belong to epics (REQ-004)."""
    # Find the Validation section
    validation_match = re.search(
        r"## Validation\s*\n(.*?)(?=\n##|\Z)",
        feature_create_content,
        re.DOTALL
    )
    assert validation_match, "Could not find Validation section"
    validation_section = validation_match.group(1)

    # Check that features always belong to epics
    assert "features always belong to epics" in validation_section.lower() or \
           "REQ-004" in validation_section, (
        "Validation must document that features always belong to epics (REQ-004)"
    )


def test_validation_epic_parameter_required(feature_create_content: str):
    """Verify that validation requires epic parameter."""
    # Find the Validation section
    validation_match = re.search(
        r"## Validation\s*\n(.*?)(?=\n##|\Z)",
        feature_create_content,
        re.DOTALL
    )
    assert validation_match, "Could not find Validation section"
    validation_section = validation_match.group(1)

    # Check that epic parameter is required
    assert "Epic parameter required" in validation_section or \
           "epic parameter" in validation_section.lower() or \
           "cannot create feature without epic" in validation_section.lower(), (
        "Validation must document that epic parameter is required"
    )


# ---------------------------------------------------------------------------
# Integration Tests: Verify all components work together
# ---------------------------------------------------------------------------

def test_all_graphiti_components_present(feature_create_content: str):
    """Verify that all Graphiti-related components are present and consistent."""
    # Check frontmatter
    assert "graphiti_synced:" in feature_create_content
    assert "last_graphiti_sync:" in feature_create_content
    assert "completeness_score:" in feature_create_content

    # Check Process section
    assert "Graphiti Push" in feature_create_content

    # Check Output Format
    assert "Graphiti" in feature_create_content

    # Check Validation
    assert "Epic must exist" in feature_create_content


def test_documentation_consistency(feature_create_content: str):
    """Verify consistency between different sections."""
    # All mentions of Graphiti should be consistent
    graphiti_mentions = re.findall(
        r"(Graphiti\s+\w+)",
        feature_create_content,
        re.IGNORECASE
    )

    # Should have multiple mentions (frontmatter, process, output)
    assert len(graphiti_mentions) >= 3, (
        "Graphiti should be mentioned in multiple sections"
    )


def test_graceful_degradation_philosophy_consistent(feature_create_content: str):
    """Verify that graceful degradation philosophy is consistently applied."""
    # Both Creation and Graphiti Push should mention graceful handling
    assert "markdown always saved" in feature_create_content.lower() or \
           "markdown is still saved" in feature_create_content.lower(), (
        "Documentation must consistently emphasize that markdown is always saved"
    )

    assert "creation succeeds" in feature_create_content.lower(), (
        "Documentation must emphasize that creation always succeeds"
    )
