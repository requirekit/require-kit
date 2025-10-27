# Model Assignment Matrix - Quick Reference

**Last Updated**: 2025-10-17
**Total Agents**: 17 (11 Sonnet, 5 Haiku, 1 delegates to stack-specific)

## Quick Lookup Table

| Agent | Model | Category | Primary Use Case |
|-------|-------|----------|------------------|
| architectural-reviewer | sonnet | Reasoning | SOLID/DRY/YAGNI analysis before implementation |
| bdd-generator | haiku | Execution | Gherkin scenario generation from EARS |
| build-validator | haiku | Execution | Code compilation and dependency validation |
| code-reviewer | sonnet | Reasoning | Code quality and compliance review |
| complexity-evaluator | sonnet | Reasoning | Implementation complexity scoring and routing |
| database-specialist | sonnet | Reasoning | Data architecture and optimization |
| debugging-specialist | sonnet | Reasoning | Root cause analysis and bug fixing |
| devops-specialist | sonnet | Reasoning | Infrastructure and deployment strategy |
| figma-react-orchestrator | sonnet | Orchestration | 6-phase Figma-to-React workflow |
| pattern-advisor | sonnet | Reasoning | Design pattern recommendation |
| python-mcp-specialist | sonnet | Reasoning | MCP server development expertise |
| requirements-analyst | haiku | Execution | EARS notation extraction |
| security-specialist | sonnet | Reasoning | Security and threat analysis |
| task-manager | sonnet | Orchestration | Task workflow coordination |
| test-orchestrator | haiku | Execution | Test coordination and execution |
| test-verifier | haiku | Execution | Test result parsing and quality gates |
| zeplin-maui-orchestrator | sonnet | Orchestration | 6-phase Zeplin-to-MAUI workflow |

## Model Distribution

```
Sonnet (Complex Reasoning):  11 agents (64.7%)
Haiku (Execution/Templates):  5 agents (29.4%)
Stack-Specific:                1 agent  (5.9%)
```

## Decision Tree for Model Selection

### Use Sonnet When:
- ✅ Complex architectural decisions required
- ✅ Multi-factor trade-off analysis needed
- ✅ Security/compliance evaluation
- ✅ Deep reasoning about system behavior
- ✅ Workflow orchestration with decision logic
- ✅ Pattern matching requires context understanding

### Use Haiku When:
- ✅ Template-based generation (EARS, Gherkin)
- ✅ Deterministic parsing (test results, build errors)
- ✅ High-volume execution tasks
- ✅ Structured data transformation
- ✅ Clear success/failure criteria
- ✅ Speed is more critical than deep analysis

## Agent Categories

### Reasoning Agents (Sonnet)

**Architectural Quality** (3 agents):
- architectural-reviewer
- pattern-advisor
- complexity-evaluator

**Code Quality** (2 agents):
- code-reviewer
- debugging-specialist

**Specialized Expertise** (4 agents):
- security-specialist
- database-specialist
- devops-specialist
- python-mcp-specialist

**Workflow Orchestration** (2 agents):
- task-manager
- figma-react-orchestrator / zeplin-maui-orchestrator

### Execution Agents (Haiku)

**Requirements & Testing** (4 agents):
- requirements-analyst
- bdd-generator
- test-verifier
- test-orchestrator

**Build & Validation** (1 agent):
- build-validator

## Cost Impact

| Configuration | Cost per Task | Annual Cost (1000 tasks) |
|--------------|---------------|-------------------------|
| All Sonnet | $0.45 | $450 |
| Optimized Mix | $0.30 | $300 |
| Savings | **33%** | **$150** |

## Performance Impact

| Agent | Model | Speed vs Sonnet |
|-------|-------|----------------|
| requirements-analyst | haiku | 3x faster |
| bdd-generator | haiku | 4x faster |
| build-validator | haiku | 5x faster |
| test-verifier | haiku | 3x faster |
| test-orchestrator | haiku | 3x faster |

**Net task completion improvement**: 20-30% faster

## When to Change Model Assignment

### Upgrade to Sonnet
- Quality issues detected in output
- Edge cases not handled properly
- Additional reasoning needed for context

### Downgrade to Haiku
- Cost pressure with acceptable quality
- Task is highly repetitive
- Strong validation mechanisms in place
- Speed more critical than nuanced analysis

## Related Documentation

- **Comprehensive Guide**: `docs/guides/model-optimization-guide.md` (400+ lines)
- **Implementation Summary**: `TASK-017-IMPLEMENTATION-SUMMARY.md`
- **Agent Files**: `installer/global/agents/*.md`

## Maintenance

### How to Update Agent Model

```bash
# 1. Edit agent frontmatter
vim installer/global/agents/[agent-name].md

# 2. Change model field
model: sonnet  # or haiku

# 3. Update rationale
model_rationale: "Clear reasoning for change"

# 4. Commit changes
git add installer/global/agents/[agent-name].md
git commit -m "Update [agent-name] to use [model]"
```

### Rollback if Needed

```bash
# Revert specific agent
git checkout HEAD -- installer/global/agents/[agent-name].md

# Revert all agents
git checkout HEAD -- installer/global/agents/*.md
```

---

**For detailed information, see**: `docs/guides/model-optimization-guide.md`
