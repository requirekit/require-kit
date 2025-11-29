#!/usr/bin/env python3
"""
Test Suite: Import Validation
Tests all relative imports work correctly in repository context.
"""
import sys
import importlib
import importlib.util
from pathlib import Path
from typing import List, Tuple, Dict


class TestImportValidation:
    """Validate imports work correctly."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent
        self.lib_dir = self.repo_root / "installer" / "global" / "lib"
        self.errors = []
        self.warnings = []

        # Add lib directory to Python path for testing
        sys.path.insert(0, str(self.lib_dir))

    def get_modules_to_test(self) -> List[Dict[str, str]]:
        """Get list of modules with their expected imports."""
        return [
            {
                'name': 'config.plan_review_config',
                'file': 'config/plan_review_config.py',
                'imports': ['.defaults', '.config_schema', 'utils']
            },
            {
                'name': 'metrics.metrics_storage',
                'file': 'metrics/metrics_storage.py',
                'imports': ['utils']
            },
            {
                'name': 'metrics.plan_review_dashboard',
                'file': 'metrics/plan_review_dashboard.py',
                'imports': ['.metrics_storage', 'config']
            },
            {
                'name': 'metrics.plan_review_metrics',
                'file': 'metrics/plan_review_metrics.py',
                'imports': ['.metrics_storage', 'config']
            },
            {
                'name': 'config',
                'file': 'config/__init__.py',
                'imports': ['.plan_review_config', '.config_schema', '.defaults']
            },
            {
                'name': 'metrics',
                'file': 'metrics/__init__.py',
                'imports': ['.plan_review_metrics', '.plan_review_dashboard']
            },
            {
                'name': 'utils',
                'file': 'utils/__init__.py',
                'imports': ['.json_serializer', '.file_operations', '.path_resolver']
            }
        ]

    def test_module_import(self, module_info: Dict[str, str]) -> Tuple[bool, str]:
        """
        Test if a module can be imported.

        Args:
            module_info: Module information dict

        Returns:
            Tuple of (success, error_message)
        """
        module_name = module_info['name']
        file_path = self.lib_dir / module_info['file']

        if not file_path.exists():
            return False, f"File not found: {module_info['file']}"

        try:
            # Try to import the module
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None or spec.loader is None:
                return False, f"Could not load spec for {module_name}"

            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            return True, ""
        except ImportError as e:
            return False, f"Import error: {e}"
        except Exception as e:
            return False, f"Error loading module: {e}"

    def test_relative_imports(self) -> bool:
        """
        Test that all relative imports resolve correctly.

        Returns:
            True if all tests pass
        """
        modules = self.get_modules_to_test()

        print(f"\n{'='*80}")
        print(f"Import Validation Tests")
        print(f"{'='*80}")
        print(f"Testing {len(modules)} modules...\n")

        passed = 0
        failed = 0

        for module_info in modules:
            success, error = self.test_module_import(module_info)

            if success:
                print(f"  ✓ {module_info['name']}")
                passed += 1
            else:
                print(f"  ✗ {module_info['name']}")
                print(f"    Error: {error}")
                self.errors.append(f"{module_info['name']}: {error}")
                failed += 1

        print(f"\n{'-'*80}")
        print(f"Results: {passed} passed, {failed} failed")
        print(f"{'-'*80}\n")

        return failed == 0


def main():
    """Main test runner."""
    tester = TestImportValidation()

    if tester.test_relative_imports():
        print("✓ All import validation tests passed")
        return 0
    else:
        print("\n✗ Import validation FAILED")
        print("\nErrors:")
        for error in tester.errors:
            print(f"  - {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
