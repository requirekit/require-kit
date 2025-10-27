#!/bin/bash

# Quick Installation Test for Current Environment
# Perfect for testing on your macOS with zsh setup

set -e

# Configuration
TEST_DIR="$HOME/agentic-flow-quick-test-$(date +%s)"
INSTALLER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() { echo -e "${GREEN}✓ $1${NC}"; }
print_error() { echo -e "${RED}✗ $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠ $1${NC}"; }

echo ""
echo "🧪 Quick Installation Test for Agentic Flow"
echo "=============================================="
echo ""

# Create isolated test environment
print_info "Creating test environment: $TEST_DIR"
mkdir -p "$TEST_DIR"

# Set fake home for isolation
export HOME="$TEST_DIR"

print_info "Testing installation in isolated environment..."

# Run the installer
if bash "$INSTALLER_DIR/scripts/install.sh"; then
    print_success "Installation completed successfully!"
else
    print_error "Installation failed!"
    rm -rf "$TEST_DIR"
    exit 1
fi

# Verify installation
print_info "Verifying installation..."

AGENTICFLOW_HOME="$TEST_DIR/.agenticflow"

# Check directory structure
if [ -d "$AGENTICFLOW_HOME" ]; then
    print_success "Agentic Flow home directory created"
else
    print_error "Agentic Flow home directory missing"
    rm -rf "$TEST_DIR"
    exit 1
fi

# Check key components
components=(
    "agents:AI agents"
    "bin:CLI commands"
    "commands:Command definitions"
    "templates:Project templates"
    "docs:Documentation"
)

for component in "${components[@]}"; do
    dir="${component%%:*}"
    desc="${component##*:}"

    if [ -d "$AGENTICFLOW_HOME/$dir" ]; then
        count=$(ls -1 "$AGENTICFLOW_HOME/$dir" 2>/dev/null | wc -l)
        print_success "$desc: $count items"
    else
        print_error "$desc directory missing"
    fi
done

# Test CLI commands
print_info "Testing CLI commands..."

if [ -f "$AGENTICFLOW_HOME/bin/agenticflow" ] && [ -x "$AGENTICFLOW_HOME/bin/agenticflow" ]; then
    print_success "CLI commands are executable"
else
    print_error "CLI commands not found or not executable"
fi

# Test project initialization
print_info "Testing project initialization..."

PROJECT_DIR="$TEST_DIR/test-project"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

export CLAUDE_HOME="$AGENTICFLOW_HOME"

if bash "$AGENTICFLOW_HOME/scripts/init-project.sh" "react"; then
    print_success "React template initialization succeeded"

    # Check project structure
    if [ -d ".claude" ] && [ -d "docs" ] && [ -d "tasks" ]; then
        print_success "Project structure created correctly"
    else
        print_error "Project structure incomplete"
    fi
else
    print_error "React template initialization failed"
fi

# Test shell integration
print_info "Testing shell integration..."

if [ -f "$TEST_DIR/.zshrc" ]; then
    if grep -q "agenticflow" "$TEST_DIR/.zshrc"; then
        print_success "Zsh integration added to .zshrc"
    else
        print_warning "Zsh integration not found in .zshrc"
    fi
elif [ -f "$TEST_DIR/.bashrc" ]; then
    if grep -q "agenticflow" "$TEST_DIR/.bashrc"; then
        print_success "Bash integration added to .bashrc"
    else
        print_warning "Bash integration not found in .bashrc"
    fi
else
    print_warning "No shell configuration file was modified"
fi

echo ""
echo "📊 Test Summary"
echo "==============="

if [ -d "$AGENTICFLOW_HOME" ] && [ -x "$AGENTICFLOW_HOME/bin/agenticflow" ]; then
    print_success "✅ Installation test PASSED"
    echo ""
    echo "🎉 Ready to install! The installation scripts work correctly in your environment."
    echo ""
    echo "To install Agentic Flow for real:"
    echo "1. Run: bash installer/scripts/install.sh"
    echo "2. Restart your terminal or run: source ~/.zshrc"
    echo "3. Test with: agentecflow doctor"
    echo "4. Initialize a project: agentecflow init react"
else
    print_error "❌ Installation test FAILED"
    echo ""
    echo "There are issues with the installation scripts."
    echo "Please review the errors above and fix before installing."
fi

# Cleanup
print_info "Cleaning up test environment..."
rm -rf "$TEST_DIR"

echo ""
echo "Test completed!"