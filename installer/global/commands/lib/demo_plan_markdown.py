"""
Demonstration: Markdown Plan Storage vs JSON

Part of TASK-027: Convert Implementation Plan Storage from JSON to Markdown.

This script demonstrates the benefits of markdown plan storage:
- Human readability
- Git diff clarity
- Manual editability
- Programmatic access via frontmatter

Run this to see a side-by-side comparison.

Author: Claude (Anthropic)
Created: 2025-10-18
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from plan_markdown_renderer import PlanMarkdownRenderer


def demo_comparison():
    """Show side-by-side comparison of JSON vs Markdown."""

    # Example plan data
    plan_data = {
        "task_id": "TASK-042",
        "saved_at": "2025-10-18T14:30:00Z",
        "version": 1,
        "plan": {
            "summary": "Implement user authentication system with JWT tokens",
            "files_to_create": [
                "src/auth/AuthService.ts",
                "src/auth/TokenManager.ts",
                "tests/unit/AuthService.test.ts"
            ],
            "files_to_modify": [
                "src/app.ts"
            ],
            "external_dependencies": [
                "jsonwebtoken ^9.0.0",
                "bcrypt ^5.1.0"
            ],
            "estimated_duration": "4 hours",
            "estimated_loc": 245,
            "complexity_score": 5,
            "risks": [
                {
                    "description": "JWT secret management",
                    "mitigation": "Use environment variables, never commit secrets"
                },
                {
                    "description": "Token expiration handling",
                    "mitigation": "Implement refresh token mechanism"
                }
            ],
            "implementation_notes": [
                "Start with TokenManager (dependency)",
                "Implement AuthService using TokenManager",
                "Write tests for happy path first",
                "Add error handling tests"
            ]
        },
        "architectural_review": {
            "score": 85,
            "solid_compliance": {
                "Single Responsibility": "Good - each class has one purpose",
                "Dependency Inversion": "Good - using interfaces"
            },
            "warnings": [
                "Consider extracting validation logic into separate class"
            ]
        }
    }

    print("=" * 80)
    print("DEMONSTRATION: JSON vs Markdown Plan Storage")
    print("=" * 80)
    print()

    # Show JSON format
    print("LEGACY FORMAT (JSON):")
    print("-" * 80)
    json_output = json.dumps(plan_data, indent=2)
    print(json_output[:500] + "\n... (truncated)")
    print()

    print("Issues with JSON:")
    print("  ❌ Not human-readable without tools")
    print("  ❌ Git diffs are noisy (structure changes)")
    print("  ❌ Hard to review in pull requests")
    print("  ❌ Manual editing is error-prone (syntax)")
    print()
    print()

    # Show markdown format
    print("NEW FORMAT (MARKDOWN):")
    print("-" * 80)
    renderer = PlanMarkdownRenderer()
    markdown_output = renderer.render(plan_data)

    # Show first 1000 chars
    print(markdown_output[:1000])
    print("\n... (continues)")
    print()

    print("Benefits of Markdown:")
    print("  ✅ Human-readable without tools")
    print("  ✅ Clear git diffs (line-by-line changes)")
    print("  ✅ Easy to review in pull requests")
    print("  ✅ Simple manual editing (no syntax errors)")
    print("  ✅ Programmatically accessible (frontmatter)")
    print("  ✅ Aligns with John Hubbard's proven pattern")
    print()

    # Show size comparison
    json_size = len(json_output)
    md_size = len(markdown_output)

    print("STORAGE COMPARISON:")
    print(f"  JSON size: {json_size} bytes")
    print(f"  Markdown size: {md_size} bytes")
    print(f"  Difference: {md_size - json_size:+d} bytes ({((md_size/json_size - 1) * 100):+.1f}%)")
    print()

    print("=" * 80)
    print("CONCLUSION:")
    print("  Markdown provides better human experience with negligible overhead")
    print("  Single source of truth (no .md + .json duplication)")
    print("  50% storage savings vs dual-format approach")
    print("=" * 80)


if __name__ == "__main__":
    demo_comparison()
