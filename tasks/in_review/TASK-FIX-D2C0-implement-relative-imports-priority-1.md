---
id: TASK-FIX-D2C0
title: Implement relative imports for Python path fix (Priority 1 - Launch Blocker)
status: in_review
created: 2025-11-29T19:40:00Z
updated: 2025-11-29T23:50:00Z
priority: critical
tags: [bug, installation, python-imports, launch-blocker, pre-launch]
complexity: 4
parent_review: TASK-REV-DEF4
cross_repo_dependency: taskwright/TASK-FIX-86B2
estimated_effort: 1-2 hours
test_results:
  status: passed
  coverage: 100%
  last_run: 2025-11-29T23:50:00Z
  total_tests: 5
  passed_tests: 5
  failed_tests: 0
  compilation_errors: 0
previous_state: backlog
state_transition_reason: "All quality gates passed"
auto_approved: true
approved_by: timeout
approved_at: 2025-11-29T23:50:00Z
review_mode: quick_optional
architectural_review_score: 92
code_review_score: 95
---

# Task: Implement Relative Imports for Python Path Fix (Priority 1)

## Context

**CRITICAL LAUNCH BLOCKER**: This task implements the fix for curl installation failures identified in Taskwright's comprehensive architectural review (TASK-REV-DEF4).

**Same Issue as Taskwright**: Python imports may use repository-based paths that don't exist in installed location.

**Coordination**: This fix **must match Taskwright's approach** (TASK-FIX-86B2) for consistency across both packages.

**Recommended Solution**: Option 1 - Relative Imports

---

## Objective

Convert all Python imports from absolute repository paths to relative installed paths, **matching Taskwright's pattern**.

**Change Pattern** (same as Taskwright):
```python
# BEFORE (potentially broken):
from installer.global.lib.feature_detection import detect_packages
# or:
from global.lib.feature_detection import detect_packages

# AFTER (works):
from lib.feature_detection import detect_packages
```

---

## Implementation Steps

### Step 1: Find All Python Imports

**Command**:
```bash
cd ~/Projects/appmilla_github/require-kit

# Check for problematic imports
grep -rn "from installer\.global\.lib" global/
grep -rn "from global\.lib" global/
grep -rn "from installer\.global\.lib" installer/
```

**Expected Files**:
- Command markdown files (`.md`)
- Python scripts (`.py`)
- Library modules (`global/lib/*.py`)

---

### Step 2: Update feature_detection.py (Main Library)

**File**: `global/lib/feature_detection.py`

**Check for**: Any imports of other lib modules

**Example Fix**:
```python
# BEFORE:
from global.lib.other_module import something

# AFTER:
from lib.other_module import something
```

**Note**: If `feature_detection.py` doesn't import other lib modules, no changes needed

---

### Step 3: Update Command Files

**Check All Commands**: `global/commands/*.md`

**Look for**: Embedded Python code with imports

**Example**: If `gather-requirements.md` has Python code

**BEFORE**:
```python
from global.lib.feature_detection import detect_packages
```

**AFTER**:
```python
from lib.feature_detection import detect_packages
```

---

### Step 4: Update Python Scripts

**Check**: `global/commands/*.py` (if any)

**Apply Same Pattern**: Use `from lib.X import Y`

**Remove**: Any repository path resolution code (like Taskwright's cleanup)

---

### Step 5: Verify Install Script

**File**: `installer/scripts/install.sh`

**Check** that it copies lib files correctly:
```bash
# Should have something like:
if [ -d "$SCRIPT_DIR/global/lib" ]; then
    mkdir -p "$INSTALL_DIR/lib"
    cp -r "$SCRIPT_DIR/global/lib"/* "$INSTALL_DIR/lib/"
fi
```

**Expected**: ✅ Already copies lib files

**If missing**: Add copy logic similar to Taskwright

---

### Step 6: Test Curl Installation

**Fresh Environment Test**:
```bash
# Clean environment
rm -rf ~/.agentecflow/*.marker
rm -rf ~/.agentecflow/commands/require-kit
rm -rf ~/.agentecflow/agents/require-kit
rm -rf ~/Downloads/require-kit  # Or wherever curl downloads

# Install via curl
curl -sSL https://raw.githubusercontent.com/requirekit/require-kit/main/installer/scripts/install.sh | bash

# Test Python-based command works (if any)
# Or verify feature detection works from Taskwright:
cd ~/Projects/appmilla_github/taskwright
python3 << 'EOF'
from lib.feature_detection import detect_packages
result = detect_packages()
print(f"RequireKit detected: {result.get('require-kit', False)}")
EOF

# Expected: ✅ No import errors, RequireKit detected correctly
```

---

### Step 7: Test Integration with Taskwright

**Test**: Ensure Taskwright can still detect RequireKit

```bash
# After RequireKit curl install
cd ~/Projects/appmilla_github/taskwright

# Test BDD mode detection
/task-create "Test BDD detection" task_type:implementation

# Try BDD mode (should detect RequireKit)
/task-work TASK-XXX --mode=bdd

# Expected: Either works with RequireKit, or shows proper error if RequireKit not fully installed
```

---

## Acceptance Criteria

- [ ] All `from installer.global.lib.X` or `from global.lib.X` imports updated to `from lib.X`
- [ ] No repository path resolution code remains
- [ ] Fresh curl installation succeeds (clean environment test)
- [ ] Git clone installation still works (no regression)
- [ ] Taskwright integration works (can detect RequireKit)
- [ ] No Python import errors in any context
- [ ] Pattern matches Taskwright implementation (consistency)

---

## Files to Check and Potentially Update

### Confirmed:
1. **global/lib/feature_detection.py** (check for imports of other lib modules)

### To Check:
2. **global/commands/*.md** (any with embedded Python)
3. **global/commands/*.py** (Python scripts)
4. **global/lib/*.py** (other library modules)
5. **installer/scripts/install.sh** (verify lib files copied)

---

## Testing Checklist

### Pre-Deployment:
- [ ] Find all import statements: `grep -r "from .*global\.lib"`
- [ ] Verify all updated to `from lib.X` pattern
- [ ] No repository path resolution code remains
- [ ] Install script copies lib files correctly

### Post-Deployment:
- [ ] Curl installation on clean environment ✅
- [ ] Git clone installation (regression check) ✅
- [ ] Taskwright can detect RequireKit ✅
- [ ] Feature detection works correctly ✅
- [ ] No import errors ✅

---

## Coordination with Taskwright

**IMPORTANT**: This fix must use the **exact same pattern** as Taskwright for consistency:

1. **Import Pattern**: `from lib.MODULE_NAME import FUNCTION`
2. **No Path Manipulation**: Remove all sys.path or repo resolution code
3. **Installed Location**: `~/.agentecflow/lib/` (or similar)
4. **Testing**: Both curl and git clone must work

**Check Taskwright's Implementation**:
```bash
# After Taskwright TASK-FIX-86B2 is complete:
cd ~/Projects/appmilla_github/taskwright
grep -r "from lib\." installer/global/commands/

# Copy the exact pattern used
```

---

## Risk Assessment

**Regression Risk**: 🟢 VERY LOW

**Why Low Risk**:
- RequireKit has fewer Python dependencies than Taskwright
- Main file is `feature_detection.py`
- Install script should already copy lib files
- Pattern proven to work in Taskwright

**If This Breaks**:
- Symptom: Import errors when Taskwright tries to detect RequireKit
- Root cause: File not copied to lib directory
- Fix: Update install script to copy missing file

---

## Related Tasks

- **Parent Review**: taskwright/TASK-REV-DEF4 (comprehensive architectural review)
- **Original Fix**: TASK-FIX-C2D8 (original RequireKit Python import fix task)
- **Taskwright Equivalent**: taskwright/TASK-FIX-86B2 (same fix for Taskwright)
- **Companion Fix**: TASK-FIX-3196 (Priority 2 - RequireKit validation)
- **Cross-Repo Dependency**: Wait for Taskwright fix first, then match pattern

---

## Implementation Notes

### Why Relative Imports Work

Similar to Taskwright, the install script copies files:
```
global/lib/feature_detection.py  →  ~/.agentecflow/lib/feature_detection.py
```

When Python code needs to import:
```python
from lib.feature_detection import detect_packages
```

Python finds: `~/.agentecflow/lib/feature_detection.py` ✅

This works **regardless** of where the repository is located.

### Architecture Benefits

- ✅ **Consistency with Taskwright**: Same pattern across both packages
- ✅ **True Standalone Installation**: No repository dependency
- ✅ **Platform Agnostic**: Works on macOS, Linux, Windows WSL
- ✅ **Robust**: User can move/delete repository safely
- ✅ **Simple**: Standard Python packaging pattern

---

## Success Metrics

After implementation:
- [ ] Zero import errors for RequireKit
- [ ] Taskwright can detect RequireKit via feature detection
- [ ] Pattern matches Taskwright (consistency verified)
- [ ] BDD mode integration works
- [ ] Ready for public launch ✅

---

## Estimated Effort

- **Step 1**: Find imports - 15 minutes
- **Step 2-4**: Update imports - 30 minutes
- **Step 5**: Verify install script - 15 minutes
- **Step 6-7**: Testing (curl + integration) - 45 minutes

**Total**: 1-2 hours

**Note**: Less complex than Taskwright because fewer Python dependencies

---

## Next Steps After Completion

1. Mark this task complete
2. Test on fresh environment
3. Verify Taskwright integration still works
4. Update TASK-FIX-C2D8 status (original issue)
5. Proceed to TASK-FIX-3196 (Priority 2 - validation)
6. Coordinate with Taskwright for launch readiness

---

**CRITICAL**: This should be completed **after** Taskwright's TASK-FIX-86B2 so we can match the exact pattern used for consistency.
