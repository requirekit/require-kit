# Agent Orchestration Guide

## Overview
This document defines how agents collaborate and when each specialist is engaged in the AI-Engineer system.

## Automatic Agent Selection

### File-Based Routing
```yaml
routing_rules:
  "*.py":
    primary: python-api-specialist
    testing: python-testing-specialist
    langchain: python-langchain-specialist
    review: code-reviewer
    
  "*.tsx, *.ts":
    primary: react-component-specialist
    state: react-state-specialist
    testing: react-testing-specialist
    review: code-reviewer
    
  "*.cs":
    primary: dotnet-api-specialist
    domain: dotnet-domain-specialist
    testing: dotnet-testing-specialist
    review: code-reviewer
    
  "*.xaml":
    primary: maui-ui-specialist
    viewmodel: maui-viewmodel-specialist
    usecase: maui-usecase-specialist
    testing: qa-tester
    review: code-reviewer
    
  "Dockerfile, docker-compose.yml":
    primary: devops-specialist
    review: security-specialist
    
  "*.sql":
    primary: database-specialist
    review: code-reviewer
    
  ".github/workflows/*.yml":
    primary: devops-specialist
    review: code-reviewer
```

### Task-Based Routing
```yaml
task_routing:
  new_feature:
    sequence:
      - requirements-analyst
      - software-architect
      - "{stack}-specialist"
      - "{stack}-testing-specialist"
      - qa-tester
      - code-reviewer
      
  bug_fix:
    sequence:
      - qa-tester  # Reproduce issue
      - "{stack}-specialist"  # Fix implementation
      - "{stack}-testing-specialist"  # Add regression test
      - code-reviewer
      
  performance_issue:
    sequence:
      - software-architect  # Analyze bottlenecks
      - "{stack}-specialist"  # Optimize code
      - devops-specialist  # Infrastructure optimization
      - qa-tester  # Performance testing
      
  security_audit:
    sequence:
      - security-specialist  # Identify vulnerabilities
      - "{stack}-specialist"  # Implement fixes
      - qa-tester  # Security testing
      - code-reviewer
      
  database_optimization:
    sequence:
      - database-specialist  # Query analysis
      - "{stack}-specialist"  # Code optimization
      - qa-tester  # Performance validation
      
  api_development:
    sequence:
      - requirements-analyst
      - software-architect
      - "{api}-specialist"  # python-api or dotnet-api
      - "{testing}-specialist"
      - qa-tester
      
  ai_workflow:
    sequence:
      - requirements-analyst
      - python-langchain-specialist
      - python-testing-specialist
      - qa-tester
```

## Collaboration Patterns

### Sequential Pattern
Agents work in sequence, each completing their task before the next begins.
```
Requirements → Architecture → Implementation → Testing → Review
```

### Parallel Pattern
Multiple agents work simultaneously on different aspects.
```
Frontend Specialist ─┐
Backend Specialist  ─┼→ Integration → Testing
Database Specialist ─┘
```

### Hierarchical Pattern
Lead agent coordinates multiple sub-agents.
```
Software Architect
    ├── Frontend Specialist
    ├── Backend Specialist
    └── Database Specialist
```

### Review Pattern
All work is reviewed by appropriate specialists.
```
Implementation → Testing → Security Review → Code Review → Approval
```

## Context Sharing

### Shared Documents
Agents share context through:
1. **Requirements**: `docs/requirements/*.md`
2. **Architecture**: `docs/adr/*.md`
3. **BDD Scenarios**: `docs/bdd/features/*.feature`
4. **State Tracking**: `docs/state/*.md`
5. **Task Context**: `tasks/{task-id}/*.md`

### Handoff Protocol
When an agent completes their work:
```markdown
## Handoff to: {next-agent}

### Completed:
- [List of completed items]

### Context:
- [Relevant decisions made]
- [Key implementation details]

### Next Steps:
- [What the next agent should do]

### Concerns:
- [Any issues or considerations]
```

## Quality Gates

### Entry Criteria
Before an agent begins work:
- Previous agent's work is complete
- Context is documented
- Requirements are clear
- Dependencies are resolved

### Exit Criteria
Before an agent hands off:
- Code passes linting
- Tests are written and passing
- Documentation is updated
- Security checks pass
- Performance benchmarks met

### Gate Definitions
```yaml
quality_gates:
  code_quality:
    linting: pass
    complexity: <10
    duplication: <5%
    
  testing:
    unit_coverage: >=80%
    integration_tests: pass
    e2e_tests: pass
    
  security:
    vulnerability_scan: pass
    dependency_audit: pass
    secrets_scan: pass
    
  performance:
    response_time: <200ms
    memory_usage: <100MB
    cpu_usage: <70%
    
  documentation:
    api_docs: complete
    code_comments: adequate
    readme_updated: true
```

## Agent Communication

### Direct Communication
Agents can directly communicate for clarification:
```markdown
@{agent-name}: [Question or request]
```

### Broadcast Communication
For team-wide updates:
```markdown
@all-agents: [Important update or decision]
```

### Escalation
When an agent needs help:
```markdown
@software-architect: Need architectural guidance on [topic]
@security-specialist: Security review needed for [component]
```

## Conflict Resolution

### Technical Conflicts
When agents disagree on technical approach:
1. Document both approaches
2. Escalate to `software-architect`
3. Decision recorded in ADR
4. All agents follow decision

### Priority Conflicts
When multiple tasks compete:
1. Check task priority in backlog
2. Consult `task-manager`
3. Follow sprint goals
4. Document decision

## Performance Monitoring

### Agent Metrics
Track for each agent:
- Task completion time
- Code quality metrics
- Test coverage achieved
- Documentation completeness
- Handoff efficiency

### System Metrics
Track overall:
- End-to-end task time
- Quality gate pass rate
- Rework frequency
- Agent utilization
- Context preservation

## Continuous Improvement

### Retrospectives
After each sprint:
1. Review agent performance
2. Identify bottlenecks
3. Update routing rules
4. Refine handoff protocols
5. Improve context sharing

### Agent Evolution
- Update agent prompts based on learnings
- Add new specialists as needed
- Refine collaboration patterns
- Optimize routing rules
- Enhance quality gates

## Quick Reference

### Common Scenarios

#### Starting a New Feature
```
1. @requirements-analyst - Gather and formalize requirements
2. @software-architect - Design solution
3. @{stack}-specialist - Implement
4. @qa-tester - Test
5. @code-reviewer - Review
```

#### Fixing a Bug
```
1. @qa-tester - Reproduce and document
2. @{stack}-specialist - Fix
3. @{stack}-testing-specialist - Add regression test
4. @code-reviewer - Verify fix
```

#### Performance Optimization
```
1. @software-architect - Profile and analyze
2. @{stack}-specialist - Optimize code
3. @database-specialist - Optimize queries
4. @devops-specialist - Infrastructure tuning
5. @qa-tester - Validate improvements
```

#### Security Issue
```
1. @security-specialist - Assess vulnerability
2. @{stack}-specialist - Implement fix
3. @security-specialist - Verify fix
4. @qa-tester - Security testing
```

## Integration with Commands

### Task Commands
- `/task-create` - Automatically assigns initial agent
- `/task-work` - Engages appropriate specialists
- `/task-test` - Activates testing specialists
- `/task-review` - Triggers review agents
- `/task-complete` - Validates all quality gates

### Direct Agent Commands
- `@agent-name` - Directly engage specific agent
- `@all-agents` - Broadcast to all agents
- `@stack-specialists` - Engage all stack specialists
- `@testing-team` - Engage all testing specialists
