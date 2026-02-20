# require-kit User Guide

**Version**: 2.0.0
**Last Updated**: 2026-02-20

## Table of Contents

1. [Introduction](#introduction)
2. [System Overview](#system-overview)
3. [Core Workflow](#core-workflow)
4. [Requirements Gathering](#requirements-gathering)
5. [EARS Notation](#ears-notation)
6. [BDD Scenario Generation](#bdd-scenario-generation)
7. [Epic/Feature Hierarchy](#epicfeature-hierarchy)
8. [Iterative Refinement](#iterative-refinement)
9. [Knowledge Graph Integration](#knowledge-graph-integration)
10. [Command Reference](#command-reference)
11. [Workflow Examples](#workflow-examples)
12. [Integration](#integration)
13. [Best Practices](#best-practices)

---

## Introduction

### What is require-kit?

require-kit is a standalone requirements management toolkit that provides structured approaches to capturing, formalizing, and organizing software requirements. It uses proven methodologies to ensure clear, testable, and traceable requirements throughout the development lifecycle.

### Core Capabilities

- **Interactive Requirements Gathering**: Conversational Q&A approach to capture complete requirements
- **EARS Notation Formalization**: Convert natural language to structured, unambiguous requirements
- **BDD/Gherkin Scenario Generation**: Create testable scenarios from requirements
- **Epic/Feature Hierarchy Management**: Organize requirements into logical project structures with three organisation patterns
- **Iterative Refinement**: Completeness scoring with targeted improvement suggestions for epics and features
- **Knowledge Graph**: Optional Graphiti integration for a queryable index of requirements
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

require-kit organizes requirements hierarchically and supports three organisation patterns so you can choose the right level of structure for each epic.

### Organisation Patterns

| Pattern | Structure | Best For |
|---------|-----------|----------|
| **Standard** | Epic → Feature → Task | Large epics with 8+ tasks across distinct capabilities |
| **Direct** | Epic → Task | Small, focused epics with 3-5 closely related tasks |
| **Mixed** | Epic → Feature + Task | Transitional epics migrating between patterns |

#### Standard Pattern (Epic → Feature → Task)

The default pattern groups tasks under features for maximum organisation.

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

**When to use:** Epic spans multiple distinct capabilities, more than 8 tasks expected, multiple team members, or feature-level progress tracking is needed.

#### Direct Pattern (Epic → Task)

Skip the feature layer for small, focused epics where features add unnecessary overhead.

```
Epic (Focused Business Objective)
├── Requirement (EARS Specification)
├── BDD Scenario (Acceptance Criteria)
├── Task (Implementation)
├── Task (Implementation)
└── Task (Implementation)
```

**When to use:** Epic has 3-5 closely related tasks, all tasks serve a single capability, or quick iteration matters more than detailed hierarchy.

```bash
# Create epic using direct pattern
/epic-create "Config Refactor" --pattern direct
```

#### Mixed Pattern (Epic → Feature + Task)

Combine features and direct tasks in one epic. Use during transitions but avoid as a permanent structure.

```
Epic (Business Objective)
├── Feature (Grouped Capability)
│   ├── Task (Implementation)
│   └── Task (Implementation)
├── Task (Direct — ungrouped)
└── Task (Direct — ungrouped)
```

**When to use:** Transitioning between direct and standard patterns during epic restructuring.

#### Pattern Selection Guide

| Epic Size | Recommended Pattern | Rationale |
|-----------|---------------------|-----------|
| 3-5 tasks | Direct | Features add overhead without value |
| 6-7 tasks | Either | Use judgement based on task relatedness |
| 8+ tasks | Standard | Features provide necessary organisation |

#### Migrating Between Patterns

Use `/epic-refine` to change an epic's organisation pattern:

```bash
# Promote direct → standard (group tasks into features)
/epic-refine EPIC-002 --pattern standard

# Simplify standard → direct (dissolve features)
/epic-refine EPIC-001 --pattern direct
```

### Creating Epics

#### Basic Epic Creation

```bash
/epic-create "User Management System"
```

#### With Pattern Flag

```bash
# Create with direct pattern (no feature layer)
/epic-create "Config Refactor" --pattern direct

# Create with metadata
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
3. Refine and improve: /epic-refine EPIC-001
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
3. Refine and improve: /feature-refine FEAT-001
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

## Iterative Refinement

### Why Iterative Refinement Matters

Well-structured requirements rarely emerge fully formed. require-kit's refinement commands help you improve epics and features through scored assessments, targeted questions, and a structured change review — so your requirements become clearer over time rather than remaining as first drafts.

### /epic-refine

Interactively refine an existing epic through completeness scoring, targeted questions, and change summaries.

#### Usage

```bash
/epic-refine EPIC-001
/epic-refine EPIC-001 --focus scope
/epic-refine EPIC-001 --focus risks
/epic-refine EPIC-001 --quick
```

#### Example Session

```
📊 Epic Completeness: EPIC-001 — User Management System

Overall Score: 62%

Dimensions:
  ✅ Business Objective  15/15 (100%)
  ✅ Scope               12/15 (80%)
  ⚠️  Success Criteria    8/20 (40%)   ← weakest
  ⚠️  Acceptance Criteria  6/15 (40%)
  ✅ Risk                 8/10 (80%)
  ✅ Constraints          8/10 (80%)
  ✅ Dependencies         4/5  (80%)
  ⚠️  Stakeholders        2/5  (40%)
  ✅ Organisation         5/5  (100%)

Q1 (Success Criteria): What measurable outcomes would indicate this epic is complete?
> Users can register, login, and manage their profiles with < 1s response times.

Q2 (Acceptance Criteria): What are the minimum conditions for a stakeholder to accept delivery?
> All authentication flows pass UAT; admin panel accessible to admin users only.

Changes to apply:
+ Added 2 success criteria items
+ Added stakeholder acceptance conditions

Apply changes? [Y]es / [N]o / [E]dit: Y

✅ Epic updated. New score: 84%
```

#### Completeness Dimensions (Epic)

| Dimension | Weight |
|-----------|--------|
| Business Objective | 15% |
| Scope | 15% |
| Success Criteria | 20% |
| Acceptance Criteria | 15% |
| Risk | 10% |
| Constraints | 10% |
| Dependencies | 5% |
| Stakeholders | 5% |
| Organisation | 5% |

#### Score Thresholds

| Score | Status |
|-------|--------|
| 80%+ | Good — ready for feature breakdown |
| 60–79% | Needs work — run another refinement cycle |
| Below 60% | Incomplete — significant gaps remain |

### /feature-refine

Interactively refine an existing feature specification with focus on acceptance criteria specificity, requirements traceability, and BDD scenario coverage.

#### Usage

```bash
/feature-refine FEAT-001
/feature-refine FEAT-001 --focus acceptance
/feature-refine FEAT-001 --focus bdd
/feature-refine FEAT-001 --focus traceability
/feature-refine FEAT-001 --quick
```

#### Example Session

```
📊 Feature Completeness: FEAT-001 — Login Functionality

Overall Score: 71%

Dimensions:
  ✅ Scope Within Epic       8/10 (80%)
  ⚠️  Acceptance Criteria   14/25 (56%)   ← weakest
  ✅ Requirements Traceability 16/20 (80%)
  ⚠️  BDD Coverage           9/15 (60%)
  ✅ Technical Considerations 12/15 (80%)
  ✅ Dependencies             9/10 (90%)
  ✅ Test Strategy             4/5 (80%)

Q1 (Acceptance Criteria): What specific conditions must be met for login to be considered working?
> Sessions must persist across page refreshes; HTTPS required; errors shown inline.

Q2 (BDD Coverage): Are edge cases like locked accounts and expired sessions covered in scenarios?
> Yes — locked accounts and session expiry both need explicit BDD scenarios.

Suggestions:
  → Run /formalize-ears to add missing EARS requirements
  → Run /generate-bdd to improve BDD coverage

Changes to apply:
+ Strengthened acceptance criteria (3 items)
+ Noted BDD gap for locked accounts and session expiry

Apply changes? [Y]es / [N]o / [E]dit: Y

✅ Feature updated. New score: 88%
```

#### Completeness Dimensions (Feature)

| Dimension | Weight |
|-----------|--------|
| Scope Within Epic | 10% |
| Acceptance Criteria | 25% |
| Requirements Traceability | 20% |
| BDD Coverage | 15% |
| Technical Considerations | 15% |
| Dependencies | 10% |
| Test Strategy | 5% |

### Three-Phase Refinement Flow

Both `/epic-refine` and `/feature-refine` follow the same three-phase flow:

1. **Current State Display** — Loads the spec, calculates a completeness score, and displays the assessment with visual indicators showing which dimensions need attention.
2. **Targeted Questions** — Presents questions one at a time starting from the weakest categories, with options to skip or finish early.
3. **Change Summary and Commit** — Displays proposed changes, offers apply options (Yes / No / Edit), updates the markdown file, and appends a `refinement_history` entry to the frontmatter.

### How Refinement Integrates with Other Commands

`/feature-refine` suggests related commands when gaps are detected:
- Suggests `/formalize-ears` when linked EARS requirements are missing
- Suggests `/generate-bdd` when BDD scenario coverage is low

`/epic-refine` detects organisation pattern issues and suggests improvements:
- Large direct-pattern epics (8+ tasks without features) — suggests grouping tasks into features
- Single-feature epics — suggests flattening to simplify hierarchy

---

## Knowledge Graph Integration

### What Graphiti Provides

Graphiti is an optional integration that creates a queryable index of your requirements. Rather than searching markdown files, you can query the knowledge graph to find related epics, trace requirements, or ask questions about your project structure.

Markdown files remain the **authoritative source of truth** — Graphiti is a derived index that you can rebuild at any time from your markdown files.

### Standalone vs Connected Modes

| Mode | How it works |
|------|-------------|
| **Standalone** | All requirements live as markdown files. No external dependencies. Full functionality without Graphiti. |
| **Connected** | Graphiti runs alongside require-kit. `/requirekit-sync` pushes markdown state to Graphiti for querying. Auto-sync available on create/refine. |

### /requirekit-sync

Re-read markdown files and push current state to Graphiti.

#### Usage

```bash
/requirekit-sync EPIC-001          # Sync a single epic
/requirekit-sync FEAT-002          # Sync a single feature
/requirekit-sync --all             # Sync everything
/requirekit-sync --all --dry-run   # Preview without writing
/requirekit-sync --all --verbose   # Show detailed output
```

#### How It Works

1. Checks that Graphiti is enabled in configuration
2. Scans `docs/epics/` and `docs/features/` for markdown files
3. Parses frontmatter and content from each file
4. Upserts episodes to Graphiti using the configured group ID
5. Displays a summary with sync results

#### Markdown-Authoritative Design

- **One-way sync** from markdown to Graphiti (markdown always wins)
- No conflict detection or bidirectional merge
- Graphiti serves as a queryable index rebuilt from markdown
- Run `/requirekit-sync --all` to fully rebuild after data loss

### Auto-Sync on Create/Refine

When Graphiti is configured with `sync_on_create: true` or `sync_on_refine: true`, the following commands auto-sync without any extra steps:

- `/epic-create` — auto-syncs if `sync_on_create: true`
- `/feature-create` — auto-syncs if `sync_on_create: true`
- `/epic-refine` — auto-syncs if `sync_on_refine: true`
- `/feature-refine` — auto-syncs if `sync_on_refine: true`

Use `/requirekit-sync` explicitly for manual or full-rebuild sync operations.

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
| `/epic-create` (direct pattern) | Create epic without feature layer | `/epic-create "Config Refactor" --pattern direct` |
| `/epic-status` | View epic progress | `/epic-status EPIC-001` |
| `/epic-refine` | Iteratively refine epic | `/epic-refine EPIC-001` |
| `/epic-sync` | Sync with PM tools | `/epic-sync EPIC-001 --jira` |

### Feature Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/feature-create` | Create new feature | `/feature-create "Login" epic:EPIC-001` |
| `/feature-status` | View feature progress | `/feature-status FEAT-001` |
| `/feature-refine` | Iteratively refine feature | `/feature-refine FEAT-001` |
| `/feature-sync` | Sync with PM tools | `/feature-sync FEAT-001 --linear` |
| `/feature-generate-tasks` | Generate task specs | `/feature-generate-tasks FEAT-001` |

### Hierarchy Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/hierarchy-view` | View project structure | `/hierarchy-view EPIC-001` |

### Sync Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/requirekit-sync` | Sync to Graphiti knowledge graph | `/requirekit-sync --all` |

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

### Example 3: Iterative Requirements Development

```bash
# Step 1: Gather requirements
/gather-requirements user-notifications

# Step 2: Formalize with EARS
/formalize-ears
# Output: REQ-050 through REQ-056

# Step 3: Create epic
/epic-create "Notification System"
# Output: docs/epics/EPIC-004.md

# Step 4: Check epic completeness and refine
/epic-refine EPIC-004
# → Score: 58% — answer targeted questions to improve
# → Score after refinement: 82% — ready to proceed

# Step 5: Create feature
/feature-create "Email Notifications" epic:EPIC-004 requirements:[REQ-050,REQ-051]
# Output: docs/features/FEAT-006.md

# Step 6: Check feature completeness and refine
/feature-refine FEAT-006
# → Score: 65% — acceptance criteria need strengthening
# → Suggests: /generate-bdd to improve BDD coverage
# → Score after refinement: 90%

# Step 7: Generate BDD scenarios
/generate-bdd FEAT-006
# Output: docs/bdd/BDD-006-email-notifications.feature

# Step 8: Review complete hierarchy with traceability
/hierarchy-view EPIC-004
# See: Epic → Feature → Requirements → BDD
```

### Example 4: Requirements Review Cycle

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

### Integration with Graphiti (Knowledge Graph)

For a queryable index of your requirements:

1. **Optional**: require-kit works fully without Graphiti
2. **Sync**: Run `/requirekit-sync --all` to populate Graphiti from your markdown files
3. **Auto-sync**: Configure `sync_on_create` and `sync_on_refine` for automatic updates
4. **Markdown wins**: Graphiti is derived from markdown — never edit it directly

See [Knowledge Graph Integration](#knowledge-graph-integration) for complete details.

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
