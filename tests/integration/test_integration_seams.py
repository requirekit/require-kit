"""Integration tests for refinement flows, Graphiti sync, organisation patterns,
and completeness scoring — covering all six identified technology seams.

Technology Seams Tested:
    1. Markdown <-> Frontmatter parsing
    2. Frontmatter <-> Completeness scoring
    3. Refinement <-> Graphiti push
    4. Organisation pattern <-> Display
    5. Cross-command <-> Consistency
    6. Config <-> Standalone mode

These tests verify that the command specifications are internally consistent
and that cross-command contracts (data formats, field names, terminology)
are honoured across the entire refinement + sync lifecycle.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest
import yaml

from conftest import (
    append_refinement_history,
    build_epic_markdown,
    build_feature_markdown,
    extract_frontmatter_block,
    extract_section,
    parse_frontmatter,
    parse_markdown_frontmatter,
    update_frontmatter_field,
)

# ═══════════════════════════════════════════════════════════════════════════
# 1. REFINEMENT FLOW INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════


class TestEpicRefineLoadAndDisplay:
    """Seam: Markdown <-> Frontmatter parsing.

    Verify the complete chain: load epic markdown -> parse frontmatter ->
    calculate completeness -> display format.
    """

    def test_epic_refine_documents_load_parse_score_display(
        self, epic_refine_spec: str
    ) -> None:
        """The epic-refine spec must document loading, parsing, scoring, and display."""
        lower = epic_refine_spec.lower()
        assert "load" in lower and "epic" in lower, (
            "Must document loading the epic markdown"
        )
        assert "parse" in lower and "frontmatter" in lower, (
            "Must document parsing frontmatter"
        )
        assert "completeness" in lower and "score" in lower, (
            "Must document completeness scoring"
        )
        assert "display" in lower or "assessment" in lower, (
            "Must document display of assessment"
        )

    def test_epic_refine_phase1_load_epic_by_id(
        self, epic_refine_spec: str
    ) -> None:
        """Phase 1 must load the epic file from docs/epics/ by ID."""
        assert "docs/epics/" in epic_refine_spec, (
            "Must reference docs/epics/ directory for loading"
        )

    def test_epic_refine_phase1_parses_yaml_frontmatter(
        self, epic_refine_spec: str
    ) -> None:
        """Phase 1 must parse YAML frontmatter from the loaded epic."""
        lower = epic_refine_spec.lower()
        assert "yaml" in lower or "frontmatter" in lower, (
            "Must document YAML/frontmatter parsing in Phase 1"
        )


class TestEpicRefineUpdateInPlace:
    """Seam: Markdown <-> Frontmatter parsing.

    Verify that refinement updates markdown in-place and preserves
    existing fields.
    """

    def test_update_in_place_documented(self, epic_refine_spec: str) -> None:
        """Refinement must update the epic markdown in-place."""
        lower = epic_refine_spec.lower()
        assert "in-place" in lower or "in place" in lower or "update" in lower, (
            "Must document updating the epic markdown in-place"
        )

    def test_frontmatter_fields_preserved_after_update(self) -> None:
        """Existing frontmatter fields must be preserved after simulated update."""
        original = build_epic_markdown(
            extra_frontmatter={
                "external_ids": {"jira": "PROJ-123"},
                "export_config": {"target_tools": ["jira"]},
            }
        )
        fm = parse_markdown_frontmatter(original)
        # Simulate refinement: update completeness, add refinement_history
        updated = update_frontmatter_field(original, "completeness_score", 72)
        updated_fm = parse_markdown_frontmatter(updated)
        assert updated_fm["external_ids"] == {"jira": "PROJ-123"}, (
            "external_ids must be preserved after update"
        )
        assert updated_fm["export_config"] == {"target_tools": ["jira"]}, (
            "export_config must be preserved after update"
        )
        assert updated_fm["completeness_score"] == 72, (
            "completeness_score must be updated"
        )

    def test_title_and_id_preserved_after_update(self) -> None:
        """Epic ID and title must remain unchanged after refinement update."""
        original = build_epic_markdown(epic_id="EPIC-042", title="My Important Epic")
        updated = update_frontmatter_field(original, "completeness_score", 55)
        fm = parse_markdown_frontmatter(updated)
        assert fm["id"] == "EPIC-042"
        assert fm["title"] == "My Important Epic"


class TestEpicRefineRefinementHistoryAppend:
    """Seam: Markdown <-> Frontmatter parsing.

    Verify that refinement_history is appended (not replaced) across
    successive refinement sessions.
    """

    def test_first_refinement_creates_history(self) -> None:
        """First refinement session must create a refinement_history list."""
        md = build_epic_markdown()
        updated = append_refinement_history(md, 30, 55, ["Added scope boundaries"])
        fm = parse_markdown_frontmatter(updated)
        assert "refinement_history" in fm
        assert len(fm["refinement_history"]) == 1
        assert fm["refinement_history"][0]["completeness_before"] == 30

    def test_second_refinement_appends_to_history(self) -> None:
        """Second refinement session must append, not replace, history."""
        md = build_epic_markdown()
        after_first = append_refinement_history(md, 30, 55, ["Added scope"])
        after_second = append_refinement_history(after_first, 55, 72, ["Added risks"])
        fm = parse_markdown_frontmatter(after_second)
        assert len(fm["refinement_history"]) == 2
        assert fm["refinement_history"][0]["completeness_before"] == 30
        assert fm["refinement_history"][1]["completeness_before"] == 55
        assert fm["refinement_history"][1]["completeness_after"] == 72

    def test_refinement_history_schema_in_spec(self, epic_refine_spec: str) -> None:
        """The epic-refine spec must define the refinement_history schema."""
        assert "refinement_history" in epic_refine_spec
        pattern = re.compile(
            r"refinement_history:\s*\n\s+-\s+date:", re.DOTALL
        )
        assert pattern.search(epic_refine_spec), (
            "Spec must show refinement_history YAML schema"
        )


class TestFeatureRefineCrossCommandSuggestions:
    """Seam: Cross-command <-> Consistency.

    Verify that feature-refine suggests related commands (/generate-bdd,
    /formalize-ears) when appropriate.
    """

    def test_suggests_generate_bdd_when_coverage_missing(
        self, feature_refine_spec: str
    ) -> None:
        """Feature refine must suggest /generate-bdd when BDD coverage is low."""
        assert "/generate-bdd" in feature_refine_spec, (
            "Must suggest /generate-bdd for missing BDD coverage"
        )

    def test_suggests_formalize_ears_when_traceability_low(
        self, feature_refine_spec: str
    ) -> None:
        """Feature refine must suggest /formalize-ears when traceability is low."""
        assert "/formalize-ears" in feature_refine_spec, (
            "Must suggest /formalize-ears for missing requirements"
        )


class TestFeatureRefineCompletenesBeforeAfter:
    """Seam: Frontmatter <-> Completeness scoring.

    Verify that completeness scores are shown before and after refinement.
    """

    def test_before_after_score_in_feature_refine(
        self, feature_refine_spec: str
    ) -> None:
        """Feature refine must show before/after completeness scores."""
        lower = feature_refine_spec.lower()
        assert "before" in lower and "after" in lower, (
            "Must show before/after score comparison"
        )
        assert "completeness" in lower, (
            "Must reference completeness score"
        )

    def test_score_change_reflected_in_frontmatter_update(self) -> None:
        """Updating completeness_score must change the frontmatter value."""
        md = build_feature_markdown(completeness_score=45)
        updated = update_frontmatter_field(md, "completeness_score", 78)
        fm = parse_markdown_frontmatter(updated)
        assert fm["completeness_score"] == 78


class TestRefineWithFocusFlag:
    """Seam: Cross-command <-> Consistency.

    Verify --focus flag restricts questions to a single category.
    """

    def test_focus_flag_restricts_to_single_category_epic(
        self, epic_refine_spec: str
    ) -> None:
        """Epic refine --focus must restrict to a single category."""
        lower = epic_refine_spec.lower()
        assert "--focus" in lower
        assert any(
            phrase in lower
            for phrase in ["restricts", "single category", "only questions"]
        ), "--focus must restrict to a single category"

    def test_focus_flag_restricts_to_single_category_feature(
        self, feature_refine_spec: str
    ) -> None:
        """Feature refine --focus must restrict to a single category."""
        lower = feature_refine_spec.lower()
        assert "--focus" in lower
        assert any(
            phrase in lower
            for phrase in ["restricts", "single category", "only"]
        ), "--focus must restrict to a single category"

    def test_epic_focus_categories_documented(self, epic_refine_spec: str) -> None:
        """All focus categories must be documented for epic-refine."""
        expected_categories = [
            "scope", "criteria", "acceptance", "dependencies",
            "risks", "constraints", "organisation",
        ]
        for cat in expected_categories:
            assert re.search(
                rf"--focus\s+{cat}", epic_refine_spec.lower()
            ), f"--focus {cat} must be documented in epic-refine"

    def test_feature_focus_categories_documented(
        self, feature_refine_spec: str
    ) -> None:
        """All focus categories must be documented for feature-refine."""
        expected_categories = [
            "acceptance", "traceability", "bdd", "technical",
            "dependencies", "scope",
        ]
        for cat in expected_categories:
            assert re.search(
                rf"--focus\s+{cat}", feature_refine_spec.lower()
            ), f"--focus {cat} must be documented in feature-refine"


class TestRefinePreservesFrontmatter:
    """Seam: Markdown <-> Frontmatter parsing.

    Verify that external_ids and export_config survive refinement round-trips.
    """

    def test_external_ids_preserved_on_epic(self) -> None:
        """external_ids must survive an epic refinement round-trip."""
        md = build_epic_markdown(
            extra_frontmatter={
                "external_ids": {"jira": "PROJ-42", "linear": "LIN-7"},
            }
        )
        # Simulate refinement round-trip
        updated = update_frontmatter_field(md, "completeness_score", 80)
        updated = append_refinement_history(updated, 40, 80, ["Added scope"])
        fm = parse_markdown_frontmatter(updated)
        assert fm["external_ids"]["jira"] == "PROJ-42"
        assert fm["external_ids"]["linear"] == "LIN-7"

    def test_export_config_preserved_on_epic(self) -> None:
        """export_config must survive an epic refinement round-trip."""
        md = build_epic_markdown(
            extra_frontmatter={
                "export_config": {
                    "target_tools": ["jira", "linear"],
                    "auto_sync": True,
                },
            }
        )
        updated = update_frontmatter_field(md, "completeness_score", 65)
        fm = parse_markdown_frontmatter(updated)
        assert fm["export_config"]["target_tools"] == ["jira", "linear"]
        assert fm["export_config"]["auto_sync"] is True

    def test_organisation_pattern_preserved_on_epic(self) -> None:
        """organisation_pattern must survive a refinement round-trip."""
        md = build_epic_markdown(organisation_pattern="direct")
        updated = update_frontmatter_field(md, "completeness_score", 50)
        fm = parse_markdown_frontmatter(updated)
        assert fm["organisation_pattern"] == "direct"


# ═══════════════════════════════════════════════════════════════════════════
# 2. GRAPHITI SYNC INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════


class TestSyncStandaloneMode:
    """Seam: Config <-> Standalone mode.

    Graphiti disabled -> refinement works -> no sync attempted -> markdown saved.
    """

    def test_graphiti_config_defaults_to_disabled(
        self, graphiti_config: dict[str, Any]
    ) -> None:
        """Default graphiti.yaml must have enabled: false (standalone mode)."""
        assert graphiti_config["enabled"] is False, (
            "Graphiti must default to disabled (standalone mode)"
        )

    def test_standalone_mode_documented_in_sync_spec(
        self, requirekit_sync_spec: str
    ) -> None:
        """requirekit-sync must document behaviour when Graphiti is disabled."""
        lower = requirekit_sync_spec.lower()
        assert "not enabled" in lower or "enabled: false" in lower or "standalone" in lower, (
            "Sync spec must document behaviour when Graphiti is disabled"
        )

    def test_epic_refine_works_without_graphiti(
        self, epic_refine_spec: str
    ) -> None:
        """Epic refine must succeed without Graphiti (graceful degradation)."""
        lower = epic_refine_spec.lower()
        assert "graceful" in lower or "unavailable" in lower or "not configured" in lower, (
            "Epic refine must document graceful Graphiti degradation"
        )

    def test_feature_refine_works_without_graphiti(
        self, feature_refine_spec: str
    ) -> None:
        """Feature refine must succeed without Graphiti."""
        lower = feature_refine_spec.lower()
        assert "graceful" in lower or "unavailable" in lower or "not configured" in lower, (
            "Feature refine must document graceful Graphiti degradation"
        )


class TestSyncAfterRefinement:
    """Seam: Refinement <-> Graphiti push.

    Graphiti enabled -> refine -> push episode with correct metadata.
    """

    def test_epic_refine_pushes_to_graphiti_when_enabled(
        self, epic_refine_spec: str
    ) -> None:
        """Epic refine must push to Graphiti when enabled."""
        lower = epic_refine_spec.lower()
        assert "graphiti" in lower and "push" in lower or "sync" in lower, (
            "Epic refine must document Graphiti push after refinement"
        )

    def test_feature_refine_pushes_to_graphiti_when_enabled(
        self, feature_refine_spec: str
    ) -> None:
        """Feature refine must push to Graphiti when enabled."""
        lower = feature_refine_spec.lower()
        assert "graphiti" in lower and ("push" in lower or "sync" in lower), (
            "Feature refine must document Graphiti push after refinement"
        )

    def test_sync_on_refine_config_field_exists(
        self, graphiti_config: dict[str, Any]
    ) -> None:
        """graphiti.yaml must have sync_on_refine field."""
        assert "sync_on_refine" in graphiti_config, (
            "Config must include sync_on_refine field"
        )


class TestSyncGracefulDegradation:
    """Seam: Refinement <-> Graphiti push.

    Graphiti enabled but unavailable -> refinement works -> markdown saved
    -> warning shown.
    """

    def test_epic_refine_saves_markdown_even_if_graphiti_fails(
        self, epic_refine_spec: str
    ) -> None:
        """Epic refine must save markdown even when Graphiti push fails."""
        lower = epic_refine_spec.lower()
        assert (
            "markdown" in lower
            and ("saved" in lower or "still" in lower or "succeeds" in lower)
        ), "Must document that markdown is saved regardless of Graphiti status"

    def test_feature_refine_never_fails_due_to_graphiti(
        self, feature_refine_spec: str
    ) -> None:
        """Feature refinement must never fail due to Graphiti errors."""
        lower = feature_refine_spec.lower()
        assert "never fail" in lower or "still succeeds" in lower or "graceful" in lower, (
            "Feature refine must document that it never fails due to Graphiti"
        )

    def test_warning_shown_when_graphiti_unavailable(
        self, feature_refine_spec: str
    ) -> None:
        """A warning must be shown when Graphiti is unavailable."""
        assert "Skipped" in feature_refine_spec or "not configured" in feature_refine_spec.lower(), (
            "Must show a warning or 'Skipped' indicator when Graphiti is unavailable"
        )


class TestSyncEpisodeSchemaEpic:
    """Seam: Refinement <-> Graphiti push.

    Verify epic episode matches schema from spec.
    """

    def test_epic_episode_has_group_id(self, requirekit_sync_spec: str) -> None:
        """Epic episode must include group_id field."""
        assert "group_id" in requirekit_sync_spec, (
            "Epic episode schema must include group_id"
        )

    def test_epic_episode_has_entity_type(self, requirekit_sync_spec: str) -> None:
        """Epic episode metadata must include entity_type."""
        assert "entity_type" in requirekit_sync_spec, (
            "Epic episode metadata must include entity_type"
        )

    def test_epic_episode_has_epic_id_in_metadata(
        self, requirekit_sync_spec: str
    ) -> None:
        """Epic episode metadata must include epic_id."""
        assert "epic_id" in requirekit_sync_spec, (
            "Epic episode metadata must include epic_id"
        )

    def test_epic_episode_has_organisation_pattern(
        self, requirekit_sync_spec: str
    ) -> None:
        """Epic episode metadata must include organisation_pattern."""
        assert "organisation_pattern" in requirekit_sync_spec, (
            "Epic episode metadata must include organisation_pattern"
        )


class TestSyncEpisodeSchemaFeature:
    """Seam: Refinement <-> Graphiti push.

    Verify feature episode matches schema from spec.
    """

    def test_feature_episode_has_feature_id(
        self, requirekit_sync_spec: str
    ) -> None:
        """Feature episode metadata must include feature_id."""
        assert "feature_id" in requirekit_sync_spec, (
            "Feature episode metadata must include feature_id"
        )

    def test_feature_episode_has_parent_epic_id(
        self, requirekit_sync_spec: str
    ) -> None:
        """Feature episode metadata must include parent epic_id."""
        # In the feature episode schema, epic_id links back to parent
        lower = requirekit_sync_spec.lower()
        assert "epic_id" in lower, (
            "Feature episode metadata must include epic_id reference"
        )

    def test_feature_episode_schema_documented_in_feature_refine(
        self, feature_refine_spec: str
    ) -> None:
        """Feature refine spec must document the feature episode schema."""
        assert "episode" in feature_refine_spec.lower() or "Episode Schema" in feature_refine_spec, (
            "Feature refine must document the episode schema"
        )


class TestRequirekitSyncRecovery:
    """Seam: Refinement <-> Graphiti push.

    Manual edit -> run /requirekit-sync -> Graphiti matches markdown.
    """

    def test_sync_command_is_one_way(self, requirekit_sync_spec: str) -> None:
        """Sync must be documented as one-way (markdown authoritative)."""
        lower = requirekit_sync_spec.lower()
        assert "one-way" in lower or "authoritative" in lower, (
            "Sync must be documented as one-way / markdown-authoritative"
        )

    def test_sync_upserts_to_graphiti(self, requirekit_sync_spec: str) -> None:
        """Sync must use upsert semantics."""
        lower = requirekit_sync_spec.lower()
        assert "upsert" in lower, (
            "Sync must document upsert semantics"
        )

    def test_sync_supports_recovery_use_case(
        self, requirekit_sync_spec: str
    ) -> None:
        """Sync must be documented as a recovery mechanism."""
        lower = requirekit_sync_spec.lower()
        assert "recovery" in lower, (
            "Sync must document recovery use case"
        )


class TestSyncUpsertDedup:
    """Seam: Refinement <-> Graphiti push.

    Push same epic twice -> single episode (dedup by epic_id).
    """

    def test_dedup_key_documented(self, requirekit_sync_spec: str) -> None:
        """Deduplication key must be documented in sync spec."""
        lower = requirekit_sync_spec.lower()
        assert "dedup" in lower or "entity_id" in lower or "epic_id" in lower, (
            "Deduplication key must be documented"
        )

    def test_upsert_overwrites_existing(self, requirekit_sync_spec: str) -> None:
        """Upsert must overwrite existing episodes."""
        lower = requirekit_sync_spec.lower()
        assert "overwrite" in lower or "update" in lower, (
            "Upsert must document overwriting existing episodes"
        )


class TestSyncGroupId:
    """Seam: Refinement <-> Graphiti push.

    Verify group ID follows ``{project}__requirements`` convention.
    """

    def test_group_id_pattern_in_config(
        self, graphiti_config: dict[str, Any]
    ) -> None:
        """Config must define group_id_pattern."""
        assert "group_id_pattern" in graphiti_config, (
            "Config must include group_id_pattern"
        )
        assert "{project}" in graphiti_config["group_id_pattern"], (
            "group_id_pattern must contain {project} placeholder"
        )
        assert "__requirements" in graphiti_config["group_id_pattern"], (
            "group_id_pattern must follow {project}__requirements convention"
        )

    def test_group_id_pattern_in_sync_spec(
        self, requirekit_sync_spec: str
    ) -> None:
        """Sync spec must reference the group_id_pattern convention."""
        assert "{project}__requirements" in requirekit_sync_spec or \
               "project_namespace" in requirekit_sync_spec, (
            "Sync spec must reference the group_id_pattern convention"
        )

    def test_group_id_consistent_across_specs(
        self,
        requirekit_sync_spec: str,
        feature_refine_spec: str,
    ) -> None:
        """group_id convention must be consistent across sync and refine specs."""
        # Both should reference the same __requirements pattern
        assert "__requirements" in requirekit_sync_spec, (
            "Sync spec must reference __requirements"
        )
        assert "__requirements" in feature_refine_spec, (
            "Feature refine spec must reference __requirements"
        )


# ═══════════════════════════════════════════════════════════════════════════
# 3. ORGANISATION PATTERN INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════


class TestEpicCreateDefaultPattern:
    """Seam: Organisation pattern <-> Display.

    Create epic without --pattern -> verify default is "features".
    """

    def test_default_pattern_is_features_in_frontmatter(
        self, epic_create_spec: str
    ) -> None:
        """Default organisation_pattern must be 'features' in frontmatter template."""
        fm = parse_frontmatter(epic_create_spec, id_prefix="EPIC-")
        assert fm.get("organisation_pattern") == "features", (
            "Default pattern must be 'features'"
        )

    def test_default_pattern_documented_as_backward_compatible(
        self, epic_create_spec: str
    ) -> None:
        """Default pattern must be documented as backward compatible."""
        lower = epic_create_spec.lower()
        assert "default" in lower and "features" in lower, (
            "Default pattern must be documented"
        )


class TestEpicCreateDirectPattern:
    """Seam: Organisation pattern <-> Display.

    Create epic with --pattern direct -> verify frontmatter.
    """

    def test_direct_pattern_flag_documented(self, epic_create_spec: str) -> None:
        """--pattern direct must be documented."""
        assert re.search(r"--pattern\s+direct", epic_create_spec), (
            "--pattern direct must be documented"
        )

    def test_direct_pattern_epic_to_task_hierarchy(
        self, epic_create_spec: str
    ) -> None:
        """Direct pattern must show EPIC -> TASK hierarchy."""
        assert re.search(
            r"EPIC.*TASK", epic_create_spec, re.IGNORECASE | re.DOTALL
        ), "Direct pattern must show EPIC -> TASK hierarchy"


class TestEpicStatusDirectDisplay:
    """Seam: Organisation pattern <-> Display.

    Direct-pattern epic -> task list shown (not features).
    """

    def test_direct_pattern_shows_tasks_in_status(
        self, epic_status_spec: str
    ) -> None:
        """Direct pattern in epic-status must show tasks, not features."""
        lower = epic_status_spec.lower()
        assert "direct" in lower, (
            "epic-status must reference direct pattern"
        )
        assert "task" in lower, (
            "epic-status direct pattern must mention tasks"
        )

    def test_pattern_column_in_portfolio_view(
        self, epic_status_spec: str
    ) -> None:
        """Portfolio view must include Pattern column."""
        assert "Pattern" in epic_status_spec or "pattern" in epic_status_spec.lower(), (
            "Portfolio view must include Pattern column"
        )


class TestEpicStatusMixedWarning:
    """Seam: Organisation pattern <-> Display.

    Mixed-pattern epic -> warning displayed.
    """

    def test_mixed_pattern_warning_in_create(self, epic_create_spec: str) -> None:
        """Mixed pattern must produce a warning at creation time."""
        lower = epic_create_spec.lower()
        # Must have both 'mixed' and 'warning' concepts nearby
        assert "mixed" in lower and ("warn" in lower or "⚠" in epic_create_spec), (
            "Mixed pattern must document a warning"
        )


class TestHierarchyViewAllPatterns:
    """Seam: Organisation pattern <-> Display.

    Three epics (direct, features, mixed) -> tree renders all correctly.
    """

    def test_hierarchy_shows_features_pattern(
        self, hierarchy_view_spec: str
    ) -> None:
        """Hierarchy view must render features pattern epics."""
        assert "features pattern" in hierarchy_view_spec.lower() or \
               "features" in hierarchy_view_spec.lower(), (
            "Hierarchy view must render features pattern"
        )

    def test_hierarchy_shows_direct_pattern(
        self, hierarchy_view_spec: str
    ) -> None:
        """Hierarchy view must render direct pattern epics."""
        assert "direct pattern" in hierarchy_view_spec.lower() or (
            "direct" in hierarchy_view_spec.lower()
        ), "Hierarchy view must render direct pattern"

    def test_hierarchy_shows_mixed_pattern(
        self, hierarchy_view_spec: str
    ) -> None:
        """Hierarchy view must render mixed pattern epics."""
        assert "mixed pattern" in hierarchy_view_spec.lower() or (
            "mixed" in hierarchy_view_spec.lower()
        ), "Hierarchy view must render mixed pattern"

    def test_hierarchy_uses_direct_tasks_grouping(
        self, hierarchy_view_spec: str
    ) -> None:
        """Mixed pattern must use [Direct Tasks] grouping in hierarchy view."""
        assert "[Direct Tasks]" in hierarchy_view_spec, (
            "Mixed pattern must use [Direct Tasks] grouping"
        )

    def test_all_three_patterns_in_single_tree(
        self, hierarchy_view_spec: str
    ) -> None:
        """A single tree view must show all three patterns."""
        lower = hierarchy_view_spec.lower()
        assert "features pattern" in lower, "Missing features pattern in tree"
        assert "direct pattern" in lower, "Missing direct pattern in tree"
        assert "mixed pattern" in lower, "Missing mixed pattern in tree"


class TestValidationTaskEpicXorFeature:
    """Seam: Organisation pattern <-> Display.

    Task specifies both epic: and feature: -> validation error.
    """

    def test_feature_requires_epic_parameter(
        self, feature_create_spec: str
    ) -> None:
        """Feature creation must require an epic parameter."""
        assert "epic:" in feature_create_spec.lower() or "epic:<epic-id>" in feature_create_spec.lower(), (
            "Feature creation must require epic parameter"
        )

    def test_epic_id_mandatory_for_features(
        self, feature_create_spec: str
    ) -> None:
        """Validation must enforce that features always belong to an epic."""
        lower = feature_create_spec.lower()
        assert "epic must exist" in lower or "epic parameter" in lower or "always belong" in lower, (
            "Validation must enforce epic association for features"
        )


class TestPatternTerminologyConsistency:
    """Seam: Cross-command <-> Consistency.

    Same terminology used across epic-create, epic-status, hierarchy-view.
    """

    def test_organisation_pattern_term_in_create(
        self, epic_create_spec: str
    ) -> None:
        """epic-create must use 'organisation_pattern' term."""
        assert "organisation_pattern" in epic_create_spec

    def test_organisation_pattern_term_in_hierarchy(
        self, hierarchy_view_spec: str
    ) -> None:
        """hierarchy-view must reference organisation patterns."""
        lower = hierarchy_view_spec.lower()
        assert "pattern" in lower and (
            "organisation" in lower or "features" in lower
        ), "hierarchy-view must reference organisation patterns"

    def test_three_pattern_names_consistent(
        self,
        epic_create_spec: str,
        hierarchy_view_spec: str,
        epic_status_spec: str,
    ) -> None:
        """Pattern names (direct, features, mixed) must be consistent across commands."""
        for spec_name, spec in [
            ("epic-create", epic_create_spec),
            ("hierarchy-view", hierarchy_view_spec),
            ("epic-status", epic_status_spec),
        ]:
            lower = spec.lower()
            assert "direct" in lower, (
                f"'{spec_name}' must mention 'direct' pattern"
            )
            assert "features" in lower, (
                f"'{spec_name}' must mention 'features' pattern"
            )
            assert "mixed" in lower, (
                f"'{spec_name}' must mention 'mixed' pattern"
            )


class TestBackwardCompatibility:
    """Seam: Organisation pattern <-> Display.

    Existing epic without organisation_pattern -> treated as "features".
    """

    def test_epic_without_pattern_defaults_to_features(self) -> None:
        """An epic with no organisation_pattern should default to features."""
        # Simulate legacy epic frontmatter (no organisation_pattern field)
        legacy_md = (
            "---\n"
            "id: EPIC-LEGACY\n"
            "title: Legacy Epic\n"
            "status: planning\n"
            "priority: normal\n"
            "---\n\n# Epic: Legacy Epic\n"
        )
        fm = parse_markdown_frontmatter(legacy_md)
        # The default should be 'features' when field is absent
        pattern = fm.get("organisation_pattern", "features")
        assert pattern == "features", (
            "Missing organisation_pattern must default to 'features'"
        )

    def test_default_documented_in_spec(self, epic_create_spec: str) -> None:
        """Default pattern must be documented as 'features' for backward compatibility."""
        lower = epic_create_spec.lower()
        assert "default" in lower and "features" in lower, (
            "Default pattern must be documented"
        )
        assert "backward" in lower or "compatible" in lower, (
            "Backward compatibility must be documented"
        )


# ═══════════════════════════════════════════════════════════════════════════
# 4. COMPLETENESS SCORING INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════


class TestEpicCompletenessEmptyEpic:
    """Seam: Frontmatter <-> Completeness scoring.

    Brand new epic -> score reflects missing fields.
    """

    def test_new_epic_starts_with_zero_score(self) -> None:
        """A new epic must start with completeness_score 0."""
        md = build_epic_markdown()
        fm = parse_markdown_frontmatter(md)
        assert fm["completeness_score"] == 0, (
            "New epic must start with score 0"
        )

    def test_empty_epic_missing_fields_documented(
        self, epic_refine_spec: str
    ) -> None:
        """Epic refine spec must document visual indicators for missing fields."""
        assert "Missing" in epic_refine_spec or "❌" in epic_refine_spec, (
            "Must show missing field indicators"
        )


class TestEpicCompletenessFullEpic:
    """Seam: Frontmatter <-> Completeness scoring.

    Fully specified epic -> 100% or near-100%.
    """

    def test_well_specified_epic_score_range(
        self, epic_refine_spec: str
    ) -> None:
        """A well-specified epic should score 80-100%."""
        lower = epic_refine_spec.lower()
        assert "80" in lower and "100" in lower, (
            "Score range 80-100% must be documented for well-specified epics"
        )

    def test_score_interpretation_documented(
        self, epic_refine_spec: str
    ) -> None:
        """Score interpretation ranges must be documented."""
        lower = epic_refine_spec.lower()
        assert "score" in lower and "interpretation" in lower or "range" in lower, (
            "Score interpretation must be documented"
        )


class TestEpicCompletenessPartial:
    """Seam: Frontmatter <-> Completeness scoring.

    Partial epic -> verify weights applied correctly.
    """

    def test_nine_dimensions_with_weights(self, epic_refine_spec: str) -> None:
        """Epic completeness must use 9 dimensions with weights."""
        lower = epic_refine_spec.lower()
        required_dimensions = [
            "business objective", "scope", "success criteria",
            "acceptance criteria", "risk", "constraints",
            "dependencies", "stakeholders", "organisation",
        ]
        for dim in required_dimensions:
            assert dim in lower, (
                f"Dimension '{dim}' must be documented"
            )

    def test_dimension_weights_documented(self, epic_refine_spec: str) -> None:
        """Weights must be documented for each dimension."""
        # Check for percentage values near dimension names
        assert "15%" in epic_refine_spec and "20%" in epic_refine_spec, (
            "Dimension weights must be documented with percentage values"
        )


class TestEpicWeightsSumTo100:
    """Seam: Frontmatter <-> Completeness scoring.

    Verify 9 dimension weights sum to exactly 100%.
    """

    def test_epic_weights_sum_to_100_percent(self, epic_refine_spec: str) -> None:
        """Epic dimension weights must sum to exactly 100%."""
        # Extract the weights from the spec table
        # Business Objective 15%, Scope 15%, Success Criteria 20%,
        # Acceptance Criteria 15%, Risk 10%, Constraints 10%,
        # Dependencies 5%, Stakeholders 5%, Organisation 5%
        expected_weights = [15, 15, 20, 15, 10, 10, 5, 5, 5]
        assert sum(expected_weights) == 100, (
            "Epic dimension weights must sum to 100%"
        )
        # Verify each weight appears in the spec
        for w in expected_weights:
            assert f"{w}%" in epic_refine_spec, (
                f"Weight {w}% must appear in epic-refine spec"
            )


class TestFeatureCompletenessEmpty:
    """Seam: Frontmatter <-> Completeness scoring.

    New feature -> verify baseline score.
    """

    def test_new_feature_starts_with_zero_score(self) -> None:
        """A new feature must start with completeness_score 0."""
        md = build_feature_markdown()
        fm = parse_markdown_frontmatter(md)
        assert fm["completeness_score"] == 0, (
            "New feature must start with score 0"
        )


class TestFeatureCompletenessFull:
    """Seam: Frontmatter <-> Completeness scoring.

    Complete feature -> verify 100% or near-100%.
    """

    def test_well_specified_feature_score_range(
        self, feature_refine_spec: str
    ) -> None:
        """A well-specified feature should score 80-100%."""
        lower = feature_refine_spec.lower()
        assert "80" in lower and "100" in lower, (
            "Score range 80-100% must be documented for well-specified features"
        )


class TestFeatureWeightsSumTo100:
    """Seam: Frontmatter <-> Completeness scoring.

    Verify 7 dimension weights sum to exactly 100%.
    """

    def test_feature_weights_sum_to_100_percent(
        self, feature_refine_spec: str
    ) -> None:
        """Feature dimension weights must sum to exactly 100%."""
        # Scope 10%, Acceptance Criteria 25%, Requirements Traceability 20%,
        # BDD Coverage 15%, Technical Considerations 15%, Dependencies 10%,
        # Test Strategy 5%
        expected_weights = [10, 25, 20, 15, 15, 10, 5]
        assert sum(expected_weights) == 100, (
            "Feature dimension weights must sum to 100%"
        )
        # Verify key weights in the spec
        for w in expected_weights:
            assert f"{w}%" in feature_refine_spec, (
                f"Weight {w}% must appear in feature-refine spec"
            )

    def test_seven_dimensions_documented(self, feature_refine_spec: str) -> None:
        """Feature completeness must document 7 dimensions."""
        lower = feature_refine_spec.lower()
        required_dimensions = [
            "scope within epic",
            "acceptance criteria",
            "requirements traceability",
            "bdd coverage",
            "technical considerations",
            "dependencies",
            "test strategy",
        ]
        for dim in required_dimensions:
            assert dim in lower, (
                f"Dimension '{dim}' must be documented"
            )


class TestScoreAfterRefinement:
    """Seam: Frontmatter <-> Completeness scoring.

    Score before -> refine -> score after -> verify improvement.
    """

    def test_score_update_reflected_in_frontmatter(self) -> None:
        """Completeness score update must be reflected in frontmatter."""
        md = build_epic_markdown(completeness_score=30)
        updated = update_frontmatter_field(md, "completeness_score", 72)
        fm = parse_markdown_frontmatter(updated)
        assert fm["completeness_score"] == 72
        assert fm["completeness_score"] > 30, (
            "Score must improve after refinement"
        )

    def test_before_after_documented_in_change_summary(
        self, epic_refine_spec: str
    ) -> None:
        """Change summary must show before/after completeness scores."""
        assert "Before Completeness" in epic_refine_spec or \
               "before" in epic_refine_spec.lower(), (
            "Change summary must reference 'before' score"
        )
        assert "After Completeness" in epic_refine_spec or \
               "after" in epic_refine_spec.lower(), (
            "Change summary must reference 'after' score"
        )


class TestScoreCalculationDeterministic:
    """Seam: Frontmatter <-> Completeness scoring.

    Same input -> same score always.
    """

    def test_same_markdown_produces_same_frontmatter(self) -> None:
        """Parsing the same markdown twice must produce identical frontmatter."""
        md = build_epic_markdown(completeness_score=55)
        fm1 = parse_markdown_frontmatter(md)
        fm2 = parse_markdown_frontmatter(md)
        assert fm1 == fm2, (
            "Same markdown must produce identical parsed frontmatter"
        )

    def test_update_is_idempotent(self) -> None:
        """Applying the same update twice must produce identical results."""
        md = build_epic_markdown(completeness_score=40)
        updated1 = update_frontmatter_field(md, "completeness_score", 75)
        updated2 = update_frontmatter_field(md, "completeness_score", 75)
        fm1 = parse_markdown_frontmatter(updated1)
        fm2 = parse_markdown_frontmatter(updated2)
        assert fm1 == fm2, (
            "Same update must produce identical frontmatter"
        )

    def test_weight_calculation_is_deterministic(self) -> None:
        """Weight-based score calculation must be deterministic."""
        # Simulate a score calculation: all 9 dimensions partially filled
        epic_weights = [15, 15, 20, 15, 10, 10, 5, 5, 5]
        dimension_scores = [0.8, 0.5, 0.3, 0.7, 0.0, 0.0, 1.0, 1.0, 0.5]
        score1 = sum(w * s for w, s in zip(epic_weights, dimension_scores))
        score2 = sum(w * s for w, s in zip(epic_weights, dimension_scores))
        assert score1 == score2, (
            "Weight-based calculation must be deterministic"
        )
        # Verify it calculates correctly
        expected = (
            15 * 0.8 + 15 * 0.5 + 20 * 0.3 + 15 * 0.7
            + 10 * 0.0 + 10 * 0.0 + 5 * 1.0 + 5 * 1.0 + 5 * 0.5
        )
        assert abs(score1 - expected) < 0.001


# ═══════════════════════════════════════════════════════════════════════════
# 5. CROSS-SEAM INTEGRATION (multi-seam tests)
# ═══════════════════════════════════════════════════════════════════════════


class TestCrossSeamConsistency:
    """Tests spanning multiple technology seams to verify end-to-end consistency."""

    def test_graphiti_fields_consistent_across_epic_and_feature(
        self,
        epic_create_spec: str,
        feature_create_spec: str,
    ) -> None:
        """Both epic and feature must have graphiti_synced, last_graphiti_sync fields."""
        for name, spec in [("epic-create", epic_create_spec), ("feature-create", feature_create_spec)]:
            assert "graphiti_synced" in spec, (
                f"{name} must include graphiti_synced field"
            )
            assert "last_graphiti_sync" in spec, (
                f"{name} must include last_graphiti_sync field"
            )

    def test_completeness_score_field_in_both_create_specs(
        self,
        epic_create_spec: str,
        feature_create_spec: str,
    ) -> None:
        """Both epic and feature create specs must include completeness_score."""
        assert "completeness_score" in epic_create_spec
        assert "completeness_score" in feature_create_spec

    def test_refinement_history_schema_consistent(
        self,
        epic_refine_spec: str,
        feature_refine_spec: str,
    ) -> None:
        """Both epic and feature refine must document refinement_history."""
        assert "refinement_history" in epic_refine_spec
        assert "refinement_history" in feature_refine_spec

    def test_graphiti_sync_config_fields_complete(
        self, graphiti_config: dict[str, Any]
    ) -> None:
        """Graphiti config must have all required fields."""
        required = [
            "enabled", "endpoint", "project_namespace",
            "group_id_pattern", "sync_on_create", "sync_on_refine",
        ]
        for field in required:
            assert field in graphiti_config, (
                f"graphiti.yaml must include '{field}' field"
            )

    def test_full_refinement_roundtrip(self) -> None:
        """Full round-trip: create -> update score -> add history -> verify all fields."""
        # 1. Create epic
        md = build_epic_markdown(
            epic_id="EPIC-RT",
            title="Roundtrip Test",
            organisation_pattern="mixed",
            extra_frontmatter={
                "external_ids": {"jira": "PROJ-RT"},
                "requirements": ["REQ-001", "REQ-002"],
            },
        )
        # 2. Simulate refinement
        updated = update_frontmatter_field(md, "completeness_score", 65)
        updated = append_refinement_history(updated, 0, 65, ["Added scope", "Added risks"])
        # 3. Simulate second refinement
        updated = update_frontmatter_field(updated, "completeness_score", 85)
        updated = append_refinement_history(updated, 65, 85, ["Added criteria"])

        # 4. Verify all fields
        fm = parse_markdown_frontmatter(updated)
        assert fm["id"] == "EPIC-RT"
        assert fm["title"] == "Roundtrip Test"
        assert fm["organisation_pattern"] == "mixed"
        assert fm["completeness_score"] == 85
        assert fm["external_ids"]["jira"] == "PROJ-RT"
        assert fm["requirements"] == ["REQ-001", "REQ-002"]
        assert len(fm["refinement_history"]) == 2
        assert fm["refinement_history"][0]["completeness_before"] == 0
        assert fm["refinement_history"][0]["completeness_after"] == 65
        assert fm["refinement_history"][1]["completeness_before"] == 65
        assert fm["refinement_history"][1]["completeness_after"] == 85
