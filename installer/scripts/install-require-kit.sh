#!/bin/bash
# require-kit Installation Script
# Installs require-kit to namespaced directories for coexistence with taskwright

set -e

INSTALL_DIR="$HOME/.agentecflow"
PACKAGE_NAME="require-kit"
PACKAGE_VERSION="1.0.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║         require-kit Installation                       ║${NC}"
    echo -e "${BLUE}║         Version: $PACKAGE_VERSION                      ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
    exit 1
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

check_prerequisites() {
    print_info "Checking prerequisites..."

    # Check for required commands
    for cmd in git bash; do
        if ! command -v $cmd &> /dev/null; then
            print_error "Required command '$cmd' not found"
        fi
    done

    # Check for Python 3 (optional but recommended for some commands)
    if ! command -v python3 &> /dev/null; then
        print_warning "Python 3 not found. Some advanced features may be limited."
    else
        print_success "Python 3 found: $(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)"
    fi

    print_success "Prerequisites check passed"
}

create_directory_structure() {
    print_info "Creating directory structure..."

    mkdir -p "$INSTALL_DIR/commands/$PACKAGE_NAME"
    mkdir -p "$INSTALL_DIR/agents/$PACKAGE_NAME"
    mkdir -p "$INSTALL_DIR/lib"
    mkdir -p "$INSTALL_DIR/.installed"

    print_success "Directory structure created"
}

install_commands() {
    print_info "Installing commands..."

    # Copy commands to namespaced directory
    local cmd_count=0
    if [ -d "$SCRIPT_DIR/global/commands" ]; then
        for cmd_file in "$SCRIPT_DIR/global/commands"/*.md; do
            if [ -f "$cmd_file" ]; then
                cp "$cmd_file" "$INSTALL_DIR/commands/$PACKAGE_NAME/" 2>/dev/null || true
                cmd_count=$((cmd_count + 1))
            fi
        done
    fi

    # Create symlinks for backwards compatibility
    for cmd in "$INSTALL_DIR/commands/$PACKAGE_NAME"/*.md; do
        if [ -f "$cmd" ]; then
            cmd_name=$(basename "$cmd")

            # Only create symlink if it doesn't exist or points to require-kit
            if [ ! -e "$INSTALL_DIR/commands/$cmd_name" ] || \
               [ "$(readlink "$INSTALL_DIR/commands/$cmd_name" 2>/dev/null)" = "$PACKAGE_NAME/$cmd_name" ]; then
                ln -sf "$PACKAGE_NAME/$cmd_name" "$INSTALL_DIR/commands/$cmd_name"
            fi
        fi
    done

    print_success "Commands installed ($cmd_count commands)"
}

install_agents() {
    print_info "Installing agents..."

    # Copy agents to namespaced directory
    local agent_count=0
    if [ -d "$SCRIPT_DIR/global/agents" ]; then
        for agent_file in "$SCRIPT_DIR/global/agents"/*.md; do
            if [ -f "$agent_file" ]; then
                cp "$agent_file" "$INSTALL_DIR/agents/$PACKAGE_NAME/" 2>/dev/null || true
                agent_count=$((agent_count + 1))
            fi
        done
    fi

    # Create symlinks for backwards compatibility
    for agent in "$INSTALL_DIR/agents/$PACKAGE_NAME"/*.md; do
        if [ -f "$agent" ]; then
            agent_name=$(basename "$agent")

            if [ ! -e "$INSTALL_DIR/agents/$agent_name" ] || \
               [ "$(readlink "$INSTALL_DIR/agents/$agent_name" 2>/dev/null)" = "$PACKAGE_NAME/$agent_name" ]; then
                ln -sf "$PACKAGE_NAME/$agent_name" "$INSTALL_DIR/agents/$agent_name"
            fi
        fi
    done

    print_success "Agents installed ($agent_count agents)"
}

install_lib() {
    print_info "Installing library files..."

    # Copy feature_detection.py (shared with taskwright)
    if [ -f "$SCRIPT_DIR/global/lib/feature_detection.py" ]; then
        cp "$SCRIPT_DIR/global/lib/feature_detection.py" "$INSTALL_DIR/lib/" 2>/dev/null || true
        print_success "Library files installed (feature_detection.py)"
    else
        print_warning "feature_detection.py not found at $SCRIPT_DIR/global/lib/feature_detection.py"
    fi
}

create_marker_file() {
    print_info "Creating package marker..."

    # Create marker file with metadata
    cat > "$INSTALL_DIR/$PACKAGE_NAME.marker" <<EOF
{
  "name": "$PACKAGE_NAME",
  "version": "$PACKAGE_VERSION",
  "installed_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "install_dir": "$INSTALL_DIR",
  "capabilities": [
    "requirements-engineering",
    "ears-notation",
    "bdd-generation",
    "epic-feature-hierarchy",
    "requirements-traceability"
  ]
}
EOF

    print_success "Marker file created at $INSTALL_DIR/$PACKAGE_NAME.marker"
}

track_installation() {
    echo "$PACKAGE_VERSION" > "$INSTALL_DIR/.installed/$PACKAGE_NAME.version"
    date +%s > "$INSTALL_DIR/.installed/$PACKAGE_NAME.timestamp"
    print_success "Installation tracked"
}

verify_installation() {
    print_info "Verifying installation..."

    local cmd_count=$(ls -1 "$INSTALL_DIR/commands/$PACKAGE_NAME"/*.md 2>/dev/null | wc -l)
    local agent_count=$(ls -1 "$INSTALL_DIR/agents/$PACKAGE_NAME"/*.md 2>/dev/null | wc -l)

    echo "  Commands installed: $cmd_count"
    echo "  Agents installed: $agent_count"

    if [ "$cmd_count" -eq 0 ]; then
        print_error "No commands installed"
    fi

    if [ "$agent_count" -eq 0 ]; then
        print_error "No agents installed"
    fi

    # Verify marker file exists
    if [ ! -f "$INSTALL_DIR/$PACKAGE_NAME.marker" ]; then
        print_error "Marker file not created"
    fi

    # Verify feature_detection.py exists
    if [ ! -f "$INSTALL_DIR/lib/feature_detection.py" ]; then
        print_warning "feature_detection.py not found (some integration features may not work)"
    fi

    print_success "Installation verified"
}

check_integration_opportunities() {
    print_info "Checking for integration opportunities..."

    # Check if taskwright is installed (optional integration)
    if [ ! -f "$INSTALL_DIR/taskwright.marker" ]; then
        echo ""
        echo -e "${YELLOW}  ℹ️  taskwright not detected${NC}"
        echo "  require-kit works standalone for requirements management"
        echo ""
        echo "  For full integration (link requirements to tasks):"
        echo "  Install taskwright from: https://github.com/taskwright-dev/taskwright"
    else
        echo ""
        print_success "taskwright detected - full integration available"
        echo "  Commands can now link requirements to tasks"
        echo "  Use /task-work --mode=bdd for BDD-driven development"
    fi
}

print_completion_message() {
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║         Installation Complete!                          ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "require-kit has been installed to ~/.agentecflow"
    echo ""
    echo "Available commands (use in Claude Code):"
    echo "  /gather-requirements - Interactive requirements gathering"
    echo "  /formalize-ears      - Convert to EARS notation"
    echo "  /generate-bdd        - Generate BDD scenarios"
    echo "  /epic-create         - Create epic"
    echo "  /feature-create      - Create feature"
    echo "  /hierarchy-view      - View epic/feature hierarchy"
    echo ""
    echo "For project setup, run:"
    echo "  cd your-project"
    echo "  require-kit init"
    echo ""
    echo "Check installation:"
    echo "  require-kit doctor"
    echo ""
}

# Main installation flow
main() {
    print_header
    check_prerequisites
    create_directory_structure
    install_commands
    install_agents
    install_lib
    create_marker_file
    track_installation
    verify_installation
    check_integration_opportunities
    print_completion_message
}

main "$@"
