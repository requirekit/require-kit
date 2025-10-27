# Plan Modifier Implementation

## Overview

The Plan Modifier module provides interactive modification capabilities for implementation plans during Phase 2.8 checkpoint. It allows users to adjust files, dependencies, risks, and effort estimates before proceeding with implementation.

**Implemented for:** TASK-029: Add "Modify Plan" Option to Phase 2.8 Checkpoint

## Architecture

### Components

1. **plan_modifier.py** (~600 lines)
   - `ModificationCategory` - Enum for modification types
   - `ModificationRecord` - Tracks individual modifications
   - `ModificationSession` - Manages modification session state
   - `PlanModifier` - Main orchestrator class
   - `PlanModificationError` - Exception handling

2. **plan_persistence.py** (+60 lines)
   - `save_plan_version()` - Save plan with version increment
   - `_backup_plan_version()` - Create timestamped backups

3. **checkpoint_display.py** (+80 lines)
   - `handle_modify_option()` - Entry point for modification workflow
   - Updated `display_phase28_checkpoint()` to show [M]odify option

## Usage

### Interactive Workflow

```python
from checkpoint_display import handle_modify_option

# From Phase 2.8 checkpoint
if user_choice == 'M':
    success = handle_modify_option(task_id)
    if success:
        # Proceed with modified plan
        proceed_to_implementation()
    else:
        # Return to checkpoint menu
        show_checkpoint_menu()
```

### Direct Modification

```python
from plan_modifier import PlanModifier

# Create modifier
modifier = PlanModifier("TASK-029")

# Run interactive session
updated_plan = modifier.run_interactive_session()

if updated_plan:
    print(f"Plan modified with {len(updated_plan['modifications'])} changes")
```

## Features

### 1. File Modifications
- Add files to create
- Remove files to create
- Add files to modify
- Remove files to modify

```
Files in Plan
=============

Files to Create (2):
  1. src/feature.py
  2. tests/test_feature.py

Files to Modify (1):
  1. src/existing.py

Options:
  1. Add file to create
  2. Remove file to create
  3. Add file to modify
  4. Remove file to modify
  5. Back to main menu
```

### 2. Dependency Modifications
- Add dependencies with version and purpose
- Remove dependencies
- Format: "package version - purpose"

```
Dependencies in Plan
====================

External Dependencies (2):
  1. requests 2.28.0 - HTTP client
  2. pytest 7.0.0 - Testing framework

Options:
  1. Add dependency
  2. Remove dependency
  3. Back to main menu
```

### 3. Risk Modifications
- Add risks with severity (high/medium/low)
- Remove risks
- Modify risk severity and mitigation

```
Risks in Plan
=============

Risks (2):
  1. HIGH: Security vulnerability in authentication
     Mitigation: Use industry-standard libraries
  2. MEDIUM: Performance degradation with large datasets

Options:
  1. Add risk
  2. Remove risk
  3. Modify risk severity/mitigation
  4. Back to main menu
```

### 4. Effort Estimate Modifications
- Update duration (human-readable)
- Update lines of code (integer)
- Update complexity score (1-10)

```
Effort Estimate
===============

Current Estimate:
  Duration: 4 hours
  Lines of Code: ~300
  Complexity: 5/10

Enter new values (press Enter to keep current):
  Duration (4 hours): 6 hours
  Lines of Code (300): 400
  Complexity (5): 6

✓ Effort estimate updated
```

### 5. Undo Support
- Undo last modification
- Reverts changes to previous state
- Maintains modification history

```
✓ Undone: FILES: add - Added src/new_module.py
```

### 6. Modification Summary
- Shows all modifications before saving
- Confirmation before finalizing
- Version increment tracking

```
Modification Summary
====================

Total Modifications: 4
  - FILES: add - Added src/new_module.py to create
  - DEPENDENCIES: add - Added requests 2.28.0 - HTTP client
  - RISKS: add - Added HIGH risk: Security vulnerability
  - EFFORT: modify - Updated effort: 6 hours, ~400 LOC, complexity 6/10

Plan version incremented: 1 → 2

Save modifications? (y/n):
```

## Version Management

### Automatic Versioning

When modifications are saved:

1. **Backup Creation**
   - Current plan backed up to `docs/state/{task_id}/versions/`
   - Filename format: `implementation_plan_v{version}_{timestamp}.md`
   - Example: `implementation_plan_v1_20251018_143022.md`

2. **Version Increment**
   - Plan version number incremented: v1 → v2 → v3
   - Version stored in plan frontmatter metadata

3. **Modification History**
   - All modifications tracked in `modification_history` field
   - Each modification includes category, action, and details

### Version Directory Structure

```
docs/state/TASK-029/
├── implementation_plan.md           # Current version
└── versions/
    ├── implementation_plan_v1_20251018_143022.md
    ├── implementation_plan_v2_20251018_151530.md
    └── implementation_plan_v3_20251018_163045.md
```

## Error Handling

### Graceful Degradation

1. **Load Failures**
   - PlanModificationError raised if plan cannot be loaded
   - Clear error messages displayed to user

2. **Save Failures**
   - Backup failure doesn't prevent save (warning logged)
   - Save failure raises PlanPersistenceError

3. **User Interruption**
   - Ctrl+C / EOF handled gracefully
   - Returns to checkpoint menu without saving

### Validation

- File paths validated (non-empty)
- Dependency names validated (non-empty)
- Risk descriptions validated (non-empty)
- Complexity score validated (1-10 range)
- Numeric inputs validated (LOC must be integer)

## Integration Points

### Phase 2.8 Checkpoint

The modification workflow integrates with Phase 2.8 checkpoint:

```python
# In task-work command Phase 2.8 checkpoint
display_phase28_checkpoint(task_id, complexity_score)

choice = input("Choice [A/M/C]: ").strip().upper()

if choice == 'A':
    # Approve - proceed to implementation
    proceed_to_phase_3()
elif choice == 'M':
    # Modify - launch modification workflow
    if handle_modify_option(task_id):
        # Modifications saved, return to checkpoint
        display_phase28_checkpoint(task_id, complexity_score)
    else:
        # Modifications cancelled, return to checkpoint
        display_phase28_checkpoint(task_id, complexity_score)
elif choice == 'C':
    # Cancel - stop task execution
    cancel_task()
```

### Existing Modules

**plan_persistence.py**
- Uses `load_plan()` to load current plan
- Uses `save_plan_version()` to save modified plan
- Uses `get_plan_path()` for backup operations

**plan_markdown_parser.py**
- Parses markdown plans (no changes needed)
- Modifications work with existing plan structure

**plan_markdown_renderer.py**
- Renders plans to markdown (no changes needed)
- Modification history included in frontmatter

## Testing Strategy

### Unit Tests

1. **plan_modifier.py**
   - Test each modification category independently
   - Test undo functionality
   - Test session state management
   - Test error handling

2. **plan_persistence.py**
   - Test `save_plan_version()` creates backups
   - Test version increment
   - Test modification history tracking

3. **checkpoint_display.py**
   - Test `handle_modify_option()` workflow
   - Test integration with PlanModifier
   - Test error handling

### Integration Tests

1. **End-to-End Workflow**
   - Load plan → modify → save → verify backup
   - Multiple modification rounds
   - Undo and redo scenarios

2. **Checkpoint Integration**
   - Display checkpoint → modify → return to checkpoint
   - Verify plan updated correctly
   - Verify version tracking

### Manual Testing

1. **Interactive Session**
   - Run through all modification categories
   - Test undo at each step
   - Verify user prompts and error messages

2. **Version History**
   - Create multiple versions
   - Verify backups created correctly
   - Verify version numbers increment

## Performance Considerations

### Memory Efficiency

- Plan data kept in memory during session (typically < 100KB)
- Modification records are lightweight dataclasses
- No need for database or complex storage

### File I/O

- Single read on session start
- Single write on session end
- Backup operation is async-safe (copy2)

### User Experience

- Clear prompts and validation messages
- Immediate feedback on modifications
- Progress displayed throughout session

## Security Considerations

### Input Validation

- All user inputs validated before processing
- File paths sanitized (no directory traversal)
- Numeric inputs type-checked and range-validated

### Data Integrity

- Original plan preserved until save confirmed
- Backup created before overwriting
- Atomic save operations (temp file + rename)

## Future Enhancements

### Potential Improvements (not in current scope)

1. **Search/Filter**
   - Search for specific files/dependencies/risks
   - Filter by category or severity

2. **Batch Operations**
   - Add multiple files at once
   - Remove all dependencies matching pattern

3. **Diff View**
   - Show side-by-side comparison of versions
   - Highlight changed sections

4. **Revert to Version**
   - Roll back to previous version
   - Preview version before reverting

5. **Collaborative Editing**
   - Conflict detection for concurrent modifications
   - Merge strategies for conflicting changes

## Dependencies

### Required Packages

- `dataclasses` (Python 3.7+)
- `enum` (Python standard library)
- `pathlib` (Python 3.4+)
- `logging` (Python standard library)
- `datetime` (Python standard library)
- `shutil` (Python standard library)

### Module Dependencies

- `plan_persistence` - Load/save plan operations
- `plan_markdown_parser` - Parse markdown plans
- `plan_markdown_renderer` - Render plans to markdown

## Documentation

### Code Documentation

- Comprehensive docstrings for all public functions
- Type hints for all function signatures
- Inline comments for complex logic

### User Documentation

- Interactive help text in each menu
- Clear option descriptions
- Example outputs in docstrings

## Changelog

### Version 1.0 (2025-10-18)

**Initial implementation for TASK-029:**

- ✅ Phase 1: Core Modifier Module
  - `plan_modifier.py` created
  - All modification categories implemented
  - Undo support added
  - Session management complete

- ✅ Phase 2: Versioning Support
  - `save_plan_version()` added to plan_persistence.py
  - `_backup_plan_version()` implemented
  - Modification history tracking added

- ✅ Phase 3: Checkpoint Integration
  - `handle_modify_option()` added to checkpoint_display.py
  - Updated checkpoint menu to show [M]odify option
  - Integration with PlanModifier complete

**Compliance with Architectural Review:**
- SOLID principles: 88% compliance
- DRY principles: 88% compliance
- YAGNI: Deferred optional features as recommended

## Support

For issues or questions about the Plan Modifier implementation:

1. Check this README for usage examples
2. Review docstrings in source code
3. Examine unit tests for additional examples
4. Check TASK-029 documentation for design decisions

## License

Part of the AI-Engineer project. See project LICENSE for details.
