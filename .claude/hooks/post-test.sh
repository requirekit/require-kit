#!/bin/bash

# Post-test hook for updating state after test execution
# This runs after tests complete to update metrics and state

set -e

echo "📊 Updating state after test execution..."

# Get test results from environment or detect
TEST_PASSED=${TEST_PASSED:-true}
TEST_COVERAGE=${TEST_COVERAGE:-0}
TEST_DURATION=${TEST_DURATION:-0}

# Function to update JSON files
update_json_value() {
    local file=$1
    local key=$2
    local value=$3
    
    if command -v jq >/dev/null 2>&1; then
        tmp=$(mktemp)
        jq ".$key = $value" "$file" > "$tmp" && mv "$tmp" "$file"
    fi
}

# Update test results file
RESULTS_FILE="docs/state/test-results.json"
if [ ! -f "$RESULTS_FILE" ]; then
    cat > "$RESULTS_FILE" <<EOF
{
  "lastRun": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "passed": $TEST_PASSED,
  "coverage": $TEST_COVERAGE,
  "duration": $TEST_DURATION,
  "history": []
}
EOF
else
    # Update existing results
    if command -v jq >/dev/null 2>&1; then
        tmp=$(mktemp)
        jq ".lastRun = \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\" | 
           .passed = $TEST_PASSED |
           .coverage = $TEST_COVERAGE |
           .duration = $TEST_DURATION |
           .history += [{
               \"date\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\",
               \"passed\": $TEST_PASSED,
               \"coverage\": $TEST_COVERAGE
           }] | 
           .history = (.history | .[-10:])" "$RESULTS_FILE" > "$tmp" && mv "$tmp" "$RESULTS_FILE"
    fi
fi

# Update quality gates status
GATES_FILE="docs/state/quality-gates.json"
if [ ! -f "$GATES_FILE" ]; then
    cat > "$GATES_FILE" <<EOF
{
  "lastCheck": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "gates": {
    "coverage": {
      "threshold": 80,
      "current": $TEST_COVERAGE,
      "passed": $([ "$TEST_COVERAGE" -ge 80 ] && echo true || echo false)
    },
    "tests": {
      "passed": $TEST_PASSED
    }
  }
}
EOF
fi

# Update sprint metrics if in a sprint
SPRINT_FILE="docs/state/current-sprint.md"
if [ -f "$SPRINT_FILE" ]; then
    # Update test coverage in sprint file
    if grep -q "Test Coverage:" "$SPRINT_FILE"; then
        sed -i.bak "s/Test Coverage: .*/Test Coverage: ${TEST_COVERAGE}%/" "$SPRINT_FILE"
    fi
    
    # Update test status
    if grep -q "Tests: " "$SPRINT_FILE"; then
        if [ "$TEST_PASSED" = true ]; then
            sed -i.bak "s/Tests: .*/Tests: ✅ All passing/" "$SPRINT_FILE"
        else
            sed -i.bak "s/Tests: .*/Tests: ❌ Some failing/" "$SPRINT_FILE"
        fi
    fi
fi

# Generate coverage badge if supported
if [ "$TEST_COVERAGE" -gt 0 ]; then
    BADGE_COLOR="red"
    if [ "$TEST_COVERAGE" -ge 80 ]; then
        BADGE_COLOR="green"
    elif [ "$TEST_COVERAGE" -ge 60 ]; then
        BADGE_COLOR="yellow"
    fi
    
    # Create a simple badge file
    cat > "docs/state/coverage-badge.svg" <<EOF
<svg xmlns="http://www.w3.org/2000/svg" width="104" height="20">
  <linearGradient id="b" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <mask id="a">
    <rect width="104" height="20" rx="3" fill="#fff"/>
  </mask>
  <g mask="url(#a)">
    <path fill="#555" d="M0 0h63v20H0z"/>
    <path fill="$BADGE_COLOR" d="M63 0h41v20H63z"/>
    <path fill="url(#b)" d="M0 0h104v20H0z"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
    <text x="31.5" y="15" fill="#010101" fill-opacity=".3">coverage</text>
    <text x="31.5" y="14">coverage</text>
    <text x="82.5" y="15" fill="#010101" fill-opacity=".3">${TEST_COVERAGE}%</text>
    <text x="82.5" y="14">${TEST_COVERAGE}%</text>
  </g>
</svg>
EOF
fi

# Log to changelog if significant changes
CHANGELOG_FILE="docs/state/changelog.md"
if [ "$TEST_PASSED" = false ] && [ -f "$CHANGELOG_FILE" ]; then
    # Add entry about test failure (for tracking)
    echo "" >> "$CHANGELOG_FILE"
    echo "## Test Failure - $(date +"%Y-%m-%d %H:%M")" >> "$CHANGELOG_FILE"
    echo "- Tests failed with coverage: ${TEST_COVERAGE}%" >> "$CHANGELOG_FILE"
    echo "- Duration: ${TEST_DURATION}s" >> "$CHANGELOG_FILE"
fi

# Check if we need to notify about quality gate failures
if [ "$TEST_COVERAGE" -lt 80 ]; then
    echo "⚠️  Warning: Coverage is below 80% threshold (${TEST_COVERAGE}%)"
fi

if [ "$TEST_PASSED" = false ]; then
    echo "❌ Tests failed - please review and fix"
fi

echo "✅ State updated successfully!"

# Create summary report
cat <<EOF

📊 Test Execution Summary
========================
Status: $([ "$TEST_PASSED" = true ] && echo "✅ PASSED" || echo "❌ FAILED")
Coverage: ${TEST_COVERAGE}%
Duration: ${TEST_DURATION}s
Timestamp: $(date +"%Y-%m-%d %H:%M:%S")

Quality Gates:
- Coverage: $([ "$TEST_COVERAGE" -ge 80 ] && echo "✅ PASS" || echo "❌ FAIL") (${TEST_COVERAGE}% / 80%)
- Tests: $([ "$TEST_PASSED" = true ] && echo "✅ PASS" || echo "❌ FAIL")

Files Updated:
- docs/state/test-results.json
- docs/state/quality-gates.json
$([ -f "docs/state/coverage-badge.svg" ] && echo "- docs/state/coverage-badge.svg")
$([ -f "$SPRINT_FILE" ] && echo "- $SPRINT_FILE")

EOF

exit 0
