# Documentation Validation Quick Reference

## Running Validation

```bash
# Feature 3.9 validation
python3 tests/documentation/validate_feature_3_9.py

# Exit code 0 = PASS (compilation success)
# Exit code 1 = FAIL (compilation failure)
```

## Understanding Results

### Compilation Status

```
✅ COMPILATION PASSED
  - Markdown syntax valid
  - All cross-references resolve
  - Tables properly formatted
  - Code blocks correctly tagged

❌ COMPILATION FAILED
  - Fix errors before task can be completed
```

### Severity Levels

| Symbol | Level | Action |
|--------|-------|--------|
| ✅ | PASS | No action required |
| ⚠ | WARNING | Should fix, doesn't block compilation |
| ❌ | ERROR | Must fix, blocks compilation |

## Validation Categories

### 1. Markdown Syntax (5 checks)
- Headers (# ## ###)
- Code blocks (``` balanced)
- Code block language tags (bash, json, regex)
- Tables (pipe formatting)
- Lists (ordered and unordered)

### 2. Cross-References (5 checks)
- UX Design Integration Workflow
- Figma-to-React Command
- Zeplin-to-MAUI Command
- Design-to-Code Common Patterns
- Internal Feature 3.8 reference

### 3. Content Completeness (10+ checks)
- 3-tier structure (Quick Start, Core Concepts, Complete Reference)
- Code examples (minimum 4, target 6+)
- Tables (URL Pattern, Supported Systems, Parameters, Troubleshooting)
- Content elements (Algorithm, Process, Gates, Examples, etc.)

### 4. Consistency (6 checks)
- Hubbard Alignment metadata
- Phase metadata
- Complexity tier
- Dependencies
- Usage guidance (When to use/skip)
- Professional tone (no decorative emojis)

## Common Issues

### Cross-Reference Not Found
```
❌ Cross-Reference Links
  ✗ Design-to-Code Common Patterns: ../shared/design-to-code-common.md (NOT FOUND)
```
**Fix**: Check file path is correct and file exists

### Missing Required Section
```
❌ 3-Tier Structure
  ✗ Complete Reference (30 minutes) (MISSING)
```
**Fix**: Add missing section with proper heading

### Unbalanced Code Blocks
```
❌ Code Block Balance
  Unbalanced code blocks detected (odd number of ```)
```
**Fix**: Ensure every ``` has a closing ```

### Missing Metadata
```
❌ Hubbard Alignment Field
  Hubbard Alignment metadata missing
```
**Fix**: Add required metadata field to feature header

## Quick Fixes

### Add Language Tags to Code Blocks

**Before**:
```markdown
```
command example
```
```

**After**:
```markdown
```bash
command example
```
```

### Fix Cross-Reference Path

**Before**:
```markdown
[Design Patterns](../shared/wrong-path.md)
```

**After**:
```markdown
[Design Patterns](../shared/design-to-code-common.md)
```

### Add Missing Metadata

**Before**:
```markdown
### Feature 3.9: Design System Detection
```

**After**:
```markdown
### Feature 3.9: Design System Detection

**Hubbard Alignment**: N/A (Specialized extension)
**Phase**: 2.8 (Implementation Planning)
**Complexity**: Tier 3 (Advanced)
**Dependencies**: Feature 3.8
```

## Integration with Task Workflow

### In `/task-work`

**Phase 4.5: Test Enforcement**
```
For documentation tasks:
1. Detect task is documentation (file type .md)
2. Run validation suite (validate_feature_3_9.py)
3. Check compilation status
4. Report results
5. Block completion if errors found
```

### Manual Validation

```bash
# Before completing documentation task
python3 tests/documentation/validate_feature_3_9.py

# If errors found, fix and re-run
# If only warnings, optionally fix
# If all pass, task complete
```

## Expected Output (Success)

```
================================================================================
VALIDATION REPORT
================================================================================

Total Checks: 16
  ✓ Passed: 15
  ⚠ Warnings: 1
  ✗ Errors: 0

================================================================================
COMPILATION STATUS (Documentation)
================================================================================
✅ COMPILATION PASSED

Documentation is:
  1. Markdown syntax valid ✓
  2. All cross-references resolve ✓
  3. Tables properly formatted ✓
  4. Code blocks correctly tagged ✓
```

## Help & Support

**Documentation**: See `tests/documentation/README.md`
**Full Results**: See `tests/documentation/TASK-030B-1.9-VALIDATION-SUMMARY.md`
**Code**: See `tests/documentation/validate_feature_3_9.py`

---

**Quick Reference Version**: 1.0
**Last Updated**: 2025-10-19
