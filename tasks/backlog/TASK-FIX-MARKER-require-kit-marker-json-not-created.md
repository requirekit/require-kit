---
id: TASK-FIX-MARKER
title: Fix require-kit.marker.json not created during installation
status: backlog
created: 2025-11-30T07:45:00Z
updated: 2025-11-30T07:45:00Z
priority: high
tags: [installation, bug, integration, marker-file]
complexity: 0
test_results:
  status: pending
  coverage: null
  last_run: null
---

# Task: Fix require-kit.marker.json not created during installation

## Description
The installer script (installer/scripts/install.sh) reports successful marker file creation but the file is not actually created on disk. The installation output shows:

```
✓ Marker file created at /Users/richwoollcott/.agentecflow/require-kit.marker.json
```

However, inspection of ~/.agentecflow/ shows the file does not exist. This prevents taskwright BDD mode from detecting the require-kit installation.

## Evidence

**Installation Output:**
```bash
ℹ Creating package marker...
✓ Marker file created at /Users/richwoollcott/.agentecflow/require-kit.marker.json
```

**Actual State:**
```bash
$ ls ~/.agentecflow/*.marker*
taskwright.marker.json  # ✅ exists
# require-kit.marker.json is MISSING ❌
```

**Expected File:**
- Path: ~/.agentecflow/require-kit.marker.json
- Format: JSON with metadata (package, version, installed, etc.)

## Root Cause Analysis

The create_marker_file() function at installer/scripts/install.sh:222-262 uses:

```bash
cat > "$INSTALL_DIR/$PACKAGE_NAME.marker.json" <<EOF
{JSON content}
EOF
```

Where:
- INSTALL_DIR="$HOME/.agentecflow" (line 7)
- PACKAGE_NAME="require-kit" (line 8)

Expected result: ~/.agentecflow/require-kit.marker.json

Possible causes:
1. **Heredoc issue**: The EOF marker or cat command failing silently
2. **Permission issue**: Directory not writable (but taskwright.marker.json exists, so unlikely)
3. **Variable expansion**: INSTALL_DIR or PACKAGE_NAME not expanded correctly
4. **Silent failure**: The function succeeds but writes to wrong location or is overwritten

## Acceptance Criteria
- [ ] Marker file is actually created at ~/.agentecflow/require-kit.marker.json during installation
- [ ] File contains valid JSON with expected metadata structure
- [ ] Installation verification correctly checks for marker file existence
- [ ] Error handling added if marker creation fails (don't report success if it failed)
- [ ] Test installation on clean system confirms file is created

## Test Requirements
- [ ] Unit test: verify create_marker_file() creates file at correct path
- [ ] Integration test: full installation creates marker file
- [ ] Validation test: marker file contains valid JSON
- [ ] Error test: installation fails if marker cannot be created

## Investigation Steps
1. Add debug output before/after marker creation to see what's happening
2. Check if file is created then deleted by subsequent steps
3. Verify directory permissions
4. Test heredoc syntax in isolation
5. Check for any errors being silenced by the script

## Implementation Notes
**Affected Files:**
- installer/scripts/install.sh:222-262 (create_marker_file function)
- installer/scripts/install.sh:287-290 (verify_installation function)

**Fix Approach:**
1. Add error checking after marker creation
2. Consider using printf or echo instead of cat with heredoc if needed
3. Add debugging output during development
4. Update verify_installation() to fail loudly if marker missing
5. Ensure no subsequent steps delete or overwrite the marker

## Related Issues
- Blocks taskwright BDD mode integration (requires marker for detection)
- Installation reports success but integration fails
- User confusion: installation appears successful but features don't work

## References
- Installer script: [installer/scripts/install.sh:222-262](installer/scripts/install.sh#L222-L262)
- Verification: [installer/scripts/install.sh:287-290](installer/scripts/install.sh#L287-L290)
- Feature detection: [installer/global/lib/feature_detection.py:84-88](installer/global/lib/feature_detection.py#L84-L88)

## Test Execution Log
[Automatically populated by /task-work]
