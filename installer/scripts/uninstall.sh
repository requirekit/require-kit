#!/bin/bash
# require-kit Uninstallation Script
# Removes require-kit from namespaced directories

set -e

INSTALL_DIR="$HOME/.agentecflow"
PACKAGE_NAME="require-kit"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║         require-kit Uninstallation                     ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

remove_commands() {
    if [ -d "$INSTALL_DIR/commands/$PACKAGE_NAME" ]; then
        print_info "Removing commands..."

        # Remove symlinks pointing to require-kit commands
        for cmd in "$INSTALL_DIR/commands/$PACKAGE_NAME"/*.md; do
            if [ -f "$cmd" ]; then
                cmd_name=$(basename "$cmd")
                symlink="$INSTALL_DIR/commands/$cmd_name"

                if [ -L "$symlink" ] && \
                   [ "$(readlink "$symlink")" = "$PACKAGE_NAME/$cmd_name" ]; then
                    rm -f "$symlink"
                fi
            fi
        done

        # Remove namespaced directory
        rm -rf "$INSTALL_DIR/commands/$PACKAGE_NAME"
        print_success "Commands removed"
    else
        print_warning "Commands directory not found"
    fi
}

remove_agents() {
    if [ -d "$INSTALL_DIR/agents/$PACKAGE_NAME" ]; then
        print_info "Removing agents..."

        # Remove symlinks pointing to require-kit agents
        for agent in "$INSTALL_DIR/agents/$PACKAGE_NAME"/*.md; do
            if [ -f "$agent" ]; then
                agent_name=$(basename "$agent")
                symlink="$INSTALL_DIR/agents/$agent_name"

                if [ -L "$symlink" ] && \
                   [ "$(readlink "$symlink")" = "$PACKAGE_NAME/$agent_name" ]; then
                    rm -f "$symlink"
                fi
            fi
        done

        # Remove namespaced directory
        rm -rf "$INSTALL_DIR/agents/$PACKAGE_NAME"
        print_success "Agents removed"
    else
        print_warning "Agents directory not found"
    fi
}

remove_marker_file() {
    if [ -f "$INSTALL_DIR/$PACKAGE_NAME.marker" ]; then
        print_info "Removing marker file..."
        rm -f "$INSTALL_DIR/$PACKAGE_NAME.marker"
        print_success "Marker file removed"
    else
        print_warning "Marker file not found"
    fi
}

remove_tracking() {
    print_info "Removing installation tracking..."
    rm -f "$INSTALL_DIR/.installed/$PACKAGE_NAME.version"
    rm -f "$INSTALL_DIR/.installed/$PACKAGE_NAME.timestamp"
    print_success "Installation tracking removed"
}

cleanup_lib() {
    # Only remove feature_detection.py if taskwright is not installed
    if [ ! -f "$INSTALL_DIR/taskwright.marker" ] && [ -f "$INSTALL_DIR/lib/feature_detection.py" ]; then
        print_info "Removing shared library files..."
        print_warning "taskwright not detected - removing feature_detection.py"
        rm -f "$INSTALL_DIR/lib/feature_detection.py"

        # Remove lib directory if empty
        if [ -d "$INSTALL_DIR/lib" ] && [ -z "$(ls -A "$INSTALL_DIR/lib")" ]; then
            rmdir "$INSTALL_DIR/lib"
        fi

        print_success "Library files removed"
    elif [ -f "$INSTALL_DIR/taskwright.marker" ]; then
        print_info "Preserving feature_detection.py (taskwright still installed)"
    fi
}

cleanup_empty_directories() {
    print_info "Cleaning up empty directories..."

    # Remove .installed if empty
    if [ -d "$INSTALL_DIR/.installed" ] && [ -z "$(ls -A "$INSTALL_DIR/.installed")" ]; then
        rmdir "$INSTALL_DIR/.installed"
        print_success "Removed empty .installed directory"
    fi

    # Remove parent directories if completely empty
    if [ -d "$INSTALL_DIR" ] && [ -z "$(ls -A "$INSTALL_DIR")" ]; then
        rmdir "$INSTALL_DIR"
        print_success "Removed empty ~/.agentecflow directory"
    fi
}

print_completion_message() {
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║         Uninstallation Complete!                        ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "require-kit has been uninstalled from ~/.agentecflow"
    echo ""

    # Check if taskwright is still installed
    if [ -f "$INSTALL_DIR/taskwright.marker" ]; then
        print_info "taskwright is still installed and available"
        echo "  Task execution features remain available"
    fi
    echo ""
}

main() {
    print_header
    remove_commands
    remove_agents
    remove_marker_file
    remove_tracking
    cleanup_lib
    cleanup_empty_directories
    print_completion_message
}

main "$@"
