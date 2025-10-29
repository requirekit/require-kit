# Documentation Levels - Executive Summary

**Date**: 2025-10-29
**Status**: Ready for Task Creation
**Priority**: HIGH (Open source competitive positioning)

---

## The Problem

Tasks currently take **5-7 hours** with **80% of time spent on verbose documentation**:
- 62 documentation files (2.3MB) for recent tasks
- 150-200 pages per task
- 500k+ tokens per task
- **2-3x slower than BMAD/SpecKit/OpenSpec**

---

## The Solution

**3-tier documentation system** with intelligent defaults:

### Tier 1: Minimal
- **Output**: Single summary (~200 lines)
- **Time**: ~12 minutes (67% faster)
- **Tokens**: ~150k (70% reduction)
- **Default for**: Complexity 1-3 (simple tasks)

### Tier 2: Standard ⭐ (DEFAULT for most tasks)
- **Output**: Summary + architecture review (~400 lines)
- **Time**: ~20 minutes (44% faster)
- **Tokens**: ~300k (40% reduction)
- **Default for**: Complexity 4-10 (medium/high tasks)

### Tier 3: Comprehensive
- **Output**: All current documentation (150-200 pages)
- **Time**: ~36 minutes (current behavior)
- **Tokens**: ~500k (current behavior)
- **Available via**: `--docs=comprehensive` flag (for audit/compliance)

---

## Configuration Hierarchy

```
1. Command-line flag    --docs=minimal|standard|comprehensive  (highest priority)
   ↓
2. Settings file        .claude/settings.json: "default_level"  (project preference)
   ↓
3. Complexity rules     1-3: Minimal, 4-10: Standard            (intelligent fallback)
```

---

## Key Design Decisions

### 1. Standard is the New Default (Updated per User Feedback)

**Original proposal**: Complexity 7-10 → Comprehensive
**Updated approach**: Complexity 4-10 → Standard

**Rationale**:
- Architecture review still runs (provides visibility)
- Reporting is streamlined (not verbose)
- Users can override to Comprehensive via flag when needed
- Better balance of speed + quality for complex tasks

### 2. Configuration in settings.json

**Location**: `.claude/settings.json`

**New section**:
```json
{
  "documentation": {
    "default_level": "auto",
    "preferences": {
      "generate_ears_requirements": "auto",
      "generate_implementation_plan": true,
      "consolidate_phase_reports": true
    }
  }
}
```

**Values**:
- `"auto"`: Use complexity rules (1-3: Minimal, 4-10: Standard)
- `"minimal"`: Always minimal (fast)
- `"standard"`: Always standard (balanced)
- `"comprehensive"`: Always comprehensive (audit)

### 3. Flag Overrides Everything

**Examples**:
```bash
# Trust the defaults (uses complexity rules)
/task-work TASK-065

# Override to minimal for speed
/task-work TASK-065 --docs=minimal

# Override to comprehensive for audit
/task-work TASK-065 --docs=comprehensive
```

---

## What You Keep (High-Value Output)

### Minimal Mode
✅ Implementation summary (the one you love!)
✅ Quality gate results
✅ Test pass/fail counts
✅ Files changed
✅ Next steps

### Standard Mode (Default for 4-10 complexity)
✅ Everything in Minimal, PLUS:
✅ Architecture review scores & summary
✅ Complexity evaluation rationale
✅ Implementation plan (saved to `.claude/task-plans/`)
✅ Key architectural decisions

### Comprehensive Mode (Available via flag)
✅ Everything in Standard, PLUS:
✅ EARS requirements (40-50 pages)
✅ Verbose architecture guides
✅ Phase-by-phase reports
✅ Complete audit trail

---

## What Gets Removed (Low-Value Duplication)

### Minimal Mode Removes:
❌ EARS requirements docs (stored in memory, not written)
❌ Verbose implementation plans (plan data preserved)
❌ Architecture guide documents (summary only)
❌ Phase-by-phase reports (single final summary)
❌ Redundant summaries (Quick Ref, Executive Summary, etc.)
❌ Test specification docs (tests are the spec)

### Standard Mode Removes:
❌ EARS requirements (unless BDD mode)
❌ Verbose standalone guides
❌ Phase-by-phase reports
❌ Redundant summaries

---

## Quality Gates (UNCHANGED)

**All modes run the same quality checks**:
- ✅ Compilation (100% required)
- ✅ Tests (100% pass required)
- ✅ Coverage (≥80% line, ≥75% branch)
- ✅ Architecture review (scored)
- ✅ Code review (scored)
- ✅ Fix loop (up to 3 attempts)

**What changes**: Only the verbosity of reporting, not the gates themselves.

---

## Expected Performance Improvements

| Complexity | Current | Minimal | Standard | Comprehensive |
|------------|---------|---------|----------|---------------|
| 1-3 (Simple) | 6 hours | 2 hours ⚡ | 3 hours | 6 hours |
| 4-6 (Medium) | 6 hours | 2.5 hours | 3 hours ⚡ | 6 hours |
| 7-10 (Complex) | 6 hours | 3 hours | 4 hours ⚡ | 6 hours |

⚡ = Default for that complexity level

**Token Savings**:
- Minimal: 70% reduction (500k → 150k)
- Standard: 40% reduction (500k → 300k)
- Comprehensive: No change (500k)

---

## Competitive Positioning

### Before
- **Agentecflow**: 6 hours, 500k tokens
- **BMAD**: 2-3 hours, 150k tokens ⚡ (faster)
- **SpecKit**: 3-4 hours, 200k tokens ⚡ (faster)

### After (with optimizations)
- **Agentecflow** (Minimal): 2 hours, 150k tokens ⚡ (on par)
- **Agentecflow** (Standard): 3-4 hours, 300k tokens ⚡ (on par)
- **BMAD/SpecKit**: 2-4 hours, 150-200k tokens
- **Advantage**: Same speed + superior quality gates

---

## Implementation Phases

### Phase A: Core Implementation (Week 1) 🎯
1. Add `--docs` flag parsing
2. Add settings.json configuration
3. Update agent prompts for doc level awareness
4. Implement consolidated reporting
5. Update documentation

**Deliverable**: Working 3-tier system

### Phase B: Polish & Preferences (Week 2)
1. Add granular preferences (EARS, architecture guides, etc.)
2. Template-based report generation
3. Update all stack templates
4. User testing & feedback

**Deliverable**: Production-ready system

### Phase C: Advanced Features (Week 3+)
1. On-demand doc generation (`/task-docs TASK-XXX --full`)
2. Documentation budgets
3. Usage metrics tracking
4. Auto-optimization

**Deliverable**: Adaptive system

---

## Example Usage Scenarios

### Scenario 1: Fast Bug Fix
```bash
/task-work TASK-047
# Complexity: 2/10
# Auto-selects: MINIMAL
# Duration: ~12 min
# Output: Single summary file
```

### Scenario 2: Medium Refactoring
```bash
/task-work TASK-065
# Complexity: 5/10
# Auto-selects: STANDARD
# Duration: ~20 min
# Output: Summary + architecture review
```

### Scenario 3: Complex Architecture (Speed)
```bash
/task-work TASK-100
# Complexity: 8/10
# Auto-selects: STANDARD
# Duration: ~24 min
# Output: Summary + architecture review
```

### Scenario 4: Complex Architecture (Audit)
```bash
/task-work TASK-100 --docs=comprehensive
# Complexity: 8/10
# Override to: COMPREHENSIVE
# Duration: ~36 min
# Output: Full audit trail (current behavior)
```

### Scenario 5: Project-Wide Speed Focus
```json
// .claude/settings.json
{
  "documentation": {
    "default_level": "minimal"
  }
}
```
```bash
/task-work TASK-ANY
# All tasks use MINIMAL by default
# Override with --docs=standard or --docs=comprehensive if needed
```

---

## Risk Mitigation

### Risk: Loss of Architecture Visibility
**Mitigation**:
- Complexity 4-10 defaults to **Standard** (includes architecture)
- Architecture review always runs (scores preserved)
- Can override to Comprehensive via flag

### Risk: Incomplete Audit Trail
**Mitigation**:
- Comprehensive mode always available via flag
- Enterprise projects can set `default_level: "comprehensive"`
- All quality gates still run (data preserved)

### Risk: User Confusion
**Mitigation**:
- Intelligent defaults (90% of users never need to think about it)
- Clear documentation with examples
- Simple override: `--docs=comprehensive` when needed

---

## Success Metrics

### Performance (Target)
- ✅ Simple tasks: <15 minutes (currently 36 min)
- ✅ Medium tasks: <25 minutes (currently 36 min)
- ✅ Complex tasks: <30 minutes (currently 36+ min)
- ✅ Token reduction: 30-70% depending on complexity

### Quality (Must Not Degrade)
- ✅ Test pass rate: 100% (same)
- ✅ Architecture review: ≥90/100 (same)
- ✅ Code review: ≥9/10 (same)
- ✅ Regression rate: <1% (same)

### User Satisfaction (Target)
- ✅ "Output quality": HIGH (maintain)
- ✅ "Execution speed": HIGH (improve from MEDIUM)
- ✅ "Documentation usefulness": HIGH (improve from MEDIUM)
- ✅ "Ease of use": HIGH (maintain)

---

## Next Steps

### 1. Review Documents
- ✅ [TASK-DOCUMENTATION-PERFORMANCE-ANALYSIS.md](TASK-DOCUMENTATION-PERFORMANCE-ANALYSIS.md) - Full analysis with metrics
- ✅ [DOCUMENTATION-LEVELS-SPECIFICATION.md](DOCUMENTATION-LEVELS-SPECIFICATION.md) - Complete implementation spec

### 2. Create Implementation Task
Use `/task-create` with the specification document to create a formal task:

**Suggested Title**: "Implement Documentation Levels for task-work Command"

**Suggested Complexity**: 6/10 (medium - multiple components but clear design)

**Suggested Subtasks**:
- TASK-XXX-1: Add flag parsing and settings schema
- TASK-XXX-2: Update agent prompts for doc level awareness
- TASK-XXX-3: Implement consolidated reporting
- TASK-XXX-4: Update documentation and templates
- TASK-XXX-5: Testing and validation

### 3. Implementation
- Execute Phase A (core functionality)
- Test with real tasks across complexity spectrum
- Measure performance improvements
- Gather user feedback

### 4. Rollout
- Update all templates with documentation defaults
- Update main CLAUDE.md with new feature
- Announce to users
- Monitor metrics

---

## Key Takeaways

1. **Default = Standard for 4-10 complexity** (balanced approach)
2. **Configuration hierarchy** gives users full control
3. **Quality unchanged** (all gates still run)
4. **33-67% faster** across complexity spectrum
5. **Competitive with alternatives** while maintaining superior quality
6. **Implementation summary preserved** (the output you love)
7. **Comprehensive mode always available** (for audit/compliance)

---

**Status**: Ready for task creation and implementation
**Expected Impact**: Significant improvement in execution speed without sacrificing quality
**User Benefit**: Fast by default, comprehensive when needed, quality always maintained

