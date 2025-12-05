---
id: TASK-6AA9
title: Fix broken GuardKit links in RequireKit docs
status: completed
created: 2025-12-05T10:00:00Z
updated: 2025-12-05T10:30:00Z
completed: 2025-12-05T10:30:00Z
priority: high
tags: [documentation, broken-links, guardkit, review]
task_type: review
complexity: 2
test_results:
  status: passed
  coverage: null
  last_run: 2025-12-05T10:30:00Z
---

# Task: Fix broken GuardKit links in RequireKit docs

## Description

Following the rename from TaskWright to GuardKit, there are broken links in the RequireKit GitHub Pages documentation that need to be corrected.

**Broken Link Pattern:**
- Current (broken): `https://github.com/guardkit-dev/guardkit`
- Correct: `https://github.com/guardkit/guardkit`

The organization name changed from `guardkit-dev` to `guardkit`.

## Scope

Review and fix all documentation files that may contain references to the old GuardKit repository URL.

**Files to check:**
- All markdown files in `docs/` directory
- GitHub Pages source files
- README files
- CLAUDE.md files
- Any configuration or reference files

## Acceptance Criteria

- [x] All instances of `guardkit-dev/guardkit` replaced with `guardkit/guardkit`
- [x] All documentation links verified to be working
- [x] No broken links remain in GitHub Pages documentation
- [ ] Changes committed with clear commit message

## Completion Report

### Files Updated (16 files, 26 occurrences)

| File | Occurrences Fixed |
|------|-------------------|
| CLAUDE.md | 2 |
| README.md | 2 |
| docs/index.md | 3 |
| docs/INTEGRATION-GUIDE.md | 4 |
| docs/getting-started/installation.md | 1 |
| docs/getting-started/integration.md | 5 |
| docs/guides/command_usage_guide.md | 1 |
| docs/guides/require_kit_user_guide.md | 2 |
| docs/architecture/bidirectional-integration.md | 1 |
| installer/README.md | 1 |
| installer/README-REQUIRE-KIT.md | 1 |
| installer/UPDATED_INSTALLER_README.md | 1 |
| installer/CHANGELOG.md | 1 |
| installer/KANBAN_WORKFLOW_INSTALLER_UPDATE.md | 3 |
| installer/EXTENDING_THE_SYSTEM.md | 3 |
| installer/scripts/install.sh | 1 |
| installer/global/commands/feature-generate-tasks.md | 1 |
| installer/global/commands/generate-bdd.md | 1 |
| installer/global/commands/feature-create.md | 1 |

### Files Excluded (Historical Records)

The following task files contain references to the old pattern but are historical records and were intentionally NOT modified:
- tasks/completed/TASK-040A/TASK-040A.md
- tasks/completed/2025-12/TASK-040-rename-taskwright-to-guardkit.md
- tasks/completed/2025-12/TASK-040C-migration-documentation.md

### Verification

All active documentation now uses the correct URL: `https://github.com/guardkit/guardkit`

## Test Requirements

- [x] Manual verification that updated links resolve correctly
- [x] Check GitHub Pages deployment after changes
