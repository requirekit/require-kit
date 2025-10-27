# Start Task

Move a task from backlog to in_progress and prepare for implementation.

## Usage
```bash
/task-start TASK-XXX [assignee:name]
```

## Example
```bash
/task-start TASK-042 assignee:john
```

## Process

1. **Validate Task Exists**
   - Check if task exists in `tasks/backlog/`
   - If not in backlog, check current status and report

2. **Check Prerequisites**
   - Verify linked requirements exist
   - Check for blocking dependencies
   - Ensure no other tasks are blocking this one

3. **Update Task Metadata**
   ```yaml
   status: in_progress
   updated: <current timestamp>
   assignee: <provided or current-user>
   ```

4. **Move Task File**
   - Move from `tasks/backlog/TASK-XXX.md`
   - To `tasks/in_progress/TASK-XXX.md`

5. **Create Implementation Checklist**
   Add to task file:
   ```markdown
   ## Implementation Checklist
   - [ ] Review requirements and acceptance criteria
   - [ ] Design solution approach
   - [ ] Implement core functionality
   - [ ] Write unit tests
   - [ ] Write integration tests
   - [ ] Update documentation
   - [ ] Run all tests locally
   ```

6. **Optional: Create Git Branch**
   If in a git repository:
   ```bash
   git checkout -b task/TASK-XXX-<sanitized-title>
   ```

## Output Format
```
🚀 Started TASK-XXX: <title>
👤 Assignee: <assignee>
📁 Moved to: tasks/in_progress/
🕐 Started at: <timestamp>

Linked Requirements:
- REQ-001: <requirement title>
- REQ-002: <requirement title>

Linked BDD Scenarios:
- BDD-001: <scenario title>
- BDD-002: <scenario title>

Implementation Checklist:
□ Review requirements
□ Design solution
□ Implement functionality
□ Write tests
□ Verify locally

Next steps:
- Use `/task-implement TASK-XXX` to generate implementation
- Use `/task-status` to view current board
```

## Validation Rules
- Task must exist in backlog
- Task cannot have unresolved blockers
- Only one task per assignee can be in_progress (configurable)
- Linked requirements must exist

## State Transition Rules
- Can only start tasks from BACKLOG
- Cannot start BLOCKED tasks
- Cannot start COMPLETED tasks
- Can restart tasks from IN_TESTING or IN_REVIEW with confirmation

## Error Handling
- Task not found: "Error: TASK-XXX not found in backlog"
- Task blocked: "Error: TASK-XXX is blocked by: <reason>"
- Already in progress: "Warning: TASK-XXX is already in progress"
- Missing requirements: "Warning: Linked requirements not found: <list>"
