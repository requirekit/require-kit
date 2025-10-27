"""
Change tracking for plan modifications.

This module records all modifications made during an interactive editing session,
maintaining a complete audit trail of changes for versioning and rollback.

Architecture:
    - Change: Individual change record (add/remove/modify)
    - ChangeTracker: Aggregates and manages changes during session

Example:
    >>> from change_tracker import ChangeTracker, ChangeType
    >>>
    >>> tracker = ChangeTracker()
    >>> tracker.record_file_added("new_file.py", "Purpose: API handler")
    >>> tracker.record_dependency_removed("old-library")
    >>> print(tracker.get_summary())
"""

from dataclasses import dataclass, field
from datetime import datetime, UTC
from enum import Enum
from typing import Any, Dict, List, Optional


class ChangeType(Enum):
    """Types of changes that can be tracked."""
    FILE_ADDED = "file_added"
    FILE_REMOVED = "file_removed"
    FILE_MODIFIED = "file_modified"
    DEPENDENCY_ADDED = "dependency_added"
    DEPENDENCY_REMOVED = "dependency_removed"
    PHASE_ADDED = "phase_added"
    PHASE_REMOVED = "phase_removed"
    PHASE_REORDERED = "phase_reordered"
    RISK_ADDED = "risk_added"
    RISK_MODIFIED = "risk_modified"
    RISK_REMOVED = "risk_removed"
    METADATA_UPDATED = "metadata_updated"


@dataclass(frozen=True)
class Change:
    """
    Individual change record.

    Captures a single modification with full context for audit trails
    and potential rollback operations.

    Attributes:
        change_type: Type of change (add/remove/modify)
        timestamp: When change was made
        target: What was changed (file path, dependency name, etc.)
        old_value: Previous value (None for additions)
        new_value: New value (None for removals)
        metadata: Additional context (reason, user input, etc.)

    Example:
        >>> change = Change(
        ...     change_type=ChangeType.FILE_ADDED,
        ...     timestamp=datetime.now(UTC),
        ...     target="api/handlers.py",
        ...     old_value=None,
        ...     new_value="Purpose: REST API handlers",
        ...     metadata={"estimated_loc": 150}
        ... )
    """
    change_type: ChangeType
    timestamp: datetime
    target: str
    old_value: Optional[Any] = None
    new_value: Optional[Any] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert change to dictionary for serialization.

        Returns:
            Dict[str, Any]: JSON-serializable dictionary
        """
        return {
            "change_type": self.change_type.value,
            "timestamp": self.timestamp.isoformat() + "Z",
            "target": self.target,
            "old_value": self.old_value,
            "new_value": self.new_value,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Change":
        """
        Create change from dictionary.

        Args:
            data: Dictionary with change fields

        Returns:
            Change: Reconstructed change object
        """
        return cls(
            change_type=ChangeType(data["change_type"]),
            timestamp=datetime.fromisoformat(data["timestamp"].rstrip("Z")),
            target=data["target"],
            old_value=data.get("old_value"),
            new_value=data.get("new_value"),
            metadata=data.get("metadata", {}),
        )

    def describe(self) -> str:
        """
        Generate human-readable description of change.

        Returns:
            str: Formatted change description
        """
        if self.change_type == ChangeType.FILE_ADDED:
            return f"Added file: {self.target}"
        elif self.change_type == ChangeType.FILE_REMOVED:
            return f"Removed file: {self.target}"
        elif self.change_type == ChangeType.FILE_MODIFIED:
            return f"Modified file: {self.target}"
        elif self.change_type == ChangeType.DEPENDENCY_ADDED:
            return f"Added dependency: {self.target}"
        elif self.change_type == ChangeType.DEPENDENCY_REMOVED:
            return f"Removed dependency: {self.target}"
        elif self.change_type == ChangeType.PHASE_ADDED:
            return f"Added phase: {self.target}"
        elif self.change_type == ChangeType.PHASE_REMOVED:
            return f"Removed phase: {self.target}"
        elif self.change_type == ChangeType.PHASE_REORDERED:
            return f"Reordered phases: {self.old_value} -> {self.new_value}"
        elif self.change_type == ChangeType.RISK_ADDED:
            return f"Added risk: {self.target}"
        elif self.change_type == ChangeType.RISK_MODIFIED:
            return f"Modified risk: {self.target}"
        elif self.change_type == ChangeType.RISK_REMOVED:
            return f"Removed risk: {self.target}"
        elif self.change_type == ChangeType.METADATA_UPDATED:
            return f"Updated {self.target}: {self.old_value} -> {self.new_value}"
        else:
            return f"Unknown change: {self.change_type.value}"


class ChangeTracker:
    """
    Aggregates and manages changes during modification session.

    Maintains a chronological list of all changes with methods for
    querying, summarizing, and persisting the change history.

    Example:
        >>> tracker = ChangeTracker()
        >>> tracker.record_file_added("api.py", "API handlers")
        >>> tracker.record_dependency_added("requests", "HTTP client")
        >>> print(f"Total changes: {tracker.change_count}")
        >>> print(tracker.get_summary())
    """

    def __init__(self):
        """Initialize empty change tracker."""
        self._changes: List[Change] = []
        self._session_start = datetime.now(UTC)

    @property
    def changes(self) -> List[Change]:
        """Get all recorded changes (read-only)."""
        return list(self._changes)

    @property
    def change_count(self) -> int:
        """Get total number of changes recorded."""
        return len(self._changes)

    @property
    def is_empty(self) -> bool:
        """Check if no changes have been recorded."""
        return len(self._changes) == 0

    def record_file_added(
        self,
        file_path: str,
        purpose: Optional[str] = None,
        estimated_loc: Optional[int] = None
    ) -> None:
        """
        Record file addition.

        Args:
            file_path: Path to file being added
            purpose: Optional description of file purpose
            estimated_loc: Optional estimated lines of code
        """
        metadata = {}
        if purpose:
            metadata["purpose"] = purpose
        if estimated_loc:
            metadata["estimated_loc"] = estimated_loc

        change = Change(
            change_type=ChangeType.FILE_ADDED,
            timestamp=datetime.now(UTC),
            target=file_path,
            old_value=None,
            new_value=purpose,
            metadata=metadata,
        )
        self._changes.append(change)

    def record_file_removed(self, file_path: str, reason: Optional[str] = None) -> None:
        """
        Record file removal.

        Args:
            file_path: Path to file being removed
            reason: Optional reason for removal
        """
        metadata = {}
        if reason:
            metadata["reason"] = reason

        change = Change(
            change_type=ChangeType.FILE_REMOVED,
            timestamp=datetime.now(UTC),
            target=file_path,
            old_value=file_path,
            new_value=None,
            metadata=metadata,
        )
        self._changes.append(change)

    def record_file_modified(
        self,
        file_path: str,
        old_purpose: Optional[str] = None,
        new_purpose: Optional[str] = None
    ) -> None:
        """
        Record file modification.

        Args:
            file_path: Path to file being modified
            old_purpose: Previous purpose/description
            new_purpose: New purpose/description
        """
        change = Change(
            change_type=ChangeType.FILE_MODIFIED,
            timestamp=datetime.now(UTC),
            target=file_path,
            old_value=old_purpose,
            new_value=new_purpose,
        )
        self._changes.append(change)

    def record_dependency_added(
        self,
        dependency: str,
        purpose: Optional[str] = None
    ) -> None:
        """
        Record dependency addition.

        Args:
            dependency: Dependency name/package
            purpose: Optional reason for adding dependency
        """
        metadata = {}
        if purpose:
            metadata["purpose"] = purpose

        change = Change(
            change_type=ChangeType.DEPENDENCY_ADDED,
            timestamp=datetime.now(UTC),
            target=dependency,
            old_value=None,
            new_value=dependency,
            metadata=metadata,
        )
        self._changes.append(change)

    def record_dependency_removed(
        self,
        dependency: str,
        reason: Optional[str] = None
    ) -> None:
        """
        Record dependency removal.

        Args:
            dependency: Dependency name/package
            reason: Optional reason for removal
        """
        metadata = {}
        if reason:
            metadata["reason"] = reason

        change = Change(
            change_type=ChangeType.DEPENDENCY_REMOVED,
            timestamp=datetime.now(UTC),
            target=dependency,
            old_value=dependency,
            new_value=None,
            metadata=metadata,
        )
        self._changes.append(change)

    def record_phase_added(self, phase_description: str, position: int) -> None:
        """
        Record phase addition.

        Args:
            phase_description: Description of new phase
            position: Position in phase list (0-indexed)
        """
        change = Change(
            change_type=ChangeType.PHASE_ADDED,
            timestamp=datetime.now(UTC),
            target=phase_description,
            old_value=None,
            new_value=phase_description,
            metadata={"position": position},
        )
        self._changes.append(change)

    def record_phase_removed(self, phase_description: str, position: int) -> None:
        """
        Record phase removal.

        Args:
            phase_description: Description of removed phase
            position: Position in phase list (0-indexed)
        """
        change = Change(
            change_type=ChangeType.PHASE_REMOVED,
            timestamp=datetime.now(UTC),
            target=phase_description,
            old_value=phase_description,
            new_value=None,
            metadata={"position": position},
        )
        self._changes.append(change)

    def record_metadata_updated(
        self,
        field_name: str,
        old_value: Any,
        new_value: Any
    ) -> None:
        """
        Record metadata field update.

        Args:
            field_name: Name of metadata field
            old_value: Previous value
            new_value: New value
        """
        change = Change(
            change_type=ChangeType.METADATA_UPDATED,
            timestamp=datetime.now(UTC),
            target=field_name,
            old_value=old_value,
            new_value=new_value,
        )
        self._changes.append(change)

    def get_changes_by_type(self, change_type: ChangeType) -> List[Change]:
        """
        Get all changes of specific type.

        Args:
            change_type: Type of changes to retrieve

        Returns:
            List[Change]: Matching changes in chronological order
        """
        return [c for c in self._changes if c.change_type == change_type]

    def get_summary(self) -> str:
        """
        Generate human-readable summary of all changes.

        Returns:
            str: Formatted summary text
        """
        if self.is_empty:
            return "No changes recorded"

        lines = [
            f"Change Summary ({self.change_count} changes)",
            "=" * 60,
        ]

        # Group changes by type
        change_groups: Dict[ChangeType, List[Change]] = {}
        for change in self._changes:
            if change.change_type not in change_groups:
                change_groups[change.change_type] = []
            change_groups[change.change_type].append(change)

        # Display each group
        for change_type, changes in sorted(change_groups.items(), key=lambda x: x[0].value):
            lines.append(f"\n{change_type.value.replace('_', ' ').title()}:")
            for change in changes:
                lines.append(f"  - {change.describe()}")

        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert tracker to dictionary for serialization.

        Returns:
            Dict[str, Any]: JSON-serializable dictionary
        """
        return {
            "session_start": self._session_start.isoformat() + "Z",
            "change_count": self.change_count,
            "changes": [c.to_dict() for c in self._changes],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChangeTracker":
        """
        Create tracker from dictionary.

        Args:
            data: Dictionary with tracker fields

        Returns:
            ChangeTracker: Reconstructed tracker object
        """
        tracker = cls()
        tracker._session_start = datetime.fromisoformat(
            data["session_start"].rstrip("Z")
        )
        tracker._changes = [Change.from_dict(c) for c in data["changes"]]
        return tracker


# Module exports
__all__ = [
    "ChangeType",
    "Change",
    "ChangeTracker",
]
