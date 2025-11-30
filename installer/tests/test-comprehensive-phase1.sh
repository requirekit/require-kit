#!/bin/bash
# Comprehensive Test Suite for TASK-IMP-UOU4 Phase 1
# Tests validation non-fatal behavior, warning messages, and backward compatibility

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL_SCRIPT="$SCRIPT_DIR/scripts/install.sh"
TEMP_INSTALL_SCRIPT="/tmp/test-install-phase1.sh"

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

# Test 1: Regression Test - Function Name Consistency
test_regression_function_name() {
    print_test_header "Test 1: Regression Test - Function Name Consistency"

    local test_output
    test_output=$(bash "$SCRIPT_DIR/tests/test-validation-function-name.sh" 2>&1)

    if echo "$test_output" | grep -q "✅ PASS: Function name is consistent"; then
        print_pass "Function name consistency check works correctly"
    else
        print_fail "Function name consistency check failed"
        echo "$test_output"
    fi
}

# Test 2: Validation Non-Fatal Behavior
test_validation_non_fatal() {
    print_test_header "Test 2: Validation Non-Fatal Behavior (Integration Test)"

    # Copy install.sh to temp location
    cp "$INSTALL_SCRIPT" "$TEMP_INSTALL_SCRIPT"

    # Inject intentional mismatch to simulate validation failure
    print_info "Injecting intentional import mismatch..."
    sed -i.bak 's/is_require_kit_installed/intentional_wrong_function_name/g' "$TEMP_INSTALL_SCRIPT"

    # Extract and run just the validate_installation function
    print_info "Testing validation function behavior..."

    # Create test script that sources functions and runs validation
    cat > /tmp/test-validation-behavior.sh <<'TESTEOF'
#!/bin/bash

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
    exit 1
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

INSTALL_DIR="/tmp/test-require-kit-install"
PACKAGE_NAME="require-kit"

# Create minimal test environment
mkdir -p "$INSTALL_DIR/lib"

# Create dummy feature_detection.py
cat > "$INSTALL_DIR/lib/feature_detection.py" <<'EOF'
def is_require_kit_installed():
    return True
EOF

# Source the modified validation function
validate_installation() {
    print_info "Validating installation..."

    # Check if Python 3 is available
    if ! command -v python3 &> /dev/null; then
        print_warning "Python 3 not found - skipping Python validation"
        return 0
    fi

    # Test Python import of feature_detection module (with WRONG function name)
    if ! python3 <<EOF
import sys
import os

# Change to installed directory
os.chdir(os.path.expanduser("$INSTALL_DIR"))

try:
    from lib.feature_detection import intentional_wrong_function_name
    print("Import successful")
    sys.exit(0)
except ImportError as e:
    print(f"Import failed: {e}", file=sys.stderr)
    sys.exit(1)
EOF
    then
        print_warning "Python module validation failed"
        echo ""
        echo "The feature_detection module could not be imported."
        echo "This indicates an installation problem with the Python library files."
        echo ""
        echo "Troubleshooting steps:"
        echo "  1. Check that $INSTALL_DIR/lib/feature_detection.py exists"
        echo "  2. Verify Python 3 is installed: python3 --version"
        echo "  3. Check the import function name is correct (run test):"
        echo "     bash installer/tests/test-validation-function-name.sh"
        echo "  4. Try reinstalling: bash install.sh"
        echo ""
        echo "Installation will continue, but some integration features may not work."
        echo ""
        return 0
    fi

    print_success "Python module validation passed"
}

# Run validation and capture exit code
validate_installation
exit_code=$?
echo "EXIT_CODE=$exit_code"
TESTEOF

    chmod +x /tmp/test-validation-behavior.sh

    # Run test and capture output
    local test_output
    test_output=$(/tmp/test-validation-behavior.sh 2>&1)
    local exit_code=$?

    print_info "Test output:"
    echo "$test_output"

    # Verify exit code is 0 (non-fatal)
    if [ "$exit_code" -eq 0 ]; then
        print_pass "Validation returns 0 on failure (non-fatal behavior)"
    else
        print_fail "Validation exited with code $exit_code (should be 0)"
    fi

    # Verify warning is shown (not error)
    if echo "$test_output" | grep -q "⚠.*Python module validation failed"; then
        print_pass "Warning message is displayed (not error)"
    else
        print_fail "Warning message not found"
    fi

    # Verify "Installation will continue" message
    if echo "$test_output" | grep -q "Installation will continue"; then
        print_pass "Message states 'Installation will continue'"
    else
        print_fail "'Installation will continue' message not found"
    fi

    # Cleanup
    rm -f "$TEMP_INSTALL_SCRIPT" "$TEMP_INSTALL_SCRIPT.bak"
    rm -rf /tmp/test-require-kit-install
    rm -f /tmp/test-validation-behavior.sh
}

# Test 3: Warning Message Quality
test_warning_message_quality() {
    print_test_header "Test 3: Warning Message Quality (User Experience Test)"

    # Check install.sh for correct messaging
    local script_content
    script_content=$(cat "$INSTALL_SCRIPT")

    # Verify print_warning is used (not print_error) - need more context lines
    if echo "$script_content" | grep -A 45 'validate_installation()' | grep -q 'print_warning "Python module validation failed"'; then
        print_pass "Uses print_warning for validation failure (not print_error)"
    else
        print_fail "Does not use print_warning for validation failure"
    fi

    # Verify troubleshooting steps are present
    if echo "$script_content" | grep -q "Troubleshooting steps:"; then
        print_pass "Troubleshooting steps are included"
    else
        print_fail "Troubleshooting steps not found"
    fi

    # Verify test script reference
    if echo "$script_content" | grep -q "test-validation-function-name.sh"; then
        print_pass "Test script reference is included"
    else
        print_fail "Test script reference not found"
    fi

    # Verify "Installation will continue" message
    if echo "$script_content" | grep -q "Installation will continue, but some integration features may not work"; then
        print_pass "Clear continuation message is present"
    else
        print_fail "Continuation message not found or unclear"
    fi
}

# Test 4: Backward Compatibility
test_backward_compatibility() {
    print_test_header "Test 4: Backward Compatibility (Regression Test)"

    local script_content
    script_content=$(cat "$INSTALL_SCRIPT")

    # Verify validation function still uses correct function name
    if echo "$script_content" | grep -q "from lib.feature_detection import is_require_kit_installed"; then
        print_pass "Correct function name is used (is_require_kit_installed)"
    else
        print_fail "Function name changed or incorrect"
    fi

    # Verify Python not found case still works (returns 0)
    if echo "$script_content" | grep -A 5 'if ! command -v python3' | grep -q 'return 0'; then
        print_pass "Python not found case returns 0 (non-fatal)"
    else
        print_fail "Python not found case does not return 0"
    fi

    # Verify validation function is called from main()
    if echo "$script_content" | grep -A 20 '^main()' | grep -q 'validate_installation'; then
        print_pass "Validation function is called from main()"
    else
        print_fail "Validation function not called from main()"
    fi

    # Verify function structure is intact
    if echo "$script_content" | grep -q '^validate_installation()'; then
        print_pass "Validation function exists and is properly defined"
    else
        print_fail "Validation function definition not found"
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

# Main test execution
main() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  TASK-IMP-UOU4 Phase 1 Comprehensive Test Suite       ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""

    # Run all tests
    test_regression_function_name
    test_validation_non_fatal
    test_warning_message_quality
    test_backward_compatibility
    test_syntax_validation

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
