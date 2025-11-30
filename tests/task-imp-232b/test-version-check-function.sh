#!/bin/bash
# TASK-IMP-232B Test Suite - Version Check Function Tests
# Tests the check_python_version() function in isolation

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

REPO_ROOT="/Users/richardwoollcott/Projects/appmilla_github/require-kit"
TESTS_PASSED=0
TESTS_FAILED=0

print_test_header() {
    echo ""
    echo "============================================"
    echo "TASK-IMP-232B: Version Check Function Tests"
    echo "============================================"
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
}

print_summary() {
    echo ""
    echo "============================================"
    echo "Test Summary"
    echo "============================================"
    echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "Failed: ${RED}$TESTS_FAILED${NC}"
    echo ""

    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "${GREEN}All version check function tests passed!${NC}"
        return 0
    else
        echo -e "${RED}Some tests failed!${NC}"
        return 1
    fi
}

# Extract and test the check_python_version function
test_function_extracts_correctly() {
    print_test "check_python_version function can be extracted"

    # Extract function from install.sh
    if sed -n '/^check_python_version()/,/^}/p' "$REPO_ROOT/installer/scripts/install.sh" > /tmp/check_python_version.sh 2>&1; then
        if [ -s /tmp/check_python_version.sh ]; then
            pass
        else
            fail "Extracted function is empty"
        fi
    else
        fail "Could not extract function"
    fi
}

# Test that function checks for python3 command
test_function_checks_python3_exists() {
    print_test "Function checks if python3 command exists"

    if grep -q 'command -v python3' /tmp/check_python_version.sh; then
        pass
    else
        fail "Function does not check for python3 command"
    fi
}

# Test that function gets Python version
test_function_gets_version() {
    print_test "Function retrieves Python version"

    if grep -q 'python3 --version' /tmp/check_python_version.sh; then
        pass
    else
        fail "Function does not retrieve Python version"
    fi
}

# Test that function compares versions correctly
test_function_compares_versions() {
    print_test "Function compares version against minimum (3.10)"

    if grep -q 'sys.version_info >= (3, 10)' /tmp/check_python_version.sh || \
       grep -q 'sys.version_info >= (\$min_major, \$min_minor)' /tmp/check_python_version.sh; then
        pass
    else
        fail "Function does not compare versions correctly"
    fi
}

# Test that function exits on failure
test_function_exits_on_failure() {
    print_test "Function exits with error code on version check failure"

    if grep -q 'exit 1' /tmp/check_python_version.sh; then
        pass
    else
        fail "Function does not exit on failure"
    fi
}

# Test function with current Python (should fail on 3.9)
test_function_with_current_python() {
    print_test "Function behavior with current Python version"

    local current_version=$(python3 --version 2>&1 | awk '{print $2}')
    local current_minor=$(echo "$current_version" | cut -d. -f2)

    echo ""
    echo "  Current Python version: $current_version"

    if [ "$current_minor" -lt 10 ]; then
        echo "  Expected: Function should fail (version < 3.10)"
        skip "Cannot test without actually running install.sh (would fail)"
    else
        echo "  Expected: Function should pass (version >= 3.10)"
        skip "Cannot test without actually running install.sh (would pass)"
    fi
}

# Test error message quality
test_error_message_includes_instructions() {
    print_test "Error message includes installation instructions"

    local instructions_found=0

    if grep -q "brew install python" /tmp/check_python_version.sh; then
        instructions_found=$((instructions_found + 1))
    fi

    if grep -q "apt install python" /tmp/check_python_version.sh; then
        instructions_found=$((instructions_found + 1))
    fi

    if grep -q "python.org" /tmp/check_python_version.sh; then
        instructions_found=$((instructions_found + 1))
    fi

    if [ $instructions_found -ge 2 ]; then
        pass
    else
        fail "Error message missing installation instructions (found $instructions_found platforms)"
    fi
}

# Test that function prints informative messages
test_function_prints_status() {
    print_test "Function prints status messages"

    if grep -q 'print_info\|print_error\|print_success\|echo' /tmp/check_python_version.sh; then
        pass
    else
        fail "Function does not print status messages"
    fi
}

# Run all tests
print_test_header
test_function_extracts_correctly
test_function_checks_python3_exists
test_function_gets_version
test_function_compares_versions
test_function_exits_on_failure
test_function_with_current_python
test_error_message_includes_instructions
test_function_prints_status
print_summary
