#!/bin/bash
# TASK-IMP-232B Test Suite - Cross-Repository Consistency Tests
# Verifies that require-kit and taskwright have consistent version requirements

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

REPO_ROOT="/Users/richardwoollcott/Projects/appmilla_github/require-kit"
TASKWRIGHT_REPO="/Users/richardwoollcott/Projects/appmilla_github/taskwright"

TESTS_PASSED=0
TESTS_FAILED=0
TESTS_SKIPPED=0

print_test_header() {
    echo ""
    echo "============================================"
    echo "TASK-IMP-232B: Cross-Repository Consistency"
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
        echo -e "${GREEN}All cross-repository tests passed!${NC}"
        return 0
    else
        echo -e "${RED}Some tests failed!${NC}"
        return 1
    fi
}

# Test 1: taskwright repository exists
test_taskwright_repo_exists() {
    print_test "taskwright repository exists at expected location"

    if [ -d "$TASKWRIGHT_REPO" ]; then
        pass
    else
        skip "taskwright repository not found at $TASKWRIGHT_REPO"
        echo ""
        echo -e "${BLUE}To enable cross-repository tests:${NC}"
        echo "  git clone https://github.com/taskwright-dev/taskwright.git"
        echo "  Place at: $TASKWRIGHT_REPO"
    fi
}

# Test 2: Both have pyproject.toml
test_both_have_pyproject() {
    print_test "Both repositories have pyproject.toml"

    if [ ! -d "$TASKWRIGHT_REPO" ]; then
        skip "taskwright repository not found"
        return
    fi

    if [ -f "$REPO_ROOT/pyproject.toml" ] && [ -f "$TASKWRIGHT_REPO/pyproject.toml" ]; then
        pass
    else
        fail "One or both repositories missing pyproject.toml"
    fi
}

# Test 3: Python version requirements match
test_python_version_consistency() {
    print_test "Python version requirements are consistent (>=3.10)"

    if [ ! -d "$TASKWRIGHT_REPO" ]; then
        skip "taskwright repository not found"
        return
    fi

    local rk_version=$(grep 'requires-python' "$REPO_ROOT/pyproject.toml" 2>/dev/null || echo "")
    local tw_version=$(grep 'requires-python' "$TASKWRIGHT_REPO/pyproject.toml" 2>/dev/null || echo "")

    if [ -z "$rk_version" ] || [ -z "$tw_version" ]; then
        fail "Could not extract Python version requirements"
        return
    fi

    if echo "$rk_version" | grep -q '>=3.10' && echo "$tw_version" | grep -q '>=3.10'; then
        pass
    else
        fail "Python version requirements do not match"
        echo "  require-kit: $rk_version"
        echo "  taskwright: $tw_version"
    fi
}

# Test 4: Both install scripts check Python version
test_both_check_version() {
    print_test "Both install.sh scripts check Python version"

    if [ ! -d "$TASKWRIGHT_REPO" ]; then
        skip "taskwright repository not found"
        return
    fi

    local rk_has_check=$(grep -c 'check_python_version' "$REPO_ROOT/installer/scripts/install.sh" 2>/dev/null || echo "0")
    local tw_has_check=$(grep -c 'check_python_version' "$TASKWRIGHT_REPO/installer/scripts/install.sh" 2>/dev/null || echo "0")

    if [ "$rk_has_check" -gt 0 ] && [ "$tw_has_check" -gt 0 ]; then
        pass
    else
        fail "One or both install scripts missing version check"
    fi
}

# Test 5: README files mention same Python version
test_readme_consistency() {
    print_test "README files mention Python 3.10 requirement"

    if [ ! -d "$TASKWRIGHT_REPO" ]; then
        skip "taskwright repository not found"
        return
    fi

    local rk_has_310=$(grep -c 'Python 3.10' "$REPO_ROOT/README.md" 2>/dev/null || echo "0")
    local tw_has_310=$(grep -c 'Python 3.10' "$TASKWRIGHT_REPO/README.md" 2>/dev/null || echo "0")

    if [ "$rk_has_310" -gt 0 ] && [ "$tw_has_310" -gt 0 ]; then
        pass
    else
        fail "README files do not consistently mention Python 3.10"
    fi
}

# Test 6: Marker files have consistent format
test_marker_file_format_consistency() {
    print_test "Marker file templates use consistent format"

    if [ ! -d "$TASKWRIGHT_REPO" ]; then
        skip "taskwright repository not found"
        return
    fi

    local rk_has_python_version=$(grep -c '"python_version":' "$REPO_ROOT/installer/scripts/install.sh" 2>/dev/null || echo "0")
    local tw_has_python_version=$(grep -c '"python_version":' "$TASKWRIGHT_REPO/installer/scripts/install.sh" 2>/dev/null || echo "0")

    if [ "$rk_has_python_version" -gt 0 ] && [ "$tw_has_python_version" -gt 0 ]; then
        pass
    else
        fail "Marker file formats are inconsistent (missing python_version)"
    fi
}

# Test 7: Integration guide mentions consistent prerequisites
test_integration_guide_prerequisites() {
    print_test "Integration guide mentions Python 3.10 prerequisite"

    # This guide is in require-kit (authoritative)
    if grep -q 'Python 3.10' "$REPO_ROOT/docs/INTEGRATION-GUIDE.md"; then
        pass
    else
        fail "Integration guide does not mention Python 3.10 prerequisite"
    fi
}

# Test 8: Error messages provide same installation instructions
test_error_message_consistency() {
    print_test "Install scripts provide consistent error messages"

    if [ ! -d "$TASKWRIGHT_REPO" ]; then
        skip "taskwright repository not found"
        return
    fi

    # Check that both mention brew, apt, and python.org
    local rk_platforms=0
    local tw_platforms=0

    grep -q 'brew install python' "$REPO_ROOT/installer/scripts/install.sh" && rk_platforms=$((rk_platforms + 1))
    grep -q 'apt install python' "$REPO_ROOT/installer/scripts/install.sh" && rk_platforms=$((rk_platforms + 1))
    grep -q 'python.org' "$REPO_ROOT/installer/scripts/install.sh" && rk_platforms=$((rk_platforms + 1))

    grep -q 'brew install python' "$TASKWRIGHT_REPO/installer/scripts/install.sh" 2>/dev/null && tw_platforms=$((tw_platforms + 1))
    grep -q 'apt install python' "$TASKWRIGHT_REPO/installer/scripts/install.sh" 2>/dev/null && tw_platforms=$((tw_platforms + 1))
    grep -q 'python.org' "$TASKWRIGHT_REPO/installer/scripts/install.sh" 2>/dev/null && tw_platforms=$((tw_platforms + 1))

    if [ "$rk_platforms" -ge 2 ] && [ "$tw_platforms" -ge 2 ]; then
        pass
    else
        fail "Error messages lack consistent platform coverage"
        echo "  require-kit platforms: $rk_platforms"
        echo "  taskwright platforms: $tw_platforms"
    fi
}

# Run all tests
print_test_header
test_taskwright_repo_exists
test_both_have_pyproject
test_python_version_consistency
test_both_check_version
test_readme_consistency
test_marker_file_format_consistency
test_integration_guide_prerequisites
test_error_message_consistency
print_summary
