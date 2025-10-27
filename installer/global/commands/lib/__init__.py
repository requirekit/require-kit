"""
Complexity evaluation library for Phase 2.7.

This package provides complexity scoring, review routing, plan modification,
versioning, and shared utilities for the Agentecflow task-work workflow.
"""

from .complexity_models import (
    ReviewMode,
    ForceReviewTrigger,
    FactorScore,
    ComplexityScore,
    ImplementationPlan,
    ReviewDecision,
    EvaluationContext
)

from .complexity_factors import (
    ComplexityFactor,
    FileComplexityFactor,
    PatternFamiliarityFactor,
    RiskLevelFactor,
    DEFAULT_FACTORS
)

from .complexity_calculator import ComplexityCalculator

from .review_router import ReviewRouter, format_complexity_summary_compact

from .agent_utils import (
    parse_implementation_plan,
    build_evaluation_context,
    format_decision_for_display,
    format_decision_for_metadata,
    log_complexity_calculation,
    extract_task_metadata_from_frontmatter
)

# Review modes (TASK-003B-2, TASK-003B-3)
from .review_modes import (
    QuickReviewResult,
    QuickReviewDisplay,
    QuickReviewHandler,
    FullReviewResult,
    FullReviewDisplay,
    FullReviewHandler,
)

# Pager display (TASK-003B-3)
from .pager_display import (
    PagerStrategy,
    UnixPagerStrategy,
    WindowsPagerStrategy,
    FallbackPagerStrategy,
    PagerDisplay,
)

# Change tracking (TASK-003B-3)
from .change_tracker import (
    ChangeType,
    Change,
    ChangeTracker,
)

# Modification session (TASK-003B-3)
from .modification_session import (
    SessionState,
    SessionMetadata,
    ModificationSession,
)

# Modification applier (TASK-003B-3)
from .modification_applier import (
    ModificationApplier,
)

# Modification persistence (TASK-003B-3)
from .modification_persistence import (
    ModificationPersistence,
)

# Version management (TASK-003B-3)
from .version_manager import (
    PlanVersion,
    VersionManager,
)

# Flag validation (TASK-003E Phase 5 Day 2)
from .flag_validator import (
    FlagValidator,
    FlagConflictError,
    validate_flags,
)

# Error message formatters (TASK-003E Phase 5 Day 2)
from .error_messages import (
    format_file_error,
    format_validation_error,
    format_calculation_error,
)

__version__ = "1.1.0"

__all__ = [
    # Models
    "ReviewMode",
    "ForceReviewTrigger",
    "FactorScore",
    "ComplexityScore",
    "ImplementationPlan",
    "ReviewDecision",
    "EvaluationContext",

    # Factors
    "ComplexityFactor",
    "FileComplexityFactor",
    "PatternFamiliarityFactor",
    "RiskLevelFactor",
    "DEFAULT_FACTORS",

    # Calculator
    "ComplexityCalculator",

    # Router
    "ReviewRouter",
    "format_complexity_summary_compact",

    # Utils
    "parse_implementation_plan",
    "build_evaluation_context",
    "format_decision_for_display",
    "format_decision_for_metadata",
    "log_complexity_calculation",
    "extract_task_metadata_from_frontmatter",

    # Review modes
    "QuickReviewResult",
    "QuickReviewDisplay",
    "QuickReviewHandler",
    "FullReviewResult",
    "FullReviewDisplay",
    "FullReviewHandler",

    # Pager display
    "PagerStrategy",
    "UnixPagerStrategy",
    "WindowsPagerStrategy",
    "FallbackPagerStrategy",
    "PagerDisplay",

    # Change tracking
    "ChangeType",
    "Change",
    "ChangeTracker",

    # Modification session
    "SessionState",
    "SessionMetadata",
    "ModificationSession",

    # Modification applier
    "ModificationApplier",

    # Modification persistence
    "ModificationPersistence",

    # Version management
    "PlanVersion",
    "VersionManager",

    # Flag validation
    "FlagValidator",
    "FlagConflictError",
    "validate_flags",

    # Error message formatters
    "format_file_error",
    "format_validation_error",
    "format_calculation_error",
]
