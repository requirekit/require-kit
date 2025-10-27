"""
Mock object fixtures for complexity-based plan review testing.

This module provides mock implementations of system components
for isolated unit testing. Separated from data fixtures to maintain
single responsibility.

Architecture:
    - Mock file system: In-memory file operations
    - Mock task context: Evaluation context without I/O
    - Mock metrics storage: Test metrics collection
    - Mock user input: Simulated user interactions

Usage:
    >>> from tests.fixtures.mock_fixtures import mock_file_system
    >>> fs = mock_file_system()
    >>> fs.write(Path("test.txt"), "content")
"""

import pytest
import sys
import importlib.util
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from unittest.mock import Mock, MagicMock

# Try to import complexity models using importlib to avoid 'global' keyword issue
MODELS_AVAILABLE = False
EvaluationContext = Mock
ImplementationPlan = Mock
ComplexityScore = Mock
FactorScore = Mock
ReviewMode = Mock

try:
    # Add installer directory to path temporarily
    installer_lib_path = Path(__file__).parent.parent.parent / "installer" / "global" / "commands" / "lib"
    if installer_lib_path.exists():
        sys.path.insert(0, str(installer_lib_path))

        # Import models
        try:
            import complexity_models
            EvaluationContext = complexity_models.EvaluationContext
            ImplementationPlan = complexity_models.ImplementationPlan
            ComplexityScore = complexity_models.ComplexityScore
            FactorScore = complexity_models.FactorScore
            ReviewMode = complexity_models.ReviewMode
            MODELS_AVAILABLE = True
        except ImportError:
            pass
        finally:
            # Clean up sys.path
            sys.path.pop(0)
except Exception:
    pass


@pytest.fixture
def mock_file_system():
    """
    Mock file system for testing without I/O.

    Provides in-memory file storage with same interface as
    real file operations.

    Example:
        >>> fs = mock_file_system()
        >>> fs.write(Path("task.md"), "content")
        >>> assert fs.read(Path("task.md")) == "content"
        >>> assert fs.exists(Path("task.md")) == True
    """
    class MockFileSystem:
        def __init__(self):
            self.files: Dict[str, str] = {}

        def write(self, path: Path, content: str) -> None:
            """Write content to mock file."""
            self.files[str(path)] = content

        def read(self, path: Path) -> str:
            """Read content from mock file."""
            if str(path) not in self.files:
                raise FileNotFoundError(f"File not found: {path}")
            return self.files[str(path)]

        def exists(self, path: Path) -> bool:
            """Check if mock file exists."""
            return str(path) in self.files

        def delete(self, path: Path) -> None:
            """Delete mock file."""
            if str(path) in self.files:
                del self.files[str(path)]

        def list_files(self, pattern: str = "*") -> List[Path]:
            """List all mock files matching pattern."""
            import fnmatch
            return [
                Path(path)
                for path in self.files.keys()
                if fnmatch.fnmatch(path, pattern)
            ]

        def clear(self) -> None:
            """Clear all mock files."""
            self.files.clear()

    return MockFileSystem()


@pytest.fixture
def mock_task_context(simple_task_data):
    """
    Mock evaluation context for complexity calculation.

    Creates a mock EvaluationContext without requiring real
    file system or task infrastructure.

    Example:
        >>> context = mock_task_context(simple_task_data)
        >>> assert context.task_id == 'TASK-SIMPLE-001'
    """
    # Create mock implementation plan
    plan = Mock(spec=ImplementationPlan if MODELS_AVAILABLE else Mock)
    plan.raw_plan = "Implementation plan text"
    plan.files_to_create = simple_task_data['files_to_create']
    plan.external_dependencies = simple_task_data['external_dependencies']
    plan.has_security_keywords = simple_task_data['has_security_keywords']
    plan.has_schema_changes = simple_task_data['has_schema_changes']
    plan.estimated_loc = simple_task_data.get('estimated_loc', 100)
    plan.estimated_duration = "2 hours"

    # Create evaluation context
    context = Mock(spec=EvaluationContext if MODELS_AVAILABLE else Mock)
    context.task_id = simple_task_data['task_id']
    context.technology_stack = simple_task_data['technology_stack'][0] if simple_task_data['technology_stack'] else 'unknown'
    context.implementation_plan = plan
    context.task_metadata = {
        'id': simple_task_data['task_id'],
        'title': simple_task_data['title'],
        'requirements': simple_task_data['requirements']
    }
    context.user_requested_review = False
    context.is_hotfix = simple_task_data['is_hotfix']

    return context


@pytest.fixture
def mock_complexity_score():
    """
    Mock complexity score for testing review modes.

    Example:
        >>> score = mock_complexity_score()
        >>> assert score.total_score == 5
        >>> assert score.review_mode.value == 'quick_optional'
    """
    # Create mock factor scores
    factor_scores = [
        Mock(
            factor_name="File Count",
            score=2,
            max_score=3,
            justification="4 files to create (medium)",
            weight=1.0
        ),
        Mock(
            factor_name="Pattern Familiarity",
            score=2,
            max_score=3,
            justification="Mix of familiar and new patterns",
            weight=1.0
        ),
        Mock(
            factor_name="Risk Level",
            score=1,
            max_score=4,
            justification="Low-medium risk indicators",
            weight=1.0
        )
    ]

    # Create complexity score
    score = Mock(spec=ComplexityScore if MODELS_AVAILABLE else Mock)
    score.total_score = 5
    score.factor_scores = factor_scores
    score.forced_review_triggers = []
    score.review_mode = Mock()
    score.review_mode.value = 'quick_optional'
    score.calculation_timestamp = datetime.now()
    score.metadata = {
        'task_id': 'TASK-MOCK-001',
        'patterns_detected': ['api', 'database'],
        'warnings': []
    }

    return score


@pytest.fixture
def mock_implementation_plan():
    """
    Mock implementation plan for testing review displays.

    Example:
        >>> plan = mock_implementation_plan()
        >>> assert len(plan.files_to_create) == 4
    """
    plan = Mock(spec=ImplementationPlan if MODELS_AVAILABLE else Mock)
    plan.raw_plan = """
    # Implementation Plan

    ## Files to Create
    1. src/api/endpoints/users.py
    2. src/models/user.py
    3. src/services/user_service.py
    4. tests/test_user_service.py

    ## Dependencies
    - FastAPI
    - SQLAlchemy

    ## Phases
    1. Create data models
    2. Implement service layer
    3. Create API endpoints
    4. Write tests
    """
    plan.files_to_create = [
        'src/api/endpoints/users.py',
        'src/models/user.py',
        'src/services/user_service.py',
        'tests/test_user_service.py'
    ]
    plan.external_dependencies = ['FastAPI', 'SQLAlchemy']
    plan.phases = [
        'Create data models',
        'Implement service layer',
        'Create API endpoints',
        'Write tests'
    ]
    plan.estimated_loc = 300
    plan.estimated_duration = "4-6 hours"
    plan.test_summary = "Unit tests for service layer, integration tests for API"
    plan.risk_details = [
        {
            'severity': 'medium',
            'description': 'Database schema changes',
            'mitigation': 'Use migrations and test in staging'
        }
    ]
    plan.risk_indicators = ['schema_changes']
    plan.has_security_keywords = False
    plan.has_schema_changes = True
    plan.implementation_instructions = "Follow TDD approach, write tests first"

    # Add complexity score to plan
    plan.complexity_score = Mock()
    plan.complexity_score.total_score = 5
    plan.complexity_score.overall_score = 50
    plan.complexity_score.patterns_detected = ['api', 'database', 'service']
    plan.complexity_score.warnings = []
    plan.complexity_score.metadata = {}

    plan.display_score = 50

    return plan


@pytest.fixture
def mock_metrics_storage(tmp_path):
    """
    Mock metrics storage for testing metrics collection.

    Uses temporary directory for test isolation.

    Example:
        >>> storage = mock_metrics_storage(tmp_path)
        >>> storage.save_metric('complexity', 5)
        >>> assert storage.load_metric('complexity') == 5
    """
    class MockMetricsStorage:
        def __init__(self, storage_path: Path):
            self.storage_path = storage_path
            self.metrics: Dict[str, Any] = {}

        def save_metric(self, key: str, value: Any) -> None:
            """Save metric to storage."""
            self.metrics[key] = value

        def load_metric(self, key: str) -> Optional[Any]:
            """Load metric from storage."""
            return self.metrics.get(key)

        def list_metrics(self) -> List[str]:
            """List all metric keys."""
            return list(self.metrics.keys())

        def clear(self) -> None:
            """Clear all metrics."""
            self.metrics.clear()

    return MockMetricsStorage(tmp_path / "metrics")


@pytest.fixture
def mock_user_input():
    """
    Mock user input for testing interactive flows.

    Provides programmatic control over user input in tests.

    Example:
        >>> user_input = mock_user_input()
        >>> user_input.set_sequence(['a', 'y'])
        >>> assert user_input.get_input() == 'a'
        >>> assert user_input.get_input() == 'y'
    """
    class MockUserInput:
        def __init__(self):
            self.input_sequence: List[str] = []
            self.input_index: int = 0

        def set_sequence(self, inputs: List[str]) -> None:
            """Set sequence of inputs to return."""
            self.input_sequence = inputs
            self.input_index = 0

        def get_input(self, prompt: str = "") -> str:
            """Get next input from sequence."""
            if self.input_index >= len(self.input_sequence):
                raise ValueError("No more inputs in sequence")
            value = self.input_sequence[self.input_index]
            self.input_index += 1
            return value

        def has_more(self) -> bool:
            """Check if more inputs available."""
            return self.input_index < len(self.input_sequence)

        def reset(self) -> None:
            """Reset to beginning of sequence."""
            self.input_index = 0

    return MockUserInput()


@pytest.fixture
def mock_countdown_timer():
    """
    Mock countdown timer for testing quick review timeouts.

    Example:
        >>> timer = mock_countdown_timer()
        >>> timer.set_result('timeout')
        >>> assert timer.run(10) == 'timeout'
    """
    class MockCountdownTimer:
        def __init__(self):
            self.result = 'timeout'
            self.duration = 0

        def set_result(self, result: str) -> None:
            """Set result to return from countdown."""
            self.result = result

        def run(self, duration: int, message: str = "", options: str = "") -> str:
            """Run mock countdown (returns immediately)."""
            self.duration = duration
            return self.result

    return MockCountdownTimer()


@pytest.fixture
def mock_task_metadata():
    """
    Mock task metadata for testing review handlers.

    Example:
        >>> metadata = mock_task_metadata()
        >>> assert metadata['id'] == 'TASK-MOCK-001'
    """
    return {
        'id': 'TASK-MOCK-001',
        'title': 'Mock task for testing',
        'status': 'in_progress',
        'created': '2025-10-10T00:00:00Z',
        'updated': '2025-10-10T00:00:00Z',
        'assignee': 'test_user',
        'priority': 'medium',
        'requirements': ['REQ-001', 'REQ-002'],
        'technology_stack': 'Python'
    }


@pytest.fixture
def mock_task_file_path(tmp_path):
    """
    Mock task file path in temporary directory.

    Example:
        >>> path = mock_task_file_path(tmp_path)
        >>> path.write_text("task content")
    """
    task_file = tmp_path / "tasks" / "in_progress" / "TASK-MOCK-001.md"
    task_file.parent.mkdir(parents=True, exist_ok=True)
    return task_file


@pytest.fixture
def mock_logger():
    """
    Mock logger for testing logging behavior.

    Example:
        >>> logger = mock_logger()
        >>> logger.info("test message")
        >>> assert "test message" in logger.messages['info']
    """
    class MockLogger:
        def __init__(self):
            self.messages = {
                'debug': [],
                'info': [],
                'warning': [],
                'error': []
            }

        def debug(self, message: str, **kwargs) -> None:
            self.messages['debug'].append(message)

        def info(self, message: str, **kwargs) -> None:
            self.messages['info'].append(message)

        def warning(self, message: str, **kwargs) -> None:
            self.messages['warning'].append(message)

        def error(self, message: str, **kwargs) -> None:
            self.messages['error'].append(message)

        def get_messages(self, level: str) -> List[str]:
            return self.messages.get(level, [])

        def clear(self) -> None:
            for level in self.messages:
                self.messages[level].clear()

    return MockLogger()


# Module exports
__all__ = [
    'mock_file_system',
    'mock_task_context',
    'mock_complexity_score',
    'mock_implementation_plan',
    'mock_metrics_storage',
    'mock_user_input',
    'mock_countdown_timer',
    'mock_task_metadata',
    'mock_task_file_path',
    'mock_logger',
]
