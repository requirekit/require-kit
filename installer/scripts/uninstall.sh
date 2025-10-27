#!/bin/bash

# Agentecflow Uninstaller
# Safely removes Agentecflow from your system

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo ""
    echo -e "${RED}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║         Agentecflow Uninstaller                       ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

confirm_uninstall() {
    echo -e "${YELLOW}⚠️  WARNING: This will remove Agentecflow from your system${NC}"
    echo ""
    echo "This will delete:"
    echo "  • ~/.agentecflow (global installation)"
    echo "  • ~/.config/agentecflow (configuration)"
    echo "  • PATH modifications in shell config"
    echo ""
    echo -e "${YELLOW}Project-specific .claude directories will NOT be removed${NC}"
    echo ""
    read -p "Are you sure you want to continue? (yes/no): " -r
    echo
    if [[ ! $REPLY =~ ^[Yy]es$ ]]; then
        echo -e "${GREEN}Uninstallation cancelled${NC}"
        exit 0
    fi
}

backup_configuration() {
    if [ -d "$HOME/.config/agentecflow" ]; then
        local backup_dir="$HOME/.config/agentecflow.backup.$(date +%Y%m%d_%H%M%S)"
        echo -e "${BLUE}Creating configuration backup at $backup_dir${NC}"
        cp -r "$HOME/.config/agentecflow" "$backup_dir"
    fi
}

remove_installation() {
    echo -e "${BLUE}Removing Agentecflow installation...${NC}"
    
    # Remove main installation
    if [ -d "$HOME/.agentecflow" ]; then
        rm -rf "$HOME/.agentecflow"
        echo -e "${GREEN}✓ Removed ~/.agentecflow${NC}"
    else
        echo -e "${YELLOW}~/.agentecflow not found${NC}"
    fi
    
    # Remove configuration
    if [ -d "$HOME/.config/agentecflow" ]; then
        rm -rf "$HOME/.config/agentecflow"
        echo -e "${GREEN}✓ Removed ~/.config/agentecflow${NC}"
    else
        echo -e "${YELLOW}~/.config/agentecflow not found${NC}"
    fi
}

remove_shell_integration() {
    echo -e "${BLUE}Removing shell integration...${NC}"
    
    local modified=false
    
    # Remove from bashrc
    if [ -f "$HOME/.bashrc" ]; then
        if grep -q "agentecflow" "$HOME/.bashrc"; then
            sed -i.backup '/# Agentecflow/,/^$/d' "$HOME/.bashrc" 2>/dev/null || \
            sed -i '' '/# Agentecflow/,/^$/d' "$HOME/.bashrc" 2>/dev/null
            echo -e "${GREEN}✓ Removed from ~/.bashrc${NC}"
            modified=true
        fi
    fi
    
    # Remove from zshrc
    if [ -f "$HOME/.zshrc" ]; then
        if grep -q "agentecflow" "$HOME/.zshrc"; then
            sed -i.backup '/# Agentecflow/,/^$/d' "$HOME/.zshrc" 2>/dev/null || \
            sed -i '' '/# Agentecflow/,/^$/d' "$HOME/.zshrc" 2>/dev/null
            echo -e "${GREEN}✓ Removed from ~/.zshrc${NC}"
            modified=true
        fi
    fi
    
    # Remove from bash_profile
    if [ -f "$HOME/.bash_profile" ]; then
        if grep -q "agentecflow" "$HOME/.bash_profile"; then
            sed -i.backup '/# Agentecflow/,/^$/d' "$HOME/.bash_profile" 2>/dev/null || \
            sed -i '' '/# Agentecflow/,/^$/d' "$HOME/.bash_profile" 2>/dev/null
            echo -e "${GREEN}✓ Removed from ~/.bash_profile${NC}"
            modified=true
        fi
    fi
    
    if [ "$modified" = true ]; then
        echo -e "${YELLOW}Note: Restart your shell for changes to take effect${NC}"
    fi
}

check_projects() {
    echo -e "${BLUE}Checking for Agentecflow projects...${NC}"
    
    local projects=$(find "$HOME" -type d -name ".claude" -maxdepth 4 2>/dev/null | head -10)
    
    if [ -n "$projects" ]; then
        echo -e "${YELLOW}Found Agentecflow projects at:${NC}"
        echo "$projects" | while read -r project; do
            echo "  • $(dirname "$project")"
        done
        echo ""
        echo -e "${YELLOW}These project configurations were NOT removed.${NC}"
        echo "To clean up a project, delete its .claude directory manually."
    else
        echo "No Agentecflow projects found in common locations"
    fi
}

print_footer() {
    echo ""
    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}Agentecflow has been successfully uninstalled${NC}"
    echo ""
    echo "Thank you for using Agentecflow!"
    echo ""
    echo "If you want to reinstall later:"
    echo "  curl -sSL https://install.agentecflow.ai | bash"
    echo ""
    echo "For feedback or issues:"
    echo "  https://github.com/appmilla/agentecflow/issues"
    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
}

# Main uninstallation
main() {
    print_header
    confirm_uninstall
    backup_configuration
    remove_installation
    remove_shell_integration
    check_projects
    print_footer
}

# Run uninstaller
main "$@"
