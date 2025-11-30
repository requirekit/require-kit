#!/bin/bash
# TASK-IMP-232B - Master Test Runner
# Executes all test suites for Python 3.10+ requirement alignment

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

TEST_DIR="/Users/richardwoollcott/Projects/appmilla_github/require-kit/tests/task-imp-232b"

print_header() {
    echo ""
    echo "========================================================"
    echo "TASK-IMP-232B: Python 3.10+ Requirement Alignment Tests"
    echo "========================================================"
    echo ""
    echo "Testing implementation of:"
    echo "  - pyproject.toml with requires-python >= 3.10"
    echo "  - README.md requirements section"
    echo "  - install.sh version check function"
    echo "  - Marker file Python metadata"
    echo "  - Integration guide prerequisites"
    echo "  - Cross-repository consistency"
    echo ""
    echo -e "${BLUE}Current Environment:${NC}"
    echo "  Python: $(python3 --version 2>&1)"
    echo "  Bash: $BASH_VERSION"
    echo "  OS: $(uname -s)"
    echo ""
}

run_test_suite() {
    local script=$1
    local name=$2

    echo ""
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}Running: $name${NC}"
    echo -e "${BLUE}================================================${NC}"

    if [ -x "$script" ]; then
        if bash "$script"; then
            echo -e "${GREEN}✓ $name completed successfully${NC}"
            return 0
        else
            echo -e "${RED}✗ $name had failures${NC}"
            return 1
        fi
    else
        echo -e "${RED}✗ Test script not executable: $script${NC}"
        chmod +x "$script"
        echo "  Fixed permissions, please run again"
        return 1
    fi
}

# Make all test scripts executable
chmod +x "$TEST_DIR"/*.sh 2>/dev/null || true

print_header

# Track overall results
TOTAL_SUITES=0
PASSED_SUITES=0
FAILED_SUITES=0

# Test Suite 1: Static Validation
TOTAL_SUITES=$((TOTAL_SUITES + 1))
if run_test_suite "$TEST_DIR/test-static-validation.sh" "Static Validation Tests"; then
    PASSED_SUITES=$((PASSED_SUITES + 1))
else
    FAILED_SUITES=$((FAILED_SUITES + 1))
fi

# Test Suite 2: Version Check Function
TOTAL_SUITES=$((TOTAL_SUITES + 1))
if run_test_suite "$TEST_DIR/test-version-check-function.sh" "Version Check Function Tests"; then
    PASSED_SUITES=$((PASSED_SUITES + 1))
else
    FAILED_SUITES=$((FAILED_SUITES + 1))
fi

# Test Suite 3: Installation with Python 3.9 (may skip if not available)
TOTAL_SUITES=$((TOTAL_SUITES + 1))
if run_test_suite "$TEST_DIR/test-installation-python39.sh" "Installation Tests (Python 3.9)"; then
    PASSED_SUITES=$((PASSED_SUITES + 1))
else
    FAILED_SUITES=$((FAILED_SUITES + 1))
fi

# Test Suite 4: Installation with Python 3.10+ (may skip if not available)
TOTAL_SUITES=$((TOTAL_SUITES + 1))
if run_test_suite "$TEST_DIR/test-installation-python310.sh" "Installation Tests (Python 3.10+)"; then
    PASSED_SUITES=$((PASSED_SUITES + 1))
else
    FAILED_SUITES=$((FAILED_SUITES + 1))
fi

# Test Suite 5: Cross-Repository Consistency
TOTAL_SUITES=$((TOTAL_SUITES + 1))
if run_test_suite "$TEST_DIR/test-cross-repo-consistency.sh" "Cross-Repository Consistency Tests"; then
    PASSED_SUITES=$((PASSED_SUITES + 1))
else
    FAILED_SUITES=$((FAILED_SUITES + 1))
fi

# Final Summary
echo ""
echo "========================================================"
echo "OVERALL TEST RESULTS"
echo "========================================================"
echo ""
echo -e "Test Suites Run: $TOTAL_SUITES"
echo -e "Passed: ${GREEN}$PASSED_SUITES${NC}"
echo -e "Failed: ${RED}$FAILED_SUITES${NC}"
echo ""

if [ $FAILED_SUITES -eq 0 ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  ALL TEST SUITES PASSED SUCCESSFULLY!     ║${NC}"
    echo -e "${GREEN}║  TASK-IMP-232B implementation validated   ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}"
    echo ""
    exit 0
else
    echo -e "${RED}╔════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║  SOME TEST SUITES FAILED                  ║${NC}"
    echo -e "${RED}║  Review output above for details          ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Note: Some tests may be skipped if environment doesn't match"
    echo "      (e.g., Python 3.9 tests on Python 3.10+ system)"
    echo ""
    exit 1
fi
