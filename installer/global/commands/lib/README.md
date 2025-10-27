# Complexity Evaluation Library

Phase 2.7 complexity evaluation system for the Agentecflow task-work workflow.

## Overview

This library calculates implementation complexity scores and routes tasks to appropriate review modes:
- **Auto-proceed** (score 1-3): Simple tasks proceed to implementation automatically
- **Quick optional** (score 4-6): Moderate tasks offer optional human checkpoint
- **Full required** (score 7-10 or triggers): Complex/risky tasks require mandatory review

## Architecture

### Strategy Pattern for Scoring Factors
```
ComplexityFactor (Protocol)
├── FileComplexityFactor (0-3 points)
├── PatternFamiliarityFactor (0-2 points)
└── RiskLevelFactor (0-3 points)
```

Each factor evaluates one aspect independently and returns a `FactorScore`.

### Core Components

```
agent_utils.py
    ↓ parse_implementation_plan()
ImplementationPlan
    ↓ build_evaluation_context()
EvaluationContext
    ↓ ComplexityCalculator.calculate()
ComplexityScore
    ↓ ReviewRouter.route()
ReviewDecision
```

## Modules

### `complexity_models.py`
Type-safe data structures using dataclasses:
- `ImplementationPlan`: Structured plan representation
- `EvaluationContext`: Context for complexity calculation
- `FactorScore`: Individual factor result
- `ComplexityScore`: Aggregate complexity score
- `ReviewDecision`: Routing decision
- `ReviewMode`, `ForceReviewTrigger`: Enums

### `complexity_factors.py`
Strategy pattern implementations for scoring factors:
- `FileComplexityFactor`: Scores based on file count (0-3)
- `PatternFamiliarityFactor`: Scores based on design patterns (0-2)
- `RiskLevelFactor`: Scores based on risk indicators (0-3)

### `complexity_calculator.py`
Core calculation engine:
- Evaluates all configured factors
- Aggregates scores (1-10 scale)
- Detects force-review triggers
- Determines review mode
- Fail-safe error handling (defaults to score=10)

### `review_router.py`
Routing logic for review modes:
- Interprets complexity scores
- Generates human-readable summaries
- Routes to Phase 3, 2.6, or 2 revision
- Creates `ReviewDecision` with recommendations

### `agent_utils.py`
Shared utility functions:
- `parse_implementation_plan()`: Extract structured data from plan text
- `build_evaluation_context()`: Build evaluation context
- `format_decision_for_display()`: Terminal-friendly formatting
- `format_decision_for_metadata()`: YAML frontmatter formatting
- `log_complexity_calculation()`: Debug logging

## Usage Example

```python
from lib.complexity_calculator import ComplexityCalculator
from lib.review_router import ReviewRouter
from lib.agent_utils import (
    parse_implementation_plan,
    build_evaluation_context,
    format_decision_for_display
)

# Parse implementation plan
plan = parse_implementation_plan(plan_text, task_id="TASK-042")

# Build context
context = build_evaluation_context(
    task_id="TASK-042",
    technology_stack="python",
    implementation_plan=plan,
    task_metadata={"priority": "high"},
    user_flags={"review": False}
)

# Calculate complexity
calculator = ComplexityCalculator()
complexity_score = calculator.calculate(context)

# Route to review mode
router = ReviewRouter()
decision = router.route(complexity_score, context)

# Display result
print(format_decision_for_display(decision))

# Extract metadata for task file
from lib.agent_utils import format_decision_for_metadata
metadata = format_decision_for_metadata(decision)
```

## Scoring System

### Total Complexity Scale: 1-10 points

**Factors**:
1. **File Complexity** (0-3 points)
   - 0-2 files: 0 points
   - 3-5 files: 1 point
   - 6-8 files: 2 points
   - 9+ files: 3 points

2. **Pattern Familiarity** (0-2 points)
   - No patterns or simple patterns: 0 points
   - Moderate patterns (Strategy, Observer): 1 point
   - Advanced patterns (Saga, CQRS): 2 points

3. **Risk Level** (0-3 points)
   - 0 risk categories: 0 points
   - 1-2 risk categories: 1 point
   - 3-4 risk categories: 2 points
   - 5+ risk categories: 3 points

**Risk Categories**:
- Security (auth, encryption, permissions)
- Data integrity (schema changes, migrations)
- External integrations (APIs, third-party services)
- Performance (optimization, caching, scaling)

### Review Mode Thresholds

| Score | Review Mode | Description |
|-------|-------------|-------------|
| 1-3 | AUTO_PROCEED | Simple tasks, no review required |
| 4-6 | QUICK_OPTIONAL | Moderate tasks, optional checkpoint |
| 7-10 | FULL_REQUIRED | Complex tasks, mandatory checkpoint |

### Force-Review Triggers

These override score-based routing and force FULL_REQUIRED review:
- **User flag**: `--review` explicitly set
- **Security keywords**: Authentication, encryption, permissions
- **Breaking changes**: Public API modifications
- **Schema changes**: Database migrations
- **Hotfix**: Production emergency fix

## Error Handling

**Fail-Safe Strategy**: If any error occurs during calculation:
1. Log error with full stack trace
2. Default to score=10 (FULL_REQUIRED review)
3. Include error details in metadata
4. Never fail the task workflow

**Conservative Defaults**:
- Unknown/missing data → Assume higher complexity
- Parsing errors → Assume higher complexity
- Calculation errors → Default to FULL_REQUIRED review

## Testing

Run the test suite:
```bash
cd installer/global/commands/lib
python3 test_complexity.py
```

Tests verify:
- Simple task routing (auto-proceed)
- Moderate task routing (optional review)
- Complex task routing (full review)
- Forced trigger handling
- Error handling (fail-safe)

## Integration with task-work Command

### Workflow Position
```
Phase 2: Implementation Planning
    ↓
Phase 2.5B: Architectural Review
    ↓
Phase 2.7: Complexity Evaluation ← THIS LIBRARY
    ↓
Phase 2.6: Human Checkpoint (if triggered)
    ↓
Phase 3: Implementation
```

### Agent Integration

**complexity-evaluator agent** orchestrates this library:
1. Receives implementation plan from Phase 2
2. Calls library functions to calculate complexity
3. Returns `ReviewDecision` to task-manager
4. Updates task metadata with evaluation results

### Task Metadata

After Phase 2.7, task frontmatter is updated:
```yaml
complexity_evaluation:
  score: 5
  review_mode: quick_optional
  action: review_required
  routing: Phase 2.6 Checkpoint (Optional)
  auto_approved: false
  timestamp: 2024-10-09T12:34:56Z
  factors:
    - name: file_complexity
      score: 1
      max: 3
      justification: "Moderate change (4 files)"
    # ... other factors ...
  triggers: []
```

## Future Enhancements

**Deferred to TASK-003B**:
- Dependency complexity factor (external APIs, databases)
- Stack-specific scoring adjustments
- Historical complexity tracking
- Machine learning for pattern detection

**Deferred to Later**:
- Integration with decision log system
- Complexity trend analysis
- Team velocity correlation
- Automated threshold tuning

## Design Principles

1. **Strategy Pattern**: Isolated, testable scoring factors
2. **Fail-Safe Defaults**: Conservative when uncertain
3. **Type Safety**: Strong typing with dataclasses
4. **Separation of Concerns**: Calculator, router, utils are independent
5. **Extensibility**: Easy to add new factors or adjust thresholds
6. **Testability**: Pure functions, no side effects
7. **Logging**: Comprehensive debugging information

## Performance

**Target**: < 5 seconds for complexity evaluation
- Efficient regex-based parsing
- No external API calls
- No database queries
- Stateless evaluation (no caching needed)

## Version

**1.0.0** - Initial implementation for TASK-003A

## Authors

- AI Engineer (Agentecflow Platform)
- Architectural design reviewed and approved (Score: 82/100)

## License

Part of Agentecflow Platform - See project LICENSE
