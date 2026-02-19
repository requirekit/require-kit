"""
Tests for the /requirekit-sync command specification.

TASK-RK01-006: Create /requirekit-sync Command

These tests verify:
1. Command file exists with valid structure (AC-001 through AC-007)
2. Sync patterns are documented (individual, full, dry-run)
3. Error handling covers all failure modes
4. Episode schema references are correct
5. Upsert deduplication pattern is specified
6. Markdown-authoritative design is enforced
"""

import os
import re
import unittest


# Resolve the path relative to this file so tests can be run from any CWD.
REPO_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
COMMAND_PATH = os.path.join(
    REPO_ROOT, "installer", "global", "commands", "requirekit-sync.md"
)
CONFIG_PATH = os.path.join(
    REPO_ROOT, "installer", "global", "config", "graphiti.yaml"
)


class TestCommandFileExists(unittest.TestCase):
    """Verify the command file is present at the expected location."""

    def test_command_file_exists(self):
        """Command file exists at installer/global/commands/requirekit-sync.md"""
        self.assertTrue(
            os.path.isfile(COMMAND_PATH),
            f"Command file not found at: {COMMAND_PATH}",
        )

    def test_command_file_is_not_empty(self):
        """Command file must contain meaningful content."""
        with open(COMMAND_PATH, "r") as f:
            content = f.read()
        self.assertGreater(
            len(content.strip()), 100,
            "Command file must contain substantial content (>100 chars)",
        )


class TestCommandStructure(unittest.TestCase):
    """Verify command file has valid markdown structure with required sections."""

    def setUp(self):
        with open(COMMAND_PATH, "r") as f:
            self.content = f.read()
        self.content_lower = self.content.lower()

    def test_has_title_heading(self):
        """Command file must start with a markdown heading."""
        self.assertTrue(
            self.content.strip().startswith("#"),
            "Command file must start with a markdown heading",
        )

    def test_has_usage_section(self):
        """Command file must contain a Usage section."""
        self.assertRegex(
            self.content,
            r"(?i)##\s+usage",
            "Command file must contain a '## Usage' section",
        )

    def test_has_examples_section(self):
        """Command file must contain an Examples section."""
        self.assertRegex(
            self.content,
            r"(?i)##\s+examples",
            "Command file must contain an '## Examples' section",
        )

    def test_has_error_handling_section(self):
        """Command file must document error handling."""
        self.assertRegex(
            self.content,
            r"(?i)##\s+error\s+handling",
            "Command file must contain an '## Error Handling' section",
        )

    def test_has_output_format_section(self):
        """Command file must document expected output format."""
        # Accept "Output Format" or "Output" or "Progress" section
        has_output = bool(re.search(
            r"(?i)##\s+(output|progress|display)",
            self.content,
        ))
        self.assertTrue(
            has_output,
            "Command file must document output format",
        )


class TestAC001IndividualAndFullSync(unittest.TestCase):
    """AC-001: Command supports individual sync (by ID) and full sync (--all)."""

    def setUp(self):
        with open(COMMAND_PATH, "r") as f:
            self.content = f.read()

    def test_supports_epic_id_argument(self):
        """Command must support syncing a specific epic by ID."""
        self.assertIn(
            "EPIC-",
            self.content,
            "Command must document syncing a specific epic (e.g. EPIC-001)",
        )

    def test_supports_feature_id_argument(self):
        """Command must support syncing a specific feature by ID."""
        self.assertIn(
            "FEAT-",
            self.content,
            "Command must document syncing a specific feature (e.g. FEAT-001)",
        )

    def test_supports_all_flag(self):
        """Command must support --all flag for full sync."""
        self.assertIn(
            "--all",
            self.content,
            "Command must support '--all' flag for full sync",
        )

    def test_usage_shows_argument_pattern(self):
        """Usage must show the [epic-id|feature-id|--all] argument pattern."""
        # Must show that all three sync targets are available
        has_pattern = (
            "epic-id" in self.content.lower()
            or "epic_id" in self.content.lower()
            or "[epic" in self.content.lower()
        )
        self.assertTrue(
            has_pattern,
            "Usage must show the argument pattern for epic/feature/all sync",
        )


class TestAC002MarkdownAuthoritative(unittest.TestCase):
    """AC-002: Markdown is authoritative (Graphiti rebuilt from markdown)."""

    def setUp(self):
        with open(COMMAND_PATH, "r") as f:
            self.content = f.read()
        self.content_lower = self.content.lower()

    def test_documents_markdown_as_source_of_truth(self):
        """Command must state that markdown files are the authoritative source."""
        has_authoritative = (
            "authoritative" in self.content_lower
            or "source of truth" in self.content_lower
        )
        self.assertTrue(
            has_authoritative,
            "Command must state markdown is the authoritative source / source of truth",
        )

    def test_documents_read_markdown_push_to_graphiti(self):
        """Command must describe reading markdown and pushing to Graphiti."""
        has_push = (
            "push" in self.content_lower
            or "upsert" in self.content_lower
            or "write" in self.content_lower
        )
        has_read = (
            "read" in self.content_lower
            or "scan" in self.content_lower
            or "parse" in self.content_lower
        )
        self.assertTrue(
            has_push and has_read,
            "Command must describe reading markdown files and pushing to Graphiti",
        )

    def test_no_conflict_detection_documented(self):
        """Command must specify no bidirectional conflict detection (markdown wins)."""
        has_no_conflict = (
            "no conflict" in self.content_lower
            or "overwrite" in self.content_lower
            or "markdown always wins" in self.content_lower
            or "markdown wins" in self.content_lower
            or "one-way" in self.content_lower
        )
        self.assertTrue(
            has_no_conflict,
            "Command must specify no conflict detection - markdown always wins",
        )


class TestAC003UpsertDeduplication(unittest.TestCase):
    """AC-003: Upsert uses entity ID as deduplication key."""

    def setUp(self):
        with open(COMMAND_PATH, "r") as f:
            self.content = f.read()
        self.content_lower = self.content.lower()

    def test_documents_upsert_pattern(self):
        """Command must document the upsert pattern."""
        self.assertIn(
            "upsert",
            self.content_lower,
            "Command must document the upsert pattern",
        )

    def test_documents_deduplication_key(self):
        """Command must specify entity ID as deduplication key."""
        has_dedup = (
            "deduplication" in self.content_lower
            or "deduplica" in self.content_lower
            or "epic_id" in self.content_lower
            or "feature_id" in self.content_lower
        )
        self.assertTrue(
            has_dedup,
            "Command must specify entity ID (epic_id/feature_id) as deduplication key",
        )


class TestAC004GracefulGraphitiUnconfigured(unittest.TestCase):
    """AC-004: Graceful handling when Graphiti not configured."""

    def setUp(self):
        with open(COMMAND_PATH, "r") as f:
            self.content = f.read()
        self.content_lower = self.content.lower()

    def test_documents_graphiti_not_configured_handling(self):
        """Command must handle Graphiti not being configured."""
        has_not_configured = (
            "not configured" in self.content_lower
            or "not enabled" in self.content_lower
            or "disabled" in self.content_lower
            or "enabled: false" in self.content_lower
        )
        self.assertTrue(
            has_not_configured,
            "Command must document handling when Graphiti is not configured",
        )

    def test_provides_setup_guidance(self):
        """Command must provide setup instructions when Graphiti is unconfigured."""
        has_setup = (
            "setup" in self.content_lower
            or "enable" in self.content_lower
            or "graphiti.yaml" in self.content_lower
            or "config" in self.content_lower
        )
        self.assertTrue(
            has_setup,
            "Command must provide setup/enable guidance when Graphiti is unconfigured",
        )


class TestAC005PartialFailureHandling(unittest.TestCase):
    """AC-005: Partial failure doesn't stop remaining syncs."""

    def setUp(self):
        with open(COMMAND_PATH, "r") as f:
            self.content = f.read()
        self.content_lower = self.content.lower()

    def test_documents_partial_failure_resilience(self):
        """Command must document that partial failures don't halt the sync."""
        has_partial = (
            "partial" in self.content_lower
            or "continue" in self.content_lower
            or "remaining" in self.content_lower
            or "skip" in self.content_lower
        )
        self.assertTrue(
            has_partial,
            "Command must document that partial failures don't stop remaining syncs",
        )

    def test_documents_connection_failure_handling(self):
        """Command must handle connection failures."""
        has_connection = (
            "connection" in self.content_lower
            or "timeout" in self.content_lower
            or "unreachable" in self.content_lower
        )
        self.assertTrue(
            has_connection,
            "Command must document connection failure handling",
        )

    def test_documents_invalid_markdown_handling(self):
        """Command must handle invalid markdown files gracefully."""
        has_invalid = (
            "invalid" in self.content_lower
            or "malformed" in self.content_lower
            or "parse error" in self.content_lower
            or "frontmatter" in self.content_lower
        )
        self.assertTrue(
            has_invalid,
            "Command must document handling of invalid/malformed markdown files",
        )


class TestAC006DryRunSupport(unittest.TestCase):
    """AC-006: --dry-run shows what would be synced without writing."""

    def setUp(self):
        with open(COMMAND_PATH, "r") as f:
            self.content = f.read()

    def test_supports_dry_run_flag(self):
        """Command must support --dry-run flag."""
        self.assertIn(
            "--dry-run",
            self.content,
            "Command must support '--dry-run' flag",
        )

    def test_dry_run_prevents_writes(self):
        """Dry-run must preview without actually writing to Graphiti."""
        content_lower = self.content.lower()
        has_preview = (
            "preview" in content_lower
            or "without writing" in content_lower
            or "would be synced" in content_lower
            or "no changes" in content_lower
            or "would sync" in content_lower
        )
        self.assertTrue(
            has_preview,
            "Dry-run must describe previewing without writing to Graphiti",
        )


class TestAC007ProgressAndSummaryOutput(unittest.TestCase):
    """AC-007: Output shows clear progress and summary."""

    def setUp(self):
        with open(COMMAND_PATH, "r") as f:
            self.content = f.read()
        self.content_lower = self.content.lower()

    def test_shows_sync_progress(self):
        """Command must show progress during sync."""
        has_progress = (
            "progress" in self.content_lower
            or "syncing" in self.content_lower
        )
        self.assertTrue(
            has_progress,
            "Command must show sync progress",
        )

    def test_shows_summary_with_counts(self):
        """Command must show summary with synced/error counts."""
        has_summary = (
            "summary" in self.content_lower
            and ("synced" in self.content_lower or "count" in self.content_lower)
        )
        self.assertTrue(
            has_summary,
            "Command must show summary with synced/error counts",
        )

    def test_shows_endpoint_info(self):
        """Command output must show the Graphiti endpoint being used."""
        has_endpoint = (
            "endpoint" in self.content_lower
            or "bolt://" in self.content_lower
        )
        self.assertTrue(
            has_endpoint,
            "Command output must show the Graphiti endpoint",
        )

    def test_shows_group_id(self):
        """Command output must show the group ID being used."""
        has_group = (
            "group" in self.content_lower
            or "__requirements" in self.content_lower
        )
        self.assertTrue(
            has_group,
            "Command output must show the group ID",
        )


class TestSyncPatterns(unittest.TestCase):
    """Verify sync patterns are properly documented."""

    def setUp(self):
        with open(COMMAND_PATH, "r") as f:
            self.content = f.read()
        self.content_lower = self.content.lower()

    def test_references_docs_epics_directory(self):
        """Command must reference docs/epics/ as scan target."""
        self.assertIn(
            "docs/epics/",
            self.content,
            "Command must reference docs/epics/ directory for scanning",
        )

    def test_references_docs_features_directory(self):
        """Command must reference docs/features/ as scan target."""
        self.assertIn(
            "docs/features/",
            self.content,
            "Command must reference docs/features/ directory for scanning",
        )

    def test_references_frontmatter_parsing(self):
        """Command must describe parsing YAML frontmatter from markdown files."""
        self.assertIn(
            "frontmatter",
            self.content_lower,
            "Command must describe parsing YAML frontmatter",
        )

    def test_references_episode_construction(self):
        """Command must describe constructing Graphiti episodes."""
        has_episode = (
            "episode" in self.content_lower
        )
        self.assertTrue(
            has_episode,
            "Command must describe constructing Graphiti episodes",
        )

    def test_references_group_id_pattern(self):
        """Command must reference {project}__requirements group ID pattern."""
        self.assertIn(
            "{project}__requirements",
            self.content,
            "Command must reference the {project}__requirements group ID pattern",
        )


class TestEpisodeSchemaReferences(unittest.TestCase):
    """Verify episode schema references are correct for both epics and features."""

    def setUp(self):
        with open(COMMAND_PATH, "r") as f:
            self.content = f.read()
        self.content_lower = self.content.lower()

    def test_epic_episode_schema_referenced(self):
        """Command must reference or document the epic episode schema."""
        has_epic_schema = (
            "entity_type" in self.content_lower
            or "epic episode" in self.content_lower
            or '"epic"' in self.content_lower
        )
        self.assertTrue(
            has_epic_schema,
            "Command must reference the epic episode schema (entity_type: epic)",
        )

    def test_feature_episode_schema_referenced(self):
        """Command must reference or document the feature episode schema."""
        has_feature_schema = (
            "feature episode" in self.content_lower
            or '"feature"' in self.content_lower
            or "entity_type" in self.content_lower
        )
        self.assertTrue(
            has_feature_schema,
            "Command must reference the feature episode schema (entity_type: feature)",
        )

    def test_metadata_fields_documented(self):
        """Command must document key metadata fields for episodes."""
        has_metadata = (
            "metadata" in self.content_lower
            or "_metadata" in self.content
        )
        self.assertTrue(
            has_metadata,
            "Command must document metadata fields for episode construction",
        )


class TestGraphitiConfigIntegration(unittest.TestCase):
    """Verify sync command properly references Graphiti configuration."""

    def setUp(self):
        with open(COMMAND_PATH, "r") as f:
            self.content = f.read()
        self.content_lower = self.content.lower()

    def test_references_graphiti_config(self):
        """Command must reference the Graphiti configuration."""
        has_config_ref = (
            "graphiti.yaml" in self.content_lower
            or "config" in self.content_lower
        )
        self.assertTrue(
            has_config_ref,
            "Command must reference the Graphiti configuration",
        )

    def test_references_enabled_check(self):
        """Command must check if Graphiti is enabled before syncing."""
        has_enabled_check = (
            "enabled" in self.content_lower
            or "check" in self.content_lower
        )
        self.assertTrue(
            has_enabled_check,
            "Command must describe checking if Graphiti is enabled",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
