"""
Demo script for checkpoint_display module.

Quick visual validation of the display_phase28_checkpoint function.
Run with: python tests/unit/test_checkpoint_display_demo.py
"""

import json
import tempfile
from pathlib import Path
import sys

# Add lib directory to path for imports
lib_path = Path(__file__).parent.parent.parent / "installer" / "global" / "commands" / "lib"
sys.path.insert(0, str(lib_path))

from checkpoint_display import display_phase28_checkpoint


def demo_simple_plan():
    """Demo with simple plan at medium complexity."""
    print("\n" + "=" * 80)
    print("DEMO 1: Simple Plan (Complexity 5)")
    print("=" * 80 + "\n")

    # Create temporary plan file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        plan_data = {
            "task_id": "TASK-DEMO-001",
            "saved_at": "2025-10-18T10:00:00",
            "version": 1,
            "plan": {
                "files_to_create": [
                    "installer/global/commands/lib/checkpoint_display.py",
                    "tests/unit/test_checkpoint_display.py"
                ],
                "external_dependencies": ["pytest"],
                "estimated_duration": "2 hours",
                "estimated_loc": 150,
                "complexity_score": 5,
                "test_summary": "Comprehensive unit tests for all dataclasses and formatting",
                "risks": [
                    {
                        "description": "Integration with existing plan_persistence module",
                        "level": "medium",
                        "mitigation": "Thorough testing with existing infrastructure"
                    }
                ]
            }
        }
        json.dump(plan_data, f)
        plan_path = Path(f.name)

    # Display checkpoint
    display_phase28_checkpoint("TASK-DEMO-001", complexity_score=5, plan_path=plan_path)

    # Cleanup
    plan_path.unlink()


def demo_complex_plan():
    """Demo with complex plan at high complexity."""
    print("\n" + "=" * 80)
    print("DEMO 2: Complex Plan (Complexity 8)")
    print("=" * 80 + "\n")

    # Create temporary plan file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        plan_data = {
            "task_id": "TASK-DEMO-002",
            "saved_at": "2025-10-18T10:00:00",
            "version": 1,
            "plan": {
                "files_to_create": [
                    "src/authentication/oauth_provider.py",
                    "src/authentication/jwt_handler.py",
                    "src/authentication/session_manager.py",
                    "src/database/user_repository.py",
                    "src/api/auth_endpoints.py",
                    "tests/unit/test_oauth.py",
                    "tests/unit/test_jwt.py",
                    "tests/integration/test_auth_flow.py"
                ],
                "files_to_modify": [
                    "src/config/settings.py",
                    "src/api/routes.py"
                ],
                "external_dependencies": [
                    {"name": "authlib", "version": "1.2.0", "purpose": "OAuth2 implementation"},
                    {"name": "pyjwt", "version": "2.6.0", "purpose": "JWT token handling"},
                    {"name": "sqlalchemy", "version": "2.0.0", "purpose": "Database ORM"}
                ],
                "estimated_duration": "8 hours",
                "estimated_loc": 500,
                "complexity_score": 8,
                "test_summary": "Unit tests for each component, integration tests for full auth flow",
                "phases": [
                    "Phase 1: OAuth provider setup",
                    "Phase 2: JWT token generation",
                    "Phase 3: Session management",
                    "Phase 4: API endpoints"
                ],
                "risks": [
                    {
                        "description": "Security vulnerability in token handling",
                        "level": "high",
                        "mitigation": "Security audit and penetration testing"
                    },
                    {
                        "description": "Database schema changes required",
                        "level": "high",
                        "mitigation": "Run migrations in transaction with rollback capability"
                    },
                    {
                        "description": "External OAuth provider rate limiting",
                        "level": "medium",
                        "mitigation": "Implement exponential backoff and caching"
                    }
                ]
            }
        }
        json.dump(plan_data, f)
        plan_path = Path(f.name)

    # Display checkpoint
    display_phase28_checkpoint("TASK-DEMO-002", complexity_score=8, plan_path=plan_path)

    # Cleanup
    plan_path.unlink()


def demo_missing_plan():
    """Demo with missing plan (high complexity)."""
    print("\n" + "=" * 80)
    print("DEMO 3: Missing Plan (Complexity 8)")
    print("=" * 80 + "\n")

    display_phase28_checkpoint("TASK-MISSING", complexity_score=8)


def demo_minimal_plan():
    """Demo with minimal plan (low complexity)."""
    print("\n" + "=" * 80)
    print("DEMO 4: Minimal Plan (Complexity 2)")
    print("=" * 80 + "\n")

    # Create temporary plan file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        plan_data = {
            "task_id": "TASK-DEMO-004",
            "saved_at": "2025-10-18T10:00:00",
            "version": 1,
            "plan": {
                "files_to_create": ["src/simple_fix.py"]
            }
        }
        json.dump(plan_data, f)
        plan_path = Path(f.name)

    # Display checkpoint
    display_phase28_checkpoint("TASK-DEMO-004", complexity_score=2, plan_path=plan_path)

    # Cleanup
    plan_path.unlink()


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("CHECKPOINT DISPLAY MODULE - VISUAL DEMO")
    print("=" * 80)

    demo_simple_plan()
    demo_complex_plan()
    demo_missing_plan()
    demo_minimal_plan()

    print("\n" + "=" * 80)
    print("DEMO COMPLETE")
    print("=" * 80 + "\n")
