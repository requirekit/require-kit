#!/bin/bash

# Agentecflow Project Initialization Script
# Works with ~/.agentecflow structure

set -e

# Configuration - Support multiple possible locations
if [ -n "$CLAUDE_HOME" ]; then
    AGENTECFLOW_HOME="$CLAUDE_HOME"
elif [ -d "$HOME/.agentecflow" ]; then
    AGENTECFLOW_HOME="$HOME/.agentecflow"
elif [ -d "$HOME/.agenticflow" ]; then
    AGENTECFLOW_HOME="$HOME/.agenticflow"
elif [ -d "$HOME/.agentic-flow" ]; then
    AGENTECFLOW_HOME="$HOME/.agentic-flow"
elif [ -d "$HOME/.claude" ]; then
    AGENTECFLOW_HOME="$HOME/.claude"
else
    echo "Error: No Agentecflow installation found"
    echo "Please run the installer first"
    exit 1
fi

PROJECT_DIR="$(pwd)"
TEMPLATE="${1:-default}"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

print_header() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║         Agentecflow Project Initialization             ║${NC}"
    echo -e "${BLUE}║         Template: ${BOLD}$(printf '%-20s' "$TEMPLATE")${NC}${BLUE}         ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Show available templates
show_templates() {
    echo "Available templates:"
    if [ -d "$AGENTICFLOW_HOME/templates" ]; then
        for template_dir in "$AGENTICFLOW_HOME/templates"/*/; do
            if [ -d "$template_dir" ]; then
                local name=$(basename "$template_dir")
                case "$name" in
                    default)
                        echo "  • default - Language-agnostic"
                        ;;
                    react)
                        echo "  • react - React with TypeScript"
                        ;;
                    python)
                        echo "  • python - Python with FastAPI"
                        ;;
                    maui)
                        echo "  • maui - .NET MAUI mobile app"
                        ;;
                    dotnet-microservice)
                        echo "  • dotnet-microservice - .NET microservice with FastEndpoints"
                        ;;
                    fullstack)
                        echo "  • fullstack - React + Python"
                        ;;
                    *)
                        echo "  • $name"
                        ;;
                esac
            fi
        done
    fi
}

# Interactive template selection
select_template_interactive() {
    show_templates
    echo ""
    read -p "Select template (default): " selected
    TEMPLATE="${selected:-default}"
}

# Detect existing project type
detect_project_type() {
    # Check for .csproj files
    if ls *.csproj 2>/dev/null | grep -q . || ls */*.csproj 2>/dev/null | grep -q .; then
        # Check if it's a MAUI project
        if ls *.csproj 2>/dev/null | xargs grep -l "Microsoft.Maui" 2>/dev/null || \
           ls */*.csproj 2>/dev/null | xargs grep -l "Microsoft.Maui" 2>/dev/null; then
            echo "maui"
        elif ls *.csproj 2>/dev/null | xargs grep -l "Microsoft.AspNetCore\|FastEndpoints" 2>/dev/null || \
             ls */*.csproj 2>/dev/null | xargs grep -l "Microsoft.AspNetCore\|FastEndpoints" 2>/dev/null; then
            echo "dotnet-microservice"
        else
            echo "dotnet"
        fi
    elif [ -f "package.json" ]; then
        if grep -q "react" package.json; then
            echo "react"
        elif grep -q "vue" package.json; then
            echo "vue"
        else
            echo "node"
        fi
    elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
        echo "python"
    else
        echo "unknown"
    fi
}

# Check if already initialized
check_existing() {
    if [ -d ".claude" ]; then
        print_warning ".claude directory already exists"
        read -p "Reinitialize? This will backup the existing configuration (y/n): " -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Initialization cancelled"
            exit 0
        fi
        mv .claude .claude.backup.$(date +%Y%m%d_%H%M%S)
        print_success "Existing configuration backed up"
    fi
}

# Create project structure
create_project_structure() {
    print_info "Creating project structure..."
    
    # Always create .claude at root
    mkdir -p .claude/{agents,commands,hooks,templates,stacks}
    
    # Always create docs at root
    mkdir -p docs/{requirements,bdd/features,adr,state}
    mkdir -p docs/requirements/{draft,approved,implemented}
    
    # Handle test directory based on project type
    local detected_type=$(detect_project_type)
    case "$detected_type" in
        maui|dotnet*)
            print_info "Tests will be managed within .NET solution structure"
            ;;
        *)
            if [ ! -d "tests" ]; then
                mkdir -p tests/{unit,integration,e2e}
                print_success "Created test directories"
            else
                print_info "Using existing tests directory"
            fi
            ;;
    esac
    
    print_success "Project structure created"
}

# Copy template files
copy_template_files() {
    local detected_type=$(detect_project_type)
    local effective_template="$TEMPLATE"
    
    # Auto-select template based on detected type if using default
    if [ "$TEMPLATE" = "default" ] && [ "$detected_type" != "unknown" ]; then
        case "$detected_type" in
            maui) effective_template="maui" ;;
            dotnet-microservice) effective_template="dotnet-microservice" ;;
            react) effective_template="react" ;;
            python) effective_template="python" ;;
        esac
        if [ "$effective_template" != "default" ]; then
            print_info "Auto-selected template: $effective_template (detected $detected_type project)"
        fi
    fi
    
    local template_dir="$AGENTICFLOW_HOME/templates/$effective_template"
    
    if [ ! -d "$template_dir" ]; then
        print_warning "Template '$effective_template' not found, using default"
        template_dir="$AGENTICFLOW_HOME/templates/default"
        effective_template="default"
    fi
    
    print_info "Using template: $effective_template"
    
    # Copy CLAUDE.md context file
    if [ -f "$template_dir/CLAUDE.md" ]; then
        cp "$template_dir/CLAUDE.md" .claude/
        print_success "Copied project context file"
    fi
    
    # Copy agents - either from template or global
    if [ -d "$template_dir/agents" ] && [ "$(ls -A $template_dir/agents 2>/dev/null)" ]; then
        cp -r "$template_dir/agents/"* .claude/agents/ 2>/dev/null || true
        print_success "Copied template-specific agents"
    elif [ -d "$AGENTICFLOW_HOME/agents" ] && [ "$(ls -A $AGENTICFLOW_HOME/agents 2>/dev/null)" ]; then
        # Copy global agents
        cp -r "$AGENTICFLOW_HOME/agents/"* .claude/agents/ 2>/dev/null || true
        print_success "Copied global agents"
    else
        print_warning "No agents found to copy"
    fi
    
    # Copy templates
    if [ -d "$template_dir/templates" ]; then
        cp -r "$template_dir/templates/"* .claude/templates/ 2>/dev/null || true
        print_success "Copied template files"
    fi
    
    # Copy other template-specific files
    for file in "$template_dir"/*.md "$template_dir"/*.json; do
        if [ -f "$file" ] && [ "$(basename "$file")" != "CLAUDE.md" ]; then
            cp "$file" .claude/
        fi
    done 2>/dev/null || true
    
    # Link to global commands
    if [ -d "$AGENTICFLOW_HOME/commands" ]; then
        for cmd in "$AGENTICFLOW_HOME/commands"/*.md; do
            if [ -f "$cmd" ]; then
                local cmd_name=$(basename "$cmd")
                # Create symlink or copy if symlink fails
                ln -sf "$cmd" ".claude/commands/$cmd_name" 2>/dev/null || \
                cp "$cmd" ".claude/commands/$cmd_name"
            fi
        done
        print_success "Linked Agentecflow commands"
    fi
    
    TEMPLATE="$effective_template"  # Update for later use
}

# Create project configuration
create_config() {
    print_info "Creating project configuration..."
    
    local project_name=$(basename "$PROJECT_DIR")
    local detected_type=$(detect_project_type)
    
    cat > .claude/settings.json << EOF
{
  "version": "1.0.0",
  "extends": "$AGENTICFLOW_HOME/templates/$TEMPLATE",
  "project": {
    "name": "$project_name",
    "template": "$TEMPLATE",
    "detected_type": "$detected_type",
    "created": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  },
  "methodology": {
    "requirements": "EARS",
    "testing": "BDD",
    "documentation": "ADR"
  },
  "quality": {
    "coverage": 80,
    "complexity": 10,
    "gates": true
  }
}
EOF
    
    print_success "Created project configuration"
}

# Create initial files
create_initial_files() {
    print_info "Creating initial documentation..."
    
    # Create .claudeignore
    cat > .claude/.claudeignore << 'EOF'
# Files to exclude from Claude context
node_modules/
venv/
.venv/
__pycache__/
*.pyc
dist/
build/
bin/
obj/
.git/
.env
*.log
coverage/
*.tmp
.vs/
.vscode/settings.json
.idea/
*.user
*.suo
EOF
    
    # Create initial sprint file
    cat > docs/state/current-sprint.md << EOF
---
sprint: 1
start: $(date +%Y-%m-%d)
status: planning
---

# Sprint 1 - Project Setup

## Goals
- [ ] Set up Agentecflow system
- [ ] Define initial requirements
- [ ] Create first BDD scenarios

## Progress
- Overall: 10% [██░░░░░░░░░░░░░░░░░░]

## Next Steps
1. Use \`/gather-requirements\` to start requirements gathering
2. Use \`/formalize-ears\` to convert to EARS notation
3. Use \`/generate-bdd\` to create test scenarios
EOF
    
    # Create first ADR
    cat > docs/adr/0001-adopt-agentic-flow.md << EOF
---
id: ADR-001
status: accepted
date: $(date +%Y-%m-%d)
---

# ADR-001: Adopt Agentecflow System

## Status
Accepted

## Context
We need a systematic approach to software development with clear requirements, automated testing, and quality gates.

## Decision
Adopt the Agentecflow system with EARS requirements and BDD testing.

## Consequences
**Positive:**
- Clear requirements traceability
- Automated test generation
- Quality enforcement

**Negative:**
- Initial learning curve
- Additional setup overhead
EOF
    
    print_success "Created initial documentation"
}

# Print next steps
print_next_steps() {
    local detected_type=$(detect_project_type)
    
    echo ""
    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✅ Agentecflow successfully initialized!${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${BOLD}Project Configuration:${NC}"
    echo "  📁 Configuration: .claude/"
    echo "  📚 Documentation: docs/"
    echo "  🎨 Template: $TEMPLATE"
    echo "  🔍 Detected Type: $detected_type"
    echo ""
    
    # List installed agents
    echo -e "${BOLD}AI Agents:${NC}"
    if [ -d ".claude/agents" ]; then
        for agent in .claude/agents/*.md; do
            if [ -f "$agent" ]; then
                echo "  🤖 $(basename "$agent" .md)"
            fi
        done
    fi
    echo ""
    
    # Template-specific instructions
    case "$TEMPLATE" in
        dotnet-microservice)
            echo -e "${BOLD}Next Steps for .NET Microservice:${NC}"
            echo "  1. Create solution and projects (if not done):"
            echo "     dotnet new sln -n YourService"
            echo "     dotnet new webapi -n YourService.API"
            echo "     dotnet new xunit -n YourService.Tests"
            echo ""
            echo "  2. Install required packages:"
            echo "     cd YourService.API"
            echo "     dotnet add package FastEndpoints"
            echo "     dotnet add package LanguageExt.Core"
            echo "     dotnet add package FluentValidation"
            echo ""
            echo "  3. Copy template files from .claude/templates/"
            echo ""
            ;;
        maui)
            echo -e "${BOLD}Next Steps for .NET MAUI:${NC}"
            echo "  1. Create MAUI app (if not done):"
            echo "     dotnet new maui -n YourApp"
            echo ""
            echo "  2. Install required packages:"
            echo "     dotnet add package LanguageExt.Core"
            echo "     dotnet add package CommunityToolkit.Mvvm"
            echo "     dotnet add package CommunityToolkit.Maui"
            echo ""
            echo "  3. Copy template files from .claude/templates/"
            echo ""
            ;;
        react)
            echo -e "${BOLD}Next Steps for React:${NC}"
            echo "  1. Ensure testing packages installed:"
            echo "     npm install -D vitest @testing-library/react"
            echo "     npm install -D @playwright/test"
            echo ""
            ;;
        python)
            echo -e "${BOLD}Next Steps for Python:${NC}"
            echo "  1. Set up virtual environment:"
            echo "     python -m venv venv"
            echo "     source venv/bin/activate"
            echo ""
            echo "  2. Install packages:"
            echo "     pip install fastapi uvicorn"
            echo "     pip install pytest pytest-asyncio"
            echo ""
            ;;
    esac
    
    echo -e "${BOLD}Workflow Commands (use in Claude/Cursor):${NC}"
    echo "  /gather-requirements - Start requirements gathering"
    echo "  /formalize-ears     - Convert to EARS notation"
    echo "  /generate-bdd       - Create test scenarios"
    echo "  /execute-tests      - Run test suite"
    echo "  /update-state       - Update progress"
    echo ""
    echo -e "${BOLD}Using AI Agents:${NC}"
    echo "  @requirements-analyst - Help with requirements"
    echo "  @bdd-generator       - Generate test scenarios"
    echo "  @code-reviewer       - Review code quality"
    echo "  @test-orchestrator   - Manage testing"
    echo ""
    echo -e "${BLUE}Ready to start development!${NC}"
}

# Main function
main() {
    # Handle arguments
    case "$1" in
        -h|--help|help)
            show_templates
            exit 0
            ;;
        -i|--interactive)
            select_template_interactive
            ;;
        "")
            # No template specified, try to auto-detect or go interactive
            local detected=$(detect_project_type)
            if [ "$detected" != "unknown" ]; then
                print_info "Detected project type: $detected"
                read -p "Use matching template? (y/n): " -r
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    case "$detected" in
                        maui) TEMPLATE="maui" ;;
                        dotnet-microservice) TEMPLATE="dotnet-microservice" ;;
                        react) TEMPLATE="react" ;;
                        python) TEMPLATE="python" ;;
                        *) TEMPLATE="default" ;;
                    esac
                else
                    select_template_interactive
                fi
            else
                select_template_interactive
            fi
            ;;
        *)
            TEMPLATE="$1"
            ;;
    esac
    
    print_header
    print_info "Using Agentecflow from: $AGENTECFLOW_HOME"
    check_existing
    create_project_structure
    copy_template_files
    create_config
    create_initial_files
    print_next_steps
}

# Run main
main "$@"
