# Task ID Duplication Analysis & Resolution

## Problem Summary

The agentecflow_platform repo encountered task ID duplication when using `/feature-generate-tasks`. Multiple features created overlapping task numbers because each feature started task numbering independently.

## Root Cause

### Issue Pattern
```
FEAT-001.1 → Generated TASK-001.1.x (TASK-001.1, TASK-001.2, ..., TASK-001.8)
FEAT-001.2 → Generated TASK-001.13+ (started from a different number)
FEAT-001.3 → Generated TASK-001.21+ (different starting point)
FEAT-001.4 → Generated TASK-001.30+ (different starting point)
```

**Problem**: The command doesn't check for the highest existing task number before generating new tasks. It assumes each feature can have its own task numbering range.

### Duplicate Task IDs Found (Example from EPIC-001)
- `TASK-001.13`: design-requirements-schema (FEAT-001.3) vs ears-parser-unit-tests (FEAT-001.2)
- `TASK-001.14`: implement-sqlalchemy-models (FEAT-001.3) vs requirement-generator-unit-tests (FEAT-001.2)
- `TASK-001.15-25`: Similar pattern continues

## Current Directory Structure (Fixed)

✅ Consolidation complete in agentecflow_platform:
```
docs/
├── epics/
│   ├── active/
│   ├── planned/
│   │   ├── EPIC-001-requirements-mcp-server.md
│   │   └── EPIC-001-FEATURES-SUMMARY.md
│   └── ROADMAP.md
├── features/
│   ├── active/
│   │   ├── FEAT-001.1-specification-analysis-tools.md
│   │   ├── FEAT-001.2-ears-requirements-engine.md
│   │   ├── FEAT-001.3-requirements-storage-retrieval.md
│   │   └── FEAT-001.4-langgraph-orchestration.md
│   └── completed/
└── tasks/
    ├── active/
    ├── backlog/
    │   ├── TASK-001.01-mcp-server-skeleton.md
    │   ├── TASK-001.02-gather-requirements-tool.md
    │   ├── ...
    │   └── TASK-001.35-performance-optimization.md
    ├── blocked/
    └── completed/
```

**Note**: Tasks have been renumbered sequentially (TASK-001.01 through TASK-001.35) to resolve duplicates.

## Solutions Required

### 1. Task ID Generation Logic Update ⚠️ CRITICAL

**Current Broken Behavior**:
```python
# feature-generate-tasks command (current)
def generate_task_id(feature_id):
    # ❌ Starts from feature-specific number without checking existing tasks
    return f"TASK-{epic_num}.{feature_num}.1"
```

**Required Fixed Behavior**:
```python
# feature-generate-tasks command (fixed)
def generate_task_id(epic_id):
    # ✅ Find highest existing task number in entire epic
    existing_tasks = glob.glob(f"docs/tasks/**/**/TASK-{epic_num}.*.md")
    max_task_num = max([extract_task_num(task) for task in existing_tasks] or [0])
    next_task_num = max_task_num + 1
    return f"TASK-{epic_num}.{next_task_num:02d}"  # Zero-padded
```

### 2. Task Numbering Strategy

**Recommended Approach**: Sequential numbering per epic

| Epic | Feature | Task Range | Example |
|------|---------|------------|---------|
| EPIC-001 | ALL | 001-999 | TASK-001.01, TASK-001.02, ... |
| EPIC-002 | ALL | 001-999 | TASK-002.01, TASK-002.02, ... |

**Benefits**:
- ✅ No task ID conflicts within an epic
- ✅ Simple to understand and maintain
- ✅ Easy to find highest task number
- ✅ Clear epic association

**Alternative (NOT Recommended)**: Feature-specific numbering
```
EPIC-001
├── FEAT-001.1 → TASK-001.1.01, TASK-001.1.02, ...
├── FEAT-001.2 → TASK-001.2.01, TASK-001.2.02, ...
```
❌ **Problem**: More complex, harder to track unique IDs

### 3. Commands Requiring Updates

#### High Priority (Create Tasks)
1. **`/feature-generate-tasks`** ⭐⭐⭐
   - Add: Check existing task numbers before generation
   - Add: Sequential numbering logic
   - Add: Duplicate detection validation

2. **`/task-create`** ⭐⭐⭐
   - Add: Auto-increment from highest existing task
   - Add: Duplicate ID validation
   - Add: Warning if task range seems full

#### Medium Priority (Move/Update Tasks)
3. **`/task-work`** ⭐⭐
   - Verify: Task ID doesn't change during move
   - Add: Validation when moving between states

4. **`/task-complete`** ⭐⭐
   - Verify: Task ID preserved in completed directory
   - Add: Check for duplicate in destination

#### Low Priority (Status/Sync)
5. **`/task-status`** ⭐
   - Add: Warning if duplicate task IDs detected

6. **`/task-sync`** ⭐
   - Add: Duplicate validation before sync

### 4. Validation Functions Needed

```bash
# Function 1: Get highest task number for epic
get_max_task_number() {
    epic_id=$1
    # Find all task files for this epic
    # Extract task numbers
    # Return highest number
}

# Function 2: Check for duplicate task IDs
check_duplicate_tasks() {
    task_id=$1
    # Search all task directories
    # Return conflict if found
}

# Function 3: Generate next task ID
generate_next_task_id() {
    epic_id=$1
    max_num=$(get_max_task_number $epic_id)
    next_num=$((max_num + 1))
    printf "TASK-%s.%02d" $epic_num $next_num
}
```

## Implementation Steps

### Phase 1: Immediate Fixes (ai-engineer repo)
1. ✅ Update `/feature-generate-tasks` command
   - Add task number lookup logic
   - Add sequential numbering
   - Add duplicate prevention

2. ✅ Update `/task-create` command
   - Add task number lookup logic
   - Add auto-increment logic
   - Add duplicate validation

### Phase 2: Validation Enhancements
3. ✅ Add validation functions to all task commands
4. ✅ Add duplicate detection to `/task-status`
5. ✅ Add duplicate warnings to `/task-sync`

### Phase 3: Documentation
6. ✅ Update command documentation with numbering rules
7. ✅ Add troubleshooting section for duplicates
8. ✅ Create migration guide for existing projects

## Prevention Checklist

When implementing task ID generation:

- [ ] **Always** check existing task numbers before generating new ID
- [ ] **Never** assume feature-specific numbering is safe
- [ ] **Always** use sequential numbering per epic
- [ ] **Always** validate no duplicate before creating file
- [ ] **Always** use zero-padded numbers for sorting (01, 02, ... 99)
- [ ] **Always** search ALL task directories (backlog, active, completed, blocked)
- [ ] **Never** hard-code task number ranges
- [ ] **Always** provide clear error messages if duplicate detected

## Testing Strategy

### Test Cases to Add
1. **Test**: Generate tasks for multiple features in same epic
   - Expected: Sequential task numbers, no duplicates

2. **Test**: Create manual task in epic with auto-generated tasks
   - Expected: Next manual task continues sequence

3. **Test**: Generate tasks after some tasks are completed
   - Expected: New tasks continue from highest number (not reuse)

4. **Test**: Detect duplicate task ID in different directories
   - Expected: Error with clear conflict message

5. **Test**: Handle task number overflow (>999)
   - Expected: Graceful handling or clear limit message

## Rollout Plan

### For ai-engineer Repo (Source)
1. Update command specifications with new logic
2. Add validation functions
3. Update documentation
4. Test with sample epic/feature structure

### For Existing Projects (agentecflow_platform)
1. Run duplicate detection script (if needed)
2. Renumber conflicting tasks (already done)
3. Update to latest ai-engineer installer
4. Verify no new duplicates occur

## Success Criteria

✅ **No duplicate task IDs** within an epic
✅ **Sequential numbering** that's easy to understand
✅ **Automatic validation** prevents duplicates
✅ **Clear error messages** when conflicts occur
✅ **Documentation** explains numbering strategy
✅ **All commands** respect task ID uniqueness

## Related Files to Update

### ai-engineer Repo
- `/installer/global/commands/feature-generate-tasks.md`
- `/installer/global/commands/task-create.md`
- `/installer/global/commands/task-work.md`
- `/installer/global/commands/task-complete.md`
- `/installer/global/commands/task-status.md`
- `/installer/global/commands/task-sync.md`

### Documentation
- `CLAUDE.md` (project instructions)
- Task management workflow docs
- Troubleshooting guides

---

**Created**: 2025-10-04
**Status**: Analysis Complete, Implementation Required
**Priority**: HIGH (prevents data corruption and confusion)
