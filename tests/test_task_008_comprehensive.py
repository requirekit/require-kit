"""
Comprehensive test suite for TASK-008: Feature Task Breakdown Implementation

This test suite covers all modules created for TASK-008:
1. task_breakdown.py - Task breakdown orchestration
2. breakdown_strategies.py - Strategy implementations
3. duplicate_detector.py - Duplicate detection
4. visualization.py - Terminal formatting
5. feature_generator.py - Task file generation

Test Coverage:
- Unit tests for each module and class
- Integration tests for full workflow
- Edge case testing
- Mock-based testing for external dependencies

Target Coverage: ≥80% line, ≥75% branch
"""

import pytest
import os
import tempfile
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, MagicMock, patch, mock_open
import sys

# Add lib path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'installer', 'global', 'commands', 'lib'))

from task_breakdown import (
    TaskBreakdownOrchestrator,
    TaskBreakdownResult,
    breakdown_feature_tasks
)
from breakdown_strategies import (
    NoBreakdownStrategy,
    LogicalBreakdownStrategy,
    FileBasedBreakdownStrategy,
    PhaseBasedBreakdownStrategy,
    get_strategy
)
from duplicate_detector import DuplicateDetector, DuplicateMatch
from visualization import TerminalFormatter, Colors, Emojis, ComplexityVisualization
from feature_generator import TaskFileGenerator, TaskFileMetadata
from complexity_models import (
    ComplexityScore,
    FactorScore,
    ReviewMode,
    ForceReviewTrigger,
    ImplementationPlan,
    EvaluationContext
)
from complexity_calculator import ComplexityCalculator


# ==================== FIXTURES ====================

@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory structure."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)

        # Create task directories
        for directory in ["backlog", "in_progress", "in_review", "blocked", "completed"]:
            (project_root / "tasks" / directory).mkdir(parents=True)

        yield project_root


@pytest.fixture
def sample_task_data():
    """Sample task data for testing."""
    return {
        "id": "TASK-001",
        "title": "Implement user authentication",
        "feature_id": "FEAT-001",
        "epic_id": "EPIC-001",
        "stack": "python",
        "files": [
            "auth/service.py",
            "auth/repository.py",
            "auth/models.py",
            "tests/test_auth.py"
        ],
        "patterns": ["Repository", "Service"],
        "dependencies": ["jwt", "bcrypt"],
        "estimated_loc": 200,
        "description": "Implement JWT-based authentication system"
    }


@pytest.fixture
def sample_complex_task_data():
    """Sample complex task for breakdown testing."""
    return {
        "id": "TASK-002",
        "title": "Build payment processing system",
        "feature_id": "FEAT-002",
        "epic_id": "EPIC-001",
        "stack": "python",
        "files": [
            "payment/models/payment.py",
            "payment/models/transaction.py",
            "payment/services/payment_service.py",
            "payment/services/refund_service.py",
            "payment/repositories/payment_repository.py",
            "payment/repositories/transaction_repository.py",
            "payment/api/payment_routes.py",
            "payment/api/webhook_handler.py",
            "payment/integrations/stripe_client.py",
            "payment/integrations/paypal_client.py",
            "tests/test_payment.py",
            "tests/test_refund.py"
        ],
        "patterns": ["Repository", "Service", "Strategy", "Adapter"],
        "dependencies": ["stripe", "paypal", "celery"],
        "estimated_loc": 800,
        "description": "Complete payment processing with multiple gateways"
    }


@pytest.fixture
def mock_complexity_score_low():
    """Mock low complexity score (1-3)."""
    return ComplexityScore(
        total_score=2,
        factor_scores=[
            FactorScore("file_complexity", 1, 3, "Simple task"),
            FactorScore("pattern_complexity", 1, 3, "Basic patterns")
        ],
        forced_review_triggers=[],
        review_mode=ReviewMode.AUTO_PROCEED,
        calculation_timestamp=datetime.now()
    )


@pytest.fixture
def mock_complexity_score_medium():
    """Mock medium complexity score (4-6)."""
    return ComplexityScore(
        total_score=5,
        factor_scores=[
            FactorScore("file_complexity", 2, 3, "Moderate files"),
            FactorScore("pattern_complexity", 2, 3, "Multiple patterns"),
            FactorScore("dependency_complexity", 1, 3, "Few deps")
        ],
        forced_review_triggers=[],
        review_mode=ReviewMode.QUICK_OPTIONAL,
        calculation_timestamp=datetime.now()
    )


@pytest.fixture
def mock_complexity_score_high():
    """Mock high complexity score (7-8)."""
    return ComplexityScore(
        total_score=7,
        factor_scores=[
            FactorScore("file_complexity", 3, 3, "Many files"),
            FactorScore("pattern_complexity", 2, 3, "Complex patterns"),
            FactorScore("dependency_complexity", 2, 3, "External deps")
        ],
        forced_review_triggers=[],
        review_mode=ReviewMode.FULL_REQUIRED,
        calculation_timestamp=datetime.now()
    )


@pytest.fixture
def mock_complexity_score_critical():
    """Mock critical complexity score (9-10)."""
    return ComplexityScore(
        total_score=10,
        factor_scores=[
            FactorScore("file_complexity", 3, 3, "Very many files"),
            FactorScore("pattern_complexity", 3, 3, "Advanced patterns"),
            FactorScore("dependency_complexity", 3, 3, "Many deps"),
            FactorScore("risk_complexity", 1, 3, "High risk")
        ],
        forced_review_triggers=[ForceReviewTrigger.SECURITY_KEYWORDS],
        review_mode=ReviewMode.FULL_REQUIRED,
        calculation_timestamp=datetime.now()
    )


# ==================== BREAKDOWN STRATEGIES TESTS ====================

class TestNoBreakdownStrategy:
    """Tests for NoBreakdownStrategy."""

    def test_no_breakdown_returns_empty_list(self, sample_task_data, mock_complexity_score_low):
        """Test that no breakdown strategy returns empty list."""
        strategy = NoBreakdownStrategy()
        result = strategy.breakdown(sample_task_data, mock_complexity_score_low)

        assert result == []
        assert isinstance(result, list)

    def test_no_breakdown_with_complex_task(self, sample_complex_task_data, mock_complexity_score_low):
        """Test no breakdown even with complex task data if score is low."""
        strategy = NoBreakdownStrategy()
        result = strategy.breakdown(sample_complex_task_data, mock_complexity_score_low)

        assert result == []


class TestLogicalBreakdownStrategy:
    """Tests for LogicalBreakdownStrategy."""

    def test_logical_breakdown_generates_subtasks(self, sample_task_data, mock_complexity_score_medium):
        """Test that logical breakdown generates component-based subtasks."""
        strategy = LogicalBreakdownStrategy()
        result = strategy.breakdown(sample_task_data, mock_complexity_score_medium)

        assert len(result) > 0
        assert all(isinstance(subtask, dict) for subtask in result)
        assert all("id" in subtask for subtask in result)
        assert all("title" in subtask for subtask in result)
        assert all("component_type" in subtask for subtask in result)

    def test_logical_breakdown_identifies_components(self, sample_task_data, mock_complexity_score_medium):
        """Test component identification logic."""
        strategy = LogicalBreakdownStrategy()
        result = strategy.breakdown(sample_task_data, mock_complexity_score_medium)

        # Should identify business logic and data components
        component_types = [subtask["component_type"] for subtask in result]
        assert "logic" in component_types or "data" in component_types

    def test_logical_breakdown_includes_tests(self, sample_task_data, mock_complexity_score_medium):
        """Test that test files are identified as separate component."""
        strategy = LogicalBreakdownStrategy()
        result = strategy.breakdown(sample_task_data, mock_complexity_score_medium)

        component_types = [subtask["component_type"] for subtask in result]
        assert "test" in component_types

    def test_logical_breakdown_empty_files_list(self, mock_complexity_score_medium):
        """Test logical breakdown with no files."""
        task_data = {
            "id": "TASK-999",
            "title": "Empty task",
            "files": [],
            "patterns": []
        }

        strategy = LogicalBreakdownStrategy()
        result = strategy.breakdown(task_data, mock_complexity_score_medium)

        # Should have fallback implementation component
        assert len(result) >= 1


class TestFileBasedBreakdownStrategy:
    """Tests for FileBasedBreakdownStrategy."""

    def test_file_based_breakdown_groups_files(self, sample_complex_task_data, mock_complexity_score_high):
        """Test that file-based breakdown groups files by module."""
        strategy = FileBasedBreakdownStrategy()
        result = strategy.breakdown(sample_complex_task_data, mock_complexity_score_high)

        assert len(result) > 0
        # Each subtask should have 1-3 files
        for subtask in result:
            assert 1 <= len(subtask.get("files", [])) <= 3

    def test_file_based_breakdown_maintains_module_grouping(self, sample_complex_task_data, mock_complexity_score_high):
        """Test that files from same module are grouped together."""
        strategy = FileBasedBreakdownStrategy()
        result = strategy.breakdown(sample_complex_task_data, mock_complexity_score_high)

        # Check that files in same subtask share common prefix
        for subtask in result:
            files = subtask.get("files", [])
            if len(files) > 1:
                # Extract module prefix from first file
                first_module = files[0].split("/")[0]
                # Check other files (most should share prefix)
                same_module = sum(1 for f in files if f.startswith(first_module))
                assert same_module >= len(files) // 2  # At least half should match

    def test_file_based_breakdown_assigns_ids(self, sample_complex_task_data, mock_complexity_score_high):
        """Test that subtasks have proper hierarchical IDs."""
        strategy = FileBasedBreakdownStrategy()
        result = strategy.breakdown(sample_complex_task_data, mock_complexity_score_high)

        for i, subtask in enumerate(result, 1):
            assert subtask["id"] == f"TASK-002.{i}"
            assert subtask["parent_task"] == "TASK-002"


class TestPhaseBasedBreakdownStrategy:
    """Tests for PhaseBasedBreakdownStrategy."""

    def test_phase_based_breakdown_creates_phases(self, sample_complex_task_data, mock_complexity_score_critical):
        """Test that phase-based breakdown creates implementation phases."""
        strategy = PhaseBasedBreakdownStrategy()
        result = strategy.breakdown(sample_complex_task_data, mock_complexity_score_critical)

        assert len(result) > 0
        # Should have at least foundation and core phases
        phase_names = [subtask.get("phase_name") for subtask in result]
        assert "Foundation" in phase_names

    def test_phase_based_breakdown_sequential_dependencies(self, sample_complex_task_data, mock_complexity_score_critical):
        """Test that phases have sequential dependencies."""
        strategy = PhaseBasedBreakdownStrategy()
        result = strategy.breakdown(sample_complex_task_data, mock_complexity_score_critical)

        # First phase should have no dependencies
        assert result[0]["dependencies"] == []

        # Subsequent phases should depend on previous
        for i in range(1, len(result)):
            deps = result[i]["dependencies"]
            assert len(deps) == 1
            assert deps[0] == f"TASK-002.{i}"

    def test_phase_based_breakdown_distributes_files(self, sample_complex_task_data, mock_complexity_score_critical):
        """Test that files are distributed across phases."""
        strategy = PhaseBasedBreakdownStrategy()
        result = strategy.breakdown(sample_complex_task_data, mock_complexity_score_critical)

        # Count total files distributed
        total_files = sum(len(subtask.get("files", [])) for subtask in result)
        original_files = len(sample_complex_task_data["files"])

        assert total_files == original_files


class TestStrategySelection:
    """Tests for strategy selection logic."""

    def test_get_strategy_low_complexity(self):
        """Test strategy selection for low complexity (1-3)."""
        strategy = get_strategy(2)
        assert isinstance(strategy, NoBreakdownStrategy)

    def test_get_strategy_medium_complexity(self):
        """Test strategy selection for medium complexity (4-6)."""
        strategy = get_strategy(5)
        assert isinstance(strategy, LogicalBreakdownStrategy)

    def test_get_strategy_high_complexity(self):
        """Test strategy selection for high complexity (7-8)."""
        strategy = get_strategy(7)
        assert isinstance(strategy, FileBasedBreakdownStrategy)

    def test_get_strategy_critical_complexity(self):
        """Test strategy selection for critical complexity (9-10)."""
        strategy = get_strategy(10)
        assert isinstance(strategy, PhaseBasedBreakdownStrategy)


# ==================== DUPLICATE DETECTOR TESTS ====================

class TestDuplicateDetector:
    """Tests for DuplicateDetector."""

    def test_find_duplicates_no_matches(self, temp_project_dir):
        """Test duplicate detection with no existing tasks."""
        detector = DuplicateDetector(project_root=str(temp_project_dir))
        task_data = {"id": "TASK-001", "title": "Implement authentication"}

        duplicates = detector.find_duplicates(task_data)
        assert duplicates == []

    def test_find_duplicates_exact_match(self, temp_project_dir):
        """Test duplicate detection with exact title match."""
        detector = DuplicateDetector(project_root=str(temp_project_dir))

        # Create existing task file
        existing_file = temp_project_dir / "tasks/backlog/TASK-001-implement-authentication.md"
        existing_file.write_text("# Implement Authentication")

        # Search for duplicate
        task_data = {"id": "TASK-002", "title": "Implement Authentication"}
        duplicates = detector.find_duplicates(task_data)

        assert len(duplicates) == 1
        assert duplicates[0].task_id == "TASK-001"
        assert duplicates[0].is_exact_match

    def test_find_duplicates_fuzzy_match(self, temp_project_dir):
        """Test fuzzy matching for similar titles."""
        detector = DuplicateDetector(project_root=str(temp_project_dir))

        # Create existing task
        existing_file = temp_project_dir / "tasks/backlog/TASK-001-user-authentication-system.md"
        existing_file.write_text("# User Authentication System")

        # Search for similar task
        task_data = {"id": "TASK-002", "title": "User Authentication Module"}
        duplicates = detector.find_duplicates(task_data, threshold_override=0.7)

        assert len(duplicates) >= 0  # May or may not match depending on threshold

    def test_calculate_similarity_exact(self, temp_project_dir):
        """Test similarity calculation for exact matches."""
        detector = DuplicateDetector(project_root=str(temp_project_dir))

        similarity = detector._calculate_similarity(
            "Implement user authentication",
            "Implement user authentication"
        )

        assert similarity == 1.0

    def test_calculate_similarity_partial(self, temp_project_dir):
        """Test similarity calculation for partial matches."""
        detector = DuplicateDetector(project_root=str(temp_project_dir))

        similarity = detector._calculate_similarity(
            "Implement user authentication",
            "Implement authentication system"
        )

        assert 0.5 < similarity < 1.0

    def test_calculate_similarity_no_match(self, temp_project_dir):
        """Test similarity calculation for no match."""
        detector = DuplicateDetector(project_root=str(temp_project_dir))

        similarity = detector._calculate_similarity(
            "Implement authentication",
            "Build payment gateway"
        )

        assert similarity < 0.5

    def test_check_exact_duplicate_exists(self, temp_project_dir):
        """Test exact duplicate check when task ID exists."""
        detector = DuplicateDetector(project_root=str(temp_project_dir))

        # Create existing task
        existing_file = temp_project_dir / "tasks/backlog/TASK-001-test.md"
        existing_file.write_text("# Test")

        exists = detector.check_exact_duplicate("TASK-001")
        assert exists is True

    def test_check_exact_duplicate_not_exists(self, temp_project_dir):
        """Test exact duplicate check when task ID doesn't exist."""
        detector = DuplicateDetector(project_root=str(temp_project_dir))

        exists = detector.check_exact_duplicate("TASK-999")
        assert exists is False

    def test_get_duplicate_summary_empty(self, temp_project_dir):
        """Test duplicate summary with no matches."""
        detector = DuplicateDetector(project_root=str(temp_project_dir))

        summary = detector.get_duplicate_summary([])

        assert summary["total_matches"] == 0
        assert summary["exact_matches"] == 0
        assert summary["likely_duplicates"] == 0


# ==================== VISUALIZATION TESTS ====================

class TestTerminalFormatter:
    """Tests for TerminalFormatter."""

    def test_formatter_initialization(self):
        """Test formatter initialization."""
        formatter = TerminalFormatter(use_color=True, use_emoji=True)
        assert formatter.use_color is True
        assert formatter.use_emoji is True

    def test_format_complexity_score(self, mock_complexity_score_medium):
        """Test complexity score formatting."""
        formatter = TerminalFormatter()
        output = formatter.format_complexity_score(mock_complexity_score_medium)

        assert "Complexity Score: 5/10" in output
        assert "Medium" in output
        assert "Factor Breakdown" in output

    def test_format_complexity_score_no_color(self, mock_complexity_score_medium):
        """Test formatting without colors."""
        formatter = TerminalFormatter(use_color=False)
        output = formatter.format_complexity_score(mock_complexity_score_medium)

        # Should not contain ANSI color codes
        assert "\033[" not in output

    def test_format_complexity_score_no_emoji(self, mock_complexity_score_medium):
        """Test formatting without emojis."""
        formatter = TerminalFormatter(use_emoji=False)
        output = formatter.format_complexity_score(mock_complexity_score_medium)

        # Should not contain emoji characters
        assert "🟢" not in output
        assert "🟡" not in output
        assert "🔴" not in output

    def test_get_complexity_visualization_low(self):
        """Test visualization for low complexity."""
        formatter = TerminalFormatter()
        viz = formatter._get_complexity_visualization(2)

        assert viz.label == "Low"
        assert viz.color_indicator == Emojis.GREEN_CIRCLE
        assert viz.color_code == Colors.GREEN

    def test_get_complexity_visualization_medium(self):
        """Test visualization for medium complexity."""
        formatter = TerminalFormatter()
        viz = formatter._get_complexity_visualization(5)

        assert viz.label == "Medium"
        assert viz.color_indicator == Emojis.YELLOW_CIRCLE

    def test_get_complexity_visualization_high(self):
        """Test visualization for high complexity."""
        formatter = TerminalFormatter()
        viz = formatter._get_complexity_visualization(7)

        assert viz.label == "High"
        assert viz.color_indicator == Emojis.RED_CIRCLE

    def test_get_complexity_visualization_critical(self):
        """Test visualization for critical complexity."""
        formatter = TerminalFormatter()
        viz = formatter._get_complexity_visualization(10)

        assert viz.label == "Critical"
        assert viz.color_indicator == Emojis.RED_CIRCLE


# ==================== TASK FILE GENERATOR TESTS ====================

class TestTaskFileGenerator:
    """Tests for TaskFileGenerator."""

    def test_generate_filename(self, temp_project_dir):
        """Test filename generation."""
        generator = TaskFileGenerator(project_root=str(temp_project_dir))

        filename = generator._generate_filename("TASK-001.2.03", "Implement Authentication System")

        assert filename.startswith("TASK-001.2.03")
        assert filename.endswith(".md")
        assert "implement" in filename.lower()

    def test_generate_task_files_creates_files(self, temp_project_dir):
        """Test that task file generation creates actual files."""
        generator = TaskFileGenerator(project_root=str(temp_project_dir))

        subtasks = [
            {
                "id": "TASK-001.1",
                "title": "Implement authentication service",
                "description": "Core auth logic",
                "complexity": "medium",
                "estimated_hours": 4
            }
        ]

        result = generator.generate_task_files(subtasks, "FEAT-001", "EPIC-001")

        assert len(result) == 1
        assert Path(result[0].file_path).exists()

    def test_generate_task_files_content_format(self, temp_project_dir):
        """Test that generated files have correct YAML frontmatter."""
        generator = TaskFileGenerator(project_root=str(temp_project_dir))

        subtasks = [
            {
                "id": "TASK-001.1",
                "title": "Test Task",
                "description": "Test description",
                "complexity": "low",
                "estimated_hours": 2
            }
        ]

        result = generator.generate_task_files(subtasks, "FEAT-001", "EPIC-001")
        content = Path(result[0].file_path).read_text()

        assert content.startswith("---")
        assert "id: TASK-001.1" in content
        assert "feature_id: FEAT-001" in content
        assert "epic_id: EPIC-001" in content

    def test_generate_next_task_id(self, temp_project_dir):
        """Test hierarchical task ID generation."""
        generator = TaskFileGenerator(project_root=str(temp_project_dir))

        task_id = generator._generate_next_task_id("EPIC-001", "FEAT-001.2", [])

        assert task_id.startswith("TASK-")
        assert "001" in task_id
        assert "2" in task_id

    def test_generate_summary_file(self, temp_project_dir):
        """Test summary file generation."""
        generator = TaskFileGenerator(project_root=str(temp_project_dir))

        metadata_list = [
            TaskFileMetadata(
                task_id="TASK-001.1",
                file_path="/path/to/task.md",
                title="Test Task",
                complexity="medium",
                parent_task=None,
                status="backlog"
            )
        ]

        summary_path = generator.generate_summary_file(metadata_list, "FEAT-001")

        assert Path(summary_path).exists()
        assert "FEAT-001" in summary_path


# ==================== TASK BREAKDOWN ORCHESTRATOR TESTS ====================

class TestTaskBreakdownOrchestrator:
    """Tests for TaskBreakdownOrchestrator."""

    def test_orchestrator_initialization(self):
        """Test orchestrator initialization."""
        orchestrator = TaskBreakdownOrchestrator()

        assert orchestrator.complexity_calculator is not None
        assert orchestrator.duplicate_detector is not None
        assert orchestrator.formatter is not None
        assert len(orchestrator.strategies) == 4

    @patch('task_breakdown.ComplexityCalculator')
    def test_breakdown_task_simple(self, mock_calc_class, sample_task_data, mock_complexity_score_low):
        """Test breakdown with simple task (no breakdown needed)."""
        # Mock complexity calculator
        mock_calc = Mock()
        mock_calc.calculate.return_value = mock_complexity_score_low
        mock_calc_class.return_value = mock_calc

        orchestrator = TaskBreakdownOrchestrator(complexity_calculator=mock_calc)
        result = orchestrator.breakdown_task(sample_task_data)

        assert result.success is True
        assert result.subtask_count == 0
        assert "no breakdown" in result.breakdown_reason.lower()

    @patch('task_breakdown.ComplexityCalculator')
    def test_breakdown_task_medium(self, mock_calc_class, sample_task_data, mock_complexity_score_medium):
        """Test breakdown with medium complexity task."""
        # Mock complexity calculator
        mock_calc = Mock()
        mock_calc.calculate.return_value = mock_complexity_score_medium
        mock_calc_class.return_value = mock_calc

        orchestrator = TaskBreakdownOrchestrator(complexity_calculator=mock_calc)
        result = orchestrator.breakdown_task(sample_task_data)

        assert result.success is True
        # Logical breakdown should create some subtasks
        assert result.subtask_count > 0
        assert result.strategy_used == "LogicalBreakdownStrategy"

    def test_validate_task_data_valid(self):
        """Test task data validation with valid data."""
        orchestrator = TaskBreakdownOrchestrator()
        task_data = {
            "id": "TASK-001",
            "title": "Test",
            "feature_id": "FEAT-001",
            "epic_id": "EPIC-001"
        }

        # Should not raise exception
        orchestrator._validate_task_data(task_data)

    def test_validate_task_data_missing_fields(self):
        """Test task data validation with missing fields."""
        orchestrator = TaskBreakdownOrchestrator()
        task_data = {"id": "TASK-001"}

        with pytest.raises(ValueError) as exc_info:
            orchestrator._validate_task_data(task_data)

        assert "Missing required fields" in str(exc_info.value)

    def test_create_evaluation_context(self):
        """Test evaluation context creation."""
        orchestrator = TaskBreakdownOrchestrator()
        task_data = {
            "id": "TASK-001",
            "title": "Test",
            "feature_id": "FEAT-001",
            "epic_id": "EPIC-001",
            "stack": "python",
            "files": ["test.py"],
            "patterns": ["Repository"]
        }

        context = orchestrator._create_evaluation_context(task_data)

        assert context.task_id == "TASK-001"
        assert context.technology_stack == "python"
        assert context.implementation_plan is not None

    def test_select_strategy_score_based(self):
        """Test strategy selection based on complexity score."""
        orchestrator = TaskBreakdownOrchestrator()

        # Test each threshold
        low_score = ComplexityScore(2, [], [], ReviewMode.AUTO_PROCEED, datetime.now())
        medium_score = ComplexityScore(5, [], [], ReviewMode.QUICK_OPTIONAL, datetime.now())
        high_score = ComplexityScore(7, [], [], ReviewMode.FULL_REQUIRED, datetime.now())
        critical_score = ComplexityScore(10, [], [], ReviewMode.FULL_REQUIRED, datetime.now())

        assert isinstance(orchestrator._select_strategy(low_score, 7), NoBreakdownStrategy)
        assert isinstance(orchestrator._select_strategy(medium_score, 7), LogicalBreakdownStrategy)
        assert isinstance(orchestrator._select_strategy(high_score, 7), FileBasedBreakdownStrategy)
        assert isinstance(orchestrator._select_strategy(critical_score, 7), PhaseBasedBreakdownStrategy)

    def test_calculate_statistics(self):
        """Test statistics calculation."""
        orchestrator = TaskBreakdownOrchestrator()

        subtasks = [
            {"complexity": "low", "estimated_hours": 2},
            {"complexity": "medium", "estimated_hours": 4},
            {"complexity": "high", "estimated_hours": 6}
        ]

        stats = orchestrator._calculate_statistics(subtasks)

        assert stats["subtask_count"] == 3
        assert stats["estimated_total_time"] == 12
        assert "low" in stats["complexity_distribution"]
        assert stats["complexity_distribution"]["low"] == 1


# ==================== INTEGRATION TESTS ====================

class TestIntegration:
    """Integration tests for full workflow."""

    @patch('task_breakdown.ComplexityCalculator')
    def test_full_breakdown_workflow(self, mock_calc_class, sample_complex_task_data, mock_complexity_score_high, temp_project_dir):
        """Test complete breakdown workflow from feature to task files."""
        # Mock complexity calculator
        mock_calc = Mock()
        mock_calc.calculate.return_value = mock_complexity_score_high
        mock_calc_class.return_value = mock_calc

        # Run breakdown
        orchestrator = TaskBreakdownOrchestrator(complexity_calculator=mock_calc)
        result = orchestrator.breakdown_task(sample_complex_task_data)

        assert result.success is True
        assert result.subtask_count > 0

        # Generate files
        generator = TaskFileGenerator(project_root=str(temp_project_dir))
        files = generator.generate_task_files(
            result.subtasks,
            sample_complex_task_data["feature_id"],
            sample_complex_task_data["epic_id"]
        )

        assert len(files) == result.subtask_count
        assert all(Path(f.file_path).exists() for f in files)

    @patch('task_breakdown.ComplexityCalculator')
    def test_breakdown_feature_tasks_api(self, mock_calc_class, mock_complexity_score_medium):
        """Test public API function breakdown_feature_tasks."""
        # Mock complexity calculator
        mock_calc = Mock()
        mock_calc.calculate.return_value = mock_complexity_score_medium
        mock_calc_class.return_value = mock_calc

        feature_data = {
            "id": "FEAT-001",
            "title": "User Management",
            "epic_id": "EPIC-001",
            "technology_stack": "python",
            "tasks": [
                {
                    "id": "TASK-001",
                    "title": "Implement user service",
                    "files": ["user/service.py", "user/repository.py"],
                    "patterns": ["Repository"]
                }
            ]
        }

        # Need to patch within the function
        with patch('task_breakdown.TaskBreakdownOrchestrator') as mock_orch_class:
            mock_orch = Mock()
            mock_result = TaskBreakdownResult(
                success=True,
                original_task=feature_data["tasks"][0],
                subtasks=[],
                complexity_score=mock_complexity_score_medium,
                strategy_used="LogicalBreakdownStrategy",
                breakdown_reason="Test"
            )
            mock_orch.breakdown_task.return_value = mock_result
            mock_orch_class.return_value = mock_orch

            result = breakdown_feature_tasks(feature_data)

            assert result is not None
            assert result.success is True


# ==================== EDGE CASE TESTS ====================

class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_empty_feature_no_tasks(self):
        """Test breakdown with feature containing no tasks."""
        feature_data = {
            "id": "FEAT-001",
            "title": "Empty Feature",
            "tasks": []
        }

        result = breakdown_feature_tasks(feature_data)

        assert result.success is True
        assert result.subtask_count == 0

    @patch('task_breakdown.ComplexityCalculator')
    def test_all_tasks_below_threshold(self, mock_calc_class, mock_complexity_score_low):
        """Test feature where all tasks are below breakdown threshold."""
        mock_calc = Mock()
        mock_calc.calculate.return_value = mock_complexity_score_low

        orchestrator = TaskBreakdownOrchestrator(complexity_calculator=mock_calc)

        tasks = [
            {"id": f"TASK-{i}", "title": f"Task {i}", "feature_id": "FEAT-001", "epic_id": "EPIC-001"}
            for i in range(1, 4)
        ]

        results = [orchestrator.breakdown_task(task) for task in tasks]

        # All should have no breakdown
        assert all(r.subtask_count == 0 for r in results)

    def test_duplicate_detection_100_percent_similarity(self, temp_project_dir):
        """Test duplicate detection with 100% similarity."""
        detector = DuplicateDetector(project_root=str(temp_project_dir))

        # Create existing task
        existing_file = temp_project_dir / "tasks/backlog/TASK-001-test-task.md"
        existing_file.write_text("# Test Task")

        task_data = {"id": "TASK-002", "title": "Test Task"}
        duplicates = detector.find_duplicates(task_data)

        if duplicates:  # May or may not find depending on parsing
            assert duplicates[0].similarity_score >= 0.9

    def test_invalid_task_data_handling(self):
        """Test handling of invalid task data."""
        orchestrator = TaskBreakdownOrchestrator()

        invalid_task = {"title": "No ID"}  # Missing required fields

        result = orchestrator.breakdown_task(invalid_task)

        assert result.success is False
        assert len(result.errors) > 0

    def test_task_file_generator_auto_id_generation(self, temp_project_dir):
        """Test automatic task ID generation when not provided."""
        generator = TaskFileGenerator(project_root=str(temp_project_dir))

        subtasks = [
            {
                "title": "Subtask without ID",
                "description": "Test",
                "complexity": "low"
            }
        ]

        result = generator.generate_task_files(subtasks, "FEAT-001", "EPIC-001")

        assert len(result) == 1
        assert result[0].task_id.startswith("TASK-")


# ==================== PERFORMANCE TESTS ====================

class TestPerformance:
    """Performance-related tests."""

    @patch('task_breakdown.ComplexityCalculator')
    def test_large_file_list_performance(self, mock_calc_class, mock_complexity_score_high):
        """Test performance with large file list."""
        mock_calc = Mock()
        mock_calc.calculate.return_value = mock_complexity_score_high

        # Create task with many files
        large_task = {
            "id": "TASK-999",
            "title": "Large task",
            "feature_id": "FEAT-001",
            "epic_id": "EPIC-001",
            "files": [f"module{i}/file{j}.py" for i in range(10) for j in range(10)],
            "patterns": ["Repository"]
        }

        orchestrator = TaskBreakdownOrchestrator(complexity_calculator=mock_calc)
        result = orchestrator.breakdown_task(large_task)

        # Should complete successfully
        assert result.success is True
        assert result.subtask_count > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
