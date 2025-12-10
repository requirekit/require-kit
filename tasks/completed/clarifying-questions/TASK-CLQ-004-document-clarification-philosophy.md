---
id: TASK-CLQ-004
title: Document Clarification Philosophy
status: completed
type: documentation
priority: medium
complexity: 2
created: 2025-12-09T11:00:00Z
completed: 2025-12-10T00:00:00Z
wave: 2
parallel_safe: false
execution_method: direct-claude-code
estimated_effort: 0.25 day
parent_review: TASK-REV-025
depends_on: [TASK-CLQ-001, TASK-CLQ-002, TASK-CLQ-003]
tags: [clarifying-questions, documentation, wave-2, sequential]
files_modified:
  - docs/INTEGRATION-GUIDE.md
---

# Document Clarification Philosophy

## Objective

Document RequireKit's clarification philosophy, explaining which commands have clarification, why, and how this differs from implementation-focused clarification (like GuardKit).

## Background

From TASK-REV-025 analysis: RequireKit's clarifications are fundamentally different from GuardKit's:

| RequireKit (Specification) | GuardKit (Implementation) |
|---------------------------|--------------------------|
| "What is out of scope?" | "JWT vs Sessions?" |
| "What are success criteria?" | "Redux vs Zustand?" |
| Technology-agnostic | Technology-specific |

This distinction must be documented for users and maintainers.

## Execution Method

**Direct Claude Code** - Documentation update to existing file.

Do NOT use `/task-work` for this task.

**Dependencies**: Wait for Wave 1 tasks (CLQ-001, 002, 003) to complete so documentation reflects actual implementation.

## Implementation

### File to Modify

`docs/INTEGRATION-GUIDE.md`

### Changes Required

Add a new section "Clarification Philosophy" (location: after the integration overview, before detailed integration steps):

```markdown
## Clarification Philosophy

RequireKit asks clarifying questions to improve **requirement specifications**, not to make implementation decisions. This is a key distinction from implementation-focused systems.

### When RequireKit Asks Questions

| Command | Has Clarification | Purpose |
|---------|-------------------|---------|
| `/gather-requirements` | Yes (3-phase) | Comprehensive requirements discovery |
| `/epic-create` | Yes | Scope, success criteria, stakeholders |
| `/feature-create` | Yes | Scope, acceptance criteria, dependencies |
| `/formalize-ears` | Yes | EARS pattern selection, completeness |
| `/generate-bdd` | No | Deterministic transformation |
| `/epic-generate-features` | No | Systematic analysis |
| `/feature-generate-tasks` | No | Rule-based generation |

### Question Types by Domain

**RequireKit Questions (Technology-Agnostic)**:
- "What is explicitly OUT OF SCOPE?"
- "What measurable outcomes define success?"
- "Which requirements does this implement?"
- "What are the testable acceptance criteria?"
- "Is this triggered by an event or always active?"

**NOT RequireKit Questions (Technology-Specific)**:
- "JWT or server-side sessions?" → GuardKit/Implementation
- "Redux, Zustand, or Context API?" → GuardKit/Implementation
- "REST or GraphQL?" → GuardKit/Implementation
- "PostgreSQL or MongoDB?" → GuardKit/Implementation

### Why This Matters

RequireKit outputs must be **technology-agnostic** so they can:
1. Work with any implementation system
2. Be consumed by GuardKit or other task execution systems
3. Remain valid regardless of technology choices
4. Be understood by non-technical stakeholders

### Clarification at Specification vs Implementation

```
                    SPECIFICATION                     IMPLEMENTATION
                    (RequireKit)                      (GuardKit/Other)
                         │                                  │
    ┌────────────────────┼──────────────────────────────────┼─────────────────┐
    │                    │                                  │                 │
    │  "What problem?"   │  "What capability?"   "How to build?"  "What tech?" │
    │  "Who uses it?"    │  "What acceptance?"   "What pattern?"  "What lib?"  │
    │  "Why needed?"     │  "What success?"      "What arch?"     "What DB?"   │
    │                    │                                  │                 │
    └────────────────────┼──────────────────────────────────┼─────────────────┘
                         │                                  │
                    TECHNOLOGY-AGNOSTIC              TECHNOLOGY-SPECIFIC
```

### Integration with GuardKit

When using RequireKit with GuardKit:

1. **RequireKit handles specification clarification**:
   - Epic scope and success criteria
   - Feature acceptance criteria
   - EARS pattern selection
   - BDD scenario completeness

2. **GuardKit handles implementation clarification**:
   - Technology choices
   - Architecture patterns
   - Error handling approaches
   - Performance trade-offs

This separation ensures:
- No duplicate questions
- Clear responsibility boundaries
- Optimal user experience
- Technology decisions deferred to implementation time

### Skipping Clarification

All RequireKit clarifications are **optional**. Users can:
- Use `--quick` flag to skip questions
- Provide parameters directly in the command
- Let AI auto-detect patterns (with `--auto` flag)

Example:
```bash
# With clarification (interactive)
/epic-create "User Management"

# Without clarification (direct)
/epic-create "User Management" priority:high quarter:Q1-2024 --quick
```
```

## Acceptance Criteria

- [ ] New "Clarification Philosophy" section added to INTEGRATION-GUIDE.md
- [ ] Table showing which commands have clarification
- [ ] Clear examples of RequireKit vs implementation questions
- [ ] Diagram showing specification vs implementation boundary
- [ ] Integration guidance for RequireKit + GuardKit users
- [ ] Skip options documented

## Testing

Manual verification:
1. Read the updated documentation
2. Verify examples are accurate
3. Verify table matches actual implementation
4. Verify philosophy aligns with TASK-REV-025 recommendations

## Notes

- This documentation helps users understand WHY clarification exists
- Important for users integrating RequireKit with other systems
- Should be updated if new commands get clarification
