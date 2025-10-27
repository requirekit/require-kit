# Agentecflow Library - Plan Review System

## Overview

This library provides the Configuration & Metrics System for the Agentecflow plan review workflow. It enables complexity-based architectural review decisions with configurable thresholds and comprehensive metrics tracking.

## Modules

### utils/
**Shared utilities following DRY principles**

- `json_serializer.py`: JSON operations with error handling
- `file_operations.py`: Atomic file operations
- `path_resolver.py`: Consistent path resolution

### config/
**Configuration management with 4-layer precedence**

- `defaults.py`: Default configuration values
- `config_schema.py`: Pydantic validation models
- `plan_review_config.py`: Singleton configuration manager

**Precedence**: CLI > ENV > Settings.json > Defaults

### metrics/
**Metrics tracking and visualization**

- `metrics_storage.py`: JSONL-based persistence
- `plan_review_metrics.py`: High-level tracking API
- `plan_review_dashboard.py`: Terminal dashboard

## Installation

```bash
pip install pydantic>=2.0.0
```

## Usage

### Configuration

```python
from config import PlanReviewConfig

config = PlanReviewConfig()

# Check if enabled
if config.is_enabled():
    # Get decision for score
    decision = config.get_threshold(75, stack='python')

    # Check force triggers
    forced = config.should_force_review(complexity=35, keywords=['database'])
```

### Metrics

```python
from metrics import PlanReviewMetrics, PlanReviewDashboard

# Track metrics
metrics = PlanReviewMetrics()
metrics.track_complexity(task_id, score, factors, stack)
metrics.track_decision(task_id, arch_score, decision, complexity, stack)
metrics.track_outcome(task_id, decision, override, duration, status, stack)

# View dashboard
dashboard = PlanReviewDashboard()
dashboard.print_dashboard(days=30)
```

## Architecture

### YAGNI Simplifications (MVP)
- ❌ No buffering (direct writes)
- ❌ No HTML export (terminal only)
- ❌ No auto-rollups (on-demand)
- ❌ No threading (simplified)

### DRY Principles
- ✅ Shared utilities module
- ✅ Centralized path resolution
- ✅ Reusable validators
- ✅ Common error handling

### Quality Standards
- ✅ Full type hints
- ✅ Google-style docstrings
- ✅ Graceful error handling
- ✅ pathlib.Path usage
- ✅ ISO 8601 timestamps
- ✅ PEP 8 compliant

## Testing

```bash
# Verify installation
cd ../../../
python3 verify_task_003d.py

# Test imports
python3 test_imports.py

# View examples
python3 examples/plan_review_usage.py
```

## Configuration Files

- **Settings**: `.claude/settings.json` (plan_review section)
- **Metrics**: `docs/state/metrics/plan_review_metrics.jsonl`

## Documentation

- **Implementation**: `docs/TASK-003D-IMPLEMENTATION.md`
- **Quick Start**: `docs/PLAN-REVIEW-QUICKSTART.md`
- **Summary**: `TASK-003D-SUMMARY.md`

## Code Statistics

- **Total Lines**: 1,396
- **Modules**: 3 (utils, config, metrics)
- **Classes**: 9
- **Functions**: 50+

## Dependencies

- **pydantic**: >=2.0.0 (schema validation)
- **Python**: >=3.11 (type hints, modern features)

## Integration

This library integrates with the task-work workflow at Phase 2.7 (Determine Review Necessity):

```python
from lib.config import PlanReviewConfig
from lib.metrics import PlanReviewMetrics

# In task-work Phase 2.7
config = PlanReviewConfig()
metrics = PlanReviewMetrics()

# Determine if review needed
if config.is_enabled() and config.should_force_review(complexity, keywords):
    # Track complexity
    metrics.track_complexity(task_id, complexity, factors, stack)

    # Run architectural review
    arch_score = architectural_reviewer.review(plan)

    # Get decision
    decision = config.get_threshold(arch_score, stack)

    # Track decision and outcome
    metrics.track_decision(...)
    metrics.track_outcome(...)
```

## License

Part of the Agentecflow AI-Engineer project.

## Support

For issues or questions, see:
- Verification: `python3 verify_task_003d.py`
- Examples: `examples/plan_review_usage.py`
- Docs: `docs/TASK-003D-IMPLEMENTATION.md`
