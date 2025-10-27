"""
Integration test configuration and shared fixtures.

This module provides configuration and fixtures specific to integration testing,
including test isolation, mock setup, and common test utilities.

Architecture:
    - Test isolation via tmp_path fixtures
    - Shared mock configurations
    - Integration-specific pytest markers
    - Cross-test utility functions

Usage:
    pytest tests/integration/ -v --integration
"""

import pytest
import sys
from pathlib import Path
from typing import Dict, Any
from unittest.mock import Mock, patch

# Add installer lib to path for imports
installer_lib_path = Path(__file__).parent.parent.parent / "installer" / "global" / "commands" / "lib"
if installer_lib_path.exists() and str(installer_lib_path) not in sys.path:
    sys.path.insert(0, str(installer_lib_path))

# Import test fixtures from other modules
from tests.fixtures.data_fixtures import *  # noqa: F403, F401
from tests.fixtures.mock_fixtures import *  # noqa: F403, F401
from tests.fixtures.factory_fixtures import *  # noqa: F403, F401


def pytest_configure(config):
    """Register custom markers for integration tests."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running (>1 second)"
    )
    config.addinivalue_line(
        "markers", "workflow: mark test as workflow integration test"
    )


@pytest.fixture
def isolated_task_dir(tmp_path):
    """
    Create isolated task directory structure for integration tests.

    Provides temporary directory with tasks/ structure for file-based tests.

    Args:
        tmp_path: pytest's tmp_path fixture

    Returns:
        Path: Root of task directory structure

    Example:
        >>> task_dir = isolated_task_dir(tmp_path)
        >>> task_file = task_dir / "tasks" / "in_progress" / "TASK-001.md"
    """
    # Create directory structure
    task_root = tmp_path / "tasks"
    (task_root / "backlog").mkdir(parents=True)
    (task_root / "in_progress").mkdir(parents=True)
    (task_root / "in_review").mkdir(parents=True)
    (task_root / "completed").mkdir(parents=True)

    # Create .plan_versions directory for version management
    (tmp_path / ".plan_versions").mkdir(parents=True)

    return tmp_path


@pytest.fixture
def mock_countdown_timer():
    """
    Mock countdown timer for quick review testing.

    Returns a configurable mock that simulates countdown_timer behavior
    without actual delays, enabling fast test execution.

    Returns:
        Mock: Configured countdown timer mock

    Example:
        >>> timer = mock_countdown_timer()
        >>> timer.return_value = "timeout"
        >>> result = some_function_using_timer()
    """
    mock_timer = Mock()
    mock_timer.return_value = "timeout"  # Default to timeout
    return mock_timer


@pytest.fixture
def mock_user_input_sequence():
    """
    Mock user input sequence for interactive testing.

    Returns a factory that creates mock input handlers with predefined
    input sequences for testing interactive workflows.

    Returns:
        callable: Factory function that creates input mocks

    Example:
        >>> input_mock = mock_user_input_sequence(['a', 'y'])
        >>> with patch('builtins.input', side_effect=input_mock):
        ...     # Test interactive flow
    """
    def _create_input_mock(sequence):
        """Create mock with input sequence."""
        return Mock(side_effect=sequence)

    return _create_input_mock


@pytest.fixture
def integration_task_metadata():
    """
    Standard task metadata for integration tests.

    Provides consistent task metadata structure across integration tests.

    Returns:
        Dict[str, Any]: Task metadata dictionary

    Example:
        >>> metadata = integration_task_metadata()
        >>> assert metadata['id'] == 'TASK-INT-001'
    """
    return {
        'id': 'TASK-INT-001',
        'title': 'Integration test task',
        'status': 'in_progress',
        'created': '2025-10-10T00:00:00Z',
        'updated': '2025-10-10T00:00:00Z',
        'assignee': 'test_user',
        'priority': 'medium',
        'requirements': ['REQ-INT-001', 'REQ-INT-002'],
        'technology_stack': 'Python',
    }


@pytest.fixture
def integration_task_file(isolated_task_dir, integration_task_metadata):
    """
    Create integration test task file with metadata.

    Creates a complete task markdown file with frontmatter and content
    for file-based integration testing.

    Args:
        isolated_task_dir: Isolated task directory fixture
        integration_task_metadata: Task metadata fixture

    Returns:
        Path: Path to created task file

    Example:
        >>> task_file = integration_task_file(isolated_task_dir, integration_task_metadata)
        >>> assert task_file.exists()
    """
    import yaml

    task_id = integration_task_metadata['id']
    task_file = isolated_task_dir / "tasks" / "in_progress" / f"{task_id}.md"

    # Create frontmatter
    frontmatter = yaml.dump(integration_task_metadata, default_flow_style=False)

    # Create content
    content = f"""---
{frontmatter}---

# {integration_task_metadata['title']}

## Description
Integration test task for workflow testing.

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Implementation Notes
Test notes for integration testing.
"""

    task_file.write_text(content, encoding='utf-8')
    return task_file


@pytest.fixture
def workflow_test_context(
    isolated_task_dir,
    integration_task_metadata,
    integration_task_file
):
    """
    Complete workflow test context with all dependencies.

    Bundles all common workflow test dependencies into a single fixture
    for convenience in integration tests.

    Args:
        isolated_task_dir: Isolated task directory
        integration_task_metadata: Task metadata
        integration_task_file: Task file path

    Returns:
        Dict[str, Any]: Context dictionary with all dependencies

    Example:
        >>> context = workflow_test_context(...)
        >>> task_file = context['task_file']
        >>> metadata = context['metadata']
    """
    return {
        'task_dir': isolated_task_dir,
        'metadata': integration_task_metadata,
        'task_file': integration_task_file,
        'task_id': integration_task_metadata['id'],
    }


# Pytest configuration for integration tests
def pytest_collection_modifyitems(config, items):
    """
    Automatically mark integration tests and configure test ordering.

    Adds 'integration' marker to all tests in integration/ directory.
    """
    integration_path = Path(__file__).parent
    for item in items:
        if str(integration_path) in str(item.fspath):
            item.add_marker(pytest.mark.integration)
