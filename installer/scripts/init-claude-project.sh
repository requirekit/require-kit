#!/bin/bash

# Claude Project Initialization Script V2
# Adapts to existing project structures and avoids duplication

set -e

# Configuration
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
PROJECT_DIR="$(pwd)"
TEMPLATE="${1:-default}"

# Global variables for template resolution
RESOLVED_TEMPLATE_PATH=""
TEMPLATE_ERROR=""

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
    echo -e "${BLUE}║         Agentic Flow Initialization                    ║${NC}"
    echo -e "${BLUE}║         Template: ${BOLD}$TEMPLATE                           ${NC}${BLUE}║${NC}"
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

# Resolve template using Chain of Responsibility pattern
# Checks local → global → default in priority order
# Sets RESOLVED_TEMPLATE_PATH on success, TEMPLATE_ERROR on failure
resolve_template() {
    local template_name="$1"

    # SECURITY: Prevent absolute paths (check first, before regex)
    if [[ "$template_name" == /* ]]; then
        TEMPLATE_ERROR="Invalid template name: absolute paths not allowed"
        return 1
    fi

    # SECURITY: Prevent path traversal attacks
    if [[ "$template_name" =~ [./] ]]; then
        TEMPLATE_ERROR="Invalid template name: contains path separators"
        return 1
    fi

    # Chain of Responsibility: local → global → default

    # 1. Check local: .claude/templates/{template_name}
    local local_template="$PROJECT_DIR/.claude/templates/$template_name"
    if [ -d "$local_template" ]; then
        RESOLVED_TEMPLATE_PATH="$local_template"
        return 0
    fi

    # 2. Check global: ~/.agentecflow/templates/{template_name}
    local global_template="$HOME/.agentecflow/templates/$template_name"
    if [ -d "$global_template" ]; then
        RESOLVED_TEMPLATE_PATH="$global_template"
        return 0
    fi

    # 3. Check default: CLAUDE_HOME/templates/{template_name}
    local default_template="$CLAUDE_HOME/templates/$template_name"
    if [ -d "$default_template" ]; then
        RESOLVED_TEMPLATE_PATH="$default_template"
        return 0
    fi

    # Template not found in any location
    TEMPLATE_ERROR="Template '$template_name' not found in any location"
    return 1
}

# Validate template structure
# Returns 0 (valid) or 1 (invalid), sets TEMPLATE_ERROR
validate_template() {
    local template_path="$1"

    # Check if directory exists
    if [ ! -d "$template_path" ]; then
        TEMPLATE_ERROR="Template directory does not exist: $template_path"
        return 1
    fi

    # Check for CLAUDE.md
    if [ ! -f "$template_path/CLAUDE.md" ]; then
        TEMPLATE_ERROR="Template missing CLAUDE.md: $template_path"
        return 1
    fi

    # Check for manifest.json (optional but recommended)
    if [ ! -f "$template_path/manifest.json" ]; then
        print_warning "Template missing manifest.json (recommended): $template_path"
    fi

    # Check for agents directory
    if [ ! -d "$template_path/agents" ]; then
        TEMPLATE_ERROR="Template missing agents/ directory: $template_path"
        return 1
    fi

    # Check for templates directory
    if [ ! -d "$template_path/templates" ]; then
        TEMPLATE_ERROR="Template missing templates/ directory: $template_path"
        return 1
    fi

    # Template is valid
    return 0
}

# List available templates from all sources
# Output: One template per line with source label
list_available_templates() {
    local templates=()
    local seen_names=()

    print_info "Available templates:"
    echo ""

    # Scan local templates (.claude/templates/)
    if [ -d "$PROJECT_DIR/.claude/templates" ]; then
        echo -e "${GREEN}Local templates (.claude/templates/):${NC}"
        for template_dir in "$PROJECT_DIR/.claude/templates"/*; do
            if [ -d "$template_dir" ]; then
                local name=$(basename "$template_dir")
                echo "  - $name [local]"
                seen_names+=("$name")
            fi
        done
        echo ""
    fi

    # Scan global templates (~/.agentecflow/templates/)
    if [ -d "$HOME/.agentecflow/templates" ]; then
        echo -e "${BLUE}Global templates (~/.agentecflow/templates/):${NC}"
        for template_dir in "$HOME/.agentecflow/templates"/*; do
            if [ -d "$template_dir" ]; then
                local name=$(basename "$template_dir")
                # Only show if not already seen in local
                if [[ ! " ${seen_names[@]} " =~ " ${name} " ]]; then
                    echo "  - $name [global]"
                    seen_names+=("$name")
                fi
            fi
        done
        echo ""
    fi

    # Scan default templates (CLAUDE_HOME/templates/)
    if [ -d "$CLAUDE_HOME/templates" ]; then
        echo -e "${YELLOW}Default templates (CLAUDE_HOME/templates/):${NC}"
        for template_dir in "$CLAUDE_HOME/templates"/*; do
            if [ -d "$template_dir" ]; then
                local name=$(basename "$template_dir")
                # Only show if not already seen
                if [[ ! " ${seen_names[@]} " =~ " ${name} " ]]; then
                    echo "  - $name [default]"
                fi
            fi
        done
        echo ""
    fi

    echo -e "${BLUE}Note: Local templates have priority over global, which have priority over default${NC}"
}

# Detect existing project type
detect_project_type() {
    # Check for .csproj files
    local csproj_files=$(ls *.csproj 2>/dev/null || ls */*.csproj 2>/dev/null || echo "")
    
    if [ -n "$csproj_files" ]; then
        # Check if it's a MAUI project
        if ls *.csproj 2>/dev/null | xargs grep -l "Microsoft.Maui" 2>/dev/null || \
           ls */*.csproj 2>/dev/null | xargs grep -l "Microsoft.Maui" 2>/dev/null; then
            echo "maui"
        elif ls *.csproj 2>/dev/null | xargs grep -l "Microsoft.AspNetCore" 2>/dev/null || \
             ls */*.csproj 2>/dev/null | xargs grep -l "Microsoft.AspNetCore" 2>/dev/null; then
            echo "dotnet-microservice"
        else
            echo "dotnet"
        fi
    elif [ -f "*.sln" ] || ls *.sln 2>/dev/null >/dev/null; then
        echo "dotnet-solution"
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
    elif [ -f "tsconfig.json" ] && [ -f "package.json" ]; then
        if grep -q "@nestjs" package.json; then
            echo "typescript-api"
        else
            echo "node"
        fi
    else
        echo "unknown"
    fi
}

# Check if global installation exists
check_global_installation() {
    if [ ! -d "$CLAUDE_HOME" ]; then
        print_error "Agentic Flow global installation not found at $CLAUDE_HOME"
        echo ""
        echo "Please install Agentic Flow globally first:"
        echo "  cd /path/to/ai-engineer/installer"
        echo "  ./install.sh"
        exit 1
    fi
    print_success "Found Agentic Flow installation at $CLAUDE_HOME"
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

# Smart structure creation based on project type
create_smart_structure() {
    local detected_type=$(detect_project_type)
    print_info "Detected project type: $detected_type"
    
    # Always create .claude at root
    mkdir -p .claude/{agents,commands,hooks,templates,stacks}

    # Always create docs at root
    mkdir -p docs/{requirements,bdd/features,adr,state}
    mkdir -p docs/requirements/{draft,approved,implemented}

    # Create task management structure
    mkdir -p tasks/{backlog,in_progress,in_review,blocked,completed}
    mkdir -p tasks/completed/{$(date +%Y-%m)}

    # Create project hierarchy structure
    mkdir -p epics/{active,archived}
    mkdir -p features/{active,archived}

    # Create portfolio tracking
    mkdir -p portfolio/{metrics,reports}
    
    # Handle test directory based on project type
    case "$detected_type" in
        maui|dotnet*)
            # .NET projects typically have test projects in solution
            print_info "Tests will be managed within .NET solution structure"
            ;;
        *)
            # Other projects benefit from separate test directories
            if [ ! -d "tests" ]; then
                mkdir -p tests/{unit,integration,e2e}
                print_success "Created test directories"
            else
                print_info "Using existing tests directory"
            fi
            ;;
    esac
    
    # Don't create src if project already has structure
    if [ "$detected_type" = "unknown" ] && [ ! -d "src" ]; then
        mkdir -p src
        print_info "Created src directory for new project"
    elif [ -d "src" ]; then
        print_info "Using existing src directory"
    else
        print_info "Project has existing structure, skipping src creation"
    fi
    
    print_success "Smart project structure created"
}

# Copy template files based on detected or specified template
copy_smart_template() {
    local detected_type=$(detect_project_type)
    local effective_template="$TEMPLATE"

    # Override template if we detected a specific type
    if [ "$TEMPLATE" = "default" ] && [ "$detected_type" != "unknown" ]; then
        case "$detected_type" in
            maui) effective_template="maui-appshell" ;;  # Default to AppShell for MAUI projects
            dotnet-microservice) effective_template="dotnet-microservice" ;;
            dotnet*) effective_template="dotnet-microservice" ;;
            react|vue) effective_template="react" ;;
            python) effective_template="python" ;;
            typescript-api) effective_template="typescript-api" ;;
            *) effective_template="default" ;;
        esac
        print_info "Auto-selected template: $effective_template"
    fi

    # Resolve template using Chain of Responsibility pattern
    if ! resolve_template "$effective_template"; then
        print_error "$TEMPLATE_ERROR"
        echo ""
        list_available_templates
        exit 1
    fi

    local template_dir="$RESOLVED_TEMPLATE_PATH"

    # Validate template structure
    if ! validate_template "$template_dir"; then
        print_error "$TEMPLATE_ERROR"
        echo ""
        print_info "Template validation failed. Please ensure the template has:"
        echo "  - CLAUDE.md (project context)"
        echo "  - agents/ directory (AI agents)"
        echo "  - templates/ directory (code templates)"
        echo "  - manifest.json (optional but recommended)"
        exit 1
    fi

    # Show resolved template source
    if [[ "$template_dir" == "$PROJECT_DIR/.claude/templates/"* ]]; then
        print_success "Using local template: $effective_template"
    elif [[ "$template_dir" == "$HOME/.agentecflow/templates/"* ]]; then
        print_success "Using global template: $effective_template"
    else
        print_success "Using default template: $effective_template"
    fi
    
    # Copy CLAUDE.md context file
    if [ -f "$template_dir/CLAUDE.md" ]; then
        cp "$template_dir/CLAUDE.md" .claude/
        print_success "Copied project context file for $effective_template"
    fi
    
    # Copy global agents first
    if [ -d "$CLAUDE_HOME/agents" ]; then
        cp -r "$CLAUDE_HOME/agents/"* .claude/agents/ 2>/dev/null || true
        print_success "Copied global AI agents"
    fi

    # Copy stack-specific agents
    if [ -d "$CLAUDE_HOME/stack-agents/$effective_template" ]; then
        cp -r "$CLAUDE_HOME/stack-agents/$effective_template/"* .claude/agents/ 2>/dev/null || true
        print_success "Copied $effective_template stack agents"
    elif [ -d "$template_dir/agents" ]; then
        cp -r "$template_dir/agents/"* .claude/agents/ 2>/dev/null || true
        print_success "Copied template AI agents"
    fi
    
    # Copy templates
    if [ -d "$template_dir/templates" ]; then
        cp -r "$template_dir/templates/"* .claude/templates/ 2>/dev/null || true
        print_success "Copied template files"
    fi
    
    # Link to global commands
    if [ -d "$CLAUDE_HOME/commands" ]; then
        for cmd in "$CLAUDE_HOME/commands"/*.md; do
            if [ -f "$cmd" ]; then
                local cmd_name=$(basename "$cmd")
                ln -sf "$cmd" ".claude/commands/$cmd_name" 2>/dev/null || \
                cp "$cmd" ".claude/commands/$cmd_name"
            fi
        done
        print_success "Linked Agentic Flow commands"
    fi
    
    TEMPLATE="$effective_template"  # Update global for later use
}

# Create project configuration
create_config() {
    print_info "Creating project configuration..."

    local project_name=$(basename "$PROJECT_DIR")
    local detected_type=$(detect_project_type)

    # Determine template source for metadata
    local template_source="default"
    if [[ "$RESOLVED_TEMPLATE_PATH" == "$PROJECT_DIR/.claude/templates/"* ]]; then
        template_source="local"
    elif [[ "$RESOLVED_TEMPLATE_PATH" == "$HOME/.agentecflow/templates/"* ]]; then
        template_source="global"
    fi

    cat > .claude/settings.json << EOF
{
  "version": "1.0.0",
  "extends": "$CLAUDE_HOME/templates/$TEMPLATE",
  "project": {
    "name": "$project_name",
    "template": "$TEMPLATE",
    "detected_type": "$detected_type",
    "created": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  },
  "template_metadata": {
    "name": "$TEMPLATE",
    "source": "$template_source",
    "source_path": "$RESOLVED_TEMPLATE_PATH",
    "initialized_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  },
  "methodology": {
    "requirements": "EARS",
    "testing": "BDD",
    "documentation": "ADR"
  },
  "structure": {
    "use_src_folder": $([ -d "src" ] && echo "true" || echo "false"),
    "test_location": "$([ "$detected_type" = "maui" ] || [ "$detected_type" = "dotnet-microservice" ] && echo "solution" || echo "root")"
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
- [ ] Set up Agentic Flow system
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

# ADR-001: Adopt Agentic Flow System

## Status
Accepted

## Context
We need a systematic approach to software development with clear requirements, automated testing, and quality gates.

## Decision
Adopt the Agentic Flow system with EARS requirements and BDD testing.

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

# Setup git hooks (if git repo)
setup_git_hooks() {
    if [ -d ".git" ]; then
        print_info "Setting up Git hooks..."
        
        # Create pre-commit hook
        cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Agentic Flow pre-commit hook

echo "Running pre-commit checks..."

# Check for draft requirements
if ls docs/requirements/draft/*.md 2>/dev/null | grep -q .; then
    echo "⚠️  Draft requirements found. Consider formalizing with /formalize-ears"
fi

# Run tests based on project type
if [ -f "*.csproj" ] || [ -f "*/*.csproj" ]; then
    dotnet test --no-build --verbosity quiet || exit 1
elif [ -f "package.json" ] && grep -q '"test"' package.json; then
    npm test -- --run --silent || exit 1
elif [ -f "pytest.ini" ] || [ -f "pyproject.toml" ]; then
    python -m pytest tests/unit -q || exit 1
fi

echo "✅ Pre-commit checks passed"
EOF
        
        chmod +x .git/hooks/pre-commit
        print_success "Git hooks configured"
    fi
}

# Create stack-specific files
create_stack_files() {
    local detected_type=$(detect_project_type)
    
    # Create stacks directory if it doesn't exist
    mkdir -p .claude/stacks
    
    case "$TEMPLATE" in
        react)
            print_info "Adding React-specific configuration..."
            cat > .claude/stacks/react.json << 'EOF'
{
  "name": "react",
  "testing": "vitest + playwright",
  "build": "vite",
  "language": "typescript"
}
EOF
            ;;
            
        python)
            print_info "Adding Python-specific configuration..."
            cat > .claude/stacks/python.json << 'EOF'
{
  "name": "python",
  "testing": "pytest",
  "framework": "fastapi",
  "language": "python3"
}
EOF
            ;;
            
        maui-appshell)
            print_info "Adding .NET MAUI AppShell-specific configuration..."
            cat > .claude/stacks/maui.json << 'EOF'
{
  "name": "maui-appshell",
  "testing": "xunit",
  "framework": "dotnet-maui",
  "language": "csharp",
  "target": "net8.0",
  "structure": "solution-based",
  "navigation": "appshell"
}
EOF
            ;;

        maui-navigationpage)
            print_info "Adding .NET MAUI NavigationPage-specific configuration..."
            cat > .claude/stacks/maui.json << 'EOF'
{
  "name": "maui-navigationpage",
  "testing": "xunit",
  "framework": "dotnet-maui",
  "language": "csharp",
  "target": "net8.0",
  "structure": "solution-based",
  "navigation": "navigationpage"
}
EOF
            ;;

        dotnet-microservice)
            print_info "Adding .NET Microservice-specific configuration..."
            cat > .claude/stacks/dotnet-microservice.json << 'EOF'
{
  "name": "dotnet-microservice",
  "testing": "xunit",
  "framework": "fastendpoints",
  "language": "csharp",
  "target": "net8.0",
  "structure": "solution-based"
}
EOF
            ;;

        typescript-api)
            print_info "Adding TypeScript API-specific configuration..."
            cat > .claude/stacks/typescript-api.json << 'EOF'
{
  "name": "typescript-api",
  "testing": "jest",
  "framework": "nestjs",
  "language": "typescript",
  "structure": "modular"
}
EOF
            ;;

        fullstack)
            print_info "Adding Full Stack-specific configuration..."
            cat > .claude/stacks/fullstack.json << 'EOF'
{
  "name": "fullstack",
  "testing": "vitest + pytest",
  "framework": "react + fastapi",
  "language": "typescript + python",
  "structure": "monorepo"
}
EOF
            ;;
    esac
}

# Print technology-specific next steps
print_tech_specific_steps() {
    local detected_type=$(detect_project_type)
    
    # Use the template if detection failed but template was specified
    if [ "$detected_type" = "unknown" ] && [ "$TEMPLATE" != "default" ]; then
        detected_type="$TEMPLATE"
    fi
    
    echo ""
    echo -e "${BOLD}Technology-Specific Setup:${NC}"
    
    case "$detected_type" in
        maui)
            echo ""
            echo -e "${YELLOW}For .NET MAUI Projects:${NC}"
            echo "1. Create your MAUI app (if not already done):"
            echo "   dotnet new maui -n YourApp"
            echo ""
            echo "2. Add test project:"
            echo "   dotnet new xunit -n YourApp.Tests"
            echo "   dotnet add YourApp.Tests reference YourApp"
            echo ""
            echo "3. Install required packages:"
            echo "   dotnet add package LanguageExt.Core"
            echo "   dotnet add package CommunityToolkit.Mvvm"
            echo ""
            ;;
            
        dotnet*)
            echo ""
            echo -e "${YELLOW}For .NET Microservice Projects:${NC}"
            echo "1. Create your API project (if not already done):"
            echo "   dotnet new webapi -n YourApi"
            echo ""
            echo "2. Add test project:"
            echo "   dotnet new xunit -n YourApi.Tests"
            echo ""
            echo "3. Install required packages:"
            echo "   dotnet add package FastEndpoints"
            echo "   dotnet add package LanguageExt.Core"
            echo ""
            ;;
            
        react)
            echo ""
            echo -e "${YELLOW}For React Projects:${NC}"
            echo "1. Your React app is already set up"
            echo ""
            echo "2. Ensure testing packages are installed:"
            echo "   npm install -D vitest @testing-library/react"
            echo "   npm install -D @playwright/test"
            echo ""
            ;;
            
        python)
            echo ""
            echo -e "${YELLOW}For Python Projects:${NC}"
            echo "1. Set up virtual environment:"
            echo "   python -m venv venv"
            echo "   source venv/bin/activate"
            echo ""
            echo "2. Install testing packages:"
            echo "   pip install pytest pytest-asyncio"
            echo ""
            ;;

        typescript-api)
            echo ""
            echo -e "${YELLOW}For TypeScript API Projects:${NC}"
            echo "1. Install dependencies (if not already done):"
            echo "   npm install"
            echo ""
            echo "2. Install testing packages:"
            echo "   npm install -D jest @types/jest ts-jest"
            echo "   npm install -D supertest @types/supertest"
            echo ""
            echo "3. Install recommended packages:"
            echo "   npm install class-validator class-transformer"
            echo ""
            ;;

        fullstack)
            echo ""
            echo -e "${YELLOW}For Full Stack Projects:${NC}"
            echo "1. Frontend setup (React):"
            echo "   cd frontend"
            echo "   npm install"
            echo "   npm install -D vitest @testing-library/react"
            echo ""
            echo "2. Backend setup (Python):"
            echo "   cd backend"
            echo "   python -m venv venv"
            echo "   source venv/bin/activate"
            echo "   pip install fastapi pytest"
            echo ""
            ;;
    esac
}

# Print next steps
print_next_steps() {
    local detected_type=$(detect_project_type)
    
    echo ""
    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✅ Agentic Flow successfully initialized!${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${BOLD}Project Structure:${NC}"
    echo "  .claude/       - Agentic Flow configuration (single location)"
    echo "  docs/          - All project documentation (single location)"
    echo "  tasks/         - Task management (backlog → in_progress → completed)"
    echo "  epics/         - Epic management (active, archived)"
    echo "  features/      - Feature management (active, archived)"
    echo "  portfolio/     - Portfolio metrics and reports"

    # Only show directories that actually exist and are relevant
    if [ -d "tests" ]; then
        echo "  tests/         - Test suites"
    fi

    if [ -d "src" ]; then
        echo "  src/           - Source code"
    fi
    
    # For .NET projects, mention the solution structure
    if [ "$detected_type" = "maui" ] || [ "$detected_type" = "dotnet-microservice" ] || [ "$detected_type" = "dotnet-solution" ] || [ "$TEMPLATE" = "maui-appshell" ] || [ "$TEMPLATE" = "maui-navigationpage" ] || [ "$TEMPLATE" = "dotnet-microservice" ]; then
        if ls *.sln 2>/dev/null >/dev/null; then
            echo "  *.sln          - .NET solution file"
        fi
        if ls *.csproj 2>/dev/null >/dev/null || ls */*.csproj 2>/dev/null >/dev/null; then
            echo "  *.csproj       - .NET project files"
        fi
    fi
    
    print_tech_specific_steps
    
    echo ""
    echo -e "${BOLD}Agentecflow Workflow:${NC}"
    echo ""
    echo "Stage 1: Requirements & Planning"
    echo -e "   ${BLUE}/gather-requirements${NC} - Interactive requirements session"
    echo -e "   ${BLUE}/formalize-ears${NC}     - Convert to EARS notation"
    echo -e "   ${BLUE}/epic-create${NC}        - Create epic with PM tool integration"
    echo ""
    echo "Stage 2: Feature & Task Definition"
    echo -e "   ${BLUE}/feature-create${NC}     - Create feature with epic linkage"
    echo -e "   ${BLUE}/generate-bdd${NC}       - Create test scenarios"
    echo -e "   ${BLUE}/task-create${NC}        - Create implementation tasks"
    echo ""
    echo "Stage 3: Engineering & Implementation"
    echo -e "   ${BLUE}/task-work${NC}          - Implement with automatic testing"
    echo -e "   ${BLUE}/task-status${NC}        - Monitor task progress"
    echo ""
    echo "Stage 4: Deployment & QA"
    echo -e "   ${BLUE}/task-complete${NC}      - Complete task with validation"
    echo -e "   ${BLUE}/hierarchy-view${NC}     - View project hierarchy"
    echo -e "   ${BLUE}/portfolio-dashboard${NC} - Executive overview"
    echo ""
    echo -e "${BLUE}📚 Documentation:${NC} docs/"
    echo -e "${BLUE}📋 Templates:${NC} .claude/templates/"
    echo -e "${BLUE}⚙️  Configuration:${NC} .claude/settings.json"
    echo ""
    echo -e "${BOLD}Important:${NC}"
    echo "• Single .claude directory at project root"
    echo "• Single docs directory for all documentation"
    echo "• Requirements flow: draft → approved → implemented"
}

# Main function
main() {
    print_header
    check_global_installation
    check_existing
    create_smart_structure
    copy_smart_template
    create_config
    create_initial_files
    setup_git_hooks
    create_stack_files
    print_next_steps
}

# Run main
main "$@"
