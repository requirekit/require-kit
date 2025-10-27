"""
Boundary condition test fixtures for TASK-003E Phase 5 Day 3.

This module provides reusable fixtures for testing boundary conditions and
edge cases in the complexity evaluation and pager display systems.

Fixtures:
    - empty_plan: Plan with all None/empty values
    - minimal_task: Task with 0 files and 0 dependencies
    - maximum_task: Task with 100+ files and 50+ dependencies
    - boundary_file_counts: Parametrized file count boundaries (0, 1, 50, 100)
    - boundary_dependency_counts: Parametrized dependency boundaries (0, 1, 10, 50)

Usage:
    >>> from tests.fixtures.boundary_helpers import empty_plan, minimal_task
    >>> def test_empty_plan(empty_plan):
    ...     assert empty_plan["overview"] is None
"""

import pytest
from typing import Dict, Any, List


@pytest.fixture
def empty_plan() -> Dict[str, Any]:
    """
    Implementation plan with all None/empty values.

    Simulates edge case where planning agent produces incomplete plan
    or all sections are missing.

    Returns:
        Dict with all plan sections set to None

    Example:
        >>> def test_empty_plan_display(empty_plan):
        ...     # All sections should display user-friendly messages
        ...     assert empty_plan["overview"] is None
        ...     assert empty_plan["architecture"] is None
    """
    return {
        "task_id": "TASK-EMPTY-001",
        "overview": None,
        "architecture": None,
        "dependencies": None,
        "testing": None,
        "steps": None,
        "files_to_create": [],
        "external_dependencies": [],
        "phases": None,
        "raw_plan": None,
        "test_summary": None,
        "risk_details": None,
        "estimated_loc": None,
        "estimated_duration": None,
    }


@pytest.fixture
def whitespace_plan() -> Dict[str, Any]:
    """
    Implementation plan with whitespace-only values.

    Tests that whitespace-only sections are treated as empty
    and display user-friendly messages.

    Returns:
        Dict with whitespace-only plan sections

    Example:
        >>> def test_whitespace_treated_as_empty(whitespace_plan):
        ...     assert whitespace_plan["overview"].strip() == ""
    """
    return {
        "task_id": "TASK-WHITESPACE-001",
        "overview": "   ",
        "architecture": "\n\n\n",
        "dependencies": "\t\t\t",
        "testing": "  \n  \t  ",
        "steps": "",
        "files_to_create": [],
        "external_dependencies": [],
        "phases": ["   ", "\n"],  # Whitespace-only phases
        "raw_plan": "   \n   ",
        "test_summary": "",
        "risk_details": [],
        "estimated_loc": None,
        "estimated_duration": None,
    }


@pytest.fixture
def partial_empty_plan() -> Dict[str, Any]:
    """
    Implementation plan with mix of None and populated sections.

    Tests that display logic correctly handles some sections being None
    while others have valid content.

    Returns:
        Dict with mixed None/populated sections

    Example:
        >>> def test_partial_empty_sections(partial_empty_plan):
        ...     assert partial_empty_plan["overview"] is not None
        ...     assert partial_empty_plan["architecture"] is None
    """
    return {
        "task_id": "TASK-PARTIAL-001",
        "overview": "Simple task to fix validation bug",
        "architecture": None,  # None
        "dependencies": "No external dependencies",
        "testing": None,  # None
        "steps": "1. Fix validator\n2. Add tests",
        "files_to_create": ["src/validators/user_validator.py"],
        "external_dependencies": [],
        "phases": None,  # None
        "raw_plan": "Detailed plan content here...",
        "test_summary": None,  # None
        "risk_details": [],
        "estimated_loc": 50,
        "estimated_duration": "1 hour",
    }


@pytest.fixture
def minimal_task() -> Dict[str, Any]:
    """
    Task with absolute minimum values (0 files, 0 dependencies).

    Tests boundary condition where task has no files to create
    and no external dependencies.

    Returns:
        Dict representing minimal valid task

    Example:
        >>> def test_zero_files_minimum_score(minimal_task):
        ...     assert len(minimal_task["files_to_create"]) == 0
        ...     assert len(minimal_task["external_dependencies"]) == 0
    """
    return {
        "task_id": "TASK-MIN-001",
        "title": "Documentation update only",
        "files_to_create": [],  # 0 files
        "external_dependencies": [],  # 0 dependencies
        "patterns_used": [],
        "estimated_loc": 0,
        "risk_indicators": [],
        "raw_plan": "Update README.md with new section",
    }


@pytest.fixture
def single_file_task() -> Dict[str, Any]:
    """
    Task with exactly 1 file (boundary condition).

    Tests edge case of minimum non-zero file count.

    Returns:
        Dict representing single-file task

    Example:
        >>> def test_single_file_task(single_file_task):
        ...     assert len(single_file_task["files_to_create"]) == 1
    """
    return {
        "task_id": "TASK-SINGLE-001",
        "title": "Fix typo in config file",
        "files_to_create": ["config.yaml"],  # Exactly 1 file
        "external_dependencies": [],
        "patterns_used": ["configuration"],
        "estimated_loc": 10,
        "risk_indicators": [],
        "raw_plan": "Correct typo in configuration key",
    }


@pytest.fixture
def large_task() -> Dict[str, Any]:
    """
    Task with 50 files (high boundary condition).

    Tests upper boundary for file count before maximum cap.

    Returns:
        Dict representing large task with 50 files

    Example:
        >>> def test_large_file_count(large_task):
        ...     assert len(large_task["files_to_create"]) == 50
    """
    return {
        "task_id": "TASK-LARGE-001",
        "title": "Implement microservices architecture",
        "files_to_create": [f"services/service_{i}/handler.py" for i in range(50)],
        "external_dependencies": ["postgresql", "redis", "rabbitmq"],
        "patterns_used": ["microservices", "event_sourcing", "cqrs"],
        "estimated_loc": 5000,
        "risk_indicators": ["distributed_system", "data_consistency"],
        "raw_plan": "Large-scale microservices implementation",
    }


@pytest.fixture
def maximum_task() -> Dict[str, Any]:
    """
    Task with 100+ files and 50+ dependencies (maximum boundary).

    Tests edge case where task exceeds normal complexity caps.
    Complexity calculation should cap at maximum score (3 for file factor).

    Returns:
        Dict representing maximum complexity task

    Example:
        >>> def test_maximum_task_complexity_capped(maximum_task):
        ...     assert len(maximum_task["files_to_create"]) > 100
        ...     assert len(maximum_task["external_dependencies"]) > 50
    """
    return {
        "task_id": "TASK-MAX-001",
        "title": "Complete system rewrite",
        "files_to_create": [f"module_{i}/file_{j}.py" for i in range(40) for j in range(3)],  # 120 files
        "external_dependencies": [f"dependency-{i:03d}" for i in range(60)],  # 60 dependencies
        "patterns_used": [
            "mvc", "repository", "factory", "singleton", "observer",
            "strategy", "command", "mediator", "chain_of_responsibility"
        ],
        "estimated_loc": 15000,
        "risk_indicators": [
            "breaking_changes", "database_migration", "security_updates",
            "api_changes", "authentication_changes"
        ],
        "raw_plan": "Massive system rewrite with extensive changes",
    }


# Parametrized boundary value fixtures
@pytest.fixture(params=[0, 1, 50, 100])
def boundary_file_count(request) -> int:
    """
    Parametrized fixture for file count boundaries.

    Provides boundary values: 0 (minimum), 1 (edge), 50 (high), 100 (maximum)

    Returns:
        int: File count boundary value

    Example:
        >>> def test_file_count_boundaries(boundary_file_count):
        ...     task = create_task_with_files(boundary_file_count)
        ...     score = calculate_complexity(task)
        ...     assert score is not None
    """
    return request.param


@pytest.fixture(params=[0, 1, 10, 50])
def boundary_dependency_count(request) -> int:
    """
    Parametrized fixture for dependency count boundaries.

    Provides boundary values: 0 (minimum), 1 (edge), 10 (medium), 50 (maximum)

    Returns:
        int: Dependency count boundary value

    Example:
        >>> def test_dependency_boundaries(boundary_dependency_count):
        ...     task = create_task_with_deps(boundary_dependency_count)
        ...     score = calculate_complexity(task)
        ...     assert score is not None
    """
    return request.param


def create_task_with_file_count(file_count: int, task_id: str = "TASK-TEST") -> Dict[str, Any]:
    """
    Helper function to create task with specific file count.

    Args:
        file_count: Number of files to include
        task_id: Optional task identifier

    Returns:
        Dict representing task with specified file count

    Example:
        >>> task = create_task_with_file_count(25, "TASK-025")
        >>> assert len(task["files_to_create"]) == 25
    """
    return {
        "task_id": task_id,
        "title": f"Task with {file_count} files",
        "files_to_create": [f"file_{i}.py" for i in range(file_count)],
        "external_dependencies": [],
        "patterns_used": [],
        "estimated_loc": file_count * 50,
        "risk_indicators": [],
        "raw_plan": f"Task requiring {file_count} file modifications",
    }


def create_task_with_dependency_count(
    dependency_count: int,
    task_id: str = "TASK-TEST"
) -> Dict[str, Any]:
    """
    Helper function to create task with specific dependency count.

    Args:
        dependency_count: Number of dependencies to include
        task_id: Optional task identifier

    Returns:
        Dict representing task with specified dependency count

    Example:
        >>> task = create_task_with_dependency_count(15, "TASK-DEP-15")
        >>> assert len(task["external_dependencies"]) == 15
    """
    return {
        "task_id": task_id,
        "title": f"Task with {dependency_count} dependencies",
        "files_to_create": ["main.py"],
        "external_dependencies": [f"dep-{i:03d}" for i in range(dependency_count)],
        "patterns_used": [],
        "estimated_loc": 100,
        "risk_indicators": [],
        "raw_plan": f"Task with {dependency_count} external dependencies",
    }


# Module exports
__all__ = [
    "empty_plan",
    "whitespace_plan",
    "partial_empty_plan",
    "minimal_task",
    "single_file_task",
    "large_task",
    "maximum_task",
    "boundary_file_count",
    "boundary_dependency_count",
    "create_task_with_file_count",
    "create_task_with_dependency_count",
]
