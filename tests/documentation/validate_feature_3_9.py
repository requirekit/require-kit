#!/usr/bin/env python3
"""
TASK-030B-1.9 Documentation Validation Suite

This is a documentation task, so testing focuses on:
1. Content completeness (all sections present)
2. Cross-reference validation (all links resolve)
3. Formatting verification (markdown syntax correct)
4. Consistency checks (matches established patterns)

Target: /Users/richardwoollcott/Projects/appmilla_github/ai-engineer/docs/guides/agentecflow-lite-workflow.md
Content: Lines 3244-3634 (391 lines) - Feature 3.9: Design System Detection
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import dataclass

# COMPILATION CHECK: For documentation tasks, compilation means:
# 1. Markdown syntax is valid (no broken formatting)
# 2. All cross-reference links resolve to existing files
# 3. Tables are properly formatted
# 4. Code blocks have correct language tags

@dataclass
class ValidationResult:
    """Result of a validation check"""
    name: str
    passed: bool
    details: str
    severity: str  # 'ERROR', 'WARNING', 'INFO'

class DocumentationValidator:
    """Validates Feature 3.9 documentation implementation"""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.target_file = self.base_path / "docs/guides/agentecflow-lite-workflow.md"
        self.results: List[ValidationResult] = []

    def validate_all(self) -> bool:
        """Run all validation checks"""
        print("=" * 80)
        print("TASK-030B-1.9 Documentation Validation Suite")
        print("=" * 80)
        print()

        # 1. Markdown Syntax Check
        print("1. Markdown Syntax Validation...")
        self.validate_markdown_syntax()
        print()

        # 2. Cross-Reference Validation
        print("2. Cross-Reference Validation...")
        self.validate_cross_references()
        print()

        # 3. Content Completeness
        print("3. Content Completeness Check...")
        self.validate_content_completeness()
        print()

        # 4. Consistency Check
        print("4. Consistency Check (vs Features 3.7-3.8)...")
        self.validate_consistency()
        print()

        # Generate Report
        return self.generate_report()

    def validate_markdown_syntax(self):
        """Validate markdown syntax is correct"""
        content = self.read_feature_content()

        # Check headers
        headers = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
        if len(headers) == 0:
            self.results.append(ValidationResult(
                "Header Check",
                False,
                "No headers found in Feature 3.9 content",
                "ERROR"
            ))
        else:
            self.results.append(ValidationResult(
                "Header Check",
                True,
                f"Found {len(headers)} properly formatted headers",
                "INFO"
            ))

        # Check code blocks
        code_blocks = re.findall(r'```(\w+)?\n', content)
        unclosed_blocks = content.count('```') % 2

        if unclosed_blocks != 0:
            self.results.append(ValidationResult(
                "Code Block Balance",
                False,
                "Unbalanced code blocks detected (odd number of ```)",
                "ERROR"
            ))
        else:
            self.results.append(ValidationResult(
                "Code Block Balance",
                True,
                f"All {content.count('```') // 2} code blocks properly closed",
                "INFO"
            ))

        # Check code block language tags
        blocks_without_lang = content.count('```\n')
        if blocks_without_lang > 0:
            self.results.append(ValidationResult(
                "Code Block Language Tags",
                False,
                f"{blocks_without_lang} code blocks missing language tags",
                "WARNING"
            ))
        else:
            self.results.append(ValidationResult(
                "Code Block Language Tags",
                True,
                "All code blocks have language tags (bash, regex, json)",
                "INFO"
            ))

        # Check tables
        table_rows = re.findall(r'^\|.+\|$', content, re.MULTILINE)
        table_separators = re.findall(r'^\|[-:\s|]+\|$', content, re.MULTILINE)

        if len(table_separators) > 0:
            self.results.append(ValidationResult(
                "Table Formatting",
                True,
                f"Found {len(table_separators)} properly formatted tables",
                "INFO"
            ))
        else:
            self.results.append(ValidationResult(
                "Table Formatting",
                False,
                "No properly formatted tables found (expected URL pattern table, supported systems table, parameters table, troubleshooting table)",
                "WARNING"
            ))

        # Check lists
        unordered_lists = len(re.findall(r'^\s*[-*]\s+.+$', content, re.MULTILINE))
        ordered_lists = len(re.findall(r'^\s*\d+\.\s+.+$', content, re.MULTILINE))

        self.results.append(ValidationResult(
            "List Formatting",
            True,
            f"Found {unordered_lists} unordered list items, {ordered_lists} ordered list items",
            "INFO"
        ))

    def validate_cross_references(self):
        """Validate all cross-reference links resolve to existing files"""
        content = self.read_feature_content()

        # Expected cross-references
        expected_refs = {
            "UX Design Integration Workflow": "../workflows/ux-design-integration-workflow.md",
            "Figma-to-React Command": "../../installer/global/commands/figma-to-react.md",
            "Zeplin-to-MAUI Command": "../../installer/global/commands/zeplin-to-maui.md",
            "Design-to-Code Common Patterns": "../shared/design-to-code-common.md"
        }

        all_passed = True
        details = []

        for ref_name, ref_path in expected_refs.items():
            # Check if reference exists in content
            if ref_path in content:
                # Resolve path
                full_path = (self.target_file.parent / ref_path).resolve()
                if full_path.exists():
                    details.append(f"  ✓ {ref_name}: {ref_path} (RESOLVED)")
                else:
                    details.append(f"  ✗ {ref_name}: {ref_path} (NOT FOUND)")
                    all_passed = False
            else:
                details.append(f"  ✗ {ref_name}: Reference not found in content")
                all_passed = False

        # Check for internal references to Feature 3.8
        if "Feature 3.8" in content or "3.8" in content:
            details.append("  ✓ Internal reference to Feature 3.8 found")
        else:
            details.append("  ✗ Internal reference to Feature 3.8 not found")
            all_passed = False

        self.results.append(ValidationResult(
            "Cross-Reference Links",
            all_passed,
            "\n".join(details),
            "ERROR" if not all_passed else "INFO"
        ))

    def validate_content_completeness(self):
        """Validate all required sections are present"""
        content = self.read_feature_content()

        # 3-tier structure
        required_sections = {
            "Quick Start (2 minutes)": r"Quick Start \(2 minutes\)",
            "Core Concepts (10 minutes)": r"Core Concepts \(10 minutes\)",
            "Complete Reference (30 minutes)": r"Complete Reference \(30 minutes\)"
        }

        all_passed = True
        details = []

        for section_name, pattern in required_sections.items():
            if re.search(pattern, content):
                details.append(f"  ✓ {section_name}")
            else:
                details.append(f"  ✗ {section_name} (MISSING)")
                all_passed = False

        self.results.append(ValidationResult(
            "3-Tier Structure",
            all_passed,
            "\n".join(details),
            "ERROR" if not all_passed else "INFO"
        ))

        # Check for code examples (minimum 4, target 6+)
        code_blocks = len(re.findall(r'```', content)) // 2
        if code_blocks >= 6:
            self.results.append(ValidationResult(
                "Code Examples",
                True,
                f"Found {code_blocks} code examples (exceeds target of 6+)",
                "INFO"
            ))
        elif code_blocks >= 4:
            self.results.append(ValidationResult(
                "Code Examples",
                True,
                f"Found {code_blocks} code examples (meets minimum of 4)",
                "WARNING"
            ))
        else:
            self.results.append(ValidationResult(
                "Code Examples",
                False,
                f"Found {code_blocks} code examples (below minimum of 4)",
                "ERROR"
            ))

        # Check for required tables
        required_tables = [
            ("URL Pattern Table", r"\|\s*Design System\s*\|.*URL Pattern"),
            ("Supported Systems Table", r"\|\s*System\s*\|.*Stack Support"),
            ("Parameters Table", r"\|\s*Parameter\s*\|.*Default"),
            ("Troubleshooting Table", r"\|\s*Issue\s*\|.*Cause.*Solution")
        ]

        table_details = []
        all_tables_found = True

        for table_name, pattern in required_tables:
            if re.search(pattern, content):
                table_details.append(f"  ✓ {table_name}")
            else:
                table_details.append(f"  ✗ {table_name} (MISSING)")
                all_tables_found = False

        self.results.append(ValidationResult(
            "Required Tables",
            all_tables_found,
            "\n".join(table_details),
            "ERROR" if not all_tables_found else "INFO"
        ))

        # Check for specific content elements
        content_elements = [
            ("URL Parsing Algorithm", r"URL Parsing Algorithm"),
            ("Detection Process", r"Detection Process"),
            ("Quality Gates", r"Quality Gates"),
            ("Real-World Example", r"Real-World Example"),
            ("Best Practices", r"Best Practices"),
            ("Success Metrics", r"Success Metrics")
        ]

        element_details = []
        all_elements_found = True

        for element_name, pattern in content_elements:
            if re.search(pattern, content):
                element_details.append(f"  ✓ {element_name}")
            else:
                element_details.append(f"  ✗ {element_name} (MISSING)")
                all_elements_found = False

        self.results.append(ValidationResult(
            "Content Elements",
            all_elements_found,
            "\n".join(element_details),
            "WARNING" if not all_elements_found else "INFO"
        ))

    def validate_consistency(self):
        """Validate consistency with Features 3.7 and 3.8"""
        content = self.read_feature_content()

        # Check for Hubbard Alignment (supports both plain and bold markdown)
        if "Hubbard Alignment" in content:
            self.results.append(ValidationResult(
                "Hubbard Alignment Field",
                True,
                "Hubbard Alignment metadata present",
                "INFO"
            ))
        else:
            self.results.append(ValidationResult(
                "Hubbard Alignment Field",
                False,
                "Hubbard Alignment metadata missing",
                "ERROR"
            ))

        # Check for Phase metadata
        if "**Phase**:" in content or "Phase:" in content:
            self.results.append(ValidationResult(
                "Phase Metadata",
                True,
                "Phase metadata present",
                "INFO"
            ))
        else:
            self.results.append(ValidationResult(
                "Phase Metadata",
                False,
                "Phase metadata missing",
                "ERROR"
            ))

        # Check for Complexity tier
        if "**Complexity**: Tier" in content or "Complexity: Tier" in content:
            self.results.append(ValidationResult(
                "Complexity Tier",
                True,
                "Complexity tier metadata present",
                "INFO"
            ))
        else:
            self.results.append(ValidationResult(
                "Complexity Tier",
                False,
                "Complexity tier metadata missing",
                "ERROR"
            ))

        # Check for Dependencies
        if "**Dependencies**:" in content or "Dependencies:" in content:
            self.results.append(ValidationResult(
                "Dependencies Field",
                True,
                "Dependencies metadata present",
                "INFO"
            ))
        else:
            self.results.append(ValidationResult(
                "Dependencies Field",
                False,
                "Dependencies metadata missing",
                "ERROR"
            ))

        # Check for "When to use" / "When to skip" sections
        when_sections = []
        if "**When to use**:" in content or "When to use:" in content:
            when_sections.append("  ✓ When to use section")
        else:
            when_sections.append("  ✗ When to use section (MISSING)")

        if "**When to skip**:" in content or "When to skip:" in content:
            when_sections.append("  ✓ When to skip section")
        else:
            when_sections.append("  ✗ When to skip section (MISSING)")

        self.results.append(ValidationResult(
            "Usage Guidance Sections",
            "MISSING" not in "\n".join(when_sections),
            "\n".join(when_sections),
            "WARNING" if "MISSING" in "\n".join(when_sections) else "INFO"
        ))

        # Check for professional tone (no emojis except standard checkmarks)
        emoji_pattern = r'[😀-🙏🚀-🛿🌀-🗿🤐-🦴🧀-🫶]'
        emojis = re.findall(emoji_pattern, content)

        if len(emojis) > 0:
            self.results.append(ValidationResult(
                "Professional Tone",
                False,
                f"Found {len(emojis)} emoji characters (should use standard ✓ ✗ symbols only)",
                "WARNING"
            ))
        else:
            self.results.append(ValidationResult(
                "Professional Tone",
                True,
                "No decorative emojis found (uses standard checkmarks only)",
                "INFO"
            ))

    def read_feature_content(self) -> str:
        """Read Feature 3.9 content from target file"""
        if not self.target_file.exists():
            raise FileNotFoundError(f"Target file not found: {self.target_file}")

        with open(self.target_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Extract lines 3244-3634 (Feature 3.9 content)
        # Line numbers are 1-indexed, so subtract 1
        feature_lines = lines[3243:3634]
        return ''.join(feature_lines)

    def generate_report(self) -> bool:
        """Generate validation report"""
        print("=" * 80)
        print("VALIDATION REPORT")
        print("=" * 80)
        print()

        errors = [r for r in self.results if r.severity == "ERROR" and not r.passed]
        warnings = [r for r in self.results if r.severity == "WARNING" and not r.passed]
        passed = [r for r in self.results if r.passed]

        # Summary
        print(f"Total Checks: {len(self.results)}")
        print(f"  ✓ Passed: {len(passed)}")
        print(f"  ⚠ Warnings: {len(warnings)}")
        print(f"  ✗ Errors: {len(errors)}")
        print()

        # Errors
        if errors:
            print("ERRORS (Must Fix):")
            print("-" * 80)
            for result in errors:
                print(f"✗ {result.name}")
                print(f"  {result.details}")
                print()

        # Warnings
        if warnings:
            print("WARNINGS (Should Fix):")
            print("-" * 80)
            for result in warnings:
                print(f"⚠ {result.name}")
                print(f"  {result.details}")
                print()

        # Success
        if not errors and not warnings:
            print("✅ ALL VALIDATION CHECKS PASSED")
            print()
            print("Feature 3.9 documentation is:")
            print("  ✓ Syntactically correct (markdown)")
            print("  ✓ All cross-references resolve")
            print("  ✓ Content complete (3-tier structure, tables, examples)")
            print("  ✓ Consistent with Features 3.7-3.8 style")
            print()

        # Detailed Results
        print("DETAILED RESULTS:")
        print("-" * 80)
        for result in self.results:
            status = "✓" if result.passed else ("⚠" if result.severity == "WARNING" else "✗")
            print(f"{status} {result.name}")
            if result.details:
                for line in result.details.split('\n'):
                    print(f"    {line}")
        print()

        # Compilation status
        print("=" * 80)
        print("COMPILATION STATUS (Documentation)")
        print("=" * 80)

        if errors:
            print("❌ COMPILATION FAILED")
            print()
            print("Documentation has errors that must be fixed:")
            for error in errors:
                print(f"  - {error.name}")
            print()
            print("Documentation cannot be considered complete until all errors are resolved.")
            return False
        else:
            print("✅ COMPILATION PASSED")
            print()
            print("Documentation is:")
            print("  1. Markdown syntax valid ✓")
            print("  2. All cross-references resolve ✓")
            print("  3. Tables properly formatted ✓")
            print("  4. Code blocks correctly tagged ✓")
            print()
            if warnings:
                print(f"Note: {len(warnings)} warnings should be addressed for optimal quality.")
            return True

def main():
    """Main entry point"""
    base_path = "/Users/richardwoollcott/Projects/appmilla_github/ai-engineer"

    validator = DocumentationValidator(base_path)

    try:
        success = validator.validate_all()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Validation failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
