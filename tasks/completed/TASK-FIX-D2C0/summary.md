# TASK-FIX-D2C0: Implementation Approach Summary

## Executive Summary

This is a Python import refactoring task to convert all absolute repository paths (`from installer.global.lib.X`) to relative installed paths (`from lib.X`), matching Taskwright's proven pattern and ensuring the system works correctly after curl installation.

**Priority**: Critical (Launch Blocker)
**Complexity**: 4/10
**Estimated Effort**: 1-2 hours
**Impact**: Unblocks successful curl-based installation and integration with Taskwright

---

## Problem

The require-kit codebase uses absolute imports that reference repository structure:
- Library files use `from global.lib.X` or `from utils import X` (broken in installed context)
- Command/agent files use `from installer.global.commands.lib.X` (references non-existent path)
- Installation script only copies individual files instead of maintaining directory structure

**Result**: The system fails when installed via curl because the absolute import paths don't exist.

---

## Solution Architecture

### Core Design Pattern

**Adopt Relative Imports**: Convert to Python's native relative import pattern

```python
# BEFORE (fails after installation)
from installer.global.lib.feature_detection import detect_packages
from global.lib.config import PlanReviewConfig
from utils import JsonSerializer

# AFTER (works everywhere)
from lib.feature_detection import detect_packages
from lib.config import PlanReviewConfig
from ..utils import JsonSerializer
```

### Key Components

1. **Within lib/ package**: Use relative imports (`.sibling`, `..parent.child`)
   - Files in `lib/config/` → import from `..utils` or `.defaults`
   - Files in `lib/metrics/` → import from `..config` or `.metrics_storage`
   - Enables self-contained package functionality

2. **Command/Agent files**: Use lib/ imports directly
   - Markdown Python blocks → `from lib.module_name import Class`
   - Executed in context where lib/ is in Python path

3. **Installation**: Recursive copy of lib/ directory structure
   - All subdirectories (config/, metrics/, utils/)
   - All __init__.py package markers
   - All Python modules
   - Preserves structure for relative imports to work

### Architecture Decisions

1. **No sys.path manipulation**: Remove dependency on path setup
   - Cleaner code
   - Works in any execution context (CLI, Claude MCP, etc.)
   - Matches Taskwright pattern

2. **Consolidate command libraries**: Move commands/lib/*.py to lib/
   - Simpler import paths
   - Single lib directory to maintain
   - Reduces install.sh complexity

3. **Preserve package structure**: All directories get __init__.py
   - Makes lib/ a proper Python package
   - Enables both relative imports (internal) and absolute imports (external)
   - Works with Python import semantics

---

## Implementation Scope

### Files to Modify

**Library Files (14 files)**:
- `lib/__init__.py` - Create/verify empty package marker
- `lib/feature_detection.py` - Verify no internal lib imports
- `lib/config/__init__.py` - Create and export PlanReviewConfig
- `lib/config/config_schema.py` - Verify schema-only module
- `lib/config/defaults.py` - Verify constants-only module
- `lib/config/plan_review_config.py` - Fix: `from utils` → `from ..utils`
- `lib/metrics/__init__.py` - Create and export metrics classes
- `lib/metrics/metrics_storage.py` - Fix: import from ..config and ..utils
- `lib/metrics/plan_review_metrics.py` - Fix: import from ..config
- `lib/metrics/plan_review_dashboard.py` - Fix: import statements if present
- `lib/utils/__init__.py` - Create and export utilities
- `lib/utils/file_operations.py` - Verify no internal lib imports
- `lib/utils/json_serializer.py` - Verify standalone utility
- `lib/utils/path_resolver.py` - Review and update if needed

**Command/Agent Files (2-5 files)**:
- `agents/code-reviewer.md` - Update Python block: `from installer.global.commands.lib.*` → `from lib.*`
- `agents/task-manager.md` - Update Python blocks with same pattern
- Other agent/command files with Python code blocks (find with grep)

**Installation Files (1 file)**:
- `installer/scripts/install.sh` - Replace file-by-file copy with recursive directory copy

### Change Pattern Across File Types

**Library files (*.py) - Within lib/ package**:
```python
# BEFORE
from utils import JsonSerializer
from config import PlanReviewConfig
from installer.global.lib.utils import PathResolver

# AFTER
from ..utils import JsonSerializer              # Parent package, sibling
from ..config import PlanReviewConfig            # Parent package, sibling
from ..utils import PathResolver                 # Consistent pattern
```

**Command/Agent files (*.md) - Python code blocks**:
```python
# BEFORE
from installer.global.commands.lib.spec_drift_detector import SpecDriftDetector

# AFTER
from lib.spec_drift_detector import SpecDriftDetector
```

**Installation script (install.sh)**:
```bash
# BEFORE
cp "$SCRIPT_DIR/global/lib/feature_detection.py" "$INSTALL_DIR/lib/" 2>/dev/null || true

# AFTER
cp -r "$SCRIPT_DIR/global/lib/"* "$INSTALL_DIR/lib/" 2>/dev/null || true
```

---

## Testing Strategy

### Test Levels

1. **Import Validation**: Verify all imports parse correctly
   - Run Python import checker script
   - Verify no circular dependencies
   - Confirm no missing modules

2. **Fresh Installation Test**: Simulate curl download and install
   - Clean ~/.agentflow directory
   - Run install script
   - Verify all lib files in ~/.agentflow/lib/
   - Test imports from ~/.agentflow context

3. **Git Clone Test**: Verify backward compatibility
   - Repository clone still works
   - Relative imports work from repo structure
   - No regressions from changes

4. **Integration Test**: Verify Taskwright detection
   - If taskwright installed, require-kit detection works
   - Command execution succeeds
   - No import errors in executing context

### Success Metrics

- Zero occurrences of `from installer.global`, `from global.lib`, or `from utils` in lib/ files
- All library files use relative imports (`.something` or `..something`)
- All __init__.py files present in lib/ and subdirectories
- Fresh installation creates complete lib/ directory structure
- All tests pass without import errors

---

## Key Technical Decisions

### Decision 1: Relative vs. Absolute Imports

**Choice**: Relative imports within lib/ package

**Rationale**:
- Works in any execution context (CLI, installed, repo, tests)
- Follows Python best practices for packages
- Matches Taskwright pattern (proven approach)
- Simpler than managing sys.path or PYTHONPATH

**Implementation**:
- Use `.module` for siblings in same directory
- Use `..parent.module` for parent package access
- Result: self-contained, portable package

---

### Decision 2: Command Library Consolidation

**Choice**: Move commands/lib/*.py to lib/

**Rationale**:
- Single lib directory reduces maintenance
- Simpler imports: `from lib.X` not `from lib.commands.X`
- Easier installation (one cp -r command)
- Aligns with Taskwright structure

**Implementation**:
- Copy commands/lib/*.py files to lib/
- Update all import statements in agents/commands
- Update install.sh (one recursive copy)
- Document in migration notes

---

### Decision 3: Package Structure

**Choice**: Maintain subdirectories with __init__.py files

**Rationale**:
- Logical grouping (config, metrics, utils)
- Enables relative imports between packages
- Allows re-exports for convenient external API
- Standard Python package structure

**Implementation**:
- Create __init__.py in each directory
- Re-export key classes in __init__.py
- Enables: `from lib.config import PlanReviewConfig`

---

## Component Structure

```
installer/global/
├── lib/                              # Main library package
│   ├── __init__.py                   # Package marker
│   ├── feature_detection.py          # Standalone core module
│   │
│   ├── config/                       # Configuration subpackage
│   │   ├── __init__.py              # Exports: PlanReviewConfig
│   │   ├── config_schema.py         # Pydantic schemas (standalone)
│   │   ├── defaults.py              # Constants (standalone)
│   │   └── plan_review_config.py    # Main config class
│   │       └─ imports: from ..utils (parent package)
│   │
│   ├── metrics/                      # Metrics subpackage
│   │   ├── __init__.py              # Exports: PlanReviewMetrics, MetricsStorage
│   │   ├── metrics_storage.py       # Storage layer
│   │   │   └─ imports: from ..config, ..utils (parent packages)
│   │   ├── plan_review_metrics.py   # High-level API
│   │   │   └─ imports: from .metrics_storage, ..config (this dir + parent)
│   │   └── plan_review_dashboard.py # Dashboard view
│   │       └─ imports: from ..config (parent package)
│   │
│   └── utils/                        # Utilities subpackage
│       ├── __init__.py              # Exports: JsonSerializer, PathResolver
│       ├── file_operations.py       # File utilities (standalone)
│       ├── json_serializer.py       # JSON utilities (standalone)
│       └── path_resolver.py         # Path utilities (standalone)
│
├── agents/                           # Agent specifications (*.md)
│   ├── code-reviewer.md             # Uses: from lib.spec_drift_detector
│   └── task-manager.md              # Uses: from lib.micro_task_detector etc
│
└── commands/                         # Command specifications (*.md)
    └── Various *.md files           # May have Python blocks
```

### Import Flow Diagram

```
External Context (CLI, Claude, etc.)
  │
  └─> import lib.feature_detection
  └─> import lib.config.PlanReviewConfig
  └─> import lib.metrics.PlanReviewMetrics
  └─> import lib.utils.JsonSerializer

Within lib/ package:
  lib/config/plan_review_config.py
    └─ from ..utils import JsonSerializer      ✓ Works (parent package)
    └─ from .defaults import DEFAULT_CONFIG    ✓ Works (same package)

  lib/metrics/plan_review_metrics.py
    └─ from .metrics_storage import *          ✓ Works (same package)
    └─ from ..config import PlanReviewConfig   ✓ Works (parent package)
```

---

## Risk Analysis & Mitigation

### Risk 1: Breaking Existing Git Clone Installations
**Severity**: Medium
**Mitigation**: Relative imports work from repository structure too
- lib/ at `installer/global/lib/` is copied to install location
- Relative imports function identically in both contexts

### Risk 2: Missing __init__.py Files
**Severity**: High
**Mitigation**: Explicit creation of all __init__.py files
- Include in implementation checklist
- Verify in git commit
- Test in validation script

### Risk 3: Circular Import Dependencies
**Severity**: Medium
**Mitigation**: Dependency analysis shows no cycles
- config (no deps within lib)
- utils (no deps within lib)
- metrics depends on config (acyclic)
- All imports flow downward (no circular refs)

### Risk 4: Installation Script Not Copying All Files
**Severity**: High
**Mitigation**: Use recursive directory copy instead of individual files
- `cp -r $SCRIPT_DIR/global/lib/* $INSTALL_DIR/lib/`
- Preserves directory structure automatically
- Catches any new files added to lib/

---

## Acceptance Criteria

All of the following must be satisfied:

- [ ] Zero absolute imports remain in lib/ files
  - No `from installer.global`, `from global.lib`, `from utils` in lib/
  - No `from config`, `from metrics` in lib/ (use relative)

- [ ] All command/agent files updated
  - No `from installer.global.commands.lib` in *.md files
  - All use `from lib.X` pattern

- [ ] Installation process verified
  - install.sh uses recursive copy
  - All subdirectories copied
  - All __init__.py files present

- [ ] Tests pass
  - Fresh curl installation succeeds
  - Git clone installation not broken
  - Imports work in installed context
  - No import errors during execution

- [ ] Taskwright integration works
  - If taskwright present, detection succeeds
  - No conflicting imports or paths

---

## Files Delivered

This implementation approach includes three comprehensive documents:

1. **TASK-FIX-D2C0-IMPLEMENTATION-PLAN.md** (This file's parent)
   - Complete problem analysis
   - Architecture decisions
   - Phase-by-phase implementation plan
   - Risk mitigation strategies
   - Dependency analysis

2. **TASK-FIX-D2C0-TECHNICAL-SPEC.md**
   - Exact file locations
   - Current vs. target code patterns
   - Import validation methods
   - Testing checklist
   - Consolidation decision details

3. **TASK-FIX-D2C0-IMPLEMENTATION-GUIDE.md**
   - Step-by-step instructions
   - Command-by-command execution
   - Troubleshooting guide
   - Quick reference tables
   - Success criteria checklist

---

## Implementation Effort Estimate

| Phase | Task | Time |
|-------|------|------|
| 1 | Pre-flight analysis | 15 min |
| 2 | Update library files | 30 min |
| 3 | Update command/agent files | 15 min |
| 4 | Update install.sh | 10 min |
| 5 | Verification and testing | 30 min |
| **Total** | | **1.5-2 hours** |

---

## Next Steps

1. **Review this approach**: Confirm architecture decisions
2. **Execute implementation**: Follow TASK-FIX-D2C0-IMPLEMENTATION-GUIDE.md
3. **Run tests**: All test scenarios in Step 7
4. **Create commit**: Document changes as described
5. **Merge to main**: Complete the launch blocker

---

## Architecture Pattern Reference

This implementation follows these established patterns:

| Pattern | Source | Applied As |
|---------|--------|------------|
| Relative imports | PEP 328 (Python standard) | lib/ package structure |
| Package structure | Python packaging guide | config/, metrics/, utils/ subdirs |
| Installation | Taskwright pattern | recursive lib/ copy |
| Testing | Standard practice | import validation + integration tests |

---

## Related Documentation

- **TASK-FIX-D2C0-IMPLEMENTATION-PLAN.md**: Detailed plan with architecture decisions
- **TASK-FIX-D2C0-TECHNICAL-SPEC.md**: Technical specifications and exact changes
- **TASK-FIX-D2C0-IMPLEMENTATION-GUIDE.md**: Step-by-step execution guide
- **INTEGRATION-GUIDE.md**: How require-kit integrates with taskwright

---

## Summary

This refactoring converts require-kit to use Python's native relative import pattern, matching Taskwright's proven approach. The changes are straightforward (convert absolute paths to relative imports), low-risk (no circular dependencies), and enable the system to function correctly after curl-based installation. Implementation time is 1-2 hours with clear test criteria for validation.

The architecture maintains logical package structure while enabling complete independence from repository paths, ensuring the system works in any execution context (CLI, installed, Taskwright integration, Claude MCP, etc.).

---

**Document Version**: 1.0
**Created**: 2025-11-29
**Status**: Ready for Review and Implementation
**Task ID**: TASK-FIX-D2C0
**Priority**: Critical (Launch Blocker)
