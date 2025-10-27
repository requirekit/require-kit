"""
Unit tests for checkpoint_display module.

Tests dataclasses, formatting functions, and helper methods.
Does not test actual file I/O or display (that's integration/E2E).

Part of TASK-028: Enhance Phase 2.8 Checkpoint Display with Plan Summary.
"""

import pytest
from pathlib import Path
import sys

# Add lib directory to path for imports
lib_path = Path(__file__).parent.parent.parent / "installer" / "global" / "commands" / "lib"
sys.path.insert(0, str(lib_path))

from checkpoint_display import (
    RiskLevel,
    FileChange,
    Dependency,
    Risk,
    EffortEstimate,
    PlanSummary,
    format_plan_summary,
    _parse_risk_level,
    _get_review_mode
)


# ============================================================================
# Test Dataclasses
# ============================================================================

class TestFileChange:
    """Test FileChange dataclass."""

    def test_file_change_basic(self):
        """Test basic FileChange creation."""
        fc = FileChange(
            path="src/feature.py",
            description="Add new feature",
            change_type="create"
        )
        assert fc.path == "src/feature.py"
        assert fc.description == "Add new feature"
        assert fc.change_type == "create"

    def test_file_change_truncation(self):
        """Test description truncation at 80 chars."""
        long_desc = "A" * 100  # 100 chars
        fc = FileChange(path="test.py", description=long_desc)

        assert len(fc.description) == 80
        assert fc.description.endswith("...")
        assert fc.description == "A" * 77 + "..."

    def test_file_change_no_truncation_short(self):
        """Test no truncation for short descriptions."""
        short_desc = "Short description"
        fc = FileChange(path="test.py", description=short_desc)

        assert fc.description == short_desc

    def test_file_change_exactly_80_chars(self):
        """Test description at exactly 80 chars (no truncation)."""
        desc_80 = "A" * 80
        fc = FileChange(path="test.py", description=desc_80)

        assert fc.description == desc_80


class TestRiskLevel:
    """Test RiskLevel enum."""

    def test_risk_level_values(self):
        """Test enum values."""
        assert RiskLevel.HIGH.value == "high"
        assert RiskLevel.MEDIUM.value == "medium"
        assert RiskLevel.LOW.value == "low"

    def test_risk_level_icons(self):
        """Test severity icons."""
        assert RiskLevel.HIGH.icon == "🔴"
        assert RiskLevel.MEDIUM.icon == "🟡"
        assert RiskLevel.LOW.icon == "🟢"

    def test_from_string_case_insensitive(self):
        """Test case-insensitive parsing."""
        assert RiskLevel.from_string("high") == RiskLevel.HIGH
        assert RiskLevel.from_string("HIGH") == RiskLevel.HIGH
        assert RiskLevel.from_string("High") == RiskLevel.HIGH
        assert RiskLevel.from_string("medium") == RiskLevel.MEDIUM
        assert RiskLevel.from_string("MEDIUM") == RiskLevel.MEDIUM
        assert RiskLevel.from_string("low") == RiskLevel.LOW
        assert RiskLevel.from_string("LOW") == RiskLevel.LOW

    def test_from_string_unknown_defaults_to_medium(self):
        """Test unknown levels default to MEDIUM."""
        assert RiskLevel.from_string("unknown") == RiskLevel.MEDIUM
        assert RiskLevel.from_string("critical") == RiskLevel.MEDIUM
        assert RiskLevel.from_string("") == RiskLevel.MEDIUM


class TestPlanSummary:
    """Test PlanSummary dataclass."""

    def test_plan_summary_empty(self):
        """Test empty plan summary."""
        summary = PlanSummary(task_id="TASK-028")

        assert summary.task_id == "TASK-028"
        assert summary.files_to_change == []
        assert summary.dependencies == []
        assert summary.risks == []
        assert summary.effort is None
        assert summary.test_summary is None
        assert summary.phases == []

    def test_plan_summary_has_high_risks_true(self):
        """Test has_high_risks property when HIGH risks exist."""
        summary = PlanSummary(
            task_id="TASK-028",
            risks=[
                Risk(description="High risk item", level=RiskLevel.HIGH),
                Risk(description="Medium risk item", level=RiskLevel.MEDIUM)
            ]
        )

        assert summary.has_high_risks is True

    def test_plan_summary_has_high_risks_false(self):
        """Test has_high_risks property when no HIGH risks."""
        summary = PlanSummary(
            task_id="TASK-028",
            risks=[
                Risk(description="Medium risk item", level=RiskLevel.MEDIUM),
                Risk(description="Low risk item", level=RiskLevel.LOW)
            ]
        )

        assert summary.has_high_risks is False

    def test_plan_summary_total_files(self):
        """Test total_files property."""
        summary = PlanSummary(
            task_id="TASK-028",
            files_to_change=[
                FileChange(path="file1.py", description="Create"),
                FileChange(path="file2.py", description="Modify"),
                FileChange(path="file3.py", description="Create")
            ]
        )

        assert summary.total_files == 3


# ============================================================================
# Test Helper Functions
# ============================================================================

class TestParseRiskLevel:
    """Test _parse_risk_level function."""

    def test_parse_valid_levels(self):
        """Test parsing valid risk levels."""
        assert _parse_risk_level("high") == RiskLevel.HIGH
        assert _parse_risk_level("medium") == RiskLevel.MEDIUM
        assert _parse_risk_level("low") == RiskLevel.LOW

    def test_parse_case_insensitive(self):
        """Test case insensitivity."""
        assert _parse_risk_level("HIGH") == RiskLevel.HIGH
        assert _parse_risk_level("MeDiUm") == RiskLevel.MEDIUM
        assert _parse_risk_level("LoW") == RiskLevel.LOW

    def test_parse_invalid_defaults_to_medium(self):
        """Test invalid levels default to MEDIUM."""
        assert _parse_risk_level("invalid") == RiskLevel.MEDIUM
        assert _parse_risk_level("") == RiskLevel.MEDIUM


class TestGetReviewMode:
    """Test _get_review_mode function."""

    def test_auto_proceed_complexity_1_3(self):
        """Test AUTO_PROCEED for complexity 1-3."""
        assert _get_review_mode(1) == "AUTO_PROCEED"
        assert _get_review_mode(2) == "AUTO_PROCEED"
        assert _get_review_mode(3) == "AUTO_PROCEED"

    def test_quick_optional_complexity_4_6(self):
        """Test QUICK_OPTIONAL for complexity 4-6."""
        assert _get_review_mode(4) == "QUICK_OPTIONAL"
        assert _get_review_mode(5) == "QUICK_OPTIONAL"
        assert _get_review_mode(6) == "QUICK_OPTIONAL"

    def test_full_required_complexity_7_10(self):
        """Test FULL_REQUIRED for complexity 7-10."""
        assert _get_review_mode(7) == "FULL_REQUIRED"
        assert _get_review_mode(8) == "FULL_REQUIRED"
        assert _get_review_mode(9) == "FULL_REQUIRED"
        assert _get_review_mode(10) == "FULL_REQUIRED"

    def test_boundary_values(self):
        """Test boundary values explicitly."""
        assert _get_review_mode(3) == "AUTO_PROCEED"
        assert _get_review_mode(4) == "QUICK_OPTIONAL"
        assert _get_review_mode(6) == "QUICK_OPTIONAL"
        assert _get_review_mode(7) == "FULL_REQUIRED"


# ============================================================================
# Test format_plan_summary
# ============================================================================

class TestFormatPlanSummary:
    """Test format_plan_summary function."""

    def test_format_empty_summary(self):
        """Test formatting empty summary."""
        summary = PlanSummary(task_id="TASK-028")
        formatted = format_plan_summary(summary)

        assert "IMPLEMENTATION PLAN SUMMARY" in formatted
        assert "TASK-028" not in formatted  # Task ID not shown in summary body

    def test_format_with_files(self):
        """Test formatting with file changes."""
        summary = PlanSummary(
            task_id="TASK-028",
            files_to_change=[
                FileChange(path="src/file1.py", description="Create", change_type="create"),
                FileChange(path="src/file2.py", description="Modify", change_type="modify")
            ]
        )
        formatted = format_plan_summary(summary)

        assert "Files to Change (2)" in formatted
        assert "src/file1.py (create)" in formatted
        assert "src/file2.py (modify)" in formatted

    def test_format_with_file_truncation(self):
        """Test file list truncation."""
        files = [
            FileChange(path=f"file{i}.py", description="Create", change_type="create")
            for i in range(10)
        ]
        summary = PlanSummary(task_id="TASK-028", files_to_change=files)
        formatted = format_plan_summary(summary, max_files=5)

        assert "Files to Change (10)" in formatted
        assert "file0.py (create)" in formatted
        assert "file4.py (create)" in formatted
        assert "... and 5 more" in formatted
        assert "file9.py" not in formatted  # Should be truncated

    def test_format_with_dependencies(self):
        """Test formatting with dependencies."""
        summary = PlanSummary(
            task_id="TASK-028",
            dependencies=[
                Dependency(name="requests", version="2.28.0", purpose="HTTP client"),
                Dependency(name="pytest", version="7.0.0")
            ]
        )
        formatted = format_plan_summary(summary)

        assert "Dependencies (2)" in formatted
        assert "requests (2.28.0)" in formatted
        assert "pytest (7.0.0)" in formatted

    def test_format_with_dependency_truncation(self):
        """Test dependency list truncation."""
        deps = [
            Dependency(name=f"package{i}", version=f"1.{i}.0")
            for i in range(6)
        ]
        summary = PlanSummary(task_id="TASK-028", dependencies=deps)
        formatted = format_plan_summary(summary, max_deps=3)

        assert "Dependencies (6)" in formatted
        assert "package0 (1.0.0)" in formatted
        assert "package2 (1.2.0)" in formatted
        assert "... and 3 more" in formatted
        assert "package5" not in formatted

    def test_format_with_risks(self):
        """Test formatting with risks."""
        summary = PlanSummary(
            task_id="TASK-028",
            risks=[
                Risk(
                    description="High risk of data loss",
                    level=RiskLevel.HIGH,
                    mitigation="Add transaction rollback"
                ),
                Risk(
                    description="Medium complexity",
                    level=RiskLevel.MEDIUM
                )
            ]
        )
        formatted = format_plan_summary(summary)

        assert "Risks (2)" in formatted
        assert "🔴 HIGH: High risk of data loss" in formatted
        assert "Mitigation: Add transaction rollback" in formatted
        assert "🟡 MEDIUM: Medium complexity" in formatted

    def test_format_with_effort(self):
        """Test formatting with effort estimate."""
        summary = PlanSummary(
            task_id="TASK-028",
            effort=EffortEstimate(
                duration="4 hours",
                lines_of_code=250,
                complexity_score=7
            )
        )
        formatted = format_plan_summary(summary)

        assert "Effort Estimate:" in formatted
        assert "Duration: 4 hours" in formatted
        assert "Lines of Code: ~250" in formatted
        assert "Complexity: 7/10" in formatted

    def test_format_with_test_summary(self):
        """Test formatting with test summary."""
        summary = PlanSummary(
            task_id="TASK-028",
            test_summary="Unit tests for all public functions, integration tests for API"
        )
        formatted = format_plan_summary(summary)

        assert "Testing Approach:" in formatted
        assert "Unit tests for all public functions" in formatted

    def test_format_skip_empty_sections(self):
        """Test that empty sections are skipped."""
        summary = PlanSummary(
            task_id="TASK-028",
            files_to_change=[
                FileChange(path="test.py", description="Create", change_type="create")
            ]
            # No dependencies, risks, effort, or test_summary
        )
        formatted = format_plan_summary(summary)

        assert "Files to Change" in formatted
        assert "Dependencies" not in formatted
        assert "Risks" not in formatted
        assert "Effort Estimate" not in formatted
        assert "Testing Approach" not in formatted

    def test_format_all_sections_complete(self):
        """Test complete summary with all sections."""
        summary = PlanSummary(
            task_id="TASK-028",
            files_to_change=[
                FileChange(path="src/checkpoint.py", description="Create", change_type="create")
            ],
            dependencies=[
                Dependency(name="pytest", version="7.0.0")
            ],
            risks=[
                Risk(description="Test risk", level=RiskLevel.LOW)
            ],
            effort=EffortEstimate(
                duration="2 hours",
                lines_of_code=100,
                complexity_score=5
            ),
            test_summary="Comprehensive unit tests"
        )
        formatted = format_plan_summary(summary)

        # Check all sections present
        assert "Files to Change" in formatted
        assert "Dependencies" in formatted
        assert "Risks" in formatted
        assert "Effort Estimate" in formatted
        assert "Testing Approach" in formatted


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
