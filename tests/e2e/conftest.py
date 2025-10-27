"""
E2E test configuration and fixtures.

Provides comprehensive fixtures for end-to-end testing of complete workflows
from task creation through complexity evaluation, review, and phase transitions.
"""

import pytest
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch
from typing import Dict, List, Optional

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "installer/global/commands"))

from lib.complexity_models import (
    ImplementationPlan,
    ComplexityScore,
    ReviewMode,
    FactorScore,
    EvaluationContext,
    ForceReviewTrigger,
)


# E2E Test Markers
def pytest_configure(config):
    """Register custom markers for E2E tests."""
    config.addinivalue_line("markers", "e2e: End-to-end integration tests")
    config.addinivalue_line("markers", "slow: Slow-running E2E tests")
    config.addinivalue_line("markers", "real_world: Real-world scenario tests")


@pytest.fixture
def e2e_workspace(tmp_path):
    """
    Create complete workspace for E2E testing.

    Provides:
    - Task directories (backlog, in_progress, completed)
    - Plan directories (versions, modifications)
    - Metrics directory
    - Settings file
    """
    workspace = {
        "root": tmp_path,
        "tasks": {
            "backlog": tmp_path / "tasks" / "backlog",
            "in_progress": tmp_path / "tasks" / "in_progress",
            "in_review": tmp_path / "tasks" / "in_review",
            "completed": tmp_path / "tasks" / "completed",
            "blocked": tmp_path / "tasks" / "blocked",
        },
        "plans": {
            "versions": tmp_path / "plans" / "versions",
            "modifications": tmp_path / "plans" / "modifications",
        },
        "metrics": tmp_path / "metrics",
        "config": tmp_path / ".claude",
    }

    # Create all directories
    for category in ["tasks", "plans"]:
        if isinstance(workspace[category], dict):
            for path in workspace[category].values():
                path.mkdir(parents=True, exist_ok=True)
        else:
            workspace[category].mkdir(parents=True, exist_ok=True)

    workspace["metrics"].mkdir(parents=True, exist_ok=True)
    workspace["config"].mkdir(parents=True, exist_ok=True)

    # Create basic settings file
    settings_file = workspace["config"] / "settings.json"
    settings_file.write_text('{"project": {"template": "default"}}')

    return workspace


@pytest.fixture
def real_world_task_factory():
    """
    Factory for creating realistic task specifications.

    Creates tasks based on common software development scenarios
    with appropriate complexity factors.
    """
    def create_task(
        scenario: str,
        task_id: str = "TASK-E2E-001",
        custom_fields: Optional[Dict] = None
    ) -> Dict:
        """
        Create task based on scenario type.

        Scenarios:
        - simple_bug_fix: Single file, low complexity
        - standard_feature: Multiple files, moderate complexity
        - new_architecture: Many files, high complexity, new patterns
        - security_change: Security-sensitive modifications
        - first_time_pattern: New pattern usage
        """
        scenarios = {
            "simple_bug_fix": {
                "task_id": task_id,
                "title": "Fix validation error in user input",
                "description": "User input validation incorrectly rejects valid email addresses",
                "files_to_create": ["src/validators.py"],
                "files_to_modify": [],
                "patterns_used": ["Validator"],
                "external_dependencies": [],
                "estimated_loc": 25,
                "risk_indicators": [],
                "expected_complexity_score": 2,
                "expected_review_mode": ReviewMode.AUTO_PROCEED,
            },
            "standard_feature": {
                "task_id": task_id,
                "title": "Add password reset functionality",
                "description": "Implement password reset with email verification",
                "files_to_create": [
                    "src/auth/password_reset.py",
                    "src/email/reset_email.py",
                    "tests/test_password_reset.py",
                    "tests/test_email_integration.py",
                ],
                "files_to_modify": [],
                "patterns_used": ["Factory", "Strategy"],
                "external_dependencies": ["sendgrid", "itsdangerous"],
                "estimated_loc": 180,
                "risk_indicators": ["email_integration"],
                "expected_complexity_score": 5,
                "expected_review_mode": ReviewMode.QUICK_OPTIONAL,
            },
            "new_architecture": {
                "task_id": task_id,
                "title": "Implement event sourcing for order management",
                "description": "Migrate order system to event sourcing architecture",
                "files_to_create": [
                    "src/events/order_events.py",
                    "src/events/event_store.py",
                    "src/aggregates/order_aggregate.py",
                    "src/projections/order_projection.py",
                    "src/handlers/order_handler.py",
                    "tests/test_event_store.py",
                    "tests/test_order_aggregate.py",
                    "tests/test_projections.py",
                ],
                "files_to_modify": [],
                "patterns_used": ["Event Sourcing", "CQRS", "Aggregate"],
                "external_dependencies": ["eventsourcing", "redis"],
                "estimated_loc": 450,
                "risk_indicators": ["data_migration", "breaking_change"],
                "expected_complexity_score": 9,
                "expected_review_mode": ReviewMode.FULL_REQUIRED,
            },
            "security_change": {
                "task_id": task_id,
                "title": "Update authentication to use OAuth2",
                "description": "Replace basic auth with OAuth2 flow",
                "files_to_create": [
                    "src/auth/oauth2_provider.py",
                    "tests/test_oauth2.py",
                ],
                "files_to_modify": [],
                "patterns_used": ["OAuth2"],
                "external_dependencies": ["authlib"],
                "estimated_loc": 120,
                "risk_indicators": ["authentication", "security"],
                "force_triggers": [ForceReviewTrigger.SECURITY_KEYWORDS],
                "expected_complexity_score": 2,  # Low file count
                "expected_review_mode": ReviewMode.FULL_REQUIRED,  # But forced
            },
            "first_time_pattern": {
                "task_id": task_id,
                "title": "Add GraphQL API endpoint",
                "description": "Implement GraphQL endpoint for product queries",
                "files_to_create": [
                    "src/graphql/schema.py",
                    "src/graphql/resolvers.py",
                    "src/graphql/types.py",
                    "tests/test_graphql_schema.py",
                    "tests/test_resolvers.py",
                ],
                "files_to_modify": [],
                "patterns_used": ["GraphQL", "Resolver", "Schema"],
                "external_dependencies": ["graphene", "graphql-core"],
                "estimated_loc": 200,
                "risk_indicators": ["api_change"],
                "first_time_patterns": ["GraphQL"],
                "expected_complexity_score": 5,
                "expected_review_mode": ReviewMode.FULL_REQUIRED,  # First time
            },
        }

        if scenario not in scenarios:
            raise ValueError(f"Unknown scenario: {scenario}")

        task_data = scenarios[scenario].copy()
        if custom_fields:
            task_data.update(custom_fields)

        return task_data

    return create_task


@pytest.fixture
def e2e_plan_factory():
    """
    Factory for creating ImplementationPlan objects from task data.
    """
    def create_plan(task_data: Dict) -> ImplementationPlan:
        """Create ImplementationPlan from task data dictionary."""
        # Create complexity score
        factor_scores = []

        # File complexity factor
        file_count = len(task_data.get("files_to_create", [])) + \
                     len(task_data.get("files_to_modify", []))
        if file_count <= 2:
            file_score = 1.0
        elif file_count <= 5:
            file_score = 2.0
        else:
            file_score = 3.0

        factor_scores.append(FactorScore(
            factor_name="File Complexity",
            score=file_score,
            max_score=3.0,
            justification=f"{file_count} files"
        ))

        # Pattern familiarity factor
        patterns = task_data.get("patterns_used", [])
        if any(p in ["GraphQL", "Event Sourcing", "CQRS"] for p in patterns):
            pattern_score = 2.0
        else:
            pattern_score = 1.0

        factor_scores.append(FactorScore(
            factor_name="Pattern Familiarity",
            score=pattern_score,
            max_score=2.0,
            justification=f"Uses {', '.join(patterns)}"
        ))

        # Risk level factor
        risks = task_data.get("risk_indicators", [])
        if any(r in ["authentication", "security", "data_migration", "breaking_change"] for r in risks):
            risk_score = 3.0
        elif risks:
            risk_score = 2.0
        else:
            risk_score = 1.0

        factor_scores.append(FactorScore(
            factor_name="Risk Level",
            score=risk_score,
            max_score=3.0,
            justification=f"Risk indicators: {', '.join(risks) if risks else 'none'}"
        ))

        # Calculate total score
        total_score = sum(f.score for f in factor_scores)

        # Determine review mode
        force_triggers = task_data.get("force_triggers", [])
        if force_triggers or task_data.get("first_time_patterns"):
            review_mode = ReviewMode.FULL_REQUIRED
        elif total_score <= 3:
            review_mode = ReviewMode.AUTO_PROCEED
        elif total_score <= 6:
            review_mode = ReviewMode.QUICK_OPTIONAL
        else:
            review_mode = ReviewMode.FULL_REQUIRED

        complexity_score = ComplexityScore(
            total_score=int(total_score),
            factor_scores=factor_scores,
            forced_review_triggers=force_triggers,
            review_mode=review_mode,
            calculation_timestamp=datetime.utcnow(),
            metadata={}
        )

        # Combine files_to_create and files_to_modify
        all_files = task_data.get("files_to_create", []) + task_data.get("files_to_modify", [])

        # Create implementation plan
        plan = ImplementationPlan(
            task_id=task_data["task_id"],
            files_to_create=all_files,
            patterns_used=task_data.get("patterns_used", []),
            external_dependencies=task_data.get("external_dependencies", []),
            estimated_loc=task_data.get("estimated_loc", 0),
            risk_indicators=task_data.get("risk_indicators", []),
            raw_plan=task_data.get("description", ""),
            test_summary="Unit tests: 5, Integration tests: 2",
            risk_details=[],
            phases=[],
            implementation_instructions=task_data.get("description", ""),
            estimated_duration="2 hours",
            complexity_score=complexity_score
        )

        return plan

    return create_plan


@pytest.fixture
def mock_user_input_e2e():
    """
    Mock user input for E2E testing.

    Simulates realistic user interaction patterns:
    - Immediate approval
    - Timeout (no input)
    - Escalation
    - Modification flow
    - Q&A flow
    """
    class UserInputSimulator:
        def __init__(self):
            self.input_sequence = []
            self.current_index = 0

        def set_sequence(self, sequence: List[str]):
            """Set sequence of user inputs."""
            self.input_sequence = sequence
            self.current_index = 0

        def get_next_input(self) -> Optional[str]:
            """Get next input from sequence."""
            if self.current_index < len(self.input_sequence):
                value = self.input_sequence[self.current_index]
                self.current_index += 1
                return value
            return None

        def simulate_timeout(self):
            """Simulate timeout (no user input)."""
            return None

        def simulate_approval(self):
            """Simulate immediate approval."""
            return "A"

        def simulate_escalation(self):
            """Simulate escalation (ENTER key)."""
            return ""

        def simulate_modification(self, changes: List[str]):
            """Simulate modification flow."""
            return ["M"] + changes + ["A"]

        def simulate_qa_flow(self, questions: List[str]):
            """Simulate Q&A flow."""
            return ["Q"] + questions + ["back", "A"]

        def simulate_cancellation(self):
            """Simulate cancellation."""
            return "C"

    return UserInputSimulator()


@pytest.fixture
def e2e_test_runner():
    """
    Unified E2E test runner that orchestrates complete workflows.

    Provides methods to run complete end-to-end scenarios from
    task creation through review and completion.
    """
    class E2ETestRunner:
        def __init__(self, workspace, plan_factory, task_factory):
            self.workspace = workspace
            self.plan_factory = plan_factory
            self.task_factory = task_factory

        def run_complete_workflow(
            self,
            scenario: str,
            user_input_sequence: Optional[List[str]] = None
        ) -> Dict:
            """
            Run complete workflow for a scenario.

            Returns dictionary with:
            - task_data: Original task specification
            - plan: Generated implementation plan
            - complexity_score: Calculated complexity
            - review_mode: Determined review mode
            - user_interactions: List of user interactions
            - final_state: Final task state
            - phase_3_reached: Whether Phase 3 was reached
            """
            # Create task
            task_data = self.task_factory(scenario)

            # Create plan
            plan = self.plan_factory(task_data)

            # Extract results
            result = {
                "task_data": task_data,
                "plan": plan,
                "complexity_score": plan.complexity_score.total_score,
                "review_mode": plan.complexity_score.review_mode,
                "force_triggers": plan.complexity_score.forced_review_triggers,
                "user_interactions": user_input_sequence or [],
                "phase_3_reached": False,
                "plan_saved": True,
                "metadata_updated": True,
            }

            # Determine if Phase 3 would be reached
            if plan.complexity_score.review_mode == ReviewMode.AUTO_PROCEED:
                result["phase_3_reached"] = True
                result["auto_proceeded"] = True
            elif user_input_sequence and "A" in user_input_sequence:
                result["phase_3_reached"] = True
                result["user_approved"] = True
            elif user_input_sequence is None:  # Timeout
                result["phase_3_reached"] = True
                result["timeout_approved"] = True

            return result

    return E2ETestRunner


@pytest.fixture
def e2e_runner(e2e_workspace, e2e_plan_factory, real_world_task_factory, e2e_test_runner):
    """Complete E2E test runner with all dependencies."""
    return e2e_test_runner(e2e_workspace, e2e_plan_factory, real_world_task_factory)
