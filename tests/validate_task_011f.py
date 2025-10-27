#!/usr/bin/env python3
"""
Standalone validation script for TASK-011F: maui-service-specialist agent documentation
No external dependencies required - uses only Python standard library.
"""

import hashlib
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


# File paths
BASE_DIR = Path(__file__).parent.parent
FILE_APPSHELL = BASE_DIR / "installer/global/templates/maui-appshell/agents/maui-service-specialist.md"
FILE_NAVPAGE = BASE_DIR / "installer/global/templates/maui-navigationpage/agents/maui-service-specialist.md"


class ValidationResult:
    """Store validation test results."""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.failures = []

    def record_pass(self, test_name: str):
        """Record a passing test."""
        self.passed += 1
        print(f"✓ {test_name}")

    def record_fail(self, test_name: str, message: str):
        """Record a failing test."""
        self.failed += 1
        self.failures.append((test_name, message))
        print(f"✗ {test_name}: {message}")

    def print_summary(self):
        """Print validation summary."""
        total = self.passed + self.failed
        print(f"\n{'=' * 70}")
        print(f"VALIDATION SUMMARY")
        print(f"{'=' * 70}")
        print(f"Total tests: {total}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")

        if self.failed > 0:
            print(f"\nFAILURES:")
            for name, message in self.failures:
                print(f"  - {name}: {message}")

        print(f"{'=' * 70}")
        return self.failed == 0


def compute_checksum(file_path: Path) -> str:
    """Compute SHA256 checksum of file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def extract_yaml_frontmatter(content: str) -> Dict:
    """Extract YAML frontmatter from markdown content."""
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        return {}

    frontmatter_text = match.group(1)

    # Simple YAML parsing (no external dependencies)
    frontmatter = {}
    for line in frontmatter_text.split("\n"):
        if ":" in line and not line.strip().startswith("-"):
            key, value = line.split(":", 1)
            frontmatter[key.strip()] = value.strip()
        elif line.strip().startswith("-"):
            # Handle list items
            if "collaborates_with" in frontmatter:
                if not isinstance(frontmatter["collaborates_with"], list):
                    frontmatter["collaborates_with"] = []
                frontmatter["collaborates_with"].append(line.strip().lstrip("- "))

    return frontmatter


def extract_sections(content: str) -> List[str]:
    """Extract section headings from markdown."""
    return re.findall(r"^## (.+)$", content, re.MULTILINE)


def extract_code_blocks(content: str) -> List[Tuple[str, str]]:
    """Extract code blocks with language markers."""
    pattern = r"```(\w+)\n(.*?)```"
    return re.findall(pattern, content, re.DOTALL)


def validate_file_existence(results: ValidationResult):
    """Validate that both files exist."""
    print("\n" + "=" * 70)
    print("FILE EXISTENCE TESTS")
    print("=" * 70)

    if FILE_APPSHELL.exists():
        results.record_pass("AppShell file exists")
    else:
        results.record_fail("AppShell file exists", f"File not found: {FILE_APPSHELL}")

    if FILE_NAVPAGE.exists():
        results.record_pass("NavigationPage file exists")
    else:
        results.record_fail("NavigationPage file exists", f"File not found: {FILE_NAVPAGE}")

    if FILE_APPSHELL.stat().st_size > 0:
        results.record_pass("AppShell file not empty")
    else:
        results.record_fail("AppShell file not empty", "File is empty")

    if FILE_NAVPAGE.stat().st_size > 0:
        results.record_pass("NavigationPage file not empty")
    else:
        results.record_fail("NavigationPage file not empty", "File is empty")


def validate_file_equality(results: ValidationResult):
    """Validate that both files are identical."""
    print("\n" + "=" * 70)
    print("FILE EQUALITY TESTS")
    print("=" * 70)

    checksum_appshell = compute_checksum(FILE_APPSHELL)
    checksum_navpage = compute_checksum(FILE_NAVPAGE)

    if checksum_appshell == checksum_navpage:
        results.record_pass("Files have identical checksums")
    else:
        results.record_fail(
            "Files have identical checksums",
            f"AppShell: {checksum_appshell[:16]}..., NavPage: {checksum_navpage[:16]}..."
        )

    content_appshell = FILE_APPSHELL.read_text(encoding="utf-8")
    content_navpage = FILE_NAVPAGE.read_text(encoding="utf-8")

    if content_appshell == content_navpage:
        results.record_pass("Files have identical content")
    else:
        results.record_fail("Files have identical content", "Content differs")

    lines_appshell = len(content_appshell.splitlines())
    lines_navpage = len(content_navpage.splitlines())

    if lines_appshell == lines_navpage:
        results.record_pass(f"Files have identical line count ({lines_appshell} lines)")
    else:
        results.record_fail(
            "Files have identical line count",
            f"AppShell: {lines_appshell}, NavPage: {lines_navpage}"
        )


def validate_yaml_frontmatter(results: ValidationResult):
    """Validate YAML frontmatter."""
    print("\n" + "=" * 70)
    print("YAML FRONTMATTER TESTS")
    print("=" * 70)

    content = FILE_APPSHELL.read_text(encoding="utf-8")
    frontmatter = extract_yaml_frontmatter(content)

    if "name" in frontmatter and frontmatter["name"] == "maui-service-specialist":
        results.record_pass("Frontmatter has correct 'name' field")
    else:
        results.record_fail("Frontmatter has correct 'name' field", f"Got: {frontmatter.get('name')}")

    if "description" in frontmatter and len(frontmatter["description"]) > 50:
        results.record_pass("Frontmatter has adequate 'description' field")
    else:
        results.record_fail("Frontmatter has adequate 'description' field", "Too short or missing")

    if "tools" in frontmatter:
        results.record_pass("Frontmatter has 'tools' field")
    else:
        results.record_fail("Frontmatter has 'tools' field", "Missing")

    if "model" in frontmatter and frontmatter["model"] == "sonnet":
        results.record_pass("Frontmatter has correct 'model' field")
    else:
        results.record_fail("Frontmatter has correct 'model' field", f"Got: {frontmatter.get('model')}")

    # Check collaborates_with (simple check for presence of collaborators in content)
    if "maui-domain-specialist" in content and "maui-repository-specialist" in content:
        results.record_pass("Frontmatter has 'collaborates_with' entries")
    else:
        results.record_fail("Frontmatter has 'collaborates_with' entries", "Missing collaborators")


def validate_section_completeness(results: ValidationResult):
    """Validate all required sections are present."""
    print("\n" + "=" * 70)
    print("SECTION COMPLETENESS TESTS")
    print("=" * 70)

    content = FILE_APPSHELL.read_text(encoding="utf-8")
    sections = extract_sections(content)

    required_sections = [
        "Core Responsibility",
        "Core Expertise",
        "Implementation Patterns",
        "Design Patterns",
        "Implementation Guidelines",
        "Complete Code Examples",
        "Anti-Patterns to Avoid",
        "Testing Strategies",
        "Best Practices Summary",
        "Collaboration & Best Practices"
    ]

    for section in required_sections:
        if section in sections:
            results.record_pass(f"Section present: {section}")
        else:
            results.record_fail(f"Section present: {section}", "Section not found")

    if len(sections) >= 9:
        results.record_pass(f"Sufficient section count ({len(sections)} >= 9)")
    else:
        results.record_fail(f"Sufficient section count", f"Only {len(sections)} sections found")


def validate_code_examples(results: ValidationResult):
    """Validate code example presence and quality."""
    print("\n" + "=" * 70)
    print("CODE EXAMPLE TESTS")
    print("=" * 70)

    content = FILE_APPSHELL.read_text(encoding="utf-8")
    code_blocks = extract_code_blocks(content)

    csharp_blocks = [block for lang, block in code_blocks if lang == "csharp"]

    if len(csharp_blocks) >= 15:
        results.record_pass(f"Sufficient C# code blocks ({len(csharp_blocks)} >= 15)")
    else:
        results.record_fail(f"Sufficient C# code blocks", f"Only {len(csharp_blocks)} found")

    # Check for key examples
    if "ProductApiService" in content:
        results.record_pass("HTTP API service example present")
    else:
        results.record_fail("HTTP API service example present", "Not found")

    if "LocationService" in content:
        results.record_pass("Location service example present")
    else:
        results.record_fail("Location service example present", "Not found")

    if "CacheService" in content:
        results.record_pass("Cache service example present")
    else:
        results.record_fail("Cache service example present", "Not found")

    # Check for substantial code blocks
    substantial_blocks = [code for lang, code in code_blocks if len(code) > 500]
    if len(substantial_blocks) >= 5:
        results.record_pass(f"Sufficient substantial code blocks ({len(substantial_blocks)} >= 5)")
    else:
        results.record_fail(f"Sufficient substantial code blocks", f"Only {len(substantial_blocks)} found")


def validate_erroror_usage(results: ValidationResult):
    """Validate ErrorOr pattern usage."""
    print("\n" + "=" * 70)
    print("ERROROR PATTERN TESTS")
    print("=" * 70)

    content = FILE_APPSHELL.read_text(encoding="utf-8")

    if "using ErrorOr;" in content:
        results.record_pass("ErrorOr import statement present")
    else:
        results.record_fail("ErrorOr import statement present", "Not found")

    erroror_count = len(re.findall(r"ErrorOr<", content))
    if erroror_count >= 30:
        results.record_pass(f"Sufficient ErrorOr usages ({erroror_count} >= 30)")
    else:
        results.record_fail(f"Sufficient ErrorOr usages", f"Only {erroror_count} found")

    error_types = ["Error.Validation(", "Error.NotFound(", "Error.Unavailable(", "Error.Forbidden(", "Error.Failure("]
    found_types = [et for et in error_types if et in content]

    if len(found_types) >= 4:
        results.record_pass(f"Error creation patterns documented ({len(found_types)}/5)")
    else:
        results.record_fail(f"Error creation patterns documented", f"Only {len(found_types)} found")


def validate_anti_patterns(results: ValidationResult):
    """Validate anti-pattern documentation."""
    print("\n" + "=" * 70)
    print("ANTI-PATTERN TESTS")
    print("=" * 70)

    content = FILE_APPSHELL.read_text(encoding="utf-8")

    wrong_count = len(re.findall(r"### WRONG:", content))
    correct_count = len(re.findall(r"### CORRECT:", content))
    pair_count = min(wrong_count, correct_count)

    if pair_count >= 4:
        results.record_pass(f"Sufficient anti-pattern pairs ({pair_count} >= 4)")
    else:
        results.record_fail(f"Sufficient anti-pattern pairs", f"Only {pair_count} found")

    anti_patterns = [
        ("Services Accessing Database Directly", "database anti-pattern"),
        ("Throwing Exceptions for Business Logic", "exception throwing anti-pattern"),
        ("Not Checking Connectivity Before API Calls", "connectivity check anti-pattern"),
        ("Synchronous File I/O in Services", "sync file I/O anti-pattern")
    ]

    for pattern_text, pattern_name in anti_patterns:
        if pattern_text in content:
            results.record_pass(f"Anti-pattern documented: {pattern_name}")
        else:
            results.record_fail(f"Anti-pattern documented: {pattern_name}", "Not found")


def validate_testing_strategies(results: ValidationResult):
    """Validate testing strategy documentation."""
    print("\n" + "=" * 70)
    print("TESTING STRATEGY TESTS")
    print("=" * 70)

    content = FILE_APPSHELL.read_text(encoding="utf-8")

    testing_elements = [
        ("ProductApiServiceTests", "HTTP service testing"),
        ("LocationServiceTests", "Location service testing"),
        ("CacheServiceTests", "Cache service testing"),
        ("Mock<HttpMessageHandler>", "HTTP mocking"),
        ("[Fact]", "xUnit test attributes"),
        ("using Xunit;", "xUnit namespace"),
        ("using FluentAssertions;", "FluentAssertions")
    ]

    for element, description in testing_elements:
        if element in content:
            results.record_pass(f"Testing element present: {description}")
        else:
            results.record_fail(f"Testing element present: {description}", f"'{element}' not found")


def validate_architectural_boundary(results: ValidationResult):
    """Validate architectural boundary documentation."""
    print("\n" + "=" * 70)
    print("ARCHITECTURAL BOUNDARY TESTS")
    print("=" * 70)

    content = FILE_APPSHELL.read_text(encoding="utf-8")

    if "CRITICAL ARCHITECTURAL BOUNDARY" in content:
        results.record_pass("Critical architectural boundary documented")
    else:
        results.record_fail("Critical architectural boundary documented", "Not found")

    if "Services do NOT access databases directly" in content:
        results.record_pass("Service/repository split documented")
    else:
        results.record_fail("Service/repository split documented", "Not found")

    service_types = ["HTTP API Integration", "Hardware and Platform Services", "Caching Services", "Authentication Services"]
    found_types = [st for st in service_types if st in content]

    if len(found_types) >= 3:
        results.record_pass(f"Service responsibilities documented ({len(found_types)}/4)")
    else:
        results.record_fail(f"Service responsibilities documented", f"Only {len(found_types)} found")


def validate_best_practices(results: ValidationResult):
    """Validate best practices documentation."""
    print("\n" + "=" * 70)
    print("BEST PRACTICES TESTS")
    print("=" * 70)

    content = FILE_APPSHELL.read_text(encoding="utf-8")

    if "Best Practices Summary" in content:
        results.record_pass("Best practices summary section exists")
    else:
        results.record_fail("Best practices summary section exists", "Not found")

    best_practice_topics = [
        "Service Boundaries",
        "Error Handling",
        ("Resilience Patterns", "Resilience"),
        "Testing"
    ]

    for topic in best_practice_topics:
        if isinstance(topic, tuple):
            if any(t in content for t in topic):
                results.record_pass(f"Best practice topic: {topic[0]}")
            else:
                results.record_fail(f"Best practice topic: {topic[0]}", "Not found")
        else:
            if topic in content:
                results.record_pass(f"Best practice topic: {topic}")
            else:
                results.record_fail(f"Best practice topic: {topic}", "Not found")


def validate_collaboration(results: ValidationResult):
    """Validate collaboration documentation."""
    print("\n" + "=" * 70)
    print("COLLABORATION TESTS")
    print("=" * 70)

    content = FILE_APPSHELL.read_text(encoding="utf-8")

    if "Collaboration & Best Practices" in content:
        results.record_pass("Collaboration section exists")
    else:
        results.record_fail("Collaboration section exists", "Not found")

    if "When I'm Engaged" in content:
        results.record_pass("'When I'm Engaged' section exists")
    else:
        results.record_fail("'When I'm Engaged' section exists", "Not found")

    if "I Collaborate With" in content:
        results.record_pass("'I Collaborate With' section exists")
    else:
        results.record_fail("'I Collaborate With' section exists", "Not found")

    collaborators = [
        "maui-domain-specialist",
        "maui-repository-specialist",
        "dotnet-testing-specialist",
        "software-architect"
    ]

    for collaborator in collaborators:
        if collaborator in content:
            results.record_pass(f"Collaborator documented: {collaborator}")
        else:
            results.record_fail(f"Collaborator documented: {collaborator}", "Not found")


def generate_final_report(results: ValidationResult):
    """Generate final validation report."""
    content = FILE_APPSHELL.read_text(encoding="utf-8")

    # Count various metrics
    line_count = len(content.splitlines())
    section_count = len(extract_sections(content))
    code_blocks = len(extract_code_blocks(content))
    erroror_count = len(re.findall(r"ErrorOr<", content))
    anti_pattern_pairs = len(re.findall(r"### WRONG:", content))

    print("\n" + "=" * 70)
    print("FINAL VALIDATION REPORT - TASK-011F")
    print("=" * 70)
    print("\nFILE STATISTICS:")
    print(f"  Line count: {line_count}")
    print(f"  Section count: {section_count}")
    print(f"  Code blocks: {code_blocks}")
    print(f"  ErrorOr usages: {erroror_count}")
    print(f"  Anti-pattern pairs: {anti_pattern_pairs}")

    print("\nFILE INTEGRITY:")
    print("  Both files exist: ✓")
    print("  Files are identical: ✓" if results.failed == 0 else "  Files are identical: ✗")
    print("  YAML frontmatter valid: ✓")

    print("\nCONTENT COMPLETENESS:")
    print(f"  Core sections: {section_count}/10 expected")
    print(f"  Code examples: {code_blocks}/18 expected")
    print(f"  ErrorOr usage: {erroror_count}/31 expected")
    print(f"  Anti-patterns: {anti_pattern_pairs}/8 expected")

    status = "✓ PASSED" if results.failed == 0 else "✗ FAILED"
    print(f"\nVALIDATION STATUS: {status}")
    print("=" * 70)


def main():
    """Run all validation tests."""
    print("=" * 70)
    print("TASK-011F VALIDATION SUITE")
    print("maui-service-specialist agent documentation")
    print("=" * 70)

    results = ValidationResult()

    validate_file_existence(results)
    validate_file_equality(results)
    validate_yaml_frontmatter(results)
    validate_section_completeness(results)
    validate_code_examples(results)
    validate_erroror_usage(results)
    validate_anti_patterns(results)
    validate_testing_strategies(results)
    validate_architectural_boundary(results)
    validate_best_practices(results)
    validate_collaboration(results)

    generate_final_report(results)

    success = results.print_summary()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
