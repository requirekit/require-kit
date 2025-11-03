# Hierarchy View - Visual Project Structure and Progress

Comprehensive visualization of the Epic → Feature → Task hierarchy with progress tracking, dependency mapping, and integration with external tools.

## Usage
```bash
/hierarchy-view [scope] [options]
```

## Examples
```bash
# View complete project hierarchy
/hierarchy-view

# View specific epic hierarchy
/hierarchy-view EPIC-001

# View feature breakdown
/hierarchy-view FEAT-003

# Portfolio overview with all epics
/hierarchy-view --portfolio

# Progress timeline view
/hierarchy-view --timeline

# Dependency mapping
/hierarchy-view --dependencies

# Workflow status
/hierarchy-view --workflow

# External tool integration view
/hierarchy-view --external-tools
```

## Visualization Formats

### Complete Hierarchy View (Default)
```
📊 Project Hierarchy Overview

🏗️ Epic → Feature → Task Structure
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          PROJECT PORTFOLIO (67% Complete)                      │
└─────────────────────────────────────────────────────────────────────────────────┘

📈 EPIC-001: User Management System (78% Complete) ✅ On Track
├── 🎯 FEAT-001: User Registration (100% Complete) ✅
│   ├── ✅ TASK-001: Design registration form (Sarah, 2 days)
│   ├── ✅ TASK-002: Implement registration API (Mike, 3 days)
│   ├── ✅ TASK-003: Add email verification (Alex, 1 day)
│   └── ✅ TASK-004: Create registration tests (Lisa, 1 day)
│
├── 🎯 FEAT-002: User Authentication (90% Complete) 🔄
│   ├── ✅ TASK-005: Design login UI (Lisa, 1 day)
│   ├── ✅ TASK-006: Implement auth API (Mike, 2 days)
│   ├── ✅ TASK-007: Add session management (Sarah, 3 days)
│   ├── ✅ TASK-008: Password reset flow (Alex, 2 days)
│   └── 🔄 TASK-009: Authentication tests (Mike, 1 day) - 80% complete
│
└── 🎯 FEAT-003: User Permissions (45% Complete) 🔄
    ├── ✅ TASK-010: Design permission model (Sarah, 2 days)
    ├── 🔄 TASK-011: Implement RBAC system (Mike, 4 days) - 60% complete
    ├── ⏳ TASK-012: Permission UI components (Lisa, 2 days)
    ├── ⏳ TASK-013: Admin dashboard (Alex, 3 days)
    └── ⏳ TASK-014: Permission tests (Mike, 2 days)

📈 EPIC-002: Payment System (34% Complete) ⚠️ At Risk
├── 🎯 FEAT-004: Payment Gateway (60% Complete) 🔄
│   ├── ✅ TASK-015: Payment provider integration (Sarah, 4 days)
│   ├── ✅ TASK-016: Payment API design (Mike, 2 days)
│   ├── 🔄 TASK-017: Payment processing logic (Alex, 3 days) - 70% complete
│   └── ⏳ TASK-018: Payment error handling (Lisa, 2 days)
│
└── 🎯 FEAT-005: Billing Management (8% Complete) ⏳
    ├── 🔄 TASK-019: Billing data model (Sarah, 2 days) - 40% complete
    ├── ⏳ TASK-020: Invoice generation (Mike, 3 days)
    ├── ⏳ TASK-021: Payment history UI (Lisa, 2 days)
    └── ⏳ TASK-022: Billing reports (Alex, 2 days)

📈 EPIC-003: Mobile Platform (15% Complete) ⏳ Planning
└── 🎯 FEAT-006: Mobile App Foundation (15% Complete) ⏳
    ├── 🔄 TASK-023: Mobile architecture design (Mike, 3 days) - 60% complete
    ├── ⏳ TASK-024: React Native setup (Sarah, 2 days)
    ├── ⏳ TASK-025: Mobile UI framework (Lisa, 4 days)
    └── ⏳ TASK-026: Mobile testing strategy (Alex, 2 days)

🔗 External Tool Integration
┌─────────────┬──────────────┬────────────────┬─────────────────┐
│ Epic        │ Jira         │ Linear         │ GitHub          │
├─────────────┼──────────────┼────────────────┼─────────────────┤
│ EPIC-001    │ PROJ-123 ✅  │ PROJECT-456 ✅ │ Milestone-1 ✅  │
│ EPIC-002    │ PROJ-124 ⚠️  │ PROJECT-457 ✅ │ Milestone-2 ✅  │
│ EPIC-003    │ PROJ-125 ✅  │ PROJECT-458 ⏳ │ Milestone-3 ⏳  │
└─────────────┴──────────────┴────────────────┴─────────────────┘

📊 Portfolio Summary
Total Epics: 3 (1 on track, 1 at risk, 1 planning)
Total Features: 6 (2 complete, 3 in progress, 1 planning)
Total Tasks: 26 (12 complete, 6 in progress, 8 planned)
Overall Progress: 67% (17.4/26 tasks weighted)
Target Completion: Q1 2024 (on track)

💡 Quick Actions
├── View epic details: /epic-status EPIC-002
├── Task execution: Use your workflow or taskwright integration
├── Sync all external tools: /epic-sync --all
└── Generate progress report: /hierarchy-view --report
```

### Progress Timeline View
```bash
/hierarchy-view --timeline

📅 Project Timeline & Progress Tracking

🗓️ Current Sprint (Week 4 of 12) - Q1 2024
┌─────────────────────────────────────────────────────────────────────────────────┐
│ Progress: ████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│ Overall: 67% Complete (Target: 70% by end of week) ⚠️ Slightly Behind          │
└─────────────────────────────────────────────────────────────────────────────────┘

📈 Epic Progress Timeline
┌──────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
│ Epic     │ Week 1  │ Week 2  │ Week 3  │ Week 4  │ Week 5  │ Week 6  │ Target  │
├──────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
│ EPIC-001 │ 15%     │ 35%     │ 55%     │ 78%     │ 90%     │ 100%    │ 100%    │
│ EPIC-002 │ 5%      │ 15%     │ 25%     │ 34%     │ 50%     │ 75%     │ 85%     │
│ EPIC-003 │ 0%      │ 0%      │ 5%      │ 15%     │ 30%     │ 50%     │ 65%     │
└──────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘

🎯 Milestone Tracking
✅ Week 1: Project setup and epic planning complete
✅ Week 2: User registration feature complete
✅ Week 3: User authentication 90% complete
🔄 Week 4: Payment integration in progress (current)
⏳ Week 5: Mobile foundation and user permissions
⏳ Week 6: Final integration and testing

🚨 Timeline Risks
⚠️ EPIC-002: 5 days behind schedule (payment provider delays)
⚠️ Resource bottleneck: Mike overallocated (3 active tasks)
💡 Recommendation: Reassign TASK-020 to available team member

📊 Velocity Analysis
Team Velocity: 2.1 tasks/week (target: 2.5)
Epic Completion Rate: 1.2 epics/month (target: 1.5)
Quality Gate Pass Rate: 95% (excellent)
External Sync Health: 90% (good)

🔮 Projected Completion
Based on current velocity:
├── EPIC-001: End of Week 5 (1 week ahead)
├── EPIC-002: End of Week 8 (2 weeks behind)
└── EPIC-003: End of Week 10 (on track)
```

### Dependency Mapping View
```bash
/hierarchy-view --dependencies

🔗 Project Dependency Map

📊 Critical Path Analysis
┌─────────────────────────────────────────────────────────────────────────────────┐
│ Critical Path: EPIC-001 → EPIC-002 → EPIC-003 (blocking chain)                 │
│ Total Duration: 12 weeks | Critical Tasks: 8 | Risk Level: Medium              │
└─────────────────────────────────────────────────────────────────────────────────┘

🔗 Inter-Epic Dependencies
EPIC-001 (User Management) → Blocks → EPIC-002 (Payment System)
├── Authentication required for payment processing
├── User sessions needed for payment security
└── Permission system required for payment admin

EPIC-002 (Payment System) → Blocks → EPIC-003 (Mobile Platform)
├── Payment API must be ready for mobile integration
└── Billing system required for mobile monetization

🔗 Feature Dependencies
FEAT-002 (Authentication) → Blocks → FEAT-004 (Payment Gateway)
├── TASK-007 (Session management) → TASK-017 (Payment processing)
└── TASK-009 (Auth tests) → TASK-018 (Payment error handling)

FEAT-001 (User Registration) → Enables → FEAT-003 (User Permissions)
├── User model required for permission assignment
└── Registration flow needed for initial role setup

🔗 Current Blockers
❌ TASK-017 (Payment processing) waiting for TASK-007 completion
   Impact: Delays FEAT-004 by 2 days
   Resolution: Complete session management tests

⚠️ TASK-022 (Billing reports) depends on external payment provider API
   Impact: May delay EPIC-002 completion
   Mitigation: Implement mock data for development

🔗 Dependency Health
✅ 18 dependencies resolved
🔄 4 dependencies in progress
⚠️ 2 dependencies at risk
❌ 1 dependency blocked

📊 Dependency Metrics
Average Resolution Time: 1.2 days
Longest Blocking Chain: 4 tasks (8 days)
Cross-Epic Dependencies: 3 (medium complexity)
External Dependencies: 2 (payment provider, mobile framework)

💡 Optimization Recommendations
1. Parallelize TASK-012 and TASK-013 (no dependencies)
2. Start TASK-024 early (mobile setup has long lead time)
3. Implement TASK-020 mock to unblock development
4. Consider splitting TASK-017 to reduce blocking impact
```

### Requirements Management Workflow Integration
```bash
/hierarchy-view --workflow

🔄 Requirements Management Workflow Status Overview

📊 Stage Distribution Across Hierarchy
┌─────────────────────────────────────────────────────────────────────────────────┐
│                     REQUIREMENTS MANAGEMENT STAGE DISTRIBUTION                   │
└─────────────────────────────────────────────────────────────────────────────────┘

📋 Stage 1: Requirements Gathering (100% Complete) ✅
├── Epic specifications: 3/3 complete
├── Feature specifications: 6/6 complete
├── EARS requirements: 100% documented
└── Human checkpoint: All specifications approved ✅

📋 Stage 2: Task Definition (90% Complete) 🔄
├── Task generation: 26/26 tasks created ✅
├── EARS requirements: 100% linked ✅
├── BDD scenarios: 85% coverage (22/26 tasks)
├── Acceptance criteria: 100% defined ✅
├── PM tool export: 90% complete (Linear pending)
└── Human checkpoint: 24/26 tasks approved ✅

📋 Stage 3: Execution (67% Complete) 🔄
├── Implementation progress: 67% average
├── Quality gates: 95% pass rate ✅
├── Test coverage: 88% average ✅
├── Collaboration: Active (60% human, 40% AI)
├── External tool sync: 90% healthy
└── Execution readiness: 12/26 tasks ready

📋 Stage 4: Validation & Completion (35% Complete) ⏳
├── Ready for completion: 12/26 (46%)
├── Testing: 8/12 completed tasks verified
├── Deployment: 6/12 deployed
├── Acceptance: 4/6 deployed features validated
└── Human checkpoint: Completion approval pending for 4 tasks

🎯 Workflow Health by Epic
EPIC-001: Execution → Completion (78% in execution, 45% completion-ready)
├── 8/10 tasks in execution phase
├── 5/10 tasks ready for completion
└── Workflow status: Healthy ✅

EPIC-002: Task Definition → Execution (34% in execution, 15% completion-ready)
├── 6/8 tasks in execution phase
├── 2/8 tasks ready for completion
└── Workflow status: At risk ⚠️ (payment provider dependency)

EPIC-003: Task Definition → Execution (15% in execution, 0% completion-ready)
├── 2/8 tasks in execution phase
├── 0/8 tasks ready for completion
└── Workflow status: On track ✅ (early planning phase)

🤝 Human Checkpoint Status
┌─────────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│ Stage           │ Pending     │ In Review   │ Approved    │ Rejected    │
├─────────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│ Gathering       │ 0           │ 0           │ 3           │ 0           │
│ Definition      │ 2           │ 0           │ 24          │ 0           │
│ Execution       │ 8           │ 6           │ 12          │ 0           │
│ Completion      │ 4           │ 2           │ 6           │ 0           │
└─────────────────┴─────────────┴─────────────┴─────────────┴─────────────┘

🔧 MCP Integration Status
✅ Requirements MCP: Active and healthy
✅ PM Tools MCP: Connected (Jira, Linear, GitHub)
⚠️ Testing MCP: Rate limited (recoverable)
✅ Deployment MCP: Active (AWS, Docker)

💡 Workflow Optimization Recommendations
1. Address Linear sync issue to reach 100% Stage 2 completion
2. Focus on payment provider integration to unblock EPIC-002
3. Prepare Stage 4 infrastructure for EPIC-001 completion
4. Schedule human checkpoints for pending Stage 3 reviews
```

### External Tools Integration View
```bash
/hierarchy-view --external-tools

🔗 External PM Tool Integration Overview

📊 Multi-Tool Synchronization Status
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        EXTERNAL TOOL INTEGRATION HEALTH                        │
└─────────────────────────────────────────────────────────────────────────────────┘

🔧 Jira Integration
Connection: ✅ Healthy (last sync: 5 minutes ago)
Project: PROJ (Company Project Management)
├── 3 Epics synced as Epics
├── 6 Features synced as Stories
├── 26 Tasks synced as Sub-tasks
├── Sync frequency: Every 15 minutes
├── Last conflict: None (24 hours)
└── API health: 100% (no rate limits)

URL Structure:
├── EPIC-001 → https://company.atlassian.net/browse/PROJ-123
├── FEAT-001 → https://company.atlassian.net/browse/PROJ-124
└── TASK-001 → https://company.atlassian.net/browse/PROJ-125

🔧 Linear Integration
Connection: ⚠️ Partial (rate limited, retry in 12 minutes)
Workspace: Engineering Team
├── 3 Epics synced as Initiatives
├── 5/6 Features synced as Features (1 pending)
├── 24/26 Tasks synced as Issues (2 pending)
├── Sync frequency: Every 30 minutes
├── Last conflict: 2 hours ago (resolved)
└── API health: 85% (rate limited)

URL Structure:
├── EPIC-001 → https://linear.app/company/initiative/PROJECT-456
├── FEAT-001 → https://linear.app/company/feature/PROJECT-457
└── TASK-001 → https://linear.app/company/issue/PROJECT-458

🔧 GitHub Projects Integration
Connection: ✅ Healthy (last sync: 2 minutes ago)
Repository: company/ai-engineer
├── 3 Epics synced as Milestones
├── 6 Features synced as Issues (labeled as features)
├── 26 Tasks synced as Issues (linked to features)
├── Sync frequency: Every 10 minutes
├── Last conflict: None (48 hours)
└── API health: 100% (no rate limits)

URL Structure:
├── EPIC-001 → https://github.com/company/ai-engineer/milestone/1
├── FEAT-001 → https://github.com/company/ai-engineer/issues/247
└── TASK-001 → https://github.com/company/ai-engineer/issues/248

🔧 Azure DevOps Integration
Connection: ⏳ Not configured
Status: Available for setup
Estimated setup time: 2 hours
Recommended for: Enterprise compliance requirements

📊 Sync Performance Metrics
Average Sync Time: 3.2 seconds per hierarchy level
Total API Calls/Hour: 245 (well within limits)
Data Consistency: 98.5% (excellent)
Conflict Resolution: 95% automatic, 5% manual

🔄 Recent Sync Activity
[10:30] ✅ TASK-017 progress updated in all tools (70% complete)
[10:25] ✅ FEAT-004 status synchronized (Jira: In Progress, Linear: Active)
[10:20] ⚠️ Linear rate limit hit, queued 2 updates for retry
[10:15] ✅ EPIC-002 progress rollup updated (34% complete)
[10:10] ✅ New task TASK-027 exported to all configured tools

🚨 Sync Issues & Resolutions
⚠️ Linear: Rate limit exceeded (auto-recovery in 12 minutes)
   Impact: 2 pending task updates
   Mitigation: Automatic retry queue active

💡 Integration Optimization
✅ All critical data synchronized within 15 minutes
✅ Hierarchy relationships preserved in all tools
✅ Progress rollup functioning correctly
⚠️ Consider increasing Linear sync interval to avoid rate limits
✅ GitHub webhook integration performing optimally

🔧 Quick Actions
├── Force sync all tools: /epic-sync --all --force
├── Resolve Linear issues: /epic-sync --tool linear --retry
├── View detailed sync logs: /hierarchy-view --sync-logs
└── Configure Azure DevOps: /pm-config azure --setup
```

## Filtering and Navigation Options

### Scope Filtering
```bash
# View specific epic with all children
/hierarchy-view EPIC-001

# View feature with all tasks
/hierarchy-view FEAT-003

# View by status
/hierarchy-view --status in_progress
/hierarchy-view --status blocked

# View by assignee
/hierarchy-view --assignee "Mike Johnson"

# View by priority
/hierarchy-view --priority high
```

### Display Options
```bash
# Compact view (summary only)
/hierarchy-view --compact

# Detailed view (full metadata)
/hierarchy-view --detailed

# Progress focus
/hierarchy-view --progress-only

# External tools only
/hierarchy-view --external-only

# Real-time monitoring
/hierarchy-view --monitor
```

### Export Options
```bash
# Export hierarchy to formats
/hierarchy-view --export json
/hierarchy-view --export csv
/hierarchy-view --export html

# Generate reports
/hierarchy-view --report executive
/hierarchy-view --report technical
/hierarchy-view --report stakeholder
```

## Interactive Features

### Real-time Updates
```bash
# Monitor mode with live updates
/hierarchy-view --monitor

📊 Live Project Hierarchy (Updating every 30 seconds)
Press 'q' to quit, 'r' to refresh, 'f' to filter

[11:45:32] ✅ TASK-017 completed (Payment processing logic)
[11:45:15] 🔄 FEAT-004 progress updated (60% → 75%)
[11:44:58] ✅ EPIC-002 milestone reached (40% complete)
[11:44:30] 🔄 External sync: Jira, Linear, GitHub updated
```

### Interactive Navigation
```bash
# Navigate hierarchy interactively
/hierarchy-view --interactive

Select scope:
1) Complete portfolio overview
2) Specific epic (EPIC-001, EPIC-002, EPIC-003)
3) Feature breakdown
4) Task details
5) Timeline view
6) Dependency mapping

Choice [1-6]: 2

Select epic:
1) EPIC-001: User Management System (78% complete)
2) EPIC-002: Payment System (34% complete)
3) EPIC-003: Mobile Platform (15% complete)

Choice [1-3]: 1

Display options for EPIC-001:
1) Hierarchy view
2) Progress timeline
3) External tool status
4) Quality metrics
5) Team workload

Choice [1-5]: 1
```

## Integration with Other Commands

### Cross-Command Navigation
```bash
# Quick actions from hierarchy view
/hierarchy-view EPIC-001

# Suggested actions shown:
💡 Available Actions:
├── Task execution: Use your workflow or taskwright integration
├── View feature details: /feature-status FEAT-003
├── Sync epic progress: /epic-sync EPIC-001
└── Generate epic report: /epic-status EPIC-001 --report
```

### Workflow Integration
```bash
# Hierarchy view triggers workflow suggestions
/hierarchy-view --suggestions

🔍 Workflow Optimization Suggestions:
1. EPIC-002 is behind schedule → Consider reassigning resources
2. TASK-017 is on critical path → Monitor closely for delays
3. Linear sync issues → Run /epic-sync --tool linear --force
4. 6 tasks ready for QA → Schedule QA review session
5. EPIC-001 near completion → Prepare celebration and retrospective
```

## Best Practices

1. **Regular Reviews**: Use hierarchy view daily for project health checks
2. **Progress Monitoring**: Monitor timeline view weekly for velocity tracking
3. **Dependency Management**: Review dependency map when planning new work
4. **External Tool Health**: Check sync status regularly to maintain data consistency
5. **Team Coordination**: Use assignee filtering for workload distribution
6. **Stakeholder Communication**: Use executive reports for business updates

This command provides comprehensive project visualization while maintaining seamless integration with the **Epic → Feature → Task hierarchy** and requirements management workflow.

**Standalone:** Works independently to visualize project structure. For task execution workflow, install taskwright.