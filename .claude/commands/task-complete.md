# Complete Task

Mark a task as complete after review approval and final verification.

## Feature Detection and Package Integration

The `/task-complete` command automatically detects which Agentecflow packages are installed and adapts its validation and reporting accordingly, enabling **bidirectional optional integration** between taskwright and require-kit.

### Package-Specific Features

| Installed Packages | Available Features | Unavailable Features |
|-------------------|-------------------|----------------------|
| **taskwright only** | ✅ Task completion workflow<br>✅ Quality gate validation<br>✅ File organization<br>✅ Basic metrics | ❌ Requirements satisfaction check<br>❌ BDD scenario validation<br>❌ Epic/Feature rollup<br>❌ PM tool sync |
| **Both installed** | ✅ All features above<br>✅ Requirements verification<br>✅ BDD scenario validation<br>✅ Epic/Feature progress rollup<br>✅ PM tool synchronization | None - full integration |

### Graceful Degradation

**When require-kit is not installed:**
- ✅ Task completion proceeds normally
- ✅ Quality gates validated (tests, coverage)
- ✅ Files organized into completed directory
- ℹ️ Requirements satisfaction check skipped
- ℹ️ BDD scenario validation skipped
- ℹ️ Epic/Feature rollup skipped
- ℹ️ PM tool sync skipped

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

   **Always Validated (taskwright):**
   - Status is `in_review`
   - All tests are passing
   - Coverage meets thresholds
   - Review checklist is complete
   - No outstanding blockers

   **Additional Validation (require-kit installed):**
   - All linked requirements are satisfied ✨
   - All BDD scenarios pass ✨
   - Epic/Feature progress calculated ✨

2. **Capture Final Metrics**
   ```yaml
   completion_metrics:
     total_duration: <from created to completed>
     implementation_time: <in_progress duration>
     testing_time: <in_testing duration>
     review_time: <in_review duration>
     test_iterations: <number of test runs>
     final_coverage: <coverage percentage>
     requirements_met: <count/total>  # Only if require-kit installed
     scenarios_passed: <count/total>   # Only if require-kit installed
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

### Example 1: taskwright only (Graceful Degradation)
```
✅ TASK-XXX COMPLETED!

ℹ️  Package Detection:
- taskwright: ✅ installed
- require-kit: ❌ not installed

📊 Task Summary:
Title: Implement user authentication
Duration: 3 days 4 hours
Implementation: 1 day 6 hours
Testing: 8 hours
Review: 4 hours

📈 Final Metrics:
- Tests: 25/25 passing ✅
- Coverage: 87.5% ✅

📁 Archived to: tasks/completed/TASK-042/

🎯 Impact:
- 5 files created
- 25 tests added
- 0 defects introduced

ℹ️  Optional Features Skipped:
- Requirements validation (install require-kit)
- BDD scenario verification (install require-kit)
- Epic/Feature progress rollup (install require-kit)
- PM tool synchronization (install require-kit)

Great work! 🎉
```

### Example 2: Both packages installed (Full Integration)
```
✅ TASK-XXX COMPLETED!

ℹ️  Package Detection:
- taskwright: ✅ installed
- require-kit: ✅ installed

📊 Task Summary:
Title: Implement user authentication
Duration: 3 days 4 hours
Implementation: 1 day 6 hours
Testing: 8 hours
Review: 4 hours

📈 Final Metrics (Core):
- Tests: 25/25 passing ✅
- Coverage: 87.5% ✅

📈 Final Metrics (require-kit):
- Requirements: 3/3 met ✅
- BDD Scenarios: 5/5 passing ✅

📊 Progress Rollup:
- Feature FEAT-003: 65% → 85% (+20%)
- Epic EPIC-001: 57% → 63% (+6%)

🔄 External Tool Updates:
✅ Jira Sub-task PROJ-129: Status → "Done"
✅ Linear Issue PROJECT-461: Status → "Completed"

📁 Archived to: tasks/completed/TASK-042/

🎯 Impact:
- 5 files created
- 25 tests added
- 3 requirements satisfied
- 0 defects introduced

Great work! 🎉
```

## Validation Rules

### Cannot Complete If:

**Always Enforced (taskwright):**
- Status is not `in_review`
- Any tests are failing
- Coverage is below threshold
- Review checklist has unchecked items

**Additional Checks (require-kit installed):**
- Linked requirements are not satisfied
- Critical BDD scenarios are failing

### Warning Conditions:
- No lessons learned documented
- No performance metrics captured
- Missing documentation updates

## Integration Actions

### GitHub Integration (Always Available)
```bash
# Close linked issue
gh issue close <issue-number> --comment "Completed in TASK-XXX"

# Update PR
gh pr merge <pr-number> --squash --subject "feat: TASK-XXX completed"
```

### PM Tool Integration (require-kit only)
When require-kit is installed, automatic synchronization with:
- **Jira**: Update Sub-task status to "Done"
- **Linear**: Update Issue status to "Completed"
- **GitHub Projects**: Close linked issue
- **Azure DevOps**: Update Task status

### Slack Notification (Always Available)
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
    "requirements_met": 3  // Only if require-kit installed
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
