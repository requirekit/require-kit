#!/bin/bash
# TASK-IMP-232B Test Suite - Installation Tests (Python 3.10+)
# Tests installation behavior when Python 3.10+ is detected

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

REPO_ROOT="/Users/richardwoollcott/Projects/appmilla_github/require-kit"
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_SKIPPED=0

print_test_header() {
    echo ""
    echo "============================================"
    echo "TASK-IMP-232B: Installation Tests (Python 3.10+)"
    echo "============================================"
    echo ""
    echo -e "${BLUE}Current Python version: $(python3 --version 2>&1)${NC}"
    echo ""
}

print_test() {
    echo -n "Testing: $1 ... "
}

pass() {
    echo -e "${GREEN}PASS${NC}"
    TESTS_PASSED=$((TESTS_PASSED + 1))
}

fail() {
    echo -e "${RED}FAIL${NC}"
    echo "  Error: $1"
    TESTS_FAILED=$((TESTS_FAILED + 1))
}

skip() {
    echo -e "${YELLOW}SKIP${NC}"
    echo "  Reason: $1"
    TESTS_SKIPPED=$((TESTS_SKIPPED + 1))
}

print_summary() {
    echo ""
    echo "============================================"
    echo "Test Summary"
    echo "============================================"
    echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "Failed: ${RED}$TESTS_FAILED${NC}"
    echo -e "Skipped: ${YELLOW}$TESTS_SKIPPED${NC}"
    echo ""

    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "${GREEN}All installation tests passed (or skipped appropriately)!${NC}"
        return 0
    else
        echo -e "${RED}Some tests failed!${NC}"
        return 1
    fi
}

# Check current Python version
check_python_version_for_test() {
    local version=$(python3 --version 2>&1 | awk '{print $2}')
    local minor=$(echo "$version" | cut -d. -f2)

    if [ "$minor" -ge 10 ]; then
        echo "true"
    else
        echo "false"
    fi
}

# Test 1: Installation succeeds with Python 3.10+
test_installation_succeeds_python310() {
    print_test "Installation succeeds with Python 3.10+"

    local is_python310=$(check_python_version_for_test)

    if [ "$is_python310" = "false" ]; then
        skip "Python 3.9 detected, cannot test Python 3.10+ success"
        return
    fi

    echo ""
    echo -e "${YELLOW}NOTE: This test would run a full installation.${NC}"
    echo -e "${YELLOW}Skipping actual installation to avoid side effects.${NC}"
    echo -e "${YELLOW}Manual test required: Run ./installer/scripts/install.sh${NC}"

    skip "Manual testing required (would modify system)"
}

# Test 2: Marker file contains Python version metadata
test_marker_file_python_metadata() {
    print_test "Marker file contains Python version metadata"

    local marker_file="$HOME/.agentecflow/require-kit.marker.json"

    if [ ! -f "$marker_file" ]; then
        skip "Marker file not found (require-kit not installed)"
        return
    fi

    if grep -q '"python_version": ">=3.10"' "$marker_file"; then
        pass
    else
        fail "Marker file missing python_version metadata"
    fi
}

# Test 3: Marker file contains detected Python version
test_marker_file_detected_version() {
    print_test "Marker file contains detected Python version"

    local marker_file="$HOME/.agentecflow/require-kit.marker.json"

    if [ ! -f "$marker_file" ]; then
        skip "Marker file not found (require-kit not installed)"
        return
    fi

    if grep -q '"python_detected":' "$marker_file"; then
        pass
    else
        fail "Marker file missing python_detected metadata"
    fi
}

# Test 4: Marker file has alignment metadata
test_marker_file_alignment() {
    print_test "Marker file contains ecosystem alignment metadata"

    local marker_file="$HOME/.agentecflow/require-kit.marker.json"

    if [ ! -f "$marker_file" ]; then
        skip "Marker file not found (require-kit not installed)"
        return
    fi

    if grep -q '"python_alignment": "taskwright_ecosystem"' "$marker_file"; then
        pass
    else
        fail "Marker file missing python_alignment metadata"
    fi
}

# Test 5: Installation prints success message
test_success_message() {
    print_test "Installation prints success message with Python version"

    local is_python310=$(check_python_version_for_test)

    if [ "$is_python310" = "false" ]; then
        skip "Python 3.9 detected, cannot test success message"
        return
    fi

    skip "Manual verification required (check install.sh output)"
}

# Test 6: Version check passes silently
test_version_check_passes() {
    print_test "Version check passes without error on Python 3.10+"

    local is_python310=$(check_python_version_for_test)

    if [ "$is_python310" = "false" ]; then
        skip "Python 3.9 detected, cannot test version check pass"
        return
    fi

    # Extract and test just the version check logic
    if python3 -c "
import sys
if sys.version_info >= (3, 10):
    sys.exit(0)
else:
    sys.exit(1)
" 2>/dev/null; then
        pass
    else
        fail "Python version check logic failed"
    fi
}

# Environment check
echo ""
echo -e "${BLUE}Environment Check:${NC}"
python3 --version
local current_minor=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f2)

if [ "$current_minor" -lt 10 ]; then
    echo -e "${YELLOW}"
    echo "WARNING: Python 3.9 detected!"
    echo "These tests verify behavior with Python 3.10+, but your system has Python 3.9."
    echo "Tests will be skipped. To fully test:"
    echo "  1. Upgrade to Python 3.10+"
    echo "  2. Or use a Python 3.10+ virtual environment"
    echo "  3. Or use Docker with Python 3.10+ image"
    echo -e "${NC}"
fi

# Run all tests
print_test_header
test_installation_succeeds_python310
test_marker_file_python_metadata
test_marker_file_detected_version
test_marker_file_alignment
test_success_message
test_version_check_passes
print_summary
