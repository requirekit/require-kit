---
id: TASK-039
title: Clean up .claude/commands/ directory to remove taskwright commands
status: completed
created: 2025-11-03T12:00:00Z
updated: 2025-11-03T14:35:00Z
completed: 2025-11-03T14:35:00Z
priority: high
tags: [cleanup, commands, require-kit, taskwright-separation]
complexity: 3
---

# Task: Clean up .claude/commands/ Directory

## Description

Remove taskwright command files from the `.claude/commands/` directory and verify that remaining require-kit command documentation is accurate and complete.

The `.claude/commands/` directory currently contains a mix of require-kit commands (requirements, BDD, epic/feature management) and taskwright commands (task execution, testing). The taskwright commands should be removed as they belong in the taskwright repository.

## Files to Remove (Taskwright Commands)

Located in `.claude/commands/`:

1. **task-complete.md** (8,577 bytes) - Task completion command
2. **task-create.md** (14,957 bytes) - Task creation command
3. **task-status.md** (10,029 bytes) - Task status monitoring
4. **task-work.md** (12,860 bytes) - Unified implementation workflow
5. **task-work-specification.md** (13,616 bytes) - Task work specifications
6. **execute-tests.md** (6,380 bytes) - Test execution command
7. **update-state.md** (6,450 bytes) - State update command

**Total**: 7 files to remove

## Files to Verify (require-kit Commands)

These should remain and be verified for accuracy:

1. **gather-requirements.md** (2,220 bytes) - Requirements gathering
2. **formalize-ears.md** (3,775 bytes) - EARS notation formalization
3. **generate-bdd.md** (5,851 bytes) - BDD scenario generation

**Note**: Epic/feature commands are in `installer/global/commands/` (correct location)

## Acceptance Criteria

- [x] All 7 taskwright command files removed from `.claude/commands/`
- [x] Moved to `.claude/commands/.deprecated/` for reference (not deleted)
- [x] Verified `gather-requirements.md` is accurate for require-kit
- [x] Verified `formalize-ears.md` is accurate for require-kit
- [x] Verified `generate-bdd.md` is accurate for require-kit
- [x] Each remaining command file references integration guide for taskwright features
- [x] No broken references to removed commands in other documentation

## Migration Strategy

Instead of deleting, move to deprecated:

```bash
# Move taskwright commands to deprecated
mkdir -p .claude/commands/.deprecated/taskwright/
mv .claude/commands/task-*.md .claude/commands/.deprecated/taskwright/
mv .claude/commands/execute-tests.md .claude/commands/.deprecated/taskwright/
mv .claude/commands/update-state.md .claude/commands/.deprecated/taskwright/
```

Add a README in the deprecated folder:

```markdown
# Deprecated Commands

These commands have been moved to the [taskwright](https://github.com/taskwright-dev/taskwright) repository.

## Moved Commands

- task-complete.md → taskwright/.claude/commands/
- task-create.md → taskwright/.claude/commands/
- task-status.md → taskwright/.claude/commands/
- task-work.md → taskwright/.claude/commands/
- task-work-specification.md → taskwright/.claude/commands/
- execute-tests.md → taskwright/.claude/commands/
- update-state.md → taskwright/.claude/commands/

## Integration

To use these commands, install taskwright alongside require-kit.
See [Integration Guide](../../docs/INTEGRATION-GUIDE.md) for details.
```

## Verification for Remaining Commands

For each of the 3 remaining command files, verify:

1. **Command description** focuses on require-kit features
2. **Examples** use only require-kit commands
3. **Integration section** exists with link to taskwright for task execution
4. **No references** to removed commands
5. **Consistent terminology** with README.md and INTEGRATION-GUIDE.md

## Test Requirements

- [x] Run command discovery to ensure removed commands don't appear
- [x] Verify Claude Code doesn't offer removed commands as suggestions
- [x] Test that remaining commands still work correctly
- [x] Verify no broken links in documentation to removed command files

## Implementation Notes

- Check if any other files reference the commands being removed
- Update any documentation that links to these command files
- Consider adding a note to the commands that they've moved to taskwright
- Coordinate with taskwright repository to ensure commands are documented there

## Related Tasks

- TASK-038: Core documentation update (may reference these commands)
- TASK-040: CLAUDE.md review (ensure no references to removed commands)
- TASK-041: Guides directory review (check for command references)

## Implementation Summary

### Completed Actions

1. **Moved 7 taskwright command files to deprecated folder**:
   - Created `.claude/commands/.deprecated/taskwright/` directory structure
   - Moved: task-complete.md, task-create.md, task-status.md, task-work.md, task-work-specification.md, execute-tests.md, update-state.md
   - Created README.md in deprecated folder explaining the move and integration with taskwright

2. **Verified remaining require-kit commands**:
   - `gather-requirements.md` - Verified accurate for require-kit
   - `formalize-ears.md` - Verified accurate for require-kit
   - `generate-bdd.md` - Updated to reference taskwright integration instead of `/execute-tests`

3. **Updated documentation references**:
   - `.claude/commands/generate-bdd.md` - Removed `/execute-tests` reference
   - `installer/global/commands/generate-bdd.md` - Removed `/execute-tests` reference
   - `installer/global/commands/feature-generate-tasks.md` - Updated taskwright command references
   - `installer/global/commands/feature-sync.md` - Added notes about taskwright integration
   - `installer/global/commands/feature-create.md` - Updated workflow references
   - `installer/global/commands/epic-status.md` - Updated quick actions
   - `installer/global/commands/epic-create.md` - Added taskwright integration notes
   - `installer/global/commands/hierarchy-view.md` - Updated quick actions and workflow references
   - `installer/global/commands/feature-status.md` - Updated cross-command navigation

### Result

The `.claude/commands/` directory now contains only require-kit commands:
- gather-requirements.md
- formalize-ears.md
- generate-bdd.md

All taskwright commands have been moved to `.claude/commands/.deprecated/taskwright/` with a clear README explaining their relocation and how to access them through taskwright integration.

Documentation has been updated to clarify that task execution features require taskwright integration, with references to INTEGRATION-GUIDE.md for setup instructions.
