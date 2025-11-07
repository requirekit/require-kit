# BDD/Gherkin Scenarios

Learn how RequireKit automatically generates testable Given-When-Then scenarios from EARS requirements.

## What is BDD?

**Behavior-Driven Development (BDD)** uses natural language scenarios to describe system behavior. RequireKit generates these scenarios automatically from your EARS requirements.

## Gherkin Syntax

Gherkin uses a simple structure:

```gherkin
Feature: [Feature name]

  Scenario: [Scenario name]
    Given [precondition]
    When [action]
    Then [expected outcome]
```

## Generation from EARS

RequireKit's `/generate-bdd` command converts EARS requirements into Gherkin scenarios:

**EARS Requirement:**
```
REQ-001 (Event-Driven):
When a user submits valid credentials, the system shall authenticate
and redirect to dashboard within 1 second.
```

**Generated BDD Scenario:**
```gherkin
Feature: User Authentication

  Scenario: Successful login with valid credentials
    Given a registered user exists with email "user@example.com"
    And the user is on the login page
    When the user submits valid credentials
    Then the system should authenticate the user
    And redirect to the dashboard within 1 second
```

## Scenario Structure

### Given (Preconditions)
Sets up the initial state:
- User data
- System configuration
- Previous actions

### When (Actions)
The action being tested:
- User interactions
- System events
- External triggers

### Then (Outcomes)
Expected results:
- System responses
- State changes
- Side effects

### And/But (Additional Steps)
Chain multiple conditions or outcomes:
- Multiple preconditions
- Sequential actions
- Multiple expected outcomes

## Benefits

### Shared Understanding
Non-technical stakeholders can read and validate scenarios.

### Automated Testing
Scenarios can drive test automation (Cucumber, SpecFlow, Behave).

### Living Documentation
Scenarios serve as executable specifications that stay current.

### Acceptance Criteria
Clear definition of "done" for each requirement.

## Example: Complete Feature

```gherkin
Feature: User Authentication

  Background:
    Given the authentication service is running
    And the user database is available

  Scenario: Successful login
    Given a user with email "test@example.com" and password "SecurePass123"
    When the user submits valid credentials
    Then the system should authenticate the user
    And redirect to the dashboard within 1 second
    And create a session with 30-minute timeout

  Scenario: Failed login - invalid password
    Given a user with email "test@example.com"
    When the user submits an incorrect password
    Then the system should display "Invalid email or password"
    And not create a session
    And log the failed attempt

  Scenario: Failed login - non-existent user
    Given no user exists with email "nonexistent@example.com"
    When the user attempts to login
    Then the system should display "Invalid email or password"
    And not reveal whether email exists

  Scenario: HTTPS enforcement
    Given a user attempts login over HTTP
    Then the system should reject the request
    And require HTTPS protocol
```

## Best Practices

✅ **One scenario per behavior**
✅ **Use concrete examples**
✅ **Keep scenarios independent**
✅ **Write from user perspective**
✅ **Include edge cases**

❌ **Don't test implementation details**
❌ **Don't make scenarios dependent**
❌ **Don't use technical jargon**

## Commands

```bash
# Generate BDD scenarios
/generate-bdd

# Generate for specific feature
/generate-bdd FEAT-001

# Regenerate scenarios after requirement changes
/generate-bdd --refresh
```

## Next Steps

- 🏗️ [Learn about Epic/Feature Hierarchy](hierarchy.md)
- 📝 [Try the Quickstart Guide](../getting-started/quickstart.md)
- 💡 [See BDD Examples](../examples/bdd.md)

---

For more details, see the [Complete User Guide](../guides/require_kit_user_guide.md).
