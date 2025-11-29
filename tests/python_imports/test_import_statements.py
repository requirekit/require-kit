#!/usr/bin/env python3
"""
Test Suite: Import Statement Validation
Validates import statements are correctly formatted (relative vs absolute).
"""
import ast
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Set


class TestImportStatements:
    """Validate import statements in modified files."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent.parent.parent
        self.lib_dir = self.repo_root / "installer" / "global" / "lib"
        self.errors = []
        self.warnings = []

        # Files modified in TASK-FIX-D2C0 and TASK-FIX-3196
        self.modified_files = [
            'config/plan_review_config.py',
            'metrics/metrics_storage.py',
            'metrics/plan_review_dashboard.py',
            'metrics/plan_review_metrics.py',
        ]

    def parse_imports(self, file_path: Path) -> Dict[str, List[str]]:
        """
        Parse import statements from a Python file.

        Args:
            file_path: Path to Python file

        Returns:
            Dict with 'relative' and 'absolute' import lists
        """
        imports = {
            'relative': [],
            'absolute': [],
            'from_relative': [],
            'from_absolute': []
        }

        try:
            with open(file_path, 'r') as f:
                tree = ast.parse(f.read(), filename=str(file_path))

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports['absolute'].append(alias.name)

                elif isinstance(node, ast.ImportFrom):
                    if node.level > 0:
                        # Relative import
                        module = node.module or ''
                        imports['from_relative'].append(f"{'.' * node.level}{module}")
                    else:
                        # Absolute import
                        if node.module:
                            imports['from_absolute'].append(node.module)

        except Exception as e:
            self.warnings.append(f"Could not parse {file_path.name}: {e}")

        return imports

    def test_file_imports(self, rel_path: str) -> Tuple[bool, List[str]]:
        """
        Test imports in a single file.

        Args:
            rel_path: Relative path from lib_dir

        Returns:
            Tuple of (success, messages)
        """
        file_path = self.lib_dir / rel_path
        if not file_path.exists():
            return False, [f"File not found: {rel_path}"]

        messages = []
        imports = self.parse_imports(file_path)

        # Define expected patterns for each file
        # TASK-FIX-3196: All cross-package imports must use RELATIVE imports
        expected_imports = {
            'config/plan_review_config.py': {
                'relative': ['.defaults', '.config_schema', '..utils'],
            },
            'metrics/metrics_storage.py': {
                'relative': ['..utils'],
            },
            'metrics/plan_review_dashboard.py': {
                'relative': ['.metrics_storage', '..config'],
            },
            'metrics/plan_review_metrics.py': {
                'relative': ['.metrics_storage', '..config'],
            },
        }

        expected = expected_imports.get(rel_path, {})

        # Check for expected relative imports
        for expected_import in expected.get('relative', []):
            if expected_import not in imports['from_relative']:
                messages.append(f"Missing expected relative import: from {expected_import}")

        # Verify no incorrect absolute imports for cross-package dependencies
        # Cross-package imports (utils, config, metrics) must be relative
        package = rel_path.split('/')[0]  # 'config' or 'metrics'

        for imp in imports['from_absolute']:
            # Check if importing from lib packages (should be relative)
            if imp in ['utils', 'config', 'metrics'] or \
               imp.startswith('utils.') or \
               imp.startswith('config.') or \
               imp.startswith('metrics.'):
                messages.append(f"Should use relative import instead of absolute: from {imp}")

        return len(messages) == 0, messages

    def run_all_tests(self) -> bool:
        """
        Run import validation on all modified files.

        Returns:
            True if all tests pass
        """
        print(f"\n{'='*80}")
        print(f"Import Statement Validation")
        print(f"{'='*80}")
        print(f"Validating imports in {len(self.modified_files)} modified files...\n")

        passed = 0
        failed = 0

        for file_path in self.modified_files:
            success, messages = self.test_file_imports(file_path)

            if success:
                print(f"  ✓ {file_path}")
                passed += 1
            else:
                print(f"  ✗ {file_path}")
                for msg in messages:
                    print(f"    - {msg}")
                self.errors.extend(messages)
                failed += 1

        print(f"\n{'-'*80}")
        print(f"Results: {passed} passed, {failed} failed")
        print(f"{'-'*80}\n")

        if self.warnings:
            print("Warnings:")
            for warning in self.warnings:
                print(f"  - {warning}")

        return failed == 0


def main():
    """Main test runner."""
    tester = TestImportStatements()

    if tester.run_all_tests():
        print("✓ All import statement validation tests passed")
        return 0
    else:
        print("\n✗ Import statement validation FAILED")
        print("\nErrors:")
        for error in tester.errors:
            print(f"  - {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
