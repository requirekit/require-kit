# BDD and Gherkin Scenario Generation

## Converting EARS to BDD Scenarios

BDD (Behavior-Driven Development) scenarios describe system behavior in a way that's understandable by all stakeholders.

## Gherkin Syntax

### Basic Structure
```gherkin
Feature: [Feature name]
  As a [type of user]
  I want [goal]
  So that [benefit]

  Scenario: [Scenario description]
    Given [initial context]
    When [action or event]
    Then [expected outcome]
```

### Keywords
- **Feature**: Groups related scenarios
- **Scenario**: A specific test case
- **Given**: Preconditions or initial state
- **When**: The action or trigger
- **Then**: The expected result
- **And/But**: Additional steps

## EARS to Gherkin Mapping

### Event-Driven EARS → Scenario
**EARS**: When [trigger], the [system] shall [response]
**Gherkin**:
```gherkin
Scenario: [Describe the trigger event]
  Given [any necessary setup]
  When [trigger]
  Then [response should occur]
```

### State-Driven EARS → Scenario with Background
**EARS**: While [state], the [system] shall [behavior]
**Gherkin**:
```gherkin
Background:
  Given the system is in [state]

Scenario: [Behavior during state]
  When [action during state]
  Then [behavior should occur]
```

### Unwanted Behavior EARS → Error Scenario
**EARS**: If [error], then the [system] shall [recovery]
**Gherkin**:
```gherkin
Scenario: Handle [error condition]
  Given [setup that might cause error]
  When [error occurs]
  Then [recovery should happen]
```

## Complete Example: User Authentication

### EARS Requirements
1. When a user submits valid credentials, the system shall authenticate and create a session
2. If invalid credentials are submitted, then the system shall display an error
3. While authenticated, the system shall allow access to protected resources

### Generated Gherkin Scenarios
```gherkin
Feature: User Authentication
  As a user
  I want to log into the system
  So that I can access my account

  Scenario: Successful login
    Given I am on the login page
    And a user exists with email "user@example.com" and password "SecurePass123"
    When I enter "user@example.com" in the email field
    And I enter "SecurePass123" in the password field
    And I click the login button
    Then I should be redirected to the dashboard
    And I should see "Welcome back!"

  Scenario: Failed login with invalid credentials
    Given I am on the login page
    When I enter "wrong@example.com" in the email field
    And I enter "WrongPassword" in the password field
    And I click the login button
    Then I should remain on the login page
    And I should see "Invalid email or password"

  Scenario: Access protected resource while authenticated
    Given I am logged in as "user@example.com"
    When I navigate to "/dashboard"
    Then I should see the dashboard content
    And I should not be redirected to login
```

## Best Practices

### Writing Good Scenarios
1. **One behavior per scenario**: Test a single aspect
2. **Independent scenarios**: Each should run in isolation
3. **Clear language**: Avoid technical jargon
4. **Concrete examples**: Use specific data
5. **Business focus**: Describe what, not how

### Common Anti-Patterns to Avoid
- UI-specific steps ("click the third button")
- Technical implementation details
- Overly complex scenarios with many steps
- Vague assertions ("everything works correctly")

## Scenario Outline for Data-Driven Tests

```gherkin
Scenario Outline: Login with various credentials
  Given I am on the login page
  When I enter "<email>" in the email field
  And I enter "<password>" in the password field
  And I click the login button
  Then I should see "<message>"

  Examples:
    | email              | password    | message                |
    | valid@example.com  | ValidPass   | Welcome back!          |
    | invalid@test.com   | WrongPass   | Invalid credentials    |
    | blocked@test.com   | AnyPass     | Account is blocked     |
```

## Tags for Organization

```gherkin
@authentication @critical
Feature: User Authentication

  @smoke @happy-path
  Scenario: Successful login
    ...

  @error-handling
  Scenario: Failed login
    ...
```

Use tags to:
- Run specific subsets of tests
- Mark priority levels
- Categorize by feature area
- Identify test types (smoke, regression, etc.)
