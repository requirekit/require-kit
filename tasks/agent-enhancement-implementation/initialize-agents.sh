#!/bin/bash
# Enhanced initialization script for AI-Engineer with agent orchestration

# Function to initialize a project with stack-specific agents
initialize_stack() {
    local stack=$1
    local project_path=$2
    
    echo "🤖 Initializing $stack stack with specialized agents..."
    
    # Create agent directories
    mkdir -p "$project_path/.claude/agents"
    mkdir -p "$project_path/.claude/methodology"
    
    # Copy global agents
    echo "📋 Copying global agents..."
    if [ -d ~/.ai-engineer/agents/global ]; then
        cp -r ~/.ai-engineer/agents/global/* "$project_path/.claude/agents/"
    fi
    
    # Copy stack-specific agents
    echo "🔧 Copying $stack-specific agents..."
    if [ -d ~/.ai-engineer/agents/stacks/$stack ]; then
        cp -r ~/.ai-engineer/agents/stacks/$stack/* "$project_path/.claude/agents/"
    fi
    
    # Copy orchestration guide
    echo "📚 Setting up orchestration..."
    cp ~/.ai-engineer/methodology/05-agent-orchestration.md \
       "$project_path/.claude/methodology/"
    
    # Update CLAUDE.md with agent references
    echo "📝 Updating CLAUDE.md..."
    cat >> "$project_path/.claude/CLAUDE.md" << 'EOF'

## Agent Orchestration Strategy

This project uses specialized agents for different aspects of development.
See `.claude/methodology/05-agent-orchestration.md` for complete orchestration patterns.

### Available Agents
EOF
    
    # Add stack-specific agent list
    case $stack in
        python)
            cat >> "$project_path/.claude/CLAUDE.md" << 'EOF'
- Python API Specialist (@python-api-specialist)
- Python LangChain Specialist (@python-langchain-specialist)
- Python Testing Specialist (@python-testing-specialist)
EOF
            ;;
        react)
            cat >> "$project_path/.claude/CLAUDE.md" << 'EOF'
- React Component Specialist (@react-component-specialist)
- React State Specialist (@react-state-specialist)
- React Testing Specialist (@react-testing-specialist)
EOF
            ;;
        dotnet-microservice)
            cat >> "$project_path/.claude/CLAUDE.md" << 'EOF'
- .NET API Specialist (@dotnet-api-specialist)
- .NET Domain Specialist (@dotnet-domain-specialist)
- .NET Testing Specialist (@dotnet-testing-specialist)
EOF
            ;;
        maui)
            cat >> "$project_path/.claude/CLAUDE.md" << 'EOF'
- MAUI UseCase Specialist (@maui-usecase-specialist)
- MAUI ViewModel Specialist (@maui-viewmodel-specialist)
- MAUI UI Specialist (@maui-ui-specialist)
EOF
            ;;
    esac
    
    # Add global agents
    cat >> "$project_path/.claude/CLAUDE.md" << 'EOF'

### Global Specialists
- Requirements Analyst (@requirements-analyst)
- Software Architect (@software-architect)
- QA Tester (@qa-tester)
- Code Reviewer (@code-reviewer)
- DevOps Specialist (@devops-specialist)
- Security Specialist (@security-specialist)
- Database Specialist (@database-specialist)

### Automatic Agent Selection
The system automatically selects appropriate agents based on file types and task context.
Refer to `.claude/methodology/05-agent-orchestration.md` for routing rules.
EOF
    
    # Update settings.json
    update_agent_registry "$project_path" "$stack"
    
    echo "✅ Agent initialization complete!"
}

# Function to update agent registry in settings.json
update_agent_registry() {
    local project_path=$1
    local stack=$2
    
    echo "⚙️ Updating settings.json..."
    
    # Create settings.json if it doesn't exist
    if [ ! -f "$project_path/.claude/settings.json" ]; then
        echo '{}' > "$project_path/.claude/settings.json"
    fi
    
    # Add orchestration configuration using a Python script for JSON manipulation
    python3 << EOF
import json
import os

settings_path = "$project_path/.claude/settings.json"

# Read existing settings
with open(settings_path, 'r') as f:
    settings = json.load(f)

# Add orchestration configuration
orchestration_config = {
    "enabled": True,
    "rules_file": "methodology/05-agent-orchestration.md",
    "stack": "$stack",
    "auto_select": {
        "enabled": True,
        "by_file_extension": {},
        "by_task_type": {}
    },
    "quality_gates": {
        "code_quality": {"enabled": True},
        "testing": {"enabled": True, "coverage_threshold": 80},
        "documentation": {"enabled": True},
        "security": {"enabled": True}
    }
}

# Add stack-specific file mappings
if "$stack" == "python":
    orchestration_config["auto_select"]["by_file_extension"][".py"] = {
        "primary": "python-api-specialist",
        "testing": "python-testing-specialist",
        "ai": "python-langchain-specialist"
    }
elif "$stack" == "react":
    orchestration_config["auto_select"]["by_file_extension"][".tsx"] = {
        "primary": "react-component-specialist",
        "state": "react-state-specialist",
        "testing": "react-testing-specialist"
    }
elif "$stack" == "dotnet-microservice":
    orchestration_config["auto_select"]["by_file_extension"][".cs"] = {
        "primary": "dotnet-api-specialist",
        "domain": "dotnet-domain-specialist",
        "testing": "dotnet-testing-specialist"
    }
elif "$stack" == "maui":
    orchestration_config["auto_select"]["by_file_extension"][".xaml"] = {
        "primary": "maui-ui-specialist",
        "viewmodel": "maui-viewmodel-specialist",
        "testing": "qa-tester"
    }

settings["agent_orchestration"] = orchestration_config

# Write updated settings
with open(settings_path, 'w') as f:
    json.dump(settings, f, indent=2)

print("Settings updated successfully!")
EOF
}

# Function to list available agents
list_agents() {
    local project_path=$1
    
    echo "📋 Available Agents in this project:"
    echo ""
    
    if [ -d "$project_path/.claude/agents" ]; then
        echo "Global Agents:"
        for agent in "$project_path/.claude/agents"/*.md; do
            if [ -f "$agent" ]; then
                basename "$agent" .md | sed 's/^/  - @/'
            fi
        done
    fi
    
    echo ""
    echo "Use '@agent-name' to engage a specific agent"
    echo "See .claude/methodology/05-agent-orchestration.md for orchestration patterns"
}

# Main script logic
case "$1" in
    init)
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo "Usage: $0 init <stack> <project_path>"
            echo "Stacks: python, react, dotnet-microservice, maui"
            exit 1
        fi
        initialize_stack "$2" "$3"
        ;;
    list)
        if [ -z "$2" ]; then
            echo "Usage: $0 list <project_path>"
            exit 1
        fi
        list_agents "$2"
        ;;
    *)
        echo "AI-Engineer Agent Initialization Script"
        echo ""
        echo "Usage:"
        echo "  $0 init <stack> <project_path>  - Initialize project with agents"
        echo "  $0 list <project_path>           - List available agents"
        echo ""
        echo "Available stacks:"
        echo "  - python             (FastAPI, LangChain, pytest)"
        echo "  - react              (React, TypeScript, RTL)"
        echo "  - dotnet-microservice (.NET, FastEndpoints, xUnit)"
        echo "  - maui               (MAUI, MVVM, UseCase pattern)"
        ;;
esac
