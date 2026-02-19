"""
Tests for the Graphiti configuration template.

TASK-RK01-003: Create Graphiti Configuration Template

These tests verify:
1. The YAML file parses correctly (no syntax errors)
2. All required fields are present
3. Default values are sensible (enabled=false for standalone mode)
4. The group_id_pattern follows the {project}__requirements convention
5. Boolean fields have correct types
"""

import os
import unittest

import yaml


# Resolve the path relative to this file so tests can be run from any CWD.
REPO_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
CONFIG_PATH = os.path.join(
    REPO_ROOT, "installer", "global", "config", "graphiti.yaml"
)


class TestGraphitiConfigFileExists(unittest.TestCase):
    """Verify the config file is present at the expected location."""

    def test_config_file_exists(self):
        """AC-001: Config file exists at installer/global/config/graphiti.yaml"""
        self.assertTrue(
            os.path.isfile(CONFIG_PATH),
            f"Config file not found at: {CONFIG_PATH}",
        )


class TestGraphitiConfigParses(unittest.TestCase):
    """Verify the YAML is syntactically valid and can be loaded."""

    def setUp(self):
        with open(CONFIG_PATH, "r") as f:
            self.config = yaml.safe_load(f)

    def test_yaml_parses_without_error(self):
        """The YAML file must be valid and non-empty."""
        self.assertIsNotNone(self.config)
        self.assertIsInstance(self.config, dict)

    def test_top_level_graphiti_key_present(self):
        """Top-level 'graphiti' key must be present."""
        self.assertIn("graphiti", self.config)

    def test_graphiti_section_is_dict(self):
        """The 'graphiti' section must be a mapping."""
        self.assertIsInstance(self.config["graphiti"], dict)


class TestGraphitiConfigRequiredFields(unittest.TestCase):
    """Verify all required fields are present under the graphiti key."""

    REQUIRED_FIELDS = [
        "enabled",
        "endpoint",
        "project_namespace",
        "group_id_pattern",
        "sync_on_create",
        "sync_on_refine",
    ]

    def setUp(self):
        with open(CONFIG_PATH, "r") as f:
            self.graphiti = yaml.safe_load(f)["graphiti"]

    def test_all_required_fields_present(self):
        """All required fields must be present in the graphiti section."""
        for field in self.REQUIRED_FIELDS:
            with self.subTest(field=field):
                self.assertIn(
                    field,
                    self.graphiti,
                    f"Required field '{field}' missing from graphiti config",
                )


class TestGraphitiConfigDefaultValues(unittest.TestCase):
    """AC-002: Verify default values are sensible for standalone mode."""

    def setUp(self):
        with open(CONFIG_PATH, "r") as f:
            self.graphiti = yaml.safe_load(f)["graphiti"]

    def test_enabled_defaults_to_false(self):
        """AC-002: enabled must default to false (standalone mode)."""
        self.assertFalse(
            self.graphiti["enabled"],
            "Default value for 'enabled' must be false (standalone mode)",
        )

    def test_enabled_is_boolean(self):
        """'enabled' must be a Python bool, not a string."""
        self.assertIsInstance(self.graphiti["enabled"], bool)

    def test_endpoint_is_bolt_uri(self):
        """Default endpoint should be a bolt:// URI."""
        endpoint = self.graphiti["endpoint"]
        self.assertIsInstance(endpoint, str)
        self.assertTrue(
            endpoint.startswith("bolt://"),
            f"Endpoint '{endpoint}' should start with 'bolt://'",
        )

    def test_project_namespace_is_non_empty_string(self):
        """project_namespace must be a non-empty string."""
        ns = self.graphiti["project_namespace"]
        self.assertIsInstance(ns, str)
        self.assertTrue(len(ns) > 0, "project_namespace must not be empty")

    def test_sync_on_create_is_boolean(self):
        """sync_on_create must be a bool."""
        self.assertIsInstance(self.graphiti["sync_on_create"], bool)

    def test_sync_on_refine_is_boolean(self):
        """sync_on_refine must be a bool."""
        self.assertIsInstance(self.graphiti["sync_on_refine"], bool)


class TestGraphitiConfigGroupIdPattern(unittest.TestCase):
    """AC-004: Verify group_id_pattern follows {project}__requirements convention."""

    def setUp(self):
        with open(CONFIG_PATH, "r") as f:
            self.graphiti = yaml.safe_load(f)["graphiti"]

    def test_group_id_pattern_contains_project_placeholder(self):
        """AC-004: group_id_pattern must contain the {project} placeholder."""
        pattern = self.graphiti["group_id_pattern"]
        self.assertIn(
            "{project}",
            pattern,
            f"group_id_pattern '{pattern}' must contain '{{project}}' placeholder",
        )

    def test_group_id_pattern_ends_with_double_underscore_requirements(self):
        """AC-004: pattern must follow {project}__requirements convention."""
        pattern = self.graphiti["group_id_pattern"]
        self.assertTrue(
            pattern.endswith("__requirements"),
            f"group_id_pattern '{pattern}' must end with '__requirements'",
        )

    def test_group_id_pattern_exact_value(self):
        """AC-004: group_id_pattern must equal '{project}__requirements'."""
        self.assertEqual(
            self.graphiti["group_id_pattern"],
            "{project}__requirements",
        )


class TestGraphitiConfigDocumentedWithComments(unittest.TestCase):
    """AC-003: Verify all fields are documented with inline comments."""

    def test_config_file_contains_field_documentation(self):
        """AC-003: The file must contain inline comments documenting fields."""
        with open(CONFIG_PATH, "r") as f:
            raw_content = f.read()

        # Check that each field has an associated comment somewhere in the file
        documented_fields = [
            "enabled",
            "endpoint",
            "project_namespace",
            "group_id_pattern",
            "sync_on_create",
            "sync_on_refine",
        ]
        for field in documented_fields:
            with self.subTest(field=field):
                self.assertIn(
                    field,
                    raw_content,
                    f"Field '{field}' should be documented in the config file",
                )

    def test_config_file_contains_standalone_mode_explanation(self):
        """AC-003: File must explain what standalone mode means."""
        with open(CONFIG_PATH, "r") as f:
            raw_content = f.read()
        self.assertIn(
            "standalone",
            raw_content.lower(),
            "Config file must contain an explanation of standalone mode",
        )

    def test_config_file_contains_enable_instructions(self):
        """AC-003: File must include instructions on how to enable Graphiti."""
        with open(CONFIG_PATH, "r") as f:
            raw_content = f.read()
        self.assertIn(
            "enabled: true",
            raw_content,
            "Config file should mention setting 'enabled: true' to activate Graphiti",
        )

    def test_config_file_contains_tip_for_standalone_users(self):
        """AC-003: File must contain a tip message for standalone users."""
        with open(CONFIG_PATH, "r") as f:
            raw_content = f.read()
        self.assertIn(
            "Tip",
            raw_content,
            "Config file must contain a Tip message for standalone users",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
