# Agentecflow Task Management System with Test Verification
## Integration Plan for Issue/Task Commands with Software Engineering Lifecycle

### Executive Summary
This document outlines the integration of an issue/task command system (similar to uk-probate-agent) with the Agentecflow methodology, emphasizing test verification and proper software engineering lifecycle adherence to prevent the common problem of "implemented but not working" code.

---

## 1. Current State Analysis

### From uk-probate-agent
- **Issue command** (`/issue`) with structured workflow (PLAN → CREATE → TEST → DEPLOY)
- **Test integration** via MCP tools (pytest, playwright)
- **Quality gates** with completion checklists
- **Domain-specific handling** (Figma, React, Backend, Legal)

### From Agentecflow System
- **EARS requirements** → **BDD scenarios** → **Tasks** → **Implementation**
- **State tracking** in markdown files
- **Quality gates** configuration
- **Template-based development**

### Key Problems to Solve
1. **"False completion"** - Claude Code reports completion but functionality doesn't work
2. **Test verification gap** - No automatic verification that tests actually pass
3. **State management** - Manual movement of completed tasks
4. **Traceability** - Linking implementation back to requirements

---

## 2. Proposed Enhanced Task Command System

### 2.1 Task Lifecycle States
```
BACKLOG → IN_PROGRESS → IN_TESTING → IN_REVIEW → COMPLETED → ARCHIVED
                          ↓
                      BLOCKED/FAILED
```

### 2.2 Enhanced Task Command Structure

```markdown
# .claude/commands/task.md
---
name: task
description: Manage tasks with full lifecycle tracking and test verification
---

Execute task following Agentecflow methodology: $ARGUMENTS

## TASK LIFECYCLE PHASES

### Phase 1: ANALYSIS
1. **Load task definition** from `docs/tasks/TASK-XXX.md`
2. **Verify prerequisites**:
   - ✓ Linked requirement exists (REQ-XXX)
   - ✓ BDD scenario defined (BDD-XXX)
   - ✓ Dependencies resolved
   - ✓ Test approach documented
3. **Update task status**: `pending` → `in_progress`
4. **Create work branch**: `task/TASK-XXX-description`

### Phase 2: IMPLEMENTATION
1. **Test-First Development**:
   - Write failing test based on BDD scenario
   - Implement minimal code to pass
   - Refactor while keeping tests green
2. **Pattern Compliance**:
   - Follow template patterns from `.claude/CLAUDE.md`
   - Use established project patterns
   - Maintain consistency with existing code
3. **Incremental commits** with descriptive messages

### Phase 3: VERIFICATION (MANDATORY)
1. **Run automated tests**:
   ```bash
   # For Python projects
   @mcp-code-checker run_pytest_check --verbosity 2
   
   # For .NET projects
   dotnet test --logger "console;verbosity=detailed"
   
   # For React/TypeScript
   npm test -- --coverage
   ```
2. **Capture test results** in task metadata
3. **Run integration tests** if applicable
4. **Performance verification** against requirements
5. **Update task status**: `in_progress` → `in_testing`

### Phase 4: VALIDATION
1. **Manual verification checklist**:
   - [ ] Feature works as described in requirement
   - [ ] All acceptance criteria met
   - [ ] No regression in existing features
   - [ ] Documentation updated
2. **Quality gate checks**:
   - Code coverage ≥ 80%
   - All tests passing
   - No critical linting errors
   - Performance benchmarks met
3. **Update task status**: `in_testing` → `in_review`

### Phase 5: COMPLETION
1. **Move task file** to `docs/worklog/completed/tasks/`
2. **Update metadata** with completion details
3. **Update sprint state** in `docs/state/current-sprint.md`
4. **Create PR** with test results included
5. **Update task status**: `in_review` → `completed`

## MANDATORY TEST VERIFICATION

### Automated Test Execution
EVERY task implementation MUST include:
1. **Test execution with output capture**
2. **Results saved to task metadata**
3. **Screenshot/video for UI components**
4. **Performance metrics logged**

### Test Result Format
```yaml
test_results:
  timestamp: 2024-12-20T10:30:00Z
  summary:
    total: 15
    passed: 14
    failed: 1
    skipped: 0
  coverage: 85%
  performance:
    render_time: 95ms
    response_time: 120ms
  failures:
    - test_name: test_edge_case_handling
      reason: "AssertionError: Expected 200, got 404"
  evidence:
    - screenshots/test-results.png
    - logs/test-output.log
```

## FAILURE HANDLING

If tests fail:
1. **Update status**: `in_testing` → `blocked`
2. **Document failure** in task file
3. **Fix implementation**
4. **Re-run tests**
5. **Only proceed when ALL tests pass**

## TASK COMMAND VARIANTS

### /task implement TASK-XXX
Full implementation with test verification

### /task test TASK-XXX
Run tests for existing implementation

### /task complete TASK-XXX
Move to completed with all checks

### /task status
Show current task states across board
```

---

## 3. Kanban Board Structure

```
docs/
├── kanban/
│   ├── backlog/           # Unstarted tasks
│   │   └── TASK-XXX.md
│   ├── in-progress/       # Active development
│   │   └── TASK-XXX.md
│   ├── in-testing/        # Awaiting test verification
│   │   └── TASK-XXX.md
│   ├── in-review/         # Tests passed, awaiting review
│   │   └── TASK-XXX.md
│   ├── blocked/           # Failed tests or dependencies
│   │   └── TASK-XXX.md
│   └── completed/         # Done with all verification
│       ├── 2024-Q4/
│       └── 2025-Q1/
│           └── TASK-XXX.md
```

---

## 4. Enhanced Task Template

```markdown
# docs/tasks/TASK-XXX.md
---
id: TASK-XXX
title: Implement Feature X
type: implementation
requirement: REQ-XXX
bdd_scenario: BDD-XXX
status: pending  # pending|in_progress|in_testing|in_review|completed|blocked
assigned_to: claude
created: 2024-12-20
updated: 2024-12-20
estimated_hours: 2
actual_hours: null
branch: task/TASK-XXX-feature-x
---

## Task Description
Clear description of what needs to be implemented

## Acceptance Criteria
- [ ] Criterion 1 (testable)
- [ ] Criterion 2 (measurable)
- [ ] Criterion 3 (observable)

## Test Requirements
### Unit Tests
- [ ] Test case 1
- [ ] Test case 2

### Integration Tests
- [ ] End-to-end scenario
- [ ] API integration

### Performance Tests
- [ ] Response time < 200ms
- [ ] Memory usage < 100MB

## Implementation Checklist
- [ ] Write failing tests first
- [ ] Implement feature
- [ ] All tests passing
- [ ] Code review ready
- [ ] Documentation updated

## Test Results
```yaml
# Automatically populated by task command
test_runs:
  - run_1:
      timestamp: null
      passed: null
      failed: null
      coverage: null
```

## Completion Evidence
- Test output: [link]
- Screenshots: [link]
- Performance metrics: [link]

## Lessons Learned
[Filled on completion]
```

---

## 5. Test Verification Integration

### 5.1 MCP Tool Integration
```python
# .claude/scripts/verify_tests.py
import subprocess
import json
import yaml
from pathlib import Path

class TestVerifier:
    def __init__(self, task_id):
        self.task_id = task_id
        self.task_file = Path(f"docs/tasks/{task_id}.md")
        
    def run_tests(self, test_type="all"):
        """Run tests and capture results"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "summary": {},
            "failures": []
        }
        
        # Run appropriate test suite
        if self.is_python_project():
            results = self.run_pytest()
        elif self.is_dotnet_project():
            results = self.run_dotnet_tests()
        elif self.is_node_project():
            results = self.run_npm_tests()
            
        return results
    
    def run_pytest(self):
        """Run pytest with coverage"""
        cmd = ["pytest", "--cov", "--json-report", "-v"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Parse JSON report
        report = json.loads(Path(".report.json").read_text())
        
        return {
            "passed": result.returncode == 0,
            "summary": report["summary"],
            "coverage": self.get_coverage(),
            "failures": report.get("failures", [])
        }
    
    def update_task_file(self, results):
        """Update task file with test results"""
        # Read task file
        content = self.task_file.read_text()
        
        # Update test results section
        # ... YAML manipulation ...
        
        # Write back
        self.task_file.write_text(updated_content)
        
    def verify_acceptance_criteria(self):
        """Check if all acceptance criteria are met"""
        # Parse task file
        # Check each criterion against test results
        # Return validation status
        pass
```

### 5.2 Command Enhancement
```markdown
# .claude/commands/test-verify.md
---
name: test-verify
description: Run tests and verify task completion
---

## Usage
/test-verify TASK-XXX [--type unit|integration|all]

## Process
1. Locate task file
2. Identify project type
3. Run appropriate tests
4. Capture results
5. Update task metadata
6. Move to next state if passing
7. Block if failing

## Example
```bash
/test-verify TASK-001 --type all

# Output:
Running tests for TASK-001...
✓ Unit tests: 15/15 passed
✓ Integration tests: 5/5 passed
✓ Coverage: 87%
✓ Performance: 95ms render time

Task TASK-001 verified successfully!
Moving to: in-review
```
```

---

## 6. Workflow Integration

### 6.1 Complete Task Workflow
```mermaid
graph TD
    A[Create Task] --> B[/task implement TASK-XXX]
    B --> C{Implementation}
    C --> D[Write Tests]
    D --> E[Write Code]
    E --> F[/test-verify TASK-XXX]
    F --> G{Tests Pass?}
    G -->|Yes| H[Move to Review]
    G -->|No| I[Fix Issues]
    I --> E
    H --> J[/task complete TASK-XXX]
    J --> K[Archive in Completed]
```

### 6.2 Daily Workflow Commands
```bash
# Morning: Check task board
/task status

# Start new task
/task implement TASK-001

# After implementation
/test-verify TASK-001

# If tests pass
/task complete TASK-001

# View completed work
/task history --period=week
```

---

## 7. Quality Gates Configuration

```yaml
# .claude/hooks/task-quality-gates.yml
task_quality_gates:
  pre_implementation:
    - requirement_exists: true
    - bdd_scenario_defined: true
    - dependencies_resolved: true
    
  post_implementation:
    - tests_written: true
    - tests_passing: true
    - coverage_threshold: 80
    - no_linting_errors: true
    
  pre_completion:
    - all_acceptance_criteria_met: true
    - documentation_updated: true
    - peer_review_approved: false  # Optional initially
    
  performance:
    react:
      render_time: 100ms
      bundle_size: 50kb
    api:
      response_time: 200ms
      throughput: 100rps
    mobile:
      startup_time: 2s
      memory_usage: 100mb
```

---

## 8. Implementation Priorities

### Phase 1: Core Commands (Week 1)
1. Create `/task` command with basic lifecycle
2. Implement test verification for one language (start with current project type)
3. Set up Kanban folder structure
4. Create task movement automation

### Phase 2: Test Integration (Week 2)
1. Integrate MCP test tools
2. Add test result capture
3. Implement quality gate checks
4. Add failure handling

### Phase 3: Reporting (Week 3)
1. Task completion metrics
2. Test coverage trends
3. Velocity tracking
4. Burndown charts

### Phase 4: Advanced Features (Week 4)
1. Dependency management
2. Parallel task handling
3. Automated PR creation
4. CI/CD integration

---

## 9. Success Metrics

### Reliability Metrics
- **False positive rate**: < 5% (claimed complete but not working)
- **Test verification rate**: 100% (all tasks have test results)
- **Regression rate**: < 2% (breaking existing features)

### Productivity Metrics
- **Task completion time**: Reduced by 30%
- **Rework rate**: < 10%
- **First-time quality**: > 90%

### Quality Metrics
- **Code coverage**: > 80% average
- **Test pass rate**: > 95%
- **Performance compliance**: > 90%

---

## 10. Migration Strategy

### For New Projects
1. Use new task command from start
2. All tasks go through verification
3. Strict enforcement of gates

### For Existing Projects (like MauiAgentecFlow)
1. Start with new tasks only
2. Gradually migrate existing tasks
3. Retrofit tests where needed
4. Phase in quality gates

---

## 11. Common Failure Scenarios and Solutions

### Scenario 1: "Works on my machine"
**Problem**: Claude Code tests in wrong environment
**Solution**: Standardized test environments, containerization

### Scenario 2: "Partial implementation"
**Problem**: Core works but edge cases fail
**Solution**: Comprehensive test requirements in task definition

### Scenario 3: "Lost context"
**Problem**: Claude forgets previous implementation details
**Solution**: Task file maintains full context and history

### Scenario 4: "Test false positives"
**Problem**: Tests pass but feature doesn't work
**Solution**: Integration tests, manual verification checklist

---

## 12. Next Steps

1. **Review and refine** this plan
2. **Choose pilot project** (MauiAgentecFlow recommended)
3. **Implement Phase 1** commands
4. **Test with real tasks**
5. **Iterate based on feedback**
6. **Roll out to all projects**

---

## Appendix A: Task Command Examples

```bash
# Create new task from requirement
/task create --from-requirement REQ-001 --title "Implement login"

# Start implementation
/task implement TASK-001

# Check status during work
/task status TASK-001

# Run tests
/test-verify TASK-001

# Complete and archive
/task complete TASK-001

# View board
/task board

# Search completed tasks
/task search --completed --keyword "login"
```

## Appendix B: Integration with Existing Tools

### GitHub Integration
```bash
# Create issue from task
gh issue create --title "TASK-001: Implement login" --body "$(cat docs/tasks/TASK-001.md)"

# Link PR to task
gh pr create --title "TASK-001: Implementation" --body "Closes #issue-number"
```

### VS Code Integration
- Task status in status bar
- Quick actions in command palette
- Test results in sidebar

### CI/CD Integration
- Webhook on task completion
- Automated deployment on verification
- Quality gate enforcement in pipeline

---

This comprehensive plan ensures that Claude Code's implementations are properly verified before being marked as complete, solving the critical "implemented but not working" problem while maintaining the flexibility and power of the Agentecflow system.