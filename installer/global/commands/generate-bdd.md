# Generate BDD Command

Generate BDD/Gherkin scenarios from EARS requirements.

## Usage
Type `/generate-bdd` to create test scenarios from EARS requirements.

## Input
I'll process EARS requirements from:
- `docs/requirements/*.md`
- Recently formalized EARS statements
- Specific requirements you identify

## Conversion Process

### EARS → Gherkin Mapping

#### Event-Driven → Scenario
```
EARS: When [trigger], the [system] shall [response]
↓
Scenario: [Description of trigger]
  Given [preconditions]
  When [trigger occurs]
  Then [response happens]
```

#### State-Driven → Background + Scenario
```
EARS: While [state], the [system] shall [behavior]
↓
Background:
  Given the system is in [state]
Scenario: [Behavior in state]
  When [action]
  Then [behavior occurs]
```

## Example Generation

### Input EARS
```
REQ-001: When a user submits valid login credentials, 
the system shall authenticate and create a session within 1 second.
```

### Generated Gherkin
```gherkin
Feature: User Authentication
  As a user
  I want to log into the system
  So that I can access my account

  @authentication @happy-path
  Scenario: Successful login with valid credentials
    Given a registered user exists with email "user@example.com"
    And the user has password "SecurePass123"
    When the user enters "user@example.com" in the email field
    And the user enters "SecurePass123" in the password field
    And the user clicks the login button
    Then the user should be authenticated successfully
    And a session should be created
    And the response time should be less than 1 second
    And the user should be redirected to the dashboard
```

## Output Structure

### Feature Files
Generated scenarios will be saved to:
```
docs/bdd/features/
├── authentication.feature
├── user-management.feature
├── api-endpoints.feature
└── error-handling.feature
```

### Test Mapping
Each scenario will include:
- Link to source EARS requirement
- Tags for test categorization
- Implementation hints
- Test data examples

## Scenario Types Generated

### Happy Path Scenarios
- Normal successful operations
- Expected user workflows

### Edge Cases
- Boundary conditions
- Unusual inputs
- Concurrency scenarios

### Error Scenarios
- Invalid inputs
- System failures
- Recovery processes

### Performance Scenarios
- Load conditions
- Response time requirements
- Resource constraints

## Quality Criteria
Generated scenarios will:
- ✓ Be independent and runnable in isolation
- ✓ Use concrete examples with test data
- ✓ Focus on behavior, not implementation
- ✓ Be readable by non-technical stakeholders
- ✓ Include all necessary preconditions

## Test Implementation Hints
Each scenario includes implementation guidance:
```python
# Generated test implementation template
@given('a registered user exists with email "{email}"')
def create_test_user(context, email):
    context.user = User.create(email=email, password="hashed")

@when('the user enters "{value}" in the {field} field')
def enter_field_value(context, value, field):
    context.page.fill(f"#{field}", value)

@then('the user should be authenticated successfully')
def verify_authentication(context):
    assert context.response.status_code == 200
    assert "session_token" in context.response.cookies
```

## Next Steps
After generating BDD scenarios:
1. Review scenarios with stakeholders
2. Implement step definitions
3. Use test automation tools or integrate with [guardkit](https://github.com/guardkit/guardkit) for execution workflows
