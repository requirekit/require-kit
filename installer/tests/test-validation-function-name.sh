#!/usr/bin/env bash
# Test that validation imports correct function name
# Prevents regression of detect_packages vs is_require_kit_installed bug

set -euo pipefail

# Configurable paths (recommended enhancement)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
INSTALL_SCRIPT="${INSTALL_SCRIPT:-$PROJECT_ROOT/installer/scripts/install.sh}"
FEATURE_DETECTION="${FEATURE_DETECTION:-$PROJECT_ROOT/installer/global/lib/feature_detection.py}"

echo "=========================================="
echo "Validation Function Name Consistency Test"
echo "=========================================="
echo ""

# Verify files exist
if [ ! -f "$INSTALL_SCRIPT" ]; then
    echo "❌ ERROR: install.sh not found at: $INSTALL_SCRIPT"
    exit 1
fi

if [ ! -f "$FEATURE_DETECTION" ]; then
    echo "❌ ERROR: feature_detection.py not found at: $FEATURE_DETECTION"
    exit 1
fi

# Extract function name from install.sh
INSTALL_FUNC=$(grep "from lib.feature_detection import" "$INSTALL_SCRIPT" \
    | head -1 \
    | sed 's/.*import //' \
    | tr -d ' \n\r')

echo "Step 1: Extract import statement from install.sh"
echo "  Imported function: '$INSTALL_FUNC'"
echo ""

# Verify function exists in feature_detection.py
echo "Step 2: Verify function exists in feature_detection.py"

if grep -q "^def $INSTALL_FUNC(" "$FEATURE_DETECTION"; then
    echo "  Found: def $INSTALL_FUNC() in feature_detection.py"
    echo ""
    echo "=========================================="
    echo "✅ PASS: Function name is consistent"
    echo "=========================================="
    exit 0
else
    echo "  NOT FOUND: def $INSTALL_FUNC() in feature_detection.py"
    echo ""
    echo "=========================================="
    echo "❌ FAIL: Function name mismatch detected"
    echo "=========================================="
    echo ""
    echo "This is the exact bug that caused the Nov 29, 2025 incident."
    echo ""
    echo "The import statement in install.sh references:"
    echo "  $INSTALL_FUNC"
    echo ""
    echo "Available functions in feature_detection.py:"
    grep "^def " "$FEATURE_DETECTION" | sed 's/def /  - /' | sed 's/(.*$//'
    echo ""
    exit 1
fi
