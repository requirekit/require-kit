# Plan Review System - Quick Start Guide

## Installation

```bash
# Install dependencies
pip install pydantic

# Verify installation
python3 verify_task_003d.py
```

## Basic Usage

### 1. Configuration

```python
from installer.global.lib.config import PlanReviewConfig

config = PlanReviewConfig()

# Check if enabled
if config.is_enabled():
    # Get decision for a score
    decision = config.get_threshold(75, stack='python')
    print(f"Decision: {decision}")
```

### 2. Track Metrics

```python
from installer.global.lib.metrics import PlanReviewMetrics

metrics = PlanReviewMetrics()

# Track complexity
metrics.track_complexity(
    task_id='TASK-001',
    complexity_score=35,
    factors={'file_count': 5},
    stack='python'
)

# Track decision
metrics.track_decision(
    task_id='TASK-001',
    architectural_score=73,
    decision='approve_with_recommendations',
    complexity_score=35,
    stack='python'
)
```

### 3. View Dashboard

```python
from installer.global.lib.metrics import PlanReviewDashboard

dashboard = PlanReviewDashboard()
dashboard.print_dashboard(days=30)
```

## Configuration Precedence

1. **CLI Arguments** (highest)
   ```python
   config.set_cli_override('thresholds.auto_approve', 85)
   ```

2. **Environment Variables**
   ```bash
   export PLAN_REVIEW_ENABLED=true
   export PLAN_REVIEW_MODE=auto
   export PLAN_REVIEW_AUTO_APPROVE_THRESHOLD=85
   ```

3. **Settings.json**
   ```json
   {
     "plan_review": {
       "enabled": true,
       "default_mode": "auto",
       "thresholds": {
         "default": {
           "auto_approve": 80
         }
       }
     }
   }
   ```

4. **Defaults** (lowest)

## Key Settings

### Thresholds
- **Auto-approve**: ≥80 (proceed without review)
- **Approve with recommendations**: 60-79 (proceed with notes)
- **Reject**: <60 (block and revise)

### Review Modes
- **auto**: Review if complexity ≥30 or force triggers
- **always**: Review every task
- **never**: Skip all reviews

### Force Triggers
- Complexity ≥30
- Critical keywords: security, database, payment, etc.

## Common Tasks

### Disable Reviews Temporarily
```bash
export PLAN_REVIEW_ENABLED=false
```

### Change Auto-Approve Threshold
```python
config.set_cli_override('thresholds.auto_approve', 85)
```

### View Last 7 Days
```python
dashboard.print_dashboard(days=7)
```

### Check Review Status
```python
if config.should_force_review(complexity=35, keywords=['database']):
    print("Review required!")
```

## Troubleshooting

### Import Errors
```bash
pip install pydantic
```

### Configuration Not Loading
```python
config.reload()  # Force reload from all sources
```

### Metrics Not Saving
- Check: `config.is_metrics_enabled()`
- Check: `docs/state/metrics/` directory exists
- Check: Write permissions

## File Locations

- **Config**: `.claude/settings.json`
- **Metrics**: `docs/state/metrics/plan_review_metrics.jsonl`
- **Modules**: `installer/global/lib/`

## Examples

See `examples/plan_review_usage.py` for complete examples.

## Documentation

- Full docs: `docs/TASK-003D-IMPLEMENTATION.md`
- Summary: `TASK-003D-SUMMARY.md`
- Verification: `python3 verify_task_003d.py`
