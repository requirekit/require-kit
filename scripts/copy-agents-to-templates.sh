#!/bin/bash

# Script to copy agents to all templates
# This ensures all templates have the same base agents

set -e

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
AI_ENGINEER_DIR="$(dirname "$SCRIPT_DIR")"
TEMPLATES_DIR="$AI_ENGINEER_DIR/installer/global/templates"
SOURCE_AGENTS_DIR="$AI_ENGINEER_DIR/.claude/agents"

echo "Copying agents to all templates..."

# List of templates to update
TEMPLATES=("default" "dotnet-microservice" "python" "react")

for template in "${TEMPLATES[@]}"; do
    TEMPLATE_DIR="$TEMPLATES_DIR/$template"
    if [ -d "$TEMPLATE_DIR" ]; then
        echo "Processing template: $template"
        
        # Create agents directory if it doesn't exist
        mkdir -p "$TEMPLATE_DIR/agents"
        
        # Copy all agent files
        if [ -d "$SOURCE_AGENTS_DIR" ]; then
            cp -r "$SOURCE_AGENTS_DIR"/*.md "$TEMPLATE_DIR/agents/" 2>/dev/null || true
            echo "  ✓ Copied agents to $template"
        fi
    else
        echo "  ⚠ Template directory not found: $template"
    fi
done

echo ""
echo "✅ Agents successfully copied to all templates!"
echo ""
echo "Templates updated:"
for template in "${TEMPLATES[@]}"; do
    if [ -d "$TEMPLATES_DIR/$template/agents" ]; then
        agent_count=$(ls -1 "$TEMPLATES_DIR/$template/agents"/*.md 2>/dev/null | wc -l)
        echo "  • $template: $agent_count agents"
    fi
done
