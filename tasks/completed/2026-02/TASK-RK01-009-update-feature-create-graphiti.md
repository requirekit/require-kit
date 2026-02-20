---
id: TASK-RK01-009
title: "Update feature-create with Graphiti push and completeness fields"
task_type: feature
parent_review: TASK-REV-RK01
feature_id: FEAT-RK-001
wave: 3
implementation_mode: direct
complexity: 3
dependencies: [TASK-RK01-003]
status: completed
priority: normal
tags: [feature-create, graphiti, completeness]
---

# Task: Update Feature Create with Graphiti Push and Completeness Fields

## Description

Update `installer/global/commands/feature-create.md` to add Graphiti push on create and completeness-related frontmatter fields.

## Files to Modify

- `installer/global/commands/feature-create.md`

## Changes Required

1. **Update Frontmatter Template**:
   - Add `graphiti_synced: false` field
   - Add `last_graphiti_sync: null` field
   - Add `completeness_score: 0` field

2. **Add Graphiti Push Step**:
   - After markdown creation, push feature episode to Graphiti if enabled
   - Use feature episode schema from FEAT-RK-001 spec
   - Graceful failure handling (markdown always saved)
   - Display "Graphiti Status" line in output

3. **Update Validation**:
   - Document that feature cannot specify both `epic:` and direct epic assignment
   - Features always belong to epics (validation rule from REQ-004)

4. **Update Output Format**:
   - Add Graphiti sync status line
   - Add initial completeness score display

## Acceptance Criteria

- [ ] Frontmatter template includes graphiti_synced, last_graphiti_sync, completeness_score
- [ ] Process section includes Graphiti push step with graceful degradation
- [ ] Output format shows Graphiti status
- [ ] Validation rules documented for epic association

## Test Requirements

- [ ] Verify frontmatter generates valid YAML
- [ ] Verify Graphiti step documented with error handling
