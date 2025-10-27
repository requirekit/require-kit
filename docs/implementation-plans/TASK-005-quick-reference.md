# TASK-005: Quick Reference - Revised Architecture

## At a Glance

**Status**: Revised to address architectural review
**Complexity**: Medium (down from High)
**Estimated Time**: 4-5 hours (down from 6-8 hours)
**LOC**: ~310 (down from ~800)

## Key Changes from Original

| Aspect | Before | After | Impact |
|--------|--------|-------|--------|
| Classes | 6+ | 3 | 50% reduction |
| LOC | ~800 | ~310 | 61% reduction |
| DRY Compliance | ❌ Violated | ✓ Compliant | Critical fix |
| Time Estimate | 6-8h | 4-5h | 38% savings |

## Architecture Summary

```
Requirements Text
    ↓
UpfrontComplexityAdapter (NEW)
    ↓
ComplexityCalculator (REUSED from TASK-003A)
    ↓
TaskSplitAdvisor (NEW)
    ↓
SplitRecommendation (NEW)
```

## File Structure

### New Files (TASK-005)
```
installer/global/commands/lib/
├── upfront_complexity_adapter.py   # ~100 LOC - Adapter pattern
├── task_split_advisor.py           # ~80 LOC - Split logic
├── split_models.py                 # ~30 LOC - Data model
└── upfront_complexity_cli.py       # ~90 LOC - CLI handler

installer/global/commands/
└── upfront-complexity-check.sh     # ~10 LOC - Bash bridge

tests/
├── test_upfront_complexity_adapter.py      # ~100 LOC
├── test_task_split_advisor.py              # ~60 LOC
└── test_upfront_complexity_integration.py  # ~40 LOC
```

### Reused Files (TASK-003A)
```
installer/global/commands/lib/
├── complexity_calculator.py        # ~350 LOC - REUSED ✓
├── complexity_models.py            # ~225 LOC - REUSED ✓
└── complexity_factors.py           # ~265 LOC - REUSED ✓

tests/
├── test_complexity_calculator.py   # ~200 LOC - REUSED ✓
└── test_complexity_factors.py      # ~200 LOC - REUSED ✓
```

## Component Responsibilities

### 1. UpfrontComplexityAdapter
**Purpose**: Convert requirements → complexity score
**Pattern**: Adapter pattern
**Dependencies**: ComplexityCalculator (TASK-003A)

**Key Methods**:
- `evaluate_requirements()` - Main entry point
- `_estimate_files()` - File count heuristics
- `_detect_patterns()` - Pattern keywords
- `_detect_risks()` - Risk keywords

### 2. TaskSplitAdvisor
**Purpose**: Generate split recommendations
**Pattern**: Simple function-oriented
**Dependencies**: ComplexityScore (TASK-003A)

**Key Methods**:
- `recommend_split()` - Main entry point (threshold: score >= 7)
- `_suggest_vertical_splits()` - By feature
- `_suggest_horizontal_splits()` - By layer
- `_suggest_risk_based_splits()` - By risk

### 3. SplitRecommendation
**Purpose**: Data model for recommendations
**Pattern**: Immutable dataclass
**Dependencies**: ComplexityScore (TASK-003A)

**Fields**:
- `should_split: bool`
- `recommended_task_count: int`
- `split_strategy: str`
- `suggested_splits: List[str]`
- `reasoning: str`

## Implementation Phases

### Phase 1: Adapter Layer (1.5h)
- [x] Design approved
- [ ] Implement UpfrontComplexityAdapter
- [ ] File estimation heuristics
- [ ] Pattern detection keywords
- [ ] Risk detection keywords
- [ ] Unit tests

### Phase 2: Split Advisor (1h)
- [x] Design approved
- [ ] Implement TaskSplitAdvisor
- [ ] Threshold logic
- [ ] Split strategies
- [ ] Unit tests

### Phase 3: Models & CLI (1h)
- [x] Design approved
- [ ] Implement SplitRecommendation
- [ ] Implement CLI handler
- [ ] Bash bridge
- [ ] Integration tests

### Phase 4: Configuration (0.5h)
- [x] Design approved
- [ ] Add upfront_complexity to settings.json
- [ ] Document configuration options

### Phase 5: Documentation (0.5h)
- [x] ADR-005 complete
- [x] Implementation plan complete
- [x] Comparison document complete
- [ ] Command documentation
- [ ] Usage examples

## Testing Strategy

### Unit Tests (60%)
- Adapter heuristics
- Split advisor logic
- Edge cases

### Integration Tests (30%)
- End-to-end flow
- CLI JSON output
- Interactive mode

### Reused Tests (10%)
- TASK-003A calculator (already passing)
- TASK-003A factors (already passing)

**Coverage Target**: >90%

## Configuration

```json
{
  "upfront_complexity": {
    "auto_split_threshold": 7,
    "max_recommended_splits": 4,
    "interactive_mode": true,
    "default_split_strategy": "vertical"
  }
}
```

## Usage Example

```bash
# Evaluate requirements and get split recommendations
/upfront-complexity-check \
  --task-id TASK-XXX \
  --requirements-file docs/requirements/REQ-001.md \
  --interactive

# Expected output (JSON)
{
  "task_id": "TASK-XXX",
  "complexity_score": 8,
  "review_mode": "full_required",
  "split_recommended": true,
  "recommendation": {
    "should_split": true,
    "recommended_task_count": 3,
    "split_strategy": "vertical",
    "suggested_splits": [
      "Task 1: User authentication API",
      "Task 2: User profile management",
      "Task 3: Password reset flow"
    ],
    "reasoning": "High complexity (8/10) due to security requirements..."
  }
}
```

## Success Criteria

- [ ] Zero duplicate complexity logic (100% TASK-003A reuse)
- [ ] 3 classes only (minimal architecture)
- [ ] >90% test coverage
- [ ] All tests passing
- [ ] No changes to TASK-003A code
- [ ] Configuration-driven behavior
- [ ] Interactive mode functional
- [ ] Documentation complete

## Dependencies

### TASK-003A (Required)
- `complexity_calculator.py` - Core scoring engine
- `complexity_models.py` - Data models
- `complexity_factors.py` - Scoring factors

**Status**: ✓ Implemented and tested (completed task)

### External Dependencies (None)
- Pure Python 3.10+
- No new external libraries required

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Heuristic accuracy | Conservative estimates, configurable keywords |
| TASK-003A changes | Integration tests catch breakage |
| Over-splitting | Threshold tuning, max splits cap |
| Under-splitting | Force-review triggers, interactive mode |

## Next Steps

1. **Review this plan**: Confirm approach ✓ (DONE)
2. **Phase 1**: Implement adapter layer
3. **Phase 2**: Implement split advisor
4. **Phase 3**: CLI and models
5. **Phase 4**: Configuration
6. **Phase 5**: Documentation
7. **Deploy**: Integrate into workflow

## Documentation References

- **ADR**: `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/docs/adr/ADR-005-upfront-complexity-refactored-architecture.md`
- **Implementation Plan**: `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/docs/implementation-plans/TASK-005-revised-plan.md`
- **Comparison**: `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/docs/implementation-plans/TASK-005-comparison.md`
- **TASK-003A Reference**: `installer/global/commands/lib/complexity_*.py`

## Questions/Clarifications

If you have questions about:
- **Architecture**: See ADR-005
- **Implementation**: See TASK-005-revised-plan.md
- **Comparison**: See TASK-005-comparison.md
- **TASK-003A Code**: See `installer/global/commands/lib/complexity_*.py`

---

**Status**: Ready for implementation approval
**Last Updated**: 2025-10-11
**Approver**: Software Architect
