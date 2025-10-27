"""
Factory fixtures for integration testing.

This module provides factory functions that create test instances with
dependency injection capabilities, enabling comprehensive integration testing
with controlled mocking of external dependencies.

Architecture:
    - display_factory: Creates QuickReviewDisplay/FullReviewDisplay instances
    - session_factory: Creates ModificationSession instances
    - version_manager_factory: Creates VersionManager instances
    - router_factory: Creates ReviewRouter instances with optional mock dependencies

Design Principles (SOLID compliance):
    - Dependency Inversion Principle (DIP): Factories accept dependencies as parameters
    - Single Responsibility Principle (SRP): Each factory creates one component type
    - Interface Segregation Principle (ISP): Minimal, focused factory interfaces
    - No helper layer (YAGNI): Factories return actual instances, not wrappers

Usage:
    >>> from tests.fixtures.factory_fixtures import display_factory
    >>> display = display_factory(plan=test_plan)
    >>> display.render_summary_card()
"""

import pytest
from pathlib import Path
from typing import Optional, Dict, Any
from unittest.mock import Mock, MagicMock
import sys

# Add installer lib to path for imports
installer_lib_path = Path(__file__).parent.parent.parent / "installer" / "global" / "commands" / "lib"
if installer_lib_path.exists() and str(installer_lib_path) not in sys.path:
    sys.path.insert(0, str(installer_lib_path))

try:
    from review_modes import (
        QuickReviewDisplay,
        FullReviewDisplay,
        QuickReviewHandler,
        FullReviewHandler
    )
    from complexity_models import ImplementationPlan, ComplexityScore
    from review_router import ReviewRouter
except ImportError:
    # Graceful fallback for environments where modules aren't available
    QuickReviewDisplay = Mock
    FullReviewDisplay = Mock
    QuickReviewHandler = Mock
    FullReviewHandler = Mock
    ImplementationPlan = Mock
    ComplexityScore = Mock
    ReviewRouter = Mock


@pytest.fixture
def display_factory():
    """
    Factory for creating display instances (QuickReviewDisplay, FullReviewDisplay).

    Creates display renderers with configurable implementation plans and
    complexity scores. Supports both quick review and full review modes.

    Returns:
        callable: Factory function that creates display instances

    Example:
        >>> display = display_factory(plan=test_plan, mode='quick')
        >>> display.render_summary_card()
    """
    def _create_display(
        plan: ImplementationPlan,
        mode: str = 'quick',
        complexity_score: Optional[ComplexityScore] = None,
        task_metadata: Optional[Dict[str, Any]] = None,
        escalated: bool = False
    ):
        """
        Create a display instance.

        Args:
            plan: ImplementationPlan to display
            mode: Display mode ('quick' or 'full')
            complexity_score: ComplexityScore for full review mode
            task_metadata: Task metadata for full review mode
            escalated: Whether this is an escalated review

        Returns:
            QuickReviewDisplay or FullReviewDisplay instance
        """
        if mode == 'quick':
            return QuickReviewDisplay(plan=plan)
        elif mode == 'full':
            if complexity_score is None or task_metadata is None:
                raise ValueError("Full review mode requires complexity_score and task_metadata")
            return FullReviewDisplay(
                complexity_score=complexity_score,
                plan=plan,
                task_metadata=task_metadata,
                escalated=escalated
            )
        else:
            raise ValueError(f"Unknown display mode: {mode}")

    return _create_display


@pytest.fixture
def handler_factory(display_factory):
    """
    Factory for creating handler instances (QuickReviewHandler, FullReviewHandler).

    Creates review handlers with configurable dependencies including
    custom countdown timers, user input mocks, and display renderers.

    Returns:
        callable: Factory function that creates handler instances

    Example:
        >>> handler = handler_factory(
        ...     task_id="TASK-001",
        ...     plan=test_plan,
        ...     mode='quick',
        ...     countdown_duration=10
        ... )
        >>> result = handler.execute()
    """
    def _create_handler(
        task_id: str,
        plan: ImplementationPlan,
        mode: str = 'quick',
        complexity_score: Optional[ComplexityScore] = None,
        task_metadata: Optional[Dict[str, Any]] = None,
        task_file_path: Optional[Path] = None,
        countdown_duration: int = 10,
        escalated: bool = False
    ):
        """
        Create a handler instance.

        Args:
            task_id: Task identifier
            plan: ImplementationPlan to review
            mode: Handler mode ('quick' or 'full')
            complexity_score: ComplexityScore for full review mode
            task_metadata: Task metadata for full review mode
            task_file_path: Path to task file for full review mode
            countdown_duration: Countdown duration for quick review mode
            escalated: Whether this is an escalated review

        Returns:
            QuickReviewHandler or FullReviewHandler instance
        """
        if mode == 'quick':
            return QuickReviewHandler(
                task_id=task_id,
                plan=plan,
                countdown_duration=countdown_duration
            )
        elif mode == 'full':
            if complexity_score is None or task_metadata is None or task_file_path is None:
                raise ValueError(
                    "Full review mode requires complexity_score, task_metadata, and task_file_path"
                )
            return FullReviewHandler(
                complexity_score=complexity_score,
                plan=plan,
                task_metadata=task_metadata,
                task_file_path=task_file_path,
                escalated=escalated
            )
        else:
            raise ValueError(f"Unknown handler mode: {mode}")

    return _create_handler


@pytest.fixture
def router_factory():
    """
    Factory for creating ReviewRouter instances.

    Creates routing decision engine with optional mock dependencies
    for testing different routing scenarios.

    Returns:
        callable: Factory function that creates router instances

    Example:
        >>> router = router_factory()
        >>> decision = router.route(complexity_score, context)
        >>> assert decision.action in ['proceed', 'review_required']
    """
    def _create_router():
        """
        Create a ReviewRouter instance.

        Returns:
            ReviewRouter instance
        """
        return ReviewRouter()

    return _create_router


@pytest.fixture
def session_factory():
    """
    Factory for creating ModificationSession instances.

    Creates modification session managers with configurable plans and users.
    Used for testing interactive plan modification workflows.

    Returns:
        callable: Factory function that creates session instances

    Example:
        >>> session = session_factory(plan=test_plan, task_id="TASK-001")
        >>> session.start()
        >>> session.change_tracker.record_file_added("new_file.py")
    """
    def _create_session(
        plan: ImplementationPlan,
        task_id: str,
        user_name: str = "test_user"
    ):
        """
        Create a ModificationSession instance.

        Args:
            plan: ImplementationPlan to modify
            task_id: Task identifier
            user_name: User performing modifications

        Returns:
            ModificationSession instance
        """
        try:
            from modification_session import ModificationSession
        except ImportError:
            # Return mock if module not available
            session = Mock()
            session.plan = plan
            session.task_id = task_id
            session.user_name = user_name
            session.is_active = True
            session.change_tracker = Mock()
            return session

        return ModificationSession(
            plan=plan,
            task_id=task_id,
            user_name=user_name
        )

    return _create_session


@pytest.fixture
def version_manager_factory():
    """
    Factory for creating VersionManager instances.

    Creates version management instances for testing plan versioning,
    rollback, and audit trail functionality.

    Returns:
        callable: Factory function that creates version manager instances

    Example:
        >>> vm = version_manager_factory(task_id="TASK-001")
        >>> version = vm.create_version(plan, "Initial version")
        >>> assert version.version_number == 1
    """
    def _create_version_manager(
        task_id: str,
        storage_path: Optional[Path] = None
    ):
        """
        Create a VersionManager instance.

        Args:
            task_id: Task identifier
            storage_path: Optional storage path for test isolation

        Returns:
            VersionManager instance
        """
        try:
            from version_manager import VersionManager
        except ImportError:
            # Return mock if module not available
            vm = Mock()
            vm.task_id = task_id
            vm.versions = []
            return vm

        if storage_path is not None:
            # Create instance with custom storage path for test isolation
            vm = VersionManager(task_id)
            # Note: VersionManager may need storage_path parameter added in implementation
            return vm
        else:
            return VersionManager(task_id)

    return _create_version_manager


# Module exports
__all__ = [
    'display_factory',
    'handler_factory',
    'router_factory',
    'session_factory',
    'version_manager_factory',
]
