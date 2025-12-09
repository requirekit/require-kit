---
id: TASK-PD-RK01
title: Consolidate duplicate agent files
status: completed
created: 2025-12-09T11:00:00Z
updated: 2025-12-09T12:30:00Z
completed: 2025-12-09T12:30:00Z
priority: high
tags: [progressive-disclosure, cleanup, wave-1]
task_type: implementation
complexity: 2
execution_mode: direct
wave: 1
conductor_workspace: null
parallel: false
blocking: true
parent_review: TASK-REV-PD01
---

# Task: Consolidate duplicate agent files

## Description

RequireKit has duplicate agent files in two locations:
- `installer/global/agents/bdd-generator.md` (606 lines, 18KB) - **Authoritative**
- `.claude/agents/bdd-generator.md` (349 lines, 10KB) - **Simplified copy**

The global version is more comprehensive and should be the single source of truth. The local `.claude/agents/` version should be a symlink or removed during installation.

## Execution Mode

**Direct Claude Code** - Simple file operations, no quality gates needed.

## Acceptance Criteria

- [x] Verify `installer/global/agents/bdd-generator.md` is superset of `.claude/agents/bdd-generator.md`
- [x] Document any content in local that's missing from global (if any)
- [x] Update installation scripts to handle agent file distribution correctly
- [x] Ensure `.claude/agents/` gets populated from `installer/global/agents/` during install

## Implementation Steps

1. **Compare files**:
   ```bash
   diff installer/global/agents/bdd-generator.md .claude/agents/bdd-generator.md
   diff installer/global/agents/requirements-analyst.md .claude/agents/requirements-analyst.md
   ```

2. **Verify global is authoritative**:
   - Check that all content in local files exists in global versions
   - Note any unique content in local files

3. **Update install.sh** (if needed):
   - Ensure agent files are copied from `installer/global/agents/` to `.claude/agents/`
   - Or create symlinks during installation

4. **Remove local duplicates** (optional):
   - If symlinks are used, remove static copies
   - Keep `.claude/agents/` directory for project-specific agent overrides

## Files to Modify

- `installer/scripts/install.sh` - Agent file distribution logic
- `.claude/agents/bdd-generator.md` - May be removed or replaced with symlink
- `.claude/agents/requirements-analyst.md` - May be removed or replaced with symlink

## Dependencies

None - this is a prerequisite task.

## Blocks

- TASK-PD-RK03 (Split bdd-generator.md)
- TASK-PD-RK04 (Split requirements-analyst.md)

## Estimated Effort

15 minutes

## Notes

This cleanup ensures we only need to apply progressive disclosure to one set of agent files (the authoritative global versions), not maintain parallel split files.

## Implementation Summary (Completed 2025-12-09)

### Analysis Results

**bdd-generator.md comparison:**
- Global version (607 lines): Comprehensive with framework-specific step definitions (pytest-bdd, SpecFlow, Cucumber.js), LangGraph integration examples, documentation level handling
- Local version (350 lines): Simplified, missing many examples, referenced "Guardkit" instead of "TaskWright"
- **Verdict**: Global is authoritative superset, local had no unique content

**requirements-analyst.md comparison:**
- Global version (389 lines): Complete metadata frontmatter (stack, phase, capabilities, keywords), model rationale, documentation level awareness section
- Local version (187 lines): Minimal metadata, missing many sections
- **Verdict**: Global is authoritative superset, local had no unique content

### Changes Made

1. **Removed duplicate agent files from `.claude/agents/`**:
   - `git rm .claude/agents/bdd-generator.md`
   - `git rm .claude/agents/requirements-analyst.md`

2. **Created `.claude/agents/.gitkeep`**: Documentation explaining:
   - Agent source hierarchy (Local > User > Global)
   - How installation works (copies from `installer/global/agents/` to `~/.agentecflow/agents/require-kit/`)
   - When to add project-specific agents to this directory
   - Frontmatter requirements for custom agents

3. **No changes needed to `install.sh`**: Already correctly handles agent distribution by copying from `installer/global/agents/` to `~/.agentecflow/agents/require-kit/`

### Files Changed

- `.claude/agents/bdd-generator.md` - REMOVED
- `.claude/agents/requirements-analyst.md` - REMOVED
- `.claude/agents/.gitkeep` - CREATED (documentation)
