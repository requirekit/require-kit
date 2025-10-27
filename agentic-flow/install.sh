#!/bin/bash

# Agentecflow - Global Installation Script
# This script installs the Agentecflow system to ~/.agentecflow

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
INSTALL_DIR="$HOME/.agentecflow"
REPO_URL="https://github.com/yourusername/agentic-flow.git"
VERSION="1.0.0"

# ASCII Art Banner
print_banner() {
    echo -e "${CYAN}"
    cat << "EOF"
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║     ┌─┐┌─┐┌─┐┌┐┌┌┬┐┬┌─┐  ┌─┐┬  ┌─┐┬ ┬               ║
    ║     ├─┤│ ┬├┤ │││ │ ││     ├┤ │  │ ││││               ║
    ║     ┴ ┴└─┘└─┘┘└┘ ┴ ┴└─┘  └  ┴─┘└─┘└┴┘               ║
    ║                                                       ║
    ║     AI-Powered Software Engineering Lifecycle        ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Functions
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    echo -e "\n${CYAN}Checking prerequisites...${NC}"
    
    # Check for required commands
    local missing_deps=()
    
    if ! command -v git &> /dev/null; then
        missing_deps+=("git")
    fi
    
    if ! command -v curl &> /dev/null && ! command -v wget &> /dev/null; then
        missing_deps+=("curl or wget")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_error "Missing required dependencies: ${missing_deps[*]}"
        echo "Please install the missing dependencies and try again."
        exit 1
    fi
    
    print_status "All prerequisites met"
}

# Backup existing installation
backup_existing() {
    if [ -d "$INSTALL_DIR" ]; then
        print_warning "Existing installation found at $INSTALL_DIR"
        echo -n "Do you want to backup the existing installation? (y/n): "
        read -r response
        
        if [[ "$response" =~ ^[Yy]$ ]]; then
            local backup_dir="${INSTALL_DIR}.backup.$(date +%Y%m%d_%H%M%S)"
            mv "$INSTALL_DIR" "$backup_dir"
            print_status "Existing installation backed up to $backup_dir"
        else
            echo -n "Do you want to overwrite the existing installation? (y/n): "
            read -r response
            if [[ "$response" =~ ^[Yy]$ ]]; then
                rm -rf "$INSTALL_DIR"
                print_status "Removed existing installation"
            else
                print_info "Installation cancelled"
                exit 0
            fi
        fi
    fi
}

# Create directory structure
create_directory_structure() {
    echo -e "\n${CYAN}Creating directory structure...${NC}"
    
    # Create main directories
    mkdir -p "$INSTALL_DIR"/{bin,versions,instructions,templates,plugins,cache}
    mkdir -p "$INSTALL_DIR"/instructions/{core,stacks}
    mkdir -p "$INSTALL_DIR"/templates/{default,react,python,typescript,go}
    
    print_status "Directory structure created"
}

# Install core files
install_core_files() {
    echo -e "\n${CYAN}Installing core files...${NC}"
    
    # Check if we're running from the repo
    if [ -f "global/bin/agentic-flow" ]; then
        # Local installation from repo
        cp -r global/* "$INSTALL_DIR/"
        print_status "Installed from local repository"
    else
        # Download from GitHub
        print_info "Downloading from GitHub..."
        
        local temp_dir=$(mktemp -d)
        cd "$temp_dir"
        
        if command -v git &> /dev/null; then
            git clone --depth 1 "$REPO_URL" . 2>/dev/null || {
                print_error "Failed to clone repository"
                rm -rf "$temp_dir"
                exit 1
            }
            cp -r global/* "$INSTALL_DIR/"
        else
            print_error "Git not found. Please install git and try again."
            rm -rf "$temp_dir"
            exit 1
        fi
        
        cd - > /dev/null
        rm -rf "$temp_dir"
        print_status "Downloaded and installed core files"
    fi
    
    # Make binary executable
    chmod +x "$INSTALL_DIR/bin/agentic-flow"
    
    # Create version symlink
    mkdir -p "$INSTALL_DIR/versions/$VERSION"
    ln -sfn "$VERSION" "$INSTALL_DIR/versions/latest"
    
    print_status "Core files installed"
}

# Setup shell integration
setup_shell_integration() {
    echo -e "\n${CYAN}Setting up shell integration...${NC}"
    
    local shell_config=""
    local shell_name=""
    
    # Detect shell
    if [ -n "$BASH_VERSION" ]; then
        shell_name="bash"
        if [ -f "$HOME/.bashrc" ]; then
            shell_config="$HOME/.bashrc"
        elif [ -f "$HOME/.bash_profile" ]; then
            shell_config="$HOME/.bash_profile"
        fi
    elif [ -n "$ZSH_VERSION" ]; then
        shell_name="zsh"
        shell_config="$HOME/.zshrc"
    else
        print_warning "Unknown shell. Please manually add $INSTALL_DIR/bin to your PATH"
        return
    fi
    
    if [ -n "$shell_config" ]; then
        # Check if already in PATH
        if ! grep -q "agentic-flow/bin" "$shell_config" 2>/dev/null; then
            echo "" >> "$shell_config"
            echo "# Agentecflow" >> "$shell_config"
            echo "export PATH=\"\$HOME/.agentecflow/bin:\$PATH\"" >> "$shell_config"
            echo "export AGENTECFLOW_HOME=\"\$HOME/.agentecflow\"" >> "$shell_config"
            
            # Add auto-completion
            echo "# Agentecflow auto-completion" >> "$shell_config"
            if [ "$shell_name" = "bash" ]; then
                echo "[ -f \"\$HOME/.agentecflow/completions/bash\" ] && source \"\$HOME/.agentecflow/completions/bash\"" >> "$shell_config"
            elif [ "$shell_name" = "zsh" ]; then
                echo "[ -f \"\$HOME/.agentecflow/completions/zsh\" ] && source \"\$HOME/.agentecflow/completions/zsh\"" >> "$shell_config"
            fi
            
            print_status "Added Agentecflow to $shell_config"
            print_info "Please run: source $shell_config"
        else
            print_status "Agentecflow already in PATH"
        fi
    fi
}

# Create default configuration
create_default_config() {
    echo -e "\n${CYAN}Creating default configuration...${NC}"
    
    cat > "$INSTALL_DIR/config.json" << EOF
{
  "version": "$VERSION",
  "claude": {
    "model": "claude-3-sonnet",
    "temperature": 0.7,
    "max_tokens": 4096
  },
  "defaults": {
    "testCoverage": 80,
    "earsCompliance": 100,
    "bddCoverage": 95,
    "maxComplexity": 10
  },
  "stacks": {
    "installed": [],
    "default": "default"
  },
  "telemetry": false
}
EOF
    
    print_status "Default configuration created"
}

# Verify installation
verify_installation() {
    echo -e "\n${CYAN}Verifying installation...${NC}"
    
    if [ -f "$INSTALL_DIR/bin/agentic-flow" ] && [ -x "$INSTALL_DIR/bin/agentic-flow" ]; then
        print_status "Binary installed and executable"
    else
        print_error "Binary not found or not executable"
        return 1
    fi
    
    if [ -d "$INSTALL_DIR/instructions/core" ]; then
        print_status "Core instructions installed"
    else
        print_error "Core instructions not found"
        return 1
    fi
    
    if [ -f "$INSTALL_DIR/config.json" ]; then
        print_status "Configuration file created"
    else
        print_error "Configuration file not found"
        return 1
    fi
    
    return 0
}

# Main installation
main() {
    print_banner
    
    echo "Welcome to the Agentecflow installation!"
    echo "This will install Agentecflow to: $INSTALL_DIR"
    echo ""
    
    check_prerequisites
    backup_existing
    create_directory_structure
    install_core_files
    create_default_config
    setup_shell_integration
    
    if verify_installation; then
        echo ""
        print_status "${GREEN}Installation completed successfully!${NC}"
        echo ""
        echo "Next steps:"
        echo "  1. Reload your shell configuration:"
        echo "     ${CYAN}source ~/.bashrc${NC} (or ~/.zshrc for zsh)"
        echo ""
        echo "  2. Verify the installation:"
        echo "     ${CYAN}agentic-flow --version${NC}"
        echo ""
        echo "  3. Initialize a project:"
        echo "     ${CYAN}cd your-project${NC}"
        echo "     ${CYAN}agentic-flow init${NC}"
        echo ""
        echo "  4. Get help:"
        echo "     ${CYAN}agentic-flow --help${NC}"
        echo ""
        echo "Documentation: https://github.com/yourusername/agentic-flow"
        echo "Happy engineering! 🚀"
    else
        print_error "Installation failed. Please check the errors above."
        exit 1
    fi
}

# Run main function
main "$@"
