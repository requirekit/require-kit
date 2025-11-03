#!/usr/bin/env python3
"""
Documentation Validation Suite for TASK-036
Validates markdown syntax, badge URLs, content presence, and consistency
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Tuple
from urllib.parse import urlparse, parse_qs

class DocumentationValidator:
    def __init__(self):
        self.results = {
            "markdown_syntax": {"passed": 0, "failed": 0, "details": []},
            "badge_urls": {"passed": 0, "failed": 0, "details": []},
            "content_validation": {"passed": 0, "failed": 0, "details": []},
            "consistency": {"passed": 0, "failed": 0, "details": []}
        }

        # Expected badge configuration from TASK-036 spec
        self.expected_badges = {
            "version": {
                "label": "version",
                "message": "1.0.0",
                "color": "0366d6"
            },
            "license": {
                "label": "license",
                "message": "MIT",
                "color": "28a745"
            },
            "standalone": {
                "label": "standalone",
                "message": "no dependencies",
                "color": "6f42c1"
            },
            "integration": {
                "label": "integration",
                "message": "taskwright optional",
                "color": "ffd33d"
            },
            "detection": {
                "label": "detection",
                "message": "automatic",
                "color": "6f42c1"
            }
        }

    def validate_markdown_syntax(self, file_path: str) -> bool:
        """Validate markdown syntax in file"""
        try:
            content = Path(file_path).read_text()
            issues = []

            # Check for malformed headers
            header_pattern = r'^#{1,6}\s+.+$'
            for line_num, line in enumerate(content.split('\n'), 1):
                if line.strip().startswith('#') and not re.match(header_pattern, line.strip()):
                    issues.append(f"Line {line_num}: Malformed header - '{line.strip()}'")

            # Check for malformed links
            link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
            links = re.finditer(link_pattern, content)
            for match in links:
                link_text = match.group(1)
                link_url = match.group(2)
                if not link_text or not link_url:
                    issues.append(f"Malformed link: [{link_text}]({link_url})")

            # Check for unclosed code blocks
            code_blocks = re.findall(r'```', content)
            if len(code_blocks) % 2 != 0:
                issues.append("Unclosed code block detected")

            if issues:
                self.results["markdown_syntax"]["failed"] += 1
                self.results["markdown_syntax"]["details"].append({
                    "file": file_path,
                    "status": "FAILED",
                    "issues": issues
                })
                return False
            else:
                self.results["markdown_syntax"]["passed"] += 1
                self.results["markdown_syntax"]["details"].append({
                    "file": file_path,
                    "status": "PASSED",
                    "issues": []
                })
                return True

        except Exception as e:
            self.results["markdown_syntax"]["failed"] += 1
            self.results["markdown_syntax"]["details"].append({
                "file": file_path,
                "status": "ERROR",
                "issues": [str(e)]
            })
            return False

    def validate_badge_url(self, badge_line: str, expected_config: Dict) -> Tuple[bool, List[str]]:
        """Validate a single badge URL structure"""
        issues = []

        # Extract badge URL from markdown
        match = re.search(r'\((https://img\.shields\.io/badge/[^)]+)\)', badge_line)
        if not match:
            issues.append("Badge URL not found or malformed")
            return False, issues

        url = match.group(1)

        # Parse URL components
        if not url.startswith("https://img.shields.io/badge/"):
            issues.append(f"Invalid badge URL base: {url}")
            return False, issues

        # Extract badge parts
        badge_parts = url.replace("https://img.shields.io/badge/", "").split("-")
        if len(badge_parts) < 3:
            issues.append(f"Invalid badge format (expected label-message-color): {url}")
            return False, issues

        # Validate label
        label = badge_parts[0]
        expected_label = expected_config["label"]
        if label != expected_label:
            issues.append(f"Label mismatch: expected '{expected_label}', got '{label}'")

        # Validate color (last component)
        color = badge_parts[-1]
        expected_color = expected_config["color"]
        if color != expected_color:
            issues.append(f"Color mismatch: expected '{expected_color}', got '{color}'")

        # Validate message (everything between label and color)
        message = "-".join(badge_parts[1:-1])
        # Handle URL encoding (spaces as %20 or -)
        expected_message = expected_config["message"].replace(" ", "%20")
        if message not in [expected_message, expected_config["message"].replace(" ", "-")]:
            issues.append(f"Message mismatch: expected '{expected_config['message']}', got '{message}'")

        return len(issues) == 0, issues

    def validate_badge_urls(self, file_path: str) -> bool:
        """Validate all badge URLs in file"""
        try:
            content = Path(file_path).read_text()
            all_passed = True

            # Extract badge lines
            badge_lines = []
            for line in content.split('\n'):
                if 'img.shields.io/badge/' in line:
                    badge_lines.append(line)

            if not badge_lines:
                self.results["badge_urls"]["failed"] += 1
                self.results["badge_urls"]["details"].append({
                    "file": file_path,
                    "status": "FAILED",
                    "reason": "No badges found"
                })
                return False

            # Validate each badge type
            for badge_type, expected in self.expected_badges.items():
                found = False
                for line in badge_lines:
                    if expected["label"] in line.lower():
                        found = True
                        is_valid, issues = self.validate_badge_url(line, expected)
                        if is_valid:
                            self.results["badge_urls"]["passed"] += 1
                            self.results["badge_urls"]["details"].append({
                                "file": file_path,
                                "badge": badge_type,
                                "status": "PASSED"
                            })
                        else:
                            all_passed = False
                            self.results["badge_urls"]["failed"] += 1
                            self.results["badge_urls"]["details"].append({
                                "file": file_path,
                                "badge": badge_type,
                                "status": "FAILED",
                                "issues": issues
                            })
                        break

                if not found:
                    all_passed = False
                    self.results["badge_urls"]["failed"] += 1
                    self.results["badge_urls"]["details"].append({
                        "file": file_path,
                        "badge": badge_type,
                        "status": "MISSING"
                    })

            return all_passed

        except Exception as e:
            self.results["badge_urls"]["failed"] += 1
            self.results["badge_urls"]["details"].append({
                "file": file_path,
                "status": "ERROR",
                "reason": str(e)
            })
            return False

    def validate_content(self, file_path: str) -> bool:
        """Validate required content is present"""
        try:
            content = Path(file_path).read_text()
            all_passed = True

            # Check for Package Status section (README only)
            if "README.md" in file_path:
                if "## Package Status" in content:
                    self.results["content_validation"]["passed"] += 1
                    self.results["content_validation"]["details"].append({
                        "file": file_path,
                        "check": "Package Status section",
                        "status": "PASSED"
                    })
                else:
                    all_passed = False
                    self.results["content_validation"]["failed"] += 1
                    self.results["content_validation"]["details"].append({
                        "file": file_path,
                        "check": "Package Status section",
                        "status": "FAILED",
                        "reason": "Section not found"
                    })

            # Check for outdated references
            outdated_terms = ["ai-engineer", "monolithic", "single package"]
            found_outdated = []
            for term in outdated_terms:
                if term.lower() in content.lower():
                    found_outdated.append(term)

            if found_outdated:
                all_passed = False
                self.results["content_validation"]["failed"] += 1
                self.results["content_validation"]["details"].append({
                    "file": file_path,
                    "check": "No outdated references",
                    "status": "FAILED",
                    "outdated_terms": found_outdated
                })
            else:
                self.results["content_validation"]["passed"] += 1
                self.results["content_validation"]["details"].append({
                    "file": file_path,
                    "check": "No outdated references",
                    "status": "PASSED"
                })

            # Verify badge placement (top of README after title)
            if "README.md" in file_path:
                lines = content.split('\n')
                title_line = -1
                first_badge_line = -1

                for i, line in enumerate(lines):
                    if line.startswith('# ') and title_line == -1:
                        title_line = i
                    if 'img.shields.io/badge/' in line and first_badge_line == -1:
                        first_badge_line = i
                        break

                if title_line >= 0 and first_badge_line >= 0:
                    if first_badge_line == title_line + 2:  # Title, blank line, badges
                        self.results["content_validation"]["passed"] += 1
                        self.results["content_validation"]["details"].append({
                            "file": file_path,
                            "check": "Badge placement",
                            "status": "PASSED"
                        })
                    else:
                        all_passed = False
                        self.results["content_validation"]["failed"] += 1
                        self.results["content_validation"]["details"].append({
                            "file": file_path,
                            "check": "Badge placement",
                            "status": "FAILED",
                            "reason": f"Badges should be at line {title_line + 2}, found at line {first_badge_line}"
                        })

            return all_passed

        except Exception as e:
            self.results["content_validation"]["failed"] += 1
            self.results["content_validation"]["details"].append({
                "file": file_path,
                "status": "ERROR",
                "reason": str(e)
            })
            return False

    def validate_consistency(self, readme_path: str, claude_path: str) -> bool:
        """Validate consistency between README.md and CLAUDE.md"""
        try:
            readme_content = Path(readme_path).read_text()
            claude_content = Path(claude_path).read_text()
            all_passed = True

            # Extract badges from both files
            readme_badges = re.findall(r'img\.shields\.io/badge/([^)]+)', readme_content)
            claude_badges = re.findall(r'img\.shields\.io/badge/([^)]+)', claude_content)

            # Check if CLAUDE.md has Package Status section
            if "## Package Status" in claude_content:
                self.results["consistency"]["passed"] += 1
                self.results["consistency"]["details"].append({
                    "check": "Package Status in CLAUDE.md",
                    "status": "PASSED"
                })
            else:
                all_passed = False
                self.results["consistency"]["failed"] += 1
                self.results["consistency"]["details"].append({
                    "check": "Package Status in CLAUDE.md",
                    "status": "FAILED",
                    "reason": "Section not found"
                })

            # Check for consistent messaging about standalone/optional integration
            key_phrases = [
                "standalone requirements management toolkit",
                "no dependencies",
                "optional integration",
                "taskwright optional"
            ]

            for phrase in key_phrases:
                in_readme = phrase.lower() in readme_content.lower()
                in_claude = phrase.lower() in claude_content.lower()

                if in_readme and in_claude:
                    self.results["consistency"]["passed"] += 1
                    self.results["consistency"]["details"].append({
                        "check": f"Consistent messaging: '{phrase}'",
                        "status": "PASSED"
                    })
                elif in_readme and not in_claude:
                    all_passed = False
                    self.results["consistency"]["failed"] += 1
                    self.results["consistency"]["details"].append({
                        "check": f"Consistent messaging: '{phrase}'",
                        "status": "FAILED",
                        "reason": "Present in README.md but missing in CLAUDE.md"
                    })
                elif not in_readme and in_claude:
                    all_passed = False
                    self.results["consistency"]["failed"] += 1
                    self.results["consistency"]["details"].append({
                        "check": f"Consistent messaging: '{phrase}'",
                        "status": "FAILED",
                        "reason": "Present in CLAUDE.md but missing in README.md"
                    })

            return all_passed

        except Exception as e:
            self.results["consistency"]["failed"] += 1
            self.results["consistency"]["details"].append({
                "status": "ERROR",
                "reason": str(e)
            })
            return False

    def run_full_validation(self):
        """Run complete validation suite"""
        print("=" * 80)
        print("DOCUMENTATION VALIDATION SUITE - TASK-036")
        print("=" * 80)
        print()

        readme_path = "/Users/richardwoollcott/Projects/appmilla_github/require-kit/README.md"
        claude_path = "/Users/richardwoollcott/Projects/appmilla_github/require-kit/CLAUDE.md"

        # Phase 1: Markdown Syntax Validation (MUST pass before proceeding)
        print("Phase 1: Markdown Syntax Validation")
        print("-" * 80)
        readme_syntax_ok = self.validate_markdown_syntax(readme_path)
        claude_syntax_ok = self.validate_markdown_syntax(claude_path)

        if not (readme_syntax_ok and claude_syntax_ok):
            print("❌ CRITICAL: Markdown syntax validation FAILED")
            print("Cannot proceed to other validations until syntax is fixed.")
            self.print_results()
            return False

        print("✅ Markdown syntax validation PASSED")
        print()

        # Phase 2: Badge URL Validation
        print("Phase 2: Badge URL Validation")
        print("-" * 80)
        readme_badges_ok = self.validate_badge_urls(readme_path)
        print(f"README.md badges: {'✅ PASSED' if readme_badges_ok else '❌ FAILED'}")
        print()

        # Phase 3: Content Validation
        print("Phase 3: Content Validation")
        print("-" * 80)
        readme_content_ok = self.validate_content(readme_path)
        claude_content_ok = self.validate_content(claude_path)
        print(f"README.md content: {'✅ PASSED' if readme_content_ok else '❌ FAILED'}")
        print(f"CLAUDE.md content: {'✅ PASSED' if claude_content_ok else '❌ FAILED'}")
        print()

        # Phase 4: Consistency Validation
        print("Phase 4: Consistency Validation")
        print("-" * 80)
        consistency_ok = self.validate_consistency(readme_path, claude_path)
        print(f"Cross-file consistency: {'✅ PASSED' if consistency_ok else '❌ FAILED'}")
        print()

        # Print detailed results
        self.print_results()

        # Return overall status
        all_passed = (readme_syntax_ok and claude_syntax_ok and
                     readme_badges_ok and readme_content_ok and
                     claude_content_ok and consistency_ok)

        return all_passed

    def print_results(self):
        """Print detailed validation results"""
        print()
        print("=" * 80)
        print("DETAILED VALIDATION RESULTS")
        print("=" * 80)
        print()

        for category, data in self.results.items():
            total = data["passed"] + data["failed"]
            pass_rate = (data["passed"] / total * 100) if total > 0 else 0

            print(f"{category.upper().replace('_', ' ')}")
            print(f"  Passed: {data['passed']}/{total} ({pass_rate:.1f}%)")
            print(f"  Failed: {data['failed']}/{total}")
            print()

            if data["failed"] > 0:
                print("  Failures:")
                for detail in data["details"]:
                    if detail.get("status") in ["FAILED", "MISSING", "ERROR"]:
                        print(f"    - {json.dumps(detail, indent=6)}")
                print()

        print("=" * 80)
        print("SUMMARY")
        print("=" * 80)
        total_passed = sum(cat["passed"] for cat in self.results.values())
        total_failed = sum(cat["failed"] for cat in self.results.values())
        total_checks = total_passed + total_failed
        overall_pass_rate = (total_passed / total_checks * 100) if total_checks > 0 else 0

        print(f"Total Checks: {total_checks}")
        print(f"Passed: {total_passed} ✅")
        print(f"Failed: {total_failed} ❌")
        print(f"Pass Rate: {overall_pass_rate:.1f}%")
        print()

        if overall_pass_rate == 100:
            print("🎉 ALL VALIDATIONS PASSED - TASK-036 READY FOR COMPLETION")
        else:
            print("⚠️  VALIDATIONS FAILED - FIXES REQUIRED BEFORE TASK COMPLETION")
        print()

    def get_minimal_output(self) -> Dict:
        """Generate minimal mode output for embedding"""
        total_passed = sum(cat["passed"] for cat in self.results.values())
        total_failed = sum(cat["failed"] for cat in self.results.values())
        total_checks = total_passed + total_failed

        return {
            "phase": "4.5",
            "status": "passed" if total_failed == 0 else "failed",
            "validation_type": "documentation",
            "final_result": {
                "total_checks": total_checks,
                "passed": total_passed,
                "failed": total_failed,
                "pass_rate": f"{(total_passed / total_checks * 100) if total_checks > 0 else 0:.1f}%"
            },
            "quality_gates": {
                "markdown_syntax": "passed" if self.results["markdown_syntax"]["failed"] == 0 else "failed",
                "badge_urls": "passed" if self.results["badge_urls"]["failed"] == 0 else "failed",
                "content_validation": "passed" if self.results["content_validation"]["failed"] == 0 else "failed",
                "consistency": "passed" if self.results["consistency"]["failed"] == 0 else "failed"
            },
            "fix_summary": "Documentation validation complete" if total_failed == 0 else f"{total_failed} validation issues detected"
        }


if __name__ == "__main__":
    validator = DocumentationValidator()
    success = validator.run_full_validation()

    # Output minimal format JSON
    print()
    print("=" * 80)
    print("MINIMAL OUTPUT (for embedding)")
    print("=" * 80)
    print(json.dumps(validator.get_minimal_output(), indent=2))

    # Exit with appropriate code
    exit(0 if success else 1)
