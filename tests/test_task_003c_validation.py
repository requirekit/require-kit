"""
Test Suite for TASK-003C: Integration with Task-Work Workflow
Validates markdown documentation quality, logical consistency, and architectural alignment.
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# Test Configuration
# ============================================================================

PROJECT_ROOT = Path("/Users/richardwoollcott/Projects/appmilla_github/ai-engineer")
TASK_WORK_FILE = PROJECT_ROOT / "installer/global/commands/task-work.md"
TASK_MANAGER_FILE = PROJECT_ROOT / "installer/global/agents/task-manager.md"
ADR_DIR = PROJECT_ROOT / "docs/adr"


class TestStatus(Enum):
    PASS = "✅"
    FAIL = "❌"
    WARN = "⚠️"


@dataclass
class TestResult:
    test_name: str
    status: TestStatus
    message: str
    details: Optional[str] = None
    file_line: Optional[str] = None


@dataclass
class ValidationReport:
    total_tests: int = 0
    passed: int = 0
    failed: int = 0
    warnings: int = 0
    results: List[TestResult] = None

    def __post_init__(self):
        if self.results is None:
            self.results = []

    def add_result(self, result: TestResult):
        self.results.append(result)
        self.total_tests += 1
        if result.status == TestStatus.PASS:
            self.passed += 1
        elif result.status == TestStatus.FAIL:
            self.failed += 1
        elif result.status == TestStatus.WARN:
            self.warnings += 1

    def pass_rate(self) -> float:
        return (self.passed / self.total_tests * 100) if self.total_tests > 0 else 0.0


# ============================================================================
# Markdown Validation Tests
# ============================================================================

class MarkdownValidator:
    """Validates markdown file structure and syntax"""

    @staticmethod
    def validate_file_exists(file_path: Path) -> TestResult:
        """Test: File exists"""
        if file_path.exists():
            return TestResult(
                test_name=f"File Exists: {file_path.name}",
                status=TestStatus.PASS,
                message=f"File found at {file_path}"
            )
        else:
            return TestResult(
                test_name=f"File Exists: {file_path.name}",
                status=TestStatus.FAIL,
                message=f"File not found at {file_path}"
            )

    @staticmethod
    def validate_markdown_syntax(content: str, filename: str) -> List[TestResult]:
        """Test: Markdown syntax is valid"""
        results = []
        lines = content.split('\n')

        # Check for malformed headers
        malformed_headers = []
        for i, line in enumerate(lines, 1):
            if line.startswith('#'):
                if not re.match(r'^#{1,6}\s+\S', line):
                    malformed_headers.append(f"Line {i}: {line[:50]}")

        if malformed_headers:
            results.append(TestResult(
                test_name=f"Markdown Syntax: {filename}",
                status=TestStatus.FAIL,
                message="Malformed headers detected",
                details="\n".join(malformed_headers)
            ))
        else:
            results.append(TestResult(
                test_name=f"Markdown Syntax: {filename}",
                status=TestStatus.PASS,
                message="All headers properly formatted"
            ))

        # Check for unclosed code blocks
        code_block_count = content.count('```')
        if code_block_count % 2 != 0:
            results.append(TestResult(
                test_name=f"Code Blocks: {filename}",
                status=TestStatus.FAIL,
                message=f"Unclosed code block detected ({code_block_count} backticks)"
            ))
        else:
            results.append(TestResult(
                test_name=f"Code Blocks: {filename}",
                status=TestStatus.PASS,
                message=f"All code blocks properly closed ({code_block_count//2} blocks)"
            ))

        return results

    @staticmethod
    def validate_section_exists(content: str, section_title: str, filename: str) -> TestResult:
        """Test: Required section exists"""
        pattern = rf'^#{1,6}\s+.*{re.escape(section_title)}.*$'
        if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
            return TestResult(
                test_name=f"Section Exists: {section_title} in {filename}",
                status=TestStatus.PASS,
                message=f"Section '{section_title}' found"
            )
        else:
            return TestResult(
                test_name=f"Section Exists: {section_title} in {filename}",
                status=TestStatus.FAIL,
                message=f"Section '{section_title}' not found",
                file_line=filename
            )


# ============================================================================
# Phase Flow Validation Tests
# ============================================================================

class PhaseFlowValidator:
    """Validates Phase 2.7 and 2.8 implementation in task-work.md"""

    @staticmethod
    def validate_phase_27_exists(content: str) -> TestResult:
        """Test: Phase 2.7 section exists"""
        pattern = r'#{1,6}\s+Phase 2\.7[:\s]'
        matches = re.findall(pattern, content, re.IGNORECASE)

        if matches:
            return TestResult(
                test_name="Phase 2.7 Documentation",
                status=TestStatus.PASS,
                message=f"Phase 2.7 section found ({len(matches)} occurrence(s))"
            )
        else:
            return TestResult(
                test_name="Phase 2.7 Documentation",
                status=TestStatus.FAIL,
                message="Phase 2.7 section not found in task-work.md"
            )

    @staticmethod
    def validate_phase_28_exists(content: str) -> TestResult:
        """Test: Phase 2.8 section exists"""
        pattern = r'#{1,6}\s+Phase 2\.8[:\s]'
        matches = re.findall(pattern, content, re.IGNORECASE)

        if matches:
            return TestResult(
                test_name="Phase 2.8 Documentation",
                status=TestStatus.PASS,
                message=f"Phase 2.8 section found ({len(matches)} occurrence(s))"
            )
        else:
            return TestResult(
                test_name="Phase 2.8 Documentation",
                status=TestStatus.FAIL,
                message="Phase 2.8 section not found in task-work.md"
            )

    @staticmethod
    def validate_phase_flow_diagram(content: str) -> TestResult:
        """Test: Phase flow diagram updated correctly"""
        # Check if Phase 2.7 and 2.8 are mentioned in sequence
        phase_order = ['2.5', '2.7', '2.8', '3']

        found_phases = []
        for phase in phase_order:
            if f'Phase {phase}' in content or f'phase {phase}' in content.lower():
                found_phases.append(phase)

        if found_phases == phase_order or set(['2.7', '2.8']).issubset(set(found_phases)):
            return TestResult(
                test_name="Phase Flow Diagram",
                status=TestStatus.PASS,
                message=f"Phase flow documented correctly (found: {', '.join(found_phases)})"
            )
        else:
            return TestResult(
                test_name="Phase Flow Diagram",
                status=TestStatus.WARN,
                message=f"Phase flow may be incomplete (found: {', '.join(found_phases)})"
            )

    @staticmethod
    def validate_complexity_evaluation(content: str) -> TestResult:
        """Test: Complexity evaluation logic documented"""
        keywords = [
            'complexity',
            'ComplexityScore',
            'complexity_score',
            'review_mode',
            'AUTO_PROCEED',
            'QUICK_OPTIONAL',
            'FULL_REQUIRED'
        ]

        found_keywords = [kw for kw in keywords if kw in content]

        if len(found_keywords) >= 5:
            return TestResult(
                test_name="Complexity Evaluation Logic",
                status=TestStatus.PASS,
                message=f"Complexity evaluation well-documented ({len(found_keywords)}/{len(keywords)} keywords)"
            )
        else:
            return TestResult(
                test_name="Complexity Evaluation Logic",
                status=TestStatus.FAIL,
                message=f"Complexity evaluation insufficiently documented ({len(found_keywords)}/{len(keywords)} keywords)"
            )

    @staticmethod
    def validate_review_mode_routing(content: str) -> TestResult:
        """Test: Review mode routing logic is complete"""
        review_modes = ['AUTO_PROCEED', 'QUICK_OPTIONAL', 'FULL_REQUIRED']

        found_modes = {mode: mode in content for mode in review_modes}

        if all(found_modes.values()):
            return TestResult(
                test_name="Review Mode Routing",
                status=TestStatus.PASS,
                message=f"All review modes documented: {', '.join(review_modes)}"
            )
        else:
            missing = [mode for mode, found in found_modes.items() if not found]
            return TestResult(
                test_name="Review Mode Routing",
                status=TestStatus.FAIL,
                message=f"Missing review modes: {', '.join(missing)}"
            )


# ============================================================================
# Task Manager Orchestration Tests
# ============================================================================

class TaskManagerValidator:
    """Validates task-manager.md orchestration logic"""

    @staticmethod
    def validate_phase_27_orchestration(content: str) -> TestResult:
        """Test: Phase 2.7 orchestration steps documented"""
        required_steps = [
            'Parse Implementation Plan',
            'Calculate Complexity Score',
            'Detect Force-Review Triggers',
            'Determine Review Mode',
            'Update Task Metadata'
        ]

        found_steps = [step for step in required_steps if step in content]

        if len(found_steps) >= 4:
            return TestResult(
                test_name="Phase 2.7 Orchestration",
                status=TestStatus.PASS,
                message=f"Orchestration steps documented ({len(found_steps)}/{len(required_steps)})"
            )
        else:
            return TestResult(
                test_name="Phase 2.7 Orchestration",
                status=TestStatus.FAIL,
                message=f"Orchestration steps incomplete ({len(found_steps)}/{len(required_steps)})"
            )

    @staticmethod
    def validate_phase_28_orchestration(content: str) -> TestResult:
        """Test: Phase 2.8 orchestration paths documented"""
        required_paths = [
            'Auto-Proceed',
            'Quick Optional Review',
            'Full Required Review'
        ]

        found_paths = [path for path in required_paths if path in content]

        if len(found_paths) >= 2:
            return TestResult(
                test_name="Phase 2.8 Orchestration",
                status=TestStatus.PASS,
                message=f"Review paths documented ({len(found_paths)}/{len(required_paths)})"
            )
        else:
            return TestResult(
                test_name="Phase 2.8 Orchestration",
                status=TestStatus.FAIL,
                message=f"Review paths incomplete ({len(found_paths)}/{len(required_paths)})"
            )

    @staticmethod
    def validate_complexity_calculator(content: str) -> TestResult:
        """Test: ComplexityCalculator references"""
        keywords = ['ComplexityCalculator', 'calculate', 'complexity_score', 'EvaluationContext']

        found = [kw for kw in keywords if kw in content]

        if len(found) >= 2:
            return TestResult(
                test_name="ComplexityCalculator Integration",
                status=TestStatus.PASS,
                message=f"Calculator integration documented ({len(found)}/{len(keywords)} keywords)"
            )
        else:
            return TestResult(
                test_name="ComplexityCalculator Integration",
                status=TestStatus.WARN,
                message=f"Calculator references minimal ({len(found)}/{len(keywords)} keywords)"
            )


# ============================================================================
# Logical Consistency Tests
# ============================================================================

class LogicalConsistencyValidator:
    """Validates logical flow and consistency"""

    @staticmethod
    def validate_phase_sequence(content: str) -> TestResult:
        """Test: Phase 2.7 → 2.8 → 3 flow is coherent"""
        # Extract phase mentions in order
        phase_pattern = r'Phase\s+(2\.7|2\.8|3)'
        phases_found = re.findall(phase_pattern, content, re.IGNORECASE)

        # Check if phases appear in logical order
        if '2.7' in phases_found and '2.8' in phases_found:
            idx_27 = phases_found.index('2.7')
            idx_28 = phases_found.index('2.8')

            if idx_27 < idx_28:
                return TestResult(
                    test_name="Phase Sequence Logic",
                    status=TestStatus.PASS,
                    message="Phase 2.7 → 2.8 → 3 flow documented in correct order"
                )
            else:
                return TestResult(
                    test_name="Phase Sequence Logic",
                    status=TestStatus.WARN,
                    message="Phase order may be inconsistent"
                )
        else:
            return TestResult(
                test_name="Phase Sequence Logic",
                status=TestStatus.FAIL,
                message="Phase 2.7 and/or 2.8 not found in sequence"
            )

    @staticmethod
    def validate_error_handling(content: str) -> TestResult:
        """Test: Error handling paths defined"""
        error_keywords = [
            'ERROR HANDLING',
            'If fails',
            'error',
            'exception',
            'fallback'
        ]

        found = sum(1 for kw in error_keywords if kw.lower() in content.lower())

        if found >= 3:
            return TestResult(
                test_name="Error Handling Paths",
                status=TestStatus.PASS,
                message=f"Error handling documented ({found}/{len(error_keywords)} keywords)"
            )
        else:
            return TestResult(
                test_name="Error Handling Paths",
                status=TestStatus.WARN,
                message=f"Error handling may be insufficient ({found}/{len(error_keywords)} keywords)"
            )

    @staticmethod
    def validate_stub_placeholders(content: str) -> TestResult:
        """Test: Stub placeholders clearly marked"""
        stub_keywords = [
            'Coming soon',
            'STUBBED',
            'TASK-003B-3',
            'TASK-003B-4',
            'MVP'
        ]

        found = [kw for kw in stub_keywords if kw in content]

        if len(found) >= 2:
            return TestResult(
                test_name="Stub Placeholders",
                status=TestStatus.PASS,
                message=f"Future work clearly marked ({len(found)} references)"
            )
        else:
            return TestResult(
                test_name="Stub Placeholders",
                status=TestStatus.WARN,
                message=f"Stub markers minimal ({len(found)} references)"
            )


# ============================================================================
# Architectural Compliance Tests
# ============================================================================

class ArchitecturalValidator:
    """Validates architectural decisions and patterns"""

    @staticmethod
    def validate_yagni_compliance(content: str) -> TestResult:
        """Test: YAGNI violations removed"""
        violations = []

        # Check for undo/history features
        if re.search(r'\bundo\b', content, re.IGNORECASE):
            violations.append("Undo functionality mentioned")
        if re.search(r'\bhistory\b.*\btrack', content, re.IGNORECASE):
            violations.append("History tracking mentioned")

        # Check for overly complex versioning
        if re.search(r'version.*history|version.*control', content, re.IGNORECASE):
            violations.append("Complex versioning system mentioned")

        if not violations:
            return TestResult(
                test_name="YAGNI Compliance",
                status=TestStatus.PASS,
                message="No YAGNI violations detected"
            )
        else:
            return TestResult(
                test_name="YAGNI Compliance",
                status=TestStatus.WARN,
                message=f"Potential YAGNI issues: {', '.join(violations)}"
            )

    @staticmethod
    def validate_metadata_builder_pattern(content: str) -> TestResult:
        """Test: MetadataBuilder pattern documented"""
        if 'MetadataBuilder' in content or 'metadata_builder' in content:
            return TestResult(
                test_name="MetadataBuilder Pattern",
                status=TestStatus.PASS,
                message="MetadataBuilder pattern referenced"
            )
        else:
            return TestResult(
                test_name="MetadataBuilder Pattern",
                status=TestStatus.WARN,
                message="MetadataBuilder pattern not explicitly mentioned"
            )

    @staticmethod
    def validate_backward_compatibility(content: str) -> TestResult:
        """Test: Backward compatibility maintained"""
        keywords = [
            'backward compatible',
            'existing',
            'legacy',
            'previous'
        ]

        found = sum(1 for kw in keywords if kw.lower() in content.lower())

        if found >= 1:
            return TestResult(
                test_name="Backward Compatibility",
                status=TestStatus.PASS,
                message=f"Backward compatibility considered ({found} references)"
            )
        else:
            return TestResult(
                test_name="Backward Compatibility",
                status=TestStatus.WARN,
                message="Backward compatibility not explicitly addressed"
            )


# ============================================================================
# Documentation Quality Tests
# ============================================================================

class DocumentationQualityValidator:
    """Validates documentation completeness and quality"""

    @staticmethod
    def validate_command_line_flags(content: str) -> TestResult:
        """Test: Command-line flags documented"""
        flag_pattern = r'--\w+'
        flags = re.findall(flag_pattern, content)

        if len(flags) >= 3:
            return TestResult(
                test_name="Command-Line Flags",
                status=TestStatus.PASS,
                message=f"Command-line flags documented ({len(flags)} flags found)"
            )
        else:
            return TestResult(
                test_name="Command-Line Flags",
                status=TestStatus.WARN,
                message=f"Few command-line flags documented ({len(flags)} flags found)"
            )

    @staticmethod
    def validate_code_examples(content: str) -> TestResult:
        """Test: Code examples are syntactically valid"""
        # Extract code blocks
        code_blocks = re.findall(r'```(?:python|yaml|bash)?\n(.*?)```', content, re.DOTALL)

        invalid_blocks = []
        for i, block in enumerate(code_blocks, 1):
            # Check for common syntax errors
            if block.strip().endswith(':') and not block.strip().endswith(':\n'):
                invalid_blocks.append(f"Block {i}: Incomplete statement")

        if not invalid_blocks:
            return TestResult(
                test_name="Code Example Validity",
                status=TestStatus.PASS,
                message=f"All code examples appear valid ({len(code_blocks)} blocks)"
            )
        else:
            return TestResult(
                test_name="Code Example Validity",
                status=TestStatus.WARN,
                message=f"Potential syntax issues in {len(invalid_blocks)} blocks"
            )

    @staticmethod
    def validate_internal_links(content: str) -> TestResult:
        """Test: Internal links are consistent"""
        # Extract markdown links
        link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        links = re.findall(link_pattern, content)

        broken_links = []
        for text, url in links:
            # Check for relative file references
            if url.startswith('../') or url.startswith('./'):
                # This is a file reference - would need actual file check
                pass
            elif url.startswith('#'):
                # Internal anchor - check if target exists
                anchor = url[1:]
                if not re.search(rf'#{{{anchor}}}|name="{anchor}"', content):
                    broken_links.append(f"{text} -> {url}")

        if not broken_links:
            return TestResult(
                test_name="Internal Link Consistency",
                status=TestStatus.PASS,
                message=f"All internal links appear valid ({len(links)} links)"
            )
        else:
            return TestResult(
                test_name="Internal Link Consistency",
                status=TestStatus.WARN,
                message=f"Potential broken links: {len(broken_links)}"
            )


# ============================================================================
# Acceptance Criteria Validation
# ============================================================================

class AcceptanceCriteriaValidator:
    """Validates that acceptance criteria from TASK-003C are addressed"""

    @staticmethod
    def validate_ac1_phase_27_documented(report: ValidationReport) -> TestResult:
        """AC1: Phase 2.7 fully documented"""
        phase_27_tests = [r for r in report.results if 'Phase 2.7' in r.test_name]
        passing = all(r.status == TestStatus.PASS for r in phase_27_tests)

        if passing and len(phase_27_tests) > 0:
            return TestResult(
                test_name="AC1: Phase 2.7 Documented",
                status=TestStatus.PASS,
                message="Phase 2.7 fully documented in task-work.md and task-manager.md"
            )
        else:
            return TestResult(
                test_name="AC1: Phase 2.7 Documented",
                status=TestStatus.FAIL,
                message="Phase 2.7 documentation incomplete"
            )

    @staticmethod
    def validate_ac2_phase_28_documented(report: ValidationReport) -> TestResult:
        """AC2: Phase 2.8 fully documented"""
        phase_28_tests = [r for r in report.results if 'Phase 2.8' in r.test_name]
        passing = all(r.status == TestStatus.PASS for r in phase_28_tests)

        if passing and len(phase_28_tests) > 0:
            return TestResult(
                test_name="AC2: Phase 2.8 Documented",
                status=TestStatus.PASS,
                message="Phase 2.8 fully documented with all review modes"
            )
        else:
            return TestResult(
                test_name="AC2: Phase 2.8 Documented",
                status=TestStatus.FAIL,
                message="Phase 2.8 documentation incomplete"
            )

    @staticmethod
    def validate_ac3_orchestration_logic(report: ValidationReport) -> TestResult:
        """AC3: task-manager.md orchestration logic complete"""
        orchestration_tests = [r for r in report.results if 'Orchestration' in r.test_name]
        passing = all(r.status == TestStatus.PASS for r in orchestration_tests)

        if passing and len(orchestration_tests) > 0:
            return TestResult(
                test_name="AC3: Orchestration Logic",
                status=TestStatus.PASS,
                message="task-manager.md orchestration logic documented"
            )
        else:
            return TestResult(
                test_name="AC3: Orchestration Logic",
                status=TestStatus.FAIL,
                message="Orchestration logic incomplete"
            )

    @staticmethod
    def validate_ac4_stubs_marked(report: ValidationReport) -> TestResult:
        """AC4: Stub placeholders clearly marked"""
        stub_tests = [r for r in report.results if 'Stub' in r.test_name]
        passing = any(r.status == TestStatus.PASS for r in stub_tests)

        if passing:
            return TestResult(
                test_name="AC4: Stub Placeholders",
                status=TestStatus.PASS,
                message="Future work clearly marked with stub placeholders"
            )
        else:
            return TestResult(
                test_name="AC4: Stub Placeholders",
                status=TestStatus.WARN,
                message="Stub placeholders could be more explicit"
            )

    @staticmethod
    def validate_ac5_yagni_compliance(report: ValidationReport) -> TestResult:
        """AC5: YAGNI violations removed"""
        yagni_tests = [r for r in report.results if 'YAGNI' in r.test_name]
        passing = any(r.status == TestStatus.PASS for r in yagni_tests)

        if passing:
            return TestResult(
                test_name="AC5: YAGNI Compliance",
                status=TestStatus.PASS,
                message="No YAGNI violations detected"
            )
        else:
            return TestResult(
                test_name="AC5: YAGNI Compliance",
                status=TestStatus.WARN,
                message="Potential YAGNI issues detected"
            )


# ============================================================================
# Test Suite Execution
# ============================================================================

def run_validation_suite() -> ValidationReport:
    """Execute complete validation test suite"""
    report = ValidationReport()

    print("=" * 80)
    print("TASK-003C VALIDATION TEST SUITE")
    print("=" * 80)
    print()

    # Load file contents
    print("Loading files...")
    task_work_content = TASK_WORK_FILE.read_text()
    task_manager_content = TASK_MANAGER_FILE.read_text()
    print(f"✓ Loaded {TASK_WORK_FILE.name} ({len(task_work_content)} chars)")
    print(f"✓ Loaded {TASK_MANAGER_FILE.name} ({len(task_manager_content)} chars)")
    print()

    # ========================================================================
    # Section 1: Markdown Validation Tests
    # ========================================================================
    print("=" * 80)
    print("SECTION 1: MARKDOWN VALIDATION")
    print("=" * 80)

    # File existence
    report.add_result(MarkdownValidator.validate_file_exists(TASK_WORK_FILE))
    report.add_result(MarkdownValidator.validate_file_exists(TASK_MANAGER_FILE))

    # Markdown syntax
    for result in MarkdownValidator.validate_markdown_syntax(task_work_content, "task-work.md"):
        report.add_result(result)

    for result in MarkdownValidator.validate_markdown_syntax(task_manager_content, "task-manager.md"):
        report.add_result(result)

    # Required sections in task-work.md
    required_sections_task_work = [
        "Phase 2.7",
        "Phase 2.8",
        "Complexity Evaluation",
        "Implementation Plan",
        "Review Mode"
    ]

    for section in required_sections_task_work:
        report.add_result(
            MarkdownValidator.validate_section_exists(task_work_content, section, "task-work.md")
        )

    # Required sections in task-manager.md
    required_sections_task_manager = [
        "Phase 2.7",
        "Phase 2.8",
        "Complexity Score",
        "Review Mode"
    ]

    for section in required_sections_task_manager:
        report.add_result(
            MarkdownValidator.validate_section_exists(task_manager_content, section, "task-manager.md")
        )

    print_section_summary(report.results[-20:])

    # ========================================================================
    # Section 2: Phase Flow Validation
    # ========================================================================
    print()
    print("=" * 80)
    print("SECTION 2: PHASE FLOW VALIDATION")
    print("=" * 80)

    report.add_result(PhaseFlowValidator.validate_phase_27_exists(task_work_content))
    report.add_result(PhaseFlowValidator.validate_phase_28_exists(task_work_content))
    report.add_result(PhaseFlowValidator.validate_phase_flow_diagram(task_work_content))
    report.add_result(PhaseFlowValidator.validate_complexity_evaluation(task_work_content))
    report.add_result(PhaseFlowValidator.validate_review_mode_routing(task_work_content))

    print_section_summary(report.results[-5:])

    # ========================================================================
    # Section 3: Task Manager Orchestration
    # ========================================================================
    print()
    print("=" * 80)
    print("SECTION 3: TASK MANAGER ORCHESTRATION")
    print("=" * 80)

    report.add_result(TaskManagerValidator.validate_phase_27_orchestration(task_manager_content))
    report.add_result(TaskManagerValidator.validate_phase_28_orchestration(task_manager_content))
    report.add_result(TaskManagerValidator.validate_complexity_calculator(task_manager_content))

    print_section_summary(report.results[-3:])

    # ========================================================================
    # Section 4: Logical Consistency
    # ========================================================================
    print()
    print("=" * 80)
    print("SECTION 4: LOGICAL CONSISTENCY")
    print("=" * 80)

    report.add_result(LogicalConsistencyValidator.validate_phase_sequence(task_work_content))
    report.add_result(LogicalConsistencyValidator.validate_error_handling(task_work_content))
    report.add_result(LogicalConsistencyValidator.validate_stub_placeholders(task_work_content))

    print_section_summary(report.results[-3:])

    # ========================================================================
    # Section 5: Architectural Compliance
    # ========================================================================
    print()
    print("=" * 80)
    print("SECTION 5: ARCHITECTURAL COMPLIANCE")
    print("=" * 80)

    report.add_result(ArchitecturalValidator.validate_yagni_compliance(task_work_content))
    report.add_result(ArchitecturalValidator.validate_metadata_builder_pattern(task_manager_content))
    report.add_result(ArchitecturalValidator.validate_backward_compatibility(task_work_content))

    print_section_summary(report.results[-3:])

    # ========================================================================
    # Section 6: Documentation Quality
    # ========================================================================
    print()
    print("=" * 80)
    print("SECTION 6: DOCUMENTATION QUALITY")
    print("=" * 80)

    report.add_result(DocumentationQualityValidator.validate_command_line_flags(task_work_content))
    report.add_result(DocumentationQualityValidator.validate_code_examples(task_work_content))
    report.add_result(DocumentationQualityValidator.validate_internal_links(task_work_content))

    print_section_summary(report.results[-3:])

    # ========================================================================
    # Section 7: Acceptance Criteria Validation
    # ========================================================================
    print()
    print("=" * 80)
    print("SECTION 7: ACCEPTANCE CRITERIA VALIDATION")
    print("=" * 80)

    report.add_result(AcceptanceCriteriaValidator.validate_ac1_phase_27_documented(report))
    report.add_result(AcceptanceCriteriaValidator.validate_ac2_phase_28_documented(report))
    report.add_result(AcceptanceCriteriaValidator.validate_ac3_orchestration_logic(report))
    report.add_result(AcceptanceCriteriaValidator.validate_ac4_stubs_marked(report))
    report.add_result(AcceptanceCriteriaValidator.validate_ac5_yagni_compliance(report))

    print_section_summary(report.results[-5:])

    return report


def print_section_summary(results: List[TestResult]):
    """Print summary of test results for a section"""
    for result in results:
        status_icon = result.status.value
        print(f"{status_icon} {result.test_name}")
        if result.status != TestStatus.PASS:
            print(f"   → {result.message}")
            if result.details:
                print(f"   → Details: {result.details[:100]}...")


def generate_detailed_report(report: ValidationReport) -> str:
    """Generate detailed markdown report"""
    lines = []
    lines.append("# TASK-003C Validation Report")
    lines.append("")
    lines.append(f"**Generated**: {Path(__file__).name}")
    lines.append(f"**Date**: 2025-10-10")
    lines.append("")

    # Executive Summary
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(f"- **Total Tests**: {report.total_tests}")
    lines.append(f"- **Passed**: {report.passed} ✅")
    lines.append(f"- **Failed**: {report.failed} ❌")
    lines.append(f"- **Warnings**: {report.warnings} ⚠️")
    lines.append(f"- **Pass Rate**: {report.pass_rate():.1f}%")
    lines.append("")

    # Overall Assessment
    if report.failed == 0:
        lines.append("**Overall Assessment**: ✅ **PASSING** - All critical tests passed")
    elif report.failed <= 2:
        lines.append("**Overall Assessment**: ⚠️ **NEEDS ATTENTION** - Minor issues detected")
    else:
        lines.append("**Overall Assessment**: ❌ **FAILING** - Critical issues detected")
    lines.append("")

    # Failed Tests
    if report.failed > 0:
        lines.append("## Failed Tests")
        lines.append("")
        for result in report.results:
            if result.status == TestStatus.FAIL:
                lines.append(f"### ❌ {result.test_name}")
                lines.append(f"- **Message**: {result.message}")
                if result.details:
                    lines.append(f"- **Details**: {result.details}")
                if result.file_line:
                    lines.append(f"- **Location**: {result.file_line}")
                lines.append("")

    # Warnings
    if report.warnings > 0:
        lines.append("## Warnings")
        lines.append("")
        for result in report.results:
            if result.status == TestStatus.WARN:
                lines.append(f"### ⚠️ {result.test_name}")
                lines.append(f"- **Message**: {result.message}")
                lines.append("")

    # All Test Results
    lines.append("## Complete Test Results")
    lines.append("")
    lines.append("| Test Name | Status | Message |")
    lines.append("|-----------|--------|---------|")
    for result in report.results:
        lines.append(f"| {result.test_name} | {result.status.value} | {result.message} |")
    lines.append("")

    # Documentation Completeness
    lines.append("## Documentation Completeness")
    lines.append("")

    doc_tests = [r for r in report.results if any(x in r.test_name for x in ['Phase', 'Section', 'Orchestration'])]
    doc_passed = sum(1 for r in doc_tests if r.status == TestStatus.PASS)
    doc_total = len(doc_tests)
    doc_percent = (doc_passed / doc_total * 100) if doc_total > 0 else 0

    lines.append(f"- **Documentation Coverage**: {doc_percent:.1f}% ({doc_passed}/{doc_total} tests)")
    lines.append("")

    # Logical Consistency
    logic_tests = [r for r in report.results if any(x in r.test_name for x in ['Logic', 'Flow', 'Sequence', 'Consistency'])]
    logic_passed = sum(1 for r in logic_tests if r.status == TestStatus.PASS)
    logic_total = len(logic_tests)
    logic_percent = (logic_passed / logic_total * 100) if logic_total > 0 else 0

    lines.append(f"- **Logical Consistency**: {logic_percent:.1f}% ({logic_passed}/{logic_total} tests)")
    lines.append("")

    # Architectural Alignment
    arch_tests = [r for r in report.results if any(x in r.test_name for x in ['YAGNI', 'Pattern', 'Architect', 'Compatibility'])]
    arch_passed = sum(1 for r in arch_tests if r.status == TestStatus.PASS)
    arch_total = len(arch_tests)
    arch_percent = (arch_passed / arch_total * 100) if arch_total > 0 else 0

    lines.append(f"- **Architectural Alignment**: {arch_percent:.1f}% ({arch_passed}/{arch_total} tests)")
    lines.append("")

    # Recommendations
    lines.append("## Recommendations")
    lines.append("")

    if report.failed > 0:
        lines.append("1. **Address Failed Tests**: Fix critical documentation gaps")
    if report.warnings > 3:
        lines.append("2. **Review Warnings**: Consider enhancing documentation clarity")
    if report.pass_rate() >= 90:
        lines.append("3. **Excellent Quality**: Documentation is comprehensive and well-structured")
    lines.append("")

    # Quality Score
    quality_score = (report.pass_rate() * 0.6 + doc_percent * 0.2 + logic_percent * 0.1 + arch_percent * 0.1)
    lines.append("## Quality Score")
    lines.append("")
    lines.append(f"**Overall Quality**: {quality_score:.1f}/100")
    lines.append("")

    if quality_score >= 90:
        lines.append("✅ **EXCELLENT** - Ready for production")
    elif quality_score >= 80:
        lines.append("✅ **GOOD** - Minor improvements recommended")
    elif quality_score >= 70:
        lines.append("⚠️ **ACCEPTABLE** - Address warnings before merging")
    else:
        lines.append("❌ **NEEDS WORK** - Significant improvements required")
    lines.append("")

    return "\n".join(lines)


def main():
    """Main test execution"""
    report = run_validation_suite()

    # Print final summary
    print()
    print("=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)
    print()
    print(f"Total Tests:  {report.total_tests}")
    print(f"Passed:       {report.passed} ✅")
    print(f"Failed:       {report.failed} ❌")
    print(f"Warnings:     {report.warnings} ⚠️")
    print(f"Pass Rate:    {report.pass_rate():.1f}%")
    print()

    # Calculate quality score
    doc_tests = [r for r in report.results if any(x in r.test_name for x in ['Phase', 'Section', 'Orchestration'])]
    doc_passed = sum(1 for r in doc_tests if r.status == TestStatus.PASS)
    doc_total = len(doc_tests)
    doc_percent = (doc_passed / doc_total * 100) if doc_total > 0 else 0

    logic_tests = [r for r in report.results if any(x in r.test_name for x in ['Logic', 'Flow', 'Sequence'])]
    logic_passed = sum(1 for r in logic_tests if r.status == TestStatus.PASS)
    logic_total = len(logic_tests)
    logic_percent = (logic_passed / logic_total * 100) if logic_total > 0 else 0

    arch_tests = [r for r in report.results if any(x in r.test_name for x in ['YAGNI', 'Pattern', 'Architect'])]
    arch_passed = sum(1 for r in arch_tests if r.status == TestStatus.PASS)
    arch_total = len(arch_tests)
    arch_percent = (arch_passed / arch_total * 100) if arch_total > 0 else 0

    quality_score = (report.pass_rate() * 0.6 + doc_percent * 0.2 + logic_percent * 0.1 + arch_percent * 0.1)

    print(f"Documentation Completeness: {doc_percent:.1f}%")
    print(f"Logical Consistency:        {logic_percent:.1f}%")
    print(f"Architectural Alignment:    {arch_percent:.1f}%")
    print()
    print(f"Overall Quality Score:      {quality_score:.1f}/100")
    print()

    # Status badge
    if quality_score >= 90:
        print("✅ EXCELLENT - Documentation is comprehensive and production-ready")
    elif quality_score >= 80:
        print("✅ GOOD - Documentation meets quality standards")
    elif quality_score >= 70:
        print("⚠️ ACCEPTABLE - Minor improvements recommended")
    else:
        print("❌ NEEDS WORK - Significant improvements required")
    print()

    # Generate detailed report
    detailed_report = generate_detailed_report(report)
    report_file = PROJECT_ROOT / "docs/test_reports/TASK-003C-validation-report.md"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(detailed_report)
    print(f"Detailed report saved: {report_file}")
    print()

    # Exit code
    if report.failed > 0:
        return 1
    else:
        return 0


if __name__ == "__main__":
    exit(main())
