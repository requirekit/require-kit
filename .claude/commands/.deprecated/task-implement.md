# Implement Task

Generate implementation code and tests based on task requirements.

## Usage
```bash
/task-implement TASK-XXX [test-first:true|false]
```

## Example
```bash
/task-implement TASK-042 test-first:true
```

## Process

1. **Load Task Context**
   - Read task file from `tasks/in_progress/`
   - Load linked EARS requirements
   - Load linked BDD scenarios
   - Analyze acceptance criteria

2. **Generate Implementation Plan**
   Based on requirements, create:
   - Component/module structure
   - API endpoints (if applicable)
   - Data models
   - Business logic flow
   - Error handling approach

3. **Test-First Approach (if enabled)**
   Generate tests BEFORE implementation:
   ```python
   # tests/test_<feature>.py
   def test_acceptance_criteria_1():
       """Test that <specific criteria>"""
       # Arrange
       # Act  
       # Assert
       assert False  # Implement me
   ```

4. **Generate Implementation**
   Create actual code files:
   - Core business logic
   - API endpoints/routes
   - Data models/schemas
   - Service layers
   - Utility functions

5. **Generate Comprehensive Tests**
   Create test suite covering:
   - Unit tests for each function/method
   - Integration tests for workflows
   - E2E tests for user scenarios
   - Edge cases and error conditions
   - Performance tests (if applicable)

6. **Update Task File**
   ```markdown
   ## Implementation Summary
   
   ### Files Created
   - src/feature/module.py
   - src/feature/service.py
   - tests/test_feature.py
   - tests/integration/test_feature_flow.py
   
   ### Test Coverage Target
   - Lines: ≥ 80%
   - Branches: ≥ 75%
   - Critical paths: 100%
   
   ### Ready for Testing
   - [ ] All tests written
   - [ ] Code reviewed locally
   - [ ] Documentation updated
   ```

7. **Move to Testing**
   - Move task from `in_progress/` to `in_testing/`
   - Update status to `in_testing`

## Output Format
```
✅ Implementation generated for TASK-XXX

📁 Files Created:
- src/auth/service.py (150 lines)
- src/auth/models.py (75 lines)
- tests/test_auth_service.py (200 lines)
- tests/integration/test_auth_flow.py (100 lines)

🧪 Test Suite:
- Unit tests: 15
- Integration tests: 5
- E2E tests: 3
- Total: 23 tests

📊 Coverage Target: 85%

🔄 Status: Moved to IN_TESTING

Next steps:
- Use `/task-test TASK-XXX` to run tests
- Use `/task-view TASK-XXX` to see details
```

## Implementation Patterns

### Python/FastAPI
```python
# Service layer
class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository
    
    async def process_task(self, task_id: str) -> Result:
        # Implementation based on requirements
        pass

# Tests
@pytest.mark.asyncio
async def test_process_task():
    service = TaskService(MockRepository())
    result = await service.process_task("TASK-001")
    assert result.success
```

### TypeScript/React
```typescript
// Component
export const TaskComponent: React.FC<TaskProps> = ({ task }) => {
    // Implementation based on requirements
    return <div>{/* UI based on specs */}</div>;
};

// Tests
describe('TaskComponent', () => {
    it('should meet acceptance criteria', () => {
        render(<TaskComponent task={mockTask} />);
        // Assertions based on requirements
    });
});
```

### .NET/C#
```csharp
// Service
public class TaskService : ITaskService
{
    public async Task<Result> ProcessTask(string taskId)
    {
        // Implementation based on requirements
    }
}

// Tests
[Fact]
public async Task ProcessTask_ShouldMeetRequirements()
{
    var service = new TaskService();
    var result = await service.ProcessTask("TASK-001");
    Assert.True(result.Success);
}
```

## Validation Rules
- Task must be in IN_PROGRESS status
- Linked requirements must be available
- Target technology stack must be identifiable
- Acceptance criteria must be defined

## Quality Standards
- All public methods must have tests
- Error cases must be handled
- Code must follow project style guide
- Documentation must be included
- No hardcoded values or credentials

## Error Handling
- Task not in progress: "Error: TASK-XXX is not in IN_PROGRESS status"
- No requirements: "Error: No requirements linked to TASK-XXX"
- Implementation conflict: "Warning: Files already exist, use --force to overwrite"
