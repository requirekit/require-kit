---
id: TASK-001C
title: "Transfer Core Agents"
created: 2025-10-19
status: backlog
priority: high
complexity: 4
parent_task: TASK-001
subtasks: []
estimated_hours: 2
---

# TASK-001C: Transfer Core Agents

## Description

Copy core AI agents from ai-engineer to agentecflow, removing references to requirements/BDD in agent prompts.

## Files to Transfer

### ✅ INCLUDE (15 agents)

```bash
# Quality Gate Agents (CRITICAL)
architectural-reviewer.md     # Phase 2.5
test-verifier.md             # Phase 4.5
test-orchestrator.md         # Phase 4.5 support
code-reviewer.md             # Phase 5
task-manager.md              # Core orchestration
complexity-evaluator.md      # Phase 2.7
build-validator.md           # Quality gates

# Supporting Agents
debugging-specialist.md
devops-specialist.md
database-specialist.md
security-specialist.md
pattern-advisor.md
python-mcp-specialist.md
figma-react-orchestrator.md
zeplin-maui-orchestrator.md
```

### ❌ EXCLUDE (2 agents)

```bash
requirements-analyst.md  # Requirements management
bdd-generator.md         # BDD scenarios
```

## Modifications Required

### For ALL Agents

**Remove references to**:
- EARS requirements
- BDD scenarios
- Epic/feature context
- Requirements traceability

**Update task context sections** from:
```
Load task requirements from docs/requirements/
Load BDD scenarios from docs/bdd/
Check epic/feature context
```

To:
```
Load task description and acceptance criteria
Load parent task context if subtask
Identify technology stack
```

## Implementation

```bash
cd ai-engineer/installer/global/agents

# Copy all agents EXCEPT requirements-analyst and bdd-generator
for agent in architectural-reviewer.md test-verifier.md test-orchestrator.md \
             code-reviewer.md task-manager.md complexity-evaluator.md \
             build-validator.md debugging-specialist.md devops-specialist.md \
             database-specialist.md security-specialist.md pattern-advisor.md \
             python-mcp-specialist.md figma-react-orchestrator.md \
             zeplin-maui-orchestrator.md; do
  cp "$agent" ../../agentecflow/installer/global/agents/
done
```

## Verification

```bash
cd agentecflow/installer/global/agents/

# Verify no requirements references
grep -i "requirements\|ears\|bdd.*scenario" *.md | \
  grep -v "# Historical" | grep -v "acceptance criteria"

# Should return EMPTY or only acceptable references like:
# - "acceptance criteria" (OK)
# - "functional requirements" in general discussion (OK)
# - "Historical note: ..." (OK)

# Count agents
ls -1 *.md | wc -l
# Expected: 15
```

## Acceptance Criteria

- [ ] 15 agents copied
- [ ] 0 references to EARS notation
- [ ] 0 references to BDD scenarios (except in mode=bdd context)
- [ ] 0 references to epic/feature context
- [ ] All agents reference task description instead of requirements
- [ ] Validation tests pass

## Estimated Time

2 hours
