# Task Command Updates for Agent Orchestration

## Updated task-work.md

Add this section to `.claude/commands/task-work.md`:

```markdown
## Automatic Agent Selection

When working on a task, the system automatically engages appropriate specialists based on:
1. File types being modified
2. Task type and context
3. Current workflow phase

Consult `.claude/methodology/05-agent-orchestration.md` for complete routing rules.

### Quick Agent Reference

#### By Technology Stack
- 🐍 **Python**: @python-api-specialist, @python-langchain-specialist, @python-testing-specialist
- ⚛️ **React**: @react-component-specialist, @react-state-specialist, @react-testing-specialist
- 🔷 **.NET**: @dotnet-api-specialist, @dotnet-domain-specialist, @dotnet-testing-specialist
- 📱 **MAUI**: @maui-usecase-specialist, @maui-viewmodel-specialist, @maui-ui-specialist

#### By Responsibility
- 📝 **Requirements**: @requirements-analyst
- 🏗️ **Architecture**: @software-architect
- 🧪 **Testing**: @qa-tester, {stack}-testing-specialist
- 🔒 **Security**: @security-specialist
- 🚀 **DevOps**: @devops-specialist
- 💾 **Database**: @database-specialist
- 🔍 **Review**: @code-reviewer

### Workflow Patterns

#### New Feature Implementation
1. @requirements-analyst → Gather and formalize requirements
2. @software-architect → Design solution architecture
3. @{stack}-specialist → Implement feature
4. @{stack}-testing-specialist → Write tests
5. @qa-tester → Integration testing
6. @code-reviewer → Final review

#### Bug Fix
1. @qa-tester → Reproduce and document issue
2. @{stack}-specialist → Implement fix
3. @{stack}-testing-specialist → Add regression test
4. @code-reviewer → Verify fix

#### Performance Optimization
1. @software-architect → Analyze bottlenecks
2. @{stack}-specialist → Optimize code
3. @database-specialist → Optimize queries (if applicable)
4. @devops-specialist → Infrastructure tuning
5. @qa-tester → Performance validation

### Agent Handoff Protocol

When an agent completes their work, they provide:
- **Completed**: List of completed items
- **Context**: Key decisions and implementation details
- **Next Steps**: What the next agent should do
- **Concerns**: Any issues or considerations

### Quality Gates

Each agent ensures:
- ✅ Code passes linting
- ✅ Tests are written and passing
- ✅ Documentation is updated
- ✅ Security checks pass
- ✅ Performance benchmarks met

### Direct Agent Engagement

To engage a specific agent directly:
```
@agent-name: [Your request or question]
```

To broadcast to all relevant agents:
```
@all-agents: [Important update or decision]
```

To request specialist help:
```
@software-architect: Need guidance on [architectural decision]
@security-specialist: Please review [security concern]
```
```

## Updated task-create.md

Add to `.claude/commands/task-create.md`:

```markdown
## Agent Assignment

When creating a task, the system automatically assigns appropriate agents based on:

### Task Type Detection
- **Feature**: requirements-analyst → software-architect → specialists
- **Bug**: qa-tester → specialists
- **Performance**: software-architect → specialists → devops-specialist
- **Security**: security-specialist → specialists
- **Refactor**: software-architect → specialists

### Stack Detection
The system detects the stack from:
- File extensions in the task scope
- Project configuration
- Explicit stack specification

### Initial Agent Assignment
Based on task type and stack:
- The first agent is automatically engaged
- Subsequent agents are queued in sequence
- Manual override is possible with @agent-name

Example:
```
Task: Add user authentication
Type: Feature
Stack: Python
Assigned: @requirements-analyst → @software-architect → @python-api-specialist → @python-testing-specialist → @qa-tester → @code-reviewer
```
```

## Updated task-test.md

Add to `.claude/commands/task-test.md`:

```markdown
## Testing Specialist Engagement

When executing tests, the appropriate testing specialists are automatically engaged:

### By Stack
- **Python**: @python-testing-specialist (pytest, async, mocking)
- **React**: @react-testing-specialist (RTL, Jest, Playwright)
- **.NET**: @dotnet-testing-specialist (xUnit, WebApplicationFactory)
- **MAUI**: @qa-tester (UI testing, integration)

### By Test Type
- **Unit Tests**: {stack}-testing-specialist
- **Integration Tests**: @qa-tester + {stack}-testing-specialist
- **E2E Tests**: @qa-tester
- **Performance Tests**: @qa-tester + @devops-specialist
- **Security Tests**: @security-specialist + @qa-tester

### Test Coverage Requirements
Each specialist ensures:
- Unit test coverage ≥ 80%
- Critical paths have integration tests
- Regression tests for bug fixes
- Performance benchmarks for optimizations
- Security tests for sensitive features

### Testing Workflow
1. **Test Planning**: Specialist creates test plan
2. **Test Implementation**: Write comprehensive tests
3. **Test Execution**: Run and validate tests
4. **Coverage Analysis**: Ensure coverage goals
5. **Test Review**: Review test quality
```

## Updated task-complete.md

Add to `.claude/commands/task-complete.md`:

```markdown
## Completion Validation

Before marking a task complete, all assigned agents must verify:

### Quality Gate Checklist
- [ ] **Requirements**: All requirements addressed (@requirements-analyst)
- [ ] **Architecture**: Design decisions documented (@software-architect)
- [ ] **Implementation**: Code complete and functional (@{stack}-specialist)
- [ ] **Testing**: Tests passing with coverage (@{stack}-testing-specialist)
- [ ] **Quality**: Code review complete (@code-reviewer)
- [ ] **Security**: Security checks passed (@security-specialist)
- [ ] **Documentation**: All docs updated (all agents)

### Agent Sign-offs
Each agent provides explicit sign-off:
```
@requirements-analyst: ✅ Requirements fulfilled
@software-architect: ✅ Architecture sound
@python-api-specialist: ✅ Implementation complete
@python-testing-specialist: ✅ Tests comprehensive
@qa-tester: ✅ Quality assured
@code-reviewer: ✅ Code approved
```

### Final Validation
The task-manager ensures:
- All quality gates passed
- All agents have signed off
- Documentation is complete
- State tracking is updated
```
