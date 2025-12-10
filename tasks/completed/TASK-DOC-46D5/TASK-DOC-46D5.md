---
id: TASK-DOC-46D5
title: Fix documentation gaps from TASK-REV-F2E1 review
status: completed
created: 2025-12-10T08:50:00Z
updated: 2025-12-10T09:35:00Z
completed: 2025-12-10T09:35:00Z
priority: normal
tags: [documentation, progressive-disclosure, clarifying-questions]
task_type: implementation
complexity: 3
related_tasks: [TASK-REV-F2E1]
completed_location: tasks/completed/TASK-DOC-46D5/
---

# Task: Fix Documentation Gaps from Review

## Description

Address the Priority 1 documentation issues identified in TASK-REV-F2E1 review.

## Background

Review TASK-REV-F2E1 identified 4 documentation improvements needed:

1. formalize-ears.md missing clarifying questions section
2. Inconsistent loading instruction format across files
3. README.md missing loading instructions for extended content
4. Root CLAUDE.md missing clarification mention

## Implementation

### 1. Add Clarifying Questions to formalize-ears.md

**File**: `.claude/commands/formalize-ears.md`

Add clarifying questions section similar to epic-create.md and feature-create.md:

```markdown
## Clarifying Questions (Interactive Mode)

When formalizing requirements interactively, these questions help ensure proper EARS patterns:

### 1. EARS Pattern Selection
```
What type of requirement is this?

Options:
- Ubiquitous (always active): "The system shall..."
- Event-driven (triggered): "When X, the system shall..."
- State-driven (conditional): "While X, the system shall..."
- Unwanted behavior (error): "If X, then the system shall..."
- Optional feature: "Where X, the system shall..."
```

### 2. Trigger/Condition Clarity
```
What triggers this requirement or under what conditions does it apply?
[Be specific about the event, state, or condition]
```

### 3. Measurable Outcomes
```
How will we know this requirement is met?
[Provide specific, measurable acceptance criteria]
```

### Skipping Clarification

```bash
# With explicit pattern (skips pattern question)
/formalize-ears "Users login" --pattern event-driven

# Auto-detect pattern
/formalize-ears "Users login" --auto

# Quick mode (minimal questions)
/formalize-ears "Users login" --quick
```
```

### 2. Standardize Loading Instructions

Update all files to use consistent format:

**Standard format**:
```markdown
## Loading Extended Content

For [detailed content description], load the extended file:

```bash
cat installer/global/agents/{name}-ext.md
```
```

**Files to update**:
- `installer/global/agents/bdd-generator.md` - Change "Read file" to `cat` command
- `installer/global/agents/requirements-analyst.md` - Add `cat` command format

### 3. Add Loading Instructions to README.md

Add after "Efficient Context Management" section:

```markdown
**Loading Extended Content**:
```bash
# For BDD generator examples
cat installer/global/agents/bdd-generator-ext.md

# For requirements analyst examples
cat installer/global/agents/requirements-analyst-ext.md
```
```

### 4. Add Clarification Mention to Root CLAUDE.md

Add after Essential Commands section:

```markdown
## Interactive Clarification

Commands `/epic-create`, `/feature-create`, and `/formalize-ears` include optional clarifying questions to improve specifications. Use `--quick` flag to skip questions when parameters are provided directly.

See `docs/INTEGRATION-GUIDE.md` for clarification philosophy details.
```

## Acceptance Criteria

- [x] formalize-ears.md has clarifying questions section
- [x] All agent files use consistent `cat` command format for loading
- [x] README.md includes loading instructions example
- [x] Root CLAUDE.md mentions clarification feature
- [x] INTEGRATION-GUIDE.md table still accurate after changes

## Files to Modify

1. `.claude/commands/formalize-ears.md`
2. `installer/global/agents/bdd-generator.md`
3. `installer/global/agents/requirements-analyst.md`
4. `README.md`
5. `CLAUDE.md`

## Testing

Manual verification:
1. Verify `cat` commands work from project root
2. Verify documentation is consistent across files
3. Verify INTEGRATION-GUIDE.md table matches actual implementation

## Notes

- Keep changes minimal and focused
- Don't add unverified performance claims
- Maintain existing documentation style
