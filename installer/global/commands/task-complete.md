# Task Complete - Finalize Task with Feature/Epic Progress Rollup

Complete tasks with comprehensive validation, automatic progress rollup to features and epics, and external PM tool synchronization.

## Feature Detection and Package Integration

The `/task-complete` command automatically detects which Agentecflow packages are installed and adapts its validation and reporting accordingly, enabling **bidirectional optional integration** between taskwright and require-kit.

### Package-Specific Features

| Installed Packages | Available Features | Unavailable Features |
|-------------------|-------------------|----------------------|
| **taskwright only** | ✅ Task completion workflow<br>✅ Quality gate validation<br>✅ File organization<br>✅ Basic metrics | ❌ Requirements satisfaction check<br>❌ BDD scenario validation<br>❌ Epic/Feature rollup<br>❌ PM tool sync |
| **Both installed** | ✅ All features above<br>✅ Requirements verification<br>✅ BDD scenario validation<br>✅ Epic/Feature progress rollup<br>✅ PM tool synchronization | None - full integration |

### Automatic Detection

The command uses `feature_detection.py` to determine available features:

```python
from lib.feature_detection import (
    is_require_kit_installed,
    supports_requirements,
    supports_epics
)

# Check what validation is available
has_require_kit = is_require_kit_installed()
can_validate_requirements = supports_requirements()
can_rollup_progress = supports_epics()
```

### Graceful Degradation

**When require-kit is not installed:**
- ✅ Task completion proceeds normally
- ✅ Quality gates validated (tests, coverage)
- ✅ Files organized into completed directory
- ℹ️ Requirements satisfaction check skipped
- ℹ️ BDD scenario validation skipped
- ℹ️ Epic/Feature rollup skipped
- ℹ️ PM tool sync skipped

**Example output (taskwright only):**
```
🏁 Completing Task: TASK-045

ℹ️  Package Detection:
- taskwright: ✅ installed
- require-kit: ❌ not installed

📁 Organizing Task Files
✅ Files organized in tasks/completed/TASK-045/

📊 Quality Gates
✅ All tests passing
✅ Coverage: 87.5%

ℹ️  Optional Features Skipped:
- Requirements validation (install require-kit)
- BDD scenario verification (install require-kit)
- Epic/Feature progress rollup (install require-kit)
- PM tool synchronization (install require-kit)

✅ Task completed successfully
```

## Usage
```bash
/task-complete TASK-XXX [options]
```

## Examples
```bash
# Complete task with full validation
/task-complete TASK-045

# Complete with custom completion criteria
/task-complete TASK-045 --criteria-override

# Complete and force sync to PM tools
/task-complete TASK-045 --force-sync

# Complete without triggering rollup (for batch operations)
/task-complete TASK-045 --no-rollup

# Complete with deployment preparation
/task-complete TASK-045 --prepare-deployment

# Interactive completion with validation
/task-complete TASK-045 --interactive
```

## Completion Validation Process

### Pre-Completion Checks (Conditional Based on Installed Packages)

Before marking a task as complete, the system validates based on available features:

**Always Validated (taskwright):**
1. **Acceptance Criteria**: All criteria must be satisfied
2. **Implementation Steps**: All steps marked as complete
3. **Quality Gates**: All gates must pass (tests, coverage, security)
4. **Code Review**: Implementation reviewed and approved
5. **Documentation**: Required documentation completed
6. **External Dependencies**: No blocking dependencies remain

**Additional Validation (require-kit installed):**
7. **Requirements Satisfaction**: All linked EARS requirements verified ✨
8. **BDD Scenarios**: All linked BDD scenarios pass ✨
9. **Epic/Feature Progress**: Progress rollup calculated ✨
10. **PM Tool Sync**: External tools updated if configured ✨

**Validation Logic:**
```python
from lib.feature_detection import supports_requirements, supports_bdd, supports_epics

# Always validate core quality gates
validate_acceptance_criteria()
validate_quality_gates()
validate_code_review()

# Conditional validation based on installed packages
if supports_requirements():
    validate_requirements_satisfaction()  # Only if require-kit installed

if supports_bdd():
    validate_bdd_scenarios()  # Only if require-kit installed

if supports_epics():
    calculate_progress_rollup()  # Only if require-kit installed
```

### File Organization on Completion

When completing a task, the system automatically organizes all task-related files into a dedicated subfolder:

```bash
# Completion process creates organized structure:
tasks/completed/
└── TASK-045/
    ├── TASK-045.md                    # Main task file
    ├── implementation-summary.md       # Any related implementation docs
    ├── completion-report.md           # Completion details
    └── coverage-report.json           # Coverage data (if exists)
```

**File Discovery and Organization Logic:**

1. **Create Task Subfolder**
   ```bash
   # Create dedicated directory for task
   mkdir -p "tasks/completed/${TASK_ID}"
   ```

2. **Move Main Task File**
   ```bash
   # Move task file from in_progress to completed subfolder
   mv "tasks/in_progress/${TASK_ID}.md" "tasks/completed/${TASK_ID}/"
   ```

3. **Discover and Move Related Files**
   ```bash
   # Find all files in project root matching TASK-XXX-*.md pattern
   # Examples: TASK-045-IMPLEMENTATION-SUMMARY.md, TASK-045-COMPLETION-REPORT.md
   find . -maxdepth 1 -name "${TASK_ID}-*.md" -type f

   # Move each related file to the task subfolder
   for file in $(find . -maxdepth 1 -name "${TASK_ID}-*.md"); do
     # Extract suffix and create clean filename
     # TASK-045-IMPLEMENTATION-SUMMARY.md → implementation-summary.md
     suffix=$(echo "$file" | sed "s/.*${TASK_ID}-//")
     mv "$file" "tasks/completed/${TASK_ID}/${suffix}"
   done
   ```

4. **Discover and Move Coverage Files (if exists)**
   ```bash
   # Find coverage files matching task pattern
   find . -maxdepth 1 -name "coverage*${TASK_ID}*.json" -type f
   find . -maxdepth 1 -name "coverage-task${TASK_ID#TASK-}*.json" -type f

   # Move to task subfolder
   for file in $(find . -maxdepth 1 -name "*${TASK_ID}*.json"); do
     mv "$file" "tasks/completed/${TASK_ID}/"
   done
   ```

5. **Update Task File Metadata**
   ```yaml
   ---
   status: completed
   completed: 2024-01-20T16:30:00Z
   completed_location: tasks/completed/TASK-045/
   organized_files: [
     "TASK-045.md",
     "implementation-summary.md",
     "completion-report.md",
     "coverage-report.json"
   ]
   ---
   ```

**Benefits of Subfolder Organization:**
- **No Root Pollution**: Keeps project root clean and organized
- **Easy Discovery**: All task-related files in one place
- **Better Traceability**: Clear association between task and its artifacts
- **Scalable**: Structure works for projects with hundreds of tasks
- **Idempotent**: Safe if subfolder already exists

**Error Handling:**
- If subfolder already exists: Skip creation (idempotent)
- If related files not found: Log info message, continue with completion
- If move fails: Log warning, but don't block completion
- Preserve git history: Use `git mv` if files are tracked

### Completion Execution

**Example 1: taskwright only (Graceful Degradation)**
```bash
/task-complete TASK-045

🏁 Completing Task: TASK-045

ℹ️  Package Detection:
- taskwright: ✅ installed (v1.0.0)
- require-kit: ❌ not installed

📁 Organizing Task Files
Creating: tasks/completed/TASK-045/
Moving: tasks/in_progress/TASK-045.md → tasks/completed/TASK-045/
Found related files:
  ✅ TASK-045-IMPLEMENTATION-SUMMARY.md → implementation-summary.md
  ✅ TASK-045-COMPLETION-REPORT.md → completion-report.md
  ✅ coverage-task045.json → coverage-report.json
Organized 4 files into tasks/completed/TASK-045/

🔄 Task State Transition
Status: IN_PROGRESS → COMPLETED
Completion Date: 2024-01-20T16:30:00Z
Duration: 2.5 days (estimated: 2 days)
Location: tasks/completed/TASK-045/

📊 Quality Gates (Core)
✅ All tests passing (100%)
✅ Coverage: 87.5% (≥80%)
✅ Code review approved
✅ Documentation complete

ℹ️  Optional Features Skipped:
- Requirements validation (install require-kit for EARS verification)
- BDD scenario validation (install require-kit for BDD verification)
- Epic/Feature rollup (install require-kit for hierarchy tracking)
- PM tool sync (install require-kit for Jira/Linear/GitHub integration)

🎉 Task Completion Summary
✅ TASK-045 successfully completed
✅ All task files organized in tasks/completed/TASK-045/
✅ Core quality gates passed

💡 Tip: Install require-kit for full integration features
```

**Example 2: Both packages installed (Full Integration)**
```bash
/task-complete TASK-045

🏁 Completing Task: TASK-045

ℹ️  Package Detection:
- taskwright: ✅ installed (v1.0.0)
- require-kit: ✅ installed (v1.0.0)

📁 Organizing Task Files
Creating: tasks/completed/TASK-045/
Moving: tasks/in_progress/TASK-045.md → tasks/completed/TASK-045/
Found related files:
  ✅ TASK-045-IMPLEMENTATION-SUMMARY.md → implementation-summary.md
  ✅ TASK-045-COMPLETION-REPORT.md → completion-report.md
  ✅ coverage-task045.json → coverage-report.json
Organized 4 files into tasks/completed/TASK-045/

🔄 Task State Transition
Status: IN_PROGRESS → COMPLETED
Completion Date: 2024-01-20T16:30:00Z
Duration: 2.5 days (estimated: 2 days)
Location: tasks/completed/TASK-045/

📊 Quality Gates (Core)
✅ All tests passing (100%)
✅ Coverage: 87.5% (≥80%)
✅ Code review approved
✅ Documentation complete

📊 Requirements Validation (require-kit)
✅ Requirements satisfied: 3/3
  - REQ-005: Authentication logic ✅
  - REQ-006: Session management ✅
  - REQ-007: Error handling ✅

📊 BDD Scenario Validation (require-kit)
✅ BDD scenarios passed: 5/5
  - Successful login ✅
  - Invalid credentials ✅
  - Session timeout ✅
  - Token refresh ✅
  - Logout ✅

📊 Progress Rollup Calculation (require-kit)
Feature FEAT-003: 65% → 85% (+20%)
Epic EPIC-001: 57% → 63% (+6%)
Portfolio: 46% → 48% (+2%)

🔄 External Tool Updates (require-kit)
✅ Jira Sub-task PROJ-129: Status → "Done"
✅ Linear Issue PROJECT-461: Status → "Completed"
✅ GitHub Issue #253: Closed

🎉 Task Completion Summary
✅ TASK-045 successfully completed
✅ Feature FEAT-003 at 85% completion
✅ Epic EPIC-001 progressed to 63%
✅ All task files organized in tasks/completed/TASK-045/
✅ All downstream dependencies cleared
✅ Full integration features activated
```

## Quality Assurance Integration

### Completion Quality Gates
Quality gates must pass before completion:
- Code Coverage: ≥80% ✅
- Test Pass Rate: 100% ✅
- Security Scan: No critical issues ✅
- Code Review: Approved ✅

## Agentecflow Stage Integration

### Stage 3 → Stage 4 Transition Support
```bash
/task-complete TASK-045 --stage-transition

🔄 Stage 3 → Stage 4 Transition: TASK-045
Implementation: 100% complete ✅
Quality Gates: 4/4 passed ✅
Ready for deployment: ✅
```

This command ensures high-quality task completion while maintaining accurate progress tracking across the **Epic → Feature → Task hierarchy**.

## Git State Commit (REQUIRED for Conductor Support)

**CRITICAL**: After completing the task and moving files to the completed directory, commit all task-related state files to git. This ensures that state is preserved across git worktrees (used by Conductor.build for parallel development).

### Implementation

After completing all file organization and state updates, execute the following Python code:

```python
from installer.global.commands.lib.git_state_helper import commit_state_files

# Commit all state files for this completed task
# This includes:
# - docs/state/{task_id}/ directory (all state files)
# - Task completion metadata
# - Progress rollup updates

try:
    commit_state_files(
        task_id="{task_id}",
        message=f"Complete {task_id} and update state"
    )
    print("✅ Task state committed to git")
except Exception as e:
    # Don't fail completion if git commit fails
    # (may not be in a git repo, or git may not be available)
    print(f"⚠️  Warning: Could not commit task state: {e}")
    print("   (This is non-critical - task completion can continue)")
```

### Why This Is Needed

- **Conductor.build** uses git worktrees for parallel development
- Each worktree has its own working directory but shares the same git repository
- State files in `docs/state/` MUST be committed to be visible across all worktrees
- Without this step, completed task state is lost when switching between worktrees

### What Gets Committed

- All files in `docs/state/{task_id}/` directory
- Progress rollup updates (if stored in state files)
- Completion metadata and timestamps
- Does NOT commit the task file itself (that's in `tasks/completed/` and handled separately)
- Does NOT push to remote (that's a separate operation)

### Error Handling

- If git commit fails, log a warning but continue with task completion
- Common reasons for failure:
  - Not in a git repository
  - Git not available in environment
  - No state files to commit (silent success)
- Task completion should never fail due to git commit issues