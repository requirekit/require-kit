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

# Python version requirements
REQUIRED_PYTHON_VERSION="3.10"

check_python_version() {
    print_info "Checking Python version..."

    local min_major=3
    local min_minor=10

    # Check if python3 is available
    if ! command -v python3 &> /dev/null; then
        echo ""
        print_error "════════════════════════════════════════════════════════"
        print_error "Python 3 not found"
        print_error "════════════════════════════════════════════════════════"
        echo ""
        print_info "Please install Python 3.10 or higher:"
        echo ""

        # Detect OS and provide specific installation instructions
        local os_type=$(uname -s)
        print_info "Installation instructions:"
        echo ""

        case "$os_type" in
            Darwin)
                print_info "macOS - Choose one of the following methods:"
                echo ""
                print_info "1. Homebrew (recommended):"
                print_info "   brew install python@3.13"
                echo ""
                print_info "2. Official installer:"
                print_info "   Download from: https://www.python.org/downloads/"
                print_info "   Select macOS installer for Python 3.13"
                echo ""
                print_info "3. pyenv (for multiple Python versions):"
                print_info "   brew install pyenv"
                print_info "   pyenv install 3.13.0"
                print_info "   pyenv global 3.13.0"
                ;;
            Linux)
                # Detect Linux distribution
                if [ -f /etc/os-release ]; then
                    . /etc/os-release
                    case "$ID" in
                        ubuntu|debian)
                            print_info "Ubuntu/Debian:"
                            print_info "   sudo apt update"
                            print_info "   sudo apt install python3.13 python3.13-venv python3.13-pip"
                            echo ""
                            print_info "If Python 3.13 is not available, add deadsnakes PPA:"
                            print_info "   sudo add-apt-repository ppa:deadsnakes/ppa"
                            print_info "   sudo apt update"
                            print_info "   sudo apt install python3.13 python3.13-venv python3.13-pip"
                            ;;
                        fedora|rhel|centos)
                            print_info "Fedora/RHEL/CentOS:"
                            print_info "   sudo dnf install python3.13"
                            echo ""
                            print_info "Or build from source:"
                            print_info "   https://www.python.org/downloads/"
                            ;;
                        arch)
                            print_info "Arch Linux:"
                            print_info "   sudo pacman -S python"
                            ;;
                        *)
                            print_info "Linux (generic):"
                            print_info "   Download from: https://www.python.org/downloads/"
                            print_info "   Or use your distribution's package manager"
                            ;;
                    esac
                else
                    print_info "Linux (generic):"
                    print_info "   Download from: https://www.python.org/downloads/"
                    print_info "   Or use your distribution's package manager"
                fi
                echo ""
                print_info "Alternative - pyenv (for multiple Python versions):"
                print_info "   curl https://pyenv.run | bash"
                print_info "   pyenv install 3.13.0"
                print_info "   pyenv global 3.13.0"
                ;;
            MINGW*|MSYS*|CYGWIN*)
                print_info "Windows (Git Bash/MSYS2/Cygwin):"
                echo ""
                print_info "1. Official installer (recommended):"
                print_info "   Download from: https://www.python.org/downloads/"
                print_info "   Select Windows installer for Python 3.13"
                print_info "   ⚠ Check 'Add Python to PATH' during installation"
                echo ""
                print_info "2. Windows Package Manager (winget):"
                print_info "   winget install Python.Python.3.13"
                echo ""
                print_info "3. Chocolatey:"
                print_info "   choco install python --version=3.13.0"
                ;;
            *)
                print_info "Generic installation:"
                print_info "   Download from: https://www.python.org/downloads/"
                ;;
        esac

        echo ""
        print_info "After installation, verify with:"
        print_info "   python3 --version"
        echo ""
        print_error "════════════════════════════════════════════════════════"
        exit 1
    fi

    # Get Python version
    local python_version=$(python3 --version 2>&1 | awk '{print $2}')
    local python_major=$(echo "$python_version" | cut -d. -f1)
    local python_minor=$(echo "$python_version" | cut -d. -f2)

    # Check version meets minimum requirement
    if ! python3 -c "import sys; exit(0 if sys.version_info >= ($min_major, $min_minor) else 1)" 2>/dev/null; then
        echo ""
        print_error "════════════════════════════════════════════════════════"
        print_error "Python 3.10+ required"
        print_error "════════════════════════════════════════════════════════"
        echo ""
        print_info "Current version: Python $python_version"
        print_info "Minimum required: Python 3.10.0"
        print_info "Recommended version: Python 3.13"
        echo ""
        print_warning "Why Python 3.10+?"
        print_info "  require-kit uses modern type hints (PEP 604) for better"
        print_info "  code quality and IDE support, aligning with taskwright."
        print_info "  Python 3.10 has been available since October 2021."
        echo ""

        # Detect OS and provide specific installation instructions
        local os_type=$(uname -s)
        print_info "Installation instructions:"
        echo ""

        case "$os_type" in
            Darwin)
                print_info "macOS - Choose one of the following methods:"
                echo ""
                print_info "1. Homebrew (recommended):"
                print_info "   brew install python@3.13"
                echo ""
                print_info "2. Official installer:"
                print_info "   Download from: https://www.python.org/downloads/"
                print_info "   Select macOS installer for Python 3.13"
                echo ""
                print_info "3. pyenv (for multiple Python versions):"
                print_info "   brew install pyenv"
                print_info "   pyenv install 3.13.0"
                print_info "   pyenv global 3.13.0"
                ;;
            Linux)
                # Detect Linux distribution
                if [ -f /etc/os-release ]; then
                    . /etc/os-release
                    case "$ID" in
                        ubuntu|debian)
                            print_info "Ubuntu/Debian:"
                            print_info "   sudo apt update"
                            print_info "   sudo apt install python3.13 python3.13-venv python3.13-pip"
                            echo ""
                            print_info "If Python 3.13 is not available, add deadsnakes PPA:"
                            print_info "   sudo add-apt-repository ppa:deadsnakes/ppa"
                            print_info "   sudo apt update"
                            print_info "   sudo apt install python3.13 python3.13-venv python3.13-pip"
                            ;;
                        fedora|rhel|centos)
                            print_info "Fedora/RHEL/CentOS:"
                            print_info "   sudo dnf install python3.13"
                            echo ""
                            print_info "Or build from source:"
                            print_info "   https://www.python.org/downloads/"
                            ;;
                        arch)
                            print_info "Arch Linux:"
                            print_info "   sudo pacman -S python"
                            ;;
                        *)
                            print_info "Linux (generic):"
                            print_info "   Download from: https://www.python.org/downloads/"
                            print_info "   Or use your distribution's package manager"
                            ;;
                    esac
                else
                    print_info "Linux (generic):"
                    print_info "   Download from: https://www.python.org/downloads/"
                    print_info "   Or use your distribution's package manager"
                fi
                echo ""
                print_info "Alternative - pyenv (for multiple Python versions):"
                print_info "   curl https://pyenv.run | bash"
                print_info "   pyenv install 3.13.0"
                print_info "   pyenv global 3.13.0"
                ;;
            MINGW*|MSYS*|CYGWIN*)
                print_info "Windows (Git Bash/MSYS2/Cygwin):"
                echo ""
                print_info "1. Official installer (recommended):"
                print_info "   Download from: https://www.python.org/downloads/"
                print_info "   Select Windows installer for Python 3.13"
                print_info "   ⚠ Check 'Add Python to PATH' during installation"
                echo ""
                print_info "2. Windows Package Manager (winget):"
                print_info "   winget install Python.Python.3.13"
                echo ""
                print_info "3. Chocolatey:"
                print_info "   choco install python --version=3.13.0"
                ;;
            *)
                print_info "Generic installation:"
                print_info "   Download from: https://www.python.org/downloads/"
                ;;
        esac

        echo ""
        print_info "After installation, verify with:"
        print_info "   python3 --version"
        echo ""
        print_info "Need help?"
        print_info "  https://github.com/requirekit/require-kit/issues"
        echo ""
        print_error "════════════════════════════════════════════════════════"
        exit 1
    fi

    print_success "Python version $python_version meets requirements"
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

    # Copy entire lib directory structure (preserves relative imports)
    if [ -d "$SCRIPT_DIR/global/lib" ]; then
        # Use cp -r to recursively copy entire lib structure
        cp -r "$SCRIPT_DIR/global/lib/"* "$INSTALL_DIR/lib/" 2>/dev/null || true

        # Count Python files installed
        local py_count=$(find "$INSTALL_DIR/lib" -name "*.py" -type f 2>/dev/null | wc -l)
        if [ "$py_count" -gt 0 ]; then
            print_success "Library files installed ($py_count Python modules)"
        else
            print_warning "No Python files found in $INSTALL_DIR/lib"
        fi
    else
        print_warning "lib directory not found at $SCRIPT_DIR/global/lib"
    fi
}

# Get the marker file path (helper function for DRY principle)
get_marker_path() {
    echo "$INSTALL_DIR/$PACKAGE_NAME.marker.json"
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
    local marker_file=$(get_marker_path)
    local python_version=$(python3 --version 2>&1 | awk '{print $2}')

    # Create marker file with metadata (JSON format to match taskwright)
    if ! cat > "$marker_file" <<EOF
{
  "package": "$PACKAGE_NAME",
  "version": "$PACKAGE_VERSION",
  "installed": "$install_date",
  "install_location": "$INSTALL_DIR",
  "repo_path": "$repo_root",
  "python_version": ">=3.10",
  "python_detected": "$python_version",
  "python_alignment": "taskwright_ecosystem",
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
    then
        print_error "Failed to create marker file at $marker_file"
        return 1
    fi

    # Verify marker file was created successfully and is non-empty
    if [ ! -f "$marker_file" ] || [ ! -s "$marker_file" ]; then
        print_error "Marker file creation verification failed"
        return 1
    fi

    print_success "Marker file created at $marker_file"
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
    local marker_file=$(get_marker_path)

    echo "  Commands installed: $cmd_count"
    echo "  Agents installed: $agent_count"

    if [ "$cmd_count" -eq 0 ]; then
        print_error "No commands installed"
    fi

    if [ "$agent_count" -eq 0 ]; then
        print_error "No agents installed"
    fi

    # Verify marker file exists and is non-empty (fail fast)
    if [ ! -f "$marker_file" ] || [ ! -s "$marker_file" ]; then
        print_error "Marker file not created"
    fi

    # Verify feature_detection.py exists
    if [ ! -f "$INSTALL_DIR/lib/feature_detection.py" ]; then
        print_warning "feature_detection.py not found (some integration features may not work)"
    fi

    print_success "Installation verified"
}

validate_installation() {
    print_info "Validating installation..."

    # Check if Python 3 is available
    if ! command -v python3 &> /dev/null; then
        print_warning "Python 3 not found - skipping Python validation"
        return 0
    fi

    # Test Python import of feature_detection module
    if ! python3 <<EOF
import sys
import os

# Change to installed directory
os.chdir(os.path.expanduser("$INSTALL_DIR"))

try:
    from lib.feature_detection import is_require_kit_installed
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

check_integration_opportunities() {
    print_info "Checking for integration opportunities..."

    # Check if taskwright is installed (optional integration)
    # Support both legacy .marker and new .marker.json formats
    if [ ! -f "$INSTALL_DIR/taskwright.marker" ] && [ ! -f "$INSTALL_DIR/taskwright.marker.json" ]; then
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
    check_python_version
    ensure_repository_files
    check_prerequisites
    create_directory_structure
    install_commands
    install_agents
    install_lib
    create_marker_file
    track_installation
    verify_installation
    validate_installation
    check_integration_opportunities
    print_completion_message
}

main "$@"
