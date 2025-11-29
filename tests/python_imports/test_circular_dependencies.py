#!/usr/bin/env python3
"""
Test Suite: Circular Dependency Detection
Verifies no circular imports exist in the codebase.
"""
import ast
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


class TestCircularDependencies:
    """Detect circular import dependencies."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent
        self.lib_dir = self.repo_root / "installer" / "global" / "lib"
        self.errors = []
        self.import_graph: Dict[str, Set[str]] = {}

    def extract_imports(self, file_path: Path) -> Set[str]:
        """
        Extract all imports from a Python file.

        Args:
            file_path: Path to Python file

        Returns:
            Set of imported module names
        """
        imports = set()

        try:
            with open(file_path, 'r') as f:
                tree = ast.parse(f.read(), filename=str(file_path))

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        if node.level > 0:
                            # Relative import
                            imports.add(self._resolve_relative_import(file_path, node.module, node.level))
                        else:
                            imports.add(node.module.split('.')[0])
        except Exception as e:
            print(f"  Warning: Could not parse {file_path.name}: {e}")

        return imports

    def _resolve_relative_import(self, file_path: Path, module: str, level: int) -> str:
        """
        Resolve relative import to absolute module name.

        Args:
            file_path: File containing the import
            module: Module name from import
            level: Number of dots in relative import

        Returns:
            Resolved module name
        """
        # Get the package path relative to lib_dir
        rel_path = file_path.parent.relative_to(self.lib_dir)

        # Go up 'level' directories
        parts = list(rel_path.parts)
        if level > 1:
            parts = parts[:-(level-1)] if len(parts) >= (level-1) else []

        if module:
            parts.append(module.split('.')[0])

        return '.'.join(parts) if parts else 'lib'

    def build_import_graph(self) -> None:
        """Build graph of module dependencies."""
        python_files = list(self.lib_dir.rglob("*.py"))

        for py_file in python_files:
            if py_file.name == '__init__.py':
                # Use directory name as module name
                module_name = py_file.parent.relative_to(self.lib_dir).as_posix().replace('/', '.')
            else:
                # Use file name (without .py) as module name
                rel_path = py_file.relative_to(self.lib_dir)
                module_name = str(rel_path.with_suffix('')).replace('/', '.')

            imports = self.extract_imports(py_file)

            # Filter to only lib imports
            lib_imports = {imp for imp in imports if imp in ['config', 'metrics', 'utils']}

            self.import_graph[module_name] = lib_imports

    def detect_circular_imports(self) -> List[List[str]]:
        """
        Detect circular dependencies using DFS.

        Returns:
            List of circular dependency chains
        """
        cycles = []
        visited = set()
        rec_stack = set()

        def dfs(node: str, path: List[str]) -> None:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in self.import_graph.get(node, set()):
                if neighbor not in visited:
                    dfs(neighbor, path.copy())
                elif neighbor in rec_stack:
                    # Found a cycle
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    if cycle not in cycles:
                        cycles.append(cycle)

            rec_stack.remove(node)

        for node in self.import_graph:
            if node not in visited:
                dfs(node, [])

        return cycles

    def run_all_tests(self) -> bool:
        """
        Run circular dependency detection.

        Returns:
            True if no circular dependencies found
        """
        print(f"\n{'='*80}")
        print(f"Circular Dependency Detection")
        print(f"{'='*80}\n")

        print("Building import graph...")
        self.build_import_graph()

        print(f"Analyzing {len(self.import_graph)} modules...")

        cycles = self.detect_circular_imports()

        if cycles:
            print(f"\n✗ Found {len(cycles)} circular dependencies:\n")
            for i, cycle in enumerate(cycles, 1):
                print(f"  {i}. {' -> '.join(cycle)}")
                self.errors.append(f"Circular dependency: {' -> '.join(cycle)}")
            return False
        else:
            print("\n✓ No circular dependencies detected")
            return True


def main():
    """Main test runner."""
    tester = TestCircularDependencies()

    if tester.run_all_tests():
        print("\n✓ All circular dependency tests passed")
        return 0
    else:
        print("\n✗ Circular dependency detection FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
