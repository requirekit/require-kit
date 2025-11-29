#!/bin/bash
# require-kit Installation Script
# Installs require-kit to namespaced directories for coexistence with taskwright

set -e

INSTALL_DIR="$HOME/.agentecflow"
PACKAGE_NAME="require-kit"
PACKAGE_VERSION="1.0.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GITHUB_REPO="https://github.com/requirekit/require-kit"
GITHUB_BRANCH="main"

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

# Download repository if running via curl (files not available locally)
ensure_repository_files() {
    # Check if we have the required files
    if [ ! -f "$SCRIPT_DIR/scripts/install.sh" ] || [ ! -d "$SCRIPT_DIR/global/commands" ]; then
        print_info "Running from curl - cloning repository permanently..."

        # Determine permanent location for repository
        # Use ~/Projects/require-kit or ~/require-kit if ~/Projects doesn't exist
        local REPO_DEST
        if [ -d "$HOME/Projects" ]; then
            REPO_DEST="$HOME/Projects/require-kit"
        else
            REPO_DEST="$HOME/require-kit"
        fi

        # Check if git is available for cloning
        if command -v git &> /dev/null; then
            # Git available - clone repository
            print_info "Cloning repository to $REPO_DEST..."

            # Remove existing directory if present
            if [ -d "$REPO_DEST" ]; then
                print_warning "Repository already exists at $REPO_DEST"
                print_info "Updating existing repository..."
                cd "$REPO_DEST" && git pull
            else
                # Clone fresh
                if ! git clone "$GITHUB_REPO" "$REPO_DEST"; then
                    print_error "Failed to clone repository"
                    print_info "Try cloning manually: git clone $GITHUB_REPO $REPO_DEST"
                    exit 1
                fi
            fi

            # Update SCRIPT_DIR to point to cloned repo
            SCRIPT_DIR="$REPO_DEST/installer"
            print_success "Repository cloned to $REPO_DEST"
        else
            # Git not available - fall back to tarball download (PERMANENT location)
            print_warning "git not found - downloading tarball instead"
            print_info "Installing git is recommended for easier updates"

            # Create permanent directory
            mkdir -p "$REPO_DEST"

            # Download and extract
            print_info "Downloading from $GITHUB_REPO to $REPO_DEST..."
            if ! curl -sSL "$GITHUB_REPO/archive/refs/heads/$GITHUB_BRANCH.tar.gz" | tar -xz -C "$REPO_DEST" --strip-components=1; then
                print_error "Failed to download repository"
                print_info "Try installing git and cloning: git clone $GITHUB_REPO $REPO_DEST"
                exit 1
            fi

            # Update SCRIPT_DIR to point to downloaded repo
            SCRIPT_DIR="$REPO_DEST/installer"
            print_success "Repository downloaded to $REPO_DEST"
        fi

        if [ ! -d "$SCRIPT_DIR" ]; then
            print_error "Downloaded repository structure not as expected"
            exit 1
        fi
    fi
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

    # Determine repository root (parent of installer/)
    # SCRIPT_DIR points to installer/ directory
    local repo_root
    if [ -d "$SCRIPT_DIR" ]; then
        repo_root="$(cd "$SCRIPT_DIR/.." && pwd)"
    else
        repo_root="$PWD"  # Fallback to current directory
    fi

    local install_date=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    # Create marker file with metadata (JSON format to match taskwright)
    cat > "$INSTALL_DIR/$PACKAGE_NAME.marker.json" <<EOF
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
    "taskwright"
  ],
  "integration_model": "bidirectional_optional",
  "description": "Requirements engineering and BDD for Agentecflow",
  "homepage": "https://github.com/requirekit/require-kit"
}
EOF

    print_success "Marker file created at $INSTALL_DIR/$PACKAGE_NAME.marker.json"
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

    # Verify marker file exists (JSON format)
    if [ ! -f "$INSTALL_DIR/$PACKAGE_NAME.marker.json" ]; then
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
    echo "For project setup, create the documentation structure:"
    echo "  cd your-project"
    echo "  mkdir -p docs/{epics,features,requirements,bdd}"
    echo ""
    echo "Then use require-kit commands in Claude Code to start gathering requirements."
    echo ""
}

# Main installation flow
main() {
    print_header
    ensure_repository_files
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
