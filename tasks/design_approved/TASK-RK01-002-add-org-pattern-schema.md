---
complexity: 5
dependencies: []
feature_id: FEAT-RK-001
id: TASK-RK01-002
implementation_mode: task-work
parent_review: TASK-REV-RK01
priority: high
status: design_approved
tags:
- organisation-pattern
- epic-create
- schema
- REQ-004
task_type: feature
title: Add organisation pattern schema to epic-create command
wave: 1
---

# Task: Add Organisation Pattern Schema to Epic Create Command

## Description

Update `installer/global/commands/epic-create.md` to support the optional feature layer (REQ-004). Add `organisation_pattern` and `direct_tasks` fields to epic frontmatter template, update examples, and add validation rules.

## Files to Modify

- `installer/global/commands/epic-create.md` - Add org pattern fields, examples, validation, Graphiti push step

## Changes Required

1. **Update Frontmatter Template**:
   - Add `organisation_pattern: features` (default for new epics)
   - Add `direct_tasks: []` field
   - Add `graphiti_synced: false` field
   - Add `last_graphiti_sync: null` field
   - Add `completeness_score: 0` field

2. **Add Organisation Pattern Documentation**:
   - Three patterns: `direct`, `features`, `mixed`
   - When to use each (direct: 3-5 tasks, features: 10+ tasks, mixed: evolving)
   - Pattern selection during creation: `--pattern direct`
   - Default behaviour: `features` (backward compatible)

3. **Update Examples**:
   - Add `--pattern direct` example
   - Add example with direct task specification
   - Show PM tool mapping for all patterns

4. **Add Graphiti Push Step**:
   - After markdown creation, push epic episode to Graphiti if enabled
   - Graceful failure handling (markdown always saved)
   - Display sync status in output

5. **Update Validation Rules**:
   - Validate `organisation_pattern` is one of: direct, features, mixed
   - Warn on mixed pattern selection

## Acceptance Criteria

- [ ] Epic frontmatter template includes `organisation_pattern`, `direct_tasks`, `graphiti_synced` fields
- [ ] Default organisation_pattern is `features` (backward compatible)
- [ ] Three patterns documented with when-to-use guidance
- [ ] Validation rejects invalid pattern values
- [ ] Mixed pattern produces a warning
- [ ] Graphiti push step documented with graceful degradation
- [ ] Examples section includes `--pattern` usage

## Test Requirements

- [ ] Verify frontmatter template generates valid YAML
- [ ] Verify default pattern is `features`
- [ ] Verify all three patterns are documented