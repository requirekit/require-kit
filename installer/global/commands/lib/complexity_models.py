"""
Data models for complexity evaluation system.

This module provides type-safe data structures for representing complexity scores,
review modes, and evaluation results. All models use dataclasses for immutability
and clear type hints for type safety.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any


class ReviewMode(Enum):
    """Review mode determines the level of human review required."""
    AUTO_PROCEED = "auto_proceed"  # Score 1-3: Display summary, proceed to Phase 3
    QUICK_OPTIONAL = "quick_optional"  # Score 4-6: Optional human review
    FULL_REQUIRED = "full_required"  # Score 7-10 or force triggers: Mandatory review


class ForceReviewTrigger(Enum):
    """Conditions that force full review regardless of complexity score."""
    USER_FLAG = "user_flag"  # --review flag explicitly set
    SECURITY_KEYWORDS = "security_keywords"  # Security-sensitive functionality
    BREAKING_CHANGES = "breaking_changes"  # Public API changes
    SCHEMA_CHANGES = "schema_changes"  # Database schema modifications
    HOTFIX = "hotfix"  # Production hotfix under time pressure


@dataclass(frozen=True)
class FactorScore:
    """Score for a single complexity factor.

    Attributes:
        factor_name: Name of the scoring factor (e.g., "file_complexity")
        score: Numeric score (0-10 scale depending on factor)
        max_score: Maximum possible score for this factor
        justification: Human-readable explanation of the score
        details: Additional context (file count, patterns detected, etc.)
    """
    factor_name: str
    score: float
    max_score: float
    justification: str
    details: Dict[str, Any] = field(default_factory=dict)

    @property
    def normalized_score(self) -> float:
        """Normalize score to 0-1 range for aggregation."""
        if self.max_score == 0:
            return 0.0
        return self.score / self.max_score


@dataclass(frozen=True)
class ComplexityScore:
    """Aggregated complexity score across all factors.

    Attributes:
        total_score: Final complexity score (1-10 scale)
        factor_scores: Individual scores for each factor
        forced_review_triggers: List of triggers forcing full review
        review_mode: Determined review mode based on score and triggers
        calculation_timestamp: When this score was calculated
        metadata: Additional context (task details, stack info, etc.)
    """
    total_score: int  # 1-10 scale
    factor_scores: List[FactorScore]
    forced_review_triggers: List[ForceReviewTrigger]
    review_mode: ReviewMode
    calculation_timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def has_forced_triggers(self) -> bool:
        """Check if any force-review triggers are active."""
        return len(self.forced_review_triggers) > 0

    @property
    def requires_human_review(self) -> bool:
        """Determine if human review is required (not auto-proceed)."""
        return self.review_mode != ReviewMode.AUTO_PROCEED

    def get_factor_score(self, factor_name: str) -> Optional[FactorScore]:
        """Retrieve score for a specific factor by name."""
        for score in self.factor_scores:
            if score.factor_name == factor_name:
                return score
        return None


@dataclass
class ImplementationPlan:
    """Structured representation of Phase 2 implementation plan.

    This model parses and structures the implementation plan from the
    planning agent for complexity analysis.

    Attributes:
        task_id: Task identifier (e.g., TASK-042)
        files_to_create: List of files to create/modify
        patterns_used: Design patterns mentioned in plan
        external_dependencies: External APIs, databases, services
        estimated_loc: Estimated lines of code (if provided)
        risk_indicators: Keywords suggesting high risk (auth, payment, etc.)
        raw_plan: Original plan text for reference
        test_summary: Optional test strategy summary (simplified)
        risk_details: Optional list of risk dictionaries (severity, description, mitigation)
        phases: Optional list of implementation phase descriptions
        implementation_instructions: Optional formatted instructions for display
        estimated_duration: Optional estimated implementation time (e.g., "2-3 hours")
        complexity_score: Optional reference to ComplexityScore object
    """
    task_id: str
    files_to_create: List[str] = field(default_factory=list)
    patterns_used: List[str] = field(default_factory=list)
    external_dependencies: List[str] = field(default_factory=list)
    estimated_loc: Optional[int] = None
    risk_indicators: List[str] = field(default_factory=list)
    raw_plan: str = ""

    # Extended fields for full review mode (TASK-003B-2)
    test_summary: Optional[str] = None
    risk_details: Optional[List[Dict[str, Any]]] = None
    phases: Optional[List[str]] = None
    implementation_instructions: Optional[str] = None
    estimated_duration: Optional[str] = None
    complexity_score: Optional[Any] = None  # Forward reference to ComplexityScore

    @property
    def file_count(self) -> int:
        """Number of files to be created/modified."""
        return len(self.files_to_create)

    @property
    def dependency_count(self) -> int:
        """Number of external dependencies."""
        return len(self.external_dependencies)

    @property
    def has_security_keywords(self) -> bool:
        """Check if plan contains security-related keywords."""
        security_keywords = [
            "authentication", "authorization", "auth", "security",
            "password", "token", "jwt", "oauth", "encryption", "crypto"
        ]
        plan_lower = self.raw_plan.lower()
        return any(keyword in plan_lower for keyword in security_keywords)

    @property
    def has_schema_changes(self) -> bool:
        """Check if plan involves database schema modifications."""
        schema_keywords = [
            "migration", "schema", "alter table", "create table",
            "drop table", "database", "db migration"
        ]
        plan_lower = self.raw_plan.lower()
        return any(keyword in plan_lower for keyword in schema_keywords)


@dataclass
class ReviewDecision:
    """Decision made during Phase 2.7 complexity evaluation.

    Attributes:
        action: Action to take (proceed, review_required, blocked)
        complexity_score: Calculated complexity score
        routing_recommendation: Next phase or human checkpoint
        summary_message: Human-readable decision explanation
        auto_approved: Whether decision was automatic (no human input)
        timestamp: When decision was made
    """
    action: str  # "proceed", "review_required", "blocked"
    complexity_score: ComplexityScore
    routing_recommendation: str  # "Phase 3", "Phase 2.6 Checkpoint", "Phase 2 Revision"
    summary_message: str
    auto_approved: bool
    timestamp: datetime

    @property
    def should_proceed_to_implementation(self) -> bool:
        """Check if task should proceed to Phase 3 implementation."""
        return self.action == "proceed"

    @property
    def needs_human_checkpoint(self) -> bool:
        """Check if Phase 2.6 human checkpoint is required."""
        return self.action == "review_required"


@dataclass
class EvaluationContext:
    """Context information for complexity evaluation.

    Attributes:
        task_id: Task identifier
        technology_stack: Detected tech stack (python, react, maui, etc.)
        implementation_plan: Parsed implementation plan from Phase 2
        task_metadata: Additional task metadata (priority, tags, etc.)
        user_flags: User-provided flags (--review, --skip-review, etc.)
    """
    task_id: str
    technology_stack: str
    implementation_plan: ImplementationPlan
    task_metadata: Dict[str, Any] = field(default_factory=dict)
    user_flags: Dict[str, bool] = field(default_factory=dict)

    @property
    def is_critical_priority(self) -> bool:
        """Check if task has critical priority."""
        return self.task_metadata.get("priority") == "critical"

    @property
    def is_hotfix(self) -> bool:
        """Check if task is marked as hotfix."""
        return self.task_metadata.get("is_hotfix", False) or \
               "hotfix" in self.task_metadata.get("tags", [])

    @property
    def user_requested_review(self) -> bool:
        """Check if user explicitly requested review."""
        return self.user_flags.get("review", False)
