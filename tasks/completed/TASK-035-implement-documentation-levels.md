---
id: TASK-035
title: Implement Documentation Levels for task-work Command (RequireKit)
status: completed
created: 2025-10-29T12:00:00Z
updated: 2025-11-02T19:30:00Z
completed: 2025-11-02T19:30:00Z
priority: high
complexity: 5
estimated_time: 2-3 hours
actual_time: 1 hour
tags: [performance, optimization, documentation, task-work, user-experience, require-kit]
epic: null
feature: null
parent_task: null
related_tasks:
  - TASK-036 (ai-engineer) - Proven implementation pattern
requirements: []
bdd_scenarios: []
test_results:
  status: passed
  coverage: 100
  last_run: 2025-11-02T19:30:00Z
  notes: "Implementation verified - all 7 agents updated, configuration complete"
---

# Task: Implement Documentation Levels for task-work Command

## Overview

Implement a 3-tier documentation system (Minimal, Standard, Comprehensive) for the `/task-work` command to reduce task execution time by 50-78% while maintaining 100% quality gates and agent collaboration.

**Note**: This task implements TASK-035 for the **RequireKit** repository. RequireKit will be split from ai-engineer and needs its own installer with updated agents.

## ✅ PROVEN PATTERN AVAILABLE (TASK-036)

**CRITICAL UPDATE (2025-10-30)**: The implementation pattern has been **proven and tested** in TASK-036 (ai-engineer):

✅ **TASK-036 Complete** (`/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/tasks/in_review/TASK-036-fix-minimal-docs-mode-enforcement.md`):
- **Implementation**: 3 agents updated with "Documentation Level Handling" guard clauses
- **Test Results**: 16/16 tests passed (100%)
- **Code Quality**: 8.5/10 (Excellent)
- **Architectural Review**: 88/100 (Auto-approved)
- **Zero Scope Creep**: Perfect plan adherence
- **Pattern Location**: `.claude/agents/requirements-analyst.md`, `bdd-generator.md`, `test-orchestrator.md`

**Key Pattern Elements**:
1. Guard clause section with CRITICAL marker
2. Mode-specific behavior definitions (minimal/standard/comprehensive)
3. Quality gate preservation statements
4. Token reduction targets (60-75%)

**Implementation Time Reduction**: Estimated time reduced from 4-5 hours to **2-3 hours** due to proven pattern.

## Context from ai-engineer Implementation

The core documentation levels infrastructure has **already been implemented** in the ai-engineer repository:

✅ **Global Infrastructure Complete (in ai-engineer)**:
- Configuration system (`.claude/settings.json` schema - 89 lines)
- Command specification updates (`task-work.md` - 450+ lines added)
- Context parameter format specification (`context-parameter-format.md` - 292 lines)
- 4 core global agents updated (requirements-analyst, architectural-reviewer, test-orchestrator, code-reviewer)
- Documentation templates created (minimal-summary, comprehensive-checklist)
- User guide created (`documentation-levels-guide.md` - 439 lines)
- Comprehensive test suite (58 tests, 100% pass rate)
- **TASK-036**: Minimal docs enforcement fix (proven pattern)

**Reference**: See `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/docs/requirements/TASK-035-FINAL-IMPLEMENTATION-SUMMARY.md`

## Scope for This Task

Task Wright will be split from ai-engineer and will have its own **installer** that installs global agents. This task updates those agents in RequireKit's installer.

### What's Already Done (in ai-engineer only)
- ✅ Configuration schema defined
- ✅ Command specifications updated
- ✅ Context parameter format specified
- ✅ Templates created
- ✅ Tests written and passing
- ✅ User documentation complete
- ✅ 4 core agents updated in ai-engineer/installer/global/agents/

### What Needs to be Done (in RequireKit)
1. **Update 7 global agents** in `installer/global/agents/` with documentation level awareness
2. **Update template settings.json** with complete documentation configuration (89 lines)
3. **Create implementation summary** documenting changes

## RequireKit Global Agents to Update (7 agents)

These agents are in `installer/global/agents/` and will be installed globally by RequireKit's installer:

1. **requirements-analyst.md** (~80 lines to add)
   - Phase: 1 (Requirements analysis)
   - Focus: EARS notation requirements
   - Output modes: Minimal (skip EARS docs), Standard (inline requirements), Comprehensive (standalone EARS doc)
   - **CRITICAL**: Must be updated (Phase 1 of task-work)

2. **architectural-reviewer.md** (~75 lines to add)
   - Phase: 2.5B (Architectural review)
   - Focus: SOLID/DRY/YAGNI scoring, design pattern recommendations
   - Output modes: Minimal (JSON scores), Standard (embedded summary), Comprehensive (standalone architecture guide)
   - **CRITICAL**: Must be updated (Phase 2.5B of task-work)

3. **test-orchestrator.md** (~145 lines to add)
   - Phase: 4 (Test orchestration)
   - Focus: Build verification, test execution, coverage enforcement
   - Output modes: Minimal (JSON), Standard (full report), Comprehensive (enhanced + supporting docs)
   - **CRITICAL**: Must be updated (Phase 4 of task-work)

4. **code-reviewer.md** (~95 lines to add)
   - Phase: 5 (Code review)
   - Focus: Quality scoring, findings reporting, Plan Audit (Phase 5.5)
   - Output modes: Minimal (JSON), Standard (markdown report), Comprehensive (detailed report + supporting docs)
   - **CRITICAL**: Must be updated (Phase 5 of task-work)

5. **task-manager.md** (~70 lines to add)
   - Phase: Orchestration
   - Focus: Workflow coordination, state management, passing documentation_level to sub-agents
   - Output modes: Coordinates summary generation based on mode
   - **CRITICAL**: Must be updated (orchestrates all phases)

6. **bdd-generator.md** (~80 lines to add)
   - Phase: 1.5 (BDD scenario generation)
   - Focus: EARS → BDD/Gherkin conversion
   - Output modes: Minimal (skip unless BDD mode), Standard (inline scenarios), Comprehensive (standalone + supporting docs)
   - **IMPORTANT**: Update for BDD mode support

7. **test-verifier.md** (~120 lines to add)
   - Phase: 4.5 (Test enforcement)
   - Focus: Test verification, auto-fix loop
   - Output modes: Minimal (pass/fail), Standard (detailed results), Comprehensive (enhanced + failure analysis)
   - **IMPORTANT**: Update for Phase 4.5 test enforcement

**Total**: ~665 lines across 7 agents

**Other agents in installer** (don't need updates - not part of task-work workflow):
- build-validator.md
- complexity-evaluator.md
- database-specialist.md
- debugging-specialist.md
- devops-specialist.md
- figma-react-orchestrator.md
- pattern-advisor.md
- python-mcp-specialist.md
- security-specialist.md
- zeplin-maui-orchestrator.md

## Acceptance Criteria

### AC1: Global Agent Updates (7/7 agents)

Update agents in `installer/global/agents/`:

- [ ] Update `requirements-analyst.md` with documentation level awareness (~80 lines)
- [ ] Update `architectural-reviewer.md` with documentation level awareness (~75 lines)
- [ ] Update `test-orchestrator.md` with documentation level awareness (~145 lines)
- [ ] Update `code-reviewer.md` with documentation level awareness (~95 lines)
- [ ] Update `task-manager.md` with documentation level awareness (~70 lines)
- [ ] Update `bdd-generator.md` with documentation level awareness (~80 lines)
- [ ] Update `test-verifier.md` with documentation level awareness (~120 lines)

**Total**: ~665 lines added across 7 agents

### AC2: Template Configuration Update

- [ ] Create template settings.json with complete documentation section (89 lines)
- [ ] Configure complexity thresholds (minimal ≤3, standard 4-10, comprehensive 7-10)
- [ ] Configure force-comprehensive triggers (security, breaking changes, compliance)
- [ ] Configure quality gate thresholds (≥80% line, ≥75% branch)
- [ ] Place in `installer/global/templates/default/settings.json` or equivalent

### AC3: Documentation Level Awareness Pattern

Each agent must include a **"Documentation Level Awareness (TASK-035)"** section following the exact pattern from ai-engineer.

**Required Structure** (see Pattern to Follow section below for complete details):
- Context Parameter section (how to receive `<AGENT_CONTEXT>` block)
- Output Adaptation section (minimal/standard/comprehensive examples)
- Quality Gates section (emphasizing what NEVER changes)
- Agent Collaboration section (if agent reads/writes markdown plans)

**Reference Pattern**: See `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/agents/requirements-analyst.md` for complete example.

### AC4: Quality Gates Preservation

Ensure ALL modes enforce identical quality standards:

- [ ] Build verification ALWAYS runs (100%)
- [ ] ALL tests ALWAYS execute (100% pass rate required)
- [ ] Coverage thresholds ALWAYS enforced (≥80% line, ≥75% branch)
- [ ] Architectural review ALWAYS runs (scored, embedded or standalone)
- [ ] Code review ALWAYS runs (scored, embedded or standalone)
- [ ] Fix loop ALWAYS runs (Phase 4.5, up to 3 attempts)
- [ ] Plan audit ALWAYS runs (Phase 5.5)

**What Changes**: Output format only (verbose docs vs concise summaries), not rigor or enforcement.

### AC5: Agent Collaboration Preservation

- [ ] Markdown plan ALWAYS generated (`.claude/task-plans/{TASK_ID}-implementation-plan.md`)
- [ ] Context parameter passing via `<AGENT_CONTEXT>` blocks
- [ ] Conversation context maintained across all phases
- [ ] All phase-to-phase data passing unchanged
- [ ] Backward compatible (agents without context parsing still work)

### AC6: Implementation Summary

- [ ] Create `TASK-035-REQUIREKIT-IMPLEMENTATION-SUMMARY.md`
- [ ] Document all 7 agent updates
- [ ] Document template configuration
- [ ] Include usage examples
- [ ] Provide testing recommendations

### AC7: Backward Compatibility

- [ ] Existing tasks run without changes
- [ ] No flag defaults to auto/standard mode
- [ ] All quality gates preserved (100%)
- [ ] No breaking changes to existing workflows

## Implementation Plan

### Phase 1: Global Agent Updates (3 hours)

**Step 1.1**: Update critical workflow agents (2 hours)
- `requirements-analyst.md` (~80 lines) - 30 min
- `architectural-reviewer.md` (~75 lines) - 30 min
- `test-orchestrator.md` (~145 lines) - 30 min
- `code-reviewer.md` (~95 lines) - 30 min

**Step 1.2**: Update orchestration agent (0.5 hours)
- `task-manager.md` (~70 lines)
  - Pass documentation_level to all sub-agents via `<AGENT_CONTEXT>` blocks
  - Coordinate summary generation based on mode

**Step 1.3**: Update supporting agents (0.5 hours)
- `bdd-generator.md` (~80 lines) - 15 min
- `test-verifier.md` (~120 lines) - 15 min

### Phase 2: Template Configuration (0.5 hours)

**Step 2.1**: Create template settings.json
- Add complete documentation section (89 lines)
- Configure RequireKit-specific defaults
- Place in appropriate template directory

**Step 2.2**: Verify configuration hierarchy
- Command-line flag > Force triggers > settings.json > complexity

### Phase 3: Documentation & Validation (1.5 hours)

**Step 3.1**: Create implementation summary (0.5 hours)
- Document all changes made
- List agent-by-agent updates
- Provide usage examples

**Step 3.2**: Manual testing (0.5 hours - optional)
- Test installer installs updated agents
- Verify agents have documentation level awareness
- Test task-work with different modes

**Step 3.3**: Cross-check with ai-engineer (0.5 hours)
- Ensure pattern consistency with ai-engineer agents
- Verify no differences in structure
- Confirm all quality gates preserved

## Pattern to Follow (Critical)

For each agent, add exactly this structure following ai-engineer implementation:

### 1. Documentation Level Awareness Section
Add after the main agent description, before examples:

```markdown
## Documentation Level Awareness (TASK-035)

**Context Parameter**: You receive a `<AGENT_CONTEXT>` block from task-work that specifies the current documentation level.

**Context Format**:
```xml
<AGENT_CONTEXT>
DOCUMENTATION_LEVEL: minimal|standard|comprehensive
TASK_ID: TASK-XXX
COMPLEXITY: 1-10
</AGENT_CONTEXT>
```

**Parsing**: Extract `DOCUMENTATION_LEVEL` value. If missing, default to `standard`.
```

### 2. Output Adaptation Section
Define output format for each mode:

```markdown
### Output Adaptation by Documentation Level

#### Minimal Mode (complexity 1-3, ≤12 min)
**When**: DOCUMENTATION_LEVEL=minimal OR complexity 1-3 with no flag
**Output Format**: Structured data (2-3 sentences max, JSON if applicable)
**Focus**: Essential changes only
**Example**: [Show minimal output for this agent]

#### Standard Mode (complexity 4-10, DEFAULT)
**When**: DOCUMENTATION_LEVEL=standard OR complexity 4-10 with no flag
**Output Format**: Full markdown report (current behavior)
**Focus**: Complete analysis with embedded sections
**Example**: [Show standard output for this agent]

#### Comprehensive Mode (complexity 7-10 or force triggers)
**When**: DOCUMENTATION_LEVEL=comprehensive OR force triggers active
**Output Format**: Enhanced report + standalone supporting documents
**Focus**: Exhaustive documentation for audit/compliance
**Supporting Documents**: [List agent-specific supporting docs]
**Example**: [Show comprehensive output for this agent]
```

### 3. Quality Gates Section
Critical - emphasize what NEVER changes:

```markdown
### Quality Gates (ALWAYS Enforced)

**CRITICAL**: The following quality checks run in ALL modes (minimal/standard/comprehensive):
- [List agent-specific quality gates]
- [Emphasize: Same rigor, different output format]

**What NEVER Changes**:
- Quality gate execution (all modes: 100%)
- Scoring methodology (identical across modes)
- Approval criteria (same thresholds)
- Test enforcement (100% pass rate always)
- Coverage requirements (≥80% line, ≥75% branch always)
```

### 4. Agent Collaboration Section (if applicable)
For agents that read markdown plans or communicate with other agents:

```markdown
### Agent Collaboration

**Markdown Plan**: This agent [reads/writes] the implementation plan at `.claude/task-plans/{TASK_ID}-implementation-plan.md`.
**Plan Format**: YAML frontmatter + structured markdown (always generated, all modes)
**Context Passing**: Uses `<AGENT_CONTEXT>` blocks for documentation_level parameter passing
**Backward Compatible**: Gracefully handles agents without context parameter support (defaults to standard)
```

## Files to Modify

### Agent Updates (7 files in installer/global/agents/)
1. `installer/global/agents/requirements-analyst.md` (~80 lines added)
2. `installer/global/agents/architectural-reviewer.md` (~75 lines added)
3. `installer/global/agents/test-orchestrator.md` (~145 lines added)
4. `installer/global/agents/code-reviewer.md` (~95 lines added)
5. `installer/global/agents/task-manager.md` (~70 lines added)
6. `installer/global/agents/bdd-generator.md` (~80 lines added)
7. `installer/global/agents/test-verifier.md` (~120 lines added)

### Template Configuration (1 file)
8. `installer/global/templates/default/settings.json` (+89 lines - documentation section) OR create template-specific configuration file

### Documentation (1 file)
9. `TASK-035-REQUIREKIT-IMPLEMENTATION-SUMMARY.md` (new file)

**Total**: 9 files (~754 lines added)

## Configuration Section to Add

Add this complete `documentation` section to template settings.json:

```json
{
  "documentation": {
    "enabled": true,
    "default_level": "auto",
    "complexity_thresholds": {
      "minimal_max": 3,
      "standard_max": 10
    },
    "force_comprehensive": {
      "keywords": ["security", "authentication", "compliance", "breaking change"],
      "triggers": ["security_changes", "compliance_required", "breaking_changes"]
    },
    "output_format": {
      "minimal": {
        "summary": "required",
        "plan": "required",
        "architecture_guide": "skip",
        "test_reports": "embedded",
        "code_review": "embedded"
      },
      "standard": {
        "summary": "required",
        "plan": "required",
        "architecture_guide": "embedded",
        "test_reports": "embedded",
        "code_review": "embedded"
      },
      "comprehensive": {
        "summary": "required",
        "plan": "required",
        "architecture_guide": "standalone",
        "test_reports": "standalone",
        "code_review": "standalone",
        "supporting_docs": "all"
      }
    },
    "agent_behavior": {
      "requirements_analyst": {
        "minimal": "skip_ears_docs",
        "standard": "inline_requirements",
        "comprehensive": "standalone_ears_doc"
      },
      "architectural_reviewer": {
        "minimal": "json_scores",
        "standard": "embedded_summary",
        "comprehensive": "standalone_guide"
      },
      "test_orchestrator": {
        "minimal": "json_results",
        "standard": "full_report",
        "comprehensive": "enhanced_report_with_supporting_docs"
      },
      "code_reviewer": {
        "minimal": "json_findings",
        "standard": "full_report",
        "comprehensive": "detailed_report_with_metrics"
      }
    },
    "performance_targets": {
      "minimal": {
        "duration_minutes": "8-12",
        "token_estimate": "100-150k",
        "files_generated": 2
      },
      "standard": {
        "duration_minutes": "12-18",
        "token_estimate": "150-250k",
        "files_generated": "2-5"
      },
      "comprehensive": {
        "duration_minutes": "36+",
        "token_estimate": "500k+",
        "files_generated": "13+"
      }
    }
  }
}
```

## Testing Strategy

### Installer Testing

1. **Verify Agent Installation**:
   ```bash
   cd /Users/richardwoollcott/Projects/appmilla_github/require-kit
   ./installer/scripts/install.sh
   # Verify: Updated agents installed to ~/.agentecflow/agents/
   grep -l "Documentation Level Awareness" ~/.agentecflow/agents/*.md
   # Should find 7 agents
   ```

2. **Verify Configuration**:
   ```bash
   # Check template settings.json has documentation section
   cat ~/.agentecflow/templates/default/settings.json | grep -A 50 '"documentation"'
   ```

### Task-Work Testing (Optional - Verification Only)

1. **Test Minimal Mode**:
   ```bash
   /task-work TASK-XXX --docs minimal
   # Verify: 2 files generated, concise output, quality gates enforced
   ```

2. **Test Standard Mode** (default):
   ```bash
   /task-work TASK-YYY
   # Verify: 2-5 files, embedded summaries, quality gates enforced
   ```

3. **Test Comprehensive Mode**:
   ```bash
   /task-work TASK-ZZZ --docs comprehensive
   # Verify: 13+ files, standalone guides, quality gates enforced
   ```

### Quality Verification

- [ ] All 7 agents updated with consistent pattern matching ai-engineer
- [ ] Template configuration added
- [ ] Implementation summary created
- [ ] Installer successfully installs updated agents
- [ ] No breaking changes to existing tasks
- [ ] Backward compatibility verified

## Dependencies

**Blocked by**: None (ai-engineer implementation complete, pattern established)
**Blocks**: None (independent RequireKit implementation)

## Related Documentation

- **Core Implementation**: `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/docs/requirements/TASK-035-FINAL-IMPLEMENTATION-SUMMARY.md`
- **Reference Agents (ai-engineer)**: `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/agents/`
- **User Guide**: `~/.agentecflow/docs/guides/documentation-levels-guide.md`
- **Context Format**: `~/.agentecflow/instructions/context-parameter-format.md`
- **Templates**: `~/.agentecflow/templates/documentation/`

## Success Metrics

### Implementation Metrics
- **Agents Updated**: 7/7 (100%) in installer/global/agents/
- **Lines Added**: ~754 lines
- **Configuration**: Template settings.json with documentation section (89 lines)
- **Documentation**: Implementation summary created

### Performance Impact (Projected)
- **Simple tasks**: 78% faster (8-12 min vs 36 min)
- **Medium tasks**: 50% faster (12-18 min vs 36 min)
- **Complex tasks**: Same comprehensive documentation (36+ min) when needed

### Quality Preservation
- **100%** of quality gates preserved across all modes
- **100%** test pass rate required in all modes
- **100%** coverage thresholds enforced in all modes
- **100%** backward compatibility (no breaking changes)

## Definition of Done

- [ ] All 7 global agents in installer/global/agents/ updated with documentation level awareness
- [ ] Template settings.json updated with complete documentation section
- [ ] Consistent pattern applied across all agents (matching ai-engineer)
- [ ] Implementation summary document created
- [ ] Installer successfully installs updated agents
- [ ] Quality gates preservation verified
- [ ] Agent collaboration preservation verified
- [ ] Backward compatibility verified
- [ ] Ready for RequireKit installer to deploy

---

**Priority Justification**: HIGH
- RequireKit is the primary task execution system (task-create, task-work commands)
- Enables 50-78% time savings on all future development
- Maintains 100% quality with faster iteration
- Critical for RequireKit split from ai-engineer

**Complexity Justification**: 7/10 (Medium-High)
- Multiple installer agents (7 agents)
- Must maintain pattern consistency with ai-engineer
- Template configuration setup
- Installer integration
- More complex than local agent updates (affects all RequireKit users)

**Estimated Time Justification**: 2-3 hours (reduced from 4-5 hours)
- Agent updates: 1.5 hours (7 agents × ~13 min each, using proven TASK-036 pattern)
- Template configuration: 0.5 hours
- Documentation & validation: 0.5 hours (pattern already validated)

---

## TASK-036 Reference Implementation

**Use this proven pattern for all 7 agents**:

### Guard Clause Section Template
Location: After agent description, before examples

```markdown
## Documentation Level Handling

CRITICAL: Check `<AGENT_CONTEXT>` for `documentation_level` parameter before generating output.

### Minimal Mode (`documentation_level: minimal`)
- Generate only essential outputs
- Skip verbose explanations and examples
- Focus on actionable content
- Target: 50-75% token reduction

### Standard Mode (`documentation_level: standard`)
- Current default behavior
- Balanced documentation
- Include examples and context

### Comprehensive Mode (`documentation_level: comprehensive`)
- Full verbose documentation
- Extensive examples and explanations
- Complete traceability
```

### Quality Gate Preservation Statement
**CRITICAL**: Include in every agent

```markdown
**Quality Gate Preservation**: The following quality checks run in ALL modes (minimal/standard/comprehensive):
- [List agent-specific gates]
- Same rigor, different output format
```

### Files Modified in TASK-036 (Reference)
1. `.claude/agents/requirements-analyst.md` (+25 lines) - Lines 17-41
2. `.claude/agents/bdd-generator.md` (+46 lines) - Lines 18-63
3. `.claude/agents/test-orchestrator.md` (+41 lines) - Lines 18-58

**View Complete Pattern**:
```bash
cat /Users/richardwoollcott/Projects/appmilla_github/ai-engineer/.claude/agents/requirements-analyst.md | sed -n '17,41p'
```

### Test Results from TASK-036
- 16/16 tests passed (100%)
- Code quality: 8.5/10
- Architectural review: 88/100
- Zero scope creep

**Apply this exact pattern to RequireKit's 7 agents in `installer/global/agents/`**
