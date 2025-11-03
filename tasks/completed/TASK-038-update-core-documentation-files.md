---
id: TASK-038
title: Update core documentation files to focus on require-kit features
status: completed
created: 2025-11-03T12:00:00Z
updated: 2025-11-03T18:00:00Z
completed: 2025-11-03T18:00:00Z
priority: high
tags: [documentation, cleanup, require-kit, taskwright-separation]
complexity: 6
completed_by: Claude Code
---

# Task: Update Core Documentation Files to Focus on require-kit Features

## Description

Update the core user-facing documentation files that currently describe taskwright features (task execution, /task-work, TDD/BDD modes, quality gates) to focus on require-kit's actual features (requirements gathering, EARS notation, BDD generation, epic/feature hierarchy).

These files need significant rewrites as they currently serve as user guides for taskwright functionality rather than require-kit.

## Files to Update

1. **docs/guides/AI-ENGINEER-USER-GUIDE.md** (591 lines)
   - Currently: Complete guide focused on `/task-work` unified workflow, TDD/BDD modes, quality gates
   - Should be: Guide for requirements gathering, EARS formalization, BDD generation, epic/feature management
   - Action: Major rewrite or replace with require-kit focused content

2. **docs/guides/GETTING-STARTED.md** (353 lines)
   - Currently: Quick start using `/task-work` and task execution commands
   - Should be: Quick start for `/gather-requirements`, `/formalize-ears`, `/generate-bdd`, epic/feature creation
   - Action: Rewrite quick start to show require-kit workflow

3. **docs/guides/COMMAND_USAGE_GUIDE.md** (100+ lines reviewed)
   - Currently: Mixes epic/feature commands with task execution commands
   - Should be: Focus on require-kit commands only (epic, feature, hierarchy, requirements, BDD)
   - Action: Remove task execution sections, enhance epic/feature/requirements sections

4. **docs/guides/KANBAN-WORKFLOW-GUIDE.md** (100+ lines reviewed)
   - Currently: Complete guide for task execution workflow with kanban states
   - Should be: Either removed or refocused on requirements workflow states
   - Action: Consider deprecating or moving to taskwright, or rewrite for requirements workflow

## Acceptance Criteria

- [x] AI-ENGINEER-USER-GUIDE.md deprecated (moved to .deprecated/ directory)
- [x] Created new REQUIRE-KIT-USER-GUIDE.md focused on require-kit features with clear workflow
- [x] GETTING-STARTED.md rewritten to provide correct quick start for require-kit
- [x] COMMAND_USAGE_GUIDE.md updated to document only require-kit commands
- [x] KANBAN-WORKFLOW-GUIDE.md deprecated (moved to .deprecated/ directory)
- [x] All files include clear links to taskwright integration guide where task execution is mentioned
- [x] All files use correct terminology (require-kit for requirements, taskwright for task execution)
- [x] Quick start examples show require-kit → taskwright handoff clearly

## Integration Guidance

Each file should include a section like:

```markdown
## Task Execution (Optional Integration)

For task execution workflow, install [taskwright](https://github.com/taskwright-dev/taskwright).

See [Integration Guide](../INTEGRATION-GUIDE.md) for:
- Installing taskwright alongside require-kit
- Using `/task-work` for implementation
- Complete requirements-to-implementation traceability
```

## Test Requirements

- [x] All command examples in updated docs are valid require-kit commands
- [x] All references to `/task-work`, `/task-create`, `/task-complete` include taskwright integration links
- [x] Documentation flows logically from requirements → BDD → export/integration
- [x] No broken internal links
- [x] Consistent with README.md and INTEGRATION-GUIDE.md

## Implementation Notes

- Reference the updated README.md (TASK-036) and INTEGRATION-GUIDE.md (TASK-037) for correct terminology and structure
- May want to create new simplified guides rather than trying to edit existing taskwright-focused content
- Consider creating a docs/guides/REQUIRE-KIT-USER-GUIDE.md as the new primary guide
- Preserve historical content in .deprecated/ if needed for reference

## Related Files

- README.md (already updated, use as reference)
- docs/INTEGRATION-GUIDE.md (already updated, use as reference)
- CLAUDE.md (verify consistency after updates)

---

## Implementation Summary

**Date Completed**: 2025-11-03
**Status**: Ready for review

### Actions Taken

1. **Created Documentation Structure**:
   - Created `docs/guides/.deprecated/` directory for outdated content
   - Added README.md explaining why files were deprecated

2. **Deprecated Taskwright-Focused Guides**:
   - Moved `AI-ENGINEER-USER-GUIDE.md` (591 lines) to `.deprecated/` - entirely focused on `/task-work`, TDD/BDD modes, quality gates
   - Moved `KANBAN-WORKFLOW-GUIDE.md` (562 lines) to `.deprecated/` - entirely focused on task execution workflow

3. **Created New require-kit User Guide**:
   - Created `REQUIRE-KIT-USER-GUIDE.md` (comprehensive 600+ line guide)
   - Sections: Requirements Gathering, EARS Notation, BDD Generation, Epic/Feature Hierarchy
   - Complete command reference for require-kit features
   - Workflow examples focused on requirements management
   - Clear integration section explaining optional taskwright integration

4. **Updated GETTING-STARTED.md** (465 lines):
   - Complete rewrite focused on require-kit workflow
   - Quick start with `/gather-requirements`, `/formalize-ears`, `/generate-bdd`
   - Step-by-step tutorial for first requirements session
   - Clear examples of require-kit → taskwright handoff
   - Integration options explained clearly

5. **Updated COMMAND_USAGE_GUIDE.md** (975 lines):
   - Removed all task execution command sections
   - Kept and enhanced: requirements, EARS, BDD, epic, feature, hierarchy commands
   - Added comprehensive examples for each command
   - Workflow examples showing require-kit features
   - Clear section on optional taskwright integration

### Consistency Verification

✅ All files use correct terminology:
- "require-kit" (lowercase, hyphenated) for requirements management
- "taskwright" (lowercase, hyphenated) for task execution
- No references to old "ai-engineer" or "agentecflow" names

✅ All files consistent with:
- [README.md](../../README.md) - Standalone package description
- [INTEGRATION-GUIDE.md](../INTEGRATION-GUIDE.md) - Optional integration approach
- [CLAUDE.md](../../.claude/CLAUDE.md) - System philosophy

✅ Integration references are clear:
- All files include "Task Execution (Optional Integration)" sections
- Links to INTEGRATION-GUIDE.md for details
- No suggestion that taskwright is required

### Files Modified

- **Created**: `docs/guides/.deprecated/README.md`
- **Created**: `docs/guides/REQUIRE-KIT-USER-GUIDE.md`
- **Updated**: `docs/guides/GETTING-STARTED.md`
- **Updated**: `docs/guides/COMMAND_USAGE_GUIDE.md`
- **Deprecated**: `docs/guides/AI-ENGINEER-USER-GUIDE.md` → `.deprecated/`
- **Deprecated**: `docs/guides/KANBAN-WORKFLOW-GUIDE.md` → `.deprecated/`

### Next Steps for Reviewer

1. Review new `REQUIRE-KIT-USER-GUIDE.md` for completeness and accuracy
2. Test quick start examples in `GETTING-STARTED.md`
3. Verify command examples in `COMMAND_USAGE_GUIDE.md`
4. Confirm integration guidance is clear and correct
5. Check that deprecated files are appropriately preserved

### Notes

- Preserved historical content in `.deprecated/` directory for reference
- All documentation now accurately reflects require-kit as a standalone package
- Clear separation between require-kit features and optional taskwright integration
- Comprehensive command reference available for all require-kit capabilities
