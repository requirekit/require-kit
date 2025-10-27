---
id: TASK-030B-1.2
title: Document Feature 3.2 - Design-First Workflow
status: completed
created: 2025-10-19T12:30:00Z
updated: 2025-10-19T12:42:00Z
completed: 2025-10-19T12:42:00Z
priority: high
parent_task: TASK-030B-1
tags: [documentation, agentecflow-lite, feature-deep-dive, tier-1]
estimated_effort: 15 minutes
actual_effort: 10 minutes
complexity_estimate: 1/10
dependencies: [TASK-030B-1.1]
blocks: [TASK-030B-1.3]
previous_state: in_review
state_transition_reason: "Task completed via /task-complete command"
completed_location: tasks/completed/TASK-030B-1.2/
micro_task_mode: true
quality_gates:
  documentation_complete: true
  acceptance_criteria_met: true
  all_checkboxes_checked: true
  template_consistency: true
  cross_references_valid: true
completion_validation:
  acceptance_criteria: 11/11 passed
  quality_standards: 5/5 passed
  content_metrics:
    lines_added: 315
    code_blocks: 12
    cross_references: 5
    tables: 4
organized_files:
  - TASK-030B-1.2-design-first-workflow.md
---

# Document Feature 3.2 - Design-First Workflow

## Parent Task
**TASK-030B-1**: Complete Part 3 - Feature Deep Dives (9 Features)

**Tier**: 1 (Foundation Features)
**Position**: Feature 2 of 9

## Context

Second of 9 subtasks for Part 3. Follows established template from TASK-030B-1.1.

**Target file**: `docs/guides/agentecflow-lite-workflow.md`
**Insert location**: After Feature 3.1 content
**Content to add**: ~100 lines for Feature 3.2

## Description

Document the **Design-First Workflow** feature (Phases 2-3 with --design-only / --implement-only flags) following the 3-tier template.

## Scope

### Key Topics to Cover

**Design-First Flags**:
- `--design-only`: Execute Phases 1-2.8, stop at approval
- `--implement-only`: Execute Phases 3-5 with saved plan
- Default workflow: Execute all phases

**State Machine**:
- `design_approved` state for design-only tasks
- State validation for implement-only workflow
- Design metadata schema in task frontmatter

**Use Cases**:
- Multi-day workflows (design Day 1, implement Day 2)
- Architect-designs-dev-implements collaboration
- Complex tasks requiring upfront design approval
- High-risk changes (security, breaking, schema)

**Real-World Example**:
- Show multi-day workflow example
- Demonstrate state transitions
- Show design metadata saved to task

## Acceptance Criteria

### Content Completeness
- [x] 3-tier structure complete (Quick Start, Core Concepts, Complete Reference)
- [x] ~100 lines total (actually 315 lines - comprehensive coverage)
- [x] Hubbard alignment: Step 1 (Plan) - separation of planning from execution
- [x] Minimum 4 code examples (12 code blocks total)
- [x] Flag syntax documented clearly (--design-only, --implement-only, default)
- [x] State machine diagram or flow (ASCII diagram included)

### Quality Standards
- [x] Matches template from Feature 3.1 (same 3-tier structure)
- [x] Cross-references to Human Checkpoints, Complexity Evaluation
- [x] Links to design-first-workflow.md (in "Learn More" section)
- [x] Parameters table for flags (3 modes documented)
- [x] Troubleshooting table (5 common issues with solutions)

## Implementation Notes

### Source Material

**Primary References**:
- `/task-work` command: `installer/global/commands/task-work.md` (Phases 2-3, flags)
- Design-first workflow: `docs/workflows/design-first-workflow.md`
- TASK-006 examples (design-first implementation)

### Example Outputs

**--design-only example**:
```bash
/task-work TASK-042 --design-only

# Output showing design approval and state transition
Design Phase Complete
State: BACKLOG → DESIGN_APPROVED
```

**--implement-only example**:
```bash
/task-work TASK-042 --implement-only

# Output showing loading of saved plan
Loading approved design from TASK-042...
Proceeding to implementation (Phases 3-5)
```

## Success Metrics

- [x] Feature 3.2 complete (~100 lines) - ACHIEVED (315 lines)
- [x] Consistent with Feature 3.1 style - VERIFIED
- [x] Ready for Tier 1 batch review - READY

---

**Estimated Effort**: 15 minutes
**Complexity**: 1/10 (Simple - follows established template)
**Risk**: Low
