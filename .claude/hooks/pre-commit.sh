#!/bin/bash

# Pre-commit hook for quality checks
# This runs before each commit to ensure code quality

set -e

echo "🔍 Running pre-commit checks..."

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Detect project type
detect_project_type() {
    if [ -f "package.json" ]; then
        echo "node"
    elif [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then
        echo "python"
    else
        echo "unknown"
    fi
}

PROJECT_TYPE=$(detect_project_type)

echo "📦 Detected project type: $PROJECT_TYPE"

# Run appropriate checks based on project type
case $PROJECT_TYPE in
    node)
        echo "🎨 Running formatters..."
        if command_exists npm; then
            npm run format:check 2>/dev/null || true
        fi

        echo "🔧 Running linters..."
        if command_exists npm; then
            npm run lint 2>/dev/null || true
        fi

        echo "📊 Running type checks..."
        if command_exists npm; then
            npm run type-check 2>/dev/null || true
        fi

        echo "🧪 Running unit tests..."
        if command_exists npm; then
            npm run test:unit 2>/dev/null || true
        fi
        ;;
        
    python)
        echo "🎨 Running formatters..."
        if command_exists black; then
            black --check src tests 2>/dev/null || true
        fi

        echo "🔧 Running linters..."
        if command_exists ruff; then
            ruff check . 2>/dev/null || true
        fi

        if command_exists mypy; then
            mypy src 2>/dev/null || true
        fi

        echo "🧪 Running unit tests..."
        if command_exists pytest; then
            pytest tests/unit -q 2>/dev/null || true
        fi
        ;;
        
    *)
        echo "⚠️  Unknown project type, skipping language-specific checks"
        ;;
esac

# Universal checks
echo "📝 Checking EARS requirements..."
if [ -d "docs/requirements" ]; then
    # Check for EARS compliance
    for file in docs/requirements/*.md; do
        if [ -f "$file" ]; then
            # Check for required EARS patterns
            if ! grep -q "When\|While\|If\|Where\|The.*shall" "$file"; then
                echo "⚠️  Warning: $file may not follow EARS notation"
            fi
        fi
    done
fi

echo "🎯 Checking BDD scenarios..."
if [ -d "docs/bdd/features" ]; then
    # Check for Gherkin syntax
    for file in docs/bdd/features/*.feature; do
        if [ -f "$file" ]; then
            # Check for basic Gherkin structure
            if ! grep -q "Feature:\|Scenario:" "$file"; then
                echo "⚠️  Warning: $file may not be a valid feature file"
            fi
        fi
    done
fi

echo "📊 Checking quality gates..."
# Check coverage if available
if [ -f "coverage/coverage-summary.json" ]; then
    # Extract coverage percentage (simplified check)
    if command_exists jq; then
        coverage=$(jq '.total.lines.pct' coverage/coverage-summary.json)
        if (( $(echo "$coverage < 80" | bc -l) )); then
            echo "⚠️  Warning: Code coverage is below 80% ($coverage%)"
        fi
    fi
fi

echo "✅ Pre-commit checks completed!"

# Note: This hook doesn't block commits, it just warns
# To make it blocking, remove "|| true" from commands and handle exit codes
exit 0
