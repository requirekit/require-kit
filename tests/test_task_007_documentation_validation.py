#!/usr/bin/env python3
"""
TASK-007 Documentation Validation Test Suite

This test suite validates that all documentation updates for TASK-007
(Enforce 100% test pass requirement) are syntactically correct, structurally
complete, and consistent across all modified files.

This is a DOCUMENTATION-ONLY task. The "tests" verify:
1. Syntactic correctness (Markdown is valid)
2. Structural completeness (all required sections present)
3. Consistency across files (cross-references are accurate)

Files under test:
- /Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/commands/task-work.md
- /Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/agents/test-orchestrator.md
- /Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/templates/maui/agents/test-orchestrator.md
"""

import os
import re
from pathlib import Path

# File paths
BASE_DIR = Path("/Users/richardwoollcott/Projects/appmilla_github/ai-engineer")
TASK_WORK_FILE = BASE_DIR / "installer/global/commands/task-work.md"
TEST_ORCHESTRATOR_FILE = BASE_DIR / "installer/global/agents/test-orchestrator.md"
MAUI_TEST_ORCHESTRATOR_FILE = BASE_DIR / "installer/global/templates/maui/agents/test-orchestrator.md"


class TestResults:
    """Collects test results for final reporting"""
    def __init__(self):
        self.passed = []
        self.failed = []

    def add_pass(self, test_name):
        self.passed.append(test_name)
        print(f"✅ PASS: {test_name}")

    def add_fail(self, test_name, reason):
        self.failed.append((test_name, reason))
        print(f"❌ FAIL: {test_name}")
        print(f"   Reason: {reason}")

    def summary(self):
        total = len(self.passed) + len(self.failed)
        print("\n" + "=" * 80)
        print("TEST SUITE SUMMARY")
        print("=" * 80)
        print(f"Total tests: {total}")
        print(f"Passed: {len(self.passed)} ✅")
        print(f"Failed: {len(self.failed)} ❌")
        print(f"Pass rate: {(len(self.passed)/total*100):.1f}%")

        if self.failed:
            print("\n❌ FAILURES:")
            for test_name, reason in self.failed:
                print(f"  - {test_name}: {reason}")
            return False
        else:
            print("\n✅ ALL TESTS PASSED")
            return True


results = TestResults()


# ============================================================================
# CATEGORY 1: FILE EXISTENCE & ACCESSIBILITY
# ============================================================================

def test_task_work_file_exists():
    """Verify task-work.md exists at expected path"""
    if TASK_WORK_FILE.exists():
        results.add_pass("task-work.md file exists")
    else:
        results.add_fail("task-work.md file exists",
                        f"File not found at {TASK_WORK_FILE}")


def test_test_orchestrator_file_exists():
    """Verify test-orchestrator.md exists at expected path"""
    if TEST_ORCHESTRATOR_FILE.exists():
        results.add_pass("test-orchestrator.md file exists")
    else:
        results.add_fail("test-orchestrator.md file exists",
                        f"File not found at {TEST_ORCHESTRATOR_FILE}")


def test_maui_test_orchestrator_file_exists():
    """Verify MAUI test-orchestrator.md exists at expected path"""
    if MAUI_TEST_ORCHESTRATOR_FILE.exists():
        results.add_pass("MAUI test-orchestrator.md file exists")
    else:
        results.add_fail("MAUI test-orchestrator.md file exists",
                        f"File not found at {MAUI_TEST_ORCHESTRATOR_FILE}")


# ============================================================================
# CATEGORY 2: MARKDOWN SYNTAX VALIDATION
# ============================================================================

def test_markdown_syntax_task_work():
    """Verify task-work.md has valid Markdown syntax"""
    content = TASK_WORK_FILE.read_text()

    # Check for unclosed code blocks
    code_block_pattern = r'```'
    code_blocks = re.findall(code_block_pattern, content)
    if len(code_blocks) % 2 != 0:
        results.add_fail("task-work.md Markdown syntax",
                        f"Unclosed code blocks detected ({len(code_blocks)} markers)")
        return

    # Check for malformed headers
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        if line.startswith('#'):
            # Headers should have space after #
            if not re.match(r'^#+\s+.+', line):
                results.add_fail("task-work.md Markdown syntax",
                                f"Malformed header at line {i}: {line[:50]}")
                return

    results.add_pass("task-work.md Markdown syntax is valid")


def test_markdown_syntax_test_orchestrator():
    """Verify test-orchestrator.md has valid Markdown syntax"""
    content = TEST_ORCHESTRATOR_FILE.read_text()

    # Check for unclosed code blocks
    code_block_pattern = r'```'
    code_blocks = re.findall(code_block_pattern, content)
    if len(code_blocks) % 2 != 0:
        results.add_fail("test-orchestrator.md Markdown syntax",
                        f"Unclosed code blocks detected ({len(code_blocks)} markers)")
        return

    results.add_pass("test-orchestrator.md Markdown syntax is valid")


def test_markdown_syntax_maui_test_orchestrator():
    """Verify MAUI test-orchestrator.md has valid Markdown syntax"""
    content = MAUI_TEST_ORCHESTRATOR_FILE.read_text()

    # Check for unclosed code blocks
    code_block_pattern = r'```'
    code_blocks = re.findall(code_block_pattern, content)
    if len(code_blocks) % 2 != 0:
        results.add_fail("MAUI test-orchestrator.md Markdown syntax",
                        f"Unclosed code blocks detected ({len(code_blocks)} markers)")
        return

    results.add_pass("MAUI test-orchestrator.md Markdown syntax is valid")


# ============================================================================
# CATEGORY 3: CONTENT COMPLETENESS - task-work.md
# ============================================================================

def test_phase_45_absolute_requirement():
    """Verify Phase 4.5 includes 'ABSOLUTE REQUIREMENT' language"""
    content = TASK_WORK_FILE.read_text()

    # Find Phase 4.5 section
    phase_45_match = re.search(
        r'#### Phase 4\.5:.*?(?=####|\Z)',
        content,
        re.DOTALL
    )

    if not phase_45_match:
        results.add_fail("Phase 4.5 ABSOLUTE REQUIREMENT",
                        "Phase 4.5 section not found in task-work.md")
        return

    phase_45_content = phase_45_match.group(0)

    if "ABSOLUTE REQUIREMENT" in phase_45_content:
        results.add_pass("Phase 4.5 contains 'ABSOLUTE REQUIREMENT'")
    else:
        results.add_fail("Phase 4.5 ABSOLUTE REQUIREMENT",
                        "Missing 'ABSOLUTE REQUIREMENT' emphatic language")


def test_phase_45_zero_tolerance():
    """Verify Phase 4.5 includes 'ZERO TOLERANCE' language"""
    content = TASK_WORK_FILE.read_text()

    phase_45_match = re.search(
        r'#### Phase 4\.5:.*?(?=####|\Z)',
        content,
        re.DOTALL
    )

    if not phase_45_match:
        results.add_fail("Phase 4.5 ZERO TOLERANCE",
                        "Phase 4.5 section not found")
        return

    phase_45_content = phase_45_match.group(0)

    if "ZERO TOLERANCE" in phase_45_content:
        results.add_pass("Phase 4.5 contains 'ZERO TOLERANCE'")
    else:
        results.add_fail("Phase 4.5 ZERO TOLERANCE",
                        "Missing 'ZERO TOLERANCE' emphatic language")


def test_step_6_blocking_logic():
    """Verify Step 6 includes explicit Python blocking logic"""
    content = TASK_WORK_FILE.read_text()

    step_6_match = re.search(
        r'### Step 6:.*?(?=###|\Z)',
        content,
        re.DOTALL
    )

    if not step_6_match:
        results.add_fail("Step 6 blocking logic",
                        "Step 6 section not found in task-work.md")
        return

    step_6_content = step_6_match.group(0)

    # Check for Python function definition
    if "def determine_next_state" in step_6_content:
        results.add_pass("Step 6 contains Python blocking logic function")
    else:
        results.add_fail("Step 6 blocking logic",
                        "Missing 'def determine_next_state' function")


def test_step_6_compilation_gate():
    """Verify Step 6 includes compilation error gate"""
    content = TASK_WORK_FILE.read_text()

    step_6_match = re.search(
        r'### Step 6:.*?(?=###|\Z)',
        content,
        re.DOTALL
    )

    if not step_6_match:
        results.add_fail("Step 6 compilation gate",
                        "Step 6 section not found")
        return

    step_6_content = step_6_match.group(0)

    if "if compilation_errors > 0:" in step_6_content:
        results.add_pass("Step 6 includes compilation error gate check")
    else:
        results.add_fail("Step 6 compilation gate",
                        "Missing 'if compilation_errors > 0:' gate logic")


def test_step_6_test_failure_gate():
    """Verify Step 6 includes test failure gate"""
    content = TASK_WORK_FILE.read_text()

    step_6_match = re.search(
        r'### Step 6:.*?(?=###|\Z)',
        content,
        re.DOTALL
    )

    if not step_6_match:
        results.add_fail("Step 6 test failure gate",
                        "Step 6 section not found")
        return

    step_6_content = step_6_match.group(0)

    if "test_failures > 0" in step_6_content and "test_pass_rate < 1.0" in step_6_content:
        results.add_pass("Step 6 includes test failure gate check")
    else:
        results.add_fail("Step 6 test failure gate",
                        "Missing comprehensive test failure gate logic")


def test_phase_4_cross_reference():
    """Verify Phase 4 references test-orchestrator.md correctly"""
    content = TASK_WORK_FILE.read_text()

    phase_4_match = re.search(
        r'#### Phase 4:.*?(?=####|\Z)',
        content,
        re.DOTALL
    )

    if not phase_4_match:
        results.add_fail("Phase 4 cross-reference",
                        "Phase 4 section not found")
        return

    phase_4_content = phase_4_match.group(0)

    if "test-orchestrator.md" in phase_4_content:
        results.add_pass("Phase 4 references test-orchestrator.md")
    else:
        results.add_fail("Phase 4 cross-reference",
                        "Missing reference to test-orchestrator.md")


def test_phase_4_mandatory_compilation():
    """Verify Phase 4 mentions mandatory compilation check"""
    content = TASK_WORK_FILE.read_text()

    phase_4_match = re.search(
        r'#### Phase 4:.*?(?=####|\Z)',
        content,
        re.DOTALL
    )

    if not phase_4_match:
        results.add_fail("Phase 4 mandatory compilation",
                        "Phase 4 section not found")
        return

    phase_4_content = phase_4_match.group(0)

    if "MANDATORY COMPILATION CHECK" in phase_4_content or "MUST verify code COMPILES" in phase_4_content:
        results.add_pass("Phase 4 mentions mandatory compilation check")
    else:
        results.add_fail("Phase 4 mandatory compilation",
                        "Missing mandatory compilation check language")


# ============================================================================
# CATEGORY 4: CONTENT COMPLETENESS - test-orchestrator.md
# ============================================================================

def test_mandatory_rule_1_header():
    """Verify test-orchestrator.md includes 'MANDATORY RULE #1' header"""
    content = TEST_ORCHESTRATOR_FILE.read_text()

    if "MANDATORY RULE #1: BUILD BEFORE TEST" in content:
        results.add_pass("test-orchestrator.md has MANDATORY RULE #1 header")
    else:
        results.add_fail("MANDATORY RULE #1 header",
                        "Missing 'MANDATORY RULE #1: BUILD BEFORE TEST' section")


def test_absolute_requirement_language():
    """Verify test-orchestrator.md includes ABSOLUTE REQUIREMENT language"""
    content = TEST_ORCHESTRATOR_FILE.read_text()

    rule_1_match = re.search(
        r'## 🚨 MANDATORY RULE #1:.*?(?=##|\Z)',
        content,
        re.DOTALL
    )

    if not rule_1_match:
        results.add_fail("ABSOLUTE REQUIREMENT in Rule #1",
                        "MANDATORY RULE #1 section not found")
        return

    rule_1_content = rule_1_match.group(0)

    if "ABSOLUTE REQUIREMENT" in rule_1_content:
        results.add_pass("test-orchestrator.md Rule #1 has ABSOLUTE REQUIREMENT")
    else:
        results.add_fail("ABSOLUTE REQUIREMENT in Rule #1",
                        "Missing 'ABSOLUTE REQUIREMENT' language")


def test_build_verification_sequence():
    """Verify test-orchestrator.md includes build verification sequence"""
    content = TEST_ORCHESTRATOR_FILE.read_text()

    required_steps = [
        "Step 1: Clean",
        "Step 2: Restore",
        "Step 3: Build",
        "Step 4: IF build fails, STOP",
        "Step 5: ONLY if build succeeds"
    ]

    all_found = all(step in content for step in required_steps)

    if all_found:
        results.add_pass("test-orchestrator.md includes complete build sequence")
    else:
        missing = [step for step in required_steps if step not in content]
        results.add_fail("Build verification sequence",
                        f"Missing steps: {missing}")


def test_stack_specific_build_commands():
    """Verify test-orchestrator.md includes stack-specific build commands"""
    content = TEST_ORCHESTRATOR_FILE.read_text()

    required_stacks = [".NET / C# / MAUI", "TypeScript / Node.js", "Python", "Java"]

    found_stacks = [stack for stack in required_stacks if stack in content]

    if len(found_stacks) >= 3:  # Allow for some flexibility
        results.add_pass("test-orchestrator.md includes stack-specific build commands")
    else:
        results.add_fail("Stack-specific build commands",
                        f"Only found {len(found_stacks)}/4 stacks: {found_stacks}")


def test_quality_gates_zero_tolerance():
    """Verify test-orchestrator.md quality gates include zero tolerance flags"""
    content = TEST_ORCHESTRATOR_FILE.read_text()

    quality_gates_match = re.search(
        r'## Quality Gate Configuration.*?(?=##|\Z)',
        content,
        re.DOTALL
    )

    if not quality_gates_match:
        results.add_fail("Quality gates zero tolerance",
                        "Quality Gate Configuration section not found")
        return

    quality_gates_content = quality_gates_match.group(0)

    checks = {
        "test_pass_rate: 100": "test_pass_rate: 100" in quality_gates_content,
        "zero_failures: true": "zero_failures: true" in quality_gates_content,
        "no_exceptions: true": "no_exceptions: true" in quality_gates_content
    }

    if all(checks.values()):
        results.add_pass("test-orchestrator.md quality gates include zero tolerance")
    else:
        missing = [key for key, found in checks.items() if not found]
        results.add_fail("Quality gates zero tolerance",
                        f"Missing: {missing}")


def test_cross_reference_to_task_work():
    """Verify test-orchestrator.md references task-work.md"""
    content = TEST_ORCHESTRATOR_FILE.read_text()

    if "task-work.md" in content:
        results.add_pass("test-orchestrator.md references task-work.md")
    else:
        results.add_fail("Cross-reference to task-work.md",
                        "Missing reference to task-work.md")


# ============================================================================
# CATEGORY 5: CONTENT COMPLETENESS - MAUI test-orchestrator.md
# ============================================================================

def test_maui_mandatory_rule_1():
    """Verify MAUI test-orchestrator.md has MANDATORY RULE #1"""
    content = MAUI_TEST_ORCHESTRATOR_FILE.read_text()

    if "MANDATORY RULE #1: BUILD BEFORE TEST (MAUI-Specific)" in content:
        results.add_pass("MAUI test-orchestrator.md has MANDATORY RULE #1")
    else:
        results.add_fail("MAUI MANDATORY RULE #1",
                        "Missing MAUI-specific MANDATORY RULE #1 section")


def test_maui_4_step_process():
    """Verify MAUI test-orchestrator.md includes 4-step build verification"""
    content = MAUI_TEST_ORCHESTRATOR_FILE.read_text()

    required_phases = [
        "Phase 1: Clean",
        "Phase 2: Restore",
        "Phase 3: Build",
        "Phase 4: Build successful"
    ]

    all_found = all(phase in content for phase in required_phases)

    if all_found:
        results.add_pass("MAUI test-orchestrator.md includes 4-step build process")
    else:
        missing = [phase for phase in required_phases if phase not in content]
        results.add_fail("MAUI 4-step build process",
                        f"Missing phases: {missing}")


def test_maui_erroror_checks():
    """Verify MAUI test-orchestrator.md includes ErrorOr pattern checks"""
    content = MAUI_TEST_ORCHESTRATOR_FILE.read_text()

    erroror_checks = [
        "check_erroror_package",
        "verify_erroror_syntax",
        "ErrorOr package must be installed"
    ]

    found = sum(1 for check in erroror_checks if check in content)

    if found >= 2:  # At least 2 of 3 checks present
        results.add_pass("MAUI test-orchestrator.md includes ErrorOr checks")
    else:
        results.add_fail("MAUI ErrorOr checks",
                        f"Only found {found}/3 ErrorOr-related checks")


def test_maui_quality_gates():
    """Verify MAUI test-orchestrator.md includes MAUI-specific quality gates"""
    content = MAUI_TEST_ORCHESTRATOR_FILE.read_text()

    maui_gates = [
        "maui_compile: true",
        "erroror_package: true",
        "xaml_valid: true",
        "usecase_coverage: 90",
        "viewmodel_coverage: 85"
    ]

    found = sum(1 for gate in maui_gates if gate in content)

    if found >= 4:  # At least 4 of 5 gates present
        results.add_pass("MAUI test-orchestrator.md includes MAUI-specific gates")
    else:
        results.add_fail("MAUI quality gates",
                        f"Only found {found}/5 MAUI-specific gates")


# ============================================================================
# CATEGORY 6: EMPHATIC LANGUAGE PRESENCE
# ============================================================================

def test_emphatic_language_count():
    """Verify emphatic language appears throughout all files"""
    files = {
        "task-work.md": TASK_WORK_FILE,
        "test-orchestrator.md": TEST_ORCHESTRATOR_FILE,
        "MAUI test-orchestrator.md": MAUI_TEST_ORCHESTRATOR_FILE
    }

    emphatic_terms = [
        "ABSOLUTE REQUIREMENT",
        "ZERO TOLERANCE",
        "MANDATORY",
        "NO EXCEPTIONS"
    ]

    total_occurrences = 0
    for file_name, file_path in files.items():
        content = file_path.read_text()
        for term in emphatic_terms:
            total_occurrences += content.count(term)

    if total_occurrences >= 15:  # Expect at least 15 occurrences total
        results.add_pass(f"Emphatic language present ({total_occurrences} occurrences)")
    else:
        results.add_fail("Emphatic language count",
                        f"Only {total_occurrences} occurrences found (expected ≥15)")


def test_visual_emphasis_present():
    """Verify visual emphasis markers (emojis) present in critical sections"""
    content = TASK_WORK_FILE.read_text() + TEST_ORCHESTRATOR_FILE.read_text()

    visual_markers = ["🚨", "❌", "✅"]

    found_markers = sum(1 for marker in visual_markers if marker in content)

    if found_markers >= 2:  # At least 2 of 3 emoji types present
        results.add_pass("Visual emphasis markers present")
    else:
        results.add_fail("Visual emphasis markers",
                        f"Only {found_markers}/3 emoji types found")


# ============================================================================
# CATEGORY 7: CROSS-REFERENCE ACCURACY
# ============================================================================

def test_task_work_references_test_orchestrator():
    """Verify task-work.md accurately references test-orchestrator.md"""
    content = TASK_WORK_FILE.read_text()

    references = [
        "test-orchestrator.md",
        "See test-orchestrator.md",
        "installer/global/agents/test-orchestrator.md"
    ]

    found = sum(1 for ref in references if ref in content)

    if found >= 1:
        results.add_pass("task-work.md references test-orchestrator.md")
    else:
        results.add_fail("task-work.md cross-reference",
                        "Missing reference to test-orchestrator.md")


def test_test_orchestrator_references_task_work():
    """Verify test-orchestrator.md accurately references task-work.md"""
    content = TEST_ORCHESTRATOR_FILE.read_text()

    references = [
        "task-work.md",
        "See task-work.md",
        "Phase 4",
        "Step 6"
    ]

    found = sum(1 for ref in references if ref in content)

    if found >= 2:
        results.add_pass("test-orchestrator.md references task-work.md")
    else:
        results.add_fail("test-orchestrator.md cross-reference",
                        f"Only {found}/4 cross-references found")


def test_maui_test_orchestrator_references():
    """Verify MAUI test-orchestrator.md includes proper cross-references"""
    content = MAUI_TEST_ORCHESTRATOR_FILE.read_text()

    if "task-work.md" in content:
        results.add_pass("MAUI test-orchestrator.md includes cross-references")
    else:
        results.add_fail("MAUI cross-references",
                        "Missing reference to task-work.md")


# ============================================================================
# RUN ALL TESTS
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("TASK-007 DOCUMENTATION VALIDATION TEST SUITE")
    print("=" * 80)
    print("Testing documentation updates for 100% test pass requirement enforcement")
    print()

    # Category 1: File Existence
    print("\nCATEGORY 1: FILE EXISTENCE & ACCESSIBILITY")
    print("-" * 80)
    test_task_work_file_exists()
    test_test_orchestrator_file_exists()
    test_maui_test_orchestrator_file_exists()

    # Category 2: Markdown Syntax
    print("\nCATEGORY 2: MARKDOWN SYNTAX VALIDATION")
    print("-" * 80)
    test_markdown_syntax_task_work()
    test_markdown_syntax_test_orchestrator()
    test_markdown_syntax_maui_test_orchestrator()

    # Category 3: Content Completeness - task-work.md
    print("\nCATEGORY 3: CONTENT COMPLETENESS - task-work.md")
    print("-" * 80)
    test_phase_45_absolute_requirement()
    test_phase_45_zero_tolerance()
    test_step_6_blocking_logic()
    test_step_6_compilation_gate()
    test_step_6_test_failure_gate()
    test_phase_4_cross_reference()
    test_phase_4_mandatory_compilation()

    # Category 4: Content Completeness - test-orchestrator.md
    print("\nCATEGORY 4: CONTENT COMPLETENESS - test-orchestrator.md")
    print("-" * 80)
    test_mandatory_rule_1_header()
    test_absolute_requirement_language()
    test_build_verification_sequence()
    test_stack_specific_build_commands()
    test_quality_gates_zero_tolerance()
    test_cross_reference_to_task_work()

    # Category 5: Content Completeness - MAUI test-orchestrator.md
    print("\nCATEGORY 5: CONTENT COMPLETENESS - MAUI test-orchestrator.md")
    print("-" * 80)
    test_maui_mandatory_rule_1()
    test_maui_4_step_process()
    test_maui_erroror_checks()
    test_maui_quality_gates()

    # Category 6: Emphatic Language
    print("\nCATEGORY 6: EMPHATIC LANGUAGE PRESENCE")
    print("-" * 80)
    test_emphatic_language_count()
    test_visual_emphasis_present()

    # Category 7: Cross-References
    print("\nCATEGORY 7: CROSS-REFERENCE ACCURACY")
    print("-" * 80)
    test_task_work_references_test_orchestrator()
    test_test_orchestrator_references_task_work()
    test_maui_test_orchestrator_references()

    # Final Summary
    success = results.summary()

    exit(0 if success else 1)
