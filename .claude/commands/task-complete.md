# Complete Task

Mark a task as complete after review approval and final verification.

## Usage
```bash
/task-complete TASK-XXX [archive:true|false]
```

## Example
```bash
/task-complete TASK-042 archive:true
```

## Process

1. **Final Verification Checklist**
   Verify that:
   - Status is `in_review`
   - All tests are passing
   - Coverage meets thresholds
   - Review checklist is complete
   - No outstanding blockers
   - All linked requirements are satisfied
   - All BDD scenarios pass

2. **Capture Final Metrics**
   ```yaml
   completion_metrics:
     total_duration: <from created to completed>
     implementation_time: <in_progress duration>
     testing_time: <in_testing duration>
     review_time: <in_review duration>
     test_iterations: <number of test runs>
     final_coverage: <coverage percentage>
     requirements_met: <count/total>
     scenarios_passed: <count/total>
   ```

3. **Generate Completion Report**
   ```markdown
   # Task Completion Report - TASK-XXX
   
   ## Summary
   **Task**: <title>
   **Completed**: <timestamp>
   **Duration**: <total days/hours>
   **Final Status**: ✅ COMPLETED
   
   ## Deliverables
   - Files created: <count>
   - Tests written: <count>
   - Coverage achieved: <percentage>
   - Requirements satisfied: <count/total>
   
   ## Quality Metrics
   - All tests passing: ✅
   - Coverage threshold met: ✅
   - Performance benchmarks: ✅
   - Security review: ✅
   - Documentation complete: ✅
   
   ## Lessons Learned
   - What went well: <summary>
   - Challenges faced: <summary>
   - Improvements for next time: <summary>
   ```

4. **Update Task Metadata**
   ```yaml
   status: completed
   completed_at: <timestamp>
   completion_metrics: <metrics object>
   final_test_results: <last test run>
   ```

5. **Archive Task**
   - Move from `tasks/in_review/` to `tasks/completed/`
   - Optionally create archive with timestamp: `tasks/completed/2024-01/TASK-XXX.md`

6. **Update Project Metrics**
   - Increment completed task count
   - Update velocity metrics
   - Update coverage trends
   - Record cycle time

7. **Trigger Post-Completion Actions**
   - Update linked GitHub issue (if any)
   - Notify stakeholders
   - Update documentation
   - Trigger deployment (if configured)

## Output Format
```
✅ TASK-XXX COMPLETED!

📊 Task Summary:
Title: Implement user authentication
Duration: 3 days 4 hours
Implementation: 1 day 6 hours
Testing: 8 hours
Review: 4 hours

📈 Final Metrics:
- Tests: 25/25 passing ✅
- Coverage: 87.5% ✅
- Requirements: 3/3 met ✅
- BDD Scenarios: 5/5 passing ✅

📁 Archived to: tasks/completed/TASK-042.md

🎯 Impact:
- 5 files created
- 25 tests added
- 3 requirements satisfied
- 0 defects introduced

🚀 Next Steps:
- Deploy to staging (if applicable)
- Update user documentation
- Monitor for issues

Great work! 🎉
```

## Validation Rules

### Cannot Complete If:
- Status is not `in_review`
- Any tests are failing
- Coverage is below threshold
- Review checklist has unchecked items
- Linked requirements are not satisfied
- Critical BDD scenarios are failing

### Warning Conditions:
- No lessons learned documented
- No performance metrics captured
- Missing documentation updates

## Integration Actions

### GitHub Integration
```bash
# Close linked issue
gh issue close <issue-number> --comment "Completed in TASK-XXX"

# Update PR
gh pr merge <pr-number> --squash --subject "feat: TASK-XXX completed"
```

### Slack Notification
```json
{
  "text": "Task Completed! 🎉",
  "blocks": [
    {
      "type": "section",
      "text": {
        "text": "TASK-XXX: Implement user authentication\nCompleted after 3 days with 87.5% coverage"
      }
    }
  ]
}
```

### Metrics Dashboard Update
```json
{
  "task_id": "TASK-XXX",
  "completed_at": "2024-01-15T16:00:00Z",
  "metrics": {
    "duration_hours": 76,
    "coverage": 87.5,
    "tests_added": 25,
    "requirements_met": 3
  }
}
```

## Completion Criteria

### Definition of Done
A task is considered DONE when:
1. ✅ All acceptance criteria are met
2. ✅ Code is written and follows standards
3. ✅ Tests are written and passing
4. ✅ Coverage meets or exceeds threshold
5. ✅ Code has been reviewed
6. ✅ Documentation is updated
7. ✅ No known defects remain
8. ✅ Performance requirements are met
9. ✅ Security requirements are satisfied
10. ✅ Task is deployed or ready for deployment

## Archive Strategy

### Folder Structure
```
tasks/completed/
├── 2024-01/
│   ├── TASK-001.md
│   ├── TASK-002.md
│   └── TASK-003.md
├── 2024-02/
│   ├── TASK-004.md
│   └── TASK-005.md
└── index.md  # Summary of all completed tasks
```

### Archive Index Entry
```markdown
## TASK-XXX: <title>
- **Completed**: 2024-01-15
- **Duration**: 3 days
- **Coverage**: 87.5%
- **Files**: [View](./2024-01/TASK-XXX.md)
```

## Error Handling
- Not in review: "Error: Task must be in review before completion"
- Tests failing: "Error: Cannot complete task with failing tests"
- Coverage low: "Error: Coverage 75% is below 80% threshold"
- Review incomplete: "Error: Review checklist has unchecked items"

## Best Practices
1. Always capture lessons learned
2. Document any technical debt incurred
3. Update team knowledge base
4. Celebrate completions! 🎉
5. Review metrics for continuous improvement
