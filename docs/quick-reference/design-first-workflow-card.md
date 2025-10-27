# Design-First Workflow Guide

## Overview

Design-first workflow splits task execution into separate design approval and implementation sessions. This is optimal for complex tasks (≥7/10), high-risk changes, or when different team members handle design and implementation.

## Quick Reference

### Workflow Flags
| Flag | Purpose | Phases | End State |
|------|---------|--------|-----------|
| `--design-only` | Design approval | 1-2.8 | DESIGN_APPROVED |
| `--implement-only` | Implementation | 3-5.5 | IN_REVIEW or BLOCKED |
| (no flags) | Complete workflow | 1-5.5 | IN_REVIEW or BLOCKED |

### State Machine
```
BACKLOG
   │
   ├─(task-work)──────────────────→ IN_PROGRESS ──→ IN_REVIEW
   │                                      ↓
   │                                  BLOCKED
   │
   └─(task-work --design-only)─→ DESIGN_APPROVED
                                      │
                                      └─(task-work --implement-only)─→ IN_PROGRESS ──→ IN_REVIEW
                                                                                ↓
                                                                            BLOCKED
```

### Prerequisites
| Flag | Required State | Required Artifacts |
|------|---------------|-------------------|
| `--design-only` | BACKLOG or IN_PROGRESS | None |
| `--implement-only` | DESIGN_APPROVED | Saved implementation plan |

## Decision Guide

### When to Use --design-only

**Use When** (any of these apply):
- Task complexity ≥ 7 (system recommends)
- High-risk changes (security, breaking changes, schema migrations)
- Multiple team members involved (architect designs, developer implements)
- Unclear requirements need design exploration
- Multi-day task (design Day 1, implement Day 2+)
- Team wants to review plan before committing to implementation
- Experimenting with different architectural approaches

**Benefits**:
- Catches design issues before implementation (saves 40-50% rework time)
- Enables architect-developer collaboration
- Allows design review without code commitment
- Provides clear implementation roadmap
- Supports iterative refinement of approach

### When to Use --implement-only

**Use When** (all must be true):
- Task is in DESIGN_APPROVED state
- Approved design exists (saved plan from --design-only)
- Ready to begin implementation
- Same or different person than who designed

**Benefits**:
- Skips design phases (faster implementation start)
- Uses pre-approved architectural decisions
- Clear implementation path from saved plan
- Supports handoff between team members

### When to Use Standard Workflow (No Flags)

**Use When**:
- Task complexity ≤ 6 (simple to medium)
- Straightforward implementation with clear approach
- Single developer handling both design and implementation
- Design and implementation can happen in same session
- Low-risk changes

**Benefits**:
- Fastest path from start to finish
- Automatic complexity-based checkpoints
- No manual state transitions needed
- Single command execution

## Examples

### Example 1: Architect-Developer Handoff
```bash
# Day 1: Architect creates design
/task-work TASK-042 --design-only

# Output:
Phase 1-2: Requirements and planning
Phase 2.5B: Architectural review (Score: 85/100)
Phase 2.7: Complexity (7/10 - Complex)
Phase 2.8: Human checkpoint
  [A]pprove selected

✅ Design approved
Plan saved: docs/state/TASK-042/implementation_plan.md
Task state: BACKLOG → DESIGN_APPROVED

# Day 2: Developer implements from plan
/task-work TASK-042 --implement-only

# Output:
Loading approved design...
Architectural score: 85/100
Complexity: 7/10
Files to create: 5

Phase 3: Implementation (using saved plan)
Phase 4: Testing
Phase 4.5: Fix loop (all tests pass)
Phase 5: Code review
Phase 5.5: Plan audit (approved)

✅ Task complete
Task state: DESIGN_APPROVED → IN_REVIEW
```

### Example 2: Multi-Day Complex Task
```bash
# Monday: Design phase (1 hour)
/task-work TASK-050 --design-only

# System evaluates complexity: 8/10
# Architect reviews plan at Phase 2.8 checkpoint
# Selects [M]odify to adjust file list
# Approves modified plan
# Task moved to DESIGN_APPROVED

# Tuesday-Thursday: Implementation (2 days)
/task-work TASK-050 --implement-only

# Loads saved plan from Monday
# Implements all phases 3-5.5
# All tests pass after 2 fix attempts
# Plan audit: 3 extra files detected (variance: +15%)
# Selects [A]pprove (variance acceptable)
# Task moved to IN_REVIEW
```

### Example 3: Security-Sensitive Change
```bash
# Security task requires design approval first
/task-work TASK-060 --design-only

# Phase 2.5B detects security keywords
# Complexity: 9/10 (very complex)
# Force trigger: Security-sensitive
# Phase 2.8: FULL_REQUIRED checkpoint

# Architect reviews:
# - Encryption algorithms
# - Key management approach
# - Security test strategy

# Selects [A]pprove after validation

# Later: Separate implementation session
/task-work TASK-060 --implement-only

# Security tests must all pass (zero tolerance)
# Phase 4.5 ensures 100% pass rate
# Plan audit verifies no security shortcuts taken
```

### Example 4: Design Iteration
```bash
# First attempt: Initial design
/task-work TASK-070 --design-only

# Architectural review: 55/100 (REJECTED)
# Issues: Too many responsibilities, low cohesion
# Phase 2.8: Selects [R]evise

# System loops back to Phase 2 with feedback
# Generates revised plan
# Re-runs architectural review: 82/100 (APPROVED)
# Selects [A]pprove

# Implementation uses refined design
/task-work TASK-070 --implement-only
```

### Example 5: Flag Validation Error
```bash
# Attempting --implement-only on wrong state
/task-work TASK-080 --implement-only

# Error:
❌ Cannot execute --implement-only workflow

Task TASK-080 is in 'backlog' state
Required state: design_approved

To approve design first, run:
  /task-work TASK-080 --design-only

Or run complete workflow without flags:
  /task-work TASK-080
```

## Common Patterns

### Pattern 1: Experienced Developer (Simple Tasks)
```bash
# Skip design phase for straightforward tasks
/task-work TASK-XXX  # Standard workflow, auto-proceed for complexity 1-3
```

### Pattern 2: Junior Developer (Learning)
```bash
# Review plan before implementation
/task-work TASK-XXX --design-only  # Get design approval
# Review saved plan in docs/state/TASK-XXX/
/task-work TASK-XXX --implement-only  # Implement approved design
```

### Pattern 3: Team Lead (Delegation)
```bash
# Lead creates design
/task-work TASK-XXX --design-only  # Architect approves at checkpoint

# Developer implements later
/task-work TASK-XXX --implement-only  # Uses lead's approved plan
```

### Pattern 4: High-Risk Production Change
```bash
# Require design approval for all production changes
/task-work TASK-XXX --design-only
# Multiple stakeholders review plan
# Approval given after validation
/task-work TASK-XXX --implement-only
# Implementation follows approved design exactly
```

## Design Metadata

### Saved Plan Contents
```
docs/state/TASK-XXX/
├── implementation_plan.md (human-readable)
├── implementation_plan.json (machine-readable)
└── complexity_score.json (evaluation results)
```

### Task Frontmatter (--design-only)
```yaml
design:
  status: approved
  approved_at: "2025-10-24T14:30:00Z"
  approved_by: "human"
  implementation_plan_version: "v1"
  architectural_review_score: 85
  complexity_score: 7
  design_session_id: "design-TASK-042-20251024143000"
```

## See Also

**Full Documentation**:
- Task work command: `installer/global/commands/task-work.md` (Phase 2.9)
- Design-first guide: `docs/guides/design-first-workflow.md`
- Plan persistence: `installer/global/commands/lib/plan_persistence.py`

**Related Cards**:
- [task-work-cheat-sheet.md](task-work-cheat-sheet.md) - Complete workflow reference
- [complexity-guide.md](complexity-guide.md) - When to use design-first
- [quality-gates-card.md](quality-gates-card.md) - Implementation quality standards
