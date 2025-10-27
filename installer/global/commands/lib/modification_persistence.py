"""
Persistence for modification sessions and changes.

This module handles saving and loading modification sessions,
providing audit trail and recovery capabilities.

Architecture:
    - ModificationPersistence: Manages session/change persistence

Example:
    >>> from modification_persistence import ModificationPersistence
    >>> from modification_session import ModificationSession
    >>>
    >>> persistence = ModificationPersistence(task_id="TASK-001")
    >>> persistence.save_session(session)
    >>> loaded_session = persistence.load_session(session_id)
"""

import json
from pathlib import Path
from typing import Optional

try:
    from .change_tracker import ChangeTracker
except ImportError:
    from change_tracker import ChangeTracker
try:
    from .complexity_models import ImplementationPlan
except ImportError:
    from complexity_models import ImplementationPlan
try:
    from .modification_session import ModificationSession, SessionMetadata
except ImportError:
    from modification_session import ModificationSession, SessionMetadata


class ModificationPersistence:
    """
    Manages persistence of modification sessions and changes.

    Provides save/load functionality for audit trails and recovery.

    Example:
        >>> persistence = ModificationPersistence("TASK-001")
        >>> persistence.save_session(session)
        >>> sessions = persistence.list_sessions()
    """

    def __init__(self, task_id: str, base_dir: Optional[Path] = None):
        """
        Initialize modification persistence.

        Args:
            task_id: Task identifier
            base_dir: Optional custom base directory (defaults to tasks/modifications)
        """
        self.task_id = task_id
        self.base_dir = base_dir or Path("tasks/modifications")
        self.task_dir = self.base_dir / task_id

        # Ensure directories exist
        self.task_dir.mkdir(parents=True, exist_ok=True)

    def save_session(self, session: ModificationSession) -> Path:
        """
        Save modification session to disk.

        Saves session metadata and change history as JSON.

        Args:
            session: ModificationSession to save

        Returns:
            Path: Path to saved session file

        Example:
            >>> path = persistence.save_session(session)
            >>> print(f"Session saved to: {path}")
        """
        session_id = session.metadata.session_id
        session_file = self.task_dir / f"{session_id}.json"

        # Build session data
        session_data = {
            "metadata": session.metadata.to_dict(),
            "change_tracker": session.change_tracker.to_dict(),
        }

        # Write to file
        with open(session_file, "w", encoding="utf-8") as f:
            json.dump(session_data, f, indent=2)

        return session_file

    def load_session(self, session_id: str) -> Optional[ModificationSession]:
        """
        Load modification session from disk.

        Args:
            session_id: Session identifier

        Returns:
            Optional[ModificationSession]: Loaded session or None if not found

        Example:
            >>> session = persistence.load_session("session-TASK-001-20251009")
            >>> if session:
            ...     print(f"Loaded {session.change_tracker.change_count} changes")
        """
        session_file = self.task_dir / f"{session_id}.json"

        if not session_file.exists():
            return None

        try:
            with open(session_file, "r", encoding="utf-8") as f:
                session_data = json.load(f)

            # Reconstruct session (partial reconstruction for read-only access)
            # Note: Cannot fully reconstruct without original plan
            # This is primarily for audit/inspection purposes

            # Create placeholder plan
            placeholder_plan = ImplementationPlan(
                task_id=self.task_id,
                raw_plan="[Plan not available in persisted session]"
            )

            session = ModificationSession(
                plan=placeholder_plan,
                task_id=self.task_id,
                user_name=session_data["metadata"].get("user_name")
            )

            # Restore change tracker
            session.change_tracker = ChangeTracker.from_dict(
                session_data["change_tracker"]
            )

            # Update internal state
            session._session_id = session_data["metadata"]["session_id"]
            session._state = session_data["metadata"]["state"]

            return session

        except Exception as e:
            print(f"Error loading session {session_id}: {e}")
            return None

    def list_sessions(self) -> list:
        """
        List all saved modification sessions for task.

        Returns:
            list: List of session IDs

        Example:
            >>> sessions = persistence.list_sessions()
            >>> for session_id in sessions:
            ...     print(f"Found session: {session_id}")
        """
        if not self.task_dir.exists():
            return []

        session_files = self.task_dir.glob("session-*.json")
        return [f.stem for f in session_files]

    def get_session_metadata(self, session_id: str) -> Optional[dict]:
        """
        Get metadata for a session without loading full session.

        Args:
            session_id: Session identifier

        Returns:
            Optional[dict]: Session metadata or None if not found

        Example:
            >>> metadata = persistence.get_session_metadata("session-TASK-001-20251009")
            >>> if metadata:
            ...     print(f"Changes: {metadata['change_count']}")
        """
        session_file = self.task_dir / f"{session_id}.json"

        if not session_file.exists():
            return None

        try:
            with open(session_file, "r", encoding="utf-8") as f:
                session_data = json.load(f)
            return session_data.get("metadata")
        except Exception:
            return None

    def delete_session(self, session_id: str) -> bool:
        """
        Delete saved modification session.

        Args:
            session_id: Session identifier

        Returns:
            bool: True if deleted, False if not found

        Example:
            >>> if persistence.delete_session("old-session-id"):
            ...     print("Session deleted")
        """
        session_file = self.task_dir / f"{session_id}.json"

        if session_file.exists():
            session_file.unlink()
            return True

        return False

    def save_change_summary(
        self,
        session_id: str,
        summary: str
    ) -> Path:
        """
        Save human-readable change summary.

        Args:
            session_id: Session identifier
            summary: Formatted summary text

        Returns:
            Path: Path to summary file

        Example:
            >>> summary_path = persistence.save_change_summary(
            ...     session_id,
            ...     tracker.get_summary()
            ... )
        """
        summary_file = self.task_dir / f"{session_id}_summary.txt"

        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(summary)

        return summary_file

    def get_latest_session_id(self) -> Optional[str]:
        """
        Get ID of most recent modification session.

        Returns:
            Optional[str]: Latest session ID or None if no sessions

        Example:
            >>> latest = persistence.get_latest_session_id()
            >>> if latest:
            ...     session = persistence.load_session(latest)
        """
        sessions = self.list_sessions()
        if not sessions:
            return None

        # Sort by timestamp in session ID (format: session-TASK-XXX-YYYYMMDDHHMMSS)
        sessions.sort(reverse=True)
        return sessions[0]


# Module exports
__all__ = [
    "ModificationPersistence",
]
