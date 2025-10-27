#!/bin/bash

# State synchronization hook
# Synchronizes project state across different tracking systems

set -e

echo "🔄 Synchronizing project state..."

# Configuration
STATE_DIR="docs/state"
SPRINT_FILE="$STATE_DIR/current-sprint.md"
BACKLOG_FILE="$STATE_DIR/product-backlog.md"
CHANGELOG_FILE="$STATE_DIR/changelog.md"

# Ensure state directory exists
mkdir -p "$STATE_DIR"

# Function to extract value from markdown
extract_md_value() {
    local file=$1
    local pattern=$2
    grep -E "$pattern" "$file" 2>/dev/null | head -1 | sed 's/.*: //'
}

# Function to count completed tasks
count_completed_tasks() {
    local file=$1
    grep -c "^\- \[x\]" "$file" 2>/dev/null || echo 0
}

# Function to count total tasks
count_total_tasks() {
    local file=$1
    grep -c "^\- \[.\]" "$file" 2>/dev/null || echo 0
}

# Initialize sprint file if not exists
if [ ! -f "$SPRINT_FILE" ]; then
    cat > "$SPRINT_FILE" <<EOF
---
sprint: 1
start: $(date +%Y-%m-%d)
end: $(date -d "+14 days" +%Y-%m-%d 2>/dev/null || date +%Y-%m-%d)
velocity: 0
status: planning
---

# Sprint 1

## Overview
- **Sprint Goal**: [Define sprint goal]
- **Progress**: 0% [░░░░░░░░░░]
- **Velocity**: 0/0 points

## Tasks
<!-- Add tasks here -->

## Quality Gates
| Gate | Status | Current | Target |
|------|--------|---------|--------|
| Coverage | ⏳ | 0% | 80% |
| Tests | ⏳ | - | Pass |
| EARS | ⏳ | 0% | 100% |
EOF
    echo "📝 Created new sprint file"
fi

# Initialize backlog file if not exists
if [ ! -f "$BACKLOG_FILE" ]; then
    cat > "$BACKLOG_FILE" <<EOF
# Product Backlog

## Ready for Development
| ID | Title | Points | Priority |
|----|-------|--------|----------|

## In Progress
| ID | Title | Assignee | Progress |
|----|-------|----------|----------|

## Completed
| ID | Title | Points | Date |
|----|-------|--------|------|
EOF
    echo "📝 Created new backlog file"
fi

# Initialize changelog if not exists
if [ ! -f "$CHANGELOG_FILE" ]; then
    cat > "$CHANGELOG_FILE" <<EOF
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- Initial project setup

### Changed

### Fixed

### Removed
EOF
    echo "📝 Created new changelog file"
fi

# Calculate sprint progress
if [ -f "$SPRINT_FILE" ]; then
    completed=$(count_completed_tasks "$SPRINT_FILE")
    total=$(count_total_tasks "$SPRINT_FILE")
    
    if [ "$total" -gt 0 ]; then
        progress=$((completed * 100 / total))
        
        # Create progress bar
        bar_length=10
        filled=$((progress * bar_length / 100))
        empty=$((bar_length - filled))
        progress_bar=""
        
        for i in $(seq 1 $filled); do
            progress_bar="${progress_bar}█"
        done
        for i in $(seq 1 $empty); do
            progress_bar="${progress_bar}░"
        done
        
        # Update progress in file
        sed -i.bak "s/Progress: .*\[.*\]/Progress: ${progress}% [${progress_bar}]/" "$SPRINT_FILE"
        sed -i.bak "s/Velocity: .* points/Velocity: ${completed}\/${total} points/" "$SPRINT_FILE"
        
        echo "📊 Sprint Progress: ${progress}% (${completed}/${total} tasks)"
    fi
fi

# Sync with Git commits
if command -v git >/dev/null 2>&1 && [ -d .git ]; then
    # Check for task references in recent commits
    recent_commits=$(git log --oneline -10 2>/dev/null || echo "")
    
    if [ -n "$recent_commits" ]; then
        echo "📝 Recent commits:"
        echo "$recent_commits" | head -5
        
        # Extract task IDs from commits
        task_ids=$(echo "$recent_commits" | grep -oE "TASK-[0-9]+" | sort -u)
        
        if [ -n "$task_ids" ]; then
            echo "📌 Tasks referenced in commits:"
            echo "$task_ids"
        fi
    fi
fi

# Check quality metrics
echo ""
echo "📊 Quality Metrics:"

# Check test results if available
if [ -f "$STATE_DIR/test-results.json" ]; then
    if command -v jq >/dev/null 2>&1; then
        coverage=$(jq -r '.coverage' "$STATE_DIR/test-results.json")
        passed=$(jq -r '.passed' "$STATE_DIR/test-results.json")
        echo "- Test Coverage: ${coverage}%"
        echo "- Tests Status: $([ "$passed" = "true" ] && echo "✅ Passing" || echo "❌ Failing")"
    fi
fi

# Check EARS compliance
if [ -d "docs/requirements" ]; then
    total_reqs=$(find docs/requirements -name "*.md" -type f | wc -l)
    valid_reqs=$(grep -l "shall" docs/requirements/*.md 2>/dev/null | wc -l)
    
    if [ "$total_reqs" -gt 0 ]; then
        compliance=$((valid_reqs * 100 / total_reqs))
        echo "- EARS Compliance: ${compliance}% (${valid_reqs}/${total_reqs})"
    fi
fi

# Check BDD coverage
if [ -d "docs/bdd/features" ]; then
    features=$(find docs/bdd/features -name "*.feature" -type f | wc -l)
    echo "- BDD Features: ${features}"
fi

# Generate state summary
SUMMARY_FILE="$STATE_DIR/summary.json"
cat > "$SUMMARY_FILE" <<EOF
{
  "updated": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "sprint": {
    "number": $(extract_md_value "$SPRINT_FILE" "sprint:" || echo 1),
    "progress": ${progress:-0},
    "completed": ${completed:-0},
    "total": ${total:-0}
  },
  "metrics": {
    "coverage": ${coverage:-0},
    "tests": ${passed:-false},
    "ears": ${compliance:-0},
    "features": ${features:-0}
  }
}
EOF

echo ""
echo "✅ State synchronization complete!"
echo "📁 State files in: $STATE_DIR"

# Optional: Push state to remote if configured
if [ -n "$SYNC_REMOTE" ]; then
    echo "🔄 Pushing state to remote..."
    # Add remote sync logic here (e.g., S3, Git, etc.)
fi

exit 0
