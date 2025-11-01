---
id: REQ-001B
title: "Extract Requirements Commands"
created: 2025-10-27
status: backlog
priority: high
complexity: 4
parent_task: REQ-001
subtasks: []
estimated_hours: 2
---

# REQ-001B: Extract Requirements Commands

## Description

Extract requirements-focused commands from ai-engineer to require-kit, removing any dependencies on task execution features.

## Commands to Extract

### Core Requirements Commands

```bash
✅ gather-requirements.md     # Interactive requirements gathering
✅ formalize-ears.md          # Convert to EARS notation
✅ generate-bdd.md            # Generate BDD/Gherkin scenarios
```

### Epic/Feature Management

```bash
✅ epic-create.md             # Create epic
✅ epic-status.md             # View epic status
✅ feature-create.md          # Create feature
✅ feature-status.md          # View feature status
✅ hierarchy-view.md          # Visualize epic/feature hierarchy
```

### Conditional Extraction

```bash
? epic-sync.md               # Only if NOT PM tool specific
? feature-sync.md            # Only if NOT PM tool specific
? epic-generate-features.md  # Evaluate usefulness
? feature-generate-tasks.md  # EXCLUDE (task-specific)
```

## Commands to Exclude

```bash
❌ task-create.md
❌ task-work.md
❌ task-complete.md
❌ task-status.md
❌ task-refine.md
❌ task-sync.md
❌ figma-to-react.md
❌ zeplin-to-maui.md
❌ debug.md
❌ portfolio-dashboard.md (if task-focused)
```

## Modifications Required

### 1. Remove Task Execution References

**In all commands, remove**:
- References to task-work
- References to quality gates (Phase 2.5, 4.5)
- References to test execution
- References to implementation

**Example**: In `feature-create.md`, remove:
```
After creating features, use /feature-generate-tasks to break into tasks
Then use /task-work to implement
```

**Keep**:
- Requirements gathering logic
- EARS notation formatting
- BDD scenario generation
- Epic/feature hierarchy management

### 2. Update generate-bdd.md

**Remove**:
- Integration with task-work
- Test execution references

**Keep**:
- Gherkin scenario generation
- Scenario validation
- Requirements traceability

### 3. Update hierarchy-view.md

**Simplify to**:
- Epic/feature tree visualization
- Requirements traceability view
- Progress based on requirements completion (not task execution)

**Remove**:
- Task completion tracking
- Implementation progress
- Quality gate status

## Implementation Steps

```bash
cd /path/to/ai-engineer/installer/global/commands

# Copy core requirements commands
cp gather-requirements.md /path/to/require-kit/requirements/commands/
cp formalize-ears.md /path/to/require-kit/requirements/commands/
cp generate-bdd.md /path/to/require-kit/requirements/commands/

# Copy epic/feature commands
cp epic-create.md /path/to/require-kit/requirements/commands/
cp epic-status.md /path/to/require-kit/requirements/commands/
cp feature-create.md /path/to/require-kit/requirements/commands/
cp feature-status.md /path/to/require-kit/requirements/commands/
cp hierarchy-view.md /path/to/require-kit/requirements/commands/
```

### Edit Commands

```bash
cd /path/to/require-kit/requirements/commands/

# For each command file:
# 1. Remove references to task execution
# 2. Remove quality gate references
# 3. Remove template/stack references
# 4. Keep requirements management logic

# Verify no task execution references remain
grep -r "task-work\|quality.*gate\|Phase [234]\\.[567]" *.md
# Should return EMPTY
```

## Verification

```bash
# Check extracted commands
ls -la /path/to/require-kit/requirements/commands/

# Verify no task execution references
grep -ri "task-work\|implementation\|quality.*gate\|test.*execution" *.md | \
  grep -v "# Historical" | grep -v "# Note:"

# Should be EMPTY or only historical context
```

## Acceptance Criteria

- [ ] 8 core requirements commands extracted
- [ ] gather-requirements.md: No task references
- [ ] formalize-ears.md: Pure EARS formatting
- [ ] generate-bdd.md: Pure scenario generation
- [ ] epic-create.md: No task generation references
- [ ] feature-create.md: No task generation references
- [ ] hierarchy-view.md: Requirements hierarchy only
- [ ] No references to task execution in any command
- [ ] All commands focused on requirements management

## Estimated Time

2 hours

## Notes

- Be thorough with grep verification
- Keep commands focused on requirements gathering/management
- Remove all execution/implementation references
- Document what was changed in each file
