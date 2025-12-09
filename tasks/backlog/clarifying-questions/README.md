# Clarifying Questions Enhancement for RequireKit

## Overview

This task set implements targeted clarifying questions for RequireKit's hierarchy commands (`/epic-create`, `/feature-create`) and EARS formalization (`/formalize-ears`), based on the analysis in TASK-REV-025.

**Review Report**: [TASK-REV-025-review-report.md](../../../.claude/reviews/TASK-REV-025-review-report.md)

## Philosophy

RequireKit clarifications focus on **requirements specification**, not implementation:

| RequireKit (Technology-Agnostic) | GuardKit (Technology-Specific) |
|----------------------------------|-------------------------------|
| "What is OUT OF SCOPE?" | "JWT vs Sessions?" |
| "What are the success criteria?" | "Redux vs Zustand?" |
| "Which requirements does this implement?" | "REST vs GraphQL?" |

This preserves RequireKit's core principle: **technology-agnostic requirements specification**.

## Task Summary

| Task ID | Title | Priority | Effort | Wave |
|---------|-------|----------|--------|------|
| TASK-CLQ-001 | Add clarification to /epic-create | High | 0.5 day | 1 |
| TASK-CLQ-002 | Add clarification to /feature-create | High | 0.5 day | 1 |
| TASK-CLQ-003 | Add pattern clarification to /formalize-ears | Medium | 0.5-1 day | 1 |
| TASK-CLQ-004 | Document clarification philosophy | Medium | 0.25 day | 2 |
| TASK-CLQ-005 | Integration testing | Medium | 0.5 day | 3 |

**Total Effort**: 1.75-2.75 days

## Wave Structure

See [IMPLEMENTATION-GUIDE.md](./IMPLEMENTATION-GUIDE.md) for detailed execution instructions.

### Wave 1: Core Enhancements (Parallel)
- TASK-CLQ-001, TASK-CLQ-002, TASK-CLQ-003
- Can run in parallel using Conductor workspaces
- Each modifies independent command files

### Wave 2: Documentation
- TASK-CLQ-004
- Depends on Wave 1 completion
- Documents the clarification philosophy

### Wave 3: Integration Testing
- TASK-CLQ-005
- Validates all enhancements work together
- End-to-end workflow testing

## Files Modified

```
installer/global/commands/
├── epic-create.md          ← TASK-CLQ-001
├── feature-create.md       ← TASK-CLQ-002
└── formalize-ears.md       ← TASK-CLQ-003

docs/
└── INTEGRATION-GUIDE.md    ← TASK-CLQ-004
```

## Success Criteria

- [ ] `/epic-create` prompts for scope, success criteria, stakeholders
- [ ] `/feature-create` prompts for scope, requirements, acceptance criteria
- [ ] `/formalize-ears` guides EARS pattern selection when ambiguous
- [ ] Clarification philosophy documented
- [ ] All commands work in typical workflow: epic → feature → requirements → EARS → BDD

## Related

- **Source Review**: TASK-REV-025
- **GuardKit Reference**: TASK-REV-B130 (different approach, implementation-focused)
- **RequireKit Philosophy**: Technology-agnostic requirements specification
