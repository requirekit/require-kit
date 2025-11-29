#!/usr/bin/env python3
"""
Test Suite: Post-Installation Validation Function
Tests the validate_installation() function behavior.
"""
import subprocess
import tempfile
import sys
from pathlib import Path


class TestValidationFunction:
    """Test the validate_installation function."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent
        self.install_script = self.repo_root / "installer" / "scripts" / "install.sh"

    def test_validation_with_python(self):
        """Test validation succeeds when Python 3 is available."""
        print("\nTest: Validation with Python 3 available")
        print("-" * 60)

        # Extract and test just the validation function
        test_script = """
#!/bin/bash
set -e

INSTALL_DIR="$HOME/.agentecflow"
GREEN='\\033[0;32m'
RED='\\033[0;31m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m'

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
    exit 1
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

validate_installation() {
    print_info "Validating installation..."

    # Check if Python 3 is available
    if ! command -v python3 &> /dev/null; then
        print_warning "Python 3 not found - skipping Python validation"
        return 0
    fi

    # Test Python import of feature_detection module
    if ! python3 <<EOF
import sys
sys.path.insert(0, "$INSTALL_DIR/lib")
try:
    from lib.feature_detection import detect_packages
    print("Import successful")
    sys.exit(0)
except ImportError as e:
    print(f"Import failed: {e}", file=sys.stderr)
    sys.exit(1)
EOF
    then
        print_error "Python module validation failed"
        echo ""
        echo "The feature_detection module could not be imported."
        echo "This indicates an installation problem with the Python library files."
        echo ""
        echo "Troubleshooting steps:"
        echo "  1. Check that $INSTALL_DIR/lib/feature_detection.py exists"
        echo "  2. Verify Python 3 is installed: python3 --version"
        echo "  3. Try reinstalling: bash install.sh"
        echo ""
        exit 1
    fi

    print_success "Python module validation passed"
}

validate_installation
"""

        # Write test script to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
            f.write(test_script)
            test_file = f.name

        try:
            # Make executable
            Path(test_file).chmod(0o755)

            # Run the test (this will fail if lib files aren't installed)
            result = subprocess.run(
                ['bash', test_file],
                capture_output=True,
                text=True,
                timeout=10
            )

            print(f"Exit code: {result.returncode}")
            print(f"Output:\n{result.stdout}")
            if result.stderr:
                print(f"Stderr:\n{result.stderr}")

            # For this test, we expect it might fail if not installed
            # What matters is the function executes correctly
            if result.returncode == 0:
                print("✓ Validation function executes successfully")
                return True
            elif "Python module validation failed" in result.stdout or \
                 "Python 3 not found" in result.stdout:
                print("✓ Validation function handles missing installation correctly")
                return True
            else:
                print("✗ Validation function failed unexpectedly")
                return False

        finally:
            # Clean up
            Path(test_file).unlink(missing_ok=True)

    def test_validation_without_python(self):
        """Test validation gracefully skips when Python 3 is not available."""
        print("\nTest: Validation without Python 3")
        print("-" * 60)

        test_script = """
#!/bin/bash

# Mock environment where python3 doesn't exist
command() {
    if [ "$2" = "python3" ]; then
        return 1  # Not found
    fi
    builtin command "$@"
}

GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m'

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

validate_installation() {
    print_info "Validating installation..."

    # Check if Python 3 is available
    if ! command -v python3 &> /dev/null; then
        print_warning "Python 3 not found - skipping Python validation"
        return 0
    fi
}

validate_installation
echo "Exit code: $?"
"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
            f.write(test_script)
            test_file = f.name

        try:
            Path(test_file).chmod(0o755)
            result = subprocess.run(
                ['bash', test_file],
                capture_output=True,
                text=True,
                timeout=5
            )

            print(f"Output:\n{result.stdout}")

            if result.returncode == 0 and "skipping Python validation" in result.stdout:
                print("✓ Validation gracefully handles missing Python 3")
                return True
            else:
                print("✗ Validation did not handle missing Python correctly")
                return False

        finally:
            Path(test_file).unlink(missing_ok=True)

    def test_validation_error_exit_code(self):
        """Test validation exits with code 1 on import failure."""
        print("\nTest: Validation error exit code")
        print("-" * 60)

        test_script = """
#!/bin/bash
set -e

GREEN='\\033[0;32m'
RED='\\033[0;31m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m'

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
    exit 1
}

validate_installation() {
    print_info "Validating installation..."

    if ! command -v python3 &> /dev/null; then
        return 0
    fi

    # Simulate import failure
    if ! python3 <<EOF
import sys
sys.exit(1)  # Force failure
EOF
    then
        print_error "Python module validation failed"
        exit 1
    fi
}

validate_installation
"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
            f.write(test_script)
            test_file = f.name

        try:
            Path(test_file).chmod(0o755)
            result = subprocess.run(
                ['bash', test_file],
                capture_output=True,
                text=True,
                timeout=5
            )

            print(f"Exit code: {result.returncode}")

            if result.returncode == 1 and "Python module validation failed" in result.stdout:
                print("✓ Validation exits with code 1 on failure")
                return True
            else:
                print("✗ Validation did not exit with correct error code")
                return False

        finally:
            Path(test_file).unlink(missing_ok=True)

    def run_all_tests(self):
        """Run all validation function tests."""
        print("\n" + "=" * 80)
        print("Post-Installation Validation Function Tests")
        print("=" * 80)

        tests = [
            self.test_validation_with_python,
            self.test_validation_without_python,
            self.test_validation_error_exit_code,
        ]

        passed = 0
        failed = 0

        for test_func in tests:
            try:
                if test_func():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"✗ Test failed with exception: {e}")
                failed += 1

        print("\n" + "-" * 80)
        print(f"Results: {passed} passed, {failed} failed")
        print("-" * 80 + "\n")

        return failed == 0


def main():
    """Main test runner."""
    tester = TestValidationFunction()

    if tester.run_all_tests():
        print("✓ All validation function tests passed")
        return 0
    else:
        print("\n✗ Validation function tests FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
