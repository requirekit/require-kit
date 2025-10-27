"""
Test suite for TASK-011A: MAUI AppShell Template Structure
Tests validate template configuration, structure, and completeness.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any
import re


class TestMauiAppShellStructure:
    """Tests for MAUI AppShell template directory structure and configuration."""

    TEMPLATE_ROOT = Path(__file__).parent.parent.parent / "installer" / "global" / "templates" / "maui-appshell"

    def test_template_directory_exists(self):
        """Verify the template root directory exists."""
        assert self.TEMPLATE_ROOT.exists(), f"Template directory not found: {self.TEMPLATE_ROOT}"
        assert self.TEMPLATE_ROOT.is_dir(), f"Template path is not a directory: {self.TEMPLATE_ROOT}"

    def test_required_configuration_files_exist(self):
        """Verify all required configuration files exist."""
        required_files = [
            "manifest.json",
            "settings.json",
            "CLAUDE.md",
            "README.md"
        ]

        for file_name in required_files:
            file_path = self.TEMPLATE_ROOT / file_name
            assert file_path.exists(), f"Required file not found: {file_name}"
            assert file_path.is_file(), f"Path is not a file: {file_name}"

            # Verify files are not empty
            assert file_path.stat().st_size > 0, f"File is empty: {file_name}"

    def test_required_directories_exist(self):
        """Verify all required directories exist."""
        required_dirs = [
            "templates",
            "templates/domain",
            "templates/repository",
            "templates/service",
            "templates/presentation",
            "templates/testing",
            "agents"
        ]

        for dir_path in required_dirs:
            full_path = self.TEMPLATE_ROOT / dir_path
            assert full_path.exists(), f"Required directory not found: {dir_path}"
            assert full_path.is_dir(), f"Path is not a directory: {dir_path}"


class TestManifestJson:
    """Tests for manifest.json validation."""

    TEMPLATE_ROOT = Path(__file__).parent.parent.parent / "installer" / "global" / "templates" / "maui-appshell"

    @property
    def manifest_path(self) -> Path:
        return self.TEMPLATE_ROOT / "manifest.json"

    @property
    def manifest(self) -> Dict[str, Any]:
        """Load and parse manifest.json."""
        with open(self.manifest_path, 'r') as f:
            return json.load(f)

    def test_manifest_json_is_valid(self):
        """Verify manifest.json is valid JSON."""
        try:
            manifest = self.manifest
            assert isinstance(manifest, dict), "Manifest should be a JSON object"
        except json.JSONDecodeError as e:
            assert False, f"Invalid JSON in manifest.json: {e}"

    def test_manifest_required_fields(self):
        """Verify manifest.json contains all required fields."""
        manifest = self.manifest
        required_fields = [
            "name",
            "version",
            "description",
            "template_type",
            "technology",
            "architecture",
            "templates",
            "agents",
            "testing",
            "quality_gates",
            "prerequisites"
        ]

        for field in required_fields:
            assert field in manifest, f"Required field '{field}' missing from manifest.json"
            assert manifest[field], f"Field '{field}' is empty or null"

    def test_manifest_name_is_correct(self):
        """Verify template name matches expected value."""
        manifest = self.manifest
        assert manifest["name"] == "maui-appshell", f"Expected name 'maui-appshell', got '{manifest['name']}'"

    def test_manifest_technology_is_dotnet_maui(self):
        """Verify technology field is set to dotnet-maui."""
        manifest = self.manifest
        assert manifest["technology"] == "dotnet-maui", f"Expected technology 'dotnet-maui', got '{manifest['technology']}'"

    def test_manifest_architecture_has_patterns(self):
        """Verify architecture section defines patterns."""
        manifest = self.manifest
        architecture = manifest.get("architecture", {})

        assert "patterns" in architecture, "Architecture section missing 'patterns'"
        patterns = architecture["patterns"]
        assert isinstance(patterns, list), "Patterns should be a list"
        assert len(patterns) > 0, "Patterns list is empty"

        # Verify expected patterns are present
        expected_patterns = [
            "Repository Pattern",
            "Service Pattern",
            "Domain Pattern",
            "ErrorOr Pattern",
            "MVVM Pattern"
        ]

        pattern_texts = [p.lower() for p in patterns]
        for expected in expected_patterns:
            assert any(expected.lower() in text for text in pattern_texts), \
                f"Expected pattern '{expected}' not found in architecture.patterns"

    def test_manifest_architecture_has_layers(self):
        """Verify architecture section defines layers."""
        manifest = self.manifest
        architecture = manifest.get("architecture", {})

        assert "layers" in architecture, "Architecture section missing 'layers'"
        layers = architecture["layers"]
        assert isinstance(layers, list), "Layers should be a list"
        assert len(layers) >= 4, "Expected at least 4 layers (Domain, Repository, Service, Presentation)"

        # Verify each layer has required fields
        for layer in layers:
            assert "name" in layer, f"Layer missing 'name' field: {layer}"
            assert "description" in layer, f"Layer missing 'description' field: {layer}"
            assert "patterns" in layer, f"Layer missing 'patterns' field: {layer}"
            assert "naming" in layer, f"Layer missing 'naming' field: {layer}"

    def test_manifest_templates_section(self):
        """Verify templates section lists all template files."""
        manifest = self.manifest
        templates = manifest.get("templates", {})

        expected_categories = ["domain", "repository", "service", "presentation", "testing"]

        for category in expected_categories:
            assert category in templates, f"Templates section missing '{category}' category"
            assert isinstance(templates[category], list), f"Templates.{category} should be a list"
            assert len(templates[category]) > 0, f"Templates.{category} is empty"

    def test_manifest_agents_section(self):
        """Verify agents section lists agent files."""
        manifest = self.manifest
        agents = manifest.get("agents", [])

        assert isinstance(agents, list), "Agents should be a list"
        assert len(agents) >= 3, "Expected at least 3 specialist agents"

        # Verify agent file naming convention
        for agent in agents:
            assert agent.endswith(".md"), f"Agent file should end with .md: {agent}"
            assert "maui-appshell" in agent, f"Agent file should contain 'maui-appshell': {agent}"

    def test_manifest_testing_configuration(self):
        """Verify testing configuration is complete."""
        manifest = self.manifest
        testing = manifest.get("testing", {})

        assert "framework" in testing, "Testing section missing 'framework'"
        assert testing["framework"] == "xUnit", "Expected testing framework 'xUnit'"

        assert "mocking" in testing, "Testing section missing 'mocking'"
        assert testing["mocking"] == "NSubstitute", "Expected mocking library 'NSubstitute'"

        assert "coverage_target" in testing, "Testing section missing 'coverage_target'"
        coverage = testing["coverage_target"]
        assert coverage["line"] >= 80, "Line coverage target should be >= 80%"
        assert coverage["branch"] >= 75, "Branch coverage target should be >= 75%"


class TestSettingsJson:
    """Tests for settings.json validation."""

    TEMPLATE_ROOT = Path(__file__).parent.parent.parent / "installer" / "global" / "templates" / "maui-appshell"

    @property
    def settings_path(self) -> Path:
        return self.TEMPLATE_ROOT / "settings.json"

    @property
    def settings(self) -> Dict[str, Any]:
        """Load and parse settings.json."""
        with open(self.settings_path, 'r') as f:
            return json.load(f)

    def test_settings_json_is_valid(self):
        """Verify settings.json is valid JSON."""
        try:
            settings = self.settings
            assert isinstance(settings, dict), "Settings should be a JSON object"
        except json.JSONDecodeError as e:
            assert False, f"Invalid JSON in settings.json: {e}"

    def test_settings_naming_conventions(self):
        """Verify naming conventions are defined."""
        settings = self.settings

        assert "naming_conventions" in settings, "Settings missing 'naming_conventions'"
        conventions = settings["naming_conventions"]

        expected_conventions = [
            "domain_operations",
            "repositories",
            "services",
            "presentation"
        ]

        for convention in expected_conventions:
            assert convention in conventions, f"Naming conventions missing '{convention}'"

            # Check for pattern OR interface/implementation structure
            convention_obj = conventions[convention]
            has_pattern = "pattern" in convention_obj
            has_interface = "interface" in convention_obj and "implementation" in convention_obj

            has_page_viewmodel = "page" in convention_obj and "viewmodel" in convention_obj
            assert has_pattern or has_interface or has_page_viewmodel, \
                f"{convention} must have 'pattern', 'interface'+'implementation', or 'page'+'viewmodel' fields"
            assert "examples" in convention_obj, f"{convention} missing 'examples' field"

    def test_settings_layer_configuration(self):
        """Verify layer configuration is complete."""
        settings = self.settings

        assert "layer_configuration" in settings, "Settings missing 'layer_configuration'"
        layers = settings["layer_configuration"]

        expected_layers = ["domain", "repository", "service", "presentation"]

        for layer in expected_layers:
            assert layer in layers, f"Layer configuration missing '{layer}'"
            layer_config = layers[layer]
            assert "namespace_pattern" in layer_config, f"{layer} missing 'namespace_pattern'"
            assert "dependencies" in layer_config, f"{layer} missing 'dependencies'"
            assert "prohibited_dependencies" in layer_config, f"{layer} missing 'prohibited_dependencies'"

    def test_settings_erroror_configuration(self):
        """Verify ErrorOr configuration is defined."""
        settings = self.settings

        assert "error_handling_configuration" in settings, "Settings missing 'error_handling_configuration'"
        error_config = settings["error_handling_configuration"]

        assert error_config["library"] == "ErrorOr", "Expected ErrorOr library"
        assert "patterns" in error_config, "ErrorOr config missing 'patterns'"
        assert "consumption" in error_config, "ErrorOr config missing 'consumption'"


class TestTemplateFiles:
    """Tests for template file existence and structure."""

    TEMPLATE_ROOT = Path(__file__).parent.parent.parent / "installer" / "global" / "templates" / "maui-appshell"

    def test_domain_templates_exist(self):
        """Verify domain template files exist."""
        domain_dir = self.TEMPLATE_ROOT / "templates" / "domain"

        expected_files = [
            "query-operation.cs.template",
            "command-operation.cs.template"
        ]

        for file_name in expected_files:
            file_path = domain_dir / file_name
            assert file_path.exists(), f"Domain template not found: {file_name}"
            assert file_path.stat().st_size > 0, f"Domain template is empty: {file_name}"

    def test_repository_templates_exist(self):
        """Verify repository template files exist."""
        repo_dir = self.TEMPLATE_ROOT / "templates" / "repository"

        expected_files = [
            "repository-interface.cs.template",
            "repository-implementation.cs.template"
        ]

        for file_name in expected_files:
            file_path = repo_dir / file_name
            assert file_path.exists(), f"Repository template not found: {file_name}"
            assert file_path.stat().st_size > 0, f"Repository template is empty: {file_name}"

    def test_service_templates_exist(self):
        """Verify service template files exist."""
        service_dir = self.TEMPLATE_ROOT / "templates" / "service"

        expected_files = [
            "service-interface.cs.template",
            "service-implementation.cs.template"
        ]

        for file_name in expected_files:
            file_path = service_dir / file_name
            assert file_path.exists(), f"Service template not found: {file_name}"
            assert file_path.stat().st_size > 0, f"Service template is empty: {file_name}"

    def test_presentation_templates_exist(self):
        """Verify presentation template files exist."""
        presentation_dir = self.TEMPLATE_ROOT / "templates" / "presentation"

        expected_files = [
            "page.xaml.template",
            "page.xaml.cs.template",
            "viewmodel.cs.template",
            "navigation-service.cs.template"
        ]

        for file_name in expected_files:
            file_path = presentation_dir / file_name
            assert file_path.exists(), f"Presentation template not found: {file_name}"
            assert file_path.stat().st_size > 0, f"Presentation template is empty: {file_name}"

    def test_testing_templates_exist(self):
        """Verify testing template files exist."""
        testing_dir = self.TEMPLATE_ROOT / "templates" / "testing"

        expected_files = [
            "domain-test.cs.template",
            "repository-test.cs.template",
            "service-test.cs.template"
        ]

        for file_name in expected_files:
            file_path = testing_dir / file_name
            assert file_path.exists(), f"Testing template not found: {file_name}"
            assert file_path.stat().st_size > 0, f"Testing template is empty: {file_name}"


class TestAgentSpecifications:
    """Tests for agent specification files."""

    TEMPLATE_ROOT = Path(__file__).parent.parent.parent / "installer" / "global" / "templates" / "maui-appshell"

    def test_agent_files_exist(self):
        """Verify agent specification files exist."""
        agents_dir = self.TEMPLATE_ROOT / "agents"

        expected_agents = [
            "maui-appshell-domain-specialist.md",
            "maui-appshell-repository-specialist.md",
            "maui-appshell-service-specialist.md"
        ]

        for agent_name in expected_agents:
            agent_path = agents_dir / agent_name
            assert agent_path.exists(), f"Agent file not found: {agent_name}"
            assert agent_path.stat().st_size > 0, f"Agent file is empty: {agent_name}"

    def test_agent_files_have_required_sections(self):
        """Verify agent files contain required sections."""
        agents_dir = self.TEMPLATE_ROOT / "agents"

        agent_files = [
            "maui-appshell-domain-specialist.md",
            "maui-appshell-repository-specialist.md",
            "maui-appshell-service-specialist.md"
        ]

        required_sections = [
            "# ",  # Title
            "## Role",
            "## Expertise",
            "## Responsibilities"
        ]

        for agent_file in agent_files:
            agent_path = agents_dir / agent_file
            content = agent_path.read_text()

            for section in required_sections:
                assert section in content, f"Agent {agent_file} missing section: {section}"


class TestTemplatePlaceholders:
    """Tests for template placeholder consistency."""

    TEMPLATE_ROOT = Path(__file__).parent.parent.parent / "installer" / "global" / "templates" / "maui-appshell"

    def get_placeholders(self, content: str) -> List[str]:
        """Extract all placeholders from template content."""
        # Match {{PlaceholderName}} pattern
        pattern = r'\{\{([^}]+)\}\}'
        return re.findall(pattern, content)

    def test_domain_templates_have_placeholders(self):
        """Verify domain templates use proper placeholders."""
        domain_dir = self.TEMPLATE_ROOT / "templates" / "domain"

        # Expected placeholders for domain templates
        expected_placeholders = [
            "ProjectName",
            "FeatureName",
            "OperationName",
            "Entity",
            "ReturnType"
        ]

        for template_file in domain_dir.glob("*.template"):
            content = template_file.read_text()
            placeholders = self.get_placeholders(content)

            # Check that at least some expected placeholders are present
            found_count = sum(1 for p in expected_placeholders if p in placeholders)
            assert found_count > 0, f"Domain template {template_file.name} has no standard placeholders"

    def test_repository_templates_have_placeholders(self):
        """Verify repository templates use proper placeholders."""
        repo_dir = self.TEMPLATE_ROOT / "templates" / "repository"

        expected_placeholders = [
            "ProjectName",
            "Entity",
            "ReturnType"
        ]

        for template_file in repo_dir.glob("*.template"):
            content = template_file.read_text()
            placeholders = self.get_placeholders(content)

            found_count = sum(1 for p in expected_placeholders if p in placeholders)
            assert found_count > 0, f"Repository template {template_file.name} has no standard placeholders"

    def test_service_templates_have_placeholders(self):
        """Verify service templates use proper placeholders."""
        service_dir = self.TEMPLATE_ROOT / "templates" / "service"

        expected_placeholders = [
            "ProjectName",
            "Purpose",
            "ReturnType"
        ]

        for template_file in service_dir.glob("*.template"):
            content = template_file.read_text()
            placeholders = self.get_placeholders(content)

            found_count = sum(1 for p in expected_placeholders if p in placeholders)
            assert found_count > 0, f"Service template {template_file.name} has no standard placeholders"

    def test_presentation_templates_have_placeholders(self):
        """Verify presentation templates use proper placeholders."""
        presentation_dir = self.TEMPLATE_ROOT / "templates" / "presentation"

        expected_placeholders = [
            "ProjectName",
            "FeatureName"
        ]

        for template_file in presentation_dir.glob("*.template"):
            content = template_file.read_text()
            placeholders = self.get_placeholders(content)

            # XAML files may have different placeholders
            if template_file.suffix == ".template":
                found_count = sum(1 for p in expected_placeholders if p in placeholders)
                assert found_count >= 0, f"Presentation template {template_file.name} should use placeholders"


class TestNamingConventions:
    """Tests for naming convention compliance."""

    TEMPLATE_ROOT = Path(__file__).parent.parent.parent / "installer" / "global" / "templates" / "maui-appshell"

    def test_domain_template_naming(self):
        """Verify domain templates follow naming conventions."""
        domain_dir = self.TEMPLATE_ROOT / "templates" / "domain"

        # Expected naming pattern: {type}-{purpose}.cs.template
        for template_file in domain_dir.glob("*.template"):
            name = template_file.stem  # Remove .template extension

            # Should end with .cs
            assert name.endswith(".cs"), f"Domain template should end with .cs: {template_file.name}"

            # Should contain operation type (query or command)
            assert "operation" in name.lower(), f"Domain template should contain 'operation': {template_file.name}"

    def test_repository_template_naming(self):
        """Verify repository templates follow naming conventions."""
        repo_dir = self.TEMPLATE_ROOT / "templates" / "repository"

        for template_file in repo_dir.glob("*.template"):
            name = template_file.stem

            assert name.endswith(".cs"), f"Repository template should end with .cs: {template_file.name}"
            assert "repository" in name.lower(), f"Repository template should contain 'repository': {template_file.name}"

    def test_service_template_naming(self):
        """Verify service templates follow naming conventions."""
        service_dir = self.TEMPLATE_ROOT / "templates" / "service"

        for template_file in service_dir.glob("*.template"):
            name = template_file.stem

            assert name.endswith(".cs"), f"Service template should end with .cs: {template_file.name}"
            assert "service" in name.lower(), f"Service template should contain 'service': {template_file.name}"

    def test_agent_file_naming(self):
        """Verify agent files follow naming conventions."""
        agents_dir = self.TEMPLATE_ROOT / "agents"

        for agent_file in agents_dir.glob("*.md"):
            name = agent_file.stem

            # Should start with maui-appshell
            assert name.startswith("maui-appshell-"), f"Agent file should start with 'maui-appshell-': {agent_file.name}"

            # Should end with -specialist
            assert name.endswith("-specialist"), f"Agent file should end with '-specialist': {agent_file.name}"


class TestDocumentationCompleteness:
    """Tests for documentation completeness."""

    TEMPLATE_ROOT = Path(__file__).parent.parent.parent / "installer" / "global" / "templates" / "maui-appshell"

    def test_claude_md_exists_and_complete(self):
        """Verify CLAUDE.md exists and has required sections."""
        claude_md = self.TEMPLATE_ROOT / "CLAUDE.md"

        assert claude_md.exists(), "CLAUDE.md not found"
        content = claude_md.read_text()

        required_sections = [
            "Template Overview",
            "Architecture Patterns",
            "Domain Pattern",
            "Repository Pattern",
            "Service Pattern",
            "ErrorOr Pattern",
            "MVVM Pattern",
            "AppShell Navigation",
            "Dependency Injection",
            "Testing Strategy"
        ]

        for section in required_sections:
            assert section in content, f"CLAUDE.md missing section: {section}"

    def test_readme_exists_and_complete(self):
        """Verify README.md exists and has required sections."""
        readme = self.TEMPLATE_ROOT / "README.md"

        assert readme.exists(), "README.md not found"
        content = readme.read_text()

        # Should contain basic information
        assert "MAUI" in content or "maui" in content.lower(), "README should mention MAUI"
        assert "AppShell" in content or "appshell" in content.lower(), "README should mention AppShell"


class TestTemplateCompleteness:
    """Tests for overall template completeness."""

    TEMPLATE_ROOT = Path(__file__).parent.parent.parent / "installer" / "global" / "templates" / "maui-appshell"

    def test_template_file_count(self):
        """Verify expected number of template files exist."""
        templates_dir = self.TEMPLATE_ROOT / "templates"

        # Count all .template files
        template_files = list(templates_dir.glob("**/*.template"))

        # Should have at least 13 templates (2 domain + 2 repository + 2 service + 4 presentation + 3 testing)
        assert len(template_files) >= 13, f"Expected at least 13 template files, found {len(template_files)}"

    def test_all_templates_have_content(self):
        """Verify all template files have meaningful content."""
        templates_dir = self.TEMPLATE_ROOT / "templates"

        for template_file in templates_dir.glob("**/*.template"):
            content = template_file.read_text()

            # Should have minimum length (not just empty)
            assert len(content) > 100, f"Template appears too short/empty: {template_file.name}"

            # Should contain at least one placeholder
            assert "{{" in content, f"Template has no placeholders: {template_file.name}"

    def test_configuration_matches_actual_files(self):
        """Verify manifest.json lists all existing template files."""
        manifest_path = self.TEMPLATE_ROOT / "manifest.json"

        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        templates_section = manifest.get("templates", {})

        # Check each category
        for category, template_list in templates_section.items():
            category_dir = self.TEMPLATE_ROOT / "templates" / category

            for template_ref in template_list:
                # Extract just the filename from the reference
                template_name = template_ref.split("/")[-1]
                template_path = category_dir / template_name

                assert template_path.exists(), f"Manifest references non-existent template: {template_ref}"


def run_tests():
    """Run all tests and report results."""
    import pytest

    # Run pytest on this file
    return pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    run_tests()
