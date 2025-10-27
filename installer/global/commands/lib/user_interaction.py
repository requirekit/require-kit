"""
Platform-agnostic user input handling with non-blocking countdown timer.

This module provides cross-platform support for non-blocking keyboard input
using the Strategy Pattern. It handles terminal state management and implements
a countdown timer with sub-second accuracy.

Architecture:
    - InputStrategy Protocol: Abstract interface for platform-specific I/O
    - UnixInputStrategy: Implementation using select() and termios
    - WindowsInputStrategy: Implementation using msvcrt
    - countdown_timer(): Main countdown function with display updates

Example:
    >>> from user_interaction import countdown_timer
    >>> result = countdown_timer(
    ...     duration_seconds=10,
    ...     message="Review architectural plan?",
    ...     options="[Enter] to review, [C]ancel, or wait to auto-proceed"
    ... )
    >>> if result == "timeout":
    ...     print("Auto-proceeding...")
    >>> elif result == "enter":
    ...     print("Escalating to full review...")
    >>> elif result == "cancel":
    ...     print("Task cancelled")
"""

import sys
import time
from abc import abstractmethod
from contextlib import contextmanager
from typing import Generator, Literal, Optional, Protocol

# Platform-specific imports
if sys.platform == "win32":
    import msvcrt
else:
    import select
    import termios
    import tty


CountdownResult = Literal["timeout", "enter", "cancel"]


class InputStrategy(Protocol):
    """
    Protocol for platform-specific non-blocking input strategies.

    Implementations must provide:
    - check_input(): Check if input is available and return key pressed
    - cleanup(): Restore terminal state on exit
    """

    @abstractmethod
    def check_input(self) -> Optional[str]:
        """
        Check for keyboard input without blocking.

        Returns:
            Optional[str]: Key pressed (lowercase), or None if no input available
        """
        ...

    @abstractmethod
    def cleanup(self) -> None:
        """
        Restore terminal state to original configuration.

        Called automatically by context manager on exit.
        """
        ...


class UnixInputStrategy:
    """
    Non-blocking input strategy for Unix-like systems (macOS, Linux).

    Uses select() for non-blocking I/O and termios for raw terminal mode.
    Automatically restores terminal state on cleanup.

    Example:
        >>> strategy = UnixInputStrategy()
        >>> strategy.setup()
        >>> key = strategy.check_input()  # Non-blocking
        >>> strategy.cleanup()  # Restore terminal
    """

    def __init__(self):
        """Initialize Unix input strategy with terminal state tracking."""
        self._original_settings: Optional[list] = None

    def setup(self) -> None:
        """
        Configure terminal for raw input mode.

        Saves original terminal settings for restoration on cleanup.
        """
        self._original_settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin.fileno())

    def check_input(self) -> Optional[str]:
        """
        Check for keyboard input using select().

        Returns:
            Optional[str]: Lowercase key pressed, or None if no input
        """
        # Use select with 0 timeout for non-blocking check
        ready, _, _ = select.select([sys.stdin], [], [], 0)
        if ready:
            char = sys.stdin.read(1)
            return char.lower()
        return None

    def cleanup(self) -> None:
        """
        Restore original terminal settings.

        Safe to call multiple times - only restores if settings were saved.
        """
        if self._original_settings is not None:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._original_settings)
            self._original_settings = None


class WindowsInputStrategy:
    """
    Non-blocking input strategy for Windows systems.

    Uses msvcrt.kbhit() and msvcrt.getch() for non-blocking keyboard input.
    No terminal state restoration needed on Windows.

    Example:
        >>> strategy = WindowsInputStrategy()
        >>> strategy.setup()
        >>> key = strategy.check_input()  # Non-blocking
        >>> strategy.cleanup()  # No-op on Windows
    """

    def setup(self) -> None:
        """
        Setup input strategy (no-op on Windows).

        Windows console API doesn't require terminal mode changes.
        """
        pass

    def check_input(self) -> Optional[str]:
        """
        Check for keyboard input using msvcrt.

        Returns:
            Optional[str]: Lowercase key pressed, or None if no input
        """
        if msvcrt.kbhit():
            char = msvcrt.getch().decode('utf-8', errors='ignore')
            return char.lower()
        return None

    def cleanup(self) -> None:
        """
        Cleanup strategy (no-op on Windows).

        Windows console API doesn't require restoration.
        """
        pass


def create_input_strategy() -> InputStrategy:
    """
    Factory function to create appropriate input strategy for current platform.

    Returns:
        InputStrategy: Platform-specific input strategy (Unix or Windows)

    Example:
        >>> strategy = create_input_strategy()
        >>> strategy.setup()
        >>> # Use strategy...
        >>> strategy.cleanup()
    """
    if sys.platform == "win32":
        return WindowsInputStrategy()
    else:
        return UnixInputStrategy()


@contextmanager
def managed_input_strategy() -> Generator[InputStrategy, None, None]:
    """
    Context manager for input strategy lifecycle management.

    Automatically calls setup() on entry and cleanup() on exit,
    ensuring terminal state is always restored even on exceptions.

    Yields:
        InputStrategy: Configured input strategy ready for use

    Example:
        >>> with managed_input_strategy() as strategy:
        ...     while True:
        ...         key = strategy.check_input()
        ...         if key:
        ...             break
        # Terminal automatically restored here
    """
    strategy = create_input_strategy()
    strategy.setup()
    try:
        yield strategy
    finally:
        strategy.cleanup()


def countdown_timer(
    duration_seconds: int,
    message: str,
    options: str,
    cancel_key: str = "c"
) -> CountdownResult:
    """
    Display countdown timer with non-blocking keyboard input.

    Shows a countdown from duration_seconds to 0, updating on the same line.
    Checks for keyboard input every ~50ms for responsive interaction.

    Supported actions:
        - Enter key: Escalate to full review (return "enter")
        - Cancel key (default 'c'): Cancel task (return "cancel")
        - Timeout: Auto-proceed when countdown reaches 0 (return "timeout")
        - Ctrl+C: Emergency exit (re-raise KeyboardInterrupt)

    Args:
        duration_seconds: Countdown duration in seconds (>0)
        message: Primary message to display above countdown
        options: Help text describing available actions
        cancel_key: Key to cancel (default 'c', case-insensitive)

    Returns:
        CountdownResult: One of "timeout", "enter", or "cancel"

    Raises:
        KeyboardInterrupt: On Ctrl+C (emergency exit)
        ValueError: If duration_seconds <= 0

    Example:
        >>> result = countdown_timer(
        ...     duration_seconds=10,
        ...     message="Architectural review starting...",
        ...     options="[Enter] to review, [C]ancel, or wait"
        ... )
        >>> if result == "timeout":
        ...     print("Auto-approved!")
    """
    if duration_seconds <= 0:
        raise ValueError(f"duration_seconds must be > 0, got {duration_seconds}")

    cancel_key_lower = cancel_key.lower()

    # Display header (static)
    print(f"\n{message}")
    print(f"{options}\n")

    try:
        with managed_input_strategy() as strategy:
            start_time = time.monotonic()
            end_time = start_time + duration_seconds

            # Polling interval for input checks (~50ms for responsiveness)
            poll_interval = 0.05

            while True:
                current_time = time.monotonic()
                remaining = end_time - current_time

                # Check if countdown expired
                if remaining <= 0:
                    # Clear countdown line and show completion
                    print("\r" + " " * 60 + "\r", end="", flush=True)
                    print("Auto-proceeding...\n", flush=True)
                    return "timeout"

                # Update countdown display (same line using \r)
                seconds_left = int(remaining) + 1  # Round up for display
                print(
                    f"\rCountdown: {seconds_left}s remaining... ",
                    end="",
                    flush=True
                )

                # Check for keyboard input
                key = strategy.check_input()
                if key is not None:
                    # Clear countdown line
                    print("\r" + " " * 60 + "\r", end="", flush=True)

                    # Handle Enter key (multiple representations)
                    if key in ('\r', '\n'):
                        print("Escalating to full review...\n", flush=True)
                        return "enter"

                    # Handle cancel key (case-insensitive)
                    elif key == cancel_key_lower:
                        print("Task cancelled.\n", flush=True)
                        return "cancel"

                    # Ignore other keys (redraw countdown)
                    else:
                        continue

                # Sleep for polling interval
                time.sleep(poll_interval)

    except KeyboardInterrupt:
        # Emergency exit - clear line and re-raise
        print("\r" + " " * 60 + "\r", end="", flush=True)
        print("Interrupted.\n", flush=True)
        raise


class FileOperations:
    """
    Utility class for atomic file operations.

    Provides safe file write operations using temp file + os.replace()
    pattern to ensure atomicity and prevent data corruption on failures.

    Example:
        >>> FileOperations.atomic_write(
        ...     file_path=Path("task.md"),
        ...     content="Updated content",
        ...     encoding="utf-8"
        ... )
    """

    @staticmethod
    def atomic_write(file_path: "Path", content: str, encoding: str = "utf-8") -> None:
        """
        Write content to file atomically using temp file pattern.

        Uses temp file + os.replace() to ensure either complete write
        or no change (no partial writes on failure).

        Args:
            file_path: Target file path
            content: Content to write
            encoding: Text encoding (default utf-8)

        Raises:
            OSError: On file system errors
            ValueError: If file_path is not a Path object

        Example:
            >>> import tempfile
            >>> from pathlib import Path
            >>> tmp = Path(tempfile.mktemp())
            >>> FileOperations.atomic_write(tmp, "test content")
            >>> assert tmp.read_text() == "test content"
            >>> tmp.unlink()  # cleanup
        """
        import os
        import tempfile
        from pathlib import Path

        if not isinstance(file_path, Path):
            raise ValueError(f"file_path must be Path object, got {type(file_path)}")

        # Create temp file in same directory for atomic replace
        file_dir = file_path.parent
        file_dir.mkdir(parents=True, exist_ok=True)

        # Use NamedTemporaryFile in same directory
        with tempfile.NamedTemporaryFile(
            mode='w',
            encoding=encoding,
            dir=file_dir,
            delete=False,
            suffix='.tmp'
        ) as tmp_file:
            tmp_path = tmp_file.name
            tmp_file.write(content)
            tmp_file.flush()
            os.fsync(tmp_file.fileno())  # Ensure data written to disk

        # Atomic replace (POSIX guarantees atomicity)
        os.replace(tmp_path, str(file_path))


# Module exports
__all__ = [
    "InputStrategy",
    "UnixInputStrategy",
    "WindowsInputStrategy",
    "create_input_strategy",
    "managed_input_strategy",
    "countdown_timer",
    "CountdownResult",
    "FileOperations",
]
