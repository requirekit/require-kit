#!/bin/bash

# Fix agents in all templates
# Copy from MAUI template which already has all agents

set -e

TEMPLATES_DIR="/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/templates"
SOURCE_DIR="$TEMPLATES_DIR/maui/agents"

# Ensure source exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source agents directory not found at $SOURCE_DIR"
    exit 1
fi

echo "Copying agents from MAUI template to all other templates..."

# Copy to default template
if [ -d "$TEMPLATES_DIR/default" ]; then
    cp -r "$SOURCE_DIR"/*.md "$TEMPLATES_DIR/default/agents/" 2>/dev/null || true
    echo "✓ Copied to default template"
fi

# Copy to dotnet-microservice template
if [ -d "$TEMPLATES_DIR/dotnet-microservice" ]; then
    cp -r "$SOURCE_DIR"/*.md "$TEMPLATES_DIR/dotnet-microservice/agents/" 2>/dev/null || true
    echo "✓ Copied to dotnet-microservice template"
fi

# Copy to python template
if [ -d "$TEMPLATES_DIR/python" ]; then
    cp -r "$SOURCE_DIR"/*.md "$TEMPLATES_DIR/python/agents/" 2>/dev/null || true
    echo "✓ Copied to python template"
fi

# Copy to react template
if [ -d "$TEMPLATES_DIR/react" ]; then
    cp -r "$SOURCE_DIR"/*.md "$TEMPLATES_DIR/react/agents/" 2>/dev/null || true
    echo "✓ Copied to react template"
fi

echo ""
echo "✅ Agents successfully distributed to all templates!"
echo ""

# Verify
echo "Verification:"
for template in default dotnet-microservice python react maui; do
    if [ -d "$TEMPLATES_DIR/$template/agents" ]; then
        count=$(ls -1 "$TEMPLATES_DIR/$template/agents"/*.md 2>/dev/null | wc -l | tr -d ' ')
        echo "  • $template: $count agents"
    else
        echo "  • $template: No agents directory"
    fi
done
