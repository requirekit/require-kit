"""
Unit tests for pager_display.py - Cross-platform pager display.

Tests cover:
    - Platform detection and strategy selection
    - Pager command availability checking
    - Content formatting and display
    - Fallback strategies
    - Error handling
"""

import pytest
import platform
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, mock_open
from datetime import datetime

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "installer/global/commands"))

from lib.complexity_models import ImplementationPlan, ComplexityScore, ReviewMode, FactorScore
from lib.pager_display import (
    PagerStrategy,
    UnixPagerStrategy,
    WindowsPagerStrategy,
    FallbackPagerStrategy,
    PagerDisplay,
)


# Test Fixtures
@pytest.fixture
def mock_implementation_plan():
    """Create mock ImplementationPlan for testing."""
    complexity_score = ComplexityScore(
        total_score=6,
        factor_scores=[
            FactorScore(
                factor_name="File Complexity",
                score=2.0,
                max_score=3.0,
                justification="4 files to create"
            )
        ],
        forced_review_triggers=[],
        review_mode=ReviewMode.QUICK_OPTIONAL,
        calculation_timestamp=datetime.now().astimezone(),
        metadata={}
    )

    return ImplementationPlan(
        task_id="TASK-001",
        files_to_create=[
            "src/module1.py",
            "src/module2.py",
            "tests/test_module1.py"
        ],
        patterns_used=["Strategy", "Factory"],
        external_dependencies=["requests", "pytest"],
        estimated_loc=250,
        risk_indicators=["database"],
        raw_plan="Implement data access layer with repository pattern",
        test_summary="Unit tests for repository, integration tests for DB",
        risk_details=[
            {
                "severity": "medium",
                "description": "Database connection handling",
                "mitigation": "Use connection pooling"
            }
        ],
        phases=[
            "Phase 1: Repository interface (~30 min)",
            "Phase 2: Implementation (~45 min)",
            "Phase 3: Testing (~30 min)"
        ],
        implementation_instructions="Implement repository pattern with connection pooling",
        estimated_duration="2 hours",
        complexity_score=complexity_score
    )


class TestUnixPagerStrategy:
    """Test suite for UnixPagerStrategy class."""

    @patch('lib.pager_display.UnixPagerStrategy._command_exists')
    def test_select_pager_prefers_env_variable(self, mock_command_exists):
        """Test that PAGER environment variable takes priority."""
        mock_command_exists.return_value = True

        with patch.dict('os.environ', {'PAGER': 'custom_pager'}):
            strategy = UnixPagerStrategy()
            assert strategy.pager_cmd == 'custom_pager'

    @patch('lib.pager_display.UnixPagerStrategy._command_exists')
    def test_select_pager_falls_back_to_less(self, mock_command_exists):
        """Test fallback to 'less' when no PAGER env var."""
        def command_exists_side_effect(cmd):
            return cmd == 'less'

        mock_command_exists.side_effect = command_exists_side_effect

        with patch.dict('os.environ', {}, clear=True):
            strategy = UnixPagerStrategy()
            assert strategy.pager_cmd == 'less'

    @patch('lib.pager_display.UnixPagerStrategy._command_exists')
    def test_select_pager_falls_back_to_more(self, mock_command_exists):
        """Test fallback to 'more' when 'less' unavailable."""
        def command_exists_side_effect(cmd):
            return cmd == 'more'

        mock_command_exists.side_effect = command_exists_side_effect

        with patch.dict('os.environ', {}, clear=True):
            strategy = UnixPagerStrategy()
            assert strategy.pager_cmd == 'more'

    @patch('lib.pager_display.UnixPagerStrategy._command_exists')
    def test_select_pager_no_pager_available(self, mock_command_exists):
        """Test when no pager is available."""
        mock_command_exists.return_value = False

        with patch.dict('os.environ', {}, clear=True):
            strategy = UnixPagerStrategy()
            assert strategy.pager_cmd == ''

    @patch('subprocess.run')
    def test_command_exists_returns_true_for_existing_command(self, mock_run):
        """Test _command_exists returns True for existing command."""
        mock_run.return_value = Mock(returncode=0)

        strategy = UnixPagerStrategy()
        result = strategy._command_exists('less')

        assert result is True
        # Note: mock_run is called during __init__ (pager selection) and then again in test
        assert mock_run.call_count >= 1

    @patch('subprocess.run')
    def test_command_exists_returns_false_for_nonexistent_command(self, mock_run):
        """Test _command_exists returns False for nonexistent command."""
        mock_run.return_value = Mock(returncode=1)

        strategy = UnixPagerStrategy()
        result = strategy._command_exists('nonexistent_cmd')

        assert result is False

    @patch('subprocess.run')
    def test_command_exists_handles_exceptions(self, mock_run):
        """Test _command_exists handles subprocess exceptions."""
        mock_run.side_effect = subprocess.TimeoutExpired('which', 2)

        strategy = UnixPagerStrategy()
        result = strategy._command_exists('test_cmd')

        assert result is False

    @patch('lib.pager_display.UnixPagerStrategy._command_exists')
    @patch('subprocess.run')
    @patch('tempfile.NamedTemporaryFile')
    @patch('pathlib.Path.unlink')
    def test_display_success_with_less(
        self,
        mock_unlink,
        mock_temp_file,
        mock_subprocess_run,
        mock_command_exists
    ):
        """Test successful display with 'less' pager."""
        mock_command_exists.return_value = True

        # Mock temporary file
        mock_file = Mock()
        mock_file.name = '/tmp/test_file.txt'
        mock_temp_file.return_value.__enter__.return_value = mock_file

        # Mock subprocess success
        mock_subprocess_run.return_value = Mock(returncode=0)

        with patch.dict('os.environ', {}, clear=True):
            strategy = UnixPagerStrategy()
            result = strategy.display("Test content", "Test Title")

        assert result is True
        mock_file.write.assert_called_once_with("Test content")
        mock_subprocess_run.assert_called_once()

    @patch('lib.pager_display.UnixPagerStrategy._command_exists')
    def test_display_fails_when_no_pager_available(self, mock_command_exists):
        """Test display fails gracefully when no pager available."""
        mock_command_exists.return_value = False

        strategy = UnixPagerStrategy()
        result = strategy.display("Test content")

        assert result is False

    @patch('lib.pager_display.UnixPagerStrategy._command_exists')
    @patch('subprocess.run')
    def test_display_handles_subprocess_error(
        self,
        mock_subprocess_run,
        mock_command_exists
    ):
        """Test display handles subprocess errors gracefully."""
        mock_command_exists.return_value = True
        mock_subprocess_run.side_effect = Exception("Subprocess error")

        strategy = UnixPagerStrategy()
        result = strategy.display("Test content")

        assert result is False

    @patch('lib.pager_display.UnixPagerStrategy._command_exists')
    def test_build_command_for_less(self, mock_command_exists):
        """Test command building for 'less' pager."""
        mock_command_exists.return_value = True

        with patch.dict('os.environ', {}, clear=True):
            strategy = UnixPagerStrategy()
            cmd = strategy._build_command("Test Title")

        assert cmd[0] == 'less'
        assert '-R' in cmd  # ANSI colors
        assert '-F' in cmd  # Quit if one screen
        assert '-X' in cmd  # Don't clear screen
        assert any('Test Title' in arg for arg in cmd)

    @patch('lib.pager_display.UnixPagerStrategy._command_exists')
    def test_build_command_for_more(self, mock_command_exists):
        """Test command building for 'more' pager."""
        def command_exists_side_effect(cmd):
            return cmd == 'more'

        mock_command_exists.side_effect = command_exists_side_effect

        with patch.dict('os.environ', {}, clear=True):
            strategy = UnixPagerStrategy()
            cmd = strategy._build_command()

        assert cmd == ['more']

    @patch('lib.pager_display.UnixPagerStrategy._command_exists')
    def test_is_available_returns_true_when_pager_exists(self, mock_command_exists):
        """Test is_available returns True when pager exists."""
        mock_command_exists.return_value = True

        with patch.dict('os.environ', {}, clear=True):
            strategy = UnixPagerStrategy()
            assert strategy.is_available() is True

    @patch('lib.pager_display.UnixPagerStrategy._command_exists')
    def test_is_available_returns_false_when_no_pager(self, mock_command_exists):
        """Test is_available returns False when no pager exists."""
        mock_command_exists.return_value = False

        with patch.dict('os.environ', {}, clear=True):
            strategy = UnixPagerStrategy()
            assert strategy.is_available() is False


class TestWindowsPagerStrategy:
    """Test suite for WindowsPagerStrategy class."""

    @patch('subprocess.run')
    @patch('tempfile.NamedTemporaryFile')
    @patch('pathlib.Path.unlink')
    def test_display_success(
        self,
        mock_unlink,
        mock_temp_file,
        mock_subprocess_run
    ):
        """Test successful display on Windows."""
        # Mock temporary file
        mock_file = Mock()
        mock_file.name = 'C:\\temp\\test_file.txt'
        mock_temp_file.return_value.__enter__.return_value = mock_file

        # Mock subprocess success
        mock_subprocess_run.return_value = Mock(returncode=0)

        strategy = WindowsPagerStrategy()
        result = strategy.display("Test content", "Test Title")

        assert result is True
        mock_file.write.assert_called_once_with("Test content")

    @patch('subprocess.run')
    def test_display_handles_error(self, mock_subprocess_run):
        """Test display handles errors on Windows."""
        mock_subprocess_run.side_effect = Exception("Windows error")

        strategy = WindowsPagerStrategy()
        result = strategy.display("Test content")

        assert result is False

    @patch('platform.system')
    def test_is_available_on_windows(self, mock_platform):
        """Test is_available returns True on Windows."""
        mock_platform.return_value = 'Windows'

        strategy = WindowsPagerStrategy()
        assert strategy.is_available() is True

    @patch('platform.system')
    def test_is_available_on_non_windows(self, mock_platform):
        """Test is_available returns False on non-Windows."""
        mock_platform.return_value = 'Linux'

        strategy = WindowsPagerStrategy()
        assert strategy.is_available() is False


class TestFallbackPagerStrategy:
    """Test suite for FallbackPagerStrategy class."""

    def test_display_prints_content(self, capsys):
        """Test fallback displays content to stdout."""
        strategy = FallbackPagerStrategy()
        result = strategy.display("Test content", "Test Title")

        assert result is True

        captured = capsys.readouterr()
        assert "Test Title" in captured.out
        assert "Test content" in captured.out

    def test_display_without_title(self, capsys):
        """Test fallback displays content without title."""
        strategy = FallbackPagerStrategy()
        result = strategy.display("Test content")

        assert result is True

        captured = capsys.readouterr()
        assert "Test content" in captured.out

    def test_is_available_always_true(self):
        """Test fallback is always available."""
        strategy = FallbackPagerStrategy()
        assert strategy.is_available() is True


class TestPagerDisplay:
    """Test suite for PagerDisplay class."""

    @patch('platform.system')
    @patch('lib.pager_display.UnixPagerStrategy.is_available')
    def test_select_strategy_unix_linux(
        self,
        mock_unix_available,
        mock_platform
    ):
        """Test Unix strategy selected on Linux."""
        mock_platform.return_value = 'Linux'
        mock_unix_available.return_value = True

        display = PagerDisplay()

        assert isinstance(display.strategy, UnixPagerStrategy)

    @patch('platform.system')
    @patch('lib.pager_display.UnixPagerStrategy.is_available')
    def test_select_strategy_unix_darwin(
        self,
        mock_unix_available,
        mock_platform
    ):
        """Test Unix strategy selected on macOS."""
        mock_platform.return_value = 'Darwin'
        mock_unix_available.return_value = True

        display = PagerDisplay()

        assert isinstance(display.strategy, UnixPagerStrategy)

    @patch('platform.system')
    @patch('lib.pager_display.WindowsPagerStrategy.is_available')
    def test_select_strategy_windows(
        self,
        mock_windows_available,
        mock_platform
    ):
        """Test Windows strategy selected on Windows."""
        mock_platform.return_value = 'Windows'
        mock_windows_available.return_value = True

        display = PagerDisplay()

        assert isinstance(display.strategy, WindowsPagerStrategy)

    @patch('platform.system')
    def test_select_strategy_fallback_unknown_platform(self, mock_platform):
        """Test fallback strategy on unknown platform."""
        mock_platform.return_value = 'UnknownOS'

        display = PagerDisplay()

        assert isinstance(display.strategy, FallbackPagerStrategy)

    @patch('platform.system')
    @patch('lib.pager_display.UnixPagerStrategy.is_available')
    def test_select_strategy_fallback_pager_unavailable(
        self,
        mock_unix_available,
        mock_platform
    ):
        """Test fallback when pager unavailable."""
        mock_platform.return_value = 'Linux'
        mock_unix_available.return_value = False

        display = PagerDisplay()

        assert isinstance(display.strategy, FallbackPagerStrategy)

    def test_show_plan_formats_and_displays(
        self,
        mock_implementation_plan
    ):
        """Test show_plan formats plan and calls strategy."""
        display = PagerDisplay()

        with patch.object(display.strategy, 'display', return_value=True) as mock_display:
            result = display.show_plan(mock_implementation_plan)

        assert result is True
        mock_display.assert_called_once()

        # Verify formatted content
        call_args = mock_display.call_args
        content = call_args[0][0]
        title = call_args[0][1]

        assert "TASK-001" in title
        assert "TASK-001" in content
        assert "src/module1.py" in content

    def test_show_content_passes_to_strategy(self):
        """Test show_content passes content to strategy."""
        display = PagerDisplay()

        with patch.object(display.strategy, 'display', return_value=True) as mock_display:
            result = display.show_content("Test content", "Test Title")

        assert result is True
        mock_display.assert_called_once_with("Test content", "Test Title")

    def test_format_plan_includes_all_sections(
        self,
        mock_implementation_plan
    ):
        """Test _format_plan includes all plan sections."""
        display = PagerDisplay()
        formatted = display._format_plan(mock_implementation_plan)

        # Verify all sections present
        assert "IMPLEMENTATION PLAN: TASK-001" in formatted
        assert "Complexity Score: 6/10" in formatted
        assert "FILES TO CREATE/MODIFY:" in formatted
        assert "src/module1.py" in formatted
        assert "EXTERNAL DEPENDENCIES:" in formatted
        assert "requests" in formatted
        assert "IMPLEMENTATION PHASES:" in formatted
        assert "Phase 1: Repository interface" in formatted
        assert "RISK ASSESSMENT:" in formatted
        assert "Database connection handling" in formatted
        assert "TEST STRATEGY:" in formatted
        assert "DETAILED IMPLEMENTATION PLAN:" in formatted

    def test_format_plan_handles_missing_optional_fields(self):
        """Test _format_plan handles missing optional fields gracefully."""
        minimal_plan = ImplementationPlan(
            task_id="TASK-MINIMAL",
            raw_plan="Minimal plan"
        )

        display = PagerDisplay()
        formatted = display._format_plan(minimal_plan)

        assert "TASK-MINIMAL" in formatted
        assert "Minimal plan" in formatted


class TestEdgeCases:
    """Test edge cases and error scenarios."""

    def test_empty_content_display(self):
        """Test displaying empty content."""
        display = PagerDisplay()
        result = display.show_content("", "Empty")

        assert result is True  # Should succeed but display nothing

    def test_very_long_content(self):
        """Test handling very long content."""
        long_content = "x" * 100000  # 100KB content

        display = PagerDisplay()
        result = display.show_content(long_content, "Long Content")

        assert result is True

    def test_content_with_special_characters(self):
        """Test content with special characters."""
        special_content = "Content with\nnewlines\tand\ttabs\x00nulls"

        display = PagerDisplay()
        result = display.show_content(special_content, "Special")

        assert result is True

    def test_plan_with_unicode_characters(self):
        """Test plan with unicode characters."""
        plan = ImplementationPlan(
            task_id="TASK-UNICODE",
            files_to_create=["файл.py", "文件.py", "ファイル.py"],
            raw_plan="Plan with unicode: 你好世界 🚀"
        )

        display = PagerDisplay()
        formatted = display._format_plan(plan)

        assert "你好世界" in formatted
        assert "🚀" in formatted

    @patch('subprocess.run')
    def test_pager_timeout_handling(self, mock_run):
        """Test handling of pager process timeout."""
        mock_run.side_effect = subprocess.TimeoutExpired('less', 30)

        display = PagerDisplay()
        # Should fall back gracefully
        result = display.show_content("Test")

        # Fallback strategy should succeed
        assert result is True


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
