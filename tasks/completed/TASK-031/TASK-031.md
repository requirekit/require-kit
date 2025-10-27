---
id: TASK-031
title: Fix task-work and task-complete State Loss in Conductor Workspaces
status: completed
created: 2025-10-18T16:30:00Z
updated: 2025-10-18T17:30:00Z
completed_at: 2025-10-18T17:30:00Z
priority: high
tags: [bug-fix, conductor-integration, workflow, state-management, critical, completed]
estimated_effort: 6 hours
actual_effort: 45 minutes
time_savings: 5.25 hours
efficiency_gain: 87.5%
complexity_estimate: 7
complexity_actual: 3
complexity_reduction: 57%
related_tasks: [TASK-026, TASK-027]
affected_commands: [task-work, task-complete]
previous_state: in_review
state_transition_reason: "Task completion - all quality gates passed, production ready"
completed_location: tasks/completed/TASK-031/
organized_files:
  - TASK-031.md
  - implementation-summary.md
  - test-summary.md
  - test-results.md
test_results:
  status: passed
  total_tests: 25
  passed: 25
  failed: 0
  coverage_line: 100
  coverage_branch: 0
  duration_seconds: 0.47
architectural_review:
  score: 62
  status: approved_with_recommendations
  design: simplified_utility_functions
  yagni_compliant: true
  pattern: utility_module_not_facade
complexity_evaluation:
  score: 3
  level: simple
  review_mode: AUTO_PROCEED
  files_created: 1
  files_modified: 4
code_review:
  score: 9.8
  grade: A+
  status: approved_for_production
  blockers: 0
  security_issues: 0
deployment:
  ready: true
  environment: production
  risk_level: low
  rollback_plan: available
---

# Fix task-work and task-complete State Loss in Conductor Workspaces

## Problem Statement

**Issue**: When using `/task-work` and `/task-complete` commands in Conductor workspaces (git worktrees), implementation summaries and state metadata are lost after merging back to main.

**Evidence**:
- TASK-026 and TASK-027 were both executed in separate Conductor workspaces
- Both tasks used `/task-work` and `/task-complete` commands
- After merge to main, the following data was missing:
  - Implementation summary files
  - Test execution logs
  - Quality gate results
  - Architectural review scores
  - Complexity evaluation results
  - Phase execution metadata

**Additional symptom**: User had to provide full path to task file instead of just task ID.

## Root Cause Hypotheses

### Hypothesis 1: State Files Not Committed in Worktree
**Theory**: Implementation summary files are created in `docs/state/{task_id}/` but not automatically committed in the Conductor workspace.

**Check**:
```bash
# In Conductor workspace
git status after /task-work
git status after /task-complete
# Are docs/state files shown as untracked?
```

**If true**: Commands should auto-stage state files or warn about uncommitted state.

### Hypothesis 2: State Directory Not Shared Between Worktrees
**Theory**: Conductor workspaces have separate `.git` directories, causing state files to be isolated per worktree.

**Check**:
```bash
# Compare state directories
ls -la docs/state/ in main
ls -la docs/state/ in conductor workspace
```

**If true**: Need worktree-aware state management.

### Hypothesis 3: Path Resolution Issues in Worktrees
**Theory**: Commands assume standard directory structure, fail to resolve paths correctly in worktrees.

**Evidence**: User had to provide full path to task file (workaround).

**Check**:
```bash
# Test path resolution
/task-work TASK-026              # Fails?
/task-work /full/path/TASK-026   # Works?
```

**If true**: Need worktree-aware path resolution logic.

### Hypothesis 4: State Merge Conflicts
**Theory**: State files are created but lost during merge due to conflicts or .gitignore rules.

**Check**:
```bash
# Check .gitignore
grep "docs/state" .gitignore
grep "implementation_plan" .gitignore
```

**If true**: Need to ensure state files are tracked and merged correctly.

### Hypothesis 5: Incomplete Task Metadata Updates
**Theory**: Task frontmatter is updated in worktree but changes are lost on merge.

**Check**:
```bash
# Compare task file frontmatter
# In worktree after /task-complete
# In main after merge
diff tasks/completed/TASK-026.md (worktree vs main)
```

**If true**: Task file updates aren't being committed properly.

## Expected Behavior

When using `/task-work` and `/task-complete` in Conductor workspaces:

1. **State Files Created**:
   ```
   docs/state/TASK-026/
     ├── implementation_plan.md
     ├── architectural_review.json
     ├── complexity_score.json
     ├── test_results.json
     ├── code_review.json
     └── plan_audit.json
   ```

2. **State Files Committed**:
   - All state files automatically staged
   - Included in worktree commits
   - Merged to main without loss

3. **Task Metadata Updated**:
   ```yaml
   ---
   id: TASK-026
   status: completed
   completed_at: 2025-10-18T13:42:00Z
   test_results:
     status: passed
     coverage: 95.2
   architectural_review:
     score: 88
   complexity_evaluation:
     score: 6
   ---
   ```

4. **Path Resolution Works**:
   ```bash
   # Should work in any workspace
   /task-work TASK-026
   /task-complete TASK-026

   # Should NOT require:
   /task-work /full/path/to/tasks/backlog/TASK-026.md
   ```

## Acceptance Criteria

### 1. Investigate and Document Root Cause
- [ ] Reproduce the issue in a Conductor workspace
- [ ] Identify which hypothesis (1-5) is correct
- [ ] Document exact failure mode
- [ ] Create test case that demonstrates the bug

### 2. Fix State File Persistence
- [ ] Ensure state files are created correctly in worktrees
- [ ] Auto-commit state files when created
- [ ] Add git hooks or command logic to track state
- [ ] Verify state files merge to main without loss

### 3. Fix Path Resolution
- [ ] Detect when running in Conductor workspace
- [ ] Resolve task file paths correctly in worktrees
- [ ] Support both relative and absolute paths
- [ ] Work from any directory in worktree

### 4. Fix Task Metadata Updates
- [ ] Ensure task frontmatter updates are committed
- [ ] Preserve all metadata during merge
- [ ] Validate metadata completeness after merge
- [ ] Auto-move task files to correct state directories

### 5. Add Conductor-Specific Validations
- [ ] Detect Conductor workspace environment
- [ ] Warn if state files aren't committed
- [ ] Provide clear error messages for path issues
- [ ] Validate state before allowing /task-complete

### 6. Create Conductor Workflow Guide
- [ ] Document best practices for Conductor usage
- [ ] Add pre-merge checklist
- [ ] Include troubleshooting section
- [ ] Provide recovery steps for lost state

## Technical Investigation

### Step 1: Reproduce in Conductor Workspace
```bash
# Create test Conductor workspace
cd ~/test-ai-engineer
conductor create-workspace test-task-031

# Create test task
/task-create "Test Conductor workflow" priority:high

# Work on task
/task-work TASK-031-TEST

# Check state files
ls -la docs/state/TASK-031-TEST/
git status

# Complete task
/task-complete TASK-031-TEST

# Check what's committed
git log --stat -1
git status

# Merge to main
git checkout main
git merge test-task-031

# Verify state persisted
ls -la docs/state/TASK-031-TEST/
cat tasks/completed/TASK-031-TEST.md
```

### Step 2: Analyze Command Execution
```python
# Check task-work.md command specification
# installer/global/commands/task-work.md

# Key questions:
# 1. Where does it create state files?
# 2. Does it commit them automatically?
# 3. Does it use relative or absolute paths?
# 4. Does it handle worktrees differently?
```

### Step 3: Check Git Worktree Behavior
```bash
# Compare git behavior
git worktree list
git rev-parse --git-common-dir
git rev-parse --git-dir

# Check if state is in common dir or worktree-specific
```

### Step 4: Review State Management Code
Files to check:
- `installer/global/commands/lib/state_manager.py` (if exists)
- `installer/global/commands/lib/plan_persistence.py`
- `installer/global/commands/lib/metrics_tracker.py`
- `installer/global/commands/lib/phase_execution.py`

Look for:
- Path resolution logic
- File creation logic
- Git commit logic
- Worktree detection

## Proposed Solutions

### Solution 1: Auto-Commit State Files
**Where**: In `task-work` and `task-complete` commands

```python
def save_state_with_commit(task_id, state_data):
    # Save state files
    state_dir = Path("docs/state") / task_id
    state_dir.mkdir(parents=True, exist_ok=True)

    # Save all state files
    save_implementation_plan(state_dir / "implementation_plan.md")
    save_test_results(state_dir / "test_results.json")
    save_code_review(state_dir / "code_review.json")
    # ... etc

    # Auto-commit state files (NEW)
    run_command(f"git add docs/state/{task_id}/")
    run_command(f'git commit -m "Save state for {task_id}"')

    return state_dir
```

**Pros**: Ensures state is never lost
**Cons**: Creates extra commits in worktree

### Solution 2: Worktree-Aware Path Resolution
**Where**: In path resolution utility

```python
def resolve_task_path(task_id_or_path):
    # If full path provided, use it
    if Path(task_id_or_path).exists():
        return Path(task_id_or_path)

    # If task ID, search all task directories
    # Handle both main and worktree directories
    search_dirs = [
        "tasks/backlog",
        "tasks/in_progress",
        "tasks/in_review",
        "tasks/blocked",
        "tasks/completed"
    ]

    # Get git root (works in worktrees)
    git_root = run_command("git rev-parse --show-toplevel").strip()

    for search_dir in search_dirs:
        pattern = Path(git_root) / search_dir / f"{task_id_or_path}*.md"
        matches = list(Path(git_root).glob(str(pattern)))
        if matches:
            return matches[0]

    raise FileNotFoundError(f"Task {task_id_or_path} not found")
```

**Pros**: Works in any workspace
**Cons**: Requires git command execution

### Solution 3: Pre-Merge Validation Hook
**Where**: Git hook or command wrapper

```bash
#!/bin/bash
# .git/hooks/pre-merge-commit or conductor-merge-wrapper.sh

# Before merging worktree to main
echo "Validating Conductor workspace before merge..."

# Check for uncommitted state files
uncommitted=$(git status --porcelain | grep "docs/state/")
if [ -n "$uncommitted" ]; then
    echo "❌ ERROR: Uncommitted state files found:"
    echo "$uncommitted"
    echo ""
    echo "Please commit state files before merging:"
    echo "  git add docs/state/"
    echo "  git commit -m 'Add task state files'"
    exit 1
fi

# Check for completed tasks
completed_tasks=$(find tasks/completed -name "*.md" -type f)
for task in $completed_tasks; do
    task_id=$(basename "$task" .md)

    # Validate state directory exists
    if [ ! -d "docs/state/$task_id" ]; then
        echo "❌ WARNING: Completed task $task_id has no state directory"
        echo "   Expected: docs/state/$task_id/"
    fi
done

echo "✅ Conductor workspace validation passed"
```

**Pros**: Catches issues before merge
**Cons**: Requires git hook setup

### Solution 4: Centralized State in Common Git Dir
**Where**: State file storage location

```python
def get_state_dir(task_id):
    # Store state in git common dir (shared across worktrees)
    git_common_dir = run_command("git rev-parse --git-common-dir").strip()
    state_dir = Path(git_common_dir).parent / "docs" / "state" / task_id
    state_dir.mkdir(parents=True, exist_ok=True)
    return state_dir
```

**Pros**: State shared across all worktrees automatically
**Cons**: Changes file organization, may conflict with existing logic

## Testing Strategy

### Manual Testing in Conductor
1. Create Conductor workspace
2. Create task with `/task-create`
3. Work on task with `/task-work`
4. Verify state files created
5. Verify git status shows state files
6. Complete task with `/task-complete`
7. Commit and merge to main
8. Verify state persisted in main

### Automated Testing
```python
# tests/integration/test_conductor_workflow.py

def test_task_work_in_conductor_workspace():
    # Setup Conductor workspace
    workspace = create_conductor_workspace("test-workspace")

    # Create and work on task
    task_id = run_command("/task-create 'Test task'")
    run_command(f"/task-work {task_id}")

    # Verify state files exist
    assert Path(f"docs/state/{task_id}/implementation_plan.md").exists()
    assert Path(f"docs/state/{task_id}/test_results.json").exists()

    # Verify state files are tracked
    git_status = run_command("git status --porcelain")
    assert f"docs/state/{task_id}/" in git_status

    # Complete and merge
    run_command(f"/task-complete {task_id}")
    merge_to_main(workspace)

    # Verify state persisted in main
    checkout_main()
    assert Path(f"docs/state/{task_id}/implementation_plan.md").exists()

    # Verify task metadata complete
    task_file = find_task_file(task_id)
    metadata = parse_frontmatter(task_file)
    assert metadata['status'] == 'completed'
    assert metadata['test_results']['status'] == 'passed'
    assert metadata['architectural_review']['score'] > 0
```

### Regression Testing
Test that fix doesn't break:
- Regular workflow (non-Conductor)
- Parallel Conductor workspaces
- Existing completed tasks
- State file reading

## Implementation Plan

### Phase 1: Investigation (2 hours)
1. Reproduce issue in Conductor workspace
2. Identify root cause (which hypothesis)
3. Document exact failure scenario
4. Create minimal test case

### Phase 2: Fix Implementation (2 hours)
1. Implement path resolution fix (Solution 2)
2. Implement auto-commit logic (Solution 1)
3. Add worktree detection
4. Add validation warnings

### Phase 3: Testing (1 hour)
1. Manual testing in Conductor
2. Automated integration tests
3. Regression testing
4. Edge case testing

### Phase 4: Documentation (1 hour)
1. Update command specifications
2. Create Conductor workflow guide
3. Add troubleshooting section
4. Document recovery procedures

## Success Metrics

### Immediate (After Fix)
- [ ] State files persist after Conductor merge (100%)
- [ ] Path resolution works without full path (100%)
- [ ] Task metadata preserved in frontmatter (100%)
- [ ] All quality gate data retained (100%)

### Long-term (30 days)
- [ ] Zero reported state loss issues in Conductor
- [ ] Conductor workflow adoption increases (if easier)
- [ ] Documentation reduces support questions by 80%

## Files to Modify

### Core Implementation
- `installer/global/commands/task-work.md` (add worktree handling)
- `installer/global/commands/task-complete.md` (add state validation)
- `installer/global/commands/lib/path_resolver.py` (worktree-aware paths)
- `installer/global/commands/lib/state_manager.py` (auto-commit logic)

### Documentation
- `docs/guides/conductor-integration.md` (update with workflow)
- `CLAUDE.md` (add Conductor best practices)
- `docs/troubleshooting/conductor-state-loss.md` (new)

### Testing
- `tests/integration/test_conductor_workflow.py` (new)
- `tests/unit/test_path_resolution_worktree.py` (new)

## Rollout Plan

### Week 1: Development
- Days 1-2: Investigation and root cause
- Days 3-4: Implementation and testing
- Day 5: Documentation

### Week 2: Validation
- Deploy to staging
- Test with real Conductor workflows
- Gather feedback
- Adjust if needed

### Week 3: Production
- Deploy to production
- Monitor for issues
- Update documentation based on usage
- Create recovery playbook

## Risk Mitigation

### Risk 1: Breaking Existing Workflows
**Mitigation**:
- Extensive regression testing
- Feature flag for Conductor-specific behavior
- Rollback plan ready

### Risk 2: Performance Impact
**Mitigation**:
- Benchmark before/after
- Optimize git operations
- Cache path resolutions

### Risk 3: Incomplete State Recovery
**Mitigation**:
- Create recovery script for existing tasks
- Document manual recovery steps
- Provide state reconstruction tools

## Recovery Procedure (For TASK-026 and TASK-027)

Since state was lost for these tasks, we need recovery:

```bash
# Manual recovery for TASK-026
cd tasks/completed
vim TASK-026-create-task-refine-command.md

# Add missing metadata from git history
git log --all --grep="TASK-026" --stat
git show <commit-hash>:docs/state/TASK-026/implementation_plan.md

# Reconstruct state directory
mkdir -p docs/state/TASK-026
# Manually recreate state files from commit history or implementation
```

**Note**: This recovery is manual and time-consuming, which is why the fix is critical.

## Related Issues

- Conductor.build integration (broader topic)
- Parallel development workflows
- Git worktree best practices
- State management architecture

## References

- Conductor.build documentation
- Git worktree documentation
- Existing Conductor integration: `docs/CONDUCTOR-INTEGRATION.md`
- TASK-026 and TASK-027 (affected tasks)

---

**Priority Justification**: HIGH because:
- Affects productivity with Conductor (parallel development tool)
- Data loss is unacceptable (implementation summaries, test results)
- Blocks adoption of Conductor workflows
- Affects quality tracking and metrics
- Currently requires manual workarounds (full paths)

**Estimated Effort**: 6 hours
- Investigation: 2 hours
- Implementation: 2 hours
- Testing: 1 hour
- Documentation: 1 hour

**Complexity**: 7/10 (High-Medium)
- Involves git worktree mechanics
- Path resolution across different environments
- State management architecture
- Backward compatibility required
- Integration with existing commands
