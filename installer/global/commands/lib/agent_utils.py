"""
Shared utility functions for agents using complexity evaluation.

This module provides reusable functions for:
1. Parsing implementation plans into ImplementationPlan models
2. Building EvaluationContext from task metadata
3. Formatting complexity results for display
4. Common error handling patterns

Used by: complexity-evaluator agent and future specialist agents.
"""

import logging
import re
from typing import Dict, Any, List, Optional
from datetime import datetime

try:
    from .complexity_models import (
        ImplementationPlan,
        EvaluationContext,
        ComplexityScore,
        ReviewDecision
    )
except ImportError:
    from complexity_models import (
        ImplementationPlan,
        EvaluationContext,
        ComplexityScore,
        ReviewDecision
    )


logger = logging.getLogger(__name__)


def parse_implementation_plan(
    plan_text: str,
    task_id: str
) -> ImplementationPlan:
    """Parse implementation plan text into structured ImplementationPlan.

    Extracts:
    - Files to create/modify (from markdown lists, code blocks)
    - Design patterns mentioned
    - External dependencies (APIs, databases, services)
    - Risk indicators (security, schema, etc.)

    Args:
        plan_text: Raw implementation plan text from Phase 2
        task_id: Task identifier

    Returns:
        ImplementationPlan with extracted structured data
    """
    try:
        # Extract files (look for common patterns)
        files = _extract_files(plan_text)

        # Extract design patterns
        patterns = _extract_patterns(plan_text)

        # Extract external dependencies
        dependencies = _extract_dependencies(plan_text)

        # Extract risk indicators
        risk_indicators = _extract_risk_indicators(plan_text)

        # Estimate LOC (if mentioned)
        estimated_loc = _extract_loc_estimate(plan_text)

        return ImplementationPlan(
            task_id=task_id,
            files_to_create=files,
            patterns_used=patterns,
            external_dependencies=dependencies,
            estimated_loc=estimated_loc,
            risk_indicators=risk_indicators,
            raw_plan=plan_text
        )

    except Exception as e:
        logger.error(f"Error parsing implementation plan for {task_id}: {e}", exc_info=True)
        # Return minimal plan to allow complexity calculation to proceed
        return ImplementationPlan(
            task_id=task_id,
            raw_plan=plan_text
        )


def _extract_files(plan_text: str) -> List[str]:
    """Extract file paths from implementation plan.

    Looks for:
    - Markdown lists with file extensions (.py, .ts, .cs, etc.)
    - Code blocks with file path comments
    - Explicit "Files to create:" sections

    Args:
        plan_text: Plan text

    Returns:
        List of file paths (deduplicated)
    """
    files = []

    # Pattern 1: Markdown list items with file extensions
    # Example: - src/services/user_service.py
    file_pattern = r'[-*]\s+([^\s]+\.(?:py|ts|tsx|js|jsx|cs|java|go|rb|php))'
    matches = re.findall(file_pattern, plan_text, re.IGNORECASE)
    files.extend(matches)

    # Pattern 2: Inline file mentions (with backticks)
    # Example: `src/models/user.py`
    inline_pattern = r'`([^\s`]+\.(?:py|ts|tsx|js|jsx|cs|java|go|rb|php))`'
    matches = re.findall(inline_pattern, plan_text, re.IGNORECASE)
    files.extend(matches)

    # Pattern 3: File path in code comments
    # Example: # File: src/services/auth.py
    comment_pattern = r'#\s*[Ff]ile:\s+([^\s]+\.(?:py|ts|tsx|js|jsx|cs|java|go|rb|php))'
    matches = re.findall(comment_pattern, plan_text)
    files.extend(matches)

    # Deduplicate and clean
    unique_files = list(set(files))
    return unique_files


def _extract_patterns(plan_text: str) -> List[str]:
    """Extract design pattern mentions from plan.

    Looks for common pattern names:
    - Repository, Factory, Strategy, Observer, etc.
    - Case-insensitive matching

    Args:
        plan_text: Plan text

    Returns:
        List of pattern names (deduplicated)
    """
    common_patterns = [
        "Repository", "Factory", "Singleton", "Adapter", "Bridge",
        "Strategy", "Observer", "Decorator", "Command", "Chain of Responsibility",
        "Mediator", "Saga", "CQRS", "Event Sourcing", "Circuit Breaker",
        "Retry", "Bulkhead", "Facade", "Proxy", "Template Method"
    ]

    patterns_found = []
    plan_lower = plan_text.lower()

    for pattern in common_patterns:
        if pattern.lower() in plan_lower:
            patterns_found.append(pattern)

    return patterns_found


def _extract_dependencies(plan_text: str) -> List[str]:
    """Extract external dependencies from plan.

    Looks for:
    - API endpoints (http://, https://)
    - Database mentions (PostgreSQL, MongoDB, etc.)
    - Third-party services (Stripe, SendGrid, etc.)

    Args:
        plan_text: Plan text

    Returns:
        List of dependency descriptions
    """
    dependencies = []

    # API endpoints
    api_pattern = r'(https?://[^\s]+)'
    apis = re.findall(api_pattern, plan_text)
    dependencies.extend([f"API: {api}" for api in apis])

    # Database mentions
    db_keywords = ["postgresql", "mysql", "mongodb", "redis", "sqlite", "dynamodb"]
    plan_lower = plan_text.lower()
    for db in db_keywords:
        if db in plan_lower:
            dependencies.append(f"Database: {db.title()}")

    # Third-party services
    service_keywords = [
        "stripe", "sendgrid", "twilio", "aws", "azure", "gcp",
        "firebase", "auth0", "okta"
    ]
    for service in service_keywords:
        if service in plan_lower:
            dependencies.append(f"Service: {service.title()}")

    return list(set(dependencies))  # Deduplicate


def _extract_risk_indicators(plan_text: str) -> List[str]:
    """Extract risk indicator keywords from plan.

    Args:
        plan_text: Plan text

    Returns:
        List of risk indicator keywords found
    """
    risk_keywords = [
        "security", "authentication", "authorization", "encryption",
        "migration", "schema", "breaking change", "performance-critical"
    ]

    indicators = []
    plan_lower = plan_text.lower()

    for keyword in risk_keywords:
        if keyword in plan_lower:
            indicators.append(keyword)

    return indicators


def _extract_loc_estimate(plan_text: str) -> Optional[int]:
    """Extract lines of code estimate if mentioned.

    Looks for patterns like:
    - "approximately 200 lines"
    - "~150 LOC"
    - "around 300 lines of code"

    Args:
        plan_text: Plan text

    Returns:
        Estimated LOC as integer, or None if not found
    """
    # Pattern: number followed by "lines" or "LOC"
    pattern = r'(\d+)\s*(?:lines|LOC|lines of code)'
    match = re.search(pattern, plan_text, re.IGNORECASE)

    if match:
        return int(match.group(1))

    return None


def build_evaluation_context(
    task_id: str,
    technology_stack: str,
    implementation_plan: ImplementationPlan,
    task_metadata: Optional[Dict[str, Any]] = None,
    user_flags: Optional[Dict[str, bool]] = None
) -> EvaluationContext:
    """Build EvaluationContext from task components.

    Args:
        task_id: Task identifier
        technology_stack: Detected tech stack
        implementation_plan: Parsed implementation plan
        task_metadata: Additional task metadata (priority, tags, etc.)
        user_flags: User-provided flags (--review, etc.)

    Returns:
        EvaluationContext ready for complexity calculation
    """
    return EvaluationContext(
        task_id=task_id,
        technology_stack=technology_stack,
        implementation_plan=implementation_plan,
        task_metadata=task_metadata or {},
        user_flags=user_flags or {}
    )


def format_decision_for_display(decision: ReviewDecision) -> str:
    """Format ReviewDecision for terminal display.

    Creates a visually formatted box with decision details.

    Args:
        decision: Review decision to format

    Returns:
        Formatted string for terminal display
    """
    box_width = 80
    separator = "=" * box_width

    lines = [
        separator,
        _center_text("PHASE 2.7 - COMPLEXITY EVALUATION RESULT", box_width),
        separator,
        "",
        decision.summary_message,
        "",
        separator
    ]

    return "\n".join(lines)


def format_decision_for_metadata(decision: ReviewDecision) -> Dict[str, Any]:
    """Format ReviewDecision for task file metadata.

    Extracts key information for storage in task frontmatter.

    Args:
        decision: Review decision

    Returns:
        Dictionary suitable for YAML frontmatter
    """
    score = decision.complexity_score

    return {
        "complexity_evaluation": {
            "score": score.total_score,
            "review_mode": score.review_mode.value,
            "action": decision.action,
            "routing": decision.routing_recommendation,
            "auto_approved": decision.auto_approved,
            "timestamp": decision.timestamp.isoformat(),
            "factors": [
                {
                    "name": f.factor_name,
                    "score": f.score,
                    "max": f.max_score,
                    "justification": f.justification
                }
                for f in score.factor_scores
            ],
            "triggers": [t.value for t in score.forced_review_triggers]
        }
    }


def _center_text(text: str, width: int) -> str:
    """Center text within given width."""
    padding = (width - len(text)) // 2
    return " " * padding + text


def log_complexity_calculation(
    task_id: str,
    complexity_score: ComplexityScore,
    decision: ReviewDecision
) -> None:
    """Log complexity calculation results for debugging.

    Args:
        task_id: Task identifier
        complexity_score: Calculated complexity score
        decision: Routing decision
    """
    logger.info(f"=== Complexity Calculation: {task_id} ===")
    logger.info(f"Total Score: {complexity_score.total_score}/10")
    logger.info(f"Review Mode: {complexity_score.review_mode.value}")

    for factor in complexity_score.factor_scores:
        logger.info(
            f"  Factor '{factor.factor_name}': {factor.score}/{factor.max_score} - "
            f"{factor.justification}"
        )

    if complexity_score.forced_review_triggers:
        trigger_names = [t.value for t in complexity_score.forced_review_triggers]
        logger.info(f"Forced Triggers: {', '.join(trigger_names)}")

    logger.info(f"Decision: {decision.action} → {decision.routing_recommendation}")
    logger.info("=" * 50)


def extract_task_metadata_from_frontmatter(frontmatter: Dict[str, Any]) -> Dict[str, Any]:
    """Extract relevant task metadata for complexity evaluation.

    Args:
        frontmatter: Parsed task file frontmatter (YAML)

    Returns:
        Dictionary with relevant metadata for EvaluationContext
    """
    return {
        "priority": frontmatter.get("priority", "medium"),
        "tags": frontmatter.get("tags", []),
        "is_hotfix": frontmatter.get("is_hotfix", False),
        "epic_id": frontmatter.get("epic"),
        "feature_id": frontmatter.get("feature")
    }
