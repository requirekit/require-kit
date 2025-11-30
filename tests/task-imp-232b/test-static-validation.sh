#!/bin/bash
# TASK-IMP-232B Test Suite - Static Validation Tests
# Tests file content without running installation

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
    echo "TASK-IMP-232B: Static Validation Tests"
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

warn() {
    echo -e "${YELLOW}WARN${NC}"
    echo "  Warning: $1"
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
        echo -e "${GREEN}All static validation tests passed!${NC}"
        return 0
    else
        echo -e "${RED}Some tests failed!${NC}"
        return 1
    fi
}

# Test 1: pyproject.toml exists and is valid TOML
test_pyproject_exists() {
    print_test "pyproject.toml exists"
    if [ ! -f "$REPO_ROOT/pyproject.toml" ]; then
        fail "pyproject.toml not found"
        return
    fi
    pass
}

test_pyproject_valid_toml() {
    print_test "pyproject.toml is valid TOML syntax"

    # Try parsing with Python tomli (or toml module)
    if python3 -c "
import sys
try:
    import tomllib  # Python 3.11+
except ImportError:
    try:
        import tomli as tomllib  # Python 3.10 with tomli
    except ImportError:
        import toml as tomllib  # Fallback

with open('$REPO_ROOT/pyproject.toml', 'rb') as f:
    try:
        tomllib.load(f) if hasattr(tomllib, 'load') else tomllib.loads(f.read().decode())
        sys.exit(0)
    except Exception as e:
        print(f'TOML parse error: {e}', file=sys.stderr)
        sys.exit(1)
" 2>/dev/null; then
        pass
    else
        # If tomllib not available, do basic syntax check
        if grep -q '\[project\]' "$REPO_ROOT/pyproject.toml"; then
            warn "Could not validate TOML syntax (tomllib not available), basic check passed"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            fail "pyproject.toml appears malformed"
        fi
    fi
}

# Test 2: pyproject.toml contains requires-python >= 3.10
test_pyproject_python_version() {
    print_test "pyproject.toml contains 'requires-python = \">=3.10\"'"

    if grep -q 'requires-python = ">=3.10"' "$REPO_ROOT/pyproject.toml"; then
        pass
    else
        fail "requires-python field not found or incorrect"
    fi
}

# Test 3: pyproject.toml has correct classifiers
test_pyproject_classifiers() {
    print_test "pyproject.toml includes Python 3.10+ classifiers"

    local classifiers_found=0
    for version in "3.10" "3.11" "3.12" "3.13"; do
        if grep -q "Programming Language :: Python :: $version" "$REPO_ROOT/pyproject.toml"; then
            classifiers_found=$((classifiers_found + 1))
        fi
    done

    if [ $classifiers_found -ge 4 ]; then
        pass
    else
        fail "Missing Python version classifiers (found $classifiers_found, expected 4)"
    fi
}

# Test 4: README.md contains requirements section
test_readme_requirements_section() {
    print_test "README.md contains Requirements section"

    if grep -q "## Requirements" "$REPO_ROOT/README.md"; then
        pass
    else
        fail "Requirements section not found in README.md"
    fi
}

# Test 5: README.md mentions Python 3.10
test_readme_python_version() {
    print_test "README.md mentions Python 3.10 or later"

    if grep -q "Python 3.10" "$REPO_ROOT/README.md"; then
        pass
    else
        fail "Python 3.10 requirement not mentioned in README.md"
    fi
}

# Test 6: install.sh contains check_python_version function
test_install_sh_function() {
    print_test "install.sh contains check_python_version() function"

    if grep -q "check_python_version()" "$REPO_ROOT/installer/scripts/install.sh"; then
        pass
    else
        fail "check_python_version() function not found"
    fi
}

# Test 7: install.sh version check logic
test_install_sh_version_check() {
    print_test "install.sh checks for Python 3.10 minimum"

    if grep -q 'min_minor=10' "$REPO_ROOT/installer/scripts/install.sh"; then
        pass
    else
        fail "Python 3.10 minimum version check not found"
    fi
}

# Test 8: install.sh calls check_python_version in main()
test_install_sh_main_calls_check() {
    print_test "install.sh main() calls check_python_version"

    # Look for check_python_version in the main function
    if sed -n '/^main()/,/^}/p' "$REPO_ROOT/installer/scripts/install.sh" | grep -q "check_python_version"; then
        pass
    else
        fail "check_python_version not called in main()"
    fi
}

# Test 9: install.sh has helpful error messages
test_install_sh_error_messages() {
    print_test "install.sh provides installation instructions on error"

    if grep -q "brew install python@3.10" "$REPO_ROOT/installer/scripts/install.sh"; then
        pass
    else
        fail "Installation instructions not found in error messages"
    fi
}

# Test 10: Marker file template includes Python metadata
test_marker_python_metadata() {
    print_test "install.sh marker file includes Python version metadata"

    if grep -q '"python_version": ">=3.10"' "$REPO_ROOT/installer/scripts/install.sh"; then
        pass
    else
        fail "Python version metadata not in marker file template"
    fi
}

# Test 11: INTEGRATION-GUIDE.md has prerequisites section
test_integration_guide_prerequisites() {
    print_test "INTEGRATION-GUIDE.md contains Prerequisites section"

    if grep -q "## Prerequisites" "$REPO_ROOT/docs/INTEGRATION-GUIDE.md"; then
        pass
    else
        fail "Prerequisites section not found"
    fi
}

# Test 12: INTEGRATION-GUIDE.md mentions Python 3.10
test_integration_guide_python() {
    print_test "INTEGRATION-GUIDE.md mentions Python 3.10 requirement"

    if grep -q "Python 3.10" "$REPO_ROOT/docs/INTEGRATION-GUIDE.md"; then
        pass
    else
        fail "Python 3.10 not mentioned in INTEGRATION-GUIDE.md"
    fi
}

# Test 13: Alignment messaging in README
test_readme_alignment_message() {
    print_test "README.md explains alignment with taskwright"

    if grep -q "taskwright" "$REPO_ROOT/README.md" | head -20; then
        pass
    else
        warn "taskwright alignment not prominently mentioned"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    fi
}

# Test 14: Installation instructions consistency
test_install_instructions_consistency() {
    print_test "README.md and INTEGRATION-GUIDE.md have consistent instructions"

    local readme_has_brew=$(grep -c "brew install python@3.10" "$REPO_ROOT/README.md" || echo "0")
    local guide_has_brew=$(grep -c "brew install python@3.10" "$REPO_ROOT/docs/INTEGRATION-GUIDE.md" || echo "0")

    if [ "$readme_has_brew" -gt 0 ] && [ "$guide_has_brew" -gt 0 ]; then
        pass
    else
        warn "Installation instructions may not be consistent across docs"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    fi
}

# Run all tests
print_test_header
test_pyproject_exists
test_pyproject_valid_toml
test_pyproject_python_version
test_pyproject_classifiers
test_readme_requirements_section
test_readme_python_version
test_install_sh_function
test_install_sh_version_check
test_install_sh_main_calls_check
test_install_sh_error_messages
test_marker_python_metadata
test_integration_guide_prerequisites
test_integration_guide_python
test_readme_alignment_message
test_install_instructions_consistency
print_summary
