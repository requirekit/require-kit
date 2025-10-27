# Complete Command Usage Guide - v2.0 Enterprise Edition

## 📚 Table of Contents
1. [Quick Command Reference](#quick-command-reference)
2. [Epic Management Commands](#epic-management-commands)
3. [Feature Management Commands](#feature-management-commands)
4. [Enhanced Task Commands](#enhanced-task-commands)
5. [Hierarchy and Portfolio Commands](#hierarchy-and-portfolio-commands)
6. [Requirements and BDD Commands](#requirements-and-bdd-commands)
7. [Stack-Specific Commands](#stack-specific-commands)
8. [Complete Workflow Examples](#complete-workflow-examples)

## Quick Command Reference

### Enterprise Hierarchy Commands
| Command | Purpose | Example |
|---------|---------|---------|
| `/epic-create` | Create strategic epic with PM integration | `/epic-create "User Management" export:jira` |
| `/epic-status` | View epic progress with feature rollup | `/epic-status EPIC-001 --hierarchy` |
| `/epic-sync` | Sync epic with external PM tools | `/epic-sync EPIC-001 --force-push` |
| `/feature-create` | Create feature with epic linkage | `/feature-create "Auth" epic:EPIC-001` |
| `/feature-status` | View feature progress with tasks | `/feature-status FEAT-001 --breakdown` |
| `/feature-sync` | Sync feature and rollup to epic | `/feature-sync FEAT-001 --rollup-progress` |
| `/feature-generate-tasks` | Auto-generate tasks from specs | `/feature-generate-tasks FEAT-001` |

### Enhanced Task Commands
| Command | Purpose | Example |
|---------|---------|---------|
| `/task-create` | Create task with hierarchy context | `/task-create "Login API" feature:FEAT-001` |
| `/task-work` | Unified implementation + testing | `/task-work TASK-001 --mode=tdd` |
| `/task-status` | Monitor task with hierarchy context | `/task-status TASK-001 --hierarchy` |
| `/task-sync` | Sync task with cascade rollup | `/task-sync TASK-001 --rollup-progress` |
| `/task-complete` | Complete with validation + rollup | `/task-complete TASK-001` |

### Visualization Commands
| Command | Purpose | Example |
|---------|---------|---------|
| `/hierarchy-view` | View complete project hierarchy | `/hierarchy-view --mode=detailed` |
| `/portfolio-dashboard` | Executive portfolio overview | `/portfolio-dashboard --stakeholder=executive` |

### Legacy Commands (Still Supported)
| Command | Purpose | Example |
|---------|---------|---------|
| `/gather-requirements` | Interactive requirements elicitation | `/gather-requirements user-auth` |
| `/formalize-ears` | Convert to EARS notation | `/formalize-ears auth-requirements.md` |
| `/generate-bdd` | Create Gherkin scenarios | `/generate-bdd REQ-001` |

## Epic Management Commands

### `/epic-create` - Create Strategic Epic

**Basic Usage:**
```bash
/epic-create "User Management System"
```

**With PM Tool Integration:**
```bash
/epic-create "User Management System" priority:high export:jira
```

**With Full Configuration:**
```bash
/epic-create "User Management System" \
  priority:high \
  export:[jira,linear] \
  stakeholders:[pm@company.com,lead@company.com] \
  business_value:8 \
  effort_estimate:21
```

**Output:**
```
✅ Epic Created: EPIC-001

📋 Epic Details
Title: User Management System
Priority: high
Business Value: 8/10
Effort Estimate: 21 story points

🔗 External Integration
Jira Epic: PROJ-123 (created)
Linear Initiative: PROJECT-456 (created)

👥 Stakeholders
Product Owner: pm@company.com
Tech Lead: lead@company.com

📁 File Location
epics/active/EPIC-001-user-management-system.md

Next Steps:
1. Create features: /feature-create "Feature Name" epic:EPIC-001
2. Monitor progress: /epic-status EPIC-001
```

### `/epic-status` - View Epic Progress

**Basic Status:**
```bash
/epic-status EPIC-001
```

**With Hierarchy View:**
```bash
/epic-status EPIC-001 --hierarchy
```

**Output:**
```
📊 Epic Status: EPIC-001 - User Management System

🎯 Overview
Status: active
Progress: 63% complete (5/8 features completed)
Timeline: On track (3 days ahead of schedule)

🔧 Features Progress
✅ FEAT-001: User Authentication (100% - 4/4 tasks)
✅ FEAT-002: Password Reset (100% - 2/2 tasks)
🔄 FEAT-003: Role Management (75% - 3/4 tasks)
⏳ FEAT-004: Admin Dashboard (0% - 0/5 tasks)

🔗 External Tool Status
Jira Epic PROJ-123: In Progress (synced 2 hours ago)
Linear Initiative PROJECT-456: Active (synced 1 hour ago)

🚀 Next Actions
1. Complete TASK-015 in Role Management
2. Start Admin Dashboard feature planning
```

### `/epic-sync` - Sync with PM Tools

**Bidirectional Sync:**
```bash
/epic-sync EPIC-001
```

**Force Push Local Changes:**
```bash
/epic-sync EPIC-001 --force-push
```

**Pull Remote Changes First:**
```bash
/epic-sync EPIC-001 --pull-first
```

## Feature Management Commands

### `/feature-create` - Create Feature with Epic Linkage

**Basic Usage:**
```bash
/feature-create "User Authentication" epic:EPIC-001
```

**With Requirements:**
```bash
/feature-create "User Authentication" \
  epic:EPIC-001 \
  requirements:[REQ-001,REQ-002] \
  priority:high
```

**With Full Specification:**
```bash
/feature-create "User Authentication" \
  epic:EPIC-001 \
  requirements:[REQ-001,REQ-002] \
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
Requirements: REQ-001, REQ-002
BDD Scenarios: BDD-001

🔄 Automatic Task Generation
5 tasks generated from requirements and BDD scenarios:
- TASK-001: Implement login endpoint
- TASK-002: Create user registration
- TASK-003: Add session management
- TASK-004: Build login UI components
- TASK-005: Write integration tests

📁 File Location
features/active/FEAT-001-user-authentication.md

Next Steps:
1. Review generated tasks
2. Start implementation: /task-work TASK-001
```

### `/feature-generate-tasks` - Auto-Generate Tasks

**Generate from EARS and BDD:**
```bash
/feature-generate-tasks FEAT-001
```

**Interactive Generation:**
```bash
/feature-generate-tasks FEAT-001 --interactive
```

**With Custom Parameters:**
```bash
/feature-generate-tasks FEAT-001 \
  --max-tasks=8 \
  --include-tests \
  --epic-context
```

## Enhanced Task Commands

### `/task-work` - Unified Implementation Workflow

**Standard Mode (Default):**
```bash
/task-work TASK-001
```

**Test-Driven Development:**
```bash
/task-work TASK-001 --mode=tdd
```

**Behavior-Driven Development:**
```bash
/task-work TASK-001 --mode=bdd
```

**With Coverage Threshold:**
```bash
/task-work TASK-001 --mode=tdd --coverage-threshold=90
```

**Output (TDD Mode):**
```
🔄 Starting Task: TASK-001 - Implement login endpoint
Mode: Test-Driven Development (TDD)

📊 TDD Cycle 1: RED
✅ Created failing test: test_login_endpoint_validation
❌ Test Status: FAILING (expected)

📊 TDD Cycle 1: GREEN
✅ Implemented: LoginEndpoint.authenticate()
✅ Test Status: PASSING

📊 TDD Cycle 1: REFACTOR
✅ Refactored: Extracted validation logic
✅ All tests still passing

🎯 Quality Gates
✅ Test Coverage: 92% (threshold: 80%)
✅ All Tests Passing: 15/15
✅ Code Complexity: 7 (limit: 10)
✅ Type Checking: Passed

📈 Progress Update
Task: TASK-001 → IN_REVIEW
Feature: FEAT-001 → 60% complete (3/5 tasks)
Epic: EPIC-001 → 47% complete
```

### `/task-status` - Monitor with Hierarchy Context

**Basic Status:**
```bash
/task-status TASK-001
```

**With Hierarchy Context:**
```bash
/task-status TASK-001 --hierarchy
```

**Output:**
```
📋 Task Status: TASK-001 - Implement login endpoint

🎯 Task Details
Status: in_review
Progress: Implementation complete, awaiting review
Quality Gates: 4/4 passed

🔗 Hierarchy Context
Epic: EPIC-001 - User Management System (47% complete)
Feature: FEAT-001 - User Authentication (60% complete)
Position: Task 3 of 5 in feature

🧪 Quality Metrics
Test Coverage: 92%
Complexity Score: 7/10
Performance: 150ms (target: <200ms)

🔄 Recent Activity
- 15 minutes ago: All quality gates passed
- 30 minutes ago: Implementation completed
- 1 hour ago: TDD cycle 3 completed

⏭️ Next Steps
1. Code review by @tech-lead
2. Integration testing
3. Complete task: /task-complete TASK-001
```

## Hierarchy and Portfolio Commands

### `/hierarchy-view` - Complete Project Visualization

**Overview Mode:**
```bash
/hierarchy-view
```

**Detailed Mode:**
```bash
/hierarchy-view --mode=detailed
```

**Timeline View:**
```bash
/hierarchy-view --mode=timeline
```

**Dependencies View:**
```bash
/hierarchy-view --mode=dependencies
```

**Output (Detailed Mode):**
```
📊 Project Hierarchy - MyProject

├── 🎯 EPIC-001: User Management System (63% complete)
│   ├── 🔧 FEAT-001: User Authentication (85% complete)
│   │   ├── ✅ TASK-001: Implement login endpoint (completed)
│   │   ├── ✅ TASK-002: Create user registration (completed)
│   │   ├── ✅ TASK-003: Add session management (completed)
│   │   ├── 🔄 TASK-004: Build login UI (in_progress)
│   │   └── ⏳ TASK-005: Integration tests (backlog)
│   ├── 🔧 FEAT-002: Password Reset (100% complete)
│   │   ├── ✅ TASK-006: Reset endpoint (completed)
│   │   └── ✅ TASK-007: Reset UI (completed)
│   └── 🔧 FEAT-003: Role Management (25% complete)
│       ├── ✅ TASK-008: Role model (completed)
│       ├── ⏳ TASK-009: RBAC logic (backlog)
│       └── ⏳ TASK-010: Admin interface (backlog)
└── 🎯 EPIC-002: Reporting System (0% complete)
    └── 🔧 FEAT-004: Basic Reports (planning)

🎯 Summary
Total Epics: 2 (1 active, 1 planning)
Total Features: 4 (3 active, 1 planning)
Total Tasks: 10 (4 completed, 1 in_progress, 5 backlog)
Overall Progress: 42% complete
```

### `/portfolio-dashboard` - Executive Overview

**Executive View:**
```bash
/portfolio-dashboard --stakeholder=executive
```

**Development Team View:**
```bash
/portfolio-dashboard --stakeholder=development
```

**Output (Executive View):**
```
📈 Portfolio Dashboard - Executive Summary

🎯 Strategic Overview
Active Epics: 3
Total Business Value: 24 points
Delivered Value: 15 points (62.5%)
ROI Target: On track for 150% ROI

📊 Progress Metrics
Overall Portfolio: 58% complete
On Schedule: 2 epics
At Risk: 1 epic (EPIC-003 - timeline concerns)
Blocked: 0 epics

👥 Resource Allocation
Development: 8 engineers (fully allocated)
QA: 2 engineers (75% allocated)
Product: 1 PM (overallocated at 110%)

🎲 Risk Assessment
🔴 High Risk: Resource constraint in QA
🟡 Medium Risk: Third-party integration delays
🟢 Low Risk: Technology stack maturity

💰 Business Metrics
Budget Utilization: 67% of allocated budget
Value Delivery Rate: 2.1 points/week (target: 2.0)
Time to Market: 3 weeks ahead of schedule

📅 Key Milestones
✅ MVP Feature Set: Completed (2 weeks early)
🔄 Beta Release: In progress (on track)
⏳ GA Release: Scheduled for 2024-Q1

🚀 Recommendations
1. Add 1 QA engineer to reduce risk
2. Prioritize EPIC-002 for Q4 delivery
3. Consider scope reduction for EPIC-003
```

## Requirements Gathering

### Basic Usage
```bash
/gather-requirements
```

### With Feature Name
```bash
/gather-requirements user-authentication
```

### Complete Example Session

```markdown
Claude: Let's gather requirements for user-authentication. What problem are we solving?

You: We need users to securely log into our web application with email and password.

Claude: Who will be using this authentication system?

You: Both regular users and administrators. Admins need access to an admin panel.

Claude: What authentication methods should we support?

You: Initially just email/password, but we want to add OAuth and 2FA later.

Claude: What should happen when authentication fails?

You: Show an error message and lock the account after 3 failed attempts.

Claude: What are the performance requirements?

You: Login should complete within 1 second, and support 1000 concurrent users.

Claude: What about session management?

You: Sessions should last 24 hours with a "remember me" option for 30 days.

Claude: Any security requirements?

You: Yes - passwords must be 8+ characters with complexity requirements, and all traffic must be HTTPS.

Claude: Great! I've captured these requirements. Here's the summary:

## Requirements Summary

### Functional Requirements
- User login with email/password
- Admin users with elevated access
- Account lockout after 3 failed attempts
- Session management (24hr default, 30 day remember)
- Future: OAuth and 2FA support

### Non-Functional Requirements
- Performance: <1 second login
- Scalability: 1000 concurrent users
- Security: Password complexity, HTTPS only
- Availability: 99.9% uptime

Ready to formalize these with /formalize-ears
```

## EARS Formalization

### Basic Usage
```bash
/formalize-ears
```

### From Specific File
```bash
/formalize-ears docs/requirements/draft/auth.md
```

### Complete Example Output

```markdown
## Formalized EARS Requirements

### REQ-001: User Login [Event-Driven]
**When** a user submits valid email and password credentials via the login form, 
**the system** shall authenticate the user and create a session within 1 second.

**Metadata:**
- Priority: High
- Epic: AUTH-001
- Test: BDD-001

### REQ-002: Invalid Login Attempt [Event-Driven]
**When** a user submits invalid credentials,
**the system** shall display an error message "Invalid email or password" 
and increment the failed attempt counter for that email.

### REQ-003: Account Lockout [Unwanted Behavior]
**If** a user submits invalid credentials 3 times within 5 minutes,
**then the system** shall lock the account for 15 minutes,
display "Account locked due to multiple failed attempts",
and send a security alert email to the account owner.

### REQ-004: Admin Access [State-Driven]
**While** a user session has admin role privileges,
**the system** shall display the admin panel navigation option
and allow access to administrative functions.

### REQ-005: Session Duration [State-Driven]
**While** a user session is active without "remember me",
**the system** shall maintain the session for 24 hours from last activity,
then require re-authentication.

### REQ-006: Remember Me [Optional Feature]
**Where** the user has selected "remember me" during login,
**the system** shall maintain the session for 30 days
and refresh the token on each visit.

### REQ-007: Concurrent Users [Ubiquitous]
**The system** shall support at least 1000 concurrent authenticated users
without performance degradation below 1 second response time.

### REQ-008: Password Complexity [Ubiquitous]
**The system** shall require passwords to be at least 8 characters
and contain at least one uppercase, one lowercase, one number, and one special character.

### REQ-009: Secure Transport [Ubiquitous]
**The system** shall only accept authentication requests over HTTPS connections
and reject any HTTP authentication attempts.

### REQ-010: Session Timeout [Unwanted Behavior]
**If** a user session expires,
**then the system** shall redirect to the login page with message "Session expired, please log in again"
and preserve the intended destination URL for post-login redirect.
```

### Validation Output
```markdown
✅ Requirements Validation Results:
- All requirements are atomic (single behavior)
- All requirements are testable
- All requirements have measurable criteria
- No conflicts detected
- Coverage: Authentication flow complete

⚠️ Suggestions:
- Consider adding requirement for password reset
- Consider adding requirement for email verification
- Consider adding audit logging requirement
```

## BDD Generation

### Basic Usage
```bash
/generate-bdd
```

### For Specific Requirement
```bash
/generate-bdd REQ-001
```

### For Epic
```bash
/generate-bdd --epic AUTH-001
```

### Complete Example Output

```gherkin
# Generated from: REQ-001, REQ-002, REQ-003
# File: docs/bdd/features/authentication.feature

@epic-AUTH-001 @authentication
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
      | inactive@example.com | Inactive0!  | user    | inactive |

  @requirement-REQ-001 @happy-path @smoke
  Scenario: Successful user login
    Given I am on the login page
    When I enter "user@example.com" in the email field
    And I enter "Valid123!" in the password field
    And I click the "Sign In" button
    Then I should be redirected to "/dashboard"
    And I should see "Welcome back!" message
    And a session cookie should be created
    And the authentication should complete within 1 second

  @requirement-REQ-001 @happy-path
  Scenario: Successful admin login
    Given I am on the login page
    When I enter "admin@example.com" in the email field
    And I enter "Admin456!" in the password field
    And I click the "Sign In" button
    Then I should be redirected to "/admin/dashboard"
    And I should see the admin navigation menu
    And the session should have admin privileges

  @requirement-REQ-002 @error-handling
  Scenario: Login with invalid password
    Given I am on the login page
    When I enter "user@example.com" in the email field
    And I enter "WrongPassword!" in the password field
    And I click the "Sign In" button
    Then I should remain on "/login"
    And I should see error message "Invalid email or password"
    And no session cookie should be created
    And the failed attempt should be logged

  @requirement-REQ-002 @error-handling
  Scenario: Login with non-existent email
    Given I am on the login page
    When I enter "notfound@example.com" in the email field
    And I enter "Password123!" in the password field
    And I click the "Sign In" button
    Then I should remain on "/login"
    And I should see error message "Invalid email or password"
    And the response should not reveal the email doesn't exist

  @requirement-REQ-003 @security @critical
  Scenario: Account lockout after failed attempts
    Given I am on the login page
    And the user "user@example.com" has 2 failed login attempts in the last 5 minutes
    When I enter "user@example.com" in the email field
    And I enter "WrongPassword!" in the password field
    And I click the "Sign In" button
    Then I should see error message "Account locked due to multiple failed attempts"
    And the account should be locked for 15 minutes
    And a security alert email should be sent to "user@example.com"
    And subsequent login attempts should be rejected

  @requirement-REQ-003 @security
  Scenario: Account unlock after timeout
    Given the user "user@example.com" was locked 16 minutes ago
    When I enter "user@example.com" in the email field
    And I enter "Valid123!" in the password field
    And I click the "Sign In" button
    Then I should be successfully authenticated
    And the failed attempt counter should be reset

  @requirement-REQ-006 @optional-feature
  Scenario: Login with remember me option
    Given I am on the login page
    When I enter "user@example.com" in the email field
    And I enter "Valid123!" in the password field
    And I check the "Remember me" checkbox
    And I click the "Sign In" button
    Then I should be redirected to "/dashboard"
    And a persistent session cookie should be created
    And the cookie should expire in 30 days
    And the cookie should be marked as secure and httpOnly

  @requirement-REQ-010 @session-management
  Scenario: Redirect after session expiry
    Given I am logged in as "user@example.com"
    And I am on page "/profile/settings"
    When my session expires after 24 hours
    And I try to access "/profile/settings"
    Then I should be redirected to "/login"
    And I should see message "Session expired, please log in again"
    And the return URL should be set to "/profile/settings"

  @requirement-REQ-010 @session-management
  Scenario: Successful redirect after re-login
    Given I was redirected to login from "/profile/settings"
    When I successfully log in
    Then I should be redirected to "/profile/settings"
    And not to the default dashboard

  @requirement-REQ-007 @performance @load-testing
  Scenario Outline: Concurrent user logins
    Given <users> users are attempting to login simultaneously
    When all users submit valid credentials
    Then all authentications should complete within <time> seconds
    And the system should remain responsive

    Examples:
      | users | time |
      | 100   | 1    |
      | 500   | 1    |
      | 1000  | 1    |

  @requirement-REQ-008 @validation
  Scenario Outline: Password complexity validation
    Given I am on the registration page
    When I enter "<password>" as my password
    Then I should see validation "<result>"

    Examples:
      | password      | result                                          |
      | short         | Password must be at least 8 characters         |
      | lowercase123! | Password must contain an uppercase letter      |
      | UPPERCASE123! | Password must contain a lowercase letter       |
      | NoNumbers!    | Password must contain a number                 |
      | NoSpecial123  | Password must contain a special character      |
      | Valid123!     | Password meets requirements                    |
```

### Step Definitions Generated

```typescript
// Generated step definitions template
// File: tests/steps/authentication.steps.ts

import { Given, When, Then } from '@cucumber/cucumber';
import { expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { DashboardPage } from '../pages/DashboardPage';

Given('I am on the login page', async function() {
  await this.page.goto('/login');
  this.loginPage = new LoginPage(this.page);
});

Given('the following users exist:', async function(dataTable) {
  const users = dataTable.hashes();
  await this.testDatabase.seedUsers(users);
});

When('I enter {string} in the email field', async function(email: string) {
  await this.loginPage.enterEmail(email);
});

When('I enter {string} in the password field', async function(password: string) {
  await this.loginPage.enterPassword(password);
});

When('I click the {string} button', async function(buttonText: string) {
  await this.loginPage.clickButton(buttonText);
});

Then('I should be redirected to {string}', async function(path: string) {
  await expect(this.page).toHaveURL(path);
});

Then('I should see {string} message', async function(message: string) {
  await expect(this.page.locator(`text=${message}`)).toBeVisible();
});

Then('a session cookie should be created', async function() {
  const cookies = await this.page.context().cookies();
  const sessionCookie = cookies.find(c => c.name === 'session');
  expect(sessionCookie).toBeDefined();
  expect(sessionCookie?.httpOnly).toBe(true);
  expect(sessionCookie?.secure).toBe(true);
});

Then('the authentication should complete within {int} second(s)', async function(seconds: number) {
  expect(this.responseTime).toBeLessThan(seconds * 1000);
});
```

## Test Execution

### Complete Test Execution Examples

#### Run All Tests
```bash
/execute-tests

Output:
═══════════════════════════════════════════════════════════════
                    TEST EXECUTION REPORT
═══════════════════════════════════════════════════════════════
Started: 2024-01-19 14:30:00
Environment: Development
Runner: Local

PHASE 1: Linting & Formatting
═══════════════════════════════════════════════════════════════
✅ ESLint.......................... PASSED [1.2s]
✅ Prettier........................ PASSED [0.8s]
✅ TypeScript Compiler............ PASSED [3.4s]

PHASE 2: Unit Tests
═══════════════════════════════════════════════════════════════
Running: 156 tests across 24 files

✅ auth.service.test.ts........... 12/12 passed [245ms]
✅ user.service.test.ts........... 8/8 passed [189ms]
✅ session.service.test.ts........ 15/15 passed [302ms]
✅ validators.test.ts............. 23/23 passed [156ms]
⚠️ cache.service.test.ts.......... 7/8 passed [445ms]
   ❌ Failed: Should evict LRU items when full

Unit Test Summary: 155/156 passed (99.4%)
Coverage: 87.3% statements, 82.1% branches

PHASE 3: Integration Tests
═══════════════════════════════════════════════════════════════
Running: 45 integration tests

✅ API Authentication.............. 8/8 passed [1.2s]
✅ Database Transactions........... 12/12 passed [2.3s]
✅ Session Management.............. 6/6 passed [0.9s]
❌ Rate Limiting................... 4/5 passed [3.1s]
   ❌ Failed: Should handle burst traffic

Integration Summary: 44/45 passed (97.8%)

PHASE 4: BDD Scenarios
═══════════════════════════════════════════════════════════════
Feature: User Authentication
  ✅ Successful user login.................. [245ms]
  ✅ Login with invalid password............ [123ms]
  ✅ Account lockout after failed attempts.. [456ms]
  ✅ Remember me option..................... [189ms]
  ✅ Session expiry redirect................ [567ms]

Feature: User Management  
  ✅ Create new user........................ [234ms]
  ✅ Update user profile.................... [345ms]
  ⚠️ Delete user account.................... [5234ms] SLOW
  
BDD Summary: 8/8 scenarios passed
Total Steps: 52/52 passed

PHASE 5: End-to-End Tests
═══════════════════════════════════════════════════════════════
Browser: Chromium

✅ Complete user journey............. PASSED [8.5s]
✅ Admin workflow.................... PASSED [6.2s]
✅ Password reset flow............... PASSED [4.3s]
❌ Concurrent user test.............. FAILED [timeout]

E2E Summary: 3/4 passed (75%)

QUALITY GATES
═══════════════════════════════════════════════════════════════
✅ Code Coverage............. 87.3% > 80%    [PASSED]
✅ Unit Test Pass Rate....... 99.4% > 95%    [PASSED]
⚠️ Integration Pass Rate..... 97.8% > 99%    [WARNING]
❌ E2E Pass Rate............. 75.0% < 90%    [FAILED]
✅ Performance............... 189ms < 200ms  [PASSED]
✅ Security Scan............. No issues      [PASSED]
✅ Complexity................ 7.2 < 10       [PASSED]

Overall Status: FAILED (1 gate failed, 1 warning)

FAILED TESTS DETAIL
═══════════════════════════════════════════════════════════════
1. cache.service.test.ts > Should evict LRU items when full
   Expected: ['item2', 'item3', 'item4']
   Received: ['item1', 'item3', 'item4']
   
   Suggested Fix:
   - Check LRU eviction logic in cache.service.ts:45
   - Verify timestamp comparison

2. Rate Limiting > Should handle burst traffic
   Expected: 429 status after 100 requests
   Received: 200 status for all requests
   
   Suggested Fix:
   - Review rate limit configuration
   - Check Redis connection for rate limit store

3. E2E > Concurrent user test
   Error: Timeout exceeded 30000ms
   
   Suggested Fix:
   - Increase timeout for load tests
   - Check for deadlocks in concurrent scenarios

RECOMMENDATIONS
═══════════════════════════════════════════════════════════════
1. Fix failing tests before merge
2. Investigate slow BDD test (>5s)
3. Add retry logic for flaky E2E test
4. Increase integration test coverage

Total Duration: 4m 32s
Report saved to: test-results/report-2024-01-19-143000.html
```

#### Run Specific Test Level
```bash
/execute-tests --level unit --coverage

Output:
Running Unit Tests with Coverage...
════════════════════════════════════════

 PASS  src/auth/auth.service.test.ts (12 tests, 245ms)
 PASS  src/user/user.service.test.ts (8 tests, 189ms)
 PASS  src/utils/validators.test.ts (23 tests, 156ms)

Test Suites: 24 passed, 24 total
Tests:       156 passed, 156 total
Time:        28.5s

Coverage Report:
════════════════════════════════════════
File                  | % Stmts | % Branch | % Funcs | % Lines |
----------------------|---------|----------|---------|---------|
All files             |   87.32 |    82.14 |   89.47 |   87.32 |
 src/auth/            |   92.31 |    87.50 |   95.00 |   92.31 |
  auth.service.ts     |   91.67 |    85.71 |  100.00 |   91.67 |
  auth.controller.ts  |   93.33 |    90.00 |   90.00 |   93.33 |
 src/user/            |   85.71 |    78.57 |   87.50 |   85.71 |
  user.service.ts     |   84.62 |    75.00 |   85.71 |   84.62 |
  user.repository.ts  |   87.50 |    83.33 |   90.00 |   87.50 |
 src/utils/           |   83.33 |    80.00 |   85.71 |   83.33 |
  validators.ts       |   81.82 |    77.78 |   83.33 |   81.82 |
  helpers.ts          |   85.71 |    83.33 |   88.89 |   85.71 |

✅ Coverage threshold met: 87.32% > 80%
```

## State Management

### Complete State Update Examples

#### Update Task Status
```bash
/update-state task TASK-001 complete

Output:
════════════════════════════════════════
         TASK STATUS UPDATE
════════════════════════════════════════

Task: TASK-001 - Implement login form
Previous Status: in-progress
New Status: ✅ COMPLETE

Related Updates:
────────────────────────────────────────
📊 Feature Progress: Authentication
   Before: 60% [██████    ]
   After:  80% [████████  ]

📈 Sprint Velocity:
   Before: 12/21 points
   After:  15/21 points

📋 Requirements Completed:
   - REQ-001: User login (100% implemented)
   - REQ-002: Error handling (100% implemented)

🧪 Test Coverage:
   - Unit Tests: 18/18 passing
   - Integration: 5/5 passing
   - BDD Scenarios: 3/3 passing

Files Updated:
────────────────────────────────────────
✅ docs/state/current-sprint.md
✅ docs/state/changelog.md
✅ docs/state/metrics.json

Notifications Sent:
────────────────────────────────────────
📧 Team notified of task completion
📊 Dashboard updated
🔄 GitHub issue #23 updated
```

#### Update Sprint Progress
```bash
/update-state sprint progress

Output:
════════════════════════════════════════
         SPRINT 3 PROGRESS
════════════════════════════════════════
Sprint 3: Authentication Implementation
Duration: Jan 15 - Jan 29, 2024
Day 5 of 14

VELOCITY
────────────────────────────────────────
Planned:    21 points
Completed:  15 points
Remaining:   6 points
Pace:       ON TRACK ✅

Progress:   71% [███████░░░]

EPIC BREAKDOWN
────────────────────────────────────────
User Management [85% Complete]
├─ Authentication [100% ✅]
│  ├─ TASK-001: Login form ✅
│  ├─ TASK-002: JWT tokens ✅
│  └─ TASK-003: Session mgmt ✅
├─ Authorization [60% 🔄]
│  ├─ TASK-004: RBAC ✅
│  ├─ TASK-005: Permissions 🔄
│  └─ TASK-006: Admin panel ⏳
└─ Profile Mgmt [0% ⏳]

QUALITY METRICS
────────────────────────────────────────
Code Coverage:      87.3% ✅ (target: 80%)
Test Pass Rate:     98.2% ✅ (target: 95%)
Code Complexity:     7.2 ✅ (target: <10)
Performance:       189ms ✅ (target: <200ms)

BLOCKERS & RISKS
────────────────────────────────────────
⚠️ TASK-005: Waiting for security review
🔴 TASK-008: API specs not finalized

BURNDOWN CHART
────────────────────────────────────────
Points
21 |█
18 |██░
15 |███░░
12 |█████░░
 9 |███████░░
 6 |█████████░░ ← Current
 3 |████████████░
 0 |██████████████
   |1 2 3 4 5 6 7 8 9 10 11 12 13 14
   Days

Projected Completion: On Schedule ✅
```

## Stack-Specific Commands

### React Stack Commands
```bash
# Create a new component with advanced patterns
/create-component UserProfile
Output: Created with error boundary, SSE hook, performance optimization

# Add SSE endpoint connection
/add-sse-endpoint /api/notifications
Output: Created useSSE hook with proper error handling and completion events

# Generate accessibility tests
/generate-a11y-tests UserProfile
Output: Created WCAG 2.1 AA compliance tests
```

### Python Stack Commands
```bash
# Create LangGraph workflow
/create-workflow document-processing
Output: Created workflow with nodes, edges, and state management

# Add SSE endpoint
/create-sse-endpoint stream-results
Output: Created with proper completion events and error handling

# Generate factory
/create-factory AgentFactory
Output: Created factory pattern with configuration
```

### .NET Microservice Commands
```bash
# Create FastEndpoint
/create-endpoint GetProductById
Output: Created with Either monad, validation, and OpenTelemetry

# Add health check
/add-health-check database
Output: Created health check with detailed status reporting

# Generate integration test
/create-integration-test GetProductById
Output: Created with WebApplicationFactory and test data
```

### .NET MAUI Commands
```bash
# Create page with ViewModel
/create-page ProductDetail
Output: Created XAML, ViewModel with UseCase, and navigation

# Add UseCase
/create-usecase GetProductDetails
Output: Created with Either monad, caching, and error handling

# Generate integration test
/create-feature-test ProductDetail
Output: Created Outside-In test with HTTP mocking
```

## Complete Workflow Examples

### Example 1: Building Authentication Feature

```bash
# Step 1: Gather Requirements
/gather-requirements authentication

# Step 2: Formalize to EARS
/formalize-ears
Output: 10 EARS requirements generated

# Step 3: Generate BDD Scenarios
/generate-bdd
Output: 15 scenarios across 3 feature files

# Step 4: Review generated artifacts
Files created:
- docs/requirements/approved/AUTH-001.md
- docs/bdd/features/authentication.feature
- docs/bdd/features/session-management.feature
- docs/bdd/features/password-reset.feature

# Step 5: Implement feature (React)
/create-component LoginForm
/create-hook useAuth
/create-service AuthService

# Step 6: Run tests
/execute-tests --level unit
Output: 24/24 tests passing

# Step 7: Run integration tests
/execute-tests --level integration
Output: 8/8 tests passing

# Step 8: Run BDD tests
/execute-tests --level bdd
Output: 15/15 scenarios passing

# Step 9: Update state
/update-state feature AUTH-001 complete
Output: Feature marked complete, sprint progress updated
```

### Example 2: API Development (Python)

```bash
# Step 1: Requirements
/gather-requirements api-endpoints

# Step 2: EARS
/formalize-ears
Output: REQ-API-001 through REQ-API-008

# Step 3: Implementation
/create-endpoint products --method GET POST PUT DELETE
/create-service ProductService
/create-repository ProductRepository
/create-workflow product-validation

# Step 4: Add streaming
/create-sse-endpoint product-updates
Output: SSE endpoint with completion events

# Step 5: Testing
/execute-tests
Output: All tests passing, coverage 92%

# Step 6: Documentation
/generate-api-docs
Output: OpenAPI specification generated
```

### Example 3: Mobile App Feature (MAUI)

```bash
# Step 1: Requirements for mobile shopping cart
/gather-requirements shopping-cart-mobile

# Step 2: EARS formalization
/formalize-ears
Output: 12 requirements for cart management

# Step 3: Create UI and logic
/create-page ShoppingCart
/create-usecase AddToCart
/create-usecase RemoveFromCart
/create-usecase CalculateTotal
/create-service CartService

# Step 4: Integration tests
/create-feature-test shopping-cart-flow
Output: Outside-In test with mocked API

# Step 5: Run tests
/execute-tests --platform android
Output: All tests passing on Android emulator

# Step 6: Performance check
/execute-tests --performance
Output: Page load: 423ms ✅, Memory: 145MB ✅
```

## Tips and Best Practices

### Requirements Gathering
- Be specific about user roles
- Include performance requirements
- Don't forget error scenarios
- Mention security constraints
- Consider future extensibility

### EARS Formalization
- Keep each requirement atomic
- Use measurable criteria
- Include timing requirements
- Cover error conditions
- Link to epics and features

### BDD Generation
- Review scenarios with stakeholders
- Ensure scenarios are independent
- Use concrete examples
- Tag appropriately for test organization
- Keep scenarios focused

### Test Execution
- Run tests frequently
- Fix failures immediately
- Monitor coverage trends
- Optimize slow tests
- Use parallel execution for speed

### State Management
- Update immediately after changes
- Include context in updates
- Link to evidence (PRs, tests)
- Communicate blockers quickly
- Keep metrics current

## Command Shortcuts

Create aliases in `.claude/config.json`:
```json
{
  "aliases": {
    "gr": "gather-requirements",
    "fe": "formalize-ears", 
    "gb": "generate-bdd",
    "et": "execute-tests",
    "us": "update-state",
    "cc": "create-component",
    "ce": "create-endpoint",
    "cu": "create-usecase"
  }
}
```

Then use:
```bash
/gr authentication
/fe
/gb REQ-001
/et --coverage
/us task TASK-001 complete
```

## Troubleshooting Commands

### Debug Mode
```bash
/gather-requirements --debug
# Shows internal processing steps

/execute-tests --verbose
# Detailed test output

/update-state --dry-run
# Preview changes without applying
```

### Recovery Commands
```bash
/rollback-state
# Revert last state change

/reset-tests
# Clear test cache and retry

/validate-requirements
# Check requirement consistency

/repair-links
# Fix broken requirement-test links
```

## Integration with CI/CD

### GitHub Actions
```yaml
- name: Validate Requirements
  run: agentecflow validate-ears

- name: Run Quality Gates
  run: agentecflow execute-tests --ci

- name: Update State
  run: agentecflow update-state --from-ci
```

### Pre-commit Hooks
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check EARS compliance
agentecflow validate-ears

# Run quick tests
agentecflow execute-tests --fast

# Update state
agentecflow update-state --auto
```

---

This comprehensive guide covers all aspects of using the AI Engineer commands with detailed examples and complete workflows.
