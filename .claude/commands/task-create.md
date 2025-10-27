# Task Create - Start a New Development Task

Create a new task with requirements, acceptance criteria, and optional BDD scenarios.

## ⚠️ CRITICAL: Documentation Only - No Implementation! ⚠️

**This command ONLY creates task documentation files.**

### ❌ DO NOT:
- Implement any code or functionality
- Modify existing source files
- Create new interfaces, classes, or components
- Write tests or test fixtures
- Update dependency injection configurations
- Make any changes beyond creating the task markdown file

### ✅ DO:
- Create the task markdown file in `docs/tasks/`
- Define acceptance criteria and requirements
- Plan the implementation approach
- Document test requirements

**Implementation happens during `/task-work` - NOT HERE!**

---

## Usage
```bash
/task-create <title> [options]
```

## Examples
```bash
# Simple task creation
/task-create "Add user authentication"

# With priority and tags
/task-create "Add user authentication" priority:high tags:[auth,security]

# Link to requirements immediately
/task-create "Add user authentication" requirements:[REQ-001,REQ-002]

# Link to epic for hierarchy and PM tool integration
/task-create "Add user authentication" epic:EPIC-001

# Full specification with epic linking
/task-create "Add user authentication" priority:high epic:EPIC-001 requirements:[REQ-001,REQ-002] bdd:[BDD-001]

# Epic linking with automatic PM tool integration
/task-create "Add user authentication" epic:EPIC-001 export:jira
```

## Task Structure

Creates a markdown file with complete metadata:
```markdown
---
id: TASK-XXX
title: Add user authentication
status: backlog
created: 2024-01-15T10:00:00Z
updated: 2024-01-15T10:00:00Z
priority: high
tags: [auth, security]
epic: EPIC-001
feature: FEAT-003
requirements: [REQ-001, REQ-002]
external_ids:
  epic_jira: PROJ-123
  epic_linear: PROJECT-456
  jira: null        # Populated after export
  linear: null      # Populated after export
bdd_scenarios: [BDD-001]
test_results:
  status: pending
  coverage: null
  last_run: null
---

# Task: Add user authentication

## Description
[Generated from requirements or provided description]

## Acceptance Criteria
- [ ] User can log in with email/password
- [ ] Session tokens are secure (from REQ-001)
- [ ] Failed attempts are rate-limited (from REQ-002)

## Test Requirements
- [ ] Unit tests for authentication service
- [ ] Integration tests for login endpoint
- [ ] E2E tests for complete login flow

## Implementation Notes
[Space for implementation details]

## Test Execution Log
[Automatically populated by /task-work]
```

## Options

### Priority Levels
- `critical` - Must be done immediately
- `high` - Important, do soon
- `normal` - Standard priority (default)
- `low` - Can wait

### Status Values
- `backlog` - Not started (default)
- `in_progress` - Being worked on
- `in_review` - Implementation complete, under review
- `blocked` - Cannot proceed
- `completed` - Done and verified

### Linking Specifications
```bash
# Link requirements during creation
/task-create "Title" requirements:[REQ-001,REQ-002,REQ-003]

# Link BDD scenarios
/task-create "Title" bdd:[BDD-001,BDD-002]

# Link to epic (automatically inherits external tool configuration)
/task-create "Title" epic:EPIC-001

# Link to both epic and feature for hierarchy
/task-create "Title" epic:EPIC-001 feature:FEAT-003

# Export task directly to PM tool (in addition to epic export)
/task-create "Title" epic:EPIC-001 export:[jira,linear]

# Create task with automatic progress tracking setup
/task-create "Title" epic:EPIC-001 feature:FEAT-003 --track-progress

# Create task with quality gate configuration
/task-create "Title" epic:EPIC-001 --quality-gates coverage:90,security:required

# Create task with Agentecflow Stage 3 integration
/task-create "Title" epic:EPIC-001 --agentecflow-stage3
```

## Automatic Enrichment

When requirements and epics are linked, the task is automatically enriched with:
1. **Acceptance criteria** extracted from EARS requirements
2. **Test scenarios** from linked BDD specifications
3. **Priority inference** based on requirement priorities
4. **Suggested tags** from requirement domains
5. **Epic context** including external tool references and stakeholder information
6. **PM tool integration** inherited from linked epic configuration
7. **Feature hierarchy** if feature is specified or inferred from epic
8. **Progress tracking configuration** for automatic rollup to feature and epic
9. **Quality gate setup** based on epic and feature requirements
10. **Agentecflow Stage 3 integration** for implementation workflow tracking

### Example with Requirements and Epic
```bash
/task-create "User login" epic:EPIC-001 requirements:[REQ-001]
```

If REQ-001 states:
> When a user submits valid credentials, the system shall authenticate within 1 second

And EPIC-001 is configured with Jira (PROJ-123) and Linear (PROJECT-456):

The task will include:
- Acceptance criteria: "Authentication completes within 1 second"
- Test requirement: "Performance test for 1-second response time"
- Tag: "performance"
- Epic context: "Part of User Management System (EPIC-001)"
- External tool references: Inherited from epic configuration
- Stakeholder information: Pulled from epic metadata
- Priority alignment: Matches epic priority if not specified

## Task ID Generation

Task IDs follow the pattern: `TASK-XXX`
- Sequential numbering
- Zero-padded to 3 digits minimum
- Unique across the project
- Never reused even if deleted

## File Organization

Tasks are organized by status:
```
tasks/
├── backlog/
│   ├── TASK-001-add-login.md
│   └── TASK-002-reset-password.md
├── in_progress/
│   └── TASK-003-user-profile.md
├── in_review/
│   └── TASK-004-notifications.md
├── blocked/
│   └── TASK-005-oauth-integration.md
└── completed/
    └── 2024-01/
        └── TASK-006-data-export.md
```

## Integration with Workflow

After creation, use the streamlined workflow:
```bash
# 1. Create the task
/task-create "Implement user authentication"
# Output: Created TASK-042

# 2. Work on it (implementation + testing)
/task-work TASK-042 [--mode=standard|tdd|bdd]
# Automatically moves to appropriate state based on test results

# 3. Complete it (after review)
/task-complete TASK-042
# Archives to completed with timestamp
```

## Batch Creation

Create multiple related tasks:
```bash
/task-create-batch epic:USER-MGMT tasks:[
  "Implement login form",
  "Add password reset",
  "Create user profile page",
  "Add session management"
]
```

Creates TASK-XXX through TASK-XXX+3 with shared epic and tags.

## Templates

Use predefined templates for common task types:
```bash
# CRUD operations
/task-create --template=crud entity:Product

# API endpoint
/task-create --template=api-endpoint method:POST path:/api/users

# UI component
/task-create --template=ui-component name:UserProfile
```

## Validation

Tasks are validated before creation:
- ✅ Title must be 5-100 characters
- ✅ No duplicate titles in active tasks
- ✅ Linked requirements must exist
- ✅ Linked BDD scenarios must exist
- ✅ Epic must be valid if specified
- ✅ Feature must belong to specified epic if both are provided
- ✅ Export tools must be configured and accessible

## Best Practices

1. **Clear titles**: Use action verbs ("Implement", "Add", "Fix", "Refactor")
2. **Link specifications**: Always link to requirements for traceability
3. **Set priority**: Helps with sprint planning
4. **Use tags**: Improves discoverability and filtering
5. **Add description**: Provide context beyond the title
6. **⚠️ Respect boundaries**: NEVER implement during task creation - wait for /task-work

## Output Format

### Success
```
✅ Task Created: TASK-042

📋 Task Details
Title: Add user authentication
Priority: high
Status: backlog
Tags: [auth, security]
Epic: EPIC-001 (User Management System)
Feature: FEAT-003 (Authentication Module)

📑 Linked Specifications
Requirements: REQ-001, REQ-002
BDD Scenarios: BDD-001

🔗 External Integration
Epic Context: User Management System
Jira Epic: PROJ-123
Linear Initiative: PROJECT-456
Task Export: Will be created in linked tools

📁 File Location
tasks/backlog/TASK-042-add-user-authentication.md

Next Steps:
1. Review task details (NO IMPLEMENTATION YET)
2. When ready to implement: /task-work TASK-042
3. Track progress: /task-status TASK-042 --hierarchy
4. Auto-sync to PM tools: /task-sync TASK-042
5. Complete task: /task-complete TASK-042

⚠️ Remember: Task is created but NOT implemented. Use /task-work for implementation.
```

### With Warnings
```
✅ Task Created: TASK-042

⚠️ Warnings:
- REQ-003 not found, skipped
- No BDD scenarios linked
- Consider adding test requirements

📋 Task Details
[... rest of output ...]
```

## Error Handling

### Duplicate Title
```
❌ Task creation failed

A task with this title already exists:
- TASK-015: Add user authentication (in_progress)

Suggestions:
- Use a more specific title
- Check if you meant to update TASK-015
```

### Invalid Requirements
```
❌ Task creation failed

Requirements not found:
- REQ-999 does not exist
- REQ-1000 does not exist

Available requirements:
- REQ-001: User login
- REQ-002: Password reset
- REQ-003: Session management
```

## PM Tool Integration

### Epic-Level Integration
When linking tasks to epics, the task automatically inherits:
- **External tool configuration** from the epic
- **Project/workspace mappings** to appropriate PM tools
- **Stakeholder assignments** and notification settings
- **Progress tracking** that rolls up to epic metrics

### Automatic Task Export
```bash
# Task will be created in Jira and Linear if epic is configured for both
/task-create "Implement login" epic:EPIC-001

# Explicit export to specific tools
/task-create "Implement login" epic:EPIC-001 export:jira

# Export to multiple tools
/task-create "Implement login" epic:EPIC-001 export:[jira,linear,github]
```

### Task-to-Story Mapping
Tasks created with epic linking are mapped to external tools as:
- **Jira**: Sub-task of epic or story within epic
- **Linear**: Issue linked to initiative (epic)
- **GitHub**: Issue linked to epic project/milestone
- **Azure DevOps**: Task work item linked to epic work item

### Progress Synchronization
Task progress automatically updates epic progress:
- Task status changes trigger epic sync
- Epic progress calculations include task completion
- External tool progress bars reflect task-level progress
- Stakeholder notifications include task-level updates

## Streamlined Workflow

This command is part of the unified 3-command workflow:
1. `/task-create` - **DOCUMENTATION ONLY** - Creates task file with requirements and epic hierarchy
2. `/task-work` - **IMPLEMENTATION** - Writes code, tests, and modifies files
3. `/task-complete` - **FINALIZATION** - Archives task and syncs progress

**IMPORTANT**: Each command has strict boundaries. Task creation NEVER includes implementation.

The streamlined workflow ensures testing is never skipped and reduces command complexity by 70%.

## Implementation Boundaries

### Clear Separation of Concerns

The task workflow is deliberately separated into distinct phases:

| Command | Purpose | What It Does | What It DOESN'T Do |
|---------|---------|--------------|-------------------|
| `/task-create` | Documentation | Creates task file with requirements | NO code changes, NO file modifications |
| `/task-work` | Implementation | Writes code, creates tests, modifies files | - |
| `/task-complete` | Finalization | Archives task, syncs status | - |

### Examples of Violations

❌ **WRONG - Creating code during task-create:**
```
User: /task-create "Add LoadingEngine"
Assistant: Creating task...
         Creating ILoadingEngine interface... ❌
         Implementing LoadingEngine... ❌
         Writing tests... ❌
```

✅ **CORRECT - Only creating documentation:**
```
User: /task-create "Add LoadingEngine"
Assistant: Creating task TASK-024...
         Created: docs/tasks/TASK-024-add-loadingengine.md

         Next step: Use /task-work TASK-024 to implement
```

### Why This Separation Matters

1. **Predictable Workflow**: Users know exactly what each command will do
2. **Review Opportunity**: Tasks can be reviewed before implementation
3. **Clean Git History**: Task creation is separate from code changes
4. **TDD Compliance**: Implementation via /task-work ensures proper TDD approach

## Enhanced Phase 3 Integration

### Agentecflow Stage 3 Integration
```bash
# Create task optimized for Stage 3: Engineering
/task-create "Implement authentication API" epic:EPIC-001 feature:FEAT-003 --agentecflow-stage3

# Includes:
# - Automatic quality gate configuration
# - Progress tracking for implementation metrics
# - Integration with AI/human collaboration tracking
# - Stage 3 → Stage 4 transition preparation
```

### Complete Task Lifecycle
```bash
# 1. Create task with full hierarchy context
/task-create "User login implementation" epic:EPIC-001 feature:FEAT-003 requirements:[REQ-001]

# 2. Begin implementation with context awareness
/task-work TASK-001 --with-context

# 3. Monitor progress with hierarchy visibility
/task-status TASK-001 --hierarchy

# 4. Sync progress to PM tools and rollup to feature/epic
/task-sync TASK-001 --rollup-progress

# 5. Complete with validation and automatic rollup
/task-complete TASK-001
```

### Quality Gates and Progress Tracking
```bash
# Create task with enhanced quality requirements
/task-create "Payment processing" epic:EPIC-002 --quality-gates coverage:95,performance:200ms,security:required

# Progress automatically rolls up:
# Task Progress → Feature Progress → Epic Progress → Portfolio Progress
```

## Integration with Epic Management Commands

### Workflow Integration
```bash
# Create epic first
/epic-create "User Management" export:jira

# Create features for the epic
/feature-create "Authentication" epic:EPIC-001

# Create tasks for features (enhanced with Phase 3 capabilities)
/task-create "Implement login" epic:EPIC-001 feature:FEAT-001 --track-progress

# Work on task (automatically updates epic progress)
/task-work TASK-001 --sync-progress

# Progress is visible in epic status with full hierarchy
/epic-status EPIC-001 --hierarchy
```

### Cross-Command References
- Tasks link to epics and features for complete hierarchy
- Epic progress automatically calculated from task completion
- Task completion triggers epic sync to external tools
- External tool IDs are preserved throughout the workflow
- Real-time progress rollup across all hierarchy levels
- Agentecflow Stage 3 metrics tracked and synchronized
