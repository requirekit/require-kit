---
id: REQ-003A
title: "Update require-kit Installer for Shared Installation"
created: 2025-10-27
status: backlog
priority: high
complexity: 4
parent_task: REQ-003
subtasks: []
estimated_hours: 2
---

# REQ-003A: Update require-kit Installer

## Description

Modify require-kit installer to install to namespaced directory `~/.agentecflow/commands/require-kit/` and `~/.agentecflow/agents/require-kit/`, allowing coexistence with dev-tasker.

## Changes Required

### 1. Update install.sh

**Current behavior**: Installs directly to `~/.agentecflow/commands/`

**New behavior**: Installs to `~/.agentecflow/commands/require-kit/`

```bash
#!/bin/bash
# require-kit Installation Script

set -e

INSTALL_DIR="$HOME/.agentecflow"
PACKAGE_NAME="require-kit"
PACKAGE_VERSION="1.0.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

print_header() {
    echo ""
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║         require-kit Installation                       ║"
    echo "║         Version: $PACKAGE_VERSION                      ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
}

print_success() {
    echo "✓ $1"
}

print_error() {
    echo "✗ $1"
    exit 1
}

check_prerequisites() {
    print_info "Checking prerequisites..."

    # Check for required commands
    for cmd in git bash; do
        if ! command -v $cmd &> /dev/null; then
            print_error "Required command '$cmd' not found"
        fi
    done

    print_success "Prerequisites check passed"
}

create_directory_structure() {
    print_info "Creating directory structure..."

    mkdir -p "$INSTALL_DIR/commands/$PACKAGE_NAME"
    mkdir -p "$INSTALL_DIR/agents/$PACKAGE_NAME"
    mkdir -p "$INSTALL_DIR/.installed"

    print_success "Directory structure created"
}

install_commands() {
    print_info "Installing commands..."

    # Copy commands to namespaced directory
    cp "$SCRIPT_DIR/global/commands/"*.md "$INSTALL_DIR/commands/$PACKAGE_NAME/" 2>/dev/null || true

    # Create symlinks for backwards compatibility
    for cmd in "$INSTALL_DIR/commands/$PACKAGE_NAME"/*.md; do
        cmd_name=$(basename "$cmd")

        # Only create symlink if it doesn't exist or points to require-kit
        if [ ! -e "$INSTALL_DIR/commands/$cmd_name" ] || \
           [ "$(readlink "$INSTALL_DIR/commands/$cmd_name" 2>/dev/null)" = "$PACKAGE_NAME/$cmd_name" ]; then
            ln -sf "$PACKAGE_NAME/$cmd_name" "$INSTALL_DIR/commands/$cmd_name"
        fi
    done

    print_success "Commands installed"
}

install_agents() {
    print_info "Installing agents..."

    # Copy agents to namespaced directory
    cp "$SCRIPT_DIR/global/agents/"*.md "$INSTALL_DIR/agents/$PACKAGE_NAME/" 2>/dev/null || true

    # Create symlinks for backwards compatibility
    for agent in "$INSTALL_DIR/agents/$PACKAGE_NAME"/*.md; do
        agent_name=$(basename "$agent")

        if [ ! -e "$INSTALL_DIR/agents/$agent_name" ] || \
           [ "$(readlink "$INSTALL_DIR/agents/$agent_name" 2>/dev/null)" = "$PACKAGE_NAME/$agent_name" ]; then
            ln -sf "$PACKAGE_NAME/$agent_name" "$INSTALL_DIR/agents/$agent_name"
        fi
    done

    print_success "Agents installed"
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

    print_success "Installation verified"
}

print_completion_message() {
    echo ""
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║         Installation Complete!                          ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
    echo "require-kit has been installed to ~/.agentecflow"
    echo ""
    echo "Available commands:"
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
}

# Main installation flow
main() {
    print_header
    check_prerequisites
    create_directory_structure
    install_commands
    install_agents
    track_installation
    verify_installation
    print_completion_message
}

main "$@"
```

### 2. Update manifest.json

```json
{
  "name": "require-kit",
  "version": "1.0.0",
  "description": "Requirements Management Toolkit with EARS, BDD, and Epic/Feature Hierarchy",
  "homepage": "https://github.com/yourusername/require-kit",
  "repository": {
    "type": "git",
    "url": "https://github.com/yourusername/require-kit.git"
  },
  "author": "Your Name",
  "license": "MIT",
  "system": {
    "min_version": "1.0.0",
    "api_version": "v1",
    "install_dir": "~/.agentecflow",
    "package_name": "require-kit",
    "namespace": "require-kit"
  },
  "capabilities": [
    "requirements-engineering",
    "ears-notation",
    "bdd-generation",
    "epic-feature-hierarchy",
    "requirements-traceability"
  ],
  "dependencies": {
    "required": ["bash", "git"],
    "optional": ["dev-tasker"]
  },
  "compatible_with": {
    "dev-tasker": ">=1.0.0"
  }
}
```

### 3. Create uninstall.sh

```bash
#!/bin/bash
# require-kit Uninstallation Script

set -e

INSTALL_DIR="$HOME/.agentecflow"
PACKAGE_NAME="require-kit"

print_header() {
    echo ""
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║         require-kit Uninstallation                     ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
}

print_success() {
    echo "✓ $1"
}

print_warning() {
    echo "⚠ $1"
}

remove_commands() {
    if [ -d "$INSTALL_DIR/commands/$PACKAGE_NAME" ]; then
        # Remove symlinks pointing to require-kit commands
        for cmd in "$INSTALL_DIR/commands/$PACKAGE_NAME"/*.md; do
            cmd_name=$(basename "$cmd")
            symlink="$INSTALL_DIR/commands/$cmd_name"

            if [ -L "$symlink" ] && \
               [ "$(readlink "$symlink")" = "$PACKAGE_NAME/$cmd_name" ]; then
                rm -f "$symlink"
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
        # Remove symlinks pointing to require-kit agents
        for agent in "$INSTALL_DIR/agents/$PACKAGE_NAME"/*.md; do
            agent_name=$(basename "$agent")
            symlink="$INSTALL_DIR/agents/$agent_name"

            if [ -L "$symlink" ] && \
               [ "$(readlink "$symlink")" = "$PACKAGE_NAME/$agent_name" ]; then
                rm -f "$symlink"
            fi
        done

        # Remove namespaced directory
        rm -rf "$INSTALL_DIR/agents/$PACKAGE_NAME"
        print_success "Agents removed"
    else
        print_warning "Agents directory not found"
    fi
}

remove_tracking() {
    rm -f "$INSTALL_DIR/.installed/$PACKAGE_NAME.version"
    rm -f "$INSTALL_DIR/.installed/$PACKAGE_NAME.timestamp"
    print_success "Installation tracking removed"
}

cleanup_empty_directories() {
    # Remove .installed if empty
    if [ -d "$INSTALL_DIR/.installed" ] && [ -z "$(ls -A "$INSTALL_DIR/.installed")" ]; then
        rmdir "$INSTALL_DIR/.installed"
    fi

    # Remove parent directories if completely empty
    if [ -d "$INSTALL_DIR" ] && [ -z "$(ls -A "$INSTALL_DIR")" ]; then
        rmdir "$INSTALL_DIR"
        print_success "Removed empty ~/.agentecflow directory"
    fi
}

print_completion_message() {
    echo ""
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║         Uninstallation Complete!                        ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
    echo "require-kit has been uninstalled from ~/.agentecflow"
    echo ""
}

main() {
    print_header
    remove_commands
    remove_agents
    remove_tracking
    cleanup_empty_directories
    print_completion_message
}

main "$@"
```

### 4. Create init-project.sh (optional)

```bash
#!/bin/bash
# require-kit Project Initialization

PACKAGE_NAME="require-kit"

print_header() {
    echo ""
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║         require-kit Project Initialization             ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
}

create_project_structure() {
    mkdir -p docs/requirements/{draft,approved,implemented}
    mkdir -p docs/epics/{active,completed,cancelled}
    mkdir -p docs/features/{active,in_progress,completed}
    mkdir -p docs/bdd

    mkdir -p .claude

    echo "✓ Project structure created"
}

create_claude_config() {
    cat > .claude/CLAUDE.md <<'EOF'
# require-kit Project Configuration

## Requirements Management

This project uses require-kit for requirements management with EARS notation.

## Commands

- /gather-requirements - Interactive requirements gathering
- /formalize-ears      - Convert to EARS notation
- /generate-bdd        - Generate BDD scenarios
- /epic-create         - Create epic
- /feature-create      - Create feature
- /hierarchy-view      - View hierarchy

## Directory Structure

- docs/requirements/ - EARS requirements
- docs/epics/        - Epic specifications
- docs/features/     - Feature specifications
- docs/bdd/          - BDD/Gherkin scenarios
EOF

    echo "✓ Configuration created"
}

main() {
    print_header
    create_project_structure
    create_claude_config

    echo ""
    echo "Project initialized! Run '/gather-requirements' to start."
    echo ""
}

main "$@"
```

## Testing

```bash
# Test installation
cd /path/to/require-kit
./installer/scripts/install.sh

# Verify structure
ls -la ~/.agentecflow/commands/require-kit/
ls -la ~/.agentecflow/agents/require-kit/
cat ~/.agentecflow/.installed/require-kit.version

# Test project init
cd /tmp/test-project
require-kit init
tree -L 2

# Test uninstallation
cd /path/to/require-kit
./installer/scripts/uninstall.sh

# Verify clean
[ ! -d ~/.agentecflow/commands/require-kit ] && echo "✓ Uninstalled"
```

## Acceptance Criteria

- [ ] install.sh installs to namespaced directories
- [ ] Symlinks created for backwards compatibility
- [ ] manifest.json updated with namespace info
- [ ] uninstall.sh removes only require-kit files
- [ ] Version tracking works (.installed/)
- [ ] Standalone installation works
- [ ] Project initialization works
- [ ] Verification tests pass

## Estimated Time

2 hours
