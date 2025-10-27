# Agentecflow CLI Script Fix

## Issue Summary

**Date**: 2025-10-18
**Severity**: High
**Impact**: `agentecflow doctor` command produced multiple script errors

## Problem Description

After installation, the `agentecflow doctor` command displayed errors:

```bash
/Users/richardwoollcott/.agentecflow/bin/agentecflow: line 65: local: can only be used in a function
/Users/richardwoollcott/.agentecflow/bin/agentecflow: line 66: [: -ge: unary operator expected
/Users/richardwoollcott/.agentecflow/bin/agentecflow: line 86: local: can only be used in a function
/Users/richardwoollcott/.agentecflow/bin/agentecflow: line 100: local: can only be used in a function
/Users/richardwoollcott/.agentecflow/bin/agentecflow: line 121: detect_project_context: command not found
```

### Root Causes

1. **`local` outside of functions** (lines 65, 86, 100, and more)
   - The `doctor` command is a case statement, not a function
   - Bash only allows `local` inside functions
   - Variables declared as `local` in case statements cause errors

2. **Missing `detect_project_context` function** (line 121)
   - Function was called but never defined
   - Caused "command not found" error

3. **Unquoted variable expansions**
   - Variables like `$agent_count` used in comparisons without quotes
   - Can cause "unary operator expected" errors when empty

## Solution

### 1. Fixed the Installed CLI Script

Updated `/Users/richardwoollcott/.agentecflow/bin/agentecflow`:

**Added `detect_project_context` function:**
```bash
# Detect project context by traversing upward
detect_project_context() {
    local current_dir="$PWD"
    local max_depth=10
    local depth=0

    while [ "$depth" -lt "$max_depth" ]; do
        if [ -d "$current_dir/.claude" ]; then
            PROJECT_ROOT="$current_dir"
            return 0
        fi
        if [ "$current_dir" = "/" ]; then
            return 1
        fi
        current_dir="$(dirname "$current_dir")"
        depth=$((depth + 1))
    done
    return 1
}
```

**Fixed all `local` declarations in case statement:**
```bash
# BEFORE (BROKEN):
local agent_count=$(ls -1 "$AGENTECFLOW_HOME/agents/"*.md 2>/dev/null | wc -l)
local target=$(readlink "$HOME/.claude/commands")
local name=$(basename "$template_dir")

# AFTER (FIXED):
agent_count=$(ls -1 "$AGENTECFLOW_HOME/agents/"*.md 2>/dev/null | wc -l)
target=$(readlink "$HOME/.claude/commands")
name=$(basename "$template_dir")
```

**Added quotes to variable expansions:**
```bash
# BEFORE:
if [ $agent_count -ge 4 ]; then

# AFTER:
if [ "$agent_count" -ge 4 ]; then
```

### 2. Fixed the Installer Template

Updated `installer/scripts/install.sh` (lines 480-635) to generate correct CLI script:

- Added `detect_project_context` function after `print_help()`
- Removed all `local` keywords from the doctor case statement
- Added quotes to all variable expansions in conditionals

## Files Modified

1. **`~/.agentecflow/bin/agentecflow`** (installed file)
   - Added `detect_project_context()` function
   - Removed 8 instances of `local` from case statement
   - Added quotes to variable comparisons

2. **`installer/scripts/install.sh`** (lines 464-643)
   - Updated CLI template generation
   - Same fixes as above, but in the heredoc template

## Testing

### Before Fix
```bash
$ agentecflow doctor
/Users/richardwoollcott/.agentecflow/bin/agentecflow: line 65: local: can only be used in a function
/Users/richardwoollcott/.agentecflow/bin/agentecflow: line 66: [: -ge: unary operator expected
...multiple errors...
```

### After Fix
```bash
$ agentecflow doctor
Running Agentecflow diagnostics...

Installation:
  ✓ Agentecflow home: /Users/richardwoollcott/.agentecflow
  ✓ Directory agents exists
  ... (all checks pass without errors)

AI Agents:
  ✓ 17 agents installed

PATH Configuration:
  ⚠ Add to PATH: export PATH="$HOME/.agentecflow/bin:$PATH"

Claude Code Integration:
  ✓ Commands symlinked correctly
  ✓ Agents symlinked correctly
  ✓ Compatible with Conductor.build for parallel development

Local Templates:
  ✓ Project context found: /Users/richardwoollcott/Projects/appmilla_github/ai-engineer
  ⚠ No .claude/templates/ directory
```

**Result**: ✅ No script errors, all diagnostics run successfully

## Impact

### Before Fix
- Users couldn't run diagnostics reliably
- Script errors obscured actual health information
- Made debugging installation issues difficult

### After Fix
- Clean diagnostic output
- Accurate health information
- Proper project context detection
- Local template validation works

## Prevention

### Why It Happened

The CLI script was written as a case statement (not a function) but used `local` declarations, which is a bash error.

### Future Prevention

1. **Bash validation in CI/CD**: Add shellcheck or bash -n validation
2. **Testing**: Test CLI commands after installation
3. **Code review**: Check for `local` outside functions
4. **Documentation**: Document bash best practices

## Related Issues

- This fix is related to but separate from the orphaned `fi` issue in `.zshrc`
- Both were installer script issues discovered during MAUI-MyDrive setup
- Both have been fixed in installer version 2.0.0+

## Manual Recovery (For Users Already Affected)

If you already have the broken `agentecflow` script:

### Option 1: Re-run Installer (Recommended)
```bash
cd /path/to/ai-engineer
./installer/scripts/install.sh
```

### Option 2: Manually Fix Installed Script
```bash
# Backup current script
cp ~/.agentecflow/bin/agentecflow ~/.agentecflow/bin/agentecflow.backup

# Edit the file
nano ~/.agentecflow/bin/agentecflow

# Make the following changes:
# 1. Add detect_project_context() function after print_help()
# 2. Remove all 'local' keywords from lines 65, 86, 100, 125, 132, 134, 135
# 3. Add quotes around variables in conditionals: "$agent_count", "$target", etc.

# Save and test
agentecflow doctor
```

## Success Criteria

✅ No script errors when running `agentecflow doctor`
✅ All diagnostics sections display correctly
✅ Project context detection works
✅ Local template validation works
✅ Agent count displays correctly
✅ Symlink checks work properly

## Additional Notes

- The PATH warning is expected if running from Claude Code environment
- Local templates warning is normal for projects without `.claude/templates/`
- Both the installed script AND the installer template were fixed

## Recommendations

1. **For Users**: Run the latest installer to get the fix
2. **For Developers**: Always test generated scripts after installation
3. **For CI/CD**: Add `bash -n` validation for generated scripts
4. **For Testing**: Include CLI command execution in test suite

---

**Status**: ✅ Fixed (2025-10-18)
**Version**: Installer v2.0.0+
**Tested**: macOS (zsh)
**Related Fix**: [installer-shell-cleanup-fix.md](installer-shell-cleanup-fix.md)
