"""
Cross-platform pager display for implementation plans.

This module provides a Strategy Pattern implementation for displaying
implementation plans in the system pager (less/more) with cross-platform support.

Architecture:
    - PagerStrategy: Abstract base for platform-specific pagers
    - UnixPagerStrategy: Unix/Linux/macOS pager (less/more)
    - WindowsPagerStrategy: Windows pager (more.com)
    - PagerDisplay: Main coordinator for pager operations

Example:
    >>> from pager_display import PagerDisplay
    >>> from complexity_models import ImplementationPlan
    >>>
    >>> display = PagerDisplay()
    >>> display.show_plan(plan)
    # Opens plan in system pager
"""

import os
import platform
import subprocess
import sys
import tempfile
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

try:
    from .complexity_models import ImplementationPlan
except ImportError:
    from complexity_models import ImplementationPlan


def format_plan_section(section_content: Optional[str], section_name: str) -> str:
    """
    Format plan section with empty value handling.

    Provides user-friendly messages for None or whitespace-only sections
    instead of displaying "None" or empty strings.

    Args:
        section_content: The section content (may be None or empty)
        section_name: The name of the section (for user-friendly message)

    Returns:
        str: Formatted section content or user-friendly placeholder

    Example:
        >>> format_plan_section(None, "overview")
        '[No overview provided]'

        >>> format_plan_section("   ", "testing")
        '[No testing provided]'

        >>> format_plan_section("Valid content", "steps")
        'Valid content'
    """
    if section_content is None or section_content.strip() == "":
        return f"[No {section_name.lower()} provided]"
    return section_content


class PagerStrategy(ABC):
    """
    Abstract base class for platform-specific pager implementations.

    Defines the interface for displaying content in a system pager.
    Implementations handle platform-specific command invocation and
    error handling.
    """

    @abstractmethod
    def display(self, content: str, title: Optional[str] = None) -> bool:
        """
        Display content in system pager.

        Args:
            content: Text content to display
            title: Optional title for the pager window

        Returns:
            bool: True if successful, False otherwise
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if this pager strategy is available on current system.

        Returns:
            bool: True if pager is available and executable
        """
        pass


class UnixPagerStrategy(PagerStrategy):
    """
    Pager strategy for Unix-like systems (Linux, macOS, BSD).

    Uses 'less' as primary pager, falls back to 'more' if less not available.
    Supports ANSI colors and provides helpful key bindings.

    Example:
        >>> strategy = UnixPagerStrategy()
        >>> if strategy.is_available():
        ...     strategy.display("Plan content...")
    """

    def __init__(self):
        """Initialize Unix pager strategy with preferred pager selection."""
        # Prefer 'less' for better features, fallback to 'more'
        self.pager_cmd = self._select_pager()

    def _select_pager(self) -> str:
        """
        Select available pager command.

        Priority:
            1. PAGER environment variable
            2. 'less' command
            3. 'more' command

        Returns:
            str: Pager command name
        """
        # Check environment variable first
        env_pager = os.environ.get('PAGER')
        if env_pager and self._command_exists(env_pager):
            return env_pager

        # Try 'less' first (better features)
        if self._command_exists('less'):
            return 'less'

        # Fallback to 'more'
        if self._command_exists('more'):
            return 'more'

        # No pager available
        return ''

    def _command_exists(self, command: str) -> bool:
        """
        Check if command exists in PATH.

        Args:
            command: Command name to check

        Returns:
            bool: True if command is executable
        """
        try:
            # Use 'which' to check command availability
            result = subprocess.run(
                ['which', command],
                capture_output=True,
                text=True,
                timeout=2
            )
            return result.returncode == 0
        except Exception:
            return False

    def display(self, content: str, title: Optional[str] = None) -> bool:
        """
        Display content in Unix pager.

        Args:
            content: Text content to display
            title: Optional title (shown in pager prompt)

        Returns:
            bool: True if display succeeded
        """
        if not self.pager_cmd:
            return False

        try:
            # Build pager command with options
            cmd = self._build_command(title)

            # Write content to temporary file
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.txt',
                delete=False,
                encoding='utf-8'
            ) as tmp_file:
                tmp_file.write(content)
                tmp_path = tmp_file.name

            try:
                # Invoke pager with file
                result = subprocess.run(
                    cmd + [tmp_path],
                    stdin=subprocess.DEVNULL,
                    check=False
                )
                return result.returncode == 0
            finally:
                # Clean up temp file
                Path(tmp_path).unlink(missing_ok=True)

        except Exception as e:
            print(f"Error displaying in pager: {e}", file=sys.stderr)
            return False

    def _build_command(self, title: Optional[str] = None) -> list:
        """
        Build pager command with appropriate options.

        Args:
            title: Optional title for pager

        Returns:
            list: Command and arguments
        """
        cmd = [self.pager_cmd]

        if self.pager_cmd == 'less':
            # Less options:
            # -R: Allow ANSI colors
            # -F: Quit if content fits on one screen
            # -X: Don't clear screen on exit
            # -S: Chop long lines instead of wrapping
            cmd.extend(['-R', '-F', '-X'])

            if title:
                # Set prompt with title
                cmd.extend(['-Ps', f'{title} (press q to quit)'])

        return cmd

    def is_available(self) -> bool:
        """
        Check if Unix pager is available.

        Returns:
            bool: True if pager command exists
        """
        return bool(self.pager_cmd)


class WindowsPagerStrategy(PagerStrategy):
    """
    Pager strategy for Windows systems.

    Uses 'more.com' command available in Windows CMD/PowerShell.
    Provides basic pagination functionality.

    Example:
        >>> strategy = WindowsPagerStrategy()
        >>> if strategy.is_available():
        ...     strategy.display("Plan content...")
    """

    def display(self, content: str, title: Optional[str] = None) -> bool:
        """
        Display content in Windows pager.

        Args:
            content: Text content to display
            title: Optional title (printed before content)

        Returns:
            bool: True if display succeeded
        """
        try:
            # Print title if provided
            if title:
                print(f"\n{'=' * 60}")
                print(f"{title}")
                print(f"{'=' * 60}\n")

            # Write content to temporary file
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.txt',
                delete=False,
                encoding='utf-8'
            ) as tmp_file:
                tmp_file.write(content)
                tmp_path = tmp_file.name

            try:
                # Invoke more.com with file
                result = subprocess.run(
                    ['more', tmp_path],
                    stdin=subprocess.DEVNULL,
                    check=False,
                    shell=True  # Required for Windows
                )
                return result.returncode == 0
            finally:
                # Clean up temp file
                Path(tmp_path).unlink(missing_ok=True)

        except Exception as e:
            print(f"Error displaying in pager: {e}", file=sys.stderr)
            return False

    def is_available(self) -> bool:
        """
        Check if Windows pager is available.

        Returns:
            bool: True if more.com exists (always true on Windows)
        """
        # more.com is always available on Windows
        return platform.system() == 'Windows'


class FallbackPagerStrategy(PagerStrategy):
    """
    Fallback strategy when no pager is available.

    Simply prints content to stdout without pagination.
    Used as last resort to ensure content is always displayable.
    """

    def display(self, content: str, title: Optional[str] = None) -> bool:
        """
        Display content without pagination.

        Args:
            content: Text content to display
            title: Optional title

        Returns:
            bool: Always returns True
        """
        if title:
            print(f"\n{'=' * 60}")
            print(f"{title}")
            print(f"{'=' * 60}\n")

        print(content)
        return True

    def is_available(self) -> bool:
        """
        Check if fallback strategy is available.

        Returns:
            bool: Always returns True (stdout always available)
        """
        return True


class PagerDisplay:
    """
    Main coordinator for pager display operations.

    Automatically selects appropriate pager strategy based on platform
    and displays implementation plans in a readable format.

    Example:
        >>> display = PagerDisplay()
        >>> display.show_plan(implementation_plan)
        # Opens plan in system pager

        >>> # Or display raw content
        >>> display.show_content("Custom content...", title="My Title")
    """

    def __init__(self):
        """Initialize pager display with platform-appropriate strategy."""
        self.strategy = self._select_strategy()

    def _select_strategy(self) -> PagerStrategy:
        """
        Select appropriate pager strategy for current platform.

        Returns:
            PagerStrategy: Platform-specific pager implementation
        """
        system = platform.system()

        if system in ('Linux', 'Darwin', 'FreeBSD', 'OpenBSD'):
            # Unix-like systems
            strategy = UnixPagerStrategy()
            if strategy.is_available():
                return strategy

        elif system == 'Windows':
            # Windows systems
            strategy = WindowsPagerStrategy()
            if strategy.is_available():
                return strategy

        # Fallback for unknown platforms or when pager unavailable
        return FallbackPagerStrategy()

    def show_plan(self, plan: ImplementationPlan) -> bool:
        """
        Display implementation plan in pager.

        Formats plan with sections for files, dependencies, phases,
        risks, and raw plan content.

        Args:
            plan: ImplementationPlan to display

        Returns:
            bool: True if display succeeded
        """
        content = self._format_plan(plan)
        title = f"Implementation Plan: {plan.task_id}"
        return self.strategy.display(content, title)

    def show_content(self, content: str, title: Optional[str] = None) -> bool:
        """
        Display arbitrary content in pager.

        Args:
            content: Text content to display
            title: Optional title

        Returns:
            bool: True if display succeeded
        """
        return self.strategy.display(content, title)

    def _format_plan(self, plan: ImplementationPlan) -> str:
        """
        Format implementation plan for display.

        Args:
            plan: ImplementationPlan to format

        Returns:
            str: Formatted plan text
        """
        sections = []

        # Header
        sections.append("=" * 70)
        sections.append(f"IMPLEMENTATION PLAN: {plan.task_id}")
        sections.append("=" * 70)
        sections.append("")

        # Complexity Score
        if plan.complexity_score:
            score = plan.complexity_score.total_score
            sections.append(f"Complexity Score: {score}/10")
            sections.append(f"Review Mode: {plan.complexity_score.review_mode.value}")
            sections.append("")

        # Files to Create
        if plan.files_to_create:
            sections.append("FILES TO CREATE/MODIFY:")
            sections.append("-" * 70)
            for file_path in plan.files_to_create:
                sections.append(f"  - {file_path}")
            sections.append("")

        # External Dependencies
        if plan.external_dependencies:
            sections.append("EXTERNAL DEPENDENCIES:")
            sections.append("-" * 70)
            for dep in plan.external_dependencies:
                sections.append(f"  - {dep}")
            sections.append("")

        # Phases
        if plan.phases:
            sections.append("IMPLEMENTATION PHASES:")
            sections.append("-" * 70)
            for i, phase in enumerate(plan.phases, 1):
                sections.append(f"  {i}. {phase}")
            sections.append("")

        # Risk Details
        if plan.risk_details:
            sections.append("RISK ASSESSMENT:")
            sections.append("-" * 70)
            for risk in plan.risk_details:
                severity = risk.get("severity", "unknown").upper()
                description = risk.get("description", "No description")
                mitigation = risk.get("mitigation", "No mitigation")
                sections.append(f"  [{severity}] {description}")
                sections.append(f"    Mitigation: {mitigation}")
                sections.append("")

        # Test Summary
        if plan.test_summary:
            sections.append("TEST STRATEGY:")
            sections.append("-" * 70)
            sections.append(f"  {plan.test_summary}")
            sections.append("")

        # Raw Plan
        sections.append("DETAILED IMPLEMENTATION PLAN:")
        sections.append("-" * 70)
        sections.append(format_plan_section(plan.raw_plan, "detailed implementation plan"))
        sections.append("")

        # Footer
        sections.append("=" * 70)
        sections.append("Press 'q' to quit, arrow keys to navigate")
        sections.append("=" * 70)

        return "\n".join(sections)


# Module exports
__all__ = [
    "format_plan_section",
    "PagerStrategy",
    "UnixPagerStrategy",
    "WindowsPagerStrategy",
    "FallbackPagerStrategy",
    "PagerDisplay",
]
