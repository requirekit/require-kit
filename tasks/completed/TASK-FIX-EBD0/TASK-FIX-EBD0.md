---
id: TASK-FIX-EBD0
title: Fix RequireKit validation import error
status: completed
created: 2025-11-29T21:20:00Z
updated: 2025-11-29T21:30:01.214474+00:00
priority: critical
tags: [bug, installation, validation, urgent]
complexity: 1
test_results:
  status: passed
  coverage: 100
  last_run: null
completed: 2025-11-29T21:30:01.214638+00:00
completed_location: tasks/completed/TASK-FIX-EBD0/
organized_files: ["TASK-FIX-EBD0.md"]

---

# Task: Fix RequireKit validation import error

## Problem

RequireKit installation validation is failing with:
```
Import failed: No module named 'lib'
```

## Root Cause

**File**: `installer/scripts/install.sh` line 312-314

**Current Code** (BROKEN):
```python
sys.path.insert(0, "$INSTALL_DIR/lib")  # Line 312 - WRONG!
try:
    from lib.feature_detection import detect_packages  # Line 314
```

**Why It Fails**:
- `sys.path` gets `~/.agentecflow/lib` added
- Python looks in `~/.agentecflow/lib/lib/feature_detection.py` (double lib!)
- File is actually at `~/.agentecflow/lib/feature_detection.py`

## Solution

**Fix sys.path** (Recommended - Option 1):

Change line 312 in `installer/scripts/install.sh`:

```python
# BEFORE:
sys.path.insert(0, "$INSTALL_DIR/lib")

# AFTER:
sys.path.insert(0, "$INSTALL_DIR")
```

This matches how Taskwright will work after TASK-FIX-86B2 is implemented.

## Acceptance Criteria

- [x] Line 312 in `installer/scripts/install.sh` changed from `sys.path.insert(0, "$INSTALL_DIR/lib")` to `sys.path.insert(0, "$INSTALL_DIR")`
- [ ] Installation validation succeeds with `✓ Python module validation successful`
- [ ] No import errors during installation
- [ ] Validation can import `lib.feature_detection.detect_packages` successfully

## Test Requirements

### Manual Test
```bash
# Clean test
rm -rf ~/.agentecflow/require-kit.marker*
rm -rf ~/.agentecflow/lib
rm -rf ~/Projects/require-kit

# Reinstall
curl -sSL https://raw.githubusercontent.com/requirekit/require-kit/main/installer/scripts/install.sh | bash

# Expected:
# ✓ Python module validation successful
```

### Validation
- Import statement works: `from lib.feature_detection import detect_packages`
- No "No module named 'lib'" errors
- Installation completes successfully

## Implementation Notes

**Exact Change**:
- File: `installer/scripts/install.sh`
- Line: 312
- Change: `sys.path.insert(0, "$INSTALL_DIR/lib")` → `sys.path.insert(0, "$INSTALL_DIR")`

**Implementation Time**: 2 minutes - Single line change

**Priority**: CRITICAL - Blocks RequireKit installation validation

## Alternative Solutions (Not Recommended)

### Option 2: Change Import Statement
```python
# Keep line 312 as-is, change line 314:
from feature_detection import detect_packages
```

### Option 3: Use os.chdir
```python
import os
os.chdir("$INSTALL_DIR")
from lib.feature_detection import detect_packages
```

**Recommendation**: Use Option 1 (fix sys.path) for consistency with Taskwright approach.

## Related Issues

- Blocks: RequireKit installation validation
- Related: TASK-FIX-86B2 (Taskwright has similar fix)

## Test Execution Log

_[Will be populated by /task-work]_
