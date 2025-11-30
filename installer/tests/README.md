# Regression Tests for require-kit Installation

## Overview

This directory contains regression tests to prevent known installation bugs from recurring.

## Tests

### test-validation-function-name.sh

**Purpose**: Prevents function name mismatch between import statement and actual function definition.

**Bug Prevented**: The November 29, 2025 incident where `install.sh` imported `detect_packages` but `feature_detection.py` defined `is_require_kit_installed`, causing fatal installation failure.

**How it Works**:
1. Extracts the imported function name from `install.sh`
2. Verifies that function exists in `feature_detection.py`
3. Fails if there's a mismatch with clear diagnostic output

**Usage**:
```bash
# Run from project root
bash installer/tests/test-validation-function-name.sh

# Or with custom paths
INSTALL_SCRIPT=/path/to/install.sh \
FEATURE_DETECTION=/path/to/feature_detection.py \
bash installer/tests/test-validation-function-name.sh
```

**When to Run**:
- Before committing changes to `install.sh` or `feature_detection.py`
- As part of CI/CD pipeline
- After merging branches that modify installation code
- When troubleshooting installation failures

## Architecture Decision Context

This test suite implements **Phase 1** of TASK-IMP-UOU4:
- Non-fatal validation (warnings instead of errors)
- Regression prevention (automated test)
- Minimal implementation (30 minutes, focused scope)

Phase 2 (comprehensive validation suite) was deferred pending evidence of additional failure modes.

## Integration with CI/CD

To add to CI pipeline:

```yaml
# Example GitHub Actions
- name: Run installation regression tests
  run: |
    bash installer/tests/test-validation-function-name.sh
```

## Future Tests

Additional tests should be added when:
1. New installation failure modes are discovered
2. Complex installation logic is added
3. Integration points with other packages change

Follow the same pattern:
- Defensive programming (validate inputs)
- Clear diagnostic output
- Configurable paths
- Single responsibility
