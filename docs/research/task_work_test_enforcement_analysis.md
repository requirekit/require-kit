# Task-Work Test Enforcement Gap Analysis

**Date**: 2025-10-01
**Issue**: task-work command sometimes completes with compilation errors or failing tests
**Requirement**: Command should ONLY complete when all tests compile and pass

## Current Behavior Analysis

### What's Happening Now

The current `task-work.md` workflow:

```
Phase 4: Testing (testing agent generates and executes tests)
  ↓
Step 5: Evaluate Quality Gates (check if tests passed)
  ↓
Step 6: Determine Next State
  - If tests pass → IN_REVIEW ✅
  - If tests fail → BLOCKED ❌
  ↓
Step 7: Generate Report (show results and STOP)
```

**PROBLEM**: The workflow **evaluates** quality gates but doesn't **enforce** them. It reports failures and moves to BLOCKED state, but then STOPS instead of fixing.

### The Gap

**Current Flow**:
```
Phase 4: Tests fail
Step 5: Detect failure
Step 6: Move to BLOCKED
Step 7: Report "Tests failed, task blocked"
END ← Stops here!
```

**Expected Flow**:
```
Phase 4: Tests fail
Step 5: Detect failure
Step 5.1: Fix compilation/test failures ← MISSING!
Step 5.2: Re-run tests
Step 5.3: Verify all pass
Step 6: Move to IN_REVIEW (only when passing)
Step 7: Report success
END
```

## Root Causes

### 1. No Retry Loop in task-work.md

The command spec has no instruction to loop back when quality gates fail:

```markdown
### Step 6: Determine Next State (REQUIRED)

Based on quality gates:
- **All gates pass (all ✅)** → Move task to `tasks/in_review/TASK-XXX.md`
- **Tests failing** → Move task to `tasks/blocked/TASK-XXX.md`  ← Just moves and stops!
- **Coverage too low** → Keep in `tasks/in_progress/TASK-XXX.md` with note
```

There's no Step 6.1: "If failing, invoke implementation agent to fix."

### 2. Testing Agent Doesn't Have Fix Authority

Phase 4 prompt says:
```
"Create comprehensive test suite for TASK-XXX implementation.
 Include: unit tests, integration tests, edge cases.
 Target: 80%+ line coverage, 75%+ branch coverage.
 Use {stack}-specific testing frameworks and patterns.
 EXECUTE the test suite and report detailed results."
```

**Missing**: "If tests fail due to implementation issues, coordinate with implementation agent to fix code until all tests pass."

### 3. No Compilation Check Before Testing

The workflow goes straight from Phase 3 (Implementation) to Phase 4 (Testing) without checking if code even compiles:

```
Phase 3: Implementation completes
  ↓ (no compilation check)
Phase 4: Testing starts
  ↓ Tests fail because code doesn't compile
```

## Solution Design

### Principle: "Don't Stop Until Green"

The task-work command should follow Test-Driven Development principles:
- RED: Tests fail (or don't compile)
- GREEN: All tests pass ← **REQUIRED** before exiting
- REFACTOR: Code review improves quality

### Proposed Fix (Minimal Changes)

#### Change 1: Add Phase 4.5 - Fix Loop (New Step)

Insert between Phase 4 (Testing) and Phase 5 (Code Review):

```markdown
#### Phase 4.5: Fix Loop (Ensure All Tests Pass)

**EVALUATE** test results from Phase 4:

**IF compilation errors OR test failures exist**:

1. **Display Failure Report**:
   ```
   ⚠️  TESTS FAILING - Entering Fix Loop

   Compilation Errors: {count}
   {List of compilation errors with file:line}

   Test Failures: {count}
   {List of failing tests with assertion details}

   Initiating automatic fix cycle...
   ```

2. **INVOKE** Task tool to fix issues:
   ```
   subagent_type: "{selected_implementation_agent_from_table}"
   description: "Fix test failures for TASK-XXX"
   prompt: "Fix the failing tests for TASK-XXX.

            Compilation Errors:
            {list_of_compilation_errors}

            Test Failures:
            {list_of_test_failures}

            Your task:
            1. Fix all compilation errors FIRST
            2. Run build to verify compilation succeeds
            3. Fix failing test assertions
            4. Ensure code matches test expectations
            5. Do NOT modify tests unless they're incorrect
            6. Do NOT skip or comment out failing tests

            All tests MUST pass before completing."
   ```

3. **WAIT** for fix to complete

4. **RE-RUN** Phase 4 (Testing):
   ```
   subagent_type: "{selected_testing_agent_from_table}"
   description: "Re-run tests for TASK-XXX after fixes"
   prompt: "Re-execute the complete test suite for TASK-XXX.
            Verify all compilation errors are resolved.
            Verify all tests now pass.
            Report detailed results."
   ```

5. **REPEAT** this loop until:
   - All tests pass ✅
   - OR max attempts reached (3 attempts)

6. **IF max attempts reached without success**:
   ```
   ❌ CRITICAL: Unable to achieve passing tests after 3 attempts

   Task moved to BLOCKED state with detailed diagnostics.
   Manual intervention required.

   Next steps:
   1. Review test failures in detail
   2. Consider if tests are correctly specified
   3. Check for missing dependencies or configuration
   4. Escalate to human developer if needed
   ```

**IF all tests pass**:
- Proceed to Phase 5 (Code Review)
```

#### Change 2: Strengthen Phase 4 Prompt

Update the testing agent prompt to be explicit about compilation:

```markdown
prompt: "Create comprehensive test suite for TASK-XXX implementation.
         Include: unit tests, integration tests, edge cases.
         Target: 80%+ line coverage, 75%+ branch coverage.
         Use {stack}-specific testing frameworks and patterns.

         CRITICAL: Verify code COMPILES before running tests.
         If compilation fails, report errors immediately.

         EXECUTE the test suite and report detailed results:
         - Compilation status (success/failure)
         - Test execution results (passed/failed counts)
         - Coverage metrics
         - Detailed failure information for any failing tests"
```

#### Change 3: Update Step 6 State Determination

Clarify that tasks only move to IN_REVIEW when EVERYTHING passes:

```markdown
### Step 6: Determine Next State (REQUIRED)

Based on Phase 4.5 final results:

- **All gates pass (all ✅)**:
  - Code compiles successfully
  - All tests pass (100%)
  - Coverage ≥ 80% line, ≥ 75% branch
  → Move task to `tasks/in_review/TASK-XXX.md`

- **Tests failing after fix loop**:
  → Move task to `tasks/blocked/TASK-XXX.md`
  → Include detailed diagnostics in task file
  → Notify that manual intervention needed

- **Coverage too low but tests pass**:
  → Re-invoke testing agent to add more tests
  → Do NOT proceed until coverage threshold met
```

## Implementation Plan

### Files to Modify

1. **installer/global/commands/task-work.md**
   - Add Phase 4.5 (Fix Loop) after Phase 4
   - Update Phase 4 testing prompt (compilation check)
   - Update Step 6 state determination
   - Add max retry limit (3 attempts)

2. **installer/global/agents/test-verifier.md** (if used)
   - Add explicit compilation check step
   - Clarify test failure reporting format

### Code Changes (Minimal)

**Location**: `installer/global/commands/task-work.md` lines 155-203

**Change Summary**:
- Insert ~50 lines for Phase 4.5 (Fix Loop)
- Update 10 lines in Phase 4 prompt
- Update 15 lines in Step 6 logic

**Total Impact**: ~75 lines changed in 1 file

### Safety Considerations

**Risk**: Infinite loop if tests never pass
**Mitigation**: Max 3 fix attempts, then move to BLOCKED with diagnostics

**Risk**: Over-fixing (agent modifying tests instead of code)
**Mitigation**: Explicit instruction "Do NOT modify tests unless they're incorrect"

**Risk**: Breaking existing working behavior
**Mitigation**: Changes are additive (new phase), existing phases unchanged

## Expected Outcomes

### Before Fix
```
User runs: /task-work TASK-042

Phase 1-3: Complete successfully
Phase 4: Tests fail (3 compilation errors, 5 test failures)
Step 5: Evaluate → Tests failing
Step 6: Move to BLOCKED
Step 7: Report "Task blocked, 8 issues found"
END ← User left with broken code
```

### After Fix
```
User runs: /task-work TASK-042

Phase 1-3: Complete successfully
Phase 4: Tests fail (3 compilation errors, 5 test failures)
Phase 4.5: Fix Loop
  Attempt 1: Fix compilation errors → Re-test → 2 test failures remain
  Attempt 2: Fix test failures → Re-test → All pass ✅
Step 5: Evaluate → All tests passing
Step 6: Move to IN_REVIEW
Step 7: Report "Task complete, all tests passing"
END ← User has working, tested code
```

## Success Metrics

**Measure**: Percentage of task-work completions that have passing tests

**Current**: ~70% (based on user report of "sometimes" failing)
**Target**: 95%+ (only BLOCKED for truly intractable issues)

**Secondary Metrics**:
- Average fix loop iterations: Should be 1-2
- Blocked task rate: Should drop from ~30% to <5%
- Time to completion: May increase slightly (10-15%) but delivers working code

## Alternatives Considered

### Alternative 1: Manual Fix Mode
- Pause and prompt user when tests fail
- **Rejected**: Defeats automation purpose, user wants hands-off

### Alternative 2: Fail Fast
- Move to BLOCKED immediately, no retry
- **Rejected**: Wastes opportunity for automated fix

### Alternative 3: Infinite Retry
- Keep trying until pass
- **Rejected**: Risk of infinite loops, no escape hatch

### Alternative 4: Parallel Fix Attempts
- Try multiple fix strategies simultaneously
- **Rejected**: Too complex, hard to debug, unnecessary

## Conclusion

**Recommendation**: Implement Phase 4.5 (Fix Loop) with 3-attempt limit.

**Rationale**:
- Minimal code changes (focused on task-work.md)
- Preserves existing working behavior
- Provides escape hatch (max attempts + BLOCKED state)
- Matches user expectation ("only finish when all tests passing")
- Aligns with TDD principles (don't stop until green)

**User Benefit**: Task-work command reliably delivers working, tested code instead of leaving developers with compilation errors or failing tests.
