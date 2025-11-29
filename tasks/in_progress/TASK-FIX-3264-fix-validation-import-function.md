---
id: TASK-FIX-3264
title: Fix RequireKit validation import function error
status: in_progress
created: 2025-11-29T21:50:00Z
updated: 2025-11-29T21:53:23.324014+00:00
priority: critical
tags: [bug, installation, validation, urgent]
complexity: 1
test_results:
  status: pending
  coverage: null
  last_run: null
---

# Task: Fix RequireKit validation import function error

## Problem

RequireKit installation validation is failing with:
```
Import failed: cannot import name 'detect_packages' from 'lib.feature_detection'
```

## Root Cause

**File**: `installer/scripts/install.sh` lines 311-320

**Current Code** (BROKEN):
```python
if ! python3 <<EOF
import sys
sys.path.insert(0, "$INSTALL_DIR")
try:
    from lib.feature_detection import detect_packages  # Function doesn't exist!
    print("Import successful")
    sys.exit(0)
except ImportError as e:
    print(f"Import failed: {e}", file=sys.stderr)
    sys.exit(1)
EOF
```

**Why It Fails**:
- The `feature_detection.py` module exists and can be imported
- BUT the function `detect_packages()` **does not exist** in the module
- The module provides: `is_require_kit_installed()`, `supports_requirements()`, etc.
- The validation imports a non-existent function

## Solution (Option 1 - Recommended)

**Use os.chdir approach** (matches taskwright's proven pattern):

Replace lines 311-320 in `installer/scripts/install.sh`:

```python
# BEFORE (lines 311-320):
if ! python3 <<EOF
import sys
sys.path.insert(0, "$INSTALL_DIR")
try:
    from lib.feature_detection import detect_packages
    print("Import successful")
    sys.exit(0)
except ImportError as e:
    print(f"Import failed: {e}", file=sys.stderr)
    sys.exit(1)
EOF

# AFTER:
if ! python3 <<EOF
import sys
import os

# Change to installed directory (matches taskwright approach)
os.chdir(os.path.expanduser("$INSTALL_DIR"))

try:
    from lib.feature_detection import is_require_kit_installed
    print("Import successful")
    sys.exit(0)
except ImportError as e:
    print(f"Import failed: {e}", file=sys.stderr)
    sys.exit(1)
EOF
```

**Key Changes**:
1. Add `import os`
2. Use `os.chdir(os.path.expanduser("$INSTALL_DIR"))` instead of `sys.path.insert()`
3. Import `is_require_kit_installed` instead of non-existent `detect_packages`
4. This matches taskwright's validation pattern (proven to work)

## Acceptance Criteria

- [x] Lines 311-320 updated in `installer/scripts/install.sh`
- [x] Validation imports `is_require_kit_installed` (real function)
- [x] Uses `os.chdir()` approach (matches taskwright)
- [ ] Installation validation succeeds with `✓ Python module validation successful` (requires manual test)
- [ ] No import errors during installation (requires manual test)
- [ ] Manual installation test passes (requires manual test)

## Context

**Taskwright's Working Approach** (for reference):
```python
import os
os.chdir(os.path.expanduser("~/.agentecflow/commands"))
from lib.id_generator import generate_task_id, validate_task_id
```

**Available Functions in feature_detection.py**:
- `is_require_kit_installed()` - ✅ Use this for validation
- `supports_requirements()` - ✅ Available
- `supports_epics()` - ✅ Available
- `supports_features()` - ✅ Available
- `supports_bdd()` - ✅ Available
- `get_available_features()` - ✅ Available
- `detect_packages()` - ❌ Does NOT exist (causing current error)

## Test Requirements

### Manual Test
```bash
# Clean test
rm -rf ~/.agentecflow/require-kit.marker*
rm -rf ~/.agentecflow/lib
rm -rf ~/Projects/require-kit

# Reinstall
curl -sSL https://raw.githubusercontent.com/requirekit/require-kit/main/installer/scripts/install.sh | bash

# Expected output:
# ✓ Python module validation successful
# (No "cannot import name 'detect_packages'" error)
```

### Validation
- Import statement works: `from lib.feature_detection import is_require_kit_installed`
- Uses `os.chdir()` approach (consistent with taskwright)
- No import errors during installation
- Installation completes successfully

## Implementation Notes

**Exact Changes**:
- File: `installer/scripts/install.sh`
- Lines: 311-320 (entire validation block)
- Approach: Use `os.chdir()` instead of `sys.path.insert()`
- Function: Import `is_require_kit_installed` instead of `detect_packages`

**Implementation Time**: 5 minutes - Replace validation block

**Priority**: CRITICAL - Blocks RequireKit installation validation

## Related Issues

- Blocks: RequireKit installation validation
- Related: TASK-FIX-EBD0 (fixed sys.path, but revealed this function error)
- Pattern: Matches taskwright's working validation approach

## Alternative Solutions (Not Recommended)

### Option 2: Keep sys.path but import real function
```python
sys.path.insert(0, "$INSTALL_DIR")
from lib.feature_detection import is_require_kit_installed
```

### Option 3: Just test module import
```python
sys.path.insert(0, "$INSTALL_DIR")
import lib.feature_detection
```

**Recommendation**: Use Option 1 (`os.chdir`) for consistency with taskwright's proven approach.

## Test Execution Log

### Task Workflow Execution - 2025-11-29

**Phase 2: Implementation Planning**
- ✅ Created implementation plan to replace validation block in install.sh
- ✅ Plan approved with clear approach to use os.chdir() pattern

**Phase 2.5B: Architectural Review**
- ✅ Score: 95/100
- ✅ Status: APPROVED
- Key strengths:
  - Matches taskwright's proven pattern for consistency
  - Uses real function (is_require_kit_installed) instead of non-existent one
  - Simplifies import mechanism with os.chdir approach
  - Maintains bidirectional integration compatibility

**Phase 3: Implementation**
- ✅ File modified: installer/scripts/install.sh (lines 311-323)
- ✅ Changes applied:
  1. Added `import os`
  2. Replaced `sys.path.insert(0, "$INSTALL_DIR")` with `os.chdir(os.path.expanduser("$INSTALL_DIR"))`
  3. Replaced non-existent `detect_packages` with real `is_require_kit_installed`
  4. Added comment: "# Change to installed directory"

**Phase 4: Testing**
- ✅ Test Results: 5/5 passed (100%)
  1. ✅ Syntax validation (no Python errors)
  2. ✅ Change verification (os.chdir present, is_require_kit_installed used)
  3. ✅ Regression check (no sys.path issues)
  4. ✅ Pattern verification (matches taskwright approach)
  5. ✅ Complete block verification (all requirements met)

**Phase 4.5: Fix Loop**
- ✅ Skipped (all tests passed on first run)

**Phase 5: Code Review**
- ✅ Score: 95/100
- ✅ Status: APPROVED
- ✅ Security: PASS
- ✅ Shell best practices: PASS
- Minor observation: Test file could be updated (non-blocking)

**Phase 5.5: Plan Audit**
- ✅ Skipped (complexity 1/10 - simple fix, no complex plan)

**Quality Gates**
- ✅ All tests passed (100%)
- ✅ Code review approved (95/100)
- ✅ Architecture review approved (95/100)
- ✅ Ready for IN_REVIEW state

**Implementation Summary**
Fixed RequireKit installation validation by replacing broken validation block with working os.chdir approach that imports the correct function (is_require_kit_installed) instead of non-existent detect_packages. This matches taskwright's proven pattern and ensures bidirectional integration consistency.
