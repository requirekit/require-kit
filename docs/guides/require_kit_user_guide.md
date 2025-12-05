# require-kit User Guide

**Version**: 1.0.0
**Last Updated**: 2025-11-03

## Table of Contents

1. [Introduction](#introduction)
2. [System Overview](#system-overview)
3. [Core Workflow](#core-workflow)
4. [Requirements Gathering](#requirements-gathering)
5. [EARS Notation](#ears-notation)
6. [BDD Scenario Generation](#bdd-scenario-generation)
7. [Epic/Feature Hierarchy](#epicfeature-hierarchy)
8. [Command Reference](#command-reference)
9. [Workflow Examples](#workflow-examples)
10. [Integration](#integration)
11. [Best Practices](#best-practices)

---

## Introduction

### What is require-kit?

require-kit is a standalone requirements management toolkit that provides structured approaches to capturing, formalizing, and organizing software requirements. It uses proven methodologies to ensure clear, testable, and traceable requirements throughout the development lifecycle.

### Core Capabilities

- **Interactive Requirements Gathering**: Conversational Q&A approach to capture complete requirements
- **EARS Notation Formalization**: Convert natural language to structured, unambiguous requirements
- **BDD/Gherkin Scenario Generation**: Create testable scenarios from requirements
- **Epic/Feature Hierarchy Management**: Organize requirements into logical project structures
- **Requirements Traceability**: Clear links from epics to features to requirements
- **Technology Agnostic**: Works with any implementation system or project management tool

### When to Use require-kit

Use require-kit when you need:
- Clear, unambiguous requirements documentation
- Requirements traceability across your project
- BDD scenarios for acceptance criteria
- Structured project organization (epics/features/requirements)
- Export capabilities to PM tools (Jira, Linear, GitHub Projects, Azure DevOps)

### Standalone or Integrated

require-kit is **fully functional standalone** with no dependencies. Optionally integrate with [guardkit](https://github.com/guardkit/guardkit) for task execution workflow.

See [Integration Guide](../INTEGRATION-GUIDE.md) for details on using require-kit with guardkit.

---

## System Overview

### Architecture

```
require-kit System
├── Requirements Gathering Agent
│   └── Interactive Q&A sessions
├── EARS Formalization Agent
│   └── Convert to structured notation
├── BDD Generator Agent
│   └── Create Gherkin scenarios
└── Epic/Feature Manager Agent
    └── Organize hierarchically
```

### Core Philosophy

**"Start with clear requirements"**

Every feature should begin with well-understood, clearly documented requirements before implementation begins. require-kit helps you:

1. **Capture** complete requirements through guided questions
2. **Formalize** into unambiguous EARS notation
3. **Generate** testable BDD scenarios
4. **Organize** into meaningful project structure
5. **Export** to your chosen implementation system

---

## Core Workflow

### The require-kit Process

```
┌─────────────────┐     ┌──────────────┐     ┌───────────────┐
│   Gather        │────▶│  Formalize   │────▶│   Generate    │
│ Requirements    │     │  with EARS   │     │  BDD Scenarios│
└─────────────────┘     └──────────────┘     └───────────────┘
         │                      │                      │
         └──────────────────────┴──────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │   Organize into        │
                    │ Epic/Feature Hierarchy │
                    └────────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │  Export/Integration    │
                    │  (PM Tools/guardkit) │
                    └────────────────────────┘
```

### Quick Start (3 Steps)

```bash
# 1. Gather requirements interactively
/gather-requirements

# 2. Formalize into EARS notation
/formalize-ears

# 3. Generate BDD scenarios
/generate-bdd
```

**Output**: Complete requirement specification ready for implementation or export.

---

## Requirements Gathering

### Interactive Q&A Process

The `/gather-requirements` command guides you through structured questions to capture complete requirements.

#### Basic Usage

```bash
/gather-requirements
```

#### With Feature Name

```bash
/gather-requirements user-authentication
```

### Example Session

```
Claude: Let's gather requirements for user authentication. What problem are we solving?

You: We need secure user login for our web application using email and password.

Claude: Who will be using this authentication system?

You: Both regular users and administrators. Admins need special access to admin features.

Claude: What should happen when authentication succeeds?

You: User should be redirected to dashboard. Session should be created.

Claude: What should happen when authentication fails?

You: Show error message. Lock account after 3 failed attempts within 5 minutes.

Claude: What are the performance requirements?

You: Login should complete within 1 second. Support 1000 concurrent users.

Claude: What are the security requirements?

You: Passwords must be 8+ characters with complexity rules. All traffic over HTTPS.
Sessions should timeout after 24 hours (or 30 days with "remember me").

Claude: Are there any compliance or regulatory requirements?

You: Need audit logging of all authentication events for SOC 2 compliance.

Claude: Great! I've captured these requirements. Here's the summary:

## Requirements Summary

### Functional Requirements
- User login with email/password
- Admin users with elevated access
- Account lockout after 3 failed attempts
- Session management (24hr default, 30 day remember)
- Audit logging for compliance

### Non-Functional Requirements
- Performance: <1 second login time
- Scalability: 1000 concurrent users
- Security: Password complexity, HTTPS only
- Compliance: SOC 2 audit logging

### Error Handling
- Invalid credentials → error message
- 3 failed attempts → account lock (15 minutes)
- Session timeout → redirect to login

Output saved to: docs/requirements/draft/user-authentication.md

Ready to formalize with /formalize-ears
```

### Question Categories

The gathering agent asks questions across key categories:

1. **Problem Definition**: What problem are we solving?
2. **User Roles**: Who will use this feature?
3. **Functional Behavior**: What should the system do?
4. **Error Handling**: What could go wrong? How to recover?
5. **Performance**: Speed, scalability requirements
6. **Security**: Authentication, authorization, data protection
7. **Compliance**: Regulatory requirements, audit needs
8. **Integration**: External systems, APIs
9. **Future Considerations**: Planned enhancements

### Tips for Effective Gathering

1. **Be Specific**: "Login in 1 second" not "fast login"
2. **Include Error Cases**: What happens when things fail?
3. **Mention Performance**: Specific numbers (1000 users, <1s response)
4. **State Security Needs**: Authentication, encryption, compliance
5. **Think Future**: Optional features for later phases

---

## EARS Notation

### What is EARS?

EARS (Easy Approach to Requirements Syntax) is a proven methodology for writing clear, unambiguous requirements using five structured patterns.

### The Five EARS Patterns

#### 1. Ubiquitous Requirements

**Format**: `The [system] shall [behavior]`

**When to Use**: Requirements that always apply, no conditions

**Examples**:
```
REQ-001: The system shall encrypt all passwords using bcrypt with cost factor 12.

REQ-002: The system shall log all authentication events to the audit database.

REQ-003: The system shall reject any non-HTTPS authentication requests.
```

#### 2. Event-Driven Requirements

**Format**: `When [trigger], the [system] shall [response]`

**When to Use**: Requirements triggered by specific events

**Examples**:
```
REQ-004: When a user submits valid credentials, the system shall create a session
         and redirect to the dashboard within 1 second.

REQ-005: When a user submits invalid credentials, the system shall display
         "Invalid email or password" and increment the failed attempt counter.

REQ-006: When a user clicks "Forgot Password", the system shall send a password
         reset email within 30 seconds.
```

#### 3. State-Driven Requirements

**Format**: `While [state], the [system] shall [behavior]`

**When to Use**: Requirements that apply only in certain states

**Examples**:
```
REQ-007: While a user session is active, the system shall validate the session
         token on each request.

REQ-008: While a user has admin role, the system shall display the admin
         navigation menu.

REQ-009: While an account is locked, the system shall reject all login attempts
         and display "Account locked" message.
```

#### 4. Unwanted Behavior Requirements

**Format**: `If [error], then the [system] shall [recovery]`

**When to Use**: Error handling and recovery requirements

**Examples**:
```
REQ-010: If a user submits invalid credentials 3 times within 5 minutes, then
         the system shall lock the account for 15 minutes and send a security
         alert email.

REQ-011: If a session expires, then the system shall redirect to the login page
         with message "Session expired" and preserve the intended destination
         URL for post-login redirect.

REQ-012: If the authentication database is unavailable, then the system shall
         return HTTP 503 with message "Service temporarily unavailable".
```

#### 5. Optional Feature Requirements

**Format**: `Where [feature], the [system] shall [behavior]`

**When to Use**: Optional or conditional features

**Examples**:
```
REQ-013: Where the user has selected "Remember Me", the system shall maintain
         the session for 30 days with automatic token refresh.

REQ-014: Where two-factor authentication is enabled, the system shall require
         a verification code after password validation.

REQ-015: Where single sign-on is configured, the system shall redirect to the
         SSO provider for authentication.
```

### Formalizing Requirements

#### Command Usage

```bash
# Formalize from gathered requirements
/formalize-ears

# Formalize specific file
/formalize-ears docs/requirements/draft/user-authentication.md
```

#### Output Format

```markdown
# User Authentication Requirements

**Epic**: EPIC-001 - User Management System
**Feature**: FEAT-001 - Login Functionality
**Date**: 2025-11-03
**Status**: Approved

## Requirements

### REQ-001: Password Encryption [Ubiquitous]
**The system** shall encrypt all passwords using bcrypt with cost factor 12.

**Rationale**: Industry best practice for password security
**Priority**: Critical
**Test**: BDD-001

---

### REQ-002: Successful Login [Event-Driven]
**When** a user submits valid email and password credentials,
**the system** shall authenticate the user, create a session, and redirect
to the dashboard within 1 second.

**Rationale**: Core authentication flow
**Priority**: High
**Test**: BDD-001, BDD-002

---

### REQ-003: Session Management [State-Driven]
**While** a user session is active,
**the system** shall validate the session token on each request and refresh
the session timeout to 24 hours from last activity.

**Rationale**: Security and user experience balance
**Priority**: High
**Test**: BDD-003

---

### REQ-004: Account Lockout [Unwanted Behavior]
**If** a user submits invalid credentials 3 times within 5 minutes,
**then the system** shall lock the account for 15 minutes, display
"Account locked" message, and send a security alert email to the account owner.

**Rationale**: Prevent brute force attacks
**Priority**: Critical
**Test**: BDD-004

---

### REQ-005: Remember Me [Optional Feature]
**Where** the user has selected "Remember Me" during login,
**the system** shall maintain the session for 30 days with automatic token
refresh on each visit.

**Rationale**: User convenience for trusted devices
**Priority**: Medium
**Test**: BDD-005
```

### EARS Best Practices

1. **One Behavior Per Requirement**: Keep requirements atomic and focused
2. **Measurable Criteria**: Include specific thresholds (1 second, 80%, 1000 users)
3. **Choose Right Pattern**: Match the requirement type to the EARS pattern
4. **Clear Language**: Avoid ambiguous words like "fast", "should", "might"
5. **Link to Tests**: Reference BDD scenarios that verify each requirement

---

## BDD Scenario Generation

### What are BDD Scenarios?

BDD (Behavior-Driven Development) scenarios use Gherkin syntax to create testable acceptance criteria from requirements. Each scenario describes how the system should behave in a specific situation.

### Gherkin Syntax

```gherkin
Feature: User Authentication
  As a user of the application
  I want to securely log in with my credentials
  So that I can access my protected resources

  Background:
    Given the authentication service is running
    And the database is accessible

  Scenario: Successful login with valid credentials
    Given a registered user with email "user@example.com"
    And the user's password is "Valid123!"
    When the user submits the login form
    Then the user should be authenticated
    And the user should be redirected to "/dashboard"
    And a session cookie should be created
    And the authentication should complete within 1 second

  Scenario: Failed login with invalid password
    Given a registered user with email "user@example.com"
    When the user submits the login form with password "WrongPassword"
    Then the user should remain on "/login"
    And an error message "Invalid email or password" should be displayed
    And no session cookie should be created
    And the failed attempt should be logged
```

### Generating BDD Scenarios

#### Command Usage

```bash
# Generate from formalized requirements
/generate-bdd

# Generate for specific requirement
/generate-bdd REQ-001

# Generate for entire feature
/generate-bdd --feature FEAT-001
```

#### Example Output

```gherkin
# Generated from: REQ-001, REQ-002, REQ-004, REQ-005
# File: docs/bdd/BDD-001-user-authentication.feature

@epic-EPIC-001 @feature-FEAT-001 @authentication
Feature: User Authentication System
  As a user of the application
  I want to securely log in with my credentials
  So that I can access my protected resources

  Background:
    Given the authentication service is running
    And the database is accessible
    And the following users exist:
      | email                | password    | role    | status |
      | user@example.com     | Valid123!   | user    | active |
      | admin@example.com    | Admin456!   | admin   | active |
      | locked@example.com   | Locked789!  | user    | locked |

  @requirement-REQ-002 @happy-path @smoke
  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter "user@example.com" in the email field
    And I enter "Valid123!" in the password field
    And I click the "Sign In" button
    Then I should be redirected to "/dashboard"
    And I should see "Welcome back!" message
    And a session cookie should be created with httpOnly and secure flags
    And the authentication should complete within 1 second

  @requirement-REQ-002 @admin @happy-path
  Scenario: Admin login redirects to admin dashboard
    Given I am on the login page
    When I enter "admin@example.com" in the email field
    And I enter "Admin456!" in the password field
    And I click the "Sign In" button
    Then I should be redirected to "/admin/dashboard"
    And I should see the admin navigation menu
    And the session should have admin privileges

  @requirement-REQ-004 @error-handling @security
  Scenario: Invalid password shows error message
    Given I am on the login page
    When I enter "user@example.com" in the email field
    And I enter "WrongPassword!" in the password field
    And I click the "Sign In" button
    Then I should remain on "/login"
    And I should see error message "Invalid email or password"
    And no session cookie should be created
    And the failed attempt should be logged for "user@example.com"

  @requirement-REQ-004 @security @critical
  Scenario: Account lockout after multiple failed attempts
    Given I am on the login page
    And the user "user@example.com" has 2 failed login attempts in the last 5 minutes
    When I enter "user@example.com" in the email field
    And I enter "WrongPassword!" in the password field
    And I click the "Sign In" button
    Then I should see error message "Account locked due to multiple failed attempts"
    And the account should be locked for 15 minutes
    And a security alert email should be sent to "user@example.com"
    And subsequent login attempts should be rejected with "Account locked" message

  @requirement-REQ-004 @security
  Scenario: Locked account can login after timeout expires
    Given the user "user@example.com" was locked 16 minutes ago
    When I enter "user@example.com" in the email field
    And I enter "Valid123!" in the password field
    And I click the "Sign In" button
    Then I should be successfully authenticated
    And the failed attempt counter should be reset to zero

  @requirement-REQ-005 @optional-feature
  Scenario: Remember me creates persistent session
    Given I am on the login page
    When I enter "user@example.com" in the email field
    And I enter "Valid123!" in the password field
    And I check the "Remember me" checkbox
    And I click the "Sign In" button
    Then I should be redirected to "/dashboard"
    And a persistent session cookie should be created
    And the cookie should expire in 30 days
    And the cookie should be marked as secure and httpOnly

  @requirement-REQ-003 @session-management
  Scenario: Session expiry redirects to login
    Given I am logged in as "user@example.com"
    And I am on page "/profile/settings"
    When my session expires after 24 hours of inactivity
    And I try to navigate to "/profile/settings"
    Then I should be redirected to "/login"
    And I should see message "Session expired, please log in again"
    And the return URL should be set to "/profile/settings"

  @requirement-REQ-003 @session-management @happy-path
  Scenario: Successful login redirects to original destination
    Given I was redirected to login from "/profile/settings"
    When I successfully log in
    Then I should be redirected to "/profile/settings"
    And not to the default dashboard

  @requirement-REQ-001 @security @performance
  Scenario Outline: Concurrent user logins
    Given <users> users are attempting to login simultaneously
    When all users submit valid credentials
    Then all authentications should complete within <time> seconds
    And the system should remain responsive
    And all passwords should be verified using bcrypt

    Examples:
      | users | time |
      | 100   | 1    |
      | 500   | 1    |
      | 1000  | 1    |
```

### BDD Best Practices

1. **User-Centric Language**: Write from user perspective ("I", "user")
2. **Independent Scenarios**: Each should run standalone
3. **Use Tags**: Organize by requirement, epic, feature, priority
4. **Concrete Examples**: Use specific data, not variables
5. **Link to Requirements**: Tag with `@requirement-REQ-XXX`
6. **Include Edge Cases**: Not just happy paths

---

## Epic/Feature Hierarchy

### Project Organization

require-kit organizes requirements hierarchically:

```
Epic (Strategic Initiative)
├── Feature (User-Facing Capability)
│   ├── Requirement (EARS Specification)
│   ├── Requirement
│   └── BDD Scenario (Acceptance Criteria)
├── Feature
│   ├── Requirement
│   └── BDD Scenario
└── Feature
```

### Creating Epics

#### Basic Epic Creation

```bash
/epic-create "User Management System"
```

#### With Metadata

```bash
/epic-create "User Management System" \
  priority:high \
  business_value:8 \
  effort_estimate:21
```

#### Example Output

```
✅ Epic Created: EPIC-001

📋 Epic Details
Title: User Management System
Priority: high
Business Value: 8/10
Effort Estimate: 21 story points

📁 File Location
docs/epics/EPIC-001-user-management-system.md

Next Steps:
1. Create features: /feature-create "Feature Name" epic:EPIC-001
2. Monitor progress: /epic-status EPIC-001
```

### Creating Features

#### Basic Feature Creation

```bash
/feature-create "Login Functionality" epic:EPIC-001
```

#### With Requirements

```bash
/feature-create "Login Functionality" \
  epic:EPIC-001 \
  requirements:[REQ-001,REQ-002,REQ-003] \
  priority:high
```

#### Example Output

```
✅ Feature Created: FEAT-001

📋 Feature Details
Title: Login Functionality
Epic: EPIC-001 (User Management System)
Priority: high
Status: active

📑 Linked Specifications
Requirements: REQ-001, REQ-002, REQ-003

📁 File Location
docs/features/FEAT-001-login-functionality.md

Next Steps:
1. Generate BDD: /generate-bdd FEAT-001
2. View hierarchy: /hierarchy-view EPIC-001
```

### Viewing Hierarchy

#### Command Usage

```bash
# View specific epic hierarchy
/hierarchy-view EPIC-001

# View all epics
/hierarchy-view

# Detailed view
/hierarchy-view EPIC-001 --mode=detailed
```

#### Example Output

```
📊 Project Hierarchy - User Management System

├── 🎯 EPIC-001: User Management System (65% complete)
│   ├── 🔧 FEAT-001: Login Functionality (100% complete)
│   │   ├── 📋 REQ-001: Password Encryption [Ubiquitous]
│   │   ├── 📋 REQ-002: Successful Login [Event-Driven]
│   │   ├── 📋 REQ-003: Session Management [State-Driven]
│   │   ├── 📋 REQ-004: Account Lockout [Unwanted Behavior]
│   │   ├── 📋 REQ-005: Remember Me [Optional Feature]
│   │   └── 🧪 BDD-001: User Authentication (8 scenarios)
│   │
│   ├── 🔧 FEAT-002: Password Reset (75% complete)
│   │   ├── 📋 REQ-006: Reset Request [Event-Driven]
│   │   ├── 📋 REQ-007: Email Validation [Ubiquitous]
│   │   ├── 📋 REQ-008: Token Expiry [Unwanted Behavior]
│   │   └── 🧪 BDD-002: Password Reset (5 scenarios)
│   │
│   └── 🔧 FEAT-003: User Profiles (25% complete)
│       ├── 📋 REQ-009: Profile Display [State-Driven]
│       ├── 📋 REQ-010: Profile Editing [Event-Driven]
│       └── 🧪 BDD-003: User Profiles (4 scenarios)

🎯 Summary
Total Epics: 1
Total Features: 3 (1 completed, 2 in progress)
Total Requirements: 10
Total BDD Scenarios: 17
Overall Progress: 65% complete
```

---

## Command Reference

### Requirements Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/gather-requirements` | Interactive Q&A gathering | `/gather-requirements user-auth` |
| `/formalize-ears` | Convert to EARS notation | `/formalize-ears draft/user-auth.md` |
| `/generate-bdd` | Generate Gherkin scenarios | `/generate-bdd REQ-001` |

### Epic Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/epic-create` | Create new epic | `/epic-create "User Management"` |
| `/epic-status` | View epic progress | `/epic-status EPIC-001` |
| `/epic-sync` | Sync with PM tools | `/epic-sync EPIC-001 --jira` |

### Feature Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/feature-create` | Create new feature | `/feature-create "Login" epic:EPIC-001` |
| `/feature-status` | View feature progress | `/feature-status FEAT-001` |
| `/feature-sync` | Sync with PM tools | `/feature-sync FEAT-001 --linear` |
| `/feature-generate-tasks` | Generate task specs | `/feature-generate-tasks FEAT-001` |

### Hierarchy Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/hierarchy-view` | View project structure | `/hierarchy-view EPIC-001` |

---

## Workflow Examples

### Example 1: New Feature from Scratch

```bash
# Step 1: Gather requirements
/gather-requirements shopping-cart

# Interactive Q&A captures complete requirements
# Output: docs/requirements/draft/shopping-cart.md

# Step 2: Formalize to EARS
/formalize-ears docs/requirements/draft/shopping-cart.md

# Output: docs/requirements/REQ-020.md through REQ-028.md

# Step 3: Create epic
/epic-create "E-Commerce Platform"

# Output: docs/epics/EPIC-002.md

# Step 4: Create feature
/feature-create "Shopping Cart" epic:EPIC-002 requirements:[REQ-020,REQ-021,REQ-022]

# Output: docs/features/FEAT-004.md

# Step 5: Generate BDD scenarios
/generate-bdd FEAT-004

# Output: docs/bdd/BDD-004-shopping-cart.feature

# Step 6: View complete hierarchy
/hierarchy-view EPIC-002

# See complete traceability: Epic → Feature → Requirements → BDD

# Step 7: Export or implement
# Option A: Export to Jira
/feature-sync FEAT-004 --jira

# Option B: Generate task specifications for guardkit
/feature-generate-tasks FEAT-004
```

### Example 2: Adding Requirements to Existing Project

```bash
# You have existing code, need to add requirements

# Step 1: Gather requirements retroactively
/gather-requirements existing-payment-system

# Document what the system currently does

# Step 2: Formalize
/formalize-ears

# Output: REQ-030 through REQ-035

# Step 3: Add to existing epic/feature
/feature-create "Payment Processing" epic:EPIC-002 requirements:[REQ-030,REQ-031,REQ-032]

# Step 4: Generate BDD for regression testing
/generate-bdd FEAT-005

# Use BDD scenarios to create regression tests

# Step 5: Link to existing code
# Edit feature file to add implementation references
```

### Example 3: Requirements Review Cycle

```bash
# Step 1: Draft requirements
/gather-requirements new-reporting-feature

# Step 2: Formalize for review
/formalize-ears

# Output: docs/requirements/REQ-040.md through REQ-045.md

# Step 3: Share with stakeholders
# Review docs/requirements/REQ-*.md files with team

# Step 4: Iterate based on feedback
# Edit requirement files, add clarifications

# Step 5: Generate BDD for validation
/generate-bdd --feature reporting

# Step 6: Review BDD scenarios with stakeholders
# Scenarios serve as acceptance criteria discussion

# Step 7: Finalize and organize
/epic-create "Reporting System"
/feature-create "Sales Reports" epic:EPIC-003 requirements:[REQ-040,REQ-041]
/feature-create "Analytics Dashboard" epic:EPIC-003 requirements:[REQ-042,REQ-043]

# Step 8: Export to PM tool
/epic-sync EPIC-003 --jira
```

---

## Integration

### Standalone Use

require-kit works completely standalone:

- Gather, formalize, and organize requirements
- Generate BDD scenarios for manual or automated testing
- Export to any PM tool (Jira, Linear, GitHub Projects, Azure DevOps)
- Maintain requirements traceability in markdown files
- Use outputs with any implementation workflow

### Integration with guardkit

For task execution workflow with quality gates:

1. **Install guardkit**: See [guardkit repository](https://github.com/guardkit/guardkit)
2. **Automatic Detection**: Both packages detect each other via marker files
3. **Enhanced Workflow**: Requirements context flows to task execution
4. **Full Traceability**: REQ → BDD → FEAT → TASK → Implementation

See [Integration Guide](../INTEGRATION-GUIDE.md) for complete details.

### PM Tool Export

#### Jira Integration

```bash
# Export feature to Jira
/feature-sync FEAT-001 --jira

# Creates Jira ticket with:
# - Title from feature
# - Description from feature details
# - Acceptance criteria from BDD scenarios
# - Links to requirements (REQ-XXX)
# - Links to epic
```

#### Linear Integration

```bash
# Export to Linear
/feature-sync FEAT-001 --linear

# Creates Linear issue with full traceability
```

#### GitHub Projects Integration

```bash
# Export to GitHub Projects
/feature-sync FEAT-001 --github

# Creates GitHub issue with requirements context
```

---

## Best Practices

### Requirements Gathering

1. **Ask Open-Ended Questions**: Don't assume, discover through conversation
2. **Capture Context**: Why is this needed? What problem does it solve?
3. **Include Non-Functionals**: Performance, security, scalability
4. **Document Constraints**: Technical limits, budget, timeline
5. **Note Future Considerations**: What might come later?

### EARS Formalization

1. **One Behavior Per Requirement**: Keep atomic and focused
2. **Use Measurable Criteria**: Specific numbers, not "fast" or "good"
3. **Choose Correct Pattern**: Match requirement type to EARS pattern
4. **Avoid Ambiguity**: Clear, unambiguous language
5. **Link Everything**: Requirements → Features → Epics

### BDD Scenarios

1. **User Language**: Write from user perspective
2. **Independent**: Scenarios should not depend on each other
3. **Concrete**: Specific examples, not abstract variables
4. **Complete**: Given-When-Then covers the full flow
5. **Tag Properly**: Link to requirements, organize by feature

### Project Organization

1. **Logical Epics**: Group related features by business capability
2. **Focused Features**: Each feature = one user-facing capability
3. **Clear Hierarchy**: Epic → Feature → Requirement → BDD
4. **Maintain Traceability**: Link everything bidirectionally
5. **Regular Reviews**: Keep requirements synchronized with reality

### File Management

1. **Meaningful Names**: descriptive-kebab-case-names.md
2. **Consistent Location**: Follow docs/ structure
3. **Version Control**: Commit requirements with code
4. **Link in Frontmatter**: Use YAML frontmatter for metadata
5. **Update Status**: Keep status fields current

---

## Summary

require-kit provides a complete requirements management workflow:

1. **Gather** requirements through interactive Q&A
2. **Formalize** into unambiguous EARS notation
3. **Generate** testable BDD scenarios
4. **Organize** into epic/feature hierarchy
5. **Export** to your chosen implementation system

**Key Principle**: Start with clear requirements, maintain traceability, and ensure testability.

Use standalone for requirements management, or integrate with guardkit for full requirements-to-implementation workflow.

---

For questions, issues, or integration guidance, see:
- [Integration Guide](../INTEGRATION-GUIDE.md)
- [README.md](../../README.md)
- [GitHub Issues](https://github.com/requirekit/require-kit/issues)
