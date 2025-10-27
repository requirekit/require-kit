# Task Work Command - Cheat Sheet

## Overview

The `/task-work` command executes the complete implementation workflow with automated quality gates, architectural review, and test enforcement. This is the primary command for implementing tasks in Agentecflow Lite.

## Quick Reference

### Command Syntax
```bash
/task-work TASK-XXX [flags]
```

### Available Flags
| Flag | Purpose | Phases Executed |
|------|---------|-----------------|
| (none) | Standard workflow | Phases 1-5.5 (all phases) |
| `--design-only` | Design approval only | Phases 1-2.8 (stop at checkpoint) |
| `--implement-only` | Implementation only | Phases 3-5.5 (use saved plan) |
| `--micro` | Trivial task fast-track | Phases 1, 3, 4, 4.5, 5 (simplified) |

### Workflow Phases
```
Phase 1: Load Task Context
Phase 2: Implementation Planning
Phase 2.5B: Architectural Review (SOLID/DRY/YAGNI evaluation)
Phase 2.7: Complexity Evaluation (routing decision)
Phase 2.8: Human Checkpoint (complexity-based)
    ↓
Phase 3: Implementation
Phase 4: Testing (with compilation check)
Phase 4.5: Fix Loop (up to 3 attempts, zero tolerance)
Phase 5: Code Review
Phase 5.5: Plan Audit (scope creep detection)
```

### State Transitions
```
BACKLOG ──(task-work)───→ IN_PROGRESS ──(tests pass)──→ IN_REVIEW
   │                            ↓
   │                       BLOCKED (tests fail after 3 attempts)
   │
   └─(task-work --design-only)─→ DESIGN_APPROVED
                                      │
                                      └─(task-work --implement-only)─→ IN_PROGRESS
```

### Quality Gates (Zero Tolerance)
| Gate | Threshold | Action if Failed |
|------|-----------|------------------|
| Compilation | 100% success | BLOCKED (no tests run) |
| Tests Pass | 100% (all pass) | Fix loop (up to 3 attempts) |
| Coverage | ≥80% lines | Request more tests (Phase 4) |
| Architectural Review | ≥60/100 | Human checkpoint (Phase 2.8) |

## Decision Guide

### When to Use --design-only
Use when:
- Task complexity ≥ 7 (system recommends)
- High-risk changes (security, breaking changes, schema)
- Multiple team members (architect designs, developer implements)
- Unclear requirements need design exploration
- Multi-day task (design Day 1, implement Day 2)

### When to Use --implement-only
Use when:
- Task is in `design_approved` state
- Approved design exists from --design-only run
- Different person implementing than who designed
- Continuing work after design approval

### When to Use --micro
Use when (ALL must be true):
- Single file modification (or docs-only)
- Complexity 1/10 (trivial change)
- No high-risk keywords (security, schema, API)
- Estimated time <1 hour

Auto-detection suggests --micro when task qualifies (10-second timeout).

## Examples

### Standard Workflow (Default)
```bash
# Complete workflow with complexity-based routing
/task-work TASK-042

# System executes all phases:
# - Phases 1-2.8: Planning and design
# - Phase 2.8 checkpoint: Auto-proceed (1-3), optional (4-6), mandatory (7-10)
# - Phases 3-5.5: Implementation, testing, review, audit
```

### Design-First Workflow
```bash
# Step 1: Design approval (complexity 7+)
/task-work TASK-042 --design-only
# → Stops at Phase 2.8 checkpoint
# → Saves plan to docs/state/TASK-042/implementation_plan.md
# → Moves task to DESIGN_APPROVED state

# Step 2: Implementation (later session)
/task-work TASK-042 --implement-only
# → Loads saved plan
# → Executes Phases 3-5.5
# → Moves to IN_REVIEW or BLOCKED based on tests
```

### Micro-Task Workflow
```bash
# Typo fix or documentation update
/task-work TASK-047 --micro

# Simplified workflow:
# Phase 1: Load context
# Phase 3: Quick implementation
# Phase 4: Compilation + tests (no coverage)
# Phase 4.5: Fix loop (1 attempt max)
# Phase 5: Lint only (skip SOLID/DRY review)
# Duration: ~3 minutes vs 15+ minutes
```

### Error Recovery
```bash
# Task blocked with test failures
/task-work TASK-042
# → 3 fix attempts exhausted
# → Task moved to BLOCKED state

# Fix issues manually, then retry
/task-work TASK-042
# → Resumes from Phase 3 (implementation)
# → Re-runs tests with fresh fix loop
```

## Common Errors

### Error: Task Not in design_approved State
```
Cannot execute --implement-only workflow
Task TASK-042 is in 'backlog' state
Required state: design_approved

Solution: Run /task-work TASK-042 --design-only first
```

### Error: Flag Conflict
```
Cannot use both --design-only and --implement-only flags together

Solution: Choose one workflow mode or use standard (no flags)
```

### Error: Micro-Task Escalation
```
Task does not qualify as micro-task:
  - Complexity: 5/10 (threshold: 1/10)
  - Multiple files detected

Solution: Use standard workflow (remove --micro flag)
```

### Error: Tests Still Failing After 3 Attempts
```
BLOCKED: 2 test failures remain after 3 fix attempts

Solution:
1. Review test failure logs in task file
2. Fix issues manually
3. Re-run /task-work TASK-042
```

## See Also

**Full Documentation**:
- Complete specification: `installer/global/commands/task-work.md`
- Architectural review: `installer/global/agents/architectural-reviewer.md`
- Test enforcement: `installer/global/agents/test-orchestrator.md`

**Related Workflows**:
- Design-first workflow: `docs/guides/design-first-workflow.md`
- Complexity management: `docs/guides/complexity-management-workflow.md`
- Iterative refinement: `docs/guides/iterative-refinement-guide.md`

**Related Cards**:
- [complexity-guide.md](complexity-guide.md) - Complexity scoring and breakdown
- [quality-gates-card.md](quality-gates-card.md) - Quality gate details
- [design-first-workflow-card.md](design-first-workflow-card.md) - Design-first patterns
