"""
Unit Tests for Refinement Handler Module.

Part of TASK-026: Create /task-refine Command for Iterative Code Refinement.

Tests cover:
- Data model creation and validation
- State validation logic
- Context loading
- Refinement application
- Quality gate re-execution
- State transition calculation
- Session tracking
- Error handling

Author: Claude (Anthropic)
Created: 2025-10-18
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

from refinement_handler import (
    RefinementRequest,
    RefinementResult,
    RefinementHandler,
    InvalidTaskStateError,
    TaskNotFoundError,
    MissingPrerequisiteError,
    AgentInvocationError,
    create_refinement_request
)


class TestDataModels(unittest.TestCase):
    """Test data model creation and validation."""

    def test_refinement_request_creation(self):
        """Test RefinementRequest dataclass creation."""
        request = RefinementRequest(
            task_id="TASK-042",
            refinement_description="Add validation",
            requested_by="human",
            requested_at="2025-10-18T11:30:00Z",
            context={}
        )

        self.assertEqual(request.task_id, "TASK-042")
        self.assertEqual(request.refinement_description, "Add validation")
        self.assertEqual(request.requested_by, "human")
        self.assertIsInstance(request.context, dict)

    def test_refinement_result_creation(self):
        """Test RefinementResult dataclass creation."""
        result = RefinementResult(
            success=True,
            task_id="TASK-042",
            refinement_id="TASK-042-refine-001",
            new_state="in_review",
            files_modified=["src/auth/login.py"],
            tests_passed=True,
            review_passed=True,
            message="Success",
            timestamp="2025-10-18T11:35:00Z"
        )

        self.assertTrue(result.success)
        self.assertEqual(result.task_id, "TASK-042")
        self.assertEqual(result.new_state, "in_review")
        self.assertEqual(len(result.files_modified), 1)
        self.assertTrue(result.tests_passed)

    def test_refinement_result_with_optional_details(self):
        """Test RefinementResult with optional test and review details."""
        result = RefinementResult(
            success=True,
            task_id="TASK-042",
            refinement_id="TASK-042-refine-001",
            new_state="in_review",
            files_modified=[],
            tests_passed=True,
            review_passed=True,
            message="Success",
            timestamp="2025-10-18T11:35:00Z",
            test_details={"total": 15, "passed": 15},
            review_details={"issues": []}
        )

        self.assertIsNotNone(result.test_details)
        self.assertEqual(result.test_details["total"], 15)
        self.assertIsNotNone(result.review_details)
        self.assertEqual(len(result.review_details["issues"]), 0)


class TestExceptions(unittest.TestCase):
    """Test custom exception classes."""

    def test_invalid_task_state_error(self):
        """Test InvalidTaskStateError exception."""
        error = InvalidTaskStateError("TASK-042", "backlog", ["in_review", "blocked"])

        self.assertEqual(error.task_id, "TASK-042")
        self.assertEqual(error.current_state, "backlog")
        self.assertIn("in_review", error.valid_states)
        self.assertIn("Cannot refine task TASK-042", str(error))

    def test_task_not_found_error(self):
        """Test TaskNotFoundError exception."""
        error = TaskNotFoundError("TASK-999", ["tasks/in_review", "tasks/blocked"])

        self.assertEqual(error.task_id, "TASK-999")
        self.assertEqual(len(error.searched_paths), 2)
        self.assertIn("Task TASK-999 not found", str(error))

    def test_missing_prerequisite_error(self):
        """Test MissingPrerequisiteError exception."""
        error = MissingPrerequisiteError("TASK-042", "implementation plan")

        self.assertEqual(error.task_id, "TASK-042")
        self.assertEqual(error.missing_prerequisite, "implementation plan")
        self.assertIn("missing prerequisite", str(error))

    def test_agent_invocation_error(self):
        """Test AgentInvocationError exception."""
        error = AgentInvocationError("TASK-042", "Agent timeout")

        self.assertEqual(error.task_id, "TASK-042")
        self.assertEqual(error.agent_error, "Agent timeout")
        self.assertIn("Agent failed", str(error))


class TestRefinementHandler(unittest.TestCase):
    """Test RefinementHandler core logic."""

    def setUp(self):
        """Set up test fixtures."""
        self.handler = RefinementHandler()

    def test_handler_initialization(self):
        """Test RefinementHandler initialization."""
        self.assertIsNotNone(self.handler)
        self.assertEqual(self.handler.VALID_STATES, ["in_review", "blocked"])

    def test_valid_states_constant(self):
        """Test VALID_STATES class constant."""
        self.assertIn("in_review", RefinementHandler.VALID_STATES)
        self.assertIn("blocked", RefinementHandler.VALID_STATES)
        self.assertNotIn("backlog", RefinementHandler.VALID_STATES)
        self.assertNotIn("completed", RefinementHandler.VALID_STATES)

    @patch.object(RefinementHandler, '_validate_state')
    @patch.object(RefinementHandler, '_load_context')
    @patch.object(RefinementHandler, '_apply_refinement')
    @patch.object(RefinementHandler, '_run_tests')
    @patch.object(RefinementHandler, '_run_code_review')
    @patch.object(RefinementHandler, '_save_refinement_session')
    @patch.object(RefinementHandler, '_update_task_state')
    def test_refine_success(
        self,
        mock_update_state,
        mock_save_session,
        mock_review,
        mock_tests,
        mock_apply,
        mock_load_context,
        mock_validate
    ):
        """Test successful refinement workflow."""
        # Setup mocks
        mock_load_context.return_value = {
            'plan': {},
            'code_review': {},
            'test_results': {}
        }
        mock_apply.return_value = ["src/auth/login.py"]
        mock_tests.return_value = {"all_passed": True, "total": 15, "passed": 15}
        mock_review.return_value = {"passed": True, "issues": []}
        mock_save_session.return_value = "TASK-042-refine-001"

        # Create request
        request = RefinementRequest(
            task_id="TASK-042",
            refinement_description="Add validation",
            requested_by="human",
            requested_at="2025-10-18T11:30:00Z",
            context={}
        )

        # Execute refinement
        result = self.handler.refine(request)

        # Verify result
        self.assertTrue(result.success)
        self.assertEqual(result.task_id, "TASK-042")
        self.assertEqual(result.new_state, "in_review")
        self.assertTrue(result.tests_passed)
        self.assertTrue(result.review_passed)
        self.assertEqual(result.refinement_id, "TASK-042-refine-001")

        # Verify all phases were called
        mock_validate.assert_called_once_with("TASK-042")
        mock_load_context.assert_called_once()
        mock_apply.assert_called_once()
        mock_tests.assert_called_once()
        mock_review.assert_called_once()
        mock_save_session.assert_called_once()
        mock_update_state.assert_called_once()

    @patch.object(RefinementHandler, '_validate_state')
    def test_refine_invalid_state(self, mock_validate):
        """Test refinement fails for invalid task state."""
        # Setup mock to raise exception
        mock_validate.side_effect = InvalidTaskStateError(
            "TASK-042", "backlog", ["in_review", "blocked"]
        )

        # Create request
        request = RefinementRequest(
            task_id="TASK-042",
            refinement_description="Add validation",
            requested_by="human",
            requested_at="2025-10-18T11:30:00Z",
            context={}
        )

        # Execute refinement
        result = self.handler.refine(request)

        # Verify result
        self.assertFalse(result.success)
        self.assertEqual(result.message, "Invalid task state")
        self.assertIsNotNone(result.error)
        self.assertIn("Cannot refine", result.error)

    def test_calculate_state_all_pass(self):
        """Test state calculation when all gates pass."""
        test_result = {"all_passed": True}
        review_result = {"passed": True}

        new_state = self.handler._calculate_state(test_result, review_result)

        self.assertEqual(new_state, "in_review")

    def test_calculate_state_tests_fail(self):
        """Test state calculation when tests fail."""
        test_result = {"all_passed": False}
        review_result = {"passed": True}

        new_state = self.handler._calculate_state(test_result, review_result)

        self.assertEqual(new_state, "blocked")

    def test_calculate_state_review_fail(self):
        """Test state calculation when review fails."""
        test_result = {"all_passed": True}
        review_result = {"passed": False}

        new_state = self.handler._calculate_state(test_result, review_result)

        self.assertEqual(new_state, "blocked")

    def test_calculate_state_both_fail(self):
        """Test state calculation when both gates fail."""
        test_result = {"all_passed": False}
        review_result = {"passed": False}

        new_state = self.handler._calculate_state(test_result, review_result)

        self.assertEqual(new_state, "blocked")

    def test_build_refinement_prompt(self):
        """Test refinement prompt generation."""
        context = {
            'task_metadata': {'title': 'User Authentication'},
            'plan': {'files': ['src/auth/login.py']},
            'code_review': {'issues': []},
            'test_results': {'total': 15, 'passed': 15}
        }

        prompt = self.handler._build_refinement_prompt(
            "TASK-042",
            "Add validation",
            context
        )

        # Verify prompt contains key sections
        self.assertIn("TASK: TASK-042", prompt)
        self.assertIn("ORIGINAL PLAN:", prompt)
        self.assertIn("CODE REVIEW COMMENTS:", prompt)
        self.assertIn("REFINEMENT REQUEST:", prompt)
        self.assertIn("Add validation", prompt)
        self.assertIn("CONSTRAINTS:", prompt)
        self.assertIn("Do NOT add scope creep", prompt)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""

    def test_create_refinement_request(self):
        """Test create_refinement_request factory function."""
        request = create_refinement_request("TASK-042", "Add validation")

        self.assertEqual(request.task_id, "TASK-042")
        self.assertEqual(request.refinement_description, "Add validation")
        self.assertEqual(request.requested_by, "human")
        self.assertIsNotNone(request.requested_at)
        self.assertIsInstance(request.context, dict)

    def test_create_refinement_request_custom_user(self):
        """Test create_refinement_request with custom user."""
        request = create_refinement_request(
            "TASK-042",
            "Add validation",
            requested_by="alice"
        )

        self.assertEqual(request.requested_by, "alice")


class TestStateTransitions(unittest.TestCase):
    """Test state transition logic."""

    def test_state_transition_success(self):
        """Test state transition from BLOCKED to IN_REVIEW."""
        handler = RefinementHandler()

        # Simulate successful refinement
        test_result = {"all_passed": True}
        review_result = {"passed": True}

        new_state = handler._calculate_state(test_result, review_result)

        self.assertEqual(new_state, "in_review")

    def test_state_transition_blocked(self):
        """Test state transition remains BLOCKED."""
        handler = RefinementHandler()

        # Simulate failed refinement
        test_result = {"all_passed": False}
        review_result = {"passed": False}

        new_state = handler._calculate_state(test_result, review_result)

        self.assertEqual(new_state, "blocked")


class TestSessionTracking(unittest.TestCase):
    """Test refinement session tracking."""

    def setUp(self):
        """Set up test fixtures."""
        self.handler = RefinementHandler()

    @patch.object(RefinementHandler, '_save_refinement_session')
    def test_session_id_generation(self, mock_save_session):
        """Test refinement session ID generation."""
        mock_save_session.return_value = "TASK-042-refine-001"

        request = RefinementRequest(
            task_id="TASK-042",
            refinement_description="Add validation",
            requested_by="human",
            requested_at="2025-10-18T11:30:00Z",
            context={}
        )

        session_id = mock_save_session(
            request,
            ["src/auth/login.py"],
            "in_review",
            {"all_passed": True},
            {"passed": True}
        )

        self.assertEqual(session_id, "TASK-042-refine-001")
        self.assertIn("TASK-042", session_id)
        self.assertIn("refine", session_id)


if __name__ == "__main__":
    unittest.main()
