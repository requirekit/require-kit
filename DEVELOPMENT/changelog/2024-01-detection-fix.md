# Fix: Project Type Detection and Output Improvements

## Issues Fixed

### Issue 1: Project Type Detection Failing
The script was detecting MAUI projects as "unknown" because the bash globbing wasn't working correctly.

**Old code**:
```bash
if [ -f "*.csproj" ] || [ -f "*/*.csproj" ]; then
```
This was looking for a literal file named `*.csproj` instead of using pattern matching.

**Fixed code**:
```bash
local csproj_files=$(ls *.csproj 2>/dev/null || ls */*.csproj 2>/dev/null || echo "")
if [ -n "$csproj_files" ]; then
```

### Issue 2: Incorrect Output for .NET Projects
The output was showing `src/` and `tests/` directories for .NET projects, which don't use that structure.

**Improvements**:
1. Detection now properly identifies .NET projects
2. Output shows `.sln` and `.csproj` files for .NET projects
3. Technology-specific setup instructions appear even when detection fails (uses template)
4. Only shows directories that actually exist

## Changes Made

### 1. Fixed `detect_project_type()` function
- Uses proper file globbing with `ls` command
- Correctly detects .csproj and .sln files
- Properly searches for Microsoft.Maui references

### 2. Improved `print_tech_specific_steps()` function
- Falls back to template name when detection fails
- Shows appropriate instructions based on template

### 3. Enhanced `print_next_steps()` function
- Shows .NET solution structure for .NET projects
- Only displays directories that exist
- Smarter about what to show based on project type

## Result

Now when running `agentec-init maui`:
- Properly detects MAUI projects (if .csproj exists)
- Doesn't create unnecessary `src/` or `tests/` directories for .NET
- Shows appropriate .NET-specific structure in output
- Provides correct MAUI setup instructions

## Testing
```bash
# In a MAUI project directory
agentec-init maui

# Should see:
# ✓ Detected project type: maui (if .csproj exists)
# - No src/ or tests/ directories created
# - Shows *.sln and *.csproj in structure
# - Displays MAUI-specific setup instructions
```
