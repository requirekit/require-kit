"""
Modification session lifecycle management.

This module manages the lifecycle of an interactive modification session,
coordinating user input, change tracking, and session state.

Architecture:
    - SessionState: Enum representing session lifecycle states
    - ModificationSession: Main coordinator for session lifecycle

Example:
    >>> from modification_session import ModificationSession
    >>> from complexity_models import ImplementationPlan
    >>>
    >>> session = ModificationSession(plan, task_id="TASK-001")
    >>> session.start()
    >>> # User makes changes...
    >>> session.end()
"""

from dataclasses import dataclass
from datetime import datetime, UTC
from enum import Enum
from typing import Optional

try:
    from .change_tracker import ChangeTracker
    from .complexity_models import ImplementationPlan
except ImportError:
    from change_tracker import ChangeTracker
    from complexity_models import ImplementationPlan


class SessionState(Enum):
    """States in modification session lifecycle."""
    IDLE = "idle"  # Session not started
    ACTIVE = "active"  # Session in progress
    COMPLETED = "completed"  # Session ended normally
    CANCELLED = "cancelled"  # Session cancelled by user
    ERROR = "error"  # Session ended due to error


@dataclass
class SessionMetadata:
    """
    Metadata about a modification session.

    Attributes:
        task_id: Task identifier
        session_id: Unique session identifier
        start_time: When session started
        end_time: When session ended (None if active)
        state: Current session state
        user_name: Optional user identifier
        change_count: Number of changes made

    Example:
        >>> metadata = SessionMetadata(
        ...     task_id="TASK-001",
        ...     session_id="session-123",
        ...     start_time=datetime.now(UTC),
        ...     end_time=None,
        ...     state=SessionState.ACTIVE,
        ...     change_count=0
        ... )
    """
    task_id: str
    session_id: str
    start_time: datetime
    end_time: Optional[datetime]
    state: SessionState
    user_name: Optional[str] = None
    change_count: int = 0

    def to_dict(self):
        """Convert metadata to dictionary for serialization."""
        return {
            "task_id": self.task_id,
            "session_id": self.session_id,
            "start_time": self.start_time.isoformat() + "Z",
            "end_time": self.end_time.isoformat() + "Z" if self.end_time else None,
            "state": self.state.value,
            "user_name": self.user_name,
            "change_count": self.change_count,
        }


class ModificationSession:
    """
    Manages lifecycle of an interactive modification session.

    Coordinates session state, change tracking, and provides
    hooks for session lifecycle events (start, end, cancel).

    Example:
        >>> session = ModificationSession(implementation_plan, "TASK-001")
        >>> session.start()
        >>> # Make modifications...
        >>> session.change_tracker.record_file_added("new_file.py")
        >>> session.end()
        >>> print(f"Session completed with {session.metadata.change_count} changes")
    """

    def __init__(
        self,
        plan: ImplementationPlan,
        task_id: str,
        user_name: Optional[str] = None
    ):
        """
        Initialize modification session.

        Args:
            plan: Implementation plan to modify
            task_id: Task identifier
            user_name: Optional user identifier
        """
        self.plan = plan
        self.task_id = task_id
        self.user_name = user_name

        # Session state
        self._state = SessionState.IDLE
        self._session_id = self._generate_session_id()
        self._start_time: Optional[datetime] = None
        self._end_time: Optional[datetime] = None

        # Change tracking
        self.change_tracker = ChangeTracker()

    @property
    def state(self) -> SessionState:
        """Get current session state."""
        return self._state

    @property
    def is_active(self) -> bool:
        """Check if session is currently active."""
        return self._state == SessionState.ACTIVE

    @property
    def is_completed(self) -> bool:
        """Check if session completed successfully."""
        return self._state == SessionState.COMPLETED

    @property
    def is_cancelled(self) -> bool:
        """Check if session was cancelled."""
        return self._state == SessionState.CANCELLED

    @property
    def metadata(self) -> SessionMetadata:
        """
        Get current session metadata.

        Returns:
            SessionMetadata: Current session state and statistics
        """
        return SessionMetadata(
            task_id=self.task_id,
            session_id=self._session_id,
            start_time=self._start_time or datetime.now(UTC),
            end_time=self._end_time,
            state=self._state,
            user_name=self.user_name,
            change_count=self.change_tracker.change_count,
        )

    def start(self) -> None:
        """
        Start modification session.

        Transitions from IDLE to ACTIVE state and records start time.

        Raises:
            RuntimeError: If session already started
        """
        if self._state != SessionState.IDLE:
            raise RuntimeError(
                f"Cannot start session in state {self._state.value}"
            )

        self._state = SessionState.ACTIVE
        self._start_time = datetime.now(UTC)

        print(f"\nStarting modification session: {self._session_id}")
        print(f"Task: {self.task_id}")
        print(f"Time: {self._start_time.isoformat()}\n")

    def end(self, save: bool = True) -> None:
        """
        End modification session normally.

        Transitions from ACTIVE to COMPLETED state and records end time.

        Args:
            save: Whether to save changes (default True)

        Raises:
            RuntimeError: If session not active
        """
        if self._state != SessionState.ACTIVE:
            raise RuntimeError(
                f"Cannot end session in state {self._state.value}"
            )

        self._state = SessionState.COMPLETED
        self._end_time = datetime.now(UTC)

        duration = (self._end_time - self._start_time).total_seconds()

        print(f"\nEnding modification session: {self._session_id}")
        print(f"Duration: {duration:.1f} seconds")
        print(f"Changes: {self.change_tracker.change_count}")
        if save:
            print("Changes will be saved to plan version.")
        print()

    def cancel(self, reason: Optional[str] = None) -> None:
        """
        Cancel modification session.

        Transitions to CANCELLED state. Changes are not saved.

        Args:
            reason: Optional cancellation reason

        Raises:
            RuntimeError: If session not active
        """
        if self._state != SessionState.ACTIVE:
            raise RuntimeError(
                f"Cannot cancel session in state {self._state.value}"
            )

        self._state = SessionState.CANCELLED
        self._end_time = datetime.now(UTC)

        print(f"\nCancelling modification session: {self._session_id}")
        if reason:
            print(f"Reason: {reason}")
        print(f"Changes: {self.change_tracker.change_count} (not saved)")
        print()

    def error(self, error_message: str) -> None:
        """
        Mark session as errored.

        Transitions to ERROR state. Called when unrecoverable error occurs.

        Args:
            error_message: Description of error
        """
        self._state = SessionState.ERROR
        self._end_time = datetime.now(UTC)

        print(f"\nSession error: {self._session_id}")
        print(f"Error: {error_message}")
        print()

    def has_unsaved_changes(self) -> bool:
        """
        Check if session has unsaved changes.

        Returns:
            bool: True if changes exist and session not completed
        """
        return (
            self.change_tracker.change_count > 0
            and self._state != SessionState.COMPLETED
        )

    def get_duration_seconds(self) -> float:
        """
        Get session duration in seconds.

        Returns:
            float: Duration in seconds (0.0 if not started)
        """
        if not self._start_time:
            return 0.0

        end_time = self._end_time or datetime.now(UTC)
        return (end_time - self._start_time).total_seconds()

    def _generate_session_id(self) -> str:
        """
        Generate unique session identifier.

        Returns:
            str: Session ID in format "session-{task_id}-{timestamp}"
        """
        timestamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S%f")
        return f"session-{self.task_id}-{timestamp}"


# Module exports
__all__ = [
    "SessionState",
    "SessionMetadata",
    "ModificationSession",
]
