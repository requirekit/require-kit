# Epic Sync - Bidirectional PM Tool Synchronization

> **Status: Specification Only**
>
> This document describes the **intended** epic-sync command behavior for PM tool integration.
> **Actual API integration requires MCP server or custom implementation.**
>
> RequireKit provides structured metadata in epic files ready for export.
> This specification defines how synchronization should work when implemented.

Synchronize epic data between local files and external project management tools (Jira, Linear, Azure DevOps, GitHub Projects).

## Usage
```bash
/epic-sync [epic-id] [options]
```

## Examples
```bash
# Sync all epics with their configured tools
/epic-sync

# Sync specific epic to all configured tools
/epic-sync EPIC-001

# Force sync specific epic to Jira
/epic-sync EPIC-001 --tool jira --force

# Export epic to new tool
/epic-sync EPIC-001 --export linear

# Setup auto-sync for epic
/epic-sync EPIC-001 --setup auto-sync

# Pull updates from external tools
/epic-sync EPIC-001 --pull

# Push local changes to external tools
/epic-sync EPIC-001 --push
```

## Sync Operations

### Bidirectional Synchronization
The sync system maintains consistency between local epic files and external PM tools:

```
Local Epic File ←→ External PM Tool
    ↓                    ↓
Epic Status         Issue/Epic Status
Progress Data       Progress Tracking
Requirements        Linked Issues
Timeline           Target Dates
Stakeholders       Assignees
```

### Conflict Resolution
When conflicts occur between local and remote data:
1. **Last Modified Wins**: Use timestamp comparison
2. **Manual Resolution**: Present choices for manual selection
3. **External Authority**: PM tool takes precedence (configurable)
4. **Local Authority**: Local file takes precedence (configurable)

## Sync Configuration

### Tool-Specific Setup
```bash
# Configure Jira integration
/epic-sync --config jira --url https://company.atlassian.net --token YOUR_TOKEN --project PROJ

# Configure Linear integration
/epic-sync --config linear --token YOUR_TOKEN --team engineering

# Configure GitHub integration
/epic-sync --config github --token YOUR_TOKEN --org company --project ai-engineer

# Configure Azure DevOps
/epic-sync --config azure --url https://dev.azure.com/company --token YOUR_TOKEN --project MyProject
```

### Auto-Sync Settings
```bash
# Enable auto-sync for all epics
/epic-sync --global-config auto-sync:true interval:15min

# Disable auto-sync for specific epic
/epic-sync EPIC-001 --config auto-sync:false

# Set sync strategy
/epic-sync EPIC-001 --config strategy:external-authority
```

## PM Tool Mapping

### Jira Integration
```yaml
sync_mapping:
  local_field: jira_field
  title: → summary
  description: → description
  status: → status
  priority: → priority
  stakeholder: → reporter
  timeline: → target_resolution
  progress: → progress (custom field)
  requirements: → epic_link (linked issues)
  quarter: → fix_version
  external_ids.jira: → key
```

### Linear Integration
```yaml
sync_mapping:
  local_field: linear_field
  title: → title
  description: → description
  status: → state
  priority: → priority (1-4 scale)
  stakeholder: → assignee
  timeline: → target_date
  progress: → progress (0-1)
  quarter: → milestone
  external_ids.linear: → id
```

### GitHub Projects Integration
```yaml
sync_mapping:
  local_field: github_field
  title: → title
  description: → body
  status: → status
  priority: → priority_label
  timeline: → milestone
  progress: → completion_percentage
  requirements: → linked_issues
  external_ids.github: → number
```

### Azure DevOps Integration
```yaml
sync_mapping:
  local_field: azure_field
  title: → title
  description: → description
  status: → state
  priority: → priority
  stakeholder: → assigned_to
  timeline: → target_date
  requirements: → related_work_items
  quarter: → iteration_path
  external_ids.azure: → id
```

## Sync Status and Health

### Health Check
```bash
# Check sync health for all epics
/epic-sync --health

# Output:
✅ Sync Health Report
┌─────────────┬──────────────────────┬─────────────┬─────────────────────────┬──────────────┐
│ Epic ID     │ Title                │ Tool        │ Last Sync               │ Status       │
├─────────────┼──────────────────────┼─────────────┼─────────────────────────┼──────────────┤
│ EPIC-001    │ User Management      │ Jira        │ 2 minutes ago           │ ✅ Healthy   │
│ EPIC-001    │ User Management      │ Linear      │ 5 minutes ago           │ ✅ Healthy   │
│ EPIC-002    │ Payment System       │ Linear      │ 2 hours ago             │ ⚠️ Stale     │
│ EPIC-003    │ Mobile Redesign      │ GitHub      │ Failed: Token expired   │ ❌ Error     │
└─────────────┴──────────────────────┴─────────────┴─────────────────────────┴──────────────┘

🔧 Recommended Actions:
1. EPIC-002: Sync now: /epic-sync EPIC-002 --force
2. EPIC-003: Update token: /epic-sync --config github --refresh-token
```

### Sync History
```bash
# View sync history for epic
/epic-sync EPIC-001 --history

# Output:
📜 Sync History: EPIC-001
┌─────────────────────────┬─────────────┬─────────────┬──────────────────────────────┐
│ Timestamp               │ Tool        │ Operation   │ Result                       │
├─────────────────────────┼─────────────┼─────────────┼──────────────────────────────┤
│ 2024-01-15 14:30:00     │ Jira        │ Push        │ ✅ Updated summary, priority │
│ 2024-01-15 14:25:00     │ Linear      │ Pull        │ ✅ Updated status            │
│ 2024-01-15 14:20:00     │ Jira        │ Push        │ ❌ Rate limit exceeded       │
│ 2024-01-15 14:15:00     │ Linear      │ Push        │ ✅ Created initiative        │
└─────────────────────────┴─────────────┴─────────────┴──────────────────────────────┘
```

## Sync Operations Detail

### Full Sync Process
```bash
/epic-sync EPIC-001

# Output:
🔄 Syncing Epic: EPIC-001 - User Management System

📊 Pre-Sync Status
Local: Modified 10 minutes ago
Jira PROJ-123: Modified 5 minutes ago (newer)
Linear PROJECT-456: Modified 15 minutes ago

🔍 Conflict Detection
Field 'status': Local='In Progress', Jira='In Review' → Using Jira (external authority)
Field 'progress': Local=45%, Linear=40% → Using Local (more recent)

⬇️ Pulling Changes from External Tools
Jira: Updated status → 'In Review'
Linear: No changes needed

⬆️ Pushing Changes to External Tools
Jira: Updated progress → 45%
Linear: Updated progress → 45%, status → 'In Review'

✅ Sync Complete
Updated 2 external tools
Resolved 2 conflicts
Updated local file: docs/epics/EPIC-001-user-management.md

📋 Summary
✅ Jira PROJ-123: Synced successfully
✅ Linear PROJECT-456: Synced successfully
🕐 Next auto-sync: 15 minutes
```

### Export to New Tool
```bash
/epic-sync EPIC-001 --export github

# Output:
📤 Exporting Epic to GitHub Projects

🔍 Epic Analysis
Title: User Management System
Status: In Progress
Progress: 45% (3/8 features)
Priority: High

🏗️ Creating GitHub Project Item
Project: ai-engineer
Repository: company/ai-engineer

✅ Export Complete
GitHub Issue: #247
URL: https://github.com/company/ai-engineer/issues/247
Project Item: Added to 'Q1-2024' milestone

📝 Local File Updated
Added external_ids.github: 247
Added GitHub sync configuration

Next Steps:
1. View in GitHub: https://github.com/company/ai-engineer/issues/247
2. Enable auto-sync: /epic-sync EPIC-001 --config auto-sync:true
```

## Conflict Resolution

### Manual Conflict Resolution
```bash
/epic-sync EPIC-001 --resolve-conflicts

# Interactive conflict resolution:
🔄 Resolving Conflicts for EPIC-001

Conflict 1/3: Field 'status'
Local Value:    'In Progress'
Jira Value:     'In Review'
Linear Value:   'In Progress'

Options:
1) Use Local value ('In Progress')
2) Use Jira value ('In Review')
3) Use Linear value ('In Progress')
4) Enter custom value
5) Skip this field

Choice [1-5]: 2

✅ Will use Jira value: 'In Review'

Conflict 2/3: Field 'priority'...
```

### Automatic Resolution Rules
```bash
# Set resolution strategy
/epic-sync EPIC-001 --config resolution-strategy:latest-wins

# Available strategies:
# - latest-wins: Use most recently modified value
# - external-authority: External tool takes precedence
# - local-authority: Local file takes precedence
# - manual: Always prompt for resolution
# - field-specific: Different strategies per field
```

## Webhooks and Real-time Sync

### Webhook Configuration
```bash
# Setup webhook listeners (where supported)
/epic-sync --setup-webhooks

# Configure webhook endpoint
/epic-sync --config webhook-url:https://your-domain.com/webhooks/epic-sync

# Test webhook connectivity
/epic-sync --test-webhooks
```

### Real-time Sync Status
```bash
# Monitor real-time sync events
/epic-sync --monitor

# Output:
🔄 Real-time Sync Monitor
Press Ctrl+C to stop...

[14:35:12] ✅ EPIC-001: Jira → Local (status updated)
[14:35:45] ⬆️ EPIC-002: Local → Linear (progress updated)
[14:36:01] ⚠️ EPIC-003: GitHub sync failed (rate limit)
[14:36:15] 🔄 EPIC-001: Auto-retry GitHub sync
[14:36:18] ✅ EPIC-001: GitHub sync recovered
```

## Data Backup and Recovery

### Backup Before Sync
```bash
# Create backup before major sync operation
/epic-sync EPIC-001 --backup

# Restore from backup if sync fails
/epic-sync EPIC-001 --restore latest

# List available backups
/epic-sync EPIC-001 --list-backups
```

### Sync Logs
```bash
# View detailed sync logs
/epic-sync --logs

# Export sync logs for analysis
/epic-sync --logs --export csv
```

## Configuration Management

### Global Configuration
```yaml
# .claude/epic-sync-config.yml
global:
  auto_sync: true
  sync_interval: "15m"
  conflict_resolution: "latest-wins"
  backup_before_sync: true
  max_retries: 3

tools:
  jira:
    enabled: true
    url: "https://company.atlassian.net"
    project: "PROJ"
    rate_limit: 100  # requests per hour

  linear:
    enabled: true
    team: "engineering"
    rate_limit: 200

  github:
    enabled: true
    org: "company"
    repository: "ai-engineer"

epics:
  EPIC-001:
    auto_sync: true
    tools: ["jira", "linear"]
    conflict_resolution: "external-authority"
  EPIC-002:
    auto_sync: false
    tools: ["linear"]
```

## Error Handling and Recovery

### Common Error Scenarios
```bash
# Rate limit exceeded
❌ Sync failed: Rate limit exceeded for Jira API
🔄 Retrying in 15 minutes...
💡 Consider increasing sync interval: /epic-sync --config sync-interval:30m

# Authentication failure
❌ Sync failed: GitHub authentication failed
🔧 Update token: /epic-sync --config github --refresh-token

# Network connectivity issues
❌ Sync failed: Connection timeout to Linear API
🔄 Retrying in 5 minutes (attempt 2/3)...

# Data conflicts
⚠️ Sync warning: Unresolvable conflict in EPIC-001
🔧 Manual resolution required: /epic-sync EPIC-001 --resolve-conflicts
```

### Recovery Operations
```bash
# Force sync ignoring errors
/epic-sync EPIC-001 --force --ignore-conflicts

# Reset sync state
/epic-sync EPIC-001 --reset-sync-state

# Rebuild external mappings
/epic-sync EPIC-001 --rebuild-mappings
```

## Performance and Optimization

### Batch Operations
```bash
# Sync multiple epics efficiently
/epic-sync EPIC-001,EPIC-002,EPIC-003 --batch

# Sync all active epics
/epic-sync --all --status active

# Parallel sync with concurrency limit
/epic-sync --all --parallel --max-concurrent 3
```

### Sync Optimization
```bash
# Incremental sync (only changed fields)
/epic-sync EPIC-001 --incremental

# Sync only specific fields
/epic-sync EPIC-001 --fields status,progress

# Skip expensive operations
/epic-sync EPIC-001 --skip-attachments --skip-comments
```

## Integration with Other Commands

### Cross-Command Integration
```bash
# Sync after epic creation
/epic-create "New Epic" export:jira
# Automatically triggers: /epic-sync EPIC-XXX

# Sync after status changes
/epic-status EPIC-001 --update status:completed
# Automatically triggers: /epic-sync EPIC-001 --fields status

# Sync when features are added
/feature-create "New Feature" epic:EPIC-001
# Automatically triggers: /epic-sync EPIC-001 --fields progress,features
```

### Workflow Automation
```bash
# Setup automated workflows
/epic-sync --config workflow:auto
# Enables:
# - Auto-sync after epic changes
# - Batch sync every 15 minutes
# - Error recovery workflows
# - Stakeholder notifications
```

## Best Practices

1. **Sync Frequency**: Balance between real-time updates and API rate limits
2. **Conflict Strategy**: Choose appropriate resolution strategy per project
3. **Backup Policy**: Always backup before major sync operations
4. **Tool Authority**: Designate primary tool for each data type
5. **Monitor Health**: Regular health checks to identify sync issues early
6. **Error Recovery**: Implement robust retry and recovery mechanisms

This command ensures seamless integration between local epic management and external PM tools, maintaining the **integration-first** philosophy while providing robust synchronization capabilities.