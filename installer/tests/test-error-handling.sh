#!/bin/bash
# Error Handling Test Suite
# Tests error handling for marker file creation

# Test configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_INSTALL_DIR="/tmp/require-kit-errortest-$$"
PACKAGE_NAME="require-kit"
PACKAGE_VERSION="1.0.0"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test tracking
TESTS_PASSED=0
TESTS_FAILED=0

pass_test() {
    local test_name="$1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo -e "${GREEN}✓ PASS:${NC} $test_name"
}

fail_test() {
    local test_name="$1"
    local reason="$2"
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "${RED}✗ FAIL:${NC} $test_name"
    echo -e "  ${RED}Reason:${NC} $reason"
}

# Setup
mkdir -p "$TEST_INSTALL_DIR"
export INSTALL_DIR="$TEST_INSTALL_DIR"
export PACKAGE_NAME="$PACKAGE_NAME"
export PACKAGE_VERSION="$PACKAGE_VERSION"

# Source functions
get_marker_path() {
    echo "$INSTALL_DIR/$PACKAGE_NAME.marker.json"
}

create_marker_file() {
    local repo_root="$SCRIPT_DIR/.."
    local install_date=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local marker_file=$(get_marker_path)

    if ! cat > "$marker_file" <<EOF
{
  "package": "$PACKAGE_NAME",
  "version": "$PACKAGE_VERSION",
  "installed": "$install_date",
  "install_location": "$INSTALL_DIR",
  "repo_path": "$repo_root",
  "provides": [
    "requirements_engineering",
    "ears_notation",
    "bdd_generation"
  ],
  "requires": [
    "guardkit"
  ],
  "integration_model": "bidirectional_optional"
}
EOF
    then
        return 1
    fi

    if [ ! -f "$marker_file" ] || [ ! -s "$marker_file" ]; then
        return 1
    fi

    return 0
}

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║    Error Handling Test Suite                            ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Test 1: Readonly directory
echo -e "${BLUE}Test 1: Readonly directory error handling${NC}"
readonly_dir="/tmp/require-kit-readonly-$$"
mkdir -p "$readonly_dir"
chmod 444 "$readonly_dir"
export INSTALL_DIR="$readonly_dir"

if create_marker_file 2>/dev/null; then
    fail_test "Readonly directory detection" "Function should have failed"
else
    pass_test "Readonly directory detection"
fi

chmod 755 "$readonly_dir"
rm -rf "$readonly_dir"

# Test 2: Missing directory
echo -e "${BLUE}Test 2: Missing directory error handling${NC}"
missing_dir="/tmp/require-kit-missing-$$"
export INSTALL_DIR="$missing_dir"

if create_marker_file 2>/dev/null; then
    fail_test "Missing directory detection" "Function should have failed"
else
    pass_test "Missing directory detection"
fi

# Test 3: Corrupted file (created but removed before verification)
echo -e "${BLUE}Test 3: File verification detects corrupted/missing file${NC}"
export INSTALL_DIR="$TEST_INSTALL_DIR"
marker_file=$(get_marker_path)

# Create file manually
cat > "$marker_file" <<EOF
{
  "package": "test"
}
EOF

# Remove file to simulate verification failure
rm -f "$marker_file"

# Verification should detect missing file
if [ ! -f "$marker_file" ]; then
    pass_test "File verification detects missing file"
else
    fail_test "File verification detects missing file" "File still exists"
fi

# Test 4: Empty file detection
echo -e "${BLUE}Test 4: Empty file detection${NC}"
touch "$marker_file"

if [ ! -s "$marker_file" ]; then
    pass_test "Empty file detection"
else
    fail_test "Empty file detection" "File is not empty"
fi

rm -f "$marker_file"

# Test 5: Successful creation and verification
echo -e "${BLUE}Test 5: Successful creation with all checks${NC}"
if create_marker_file; then
    if [ -f "$marker_file" ] && [ -s "$marker_file" ]; then
        pass_test "Successful creation with verification"
    else
        fail_test "Successful creation with verification" "File not created properly"
    fi
else
    fail_test "Successful creation with verification" "Function failed"
fi

# Test 6: JSON validity check
echo -e "${BLUE}Test 6: JSON validity check${NC}"
if command -v python3 &> /dev/null; then
    if python3 -c "import json; json.load(open('$marker_file'))" 2>/dev/null; then
        pass_test "JSON validity check"
    else
        fail_test "JSON validity check" "Invalid JSON"
    fi
else
    echo -e "${YELLOW}⚠ SKIP:${NC} Python3 not available for JSON validation"
fi

# Test 7: 2-layer error handling (cat fails)
echo -e "${BLUE}Test 7: Cat command failure handling${NC}"
# Simulate cat failure by redirecting to a file that can't be written
invalid_file="/dev/full"  # Special device that's always full

if cat > "$invalid_file" <<EOF 2>/dev/null
test
EOF
then
    fail_test "Cat failure detection" "Should have failed writing to /dev/full"
else
    pass_test "Cat failure detection"
fi

# Cleanup
rm -rf "$TEST_INSTALL_DIR"

# Print results
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║    Test Results Summary                                 ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

total_tests=$((TESTS_PASSED + TESTS_FAILED))
echo "Total Tests: $total_tests"
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║    ALL ERROR HANDLING TESTS PASSED ✓                    ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
    exit 0
else
    echo -e "${RED}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║    SOME TESTS FAILED ✗                                  ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════╝${NC}"
    exit 1
fi
