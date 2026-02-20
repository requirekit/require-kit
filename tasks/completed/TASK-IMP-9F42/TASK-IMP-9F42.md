---
id: TASK-IMP-9F42
title: Clean up FEAT-498F post-AutoBuild task state and directory artifacts
status: completed
task_type: feature
parent_review: TASK-REV-E2DD
feature_ref: FEAT-498F
created: 2026-02-20T00:00:00Z
updated: 2026-02-20T00:00:00Z
completed: 2026-02-20T16:30:00Z
completed_location: tasks/completed/TASK-IMP-9F42/
priority: high
tags: [autobuild, cleanup, task-state, feat-498f]
complexity: 3
implementation_mode: direct
organized_files: [TASK-IMP-9F42.md]
---

# Task: Clean Up FEAT-498F Post-AutoBuild State

## Description

Execute the cleanup recommendations from review TASK-REV-E2DD. All 6 actions are low-risk file operations with no code impact.

**Review report:** `.claude/reviews/TASK-REV-E2DD-review-report.md`

## Root Cause (from review)

Git merge path mismatch: main-side added tasks in `tasks/backlog/requirekit-v2-refinement-commands/` subdirectory, AutoBuild worked with flat paths. Merge preserved both, creating duplicates.

## Actions

### 1. Delete duplicate backlog subdirectory
```bash
rm -rf tasks/backlog/requirekit-v2-refinement-commands/
```
- 16 files (14 task specs + README.md + IMPLEMENTATION-GUIDE.md)
- These are stale copies with incorrect status fields
- Authoritative copies are in `tasks/design_approved/`

### 2. Move 12 tasks from design_approved to completed
```bash
mkdir -p tasks/completed/2026-02
# Move 12 tasks from design_approved/
mv tasks/design_approved/TASK-RK01-001-update-agent-refinement-mode.md tasks/completed/2026-02/
mv tasks/design_approved/TASK-RK01-002-add-org-pattern-schema.md tasks/completed/2026-02/
mv tasks/design_approved/TASK-RK01-003.md tasks/completed/2026-02/
mv tasks/design_approved/TASK-RK01-004-create-epic-refine-command.md tasks/completed/2026-02/
mv tasks/design_approved/TASK-RK01-005-create-feature-refine-command.md tasks/completed/2026-02/
mv tasks/design_approved/TASK-RK01-006-create-requirekit-sync-command.md tasks/completed/2026-02/
mv tasks/design_approved/TASK-RK01-007-update-epic-status-org-patterns.md tasks/completed/2026-02/
mv tasks/design_approved/TASK-RK01-008-update-hierarchy-view-org-patterns.md tasks/completed/2026-02/
mv tasks/design_approved/TASK-RK01-011-update-docs-site-commands.md tasks/completed/2026-02/
mv tasks/design_approved/TASK-RK01-012-update-docs-hierarchy-concepts.md tasks/completed/2026-02/
mv tasks/design_approved/TASK-RK01-013-integration-tests.md tasks/completed/2026-02/
mv tasks/design_approved/TASK-RK01-014-e2e-tests.md tasks/completed/2026-02/
```
- Update `status: completed` in each file's frontmatter

### 3. Move 2 remaining tasks from backlog to completed
```bash
# Tasks 009 and 010 only exist in flat backlog (not in subdirectory)
mv tasks/backlog/TASK-RK01-009-update-feature-create-graphiti.md tasks/completed/2026-02/
mv tasks/backlog/TASK-RK01-010-update-overview-instructions.md tasks/completed/2026-02/
```
- Update `status: completed` in each file's frontmatter
- Note: these were NOT in the subdirectory -- they're at `tasks/backlog/` flat path

### 4. Update FEAT-498F.yaml
Update `.guardkit/features/FEAT-498F.yaml`:
- `status: completed` (was: failed)
- All 14 tasks: `status: completed`, `result.final_decision: approved`
- `execution.tasks_completed: 14` (was: 2)
- `execution.tasks_failed: 0` (was: 1)
- `execution.archived_at: 2026-02-20T00:00:00Z`

### 5. Clean up worktree
```bash
# Option A: via guardkit
guardkit worktree cleanup FEAT-498F

# Option B: manual (if guardkit command not available)
rm -rf .guardkit/worktrees/FEAT-498F
```

### 6. Delete orphaned planning task
```bash
rm tasks/backlog/TASK-REV-RK01-plan-requirekit-v2-refinement-commands.md
```

## Acceptance Criteria

- [x] No TASK-RK01-* files in `tasks/backlog/`
- [x] No `requirekit-v2-refinement-commands/` subdirectory in backlog
- [x] All 14 TASK-RK01-* files in `tasks/completed/2026-02/` with `status: completed`
- [x] FEAT-498F.yaml shows `status: completed` with 14/14 tasks completed
- [x] Worktree removed (`.guardkit/worktrees/FEAT-498F` gone)
- [x] Planning task removed from backlog
- [x] `design_approved/` has no TASK-RK01-* files remaining

## Risk Assessment

All actions are file deletions/moves with no code impact. The authoritative implementation work is on the `main` branch in the actual source files (commands, agents, docs, tests). Task files are organizational metadata only.
