#!/usr/bin/env python3
"""
Complexity Evaluation for TASK-003B-4: Q&A Mode - Interactive Plan Questions

This script performs Phase 2.7 complexity evaluation based on the implementation plan.
"""

import sys
from datetime import datetime
from pathlib import Path

# Add lib path for imports
lib_path = Path(__file__).parent / "installer/global/commands/lib"
sys.path.insert(0, str(lib_path))

from complexity_models import (
    ImplementationPlan,
    EvaluationContext,
    ComplexityScore,
    FactorScore,
    ReviewMode,
    ForceReviewTrigger,
    ReviewDecision
)
from complexity_calculator import ComplexityCalculator
from complexity_factors import FileComplexityFactor, PatternFamiliarityFactor, RiskLevelFactor


def build_implementation_plan() -> ImplementationPlan:
    """Build ImplementationPlan from TASK-003B-4 specifications."""

    # From implementation plan analysis
    files_to_create = [
        "installer/global/commands/lib/qa_manager.py"  # 1 new file (~400 lines)
    ]

    # Files to modify (extracted from implementation plan)
    files_to_modify = [
        "installer/global/commands/lib/review_modes.py"  # 1 method modification (~50 lines)
    ]

    # Combine for total file count
    all_files = files_to_create + files_to_modify

    # Design patterns mentioned
    patterns_used = [
        "Strategy",  # Section extractors
        "Dataclass",  # QAExchange, QASession
        "Session Management"  # QASession pattern
    ]

    # External dependencies
    external_dependencies = []  # Zero external dependencies (Python 3.9+ stdlib only)

    # Raw implementation plan text (excerpt)
    raw_plan = """
# TASK-003B-4: Q&A Mode - Interactive Plan Questions
## Implementation Design Document (Simplified Version)

**Status**: Design Phase
**Priority**: LOW (optional enhancement)
**Estimated Effort**: 3 hours
**Approach**: Simplified keyword matching (no AI agent dependency)

### 1. Executive Summary
Implement **simplified Q&A mode** for TASK-003B-4 using keyword-based pattern matching
instead of full AI agent integration. This provides 80% of value with 20% of effort.

### 2. Architecture Design

#### Class Structure:
1. QAExchange (dataclass) - Single question-answer exchange
2. QASession (dataclass) - Complete Q&A session metadata
3. KeywordMatcher - Maps user questions to plan sections via keyword patterns
4. PlanSectionExtractor - Extracts relevant plan sections (Strategy pattern)
5. QAManager - Main coordinator for Q&A mode

#### Integration Point:
- Target File: review_modes.py
- Target Class: FullReviewHandler._handle_question() (currently stub)
- Entry Point: User presses [Q] at full review checkpoint

### 3. File Structure
New Files:
- qa_manager.py (400 lines) - All Q&A classes

Modified Files:
- review_modes.py (1 method, ~50 lines modification)

### 4. Risk Assessment
- Security: None (no user data handling, keyboard input only)
- Schema changes: Yes (task metadata YAML - adds qa_session field)
- Performance: Low risk (<100ms response time for keyword matching)
- Breaking changes: None (adds optional [Q] command to existing checkpoint)

### 5. Implementation Phases
Phase 1: Core Classes (1 hour)
Phase 2: Section Extraction (1 hour)
Phase 3: Q&A Manager (45 minutes)
Phase 4: Integration (30 minutes)
Phase 5: Testing (45 minutes)
Phase 6: Documentation & Polish (15 minutes)

**Total Estimated Time**: 3 hours
**Estimated LOC**: 400 (qa_manager.py) + 50 (review_modes.py) = 450 lines
"""

    # Risk details from architectural review
    risk_details = []  # Zero critical issues from architectural review (88/100 score)

    # Implementation phases
    phases = [
        "Phase 1: Core Classes (1 hour)",
        "Phase 2: Section Extraction (1 hour)",
        "Phase 3: Q&A Manager (45 minutes)",
        "Phase 4: Integration (30 minutes)",
        "Phase 5: Testing (45 minutes)",
        "Phase 6: Documentation & Polish (15 minutes)"
    ]

    # Test strategy
    test_summary = """
Unit tests for KeywordMatcher, PlanSectionExtractor, QAManager.
Integration tests for complete Q&A workflow.
Target coverage: ≥80%
    """

    return ImplementationPlan(
        task_id="TASK-003B-4",
        files_to_create=all_files,
        patterns_used=patterns_used,
        external_dependencies=external_dependencies,
        estimated_loc=450,
        risk_indicators=[],
        raw_plan=raw_plan,
        test_summary=test_summary,
        risk_details=risk_details,
        phases=phases,
        estimated_duration="3 hours"
    )


def build_evaluation_context(plan: ImplementationPlan) -> EvaluationContext:
    """Build EvaluationContext for complexity calculation."""

    task_metadata = {
        "id": "TASK-003B-4",
        "title": "Q&A Mode - Interactive Plan Questions",
        "priority": "low",  # From implementation plan
        "tags": ["optional", "enhancement"],
        "is_hotfix": False
    }

    user_flags = {
        "review": False  # --review flag not present
    }

    return EvaluationContext(
        task_id="TASK-003B-4",
        technology_stack="python",
        implementation_plan=plan,
        task_metadata=task_metadata,
        user_flags=user_flags
    )


def format_decision_summary(decision: ReviewDecision) -> str:
    """Format decision for human-readable display."""

    score = decision.complexity_score

    # Determine emoji based on review mode
    if score.review_mode == ReviewMode.AUTO_PROCEED:
        emoji = "✅"
        mode_label = "AUTO-PROCEED"
    elif score.review_mode == ReviewMode.QUICK_OPTIONAL:
        emoji = "⚠️ "
        mode_label = "OPTIONAL REVIEW"
    else:
        emoji = "🔴"
        mode_label = "REVIEW REQUIRED"

    lines = [
        f"\n{emoji} Complexity Evaluation - TASK-003B-4",
        f"\nScore: {score.total_score}/10 ({mode_label})",
        ""
    ]

    # Add force-review triggers if present
    if score.forced_review_triggers:
        lines.append("Force-Review Triggers:")
        for trigger in score.forced_review_triggers:
            lines.append(f"  🔴 {trigger.value.replace('_', ' ').title()}")
        lines.append("")

    # Add factor breakdown
    lines.append("Factor Breakdown:")
    for factor_score in score.factor_scores:
        # Determine indicator based on score
        if factor_score.score == 0:
            indicator = "•"
        elif factor_score.score >= factor_score.max_score * 0.7:
            indicator = "🔴"
        elif factor_score.score >= factor_score.max_score * 0.4:
            indicator = "⚠️ "
        else:
            indicator = "•"

        lines.append(
            f"  {indicator} {factor_score.factor_name}: {int(factor_score.score)}/{int(factor_score.max_score)} - "
            f"{factor_score.justification}"
        )

    lines.append("")

    # Add routing decision
    if score.review_mode == ReviewMode.AUTO_PROCEED:
        lines.append("✅ AUTO-PROCEEDING to Phase 3 (Implementation)")
        lines.append("   No human review required for this simple task.")
    elif score.review_mode == ReviewMode.QUICK_OPTIONAL:
        lines.append("⚠️  OPTIONAL CHECKPOINT")
        lines.append("   You may review the plan before proceeding, but it's not required.")
        lines.append("   [A]pprove and proceed | [R]eview in detail | [Enter] to auto-approve")
    else:
        lines.append("🔴 MANDATORY CHECKPOINT - Phase 2.6 Required")
        lines.append("   This task requires human review before implementation.")
        lines.append("   Proceeding to Phase 2.6 human checkpoint...")

    lines.append("")

    return "\n".join(lines)


def format_metadata_for_yaml(decision: ReviewDecision) -> dict:
    """Format decision for task metadata YAML."""

    score = decision.complexity_score

    return {
        "complexity_evaluation": {
            "total_score": score.total_score,
            "review_mode": score.review_mode.value,
            "action": decision.action,
            "routing": decision.routing_recommendation,
            "auto_approved": decision.auto_approved,
            "timestamp": decision.timestamp.isoformat() + "Z",
            "factor_scores": [
                {
                    "name": fs.factor_name,
                    "score": int(fs.score),
                    "max": int(fs.max_score),
                    "justification": fs.justification
                }
                for fs in score.factor_scores
            ],
            "forced_triggers": [t.value for t in score.forced_review_triggers],
            "summary": decision.summary_message
        }
    }


def main():
    """Execute complexity evaluation for TASK-003B-4."""

    print("=" * 80)
    print("Phase 2.7: Complexity Evaluation - TASK-003B-4")
    print("=" * 80)
    print()

    # Step 1: Build implementation plan
    print("Step 1: Parsing implementation plan...")
    plan = build_implementation_plan()
    print(f"  ✓ Files to create/modify: {len(plan.files_to_create)}")
    print(f"  ✓ Design patterns: {len(plan.patterns_used)}")
    print(f"  ✓ External dependencies: {len(plan.external_dependencies)}")
    print(f"  ✓ Estimated LOC: {plan.estimated_loc}")
    print()

    # Step 2: Build evaluation context
    print("Step 2: Building evaluation context...")
    context = build_evaluation_context(plan)
    print(f"  ✓ Task ID: {context.task_id}")
    print(f"  ✓ Technology stack: {context.technology_stack}")
    print(f"  ✓ Priority: {context.task_metadata['priority']}")
    print(f"  ✓ User flags: {context.user_flags}")
    print()

    # Step 3: Calculate complexity score
    print("Step 3: Calculating complexity score...")
    calculator = ComplexityCalculator()
    complexity_score = calculator.calculate(context)
    print(f"  ✓ Total score: {complexity_score.total_score}/10")
    print(f"  ✓ Review mode: {complexity_score.review_mode.value}")
    print(f"  ✓ Forced triggers: {len(complexity_score.forced_review_triggers)}")
    print()

    # Step 4: Build review decision
    print("Step 4: Building review decision...")

    if complexity_score.review_mode == ReviewMode.AUTO_PROCEED:
        action = "proceed"
        routing = "Phase 3 (Implementation)"
        auto_approved = True
    elif complexity_score.review_mode == ReviewMode.QUICK_OPTIONAL:
        action = "review_required"
        routing = "Phase 2.6 Checkpoint (Optional)"
        auto_approved = False
    else:
        action = "review_required"
        routing = "Phase 2.6 Checkpoint (Mandatory)"
        auto_approved = False

    decision = ReviewDecision(
        action=action,
        complexity_score=complexity_score,
        routing_recommendation=routing,
        summary_message=f"Score {complexity_score.total_score}/10 → {complexity_score.review_mode.value}",
        auto_approved=auto_approved,
        timestamp=datetime.now()
    )
    print(f"  ✓ Action: {decision.action}")
    print(f"  ✓ Routing: {decision.routing_recommendation}")
    print(f"  ✓ Auto-approved: {decision.auto_approved}")
    print()

    # Step 5: Display decision summary
    print("Step 5: Decision Summary")
    print("-" * 80)
    summary = format_decision_summary(decision)
    print(summary)

    # Step 6: Generate metadata for task file
    print("\nStep 6: Task Metadata Update")
    print("-" * 80)
    metadata = format_metadata_for_yaml(decision)

    import yaml
    print("\nMetadata to add to TASK-003B-4.md:")
    print(yaml.dump(metadata, default_flow_style=False, sort_keys=False))

    # Step 7: Final recommendations
    print("\nStep 7: Final Recommendations")
    print("-" * 80)
    print(f"\n✓ Complexity evaluation complete for TASK-003B-4")
    print(f"✓ Total score: {complexity_score.total_score}/10")
    print(f"✓ Routing: {decision.routing_recommendation}")

    if decision.should_proceed_to_implementation:
        print(f"\n✅ APPROVED: Proceeding directly to Phase 3 (Implementation)")
        print(f"   No human review required for this low-complexity task.")
    elif complexity_score.review_mode == ReviewMode.QUICK_OPTIONAL:
        print(f"\n⚠️  OPTIONAL REVIEW: Human checkpoint offered but not required")
        print(f"   Task can auto-proceed if user chooses [Enter] or [A]pprove.")
    else:
        print(f"\n🔴 REVIEW REQUIRED: Mandatory Phase 2.6 checkpoint")
        print(f"   Human review required before implementation can begin.")

    print("\n" + "=" * 80)
    print("Complexity evaluation complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
