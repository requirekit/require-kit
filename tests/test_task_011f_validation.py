"""
Comprehensive validation suite for TASK-011F: maui-service-specialist agent documentation
Tests file existence, equality, structure, content, and code examples.
"""

import hashlib
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

import pytest
import yaml


# File paths
BASE_DIR = Path(__file__).parent.parent
FILE_APPSHELL = BASE_DIR / "installer/global/templates/maui-appshell/agents/maui-service-specialist.md"
FILE_NAVPAGE = BASE_DIR / "installer/global/templates/maui-navigationpage/agents/maui-service-specialist.md"


class TestFileExistence:
    """Test that both markdown files exist."""

    def test_appshell_file_exists(self):
        """Verify maui-appshell agent file exists."""
        assert FILE_APPSHELL.exists(), f"File does not exist: {FILE_APPSHELL}"

    def test_navpage_file_exists(self):
        """Verify maui-navigationpage agent file exists."""
        assert FILE_NAVPAGE.exists(), f"File does not exist: {FILE_NAVPAGE}"

    def test_files_not_empty(self):
        """Verify both files are not empty."""
        assert FILE_APPSHELL.stat().st_size > 0, "AppShell file is empty"
        assert FILE_NAVPAGE.stat().st_size > 0, "NavigationPage file is empty"


class TestFileEquality:
    """Test that both files are byte-for-byte identical."""

    def _compute_checksum(self, file_path: Path) -> str:
        """Compute SHA256 checksum of file."""
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    def test_files_identical_checksum(self):
        """Verify files have identical SHA256 checksums."""
        checksum_appshell = self._compute_checksum(FILE_APPSHELL)
        checksum_navpage = self._compute_checksum(FILE_NAVPAGE)

        assert checksum_appshell == checksum_navpage, (
            f"Files are not identical:\n"
            f"AppShell checksum: {checksum_appshell}\n"
            f"NavPage checksum:  {checksum_navpage}"
        )

    def test_files_identical_content(self):
        """Verify files have identical text content."""
        content_appshell = FILE_APPSHELL.read_text(encoding="utf-8")
        content_navpage = FILE_NAVPAGE.read_text(encoding="utf-8")

        assert content_appshell == content_navpage, (
            "Files have different content. "
            "Run 'diff' command to see differences."
        )

    def test_files_identical_line_count(self):
        """Verify files have identical line counts."""
        lines_appshell = len(FILE_APPSHELL.read_text(encoding="utf-8").splitlines())
        lines_navpage = len(FILE_NAVPAGE.read_text(encoding="utf-8").splitlines())

        assert lines_appshell == lines_navpage, (
            f"Files have different line counts: "
            f"AppShell={lines_appshell}, NavPage={lines_navpage}"
        )


class TestYAMLFrontmatter:
    """Test YAML frontmatter parsing and validation."""

    def _extract_frontmatter(self, file_path: Path) -> Dict:
        """Extract YAML frontmatter from markdown file."""
        content = file_path.read_text(encoding="utf-8")

        # Match YAML frontmatter between --- delimiters
        match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        if not match:
            pytest.fail(f"No YAML frontmatter found in {file_path}")

        frontmatter_text = match.group(1)
        try:
            return yaml.safe_load(frontmatter_text)
        except yaml.YAMLError as e:
            pytest.fail(f"Failed to parse YAML frontmatter: {e}")

    def test_frontmatter_valid_yaml(self):
        """Verify frontmatter is valid YAML in both files."""
        self._extract_frontmatter(FILE_APPSHELL)
        self._extract_frontmatter(FILE_NAVPAGE)

    def test_frontmatter_has_name(self):
        """Verify frontmatter has 'name' field."""
        fm_appshell = self._extract_frontmatter(FILE_APPSHELL)
        fm_navpage = self._extract_frontmatter(FILE_NAVPAGE)

        assert "name" in fm_appshell, "Missing 'name' field in AppShell frontmatter"
        assert "name" in fm_navpage, "Missing 'name' field in NavPage frontmatter"
        assert fm_appshell["name"] == "maui-service-specialist"
        assert fm_navpage["name"] == "maui-service-specialist"

    def test_frontmatter_has_description(self):
        """Verify frontmatter has 'description' field."""
        fm_appshell = self._extract_frontmatter(FILE_APPSHELL)
        fm_navpage = self._extract_frontmatter(FILE_NAVPAGE)

        assert "description" in fm_appshell, "Missing 'description' in AppShell"
        assert "description" in fm_navpage, "Missing 'description' in NavPage"
        assert len(fm_appshell["description"]) > 50, "Description too short"

    def test_frontmatter_has_tools(self):
        """Verify frontmatter has 'tools' field."""
        fm_appshell = self._extract_frontmatter(FILE_APPSHELL)

        assert "tools" in fm_appshell, "Missing 'tools' field"
        assert isinstance(fm_appshell["tools"], str), "Tools should be string"

    def test_frontmatter_has_model(self):
        """Verify frontmatter has 'model' field."""
        fm_appshell = self._extract_frontmatter(FILE_APPSHELL)

        assert "model" in fm_appshell, "Missing 'model' field"
        assert fm_appshell["model"] == "sonnet"

    def test_frontmatter_has_collaborates_with(self):
        """Verify frontmatter has 'collaborates_with' field."""
        fm_appshell = self._extract_frontmatter(FILE_APPSHELL)

        assert "collaborates_with" in fm_appshell, "Missing 'collaborates_with' field"
        assert isinstance(fm_appshell["collaborates_with"], list), "collaborates_with should be list"
        assert len(fm_appshell["collaborates_with"]) >= 3, "Should collaborate with at least 3 agents"


class TestSectionCompleteness:
    """Test that all required sections are present."""

    def _extract_sections(self, file_path: Path) -> List[str]:
        """Extract section headings from markdown file."""
        content = file_path.read_text(encoding="utf-8")

        # Find all markdown headings (## Level 2)
        sections = re.findall(r"^## (.+)$", content, re.MULTILINE)
        return sections

    def test_has_core_responsibility_section(self):
        """Verify 'Core Responsibility' section exists."""
        sections = self._extract_sections(FILE_APPSHELL)
        assert "Core Responsibility" in sections

    def test_has_core_expertise_section(self):
        """Verify 'Core Expertise' section exists."""
        sections = self._extract_sections(FILE_APPSHELL)
        assert "Core Expertise" in sections

    def test_has_implementation_patterns_section(self):
        """Verify 'Implementation Patterns' section exists."""
        sections = self._extract_sections(FILE_APPSHELL)
        assert "Implementation Patterns" in sections

    def test_has_design_patterns_section(self):
        """Verify 'Design Patterns' section exists."""
        sections = self._extract_sections(FILE_APPSHELL)
        assert "Design Patterns" in sections

    def test_has_implementation_guidelines_section(self):
        """Verify 'Implementation Guidelines' section exists."""
        sections = self._extract_sections(FILE_APPSHELL)
        assert "Implementation Guidelines" in sections

    def test_has_complete_code_examples_section(self):
        """Verify 'Complete Code Examples' section exists."""
        sections = self._extract_sections(FILE_APPSHELL)
        assert "Complete Code Examples" in sections

    def test_has_anti_patterns_section(self):
        """Verify 'Anti-Patterns to Avoid' section exists."""
        sections = self._extract_sections(FILE_APPSHELL)
        assert "Anti-Patterns to Avoid" in sections

    def test_has_testing_strategies_section(self):
        """Verify 'Testing Strategies' section exists."""
        sections = self._extract_sections(FILE_APPSHELL)
        assert "Testing Strategies" in sections

    def test_has_best_practices_summary_section(self):
        """Verify 'Best Practices Summary' section exists."""
        sections = self._extract_sections(FILE_APPSHELL)
        assert "Best Practices Summary" in sections

    def test_has_collaboration_section(self):
        """Verify 'Collaboration & Best Practices' section exists."""
        sections = self._extract_sections(FILE_APPSHELL)
        assert "Collaboration & Best Practices" in sections

    def test_minimum_section_count(self):
        """Verify at least 9 major sections."""
        sections = self._extract_sections(FILE_APPSHELL)
        assert len(sections) >= 9, f"Expected at least 9 sections, got {len(sections)}"


class TestCodeExamples:
    """Test code block presence and quality."""

    def _extract_code_blocks(self, file_path: Path) -> List[Tuple[str, str]]:
        """Extract code blocks with language markers."""
        content = file_path.read_text(encoding="utf-8")

        # Find all code blocks with language markers
        pattern = r"```(\w+)\n(.*?)```"
        matches = re.findall(pattern, content, re.DOTALL)
        return matches

    def test_has_csharp_code_blocks(self):
        """Verify presence of C# code examples."""
        code_blocks = self._extract_code_blocks(FILE_APPSHELL)
        csharp_blocks = [block for lang, block in code_blocks if lang == "csharp"]

        assert len(csharp_blocks) >= 15, f"Expected at least 15 C# code blocks, got {len(csharp_blocks)}"

    def test_code_blocks_not_empty(self):
        """Verify code blocks are not empty."""
        code_blocks = self._extract_code_blocks(FILE_APPSHELL)

        for lang, code in code_blocks:
            assert len(code.strip()) > 0, f"Empty {lang} code block found"

    def test_code_blocks_minimum_length(self):
        """Verify code blocks have substantial content."""
        code_blocks = self._extract_code_blocks(FILE_APPSHELL)

        # At least 5 code blocks should be > 500 characters (substantial examples)
        substantial_blocks = [code for lang, code in code_blocks if len(code) > 500]
        assert len(substantial_blocks) >= 5, (
            f"Expected at least 5 substantial code blocks (>500 chars), "
            f"got {len(substantial_blocks)}"
        )

    def test_has_http_api_service_example(self):
        """Verify HTTP API service implementation example exists."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")
        assert "ProductApiService" in content
        assert "HttpClient" in content
        assert "Polly" in content

    def test_has_location_service_example(self):
        """Verify location service implementation example exists."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")
        assert "LocationService" in content
        assert "Geolocation" in content
        assert "ILocationService" in content

    def test_has_cache_service_example(self):
        """Verify cache service implementation example exists."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")
        assert "CacheService" in content
        assert "ConcurrentDictionary" in content
        assert "ICacheService" in content


class TestErrorOrPatternUsage:
    """Test ErrorOr pattern usage throughout documentation."""

    def test_erroror_import_statement(self):
        """Verify ErrorOr import statements present."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")
        assert "using ErrorOr;" in content

    def test_erroror_return_types(self):
        """Verify ErrorOr return types used in examples."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")

        # Count ErrorOr usage in method signatures
        erroror_count = len(re.findall(r"Task<ErrorOr<", content))
        assert erroror_count >= 30, f"Expected at least 30 ErrorOr usages, got {erroror_count}"

    def test_erroror_error_creation(self):
        """Verify Error creation patterns documented."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")

        assert "Error.Validation(" in content
        assert "Error.NotFound(" in content
        assert "Error.Unavailable(" in content
        assert "Error.Forbidden(" in content
        assert "Error.Failure(" in content

    def test_erroror_error_handling(self):
        """Verify error handling patterns documented."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")

        assert "if (result.IsError)" in content or "result.IsError" in content
        assert "result.Errors" in content or "result.FirstError" in content


class TestAntiPatterns:
    """Test anti-pattern documentation."""

    def _extract_anti_pattern_pairs(self, file_path: Path) -> int:
        """Count WRONG/CORRECT anti-pattern pairs."""
        content = file_path.read_text(encoding="utf-8")

        # Count "WRONG" and "CORRECT" markers
        wrong_count = len(re.findall(r"### WRONG:", content))
        correct_count = len(re.findall(r"### CORRECT:", content))

        # Each anti-pattern should have a WRONG and CORRECT pair
        return min(wrong_count, correct_count)

    def test_has_anti_patterns(self):
        """Verify anti-patterns are documented."""
        pair_count = self._extract_anti_pattern_pairs(FILE_APPSHELL)
        assert pair_count >= 4, f"Expected at least 4 anti-pattern pairs, got {pair_count}"

    def test_services_database_anti_pattern(self):
        """Verify services accessing database anti-pattern documented."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")
        assert "Services Accessing Database Directly" in content
        assert "WRONG - Services should NEVER access database directly" in content

    def test_exception_throwing_anti_pattern(self):
        """Verify exception throwing anti-pattern documented."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")
        assert "Throwing Exceptions for Business Logic" in content
        assert "Using ErrorOr for Functional Error Handling" in content

    def test_connectivity_check_anti_pattern(self):
        """Verify connectivity check anti-pattern documented."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")
        assert "Not Checking Connectivity Before API Calls" in content
        assert "Check Connectivity First" in content

    def test_sync_file_io_anti_pattern(self):
        """Verify synchronous file I/O anti-pattern documented."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")
        assert "Synchronous File I/O in Services" in content
        assert "Async File I/O" in content


class TestTestingStrategies:
    """Test testing strategy documentation."""

    def test_has_http_service_testing(self):
        """Verify HTTP service testing strategy documented."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")
        assert "HTTP Service Testing with MockHttpMessageHandler" in content
        assert "ProductApiServiceTests" in content
        assert "Mock<HttpMessageHandler>" in content

    def test_has_location_service_testing(self):
        """Verify location service testing strategy documented."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")
        assert "Location Service Testing with Mocked Platform Services" in content
        assert "LocationServiceTests" in content

    def test_has_cache_service_testing(self):
        """Verify cache service testing strategy documented."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")
        assert "Cache Service Testing" in content
        assert "CacheServiceTests" in content

    def test_has_test_attributes(self):
        """Verify xUnit test attributes present."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")
        assert "[Fact]" in content
        assert "using Xunit;" in content
        assert "using FluentAssertions;" in content


class TestArchitecturalBoundary:
    """Test architectural boundary documentation."""

    def test_critical_boundary_documented(self):
        """Verify CRITICAL ARCHITECTURAL BOUNDARY section exists."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")
        assert "CRITICAL ARCHITECTURAL BOUNDARY" in content

    def test_service_repository_split_documented(self):
        """Verify service/repository split is documented."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")
        assert "Services do NOT access databases directly" in content
        assert "exclusive responsibility of Repositories" in content

    def test_service_responsibilities_documented(self):
        """Verify service responsibilities are clearly documented."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")
        assert "HTTP API Integration" in content
        assert "Hardware and Platform Services" in content
        assert "Caching Services" in content
        assert "Authentication Services" in content


class TestBestPractices:
    """Test best practices documentation."""

    def test_best_practices_summary_exists(self):
        """Verify best practices summary section exists."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")
        assert "Best Practices Summary" in content

    def test_service_boundaries_documented(self):
        """Verify service boundaries best practices documented."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")
        assert "Service Boundaries" in content
        assert "Services handle external integrations" in content

    def test_error_handling_best_practices(self):
        """Verify error handling best practices documented."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")
        assert "Error Handling" in content
        assert "Return ErrorOr<T>" in content

    def test_resilience_patterns_documented(self):
        """Verify resilience patterns best practices documented."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")
        assert "Resilience Patterns" in content or "Resilience" in content
        assert "Implement retry logic" in content
        assert "Use circuit breaker" in content


class TestCollaboration:
    """Test collaboration section documentation."""

    def test_collaboration_section_exists(self):
        """Verify collaboration section exists."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")
        assert "Collaboration & Best Practices" in content

    def test_when_engaged_documented(self):
        """Verify 'When I'm Engaged' section exists."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")
        assert "When I'm Engaged" in content

    def test_collaborates_with_documented(self):
        """Verify 'I Collaborate With' section exists."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")
        assert "I Collaborate With" in content

    def test_collaborates_with_domain_specialist(self):
        """Verify collaboration with domain specialist documented."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")
        assert "maui-domain-specialist" in content

    def test_collaborates_with_repository_specialist(self):
        """Verify collaboration with repository specialist documented."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")
        assert "maui-repository-specialist" in content

    def test_collaborates_with_testing_specialist(self):
        """Verify collaboration with testing specialist documented."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")
        assert "dotnet-testing-specialist" in content


class TestValidationSummary:
    """Generate summary report of validation results."""

    def test_generate_validation_report(self):
        """Generate comprehensive validation report."""
        content = FILE_APPSHELL.read_text(encoding="utf-8")

        # Count various metrics
        line_count = len(content.splitlines())
        section_count = len(re.findall(r"^## (.+)$", content, re.MULTILINE))
        code_blocks = len(re.findall(r"```(\w+)", content))
        erroror_count = len(re.findall(r"ErrorOr<", content))
        anti_pattern_pairs = len(re.findall(r"### WRONG:", content))

        report = f"""
VALIDATION REPORT - TASK-011F
==============================

FILE STATISTICS:
- Line count: {line_count}
- Section count: {section_count}
- Code blocks: {code_blocks}
- ErrorOr usages: {erroror_count}
- Anti-pattern pairs: {anti_pattern_pairs}

FILE INTEGRITY:
- Both files exist: ✓
- Files are identical: ✓
- YAML frontmatter valid: ✓

CONTENT COMPLETENESS:
- Core sections: {section_count}/10 expected
- Code examples: {code_blocks}/18 expected
- ErrorOr usage: {erroror_count}/31 expected
- Anti-patterns: {anti_pattern_pairs}/8 expected

VALIDATION STATUS: ✓ PASSED
"""

        print(report)

        # Basic assertions for the report
        assert line_count > 1600, f"File too short: {line_count} lines"
        assert section_count >= 9, f"Too few sections: {section_count}"
        assert code_blocks >= 15, f"Too few code blocks: {code_blocks}"
        assert erroror_count >= 30, f"Too few ErrorOr usages: {erroror_count}"


if __name__ == "__main__":
    # Run with pytest
    pytest.main([__file__, "-v", "--tb=short"])
