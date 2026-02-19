---
id: TASK-RK01-005
title: "Create /feature-refine command"
task_type: feature
parent_review: TASK-REV-RK01
feature_id: FEAT-RK-001
wave: 2
implementation_mode: task-work
complexity: 6
dependencies: [TASK-RK01-001]
status: pending
priority: high
tags: [feature-refine, refinement, command]
---

# Task: Create /feature-refine Command

## Description

Create the `/feature-refine` command definition at `installer/global/commands/feature-refine.md`. Interactive refinement of existing features with focus on acceptance criteria specificity, requirements traceability, and BDD scenario coverage.

## Files to Create

- `installer/global/commands/feature-refine.md` - Feature refinement command definition

## Changes Required

Same three-phase pattern as `/epic-refine` (display → questions → summary), with feature-specific question categories:

### Phase 1: Current State Display
- Load feature markdown file by ID
- Parse frontmatter and content
- Calculate feature completeness score (7-dimension model)
- Show linked epic context
- Display completeness assessment

### Phase 2: Targeted Questions (Feature-Specific Categories)

| Category | When Asked | Focus |
|----------|-----------|-------|
| Acceptance Criteria | Criteria aren't testable/specific | Specificity and measurability |
| Requirements Traceability | Missing EARS requirement links | Link to EARS requirements |
| BDD Coverage | Missing/incomplete scenarios | Generate with `/generate-bdd` |
| Technical Considerations | Architecture decisions missing | API, performance, dependencies |
| Dependencies | No dependency analysis | Feature dependencies |
| Scope Within Epic | Overlap with other features | Differentiation |

### Phase 3: Change Summary and Commit
- Same pattern as epic-refine
- Feature-specific refinement_history
- Graphiti push with feature episode schema

### Arguments
```bash
/feature-refine <feature-id> [options]
/feature-refine FEAT-001
/feature-refine FEAT-001 --focus acceptance
/feature-refine FEAT-001 --focus technical
/feature-refine FEAT-001 --focus bdd
```

### Cross-Command Integration
- Can suggest running `/formalize-ears` to create linked requirements
- Can suggest running `/generate-bdd` to create missing scenarios
- Shows parent epic completeness for context

## Acceptance Criteria

- [ ] Command file follows established pattern
- [ ] Three-phase flow with feature-specific questions
- [ ] 6 question categories matching FEAT-RK-001 spec
- [ ] Feature completeness score (7 dimensions) calculated
- [ ] `--focus` flag restricts to single category
- [ ] Cross-command suggestions for `/formalize-ears` and `/generate-bdd`
- [ ] Graphiti push with feature episode schema
- [ ] Same UX patterns as epic-refine ([REFINE] prefix, one-at-a-time, skip/done)

## Test Requirements

- [ ] Verify command file has valid structure
- [ ] Verify all 6 question categories present
- [ ] Verify feature completeness dimensions match spec
