---
id: TASK-DOC-005
title: Update commands/epics.md with --pattern flag for /epic-create
status: completed
task_type: implementation
created: 2026-02-20T00:00:00Z
completed: 2026-02-20T00:00:00Z
priority: medium
complexity: 2
parent_review: TASK-REV-9480
feature_id: feat-498f-docs-update
wave: 1
implementation_mode: direct
tags: [documentation, mkdocs, feat-498f]
completed_location: tasks/completed/TASK-DOC-005/
organized_files: [TASK-DOC-005.md]
---

# Task: Update commands/epics.md /epic-create with --pattern Flag

## Description

Update the `/epic-create` section in `docs/commands/epics.md` (lines 5-14) to document the `--pattern` flag added by FEAT-498F.

## Current State

```markdown
## /epic-create
Create a new epic.
**Usage:**
/epic-create "Epic Title"
```

## Changes Required

Add `--pattern` flag documentation:

```markdown
## /epic-create

Create a new epic.

**Usage:**
/epic-create "Epic Title" [options]

**Examples:**
/epic-create "User Management System"
/epic-create "Config Refactor" --pattern direct

**Options:**

| Flag | Description |
|---|---|
| `--pattern <pattern>` | Set organisation pattern: `standard` (default), `direct`, or `mixed` |
```

Also add brief note about Graphiti auto-sync if configured.

## Acceptance Criteria

- [x] `--pattern` flag documented with all 3 values
- [x] Examples show both basic and pattern-specific usage
- [x] Options table added
- [x] Style consistent with other command sections on the same page
