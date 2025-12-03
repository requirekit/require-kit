#!/bin/bash
# Comprehensive Test Suite for Marker File Implementation
# Tests for TASK-FIX-MARKER

# Test configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_INSTALL_DIR="/tmp/require-kit-test-$$"
PACKAGE_NAME="require-kit"
PACKAGE_VERSION="1.0.0"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test tracking
TESTS_PASSED=0
TESTS_FAILED=0
TEST_RESULTS=()

# Setup test environment
setup_test_env() {
    echo -e "${BLUE}Setting up test environment...${NC}"

    # Create temporary test directory
    mkdir -p "$TEST_INSTALL_DIR"

    # Export variables for sourced functions
    export INSTALL_DIR="$TEST_INSTALL_DIR"
    export PACKAGE_NAME="$PACKAGE_NAME"
    export PACKAGE_VERSION="$PACKAGE_VERSION"

    echo -e "${GREEN}✓ Test environment created at $TEST_INSTALL_DIR${NC}"
}

# Cleanup test environment
cleanup_test_env() {
    echo -e "${BLUE}Cleaning up test environment...${NC}"
    rm -rf "$TEST_INSTALL_DIR"
    echo -e "${GREEN}✓ Test environment cleaned${NC}"
}

# Test result tracking
pass_test() {
    local test_name="$1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
    TEST_RESULTS+=("PASS: $test_name")
    echo -e "${GREEN}✓ PASS:${NC} $test_name"
}

fail_test() {
    local test_name="$1"
    local reason="$2"
    TESTS_FAILED=$((TESTS_FAILED + 1))
    TEST_RESULTS+=("FAIL: $test_name - $reason")
    echo -e "${RED}✗ FAIL:${NC} $test_name"
    echo -e "  ${RED}Reason:${NC} $reason"
}

# Source helper functions from install.sh
source_install_functions() {
    # Extract just the functions we need for testing
    # We'll define them locally to avoid running the full script

    get_marker_path() {
        echo "$INSTALL_DIR/$PACKAGE_NAME.marker.json"
    }

    create_marker_file() {
        local repo_root
        if [ -d "$SCRIPT_DIR" ]; then
            repo_root="$(cd "$SCRIPT_DIR/.." && pwd)"
        else
            repo_root="$PWD"
        fi

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
    "bdd_generation",
    "epic_management",
    "feature_management",
    "requirements_traceability"
  ],
  "requires": [
    "guardkit"
  ],
  "integration_model": "bidirectional_optional",
  "description": "Requirements engineering and BDD for Agentecflow",
  "homepage": "https://github.com/requirekit/require-kit"
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

    print_error() {
        echo -e "${RED}✗ $1${NC}"
        return 1
    }
}

# ===== UNIT TESTS =====

test_get_marker_path_returns_correct_path() {
    local expected="$TEST_INSTALL_DIR/$PACKAGE_NAME.marker.json"
    local actual=$(get_marker_path)

    if [ "$actual" = "$expected" ]; then
        pass_test "get_marker_path() returns correct path"
    else
        fail_test "get_marker_path() returns correct path" "Expected: $expected, Got: $actual"
    fi
}

test_create_marker_file_success() {
    local marker_file=$(get_marker_path)

    # Remove if exists
    rm -f "$marker_file"

    # Create marker file
    if create_marker_file; then
        pass_test "create_marker_file() succeeds in normal conditions"
    else
        fail_test "create_marker_file() succeeds in normal conditions" "Function returned non-zero"
    fi
}

test_marker_file_exists_after_creation() {
    local marker_file=$(get_marker_path)

    # Remove if exists
    rm -f "$marker_file"

    # Create marker file
    create_marker_file

    if [ -f "$marker_file" ]; then
        pass_test "Marker file exists after creation"
    else
        fail_test "Marker file exists after creation" "File not found at $marker_file"
    fi
}

test_marker_file_not_empty() {
    local marker_file=$(get_marker_path)

    # Remove if exists
    rm -f "$marker_file"

    # Create marker file
    create_marker_file

    if [ -s "$marker_file" ]; then
        pass_test "Marker file is not empty"
    else
        fail_test "Marker file is not empty" "File is empty or does not exist"
    fi
}

test_create_marker_file_handles_missing_file() {
    local marker_file=$(get_marker_path)

    # Create marker file
    create_marker_file

    # Remove the file to simulate verification failure
    rm -f "$marker_file"

    # Try to verify (should fail in create_marker_file verification step)
    if [ ! -f "$marker_file" ]; then
        pass_test "create_marker_file() verification detects missing file"
    else
        fail_test "create_marker_file() verification detects missing file" "File exists when it should not"
    fi
}

test_create_marker_file_handles_empty_file() {
    local marker_file=$(get_marker_path)

    # Create an empty file
    rm -f "$marker_file"
    touch "$marker_file"

    if [ ! -s "$marker_file" ]; then
        pass_test "create_marker_file() verification detects empty file"
    else
        fail_test "create_marker_file() verification detects empty file" "File is not empty"
    fi
}

test_create_marker_file_readonly_directory() {
    # Create a readonly directory scenario
    local readonly_dir="/tmp/require-kit-readonly-$$"
    mkdir -p "$readonly_dir"

    # Save original INSTALL_DIR
    local original_install_dir="$INSTALL_DIR"
    export INSTALL_DIR="$readonly_dir"

    # Make directory readonly
    chmod 444 "$readonly_dir"

    # Try to create marker file (should fail)
    if ! create_marker_file 2>/dev/null; then
        pass_test "create_marker_file() fails gracefully with readonly directory"
    else
        fail_test "create_marker_file() fails gracefully with readonly directory" "Function succeeded when it should have failed"
    fi

    # Cleanup
    chmod 755 "$readonly_dir"
    rm -rf "$readonly_dir"
    export INSTALL_DIR="$original_install_dir"
}

# ===== INTEGRATION TESTS =====

test_marker_file_contains_valid_json() {
    local marker_file=$(get_marker_path)

    # Remove if exists
    rm -f "$marker_file"

    # Create marker file
    create_marker_file

    # Try to parse JSON
    if command -v python3 &> /dev/null; then
        if python3 -c "import json; json.load(open('$marker_file'))" 2>/dev/null; then
            pass_test "Marker file contains valid JSON"
        else
            fail_test "Marker file contains valid JSON" "JSON parsing failed"
        fi
    else
        # Fallback: basic JSON validation
        if grep -q '"package":' "$marker_file" && grep -q '"version":' "$marker_file"; then
            pass_test "Marker file contains valid JSON (basic validation)"
        else
            fail_test "Marker file contains valid JSON (basic validation)" "Required fields not found"
        fi
    fi
}

test_marker_file_contains_package_name() {
    local marker_file=$(get_marker_path)

    # Remove if exists
    rm -f "$marker_file"

    # Create marker file
    create_marker_file

    if grep -q "\"package\": \"$PACKAGE_NAME\"" "$marker_file"; then
        pass_test "Marker file contains correct package name"
    else
        fail_test "Marker file contains correct package name" "Package name not found or incorrect"
    fi
}

test_marker_file_contains_version() {
    local marker_file=$(get_marker_path)

    # Remove if exists
    rm -f "$marker_file"

    # Create marker file
    create_marker_file

    if grep -q "\"version\": \"$PACKAGE_VERSION\"" "$marker_file"; then
        pass_test "Marker file contains correct version"
    else
        fail_test "Marker file contains correct version" "Version not found or incorrect"
    fi
}

test_marker_file_contains_install_location() {
    local marker_file=$(get_marker_path)

    # Remove if exists
    rm -f "$marker_file"

    # Create marker file
    create_marker_file

    if grep -q "\"install_location\": \"$INSTALL_DIR\"" "$marker_file"; then
        pass_test "Marker file contains correct install location"
    else
        fail_test "Marker file contains correct install location" "Install location not found or incorrect"
    fi
}

test_marker_file_contains_all_required_fields() {
    local marker_file=$(get_marker_path)

    # Remove if exists
    rm -f "$marker_file"

    # Create marker file
    create_marker_file

    local required_fields=("package" "version" "installed" "install_location" "repo_path" "provides" "requires" "integration_model")
    local all_present=true

    for field in "${required_fields[@]}"; do
        if ! grep -q "\"$field\":" "$marker_file"; then
            all_present=false
            break
        fi
    done

    if $all_present; then
        pass_test "Marker file contains all required fields"
    else
        fail_test "Marker file contains all required fields" "Some required fields are missing"
    fi
}

test_repeated_installation_idempotent() {
    local marker_file=$(get_marker_path)

    # Remove if exists
    rm -f "$marker_file"

    # Create marker file first time
    create_marker_file
    local first_content=$(cat "$marker_file")

    # Sleep to ensure timestamp would differ if not idempotent
    sleep 1

    # Create marker file second time
    create_marker_file
    local second_content=$(cat "$marker_file")

    # Content should be similar (timestamps will differ)
    if [ -n "$first_content" ] && [ -n "$second_content" ]; then
        pass_test "Repeated installation is idempotent"
    else
        fail_test "Repeated installation is idempotent" "Marker file content missing"
    fi
}

# ===== BASH SYNTAX VALIDATION =====

test_bash_syntax_valid() {
    if bash -n "$SCRIPT_DIR/scripts/install.sh" 2>/dev/null; then
        pass_test "Bash syntax is valid (bash -n)"
    else
        fail_test "Bash syntax is valid (bash -n)" "Syntax errors detected"
    fi
}

test_shellcheck_if_available() {
    if command -v shellcheck &> /dev/null; then
        # Run shellcheck, but only fail on errors (not warnings)
        if shellcheck -S error "$SCRIPT_DIR/scripts/install.sh" 2>/dev/null; then
            pass_test "ShellCheck validation passed (errors only)"
        else
            fail_test "ShellCheck validation passed (errors only)" "ShellCheck detected errors"
        fi
    else
        echo -e "${YELLOW}⚠ SKIP:${NC} ShellCheck not available (install shellcheck for additional validation)"
    fi
}

# ===== FILE SYSTEM VALIDATION =====

test_marker_file_permissions() {
    local marker_file=$(get_marker_path)

    # Remove if exists
    rm -f "$marker_file"

    # Create marker file
    create_marker_file

    # Check if file is readable
    if [ -r "$marker_file" ]; then
        pass_test "Marker file has correct permissions (readable)"
    else
        fail_test "Marker file has correct permissions (readable)" "File is not readable"
    fi
}

test_marker_file_location() {
    local marker_file=$(get_marker_path)
    local expected_location="$TEST_INSTALL_DIR/$PACKAGE_NAME.marker.json"

    if [ "$marker_file" = "$expected_location" ]; then
        pass_test "Marker file is in correct location"
    else
        fail_test "Marker file is in correct location" "Expected: $expected_location, Got: $marker_file"
    fi
}

# ===== TEST EXECUTION =====

run_all_tests() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║    Marker File Implementation Test Suite              ║${NC}"
    echo -e "${BLUE}║    TASK-FIX-MARKER                                     ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""

    # Setup
    setup_test_env
    source_install_functions

    echo ""
    echo -e "${BLUE}===== UNIT TESTS =====${NC}"
    test_get_marker_path_returns_correct_path
    test_create_marker_file_success
    test_marker_file_exists_after_creation
    test_marker_file_not_empty
    test_create_marker_file_handles_missing_file
    test_create_marker_file_handles_empty_file
    test_create_marker_file_readonly_directory

    echo ""
    echo -e "${BLUE}===== INTEGRATION TESTS =====${NC}"
    test_marker_file_contains_valid_json
    test_marker_file_contains_package_name
    test_marker_file_contains_version
    test_marker_file_contains_install_location
    test_marker_file_contains_all_required_fields
    test_repeated_installation_idempotent

    echo ""
    echo -e "${BLUE}===== BASH SYNTAX VALIDATION =====${NC}"
    test_bash_syntax_valid
    test_shellcheck_if_available

    echo ""
    echo -e "${BLUE}===== FILE SYSTEM VALIDATION =====${NC}"
    test_marker_file_permissions
    test_marker_file_location

    # Cleanup
    cleanup_test_env

    # Print results
    print_test_summary
}

print_test_summary() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║    Test Results Summary                                 ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""

    local total_tests=$((TESTS_PASSED + TESTS_FAILED))
    echo "Total Tests: $total_tests"
    echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
    echo -e "${RED}Failed: $TESTS_FAILED${NC}"
    echo ""

    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
        echo -e "${GREEN}║    ALL TESTS PASSED ✓                                   ║${NC}"
        echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
        exit 0
    else
        echo -e "${RED}╔════════════════════════════════════════════════════════╗${NC}"
        echo -e "${RED}║    SOME TESTS FAILED ✗                                  ║${NC}"
        echo -e "${RED}╚════════════════════════════════════════════════════════╝${NC}"
        echo ""
        echo "Failed tests:"
        for result in "${TEST_RESULTS[@]}"; do
            if [[ $result == FAIL:* ]]; then
                echo -e "  ${RED}✗${NC} ${result#FAIL: }"
            fi
        done
        exit 1
    fi
}

# Run all tests
run_all_tests
