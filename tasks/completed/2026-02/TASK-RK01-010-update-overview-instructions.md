---
id: TASK-RK01-010
title: "Update overview instructions with refinement workflow"
task_type: documentation
parent_review: TASK-REV-RK01
feature_id: FEAT-RK-001
wave: 3
implementation_mode: direct
complexity: 3
dependencies: [TASK-RK01-001]
status: completed
priority: normal
tags: [overview, instructions, documentation]
---

# Task: Update Overview Instructions with Refinement Workflow

## Description

Update `installer/global/instructions/core/00-overview.md` to document the refinement workflow, optional feature layer, and Graphiti integration as core components.

## Files to Modify

- `installer/global/instructions/core/00-overview.md`

## Changes Required

1. **Add Requirements Refinement Component** (new section 5):
   - Purpose: Iterative improvement of requirements
   - Method: Guided refinement with completeness scoring
   - Output: Refined epics/features with tracked history
   - Commands: `/epic-refine`, `/feature-refine`

2. **Update Development Flow**:
   - Add "Refinement" step between gathering and formalization
   - Add "Graphiti Sync" as optional parallel step

3. **Update Project Hierarchy Section**:
   - Document three organisation patterns
   - Show all three hierarchy structures

4. **Update Available Commands List**:
   - Add `/epic-refine` and `/feature-refine`
   - Add `/requirekit-sync`

5. **Add Key Principle**:
   - "Iterative Refinement: Requirements improve through structured feedback"

## Acceptance Criteria

- [ ] Refinement documented as core component
- [ ] Development flow updated with refinement step
- [ ] Three organisation patterns shown
- [ ] New commands listed
- [ ] New principle added

## Test Requirements

- [ ] Verify file is valid markdown
- [ ] Verify all new commands mentioned
