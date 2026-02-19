"""E2E test fixtures for complete command pipeline testing.

Provides temporary directory structures, sample markdown builders,
command spec loaders, and pipeline simulation helpers used across
all E2E test modules. All fixtures use temp directories to avoid
side effects on real data.
"""

from __future__ import annotations

import re
import shutil
import textwrap
from pathlib import Path
from typing import Any, Generator

import pytest
import yaml


# ---------------------------------------------------------------------------
# Path constants
# ---------------------------------------------------------------------------

_WORKTREE_ROOT = Path(__file__).resolve().parents[2]
_COMMANDS_DIR = _WORKTREE_ROOT / "installer" / "global" / "commands"
_CONFIG_DIR = _WORKTREE_ROOT / "installer" / "global" / "config"


# ---------------------------------------------------------------------------
# Command-spec loading
# ---------------------------------------------------------------------------


def _load_command(name: str) -> str:
    """Load a command specification markdown file by name."""
    path = _COMMANDS_DIR / f"{name}.md"
    if not path.exists():
        raise FileNotFoundError(f"Command spec not found: {path}")
    return path.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def epic_create_spec() -> str:
    """Full text of installer/global/commands/epic-create.md."""
    return _load_command("epic-create")


@pytest.fixture(scope="session")
def epic_refine_spec() -> str:
    """Full text of installer/global/commands/epic-refine.md."""
    return _load_command("epic-refine")


@pytest.fixture(scope="session")
def epic_status_spec() -> str:
    """Full text of installer/global/commands/epic-status.md."""
    return _load_command("epic-status")


@pytest.fixture(scope="session")
def feature_create_spec() -> str:
    """Full text of installer/global/commands/feature-create.md."""
    return _load_command("feature-create")


@pytest.fixture(scope="session")
def feature_refine_spec() -> str:
    """Full text of installer/global/commands/feature-refine.md."""
    return _load_command("feature-refine")


@pytest.fixture(scope="session")
def hierarchy_view_spec() -> str:
    """Full text of installer/global/commands/hierarchy-view.md."""
    return _load_command("hierarchy-view")


@pytest.fixture(scope="session")
def requirekit_sync_spec() -> str:
    """Full text of installer/global/commands/requirekit-sync.md."""
    return _load_command("requirekit-sync")


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


class _MkDocsLoader(yaml.SafeLoader):
    """Custom YAML loader that handles !!python/name tags from mkdocs.yml.

    MkDocs uses ``!!python/name:`` tags for plugin references (e.g. emoji
    index/generators). SafeLoader rejects these, so we register a
    passthrough constructor that returns the tag value as a plain string.
    """


def _python_name_constructor(
    loader: yaml.Loader, node: yaml.ScalarNode
) -> str:
    """Return the scalar value unchanged for !!python/name tags."""
    return loader.construct_scalar(node)


_MkDocsLoader.add_constructor(
    "tag:yaml.org,2002:python/name:pymdownx.emoji.twemoji",
    _python_name_constructor,
)
_MkDocsLoader.add_constructor(
    "tag:yaml.org,2002:python/name:pymdownx.emoji.to_svg",
    _python_name_constructor,
)
_MkDocsLoader.add_constructor(
    "tag:yaml.org,2002:python/name:pymdownx.superfences.fence_code_format",
    _python_name_constructor,
)


@pytest.fixture(scope="session")
def mkdocs_config() -> dict[str, Any]:
    """Parsed mkdocs.yml configuration.

    Uses a custom loader to handle ``!!python/name:`` tags that MkDocs
    uses for plugin references (e.g. emoji, superfences).
    """
    path = _WORKTREE_ROOT / "mkdocs.yml"
    if not path.exists():
        pytest.fail(f"mkdocs.yml not found at {path}")
    raw = yaml.load(path.read_text(encoding="utf-8"), Loader=_MkDocsLoader)
    if not isinstance(raw, dict):
        pytest.fail("mkdocs.yml did not parse to a dictionary")
    return raw


# ---------------------------------------------------------------------------
# Temporary workspace fixture
# ---------------------------------------------------------------------------


@pytest.fixture()
def workspace(tmp_path: Path) -> Path:
    """Create a temporary workspace with docs/epics and docs/features dirs.

    Yields the workspace root path. Cleanup is automatic via tmp_path.
    """
    epics_dir = tmp_path / "docs" / "epics"
    features_dir = tmp_path / "docs" / "features"
    bdd_dir = tmp_path / "docs" / "bdd"
    requirements_dir = tmp_path / "docs" / "requirements"
    epics_dir.mkdir(parents=True)
    features_dir.mkdir(parents=True)
    bdd_dir.mkdir(parents=True)
    requirements_dir.mkdir(parents=True)
    return tmp_path


# ---------------------------------------------------------------------------
# Markdown builders
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
    """Build a sample epic markdown string with frontmatter."""
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
    """Build a sample feature markdown string with frontmatter."""
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
# Frontmatter helpers
# ---------------------------------------------------------------------------


def parse_markdown_frontmatter(markdown: str) -> dict[str, Any]:
    """Parse YAML frontmatter from a markdown string.

    Expects the document to start with ``---`` delimited YAML.
    """
    match = re.match(r"^---\s*\n(.*?)\n---", markdown, re.DOTALL)
    if not match:
        raise ValueError("No frontmatter found in markdown")
    parsed = yaml.safe_load(match.group(1))
    if not isinstance(parsed, dict):
        raise ValueError("Frontmatter did not parse to a dictionary")
    return parsed


def update_frontmatter_field(markdown: str, field: str, value: Any) -> str:
    """Update a single field in the YAML frontmatter of a markdown string."""
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
    date: str = "2026-02-19T14:30:00Z",
) -> str:
    """Append a refinement_history entry to the frontmatter."""
    fm = parse_markdown_frontmatter(markdown)
    history = fm.get("refinement_history", []) or []
    history.append(
        {
            "date": date,
            "changes": changes,
            "completeness_before": completeness_before,
            "completeness_after": completeness_after,
        }
    )
    fm["refinement_history"] = history
    return update_frontmatter_field(markdown, "refinement_history", history)


def extract_section(content: str, heading: str) -> str:
    """Extract the text of a markdown section by heading."""
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\b(.*?)(?=\n##\s[^#]|\Z)",
        re.DOTALL | re.MULTILINE,
    )
    match = pattern.search(content)
    if not match:
        raise ValueError(f"Section '## {heading}' not found")
    return match.group(1)


# ---------------------------------------------------------------------------
# Pipeline simulation helpers
# ---------------------------------------------------------------------------


def simulate_epic_create(
    workspace: Path,
    epic_id: str = "EPIC-001",
    title: str = "Test Epic",
    organisation_pattern: str = "features",
    completeness_score: int = 0,
    body: str = "",
    extra_frontmatter: dict[str, Any] | None = None,
) -> Path:
    """Simulate /epic-create by writing an epic markdown file.

    Returns the path to the created file.
    """
    md = build_epic_markdown(
        epic_id=epic_id,
        title=title,
        organisation_pattern=organisation_pattern,
        completeness_score=completeness_score,
        body=body,
        extra_frontmatter=extra_frontmatter,
    )
    epic_file = workspace / "docs" / "epics" / f"{epic_id.lower()}.md"
    epic_file.write_text(md, encoding="utf-8")
    return epic_file


def simulate_feature_create(
    workspace: Path,
    feature_id: str = "FEAT-001",
    title: str = "Test Feature",
    epic: str = "EPIC-001",
    completeness_score: int = 0,
    body: str = "",
    extra_frontmatter: dict[str, Any] | None = None,
) -> Path:
    """Simulate /feature-create by writing a feature markdown file.

    Returns the path to the created file.
    """
    md = build_feature_markdown(
        feature_id=feature_id,
        title=title,
        epic=epic,
        completeness_score=completeness_score,
        body=body,
        extra_frontmatter=extra_frontmatter,
    )
    feat_file = workspace / "docs" / "features" / f"{feature_id.lower()}.md"
    feat_file.write_text(md, encoding="utf-8")
    return feat_file


def simulate_epic_refine(
    epic_file: Path,
    completeness_before: int,
    completeness_after: int,
    changes: list[str],
    date: str = "2026-02-19T14:30:00Z",
) -> str:
    """Simulate /epic-refine by updating completeness and appending history.

    Returns the updated markdown content.
    """
    md = epic_file.read_text(encoding="utf-8")
    md = update_frontmatter_field(md, "completeness_score", completeness_after)
    md = append_refinement_history(md, completeness_before, completeness_after, changes, date)
    epic_file.write_text(md, encoding="utf-8")
    return md


def simulate_feature_refine(
    feat_file: Path,
    completeness_before: int,
    completeness_after: int,
    changes: list[str],
    date: str = "2026-02-19T14:30:00Z",
) -> str:
    """Simulate /feature-refine by updating completeness and appending history.

    Returns the updated markdown content.
    """
    md = feat_file.read_text(encoding="utf-8")
    md = update_frontmatter_field(md, "completeness_score", completeness_after)
    md = append_refinement_history(md, completeness_before, completeness_after, changes, date)
    feat_file.write_text(md, encoding="utf-8")
    return md


def simulate_sync(
    file_path: Path,
    graphiti_enabled: bool = False,
) -> dict[str, Any]:
    """Simulate /requirekit-sync by reading markdown and marking sync status.

    Returns a result dict describing what would happen.
    """
    md = file_path.read_text(encoding="utf-8")
    fm = parse_markdown_frontmatter(md)

    result: dict[str, Any] = {
        "entity_id": fm.get("id", "UNKNOWN"),
        "entity_type": "epic" if "EPIC-" in fm.get("id", "") else "feature",
        "markdown_read": True,
        "graphiti_enabled": graphiti_enabled,
        "graphiti_pushed": False,
        "sync_status": "skipped",
    }

    if graphiti_enabled:
        # Simulate a successful sync
        md = update_frontmatter_field(md, "graphiti_synced", True)
        md = update_frontmatter_field(md, "last_graphiti_sync", "2026-02-19T15:00:00Z")
        file_path.write_text(md, encoding="utf-8")
        result["graphiti_pushed"] = True
        result["sync_status"] = "success"
    else:
        result["sync_status"] = "skipped_not_enabled"

    return result


def read_epic_status(
    workspace: Path,
    epic_id: str,
) -> dict[str, Any]:
    """Simulate /epic-status by reading epic and its linked features.

    Returns a status summary dict.
    """
    epic_file = workspace / "docs" / "epics" / f"{epic_id.lower()}.md"
    if not epic_file.exists():
        raise FileNotFoundError(f"Epic file not found: {epic_file}")

    md = epic_file.read_text(encoding="utf-8")
    fm = parse_markdown_frontmatter(md)

    # Gather linked features
    features_dir = workspace / "docs" / "features"
    linked_features: list[dict[str, Any]] = []
    if features_dir.exists():
        for feat_file in features_dir.glob("*.md"):
            feat_md = feat_file.read_text(encoding="utf-8")
            feat_fm = parse_markdown_frontmatter(feat_md)
            if feat_fm.get("epic") == epic_id:
                linked_features.append(feat_fm)

    return {
        "id": fm["id"],
        "title": fm["title"],
        "status": fm.get("status", "planning"),
        "priority": fm.get("priority", "normal"),
        "organisation_pattern": fm.get("organisation_pattern", "features"),
        "completeness_score": fm.get("completeness_score", 0),
        "graphiti_synced": fm.get("graphiti_synced", False),
        "last_graphiti_sync": fm.get("last_graphiti_sync"),
        "direct_tasks": fm.get("direct_tasks", []),
        "linked_features": linked_features,
        "refinement_history": fm.get("refinement_history", []),
    }


def calculate_completeness(
    dimension_scores: list[float],
    weights: list[int],
) -> float:
    """Calculate weighted completeness score from dimension scores and weights.

    Both lists must have the same length.
    """
    if len(dimension_scores) != len(weights):
        raise ValueError(
            f"dimension_scores ({len(dimension_scores)}) and "
            f"weights ({len(weights)}) must have same length"
        )
    return sum(w * s for w, s in zip(weights, dimension_scores))
