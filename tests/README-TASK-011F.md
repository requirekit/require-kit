# TASK-011F Test Suite

## Quick Start

Run the comprehensive validation suite:

```bash
python3 tests/validate_task_011f.py
```

Expected output: **58/58 tests passed**

## What This Tests

The validation suite comprehensively tests the `maui-service-specialist` agent documentation created in TASK-011F:

### Files Under Test
- `installer/global/templates/maui-appshell/agents/maui-service-specialist.md`
- `installer/global/templates/maui-navigationpage/agents/maui-service-specialist.md`

### Test Categories (58 Total Tests)

1. **File Existence** (4 tests)
   - Both files exist in correct locations
   - Both files are non-empty

2. **File Equality** (3 tests)
   - Files are byte-for-byte identical
   - Checksums match
   - Line counts match

3. **YAML Frontmatter** (5 tests)
   - Valid YAML syntax
   - Correct agent name
   - Adequate description
   - Tools defined
   - Collaborators listed

4. **Section Completeness** (11 tests)
   - All 10 required sections present
   - Core Responsibility
   - Core Expertise
   - Implementation Patterns
   - Design Patterns
   - Implementation Guidelines
   - Complete Code Examples
   - Anti-Patterns to Avoid
   - Testing Strategies
   - Best Practices Summary
   - Collaboration & Best Practices

5. **Code Examples** (5 tests)
   - 18+ C# code blocks
   - HTTP API service example
   - Location service example
   - Cache service example
   - Substantial code blocks (>500 chars)

6. **ErrorOr Pattern** (3 tests)
   - ErrorOr import present
   - 30+ ErrorOr usages
   - All 5 error types documented

7. **Anti-Patterns** (5 tests)
   - 4+ WRONG/CORRECT pairs
   - Database access anti-pattern
   - Exception throwing anti-pattern
   - Connectivity check anti-pattern
   - Synchronous I/O anti-pattern

8. **Testing Strategies** (7 tests)
   - HTTP service testing
   - Location service testing
   - Cache service testing
   - HTTP mocking patterns
   - xUnit attributes
   - FluentAssertions

9. **Architectural Boundary** (3 tests)
   - Critical boundary documented
   - Service/repository split
   - Service responsibilities

10. **Best Practices** (5 tests)
    - Best practices summary
    - Service boundaries
    - Error handling
    - Resilience patterns
    - Testing principles

11. **Collaboration** (8 tests)
    - Collaboration section exists
    - "When I'm Engaged" section
    - "I Collaborate With" section
    - All 4 collaborators documented

## Test Results

### Last Validation Run

```
======================================================================
VALIDATION SUMMARY
======================================================================
Total tests: 58
Passed: 58
Failed: 0
======================================================================

VALIDATION STATUS: ✓ PASSED
```

### Metrics

```
Line Count:         1,654 lines
Section Count:      10 major sections
Code Blocks:        18 C# examples
ErrorOr Usages:     31 instances
Anti-Pattern Pairs: 4 WRONG/CORRECT pairs
```

## Alternative Test Runners

### Run with pytest (if available)

```bash
python3 -m pytest tests/test_task_011f_validation.py -v
```

### Run with detailed output

```bash
python3 tests/validate_task_011f.py 2>&1 | tee test-results.log
```

## CI/CD Integration

Add to `.github/workflows/test.yml`:

```yaml
- name: Validate TASK-011F
  run: python3 tests/validate_task_011f.py
```

## Dependencies

**None!** The validation script uses only Python standard library:
- `hashlib` - Checksum verification
- `pathlib` - File path handling
- `re` - Pattern matching
- `sys` - Exit codes

No `pip install` required.

## Test Coverage

### Acceptance Criteria Coverage

✅ **AC1: File Creation**
- Both files created in correct locations
- Files are byte-for-byte identical

✅ **AC2: Content Structure**
- 10/10 required sections present
- Valid YAML frontmatter
- Hierarchical structure

✅ **AC3: Code Examples**
- 18 C# code blocks (3+ required)
- 3 complete service implementations
- 3 design patterns
- 3 test suites

✅ **AC4: ErrorOr Pattern**
- 31 usages (baseline required)
- All 5 error types

✅ **AC5: Anti-Patterns**
- 4 WRONG/CORRECT pairs
- Architectural boundaries
- Error handling patterns

✅ **AC6: Testing Strategies**
- HTTP service testing
- Platform service testing
- Cache service testing

✅ **AC7: Collaboration**
- 4 collaborating agents
- Engagement scenarios
- Best practices

## Detailed Report

For comprehensive test results and analysis, see:
- **Full Report**: `tests/TASK-011F-TEST-REPORT.md`
- **Test Script**: `tests/validate_task_011f.py`
- **Pytest Suite**: `tests/test_task_011f_validation.py`

## Troubleshooting

### If tests fail

1. **File not found**
   ```
   Ensure files exist:
   - installer/global/templates/maui-appshell/agents/maui-service-specialist.md
   - installer/global/templates/maui-navigationpage/agents/maui-service-specialist.md
   ```

2. **Files not identical**
   ```bash
   diff installer/global/templates/maui-appshell/agents/maui-service-specialist.md \
        installer/global/templates/maui-navigationpage/agents/maui-service-specialist.md
   ```

3. **Section missing**
   ```
   Check that all 10 required sections are present with exact heading names
   ```

4. **Python not found**
   ```bash
   # Use python3 explicitly
   python3 tests/validate_task_011f.py
   ```

## Success Criteria

For TASK-011F to be considered complete:
- ✅ All 58 tests must pass
- ✅ Files must be byte-for-byte identical
- ✅ All acceptance criteria validated
- ✅ Exit code 0

Current Status: **✅ ALL CRITERIA MET**
