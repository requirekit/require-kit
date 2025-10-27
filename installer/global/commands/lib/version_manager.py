"""
Version management for implementation plans.

This module implements the Memento Pattern for plan versioning, allowing
plans to evolve through modifications with full version history and metadata.

Architecture:
    - PlanVersion: Memento storing plan snapshot with metadata
    - VersionManager: Caretaker managing version history

Example:
    >>> from version_manager import VersionManager
    >>> from complexity_models import ImplementationPlan
    >>>
    >>> manager = VersionManager(task_id="TASK-001")
    >>> version = manager.create_version(plan, "Initial plan")
    >>> plan_v2 = manager.get_latest_version()
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

try:
    from .complexity_models import ImplementationPlan, ComplexityScore
except ImportError:
    from complexity_models import ImplementationPlan, ComplexityScore


@dataclass
class PlanVersion:
    """
    Memento storing implementation plan snapshot.

    Captures plan state at a point in time with metadata about
    the version (creation time, reason, author, etc.).

    Attributes:
        version_number: Sequential version number (1, 2, 3, ...)
        plan: Implementation plan snapshot
        created_at: When version was created
        created_by: Who created version (user or system)
        change_reason: Why version was created
        previous_version: Previous version number (None for v1)
        metadata: Additional context

    Example:
        >>> version = PlanVersion(
        ...     version_number=2,
        ...     plan=modified_plan,
        ...     created_at=datetime.utcnow(),
        ...     created_by="user",
        ...     change_reason="Added error handling file",
        ...     previous_version=1
        ... )
    """
    version_number: int
    plan: ImplementationPlan
    created_at: datetime
    created_by: str
    change_reason: str
    previous_version: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert version to dictionary for serialization.

        Returns:
            Dict[str, Any]: JSON-serializable dictionary
        """
        return {
            "version_number": self.version_number,
            "plan": self._serialize_plan(self.plan),
            "created_at": self.created_at.isoformat() + "Z",
            "created_by": self.created_by,
            "change_reason": self.change_reason,
            "previous_version": self.previous_version,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PlanVersion":
        """
        Create version from dictionary.

        Args:
            data: Dictionary with version fields

        Returns:
            PlanVersion: Reconstructed version object
        """
        return cls(
            version_number=data["version_number"],
            plan=cls._deserialize_plan(data["plan"]),
            created_at=datetime.fromisoformat(data["created_at"].rstrip("Z")),
            created_by=data["created_by"],
            change_reason=data["change_reason"],
            previous_version=data.get("previous_version"),
            metadata=data.get("metadata", {}),
        )

    @staticmethod
    def _serialize_plan(plan: ImplementationPlan) -> Dict[str, Any]:
        """
        Serialize implementation plan to dictionary.

        Args:
            plan: Plan to serialize

        Returns:
            Dict[str, Any]: Serialized plan
        """
        return {
            "task_id": plan.task_id,
            "files_to_create": plan.files_to_create,
            "patterns_used": plan.patterns_used,
            "external_dependencies": plan.external_dependencies,
            "estimated_loc": plan.estimated_loc,
            "risk_indicators": plan.risk_indicators,
            "raw_plan": plan.raw_plan,
            "test_summary": plan.test_summary,
            "risk_details": plan.risk_details,
            "phases": plan.phases,
            "implementation_instructions": plan.implementation_instructions,
            "estimated_duration": plan.estimated_duration,
            # Note: complexity_score not serialized (calculated fresh)
        }

    @staticmethod
    def _deserialize_plan(data: Dict[str, Any]) -> ImplementationPlan:
        """
        Deserialize implementation plan from dictionary.

        Args:
            data: Serialized plan data

        Returns:
            ImplementationPlan: Reconstructed plan
        """
        return ImplementationPlan(
            task_id=data["task_id"],
            files_to_create=data.get("files_to_create", []),
            patterns_used=data.get("patterns_used", []),
            external_dependencies=data.get("external_dependencies", []),
            estimated_loc=data.get("estimated_loc"),
            risk_indicators=data.get("risk_indicators", []),
            raw_plan=data.get("raw_plan", ""),
            test_summary=data.get("test_summary"),
            risk_details=data.get("risk_details"),
            phases=data.get("phases"),
            implementation_instructions=data.get("implementation_instructions"),
            estimated_duration=data.get("estimated_duration"),
            complexity_score=None,  # Recalculate if needed
        )

    def get_summary(self) -> str:
        """
        Generate human-readable version summary.

        Returns:
            str: Formatted summary
        """
        lines = [
            f"Version {self.version_number}",
            f"Created: {self.created_at.isoformat()}",
            f"By: {self.created_by}",
            f"Reason: {self.change_reason}",
        ]

        if self.previous_version:
            lines.append(f"Previous: v{self.previous_version}")

        # Plan statistics
        lines.append(f"Files: {len(self.plan.files_to_create)}")
        lines.append(f"Dependencies: {len(self.plan.external_dependencies)}")

        if self.plan.estimated_loc:
            lines.append(f"Est. LOC: {self.plan.estimated_loc}")

        return "\n".join(lines)


class VersionManager:
    """
    Manages version history for implementation plans.

    Implements Caretaker role in Memento Pattern, maintaining
    sequential versions with persistence and query capabilities.

    Example:
        >>> manager = VersionManager("TASK-001")
        >>> v1 = manager.create_version(initial_plan, "Initial plan")
        >>> v2 = manager.create_version(modified_plan, "Added error handling")
        >>> history = manager.get_version_history()
        >>> latest = manager.get_latest_version()
    """

    def __init__(self, task_id: str, base_dir: Optional[Path] = None):
        """
        Initialize version manager.

        Args:
            task_id: Task identifier
            base_dir: Optional custom base directory (defaults to tasks/versions)
        """
        self.task_id = task_id
        self.base_dir = base_dir or Path("tasks/versions")
        self.task_dir = self.base_dir / task_id

        # Ensure directories exist
        self.task_dir.mkdir(parents=True, exist_ok=True)

        # Load existing versions
        self._versions: Dict[int, PlanVersion] = {}
        self._load_versions()

    def create_version(
        self,
        plan: ImplementationPlan,
        change_reason: str,
        created_by: str = "user"
    ) -> PlanVersion:
        """
        Create new plan version.

        Args:
            plan: Implementation plan to version
            change_reason: Reason for creating version
            created_by: Who created version (default "user")

        Returns:
            PlanVersion: Newly created version

        Example:
            >>> version = manager.create_version(
            ...     modified_plan,
            ...     "Added error handling file"
            ... )
            >>> print(f"Created version {version.version_number}")
        """
        # Determine version number
        version_number = self._get_next_version_number()

        # Get previous version number
        previous_version = version_number - 1 if version_number > 1 else None

        # Create version
        version = PlanVersion(
            version_number=version_number,
            plan=plan,
            created_at=datetime.utcnow(),
            created_by=created_by,
            change_reason=change_reason,
            previous_version=previous_version,
            metadata={
                "task_id": self.task_id,
                "file_count": len(plan.files_to_create),
                "dependency_count": len(plan.external_dependencies),
            }
        )

        # Save version
        self._save_version(version)

        # Add to cache
        self._versions[version_number] = version

        return version

    def get_version(self, version_number: int) -> Optional[PlanVersion]:
        """
        Get specific plan version.

        Args:
            version_number: Version number to retrieve

        Returns:
            Optional[PlanVersion]: Version or None if not found

        Example:
            >>> version = manager.get_version(2)
            >>> if version:
            ...     print(version.change_reason)
        """
        return self._versions.get(version_number)

    def get_latest_version(self) -> Optional[PlanVersion]:
        """
        Get most recent plan version.

        Returns:
            Optional[PlanVersion]: Latest version or None if no versions

        Example:
            >>> latest = manager.get_latest_version()
            >>> if latest:
            ...     print(f"Current version: {latest.version_number}")
        """
        if not self._versions:
            return None

        max_version = max(self._versions.keys())
        return self._versions[max_version]

    def get_version_history(self) -> List[PlanVersion]:
        """
        Get all versions in chronological order.

        Returns:
            List[PlanVersion]: All versions sorted by version number

        Example:
            >>> history = manager.get_version_history()
            >>> for version in history:
            ...     print(f"v{version.version_number}: {version.change_reason}")
        """
        return [
            self._versions[v]
            for v in sorted(self._versions.keys())
        ]

    def get_version_count(self) -> int:
        """
        Get total number of versions.

        Returns:
            int: Number of versions
        """
        return len(self._versions)

    def compare_versions(
        self,
        version_a: int,
        version_b: int
    ) -> Dict[str, Any]:
        """
        Compare two versions.

        Args:
            version_a: First version number
            version_b: Second version number

        Returns:
            Dict[str, Any]: Comparison results

        Example:
            >>> diff = manager.compare_versions(1, 2)
            >>> print(f"Files added: {diff['files_added']}")
            >>> print(f"Files removed: {diff['files_removed']}")
        """
        va = self.get_version(version_a)
        vb = self.get_version(version_b)

        if not va or not vb:
            return {"error": "One or both versions not found"}

        # Compare files
        files_a = set(va.plan.files_to_create)
        files_b = set(vb.plan.files_to_create)

        # Compare dependencies
        deps_a = set(va.plan.external_dependencies)
        deps_b = set(vb.plan.external_dependencies)

        return {
            "version_a": version_a,
            "version_b": version_b,
            "files_added": list(files_b - files_a),
            "files_removed": list(files_a - files_b),
            "files_unchanged": list(files_a & files_b),
            "dependencies_added": list(deps_b - deps_a),
            "dependencies_removed": list(deps_a - deps_b),
            "dependencies_unchanged": list(deps_a & deps_b),
            "loc_change": (vb.plan.estimated_loc or 0) - (va.plan.estimated_loc or 0),
        }

    def delete_version(self, version_number: int) -> bool:
        """
        Delete specific version.

        Args:
            version_number: Version to delete

        Returns:
            bool: True if deleted, False if not found

        Note:
            Cannot delete version 1 if other versions exist
        """
        if version_number not in self._versions:
            return False

        # Don't allow deleting v1 if other versions exist
        if version_number == 1 and len(self._versions) > 1:
            raise ValueError("Cannot delete version 1 with other versions present")

        # Delete file
        version_file = self._get_version_file_path(version_number)
        if version_file.exists():
            version_file.unlink()

        # Remove from cache
        del self._versions[version_number]

        return True

    def _get_next_version_number(self) -> int:
        """Get next sequential version number."""
        if not self._versions:
            return 1
        return max(self._versions.keys()) + 1

    def _get_version_file_path(self, version_number: int) -> Path:
        """Get file path for version."""
        return self.task_dir / f"v{version_number}.json"

    def _save_version(self, version: PlanVersion) -> None:
        """Save version to disk."""
        version_file = self._get_version_file_path(version.version_number)

        with open(version_file, "w", encoding="utf-8") as f:
            json.dump(version.to_dict(), f, indent=2)

    def _load_versions(self) -> None:
        """Load all versions from disk."""
        if not self.task_dir.exists():
            return

        for version_file in self.task_dir.glob("v*.json"):
            try:
                with open(version_file, "r", encoding="utf-8") as f:
                    version_data = json.load(f)

                version = PlanVersion.from_dict(version_data)
                self._versions[version.version_number] = version

            except Exception as e:
                print(f"Error loading version {version_file}: {e}")


# Module exports
__all__ = [
    "PlanVersion",
    "VersionManager",
]
