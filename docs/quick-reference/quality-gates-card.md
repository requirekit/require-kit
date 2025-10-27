# Quality Gates Reference

## Overview

Quality gates enforce zero-tolerance quality standards in Agentecflow Lite. Tasks cannot proceed to IN_REVIEW state unless ALL gates pass. The Phase 4.5 fix loop automatically attempts to resolve failures (up to 3 attempts).

## Quick Reference

### All Quality Gates
| Gate | Threshold | Status | Action if Failed |
|------|-----------|--------|------------------|
| **Compilation** | 100% success | MANDATORY | BLOCKED (cannot run tests) |
| **Tests Pass** | 100% (all pass) | MANDATORY | Fix loop (3 attempts) |
| **Line Coverage** | ≥80% | MANDATORY | Generate more tests |
| **Branch Coverage** | ≥75% | MANDATORY | Generate more tests |
| **Architectural Review** | ≥60/100 | RECOMMENDED | Human checkpoint |
| **Performance** | <30s test runtime | WARNING | Suggest optimization |

### Zero Tolerance Rules

**Rule 1: Compilation** (BLOCKING)
- Code MUST compile with zero errors
- Tests will NOT run if compilation fails
- **Consequence**: Task moves to BLOCKED immediately

**Rule 2: Tests Pass** (BLOCKING)
- ALL tests MUST pass (100% pass rate)
- NO tests can be skipped, ignored, or commented out
- **Consequence**: Fix loop (up to 3 attempts), then BLOCKED

**Rule 3: Coverage** (REGENERATIVE)
- Line coverage ≥ 80%
- Branch coverage ≥ 75%
- **Consequence**: Task stays IN_PROGRESS, more tests generated

### Phase 4.5 Fix Loop Flowchart
```
Phase 4: Tests Execute
    ↓
┌───[All tests pass?]───┐
│   YES              NO  │
│    ↓                ↓  │
│ Phase 5      Fix Attempt 1
│              (analyze failures)
│                   ↓
│            Re-run tests
│                   ↓
│         [All tests pass?]
│           YES        NO
│            ↓          ↓
│         Phase 5  Fix Attempt 2
│                  (analyze failures)
│                       ↓
│                 Re-run tests
│                       ↓
│              [All tests pass?]
│                YES        NO
│                 ↓          ↓
│              Phase 5  Fix Attempt 3
│                       (analyze failures)
│                            ↓
│                      Re-run tests
│                            ↓
│                   [All tests pass?]
│                     YES        NO
│                      ↓          ↓
│                   Phase 5   BLOCKED
│
└─→ Continue workflow
```

## Decision Guide

### When Gates Fail

**Compilation Fails**
1. Check error messages for file:line details
2. Fix compilation errors manually
3. Verify all dependencies installed
4. Re-run `/task-work TASK-XXX`

**Tests Fail (1st Attempt)**
- System automatically analyzes failures
- Generates fixes based on error patterns
- Re-runs tests with fixes applied
- **No manual intervention required**

**Tests Fail (2nd Attempt)**
- System re-analyzes remaining failures
- Attempts alternative fix strategies
- Re-runs tests again
- **No manual intervention required**

**Tests Fail (3rd Attempt - Final)**
- System exhausts automatic fix strategies
- Task moves to BLOCKED state
- Diagnostics saved to task file
- **Manual intervention required**

**Coverage Below Threshold**
- Task stays in IN_PROGRESS
- Testing agent generates additional tests
- Re-run Phase 4 automatically
- **No manual intervention required**

### Escalation Paths

**Level 1: Automatic (Phase 4.5)**
- Fix loop handles test failures automatically
- Up to 3 attempts with different strategies
- Most failures resolved without human intervention

**Level 2: Manual (BLOCKED state)**
- Review detailed diagnostics in task file
- Fix issues manually in code
- Re-run `/task-work TASK-XXX` to retry
- Task resumes from Phase 3 (implementation)

**Level 3: Architectural (High complexity)**
- Failures indicate design issues
- Consider running `/task-work TASK-XXX --design-only`
- Review architectural review recommendations
- May need to revise implementation approach

**Level 4: Team Escalation (Persistent failures)**
- Consult with senior developer or architect
- Review task complexity (may need breakdown)
- Consider splitting into smaller subtasks
- Update requirements if needed

## Examples

### Example 1: Compilation Failure
```bash
/task-work TASK-042

Phase 4: Testing
🔨 Verifying compilation...
❌ COMPILATION FAILED - Cannot proceed with tests

Errors:
  src/auth/login.py:45 - NameError: name 'bcrypt' not defined
  src/auth/session.py:23 - ImportError: No module named 'jwt'

Task moved to BLOCKED state

Next Steps:
1. Install missing dependencies: pip install bcrypt pyjwt
2. Fix import statements
3. Re-run: /task-work TASK-042
```

### Example 2: Test Failures (Successful Fix Loop)
```bash
/task-work TASK-042

Phase 4: Testing
✅ Compilation successful
🧪 Running tests...
❌ 3 tests failed

Phase 4.5: Fix Loop (Attempt 1/3)
Analyzing failures:
  - test_login_with_invalid_password: AssertionError
  - test_session_expiry: Expected behavior mismatch
  - test_password_validation: None returned instead of error

Generating fixes...
Re-running tests...
✅ All tests passing!

Phase 5: Code Review
✅ Task moved to IN_REVIEW
```

### Example 3: Coverage Below Threshold
```bash
/task-work TASK-042

Phase 4: Testing
✅ Compilation successful
✅ All tests passing (15/15)
⚠️  Coverage: 72% (required: 80%)

Uncovered code:
  - src/auth/login.py lines 45-52 (error handling)
  - src/auth/session.py lines 78-85 (edge case)

Generating additional tests...
Re-running tests with new coverage...
✅ Coverage: 84% (threshold met)

Phase 5: Code Review
```

### Example 4: BLOCKED After 3 Attempts
```bash
/task-work TASK-042

Phase 4.5: Fix Loop (Attempt 3/3)
❌ Unable to achieve passing tests after 3 attempts

Final Status:
  - Tests: 12 passed, 2 failed
  - Failures: test_oauth_callback, test_token_refresh

Task moved to BLOCKED state

Diagnostics saved to: tasks/blocked/TASK-042.md

Required Actions:
1. Review OAuth provider configuration
2. Verify redirect URI settings
3. Check token refresh logic
4. Re-run after manual fixes: /task-work TASK-042
```

## Common Failure Patterns

### Pattern 1: Missing Dependencies
```
Error: ImportError: No module named 'X'
Fix: Install dependency via package manager
Prevention: Declare all dependencies in requirements/package.json
```

### Pattern 2: Async Handling
```
Error: Promise rejected / Timeout exceeded
Fix: Add proper async/await handling
Prevention: Use async testing utilities
```

### Pattern 3: State Management
```
Error: Cannot read property 'X' of undefined
Fix: Verify test data setup and initialization
Prevention: Use test fixtures and factories
```

### Pattern 4: External Services
```
Error: ECONNREFUSED / Service unavailable
Fix: Mock external services in tests
Prevention: Use dependency injection for testability
```

## See Also

**Full Documentation**:
- Task workflow: `installer/global/commands/task-work.md` (Phase 4-4.5)
- Test orchestration: `installer/global/agents/test-orchestrator.md`
- Code review: `installer/global/agents/code-reviewer.md`

**Related Cards**:
- [task-work-cheat-sheet.md](task-work-cheat-sheet.md) - Complete workflow phases
- [complexity-guide.md](complexity-guide.md) - Task complexity evaluation
- [design-first-workflow-card.md](design-first-workflow-card.md) - Complex task handling
