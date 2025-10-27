# Test Task

Execute tests for a task and verify quality gates before allowing completion.

## Usage
```bash
/task-test TASK-XXX [verbose:true|false] [coverage-only:true|false]
```

## Example
```bash
/task-test TASK-042 verbose:true
```

## Process

1. **Detect Technology Stack**
   Identify project type by checking for:
   - `pytest.ini` or `pyproject.toml` → Python
   - `package.json` with test script → JavaScript/TypeScript  
   - `*.csproj` files → .NET
   - `playwright.config.ts` → Playwright E2E

2. **Execute Test Suite**
   
   ### Python (pytest)
   ```bash
   pytest tests/ -v --cov=src --cov-report=term --cov-report=json
   ```
   
   ### JavaScript/TypeScript (npm)
   ```bash
   npm test -- --coverage --json --outputFile=test-results.json
   ```
   
   ### .NET
   ```bash
   dotnet test --collect:"XPlat Code Coverage" --logger:"json"
   ```
   
   ### Playwright E2E
   ```bash
   npx playwright test --reporter=json
   ```

3. **Parse Test Results**
   Extract from test output:
   - Total tests run
   - Tests passed
   - Tests failed
   - Tests skipped
   - Execution time
   - Error details for failures

4. **Parse Coverage Metrics**
   Extract coverage data:
   - Line coverage %
   - Branch coverage %
   - Function coverage %
   - Statement coverage %
   - Uncovered files list

5. **Evaluate Quality Gates**
   ```yaml
   gates:
     tests:
       all_passing: required
       no_skipped: warning
     coverage:
       lines: ≥ 80%
       branches: ≥ 75%
       functions: ≥ 80%
     performance:
       total_time: < 30s
       slowest_test: < 5s
   ```

6. **Update Task Metadata**
   ```yaml
   test_results:
     status: passed|failed|partial
     last_run: <timestamp>
     coverage: 87.5
     passed: 23
     failed: 0
     skipped: 2
     execution_log: |
       [Full test output captured here]
   ```

7. **Determine Next State**
   - All gates pass → Can move to IN_REVIEW
   - Any required gate fails → Move to BLOCKED
   - Warnings only → Can proceed with caution

## Output Format

### Success Case
```
✅ TESTS PASSED for TASK-XXX

📊 Test Results:
├─ Total: 25 tests
├─ Passed: 25 ✅
├─ Failed: 0
├─ Skipped: 0
└─ Duration: 12.3s

📈 Coverage Report:
├─ Lines: 87.5% ✅ (threshold: 80%)
├─ Branches: 82.1% ✅ (threshold: 75%)
├─ Functions: 91.3% ✅ (threshold: 80%)
└─ Statements: 88.7% ✅

🎯 Quality Gates: ALL PASSING

✅ Task ready for review!
Next step: Use `/task-review TASK-XXX` to move to review
```

### Failure Case
```
❌ TESTS FAILED for TASK-XXX

📊 Test Results:
├─ Total: 25 tests
├─ Passed: 23 ⚠️
├─ Failed: 2 ❌
├─ Skipped: 0
└─ Duration: 15.7s

Failed Tests:
1. test_auth_service.py::test_login_invalid_credentials
   AssertionError: Expected 401, got 500
   Line 45: assert response.status_code == 401

2. test_auth_service.py::test_session_timeout
   TimeoutError: Test exceeded 5s limit
   Line 78: await session.wait_for_timeout()

📈 Coverage Report:
├─ Lines: 75.2% ❌ (threshold: 80%)
├─ Branches: 71.0% ❌ (threshold: 75%)
└─ Functions: 78.5% ⚠️ (threshold: 80%)

🚫 Quality Gates: 2 CRITICAL FAILURES

Task moved to BLOCKED
Fix required issues and run `/task-test TASK-XXX` again
```

## Detailed Test Report
When verbose mode is enabled, also generate:
```markdown
## Detailed Test Execution Log

### Test Run Information
- Command: pytest tests/ -v --cov=src
- Started: 2024-01-15 14:30:00
- Completed: 2024-01-15 14:30:12
- Environment: Python 3.11.0, pytest 7.4.0

### Test Results by Module
#### tests/test_auth_service.py (10 tests)
✅ test_login_valid_credentials - 0.12s
✅ test_login_invalid_credentials - 0.08s
✅ test_password_hashing - 0.03s
...

#### tests/test_user_model.py (8 tests)
✅ test_user_creation - 0.02s
✅ test_user_validation - 0.01s
...

### Coverage Details
#### Covered Files
- src/auth/service.py: 92.3%
  - Missing: lines 45-47 (error handling)
- src/auth/models.py: 88.1%
  - Missing: lines 23, 78-80

#### Uncovered Files
- src/auth/validators.py: 0% (no tests)
```

## Test Failure Diagnosis
For failed tests, provide:
1. **Error Type**: Assertion, Timeout, Import, etc.
2. **Location**: File, function, line number
3. **Expected vs Actual**: What was expected and what occurred
4. **Stack Trace**: Last 10 lines of trace
5. **Suggested Fix**: Common solutions for this error type

## Performance Analysis
When tests pass but are slow:
```
⚠️ Performance Warning

Slow Tests Detected:
1. test_database_migration - 8.2s (threshold: 5s)
2. test_large_file_upload - 6.7s (threshold: 5s)

Consider:
- Mocking external dependencies
- Using test fixtures
- Parallelizing test execution
```

## Integration Points

### MCP Code Checker (Python)
```bash
mcp-code-checker:run_pytest_check --verbosity 2
```

### Playwright Integration
```bash
playwright:browser_snapshot
playwright:browser_take_screenshot --filename test-result.png
```

### CI/CD Webhook
Can post results to CI/CD system:
```json
{
  "task_id": "TASK-XXX",
  "test_status": "passed",
  "coverage": 87.5,
  "timestamp": "2024-01-15T14:30:00Z"
}
```

## Error Handling
- No tests found: "Error: No tests found for TASK-XXX"
- Test command failed: "Error: Test execution failed - check configuration"
- Coverage below minimum: "Error: Coverage 65% is below minimum 80%"
- Timeout exceeded: "Error: Tests exceeded 30s timeout"

## Configuration
Quality gates can be customized in `.claude/test-config.yaml`:
```yaml
quality_gates:
  coverage:
    lines: 85
    branches: 80
    functions: 85
  performance:
    max_duration: 20
    max_single_test: 3
  required_test_types:
    - unit
    - integration
```
