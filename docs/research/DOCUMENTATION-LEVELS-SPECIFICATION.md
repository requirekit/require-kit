# Documentation Levels - Implementation Specification

**Date**: 2025-10-29
**Status**: Ready for Implementation
**Owner**: Task-Work Command Enhancement

---

## Overview

This specification defines a **tiered documentation system** for the `/task-work` command that balances speed with quality through three documentation levels: **minimal**, **standard**, and **comprehensive**.

---

## Design Principles

### 1. Intelligent Defaults
- **Low complexity (1-3)**: Minimal documentation (fast iteration)
- **Medium/High complexity (4-10)**: Standard documentation (balanced approach)
- Default provides good balance of speed and visibility

### 2. User Control via Configuration Hierarchy
```
Command-line flag --docs   (highest priority)
    ↓
.claude/settings.json      (project-level preference)
    ↓
Complexity-based rules     (intelligent fallback)
```

### 3. No Quality Compromise
- All quality gates remain active
- Architecture review always runs (just less verbose reporting)
- Code review always runs
- Test coverage always measured
- Only documentation verbosity changes

---

## Documentation Levels Detailed

### Level 1: Minimal (RUTHLESSLY PRUNED)

**Purpose**: Fast execution for simple tasks - **code is documentation**

**Philosophy**: Only generate what humans actually read. Delete everything else.

**Generated Documents** (2 files total):

1. **Implementation Summary** (`TASK-XXX-SUMMARY.md`, ~200 lines)
   - What changed (files, LOC, +/- lines)
   - Quality gate results (compilation, tests, coverage, architecture score, review score)
   - Test results (passed/failed counts)
   - Critical decisions made
   - Next steps

2. **Markdown Implementation Plan** (`.claude/task-plans/TASK-XXX-implementation-plan.md`, ~500 lines)
   - **Why**: Required for agent collaboration (Phase 2.5B, 5.5)
   - **Human value**: Can read at checkpoint (Phase 2.8) if desired
   - **Format**: Structured markdown with YAML frontmatter
   - **Lightweight**: ~500 lines vs 1,750 lines for verbose plan

**That's it. Nothing else.**

**Deleted Entirely** (shelf-ware - nobody reads these):
- ❌ EARS requirements formalization (1,587 lines) - tests are better specs
- ❌ Verbose TDD implementation plan (1,750 lines) - code is better documentation
- ❌ Architecture guide documents (665 lines) - scores in summary are sufficient
- ❌ Phase-by-phase status reports (variable) - single final summary is enough
- ❌ Redundant summaries (Quick Reference, Executive Summary, Index, etc.) - pure duplication
- ❌ Test specification documents - tests themselves are the spec
- ❌ Verbose test reports - CI output + summary is sufficient
- ❌ Verbose code review reports - scores in summary are sufficient

**Quality Gates Still Run** (no compromise):
- ✅ Compilation check (100% pass required)
- ✅ Test execution (100% pass required)
- ✅ Coverage measurement (≥80% line, ≥75% branch)
- ✅ Architecture review (scored, embedded in summary)
- ✅ Code review (scored, embedded in summary)

**Expected Performance**:
- Duration: ~8-12 minutes (vs 36+ minutes currently)
- Tokens: ~100-150k (vs 500k currently)
- Files: 2 (vs 13+ currently)
- Size: ~15KB (vs 210KB currently)
- Reduction: **67-78% time savings, 70-80% token savings, 85% file reduction**

**Human Read Time**:
- Implementation summary: 2-3 minutes
- Markdown plan: 5-10 minutes (optional, at checkpoint)
- **Total**: ~5-10 minutes (vs 0 minutes for verbose docs nobody reads)

**Agent Collaboration**:
- ✅ Fully functional (markdown plan preserved)
- ✅ Phase 2.5B architectural review reads plan
- ✅ Phase 5.5 plan audit reads plan
- ✅ Conversation context maintained

**Use Cases**:
- Bug fixes (complexity 1-3)
- Simple refactoring (complexity 1-3)
- Configuration changes
- Minor feature additions
- Documentation updates
- **Any task where speed > verbose documentation**

---

### Level 2: Standard (DEFAULT - STREAMLINED)

**Purpose**: Balanced approach with architecture visibility - **still ruthlessly pruned**

**Philosophy**: Generate enhanced summary with architecture insights. Delete verbose standalone docs.

**Generated Documents** (2 files total):

1. **Enhanced Implementation Summary** (`TASK-XXX-SUMMARY.md`, ~300-400 lines)
   - What changed (files, LOC, +/- lines)
   - **Architecture Review Section** (embedded, not standalone):
     - SOLID/DRY/YAGNI scores (with breakdown)
     - Pattern compliance
     - Risk assessment
     - Key recommendations
     - Approval decision
   - **Test Results Section** (embedded, not standalone):
     - Compilation status
     - Test pass/fail counts
     - Coverage metrics (line/branch)
     - Fix loop attempts (if any)
   - **Code Review Section** (embedded, not standalone):
     - Quality score
     - Critical findings (if any)
     - Approval decision
   - Critical decisions made
   - Next steps

2. **Markdown Implementation Plan** (`.claude/task-plans/TASK-XXX-implementation-plan.md`, ~500 lines)
   - **Why**: Required for agent collaboration + human checkpoint
   - **Human value**: Reviewed at Phase 2.8 checkpoint (5-10 min read)
   - **Agent value**: Read by architectural-reviewer (Phase 2.5B) and code-reviewer (Phase 5.5)
   - **Format**: Structured markdown with YAML frontmatter

**That's it. Nothing else.**

**Deleted Entirely** (even for complex tasks - code is truth):
- ❌ EARS requirements (unless BDD mode explicitly enabled) - task description + tests are sufficient
- ❌ Verbose TDD implementation plan (1,750 lines) - markdown plan is sufficient
- ❌ Standalone architecture guide (665 lines) - embedded in summary instead
- ❌ Standalone test reports - embedded in summary instead
- ❌ Standalone code review reports - embedded in summary instead
- ❌ Phase-by-phase status reports - single final summary
- ❌ Redundant summaries (Quick Reference, Executive Summary, Visual Guide, Index, Checklist, etc.)

**Quality Gates Still Run** (no compromise):
- ✅ All gates active (same as minimal)
- ✅ Architecture review with detailed scoring (embedded in summary)
- ✅ Complexity evaluation with rationale
- ✅ Human checkpoint (if complexity ≥4) using markdown plan

**Expected Performance**:
- Duration: ~12-18 minutes (vs 36+ minutes currently)
- Tokens: ~200-300k (vs 500k currently)
- Files: 2 (vs 13+ currently)
- Size: ~30KB (vs 210KB currently)
- Reduction: **50-67% time savings, 40-60% token savings, 85% file reduction**

**Human Read Time**:
- Implementation summary: 5-10 minutes (expanded with architecture/review sections)
- Markdown plan: 5-10 minutes (at checkpoint)
- **Total**: ~10-20 minutes (actually valuable reading)

**Agent Collaboration**:
- ✅ Fully functional (markdown plan preserved)
- ✅ Architecture review reads plan, embeds findings in summary
- ✅ Plan audit reads plan, embeds findings in summary
- ✅ Conversation context maintained

**Use Cases**:
- Medium complexity tasks (4-6)
- High complexity tasks (7-10)
- Architecture-sensitive changes
- Pattern-driven development
- Team collaboration (plan review at checkpoint)
- **Default for most development work**

---

### Level 3: Comprehensive

**Purpose**: Full documentation for audit, compliance, training, and complex architectures

**Generated Documents**:
1. **Requirements Analysis** (40-50 pages)
   - EARS notation requirements
   - Acceptance criteria breakdown
   - Test case specifications
   - Traceability matrices

2. **Implementation Plan** (50-60 pages)
   - TDD cycle detailed plan
   - File-by-file implementation guide
   - Complete test specifications
   - Architecture diagrams
   - Dependency analysis

3. **Architecture Guide** (25-30 pages)
   - Pattern documentation
   - SOLID compliance analysis
   - Dependency diagrams
   - Integration points
   - Risk assessment

4. **Completion Report** (15-20 pages)
   - Implementation summary
   - Quality gate results
   - Test coverage metrics
   - Code review findings
   - Next steps

5. **Supporting Documents**
   - Quick Reference
   - Executive Summary
   - Visual Guide
   - Architecture Diagram
   - Checklist
   - Index/Manifest

**Quality Gates**:
- ✅ All gates active with verbose reporting

**Expected Performance**:
- Duration: ~36+ minutes (current behavior)
- Tokens: ~500k+ (current behavior)
- **No change from current** (this is existing behavior)

**Use Cases**:
- Enterprise compliance requirements
- Audit trail creation
- Training/documentation purposes
- Complex architectural changes
- Security/schema critical changes
- External stakeholder communication

---

## Configuration Hierarchy

### Priority 1: Command-Line Flag (Highest)

**Syntax**:
```bash
/task-work TASK-XXX --docs=minimal
/task-work TASK-XXX --docs=standard
/task-work TASK-XXX --docs=comprehensive
```

**Behavior**: Overrides all other settings (config file, complexity rules)

**Use Cases**:
- One-off override (usually comprehensive for specific task)
- Testing different documentation levels
- Audit requirement for specific task

**Examples**:
```bash
# Simple task but need comprehensive docs for audit
/task-work TASK-047 --docs=comprehensive

# Complex task but you trust the approach, want speed
/task-work TASK-065 --docs=minimal

# Default to complexity rules
/task-work TASK-065
```

---

### Priority 2: Configuration File (Project-Level)

**Location**: `.claude/settings.json`

**New Configuration Section**:
```json
{
  "stack": "maui",
  "plan_review": { ... },
  "task_creation": { ... },

  "documentation": {
    "default_level": "auto",
    "preferences": {
      "generate_ears_requirements": "auto",
      "generate_implementation_plan": true,
      "generate_architecture_guides": "auto",
      "consolidate_phase_reports": true,
      "verbose_test_documentation": false
    },
    "level_overrides": {
      "minimal": {
        "max_files": 1,
        "max_pages": 10
      },
      "standard": {
        "max_files": 3,
        "max_pages": 50
      },
      "comprehensive": {
        "max_files": 999,
        "max_pages": 999
      }
    }
  }
}
```

**Field Definitions**:

#### `default_level` (string)
- **Values**: `"auto"` | `"minimal"` | `"standard"` | `"comprehensive"`
- **Default**: `"auto"`
- **Behavior**:
  - `"auto"`: Use complexity-based rules (see Priority 3)
  - `"minimal"`: Always minimal (unless --docs flag overrides)
  - `"standard"`: Always standard (unless --docs flag overrides)
  - `"comprehensive"`: Always comprehensive (unless --docs flag overrides)

#### `preferences.generate_ears_requirements` (string)
- **Values**: `"auto"` | `"always"` | `"never"`
- **Default**: `"auto"`
- **Behavior**:
  - `"auto"`: Generate if BDD mode OR complexity ≥7 OR requirements undefined
  - `"always"`: Always generate EARS requirements
  - `"never"`: Never generate EARS requirements

#### `preferences.generate_implementation_plan` (boolean)
- **Values**: `true` | `false`
- **Default**: `true`
- **Behavior**: Controls markdown plan saved to `.claude/task-plans/`
- **Note**: Always generated for Phase 2.8 checkpoint, this controls persistence

#### `preferences.generate_architecture_guides` (string)
- **Values**: `"auto"` | `"always"` | `"never"`
- **Default**: `"auto"`
- **Behavior**:
  - `"auto"`: Generate if complexity ≥4 AND level ≥ standard
  - `"always"`: Always generate standalone architecture guides
  - `"never"`: Embed architecture summary in main report only

#### `preferences.consolidate_phase_reports` (boolean)
- **Values**: `true` | `false`
- **Default**: `true`
- **Behavior**:
  - `true`: Single final summary only (recommended)
  - `false`: Generate phase-by-phase status reports (verbose, current behavior)

#### `preferences.verbose_test_documentation` (boolean)
- **Values**: `true` | `false`
- **Default**: `false`
- **Behavior**:
  - `false`: Test summary in final report only
  - `true`: Generate test specs across multiple phases (current behavior)

**Example Configurations**:

**Speed-focused project**:
```json
{
  "documentation": {
    "default_level": "minimal",
    "preferences": {
      "generate_ears_requirements": "never",
      "generate_implementation_plan": false,
      "consolidate_phase_reports": true,
      "verbose_test_documentation": false
    }
  }
}
```

**Enterprise compliance project**:
```json
{
  "documentation": {
    "default_level": "comprehensive",
    "preferences": {
      "generate_ears_requirements": "always",
      "generate_implementation_plan": true,
      "generate_architecture_guides": "always",
      "consolidate_phase_reports": false,
      "verbose_test_documentation": true
    }
  }
}
```

**Balanced approach (RECOMMENDED DEFAULT)**:
```json
{
  "documentation": {
    "default_level": "auto",
    "preferences": {
      "generate_ears_requirements": "auto",
      "generate_implementation_plan": true,
      "generate_architecture_guides": "auto",
      "consolidate_phase_reports": true,
      "verbose_test_documentation": false
    }
  }
}
```

---

### Priority 3: Complexity-Based Rules (Intelligent Fallback)

**Applied When**:
- No `--docs` flag provided
- `default_level: "auto"` in settings.json (or field not present)

**Rules** (UPDATED per user feedback):

| Complexity Score | Documentation Level | Rationale |
|------------------|---------------------|-----------|
| 1-3 (Simple) | **Minimal** | Fast iteration, low risk, simple changes |
| 4-6 (Medium) | **Standard** | Architecture visibility valuable, balanced speed |
| 7-10 (Complex) | **Standard** | Full architecture review, but streamlined reporting |

**Note**: User can override to **Comprehensive** via flag for any task needing audit trail.

**Complexity Score Calculation** (unchanged):
- File complexity (0-3): Based on number of files
- Pattern familiarity (0-2): Known vs new patterns
- Risk assessment (0-3): Low/medium/high risk
- Dependencies (0-2): Number of external dependencies

**Examples**:

```bash
# TASK-047: Bug fix (complexity 2/10)
/task-work TASK-047
# → Uses MINIMAL (fast, ~12 min)

# TASK-065: Refactoring (complexity 5/10)
/task-work TASK-065
# → Uses STANDARD (balanced, ~20 min)

# TASK-100: New architecture (complexity 8/10)
/task-work TASK-100
# → Uses STANDARD (architecture visible, ~24 min)

# TASK-100: Same, but need audit docs
/task-work TASK-100 --docs=comprehensive
# → Uses COMPREHENSIVE (full audit trail, ~36+ min)
```

---

## Decision Tree

```
┌─────────────────────────────┐
│ /task-work TASK-XXX [flags] │
└──────────┬──────────────────┘
           │
           ├──► --docs=minimal? ──────────► MINIMAL
           │
           ├──► --docs=standard? ─────────► STANDARD
           │
           ├──► --docs=comprehensive? ────► COMPREHENSIVE
           │
           └──► No --docs flag
                │
                ├──► Check settings.json
                │    │
                │    ├──► default_level: "minimal"? ──► MINIMAL
                │    │
                │    ├──► default_level: "standard"? ─► STANDARD
                │    │
                │    ├──► default_level: "comprehensive"? ─► COMPREHENSIVE
                │    │
                │    └──► default_level: "auto" (or missing)
                │         │
                │         └──► Use Complexity Rules
                │              │
                │              ├──► Complexity 1-3? ──► MINIMAL
                │              │
                │              ├──► Complexity 4-6? ──► STANDARD
                │              │
                │              └──► Complexity 7-10? ─► STANDARD
                │
                └──► (user can override via flag at any time)
```

---

## Implementation Changes Required

### 1. Command Parser Updates

**File**: `installer/global/commands/task-work.md`

**Add Flag**:
```markdown
## Flags

### --docs=LEVEL

**Values**: minimal | standard | comprehensive
**Default**: Auto-determined by complexity or settings.json
**Priority**: Overrides settings.json and complexity rules

**Examples**:
/task-work TASK-065 --docs=minimal
/task-work TASK-065 --docs=standard
/task-work TASK-065 --docs=comprehensive
```

### 2. Settings Schema Update

**File**: `.claude/settings.json`

**Add Section**:
```json
{
  "documentation": {
    "default_level": "auto",
    "preferences": {
      "generate_ears_requirements": "auto",
      "generate_implementation_plan": true,
      "generate_architecture_guides": "auto",
      "consolidate_phase_reports": true,
      "verbose_test_documentation": false
    }
  }
}
```

### 3. Agent Prompt Updates

**Files to Update**:
- `installer/global/agents/requirements-analyst.md`
- `installer/global/agents/architectural-reviewer.md`
- `installer/global/agents/test-orchestrator.md`
- `installer/global/agents/code-reviewer.md`
- Stack-specific planning agents (maui-usecase-specialist, etc.)

**Add to Each Agent**:
```markdown
## Documentation Level Awareness

You will receive a `documentation_level` parameter: minimal | standard | comprehensive

### Minimal Mode
- Store analysis data in structured format (for final summary)
- Do NOT generate standalone documents
- Do NOT generate verbose reports
- Focus on implementation/review

### Standard Mode
- Generate concise architecture summary (embed in main report)
- Store plan data (already done via markdown plan)
- Consolidated final report only

### Comprehensive Mode
- Current behavior (generate all documents)
- Verbose reports and standalone guides
```

### 4. Task-Work Execution Logic

**Pseudocode**:
```python
def determine_documentation_level(task_id: str, flags: dict) -> str:
    # Priority 1: Command-line flag
    if flags.get("docs"):
        return flags["docs"]  # minimal | standard | comprehensive

    # Priority 2: Settings.json
    settings = load_settings(".claude/settings.json")
    default_level = settings.get("documentation", {}).get("default_level", "auto")

    if default_level != "auto":
        return default_level  # minimal | standard | comprehensive

    # Priority 3: Complexity-based rules
    complexity_score = evaluate_complexity(task_id)

    if complexity_score <= 3:
        return "minimal"
    else:  # 4-10
        return "standard"

def task_work(task_id: str, flags: dict):
    # Determine level
    doc_level = determine_documentation_level(task_id, flags)

    # Pass to all agents
    context = {
        "task_id": task_id,
        "documentation_level": doc_level,
        "preferences": load_documentation_preferences()
    }

    # Execute phases with context
    phase1_result = run_agent("requirements-analyst", context)
    phase2_result = run_agent("planning-specialist", context)
    # ... etc

    # Generate final summary based on level
    generate_final_summary(doc_level, all_phase_results)
```

### 5. Final Summary Generator

**New Component**: `lib/documentation_generator.py`

**Responsibilities**:
- Consolidate phase results into single summary
- Apply documentation level rules
- Generate appropriate output based on level

**Templates**:
- `minimal_summary_template.md` (~200 lines)
- `standard_summary_template.md` (~400 lines)
- `comprehensive_summary_template.md` (current behavior)

---

## Agent-Specific Changes

### Requirements Analyst (Phase 1)

**Current Behavior**: Generate 40-50 pages of EARS requirements (1,587 lines)

**New Behavior (RUTHLESS PRUNING)**:
```python
if documentation_level == "minimal":
    # Store requirements in memory for test generation
    # Do NOT write any document files
    # Requirements passed via conversation context to Phase 2
    return {"requirements": parsed_requirements}

elif documentation_level == "standard":
    # STILL no document generated (markdown plan + tests are sufficient)
    # Exception: BDD mode explicitly enabled
    if mode == "bdd":
        write_requirements_doc()  # BDD needs formal requirements
    # Otherwise: NO document generated

    return {"requirements": parsed_requirements}

else:  # comprehensive
    # Current behavior: write full REQUIREMENTS-ANALYSIS.md
    write_requirements_doc()
    return {"requirements": parsed_requirements}
```

**Rationale**:
- Task description has requirements
- Tests are executable requirements (better than docs)
- Markdown plan includes key requirements
- **Nobody reads 1,587-line requirements docs after implementation**
- Only BDD mode needs formal EARS notation

### Planning Specialist (Phase 2)

**Current Behavior**: Generate 50-60 pages of implementation plan (1,750 lines)

**New Behavior (RUTHLESS PRUNING)**:
```python
# ALL MODES: Save markdown plan (lightweight, required for agents + human checkpoint)
save_plan_markdown(implementation_plan)  # ~500 lines

if documentation_level == "minimal":
    # Do NOT write verbose TDD-IMPLEMENTATION-PLAN.md
    # Markdown plan is sufficient
    return {"plan": implementation_plan}

elif documentation_level == "standard":
    # Do NOT write verbose TDD-IMPLEMENTATION-PLAN.md
    # Markdown plan is sufficient (even for complex tasks)
    return {"plan": implementation_plan}

else:  # comprehensive
    # Write verbose TDD-IMPLEMENTATION-PLAN.md (1,750 lines)
    # PLUS markdown plan (for agents)
    write_verbose_implementation_plan_doc()
    return {"plan": implementation_plan}
```

**Rationale**:
- Markdown plan (500 lines) has all essential information
- Agents read markdown plan (not verbose doc)
- Humans read markdown plan at checkpoint
- **Nobody reads 1,750-line TDD docs after code exists**
- Verbose doc is 100% redundant shelf-ware

### Architectural Reviewer (Phase 2.5B)

**Current Behavior**: Generate 25-30 pages architecture guide (665 lines)

**New Behavior (RUTHLESS PRUNING)**:
```python
# ALL MODES: Run full architectural review (quality gate)
review_result = run_full_architecture_review()

if documentation_level == "minimal":
    # Do NOT write ARCHITECTURE-GUIDE.md
    # Store scores + concise summary for embedding in final summary
    return {
        "scores": scores,  # SOLID, DRY, YAGNI numeric scores
        "summary": concise_summary  # 5-10 lines for final summary
    }

elif documentation_level == "standard":
    # Do NOT write ARCHITECTURE-GUIDE.md
    # Store scores + detailed summary for embedding in final summary
    return {
        "scores": scores,  # Full breakdown (SOLID 48/50, DRY 22/25, etc.)
        "summary": detailed_summary  # ~50 lines for Architecture Review section
    }

else:  # comprehensive
    # Write full ARCHITECTURE-GUIDE.md (665 lines)
    write_architecture_guide()
    return {"scores": scores, "guide": full_guide}
```

**Rationale**:
- Architecture review always runs (quality gate)
- Scores are what matters (embedded in summary)
- **Nobody reads 665-line standalone guides after code exists**
- Code is the truth (not architectural speculation)
- Detailed findings embedded in enhanced summary (Standard mode)

### Test Orchestrator (Phase 4)

**Current Behavior**: Generate verbose test reports across multiple phases

**New Behavior (RUTHLESS PRUNING)**:
```python
# ALL MODES: Run tests, enforce quality gates
test_result = run_full_test_suite()

if documentation_level == "minimal":
    # Do NOT write TEST-REPORT.md or phase reports
    # Store test results for embedding in final summary
    return {
        "results": test_results,  # Pass/fail counts, coverage
        "summary": concise_summary  # 5-10 lines for final summary
    }

elif documentation_level == "standard":
    # Do NOT write TEST-REPORT.md or phase reports
    # Store detailed results for embedding in final summary
    return {
        "results": test_results,  # Full breakdown
        "summary": detailed_summary  # ~30 lines for Test Results section
    }

else:  # comprehensive
    # Write full TEST-REPORT.md
    write_test_reports()
    return {"results": test_results, "reports": all_reports}
```

**Rationale**:
- Tests always run (quality gate)
- CI output shows real-time results (better than docs)
- **Nobody reads verbose test reports after tests pass**
- Terminal output or CI logs are preferred
- Summary stats embedded in final summary are sufficient

### Code Reviewer (Phase 5)

**Current Behavior**: Generate 15-20 page code review report

**New Behavior (RUTHLESS PRUNING)**:
```python
# ALL MODES: Run full code review (quality gate)
review_result = run_full_code_review()

if documentation_level == "minimal":
    # Do NOT write CODE-REVIEW-REPORT.md
    # Store score + critical issues only for final summary
    return {
        "score": score,  # Overall quality score (9.2/10)
        "issues": blocking_issues,  # Only critical/blocking issues
        "summary": concise_summary  # 3-5 lines for final summary
    }

elif documentation_level == "standard":
    # Do NOT write CODE-REVIEW-REPORT.md
    # Store score + detailed findings for embedding in final summary
    return {
        "score": score,  # Full breakdown
        "issues": all_issues,  # All findings (blocking + minor)
        "summary": detailed_summary  # ~30 lines for Code Review section
    }

else:  # comprehensive
    # Write full CODE-REVIEW-REPORT.md (15-20 pages)
    write_code_review_report()
    return {"score": score, "report": full_report}
```

**Rationale**:
- Code review always runs (quality gate)
- Score + blocking issues are what matter
- **Nobody reads 15-20 page reports after code is approved**
- Code itself is reviewed (in IDE, PR)
- Summary findings embedded in final summary are sufficient

---

## Final Summary Formats

### Minimal Summary (~200 lines)

**Filename**: `TASK-{id}-SUMMARY.md`

**Content**:
```markdown
# TASK-{id} Implementation Summary

## Overview
{one-paragraph description of what was done}

## Changes
- Modified: {file1} ({additions}+ / {deletions}-)
- Modified: {file2} ({additions}+ / {deletions}-)
- Created: {file3} ({lines} lines)

## Quality Results
- Compilation: {✅|❌} {errors} errors
- Tests: {✅|❌} {passed}/{total} passing ({percentage}%)
- Coverage: {✅|❌} {line}% line, {branch}% branch
- Architecture Review: {✅|❌} {score}/100
- Code Review: {✅|❌} {score}/10

## Key Decisions
- {decision1}
- {decision2}

## Status
- Previous: {previous_state}
- Current: {current_state}
- Duration: {actual} (estimated {estimated})
- Ready for: {next_action}

## Next Steps
1. {step1}
2. {step2}
```

### Standard Summary (~400 lines)

**Filename**: `TASK-{id}-SUMMARY.md`

**Content**: Minimal summary PLUS:
```markdown
## Architecture Review

### Scores
- SOLID Principles: {score}/50
- DRY Compliance: {score}/25
- YAGNI Balance: {score}/25
- Overall: {total}/100

### Key Findings
- {finding1}
- {finding2}

### Recommendations
- {recommendation1}
- {recommendation2}

## Implementation Plan Highlights
{if Phase 2.8 checkpoint was triggered}

- Pattern: {pattern_name}
- Approach: {approach}
- Risk Mitigation: {mitigations}

{Reference to full plan in .claude/task-plans/{id}-implementation-plan.md}

## Test Summary

### Coverage
- Line: {line}% ({covered}/{total} lines)
- Branch: {branch}% ({covered}/{total} branches)

### Test Breakdown
- {TestClass1}: {passed}/{total} tests
- {TestClass2}: {passed}/{total} tests

### Fix Loop
- Attempts: {attempts}
- Final Status: {✅ All passing}
```

### Comprehensive Summary (Current Behavior)

Multiple standalone documents (150-200 pages total):
- REQUIREMENTS-ANALYSIS.md
- TDD-IMPLEMENTATION-PLAN.md
- ARCHITECTURE-GUIDE.md
- COMPLETION-REPORT.md
- Quick Reference, Executive Summary, Visual Guide, etc.

---

## Migration Strategy

### Phase 1: Add Configuration Support (Week 1)

**Tasks**:
1. Add `documentation` section to `.claude/settings.json` schema
2. Update settings validation
3. Add `--docs` flag parsing to task-work command
4. Implement decision tree logic
5. Update CLAUDE.md documentation

**Testing**:
- Verify flag override works
- Verify settings.json default works
- Verify complexity fallback works

### Phase 2: Update Agent Prompts (Week 1-2)

**Tasks**:
1. Add documentation level awareness to all agents
2. Update each agent's output logic (minimal/standard/comprehensive)
3. Test each agent in isolation

**Testing**:
- Run test tasks with each documentation level
- Verify output matches specification

### Phase 3: Implement Consolidated Reporting (Week 2)

**Tasks**:
1. Create `lib/documentation_generator.py`
2. Implement templates (minimal, standard, comprehensive)
3. Update task-work to use consolidated reporting
4. Remove redundant phase reports

**Testing**:
- Compare output quality across levels
- Verify all necessary information preserved
- Measure time/token savings

### Phase 4: Rollout & Metrics (Week 3)

**Tasks**:
1. Update all templates with documentation defaults
2. Update documentation and examples
3. Monitor task execution metrics
4. Gather user feedback

**Success Metrics**:
- Simple task duration: <15 minutes (target)
- Medium task duration: <25 minutes (target)
- User satisfaction: High (maintain current quality rating)
- Token usage: 60-70% reduction for simple tasks

---

## Testing Plan

### Test Cases

#### TC-1: Flag Override (Minimal)
```bash
/task-work TASK-COMPLEX --docs=minimal
```
**Expected**: TASK-COMPLEX (complexity 8) uses minimal docs despite high complexity

#### TC-2: Flag Override (Comprehensive)
```bash
/task-work TASK-SIMPLE --docs=comprehensive
```
**Expected**: TASK-SIMPLE (complexity 2) uses comprehensive docs despite low complexity

#### TC-3: Settings Default (Minimal)
```json
{"documentation": {"default_level": "minimal"}}
```
```bash
/task-work TASK-MEDIUM
```
**Expected**: TASK-MEDIUM (complexity 5) uses minimal docs (settings override)

#### TC-4: Settings Default (Standard)
```json
{"documentation": {"default_level": "standard"}}
```
```bash
/task-work TASK-SIMPLE
```
**Expected**: TASK-SIMPLE (complexity 2) uses standard docs (settings override)

#### TC-5: Complexity Fallback (Simple → Minimal)
```json
{"documentation": {"default_level": "auto"}}
```
```bash
/task-work TASK-SIMPLE
```
**Expected**: TASK-SIMPLE (complexity 2) uses minimal docs (complexity rule)

#### TC-6: Complexity Fallback (Medium → Standard)
```bash
/task-work TASK-MEDIUM
```
**Expected**: TASK-MEDIUM (complexity 5) uses standard docs (complexity rule)

#### TC-7: Complexity Fallback (High → Standard)
```bash
/task-work TASK-COMPLEX
```
**Expected**: TASK-COMPLEX (complexity 8) uses standard docs (NEW RULE)

#### TC-8: Quality Gates Unchanged
```bash
/task-work TASK-ANY --docs=minimal
```
**Expected**: All quality gates run, scores recorded, tests must pass

---

## Documentation Updates Required

### 1. CLAUDE.md
- Add documentation levels overview
- Add --docs flag documentation
- Add settings.json documentation section
- Update examples

### 2. docs/guides/agentecflow-lite-workflow.md
- Add documentation levels explanation
- Add recommended defaults
- Add override examples

### 3. installer/global/commands/task-work.md
- Add --docs flag specification
- Add configuration hierarchy
- Add decision tree diagram

### 4. All Templates
- Add documentation defaults to template settings.json files
- Recommend "auto" for most projects

---

## Risks & Mitigations

### Risk 1: Users Miss Important Architecture Info

**Concern**: Minimal mode omits architecture guide

**Mitigation**:
- Architecture review still runs (scores preserved)
- Key findings embedded in summary
- Can regenerate with `/task-docs TASK-XXX --architecture` (future enhancement)
- Medium/high complexity defaults to standard (includes architecture)

### Risk 2: Incomplete Audit Trail

**Concern**: Compliance requirements need comprehensive docs

**Mitigation**:
- Comprehensive mode available via flag or settings
- Enterprise projects can set `default_level: "comprehensive"`
- All quality gates still run (data preserved)
- Git commit messages capture decisions

### Risk 3: Confusion About Which Level to Use

**Concern**: Users won't know when to override

**Mitigation**:
- Intelligent defaults work for 90% of cases
- Clear documentation with examples
- Simple rule: "trust the default unless you need audit trail"
- Flag is optional (not required)

---

## Success Criteria

### Performance Targets (UPDATED - RUTHLESS PRUNING)

| Metric | Current | Target (Minimal) | Target (Standard) | Improvement |
|--------|---------|------------------|-------------------|-------------|
| Simple task duration | 36 min | 8-10 min | 12-15 min | 67-78% faster |
| Medium task duration | 36 min | 10-12 min | 15-18 min | 50-72% faster |
| Complex task duration | 36 min | 12-15 min | 18-22 min | 39-67% faster |
| Simple task tokens | 500k | 100-120k | 150-200k | 76-80% reduction |
| Medium task tokens | 500k | 120-150k | 200-250k | 50-76% reduction |
| Complex task tokens | 500k | 150-200k | 250-300k | 40-70% reduction |
| Files generated | 13+ | 2 | 2 | 85% reduction |
| Documentation size | 210KB | 15KB | 30KB | 86-93% reduction |

**Key Improvements (vs original targets)**:
- **More aggressive**: Ruthless pruning enables 67-78% time savings (vs 50-70% originally)
- **Token efficiency**: 76-80% reduction for simple tasks (vs 60-70% originally)
- **File count**: 85% reduction (2 files vs 13+)
- **Maintained quality**: All quality gates still run, 0% information loss

### Quality Targets (Must Not Degrade)

| Metric | Current | Target |
|--------|---------|--------|
| Test pass rate | 100% | 100% |
| Architecture review score | ≥90/100 | ≥90/100 |
| Code review score | ≥9/10 | ≥9/10 |
| Regression rate | <1% | <1% |

### User Satisfaction

- "Output quality": Maintain HIGH
- "Execution speed": Increase to HIGH
- "Documentation usefulness": Increase to HIGH
- "Ease of use": Maintain HIGH

---

## Conclusion

This specification provides a **pragmatic approach** to documentation levels:

1. **Fast by default** for simple tasks (minimal)
2. **Balanced approach** for medium/complex tasks (standard)
3. **Full audit trail** available when needed (comprehensive via flag)
4. **User control** via configuration hierarchy (flag > config > complexity)
5. **No quality compromise** (all gates still run)

**Expected Impact**:
- 35-70% time savings across task complexity spectrum
- 30-70% token savings
- Maintained code quality
- Improved competitive position
- User flexibility

**Ready for**: TASK creation and implementation

---

## Appendix: Example Outputs

### Example 1: Simple Bug Fix (Minimal)

**Command**:
```bash
/task-work TASK-047
# Complexity: 2/10 → Auto-selects MINIMAL
```

**Output**: Single file `TASK-047-SUMMARY.md` (~200 lines)

**Duration**: ~12 minutes (67% faster)
**Tokens**: ~150k (70% reduction)

---

### Example 2: Medium Refactoring (Standard)

**Command**:
```bash
/task-work TASK-065
# Complexity: 5/10 → Auto-selects STANDARD
```

**Output**:
- `TASK-065-SUMMARY.md` (~400 lines, includes architecture summary)
- `.claude/task-plans/TASK-065-implementation-plan.md` (if checkpoint triggered)

**Duration**: ~20 minutes (44% faster)
**Tokens**: ~300k (40% reduction)

---

### Example 3: Complex Architecture (Standard with Override)

**Command**:
```bash
/task-work TASK-100
# Complexity: 8/10 → Auto-selects STANDARD

# Override for audit:
/task-work TASK-100 --docs=comprehensive
```

**Output (Standard)**:
- Same as Example 2

**Output (Comprehensive)**:
- All current documents (13+ files, 150-200 pages)

**Duration**:
- Standard: ~24 minutes (33% faster)
- Comprehensive: ~36 minutes (current behavior)

---

## Next Steps for Implementation

1. **Review & Approve** this specification
2. **Create TASK** for implementation
3. **Assign priority** (recommend HIGH for open source competitiveness)
4. **Implement Phase 1** (configuration support)
5. **Test & Iterate** based on real usage
6. **Roll out** to all templates


---

## Summary of Changes (User Feedback Integrated)

### What Changed Based on User Input

**User Insight #1**: "I agree I only ever read the implementation summary or the plan if at a checkpoint"

**Action Taken**:
- ❌ Deleted ALL verbose standalone documentation (requirements, guides, reports)
- ✅ Kept ONLY what users actually read:
  1. Implementation summary (what you love)
  2. Markdown plan (for checkpoint review)

**User Insight #2**: "Do we even need the TDD document if it's only read by humans after work is done?"

**Action Taken**:
- ❌ Deleted verbose TDD plan (1,750 lines) from Minimal/Standard modes
- ✅ Kept lightweight markdown plan (500 lines) for agents + human checkpoint
- **Rationale**: Code is better documentation than stale plans

**User Insight #3**: "Documentation forms shared memory for agent collaboration"

**Action Taken**:
- ✅ Preserved markdown plan (agents read this for Phase 2.5B, 5.5)
- ✅ Preserved conversation context (main agent memory)
- ❌ Deleted verbose docs (0 agents read these)
- **Result**: Agent collaboration 100% functional, 80% less documentation

### Final Documentation Strategy

**Minimal Mode (Complexity 1-3)**:
- 2 files: Summary + Markdown plan
- 8-10 minutes execution
- 100-120k tokens
- **What you read**: Summary (2-3 min)

**Standard Mode (Complexity 4-10) - DEFAULT**:
- 2 files: Enhanced summary + Markdown plan
- 12-18 minutes execution
- 150-250k tokens
- **What you read**: Summary (5-10 min), Plan at checkpoint (5-10 min)

**Comprehensive Mode (--docs=comprehensive)**:
- 13+ files: Everything
- 36+ minutes execution
- 500k+ tokens
- **When to use**: Compliance, audit, training (rare)

### Performance Impact

| Metric | Before | After (Standard) | Savings |
|--------|--------|------------------|---------|
| Duration | 36 min | 12-18 min | 50-67% |
| Tokens | 500k | 150-250k | 50-70% |
| Files | 13+ | 2 | 85% |
| Read by humans | 1 file | 2 files | Same (but both valuable) |
| Read by agents | 1 file | 1 file | Same |

### Philosophy

**Before**: Document everything "just in case"  
**After**: Document only what's read (code is documentation)

**Principle**: **If nobody reads it, delete it.**

---

**Status**: Specification complete (RUTHLESSLY PRUNED)  
**Impact**: 67-78% time savings, 76-80% token savings, 0% quality loss  
**Agent Collaboration**: Fully preserved (markdown plan + conversation context)  
**Recommendation**: Proceed with implementation immediately

