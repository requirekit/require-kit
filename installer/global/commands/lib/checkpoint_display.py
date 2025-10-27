"""
Checkpoint Display Module - Enhanced Phase 2.8 checkpoint with implementation plan summary.

Part of TASK-028: Enhance Phase 2.8 Checkpoint Display with Plan Summary.

This module loads saved implementation plans and displays them in a user-friendly format
during Phase 2.8 checkpoint (human review of implementation plan). Provides context for
developers to make informed approve/modify/cancel decisions.

Storage location: docs/state/{task_id}/implementation_plan.md (or .json for legacy)

Author: Claude (Anthropic)
Created: 2025-10-18
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Optional, Dict, Any
import logging

try:
    from .plan_persistence import load_plan, plan_exists, get_plan_path, PlanPersistenceError
    from .plan_modifier import PlanModifier, PlanModificationError
except ImportError:
    # Fallback for direct execution (tests)
    from plan_persistence import load_plan, plan_exists, get_plan_path, PlanPersistenceError
    from plan_modifier import PlanModifier, PlanModificationError

# Configure logging
logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """Risk severity levels for implementation risks."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

    @property
    def icon(self) -> str:
        """Get severity icon for display."""
        return {
            RiskLevel.HIGH: "🔴",
            RiskLevel.MEDIUM: "🟡",
            RiskLevel.LOW: "🟢"
        }[self]

    @classmethod
    def from_string(cls, level: str) -> 'RiskLevel':
        """Parse risk level from string (case-insensitive)."""
        level_lower = level.strip().lower()
        for risk_level in cls:
            if risk_level.value == level_lower:
                return risk_level
        # Default to MEDIUM if unknown
        logger.warning(f"Unknown risk level '{level}', defaulting to MEDIUM")
        return cls.MEDIUM


@dataclass
class FileChange:
    """Represents a file to be created or modified.

    Attributes:
        path: Relative file path (e.g., "src/feature.py")
        description: Brief description of changes (truncated to 80 chars)
        change_type: "create" or "modify"
    """
    path: str
    description: str
    change_type: str = "create"

    def __post_init__(self):
        """Truncate description if too long."""
        if len(self.description) > 80:
            self.description = self.description[:77] + "..."


@dataclass
class Dependency:
    """External dependency required for implementation.

    Attributes:
        name: Package/library name
        version: Version requirement (optional)
        purpose: Why this dependency is needed
    """
    name: str
    version: Optional[str] = None
    purpose: Optional[str] = None


@dataclass
class Risk:
    """Implementation risk with severity and mitigation.

    Attributes:
        description: Risk description
        level: Severity level (HIGH/MEDIUM/LOW)
        mitigation: How to mitigate this risk (optional)
    """
    description: str
    level: RiskLevel
    mitigation: Optional[str] = None


@dataclass
class EffortEstimate:
    """Effort estimation for implementation.

    Attributes:
        duration: Human-readable duration (e.g., "4 hours")
        lines_of_code: Estimated LOC to write
        complexity_score: 1-10 complexity score
    """
    duration: str
    lines_of_code: int
    complexity_score: int


@dataclass
class PlanSummary:
    """Complete implementation plan summary for checkpoint display.

    Attributes:
        task_id: Task identifier
        files_to_change: List of files to create/modify
        dependencies: External dependencies required
        risks: Implementation risks
        effort: Effort estimate
        test_summary: Testing approach summary
        phases: Implementation phases
    """
    task_id: str
    files_to_change: List[FileChange] = field(default_factory=list)
    dependencies: List[Dependency] = field(default_factory=list)
    risks: List[Risk] = field(default_factory=list)
    effort: Optional[EffortEstimate] = None
    test_summary: Optional[str] = None
    phases: List[str] = field(default_factory=list)

    @property
    def has_high_risks(self) -> bool:
        """Check if any HIGH severity risks exist."""
        return any(risk.level == RiskLevel.HIGH for risk in self.risks)

    @property
    def total_files(self) -> int:
        """Total number of files to change."""
        return len(self.files_to_change)


def _parse_risk_level(level_str: str) -> RiskLevel:
    """Parse risk level from string with fallback to MEDIUM."""
    return RiskLevel.from_string(level_str)


def load_plan_summary(task_id: str, plan_path: Optional[Path] = None) -> Optional[PlanSummary]:
    """
    Load implementation plan and convert to PlanSummary for display.

    Loads saved implementation plan from markdown or JSON format and converts
    to structured PlanSummary dataclass for checkpoint display.

    Args:
        task_id: Task identifier (e.g., "TASK-028")
        plan_path: Optional explicit path to plan file (defaults to standard location)

    Returns:
        PlanSummary if plan exists and loads successfully, None otherwise

    Raises:
        PlanPersistenceError: If plan exists but loading fails

    Example:
        >>> summary = load_plan_summary("TASK-028")
        >>> if summary:
        ...     print(f"Files: {summary.total_files}")
        ...     print(f"Risks: {len(summary.risks)}")
        Files: 4
        Risks: 2
    """
    try:
        # Check if plan exists
        if plan_path is None and not plan_exists(task_id):
            logger.info(f"No implementation plan found for {task_id}")
            return None

        # Load plan data
        plan_data = load_plan(task_id) if plan_path is None else _load_from_path(plan_path)
        if plan_data is None:
            return None

        # Check if plan was marked as empty during save
        if plan_data.get("empty_plan", False):
            logger.warning(f"Plan for {task_id} was saved as empty - invalid plan")
            return None

        # Extract plan section (unwrap metadata wrapper)
        plan = plan_data.get("plan", {})
        if not plan:
            logger.warning(f"Plan for {task_id} has no 'plan' section")
            return None

        # Note: We don't validate for empty content here because:
        # 1. The empty_plan marker (above) already handles truly empty plans
        # 2. Plans with explicit empty lists are valid (e.g., "no dependencies needed")
        # 3. The application layer can decide how to handle empty summaries

        # Parse files to change
        files_to_change = []
        for file_path in plan.get("files_to_create", []):
            files_to_change.append(FileChange(
                path=file_path,
                description="Create new file",
                change_type="create"
            ))
        for file_path in plan.get("files_to_modify", []):
            files_to_change.append(FileChange(
                path=file_path,
                description="Modify existing file",
                change_type="modify"
            ))

        # Parse dependencies
        dependencies = []
        for dep in plan.get("external_dependencies", []):
            if isinstance(dep, str):
                # Try to parse "name version - purpose" format from markdown
                # Example: "requests 2.28.0 - HTTP client"
                if " - " in dep:
                    # Split by " - " to separate version info from purpose
                    dep_info, purpose = dep.split(" - ", 1)
                    parts = dep_info.split(maxsplit=1)
                    if len(parts) == 2:
                        dependencies.append(Dependency(name=parts[0], version=parts[1], purpose=purpose))
                    else:
                        dependencies.append(Dependency(name=parts[0], purpose=purpose))
                else:
                    # No purpose, try to parse "name version"
                    parts = dep.split(maxsplit=1)
                    if len(parts) == 2:
                        dependencies.append(Dependency(name=parts[0], version=parts[1]))
                    else:
                        dependencies.append(Dependency(name=dep))
            elif isinstance(dep, dict):
                dependencies.append(Dependency(
                    name=dep.get("name", ""),
                    version=dep.get("version"),
                    purpose=dep.get("purpose")
                ))

        # Parse risks
        risks = []
        for risk in plan.get("risks", []):
            if isinstance(risk, str):
                # Simple string risk, default to MEDIUM
                risks.append(Risk(
                    description=risk,
                    level=RiskLevel.MEDIUM
                ))
            elif isinstance(risk, dict):
                risks.append(Risk(
                    description=risk.get("description", ""),
                    level=_parse_risk_level(risk.get("level", "medium")),
                    mitigation=risk.get("mitigation")
                ))

        # Parse effort estimate (only if at least one effort field is present)
        effort = None
        if "estimated_duration" in plan or "estimated_loc" in plan or "complexity_score" in plan:
            # Only create EffortEstimate if we have actual data (not just defaults)
            has_duration = "estimated_duration" in plan and plan["estimated_duration"] not in (None, "None", "Unknown", "Not estimated")
            has_loc = "estimated_loc" in plan and plan["estimated_loc"] not in (None, 0, "N/A")
            has_complexity = "complexity_score" in plan and plan["complexity_score"] not in (None, "N/A")

            if has_duration or has_loc or has_complexity:
                effort = EffortEstimate(
                    duration=plan.get("estimated_duration", "Unknown"),
                    lines_of_code=plan.get("estimated_loc", 0),
                    complexity_score=plan.get("complexity_score", 5)
                )

        # Create summary
        return PlanSummary(
            task_id=task_id,
            files_to_change=files_to_change,
            dependencies=dependencies,
            risks=risks,
            effort=effort,
            test_summary=plan.get("test_summary"),
            phases=plan.get("phases", [])
        )

    except PlanPersistenceError:
        # Re-raise persistence errors
        raise
    except Exception as e:
        # Re-raise unexpected errors for proper handling at display level
        logger.error(f"Failed to load plan summary for {task_id}: {e}")
        raise


def _load_from_path(plan_path: Path) -> Optional[Dict[str, Any]]:
    """Load plan from explicit path (for testing)."""
    import json
    if not plan_path.exists():
        return None

    try:
        # Try JSON first
        if plan_path.suffix == ".json":
            with open(plan_path, 'r') as f:
                return json.load(f)
        # Try markdown
        elif plan_path.suffix == ".md":
            from plan_markdown_parser import PlanMarkdownParser
            parser = PlanMarkdownParser()
            return parser.parse_file(plan_path)
    except Exception as e:
        logger.error(f"Failed to load plan from {plan_path}: {e}")
        return None


def format_plan_summary(summary: PlanSummary, max_files: int = 5, max_deps: int = 3) -> str:
    """
    Format PlanSummary as human-readable text for display.

    Creates formatted output with truncation for long lists, severity icons
    for risks, and clear section headers.

    Args:
        summary: PlanSummary to format
        max_files: Maximum files to show before truncation (default: 5)
        max_deps: Maximum dependencies to show before truncation (default: 3)

    Returns:
        Formatted string ready for display

    Example:
        >>> summary = PlanSummary(task_id="TASK-028", ...)
        >>> print(format_plan_summary(summary))

        IMPLEMENTATION PLAN SUMMARY
        ===========================

        Files to Change (4):
        - src/checkpoint.py (create)
        - tests/test_checkpoint.py (create)
        ...
    """
    lines = []
    lines.append("")
    lines.append("IMPLEMENTATION PLAN SUMMARY")
    lines.append("=" * 40)
    lines.append("")

    # Files section
    if summary.files_to_change:
        truncated_files = summary.files_to_change[:max_files]
        lines.append(f"Files to Change ({summary.total_files}):")
        for file_change in truncated_files:
            action = "create" if file_change.change_type == "create" else "modify"
            lines.append(f"  - {file_change.path} ({action})")

        if summary.total_files > max_files:
            remaining = summary.total_files - max_files
            lines.append(f"  ... and {remaining} more")
        lines.append("")

    # Dependencies section (skip if empty)
    if summary.dependencies:
        truncated_deps = summary.dependencies[:max_deps]
        lines.append(f"Dependencies ({len(summary.dependencies)}):")
        for dep in truncated_deps:
            version_str = f" ({dep.version})" if dep.version else ""
            lines.append(f"  - {dep.name}{version_str}")

        if len(summary.dependencies) > max_deps:
            remaining = len(summary.dependencies) - max_deps
            lines.append(f"  ... and {remaining} more")
        lines.append("")

    # Risks section (skip if empty)
    if summary.risks:
        lines.append(f"Risks ({len(summary.risks)}):")
        for risk in summary.risks:
            lines.append(f"  {risk.level.icon} {risk.level.value.upper()}: {risk.description}")
            if risk.mitigation:
                lines.append(f"    Mitigation: {risk.mitigation}")
        lines.append("")

    # Effort estimate section (skip if empty)
    if summary.effort:
        lines.append("Effort Estimate:")
        lines.append(f"  Duration: {summary.effort.duration}")
        lines.append(f"  Lines of Code: ~{summary.effort.lines_of_code}")
        lines.append(f"  Complexity: {summary.effort.complexity_score}/10")
        lines.append("")

    # Test summary section (skip if empty)
    if summary.test_summary:
        lines.append("Testing Approach:")
        lines.append(f"  {summary.test_summary}")
        lines.append("")

    return "\n".join(lines)


def _get_review_mode(complexity_score: int) -> str:
    """Determine review mode from complexity score.

    Args:
        complexity_score: 1-10 complexity score

    Returns:
        Review mode string: "AUTO_PROCEED", "QUICK_OPTIONAL", or "FULL_REQUIRED"
    """
    if complexity_score <= 3:
        return "AUTO_PROCEED"
    elif complexity_score <= 6:
        return "QUICK_OPTIONAL"
    else:
        return "FULL_REQUIRED"


def display_phase28_checkpoint(
    task_id: str,
    complexity_score: int,
    plan_path: Optional[Path] = None
) -> None:
    """
    Display Phase 2.8 checkpoint with implementation plan summary.

    Main entry point for checkpoint display. Loads plan summary and displays
    formatted output. Handles missing plans gracefully with appropriate warnings.

    Args:
        task_id: Task identifier
        complexity_score: 1-10 complexity score
        plan_path: Optional explicit path to plan file

    Example:
        >>> display_phase28_checkpoint("TASK-028", 7)

        PHASE 2.8: IMPLEMENTATION PLAN CHECKPOINT
        =========================================

        Task: TASK-028
        Complexity: 7/10 (Complex - requires full review)

        IMPLEMENTATION PLAN SUMMARY
        ...
    """
    print("\n" + "=" * 60)
    print("PHASE 2.8: IMPLEMENTATION PLAN CHECKPOINT")
    print("=" * 60)
    print()
    print(f"Task: {task_id}")

    # Display complexity and review mode
    review_mode = _get_review_mode(complexity_score)
    mode_description = {
        "AUTO_PROCEED": "Simple - auto-proceed",
        "QUICK_OPTIONAL": "Medium - quick review",
        "FULL_REQUIRED": "Complex - requires full review"
    }[review_mode]
    print(f"Complexity: {complexity_score}/10 ({mode_description})")
    print()

    # Load and display plan summary
    try:
        summary = load_plan_summary(task_id, plan_path)

        if summary:
            formatted = format_plan_summary(summary)
            print(formatted)

            # Display plan file location
            if plan_path:
                print(f"Plan file: {plan_path}")
            else:
                print(f"Plan file: docs/state/{task_id}/implementation_plan.md")
            print(f"View with: cat docs/state/{task_id}/implementation_plan.md")
            print()
        else:
            print("⚠️  No implementation plan found")
            if complexity_score >= 7:
                print("WARNING: Complex task without saved plan - consider running with --design-only first")
            print()

    except PlanPersistenceError as e:
        logger.error(f"Failed to load plan: {e}")
        print(f"⚠️  Error loading implementation plan: {e}")
        print()
    except Exception as e:
        logger.error(f"Unexpected error in checkpoint display: {e}")
        print(f"⚠️  Unexpected error: {e}")
        print()

    # Display checkpoint instructions
    print("=" * 60)
    print("CHECKPOINT: Review implementation plan")
    print("=" * 60)
    print()
    print("Options:")
    print("  [A]pprove  - Proceed with implementation")
    print("  [M]odify   - Adjust plan before implementation")
    print("  [C]ancel   - Stop task execution")
    print()


def handle_modify_option(task_id: str) -> bool:
    """
    Handle the [M]odify option from Phase 2.8 checkpoint.

    Launches interactive plan modification workflow, allowing users to
    modify files, dependencies, risks, and effort estimates before
    proceeding with implementation.

    Args:
        task_id: Task identifier

    Returns:
        True if plan was successfully modified and should proceed to implementation,
        False if modification was cancelled or failed

    Example:
        >>> if handle_modify_option("TASK-029"):
        ...     print("Plan modified, proceeding with implementation")
        ... else:
        ...     print("Modification cancelled")

        Plan Modification Session for TASK-029
        ========================================

        Current Modifications: 0

        What would you like to modify?
        1. Files (add/remove)
        2. Dependencies
        3. Risks
        4. Effort Estimate
        5. Undo Last Change
        6. Save and Exit
        7. Cancel (discard changes)

        Choice:
    """
    try:
        print("\n" + "=" * 60)
        print("PLAN MODIFICATION")
        print("=" * 60)
        print()
        print("You can now modify the implementation plan before proceeding.")
        print("Changes will be saved with version tracking.")
        print()

        # Launch plan modifier
        modifier = PlanModifier(task_id)
        updated_plan = modifier.run_interactive_session()

        if updated_plan:
            print("\n" + "=" * 60)
            print("PLAN MODIFICATION COMPLETE")
            print("=" * 60)
            print()
            print("✓ Implementation plan has been updated")
            print("✓ Previous version backed up to versions/ directory")
            print()
            print("Returning to checkpoint menu...")
            return True
        else:
            print("\n" + "=" * 60)
            print("MODIFICATION CANCELLED")
            print("=" * 60)
            print()
            print("Original plan unchanged.")
            print("Returning to checkpoint menu...")
            return False

    except PlanModificationError as e:
        logger.error(f"Plan modification failed: {e}")
        print(f"\n❌ Plan modification failed: {e}")
        print("Returning to checkpoint menu...")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during plan modification: {e}")
        print(f"\n❌ Unexpected error: {e}")
        print("Returning to checkpoint menu...")
        return False


# Module exports
__all__ = [
    "RiskLevel",
    "FileChange",
    "Dependency",
    "Risk",
    "EffortEstimate",
    "PlanSummary",
    "load_plan_summary",
    "format_plan_summary",
    "display_phase28_checkpoint",
    "handle_modify_option"
]
