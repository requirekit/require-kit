# TASK-035 Analysis for require-kit - Documentation Levels

**Date**: 2025-11-01
**Status**: HIGHLY RELEVANT (Simplified Scope)
**Effort**: 1-2 hours (vs original 16-20 hours for full task execution system)

## Executive Summary

**YES - This is relevant to require-kit**, but with MUCH simpler scope:
- **Original TASK-035**: 7 agents for full task execution workflow (deleted in REQ-002)
- **require-kit TASK-035**: Only **2 agents** for requirements gathering
- **Time savings**: Same 50-70% token reduction potential
- **Effort reduction**: 1-2 hours vs 16-20 hours (90% reduction)

## Current State (Post-REQ-002)

require-kit has only **2 agents**:
1. `requirements-analyst.md` - EARS notation gathering
2. `bdd-generator.md` - BDD/Gherkin scenario generation

require-kit has **12 commands**:
- `gather-requirements.md` ← Uses requirements-analyst
- `formalize-ears.md` ← Uses requirements-analyst
- `generate-bdd.md` ← Uses bdd-generator
- Epic/feature commands (9) ← Minimal output already

## Problem Statement

The requirements-analyst and bdd-generator agents can be verbose, especially when:
- Gathering comprehensive requirements (long EARS documentation)
- Generating extensive BDD scenarios (multiple files, detailed examples)
- Creating epic/feature hierarchies (verbose explanations)

**Token Usage Observations**:
- Simple requirement: Can consume 50-100K tokens with full documentation
- Complex feature: Can consume 150-300K tokens with comprehensive EARS + BDD
- Most of this is explanation and examples that might not always be needed

## Proposed Solution: Documentation Levels for require-kit

Add 3 documentation levels to require-kit commands:

### Minimal Mode (Quick Requirements)
**Use Case**: Simple requirements, quick iteration, basic documentation
**Commands affected**: `gather-requirements`, `formalize-ears`, `generate-bdd`
**Behavior**:
- requirements-analyst: Skip verbose EARS documentation, focus on core requirements only
- bdd-generator: Generate essential scenarios only (happy path + 1 error case)
- Token reduction: 60-75%
- Output: Inline requirements in task files (no standalone docs)

**Example**:
```bash
/gather-requirements --docs minimal
# Result: Concise Q&A, requirements embedded in task file, minimal explanation
```

### Standard Mode (DEFAULT - Current Behavior)
**Use Case**: Most requirements gathering, balanced documentation
**Commands affected**: All (default behavior)
**Behavior**:
- requirements-analyst: Current behavior (inline EARS + examples)
- bdd-generator: Current behavior (comprehensive scenarios)
- Token usage: Current baseline
- Output: Standard markdown files with embedded content

### Comprehensive Mode (Detailed Documentation)
**Use Case**: Complex features, compliance/audit requirements, handoff documentation
**Commands affected**: `gather-requirements`, `formalize-ears`, `generate-bdd`
**Behavior**:
- requirements-analyst: Standalone EARS documentation + rationale + examples + traceability
- bdd-generator: Exhaustive BDD scenarios + supporting documentation + test data
- Token usage: 150-200% of standard (more comprehensive)
- Output: Multiple standalone documents

**Example**:
```bash
/gather-requirements --docs comprehensive
# Result: Standalone EARS doc + requirements traceability matrix + acceptance criteria doc
```

## Implementation Plan (Simplified)

### Phase 1: Update 2 Agents (1 hour)

#### 1.1: requirements-analyst.md (~30 min)
Add documentation level awareness section:

```markdown
## Documentation Level Handling

CRITICAL: Check for `--docs` flag or complexity to determine output level.

### Minimal Mode (--docs minimal)
- Skip verbose EARS documentation
- Generate concise requirement statements only
- Embed requirements inline in task files
- Target: 60-75% token reduction

**Output Example**:
```markdown
## REQ-042: User Authentication

When valid credentials submitted, system shall:
- Validate against auth service
- Generate JWT (24h expiry)
- Return token in response
- Log event
```

### Standard Mode (DEFAULT)
- Current behavior
- Inline EARS with examples
- Balanced documentation

### Comprehensive Mode (--docs comprehensive)
- Standalone EARS documentation file
- Full rationale and traceability
- Detailed acceptance criteria
- Examples for each scenario

**Output Example**: Separate files:
- `docs/requirements/REQ-042-ears.md` (full specification)
- `docs/requirements/REQ-042-traceability.md` (links to tests, features)
- `docs/requirements/REQ-042-acceptance.md` (detailed criteria)
```

#### 1.2: bdd-generator.md (~30 min)
Add documentation level awareness section:

```markdown
## Documentation Level Handling

CRITICAL: Check for `--docs` flag to determine BDD output verbosity.

### Minimal Mode (--docs minimal)
- Generate essential scenarios only (happy path + 1 error case)
- Skip extensive examples and edge cases
- Concise scenario descriptions
- Target: 65-80% token reduction

**Output Example**:
```gherkin
Feature: User Authentication

  Scenario: Successful login
    Given user has valid credentials
    When user submits login form
    Then user receives JWT token
    And user is redirected to dashboard

  Scenario: Invalid credentials
    Given user has invalid credentials
    When user submits login form
    Then user sees error message
```

### Standard Mode (DEFAULT)
- Current behavior
- Comprehensive scenarios with examples
- Happy path + error cases + edge cases

### Comprehensive Mode (--docs comprehensive)
- Exhaustive BDD scenarios
- Multiple examples per scenario (Scenario Outline)
- Supporting documentation (test data, setup guides)
- Edge cases and performance scenarios

**Output Example**: Separate files:
- `docs/bdd/REQ-042-scenarios.feature` (main scenarios)
- `docs/bdd/REQ-042-test-data.md` (test data tables)
- `docs/bdd/REQ-042-edge-cases.feature` (additional scenarios)
```

### Phase 2: Update Commands (0.5 hours)

Update 3 commands to accept `--docs` flag:

#### 2.1: gather-requirements.md
```markdown
## Usage

```bash
/gather-requirements [--docs minimal|standard|comprehensive]
```

### Flags

- `--docs minimal`: Quick requirements gathering, minimal documentation
- `--docs standard`: DEFAULT - Balanced documentation (current behavior)
- `--docs comprehensive`: Detailed documentation for audit/compliance
```

#### 2.2: formalize-ears.md
Add same `--docs` flag support

#### 2.3: generate-bdd.md
Add same `--docs` flag support

### Phase 3: Create Summary Doc (0.5 hours)

Document the changes in `TASK-035-REQUIREKIT-IMPLEMENTATION-SUMMARY.md`

## Files to Modify

### Agents (2 files - ~60 lines total)
1. `installer/global/agents/requirements-analyst.md` (~30 lines)
2. `installer/global/agents/bdd-generator.md` (~30 lines)

### Commands (3 files - ~30 lines total)
3. `installer/global/commands/gather-requirements.md` (~10 lines - add --docs flag)
4. `installer/global/commands/formalize-ears.md` (~10 lines - add --docs flag)
5. `installer/global/commands/generate-bdd.md` (~10 lines - add --docs flag)

### Documentation (1 file - new)
6. `TASK-035-REQUIREKIT-IMPLEMENTATION-SUMMARY.md` (new file)

**Total**: 6 files, ~90 lines added

## Expected Benefits

### Token Reduction
- **Minimal mode**: 60-75% fewer tokens (similar to proven TASK-036 results)
- **Standard mode**: Same as current (baseline)
- **Comprehensive mode**: 150-200% of standard (when needed)

### Time Savings
- **Simple requirements**: 50-70% faster gathering
- **Standard requirements**: Same as current
- **Complex features**: Same comprehensive documentation when needed

### Use Cases

**When to use MINIMAL**:
- Bug fixes (just need core requirement statement)
- Simple features (basic CRUD operations)
- Internal tools (less documentation needed)
- Rapid prototyping
- Iterative refinement (first draft)

**When to use STANDARD** (default):
- Most requirements gathering
- Feature development
- Normal workflow

**When to use COMPREHENSIVE**:
- Complex features requiring audit trail
- Compliance/regulatory requirements
- Handoff documentation (to other teams)
- Production-critical features
- Public API design

## Comparison with Original TASK-035

| Aspect | Original TASK-035 | require-kit TASK-035 |
|--------|-------------------|----------------------|
| **Agents** | 7 agents (task execution) | 2 agents (requirements) |
| **Commands** | task-work (multi-phase) | gather/formalize/generate (3 commands) |
| **Complexity** | 7/10 (high) | 3/10 (low) |
| **Effort** | 16-20 hours | 1-2 hours |
| **Benefit** | 50-78% time reduction in task execution | 60-75% token reduction in requirements |
| **Scope** | Full SDLC workflow | Requirements gathering only |

## Risk Assessment

### Risks
- **Low Risk**: Only 2 agents, well-defined scope
- **Proven Pattern**: TASK-036 validated the approach
- **Backward Compatible**: Standard mode = current behavior
- **No Quality Impact**: Same rigor, just less verbose output

### Mitigation
- Test with simple requirement first
- Validate minimal mode produces correct EARS notation
- Ensure BDD scenarios remain testable in all modes

## Recommendation

**Priority**: HIGH (but after TASK-019 and REQ-003)

**Rationale**:
1. **High ROI**: 1-2 hours effort for 60-75% token reduction
2. **Proven Pattern**: TASK-036 validated the approach (16/16 tests passed)
3. **Simple Scope**: Only 2 agents (vs original 7)
4. **Backward Compatible**: No breaking changes
5. **Pairs Well**: Complements TASK-019 (concise mode)

**Implementation Order**:
1. ✅ REQ-002: Delete Agentecflow (DONE)
2. TASK-019: Concise Mode (2-3 hours) ← Do first
3. REQ-003: Shared Installer (5 hours) ← Critical for distribution
4. **TASK-035-SIMPLIFIED**: Documentation Levels (1-2 hours) ← Then do this
5. TASK-022: Spec Templates (6-8 hours)

## Action Items

1. **Rename Task**: "TASK-035-SIMPLIFIED: Add Documentation Levels to Requirements Commands"
2. **Update Scope**: Remove references to deleted agents (architectural-reviewer, test-orchestrator, code-reviewer, etc.)
3. **Focus**: Only requirements-analyst and bdd-generator
4. **Priority**: HIGH (but after TASK-019 and REQ-003)

## Example Usage Patterns

### Quick Bug Fix Requirement
```bash
# Minimal docs for quick iteration
/gather-requirements --docs minimal
# Result: Concise requirement, no verbose EARS explanation
```

### Standard Feature
```bash
# Default behavior (no flag needed)
/gather-requirements
/formalize-ears
/generate-bdd
# Result: Current balanced documentation
```

### Compliance Feature
```bash
# Comprehensive docs for audit
/gather-requirements --docs comprehensive
/formalize-ears --docs comprehensive
/generate-bdd --docs comprehensive
# Result: Full EARS specification + traceability + exhaustive BDD scenarios
```

## Success Metrics

### Implementation
- ✅ 2 agents updated (100%)
- ✅ 3 commands updated (100%)
- ✅ Documentation created
- ✅ Backward compatible (standard mode = current behavior)

### Performance
- 🎯 60-75% token reduction (minimal mode)
- 🎯 50-70% faster requirements gathering (minimal mode)
- 🎯 Same quality requirements in all modes

### Adoption
- Track usage of --docs flag
- Measure token savings
- Gather user feedback

## Conclusion

**TASK-035 is HIGHLY RELEVANT to require-kit**, but needs simplification:
- Original: 7 agents, 16-20 hours, complex task execution workflow
- Simplified: 2 agents, 1-2 hours, requirements gathering only

**Recommendation: Implement as TASK-035-SIMPLIFIED after TASK-019 and REQ-003**

This gives require-kit the same token reduction benefits (60-75%) that task-work got from documentation levels, but with 90% less implementation effort.

---

**Prepared by**: Claude Code
**Date**: 2025-11-01
**Context**: Post-REQ-002 analysis for require-kit scope
