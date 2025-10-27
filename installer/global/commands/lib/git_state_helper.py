"""
Git State Helper - Simplified utility for committing task state in git worktrees.

This module provides three simple utility functions for managing task state files
in git repositories, with special support for git worktrees (used by Conductor).

Design: SIMPLIFIED approach (approved by architectural review)
- Single module with 3 focused functions
- No facade patterns or complex abstractions
- ~30 lines of actual code
- Cross-platform compatible (pathlib)

Part of TASK-031: Fix task-work and task-complete State Loss in Conductor Workspaces
Architectural Review Score: 62/100 (Approved with Recommendations)
Complexity: 3/10 (Simple)

Author: Claude (Anthropic)
Created: 2025-10-18
"""

from pathlib import Path
import subprocess
from typing import Optional


def get_git_root() -> Path:
    """Get git repository root (works in worktrees).

    Uses `git rev-parse --show-toplevel` which correctly returns the repository
    root even when executed from within a git worktree. This is crucial for
    Conductor workspaces where each worktree has its own working directory but
    shares the same repository.

    Returns:
        Path: Absolute path to git repository root

    Raises:
        subprocess.CalledProcessError: If not in a git repository

    Example:
        >>> git_root = get_git_root()
        >>> print(git_root)
        /Users/username/Projects/my-project
    """
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True
    )
    return Path(result.stdout.strip())


def resolve_state_dir(task_id: str) -> Path:
    """Resolve state directory path relative to git root.

    Creates the state directory if it doesn't exist. The state directory is
    always relative to the git repository root, ensuring consistent paths
    across all worktrees.

    Args:
        task_id: Task identifier (e.g., "TASK-031")

    Returns:
        Path: Absolute path to state directory for this task

    Example:
        >>> state_dir = resolve_state_dir("TASK-031")
        >>> print(state_dir)
        /Users/username/Projects/my-project/docs/state/TASK-031
    """
    git_root = get_git_root()
    state_dir = git_root / "docs" / "state" / task_id
    state_dir.mkdir(parents=True, exist_ok=True)
    return state_dir


def commit_state_files(task_id: str, message: Optional[str] = None) -> None:
    """Stage and commit state files for a task.

    Stages all files in the task's state directory and creates a commit.
    Does not fail if there are no changes to commit (silent success).

    This function should be called after:
    1. task-work completes (after Phase 5)
    2. task-complete finishes (after moving to completed state)

    Args:
        task_id: Task identifier (e.g., "TASK-031")
        message: Optional custom commit message. If None, uses default message.

    Note:
        Does not fail if nothing to commit (silent when no changes).
        Does not push to remote (that's a separate operation).

    Example:
        >>> commit_state_files("TASK-031", "Save implementation state for TASK-031")
        # Creates commit with all state files for TASK-031

        >>> commit_state_files("TASK-031")  # Uses default message
        # Creates commit with message "Save state for TASK-031"
    """
    state_dir = resolve_state_dir(task_id)

    # Stage state directory (all files within it)
    subprocess.run(
        ["git", "add", str(state_dir)],
        check=True,
        capture_output=True
    )

    # Commit if there are changes (check=False to avoid error on no changes)
    commit_message = message or f"Save state for {task_id}"
    subprocess.run(
        ["git", "commit", "-m", commit_message],
        check=False,  # Don't fail if nothing to commit
        capture_output=True
    )
