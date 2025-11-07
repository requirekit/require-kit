# Your First Requirements

Step-by-step walkthrough of gathering and formalizing your first requirements using RequireKit.

## Overview

In this guide, you'll learn how to:
1. Gather requirements through interactive Q&A
2. Formalize them using EARS notation
3. Generate BDD scenarios for testing
4. Organize them into epics and features

**Time required**: 10-15 minutes

## Example: User Login Feature

Let's document requirements for a user login feature.

### Step 1: Start Requirements Gathering

```bash
/gather-requirements user-login
```

The requirements analyst agent will start an interactive Q&A session.

### Step 2: Answer the Questions

Be specific and think about:
- **Who** will use this feature?
- **What** should happen in normal scenarios?
- **What** should happen when things go wrong?
- **Performance** requirements (response times, scalability)
- **Security** requirements (authentication, authorization, encryption)

**Example conversation:**

```
Q: What problem are we solving?
A: Users need to securely log into our application with email and password.

Q: Who will be using this feature?
A: Regular users and administrators.

Q: What should happen on successful login?
A: Redirect to dashboard and create a session.

Q: What should happen on failed login?
A: Show an error message "Invalid email or password".

Q: Any performance requirements?
A: Login should complete in under 1 second.

Q: Security requirements?
A: - Passwords must be hashed using bcrypt
    - Only accept requests over HTTPS
    - Validate session tokens on each request
```

**Output**: `docs/requirements/draft/user-login.md`

### Step 3: Review Draft Requirements

Open the draft file and review the captured requirements. Make any needed edits.

```bash
cat docs/requirements/draft/user-login.md
```

### Step 4: Formalize with EARS Notation

Convert the draft requirements into structured EARS notation:

```bash
/formalize-ears
```

**The agent will**:
- Analyze the draft requirements
- Identify requirement types (ubiquitous, event-driven, state-driven, etc.)
- Generate formal EARS statements
- Create individual requirement files

**Output**: Multiple requirement files (`REQ-001.md`, `REQ-002.md`, etc.)

**Example EARS requirements:**

```
REQ-001 (Event-Driven):
When a user submits valid credentials, the system shall authenticate
and redirect to dashboard within 1 second.

REQ-002 (Unwanted Behavior):
If authentication fails, then the system shall display
"Invalid email or password" message.

REQ-003 (Ubiquitous):
The system shall hash all passwords using bcrypt.

REQ-004 (Ubiquitous):
The system shall accept authentication requests only over HTTPS.

REQ-005 (State-Driven):
While a user session is active, the system shall validate
the session token on each request.
```

### Step 5: Generate BDD Scenarios

Create testable Given-When-Then scenarios:

```bash
/generate-bdd
```

**Output**: `docs/bdd/BDD-001-user-authentication.feature`

**Example BDD scenarios:**

```gherkin
Feature: User Authentication

  Scenario: Successful login with valid credentials
    Given a registered user exists with email "user@example.com"
    And the user is on the login page
    When the user submits valid credentials
    Then the system should authenticate the user
    And redirect to the dashboard within 1 second

  Scenario: Failed login with invalid credentials
    Given a user is on the login page
    When the user submits invalid credentials
    Then the system should display "Invalid email or password"

  Scenario: Password security
    Given a new user registers
    Then the system should hash the password using bcrypt
    And store only the hashed password

  Scenario: HTTPS enforcement
    Given a user attempts to login over HTTP
    Then the system should reject the request
    And require HTTPS
```

### Step 6: Organize into Hierarchy

Create an epic and feature to organize these requirements:

```bash
# Create epic
/epic-create "User Management System"

# Create feature linked to epic
/feature-create "User Authentication" epic:EPIC-001 requirements:[REQ-001,REQ-002,REQ-003,REQ-004,REQ-005]

# View complete hierarchy
/hierarchy-view EPIC-001
```

**Output hierarchy:**

```
EPIC-001: User Management System
├── FEAT-001: User Authentication
    ├── REQ-001: User login with valid credentials
    ├── REQ-002: Failed authentication handling
    ├── REQ-003: Password hashing
    ├── REQ-004: HTTPS enforcement
    └── REQ-005: Session validation
```

## Understanding the Files

### Requirement Files (REQ-XXX.md)

Each requirement file contains:
- ID and title
- EARS pattern type
- Formal requirement statement
- Rationale
- Acceptance criteria
- Links to related BDD scenarios

### BDD Scenario Files (BDD-XXX.feature)

Gherkin feature files with:
- Feature description
- Multiple scenarios
- Given-When-Then steps
- Links back to requirements

### Epic Files (EPIC-XXX.md)

Epic specifications with:
- Strategic business objective
- Linked features
- Success criteria
- Metadata for PM tool export

### Feature Files (FEAT-XXX.md)

Feature specifications with:
- Feature description
- Linked requirements
- Linked BDD scenarios
- Acceptance criteria
- Metadata for PM tool export

## Best Practices

### During Requirements Gathering

✅ **Do:**
- Be specific about behavior
- Include error scenarios
- Specify performance requirements
- Consider security implications
- Think about edge cases

❌ **Don't:**
- Be vague ("should work well")
- Skip error handling
- Ignore non-functional requirements
- Assume implicit requirements

### After EARS Formalization

✅ **Review:**
- Each requirement is unambiguous
- Correct EARS pattern chosen
- Requirements are testable
- No implementation details leaked

### After BDD Generation

✅ **Verify:**
- Scenarios cover all requirements
- Given-When-Then format is clear
- Scenarios are executable
- Edge cases are included

## What's Next?

Now that you understand the workflow:

- 📖 [Learn more about EARS Notation](../core-concepts/ears-notation.md)
- 🎯 [Understand BDD Scenarios](../core-concepts/bdd-scenarios.md)
- 📚 [Explore the Command Reference](../commands/index.md)
- 💡 [See More Examples](../examples/index.md)

## Practice Exercises

Try gathering requirements for these features:

1. **Password Reset**: Users can reset forgotten passwords
2. **Shopping Cart**: Users can add/remove items from cart
3. **File Upload**: Users can upload files with validation

---

**Ready for more?** Check out the [Complete User Guide](../guides/require_kit_user_guide.md)
