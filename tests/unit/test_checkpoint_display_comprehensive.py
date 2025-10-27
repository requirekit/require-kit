"""
Comprehensive unit tests for checkpoint_display module (TASK-028).

This suite provides extensive coverage including:
- All dataclasses (FileChange, Dependency, Risk, EffortEstimate, PlanSummary)
- All formatting functions (format_plan_summary, display_phase28_checkpoint)
- Plan loading functionality (load_plan_summary)
- Edge cases and error handling

Target Coverage:
- Line coverage: ≥80%
- Branch coverage: ≥75%
"""

import pytest
from pathlib import Path
import sys
import tempfile
import json
from unittest.mock import patch, MagicMock

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
    load_plan_summary,
    format_plan_summary,
    display_phase28_checkpoint,
    _parse_risk_level,
    _get_review_mode,
    _load_from_path,
    PlanPersistenceError
)


# ============================================================================
# Test Dataclasses - Comprehensive Coverage
# ============================================================================

class TestFileChangeComprehensive:
    """Comprehensive tests for FileChange dataclass."""

    def test_file_change_default_change_type(self):
        """Test default change_type is 'create'."""
        fc = FileChange(path="src/feature.py", description="Add new feature")
        assert fc.change_type == "create"

    def test_file_change_modify_type(self):
        """Test change_type can be 'modify'."""
        fc = FileChange(
            path="src/existing.py",
            description="Update existing feature",
            change_type="modify"
        )
        assert fc.change_type == "modify"

    def test_file_change_truncation_boundary_79_chars(self):
        """Test truncation boundary at 79 chars (should truncate)."""
        desc_79 = "A" * 79
        fc = FileChange(path="test.py", description=desc_79)
        assert fc.description == desc_79  # No truncation at 79

    def test_file_change_truncation_boundary_81_chars(self):
        """Test truncation boundary at 81 chars (should truncate)."""
        desc_81 = "A" * 81
        fc = FileChange(path="test.py", description=desc_81)
        assert len(fc.description) == 80
        assert fc.description.endswith("...")

    def test_file_change_empty_description(self):
        """Test FileChange with empty description."""
        fc = FileChange(path="test.py", description="")
        assert fc.description == ""

    def test_file_change_special_characters_in_path(self):
        """Test FileChange with special characters in path."""
        fc = FileChange(
            path="src/models/user_model.py",
            description="Add user model"
        )
        assert fc.path == "src/models/user_model.py"


class TestDependencyComprehensive:
    """Comprehensive tests for Dependency dataclass."""

    def test_dependency_only_name(self):
        """Test Dependency with only name."""
        dep = Dependency(name="requests")
        assert dep.name == "requests"
        assert dep.version is None
        assert dep.purpose is None

    def test_dependency_with_version(self):
        """Test Dependency with name and version."""
        dep = Dependency(name="pytest", version="7.0.0")
        assert dep.name == "pytest"
        assert dep.version == "7.0.0"
        assert dep.purpose is None

    def test_dependency_with_all_fields(self):
        """Test Dependency with all fields."""
        dep = Dependency(
            name="fastapi",
            version="0.95.0",
            purpose="API framework"
        )
        assert dep.name == "fastapi"
        assert dep.version == "0.95.0"
        assert dep.purpose == "API framework"

    def test_dependency_empty_name(self):
        """Test Dependency with empty name."""
        dep = Dependency(name="")
        assert dep.name == ""


class TestRiskComprehensive:
    """Comprehensive tests for Risk dataclass."""

    def test_risk_without_mitigation(self):
        """Test Risk without mitigation."""
        risk = Risk(description="Data loss risk", level=RiskLevel.HIGH)
        assert risk.description == "Data loss risk"
        assert risk.level == RiskLevel.HIGH
        assert risk.mitigation is None

    def test_risk_with_mitigation(self):
        """Test Risk with mitigation."""
        risk = Risk(
            description="API timeout",
            level=RiskLevel.MEDIUM,
            mitigation="Add retry logic"
        )
        assert risk.description == "API timeout"
        assert risk.level == RiskLevel.MEDIUM
        assert risk.mitigation == "Add retry logic"

    def test_risk_all_severity_levels(self):
        """Test Risk with all severity levels."""
        high_risk = Risk(description="Critical", level=RiskLevel.HIGH)
        medium_risk = Risk(description="Moderate", level=RiskLevel.MEDIUM)
        low_risk = Risk(description="Minor", level=RiskLevel.LOW)

        assert high_risk.level == RiskLevel.HIGH
        assert medium_risk.level == RiskLevel.MEDIUM
        assert low_risk.level == RiskLevel.LOW


class TestEffortEstimateComprehensive:
    """Comprehensive tests for EffortEstimate dataclass."""

    def test_effort_estimate_basic(self):
        """Test basic EffortEstimate."""
        effort = EffortEstimate(
            duration="4 hours",
            lines_of_code=250,
            complexity_score=7
        )
        assert effort.duration == "4 hours"
        assert effort.lines_of_code == 250
        assert effort.complexity_score == 7

    def test_effort_estimate_zero_lines(self):
        """Test EffortEstimate with zero lines of code."""
        effort = EffortEstimate(
            duration="1 hour",
            lines_of_code=0,
            complexity_score=1
        )
        assert effort.lines_of_code == 0

    def test_effort_estimate_max_complexity(self):
        """Test EffortEstimate with max complexity."""
        effort = EffortEstimate(
            duration="2 days",
            lines_of_code=1000,
            complexity_score=10
        )
        assert effort.complexity_score == 10

    def test_effort_estimate_min_complexity(self):
        """Test EffortEstimate with min complexity."""
        effort = EffortEstimate(
            duration="30 minutes",
            lines_of_code=50,
            complexity_score=1
        )
        assert effort.complexity_score == 1


class TestPlanSummaryComprehensive:
    """Comprehensive tests for PlanSummary dataclass."""

    def test_plan_summary_has_high_risks_empty(self):
        """Test has_high_risks with empty risks list."""
        summary = PlanSummary(task_id="TASK-028", risks=[])
        assert summary.has_high_risks is False

    def test_plan_summary_has_high_risks_only_low(self):
        """Test has_high_risks with only low risks."""
        summary = PlanSummary(
            task_id="TASK-028",
            risks=[
                Risk(description="Minor issue", level=RiskLevel.LOW),
                Risk(description="Another minor issue", level=RiskLevel.LOW)
            ]
        )
        assert summary.has_high_risks is False

    def test_plan_summary_has_high_risks_multiple_high(self):
        """Test has_high_risks with multiple high risks."""
        summary = PlanSummary(
            task_id="TASK-028",
            risks=[
                Risk(description="Critical issue 1", level=RiskLevel.HIGH),
                Risk(description="Critical issue 2", level=RiskLevel.HIGH)
            ]
        )
        assert summary.has_high_risks is True

    def test_plan_summary_total_files_zero(self):
        """Test total_files with no files."""
        summary = PlanSummary(task_id="TASK-028")
        assert summary.total_files == 0

    def test_plan_summary_total_files_many(self):
        """Test total_files with many files."""
        files = [
            FileChange(path=f"file{i}.py", description=f"File {i}")
            for i in range(20)
        ]
        summary = PlanSummary(task_id="TASK-028", files_to_change=files)
        assert summary.total_files == 20

    def test_plan_summary_with_phases(self):
        """Test PlanSummary with implementation phases."""
        summary = PlanSummary(
            task_id="TASK-028",
            phases=[
                "Phase 1: Setup",
                "Phase 2: Implementation",
                "Phase 3: Testing"
            ]
        )
        assert len(summary.phases) == 3
        assert summary.phases[0] == "Phase 1: Setup"


# ============================================================================
# Test Helper Functions - Comprehensive Coverage
# ============================================================================

class TestParseRiskLevelComprehensive:
    """Comprehensive tests for _parse_risk_level function."""

    def test_parse_with_whitespace(self):
        """Test parsing with leading/trailing whitespace."""
        assert _parse_risk_level("  high  ") == RiskLevel.HIGH
        assert _parse_risk_level("\tmedium\n") == RiskLevel.MEDIUM

    def test_parse_mixed_case(self):
        """Test parsing with mixed case."""
        assert _parse_risk_level("HiGh") == RiskLevel.HIGH
        assert _parse_risk_level("MeDiUm") == RiskLevel.MEDIUM
        assert _parse_risk_level("LoW") == RiskLevel.LOW

    def test_parse_numeric_string(self):
        """Test parsing numeric string defaults to MEDIUM."""
        assert _parse_risk_level("123") == RiskLevel.MEDIUM


class TestGetReviewModeComprehensive:
    """Comprehensive tests for _get_review_mode function."""

    def test_all_complexity_scores(self):
        """Test all complexity scores from 1 to 10."""
        expected = {
            1: "AUTO_PROCEED",
            2: "AUTO_PROCEED",
            3: "AUTO_PROCEED",
            4: "QUICK_OPTIONAL",
            5: "QUICK_OPTIONAL",
            6: "QUICK_OPTIONAL",
            7: "FULL_REQUIRED",
            8: "FULL_REQUIRED",
            9: "FULL_REQUIRED",
            10: "FULL_REQUIRED"
        }
        for score, expected_mode in expected.items():
            assert _get_review_mode(score) == expected_mode

    def test_edge_case_zero_complexity(self):
        """Test edge case with zero complexity."""
        # Zero should map to AUTO_PROCEED (<=3)
        assert _get_review_mode(0) == "AUTO_PROCEED"

    def test_edge_case_negative_complexity(self):
        """Test edge case with negative complexity."""
        # Negative should map to AUTO_PROCEED (<=3)
        assert _get_review_mode(-1) == "AUTO_PROCEED"

    def test_edge_case_high_complexity(self):
        """Test edge case with very high complexity."""
        assert _get_review_mode(100) == "FULL_REQUIRED"


# ============================================================================
# Test format_plan_summary - Comprehensive Coverage
# ============================================================================

class TestFormatPlanSummaryComprehensive:
    """Comprehensive tests for format_plan_summary function."""

    def test_format_with_no_version_dependencies(self):
        """Test formatting dependencies without versions."""
        summary = PlanSummary(
            task_id="TASK-028",
            dependencies=[
                Dependency(name="requests"),
                Dependency(name="pytest")
            ]
        )
        formatted = format_plan_summary(summary)
        assert "requests" in formatted
        assert "pytest" in formatted
        # Should not have version indicators
        assert "requests ()" not in formatted

    def test_format_with_risk_no_mitigation(self):
        """Test formatting risk without mitigation."""
        summary = PlanSummary(
            task_id="TASK-028",
            risks=[
                Risk(description="No mitigation risk", level=RiskLevel.HIGH)
            ]
        )
        formatted = format_plan_summary(summary)
        assert "🔴 HIGH: No mitigation risk" in formatted
        assert "Mitigation:" not in formatted

    def test_format_custom_max_files(self):
        """Test custom max_files parameter."""
        files = [FileChange(path=f"f{i}.py", description="Test") for i in range(20)]
        summary = PlanSummary(task_id="TASK-028", files_to_change=files)

        # Test with different max_files values
        formatted_2 = format_plan_summary(summary, max_files=2)
        assert "... and 18 more" in formatted_2

        formatted_10 = format_plan_summary(summary, max_files=10)
        assert "... and 10 more" in formatted_10

    def test_format_custom_max_deps(self):
        """Test custom max_deps parameter."""
        deps = [Dependency(name=f"pkg{i}") for i in range(15)]
        summary = PlanSummary(task_id="TASK-028", dependencies=deps)

        formatted_5 = format_plan_summary(summary, max_deps=5)
        assert "... and 10 more" in formatted_5

    def test_format_exact_max_files_no_truncation(self):
        """Test no truncation when files equal max_files."""
        files = [FileChange(path=f"f{i}.py", description="Test") for i in range(5)]
        summary = PlanSummary(task_id="TASK-028", files_to_change=files)

        formatted = format_plan_summary(summary, max_files=5)
        assert "... and" not in formatted

    def test_format_exact_max_deps_no_truncation(self):
        """Test no truncation when deps equal max_deps."""
        deps = [Dependency(name=f"pkg{i}") for i in range(3)]
        summary = PlanSummary(task_id="TASK-028", dependencies=deps)

        formatted = format_plan_summary(summary, max_deps=3)
        assert "... and" not in formatted

    def test_format_section_ordering(self):
        """Test that sections appear in correct order."""
        summary = PlanSummary(
            task_id="TASK-028",
            files_to_change=[FileChange(path="f.py", description="Test")],
            dependencies=[Dependency(name="pkg")],
            risks=[Risk(description="Risk", level=RiskLevel.LOW)],
            effort=EffortEstimate("1 hour", 100, 3),
            test_summary="Test plan"
        )
        formatted = format_plan_summary(summary)

        # Check order
        files_idx = formatted.find("Files to Change")
        deps_idx = formatted.find("Dependencies")
        risks_idx = formatted.find("Risks")
        effort_idx = formatted.find("Effort Estimate")
        test_idx = formatted.find("Testing Approach")

        assert files_idx < deps_idx < risks_idx < effort_idx < test_idx

    def test_format_multiline_test_summary(self):
        """Test formatting with multiline test summary."""
        summary = PlanSummary(
            task_id="TASK-028",
            test_summary="Line 1: Unit tests\nLine 2: Integration tests\nLine 3: E2E tests"
        )
        formatted = format_plan_summary(summary)
        assert "Testing Approach:" in formatted
        assert "Line 1" in formatted


# ============================================================================
# Test load_plan_summary - Comprehensive Coverage
# ============================================================================

class TestLoadPlanSummaryComprehensive:
    """Comprehensive tests for load_plan_summary function."""

    def test_load_plan_summary_no_plan_exists(self):
        """Test loading when no plan exists."""
        with patch('checkpoint_display.plan_exists', return_value=False):
            summary = load_plan_summary("TASK-NONEXISTENT")
            assert summary is None

    def test_load_plan_summary_empty_plan_section(self):
        """Test loading plan with empty 'plan' section."""
        with patch('checkpoint_display.plan_exists', return_value=True):
            with patch('checkpoint_display.load_plan', return_value={"plan": {}}):
                summary = load_plan_summary("TASK-028")
                assert summary is None

    def test_load_plan_summary_no_plan_key(self):
        """Test loading plan without 'plan' key."""
        with patch('checkpoint_display.plan_exists', return_value=True):
            with patch('checkpoint_display.load_plan', return_value={"other": "data"}):
                summary = load_plan_summary("TASK-028")
                assert summary is None

    def test_load_plan_summary_with_files_to_create(self):
        """Test loading plan with files_to_create."""
        plan_data = {
            "plan": {
                "files_to_create": ["src/file1.py", "src/file2.py"],
                "files_to_modify": []
            }
        }
        with patch('checkpoint_display.plan_exists', return_value=True):
            with patch('checkpoint_display.load_plan', return_value=plan_data):
                summary = load_plan_summary("TASK-028")
                assert summary is not None
                assert len(summary.files_to_change) == 2
                assert all(fc.change_type == "create" for fc in summary.files_to_change)

    def test_load_plan_summary_with_files_to_modify(self):
        """Test loading plan with files_to_modify."""
        plan_data = {
            "plan": {
                "files_to_create": [],
                "files_to_modify": ["src/existing1.py", "src/existing2.py"]
            }
        }
        with patch('checkpoint_display.plan_exists', return_value=True):
            with patch('checkpoint_display.load_plan', return_value=plan_data):
                summary = load_plan_summary("TASK-028")
                assert summary is not None
                assert len(summary.files_to_change) == 2
                assert all(fc.change_type == "modify" for fc in summary.files_to_change)

    def test_load_plan_summary_with_mixed_files(self):
        """Test loading plan with both create and modify files."""
        plan_data = {
            "plan": {
                "files_to_create": ["new.py"],
                "files_to_modify": ["existing.py"]
            }
        }
        with patch('checkpoint_display.plan_exists', return_value=True):
            with patch('checkpoint_display.load_plan', return_value=plan_data):
                summary = load_plan_summary("TASK-028")
                assert summary is not None
                assert len(summary.files_to_change) == 2
                assert summary.files_to_change[0].change_type == "create"
                assert summary.files_to_change[1].change_type == "modify"

    def test_load_plan_summary_with_string_dependencies(self):
        """Test loading plan with string dependencies."""
        plan_data = {
            "plan": {
                "external_dependencies": ["requests", "pytest", "fastapi"]
            }
        }
        with patch('checkpoint_display.plan_exists', return_value=True):
            with patch('checkpoint_display.load_plan', return_value=plan_data):
                summary = load_plan_summary("TASK-028")
                assert summary is not None
                assert len(summary.dependencies) == 3
                assert summary.dependencies[0].name == "requests"

    def test_load_plan_summary_with_dict_dependencies(self):
        """Test loading plan with dict dependencies."""
        plan_data = {
            "plan": {
                "external_dependencies": [
                    {"name": "requests", "version": "2.28.0", "purpose": "HTTP client"},
                    {"name": "pytest", "version": "7.0.0"}
                ]
            }
        }
        with patch('checkpoint_display.plan_exists', return_value=True):
            with patch('checkpoint_display.load_plan', return_value=plan_data):
                summary = load_plan_summary("TASK-028")
                assert summary is not None
                assert len(summary.dependencies) == 2
                assert summary.dependencies[0].version == "2.28.0"
                assert summary.dependencies[0].purpose == "HTTP client"
                assert summary.dependencies[1].version == "7.0.0"

    def test_load_plan_summary_with_string_risks(self):
        """Test loading plan with string risks (defaults to MEDIUM)."""
        plan_data = {
            "plan": {
                "risks": ["Risk 1", "Risk 2"]
            }
        }
        with patch('checkpoint_display.plan_exists', return_value=True):
            with patch('checkpoint_display.load_plan', return_value=plan_data):
                summary = load_plan_summary("TASK-028")
                assert summary is not None
                assert len(summary.risks) == 2
                assert all(r.level == RiskLevel.MEDIUM for r in summary.risks)

    def test_load_plan_summary_with_dict_risks(self):
        """Test loading plan with dict risks."""
        plan_data = {
            "plan": {
                "risks": [
                    {"description": "High risk", "level": "high", "mitigation": "Fix it"},
                    {"description": "Low risk", "level": "low"}
                ]
            }
        }
        with patch('checkpoint_display.plan_exists', return_value=True):
            with patch('checkpoint_display.load_plan', return_value=plan_data):
                summary = load_plan_summary("TASK-028")
                assert summary is not None
                assert len(summary.risks) == 2
                assert summary.risks[0].level == RiskLevel.HIGH
                assert summary.risks[0].mitigation == "Fix it"
                assert summary.risks[1].level == RiskLevel.LOW

    def test_load_plan_summary_with_effort_partial(self):
        """Test loading plan with partial effort data."""
        plan_data = {
            "plan": {
                "estimated_duration": "4 hours"
            }
        }
        with patch('checkpoint_display.plan_exists', return_value=True):
            with patch('checkpoint_display.load_plan', return_value=plan_data):
                summary = load_plan_summary("TASK-028")
                assert summary is not None
                assert summary.effort is not None
                assert summary.effort.duration == "4 hours"
                assert summary.effort.lines_of_code == 0

    def test_load_plan_summary_with_effort_complete(self):
        """Test loading plan with complete effort data."""
        plan_data = {
            "plan": {
                "estimated_duration": "2 days",
                "estimated_loc": 500,
                "complexity_score": 8
            }
        }
        with patch('checkpoint_display.plan_exists', return_value=True):
            with patch('checkpoint_display.load_plan', return_value=plan_data):
                summary = load_plan_summary("TASK-028")
                assert summary is not None
                assert summary.effort.duration == "2 days"
                assert summary.effort.lines_of_code == 500
                assert summary.effort.complexity_score == 8

    def test_load_plan_summary_with_test_summary(self):
        """Test loading plan with test summary."""
        plan_data = {
            "plan": {
                "test_summary": "Comprehensive unit and integration tests"
            }
        }
        with patch('checkpoint_display.plan_exists', return_value=True):
            with patch('checkpoint_display.load_plan', return_value=plan_data):
                summary = load_plan_summary("TASK-028")
                assert summary is not None
                assert summary.test_summary == "Comprehensive unit and integration tests"

    def test_load_plan_summary_with_phases(self):
        """Test loading plan with implementation phases."""
        plan_data = {
            "plan": {
                "phases": ["Phase 1: Setup", "Phase 2: Implementation"]
            }
        }
        with patch('checkpoint_display.plan_exists', return_value=True):
            with patch('checkpoint_display.load_plan', return_value=plan_data):
                summary = load_plan_summary("TASK-028")
                assert summary is not None
                assert len(summary.phases) == 2
                assert summary.phases[0] == "Phase 1: Setup"

    def test_load_plan_summary_persistence_error(self):
        """Test handling of PlanPersistenceError."""
        with patch('checkpoint_display.plan_exists', return_value=True):
            with patch('checkpoint_display.load_plan', side_effect=PlanPersistenceError("Error")):
                with pytest.raises(PlanPersistenceError):
                    load_plan_summary("TASK-028")

    def test_load_plan_summary_unexpected_error(self):
        """Test handling of unexpected errors - should re-raise for proper handling."""
        with patch('checkpoint_display.plan_exists', return_value=True):
            with patch('checkpoint_display.load_plan', side_effect=Exception("Unexpected")):
                with pytest.raises(Exception, match="Unexpected"):
                    load_plan_summary("TASK-028")


# ============================================================================
# Test display_phase28_checkpoint - Comprehensive Coverage
# ============================================================================

class TestDisplayPhase28CheckpointComprehensive:
    """Comprehensive tests for display_phase28_checkpoint function."""

    def test_display_with_low_complexity(self, capsys):
        """Test display with low complexity (AUTO_PROCEED)."""
        plan_data = {
            "plan": {
                "files_to_create": ["test.py"],
                "estimated_duration": "1 hour"
            }
        }
        with patch('checkpoint_display.plan_exists', return_value=True):
            with patch('checkpoint_display.load_plan', return_value=plan_data):
                display_phase28_checkpoint("TASK-028", 2)

        captured = capsys.readouterr()
        assert "PHASE 2.8: IMPLEMENTATION PLAN CHECKPOINT" in captured.out
        assert "TASK-028" in captured.out
        assert "2/10 (Simple - auto-proceed)" in captured.out

    def test_display_with_medium_complexity(self, capsys):
        """Test display with medium complexity (QUICK_OPTIONAL)."""
        plan_data = {"plan": {"files_to_create": ["test.py"]}}
        with patch('checkpoint_display.plan_exists', return_value=True):
            with patch('checkpoint_display.load_plan', return_value=plan_data):
                display_phase28_checkpoint("TASK-028", 5)

        captured = capsys.readouterr()
        assert "5/10 (Medium - quick review)" in captured.out

    def test_display_with_high_complexity(self, capsys):
        """Test display with high complexity (FULL_REQUIRED)."""
        plan_data = {"plan": {"files_to_create": ["test.py"]}}
        with patch('checkpoint_display.plan_exists', return_value=True):
            with patch('checkpoint_display.load_plan', return_value=plan_data):
                display_phase28_checkpoint("TASK-028", 8)

        captured = capsys.readouterr()
        assert "8/10 (Complex - requires full review)" in captured.out

    def test_display_with_no_plan(self, capsys):
        """Test display when no plan exists."""
        with patch('checkpoint_display.plan_exists', return_value=False):
            display_phase28_checkpoint("TASK-028", 5)

        captured = capsys.readouterr()
        assert "⚠️  No implementation plan found" in captured.out

    def test_display_with_no_plan_high_complexity(self, capsys):
        """Test display when no plan exists with high complexity."""
        with patch('checkpoint_display.plan_exists', return_value=False):
            display_phase28_checkpoint("TASK-028", 9)

        captured = capsys.readouterr()
        assert "⚠️  No implementation plan found" in captured.out
        assert "WARNING: Complex task without saved plan" in captured.out

    def test_display_with_complete_plan(self, capsys):
        """Test display with complete plan data."""
        plan_data = {
            "plan": {
                "files_to_create": ["src/feature.py"],
                "files_to_modify": ["src/existing.py"],
                "external_dependencies": [{"name": "pytest", "version": "7.0.0"}],
                "risks": [{"description": "Test risk", "level": "medium"}],
                "estimated_duration": "4 hours",
                "estimated_loc": 200,
                "complexity_score": 6,
                "test_summary": "Unit tests required"
            }
        }
        with patch('checkpoint_display.plan_exists', return_value=True):
            with patch('checkpoint_display.load_plan', return_value=plan_data):
                display_phase28_checkpoint("TASK-028", 6)

        captured = capsys.readouterr()
        assert "Files to Change" in captured.out
        assert "Dependencies" in captured.out
        assert "Risks" in captured.out
        assert "Effort Estimate" in captured.out
        assert "Testing Approach" in captured.out

    def test_display_shows_checkpoint_options(self, capsys):
        """Test that checkpoint options are displayed."""
        with patch('checkpoint_display.plan_exists', return_value=False):
            display_phase28_checkpoint("TASK-028", 5)

        captured = capsys.readouterr()
        assert "[A]pprove  - Proceed with implementation" in captured.out
        assert "[M]odify   - Adjust plan and regenerate" in captured.out
        assert "[C]ancel   - Stop task execution" in captured.out

    def test_display_with_plan_path(self, capsys):
        """Test display with explicit plan_path."""
        plan_path = Path("/tmp/test_plan.md")
        plan_data = {"plan": {"files_to_create": ["test.py"]}}

        with patch('checkpoint_display._load_from_path', return_value=plan_data):
            display_phase28_checkpoint("TASK-028", 5, plan_path=plan_path)

        captured = capsys.readouterr()
        assert "Plan file: /tmp/test_plan.md" in captured.out

    def test_display_persistence_error(self, capsys):
        """Test display handling PlanPersistenceError."""
        with patch('checkpoint_display.plan_exists', return_value=True):
            with patch('checkpoint_display.load_plan', side_effect=PlanPersistenceError("Load error")):
                display_phase28_checkpoint("TASK-028", 5)

        captured = capsys.readouterr()
        assert "⚠️  Error loading implementation plan" in captured.out

    def test_display_unexpected_error(self, capsys):
        """Test display handling unexpected errors."""
        with patch('checkpoint_display.plan_exists', return_value=True):
            with patch('checkpoint_display.load_plan', side_effect=Exception("Unexpected")):
                display_phase28_checkpoint("TASK-028", 5)

        captured = capsys.readouterr()
        assert "⚠️  Unexpected error" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
