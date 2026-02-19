"""Tests for TASK-RK01-007: Update Epic Status to Display Organisation Patterns.

Validates that installer/global/commands/epic-status.md displays both features
and direct tasks, handles all three organisation patterns (direct, features, mixed),
shows Graphiti sync status, and calculates progress correctly for each pattern.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

EPIC_STATUS_PATH = (
    Path(__file__).resolve().parents[1]
    / "installer"
    / "global"
    / "commands"
    / "epic-status.md"
)


@pytest.fixture(scope="module")
def epic_status_content() -> str:
    """Read the full epic-status.md file content."""
    if not EPIC_STATUS_PATH.exists():
        pytest.fail(f"epic-status.md not found at {EPIC_STATUS_PATH}")
    return EPIC_STATUS_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def lower_content(epic_status_content: str) -> str:
    """Lowercase version for case-insensitive matching."""
    return epic_status_content.lower()


# ---------------------------------------------------------------------------
# AC-001: Portfolio view shows pattern column for all epics
# ---------------------------------------------------------------------------


class TestPortfolioPatternColumn:
    """Verify the portfolio view table includes an organisation pattern column."""

    def test_pattern_column_in_portfolio_table(
        self, epic_status_content: str
    ) -> None:
        """The portfolio overview table must include a 'Pattern' column header."""
        assert re.search(
            r"Pattern", epic_status_content
        ), "Portfolio view table must include a 'Pattern' column"

    def test_portfolio_shows_direct_pattern_value(
        self, epic_status_content: str
    ) -> None:
        """Portfolio view must show 'direct' as a pattern value in a table row."""
        assert re.search(
            r"direct", epic_status_content
        ), "Portfolio view must show 'direct' pattern value"

    def test_portfolio_shows_features_pattern_value(
        self, epic_status_content: str
    ) -> None:
        """Portfolio view must show 'features' as a pattern value in a table row."""
        # 'features' already existed, but must be in context of pattern column
        assert re.search(
            r"(?i)features\s*│|│\s*features|pattern.*features|features.*pattern",
            epic_status_content,
        ), "Portfolio view must show 'features' pattern value"

    def test_portfolio_shows_mixed_pattern_value(
        self, epic_status_content: str
    ) -> None:
        """Portfolio view must show 'mixed' as a pattern value in a table row."""
        assert re.search(
            r"(?i)mixed\s*│|│\s*mixed|mixed.*pattern",
            epic_status_content,
        ), "Portfolio view must show 'mixed' pattern value"

    def test_portfolio_shows_task_count_for_direct(
        self, epic_status_content: str
    ) -> None:
        """Direct-pattern epics must show task count in portfolio."""
        assert re.search(
            r"\d+\s*tasks?", epic_status_content
        ), "Direct-pattern epics must show task count"

    def test_portfolio_shows_feature_count_for_features(
        self, epic_status_content: str
    ) -> None:
        """Features-pattern epics must show feature count in portfolio."""
        assert re.search(
            r"\d+\s*features?", epic_status_content
        ), "Features-pattern epics must show feature count"


# ---------------------------------------------------------------------------
# AC-002: Direct-pattern epics show task list instead of feature list
# ---------------------------------------------------------------------------


class TestDirectPatternDisplay:
    """Verify direct-pattern epics show task list in detailed view."""

    def test_direct_pattern_section_exists(
        self, epic_status_content: str
    ) -> None:
        """A detailed view for direct-pattern epics must exist."""
        assert re.search(
            r"Pattern:\s*direct", epic_status_content
        ), "Detailed view must show 'Pattern: direct'"

    def test_direct_tasks_section_header(
        self, epic_status_content: str
    ) -> None:
        """Direct-pattern display must include 'Direct Tasks' section header."""
        assert re.search(
            r"Direct Tasks\s*\(\d+\)", epic_status_content
        ), "Direct-pattern display must include 'Direct Tasks (N)' section"

    def test_direct_tasks_list_shows_task_ids(
        self, epic_status_content: str
    ) -> None:
        """Direct tasks section must list task IDs (TASK-XXX format)."""
        # Find the Direct Tasks section and check for task IDs within it
        assert re.search(
            r"Direct Tasks.*TASK-\d+",
            epic_status_content,
            re.DOTALL,
        ), "Direct Tasks section must list tasks with TASK-XXX IDs"

    def test_direct_tasks_show_status_indicators(
        self, epic_status_content: str
    ) -> None:
        """Direct tasks must show status indicators (in_progress, backlog, etc.)."""
        assert re.search(
            r"Direct Tasks.*\[(?:in_progress|backlog|complete|done)\]",
            epic_status_content,
            re.DOTALL | re.IGNORECASE,
        ), "Direct tasks must show status indicators in brackets"

    def test_direct_pattern_progress_shows_task_ratio(
        self, epic_status_content: str
    ) -> None:
        """Direct-pattern progress must show task completion ratio."""
        # Match patterns like "33% (1/3 tasks" or "Progress: N%"
        assert re.search(
            r"Progress.*\d+%.*\d+/\d+\s*task",
            epic_status_content,
            re.DOTALL | re.IGNORECASE,
        ), "Direct-pattern progress must show task completion ratio"

    def test_direct_pattern_display_format_matches_spec(
        self, epic_status_content: str
    ) -> None:
        """Direct pattern display must match the specified format from the task."""
        # Verify the key structure elements are present
        assert re.search(
            r"Epic:.*EPIC-\d+.*\n.*Status:.*Pattern:\s*direct",
            epic_status_content,
            re.IGNORECASE,
        ), "Direct pattern display must match specified format"


# ---------------------------------------------------------------------------
# AC-003: Mixed-pattern epics show both with warning
# ---------------------------------------------------------------------------


class TestMixedPatternDisplay:
    """Verify mixed-pattern epics show both features and tasks with warning."""

    def test_mixed_pattern_section_exists(
        self, epic_status_content: str
    ) -> None:
        """A detailed view for mixed-pattern epics must exist."""
        assert re.search(
            r"Pattern:\s*mixed", epic_status_content
        ), "Detailed view must show 'Pattern: mixed'"

    def test_mixed_pattern_warning_present(
        self, epic_status_content: str
    ) -> None:
        """Mixed-pattern display must include a warning message."""
        assert re.search(
            r"⚠️.*mixed|mixed.*⚠️|Mixed organisation|consider.*group",
            epic_status_content,
            re.IGNORECASE,
        ), "Mixed-pattern display must include a warning"

    def test_mixed_pattern_shows_features_section(
        self, epic_status_content: str
    ) -> None:
        """Mixed-pattern display must show Features section."""
        # After 'Pattern: mixed', there should be a Features section
        mixed_section = re.search(
            r"Pattern:\s*mixed.*?Features\s*\(\d+\)",
            epic_status_content,
            re.DOTALL | re.IGNORECASE,
        )
        assert mixed_section, "Mixed-pattern display must show 'Features (N)' section"

    def test_mixed_pattern_shows_direct_tasks_section(
        self, epic_status_content: str
    ) -> None:
        """Mixed-pattern display must show Direct Tasks section."""
        mixed_section = re.search(
            r"Pattern:\s*mixed.*?Direct Tasks\s*\(\d+\)",
            epic_status_content,
            re.DOTALL | re.IGNORECASE,
        )
        assert mixed_section, "Mixed-pattern display must show 'Direct Tasks (N)' section"

    def test_mixed_pattern_both_sections_present(
        self, epic_status_content: str
    ) -> None:
        """Mixed-pattern must show BOTH Features and Direct Tasks sections together."""
        # Both sections must appear after a mixed pattern indicator
        has_features = re.search(
            r"Pattern:\s*mixed.*?Features\s*\(\d+\)",
            epic_status_content,
            re.DOTALL | re.IGNORECASE,
        )
        has_tasks = re.search(
            r"Pattern:\s*mixed.*?Direct Tasks\s*\(\d+\)",
            epic_status_content,
            re.DOTALL | re.IGNORECASE,
        )
        assert has_features and has_tasks, (
            "Mixed-pattern must show both Features and Direct Tasks sections"
        )


# ---------------------------------------------------------------------------
# AC-004: Progress calculated correctly for all three patterns
# ---------------------------------------------------------------------------


class TestProgressCalculation:
    """Verify progress calculation documentation for each pattern."""

    def test_direct_pattern_progress_formula(
        self, lower_content: str
    ) -> None:
        """Direct pattern progress must use task-based calculation."""
        assert re.search(
            r"direct.*completed?\s*tasks?\s*/\s*total\s*tasks?|direct.*task.*progress",
            lower_content,
            re.DOTALL,
        ), "Direct pattern progress must use completed tasks / total tasks formula"

    def test_features_pattern_progress_formula(
        self, lower_content: str
    ) -> None:
        """Features pattern progress must use feature-based calculation."""
        assert re.search(
            r"features?.*feature.*complet|features?\s*pattern.*current|feature.*progress",
            lower_content,
            re.DOTALL,
        ), "Features pattern must use feature completion for progress"

    def test_mixed_pattern_progress_formula(
        self, lower_content: str
    ) -> None:
        """Mixed pattern progress must use weighted combination."""
        assert re.search(
            r"mixed.*weight|weight.*combin|mixed.*progress.*combin",
            lower_content,
            re.DOTALL,
        ), "Mixed pattern progress must use weighted combination"

    def test_progress_calculation_section_exists(
        self, epic_status_content: str
    ) -> None:
        """A progress calculation section must document all three pattern formulas."""
        assert re.search(
            r"(?i)progress\s+calculation",
            epic_status_content,
        ), "A 'Progress Calculation' section must exist"


# ---------------------------------------------------------------------------
# AC-005: Graphiti sync status displayed when enabled
# ---------------------------------------------------------------------------


class TestGraphitiSyncStatus:
    """Verify Graphiti sync status display."""

    def test_graphiti_sync_indicator_present(
        self, epic_status_content: str
    ) -> None:
        """Graphiti sync status indicator must be present in the display."""
        assert re.search(
            r"(?i)graphiti.*sync|graphiti.*status",
            epic_status_content,
        ), "Graphiti sync status indicator must be present"

    def test_graphiti_last_sync_time(
        self, epic_status_content: str
    ) -> None:
        """Graphiti display must show last sync time."""
        assert re.search(
            r"(?i)graphiti.*last\s*sync|last.*graphiti.*sync",
            epic_status_content,
        ), "Graphiti display must show last sync time"

    def test_graphiti_sync_alongside_pm_tools(
        self, epic_status_content: str
    ) -> None:
        """Graphiti sync must appear alongside PM tool sync status."""
        assert re.search(
            r"(?i)graphiti.*sync|sync.*graphiti",
            epic_status_content,
        ), "Graphiti sync indicator must appear alongside PM tool status"


# ---------------------------------------------------------------------------
# AC-006: Completeness score shown in detailed view
# ---------------------------------------------------------------------------


class TestCompletenessScore:
    """Verify completeness score is shown in detailed view."""

    def test_completeness_score_in_detailed_view(
        self, epic_status_content: str
    ) -> None:
        """The detailed view must display a completeness score."""
        assert re.search(
            r"(?i)completeness.*score|completeness.*\d+%",
            epic_status_content,
        ), "Detailed view must display completeness score"

    def test_completeness_score_has_numeric_value(
        self, epic_status_content: str
    ) -> None:
        """Completeness score must include a numeric percentage or fraction."""
        assert re.search(
            r"(?i)completeness.*\d+[%/]",
            epic_status_content,
        ), "Completeness score must include a numeric value"


# ---------------------------------------------------------------------------
# AC-007: Backward compatible (existing features-pattern epics display unchanged)
# ---------------------------------------------------------------------------


class TestBackwardCompatibility:
    """Verify backward compatibility with existing features-pattern display."""

    def test_feature_breakdown_section_preserved(
        self, epic_status_content: str
    ) -> None:
        """The existing 'Feature Breakdown' section must still be present."""
        assert re.search(
            r"Feature Breakdown", epic_status_content
        ), "Feature Breakdown section must be preserved for backward compatibility"

    def test_feature_status_icons_preserved(
        self, epic_status_content: str
    ) -> None:
        """Feature status icons (✅, 🔄, ⏳) must still be present."""
        assert "✅" in epic_status_content, "✅ icon must be preserved"
        assert "🔄" in epic_status_content, "🔄 icon must be preserved"

    def test_feat_ids_still_present(
        self, epic_status_content: str
    ) -> None:
        """FEAT-XXX IDs must still be present in feature breakdown."""
        assert re.search(
            r"FEAT-\d+", epic_status_content
        ), "FEAT-XXX IDs must be preserved"

    def test_original_portfolio_structure_maintained(
        self, epic_status_content: str
    ) -> None:
        """The original portfolio table structure must be maintained."""
        assert re.search(
            r"Epic Portfolio Status|Epic ID.*Title.*Priority",
            epic_status_content,
            re.IGNORECASE,
        ), "Original portfolio table structure must be maintained"

    def test_organisation_pattern_line_in_detailed_view(
        self, epic_status_content: str
    ) -> None:
        """Detailed view must include 'Organisation Pattern' or 'Pattern' line after Priority."""
        assert re.search(
            r"Priority.*Pattern|Pattern.*direct|Pattern.*features|Pattern.*mixed",
            epic_status_content,
            re.DOTALL | re.IGNORECASE,
        ), "Detailed view must include Pattern line"


# ---------------------------------------------------------------------------
# Test Requirements: Verify direct pattern display format matches spec
# ---------------------------------------------------------------------------


class TestDirectPatternSpecFormat:
    """Verify the direct pattern display matches the task specification."""

    def test_direct_pattern_has_emoji_prefix(
        self, epic_status_content: str
    ) -> None:
        """Direct pattern epic display must use 📋 emoji prefix."""
        assert re.search(
            r"📋.*Epic.*EPIC-\d+",
            epic_status_content,
        ), "Direct pattern display must use 📋 emoji prefix"

    def test_direct_pattern_task_status_emoji(
        self, epic_status_content: str
    ) -> None:
        """Direct tasks must use status emojis (🔄, ⏳, ✅)."""
        # Check for at least one task status emoji near TASK-IDs
        assert re.search(
            r"[🔄⏳✅].*TASK-\d+|TASK-\d+.*[🔄⏳✅]",
            epic_status_content,
        ), "Direct tasks must use status emojis"


# ---------------------------------------------------------------------------
# Test Requirements: Verify mixed pattern warning appears
# ---------------------------------------------------------------------------


class TestMixedPatternWarning:
    """Verify the mixed pattern warning matches specification."""

    def test_mixed_warning_text_content(
        self, epic_status_content: str
    ) -> None:
        """Mixed pattern warning must suggest grouping tasks into features."""
        assert re.search(
            r"(?i)consider.*group.*task.*feature|group.*task.*feature",
            epic_status_content,
        ), "Mixed pattern warning must suggest grouping tasks into features"


# ---------------------------------------------------------------------------
# Test Requirements: Verify progress calculation for each pattern
# ---------------------------------------------------------------------------


class TestProgressCalculationPerPattern:
    """Verify the updated progress calculation section."""

    def test_progress_section_covers_three_patterns(
        self, epic_status_content: str
    ) -> None:
        """Progress calculation section must cover all three patterns."""
        section = re.search(
            r"(?i)progress\s+calculation.*?(?=##\s|\Z)",
            epic_status_content,
            re.DOTALL,
        )
        assert section, "Progress Calculation section must exist"
        section_text = section.group(0).lower()
        assert "direct" in section_text, "Progress section must cover direct pattern"
        assert "feature" in section_text, "Progress section must cover features pattern"
        assert "mixed" in section_text, "Progress section must cover mixed pattern"
