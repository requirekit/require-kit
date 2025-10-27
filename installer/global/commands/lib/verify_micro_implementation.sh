#!/bin/bash
# Verification script for TASK-020 Micro-Task Mode Implementation

echo "======================================================================"
echo "TASK-020 IMPLEMENTATION VERIFICATION"
echo "======================================================================"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Track results
PASSED=0
FAILED=0

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Check files exist
echo "1. Checking file existence..."
FILES=(
    "micro_task_detector.py"
    "micro_task_workflow.py"
    "test_micro_task_detector.py"
    "test_micro_workflow.py"
    "test_micro_basic.py"
    "MICRO_TASK_README.md"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "  ${GREEN}✓${NC} $file"
        ((PASSED++))
    else
        echo -e "  ${RED}✗${NC} $file (missing)"
        ((FAILED++))
    fi
done
echo ""

# Test 2: Compile Python modules
echo "2. Compiling Python modules..."
if python3 -m py_compile micro_task_detector.py micro_task_workflow.py 2>/dev/null; then
    echo -e "  ${GREEN}✓${NC} All modules compile successfully"
    ((PASSED++))
else
    echo -e "  ${RED}✗${NC} Compilation failed"
    ((FAILED++))
fi
echo ""

# Test 3: Run basic sanity tests
echo "3. Running basic sanity tests..."
if python3 test_micro_basic.py > /tmp/test_output.txt 2>&1; then
    echo -e "  ${GREEN}✓${NC} All sanity tests passed"
    ((PASSED++))
    grep "✅" /tmp/test_output.txt | head -5
else
    echo -e "  ${RED}✗${NC} Sanity tests failed"
    ((FAILED++))
    tail -10 /tmp/test_output.txt
fi
echo ""

# Test 4: Check line counts
echo "4. Checking line counts..."
DETECTOR_LINES=$(wc -l < micro_task_detector.py)
WORKFLOW_LINES=$(wc -l < micro_task_workflow.py)

if [ "$DETECTOR_LINES" -gt 300 ]; then
    echo -e "  ${GREEN}✓${NC} micro_task_detector.py: $DETECTOR_LINES lines (target: >300)"
    ((PASSED++))
else
    echo -e "  ${RED}✗${NC} micro_task_detector.py: $DETECTOR_LINES lines (target: >300)"
    ((FAILED++))
fi

if [ "$WORKFLOW_LINES" -gt 250 ]; then
    echo -e "  ${GREEN}✓${NC} micro_task_workflow.py: $WORKFLOW_LINES lines (target: >250)"
    ((PASSED++))
else
    echo -e "  ${RED}✗${NC} micro_task_workflow.py: $WORKFLOW_LINES lines (target: >250)"
    ((FAILED++))
fi
echo ""

# Test 5: Check documentation updates
echo "5. Checking documentation updates..."
cd ../../..

if grep -q "Micro-Task Mode" commands/task-work.md; then
    echo -e "  ${GREEN}✓${NC} task-work.md updated with micro-task documentation"
    ((PASSED++))
else
    echo -e "  ${RED}✗${NC} task-work.md missing micro-task documentation"
    ((FAILED++))
fi

if grep -q "Micro-Task Workflow" agents/task-manager.md; then
    echo -e "  ${GREEN}✓${NC} task-manager.md updated with micro-task workflow"
    ((PASSED++))
else
    echo -e "  ${RED}✗${NC} task-manager.md missing micro-task workflow"
    ((FAILED++))
fi
echo ""

# Test 6: Import verification
echo "6. Verifying Python imports..."
cd commands/lib
if python3 -c "from micro_task_detector import MicroTaskDetector, MicroTaskAnalysis; print('Detector imports OK')" 2>&1 | grep -q "OK"; then
    echo -e "  ${GREEN}✓${NC} micro_task_detector imports successfully"
    ((PASSED++))
else
    echo -e "  ${RED}✗${NC} micro_task_detector import failed"
    ((FAILED++))
fi

if python3 -c "from micro_task_workflow import MicroTaskWorkflow, MicroWorkflowResult; print('Workflow imports OK')" 2>&1 | grep -q "OK"; then
    echo -e "  ${GREEN}✓${NC} micro_task_workflow imports successfully"
    ((PASSED++))
else
    echo -e "  ${RED}✗${NC} micro_task_workflow import failed"
    ((FAILED++))
fi
echo ""

# Summary
echo "======================================================================"
echo "VERIFICATION SUMMARY"
echo "======================================================================"
echo -e "Total Tests: $((PASSED + FAILED))"
echo -e "${GREEN}Passed: $PASSED${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}Failed: $FAILED${NC}"
else
    echo -e "${GREEN}Failed: $FAILED${NC}"
fi
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ ALL VERIFICATION CHECKS PASSED${NC}"
    echo ""
    echo "Implementation is ready for:"
    echo "  1. Phase 5 Code Review"
    echo "  2. Integration with task-work orchestration"
    echo "  3. End-to-end workflow testing"
    exit 0
else
    echo -e "${RED}❌ SOME VERIFICATION CHECKS FAILED${NC}"
    echo ""
    echo "Please review failed checks and fix issues."
    exit 1
fi
