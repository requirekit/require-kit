# TASK-FIX-D2C0: Step-by-Step Implementation Guide

## Quick Reference

**Task**: Convert Python imports from absolute paths to relative imports
**Priority**: Critical (Launch Blocker)
**Estimated Time**: 1-2 hours
**Key Command**: Convert `from installer.global.lib.X` → `from lib.X`

---

## Pre-Flight Checklist

Before starting, verify you have:

```bash
# Verify working directory
pwd
# Should output: /Users/richardwoollcott/Projects/appmilla_github/require-kit

# Verify git status is clean
git status
# Should show: "On branch RichWoollcott/la-paz-v1" and "nothing to commit, working tree clean"

# Verify directory structure
ls -la installer/global/lib/
# Should show: config/, metrics/, utils/, and .py files

# List Python files to update
find installer/global/lib -name "*.py" | wc -l
# Should show ~14 files
```

---

## Step 1: Analyze Current State (15 minutes)

### Step 1.1: Find All Bad Imports

```bash
# Find all absolute imports
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit
grep -r "from installer.global\|from global.lib" installer/global --include="*.py" --include="*.md" > /tmp/bad_imports.txt
cat /tmp/bad_imports.txt
```

**Expected Output Examples**:
```
installer/global/agents/code-reviewer.md:from installer.global.commands.lib.spec_drift_detector import (
installer/global/agents/task-manager.md:from installer.global.commands.lib.micro_task_detector import MicroTaskDetector
installer/global/lib/config/plan_review_config.py:from utils import JsonSerializer, PathResolver
installer/global/lib/metrics/plan_review_metrics.py:from config import PlanReviewConfig
```

### Step 1.2: Find sys.path Manipulation

```bash
# Check for path manipulation
grep -r "sys.path\|PYTHONPATH" installer --include="*.py" --include="*.sh" | grep -v "test" | grep -v "#"

# Should be empty or minimal (expected for test files only)
```

### Step 1.3: Document Files Needing Changes

Create `/tmp/files_to_update.txt`:

```bash
# Library files with imports
echo "=== Library Files ===" >> /tmp/files_to_update.txt
find installer/global/lib -name "*.py" -type f | sort >> /tmp/files_to_update.txt

# Command/Agent files with Python
echo "" >> /tmp/files_to_update.txt
echo "=== Command/Agent Files ===" >> /tmp/files_to_update.txt
grep -l "from installer.global\|from global.lib" installer/global/agents/*.md installer/global/commands/*.md 2>/dev/null >> /tmp/files_to_update.txt

cat /tmp/files_to_update.txt
```

---

## Step 2: Update Library Files (30 minutes)

### Step 2.1: Update config/plan_review_config.py

```bash
# First, read the file to see current state
head -20 /Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/global/lib/config/plan_review_config.py
```

The import line should look like:
```python
from utils import JsonSerializer, PathResolver
```

**Required Change**:
- Line 8: Change `from utils import` to `from ..utils import`

**Why**: We're in `lib/config/`, so to reach `lib/utils/` we go up two levels (`..`)

---

### Step 2.2: Update metrics/plan_review_metrics.py

```bash
head -10 /Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/global/lib/metrics/plan_review_metrics.py
```

The import line should look like:
```python
from config import PlanReviewConfig
```

**Required Change**:
- Change `from config import` to `from ..config import`

**Why**: We're in `lib/metrics/`, so to reach `lib/config/` we go up two levels (`..`)

---

### Step 2.3: Update metrics/metrics_storage.py

```bash
head -10 /Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/global/lib/metrics/metrics_storage.py
```

Look for imports like:
```python
from config import PlanReviewConfig
from utils import JsonSerializer, PathResolver
```

**Required Changes**:
- Change `from config import` to `from ..config import`
- Change `from utils import` to `from ..utils import`

---

### Step 2.4: Check Other Library Files

For each file, check what imports it has:

```bash
# Check each file
for file in installer/global/lib/utils/*.py installer/global/lib/config/*.py installer/global/lib/metrics/*.py; do
  echo "=== $file ==="
  grep -n "^from\|^import" "$file" | head -5
done
```

**For each file found with imports**:
- `from config import` → `from ..config import`
- `from utils import` → `from ..utils import`
- `from .sibling import` → Keep as-is (already relative)
- `from ..parent import` → Keep as-is (already relative)
- stdlib imports → Keep as-is (no change needed)

---

### Step 2.5: Verify/Create __init__.py Files

```bash
# Check if all __init__.py files exist
find installer/global/lib -type d | while read dir; do
  if [ ! -f "$dir/__init__.py" ]; then
    echo "MISSING: $dir/__init__.py"
  else
    echo "OK: $dir/__init__.py"
  fi
done
```

If any are missing, create them with:

```bash
# Create missing __init__.py files
touch installer/global/lib/__init__.py
touch installer/global/lib/config/__init__.py
touch installer/global/lib/metrics/__init__.py
touch installer/global/lib/utils/__init__.py
```

**For each __init__.py file**, add minimal content:

```python
"""[Module name] module."""
# Package initialization
```

---

## Step 3: Update Command/Agent Files (15 minutes)

### Step 3.1: Find Python Blocks in Agent Files

```bash
grep -n "from installer.global" installer/global/agents/*.md
```

**Expected Output**:
```
installer/global/agents/code-reviewer.md:from installer.global.commands.lib.spec_drift_detector import (
installer/global/agents/task-manager.md:from installer.global.commands.lib.micro_task_detector import MicroTaskDetector
```

### Step 3.2: Update code-reviewer.md

Look for the Python block around the `SpecDriftDetector` import.

**Current**:
```python
from installer.global.commands.lib.spec_drift_detector import (
```

**Target**:
```python
from lib.spec_drift_detector import (
```

**Why**: After installation, modules will be at `~/.agentflow/lib/spec_drift_detector.py`

---

### Step 3.3: Update task-manager.md

Look for all Python blocks with imports starting with `from installer.global.commands.lib`.

**Current Examples**:
```python
from installer.global.commands.lib.micro_task_detector import MicroTaskDetector
from installer.global.commands.lib.phase_execution import execute_phases
```

**Target**:
```python
from lib.micro_task_detector import MicroTaskDetector
from lib.phase_execution import execute_phases
```

---

### Step 3.4: Search All Command/Agent Files

```bash
# Find all .md files with bad imports
grep -r "from installer.global" installer/global/commands/ installer/global/agents/ --include="*.md" | cut -d: -f1 | sort -u
```

For each file found, update all `from installer.global.commands.lib.X` to `from lib.X`

---

## Step 4: Update Installation Script (10 minutes)

### Step 4.1: Review Current install.sh

```bash
grep -A 20 "install_lib()" /Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/scripts/install.sh
```

### Step 4.2: Expected Current Pattern

Around line 202-210, should show:
```bash
install_lib() {
    print_info "Installing library files..."

    if [ -f "$SCRIPT_DIR/global/lib/feature_detection.py" ]; then
        cp "$SCRIPT_DIR/global/lib/feature_detection.py" "$INSTALL_DIR/lib/" 2>/dev/null || true
    fi
    # ... more individual copies
}
```

### Step 4.3: Update install.sh

Replace the `install_lib()` function with:

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

---

## Step 5: Verification (10 minutes)

### Step 5.1: Check for Bad Imports

```bash
# This should return NOTHING
grep -r "from installer.global\|from global.lib" /Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/global --include="*.py" --include="*.md" 2>/dev/null
# If blank, all imports are fixed!
```

### Step 5.2: Check for Path Manipulation

```bash
# This should return NOTHING (except maybe in test files with comments)
grep -r "sys.path\|PYTHONPATH" /Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/global --include="*.py" | grep -v "test" | grep -v "#"
```

### Step 5.3: Verify __init__.py Files

```bash
# All of these should exist:
ls -1 /Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/global/lib/__init__.py
ls -1 /Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/global/lib/config/__init__.py
ls -1 /Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/global/lib/metrics/__init__.py
ls -1 /Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/global/lib/utils/__init__.py
```

### Step 5.4: Verify install.sh Changes

```bash
# Check that install_lib() was updated correctly
grep -A 15 "install_lib()" /Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/scripts/install.sh | grep "cp -r"
# Should show the recursive copy command
```

---

## Step 6: Git Commit

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit

# Check what changed
git status

# Stage changes
git add -A

# Create commit
git commit -m "fix: convert absolute imports to relative imports for installation compatibility

- Update all lib/ module imports to use relative imports (from lib.X pattern)
- Fix config/plan_review_config.py to import from ..utils
- Fix metrics/plan_review_metrics.py to import from ..config
- Fix metrics/metrics_storage.py to import from ..config and ..utils
- Update agent files to import from lib.X instead of installer.global
- Update install.sh to use recursive copy for lib/ directory
- Add/verify __init__.py files in all lib/ subdirectories
- Matches Taskwright import pattern for consistency

Fixes TASK-FIX-D2C0 - Implements relative imports for Python path fix"

# Verify
git status
```

---

## Step 7: Testing (20 minutes)

### Test 7.1: Verify Git Clone Works

```bash
# Make a temporary directory for testing
mkdir -p /tmp/test-require-kit-install
cd /tmp/test-require-kit-install

# Copy the modified code
cp -r /Users/richardwoollcott/Projects/appmilla_github/require-kit .
cd require-kit

# Run the install script
chmod +x installer/scripts/install.sh
bash installer/scripts/install.sh

# Verify files were installed
echo "=== Checking installation ==="
ls -la ~/.agentflow/lib/ | head -20
ls -la ~/.agentflow/lib/config/ | head -10
ls -la ~/.agentflow/lib/metrics/ | head -10
ls -la ~/.agentflow/lib/utils/ | head -10
```

### Test 7.2: Verify Imports Work

```bash
# Test that imports work
python3 << 'EOF'
import sys
import os

# Test 1: Direct lib import
sys.path.insert(0, os.path.expanduser('~/.agentflow'))
try:
    from lib.feature_detection import detect_packages
    print("✓ Test 1 PASSED: feature_detection import works")
except ImportError as e:
    print(f"✗ Test 1 FAILED: {e}")
    sys.exit(1)

# Test 2: Config module
try:
    from lib.config import PlanReviewConfig
    print("✓ Test 2 PASSED: config import works")
except ImportError as e:
    print(f"✗ Test 2 FAILED: {e}")
    sys.exit(1)

# Test 3: Metrics module
try:
    from lib.metrics import PlanReviewMetrics, MetricsStorage
    print("✓ Test 3 PASSED: metrics import works")
except ImportError as e:
    print(f"✗ Test 3 FAILED: {e}")
    sys.exit(1)

# Test 4: Utils module
try:
    from lib.utils import JsonSerializer, PathResolver
    print("✓ Test 4 PASSED: utils import works")
except ImportError as e:
    print(f"✗ Test 4 FAILED: {e}")
    sys.exit(1)

# Test 5: Create config instance
try:
    config = PlanReviewConfig()
    print("✓ Test 5 PASSED: PlanReviewConfig instantiation works")
except Exception as e:
    print(f"✗ Test 5 FAILED: {e}")
    sys.exit(1)

print("\nAll import tests PASSED!")
EOF
```

### Test 7.3: Verify No Bad Imports Remain

```bash
# In the copied test directory, verify all imports are fixed
cd /tmp/test-require-kit-install/require-kit
echo "=== Checking for remaining bad imports ==="
bad_imports=$(grep -r "from installer.global\|from global.lib" installer/global --include="*.py" --include="*.md" 2>/dev/null | wc -l)
if [ "$bad_imports" -eq 0 ]; then
  echo "✓ No bad imports found"
else
  echo "✗ Found $bad_imports bad imports"
  grep -r "from installer.global\|from global.lib" installer/global --include="*.py" --include="*.md"
fi
```

---

## Troubleshooting

### Problem: Import Error After Changes

**Symptom**: `ModuleNotFoundError: No module named 'config'`

**Solution**:
1. Check that you changed `from config import` to `from ..config import`
2. Verify the import is in a file that's in a subdirectory (config/, metrics/, etc.)
3. Check the __init__.py file exists in the target directory

**Example Fix**:
```python
# WRONG - still absolute
from config import PlanReviewConfig

# RIGHT - now relative
from ..config import PlanReviewConfig
```

---

### Problem: Missing __init__.py Files

**Symptom**: Python doesn't recognize lib/ as a package

**Solution**:
```bash
# Verify all directories have __init__.py
find installer/global/lib -type d -exec touch {}/__init__.py \;

# Verify
find installer/global/lib -name "__init__.py" | sort
```

---

### Problem: Install Script Not Copying All Files

**Symptom**: After installation, some lib files are missing

**Solution**:
1. Verify the install.sh has the `cp -r` command
2. Check that `$SCRIPT_DIR/global/lib/` path is correct
3. Verify directory permissions: `chmod -R 755 installer/global/lib/`

---

### Problem: Commands Still Reference Old Import Path

**Symptom**: Agent/command file still has `from installer.global.commands.lib`

**Solution**:
1. Use grep to find all remaining bad imports:
   ```bash
   grep -r "from installer.global" installer/global/agents/ installer/global/commands/ --include="*.md"
   ```
2. For each result, update the Markdown file
3. Change `from installer.global.commands.lib.X` to `from lib.X`

---

## Quick Reference: Import Pattern Table

| Current Import | New Import | File Location |
|---|---|---|
| `from utils import X` | `from ..utils import X` | `lib/config/*.py` or `lib/metrics/*.py` |
| `from config import X` | `from ..config import X` | `lib/metrics/*.py` |
| `from .sibling import X` | `from .sibling import X` | Keep as-is (already relative) |
| `from installer.global.lib.X` | `from lib.X` | Command/Agent .md files |
| `from installer.global.commands.lib.X` | `from lib.X` | Command/Agent .md files |
| `from lib.X import Y` | `from lib.X import Y` | Keep in .md files (exec context) |

---

## Summary Checklist

- [ ] Step 1: Analyzed current state with grep
- [ ] Step 2: Updated all library files with relative imports
- [ ] Step 2.5: Verified/created all __init__.py files
- [ ] Step 3: Updated command/agent files with relative imports
- [ ] Step 4: Updated install.sh with recursive copy
- [ ] Step 5: Verified no bad imports remain
- [ ] Step 6: Created git commit
- [ ] Step 7.1: Tested git clone installation
- [ ] Step 7.2: Tested that imports work
- [ ] Step 7.3: Verified no bad imports in test copy

---

## Success Criteria

When all tests pass:

1. `grep -r "from installer.global"` returns nothing
2. `grep -r "from global.lib"` returns nothing
3. Fresh installation creates `~/.agentflow/lib/` with all subdirectories
4. `python3 -c "from lib.feature_detection import detect_packages"` works
5. All __init__.py files exist in lib/ and subdirectories
6. Command files execute without import errors

---

**Status**: Ready to implement
**Next**: Start with Step 1 (Pre-flight Checklist)
**Time Estimate**: 1-2 hours total
