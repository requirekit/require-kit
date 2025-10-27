"""
Apply modifications to implementation plans.

This module applies recorded changes from a modification session back to
an ImplementationPlan, creating a new version with updated fields.

Architecture:
    - ModificationApplier: Applies changes to create modified plan

Example:
    >>> from modification_applier import ModificationApplier
    >>> from change_tracker import ChangeTracker
    >>>
    >>> applier = ModificationApplier(original_plan, change_tracker)
    >>> modified_plan = applier.apply()
"""

import copy
from typing import List

try:
    from .change_tracker import Change, ChangeTracker, ChangeType
    from .complexity_models import ImplementationPlan
except ImportError:
    from change_tracker import Change, ChangeTracker, ChangeType
    from complexity_models import ImplementationPlan


class ModificationApplier:
    """
    Applies changes to implementation plans.

    Takes an original plan and a change tracker, applies all recorded
    changes, and produces a new modified plan instance.

    Example:
        >>> applier = ModificationApplier(original_plan, tracker)
        >>> modified_plan = applier.apply()
        >>> print(f"Files changed: {len(modified_plan.files_to_create)}")
    """

    def __init__(
        self,
        original_plan: ImplementationPlan,
        change_tracker: ChangeTracker
    ):
        """
        Initialize modification applier.

        Args:
            original_plan: Original implementation plan
            change_tracker: Tracker with recorded changes
        """
        self.original_plan = original_plan
        self.change_tracker = change_tracker

    def apply(self) -> ImplementationPlan:
        """
        Apply all changes to create modified plan.

        Creates a deep copy of the original plan and applies changes
        in chronological order. Returns new plan instance.

        Returns:
            ImplementationPlan: New plan with changes applied

        Example:
            >>> modified_plan = applier.apply()
            >>> assert modified_plan is not applier.original_plan
        """
        # Start with deep copy of original plan
        modified_plan = self._copy_plan(self.original_plan)

        # Apply changes in chronological order
        for change in self.change_tracker.changes:
            modified_plan = self._apply_change(modified_plan, change)

        return modified_plan

    def _copy_plan(self, plan: ImplementationPlan) -> ImplementationPlan:
        """
        Create deep copy of implementation plan.

        Args:
            plan: Plan to copy

        Returns:
            ImplementationPlan: New plan instance
        """
        # Deep copy all list fields to avoid shared references
        return ImplementationPlan(
            task_id=plan.task_id,
            files_to_create=list(plan.files_to_create),
            patterns_used=list(plan.patterns_used),
            external_dependencies=list(plan.external_dependencies),
            estimated_loc=plan.estimated_loc,
            risk_indicators=list(plan.risk_indicators),
            raw_plan=plan.raw_plan,
            test_summary=plan.test_summary,
            risk_details=copy.deepcopy(plan.risk_details) if plan.risk_details else None,
            phases=list(plan.phases) if plan.phases else None,
            implementation_instructions=plan.implementation_instructions,
            estimated_duration=plan.estimated_duration,
            complexity_score=plan.complexity_score,
        )

    def _apply_change(
        self,
        plan: ImplementationPlan,
        change: Change
    ) -> ImplementationPlan:
        """
        Apply single change to plan.

        Args:
            plan: Plan to modify
            change: Change to apply

        Returns:
            ImplementationPlan: Plan with change applied
        """
        if change.change_type == ChangeType.FILE_ADDED:
            return self._apply_file_added(plan, change)
        elif change.change_type == ChangeType.FILE_REMOVED:
            return self._apply_file_removed(plan, change)
        elif change.change_type == ChangeType.FILE_MODIFIED:
            return self._apply_file_modified(plan, change)
        elif change.change_type == ChangeType.DEPENDENCY_ADDED:
            return self._apply_dependency_added(plan, change)
        elif change.change_type == ChangeType.DEPENDENCY_REMOVED:
            return self._apply_dependency_removed(plan, change)
        elif change.change_type == ChangeType.PHASE_ADDED:
            return self._apply_phase_added(plan, change)
        elif change.change_type == ChangeType.PHASE_REMOVED:
            return self._apply_phase_removed(plan, change)
        elif change.change_type == ChangeType.METADATA_UPDATED:
            return self._apply_metadata_updated(plan, change)
        else:
            # Unknown change type - skip silently
            return plan

    def _apply_file_added(
        self,
        plan: ImplementationPlan,
        change: Change
    ) -> ImplementationPlan:
        """Apply file addition change."""
        file_path = change.target

        # Add file if not already present
        if file_path not in plan.files_to_create:
            plan.files_to_create.append(file_path)

        return plan

    def _apply_file_removed(
        self,
        plan: ImplementationPlan,
        change: Change
    ) -> ImplementationPlan:
        """Apply file removal change."""
        file_path = change.target

        # Remove file if present
        if file_path in plan.files_to_create:
            plan.files_to_create.remove(file_path)

        return plan

    def _apply_file_modified(
        self,
        plan: ImplementationPlan,
        change: Change
    ) -> ImplementationPlan:
        """Apply file modification change."""
        # File modifications don't change the files list,
        # only the purpose/description which is tracked in raw_plan
        # For now, this is a no-op on the structured plan
        return plan

    def _apply_dependency_added(
        self,
        plan: ImplementationPlan,
        change: Change
    ) -> ImplementationPlan:
        """Apply dependency addition change."""
        dependency = change.target

        # Add dependency if not already present
        if dependency not in plan.external_dependencies:
            plan.external_dependencies.append(dependency)

        return plan

    def _apply_dependency_removed(
        self,
        plan: ImplementationPlan,
        change: Change
    ) -> ImplementationPlan:
        """Apply dependency removal change."""
        dependency = change.target

        # Remove dependency if present
        if dependency in plan.external_dependencies:
            plan.external_dependencies.remove(dependency)

        return plan

    def _apply_phase_added(
        self,
        plan: ImplementationPlan,
        change: Change
    ) -> ImplementationPlan:
        """Apply phase addition change."""
        phase_description = change.target
        position = change.metadata.get("position", -1)

        # Initialize phases list if needed
        if plan.phases is None:
            plan.phases = []

        # Insert phase at position (or append if position invalid)
        if 0 <= position <= len(plan.phases):
            plan.phases.insert(position, phase_description)
        else:
            plan.phases.append(phase_description)

        return plan

    def _apply_phase_removed(
        self,
        plan: ImplementationPlan,
        change: Change
    ) -> ImplementationPlan:
        """Apply phase removal change."""
        phase_description = change.target

        # Remove phase if present
        if plan.phases and phase_description in plan.phases:
            plan.phases.remove(phase_description)

        return plan

    def _apply_metadata_updated(
        self,
        plan: ImplementationPlan,
        change: Change
    ) -> ImplementationPlan:
        """Apply metadata update change."""
        field_name = change.target
        new_value = change.new_value

        # Update specific metadata fields
        if field_name == "estimated_loc" and isinstance(new_value, int):
            plan.estimated_loc = new_value
        elif field_name == "estimated_duration" and isinstance(new_value, str):
            plan.estimated_duration = new_value
        elif field_name == "test_summary" and isinstance(new_value, str):
            plan.test_summary = new_value
        elif field_name == "raw_plan" and isinstance(new_value, str):
            plan.raw_plan = new_value
        elif field_name == "implementation_instructions" and isinstance(new_value, str):
            plan.implementation_instructions = new_value

        return plan

    def get_change_summary(self) -> str:
        """
        Generate summary of changes to be applied.

        Returns:
            str: Human-readable summary
        """
        if self.change_tracker.is_empty:
            return "No changes to apply"

        return self.change_tracker.get_summary()

    def validate_changes(self) -> List[str]:
        """
        Validate that changes can be applied safely.

        Returns:
            List[str]: List of validation errors (empty if valid)

        Example:
            >>> errors = applier.validate_changes()
            >>> if errors:
            ...     print("Cannot apply changes:")
            ...     for error in errors:
            ...         print(f"  - {error}")
        """
        errors = []

        # Check for conflicting file operations
        files_added = set()
        files_removed = set()

        for change in self.change_tracker.changes:
            if change.change_type == ChangeType.FILE_ADDED:
                file_path = change.target
                if file_path in files_removed:
                    errors.append(
                        f"Conflicting operations on file: {file_path} "
                        "(both added and removed)"
                    )
                files_added.add(file_path)

            elif change.change_type == ChangeType.FILE_REMOVED:
                file_path = change.target
                if file_path in files_added:
                    errors.append(
                        f"Conflicting operations on file: {file_path} "
                        "(both added and removed)"
                    )
                files_removed.add(file_path)

        # Check that removed files exist in original plan
        for file_path in files_removed:
            if file_path not in self.original_plan.files_to_create:
                errors.append(
                    f"Cannot remove file not in plan: {file_path}"
                )

        # Check that removed dependencies exist in original plan
        for change in self.change_tracker.get_changes_by_type(
            ChangeType.DEPENDENCY_REMOVED
        ):
            dep = change.target
            if dep not in self.original_plan.external_dependencies:
                errors.append(
                    f"Cannot remove dependency not in plan: {dep}"
                )

        return errors


# Module exports
__all__ = [
    "ModificationApplier",
]
