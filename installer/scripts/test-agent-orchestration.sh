#!/bin/bash

# Test Agent Orchestration
# Verifies that specialized agents are properly integrated and accessible

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "🧪 Testing Agent Orchestration..."
echo ""

# Function to test agent availability
test_agent() {
    local agent_file="$1"
    local agent_name="$2"
    
    if [ -f "$agent_file" ]; then
        # Check if agent has required sections (YAML frontmatter and content)
        if grep -q "^---$" "$agent_file" && \
           grep -q "^name:" "$agent_file" && \
           grep -q "^description:" "$agent_file" && \
           grep -q "## Core Expertise" "$agent_file"; then
            echo "  ✅ $agent_name - Valid structure"
        else
            echo "  ⚠️  $agent_name - Missing required sections"
            return 1
        fi
    else
        echo "  ❌ $agent_name - Not found"
        return 1
    fi
}

# Test .NET Microservice agents
echo "📦 Testing .NET Microservice Agents:"
test_agent "$PROJECT_ROOT/installer/global/templates/dotnet-microservice/agents/dotnet-api-specialist.md" "API Specialist"
test_agent "$PROJECT_ROOT/installer/global/templates/dotnet-microservice/agents/dotnet-domain-specialist.md" "Domain Specialist"
test_agent "$PROJECT_ROOT/installer/global/templates/dotnet-microservice/agents/dotnet-testing-specialist.md" "Testing Specialist"
echo ""

# Test MAUI agents
echo "📱 Testing MAUI Agents:"
test_agent "$PROJECT_ROOT/installer/global/templates/maui/agents/maui-usecase-specialist.md" "UseCase Specialist"
test_agent "$PROJECT_ROOT/installer/global/templates/maui/agents/maui-viewmodel-specialist.md" "ViewModel Specialist"
test_agent "$PROJECT_ROOT/installer/global/templates/maui/agents/maui-ui-specialist.md" "UI Specialist"
echo ""

# Test React agents
echo "⚛️  Testing React Agents:"
test_agent "$PROJECT_ROOT/installer/global/templates/react/agents/react-state-specialist.md" "State Specialist"
test_agent "$PROJECT_ROOT/installer/global/templates/react/agents/react-testing-specialist.md" "Testing Specialist"
echo ""

# Test Global agents
echo "🌍 Testing Global Specialist Agents:"
test_agent "$PROJECT_ROOT/installer/global/agents/devops-specialist.md" "DevOps Specialist"
test_agent "$PROJECT_ROOT/installer/global/agents/security-specialist.md" "Security Specialist"
test_agent "$PROJECT_ROOT/installer/global/agents/database-specialist.md" "Database Specialist"
echo ""

# Test orchestration patterns
echo "🎭 Testing Orchestration Patterns:"

# Check if agents have collaboration points
echo "  Checking collaboration points..."
if grep -q "collaborates_with:" "$PROJECT_ROOT/installer/global/agents/devops-specialist.md"; then
    echo "  ✅ Global agents have collaboration metadata"
else
    echo "  ⚠️  Missing collaboration metadata in global agents"
fi

if grep -q "orchestration:" "$PROJECT_ROOT/installer/global/templates/dotnet-microservice/agents/dotnet-api-specialist.md"; then
    echo "  ✅ Stack agents have orchestration metadata"
else
    echo "  ⚠️  Missing orchestration metadata in stack agents"
fi

echo ""
echo "✨ Agent orchestration test complete!"