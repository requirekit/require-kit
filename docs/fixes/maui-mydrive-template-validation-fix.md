# MAUI-MyDrive Template Validation Fix

## Issue Summary

**Date**: 2025-10-18
**Severity**: Medium
**Impact**: Local maui-mydrive template showed as invalid in `agentecflow doctor`

## Problem Description

After following the MAUI-MyDrive setup guide, running `agentecflow doctor` in the MyDrive project showed:

```bash
Local Templates:
  ✓ Project context found: /Users/richardwoollcott/Projects/appmilla_github/DeCUK.Mobile.MyDrive
  ✓ 1 local templates available

  Available local templates:
    ✗ maui-mydrive (missing CLAUDE.md)
```

Then after fixing CLAUDE.md:

```bash
    ✗ maui-mydrive (missing templates/)
```

### Root Causes

1. **Missing CLAUDE.md file** at template root
   - TASK-011G created `docs/README.md` but not root-level `CLAUDE.md`
   - Template validator expects `CLAUDE.md` at `<template>/CLAUDE.md`

2. **Incorrect directory structure**
   - Templates were in `src/` directory
   - Should be in `templates/` directory (matching global template structure)

## Expected vs Actual Structure

### What Was Created (TASK-011G)

```
.claude/templates/maui-mydrive/
├── agents/
├── docs/
│   └── README.md          # Only README in docs/
├── manifest.json
├── src/                   # ❌ Should be templates/
│   ├── BaseEngine.cs
│   ├── FeatureEngine.cs
│   └── ...
└── tests/
```

### What Was Expected

```
.claude/templates/maui-mydrive/
├── agents/
├── CLAUDE.md              # ✅ Required at root
├── docs/
│   └── README.md
├── manifest.json
├── templates/             # ✅ Not src/
│   ├── BaseEngine.cs
│   ├── FeatureEngine.cs
│   └── ...
└── tests/
```

### Global Template Reference

```bash
$ ls -la ~/.agentecflow/templates/maui-appshell/
drwxr-xr-x   agents/
-rw-r--r--   CLAUDE.md      # ✅ At root
-rw-r--r--   manifest.json
-rw-r--r--   README.md
drwxr-xr-x   templates/     # ✅ Named templates/
```

## Solution

### Fix 1: Created CLAUDE.md at Root

Created `/Users/richardwoollcott/Projects/appmilla_github/DeCUK.Mobile.MyDrive/.claude/templates/maui-mydrive/CLAUDE.md` with:

- Template overview and purpose
- Architecture documentation (Engine pattern)
- Available templates listing
- Usage examples
- Quality standards
- Specialized agents description
- Links to detailed documentation
- Validation instructions
- Version history

**Key Content**:
```markdown
# MAUI-MyDrive Template - Engine Pattern

This is a **local template** for the DeCUK.Mobile.MyDrive project that preserves
the Engine pattern and DeCUK namespace conventions.

## Template Information
- **Scope**: Local (MyDrive project only)
- **Stack**: maui-mydrive
- **Base Template**: maui-appshell (global)
- **Namespace**: DeCUK.Mobile.MyDrive.*
- **Pattern**: Engine suffix (e.g., AuthenticationEngine, RouteEngine)
...
```

### Fix 2: Renamed src/ to templates/

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/DeCUK.Mobile.MyDrive/.claude/templates/maui-mydrive
mv src templates
```

This matches the global template directory structure.

## Template Validation Rules

The `agentecflow doctor` command validates local templates with these checks:

### Required Files/Directories (Critical)

| Item | Location | Purpose |
|------|----------|---------|
| `CLAUDE.md` | Root | Template instructions for Claude Code |
| `manifest.json` | Root | Template metadata and configuration |
| `agents/` | Root | Template-specific AI agents |
| `templates/` | Root | Source code templates |

### Optional (Warnings Only)

| Item | Location | Purpose |
|------|----------|---------|
| `README.md` | Root | User documentation |
| `docs/` | Root | Additional documentation |
| `tests/` | Root | Test templates |

### Validation Logic (from agentecflow CLI)

```bash
# Check for required files
if [ ! -f "$template_dir/CLAUDE.md" ]; then
    status="missing CLAUDE.md"  # ✗ FAIL
elif [ ! -d "$template_dir/agents" ]; then
    status="missing agents/"     # ✗ FAIL
elif [ ! -d "$template_dir/templates" ]; then
    status="missing templates/"  # ✗ FAIL
else
    status="valid"               # ✓ PASS
fi
```

## Testing

### Before Fix

```bash
$ cd /Users/richardwoollcott/Projects/appmilla_github/DeCUK.Mobile.MyDrive
$ agentecflow doctor

Local Templates:
  ✓ 1 local templates available
  ✗ maui-mydrive (missing CLAUDE.md)

# After creating CLAUDE.md:
  ✗ maui-mydrive (missing templates/)
```

### After Fix

```bash
$ cd /Users/richardwoollcott/Projects/appmilla_github/DeCUK.Mobile.MyDrive
$ agentecflow doctor

Local Templates:
  ✓ Project context found: /Users/richardwoollcott/Projects/appmilla_github/DeCUK.Mobile.MyDrive
  ✓ 1 local templates available

  Available local templates:
    ✓ maui-mydrive (valid)

  Template resolution order:
    1. Local (.claude/templates/) [HIGHEST PRIORITY]
    2. Global (~/.agentecflow/templates/)
    3. Default (CLAUDE_HOME/templates/) [LOWEST PRIORITY]
```

✅ **SUCCESS** - Template is now valid!

## Final Template Structure

```
DeCUK.Mobile.MyDrive/.claude/templates/maui-mydrive/
├── agents/                              # MyDrive-specific AI agents
│   ├── engine-pattern-specialist.md
│   ├── mydrive-architect.md
│   └── maui-mydrive-generator.md
├── CLAUDE.md                            # ✅ Template instructions (NEW)
├── docs/                                # Detailed documentation
│   ├── README.md
│   ├── engine-patterns.md
│   ├── namespace-conventions.md
│   └── migration-guide.md
├── manifest.json                        # Template metadata
├── templates/                           # ✅ Source templates (RENAMED from src/)
│   ├── BaseEngine.cs
│   ├── FeatureEngine.cs
│   ├── IFeatureEngine.cs
│   └── FeatureViewModelEngine.cs
└── tests/                               # Test templates
    ├── FeatureEngineTests.cs
    ├── FeatureViewModelEngineTests.cs
    └── validate-mydrive-template.sh
```

## Files Modified

1. **Created**: `/Users/richardwoollcott/Projects/appmilla_github/DeCUK.Mobile.MyDrive/.claude/templates/maui-mydrive/CLAUDE.md`
   - 7,147 bytes
   - Comprehensive template documentation

2. **Renamed**: `src/` → `templates/`
   - Matches global template structure
   - Contains all source code templates

## Impact

### Before Fix
- ❌ Template shown as invalid
- ❌ Unclear if template would be used
- ❌ No template instructions for Claude Code
- ❌ Failed validation checks

### After Fix
- ✅ Template validates successfully
- ✅ Clear "valid" status in doctor output
- ✅ CLAUDE.md provides template instructions
- ✅ Matches global template structure
- ✅ Ready for use in MyDrive project

## Prevention

### For TASK-011G Template Creation

When creating local templates from global templates in the future:

1. **Copy the complete structure** including:
   - `CLAUDE.md` at root (required)
   - `agents/` directory (required)
   - `templates/` directory NOT `src/` (required)
   - `manifest.json` at root (required)

2. **Validate structure** matches global templates:
   ```bash
   # Compare with global template
   ls -la ~/.agentecflow/templates/maui-appshell/
   ls -la .claude/templates/your-template/
   ```

3. **Test immediately**:
   ```bash
   agentecflow doctor
   # Should show: ✓ template-name (valid)
   ```

### Template Creation Checklist

When creating a new local template:

- [ ] Create root-level `CLAUDE.md` with template instructions
- [ ] Create `manifest.json` with template metadata
- [ ] Create `agents/` directory with at least one agent
- [ ] Create `templates/` directory (NOT `src/`) with code templates
- [ ] Run `agentecflow doctor` to verify validation
- [ ] Check output shows `✓ template-name (valid)`

## Recommendations

1. **Update TASK-011G Documentation**
   - Add requirement for CLAUDE.md at root
   - Specify `templates/` directory (not `src/`)
   - Include validation step in acceptance criteria

2. **Update Template Generator**
   - If there's a template generator script, update it to create CLAUDE.md
   - Ensure it uses `templates/` directory name

3. **Add to Setup Guide**
   - Include validation step in setup guide
   - Document expected structure
   - Provide troubleshooting for validation failures

## Success Criteria

✅ CLAUDE.md exists at template root
✅ templates/ directory contains source templates
✅ `agentecflow doctor` shows template as "valid"
✅ Template ready for use in MyDrive project
✅ Structure matches global template pattern

## Related Documentation

- **Setup Guide**: [docs/guides/maui-mydrive-setup-guide.md](../guides/maui-mydrive-setup-guide.md)
- **TASK-011G**: [tasks/completed/TASK-011G-maui-mydrive-local-template.md](../../tasks/completed/TASK-011G-maui-mydrive-local-template.md)
- **Template Architecture**: [docs/shared/maui-template-architecture.md](../shared/maui-template-architecture.md)

---

**Status**: ✅ Fixed (2025-10-18)
**Verified**: MyDrive template now validates successfully
**Ready**: Template ready for use in development
