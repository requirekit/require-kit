# Quality Gates Workflow

## Overview

Quality gates in Agentecflow Lite provide automated enforcement of code quality, testing standards, and implementation integrity. This workflow ensures that every task meets minimum quality thresholds before transitioning to review state, preventing broken code from entering the codebase.

**Key Quality Gates:**
- **Phase 4.5**: Test Enforcement Loop (zero-tolerance for failures)
- **Phase 5.5**: Plan Audit (scope creep detection)
- **Coverage Thresholds**: Automated measurement and enforcement
- **Performance Monitoring**: Test execution time tracking

## Prerequisites

- Task in `in_progress` state
- Implementation complete (Phase 3 finished)
- Tests generated or written (Phase 4 triggered)
- Project configured with testing framework

**Technology-Specific Requirements:**
- **Python**: pytest with pytest-cov installed
- **TypeScript/JavaScript**: Jest or Vitest configured
- **.NET**: xUnit with coverlet installed

## Phase 4.5: Test Enforcement Loop

Phase 4.5 implements **zero-tolerance** for test failures. The system automatically attempts to fix failing tests up to 3 times before blocking the task.

### Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                   PHASE 4.5: TEST ENFORCEMENT LOOP              │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │  Compilation Check    │
                    │  (Mandatory Step)     │
                    └───────────────────────┘
                                │
                ┌───────────────┴───────────────┐
                │                               │
                ▼                               ▼
    ┌───────────────────┐         ┌───────────────────┐
    │ Build SUCCESS     │         │ Build FAILED      │
    │ Continue →        │         │ Analyze errors    │
    └───────────────────┘         └───────────────────┘
                │                               │
                │                               ▼
                │                 ┌───────────────────────┐
                │                 │ Fix Loop (1 attempt)  │
                │                 │ - Fix compilation     │
                │                 │ - Rebuild             │
                │                 └───────────────────────┘
                │                               │
                │                 ┌─────────────┴─────────────┐
                │                 │                           │
                │                 ▼                           ▼
                │     ┌─────────────────┐       ┌─────────────────┐
                │     │ Fixed           │       │ Still Broken    │
                │     │ Continue →      │       │ → BLOCKED       │
                │     └─────────────────┘       └─────────────────┘
                │                 │
                └─────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │  Run Test Suite       │
                    └───────────────────────┘
                                │
                ┌───────────────┴───────────────┐
                │                               │
                ▼                               ▼
    ┌───────────────────┐         ┌───────────────────┐
    │ ALL TESTS PASS    │         │ TESTS FAIL        │
    │ Check coverage →  │         │ Enter fix loop    │
    └───────────────────┘         └───────────────────┘
                │                               │
                │                               ▼
                │                 ┌───────────────────────┐
                │                 │ Fix Loop (3 attempts) │
                │                 │ Attempt 1: Fix tests  │
                │                 │ Attempt 2: Fix tests  │
                │                 │ Attempt 3: Fix tests  │
                │                 └───────────────────────┘
                │                               │
                │                 ┌─────────────┴─────────────┐
                │                 │                           │
                │                 ▼                           ▼
                │     ┌─────────────────┐       ┌─────────────────┐
                │     │ Tests Pass      │       │ Still Failing   │
                │     │ Continue →      │       │ → BLOCKED       │
                │     └─────────────────┘       └─────────────────┘
                │                 │
                └─────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │  Phase 5: Review      │
                    └───────────────────────┘
```

### Zero-Tolerance Policy

**Enforcement Rules:**
1. **Compilation**: Code MUST compile with zero errors before testing
2. **Test Pass Rate**: 100% required (no failures, no skips)
3. **Coverage**: ≥80% line coverage, ≥75% branch coverage
4. **Performance**: <30s test execution (warning only)

**What Gets Blocked:**
- ❌ Compilation errors remaining after fix attempt
- ❌ Any test failures after 3 fix attempts
- ❌ Skipped or ignored tests (tests must run)
- ❌ Test crashes or unhandled exceptions

**What Gets Warning (Not Blocking):**
- ⚠️ Test execution time >30 seconds
- ⚠️ Coverage slightly below threshold (75-79%)
- ⚠️ No tests for utility functions (if justified)

### Fix Loop Process

**Attempt 1:**
```bash
1. Analyze failure messages and stack traces
2. Identify root cause (implementation bug, test issue, configuration)
3. Apply targeted fix (minimal change)
4. Re-run tests
5. If pass → continue, if fail → Attempt 2
```

**Attempt 2:**
```bash
1. Deeper analysis (check dependencies, state management)
2. Apply broader fix (may refactor implementation)
3. Re-run tests
4. If pass → continue, if fail → Attempt 3
```

**Attempt 3 (Final):**
```bash
1. Comprehensive analysis (review entire implementation)
2. Apply complete fix (may restructure code)
3. Re-run tests
4. If pass → continue, if fail → BLOCKED
```

### Example: Test Failure Recovery

**Scenario**: Authentication service tests failing due to password hashing

**Initial Failure (Phase 4):**
```
❌ Test Suite Failed: 3/15 tests failing

Failed Tests:
1. test_auth_service.py::test_login_valid_credentials
   AssertionError: Expected 200, got 401

2. test_auth_service.py::test_password_verification
   AssertionError: Password verification failed for valid password

3. test_auth_service.py::test_session_creation
   SessionNotFoundError: No session created after login
```

**Fix Loop - Attempt 1:**
```
Analyzing failures...
Root cause: Password hashing mismatch (bcrypt vs sha256)

Applying fix:
- Updated AuthService.verify_password to use bcrypt
- Added bcrypt dependency

Re-running tests...
✅ All tests passed!

Duration: 45 seconds
Coverage: 87% (line), 82% (branch)
```

**Result**: Proceed to Phase 5 (Code Review)

## Phase 5.5: Plan Audit

After implementation completes and tests pass, Phase 5.5 audits the implementation against the original plan to detect scope creep and variances.

### Audit Checks

| Check | Purpose | Threshold |
|-------|---------|-----------|
| **File Count Match** | Verify planned files created | 100% match |
| **Implementation Completeness** | All planned work done | 100% complete |
| **Scope Creep Detection** | No unplanned features | 0 violations |
| **LOC Variance** | Actual vs estimated lines | ±20% acceptable |
| **Duration Variance** | Actual vs estimated time | ±30% acceptable |
| **Test Coverage** | Meets threshold | ≥80% line, ≥75% branch |

### Decision Options

When plan audit runs, you'll see one of these outcomes:

**1. ✅ APPROVED** (All checks passed)
```
VERDICT: ✅ APPROVED - Implementation matches plan

All planned files created
No scope creep detected
Variances within tolerance
Coverage exceeds threshold

OPTIONS:
[A] Approve - Mark task complete (recommended)
[V] View - Show detailed audit report
```

**2. ⚠️ VARIANCE DETECTED** (Minor issues)
```
VERDICT: ⚠️ VARIANCE - Review recommended

Files: 4/4 created ✅
LOC: +15% over estimate (acceptable)
Duration: +25% over estimate (acceptable)
Scope: No violations ✅

VARIANCES:
- Implementation took longer due to edge case handling
- Added extra validation (within scope)

OPTIONS:
[A] Approve - Accept variances (recommended)
[R] Review - Examine variances in detail
[J] Justify - Add justification notes
```

**3. ❌ SCOPE CREEP** (Major issues)
```
VERDICT: ❌ SCOPE CREEP - Escalation required

Files: 6/4 created (2 unplanned) ❌
LOC: +45% over estimate ❌
Scope violations: 2 detected

UNPLANNED CHANGES:
- Added caching layer (not in plan)
- Implemented rate limiting (not in requirements)

OPTIONS:
[E] Escalate - Requires senior review (recommended)
[J] Justify - Explain why changes were necessary
[R] Revert - Remove unplanned changes
[C] Cancel - Mark task invalid
```

### Scope Creep Detection

**What Triggers Scope Creep Alert:**
- ❌ Unplanned files created (not in implementation plan)
- ❌ Unplanned features implemented (not in requirements)
- ❌ Unplanned dependencies added (not in plan)
- ❌ LOC variance >50% (major underestimate or overengineering)
- ❌ Duration variance >100% (plan was significantly off)

**What Doesn't Trigger Alert:**
- ✅ Refactoring for better code quality
- ✅ Bug fixes discovered during implementation
- ✅ Additional tests beyond minimum coverage
- ✅ Improved error handling (defensive programming)
- ✅ Better naming or documentation

### Example: Variance Threshold Violation

**Scenario**: User registration task exceeded LOC estimate by 60%

**Plan Audit Report:**
```
═══════════════════════════════════════════════════════
PHASE 5.5 - PLAN AUDIT
═══════════════════════════════════════════════════════

IMPLEMENTATION AUDIT RESULTS:

FILES:
  ✓ Planned: 3 files
  ✓ Created: 3 files
  ✓ Match: 100%

IMPLEMENTATION:
  ✓ All planned features completed
  ⚠️ Additional features detected:
     - Email verification workflow (not in original plan)
     - Password strength validation (not in original plan)

VARIANCES:
  Lines of Code: 480 (planned: 300) → +60% ❌ EXCEEDS TOLERANCE
  Duration: 6.5 hours (planned: 4 hours) → +62% ❌ EXCEEDS TOLERANCE

TESTS:
  ✓ Coverage: 89% (required: 80%)
  ✓ All tests passing

SCOPE CREEP: 2 violations detected

VERDICT: ❌ REQUIRES REVIEW

OPTIONS:
[E] Escalate - Requires senior review
[J] Justify - Explain additions
[R] Revert - Remove unplanned features
```

**Recommended Action**: Escalate for review, justify additions as necessary security features

## Quality Gate Thresholds

### Compilation (MANDATORY)

| Language | Command | Success Criteria |
|----------|---------|------------------|
| **Python** | `python -m py_compile src/**/*.py` | Exit code 0, no syntax errors |
| **TypeScript** | `tsc --noEmit` | Exit code 0, no type errors |
| **JavaScript** | `node --check src/**/*.js` | Exit code 0, no syntax errors |
| **.NET** | `dotnet build` | Exit code 0, 0 warnings (if configured) |

### Tests (MANDATORY)

| Metric | Threshold | Action if Failed |
|--------|-----------|------------------|
| **Pass Rate** | 100% | BLOCKED after 3 attempts |
| **Failed Tests** | 0 | Fix loop triggered |
| **Skipped Tests** | 0 | Must run all tests |
| **Test Crashes** | 0 | BLOCKED after 3 attempts |

### Coverage (MANDATORY)

| Type | Threshold | Action if Below |
|------|-----------|-----------------|
| **Line Coverage** | ≥80% | Generate additional tests |
| **Branch Coverage** | ≥75% | Generate additional tests |
| **Function Coverage** | ≥80% | Warning only |

### Performance (WARNING ONLY)

| Metric | Threshold | Action if Exceeded |
|--------|-----------|-------------------|
| **Total Test Time** | <30 seconds | Warning message |
| **Single Test Time** | <5 seconds | Warning message |

## Troubleshooting

### Common Failures and Solutions

#### Issue: Compilation Errors Persist After Fix

**Symptoms:**
- Build fails after fix attempt
- Same errors repeat across attempts
- New errors appear after each fix

**Diagnosis:**
```bash
# Check for circular dependencies
grep -r "import.*from.*src" src/

# Verify dependency versions
pip freeze | grep <package>  # Python
npm list <package>          # Node
dotnet list package         # .NET
```

**Solutions:**
1. **Circular Dependencies**: Refactor to break cycles
2. **Missing Dependencies**: Install required packages
3. **Version Conflicts**: Update or pin dependency versions
4. **Type Errors**: Add type annotations or fix type mismatches

#### Issue: Tests Fail Intermittently

**Symptoms:**
- Tests pass sometimes, fail other times
- Different failures on each run
- "Flaky test" warnings

**Diagnosis:**
```bash
# Run tests multiple times
for i in {1..10}; do pytest tests/ -v; done

# Check for race conditions
pytest tests/ -v --tb=long

# Look for shared state
grep -r "global " tests/
```

**Solutions:**
1. **Race Conditions**: Add proper synchronization (locks, async/await)
2. **Shared State**: Use test fixtures to isolate state
3. **External Dependencies**: Mock external services
4. **Timing Issues**: Add retries or increase timeouts

#### Issue: Coverage Below Threshold

**Symptoms:**
- Line coverage: 72% (required: 80%)
- Branch coverage: 68% (required: 75%)
- Specific files with low coverage

**Diagnosis:**
```bash
# Identify uncovered lines
pytest --cov=src --cov-report=html
open htmlcov/index.html

# Find uncovered branches
pytest --cov=src --cov-branch --cov-report=term-missing
```

**Solutions:**
1. **Add Edge Case Tests**: Test error conditions, boundary values
2. **Test Private Methods**: Use test fixtures to access private methods
3. **Integration Tests**: Add tests for component interactions
4. **Mock External Services**: Test error handling with mocked failures

#### Issue: Fix Loop Max Attempts Exceeded

**Symptoms:**
- 3 fix attempts completed
- Tests still failing
- Task moved to BLOCKED state

**Diagnosis:**
```bash
# Review fix loop log
cat docs/state/{task_id}/fix_loop_log.json

# Check test output
cat docs/state/{task_id}/test_results_attempt_3.json

# Review implementation changes
git diff HEAD~3 HEAD
```

**Solutions:**
1. **Manual Review Required**: Complex issue needs human analysis
2. **Architectural Problem**: Design needs revision
3. **Test Specification Error**: Tests may be incorrect
4. **External Dependency Issue**: Service or API not available

## Escalation Paths

### When to Escalate

**Immediate Escalation (BLOCKING):**
- ❌ Compilation errors persist after 3 attempts
- ❌ Tests fail after 3 attempts with no progress
- ❌ Scope creep detected (unplanned features)
- ❌ Security vulnerabilities found in code review

**Review Required (WARNING):**
- ⚠️ Coverage slightly below threshold (75-79%)
- ⚠️ Performance issues (>30s test execution)
- ⚠️ LOC variance >50% (significant underestimate)
- ⚠️ Duration variance >100% (plan significantly off)

**Normal Progress (NO ESCALATION):**
- ✅ All tests passing after fix loop
- ✅ Coverage exceeds thresholds
- ✅ Variances within acceptable range
- ✅ No scope creep detected

### Escalation Workflow

**Step 1: Gather Context**
```bash
# Export task context
/task-status TASK-XXX --detailed > escalation_context.txt

# Export test results
cat docs/state/{task_id}/test_results.json >> escalation_context.txt

# Export plan audit
cat docs/state/{task_id}/plan_audit.json >> escalation_context.txt
```

**Step 2: Identify Blocker Type**
- **Technical**: Requires senior developer review
- **Architectural**: Requires architect review
- **Scope**: Requires product owner review
- **Security**: Requires security team review

**Step 3: Create Escalation Issue**
```bash
# For Jira users
/task-sync TASK-XXX --escalate --assignee "senior-dev"

# For Linear users
linear issue create --title "Escalation: TASK-XXX" \
  --description "$(cat escalation_context.txt)"

# For GitHub users
gh issue create --title "Escalation: TASK-XXX" \
  --body "$(cat escalation_context.txt)" \
  --label "escalation,blocked"
```

**Step 4: Await Resolution**
- Task remains in BLOCKED state
- Human review and fix required
- Re-run `/task-work TASK-XXX` after manual fix

## Related Workflows

- **[Agentecflow Lite Workflow](../guides/agentecflow-lite-workflow.md)** - Complete workflow overview
- **[Complexity Management Workflow](./complexity-management-workflow.md)** - Task complexity evaluation
- **[Design-First Workflow](./design-first-workflow.md)** - Design approval process
- **[Iterative Refinement Workflow](./iterative-refinement-workflow.md)** - Post-completion improvements

## FAQ

**Q: Can I skip quality gates for urgent fixes?**
A: No. Quality gates are mandatory. For urgent hotfixes, use complexity evaluation to auto-proceed (score 1-3), but tests must still pass.

**Q: What if tests are failing due to flaky external service?**
A: Mock the external service. Tests should not depend on external services. If service is critical, use test containers or local mock.

**Q: Can I manually approve tasks with failing tests?**
A: No. The system enforces zero-tolerance. Fix the tests or fix the implementation before approval.

**Q: What happens if coverage is 79% (just below 80%)?**
A: System generates warning and requests additional tests. For micro-tasks, coverage may be skipped. For standard tasks, coverage is mandatory.

**Q: How do I justify scope creep if it was necessary?**
A: Use the [J]ustify option in plan audit. Provide clear rationale: security requirement, performance requirement, bug fix, etc. Justification is logged in task metadata.

**Q: Can I disable quality gates for documentation-only changes?**
A: Yes. Use `--micro` flag for documentation tasks. Quality gates are simplified: compilation skipped, coverage skipped, only lint checks run.
