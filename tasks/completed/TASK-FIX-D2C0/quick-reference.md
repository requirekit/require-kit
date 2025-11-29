# TASK-FIX-D2C0: Quick Reference Card

## At a Glance

**Task**: Convert Python imports from absolute paths to relative paths
**Priority**: Critical (Launch Blocker)
**Time**: 1-2 hours
**Key Change**: `from installer.global.lib.X` → `from lib.X`

---

## The Problem in 30 Seconds

Require-kit uses absolute imports that reference repository paths. When installed via curl to `~/.agentflow/`, these paths don't exist, causing import failures.

## The Solution in 30 Seconds

Use Python's native relative import pattern. Files in `lib/config/` import from `..utils` (parent package), files in `lib/metrics/` import from `..config`, etc. External code just does `from lib.X import Y`.

---

## Import Conversion Table

| Location | Old Pattern | New Pattern | Why |
|----------|------------|------------|-----|
| `lib/config/plan_review_config.py` | `from utils import X` | `from ..utils import X` | Go up to lib/, then into utils/ |
| `lib/metrics/plan_review_metrics.py` | `from config import X` | `from ..config import X` | Go up to lib/, then into config/ |
| `lib/metrics/metrics_storage.py` | `from config import X` | `from ..config import X` | Same pattern |
| `agents/code-reviewer.md` | `from installer.global.commands.lib.X` | `from lib.X import Y` | External code: simple absolute to lib/ |
| `installer/scripts/install.sh` | `cp file1.py file2.py file3.py` | `cp -r lib/* target/lib/` | Copy whole directory structure |

---

## Files to Update (The Whole List)

### Library Files (14 files to check/update)
```
installer/global/lib/
├── __init__.py                          # Verify exists
├── feature_detection.py                 # Verify no lib imports
├── config/
│   ├── __init__.py                      # Create
│   ├── config_schema.py                 # Verify no lib imports
│   ├── defaults.py                      # Verify no lib imports
│   └── plan_review_config.py            # FIX: from utils → from ..utils
├── metrics/
│   ├── __init__.py                      # Create
│   ├── metrics_storage.py               # FIX: from config/utils → from ../
│   ├── plan_review_metrics.py           # FIX: from config → from ..config
│   └── plan_review_dashboard.py         # Check imports
└── utils/
    ├── __init__.py                      # Create
    ├── file_operations.py               # Verify no lib imports
    ├── json_serializer.py               # Verify no lib imports
    └── path_resolver.py                 # Check imports
```

### Command/Agent Files (2-5 files with Python blocks)
```
installer/global/
├── agents/code-reviewer.md              # FIX: from installer.global.commands.lib → from lib
├── agents/task-manager.md               # FIX: same pattern
└── Check all *.md files for Python code blocks
```

### Installation File (1 file)
```
installer/scripts/install.sh             # Update install_lib() function
```

---

## Implementation Checklist

### Before You Start
- [ ] Verify you're in: `/Users/richardwoollcott/Projects/appmilla_github/require-kit`
- [ ] Run: `git status` (should be clean)
- [ ] Run: `grep -r "from installer.global" installer/global --include="*.py" --include="*.md"` (to see what needs fixing)

### Phase 1: Library Files (30 min)
- [ ] Edit `lib/config/plan_review_config.py` - Fix `from utils` → `from ..utils`
- [ ] Edit `lib/metrics/plan_review_metrics.py` - Fix `from config` → `from ..config`
- [ ] Edit `lib/metrics/metrics_storage.py` - Fix both config and utils imports
- [ ] Edit `lib/metrics/plan_review_dashboard.py` - Check and fix if needed
- [ ] Create/verify all `__init__.py` files in all directories
- [ ] Review `lib/utils/path_resolver.py` - ensure it doesn't have broken imports

### Phase 2: Command/Agent Files (15 min)
- [ ] Edit `agents/code-reviewer.md` - Fix `from installer.global.commands.lib` → `from lib`
- [ ] Edit `agents/task-manager.md` - Same fix
- [ ] Search for any other .md files with Python blocks: `grep -l "from installer.global" agents/*.md commands/*.md`
- [ ] Fix any found

### Phase 3: Install Script (10 min)
- [ ] Edit `installer/scripts/install.sh`
- [ ] Find `install_lib()` function
- [ ] Replace file-by-file copy with: `cp -r "$SCRIPT_DIR/global/lib/"* "$INSTALL_DIR/lib/"`

### Phase 4: Verification (10 min)
- [ ] Run: `grep -r "from installer.global\|from global.lib" installer/global --include="*.py" --include="*.md"` (should be empty)
- [ ] Run: `find installer/global/lib -type d | while read d; do [ ! -f "$d/__init__.py" ] && echo "MISSING: $d/__init__.py"; done` (should be empty)
- [ ] Run test: See Testing section

### Phase 5: Commit (5 min)
- [ ] Stage: `git add -A`
- [ ] Commit: See git commit template in Implementation Guide
- [ ] Push: `git push origin RichWoollcott/la-paz-v1`

---

## Testing Quick Commands

```bash
# After making changes, run these to verify

# 1. Check no bad imports remain
grep -r "from installer.global\|from global.lib" installer/global --include="*.py" --include="*.md"
# Should output: NOTHING

# 2. Verify __init__.py files
find installer/global/lib -type d | while read d; do
  [ ! -f "$d/__init__.py" ] && echo "MISSING: $d/__init__.py"
done
# Should output: NOTHING

# 3. Test imports work
python3 << 'EOF'
import sys
sys.path.insert(0, 'installer/global/lib')
from feature_detection import detect_packages
print("✓ Imports work!")
EOF

# 4. Test git clone install
cd /tmp && cp -r /path/to/require-kit . && cd require-kit/installer/scripts && bash install.sh
# Then verify: ls ~/.agentflow/lib/config/ (should show files)
```

---

## Common Mistakes to Avoid

| Mistake | Problem | Fix |
|---------|---------|-----|
| `from config import X` in lib/metrics/ | Breaks - config not in path | `from ..config import X` |
| `from utils import X` in lib/config/ | Breaks - utils not in path | `from ..utils import X` |
| Missing __init__.py in lib/config/ | Python doesn't recognize it as package | Create empty file: `touch lib/config/__init__.py` |
| Only copying feature_detection.py in install | Misses config/, metrics/, utils/ dirs | Use `cp -r lib/* target/lib/` |
| Leaving `from installer.global` in .md files | Fails when executed | Change to `from lib.X` |
| Not updating agent/command files | Commands still break | Search all .md files for "from installer" |

---

## Import Pattern Quick Reference

### Within lib/ Package (Relative)
```python
# In lib/config/plan_review_config.py:
from .defaults import DEFAULT_CONFIG            # ✓ Same directory
from .config_schema import ConfigSchema          # ✓ Same directory
from ..utils import JsonSerializer, PathResolver # ✓ Parent package

# NOT:
from installer.global.lib.config.defaults import DEFAULT_CONFIG  # ✗ Absolute
from utils import JsonSerializer                 # ✗ Path not found
```

### External Code (Absolute to lib/)
```python
# In Python script, agent, or command:
from lib.feature_detection import detect_packages        # ✓ Works
from lib.config import PlanReviewConfig                  # ✓ Works
from lib.metrics import PlanReviewMetrics                # ✓ Works

# NOT:
from installer.global.lib.feature_detection import *    # ✗ Not found after install
from global.lib.config import PlanReviewConfig           # ✗ Not found after install
```

---

## File Edit Examples

### Example 1: Fix lib/config/plan_review_config.py
```diff
  import os
  from typing import Optional, Dict, Any, Literal
  from pathlib import Path

  from .defaults import DEFAULT_CONFIG
  from .config_schema import ConfigSchema, ThresholdConfig
- from utils import JsonSerializer, PathResolver
+ from ..utils import JsonSerializer, PathResolver
```

### Example 2: Fix lib/metrics/plan_review_metrics.py
```diff
  from datetime import datetime
  from typing import Dict, Any, Optional, Literal

  from .metrics_storage import MetricsStorage
- from config import PlanReviewConfig
+ from ..config import PlanReviewConfig
```

### Example 3: Fix agents/code-reviewer.md
```diff
  ```python
- from installer.global.commands.lib.spec_drift_detector import (
+ from lib.spec_drift_detector import (
      SpecDriftDetector,
      format_drift_report
  )
  ```
```

### Example 4: Fix install.sh
```diff
  install_lib() {
      print_info "Installing library files..."
-     if [ -f "$SCRIPT_DIR/global/lib/feature_detection.py" ]; then
-         cp "$SCRIPT_DIR/global/lib/feature_detection.py" "$INSTALL_DIR/lib/" 2>/dev/null || true
-     fi
+     mkdir -p "$INSTALL_DIR/lib"
+     if [ -d "$SCRIPT_DIR/global/lib" ]; then
+         cp -r "$SCRIPT_DIR/global/lib/"* "$INSTALL_DIR/lib/" 2>/dev/null || true
+     fi
  }
```

---

## Success Criteria (Just These 4 Things)

1. **No absolute imports remain**
   ```bash
   grep -r "from installer.global\|from global.lib" installer/global --include="*.py" --include="*.md"
   # Returns: NOTHING (empty output)
   ```

2. **All __init__.py files exist**
   ```bash
   ls installer/global/lib/__init__.py
   ls installer/global/lib/config/__init__.py
   ls installer/global/lib/metrics/__init__.py
   ls installer/global/lib/utils/__init__.py
   # All 4 should exist
   ```

3. **Imports work**
   ```bash
   cd /tmp && cp -r /path/to/require-kit . && cd require-kit
   python3 -c "import sys; sys.path.insert(0, 'installer/global/lib'); from feature_detection import detect_packages; print('OK')"
   # Should print: OK
   ```

4. **Installation creates lib directory**
   ```bash
   rm -rf ~/.agentflow && installer/scripts/install.sh
   ls ~/.agentflow/lib/config/ | grep -q "plan_review_config.py"
   # Should return success (file exists)
   ```

---

## Estimated Time by Phase

| Phase | Minutes |
|-------|---------|
| Library files | 30 |
| Command/agent files | 15 |
| Install script | 10 |
| Verification | 10 |
| Testing | 15 |
| Git commit & push | 5 |
| **Total** | **85 minutes (1.5 hours)** |

---

## Key Files Location

```
/Users/richardwoollcott/Projects/appmilla_github/require-kit/
├── installer/
│   ├── global/
│   │   ├── lib/                    <- Library files to fix
│   │   ├── agents/                 <- Agent markdown files to fix
│   │   └── commands/               <- Command markdown files to fix
│   └── scripts/
│       └── install.sh              <- Installation script to fix
└── .conductor/la-paz-v1/           <- This folder (documentation)
    ├── TASK-FIX-D2C0-IMPLEMENTATION-PLAN.md     <- Full plan
    ├── TASK-FIX-D2C0-TECHNICAL-SPEC.md          <- Technical details
    ├── TASK-FIX-D2C0-IMPLEMENTATION-GUIDE.md    <- Step by step
    └── TASK-FIX-D2C0-QUICK-REFERENCE.md         <- This file
```

---

## Need Help?

| Problem | Solution | Time |
|---------|----------|------|
| Which files to change? | See "Files to Update" section above | 2 min |
| How to fix an import? | See "Import Pattern Quick Reference" | 1 min |
| What does the code look like? | See "File Edit Examples" | 2 min |
| How do I test? | See "Testing Quick Commands" | 5 min |
| Detailed step-by-step? | Read TASK-FIX-D2C0-IMPLEMENTATION-GUIDE.md | 30 min |
| Architecture questions? | Read TASK-FIX-D2C0-IMPLEMENTATION-PLAN.md | 20 min |
| Technical specifications? | Read TASK-FIX-D2C0-TECHNICAL-SPEC.md | 15 min |

---

## Git Commit Message Template

```
fix: convert absolute imports to relative imports for installation compatibility

- Update all lib/ module imports to use relative imports
- Fix config/plan_review_config.py to import from ..utils
- Fix metrics modules to import from ..config
- Update agent files to import from lib.X pattern
- Update install.sh to use recursive copy for lib/ directory
- Add/verify __init__.py files in all lib/ subdirectories

Fixes TASK-FIX-D2C0 - Implements relative imports for Python path fix
Matches Taskwright import pattern for consistency
```

---

## Reference Documents

This quick reference is a summary of:

1. **TASK-FIX-D2C0-IMPLEMENTATION-PLAN.md** (25 pages)
   - Full problem analysis, architecture decisions, risk mitigation
   - Read if you need the "why" and "how"

2. **TASK-FIX-D2C0-TECHNICAL-SPEC.md** (20 pages)
   - Exact file locations, code before/after, testing procedures
   - Read if you want technical depth

3. **TASK-FIX-D2C0-IMPLEMENTATION-GUIDE.md** (25 pages)
   - Step-by-step instructions with commands to run
   - Read if you want to follow along

4. **TASK-FIX-D2C0-SUMMARY.md** (15 pages)
   - Executive summary, component structure, effort estimates
   - Read for overview

5. **TASK-FIX-D2C0-QUICK-REFERENCE.md** (This file)
   - Quick lookup table, common mistakes, file examples
   - Use as your working reference while implementing

---

**Start here**: Follow the Implementation Checklist section above
**Time estimate**: 1.5 hours (85 minutes)
**Difficulty**: Moderate (straightforward changes, but many files)
**Risk**: Low (no circular dependencies, backward compatible)

Good luck!
