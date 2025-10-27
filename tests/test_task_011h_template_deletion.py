#!/usr/bin/env python3
"""
TASK-011H Verification Tests
Test suite to verify old MAUI template deletion and no breakage
"""

import os
import subprocess
import json
from pathlib import Path

# Test configuration
REPO_ROOT = Path(__file__).parent.parent
TEMPLATES_DIR = REPO_ROOT / "installer" / "global" / "templates"
SCRIPTS_DIR = REPO_ROOT / "installer" / "scripts"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name):
    print(f"\n{Colors.BLUE}Testing: {name}{Colors.END}")

def print_pass(message):
    print(f"  {Colors.GREEN}✓ {message}{Colors.END}")

def print_fail(message):
    print(f"  {Colors.RED}✗ {message}{Colors.END}")

def print_info(message):
    print(f"  {Colors.YELLOW}ℹ {message}{Colors.END}")

# Test 1: Verify old template deleted
def test_old_template_deleted():
    print_test("Old MAUI template deleted")

    old_template = TEMPLATES_DIR / "maui"
    if not old_template.exists():
        print_pass("Old 'maui' template directory deleted")
        return True
    else:
        print_fail(f"Old 'maui' template still exists at: {old_template}")
        return False

# Test 2: Verify new templates exist
def test_new_templates_exist():
    print_test("New MAUI templates exist")

    appshell_template = TEMPLATES_DIR / "maui-appshell"
    navpage_template = TEMPLATES_DIR / "maui-navigationpage"

    results = []

    if appshell_template.exists():
        print_pass(f"maui-appshell template exists")
        results.append(True)
    else:
        print_fail(f"maui-appshell template NOT FOUND at: {appshell_template}")
        results.append(False)

    if navpage_template.exists():
        print_pass(f"maui-navigationpage template exists")
        results.append(True)
    else:
        print_fail(f"maui-navigationpage template NOT FOUND at: {navpage_template}")
        results.append(False)

    return all(results)

# Test 3: Verify template count
def test_template_count():
    print_test("Template count verification")

    # Expected templates
    expected_templates = [
        "default",
        "react",
        "python",
        "typescript-api",
        "maui-appshell",
        "maui-navigationpage",
        "dotnet-microservice",
        "fullstack"
    ]

    actual_templates = []
    for item in TEMPLATES_DIR.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            actual_templates.append(item.name)

    actual_templates.sort()
    expected_templates.sort()

    print_info(f"Expected templates: {', '.join(expected_templates)}")
    print_info(f"Actual templates: {', '.join(actual_templates)}")

    if set(actual_templates) == set(expected_templates):
        print_pass(f"Template count correct: {len(expected_templates)} templates")
        return True
    else:
        missing = set(expected_templates) - set(actual_templates)
        extra = set(actual_templates) - set(expected_templates)
        if missing:
            print_fail(f"Missing templates: {missing}")
        if extra:
            print_fail(f"Extra templates: {extra}")
        return False

# Test 4: Verify no references to old template in scripts
def test_no_old_template_references():
    print_test("No old template references in completion scripts")

    install_sh = SCRIPTS_DIR / "install.sh"

    results = []

    with open(install_sh, 'r') as f:
        content = f.read()

    # Check completion templates don't have standalone "maui"
    if 'templates="default react python maui-appshell maui-navigationpage' in content:
        print_pass("install.sh completion updated correctly")
        results.append(True)
    else:
        print_fail("install.sh completion still references old 'maui' template")
        results.append(False)

    # Verify old "maui" not in completion (but "maui-appshell" is OK)
    lines_with_old_maui = []
    for i, line in enumerate(content.split('\n'), 1):
        if 'templates=' in line and '"maui"' in line and 'maui-appshell' not in line:
            lines_with_old_maui.append(i)

    if not lines_with_old_maui:
        print_pass("No standalone 'maui' references in templates list")
        results.append(True)
    else:
        print_fail(f"Found old 'maui' reference at lines: {lines_with_old_maui}")
        results.append(False)

    return all(results)

# Test 5: Verify CLAUDE.md updated
def test_claude_md_updated():
    print_test("CLAUDE.md updated with new templates")

    claude_md = REPO_ROOT / "CLAUDE.md"

    with open(claude_md, 'r') as f:
        content = f.read()

    results = []

    if 'maui-appshell' in content and 'maui-navigationpage' in content:
        print_pass("CLAUDE.md mentions both new templates")
        results.append(True)
    else:
        print_fail("CLAUDE.md missing new template references")
        results.append(False)

    # Check it doesn't reference old template in Available Templates section
    # (It's OK to have "maui" in other contexts like detection)
    available_templates_section = content[content.find('### Available Templates'):content.find('## Conductor Integration')]

    if '**maui**:' in available_templates_section or '- **maui**' in available_templates_section:
        print_fail("CLAUDE.md Available Templates section still lists old 'maui' template")
        results.append(False)
    else:
        print_pass("CLAUDE.md Available Templates section updated")
        results.append(True)

    return all(results)

# Test 6: Verify migration plan has rollback section
def test_migration_plan_rollback():
    print_test("Migration plan has rollback section")

    migration_plan = REPO_ROOT / "docs" / "workflows" / "maui-template-migration-plan.md"

    with open(migration_plan, 'r') as f:
        content = f.read()

    results = []

    if '## Rollback Procedure' in content:
        print_pass("Migration plan has Rollback Procedure section")
        results.append(True)
    else:
        print_fail("Migration plan missing Rollback Procedure section")
        results.append(False)

    if '8e393d206f1882b462552080ed53fc5c01cc30c0' in content:
        print_pass("Migration plan includes checkpoint commit hash")
        results.append(True)
    else:
        print_fail("Migration plan missing checkpoint commit hash")
        results.append(False)

    return all(results)

# Test 7: Verify init-claude-project.sh updated
def test_init_script_updated():
    print_test("init-claude-project.sh updated correctly")

    init_script = SCRIPTS_DIR / "init-claude-project.sh"

    with open(init_script, 'r') as f:
        content = f.read()

    results = []

    # Check auto-detection defaults to maui-appshell
    if 'maui) effective_template="maui-appshell"' in content:
        print_pass("Auto-detection defaults to maui-appshell")
        results.append(True)
    else:
        print_fail("Auto-detection not updated to maui-appshell")
        results.append(False)

    # Check stack configs exist for both templates
    if 'maui-appshell)' in content and 'maui-navigationpage)' in content:
        print_pass("Stack configs for both new templates exist")
        results.append(True)
    else:
        print_fail("Missing stack configs for new templates")
        results.append(False)

    return all(results)

# Test 8: Verify MyDrive local template exists (if applicable)
def test_mydrive_local_template():
    print_test("MyDrive local template structure (if exists)")

    # This is optional - only if MyDrive project is accessible
    mydrive_path = Path.home() / "Projects" / "appmilla_github" / "DeCUK.Mobile.MyDrive"
    mydrive_template = mydrive_path / ".claude" / "templates" / "maui-mydrive"

    if not mydrive_path.exists():
        print_info("MyDrive project not found (this is OK)")
        return True

    if mydrive_template.exists():
        print_pass("MyDrive local template exists")

        # Check key files
        manifest = mydrive_template / "manifest.json"
        if manifest.exists():
            print_pass("MyDrive template has manifest.json")
        else:
            print_fail("MyDrive template missing manifest.json")

        return True
    else:
        print_info("MyDrive local template not yet created (Phase 3 of migration)")
        return True

def run_all_tests():
    print(f"\n{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BLUE}TASK-011H: Verification Test Suite{Colors.END}")
    print(f"{Colors.BLUE}{'='*70}{Colors.END}")

    tests = [
        ("Old template deleted", test_old_template_deleted),
        ("New templates exist", test_new_templates_exist),
        ("Template count correct", test_template_count),
        ("No old template refs", test_no_old_template_references),
        ("CLAUDE.md updated", test_claude_md_updated),
        ("Migration plan rollback", test_migration_plan_rollback),
        ("Init script updated", test_init_script_updated),
        ("MyDrive local template", test_mydrive_local_template),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print_fail(f"Test crashed: {e}")
            results.append((name, False))

    # Summary
    print(f"\n{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BLUE}Test Summary{Colors.END}")
    print(f"{Colors.BLUE}{'='*70}{Colors.END}\n")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = f"{Colors.GREEN}PASS{Colors.END}" if result else f"{Colors.RED}FAIL{Colors.END}"
        print(f"  {status} - {name}")

    print(f"\n{Colors.BLUE}Results: {passed}/{total} tests passed{Colors.END}")

    if passed == total:
        print(f"{Colors.GREEN}✓ All tests passed! TASK-011H ready for completion.{Colors.END}\n")
        return 0
    else:
        print(f"{Colors.RED}✗ Some tests failed. Review issues above.{Colors.END}\n")
        return 1

if __name__ == "__main__":
    exit(run_all_tests())
