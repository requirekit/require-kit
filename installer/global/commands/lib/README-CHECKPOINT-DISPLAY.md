# Checkpoint Display Module - Quick Reference

## Overview

The `checkpoint_display` module provides enhanced Phase 2.8 checkpoint display with implementation plan summary. It loads saved plans and presents them in a user-friendly format for human review.

## Quick Start

```python
from checkpoint_display import display_phase28_checkpoint

# Display checkpoint with plan
display_phase28_checkpoint(
    task_id="TASK-042",
    complexity_score=7,
    plan_path=None  # Uses standard location: docs/state/TASK-042/implementation_plan.md
)
```

## Core Components

### Dataclasses

```python
@dataclass
class FileChange:
    """File to be created or modified."""
    path: str
    description: str  # Auto-truncated to 80 chars
    change_type: str = "create"  # "create" or "modify"

@dataclass
class Dependency:
    """External dependency required."""
    name: str
    version: Optional[str] = None
    purpose: Optional[str] = None

@dataclass
class Risk:
    """Implementation risk."""
    description: str
    level: RiskLevel  # HIGH, MEDIUM, LOW
    mitigation: Optional[str] = None

@dataclass
class EffortEstimate:
    """Effort estimation."""
    duration: str  # e.g., "4 hours"
    lines_of_code: int
    complexity_score: int  # 1-10

@dataclass
class PlanSummary:
    """Complete plan summary."""
    task_id: str
    files_to_change: List[FileChange]
    dependencies: List[Dependency]
    risks: List[Risk]
    effort: Optional[EffortEstimate]
    test_summary: Optional[str]
    phases: List[str]
```

### Key Functions

```python
def load_plan_summary(
    task_id: str,
    plan_path: Optional[Path] = None
) -> Optional[PlanSummary]:
    """Load plan and convert to PlanSummary."""
    pass

def format_plan_summary(
    summary: PlanSummary,
    max_files: int = 5,
    max_deps: int = 3
) -> str:
    """Format summary as human-readable text."""
    pass

def display_phase28_checkpoint(
    task_id: str,
    complexity_score: int,
    plan_path: Optional[Path] = None
) -> None:
    """Display complete checkpoint with plan."""
    pass
```

## Display Format

### With Plan

```
============================================================
PHASE 2.8: IMPLEMENTATION PLAN CHECKPOINT
============================================================

Task: TASK-042
Complexity: 7/10 (Complex - requires full review)

IMPLEMENTATION PLAN SUMMARY
========================================

Files to Change (4):
  - src/checkpoint_display.py (create)
  - tests/test_checkpoint.py (create)
  - src/plan_persistence.py (modify)
  - README.md (modify)

Dependencies (2):
  - pytest (7.0.0)
  - pydantic (2.0.0)

Risks (2):
  🔴 HIGH: Security vulnerability
    Mitigation: Security audit required
  🟡 MEDIUM: External API dependency
    Mitigation: Add retry logic

Effort Estimate:
  Duration: 4 hours
  Lines of Code: ~250
  Complexity: 7/10

Testing Approach:
  Unit tests for all functions, integration tests for API

Plan file: docs/state/TASK-042/implementation_plan.md
View with: cat docs/state/TASK-042/implementation_plan.md

============================================================
CHECKPOINT: Review implementation plan
============================================================

Options:
  [A]pprove  - Proceed with implementation
  [M]odify   - Adjust plan and regenerate
  [C]ancel   - Stop task execution
```

### Without Plan (High Complexity)

```
============================================================
PHASE 2.8: IMPLEMENTATION PLAN CHECKPOINT
============================================================

Task: TASK-042
Complexity: 8/10 (Complex - requires full review)

⚠️  No implementation plan found
WARNING: Complex task without saved plan - consider running with --design-only first

============================================================
CHECKPOINT: Review implementation plan
============================================================

Options:
  [A]pprove  - Proceed with implementation
  [M]odify   - Adjust plan and regenerate
  [C]ancel   - Stop task execution
```

## Display Rules

### Truncation
- **Files**: Show first 5, then "... and N more"
- **Dependencies**: Show first 3, then "... and N more"
- **File Descriptions**: Truncate at 80 chars with "..."

### Section Skipping
Empty sections are automatically hidden:
- No dependencies → skip "Dependencies" section
- No risks → skip "Risks" section
- No effort → skip "Effort Estimate" section
- No test summary → skip "Testing Approach" section

### Risk Severity Icons
- 🔴 HIGH: Critical risks requiring mitigation
- 🟡 MEDIUM: Moderate risks with optional mitigation
- 🟢 LOW: Minor risks, informational

### Review Mode Display
- **Complexity 1-3**: "Simple - auto-proceed"
- **Complexity 4-6**: "Medium - quick review"
- **Complexity 7-10**: "Complex - requires full review"

## Error Handling

### Graceful Degradation
```python
# Missing plan file
summary = load_plan_summary("TASK-XXX")
# Returns: None (no exception)

# Invalid JSON
summary = load_plan_summary("TASK-XXX", plan_path=Path("invalid.json"))
# Returns: None (logged warning)

# Empty plan section
summary = load_plan_summary("TASK-XXX", plan_path=Path("empty.json"))
# Returns: None (logged warning)
```

### Logging
```python
import logging
logger = logging.getLogger(__name__)

# Warnings for missing data
logger.warning(f"Unknown risk level '{level}', defaulting to MEDIUM")

# Errors for failures
logger.error(f"Failed to load plan summary for {task_id}: {e}")
```

## Integration Examples

### From task-work.md Phase 2.8
```python
from checkpoint_display import display_phase28_checkpoint

# In Phase 2.8 checkpoint
display_phase28_checkpoint(
    task_id=task_id,
    complexity_score=complexity_result.total_score
)

# Get user input
choice = input("Your choice [A/M/C]: ").strip().upper()
if choice == "A":
    proceed_to_phase_3()
elif choice == "M":
    modify_plan()
elif choice == "C":
    cancel_task()
```

### From phase_execution.py
```python
from checkpoint_display import load_plan_summary, format_plan_summary

# Load summary for processing
summary = load_plan_summary(task_id)
if summary:
    # Check for high risks
    if summary.has_high_risks:
        logger.warning(f"Task {task_id} has HIGH risks")

    # Get formatted display
    formatted = format_plan_summary(summary)
    print(formatted)
```

## Testing

### Unit Tests
```bash
pytest tests/unit/test_checkpoint_display.py -v
```

### Integration Tests
```bash
pytest tests/integration/test_plan_loading.py -v
```

### E2E Tests
```bash
pytest tests/e2e/test_phase28_checkpoint.py -v
```

### All Tests
```bash
pytest tests/unit/test_checkpoint_display.py \
       tests/integration/test_plan_loading.py \
       tests/e2e/test_phase28_checkpoint.py -v
```

## Common Patterns

### Check Plan Existence
```python
from plan_persistence import plan_exists

if plan_exists(task_id):
    display_phase28_checkpoint(task_id, complexity_score)
else:
    print("No plan found - run with --design-only first")
```

### Load and Inspect Summary
```python
summary = load_plan_summary(task_id)
if summary:
    print(f"Files: {summary.total_files}")
    print(f"High risks: {summary.has_high_risks}")
    print(f"Estimated: {summary.effort.duration}")
```

### Format for Display
```python
summary = load_plan_summary(task_id)
if summary:
    # Custom truncation
    formatted = format_plan_summary(
        summary,
        max_files=10,  # Show more files
        max_deps=5     # Show more dependencies
    )
    print(formatted)
```

## Dependencies

### Required Modules
- `plan_persistence` - Plan loading and existence checking
- `pathlib` - Path operations
- `dataclasses` - Data structure definitions
- `enum` - RiskLevel enum
- `logging` - Error and warning logging
- `typing` - Type hints

### Optional Modules
- `plan_markdown_parser` - Markdown plan parsing (via plan_persistence)
- `jinja2` - Template rendering (via plan_markdown_renderer)

## File Locations

- **Module**: `installer/global/commands/lib/checkpoint_display.py`
- **Unit Tests**: `tests/unit/test_checkpoint_display.py`
- **Integration Tests**: `tests/integration/test_plan_loading.py`
- **E2E Tests**: `tests/e2e/test_phase28_checkpoint.py`
- **Plans**: `docs/state/{task_id}/implementation_plan.md` (or `.json`)

## Version History

- **v1.0.0** (2025-10-18): Initial implementation (TASK-028)
  - Core dataclasses
  - Plan loading and formatting
  - Checkpoint display
  - Comprehensive test suite

## Support

For issues or questions:
1. Check test files for usage examples
2. Review TASK-028-IMPLEMENTATION-SUMMARY.md
3. Examine existing plan files in docs/state/
4. Contact: Claude (Anthropic)
