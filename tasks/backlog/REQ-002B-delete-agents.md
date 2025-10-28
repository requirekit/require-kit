---
id: REQ-002B
title: "Delete Execution Agents"
created: 2025-10-27
status: backlog
priority: high
complexity: 3
parent_task: REQ-002
subtasks: []
estimated_hours: 0.5
---

# REQ-002B: Delete Execution Agents

## Description

Delete all task execution, quality gate, and stack-specific agents from `installer/global/agents/`, keeping ONLY requirements management agents.

## Agents to DELETE

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/global/agents/

# Quality gate agents
rm -f architectural-reviewer.md
rm -f test-verifier.md
rm -f test-orchestrator.md
rm -f code-reviewer.md
rm -f build-validator.md
rm -f complexity-evaluator.md

# Task execution
rm -f task-manager.md

# Stack-specific specialists
rm -f debugging-specialist.md
rm -f devops-specialist.md
rm -f database-specialist.md
rm -f security-specialist.md
rm -f pattern-advisor.md
rm -f python-mcp-specialist.md

# UX integration
rm -f figma-react-orchestrator.md
rm -f zeplin-maui-orchestrator.md
```

## Agents to KEEP

```bash
# Requirements management
✅ requirements-analyst.md
✅ bdd-generator.md
```

## Implementation

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/global/agents/

# Delete quality gate agents
rm -f architectural-reviewer.md test-verifier.md test-orchestrator.md code-reviewer.md build-validator.md complexity-evaluator.md

# Delete task execution
rm -f task-manager.md

# Delete stack specialists
rm -f debugging-specialist.md devops-specialist.md database-specialist.md security-specialist.md pattern-advisor.md python-mcp-specialist.md

# Delete UX integration
rm -f figma-react-orchestrator.md zeplin-maui-orchestrator.md

# List remaining agents
echo "Remaining agents:"
ls -1 *.md
```

## Verification

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/global/agents/

# Count remaining agents
ls -1 *.md | wc -l
# Expected: 2 (requirements-analyst, bdd-generator)

# Verify only requirements agents remain
ls -1
# Should show ONLY:
# - requirements-analyst.md
# - bdd-generator.md

# Verify no quality gate agents
ls -1 | grep -E "reviewer|verifier|validator|evaluator|manager"
# Should return EMPTY
```

## Acceptance Criteria

- [ ] 15 execution agents deleted
- [ ] 2 requirements agents remain
- [ ] Only requirements-analyst.md and bdd-generator.md exist
- [ ] No quality gate agents
- [ ] No stack-specific agents
- [ ] No UX integration agents
- [ ] Verification tests pass

## Estimated Time

0.5 hours

## Notes

- Straightforward deletion task
- Keep ONLY requirements-analyst and bdd-generator
- Everything else gets deleted
- Commit after verification
