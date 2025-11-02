# Feature Status - View Feature Progress and Epic Integration

Display feature status, task progress, PM tool sync status, and integration with epic-level tracking for comprehensive project visibility.

## Usage
```bash
/feature-status [feature-id] [options]
```

## Examples
```bash
# View all active features
/feature-status

# View specific feature details
/feature-status FEAT-001

# Show features by epic
/feature-status --epic EPIC-001

# Show only features with issues
/feature-status --blocked

# View progress dashboard
/feature-status --dashboard

# Show PM tool sync status
/feature-status --sync-status

# Export feature status report
/feature-status --report stakeholder
```

## Output Formats

### All Features Overview
```
📊 Feature Portfolio Status

🏃 Active Features (5)
┌─────────────┬─────────────────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│ Feature ID  │ Title                   │ Epic        │ Progress    │ Tasks       │ Status      │
├─────────────┼─────────────────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│ FEAT-001    │ User Authentication     │ EPIC-001    │ 60% (3/5)   │ 2 blocked   │ ⚠️ At Risk   │
│ FEAT-002    │ User Profile            │ EPIC-001    │ 100% (4/4)  │ All done    │ ✅ Complete │
│ FEAT-003    │ Payment Gateway         │ EPIC-002    │ 25% (1/4)   │ 1 active    │ 🔄 On Track │
│ FEAT-004    │ Mobile Responsive       │ EPIC-003    │ 0% (0/6)    │ Not started │ ⏳ Planned  │
│ FEAT-005    │ Data Export             │ EPIC-002    │ 75% (3/4)   │ 1 in review │ ✅ On Track │
└─────────────┴─────────────────────────┴─────────────┴─────────────┴─────────────┴─────────────┘

📈 Progress by Epic
EPIC-001 (User Management): 80% complete (2/3 features done)
EPIC-002 (Payment System): 50% complete (1/2 features done)
EPIC-003 (Mobile Platform): 0% complete (0/1 features done)

🚨 Attention Needed
⚠️ FEAT-001: 2 blocked tasks require resolution
🔄 FEAT-003: Behind schedule (25% at week 2 of 4)

🔗 External Tool Health
✅ Jira: 4/5 features synced
⚠️ Linear: 2 features pending sync
✅ GitHub: All features linked
```

### Single Feature Detailed View
```
📋 Feature Details: FEAT-001

🎯 User Authentication System
Epic: EPIC-001 (User Management System)
Priority: High | Timeline: 2 weeks | Status: At Risk ⚠️

📊 Progress Overview
┌─────────────────────────────────────────────────────────────┐
│ ████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│ 60% Complete (3/5 tasks, 12/20 acceptance criteria)        │
└─────────────────────────────────────────────────────────────┘

🎯 Acceptance Criteria Progress
✅ AC-001: User can log in with email/password
✅ AC-002: Invalid credentials show error message
🔄 AC-003: Session expires after 24 hours (in progress)
⏳ AC-004: Password complexity validation (pending)

📋 Task Breakdown
✅ TASK-043: Design authentication UI (completed 2 days ago)
✅ TASK-044: Implement login API endpoint (completed 1 day ago)
🔄 TASK-045: Add session management (Mike - 70% complete)
❌ TASK-046: Password reset flow (blocked - email service issue)
⏳ TASK-047: Authentication tests (pending TASK-046)

⏰ Timeline Analysis
Created: 2024-01-10
Target: 2024-01-24 (2 weeks)
Elapsed: 8 days (57%)
Progress: 60% ✅ Slightly ahead
Projected: On track if blockers resolved

👥 Stakeholders
Product Owner: Sarah Chen
Tech Lead: Mike Johnson
Designer: Lisa Park
QA Engineer: Alex Rodriguez

🔗 External Integration
Jira Story: PROJ-124
  URL: https://company.atlassian.net/browse/PROJ-124
  Status: In Progress
  Last Sync: 30 minutes ago ✅

Linear Feature: PROJECT-457
  URL: https://linear.app/company/feature/PROJECT-457
  Status: In Progress
  Last Sync: 2 hours ago ⚠️

GitHub Issues: #248, #249, #250, #251, #252
  Project: Q1-User-Features
  Milestone: Sprint-3
  Last Sync: 15 minutes ago ✅

📈 Quality Metrics
Code Coverage: 78% (target: 85%)
Test Pass Rate: 95% (19/20 tests)
Performance: Login < 180ms (target: <200ms) ✅
Security Scan: No issues found ✅

🚨 Blockers & Risks
❌ TASK-046: Email service configuration pending
   Impact: Blocks password reset and final testing
   Owner: DevOps team
   ETA: 2 days

⚠️ Risk: Timeline at risk if email service delayed beyond Thursday
   Mitigation: Consider temporary email solution

📊 Requirements Traceability
REQ-001: User login authentication → TASK-043 ✅, TASK-044 ✅
REQ-002: Session security → TASK-045 🔄
REQ-003: Password validation → TASK-046 ❌ (blocked)

🧪 BDD Scenario Status
BDD-001: Successful login flow → 95% implemented
BDD-002: Failed login handling → 100% implemented ✅
BDD-003: Session timeout → 70% implemented

📁 Documentation
Feature File: docs/features/FEAT-001-user-authentication.md
Requirements: REQ-001, REQ-002, REQ-003
Test Reports: tests/reports/feat-001-auth.html
Design Assets: figma.com/auth-components

🔄 Recent Activity
[15 min ago] TASK-045: Session management 70% complete
[2 hours ago] Linear sync delayed (rate limit)
[1 day ago] TASK-044: Login API completed and deployed
[2 days ago] TASK-043: UI design approved and implemented
```

### Epic Feature Dashboard
```bash
/feature-status --epic EPIC-001

📊 Epic Feature Dashboard: EPIC-001

🎯 User Management System
Epic Progress: 67% (2/3 features complete)
Timeline: Q1-2024 | Status: On Track ✅

📋 Feature Breakdown
┌─────────────┬─────────────────────────┬─────────────┬─────────────┬─────────────┐
│ Feature ID  │ Title                   │ Progress    │ Timeline    │ Status      │
├─────────────┼─────────────────────────┼─────────────┼─────────────┼─────────────┤
│ FEAT-001    │ User Authentication     │ 60% (3/5)   │ 2 weeks     │ ⚠️ At Risk   │
│ FEAT-002    │ User Profile            │ 100% (4/4)  │ Completed   │ ✅ Done     │
│ FEAT-003    │ User Permissions        │ 0% (0/4)    │ 3 weeks     │ ⏳ Planned  │
└─────────────┴─────────────────────────┴─────────────┴─────────────┴─────────────┘

📈 Progress Trend
Week 1: 20% → Week 2: 45% → Week 3: 67%
Velocity: 22% per week
Projection: On track for Q1 completion

🎯 Critical Path
1. Complete FEAT-001 (resolve email service blocker)
2. Begin FEAT-003 implementation
3. Final integration testing

🔗 External Tool Rollup
Jira Epic: PROJ-123 (67% complete)
Linear Initiative: PROJECT-456 (67% complete)
Sync Status: All tools current ✅
```

### Workflow Integration Dashboard
```bash
/feature-status --workflow

🔄 Workflow Integration Status

📋 Task Definition (Feature Level)
┌─────────────┬─────────────────────────┬─────────────┬─────────────┬──────────────┐
│ Feature ID  │ Title                   │ Tasks Gen   │ PM Export   │ Ready Status │
├─────────────┼─────────────────────────┼─────────────┼─────────────┼──────────────┤
│ FEAT-001    │ User Authentication     │ ✅ Complete │ ✅ Synced   │ 🔄 In Prog   │
│ FEAT-002    │ User Profile            │ ✅ Complete │ ✅ Synced   │ ✅ Complete  │
│ FEAT-003    │ User Permissions        │ ✅ Complete │ ⏳ Pending  │ ⏳ Waiting    │
└─────────────┴─────────────────────────┴─────────────┴─────────────┴──────────────┘

🎯 Human Checkpoints Status
✅ Feature specifications reviewed and approved
✅ Task definitions reviewed and approved
🔄 Execution in progress (FEAT-001)
⏳ Pending PM tool export (FEAT-003)

📈 Workflow Health
Task Definition → Execution Transition: 67% complete
AI/Human Task Assignment: Mixed mode active
External Tool Integration: Healthy ✅

🔄 MCP Integration Status
✅ Requirements MCP: Active and synced
✅ PM Tools MCP: Connected (Jira, Linear, GitHub)
⚠️ Execution MCP: Pending configuration (taskwright)
⏳ Validation MCP: Ready for completion
```

## Options

### Filtering Options
```bash
# View by status
/feature-status --status active
/feature-status --status completed
/feature-status --status blocked

# View by priority
/feature-status --priority critical
/feature-status --priority high

# View by timeline
/feature-status --overdue
/feature-status --current-sprint

# View by PM tool
/feature-status --tool jira
/feature-status --sync-issues
```

### Display Options
```bash
# Detailed view
/feature-status FEAT-001 --detailed

# Progress focus
/feature-status --progress-only

# Task breakdown
/feature-status FEAT-001 --tasks

# Stakeholder view
/feature-status --stakeholder-view

# Compact view
/feature-status --compact
```

### Export Options
```bash
# Export status to file
/feature-status --export csv
/feature-status --export json

# Generate status reports
/feature-status --report weekly
/feature-status --report stakeholder
/feature-status --report technical
```

## Integration Features

### Real-time Progress Tracking
- **Green ✅**: Feature on track, no blockers
- **Yellow ⚠️**: At risk, attention needed
- **Red ❌**: Blocked or significantly delayed
- **Blue 🔄**: In progress, normal velocity

### Epic Progress Rollup
Feature progress automatically contributes to epic calculations:
```
Epic Progress = (Σ Feature Progress × Feature Weight) / Total Features
Feature Progress = (Completed Tasks / Total Tasks) × 100
Task Weighting = Based on complexity and acceptance criteria count
```

### PM Tool Sync Status
- **Bidirectional Sync**: Changes flow between local and external tools
- **Conflict Detection**: Identifies and highlights sync conflicts
- **Health Monitoring**: Tracks API connectivity and sync frequency
- **Automatic Recovery**: Retries failed syncs with backoff strategy

### Requirements Management Workflow Integration
Features provide critical metrics for task definition → execution transition:
- **Task Definition Completeness**: All tasks generated and approved
- **Human Checkpoint Status**: Approvals and review states
- **PM Tool Readiness**: External integrations configured
- **Execution Readiness**: Prerequisites satisfied for task execution (taskwright)

## Command Variations

### Quick Status Check
```bash
/feature-status --quick
# Shows one-line status for each active feature
```

### Management Dashboard
```bash
/feature-status --dashboard
# Full portfolio view with trends and health indicators
```

### Developer View
```bash
/feature-status --dev-view
# Technical details: coverage, performance, test status
```

### Stakeholder Report
```bash
/feature-status --stakeholder-view
# Business-focused view with progress and timeline info
```

## Integration with Other Commands

### Cross-Command Navigation
```bash
# From feature status to task breakdown
/feature-status FEAT-001 → shows "Run: /task-status feature:FEAT-001"

# From feature status to epic overview
/feature-status FEAT-001 → shows "Run: /epic-status EPIC-001"

# Sync management
/feature-status FEAT-001 → shows "Run: /feature-sync FEAT-001"
```

### Workflow Integration
```bash
# Status check before adding tasks
/feature-status FEAT-001 --brief
/task-create "New Task" feature:FEAT-001

# Progress check before feature completion
/feature-status FEAT-001 --completion-check
/feature-complete FEAT-001
```

## Performance Metrics

### Quality Gates Integration
Features automatically track quality metrics:
- **Test Coverage**: Target vs actual coverage
- **Performance**: Response time benchmarks
- **Security**: Vulnerability scan results
- **Code Quality**: Static analysis scores

### Trend Analysis
```
📈 Feature Velocity Trends
Current Sprint: 1.5 features/week (target: 2.0)
Last Sprint: 2.2 features/week
Rolling Average: 1.8 features/week
Trend: Slightly below target ⚠️
```

## Best Practices

1. **Regular Monitoring**: Check feature status daily during active development
2. **Blocker Resolution**: Address blocked tasks immediately to prevent cascade delays
3. **Sync Health**: Monitor PM tool sync status to maintain data consistency
4. **Stakeholder Communication**: Use stakeholder view for business updates
5. **Epic Alignment**: Ensure feature progress supports epic objectives
6. **Quality Focus**: Monitor coverage and performance metrics continuously

This command provides comprehensive feature tracking while maintaining seamless integration with the task definition workflow and external PM tool ecosystem. For task execution, see taskwright.