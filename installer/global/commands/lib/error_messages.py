"""
User-Friendly Error Message Wrappers.

Part of TASK-003E Phase 5 Day 2 implementation.
Provides human-readable error messages with actionable guidance for common errors.
"""

import errno
import os
from typing import Optional


def format_file_error(error: OSError, context: str) -> str:
    """
    Format file operation errors with errno-specific guidance.

    Args:
        error: OSError exception with errno
        context: Context string describing what was being attempted

    Returns:
        Formatted error message with problem description and solution

    Examples:
        >>> error = OSError(errno.EROFS, "Read-only file system")
        >>> msg = format_file_error(error, "write task to backlog")
        >>> print(msg)
        ❌ File operation failed: write task to backlog
        Problem: Read-only file system (errno 30)
        Solution: Check if the filesystem is mounted read-only...

        >>> error = OSError(errno.ENOSPC, "No space left on device")
        >>> msg = format_file_error(error, "save metrics")
        >>> print(msg)
        ❌ File operation failed: save metrics
        Problem: No space left on device (errno 28)
        Solution: Free up disk space...
    """
    error_code = getattr(error, 'errno', None)
    error_msg = str(error)

    # Build base message
    message_lines = [
        f"❌ File operation failed: {context}",
        f"Problem: {error_msg}"
    ]

    # Add errno if available
    if error_code is not None:
        message_lines[1] = f"Problem: {error_msg} (errno {error_code})"

    # Add solution based on errno
    solution = _get_errno_solution(error_code)
    if solution:
        message_lines.append(f"Solution: {solution}")
    else:
        # Generic solution for unknown errors
        message_lines.append(
            "Solution: Check file permissions and disk space. "
            "Contact system administrator if issue persists."
        )

    return "\n".join(message_lines)


def format_validation_error(error: ValueError, field: str) -> str:
    """
    Format validation errors with field context.

    Args:
        error: ValueError exception
        field: Field name that failed validation

    Returns:
        Formatted error message with problem description and solution

    Examples:
        >>> error = ValueError("must be positive")
        >>> msg = format_validation_error(error, "complexity_score")
        >>> print(msg)
        ❌ Validation failed for field: complexity_score
        Problem: must be positive
        Solution: Ensure 'complexity_score' contains a valid value...

        >>> error = ValueError("required field missing")
        >>> msg = format_validation_error(error, "task_id")
        >>> print(msg)
        ❌ Validation failed for field: task_id
        Problem: required field missing
        Solution: Ensure 'task_id' contains a valid value...
    """
    error_msg = str(error)

    message_lines = [
        f"❌ Validation failed for field: {field}",
        f"Problem: {error_msg}",
        f"Solution: Ensure '{field}' contains a valid value. "
        f"Check the field type and constraints."
    ]

    return "\n".join(message_lines)


def format_calculation_error(error: Exception, task_id: str) -> str:
    """
    Format calculation errors with task context.

    Args:
        error: Exception that occurred during calculation
        task_id: Task identifier for context

    Returns:
        Formatted error message with problem description and solution

    Examples:
        >>> error = ZeroDivisionError("division by zero")
        >>> msg = format_calculation_error(error, "TASK-001")
        >>> print(msg)
        ❌ Calculation failed for task: TASK-001
        Problem: division by zero (ZeroDivisionError)
        Solution: Check calculation inputs for task TASK-001...

        >>> error = KeyError("missing_metric")
        >>> msg = format_calculation_error(error, "TASK-002")
        >>> print(msg)
        ❌ Calculation failed for task: TASK-002
        Problem: 'missing_metric' (KeyError)
        Solution: Check calculation inputs for task TASK-002...
    """
    error_type = type(error).__name__
    error_msg = str(error)

    message_lines = [
        f"❌ Calculation failed for task: {task_id}",
        f"Problem: {error_msg} ({error_type})",
        f"Solution: Check calculation inputs for task {task_id}. "
        f"Verify all required metrics and data are available."
    ]

    return "\n".join(message_lines)


def _get_errno_solution(error_code: Optional[int]) -> Optional[str]:
    """
    Get solution guidance for specific errno values.

    Args:
        error_code: errno value from OSError

    Returns:
        Solution string or None if no specific guidance available

    Supported errno values:
        - 30 (EROFS): Read-only file system
        - 28 (ENOSPC): No space left on device
        - 13 (EACCES): Permission denied
        - 2 (ENOENT): No such file or directory
    """
    if error_code is None:
        return None

    # Map errno values to solutions
    errno_solutions = {
        errno.EROFS: (
            "Check if the filesystem is mounted read-only. "
            "Remount with write permissions: sudo mount -o remount,rw <device>"
        ),
        errno.ENOSPC: (
            "Free up disk space by removing unnecessary files. "
            "Check available space with 'df -h'"
        ),
        errno.EACCES: (
            "Check file and directory permissions. "
            "Ensure you have write access: ls -la <path>"
        ),
        errno.ENOENT: (
            "Verify the file or directory path exists. "
            "Check parent directories are created."
        ),
    }

    return errno_solutions.get(error_code)


# Module exports
__all__ = [
    "format_file_error",
    "format_validation_error",
    "format_calculation_error",
]
