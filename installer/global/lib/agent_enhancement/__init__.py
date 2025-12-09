"""
Agent Enhancement Package

Progressive disclosure infrastructure for RequireKit agent files.

TASK-PD-RK02: Copied from GuardKit for RequireKit use.
"""

from .models import AgentEnhancement, SplitContent, EnhancementResult
from .applier import EnhancementApplier

__all__ = [
    'AgentEnhancement',
    'SplitContent',
    'EnhancementResult',
    'EnhancementApplier',
]
