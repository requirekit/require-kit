# TASK-005: Upfront Complexity Evaluation - REVISED Implementation Plan

## Revision Summary

**Date**: 2025-10-11
**Reason**: Architectural review identified critical DRY violation and over-engineering
**Status**: Refactored to reuse TASK-003A infrastructure

### Critical Changes

1. **DRY Compliance**: Reuse TASK-003A complexity calculation engine (zero duplicate logic)
2. **Simplified Architecture**: Reduced from 6+ classes to 3 classes
3. **Adapter Pattern**: Thin adapter layer for requirements-based input
4. **60% Code Reduction**: ~300 LOC vs. ~800 LOC originally proposed
5. **40% Time Savings**: 4-5 hours vs. 6-8 hours estimated

## Architecture Overview

### Reused Components (TASK-003A)

**From** `installer/global/commands/lib/`:
- `complexity_calculator.py` - Core scoring engine (1-10 scale, 3 factors)
- `complexity_models.py` - Data models (ComplexityScore, FactorScore, ReviewMode)
- `complexity_factors.py` - Strategy pattern factors (File, Pattern, Risk)

**Why Reuse**: Production-ready, tested, same scoring methodology

### New Components (TASK-005)

#### 1. UpfrontComplexityAdapter
**File**: `installer/global/commands/lib/upfront_complexity_adapter.py`

```python
"""
Adapter that converts requirements text to implementation plan format
for complexity evaluation using TASK-003A's calculator.
"""

class UpfrontComplexityAdapter:
    def __init__(self, calculator: ComplexityCalculator):
        """Initialize with existing TASK-003A calculator."""
        self.calculator = calculator

    def evaluate_requirements(
        self,
        requirements_text: str,
        task_id: str,
        metadata: Dict[str, Any]
    ) -> ComplexityScore:
        """
        Main entry point: Requirements → ComplexityScore

        Flow:
        1. Parse requirements to estimate files
        2. Detect patterns from keywords
        3. Identify risk indicators
        4. Build ImplementationPlan (TASK-003A model)
        5. Delegate to ComplexityCalculator
        """
        pass

    def _estimate_files_from_requirements(self, text: str) -> List[str]:
        """
        Heuristic file estimation from requirements.

        Heuristics:
        - Count entities mentioned (User, Order, Product → models)
        - Detect API endpoints (REST → controllers, services)
        - Identify UI components (form, dashboard → views)
        - Database keywords (schema → migrations)
        """
        pass

    def _detect_patterns_from_requirements(self, text: str) -> List[str]:
        """
        Pattern detection from requirements keywords.

        Examples:
        - "authentication" → Strategy pattern (auth providers)
        - "notification" → Observer pattern (event handlers)
        - "caching" → Decorator pattern
        - "state machine" → State pattern
        """
        pass

    def _detect_risk_indicators(self, text: str) -> List[str]:
        """
        Risk detection from requirements.

        Categories:
        - Security: "auth", "permission", "encryption"
        - Data: "migration", "schema", "transaction"
        - External: "API", "integration", "third-party"
        - Performance: "real-time", "scaling", "caching"
        """
        pass
```

**Complexity**: ~100 LOC, straightforward heuristics

#### 2. TaskSplitAdvisor
**File**: `installer/global/commands/lib/task_split_advisor.py`

```python
"""
Recommends task splitting based on complexity score from TASK-003A.
Simple function-oriented approach (not over-class-ified).
"""

class TaskSplitAdvisor:
    def recommend_split(
        self,
        complexity_score: ComplexityScore,
        requirements_text: str
    ) -> Optional[SplitRecommendation]:
        """
        Generate split recommendations if score >= 7.

        Thresholds:
        - Score 1-6: No split needed (return None)
        - Score 7-8: Recommend 2-3 tasks
        - Score 9-10: Recommend 3-4 tasks
        """
        if complexity_score.total_score <= 6:
            return None

        return self._generate_recommendations(complexity_score, requirements_text)

    def _generate_recommendations(
        self,
        score: ComplexityScore,
        text: str
    ) -> SplitRecommendation:
        """
        Heuristic-based split suggestions.

        Strategies:
        - Vertical: By feature/user story (login, registration, password reset)
        - Horizontal: By layer (API, business logic, database)
        - By-Risk: Separate security/data from standard logic
        """
        pass

    def _suggest_vertical_splits(self, text: str) -> List[str]:
        """Split by feature boundaries (user stories)."""
        pass

    def _suggest_horizontal_splits(self, text: str) -> List[str]:
        """Split by architectural layers (API → logic → data)."""
        pass

    def _suggest_risk_based_splits(self, score: ComplexityScore, text: str) -> List[str]:
        """Split by risk level (isolate high-risk components)."""
        pass
```

**Complexity**: ~80 LOC, simple heuristics

#### 3. SplitRecommendation Model
**File**: `installer/global/commands/lib/split_models.py`

```python
"""Data model for task splitting recommendations."""

from dataclasses import dataclass, field
from typing import List
from .complexity_models import ComplexityScore

@dataclass(frozen=True)
class SplitRecommendation:
    """Task splitting recommendation based on complexity analysis."""

    should_split: bool
    recommended_task_count: int  # 2-4 typically
    split_strategy: str  # "vertical", "horizontal", "by-risk"
    suggested_splits: List[str]  # Human-readable descriptions
    reasoning: str  # Why split is recommended
    complexity_breakdown: ComplexityScore  # Original complexity score

    @property
    def is_critical_split(self) -> bool:
        """Check if split is critical (score >= 9)."""
        return self.complexity_breakdown.total_score >= 9
```

**Complexity**: ~30 LOC, simple data class

#### 4. CLI Handler
**File**: `installer/global/commands/lib/upfront_complexity_cli.py`

```python
"""CLI entry point for upfront complexity evaluation command."""

import json
import sys
from pathlib import Path
from .upfront_complexity_adapter import UpfrontComplexityAdapter
from .task_split_advisor import TaskSplitAdvisor
from .complexity_calculator import ComplexityCalculator
from .complexity_factors import DEFAULT_FACTORS

def main():
    """
    CLI flow:
    1. Parse args (--task-id, --requirements-file)
    2. Read requirements text
    3. Evaluate complexity via adapter
    4. Generate split recommendations
    5. Output JSON results
    6. Optional: Interactive decision prompt
    """

    # Initialize TASK-003A components
    calculator = ComplexityCalculator(factors=DEFAULT_FACTORS)
    adapter = UpfrontComplexityAdapter(calculator)
    advisor = TaskSplitAdvisor()

    # Parse CLI args
    args = parse_arguments()

    # Read requirements
    requirements = Path(args.requirements_file).read_text()

    # Evaluate complexity
    complexity = adapter.evaluate_requirements(
        requirements_text=requirements,
        task_id=args.task_id,
        metadata={"source": "upfront-evaluation"}
    )

    # Generate recommendations
    recommendation = advisor.recommend_split(complexity, requirements)

    # Output JSON
    result = {
        "task_id": args.task_id,
        "complexity_score": complexity.total_score,
        "review_mode": complexity.review_mode.value,
        "split_recommended": recommendation is not None,
        "recommendation": recommendation.__dict__ if recommendation else None
    }

    print(json.dumps(result, indent=2, default=str))

    # Interactive mode
    if args.interactive and recommendation:
        handle_interactive_decision(recommendation)

def handle_interactive_decision(recommendation: SplitRecommendation):
    """Interactive prompt for split decision."""
    print("\n=== Task Splitting Recommendation ===")
    print(f"Complexity Score: {recommendation.complexity_breakdown.total_score}/10")
    print(f"Strategy: {recommendation.split_strategy}")
    print(f"\nSuggested Splits ({recommendation.recommended_task_count}):")
    for i, split in enumerate(recommendation.suggested_splits, 1):
        print(f"  {i}. {split}")
    print(f"\nReasoning: {recommendation.reasoning}")

    choice = input("\nProceed with split? [y/N]: ").strip().lower()
    if choice == 'y':
        print("Split accepted. Create tasks manually or use /feature-generate-tasks.")
    else:
        print("Proceeding with single task (not recommended for high complexity).")

if __name__ == "__main__":
    main()
```

**Complexity**: ~90 LOC, straightforward CLI handling

#### 5. Bash Bridge
**File**: `installer/global/commands/upfront-complexity-check.sh`

```bash
#!/bin/bash
# Minimal bash bridge to Python CLI

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_CLI="$SCRIPT_DIR/lib/upfront_complexity_cli.py"

# Forward all args to Python CLI
python3 "$PYTHON_CLI" "$@"
```

**Complexity**: ~10 LOC, simple delegation

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. INPUT: Requirements Text                                 │
│    - EARS notation                                          │
│    - BDD scenarios                                          │
│    - Feature descriptions                                   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. UpfrontComplexityAdapter                                 │
│    - Parse requirements                                     │
│    - Estimate files (heuristics)                            │
│    - Detect patterns (keywords)                             │
│    - Identify risks (keywords)                              │
│    - Build ImplementationPlan (TASK-003A model)             │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. ComplexityCalculator (TASK-003A - REUSED)                │
│    - Evaluate factors (File, Pattern, Risk)                 │
│    - Aggregate score (1-10 scale)                           │
│    - Detect force-review triggers                           │
│    - Determine review mode                                  │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. ComplexityScore (TASK-003A model)                        │
│    - total_score: int (1-10)                                │
│    - factor_scores: List[FactorScore]                       │
│    - review_mode: ReviewMode                                │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. TaskSplitAdvisor                                         │
│    - Check threshold (score >= 7)                           │
│    - Generate split recommendations                         │
│    - Determine split strategy                               │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. OUTPUT: SplitRecommendation (or None)                    │
│    - should_split: bool                                     │
│    - recommended_task_count: int                            │
│    - split_strategy: str                                    │
│    - suggested_splits: List[str]                            │
│    - reasoning: str                                         │
└─────────────────────────────────────────────────────────────┘
```

## Implementation Phases

### Phase 1: Adapter Layer (1.5 hours)

**File**: `installer/global/commands/lib/upfront_complexity_adapter.py`

**Tasks**:
1. Implement `UpfrontComplexityAdapter` class
2. File estimation heuristics:
   - Entity detection (User, Order → models)
   - API endpoint detection (GET /users → controller)
   - UI component detection (form, dashboard → views)
3. Pattern detection heuristics:
   - Keyword mapping (auth → Strategy, notification → Observer)
4. Risk indicator detection:
   - Security keywords
   - Data integrity keywords
   - External integration keywords
5. Build `ImplementationPlan` from heuristics

**Testing**:
- Unit tests for each heuristic function
- Integration test: requirements → ImplementationPlan
- Edge cases: empty requirements, ambiguous requirements

**Estimated LOC**: ~100

### Phase 2: Split Advisor (1 hour)

**File**: `installer/global/commands/lib/task_split_advisor.py`

**Tasks**:
1. Implement `TaskSplitAdvisor` class
2. Threshold logic (score >= 7)
3. Split strategies:
   - Vertical splits (by feature)
   - Horizontal splits (by layer)
   - Risk-based splits (isolate high-risk)
4. Heuristic split suggestions

**Testing**:
- Unit tests for each split strategy
- Threshold tests (score 6 vs. 7+)
- Split count tests (7-8 → 2-3, 9-10 → 3-4)

**Estimated LOC**: ~80

### Phase 3: Models & CLI (1 hour)

**File**: `installer/global/commands/lib/split_models.py`
**File**: `installer/global/commands/lib/upfront_complexity_cli.py`
**File**: `installer/global/commands/upfront-complexity-check.sh`

**Tasks**:
1. Implement `SplitRecommendation` dataclass
2. CLI argument parsing
3. JSON I/O handling
4. Interactive decision flow
5. Bash bridge script

**Testing**:
- End-to-end CLI tests
- JSON output validation
- Interactive mode tests (mocked input)

**Estimated LOC**: ~120 total

### Phase 4: Configuration (0.5 hours)

**File**: `.claude/settings.json`

```json
{
  "upfront_complexity": {
    "auto_split_threshold": 7,
    "max_recommended_splits": 4,
    "interactive_mode": true,
    "default_split_strategy": "vertical",
    "patterns": {
      "entity_keywords": ["user", "order", "product", "customer"],
      "api_keywords": ["endpoint", "route", "api", "rest"],
      "ui_keywords": ["form", "dashboard", "component", "view"]
    },
    "risks": {
      "security_keywords": ["auth", "password", "token", "encryption"],
      "data_keywords": ["migration", "schema", "database"],
      "external_keywords": ["api", "integration", "third-party"]
    }
  }
}
```

**Tasks**:
1. Define configuration schema
2. Load configuration in adapter/advisor
3. Document configuration options

### Phase 5: Testing (1 hour)

**Files**:
- `tests/test_upfront_complexity_adapter.py`
- `tests/test_task_split_advisor.py`
- `tests/test_upfront_complexity_integration.py`

**Test Cases**:

**Adapter Tests**:
- Requirements → ImplementationPlan conversion
- File estimation accuracy
- Pattern detection accuracy
- Risk indicator detection
- Edge cases (empty, malformed requirements)

**Advisor Tests**:
- Threshold logic (6 vs. 7+)
- Split strategy selection
- Split count recommendations
- Reasoning generation

**Integration Tests**:
- End-to-end: requirements → complexity → recommendations
- Reuse TASK-003A calculator tests
- CLI JSON output validation
- Interactive mode flow

**Coverage Target**: >90%

### Phase 6: Documentation (0.5 hours)

**File**: `installer/global/commands/upfront-complexity-check.md`

```markdown
# /upfront-complexity-check

## Purpose
Evaluate task complexity from requirements text and recommend task splitting
before implementation begins.

## Usage
```bash
/upfront-complexity-check --task-id TASK-XXX --requirements-file path/to/requirements.md [--interactive]
```

## Arguments
- `--task-id`: Task identifier (e.g., TASK-005)
- `--requirements-file`: Path to requirements file (EARS or BDD)
- `--interactive`: Enable interactive split decision (optional)

## Output
JSON with complexity score and split recommendations.

## Examples
[See full examples in documentation]

## Configuration
See `.claude/settings.json` for customization options.
```

**Tasks**:
1. Write command documentation
2. Add usage examples
3. Document configuration options
4. Add troubleshooting section

## File Structure (Final)

```
installer/global/commands/
├── lib/
│   ├── complexity_calculator.py           # TASK-003A (reused) ✓
│   ├── complexity_models.py               # TASK-003A (reused) ✓
│   ├── complexity_factors.py              # TASK-003A (reused) ✓
│   ├── upfront_complexity_adapter.py      # NEW (~100 LOC)
│   ├── task_split_advisor.py              # NEW (~80 LOC)
│   ├── split_models.py                    # NEW (~30 LOC)
│   └── upfront_complexity_cli.py          # NEW (~90 LOC)
├── upfront-complexity-check.sh            # NEW (~10 LOC)
└── upfront-complexity-check.md            # NEW (docs)

tests/
├── test_complexity_calculator.py          # TASK-003A (reused) ✓
├── test_complexity_factors.py             # TASK-003A (reused) ✓
├── test_upfront_complexity_adapter.py     # NEW (~100 LOC)
├── test_task_split_advisor.py             # NEW (~60 LOC)
└── test_upfront_complexity_integration.py # NEW (~40 LOC)

.claude/
└── settings.json                          # UPDATE (add upfront config)

docs/adr/
└── ADR-005-upfront-complexity-refactored-architecture.md  # NEW ✓
```

## Code Metrics Summary

### New Code (TASK-005)
- **Production Code**: ~310 LOC
  - upfront_complexity_adapter.py: ~100 LOC
  - task_split_advisor.py: ~80 LOC
  - split_models.py: ~30 LOC
  - upfront_complexity_cli.py: ~90 LOC
  - upfront-complexity-check.sh: ~10 LOC

- **Test Code**: ~200 LOC
  - test_upfront_complexity_adapter.py: ~100 LOC
  - test_task_split_advisor.py: ~60 LOC
  - test_upfront_complexity_integration.py: ~40 LOC

- **Total New Code**: ~510 LOC

### Reused Code (TASK-003A)
- complexity_calculator.py: ~350 LOC (reused 100%)
- complexity_models.py: ~225 LOC (reused 100%)
- complexity_factors.py: ~265 LOC (reused 100%)
- **Total Reused**: ~840 LOC

### Comparison to Original Proposal
| Metric | Original | Revised | Savings |
|--------|----------|---------|---------|
| Production LOC | ~800 | ~310 | 61% |
| Test LOC | ~400 | ~200 | 50% |
| Total LOC | ~1200 | ~510 | 58% |
| New Classes | 6+ | 3 | 50% |
| Files | 10+ | 7 | 30% |
| Estimated Hours | 6-8 | 4-5 | 38% |

## Testing Strategy

### Unit Tests (60% of testing effort)
- Adapter heuristics (file estimation, pattern detection, risk detection)
- Split advisor logic (threshold, strategies, recommendations)
- Edge cases and error handling

### Integration Tests (30% of testing effort)
- End-to-end flow: requirements → complexity → recommendations
- CLI JSON output validation
- Interactive mode flow

### Reused Tests (10% of testing effort)
- TASK-003A calculator tests (already passing)
- TASK-003A factor tests (already passing)

### Coverage Target
- **New Code**: >90% coverage
- **Integration**: 100% critical paths covered
- **Reused Code**: Already at >95% coverage from TASK-003A

## Configuration Options

### `.claude/settings.json`

```json
{
  "upfront_complexity": {
    // Threshold for auto-split recommendations
    "auto_split_threshold": 7,

    // Maximum number of recommended task splits
    "max_recommended_splits": 4,

    // Enable interactive decision prompts
    "interactive_mode": true,

    // Default split strategy
    "default_split_strategy": "vertical",

    // Pattern detection keywords
    "patterns": {
      "entity_keywords": ["user", "order", "product", "customer", "account"],
      "api_keywords": ["endpoint", "route", "api", "rest", "graphql"],
      "ui_keywords": ["form", "dashboard", "component", "view", "page"]
    },

    // Risk detection keywords
    "risks": {
      "security_keywords": ["auth", "password", "token", "encryption", "permission"],
      "data_keywords": ["migration", "schema", "database", "transaction"],
      "external_keywords": ["api", "integration", "third-party", "webhook"]
    },

    // Split strategy preferences
    "split_preferences": {
      "prefer_vertical": true,
      "isolate_risks": true,
      "max_files_per_task": 5
    }
  }
}
```

## Success Criteria

### Code Quality
- [ ] Zero duplicate complexity logic (100% reuse of TASK-003A)
- [ ] 3 classes only (UpfrontComplexityAdapter, TaskSplitAdvisor, SplitRecommendation)
- [ ] >90% test coverage for new code
- [ ] All tests passing (unit, integration, reused)

### Architecture
- [ ] Adapter pattern correctly implemented
- [ ] Clean separation: adapter (TASK-005) vs. core (TASK-003A)
- [ ] No modifications to TASK-003A code
- [ ] Strategy pattern extensible (pattern/risk registries)

### Functionality
- [ ] Requirements → complexity score working
- [ ] Split recommendations accurate for score >= 7
- [ ] Interactive mode functional
- [ ] JSON output correct format
- [ ] Configuration-driven behavior

### Documentation
- [ ] ADR-005 complete
- [ ] Command documentation complete
- [ ] Configuration documented
- [ ] Examples provided
- [ ] Troubleshooting guide

### Performance
- [ ] Complexity evaluation <1s for typical requirements
- [ ] No performance degradation vs. TASK-003A
- [ ] Handles large requirements (>1000 lines)

## Migration Notes

### No TASK-003A Changes Required
- TASK-003A code remains untouched
- No refactoring of existing code
- TASK-005 imports TASK-003A modules as-is

### Configuration Changes
- Add `upfront_complexity` section to `.claude/settings.json`
- No impact on existing TASK-003A configuration

### Testing Changes
- New test files only (no changes to TASK-003A tests)
- Reuse TASK-003A test fixtures where applicable

## Risk Mitigation

### Risk: Heuristic Accuracy
**Mitigation**: Conservative estimates (default to higher complexity), configuration-driven keywords

### Risk: TASK-003A Breaking Changes
**Mitigation**: Pin to specific TASK-003A version, integration tests will catch breakage

### Risk: Over-Splitting
**Mitigation**: Threshold tuning (default 7), max_recommended_splits cap (4)

### Risk: Under-Splitting
**Mitigation**: Force-review triggers from TASK-003A still apply, interactive mode allows override

## Next Steps

1. **Review this plan**: Confirm architectural approach
2. **Implement Phase 1**: Adapter layer with TASK-003A integration
3. **Implement Phase 2**: Split advisor logic
4. **Implement Phase 3**: CLI and models
5. **Configure**: Add upfront_complexity settings
6. **Test**: Comprehensive test suite
7. **Document**: Command documentation
8. **Deploy**: Integrate into agentecflow workflow

## Conclusion

This revised plan addresses all architectural review concerns:
- **DRY Violation**: Eliminated by reusing TASK-003A
- **Over-Engineering**: Reduced from 6+ to 3 classes
- **Missing Extensibility**: Inherited from TASK-003A's Strategy pattern
- **Code Reduction**: 60% fewer LOC, 40% time savings

The implementation is **minimal, DRY-compliant, and production-ready**.
