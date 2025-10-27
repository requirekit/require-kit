#!/bin/bash

# Claude Global Installation Script
# Installs the Claude/Agentic Flow system to ~/.claude

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Installation configuration
CLAUDE_VERSION="1.0.0"
INSTALL_DIR="$HOME/.claude"
CONFIG_DIR="$HOME/.config/claude"
INSTALLER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

print_header() {
    echo ""
    print_message "$BLUE" "╔════════════════════════════════════════════════════════╗"
    print_message "$BLUE" "║         Claude Global Installation                     ║"
    print_message "$BLUE" "║         Agentic Flow Methodology v$CLAUDE_VERSION      ║"
    print_message "$BLUE" "╚════════════════════════════════════════════════════════╝"
    echo ""
}

print_message() {
    local color=$1
    shift
    echo -e "${color}$@${NC}"
}

print_success() {
    print_message "$GREEN" "✓ $1"
}

print_error() {
    print_message "$RED" "✗ $1"
}

print_warning() {
    print_message "$YELLOW" "⚠ $1"
}

print_info() {
    print_message "$BLUE" "ℹ $1"
}

# Check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."
    
    local missing_deps=()
    
    for cmd in git curl bash; do
        if ! command -v $cmd &> /dev/null; then
            missing_deps+=($cmd)
        fi
    done
    
    if [ ${#missing_deps[@]} -gt 0 ]; then
        print_error "Missing required dependencies: ${missing_deps[*]}"
        exit 1
    fi
    
    print_success "All prerequisites met"
}

# Backup existing installation
backup_existing() {
    if [ -d "$INSTALL_DIR/instructions" ] || [ -d "$INSTALL_DIR/templates" ]; then
        local backup_dir="${INSTALL_DIR}.backup.$(date +%Y%m%d_%H%M%S)"
        print_warning "Existing Claude global installation found"
        print_info "Creating backup at $backup_dir"
        
        mkdir -p "$backup_dir"
        [ -d "$INSTALL_DIR/instructions" ] && cp -r "$INSTALL_DIR/instructions" "$backup_dir/"
        [ -d "$INSTALL_DIR/templates" ] && cp -r "$INSTALL_DIR/templates" "$backup_dir/"
        [ -d "$INSTALL_DIR/commands" ] && cp -r "$INSTALL_DIR/commands" "$backup_dir/"
        
        print_success "Backup created"
    fi
}

# Create directory structure
create_directories() {
    print_info "Creating Claude global directory structure..."
    
    # Create main directories
    mkdir -p "$INSTALL_DIR"/{instructions/core,templates,commands,scripts}
    mkdir -p "$CONFIG_DIR"
    
    print_success "Directory structure created"
}

# Install global files
install_global_files() {
    print_info "Installing global methodology and templates..."
    
    # Copy instructions
    if [ -d "$INSTALLER_DIR/global/instructions" ]; then
        cp -r "$INSTALLER_DIR/global/instructions/"* "$INSTALL_DIR/instructions/" 2>/dev/null || true
        print_success "Installed methodology instructions"
    fi
    
    # Copy ALL templates including maui-appshell, maui-navigationpage and dotnet-microservice
    if [ -d "$INSTALLER_DIR/global/templates" ]; then
        cp -r "$INSTALLER_DIR/global/templates/"* "$INSTALL_DIR/templates/" 2>/dev/null || true
        print_success "Installed project templates"
    fi
    
    # Copy commands
    if [ -d "$INSTALLER_DIR/global/commands" ]; then
        cp -r "$INSTALLER_DIR/global/commands/"* "$INSTALL_DIR/commands/" 2>/dev/null || true
        print_success "Installed Claude commands"
    fi
    
    # Copy the correct initialization script (init-claude-project.sh)
    cp "$INSTALLER_DIR/scripts/init-claude-project.sh" "$INSTALL_DIR/scripts/claude-init"
    chmod +x "$INSTALL_DIR/scripts/claude-init"
    print_success "Installed project initialization script"
}

# Create the main agentic command
create_agentic_command() {
    print_info "Creating agentic-init command..."
    
    # Create bin directory if it doesn't exist
    mkdir -p "$HOME/.local/bin"
    
    cat > "$HOME/.local/bin/agentic-init" << 'EOF'
#!/bin/bash

# Agentic Flow Project Initialization
# Run this in any project directory to set up Claude/Agentic Flow

CLAUDE_HOME="$HOME/.claude"
PROJECT_DIR="$(pwd)"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_help() {
    echo "Agentic Flow Project Initialization"
    echo ""
    echo "Usage: agentic-init [template]"
    echo ""
    echo "Templates:"
    echo "  default    - Language-agnostic template"
    echo "  react      - React with TypeScript"
    echo "  python     - Python with FastAPI"
    echo "  maui-appshell       - .NET MAUI mobile app with AppShell navigation"
    echo "  maui-navigationpage - .NET MAUI mobile app with NavigationPage stack"
    echo "  dotnet-microservice - .NET microservice with FastEndpoints"
    echo "  fullstack  - React + Python"
    echo ""
    echo "Examples:"
    echo "  agentic-init                  # Interactive setup"
    echo "  agentic-init react            # Initialize with React template"
    echo "  agentic-init maui-appshell    # Initialize with .NET MAUI AppShell template"
}

if [ "$1" = "help" ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    print_help
    exit 0
fi

# Check if Claude is installed globally
if [ ! -d "$CLAUDE_HOME" ]; then
    echo -e "${RED}Error: Claude global installation not found at $CLAUDE_HOME${NC}"
    echo "Please run the global installer first:"
    echo "  curl -sSL https://raw.githubusercontent.com/appmilla/agentic-flow/main/installer/scripts/install-global.sh | bash"
    exit 1
fi

# Run the initialization script
if [ -f "$CLAUDE_HOME/scripts/claude-init" ]; then
    exec "$CLAUDE_HOME/scripts/claude-init" "$@"
else
    echo -e "${RED}Error: Initialization script not found${NC}"
    exit 1
fi
EOF
    
    chmod +x "$HOME/.local/bin/agentic-init"
    print_success "Created agentic-init command"
}

# Setup shell integration
setup_shell_integration() {
    print_info "Setting up shell integration..."
    
    local shell_config=""
    
    # Detect shell
    if [ -n "$BASH_VERSION" ]; then
        if [ -f "$HOME/.bashrc" ]; then
            shell_config="$HOME/.bashrc"
        elif [ -f "$HOME/.bash_profile" ]; then
            shell_config="$HOME/.bash_profile"
        fi
    elif [ -n "$ZSH_VERSION" ]; then
        shell_config="$HOME/.zshrc"
    fi
    
    if [ -z "$shell_config" ]; then
        print_warning "Could not detect shell configuration file"
        print_info "Please add the following to your shell configuration manually:"
        echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
        echo "    export CLAUDE_HOME=\"\$HOME/.claude\""
        return
    fi
    
    # Check if already configured
    if grep -q "CLAUDE_HOME" "$shell_config" 2>/dev/null; then
        print_info "Shell integration already configured"
        return
    fi
    
    # Add to shell configuration
    cat >> "$shell_config" << 'EOF'

# Claude/Agentic Flow
export PATH="$HOME/.local/bin:$PATH"
export CLAUDE_HOME="$HOME/.claude"
EOF
    
    print_success "Shell integration added to $shell_config"
}

# Create global configuration
create_global_config() {
    print_info "Creating global configuration..."
    
    cat > "$CONFIG_DIR/config.json" << 'EOF'
{
  "version": "1.0.0",
  "methodology": "agentic-flow",
  "defaults": {
    "template": "default",
    "testing": {
      "coverage_threshold": 80,
      "quality_gates": true
    },
    "requirements": {
      "format": "EARS",
      "validation": true
    }
  }
}
EOF
    
    print_success "Global configuration created"
}

# Create version file
create_version_file() {
    echo "$CLAUDE_VERSION" > "$INSTALL_DIR/version"
    print_success "Version file created"
}

# List available templates
list_templates() {
    print_info "Detecting available templates..."
    
    local templates=()
    
    if [ -d "$INSTALLER_DIR/global/templates" ]; then
        for template_dir in "$INSTALLER_DIR/global/templates"/*/; do
            if [ -d "$template_dir" ]; then
                template_name=$(basename "$template_dir")
                templates+=("$template_name")
            fi
        done
    fi
    
    if [ ${#templates[@]} -gt 0 ]; then
        print_success "Found ${#templates[@]} templates"
        for template in "${templates[@]}"; do
            case "$template" in
                default)
                    echo "  • default - Language-agnostic"
                    ;;
                react)
                    echo "  • react - React with TypeScript"
                    ;;
                python)
                    echo "  • python - Python with FastAPI"
                    ;;
                maui-appshell)
                    echo "  • maui-appshell - .NET MAUI mobile app with AppShell"
                    ;;
                maui-navigationpage)
                    echo "  • maui-navigationpage - .NET MAUI mobile app with NavigationPage"
                    ;;
                dotnet-microservice)
                    echo "  • dotnet-microservice - .NET microservice with FastEndpoints"
                    ;;
                fullstack)
                    echo "  • fullstack - React + Python"
                    ;;
                *)
                    echo "  • $template"
                    ;;
            esac
        done
    fi
}

# Main installation
main() {
    print_header
    
    print_info "Installing Claude global system to $INSTALL_DIR"
    echo ""
    
    # Run installation steps
    check_prerequisites
    backup_existing
    create_directories
    install_global_files
    create_agentic_command
    setup_shell_integration
    create_global_config
    create_version_file
    
    echo ""
    print_success "Claude global installation complete!"
    echo ""
    print_info "Installation locations:"
    echo "  • Global files: $INSTALL_DIR"
    echo "  • Configuration: $CONFIG_DIR"
    echo "  • Command: $HOME/.local/bin/agentic-init"
    echo ""
    print_info "To initialize a project:"
    echo "  1. Navigate to your project directory"
    echo "  2. Run: agentic-init [template]"
    echo ""
    print_info "Available templates:"
    list_templates
    echo ""
    print_warning "Please restart your shell or run:"
    echo "  source ~/.bashrc  # or ~/.zshrc"
}

# Run main installation
main "$@"
