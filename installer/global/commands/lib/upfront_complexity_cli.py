#!/usr/bin/env python3
"""
CLI handler for upfront complexity evaluation.

This module provides the command-line interface for evaluating task complexity
from requirements text and generating task splitting recommendations.

Usage:
    python3 upfront_complexity_cli.py --task-id TASK-XXX --title "Task title" \
        --description "Requirements text" [--interactive]
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Handle imports for both direct execution and import as module
try:
    from .upfront_complexity_adapter import UpfrontComplexityAdapter
    from .task_split_advisor import TaskSplitAdvisor
    from .complexity_calculator import ComplexityCalculator
    from .complexity_factors import DEFAULT_FACTORS
except ImportError:
    # Add lib directory to path if not already there
    lib_dir = Path(__file__).parent
    if str(lib_dir) not in sys.path:
        sys.path.insert(0, str(lib_dir))

    from upfront_complexity_adapter import UpfrontComplexityAdapter
    from task_split_advisor import TaskSplitAdvisor
    from complexity_calculator import ComplexityCalculator
    from complexity_factors import DEFAULT_FACTORS


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Evaluate task complexity from requirements and recommend splitting",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--task-id",
        required=True,
        help="Task identifier (e.g., TASK-005)"
    )

    parser.add_argument(
        "--title",
        required=True,
        help="Task title"
    )

    parser.add_argument(
        "--description",
        help="Requirements text (inline)"
    )

    parser.add_argument(
        "--requirements-file",
        type=Path,
        help="Path to requirements file (alternative to --description)"
    )

    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Enable interactive split decision prompt"
    )

    parser.add_argument(
        "--json-only",
        action="store_true",
        help="Output only JSON (no interactive prompts or formatting)"
    )

    parser.add_argument(
        "--split-threshold",
        type=int,
        default=7,
        help="Complexity score threshold for split recommendations (default: 7)"
    )

    parser.add_argument(
        "--technology-stack",
        default="unknown",
        help="Technology stack for context (e.g., python, react, typescript)"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )

    return parser.parse_args()


def load_requirements_text(args: argparse.Namespace) -> str:
    """Load requirements text from file or inline argument.

    Args:
        args: Parsed command-line arguments

    Returns:
        Requirements text

    Raises:
        ValueError: If neither description nor requirements file provided
    """
    if args.description:
        return args.description

    if args.requirements_file:
        if not args.requirements_file.exists():
            raise FileNotFoundError(f"Requirements file not found: {args.requirements_file}")
        return args.requirements_file.read_text()

    raise ValueError("Either --description or --requirements-file must be provided")


def build_metadata(args: argparse.Namespace) -> Dict[str, Any]:
    """Build task metadata from arguments.

    Args:
        args: Parsed command-line arguments

    Returns:
        Metadata dictionary
    """
    return {
        "task_id": args.task_id,
        "title": args.title,
        "technology_stack": args.technology_stack,
        "source": "upfront-evaluation"
    }


def evaluate_complexity(args: argparse.Namespace) -> Dict[str, Any]:
    """Main complexity evaluation workflow.

    Args:
        args: Parsed command-line arguments

    Returns:
        Evaluation results dictionary

    Raises:
        Exception: If evaluation fails
    """
    try:
        # Load requirements
        requirements_text = load_requirements_text(args)
        logger.info(f"Loaded requirements ({len(requirements_text)} characters)")

        # Initialize TASK-003A components
        calculator = ComplexityCalculator(factors=DEFAULT_FACTORS)
        adapter = UpfrontComplexityAdapter(calculator)
        advisor = TaskSplitAdvisor(split_threshold=args.split_threshold)

        logger.info("Initialized complexity evaluation components")

        # Build metadata
        metadata = build_metadata(args)

        # Evaluate complexity (delegates to TASK-003A)
        complexity_score = adapter.evaluate_requirements(
            requirements_text=requirements_text,
            task_id=args.task_id,
            metadata=metadata
        )

        logger.info(
            f"Complexity evaluated: score={complexity_score.total_score}, "
            f"mode={complexity_score.review_mode.value}"
        )

        # Generate split recommendation
        recommendation = advisor.recommend_split(complexity_score, requirements_text)

        if recommendation:
            logger.info(
                f"Split recommended: {recommendation.recommended_task_count} tasks, "
                f"strategy={recommendation.split_strategy}"
            )
        else:
            logger.info("No split recommended (complexity below threshold)")

        # Build result
        result = {
            "task_id": args.task_id,
            "title": args.title,
            "complexity_score": complexity_score.total_score,
            "review_mode": complexity_score.review_mode.value,
            "requires_review": complexity_score.requires_human_review,
            "forced_triggers": [t.value for t in complexity_score.forced_review_triggers],
            "split_recommended": recommendation is not None,
            "recommendation": recommendation.to_dict() if recommendation else None,
            "factor_scores": [
                {
                    "name": fs.factor_name,
                    "score": fs.score,
                    "max_score": fs.max_score,
                    "justification": fs.justification
                }
                for fs in complexity_score.factor_scores
            ]
        }

        return result

    except Exception as e:
        logger.error(f"Complexity evaluation failed: {e}", exc_info=True)
        raise


def handle_interactive_decision(recommendation: Dict[str, Any]) -> str:
    """Handle interactive split decision prompt.

    Args:
        recommendation: Split recommendation dictionary

    Returns:
        User decision: "create", "split", "modify", or "abort"
    """
    print("\n" + "=" * 70)
    print("TASK COMPLEXITY ANALYSIS")
    print("=" * 70)

    print(f"\nComplexity Score: {recommendation['complexity_score']}/10")
    print(f"Review Mode: {recommendation['review_mode']}")
    print(f"Split Urgency: {recommendation.get('split_urgency', 'N/A')}")

    if recommendation.get('forced_triggers'):
        print(f"\nForce-Review Triggers:")
        for trigger in recommendation['forced_triggers']:
            print(f"  - {trigger}")

    rec_data = recommendation.get('recommendation')
    if rec_data:
        print(f"\n{'-' * 70}")
        print("SPLIT RECOMMENDATION")
        print(f"{'-' * 70}")
        print(f"\nStrategy: {rec_data['split_strategy']}")
        print(f"Recommended Tasks: {rec_data['recommended_task_count']}")
        print(f"\nReasoning:")
        print(f"  {rec_data['reasoning']}")

        print(f"\nSuggested Subtasks:")
        for i, split in enumerate(rec_data['suggested_splits'], 1):
            print(f"\n  {i}. {split['title']}")
            print(f"     Description: {split['description']}")
            print(f"     Est. Complexity: {split['estimated_complexity']}/10")
            if split.get('dependencies'):
                print(f"     Dependencies: {', '.join(split['dependencies'])}")

    print(f"\n{'-' * 70}")
    print("DECISION OPTIONS")
    print(f"{'-' * 70}")
    print("  [C]reate - Create task as-is (single task)")
    print("  [S]plit  - Accept split recommendation (create subtasks)")
    print("  [M]odify - Modify complexity threshold or strategy")
    print("  [A]bort  - Cancel task creation")

    while True:
        choice = input("\nYour decision [C/S/M/A]: ").strip().upper()
        if choice in ["C", "S", "M", "A"]:
            decision_map = {
                "C": "create",
                "S": "split",
                "M": "modify",
                "A": "abort"
            }
            decision = decision_map[choice]
            print(f"\nDecision recorded: {decision}")
            return decision
        else:
            print("Invalid choice. Please enter C, S, M, or A.")


def format_json_output(result: Dict[str, Any]) -> str:
    """Format result as JSON string.

    Args:
        result: Evaluation result dictionary

    Returns:
        JSON string
    """
    return json.dumps(result, indent=2, default=str)


def main():
    """Main entry point for CLI."""
    try:
        # Parse arguments
        args = parse_arguments()

        # Configure logging level
        if args.debug:
            logging.getLogger().setLevel(logging.DEBUG)

        # Evaluate complexity
        result = evaluate_complexity(args)

        # Handle output mode
        if args.json_only:
            # JSON-only mode: print and exit
            print(format_json_output(result))
            sys.exit(0)

        # Interactive mode
        if args.interactive and result.get("split_recommended"):
            decision = handle_interactive_decision(result)
            result["user_decision"] = decision

            # Output final result with decision
            print("\n" + "=" * 70)
            print("FINAL RESULT")
            print("=" * 70)
            print(format_json_output(result))
        else:
            # Non-interactive mode: just print JSON
            print(format_json_output(result))

        # Exit with appropriate code
        if result.get("user_decision") == "abort":
            sys.exit(1)
        else:
            sys.exit(0)

    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=args.debug if 'args' in locals() else False)
        sys.exit(1)


if __name__ == "__main__":
    main()
