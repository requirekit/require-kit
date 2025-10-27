# Link BDD Scenarios to Task

Link Gherkin/BDD scenarios to a task for behavior-driven development.

## Usage
```bash
/task-link-bdd TASK-XXX BDD-YYY [BDD-ZZZ ...]
```

## Example
```bash
/task-link-bdd TASK-042 BDD-001 BDD-002 BDD-003
```

## Process

1. **Validate Task Exists**
   - Check task file in any state directory
   - Load current task metadata

2. **Validate BDD Scenarios Exist**
   - Check each scenario in `docs/bdd/features/`
   - Verify scenarios are valid Gherkin format

3. **Parse Scenario Details**
   ```gherkin
   Feature: User Authentication
     As a user
     I want to log in to the system
     So that I can access protected resources
     
     Scenario: Successful login
       Given a registered user exists
       When they submit valid credentials
       Then they should be logged in
       And a session should be created
   ```

4. **Update Task File**
   ```yaml
   bdd_scenarios: [BDD-001, BDD-002, BDD-003]
   scenario_coverage:
     BDD-001:
       title: "Successful login"
       feature: "User Authentication"
       status: "pending"
       tests: []
     BDD-002:
       title: "Failed login attempt"
       feature: "User Authentication"
       status: "pending"
       tests: []
     BDD-003:
       title: "Session timeout"
       feature: "Session Management"
       status: "pending"
       tests: []
   ```

5. **Create Scenario Checklist**
   Add to task file:
   ```markdown
   ## BDD Scenario Coverage
   - [ ] BDD-001: Successful login
     - Given: User exists in database
     - When: Valid credentials submitted
     - Then: User logged in, session created
   - [ ] BDD-002: Failed login attempt
     - Given: User exists
     - When: Invalid credentials submitted
     - Then: Error message, no session
   - [ ] BDD-003: Session timeout
     - Given: User logged in
     - When: Session expires
     - Then: User redirected to login
   ```

6. **Generate Test Stubs**
   Create test implementations for scenarios:
   ```python
   # tests/features/test_authentication.py
   
   @pytest.mark.bdd("BDD-001")
   def test_successful_login():
       """Scenario: Successful login"""
       # Given a registered user exists
       user = create_test_user()
       
       # When they submit valid credentials
       response = login(user.email, user.password)
       
       # Then they should be logged in
       assert response.status_code == 200
       assert response.json()["authenticated"] == True
       
       # And a session should be created
       assert "session_id" in response.cookies
   ```

## Output Format
```
✅ BDD Scenarios linked to TASK-042

🎬 Linked Scenarios (3):
├─ BDD-001: Successful login
│  Feature: User Authentication
│  Steps: 4
│  Complexity: Simple
│
├─ BDD-002: Failed login attempt
│  Feature: User Authentication
│  Steps: 3
│  Complexity: Simple
│
└─ BDD-003: Session timeout
   Feature: Session Management
   Steps: 3
   Complexity: Medium

📊 Test Generation:
- Scenarios to implement: 3
- Total test steps: 10
- Estimated test cases: 6-8
- Estimated effort: 1 day

🔗 BDD Mapping established:
Features → Scenarios → Task → Tests

📝 Next steps:
- Review scenarios in docs/bdd/features/
- Use `/task-implement TASK-042` to generate BDD tests
- Run tests with `/task-test TASK-042`
```

## BDD Test Generation

### Cucumber-Style Tests (JavaScript)
```javascript
// tests/features/authentication.feature
Feature: User Authentication
  
  @BDD-001
  Scenario: Successful login
    Given a registered user "test@example.com"
    When they login with valid credentials
    Then they should see the dashboard
    And their session should be active

// tests/steps/authentication.steps.js
Given('a registered user {string}', async (email) => {
  await createUser(email);
});

When('they login with valid credentials', async () => {
  await page.fill('#email', 'test@example.com');
  await page.fill('#password', 'validpassword');
  await page.click('#login-button');
});

Then('they should see the dashboard', async () => {
  await expect(page).toHaveURL('/dashboard');
});
```

### Behave-Style Tests (Python)
```python
# tests/features/authentication.feature
Feature: User Authentication
  
  @BDD-001
  Scenario: Successful login
    Given a registered user exists
    When they submit valid credentials
    Then they should be logged in
    And a session should be created

# tests/steps/authentication_steps.py
from behave import given, when, then

@given('a registered user exists')
def step_create_user(context):
    context.user = create_test_user()

@when('they submit valid credentials')
def step_submit_credentials(context):
    context.response = login(
        context.user.email,
        context.user.password
    )

@then('they should be logged in')
def step_verify_login(context):
    assert context.response.status_code == 200
```

### SpecFlow-Style Tests (.NET)
```csharp
// Tests/Features/Authentication.feature
Feature: User Authentication

@BDD-001
Scenario: Successful login
    Given a registered user exists
    When they submit valid credentials
    Then they should be logged in
    And a session should be created

// Tests/Steps/AuthenticationSteps.cs
[Binding]
public class AuthenticationSteps
{
    [Given(@"a registered user exists")]
    public void GivenARegisteredUserExists()
    {
        _user = CreateTestUser();
    }
    
    [When(@"they submit valid credentials")]
    public void WhenTheySubmitValidCredentials()
    {
        _response = Login(_user.Email, _user.Password);
    }
    
    [Then(@"they should be logged in")]
    public void ThenTheyShouldBeLoggedIn()
    {
        Assert.Equal(200, _response.StatusCode);
    }
}
```

## Scenario Analysis

### Complexity Assessment
```python
def assess_scenario_complexity(scenario):
    step_count = len(scenario.steps)
    has_tables = any(step.has_table for step in scenario.steps)
    has_examples = scenario.has_examples
    has_background = scenario.feature.has_background
    
    complexity_score = step_count
    if has_tables: complexity_score += 3
    if has_examples: complexity_score += 2
    if has_background: complexity_score += 1
    
    if complexity_score <= 5:
        return "Simple"
    elif complexity_score <= 10:
        return "Medium"
    else:
        return "Complex"
```

### Coverage Mapping
```python
def map_scenario_to_tests(scenario_id):
    """Map BDD scenario to test functions"""
    test_mapping = {
        'BDD-001': [
            'test_successful_login',
            'test_session_creation',
            'test_redirect_after_login'
        ],
        'BDD-002': [
            'test_invalid_password',
            'test_invalid_username',
            'test_error_message_display'
        ],
        'BDD-003': [
            'test_session_timeout',
            'test_redirect_to_login',
            'test_session_cleanup'
        ]
    }
    return test_mapping.get(scenario_id, [])
```

## Auto-Discovery

### Find Related Scenarios
```bash
/task-discover-bdd TASK-XXX
```
Automatically finds scenarios based on:
- Task title keywords
- Linked requirements
- Feature file names
- Scenario descriptions

### Bulk Linking
```bash
/task-link-bdd TASK-XXX --all-in-feature "User Authentication"
```
Links all scenarios from a specific feature file.

## Scenario Verification

### Check Implementation
```bash
/task-check-bdd TASK-XXX
```
Verifies that:
- All linked scenarios have test implementations
- All test steps are defined
- No undefined steps exist
- All scenarios pass when executed

### Generate Coverage Report
```markdown
# BDD Coverage Report - TASK-XXX

## Summary
- Scenarios Linked: 3
- Scenarios Implemented: 2 (67%)
- Steps Defined: 8/10 (80%)
- Scenarios Passing: 1/2 (50%)

## Scenario Status

### ✅ BDD-001: Successful login
- Status: PASSING
- All steps implemented
- Test duration: 2.3s

### ⚠️ BDD-002: Failed login attempt
- Status: FAILING
- Step undefined: "error message should be displayed"
- Last failure: Line 45

### ❌ BDD-003: Session timeout
- Status: NOT IMPLEMENTED
- No test file found
- Action needed: Implement scenario

## Recommendations
1. Define missing step for BDD-002
2. Implement BDD-003 scenario
3. Run full BDD suite to verify
```

## Integration with Execution

### Run BDD Tests Only
```bash
/task-test TASK-XXX --bdd-only
```
Executes only the BDD scenarios linked to the task.

### BDD Test Report
```
BDD Test Results - TASK-XXX
============================

Feature: User Authentication
✅ Scenario: Successful login (BDD-001) - 2.3s
   ✅ Given a registered user exists
   ✅ When they submit valid credentials
   ✅ Then they should be logged in
   ✅ And a session should be created

❌ Scenario: Failed login attempt (BDD-002) - 1.1s
   ✅ Given a registered user exists
   ✅ When they submit invalid credentials
   ❌ Then an error message should be displayed
      Error: Step not defined

⏭️ Scenario: Session timeout (BDD-003) - SKIPPED
   Reason: Not implemented

Summary: 1 passed, 1 failed, 1 skipped
```

## Living Documentation

### Generate Documentation
```bash
/task-generate-bdd-docs TASK-XXX
```
Creates living documentation from scenarios:

```markdown
# User Authentication Feature

## Overview
This feature allows users to authenticate with the system.

## Scenarios

### ✅ Successful Login
**Purpose**: Verify users can log in with valid credentials
**Status**: Implemented and passing

**Steps**:
1. Given a registered user exists
2. When they submit valid credentials
3. Then they should be logged in
4. And a session should be created

**Test Coverage**: 100%
**Last Verified**: 2024-01-15

### ❌ Failed Login Attempt
**Purpose**: Verify system handles invalid credentials
**Status**: Partially implemented

**Steps**:
1. Given a registered user exists
2. When they submit invalid credentials
3. Then an error message should be displayed

**Test Coverage**: 67%
**Issues**: Step 3 not defined
```

## Best Practices

1. **Link scenarios before implementation** - Design behavior first
2. **Keep scenarios atomic** - One behavior per scenario
3. **Use consistent language** - Gherkin keywords consistently
4. **Map to requirements** - Each scenario should trace to requirements
5. **Run regularly** - Execute BDD tests on every change
6. **Update scenarios** - When behavior changes, update scenarios
7. **Generate documentation** - Keep living docs current
