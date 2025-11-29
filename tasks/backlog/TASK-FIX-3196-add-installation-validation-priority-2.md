---
id: TASK-FIX-3196
title: Add post-installation validation for RequireKit (Priority 2)
status: backlog
created: 2025-11-29T19:40:00Z
updated: 2025-11-29T19:40:00Z
priority: high
tags: [installation, validation, quality-gates, pre-launch]
complexity: 2
parent_review: TASK-REV-DEF4
depends_on: TASK-FIX-D2C0
cross_repo_coordination: taskwright/TASK-FIX-7EA8
estimated_effort: 45 minutes
test_results:
  status: pending
  coverage: null
  last_run: null
---

# Task: Add Post-Installation Validation for RequireKit (Priority 2)

## Context

**From TASK-REV-DEF4 Review**: Priority 2 recommendation to add fail-fast validation during installation.

**Coordination**: Match Taskwright's validation approach (TASK-FIX-7EA8) for consistency.

**Current Issue**: Installation completes successfully even if Python imports are broken. Users discover issues at runtime.

---

## Objective

Add post-installation validation to RequireKit install script, **matching Taskwright's pattern**.

---

## Implementation Steps

### Step 1: Add Post-Installation Validation

**File**: `installer/scripts/install.sh`

**Location**: End of script (before final success message)

**Add This Code** (matching Taskwright's pattern):
```bash
echo ""
echo "=========================================="
echo "Validating RequireKit installation..."
echo "=========================================="

# Test Python imports work
python3 << 'EOF'
import sys
import os

# Change to installed lib directory
lib_dir = os.path.expanduser("~/.agentecflow/lib")
if os.path.exists(lib_dir):
    os.chdir(os.path.dirname(lib_dir))

    # Test feature detection import
    try:
        from lib.feature_detection import detect_packages
        print("✅ Python imports validated successfully")
    except ImportError as e:
        print(f"❌ ERROR: Python import validation failed")
        print(f"   {e}")
        print("")
        print("   This is a bug in the installation script.")
        print("   Please report this issue with the error message above.")
        sys.exit(1)
else:
    print("✅ No Python libraries to validate (marker-only install)")
EOF

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Installation validation failed"
    echo "   Installation incomplete - please report this issue"
    exit 1
fi

echo "✅ RequireKit installation validated successfully"
echo ""
```

**Why This Helps**:
- ✅ Catches import errors during installation
- ✅ Provides clear error messages
- ✅ Fails fast if something wrong
- ✅ Consistent with Taskwright validation

---

### Step 2: Update Marker File Schema (Optional)

**File**: `installer/scripts/install.sh`

**Match Taskwright's Schema**:

**BEFORE**:
```json
{
  "package": "require-kit",
  "version": "$VERSION",
  "repo_path": "$REPO_DIR",
  "install_location": "~/.agentecflow"
}
```

**AFTER**:
```json
{
  "package": "require-kit",
  "version": "$VERSION",
  "install_location": "~/.agentecflow",
  "install_date": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "install_method": "$INSTALL_METHOD"
}
```

**Changes** (same as Taskwright):
- ❌ **Remove**: `repo_path` (confusing)
- ✅ **Add**: `install_method` (curl vs git-clone)
- ✅ **Add**: `install_date` (diagnostics)

---

## Acceptance Criteria

### Must Have:
- [ ] Post-installation validation added
- [ ] Validation tests feature_detection import
- [ ] Clear error messages if validation fails
- [ ] Installation exits with error if validation fails
- [ ] Pattern matches Taskwright validation

### Should Have (if time permits):
- [ ] Marker file schema updated to match Taskwright

### Testing:
- [ ] Fresh curl installation passes validation
- [ ] Validation catches broken imports
- [ ] Error messages are helpful
- [ ] No false positives

---

## Testing Plan

### Test 1: Validation Passes for Good Install

```bash
# Fresh install
rm -rf ~/.agentecflow/*.marker
rm -rf ~/.agentecflow/lib
curl -sSL .../install.sh | bash

# Expected: Validation passes
# Output: "✅ RequireKit installation validated successfully"
```

### Test 2: Taskwright Can Detect RequireKit

```bash
# After RequireKit install with validation
cd ~/Projects/appmilla_github/taskwright

# Test detection
python3 << 'EOF'
from lib.feature_detection import detect_packages
result = detect_packages()
print(f"RequireKit detected: {result.get('require-kit', False)}")
EOF

# Expected: ✅ RequireKit detected: True
```

---

## Risk Assessment

**Regression Risk**: 🟢 VERY LOW

**Why Low Risk**:
- Validation is additive (doesn't change existing logic)
- RequireKit has simpler install than Taskwright
- Pattern proven to work in Taskwright

---

## Implementation Effort

- **Step 1**: Add validation - 30 minutes
- **Step 2**: Update marker file - 10 minutes
- **Testing**: Validate on clean environment - 15 minutes

**Total**: 45 minutes - 1 hour

---

## Success Metrics

After implementation:
- [ ] Installation validation catches broken imports
- [ ] Clear error messages guide users
- [ ] Fail-fast principle enforced
- [ ] Consistent with Taskwright

---

## Related Tasks

- **Depends On**: TASK-FIX-D2C0 (implement relative imports first)
- **Parent Review**: taskwright/TASK-REV-DEF4 (architectural review)
- **Taskwright Equivalent**: taskwright/TASK-FIX-7EA8 (same validation)
- **Coordination**: Match Taskwright's validation pattern

---

## Notes

**Simpler Than Taskwright**:
- RequireKit has fewer Python dependencies
- Main validation is `feature_detection.py` import
- Can use simpler validation logic

**Order of Operations**:
1. First: Fix imports (TASK-FIX-D2C0)
2. Second: Add validation (this task)
3. Third: Test integration with Taskwright
4. Ready for launch ✅

**Optional**: Can be deferred if time-constrained, but recommended for quality assurance.
