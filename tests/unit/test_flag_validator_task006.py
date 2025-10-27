"""
Unit tests for flag_validator.py - TASK-006 extensions (design_only/implement_only flags).

Tests cover:
    - design_only and implement_only mutual exclusivity
    - Flag conflict detection for new flags
    - Error message quality for design-first workflow
    - Integration with existing flag validation

Part of TASK-006: Add Design-First Workflow Flags to task-work Command
"""

import pytest
from pathlib import Path
import sys

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "installer/global/commands/lib"))

from flag_validator import (
    FlagValidator,
    FlagConflictError,
    validate_flags,
)


class TestDesignOnlyImplementOnlyMutualExclusivity:
    """Test suite for design_only and implement_only mutual exclusivity."""

    def test_both_flags_raises_conflict_error(self):
        """Test that using both --design-only and --implement-only raises FlagConflictError."""
        validator = FlagValidator()
        flags = {
            "design_only": True,
            "implement_only": True
        }

        with pytest.raises(FlagConflictError) as exc_info:
            validator.validate(flags)

        assert "Cannot use both" in str(exc_info.value)
        assert "--design-only" in str(exc_info.value)
        assert "--implement-only" in str(exc_info.value)

    def test_design_only_alone_is_valid(self):
        """Test that --design-only alone is valid."""
        validator = FlagValidator()
        flags = {"design_only": True}

        # Should not raise
        validator.validate(flags)

    def test_implement_only_alone_is_valid(self):
        """Test that --implement-only alone is valid."""
        validator = FlagValidator()
        flags = {"implement_only": True}

        # Should not raise
        validator.validate(flags)

    def test_neither_flag_is_valid(self):
        """Test that having neither flag is valid."""
        validator = FlagValidator()
        flags = {}

        # Should not raise
        validator.validate(flags)

    def test_design_only_false_implement_only_false(self):
        """Test that both flags set to False is valid."""
        validator = FlagValidator()
        flags = {
            "design_only": False,
            "implement_only": False
        }

        # Should not raise
        validator.validate(flags)

    def test_design_only_true_implement_only_false(self):
        """Test that design_only=True, implement_only=False is valid."""
        validator = FlagValidator()
        flags = {
            "design_only": True,
            "implement_only": False
        }

        # Should not raise
        validator.validate(flags)

    def test_design_only_false_implement_only_true(self):
        """Test that design_only=False, implement_only=True is valid."""
        validator = FlagValidator()
        flags = {
            "design_only": False,
            "implement_only": True
        }

        # Should not raise
        validator.validate(flags)


class TestFlagConflictErrorMessage:
    """Test suite for error message quality for design-first workflow flags."""

    def test_error_message_provides_workflow_guidance(self):
        """Test that error message explains the three workflow modes."""
        validator = FlagValidator()
        flags = {
            "design_only": True,
            "implement_only": True
        }

        with pytest.raises(FlagConflictError) as exc_info:
            validator.validate(flags)

        error_msg = str(exc_info.value)
        # Should explain all three modes
        assert "design-only" in error_msg.lower()
        assert "implement-only" in error_msg.lower()
        assert "no flags" in error_msg.lower() or "default" in error_msg.lower()

    def test_error_message_includes_phase_information(self):
        """Test that error message includes phase information."""
        validator = FlagValidator()
        flags = {
            "design_only": True,
            "implement_only": True
        }

        with pytest.raises(FlagConflictError) as exc_info:
            validator.validate(flags)

        error_msg = str(exc_info.value)
        # Should mention phases or workflow stages
        assert "Phases" in error_msg or "design" in error_msg.lower()

    def test_error_message_provides_examples(self):
        """Test that error message provides usage examples."""
        validator = FlagValidator()
        flags = {
            "design_only": True,
            "implement_only": True
        }

        with pytest.raises(FlagConflictError) as exc_info:
            validator.validate(flags)

        error_msg = str(exc_info.value)
        # Should include example commands
        assert "/task-work" in error_msg or "TASK-" in error_msg or "Example" in error_msg


class TestDesignFirstWorkflowWithOtherFlags:
    """Test suite for design-first workflow flags combined with other flags."""

    def test_design_only_with_skip_review_is_valid(self):
        """Test that --design-only with --skip-review is valid."""
        validator = FlagValidator()
        flags = {
            "design_only": True,
            "skip_review": True
        }

        # Should not raise conflict (though may not make logical sense)
        validator.validate(flags)

    def test_design_only_with_force_review_is_valid(self):
        """Test that --design-only with --force-review is valid."""
        validator = FlagValidator()
        flags = {
            "design_only": True,
            "force_review": True
        }

        # Should not raise conflict
        validator.validate(flags)

    def test_implement_only_with_auto_proceed_is_valid(self):
        """Test that --implement-only with --auto-proceed is valid."""
        validator = FlagValidator()
        flags = {
            "implement_only": True,
            "auto_proceed": True
        }

        # Should not raise conflict
        validator.validate(flags)

    def test_design_only_with_multiple_flags(self):
        """Test --design-only with multiple other flags."""
        validator = FlagValidator()
        flags = {
            "design_only": True,
            "force_review": True,
            "review_plan": True
        }

        # Should not raise conflict for design_only combinations
        validator.validate(flags)


class TestGetEnabledFlagsWithDesignFirst:
    """Test suite for get_enabled_flags with design-first workflow flags."""

    def test_get_enabled_flags_includes_design_only(self):
        """Test that get_enabled_flags includes design_only when True."""
        validator = FlagValidator()
        flags = {"design_only": True, "other_flag": False}

        enabled = validator.get_enabled_flags(flags)

        assert "design_only" in enabled
        assert "other_flag" not in enabled

    def test_get_enabled_flags_includes_implement_only(self):
        """Test that get_enabled_flags includes implement_only when True."""
        validator = FlagValidator()
        flags = {"implement_only": True}

        enabled = validator.get_enabled_flags(flags)

        assert "implement_only" in enabled

    def test_get_enabled_flags_excludes_false_flags(self):
        """Test that get_enabled_flags excludes False flags."""
        validator = FlagValidator()
        flags = {
            "design_only": False,
            "implement_only": False,
            "force_review": True
        }

        enabled = validator.get_enabled_flags(flags)

        assert "design_only" not in enabled
        assert "implement_only" not in enabled
        assert "force_review" in enabled


class TestValidateAndSummarizeWithDesignFirst:
    """Test suite for validate_and_summarize with design-first workflow flags."""

    def test_validate_and_summarize_design_only(self):
        """Test validate_and_summarize with design_only flag."""
        validator = FlagValidator()
        flags = {"design_only": True}

        summary = validator.validate_and_summarize(flags)

        assert "design_only" in summary

    def test_validate_and_summarize_implement_only(self):
        """Test validate_and_summarize with implement_only flag."""
        validator = FlagValidator()
        flags = {"implement_only": True}

        summary = validator.validate_and_summarize(flags)

        assert "implement_only" in summary

    def test_validate_and_summarize_conflict_raises_error(self):
        """Test that validate_and_summarize raises error for conflicts."""
        validator = FlagValidator()
        flags = {
            "design_only": True,
            "implement_only": True
        }

        with pytest.raises(FlagConflictError):
            validator.validate_and_summarize(flags)

    def test_validate_and_summarize_no_flags(self):
        """Test validate_and_summarize with no flags enabled."""
        validator = FlagValidator()
        flags = {}

        summary = validator.validate_and_summarize(flags)

        assert "none" in summary.lower()


class TestConvenienceFunctionWithDesignFirst:
    """Test suite for convenience validate_flags function with design-first flags."""

    def test_validate_flags_convenience_function_accepts_design_only(self):
        """Test that convenience function works with design_only."""
        flags = {"design_only": True}

        # Should not raise
        validate_flags(flags)

    def test_validate_flags_convenience_function_accepts_implement_only(self):
        """Test that convenience function works with implement_only."""
        flags = {"implement_only": True}

        # Should not raise
        validate_flags(flags)

    def test_validate_flags_convenience_function_raises_on_conflict(self):
        """Test that convenience function raises error on conflict."""
        flags = {
            "design_only": True,
            "implement_only": True
        }

        with pytest.raises(FlagConflictError):
            validate_flags(flags)


class TestBackwardCompatibility:
    """Test suite for backward compatibility with existing flag validation."""

    def test_existing_skip_review_force_review_conflict_still_works(self):
        """Test that existing skip_review/force_review conflict still works."""
        validator = FlagValidator()
        flags = {
            "skip_review": True,
            "force_review": True
        }

        with pytest.raises(FlagConflictError):
            validator.validate(flags)

    def test_existing_skip_review_review_plan_conflict_still_works(self):
        """Test that existing skip_review/review_plan conflict still works."""
        validator = FlagValidator()
        flags = {
            "skip_review": True,
            "review_plan": True
        }

        with pytest.raises(FlagConflictError):
            validator.validate(flags)

    def test_existing_force_review_auto_proceed_override_still_works(self):
        """Test that existing force_review/auto_proceed override still works."""
        validator = FlagValidator()
        flags = {
            "force_review": True,
            "auto_proceed": True
        }

        # Should apply override, not raise error
        validator.validate(flags)

        # auto_proceed should be disabled
        assert flags["auto_proceed"] is False

    def test_design_first_flags_do_not_interfere_with_existing_validation(self):
        """Test that new flags don't interfere with existing validation."""
        validator = FlagValidator()

        # Test all existing conflict scenarios still work with design flags present
        test_cases = [
            # Existing conflicts should still be detected
            {"skip_review": True, "force_review": True, "design_only": False},
            {"skip_review": True, "review_plan": True, "implement_only": False},
        ]

        for flags in test_cases:
            with pytest.raises(FlagConflictError):
                validator.validate(flags)


class TestFlagValidatorConflictsConfiguration:
    """Test suite for CONFLICTS configuration includes design-first flags."""

    def test_conflicts_list_includes_design_implement_conflict(self):
        """Test that CONFLICTS list includes design_only/implement_only conflict."""
        validator = FlagValidator()

        # Check that conflict is defined
        conflict_found = False
        for conflict in validator.CONFLICTS:
            flag_names = conflict["flags"]
            if "design_only" in flag_names and "implement_only" in flag_names:
                conflict_found = True
                break

        assert conflict_found, "design_only/implement_only conflict not found in CONFLICTS"

    def test_design_implement_conflict_has_error_message(self):
        """Test that design/implement conflict has an error message."""
        validator = FlagValidator()

        for conflict in validator.CONFLICTS:
            flag_names = conflict["flags"]
            if "design_only" in flag_names and "implement_only" in flag_names:
                assert "error" in conflict
                assert len(conflict["error"]) > 0
                break


class TestEdgeCases:
    """Test suite for edge cases with design-first workflow flags."""

    def test_design_only_with_empty_other_flags(self):
        """Test design_only with no other flags in dict."""
        validator = FlagValidator()
        flags = {"design_only": True}

        validator.validate(flags)
        enabled = validator.get_enabled_flags(flags)

        assert enabled == ["design_only"]

    def test_implement_only_with_empty_other_flags(self):
        """Test implement_only with no other flags in dict."""
        validator = FlagValidator()
        flags = {"implement_only": True}

        validator.validate(flags)
        enabled = validator.get_enabled_flags(flags)

        assert enabled == ["implement_only"]

    def test_all_flags_false_is_valid(self):
        """Test that all flags set to False is valid."""
        validator = FlagValidator()
        flags = {
            "design_only": False,
            "implement_only": False,
            "skip_review": False,
            "force_review": False,
            "auto_proceed": False
        }

        validator.validate(flags)
        enabled = validator.get_enabled_flags(flags)

        assert len(enabled) == 0

    def test_design_only_string_value_not_boolean(self):
        """Test behavior with non-boolean values (edge case)."""
        validator = FlagValidator()
        flags = {
            "design_only": "true",  # String instead of boolean
            "implement_only": False
        }

        # get() should treat non-False as truthy
        # This tests the actual behavior of the validator
        enabled = validator.get_enabled_flags(flags)

        # String "true" should be truthy
        assert "design_only" in enabled
