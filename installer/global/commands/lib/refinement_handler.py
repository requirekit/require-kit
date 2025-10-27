"""
Refinement Handler Module - Enables iterative code refinement for tasks in review.

Part of TASK-026: Create /task-refine Command for Iterative Code Refinement.

This module provides the core logic for refining tasks that have completed implementation
but require adjustments based on code review feedback or human inspection. It enables
John Hubbard's "re-execute as necessary" pattern and Fowler's "small, iterative steps" approach.

Key Features:
- State validation (IN_REVIEW or BLOCKED only)
- Context loading (plan, review, audit, code)
- Targeted refinement application via AI agent
- Quality gate re-execution (tests, fix loop, code review)
- Refinement session tracking

Author: Claude (Anthropic)
Created: 2025-10-18
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import json


# ============================================================================
# Data Models
# ============================================================================

@dataclass
class RefinementRequest:
    """
    Encapsulates a refinement request from a human.

    Attributes:
        task_id: Task identifier (e.g., "TASK-026")
        refinement_description: Human-readable description of what to fix/improve
        requested_by: Username or "human"
        requested_at: ISO 8601 timestamp
        context: Loaded task context (plan, review, code, etc.)

    Example:
        >>> request = RefinementRequest(
        ...     task_id="TASK-042",
        ...     refinement_description="Add input validation to login endpoint",
        ...     requested_by="human",
        ...     requested_at="2025-10-18T11:30:00Z",
        ...     context={}
        ... )
    """
    task_id: str
    refinement_description: str
    requested_by: str
    requested_at: str
    context: Dict[str, Any]


@dataclass
class RefinementResult:
    """
    Encapsulates the outcome of a refinement operation.

    Attributes:
        success: Whether refinement completed successfully
        task_id: Task identifier
        refinement_id: Unique session ID (e.g., "TASK-042-refine-001")
        new_state: New task state after refinement ("in_review" or "blocked")
        files_modified: List of files changed during refinement
        tests_passed: Whether all tests passed after refinement
        review_passed: Whether code review passed after refinement
        message: Human-readable outcome message
        timestamp: ISO 8601 timestamp of completion

        # Optional detailed results (None if not needed)
        test_details: Full test execution results (optional)
        review_details: Full code review results (optional)
        error: Error message if refinement failed (optional)

    Example:
        >>> result = RefinementResult(
        ...     success=True,
        ...     task_id="TASK-042",
        ...     refinement_id="TASK-042-refine-001",
        ...     new_state="in_review",
        ...     files_modified=["src/auth/login.py", "tests/test_login.py"],
        ...     tests_passed=True,
        ...     review_passed=True,
        ...     message="Refinement successful",
        ...     timestamp="2025-10-18T11:35:00Z"
        ... )
    """
    success: bool
    task_id: str
    refinement_id: str
    new_state: str
    files_modified: List[str]
    tests_passed: bool
    review_passed: bool
    message: str
    timestamp: str

    # Optional detailed results
    test_details: Optional[Dict[str, Any]] = None
    review_details: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


# ============================================================================
# Custom Exceptions
# ============================================================================

class RefinementError(Exception):
    """Base exception for refinement errors."""
    pass


class InvalidTaskStateError(RefinementError):
    """Raised when task state is invalid for refinement."""
    def __init__(self, task_id: str, current_state: str, valid_states: List[str]):
        self.task_id = task_id
        self.current_state = current_state
        self.valid_states = valid_states
        message = (
            f"Cannot refine task {task_id} in {current_state} state.\n"
            f"Valid states: {', '.join(valid_states)}"
        )
        super().__init__(message)


class TaskNotFoundError(RefinementError):
    """Raised when task file cannot be found."""
    def __init__(self, task_id: str, searched_paths: List[str]):
        self.task_id = task_id
        self.searched_paths = searched_paths
        message = (
            f"Task {task_id} not found.\n"
            f"Searched in: {', '.join(searched_paths)}"
        )
        super().__init__(message)


class MissingPrerequisiteError(RefinementError):
    """Raised when required prerequisites are missing."""
    def __init__(self, task_id: str, missing_prerequisite: str):
        self.task_id = task_id
        self.missing_prerequisite = missing_prerequisite
        message = (
            f"Task {task_id} is missing prerequisite: {missing_prerequisite}\n"
            f"Run /task-work {task_id} first to complete implementation."
        )
        super().__init__(message)


class AgentInvocationError(RefinementError):
    """Raised when AI agent fails to apply refinement."""
    def __init__(self, task_id: str, agent_error: str):
        self.task_id = task_id
        self.agent_error = agent_error
        message = (
            f"Agent failed to apply refinement to {task_id}:\n"
            f"{agent_error}"
        )
        super().__init__(message)


# ============================================================================
# Refinement Handler
# ============================================================================

class RefinementHandler:
    """
    Orchestrates the refinement workflow for tasks in review.

    Workflow:
        1. Validate task state (IN_REVIEW or BLOCKED)
        2. Load context (plan, review, code)
        3. Apply refinement via AI agent
        4. Re-run quality gates (tests, fix loop, code review)
        5. Calculate new state
        6. Track refinement session

    Example:
        >>> handler = RefinementHandler()
        >>> request = RefinementRequest(...)
        >>> result = handler.refine(request)
        >>> print(f"Refinement {result.refinement_id}: {result.new_state}")
    """

    # Valid task states for refinement
    VALID_STATES = ["in_review", "blocked"]

    def __init__(self):
        """Initialize refinement handler."""
        pass

    def refine(self, request: RefinementRequest) -> RefinementResult:
        """
        Main entry point for refinement workflow.

        Args:
            request: RefinementRequest containing task_id and refinement description

        Returns:
            RefinementResult with outcome details

        Raises:
            InvalidTaskStateError: Task not in valid state
            TaskNotFoundError: Task file not found
            MissingPrerequisiteError: Required prerequisites missing
            AgentInvocationError: Agent failed to apply refinement

        Example:
            >>> request = RefinementRequest(
            ...     task_id="TASK-042",
            ...     refinement_description="Add validation",
            ...     requested_by="human",
            ...     requested_at=datetime.now().isoformat(),
            ...     context={}
            ... )
            >>> result = handler.refine(request)
        """
        try:
            # 1. Validate task state
            self._validate_state(request.task_id)

            # 2. Load context
            context = self._load_context(request.task_id)
            request.context = context

            # 3. Apply refinement
            modified_files = self._apply_refinement(
                request.task_id,
                request.refinement_description,
                context
            )

            # 4. Re-run quality gates
            test_result = self._run_tests(request.task_id)
            review_result = self._run_code_review(request.task_id)

            # 5. Calculate new state
            new_state = self._calculate_state(test_result, review_result)

            # 6. Save refinement session
            refinement_id = self._save_refinement_session(
                request,
                modified_files,
                new_state,
                test_result,
                review_result
            )

            # 7. Update task state
            self._update_task_state(request.task_id, new_state)

            # 8. Build result
            return RefinementResult(
                success=True,
                task_id=request.task_id,
                refinement_id=refinement_id,
                new_state=new_state,
                files_modified=modified_files,
                tests_passed=test_result.get("all_passed", False),
                review_passed=review_result.get("passed", False),
                message=f"Refinement successful: {request.refinement_description}",
                timestamp=datetime.now().isoformat(),
                test_details=test_result,
                review_details=review_result
            )

        except TaskNotFoundError as e:
            return RefinementResult(
                success=False,
                task_id=request.task_id,
                refinement_id="",
                new_state="",
                files_modified=[],
                tests_passed=False,
                review_passed=False,
                message="Task not found",
                timestamp=datetime.now().isoformat(),
                error=str(e)
            )

        except InvalidTaskStateError as e:
            return RefinementResult(
                success=False,
                task_id=request.task_id,
                refinement_id="",
                new_state=e.current_state,
                files_modified=[],
                tests_passed=False,
                review_passed=False,
                message="Invalid task state",
                timestamp=datetime.now().isoformat(),
                error=str(e)
            )

        except MissingPrerequisiteError as e:
            return RefinementResult(
                success=False,
                task_id=request.task_id,
                refinement_id="",
                new_state="",
                files_modified=[],
                tests_passed=False,
                review_passed=False,
                message="Missing prerequisites",
                timestamp=datetime.now().isoformat(),
                error=str(e)
            )

        except AgentInvocationError as e:
            # Refinement failed, but task state remains unchanged
            current_state = self._get_current_state(request.task_id)
            return RefinementResult(
                success=False,
                task_id=request.task_id,
                refinement_id="",
                new_state=current_state,
                files_modified=[],
                tests_passed=False,
                review_passed=False,
                message="Agent failed to apply refinement",
                timestamp=datetime.now().isoformat(),
                error=str(e)
            )

    # ========================================================================
    # Private Methods
    # ========================================================================

    def _validate_state(self, task_id: str) -> None:
        """
        Validate that task is in a valid state for refinement.

        Args:
            task_id: Task identifier

        Raises:
            TaskNotFoundError: Task file not found
            InvalidTaskStateError: Task not in valid state
            MissingPrerequisiteError: Prerequisites missing
        """
        # TODO: Implement task file finding
        # task_file = find_task_file(task_id)
        # if not task_file:
        #     raise TaskNotFoundError(task_id, ["tasks/in_review", "tasks/blocked"])

        # TODO: Parse task metadata
        # metadata = parse_frontmatter(task_file)
        # current_state = metadata.get("status", "unknown")

        # For now, placeholder implementation
        current_state = "in_review"  # Placeholder

        if current_state not in self.VALID_STATES:
            raise InvalidTaskStateError(task_id, current_state, self.VALID_STATES)

        # TODO: Check for implementation plan
        # if not plan_exists(task_id):
        #     raise MissingPrerequisiteError(task_id, "implementation plan")

        # TODO: Check for code files
        # if not code_files_exist(task_id):
        #     raise MissingPrerequisiteError(task_id, "code files")

    def _load_context(self, task_id: str) -> Dict[str, Any]:
        """
        Load full context for refinement.

        Args:
            task_id: Task identifier

        Returns:
            Dictionary containing:
            - plan: Implementation plan (Phase 2.7 output)
            - code_review: Code review results (Phase 5 output)
            - test_results: Test execution results (Phase 4 output)
            - task_metadata: Task frontmatter metadata
            - files_created: List of files created during implementation
        """
        # TODO: Implement context loading
        # return {
        #     'plan': load_implementation_plan(task_id),
        #     'code_review': load_code_review_results(task_id),
        #     'test_results': load_test_results(task_id),
        #     'task_metadata': load_task_metadata(task_id),
        #     'files_created': find_task_files(task_id)
        # }

        # Placeholder
        return {
            'plan': {},
            'code_review': {},
            'test_results': {},
            'task_metadata': {},
            'files_created': []
        }

    def _apply_refinement(
        self,
        task_id: str,
        refinement_description: str,
        context: Dict[str, Any]
    ) -> List[str]:
        """
        Apply refinement to task code via AI agent.

        Args:
            task_id: Task identifier
            refinement_description: What to refine
            context: Full task context

        Returns:
            List of modified file paths

        Raises:
            AgentInvocationError: Agent failed to apply refinement
        """
        # TODO: Build refinement prompt
        prompt = self._build_refinement_prompt(
            task_id,
            refinement_description,
            context
        )

        # TODO: Invoke task-manager agent
        # from .agent_utils import invoke_agent
        # agent_result = invoke_agent("task-manager", prompt)

        # TODO: Extract modified files from agent result
        # modified_files = extract_modified_files(agent_result)

        # Placeholder
        modified_files = []

        return modified_files

    def _build_refinement_prompt(
        self,
        task_id: str,
        refinement_description: str,
        context: Dict[str, Any]
    ) -> str:
        """
        Build context-rich prompt for refinement agent.

        Args:
            task_id: Task identifier
            refinement_description: What to refine
            context: Full task context

        Returns:
            Formatted prompt string
        """
        prompt = f"""You are refining an existing implementation.

TASK: {task_id} - {context.get('task_metadata', {}).get('title', 'Unknown')}

ORIGINAL PLAN:
{json.dumps(context.get('plan', {}), indent=2)}

CODE REVIEW COMMENTS:
{json.dumps(context.get('code_review', {}), indent=2)}

TEST RESULTS:
{json.dumps(context.get('test_results', {}), indent=2)}

REFINEMENT REQUEST:
{refinement_description}

INSTRUCTIONS:
1. Apply ONLY the requested refinement
2. Do NOT change unrelated code
3. Preserve existing patterns and style
4. Update tests if necessary
5. Do NOT add scope creep

CONSTRAINTS:
- Modify existing files only (no new files unless explicitly requested)
- Follow original architectural decisions
- Maintain test coverage
- Fix the specific issue mentioned
- Do NOT introduce new features beyond original scope
"""
        return prompt

    def _run_tests(self, task_id: str) -> Dict[str, Any]:
        """
        Re-run Phase 4 testing.

        Args:
            task_id: Task identifier

        Returns:
            Test execution results
        """
        # TODO: Integrate with phase_execution.py
        # from .phase_execution import execute_phase_4
        # return execute_phase_4(task_id)

        # Placeholder
        return {
            "all_passed": True,
            "total": 15,
            "passed": 15,
            "failed": 0
        }

    def _run_code_review(self, task_id: str) -> Dict[str, Any]:
        """
        Re-run Phase 5 code review.

        Args:
            task_id: Task identifier

        Returns:
            Code review results
        """
        # TODO: Integrate with phase_execution.py
        # from .phase_execution import execute_phase_5
        # return execute_phase_5(task_id)

        # Placeholder
        return {
            "passed": True,
            "issues": []
        }

    def _calculate_state(
        self,
        test_result: Dict[str, Any],
        review_result: Dict[str, Any]
    ) -> str:
        """
        Calculate new task state based on quality gate results.

        Args:
            test_result: Test execution results
            review_result: Code review results

        Returns:
            New state: "in_review" or "blocked"

        Logic:
            - All gates pass → IN_REVIEW
            - Any gate fails → BLOCKED
        """
        tests_passed = test_result.get("all_passed", False)
        review_passed = review_result.get("passed", False)

        if tests_passed and review_passed:
            return "in_review"
        else:
            return "blocked"

    def _save_refinement_session(
        self,
        request: RefinementRequest,
        modified_files: List[str],
        new_state: str,
        test_result: Dict[str, Any],
        review_result: Dict[str, Any]
    ) -> str:
        """
        Save refinement session metadata and append to task changelog.

        Args:
            request: Original refinement request
            modified_files: Files modified during refinement
            new_state: New task state
            test_result: Test execution results
            review_result: Code review results

        Returns:
            Refinement session ID (e.g., "TASK-042-refine-001")
        """
        # TODO: Get next refinement number
        # refinement_number = get_next_refinement_number(request.task_id)
        refinement_number = 1  # Placeholder

        session_id = f"{request.task_id}-refine-{refinement_number:03d}"

        # TODO: Append to task file changelog
        refinement_entry = f"""
## Refinement {refinement_number} - {request.requested_at}
**Description**: {request.refinement_description}
**Outcome**: {'SUCCESS' if new_state == 'in_review' else 'BLOCKED'} → {new_state.upper()}
**Tests Passed**: {test_result.get('passed', 0)}/{test_result.get('total', 0)}
**Review Issues**: {len(review_result.get('issues', []))}
**Files Modified**:
{chr(10).join(f'- {f}' for f in modified_files)}
"""

        # TODO: Update task frontmatter
        refinement_metadata = {
            "session_id": session_id,
            "description": request.refinement_description,
            "requested_at": request.requested_at,
            "outcome": "success" if new_state == "in_review" else "blocked",
            "files_modified": modified_files,
            "tests_passed": test_result.get("all_passed", False),
            "review_passed": review_result.get("passed", False)
        }

        # TODO: Save to task file
        # append_to_task_file(task_file, refinement_entry)
        # update_task_frontmatter(task_file, {"refinements": append_to_list(refinement_metadata)})

        return session_id

    def _update_task_state(self, task_id: str, new_state: str) -> None:
        """
        Update task state in frontmatter and move file if necessary.

        Args:
            task_id: Task identifier
            new_state: New state to transition to
        """
        # TODO: Update task frontmatter
        # update_task_frontmatter(task_id, {"status": new_state})

        # TODO: Move task file if state changed directory
        # current_dir = get_task_directory(task_id)
        # new_dir = f"tasks/{new_state}"
        # if current_dir != new_dir:
        #     move_task_file(task_id, current_dir, new_dir)
        pass

    def _get_current_state(self, task_id: str) -> str:
        """
        Get current task state.

        Args:
            task_id: Task identifier

        Returns:
            Current state string
        """
        # TODO: Parse task frontmatter
        # metadata = parse_frontmatter(find_task_file(task_id))
        # return metadata.get("status", "unknown")

        # Placeholder
        return "in_review"


# ============================================================================
# Utility Functions
# ============================================================================

def create_refinement_request(
    task_id: str,
    description: str,
    requested_by: str = "human"
) -> RefinementRequest:
    """
    Factory function to create a RefinementRequest.

    Args:
        task_id: Task identifier
        description: Refinement description
        requested_by: Username (default: "human")

    Returns:
        RefinementRequest instance

    Example:
        >>> request = create_refinement_request(
        ...     "TASK-042",
        ...     "Add input validation"
        ... )
    """
    return RefinementRequest(
        task_id=task_id,
        refinement_description=description,
        requested_by=requested_by,
        requested_at=datetime.now().isoformat(),
        context={}
    )


# ============================================================================
# Main Entry Point (for CLI testing)
# ============================================================================

if __name__ == "__main__":
    """
    Command-line interface for testing refinement handler.

    Usage:
        python refinement_handler.py TASK-042 "Add validation"
    """
    import sys

    if len(sys.argv) < 3:
        print("Usage: python refinement_handler.py TASK-XXX \"refinement description\"")
        sys.exit(1)

    task_id = sys.argv[1]
    description = sys.argv[2]

    # Create request
    request = create_refinement_request(task_id, description)

    # Execute refinement
    handler = RefinementHandler()
    result = handler.refine(request)

    # Display result
    if result.success:
        print(f"✅ Refinement successful: {result.refinement_id}")
        print(f"   New State: {result.new_state}")
        print(f"   Files Modified: {len(result.files_modified)}")
        print(f"   Tests Passed: {result.tests_passed}")
        print(f"   Review Passed: {result.review_passed}")
    else:
        print(f"❌ Refinement failed: {result.message}")
        if result.error:
            print(f"   Error: {result.error}")
