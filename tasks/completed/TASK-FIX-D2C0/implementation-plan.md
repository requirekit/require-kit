# TASK-FIX-D2C0: Relative Imports Implementation Plan

## Overview

Convert all Python imports from absolute repository paths (`from installer.global.lib.X` or `from global.lib.X`) to relative installed paths (`from lib.X`) to match Taskwright's pattern and ensure the system works correctly after installation.

**Status**: Planning
**Priority**: Critical (Launch Blocker)
**Complexity**: 4/10
**Estimated Effort**: 1-2 hours

---

## Problem Statement

### Current State
The codebase contains absolute imports that reference repository paths:
- `from installer.global.lib.X import Y` - When running from source
- `from global.lib.X import Y` - When running from installed location
- Mixed patterns across library files, command files, and agent specifications

### Issues
1. **Installation Context Mismatch**: Absolute paths work in repository context but fail after curl installation
2. **Inconsistent Patterns**: Some files use `installer.global`, others use `global`, creating confusion
3. **Path Dependency**: Code relies on PYTHONPATH or sys.path manipulation rather than proper package structure
4. **Non-Standard Pattern**: Taskwright uses relative imports (`from lib.X`) which is simpler and more reliable

### Example Problems
```python
# When installed via curl to ~/.agentflow/bin/require-kit
# This fails because installer/global is not in the path:
from installer.global.lib.feature_detection import detect_packages
from global.lib.config import PlanReviewConfig
```

---

## Solution Architecture

### Design Principles

1. **Relative Imports**: Use relative imports within the `lib/` package
   - Simple: No path manipulation needed
   - Portable: Works from any execution context
   - Consistent: Matches Taskwright's proven pattern

2. **Installation-Aware Structure**: Ensure installed lib/ directory works standalone
   - `~/.agentflow/lib/` contains all Python modules
   - Files can import from lib without path setup
   - Works with Claude's MCP server execution context

3. **No Path Manipulation**: Remove dependency on sys.path hacks
   - No PYTHONPATH environment variable needed
   - No sys.path.insert() calls
   - Pure Python package semantics

### Import Pattern Changes

```python
# BEFORE (current, broken after installation)
from installer.global.lib.feature_detection import detect_packages
from global.lib.config import PlanReviewConfig
from lib.utils.path_resolver import PathResolver

# AFTER (works everywhere)
from lib.feature_detection import detect_packages
from lib.config import PlanReviewConfig
from lib.utils.path_resolver import PathResolver
```

### Directory Structure Reference

```
installer/global/
├── lib/                          # Main library package
│   ├── __init__.py              # Package marker
│   ├── feature_detection.py      # Core library
│   ├── config/
│   │   ├── __init__.py
│   │   ├── config_schema.py
│   │   ├── defaults.py
│   │   └── plan_review_config.py
│   ├── metrics/
│   │   ├── __init__.py
│   │   ├── metrics_storage.py
│   │   ├── plan_review_metrics.py
│   │   └── plan_review_dashboard.py
│   └── utils/
│       ├── __init__.py
│       ├── file_operations.py
│       ├── json_serializer.py
│       └── path_resolver.py
├── commands/                     # Command specs (*.md files with embedded Python)
├── agents/                       # Agent specs (*.md files with embedded Python)
└── instructions/               # Instruction files (may reference lib)

# After installation to ~/.agentflow
~/.agentflow/
├── lib/                         # Copied lib/ directory
│   ├── __init__.py
│   ├── feature_detection.py
│   ├── config/
│   ├── metrics/
│   └── utils/
├── bin/
├── commands/
└── agents/
```

---

## Implementation Components

### 1. Library Files (Import Internal Dependencies)

**Files to Update**:
- `/installer/global/lib/feature_detection.py`
- `/installer/global/lib/config/config_schema.py`
- `/installer/global/lib/config/defaults.py`
- `/installer/global/lib/config/plan_review_config.py`
- `/installer/global/lib/metrics/plan_review_dashboard.py`
- `/installer/global/lib/metrics/plan_review_metrics.py`
- `/installer/global/lib/metrics/metrics_storage.py`
- `/installer/global/lib/utils/file_operations.py`
- `/installer/global/lib/utils/json_serializer.py`
- `/installer/global/lib/utils/path_resolver.py`

**Change Pattern**:
```python
# Intra-lib imports use relative imports
# From config/plan_review_config.py:
from .defaults import DEFAULT_CONFIG              # Sibling module
from .config_schema import ConfigSchema            # Sibling module
from ..utils import JsonSerializer, PathResolver   # Parent.child modules

# NOT:
from installer.global.lib.config.defaults import DEFAULT_CONFIG
from global.lib.utils import JsonSerializer
```

### 2. Command Files (Python Code Blocks)

**Files to Update**:
- `/installer/global/agents/code-reviewer.md` - Contains SpecDriftDetector import
- `/installer/global/agents/task-manager.md` - Contains multiple lib imports

**Change Pattern**:
```python
# BEFORE (in Markdown Python block)
from installer.global.commands.lib.spec_drift_detector import SpecDriftDetector

# AFTER
from lib.spec_drift_detector import SpecDriftDetector
# or (if module moved to lib/):
from lib.commands.spec_drift_detector import SpecDriftDetector
```

**Special Consideration**: Command/agent files with Python code blocks need imports that work when executed by Claude. The execution context will have `lib/` in the Python path when running via installed require-kit.

### 3. Python Scripts

**Files to Check**:
- `/installer/scripts/install.sh` - Verify lib/ files are copied correctly
- Any Python scripts in `/installer/scripts/` (if present)

**Verification**:
```bash
# In install.sh, verify this exists:
cp "$SCRIPT_DIR/global/lib/feature_detection.py" "$INSTALL_DIR/lib/"
# and for all lib/ modules
```

### 4. Path Resolver Utility

**File**: `/installer/global/lib/utils/path_resolver.py`

**Current Role**: Likely handles repository path resolution

**Action**:
- Review what paths it resolves
- Update to handle installed context (if needed)
- Consider if it's still needed (prefer simpler approach)
- Or keep it but ensure it doesn't break relative imports

---

## Implementation Sequence

### Phase 1: Analyze Current Imports (Pre-check)

```bash
# 1. Find all Python imports
grep -r "^from\|^import" /installer/global/lib --include="*.py" \
  | grep -v "^#" > /tmp/current_imports.txt

# 2. Find all absolute imports
grep -r "from installer\|from global\|import installer\|import global" \
  /installer/global --include="*.py" --include="*.md" \
  > /tmp/absolute_imports.txt

# 3. Check for sys.path manipulation
grep -r "sys.path\|PYTHONPATH" /installer --include="*.py" --include="*.sh" \
  > /tmp/path_manipulation.txt

# Results:
# - absolute_imports.txt should show what needs changing
# - path_manipulation.txt should be empty after fix
# - current_imports.txt verifies no circular dependencies
```

### Phase 2: Update Library Files

**Step 1**: Fix intra-package imports in lib/ (local relative imports)

Files to update in order (dependencies first):
1. `lib/__init__.py` - Ensure empty or minimal
2. `lib/utils/__init__.py` - Utility module initializer
3. `lib/utils/json_serializer.py` - No lib dependencies
4. `lib/utils/path_resolver.py` - May import others, review
5. `lib/utils/file_operations.py` - Check for lib imports
6. `lib/config/__init__.py` - Package initializer
7. `lib/config/defaults.py` - Likely no lib imports
8. `lib/config/config_schema.py` - May import from defaults
9. `lib/config/plan_review_config.py` - Imports from .defaults and .schema
10. `lib/metrics/__init__.py` - Package initializer
11. `lib/metrics/metrics_storage.py` - Check for imports
12. `lib/metrics/plan_review_metrics.py` - Imports from metrics_storage and config
13. `lib/metrics/plan_review_dashboard.py` - Check dependencies
14. `lib/feature_detection.py` - Check for lib imports

**Pattern**:
```python
# For same-level sibling (in same directory)
from .sibling_module import Something

# For child module (in subdirectory)
from .subdir.child_module import Something

# For parent module (one level up)
from ..module_name import Something

# For parent's sibling
from ..other_subdir.module import Something

# NEVER use:
# from installer.global.lib.X
# from global.lib.X
# from lib.X (only in external code, not within lib/)
```

### Phase 3: Update Command and Agent Files

**Step 1**: Find all Python code blocks in Markdown

```bash
grep -l "```python" /installer/global/agents/*.md /installer/global/commands/*.md
```

**Step 2**: Update each file's Python imports

Current files with imports to fix:
- `agents/code-reviewer.md`: `from installer.global.commands.lib.spec_drift_detector`
- `agents/task-manager.md`: Multiple `from installer.global.commands.lib.*`

**Pattern**:
```markdown
# In Markdown Python code blocks, use:
from lib.module_name import Something

# NOT:
from installer.global.commands.lib.module_name import Something
```

**Question**: If `spec_drift_detector` and others are in `commands/lib/`, should they be moved to main `lib/`?
- **Recommendation**: Yes, consolidate to main `lib/` for simpler imports
- Alternative: Update install.sh to copy `commands/lib/` content to `lib/`

### Phase 4: Verify Installation Process

**File**: `/installer/scripts/install.sh`

**Current State** (around line 202-210):
```bash
install_lib() {
    print_info "Installing library files..."

    if [ -f "$SCRIPT_DIR/global/lib/feature_detection.py" ]; then
        cp "$SCRIPT_DIR/global/lib/feature_detection.py" "$INSTALL_DIR/lib/" 2>/dev/null || true
    fi
    # ... other files
}
```

**Required Changes**:
1. Ensure ALL lib/ files are copied (not just feature_detection.py)
2. Preserve directory structure (config/, metrics/, utils/ subdirs)
3. Ensure __init__.py files are copied
4. Add installation of any commands/lib/ files (or consolidate first)

**Updated Pattern**:
```bash
install_lib() {
    print_info "Installing library files..."
    mkdir -p "$INSTALL_DIR/lib"

    # Copy entire lib directory structure
    if [ -d "$SCRIPT_DIR/global/lib" ]; then
        # Recursive copy preserving directory structure
        cp -r "$SCRIPT_DIR/global/lib/"* "$INSTALL_DIR/lib/" 2>/dev/null || true
        print_success "Library files installed"
    else
        print_error "Library directory not found"
    fi
}
```

### Phase 5: Testing Strategy

**Test 1**: Fresh curl installation (clean environment)
```bash
# Simulate curl installation
mkdir /tmp/test_install
cd /tmp/test_install
curl -sSL https://raw.githubusercontent.com/require-kit/require-kit/main/installer/scripts/install.sh | bash

# Verify
ls -la ~/.agentflow/lib/
python3 -c "from lib.feature_detection import detect_packages; print('Success!')"
```

**Test 2**: Git clone installation (no regression)
```bash
git clone https://github.com/require-kit/require-kit.git
cd require-kit
./installer/scripts/install.sh

# Verify same as Test 1
```

**Test 3**: Relative imports work
```bash
cd ~/.agentflow/lib
python3 -c "from feature_detection import detect_packages; print('Success!')"

cd ~/.agentflow
python3 -c "from lib.feature_detection import detect_packages; print('Success!')"
```

**Test 4**: Taskwright integration
```bash
# If taskwright installed, verify require-kit detection works
taskwright detect-packages
```

**Test 5**: Import validation (no cycles, no missing deps)
```python
# Create test script that imports all key modules
import sys
sys.path.insert(0, '~/.agentflow')

from lib.feature_detection import detect_packages
from lib.config import PlanReviewConfig
from lib.metrics import PlanReviewMetrics
from lib.utils import PathResolver, JsonSerializer

print("All imports successful!")
```

---

## Dependency Analysis

### Internal Library Dependencies

```
feature_detection.py
  └─ [no internal lib dependencies, stdlib only]

config/config_schema.py
  └─ [no internal lib dependencies, pydantic only]

config/defaults.py
  └─ [no internal lib dependencies]

config/plan_review_config.py
  ├─ config/defaults.py (sibling: from .defaults)
  ├─ config/config_schema.py (sibling: from .config_schema)
  └─ utils/path_resolver.py (parent: from ..utils)

metrics/metrics_storage.py
  ├─ config/plan_review_config.py (from ..config)
  └─ utils/json_serializer.py (from ..utils)

metrics/plan_review_metrics.py
  ├─ metrics/metrics_storage.py (sibling: from .metrics_storage)
  └─ config/plan_review_config.py (parent: from ..config)

metrics/plan_review_dashboard.py
  ├─ metrics/metrics_storage.py (sibling: from .metrics_storage)
  └─ config/plan_review_config.py (parent: from ..config)

utils/file_operations.py
  └─ [no internal lib dependencies]

utils/json_serializer.py
  └─ [no internal lib dependencies]

utils/path_resolver.py
  └─ [likely no internal lib dependencies, but verify]
```

**No Circular Dependencies**: Dependencies flow downward (utils used by everything, config used by metrics, etc.)

---

## Code Pattern Examples

### Example 1: Within lib/ Package (Relative Imports)

**File**: `/installer/global/lib/config/plan_review_config.py`

```python
# BEFORE
import os
from pathlib import Path
from installer.global.lib.config.defaults import DEFAULT_CONFIG
from installer.global.lib.config.config_schema import ConfigSchema, ThresholdConfig
from installer.global.lib.utils import JsonSerializer, PathResolver

# AFTER
import os
from pathlib import Path
from .defaults import DEFAULT_CONFIG
from .config_schema import ConfigSchema, ThresholdConfig
from ..utils import JsonSerializer, PathResolver
```

### Example 2: Metrics Module with Multiple Imports

**File**: `/installer/global/lib/metrics/plan_review_metrics.py`

```python
# BEFORE
from installer.global.lib.metrics.metrics_storage import MetricsStorage
from installer.global.lib.config import PlanReviewConfig

# AFTER
from .metrics_storage import MetricsStorage
from ..config import PlanReviewConfig
```

### Example 3: Command File with Python Block

**File**: `/installer/global/agents/code-reviewer.md`

```markdown
### Step 1: Spec Drift Detection

```python
# BEFORE
from installer.global.commands.lib.spec_drift_detector import (
    SpecDriftDetector,
    format_drift_report
)

# AFTER (if spec_drift_detector moved to lib/)
from lib.spec_drift_detector import (
    SpecDriftDetector,
    format_drift_report
)

# OR (if keeping in commands/lib/, ensure install.sh copies it)
from lib.commands.spec_drift_detector import (
    SpecDriftDetector,
    format_drift_report
)
```

---

## Decision Points

### 1. Location of Command-Specific Libraries

**Decision**: Should `commands/lib/*.py` modules be:

**Option A** (Recommended): Consolidate into main `lib/`
- Simpler imports: `from lib.spec_drift_detector`
- Single lib directory to maintain
- Easier installation
- Preferred

**Option B**: Keep in `commands/lib/`, copy to installed `lib/commands/`
- Logical separation of concerns
- More imports: `from lib.commands.spec_drift_detector`
- Requires more install.sh changes
- Not preferred

**Recommendation**: Go with Option A - consolidate to main lib/ and update all imports

### 2. Path Resolver Utility

**Decision**: Should `utils/path_resolver.py` be kept?

**Current Use**: Likely resolves repository paths for development/testing

**Recommendation**:
- Keep the file but review its usage
- Update it to work with installed context (not repo paths)
- Or mark as "development only" if not needed post-installation
- Verify it's not used in critical paths

### 3. Python Path Setup in install.sh

**Decision**: Need any PYTHONPATH or sys.path setup?

**Answer**: No
- Installed location `~/.agentflow/lib/` should be in Python path naturally
- Or Claude's MCP execution context handles it
- Remove any path manipulation from install.sh

---

## Acceptance Criteria Mapping

| Criterion | Implementation | Verification |
|-----------|-----------------|--------------|
| All `from installer.global.lib.X` imports updated to `from lib.X` | Phase 2 library updates | grep finds no matches |
| All `from global.lib.X` imports updated to `from lib.X` | Phase 2 library updates | grep finds no matches |
| No repository path resolution code remains | Phase 4 path verification | Review path_resolver.py usage |
| Fresh curl installation succeeds | Phase 4 install verification | Test 1 passes |
| Git clone installation still works | Phase 4 install verification | Test 2 passes |
| Taskwright integration works | Phase 5 integration test | Test 4 passes |
| No Python import errors | Phase 5 import validation | Test 5 passes |
| Pattern matches Taskwright | Design & Phase 2 | Code review against taskwright |

---

## Risk Mitigation

### Risk 1: Breaking Existing Installations
**Impact**: Users with git clones in ~/Projects/require-kit
**Mitigation**:
- Relative imports work from both repo and installed locations
- Git clone still works because lib/ at installer/global/lib/ is copied

### Risk 2: Circular Import Dependencies
**Mitigation**:
- Dependency analysis shows no cycles
- Test with import validation script
- Monitor import warnings

### Risk 3: Missing File Copies During Installation
**Impact**: Fresh curl install missing lib files
**Mitigation**:
- Use recursive cp with proper directory structure
- Verify all __init__.py files copied
- Add size/count validation in install.sh

### Risk 4: Commands/Agents with Embedded Python
**Impact**: If not updated, Python blocks will fail
**Mitigation**:
- Find all Python code blocks in .md files
- Update each import statement
- Test by executing command code

---

## Files to Modify

### Library Files (20 files)
1. `/installer/global/lib/__init__.py` - Verify empty
2. `/installer/global/lib/feature_detection.py` - Verify no lib imports
3. `/installer/global/lib/config/__init__.py`
4. `/installer/global/lib/config/config_schema.py`
5. `/installer/global/lib/config/defaults.py`
6. `/installer/global/lib/config/plan_review_config.py`
7. `/installer/global/lib/metrics/__init__.py`
8. `/installer/global/lib/metrics/metrics_storage.py`
9. `/installer/global/lib/metrics/plan_review_metrics.py`
10. `/installer/global/lib/metrics/plan_review_dashboard.py`
11. `/installer/global/lib/utils/__init__.py`
12. `/installer/global/lib/utils/file_operations.py`
13. `/installer/global/lib/utils/json_serializer.py`
14. `/installer/global/lib/utils/path_resolver.py`

### Command/Agent Files (2-5 files)
1. `/installer/global/agents/code-reviewer.md` - Update Python blocks
2. `/installer/global/agents/task-manager.md` - Update Python blocks
3. Potential others (check with grep)

### Installation Files (1 file)
1. `/installer/scripts/install.sh` - Ensure all lib files copied

---

## Success Criteria

All of the following must be true:

- [ ] All library files use relative imports (`from .module`, `from ..parent.module`)
- [ ] No `from installer.global`, `from global`, or `from lib.X` in lib/ files themselves
- [ ] Command/agent files updated with proper relative imports
- [ ] install.sh copies all lib files recursively with structure preserved
- [ ] Fresh curl installation succeeds in clean environment
- [ ] Git clone installation not broken (backward compatible)
- [ ] Taskwright integration detects require-kit successfully
- [ ] No Python import errors when executing commands/agents
- [ ] All tests pass (Test 1-5)

---

## Next Steps

1. **Review this plan** - Confirm approach and decisions
2. **Phase 1 Analysis** - Run grep commands to identify all files needing changes
3. **Phase 2 Implementation** - Update library files with relative imports
4. **Phase 3 Updates** - Fix command/agent files
5. **Phase 4 Verification** - Update install.sh and verify copying
6. **Phase 5 Testing** - Execute all test scenarios
7. **Documentation** - Update INTEGRATION-GUIDE.md if needed

---

## References

- Taskwright relative imports pattern: `from lib.module_name`
- Python relative imports: [PEP 328](https://www.python.org/dev/peps/pep-0328/)
- Package structure: [Python Packaging Guide](https://packaging.python.org/)

---

**Document Version**: 1.0
**Created**: 2025-11-29
**Status**: Ready for Implementation
**Next Review**: After Phase 1 Analysis
