"""
Review routing logic for Phase 2.7 complexity evaluation.

This module translates complexity scores into actionable routing decisions:
- Auto-proceed to Phase 3 (simple tasks)
- Quick optional human checkpoint (moderate tasks)
- Full required human checkpoint (complex/risky tasks)

It generates human-readable summaries and routing recommendations.
"""

import logging
from datetime import datetime
from typing import Dict, Any

try:
    from .complexity_models import (
        ComplexityScore,
        ReviewMode,
        ReviewDecision,
        EvaluationContext
    )
except ImportError:
    from complexity_models import (
        ComplexityScore,
        ReviewMode,
        ReviewDecision,
        EvaluationContext
    )


logger = logging.getLogger(__name__)


class ReviewRouter:
    """Routes tasks to appropriate review mode based on complexity score.

    Responsibilities:
    1. Interpret complexity score and triggers
    2. Generate human-readable summary
    3. Determine next phase (3, 2.6, or 2 revision)
    4. Create ReviewDecision with routing recommendation
    """

    def route(
        self,
        complexity_score: ComplexityScore,
        context: EvaluationContext
    ) -> ReviewDecision:
        """Route task based on complexity score.

        Args:
            complexity_score: Calculated complexity score
            context: Evaluation context

        Returns:
            ReviewDecision with action and routing recommendation
        """
        try:
            logger.info(
                f"Routing task {context.task_id}: "
                f"score={complexity_score.total_score}, "
                f"mode={complexity_score.review_mode.value}"
            )

            # Route based on review mode
            if complexity_score.review_mode == ReviewMode.AUTO_PROCEED:
                decision = self._auto_proceed_decision(complexity_score, context)
            elif complexity_score.review_mode == ReviewMode.QUICK_OPTIONAL:
                decision = self._quick_optional_decision(complexity_score, context)
            else:  # ReviewMode.FULL_REQUIRED
                decision = self._full_required_decision(complexity_score, context)

            logger.info(
                f"Routing decision: action={decision.action}, "
                f"recommendation={decision.routing_recommendation}"
            )

            return decision

        except Exception as e:
            # Fail-safe: Default to review required
            logger.error(f"Error routing task {context.task_id}: {e}", exc_info=True)
            return self._create_failsafe_decision(complexity_score, context, str(e))

    def _auto_proceed_decision(
        self,
        complexity_score: ComplexityScore,
        context: EvaluationContext
    ) -> ReviewDecision:
        """Create decision for auto-proceed tasks (score 1-3).

        Auto-proceed flow:
        - Display complexity summary
        - Automatically proceed to Phase 3 implementation
        - No human intervention required

        Args:
            complexity_score: Complexity score
            context: Evaluation context

        Returns:
            ReviewDecision with proceed action
        """
        summary = self._build_auto_proceed_summary(complexity_score, context)

        return ReviewDecision(
            action="proceed",
            complexity_score=complexity_score,
            routing_recommendation="Phase 3",
            summary_message=summary,
            auto_approved=True,
            timestamp=datetime.now()
        )

    def _quick_optional_decision(
        self,
        complexity_score: ComplexityScore,
        context: EvaluationContext
    ) -> ReviewDecision:
        """Create decision for quick optional review tasks (score 4-6).

        Quick optional flow:
        - Display complexity summary with optional checkpoint prompt
        - User can approve (proceed to Phase 3) or review (Phase 2.6)
        - Default to proceed after timeout (non-blocking)

        Args:
            complexity_score: Complexity score
            context: Evaluation context

        Returns:
            ReviewDecision with review_required action (but optional)
        """
        summary = self._build_quick_optional_summary(complexity_score, context)

        return ReviewDecision(
            action="review_required",  # Triggers optional checkpoint
            complexity_score=complexity_score,
            routing_recommendation="Phase 2.6 Checkpoint (Optional)",
            summary_message=summary,
            auto_approved=False,
            timestamp=datetime.now()
        )

    def _full_required_decision(
        self,
        complexity_score: ComplexityScore,
        context: EvaluationContext
    ) -> ReviewDecision:
        """Create decision for full required review tasks (score 7-10 or triggers).

        Full required flow:
        - Display detailed complexity summary
        - Mandatory Phase 2.6 human checkpoint
        - User must approve, revise, or escalate

        Args:
            complexity_score: Complexity score
            context: Evaluation context

        Returns:
            ReviewDecision with review_required action (mandatory)
        """
        summary = self._build_full_required_summary(complexity_score, context)

        return ReviewDecision(
            action="review_required",  # Triggers mandatory checkpoint
            complexity_score=complexity_score,
            routing_recommendation="Phase 2.6 Checkpoint (Required)",
            summary_message=summary,
            auto_approved=False,
            timestamp=datetime.now()
        )

    def _build_auto_proceed_summary(
        self,
        complexity_score: ComplexityScore,
        context: EvaluationContext
    ) -> str:
        """Build summary message for auto-proceed tasks.

        Format:
        - Complexity score and interpretation
        - Factor breakdown
        - Auto-proceed confirmation

        Args:
            complexity_score: Complexity score
            context: Evaluation context

        Returns:
            Human-readable summary string
        """
        lines = [
            f"✅ Complexity Evaluation - {context.task_id}",
            "",
            f"Score: {complexity_score.total_score}/10 (Low Complexity - Auto-Proceed)",
            "",
            "Factor Breakdown:"
        ]

        for factor in complexity_score.factor_scores:
            lines.append(
                f"  • {factor.factor_name}: {factor.score}/{factor.max_score} - "
                f"{factor.justification}"
            )

        lines.extend([
            "",
            "✅ AUTO-PROCEEDING to Phase 3 (Implementation)",
            "   No human review required for this simple task."
        ])

        return "\n".join(lines)

    def _build_quick_optional_summary(
        self,
        complexity_score: ComplexityScore,
        context: EvaluationContext
    ) -> str:
        """Build summary message for quick optional review tasks.

        Format:
        - Complexity score and interpretation
        - Factor breakdown with warnings
        - Optional checkpoint prompt

        Args:
            complexity_score: Complexity score
            context: Evaluation context

        Returns:
            Human-readable summary string
        """
        lines = [
            f"⚠️  Complexity Evaluation - {context.task_id}",
            "",
            f"Score: {complexity_score.total_score}/10 (Moderate Complexity - Optional Review)",
            "",
            "Factor Breakdown:"
        ]

        for factor in complexity_score.factor_scores:
            icon = "⚠️" if factor.score >= factor.max_score * 0.7 else "•"
            lines.append(
                f"  {icon} {factor.factor_name}: {factor.score}/{factor.max_score} - "
                f"{factor.justification}"
            )

        lines.extend([
            "",
            "⚠️  OPTIONAL CHECKPOINT",
            "   You may review the plan before proceeding, but it's not required.",
            "   [A]pprove and proceed | [R]eview in detail | [Enter] to auto-approve"
        ])

        return "\n".join(lines)

    def _build_full_required_summary(
        self,
        complexity_score: ComplexityScore,
        context: EvaluationContext
    ) -> str:
        """Build summary message for full required review tasks.

        Format:
        - Complexity score and severity
        - Force-review triggers (if any)
        - Factor breakdown with critical indicators
        - Mandatory checkpoint warning

        Args:
            complexity_score: Complexity score
            context: Evaluation context

        Returns:
            Human-readable summary string
        """
        lines = [
            f"🔴 Complexity Evaluation - {context.task_id}",
            "",
            f"Score: {complexity_score.total_score}/10 (High Complexity - REVIEW REQUIRED)",
            ""
        ]

        # Include force-review triggers if present
        if complexity_score.forced_review_triggers:
            lines.append("Force-Review Triggers:")
            for trigger in complexity_score.forced_review_triggers:
                lines.append(f"  🔴 {trigger.value.replace('_', ' ').title()}")
            lines.append("")

        lines.append("Factor Breakdown:")

        for factor in complexity_score.factor_scores:
            # Critical if score >= 70% of max
            is_critical = factor.score >= factor.max_score * 0.7
            icon = "🔴" if is_critical else "⚠️"
            lines.append(
                f"  {icon} {factor.factor_name}: {factor.score}/{factor.max_score} - "
                f"{factor.justification}"
            )

        lines.extend([
            "",
            "🔴 MANDATORY CHECKPOINT - Phase 2.6 Required",
            "   This task requires human review before implementation.",
            "   Proceeding to Phase 2.6 human checkpoint..."
        ])

        return "\n".join(lines)

    def _create_failsafe_decision(
        self,
        complexity_score: ComplexityScore,
        context: EvaluationContext,
        error_message: str
    ) -> ReviewDecision:
        """Create fail-safe decision when routing fails.

        Fail-safe strategy:
        - Action: review_required (mandatory)
        - Route to Phase 2.6 checkpoint
        - Include error in metadata

        Args:
            complexity_score: Complexity score (may be fail-safe score)
            context: Evaluation context
            error_message: Error that triggered fail-safe

        Returns:
            ReviewDecision with fail-safe defaults
        """
        logger.warning(
            f"Creating fail-safe routing decision for {context.task_id}: {error_message}"
        )

        summary = (
            f"⚠️  Complexity Evaluation Error - {context.task_id}\n"
            f"\n"
            f"An error occurred during complexity evaluation:\n"
            f"{error_message}\n"
            f"\n"
            f"Defaulting to FULL REVIEW REQUIRED for safety.\n"
            f"Please review the implementation plan before proceeding.\n"
        )

        return ReviewDecision(
            action="review_required",
            complexity_score=complexity_score,
            routing_recommendation="Phase 2.6 Checkpoint (Required - Error Recovery)",
            summary_message=summary,
            auto_approved=False,
            timestamp=datetime.now()
        )


def format_complexity_summary_compact(complexity_score: ComplexityScore) -> str:
    """Format compact complexity summary for display in task metadata.

    Used for task file metadata and logging.

    Args:
        complexity_score: Complexity score to format

    Returns:
        Compact single-line or multi-line summary
    """
    trigger_text = ""
    if complexity_score.forced_review_triggers:
        triggers = [t.value for t in complexity_score.forced_review_triggers]
        trigger_text = f", triggers: {', '.join(triggers)}"

    factors_text = ", ".join(
        f"{f.factor_name}={f.score}/{f.max_score}"
        for f in complexity_score.factor_scores
    )

    return (
        f"Complexity: {complexity_score.total_score}/10 "
        f"({complexity_score.review_mode.value})"
        f"{trigger_text} | Factors: {factors_text}"
    )
