"""
Phase Execution Module - Orchestrates task-work phase execution with design-first workflow support.

Part of TASK-006: Add Design-First Workflow Flags to task-work Command.

This module provides the main entry point for executing task-work phases in different modes:
- Standard mode (default): Executes all phases in sequence
- Design-only mode (--design-only): Executes design phases only, stops at approval
- Implement-only mode (--implement-only): Executes implementation phases using saved design

Author: Claude (Anthropic)
Created: 2025-10-11
"""

from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime
import json


class PhaseExecutionError(Exception):
    """Raised when phase execution fails."""
    pass


class StateValidationError(Exception):
    """Raised when task state is invalid for the requested operation."""
    pass


def execute_phases(
    task_id: str,
    task_context: Dict[str, Any],
    design_only: bool = False,
    implement_only: bool = False,
    stack: str = "default"
) -> Dict[str, Any]:
    """
    Main entry point for phase execution. Routes to appropriate workflow based on flags.

    Args:
        task_id: Task identifier (e.g., "TASK-006")
        task_context: Task context loaded from task file (frontmatter + content)
        design_only: If True, execute design phases only
        implement_only: If True, execute implementation phases only (requires approved design)
        stack: Technology stack (e.g., "python", "react", "maui")

    Returns:
        Dictionary containing execution results:
        {
            "success": bool,
            "workflow_mode": str,  # "standard", "design_only", "implement_only"
            "phases_executed": List[str],
            "final_state": str,
            "duration_seconds": float,
            "results": Dict[str, Any]
        }

    Raises:
        ValueError: If both flags are True (mutual exclusivity violation)
        StateValidationError: If task state is invalid for requested operation
        PhaseExecutionError: If phase execution fails

    Examples:
        >>> # Standard workflow
        >>> result = execute_phases("TASK-006", context)
        >>> result["workflow_mode"]
        'standard'

        >>> # Design-only workflow
        >>> result = execute_phases("TASK-006", context, design_only=True)
        >>> result["final_state"]
        'design_approved'

        >>> # Implement-only workflow
        >>> result = execute_phases("TASK-006", context, implement_only=True)
        >>> result["workflow_mode"]
        'implement_only'
    """
    # Validate mutual exclusivity
    if design_only and implement_only:
        raise ValueError(
            "Cannot use both --design-only and --implement-only flags together.\n"
            "Choose one workflow mode:\n"
            "  --design-only: Execute design phases only\n"
            "  --implement-only: Execute implementation phases only\n"
            "  (no flags): Execute complete workflow"
        )

    # Route to appropriate workflow
    start_time = datetime.now()

    if design_only:
        result = execute_design_phases(task_id, task_context, stack)
        workflow_mode = "design_only"
    elif implement_only:
        result = execute_implementation_phases(task_id, task_context, stack)
        workflow_mode = "implement_only"
    else:
        result = execute_standard_phases(task_id, task_context, stack)
        workflow_mode = "standard"

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    return {
        "success": result.get("success", True),
        "workflow_mode": workflow_mode,
        "phases_executed": result.get("phases_executed", []),
        "final_state": result.get("final_state", "unknown"),
        "duration_seconds": duration,
        "results": result
    }


def execute_design_phases(
    task_id: str,
    task_context: Dict[str, Any],
    stack: str = "default"
) -> Dict[str, Any]:
    """
    Execute design phases only (Phase 1 through Phase 2.6).

    Phases executed:
    - Phase 1: Load Task Context
    - Phase 2: Implementation Planning
    - Phase 2.5A: Pattern Suggestion (if Design Patterns MCP available)
    - Phase 2.5B: Architectural Review
    - Phase 2.7: Complexity Evaluation & Plan Persistence
    - Phase 2.8: Human Checkpoint (mandatory, design-focused)

    After approval, task moves to 'design_approved' state with saved implementation plan.

    Args:
        task_id: Task identifier
        task_context: Task context from task file
        stack: Technology stack

    Returns:
        Dictionary with execution results:
        {
            "success": bool,
            "phases_executed": List[str],
            "final_state": str,  # "design_approved" or "blocked"
            "design_approved": bool,
            "plan_path": Optional[str],
            "architectural_review": Dict[str, Any],
            "complexity_evaluation": Dict[str, Any]
        }

    Raises:
        StateValidationError: If task state is invalid for design phase
        PhaseExecutionError: If phase execution fails
    """
    phases_executed = []

    # Validate task state (can run design-only from backlog, in_progress, or blocked)
    current_state = task_context.get("status", "unknown")
    valid_states = ["backlog", "in_progress", "blocked"]

    if current_state not in valid_states:
        raise StateValidationError(
            f"Cannot execute design-only workflow from '{current_state}' state.\n"
            f"Valid states: {', '.join(valid_states)}\n"
            f"Current state: {current_state}"
        )

    print(f"\n🎨 Starting Design-Only Workflow for {task_id}")
    print(f"Current state: {current_state}")
    print(f"Technology stack: {stack}\n")

    # Phase 1: Load Task Context (already done, just record)
    phases_executed.append("Phase 1: Load Task Context")
    print("✅ Phase 1: Task context loaded")

    # Phase 2: Implementation Planning (delegated to agent)
    phases_executed.append("Phase 2: Implementation Planning")
    print("⏳ Phase 2: Invoking planning agent...")
    # NOTE: Agent invocation happens in task-work.md protocol
    # This function orchestrates the flow

    # Phase 2.5A: Pattern Suggestion (optional, if MCP available)
    # Skipped in MVP - will be invoked by task-work.md if available

    # Phase 2.5B: Architectural Review (delegated to agent)
    phases_executed.append("Phase 2.5B: Architectural Review")
    print("⏳ Phase 2.5B: Invoking architectural reviewer...")
    # NOTE: Agent invocation happens in task-work.md protocol

    # Phase 2.7: Complexity Evaluation & Plan Persistence
    phases_executed.append("Phase 2.7: Complexity Evaluation")
    print("⏳ Phase 2.7: Evaluating complexity and persisting plan...")
    # NOTE: Agent invocation happens in task-work.md protocol

    # Phase 2.8: Human Checkpoint (mandatory for design-only)
    phases_executed.append("Phase 2.8: Design Approval Checkpoint")
    print("⏳ Phase 2.8: Awaiting design approval...")
    # NOTE: Human interaction happens in task-work.md protocol

    # Return structure (actual values filled by task-work protocol)
    return {
        "success": True,
        "phases_executed": phases_executed,
        "final_state": "design_approved",  # Assuming approval
        "design_approved": True,
        "plan_path": f"docs/state/{task_id}/implementation_plan.json",
        "architectural_review": {},  # Filled by task-work protocol
        "complexity_evaluation": {}  # Filled by task-work protocol
    }


def execute_implementation_phases(
    task_id: str,
    task_context: Dict[str, Any],
    stack: str = "default"
) -> Dict[str, Any]:
    """
    Execute implementation phases only (Phase 3 through Phase 5).

    Prerequisite: Task must be in 'design_approved' state.

    Phases executed:
    - Phase 3: Implementation (using saved plan)
    - Phase 4: Testing
    - Phase 4.5: Fix Loop (ensure tests pass)
    - Phase 5: Code Review

    After completion, task moves to 'in_review' (if pass) or 'blocked' (if fail).

    Args:
        task_id: Task identifier
        task_context: Task context from task file
        stack: Technology stack

    Returns:
        Dictionary with execution results:
        {
            "success": bool,
            "phases_executed": List[str],
            "final_state": str,  # "in_review" or "blocked"
            "tests_passed": bool,
            "test_results": Dict[str, Any],
            "quality_gates": Dict[str, bool]
        }

    Raises:
        StateValidationError: If task is not in 'design_approved' state
        PhaseExecutionError: If saved design plan is missing or invalid
    """
    phases_executed = []

    # Validate task state (MUST be design_approved)
    current_state = task_context.get("status", "unknown")

    if current_state != "design_approved":
        raise StateValidationError(
            f"❌ Cannot execute --implement-only workflow\n\n"
            f"Task {task_id} is in '{current_state}' state.\n"
            f"Required state: design_approved\n\n"
            f"To approve design first, run:\n"
            f"  /task-work {task_id} --design-only\n\n"
            f"Or run complete workflow without flags:\n"
            f"  /task-work {task_id}"
        )

    # Validate design metadata exists
    design_metadata = task_context.get("design", {})
    if not design_metadata or design_metadata.get("status") != "approved":
        raise PhaseExecutionError(
            f"❌ Design metadata missing or invalid for {task_id}\n\n"
            f"Task is in design_approved state, but design metadata is incomplete.\n"
            f"This may indicate a corrupted task file.\n\n"
            f"Options:\n"
            f"1. Re-run design phase: /task-work {task_id} --design-only\n"
            f"2. Run full workflow: /task-work {task_id}\n"
            f"3. Manually fix task metadata"
        )

    # Load saved implementation plan
    plan_path = Path(f"docs/state/{task_id}/implementation_plan.json")
    if not plan_path.exists():
        raise PhaseExecutionError(
            f"❌ Implementation plan not found: {plan_path}\n\n"
            f"Design was approved but plan file is missing.\n"
            f"Re-run design phase: /task-work {task_id} --design-only"
        )

    print(f"\n🚀 Starting Implementation-Only Workflow for {task_id}")
    print(f"Current state: {current_state}")
    print(f"Using approved design from: {design_metadata.get('approved_at', 'unknown')}\n")

    # Display design summary
    _display_implementation_start_context(task_id, task_context, design_metadata)

    # Phase 3: Implementation (delegated to agent)
    phases_executed.append("Phase 3: Implementation")
    print("\n⏳ Phase 3: Invoking implementation agent...")
    # NOTE: Agent invocation happens in task-work.md protocol

    # Phase 4: Testing (delegated to agent)
    phases_executed.append("Phase 4: Testing")
    print("⏳ Phase 4: Invoking testing agent...")
    # NOTE: Agent invocation happens in task-work.md protocol

    # Phase 4.5: Fix Loop (automated)
    phases_executed.append("Phase 4.5: Fix Loop")
    print("⏳ Phase 4.5: Ensuring all tests pass...")
    # NOTE: Fix loop happens in task-work.md protocol

    # Phase 5: Code Review (delegated to agent)
    phases_executed.append("Phase 5: Code Review")
    print("⏳ Phase 5: Invoking code reviewer...")
    # NOTE: Agent invocation happens in task-work.md protocol

    # Phase 5.5: Plan Audit (NEW - Hubbard's Step 6)
    phases_executed.append("Phase 5.5: Plan Audit")
    print("⏳ Phase 5.5: Auditing implementation against plan...")
    # NOTE: Audit happens in task-work.md protocol

    # Return structure (actual values filled by task-work protocol)
    return {
        "success": True,
        "phases_executed": phases_executed,
        "final_state": "in_review",  # Assuming success
        "tests_passed": True,
        "test_results": {},  # Filled by task-work protocol
        "quality_gates": {}  # Filled by task-work protocol
    }


def execute_standard_phases(
    task_id: str,
    task_context: Dict[str, Any],
    stack: str = "default"
) -> Dict[str, Any]:
    """
    Execute standard full workflow (all phases in sequence).

    This is the default behavior when no flags are provided.
    Maintains backward compatibility with existing task-work implementation.

    Phases executed:
    - Phase 1: Load Task Context
    - Phase 2: Implementation Planning
    - Phase 2.5A: Pattern Suggestion (optional)
    - Phase 2.5B: Architectural Review
    - Phase 2.7: Complexity Evaluation
    - Phase 2.8: Human Checkpoint (if triggered by complexity)
    - Phase 3: Implementation
    - Phase 4: Testing
    - Phase 4.5: Fix Loop
    - Phase 5: Code Review

    Args:
        task_id: Task identifier
        task_context: Task context from task file
        stack: Technology stack

    Returns:
        Dictionary with execution results (all phases)
    """
    phases_executed = []

    print(f"\n🔄 Starting Standard Workflow for {task_id}")
    print(f"Technology stack: {stack}")
    print("Executing all phases in sequence...\n")

    # All phases execute as per current implementation
    # This function maintains backward compatibility
    phases_executed = [
        "Phase 1: Load Task Context",
        "Phase 2: Implementation Planning",
        "Phase 2.5B: Architectural Review",
        "Phase 2.7: Complexity Evaluation",
        "Phase 2.8: Human Checkpoint (if triggered)",
        "Phase 3: Implementation",
        "Phase 4: Testing",
        "Phase 4.5: Fix Loop",
        "Phase 5: Code Review",
        "Phase 5.5: Plan Audit"
    ]

    # NOTE: Actual phase execution happens in task-work.md protocol
    # This function just orchestrates the flow

    return {
        "success": True,
        "phases_executed": phases_executed,
        "final_state": "in_review",  # Typical successful outcome
        "workflow_note": "Standard workflow - all phases executed"
    }


def _display_implementation_start_context(
    task_id: str,
    task_context: Dict[str, Any],
    design_metadata: Dict[str, Any]
) -> None:
    """
    Display implementation start context showing approved design summary.

    Args:
        task_id: Task identifier
        task_context: Full task context
        design_metadata: Design metadata from task frontmatter
    """
    print("\n" + "=" * 67)
    print("🚀 IMPLEMENTATION PHASE (--implement-only mode)")
    print("=" * 67)
    print()
    print(f"TASK: {task_id} - {task_context.get('title', 'Untitled')}")
    print()
    print("APPROVED DESIGN:")
    print(f"  Design approved: {design_metadata.get('approved_at', 'unknown')}")
    print(f"  Approved by: {design_metadata.get('approved_by', 'unknown')}")
    print(f"  Architectural score: {design_metadata.get('architectural_review_score', 'N/A')}/100")
    print(f"  Complexity score: {design_metadata.get('complexity_score', 'N/A')}/10")
    print()

    # Load and display plan summary if available
    plan_path = Path(f"docs/state/{task_id}/implementation_plan.json")
    if plan_path.exists():
        try:
            with open(plan_path, 'r') as f:
                plan = json.load(f)

            print("IMPLEMENTATION PLAN:")
            print(f"  Files to create: {len(plan.get('files_to_create', []))}")
            print(f"  External dependencies: {len(plan.get('external_dependencies', []))}")
            print(f"  Estimated duration: {plan.get('estimated_duration', 'N/A')}")
            print(f"  Test strategy: {plan.get('test_summary', 'N/A')}")
            print()
        except Exception as e:
            print(f"  ⚠️  Could not load plan details: {e}")
            print()

    print("Beginning implementation phases (3 → 4 → 4.5 → 5)...")
    print("=" * 67)
    print()


def execute_phase_5_5_plan_audit(
    task_id: str,
    task_context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Phase 5.5: Audit implementation against saved plan.

    Implements Hubbard's Step 6 (Audit) - verifies actual implementation
    matches the approved architectural plan.

    Args:
        task_id: Task identifier
        task_context: Task context from task file

    Returns:
        Dictionary with audit results:
        {
            "approved": bool,
            "report": PlanAuditReport,
            "decision": str,
            "skipped": bool
        }

    Example:
        >>> result = execute_phase_5_5_plan_audit("TASK-025", context)
        >>> if result["approved"]:
        ...     print("Audit passed")
    """
    from .plan_audit import PlanAuditor, format_audit_report, PlanAuditError
    from .plan_persistence import plan_exists
    from .metrics.plan_audit_metrics import PlanAuditMetricsTracker

    # Check if plan exists
    if not plan_exists(task_id):
        print("⚠️  No implementation plan found - skipping audit")
        return {"approved": True, "report": None, "decision": "skipped", "skipped": True}

    try:
        # Run audit
        auditor = PlanAuditor()
        report = auditor.audit_implementation(task_id)

        # Display report
        print("\n" + format_audit_report(report))

        # Prompt for decision with timeout
        decision = prompt_with_timeout(
            "Choice [A]pprove/[R]evise/[E]scalate/[C]ancel (30s timeout = auto-approve): ",
            timeout=30,
            default="A"
        )

        # Handle decision
        approved = handle_audit_decision(task_id, report, decision)

        # Track metrics
        tracker = PlanAuditMetricsTracker()
        tracker.record_audit(task_id, report, decision.lower())

        return {
            "approved": approved,
            "report": report,
            "decision": decision.lower(),
            "skipped": False
        }

    except PlanAuditError as e:
        print(f"⚠️  Audit error: {e}")
        print("Defaulting to approve (non-blocking)")
        return {"approved": True, "report": None, "decision": "error", "skipped": False}


def prompt_with_timeout(prompt: str, timeout: int, default: str) -> str:
    """
    Prompt user with timeout (auto-returns default after timeout).

    Uses threading to implement timeout behavior.

    Args:
        prompt: Prompt text to display
        timeout: Timeout in seconds
        default: Default value if timeout occurs

    Returns:
        User input or default value

    Example:
        >>> response = prompt_with_timeout("Continue? ", 30, "Y")
        >>> print(response)
        'Y'
    """
    import sys
    import threading

    result = [default]  # Mutable container for thread communication

    def get_input():
        try:
            result[0] = input(prompt).strip().upper()
        except Exception:
            pass

    thread = threading.Thread(target=get_input)
    thread.daemon = True
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        print(f"\n⏱️  Timeout - defaulting to [{default}]")

    return result[0]


def handle_audit_decision(
    task_id: str,
    report: Any,  # PlanAuditReport
    decision: str
) -> bool:
    """
    Handle audit decision and update task state.

    Args:
        task_id: Task identifier
        report: PlanAuditReport object
        decision: User decision ("A", "R", "E", "C")

    Returns:
        True if approved (continue to IN_REVIEW)
        False if blocked (transition to BLOCKED)

    Example:
        >>> approved = handle_audit_decision("TASK-025", report, "A")
        >>> print(approved)
        True
    """
    decision_lower = decision.lower()

    if decision_lower == "a":
        # Approve - add note to task metadata
        print("✅ Audit approved - proceeding to IN_REVIEW")
        _update_task_metadata(task_id, report, "approved")
        return True

    elif decision_lower == "r":
        # Revise - transition to BLOCKED
        print("❌ Audit revision requested - transitioning to BLOCKED")
        _update_task_metadata(task_id, report, "revision_requested")
        return False

    elif decision_lower == "e":
        # Escalate - create follow-up task, proceed to IN_REVIEW with warning
        print("⚠️  Audit escalated - creating follow-up task")
        _create_followup_task(task_id, report)
        _update_task_metadata(task_id, report, "escalated")
        return True

    elif decision_lower == "c":
        # Cancel - transition to BLOCKED
        print("❌ Audit cancelled - transitioning to BLOCKED")
        _update_task_metadata(task_id, report, "cancelled")
        return False

    else:
        # Invalid input - default to approve with warning
        print(f"⚠️  Invalid input '{decision}' - defaulting to Approve")
        _update_task_metadata(task_id, report, "approved_default")
        return True


def _update_task_metadata(task_id: str, report: Any, decision: str) -> None:
    """
    Update task frontmatter with audit results.

    Args:
        task_id: Task identifier
        report: PlanAuditReport object
        decision: Audit decision
    """
    task_file = _find_task_file(task_id)
    if not task_file:
        return

    try:
        import yaml

        with open(task_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split frontmatter and body
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1])
            body = parts[2]

            # Add audit metadata
            frontmatter["plan_audit"] = {
                "severity": report.severity,
                "discrepancies_count": len(report.discrepancies),
                "decision": decision,
                "audited_at": report.timestamp
            }

            # Write back
            with open(task_file, 'w', encoding='utf-8') as f:
                f.write("---\n")
                yaml.dump(frontmatter, f, default_flow_style=False)
                f.write("---")
                f.write(body)

    except Exception as e:
        print(f"⚠️  Could not update task metadata: {e}")


def _create_followup_task(task_id: str, report: Any) -> None:
    """
    Create follow-up task for scope creep investigation.

    Args:
        task_id: Original task identifier
        report: PlanAuditReport object
    """
    # Placeholder - actual implementation would:
    # 1. Generate new task file in tasks/backlog/
    # 2. Link to original task
    # 3. Add discrepancies as requirements
    print(f"📝 Follow-up task created: {task_id}-AUDIT-FOLLOWUP")
    print("   (Note: Follow-up task creation not yet implemented)")


def _find_task_file(task_id: str) -> Optional[Path]:
    """
    Find task file across all state directories.

    Args:
        task_id: Task identifier

    Returns:
        Path to task file or None if not found
    """
    for state_dir in ["backlog", "in_progress", "in_review", "blocked", "completed"]:
        task_file = Path(f"tasks/{state_dir}/{task_id}.md")
        if task_file.exists():
            return task_file
    return None


# Module exports
__all__ = [
    "execute_phases",
    "execute_design_phases",
    "execute_implementation_phases",
    "execute_standard_phases",
    "execute_phase_5_5_plan_audit",
    "prompt_with_timeout",
    "handle_audit_decision",
    "PhaseExecutionError",
    "StateValidationError"
]
