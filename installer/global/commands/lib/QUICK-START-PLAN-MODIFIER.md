# Quick Start Guide: Plan Modifier

## 2-Minute Quick Start

### What is Plan Modifier?

Plan Modifier allows you to interactively modify implementation plans during Phase 2.8 checkpoint before proceeding with implementation.

### When to Use It?

Use Plan Modifier when you want to:
- Add or remove files from the implementation plan
- Adjust dependencies or their versions
- Update risk assessments or mitigation strategies
- Revise effort estimates (duration, LOC, complexity)

### How to Use It?

**During Phase 2.8 Checkpoint:**

```
============================================================
PHASE 2.8: IMPLEMENTATION PLAN CHECKPOINT
============================================================

Task: TASK-029
Complexity: 7/10 (Complex - requires full review)

IMPLEMENTATION PLAN SUMMARY
========================================

Files to Change (3):
  - installer/global/commands/lib/plan_modifier.py (create)
  - installer/global/commands/lib/plan_persistence.py (modify)
  - installer/global/commands/lib/checkpoint_display.py (modify)

Dependencies (1):
  - python 3.7+ - Required for dataclasses

Risks (1):
  🟡 MEDIUM: Integration with existing checkpoint flow
    Mitigation: Careful testing of checkpoint loop

Effort Estimate:
  Duration: 4 hours
  Lines of Code: ~600
  Complexity: 7/10

============================================================
CHECKPOINT: Review implementation plan
============================================================

Options:
  [A]pprove  - Proceed with implementation
  [M]odify   - Adjust plan before implementation  ← SELECT THIS
  [C]ancel   - Stop task execution

Choice: M                                         ← TYPE 'M'
```

**Modification Session Starts:**

```
============================================================
PLAN MODIFICATION
============================================================

You can now modify the implementation plan before proceeding.
Changes will be saved with version tracking.

============================================================
Plan Modification Session for TASK-029
============================================================

Current Modifications: 0

What would you like to modify?
  1. Files (add/remove)
  2. Dependencies
  3. Risks
  4. Effort Estimate
  5. Undo Last Change
  6. Save and Exit
  7. Cancel (discard changes)

Choice: 1                                         ← SELECT CATEGORY
```

## Common Workflows

### 1. Add a New File

```
Choice: 1  (Files)

Files in Plan
=============

Files to Create (3):
  1. plan_modifier.py
  2. plan_persistence.py
  3. checkpoint_display.py

Options:
  1. Add file to create
  2. Remove file to create
  3. Add file to modify
  4. Remove file to modify
  5. Back to main menu

Choice: 1

Enter file path to create: tests/unit/test_plan_modifier.py
✓ Added 'tests/unit/test_plan_modifier.py' to files to create
```

### 2. Add a Dependency

```
Choice: 2  (Dependencies)

Dependencies in Plan
====================

External Dependencies (1):
  1. python 3.7+ - Required for dataclasses

Options:
  1. Add dependency
  2. Remove dependency
  3. Back to main menu

Choice: 1

Enter dependency information:
  Package name: pytest
  Version (optional): 7.0.0
  Purpose (optional): Unit testing framework
✓ Added dependency 'pytest 7.0.0 - Unit testing framework'
```

### 3. Add a Risk

```
Choice: 3  (Risks)

Risks in Plan
=============

Risks (1):
  1. MEDIUM: Integration with existing checkpoint flow
     Mitigation: Careful testing of checkpoint loop

Options:
  1. Add risk
  2. Remove risk
  3. Modify risk severity/mitigation
  4. Back to main menu

Choice: 1

Enter risk information:
  Risk description: Input validation may miss edge cases
  Severity (high/medium/low) [medium]: high
  Mitigation strategy (optional): Comprehensive unit tests with edge cases
✓ Added risk 'Input validation may miss edge cases'
```

### 4. Update Effort Estimate

```
Choice: 4  (Effort Estimate)

Effort Estimate
===============

Current Estimate:
  Duration: 4 hours
  Lines of Code: ~600
  Complexity: 7/10

Enter new values (press Enter to keep current):
  Duration (4 hours): 6 hours
  Lines of Code (600): 800
  Complexity (7): 8

✓ Effort estimate updated
```

### 5. Undo Last Change

```
Current Modifications: 4
  - FILES: add - Added tests/unit/test_plan_modifier.py
  - DEPENDENCIES: add - Added pytest 7.0.0
  - RISKS: add - Added HIGH risk: Input validation
  - EFFORT: modify - Updated effort: 6 hours, ~800 LOC, 8/10

Choice: 5  (Undo Last Change)

✓ Undone: EFFORT: modify - Updated effort: 6 hours, ~800 LOC, 8/10

Current Modifications: 3
  - FILES: add - Added tests/unit/test_plan_modifier.py
  - DEPENDENCIES: add - Added pytest 7.0.0
  - RISKS: add - Added HIGH risk: Input validation
```

### 6. Save and Exit

```
Choice: 6  (Save and Exit)

Modification Summary
====================

Total Modifications: 3
  - FILES: add - Added tests/unit/test_plan_modifier.py
  - DEPENDENCIES: add - Added pytest 7.0.0
  - RISKS: add - Added HIGH risk: Input validation

Plan version incremented: 1 → 2

Save modifications? (y/n): y

✓ Plan saved to: /path/to/docs/state/TASK-029/implementation_plan.md
✓ Version incremented: 1 → 2

============================================================
PLAN MODIFICATION COMPLETE
============================================================

✓ Implementation plan has been updated
✓ Previous version backed up to versions/ directory

Returning to checkpoint menu...
```

## Version History

After modifications, your plan versions are automatically backed up:

```
docs/state/TASK-029/
├── implementation_plan.md           ← Current version (v2)
└── versions/
    └── implementation_plan_v1_20251018_143022.md  ← Backup of v1
```

You can always review previous versions to see what changed.

## Tips

1. **Review Before Modifying**: Read the plan summary carefully before making changes
2. **Use Undo Freely**: If you make a mistake, just undo it
3. **Save Incrementally**: Make a few changes, save, then make more if needed
4. **Check Backups**: Previous versions are always saved, so you can't lose data
5. **Press Enter to Keep**: When updating effort, press Enter to keep current values

## Keyboard Shortcuts

- **Ctrl+C**: Cancel modification session (same as choosing 'Cancel')
- **Enter**: Keep current value when updating effort estimates
- **c**: Cancel removal operations (when selecting item to remove)

## Error Handling

The modifier handles common issues gracefully:

- **Empty Input**: "Field cannot be empty" - you'll be prompted again
- **Invalid Number**: "Invalid number" - you'll be prompted again
- **Out of Range**: "Must be 1-10" - you'll be prompted again
- **Ctrl+C**: Session cancelled, no changes saved
- **EOF**: Session cancelled, no changes saved

## Integration with Task Workflow

The Plan Modifier is seamlessly integrated into the `/task-work` command:

```bash
# Run task with design-only flag
/task-work TASK-029 --design-only

# Phase 2.8 checkpoint displays
# Choose [M]odify to adjust the plan
# Make your modifications
# Save and exit

# Continue with implementation using modified plan
/task-work TASK-029 --implement-only
```

## Further Reading

- **Complete Documentation**: See `README-PLAN-MODIFIER.md`
- **Implementation Details**: See `TASK-029-IMPLEMENTATION-SUMMARY.md`
- **API Reference**: See docstrings in `plan_modifier.py`

## Support

For issues or questions:
1. Check the comprehensive README: `README-PLAN-MODIFIER.md`
2. Review the implementation summary: `TASK-029-IMPLEMENTATION-SUMMARY.md`
3. Examine the source code docstrings in `plan_modifier.py`
