# Iterative Refinement Workflow

## Overview

The `/task-refine` command enables lightweight, iterative improvements to completed tasks without triggering the full `/task-work` workflow. Use this for minor code quality improvements, clarifications, and polish after a task passes quality gates.

**Key Benefits:**
- **Context Preservation**: Retains original implementation plan, review comments, audit history
- **Lightweight Process**: Skips planning and architectural review phases
- **Multiple Iterations**: Apply refinements in small, focused cycles
- **Safe Modifications**: Maintains all quality gates (tests must still pass)

**Not a Replacement For:** Major refactoring, new features, architectural changes, or bug fixes requiring significant rework. Use `/task-work` for those.

## Prerequisites

**Task State Requirements:**
- Task must be in `in_review` or `completed` state
- All tests must currently be passing (100% pass rate)
- Implementation must be complete (not in `in_progress` or `blocked`)

**What You'll Need:**
- Clear refinement goal (specific, focused change)
- Understanding of existing implementation
- Confidence that change won't break tests

## When to Refine vs Re-work

### ✅ Use `/task-refine` When:

**Code Quality Improvements:**
- Variable/function renaming for clarity
- Adding inline comments or docstrings
- Extracting helper functions (no logic change)
- Improving formatting or style
- Adding type hints or annotations

**Small Additions:**
- Adding logging statements
- Adding defensive checks (validation, null checks)
- Improving error messages
- Adding debug information

**Minor Adjustments:**
- Adjusting default values
- Changing log levels
- Tweaking timeouts or thresholds
- Fixing typos in strings or comments

### ❌ Use `/task-work` (Full Re-work) When:

**New Features:**
- Adding functionality not in original scope
- Implementing new requirements
- Extending API surface area
- New file creation required

**Architectural Changes:**
- Changing design patterns
- Refactoring class structure
- Modifying data flow
- Changing dependencies

**Major Refactoring:**
- Moving code between modules
- Splitting or merging classes
- Changing interfaces or contracts
- Deleting significant code

**Bug Fixes:**
- Fixing logic errors
- Correcting algorithm flaws
- Resolving race conditions
- Addressing security vulnerabilities

### Decision Tree

```
Need to modify completed task?
│
├─ Changes affect behavior? ──────────────────────────→ YES → Use /task-work
│
├─ Changes add new features? ─────────────────────────→ YES → Use /task-work
│
├─ Changes require new files? ────────────────────────→ YES → Use /task-work
│
├─ Changes may break tests? ──────────────────────────→ YES → Use /task-work
│
├─ Changes are architectural? ────────────────────────→ YES → Use /task-work
│
└─ Small quality improvements only? ──────────────────→ YES → Use /task-refine
   (naming, comments, formatting, logging)
```

## Context Preservation Benefits

### What Gets Preserved

**1. Implementation Plan**
- Original plan remains intact
- Refinement notes added as appendix
- Plan version history maintained

**2. Architectural Review Results**
- Original scores preserved (SOLID, DRY, YAGNI)
- Refinement doesn't trigger re-review
- Historical review comments retained

**3. Plan Audit History**
- Original variance analysis preserved
- Refinement tracked as separate change
- Cumulative refinement log maintained

**4. Test Results**
- Original test results archived
- New test results added to history
- Coverage changes tracked

### Why This Matters

**Traceability:**
- Can trace decision history (why was it built this way?)
- Audit trail for compliance (what changed when?)
- Learning resource (how did design evolve?)

**Efficiency:**
- No need to re-generate implementation plan
- No architectural review overhead
- Fast iteration (2-5 minutes vs 15-20 minutes)

**Safety:**
- Original context prevents over-refinement
- Helps decide when to stop refining
- Catches scope creep in refinements

## Command Usage

### Basic Syntax

```bash
/task-refine TASK-XXX "refinement description"
```

**Parameters:**
- `TASK-XXX`: Task ID (must be in `in_review` or `completed` state)
- `"refinement description"`: Brief description of change (1-2 sentences)

**Flags:**
- `--with-context`: Include epic/feature context (verbose mode)
- `--dry-run`: Preview changes without applying (coming soon)

### Examples

**Example 1: Add Logging**
```bash
/task-refine TASK-042 "Add debug logging to authentication flow"

# System executes:
# 1. Load task from in_review/TASK-042.md
# 2. Load implementation plan and review context
# 3. Apply refinement: Add logger.debug() calls
# 4. Re-run tests (must pass)
# 5. Update task with refinement log
# 6. Keep task in in_review state
```

**Example 2: Improve Variable Names**
```bash
/task-refine TASK-043 "Rename variables for clarity: usr → current_user, pwd → password_hash"

# System executes:
# 1. Load task context
# 2. Refactor variable names across all files
# 3. Ensure tests still pass
# 4. Log refinement in task metadata
```

**Example 3: Add Type Hints (Python)**
```bash
/task-refine TASK-044 "Add type hints to public functions for better IDE support"

# System executes:
# 1. Analyze function signatures
# 2. Add type annotations (def login(user: User) -> AuthResult)
# 3. Run mypy type checker
# 4. Run tests (ensure type changes don't break)
```

**Example 4: Extract Helper Function**
```bash
/task-refine TASK-045 "Extract validation logic into _validate_input() helper"

# System executes:
# 1. Identify validation code blocks
# 2. Extract into private helper function
# 3. Update callers to use helper
# 4. Run tests (ensure behavior unchanged)
```

### With Context (Verbose Mode)

```bash
/task-refine TASK-042 "Add logging" --with-context

# Additional context loaded:
# - Epic: EPIC-001 (User Management)
# - Feature: FEAT-003 (Authentication)
# - Related requirements: REQ-001, REQ-002
# - Related tasks: TASK-040, TASK-041, TASK-043

# Benefit: Better understanding of broader context
# Use when: Refinement may affect related tasks
```

## Multiple Refinement Cycles

### Refinement Versioning

Each refinement cycle creates a versioned log entry:

```yaml
# Task metadata after 3 refinements
refinements:
  - version: 1
    date: "2025-10-20T14:30:00Z"
    description: "Add debug logging to authentication flow"
    files_modified: ["src/auth/auth_service.py"]
    test_status: "passed"
    duration: "2 minutes"

  - version: 2
    date: "2025-10-20T15:45:00Z"
    description: "Rename usr → current_user for clarity"
    files_modified: ["src/auth/auth_service.py", "tests/test_auth.py"]
    test_status: "passed"
    duration: "3 minutes"

  - version: 3
    date: "2025-10-21T09:15:00Z"
    description: "Extract validation into _validate_credentials helper"
    files_modified: ["src/auth/auth_service.py"]
    test_status: "passed"
    duration: "4 minutes"
```

### History Tracking

**View Refinement History:**
```bash
/task-status TASK-042 --refinements

# Output:
# TASK-042: Implement user authentication
# Status: in_review
# Refinements: 3 total
#
# 1. 2025-10-20 14:30 - Add debug logging
#    Files: src/auth/auth_service.py
#    Status: ✅ Passed tests
#
# 2. 2025-10-20 15:45 - Rename usr → current_user
#    Files: src/auth/auth_service.py, tests/test_auth.py
#    Status: ✅ Passed tests
#
# 3. 2025-10-21 09:15 - Extract validation helper
#    Files: src/auth/auth_service.py
#    Status: ✅ Passed tests
```

**Git History Integration:**
```bash
# Each refinement creates a commit
git log --oneline TASK-042

# Output:
# abc1234 [TASK-042] Refinement v3: Extract validation helper
# def5678 [TASK-042] Refinement v2: Rename usr → current_user
# ghi9012 [TASK-042] Refinement v1: Add debug logging
# jkl3456 [TASK-042] Initial implementation
```

### When to Stop Refining

**Stop Criteria:**

**✅ Good Stopping Points:**
- Code is readable and maintainable
- All obvious improvements applied
- No more "quick wins" visible
- Team consensus on "good enough"
- Time investment reaches diminishing returns

**⚠️ Warning Signs (Approaching Over-Refinement):**
- 5+ refinement cycles on single task
- Refinements take longer than original implementation
- Tests start failing frequently
- Changes become more than "minor adjustments"
- Questioning original design decisions

**❌ Stop Immediately If:**
- Considering architectural changes
- Wanting to add new features
- Original implementation seems flawed
- Tests break and hard to fix
- Scope expanding beyond original task

**Alternative Actions:**
- Create new task for architectural improvements
- Schedule team discussion for design review
- Document technical debt item for later
- Accept current state as "good enough for now"

## Troubleshooting

### Common Issues

#### Issue: Refinement Breaks Tests

**Symptoms:**
- Tests passed before refinement
- Tests failing after refinement
- Error messages unclear

**Diagnosis:**
```bash
# Compare test output before/after
diff docs/state/{task_id}/test_results_original.json \
     docs/state/{task_id}/test_results_refinement_v1.json

# Review changes made
git diff HEAD~1 HEAD

# Run specific failing test
pytest tests/test_auth.py::test_login_valid_credentials -vv
```

**Solutions:**
1. **Revert Refinement**: `git revert HEAD` and try smaller change
2. **Fix Tests**: If test was too brittle, update test
3. **Fix Implementation**: Correct the refinement logic
4. **Escalate to Re-work**: Use `/task-work` if change too complex

#### Issue: Refinement Changes Behavior

**Symptoms:**
- Tests pass but behavior different
- Unexpected side effects
- Integration tests failing

**Diagnosis:**
```bash
# Run full test suite (not just unit tests)
pytest tests/ -v --integration

# Check for side effects
git diff HEAD~1 HEAD --stat

# Review original acceptance criteria
cat tasks/in_review/TASK-042.md | grep -A 10 "Acceptance Criteria"
```

**Solutions:**
1. **Revert if Unintended**: Undo refinement, behavior must not change
2. **Update Documentation**: If behavior change intentional, document
3. **Create New Task**: If behavior change significant, track separately

#### Issue: Refinement Taking Too Long

**Symptoms:**
- Refinement exceeds 10 minutes
- Multiple attempts required
- Complexity increasing

**Diagnosis:**
- Is this really a "refinement" or a "re-work"?
- Are you changing design, not just polish?
- Should this be a new task?

**Solutions:**
1. **Switch to `/task-work`**: Abandon refinement, use full workflow
2. **Break Down Change**: Apply refinement in smaller steps
3. **Accept Current State**: Maybe "good enough" already achieved

#### Issue: Task Not in Eligible State

**Error Message:**
```
❌ Error: Cannot refine TASK-042

Task is in 'in_progress' state.
Required states: in_review, completed

Tasks in progress should use /task-work to complete implementation.
```

**Solutions:**
1. Complete task first: `/task-work TASK-042`
2. Wait for quality gates to pass
3. Once in `in_review`, retry refinement

## Real-World Examples

### Example 1: Adding Logging to Reviewed Task

**Scenario:** Task completed and in review. Code reviewer requests more logging.

**Initial Task State:**
- State: `in_review`
- Tests: 15/15 passing
- Coverage: 87%
- Review comment: "Add logging at key decision points"

**Refinement Process:**
```bash
# Step 1: Apply refinement
/task-refine TASK-042 "Add INFO logging at authentication decision points"

# System output:
Refinement v1: Adding logging to TASK-042
Analyzing code for decision points...
Adding logger.info() calls:
  - src/auth/auth_service.py:45 (login attempt)
  - src/auth/auth_service.py:67 (authentication success)
  - src/auth/auth_service.py:72 (authentication failure)

Re-running tests...
✅ All tests passing (15/15)
Coverage: 87% (unchanged)

Refinement complete: 2 minutes 15 seconds
```

**Result:**
- Files modified: 1 (src/auth/auth_service.py)
- Lines added: 3 (logger.info calls)
- Tests: Still passing
- Task remains in `in_review` (ready for re-review)

### Example 2: Fixing Edge Case After Completion

**Scenario:** Task completed 2 weeks ago. Edge case discovered in production.

**Initial Task State:**
- State: `completed` (archived)
- Tests: 20/20 passing
- Coverage: 92%
- Issue: Empty string input causes crash (not covered by tests)

**Refinement Process:**
```bash
# Step 1: Move task back to in_review
/task-reopen TASK-043

# Step 2: Apply refinement
/task-refine TASK-043 "Add validation for empty string input"

# System output:
Refinement v1: Adding validation to TASK-043
Analyzing edge case...
Adding validation check:
  - src/utils/validator.py:23 (empty string check)

Generating test:
  - tests/test_validator.py:45 (test_validate_empty_string)

Re-running tests...
✅ All tests passing (21/21, +1 new test)
Coverage: 94% (+2%)

Refinement complete: 4 minutes 30 seconds
```

**Result:**
- Files modified: 2
- Tests added: 1
- Coverage improved: 92% → 94%
- Task back in `in_review` (ready for re-deployment)

### Example 3: Multiple Refinement Cycle Scenario

**Scenario:** Iterative code review feedback over 3 cycles.

**Cycle 1: Add Type Hints**
```bash
/task-refine TASK-044 "Add type hints to all public methods"

# Result:
# - 15 functions annotated
# - mypy checks passing
# - Duration: 5 minutes
```

**Cycle 2: Improve Docstrings**
```bash
/task-refine TASK-044 "Add docstrings with parameter descriptions"

# Result:
# - 15 docstrings added (Google style)
# - Sphinx docs generated
# - Duration: 6 minutes
```

**Cycle 3: Extract Magic Numbers**
```bash
/task-refine TASK-044 "Extract magic numbers into named constants"

# Result:
# - 8 constants extracted (MAX_RETRIES, TIMEOUT_SECONDS, etc.)
# - Code more readable
# - Duration: 3 minutes
```

**Total Refinement Investment:**
- 3 cycles
- 14 minutes total
- Original implementation: 45 minutes
- Refinement overhead: 31% (acceptable)

**When to Stop:**
- Code now highly readable
- Type safe and well-documented
- No more obvious improvements
- Team consensus: "looks great!"

## Related Workflows

- **[Agentecflow Lite Workflow](../guides/agentecflow-lite-workflow.md)** - Complete workflow overview
- **[Quality Gates Workflow](./quality-gates-workflow.md)** - Testing and quality enforcement
- **[Design-First Workflow](./design-first-workflow.md)** - Design approval process
- **[Markdown Plans Workflow](./markdown-plans-workflow.md)** - Implementation plan format

## FAQ

**Q: Can I refine a task multiple times?**
A: Yes! Refinements are versioned and tracked. However, if you exceed 5 refinements, consider whether re-work is more appropriate.

**Q: Does refinement trigger architectural review?**
A: No. Refinements are lightweight and skip Phase 2.5 (architectural review). Original review results are preserved.

**Q: What if refinement breaks tests?**
A: System enters fix loop (1 attempt). If tests still fail, refinement is rejected and task state unchanged. Consider using `/task-work` for more complex changes.

**Q: Can I refine tasks in `blocked` state?**
A: No. Tasks must be in `in_review` or `completed` state. Blocked tasks should use `/task-work` to unblock.

**Q: Does refinement reset plan audit?**
A: No. Original plan audit preserved. Refinements tracked separately to show post-completion changes.

**Q: Can refinement add new files?**
A: No. Refinements only modify existing files. New files require `/task-work` (full workflow).

**Q: How do I undo a refinement?**
A: Use `git revert` to undo the refinement commit. Refinement history preserved in task metadata.

**Q: Can I refine multiple tasks at once?**
A: No. Refinements are task-specific. Use individual `/task-refine` commands for each task.

**Q: Does refinement count toward velocity?**
A: No. Refinements are maintenance, not new work. Original task completion counts toward velocity.

**Q: When should I create a new task instead of refining?**
A: If the change: (1) adds new features, (2) requires new files, (3) changes architecture, or (4) takes >15 minutes. These should be new tasks.
