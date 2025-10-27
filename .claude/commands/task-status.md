# Task Status Dashboard

View the current task board with all tasks organized by status.

## Usage
```bash
/task-status [filter:all|mine|today|week] [format:board|list|metrics]
```

## Examples
```bash
/task-status                    # Default kanban board view
/task-status filter:mine        # Only tasks assigned to you
/task-status format:metrics     # Show metrics dashboard
/task-status filter:week        # Tasks updated this week
```

## Display Formats

### 1. Kanban Board View (Default)
```
╔════════════════════════════════════════════════════════════════╗
║                    TASK BOARD - 2024-01-15                     ║
╚════════════════════════════════════════════════════════════════╝

┌─────────────────┬─────────────────┬─────────────────┐
│   BACKLOG (5)   │ IN_PROGRESS (2) │ IN_TESTING (1)  │
├─────────────────┼─────────────────┼─────────────────┤
│ TASK-043 [HIGH] │ TASK-041 [MED]  │ TASK-040 [HIGH] │
│ Add search      │ Refactor auth   │ Payment API     │
│ Tags: ui, api   │ @alice          │ ⏳ Running...   │
│                 │ 🕐 2 days       │                 │
├─────────────────┼─────────────────┼─────────────────┤
│ TASK-044 [LOW]  │ TASK-042 [HIGH] │                 │
│ Export feature  │ User profile    │                 │
│ Tags: backend   │ @bob            │                 │
│                 │ 🕐 4 hours      │                 │
├─────────────────┼─────────────────┼─────────────────┤
│ TASK-045 [MED]  │                 │                 │
│ Admin dashboard │                 │                 │
│ Tags: ui, admin │                 │                 │
└─────────────────┴─────────────────┴─────────────────┘

┌─────────────────┬─────────────────┬─────────────────┐
│  IN_REVIEW (1)  │   BLOCKED (1)   │ COMPLETED (3)   │
├─────────────────┼─────────────────┼─────────────────┤
│ TASK-039 [HIGH] │ TASK-038 [HIGH] │ ✅ TASK-037     │
│ Email service   │ Social login    │ ✅ TASK-036     │
│ ✅ 25/25 tests  │ ❌ 3 failures   │ ✅ TASK-035     │
│ 📊 92% coverage │ OAuth callback  │ Today: 3        │
└─────────────────┴─────────────────┴─────────────────┘

📊 METRICS: Velocity: 3/day | Coverage Avg: 86% | Blocked: 1
```

### 2. List View
```
TASK LIST - 2024-01-15
=======================

BACKLOG (5 tasks)
-----------------
• TASK-043 [HIGH] - Add search functionality
  Created: 2024-01-10 | Tags: ui, api
  
• TASK-044 [LOW] - Export feature
  Created: 2024-01-11 | Tags: backend
  
• TASK-045 [MED] - Admin dashboard
  Created: 2024-01-12 | Tags: ui, admin

IN_PROGRESS (2 tasks) 
---------------------
• TASK-041 [MED] - Refactor auth service
  Assignee: alice | Started: 2024-01-13 (2 days ago)
  Progress: 60% | Tests: 0/15 written
  
• TASK-042 [HIGH] - Add user profile page
  Assignee: bob | Started: 2024-01-15 (4 hours ago)
  Progress: 30% | Tests: 5/20 written

IN_TESTING (1 task)
-------------------
• TASK-040 [HIGH] - Payment integration
  Status: Tests running...
  Last run: 2024-01-15 14:30:00
  Current: 18/20 passing

IN_REVIEW (1 task)
------------------
• TASK-039 [HIGH] - Email notifications
  Reviewer: carol | Tests: ✅ 25/25 passing
  Coverage: 92% | Ready for completion

BLOCKED (1 task)
----------------
• TASK-038 [HIGH] - Social login
  Blocked since: 2024-01-14
  Reason: OAuth callback failing (3 tests)
  Action needed: Fix authentication flow

COMPLETED TODAY (3 tasks)
--------------------------
✅ TASK-037 - Password reset (87% coverage)
✅ TASK-036 - User preferences (91% coverage)
✅ TASK-035 - Activity logging (83% coverage)
```

### 3. Metrics Dashboard
```
╔════════════════════════════════════════════════════════════════╗
║                    METRICS DASHBOARD                           ║
╚════════════════════════════════════════════════════════════════╝

📈 VELOCITY METRICS
├─ Daily Average: 2.5 tasks
├─ Weekly Total: 17 tasks
├─ Sprint Progress: 65% (13/20 tasks)
└─ Estimated Completion: 3 days

📊 QUALITY METRICS
├─ Average Coverage: 86.3%
├─ Test Pass Rate: 94%
├─ First-Time Pass: 78%
├─ Average Review Time: 4.2 hours
└─ Defect Escape Rate: 2%

⏱️ CYCLE TIME ANALYSIS
├─ Backlog → Started: 2.1 days avg
├─ Started → Testing: 1.3 days avg
├─ Testing → Review: 0.5 days avg
├─ Review → Complete: 0.3 days avg
└─ Total Cycle Time: 4.2 days avg

🚫 BOTTLENECKS
├─ Testing Queue: 3 tasks waiting
├─ Review Queue: 1 task waiting
├─ Blocked Tasks: 1 (12 hours)
└─ Resource Utilization: 85%

📉 RISK INDICATORS
├─ Tasks at Risk: 2
│  ├─ TASK-041: Behind schedule
│  └─ TASK-038: Blocked >24h
├─ Coverage Declining: -3% this week
└─ Test Failures Increasing: +15%

🎯 SPRINT GOALS
├─ Target: 20 tasks
├─ Completed: 13 (65%)
├─ In Progress: 4 (20%)
├─ At Risk: 2 (10%)
└─ Not Started: 1 (5%)

📊 DISTRIBUTION BY PRIORITY
├─ CRITICAL: ████░░░░░░ 40% (2/5)
├─ HIGH:     ███████░░░ 70% (7/10)
├─ MEDIUM:   █████░░░░░ 50% (3/6)
└─ LOW:      ██░░░░░░░░ 20% (1/5)

👥 TEAM PERFORMANCE
├─ alice: 4 completed, 1 in progress
├─ bob: 3 completed, 1 in progress
├─ carol: 2 completed, 1 reviewing
└─ Unassigned: 5 in backlog
```

## Filtering Options

### By Assignee
```bash
/task-status filter:assignee:alice
```
Shows only tasks assigned to alice.

### By Time Period
```bash
/task-status filter:today      # Updated today
/task-status filter:week       # Updated this week
/task-status filter:sprint     # Current sprint
/task-status filter:month      # This month
```

### By Priority
```bash
/task-status filter:priority:high
/task-status filter:priority:critical
```

### By Status
```bash
/task-status filter:status:blocked
/task-status filter:status:in_testing
```

### By Tags
```bash
/task-status filter:tag:backend
/task-status filter:tag:security
```

### Combined Filters
```bash
/task-status filter:mine,priority:high,status:in_progress
```

## Status Indicators

### Task State Icons
- 📋 BACKLOG - Not started
- 🔄 IN_PROGRESS - Active work
- 🧪 IN_TESTING - Tests running
- 👀 IN_REVIEW - Awaiting approval
- ❌ BLOCKED - Cannot proceed
- ✅ COMPLETED - Done

### Priority Indicators
- 🔴 CRITICAL - Drop everything
- 🟠 HIGH - Important
- 🟡 MEDIUM - Normal
- 🟢 LOW - Nice to have

### Test Status
- ✅ All passing
- ⚠️ Some failures
- ❌ All failing
- ⏳ Running
- ⭕ Not started

### Time Indicators
- 🕐 Time in current state
- ⏰ Overdue
- 📅 Scheduled
- 🎯 On track

## Quick Actions

From the status view, you can:
```
[1] Start TASK-043
[2] Test TASK-040
[3] Complete TASK-039
[4] Unblock TASK-038
[5] Refresh view
[Q] Quit

Select action: _
```

## Report Generation

### Daily Standup Report
```bash
/task-status report:standup
```
Generates:
- Yesterday's completions
- Today's in progress
- Current blockers

### Sprint Report
```bash
/task-status report:sprint
```
Generates:
- Sprint progress
- Velocity trends
- Risk assessment
- Recommendations

### Weekly Summary
```bash
/task-status report:weekly
```
Generates:
- Tasks completed
- Coverage trends
- Team performance
- Lessons learned

## Export Options

### CSV Export
```bash
/task-status export:csv > tasks.csv
```

### JSON Export
```bash
/task-status export:json > tasks.json
```

### Markdown Report
```bash
/task-status export:markdown > status.md
```

## Configuration

### Customize Display
```yaml
# .claude/task-status.config.yaml
display:
  max_tasks_per_column: 5
  show_descriptions: true
  show_assignees: true
  show_time_in_state: true
  
colors:
  critical: red
  high: orange
  medium: yellow
  low: green
  
metrics:
  velocity_period: week
  coverage_threshold: 80
  cycle_time_target: 3
```

## Integration

### Slack Integration
Post status to Slack:
```bash
/task-status notify:slack:#team-channel
```

### Email Report
Send status via email:
```bash
/task-status notify:email:team@company.com
```

### Dashboard URL
Generate shareable link:
```bash
/task-status share:generate
# Output: https://tasks.company.com/board/abc123
```

## Best Practices

1. **Check status at start of day** - Understand priorities
2. **Update throughout day** - Keep team informed
3. **Review blocked tasks** - Unblock quickly
4. **Monitor cycle time** - Identify bottlenecks
5. **Track velocity** - Improve estimates
6. **Celebrate completions** - Recognize achievements
