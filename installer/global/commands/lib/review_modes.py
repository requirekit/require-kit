"""
Quick Review Mode implementation for architectural review workflow.

This module implements the Quick Review Mode (10-second countdown with summary card)
as part of the architectural review system. It coordinates display rendering,
user interaction, and outcome handling.

Architecture:
    - QuickReviewResult: Dataclass for review outcomes
    - QuickReviewDisplay: Terminal UI rendering for summary cards
    - QuickReviewHandler: Main coordinator for quick review workflow

Example:
    >>> from review_modes import QuickReviewHandler
    >>> from complexity_models import ImplementationPlan
    >>>
    >>> handler = QuickReviewHandler(task_id="TASK-001", plan=plan)
    >>> result = handler.execute()
    >>>
    >>> if result.action == "timeout":
    ...     print(f"Auto-approved at {result.timestamp}")
    >>> elif result.action == "enter":
    ...     # Escalate to full review
    ...     pass
"""

import json
import os
import re
import yaml
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Literal, Optional, TYPE_CHECKING

try:
    from .complexity_models import ImplementationPlan, ReviewDecision, ReviewMode
    from .user_interaction import countdown_timer, CountdownResult
except ImportError:
    from complexity_models import ImplementationPlan, ReviewDecision, ReviewMode
    from user_interaction import countdown_timer, CountdownResult

# Import types only for type checking to avoid circular imports
if TYPE_CHECKING:
    from .modification_session import ModificationSession


ReviewAction = Literal["timeout", "enter", "cancel"]


@dataclass
class QuickReviewResult:
    """
    Result of a quick review session.

    Captures the user's decision and any metadata updates required
    for task state management.

    Attributes:
        action: User's choice ("timeout" = auto-proceed, "enter" = escalate, "cancel" = cancel)
        timestamp: ISO 8601 timestamp of the review completion
        auto_approved: Whether review was auto-approved (timeout)
        metadata_updates: Dictionary of updates to apply to task metadata

    Example:
        >>> result = QuickReviewResult(
        ...     action="timeout",
        ...     timestamp="2025-10-09T10:30:00Z",
        ...     auto_approved=True,
        ...     metadata_updates={"review_mode": "quick", "auto_approved": True}
        ... )
    """
    action: ReviewAction
    timestamp: str
    auto_approved: bool
    metadata_updates: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert result to dictionary for serialization.

        Returns:
            Dict[str, Any]: JSON-serializable dictionary
        """
        return {
            "action": self.action,
            "timestamp": self.timestamp,
            "auto_approved": self.auto_approved,
            "metadata_updates": self.metadata_updates,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QuickReviewResult":
        """
        Create result from dictionary.

        Args:
            data: Dictionary with result fields

        Returns:
            QuickReviewResult: Reconstructed result object
        """
        return cls(
            action=data["action"],
            timestamp=data["timestamp"],
            auto_approved=data["auto_approved"],
            metadata_updates=data.get("metadata_updates", {}),
        )


class QuickReviewDisplay:
    """
    Terminal UI renderer for quick review summary cards.

    Formats and displays architectural review information in a
    visually clear, scannable format for rapid decision-making.

    Example:
        >>> display = QuickReviewDisplay(plan=plan)
        >>> display.render_summary_card()
        # Outputs formatted summary to console
    """

    def __init__(self, plan: ImplementationPlan):
        """
        Initialize display renderer with implementation plan.

        Args:
            plan: ImplementationPlan containing architectural details
        """
        self.plan = plan

    def format_complexity_badge(self) -> str:
        """
        Format complexity score as colored badge.

        Returns color-coded representation based on score thresholds:
            - Green (>=80): Excellent
            - Yellow (60-79): Acceptable
            - Red (<60): Needs revision

        Returns:
            str: Formatted badge string

        Example:
            >>> display.format_complexity_badge()
            "[SCORE: 87/100 - Excellent]"
        """
        # Try to get display_score (0-100), fallback to total_score (1-10) * 10
        if hasattr(self.plan, 'display_score'):
            score = self.plan.display_score
        elif hasattr(self.plan.complexity_score, 'overall_score'):
            score = self.plan.complexity_score.overall_score
        else:
            # Convert 1-10 scale to 0-100
            score = self.plan.complexity_score.total_score * 10

        # Color coding based on score thresholds
        if score >= 80:
            label = "Excellent"
            # Note: Could add ANSI color codes here for terminal colors
        elif score >= 60:
            label = "Acceptable"
        else:
            label = "Needs Revision"

        return f"[SCORE: {score}/100 - {label}]"

    def format_file_summary(self) -> str:
        """
        Format file creation summary.

        Returns:
            str: Human-readable file count summary

        Example:
            >>> display.format_file_summary()
            "3 files (245 lines)"
        """
        num_files = len(self.plan.files_to_create)
        # Use estimated_loc if available, otherwise just show file count
        if hasattr(self.plan, 'estimated_loc') and self.plan.estimated_loc:
            return f"{num_files} files ({self.plan.estimated_loc} lines)"
        else:
            return f"{num_files} files"

    def render_summary_card(self) -> None:
        """
        Render complete summary card to console.

        Displays:
            - Complexity score badge
            - File creation summary
            - Implementation instructions (truncated if long)
            - Key architectural patterns

        Example:
            >>> display = QuickReviewDisplay(plan=plan)
            >>> display.render_summary_card()
            ========================================
            ARCHITECTURAL REVIEW - QUICK MODE
            ========================================
            ...
        """
        print("\n" + "=" * 60)
        print("ARCHITECTURAL REVIEW - QUICK MODE")
        print("=" * 60)

        # Complexity score
        print(f"\nComplexity Score: {self.format_complexity_badge()}")

        # File summary
        print(f"Files to Create: {self.format_file_summary()}")

        # Implementation instructions (truncated)
        # Use implementation_instructions if available, otherwise raw_plan
        instructions = getattr(self.plan, 'implementation_instructions', self.plan.raw_plan)
        # Handle None or empty instructions
        if instructions and len(instructions) > 200:
            instructions = instructions[:197] + "..."
        if instructions:
            print(f"\nInstructions: {instructions}")

        # Key patterns (first 3)
        # Check both metadata and attribute for patterns_detected
        patterns = []
        if hasattr(self.plan.complexity_score, 'patterns_detected'):
            patterns = self.plan.complexity_score.patterns_detected
        elif 'patterns_detected' in self.plan.complexity_score.metadata:
            patterns = self.plan.complexity_score.metadata['patterns_detected']

        if patterns:
            print(f"\nKey Patterns: {', '.join(patterns[:3])}")

        # Warnings (if any)
        warnings = []
        if hasattr(self.plan.complexity_score, 'warnings'):
            warnings = self.plan.complexity_score.warnings
        elif 'warnings' in self.plan.complexity_score.metadata:
            warnings = self.plan.complexity_score.metadata['warnings']

        if warnings:
            print(f"\nWarnings: {len(warnings)} issue(s) detected")
            for warning in warnings[:2]:
                print(f"  - {warning}")

        print("\n" + "=" * 60)


class QuickReviewHandler:
    """
    Main coordinator for Quick Review Mode workflow.

    Orchestrates the 10-second countdown, summary display, user interaction,
    and outcome handling. Implements fail-safe escalation on errors.

    Example:
        >>> handler = QuickReviewHandler(
        ...     task_id="TASK-001",
        ...     plan=implementation_plan
        ... )
        >>> result = handler.execute()
        >>>
        >>> if result.action == "timeout":
        ...     # Auto-proceed to implementation
        ...     pass
        >>> elif result.action == "enter":
        ...     # Escalate to full review
        ...     full_review_handler.execute()
    """

    def __init__(
        self,
        task_id: str,
        plan: ImplementationPlan,
        countdown_duration: int = 10
    ):
        """
        Initialize quick review handler.

        Args:
            task_id: Task identifier (e.g., "TASK-001")
            plan: ImplementationPlan with architectural details
            countdown_duration: Countdown length in seconds (default 10)
        """
        self.task_id = task_id
        self.plan = plan
        self.countdown_duration = countdown_duration
        self.display = QuickReviewDisplay(plan)

    def execute(self) -> QuickReviewResult:
        """
        Execute quick review workflow.

        Workflow:
            1. Display summary card
            2. Start 10-second countdown
            3. Handle user input (timeout/enter/cancel)
            4. Return result with metadata

        Returns:
            QuickReviewResult: Review outcome with metadata

        Raises:
            KeyboardInterrupt: On Ctrl+C (emergency exit)

        Example:
            >>> result = handler.execute()
            >>> print(f"Action: {result.action}")
            >>> print(f"Auto-approved: {result.auto_approved}")
        """
        try:
            # Display summary card
            self.display.render_summary_card()

            # Start countdown with user interaction
            countdown_result = countdown_timer(
                duration_seconds=self.countdown_duration,
                message="Quick review mode active.",
                options="Press [Enter] to see full review, [C] to cancel, or wait to auto-proceed"
            )

            # Handle countdown result
            if countdown_result == "timeout":
                return self.handle_timeout()
            elif countdown_result == "enter":
                return self.handle_escalation()
            elif countdown_result == "cancel":
                return self.handle_cancellation()
            else:
                # Should never reach here, but fail-safe to escalation
                return self.handle_escalation()

        except KeyboardInterrupt:
            # Emergency exit - re-raise for upstream handling
            raise

        except Exception as e:
            # Fail-safe: Escalate to full review on any errors
            print(f"\nError during quick review: {e}")
            print("Escalating to full review for safety...\n")
            return self.handle_escalation()

    def handle_timeout(self) -> QuickReviewResult:
        """
        Handle timeout (auto-proceed) outcome.

        Creates result indicating auto-approval and sets metadata
        for task tracking.

        Returns:
            QuickReviewResult: Result with auto-approval metadata

        Example:
            >>> result = handler.handle_timeout()
            >>> assert result.auto_approved == True
        """
        timestamp = datetime.utcnow().isoformat() + "Z"

        # Get score for metadata (handle different score formats)
        if hasattr(self.plan, 'display_score'):
            score = self.plan.display_score
        elif hasattr(self.plan.complexity_score, 'overall_score'):
            score = self.plan.complexity_score.overall_score
        else:
            score = self.plan.complexity_score.total_score * 10

        metadata = {
            "review_mode": "quick_review",
            "review_action": "auto_approved",
            "review_timestamp": timestamp,
            "complexity_score": score,
            "auto_approved": True,
        }

        return QuickReviewResult(
            action="timeout",
            timestamp=timestamp,
            auto_approved=True,
            metadata_updates=metadata,
        )

    def handle_escalation(self) -> QuickReviewResult:
        """
        Handle escalation to full review.

        Creates result indicating user requested full review.
        Caller is responsible for invoking full review workflow.

        Returns:
            QuickReviewResult: Result indicating escalation needed

        Example:
            >>> result = handler.handle_escalation()
            >>> if result.action == "enter":
            ...     # Invoke full review handler
            ...     full_review_handler.execute()
        """
        timestamp = datetime.utcnow().isoformat() + "Z"

        metadata = {
            "review_mode": "quick_review",
            "review_action": "escalated_to_full",
            "escalation_timestamp": timestamp,
            "auto_approved": False,
        }

        return QuickReviewResult(
            action="enter",
            timestamp=timestamp,
            auto_approved=False,
            metadata_updates=metadata,
        )

    def handle_cancellation(self) -> QuickReviewResult:
        """
        Handle task cancellation.

        Creates result indicating user cancelled the task.
        Caller should abort task execution.

        Returns:
            QuickReviewResult: Result indicating cancellation

        Example:
            >>> result = handler.handle_cancellation()
            >>> if result.action == "cancel":
            ...     print("Task aborted by user")
            ...     sys.exit(1)
        """
        timestamp = datetime.utcnow().isoformat() + "Z"

        metadata = {
            "review_mode": "quick_review",
            "review_action": "cancelled",
            "cancellation_timestamp": timestamp,
            "auto_approved": False,
        }

        return QuickReviewResult(
            action="cancel",
            timestamp=timestamp,
            auto_approved=False,
            metadata_updates=metadata,
        )

    def save_result(self, result: QuickReviewResult, output_path: Optional[Path] = None) -> None:
        """
        Save review result to JSON file.

        Useful for audit trails and debugging. Default location is
        task directory with name {task_id}_review_result.json.

        Args:
            result: QuickReviewResult to save
            output_path: Optional custom output path

        Example:
            >>> handler.save_result(result)
            # Saves to tasks/in_progress/TASK-001_review_result.json
        """
        if output_path is None:
            # Default to task directory
            task_dir = Path(f"tasks/in_progress")
            task_dir.mkdir(parents=True, exist_ok=True)
            output_path = task_dir / f"{self.task_id}_review_result.json"

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, indent=2)


class FullReviewDisplay:
    """
    Terminal UI renderer for full review comprehensive checkpoints.

    Formats and displays complete architectural review information including
    complexity breakdown, changes summary, risk assessment, and implementation
    phases for comprehensive decision-making.

    Example:
        >>> display = FullReviewDisplay(
        ...     complexity_score=score,
        ...     plan=plan,
        ...     task_metadata=metadata
        ... )
        >>> display.render_full_checkpoint()
        # Outputs comprehensive review display to console
    """

    def __init__(
        self,
        complexity_score: "ComplexityScore",
        plan: ImplementationPlan,
        task_metadata: Dict[str, Any],
        escalated: bool = False
    ):
        """
        Initialize full review display renderer.

        Args:
            complexity_score: ComplexityScore with evaluation results
            plan: ImplementationPlan with architectural details
            task_metadata: Task metadata (id, title, etc.)
            escalated: Whether this is an escalated review
        """
        self.complexity_score = complexity_score
        self.plan = plan
        self.task_metadata = task_metadata
        self.escalated = escalated

    def render_full_checkpoint(self) -> None:
        """
        Render complete comprehensive checkpoint display.

        Displays:
            - Header section with task info and complexity score
            - Complexity factors breakdown
            - Changes summary with files and dependencies
            - Risk assessment with mitigations
            - Implementation order and phases
            - Decision prompt with options

        Example:
            >>> display.render_full_checkpoint()
            ======================================================================
            IMPLEMENTATION PLAN REVIEW
            ======================================================================
            ...
        """
        # Get terminal width, default to 80
        try:
            import os
            width = os.get_terminal_size().columns
            width = max(70, min(width, 120))  # Clamp between 70-120
        except Exception:
            width = 80

        separator = "=" * width

        print(f"\n{separator}")
        print("IMPLEMENTATION PLAN REVIEW")
        print(separator)

        # Render all sections
        self._display_header()
        self._display_complexity_breakdown()
        self._display_changes_summary()
        self._display_risk_assessment()
        self._display_implementation_order()

        print(f"\n{separator}")
        self._display_decision_options()

    def _display_header(self) -> None:
        """
        Display header section with task info and complexity score.

        Shows:
            - Task ID and title
            - Complexity score with colored indicator
            - Review mode (escalated or full required)
            - Estimated implementation duration
        """
        score = self.complexity_score.total_score
        indicator = "🔴" if score >= 7 else "🟡" if score >= 4 else "🟢"

        task_id = self.task_metadata.get("id", "UNKNOWN")
        task_title = self.task_metadata.get("title", "No title")

        print(f"\nTask: {task_id} - {task_title}")
        print(f"Complexity: {indicator} {score}/10")

        if self.escalated:
            print("⬆️ Escalated from quick review")

        # Use estimated_duration from plan if available
        duration = self.plan.estimated_duration or "Not estimated"
        print(f"Estimated Time: ~{duration}")

    def _display_complexity_breakdown(self) -> None:
        """
        Display complexity factors breakdown section.

        Shows:
            - Each factor with score and justification
            - Visual severity indicators
            - Force-review triggers if any
        """
        print("\n📊 COMPLEXITY BREAKDOWN:")

        for factor_score in self.complexity_score.factor_scores:
            max_score = factor_score.max_score
            score_val = factor_score.score

            # Determine severity indicator
            if max_score > 0:
                score_ratio = score_val / max_score
                if score_ratio >= 0.9:
                    severity = "🔴"
                elif score_ratio >= 0.5:
                    severity = "🟡"
                else:
                    severity = "🟢"
            else:
                severity = "🟢"

            print(f"\n  {severity} {factor_score.factor_name}: {score_val}/{max_score} points")
            print(f"     → {factor_score.justification}")

        # Display force-review triggers
        if self.complexity_score.forced_review_triggers:
            print("\n  ⚡ FORCE-REVIEW TRIGGERS:")
            for trigger in self.complexity_score.forced_review_triggers:
                trigger_name = trigger.name.replace("_", " ").title()
                print(f"     - {trigger_name}")

    def _display_changes_summary(self) -> None:
        """
        Display changes summary section.

        Shows:
            - Files to create/modify with purposes
            - New dependencies
            - Test strategy summary
        """
        print("\n📁 CHANGES SUMMARY:")

        # Files to create
        files_count = len(self.plan.files_to_create)
        print(f"\n  Files to Create/Modify: {files_count}")
        for file_path in self.plan.files_to_create[:10]:  # Limit to first 10
            print(f"    - {file_path}")
        if files_count > 10:
            print(f"    ... and {files_count - 10} more")

        # External dependencies
        if self.plan.external_dependencies:
            print(f"\n  External Dependencies: {len(self.plan.external_dependencies)}")
            for dep in self.plan.external_dependencies[:5]:
                print(f"    - {dep}")

        # Test strategy summary
        if self.plan.test_summary:
            print(f"\n  Test Strategy:")
            print(f"    {self.plan.test_summary}")

    def _display_risk_assessment(self) -> None:
        """
        Display risk assessment section.

        Shows:
            - Identified risks by severity
            - Mitigation strategies
            - Impact descriptions
        """
        print("\n⚠️ RISK ASSESSMENT:")

        # Use risk_details if available, otherwise fallback to risk_indicators
        if self.plan.risk_details:
            for risk in self.plan.risk_details:
                severity = risk.get("severity", "unknown").lower()
                severity_icon = "🔴" if severity == "high" else \
                               "🟡" if severity == "medium" else "🟢"

                description = risk.get("description", "No description")
                mitigation = risk.get("mitigation", "No mitigation specified")

                print(f"\n  {severity_icon} {severity.upper()}: {description}")
                print(f"     Mitigation: {mitigation}")
        elif self.plan.risk_indicators:
            print("\n  Risk Indicators Detected:")
            for indicator in self.plan.risk_indicators:
                print(f"    - {indicator}")
        else:
            print("\n  No specific risks identified")

    def _display_implementation_order(self) -> None:
        """
        Display implementation order section.

        Shows:
            - Phased implementation steps
            - Time estimates per phase
            - Dependencies between phases
        """
        print("\n📋 IMPLEMENTATION ORDER:")

        # Use phases if available, otherwise show generic message
        if self.plan.phases:
            for i, phase in enumerate(self.plan.phases, 1):
                print(f"\n  {i}. {phase}")
        else:
            print("\n  Implementation phases not detailed in plan")

        # Show estimated LOC if available
        if self.plan.estimated_loc:
            print(f"\n  Estimated Lines of Code: ~{self.plan.estimated_loc}")

    def _display_decision_options(self) -> None:
        """
        Display decision options prompt.

        Shows available actions:
            [A] Approve - Proceed with plan
            [M] Modify - Edit plan
            [V] View - See full details in pager
            [Q] Question - Ask about rationale
            [C] Cancel - Return to backlog
        """
        print("\nDECISION OPTIONS:")
        print("  [A] Approve  - Proceed with this plan as-is")
        print("  [M] Modify   - Interactively edit the plan")
        print("  [V] View     - See full implementation plan in pager")
        print("  [Q] Question - Ask questions about the plan")
        print("  [C] Cancel   - Return task to backlog")
        print()


@dataclass
class FullReviewResult:
    """
    Result of a full review session.

    Captures the user's decision and any metadata updates required
    for task state management in full review mode.

    Attributes:
        action: User's choice ("approve", "cancel", or escalation target)
        timestamp: ISO 8601 timestamp of the review completion
        approved: Whether review was approved for implementation
        metadata_updates: Dictionary of updates to apply to task metadata
        proceed_to_phase_3: Flag indicating whether to proceed to implementation

    Example:
        >>> result = FullReviewResult(
        ...     action="approve",
        ...     timestamp="2025-10-09T10:30:00Z",
        ...     approved=True,
        ...     metadata_updates={"review_mode": "full_required", "approved": True},
        ...     proceed_to_phase_3=True
        ... )
    """
    action: Literal["approve", "modify", "view", "question", "cancel"]
    timestamp: str
    approved: bool
    metadata_updates: Dict[str, Any] = field(default_factory=dict)
    proceed_to_phase_3: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert result to dictionary for serialization.

        Returns:
            Dict[str, Any]: JSON-serializable dictionary
        """
        return {
            "action": self.action,
            "timestamp": self.timestamp,
            "approved": self.approved,
            "metadata_updates": self.metadata_updates,
            "proceed_to_phase_3": self.proceed_to_phase_3,
        }


class FullReviewHandler:
    """
    Main coordinator for Full Review Mode workflow.

    Orchestrates comprehensive review display, user interaction, decision
    handling for approve/cancel actions, and state management. Implements
    stubs for modify/view/question actions (to be implemented in future tasks).

    Example:
        >>> handler = FullReviewHandler(
        ...     complexity_score=score,
        ...     plan=plan,
        ...     task_metadata=metadata,
        ...     task_file_path=Path("tasks/in_progress/TASK-001.md")
        ... )
        >>> result = handler.execute()
        >>>
        >>> if result.action == "approve":
        ...     # Proceed to Phase 3 implementation
        ...     pass
        >>> elif result.action == "cancel":
        ...     # Task cancelled, moved to backlog
        ...     pass
    """

    def __init__(
        self,
        complexity_score: "ComplexityScore",
        plan: ImplementationPlan,
        task_metadata: Dict[str, Any],
        task_file_path: Path,
        escalated: bool = False
    ):
        """
        Initialize full review handler.

        Args:
            complexity_score: ComplexityScore with evaluation results
            plan: ImplementationPlan with architectural details
            task_metadata: Task metadata (id, title, status, etc.)
            task_file_path: Path to task markdown file
            escalated: Whether this is an escalated review
        """
        self.complexity_score = complexity_score
        self.plan = plan
        self.task_metadata = task_metadata
        self.task_file_path = task_file_path
        self.escalated = escalated
        self.task_id = task_metadata.get("id", "UNKNOWN")
        self.review_start_time = datetime.utcnow()
        self.display = FullReviewDisplay(
            complexity_score=complexity_score,
            plan=plan,
            task_metadata=task_metadata,
            escalated=escalated
        )

    def execute(self) -> FullReviewResult:
        """
        Execute full review workflow.

        Workflow:
            1. Display comprehensive checkpoint
            2. Prompt for user decision
            3. Handle decision (approve/cancel/modify/view/question)
            4. Return result with metadata

        Returns:
            FullReviewResult: Review outcome with metadata

        Raises:
            KeyboardInterrupt: On Ctrl+C (handled as cancellation)

        Example:
            >>> result = handler.execute()
            >>> print(f"Action: {result.action}")
            >>> print(f"Approved: {result.approved}")
            >>> print(f"Proceed: {result.proceed_to_phase_3}")
        """
        try:
            # Display comprehensive checkpoint
            self.display.render_full_checkpoint()

            # Input validation loop with retry (max 3 invalid attempts)
            invalid_attempts = 0
            max_invalid_attempts = 3

            while True:
                choice = self._prompt_for_decision()

                if choice == 'a':
                    return self._handle_approval()
                elif choice == 'c':
                    result = self._handle_cancellation()
                    if result is not None:  # Confirmation succeeded
                        return result
                    # Confirmation aborted, re-prompt
                    continue
                elif choice == 'm':
                    # Enter modify mode - may return to continue loop or result
                    result = self._handle_modify()
                    if result is not None:
                        return result
                    # None means return to checkpoint, re-display and re-prompt
                    self.display.render_full_checkpoint()
                    continue
                elif choice == 'v':
                    # View mode - display plan in pager, then re-prompt
                    self._handle_view()
                    continue
                elif choice == 'q':
                    # Enter Q&A mode - may return to continue loop or result
                    result = self._handle_question()
                    if result is not None:
                        return result
                    # None means return to checkpoint, re-display and re-prompt
                    self.display.render_full_checkpoint()
                    continue
                else:
                    invalid_attempts += 1
                    print(f"\n❌ Invalid choice: '{choice}'")
                    print("Please enter A (Approve), M (Modify), V (View), Q (Question), or C (Cancel)\n")

                    if invalid_attempts >= max_invalid_attempts:
                        print(f"⚠️ {invalid_attempts} invalid attempts. Please review options carefully.\n")

                    continue

        except KeyboardInterrupt:
            # Ctrl+C treated as cancellation request
            print("\n\n⚠️ Interrupt detected. Treating as cancellation request...")
            return self._handle_cancellation(force=True)

        except Exception as e:
            # Unexpected error - log and re-raise
            print(f"\n❌ Error during full review: {e}")
            raise

    def _prompt_for_decision(self) -> str:
        """
        Prompt user for decision input.

        Returns:
            str: Lowercase single character choice

        Example:
            >>> choice = handler._prompt_for_decision()
            >>> assert choice in ['a', 'm', 'v', 'q', 'c']
        """
        choice = input("Your choice (A/M/V/Q/C): ").strip().lower()

        # Handle multi-character input - use first character
        if len(choice) > 1:
            choice = choice[0]

        # Handle empty input
        if not choice:
            print("\n⚠️ Please enter a choice (A/M/V/Q/C)\n")
            return ""  # Will be treated as invalid

        return choice

    def _handle_approval(self) -> FullReviewResult:
        """
        Handle plan approval.

        Creates result indicating approval, updates task metadata with
        approval details, and sets proceed flag for Phase 3.

        Returns:
            FullReviewResult: Result with approval metadata

        Example:
            >>> result = handler._handle_approval()
            >>> assert result.approved == True
            >>> assert result.proceed_to_phase_3 == True
        """
        print("\n✅ Plan approved!")
        print("Proceeding to Phase 3 (Implementation)...\n")

        timestamp = datetime.utcnow().isoformat() + "Z"
        review_duration = (datetime.utcnow() - self.review_start_time).total_seconds()

        # Build metadata updates
        metadata_updates = {
            "implementation_plan": {
                "approved": True,
                "approved_by": "user",
                "approved_at": timestamp,
                "review_mode": "escalated" if self.escalated else "full_required",
                "review_duration_seconds": int(review_duration),
                "complexity_score": self.complexity_score.total_score,
            }
        }

        return FullReviewResult(
            action="approve",
            timestamp=timestamp,
            approved=True,
            metadata_updates=metadata_updates,
            proceed_to_phase_3=True,
        )

    def _handle_cancellation(self, force: bool = False) -> Optional[FullReviewResult]:
        """
        Handle task cancellation with confirmation.

        Prompts user for confirmation unless forced. On confirmation,
        moves task to backlog and updates metadata.

        Args:
            force: Skip confirmation prompt (for Ctrl+C handling)

        Returns:
            Optional[FullReviewResult]: Result if confirmed, None if aborted

        Example:
            >>> result = handler._handle_cancellation()
            >>> if result:
            ...     assert result.action == "cancel"
            ...     assert result.approved == False
        """
        if not force:
            print("\n⚠️ Are you sure you want to cancel this task?")
            print("All work completed so far will be saved.\n")
            confirm = input("Confirm cancellation? [y/N]: ").strip().lower()
        else:
            confirm = 'y'  # Force confirmation on Ctrl+C

        if confirm == 'y':
            print("\n❌ Task cancelled. Moving to backlog...\n")

            timestamp = datetime.utcnow().isoformat() + "Z"

            # Build metadata updates
            metadata_updates = {
                "status": "backlog",
                "cancelled": True,
                "cancelled_at": timestamp,
                "cancellation_reason": "user_requested",
            }

            # Move task file to backlog
            self._move_task_to_backlog()

            return FullReviewResult(
                action="cancel",
                timestamp=timestamp,
                approved=False,
                metadata_updates=metadata_updates,
                proceed_to_phase_3=False,
            )
        else:
            print("\nCancellation aborted. Returning to checkpoint...\n")
            return None  # Signal to re-prompt

    def _handle_view(self) -> None:
        """
        Handle [V]iew action - display plan in system pager.

        Opens implementation plan in cross-platform pager (less/more)
        for detailed inspection. Returns to checkpoint after viewing.

        Example:
            >>> handler._handle_view()
            # Opens plan in pager, user reads, returns to checkpoint
        """
        try:
            from .pager_display import PagerDisplay
        except ImportError:
            from pager_display import PagerDisplay

        print("\n📖 Opening implementation plan in pager...")

        try:
            pager = PagerDisplay()
            success = pager.show_plan(self.plan)

            if not success:
                print("⚠️ Could not open pager, displaying inline instead:\n")
                # Fallback to inline display
                print(pager._format_plan(self.plan))

        except Exception as e:
            print(f"❌ Error displaying plan: {e}")
            print("Returning to checkpoint...\n")

    def _handle_modify(self) -> Optional[FullReviewResult]:
        """
        Handle [M]odify action - interactive plan modification.

        Enters interactive modification mode where user can:
        - Add/remove files
        - Add/remove dependencies
        - Modify phases
        - Update metadata

        Returns:
            Optional[FullReviewResult]: Result if session ends with approve/cancel,
                                       None if returning to checkpoint

        Example:
            >>> result = handler._handle_modify()
            >>> if result:
            ...     # User approved or cancelled
            ...     return result
            >>> else:
            ...     # User wants to return to checkpoint
            ...     continue
        """
        try:
            from .modification_session import ModificationSession
            from .modification_applier import ModificationApplier
            from .modification_persistence import ModificationPersistence
            from .version_manager import VersionManager
        except ImportError:
            from modification_session import ModificationSession
            from modification_applier import ModificationApplier
            from modification_persistence import ModificationPersistence
            from version_manager import VersionManager

        print("\n🔧 Entering modification mode...\n")

        # Create modification session
        session = ModificationSession(
            plan=self.plan,
            task_id=self.task_id,
            user_name="user"
        )

        try:
            session.start()

            # Interactive modification loop
            while session.is_active:
                print("\n" + "=" * 60)
                print("MODIFICATION MENU")
                print("=" * 60)
                print("\n[F] Add/Remove Files")
                print("[D] Add/Remove Dependencies")
                print("[P] View/Modify Phases")
                print("[M] Update Metadata (LOC, duration)")
                print("[S] Show Changes Summary")
                print("[A] Apply Changes & Return to Review")
                print("[C] Cancel Modifications")
                print()

                choice = input("Your choice: ").strip().lower()

                if choice == 'f':
                    self._modify_files(session)
                elif choice == 'd':
                    self._modify_dependencies(session)
                elif choice == 'p':
                    self._modify_phases(session)
                elif choice == 'm':
                    self._modify_metadata(session)
                elif choice == 's':
                    print("\n" + session.change_tracker.get_summary())
                elif choice == 'a':
                    return self._apply_modifications_and_return(session)
                elif choice == 'c':
                    return self._cancel_modifications(session)
                else:
                    print(f"\n❌ Invalid choice: '{choice}'")
                    print("Please choose F, D, P, M, S, A, or C\n")

        except KeyboardInterrupt:
            print("\n\n⚠️ Interrupt detected during modification...")
            session.cancel("Interrupted by user")
            print("Returning to checkpoint...\n")
            return None

        except Exception as e:
            print(f"\n❌ Error during modification: {e}")
            session.error(str(e))
            print("Returning to checkpoint...\n")
            return None

    def _modify_files(self, session: "ModificationSession") -> None:
        """Handle file add/remove operations."""
        print("\n" + "=" * 60)
        print("FILE MODIFICATION")
        print("=" * 60)
        print("\nCurrent files:")
        for i, file_path in enumerate(session.plan.files_to_create, 1):
            print(f"  {i}. {file_path}")

        print("\n[A] Add file")
        print("[R] Remove file")
        print("[B] Back to menu")
        print()

        choice = input("Your choice: ").strip().lower()

        if choice == 'a':
            file_path = input("Enter file path: ").strip()
            if file_path:
                purpose = input("Purpose (optional): ").strip() or None
                session.change_tracker.record_file_added(file_path, purpose)
                print(f"✅ Marked file for addition: {file_path}")
        elif choice == 'r':
            file_num = input("Enter file number to remove: ").strip()
            try:
                idx = int(file_num) - 1
                if 0 <= idx < len(session.plan.files_to_create):
                    file_path = session.plan.files_to_create[idx]
                    session.change_tracker.record_file_removed(file_path)
                    print(f"✅ Marked file for removal: {file_path}")
                else:
                    print("❌ Invalid file number")
            except ValueError:
                print("❌ Please enter a valid number")

    def _modify_dependencies(self, session: "ModificationSession") -> None:
        """Handle dependency add/remove operations."""
        print("\n" + "=" * 60)
        print("DEPENDENCY MODIFICATION")
        print("=" * 60)
        print("\nCurrent dependencies:")
        for i, dep in enumerate(session.plan.external_dependencies, 1):
            print(f"  {i}. {dep}")

        print("\n[A] Add dependency")
        print("[R] Remove dependency")
        print("[B] Back to menu")
        print()

        choice = input("Your choice: ").strip().lower()

        if choice == 'a':
            dependency = input("Enter dependency name: ").strip()
            if dependency:
                purpose = input("Purpose (optional): ").strip() or None
                session.change_tracker.record_dependency_added(dependency, purpose)
                print(f"✅ Marked dependency for addition: {dependency}")
        elif choice == 'r':
            dep_num = input("Enter dependency number to remove: ").strip()
            try:
                idx = int(dep_num) - 1
                if 0 <= idx < len(session.plan.external_dependencies):
                    dependency = session.plan.external_dependencies[idx]
                    session.change_tracker.record_dependency_removed(dependency)
                    print(f"✅ Marked dependency for removal: {dependency}")
                else:
                    print("❌ Invalid dependency number")
            except ValueError:
                print("❌ Please enter a valid number")

    def _modify_phases(self, session: "ModificationSession") -> None:
        """Handle phase viewing and modification."""
        print("\n" + "=" * 60)
        print("IMPLEMENTATION PHASES")
        print("=" * 60)

        if session.plan.phases:
            print("\nCurrent phases:")
            for i, phase in enumerate(session.plan.phases, 1):
                print(f"  {i}. {phase}")
        else:
            print("\nNo phases defined")

        print("\n[A] Add phase")
        print("[R] Remove phase")
        print("[B] Back to menu")
        print()

        choice = input("Your choice: ").strip().lower()

        if choice == 'a':
            phase_desc = input("Enter phase description: ").strip()
            if phase_desc:
                # Default to appending at end
                position = len(session.plan.phases) if session.plan.phases else 0
                session.change_tracker.record_phase_added(phase_desc, position)
                print(f"✅ Marked phase for addition: {phase_desc}")
        elif choice == 'r':
            if not session.plan.phases:
                print("❌ No phases to remove")
                return

            phase_num = input("Enter phase number to remove: ").strip()
            try:
                idx = int(phase_num) - 1
                if 0 <= idx < len(session.plan.phases):
                    phase_desc = session.plan.phases[idx]
                    session.change_tracker.record_phase_removed(phase_desc, idx)
                    print(f"✅ Marked phase for removal: {phase_desc}")
                else:
                    print("❌ Invalid phase number")
            except ValueError:
                print("❌ Please enter a valid number")

    def _modify_metadata(self, session: "ModificationSession") -> None:
        """Handle metadata updates."""
        print("\n" + "=" * 60)
        print("METADATA UPDATE")
        print("=" * 60)
        print("\nCurrent metadata:")
        print(f"  Estimated LOC: {session.plan.estimated_loc or 'Not set'}")
        print(f"  Estimated Duration: {session.plan.estimated_duration or 'Not set'}")
        print(f"  Test Summary: {session.plan.test_summary or 'Not set'}")

        print("\n[L] Update estimated LOC")
        print("[D] Update estimated duration")
        print("[T] Update test summary")
        print("[B] Back to menu")
        print()

        choice = input("Your choice: ").strip().lower()

        if choice == 'l':
            loc_str = input("Enter estimated LOC: ").strip()
            try:
                new_loc = int(loc_str)
                old_loc = session.plan.estimated_loc
                session.change_tracker.record_metadata_updated(
                    "estimated_loc", old_loc, new_loc
                )
                print(f"✅ Marked LOC for update: {old_loc} → {new_loc}")
            except ValueError:
                print("❌ Please enter a valid number")
        elif choice == 'd':
            new_duration = input("Enter estimated duration (e.g., '2-3 hours'): ").strip()
            if new_duration:
                old_duration = session.plan.estimated_duration
                session.change_tracker.record_metadata_updated(
                    "estimated_duration", old_duration, new_duration
                )
                print(f"✅ Marked duration for update: {old_duration} → {new_duration}")
        elif choice == 't':
            new_summary = input("Enter test summary: ").strip()
            if new_summary:
                old_summary = session.plan.test_summary
                session.change_tracker.record_metadata_updated(
                    "test_summary", old_summary, new_summary
                )
                print(f"✅ Marked test summary for update")

    def _apply_modifications_and_return(
        self,
        session: "ModificationSession"
    ) -> Optional[FullReviewResult]:
        """Apply modifications, create new version, and return to checkpoint."""
        try:
            from .modification_applier import ModificationApplier
            from .modification_persistence import ModificationPersistence
            from .version_manager import VersionManager
        except ImportError:
            from modification_applier import ModificationApplier
            from modification_persistence import ModificationPersistence
            from version_manager import VersionManager
        try:
            from .complexity_calculator import ComplexityCalculator
            from .complexity_models import EvaluationContext
        except ImportError:
            from complexity_calculator import ComplexityCalculator
            from complexity_models import EvaluationContext

        if session.change_tracker.is_empty:
            print("\n⚠️ No changes to apply")
            session.end(save=False)
            return None

        print("\n" + "=" * 60)
        print("APPLYING MODIFICATIONS")
        print("=" * 60)

        # Show change summary
        print("\n" + session.change_tracker.get_summary())

        # Confirm application
        print("\n⚠️ Apply these changes and create new plan version?")
        confirm = input("Confirm? [y/N]: ").strip().lower()

        if confirm != 'y':
            print("\nApplication cancelled. Returning to modification menu...\n")
            return None

        try:
            # Apply changes to create modified plan
            applier = ModificationApplier(self.plan, session.change_tracker)
            modified_plan = applier.apply()

            # Recalculate complexity for modified plan
            calculator = ComplexityCalculator()
            context = EvaluationContext(
                task_id=self.task_id,
                technology_stack=self.task_metadata.get("technology_stack", "unknown"),
                implementation_plan=modified_plan,
                task_metadata=self.task_metadata,
            )
            new_complexity = calculator.calculate(context)
            modified_plan.complexity_score = new_complexity

            # Create new version
            version_manager = VersionManager(self.task_id)
            version = version_manager.create_version(
                modified_plan,
                change_reason=f"Modified in review ({session.change_tracker.change_count} changes)",
                created_by="user"
            )

            # Save session for audit trail
            persistence = ModificationPersistence(self.task_id)
            persistence.save_session(session)

            # End session
            session.end(save=True)

            # Update handler's plan to modified version
            self.plan = modified_plan
            self.complexity_score = new_complexity

            print(f"\n✅ Changes applied successfully!")
            print(f"Created plan version {version.version_number}")
            print(f"New complexity score: {new_complexity.total_score}/10")
            print("\nReturning to checkpoint with modified plan...\n")

            # Return None to re-display checkpoint with modified plan
            return None

        except Exception as e:
            print(f"\n❌ Error applying modifications: {e}")
            print("Returning to modification menu...\n")
            session.error(str(e))
            return None

    def _cancel_modifications(
        self,
        session: "ModificationSession"
    ) -> Optional[FullReviewResult]:
        """Cancel modifications and return to checkpoint."""
        if session.change_tracker.change_count > 0:
            print(f"\n⚠️ You have {session.change_tracker.change_count} unsaved changes.")
            print("Are you sure you want to cancel modifications?")
            confirm = input("Confirm? [y/N]: ").strip().lower()

            if confirm != 'y':
                print("\nCancellation aborted. Returning to modification menu...\n")
                return None

        session.cancel("User requested cancellation")
        print("Returning to checkpoint...\n")
        return None

    def _handle_question(self) -> Optional[FullReviewResult]:
        """
        Handle [Q]uestion command - enter Q&A mode.

        Enters interactive Q&A mode where user can ask questions about
        the implementation plan and receive contextual answers via
        keyword-based extraction.

        Returns:
            Optional[FullReviewResult]: None to return to checkpoint,
                                       or result if session ends with decision

        Example:
            >>> result = handler._handle_question()
            >>> if result is None:
            ...     # User typed 'back', return to checkpoint
            ...     continue
        """
        try:
            from .qa_manager import QAManager
        except ImportError:
            from qa_manager import QAManager

        # Create QAManager
        qa_manager = QAManager(
            plan=self.plan,
            task_id=self.task_id,
            task_metadata=self.task_metadata
        )

        # Run Q&A session
        session = qa_manager.run_qa_session()

        # Save session to metadata if completed
        if session and session.ended_at:
            qa_manager.save_to_metadata(str(self.task_file_path))

        # Return None to indicate return to checkpoint
        return None

    def _move_task_to_backlog(self) -> None:
        """
        Move task file from in_progress to backlog directory.

        Uses atomic file operations to ensure safe state transition.
        Updates task metadata before moving file.

        Raises:
            OSError: On file system errors
        """
        try:
            from .user_interaction import FileOperations
        except ImportError:
            from user_interaction import FileOperations

        # Read current task file
        content = self.task_file_path.read_text(encoding="utf-8")

        # Parse frontmatter and update status
        match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
        if match:
            frontmatter = yaml.safe_load(match.group(1))
            body = match.group(2)

            # Update frontmatter
            frontmatter["status"] = "backlog"
            frontmatter["cancelled"] = True
            frontmatter["cancelled_at"] = datetime.utcnow().isoformat() + "Z"
            frontmatter["updated"] = datetime.utcnow().isoformat() + "Z"

            # Rebuild content
            updated_content = f"---\n{yaml.dump(frontmatter, default_flow_style=False)}---\n{body}"
        else:
            # No frontmatter found, use original content
            updated_content = content

        # Determine backlog path relative to task file location
        # task_file_path is typically: .../tasks/in_progress/TASK-XXX.md
        # We want: .../tasks/backlog/TASK-XXX.md
        tasks_dir = self.task_file_path.parent.parent  # Go up from in_progress to tasks
        backlog_dir = tasks_dir / "backlog"

        try:
            backlog_dir.mkdir(parents=True, exist_ok=True)
            backlog_path = backlog_dir / self.task_file_path.name

            # Write to backlog location atomically
            FileOperations.atomic_write(backlog_path, updated_content)

            # Remove from in_progress
            self.task_file_path.unlink()

            print(f"\n✅ Task moved to backlog: {backlog_path.name}")

        except OSError as e:
            # File write failure - log error but don't crash
            print(f"\n⚠️  Warning: Could not move task file to backlog: {e}")
            print(f"    Task status updated but file remains in: {self.task_file_path.parent.name}/")
            print(f"    You can manually move the file later if needed.")
            # Continue - task cancellation processed even if file move fails


# Module exports
__all__ = [
    "ReviewAction",
    "QuickReviewResult",
    "QuickReviewDisplay",
    "QuickReviewHandler",
    "FullReviewResult",
    "FullReviewDisplay",
    "FullReviewHandler",
]
