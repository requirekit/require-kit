---
id: TASK-FIX-C2D8
title: Fix Python import paths for curl installation compatibility
status: backlog
created: 2025-11-29T18:20:00Z
updated: 2025-11-29T18:20:00Z
priority: high
tags: [bug, installation, python, imports]
complexity: 5
test_results:
  status: pending
  coverage: null
  last_run: null
---

# Task: Fix Python import paths for curl installation compatibility

## Problem Description

When require-kit is installed via curl (not from a local git clone), Python imports may fail because:

1. **Wrong import paths**: Commands may reference repo-based paths that don't exist after installation
2. **Missing Python path setup**: The `repo_path` field in the marker file exists but isn't used
3. **Inconsistent with taskwright**: Should use same pattern as taskwright for consistency

### Current Status
- `feature_detection.py` is copied to `~/.agentecflow/lib/` during installation
- Commands need to import it using the correct path
- Should match taskwright's solution for consistency

## Root Cause Analysis

The install script copies Python files:
- **From**: `$SCRIPT_DIR/global/lib/feature_detection.py`
- **To**: `~/.agentecflow/lib/feature_detection.py`

Any imports must reference the installed location, not the repository location.

## Acceptance Criteria

- [ ] All Python imports in require-kit commands use paths compatible with curl installation
- [ ] Import pattern matches taskwright's solution for consistency
- [ ] Installation script validates all referenced Python modules are copied
- [ ] Test curl installation successfully runs commands with Python imports
- [ ] Documentation shows correct import paths

## Proposed Solutions

### Option 1: Use Installed Location Imports (Recommended)
```python
# BEFORE (may be broken):
from installer.global.lib.feature_detection import detect_packages

# AFTER (works everywhere):
from lib.feature_detection import detect_packages
```

**Pros**: Simple, consistent with taskwright, works immediately
**Cons**: Requires updating command documentation

### Option 2: Match Taskwright's Solution
Wait for taskwright to implement their fix (TASK-FIX-A7B3), then apply the same pattern here.

**Pros**: Ensures consistency across both packages
**Cons**: Blocks on taskwright completion

## Implementation Plan

1. **Wait for taskwright solution** (TASK-FIX-A7B3 in taskwright repo)
2. **Audit require-kit commands** for Python import statements
3. **Apply same pattern** as taskwright uses
4. **Update install script** if needed to match taskwright
5. **Test curl installation** end-to-end

## Files Affected

### Command Files
- Check all `.md` files in `global/commands/` for Python import statements
- Update to use installed path pattern

### Library Files
- `global/lib/feature_detection.py` - Shared with taskwright
- May need updates to import other modules

### Install Script
- `installer/scripts/install.sh` - Already copies to `lib/` directory
- May need additional validation steps

## Dependencies

- **Blocks on**: taskwright TASK-FIX-A7B3 (for solution pattern)
- **Related**: Both packages need consistent approach

## Test Plan

1. **Fresh curl install test**:
   ```bash
   # Clean environment
   rm -rf ~/.agentecflow/*.marker*
   rm -rf ~/.agentecflow/commands/require-kit
   rm -rf ~/.agentecflow/agents/require-kit

   # Install via curl
   curl -sSL https://raw.githubusercontent.com/requirekit/require-kit/main/installer/scripts/install.sh | bash

   # Test commands that use Python
   /gather-requirements "Test"
   ```

2. **Verify integration with taskwright** still works
3. **Check feature detection** works correctly

## Notes

- Less urgent than taskwright's issue since require-kit has fewer Python dependencies
- Should maintain consistency with taskwright's solution
- `feature_detection.py` is the main Python file affected
- Consider adding validation to `requirekit-doctor` command (if one exists)

## Related Issues

- Taskwright TASK-FIX-A7B3 (same issue)
- Marker file format updates (COMPLETED)
- Integration detection fix (COMPLETED)
