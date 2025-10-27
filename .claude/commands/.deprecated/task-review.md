# Review Task

Move a task to review after tests pass, preparing for final completion.

## Usage
```bash
/task-review TASK-XXX [reviewer:name] [checklist:strict|standard|quick]
```

## Example
```bash
/task-review TASK-042 reviewer:alice checklist:strict
```

## Process

1. **Verify Test Results**
   Check that task has:
   - Status: `in_testing`
   - test_results.status: `passed`
   - Coverage meets thresholds
   - No critical failures

2. **Generate Review Checklist**
   
   ### Strict Checklist (for critical features)
   ```markdown
   ## Code Review Checklist
   - [ ] All acceptance criteria met
   - [ ] Tests coverage ≥ 90%
   - [ ] No security vulnerabilities
   - [ ] Performance benchmarks met
   - [ ] Documentation complete
   - [ ] Error handling comprehensive
   - [ ] Logging appropriate
   - [ ] No hardcoded values
   - [ ] Code follows style guide
   - [ ] Accessibility standards met
   - [ ] Backward compatibility maintained
   - [ ] Database migrations tested
   - [ ] API contracts validated
   - [ ] Integration points verified
   - [ ] Rollback plan documented
   ```
   
   ### Standard Checklist (default)
   ```markdown
   ## Code Review Checklist
   - [ ] Acceptance criteria met
   - [ ] Tests passing with ≥ 80% coverage
   - [ ] No obvious security issues
   - [ ] Basic documentation present
   - [ ] Error handling implemented
   - [ ] Code follows conventions
   - [ ] No console.logs or debug code
   ```
   
   ### Quick Checklist (for minor changes)
   ```markdown
   ## Code Review Checklist
   - [ ] Tests passing
   - [ ] No broken functionality
   - [ ] Code looks reasonable
   ```

3. **Verify Requirements Traceability**
   Ensure all linked requirements are:
   - Implemented in code
   - Covered by tests
   - Documented properly

4. **Check BDD Scenarios**
   Verify that linked scenarios:
   - Have corresponding tests
   - Pass when executed
   - Match implementation

5. **Performance Review**
   If applicable, verify:
   - Response times meet SLA
   - Memory usage acceptable
   - Database queries optimized
   - No N+1 query problems

6. **Security Review**
   Check for:
   - Input validation
   - SQL injection prevention
   - XSS prevention
   - Proper authentication
   - Authorization checks
   - Sensitive data handling

7. **Update Task Status**
   ```yaml
   status: in_review
   updated: <timestamp>
   reviewer: <reviewer name>
   review_checklist: |
     - [x] Tests passing
     - [x] Coverage adequate
     - [ ] Documentation updated
     - [ ] Security reviewed
   ```

8. **Move Task File**
   Move from `tasks/in_testing/` to `tasks/in_review/`

## Output Format
```
📋 TASK-XXX moved to REVIEW

Task: Implement user authentication
Reviewer: alice
Review Type: Standard

✅ Pre-Review Verification:
├─ Tests: 25/25 passing ✅
├─ Coverage: 87.5% ✅
├─ Performance: <100ms ✅
└─ Security: Basic checks passed ✅

📝 Review Checklist:
□ Acceptance criteria met
□ Tests adequate
□ Documentation updated
□ Code quality acceptable
□ Security reviewed
□ Performance acceptable

📊 Requirements Coverage:
├─ REQ-001: ✅ Implemented & Tested
├─ REQ-002: ✅ Implemented & Tested
└─ REQ-003: ⚠️ Partially implemented

🔍 Files to Review:
- src/auth/service.py (150 lines)
- src/auth/models.py (75 lines)
- tests/test_auth.py (200 lines)

Next steps:
- Complete review checklist
- Use `/task-complete TASK-XXX` when approved
- Use `/task-request-changes TASK-XXX` if changes needed
```

## Review Feedback Options

### Request Changes
```bash
/task-request-changes TASK-XXX "Feedback details"
```
This moves task back to IN_PROGRESS with feedback.

### Conditional Approval
```bash
/task-approve-with-conditions TASK-XXX "Conditions"
```
Approves but requires minor fixes before completion.

### Full Approval
```bash
/task-approve TASK-XXX
```
Marks all checklist items as complete.

## Code Review Integration

### GitHub PR Integration
If linked to a GitHub PR:
```bash
gh pr review <pr-number> --approve
gh pr merge <pr-number>
```

### GitLab MR Integration
If linked to GitLab MR:
```bash
glab mr approve <mr-number>
glab mr merge <mr-number>
```

## Quality Metrics Tracking
Track review metrics:
- Review duration
- Number of iterations
- Common issues found
- Reviewer workload

## Review Report Template
```markdown
# Review Report - TASK-XXX

## Summary
- **Reviewer**: alice
- **Date**: 2024-01-15
- **Duration**: 45 minutes
- **Result**: APPROVED WITH CONDITIONS

## Strengths
- Comprehensive test coverage
- Clean code structure
- Good error handling

## Issues Found
1. Missing API documentation
2. Performance could be optimized in auth loop
3. Some edge cases not covered

## Conditions for Approval
- [ ] Add API documentation
- [ ] Optimize authentication loop
- [ ] Add test for edge case X

## Overall Assessment
Good implementation that meets requirements. Minor improvements needed before deployment.
```

## Validation Rules
- Task must be in IN_TESTING status
- Tests must be passing
- Coverage must meet minimum thresholds
- No CRITICAL security issues
- At least one reviewer must be assigned

## Error Handling
- Tests not passing: "Error: Cannot review - tests are failing"
- Coverage too low: "Warning: Coverage below threshold but review allowed"
- Missing requirements: "Warning: Some requirements not verified"
- No reviewer: "Error: Reviewer must be specified"
