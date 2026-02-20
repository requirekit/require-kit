---
id: TASK-DOC-004
title: Update commands/hierarchy.md with new flags and examples
status: completed
task_type: implementation
created: 2026-02-20T00:00:00Z
completed: 2026-02-20T00:00:00Z
priority: medium
complexity: 3
parent_review: TASK-REV-9480
feature_id: feat-498f-docs-update
wave: 1
implementation_mode: direct
tags: [documentation, mkdocs, feat-498f]
completed_location: tasks/completed/TASK-DOC-004/
organized_files:
  - TASK-DOC-004.md
---

# Task: Update commands/hierarchy.md with New Flags and Examples

## Description

Expand `docs/commands/hierarchy.md` from its current 17 lines to properly document the FEAT-498F enhancements to `/hierarchy-view`.

## Current State

The file is minimal:
```markdown
# Hierarchy Commands
Commands for visualizing and navigating requirement hierarchies.
## /hierarchy-view
View complete epic/feature/requirement hierarchy.
**Usage:** /hierarchy-view EPIC-XXX
**Output:** Visual tree showing all linked artifacts.
```

## Changes Required

Expand to include:
1. Full usage syntax with all options
2. `--pattern` filter flag (filter hierarchy by organisation pattern: standard, direct, mixed)
3. `--graphiti-status` filter (filter by Graphiti sync status)
4. Pattern-aware tree rendering explanation
5. Graphiti health display in workflow view
6. Output examples for each pattern type (Standard, Direct, Mixed)
7. Options table with all flags

## Source Material

- `docs/core-concepts/hierarchy.md` for pattern examples
- `docs/commands/epics.md` style for formatting consistency

## Acceptance Criteria

- [x] All new flags documented with descriptions
- [x] Output examples for Standard, Direct, and Mixed patterns
- [x] Options table formatted consistently with other command pages
- [x] Link to detailed hierarchy documentation maintained

## Completion Notes

Expanded `docs/commands/hierarchy.md` from 17 lines to 87 lines. Changes include:
- Full usage syntax with `--pattern` and `--graphiti-status` flags
- Options table consistent with `epics.md` formatting
- Pattern-aware tree rendering section with concrete output examples for all three patterns (Standard, Direct, Mixed)
- Graphiti health display section documenting workflow view indicators
- Links to command usage guide and `core-concepts/hierarchy.md`
