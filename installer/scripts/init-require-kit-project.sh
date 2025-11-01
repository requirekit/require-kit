#!/bin/bash
# require-kit Project Initialization
# Creates required directory structure for requirements management

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
    echo -e "${BLUE}║         require-kit Project Initialization             ║${NC}"
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

create_project_structure() {
    print_info "Creating project structure..."

    # Requirements directories
    mkdir -p docs/requirements/{draft,approved,implemented}
    print_success "Created docs/requirements/ (draft, approved, implemented)"

    # Epic and Feature directories
    mkdir -p docs/epics/{active,completed,cancelled}
    print_success "Created docs/epics/ (active, completed, cancelled)"

    mkdir -p docs/features/{active,in_progress,completed}
    print_success "Created docs/features/ (active, in_progress, completed)"

    # BDD scenarios directory
    mkdir -p docs/bdd
    print_success "Created docs/bdd/"

    # Claude configuration directory
    mkdir -p .claude
    print_success "Created .claude/"

    echo ""
    print_success "Project structure created"
}

create_claude_config() {
    print_info "Creating Claude configuration..."

    cat > .claude/CLAUDE.md <<'EOF'
# require-kit Project Configuration

## Requirements Management

This project uses require-kit for requirements management with EARS notation.

## Commands

### Requirements Engineering
- /gather-requirements - Interactive requirements gathering
- /formalize-ears      - Convert to EARS notation
- /generate-bdd        - Generate BDD scenarios

### Epic & Feature Management
- /epic-create         - Create epic
- /feature-create      - Create feature
- /hierarchy-view      - View epic/feature hierarchy

## Directory Structure

- docs/requirements/ - EARS requirements (draft, approved, implemented)
- docs/epics/        - Epic specifications (active, completed, cancelled)
- docs/features/     - Feature specifications (active, in_progress, completed)
- docs/bdd/          - BDD/Gherkin scenarios

## EARS Notation Patterns

1. **Ubiquitous**: `The [system] shall [behavior]`
2. **Event-Driven**: `When [trigger], the [system] shall [response]`
3. **State-Driven**: `While [state], the [system] shall [behavior]`
4. **Unwanted Behavior**: `If [error], then the [system] shall [recovery]`
5. **Optional Feature**: `Where [feature], the [system] shall [behavior]`

## Workflow

1. Gather requirements: `/gather-requirements`
2. Formalize to EARS: `/formalize-ears`
3. Generate BDD scenarios: `/generate-bdd`
4. Create epics: `/epic-create`
5. Break into features: `/feature-create`
6. View hierarchy: `/hierarchy-view`

EOF

    print_success "Configuration created"
}

create_readme() {
    print_info "Creating README..."

    cat > docs/README.md <<'EOF'
# Requirements Documentation

This directory contains all requirements, epics, features, and BDD scenarios for this project.

## Directory Structure

### Requirements (`requirements/`)
- **draft/** - Requirements being gathered and refined
- **approved/** - Finalized requirements ready for implementation
- **implemented/** - Completed requirements with traceability

All requirements use **EARS notation** for clarity and testability.

### Epics (`epics/`)
- **active/** - Currently active epics
- **completed/** - Finished epics
- **cancelled/** - Cancelled or deprioritized epics

Epics represent large bodies of work that can span multiple releases.

### Features (`features/`)
- **active/** - Features ready to be worked on
- **in_progress/** - Features currently under development
- **completed/** - Finished features

Features are slices of epics that deliver specific value.

### BDD Scenarios (`bdd/`)
Gherkin scenarios generated from EARS requirements for behavior-driven development.

## Commands

Run these commands in Claude Code:

- `/gather-requirements` - Start requirements gathering
- `/formalize-ears` - Convert to EARS notation
- `/generate-bdd` - Generate BDD scenarios
- `/epic-create` - Create new epic
- `/feature-create` - Create new feature
- `/hierarchy-view` - View epic/feature hierarchy

## Integration

If **taskwright** is installed, you can link requirements to tasks for full traceability:
- Requirements → Epics → Features → Tasks → Implementation

EOF

    print_success "README created"
}

check_existing_config() {
    if [ -d ".claude" ] && [ -f ".claude/CLAUDE.md" ]; then
        print_warning "Existing .claude/CLAUDE.md found"
        echo -n "Overwrite? (y/n): "
        read -r response
        if [ "$response" != "y" ]; then
            print_info "Skipping configuration creation"
            return 1
        fi
    fi
    return 0
}

main() {
    print_header

    # Check if we're in a git repository (optional)
    if git rev-parse --git-dir > /dev/null 2>&1; then
        print_success "Git repository detected"
    else
        print_warning "Not in a git repository - consider initializing git"
    fi

    echo ""

    # Create structure
    create_project_structure
    echo ""

    # Create configuration
    if check_existing_config; then
        create_claude_config
        echo ""
    fi

    # Create README
    create_readme
    echo ""

    # Check for taskwright integration
    if [ -f "$HOME/.agentecflow/taskwright.marker" ]; then
        print_success "taskwright detected - full integration available"
        echo "  You can link requirements to tasks for complete traceability"
    else
        print_info "taskwright not detected - requirements management only"
        echo "  Install taskwright for task execution and full integration"
    fi

    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║         Initialization Complete!                        ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Project initialized for require-kit!"
    echo ""
    echo "Next steps:"
    echo "  1. Run '/gather-requirements' in Claude Code to start"
    echo "  2. Use '/formalize-ears' to convert to EARS notation"
    echo "  3. Generate BDD scenarios with '/generate-bdd'"
    echo ""
}

main "$@"
