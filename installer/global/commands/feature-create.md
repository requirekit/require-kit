# Feature Create - Bridge Epic Requirements to Implementation Tasks

Create features that decompose epics into implementable units with EARS requirements, BDD scenarios, and automatic task generation for external PM tool integration.

## Usage
```bash
/feature-create <title> epic:<epic-id> [options]
```

## Examples
```bash
# Simple feature creation within an epic
/feature-create "User Authentication" epic:EPIC-001

# With requirements and BDD scenarios
/feature-create "User Authentication" epic:EPIC-001 requirements:[REQ-001,REQ-002] bdd:[BDD-001]

# With priority and timeline
/feature-create "User Authentication" epic:EPIC-001 priority:high timeline:2weeks

# Full specification with PM tool export
/feature-create "User Authentication" epic:EPIC-001 priority:high requirements:[REQ-001,REQ-002] export:jira

# Auto-generate tasks from requirements
/feature-create "User Authentication" epic:EPIC-001 requirements:[REQ-001,REQ-002] auto-tasks:true
```

## Feature Structure

Creates a comprehensive feature definition optimized for requirements management and external PM tool integration:

```markdown
---
id: FEAT-XXX
title: User Authentication
epic: EPIC-001
status: planning
created: 2024-01-15T10:00:00Z
updated: 2024-01-15T10:00:00Z
priority: high
timeline: 2weeks
complexity: medium
requirements: [REQ-001, REQ-002, REQ-003]
bdd_scenarios: [BDD-001, BDD-002]
acceptance_criteria: [AC-001, AC-002]
external_ids:
  epic_jira: PROJ-123
  epic_linear: PROJECT-456
  jira: null         # Populated after export as Story/Feature
  linear: null       # Populated after export as Feature
  github: null       # Populated after export as Issue/Feature
progress:
  tasks_planned: 0
  tasks_completed: 0
  coverage_target: 85
  performance_target: "<200ms"
stakeholders:
  product_owner: "Sarah Chen"
  tech_lead: "Mike Johnson"
  designer: "Lisa Park"
export_config:
  target_tools: [jira, linear]
  auto_task_creation: true
  sync_enabled: true
---

# Feature: User Authentication

## Business Value
[High-level value this feature delivers to users/business]

## Scope Definition
### In Scope
- [ ] User login with email/password
- [ ] Session management
- [ ] Password reset functionality
- [ ] Basic user profile

### Out of Scope
- [ ] Social media authentication
- [ ] Two-factor authentication
- [ ] Advanced user permissions

## Requirements Traceability
- **REQ-001**: User login authentication (EARS: When user submits valid credentials, system shall authenticate within 1 second)
- **REQ-002**: Session security (EARS: The system shall maintain secure sessions for 24 hours)
- **REQ-003**: Password validation (EARS: The system shall enforce password complexity rules)

## Acceptance Criteria
- **AC-001**: User can log in with valid email/password
- **AC-002**: Invalid credentials show appropriate error message
- **AC-003**: Session expires after 24 hours of inactivity
- **AC-004**: Password must meet complexity requirements

## BDD Scenarios
- **BDD-001**: Successful user login flow
- **BDD-002**: Failed login attempt handling
- **BDD-003**: Session timeout behavior

## Implementation Tasks
[Auto-generated from requirements or manually defined]
- [ ] TASK-XXX: Design authentication UI
- [ ] TASK-XXX: Implement login API endpoint
- [ ] TASK-XXX: Add session management
- [ ] TASK-XXX: Create password reset flow

## Technical Considerations
### Architecture Decisions
- Authentication strategy: JWT tokens
- Session storage: Redis
- Password hashing: bcrypt with salt

### Dependencies
- Database schema updates required
- API endpoints: /auth/login, /auth/logout, /auth/reset
- UI components: LoginForm, PasswordReset

### Performance Requirements
- Login response time: <200ms
- Session validation: <50ms
- Password reset: <1s

## Test Strategy
### Unit Tests
- Authentication service methods
- JWT token validation
- Password hashing utilities

### Integration Tests
- Login API endpoint
- Session management middleware
- Database authentication queries

### E2E Tests
- Complete login flow
- Password reset workflow
- Session timeout behavior

## Design Assets
[Links to Figma designs, wireframes, or UI mockups]
- Login form design: [Figma Link]
- Error state designs: [Figma Link]
- Mobile responsive layouts: [Figma Link]

## Progress Tracking
### Definition of Done
- [ ] All acceptance criteria met
- [ ] Code reviewed and approved
- [ ] Unit tests ≥85% coverage
- [ ] Integration tests passing
- [ ] E2E tests passing
- [ ] Performance requirements met
- [ ] Security review completed
- [ ] Documentation updated

### External Tool Integration
- **Jira Epic**: PROJ-123 (User Management)
- **Linear Initiative**: PROJECT-456 (Q1 User Features)
- **GitHub Milestone**: User-Auth-Sprint-1

## Risk Assessment
### High Risk
- [ ] Third-party authentication service dependency

### Medium Risk
- [ ] Database migration complexity
- [ ] Cross-browser compatibility

### Low Risk
- [ ] UI component library integration

## Change Log
[Automatically maintained during feature lifecycle]
```

## Feature-Epic-Task Hierarchy

Features bridge the gap between business epics and implementation tasks:

```
EPIC-001: User Management System
├── FEAT-001: User Authentication
│   ├── TASK-001: Design login UI
│   ├── TASK-002: Implement auth API
│   └── TASK-003: Add session management
├── FEAT-002: User Profile Management
│   ├── TASK-004: Create profile form
│   └── TASK-005: Add avatar upload
└── FEAT-003: User Permissions
    ├── TASK-006: Implement RBAC
    └── TASK-007: Add admin dashboard
```

## Automatic Task Generation

When `auto-tasks:true` is specified, features automatically generate implementation tasks:

```bash
/feature-create "User Authentication" epic:EPIC-001 requirements:[REQ-001,REQ-002] auto-tasks:true

# Automatically creates:
# TASK-XXX: Implement login form (from REQ-001)
# TASK-XXX: Add session management (from REQ-002)
# TASK-XXX: Create authentication tests
# TASK-XXX: Design authentication UI
```

### Task Generation Rules
1. **From EARS Requirements**: Each requirement generates 1-2 implementation tasks
2. **From BDD Scenarios**: Each scenario generates testing tasks
3. **From Acceptance Criteria**: Complex criteria generate multiple tasks
4. **Standard Tasks**: UI, API, Tests, Documentation automatically added

## PM Tool Integration

### Feature Mapping to External Tools

#### Jira Integration
```yaml
feature_mapping:
  title: → Summary (Story/Feature level)
  description: → Description
  epic: → Epic Link
  acceptance_criteria: → Acceptance Criteria field
  tasks: → Sub-tasks or Stories
  priority: → Priority
  timeline: → Sprint assignment
```

#### Linear Integration
```yaml
feature_mapping:
  title: → Title (Feature level)
  description: → Description
  epic: → Initiative link
  acceptance_criteria: → Description section
  tasks: → Child issues
  priority: → Priority (1-4 scale)
  timeline: → Target date
```

#### GitHub Projects Integration
```yaml
feature_mapping:
  title: → Issue title
  description: → Issue body
  epic: → Milestone/Project link
  acceptance_criteria: → Checklist in description
  tasks: → Linked issues
  priority: → Priority label
```

## Options

### Priority Levels
- `critical` - Blocking epic progress
- `high` - Important for epic success
- `normal` - Standard feature priority (default)
- `low` - Nice to have feature

### Complexity Estimation
- `simple` - 1-3 tasks, 1-2 days
- `medium` - 4-8 tasks, 3-5 days (default)
- `complex` - 9+ tasks, 1-2 weeks

### Timeline Options
- `timeline:Xdays` - Duration in days
- `timeline:Xweeks` - Duration in weeks
- `sprint:X` - Target sprint number
- `deadline:YYYY-MM-DD` - Hard deadline

## Workflow Integration

Features bridge requirements and implementation:

### Review and Approval Workflow
```bash
# Create feature for review
/feature-create "User Authentication" epic:EPIC-001 requirements:[REQ-001,REQ-002]

# Review and approve feature specification
# (Checkpoint: Does feature match expectations?)

# Generate task specifications automatically after approval
/feature-generate-tasks FEAT-001  # Works with or without taskwright

# Review generated tasks
# (Checkpoint: Are tasks appropriate?)

# Export to PM tools after approval
/feature-sync FEAT-001 --export
```

### Requirements to Implementation Bridge
Features provide the critical connection from requirements to implementation:

1. **Requirements Input**: EARS notation from requirements gathering
2. **Feature Definition**: Breakdown into implementable units
3. **Task Generation**: Concrete implementation tasks (optional, via taskwright)
4. **PM Tool Export**: Integration with project management systems
5. **Implementation**: Tasks ready for execution in any workflow system

## Validation

Features are validated before creation:
- ✅ Title must be 10-80 characters
- ✅ Epic must exist and be active
- ✅ No duplicate feature titles within epic
- ✅ Linked requirements must exist
- ✅ Linked BDD scenarios must exist
- ✅ Timeline must be realistic for complexity
- ✅ PM tool credentials valid if exporting

## Output Format

### Success with Auto-Tasks
```
✅ Feature Created: FEAT-042

📋 Feature Details
Title: User Authentication
Epic: EPIC-001 (User Management System)
Priority: high
Timeline: 2 weeks
Complexity: medium

📑 Linked Specifications
Requirements: REQ-001, REQ-002, REQ-003
BDD Scenarios: BDD-001, BDD-002
Acceptance Criteria: 4 criteria defined

🔗 External Integration
Epic Context: User Management System
Jira Epic: PROJ-123
Linear Initiative: PROJECT-456

🎯 Auto-Generated Tasks (5)
✅ TASK-043: Design authentication UI
✅ TASK-044: Implement login API endpoint
✅ TASK-045: Add session management
✅ TASK-046: Create password reset flow
✅ TASK-047: Implement authentication tests

📁 File Location
docs/features/FEAT-042-user-authentication.md

📊 Progress Dashboard
Tasks: 0/5 completed (0%)
Target Coverage: 85%
Performance Target: <200ms

Next Steps:
1. Review feature specification
2. Begin implementation with your workflow or taskwright integration
3. Track progress: /feature-status FEAT-042
4. Sync to PM tools: /feature-sync FEAT-042
```

### Integration Example
```
🔄 Integration Active

📋 Feature Specification Complete
✅ Feature specification created
✅ Requirements traceability established
✅ Acceptance criteria defined
✅ BDD scenarios linked
✅ Implementation tasks generated

🔗 External Tool Sync
✅ Jira: Feature story PROJ-124 created
✅ Linear: Feature PROJECT-457 created
📋 GitHub: Ready for issue export

🎯 Ready for Implementation
All tasks ready for execution in any workflow system
Checkpoint: Proceed with implementation?
```

## File Organization

```
docs/
├── features/
│   ├── active/
│   │   ├── FEAT-001-user-authentication.md
│   │   └── FEAT-002-user-profile.md
│   ├── in_progress/
│   │   └── FEAT-003-user-permissions.md
│   ├── completed/
│   │   └── 2024-Q1/
│   │       └── FEAT-004-user-registration.md
│   └── cancelled/
│       └── FEAT-005-social-auth.md
```

## Best Practices

1. **Epic Alignment**: Features must clearly contribute to epic objectives
2. **Scope Management**: Keep features focused and implementable in 1-2 weeks
3. **Requirements Traceability**: Always link to EARS requirements
4. **Acceptance Criteria**: Define clear, testable success criteria
5. **Task Granularity**: Auto-generated tasks should be 1-3 days of work
6. **PM Tool Integration**: Export early and sync frequently
7. **Human Checkpoints**: Review before task generation and implementation

This feature management system provides the critical bridge between business requirements and implementation tasks while maintaining full integration with external PM tools. For task execution, consider integrating with [taskwright](https://github.com/taskwright-dev/taskwright).