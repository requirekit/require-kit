# Task Management Command

Comprehensive task management with mandatory test verification before completion.

## Usage Patterns

### Create a new task
```bash
/task create <title> <description>
```

### Start working on a task
```bash
/task start TASK-XXX
```

### Implement a task with tests
```bash
/task implement TASK-XXX
```

### Run tests and verify
```bash
/task test TASK-XXX
```

### Move to review (only if tests pass)
```bash
/task review TASK-XXX
```

### Complete task (only after review)
```bash
/task complete TASK-XXX
```

### View task board
```bash
/task status
```

### View specific task details
```bash
/task view TASK-XXX
```

## Task Lifecycle

```
BACKLOG → IN_PROGRESS → IN_TESTING → IN_REVIEW → COMPLETED
                ↓             ↓            ↓
             BLOCKED       BLOCKED      BLOCKED
```

## Test Verification Requirements

Tasks CANNOT move to COMPLETED without:
1. ✅ All tests written and passing
2. ✅ Test results captured in task metadata
3. ✅ Coverage metrics meet thresholds
4. ✅ Performance benchmarks validated
5. ✅ Manual verification checklist complete

## Task File Structure

Each task is a markdown file with metadata:
```markdown
---
id: TASK-001
title: Implement user authentication
status: in_progress
created: 2024-01-15T10:00:00Z
updated: 2024-01-15T14:30:00Z
assignee: ai-engineer
priority: high
tags: [auth, security, backend]
requirements: [REQ-001, REQ-002]
bdd_scenarios: [BDD-001, BDD-002]
test_results:
  status: pending
  last_run: null
  coverage: null
  passed: null
  failed: null
---

# Task Description
[Detailed description]

## Acceptance Criteria
- [ ] User can log in with email/password
- [ ] Session tokens are secure
- [ ] Failed attempts are rate-limited

## Test Requirements
- [ ] Unit tests for auth service
- [ ] Integration tests for API endpoints
- [ ] E2E tests for login flow

## Implementation Notes
[Any relevant notes]

## Test Execution Log
[Automatically populated]
```

## Commands Implementation

### Create Task
1. Generate unique task ID
2. Create task file in backlog/
3. Link to requirements and BDD scenarios
4. Return task ID for reference

### Start Task
1. Move from backlog/ to in_progress/
2. Update status and timestamp
3. Set assignee
4. Create implementation branch (optional)

### Implement Task
1. Generate code based on requirements
2. Create comprehensive tests
3. Update task with implementation details
4. Move to in_testing/

### Test Task
1. Execute all related tests
2. Capture test results and coverage
3. Update task metadata with results
4. If tests fail → move to blocked/
5. If tests pass → ready for review

### Review Task
1. Verify test results are passing
2. Check coverage thresholds
3. Validate against requirements
4. Move to in_review/

### Complete Task
1. Final verification checks
2. Archive test results
3. Move to completed/
4. Update project metrics

## Quality Gates

Tasks are automatically blocked if:
- Test coverage < 80%
- Any critical tests failing
- Performance benchmarks not met
- Missing required documentation
- Incomplete acceptance criteria

## Integration Points

- **GitHub Issues**: Tasks can be linked to issues
- **CI/CD Pipeline**: Test results from CI are captured
- **MCP Code Checker**: Python test verification
- **Playwright**: UI test verification
- **dotnet test**: .NET test verification

## Automation Hooks

### Pre-move Validation
Before moving between states, validate:
- Required fields are complete
- Dependencies are resolved
- Tests are passing (for completion)
- Reviews are approved (for completion)

### Post-move Actions
After state changes:
- Update project metrics
- Notify stakeholders
- Trigger CI/CD if needed
- Update related tasks

## Example Workflow

```bash
# Create a new task
/task create "Add user profile page" "Create a profile page with edit capabilities"
# Output: Created TASK-042

# Start working on it
/task start TASK-042
# Output: TASK-042 moved to IN_PROGRESS

# Implement with tests
/task implement TASK-042
# Output: Implementation complete, tests created, moved to IN_TESTING

# Run tests
/task test TASK-042
# Output: 
#   ✅ 15/15 tests passing
#   ✅ Coverage: 87%
#   ✅ Performance: <100ms
#   Ready for review

# Move to review
/task review TASK-042
# Output: TASK-042 moved to IN_REVIEW

# Complete after review
/task complete TASK-042
# Output: TASK-042 completed and archived
```

## Dashboard View

```
/task status

KANBAN BOARD
============

BACKLOG (5)
-----------
• TASK-043: Implement search functionality
• TASK-044: Add export feature
• TASK-045: Create admin dashboard
• TASK-046: Optimize database queries
• TASK-047: Add multi-language support

IN_PROGRESS (2)
---------------
• TASK-041: Refactor auth service
• TASK-042: Add user profile page

IN_TESTING (1)
--------------
• TASK-040: Payment integration
  ⏳ Tests running...

IN_REVIEW (1)
-------------
• TASK-039: Email notifications
  ✅ All tests passing (25/25)
  📊 Coverage: 92%

BLOCKED (1)
-----------
• TASK-038: Social login
  ❌ 3 tests failing
  🔧 Needs: Fix OAuth callback

COMPLETED TODAY (3)
-------------------
✓ TASK-037: Password reset
✓ TASK-036: User preferences
✓ TASK-035: Activity logging
```
