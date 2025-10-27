# Task Sync - Bidirectional PM Tool Synchronization for Tasks

Synchronize individual task data between local files and external project management tools with automatic feature/epic progress rollup.

## Usage
```bash
/task-sync [task-id] [options]
```

## Examples
```bash
# Sync all tasks with their configured tools
/task-sync

# Sync specific task to all configured tools
/task-sync TASK-001

# Force sync specific task to Jira
/task-sync TASK-001 --tool jira --force

# Export task to new tool
/task-sync TASK-001 --export linear

# Sync with feature and epic rollup
/task-sync TASK-001 --rollup-progress

# Pull updates from external tools
/task-sync TASK-001 --pull

# Push local changes to external tools
/task-sync TASK-001 --push
```

## Task-Level Synchronization

### Bidirectional Data Flow
Tasks sync with external tools as Issues/Sub-tasks with automatic hierarchy linkage:

```
Local Task File ←→ External PM Tool (Issue/Sub-task)
    ↓                         ↓
Task Progress            Issue/Sub-task Status
Acceptance Criteria      Issue Description/Checklist
Implementation Steps     Comments/Updates
Feature Context         Parent Feature/Story Link
Epic Context            Epic/Initiative Link
```

### Hierarchy Preservation in External Tools
```
External Tool Hierarchy:
EPIC (Initiative/Epic)
└── FEAT (Story/Feature)
    ├── TASK (Sub-task/Issue) ← Synced individually
    └── TASK (Sub-task/Issue) ← Synced individually
```

## PM Tool Mapping

### Jira Integration (Tasks as Sub-tasks)
```yaml
task_mapping:
  local_field: jira_field
  title: → summary
  description: → description
  status: → status
  progress: → progress_percentage
  assignee: → assignee
  priority: → priority
  acceptance_criteria: → description_section
  implementation_steps: → comments
  feature: → parent_issue (story link)
  epic: → epic_link
  timeline: → due_date
  complexity: → story_points
  external_ids.jira: → key
```

### Linear Integration (Tasks as Issues)
```yaml
task_mapping:
  local_field: linear_field
  title: → title
  description: → description
  status: → state
  progress: → completion_percentage
  assignee: → assignee
  priority: → priority (1-4 scale)
  acceptance_criteria: → description_section
  feature: → parent_issue
  epic: → initiative_link
  timeline: → target_date
  complexity: → estimate
  external_ids.linear: → id
```

### GitHub Projects Integration (Tasks as Issues)
```yaml
task_mapping:
  local_field: github_field
  title: → title
  description: → body
  status: → status
  progress: → completion_percentage
  assignee: → assignees
  priority: → priority_label
  acceptance_criteria: → checklist_in_body
  feature: → linked_issue
  epic: → milestone_link
  timeline: → milestone_date
  complexity: → size_label
  external_ids.github: → number
```

### Azure DevOps Integration (Tasks as Task Work Items)
```yaml
task_mapping:
  local_field: azure_field
  title: → title
  description: → description
  status: → state
  progress: → completed_work
  assignee: → assigned_to
  priority: → priority
  acceptance_criteria: → acceptance_criteria
  feature: → parent_work_item
  epic: → epic_link
  timeline: → target_date
  complexity: → effort
  external_ids.azure: → id
```

## Sync Operations Detail

### Individual Task Sync
```bash
/task-sync TASK-045

# Output:
🔄 Syncing Task: TASK-045 - Add Session Management

📊 Pre-Sync Status
Local: Modified 10 minutes ago
Jira PROJ-129: Modified 5 minutes ago (newer)
Linear PROJECT-461: Modified 20 minutes ago

🔗 Hierarchy Context Validation
Feature FEAT-003: ✅ Synced with external tools
Epic EPIC-001: ✅ Synced with external tools
Parent Links: ✅ Valid in all tools

📋 Progress Analysis
Local Progress: 60% (3/5 implementation steps)
Acceptance Criteria: 6/10 completed
Quality Gates: 3/4 passed
Test Coverage: 85%

🔍 Conflict Detection
Field 'status': Local='In Progress', Jira='In Review' → Using Jira (external authority)
Field 'progress': Local=60%, Calculated=60% → No conflict
Field 'assignee': Local='Sarah', Linear='Sarah Chen' → Normalize to 'Sarah Chen'

⬇️ Pulling Changes from External Tools
Jira: Updated status → 'In Review'
Jira: Added comment from Mike → "Good progress on session service"
Linear: No significant changes

⬆️ Pushing Changes to External Tools
Jira: Updated acceptance criteria completion → 6/10
Linear: Updated progress → 60%
Linear: Updated test coverage → 85%

📊 Progress Rollup Calculation
Task completion contributes to:
├── Feature FEAT-003: 62% → 65% (+3%)
├── Epic EPIC-001: 55% → 57% (+2%)
└── Portfolio: 45% → 46% (+1%)

🔄 Automatic Feature/Epic Sync
✅ Feature FEAT-003: Progress updated via /feature-sync
✅ Epic EPIC-001: Progress updated via /epic-sync

✅ Sync Complete
Updated 2 external tools
Resolved 3 conflicts
Updated feature and epic progress
Maintained hierarchy integrity

📋 Summary
✅ Jira Sub-task PROJ-129: Synced successfully
✅ Linear Issue PROJECT-461: Synced successfully
🕐 Next auto-sync: 15 minutes
📈 Feature progress updated: 62% → 65%
📊 Epic progress updated: 55% → 57%
```

### Batch Task Sync
```bash
/task-sync --feature FEAT-003

# Output:
🔄 Syncing All Tasks for Feature: FEAT-003

📊 Feature Context
Feature: FEAT-003 (User Authentication)
Epic: EPIC-001 (User Management System)
Tasks to Sync: 5 tasks

📋 Task Sync Results
✅ TASK-043: Design auth UI (100% complete)
   ├── Jira PROJ-127: ✅ Synced
   └── Linear PROJECT-460: ✅ Synced

🔄 TASK-044: Implement login API (90% complete)
   ├── Jira PROJ-128: ✅ Synced (status: In Review)
   └── Linear PROJECT-461: ✅ Synced

🔄 TASK-045: Add session management (65% complete)
   ├── Jira PROJ-129: ✅ Synced
   └── Linear PROJECT-462: ✅ Synced

❌ TASK-046: Password reset flow (0% complete)
   ├── Jira PROJ-130: ✅ Synced (status: Blocked)
   └── Linear PROJECT-463: ⚠️ Rate limit (retry in 15 min)

⏳ TASK-047: Authentication tests (0% complete)
   ├── Jira PROJ-131: ✅ Synced (status: Pending)
   └── Linear PROJECT-464: ✅ Synced

📊 Feature Progress Rollup
Previous: 62% → Current: 65% (+3%)
Calculation: (100% + 90% + 65% + 0% + 0%) / 5 = 51% → Weighted: 65%

📈 Epic Progress Impact
Epic EPIC-001: 55% → 57% (feature weight: 33%)

✅ Batch Sync Complete
Synced 5 tasks across 2 PM tools
1 tool rate limited (auto-retry scheduled)
Feature and epic progress updated
```

## Progress Rollup Integration

### Automatic Progress Calculation
Task sync automatically triggers feature and epic progress updates:

```
Task Progress Update → Feature Recalculation → Epic Recalculation
Task Status Change → Feature Status Check → Epic Status Check
Task Completion → Feature Milestone Check → Epic Milestone Check
```

### Rollup Configuration
```bash
# Enable automatic rollup (default)
/task-sync TASK-001 --rollup auto

# Manual rollup only
/task-sync TASK-001 --rollup manual

# Skip rollup (for batch operations)
/task-sync TASK-001 --no-rollup
```

## Integration with Feature and Epic Sync

### Cascade Sync Operations
```bash
# Task sync triggers feature sync
/task-sync TASK-045
# Automatically executes: /feature-sync FEAT-003 --progress-only

# Feature sync triggers epic sync
# Automatically executes: /epic-sync EPIC-001 --progress-only

# Full hierarchy sync
/task-sync TASK-045 --cascade-sync
# Executes: task-sync → feature-sync → epic-sync
```

### Sync Coordination
```bash
# Prevent cascade conflicts
/task-sync TASK-045 --coordinate
# Ensures feature and epic sync don't conflict with task sync

# Batch hierarchy sync
/task-sync --epic EPIC-001 --full-hierarchy
# Syncs all tasks, then features, then epic
```

## Quality Gate Integration

### Test Result Sync
```bash
/task-sync TASK-045 --include-tests

# Syncs:
# - Test coverage percentage
# - Test pass/fail status
# - Quality gate results
# - Code quality metrics
```

### Implementation Progress Sync
```bash
/task-sync TASK-045 --implementation-details

# Syncs:
# - Acceptance criteria completion
# - Implementation step progress
# - Code review status
# - Deployment readiness
```

## Conflict Resolution

### Task-Level Conflicts
```bash
# Automatic resolution based on task type
Progress Conflicts: Use calculated progress from acceptance criteria
Status Conflicts: Use external tool (PM tool authority)
Assignment Conflicts: Use most recent assignment
Content Conflicts: Merge with conflict markers

# Manual resolution
/task-sync TASK-045 --resolve-conflicts
```

### Hierarchy Consistency
```bash
# Validate hierarchy links
/task-sync TASK-045 --validate-hierarchy

# Repair broken links
/task-sync TASK-045 --repair-links

# Rebuild hierarchy
/task-sync TASK-045 --rebuild-hierarchy
```

## Performance Optimization

### Smart Sync
```bash
# Only sync changed fields
/task-sync TASK-045 --incremental

# Sync specific fields only
/task-sync TASK-045 --fields progress,status,assignee

# Skip expensive operations
/task-sync TASK-045 --skip-rollup --skip-validation
```

### Batch Optimization
```bash
# Parallel sync for independent tasks
/task-sync --feature FEAT-003 --parallel

# Rate limit management
/task-sync --all --rate-limit 50  # requests per minute

# Prioritized sync
/task-sync --blocked --priority high
```

## Error Handling

### Common Scenarios
```bash
# Missing parent feature/epic
❌ Task sync failed: Feature FEAT-003 not found in Jira
🔧 Fix: /feature-sync FEAT-003 --export jira

# Hierarchy mismatch
❌ Task sync failed: Task linked to wrong feature in Linear
🔧 Fix: /task-sync TASK-045 --repair-links

# Permission issues
❌ Task sync failed: No permission to update Jira issue
🔧 Fix: Update Jira permissions or use different account

# Rate limiting
⚠️ Task sync rate limited: Linear API limit exceeded
🔄 Auto-retry in 15 minutes, or use: /task-sync TASK-045 --retry-now
```

## Agentecflow Stage 3 Integration

### Implementation Progress Sync
```bash
/task-sync TASK-045 --agentecflow-stage3

# Output:
🔄 Agentecflow Stage 3 Task Sync: TASK-045

📊 Implementation Progress
Code Implementation: 65% complete
Test Coverage: 85% (target: 80%) ✅
Quality Gates: 3/4 passed
Documentation: 70% complete

🔗 External Tool Sync
✅ Jira: Implementation progress updated
✅ Linear: Quality metrics synced
✅ GitHub: Code review status updated

🎯 Stage 3 → Stage 4 Readiness
Task Readiness: 75% (needs final tests)
Feature Readiness: 85% (on track)
Epic Readiness: 65% (multiple features in progress)

📊 Human/AI Collaboration Tracking
Implementation Mode: Human-led with AI assistance
Code Generation: 40% AI, 60% human
Test Generation: 80% AI, 20% human validation
Quality Assurance: 100% human review

✅ Stage 3 Integration Complete
Implementation progress tracked
Quality metrics synchronized
Readiness calculated for Stage 4 transition
```

## Integration with Other Commands

### Automatic Sync Triggers
```bash
# Task work completion triggers sync
/task-work TASK-045
# Automatically executes: /task-sync TASK-045 --rollup-progress

# Task completion triggers hierarchy sync
/task-complete TASK-045
# Automatically executes: /task-sync TASK-045 --cascade-sync

# Task status changes trigger sync
/task-status TASK-045 --update-status completed
# Automatically executes: /task-sync TASK-045
```

### Cross-Command Integration
```bash
# View task after sync
/task-sync TASK-045 → /task-status TASK-045 --hierarchy

# Sync related tasks
/task-sync TASK-045 --sync-dependencies

# Sync blocking/blocked tasks
/task-sync TASK-045 --sync-blockers
```

## Configuration Management

### Task-Level Sync Configuration
```yaml
# .claude/task-sync-config.yml
tasks:
  TASK-045:
    auto_sync: true
    sync_interval: "15m"
    rollup_progress: true
    tools: ["jira", "linear"]
    conflict_resolution: "external-authority"
    include_tests: true
    sync_dependencies: false

  TASK-046:
    auto_sync: false
    manual_sync_only: true
    tools: ["jira"]
```

### Feature Inheritance
Tasks inherit sync configuration from their parent feature where not specified locally.

## Best Practices

1. **Hierarchy Sync Order**: Always sync parent feature/epic before individual tasks
2. **Progress Accuracy**: Use acceptance criteria completion for accurate progress calculation
3. **Frequent Sync**: Enable auto-sync for active tasks to maintain real-time consistency
4. **Rollup Coordination**: Allow automatic rollup to maintain feature/epic progress accuracy
5. **Conflict Strategy**: Use external tool authority for status, local authority for technical metrics
6. **Performance Monitoring**: Monitor sync performance and use batch operations for large task sets

This command ensures seamless integration between individual task management and external PM tools while maintaining the complete **Epic → Feature → Task hierarchy** and supporting **Agentecflow Stage 3: Engineering** workflow tracking.