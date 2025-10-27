# ADR-005: Upfront Complexity Evaluation - Refactored Architecture

## Status
**Proposed** - Addressing architectural review recommendations

## Context

TASK-005 requires implementing upfront complexity evaluation with task splitting recommendations. The initial architectural review identified critical issues:

1. **DRY Violation**: Reimplementing complexity algorithm that already exists in TASK-003A
2. **Over-Engineering**: 6+ classes proposed where 3-4 would suffice
3. **Missing Extensibility**: Hard-coded pattern detection rules
4. **Lack of Reusability**: Not leveraging existing complexity calculation infrastructure

### Existing TASK-003A Infrastructure

TASK-003A has already implemented a robust, production-ready complexity evaluation system:

**Core Components** (`installer/global/commands/lib/`):
- `complexity_calculator.py` - Core scoring engine with 4-factor aggregation
- `complexity_models.py` - Complete data models (ComplexityScore, FactorScore, ReviewMode, etc.)
- `complexity_factors.py` - Strategy pattern for factor evaluation (File, Pattern, Risk factors)

**Key Capabilities**:
- 1-10 complexity scoring scale
- 3 core factors: FileComplexity (0-3), PatternFamiliarity (0-2), RiskLevel (0-3)
- Force-review triggers (security, schema changes, breaking changes, hotfix)
- Fail-safe error handling (defaults to score=10 on errors)
- Review mode routing: AUTO_PROCEED (1-3), QUICK_OPTIONAL (4-6), FULL_REQUIRED (7-10)

### TASK-005 Requirements Gap

TASK-003A evaluates complexity from **implementation plans** (Phase 2.7).
TASK-005 needs to evaluate complexity from **requirements** (earlier in workflow).

**Key Differences**:
- **Input**: Requirements text vs. implementation plan
- **Output**: Split recommendations vs. review mode routing
- **Timing**: Feature planning stage vs. task implementation stage
- **Purpose**: Proactive decomposition vs. reactive quality gates

## Decision

**Refactor TASK-005 to reuse TASK-003A infrastructure with minimal new code.**

### Architecture Principles

1. **Maximum Reuse**: Use TASK-003A's complexity core without modification
2. **Adapter Pattern**: Create thin adapter layer for requirements-based input
3. **Minimal Classes**: 3-4 classes total (down from 6+ proposed)
4. **Shared Configuration**: Unified pattern registry and risk rules
5. **DRY Compliance**: Zero duplicate complexity logic

### Revised Component Design

#### Shared Library (`installer/global/commands/lib/`)

**No Changes Needed**:
- `complexity_calculator.py` - Reuse as-is
- `complexity_models.py` - Reuse all models
- `complexity_factors.py` - Reuse all factors

**New Shared Components**:

```python
# lib/upfront_complexity_adapter.py (TASK-005 specific)
class UpfrontComplexityAdapter:
    """Adapts requirements text to implementation plan format for complexity evaluation.

    This is the key DRY-compliance component that bridges requirements → complexity scoring
    without reimplementing the core algorithm.
    """

    def __init__(self, calculator: ComplexityCalculator):
        self.calculator = calculator

    def evaluate_requirements(
        self,
        requirements_text: str,
        task_id: str,
        metadata: Dict[str, Any]
    ) -> ComplexityScore:
        """Convert requirements to plan format and evaluate complexity."""
        # 1. Parse requirements to estimate file count
        # 2. Detect patterns from requirements keywords
        # 3. Identify risk indicators from requirements
        # 4. Build ImplementationPlan from requirements
        # 5. Delegate to existing ComplexityCalculator
        pass

    def _estimate_files_from_requirements(self, text: str) -> List[str]:
        """Heuristic file estimation from requirements."""
        pass

    def _detect_patterns_from_requirements(self, text: str) -> List[str]:
        """Pattern detection from requirements keywords."""
        pass
```

```python
# lib/task_split_advisor.py (TASK-005 specific)
class TaskSplitAdvisor:
    """Recommends task splitting based on complexity score.

    Simple function-oriented approach (not over-class-ified).
    """

    def recommend_split(
        self,
        complexity_score: ComplexityScore,
        requirements_text: str
    ) -> Optional[SplitRecommendation]:
        """Generate split recommendations if complexity threshold exceeded."""
        if complexity_score.total_score <= 6:
            return None  # No split needed

        # Generate split recommendations for scores 7+
        return self._generate_recommendations(complexity_score, requirements_text)

    def _generate_recommendations(
        self,
        score: ComplexityScore,
        text: str
    ) -> SplitRecommendation:
        """Simple heuristic-based split suggestions."""
        pass
```

```python
# lib/split_models.py (TASK-005 specific)
@dataclass(frozen=True)
class SplitRecommendation:
    """Task splitting recommendation."""
    should_split: bool
    recommended_task_count: int  # 2-4 tasks typically
    split_strategy: str  # "horizontal", "vertical", "by-layer"
    suggested_splits: List[str]  # Human-readable split descriptions
    reasoning: str
    complexity_breakdown: ComplexityScore
```

#### Command Integration (`installer/global/commands/`)

```bash
# upfront-complexity-check.sh (minimal bash bridge)
#!/bin/bash
# JSON I/O bridge to Python logic
python3 -m lib.upfront_complexity_cli "$@"
```

```python
# lib/upfront_complexity_cli.py (TASK-005 command handler)
def main():
    """CLI entry point for upfront complexity evaluation."""
    # 1. Parse CLI args (task-id, requirements file path)
    # 2. Read requirements
    # 3. Call UpfrontComplexityAdapter.evaluate_requirements()
    # 4. Call TaskSplitAdvisor.recommend_split()
    # 5. Output JSON results
    # 6. Optional: Interactive split decision
    pass
```

### Simplified Class Structure

**Total Classes: 3** (down from 6+ proposed)

1. **UpfrontComplexityAdapter** - Adapter for requirements input (new)
2. **TaskSplitAdvisor** - Split recommendations logic (new)
3. **SplitRecommendation** - Data model for split suggestions (new)

**Reused from TASK-003A: 6 classes**
- ComplexityCalculator
- ComplexityScore, FactorScore, ImplementationPlan, EvaluationContext, ReviewDecision
- FileComplexityFactor, PatternFamiliarityFactor, RiskLevelFactor

**Total System: 9 classes** (vs. 12+ in original proposal)

### Data Flow

```
Requirements Text
    ↓
UpfrontComplexityAdapter
    ↓ (converts to ImplementationPlan format)
ComplexityCalculator (TASK-003A - reused)
    ↓ (returns ComplexityScore)
TaskSplitAdvisor
    ↓ (if score >= 7)
SplitRecommendation
    ↓
JSON Output / Interactive Decision
```

## Consequences

### Positive

1. **Zero Duplicate Logic**: Reuses all TASK-003A complexity scoring
2. **Smaller Codebase**: ~300 LOC vs. ~800 LOC originally proposed
3. **Maintainability**: Single source of truth for complexity algorithms
4. **Consistency**: Same scoring logic for requirements and implementation
5. **Faster Development**: 60% less code to write and test
6. **Extensibility**: Strategy pattern from TASK-003A extends to TASK-005
7. **Type Safety**: Reuses all existing data models

### Negative

1. **Abstraction Layer**: Adapter adds indirection (minimal, acceptable)
2. **Estimation Heuristics**: Requirements → file count is approximate (inherent to problem)
3. **Coupling**: TASK-005 depends on TASK-003A library stability (acceptable, both in same system)

### Risks Mitigated

1. **DRY Violation**: Completely eliminated
2. **Over-Engineering**: Reduced from 6 to 3 new classes
3. **Hard-Coded Rules**: Reuses TASK-003A's pattern/risk registries
4. **Testing Burden**: Reuses TASK-003A's test suite

## Implementation Plan

### Phase 1: Shared Library Refactoring (1-2 hours)

**File**: `installer/global/commands/lib/upfront_complexity_adapter.py`
- UpfrontComplexityAdapter class
- Requirements parsing heuristics
- Pattern/risk detection from requirements text

**File**: `installer/global/commands/lib/task_split_advisor.py`
- TaskSplitAdvisor class
- Split recommendation logic
- Heuristic split strategies

**File**: `installer/global/commands/lib/split_models.py`
- SplitRecommendation dataclass
- Helper methods

### Phase 2: Command Integration (1 hour)

**File**: `installer/global/commands/upfront-complexity-check.sh`
- Bash bridge to Python CLI

**File**: `installer/global/commands/lib/upfront_complexity_cli.py`
- CLI argument parsing
- JSON I/O handling
- Interactive decision flow

### Phase 3: Configuration (0.5 hours)

**File**: `.claude/settings.json`
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

### Phase 4: Testing (1.5 hours)

**File**: `tests/test_upfront_complexity_adapter.py`
- Requirements → ImplementationPlan conversion tests
- Pattern/risk detection tests
- Edge cases (empty requirements, ambiguous requirements)

**File**: `tests/test_task_split_advisor.py`
- Split recommendation logic tests
- Threshold tests (score 6 vs. 7+)
- Split strategy tests

**Integration Tests**:
- End-to-end requirements → recommendations flow
- Reuse TASK-003A's ComplexityCalculator test suite

### Phase 5: Documentation (0.5 hours)

**File**: `installer/global/commands/upfront-complexity-check.md`
- Command usage documentation
- Examples
- Configuration options

## File Structure

```
installer/global/commands/
├── lib/
│   ├── complexity_calculator.py           # TASK-003A (reused)
│   ├── complexity_models.py               # TASK-003A (reused)
│   ├── complexity_factors.py              # TASK-003A (reused)
│   ├── upfront_complexity_adapter.py      # NEW (TASK-005)
│   ├── task_split_advisor.py              # NEW (TASK-005)
│   ├── split_models.py                    # NEW (TASK-005)
│   └── upfront_complexity_cli.py          # NEW (TASK-005)
├── upfront-complexity-check.sh            # NEW (TASK-005 command)
└── upfront-complexity-check.md            # NEW (TASK-005 docs)

tests/
├── test_complexity_calculator.py          # TASK-003A (reused)
├── test_complexity_factors.py             # TASK-003A (reused)
├── test_upfront_complexity_adapter.py     # NEW (TASK-005)
└── test_task_split_advisor.py             # NEW (TASK-005)
```

## Migration Strategy

### Step 1: Verify TASK-003A Stability
- Ensure TASK-003A code is committed and stable
- Run TASK-003A test suite to confirm baseline

### Step 2: Extract Shared Components
- No extraction needed - TASK-003A code stays in place
- TASK-005 imports from `lib/complexity_*.py`

### Step 3: Build Adapter Layer
- Implement UpfrontComplexityAdapter
- Test against TASK-003A's ComplexityCalculator

### Step 4: Implement Split Logic
- Implement TaskSplitAdvisor
- Test split recommendations

### Step 5: Integration Testing
- End-to-end workflow tests
- Verify JSON I/O
- Test interactive mode

## Complexity Estimate

### Original Proposal
- **Files**: 8-10 files
- **LOC**: ~800 lines
- **Classes**: 6+ classes
- **Tests**: ~400 LOC

### Revised Proposal
- **Files**: 4 new files (reusing 3 from TASK-003A)
- **LOC**: ~300 lines (60% reduction)
- **Classes**: 3 new classes (50% reduction)
- **Tests**: ~200 LOC (50% reduction)

### Time Estimate
- **Original**: 6-8 hours
- **Revised**: 4-5 hours (40% time savings)

## Alternatives Considered

### Alternative 1: Duplicate Complexity Logic
**Rejected**: Violates DRY principle, creates maintenance burden

### Alternative 2: Completely New Scoring Algorithm
**Rejected**: Inconsistent with TASK-003A, requires full re-testing

### Alternative 3: Merge TASK-005 into TASK-003A
**Rejected**: Different use cases (requirements vs. implementation), separation of concerns

### Alternative 4: Shared Base Class
**Rejected**: Adapter pattern is simpler, less coupling

## Review Checklist

- [ ] Zero duplicate complexity scoring logic
- [ ] Reuses all TASK-003A infrastructure
- [ ] 3-4 classes only (minimal viable architecture)
- [ ] Strategy pattern for extensibility
- [ ] Comprehensive test coverage (leveraging TASK-003A tests)
- [ ] Clear separation: adapter (TASK-005) vs. core (TASK-003A)
- [ ] Configuration-driven behavior
- [ ] JSON I/O for bash integration
- [ ] Interactive split decision flow
- [ ] Documentation complete

## Success Metrics

1. **Code Reuse**: 100% of TASK-003A complexity logic reused
2. **LOC Reduction**: 60% fewer lines than original proposal
3. **Class Count**: 50% fewer classes than original proposal
4. **Test Coverage**: >90% coverage using TASK-003A test suite
5. **Development Time**: 40% time savings vs. original estimate

## References

- TASK-003A: Architectural Review (Phase 2.7)
- TASK-005: Upfront Complexity Evaluation with Task Splitting
- Architectural Review Feedback: Critical DRY violation identified
- Strategy Pattern: GoF Design Patterns
- Adapter Pattern: GoF Design Patterns
