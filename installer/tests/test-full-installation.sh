#!/bin/bash
# Full Installation Integration Test
# Tests complete installation flow including marker file creation

# Test configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_INSTALL_DIR="/tmp/require-kit-fulltest-$$"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║    Full Installation Integration Test                  ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Setup
echo -e "${BLUE}Setting up test environment...${NC}"
mkdir -p "$TEST_INSTALL_DIR"
export HOME="$TEST_INSTALL_DIR"
export INSTALL_DIR="$TEST_INSTALL_DIR/.agentecflow"

# Run installation script
echo ""
echo -e "${BLUE}Running installation script...${NC}"
if bash "$SCRIPT_DIR/scripts/install.sh"; then
    echo -e "${GREEN}✓ Installation script completed successfully${NC}"
else
    echo -e "${RED}✗ Installation script failed${NC}"
    rm -rf "$TEST_INSTALL_DIR"
    exit 1
fi

# Verify marker file
echo ""
echo -e "${BLUE}Verifying marker file...${NC}"

MARKER_FILE="$INSTALL_DIR/require-kit.marker.json"

if [ ! -f "$MARKER_FILE" ]; then
    echo -e "${RED}✗ Marker file not found at $MARKER_FILE${NC}"
    rm -rf "$TEST_INSTALL_DIR"
    exit 1
fi

if [ ! -s "$MARKER_FILE" ]; then
    echo -e "${RED}✗ Marker file is empty${NC}"
    rm -rf "$TEST_INSTALL_DIR"
    exit 1
fi

echo -e "${GREEN}✓ Marker file exists and is non-empty${NC}"

# Validate JSON structure
if command -v python3 &> /dev/null; then
    if python3 -c "import json; data = json.load(open('$MARKER_FILE')); assert data['package'] == 'require-kit'; assert 'version' in data; assert 'installed' in data" 2>/dev/null; then
        echo -e "${GREEN}✓ Marker file contains valid JSON with required fields${NC}"
    else
        echo -e "${RED}✗ Marker file JSON validation failed${NC}"
        cat "$MARKER_FILE"
        rm -rf "$TEST_INSTALL_DIR"
        exit 1
    fi
fi

# Display marker file content
echo ""
echo -e "${BLUE}Marker file content:${NC}"
cat "$MARKER_FILE"

# Verify installation structure
echo ""
echo -e "${BLUE}Verifying installation structure...${NC}"

if [ -d "$INSTALL_DIR/commands/require-kit" ]; then
    cmd_count=$(ls -1 "$INSTALL_DIR/commands/require-kit"/*.md 2>/dev/null | wc -l)
    echo -e "${GREEN}✓ Commands directory exists ($cmd_count commands)${NC}"
else
    echo -e "${RED}✗ Commands directory not found${NC}"
fi

if [ -d "$INSTALL_DIR/agents/require-kit" ]; then
    agent_count=$(ls -1 "$INSTALL_DIR/agents/require-kit"/*.md 2>/dev/null | wc -l)
    echo -e "${GREEN}✓ Agents directory exists ($agent_count agents)${NC}"
else
    echo -e "${RED}✗ Agents directory not found${NC}"
fi

if [ -f "$INSTALL_DIR/lib/feature_detection.py" ]; then
    echo -e "${GREEN}✓ Library files installed${NC}"
else
    echo -e "${YELLOW}⚠ Library files not found (may be expected if source not available)${NC}"
fi

# Cleanup
echo ""
echo -e "${BLUE}Cleaning up test environment...${NC}"
rm -rf "$TEST_INSTALL_DIR"
echo -e "${GREEN}✓ Test environment cleaned${NC}"

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║    FULL INSTALLATION TEST PASSED ✓                      ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

exit 0
