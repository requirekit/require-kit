"""
Core complexity calculation engine.

This module aggregates individual factor scores into a final complexity score
and handles error scenarios with fail-safe defaults.

Scoring Scale:
- 1-3 points: Auto-proceed (simple tasks)
- 4-6 points: Quick optional review
- 7-10 points: Full review required

Error Handling:
- On any error during calculation, default to score=10 (full review required)
- Log errors for debugging but never fail the task workflow
"""

import logging
from datetime import datetime
from typing import List, Optional

try:
    from .complexity_models import (
        ComplexityScore,
        FactorScore,
        ReviewMode,
        ForceReviewTrigger,
        EvaluationContext
    )
except ImportError:
    from complexity_models import (
        ComplexityScore,
        FactorScore,
        ReviewMode,
        ForceReviewTrigger,
        EvaluationContext
    )
try:
    from .complexity_factors import ComplexityFactor, DEFAULT_FACTORS
except ImportError:
    from complexity_factors import ComplexityFactor, DEFAULT_FACTORS


logger = logging.getLogger(__name__)


class ComplexityCalculator:
    """Calculates aggregate complexity score from multiple factors.

    This is the core calculation engine that:
    1. Evaluates all configured factors
    2. Aggregates scores into total complexity (1-10 scale)
    3. Detects force-review triggers
    4. Determines appropriate review mode
    5. Handles errors with fail-safe defaults
    """

    # Scoring configuration
    MAX_TOTAL_SCORE = 10  # Maximum aggregate complexity score

    # Review mode thresholds
    AUTO_PROCEED_THRESHOLD = 3  # Score <= 3: auto-proceed
    QUICK_OPTIONAL_THRESHOLD = 6  # Score 4-6: quick optional review
    # Score >= 7: full required review

    def __init__(self, factors: Optional[List[ComplexityFactor]] = None):
        """Initialize calculator with scoring factors.

        Args:
            factors: List of ComplexityFactor implementations to evaluate.
                    Defaults to DEFAULT_FACTORS (3 core factors).
        """
        self.factors = factors if factors is not None else DEFAULT_FACTORS
        logger.info(f"ComplexityCalculator initialized with {len(self.factors)} factors")

    def calculate(self, context: EvaluationContext) -> ComplexityScore:
        """Calculate aggregate complexity score for a task.

        This is the main entry point for complexity calculation. It orchestrates:
        1. Factor evaluation
        2. Score aggregation
        3. Trigger detection
        4. Review mode determination

        Args:
            context: Evaluation context with task and plan details

        Returns:
            ComplexityScore with total score, factor scores, and review mode

        Raises:
            Never raises - returns fail-safe score=10 on any error
        """
        try:
            logger.info(f"Calculating complexity for task {context.task_id}")

            # Step 1: Evaluate all factors
            factor_scores = self._evaluate_factors(context)

            # Step 2: Aggregate into total score
            total_score = self._aggregate_scores(factor_scores)

            # Step 3: Detect force-review triggers
            forced_triggers = self._detect_forced_triggers(context)

            # Step 4: Determine review mode
            review_mode = self._determine_review_mode(total_score, forced_triggers)

            # Step 5: Build result
            complexity_score = ComplexityScore(
                total_score=total_score,
                factor_scores=factor_scores,
                forced_review_triggers=forced_triggers,
                review_mode=review_mode,
                calculation_timestamp=datetime.now(),
                metadata={
                    "task_id": context.task_id,
                    "technology_stack": context.technology_stack,
                    "factors_evaluated": len(factor_scores)
                }
            )

            logger.info(
                f"Complexity calculated: score={total_score}, "
                f"mode={review_mode.value}, triggers={len(forced_triggers)}"
            )

            return complexity_score

        except Exception as e:
            # Fail-safe: Default to maximum complexity (full review required)
            logger.error(
                f"Error calculating complexity for {context.task_id}: {e}",
                exc_info=True
            )
            return self._create_failsafe_score(context, str(e))

    def _evaluate_factors(self, context: EvaluationContext) -> List[FactorScore]:
        """Evaluate all configured factors.

        Args:
            context: Evaluation context

        Returns:
            List of FactorScore results (one per factor)

        Note:
            If a factor evaluation fails, it's logged but doesn't fail the entire calculation.
        """
        factor_scores = []

        for factor in self.factors:
            try:
                score = factor.evaluate(context)
                factor_scores.append(score)
                logger.debug(
                    f"Factor '{score.factor_name}': {score.score}/{score.max_score} - "
                    f"{score.justification}"
                )
            except Exception as e:
                # Log factor error but continue with other factors
                factor_name = getattr(factor, 'FACTOR_NAME', factor.__class__.__name__)
                logger.error(f"Error evaluating factor {factor_name}: {e}", exc_info=True)
                # Skip failed factor (conservative: don't add zero score, just omit)

        return factor_scores

    def _aggregate_scores(self, factor_scores: List[FactorScore]) -> int:
        """Aggregate factor scores into total complexity score.

        Aggregation strategy:
        - Sum raw scores from all factors
        - Cap at MAX_TOTAL_SCORE (10)
        - Round to nearest integer

        Args:
            factor_scores: List of individual factor scores

        Returns:
            Total complexity score (1-10 scale, capped)
        """
        if not factor_scores:
            # No factors evaluated - default to moderate complexity
            logger.warning("No factor scores available, defaulting to score=5")
            return 5

        # Sum raw scores
        raw_total = sum(score.score for score in factor_scores)

        # Cap at maximum
        capped_total = min(raw_total, self.MAX_TOTAL_SCORE)

        # Round to integer (already int, but explicit for clarity)
        final_score = int(round(capped_total))

        # Ensure minimum score of 1 (0 is not valid)
        final_score = max(final_score, 1)

        logger.debug(
            f"Score aggregation: raw={raw_total}, "
            f"capped={capped_total}, final={final_score}"
        )

        return final_score

    def _detect_forced_triggers(self, context: EvaluationContext) -> List[ForceReviewTrigger]:
        """Detect conditions that force full review regardless of complexity score.

        Force-review triggers:
        - User explicitly requested review (--review flag)
        - Security-sensitive functionality
        - Breaking changes to public APIs
        - Database schema modifications
        - Production hotfix

        Args:
            context: Evaluation context

        Returns:
            List of triggered ForceReviewTrigger enums
        """
        triggers = []

        # Check user flag
        if context.user_requested_review:
            triggers.append(ForceReviewTrigger.USER_FLAG)
            logger.info("Force trigger: User explicitly requested review")

        # Check security keywords
        if context.implementation_plan.has_security_keywords:
            triggers.append(ForceReviewTrigger.SECURITY_KEYWORDS)
            logger.info("Force trigger: Security-sensitive functionality detected")

        # Check schema changes
        if context.implementation_plan.has_schema_changes:
            triggers.append(ForceReviewTrigger.SCHEMA_CHANGES)
            logger.info("Force trigger: Database schema changes detected")

        # Check hotfix flag
        if context.is_hotfix:
            triggers.append(ForceReviewTrigger.HOTFIX)
            logger.info("Force trigger: Production hotfix detected")

        # Check breaking changes (analyze plan text)
        if self._has_breaking_changes(context.implementation_plan.raw_plan):
            triggers.append(ForceReviewTrigger.BREAKING_CHANGES)
            logger.info("Force trigger: Breaking changes detected")

        return triggers

    def _has_breaking_changes(self, plan_text: str) -> bool:
        """Detect breaking changes from plan text.

        Heuristics:
        - Mentions of "breaking change"
        - Public API modifications (remove, delete, rename endpoints)
        - Contract changes (request/response format changes)

        Args:
            plan_text: Implementation plan text

        Returns:
            True if breaking changes detected
        """
        breaking_keywords = [
            "breaking change", "breaking api", "remove endpoint",
            "delete endpoint", "rename endpoint", "change contract",
            "modify response", "modify request", "api version"
        ]

        plan_lower = plan_text.lower()
        return any(keyword in plan_lower for keyword in breaking_keywords)

    def _determine_review_mode(
        self,
        total_score: int,
        forced_triggers: List[ForceReviewTrigger]
    ) -> ReviewMode:
        """Determine appropriate review mode based on score and triggers.

        Decision logic:
        1. If any force-review triggers present → FULL_REQUIRED
        2. Else if score <= 3 → AUTO_PROCEED
        3. Else if score 4-6 → QUICK_OPTIONAL
        4. Else (score >= 7) → FULL_REQUIRED

        Args:
            total_score: Aggregate complexity score (1-10)
            forced_triggers: List of active force-review triggers

        Returns:
            ReviewMode enum value
        """
        # Force-review triggers override score-based routing
        if forced_triggers:
            logger.info(
                f"Review mode: FULL_REQUIRED (triggers: "
                f"{[t.value for t in forced_triggers]})"
            )
            return ReviewMode.FULL_REQUIRED

        # Score-based routing
        if total_score <= self.AUTO_PROCEED_THRESHOLD:
            logger.info(f"Review mode: AUTO_PROCEED (score={total_score})")
            return ReviewMode.AUTO_PROCEED
        elif total_score <= self.QUICK_OPTIONAL_THRESHOLD:
            logger.info(f"Review mode: QUICK_OPTIONAL (score={total_score})")
            return ReviewMode.QUICK_OPTIONAL
        else:
            logger.info(f"Review mode: FULL_REQUIRED (score={total_score})")
            return ReviewMode.FULL_REQUIRED

    def _create_failsafe_score(
        self,
        context: EvaluationContext,
        error_message: str
    ) -> ComplexityScore:
        """Create fail-safe complexity score when calculation fails.

        Fail-safe strategy:
        - Score = 10 (maximum complexity)
        - Review mode = FULL_REQUIRED (mandatory review)
        - Include error details in metadata

        Args:
            context: Evaluation context
            error_message: Error that triggered fail-safe

        Returns:
            ComplexityScore with conservative defaults
        """
        logger.warning(
            f"Creating fail-safe score for {context.task_id} due to error: {error_message}"
        )

        return ComplexityScore(
            total_score=self.MAX_TOTAL_SCORE,  # Maximum complexity
            factor_scores=[],  # No factor scores available
            forced_review_triggers=[],  # No triggers detected
            review_mode=ReviewMode.FULL_REQUIRED,  # Force full review
            calculation_timestamp=datetime.now(),
            metadata={
                "task_id": context.task_id,
                "technology_stack": context.technology_stack,
                "failsafe": True,
                "error": error_message,
                "reason": "Complexity calculation failed - defaulting to full review for safety"
            }
        )
