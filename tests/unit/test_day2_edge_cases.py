"""
Unit tests for TASK-003E Phase 5 Day 2 Edge Cases.

Tests all Day 2 implementations:
- File write failure handling (review_modes.py)
- Configuration flag conflict detection (flag_validator.py)
- Corrupted metrics file skipping (metrics_storage.py)
- User-friendly error message wrappers (error_messages.py)
"""

import errno
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import pytest

# Import modules under test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "installer" / "global" / "commands" / "lib"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "installer" / "global" / "lib" / "metrics"))

from flag_validator import FlagValidator, FlagConflictError, validate_flags
from metrics_storage import MetricsStorage
from error_messages import format_file_error, format_validation_error, format_calculation_error


# ============================================================================
# Test File Write Failure Handling (review_modes.py)
# ============================================================================

class TestFileWriteFailureHandling:
    """Test file write failure handling in review_modes.py."""

    def test_move_to_backlog_handles_write_failure(self, capsys):
        """Test _move_task_to_backlog handles write failures gracefully."""
        # Import FullReviewHandler
        from review_modes import FullReviewHandler
        from complexity_models import ImplementationPlan, ComplexityScore

        # Create temp file
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = Path(tmpdir) / "tasks" / "in_progress"
            task_dir.mkdir(parents=True)
            task_file = task_dir / "TASK-001.md"
            task_file.write_text("---\ntitle: Test\nstatus: in_progress\n---\nContent")

            # Mock plan and score
            plan = Mock(spec=ImplementationPlan)
            plan.raw_plan = "Test plan"
            plan.files_to_create = []
            plan.external_dependencies = []
            plan.phases = []
            plan.estimated_loc = 100
            plan.estimated_duration = "1 hour"
            plan.test_summary = "Test summary"
            plan.risk_details = []
            plan.risk_indicators = []

            score = Mock(spec=ComplexityScore)
            score.total_score = 5
            score.factor_scores = []
            score.forced_review_triggers = []

            metadata = {"id": "TASK-001", "title": "Test Task"}

            # Create handler
            handler = FullReviewHandler(
                complexity_score=score,
                plan=plan,
                task_metadata=metadata,
                task_file_path=task_file
            )

            # Mock FileOperations to raise OSError on atomic_write
            # FileOperations is imported inside the method from user_interaction
            with patch('user_interaction.FileOperations.atomic_write') as mock_write:
                mock_write.side_effect = OSError(errno.EROFS, "Read-only file system")

                # Call _move_task_to_backlog - should not crash
                handler._move_task_to_backlog()

            # Check warning was printed
            captured = capsys.readouterr()
            assert "Warning: Could not move task file to backlog" in captured.out
            assert "Read-only file system" in captured.out

    def test_move_to_backlog_handles_permission_error(self, capsys):
        """Test _move_task_to_backlog handles permission errors gracefully."""
        from review_modes import FullReviewHandler
        from complexity_models import ImplementationPlan, ComplexityScore

        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = Path(tmpdir) / "tasks" / "in_progress"
            task_dir.mkdir(parents=True)
            task_file = task_dir / "TASK-002.md"
            task_file.write_text("---\ntitle: Test\nstatus: in_progress\n---\nContent")

            plan = Mock(spec=ImplementationPlan)
            plan.raw_plan = "Test"
            plan.files_to_create = []
            plan.external_dependencies = []
            plan.phases = []
            plan.estimated_loc = 50
            plan.estimated_duration = "30 min"
            plan.test_summary = None
            plan.risk_details = []
            plan.risk_indicators = []

            score = Mock(spec=ComplexityScore)
            score.total_score = 3
            score.factor_scores = []
            score.forced_review_triggers = []

            metadata = {"id": "TASK-002", "title": "Test Task 2"}

            handler = FullReviewHandler(
                complexity_score=score,
                plan=plan,
                task_metadata=metadata,
                task_file_path=task_file
            )

            # Mock permission error
            with patch('user_interaction.FileOperations.atomic_write') as mock_write:
                mock_write.side_effect = OSError(errno.EACCES, "Permission denied")

                handler._move_task_to_backlog()

            captured = capsys.readouterr()
            assert "Warning: Could not move task file to backlog" in captured.out
            assert "Permission denied" in captured.out

    def test_move_to_backlog_continues_on_error(self):
        """Test _move_task_to_backlog continues execution even on write failure."""
        from review_modes import FullReviewHandler
        from complexity_models import ImplementationPlan, ComplexityScore

        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = Path(tmpdir) / "tasks" / "in_progress"
            task_dir.mkdir(parents=True)
            task_file = task_dir / "TASK-003.md"
            task_file.write_text("---\ntitle: Test\nstatus: in_progress\n---\nContent")

            plan = Mock(spec=ImplementationPlan)
            plan.raw_plan = "Test"
            plan.files_to_create = []
            plan.external_dependencies = []
            plan.phases = []
            plan.estimated_loc = 75
            plan.estimated_duration = "45 min"
            plan.test_summary = "Tests"
            plan.risk_details = []
            plan.risk_indicators = []

            score = Mock(spec=ComplexityScore)
            score.total_score = 4
            score.factor_scores = []
            score.forced_review_triggers = []

            metadata = {"id": "TASK-003", "title": "Test Task 3"}

            handler = FullReviewHandler(
                complexity_score=score,
                plan=plan,
                task_metadata=metadata,
                task_file_path=task_file
            )

            # Mock failure but ensure no exception propagates
            with patch('user_interaction.FileOperations.atomic_write') as mock_write:
                mock_write.side_effect = OSError(errno.ENOSPC, "No space left")

                # Should not raise exception
                try:
                    handler._move_task_to_backlog()
                    success = True
                except Exception:
                    success = False

                assert success, "Method should not raise exception on write failure"


# ============================================================================
# Test Flag Conflict Detection (flag_validator.py)
# ============================================================================

class TestFlagConflictDetection:
    """Test configuration flag conflict detection."""

    def test_flag_conflict_skip_and_force_raises_error(self):
        """Test that skip_review + force_review raises FlagConflictError."""
        flags = {
            "skip_review": True,
            "force_review": True
        }

        validator = FlagValidator()

        with pytest.raises(FlagConflictError) as exc_info:
            validator.validate(flags)

        error_msg = str(exc_info.value)
        assert "skip-review" in error_msg.lower()
        assert "force-review" in error_msg.lower()
        assert "Solution:" in error_msg

    def test_flag_override_force_over_auto_proceeds(self, capsys):
        """Test that force_review overrides auto_proceed with warning."""
        flags = {
            "force_review": True,
            "auto_proceed": True
        }

        validator = FlagValidator()
        validator.validate(flags)

        # Check auto_proceed was disabled
        assert flags["force_review"] is True
        assert flags["auto_proceed"] is False

        # Check warning was printed
        captured = capsys.readouterr()
        assert "⚠️" in captured.out
        assert "force-review takes precedence" in captured.out

    def test_flag_conflict_skip_and_review_plan(self):
        """Test that skip_review + review_plan raises FlagConflictError."""
        flags = {
            "skip_review": True,
            "review_plan": True
        }

        validator = FlagValidator()

        with pytest.raises(FlagConflictError) as exc_info:
            validator.validate(flags)

        error_msg = str(exc_info.value)
        assert "skip-review" in error_msg.lower()
        assert "review-plan" in error_msg.lower()

    def test_enabled_flags_list_correct(self):
        """Test get_enabled_flags returns correct list."""
        flags = {
            "force_review": True,
            "auto_proceed": False,
            "skip_review": False,
            "dry_run": True
        }

        validator = FlagValidator()
        enabled = validator.get_enabled_flags(flags)

        assert len(enabled) == 2
        assert "force_review" in enabled
        assert "dry_run" in enabled
        assert "auto_proceed" not in enabled


# ============================================================================
# Test Corrupted Metrics Handling (metrics_storage.py)
# ============================================================================

class TestCorruptedMetricsHandling:
    """Test corrupted metrics file handling."""

    @pytest.fixture
    def temp_metrics_file(self):
        """Create temporary metrics file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            metrics_file = Path(tmpdir) / "metrics.jsonl"
            yield metrics_file

    def test_skip_corrupted_json_lines(self, temp_metrics_file, capsys):
        """Test that corrupted JSON lines are skipped during read."""
        # Write mixed valid/invalid JSON
        content = (
            '{"type": "valid1", "value": 1}\n'
            '{"invalid": json syntax}\n'  # Corrupted line
            '{"type": "valid2", "value": 2}\n'
            'completely invalid\n'  # Another corrupted line
            '{"type": "valid3", "value": 3}\n'
        )
        temp_metrics_file.write_text(content)

        storage = MetricsStorage(metrics_file=temp_metrics_file)
        metrics = storage.read_all_metrics()

        # Should get only 3 valid metrics
        assert len(metrics) == 3
        assert metrics[0]["type"] == "valid1"
        assert metrics[1]["type"] == "valid2"
        assert metrics[2]["type"] == "valid3"

        # Check warnings were printed
        captured = capsys.readouterr()
        assert "Warning" in captured.out
        assert "Skipping corrupted metric" in captured.out

    def test_corrupted_metrics_line_numbers_logged(self, temp_metrics_file, capsys):
        """Test that corrupted lines include line numbers in warnings."""
        content = (
            '{"type": "valid1", "value": 1}\n'
            '{"bad json\n'  # Line 2 - corrupted
            '{"type": "valid2", "value": 2}\n'
        )
        temp_metrics_file.write_text(content)

        storage = MetricsStorage(metrics_file=temp_metrics_file)
        storage.read_all_metrics()

        captured = capsys.readouterr()
        # Should mention line number
        assert "line 2" in captured.out
        assert "Line content:" in captured.out


# ============================================================================
# Test Error Message Formatters (error_messages.py)
# ============================================================================

class TestErrorMessageFormatters:
    """Test user-friendly error message formatters."""

    def test_format_file_error_errno_30_read_only(self):
        """Test format_file_error for EROFS (read-only filesystem)."""
        error = OSError(errno.EROFS, "Read-only file system")
        msg = format_file_error(error, "write task to backlog")

        assert "❌" in msg
        assert "write task to backlog" in msg
        assert "Read-only file system" in msg
        assert "errno 30" in msg
        assert "Solution:" in msg
        assert "remount" in msg.lower()

    def test_format_file_error_errno_28_no_space(self):
        """Test format_file_error for ENOSPC (no space left)."""
        error = OSError(errno.ENOSPC, "No space left on device")
        msg = format_file_error(error, "save metrics")

        assert "❌" in msg
        assert "save metrics" in msg
        assert "No space left" in msg
        assert "errno 28" in msg
        assert "Solution:" in msg
        assert "disk space" in msg.lower()

    def test_format_file_error_errno_13_permission(self):
        """Test format_file_error for EACCES (permission denied)."""
        error = OSError(errno.EACCES, "Permission denied")
        msg = format_file_error(error, "create directory")

        assert "❌" in msg
        assert "create directory" in msg
        assert "Permission denied" in msg
        assert "errno 13" in msg
        assert "Solution:" in msg
        assert "permissions" in msg.lower()

    def test_format_file_error_errno_2_not_found(self):
        """Test format_file_error for ENOENT (file not found)."""
        error = OSError(errno.ENOENT, "No such file or directory")
        msg = format_file_error(error, "read config file")

        assert "❌" in msg
        assert "read config file" in msg
        assert "No such file" in msg
        assert "errno 2" in msg
        assert "Solution:" in msg
        assert "path exists" in msg.lower()

    def test_format_validation_error_includes_solution(self):
        """Test format_validation_error includes actionable solution."""
        error = ValueError("must be positive integer")
        msg = format_validation_error(error, "complexity_score")

        assert "❌" in msg
        assert "complexity_score" in msg
        assert "must be positive integer" in msg
        assert "Solution:" in msg
        assert "valid value" in msg

    def test_format_validation_error_multiple_fields(self):
        """Test format_validation_error works for different fields."""
        error1 = ValueError("required field missing")
        msg1 = format_validation_error(error1, "task_id")

        error2 = ValueError("invalid format")
        msg2 = format_validation_error(error2, "timestamp")

        # Check both messages are properly formatted
        assert "task_id" in msg1
        assert "timestamp" in msg2
        assert "Solution:" in msg1
        assert "Solution:" in msg2

    def test_format_calculation_error_includes_task_context(self):
        """Test format_calculation_error includes task context."""
        error = ZeroDivisionError("division by zero")
        msg = format_calculation_error(error, "TASK-001")

        assert "❌" in msg
        assert "TASK-001" in msg
        assert "division by zero" in msg
        assert "ZeroDivisionError" in msg
        assert "Solution:" in msg
        assert "calculation inputs" in msg

    def test_format_calculation_error_key_error(self):
        """Test format_calculation_error handles KeyError."""
        error = KeyError("missing_metric")
        msg = format_calculation_error(error, "TASK-002")

        assert "❌" in msg
        assert "TASK-002" in msg
        assert "missing_metric" in msg
        assert "KeyError" in msg
        assert "Solution:" in msg
        assert "required metrics" in msg


# ============================================================================
# Integration Tests
# ============================================================================

class TestDay2EdgeCasesIntegration:
    """Integration tests for Day 2 edge case implementations."""

    def test_flag_validator_validate_and_summarize(self):
        """Test validate_and_summarize convenience method."""
        flags = {
            "force_review": True,
            "auto_proceed": False
        }

        validator = FlagValidator()
        summary = validator.validate_and_summarize(flags)

        assert "force_review" in summary
        assert summary.startswith("Active flags:")

    def test_convenience_validate_flags_function(self):
        """Test module-level validate_flags convenience function."""
        flags = {
            "skip_review": True,
            "force_review": True
        }

        with pytest.raises(FlagConflictError):
            validate_flags(flags)

    def test_metrics_storage_with_error_formatter(self, capsys):
        """Test MetricsStorage error handling integrates with error formatters."""
        # Create storage with invalid path
        invalid_path = Path("/invalid/path/metrics.jsonl")
        storage = MetricsStorage(metrics_file=invalid_path)

        metric = {"type": "test", "value": 42}
        result = storage.append_metric(metric)

        # Should fail gracefully
        assert result is False

        # Should print warning
        captured = capsys.readouterr()
        assert "Warning" in captured.out or "Failed" in captured.out
