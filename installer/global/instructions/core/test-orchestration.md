# Test Orchestration and Quality Gates

## Test Strategy

### Test Pyramid
```
        /\
       /E2E\      <- End-to-end tests (Few)
      /------\
     /  Integ  \   <- Integration tests (Some)
    /----------\
   /    Unit    \  <- Unit tests (Many)
  /--------------\
```

## Test Types and When to Use Them

### Unit Tests
**Purpose**: Test individual functions/methods in isolation
**When to run**: On every code change
**Tools**: Jest, pytest, JUnit
**Example**:
```python
def test_calculate_tax():
    assert calculate_tax(100, 0.1) == 10
```

### Integration Tests
**Purpose**: Test component interactions
**When to run**: Before commits
**Tools**: Testing library, pytest with fixtures
**Example**:
```python
def test_api_database_integration():
    response = api_client.create_user({"name": "Test"})
    user = database.get_user(response["id"])
    assert user.name == "Test"
```

### End-to-End Tests
**Purpose**: Test complete user workflows
**When to run**: Before deployments
**Tools**: Playwright, Cypress, Selenium
**Example**:
```typescript
test('user can complete purchase', async ({ page }) => {
  await page.goto('/shop');
  await page.click('[data-testid="add-to-cart"]');
  await page.click('[data-testid="checkout"]');
  await expect(page).toHaveURL('/confirmation');
});
```

## Quality Gates

### What are Quality Gates?
Automated checkpoints that ensure code quality before progression.

### Standard Quality Gates

#### 1. Code Coverage Gate
**Threshold**: ≥80% coverage
**Enforcement**: Block merge if below threshold
```yaml
coverage:
  threshold:
    global: 80
    functions: 75
    lines: 80
    branches: 70
```

#### 2. Test Pass Rate Gate
**Threshold**: 100% tests passing
**Enforcement**: Block deployment on failure

#### 3. Complexity Gate
**Threshold**: Cyclomatic complexity ≤10
**Enforcement**: Warning at 10, error at 15

#### 4. Security Gate
**Checks**: No critical vulnerabilities
**Tools**: Snyk, OWASP dependency check

#### 5. Performance Gate
**Metrics**: Response time, memory usage
**Threshold**: P95 < 200ms

## Test Orchestration Patterns

### Intelligent Test Selection
Run only tests affected by changes:
```python
def select_tests(changed_files):
    tests = []
    for file in changed_files:
        if file.startswith('src/'):
            tests.extend(find_unit_tests(file))
        if 'api' in file:
            tests.extend(find_integration_tests(file))
        if file.endswith('.feature'):
            tests.extend(find_e2e_tests(file))
    return deduplicate(tests)
```

### Parallel Execution
```javascript
// Run test suites in parallel
const results = await Promise.all([
  runUnitTests(),
  runIntegrationTests(),
  runE2ETests()
]);
```

### Test Prioritization
1. **Smoke tests** - Critical path (run first)
2. **Changed code** - Tests for modified files
3. **Failed previously** - Recent failures
4. **Risk-based** - High-risk areas
5. **Everything else** - Comprehensive suite

## BDD Test Implementation

### From Gherkin to Code
```gherkin
Scenario: Successful login
  Given I am on the login page
  When I enter valid credentials
  Then I should see the dashboard
```

### Implementation:
```python
@given('I am on the login page')
def navigate_to_login(page):
    page.goto('/login')

@when('I enter valid credentials')
def enter_credentials(page):
    page.fill('#email', 'user@test.com')
    page.fill('#password', 'password123')
    page.click('#submit')

@then('I should see the dashboard')
def verify_dashboard(page):
    expect(page).to_have_url('/dashboard')
    expect(page.locator('h1')).to_contain_text('Dashboard')
```

## Continuous Testing Pipeline

### Pre-Commit Hooks
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run unit tests for changed files
npm test -- --findRelatedTests

# Check code coverage
npm test -- --coverage --coverageThreshold='{"global":{"lines":80}}'

# Run linting
npm run lint
```

### CI/CD Pipeline
```yaml
name: Test Pipeline
on: [push, pull_request]

jobs:
  test:
    steps:
      - name: Unit Tests
        run: npm test
        
      - name: Integration Tests
        run: npm run test:integration
        
      - name: Coverage Check
        run: npm run test:coverage
        
      - name: Quality Gates
        run: |
          npm run quality:check
          if [ $? -ne 0 ]; then
            echo "Quality gates failed"
            exit 1
          fi
```

## Test Reporting

### Metrics to Track
- **Test execution time**: Identify slow tests
- **Flaky test rate**: Tests that intermittently fail
- **Coverage trends**: Coverage over time
- **Failure patterns**: Common failure causes
- **MTTR**: Mean time to repair failures

### Report Format
```markdown
## Test Execution Report

**Date**: 2024-01-15
**Build**: #1234

### Summary
- Total Tests: 245
- Passed: 242 (98.8%)
- Failed: 3 (1.2%)
- Skipped: 0
- Duration: 2m 34s

### Coverage
- Statements: 85.3%
- Branches: 78.9%
- Functions: 89.2%
- Lines: 84.7%

### Quality Gates
| Gate | Status | Threshold | Actual |
|------|--------|-----------|--------|
| Coverage | ✅ Pass | 80% | 85.3% |
| Tests Pass | ❌ Fail | 100% | 98.8% |
| Complexity | ✅ Pass | ≤10 | 7.2 |

### Failed Tests
1. `test_user_login` - Timeout after 5s
2. `test_api_response` - Expected 200, got 500
3. `test_data_validation` - Assertion failed
```
