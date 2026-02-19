"""Tests for TASK-RK01-008: Update Hierarchy View to Render All Organisation Patterns.

Validates that installer/global/commands/hierarchy-view.md renders direct-pattern
and mixed-pattern epics in tree view, includes Graphiti integration display,
and provides updated filtering options for all organisation patterns.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

HIERARCHY_VIEW_PATH = (
    Path(__file__).resolve().parents[1]
    / "installer"
    / "global"
    / "commands"
    / "hierarchy-view.md"
)


@pytest.fixture(scope="module")
def hierarchy_view_content() -> str:
    """Read the full hierarchy-view.md file content."""
    if not HIERARCHY_VIEW_PATH.exists():
        pytest.fail(f"hierarchy-view.md not found at {HIERARCHY_VIEW_PATH}")
    return HIERARCHY_VIEW_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def hierarchy_view_lower(hierarchy_view_content: str) -> str:
    """Return lowercased hierarchy-view.md content for case-insensitive checks."""
    return hierarchy_view_content.lower()


# ---------------------------------------------------------------------------
# AC-001: Tree view renders all three organisation patterns correctly
# ---------------------------------------------------------------------------


class TestTreeViewAllPatterns:
    """Verify tree view renders features, direct, and mixed patterns."""

    def test_features_pattern_tree_present(
        self, hierarchy_view_content: str
    ) -> None:
        """Tree view must show an epic using the features pattern (EPIC → FEAT → TASK)."""
        assert re.search(
            r"features\s+pattern", hierarchy_view_content, re.IGNORECASE
        ), "A features pattern epic must be shown in the tree view"

    def test_direct_pattern_tree_present(
        self, hierarchy_view_content: str
    ) -> None:
        """Tree view must show an epic using the direct pattern (EPIC → TASK)."""
        assert re.search(
            r"direct\s+pattern", hierarchy_view_content, re.IGNORECASE
        ), "A direct pattern epic must be shown in the tree view"

    def test_mixed_pattern_tree_present(
        self, hierarchy_view_content: str
    ) -> None:
        """Tree view must show an epic using the mixed pattern."""
        assert re.search(
            r"mixed\s+pattern", hierarchy_view_content, re.IGNORECASE
        ), "A mixed pattern epic must be shown in the tree view"

    def test_three_distinct_epics_in_tree(
        self, hierarchy_view_content: str
    ) -> None:
        """Tree view must show at least three distinct epics with pattern labels."""
        epic_matches = re.findall(
            r"EPIC-\d+.*?\((?:features|direct|mixed)\s+pattern\)",
            hierarchy_view_content,
            re.IGNORECASE,
        )
        assert len(epic_matches) >= 3, (
            f"Expected at least 3 epics with pattern labels, found {len(epic_matches)}"
        )


# ---------------------------------------------------------------------------
# AC-002: Direct-pattern epics show tasks directly under epic
# ---------------------------------------------------------------------------


class TestDirectPatternTasks:
    """Verify direct-pattern epics show tasks directly (no feature layer)."""

    def test_direct_epic_has_tasks_without_features(
        self, hierarchy_view_content: str
    ) -> None:
        """Direct pattern epic must have TASK entries without FEAT intermediary."""
        # Look for a direct pattern epic followed by TASK entries (with tree chars)
        assert re.search(
            r"direct\s+pattern\).*?\n(?:.*?├──.*?TASK|.*?└──.*?TASK)",
            hierarchy_view_content,
            re.IGNORECASE | re.DOTALL,
        ), "Direct pattern epic must show tasks directly under the epic"

    def test_direct_pattern_no_feat_under_epic(
        self, hierarchy_view_content: str
    ) -> None:
        """Direct pattern epic must NOT have FEAT entries under it."""
        # Extract the direct pattern block: from the direct pattern epic line
        # until the next epic or end of block
        direct_block_match = re.search(
            r"(EPIC-\d+:.*?\(direct\s+pattern\).*?)(?=EPIC-\d+:|```)",
            hierarchy_view_content,
            re.IGNORECASE | re.DOTALL,
        )
        assert direct_block_match, "Could not find direct pattern epic block"
        direct_block = direct_block_match.group(1)
        assert "FEAT-" not in direct_block, (
            "Direct pattern epic must NOT contain FEAT entries"
        )


# ---------------------------------------------------------------------------
# AC-003: Mixed-pattern epics show "[Direct Tasks]" group with visual separation
# ---------------------------------------------------------------------------


class TestMixedPatternDirectTasksGroup:
    """Verify mixed-pattern epics show [Direct Tasks] grouping."""

    def test_direct_tasks_group_label_present(
        self, hierarchy_view_content: str
    ) -> None:
        """Mixed pattern must show a '[Direct Tasks]' group label."""
        assert "[Direct Tasks]" in hierarchy_view_content, (
            "Mixed pattern must include '[Direct Tasks]' group label"
        )

    def test_direct_tasks_group_under_mixed_epic(
        self, hierarchy_view_content: str
    ) -> None:
        """[Direct Tasks] group must appear under a mixed-pattern epic."""
        mixed_block_match = re.search(
            r"(EPIC-\d+:.*?\(mixed\s+pattern\).*?)(?=EPIC-\d+:|```)",
            hierarchy_view_content,
            re.IGNORECASE | re.DOTALL,
        )
        assert mixed_block_match, "Could not find mixed pattern epic block"
        mixed_block = mixed_block_match.group(1)
        assert "[Direct Tasks]" in mixed_block, (
            "[Direct Tasks] group must appear within the mixed pattern epic"
        )

    def test_mixed_pattern_has_features_and_direct_tasks(
        self, hierarchy_view_content: str
    ) -> None:
        """Mixed pattern must show both FEAT entries and [Direct Tasks] group."""
        mixed_block_match = re.search(
            r"(EPIC-\d+:.*?\(mixed\s+pattern\).*?)(?=EPIC-\d+:|```)",
            hierarchy_view_content,
            re.IGNORECASE | re.DOTALL,
        )
        assert mixed_block_match, "Could not find mixed pattern epic block"
        mixed_block = mixed_block_match.group(1)
        assert "FEAT-" in mixed_block, (
            "Mixed pattern epic must contain at least one FEAT entry"
        )
        assert "[Direct Tasks]" in mixed_block, (
            "Mixed pattern epic must contain [Direct Tasks] group"
        )


# ---------------------------------------------------------------------------
# AC-004: Pattern label shown next to each epic
# ---------------------------------------------------------------------------


class TestPatternLabels:
    """Verify pattern labels are shown next to each epic."""

    def test_features_pattern_label(self, hierarchy_view_content: str) -> None:
        """At least one epic must show '(features pattern)' label."""
        assert re.search(
            r"EPIC-\d+:.*\(features\s+pattern\)",
            hierarchy_view_content,
            re.IGNORECASE,
        ), "An epic with '(features pattern)' label must be present"

    def test_direct_pattern_label(self, hierarchy_view_content: str) -> None:
        """At least one epic must show '(direct pattern)' label."""
        assert re.search(
            r"EPIC-\d+:.*\(direct\s+pattern\)",
            hierarchy_view_content,
            re.IGNORECASE,
        ), "An epic with '(direct pattern)' label must be present"

    def test_mixed_pattern_label(self, hierarchy_view_content: str) -> None:
        """At least one epic must show '(mixed pattern)' label."""
        assert re.search(
            r"EPIC-\d+:.*\(mixed\s+pattern\)",
            hierarchy_view_content,
            re.IGNORECASE,
        ), "An epic with '(mixed pattern)' label must be present"


# ---------------------------------------------------------------------------
# AC-005: Graphiti integration section in external tools view
# ---------------------------------------------------------------------------


class TestGraphitiIntegration:
    """Verify Graphiti integration is shown in external tools view."""

    def test_graphiti_section_present(
        self, hierarchy_view_content: str
    ) -> None:
        """External tools view must include a Graphiti integration section."""
        assert re.search(
            r"(?i)graphiti\s+integration|graphiti.*knowledge\s*graph",
            hierarchy_view_content,
        ), "A Graphiti integration section must be present"

    def test_graphiti_connection_status(
        self, hierarchy_view_lower: str
    ) -> None:
        """Graphiti section must show connection status."""
        assert "graphiti" in hierarchy_view_lower and (
            "connection" in hierarchy_view_lower
            or "status" in hierarchy_view_lower
            or "healthy" in hierarchy_view_lower
        ), "Graphiti section must show connection status"

    def test_graphiti_episodes_synced(
        self, hierarchy_view_lower: str
    ) -> None:
        """Graphiti section must show episodes synced."""
        assert "episode" in hierarchy_view_lower, (
            "Graphiti section must show episodes synced"
        )

    def test_graphiti_last_sync(
        self, hierarchy_view_lower: str
    ) -> None:
        """Graphiti section must show last sync time."""
        assert "graphiti" in hierarchy_view_lower and (
            "last sync" in hierarchy_view_lower
            or "last_sync" in hierarchy_view_lower
            or "synced" in hierarchy_view_lower
        ), "Graphiti section must show last sync information"

    def test_graphiti_group_id(
        self, hierarchy_view_content: str
    ) -> None:
        """Graphiti section must display group ID format ({project}__requirements)."""
        assert re.search(
            r"__requirements", hierarchy_view_content
        ), "Graphiti section must show group ID with '__requirements' format"

    def test_graphiti_in_workflow_view(
        self, hierarchy_view_content: str
    ) -> None:
        """Workflow status view must include Graphiti knowledge graph health."""
        # Look for Graphiti mention near workflow context
        assert re.search(
            r"(?i)graphiti.*health|knowledge\s*graph.*health",
            hierarchy_view_content,
        ), "Workflow view must include Graphiti knowledge graph health indicator"

    def test_graphiti_episode_coverage(
        self, hierarchy_view_lower: str
    ) -> None:
        """Workflow view must show episode coverage per entity type."""
        assert "episode coverage" in hierarchy_view_lower or (
            "episode" in hierarchy_view_lower
            and "coverage" in hierarchy_view_lower
        ), "Workflow view must show episode coverage per entity type"

    def test_graphiti_completeness_scores(
        self, hierarchy_view_lower: str
    ) -> None:
        """Workflow view must display completeness scores."""
        assert "completeness" in hierarchy_view_lower, (
            "Workflow view must display completeness scores"
        )


# ---------------------------------------------------------------------------
# AC-006: --pattern filter works correctly
# ---------------------------------------------------------------------------


class TestPatternFilter:
    """Verify --pattern filter is documented."""

    def test_pattern_filter_option_documented(
        self, hierarchy_view_content: str
    ) -> None:
        """--pattern filter option must be documented."""
        assert "--pattern" in hierarchy_view_content, (
            "--pattern filter option must be documented"
        )

    def test_pattern_filter_values_documented(
        self, hierarchy_view_content: str
    ) -> None:
        """--pattern filter must document direct, features, and mixed values."""
        assert re.search(
            r"--pattern.*(?:direct|features|mixed)",
            hierarchy_view_content,
            re.IGNORECASE,
        ), "--pattern filter must list valid values"

    def test_graphiti_status_filter_documented(
        self, hierarchy_view_content: str
    ) -> None:
        """--graphiti-status filter option must be documented."""
        assert "--graphiti-status" in hierarchy_view_content, (
            "--graphiti-status filter option must be documented"
        )


# ---------------------------------------------------------------------------
# AC-007: Dependency mapping handles all patterns
# ---------------------------------------------------------------------------


class TestDependencyMappingPatterns:
    """Verify dependency mapping handles all organisation patterns."""

    def test_direct_pattern_dependencies(
        self, hierarchy_view_content: str
    ) -> None:
        """Dependency mapping must handle direct-pattern task-to-task deps."""
        lower = hierarchy_view_content.lower()
        assert "direct" in lower and "dependenc" in lower, (
            "Dependency mapping must mention direct-pattern dependencies"
        )

    def test_cross_epic_dependencies(
        self, hierarchy_view_content: str
    ) -> None:
        """Dependency mapping must show cross-epic dependencies for all patterns."""
        assert re.search(
            r"(?i)cross.?epic.*dependenc|inter.?epic.*dependenc",
            hierarchy_view_content,
        ), "Cross-epic dependencies must be documented for all patterns"


# ---------------------------------------------------------------------------
# AC-008: Backward compatible with existing features-pattern epics
# ---------------------------------------------------------------------------


class TestBackwardCompatibility:
    """Verify backward compatibility with existing features-pattern view."""

    def test_features_pattern_still_shows_feat_task_hierarchy(
        self, hierarchy_view_content: str
    ) -> None:
        """Features pattern must still show EPIC → FEAT → TASK hierarchy."""
        features_block_match = re.search(
            r"(EPIC-\d+:.*?\(features\s+pattern\).*?)(?=EPIC-\d+:|```)",
            hierarchy_view_content,
            re.IGNORECASE | re.DOTALL,
        )
        assert features_block_match, "Could not find features pattern epic block"
        features_block = features_block_match.group(1)
        assert "FEAT-" in features_block, (
            "Features pattern must still include FEAT entries"
        )
        assert "TASK-" in features_block, (
            "Features pattern must still include TASK entries"
        )

    def test_original_external_tools_preserved(
        self, hierarchy_view_content: str
    ) -> None:
        """Original external tools (Jira, Linear, GitHub) must still be present."""
        lower = hierarchy_view_content.lower()
        assert "jira" in lower, "Jira integration must still be present"
        assert "linear" in lower, "Linear integration must still be present"
        assert "github" in lower, "GitHub integration must still be present"

    def test_portfolio_view_preserved(
        self, hierarchy_view_content: str
    ) -> None:
        """Portfolio view option must still be present."""
        assert "--portfolio" in hierarchy_view_content, (
            "--portfolio option must still be present"
        )

    def test_timeline_view_preserved(
        self, hierarchy_view_content: str
    ) -> None:
        """Timeline view option must still be present."""
        assert "--timeline" in hierarchy_view_content, (
            "--timeline option must still be present"
        )

    def test_dependencies_view_preserved(
        self, hierarchy_view_content: str
    ) -> None:
        """Dependencies view option must still be present."""
        assert "--dependencies" in hierarchy_view_content, (
            "--dependencies option must still be present"
        )
