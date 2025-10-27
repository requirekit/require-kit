"""
Plan Persistence Module - Saves and loads implementation plans for design-first workflow.

Part of TASK-006: Add Design-First Workflow Flags to task-work Command.
Updated by TASK-027: Convert Implementation Plan Storage from JSON to Markdown.

This module handles persisting implementation plans to disk when using the --design-only flag,
and loading them back when using the --implement-only flag.

Storage format: Markdown (.md) with frontmatter metadata for human readability and better git diffs.
Legacy format: JSON (.json) still supported for backward compatibility.

Storage location: docs/state/{task_id}/implementation_plan.md

Author: Claude (Anthropic)
Created: 2025-10-11
Updated: 2025-10-18
"""

from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import json

try:
    from .plan_markdown_renderer import PlanMarkdownRenderer, PlanMarkdownRendererError
    from .plan_markdown_parser import PlanMarkdownParser, PlanMarkdownParserError
    from .git_state_helper import commit_state_files
except ImportError:
    # Fallback for direct execution (tests)
    from plan_markdown_renderer import PlanMarkdownRenderer, PlanMarkdownRendererError
    from plan_markdown_parser import PlanMarkdownParser, PlanMarkdownParserError
    try:
        from git_state_helper import commit_state_files
    except ImportError:
        # If git_state_helper not available (e.g., in tests), provide no-op
        def commit_state_files(task_id: str, message: str = None) -> None:
            pass


class PlanPersistenceError(Exception):
    """Raised when plan persistence operations fail."""
    pass


def save_plan(
    task_id: str,
    plan: Dict[str, Any],
    review_result: Optional[Dict[str, Any]] = None
) -> str:
    """
    Save implementation plan to disk as markdown.

    Creates the state directory if it doesn't exist, then saves the plan as markdown
    with frontmatter metadata. This provides better human readability, clearer git diffs,
    and aligns with proven workflow patterns (John Hubbard's .md files).

    Args:
        task_id: Task identifier (e.g., "TASK-006")
        plan: Implementation plan dictionary containing:
            - files_to_create: List[str]
            - files_to_modify: List[str]
            - external_dependencies: List[str]
            - estimated_duration: str
            - estimated_loc: int
            - phases: List[str]
            - test_summary: str
            - risks: List[Dict]
        review_result: Optional architectural review results

    Returns:
        Absolute path to saved plan file (markdown)

    Raises:
        PlanPersistenceError: If save operation fails

    Example:
        >>> plan = {
        ...     "files_to_create": ["src/feature.py", "tests/test_feature.py"],
        ...     "estimated_duration": "4 hours"
        ... }
        >>> path = save_plan("TASK-006", plan)
        >>> print(path)
        /absolute/path/docs/state/TASK-006/implementation_plan.md
    """
    try:
        # Create state directory
        state_dir = Path("docs/state") / task_id
        state_dir.mkdir(parents=True, exist_ok=True)

        # Add metadata
        plan_with_metadata = {
            "task_id": task_id,
            "saved_at": datetime.now().isoformat(),
            "version": 1,
            "plan": plan
        }

        # Mark if plan is completely empty (for validation in load_plan_summary)
        # Only mark as empty if plan dict has NO keys at all
        if plan is None or (isinstance(plan, dict) and len(plan) == 0):
            plan_with_metadata["empty_plan"] = True

        # Add review result if provided
        if review_result:
            plan_with_metadata["architectural_review"] = review_result

        # Save as Markdown (single source of truth)
        md_path = state_dir / "implementation_plan.md"
        renderer = PlanMarkdownRenderer()
        renderer.save_markdown(plan_with_metadata, md_path)

        # Commit state files to git (for Conductor worktree support)
        try:
            commit_state_files(task_id, f"Save implementation plan for {task_id}")
        except Exception:
            # Don't fail save operation if git commit fails
            # (may not be in a git repo, or git may not be available)
            pass

        return str(md_path.absolute())

    except (PlanMarkdownRendererError, Exception) as e:
        raise PlanPersistenceError(
            f"Failed to save implementation plan for {task_id}: {e}"
        ) from e


def load_plan(task_id: str) -> Optional[Dict[str, Any]]:
    """
    Load implementation plan from disk.

    Prefers markdown format (.md) over legacy JSON format (.json).
    This provides backward compatibility while encouraging the new markdown format.

    Args:
        task_id: Task identifier (e.g., "TASK-006")

    Returns:
        Plan dictionary if found, None if file doesn't exist

    Raises:
        PlanPersistenceError: If load operation fails (but file exists)

    Example:
        >>> plan = load_plan("TASK-006")
        >>> if plan:
        ...     print(plan["plan"]["estimated_duration"])
        4 hours
    """
    md_path = Path("docs/state") / task_id / "implementation_plan.md"
    json_path = Path("docs/state") / task_id / "implementation_plan.json"

    # Try markdown first (primary format)
    if md_path.exists():
        try:
            parser = PlanMarkdownParser()
            return parser.parse_file(md_path)
        except PlanMarkdownParserError as e:
            raise PlanPersistenceError(
                f"Failed to load markdown plan for {task_id}: {e}"
            ) from e

    # Fall back to JSON (legacy format)
    if json_path.exists():
        try:
            with open(json_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise PlanPersistenceError(
                f"Failed to load JSON plan for {task_id}: {e}"
            ) from e

    # No plan found
    return None


def plan_exists(task_id: str) -> bool:
    """
    Check if implementation plan exists for task.

    Checks for both markdown (.md) and legacy JSON (.json) formats.

    Args:
        task_id: Task identifier (e.g., "TASK-006")

    Returns:
        True if plan file exists (either format), False otherwise

    Example:
        >>> if plan_exists("TASK-006"):
        ...     plan = load_plan("TASK-006")
        ... else:
        ...     print("No plan found")
    """
    md_path = Path("docs/state") / task_id / "implementation_plan.md"
    json_path = Path("docs/state") / task_id / "implementation_plan.json"
    return md_path.exists() or json_path.exists()


def get_plan_path(task_id: str) -> Optional[Path]:
    """
    Get path to implementation plan file if it exists.

    Checks for both markdown (.md) and legacy JSON (.json) formats,
    returning the markdown path if both exist.

    Args:
        task_id: Task identifier (e.g., "TASK-006")

    Returns:
        Path to plan file if exists, None otherwise

    Example:
        >>> path = get_plan_path("TASK-006")
        >>> if path:
        ...     print(f"Plan at: {path}")
        Plan at: docs/state/TASK-006/implementation_plan.md
    """
    md_path = Path("docs/state") / task_id / "implementation_plan.md"
    json_path = Path("docs/state") / task_id / "implementation_plan.json"

    # Prefer markdown over JSON
    if md_path.exists():
        return md_path
    elif json_path.exists():
        return json_path
    else:
        return None


def delete_plan(task_id: str) -> None:
    """
    Delete implementation plan from disk.

    Use with caution - this is typically only called when cancelling a task
    or when re-running design phase. Deletes both markdown and JSON formats if present.

    Args:
        task_id: Task identifier (e.g., "TASK-006")

    Raises:
        PlanPersistenceError: If delete operation fails

    Example:
        >>> delete_plan("TASK-006")
        >>> plan_exists("TASK-006")
        False
    """
    md_path = Path("docs/state") / task_id / "implementation_plan.md"
    json_path = Path("docs/state") / task_id / "implementation_plan.json"

    try:
        # Delete markdown if exists
        if md_path.exists():
            md_path.unlink()

        # Delete JSON if exists (legacy cleanup)
        if json_path.exists():
            json_path.unlink()

    except Exception as e:
        raise PlanPersistenceError(
            f"Failed to delete implementation plan for {task_id}: {e}"
        ) from e


def save_plan_version(
    task_id: str,
    plan: Dict[str, Any],
    modifications: Optional[list] = None
) -> str:
    """
    Save implementation plan with version increment and automatic backup.

    Creates a backup of the current plan in versions/ directory before saving
    the updated plan. This provides version history for plan modifications.

    Args:
        task_id: Task identifier (e.g., "TASK-029")
        plan: Implementation plan dictionary (with updated version number)
        modifications: Optional list of ModificationRecord objects documenting changes

    Returns:
        Absolute path to saved plan file (markdown)

    Raises:
        PlanPersistenceError: If save or backup operation fails

    Example:
        >>> plan = load_plan("TASK-029")
        >>> plan['version'] = 2
        >>> path = save_plan_version("TASK-029", plan, modifications)
        >>> print(path)
        /absolute/path/docs/state/TASK-029/implementation_plan.md
    """
    try:
        # Backup current version if it exists
        _backup_plan_version(task_id)

        # Add modification history to plan if provided
        if modifications:
            # Convert ModificationRecord objects to dicts for serialization
            mod_dicts = []
            for mod in modifications:
                mod_dict = {
                    "category": mod.category.value if hasattr(mod, 'category') else str(mod),
                    "action": getattr(mod, 'action', 'unknown'),
                    "details": getattr(mod, 'details', str(mod))
                }
                mod_dicts.append(mod_dict)

            # Add to plan metadata
            if 'modification_history' not in plan:
                plan['modification_history'] = []
            plan['modification_history'].extend(mod_dicts)

        # Save updated plan (uses existing save_plan function)
        return save_plan(task_id, plan.get('plan', {}), plan.get('architectural_review'))

    except Exception as e:
        raise PlanPersistenceError(
            f"Failed to save plan version for {task_id}: {e}"
        ) from e


def _backup_plan_version(task_id: str) -> Optional[Path]:
    """
    Backup current plan to versions/ directory.

    Creates a timestamped backup of the current implementation plan before
    modifications are saved. Backups are stored in docs/state/{task_id}/versions/.

    Args:
        task_id: Task identifier (e.g., "TASK-029")

    Returns:
        Path to backup file if backup was created, None if no current plan exists

    Raises:
        PlanPersistenceError: If backup operation fails
    """
    try:
        # Check if current plan exists
        current_plan_path = get_plan_path(task_id)
        if not current_plan_path or not current_plan_path.exists():
            # No current plan to backup
            return None

        # Create versions directory
        versions_dir = Path("docs/state") / task_id / "versions"
        versions_dir.mkdir(parents=True, exist_ok=True)

        # Load current plan to get version number
        current_plan = load_plan(task_id)
        version = current_plan.get('version', 1) if current_plan else 1

        # Create backup filename with version and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"implementation_plan_v{version}_{timestamp}.md"
        backup_path = versions_dir / backup_filename

        # Copy current plan to backup location
        import shutil
        shutil.copy2(current_plan_path, backup_path)

        return backup_path

    except Exception as e:
        # Log error but don't fail the save operation
        # Backup is nice-to-have, not critical
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Failed to backup plan version for {task_id}: {e}")
        return None


# Module exports
__all__ = [
    "save_plan",
    "load_plan",
    "plan_exists",
    "get_plan_path",
    "delete_plan",
    "save_plan_version",
    "PlanPersistenceError"
]
