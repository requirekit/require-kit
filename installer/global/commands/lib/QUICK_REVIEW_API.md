# Quick Review Mode API Reference

## Module: `user_interaction.py`

### countdown_timer()

Non-blocking countdown timer with keyboard input handling.

```python
from user_interaction import countdown_timer

result = countdown_timer(
    duration_seconds=10,
    message="Quick review mode active.",
    options="Press [Enter] to see full review, [C] to cancel, or wait to auto-proceed"
)

# Returns: "timeout" | "enter" | "cancel"
```

**Parameters**:
- `duration_seconds` (int): Countdown length (>0)
- `message` (str): Primary message displayed above countdown
- `options` (str): Help text describing available actions
- `cancel_key` (str): Key to cancel (default 'c', case-insensitive)

**Returns**: `CountdownResult` = `Literal["timeout", "enter", "cancel"]`

**Raises**:
- `ValueError`: If duration_seconds ≤ 0
- `KeyboardInterrupt`: On Ctrl+C (emergency exit)

**Platform Support**:
- Unix/macOS: Uses `select()` and `termios` (non-blocking raw input)
- Windows: Uses `msvcrt.kbhit()` and `msvcrt.getch()`

---

## Module: `review_modes.py`

### QuickReviewHandler

Main coordinator for Quick Review Mode workflow.

```python
from review_modes import QuickReviewHandler
from complexity_models import ImplementationPlan

handler = QuickReviewHandler(
    task_id="TASK-001",
    plan=implementation_plan,
    countdown_duration=10  # Optional, default=10
)

result = handler.execute()
```

**Methods**:

#### `execute() -> QuickReviewResult`
Execute complete quick review workflow:
1. Display summary card
2. Start countdown timer
3. Handle user input
4. Return result with metadata

**Returns**: `QuickReviewResult` with:
- `action`: "timeout" | "enter" | "cancel"
- `timestamp`: ISO 8601 timestamp
- `auto_approved`: Boolean
- `metadata_updates`: Dict for task tracking

#### `save_result(result, output_path=None)`
Save review result to JSON file for audit trail.

---

### QuickReviewDisplay

Terminal UI renderer for summary cards.

```python
from review_modes import QuickReviewDisplay

display = QuickReviewDisplay(plan=implementation_plan)
display.render_summary_card()
```

**Methods**:

#### `format_complexity_badge() -> str`
Format score as colored badge (e.g., "[SCORE: 87/100 - Excellent]")

#### `format_file_summary() -> str`
Format file count (e.g., "3 files (300 lines)")

#### `render_summary_card()`
Display complete summary to console with:
- Complexity score badge
- File creation summary
- Implementation instructions (truncated)
- Key patterns (top 3)
- Warnings (if any)

---

### QuickReviewResult

Dataclass representing review outcome.

```python
from review_modes import QuickReviewResult

result = QuickReviewResult(
    action="timeout",
    timestamp="2025-10-09T10:30:00Z",
    auto_approved=True,
    metadata_updates={
        "review_mode": "quick_review",
        "review_action": "auto_approved",
        "complexity_score": 87
    }
)

# Serialize
data = result.to_dict()

# Deserialize
restored = QuickReviewResult.from_dict(data)
```

---

## Complete Workflow Example

```python
from review_modes import QuickReviewHandler
from complexity_models import ImplementationPlan

def quick_review_workflow(task_id: str, plan: ImplementationPlan):
    """Execute quick review for a task."""

    # 1. Create handler
    handler = QuickReviewHandler(
        task_id=task_id,
        plan=plan,
        countdown_duration=10
    )

    # 2. Execute review (displays summary + countdown)
    try:
        result = handler.execute()
    except KeyboardInterrupt:
        print("\nReview interrupted by user")
        return None

    # 3. Handle result
    if result.action == "timeout":
        # Auto-approved: Proceed to implementation
        print(f"✅ Auto-approved (score: {plan.complexity_score.total_score})")
        return {"proceed": True, "metadata": result.metadata_updates}

    elif result.action == "enter":
        # Escalate to full review
        print("📋 Escalating to full review...")
        # Call FullReviewHandler here
        return {"proceed": False, "needs_full_review": True}

    elif result.action == "cancel":
        # User cancelled task
        print("❌ Task cancelled by user")
        return {"proceed": False, "cancelled": True}

    # 4. Save result for audit
    handler.save_result(result)

    return result
```

---

## Error Handling

### Fail-Safe Escalation

All errors during quick review automatically escalate to full review:

```python
try:
    result = handler.execute()
except Exception as e:
    # Automatically escalates on any error
    # Returns result with action="enter"
    print(f"Error: {e}")
    print("Escalating to full review for safety...")
```

### Terminal State Restoration

Terminal state is **always** restored via context managers:

```python
with managed_input_strategy() as strategy:
    # Terminal in raw mode
    key = strategy.check_input()
# Terminal automatically restored here (even on exceptions)
```

---

## Testing

### Run Test Suite

```bash
python3 installer/global/commands/lib/test_quick_review.py
```

### Mock Usage in Tests

```python
from unittest.mock import Mock, patch

# Mock countdown_timer for testing
with patch('lib.review_modes.countdown_timer', return_value="timeout"):
    result = handler.execute()
    assert result.action == "timeout"
    assert result.auto_approved is True
```

---

## Integration Points

### Input (from Phase 2 - Implementation Planning)
- `ImplementationPlan`: Contains files, patterns, dependencies
- `ComplexityScore`: Contains total_score, metadata, patterns

### Output (to Phase 3 - Implementation or Full Review)
- `QuickReviewResult`: Contains action, timestamp, metadata_updates
- Task metadata updates for state tracking

### Dependencies
- `complexity_models.py`: Data structures for plans and scores
- Python stdlib: `sys`, `time`, `select`, `termios`, `msvcrt`, `datetime`, `json`, `pathlib`

---

## Platform Compatibility

| Platform | Input Method | Terminal Mode | Status |
|----------|--------------|---------------|--------|
| macOS | `select()` + `termios` | Raw mode | ✅ Tested |
| Linux | `select()` + `termios` | Raw mode | ✅ Expected to work |
| Windows | `msvcrt` | Console API | ⚠️ Untested (should work) |

---

## Performance Characteristics

- **Countdown Accuracy**: ±100ms (tested at 1.02s for 1s countdown)
- **Key Response Time**: 50-110ms (excellent UX)
- **Polling Interval**: 50ms (configurable in countdown_timer)
- **Memory Overhead**: Minimal (context managers, no persistent state)

---

## Future Enhancements

### TASK-003B-2 (Full Review Mode)
- Detailed complexity breakdown display
- File-by-file review workflow
- Comment and approval system
- Enhanced formatting with ANSI colors

### TASK-003B-3 (Router Integration)
- Automatic mode selection (auto/quick/full)
- Human checkpoint triggering
- Integration with task-work command
- Progress tracking and resumption

---

## Support

For questions or issues, refer to:
- Main implementation: `user_interaction.py`, `review_modes.py`
- Test suite: `test_quick_review.py`
- Architecture docs: TASK-003B-1 Phase 2 architectural review (Score: 87/100)
