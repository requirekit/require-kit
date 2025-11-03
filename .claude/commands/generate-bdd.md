# Generate BDD Command

Transform EARS requirements into executable BDD/Gherkin scenarios for test automation.

## Command
```
/generate-bdd [requirement-id]
```

## What This Does

Converts formal EARS requirements into Gherkin scenarios that:
- Serve as living documentation
- Drive test automation
- Validate implementation
- Bridge requirements and code

## Input: EARS Requirements

```
## REQ-001: User Login [Event-Driven]
When a user submits valid credentials, the system shall authenticate the user within 1 second.
```

## Output: Gherkin Scenarios

```gherkin
# Requirement: REQ-001
@requirement-REQ-001 @authentication @critical
Feature: User Authentication
  As a registered user
  I want to log into the system
  So that I can access protected resources

  Background:
    Given the authentication service is available
    And the following users exist:
      | email              | password | status |
      | user@example.com   | Pass123! | active |
      | locked@example.com | Pass456! | locked |

  @happy-path @smoke
  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter "user@example.com" as email
    And I enter "Pass123!" as password
    And I click the login button
    Then I should be authenticated successfully
    And I should be redirected to the dashboard
    And the authentication should complete within 1 second

  @edge-case
  Scenario: Login with remember me option
    Given I am on the login page
    When I enter valid credentials
    And I check "Remember me"
    And I click the login button
    Then a persistent session should be created
    And the session should expire in 30 days

  @error-handling
  Scenario: Login with invalid credentials
    Given I am on the login page
    When I enter "user@example.com" as email
    And I enter "WrongPass!" as password
    And I click the login button
    Then I should see an error message "Invalid credentials"
    And I should remain on the login page

  @security
  Scenario: Account lockout after failed attempts
    Given a user has 2 failed login attempts
    When they fail to login a third time
    Then their account should be locked
    And they should see "Account locked for 15 minutes"
    And an admin should be notified
```

## Transformation Patterns

### Event-Driven → Given-When-Then
```
EARS: When [event], the system shall [response]
BDD:  Given [setup]
      When [event]
      Then [response]
```

### State-Driven → Scenario with State
```
EARS: While [state], the system shall [behavior]
BDD:  Given the system is in [state]
      When [action]
      Then [behavior is maintained]
```

### Unwanted Behavior → Error Scenario
```
EARS: If [error], then the system shall [recovery]
BDD:  Given [setup that could fail]
      When [error occurs]
      Then [recovery happens]
```

## Scenario Coverage

For each EARS requirement, generates:
1. **Happy Path** - Primary success scenario
2. **Edge Cases** - Boundary conditions
3. **Error Cases** - Failure handling
4. **Performance** - Timing requirements
5. **Security** - Access control

## Tags Generated

```gherkin
@requirement-REQ-XXX  # Links to EARS requirement
@epic-EPIC-XXX       # Links to epic
@feature-FEAT-XXX    # Links to feature
@priority-high       # Priority level
@smoke               # Smoke test candidate
@regression          # Regression suite
@api                 # API testing
@ui                  # UI testing
```

## Test Data Specification

```gherkin
Examples:
  | email               | password  | result  | message              |
  | valid@test.com      | Valid123! | success | Welcome              |
  | invalid@test.com    | Wrong!    | failure | Invalid credentials  |
  | locked@test.com     | Valid123! | failure | Account locked       |
  | expired@test.com    | Valid123! | failure | Password expired     |
```

## Quality Criteria

Each scenario validated for:
- ✅ Single behavior focus
- ✅ Independent execution
- ✅ Concrete examples
- ✅ Business language
- ✅ Clear assertions
- ✅ Proper tags
- ✅ Test data defined

## Advanced Features

### Scenario Outlines
```gherkin
Scenario Outline: Password validation
  When I enter "<password>"
  Then validation should be "<r>"
  
  Examples:
    | password   | result  |
    | short      | invalid |
    | NoNumber!  | invalid |
    | Valid123!  | valid   |
```

### Background Setup
```gherkin
Background:
  Given test database is initialized
  And cache is cleared
  And the following configuration:
    | setting          | value |
    | max_attempts     | 3     |
    | lockout_duration | 15    |
```

## Output Structure

```
docs/bdd/features/
├── authentication.feature
├── user-management.feature
├── data-processing.feature
└── api/
    ├── endpoints.feature
    └── integration.feature
```

## Integration Hints

Each scenario includes:
```gherkin
# Implementation: tests/e2e/auth.spec.ts::testLogin
# Test data: factories/user.factory.ts
# Cleanup: delete test sessions after each scenario
```

## Usage Examples

```bash
# Generate for all requirements
/generate-bdd

# Generate for specific requirement
/generate-bdd REQ-001

# Generate for an epic
/generate-bdd --epic EPIC-001

# Generate with specific tags
/generate-bdd --tags critical,smoke
```

## Next Steps

After generating BDD scenarios:
1. Review scenarios with stakeholders
2. Implement step definitions
3. Create test data fixtures
4. Use test automation tools or integrate with [taskwright](https://github.com/taskwright-dev/taskwright) for execution workflows

## Best Practices

1. **Keep scenarios focused** - One behavior per scenario
2. **Use domain language** - Avoid technical terms
3. **Provide examples** - Concrete over abstract
4. **Tag appropriately** - For test organization
5. **Maintain independence** - No scenario dependencies

Ready to generate comprehensive BDD scenarios from your EARS requirements!
