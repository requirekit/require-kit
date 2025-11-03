# Epic Status - View Epic Progress and PM Tool Sync Status

Display epic status, progress, and synchronization status with external project management tools.

## Usage
```bash
/epic-status [epic-id] [options]
```

## Examples
```bash
# View all active epics
/epic-status

# View specific epic details
/epic-status EPIC-001

# Show only epics with sync issues
/epic-status --sync-issues

# View epics by quarter
/epic-status --quarter Q1-2024

# Show progress with external tool links
/epic-status EPIC-001 --detailed

# Show feature breakdown
/epic-status EPIC-001 --features

# Show both features and tasks
/epic-status EPIC-001 --hierarchy
```

## Output Formats

### All Epics Overview
```
📊 Epic Portfolio Status

🏃 Active Epics (3)
┌─────────────┬──────────────────────┬──────────┬─────────────┬──────────────┬─────────────┐
│ Epic ID     │ Title                │ Priority │ Progress    │ Features     │ External     │ Sync Status │
├─────────────┼──────────────────────┼──────────┼─────────────┼─────────────┼──────────────┼─────────────┤
│ EPIC-001    │ User Management      │ High     │ 67% (2/3)   │ 3 features  │ Jira, Linear│ ✅ Synced   │
│ EPIC-002    │ Payment System       │ Critical │ 25% (1/4)   │ 2 features  │ Linear       │ ⚠️  Pending  │
│ EPIC-003    │ Mobile Redesign      │ Normal   │ 0% (0/3)    │ 3 features  │ GitHub       │ ❌ Failed   │
└─────────────┴──────────────────────┴──────────┴─────────────┴──────────────┴─────────────┘

📅 By Quarter
Q1-2024: 2 epics (1 on track, 1 at risk)
Q2-2024: 1 epic (planning phase)

🔗 External Tool Summary
✅ Jira: 1 epic synced
⚠️ Linear: 2 epics (1 sync pending)
❌ GitHub: 1 epic (sync failed)

📈 Overall Progress: 19% (4/22 features complete)
```

### Single Epic Detailed View
```
📋 Epic Details: EPIC-001

🎯 User Management System
Priority: High | Quarter: Q1-2024 | Status: In Progress

📊 Progress Overview
┌─────────────────────────────────────────────────────────────┐
│ ████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░  │
│ 67% Complete (2/3 features, 7/10 tasks)                    │
└─────────────────────────────────────────────────────────────┘

🎯 Success Criteria
✅ User registration flow completed
✅ Basic authentication implemented
🔄 Role-based permissions (in progress)
⏳ User profile management (pending)
⏳ Account recovery system (pending)

⏰ Timeline
Created: 2024-01-15
Target: Q1-2024 (8 weeks)
Remaining: 4.2 weeks
Status: On Track ✅

👥 Stakeholders
Product Owner: Sarah Chen
Engineering Lead: Mike Johnson
Design Lead: Lisa Park

🔗 External Integration
Jira Epic: PROJ-123
  URL: https://company.atlassian.net/browse/PROJ-123
  Last Sync: 2 hours ago ✅
  Status: In Progress

Linear Initiative: PROJECT-456
  URL: https://linear.app/company/initiative/PROJECT-456
  Last Sync: 5 minutes ago ✅
  Status: In Progress

📋 Feature Breakdown
✅ FEAT-001: User Registration (100% - 4/4 tasks)
✅ FEAT-002: Basic Authentication (100% - 3/3 tasks)
🔄 FEAT-003: Role Management (60% - 3/5 tasks)

💡 Feature Details
View feature details: /feature-status FEAT-001
Sync feature progress: /feature-sync FEAT-003
Create new feature: /feature-create "Feature Name" epic:EPIC-001

🎯 Current Sprint Focus
▶️ TASK-042: Implement role assignment UI (Mike - In Progress)
▶️ TASK-043: Add permission validation (Lisa - In Review)
⏳ TASK-044: Role inheritance logic (Backlog)

📈 Burndown Trend
Week 1: 0% → Week 2: 15% → Week 3: 30% → Week 4: 45%
Velocity: 15% per week (on track for Q1 completion)

🚨 Risks & Blockers
None currently identified ✅

📁 Documentation
Epic File: docs/epics/EPIC-001-user-management.md
Features: 3 features (2 complete, 1 in progress)
Requirements: REQ-001, REQ-002, REQ-003
BDD Scenarios: 15 scenarios (12 passing, 3 pending)
```

### Epic Hierarchy View
```bash
/epic-status EPIC-001 --hierarchy

📊 Epic Hierarchy: EPIC-001 - User Management System

📋 Complete Epic → Feature → Task Structure
EPIC-001: User Management System (67% complete)
├── FEAT-001: User Registration (100% ✅)
│   ├── TASK-001: Design registration form (✅ Complete)
│   ├── TASK-002: Implement registration API (✅ Complete)
│   ├── TASK-003: Add email verification (✅ Complete)
│   └── TASK-004: Create registration tests (✅ Complete)
├── FEAT-002: Basic Authentication (100% ✅)
│   ├── TASK-005: Design login UI (✅ Complete)
│   ├── TASK-006: Implement auth API (✅ Complete)
│   └── TASK-007: Add session management (✅ Complete)
└── FEAT-003: Role Management (60% 🔄)
    ├── TASK-008: Design role UI (✅ Complete)
    ├── TASK-009: Implement RBAC logic (✅ Complete)
    ├── TASK-010: Add permission validation (🔄 In Progress - Lisa)
    ├── TASK-011: Role inheritance logic (⏳ Pending)
    └── TASK-012: Role management tests (⏳ Pending)

🔗 External Tool Hierarchy
Jira Epic PROJ-123
├── Story PROJ-124 (FEAT-001) ✅
├── Story PROJ-125 (FEAT-002) ✅
└── Story PROJ-126 (FEAT-003) 🔄
    ├── Sub-task PROJ-127 (TASK-008) ✅
    ├── Sub-task PROJ-128 (TASK-009) ✅
    ├── Sub-task PROJ-129 (TASK-010) 🔄
    ├── Sub-task PROJ-130 (TASK-011) ⏳
    └── Sub-task PROJ-131 (TASK-012) ⏳

📊 Progress Rollup Calculation
Feature Progress = (Completed Tasks / Total Tasks) × 100
Epic Progress = (Σ Feature Progress × Feature Weight) / Total Features
Current: (100% + 100% + 60%) / 3 = 87% → Weighted: 67%

💡 Quick Actions
Create feature: /feature-create "Feature Name" epic:EPIC-001
View feature: /feature-status FEAT-003
# Task execution: Use your workflow or integrate with taskwright
Sync hierarchy: /epic-sync EPIC-001 --include-features
```

### Sync Issues View
```
🔄 Epic Sync Status Report

❌ Sync Issues (2)
┌─────────────┬──────────────────────┬─────────────┬─────────────────────────┐
│ Epic ID     │ Title                │ Tool        │ Issue                   │
├─────────────┼──────────────────────┼─────────────┼─────────────────────────┤
│ EPIC-002    │ Payment System       │ Linear      │ Rate limit exceeded     │
│ EPIC-003    │ Mobile Redesign      │ GitHub      │ Invalid project token   │
└─────────────┴──────────────────────┴─────────────┴─────────────────────────┘

⚠️ Sync Warnings (1)
EPIC-001: Jira sync delayed (last: 4 hours ago)

🔧 Recommended Actions
1. EPIC-002: Retry Linear sync in 15 minutes
2. EPIC-003: Update GitHub token: /pm-config github --refresh-token
3. EPIC-001: Force Jira sync: /epic-sync EPIC-001 --force

📊 Sync Health: 67% (2/3 tools healthy)
```

### Progress Dashboard
```
📈 Epic Progress Dashboard

🎯 Portfolio Health
Overall Progress: 34% (38/112 total tasks, 15/45 features)
On Track: 5 epics ✅
At Risk: 2 epics ⚠️
Blocked: 1 epic ❌

📅 Quarterly View
Q1-2024 Progress: ████████░░░░░░░░░░░░ 40% (2/5 epics complete)
Q2-2024 Planning: ███░░░░░░░░░░░░░░░░░ 15% (requirements gathering)

🏆 Recent Completions
✅ EPIC-007: API Documentation (completed 2 days ago)
✅ EPIC-005: Security Audit (completed 1 week ago)

⚡ Velocity Trends
This Quarter: 2.1 epics/month (target: 2.5)
Last Quarter: 2.8 epics/month
Trend: Slightly below target ⚠️

🔄 External Tool Health
Jira: ✅ Healthy (last sync: 1 min ago)
Linear: ⚠️ Rate limited (last sync: 2 hours ago)
GitHub: ❌ Token expired (last sync: 2 days ago)
Azure DevOps: Not configured
```

## Options

### Filtering Options
```bash
# View by status
/epic-status --status active
/epic-status --status completed
/epic-status --status cancelled

# View by priority
/epic-status --priority critical
/epic-status --priority high

# View by quarter/timeline
/epic-status --quarter Q1-2024
/epic-status --overdue

# View by external tool
/epic-status --tool jira
/epic-status --tool linear
/epic-status --sync-issues
```

### Display Options
```bash
# Detailed view
/epic-status EPIC-001 --detailed

# Progress focus
/epic-status --progress-only

# External links focus
/epic-status --external-only

# Compact view
/epic-status --compact

# Feature breakdown view
/epic-status EPIC-001 --features

# Complete hierarchy view
/epic-status EPIC-001 --hierarchy

# Feature and task details
/epic-status EPIC-001 --detailed --features
```

### Export Options
```bash
# Export status to file
/epic-status --export csv
/epic-status --export json

# Generate status report
/epic-status --report weekly
/epic-status --report stakeholder
```

## Integration Features

### Real-time Sync Status
- **Green ✅**: Synced within last hour
- **Yellow ⚠️**: Sync delayed (1-24 hours)
- **Red ❌**: Sync failed or >24 hours old

### External Tool Deep Links
- Direct links to epic in external tools
- One-click navigation to related items
- Status synchronization indicators

### Progress Calculation
```
Epic Progress = (Completed Features / Total Features) × 100
Feature Progress = (Completed Tasks / Total Tasks) × 100
Rollup Progress = Weighted average based on feature complexity
```

### Smart Notifications
```bash
# Epic approaching deadline
⚠️ EPIC-001 target date in 3 days (currently 45% complete)

# Sync issues detected
❌ EPIC-002 Linear sync failed (retry recommended)

# Progress milestones
🎉 EPIC-003 reached 50% completion milestone
```

## Command Variations

### Quick Status Check
```bash
/epic-status --quick
# Shows one-line status for each active epic
```

### Management Dashboard
```bash
/epic-status --dashboard
# Full portfolio view with trends and health indicators
```

### Stakeholder Report
```bash
/epic-status --stakeholder-view
# Business-focused view with less technical detail
```

## Integration with Other Commands

### Cross-Command Navigation
```bash
# From epic status to feature breakdown
/epic-status EPIC-001 → shows "Run: /feature-status EPIC-001"

# From epic status to task details
/epic-status EPIC-001 → shows "Run: /task-status feature:FEAT-003"

# Sync management
/epic-status EPIC-001 → shows "Run: /epic-sync EPIC-001"
```

### Workflow Integration
```bash
# Status check before creating features
/epic-status EPIC-001 --brief
/feature-create "New Feature" epic:EPIC-001

# Progress check before marking epic complete
/epic-status EPIC-001 --completion-check
/epic-complete EPIC-001
```

## Best Practices

1. **Regular Status Checks**: Run `/epic-status` weekly for portfolio health
2. **Monitor Sync Health**: Check sync status daily if using external tools
3. **Track Progress Trends**: Use progress dashboard for velocity insights
4. **Address Sync Issues**: Fix sync problems immediately to maintain data consistency
5. **Stakeholder Communication**: Use stakeholder view for business updates

This command provides comprehensive epic tracking while maintaining focus on **external tool integration** and **minimal local state management**.