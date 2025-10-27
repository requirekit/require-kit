"""Default configuration values for plan review system."""
from typing import Dict, Any


DEFAULT_CONFIG: Dict[str, Any] = {
    "enabled": True,
    "default_mode": "auto",  # auto, always, never

    "thresholds": {
        "default": {
            "auto_approve": 80,
            "approve_with_recommendations": 60,
            "reject": 0
        },
        # Stack-specific overrides
        "stack_overrides": {
            "python": {
                "auto_approve": 80,
                "approve_with_recommendations": 60,
                "reject": 0
            },
            "typescript": {
                "auto_approve": 80,
                "approve_with_recommendations": 60,
                "reject": 0
            },
            "react": {
                "auto_approve": 80,
                "approve_with_recommendations": 60,
                "reject": 0
            },
            "dotnet": {
                "auto_approve": 80,
                "approve_with_recommendations": 60,
                "reject": 0
            }
        }
    },

    "force_triggers": {
        "min_complexity": 30,  # Force review if complexity >= 30
        "critical_keywords": [
            "security", "authentication", "authorization", "payment",
            "database", "migration", "schema", "api", "integration"
        ]
    },

    "timeouts": {
        "architectural_review_seconds": 300,  # 5 minutes
        "human_checkpoint_seconds": 1800  # 30 minutes
    },

    "weights": {
        "solid_principles": 0.30,
        "dry_principle": 0.25,
        "yagni_principle": 0.25,
        "testability": 0.20
    },

    "metrics": {
        "enabled": True,
        "retention_days": 90,
        "output_format": "terminal"  # Only terminal for MVP (no HTML)
    }
}
