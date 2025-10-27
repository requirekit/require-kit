# Link Requirements to Task

Link EARS requirements to a task for traceability and validation.

## Usage
```bash
/task-link-requirements TASK-XXX REQ-YYY [REQ-ZZZ ...]
```

## Example
```bash
/task-link-requirements TASK-042 REQ-001 REQ-002 REQ-003
```

## Process

1. **Validate Task Exists**
   - Check task file in any state directory
   - Load current task metadata

2. **Validate Requirements Exist**
   - Check each requirement in `docs/requirements/`
   - Verify requirement files are valid EARS format

3. **Analyze Requirement Relevance**
   - Extract requirement descriptions
   - Check for keyword matches with task title
   - Suggest additional related requirements

4. **Update Task File**
   ```yaml
   requirements: [REQ-001, REQ-002, REQ-003]
   requirement_coverage:
     REQ-001:
       title: "User authentication"
       status: "pending"
       tests: []
     REQ-002:
       title: "Session management"
       status: "pending"
       tests: []
     REQ-003:
       title: "Password validation"
       status: "pending"
       tests: []
   ```

5. **Create Requirement Checklist**
   Add to task file:
   ```markdown
   ## Requirements Coverage
   - [ ] REQ-001: User authentication
     - Acceptance criteria from requirement
     - Test cases to implement
   - [ ] REQ-002: Session management
     - Acceptance criteria from requirement
     - Test cases to implement
   - [ ] REQ-003: Password validation
     - Acceptance criteria from requirement
     - Test cases to implement
   ```

6. **Generate Test Mapping**
   Create test requirements based on linked requirements:
   ```markdown
   ## Test Requirements from EARS
   
   ### REQ-001: User authentication
   - test_valid_login()
   - test_invalid_credentials()
   - test_account_lockout()
   
   ### REQ-002: Session management
   - test_session_creation()
   - test_session_timeout()
   - test_session_refresh()
   
   ### REQ-003: Password validation
   - test_password_strength()
   - test_password_history()
   - test_password_reset()
   ```

## Output Format
```
✅ Requirements linked to TASK-042

📋 Linked Requirements (3):
├─ REQ-001: User authentication
│  Type: Event-driven
│  Priority: High
│  Tests needed: 3
│
├─ REQ-002: Session management
│  Type: State-driven
│  Priority: High
│  Tests needed: 3
│
└─ REQ-003: Password validation
   Type: Ubiquitous
   Priority: Medium
   Tests needed: 3

📊 Coverage Analysis:
- Total acceptance criteria: 9
- Test cases required: 9
- Estimated effort: 2 days

🔗 Traceability established:
Requirements → Task → Tests → Implementation

📝 Next steps:
- Review requirement details in docs/requirements/
- Use `/task-implement TASK-042` to generate code
- Tests will be mapped to requirements automatically
```

## Validation Rules
- Task must exist
- Requirements must exist in docs/requirements/
- Requirements must be valid EARS format
- No duplicate requirement links
- Maximum 10 requirements per task (configurable)

## Requirement Analysis

### EARS Pattern Detection
```python
def analyze_requirement_pattern(req_text):
    patterns = {
        'ubiquitous': r'The .* shall .*',
        'event_driven': r'When .*, the .* shall .*',
        'state_driven': r'While .*, the .* shall .*',
        'optional': r'Where .*, the .* shall .*',
        'unwanted': r'If .*, then the .* shall .*'
    }
    
    for pattern_type, regex in patterns.items():
        if re.match(regex, req_text):
            return pattern_type
    return 'unknown'
```

### Test Generation Rules
- Ubiquitous: Basic functionality tests
- Event-driven: Trigger and response tests
- State-driven: State transition tests
- Optional: Feature flag tests
- Unwanted: Error handling tests

## Auto-Discovery

### Find Related Requirements
```bash
/task-discover-requirements TASK-XXX
```
Automatically finds and suggests requirements based on:
- Task title keywords
- Task description content
- Similar completed tasks
- Tag matches

### Bulk Linking
```bash
/task-link-requirements TASK-XXX --all-matching
```
Links all requirements that match task keywords.

## Requirement Verification

### Check Coverage
```bash
/task-check-requirements TASK-XXX
```
Verifies that:
- All linked requirements have tests
- All tests map to requirements
- No requirements are missing coverage
- No orphaned tests exist

### Generate Coverage Report
```markdown
# Requirements Coverage Report - TASK-XXX

## Summary
- Requirements Linked: 3
- Requirements Covered: 2 (67%)
- Tests Mapped: 6/9 (67%)

## Coverage Details

### ✅ REQ-001: User authentication
- Status: COVERED
- Tests: 3/3 implemented
- All acceptance criteria met

### ⚠️ REQ-002: Session management
- Status: PARTIAL
- Tests: 2/3 implemented
- Missing: test_session_refresh()

### ❌ REQ-003: Password validation
- Status: NOT COVERED
- Tests: 0/3 implemented
- Action needed: Implement all tests

## Recommendations
1. Implement missing session refresh test
2. Add all password validation tests
3. Run full test suite to verify
```

## Integration with Implementation

When `/task-implement` is called:
1. Load all linked requirements
2. Parse EARS statements
3. Generate code that satisfies requirements
4. Create tests that verify requirements
5. Map tests back to requirement IDs

Example test annotation:
```python
@pytest.mark.requirement("REQ-001")
def test_user_authentication():
    """Verifies REQ-001: User authentication requirement"""
    # Test implementation
    pass
```

## Traceability Matrix

Generate a full traceability matrix:
```bash
/task-traceability TASK-XXX
```

Output:
```
Traceability Matrix - TASK-XXX
================================

Requirement | Task | Implementation | Tests | Status
------------|------|----------------|-------|--------
REQ-001     | ✅   | auth.py:45     | 3/3   | PASS
REQ-002     | ✅   | session.py:12  | 2/3   | PARTIAL
REQ-003     | ✅   | validate.py:8  | 0/3   | FAIL

Legend:
✅ Linked/Implemented
⚠️ Partial
❌ Missing/Failed
```

## Best Practices

1. **Link requirements early** - Before implementation
2. **Keep links updated** - Add new requirements as discovered
3. **Verify coverage** - Before marking task complete
4. **Document gaps** - If requirement cannot be fully met
5. **Review traceability** - During task review phase
