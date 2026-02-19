#!/usr/bin/env python3
"""
Tests for TASK-RK01-010: Update Overview Instructions with Refinement Workflow

Validates that the overview file contains all required documentation updates.
"""

import os
import re
from pathlib import Path


def test_file_exists():
    """Verify the overview file exists."""
    file_path = Path("installer/global/instructions/core/00-overview.md")
    assert file_path.exists(), f"Overview file not found at {file_path}"
    print("✓ Overview file exists")


def test_file_is_valid_markdown():
    """Verify the file is valid markdown (basic check)."""
    file_path = Path("installer/global/instructions/core/00-overview.md")
    content = file_path.read_text()

    # Check for basic markdown structure
    assert content.strip(), "File is empty"
    assert "# " in content, "No headers found"
    print("✓ File is valid markdown")


def test_refinement_component_section():
    """Verify Requirements Refinement component section exists."""
    file_path = Path("installer/global/instructions/core/00-overview.md")
    content = file_path.read_text()

    # Check for refinement section
    assert "### 4. Requirements Refinement" in content, "Refinement section header not found"
    assert "Purpose**: Iterative improvement" in content, "Refinement purpose not found"
    assert "Method**: Completeness scoring" in content, "Refinement method not found"
    assert "Output**: Refined epics/features" in content, "Refinement output not found"
    assert "Commands**: `/epic-refine`, `/feature-refine`" in content, "Refinement commands not found"
    print("✓ Requirements Refinement component section present")


def test_development_flow_updated():
    """Verify development flow includes refinement step."""
    file_path = Path("installer/global/instructions/core/00-overview.md")
    content = file_path.read_text()

    # Check for updated flow
    assert "Refinement (Completeness scoring & targeted questions)" in content, \
        "Refinement step not in development flow"
    assert "Graphiti Sync (Optional knowledge graph integration)" in content, \
        "Graphiti sync not in development flow"
    print("✓ Development flow updated with refinement step")


def test_three_organisation_patterns():
    """Verify all three organisation patterns are documented."""
    file_path = Path("installer/global/instructions/core/00-overview.md")
    content = file_path.read_text()

    # Check for organization patterns section
    assert "### Three Organisation Patterns" in content, \
        "Three Organisation Patterns section not found"

    # Check for all three patterns
    assert "#### 1. Direct Pattern" in content, "Direct Pattern section not found"
    assert "#### 2. Features Pattern" in content, "Features Pattern section not found"
    assert "#### 3. Mixed Pattern" in content, "Mixed Pattern section not found"

    # Check for pattern descriptions
    assert "Simple epics with tasks directly attached" in content, \
        "Direct pattern description not found"
    assert "Complex epics organized through features" in content, \
        "Features pattern description not found"
    assert "Combination of direct tasks and features" in content, \
        "Mixed pattern description not found"

    # Check for when to use guidance
    assert "**When to use**: Small epics with 3-5 focused tasks" in content, \
        "Direct pattern when-to-use not found"
    assert "**When to use**: Large epics requiring logical grouping (default)" in content, \
        "Features pattern when-to-use not found"
    assert "**When to use**: Evolving epics transitioning between patterns" in content, \
        "Mixed pattern when-to-use not found"

    print("✓ All three organisation patterns documented")


def test_new_commands_listed():
    """Verify new commands are in the Available Commands section."""
    file_path = Path("installer/global/instructions/core/00-overview.md")
    content = file_path.read_text()

    # Check for new commands
    assert "/epic-refine" in content, "/epic-refine command not found"
    assert "/feature-refine" in content, "/feature-refine command not found"
    assert "/requirekit-sync" in content, "/requirekit-sync command not found"

    # Check they're in the commands section
    commands_section = content[content.find("## Available Commands"):]
    assert "/epic-refine" in commands_section, "/epic-refine not in Available Commands section"
    assert "/feature-refine" in commands_section, "/feature-refine not in Available Commands section"
    assert "/requirekit-sync" in commands_section, "/requirekit-sync not in Available Commands section"

    # Check for Integration Commands section
    assert "### Integration Commands" in content, "Integration Commands section not found"

    print("✓ All new commands listed in Available Commands")


def test_new_principle_added():
    """Verify the Iterative Refinement principle is added."""
    file_path = Path("installer/global/instructions/core/00-overview.md")
    content = file_path.read_text()

    # Check for new principle
    assert "### 6. Iterative Refinement" in content, \
        "Iterative Refinement principle header not found"
    assert "Requirements improve through structured feedback and completeness scoring" in content, \
        "Iterative Refinement principle description not found"

    print("✓ Iterative Refinement principle added")


def test_state_management_renumbered():
    """Verify State Management section renumbered to 5."""
    file_path = Path("installer/global/instructions/core/00-overview.md")
    content = file_path.read_text()

    # Check that State Management is now section 5
    assert "### 5. State Management" in content, \
        "State Management not renumbered to section 5"

    print("✓ State Management correctly renumbered")


def test_command_descriptions():
    """Verify command descriptions are present."""
    file_path = Path("installer/global/instructions/core/00-overview.md")
    content = file_path.read_text()

    # Check for command descriptions
    assert "Refine existing epics with completeness scoring" in content, \
        "/epic-refine description not found"
    assert "Refine existing features with targeted questions" in content, \
        "/feature-refine description not found"
    assert "Sync epics/features to Graphiti knowledge graph" in content, \
        "/requirekit-sync description not found"

    print("✓ All command descriptions present")


def run_all_tests():
    """Run all tests and report results."""
    tests = [
        test_file_exists,
        test_file_is_valid_markdown,
        test_refinement_component_section,
        test_development_flow_updated,
        test_three_organisation_patterns,
        test_new_commands_listed,
        test_new_principle_added,
        test_state_management_renumbered,
        test_command_descriptions,
    ]

    print("Running TASK-RK01-010 tests...\n")

    passed = 0
    failed = 0
    errors = []

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            failed += 1
            errors.append(f"FAILED: {test.__name__}: {str(e)}")
        except Exception as e:
            failed += 1
            errors.append(f"ERROR: {test.__name__}: {str(e)}")

    print(f"\n{'='*60}")
    print(f"Test Results: {passed} passed, {failed} failed")
    print(f"{'='*60}")

    if errors:
        print("\nFailures:")
        for error in errors:
            print(f"  {error}")
        return 1

    print("\n✅ All tests passed!")
    return 0


if __name__ == "__main__":
    exit(run_all_tests())
