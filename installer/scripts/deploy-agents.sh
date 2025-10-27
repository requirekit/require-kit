#!/bin/bash

# Deploy Agents Script
# Deploys specialized agents from development to production locations

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "🚀 Deploying Specialized Agents..."

# Function to deploy agents
deploy_agents() {
    local source_dir="$1"
    local target_dir="$2"
    local agent_type="$3"
    
    if [ -d "$source_dir" ]; then
        echo "  📦 Deploying $agent_type agents..."
        mkdir -p "$target_dir"
        cp -f "$source_dir"/*.md "$target_dir/" 2>/dev/null || true
        echo "  ✅ $agent_type agents deployed"
    else
        echo "  ⚠️  $agent_type source directory not found"
    fi
}

# Deploy stack-specific agents
deploy_agents \
    "$PROJECT_ROOT/tasks/agent-enhancement-implementation/agents/dotnet" \
    "$PROJECT_ROOT/installer/global/templates/dotnet-microservice/agents" \
    ".NET Microservice"

deploy_agents \
    "$PROJECT_ROOT/tasks/agent-enhancement-implementation/agents/maui" \
    "$PROJECT_ROOT/installer/global/templates/maui/agents" \
    "MAUI"

deploy_agents \
    "$PROJECT_ROOT/tasks/agent-enhancement-implementation/agents/react" \
    "$PROJECT_ROOT/installer/global/templates/react/agents" \
    "React"

deploy_agents \
    "$PROJECT_ROOT/tasks/agent-enhancement-implementation/agents/python" \
    "$PROJECT_ROOT/installer/global/templates/python/agents" \
    "Python"

# Deploy global agents
deploy_agents \
    "$PROJECT_ROOT/tasks/agent-enhancement-implementation/agents/global" \
    "$PROJECT_ROOT/installer/global/agents" \
    "Global Specialist"

echo ""
echo "✨ Agent deployment complete!"
echo ""
echo "Deployed agents summary:"
echo "  - .NET Microservice: $(ls -1 "$PROJECT_ROOT/installer/global/templates/dotnet-microservice/agents"/*.md 2>/dev/null | wc -l) agents"
echo "  - MAUI: $(ls -1 "$PROJECT_ROOT/installer/global/templates/maui/agents"/*.md 2>/dev/null | wc -l) agents"
echo "  - React: $(ls -1 "$PROJECT_ROOT/installer/global/templates/react/agents"/*.md 2>/dev/null | wc -l) agents"
echo "  - Python: $(ls -1 "$PROJECT_ROOT/installer/global/templates/python/agents"/*.md 2>/dev/null | wc -l) agents"
echo "  - Global: $(ls -1 "$PROJECT_ROOT/installer/global/agents"/*.md 2>/dev/null | wc -l) agents"