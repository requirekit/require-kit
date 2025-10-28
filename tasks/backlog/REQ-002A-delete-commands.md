---
id: REQ-002A
title: "Delete Task Execution Commands"
created: 2025-10-27
status: backlog
priority: high
complexity: 3
parent_task: REQ-002
subtasks: []
estimated_hours: 0.5
---

# REQ-002A: Delete Task Execution Commands

## Description

Delete all task execution and quality gate commands from `installer/global/commands/`, keeping ONLY requirements management commands.

## Commands to DELETE

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/global/commands/

# Task execution commands
rm -f task-create.md
rm -f task-work.md
rm -f task-complete.md
rm -f task-status.md
rm -f task-refine.md
rm -f task-sync.md
rm -f debug.md

# UX integration commands
rm -f figma-to-react.md
rm -f zeplin-to-maui.md
rm -f mcp-zeplin.md

# Dashboard/visualization (if task-focused)
rm -f portfolio-dashboard.md
```

## Commands to KEEP

```bash
# Requirements gathering
✅ gather-requirements.md
✅ formalize-ears.md
✅ generate-bdd.md

# Epic management
✅ epic-create.md
✅ epic-status.md
✅ epic-sync.md
✅ epic-generate-features.md

# Feature management
✅ feature-create.md
✅ feature-status.md
✅ feature-sync.md
✅ feature-generate-tasks.md (evaluate - may need modification)

# Visualization
✅ hierarchy-view.md
```

## Implementation

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/global/commands/

# Delete task execution commands
rm -f task-create.md task-work.md task-complete.md task-status.md task-refine.md task-sync.md debug.md

# Delete UX integration commands
rm -f figma-to-react.md zeplin-to-maui.md mcp-zeplin.md

# Delete dashboard (if exists)
rm -f portfolio-dashboard.md

# List remaining commands
echo "Remaining commands:"
ls -1 *.md
```

## Verification

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/global/commands/

# Count remaining commands
ls -1 *.md | wc -l
# Expected: 11-12 (requirements and epic/feature commands)

# Verify no task execution commands
ls -1 | grep -E "task-(create|work|complete|status|refine|sync)"
# Should return EMPTY

# Verify no UX integration
ls -1 | grep -E "figma|zeplin"
# Should return EMPTY
```

## Post-Deletion Review

Check `feature-generate-tasks.md`:
- If it generates task files for execution → DELETE
- If it generates feature breakdown only → KEEP (with modifications)

## Acceptance Criteria

- [ ] 11-12 task execution/UX commands deleted
- [ ] 11-12 requirements commands remain
- [ ] No task-create, task-work, task-complete, etc.
- [ ] No figma-to-react, zeplin-to-maui
- [ ] Only requirements/epic/feature commands remain
- [ ] Verification tests pass

## Estimated Time

0.5 hours

## Notes

- Simple file deletion task
- Verify count after deletion
- Commit changes after verification
