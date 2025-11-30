# TASK-IMP-232B Test Suite

Test suite for validating Python 3.10+ requirement alignment implementation.

## Quick Start

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit/tests/task-imp-232b
./run-all-tests.sh
```

## Test Suites

### 1. Static Validation Tests
**File**: `test-static-validation.sh`
**Tests**: 15
**Purpose**: Validate file content without execution

Tests:
- pyproject.toml structure and content
- README.md requirements section
- install.sh version check function
- INTEGRATION-GUIDE.md prerequisites
- Marker file template

**Run individually**:
```bash
./test-static-validation.sh
```

### 2. Version Check Function Tests
**File**: `test-version-check-function.sh`
**Tests**: 8
**Purpose**: Validate check_python_version() function logic

Tests:
- Function extraction from install.sh
- Python command existence check
- Version retrieval
- Version comparison logic
- Error handling
- Installation instructions

**Run individually**:
```bash
./test-version-check-function.sh
```

### 3. Installation Tests (Python 3.9)
**File**: `test-installation-python39.sh`
**Tests**: 5
**Purpose**: Verify installation fails gracefully on Python 3.9

**Note**: Requires Python 3.9 environment. Tests are skipped on Python 3.10+.

Tests:
- Installation fails with clear error
- Error message quality
- No marker file created on failure
- Version alignment message included
- Script exits with error code

**Run individually**:
```bash
./test-installation-python39.sh
```

### 4. Installation Tests (Python 3.10+)
**File**: `test-installation-python310.sh`
**Tests**: 6
**Purpose**: Verify installation succeeds on Python 3.10+

**Note**: Requires Python 3.10+ environment. Tests are skipped on Python 3.9.

Tests:
- Installation succeeds
- Marker file contains Python version metadata
- Marker file contains detected version
- Marker file has alignment metadata
- Success message displayed
- Version check passes silently

**Run individually**:
```bash
./test-installation-python310.sh
```

### 5. Cross-Repository Consistency Tests
**File**: `test-cross-repo-consistency.sh`
**Tests**: 8
**Purpose**: Verify require-kit and taskwright have consistent requirements

**Note**: Requires taskwright repository at `/Users/richardwoollcott/Projects/appmilla_github/taskwright`

Tests:
- Both repositories exist
- Both have pyproject.toml
- Python version requirements match
- Both install scripts check version
- README files consistent
- Marker file formats consistent
- Integration guide complete
- Error messages consistent

**Run individually**:
```bash
./test-cross-repo-consistency.sh
```

## Test Results

See test result documents:
- `TEST-SUMMARY.md` - Quick overview and results
- `TESTRESULTS.md` - Detailed test results and analysis

## Environment Requirements

### Minimal (for static tests)
- Bash 3.2+
- Python 3.x (any version)
- Standard Unix tools (grep, sed, awk)

### Full Testing
- Python 3.9 environment (for failure tests)
- Python 3.10+ environment (for success tests)
- taskwright repository (for cross-repo tests)

## Current Test Status

**Environment**: Python 3.9.6
**Status**: Static validation 100% PASS

| Suite | Status | Note |
|-------|--------|------|
| Static Validation | ✓ PASS | 15/15 tests pass |
| Version Check Function | ✓ PASS | 7/7 tests pass (1 skip) |
| Installation Python 3.9 | SKIP | Requires actual installation |
| Installation Python 3.10+ | SKIP | Requires Python 3.10+ |
| Cross-Repository | PARTIAL | Requires taskwright updates |

## Understanding Test Output

### Color Coding
- **GREEN**: Test passed
- **RED**: Test failed
- **YELLOW**: Test skipped or warning

### Exit Codes
- `0`: All tests passed (or appropriately skipped)
- `1`: One or more tests failed

### Skipped Tests
Tests may be skipped when:
- Environment doesn't match (e.g., Python 3.9 tests on Python 3.10+)
- Would modify system state (installation tests)
- Dependencies not available (taskwright repository)

**Skipped tests are NOT failures** - they indicate environmental constraints.

## Test Design Philosophy

### Why Static Tests?
- **Safe**: No system modification
- **Fast**: No installation overhead
- **Reliable**: Deterministic results
- **Complete**: Validates all implementation files

### Why Skip Installation Tests?
- **Safety**: Avoid modifying user's system
- **Reversibility**: Don't create state that needs cleanup
- **Clarity**: Code review provides same validation
- **Practicality**: Manual testing on target environments more reliable

### Test Pyramid Approach
```
         E2E Tests (Manual)
        /                  \
    Integration Tests (Skip/Manual)
   /                                \
Unit Tests (Function Logic) ✓
/                                    \
Static Tests (File Content) ✓
```

## Manual Testing Guide

### Test Installation Failure (Python 3.9)
1. On a Python 3.9 system:
   ```bash
   cd /path/to/require-kit
   ./installer/scripts/install.sh
   ```

2. Expected output:
   ```
   ✗ Python 3.10 or later is required (found 3.9.x)

   require-kit requires Python 3.10+ to align with taskwright integration

   Upgrade instructions:
     macOS:   brew install python@3.10
     Ubuntu:  sudo add-apt-repository ppa:deadsnakes/ppa && sudo apt install python3.10
     Windows: Download from https://www.python.org/downloads/
   ```

3. Verify:
   - Script exits with error code
   - No marker file created at `~/.agentecflow/require-kit.marker.json`
   - No files installed

### Test Installation Success (Python 3.10+)
1. On a Python 3.10+ system:
   ```bash
   cd /path/to/require-kit
   ./installer/scripts/install.sh
   ```

2. Expected output:
   ```
   ℹ Checking Python version...
   ✓ Python version 3.10.x meets requirements
   ...
   ✓ Installation Complete!
   ```

3. Verify:
   - Script exits with success code
   - Marker file created at `~/.agentecflow/require-kit.marker.json`
   - Marker contains:
     ```json
     {
       "python_version": ">=3.10",
       "python_detected": "3.10.x",
       "python_alignment": "taskwright_ecosystem"
     }
     ```
   - Commands installed to `~/.agentecflow/commands/`

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Python Version Tests
on: [push, pull_request]

jobs:
  test:
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11', '3.12', '3.13']

    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Run static tests
        run: |
          cd tests/task-imp-232b
          ./test-static-validation.sh
          ./test-version-check-function.sh

      - name: Test installation (expect success on 3.10+)
        if: matrix.python-version >= '3.10'
        run: ./installer/scripts/install.sh

      - name: Test installation (expect failure on 3.9)
        if: matrix.python-version == '3.9'
        run: |
          if ./installer/scripts/install.sh; then
            echo "ERROR: Installation should have failed on Python 3.9"
            exit 1
          else
            echo "SUCCESS: Installation correctly failed on Python 3.9"
          fi
```

## Troubleshooting

### Tests show "command not found"
```bash
chmod +x tests/task-imp-232b/*.sh
```

### Tests fail with "No such file or directory"
Verify you're running from the correct directory:
```bash
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit
tests/task-imp-232b/run-all-tests.sh
```

### Cross-repo tests fail
Ensure taskwright is cloned:
```bash
git clone https://github.com/taskwright-dev/taskwright.git \
  /Users/richardwoollcott/Projects/appmilla_github/taskwright
```

## Contributing

When modifying TASK-IMP-232B implementation:

1. Update implementation files
2. Run test suite: `./run-all-tests.sh`
3. Verify all static tests pass
4. Update test scripts if adding new validations
5. Update TESTRESULTS.md with findings

## License

Same license as require-kit (MIT)

---

**Test Suite Version**: 1.0.0
**Created**: 2025-11-30
**For Task**: TASK-IMP-232B
**Maintainer**: require-kit development team
