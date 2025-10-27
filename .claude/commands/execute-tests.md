# Execute Tests Command

Run the test suite with quality gates and comprehensive reporting.

## Command
```
/execute-tests [options]
```

## Options

```bash
# Run all tests
/execute-tests

# Run specific level
/execute-tests --level unit
/execute-tests --level integration
/execute-tests --level e2e
/execute-tests --level bdd

# Run by tags
/execute-tests --tags smoke
/execute-tests --tags "critical,authentication"

# Run changed only
/execute-tests --changed

# Run with coverage
/execute-tests --coverage

# Run in watch mode
/execute-tests --watch
```

## Execution Strategy

### Test Order (Fail Fast)
1. **Lint & Format** (1s)
2. **Unit Tests** (30s)
3. **Integration Tests** (2m)
4. **BDD Scenarios** (5m)
5. **E2E Tests** (10m)

### Smart Selection
Based on changed files:
- `src/` changes → unit + integration
- `*.tsx` changes → component + e2e
- `requirements/` changes → bdd
- `config` changes → all tests

## Quality Gates

### Required Gates (Must Pass)
```yaml
coverage:
  lines: 80%
  branches: 75%
  functions: 80%

compliance:
  ears: 100%
  security: pass

performance:
  unit_tests: < 30s
  api_response: < 200ms
```

### Warning Gates (Should Pass)
```yaml
bdd_coverage: 95%
complexity: < 10
duplication: < 3%
```

## Test Output

### Progress Display
```
Running Test Suite...
========================
✅ Lint & Format      [1.2s]
✅ Unit Tests         [28.5s] 156/156 passed
⏳ Integration Tests  [45.3s] 23/25 passed
   ❌ API timeout test failed
   ❌ Database connection test failed
⏳ BDD Scenarios      [2m 15s] ...running
⏭️  E2E Tests         ...pending
```

### Coverage Report
```
---------------------------|---------|----------|---------|---------|
File                       | % Stmts | % Branch | % Funcs | % Lines |
---------------------------|---------|----------|---------|---------|
All files                  |   85.71 |    82.35 |   88.89 |   85.71 |
 src/auth/                 |   90.00 |    85.71 |  100.00 |   90.00 |
  login.service.ts         |   88.89 |    83.33 |  100.00 |   88.89 |
  session.service.ts       |   91.67 |    88.89 |  100.00 |   91.67 |
 src/user/                 |   81.82 |    78.57 |   80.00 |   81.82 |
  user.service.ts          |   81.82 |    78.57 |   80.00 |   81.82 |
---------------------------|---------|----------|---------|---------|

✅ Coverage gate PASSED: 85.71% > 80%
```

### BDD Report
```
Feature: User Authentication
  ✅ Successful login (245ms)
  ✅ Invalid credentials (123ms)
  ✅ Account lockout (356ms)
  ✅ Password reset (567ms)

Feature: Session Management
  ✅ Create session (189ms)
  ✅ Refresh token (201ms)
  ❌ Session timeout (5001ms) - Timeout exceeded
  
7 scenarios (6 passed, 1 failed)
28 steps (27 passed, 1 failed)
Total: 6.521s
```

### Quality Gate Summary
```
Quality Gates Status
====================
✅ Code Coverage      85.7% > 80%    PASS
✅ EARS Compliance    100% = 100%     PASS
⚠️  BDD Coverage      92% < 95%       WARN
✅ Complexity         7.2 < 10        PASS
✅ Security Scan      No issues       PASS
❌ Performance        215ms > 200ms   FAIL

Overall: FAILED (1 required gate failed)
```

## Failure Handling

### On Test Failure
```
❌ Test Failed: tests/integration/api/auth.test.ts

  UserAuthentication › should handle concurrent logins

  Expected: 200
  Received: 429

  Stack:
    at auth.test.ts:45:15
    at processTicksAndRejections:96:5

  Suggested Fix:
  - Check rate limiting configuration
  - Verify test data cleanup
  - Review concurrent request handling

  Related Code:
  - src/api/auth/rateLimit.ts:23
  - src/services/auth.service.ts:145
```

### On Gate Failure
```
❌ Quality Gate Failed: Code Coverage

Current: 78.5%
Required: 80.0%
Gap: 1.5%

Uncovered Files:
- src/utils/validators.ts (65% coverage)
  Lines: 23-27, 45-52
- src/api/error-handler.ts (71% coverage)
  Lines: 15-19

Run with --coverage-detail for full report
```

## Test Debugging

### Debug Mode
```bash
# Verbose output
/execute-tests --verbose

# Debug specific test
/execute-tests --grep "login" --debug

# With browser UI (Playwright)
/execute-tests --headed

# Slow motion
/execute-tests --slow-mo 100

# Single test file
/execute-tests tests/unit/auth.test.ts
```

### Troubleshooting

**Flaky Tests**
```
⚠️ Flaky Test Detected: tests/e2e/checkout.test.ts
Failure rate: 15% (3/20 runs)
Pattern: Timeout on payment processing
Suggested: Increase timeout or add retry logic
```

**Slow Tests**
```
🐌 Slow Tests Detected:
1. tests/e2e/report-generation.test.ts (45s)
2. tests/integration/bulk-import.test.ts (32s)
3. tests/e2e/full-workflow.test.ts (28s)

Consider: Parallelization or test optimization
```

## Parallel Execution

```bash
# Run in parallel (default: CPU cores)
/execute-tests --parallel

# Specific workers
/execute-tests --parallel 4

# Parallel by suite
/execute-tests --parallel-suites
```

## CI/CD Integration

### GitHub Actions
```yaml
- name: Execute Tests
  run: |
    npm run test:ci
    
- name: Upload Results
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: test-results
    path: |
      coverage/
      test-results/
      screenshots/
```

## Test Reports

### HTML Report
```
✅ HTML report generated: coverage/index.html
📊 View at: http://localhost:8080/coverage
```

### JSON Report
```json
{
  "summary": {
    "total": 234,
    "passed": 228,
    "failed": 4,
    "skipped": 2,
    "duration": "4m 32s"
  },
  "coverage": {
    "lines": 85.7,
    "branches": 82.3,
    "functions": 88.9
  },
  "gates": {
    "passed": ["coverage", "complexity"],
    "failed": ["performance"],
    "warnings": ["bdd_coverage"]
  }
}
```

## State Updates

After test execution:
- Updates `docs/state/test-results.json`
- Updates coverage badges
- Updates sprint progress
- Logs to changelog if significant

## Emergency Commands

```bash
# Skip gates (emergency only)
/execute-tests --skip-gates

# Fast mode (unit only)
/execute-tests --fast

# Smoke tests only
/execute-tests --smoke

# Retry failed tests
/execute-tests --retry-failed
```

## Best Practices

1. **Run frequently** - After every change
2. **Fix immediately** - Don't let failures accumulate
3. **Monitor trends** - Watch for degradation
4. **Optimize slow tests** - Keep feedback fast
5. **Maintain test data** - Clean, consistent, isolated

Ready to execute your comprehensive test suite!
