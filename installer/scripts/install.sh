#!/bin/bash

# Agentecflow - Global Installation Script
# Creates the complete ~/.agentecflow structure matching production setup

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Installation configuration
AGENTECFLOW_VERSION="2.0.0"
INSTALL_DIR="$HOME/.agentecflow"
CONFIG_DIR="$HOME/.config/agentecflow"
INSTALLER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Test mode configuration
TEST_MODE=false
if [ "$1" = "--test-mode" ]; then
    TEST_MODE=true
    print_info "Running in test mode"
fi

# Function to print colored messages
print_message() {
    local color=$1
    shift
    echo -e "${color}$@${NC}"
}

print_header() {
    echo ""
    print_message "$BLUE" "╔════════════════════════════════════════════════════════╗"
    print_message "$BLUE" "║         Agentecflow Installation System                ║"
    print_message "$BLUE" "║         Version: $AGENTECFLOW_VERSION                  ║"
    print_message "$BLUE" "╚════════════════════════════════════════════════════════╝"
    echo ""
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

# Detect project context by finding .claude/ directory
# Sets PROJECT_ROOT if found
# Returns 0 (found) or 1 (not found)
detect_project_context() {
    local current_dir="$PWD"
    local max_depth=10
    local depth=0

    while [ "$depth" -lt "$max_depth" ]; do
        if [ -d "$current_dir/.claude" ]; then
            PROJECT_ROOT="$current_dir"
            return 0
        fi

        # Stop at filesystem root
        if [ "$current_dir" = "/" ]; then
            break
        fi

        # Move up one directory
        current_dir="$(dirname "$current_dir")"
        depth=$((depth + 1))
    done

    # Not found
    PROJECT_ROOT=""
    return 1
}

# Check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."
    
    local missing_deps=()
    
    # Check for required commands
    for cmd in git curl bash; do
        if ! command -v $cmd &> /dev/null; then
            missing_deps+=($cmd)
        fi
    done
    
    # Check for Node.js (optional but recommended)
    if ! command -v node &> /dev/null; then
        print_warning "Node.js not found. Some features may be limited."
    else
        print_success "Node.js found: $(node --version)"
    fi
    
    # Check for Python (REQUIRED for complexity evaluation and task splitting)
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is REQUIRED for complexity evaluation and task splitting features"
        print_info "Agentecflow requires Python 3.7+ for core functionality"
        print_info "Please install Python 3.7 or higher and try again"
        missing_deps+=("python3")
    else
        # Check Python version
        python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
        python_major=$(echo $python_version | cut -d. -f1)
        python_minor=$(echo $python_version | cut -d. -f2)

        if [ "$python_major" -lt 3 ] || ([ "$python_major" -eq 3 ] && [ "$python_minor" -lt 7 ]); then
            print_error "Python 3.7+ is required (found: Python $python_version)"
            print_info "Please upgrade Python to version 3.7 or higher"
            print_info "Complexity evaluation features require Python 3.7+ standard library"
            missing_deps+=("python3.7+")
        else
            print_success "Python found: Python $python_version (>= 3.7 required)"

            # Check for pip (needed for Jinja2 and python-frontmatter)
            if ! command -v pip3 &> /dev/null; then
                print_warning "pip3 not found - Python packages (Jinja2, python-frontmatter) may need manual installation"
                print_info "Install with: python3 -m ensurepip or use your package manager"
            else
                print_success "pip3 found - can install Python dependencies"

                # Check if Jinja2 and python-frontmatter are installed
                python3 -c "import jinja2" 2>/dev/null
                if [ $? -ne 0 ]; then
                    print_info "Installing Jinja2 (required for plan markdown rendering)..."
                    pip3 install -q Jinja2 || print_warning "Failed to install Jinja2 - install manually with: pip3 install Jinja2"
                fi

                python3 -c "import frontmatter" 2>/dev/null
                if [ $? -ne 0 ]; then
                    print_info "Installing python-frontmatter (required for plan metadata)..."
                    pip3 install -q python-frontmatter || print_warning "Failed to install python-frontmatter - install manually with: pip3 install python-frontmatter"
                fi
            fi
        fi
    fi
    
    if [ ${#missing_deps[@]} -gt 0 ]; then
        print_error "Missing required dependencies: ${missing_deps[*]}"
        print_info "Please install missing dependencies and try again."
        exit 1
    fi
    
    print_success "All required prerequisites met"
}

# Backup existing installation
backup_existing() {
    # Check for any existing installations
    local existing_dirs=()

    [ -d "$HOME/.agentecflow" ] && existing_dirs+=(".agentecflow")
    [ -d "$HOME/.agenticflow" ] && existing_dirs+=(".agenticflow")
    [ -d "$HOME/.agentic-flow" ] && existing_dirs+=(".agentic-flow")
    [ -d "$HOME/.claude" ] && existing_dirs+=(".claude")
    
    if [ ${#existing_dirs[@]} -gt 0 ]; then
        print_warning "Found existing installations: ${existing_dirs[*]}"
        
        for dir in "${existing_dirs[@]}"; do
            local full_path="$HOME/$dir"
            local backup_dir="${full_path}.backup.$(date +%Y%m%d_%H%M%S)"
            print_info "Creating backup of $dir at $backup_dir"
            mv "$full_path" "$backup_dir"
            print_success "Backup created: $backup_dir"
        done
    fi
}

# Create complete directory structure matching Product Owner's setup
create_directories() {
    print_info "Creating complete directory structure..."
    
    # Create all directories that Product Owner has
    mkdir -p "$INSTALL_DIR"/{agents,bin,cache,commands,completions,docs,instructions,plugins,scripts,templates,versions}

    # Create project management directories
    mkdir -p "$INSTALL_DIR/project-templates"/{epics,features,tasks,portfolio}
    
    # Create sub-directories for instructions
    mkdir -p "$INSTALL_DIR/instructions"/{core,stacks}
    
    # Create sub-directories for templates
    mkdir -p "$INSTALL_DIR/templates"/{default,react,python,maui,dotnet-microservice,fullstack,typescript-api}
    
    # Create versions structure
    mkdir -p "$INSTALL_DIR/versions/$AGENTICFLOW_VERSION"
    
    # Create config directory
    mkdir -p "$CONFIG_DIR"
    
    print_success "Complete directory structure created"
}

# Copy and organize global files
install_global_files() {
    print_info "Installing global files..."
    
    # Copy instructions
    if [ -d "$INSTALLER_DIR/global/instructions" ]; then
        cp -r "$INSTALLER_DIR/global/instructions/"* "$INSTALL_DIR/instructions/" 2>/dev/null || true
        print_success "Installed methodology instructions"
    fi
    
    # Copy templates with complete structure
    if [ -d "$INSTALLER_DIR/global/templates" ]; then
        for template_dir in "$INSTALLER_DIR/global/templates"/*; do
            if [ -d "$template_dir" ]; then
                local template_name=$(basename "$template_dir")
                cp -r "$template_dir" "$INSTALL_DIR/templates/" 2>/dev/null || true
                
                # Ensure each template has agents directory
                mkdir -p "$INSTALL_DIR/templates/$template_name/agents"
            fi
        done
        print_success "Installed project templates"
    fi
    
    # Copy commands
    if [ -d "$INSTALLER_DIR/global/commands" ]; then
        # Copy markdown command files
        find "$INSTALLER_DIR/global/commands" -maxdepth 1 -name "*.md" -exec cp {} "$INSTALL_DIR/commands/" \; 2>/dev/null || true

        # Copy lib directory (excluding test files, cache, and artifacts)
        if [ -d "$INSTALLER_DIR/global/commands/lib" ]; then
            mkdir -p "$INSTALL_DIR/commands/lib"

            # Copy Python production files only (exclude test_*, cache, coverage)
            find "$INSTALLER_DIR/global/commands/lib" \
                -maxdepth 1 \
                -type f \
                -name "*.py" \
                ! -name "test_*" \
                ! -name "*_test.py" \
                -exec cp {} "$INSTALL_DIR/commands/lib/" \; 2>/dev/null || true

            # Copy documentation files (README, API docs)
            find "$INSTALLER_DIR/global/commands/lib" \
                -maxdepth 1 \
                -type f \
                -name "*.md" \
                ! -name "TASK-*.md" \
                -exec cp {} "$INSTALL_DIR/commands/lib/" \; 2>/dev/null || true

            # Copy templates directory (for Jinja2 templates)
            if [ -d "$INSTALLER_DIR/global/commands/lib/templates" ]; then
                cp -r "$INSTALLER_DIR/global/commands/lib/templates" "$INSTALL_DIR/commands/lib/" 2>/dev/null || true
                print_success "Installed Jinja2 templates for plan rendering"
            fi

            # Count installed Python files
            local python_count=$(ls -1 "$INSTALL_DIR/commands/lib/"*.py 2>/dev/null | wc -l)
            print_success "Installed commands with lib ($python_count Python modules, production only)"
        else
            print_success "Installed commands"
        fi
    fi
    
    # Copy documentation
    if [ -d "$INSTALLER_DIR/global/docs" ]; then
        cp -r "$INSTALLER_DIR/global/docs/"* "$INSTALL_DIR/docs/" 2>/dev/null || true
        print_success "Installed documentation"
    fi
    
    # Copy the initialization script
    if [ -f "$INSTALLER_DIR/scripts/init-claude-project.sh" ]; then
        cp "$INSTALLER_DIR/scripts/init-claude-project.sh" "$INSTALL_DIR/scripts/init-project.sh"
        chmod +x "$INSTALL_DIR/scripts/init-project.sh"
        print_success "Installed initialization script"
    fi
    
    print_success "Global files installed"
}

# Install global agents (comprehensive agent ecosystem)
install_global_agents() {
    print_info "Installing global AI agents..."

    # Install core global agents first
    if [ -d "$INSTALLER_DIR/global/agents" ] && [ "$(ls -A $INSTALLER_DIR/global/agents)" ]; then
        cp -r "$INSTALLER_DIR/global/agents/"* "$INSTALL_DIR/agents/" 2>/dev/null || true
        print_success "Installed core global agents"
    fi

    # Install stack-specific agents to global location for template copying
    for template_dir in "$INSTALLER_DIR/global/templates"/*; do
        if [ -d "$template_dir/agents" ] && [ "$(ls -A $template_dir/agents)" ]; then
            local template_name=$(basename "$template_dir")
            mkdir -p "$INSTALL_DIR/stack-agents/$template_name"
            cp -r "$template_dir/agents/"* "$INSTALL_DIR/stack-agents/$template_name/" 2>/dev/null || true
            print_success "Installed $template_name stack agents"
        fi
    done

    # Count total agents
    local global_agent_count=$(ls -1 "$INSTALL_DIR/agents/"*.md 2>/dev/null | wc -l)
    local stack_agent_count=$(find "$INSTALL_DIR/stack-agents" -name "*.md" 2>/dev/null | wc -l)
    local total_agents=$((global_agent_count + stack_agent_count))

    if [ $total_agents -gt 0 ]; then
        print_success "Installed $total_agents total agents ($global_agent_count global + $stack_agent_count stack-specific)"

        # List the global agents
        if [ $global_agent_count -gt 0 ]; then
            echo "  Global agents:"
            for agent in "$INSTALL_DIR/agents/"*.md; do
                if [ -f "$agent" ]; then
                    echo "    - $(basename "$agent" .md)"
                fi
            done
        fi
    else
        print_warning "No agents found to install"
        print_info "Creating placeholder agents..."
        
        # Create the 4 core agents as placeholders if they don't exist
        cat > "$INSTALL_DIR/agents/requirements-analyst.md" << 'EOF'
---
name: requirements-analyst
description: Specialist in gathering and formalizing requirements using EARS notation
tools: Read, Write, Search
model: sonnet
---

You are a requirements engineering specialist focused on EARS notation.

## Your Responsibilities
1. Gather requirements through structured Q&A
2. Formalize requirements using EARS patterns
3. Validate completeness and clarity
4. Maintain traceability

## EARS Patterns
- Ubiquitous: "The [system] shall [behavior]"
- Event-driven: "When [trigger], the [system] shall [response]"
- State-driven: "While [condition], the [system] shall [behavior]"
- Unwanted: "If [error], then the [system] shall [recovery]"
- Optional: "Where [feature], the [system] shall [behavior]"
EOF

        cat > "$INSTALL_DIR/agents/bdd-generator.md" << 'EOF'
---
name: bdd-generator
description: Converts EARS requirements to BDD/Gherkin scenarios
tools: Read, Write, Generate
model: sonnet
---

You are a BDD specialist who converts EARS requirements to Gherkin scenarios.

## Your Responsibilities
1. Analyze EARS requirements
2. Generate comprehensive BDD scenarios
3. Ensure testability
4. Maintain requirement traceability

## Gherkin Format
Feature: [Feature Name]
  Scenario: [Scenario Description]
    Given [initial context]
    When [action or event]
    Then [expected outcome]
EOF

        cat > "$INSTALL_DIR/agents/code-reviewer.md" << 'EOF'
---
name: code-reviewer
description: Reviews code for quality, standards, and best practices
tools: Read, Analyze, Comment
model: sonnet
---

You are a code quality specialist focused on standards and best practices.

## Your Responsibilities
1. Review code changes for quality
2. Check adherence to patterns
3. Validate test coverage
4. Ensure documentation
EOF

        cat > "$INSTALL_DIR/agents/test-orchestrator.md" << 'EOF'
---
name: test-orchestrator
description: Manages test execution and quality gates
tools: Execute, Analyze, Report
model: sonnet
---

You are a test orchestration specialist managing quality gates.

## Your Responsibilities
1. Determine which tests to run
2. Execute test suites
3. Validate quality gates
4. Generate test reports
EOF
        
        print_success "Created core placeholder agents"
    fi

    # Create stack-agents directory structure even if no agents
    mkdir -p "$INSTALL_DIR/stack-agents"/{default,react,python,maui,dotnet-microservice,fullstack,typescript-api}
}

# Create the main CLI executables
create_cli_commands() {
    print_info "Creating CLI commands..."
    
    # Create agentec-init command (primary command)
    cat > "$INSTALL_DIR/bin/agentec-init" << 'EOF'
#!/bin/bash

# Agentecflow Project Initialization
# Primary command for initializing projects

AGENTECFLOW_HOME="$HOME/.agentecflow"
PROJECT_DIR="$(pwd)"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_help() {
    echo "Agentecflow Project Initialization"
    echo ""
    echo "Usage: agentec-init [template]"
    echo ""
    echo "Templates:"
    echo "  default             - Language-agnostic template"
    echo "  react               - React with TypeScript"
    echo "  python              - Python with FastAPI"
    echo "  maui                - .NET MAUI mobile app"
    echo "  dotnet-microservice - .NET microservice with FastEndpoints"
    echo "  fullstack           - React + Python"
    echo "  typescript-api      - NestJS TypeScript backend API"
    echo ""
    echo "Examples:"
    echo "  agentec-init                    # Interactive setup"
    echo "  agentec-init react              # Initialize with React template"
    echo "  agentec-init dotnet-microservice # Initialize with .NET microservice"
}

if [ "$1" = "help" ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    print_help
    exit 0
fi

# Check if Agentecflow is installed
if [ ! -d "$AGENTECFLOW_HOME" ]; then
    echo -e "${RED}Error: Agentecflow not installed at $AGENTECFLOW_HOME${NC}"
    echo "Please run the installer first"
    exit 1
fi

# Run the initialization script
if [ -f "$AGENTECFLOW_HOME/scripts/init-project.sh" ]; then
    # Set environment variable for the init script
    export CLAUDE_HOME="$AGENTECFLOW_HOME"
    exec "$AGENTECFLOW_HOME/scripts/init-project.sh" "$@"
else
    echo -e "${RED}Error: Initialization script not found${NC}"
    echo "Looking for: $AGENTECFLOW_HOME/scripts/init-project.sh"
    exit 1
fi
EOF

    chmod +x "$INSTALL_DIR/bin/agentec-init"
    print_success "Created agentec-init command"

    # Create agentecflow main command
    cat > "$INSTALL_DIR/bin/agentecflow" << 'EOF'
#!/bin/bash

# Agentecflow CLI
# Main command-line interface for Agentecflow

AGENTECFLOW_HOME="$HOME/.agentecflow"
AGENTECFLOW_VERSION="1.0.0"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_help() {
    echo "Agentecflow - AI-Powered Software Engineering Lifecycle System"
    echo ""
    echo "Usage: agentecflow <command> [options]"
    echo ""
    echo "Commands:"
    echo "  init [template]     Initialize Agentecflow in current directory"
    echo "  doctor              Check system health and configuration"
    echo "  version             Show version information"
    echo "  help                Show this help message"
    echo ""
    echo "Examples:"
    echo "  agentecflow init                    # Interactive initialization"
    echo "  agentecflow init react              # Initialize with React template"
    echo "  agentecflow init dotnet-microservice # Initialize with .NET microservice"
    echo "  agentecflow doctor                  # Check installation health"
}

# Detect project context by traversing upward
detect_project_context() {
    local current_dir="$PWD"
    local max_depth=10
    local depth=0

    while [ "$depth" -lt "$max_depth" ]; do
        if [ -d "$current_dir/.claude" ]; then
            PROJECT_ROOT="$current_dir"
            return 0
        fi
        if [ "$current_dir" = "/" ]; then
            return 1
        fi
        current_dir="$(dirname "$current_dir")"
        depth=$((depth + 1))
    done
    return 1
}

case "$1" in
    init)
        shift
        export CLAUDE_HOME="$AGENTECFLOW_HOME"
        exec "$AGENTECFLOW_HOME/bin/agentec-init" "$@"
        ;;
    doctor)
        echo -e "${BLUE}Running Agentecflow diagnostics...${NC}"
        echo ""

        # Check installation
        echo "Installation:"
        if [ -d "$AGENTECFLOW_HOME" ]; then
            echo -e "  ${GREEN}✓${NC} Agentecflow home: $AGENTECFLOW_HOME"

            # Check key directories
            for dir in agents bin cache commands completions docs instructions plugins scripts templates versions; do
                if [ -d "$AGENTECFLOW_HOME/$dir" ]; then
                    echo -e "  ${GREEN}✓${NC} Directory $dir exists"
                else
                    echo -e "  ${RED}✗${NC} Directory $dir missing"
                fi
            done
        else
            echo -e "  ${RED}✗${NC} Agentecflow home not found"
        fi

        # Check agents
        echo ""
        echo "AI Agents:"
        if [ -d "$AGENTECFLOW_HOME/agents" ]; then
            agent_count=$(ls -1 "$AGENTECFLOW_HOME/agents/"*.md 2>/dev/null | wc -l)
            if [ "$agent_count" -ge 4 ]; then
                echo -e "  ${GREEN}✓${NC} $agent_count agents installed"
            else
                echo -e "  ${YELLOW}⚠${NC} Only $agent_count agents found (expected 4+)"
            fi
        fi

        # Check PATH
        echo ""
        echo "PATH Configuration:"
        if [[ ":$PATH:" == *":$AGENTECFLOW_HOME/bin:"* ]]; then
            echo -e "  ${GREEN}✓${NC} Agentecflow bin in PATH"
        else
            echo -e "  ${YELLOW}⚠${NC} Add to PATH: export PATH=\"\$HOME/.agentecflow/bin:\$PATH\""
        fi

        # Check Claude Code integration
        echo ""
        echo "Claude Code Integration:"
        if [ -L "$HOME/.claude/commands" ]; then
            target=$(readlink "$HOME/.claude/commands")
            if [ "$target" = "$AGENTECFLOW_HOME/commands" ]; then
                echo -e "  ${GREEN}✓${NC} Commands symlinked correctly"
            else
                echo -e "  ${YELLOW}⚠${NC} Commands symlinked to unexpected location: $target"
            fi
        elif [ -d "$HOME/.claude/commands" ]; then
            echo -e "  ${YELLOW}⚠${NC} Commands directory exists but is not symlinked"
            echo -e "      Run installer again to create symlink"
        else
            echo -e "  ${RED}✗${NC} Commands not configured for Claude Code"
        fi

        if [ -L "$HOME/.claude/agents" ]; then
            target=$(readlink "$HOME/.claude/agents")
            if [ "$target" = "$AGENTECFLOW_HOME/agents" ]; then
                echo -e "  ${GREEN}✓${NC} Agents symlinked correctly"
            else
                echo -e "  ${YELLOW}⚠${NC} Agents symlinked to unexpected location: $target"
            fi
        elif [ -d "$HOME/.claude/agents" ]; then
            echo -e "  ${YELLOW}⚠${NC} Agents directory exists but is not symlinked"
            echo -e "      Run installer again to create symlink"
        else
            echo -e "  ${RED}✗${NC} Agents not configured for Claude Code"
        fi

        if [ -L "$HOME/.claude/commands" ] && [ -L "$HOME/.claude/agents" ]; then
            echo -e "  ${GREEN}✓${NC} Compatible with Conductor.build for parallel development"
        fi

        # Check for local project templates
        echo ""
        echo "Local Templates:"
        PROJECT_ROOT=""
        if detect_project_context; then
            echo -e "  ${GREEN}✓${NC} Project context found: $PROJECT_ROOT"

            if [ -d "$PROJECT_ROOT/.claude/templates" ]; then
                local_template_count=$(ls -1d "$PROJECT_ROOT/.claude/templates"/*/ 2>/dev/null | wc -l)
                if [ "$local_template_count" -gt 0 ]; then
                    echo -e "  ${GREEN}✓${NC} $local_template_count local templates available"
                    echo ""
                    echo "  Available local templates:"
                    for template_dir in "$PROJECT_ROOT/.claude/templates"/*; do
                        if [ -d "$template_dir" ]; then
                            name=$(basename "$template_dir")
                            # Validate template structure
                            valid="${GREEN}✓${NC}"
                            status="valid"
                            if [ ! -f "$template_dir/CLAUDE.md" ]; then
                                valid="${RED}✗${NC}"
                                status="missing CLAUDE.md"
                            elif [ ! -d "$template_dir/agents" ]; then
                                valid="${RED}✗${NC}"
                                status="missing agents/"
                            elif [ ! -d "$template_dir/templates" ]; then
                                valid="${RED}✗${NC}"
                                status="missing templates/"
                            fi
                            echo -e "    $valid $name ($status)"
                        fi
                    done
                else
                    echo -e "  ${YELLOW}⚠${NC} No local templates found"
                fi
            else
                echo -e "  ${YELLOW}⚠${NC} No .claude/templates/ directory"
            fi

            echo ""
            echo "  Template resolution order:"
            echo "    1. Local (.claude/templates/) [HIGHEST PRIORITY]"
            echo "    2. Global (~/.agentecflow/templates/)"
            echo "    3. Default (CLAUDE_HOME/templates/) [LOWEST PRIORITY]"
        else
            echo -e "  ${BLUE}ℹ${NC} Not in a project directory"
            echo -e "      Run this command from a project initialized with agentec-init"
        fi
        ;;
    version|--version|-v)
        echo "Agentecflow version $AGENTECFLOW_VERSION"
        echo "Installation: $AGENTECFLOW_HOME"
        ;;
    help|--help|-h|"")
        print_help
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        echo "Run 'agentecflow help' for usage information"
        exit 1
        ;;
esac
EOF

    chmod +x "$INSTALL_DIR/bin/agentecflow"

    # Create shorthand aliases
    ln -sf "$INSTALL_DIR/bin/agentecflow" "$INSTALL_DIR/bin/af"
    ln -sf "$INSTALL_DIR/bin/agentec-init" "$INSTALL_DIR/bin/ai"

    print_success "Created CLI commands (agentecflow, agentec-init, af, ai)"
}

# Setup shell integration
setup_shell_integration() {
    print_info "Setting up shell integration..."

    local shell_config=""
    local shell_name=""

    # Enhanced shell detection
    if [ -n "$ZSH_VERSION" ] || [ -n "$ZSH_NAME" ] || [ "$SHELL" = "/bin/zsh" ] || [ "$SHELL" = "/usr/bin/zsh" ]; then
        shell_name="zsh"
        shell_config="$HOME/.zshrc"
        print_info "Detected zsh shell"
    elif [ -n "$BASH_VERSION" ] || [ "$SHELL" = "/bin/bash" ] || [ "$SHELL" = "/usr/bin/bash" ]; then
        shell_name="bash"
        print_info "Detected bash shell"
        if [ -f "$HOME/.bashrc" ]; then
            shell_config="$HOME/.bashrc"
        elif [ -f "$HOME/.bash_profile" ]; then
            shell_config="$HOME/.bash_profile"
        elif [ "$(uname)" = "Darwin" ]; then
            # macOS defaults to .bash_profile
            shell_config="$HOME/.bash_profile"
        else
            # Linux defaults to .bashrc
            shell_config="$HOME/.bashrc"
        fi
    else
        # Try to detect from SHELL environment variable
        case "$SHELL" in
            */zsh)
                shell_name="zsh"
                shell_config="$HOME/.zshrc"
                print_info "Detected zsh from SHELL variable"
                ;;
            */bash)
                shell_name="bash"
                shell_config="$HOME/.bashrc"
                print_info "Detected bash from SHELL variable"
                ;;
            *)
                shell_name="unknown"
                print_warning "Unknown shell: $SHELL"
                ;;
        esac
    fi
    
    if [ -z "$shell_config" ]; then
        print_warning "Could not detect shell configuration file"
        print_info "Please add the following to your shell configuration manually:"
        echo "    export PATH=\"\$HOME/.agentecflow/bin:\$PATH\""
        echo "    export AGENTECFLOW_HOME=\"\$HOME/.agentecflow\""
        return
    fi

    # Remove old configurations if they exist
    if grep -q "\.agenticflow\|\.agentic-flow\|\.claude\|CLAUDE_HOME\|AGENTIC_FLOW_HOME\|AGENTICFLOW_HOME" "$shell_config" 2>/dev/null; then
        print_info "Removing old Agentecflow configurations..."
        # Create backup
        cp "$shell_config" "$shell_config.backup.$(date +%Y%m%d_%H%M%S)"

        # Use sed to remove entire configuration blocks (comments + code + fi)
        # This prevents orphaned 'fi' statements
        sed -i.bak '/# Agentic Flow/,/^fi$/d; /# Agentecflow/,/^fi$/d' "$shell_config" 2>/dev/null || \
        sed -i '' '/# Agentic Flow/,/^fi$/d; /# Agentecflow/,/^fi$/d' "$shell_config" 2>/dev/null || \
        {
            # Fallback: Remove individual lines but also check for orphaned fi
            grep -v "\.agenticflow\|\.agentic-flow\|\.claude\|CLAUDE_HOME\|AGENTIC_FLOW_HOME\|AGENTICFLOW_HOME" "$shell_config" > "$shell_config.tmp"
            # Remove orphaned 'fi' that appears after removed 'if' statements
            awk '
                /^# Agentic Flow/ { in_block=1; next }
                /^# Agentecflow/ { in_block=1; next }
                in_block && /^fi$/ { in_block=0; next }
                !in_block { print }
            ' "$shell_config.tmp" > "$shell_config.tmp2"
            mv "$shell_config.tmp2" "$shell_config"
            rm -f "$shell_config.tmp"
        }
    fi

    # Check if already configured correctly
    if grep -q "\.agentecflow/bin" "$shell_config" 2>/dev/null; then
        print_info "Shell integration already configured"
        return
    fi

    # Add to shell configuration
    cat >> "$shell_config" << 'EOF'

# Agentecflow
export PATH="$HOME/.agentecflow/bin:$PATH"
export AGENTECFLOW_HOME="$HOME/.agentecflow"

# Agentecflow completions (if available)
if [ -f "$HOME/.agentecflow/completions/agentecflow.bash" ]; then
    source "$HOME/.agentecflow/completions/agentecflow.bash"
fi
EOF
    
    print_success "Shell integration added to $shell_config"
    print_info "Please restart your shell or run: source $shell_config"
}

# Create global configuration
create_global_config() {
    print_info "Creating global configuration..."
    
    cat > "$CONFIG_DIR/config.json" << EOF
{
  "version": "$AGENTICFLOW_VERSION",
  "installation": {
    "home": "$INSTALL_DIR",
    "installed": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  },
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
  },
  "agents": {
    "core": [
      "requirements-analyst",
      "bdd-generator",
      "code-reviewer",
      "test-orchestrator"
    ]
  },
  "plugins": {
    "auto_discover": true,
    "directories": [
      "~/.agentecflow/plugins"
    ]
  }
}
EOF

    print_success "Global configuration created"
}

# Install completion scripts
install_completions() {
    print_info "Installing shell completions..."

    # Bash completion
    cat > "$INSTALL_DIR/completions/agentecflow.bash" << 'EOF'
# Bash completion for agentecflow and agentec-init

# Helper function to list all available templates dynamically
_list_all_templates() {
    local templates=()
    local agentecflow_home="$HOME/.agentecflow"

    # Add local templates if in a project
    local current_dir="$PWD"
    local max_depth=10
    local depth=0
    while [ "$depth" -lt "$max_depth" ]; do
        if [ -d "$current_dir/.claude/templates" ]; then
            for template_dir in "$current_dir/.claude/templates"/*; do
                if [ -d "$template_dir" ]; then
                    templates+=("$(basename "$template_dir")")
                fi
            done
            break
        fi
        if [ "$current_dir" = "/" ]; then
            break
        fi
        current_dir="$(dirname "$current_dir")"
        depth=$((depth + 1))
    done

    # Add global templates
    if [ -d "$agentecflow_home/templates" ]; then
        for template_dir in "$agentecflow_home/templates"/*; do
            if [ -d "$template_dir" ]; then
                local name=$(basename "$template_dir")
                # Add only if not already in list (avoid duplicates)
                if [[ ! " ${templates[@]} " =~ " ${name} " ]]; then
                    templates+=("$name")
                fi
            fi
        done
    fi

    echo "${templates[@]}"
}

_agentecflow() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="init doctor version help"

    case "${prev}" in
        agentecflow|af)
            COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
            return 0
            ;;
        init|agentec-init|ai)
            local templates=$(_list_all_templates)
            COMPREPLY=( $(compgen -W "${templates}" -- ${cur}) )
            return 0
            ;;
    esac
}

_agentec_init() {
    local cur templates
    cur="${COMP_WORDS[COMP_CWORD]}"
    templates=$(_list_all_templates)
    COMPREPLY=( $(compgen -W "${templates}" -- ${cur}) )
}

complete -F _agentecflow agentecflow
complete -F _agentecflow af
complete -F _agentec_init agentec-init
complete -F _agentec_init ai
EOF
    
    print_success "Shell completions installed"
}

# Create version management
create_version_management() {
    print_info "Setting up version management..."
    
    # Create version file
    echo "$AGENTICFLOW_VERSION" > "$INSTALL_DIR/versions/current"
    
    # Create symlink to current version
    ln -sf "$AGENTICFLOW_VERSION" "$INSTALL_DIR/versions/latest"
    
    # Create version info file
    cat > "$INSTALL_DIR/versions/$AGENTICFLOW_VERSION/info.json" << EOF
{
  "version": "$AGENTICFLOW_VERSION",
  "released": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "features": [
    "EARS requirements notation",
    "BDD/Gherkin generation",
    "Epic/Feature/Task hierarchy",
    "Portfolio management",
    "PM tool integration",
    "Quality gates",
    "Test orchestration",
    "10+ core AI agents",
    "7 project templates",
    "Agentecflow Stage 1-4 support"
  ]
}
EOF
    
    print_success "Version management configured"
}

# Create cache directories
setup_cache() {
    print_info "Setting up cache directories..."
    
    mkdir -p "$INSTALL_DIR/cache"/{responses,artifacts,sessions}
    
    # Create cache config
    cat > "$INSTALL_DIR/cache/config.json" << 'EOF'
{
  "max_size_mb": 100,
  "ttl_hours": 24,
  "auto_clean": true
}
EOF
    
    print_success "Cache directories created"
}

# Final summary
print_summary() {
    echo ""
    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✅ Agentecflow installation complete!${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${BOLD}Installation Summary:${NC}"
    echo "  📁 Home Directory: $INSTALL_DIR"
    echo "  🔧 Configuration: $CONFIG_DIR"
    echo "  📦 Version: $AGENTECFLOW_VERSION"
    echo ""
    echo -e "${BOLD}Installed Components:${NC}"
    
    # Count components
    local agent_count=$(ls -1 "$INSTALL_DIR/agents/"*.md 2>/dev/null | wc -l)
    local template_count=$(ls -1d "$INSTALL_DIR/templates"/*/ 2>/dev/null | wc -l)
    local command_count=$(ls -1 "$INSTALL_DIR/commands/"*.md 2>/dev/null | wc -l)
    
    echo "  🤖 AI Agents: $agent_count"
    echo "  📋 Templates: $template_count"
    echo "  ⚡ Commands: $command_count"
    echo ""
    echo -e "${BOLD}Available Commands:${NC}"
    echo "  • agentec-init [template]  - Initialize a project"
    echo "  • agentecflow init         - Alternative initialization"
    echo "  • agentecflow doctor       - Check system health"
    echo "  • af                       - Short for agentecflow"
    echo "  • ai                       - Short for agentec-init"
    echo ""
    echo -e "${BOLD}Available Templates:${NC}"
    for template in "$INSTALL_DIR/templates"/*/; do
        if [ -d "$template" ]; then
            local name=$(basename "$template")
            case "$name" in
                default)
                    echo "  • $name - Language-agnostic"
                    ;;
                react)
                    echo "  • $name - React with TypeScript"
                    ;;
                python)
                    echo "  • $name - Python with FastAPI"
                    ;;
                maui)
                    echo "  • $name - .NET MAUI mobile app"
                    ;;
                dotnet-microservice)
                    echo "  • $name - .NET microservice with FastEndpoints"
                    ;;
                fullstack)
                    echo "  • $name - React + Python"
                    ;;
                typescript-api)
                    echo "  • $name - NestJS TypeScript backend API"
                    ;;
                *)
                    echo "  • $name"
                    ;;
            esac
        fi
    done
    echo ""
    echo -e "${BOLD}Claude Code Integration:${NC}"
    if [ -L "$HOME/.claude/commands" ] && [ -L "$HOME/.claude/agents" ]; then
        echo -e "  ${GREEN}✓${NC} Commands available in Claude Code (via symlink)"
        echo -e "  ${GREEN}✓${NC} Agents available in Claude Code (via symlink)"
        echo -e "  ${GREEN}✓${NC} Compatible with Conductor.build for parallel development"
    else
        echo -e "  ${YELLOW}⚠${NC} Claude Code integration not configured"
    fi
    echo ""
    echo -e "${YELLOW}⚠ Next Steps:${NC}"
    echo "  1. Restart your shell or run: source ~/.bashrc (or ~/.zshrc)"
    echo "  2. Navigate to your project directory"
    echo "  3. Run: agentec-init dotnet-microservice"
    echo "  4. (Optional) Install Conductor.build for parallel development"
    echo ""
    echo -e "${BLUE}📚 Documentation: $INSTALL_DIR/docs/${NC}"
    echo -e "${BLUE}❓ Check health: agentecflow doctor${NC}"
    echo -e "${BLUE}🔗 Conductor: https://conductor.build${NC}"
}

# Setup Claude Code integration (for Conductor compatibility)
setup_claude_integration() {
    print_info "Setting up Claude Code integration..."

    # Ensure ~/.claude exists
    if [ ! -d "$HOME/.claude" ]; then
        mkdir -p "$HOME/.claude"
        print_success "Created ~/.claude directory"
    fi

    # Handle existing commands directory
    if [ -d "$HOME/.claude/commands" ] && [ ! -L "$HOME/.claude/commands" ]; then
        local backup_dir="$HOME/.claude/commands.backup.$(date +%Y%m%d_%H%M%S)"
        mv "$HOME/.claude/commands" "$backup_dir"
        print_warning "Backed up existing commands to $backup_dir"
    elif [ -L "$HOME/.claude/commands" ]; then
        rm "$HOME/.claude/commands"
        print_info "Removed existing commands symlink"
    fi

    # Handle existing agents directory
    if [ -d "$HOME/.claude/agents" ] && [ ! -L "$HOME/.claude/agents" ]; then
        local backup_dir="$HOME/.claude/agents.backup.$(date +%Y%m%d_%H%M%S)"
        mv "$HOME/.claude/agents" "$backup_dir"
        print_warning "Backed up existing agents to $backup_dir"
    elif [ -L "$HOME/.claude/agents" ]; then
        rm "$HOME/.claude/agents"
        print_info "Removed existing agents symlink"
    fi

    # Create symlinks
    ln -sf "$INSTALL_DIR/commands" "$HOME/.claude/commands"
    ln -sf "$INSTALL_DIR/agents" "$HOME/.claude/agents"

    # Verify symlinks
    if [ -L "$HOME/.claude/commands" ] && [ -L "$HOME/.claude/agents" ]; then
        print_success "Claude Code integration configured successfully"
        print_info "  Commands: ~/.claude/commands → ~/.agentecflow/commands"
        print_info "  Agents: ~/.claude/agents → ~/.agentecflow/agents"
        echo ""
        print_success "All agentecflow commands now available in Claude Code!"
        print_info "Compatible with Conductor.build for parallel development"
    else
        print_error "Failed to create symlinks for Claude Code integration"
        print_warning "Commands and agents may not be available in Claude Code"
    fi
}

# Main installation
main() {
    print_header

    print_info "Installing Agentecflow to $INSTALL_DIR"
    echo ""

    # Run installation steps
    check_prerequisites
    backup_existing
    create_directories
    install_global_files
    install_global_agents
    create_cli_commands
    setup_shell_integration
    create_global_config
    install_completions
    create_version_management
    setup_cache
    setup_claude_integration

    # Print summary
    print_summary
}

# Run main installation
main "$@"
