---
complexity: 5
dependencies:
- TASK-RK01-002
feature_id: FEAT-RK-001
id: TASK-RK01-007
implementation_mode: task-work
parent_review: TASK-REV-RK01
priority: high
status: design_approved
tags:
- epic-status
- organisation-pattern
- display
task_type: feature
title: Update epic-status to display organisation patterns
wave: 3
---

# Task: Update Epic Status to Display Organisation Patterns

## Description

Update `installer/global/commands/epic-status.md` to display both features and direct tasks, handle all three organisation patterns (direct, features, mixed), and show Graphiti sync status.

## Files to Modify

- `installer/global/commands/epic-status.md`

## Changes Required

1. **Update Portfolio View Table**:
   - Add "Pattern" column showing organisation_pattern
   - Show task count for direct-pattern epics
   - Show feature count for features-pattern epics
   - Show both for mixed-pattern epics

2. **Update Detailed View**:
   - Add "Organisation Pattern" line after Priority
   - For `direct` pattern: Show "Direct Tasks (N)" section
   - For `features` pattern: Show "Features (N)" section (current behaviour)
   - For `mixed` pattern: Show both sections + warning

3. **Add Direct Tasks Display**:
   ```
   📋 Epic: EPIC-002 — Fix Auth Bugs
   Status: in_progress | Priority: high | Pattern: direct

   Direct Tasks (3):
     🔄 TASK-004: Debug session timeout [in_progress]
     ⏳ TASK-005: Fix password reset [backlog]
     ⏳ TASK-006: Update tests [backlog]

   Progress: 33% (1/3 tasks in progress)
   ```

4. **Add Mixed Pattern Display**:
   ```
   📋 Epic: EPIC-003 — Platform Upgrade
   Status: in_progress | Pattern: mixed
   ⚠️ Mixed organisation — consider grouping tasks into features

   Features (1):
     🔄 FEAT-002: UI Redesign (1 task)

   Direct Tasks (1):
     ⏳ TASK-008: Upgrade dependencies [backlog]
   ```

5. **Add Graphiti Sync Status**:
   - Show Graphiti sync indicator alongside PM tool status
   - Display last sync time
   - Add completeness score to detailed view

6. **Update Progress Calculation**:
   - Direct pattern: count completed tasks / total tasks
   - Features pattern: current behaviour (feature completion)
   - Mixed pattern: weighted combination

## Acceptance Criteria

- [ ] Portfolio view shows pattern column for all epics
- [ ] Direct-pattern epics show task list instead of feature list
- [ ] Mixed-pattern epics show both with warning
- [ ] Progress calculated correctly for all three patterns
- [ ] Graphiti sync status displayed when enabled
- [ ] Completeness score shown in detailed view
- [ ] Backward compatible (existing features-pattern epics display unchanged)

## Test Requirements

- [ ] Verify direct pattern display format matches spec
- [ ] Verify mixed pattern warning appears
- [ ] Verify progress calculation for each pattern