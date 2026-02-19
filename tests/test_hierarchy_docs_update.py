"""Tests for TASK-RK01-012: Hierarchy docs update with optional feature layer patterns.

Validates that the updated hierarchy.md and CLAUDE.md files contain all required
content per the acceptance criteria, and that internal links resolve correctly.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

# Project root for the worktree
PROJECT_ROOT = Path(__file__).resolve().parent.parent


class TestHierarchyMdOrganisationPatterns:
    """AC: hierarchy.md shows all three organisation patterns with diagrams."""

    @pytest.fixture()
    def hierarchy_content(self) -> str:
        path = PROJECT_ROOT / "docs" / "core-concepts" / "hierarchy.md"
        return path.read_text(encoding="utf-8")

    def test_standard_pattern_documented(self, hierarchy_content: str) -> None:
        assert "Standard Pattern" in hierarchy_content
        assert "Epic → Feature → Task" in hierarchy_content

    def test_direct_pattern_documented(self, hierarchy_content: str) -> None:
        assert "Direct Pattern" in hierarchy_content
        assert "Epic → Task" in hierarchy_content

    def test_mixed_pattern_documented(self, hierarchy_content: str) -> None:
        assert "Mixed Pattern" in hierarchy_content
        assert "Epic → Feature + Task" in hierarchy_content

    def test_three_patterns_in_overview_table(self, hierarchy_content: str) -> None:
        """The Organisation Patterns section has a table listing all three."""
        assert "| **Standard**" in hierarchy_content
        assert "| **Direct**" in hierarchy_content
        assert "| **Mixed**" in hierarchy_content

    def test_standard_diagram_present(self, hierarchy_content: str) -> None:
        """Standard pattern has an ASCII tree diagram."""
        assert "EPIC (Strategic Business Objective)" in hierarchy_content
        assert "FEATURE (Implementation Unit)" in hierarchy_content

    def test_direct_diagram_present(self, hierarchy_content: str) -> None:
        """Direct pattern has an ASCII tree diagram."""
        assert "EPIC (Focused Business Objective)" in hierarchy_content
        assert "TASK-001 (Implementation)" in hierarchy_content

    def test_mixed_diagram_present(self, hierarchy_content: str) -> None:
        """Mixed pattern has an ASCII tree diagram showing both features and direct tasks."""
        assert "FEATURE (Grouped Capability)" in hierarchy_content
        assert "Direct Task" in hierarchy_content


class TestHierarchyMdPmToolMapping:
    """AC: PM tool mapping table for all patterns."""

    @pytest.fixture()
    def hierarchy_content(self) -> str:
        path = PROJECT_ROOT / "docs" / "core-concepts" / "hierarchy.md"
        return path.read_text(encoding="utf-8")

    def test_pm_tool_mapping_section_exists(self, hierarchy_content: str) -> None:
        assert "## PM Tool Mapping" in hierarchy_content

    def test_jira_mapping(self, hierarchy_content: str) -> None:
        assert "Jira" in hierarchy_content

    def test_linear_mapping(self, hierarchy_content: str) -> None:
        assert "Linear" in hierarchy_content

    def test_github_projects_mapping(self, hierarchy_content: str) -> None:
        assert "GitHub Projects" in hierarchy_content

    def test_azure_devops_mapping(self, hierarchy_content: str) -> None:
        assert "Azure DevOps" in hierarchy_content

    def test_pattern_specific_mappings(self, hierarchy_content: str) -> None:
        """Each pattern has its own mapping example."""
        assert "Standard Pattern" in hierarchy_content
        assert "Direct Pattern" in hierarchy_content
        assert "Mixed Pattern" in hierarchy_content


class TestHierarchyMdTraceability:
    """AC: Traceability updated for direct-pattern epics."""

    @pytest.fixture()
    def hierarchy_content(self) -> str:
        path = PROJECT_ROOT / "docs" / "core-concepts" / "hierarchy.md"
        return path.read_text(encoding="utf-8")

    def test_forward_traceability_standard(self, hierarchy_content: str) -> None:
        assert "Forward Traceability (Standard Pattern)" in hierarchy_content

    def test_forward_traceability_direct(self, hierarchy_content: str) -> None:
        assert "Forward Traceability (Direct Pattern)" in hierarchy_content

    def test_backward_traceability_both_patterns(self, hierarchy_content: str) -> None:
        assert "Backward Traceability" in hierarchy_content


class TestHierarchyMdBestPractices:
    """AC: Best practices include pattern selection guidance."""

    @pytest.fixture()
    def hierarchy_content(self) -> str:
        path = PROJECT_ROOT / "docs" / "core-concepts" / "hierarchy.md"
        return path.read_text(encoding="utf-8")

    def test_pattern_selection_section(self, hierarchy_content: str) -> None:
        assert "Pattern Selection" in hierarchy_content

    def test_direct_recommendation_small_epics(self, hierarchy_content: str) -> None:
        """Direct pattern recommended for 3-5 tasks."""
        assert "3-5 tasks" in hierarchy_content
        assert "Direct" in hierarchy_content

    def test_standard_recommendation_large_epics(self, hierarchy_content: str) -> None:
        """Standard pattern recommended for 8+ tasks."""
        assert "8+ tasks" in hierarchy_content
        assert "Standard" in hierarchy_content

    def test_avoid_mixed_guidance(self, hierarchy_content: str) -> None:
        """Warns against permanent mixed pattern."""
        assert "Avoid mixed unless transitioning" in hierarchy_content


class TestClaudeMdRefinementCommands:
    """AC: CLAUDE.md includes refinement commands."""

    @pytest.fixture()
    def claude_content(self) -> str:
        path = PROJECT_ROOT / "CLAUDE.md"
        return path.read_text(encoding="utf-8")

    def test_refinement_section_exists(self, claude_content: str) -> None:
        assert "### Requirements Refinement" in claude_content

    def test_epic_refine_command(self, claude_content: str) -> None:
        assert "/epic-refine EPIC-XXX" in claude_content

    def test_feature_refine_command(self, claude_content: str) -> None:
        assert "/feature-refine FEAT-XXX" in claude_content

    def test_requirekit_sync_command(self, claude_content: str) -> None:
        assert "/requirekit-sync" in claude_content


class TestClaudeMdWorkflowUpdated:
    """AC: CLAUDE.md workflow updated with refinement step."""

    @pytest.fixture()
    def claude_content(self) -> str:
        path = PROJECT_ROOT / "CLAUDE.md"
        return path.read_text(encoding="utf-8")

    def test_workflow_has_refine_step(self, claude_content: str) -> None:
        assert "**Refine**" in claude_content

    def test_refine_step_mentions_commands(self, claude_content: str) -> None:
        assert "/epic-refine" in claude_content
        assert "/feature-refine" in claude_content

    def test_workflow_order(self, claude_content: str) -> None:
        """Refinement step comes between BDD generation and Organize."""
        bdd_pos = claude_content.index("**Generate BDD**")
        refine_pos = claude_content.index("**Refine**")
        organize_pos = claude_content.index("**Organize**")
        assert bdd_pos < refine_pos < organize_pos

    def test_organisation_patterns_note(self, claude_content: str) -> None:
        """CLAUDE.md notes that epics support three org patterns."""
        assert "three patterns" in claude_content or "three organisation patterns" in claude_content


class TestHierarchyMdLinks:
    """Test that internal links in hierarchy.md resolve to existing files."""

    @pytest.fixture()
    def hierarchy_content(self) -> str:
        path = PROJECT_ROOT / "docs" / "core-concepts" / "hierarchy.md"
        return path.read_text(encoding="utf-8")

    def test_traceability_link(self) -> None:
        target = PROJECT_ROOT / "docs" / "core-concepts" / "traceability.md"
        assert target.exists(), f"Link target missing: {target}"

    def test_first_requirements_link(self) -> None:
        target = PROJECT_ROOT / "docs" / "getting-started" / "first-requirements.md"
        assert target.exists(), f"Link target missing: {target}"

    def test_features_example_link(self) -> None:
        target = PROJECT_ROOT / "docs" / "examples" / "features.md"
        assert target.exists(), f"Link target missing: {target}"

    def test_all_markdown_links_resolve(self, hierarchy_content: str) -> None:
        """Extract all relative markdown links and verify they resolve."""
        link_pattern = re.compile(r'\[.*?\]\((\.\./.*?\.md|[a-zA-Z].*?\.md)\)')
        links = link_pattern.findall(hierarchy_content)
        hierarchy_dir = PROJECT_ROOT / "docs" / "core-concepts"
        for link in links:
            resolved = (hierarchy_dir / link).resolve()
            assert resolved.exists(), f"Broken link: {link} -> {resolved}"
