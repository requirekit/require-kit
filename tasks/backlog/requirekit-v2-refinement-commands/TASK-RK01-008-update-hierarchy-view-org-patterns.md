---
id: TASK-RK01-008
title: "Update hierarchy-view to render all organisation patterns"
task_type: feature
parent_review: TASK-REV-RK01
feature_id: FEAT-RK-001
wave: 3
implementation_mode: task-work
complexity: 6
dependencies: [TASK-RK01-002]
status: pending
priority: high
tags: [hierarchy-view, organisation-pattern, tree-view]
---

# Task: Update Hierarchy View to Render All Organisation Patterns

## Description

Update `installer/global/commands/hierarchy-view.md` to render direct-pattern and mixed-pattern epics in tree view, add Graphiti integration display, and update filtering options.

## Files to Modify

- `installer/global/commands/hierarchy-view.md`

## Changes Required

1. **Rewrite Default Tree View** to handle all three patterns:
   ```
   EPIC-001: User Management System (features pattern)
   ├── FEAT-001: User Authentication
   │   ├── TASK-001: Implement login [completed]
   │   └── TASK-002: Add session handling [in_progress]
   └── FEAT-002: Profile Management
       └── TASK-003: Create profile form [backlog]

   EPIC-002: Fix Auth Bugs (direct pattern)
   ├── TASK-004: Debug session timeout [in_progress]
   ├── TASK-005: Fix password reset [backlog]
   └── TASK-006: Update tests [backlog]

   EPIC-003: Platform Upgrade (mixed pattern)
   ├── FEAT-002: UI Redesign
   │   └── TASK-007: Update logo [backlog]
   └── [Direct Tasks]
       └── TASK-008: Upgrade dependencies [backlog]
   ```

2. **Update External Tools View**:
   - Add Graphiti integration section
   - Show connection status, episodes synced, last sync
   - Display group ID (`{project}__requirements`)

3. **Update Workflow Status View**:
   - Add Graphiti knowledge graph health indicator
   - Show episode coverage per entity type
   - Display completeness scores

4. **Update Filtering Options**:
   - Add `--pattern [direct|features|mixed]` filter
   - Add `--graphiti-status` filter

5. **Update Dependency Mapping**:
   - Handle direct-pattern epic dependencies (task-to-task, no feature layer)
   - Show cross-epic dependencies correctly for all patterns

## Acceptance Criteria

- [ ] Tree view renders all three organisation patterns correctly
- [ ] Direct-pattern epics show tasks directly under epic
- [ ] Mixed-pattern epics show "[Direct Tasks]" group with visual separation
- [ ] Pattern label shown next to each epic
- [ ] Graphiti integration section in external tools view
- [ ] `--pattern` filter works correctly
- [ ] Dependency mapping handles all patterns
- [ ] Backward compatible with existing features-pattern epics

## Test Requirements

- [ ] Verify tree rendering for each pattern
- [ ] Verify mixed pattern "[Direct Tasks]" grouping
- [ ] Verify filtering options documented
