---
id: TASK-DOC-026
title: Document when to use /feature-generate-tasks vs /feature-plan
status: completed
task_type: implementation
created: 2025-12-09T14:05:00Z
updated: 2025-12-09T14:35:00Z
completed: 2025-12-09T14:35:00Z
completed_location: tasks/completed/TASK-DOC-026/
priority: normal
tags: [documentation, command-clarification, integration-guide]
epic: null
feature: null
requirements: []
related_tasks: [TASK-REV-025]
external_ids:
  epic_jira: null
  epic_linear: null
  jira: null
  linear: null
bdd_scenarios: []
test_results:
  status: pending
  coverage: null
  last_run: null
---

# Task: Document when to use /feature-generate-tasks vs /feature-plan

## Context

Created from review TASK-REV-025 findings. Users may be confused about when to use `/feature-generate-tasks` (require-kit) vs `/feature-plan` (guardkit). Documentation should clarify these are complementary commands with different purposes.

## Source Review

- **Review Task**: TASK-REV-025
- **Decision**: Keep both commands (complementary)
- **Report**: [.claude/reviews/TASK-REV-025-feature-generate-tasks-review-report.md](../../.claude/reviews/TASK-REV-025-feature-generate-tasks-review-report.md)

## Implementation Scope

Add the following documentation to `docs/INTEGRATION-GUIDE.md`:

### Section to Add: "Feature Planning vs Task Generation"

```markdown
## Feature Planning vs Task Generation

RequireKit and GuardKit provide complementary commands for different stages of feature development.

### When to use `/feature-plan` (guardkit)
- Planning new features from scratch
- Evaluating technical approaches and trade-offs
- Quick feature exploration before commitment
- Getting effort estimates before starting
- **Input**: Natural language description ("implement dark mode")
- **Output**: Technical analysis, decision checkpoint, optional subtasks

### When to use `/feature-generate-tasks` (require-kit)
- You have a structured feature specification (FEAT-XXX)
- You need tasks exported to PM tools (Jira, Linear, GitHub, Azure DevOps)
- You need hierarchical task IDs for tracking (TASK-001.2.01)
- You want tasks derived from requirements and BDD scenarios
- You need traceability from requirements to implementation
- **Input**: Feature ID with linked requirements and BDD scenarios
- **Output**: Multiple task files ready for PM tool export

### Typical Workflow

1. `/feature-plan "description"` - Quick planning and approach decision
2. `/gather-requirements` - Formal requirements gathering (if needed)
3. `/feature-create` - Create structured feature spec
4. `/feature-generate-tasks FEAT-XXX` - Generate PM-exportable tasks
5. `/task-work TASK-XXX` - Execute implementation (guardkit)

### Comparison Matrix

| Aspect | `/feature-plan` | `/feature-generate-tasks` |
|--------|-----------------|--------------------------|
| Input | Natural language | Structured feature spec |
| Output | Analysis + decision | Exportable task files |
| PM Export | No | Yes (Jira, Linear, etc.) |
| Traceability | No | Yes (REQ → Task) |
| Hierarchy IDs | No | Yes (TASK-001.2.01) |
| Best for | Planning | Generation |
```

## Acceptance Criteria

- [x] Documentation added to `docs/INTEGRATION-GUIDE.md`
- [x] Clear guidance on when to use each command
- [x] Workflow example showing both commands in sequence
- [x] Comparison matrix for quick reference

## Estimated Effort

~0.5 days (2-4 hours)

## Notes

- This task addresses potential user confusion between the two commands
- No code changes required - documentation only
- Preserves value of both require-kit and guardkit functionality
