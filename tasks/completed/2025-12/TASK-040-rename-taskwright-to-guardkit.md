---
id: TASK-040
title: Rename taskwright to guardkit across codebase (Parent)
status: completed
created: 2025-12-03T10:00:00Z
updated: 2025-12-03T12:00:00Z
completed: 2025-12-03T12:00:00Z
priority: high
tags: [refactoring, branding, rename, parent-task]
task_type: parent
complexity: 4
subtasks: [TASK-040A, TASK-040B, TASK-040C]
review_completed: true
review_report: .claude/reviews/TASK-040-review-report.md
---

# Task: Rename taskwright to guardkit across codebase (Parent)

## Status: Split into Subtasks

This task has been **reviewed and split** into three coordinated subtasks based on architectural analysis.

**Review Report**: [.claude/reviews/TASK-040-review-report.md](../../.claude/reviews/TASK-040-review-report.md)

## Subtasks

| Task | Scope | Status | Repo |
|------|-------|--------|------|
| **TASK-040A** | Rename refs in require-kit | backlog | require-kit |
| **TASK-040B** | Rename refs in guardkit | backlog | guardkit |
| **TASK-040C** | Migration documentation | blocked | both |

### Execution Order

```
TASK-040A ──┬──> TASK-040C ──> TASK-040 Complete
TASK-040B ──┘
```

- TASK-040A and TASK-040B can run **in parallel**
- TASK-040C is **blocked** until both A and B complete

## Original Description

The taskwright repository and product has been renamed to **guardkit** due to a naming conflict. This task involves searching for all occurrences of 'taskwright' throughout the codebase and replacing them with 'guardkit'.

## Scope Analysis

**Initial grep results:** 85 occurrences across 20+ files

### Files to Review

Based on initial search, the following areas contain 'taskwright' references:

1. **Root documentation**
   - `CLAUDE.md` (5 occurrences)
   - `README.md` (8 occurrences)
   - `DOCS-SETUP.md` (1 occurrence)
   - `mkdocs.yml` (3 occurrences)

2. **Documentation site (generated)**
   - `site/` directory - multiple HTML files (these may regenerate from source)
   - `site/search/search_index.json`
   - `site/integration/features.json`

3. **Source documentation**
   - `docs/developer/architecture.md` (3 occurrences)

4. **Installer/commands**
   - `installer/global/commands/feature-sync.md` (7 occurrences)
   - `installer/global/commands/epic-create.md` (2 occurrences)

## Acceptance Criteria

- [ ] All occurrences of 'taskwright' replaced with 'guardkit'
- [ ] All occurrences of 'Taskwright' replaced with 'Guardkit' (preserve case)
- [ ] All occurrences of 'TASKWRIGHT' replaced with 'GUARDKIT' (preserve case)
- [ ] URLs updated (e.g., github.com/taskwright-dev → github.com/guardkit-dev if applicable)
- [ ] Generated site files regenerated after source changes
- [ ] No broken links or references after rename
- [ ] Build/documentation generation still works

## Implementation Notes

### Rename Mapping

| Old | New |
|-----|-----|
| taskwright | guardkit |
| Taskwright | Guardkit |
| TASKWRIGHT | GUARDKIT |
| taskwright-dev | guardkit-dev (if used in URLs) |

### Considerations

1. **Generated files**: The `site/` directory appears to contain generated documentation. Focus on source files first, then regenerate.

2. **Case sensitivity**: Ensure proper case matching for each replacement.

3. **Context verification**: Review each replacement to ensure it makes sense in context.

4. **URL references**: Check for any GitHub URLs or package references that may need updating.

## Test Requirements

- [ ] Grep for 'taskwright' returns 0 results after completion
- [ ] Documentation site builds successfully
- [ ] All internal links still work
- [ ] README renders correctly

## Commands for Execution

```bash
# Find all occurrences (case-insensitive)
grep -ri "taskwright" --include="*.md" --include="*.yml" --include="*.json"

# Exclude generated site directory for source changes
grep -ri "taskwright" --include="*.md" --include="*.yml" --exclude-dir="site"

# After source changes, regenerate docs
mkdocs build
```

## Next Steps

1. Review task details
2. When ready: `/task-work TASK-040`
3. Track progress: `/task-status TASK-040`
4. Complete task: `/task-complete TASK-040`
