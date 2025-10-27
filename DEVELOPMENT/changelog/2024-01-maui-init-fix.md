# Fix: MAUI Initialization Error

## Issue
When running `agentec-init maui`, the script failed with:
```
/Users/richardwoollcott/.claude/scripts/claude-init: line 389: .claude/stacks/maui.json: No such file or directory
```

## Root Cause
The `create_stack_files()` function was trying to write stack configuration files to `.claude/stacks/` directory, but that directory wasn't being created.

## Fix Applied
1. **Added `stacks` to initial directory creation** in `create_smart_structure()`:
   ```bash
   mkdir -p .claude/{agents,commands,hooks,templates,stacks}
   ```

2. **Added safety check** in `create_stack_files()`:
   ```bash
   # Create stacks directory if it doesn't exist
   mkdir -p .claude/stacks
   ```

## Files Modified
- `/installer/scripts/init-claude-project.sh`
  - Line 106: Added `stacks` to mkdir command
  - Line 362: Added `mkdir -p .claude/stacks` before writing stack files

## Testing
To test the fix:
1. Reinstall the global installer
2. Create a new test directory
3. Run `agentec-init maui`
4. Verify `.claude/stacks/maui.json` is created successfully

## Prevention
- Always ensure parent directories exist before writing files
- Use `mkdir -p` for safety when creating nested structures
- Consider adding error checking for file write operations
