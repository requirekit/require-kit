# BDD Generator - Extended Documentation

**Core Documentation**: See `installer/global/agents/bdd-generator.md` for essential patterns, boundaries, and transformation rules.

This extended documentation provides framework-specific implementation details, advanced techniques, and integration examples.

---

## Framework-Specific Step Definitions

### Python (pytest-bdd)

```python
from pytest_bdd import scenarios, given, when, then
import pytest

scenarios('authentication.feature')

@given('a user with email "user@example.com" and password "password123"')
def user_with_credentials(context):
    context.user = {
        "email": "user@example.com",
        "password": "password123"
    }

@when('the user submits the login form')
def submit_login(context):
    from auth_service import authenticate
    context.result = authenticate(
        context.user["email"],
        context.user["password"]
    )

@then('the system should authenticate the credentials')
def verify_authentication(context):
    assert context.result.authenticated is True
    assert context.result.user_id is not None

@then('the user should be redirected to the dashboard')
def verify_redirect(context):
    assert context.result.redirect_url == "/dashboard"
```

### .NET (SpecFlow)

```csharp
using TechTalk.SpecFlow;
using Xunit;
using AuthService;

[Binding]
public class AuthenticationSteps
{
    private readonly ScenarioContext _context;
    private AuthResult _result;

    public AuthenticationSteps(ScenarioContext context)
    {
        _context = context;
    }

    [Given(@"a user with email ""(.*)"" and password ""(.*)""")]
    public void GivenUserWithCredentials(string email, string password)
    {
        _context["user"] = new { Email = email, Password = password };
    }

    [When(@"the user submits the login form")]
    public void WhenUserSubmitsLogin()
    {
        var user = _context["user"];
        _result = AuthService.Authenticate(user.Email, user.Password);
    }

    [Then(@"the system should authenticate the credentials")]
    public void ThenSystemAuthenticates()
    {
        Assert.True(_result.Authenticated);
        Assert.NotNull(_result.UserId);
    }

    [Then(@"the user should be redirected to the dashboard")]
    public void ThenUserRedirected()
    {
        Assert.Equal("/dashboard", _result.RedirectUrl);
    }
}
```

### TypeScript (Cucumber.js)

```typescript
import { Given, When, Then } from '@cucumber/cucumber';
import { expect } from 'chai';
import { authenticate } from '../services/auth-service';

interface User {
  email: string;
  password: string;
}

Given('a user with email {string} and password {string}',
  function(email: string, password: string) {
    this.user = { email, password };
  }
);

When('the user submits the login form', async function() {
  this.result = await authenticate(this.user.email, this.user.password);
});

Then('the system should authenticate the credentials', function() {
  expect(this.result.authenticated).to.be.true;
  expect(this.result.userId).to.exist;
});

Then('the user should be redirected to the dashboard', function() {
  expect(this.result.redirectUrl).to.equal('/dashboard');
});
```

---

## LangGraph Integration Example

### Complexity Routing with BDD

**EARS Requirement**:
```
WHEN task complexity score exceeds 7, system SHALL invoke FULL_REQUIRED checkpoint
```

**Gherkin Scenario**:
```gherkin
@requirement-REQ-WORKFLOW-001
Feature: Complexity-based workflow routing
  As a workflow orchestrator
  I want to route tasks based on complexity score
  So that high-complexity tasks receive appropriate review

  Background:
    Given a LangGraph workflow with complexity routing node
    And the following checkpoint thresholds:
      | threshold | checkpoint     |
      | 7         | FULL_REQUIRED  |
      | 4         | LIGHT_OPTIONAL |
      | 0         | SKIP           |

  @happy-path @high-complexity
  Scenario: High complexity task triggers full review
    Given a task with complexity score 8
    When the workflow reaches the complexity routing node
    Then the system should invoke FULL_REQUIRED checkpoint
    And the task should be routed to architectural-reviewer
    And the task should be routed to code-reviewer

  @medium-complexity
  Scenario: Medium complexity task triggers optional review
    Given a task with complexity score 5
    When the workflow reaches the complexity routing node
    Then the system should invoke LIGHT_OPTIONAL checkpoint
    And the system should prompt user for review preference

  @low-complexity
  Scenario: Low complexity task skips review
    Given a task with complexity score 2
    When the workflow reaches the complexity routing node
    Then the system should skip checkpoint
    And the task should proceed directly to implementation
```

**Python Step Definitions (LangGraph)**:
```python
from pytest_bdd import scenarios, given, when, then
from langgraph.graph import StateGraph
from complexity_router import route_by_complexity

scenarios('complexity_routing.feature')

@given('a LangGraph workflow with complexity routing node')
def workflow_with_routing(context):
    graph = StateGraph()
    graph.add_node("complexity_router", route_by_complexity)
    context.workflow = graph.compile()

@given('a task with complexity score {score:d}', target_fixture='task_state')
def task_with_complexity(score):
    return {"complexity_score": score, "task_id": "TASK-042"}

@when('the workflow reaches the complexity routing node')
def execute_routing(context, task_state):
    context.result = context.workflow.invoke(task_state)

@then('the system should invoke {checkpoint} checkpoint')
def verify_checkpoint(context, checkpoint):
    assert context.result["checkpoint"] == checkpoint

@then('the task should be routed to {agent}')
def verify_agent_routing(context, agent):
    assert agent in context.result["routed_agents"]
```

---

## Common Scenario Patterns

### Authentication

```gherkin
@requirement-REQ-AUTH-001
Scenario: Successful login
  Given a registered user with valid credentials
  When they submit their login information
  Then they should be authenticated
  And a session should be created
  And they should be redirected to the dashboard

@requirement-REQ-AUTH-002 @error-handling
Scenario: Account lockout after failed attempts
  Given a user who has failed login 2 times
  When they fail login a third time
  Then their account should be locked
  And they should see a lockout message
  And an admin should be notified
```

### Data Validation

```gherkin
@requirement-REQ-VAL-001
Scenario Outline: Field validation rules
  Given a user filling out a form
  When they enter "<value>" in the "<field>"
  Then validation should "<result>"
  And show message "<message>"

  Examples:
    | field    | value          | result | message                |
    | email    | invalid        | fail   | Invalid email format   |
    | email    | test@test.com  | pass   |                        |
    | phone    | 123            | fail   | Phone too short        |
    | phone    | 1234567890     | pass   |                        |
```

### API Interactions

```gherkin
@requirement-REQ-API-001
Scenario: Successful API request
  Given an authenticated API client
  When they request resource "/users/123"
  Then the response status should be 200
  And the response should contain user data
  And the response time should be under 200ms

@requirement-REQ-API-002 @rate-limiting
Scenario: Rate limiting
  Given an API client at their rate limit
  When they make another request
  Then the response status should be 429
  And the response should include retry-after header
```

---

## Advanced Techniques

### Data Tables

```gherkin
Scenario: Bulk user creation
  Given an admin user
  When they create users with:
    | email             | role    | department |
    | alice@example.com | manager | sales      |
    | bob@example.com   | analyst | finance    |
  Then 2 users should be created
  And welcome emails should be sent
```

**Step Implementation**:
```python
@when('they create users with:')
def create_users(context):
    users = []
    for row in context.table:
        user = create_user(
            email=row['email'],
            role=row['role'],
            department=row['department']
        )
        users.append(user)
    context.created_users = users
```

### Background Context

```gherkin
Background:
  Given the following test data exists:
    | id | name    | status |
    | 1  | Widget  | active |
    | 2  | Gadget  | draft  |
  And a user with admin role
```

**Purpose**: Establishes common setup for all scenarios in a feature. Runs before each scenario.

**Best Practice**: Use Background for essential preconditions only. Don't overload with complex setup.

### Scenario Outlines

```gherkin
Scenario Outline: Permission checking
  Given a user with role "<role>"
  When they try to "<action>" a resource
  Then access should be "<result>"

  Examples:
    | role  | action | result  |
    | admin | delete | allowed |
    | user  | delete | denied  |
    | guest | read   | allowed |
```

**Step Implementation**:
```python
@given('a user with role {string}')
def user_with_role(context, role):
    context.user = User(role=role)

@when('they try to {string} a resource')
def attempt_action(context, action):
    context.result = context.user.attempt(action, resource=context.resource)

@then('access should be {string}')
def verify_access(context, expected_result):
    assert context.result == expected_result
```

---

## Integration with Test Automation

### Linking to Implementation

```gherkin
# Implementation: tests/e2e/authentication.spec.ts
# Method: test_successful_login
# Test ID: AUTH-TC-001
Scenario: User login
  Given a user with valid credentials
  When they submit the login form
  Then they should be authenticated
```

**Benefits**:
- Traceability from scenario to test code
- Easy navigation for developers
- Test ID for reporting and tracking

### Automation Hints

```gherkin
# Data setup: use factory :user, :registered
# Cleanup: delete created sessions
# Timeout: 5 seconds
# Tags: @smoke @regression
Scenario: Session management
  Given a user is logged in
  When their session expires
  Then they should be prompted to re-authenticate
```

**Purpose**: Provides execution context for automated test runners.

### CI/CD Integration

**Example GitHub Actions Workflow**:
```yaml
name: BDD Tests

on: [push, pull_request]

jobs:
  bdd-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install pytest pytest-bdd
      - name: Run BDD scenarios
        run: |
          pytest --gherkin-terminal-reporter
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v2
        with:
          name: bdd-results
          path: test-results/
```

### Test Reporting

**Cucumber JSON Output**:
```bash
pytest --cucumber-json=report.json
```

**HTML Report Generation**:
```bash
pytest --html=report.html --self-contained-html
```

**Integration with Test Management Tools**:
- Xray (Jira)
- TestRail
- qTest
- Zephyr

---

## Complete EARS to Gherkin Examples

### Event-Driven (Full Example)

**EARS Requirement**:
```
WHEN user submits login form, system SHALL authenticate credentials
```

**Gherkin Output**:
```gherkin
@requirement-REQ-AUTH-001
Scenario: User login with valid credentials
  Given a user with email "user@example.com" and password "password123"
  When the user submits the login form
  Then the system should authenticate the credentials
  And the user should be redirected to the dashboard
```

### State-Driven (Full Example)

**EARS Requirement**:
```
WHILE user is authenticated, system SHALL display personalized content
```

**Gherkin Output**:
```gherkin
Background:
  Given a user is authenticated as "alice@example.com"

@requirement-REQ-AUTH-002
Scenario: Display personalized dashboard
  When the user navigates to the dashboard
  Then the system should display personalized content
  And the content should include the user's name
```

### Unwanted Behavior (Full Example)

**EARS Requirement**:
```
IF login fails 3 times, system SHALL lock account for 30 minutes
```

**Gherkin Output**:
```gherkin
@requirement-REQ-AUTH-003 @error-handling
Scenario: Account lockout after failed login attempts
  Given a user with account "alice@example.com"
  And the user has failed login 2 times
  When the user fails login a third time
  Then the system should lock the account
  And the system should display "Account locked for 30 minutes"
  And the system should send a security alert email
```

### Optional Feature (Full Example)

**EARS Requirement**:
```
WHERE two-factor authentication is enabled, system SHALL require verification code
```

**Gherkin Output**:
```gherkin
@requirement-REQ-AUTH-004 @optional-feature
Scenario Outline: Two-factor authentication verification
  Given a user with email "<email>" and 2FA status "<2fa_enabled>"
  When the user submits valid credentials
  Then the system should <action>

  Examples:
    | email             | 2fa_enabled | action                           |
    | alice@example.com | true        | prompt for verification code     |
    | bob@example.com   | false       | authenticate and redirect        |
```

---

## Additional Scenario Patterns

### Error Recovery

```gherkin
@requirement-REQ-ERR-001
Scenario: Graceful degradation when service unavailable
  Given the payment service is unavailable
  When a user attempts to checkout
  Then the system should queue the payment request
  And the user should see a "Processing" message
  And the system should retry the payment when service recovers
```

### Performance Requirements

```gherkin
@requirement-REQ-PERF-001 @performance
Scenario: API response time
  Given 100 concurrent users
  When they request the user list endpoint
  Then all responses should complete within 500ms
  And the 95th percentile should be under 300ms
```

### Security Requirements

```gherkin
@requirement-REQ-SEC-001 @security
Scenario: SQL injection prevention
  Given a user input field for username
  When a user enters "admin' OR '1'='1"
  Then the system should sanitize the input
  And the system should not execute raw SQL
  And the login should fail
```

---

## Best Practices for Complex Scenarios

### Breaking Down Complex Workflows

**Anti-pattern**: One massive scenario with 15+ steps

**Better approach**: Multiple focused scenarios

```gherkin
# Instead of one huge checkout scenario
Scenario: Complete checkout flow  # TOO BIG
  Given user has items in cart
  And user is logged in
  And user enters shipping address
  And user selects shipping method
  And user enters payment info
  And user applies coupon code
  And user confirms order
  ...  # 15 more steps

# Break into focused scenarios
Scenario: Add shipping address
  Given a user with items in cart
  When they add a valid shipping address
  Then the address should be saved
  And they should proceed to shipping method

Scenario: Apply valid coupon
  Given a user at checkout
  When they apply coupon code "SAVE20"
  Then the discount should be applied
  And the total should be reduced by 20%

Scenario: Complete payment
  Given a user at payment step
  When they submit valid payment info
  Then the order should be confirmed
  And they should receive confirmation email
```

### Handling Asynchronous Behavior

```gherkin
@requirement-REQ-ASYNC-001
Scenario: Asynchronous job processing
  Given a user uploads a large file
  When the upload completes
  Then the system should queue a processing job
  And the user should see "Processing" status
  When I wait for job completion (max 30 seconds)
  Then the file should be processed
  And the user should see "Completed" status
```

**Step Implementation**:
```python
@when('I wait for job completion (max {timeout:d} seconds)')
def wait_for_completion(context, timeout):
    import time
    start = time.time()
    while time.time() - start < timeout:
        if context.job.status == "completed":
            return
        time.sleep(1)
    raise TimeoutError(f"Job did not complete within {timeout} seconds")
```

---

## Troubleshooting Common Issues

### Issue: Flaky Tests

**Symptom**: Scenarios pass sometimes, fail other times

**Solutions**:
1. Remove dependencies on execution order
2. Ensure proper test data isolation
3. Add explicit waits for async operations
4. Use unique identifiers for test data

### Issue: Unclear Failure Messages

**Anti-pattern**:
```gherkin
Then the system should work correctly
```

**Better**:
```gherkin
Then the user account should be created
And the user should receive a welcome email
And the user should be able to log in
```

### Issue: Technical Implementation Leakage

**Anti-pattern**:
```gherkin
When I POST to "/api/v1/users" with JSON payload
Then the database should have a new row in users table
```

**Better**:
```gherkin
When I create a new user account
Then the user should appear in the user list
```

---

**Return to Core Documentation**: `installer/global/agents/bdd-generator.md`
