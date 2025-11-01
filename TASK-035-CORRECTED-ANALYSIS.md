# TASK-035 Corrected Analysis - Documentation Levels for require-kit

**Date**: 2025-11-01
**Status**: IRRELEVANT TO REQUIRE-KIT (After Deeper Review)
**Previous Analysis**: INCORRECT - Misunderstood the architecture

## Critical Realization

After reviewing the `/task-work` command documentation, I now understand the architecture:

```
┌─────────────────┐         ┌──────────────────┐
│   taskwright    │         │   require-kit    │
│                 │         │                  │
│ - /task-work    │◄───────►│ - /gather-req    │
│ - /task-create  │  reads  │ - /formalize-ears│
│ - /task-complete│  from   │ - /generate-bdd  │
│ - Quality gates │         │ - Epic/Feature   │
│ - Test execution│         │   management     │
└─────────────────┘         └──────────────────┘
   Execution side              Requirements side
```

## Key Architecture Facts

1. **taskwright owns /task-work**: Task execution, quality gates, test orchestration
2. **require-kit provides inputs**: Requirements (EARS), BDD scenarios, epic/feature context
3. **Bidirectional optional**: taskwright can read from require-kit when both installed
4. **Separate concerns**:
   - taskwright = DO the work (implementation, testing, quality)
   - require-kit = DEFINE the work (requirements, scenarios, hierarchy)

## Why TASK-035 is IRRELEVANT to require-kit

### Original TASK-035 Scope
- **Target**: `/task-work` command (in taskwright)
- **Agents**: 7 agents used during task execution workflow
- **Purpose**: Reduce verbose output during implementation phases
- **Where**: taskwright repository, NOT require-kit

### What TASK-035 Does
TASK-035 adds documentation levels to the **execution workflow**:
- Phase 1: Requirements Analysis (uses requirements-analyst from require-kit)
- Phase 2: Implementation Planning
- Phase 2.5: Architectural Review
- Phase 3: Implementation
- Phase 4: Test Execution
- Phase 5: Code Review

All these phases are **taskwright's responsibility**.

### What require-kit Does
require-kit provides **inputs** to taskwright:
- EARS requirements (via requirements-analyst)
- BDD scenarios (via bdd-generator)
- Epic/feature hierarchy
- Acceptance criteria

These are consumed by taskwright's `/task-work` command.

## The Confusion

My previous analysis was **WRONG** because I thought:
- ❌ require-kit runs the execution workflow
- ❌ require-kit needs documentation levels for task-work
- ❌ require-kit has 7 agents for execution

**Reality**:
- ✅ require-kit only gathers requirements
- ✅ taskwright runs the execution workflow
- ✅ require-kit has 2 agents (requirements-analyst, bdd-generator)

## What Actually Matters for require-kit

The **real** question is: Do require-kit's **requirements gathering commands** need documentation levels?

Let's analyze the actual require-kit commands:

### Commands Analysis

#### 1. /gather-requirements
**What it does**: Interactive Q&A to gather requirements
**Output**: Raw requirements (unformalized)
**Verbosity**: Moderate - Q&A session
**Documentation level impact**: LOW - Interactive session, not much to reduce

#### 2. /formalize-ears
**What it does**: Convert requirements to EARS notation
**Output**: Formalized EARS requirements
**Verbosity**: Can be verbose with examples and rationale
**Documentation level impact**: MEDIUM - Could benefit from concise mode

**Example verbose output**:
```markdown
## REQ-042: User Authentication

### EARS Pattern: Event-Driven
**Format**: When [trigger], the [system] shall [response]

**Requirement Statement**:
When a user submits valid credentials through the authentication endpoint,
the system shall authenticate the user, generate a JWT token with 24-hour
expiration, and return the token in the response body.

**Rationale**:
User authentication is critical for securing the application. We use JWT
tokens for stateless authentication, allowing for scalability and easier
microservices integration. The 24-hour expiration balances security with
user convenience...

**Acceptance Criteria**:
1. Valid credentials accepted
2. Invalid credentials rejected
3. Token generated within 1 second
4. Token includes user ID and role claims...

**Examples**:
- Valid login: user@example.com / correct_password → JWT token
- Invalid login: user@example.com / wrong_password → 401 error
- Missing fields: {} → 400 error

**Traceability**:
- Epic: EPIC-010 (User Management)
- Feature: FEAT-042 (Authentication)
- Related Requirements: REQ-041 (Session Management), REQ-043 (Password Reset)
```

**Could be concise**:
```markdown
## REQ-042: User Authentication

**EARS**: When valid credentials submitted, system shall authenticate, generate JWT (24h expiry), return token.

**Acceptance Criteria**:
- Valid credentials → JWT token
- Invalid credentials → 401 error
- Response time < 1s
```

#### 3. /generate-bdd
**What it does**: Generate BDD/Gherkin scenarios from EARS
**Output**: Gherkin feature files
**Verbosity**: Can be very verbose with multiple scenarios
**Documentation level impact**: HIGH - Could greatly benefit

**Example verbose output**:
```gherkin
Feature: User Authentication
  As a registered user
  I want to log in securely
  So that I can access protected resources

  Background:
    Given the authentication service is running
    And the database is seeded with test users
    And the JWT secret is configured

  Scenario: Successful login with valid credentials
    Given a registered user exists with email "user@example.com"
    And the user has a valid password "SecurePass123!"
    When the user submits a login request with:
      | email              | password        |
      | user@example.com   | SecurePass123!  |
    Then the response status should be 200
    And the response should contain a JWT token
    And the token should be valid for 24 hours
    And the token should contain user_id claim
    And the token should contain role claim

  Scenario: Login fails with invalid password
    Given a registered user exists with email "user@example.com"
    And the user has a valid password "SecurePass123!"
    When the user submits a login request with:
      | email              | password    |
      | user@example.com   | WrongPass!  |
    Then the response status should be 401
    And the response should contain error message "Invalid credentials"
    And no token should be generated

  Scenario: Login fails with non-existent user
    Given no user exists with email "nobody@example.com"
    When the user submits a login request with:
      | email                | password        |
      | nobody@example.com   | AnyPassword123  |
    Then the response status should be 401
    And the response should contain error message "Invalid credentials"

  # ... 10 more scenarios for edge cases ...
```

**Could be concise**:
```gherkin
Feature: User Authentication

  Scenario: Successful login
    Given registered user "user@example.com"
    When submit valid credentials
    Then return 200 with JWT token (24h expiry)

  Scenario: Invalid credentials
    Given registered user "user@example.com"
    When submit invalid password
    Then return 401 error
```

## Revised Assessment

### Does require-kit Need Documentation Levels?

**For /formalize-ears**: YES (MEDIUM priority)
- Can be verbose with rationale, examples, traceability
- Concise mode would help: Just EARS statement + acceptance criteria
- **BUT**: This is already covered by **TASK-019: Concise Mode**!

**For /generate-bdd**: YES (HIGH priority)
- Can generate 15+ scenarios with detailed steps
- Concise mode would help: Essential scenarios only (happy path + 1 error)
- **This is NOT covered by TASK-019**

**For /gather-requirements**: NO
- Interactive Q&A session, minimal output
- Not much to optimize

## The Real Task for require-kit

Instead of TASK-035 (which is for taskwright's execution workflow), require-kit needs:

### New Task: Documentation Levels for BDD Generation

**Scope**: Add `--docs` flag to /generate-bdd command

**Implementation**:
1. Update bdd-generator agent with documentation level awareness
2. Add --docs flag to generate-bdd command
3. Implement 3 levels:
   - **Minimal**: Happy path + 1 error scenario
   - **Standard** (default): Comprehensive scenarios (current behavior)
   - **Comprehensive**: Exhaustive scenarios + edge cases + data tables

**Effort**: 30-45 minutes (1 agent, 1 command)

**Files**:
- `installer/global/agents/bdd-generator.md` (~30 lines)
- `installer/global/commands/generate-bdd.md` (~10 lines)

## Relationship with TASK-019

**TASK-019** (Concise Mode for EARS) already addresses /formalize-ears verbosity:
- Adds --concise flag to formalize-ears
- 500-word limit
- Focus on behavior, not implementation
- This is EXACTLY what we need for EARS requirements

**Remaining gap**: BDD scenario generation verbosity

## Final Recommendation

### 1. TASK-035 is NOT for require-kit
- TASK-035 targets taskwright's /task-work execution workflow
- require-kit doesn't run task-work, it provides inputs to it
- **Action**: Remove TASK-035 from require-kit backlog

### 2. TASK-019 addresses EARS verbosity
- TASK-019 already adds concise mode to formalize-ears
- This covers the requirements documentation side
- **Action**: Prioritize TASK-019

### 3. Create NEW task for BDD verbosity (if needed)
- **New**: TASK-037: Add Documentation Levels to BDD Generation
- Add --docs flag to /generate-bdd
- Update bdd-generator agent
- 30-45 minute effort
- **Action**: Create as separate task if BDD verbosity is a problem

## Updated Implementation Order

1. ✅ REQ-002: Delete Agentecflow (COMPLETED)
2. ⭐ **TASK-019**: Concise Mode for EARS (2-3 hours) ← **Addresses EARS verbosity**
3. ⭐⭐⭐ **REQ-003**: Shared Installer (5 hours) ← **Critical**
4. ~~TASK-035: Documentation Levels~~ ← **REMOVE** (belongs in taskwright)
5. **TASK-022**: Spec Templates (6-8 hours)
6. **TASK-021**: Requirement Versioning (8-10 hours)
7. **[NEW] TASK-037**: BDD Documentation Levels (0.5-1 hour) ← **Optional: Only if BDD verbosity is a problem**

## Conclusion

**TASK-035 is IRRELEVANT to require-kit** because:
1. TASK-035 targets taskwright's /task-work workflow
2. require-kit doesn't own the execution workflow
3. require-kit's verbosity concerns are already addressed by TASK-019 (EARS) and potentially a new TASK-037 (BDD)

**Recommendation**:
- ❌ **Remove TASK-035** from require-kit backlog (it belongs in taskwright)
- ✅ **Focus on TASK-019** (concise mode for EARS - already planned)
- ✅ **Consider new task** for BDD verbosity if it's a real problem (quick 30-45 min task)

---

**Prepared by**: Claude Code
**Date**: 2025-11-01
**Context**: Corrected analysis after understanding taskwright/require-kit architecture
**Previous Analysis**: INCORRECT - Misunderstood which repository owns which workflow
