#!/bin/bash

# Script to update agentecflow → agentecflow branding
# Product name: Agentecflow
# Directory: ~/.agentecflow
# Commands: agentecflow, agentec-init

set -e

echo "🔄 Updating branding from 'agentecflow' to 'agentecflow'..."
echo ""

# Files to update (excluding node_modules, .git, etc.)
find_files() {
    find . -type f \( \
        -name "*.md" -o \
        -name "*.sh" -o \
        -name "*.json" -o \
        -name "*.py" \
    \) \
    ! -path "*/node_modules/*" \
    ! -path "*/.git/*" \
    ! -path "*/venv/*" \
    ! -path "*/.venv/*" \
    ! -path "*/build/*" \
    ! -path "*/dist/*"
}

# Create backup
echo "📦 Creating backup..."
BACKUP_DIR="backup-branding-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
find_files | while read file; do
    mkdir -p "$BACKUP_DIR/$(dirname "$file")"
    cp "$file" "$BACKUP_DIR/$file" 2>/dev/null || true
done
echo "✓ Backup created at: $BACKUP_DIR"
echo ""

# Replacements to make:
# 1. agentecflow → agentecflow (command name)
# 2. agentec-init → agentec-init (command name)
# 3. ~/.agentecflow → ~/.agentecflow (directory)
# 4. AGENTECFLOW → AGENTECFLOW (environment variable)
# 5. Agentecflow → Agentecflow (product name in text)
# 6. agentecflow.bash → agentecflow.bash (completion file)

echo "🔧 Updating files..."

# Update all markdown, shell, json, and python files
find_files | while read file; do
    if [ -f "$file" ]; then
        # Create temporary file
        temp_file="${file}.tmp"

        # Perform replacements
        sed \
            -e 's/agentecflow init/agentecflow init/g' \
            -e 's/agentecflow doctor/agentecflow doctor/g' \
            -e 's/agentecflow --help/agentecflow --help/g' \
            -e 's/agentecflow help/agentecflow help/g' \
            -e 's/agentecflow version/agentecflow version/g' \
            -e 's/agentecflow\([^e]\)/agentecflow\1/g' \
            -e 's/agentec-init/agentec-init/g' \
            -e 's/\.agentecflow/.agentecflow/g' \
            -e 's/AGENTECFLOW/AGENTECFLOW/g' \
            -e 's/Agentecflow/Agentecflow/g' \
            -e 's/agentecflow\.bash/agentecflow.bash/g' \
            "$file" > "$temp_file"

        # Replace original file if changes were made
        if ! cmp -s "$file" "$temp_file"; then
            mv "$temp_file" "$file"
            echo "  Updated: $file"
        else
            rm "$temp_file"
        fi
    fi
done

echo ""
echo "✅ Branding update complete!"
echo ""
echo "📊 Summary of changes:"
echo "  Product name: Agentecflow"
echo "  Directory: ~/.agentecflow"
echo "  Commands: agentecflow, agentec-init"
echo ""
echo "🔍 To verify, run:"
echo "  grep -r 'agentecflow' --include='*.md' --include='*.sh' | grep -v backup"
echo ""
echo "💾 Backup location: $BACKUP_DIR"
