---
id: REQ-001C
title: "Extract Requirements Agents"
created: 2025-10-27
status: backlog
priority: high
complexity: 3
parent_task: REQ-001
subtasks: []
estimated_hours: 1
---

# REQ-001C: Extract Requirements Agents

## Description

Extract requirements-focused AI agents from ai-engineer to require-kit.

## Agents to Extract

### Core Requirements Agents

```bash
✅ requirements-analyst.md    # EARS notation expert
✅ bdd-generator.md          # BDD/Gherkin scenario expert
```

## Agents to Exclude

```bash
❌ architectural-reviewer.md     # Implementation quality
❌ test-verifier.md             # Test execution
❌ test-orchestrator.md         # Test execution
❌ code-reviewer.md             # Code review
❌ task-manager.md              # Task execution
❌ complexity-evaluator.md      # Implementation planning
❌ build-validator.md           # Compilation
❌ debugging-specialist.md      # Debugging
❌ devops-specialist.md         # Infrastructure
❌ database-specialist.md       # Database
❌ security-specialist.md       # Security
❌ pattern-advisor.md           # Design patterns
❌ All stack-specific agents
❌ All UX integration agents
```

## Modifications Required

### requirements-analyst.md

**Keep**:
- EARS notation patterns
- Requirements gathering techniques
- Requirement validation
- Traceability logic

**Remove**:
- References to task implementation
- References to quality gates
- References to test execution

### bdd-generator.md

**Keep**:
- Gherkin scenario generation
- Given/When/Then formatting
- Scenario validation
- Requirements traceability

**Remove**:
- References to test execution
- References to task-work integration
- References to implementation validation

## Implementation Steps

```bash
cd /path/to/ai-engineer/installer/global/agents

# Copy requirements agents
cp requirements-analyst.md /path/to/require-kit/requirements/agents/
cp bdd-generator.md /path/to/require-kit/requirements/agents/
```

### Edit Agents

```bash
cd /path/to/require-kit/requirements/agents/

# Edit requirements-analyst.md
# Remove:
# - Task implementation references
# - Quality gate references
# - Test execution references

# Edit bdd-generator.md
# Remove:
# - Test execution references
# - Task-work integration
# - Implementation validation

# Verify
grep -ri "task-work\|implementation\|quality.*gate\|test.*execution" *.md | \
  grep -v "# Historical"
# Should be EMPTY
```

## Verification

```bash
cd /path/to/require-kit/requirements/agents/

# Count agents
ls -1 *.md | wc -l
# Expected: 2

# Check no implementation references
grep -ri "implementation\|task.*work\|quality.*gate" *.md | \
  grep -v "# Historical" | grep -v "requirements implementation"
# Should be EMPTY or only "requirements implementation" context
```

## Acceptance Criteria

- [ ] 2 agents extracted
- [ ] requirements-analyst.md: Pure requirements focus
- [ ] bdd-generator.md: Pure scenario generation focus
- [ ] No references to task execution
- [ ] No references to implementation quality
- [ ] No references to test execution
- [ ] Agents focus exclusively on requirements management

## Estimated Time

1 hour

## Notes

- Only 2 agents needed for requirements management
- Keep agents focused on requirements gathering/formalization
- Remove all implementation/execution references
- Agents should be usable without Agentecflow
