# Update State Command

Update project state tracking including progress, test results, and sprint metrics.

## Command
```
/update-state [component] [status]
```

## Components to Update

```bash
# Task status
/update-state task TASK-001 complete
/update-state task TASK-002 in-progress
/update-state task TASK-003 blocked

# Feature progress
/update-state feature FEAT-001 75%

# Epic status
/update-state epic EPIC-001 complete

# Sprint metrics
/update-state sprint velocity 19/21

# Test results
/update-state tests passed
```

## State Files Updated

### Current Sprint (`docs/state/current-sprint.md`)
```markdown
---
sprint: 3
start: 2024-01-15
end: 2024-01-29
velocity: 21
---

# Sprint 3 Progress

## Overview
- **Sprint Goal**: Implement authentication system
- **Progress**: 75% [███████▌  ]
- **Velocity**: 16/21 points
- **Days Remaining**: 5

## Epic: User Management [85% Complete]

### Feature: Authentication [✅ Complete]
#### Tasks
- [x] TASK-001: Design login form
  - Status: ✅ Complete
  - EARS: REQ-001, REQ-002
  - BDD: 5/5 scenarios passing
  - Tests: 100% coverage
  - Completed: 2024-01-18

- [x] TASK-002: Implement JWT tokens
  - Status: ✅ Complete
  - EARS: REQ-003
  - Tests: 15/15 passing
  - Completed: 2024-01-19
```

### Product Backlog (`docs/state/product-backlog.md`)
```markdown
# Product Backlog

## Ready for Development
| ID | Title | Points | Priority | Dependencies |
|----|-------|--------|----------|--------------|
| TASK-010 | Payment integration | 8 | High | TASK-009 |
| TASK-011 | Email notifications | 5 | Medium | None |
| TASK-012 | Dashboard analytics | 13 | Low | TASK-010 |

## In Progress
| ID | Title | Assignee | Progress |
|----|-------|----------|----------|
| TASK-008 | User profiles | @dev1 | 60% |
| TASK-009 | API gateway | @dev2 | 30% |

## Completed This Sprint
| ID | Title | Points | Completed |
|----|-------|--------|-----------|
| TASK-001 | Login form | 3 | 2024-01-18 |
| TASK-002 | JWT tokens | 5 | 2024-01-19 |
```

### Changelog (`docs/state/changelog.md`)
```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- User authentication with JWT tokens (TASK-001, TASK-002)
- Session management (TASK-003)
- Password reset functionality (TASK-004)

### Changed
- Updated login UI for better UX
- Improved error messages

### Fixed
- Race condition in token refresh
- Memory leak in session storage

## [2024-01-19]

### Task Completions
- ✅ TASK-001: Login form implementation
  - EARS: REQ-001, REQ-002 implemented
  - BDD: 5 scenarios, 100% passing
  - Coverage: 95% lines, 90% branches
  - Review: Approved by @reviewer

- ✅ TASK-002: JWT token implementation
  - EARS: REQ-003 implemented
  - Tests: 15 unit, 5 integration
  - Performance: <50ms token generation
```

## Progress Visualization

### Sprint Burndown
```
Points Remaining
21 |█
19 |██
17 |███
15 |████
13 |█████
11 |██████
 9 |████████
 7 |██████████
 5 |████████████
 3 |███████████████
 1 |████████████████████
   |1 2 3 4 5 6 7 8 9 10 (Days)
```

### Velocity Trend
```
Sprint Velocity
25 |        ██
20 |    ██  ██  ██
15 |██  ██  ██  ██
10 |██  ██  ██  ██
 5 |██  ██  ██  ██
 0 |S1  S2  S3  S4
    21  19  16  ? (points)
```

## Quality Metrics Update

### Test Coverage Trend
```yaml
coverage_history:
  - date: 2024-01-15
    unit: 75%
    integration: 65%
    e2e: 80%
    
  - date: 2024-01-18
    unit: 82%
    integration: 71%
    e2e: 85%
    
  - date: 2024-01-19
    unit: 85%
    integration: 73%
    e2e: 87%
```

### Defect Tracking
```yaml
defects:
  found_in_dev: 12
  found_in_review: 5
  found_in_production: 1
  
  by_severity:
    critical: 1
    major: 4
    minor: 13
    
  resolution_time:
    average: 4.5 hours
    p95: 12 hours
```

## Automated Updates

### From Test Results
```bash
# After test execution
/execute-tests
# Automatically updates:
# - Test coverage metrics
# - Pass/fail counts
# - Performance benchmarks
```

### From Git Commits
```bash
# On commit with pattern
git commit -m "feat(TASK-001): complete login form"
# Automatically updates:
# - Task status
# - Changelog
# - Sprint progress
```

### From PR Merge
```bash
# On PR merge
# Automatically updates:
# - Feature completion
# - Test results
# - Documentation status
```

## State Synchronization

### With GitHub
```yaml
sync:
  issues:
    - status changes
    - label updates
    - milestone progress
    
  pull_requests:
    - review status
    - merge status
    - check results
```

### With Linear/Jira
```yaml
sync:
  tasks:
    - status updates
    - point changes
    - assignee changes
    
  epics:
    - progress percentage
    - child task rollup
```

## Manual Update Examples

### Complete a Task
```bash
/update-state task TASK-001 complete

✅ Task TASK-001 marked complete
📊 Feature progress: 75% → 85%
📈 Sprint velocity: 14/21 → 17/21
📝 Changelog updated
```

### Block a Task
```bash
/update-state task TASK-005 blocked "Waiting for API specs"

⚠️ Task TASK-005 blocked
📝 Reason: Waiting for API specs
📊 Sprint risk increased
🔔 Team notified
```

### Update Test Results
```bash
/update-state tests unit:passed:156/156 coverage:87%

✅ Unit tests: 156/156 passed
📊 Coverage: 87% (↑ 2%)
✅ Quality gate: PASSED
📝 Metrics updated
```

## Sprint Ceremonies

### Daily Standup Update
```bash
/update-state daily
# Generates:
# - Tasks in progress
# - Blockers
# - Today's plan
```

### Sprint Review
```bash
/update-state sprint-review
# Generates:
# - Completed features
# - Demo items
# - Metrics summary
```

### Retrospective Data
```bash
/update-state retro
# Collects:
# - Velocity achieved
# - Quality metrics
# - Team feedback
```

## Notifications

Updates trigger notifications for:
- Task completion
- Blocking issues
- Gate failures
- Milestone achievement

## Best Practices

1. **Update immediately** - Don't batch updates
2. **Include context** - Add reasons for blocks/failures
3. **Verify accuracy** - Double-check before updating
4. **Link evidence** - Reference test results, PRs
5. **Communicate changes** - Notify affected team members

Ready to keep your project state current and transparent!
