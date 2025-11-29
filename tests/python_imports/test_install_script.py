#!/usr/bin/env python3
"""
Test Suite: Installation Script Validation
Verifies install.sh copies lib files correctly.
"""
import subprocess
import tempfile
import shutil
import sys
from pathlib import Path
from typing import List, Tuple


class TestInstallScript:
    """Test installation script functionality."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent
        self.install_script = self.repo_root / "installer" / "scripts" / "install.sh"
        self.lib_dir = self.repo_root / "installer" / "global" / "lib"
        self.errors = []
        self.warnings = []

    def test_script_exists(self) -> Tuple[bool, str]:
        """Test that install script exists and is executable."""
        if not self.install_script.exists():
            return False, f"Install script not found at {self.install_script}"

        if not self.install_script.is_file():
            return False, f"Install script is not a file: {self.install_script}"

        # Check if script is executable (on Unix systems)
        if not self.install_script.stat().st_mode & 0o111:
            return False, f"Install script is not executable"

        return True, ""

    def test_lib_directory_structure(self) -> Tuple[bool, str]:
        """Test that lib directory has expected structure."""
        expected_dirs = ['config', 'metrics', 'utils']
        missing_dirs = []

        for dir_name in expected_dirs:
            dir_path = self.lib_dir / dir_name
            if not dir_path.is_dir():
                missing_dirs.append(dir_name)

        if missing_dirs:
            return False, f"Missing lib subdirectories: {', '.join(missing_dirs)}"

        return True, ""

    def test_lib_files_exist(self) -> Tuple[bool, List[str]]:
        """Test that all expected lib files exist."""
        expected_files = [
            'feature_detection.py',
            'config/__init__.py',
            'config/plan_review_config.py',
            'config/config_schema.py',
            'config/defaults.py',
            'metrics/__init__.py',
            'metrics/metrics_storage.py',
            'metrics/plan_review_dashboard.py',
            'metrics/plan_review_metrics.py',
            'utils/__init__.py',
            'utils/json_serializer.py',
            'utils/file_operations.py',
            'utils/path_resolver.py',
        ]

        missing_files = []
        for file_path in expected_files:
            full_path = self.lib_dir / file_path
            if not full_path.exists():
                missing_files.append(file_path)

        return len(missing_files) == 0, missing_files

    def test_install_script_syntax(self) -> Tuple[bool, str]:
        """Test that install script has valid bash syntax."""
        try:
            result = subprocess.run(
                ['bash', '-n', str(self.install_script)],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode != 0:
                return False, f"Bash syntax error: {result.stderr}"

            return True, ""
        except subprocess.TimeoutExpired:
            return False, "Script syntax check timed out"
        except Exception as e:
            return False, f"Error checking script syntax: {e}"

    def test_install_function_exists(self) -> Tuple[bool, str]:
        """Test that install_lib function exists in script."""
        try:
            with open(self.install_script, 'r') as f:
                content = f.read()

            if 'install_lib()' not in content:
                return False, "install_lib function not found in script"

            if 'feature_detection.py' not in content:
                return False, "Script does not reference feature_detection.py"

            return True, ""
        except Exception as e:
            return False, f"Error reading install script: {e}"

    def test_validate_function_exists(self) -> Tuple[bool, str]:
        """Test that validate_installation function exists in script."""
        try:
            with open(self.install_script, 'r') as f:
                content = f.read()

            if 'validate_installation()' not in content:
                return False, "validate_installation function not found in script"

            return True, ""
        except Exception as e:
            return False, f"Error reading install script: {e}"

    def test_validate_function_content(self) -> Tuple[bool, str]:
        """Test that validate_installation function has expected content."""
        try:
            with open(self.install_script, 'r') as f:
                content = f.read()

            # Check for Python import test
            if 'from lib.feature_detection import detect_packages' not in content:
                return False, "Validation does not test feature_detection import"

            # Check for proper error handling
            if 'Python module validation failed' not in content:
                return False, "Validation missing proper error message"

            # Check for exit on failure
            if 'exit 1' not in content:
                return False, "Validation does not exit with error code on failure"

            # Check for Python 3 check
            if 'command -v python3' not in content:
                return False, "Validation does not check for Python 3"

            return True, ""
        except Exception as e:
            return False, f"Error reading install script: {e}"

    def test_validate_called_in_main(self) -> Tuple[bool, str]:
        """Test that validate_installation is called in main flow."""
        try:
            with open(self.install_script, 'r') as f:
                content = f.read()

            # Find the main() function
            main_start = content.find('main() {')
            if main_start == -1:
                return False, "main() function not found"

            main_end = content.find('}', main_start)
            main_content = content[main_start:main_end]

            if 'validate_installation' not in main_content:
                return False, "validate_installation not called in main()"

            # Check it's called before completion message
            verify_pos = main_content.find('verify_installation')
            validate_pos = main_content.find('validate_installation')
            complete_pos = main_content.find('print_completion_message')

            if verify_pos == -1 or validate_pos == -1 or complete_pos == -1:
                return False, "Cannot find all required function calls in main()"

            if not (verify_pos < validate_pos < complete_pos):
                return False, "validate_installation not called in correct order (should be after verify, before completion)"

            return True, ""
        except Exception as e:
            return False, f"Error analyzing main() function: {e}"

    def run_all_tests(self) -> bool:
        """
        Run all installation script tests.

        Returns:
            True if all tests pass
        """
        print(f"\n{'='*80}")
        print(f"Installation Script Tests")
        print(f"{'='*80}\n")

        tests = [
            ("Script exists and executable", self.test_script_exists),
            ("Lib directory structure", self.test_lib_directory_structure),
            ("Bash syntax validation", self.test_install_script_syntax),
            ("install_lib function exists", self.test_install_function_exists),
            ("validate_installation function exists", self.test_validate_function_exists),
            ("validate_installation function content", self.test_validate_function_content),
            ("validate_installation called in main", self.test_validate_called_in_main),
        ]

        passed = 0
        failed = 0

        for test_name, test_func in tests:
            success, error = test_func()

            if success:
                print(f"  ✓ {test_name}")
                passed += 1
            else:
                print(f"  ✗ {test_name}")
                print(f"    Error: {error}")
                self.errors.append(f"{test_name}: {error}")
                failed += 1

        # Special test for file existence (returns list)
        print(f"  Testing lib files existence...")
        success, missing_files = self.test_lib_files_exist()
        if success:
            print(f"  ✓ All lib files exist")
            passed += 1
        else:
            print(f"  ✗ Missing lib files:")
            for file_path in missing_files:
                print(f"    - {file_path}")
            self.errors.append(f"Missing files: {', '.join(missing_files)}")
            failed += 1

        print(f"\n{'-'*80}")
        print(f"Results: {passed} passed, {failed} failed")
        print(f"{'-'*80}\n")

        return failed == 0


def main():
    """Main test runner."""
    tester = TestInstallScript()

    if tester.run_all_tests():
        print("✓ All installation script tests passed")
        return 0
    else:
        print("\n✗ Installation script tests FAILED")
        print("\nErrors:")
        for error in tester.errors:
            print(f"  - {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
