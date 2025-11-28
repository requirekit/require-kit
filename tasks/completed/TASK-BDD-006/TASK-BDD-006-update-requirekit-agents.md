---
id: TASK-BDD-006
title: Update RequireKit agents to discovery format
status: completed
created: 2025-11-28T15:27:39.493246+00:00
updated: 2025-11-28T20:45:00.000000+00:00
completed: 2025-11-28T20:45:00.000000+00:00
priority: high
tags: [bdd-restoration, requirekit, agents, wave1]
complexity: 4
task_type: refactoring
estimated_effort: 1-2 hours
actual_effort: 1.5 hours
wave: 1
parallel: true
implementation_method: claude-code-direct
parent_epic: bdd-restoration
repository: require-kit
completed_location: tasks/completed/TASK-BDD-006/
organized_files:
  - TASK-BDD-006-update-requirekit-agents.md
  - completion-summary.md
test_results:
  status: not_applicable
  coverage: null
  last_run: null
  notes: Refactoring task - no new code to test
---

# Task: Update RequireKit agents to discovery format

## Context

Update all RequireKit agents with GitHub-inspired format including frontmatter metadata for agent discovery and ALWAYS/NEVER/ASK boundary sections.

**Parent Epic**: BDD Mode Restoration
**Wave**: 1 (Foundation - runs in parallel, DIFFERENT REPO)
**Repository**: require-kit (NOT taskwright)
**Implementation**: Use Claude Code directly (mass refactoring)

## Description

This task is executed in the **require-kit repository**, not taskwright.

Update agents to match TaskWright's agent format:
1. Add YAML frontmatter with discovery metadata
2. Add ALWAYS/NEVER/ASK boundary sections
3. Maintain existing functionality
4. Enable discovery from TaskWright

## Acceptance Criteria

### Agents to Update

**Primary Focus**:
- [x] `bdd-generator.md` (critical for BDD mode)

**Secondary** (completed):
- [x] `requirements-analyst.md` (was requirement-formalizer.md)
- [x] `architectural-reviewer.md`
- [x] `code-reviewer.md`
- [x] `test-orchestrator.md`
- [x] `task-manager.md`
- [x] `test-verifier.md`
- [x] `.claude/agents/bdd-generator.md`

### Agent Format Template

```markdown
---
name: bdd-generator
description: Converts EARS requirements to Gherkin scenarios for BDD workflows
version: 2.0.0
stack: [cross-stack]
phase: implementation
capabilities:
  - ears-to-gherkin
  - scenario-generation
  - given-when-then
  - acceptance-criteria
  - behavior-specification
keywords:
  - bdd
  - gherkin
  - behavior-driven-development
  - ears
  - scenarios
  - feature-files
  - given-when-then
model: sonnet
author: RequireKit Team
---

# BDD Generator Agent

Converts EARS (Easy Approach to Requirements Syntax) requirements into Gherkin scenarios for Behavior-Driven Development workflows.

## Quick Start

**Invoked when**:
- Task has `--mode=bdd` flag (from TaskWright)
- Task frontmatter includes `bdd_scenarios` field
- RequireKit is installed and detected

**Input**: EARS requirement or task description with behavioral specifications
**Output**: Gherkin feature file with Given/When/Then scenarios

**Technology Stack**: Cross-stack (generates framework-specific step definitions)

## Boundaries

### ALWAYS
- ✅ Convert EARS Event-Driven to Given/When/Then scenarios (precise behavioral mapping)
- ✅ Use concrete examples in scenarios, not abstract placeholders (makes tests executable)
- ✅ Tag scenarios by priority and category (@smoke, @regression, @critical)
- ✅ Link scenarios to requirement IDs in comments (maintains traceability)
- ✅ Generate scenario outlines for data-driven test cases (DRY principle)

### NEVER
- ❌ Never create scenarios without clear acceptance criteria (leads to ambiguous tests)
- ❌ Never use implementation details in Given/When/Then steps (couples tests to code)
- ❌ Never generate more than 20 scenarios per feature (indicates poor decomposition)
- ❌ Never skip Background sections when setup is repeated (violates DRY)
- ❌ Never use database-specific terms in scenarios (breaks technology independence)

### ASK
- ⚠️ Multiple valid interpretations of requirement: Ask which behavior to prioritize
- ⚠️ Edge case handling unclear: Ask for business rule clarification before generating scenario
- ⚠️ Scenario complexity exceeds 7 steps: Ask if feature should be decomposed into smaller features

## Capabilities

### 1. EARS to Gherkin Transformation

#### Event-Driven Requirements

**EARS Format**:
```
WHEN user submits login form, system SHALL authenticate credentials
```

**Gherkin Output**:
```gherkin
Scenario: User login with valid credentials
  Given a user with email "user@example.com" and password "password123"
  When the user submits the login form
  Then the system should authenticate the credentials
  And the user should be redirected to the dashboard
```

[... rest of agent content with examples, patterns, etc ...]
```

### bdd-generator.md Specific Content

**Add these sections**:

1. **EARS Transformation Patterns**
   - Event-Driven → Scenario
   - State-Driven → Background + Scenario
   - Unwanted Behavior → Error Scenario
   - Optional Feature → Scenario Outline

2. **Gherkin Best Practices**
   - One behavior per scenario
   - Independent scenarios (no ordering dependencies)
   - Concrete examples over abstract
   - Background for common setup

3. **Framework-Specific Step Definitions**

**Python (pytest-bdd)**:
```python
from pytest_bdd import scenarios, given, when, then

scenarios('complexity_routing.feature')

@given('a task with complexity score 8')
def task_high_complexity(context):
    context.state = {"complexity_score": 8}

@when('the workflow reaches Phase 2.8')
def reach_phase_28(context):
    context.result = complexity_router(context.state)

@then('the system should invoke FULL_REQUIRED checkpoint')
def verify_full_required(context):
    assert context.result == "full_review"
```

**.NET (SpecFlow)**:
```csharp
[Given(@"a task with complexity score (.*)")]
public void GivenTaskWithComplexityScore(int score)
{
    _context.State = new TaskState { ComplexityScore = score };
}

[When(@"the workflow reaches Phase 2.8")]
public void WhenWorkflowReachesPhase28()
{
    _context.Result = ComplexityRouter.Route(_context.State);
}

[Then(@"the system should invoke FULL_REQUIRED checkpoint")]
public void ThenSystemShouldInvokeFullRequired()
{
    Assert.Equal("full_review", _context.Result);
}
```

**TypeScript (Cucumber.js)**:
```typescript
Given('a task with complexity score {int}', function(score: number) {
  this.state = { complexityScore: score };
});

When('the workflow reaches Phase 2.8', function() {
  this.result = complexityRouter(this.state);
});

Then('the system should invoke FULL_REQUIRED checkpoint', function() {
  assert.equal(this.result, 'full_review');
});
```

4. **LangGraph Integration Example**

Use the complexity routing example from the architectural review as the canonical example.

## Testing Requirements

### Verify Agent Discovery

**From TaskWright repo**:
```python
# Test that TaskWright can discover bdd-generator
from agent_discovery import discover_agent

agent = discover_agent(
    stack="cross-stack",
    phase="implementation",
    keywords=["bdd", "gherkin"]
)

assert agent.name == "bdd-generator"
assert "ears-to-gherkin" in agent.capabilities
```

### Verify Agent Invocation

**From BDD mode workflow**:
```bash
cd ~/Projects/taskwright
/task-work TASK-XXX --mode=bdd

# Should find and invoke bdd-generator from RequireKit
# Should generate correct step definitions
# Should implement to pass scenarios
```

### Verify Boundary Sections

- [x] ALWAYS section has 5-7 rules with ✅ emoji
- [x] NEVER section has 5-7 rules with ❌ emoji
- [x] ASK section has 3-5 scenarios with ⚠️ emoji
- [x] Each rule has (rationale) in parentheses
- [x] Sections placed after Quick Start, before Capabilities

## Success Criteria

- [x] bdd-generator.md has complete frontmatter
- [x] bdd-generator.md has boundary sections
- [x] All other RequireKit agents updated (8 agents total)
- [x] Agent discovery metadata ready for TaskWright
- [x] Existing RequireKit workflows unaffected (preserved documentation level handling)
- [x] Format matches TaskWright agent standards

## Implementation Notes

### Reference Agents

**TaskWright examples for format**:
- `installer/global/agents/python-api-specialist.md`
- `installer/global/agents/react-state-specialist.md`
- `installer/global/agents/dotnet-domain-specialist.md`

All have:
- YAML frontmatter with metadata
- ALWAYS/NEVER/ASK sections
- Clear capability descriptions

### Metadata Guidelines

**stack**: Technologies agent supports
- `[cross-stack]` for framework-agnostic
- `[python, typescript, dotnet]` for multi-stack
- `[python]` for single stack

**phase**: When agent is used
- `implementation` for code generation
- `review` for analysis
- `testing` for test creation

**capabilities**: What agent does (searchable)

**keywords**: Search terms for discovery

## Related Tasks

**Depends On**: None (Wave 1 parallel starter)
**Blocks**: None (enhancement, not blocker)
**Parallel With**: TASK-BDD-001, TASK-BDD-002 (different repo)
**Repository**: require-kit (IMPORTANT)

## References

- [Agent Enhancement Guide](../../../docs/guides/agent-enhancement-guide.md)
- [GitHub Agent Best Practices](../../../docs/analysis/github-agent-best-practices-analysis.md)
- [agent-content-enhancer](../../../installer/global/agents/agent-content-enhancer.md)
- TaskWright agent examples (for format)
