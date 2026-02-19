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

# Create epic with direct task pattern (no intermediate features)
/epic-create "Fix Auth Bugs" --pattern direct

# Create epic with explicit features pattern (default)
/epic-create "User Management System" --pattern features priority:high

# Create epic with mixed pattern (features + direct tasks)
/epic-create "Platform Upgrade" --pattern mixed
```

## Clarifying Questions (Interactive Mode)

When creating an epic interactively, the following questions help ensure a well-scoped epic:

### 1. Scope Boundary
```
What is explicitly OUT OF SCOPE for this epic?
[Helps prevent scope creep and sets clear boundaries]

Examples:
- "Mobile app support (web only for now)"
- "Third-party integrations"
- "Advanced analytics"
```

### 2. Success Criteria
```
What measurable outcomes define success for this epic?
[Provide 2-3 specific, measurable criteria]

Examples:
- "User registration rate increases by 20%"
- "Page load time under 2 seconds"
- "Zero critical security vulnerabilities"
```

### 3. Stakeholders
```
Who are the key stakeholders for this epic?

- Product Owner: [Name or role]
- Engineering Lead: [Name or role]
- Design Lead: [Name or role]
- Other: [Name/role if applicable]
```

### 4. Timeline Constraints
```
Are there timeline constraints or dependencies?

Options:
- Quarter target (e.g., "Q1-2024")
- Specific deadline (e.g., "2024-03-15")
- Dependency (e.g., "After EPIC-002 completes")
- Flexible (no hard constraints)
```

### 5. PM Tool Export (Optional)
```
Should this epic sync to external PM tools?

Options:
- Jira (project key: ___)
- Linear (team: ___)
- GitHub Projects (repo: ___)
- Azure DevOps (project: ___)
- None (local only)
```

### Skipping Clarification

For quick epic creation without clarification:
```bash
# Direct creation with all parameters
/epic-create "Title" priority:high quarter:Q1-2024 stakeholder:"Team Lead"

# Or use --quick flag to skip questions
/epic-create "Title" --quick
```

### Clarification Output

Answers are stored in the epic frontmatter:
```yaml
clarification:
  out_of_scope: ["Mobile support", "Third-party integrations"]
  success_criteria:
    - "User registration +20%"
    - "Page load <2s"
  stakeholders:
    product_owner: "Sarah Chen"
    engineering_lead: "Mike Johnson"
  timeline: "Q1-2024"
  pm_tools: ["jira"]
```

## Process

When creating an epic:

1. **Clarification** (interactive mode): Answer scoping questions to define boundaries, success criteria, stakeholders, and timeline
2. **Pattern Selection**: Determine organisation pattern (`direct`, `features`, or `mixed`). Defaults to `features` if not specified
3. **Validation**: Verify epic structure, check for duplicates, validate PM tool credentials, and validate organisation_pattern value
4. **Creation**: Generate epic file with frontmatter and structured content (markdown always saved regardless of downstream steps)
5. **Graphiti Push** (if enabled): Push epic episode to Graphiti knowledge graph. This step uses graceful degradation — if Graphiti is unavailable or not configured, the epic markdown is still saved and creation succeeds. Sync status is displayed in output
6. **Export** (optional): Sync to configured PM tools with bidirectional linking

For quick creation without clarification, use the `--quick` flag or provide all parameters directly.

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
organisation_pattern: features
direct_tasks: []
graphiti_synced: false
last_graphiti_sync: null
completeness_score: 0
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

## Organisation Patterns

Epics support three organisation patterns that control how work is structured beneath them. The pattern is set at creation time via the `--pattern` flag and stored in the `organisation_pattern` frontmatter field.

### Pattern: `direct` — EPIC → TASK

Use the direct pattern for small epics with 3-5 tasks where an intermediate feature layer adds unnecessary ceremony.

**When to use**:
- Small epics with 3-5 tasks
- Bug fix epics grouping related fixes
- Technical debt or cleanup work
- Research spikes and investigative work
- Infrastructure and deployment tasks
- Solo developer workflows

**Example**:
```
EPIC-002: Fix Auth Bugs
  └── TASK-004: Debug session timeout
  └── TASK-005: Fix password reset
  └── TASK-006: Update tests
```

**Creation**:
```bash
/epic-create "Fix Auth Bugs" --pattern direct
```

### Pattern: `features` (Default) — EPIC → FEATURE → TASK

The features pattern is the default and provides backward compatible behaviour. Use it for large epics requiring team coordination and requirements traceability.

**When to use**:
- Large epics with 10+ tasks
- Customer-facing capabilities
- Natural groupings with clear feature boundaries
- Team coordination with 3+ developers
- Requirements traceability to EARS requirements
- Multi-sprint initiatives
- PM tool reporting at feature level

**Example**:
```
EPIC-001: User Management
  └── FEAT-001: Authentication
        └── TASK-001: Implement login
        └── TASK-002: Add session handling
  └── FEAT-002: Profile Management
        └── TASK-003: Create profile form
        └── TASK-004: Add avatar upload
```

**Creation**:
```bash
/epic-create "User Management System"  # defaults to features
/epic-create "User Management System" --pattern features
```

### Pattern: `mixed` — Both Features and Direct Tasks

The mixed pattern allows an epic to contain both features and direct tasks. This suits evolving epics where structured feature work coexists with miscellaneous tasks (documentation, deployment, testing).

⚠️ **Warning**: Selecting the mixed pattern produces a warning encouraging consistency. Consider whether all tasks should be grouped under features or whether the epic should use the direct pattern instead.

**When to use**:
- Epic has structured features for main work plus miscellaneous tasks
- Evolving epics transitioning between patterns
- Epics where some work doesn't fit neatly into a feature

**Example**:
```
EPIC-003: Platform Upgrade
├── FEAT-001: UI Redesign
│   ├── TASK-001: Update components
│   └── TASK-002: Redesign dashboard
├── FEAT-002: API Modernization
│   ├── TASK-003: Migrate to GraphQL
│   └── TASK-004: Add rate limiting
└── [Direct Tasks]
    ├── TASK-005: Update documentation
    └── TASK-006: Deploy to staging
```

**Creation**:
```bash
/epic-create "Platform Upgrade" --pattern mixed
```

### Pattern Selection Guidance

| Criteria | `direct` | `features` | `mixed` |
|---|---|---|---|
| Task count | 3-5 tasks | 10+ tasks | Varies |
| Team size | Solo / small | 3+ developers | Any |
| Epic type | Bug fixes, tech debt, spikes | Customer-facing, complex | Evolving |
| Traceability | Task → Epic | Task → Feature → Epic | Both paths |
| PM tool mapping | Epic → Story | Epic → Story → Sub-task | Both mappings |

### PM Tool Mapping by Pattern

#### Direct Pattern (EPIC → TASK)
```yaml
# Jira: Epic → Story (task promoted to story level)
# Linear: Initiative → Issue
# GitHub: Milestone → Issue
direct_pattern_mapping:
  jira:
    epic: Epic
    task: Story
  linear:
    epic: Initiative
    task: Issue
  github:
    epic: Milestone
    task: Issue
```

#### Features Pattern (EPIC → FEATURE → TASK)
```yaml
# Jira: Epic → Story (feature) → Sub-task (task)
# Linear: Initiative → Feature → Issue
# GitHub: Milestone → Issue (feature) → Linked Issue (task)
features_pattern_mapping:
  jira:
    epic: Epic
    feature: Story
    task: Sub-task
  linear:
    epic: Initiative
    feature: Feature
    task: Issue
  github:
    epic: Milestone
    feature: Issue
    task: Linked Issue
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

### Organisation Pattern
- `--pattern direct` - Epic → Task (small epics, 3-5 tasks)
- `--pattern features` - Epic → Feature → Task (default, large epics)
- `--pattern mixed` - Both features and direct tasks (evolving epics)

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
Organisation Pattern: features

🧠 Graphiti Sync
Status: ✅ Synced (or ⚠️ Skipped — Graphiti not configured)

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
- ✅ Valid organisation_pattern must be one of: `direct`, `features`, `mixed`
- ⚠️ Mixed pattern selection produces a warning suggesting consistent organisation

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