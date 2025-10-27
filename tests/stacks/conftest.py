"""
Stack-specific test configuration and fixtures.

Provides fixtures for testing complexity calculation and pattern detection
across different technology stacks (Python, React, MAUI, NestJS, .NET API).
"""

import pytest
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "installer/global/commands"))

from lib.complexity_models import (
    ImplementationPlan,
    ComplexityScore,
    ReviewMode,
    FactorScore,
)


# Stack-Specific Test Markers
def pytest_configure(config):
    """Register custom markers for stack-specific tests."""
    config.addinivalue_line("markers", "stack: Stack-specific integration tests")
    config.addinivalue_line("markers", "python_api: Python/FastAPI stack tests")
    config.addinivalue_line("markers", "react: React stack tests")
    config.addinivalue_line("markers", "maui: .NET MAUI stack tests")
    config.addinivalue_line("markers", "nestjs: NestJS/TypeScript stack tests")
    config.addinivalue_line("markers", "dotnet_api: .NET API stack tests")


@pytest.fixture
def stack_task_factory():
    """
    Factory for creating stack-specific task specifications.

    Creates realistic tasks for each supported technology stack
    with appropriate patterns, dependencies, and file structures.
    """
    def create_stack_task(stack: str, task_id: str = "TASK-STACK-001") -> Dict:
        """
        Create task specification for a given stack.

        Supported stacks:
        - python_api: FastAPI REST API
        - react: React component with hooks
        - maui: .NET MAUI MVVM mobile app
        - nestjs: NestJS TypeScript API
        - dotnet_api: .NET API with FastEndpoints
        """
        stacks = {
            "python_api": {
                "task_id": task_id,
                "title": "Add user profile endpoint to FastAPI service",
                "description": "Implement GET /users/{id}/profile endpoint with Pydantic validation",
                "stack": "python",
                "files_to_create": [
                    "src/api/routers/user_profile.py",
                    "src/models/user_profile.py",
                    "src/services/profile_service.py",
                    "tests/test_user_profile_api.py",
                ],
                "patterns_used": ["Repository", "Service Layer", "Pydantic"],
                "external_dependencies": ["fastapi", "pydantic", "sqlalchemy"],
                "estimated_loc": 150,
                "risk_indicators": ["database"],
                "expected_patterns_detected": ["FastAPI", "pytest", "Pydantic"],
                "expected_complexity_range": (4, 6),
            },
            "react": {
                "task_id": task_id,
                "title": "Create user profile card component",
                "description": "Build reusable UserProfileCard with hooks and context",
                "stack": "react",
                "files_to_create": [
                    "src/components/UserProfileCard.tsx",
                    "src/hooks/useUserProfile.ts",
                    "src/context/UserContext.tsx",
                    "src/components/__tests__/UserProfileCard.test.tsx",
                ],
                "patterns_used": ["Hooks", "Context API", "Component Composition"],
                "external_dependencies": ["react", "react-query", "@testing-library/react"],
                "estimated_loc": 200,
                "risk_indicators": [],
                "expected_patterns_detected": ["hooks", "context", "state"],
                "expected_complexity_range": (4, 6),
            },
            "maui": {
                "task_id": task_id,
                "title": "Implement login screen with MVVM pattern",
                "description": "Create LoginPage with LoginViewModel and navigation",
                "stack": "maui",
                "files_to_create": [
                    "Views/LoginPage.xaml",
                    "Views/LoginPage.xaml.cs",
                    "ViewModels/LoginViewModel.cs",
                    "UseCases/Authentication/LoginUseCase.cs",
                    "Tests/ViewModels/LoginViewModelTests.cs",
                ],
                "patterns_used": ["MVVM", "UseCase", "ErrorOr"],
                "external_dependencies": ["CommunityToolkit.Mvvm", "ErrorOr"],
                "estimated_loc": 220,
                "risk_indicators": ["authentication"],
                "expected_patterns_detected": ["MVVM", "ErrorOr", "commands"],
                "expected_complexity_range": (5, 7),
            },
            "nestjs": {
                "task_id": task_id,
                "title": "Add product catalog controller with DI",
                "description": "Implement ProductController with dependency injection and DTOs using decorators and result pattern",
                "stack": "nestjs",
                "files_to_create": [
                    "src/products/product.controller.ts",
                    "src/products/dto/create-product.dto.ts",
                    "src/products/product.service.ts",
                    "src/products/product.module.ts",
                    "test/products/product.controller.spec.ts",
                ],
                "patterns_used": ["Dependency Injection", "DTO", "Result Pattern"],
                "external_dependencies": ["@nestjs/common", "class-validator", "neverthrow"],
                "estimated_loc": 180,
                "risk_indicators": [],
                "expected_patterns_detected": ["dependency injection", "dto", "result"],
                "expected_complexity_range": (4, 6),
            },
            "dotnet_api": {
                "task_id": task_id,
                "title": "Create order management endpoint",
                "description": "Implement REPR pattern endpoint with FastEndpoints and Either monad",
                "stack": "dotnet-microservice",
                "files_to_create": [
                    "Features/Orders/CreateOrder/Endpoint.cs",
                    "Features/Orders/CreateOrder/Request.cs",
                    "Features/Orders/CreateOrder/Response.cs",
                    "Features/Orders/CreateOrder/Mapper.cs",
                    "Tests/Features/Orders/CreateOrderTests.cs",
                ],
                "patterns_used": ["REPR", "Either Monad", "Vertical Slice"],
                "external_dependencies": ["FastEndpoints", "LanguageExt.Core", "FluentValidation"],
                "estimated_loc": 190,
                "risk_indicators": [],
                "expected_patterns_detected": ["REPR", "Either", "endpoints"],
                "expected_complexity_range": (4, 6),
            },
        }

        if stack not in stacks:
            raise ValueError(f"Unknown stack: {stack}. Supported: {list(stacks.keys())}")

        return stacks[stack]

    return create_stack_task


@pytest.fixture
def stack_plan_factory():
    """
    Factory for creating ImplementationPlan objects from stack task data.
    """
    def create_plan(task_data: Dict) -> ImplementationPlan:
        """Create ImplementationPlan from stack task data."""
        # Calculate file complexity
        file_count = len(task_data.get("files_to_create", []))
        if file_count <= 2:
            file_score = 1.0
        elif file_count <= 5:
            file_score = 2.0
        else:
            file_score = 3.0

        # Pattern familiarity (stack-specific patterns are moderately familiar)
        pattern_score = 1.5

        # Risk level
        risks = task_data.get("risk_indicators", [])
        if any(r in ["authentication", "security", "payment"] for r in risks):
            risk_score = 3.0
        elif risks:
            risk_score = 2.0
        else:
            risk_score = 1.0

        # Create factor scores
        factor_scores = [
            FactorScore(
                factor_name="File Complexity",
                score=file_score,
                max_score=3.0,
                justification=f"{file_count} files ({task_data.get('stack', 'unknown')} stack)"
            ),
            FactorScore(
                factor_name="Pattern Familiarity",
                score=pattern_score,
                max_score=2.0,
                justification=f"Stack-specific patterns: {', '.join(task_data.get('patterns_used', []))}"
            ),
            FactorScore(
                factor_name="Risk Level",
                score=risk_score,
                max_score=3.0,
                justification=f"Risk indicators: {', '.join(risks) if risks else 'none'}"
            ),
        ]

        total_score = int(sum(f.score for f in factor_scores))

        # Determine review mode based on score
        if total_score <= 3:
            review_mode = ReviewMode.AUTO_PROCEED
        elif total_score <= 6:
            review_mode = ReviewMode.QUICK_OPTIONAL
        else:
            review_mode = ReviewMode.FULL_REQUIRED

        # Create complexity score
        complexity_score = ComplexityScore(
            total_score=total_score,
            factor_scores=factor_scores,
            forced_review_triggers=[],
            review_mode=review_mode,
            calculation_timestamp=datetime.utcnow(),
            metadata={"stack": task_data.get("stack", "unknown")}
        )

        # Create implementation plan
        plan = ImplementationPlan(
            task_id=task_data["task_id"],
            files_to_create=task_data.get("files_to_create", []),
            patterns_used=task_data.get("patterns_used", []),
            external_dependencies=task_data.get("external_dependencies", []),
            estimated_loc=task_data.get("estimated_loc", 0),
            risk_indicators=task_data.get("risk_indicators", []),
            raw_plan=task_data.get("description", ""),
            test_summary=f"{task_data.get('stack', 'unknown')} stack tests",
            risk_details=[],
            phases=[],
            implementation_instructions=task_data.get("description", ""),
            estimated_duration="2 hours",
            complexity_score=complexity_score
        )

        return plan

    return create_plan


@pytest.fixture
def pattern_detection_validator():
    """
    Validator for stack-specific pattern detection.

    Verifies that the system correctly identifies technology-specific
    patterns, dependencies, and file structures.
    """
    def validate_patterns(plan: ImplementationPlan, expected_patterns: List[str]) -> Dict:
        """
        Validate that expected patterns are detected in the plan.

        Returns dict with:
        - patterns_found: List of detected patterns
        - patterns_missing: List of expected but not found
        - detection_rate: Percentage of patterns found
        """
        plan_text = (
            plan.raw_plan.lower() + " " +
            " ".join(plan.patterns_used).lower() + " " +
            " ".join(plan.files_to_create).lower() + " " +
            " ".join(plan.external_dependencies).lower()
        )

        patterns_found = []
        patterns_missing = []

        for pattern in expected_patterns:
            if pattern.lower() in plan_text:
                patterns_found.append(pattern)
            else:
                patterns_missing.append(pattern)

        detection_rate = (len(patterns_found) / len(expected_patterns) * 100) if expected_patterns else 0

        return {
            "patterns_found": patterns_found,
            "patterns_missing": patterns_missing,
            "detection_rate": detection_rate,
            "total_expected": len(expected_patterns),
            "total_found": len(patterns_found),
        }

    return validate_patterns


@pytest.fixture
def complexity_range_validator():
    """
    Validator for complexity score ranges.

    Ensures calculated complexity falls within expected range for stack.
    """
    def validate_complexity(actual_score: int, expected_range: tuple) -> Dict:
        """
        Validate complexity score is within expected range.

        Returns dict with:
        - in_range: Boolean indicating if score is in range
        - actual_score: The calculated score
        - expected_range: The expected (min, max) range
        - deviation: How far outside range (0 if in range)
        """
        min_score, max_score = expected_range
        in_range = min_score <= actual_score <= max_score

        if actual_score < min_score:
            deviation = min_score - actual_score
        elif actual_score > max_score:
            deviation = actual_score - max_score
        else:
            deviation = 0

        return {
            "in_range": in_range,
            "actual_score": actual_score,
            "expected_range": expected_range,
            "expected_min": min_score,
            "expected_max": max_score,
            "deviation": deviation,
        }

    return validate_complexity


@pytest.fixture
def stack_file_structure_validator():
    """
    Validator for stack-specific file structure conventions.

    Verifies files follow technology-specific naming and organization patterns.
    """
    def validate_structure(files: List[str], stack: str) -> Dict:
        """
        Validate file structure follows stack conventions.

        Returns dict with:
        - valid: Boolean indicating if structure is valid
        - conventions_followed: List of conventions followed
        - conventions_violated: List of conventions violated
        """
        conventions = {
            "python": [
                ("snake_case", all("_" in f or f.isupper() or "/" in f for f in files if ".py" in f)),
                ("test_prefix", any(f.startswith("test") or "/test" in f for f in files if ".py" in f)),
                ("src_directory", any(f.startswith("src/") for f in files)),
            ],
            "react": [
                ("PascalCase_components", any(f[0].isupper() if f else False for f in files if ".tsx" in f or ".jsx" in f)),
                ("test_suffix", any(".test." in f or ".spec." in f for f in files)),
                ("typescript", any(".ts" in f or ".tsx" in f for f in files)),
            ],
            "maui": [
                ("PascalCase", all(f.split("/")[-1][0].isupper() if f.split("/")[-1] else False for f in files if ".cs" in f)),
                ("xaml_codebehind", any(".xaml.cs" in f for f in files) or not any(".xaml" in f for f in files)),
                ("Tests_directory", any("Tests/" in f or "Test" in f for f in files if "Test" in f)),
            ],
            "nestjs": [
                ("kebab-case", any("-" in f for f in files if ".ts" in f)),
                ("spec_suffix", any(".spec.ts" in f for f in files)),
                ("module_pattern", any(".module.ts" in f for f in files)),
            ],
            "dotnet-microservice": [
                ("PascalCase", all(f.split("/")[-1][0].isupper() if f.split("/")[-1] else False for f in files if ".cs" in f)),
                ("Features_structure", any("Features/" in f for f in files)),
                ("Tests_directory", any("Tests/" in f for f in files if "Test" in f)),
            ],
        }

        stack_conventions = conventions.get(stack, [])
        conventions_followed = [name for name, check in stack_conventions if check]
        conventions_violated = [name for name, check in stack_conventions if not check]

        return {
            "valid": len(conventions_violated) == 0,
            "conventions_followed": conventions_followed,
            "conventions_violated": conventions_violated,
            "compliance_rate": (len(conventions_followed) / len(stack_conventions) * 100) if stack_conventions else 100,
        }

    return validate_structure
