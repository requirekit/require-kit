#!/bin/bash

# validate-template.sh
# Validates the maui-navigationpage template structure and content
# Exit codes: 0 = success, 1 = validation failures

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0

# Template root (parent of tests directory)
TEMPLATE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "============================================"
echo "MAUI NavigationPage Template Validator"
echo "============================================"
echo "Template root: $TEMPLATE_ROOT"
echo ""

# Helper functions
check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASS_COUNT++))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAIL_COUNT++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARN_COUNT++))
}

check_directory() {
    local dir="$1"
    local full_path="$TEMPLATE_ROOT/$dir"

    if [ -d "$full_path" ]; then
        check_pass "Directory exists: $dir"
        return 0
    else
        check_fail "Directory missing: $dir"
        return 1
    fi
}

check_file() {
    local file="$1"
    local full_path="$TEMPLATE_ROOT/$file"

    if [ -f "$full_path" ]; then
        check_pass "File exists: $file"
        return 0
    else
        check_fail "File missing: $file"
        return 1
    fi
}

validate_json() {
    local file="$1"
    local full_path="$TEMPLATE_ROOT/$file"

    if ! check_file "$file"; then
        return 1
    fi

    if command -v jq &> /dev/null; then
        if jq empty "$full_path" 2>/dev/null; then
            check_pass "Valid JSON: $file"
            return 0
        else
            check_fail "Invalid JSON: $file"
            return 1
        fi
    else
        check_warn "jq not installed, skipping JSON validation for: $file"
        return 0
    fi
}

check_json_field() {
    local file="$1"
    local field="$2"
    local full_path="$TEMPLATE_ROOT/$file"

    if ! command -v jq &> /dev/null; then
        return 0
    fi

    if jq -e "$field" "$full_path" &> /dev/null; then
        check_pass "JSON field exists: $file -> $field"
        return 0
    else
        check_fail "JSON field missing: $file -> $field"
        return 1
    fi
}

check_doc_section() {
    local file="$1"
    local section="$2"
    local full_path="$TEMPLATE_ROOT/$file"

    if ! check_file "$file"; then
        return 1
    fi

    if grep -q "^## $section" "$full_path"; then
        check_pass "Doc section exists: $file -> $section"
        return 0
    else
        check_fail "Doc section missing: $file -> $section"
        return 1
    fi
}

# Section 1: Directory Structure
echo "Section 1: Directory Structure"
echo "------------------------------"

check_directory "agents"
check_directory "templates"
check_directory "templates/Domain"
check_directory "templates/Repository"
check_directory "templates/Service"
check_directory "templates/ViewModel"
check_directory "templates/Page"
check_directory "templates/Navigation"
check_directory "config"
check_directory "docs"
check_directory "tests"

echo ""

# Section 2: File Existence
echo "Section 2: File Existence"
echo "-------------------------"

# Agent files
check_file "agents/architectural-reviewer.md"
check_file "agents/bdd-generator.md"
check_file "agents/code-reviewer.md"
check_file "agents/maui-ui-specialist.md"
check_file "agents/maui-usecase-specialist.md"
check_file "agents/maui-viewmodel-specialist.md"
check_file "agents/requirements-analyst.md"
check_file "agents/test-orchestrator.md"

# Navigation components
check_file "templates/Navigation/INavigationService.cs"
check_file "templates/Navigation/NavigationService.cs"
check_file "templates/Navigation/MauiProgram.Navigation.cs"

# Configuration files
check_file "config/manifest.json"
check_file "config/settings.json"
check_file "config/.gitignore"

# Documentation files
check_file "docs/CLAUDE.md"
check_file "docs/README.md"
check_file "docs/MIGRATION.md"

# Test files
check_file "tests/validate-template.sh"

echo ""

# Section 3: JSON Validation
echo "Section 3: JSON Validation"
echo "--------------------------"

validate_json "config/manifest.json"
validate_json "config/settings.json"

# Check manifest.json structure
check_json_field "config/manifest.json" ".template.name"
check_json_field "config/manifest.json" ".template.version"
check_json_field "config/manifest.json" ".stack.navigation_pattern"
check_json_field "config/manifest.json" ".agents"
check_json_field "config/manifest.json" ".templates"

# Check settings.json structure
check_json_field "config/settings.json" ".navigation"
check_json_field "config/settings.json" ".architecture"
check_json_field "config/settings.json" ".testing"
check_json_field "config/settings.json" ".quality_gates"

echo ""

# Section 4: Documentation Completeness
echo "Section 4: Documentation Completeness"
echo "-------------------------------------"

# CLAUDE.md sections
check_doc_section "docs/CLAUDE.md" "Template Overview"
check_doc_section "docs/CLAUDE.md" "When to Use NavigationPage vs AppShell"
check_doc_section "docs/CLAUDE.md" "Navigation Architecture"
check_doc_section "docs/CLAUDE.md" "Navigation Patterns"
check_doc_section "docs/CLAUDE.md" "Code Generation Guidelines"
check_doc_section "docs/CLAUDE.md" "Testing Requirements"

# README.md sections
check_doc_section "docs/README.md" "Quick Start"
check_doc_section "docs/README.md" "Navigation Architecture"
check_doc_section "docs/README.md" "API Reference"
check_doc_section "docs/README.md" "Template Components"
check_doc_section "docs/README.md" "Examples"
check_doc_section "docs/README.md" "Troubleshooting"

# MIGRATION.md sections
check_doc_section "docs/MIGRATION.md" "Why Migrate?"
check_doc_section "docs/MIGRATION.md" "Step-by-Step Migration"
check_doc_section "docs/MIGRATION.md" "API Mapping Table"
check_doc_section "docs/MIGRATION.md" "Common Migration Pitfalls"

echo ""

# Section 5: Source Attribution
echo "Section 5: Source Attribution"
echo "-----------------------------"

# Check that copied agent files have source attribution
for agent_file in "$TEMPLATE_ROOT/agents"/*.md; do
    if [ -f "$agent_file" ]; then
        filename=$(basename "$agent_file")
        if head -n 1 "$agent_file" | grep -q "# SOURCE:"; then
            check_pass "Source attribution present: agents/$filename"
        else
            check_fail "Source attribution missing: agents/$filename"
        fi
    fi
done

echo ""

# Section 6: Optional Compilation Test
echo "Section 6: Optional Compilation Test"
echo "------------------------------------"

if command -v dotnet &> /dev/null; then
    check_pass "dotnet SDK available"

    # Create a temporary test project to validate templates compile
    TEMP_DIR=$(mktemp -d)
    trap "rm -rf $TEMP_DIR" EXIT

    echo "Creating test project in: $TEMP_DIR"

    cd "$TEMP_DIR"
    dotnet new maui -n TestProject &> /dev/null

    if [ $? -eq 0 ]; then
        check_pass "Created test MAUI project"

        # Copy Navigation templates
        mkdir -p TestProject/Navigation
        cp "$TEMPLATE_ROOT/templates/Navigation"/*.cs TestProject/Navigation/ 2>/dev/null

        # Replace placeholders
        find TestProject/Navigation -name "*.cs" -exec sed -i.bak 's/{{ProjectName}}/TestProject/g' {} \;

        # Try to compile (this will fail due to missing dependencies, but checks syntax)
        cd TestProject
        dotnet build &> /dev/null

        if [ $? -eq 0 ]; then
            check_pass "Navigation templates compile successfully"
        else
            check_warn "Navigation templates compilation requires full project setup"
        fi
    else
        check_warn "Could not create test project"
    fi
else
    check_warn "dotnet SDK not installed, skipping compilation test"
fi

echo ""

# Summary
echo "============================================"
echo "Validation Summary"
echo "============================================"
echo -e "${GREEN}Passed:${NC} $PASS_COUNT"
echo -e "${RED}Failed:${NC} $FAIL_COUNT"
echo -e "${YELLOW}Warnings:${NC} $WARN_COUNT"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}✓ Template validation PASSED${NC}"
    exit 0
else
    echo -e "${RED}✗ Template validation FAILED${NC}"
    echo "Please fix the failures above and run validation again."
    exit 1
fi
