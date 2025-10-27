# Kanban Task Workflow Implementation Guide

## Overview

This comprehensive guide explains how to use the kanban task workflow system with mandatory test verification. The system ensures that every task goes through proper development, testing, and review phases before completion.

## Core Philosophy

**"No task is complete until tests pass"**

The system enforces quality gates at every stage to prevent the common problem of "implemented but not working" code.

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Task Workflow System                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Commands                 Agents                        │
│  ├── task                 ├── task-manager             │
│  ├── task-create          └── test-verifier            │
│  ├── task-start                                         │
│  ├── task-implement       Task States                   │
│  ├── task-test            ├── backlog/                 │
│  ├── task-review          ├── in_progress/             │
│  ├── task-complete        ├── in_testing/              │
│  ├── task-status          ├── in_review/               │
│  ├── task-link-requirements ├── blocked/               │
│  └── task-link-bdd        └── completed/                │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Create Your First Task
```bash
# Create a new task
/task-create "Add user authentication" priority:high tags:security,backend

# Output: Created TASK-001
```

### 2. Link Requirements and Scenarios
```bash
# Link EARS requirements
/task-link-requirements TASK-001 REQ-001 REQ-002

# Link BDD scenarios
/task-link-bdd TASK-001 BDD-001 BDD-002
```

### 3. Start Working
```bash
# Move task to in_progress
/task-start TASK-001
```

### 4. Implement with Tests
```bash
# Generate implementation and tests
/task-implement TASK-001 test-first:true
```

### 5. Run Tests
```bash
# Execute and verify tests
/task-test TASK-001 verbose:true
```

### 6. Review
```bash
# Move to review after tests pass
/task-review TASK-001 reviewer:alice
```

### 7. Complete
```bash
# Mark as complete after review
/task-complete TASK-001
```

## Task Lifecycle

```
┌──────────┐     ┌──────────────┐     ┌────────────┐
│ BACKLOG  │────▶│ IN_PROGRESS  │────▶│ IN_TESTING │
└──────────┘     └──────────────┘     └────────────┘
                         │                    │
                         ▼                    ▼
                   ┌──────────┐        ┌──────────┐
                   │ BLOCKED  │        │ BLOCKED  │
                   └──────────┘        └──────────┘
                                              │
                                              ▼
┌──────────┐     ┌────────────┐       ┌────────────┐
│COMPLETED │◀────│ IN_REVIEW  │◀──────│    (pass)  │
└──────────┘     └────────────┘       └────────────┘
```

## Task File Structure

Each task is a markdown file with YAML frontmatter:

```yaml
---
id: TASK-001
title: Add user authentication
status: in_progress
created: 2024-01-15T10:00:00Z
updated: 2024-01-15T14:30:00Z
assignee: john
priority: high
tags: [security, backend]
requirements: [REQ-001, REQ-002]
bdd_scenarios: [BDD-001, BDD-002]
test_results:
  status: pending
  last_run: null
  coverage: null
  passed: null
  failed: null
  execution_log: null
blocked_reason: null
---

# Task Description
Implement secure user authentication with JWT tokens.

## Acceptance Criteria
- [ ] Users can log in with email/password
- [ ] Sessions use secure JWT tokens
- [ ] Failed attempts are rate-limited
- [ ] Passwords are properly hashed

## Test Requirements
- [ ] Unit tests for auth service
- [ ] Integration tests for login flow
- [ ] E2E tests for user journey
- [ ] Security tests for vulnerabilities

## Implementation Notes
Using bcrypt for password hashing, JWT for sessions.

## Test Execution Log
[Automatically populated when tests run]
```

## Test Verification Process

### Automatic Test Detection
The system automatically detects your testing framework:
- **Python**: pytest, unittest
- **JavaScript/TypeScript**: Jest, Vitest, Mocha
- **NET**: dotnet test, xUnit, NUnit
- **E2E**: Playwright, Cypress, Selenium

### Test Execution
```bash
# Python
pytest tests/ -v --cov=src --cov-report=term

# JavaScript
npm test -- --coverage

# .NET
dotnet test --collect:"XPlat Code Coverage"

# Playwright
npx playwright test
```

### Quality Gates
Tests must meet these thresholds:
- **Coverage**: ≥80% (configurable)
- **Pass Rate**: 100% for critical tests
- **Performance**: <30s total execution
- **No Flaky Tests**: Consistent results

### Test Results in Task
```yaml
test_results:
  status: passed
  last_run: 2024-01-15T14:30:00Z
  coverage: 87.5
  passed: 25
  failed: 0
  execution_log: |
    ============================= test session starts ==============================
    collected 25 items
    
    tests/test_auth.py::test_login PASSED                                    [ 4%]
    tests/test_auth.py::test_logout PASSED                                   [ 8%]
    ...
    
    ===================== 25 passed in 12.34s =====================
    
    Coverage Report:
    Name                  Stmts   Miss  Cover
    -----------------------------------------
    src/auth/service.py      45      6    87%
    src/auth/models.py       23      2    91%
    -----------------------------------------
    TOTAL                    68      8    88%
```

## Common Workflows

### Workflow 1: Feature Development
```bash
# 1. Create feature task
/task-create "Add search functionality" priority:high

# 2. Link requirements
/task-link-requirements TASK-002 REQ-010 REQ-011

# 3. Start development
/task-start TASK-002

# 4. Implement with TDD
/task-implement TASK-002 test-first:true

# 5. Run tests iteratively
/task-test TASK-002
# Fix failures...
/task-test TASK-002
# All pass!

# 6. Code review
/task-review TASK-002

# 7. Complete
/task-complete TASK-002
```

### Workflow 2: Bug Fix
```bash
# 1. Create bug task
/task-create "Fix login timeout" priority:critical tags:bug

# 2. Start immediately
/task-start TASK-003

# 3. Write regression test first
echo "def test_login_timeout_bug(): ..." > tests/test_regression.py

# 4. Fix the bug
# ... implement fix ...

# 5. Verify fix
/task-test TASK-003

# 6. Fast track review
/task-review TASK-003 checklist:quick

# 7. Deploy fix
/task-complete TASK-003
```

### Workflow 3: Refactoring
```bash
# 1. Create refactor task
/task-create "Refactor auth service" tags:refactor,technical-debt

# 2. Ensure existing tests pass
/task-test TASK-004

# 3. Start refactoring
/task-start TASK-004

# 4. Refactor code
# ... refactor implementation ...

# 5. Verify no regression
/task-test TASK-004

# 6. Review changes
/task-review TASK-004 checklist:strict

# 7. Complete
/task-complete TASK-004
```

## Handling Blocked Tasks

### When Tests Fail
```bash
# Task automatically moves to blocked
/task-test TASK-005
# ❌ 3 tests failing
# Task moved to BLOCKED

# Fix the issues
# ... fix code ...

# Re-run tests
/task-test TASK-005
# ✅ All tests passing
# Task can now proceed to review
```

### Manual Blocking
```bash
# Block a task with reason
/task-block TASK-006 "Waiting for API documentation"

# Unblock when ready
/task-unblock TASK-006
```

## Dashboard and Reporting

### View Current Board
```bash
# Default kanban view
/task-status

# Your tasks only
/task-status filter:mine

# Metrics dashboard
/task-status format:metrics
```

### Generate Reports
```bash
# Daily standup
/task-status report:standup

# Sprint summary
/task-status report:sprint

# Export to CSV
/task-status export:csv > tasks.csv
```

## Configuration

### Global Settings
`.claude/task-config.yaml`:
```yaml
quality_gates:
  coverage:
    minimum: 80
    target: 90
  performance:
    max_duration: 30
    max_single_test: 5
  
workflow:
  require_requirements: true
  require_bdd: false
  auto_assign: true
  
notifications:
  slack_webhook: https://...
  email_on_complete: true
```

### Per-Project Overrides
`.claude/project-task-config.yaml`:
```yaml
quality_gates:
  coverage:
    minimum: 90  # Stricter for this project
```

## Integration with External Tools

### GitHub Integration
```bash
# Link task to issue
/task-link-github TASK-007 issue:123

# Auto-close issue on completion
/task-complete TASK-007 --close-github-issue
```

### CI/CD Integration
```yaml
# .github/workflows/task-tests.yml
name: Task Tests
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run task tests
        run: |
          task_id=$(git branch --show-current | grep -oP 'TASK-\d+')
          claude-code task-test $task_id
```

## Best Practices

### 1. Always Link Requirements
Every task should trace back to requirements:
```bash
/task-link-requirements TASK-XXX REQ-YYY
```

### 2. Write Tests First
Use test-first approach:
```bash
/task-implement TASK-XXX test-first:true
```

### 3. Run Tests Frequently
Test early and often:
```bash
/task-test TASK-XXX --watch
```

### 4. Document Blockers
Always provide clear blocking reasons:
```bash
/task-block TASK-XXX "Missing third-party API key"
```

### 5. Review Thoroughly
Use appropriate review checklist:
```bash
/task-review TASK-XXX checklist:strict  # For critical features
/task-review TASK-XXX checklist:standard  # For normal features
/task-review TASK-XXX checklist:quick  # For minor changes
```

### 6. Capture Lessons Learned
Document what you learned:
```markdown
## Lessons Learned
- OAuth implementation more complex than expected
- Need better test fixtures for auth flow
- Consider using auth library next time
```

## Troubleshooting

### Problem: Tests Not Found
```bash
Error: No tests found for TASK-XXX
```
**Solution**: Ensure test files exist in standard locations:
- Python: `tests/`, `test_*.py`
- JavaScript: `__tests__/`, `*.test.js`
- .NET: `*.Tests.csproj`

### Problem: Coverage Too Low
```bash
Error: Coverage 65% is below 80% threshold
```
**Solution**: Add more tests or adjust threshold:
```bash
# Add more tests
/task-implement TASK-XXX --add-tests

# Or temporarily lower threshold (not recommended)
/task-test TASK-XXX --coverage-threshold:65
```

### Problem: Task Stuck in Blocked
```bash
Task TASK-XXX has been blocked for 3 days
```
**Solution**: Review and resolve:
```bash
# Check blocking reason
/task-view TASK-XXX

# Resolve issue and unblock
/task-unblock TASK-XXX

# Re-run tests
/task-test TASK-XXX
```

## Advanced Features

### Batch Operations
```bash
# Start multiple tasks
/task-batch start TASK-010 TASK-011 TASK-012

# Test all in_progress tasks
/task-batch test status:in_progress

# Complete all reviewed tasks
/task-batch complete status:in_review
```

### Task Dependencies
```bash
# Set dependency
/task-depends TASK-020 on:TASK-019

# View dependency graph
/task-dependencies --graph
```

### Time Tracking
```bash
# Log time spent
/task-log TASK-XXX hours:4 description:"Implemented auth service"

# View time report
/task-time-report TASK-XXX
```

## Command Reference

### Core Commands
- `/task` - Main task management command
- `/task-create` - Create new task
- `/task-start` - Begin work on task
- `/task-implement` - Generate implementation
- `/task-test` - Run and verify tests
- `/task-review` - Move to review
- `/task-complete` - Mark as done
- `/task-status` - View task board

### Utility Commands
- `/task-link-requirements` - Link EARS requirements
- `/task-link-bdd` - Link BDD scenarios
- `/task-block` - Block task with reason
- `/task-unblock` - Remove block
- `/task-view` - Show task details
- `/task-update` - Update task metadata
- `/task-delete` - Delete task (with confirmation)

### Reporting Commands
- `/task-status` - Current board view
- `/task-status report:standup` - Daily standup
- `/task-status report:sprint` - Sprint summary
- `/task-status export:csv` - Export to CSV

## Success Metrics

Track these metrics to measure system effectiveness:

### Quality Metrics
- **Test Coverage**: Average across all tasks (target: >85%)
- **First-Time Pass Rate**: Tasks passing tests on first run (target: >70%)
- **Defect Escape Rate**: Bugs found after completion (target: <5%)

### Velocity Metrics
- **Cycle Time**: Backlog to Completed (target: <3 days)
- **Throughput**: Tasks completed per week
- **Work in Progress**: Active tasks (limit: 3 per person)

### Process Metrics
- **Blocked Time**: Average time in blocked state (target: <4 hours)
- **Review Time**: Average time in review (target: <2 hours)
- **Test Execution Time**: Average test run duration (target: <30s)

## Conclusion

This kanban task workflow system ensures quality through mandatory test verification at every stage. By following this guide, you'll deliver working, tested code consistently.

Remember: **"No task is complete until tests pass!"** 🎯
