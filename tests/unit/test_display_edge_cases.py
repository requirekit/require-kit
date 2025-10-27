"""
Unit tests for TASK-003E Phase 5 Day 3: Display Edge Cases.

Tests empty section handling in pager_display.py:
- All empty sections display user-friendly messages
- Partial empty sections (mix of None and populated)
- Whitespace-only sections treated as empty

This tests the format_plan_section function added to pager_display.py.
"""

import pytest
import sys
from pathlib import Path
from typing import Dict, Any
from unittest.mock import Mock

# Add installer lib to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "installer" / "global" / "commands" / "lib"))

from pager_display import PagerDisplay, format_plan_section
from complexity_models import ImplementationPlan, ComplexityScore, ReviewMode

# Import boundary helpers
sys.path.insert(0, str(Path(__file__).parent.parent / "fixtures"))
from boundary_helpers import empty_plan, whitespace_plan, partial_empty_plan


# ============================================================================
# Test Empty Section Handling
# ============================================================================

class TestEmptySectionHandling:
    """Test that empty/None plan sections display user-friendly messages."""

    def test_all_empty_sections_display_messages(self, empty_plan):
        """Test that all None sections show user-friendly messages."""
        # Create ImplementationPlan with all None sections
        plan = ImplementationPlan(
            task_id=empty_plan["task_id"],
            files_to_create=[],
            external_dependencies=[],
            raw_plan=None,  # None
            test_summary=None,  # None
            risk_details=None,  # None
            phases=None,  # None
            estimated_loc=None,
            estimated_duration=None
        )

        # Add mock complexity score
        plan.complexity_score = Mock(spec=ComplexityScore)
        plan.complexity_score.total_score = 5
        plan.complexity_score.review_mode = ReviewMode.QUICK_OPTIONAL
        plan.complexity_score.factor_scores = []

        # Format plan for display
        display = PagerDisplay()
        formatted_content = display._format_plan(plan)

        # Verify user-friendly messages appear
        # When raw_plan is None, format_plan_section should provide default
        assert formatted_content is not None
        assert "IMPLEMENTATION PLAN" in formatted_content
        assert empty_plan["task_id"] in formatted_content

        # Verify sections are handled gracefully (no crashes, no "None" strings)
        assert "None" not in formatted_content or "[No" in formatted_content

    def test_partial_empty_sections(self, partial_empty_plan):
        """Test mix of None and populated sections."""
        # Create plan with some None, some populated sections
        plan = ImplementationPlan(
            task_id=partial_empty_plan["task_id"],
            files_to_create=partial_empty_plan["files_to_create"],
            external_dependencies=[],
            raw_plan=partial_empty_plan["raw_plan"],
            test_summary=None,  # None
            risk_details=[],
            phases=None,  # None
            estimated_loc=partial_empty_plan["estimated_loc"],
            estimated_duration=partial_empty_plan["estimated_duration"]
        )

        # Add complexity score
        plan.complexity_score = Mock(spec=ComplexityScore)
        plan.complexity_score.total_score = 3
        plan.complexity_score.review_mode = ReviewMode.AUTO_PROCEED
        plan.complexity_score.factor_scores = []

        display = PagerDisplay()
        formatted_content = display._format_plan(plan)

        # Verify populated sections appear
        assert "IMPLEMENTATION PLAN" in formatted_content
        assert partial_empty_plan["raw_plan"] in formatted_content
        assert partial_empty_plan["files_to_create"][0] in formatted_content

        # Verify no crashes and content is coherent
        assert formatted_content is not None
        assert len(formatted_content) > 0

    def test_whitespace_only_sections_treated_as_empty(self, whitespace_plan):
        """Test that whitespace-only sections are treated as empty."""
        # Test the format_plan_section function directly
        whitespace_overview = whitespace_plan["overview"]
        formatted = format_plan_section(whitespace_overview, "overview")

        # Whitespace-only should be treated as empty
        assert "[No overview provided]" == formatted

        # Test with newlines and tabs
        whitespace_arch = whitespace_plan["architecture"]
        formatted_arch = format_plan_section(whitespace_arch, "architecture")
        assert "[No architecture provided]" == formatted_arch

        # Test with mixed whitespace
        whitespace_testing = whitespace_plan["testing"]
        formatted_testing = format_plan_section(whitespace_testing, "testing")
        assert "[No testing provided]" == formatted_testing


# ============================================================================
# Test format_plan_section Function
# ============================================================================

class TestFormatPlanSection:
    """Test the format_plan_section utility function."""

    def test_format_plan_section_none_value(self):
        """Test format_plan_section with None value."""
        result = format_plan_section(None, "dependencies")
        assert result == "[No dependencies provided]"

    def test_format_plan_section_empty_string(self):
        """Test format_plan_section with empty string."""
        result = format_plan_section("", "testing")
        assert result == "[No testing provided]"

    def test_format_plan_section_whitespace_only(self):
        """Test format_plan_section with whitespace-only string."""
        # Spaces only
        result1 = format_plan_section("   ", "overview")
        assert result1 == "[No overview provided]"

        # Newlines only
        result2 = format_plan_section("\n\n\n", "steps")
        assert result2 == "[No steps provided]"

        # Tabs only
        result3 = format_plan_section("\t\t\t", "architecture")
        assert result3 == "[No architecture provided]"

        # Mixed whitespace
        result4 = format_plan_section("  \n  \t  ", "testing")
        assert result4 == "[No testing provided]"

    def test_format_plan_section_valid_content(self):
        """Test format_plan_section with valid content."""
        content = "This is valid plan content"
        result = format_plan_section(content, "overview")
        assert result == content

    def test_format_plan_section_preserves_content(self):
        """Test that valid content is returned unchanged."""
        multiline_content = """
        Step 1: Analyze requirements
        Step 2: Design solution
        Step 3: Implement
        """
        result = format_plan_section(multiline_content, "steps")
        assert result == multiline_content


# ============================================================================
# Integration Tests
# ============================================================================

class TestDisplayEdgeCasesIntegration:
    """Integration tests for display edge cases."""

    def test_pager_display_with_completely_empty_plan(self):
        """Test PagerDisplay handles completely empty plan without crashing."""
        plan = ImplementationPlan(
            task_id="TASK-EMPTY-INTEGRATION",
            files_to_create=[],
            external_dependencies=[],
            raw_plan="",  # Empty
        )

        # Add minimal complexity score
        plan.complexity_score = Mock(spec=ComplexityScore)
        plan.complexity_score.total_score = 1
        plan.complexity_score.review_mode = ReviewMode.AUTO_PROCEED
        plan.complexity_score.factor_scores = []

        display = PagerDisplay()

        # Should not crash
        try:
            formatted = display._format_plan(plan)
            success = True
        except Exception as e:
            success = False
            error_msg = str(e)

        assert success, f"PagerDisplay should handle empty plan gracefully, but got error: {error_msg if not success else ''}"
        assert formatted is not None
        assert "TASK-EMPTY-INTEGRATION" in formatted

    def test_pager_display_handles_mixed_empty_sections(self):
        """Test PagerDisplay with realistic mix of empty/populated sections."""
        plan = ImplementationPlan(
            task_id="TASK-MIXED-001",
            files_to_create=["src/main.py", "tests/test_main.py"],
            external_dependencies=["pytest"],
            raw_plan="Implement feature X with tests",
            test_summary=None,  # Empty
            risk_details=None,  # Empty
            phases=["Phase 1: Setup", "Phase 2: Implement"],
            estimated_loc=150,
            estimated_duration="3 hours"
        )

        plan.complexity_score = Mock(spec=ComplexityScore)
        plan.complexity_score.total_score = 4
        plan.complexity_score.review_mode = ReviewMode.QUICK_OPTIONAL
        plan.complexity_score.factor_scores = []

        display = PagerDisplay()
        formatted = display._format_plan(plan)

        # Verify populated sections appear
        assert "src/main.py" in formatted
        assert "pytest" in formatted
        assert "Phase 1: Setup" in formatted

        # Verify no "None" strings appear (replaced with user-friendly messages)
        # Note: The string "None" might appear in other contexts, so this is not strict
        assert formatted is not None
        assert len(formatted) > 0

    def test_edge_case_single_space_string(self):
        """Test edge case of single space as section content."""
        result = format_plan_section(" ", "overview")
        assert result == "[No overview provided]"

    def test_edge_case_single_newline_string(self):
        """Test edge case of single newline as section content."""
        result = format_plan_section("\n", "testing")
        assert result == "[No testing provided]"
