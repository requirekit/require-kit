"""Shared fixtures and helpers for integration tests.

Provides common fixtures for loading command specifications, parsing
frontmatter, constructing sample markdown, and configuring Graphiti
settings used across all integration test modules.
"""

from __future__ import annotations

import re
import textwrap
from pathlib import Path
from typing import Any

import pytest
import yaml


# ---------------------------------------------------------------------------
# Path constants
# ---------------------------------------------------------------------------

_WORKTREE_ROOT = Path(__file__).resolve().parents[2]
_COMMANDS_DIR = _WORKTREE_ROOT / "installer" / "global" / "commands"
_CONFIG_DIR = _WORKTREE_ROOT / "installer" / "global" / "config"

# ---------------------------------------------------------------------------
# Command-spec loading fixtures
# ---------------------------------------------------------------------------


def _load_command(name: str) -> str:
    """Load a command specification markdown file by name.

    Args:
        name: Command filename without extension (e.g. ``'epic-refine'``).

    Returns:
        Full text content of the command markdown file.

    Raises:
        FileNotFoundError: If the command file does not exist.
    """
    path = _COMMANDS_DIR / f"{name}.md"
    if not path.exists():
        raise FileNotFoundError(f"Command spec not found: {path}")
    return path.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def epic_refine_spec() -> str:
    """Full text of installer/global/commands/epic-refine.md."""
    return _load_command("epic-refine")


@pytest.fixture(scope="session")
def feature_refine_spec() -> str:
    """Full text of installer/global/commands/feature-refine.md."""
    return _load_command("feature-refine")


@pytest.fixture(scope="session")
def epic_create_spec() -> str:
    """Full text of installer/global/commands/epic-create.md."""
    return _load_command("epic-create")


@pytest.fixture(scope="session")
def feature_create_spec() -> str:
    """Full text of installer/global/commands/feature-create.md."""
    return _load_command("feature-create")


@pytest.fixture(scope="session")
def hierarchy_view_spec() -> str:
    """Full text of installer/global/commands/hierarchy-view.md."""
    return _load_command("hierarchy-view")


@pytest.fixture(scope="session")
def requirekit_sync_spec() -> str:
    """Full text of installer/global/commands/requirekit-sync.md."""
    return _load_command("requirekit-sync")


@pytest.fixture(scope="session")
def epic_status_spec() -> str:
    """Full text of installer/global/commands/epic-status.md."""
    return _load_command("epic-status")


# ---------------------------------------------------------------------------
# Graphiti configuration fixture
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def graphiti_config() -> dict[str, Any]:
    """Parsed graphiti.yaml configuration."""
    path = _CONFIG_DIR / "graphiti.yaml"
    if not path.exists():
        pytest.fail(f"graphiti.yaml not found at {path}")
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if raw is None or "graphiti" not in raw:
        pytest.fail("graphiti.yaml must contain a 'graphiti' key")
    return raw["graphiti"]


# ---------------------------------------------------------------------------
# Frontmatter extraction helpers
# ---------------------------------------------------------------------------


def extract_frontmatter_block(content: str, id_prefix: str = "EPIC-") -> str:
    """Extract the YAML frontmatter block that starts with a given id prefix.

    Searches for ``---\\nid: <prefix>...---`` blocks and returns the longest
    match (the most complete frontmatter template).

    Args:
        content: Full markdown text.
        id_prefix: Prefix to look for in the ``id:`` field (default ``EPIC-``).

    Returns:
        Raw YAML text of the matched block (without the ``---`` delimiters).

    Raises:
        ValueError: If no matching frontmatter block is found.
    """
    pattern = re.compile(rf"---\s*\n(id:\s*{re.escape(id_prefix)}.*?)---", re.DOTALL)
    matches = pattern.findall(content)
    if not matches:
        raise ValueError(
            f"No frontmatter block with id prefix '{id_prefix}' found"
        )
    return max(matches, key=len)


def parse_frontmatter(content: str, id_prefix: str = "EPIC-") -> dict[str, Any]:
    """Extract and parse frontmatter YAML from markdown content.

    Args:
        content: Full markdown text.
        id_prefix: Prefix to look for in the ``id:`` field.

    Returns:
        Parsed YAML dictionary.
    """
    raw = extract_frontmatter_block(content, id_prefix)
    parsed = yaml.safe_load(raw)
    if not isinstance(parsed, dict):
        raise ValueError("Frontmatter YAML did not parse to a dictionary")
    return parsed


def extract_section(content: str, heading: str) -> str:
    """Extract the text of a markdown section by heading.

    Args:
        content: Full markdown text.
        heading: The heading text (without ``##`` prefix).

    Returns:
        Section body text (everything up to the next same-level heading or EOF).

    Raises:
        ValueError: If the section is not found.
    """
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\b(.*?)(?=\n##\s[^#]|\Z)",
        re.DOTALL | re.MULTILINE,
    )
    match = pattern.search(content)
    if not match:
        raise ValueError(f"Section '## {heading}' not found")
    return match.group(1)


# ---------------------------------------------------------------------------
# Sample markdown builders (for frontmatter round-trip tests)
# ---------------------------------------------------------------------------


def build_epic_markdown(
    epic_id: str = "EPIC-001",
    title: str = "Test Epic",
    status: str = "planning",
    priority: str = "high",
    organisation_pattern: str = "features",
    completeness_score: int = 0,
    extra_frontmatter: dict[str, Any] | None = None,
    body: str = "",
) -> str:
    """Build a sample epic markdown string with frontmatter.

    Args:
        epic_id: Epic identifier.
        title: Epic title.
        status: Lifecycle status.
        priority: Priority level.
        organisation_pattern: One of ``features``, ``direct``, ``mixed``.
        completeness_score: Numeric completeness score.
        extra_frontmatter: Additional frontmatter fields to include.
        body: Markdown body content.

    Returns:
        Complete markdown string with YAML frontmatter.
    """
    fm: dict[str, Any] = {
        "id": epic_id,
        "title": title,
        "status": status,
        "priority": priority,
        "organisation_pattern": organisation_pattern,
        "direct_tasks": [],
        "graphiti_synced": False,
        "last_graphiti_sync": None,
        "completeness_score": completeness_score,
    }
    if extra_frontmatter:
        fm.update(extra_frontmatter)
    yaml_str = yaml.dump(fm, default_flow_style=False, sort_keys=False)
    return f"---\n{yaml_str}---\n\n# Epic: {title}\n\n{body}"


def build_feature_markdown(
    feature_id: str = "FEAT-001",
    title: str = "Test Feature",
    epic: str = "EPIC-001",
    status: str = "planning",
    priority: str = "normal",
    completeness_score: int = 0,
    extra_frontmatter: dict[str, Any] | None = None,
    body: str = "",
) -> str:
    """Build a sample feature markdown string with frontmatter.

    Args:
        feature_id: Feature identifier.
        title: Feature title.
        epic: Parent epic ID.
        status: Lifecycle status.
        priority: Priority level.
        completeness_score: Numeric completeness score.
        extra_frontmatter: Additional frontmatter fields to include.
        body: Markdown body content.

    Returns:
        Complete markdown string with YAML frontmatter.
    """
    fm: dict[str, Any] = {
        "id": feature_id,
        "title": title,
        "epic": epic,
        "status": status,
        "priority": priority,
        "graphiti_synced": False,
        "last_graphiti_sync": None,
        "completeness_score": completeness_score,
        "requirements": [],
        "bdd_scenarios": [],
        "acceptance_criteria": [],
    }
    if extra_frontmatter:
        fm.update(extra_frontmatter)
    yaml_str = yaml.dump(fm, default_flow_style=False, sort_keys=False)
    return f"---\n{yaml_str}---\n\n# Feature: {title}\n\n{body}"


# ---------------------------------------------------------------------------
# Frontmatter round-trip helpers
# ---------------------------------------------------------------------------


def parse_markdown_frontmatter(markdown: str) -> dict[str, Any]:
    """Parse YAML frontmatter from a markdown string.

    Expects the document to start with ``---`` delimited YAML.

    Args:
        markdown: Markdown text with frontmatter.

    Returns:
        Parsed frontmatter dictionary.

    Raises:
        ValueError: If no frontmatter delimiters are found.
    """
    match = re.match(r"^---\s*\n(.*?)\n---", markdown, re.DOTALL)
    if not match:
        raise ValueError("No frontmatter found in markdown")
    parsed = yaml.safe_load(match.group(1))
    if not isinstance(parsed, dict):
        raise ValueError("Frontmatter did not parse to a dictionary")
    return parsed


def update_frontmatter_field(
    markdown: str, field: str, value: Any
) -> str:
    """Update a single field in the YAML frontmatter of a markdown string.

    Args:
        markdown: Original markdown text.
        field: Frontmatter field name.
        value: New value for the field.

    Returns:
        Updated markdown text with modified frontmatter.
    """
    fm = parse_markdown_frontmatter(markdown)
    fm[field] = value
    yaml_str = yaml.dump(fm, default_flow_style=False, sort_keys=False)
    body_match = re.search(r"^---\s*\n.*?\n---\s*\n(.*)", markdown, re.DOTALL)
    body = body_match.group(1) if body_match else ""
    return f"---\n{yaml_str}---\n{body}"


def append_refinement_history(
    markdown: str,
    completeness_before: int,
    completeness_after: int,
    changes: list[str],
) -> str:
    """Append a refinement_history entry to the frontmatter.

    Args:
        markdown: Original markdown text.
        completeness_before: Score before refinement.
        completeness_after: Score after refinement.
        changes: List of change descriptions.

    Returns:
        Updated markdown with new refinement_history entry appended.
    """
    fm = parse_markdown_frontmatter(markdown)
    history = fm.get("refinement_history", []) or []
    history.append(
        {
            "date": "2026-02-19T14:30:00Z",
            "changes": changes,
            "completeness_before": completeness_before,
            "completeness_after": completeness_after,
        }
    )
    fm["refinement_history"] = history
    return update_frontmatter_field(markdown, "refinement_history", history)
