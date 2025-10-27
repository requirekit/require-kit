#!/usr/bin/env python3
"""
Example usage of Plan Review Configuration & Metrics System.

This demonstrates how to use the configuration and metrics modules
in the task-work workflow (Phase 2.7).
"""
import sys
from pathlib import Path

# Add lib to path
lib_path = Path(__file__).parent.parent / 'installer' / 'global' / 'lib'
sys.path.insert(0, str(lib_path))


def example_configuration_usage():
    """Demonstrate configuration management."""
    print("=" * 80)
    print("Configuration Usage Example")
    print("=" * 80)

    from config import PlanReviewConfig

    # Get singleton instance
    config = PlanReviewConfig()

    # Check if system is enabled
    if not config.is_enabled():
        print("Plan review system is disabled")
        return

    print(f"✓ Plan review enabled: {config.is_enabled()}")
    print(f"✓ Review mode: {config.get_mode()}")
    print(f"✓ Metrics enabled: {config.is_metrics_enabled()}")

    # Get decision threshold for a score
    score = 73
    stack = 'python'
    decision = config.get_threshold(score, stack)
    print(f"\n✓ Score {score} for {stack} → {decision}")

    # Check if review should be forced
    complexity = 35
    keywords = ['database', 'migration']
    forced = config.should_force_review(complexity, keywords)
    print(f"✓ Complexity {complexity} with keywords {keywords} → Forced: {forced}")

    # Get timeouts
    arch_timeout = config.get_timeout('architectural_review')
    human_timeout = config.get_timeout('human_checkpoint')
    print(f"✓ Architectural review timeout: {arch_timeout}s")
    print(f"✓ Human checkpoint timeout: {human_timeout}s")

    # Get weights
    weights = config.get_weights()
    print(f"✓ Scoring weights: {weights}")

    # CLI override example
    print("\n--- CLI Override Example ---")
    config.set_cli_override('thresholds.auto_approve', 85)
    decision_after = config.get_threshold(score, stack)
    print(f"✓ After CLI override (85): Score {score} → {decision_after}")


def example_metrics_tracking():
    """Demonstrate metrics tracking."""
    print("\n" + "=" * 80)
    print("Metrics Tracking Example")
    print("=" * 80)

    from metrics import PlanReviewMetrics

    metrics = PlanReviewMetrics()

    # Track complexity
    print("\n1. Tracking complexity calculation...")
    success = metrics.track_complexity(
        task_id='TASK-EXAMPLE-001',
        complexity_score=28,
        factors={
            'file_count': 3,
            'dependencies': 8,
            'critical_keywords': 1
        },
        stack='python'
    )
    print(f"   {'✓' if success else '✗'} Complexity tracked: {success}")

    # Track architectural decision
    print("\n2. Tracking architectural review decision...")
    success = metrics.track_decision(
        task_id='TASK-EXAMPLE-001',
        architectural_score=73,
        decision='approve_with_recommendations',
        complexity_score=28,
        stack='python',
        forced=False,
        recommendations=[
            'Consider extracting database logic into separate module',
            'Add integration tests for migration scenarios'
        ]
    )
    print(f"   {'✓' if success else '✗'} Decision tracked: {success}")

    # Track final outcome
    print("\n3. Tracking final outcome...")
    success = metrics.track_outcome(
        task_id='TASK-EXAMPLE-001',
        decision='approve_with_recommendations',
        human_override=False,
        duration_seconds=287.5,
        final_status='approved',
        stack='python'
    )
    print(f"   {'✓' if success else '✗'} Outcome tracked: {success}")

    # Get recent metrics
    print("\n4. Querying recent metrics...")
    recent = metrics.get_recent_metrics(days=7)
    print(f"   ✓ Found {len(recent)} metrics from last 7 days")


def example_dashboard_visualization():
    """Demonstrate dashboard visualization."""
    print("\n" + "=" * 80)
    print("Dashboard Visualization Example")
    print("=" * 80)

    from metrics import PlanReviewDashboard

    dashboard = PlanReviewDashboard()

    # Render dashboard
    print("\nGenerating dashboard for last 30 days...\n")
    dashboard.print_dashboard(days=30)


def example_integration_workflow():
    """Demonstrate complete workflow integration."""
    print("\n" + "=" * 80)
    print("Complete Workflow Integration Example")
    print("=" * 80)

    from config import PlanReviewConfig
    from metrics import PlanReviewMetrics

    # Simulate task-work Phase 2.7: Determine review necessity

    task_id = 'TASK-EXAMPLE-002'
    complexity_score = 35  # From complexity_calculator
    stack = 'python'

    print(f"\nTask: {task_id}")
    print(f"Complexity Score: {complexity_score}")
    print(f"Stack: {stack}")

    # Step 1: Load configuration
    config = PlanReviewConfig()

    # Step 2: Check if plan review is enabled
    if not config.is_enabled():
        print("\n✓ Plan review disabled - skipping")
        return

    # Step 3: Check mode
    mode = config.get_mode()
    print(f"\n✓ Review mode: {mode}")

    if mode == 'never':
        print("✓ Mode is 'never' - skipping review")
        return

    # Step 4: Check if review should be forced
    keywords = ['database', 'migration', 'schema']
    forced = config.should_force_review(complexity_score, keywords)
    print(f"✓ Force triggers checked: {forced}")

    # Step 5: Determine if review is needed
    needs_review = False
    if mode == 'always':
        needs_review = True
        print("✓ Mode is 'always' - review required")
    elif forced:
        needs_review = True
        print("✓ Force trigger activated - review required")
    elif mode == 'auto' and complexity_score >= 30:
        needs_review = True
        print(f"✓ Complexity {complexity_score} >= 30 - review required")

    if not needs_review:
        print("✓ No review needed - proceeding to implementation")
        return

    print("\n--- Architectural Review Triggered ---")

    # Step 6: Track complexity metric
    metrics = PlanReviewMetrics()
    metrics.track_complexity(
        task_id=task_id,
        complexity_score=complexity_score,
        factors={
            'keywords': keywords,
            'file_count': 5,
            'dependencies': 12
        },
        stack=stack
    )
    print("✓ Complexity metric tracked")

    # Step 7: Simulate architectural review
    # (In real workflow, this calls architectural-reviewer agent)
    architectural_score = 73  # Example score from review

    # Step 8: Get decision based on score
    decision = config.get_threshold(architectural_score, stack)
    print(f"\n✓ Architectural score: {architectural_score}")
    print(f"✓ Decision: {decision}")

    # Step 9: Track decision metric
    recommendations = [
        'Extract database operations to repository pattern',
        'Add rollback mechanism for migration failures'
    ]
    metrics.track_decision(
        task_id=task_id,
        architectural_score=architectural_score,
        decision=decision,
        complexity_score=complexity_score,
        stack=stack,
        forced=forced,
        recommendations=recommendations
    )
    print("✓ Decision metric tracked")

    # Step 10: Handle decision
    if decision == 'reject':
        print("\n✗ Plan rejected - revise and resubmit")
        return

    if decision == 'approve_with_recommendations':
        print(f"\n✓ Plan approved with {len(recommendations)} recommendations")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")

        # Optional: Trigger human checkpoint for critical tasks
        # (Phase 2.6 in workflow)

    elif decision == 'auto_approve':
        print("\n✓ Plan auto-approved - proceeding to implementation")

    # Step 11: Track final outcome
    metrics.track_outcome(
        task_id=task_id,
        decision=decision,
        human_override=False,
        duration_seconds=312.7,
        final_status='approved',
        stack=stack
    )
    print("✓ Outcome metric tracked")

    print("\n✓ Proceeding to Phase 3: Implementation")


if __name__ == '__main__':
    try:
        # Run all examples
        example_configuration_usage()
        example_metrics_tracking()
        example_dashboard_visualization()
        example_integration_workflow()

        print("\n" + "=" * 80)
        print("✅ All examples completed successfully!")
        print("=" * 80)

    except ImportError as e:
        print(f"\n✗ Import error: {e}")
        print("\nPlease ensure pydantic is installed:")
        print("  pip install pydantic")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
