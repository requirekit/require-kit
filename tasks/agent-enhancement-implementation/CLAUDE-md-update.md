# Updated CLAUDE.md Section for Agent Orchestration

Add this section to your existing `.claude/CLAUDE.md` file:

## Agent Orchestration Strategy

This project uses specialized agents for different aspects of development. The system automatically selects the appropriate agent based on the task type and files being modified.

**Reference**: `.claude/methodology/05-agent-orchestration.md` for complete orchestration patterns.

### Available Specialists

#### Stack-Specific Agents

**Python Stack**
- `@python-api-specialist` - FastAPI/Flask APIs, async patterns, validation
- `@python-langchain-specialist` - LangChain/LangGraph, RAG, AI workflows
- `@python-testing-specialist` - pytest, mocking, async testing

**React Stack**
- `@react-component-specialist` - Components, hooks, performance
- `@react-state-specialist` - State management, Context, Zustand, Redux
- `@react-testing-specialist` - RTL, Jest, Playwright, visual regression

**.NET Microservice Stack**
- `@dotnet-api-specialist` - FastEndpoints, Either monad, functional patterns
- `@dotnet-domain-specialist` - DDD, aggregates, value objects
- `@dotnet-testing-specialist` - xUnit, WebApplicationFactory, TDD

**MAUI Stack**
- `@maui-usecase-specialist` - UseCase pattern, business logic
- `@maui-viewmodel-specialist` - MVVM, data binding, commands
- `@maui-ui-specialist` - XAML, layouts, platform-specific UI

#### Global Specialists
- `@requirements-analyst` - EARS notation, requirements gathering
- `@software-architect` - System design, patterns, decisions
- `@qa-tester` - Test strategies, quality assurance
- `@code-reviewer` - Code quality, standards enforcement
- `@devops-specialist` - CI/CD, containers, deployment
- `@security-specialist` - Security audits, OWASP compliance
- `@database-specialist` - Schema design, optimization

### Automatic Agent Selection Rules

The system automatically engages agents based on:

#### File Type
- `*.py` → Python specialists
- `*.tsx, *.ts` → React specialists
- `*.cs` → .NET specialists
- `*.xaml` → MAUI specialists
- `Dockerfile` → DevOps specialist
- `*.sql` → Database specialist

#### Task Type
- New feature → Requirements → Architecture → Implementation → Testing → Review
- Bug fix → QA → Implementation → Testing → Review
- Performance → Architecture → Implementation → DevOps → Testing
- Security → Security audit → Implementation → Testing → Review

### How to Work with Agents

1. **Let the system auto-select** - The orchestration system will choose appropriate agents
2. **Direct engagement** - Use `@agent-name` to engage specific agents
3. **Follow handoff protocols** - Agents will hand off work with context
4. **Review quality gates** - Each agent ensures quality before handoff

### Quality Standards

All agents enforce:
- Code quality (linting, complexity, duplication)
- Test coverage (≥80% for critical code)
- Documentation (API docs, comments, README updates)
- Security (vulnerability scanning, dependency audits)
- Performance (response time, resource usage)

### Example Workflows

#### Implementing a New API Endpoint
```
1. @requirements-analyst - Define endpoint requirements
2. @software-architect - Design API structure
3. @python-api-specialist - Implement endpoint
4. @python-testing-specialist - Write tests
5. @qa-tester - Integration testing
6. @code-reviewer - Final review
```

#### Fixing a React Component Bug
```
1. @qa-tester - Reproduce issue
2. @react-component-specialist - Fix component
3. @react-testing-specialist - Add regression test
4. @code-reviewer - Verify fix
```

#### Adding LangChain Workflow
```
1. @requirements-analyst - Define workflow requirements
2. @python-langchain-specialist - Implement workflow
3. @python-testing-specialist - Test workflow
4. @qa-tester - End-to-end testing
```

### Context Preservation

Agents maintain context through:
- Shared documents in `docs/` directories
- Code comments and documentation
- Handoff notes between agents
- Architecture decision records (ADRs)
- Task-specific context in `tasks/` directory

Remember: The orchestration system ensures the right expert handles each aspect of development, maintaining quality and consistency throughout the project.
