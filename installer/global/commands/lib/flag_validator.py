"""
Flag Validator - Configuration flag conflict detection and validation.

Part of TASK-003E Phase 5 Day 2 implementation.
Detects conflicting command-line flags and provides helpful error messages.
"""

from typing import Dict, List, Optional


class FlagConflictError(ValueError):
    """Raised when conflicting flags are detected."""
    pass


class FlagValidator:
    """
    Validates command-line flags for conflicts and invalid combinations.

    Examples:
        >>> validator = FlagValidator()
        >>> flags = {"skip_review": True, "force_review": True}
        >>> validator.validate(flags)  # Raises FlagConflictError

        >>> flags = {"auto_proceed": True, "force_review": True}
        >>> validator.validate(flags)  # Logs warning, auto_proceed disabled
    """

    # Define conflicting flag pairs
    CONFLICTS = [
        {
            "flags": ["skip_review", "force_review"],
            "error": (
                "Conflicting flags: --skip-review and --force-review "
                "cannot be used together.\n"
                "  --skip-review: Skip all review checkpoints\n"
                "  --force-review: Force review even for low complexity\n"
                "Solution: Choose only one flag based on your need."
            )
        },
        {
            "flags": ["skip_review", "review_plan"],
            "error": (
                "Conflicting flags: --skip-review and --review-plan "
                "cannot be used together.\n"
                "  --skip-review: Skip all reviews\n"
                "  --review-plan: Force plan review\n"
                "Solution: Remove --skip-review if you want to review the plan."
            )
        },
        {
            "flags": ["design_only", "implement_only"],
            "error": (
                "❌ Error: Cannot use both --design-only and --implement-only flags together\n\n"
                "Choose one workflow mode:\n"
                "  --design-only     Execute design phases only (Phases 1-2.8)\n"
                "  --implement-only  Execute implementation phases only (Phases 3-5)\n"
                "  (no flags)        Execute complete workflow (default)\n\n"
                "Example usage:\n"
                "  /task-work TASK-006 --design-only\n"
                "  /task-work TASK-006 --implement-only\n"
                "  /task-work TASK-006"
            )
        }
    ]

    # Define flag overrides (one flag takes precedence)
    OVERRIDES = [
        {
            "dominant": "force_review",
            "overridden": "auto_proceed",
            "warning": (
                "⚠️  Flag override: --force-review takes precedence over --auto-proceed.\n"
                "    Full review checkpoint will be shown regardless of complexity score."
            )
        },
        {
            "dominant": "force_review",
            "overridden": "skip_review",
            "warning": (
                "⚠️  Flag override: --force-review takes precedence over --skip-review.\n"
                "    Review checkpoints will be shown."
            )
        }
    ]

    def validate(self, user_flags: Dict[str, bool]) -> None:
        """
        Validate user flags for conflicts and apply overrides.

        Args:
            user_flags: Dictionary of flag names to boolean values

        Raises:
            FlagConflictError: If conflicting flags are detected

        Side Effects:
            - Modifies user_flags dict to apply overrides
            - Prints warnings for override scenarios

        Example:
            >>> flags = {"force_review": True, "auto_proceed": True}
            >>> FlagValidator().validate(flags)
            ⚠️  Flag override: --force-review takes precedence...
            >>> flags["auto_proceed"]
            False
        """
        # Check for hard conflicts (raise error)
        self._check_conflicts(user_flags)

        # Apply overrides (warn and modify)
        self._apply_overrides(user_flags)

    def _check_conflicts(self, user_flags: Dict[str, bool]) -> None:
        """Check for conflicting flag combinations."""
        for conflict in self.CONFLICTS:
            flag_names = conflict["flags"]

            # Check if all conflicting flags are set to True
            if all(user_flags.get(flag, False) for flag in flag_names):
                raise FlagConflictError(conflict["error"])

    def _apply_overrides(self, user_flags: Dict[str, bool]) -> None:
        """Apply flag overrides and print warnings."""
        for override in self.OVERRIDES:
            dominant = override["dominant"]
            overridden = override["overridden"]

            # Check if both flags are set
            if user_flags.get(dominant) and user_flags.get(overridden):
                print(f"\n{override['warning']}\n")
                # Disable the overridden flag
                user_flags[overridden] = False

    def get_enabled_flags(self, user_flags: Dict[str, bool]) -> List[str]:
        """
        Get list of enabled flag names.

        Args:
            user_flags: Dictionary of flag names to boolean values

        Returns:
            List of flag names where value is True

        Example:
            >>> flags = {"force_review": True, "auto_proceed": False, "dry_run": True}
            >>> FlagValidator().get_enabled_flags(flags)
            ['force_review', 'dry_run']
        """
        return [flag for flag, enabled in user_flags.items() if enabled]

    def validate_and_summarize(self, user_flags: Dict[str, bool]) -> str:
        """
        Validate flags and return a summary string.

        Args:
            user_flags: Dictionary of flag names to boolean values

        Returns:
            Summary string of active flags after validation

        Raises:
            FlagConflictError: If conflicting flags detected

        Example:
            >>> flags = {"force_review": True}
            >>> FlagValidator().validate_and_summarize(flags)
            'Active flags: force_review'
        """
        self.validate(user_flags)
        enabled = self.get_enabled_flags(user_flags)

        if enabled:
            return f"Active flags: {', '.join(enabled)}"
        else:
            return "Active flags: none"


# Convenience function for direct validation
def validate_flags(user_flags: Dict[str, bool]) -> None:
    """
    Validate user flags for conflicts.

    This is a convenience function that creates a FlagValidator
    instance and calls validate().

    Args:
        user_flags: Dictionary of flag names to boolean values

    Raises:
        FlagConflictError: If conflicting flags detected

    Example:
        >>> flags = {"skip_review": True, "force_review": True}
        >>> validate_flags(flags)  # Raises FlagConflictError
    """
    validator = FlagValidator()
    validator.validate(user_flags)


# Module exports
__all__ = [
    "FlagValidator",
    "FlagConflictError",
    "validate_flags"
]
