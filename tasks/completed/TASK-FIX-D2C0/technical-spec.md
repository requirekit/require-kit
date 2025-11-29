# TASK-FIX-D2C0: Technical Specification - Relative Imports

## Document Purpose

Detailed technical specification for implementing relative imports in require-kit library and command files. Includes exact file locations, current code patterns, target patterns, and validation methods.

---

## Part 1: Library File Changes

### 1.1 Core Configuration Files

#### File: `/installer/global/lib/config/plan_review_config.py`

**Current Code (lines 1-8)**:
```python
import os
from typing import Optional, Dict, Any, Literal
from pathlib import Path

from .defaults import DEFAULT_CONFIG
from .config_schema import ConfigSchema, ThresholdConfig
from utils import JsonSerializer, PathResolver
```

**Issue**: Line 7 uses `from utils import` which is broken absolute import

**Target Code**:
```python
import os
from typing import Optional, Dict, Any, Literal
from pathlib import Path

from .defaults import DEFAULT_CONFIG
from .config_schema import ConfigSchema, ThresholdConfig
from ..utils import JsonSerializer, PathResolver
```

**Change**: `from utils import` → `from ..utils import`

---

#### File: `/installer/global/lib/metrics/plan_review_metrics.py`

**Current Code (lines 1-6)**:
```python
from datetime import datetime
from typing import Dict, Any, Optional, Literal

from .metrics_storage import MetricsStorage
from config import PlanReviewConfig
```

**Issue**: Line 5 uses `from config import` which is broken absolute import

**Target Code**:
```python
from datetime import datetime
from typing import Dict, Any, Optional, Literal

from .metrics_storage import MetricsStorage
from ..config import PlanReviewConfig
```

**Change**: `from config import` → `from ..config import`

---

#### File: `/installer/global/lib/metrics/metrics_storage.py`

**Current Code (first 15 lines)**:
```python
"""Metrics storage and retrieval system."""
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

from config import PlanReviewConfig
from utils import JsonSerializer, PathResolver
```

**Issue**: Lines 7-8 use absolute imports

**Target Code**:
```python
"""Metrics storage and retrieval system."""
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

from ..config import PlanReviewConfig
from ..utils import JsonSerializer, PathResolver
```

**Changes**:
- `from config import` → `from ..config import`
- `from utils import` → `from ..utils import`

---

#### File: `/installer/global/lib/metrics/plan_review_dashboard.py`

**Current Likely Pattern**:
```python
# Check for these patterns:
from config import PlanReviewConfig
from metrics_storage import MetricsStorage
```

**Target Pattern**:
```python
from ..config import PlanReviewConfig
from .metrics_storage import MetricsStorage
```

---

### 1.2 Package Initializer Files

#### File: `/installer/global/lib/__init__.py`

**Target Content**:
```python
"""require-kit library package."""
# Package initialization - typically empty or minimal imports
```

**Purpose**: Mark lib/ as Python package

---

#### File: `/installer/global/lib/config/__init__.py`

**Target Content**:
```python
"""Configuration module for require-kit."""
from .plan_review_config import PlanReviewConfig

__all__ = ["PlanReviewConfig"]
```

**Purpose**: Re-export key classes for convenience imports

---

#### File: `/installer/global/lib/metrics/__init__.py`

**Target Content**:
```python
"""Metrics module for plan review system."""
from .plan_review_metrics import PlanReviewMetrics
from .metrics_storage import MetricsStorage

__all__ = ["PlanReviewMetrics", "MetricsStorage"]
```

**Purpose**: Re-export key classes

---

#### File: `/installer/global/lib/utils/__init__.py`

**Target Content**:
```python
"""Utility modules for require-kit."""
from .json_serializer import JsonSerializer
from .path_resolver import PathResolver
from .file_operations import FileOperations

__all__ = ["JsonSerializer", "PathResolver", "FileOperations"]
```

**Purpose**: Re-export utilities for convenient imports

---

### 1.3 Utility Files (Verify No Imports)

#### File: `/installer/global/lib/utils/file_operations.py`

**Verify**: Check that this file has no internal lib imports
- Should only use stdlib
- If it imports from other utils modules, use relative imports

**Pattern if needed**:
```python
from .json_serializer import JsonSerializer  # Sibling
```

---

#### File: `/installer/global/lib/utils/json_serializer.py`

**Verify**: Should only import stdlib
- No lib dependencies expected
- Standalone utility

---

#### File: `/installer/global/lib/utils/path_resolver.py`

**Critical**: Review this file carefully
- What paths does it resolve?
- Does it reference `installer` or `global` directories?
- Update to work with installed paths (~/.agentflow/)

**If it resolves repository paths**, update:
```python
# BEFORE - resolving to installer/global
repo_path = os.path.join(os.path.dirname(__file__), '../../..')
features_dir = os.path.join(repo_path, 'docs', 'features')

# AFTER - relative to installed location
lib_dir = os.path.dirname(__file__)  # ~/.agentflow/lib/
parent_dir = os.path.dirname(lib_dir)  # ~/.agentflow/
docs_dir = os.path.join(parent_dir, 'docs')
features_dir = os.path.join(docs_dir, 'features')
```

---

### 1.4 Core Library Files (Verify No Imports)

#### File: `/installer/global/lib/config/config_schema.py`

**Verify**: Should only import from pydantic and typing
- No internal lib imports expected
- Standalone schema definitions

---

#### File: `/installer/global/lib/config/defaults.py`

**Verify**: Should only contain constant definitions
- No internal lib imports expected
- Likely only imports like `Dict`, `Any` from typing

---

#### File: `/installer/global/lib/feature_detection.py`

**Verify**: Should only import stdlib
- No internal lib imports expected
- Standalone feature detection logic

---

## Part 2: Command and Agent File Changes

### 2.1 Agent Files with Embedded Python

#### File: `/installer/global/agents/code-reviewer.md`

**Location**: Search for "```python" blocks

**Current Pattern** (around line 150-160):
```python
from installer.global.commands.lib.spec_drift_detector import (
    SpecDriftDetector,
    format_drift_report
)
```

**Issue**: References `installer.global.commands.lib` which doesn't exist after installation

**Decision Required**: Where should `spec_drift_detector` live?

**Option A - Consolidate to lib/** (Recommended):
- Move `spec_drift_detector.py` to `/installer/global/lib/`
- Update import to:
```python
from lib.spec_drift_detector import (
    SpecDriftDetector,
    format_drift_report
)
```

**Option B - Keep structure, copy to lib/commands/**:
- Keep at `commands/lib/spec_drift_detector.py`
- Update install.sh to copy: `commands/lib/*.py` → `lib/commands/`
- Update import to:
```python
from lib.commands.spec_drift_detector import (
    SpecDriftDetector,
    format_drift_report
)
```

---

#### File: `/installer/global/agents/task-manager.md`

**Current Patterns**:
```python
from installer.global.commands.lib.micro_task_detector import MicroTaskDetector
# and comments like:
# - Import: `from installer.global.commands.lib.phase_execution import execute_phases`
# - Import: `from installer.global.commands.lib.plan_persistence import save_plan, load_plan, plan_exists`
# - Import: `from installer.global.commands.lib.flag_validator import validate_flags`
```

**Target Pattern** (after consolidation):
```python
from lib.micro_task_detector import MicroTaskDetector
# and:
# - Import: `from lib.phase_execution import execute_phases`
# - Import: `from lib.plan_persistence import save_plan, load_plan, plan_exists`
# - Import: `from lib.flag_validator import validate_flags`
```

---

### 2.2 Command Files with Embedded Python

**Action**: Search for "```python" in all files:

```bash
grep -l "^\`\`\`python" /installer/global/commands/*.md
```

**For Each File Found**:
1. View the Python code block
2. Check for imports matching `from installer.global` or `from global`
3. Update to `from lib.X` pattern
4. Re-check for any other absolute imports

---

## Part 3: Installation File Changes

### 3.1 install.sh Library Installation

#### File: `/installer/scripts/install.sh`

**Current Pattern** (around line 202-210):
```bash
install_lib() {
    print_info "Installing library files..."

    if [ -f "$SCRIPT_DIR/global/lib/feature_detection.py" ]; then
        cp "$SCRIPT_DIR/global/lib/feature_detection.py" "$INSTALL_DIR/lib/" 2>/dev/null || true
    fi

    # ... other individual files
}
```

**Issues**:
1. Only copies single files, not directory structure
2. Doesn't handle subdirectories (config/, metrics/, utils/)
3. Doesn't copy __init__.py files
4. Not maintainable if lib/ grows

**Target Pattern**:
```bash
install_lib() {
    print_info "Installing library files..."

    # Create lib directory if not exists
    mkdir -p "$INSTALL_DIR/lib"

    # Copy entire lib directory structure recursively
    if [ -d "$SCRIPT_DIR/global/lib" ]; then
        # Copy all Python files and subdirectories
        cp -r "$SCRIPT_DIR/global/lib/"* "$INSTALL_DIR/lib/" 2>/dev/null || true

        if [ -d "$INSTALL_DIR/lib" ] && [ "$(ls -A "$INSTALL_DIR/lib")" ]; then
            print_success "Library files installed successfully"
        else
            print_warning "Library files may not have been installed correctly"
        fi
    else
        print_error "Library directory not found at $SCRIPT_DIR/global/lib"
    fi
}
```

**Key Changes**:
1. Recursive copy: `cp -r "$SCRIPT_DIR/global/lib/"*`
2. Preserves directory structure automatically
3. Includes all __init__.py files
4. Single operation instead of multiple individual copies
5. Added validation check

**Verification in install.sh**:
- Around line 285, verify lib files exist:
```bash
if [ ! -f "$INSTALL_DIR/lib/feature_detection.py" ]; then
    # This is already there, good
fi
```

---

## Part 4: Import Validation

### 4.1 Verification Script

**Purpose**: Validate all imports work correctly

**File**: Create `/Users/richardwoollcott/Projects/appmilla_github/require-kit/test_imports.py`

```python
#!/usr/bin/env python3
"""
Validation script for require-kit imports.
Tests that all imports work correctly after relative import changes.
"""

import sys
import os

def test_lib_imports():
    """Test all library imports."""
    print("Testing library imports...")

    try:
        # Add lib to path as it would be in installed context
        lib_path = os.path.join(os.path.dirname(__file__), 'installer', 'global', 'lib')
        sys.path.insert(0, lib_path)

        # Test feature detection
        from feature_detection import detect_packages
        print("✓ feature_detection import successful")

        # Test config module
        from config import PlanReviewConfig
        from config.defaults import DEFAULT_CONFIG
        from config.config_schema import ConfigSchema
        print("✓ config module imports successful")

        # Test metrics module
        from metrics import PlanReviewMetrics, MetricsStorage
        print("✓ metrics module imports successful")

        # Test utils module
        from utils import JsonSerializer, PathResolver
        print("✓ utils module imports successful")

        # Test cross-module imports
        config = PlanReviewConfig()
        print("✓ PlanReviewConfig instantiation successful")

        print("\nAll imports passed!")
        return True

    except ImportError as e:
        print(f"✗ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_relative_imports():
    """Test that relative imports are being used."""
    print("\nChecking for relative imports in library files...")

    lib_dir = os.path.join(os.path.dirname(__file__), 'installer', 'global', 'lib')

    # Patterns to check for
    patterns_to_avoid = [
        'from installer.global',
        'from global.lib',
        'import installer.global',
        'import global.lib'
    ]

    for root, dirs, files in os.walk(lib_dir):
        # Skip __pycache__
        dirs[:] = [d for d in dirs if d != '__pycache__']

        for file in files:
            if not file.endswith('.py'):
                continue

            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                for line_no, line in enumerate(f, 1):
                    for pattern in patterns_to_avoid:
                        if pattern in line and not line.strip().startswith('#'):
                            print(f"✗ Found bad pattern in {filepath}:{line_no}")
                            print(f"  {line.strip()}")
                            return False

    print("✓ No absolute imports found")
    return True

if __name__ == '__main__':
    success = True
    success = test_relative_imports() and success
    success = test_lib_imports() and success

    sys.exit(0 if success else 1)
```

**Usage**:
```bash
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit
python3 test_imports.py
```

---

### 4.2 Grep Verification Commands

```bash
# Check for absolute imports in library files
grep -r "from installer.global\|from global.lib\|import installer.global\|import global.lib" \
  /installer/global/lib --include="*.py"

# Check for absolute imports in command/agent files
grep -r "from installer.global\|from global.lib" \
  /installer/global/commands /installer/global/agents --include="*.md"

# Check for sys.path manipulation
grep -r "sys.path\|PYTHONPATH\|append\|insert" \
  /installer/global/lib --include="*.py" | grep -v "# " | grep -v "test"

# Verify all __init__.py files exist
find /installer/global/lib -type d | while read dir; do
  if [ ! -f "$dir/__init__.py" ]; then
    echo "Missing: $dir/__init__.py"
  fi
done
```

**Expected Results After Changes**:
- First grep: No output (no bad imports)
- Second grep: No output (no bad imports in commands)
- Third grep: No output (no path manipulation)
- Fourth grep: All directories have __init__.py

---

## Part 5: Testing Checklist

### 5.1 Pre-Implementation Testing

```bash
# Analyze current state
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit

# Count files to update
echo "Python files in lib:"
find installer/global/lib -name "*.py" -type f | wc -l

echo "Markdown files with Python code:"
grep -l "^\`\`\`python" installer/global/commands/*.md installer/global/agents/*.md | wc -l

echo "Bad imports to fix:"
grep -r "from installer.global\|from global.lib" installer/global --include="*.py" --include="*.md" | wc -l
```

---

### 5.2 Post-Implementation Testing

**Test 1: Git Clone Installation**
```bash
# From repository root
cd /tmp/test-require-kit
cp -r /Users/richardwoollcott/Projects/appmilla_github/require-kit .
cd require-kit/installer/scripts
chmod +x install.sh
bash -x install.sh  # Run with debug output

# Verify
ls -la ~/.agentflow/lib/
ls -la ~/.agentflow/lib/config/
ls -la ~/.agentflow/lib/metrics/
ls -la ~/.agentflow/lib/utils/

# Test imports
cd ~/.agentflow
python3 -c "from lib.feature_detection import detect_packages; print('✓ Git clone test passed')"
```

**Test 2: Simulated Curl Installation**
```bash
# Clean environment test
rm -rf ~/.agentflow
mkdir -p /tmp/curl_test
cd /tmp/curl_test

# Download and run install script (simulate curl)
curl -sSL https://raw.githubusercontent.com/require-kit/require-kit/YOUR_BRANCH/installer/scripts/install.sh | bash

# Verify
ls -la ~/.agentflow/lib/
python3 -c "from lib.feature_detection import detect_packages; print('✓ Curl test passed')"
```

**Test 3: Relative Import Validation**
```bash
python3 /Users/richardwoollcott/Projects/appmilla_github/require-kit/test_imports.py
```

**Test 4: Command Execution**
```bash
# If require-kit commands are installed, test that they work
# This depends on how commands are executed in your system
require-kit-command-name --help  # Should work without import errors
```

---

## Part 6: Consolidation Decision - Commands/Lib Files

### Decision: Move commands/lib/* to lib/

**Rationale**:
1. Simpler import paths: `from lib.X` instead of `from lib.commands.X`
2. Single lib directory to maintain
3. Easier installation process
4. Matches Taskwright pattern more closely

**Implementation**:
1. Copy any Python files from `commands/lib/` to `lib/`
2. Update all imports in agents/commands markdown files
3. Update install.sh to include new files
4. Remove or deprecate `commands/lib/` directory

**Files likely involved**:
- `commands/lib/spec_drift_detector.py` → `lib/spec_drift_detector.py`
- `commands/lib/micro_task_detector.py` → `lib/micro_task_detector.py`
- `commands/lib/phase_execution.py` → `lib/phase_execution.py`
- `commands/lib/plan_persistence.py` → `lib/plan_persistence.py`
- `commands/lib/flag_validator.py` → `lib/flag_validator.py`
- (Any others found)

---

## Implementation Order

1. **Analyze** (15 min)
   - Run grep commands from Section 5.1
   - Document all files needing changes

2. **Update Library Files** (30 min)
   - Fix intra-lib imports (Sections 1.1-1.4)
   - Ensure __init__.py files exist (Section 1.2)

3. **Move Command Libraries** (15 min)
   - Copy commands/lib/ files to lib/
   - Update install.sh
   - Verify no duplicates

4. **Update Command/Agent Files** (15 min)
   - Find all Python code blocks in .md files
   - Update imports in each block

5. **Update install.sh** (10 min)
   - Implement recursive copy (Section 3.1)
   - Verify directory structure preserved

6. **Validation** (10 min)
   - Run test_imports.py script
   - Run grep verification commands

7. **Testing** (20 min)
   - Git clone test
   - Curl simulation test
   - Command execution test

**Total Estimated Time**: 2 hours

---

## File List Summary

### Files to Modify (26 total)

**Library Files (14)**:
1. `installer/global/lib/__init__.py` - Create/verify
2. `installer/global/lib/feature_detection.py` - Verify no imports
3. `installer/global/lib/config/__init__.py` - Create/update
4. `installer/global/lib/config/config_schema.py` - Verify no imports
5. `installer/global/lib/config/defaults.py` - Verify no imports
6. `installer/global/lib/config/plan_review_config.py` - Fix imports
7. `installer/global/lib/metrics/__init__.py` - Create/update
8. `installer/global/lib/metrics/metrics_storage.py` - Fix imports
9. `installer/global/lib/metrics/plan_review_metrics.py` - Fix imports
10. `installer/global/lib/metrics/plan_review_dashboard.py` - Fix imports
11. `installer/global/lib/utils/__init__.py` - Create/update
12. `installer/global/lib/utils/file_operations.py` - Verify no imports
13. `installer/global/lib/utils/json_serializer.py` - Verify no imports
14. `installer/global/lib/utils/path_resolver.py` - Review and fix if needed

**Command/Agent Files (2-5)**:
1. `installer/global/agents/code-reviewer.md` - Fix Python blocks
2. `installer/global/agents/task-manager.md` - Fix Python blocks
3. Other agent/command files - Check for Python blocks

**Installation Files (1)**:
1. `installer/scripts/install.sh` - Update lib installation

**New Files (1)**:
1. `test_imports.py` - Create validation script

---

**Document Version**: 1.0
**Created**: 2025-11-29
**Status**: Ready for Implementation
