#!/bin/bash
# Comprehensive Test Suite for TASK-FIX-MARKER
# Tests marker file creation with error handling and verification

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL_SCRIPT="$SCRIPT_DIR/scripts/install.sh"

TEST_PASSED=0
TEST_FAILED=0
TEST_TOTAL=0

print_test_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

print_pass() {
    echo -e "${GREEN}✅ PASS: $1${NC}"
    TEST_PASSED=$((TEST_PASSED + 1))
    TEST_TOTAL=$((TEST_TOTAL + 1))
}

print_fail() {
    echo -e "${RED}❌ FAIL: $1${NC}"
    TEST_FAILED=$((TEST_FAILED + 1))
    TEST_TOTAL=$((TEST_TOTAL + 1))
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Test 1: Helper Function Exists (DRY Principle)
test_helper_function_exists() {
    print_test_header "Test 1: Helper Function Exists (DRY Principle)"

    local script_content
    script_content=$(cat "$INSTALL_SCRIPT")

    # Verify get_marker_path function exists
    if echo "$script_content" | grep -q "^get_marker_path()"; then
        print_pass "get_marker_path() helper function exists"
    else
        print_fail "get_marker_path() helper function not found"
    fi

    # Verify function implementation
    if echo "$script_content" | grep -A 2 "^get_marker_path()" | grep -q 'echo "$INSTALL_DIR/$PACKAGE_NAME.marker.json"'; then
        print_pass "get_marker_path() returns correct path"
    else
        print_fail "get_marker_path() implementation incorrect"
    fi

    # Verify function is used in create_marker_file
    if echo "$script_content" | grep -A 50 "^create_marker_file()" | grep -q 'local marker_file=$(get_marker_path)'; then
        print_pass "create_marker_file() uses get_marker_path() helper"
    else
        print_fail "create_marker_file() does not use helper function"
    fi

    # Verify function is used in verify_installation
    if echo "$script_content" | grep -A 30 "^verify_installation()" | grep -q 'local marker_file=$(get_marker_path)'; then
        print_pass "verify_installation() uses get_marker_path() helper"
    else
        print_fail "verify_installation() does not use helper function"
    fi
}

# Test 2: Error Handling on Heredoc Creation
test_error_handling_heredoc() {
    print_test_header "Test 2: Error Handling on Heredoc Creation"

    local script_content
    script_content=$(cat "$INSTALL_SCRIPT")

    # Verify heredoc is wrapped in if ! ... then pattern
    if echo "$script_content" | grep -A 30 "^create_marker_file()" | grep -q "if ! cat >"; then
        print_pass "Heredoc write uses 'if ! cat >' pattern for error handling"
    else
        print_fail "Heredoc write does not use error handling pattern"
    fi

    # Verify error message on failure
    if echo "$script_content" | grep -A 45 "^create_marker_file()" | grep -q 'print_error "Failed to create marker file at'; then
        print_pass "Error message 'Failed to create marker file' exists"
    else
        print_fail "Error message not found"
    fi

    # Verify return 1 on failure
    if echo "$script_content" | grep -A 45 "^create_marker_file()" | grep -A 2 'print_error "Failed to create marker file' | grep -q 'return 1'; then
        print_pass "Function returns 1 on heredoc failure"
    else
        print_fail "Function does not return 1 on failure"
    fi
}

# Test 3: File Verification After Creation
test_file_verification() {
    print_test_header "Test 3: File Verification After Creation"

    local script_content
    script_content=$(cat "$INSTALL_SCRIPT")

    # Verify file existence check
    if echo "$script_content" | grep -A 50 "^create_marker_file()" | grep -q 'if \[ ! -f "$marker_file" \]'; then
        print_pass "Verifies marker file exists after creation"
    else
        print_fail "Does not verify file existence"
    fi

    # Verify non-empty check
    if echo "$script_content" | grep -A 50 "^create_marker_file()" | grep -q '\[ ! -s "$marker_file" \]'; then
        print_pass "Verifies marker file is non-empty (-s check)"
    else
        print_fail "Does not verify file is non-empty"
    fi

    # Verify verification error message
    if echo "$script_content" | grep -A 50 "^create_marker_file()" | grep -q 'print_error "Marker file creation verification failed"'; then
        print_pass "Verification failure shows correct error message"
    else
        print_fail "Verification error message not found"
    fi

    # Verify return 1 on verification failure
    if echo "$script_content" | grep -A 50 "^create_marker_file()" | grep -A 2 'print_error "Marker file creation verification failed"' | grep -q 'return 1'; then
        print_pass "Function returns 1 on verification failure"
    else
        print_fail "Function does not return 1 on verification failure"
    fi
}

# Test 4: verify_installation Fail Fast Behavior
test_verify_installation_fail_fast() {
    print_test_header "Test 4: verify_installation() Fail Fast Behavior"

    local script_content
    script_content=$(cat "$INSTALL_SCRIPT")

    # Verify verify_installation uses get_marker_path
    if echo "$script_content" | grep -A 30 "^verify_installation()" | grep -q 'local marker_file=$(get_marker_path)'; then
        print_pass "verify_installation() uses get_marker_path() helper"
    else
        print_fail "verify_installation() does not use helper function"
    fi

    # Verify fail fast check exists
    if echo "$script_content" | grep -A 30 "^verify_installation()" | grep -q 'if \[ ! -f "$marker_file" \] || \[ ! -s "$marker_file" \]'; then
        print_pass "verify_installation() checks file exists and is non-empty"
    else
        print_fail "verify_installation() missing fail-fast checks"
    fi

    # Verify uses print_error (which exits)
    if echo "$script_content" | grep -A 30 "^verify_installation()" | grep -A 1 'if \[ ! -f "$marker_file" \] || \[ ! -s "$marker_file" \]' | grep -q 'print_error "Marker file not created"'; then
        print_pass "verify_installation() calls print_error on failure (fail fast)"
    else
        print_fail "verify_installation() does not fail fast"
    fi
}

# Test 5: Syntax Validation
test_syntax_validation() {
    print_test_header "Test 5: Syntax Validation"

    # Check bash syntax
    if bash -n "$INSTALL_SCRIPT" 2>&1; then
        print_pass "install.sh has valid bash syntax"
    else
        print_fail "install.sh has syntax errors"
    fi
}

# Test 6: Integration Test - Simulated Failure
test_simulated_failure() {
    print_test_header "Test 6: Integration Test - Simulated Failure Handling"

    # Create a test script that simulates create_marker_file
    cat > /tmp/test-marker-creation.sh <<'TESTEOF'
#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

print_error() {
    echo -e "${RED}✗ $1${NC}"
    return 1
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

INSTALL_DIR="/tmp/test-marker"
PACKAGE_NAME="require-kit"

get_marker_path() {
    echo "$INSTALL_DIR/$PACKAGE_NAME.marker.json"
}

# Simulate successful creation
test_successful_creation() {
    mkdir -p "$INSTALL_DIR"
    local marker_file=$(get_marker_path)

    if ! cat > "$marker_file" <<EOF
{
  "package": "$PACKAGE_NAME",
  "version": "1.0.0",
  "test": "data"
}
EOF
    then
        print_error "Failed to create marker file at $marker_file"
        return 1
    fi

    # Verify marker file was created successfully and is non-empty
    if [ ! -f "$marker_file" ] || [ ! -s "$marker_file" ]; then
        print_error "Marker file creation verification failed"
        return 1
    fi

    print_success "Marker file created successfully"
    return 0
}

# Simulate failed creation (read-only directory)
test_failed_creation() {
    local readonly_dir="/tmp/test-readonly-marker"
    mkdir -p "$readonly_dir"
    chmod 444 "$readonly_dir"

    INSTALL_DIR="$readonly_dir"
    local marker_file=$(get_marker_path)

    if ! cat > "$marker_file" <<EOF
{
  "package": "$PACKAGE_NAME",
  "version": "1.0.0"
}
EOF
    then
        print_error "Failed to create marker file at $marker_file"
        chmod 755 "$readonly_dir" 2>/dev/null
        rm -rf "$readonly_dir" 2>/dev/null
        return 1
    fi

    chmod 755 "$readonly_dir" 2>/dev/null
    rm -rf "$readonly_dir" 2>/dev/null
    return 0
}

# Run tests
echo "=== Test 1: Successful Creation ==="
if test_successful_creation; then
    echo "SUCCESS_TEST=PASSED"
else
    echo "SUCCESS_TEST=FAILED"
fi

echo ""
echo "=== Test 2: Failed Creation (should fail) ==="
if test_failed_creation; then
    echo "FAILURE_TEST=SHOULD_HAVE_FAILED"
else
    echo "FAILURE_TEST=CORRECTLY_FAILED"
fi

# Cleanup
rm -rf /tmp/test-marker /tmp/test-readonly-marker 2>/dev/null
TESTEOF

    chmod +x /tmp/test-marker-creation.sh

    # Run test and capture output
    local test_output
    test_output=$(/tmp/test-marker-creation.sh 2>&1)

    print_info "Test output:"
    echo "$test_output"

    # Verify successful creation works
    if echo "$test_output" | grep -q "SUCCESS_TEST=PASSED"; then
        print_pass "Successful marker creation works correctly"
    else
        print_fail "Successful marker creation failed"
    fi

    # Verify failed creation is caught
    if echo "$test_output" | grep -q "FAILURE_TEST=CORRECTLY_FAILED"; then
        print_pass "Failed marker creation is properly caught"
    else
        print_fail "Failed marker creation not caught"
    fi

    # Verify error messages appear
    if echo "$test_output" | grep -q "Failed to create marker file at"; then
        print_pass "Error message displayed on failure"
    else
        print_fail "Error message not displayed"
    fi

    # Cleanup
    rm -f /tmp/test-marker-creation.sh
}

# Test 7: Backward Compatibility
test_backward_compatibility() {
    print_test_header "Test 7: Backward Compatibility"

    local script_content
    script_content=$(cat "$INSTALL_SCRIPT")

    # Verify marker file still uses JSON format
    if echo "$script_content" | grep -A 30 "^create_marker_file()" | grep -q '"package":.*"$PACKAGE_NAME"'; then
        print_pass "Marker file still uses JSON format"
    else
        print_fail "Marker file format changed"
    fi

    # Verify marker filename hasn't changed
    if echo "$script_content" | grep -q '\$PACKAGE_NAME.marker.json'; then
        print_pass "Marker filename format unchanged (.marker.json)"
    else
        print_fail "Marker filename format changed"
    fi

    # Verify create_marker_file is still called from main()
    if echo "$script_content" | grep -A 20 '^main()' | grep -q 'create_marker_file'; then
        print_pass "create_marker_file() still called from main()"
    else
        print_fail "create_marker_file() not called from main()"
    fi
}

# Test 8: Code Quality - DRY Principle
test_dry_principle() {
    print_test_header "Test 8: Code Quality - DRY Principle Compliance"

    local script_content
    script_content=$(cat "$INSTALL_SCRIPT")

    # Count hardcoded marker path occurrences (should be minimal)
    local hardcoded_count
    hardcoded_count=$(echo "$script_content" | grep -c '\$INSTALL_DIR/\$PACKAGE_NAME\.marker\.json' || true)

    print_info "Hardcoded marker path occurrences: $hardcoded_count"

    # Should appear only in get_marker_path function (1 occurrence)
    if [ "$hardcoded_count" -le 2 ]; then
        print_pass "DRY principle followed - minimal hardcoded paths (count: $hardcoded_count)"
    else
        print_fail "DRY principle violated - too many hardcoded paths (count: $hardcoded_count)"
    fi

    # Verify get_marker_path is reused
    local usage_count
    usage_count=$(echo "$script_content" | grep -c 'get_marker_path' || true)

    if [ "$usage_count" -ge 3 ]; then
        print_pass "get_marker_path() reused appropriately (count: $usage_count)"
    else
        print_fail "get_marker_path() not reused enough (count: $usage_count)"
    fi
}

# Main test execution
main() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  TASK-FIX-MARKER Comprehensive Test Suite             ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""

    # Run all tests
    test_helper_function_exists
    test_error_handling_heredoc
    test_file_verification
    test_verify_installation_fail_fast
    test_syntax_validation
    test_simulated_failure
    test_backward_compatibility
    test_dry_principle

    # Print summary
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Test Summary${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo "Total Tests: $TEST_TOTAL"
    echo -e "${GREEN}Passed: $TEST_PASSED${NC}"
    echo -e "${RED}Failed: $TEST_FAILED${NC}"
    echo ""

    # Calculate pass rate
    if [ "$TEST_TOTAL" -gt 0 ]; then
        local pass_rate=$((TEST_PASSED * 100 / TEST_TOTAL))
        echo "Pass Rate: ${pass_rate}%"
        echo ""
    fi

    if [ "$TEST_FAILED" -eq 0 ]; then
        echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
        echo -e "${GREEN}║  ✅ ALL TESTS PASSED - 100% PASS RATE                  ║${NC}"
        echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
        exit 0
    else
        echo -e "${RED}╔════════════════════════════════════════════════════════╗${NC}"
        echo -e "${RED}║  ❌ SOME TESTS FAILED                                   ║${NC}"
        echo -e "${RED}╚════════════════════════════════════════════════════════╝${NC}"
        exit 1
    fi
}

main "$@"
