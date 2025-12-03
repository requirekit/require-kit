# require-kit Command Usage Guide

**Version**: 1.0.0
**Last Updated**: 2025-11-03

## Table of Contents

1. [Quick Command Reference](#quick-command-reference)
2. [Requirements Management Commands](#requirements-management-commands)
3. [Epic Management Commands](#epic-management-commands)
4. [Feature Management Commands](#feature-management-commands)
5. [Hierarchy Commands](#hierarchy-commands)
6. [Export and Integration Commands](#export-and-integration-commands)
7. [Complete Workflow Examples](#complete-workflow-examples)

---

## Quick Command Reference

### Requirements Commands
| Command | Purpose | Example |
|---------|---------|---------|
| `/gather-requirements` | Interactive requirements gathering | `/gather-requirements user-auth` |
| `/formalize-ears` | Convert to EARS notation | `/formalize-ears draft/auth.md` |
| `/generate-bdd` | Create Gherkin scenarios | `/generate-bdd REQ-001` |

### Epic Management Commands
| Command | Purpose | Example |
|---------|---------|---------|
| `/epic-create` | Create strategic epic | `/epic-create "User Management"` |
| `/epic-status` | View epic progress | `/epic-status EPIC-001` |
| `/epic-sync` | Sync with PM tools | `/epic-sync EPIC-001 --jira` |

### Feature Management Commands
| Command | Purpose | Example |
|---------|---------|---------|
| `/feature-create` | Create feature with epic linkage | `/feature-create "Auth" epic:EPIC-001` |
| `/feature-status` | View feature progress | `/feature-status FEAT-001` |
| `/feature-sync` | Sync feature with PM tools | `/feature-sync FEAT-001 --jira` |
| `/feature-generate-tasks` | Generate task specifications | `/feature-generate-tasks FEAT-001` |

### Hierarchy Commands
| Command | Purpose | Example |
|---------|---------|---------|
| `/hierarchy-view` | View project hierarchy | `/hierarchy-view EPIC-001` |

---

## Requirements Management Commands

### `/gather-requirements` - Interactive Requirements Gathering

**Purpose**: Conduct guided Q&A sessions to capture complete requirements.

**Basic Usage:**
```bash
/gather-requirements
```

**With Feature Name:**
```bash
/gather-requirements user-authentication
```

**With Context:**
```bash
/gather-requirements user-authentication --context="Web application for healthcare"
```

**Output:**
```
✅ Requirements Gathering Complete

Captured Requirements:
- Functional: 12 items
- Non-Functional: 5 items
- Security: 4 items
- Performance: 3 items

Output File: docs/requirements/draft/user-authentication.md

Next Steps:
1. Review captured requirements
2. Formalize with /formalize-ears
3. Generate BDD with /generate-bdd
```

**Question Categories:**
- Problem Definition
- User Roles and Personas
- Functional Behavior
- Error Handling
- Performance Requirements
- Security Constraints
- Compliance Needs
- Integration Points
- Future Considerations

### `/formalize-ears` - Convert to EARS Notation

**Purpose**: Transform natural language requirements into structured EARS notation.

**Basic Usage:**
```bash
/formalize-ears
```

**From Specific File:**
```bash
/formalize-ears docs/requirements/draft/user-authentication.md
```

**With Validation:**
```bash
/formalize-ears --validate --strict
```

**Output:**
```
✅ EARS Formalization Complete

Generated Requirements:
- Ubiquitous: 3 requirements
- Event-Driven: 5 requirements
- State-Driven: 4 requirements
- Unwanted Behavior: 3 requirements
- Optional Feature: 2 requirements

Total: 17 EARS requirements

Files Created:
- docs/requirements/REQ-001.md through REQ-017.md

Validation Results:
✅ All requirements are atomic
✅ All requirements are testable
✅ All requirements have measurable criteria
✅ No conflicts detected
✅ Coverage complete

Next Steps:
1. Review generated EARS requirements
2. Generate BDD scenarios: /generate-bdd
```

**EARS Patterns:**

1. **Ubiquitous**: `The [system] shall [behavior]`
```
REQ-001: The system shall encrypt all passwords using bcrypt with cost factor 12.
```

2. **Event-Driven**: `When [trigger], the [system] shall [response]`
```
REQ-002: When a user submits valid credentials, the system shall authenticate
         within 1 second and redirect to the dashboard.
```

3. **State-Driven**: `While [state], the [system] shall [behavior]`
```
REQ-003: While a user session is active, the system shall validate the session
         token on each request.
```

4. **Unwanted Behavior**: `If [error], then the [system] shall [recovery]`
```
REQ-004: If authentication fails 3 times within 5 minutes, then the system shall
         lock the account for 15 minutes and send a security alert email.
```

5. **Optional Feature**: `Where [feature], the [system] shall [behavior]`
```
REQ-005: Where the user has selected "Remember Me", the system shall maintain
         the session for 30 days with automatic token refresh.
```

### `/generate-bdd` - Create BDD/Gherkin Scenarios

**Purpose**: Generate testable Gherkin scenarios from EARS requirements.

**Basic Usage:**
```bash
/generate-bdd
```

**For Specific Requirement:**
```bash
/generate-bdd REQ-001
```

**For Feature:**
```bash
/generate-bdd --feature FEAT-001
```

**For Epic:**
```bash
/generate-bdd --epic EPIC-001
```

**Output:**
```
✅ BDD Generation Complete

Generated Scenarios:
- Feature: User Authentication
  - 8 scenarios (6 positive, 2 negative)
  - Coverage: REQ-001 through REQ-005

Files Created:
- docs/bdd/BDD-001-user-authentication.feature

Scenario Types:
✅ Happy Path: 4 scenarios
✅ Error Handling: 2 scenarios
✅ Performance: 1 scenario
✅ Security: 1 scenario

Tags Applied:
@requirement-REQ-XXX (links to requirements)
@epic-EPIC-001 (links to epic)
@feature-FEAT-001 (links to feature)
@smoke, @critical (test priority)

Next Steps:
1. Review generated scenarios with stakeholders
2. Export to test framework
3. Link to features: /feature-create with bdd:[BDD-001]
```

**Example Generated Scenario:**
```gherkin
@epic-EPIC-001 @feature-FEAT-001 @requirement-REQ-002
Scenario: Successful user login
  Given a registered user with email "user@example.com"
  And the user's password is "Valid123!"
  When the user submits the login form
  Then the user should be authenticated
  And the user should be redirected to "/dashboard"
  And a session cookie should be created
  And the authentication should complete within 1 second
```

---

## Epic Management Commands

### `/epic-create` - Create Strategic Epic

**Purpose**: Create a new epic representing a strategic initiative or major feature area.

**Basic Usage:**
```bash
/epic-create "User Management System"
```

**With Metadata:**
```bash
/epic-create "User Management System" \
  priority:high \
  business_value:8 \
  effort_estimate:21 \
  stakeholders:[pm@company.com,lead@company.com]
```

**With PM Tool Integration:**
```bash
/epic-create "User Management System" \
  priority:high \
  export:[jira,linear]
```

**Output:**
```
✅ Epic Created: EPIC-001

📋 Epic Details
Title: User Management System
Priority: high
Business Value: 8/10
Effort Estimate: 21 story points
Status: active

👥 Stakeholders
Product Owner: pm@company.com
Tech Lead: lead@company.com

🔗 External Integration
Jira Epic: PROJ-123 (created)
Linear Initiative: PROJECT-456 (created)

📁 File Location
docs/epics/EPIC-001-user-management-system.md

Next Steps:
1. Create features: /feature-create "Feature Name" epic:EPIC-001
2. Monitor progress: /epic-status EPIC-001
3. View hierarchy: /hierarchy-view EPIC-001
```

### `/epic-status` - View Epic Progress

**Purpose**: Monitor epic progress including feature rollup and completion metrics.

**Basic Status:**
```bash
/epic-status EPIC-001
```

**With Hierarchy:**
```bash
/epic-status EPIC-001 --hierarchy
```

**With Detailed Metrics:**
```bash
/epic-status EPIC-001 --detailed --include-bdd
```

**Output:**
```
📊 Epic Status: EPIC-001 - User Management System

🎯 Overview
Status: active
Progress: 63% complete (5/8 features completed)
Timeline: On track (3 days ahead of schedule)

🔧 Features Progress
✅ FEAT-001: User Authentication (100% - 5/5 requirements)
✅ FEAT-002: Password Reset (100% - 3/3 requirements)
🔄 FEAT-003: Role Management (75% - 3/4 requirements)
⏳ FEAT-004: Admin Dashboard (0% - 0/6 requirements)

📋 Requirements Summary
Total: 18 requirements
Completed: 11 (61%)
In Progress: 3 (17%)
Not Started: 4 (22%)

🧪 BDD Scenarios
Total: 25 scenarios
Linked to Features: 20
Ready for Testing: 18

🔗 External Tool Status
Jira Epic PROJ-123: In Progress (synced 2 hours ago)
Linear Initiative PROJECT-456: Active (synced 1 hour ago)

🚀 Next Actions
1. Complete FEAT-003 remaining requirements
2. Start FEAT-004 requirements gathering
3. Review BDD scenarios for FEAT-003
```

### `/epic-sync` - Sync with PM Tools

**Purpose**: Bidirectional sync of epic data with external project management tools.

**Bidirectional Sync:**
```bash
/epic-sync EPIC-001
```

**Force Push Local Changes:**
```bash
/epic-sync EPIC-001 --force-push
```

**Pull Remote Changes:**
```bash
/epic-sync EPIC-001 --pull-first
```

**Sync to Specific Tool:**
```bash
/epic-sync EPIC-001 --jira-only
/epic-sync EPIC-001 --linear-only
```

**Output:**
```
🔄 Syncing EPIC-001 with External Tools

📤 Pushing to Jira (PROJ-123)
✅ Updated epic status: In Progress
✅ Updated progress: 63%
✅ Synced 4 features
✅ Updated stakeholder assignments

📤 Pushing to Linear (PROJECT-456)
✅ Updated initiative status: Active
✅ Updated completion: 63%
✅ Synced feature links

✅ Sync Complete
Last Sync: 2025-11-03T14:30:00Z
Next Sync: 2025-11-03T15:30:00Z (auto)
```

---

## Feature Management Commands

### `/feature-create` - Create Feature with Epic Linkage

**Purpose**: Create a feature specification linked to an epic with requirements and BDD.

**Basic Usage:**
```bash
/feature-create "User Authentication" epic:EPIC-001
```

**With Requirements:**
```bash
/feature-create "User Authentication" \
  epic:EPIC-001 \
  requirements:[REQ-001,REQ-002,REQ-003] \
  priority:high
```

**With Full Specification:**
```bash
/feature-create "User Authentication" \
  epic:EPIC-001 \
  requirements:[REQ-001,REQ-002,REQ-003] \
  bdd:[BDD-001] \
  export:jira \
  priority:high
```

**Output:**
```
✅ Feature Created: FEAT-001

📋 Feature Details
Title: User Authentication
Epic: EPIC-001 (User Management System)
Priority: high
Status: active

📑 Linked Specifications
Requirements: REQ-001, REQ-002, REQ-003
BDD Scenarios: BDD-001 (8 scenarios)

🔄 PM Tool Integration
Jira Story: PROJ-124 (created)
- User Story: From feature description
- Acceptance Criteria: From BDD scenarios
- Linked to Epic: PROJ-123

📁 File Location
docs/features/FEAT-001-user-authentication.md

Next Steps:
1. Review generated feature specification
2. Generate task specs: /feature-generate-tasks FEAT-001
3. Export to additional tools: /feature-sync FEAT-001 --linear
```

### `/feature-status` - View Feature Progress

**Purpose**: Monitor feature progress including requirements and BDD scenario completion.

**Basic Status:**
```bash
/feature-status FEAT-001
```

**With Requirements Breakdown:**
```bash
/feature-status FEAT-001 --breakdown
```

**With BDD Coverage:**
```bash
/feature-status FEAT-001 --bdd-coverage
```

**Output:**
```
📋 Feature Status: FEAT-001 - User Authentication

🎯 Feature Details
Epic: EPIC-001 - User Management System
Status: in_progress
Progress: 75% complete

📋 Requirements Progress
✅ REQ-001: Password Encryption [Ubiquitous] (complete)
✅ REQ-002: Successful Login [Event-Driven] (complete)
🔄 REQ-003: Session Management [State-Driven] (in progress)
⏳ REQ-004: Account Lockout [Unwanted Behavior] (not started)

🧪 BDD Scenario Coverage
Total Scenarios: 8
✅ Implemented: 6 (75%)
🔄 In Progress: 1 (13%)
⏳ Not Started: 1 (12%)

Scenarios by Type:
- Happy Path: 4/4 complete
- Error Handling: 1/2 complete
- Security: 1/1 complete
- Performance: 0/1 complete

🔗 Traceability
Epic → Feature → Requirements → BDD: Complete
External Links: Jira PROJ-124, Linear ISS-456

⏭️ Next Steps
1. Complete REQ-003 specification
2. Start REQ-004 implementation planning
3. Implement remaining BDD scenario
```

### `/feature-sync` - Sync with PM Tools

**Purpose**: Sync feature and requirements with external project management tools.

**Basic Sync:**
```bash
/feature-sync FEAT-001
```

**With Progress Rollup:**
```bash
/feature-sync FEAT-001 --rollup-progress
```

**To Specific Tool:**
```bash
/feature-sync FEAT-001 --jira
/feature-sync FEAT-001 --linear
/feature-sync FEAT-001 --github
```

**Output:**
```
🔄 Syncing FEAT-001 with PM Tools

📤 Exporting to Jira
✅ Updated story: PROJ-124
✅ Status: In Progress
✅ Progress: 75%
✅ Updated acceptance criteria from BDD-001
✅ Linked 4 requirements as subtasks

📤 Exporting to Linear
✅ Updated issue: ISS-456
✅ Status: In Progress
✅ Progress: 75%

📈 Rolling up to Epic
✅ Updated EPIC-001 progress
✅ Recalculated epic completion: 58% → 63%

✅ Sync Complete
```

### `/feature-generate-tasks` - Generate Task Specifications

**Purpose**: Auto-generate task specifications from feature requirements and BDD scenarios.

**Basic Generation:**
```bash
/feature-generate-tasks FEAT-001
```

**With Parameters:**
```bash
/feature-generate-tasks FEAT-001 \
  --max-tasks=8 \
  --include-tests \
  --epic-context
```

**Interactive Mode:**
```bash
/feature-generate-tasks FEAT-001 --interactive
```

**Output:**
```
✅ Task Specifications Generated

Generated 5 tasks from FEAT-001:

📋 TASK-001: Implement login endpoint
- Requirements: REQ-002
- BDD Scenarios: BDD-001 (scenarios 1-3)
- Estimated Effort: 3 story points

📋 TASK-002: Create user registration
- Requirements: REQ-006, REQ-007
- BDD Scenarios: BDD-001 (scenarios 4-5)
- Estimated Effort: 5 story points

📋 TASK-003: Add session management
- Requirements: REQ-003
- BDD Scenarios: BDD-001 (scenario 6)
- Estimated Effort: 3 story points

📋 TASK-004: Build login UI components
- Requirements: REQ-002
- BDD Scenarios: BDD-001 (scenarios 1-2)
- Estimated Effort: 2 story points

📋 TASK-005: Integration tests
- Requirements: All
- BDD Scenarios: BDD-001 (all)
- Estimated Effort: 2 story points

Total Effort: 15 story points

📁 Files Created
tasks/backlog/TASK-001.md through TASK-005.md

Next Steps:
1. Review generated task specifications
2. For task execution: Install guardkit
3. See Integration Guide for workflow
```

---

## Hierarchy Commands

### `/hierarchy-view` - View Project Hierarchy

**Purpose**: Visualize complete project structure showing epics, features, requirements, and BDD.

**Overview Mode:**
```bash
/hierarchy-view
```

**For Specific Epic:**
```bash
/hierarchy-view EPIC-001
```

**Detailed Mode:**
```bash
/hierarchy-view EPIC-001 --mode=detailed
```

**With BDD:**
```bash
/hierarchy-view EPIC-001 --include-bdd
```

**Output:**
```
📊 Project Hierarchy - User Management System

├── 🎯 EPIC-001: User Management System (63% complete)
│   │
│   ├── 🔧 FEAT-001: User Authentication (100% complete)
│   │   ├── 📋 REQ-001: Password Encryption [Ubiquitous] ✅
│   │   ├── 📋 REQ-002: Successful Login [Event-Driven] ✅
│   │   ├── 📋 REQ-003: Session Management [State-Driven] ✅
│   │   ├── 📋 REQ-004: Account Lockout [Unwanted Behavior] ✅
│   │   ├── 📋 REQ-005: Remember Me [Optional Feature] ✅
│   │   └── 🧪 BDD-001: User Authentication (8 scenarios) ✅
│   │
│   ├── 🔧 FEAT-002: Password Reset (100% complete)
│   │   ├── 📋 REQ-006: Reset Request [Event-Driven] ✅
│   │   ├── 📋 REQ-007: Email Validation [Ubiquitous] ✅
│   │   ├── 📋 REQ-008: Token Expiry [Unwanted Behavior] ✅
│   │   └── 🧪 BDD-002: Password Reset (5 scenarios) ✅
│   │
│   ├── 🔧 FEAT-003: Role Management (75% complete)
│   │   ├── 📋 REQ-009: Role Assignment [Event-Driven] ✅
│   │   ├── 📋 REQ-010: Permission Check [State-Driven] ✅
│   │   ├── 📋 REQ-011: Role Hierarchy [Ubiquitous] 🔄
│   │   ├── 📋 REQ-012: Invalid Role [Unwanted Behavior] ⏳
│   │   └── 🧪 BDD-003: Role Management (6 scenarios) 🔄
│   │
│   └── 🔧 FEAT-004: Admin Dashboard (0% complete)
│       ├── 📋 REQ-013: Dashboard Layout [Ubiquitous] ⏳
│       ├── 📋 REQ-014: User List View [State-Driven] ⏳
│       ├── 📋 REQ-015: User Actions [Event-Driven] ⏳
│       ├── 📋 REQ-016: Audit Log [Ubiquitous] ⏳
│       ├── 📋 REQ-017: Access Control [State-Driven] ⏳
│       ├── 📋 REQ-018: Error Display [Unwanted Behavior] ⏳
│       └── 🧪 BDD-004: Admin Dashboard (planning)

🎯 Summary
Epics: 1 active
Features: 4 (2 completed, 1 in progress, 1 not started)
Requirements: 18 total (11 complete, 3 in progress, 4 not started)
BDD Scenarios: 25 total (20 complete, 3 in progress, 2 planned)
Overall Progress: 63% complete

📈 Progress Trend
Last 7 days: +15% completion
Velocity: 2.1 requirements/day
Projected Completion: 5 days

🔗 External Links
Jira Epic: PROJ-123
Linear Initiative: PROJECT-456
```

---

## Export and Integration Commands

### Export to Jira

```bash
# Export epic
/epic-sync EPIC-001 --jira

# Export feature
/feature-sync FEAT-001 --jira

# Export with force
/feature-sync FEAT-001 --jira --force-push
```

**Creates in Jira:**
- Epic with business value and timeline
- User Stories from features
- Acceptance criteria from BDD scenarios
- Requirements as subtasks
- Full traceability links

### Export to Linear

```bash
# Export epic
/epic-sync EPIC-001 --linear

# Export feature
/feature-sync FEAT-001 --linear
```

**Creates in Linear:**
- Initiative from epic
- Issues from features
- Requirements context
- BDD acceptance criteria
- Traceability metadata

### Export to GitHub Projects

```bash
# Export feature
/feature-sync FEAT-001 --github

# Creates GitHub issue with:
# - Feature description
# - Requirements checklist
# - BDD scenarios
# - Labels from tags
```

### Export to Azure DevOps

```bash
# Export epic
/epic-sync EPIC-001 --azure

# Export feature
/feature-sync FEAT-001 --azure
```

---

## Complete Workflow Examples

### Example 1: New Feature from Scratch

```bash
# Step 1: Gather requirements
/gather-requirements shopping-cart
# Interactive Q&A captures complete requirements

# Step 2: Formalize to EARS
/formalize-ears
# Output: docs/requirements/REQ-020.md through REQ-028.md

# Step 3: Create epic
/epic-create "E-Commerce Platform"
# Output: docs/epics/EPIC-002.md

# Step 4: Create feature
/feature-create "Shopping Cart" \
  epic:EPIC-002 \
  requirements:[REQ-020,REQ-021,REQ-022] \
  priority:high
# Output: docs/features/FEAT-004.md

# Step 5: Generate BDD scenarios
/generate-bdd FEAT-004
# Output: docs/bdd/BDD-004-shopping-cart.feature

# Step 6: View complete hierarchy
/hierarchy-view EPIC-002

# Step 7: Export to Jira
/feature-sync FEAT-004 --jira

# Step 8: Generate task specifications (optional)
/feature-generate-tasks FEAT-004
# Output: tasks/backlog/TASK-*.md
```

**Result**: Complete feature specification ready for implementation or export.

### Example 2: Epic with Multiple Features

```bash
# Create epic
/epic-create "User Management System" \
  priority:high \
  business_value:9 \
  export:[jira,linear]
# Output: EPIC-001

# Create features
/feature-create "Login" epic:EPIC-001
/feature-create "Registration" epic:EPIC-001
/feature-create "Password Reset" epic:EPIC-001
/feature-create "User Profiles" epic:EPIC-001

# For each feature, gather and formalize
/gather-requirements login
/formalize-ears
/generate-bdd
# Link to FEAT-001

/gather-requirements registration
/formalize-ears
/generate-bdd
# Link to FEAT-002

# Continue for remaining features...

# View complete epic
/hierarchy-view EPIC-001

# Export epic with all features
/epic-sync EPIC-001 --jira
```

### Example 3: Requirements Review and Iteration

```bash
# Step 1: Draft initial requirements
/gather-requirements reporting-system
# Output: docs/requirements/draft/reporting-system.md

# Step 2: Formalize for review
/formalize-ears docs/requirements/draft/reporting-system.md
# Output: REQ-030 through REQ-040

# Step 3: Share with stakeholders
# Team reviews docs/requirements/REQ-*.md files

# Step 4: Iterate based on feedback
# Edit requirement files to incorporate feedback

# Step 5: Re-validate
/formalize-ears --validate docs/requirements/REQ-030.md

# Step 6: Generate BDD for validation
/generate-bdd --feature reporting-system
# Output: docs/bdd/BDD-005-reporting.feature

# Step 7: Review BDD with stakeholders
# BDD scenarios serve as acceptance criteria

# Step 8: Finalize and organize
/epic-create "Reporting System"
/feature-create "Sales Reports" \
  epic:EPIC-003 \
  requirements:[REQ-030,REQ-031,REQ-032]
/feature-create "Analytics Dashboard" \
  epic:EPIC-003 \
  requirements:[REQ-033,REQ-034]

# Step 9: Export to PM tools
/epic-sync EPIC-003 --jira --linear
```

### Example 4: Adding Requirements to Existing Code

```bash
# You have existing code, need to add requirements retroactively

# Step 1: Document what exists
/gather-requirements existing-payment-system
# Describe current functionality

# Step 2: Formalize
/formalize-ears
# Output: REQ-050 through REQ-058

# Step 3: Create structure
/epic-create "Payment Processing"
/feature-create "Credit Card Payments" \
  epic:EPIC-004 \
  requirements:[REQ-050,REQ-051,REQ-052]

# Step 4: Generate BDD for regression testing
/generate-bdd FEAT-010

# Step 5: Link to existing code
# Edit feature file to add implementation references

# Step 6: Export for tracking
/feature-sync FEAT-010 --jira
```

---

## Task Execution (Optional Integration)

For task execution workflow, install [guardkit](https://github.com/guardkit-dev/guardkit).

See [Integration Guide](../INTEGRATION-GUIDE.md) for:
- Installing guardkit alongside require-kit
- Using `/task-work` for implementation
- Complete requirements-to-implementation traceability
- TDD workflow with quality gates

---

## Tips and Best Practices

### Requirements Gathering
- **Be Specific**: Use concrete numbers ("1 second", "1000 users") not vague terms ("fast", "many")
- **Include Error Cases**: Don't forget what happens when things go wrong
- **Ask "Why"**: Understand the problem before prescribing solutions
- **Capture Context**: Document assumptions and constraints

### EARS Formalization
- **One Behavior Per Requirement**: Keep requirements atomic and focused
- **Choose Right Pattern**: Match the requirement type to the EARS pattern
- **Measurable Criteria**: Include specific, testable thresholds
- **Avoid Ambiguity**: Use clear, unambiguous language

### BDD Scenarios
- **User Perspective**: Write from the user's point of view ("I", "user")
- **Independent Scenarios**: Each should run standalone
- **Concrete Examples**: Use specific data, not abstract variables
- **Complete Coverage**: Include happy paths, error cases, edge cases

### Project Organization
- **Meaningful Epics**: Group related features by business capability
- **Focused Features**: One feature = one user-facing capability
- **Clear Hierarchy**: Maintain Epic → Feature → Requirement → BDD links
- **Regular Sync**: Keep PM tools synchronized

---

## Additional Resources

### Documentation
- **[Getting Started](getting_started.md)** - Quick start guide
- **[User Guide](require_kit_user_guide.md)** - Comprehensive feature documentation
- **[Integration Guide](../INTEGRATION-GUIDE.md)** - Using with guardkit
- **[README](../../README.md)** - Overview and quick reference

### Support
- **GitHub Issues**: [require-kit issues](https://github.com/requirekit/require-kit/issues)
- **Examples**: See `docs/requirements/`, `docs/bdd/`, `docs/epics/`, `docs/features/`

---

**Version**: 1.0.0 | **Last Updated**: 2025-11-03 | [require-kit](https://github.com/requirekit/require-kit)
