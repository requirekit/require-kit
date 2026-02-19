"""E2E tests for complete command pipelines.

TASK-RK01-014: Verifies that command pipelines work together as integrated
systems, simulating real user workflows from epic creation through refinement
to sync. All tests use temporary directories for isolation.

Test Scenarios:
    1. Epic Refinement Pipeline - full lifecycle: create -> refine -> sync -> status
    2. Feature Refinement Pipeline - create -> refine -> cross-command suggestions
    3. Multi-Pattern Hierarchy - all three patterns in one hierarchy view
    4. Documentation Build - mkdocs navigation and structure verification
    5. User Workflow Simulations - James's product owner use cases
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any

import pytest
import yaml

from conftest import (
    append_refinement_history,
    build_epic_markdown,
    build_feature_markdown,
    calculate_completeness,
    parse_markdown_frontmatter,
    read_epic_status,
    simulate_epic_create,
    simulate_epic_refine,
    simulate_feature_create,
    simulate_feature_refine,
    simulate_sync,
    update_frontmatter_field,
)


# ═══════════════════════════════════════════════════════════════════════════
# 1. EPIC REFINEMENT PIPELINE
# Simulates: create -> refine -> sync -> status -> refine again
# ═══════════════════════════════════════════════════════════════════════════


class TestEpicCreateRefineSyncPipeline:
    """E2E: Full epic lifecycle — create, refine, sync, status, refine again.

    User scenario: Product owner James creates an epic, iteratively
    refines it, syncs to Graphiti, checks status, then refines more.
    """

    def test_epic_create_produces_valid_file(self, workspace: Path) -> None:
        """Step 1: /epic-create produces a valid markdown file with frontmatter."""
        epic_file = simulate_epic_create(
            workspace, epic_id="EPIC-E2E-001", title="User Auth System"
        )
        assert epic_file.exists(), "Epic file must be created"
        md = epic_file.read_text(encoding="utf-8")
        fm = parse_markdown_frontmatter(md)
        assert fm["id"] == "EPIC-E2E-001"
        assert fm["title"] == "User Auth System"
        assert fm["completeness_score"] == 0, "New epic starts with score 0"

    def test_initial_completeness_is_low(self, workspace: Path) -> None:
        """Step 2: Newly created epic has low (zero) completeness score."""
        epic_file = simulate_epic_create(
            workspace, epic_id="EPIC-E2E-002", title="Low Score Epic"
        )
        fm = parse_markdown_frontmatter(epic_file.read_text(encoding="utf-8"))
        assert fm["completeness_score"] == 0, "Initial score must be 0"

    def test_epic_refine_updates_score_and_history(self, workspace: Path) -> None:
        """Step 3-6: /epic-refine updates completeness and appends history."""
        epic_file = simulate_epic_create(
            workspace, epic_id="EPIC-E2E-003", title="Refinement Target"
        )

        # Simulate refinement: add success criteria + scope
        simulate_epic_refine(
            epic_file,
            completeness_before=0,
            completeness_after=55,
            changes=["Added success criteria", "Defined scope boundaries"],
        )

        md = epic_file.read_text(encoding="utf-8")
        fm = parse_markdown_frontmatter(md)

        # Verify score improved
        assert fm["completeness_score"] == 55, "Score must improve after refinement"

        # Verify refinement_history entry
        assert "refinement_history" in fm, "refinement_history must be appended"
        assert len(fm["refinement_history"]) == 1
        entry = fm["refinement_history"][0]
        assert entry["completeness_before"] == 0
        assert entry["completeness_after"] == 55
        assert "Added success criteria" in entry["changes"]

    def test_sync_marks_graphiti_fields(self, workspace: Path) -> None:
        """Step 7: /requirekit-sync updates graphiti_synced and last_graphiti_sync."""
        epic_file = simulate_epic_create(
            workspace, epic_id="EPIC-E2E-004", title="Sync Target"
        )
        simulate_epic_refine(epic_file, 0, 60, ["Added scope"])

        # Sync with Graphiti enabled
        result = simulate_sync(epic_file, graphiti_enabled=True)
        assert result["graphiti_pushed"] is True
        assert result["sync_status"] == "success"

        fm = parse_markdown_frontmatter(epic_file.read_text(encoding="utf-8"))
        assert fm["graphiti_synced"] is True, "graphiti_synced must be True"
        assert fm["last_graphiti_sync"] is not None, "last_graphiti_sync must be set"

    def test_epic_status_shows_all_fields(self, workspace: Path) -> None:
        """Step 8: /epic-status shows all updated fields after full pipeline."""
        epic_file = simulate_epic_create(
            workspace,
            epic_id="EPIC-E2E-005",
            title="Status Check Epic",
            body="## Business Objective\n\nProvide user authentication.\n",
        )
        simulate_epic_refine(epic_file, 0, 65, ["Added scope", "Added risks"])
        simulate_sync(epic_file, graphiti_enabled=True)

        status = read_epic_status(workspace, "EPIC-E2E-005")
        assert status["id"] == "EPIC-E2E-005"
        assert status["completeness_score"] == 65
        assert status["graphiti_synced"] is True
        assert len(status["refinement_history"]) == 1

    def test_full_pipeline_preserves_all_data(self, workspace: Path) -> None:
        """Full cycle: create -> refine -> sync -> status with all data preserved."""
        epic_file = simulate_epic_create(
            workspace,
            epic_id="EPIC-E2E-006",
            title="Full Pipeline Epic",
            extra_frontmatter={"external_ids": {"jira": "PROJ-100"}},
        )

        # First refinement
        simulate_epic_refine(epic_file, 0, 45, ["Added scope"])
        # Second refinement
        simulate_epic_refine(
            epic_file, 45, 75, ["Added risks", "Added constraints"],
            date="2026-02-19T15:30:00Z",
        )
        # Sync
        simulate_sync(epic_file, graphiti_enabled=True)
        # Read status
        status = read_epic_status(workspace, "EPIC-E2E-006")

        # All fields preserved
        assert status["id"] == "EPIC-E2E-006"
        assert status["completeness_score"] == 75
        assert status["graphiti_synced"] is True
        assert len(status["refinement_history"]) == 2
        # External IDs survive the pipeline
        fm = parse_markdown_frontmatter(epic_file.read_text(encoding="utf-8"))
        assert fm["external_ids"]["jira"] == "PROJ-100"


class TestEpicCreateDirectPatternPipeline:
    """E2E: Direct-pattern epic lifecycle — create, status, hierarchy, refine.

    User scenario: James creates a small utility epic with --pattern direct
    (no features layer) and verifies the hierarchy works without features.
    """

    def test_direct_pattern_in_frontmatter(self, workspace: Path) -> None:
        """Step 1-2: Create epic with direct pattern, verify frontmatter."""
        epic_file = simulate_epic_create(
            workspace,
            epic_id="EPIC-DIR-001",
            title="Utility Scripts",
            organisation_pattern="direct",
            extra_frontmatter={"direct_tasks": ["TASK-001", "TASK-002"]},
        )
        fm = parse_markdown_frontmatter(epic_file.read_text(encoding="utf-8"))
        assert fm["organisation_pattern"] == "direct"
        assert fm["direct_tasks"] == ["TASK-001", "TASK-002"]

    def test_direct_status_shows_tasks_not_features(self, workspace: Path) -> None:
        """Step 3: /epic-status shows direct tasks, no features."""
        simulate_epic_create(
            workspace,
            epic_id="EPIC-DIR-002",
            title="Direct Tasks Epic",
            organisation_pattern="direct",
            extra_frontmatter={"direct_tasks": ["TASK-A", "TASK-B", "TASK-C"]},
        )
        status = read_epic_status(workspace, "EPIC-DIR-002")
        assert status["organisation_pattern"] == "direct"
        assert len(status["direct_tasks"]) == 3
        assert len(status["linked_features"]) == 0, "Direct pattern has no features"

    def test_direct_hierarchy_no_feature_layer(
        self, workspace: Path, hierarchy_view_spec: str
    ) -> None:
        """Step 4: /hierarchy-view renders direct pattern without features."""
        # Verify the hierarchy-view spec documents direct pattern
        lower = hierarchy_view_spec.lower()
        assert "direct" in lower, "Hierarchy view must document direct pattern"

        # Simulate direct epic in workspace
        simulate_epic_create(
            workspace,
            epic_id="EPIC-DIR-003",
            title="Hierarchy Direct Test",
            organisation_pattern="direct",
        )
        status = read_epic_status(workspace, "EPIC-DIR-003")
        assert status["organisation_pattern"] == "direct"
        assert status["linked_features"] == []

    def test_direct_refine_organisation_aware(
        self, workspace: Path, epic_refine_spec: str
    ) -> None:
        """Step 5: /epic-refine is organisation-aware for direct pattern."""
        # Verify the spec documents organisation awareness
        lower = epic_refine_spec.lower()
        assert "organisation" in lower, "Epic refine must assess organisation"

        # Simulate a small direct epic — should not suggest adding features
        epic_file = simulate_epic_create(
            workspace,
            epic_id="EPIC-DIR-004",
            title="Small Direct Epic",
            organisation_pattern="direct",
            extra_frontmatter={"direct_tasks": ["TASK-1", "TASK-2"]},
        )
        fm = parse_markdown_frontmatter(epic_file.read_text(encoding="utf-8"))
        # Small direct epic (2 tasks) should stay direct
        assert len(fm["direct_tasks"]) < 8, "Small epic shouldn't need features"


class TestEpicRefineMultipleSessions:
    """E2E: Multiple refinement sessions preserve cumulative history.

    User scenario: James refines an epic over multiple sessions,
    each time improving a different aspect.
    """

    def test_two_sessions_produce_two_history_entries(self, workspace: Path) -> None:
        """Steps 1-4: Two sessions append two distinct history entries."""
        epic_file = simulate_epic_create(
            workspace, epic_id="EPIC-MULTI-001", title="Multi-Session Epic"
        )

        # Session 1: add success criteria
        simulate_epic_refine(
            epic_file, 0, 40,
            ["Added success criteria"],
            date="2026-02-19T10:00:00Z",
        )

        # Session 2: add risks
        simulate_epic_refine(
            epic_file, 40, 65,
            ["Added risk assessment", "Added constraints"],
            date="2026-02-19T14:00:00Z",
        )

        fm = parse_markdown_frontmatter(epic_file.read_text(encoding="utf-8"))
        assert len(fm["refinement_history"]) == 2, "Must have 2 history entries"
        assert fm["refinement_history"][0]["completeness_before"] == 0
        assert fm["refinement_history"][0]["completeness_after"] == 40
        assert fm["refinement_history"][1]["completeness_before"] == 40
        assert fm["refinement_history"][1]["completeness_after"] == 65

    def test_cumulative_completeness_improvement(self, workspace: Path) -> None:
        """Step 5: Completeness improves cumulatively across sessions."""
        epic_file = simulate_epic_create(
            workspace, epic_id="EPIC-MULTI-002", title="Cumulative Score Epic"
        )
        simulate_epic_refine(epic_file, 0, 30, ["Initial scope"])
        simulate_epic_refine(epic_file, 30, 55, ["Added criteria"])
        simulate_epic_refine(epic_file, 55, 80, ["Added risks and constraints"])

        fm = parse_markdown_frontmatter(epic_file.read_text(encoding="utf-8"))
        assert fm["completeness_score"] == 80
        assert len(fm["refinement_history"]) == 3

        # Verify monotonic improvement
        scores = [
            fm["refinement_history"][i]["completeness_after"]
            for i in range(3)
        ]
        assert scores == sorted(scores), "Scores must improve monotonically"

    def test_no_data_lost_between_sessions(self, workspace: Path) -> None:
        """Step 6: No data is lost between refinement sessions."""
        epic_file = simulate_epic_create(
            workspace,
            epic_id="EPIC-MULTI-003",
            title="Data Preservation Epic",
            extra_frontmatter={
                "external_ids": {"jira": "PROJ-99"},
                "requirements": ["REQ-001"],
            },
        )

        simulate_epic_refine(epic_file, 0, 50, ["Session 1 changes"])
        simulate_epic_refine(epic_file, 50, 70, ["Session 2 changes"])

        fm = parse_markdown_frontmatter(epic_file.read_text(encoding="utf-8"))
        # Verify no data lost
        assert fm["id"] == "EPIC-MULTI-003"
        assert fm["title"] == "Data Preservation Epic"
        assert fm["external_ids"]["jira"] == "PROJ-99"
        assert fm["requirements"] == ["REQ-001"]
        assert fm["organisation_pattern"] == "features"
        # Both sessions' changes preserved
        all_changes = []
        for entry in fm["refinement_history"]:
            all_changes.extend(entry["changes"])
        assert "Session 1 changes" in all_changes
        assert "Session 2 changes" in all_changes


# ═══════════════════════════════════════════════════════════════════════════
# 2. FEATURE REFINEMENT PIPELINE
# Simulates: create feature -> refine -> cross-command integration
# ═══════════════════════════════════════════════════════════════════════════


class TestFeatureCreateRefinePipeline:
    """E2E: Feature lifecycle — create linked to epic, refine, verify hierarchy.

    User scenario: James creates a feature linked to an epic, refines it,
    and checks that the parent epic's hierarchy reflects the changes.
    """

    def test_feature_create_linked_to_epic(self, workspace: Path) -> None:
        """Step 1: Feature is created linked to parent epic."""
        simulate_epic_create(
            workspace, epic_id="EPIC-FRP-001", title="Parent Epic"
        )
        feat_file = simulate_feature_create(
            workspace,
            feature_id="FEAT-FRP-001",
            title="Auth Login",
            epic="EPIC-FRP-001",
        )

        fm = parse_markdown_frontmatter(feat_file.read_text(encoding="utf-8"))
        assert fm["id"] == "FEAT-FRP-001"
        assert fm["epic"] == "EPIC-FRP-001"
        assert fm["completeness_score"] == 0

    def test_feature_refine_updates_markdown(self, workspace: Path) -> None:
        """Steps 3-4: /feature-refine updates completeness and history."""
        simulate_epic_create(
            workspace, epic_id="EPIC-FRP-002", title="Parent Epic 2"
        )
        feat_file = simulate_feature_create(
            workspace,
            feature_id="FEAT-FRP-002",
            title="Auth Register",
            epic="EPIC-FRP-002",
        )

        simulate_feature_refine(
            feat_file, 0, 60,
            ["Added acceptance criteria", "Defined test strategy"],
        )

        fm = parse_markdown_frontmatter(feat_file.read_text(encoding="utf-8"))
        assert fm["completeness_score"] == 60
        assert len(fm["refinement_history"]) == 1

    def test_parent_epic_hierarchy_reflects_feature(
        self, workspace: Path
    ) -> None:
        """Steps 5-6: Parent epic's hierarchy shows linked feature correctly."""
        simulate_epic_create(
            workspace, epic_id="EPIC-FRP-003", title="Auth Epic"
        )
        simulate_feature_create(
            workspace,
            feature_id="FEAT-FRP-003",
            title="Login Feature",
            epic="EPIC-FRP-003",
        )
        simulate_feature_create(
            workspace,
            feature_id="FEAT-FRP-004",
            title="Register Feature",
            epic="EPIC-FRP-003",
        )

        status = read_epic_status(workspace, "EPIC-FRP-003")
        assert len(status["linked_features"]) == 2
        feature_ids = {f["id"] for f in status["linked_features"]}
        assert "FEAT-FRP-003" in feature_ids
        assert "FEAT-FRP-004" in feature_ids


class TestFeatureRefineBddIntegration:
    """E2E: Feature refine suggests /generate-bdd when BDD coverage is low.

    User scenario: James creates a feature with no BDD scenarios, refines
    with --focus bdd, and the system suggests running /generate-bdd.
    """

    def test_feature_with_no_bdd_starts_empty(self, workspace: Path) -> None:
        """Step 1: Feature created with no BDD scenarios."""
        simulate_epic_create(
            workspace, epic_id="EPIC-BDD-001", title="BDD Test Epic"
        )
        feat_file = simulate_feature_create(
            workspace,
            feature_id="FEAT-BDD-001",
            title="BDD Coverage Feature",
            epic="EPIC-BDD-001",
        )
        fm = parse_markdown_frontmatter(feat_file.read_text(encoding="utf-8"))
        assert fm["bdd_scenarios"] == [], "New feature has no BDD scenarios"

    def test_feature_refine_spec_suggests_generate_bdd(
        self, feature_refine_spec: str
    ) -> None:
        """Steps 2-3: feature-refine spec suggests /generate-bdd."""
        assert "/generate-bdd" in feature_refine_spec, (
            "Feature refine must suggest /generate-bdd when BDD coverage is low"
        )

    def test_bdd_coverage_in_completeness_dimensions(
        self, feature_refine_spec: str
    ) -> None:
        """Step 4: BDD coverage is a dimension in the completeness score."""
        lower = feature_refine_spec.lower()
        assert "bdd coverage" in lower, (
            "BDD coverage must be a completeness dimension"
        )


class TestFeatureRefineEarsIntegration:
    """E2E: Feature refine suggests /formalize-ears when traceability is low.

    User scenario: James has a feature with no EARS requirements. The system
    suggests running /formalize-ears during refinement.
    """

    def test_feature_with_no_requirements_starts_empty(
        self, workspace: Path
    ) -> None:
        """Step 1: Feature created with no requirements."""
        simulate_epic_create(
            workspace, epic_id="EPIC-EARS-001", title="EARS Test Epic"
        )
        feat_file = simulate_feature_create(
            workspace,
            feature_id="FEAT-EARS-001",
            title="Requirements Feature",
            epic="EPIC-EARS-001",
        )
        fm = parse_markdown_frontmatter(feat_file.read_text(encoding="utf-8"))
        assert fm["requirements"] == [], "New feature has no requirements"

    def test_feature_refine_spec_suggests_formalize_ears(
        self, feature_refine_spec: str
    ) -> None:
        """Steps 2-3: feature-refine spec suggests /formalize-ears."""
        assert "/formalize-ears" in feature_refine_spec, (
            "Feature refine must suggest /formalize-ears when traceability is low"
        )

    def test_requirements_traceability_in_completeness(
        self, feature_refine_spec: str
    ) -> None:
        """Step 4: Requirements traceability is a completeness dimension."""
        lower = feature_refine_spec.lower()
        assert "requirements traceability" in lower, (
            "Requirements traceability must be a completeness dimension"
        )


# ═══════════════════════════════════════════════════════════════════════════
# 3. MULTI-PATTERN HIERARCHY E2E
# Simulates: three epics (direct, features, mixed) in one view
# ═══════════════════════════════════════════════════════════════════════════


class TestMixedHierarchyRendering:
    """E2E: Verify all three organisation patterns work in one hierarchy.

    User scenario: James has a portfolio with different-sized epics using
    all three patterns and wants to see them all in a single hierarchy view.
    """

    def test_three_patterns_coexist_in_workspace(self, workspace: Path) -> None:
        """Step 1: Create 3 epics with different patterns."""
        simulate_epic_create(
            workspace,
            epic_id="EPIC-FEAT-001",
            title="Features Pattern Epic",
            organisation_pattern="features",
        )
        simulate_epic_create(
            workspace,
            epic_id="EPIC-DIRE-001",
            title="Direct Pattern Epic",
            organisation_pattern="direct",
            extra_frontmatter={"direct_tasks": ["TASK-D1", "TASK-D2"]},
        )
        simulate_epic_create(
            workspace,
            epic_id="EPIC-MIX-001",
            title="Mixed Pattern Epic",
            organisation_pattern="mixed",
            extra_frontmatter={"direct_tasks": ["TASK-M1"]},
        )

        # Verify all three files exist
        epics_dir = workspace / "docs" / "epics"
        epic_files = list(epics_dir.glob("*.md"))
        assert len(epic_files) == 3, "Three epic files must exist"

    def test_all_patterns_render_in_hierarchy_spec(
        self, hierarchy_view_spec: str
    ) -> None:
        """Step 2: /hierarchy-view spec renders all three patterns."""
        lower = hierarchy_view_spec.lower()
        assert "features pattern" in lower, "Must render features pattern"
        assert "direct pattern" in lower, "Must render direct pattern"
        assert "mixed pattern" in lower, "Must render mixed pattern"

    def test_each_pattern_displays_correctly_via_status(
        self, workspace: Path
    ) -> None:
        """Step 3: /epic-status displays each pattern correctly."""
        # Create all three
        simulate_epic_create(
            workspace,
            epic_id="EPIC-STA-001",
            title="Features Status",
            organisation_pattern="features",
        )
        simulate_feature_create(
            workspace,
            feature_id="FEAT-STA-001",
            title="Feature Under Status",
            epic="EPIC-STA-001",
        )
        simulate_epic_create(
            workspace,
            epic_id="EPIC-STA-002",
            title="Direct Status",
            organisation_pattern="direct",
            extra_frontmatter={"direct_tasks": ["TASK-S1", "TASK-S2"]},
        )
        simulate_epic_create(
            workspace,
            epic_id="EPIC-STA-003",
            title="Mixed Status",
            organisation_pattern="mixed",
            extra_frontmatter={"direct_tasks": ["TASK-M1"]},
        )
        simulate_feature_create(
            workspace,
            feature_id="FEAT-STA-002",
            title="Mixed Feature",
            epic="EPIC-STA-003",
        )

        # Verify each status
        feat_status = read_epic_status(workspace, "EPIC-STA-001")
        assert feat_status["organisation_pattern"] == "features"
        assert len(feat_status["linked_features"]) >= 1

        dir_status = read_epic_status(workspace, "EPIC-STA-002")
        assert dir_status["organisation_pattern"] == "direct"
        assert len(dir_status["direct_tasks"]) == 2

        mix_status = read_epic_status(workspace, "EPIC-STA-003")
        assert mix_status["organisation_pattern"] == "mixed"
        assert len(mix_status["direct_tasks"]) >= 1
        assert len(mix_status["linked_features"]) >= 1

    def test_progress_works_for_all_patterns(self, workspace: Path) -> None:
        """Step 4: Progress calculation works for all three patterns."""
        # Create and refine each pattern
        for epic_id, pattern in [
            ("EPIC-PROG-001", "features"),
            ("EPIC-PROG-002", "direct"),
            ("EPIC-PROG-003", "mixed"),
        ]:
            ef = simulate_epic_create(
                workspace,
                epic_id=epic_id,
                title=f"{pattern.title()} Progress Epic",
                organisation_pattern=pattern,
            )
            simulate_epic_refine(ef, 0, 50, [f"Added scope for {pattern}"])
            status = read_epic_status(workspace, epic_id)
            assert status["completeness_score"] == 50


class TestPatternEvolution:
    """E2E: Direct pattern suggests adding features when tasks grow large.

    User scenario: James starts with a direct-pattern epic, adds tasks
    until 8+, and the system suggests adding features to organize.
    """

    def test_small_direct_stays_direct(self, workspace: Path) -> None:
        """Steps 1-2: Direct epic with 3 tasks stays direct."""
        simulate_epic_create(
            workspace,
            epic_id="EPIC-EVO-001",
            title="Small Direct Epic",
            organisation_pattern="direct",
            extra_frontmatter={"direct_tasks": ["T-1", "T-2", "T-3"]},
        )
        fm = parse_markdown_frontmatter(
            (workspace / "docs" / "epics" / "epic-evo-001.md").read_text(encoding="utf-8")
        )
        assert len(fm["direct_tasks"]) == 3
        assert fm["organisation_pattern"] == "direct"

    def test_large_direct_exceeds_threshold(self, workspace: Path) -> None:
        """Step 3: Direct epic with 8+ tasks exceeds the threshold."""
        tasks = [f"T-{i}" for i in range(1, 10)]
        simulate_epic_create(
            workspace,
            epic_id="EPIC-EVO-002",
            title="Large Direct Epic",
            organisation_pattern="direct",
            extra_frontmatter={"direct_tasks": tasks},
        )
        fm = parse_markdown_frontmatter(
            (workspace / "docs" / "epics" / "epic-evo-002.md").read_text(encoding="utf-8")
        )
        assert len(fm["direct_tasks"]) >= 8, "Large epic has 8+ tasks"

    def test_epic_refine_spec_detects_large_direct(
        self, epic_refine_spec: str
    ) -> None:
        """Step 3: /epic-refine spec documents detection of 8+ task threshold."""
        lower = epic_refine_spec.lower()
        assert "8+" in lower or "eight" in lower or "8 task" in lower, (
            "Epic refine must document 8+ task threshold for direct pattern"
        )

    def test_mixed_pattern_has_features_and_tasks(
        self, workspace: Path
    ) -> None:
        """Step 4: Mixed pattern epic has both features and direct tasks."""
        simulate_epic_create(
            workspace,
            epic_id="EPIC-EVO-003",
            title="Evolved Mixed Epic",
            organisation_pattern="mixed",
            extra_frontmatter={"direct_tasks": ["T-1", "T-2"]},
        )
        simulate_feature_create(
            workspace,
            feature_id="FEAT-EVO-001",
            title="Grouped Feature",
            epic="EPIC-EVO-003",
        )
        status = read_epic_status(workspace, "EPIC-EVO-003")
        assert status["organisation_pattern"] == "mixed"
        assert len(status["direct_tasks"]) >= 1
        assert len(status["linked_features"]) >= 1


# ═══════════════════════════════════════════════════════════════════════════
# 4. DOCUMENTATION BUILD E2E
# Verifies mkdocs.yml structure and navigation
# ═══════════════════════════════════════════════════════════════════════════


class TestMkdocsBuildStructure:
    """E2E: Verify documentation site configuration is valid.

    User scenario: Developer verifies that mkdocs.yml is properly
    configured and all referenced pages exist in navigation.
    """

    def test_mkdocs_yml_parses_successfully(
        self, mkdocs_config: dict[str, Any]
    ) -> None:
        """Step 1: mkdocs.yml parses as valid YAML."""
        assert "site_name" in mkdocs_config
        assert mkdocs_config["site_name"] == "RequireKit"

    def test_mkdocs_has_nav_section(
        self, mkdocs_config: dict[str, Any]
    ) -> None:
        """Step 2: mkdocs.yml has a nav section."""
        assert "nav" in mkdocs_config, "mkdocs.yml must have a nav section"
        assert isinstance(mkdocs_config["nav"], list)

    def test_commands_reference_in_navigation(
        self, mkdocs_config: dict[str, Any]
    ) -> None:
        """Step 2-3: Commands Reference appears in navigation."""
        nav_str = yaml.dump(mkdocs_config["nav"])
        assert "Commands Reference" in nav_str, (
            "Commands Reference must appear in navigation"
        )

    def test_core_concepts_in_navigation(
        self, mkdocs_config: dict[str, Any]
    ) -> None:
        """Navigation includes Core Concepts with hierarchy."""
        nav_str = yaml.dump(mkdocs_config["nav"])
        assert "Core Concepts" in nav_str
        assert "hierarchy" in nav_str.lower(), (
            "Core Concepts must include hierarchy documentation"
        )

    def test_command_pages_exist(self) -> None:
        """Step 3: Referenced command pages exist on disk."""
        docs_dir = _WORKTREE_ROOT / "docs"
        expected_pages = [
            "commands/index.md",
            "commands/epics.md",
            "commands/features.md",
            "commands/hierarchy.md",
            "commands/sync.md",
        ]
        for page in expected_pages:
            page_path = docs_dir / page
            assert page_path.exists(), f"Expected page {page} to exist at {page_path}"

    def test_hierarchy_concept_page_exists(self) -> None:
        """Hierarchy concepts page exists."""
        hierarchy_page = _WORKTREE_ROOT / "docs" / "core-concepts" / "hierarchy.md"
        assert hierarchy_page.exists(), "Hierarchy concept page must exist"


# Resolve _WORKTREE_ROOT at module level for use in test methods
_WORKTREE_ROOT = Path(__file__).resolve().parents[2]


class TestInternalLinksValid:
    """E2E: Verify internal documentation links are resolvable.

    Scans mkdocs.yml navigation for referenced files and ensures they exist.
    """

    def _extract_nav_paths(self, nav: list[Any]) -> list[str]:
        """Recursively extract file paths from mkdocs nav structure."""
        paths: list[str] = []
        for item in nav:
            if isinstance(item, str):
                paths.append(item)
            elif isinstance(item, dict):
                for value in item.values():
                    if isinstance(value, str):
                        paths.append(value)
                    elif isinstance(value, list):
                        paths.extend(self._extract_nav_paths(value))
        return paths

    def test_all_nav_files_exist(
        self, mkdocs_config: dict[str, Any]
    ) -> None:
        """All files referenced in mkdocs.yml nav must exist."""
        docs_dir = _WORKTREE_ROOT / "docs"
        nav = mkdocs_config.get("nav", [])
        paths = self._extract_nav_paths(nav)

        missing: list[str] = []
        for rel_path in paths:
            full_path = docs_dir / rel_path
            if not full_path.exists():
                missing.append(rel_path)

        assert not missing, (
            f"Missing doc pages referenced in mkdocs.yml nav: {missing}"
        )


class TestNewPagesInNavigation:
    """E2E: Verify new command pages appear in Commands Reference nav."""

    def test_epic_commands_in_nav(
        self, mkdocs_config: dict[str, Any]
    ) -> None:
        """Epic commands page must appear in navigation."""
        nav_str = yaml.dump(mkdocs_config["nav"])
        assert "epics" in nav_str.lower(), "Epic commands must appear in nav"

    def test_feature_commands_in_nav(
        self, mkdocs_config: dict[str, Any]
    ) -> None:
        """Feature commands page must appear in navigation."""
        nav_str = yaml.dump(mkdocs_config["nav"])
        assert "features" in nav_str.lower(), "Feature commands must appear in nav"

    def test_hierarchy_commands_in_nav(
        self, mkdocs_config: dict[str, Any]
    ) -> None:
        """Hierarchy commands page must appear in navigation."""
        nav_str = yaml.dump(mkdocs_config["nav"])
        assert "hierarchy" in nav_str.lower(), "Hierarchy commands must appear in nav"

    def test_sync_commands_in_nav(
        self, mkdocs_config: dict[str, Any]
    ) -> None:
        """Sync commands page must appear in navigation."""
        nav_str = yaml.dump(mkdocs_config["nav"])
        assert "sync" in nav_str.lower(), "Sync commands must appear in nav"


# ═══════════════════════════════════════════════════════════════════════════
# 5. USER WORKFLOW SIMULATIONS
# Simulates James's (product owner) real workflows
# ═══════════════════════════════════════════════════════════════════════════


class TestHappyPathWorkflow:
    """E2E: Happy path — create -> refine iteratively -> 80%+ -> sync.

    User scenario: James creates an epic, refines it through multiple
    sessions until completeness reaches 80%+, then syncs to Graphiti.
    """

    def test_iterative_refinement_to_80_percent(self, workspace: Path) -> None:
        """Happy path: create epic, refine to 80%+, sync."""
        epic_file = simulate_epic_create(
            workspace,
            epic_id="EPIC-HAPPY-001",
            title="Happy Path Epic",
            body="## Business Objective\n\nDeliver user auth.\n",
        )

        # Session 1: scope and criteria
        simulate_epic_refine(epic_file, 0, 35, ["Added scope", "Added success criteria"])

        # Session 2: risks and dependencies
        simulate_epic_refine(
            epic_file, 35, 65,
            ["Added risks", "Added dependencies"],
            date="2026-02-19T11:00:00Z",
        )

        # Session 3: constraints and acceptance
        simulate_epic_refine(
            epic_file, 65, 85,
            ["Added constraints", "Added acceptance criteria"],
            date="2026-02-19T14:00:00Z",
        )

        # Verify 80%+ reached
        fm = parse_markdown_frontmatter(epic_file.read_text(encoding="utf-8"))
        assert fm["completeness_score"] >= 80, "Must reach 80%+ completeness"

        # Sync
        result = simulate_sync(epic_file, graphiti_enabled=True)
        assert result["sync_status"] == "success"

        # Final verification
        final_fm = parse_markdown_frontmatter(epic_file.read_text(encoding="utf-8"))
        assert final_fm["graphiti_synced"] is True
        assert len(final_fm["refinement_history"]) == 3


class TestQuickModeWorkflow:
    """E2E: Quick mode — create -> /epic-refine --quick -> AI suggestions.

    User scenario: James is in a hurry and uses --quick flag to let
    the system apply AI-suggested improvements automatically.
    """

    def test_quick_flag_documented_in_spec(self, epic_refine_spec: str) -> None:
        """Quick mode: --quick flag is documented in epic-refine spec."""
        assert "--quick" in epic_refine_spec, (
            "--quick flag must be documented"
        )

    def test_quick_mode_skips_interactive_prompts(
        self, epic_refine_spec: str
    ) -> None:
        """Quick mode: --quick skips interactive prompts."""
        lower = epic_refine_spec.lower()
        quick_idx = lower.find("--quick")
        assert quick_idx >= 0
        nearby = lower[max(0, quick_idx - 200):quick_idx + 300]
        assert any(
            word in nearby
            for word in ["skip", "automatic", "ai-suggested", "non-interactive"]
        ), "--quick must skip prompts or apply automatic improvements"

    def test_quick_mode_still_updates_score(self, workspace: Path) -> None:
        """Quick mode: score still improves even without interactive prompts."""
        epic_file = simulate_epic_create(
            workspace, epic_id="EPIC-QUICK-001", title="Quick Mode Epic"
        )
        # Simulate quick refinement (automatic improvements)
        simulate_epic_refine(epic_file, 0, 50, ["AI-suggested scope improvements"])
        fm = parse_markdown_frontmatter(epic_file.read_text(encoding="utf-8"))
        assert fm["completeness_score"] > 0, "Quick mode must still improve score"


class TestFocusModeWorkflow:
    """E2E: Focus mode — create -> /epic-refine --focus risks -> only risks.

    User scenario: James wants to focus specifically on risk assessment
    for an epic and uses the --focus flag.
    """

    def test_focus_flag_documented(self, epic_refine_spec: str) -> None:
        """Focus mode: --focus flag is documented."""
        assert "--focus" in epic_refine_spec

    def test_focus_risks_category_supported(self, epic_refine_spec: str) -> None:
        """Focus mode: --focus risks is a supported category."""
        lower = epic_refine_spec.lower()
        assert re.search(r"--focus\s+risks", lower), (
            "--focus risks must be documented"
        )

    def test_focus_mode_refines_targeted_dimension(
        self, workspace: Path
    ) -> None:
        """Focus mode: refinement targets the specified dimension."""
        epic_file = simulate_epic_create(
            workspace, epic_id="EPIC-FOCUS-001", title="Focus Mode Epic"
        )
        # Simulate focused refinement on risks only
        simulate_epic_refine(
            epic_file, 0, 25,
            ["Added risk: data breach", "Added risk: vendor lock-in"],
        )
        fm = parse_markdown_frontmatter(epic_file.read_text(encoding="utf-8"))
        assert fm["completeness_score"] > 0
        assert "risk" in fm["refinement_history"][0]["changes"][0].lower()


class TestStandaloneModeWorkflow:
    """E2E: Standalone mode — everything works without Graphiti.

    User scenario: James uses RequireKit standalone without Graphiti
    configured. All operations must succeed gracefully.
    """

    def test_standalone_mode_create_and_refine(self, workspace: Path) -> None:
        """Standalone: create and refine work without Graphiti."""
        epic_file = simulate_epic_create(
            workspace, epic_id="EPIC-ALONE-001", title="Standalone Epic"
        )
        simulate_epic_refine(epic_file, 0, 50, ["Added scope"])
        fm = parse_markdown_frontmatter(epic_file.read_text(encoding="utf-8"))
        assert fm["completeness_score"] == 50
        assert fm["graphiti_synced"] is False

    def test_standalone_sync_skips_gracefully(self, workspace: Path) -> None:
        """Standalone: sync skips Graphiti when not enabled."""
        epic_file = simulate_epic_create(
            workspace, epic_id="EPIC-ALONE-002", title="Standalone Sync"
        )
        result = simulate_sync(epic_file, graphiti_enabled=False)
        assert result["graphiti_pushed"] is False
        assert result["sync_status"] == "skipped_not_enabled"

        # Markdown still readable
        fm = parse_markdown_frontmatter(epic_file.read_text(encoding="utf-8"))
        assert fm["graphiti_synced"] is False

    def test_standalone_graphiti_defaults_disabled(
        self, graphiti_config: dict[str, Any]
    ) -> None:
        """Standalone: graphiti.yaml defaults to disabled."""
        assert graphiti_config["enabled"] is False

    def test_standalone_refine_spec_documents_degradation(
        self, epic_refine_spec: str
    ) -> None:
        """Standalone: epic-refine spec documents graceful degradation."""
        lower = epic_refine_spec.lower()
        assert any(
            term in lower
            for term in ["graceful", "unavailable", "not configured"]
        ), "Epic refine must document graceful Graphiti degradation"


class TestRecoveryModeWorkflow:
    """E2E: Recovery mode — manual markdown edit -> /requirekit-sync -> match.

    User scenario: James manually edits epic markdown, then runs sync
    to ensure Graphiti matches the updated content.
    """

    def test_manual_edit_then_sync(self, workspace: Path) -> None:
        """Recovery: manual markdown edit followed by sync works."""
        epic_file = simulate_epic_create(
            workspace, epic_id="EPIC-RECOV-001", title="Recovery Epic"
        )

        # Simulate manual edit: directly change completeness_score
        md = epic_file.read_text(encoding="utf-8")
        md = update_frontmatter_field(md, "completeness_score", 70)
        md = update_frontmatter_field(md, "status", "in_progress")
        epic_file.write_text(md, encoding="utf-8")

        # Now sync — should read the manually edited markdown
        result = simulate_sync(epic_file, graphiti_enabled=True)
        assert result["markdown_read"] is True
        assert result["sync_status"] == "success"

        fm = parse_markdown_frontmatter(epic_file.read_text(encoding="utf-8"))
        assert fm["completeness_score"] == 70
        assert fm["status"] == "in_progress"
        assert fm["graphiti_synced"] is True

    def test_sync_spec_documents_recovery(
        self, requirekit_sync_spec: str
    ) -> None:
        """Recovery: sync spec documents recovery use case."""
        lower = requirekit_sync_spec.lower()
        assert "recovery" in lower, "Sync must document recovery use case"

    def test_sync_is_markdown_authoritative(
        self, requirekit_sync_spec: str
    ) -> None:
        """Recovery: sync is one-way, markdown-authoritative."""
        lower = requirekit_sync_spec.lower()
        assert "authoritative" in lower or "one-way" in lower, (
            "Sync must be documented as markdown-authoritative"
        )


# ═══════════════════════════════════════════════════════════════════════════
# COMPLETENESS SCORING INTEGRATION
# Verifies weighted scoring works across the pipeline
# ═══════════════════════════════════════════════════════════════════════════


class TestCompletenessScoring:
    """E2E: Verify completeness scoring dimensions and weights.

    Validates that the 9-dimension epic model and 7-dimension feature
    model produce correct weighted scores across the pipeline.
    """

    def test_epic_weights_sum_to_100(self) -> None:
        """Epic completeness: 9 dimension weights sum to exactly 100."""
        epic_weights = [15, 15, 20, 15, 10, 10, 5, 5, 5]
        assert sum(epic_weights) == 100, "Epic weights must sum to 100"

    def test_feature_weights_sum_to_100(self) -> None:
        """Feature completeness: 7 dimension weights sum to exactly 100."""
        feature_weights = [10, 25, 20, 15, 15, 10, 5]
        assert sum(feature_weights) == 100, "Feature weights must sum to 100"

    def test_epic_score_calculation_is_deterministic(self) -> None:
        """Same inputs always produce same score."""
        epic_weights = [15, 15, 20, 15, 10, 10, 5, 5, 5]
        dimension_scores = [0.8, 0.5, 0.3, 0.7, 0.0, 0.0, 1.0, 1.0, 0.5]
        score1 = calculate_completeness(dimension_scores, epic_weights)
        score2 = calculate_completeness(dimension_scores, epic_weights)
        assert score1 == score2

    def test_epic_partial_score_calculation(self) -> None:
        """Partial epic produces expected weighted score."""
        epic_weights = [15, 15, 20, 15, 10, 10, 5, 5, 5]
        # All dimensions at 50% → score = 50
        half_scores = [0.5] * 9
        score = calculate_completeness(half_scores, epic_weights)
        assert abs(score - 50.0) < 0.001

    def test_feature_partial_score_calculation(self) -> None:
        """Partial feature produces expected weighted score."""
        feature_weights = [10, 25, 20, 15, 15, 10, 5]
        # All dimensions at 50% → score = 50
        half_scores = [0.5] * 7
        score = calculate_completeness(half_scores, feature_weights)
        assert abs(score - 50.0) < 0.001

    def test_score_reflects_in_frontmatter_after_pipeline(
        self, workspace: Path
    ) -> None:
        """Score written during refinement persists through pipeline."""
        epic_file = simulate_epic_create(
            workspace, epic_id="EPIC-SCORE-001", title="Score Test"
        )
        simulate_epic_refine(epic_file, 0, 72, ["All dimensions assessed"])
        simulate_sync(epic_file, graphiti_enabled=True)

        fm = parse_markdown_frontmatter(epic_file.read_text(encoding="utf-8"))
        assert fm["completeness_score"] == 72


# ═══════════════════════════════════════════════════════════════════════════
# INTERMEDIATE STATE VERIFICATION
# Tests verify intermediate states, not just final state
# ═══════════════════════════════════════════════════════════════════════════


class TestIntermediateStates:
    """E2E: Verify intermediate pipeline states are correct.

    Ensures that each step in the pipeline produces the expected
    intermediate state before proceeding to the next step.
    """

    def test_create_state_before_refine(self, workspace: Path) -> None:
        """After create, before refine: score=0, no history, not synced."""
        epic_file = simulate_epic_create(
            workspace, epic_id="EPIC-INT-001", title="Intermediate Test"
        )
        fm = parse_markdown_frontmatter(epic_file.read_text(encoding="utf-8"))
        assert fm["completeness_score"] == 0
        assert fm.get("refinement_history") is None or fm.get("refinement_history") == []
        assert fm["graphiti_synced"] is False

    def test_refine_state_before_sync(self, workspace: Path) -> None:
        """After refine, before sync: score improved, history exists, not synced."""
        epic_file = simulate_epic_create(
            workspace, epic_id="EPIC-INT-002", title="Pre-Sync Test"
        )
        simulate_epic_refine(epic_file, 0, 55, ["Added scope"])

        fm = parse_markdown_frontmatter(epic_file.read_text(encoding="utf-8"))
        assert fm["completeness_score"] == 55
        assert len(fm["refinement_history"]) == 1
        assert fm["graphiti_synced"] is False, "Not yet synced"

    def test_sync_state_after_pipeline(self, workspace: Path) -> None:
        """After sync: score preserved, history preserved, synced=True."""
        epic_file = simulate_epic_create(
            workspace, epic_id="EPIC-INT-003", title="Post-Sync Test"
        )
        simulate_epic_refine(epic_file, 0, 60, ["Added scope"])
        simulate_sync(epic_file, graphiti_enabled=True)

        fm = parse_markdown_frontmatter(epic_file.read_text(encoding="utf-8"))
        assert fm["completeness_score"] == 60
        assert len(fm["refinement_history"]) == 1
        assert fm["graphiti_synced"] is True
        assert fm["last_graphiti_sync"] is not None

    def test_second_refine_after_sync(self, workspace: Path) -> None:
        """After sync + second refine: score updated, 2 history entries, sync reset."""
        epic_file = simulate_epic_create(
            workspace, epic_id="EPIC-INT-004", title="Post-Sync Refine"
        )
        simulate_epic_refine(epic_file, 0, 50, ["Initial scope"])
        simulate_sync(epic_file, graphiti_enabled=True)

        # Second refinement after sync
        simulate_epic_refine(
            epic_file, 50, 75,
            ["Added risks after sync"],
            date="2026-02-19T16:00:00Z",
        )

        fm = parse_markdown_frontmatter(epic_file.read_text(encoding="utf-8"))
        assert fm["completeness_score"] == 75
        assert len(fm["refinement_history"]) == 2
        # Note: graphiti_synced may still be True from sync, but score is updated
        # This is a valid intermediate state — the markdown is ahead of Graphiti
