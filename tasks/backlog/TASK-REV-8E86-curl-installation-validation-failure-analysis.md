---
id: TASK-REV-8E86
title: Review and Fix cURL Installation Validation Failure
status: backlog
created: 2025-11-29T22:45:00Z
updated: 2025-11-29T22:45:00Z
priority: high
tags: [installation, validation, bug-fix, reliability]
complexity: 6
task_type: review
decision_required: true
---

# Task: Review and Fix cURL Installation Validation Failure

## Description

Analysis of a production incident where the requirekit cURL installation (`curl -sSL https://raw.githubusercontent.com/requirekit/require-kit/main/installer/scripts/install.sh | bash`) failed silently due to a validation bug, leaving users without functioning commands despite files being installed.

## Incident Timeline

| Time | Event | Status |
|------|-------|--------|
| 21:30 | `ac8c9b9` - Added `validate_installation()` with bug | ❌ Broken |
| 21:30 | `e79f537` - Fixed sys.path issue | ⚠️ Still broken |
| 22:08 | `942e549` - Fixed function name bug | ✅ Working |
| **22:10** | **User ran cURL installation** | **❌ Got buggy version** |
| 22:25 | Taskwright installed successfully | ✅ Working |
| 22:33 | Manual install.sh run (successful) | ✅ Working |

## Root Cause

### The Bug (Version at 22:08)

**File**: `installer/scripts/install.sh` (line ~314)

```python
# Validation attempted to import wrong function name
python3 <<EOF
import sys
sys.path.insert(0, "$INSTALL_DIR")
try:
    from lib.feature_detection import detect_packages  # ❌ WRONG FUNCTION
    print("Import successful")
    sys.exit(0)
except ImportError as e:
    print(f"Import failed: {e}", file=sys.stderr)
    sys.exit(1)  # ← Caused script to exit due to 'set -e'
EOF
```

**Actual Function**: `lib/feature_detection.py` contains `is_require_kit_installed()`, NOT `detect_packages`

### Impact Chain

1. ✅ Script successfully installed all files:
   - Cloned repository to `~/Projects/require-kit`
   - Created `~/.agentecflow/commands/require-kit/` directory
   - Installed 12 command files
   - Installed 7 agent files
   - Installed 14 Python library files
   - Created marker file `~/.agentecflow/require-kit.marker.json`

2. ❌ Validation failed:
   - Python import threw `ImportError: cannot import name 'detect_packages'`
   - Python exited with code 1
   - Bash script detected failure (`if ! python3 <<EOF`)
   - Called `print_error` which executes `exit 1`
   - Script terminated due to `set -e` at line 5

3. ❌ User never saw:
   - `check_integration_opportunities()` - Would show taskwright detection
   - `print_completion_message()` - Would show available commands
   - Clear indication of installation success/failure

## Technical Analysis

### Script Flow Breakdown

```bash
main() {
    print_header                   # ✅ Executed
    ensure_repository_files        # ✅ Cloned repo to ~/Projects/require-kit
    check_prerequisites            # ✅ Passed
    create_directory_structure     # ✅ Created dirs
    install_commands               # ✅ Installed 12 commands
    install_agents                 # ✅ Installed 7 agents
    install_lib                    # ✅ Installed Python libs
    create_marker_file             # ✅ Created marker
    track_installation             # ✅ Tracked installation
    verify_installation            # ✅ Verified files exist
    validate_installation          # ❌ FAILED HERE - exit 1
    # Never reached:
    check_integration_opportunities
    print_completion_message
}
```

### The Fix (Commit 942e549)

```diff
- from lib.feature_detection import detect_packages
+ from lib.feature_detection import is_require_kit_installed
```

### Why This Was Silent

1. **Installation appeared complete** - All files were on disk
2. **No clear error message** - User just saw validation failure
3. **Commands weren't available** - Despite files existing
4. **Marker file existed** - But validation failure made it seem like total failure

## Evidence

### Git History Analysis

```bash
# Validation evolution
ac8c9b9 feat: add post-installation validation for RequireKit
e79f537 Complete TASK-FIX-EBD0: Fix RequireKit validation import error
942e549 fix for detection  # ← Fixed function name

# User cloned 2 minutes after fix was committed
# Commit: 22:08
# Clone:  22:10
# Got the HEAD version which had the bug
```

### Verification Test

Current cURL installation **works perfectly**:
```bash
$ curl -sSL https://raw.githubusercontent.com/requirekit/require-kit/main/installer/scripts/install.sh | bash

✓ Commands installed (12 commands)
✓ Agents installed (7 agents)
✓ Library files installed (14 Python modules)
✓ Marker file created
✓ Installation verified
✓ Python module validation passed  # ← Now works!
✓ taskwright detected - full integration available

Installation Complete!
```

## Acceptance Criteria

### Must Fix
- [ ] Validation should be non-fatal to prevent silent installation failures
- [ ] Clear differentiation between "installation failed" vs "validation failed"
- [ ] User should see completion message even if validation fails
- [ ] Validation errors should include troubleshooting steps
- [ ] Add function name validation tests to prevent future import errors

### Should Improve
- [ ] Add smoke test that validates the validation function itself
- [ ] Consider moving validation earlier in the process
- [ ] Add exit code documentation (0=success, 1=install failed, 2=validation warning)
- [ ] Improve error messages with actionable next steps

### Nice to Have
- [ ] Add --skip-validation flag for advanced users
- [ ] Log validation details to a file for debugging
- [ ] Add retry logic for validation failures
- [ ] Create automated test suite for installation script

## Proposed Solution

### Option 1: Non-Fatal Validation (Recommended)

```bash
validate_installation() {
    print_info "Validating installation..."

    if ! command -v python3 &> /dev/null; then
        print_warning "Python 3 not found - skipping Python validation"
        return 0
    fi

    if ! python3 <<EOF
# ... validation code ...
EOF
    then
        print_warning "Python module validation failed"
        echo ""
        echo "The feature_detection module could not be imported."
        echo "This may indicate an installation issue, but basic functionality should work."
        echo ""
        echo "Troubleshooting steps:"
        echo "  1. Check that $INSTALL_DIR/lib/feature_detection.py exists"
        echo "  2. Verify Python 3 is installed: python3 --version"
        echo "  3. Try reinstalling: bash install.sh"
        echo ""
        echo "You can still try using the commands - they may work despite this warning."
        echo ""
        return 0  # ← Non-fatal, continue with installation
    fi

    print_success "Python module validation passed"
}
```

### Option 2: Separate Validation Script

Move validation to a separate post-install check script:
```bash
# install.sh - No validation, just installation
main() {
    # ... install everything ...
    print_completion_message

    # Suggest running validation separately
    echo ""
    echo "To verify installation:"
    echo "  bash installer/scripts/validate.sh"
}

# validate.sh - Separate validation that can fail safely
# Users can run manually or skip if they want
```

### Option 3: Exit Code Strategy

Use different exit codes for different failure types:
```bash
# 0 - Complete success
# 1 - Installation failed (files not copied)
# 2 - Installation succeeded, validation failed (warning)
# 3 - Installation succeeded, validation skipped

validate_installation() {
    # ... validation logic ...
    if validation_failed; then
        print_warning "Validation failed - see details above"
        exit 2  # ← Different exit code
    fi
}
```

## Decision Required

**Choose one approach:**

1. **Option 1** (Non-Fatal Validation) - Recommended for better UX
   - ✅ Users always see completion message
   - ✅ Commands are available even if validation fails
   - ✅ Clear warning messages with troubleshooting
   - ⚠️ Might hide real installation issues

2. **Option 2** (Separate Validation) - More explicit
   - ✅ Clear separation of concerns
   - ✅ Users can skip validation if needed
   - ✅ Easier to debug validation issues
   - ⚠️ Extra step for users

3. **Option 3** (Exit Code Strategy) - Most technically correct
   - ✅ Programmatically detectable states
   - ✅ Scripts can handle different failure modes
   - ✅ Standard practice for installers
   - ⚠️ More complex error handling

## Test Requirements

### Unit Tests
```bash
# Test 1: Validation function name matches actual code
test_validation_import() {
    # Extract function name from install.sh
    grep "from lib.feature_detection import" install.sh

    # Verify function exists in feature_detection.py
    grep "^def.*install" lib/feature_detection.py

    # Assert they match
}

# Test 2: Validation failure doesn't block installation
test_non_fatal_validation() {
    # Mock validation failure
    # Verify completion message still shows
    # Verify marker file exists
}

# Test 3: Installation with broken Python
test_missing_python() {
    # Temporarily hide Python
    # Verify installation completes
    # Verify warning is shown
}
```

### Integration Tests
```bash
# Test 4: Full cURL installation
test_curl_installation() {
    curl -sSL https://raw.githubusercontent.com/requirekit/require-kit/main/installer/scripts/install.sh | bash

    # Verify marker file exists
    # Verify commands available
    # Verify agents installed
}

# Test 5: Installation on clean system
test_clean_install() {
    rm -rf ~/.agentecflow/require-kit*
    bash install.sh

    # Verify all files present
    # Verify validation passes
}
```

### Smoke Tests
```bash
# Test 6: Validation function works
test_validation_smoke() {
    cd ~/.agentecflow
    python3 -c "from lib.feature_detection import is_require_kit_installed; print(is_require_kit_installed())"

    # Should print True or False, not error
}
```

## Implementation Notes

### Files to Modify
- `installer/scripts/install.sh` - Main installation script
- `lib/feature_detection.py` - Verify function names
- `tests/test_installation.sh` - Add test coverage

### Backward Compatibility
- ✅ Existing installations unaffected
- ✅ Old validation behavior removed
- ✅ New validation is backward compatible

### Performance Impact
- No performance impact
- Validation is optional/non-blocking
- Same installation time

## Risks and Mitigations

### Risk 1: Hiding Real Issues
**Mitigation**: Clear warning messages, suggest verification steps

### Risk 2: Users Skip Validation
**Mitigation**: Make validation default but non-fatal, log results

### Risk 3: Breaking Existing Scripts
**Mitigation**: Maintain same exit codes for success (0) and hard failure (1)

## Success Metrics

- ✅ 100% of cURL installations complete successfully
- ✅ Zero silent failures (all failures show clear messages)
- ✅ Validation errors are actionable
- ✅ Installation time unchanged
- ✅ Test coverage for validation logic

## Related Tasks

- TASK-FIX-EBD0: Fix RequireKit validation import error (completed)
- TASK-FIX-3264: Fix RequireKit validation import function error (completed)
- TASK-FIX-3196: Add installation validation (completed)

## References

- Commit `942e549`: fix for detection
- Commit `e79f537`: Complete TASK-FIX-EBD0
- Commit `ac8c9b9`: feat: add post-installation validation
- Production incident: Nov 29, 2025 22:10
- Analysis document: `docs/requirekit-curl-installation-diagnosis.md` (test-api-service repo)

---

## Next Steps

1. **Review this analysis** - Confirm root cause and proposed solutions
2. **Make decision** - Choose Option 1, 2, or 3
3. **Implement fix** - Modify `installer/scripts/install.sh`
4. **Add tests** - Ensure validation errors are caught
5. **Verify fix** - Test cURL installation on clean system
6. **Document** - Update installation docs with troubleshooting

**Recommended**: Start with **Option 1 (Non-Fatal Validation)** as it provides the best user experience while still catching validation issues.
