#!/usr/bin/env python3
"""
Test Suite: Python Syntax Validation
Tests all Python files have valid syntax and compile successfully.
"""
import py_compile
import os
import sys
from pathlib import Path
from typing import List, Tuple


class TestSyntaxValidation:
    """Validate Python syntax across all library files."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent
        self.lib_dir = self.repo_root / "installer" / "global" / "lib"
        self.errors = []
        self.warnings = []

    def get_python_files(self) -> List[Path]:
        """Get all Python files in lib directory."""
        return list(self.lib_dir.rglob("*.py"))

    def test_file_syntax(self, file_path: Path) -> Tuple[bool, str]:
        """
        Test if a Python file has valid syntax.

        Args:
            file_path: Path to Python file

        Returns:
            Tuple of (success, error_message)
        """
        try:
            # Attempt to compile the file
            py_compile.compile(str(file_path), doraise=True)
            return True, ""
        except py_compile.PyCompileError as e:
            error_msg = f"Syntax error in {file_path.relative_to(self.repo_root)}: {e}"
            return False, error_msg
        except Exception as e:
            error_msg = f"Compilation error in {file_path.relative_to(self.repo_root)}: {e}"
            return False, error_msg

    def run_all_tests(self) -> bool:
        """
        Run syntax validation on all Python files.

        Returns:
            True if all tests pass
        """
        python_files = self.get_python_files()

        if not python_files:
            self.warnings.append("No Python files found to test")
            return False

        print(f"\n{'='*80}")
        print(f"Python Syntax Validation")
        print(f"{'='*80}")
        print(f"Testing {len(python_files)} Python files...\n")

        passed = 0
        failed = 0

        for py_file in sorted(python_files):
            rel_path = py_file.relative_to(self.repo_root)
            success, error = self.test_file_syntax(py_file)

            if success:
                print(f"  ✓ {rel_path}")
                passed += 1
            else:
                print(f"  ✗ {rel_path}")
                print(f"    Error: {error}")
                self.errors.append(error)
                failed += 1

        print(f"\n{'-'*80}")
        print(f"Results: {passed} passed, {failed} failed")
        print(f"{'-'*80}\n")

        return failed == 0


def main():
    """Main test runner."""
    tester = TestSyntaxValidation()

    if tester.run_all_tests():
        print("✓ All syntax validation tests passed")
        return 0
    else:
        print("\n✗ Syntax validation FAILED")
        print("\nErrors:")
        for error in tester.errors:
            print(f"  - {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
