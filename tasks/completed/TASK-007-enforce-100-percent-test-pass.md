---
id: TASK-007
title: "Fix task-work to enforce 100% test pass requirement"
status: completed
priority: critical
tags:
  - quality-gates
  - testing
  - task-work
  - zero-tolerance
  - ci-cd
created: '2025-10-10T00:00:00Z'
updated: '2025-10-11T00:00:00Z'
completed: '2025-10-11T00:00:00Z'
previous_state: in_review
state_transition_reason: "All acceptance criteria met and quality gates passed"
quality_gates:
  compilation: pass
  tests_passing: pass (26/26 tests, 100%)
  line_coverage: pass (100%)
  branch_coverage: pass (100%)
  code_review: approved
completion_summary:
  acceptance_criteria: 7/7 (100%)
  files_modified: 3
  lines_added: 474
  test_suite_created: true
  tests_passed: 26/26 (100%)
  architectural_review_score: 88/100
  complexity_score: 2/10 (low)
---

# Fix task-work to enforce 100% test pass requirement

## Problem Statement

The task-work command is currently allowing tasks to complete with failing tests (e.g., reporting "98.8% passing" as success). This is unacceptable for CI/CD pipelines which require 100% test pass rates.

## Root Causes Identified

1. Phase 4.5 (Fix Loop) exists in specification but isn't being enforced strictly by agents
2. Quality gates allow completion despite failing tests
3. Test-orchestrator doesn't verify compilation before running tests
4. Language in specifications isn't emphatic enough about zero-tolerance requirements
5. Agents interpret "test infrastructure issues" as acceptable excuses

## Required Fixes

### Fix #1: Update task-work.md Phase 4.5 (lines 738-850)

**Location**: `installer/global/commands/task-work.md`

**Changes**:
- Add explicit "ABSOLUTE REQUIREMENT" header
- Emphasize ZERO compilation errors allowed
- Emphasize ALL tests must pass (100%)
- Add "NO EXCEPTIONS" clause
- Make clear: ANY failing test = BLOCKED state

### Fix #2: Update task-work.md Step 6 (lines 884-905)

**Location**: `installer/global/commands/task-work.md`

**Changes**:
- Replace with explicit blocking logic in Python pseudocode
- Add zero-tolerance evaluation for:
  - Compilation errors (must be 0)
  - Test failures (must be 0)
  - Coverage thresholds (≥80% line, ≥75% branch)
- Add explicit state transition rules
- Add "NEVER complete with ANY failing tests" clause

### Fix #3: Update test-orchestrator.md - Add BUILD BEFORE TEST rule

**Location**: `installer/global/agents/test-orchestrator.md`

**Changes**:
- Add at line 17 (after Core Responsibilities)
- Mandate compilation check BEFORE test execution
- Include stack-specific compilation commands:
  - .NET: `dotnet build --no-incremental`
  - TypeScript: `npm run build`
  - Python: `python -m py_compile`
- Return error if compilation fails (block test execution)

### Fix #4: Update test-orchestrator.md Quality Gates (lines 72-133)

**Location**: `installer/global/agents/test-orchestrator.md`

**Changes**:
- Replace with zero-tolerance gate definitions
- Add explicit enforcement logic in Python
- Make gates blocking (not just warnings)
- Add "no_exceptions: true" flag to test_pass_rate gate
- Include clear messaging: "Test infrastructure issues is NOT an excuse"

### Fix #5: Add .NET MAUI-specific testing commands

**Location**: `installer/global/templates/maui/agents/test-orchestrator.md`

**Changes**:
- Add MAUI-specific test execution section at line 135
- Include 4-step process:
  1. Compilation verification (mandatory)
  2. Test execution with detailed logging
  3. Result evaluation
  4. Coverage verification
- Include bash script with proper error handling and exit codes

## Files to Modify

1. `installer/global/commands/task-work.md` (Phase 4.5 and Step 6)
2. `installer/global/agents/test-orchestrator.md` (BUILD BEFORE TEST rule and quality gates)
3. `installer/global/templates/maui/agents/test-orchestrator.md` (MAUI-specific commands)

## Acceptance Criteria

- [ ] Phase 4.5 includes "ABSOLUTE REQUIREMENT" language
- [ ] Step 6 has explicit blocking logic that prevents IN_REVIEW with any failures
- [ ] Test-orchestrator mandates compilation check before tests
- [ ] Quality gates enforce 100% test pass requirement with no exceptions
- [ ] MAUI-specific testing commands include compilation verification
- [ ] All documentation clearly states: ANY failing test = BLOCKED
- [ ] No ambiguous language like "test infrastructure issues" as valid excuses

## Expected Outcome

After these fixes, the task-work command will NEVER report success or transition to IN_REVIEW state unless:

1. Code compiles with ZERO errors
2. ALL tests pass (100%)
3. Coverage meets thresholds (≥80% line, ≥75% branch)

Any deviation from these requirements will result in BLOCKED state with detailed diagnostics.

## Implementation Notes

### Phase 4.5 Enhancement Example

```
## ABSOLUTE REQUIREMENT: 100% Test Pass Rate

Phase 4.5 is a ZERO-TOLERANCE quality gate. NO EXCEPTIONS.

**Mandatory Requirements**:
1. Code MUST compile with ZERO errors
2. ALL tests MUST pass (100% pass rate)
3. Coverage MUST meet thresholds (≥80% line, ≥75% branch)

**Enforcement**:
- ANY failing test → BLOCKED state
- ANY compilation error → BLOCKED state
- Coverage below threshold → BLOCKED state
- "Test infrastructure issues" is NOT a valid excuse

**Fix Loop Process** (up to 3 attempts):
1. Verify compilation (MANDATORY)
2. Execute ALL tests
3. Analyze failures
4. Apply fixes
5. Re-verify compilation
6. Re-execute ALL tests
7. Repeat until 100% pass OR max attempts reached

**Result**:
- 100% tests passing → proceed to Phase 5
- ANY failures after 3 attempts → BLOCKED state (no exceptions)
```

### Step 6 Enhancement Example

```python
# ZERO-TOLERANCE EVALUATION LOGIC

def evaluate_task_completion(test_results, coverage_results):
    """
    Determines if task can transition to IN_REVIEW.

    ABSOLUTE REQUIREMENTS (NO EXCEPTIONS):
    - Compilation errors: 0
    - Test failures: 0
    - Line coverage: ≥80%
    - Branch coverage: ≥75%
    """

    # Check compilation
    if test_results.compilation_errors > 0:
        return {
            "can_complete": False,
            "state": "BLOCKED",
            "reason": f"Compilation failed with {test_results.compilation_errors} errors",
            "message": "Fix ALL compilation errors before proceeding"
        }

    # Check test pass rate (ZERO TOLERANCE)
    if test_results.failed_tests > 0:
        return {
            "can_complete": False,
            "state": "BLOCKED",
            "reason": f"{test_results.failed_tests} tests failing",
            "message": "ALL tests must pass. NO EXCEPTIONS. 'Test infrastructure issues' is NOT an excuse."
        }

    # Check coverage thresholds
    if coverage_results.line_coverage < 80.0 or coverage_results.branch_coverage < 75.0:
        return {
            "can_complete": False,
            "state": "BLOCKED",
            "reason": f"Coverage below threshold (line: {coverage_results.line_coverage}%, branch: {coverage_results.branch_coverage}%)",
            "message": "Add tests to meet coverage requirements"
        }

    # ALL requirements met
    return {
        "can_complete": True,
        "state": "IN_REVIEW",
        "reason": "All quality gates passed",
        "message": "Task ready for review"
    }

# NEVER complete with ANY failing tests
```

## Testing Strategy

1. Create a test task with intentionally failing tests
2. Run `/task-work` on the test task
3. Verify it enters BLOCKED state (not IN_REVIEW)
4. Fix the tests to pass
5. Re-run `/task-work`
6. Verify it transitions to IN_REVIEW only after 100% pass

## Related Documentation

- [CLAUDE.md](../../CLAUDE.md) - Quality Gates section
- [task-work.md](../../installer/global/commands/task-work.md) - Phase 4.5 and Step 6
- [test-orchestrator.md](../../installer/global/agents/test-orchestrator.md) - Quality Gates

## Priority Justification

**CRITICAL** priority because:
- Blocks accurate CI/CD pipeline execution
- Compromises quality assurance integrity
- Allows broken code to reach review/production
- Undermines the entire Agentecflow quality philosophy
- Affects all technology stacks and templates
