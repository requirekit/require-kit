"""
Stack-specific complexity calculation and pattern detection tests.

Tests that the complexity calculation system correctly handles
technology-specific patterns, dependencies, and file structures
across 5 different technology stacks.

Stacks Tested:
1. Python API (FastAPI + pytest + Pydantic)
2. React (TypeScript + hooks + context)
3. MAUI (.NET MAUI + MVVM + ErrorOr)
4. NestJS (TypeScript + DI + decorators)
5. .NET API (FastEndpoints + REPR + Either)
"""

import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "installer/global/commands"))

from lib.complexity_models import ReviewMode


@pytest.mark.stack
@pytest.mark.python_api
class TestPythonAPIStack:
    """
    Tests for Python/FastAPI stack.

    Validates:
    - FastAPI REST API pattern detection
    - Pydantic model recognition
    - pytest testing framework
    - Repository and Service Layer patterns
    """

    def test_python_api_plan_generation(
        self,
        stack_task_factory,
        stack_plan_factory
    ):
        """Test plan generation for Python API task."""
        # GIVEN: Python API task
        task_data = stack_task_factory("python_api")

        # WHEN: Plan is generated
        plan = stack_plan_factory(task_data)

        # THEN: Plan contains Python-specific structure
        assert plan.task_id == task_data["task_id"]
        assert len(plan.files_to_create) == 4
        assert any("router" in f for f in plan.files_to_create)
        assert any("model" in f for f in plan.files_to_create)
        assert any("service" in f for f in plan.files_to_create)
        assert any("test" in f for f in plan.files_to_create)

    def test_python_api_pattern_detection(
        self,
        stack_task_factory,
        stack_plan_factory,
        pattern_detection_validator
    ):
        """Test FastAPI pattern detection."""
        # GIVEN: Python API task with expected patterns
        task_data = stack_task_factory("python_api")
        plan = stack_plan_factory(task_data)

        # WHEN: Patterns are validated
        expected_patterns = task_data["expected_patterns_detected"]
        result = pattern_detection_validator(plan, expected_patterns)

        # THEN: Core FastAPI patterns are detected
        assert "FastAPI" in result["patterns_found"] or "fastapi" in " ".join(plan.external_dependencies).lower()
        assert "Pydantic" in result["patterns_found"] or "pydantic" in " ".join(plan.external_dependencies).lower()
        assert result["detection_rate"] >= 60  # At least 60% patterns detected

    def test_python_api_complexity_calculation(
        self,
        stack_task_factory,
        stack_plan_factory,
        complexity_range_validator
    ):
        """Test complexity calculation for Python API."""
        # GIVEN: Python API task
        task_data = stack_task_factory("python_api")
        plan = stack_plan_factory(task_data)

        # WHEN: Complexity is validated
        expected_range = task_data["expected_complexity_range"]
        result = complexity_range_validator(plan.complexity_score.total_score, expected_range)

        # THEN: Complexity is in expected range
        assert result["in_range"], \
            f"Complexity {result['actual_score']} outside range {result['expected_range']}"
        assert plan.complexity_score.review_mode in [ReviewMode.QUICK_OPTIONAL, ReviewMode.FULL_REQUIRED]

    def test_python_api_file_structure(
        self,
        stack_task_factory,
        stack_file_structure_validator
    ):
        """Test Python file structure conventions."""
        # GIVEN: Python API task files
        task_data = stack_task_factory("python_api")
        files = task_data["files_to_create"]

        # WHEN: Structure is validated
        result = stack_file_structure_validator(files, "python")

        # THEN: Python conventions are followed
        assert result["compliance_rate"] >= 66  # At least 2/3 conventions
        assert "src_directory" in result["conventions_followed"]

    def test_python_api_dependencies(
        self,
        stack_task_factory,
        stack_plan_factory
    ):
        """Test Python API dependency detection."""
        # GIVEN: Python API task
        task_data = stack_task_factory("python_api")
        plan = stack_plan_factory(task_data)

        # THEN: Core dependencies are present
        deps_lower = [d.lower() for d in plan.external_dependencies]
        assert "fastapi" in deps_lower
        assert "pydantic" in deps_lower
        assert len(plan.external_dependencies) >= 2


@pytest.mark.stack
@pytest.mark.react
class TestReactStack:
    """
    Tests for React/TypeScript stack.

    Validates:
    - React component patterns
    - Hooks usage detection
    - Context API recognition
    - TypeScript file structure
    """

    def test_react_plan_generation(
        self,
        stack_task_factory,
        stack_plan_factory
    ):
        """Test plan generation for React task."""
        # GIVEN: React task
        task_data = stack_task_factory("react")

        # WHEN: Plan is generated
        plan = stack_plan_factory(task_data)

        # THEN: Plan contains React-specific structure
        assert len(plan.files_to_create) == 4
        assert any(".tsx" in f for f in plan.files_to_create)
        assert any("component" in f.lower() for f in plan.files_to_create)
        assert any("hook" in f.lower() for f in plan.files_to_create)
        assert any("context" in f.lower() for f in plan.files_to_create)

    def test_react_pattern_detection(
        self,
        stack_task_factory,
        stack_plan_factory,
        pattern_detection_validator
    ):
        """Test React pattern detection."""
        # GIVEN: React task with expected patterns
        task_data = stack_task_factory("react")
        plan = stack_plan_factory(task_data)

        # WHEN: Patterns are validated
        expected_patterns = task_data["expected_patterns_detected"]
        result = pattern_detection_validator(plan, expected_patterns)

        # THEN: Core React patterns are detected
        assert result["detection_rate"] >= 60
        assert len(result["patterns_found"]) >= 2

    def test_react_complexity_calculation(
        self,
        stack_task_factory,
        stack_plan_factory,
        complexity_range_validator
    ):
        """Test complexity calculation for React."""
        # GIVEN: React task
        task_data = stack_task_factory("react")
        plan = stack_plan_factory(task_data)

        # WHEN: Complexity is validated
        expected_range = task_data["expected_complexity_range"]
        result = complexity_range_validator(plan.complexity_score.total_score, expected_range)

        # THEN: Complexity is in expected range
        assert result["in_range"], \
            f"Complexity {result['actual_score']} outside range {result['expected_range']}"

    def test_react_file_structure(
        self,
        stack_task_factory,
        stack_file_structure_validator
    ):
        """Test React file structure conventions."""
        # GIVEN: React task files
        task_data = stack_task_factory("react")
        files = task_data["files_to_create"]

        # WHEN: Structure is validated
        result = stack_file_structure_validator(files, "react")

        # THEN: React conventions are followed
        assert result["compliance_rate"] >= 66
        assert "typescript" in result["conventions_followed"]

    def test_react_dependencies(
        self,
        stack_task_factory,
        stack_plan_factory
    ):
        """Test React dependency detection."""
        # GIVEN: React task
        task_data = stack_task_factory("react")
        plan = stack_plan_factory(task_data)

        # THEN: Core React dependencies are present
        deps_lower = [d.lower() for d in plan.external_dependencies]
        assert "react" in deps_lower
        assert len(plan.external_dependencies) >= 2


@pytest.mark.stack
@pytest.mark.maui
class TestMAUIStack:
    """
    Tests for .NET MAUI stack.

    Validates:
    - MVVM pattern detection
    - ErrorOr result type usage
    - XAML file structure
    - UseCase pattern recognition
    """

    def test_maui_plan_generation(
        self,
        stack_task_factory,
        stack_plan_factory
    ):
        """Test plan generation for MAUI task."""
        # GIVEN: MAUI task
        task_data = stack_task_factory("maui")

        # WHEN: Plan is generated
        plan = stack_plan_factory(task_data)

        # THEN: Plan contains MAUI-specific structure
        assert len(plan.files_to_create) == 5
        assert any(".xaml" in f for f in plan.files_to_create)
        assert any("ViewModel" in f for f in plan.files_to_create)
        assert any("UseCase" in f for f in plan.files_to_create)
        assert any("Test" in f for f in plan.files_to_create)

    def test_maui_pattern_detection(
        self,
        stack_task_factory,
        stack_plan_factory,
        pattern_detection_validator
    ):
        """Test MAUI pattern detection."""
        # GIVEN: MAUI task with expected patterns
        task_data = stack_task_factory("maui")
        plan = stack_plan_factory(task_data)

        # WHEN: Patterns are validated
        expected_patterns = task_data["expected_patterns_detected"]
        result = pattern_detection_validator(plan, expected_patterns)

        # THEN: Core MAUI patterns are detected
        assert "MVVM" in result["patterns_found"]
        assert result["detection_rate"] >= 60

    def test_maui_complexity_calculation(
        self,
        stack_task_factory,
        stack_plan_factory,
        complexity_range_validator
    ):
        """Test complexity calculation for MAUI."""
        # GIVEN: MAUI task
        task_data = stack_task_factory("maui")
        plan = stack_plan_factory(task_data)

        # WHEN: Complexity is validated
        expected_range = task_data["expected_complexity_range"]
        result = complexity_range_validator(plan.complexity_score.total_score, expected_range)

        # THEN: Complexity is in expected range
        assert result["in_range"], \
            f"Complexity {result['actual_score']} outside range {result['expected_range']}"
        # MAUI tasks often require full review due to mobile complexity
        assert plan.complexity_score.review_mode in [ReviewMode.QUICK_OPTIONAL, ReviewMode.FULL_REQUIRED]

    def test_maui_file_structure(
        self,
        stack_task_factory,
        stack_file_structure_validator
    ):
        """Test MAUI file structure conventions."""
        # GIVEN: MAUI task files
        task_data = stack_task_factory("maui")
        files = task_data["files_to_create"]

        # WHEN: Structure is validated
        result = stack_file_structure_validator(files, "maui")

        # THEN: MAUI conventions are followed
        assert result["compliance_rate"] >= 66
        assert "PascalCase" in result["conventions_followed"]

    def test_maui_dependencies(
        self,
        stack_task_factory,
        stack_plan_factory
    ):
        """Test MAUI dependency detection."""
        # GIVEN: MAUI task
        task_data = stack_task_factory("maui")
        plan = stack_plan_factory(task_data)

        # THEN: Core MAUI dependencies are present
        assert "ErrorOr" in plan.external_dependencies
        assert len(plan.external_dependencies) >= 1


@pytest.mark.stack
@pytest.mark.nestjs
class TestNestJSStack:
    """
    Tests for NestJS/TypeScript stack.

    Validates:
    - Dependency Injection pattern
    - Decorator usage
    - DTO pattern recognition
    - Module structure
    """

    def test_nestjs_plan_generation(
        self,
        stack_task_factory,
        stack_plan_factory
    ):
        """Test plan generation for NestJS task."""
        # GIVEN: NestJS task
        task_data = stack_task_factory("nestjs")

        # WHEN: Plan is generated
        plan = stack_plan_factory(task_data)

        # THEN: Plan contains NestJS-specific structure
        assert len(plan.files_to_create) == 5
        assert any(".controller.ts" in f for f in plan.files_to_create)
        assert any(".service.ts" in f for f in plan.files_to_create)
        assert any(".module.ts" in f for f in plan.files_to_create)
        assert any("dto" in f.lower() for f in plan.files_to_create)

    def test_nestjs_pattern_detection(
        self,
        stack_task_factory,
        stack_plan_factory,
        pattern_detection_validator
    ):
        """Test NestJS pattern detection."""
        # GIVEN: NestJS task with expected patterns
        task_data = stack_task_factory("nestjs")
        plan = stack_plan_factory(task_data)

        # WHEN: Patterns are validated
        expected_patterns = task_data["expected_patterns_detected"]
        result = pattern_detection_validator(plan, expected_patterns)

        # THEN: Core NestJS patterns are detected
        assert result["detection_rate"] >= 60
        assert len(result["patterns_found"]) >= 2

    def test_nestjs_complexity_calculation(
        self,
        stack_task_factory,
        stack_plan_factory,
        complexity_range_validator
    ):
        """Test complexity calculation for NestJS."""
        # GIVEN: NestJS task
        task_data = stack_task_factory("nestjs")
        plan = stack_plan_factory(task_data)

        # WHEN: Complexity is validated
        expected_range = task_data["expected_complexity_range"]
        result = complexity_range_validator(plan.complexity_score.total_score, expected_range)

        # THEN: Complexity is in expected range
        assert result["in_range"], \
            f"Complexity {result['actual_score']} outside range {result['expected_range']}"

    def test_nestjs_file_structure(
        self,
        stack_task_factory,
        stack_file_structure_validator
    ):
        """Test NestJS file structure conventions."""
        # GIVEN: NestJS task files
        task_data = stack_task_factory("nestjs")
        files = task_data["files_to_create"]

        # WHEN: Structure is validated
        result = stack_file_structure_validator(files, "nestjs")

        # THEN: NestJS conventions are followed
        assert result["compliance_rate"] >= 66
        assert "module_pattern" in result["conventions_followed"]

    def test_nestjs_dependencies(
        self,
        stack_task_factory,
        stack_plan_factory
    ):
        """Test NestJS dependency detection."""
        # GIVEN: NestJS task
        task_data = stack_task_factory("nestjs")
        plan = stack_plan_factory(task_data)

        # THEN: Core NestJS dependencies are present
        deps_lower = [d.lower() for d in plan.external_dependencies]
        assert any("nestjs" in d for d in deps_lower)
        assert len(plan.external_dependencies) >= 2


@pytest.mark.stack
@pytest.mark.dotnet_api
class TestDotNetAPIStack:
    """
    Tests for .NET API stack (FastEndpoints).

    Validates:
    - REPR pattern recognition
    - Either monad usage
    - Vertical Slice Architecture
    - FastEndpoints structure
    """

    def test_dotnet_api_plan_generation(
        self,
        stack_task_factory,
        stack_plan_factory
    ):
        """Test plan generation for .NET API task."""
        # GIVEN: .NET API task
        task_data = stack_task_factory("dotnet_api")

        # WHEN: Plan is generated
        plan = stack_plan_factory(task_data)

        # THEN: Plan contains .NET API-specific structure
        assert len(plan.files_to_create) == 5
        assert any("Endpoint.cs" in f for f in plan.files_to_create)
        assert any("Request.cs" in f for f in plan.files_to_create)
        assert any("Response.cs" in f for f in plan.files_to_create)
        assert any("Features/" in f for f in plan.files_to_create)

    def test_dotnet_api_pattern_detection(
        self,
        stack_task_factory,
        stack_plan_factory,
        pattern_detection_validator
    ):
        """Test .NET API pattern detection."""
        # GIVEN: .NET API task with expected patterns
        task_data = stack_task_factory("dotnet_api")
        plan = stack_plan_factory(task_data)

        # WHEN: Patterns are validated
        expected_patterns = task_data["expected_patterns_detected"]
        result = pattern_detection_validator(plan, expected_patterns)

        # THEN: Core .NET API patterns are detected
        assert "REPR" in result["patterns_found"]
        assert result["detection_rate"] >= 60

    def test_dotnet_api_complexity_calculation(
        self,
        stack_task_factory,
        stack_plan_factory,
        complexity_range_validator
    ):
        """Test complexity calculation for .NET API."""
        # GIVEN: .NET API task
        task_data = stack_task_factory("dotnet_api")
        plan = stack_plan_factory(task_data)

        # WHEN: Complexity is validated
        expected_range = task_data["expected_complexity_range"]
        result = complexity_range_validator(plan.complexity_score.total_score, expected_range)

        # THEN: Complexity is in expected range
        assert result["in_range"], \
            f"Complexity {result['actual_score']} outside range {result['expected_range']}"

    def test_dotnet_api_file_structure(
        self,
        stack_task_factory,
        stack_file_structure_validator
    ):
        """Test .NET API file structure conventions."""
        # GIVEN: .NET API task files
        task_data = stack_task_factory("dotnet_api")
        files = task_data["files_to_create"]

        # WHEN: Structure is validated
        result = stack_file_structure_validator(files, "dotnet-microservice")

        # THEN: .NET API conventions are followed
        assert result["compliance_rate"] >= 66
        assert "Features_structure" in result["conventions_followed"]

    def test_dotnet_api_dependencies(
        self,
        stack_task_factory,
        stack_plan_factory
    ):
        """Test .NET API dependency detection."""
        # GIVEN: .NET API task
        task_data = stack_task_factory("dotnet_api")
        plan = stack_plan_factory(task_data)

        # THEN: Core .NET API dependencies are present
        assert "FastEndpoints" in plan.external_dependencies
        assert len(plan.external_dependencies) >= 2


@pytest.mark.stack
class TestCrossStackValidation:
    """
    Cross-stack validation tests.

    Validates that different stacks have distinct characteristics
    and the system correctly differentiates between them.
    """

    def test_all_stacks_generate_valid_plans(
        self,
        stack_task_factory,
        stack_plan_factory
    ):
        """Test that all stacks generate valid plans."""
        stacks = ["python_api", "react", "maui", "nestjs", "dotnet_api"]

        for stack in stacks:
            # GIVEN: Task for each stack
            task_data = stack_task_factory(stack)
            plan = stack_plan_factory(task_data)

            # THEN: Plan is valid
            assert plan.task_id is not None
            assert len(plan.files_to_create) > 0
            assert plan.complexity_score is not None
            assert plan.complexity_score.total_score > 0

    def test_stacks_have_distinct_patterns(
        self,
        stack_task_factory,
        stack_plan_factory
    ):
        """Test that each stack uses distinct patterns."""
        stacks = {
            "python_api": ["Repository", "Pydantic"],
            "react": ["Hooks", "Context API"],
            "maui": ["MVVM", "ErrorOr"],
            "nestjs": ["Dependency Injection", "DTO"],
            "dotnet_api": ["REPR", "Either Monad"],
        }

        for stack_name, expected_patterns in stacks.items():
            # GIVEN: Task for stack
            task_data = stack_task_factory(stack_name)
            plan = stack_plan_factory(task_data)

            # THEN: Stack-specific patterns are present
            plan_patterns = plan.patterns_used
            assert any(p in plan_patterns for p in expected_patterns), \
                f"Stack '{stack_name}' missing expected patterns: {expected_patterns}"

    def test_stacks_have_appropriate_file_counts(
        self,
        stack_task_factory,
        stack_plan_factory
    ):
        """Test that stack file counts are reasonable."""
        stacks = ["python_api", "react", "maui", "nestjs", "dotnet_api"]

        for stack in stacks:
            # GIVEN: Task for stack
            task_data = stack_task_factory(stack)
            plan = stack_plan_factory(task_data)

            # THEN: File count is reasonable (4-5 files for standard tasks)
            assert 4 <= len(plan.files_to_create) <= 6, \
                f"Stack '{stack}' has unexpected file count: {len(plan.files_to_create)}"

    def test_complexity_scores_are_consistent(
        self,
        stack_task_factory,
        stack_plan_factory
    ):
        """Test that complexity scores are consistent across stacks."""
        stacks = ["python_api", "react", "maui", "nestjs", "dotnet_api"]
        scores = []

        for stack in stacks:
            # GIVEN: Task for each stack
            task_data = stack_task_factory(stack)
            plan = stack_plan_factory(task_data)
            scores.append(plan.complexity_score.total_score)

        # THEN: All scores are in similar range (4-7 for standard tasks)
        assert all(4 <= score <= 7 for score in scores), \
            f"Inconsistent scores across stacks: {scores}"
        assert max(scores) - min(scores) <= 2, \
            f"Too much variance in scores: {scores}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
