# Task-Work Command: Practical Example

## Scenario: Implementing User Authentication

This example demonstrates how the new unified `/task-work` command streamlines the development process compared to the current multi-command approach.

## Current Approach (7 Commands) ❌

```bash
# 1. Create task
/task-create "Implement user authentication" priority:high

# 2. Link requirements
/task-link-requirements TASK-042 REQ-001 REQ-002 REQ-003

# 3. Link BDD scenarios  
/task-link-bdd TASK-042 BDD-001 BDD-002

# 4. Start work
/task-start TASK-042

# 5. Generate implementation
/task-implement TASK-042 test-first:true

# 6. Run tests
/task-test TASK-042

# 7. If tests pass, move to review
/task-review TASK-042
```

**Problems:**
- Developer must remember 7 different commands
- Easy to skip steps (especially testing)
- Manual state management
- No guarantee of quality verification

## New Approach (1 Command) ✅

```bash
# Single command does everything
/task-work TASK-042 --mode=tdd
```

## What Happens Behind the Scenes

### Initial Task File
```markdown
# tasks/in_progress/TASK-042.md
---
id: TASK-042
title: Implement user authentication
status: in_progress
requirements: [REQ-001, REQ-002, REQ-003]
bdd_scenarios: [BDD-001, BDD-002]
---

## Requirements
- REQ-001: User login with email/password
- REQ-002: Session management with JWT
- REQ-003: Password reset functionality

## Acceptance Criteria
- [ ] Users can log in with valid credentials
- [ ] Invalid credentials show error message
- [ ] Sessions expire after 24 hours
- [ ] Users can reset forgotten passwords
```

### Step-by-Step Execution

#### 1. Command Invocation
```
User: /task-work TASK-042 --mode=tdd
```

#### 2. Claude's Response - Phase 1: Test Generation (RED)
```
🔴 TDD Mode: Generating Failing Tests for TASK-042

Creating test file: tests/test_auth_service.py

📝 Generated 8 tests based on requirements:
- ✍️ test_successful_login_with_valid_credentials
- ✍️ test_login_fails_with_invalid_password  
- ✍️ test_login_fails_with_nonexistent_user
- ✍️ test_session_token_is_jwt_format
- ✍️ test_session_expires_after_24_hours
- ✍️ test_password_reset_sends_email
- ✍️ test_password_reset_token_expires
- ✍️ test_password_reset_updates_password

Running tests to confirm RED state...

❌ All 8 tests failing (expected in TDD)
- ImportError: cannot import name 'AuthService'

Ready for GREEN phase...
```

#### 3. Claude's Response - Phase 2: Implementation (GREEN)
```
🟢 TDD Mode: Implementing Code to Pass Tests

Creating implementation files:
- ✅ src/services/auth_service.py (120 lines)
- ✅ src/models/user_model.py (45 lines)  
- ✅ src/utils/jwt_handler.py (35 lines)
- ✅ src/utils/email_service.py (28 lines)

Running tests...

✅ 6/8 tests passing
❌ 2 tests still failing:
- test_session_expires_after_24_hours: Expiry not set correctly
- test_password_reset_token_expires: Token expiry missing

Fixing implementation...
- Updated jwt_handler.py: Added expiry parameter
- Updated auth_service.py: Set 24-hour expiry

Running tests again...

✅ All 8 tests passing!

Moving to REFACTOR phase...
```

#### 4. Claude's Response - Phase 3: Refactoring & Coverage
```
🔵 TDD Mode: Refactoring and Improving Coverage

Code improvements:
- ♻️ Extracted password validation to separate method
- ♻️ Added type hints throughout
- ♻️ Improved error messages
- ♻️ Added logging for security events

Running extended test suite...

📊 Test Results:
├─ Unit Tests: 8/8 passing ✅
├─ Integration Tests: 3/3 passing ✅
├─ Total: 11 tests passing
└─ Duration: 2.3s

📈 Coverage Report:
├─ Lines: 92% ✅ (target: 80%)
├─ Branches: 88% ✅ (target: 75%)
├─ Functions: 100% ✅
└─ Statements: 91% ✅

🎯 All Quality Gates: PASSED
```

#### 5. Claude's Response - Final Summary
```
✅ TASK-042 Implementation Complete!

## Summary
- **Mode**: TDD (Red-Green-Refactor)
- **Duration**: 45 seconds
- **Files Created**: 7
- **Tests Written**: 11
- **Coverage**: 92%

## Implementation Details

### Files Created
1. `src/services/auth_service.py` - Main authentication logic
2. `src/models/user_model.py` - User data model
3. `src/utils/jwt_handler.py` - JWT token management
4. `src/utils/email_service.py` - Email sending for password reset
5. `tests/test_auth_service.py` - Unit tests
6. `tests/integration/test_auth_flow.py` - Integration tests
7. `docs/api/auth_endpoints.md` - API documentation

### Requirements Satisfied
- ✅ REQ-001: Login with email/password implemented
- ✅ REQ-002: JWT session management working
- ✅ REQ-003: Password reset flow complete

### BDD Scenarios Passing
- ✅ BDD-001: User login scenario
- ✅ BDD-002: Password reset scenario

## Task Status Update
**Previous**: IN_PROGRESS
**Current**: IN_REVIEW
**Reason**: All tests passing, coverage exceeds thresholds

## Next Steps
1. Review the implementation: `/task-review TASK-042`
2. Or make changes and re-test: `/task-work TASK-042`
3. View detailed test report: `/task-view TASK-042 --show-tests`

Task file updated: tasks/in_review/TASK-042.md
```

### Final Task File After Work
```markdown
# tasks/in_review/TASK-042.md
---
id: TASK-042
title: Implement user authentication
status: in_review
created: 2024-01-15T09:00:00Z
updated: 2024-01-15T09:45:00Z
assignee: current_user
priority: high
requirements: [REQ-001, REQ-002, REQ-003]
bdd_scenarios: [BDD-001, BDD-002]
test_results:
  status: passed
  last_run: 2024-01-15T09:45:00Z
  coverage: 92
  passed: 11
  failed: 0
  duration: 2.3
implementation:
  mode: tdd
  files_created: 7
  lines_of_code: 263
  lines_of_tests: 198
---

## Requirements
- ✅ REQ-001: User login with email/password
- ✅ REQ-002: Session management with JWT
- ✅ REQ-003: Password reset functionality

## Acceptance Criteria
- [x] Users can log in with valid credentials
- [x] Invalid credentials show error message
- [x] Sessions expire after 24 hours
- [x] Users can reset forgotten passwords

## Implementation Summary

### TDD Workflow
1. **RED Phase**: Created 8 failing tests based on requirements
2. **GREEN Phase**: Implemented minimal code to pass tests
3. **REFACTOR Phase**: Improved code quality while maintaining green tests

### Files Created
- `src/services/auth_service.py` - Core authentication logic
- `src/models/user_model.py` - User model with validation
- `src/utils/jwt_handler.py` - JWT token management
- `src/utils/email_service.py` - Email service for password reset
- `tests/test_auth_service.py` - Comprehensive unit tests
- `tests/integration/test_auth_flow.py` - End-to-end flow tests
- `docs/api/auth_endpoints.md` - API documentation

### Test Coverage
- Line Coverage: 92%
- Branch Coverage: 88%
- Function Coverage: 100%
- All 11 tests passing

### Quality Gates
✅ All tests passing
✅ Coverage exceeds minimum (80%)
✅ No security vulnerabilities detected
✅ Performance benchmarks met (<100ms response)
✅ Documentation complete

## Review Checklist
- [ ] Code follows project conventions
- [ ] Error handling is comprehensive
- [ ] Security best practices followed
- [ ] API documentation accurate
- [ ] No hardcoded secrets
- [ ] Logging appropriate
```

## Comparison: Old vs New

### Old Workflow (Multiple Commands)
```
Time: ~10 minutes (with context switching)
Commands to remember: 7
Risk of skipping steps: High
Manual verification: Required
State management: Manual
Quality guarantee: No
```

### New Workflow (Single Command)
```
Time: ~1 minute
Commands to remember: 1
Risk of skipping steps: None (automated)
Manual verification: Not needed
State management: Automatic
Quality guarantee: Built-in
```

## Different Modes Examples

### Standard Mode (Default)
```bash
/task-work TASK-043
# Generates implementation and tests together
# Runs tests once
# Updates state based on results
```

### TDD Mode
```bash
/task-work TASK-044 --mode=tdd
# Tests first (RED)
# Minimal implementation (GREEN)
# Refactor (REFACTOR)
# Ensures test-driven development
```

### BDD Mode
```bash
/task-work TASK-045 --mode=bdd
# Starts from Gherkin scenarios
# Generates step definitions
# Implements features to satisfy scenarios
# Creates additional unit tests
```

### Hotfix Mode
```bash
/task-work TASK-046 --mode=hotfix
# Minimal tests for the fix
# Quick implementation
# Fast verification
# Expedited to review
```

## Error Recovery Examples

### Example: Test Failure
```
/task-work TASK-047

❌ Tests Failed - TASK-047 Blocked

Failed Test: test_data_validation
  AssertionError: Expected ValidationError not raised
  
Suggested Fix:
Add validation in data_service.py:
  if not data.is_valid():
      raise ValidationError("Invalid data format")

After fixing, run:
/task-work TASK-047 --fix-only
```

### Example: Low Coverage
```
/task-work TASK-048

⚠️ Coverage Below Threshold

Current: 75% (Required: 80%)

Uncovered lines:
- error_handler.py: lines 23-29
- data_processor.py: lines 45-52

Generating additional tests...
✅ Added 3 tests for error scenarios
✅ Coverage now: 85%

Task moved to IN_REVIEW
```

## Integration with External Tools

### Future MCP Integration
```bash
# When MCP servers are available
/task-work TASK-049 --sync-to=jira

# Would automatically:
# 1. Create/update Jira ticket
# 2. Log work time
# 3. Attach test results
# 4. Update status
# 5. Link commits
```

### CI/CD Integration
```yaml
# Automated in CI pipeline
on: [push]
jobs:
  task-work:
    steps:
      - run: claude-code task-work $TASK_ID --mode=ci
      # Runs in CI mode with:
      # - Stricter quality gates
      # - Full test suite
      # - Security scanning
      # - Performance benchmarks
```

## Benefits Realized

1. **Developer Productivity**: 70% reduction in command complexity
2. **Quality Assurance**: 100% of tasks have tests before review
3. **Faster Feedback**: Immediate test results and quality verification
4. **Better Compliance**: TDD/BDD practices enforced automatically
5. **Reduced Defects**: Issues caught before code review
6. **Simplified Onboarding**: New developers only learn one command
7. **Consistent Workflow**: Every task follows the same quality process

## Conclusion

The unified `/task-work` command transforms task implementation from a multi-step, error-prone process into a single, reliable workflow that guarantees quality. By combining implementation, testing, and verification into one command, we ensure that every piece of code is tested, meets quality standards, and is ready for review - all with a single command that takes less than a minute to execute.
