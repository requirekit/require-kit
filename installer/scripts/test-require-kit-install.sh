#!/bin/bash
# Test require-kit Installation
# Verifies that the namespaced installation works correctly

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

TEST_DIR="/tmp/require-kit-install-test-$$"
INSTALL_DIR="$TEST_DIR/.agentecflow"

print_header() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║         require-kit Installation Test                  ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_test() {
    echo -e "${BLUE}▶ $1${NC}"
}

print_pass() {
    echo -e "${GREEN}  ✓ $1${NC}"
}

print_fail() {
    echo -e "${RED}  ✗ $1${NC}"
    FAILED=1
}

print_info() {
    echo -e "${YELLOW}  ℹ $1${NC}"
}

FAILED=0

setup_test() {
    print_test "Setting up test environment..."

    mkdir -p "$TEST_DIR"
    export HOME="$TEST_DIR"

    print_pass "Test directory created: $TEST_DIR"
}

test_installation() {
    print_test "Running installation..."

    cd "$(dirname "${BASH_SOURCE[0]}")/.."

    # Run installer
    if bash scripts/install-require-kit.sh > /dev/null 2>&1; then
        print_pass "Installation completed successfully"
    else
        print_fail "Installation failed"
        return 1
    fi
}

test_directory_structure() {
    print_test "Verifying directory structure..."

    # Check namespaced directories
    if [ -d "$INSTALL_DIR/commands/require-kit" ]; then
        print_pass "Commands directory exists: ~/.agentecflow/commands/require-kit/"
    else
        print_fail "Commands directory missing"
    fi

    if [ -d "$INSTALL_DIR/agents/require-kit" ]; then
        print_pass "Agents directory exists: ~/.agentecflow/agents/require-kit/"
    else
        print_fail "Agents directory missing"
    fi

    if [ -d "$INSTALL_DIR/lib" ]; then
        print_pass "Lib directory exists: ~/.agentecflow/lib/"
    else
        print_fail "Lib directory missing"
    fi

    if [ -d "$INSTALL_DIR/.installed" ]; then
        print_pass "Tracking directory exists: ~/.agentecflow/.installed/"
    else
        print_fail "Tracking directory missing"
    fi
}

test_commands_installed() {
    print_test "Verifying commands installed..."

    local cmd_count=$(ls -1 "$INSTALL_DIR/commands/require-kit"/*.md 2>/dev/null | wc -l)

    if [ "$cmd_count" -gt 0 ]; then
        print_pass "Found $cmd_count commands in require-kit/"

        # Check for key commands
        for cmd in gather-requirements.md formalize-ears.md generate-bdd.md epic-create.md feature-create.md; do
            if [ -f "$INSTALL_DIR/commands/require-kit/$cmd" ]; then
                print_pass "  - $cmd"
            else
                print_info "  - $cmd (not found, may not be implemented yet)"
            fi
        done
    else
        print_fail "No commands found in require-kit/"
    fi
}

test_agents_installed() {
    print_test "Verifying agents installed..."

    local agent_count=$(ls -1 "$INSTALL_DIR/agents/require-kit"/*.md 2>/dev/null | wc -l)

    if [ "$agent_count" -gt 0 ]; then
        print_pass "Found $agent_count agents in require-kit/"

        # Check for key agents
        for agent in requirements-analyst.md bdd-generator.md; do
            if [ -f "$INSTALL_DIR/agents/require-kit/$agent" ]; then
                print_pass "  - $agent"
            else
                print_info "  - $agent (not found, may not be implemented yet)"
            fi
        done
    else
        print_fail "No agents found in require-kit/"
    fi
}

test_symlinks() {
    print_test "Verifying backwards-compatibility symlinks..."

    # Count symlinks in commands/
    local symlink_count=0
    for link in "$INSTALL_DIR/commands"/*.md; do
        if [ -L "$link" ]; then
            local target=$(readlink "$link")
            if [[ "$target" == "require-kit/"* ]]; then
                symlink_count=$((symlink_count + 1))
            fi
        fi
    done

    if [ "$symlink_count" -gt 0 ]; then
        print_pass "Found $symlink_count command symlinks"
    else
        print_info "No command symlinks created (may be expected if no commands exist)"
    fi
}

test_marker_file() {
    print_test "Verifying marker file..."

    if [ -f "$INSTALL_DIR/require-kit.marker" ]; then
        print_pass "Marker file exists: require-kit.marker"

        # Verify JSON content
        if python3 -m json.tool "$INSTALL_DIR/require-kit.marker" > /dev/null 2>&1; then
            print_pass "Marker file is valid JSON"

            # Check required fields
            local name=$(python3 -c "import json; print(json.load(open('$INSTALL_DIR/require-kit.marker'))['name'])" 2>/dev/null)
            if [ "$name" = "require-kit" ]; then
                print_pass "Marker file has correct package name"
            else
                print_fail "Marker file has incorrect package name: $name"
            fi
        else
            print_fail "Marker file is not valid JSON"
        fi
    else
        print_fail "Marker file missing"
    fi
}

test_feature_detection() {
    print_test "Verifying feature_detection.py..."

    if [ -f "$INSTALL_DIR/lib/feature_detection.py" ]; then
        print_pass "feature_detection.py installed"

        # Test Python import
        if python3 -c "import sys; sys.path.insert(0, '$INSTALL_DIR'); from lib.feature_detection import is_require_kit_installed" 2>/dev/null; then
            print_pass "feature_detection.py is importable"
        else
            print_fail "feature_detection.py has import errors"
        fi
    else
        print_fail "feature_detection.py missing"
    fi
}

test_version_tracking() {
    print_test "Verifying version tracking..."

    if [ -f "$INSTALL_DIR/.installed/require-kit.version" ]; then
        local version=$(cat "$INSTALL_DIR/.installed/require-kit.version")
        print_pass "Version file exists: $version"
    else
        print_fail "Version file missing"
    fi

    if [ -f "$INSTALL_DIR/.installed/require-kit.timestamp" ]; then
        local timestamp=$(cat "$INSTALL_DIR/.installed/require-kit.timestamp")
        print_pass "Timestamp file exists: $timestamp"
    else
        print_fail "Timestamp file missing"
    fi
}

test_uninstallation() {
    print_test "Testing uninstallation..."

    cd "$(dirname "${BASH_SOURCE[0]}")/.."

    if bash scripts/uninstall-require-kit.sh > /dev/null 2>&1; then
        print_pass "Uninstallation completed successfully"

        # Verify clean removal
        if [ ! -d "$INSTALL_DIR/commands/require-kit" ]; then
            print_pass "Commands directory removed"
        else
            print_fail "Commands directory still exists"
        fi

        if [ ! -d "$INSTALL_DIR/agents/require-kit" ]; then
            print_pass "Agents directory removed"
        else
            print_fail "Agents directory still exists"
        fi

        if [ ! -f "$INSTALL_DIR/require-kit.marker" ]; then
            print_pass "Marker file removed"
        else
            print_fail "Marker file still exists"
        fi
    else
        print_fail "Uninstallation failed"
    fi
}

cleanup() {
    print_test "Cleaning up test environment..."
    rm -rf "$TEST_DIR"
    print_pass "Test directory removed"
}

print_summary() {
    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
    if [ $FAILED -eq 0 ]; then
        echo -e "${GREEN}✅ All tests passed!${NC}"
        echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
        return 0
    else
        echo -e "${RED}❌ Some tests failed${NC}"
        echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
        return 1
    fi
}

main() {
    print_header

    setup_test
    test_installation
    test_directory_structure
    test_commands_installed
    test_agents_installed
    test_symlinks
    test_marker_file
    test_feature_detection
    test_version_tracking
    test_uninstallation

    cleanup
    print_summary
}

main "$@"
