# Backlog Implementation Order - require-kit

**Date**: 2025-11-01
**Context**: Post-REQ-002 cleanup - Repository now focuses exclusively on requirements management

## Summary

After analyzing all 10 backlog tasks, here's the recommended implementation order based on:
- Dependencies between tasks
- Impact on core functionality
- Complexity and effort required
- Current state of the repository (post-REQ-002 cleanup)
- Alignment with require-kit's focus (requirements management)

## High Priority Tasks (Do First)

### 1. TASK-019: Add Concise Mode to EARS Formalization ⭐
**Priority**: HIGH | **Effort**: 2-3 hours | **Complexity**: 3/10

**Why First:**
- Low complexity, high impact
- No dependencies
- Directly improves core requirements gathering functionality
- Reduces token usage by 50-70%
- Addresses verbose specifications problem
- Can be completed quickly for immediate value

**Implementation:**
- Add `--concise` flag to `/formalize-ears` command
- Enforce 500-word limit per requirement
- Update requirements-analyst agent with concise guidelines
- Create validation logic for word count

**Dependencies**: None

**Related**: TASK-021 (versioning), TASK-022 (templates)

---

### 2. TASK-033: Rebrand to dev-tasker ⚠️
**Priority**: HIGH | **Effort**: 2-4 hours | **Complexity**: 3/10

**Why Second:**
- **IMPORTANT NOTE**: This task is mostly IRRELEVANT to require-kit post-REQ-002
- After REQ-002, require-kit no longer contains task execution features
- This task was written before the split
- Most references to "agentecflow init" and "dev-tasker" are in code that was deleted

**Recommendation**:
- **ARCHIVE or SKIP** this task for require-kit
- This task belongs in the taskwright repository (the task execution system)
- require-kit should focus on requirements commands only

**Current Action**: Review and likely archive this task

---

### 3. REQ-003: Create Shared Installer Strategy ⭐⭐⭐
**Priority**: HIGH | **Effort**: 5 hours | **Complexity**: 6/10

**Why Third:**
- Critical infrastructure task
- Enables standalone installation of require-kit
- Allows optional integration with taskwright
- Required before any distribution or wider use
- Well-specified with clear subtasks (REQ-003A, REQ-003B, REQ-003C)

**Implementation:**
- REQ-003A: Update require-kit installer (2 hours)
- REQ-003B: Update taskwright installer (2 hours) - NOT in this repo
- REQ-003C: Test combined installation (1 hour)

**Dependencies**: None (can be done immediately)

**Critical**: This is the foundation for distributing require-kit as a standalone tool

---

## Medium Priority Tasks (Do Next)

### 4. TASK-022: Create Spec Templates by Task Type
**Priority**: MEDIUM | **Effort**: 6-8 hours | **Complexity**: 5/10

**Why Fourth:**
- Builds on TASK-019 (concise mode)
- Provides specialized templates for different requirement types
- Medium complexity, medium effort
- Good value for improving requirements gathering

**Implementation:**
- Create 6 specialized templates (bug-fix, feature, refactor, docs, performance, security)
- Update gather-requirements command
- Different word limits per template type

**Dependencies**: None (but pairs well with TASK-019)

**Related**: TASK-019 (concise mode)

---

### 5. TASK-021: Implement Requirement Versioning System
**Priority**: MEDIUM | **Effort**: 8-10 hours | **Complexity**: 6/10

**Why Fifth:**
- Important for iterative requirements refinement
- Required by TASK-023 (regeneration)
- Medium-high complexity
- Adds significant value to requirements management

**Implementation:**
- Create version data model
- Build `/refine-requirements` command
- Version history storage (JSON)
- Task linkage to specific requirement versions

**Dependencies**: None (but enables TASK-023)

**Blocks**: TASK-023 (spec regeneration)

---

## Low Priority Tasks (Do Later)

### 6. TASK-023: Implement Spec Regeneration Command
**Priority**: LOW | **Effort**: 16-20 hours | **Complexity**: 8/10

**Why Sixth:**
- **HIGH COMPLEXITY** (8/10) - Most complex task in backlog
- Requires TASK-021 to be completed first (versioning dependency)
- High effort (16-20 hours)
- "Spec-as-source" is advanced feature
- Should be split into 2 subtasks
- **NOTE**: This task references task execution features deleted in REQ-002

**Recommendation**:
- **DEFER** until TASK-021 is complete
- Consider if this belongs in taskwright instead of require-kit
- May need significant rework post-REQ-002 cleanup

**Dependencies**: TASK-021 (BLOCKING - must be done first)

---

### 7. TASK-024: Add Compliance Scorecard to Task Completion
**Priority**: LOW | **Effort**: 12-16 hours | **Complexity**: 7/10

**Why Seventh:**
- **IRRELEVANT** to require-kit post-REQ-002
- This task is about `/task-complete` command
- Task completion is part of task execution (deleted in REQ-002)
- High complexity, high effort

**Recommendation**:
- **ARCHIVE or MOVE** to taskwright repository
- This is NOT a requirements management feature
- Does not belong in require-kit

---

### 8. TASK-034: Enhance Phase 2.8 with Business Decision Detection
**Priority**: LOW | **Effort**: 4-6 hours | **Complexity**: 6/10

**Why Eighth:**
- **IRRELEVANT** to require-kit post-REQ-002
- This task references `/task-work` workflow phases
- Task execution workflow was deleted in REQ-002
- References architectural reviewers and execution agents (deleted)

**Recommendation**:
- **ARCHIVE or MOVE** to taskwright repository
- This is NOT a requirements management feature
- Does not belong in require-kit

---

### 9. TASK-035: Implement Documentation Levels for task-work
**Priority**: N/A | **Status**: NOT APPLICABLE

**Why Not Applicable:**
- **BELONGS IN TASKWRIGHT** repository, not require-kit
- TASK-035 targets the `/task-work` execution workflow (owned by taskwright)
- Designed for 7 execution agents (architectural-reviewer, test-orchestrator, code-reviewer, etc.)
- require-kit only has 2 agents (requirements-analyst, bdd-generator) for requirements gathering
- **Architecture**: taskwright = execution, require-kit = requirements/inputs

**Corrected Understanding**:
After reviewing `/task-work` documentation, the architecture is:
- **taskwright**: Owns task execution workflow (/task-work, quality gates, testing)
- **require-kit**: Provides inputs (EARS requirements, BDD scenarios, epic/feature hierarchy)
- **Integration**: taskwright reads from require-kit when both installed

**What require-kit Actually Needs**:
- **EARS verbosity** → Already covered by **TASK-019** (Concise Mode)
- **BDD verbosity** → Optionally create new small task for `/generate-bdd` (30-45 min)

**Recommendation**:
- **REMOVE from require-kit backlog** - This task belongs in taskwright repository
- **Focus on TASK-019 instead** - Already addresses require-kit's verbosity concerns
- **See**: TASK-035-CORRECTED-ANALYSIS.md for detailed explanation

---

### 10. TASK-MOCK-001
**Priority**: N/A | **Status**: Unknown

**Recommendation**: Review and determine relevance

---

## Recommended Implementation Sequence

### Phase 1: Core Improvements (Immediate - 1 week)
1. ✅ **REQ-002**: Delete Agentecflow Features (COMPLETED)
2. ⭐ **TASK-019**: Concise Mode (2-3 hours) - Quick win
3. ⭐⭐⭐ **REQ-003**: Shared Installer (5 hours) - Critical infrastructure

**Total Effort**: ~7-8 hours
**Impact**: High - Makes require-kit installable and improves core functionality

---

### Phase 2: Enhanced Requirements Features (Next - 2 weeks)
4. **TASK-022**: Spec Templates (6-8 hours) - Specialized templates
5. **TASK-021**: Requirement Versioning (8-10 hours) - Enables refinement

**Total Effort**: ~14-18 hours
**Impact**: Medium-High - Significantly improves requirements management

---

### Phase 3: Advanced Features (Future - 3-4 weeks)
6. **TASK-023**: Spec Regeneration (16-20 hours) - Advanced spec-as-source
   - **Note**: Requires rework post-REQ-002, may belong in taskwright

**Total Effort**: ~16-20 hours
**Impact**: Medium - Advanced feature, needs reconsideration

---

### Phase 4: Archive/Move to taskwright
7-9. **Archive These Tasks** (not relevant to require-kit):
   - TASK-024: Compliance Scorecard (task execution feature)
   - TASK-034: Phase 2.8 Enhancement (task execution feature)
   - TASK-035: Documentation Levels (task execution feature)
   - TASK-033: Rebrand to dev-tasker (mostly obsolete post-REQ-002)

**Action**: Move to taskwright repository or archive

---

## Task Categorization by Relevance

### ✅ KEEP in require-kit (Requirements Management)
- **TASK-019**: Concise Mode ⭐ **[SOLVES VERBOSITY PROBLEM]**
- **TASK-021**: Requirement Versioning ⭐
- **TASK-022**: Spec Templates ⭐
- **REQ-003**: Shared Installer ⭐⭐⭐

### ❌ MOVE to taskwright (Task Execution)
- **TASK-024**: Compliance Scorecard
- **TASK-034**: Phase 2.8 Enhancement
- **TASK-035**: Documentation Levels **[BELONGS IN TASKWRIGHT - NOT REQUIRE-KIT]**

### ⚠️ NEEDS REVIEW
- **TASK-023**: Spec Regeneration (may belong in taskwright)
- **TASK-033**: Rebrand to dev-tasker (mostly obsolete)
- **TASK-MOCK-001**: Unknown status

### 📝 OPTIONAL NEW TASK
- **TASK-037**: Add --docs flag to /generate-bdd (30-45 min)
  - Only if BDD scenario verbosity becomes a problem
  - Simple: 1 agent, 1 command
  - Lower priority than TASK-019

---

## Dependencies Graph

```
TASK-019 (Concise Mode)
  ↓ [pairs with]
TASK-022 (Spec Templates)

REQ-003 (Shared Installer) [standalone - critical]

TASK-021 (Requirement Versioning)
  ↓ [blocks]
TASK-023 (Spec Regeneration) [needs review]

TASK-024, TASK-034, TASK-035 [move to taskwright]
```

---

## Immediate Action Plan

### Week 1: Foundation
1. ✅ Complete REQ-002 (DONE)
2. Implement TASK-019: Concise Mode (2-3 hours)
3. Implement REQ-003: Shared Installer (5 hours)

### Week 2-3: Core Features
4. Implement TASK-022: Spec Templates (6-8 hours)
5. Implement TASK-021: Requirement Versioning (8-10 hours)

### Week 4: Cleanup & Review
6. Archive/Move irrelevant tasks (TASK-024, TASK-034, TASK-035, TASK-033)
7. Review TASK-023 for post-REQ-002 relevance
8. Plan next iteration

---

## Success Metrics

### After Phase 1 (Week 1)
- ✅ require-kit installable standalone
- ✅ 50-70% reduction in token usage (concise mode)
- ✅ Clean separation from taskwright

### After Phase 2 (Week 2-3)
- ✅ 6 specialized requirement templates available
- ✅ Requirement versioning and refinement workflow
- ✅ Improved requirements gathering experience

---

## Notes

1. **Post-REQ-002 Impact**: Many tasks (TASK-024, TASK-034, TASK-035) are now irrelevant because they reference deleted features
2. **Repository Focus**: require-kit is now ONLY about requirements management (EARS, BDD, epic/feature hierarchy)
3. **Integration Model**: require-kit provides inputs (requirements, BDD scenarios) → taskwright handles execution
4. **Architecture Clarity**: taskwright owns /task-work execution workflow, require-kit provides requirements
5. **Verbosity Solution**: TASK-019 (Concise Mode) solves the verbosity problem that TASK-035 was meant to address
6. **Critical Path**: REQ-003 (installer) is critical for distribution
7. **Quick Wins**: TASK-019 provides immediate value with minimal effort

---

## Recommendation Summary

**Start with:**
1. TASK-019 (Concise Mode) - 2-3 hours - Quick win
2. REQ-003 (Shared Installer) - 5 hours - Critical infrastructure

**Then proceed with:**
3. TASK-022 (Spec Templates) - 6-8 hours
4. TASK-021 (Requirement Versioning) - 8-10 hours

**Archive/Move these:**
- TASK-024, TASK-034, TASK-035 → Move to taskwright repository
- TASK-033 → Archive (obsolete post-REQ-002)
- TASK-023 → Review for relevance post-REQ-002

**Total Realistic Backlog**: 4 tasks (~21-26 hours of work)
**Total Tasks to Archive/Move**: 5 tasks

**Key Correction**: TASK-035 is NOT about require-kit's agents getting documentation levels. It's about taskwright's /task-work execution workflow. TASK-019 (Concise Mode) already solves require-kit's verbosity concerns.

---

**Prepared by**: Claude Code
**Date**: 2025-11-01
**Context**: Post-REQ-002 cleanup analysis
