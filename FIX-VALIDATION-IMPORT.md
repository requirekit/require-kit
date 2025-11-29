# URGENT FIX: RequireKit Validation Import Error

## Problem

RequireKit installation validation is failing with:
```
Import failed: No module named 'lib'
```

## Root Cause

File: `installer/scripts/install.sh` line 312-314

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

## Fix

### Option 1: Fix sys.path (Recommended)

**Change line 312**:
```python
# BEFORE:
sys.path.insert(0, "$INSTALL_DIR/lib")

# AFTER:
sys.path.insert(0, "$INSTALL_DIR")
```

### Option 2: Change Import Statement

**Change line 314**:
```python
# Keep line 312 as-is:
sys.path.insert(0, "$INSTALL_DIR/lib")

# Change line 314:
# BEFORE:
from lib.feature_detection import detect_packages

# AFTER:
from feature_detection import detect_packages
```

### Option 3: Use os.chdir (Cleanest)

**Replace lines 311-314**:
```python
if ! python3 <<EOF
import sys
import os

# Change to install directory
os.chdir("$INSTALL_DIR")

# Import using relative path
from lib.feature_detection import detect_packages
print("Import successful")
sys.exit(0)
EOF
```

## Recommended: Option 1

**Exact Change Needed**:

File: `installer/scripts/install.sh`
Line: 312

```bash
# BEFORE:
sys.path.insert(0, "$INSTALL_DIR/lib")

# AFTER:
sys.path.insert(0, "$INSTALL_DIR")
```

This matches how Taskwright will work after TASK-FIX-86B2 is implemented.

## Testing

After fix:
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

## Implementation Time

**2 minutes** - Single line change

## Priority

**CRITICAL** - Blocks RequireKit installation validation
