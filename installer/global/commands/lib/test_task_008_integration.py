"""
Integration test for TASK-008 modules.

This test verifies that all 5 new modules work together correctly:
1. task_breakdown.py - Main orchestration
2. breakdown_strategies.py - Strategy implementations
3. duplicate_detector.py - Duplicate detection
4. visualization.py - Terminal formatting
5. feature_generator.py - File generation

Run with: python3 -m pytest test_task_008_integration.py -v
"""

import pytest
from pathlib import Path
import tempfile
import os

# Import all new modules
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
from visualization import TerminalFormatter, Colors, Emojis
from feature_generator import TaskFileGenerator, TaskFileMetadata
from complexity_models import ComplexityScore, ImplementationPlan, EvaluationContext, ReviewMode
from complexity_calculator import ComplexityCalculator


class TestModuleImports:
    """Test that all modules import correctly."""

    def test_task_breakdown_imports(self):
        """Test task_breakdown module imports."""
        assert TaskBreakdownOrchestrator is not None
        assert TaskBreakdownResult is not None
        assert breakdown_feature_tasks is not None

    def test_breakdown_strategies_imports(self):
        """Test breakdown_strategies module imports."""
        assert NoBreakdownStrategy is not None
        assert LogicalBreakdownStrategy is not None
        assert FileBasedBreakdownStrategy is not None
        assert PhaseBasedBreakdownStrategy is not None
        assert get_strategy is not None

    def test_duplicate_detector_imports(self):
        """Test duplicate_detector module imports."""
        assert DuplicateDetector is not None
        assert DuplicateMatch is not None

    def test_visualization_imports(self):
        """Test visualization module imports."""
        assert TerminalFormatter is not None
        assert Colors is not None
        assert Emojis is not None

    def test_feature_generator_imports(self):
        """Test feature_generator module imports."""
        assert TaskFileGenerator is not None
        assert TaskFileMetadata is not None


class TestBreakdownStrategies:
    """Test breakdown strategy implementations."""

    def test_no_breakdown_strategy(self):
        """Test NoBreakdownStrategy returns empty list."""
        strategy = NoBreakdownStrategy()
        task_data = {"id": "TASK-001", "title": "Simple task", "files": ["file.py"]}

        # Create mock complexity score
        plan = ImplementationPlan(task_id="TASK-001", files_to_create=["file.py"])
        context = EvaluationContext(
            task_id="TASK-001",
            technology_stack="python",
            implementation_plan=plan
        )
        calculator = ComplexityCalculator()
        complexity_score = calculator.calculate(context)

        result = strategy.breakdown(task_data, complexity_score)
        assert result == []

    def test_logical_breakdown_strategy(self):
        """Test LogicalBreakdownStrategy generates component-based subtasks."""
        strategy = LogicalBreakdownStrategy()
        task_data = {
            "id": "TASK-002",
            "title": "Build dashboard",
            "files": ["dashboard_view.py", "dashboard_service.py", "test_dashboard.py"],
            "patterns": ["MVC"]
        }

        plan = ImplementationPlan(
            task_id="TASK-002",
            files_to_create=task_data["files"],
            patterns_used=task_data["patterns"]
        )
        context = EvaluationContext(
            task_id="TASK-002",
            technology_stack="python",
            implementation_plan=plan
        )
        calculator = ComplexityCalculator()
        complexity_score = calculator.calculate(context)

        result = strategy.breakdown(task_data, complexity_score)
        assert len(result) > 0
        assert all("id" in subtask for subtask in result)
        assert all(subtask["parent_task"] == "TASK-002" for subtask in result)

    def test_get_strategy_selection(self):
        """Test strategy selection based on complexity score."""
        # Low complexity
        strategy_low = get_strategy(2)
        assert isinstance(strategy_low, NoBreakdownStrategy)

        # Medium complexity
        strategy_medium = get_strategy(5)
        assert isinstance(strategy_medium, LogicalBreakdownStrategy)

        # High complexity
        strategy_high = get_strategy(8)
        assert isinstance(strategy_high, FileBasedBreakdownStrategy)

        # Critical complexity
        strategy_critical = get_strategy(10)
        assert isinstance(strategy_critical, PhaseBasedBreakdownStrategy)


class TestDuplicateDetector:
    """Test duplicate detection functionality."""

    def test_duplicate_detector_initialization(self):
        """Test DuplicateDetector initializes correctly."""
        detector = DuplicateDetector(threshold=0.85)
        assert detector.threshold == 0.85

    def test_find_duplicates_empty(self):
        """Test find_duplicates with no existing tasks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            detector = DuplicateDetector(project_root=tmpdir)
            task_data = {"id": "TASK-001", "title": "New task"}

            duplicates = detector.find_duplicates(task_data)
            assert duplicates == []

    def test_check_exact_duplicate(self):
        """Test exact duplicate checking."""
        with tempfile.TemporaryDirectory() as tmpdir:
            detector = DuplicateDetector(project_root=tmpdir)

            # Should not find duplicate in empty directory
            result = detector.check_exact_duplicate("TASK-999")
            assert result is False


class TestVisualization:
    """Test terminal visualization and formatting."""

    def test_formatter_initialization(self):
        """Test TerminalFormatter initializes correctly."""
        formatter = TerminalFormatter(use_color=True, use_emoji=True)
        assert formatter.use_color is True
        assert formatter.use_emoji is True

    def test_format_complexity_score(self):
        """Test complexity score formatting."""
        formatter = TerminalFormatter()

        plan = ImplementationPlan(
            task_id="TASK-001",
            files_to_create=["file1.py", "file2.py"]
        )
        context = EvaluationContext(
            task_id="TASK-001",
            technology_stack="python",
            implementation_plan=plan
        )
        calculator = ComplexityCalculator()
        complexity_score = calculator.calculate(context)

        output = formatter.format_complexity_score(complexity_score)
        assert "Complexity Score" in output
        assert "Factor Breakdown" in output

    def test_format_breakdown_result(self):
        """Test breakdown result formatting."""
        formatter = TerminalFormatter()

        result = TaskBreakdownResult(
            success=True,
            original_task={"id": "TASK-001", "title": "Test task"},
            subtasks=[
                {"id": "TASK-001.1", "title": "Subtask 1", "complexity": "medium", "estimated_hours": 4}
            ],
            strategy_used="LogicalBreakdownStrategy",
            breakdown_reason="Moderate complexity"
        )

        output = formatter.format_breakdown_result(result)
        assert "Task Breakdown Result" in output
        assert "TASK-001" in output
        assert "Subtask 1" in output


class TestFeatureGenerator:
    """Test task file generation functionality."""

    def test_generator_initialization(self):
        """Test TaskFileGenerator initializes correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = TaskFileGenerator(project_root=tmpdir)
            assert generator.project_root == Path(tmpdir)

    def test_generate_filename(self):
        """Test filename generation."""
        generator = TaskFileGenerator()

        filename = generator._generate_filename("TASK-001.2.05", "Implement Authentication")
        assert filename.startswith("TASK-001.2.05-")
        assert filename.endswith(".md")
        assert "implement" in filename.lower()
        assert "authentication" in filename.lower()

    def test_generate_task_files(self):
        """Test task file generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = TaskFileGenerator(project_root=tmpdir)

            # Create output directory
            output_dir = Path(tmpdir) / "tasks" / "backlog"
            output_dir.mkdir(parents=True, exist_ok=True)

            subtasks = [
                {
                    "id": "TASK-001.1.01",
                    "title": "Test Subtask",
                    "description": "Test description",
                    "files": ["file1.py"],
                    "complexity": "medium",
                    "estimated_hours": 4
                }
            ]

            result = generator.generate_task_files(
                subtasks,
                feature_id="FEAT-001.1",
                epic_id="EPIC-001",
                output_dir="tasks/backlog"
            )

            assert len(result) == 1
            assert result[0].task_id == "TASK-001.1.01"
            assert Path(result[0].file_path).exists()


class TestTaskBreakdownOrchestrator:
    """Test main orchestration workflow."""

    def test_orchestrator_initialization(self):
        """Test TaskBreakdownOrchestrator initializes correctly."""
        orchestrator = TaskBreakdownOrchestrator()
        assert orchestrator.complexity_calculator is not None
        assert orchestrator.duplicate_detector is not None
        assert orchestrator.formatter is not None

    def test_breakdown_task_simple(self):
        """Test breakdown for simple task (no breakdown needed)."""
        orchestrator = TaskBreakdownOrchestrator()

        task_data = {
            "id": "TASK-001",
            "title": "Simple update",
            "feature_id": "FEAT-001",
            "epic_id": "EPIC-001",
            "files": ["file.py"],
            "patterns": [],
            "dependencies": []
        }

        result = orchestrator.breakdown_task(task_data, threshold_override=7)

        assert result.success is True
        assert result.subtask_count == 0  # No breakdown needed

    def test_breakdown_task_complex(self):
        """Test breakdown for complex task."""
        orchestrator = TaskBreakdownOrchestrator()

        task_data = {
            "id": "TASK-002",
            "title": "Complex feature",
            "feature_id": "FEAT-001",
            "epic_id": "EPIC-001",
            "files": [f"file{i}.py" for i in range(1, 11)],  # 10 files
            "patterns": ["Strategy", "Factory"],
            "dependencies": ["external_api"],
            "description": "Complex implementation with multiple components"
        }

        result = orchestrator.breakdown_task(task_data, threshold_override=5)

        assert result.success is True
        # Should generate subtasks for complex task
        assert result.complexity_score is not None


class TestEndToEndIntegration:
    """Test complete end-to-end workflow."""

    def test_complete_breakdown_workflow(self):
        """Test complete breakdown workflow from feature data to file generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Setup
            orchestrator = TaskBreakdownOrchestrator()
            generator = TaskFileGenerator(project_root=tmpdir)

            # Create task directories
            backlog_dir = Path(tmpdir) / "tasks" / "backlog"
            backlog_dir.mkdir(parents=True, exist_ok=True)

            # Feature data with moderate complexity task
            feature_data = {
                "id": "FEAT-001.1",
                "epic_id": "EPIC-001",
                "title": "User Authentication",
                "technology_stack": "python",
                "tasks": [
                    {
                        "id": "TASK-001.1.01",
                        "title": "Build authentication system",
                        "feature_id": "FEAT-001.1",
                        "epic_id": "EPIC-001",
                        "files": [
                            "auth_service.py",
                            "user_repository.py",
                            "auth_routes.py",
                            "test_auth.py"
                        ],
                        "patterns": ["Repository", "Strategy"],
                        "dependencies": [],
                        "description": "Complete authentication system"
                    }
                ]
            }

            # Step 1: Breakdown feature tasks
            breakdown_result = breakdown_feature_tasks(
                feature_data,
                threshold_override=3  # Low threshold to force breakdown
            )

            assert breakdown_result.success is True

            # Step 2: Generate files if breakdown occurred
            if breakdown_result.requires_breakdown:
                file_metadata = generator.generate_task_files(
                    breakdown_result.subtasks,
                    feature_id=feature_data["id"],
                    epic_id=feature_data["epic_id"],
                    output_dir="tasks/backlog"
                )

                assert len(file_metadata) > 0
                for metadata in file_metadata:
                    assert Path(metadata.file_path).exists()


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])
