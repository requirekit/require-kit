# Task Refine - Iterative Code Refinement Command

## Overview

The `/task-refine` command enables lightweight, iterative refinement of tasks that have completed implementation but require adjustments based on code review feedback or human inspection.

**Purpose**: Apply targeted fixes without re-running the full task-work workflow.

**Alignment**: Implements John Hubbard's workflow Step 5 ("Re-execute as necessary until tests pass") and Martin Fowler's research emphasis on "small, iterative steps."

## Command Syntax

```bash
/task-refine TASK-XXX "refinement description" [--interactive]
```

### Arguments

**TASK-XXX** (required)
- Task identifier (e.g., `TASK-026`, `TASK-042`)
- Task MUST be in `IN_REVIEW` or `BLOCKED` state

**"refinement description"** (required)
- Human-readable description of what to fix or improve
- Specific and actionable (not vague like "make it better")
- Examples:
  - `"Add input validation to login endpoint"`
  - `"Extract token logic into separate class"`
  - `"Fix memory leak in session manager"`
  - `"Improve error messages in auth flow"`

**--interactive** (optional)
- Opens chat-like interface for back-and-forth refinement
- Allows multiple refinement requests in single session
- Runs quality gates after human confirms changes

## State Requirements

### Valid States

The task MUST be in one of these states:
- **IN_REVIEW**: Task completed, passed quality gates, ready for review
- **BLOCKED**: Task failed quality gates (tests or code review)

### Prerequisites

The task MUST have:
- ✅ Implementation plan (from Phase 2.7 of `/task-work`)
- ✅ Created code files (from Phase 3)
- ✅ Test results (from Phase 4)
- ✅ Code review results (from Phase 5, if in IN_REVIEW)

### Invalid States

These states will **reject** refinement:
- **BACKLOG**: Task not started (use `/task-work` instead)
- **IN_PROGRESS**: Task currently being worked on (complete it first)
- **DESIGN_APPROVED**: Task designed but not implemented (use `/task-work --implement-only` instead)
- **COMPLETED**: Task finished and archived (create new task instead)

## Workflow

```
┌─────────────────────────────────────────┐
│ 1. Validate State                       │
│    - Check task is IN_REVIEW or BLOCKED │
│    - Verify plan exists                 │
│    - Verify code files exist            │
└──────────────┬──────────────────────────┘
               ▼
┌─────────────────────────────────────────┐
│ 2. Load Context                         │
│    - Implementation plan (Phase 2.7)    │
│    - Code review comments (Phase 5)     │
│    - Test results (Phase 4)             │
│    - Existing code files                │
└──────────────┬──────────────────────────┘
               ▼
┌─────────────────────────────────────────┐
│ 3. Apply Refinement                     │
│    - Build context-rich prompt          │
│    - Invoke task-manager agent          │
│    - Extract modified files             │
└──────────────┬──────────────────────────┘
               ▼
┌─────────────────────────────────────────┐
│ 4. Re-run Quality Gates                 │
│    - Phase 4: Testing                   │
│    - Phase 4.5: Fix loop (if tests fail)│
│    - Phase 5: Code review               │
└──────────────┬──────────────────────────┘
               ▼
┌─────────────────────────────────────────┐
│ 5. Calculate New State                  │
│    - All gates pass → IN_REVIEW         │
│    - Any gate fails → BLOCKED           │
└──────────────┬──────────────────────────┘
               ▼
┌─────────────────────────────────────────┐
│ 6. Track Refinement Session             │
│    - Append to task changelog           │
│    - Update task metadata               │
│    - Save refinement timestamp          │
└─────────────────────────────────────────┘
```

## Refinement Scope Constraints

To prevent scope creep, refinements are constrained by:

### What Refinements CAN Do ✅

1. **Fix Bugs**: Correct implementation errors identified in review
2. **Improve Code Quality**: Refactor for better readability, maintainability
3. **Add Missing Elements**: Add validation, error handling, edge cases **within original scope**
4. **Adjust Implementation Details**: Change how something is implemented (not what)

### What Refinements CANNOT Do ❌

1. **Add New Features**: No new requirements beyond original task scope
2. **Change Architecture**: No fundamental architectural changes (create new task)
3. **Add New Dependencies**: No new external libraries (unless fixing a bug)
4. **Expand Scope**: No new files, classes, or modules (unless essential to fix)

### Enforcement

The refinement prompt includes explicit constraints:

```
CONSTRAINTS:
- Apply ONLY the requested refinement
- Do NOT change unrelated code
- Preserve existing patterns and style
- Update tests if necessary
- Do NOT add scope creep
- Modify existing files only (no new files unless requested)
- Follow original architectural decisions
- Maintain test coverage
```

## Examples

### Example 1: Add Input Validation

```bash
/task-refine TASK-042 "Add input validation to login endpoint"

# Output:
🔄 Refining TASK-042: Implement user authentication API

📋 Loading context:
   ✅ Implementation plan loaded
   ✅ Code review comments loaded (2 issues)
   ✅ Test results loaded (12/12 passed)
   ✅ Files: src/auth/login.py, tests/test_login.py

🤖 Applying refinement: "Add input validation to login endpoint"
   - Added email format validation
   - Added password length validation (min 8 chars)
   - Updated tests for validation scenarios

🧪 Re-running quality gates:
   Phase 4 (Testing): ✅ 15/15 passed (+3 new tests)
   Phase 4.5 (Fix Loop): ⏭️  Skipped (tests passed)
   Phase 5 (Code Review): ✅ No issues

📊 Result:
   Status: SUCCESS
   New State: IN_REVIEW
   Files Modified: 2 (src/auth/login.py, tests/test_login.py)
   Refinement Session: TASK-042-refine-001

✅ Task TASK-042 → IN_REVIEW (ready for completion)
```

### Example 2: Fix Failing Tests

```bash
/task-refine TASK-055 "Fix race condition in async handler"

# Output:
🔄 Refining TASK-055: Implement async event processing

📋 Loading context:
   ✅ Implementation plan loaded
   ✅ Code review comments loaded (blocked on tests)
   ✅ Test results loaded (8/10 passed, 2 failed)
   ✅ Files: src/events/handler.py, tests/test_handler.py

🤖 Applying refinement: "Fix race condition in async handler"
   - Added asyncio.Lock to prevent concurrent access
   - Fixed await ordering in event processing
   - Added lock release in finally block

🧪 Re-running quality gates:
   Phase 4 (Testing): ❌ 9/10 passed (1 timeout)
   Phase 4.5 (Fix Loop): 🔄 Fixing test failures...
      Attempt 1: Added timeout handling
      Phase 4 (Re-test): ✅ 10/10 passed
   Phase 5 (Code Review): ✅ No issues

📊 Result:
   Status: SUCCESS
   New State: IN_REVIEW
   Files Modified: 2 (src/events/handler.py, tests/test_handler.py)
   Refinement Session: TASK-055-refine-002

✅ Task TASK-055 → IN_REVIEW (ready for completion)
```

### Example 3: Extract to Separate Class

```bash
/task-refine TASK-063 "Extract token logic into separate TokenManager class"

# Output:
🔄 Refining TASK-063: Implement session management

📋 Loading context:
   ✅ Implementation plan loaded
   ✅ Code review comments loaded (complexity warning)
   ✅ Test results loaded (18/18 passed)
   ✅ Files: src/session/manager.py, tests/test_session.py

🤖 Applying refinement: "Extract token logic into separate TokenManager class"
   - Created TokenManager class
   - Moved token generation, validation, expiry logic
   - Updated SessionManager to use TokenManager
   - Refactored tests for new structure

🧪 Re-running quality gates:
   Phase 4 (Testing): ✅ 20/20 passed (+2 tests for TokenManager)
   Phase 4.5 (Fix Loop): ⏭️  Skipped (tests passed)
   Phase 5 (Code Review): ✅ Complexity improved (cyclomatic: 12 → 8)

📊 Result:
   Status: SUCCESS
   New State: IN_REVIEW
   Files Modified: 2 (src/session/manager.py, tests/test_session.py)
   Files Created: 1 (src/session/token_manager.py)
   Refinement Session: TASK-063-refine-001

✅ Task TASK-063 → IN_REVIEW (ready for completion)
```

### Example 4: Interactive Mode

```bash
/task-refine TASK-070 --interactive

# Output:
🔄 Starting interactive refinement for TASK-070

📋 Task: Implement rate limiting middleware
   Status: BLOCKED (code review identified issues)

💬 Refinement Chat (type 'done' to finish, 'cancel' to abort)

You: Add retry logic with exponential backoff

AI: I've added retry logic to the rate limiter:
   - Exponential backoff: 1s, 2s, 4s, 8s, 16s (max)
   - Configurable max retries (default: 5)
   - Added RetryConfig dataclass

   Modified files: src/middleware/rate_limiter.py

   Continue refining? (yes/no/run tests)

You: run tests

AI: Running quality gates...
   Phase 4 (Testing): ✅ 22/22 passed (+4 retry tests)
   Phase 5 (Code Review): ⚠️  1 issue: Consider adding jitter to backoff

   Continue refining? (yes/no/done)

You: Add jitter to backoff

AI: Added random jitter to exponential backoff:
   - Jitter: ±10% of backoff delay
   - Prevents thundering herd problem

   Modified files: src/middleware/rate_limiter.py

   Run tests again? (yes/no/done)

You: yes

AI: Running quality gates...
   Phase 4 (Testing): ✅ 23/23 passed (+1 jitter test)
   Phase 5 (Code Review): ✅ No issues

   Refinement complete? (yes/cancel)

You: yes

📊 Result:
   Status: SUCCESS
   New State: IN_REVIEW
   Total Refinements: 2 (retry logic, jitter)
   Files Modified: 1 (src/middleware/rate_limiter.py)
   Refinement Session: TASK-070-refine-003

✅ Task TASK-070 → IN_REVIEW (ready for completion)
```

## Integration with Task Workflow

### After `/task-work`

```bash
# Complete workflow
/task-work TASK-042 --mode=tdd
# Task reaches IN_REVIEW state

# Code review identifies issues
/task-status TASK-042
# Shows: IN_REVIEW, 2 code review issues

# Apply refinement
/task-refine TASK-042 "Add input validation per review comments"
# Task remains in IN_REVIEW, issues resolved

# Complete task
/task-complete TASK-042
```

### Iterative Refinement

```bash
# First refinement
/task-refine TASK-042 "Add validation"
# Result: IN_REVIEW

# Second refinement (if needed)
/task-refine TASK-042 "Improve error messages"
# Result: IN_REVIEW

# Third refinement (if needed)
/task-refine TASK-042 "Extract validation logic to utility"
# Result: IN_REVIEW

# Complete when satisfied
/task-complete TASK-042
```

### Fixing Blocked Tasks

```bash
# Task blocked on failing tests
/task-status TASK-055
# Shows: BLOCKED, 2/10 tests failing

# Refine to fix tests
/task-refine TASK-055 "Fix async race conditions causing test failures"
# Phase 4.5 (fix loop) runs automatically
# Result: IN_REVIEW (if tests pass) or BLOCKED (if still failing)
```

## Task Metadata Tracking

Each refinement session is tracked in the task file frontmatter:

```yaml
---
id: TASK-042
status: in_review
refinements:
  - session_id: TASK-042-refine-001
    description: "Add input validation to login endpoint"
    requested_at: "2025-10-18T11:30:00Z"
    outcome: success
    files_modified: ["src/auth/login.py", "tests/test_login.py"]
    tests_passed: true
    review_passed: true
  - session_id: TASK-042-refine-002
    description: "Improve error messages in validation"
    requested_at: "2025-10-18T14:15:00Z"
    outcome: success
    files_modified: ["src/auth/login.py"]
    tests_passed: true
    review_passed: true
refinement_count: 2
last_refinement: "2025-10-18T14:15:00Z"
---
```

### Refinement Log

In addition to frontmatter, a refinement log is appended to the task file body:

```markdown
## Refinement History

### Refinement 1 - 2025-10-18T11:30:00Z
**Description**: Add input validation to login endpoint
**Outcome**: SUCCESS → IN_REVIEW
**Tests Passed**: 15/15
**Review Issues**: 0
**Files Modified**:
- src/auth/login.py
- tests/test_login.py

### Refinement 2 - 2025-10-18T14:15:00Z
**Description**: Improve error messages in validation
**Outcome**: SUCCESS → IN_REVIEW
**Tests Passed**: 15/15
**Review Issues**: 0
**Files Modified**:
- src/auth/login.py
```

## Error Handling

### Task Not Found

```bash
/task-refine TASK-999 "Fix something"

# Output:
❌ Error: Task TASK-999 not found
   Searched in: tasks/backlog, tasks/in_progress, tasks/in_review, tasks/blocked

   Hint: Use /task-status to list available tasks
```

### Invalid State

```bash
/task-refine TASK-042 "Add feature"
# Task is in BACKLOG state

# Output:
❌ Error: Cannot refine task in BACKLOG state
   Current State: BACKLOG
   Valid States: IN_REVIEW, BLOCKED

   Use /task-work TASK-042 to implement the task first.
```

### Missing Prerequisites

```bash
/task-refine TASK-042 "Fix something"
# Task has no implementation plan

# Output:
❌ Error: Task TASK-042 has no implementation plan

   This task has not been implemented yet.
   Run /task-work TASK-042 to implement before refining.
```

### Agent Failure

```bash
/task-refine TASK-042 "Add complex feature requiring architectural changes"

# Output:
⚠️  Warning: Refinement agent failed to apply changes
   Error: Requested change exceeds refinement scope

   The requested change appears to require architectural modifications
   that go beyond refinement scope.

   Recommendations:
   1. Create a new task for the architectural change
   2. Simplify the refinement request to be more targeted
   3. Consider using /task-work with a new task for major changes

   Task state unchanged: IN_REVIEW
```

## Success Metrics

Track these metrics to evaluate effectiveness:

### Usage Metrics
- **Refinement Rate**: % of tasks that use refinement (target: 50%)
- **Iterations per Task**: Average refinement cycles per task (target: 1-2)
- **Refinement Success Rate**: % of refinements that resolve issues (target: 90%)

### Time Savings
- **Time per Refinement**: Average duration (target: 10-15 min)
- **Savings vs Re-run**: Time saved vs re-running full `/task-work` (target: 60-80%)
- **Savings vs Manual Edit**: Time saved vs manual editing (target: 40-60%)

### Quality Impact
- **Review Issues Resolved**: % of code review issues fixed via refinement (target: 80%)
- **Test Failure Recovery**: % of blocked tasks unblocked via refinement (target: 70%)
- **Scope Creep Incidents**: Refinements that added unintended scope (target: <5%)

## Related Commands

- **`/task-work`**: Initial task implementation (prerequisite)
- **`/task-status`**: Check task state and eligibility for refinement
- **`/task-complete`**: Finalize task after successful refinement
- **`/task-sync`**: Sync refined task to external PM tools

## Implementation Details

### Core Module
- **File**: `installer/global/commands/lib/refinement_handler.py`
- **Entry Point**: `RefinementHandler.refine(request: RefinementRequest) -> RefinementResult`

### Agent Invocation
- **Agent**: `task-manager` (same as `/task-work` Phase 3)
- **Prompt Template**: Includes original plan, review comments, refinement request, and constraints

### Quality Gates
- Reuses existing phase execution functions:
  - `execute_phase_4()` - Testing
  - `execute_phase_4_5()` - Fix loop
  - `execute_phase_5()` - Code review

### State Transitions
- **IN_REVIEW → IN_REVIEW**: Refinement successful, all gates pass
- **IN_REVIEW → BLOCKED**: Refinement introduced test failures
- **BLOCKED → IN_REVIEW**: Refinement fixed tests, passed code review
- **BLOCKED → BLOCKED**: Refinement didn't resolve issues

## References

- **John Hubbard's Workflow**: Step 5 - "Re-execute as necessary until tests pass"
- **Martin Fowler SDD Research**: "Small, iterative steps" for maintainability
- **Implementation Plan**: `docs/research/implementation-plan-and-code-review-analysis.md`
- **Related Task**: TASK-026 - Create task-refine command

## Version History

- **v1.0** (2025-10-18): Initial implementation
  - Core refinement workflow
  - State validation
  - Quality gate re-execution
  - Session tracking
