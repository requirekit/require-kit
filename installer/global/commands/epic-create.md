# Epic Create - Define Business Initiative for PM Tool Integration

Create a business epic with requirements and export it to external project management tools (Jira, Linear, Azure DevOps, GitHub Projects).

## Usage
```bash
/epic-create <title> [options]
```

## Examples
```bash
# Simple epic creation
/epic-create "User Management System"

# With business context and PM tool export
/epic-create "User Management System" priority:high quarter:Q1-2024 export:jira

# With stakeholders and timeline
/epic-create "Payment Processing" stakeholder:"Product Team" timeline:8weeks export:linear

# Link to project requirements
/epic-create "Mobile App Redesign" requirements:[REQ-001,REQ-002] export:github
```

## Epic Structure (Optimized for PM Tool Export)

Creates a lightweight epic definition designed for external tool integration:

```markdown
---
id: EPIC-XXX
title: User Management System
status: planning
created: 2024-01-15T10:00:00Z
updated: 2024-01-15T10:00:00Z
priority: high
quarter: Q1-2024
stakeholder: Product Team
estimated_weeks: 6
export_config:
  target_tools: [jira, linear]
  jira_project: "PROJ"
  linear_team: "engineering"
  auto_sync: true
external_ids:
  jira: null      # Populated after export
  linear: null    # Populated after export
  github: null    # Populated after export
requirements: [REQ-001, REQ-002]
---

# Epic: User Management System

## Business Objective
[High-level business goal this epic achieves]

## Success Criteria
- [ ] [Measurable business outcome 1]
- [ ] [Measurable business outcome 2]
- [ ] [Measurable business outcome 3]

## Scope
### In Scope
- [What this epic includes]
- [Key capabilities to be delivered]

### Out of Scope
- [What this epic explicitly does not include]
- [Deferred capabilities]

## Stakeholders
- **Product Owner**: [Name]
- **Engineering Lead**: [Name]
- **Design Lead**: [Name]

## Timeline
- **Target Quarter**: Q1-2024
- **Estimated Duration**: 6 weeks
- **Key Milestones**:
  - [ ] Week 2: Feature breakdown complete
  - [ ] Week 4: Core features implemented
  - [ ] Week 6: Epic complete and validated

## Dependencies
- [Other epics or external dependencies]
- [Blocked by / Blocking relationships]

## Export Status
- **Last Synced**: [Timestamp]
- **External Links**:
  - Jira Epic: [Auto-populated after export]
  - Linear Initiative: [Auto-populated after export]
  - GitHub Project: [Auto-populated after export]

## Feature Breakdown
[This will be populated by /feature-create commands]

## Implementation Notes
[Technical considerations or architecture decisions]
```

## Export Integration Options

### Target PM Tools
- **Jira**: Creates Epic issue type with proper linking
- **Linear**: Creates Initiative with team assignment
- **Azure DevOps**: Creates Epic work item with area path
- **GitHub Projects**: Creates Epic item with milestone linking

### Export Configuration
```bash
# Configure default export target
/epic-create "Title" export:jira project:MYPROJ

# Export to multiple tools
/epic-create "Title" export:[jira,linear,github]

# Set up auto-sync
/epic-create "Title" export:linear auto-sync:true
```

## PM Tool Mapping

### Jira Integration
```yaml
epic_mapping:
  title: → Summary
  description: → Description
  priority: → Priority
  stakeholder: → Reporter
  timeline: → Target Resolution
  requirements: → Links (implements)
  quarter: → Fix Version
```

### Linear Integration
```yaml
epic_mapping:
  title: → Title
  description: → Description
  priority: → Priority (1-4 scale)
  stakeholder: → Assignee
  timeline: → Target Date
  quarter: → Milestone
```

### GitHub Projects Integration
```yaml
epic_mapping:
  title: → Title
  description: → Body
  priority: → Priority Label
  timeline: → Milestone
  requirements: → Linked Issues
```

## Options

### Priority Levels (PM Tool Compatible)
- `critical` - P0/Highest (maps to tool equivalents)
- `high` - P1/High
- `normal` - P2/Medium (default)
- `low` - P3/Low

### Timeline Estimation
- `timeline:Xweeks` - Duration estimate
- `quarter:Q1-2024` - Target quarter
- `deadline:2024-03-15` - Hard deadline

### Export Targets
- `export:jira` - Export to Jira
- `export:linear` - Export to Linear
- `export:azure` - Export to Azure DevOps
- `export:github` - Export to GitHub Projects
- `export:[tool1,tool2]` - Multi-tool export

## Automatic Export Process

When an epic is created with export options:

1. **Validate Target Tool Access**
   - Check API credentials
   - Verify project/workspace access
   - Validate required fields

2. **Create External Epic**
   - Map epic fields to tool format
   - Create epic in target tool(s)
   - Store external ID in epic metadata

3. **Setup Sync Configuration**
   - Configure webhook listeners (if supported)
   - Schedule periodic sync checks
   - Enable bidirectional updates

4. **Link Local and Remote**
   - Update epic with external URLs
   - Create reference mapping
   - Enable status synchronization

## Output Format

### Success with Export
```
✅ Epic Created: EPIC-042

📋 Epic Details
Title: User Management System
Priority: high
Quarter: Q1-2024
Estimated Duration: 6 weeks

🔗 External Integration
Target Tools: Jira, Linear
Export Status: ✅ Completed

📑 Created External Items
Jira Epic: PROJ-123
  URL: https://company.atlassian.net/browse/PROJ-123
Linear Initiative: PROJECT-456
  URL: https://linear.app/company/initiative/PROJECT-456

📁 Local File
docs/epics/EPIC-042-user-management-system.md

Next Steps:
1. Define features: /feature-create "Feature Name" epic:EPIC-042
2. View status: /epic-status EPIC-042
3. Sync updates: /epic-sync EPIC-042
```

### Local Only Creation
```
✅ Epic Created: EPIC-042

📋 Epic Details
Title: User Management System
Priority: high
Status: planning

📁 Local File
docs/epics/EPIC-042-user-management-system.md

💡 Integration Available
Export to PM tools: /epic-sync EPIC-042 --export jira
Configure auto-sync: /epic-sync EPIC-042 --setup

Next Steps:
1. Export to PM tool: /epic-sync EPIC-042 --export [tool]
2. Define features: /feature-create "Feature Name" epic:EPIC-042
```

## Validation

Epics are validated before creation:
- ✅ Title must be 10-100 characters
- ✅ No duplicate titles in active epics
- ✅ Valid priority level
- ✅ PM tool credentials (if exporting)
- ✅ Timeline format validation
- ✅ Linked requirements must exist

## File Organization

```
docs/
├── epics/
│   ├── active/
│   │   ├── EPIC-001-user-management.md
│   │   └── EPIC-002-payment-system.md
│   ├── completed/
│   │   └── 2024-Q1/
│   │       └── EPIC-003-mobile-redesign.md
│   └── cancelled/
│       └── EPIC-004-legacy-migration.md
```

## Integration with Existing Commands

### Enhanced Task Linking
```bash
# Note: Task execution requires guardkit integration
# See INTEGRATION-GUIDE.md for setup

# Tasks can link to epics (guardkit)
# /task-create "Login implementation" epic:EPIC-001

# Epic information flows down to tasks
# External epic IDs automatically linked in task exports
```

### Requirements Connection
```bash
# Epics can link to project requirements
/epic-create "Title" requirements:[REQ-001,REQ-002]

# Feature requirements will inherit epic context
```

## Best Practices for PM Tool Integration

1. **Start with Local Definition**: Create epic locally first, then export
2. **Single Source of Truth**: Choose primary PM tool for status updates
3. **Bidirectional Sync**: Keep local and remote in sync
4. **Minimal Local State**: Don't duplicate PM tool functionality
5. **Export Early**: Export to PM tools as soon as epic is defined

## Configuration Required

### PM Tool Setup
```bash
# Configure Jira integration
/pm-config jira --url https://company.atlassian.net --token YOUR_TOKEN --project PROJ

# Configure Linear integration
/pm-config linear --token YOUR_TOKEN --team engineering

# Configure GitHub integration
/pm-config github --token YOUR_TOKEN --org company --project ai-engineer
```

## Future MCP Integration Points

When MCP servers become available:
- **Automatic Sync**: Real-time bidirectional synchronization
- **Status Updates**: Epic status changes flow between tools
- **Notification Integration**: Slack/Teams notifications on epic changes
- **Reporting**: Cross-tool epic progress reporting

This epic management focuses on **integration and export** rather than building a local PM system, positioning the Agentic Flow as a **requirements-to-PM-tool bridge** that enhances existing workflows.