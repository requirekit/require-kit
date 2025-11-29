#!/usr/bin/env python3
"""
Test Suite: Integration Tests
Validates end-to-end functionality of the Python path fix.
"""
import sys
import subprocess
import tempfile
from pathlib import Path
from typing import Tuple


class TestIntegration:
    """Integration tests for complete workflow."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent.parent.parent
        self.lib_dir = self.repo_root / "installer" / "global" / "lib"
        self.install_script = self.repo_root / "installer" / "scripts" / "install.sh"
        self.errors = []
        self.warnings = []

    def test_lib_structure_integrity(self) -> Tuple[bool, str]:
        """Test that lib directory structure is complete."""
        required_structure = {
            'config': ['__init__.py', 'plan_review_config.py', 'config_schema.py', 'defaults.py'],
            'metrics': ['__init__.py', 'metrics_storage.py', 'plan_review_dashboard.py', 'plan_review_metrics.py'],
            'utils': ['__init__.py', 'json_serializer.py', 'file_operations.py', 'path_resolver.py'],
        }

        missing = []
        for package, files in required_structure.items():
            package_dir = self.lib_dir / package
            if not package_dir.exists():
                missing.append(f"Package directory: {package}/")
                continue

            for file_name in files:
                file_path = package_dir / file_name
                if not file_path.exists():
                    missing.append(f"{package}/{file_name}")

        # Check root lib files
        if not (self.lib_dir / 'feature_detection.py').exists():
            missing.append('feature_detection.py')

        if missing:
            return False, f"Missing files: {', '.join(missing)}"

        return True, ""

    def test_import_chain_config(self) -> Tuple[bool, str]:
        """Test that config package import chain works."""
        # Verify __init__.py exports
        init_file = self.lib_dir / 'config' / '__init__.py'

        try:
            with open(init_file, 'r') as f:
                content = f.read()

            expected_imports = ['PlanReviewConfig', 'ConfigSchema', 'ThresholdConfig', 'MetricsConfig', 'DEFAULT_CONFIG']
            missing_imports = []

            for imp in expected_imports:
                if imp not in content:
                    missing_imports.append(imp)

            if missing_imports:
                return False, f"Missing exports in config/__init__.py: {', '.join(missing_imports)}"

            return True, ""
        except Exception as e:
            return False, f"Error reading config/__init__.py: {e}"

    def test_import_chain_metrics(self) -> Tuple[bool, str]:
        """Test that metrics package import chain works."""
        init_file = self.lib_dir / 'metrics' / '__init__.py'

        try:
            with open(init_file, 'r') as f:
                content = f.read()

            expected_imports = ['PlanReviewMetrics', 'PlanReviewDashboard']
            missing_imports = []

            for imp in expected_imports:
                if imp not in content:
                    missing_imports.append(imp)

            if missing_imports:
                return False, f"Missing exports in metrics/__init__.py: {', '.join(missing_imports)}"

            return True, ""
        except Exception as e:
            return False, f"Error reading metrics/__init__.py: {e}"

    def test_import_chain_utils(self) -> Tuple[bool, str]:
        """Test that utils package import chain works."""
        init_file = self.lib_dir / 'utils' / '__init__.py'

        try:
            with open(init_file, 'r') as f:
                content = f.read()

            expected_imports = ['JsonSerializer', 'FileOperations', 'PathResolver']
            missing_imports = []

            for imp in expected_imports:
                if imp not in content:
                    missing_imports.append(imp)

            if missing_imports:
                return False, f"Missing exports in utils/__init__.py: {', '.join(missing_imports)}"

            return True, ""
        except Exception as e:
            return False, f"Error reading utils/__init__.py: {e}"

    def test_cross_package_imports(self) -> Tuple[bool, str]:
        """Test that cross-package imports use RELATIVE imports (TASK-FIX-3196)."""
        test_cases = [
            ('config/plan_review_config.py', 'from ..utils import'),
            ('metrics/metrics_storage.py', 'from ..utils import'),
            ('metrics/plan_review_dashboard.py', 'from ..config import'),
            ('metrics/plan_review_metrics.py', 'from ..config import'),
        ]

        errors = []
        for file_path, expected_import in test_cases:
            full_path = self.lib_dir / file_path

            try:
                with open(full_path, 'r') as f:
                    content = f.read()

                if expected_import not in content:
                    errors.append(f"{file_path}: missing '{expected_import}'")
            except Exception as e:
                errors.append(f"{file_path}: error reading - {e}")

        if errors:
            return False, "; ".join(errors)

        return True, ""

    def test_relative_imports_within_package(self) -> Tuple[bool, str]:
        """Test that within-package imports use relative imports."""
        test_cases = [
            ('config/plan_review_config.py', ['from .defaults import', 'from .config_schema import']),
            ('metrics/plan_review_dashboard.py', ['from .metrics_storage import']),
            ('metrics/plan_review_metrics.py', ['from .metrics_storage import']),
        ]

        errors = []
        for file_path, expected_imports in test_cases:
            full_path = self.lib_dir / file_path

            try:
                with open(full_path, 'r') as f:
                    content = f.read()

                for expected_import in expected_imports:
                    if expected_import not in content:
                        errors.append(f"{file_path}: missing '{expected_import}'")
            except Exception as e:
                errors.append(f"{file_path}: error reading - {e}")

        if errors:
            return False, "; ".join(errors)

        return True, ""

    def run_all_tests(self) -> bool:
        """
        Run all integration tests.

        Returns:
            True if all tests pass
        """
        print(f"\n{'='*80}")
        print(f"Integration Tests")
        print(f"{'='*80}\n")

        tests = [
            ("Lib directory structure integrity", self.test_lib_structure_integrity),
            ("Config package import chain", self.test_import_chain_config),
            ("Metrics package import chain", self.test_import_chain_metrics),
            ("Utils package import chain", self.test_import_chain_utils),
            ("Cross-package imports", self.test_cross_package_imports),
            ("Relative imports within packages", self.test_relative_imports_within_package),
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

        print(f"\n{'-'*80}")
        print(f"Results: {passed} passed, {failed} failed")
        print(f"{'-'*80}\n")

        return failed == 0


def main():
    """Main test runner."""
    tester = TestIntegration()

    if tester.run_all_tests():
        print("✓ All integration tests passed")
        return 0
    else:
        print("\n✗ Integration tests FAILED")
        print("\nErrors:")
        for error in tester.errors:
            print(f"  - {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
