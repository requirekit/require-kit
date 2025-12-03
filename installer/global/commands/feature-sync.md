# Feature Sync - Bidirectional PM Tool Synchronization

Synchronize feature data between local files and external project management tools with task-level progress rollup and epic integration.

## Usage
```bash
/feature-sync [feature-id] [options]
```

## Examples
```bash
# Sync all features with their configured tools
/feature-sync

# Sync specific feature to all configured tools
/feature-sync FEAT-001

# Force sync specific feature to Jira
/feature-sync FEAT-001 --tool jira --force

# Export feature to new tool
/feature-sync FEAT-001 --export linear

# Sync with task progress rollup
/feature-sync FEAT-001 --include-tasks

# Pull updates from external tools
/feature-sync FEAT-001 --pull

# Push local changes to external tools
/feature-sync FEAT-001 --push
```

## Feature-Level Synchronization

### Bidirectional Data Flow
Features sync with external tools as Stories/Features with automatic task linkage:

```
Local Feature File ←→ External PM Tool (Story/Feature)
    ↓                         ↓
Task Progress            Sub-tasks/Child Issues
Epic Context            Epic/Initiative Link
Requirements            Acceptance Criteria
BDD Scenarios           Test Cases
Timeline               Sprint Assignment
```

### Epic-Feature-Task Hierarchy Sync
```
External Tool Hierarchy:
EPIC (Initiative/Epic)
├── FEAT (Story/Feature)
│   ├── TASK (Sub-task/Issue)
│   └── TASK (Sub-task/Issue)
└── FEAT (Story/Feature)
    ├── TASK (Sub-task/Issue)
    └── TASK (Sub-task/Issue)
```

## PM Tool Mapping

### Jira Integration (Features as Stories)
```yaml
feature_mapping:
  local_field: jira_field
  title: → summary
  description: → description
  epic: → epic_link
  acceptance_criteria: → acceptance_criteria (custom field)
  priority: → priority
  timeline: → sprint
  complexity: → story_points
  tasks: → sub_tasks (linked issues)
  progress: → progress (calculated from sub-tasks)
  status: → status
  requirements: → linked_issues (implements)
  bdd_scenarios: → test_cases (linked)
```

### Linear Integration (Features as Features)
```yaml
feature_mapping:
  local_field: linear_field
  title: → title
  description: → description
  epic: → initiative_link
  acceptance_criteria: → description_section
  priority: → priority (1-4 scale)
  timeline: → target_date
  complexity: → estimate
  tasks: → child_issues
  progress: → completion_percentage
  status: → state
  requirements: → related_issues
```

### GitHub Projects Integration (Features as Enhanced Issues)
```yaml
feature_mapping:
  local_field: github_field
  title: → title
  description: → body
  epic: → milestone_link
  acceptance_criteria: → checklist_in_body
  priority: → priority_label
  timeline: → milestone_date
  complexity: → size_label
  tasks: → linked_issues
  progress: → project_field
  status: → status_field
  requirements: → linked_issues
```

### Azure DevOps Integration (Features as Feature Work Items)
```yaml
feature_mapping:
  local_field: azure_field
  title: → title
  description: → description
  epic: → parent_epic
  acceptance_criteria: → acceptance_criteria
  priority: → priority
  timeline: → iteration_path
  complexity: → effort
  tasks: → child_tasks
  progress: → completed_work
  status: → state
  requirements: → related_work_items
```

## Task Progress Rollup

### Automatic Progress Calculation
Feature progress automatically calculated from linked tasks:
```
Feature Progress = (Σ Completed Tasks / Total Tasks) × 100
Weighted Progress = (Σ Task Weight × Completion) / Total Weight
Epic Progress = (Σ Feature Progress × Feature Weight) / Total Features
```

### Progress Sync to External Tools
```bash
/feature-sync FEAT-001 --include-tasks

# Syncs:
# - Feature-level progress to external tool
# - Individual task status and completion
# - Epic-level rollup progress
# - Timeline and milestone updates
```

## Sync Operations Detail

### Full Feature Sync
```bash
/feature-sync FEAT-001

# Output:
🔄 Syncing Feature: FEAT-001 - User Authentication

📊 Pre-Sync Status
Local: Modified 5 minutes ago
Jira PROJ-124: Modified 10 minutes ago
Linear PROJECT-457: Modified 15 minutes ago

🔗 Epic Context Validation
Epic EPIC-001: ✅ Synced with external tools
Jira Epic: PROJ-123 ✅
Linear Initiative: PROJECT-456 ✅

📋 Task Progress Rollup
TASK-043: ✅ Complete (100%)
TASK-044: ✅ Complete (100%)
TASK-045: 🔄 In Progress (70%)
TASK-046: ❌ Blocked (0%)
TASK-047: ⏳ Pending (0%)
Calculated Progress: 54% (2.7/5 tasks weighted)

🔍 Conflict Detection
Field 'status': Local='In Progress', Jira='In Review' → Using Jira (external authority)
Field 'progress': Local=60%, Calculated=54% → Using Calculated (task-based)

⬇️ Pulling Changes from External Tools
Jira: Updated status → 'In Review'
Jira: Updated sprint assignment → 'Sprint-4'
Linear: No significant changes

⬆️ Pushing Changes to External Tools
Jira: Updated progress → 54%
Jira: Updated task completion → 2/5 completed
Linear: Updated progress → 54%
Linear: Updated status → 'In Review'

📋 Task Sync Status
✅ TASK-043: Synced to Jira sub-task PROJ-125
✅ TASK-044: Synced to Jira sub-task PROJ-126
🔄 TASK-045: Synced to Jira sub-task PROJ-127 (in progress)
❌ TASK-046: Synced to Jira sub-task PROJ-128 (blocked)
⏳ TASK-047: Synced to Jira sub-task PROJ-129 (pending)

✅ Sync Complete
Updated 2 external tools
Resolved 2 conflicts
Synced 5 linked tasks
Updated epic progress rollup

📋 Summary
✅ Jira Story PROJ-124: Synced successfully
✅ Linear Feature PROJECT-457: Synced successfully
🕐 Next auto-sync: 30 minutes
📈 Epic EPIC-001 progress updated: 67% → 54%
```

### Export to New Tool
```bash
/feature-sync FEAT-001 --export github

# Output:
📤 Exporting Feature to GitHub Projects

🔍 Feature Analysis
Title: User Authentication
Epic: EPIC-001 (User Management System)
Progress: 54% (2.7/5 tasks)
Tasks: 5 linked tasks

🔗 Epic Context Inheritance
GitHub Epic Issue: #245 (User Management System)
Project: Q1-User-Features
Milestone: Sprint-3

🏗️ Creating GitHub Feature Issue
Repository: company/ai-engineer
Title: "[FEATURE] User Authentication"
Labels: feature, authentication, high-priority

📋 Acceptance Criteria Export
✅ AC-001: User can log in with email/password
✅ AC-002: Invalid credentials show error message
🔄 AC-003: Session expires after 24 hours
⏳ AC-004: Password complexity validation

📋 Task Linkage
Creating linked issues for 5 tasks:
✅ Issue #246: Design authentication UI (TASK-043)
✅ Issue #247: Implement login API (TASK-044)
🔄 Issue #248: Add session management (TASK-045)
❌ Issue #249: Password reset flow (TASK-046)
⏳ Issue #250: Authentication tests (TASK-047)

✅ Export Complete
GitHub Feature Issue: #251
URL: https://github.com/company/ai-engineer/issues/251
Project: Added to Q1-User-Features
Milestone: Sprint-3

📝 Local File Updated
Added external_ids.github: 251
Added GitHub sync configuration
Updated sync schedule

Next Steps:
1. View in GitHub: https://github.com/company/ai-engineer/issues/251
2. Enable auto-sync: /feature-sync FEAT-001 --config auto-sync:true
3. Monitor progress: /feature-status FEAT-001
```

## Workflow Integration

### Task Definition → Execution Transition Support
```bash
/feature-sync FEAT-001 --workflow-bridge

# Output:
🔄 Workflow Bridge: FEAT-001

📋 Task Definition Complete
✅ Feature specification complete
✅ Requirements traceability established
✅ Acceptance criteria defined (4 criteria)
✅ BDD scenarios linked (3 scenarios)
✅ Implementation tasks generated (5 tasks)

🔗 External Tool Readiness
✅ Jira: Feature story PROJ-124 ready
✅ Linear: Feature PROJECT-457 ready
✅ GitHub: Feature issue #251 ready

👥 Human Checkpoint Status
✅ Feature specification approved
✅ Task breakdown reviewed
🔄 Task execution in progress (54% complete)

🎯 Task Execution Integration
✅ Tasks ready for assignment (guardkit)
✅ PM tools configured for progress tracking
✅ Quality gates defined and monitored
🔄 Execution actively tracked

📊 Workflow Health Metrics
Task Definition Completeness: 100%
PM Tool Integration: 100%
Execution Progress: 54%
Quality Gate Compliance: 85%

🔄 MCP Integration Status
✅ Requirements MCP: Active
✅ PM Tools MCP: Connected and syncing
✅ Task Management MCP: Operational (guardkit)
⏳ Validation MCP: Ready for completion

✅ Workflow Bridge Healthy
Feature ready for continued execution
All external integrations operational
Progress tracking active across tools
```

## Conflict Resolution

### Automatic Resolution Strategies
```bash
# Task-based progress calculation takes precedence
Feature Progress = Calculated from actual task completion

# External tool status authority (configurable)
/feature-sync FEAT-001 --config resolution-strategy:external-authority

# Available strategies:
# - task-calculated: Use task completion for progress (default)
# - external-authority: External tool takes precedence
# - local-authority: Local file takes precedence
# - manual: Always prompt for resolution
```

### Manual Conflict Resolution
```bash
/feature-sync FEAT-001 --resolve-conflicts

# Interactive conflict resolution for feature-level conflicts
# Task-level conflicts handled by task sync
```

## Batch Operations

### Multi-Feature Sync
```bash
# Sync all features in an epic
/feature-sync --epic EPIC-001

# Sync features by status
/feature-sync --status in_progress

# Parallel sync with task rollup
/feature-sync --all --include-tasks --parallel
```

## Performance Optimization

### Incremental Sync
```bash
# Sync only changed features and their tasks
/feature-sync --incremental

# Sync specific fields only
/feature-sync FEAT-001 --fields progress,status,tasks

# Skip expensive operations
/feature-sync FEAT-001 --skip-task-sync
```

## Error Handling

### Common Scenarios
```bash
# Epic sync dependency check
❌ Feature sync failed: Epic EPIC-001 not synced to target tool
🔧 Fix: /epic-sync EPIC-001 --tool jira

# Task sync issues
⚠️ Feature sync warning: 2/5 tasks failed to sync
🔧 Resolution: Task-level issues don't block feature sync

# Hierarchy validation
❌ Feature sync failed: Tasks reference invalid epic in external tool
🔧 Fix: /feature-sync FEAT-001 --rebuild-hierarchy
```

## Integration with Other Commands

### Automatic Sync Triggers
```bash
# Note: The following examples show integration with guardkit
# See INTEGRATION-GUIDE.md for guardkit setup

# Feature sync triggered by task completion (guardkit)
# /task-complete TASK-043
# Automatically triggers: /feature-sync FEAT-001 --fields progress

# Epic sync triggered by feature completion
# /feature-complete FEAT-001
# Automatically triggers: /epic-sync EPIC-001 --fields progress

# Task creation triggers feature sync (guardkit)
# /task-create "New Task" feature:FEAT-001
# Automatically triggers: /feature-sync FEAT-001 --fields tasks
```

### Cross-Command Integration
```bash
# View feature after sync
/feature-sync FEAT-001 → /feature-status FEAT-001

# Sync all related entities
/feature-sync FEAT-001 --with-epic --with-tasks
```

## Configuration Management

### Feature-Level Configuration
```yaml
# .claude/feature-sync-config.yml
features:
  FEAT-001:
    auto_sync: true
    sync_interval: "30m"
    include_tasks: true
    tools: ["jira", "linear"]
    conflict_resolution: "task-calculated"
    epic_rollup: true

  FEAT-002:
    auto_sync: false
    tools: ["github"]
    manual_sync_only: true
```

### Epic Inheritance
Features automatically inherit sync configuration from their epic where not specified locally.

## Best Practices

1. **Epic-First Sync**: Always ensure epic is synced before feature sync
2. **Task Progress Authority**: Use task completion for accurate progress calculation
3. **Frequent Sync**: Enable auto-sync for active features to maintain consistency
4. **Hierarchy Validation**: Verify epic-feature-task relationships in external tools
5. **Conflict Strategy**: Choose appropriate resolution strategy per project workflow
6. **Performance Monitoring**: Monitor sync performance and optimize for large feature sets

This command ensures seamless integration between local feature management and external PM tools while maintaining the complete **Epic → Feature → Task hierarchy** and supporting the requirements management to task specification workflow.

**Standalone:** Works independently for PM tool synchronization. For task execution workflow, install guardkit.