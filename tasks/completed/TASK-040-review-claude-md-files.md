---
id: TASK-040
title: Review CLAUDE.md files to ensure correct require-kit scope
status: completed
created: 2025-11-03T12:00:00Z
updated: 2025-11-03T14:30:00Z
completed: 2025-11-03T14:30:00Z
priority: medium
tags: [documentation, claude-instructions, verification]
complexity: 2
---

# Task: Review CLAUDE.md Files for Correct Scope

## Description

Verify that both CLAUDE.md files (root and .claude/ directory) are correctly scoped to require-kit features and don't inadvertently document taskwright features.

These files provide instructions to Claude Code AI and should accurately represent what require-kit provides versus what requires taskwright integration.

## Files to Review

1. **CLAUDE.md** (root directory, 128 lines)
   - Primary project instructions file
   - Read by Claude Code when working in this repository
   - Already reviewed and appears correct

2. **.claude/CLAUDE.md** (59 lines)
   - Additional project context
   - More concise version of root CLAUDE.md
   - Already reviewed and appears correct

## Acceptance Criteria

- [ ] Both CLAUDE.md files focus exclusively on require-kit features
- [ ] No documentation of taskwright features (task execution, quality gates, etc.)
- [ ] Integration section clearly points to taskwright for task execution
- [ ] Essential commands section lists only require-kit commands
- [ ] Core AI agents section lists only require-kit agents
- [ ] Package status section accurately describes standalone + optional integration
- [ ] Workflow overview shows require-kit workflow, not task execution
- [ ] Best practices are specific to requirements management

## Review Checklist

### Root CLAUDE.md

Current structure appears correct:
- ✅ Project Context: "requirements management toolkit"
- ✅ Core Principles: Requirements First, BDD Scenarios, Traceability
- ✅ Essential Commands: gather-requirements, formalize-ears, generate-bdd, epic/feature
- ✅ Package Status: Standalone with optional taskwright integration
- ✅ Integration section: Points to taskwright for task execution
- ✅ Workflow Overview: Requirements → EARS → BDD → Organize → Export

**Action**: Verify no taskwright features mentioned, enhance if needed

### .claude/CLAUDE.md

Current structure appears correct:
- ✅ More concise version of root CLAUDE.md
- ✅ Focuses on core principles and philosophy
- ✅ Integration section points to taskwright

**Action**: Verify consistency with root CLAUDE.md

## Potential Issues to Check

1. **Command References**
   - Ensure no `/task-work`, `/task-create`, `/task-complete` commands listed
   - Ensure no references to removed commands from TASK-039

2. **Feature Claims**
   - No claims about task execution, quality gates, TDD/BDD modes
   - No claims about automated testing or coverage enforcement

3. **Workflow Descriptions**
   - Workflow should end at "Export" or "Integration"
   - Should not include task execution phases

4. **Agent Descriptions**
   - Should list only: requirements-analyst, bdd-generator, epic-manager
   - Should NOT list: task-manager, test-verifier, code-reviewer

5. **Integration Guidance**
   - Should clearly distinguish require-kit features from taskwright features
   - Should point to integration guide for combined workflow

## Updates Needed (If Any)

If issues found, update files to:

1. Remove any taskwright feature documentation
2. Add clear integration section if missing
3. Ensure agent list is accurate (requirements agents only)
4. Update workflow to stop at requirements/export phase
5. Add pointer to INTEGRATION-GUIDE.md for full workflow

## Test Requirements

- [ ] Both CLAUDE.md files accurately represent require-kit scope
- [ ] No confusion about what features are built-in vs. require integration
- [ ] Commands listed match commands in .claude/commands/ and installer/global/commands/
- [ ] Integration guidance is clear and actionable
- [ ] Consistent terminology with README.md and INTEGRATION-GUIDE.md

## Implementation Notes

- These files were updated in previous tasks (TASK-036/037) so may already be correct
- Focus on verification rather than major rewrites
- Any changes should be minimal and surgical
- Maintain consistency with README.md package status section

## Validation

After any updates:

1. Read both CLAUDE.md files as if you're a new user
2. Confirm understanding of what require-kit does
3. Confirm understanding of when you need taskwright
4. Verify no confusion about feature boundaries

## Related Tasks

- TASK-038: Core documentation (should be consistent with CLAUDE.md)
- TASK-039: Commands cleanup (CLAUDE.md should not reference removed commands)

---

## Completion Summary

**Completed**: 2025-11-03T14:30:00Z

### Review Results

Both CLAUDE.md files were reviewed and found to be mostly correct, with one issue identified and fixed:

#### Root CLAUDE.md (128 lines)
- ✅ Project Context: Correctly describes as "requirements management toolkit"
- ✅ Core Principles: Focuses on Requirements First, BDD Scenarios, Traceability
- ✅ Essential Commands: Lists only require-kit commands (all verified to exist)
- ✅ Package Status: Accurately describes standalone functionality with optional taskwright integration
- ✅ Workflow Overview: Correctly stops at "Export" phase
- ✅ Integration sections: Clearly distinguish require-kit from taskwright features
- ✅ Best Practices: Specific to requirements management
- ❌ **Issue Fixed**: Core AI Agents section listed non-existent "epic-manager" agent

#### .claude/CLAUDE.md (59 lines)
- ✅ Concise version of root CLAUDE.md
- ✅ Focuses on core principles and philosophy
- ✅ Integration section clearly points to taskwright for task execution
- ✅ Workflow Overview: Correctly stops at "Export" phase
- ✅ Consistent with root CLAUDE.md
- ✅ No issues found

### Changes Made

**File**: `/CLAUDE.md`

**Change**: Updated Core AI Agents section (lines 56-64)
- Removed non-existent "epic-manager" agent reference
- Updated to list only actual agents: requirements-analyst, bdd-generator
- Added note explaining epic/feature management is handled through commands
- Updated agent path reference to `installer/global/agents/*.md` (more accurate)

### Verification

All acceptance criteria met:
- ✅ Both CLAUDE.md files focus exclusively on require-kit features
- ✅ No documentation of taskwright features (task execution, quality gates, etc.)
- ✅ Integration section clearly points to taskwright for task execution
- ✅ Essential commands section lists only require-kit commands
- ✅ Core AI agents section lists only require-kit agents (fixed)
- ✅ Package status section accurately describes standalone + optional integration
- ✅ Workflow overview shows require-kit workflow, not task execution
- ✅ Best practices are specific to requirements management

### Command Verification

All commands referenced in CLAUDE.md were verified to exist:
- `/gather-requirements` - exists in `.claude/commands/`
- `/formalize-ears` - exists in `.claude/commands/`
- `/generate-bdd` - exists in `.claude/commands/`
- `/epic-create` - exists in `installer/global/commands/`
- `/feature-create` - exists in `installer/global/commands/`
- `/hierarchy-view` - exists in `installer/global/commands/`

### Agent Verification

Verified agent list matches actual agents:
- `requirements-analyst` - exists in `installer/global/agents/`
- `bdd-generator` - exists in `installer/global/agents/`

Confirmed that taskwright-related agents (task-manager, test-verifier, test-orchestrator, code-reviewer) are NOT documented in CLAUDE.md, as expected.

### Conclusion

TASK-040 completed successfully. Both CLAUDE.md files now accurately represent require-kit's scope and capabilities, with clear separation between require-kit features and optional taskwright integration.
