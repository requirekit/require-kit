---
id: TASK-015
title: Fix Zeplin-to-MAUI Icon Rendering Issue
status: in_review
created: 2025-10-15T00:00:00Z
updated: 2025-10-16T15:25:00Z
completed_at: 2025-10-16T15:25:00Z
previous_state: in_progress
state_transition_reason: "All quality gates passed - tests passing, coverage exceeds thresholds"
priority: high
tags: [zeplin, maui, icon-rendering, bug-fix, xaml]
requirements: []
bdd_scenarios: []
related_tasks: [TASK-004]
business_need: "Fix icon rendering in Zeplin-to-MAUI generated XAML - icons currently display as Chinese characters instead of Material Design icons"
test_results:
  status: passed
  tests_total: 53
  tests_passed: 53
  tests_failed: 0
  coverage_line: 98.4
  coverage_branch: 94.82
  coverage_function: 100
  performance_single_icon_ms: 0.5
  performance_batch_100_ms: 10
  last_run: 2025-10-16T15:23:00Z
review:
  mode: quick_optional
  action: timeout
  reviewed_at: 2025-10-16T15:21:00Z
  auto_approved: true
  complexity_score: 4
  architectural_score: 88
  duration_seconds: 10
  phase_2_6_checkpoint: skipped
  code_review_score: 92
  code_review_status: approved
---

# Task: Fix Zeplin-to-MAUI Icon Rendering Issue

## Description

The `/zeplin-to-maui` command generates XAML with `FontImageSource` Glyph values that render as Chinese characters instead of the intended Material Design icons. The issue is with the Unicode escape format used in the generated XAML.

### Current Problem

Generated XAML uses HTML entity format which doesn't work correctly in XAML:

```xml
<FontImageSource FontFamily="{StaticResource IconsFontFamily}"
                 Glyph="&#xe5d2;"
                 Color="White"
                 Size="34" />
```

**Result**: Icon displays as Chinese character (e.g., 嘒) instead of the hamburger menu icon.

### Root Cause

XAML requires Unicode escape sequences in a different format than HTML entities:
- ❌ **Current (incorrect)**: `&#xe5d2;` (HTML entity format)
- ✅ **Required**: `&#xE5D2;` (XAML Unicode format with capital hex digits)

## Acceptance Criteria

### 1. Icon Glyph Format Fix
- [ ] Update Zeplin-to-MAUI icon extraction to use correct XAML Unicode format
- [ ] Convert HTML entity format `&#xABCD;` to XAML format `\uE5D2` or direct Unicode character
- [ ] Handle both lowercase and uppercase hex digits in Zeplin icon codes
- [ ] Validate icon codes are valid Material Design icon codes

### 2. FontFamily Verification
- [ ] Verify `IconsFontFamily` static resource exists in generated XAML
- [ ] Ensure Material Design Icons font file is referenced correctly
- [ ] Add fallback mechanism if font family not found
- [ ] Document required font family setup in MAUI project

### 3. Testing
- [ ] Test with multiple Material Design icons from Zeplin designs
- [ ] Verify icons render correctly on iOS
- [ ] Verify icons render correctly on Android
- [ ] Verify icons render correctly on Windows (if applicable)
- [ ] Test edge cases (missing icons, invalid codes)

### 4. Documentation Update
- [ ] Update `/zeplin-to-maui` command documentation with icon handling
- [ ] Add troubleshooting section for icon rendering issues
- [ ] Document Material Design Icons setup requirements
- [ ] Provide examples of correct vs. incorrect icon syntax

## Technical Specifications

### Icon Code Conversion Logic

```csharp
// Zeplin provides icon codes in various formats:
// Format 1: HTML entity: &#xe5d2;
// Format 2: Unicode: \ue5d2
// Format 3: Hex: 0xe5d2

// Convert to XAML-compatible format:
string ConvertIconCode(string zeplinIconCode)
{
    // Remove HTML entity wrapper if present
    if (zeplinIconCode.StartsWith("&#x") && zeplinIconCode.EndsWith(";"))
    {
        string hexCode = zeplinIconCode.Substring(3, zeplinIconCode.Length - 4);
        // Convert to Unicode character
        int codePoint = Convert.ToInt32(hexCode, 16);
        return char.ConvertFromUtf32(codePoint);
    }

    // Handle other formats...
    return zeplinIconCode;
}
```

### Expected XAML Output

**Option 1: Direct Unicode Character** (Recommended)
```xml
<FontImageSource FontFamily="{StaticResource IconsFontFamily}"
                 Glyph="󰍜"
                 Color="White"
                 Size="34" />
```

**Option 2: Unicode Escape in C# Code-Behind**
```csharp
// In C# code-behind
var menuIcon = "\uE5D2"; // Unicode for menu icon
```

**Option 3: XAML Character Entity** (if supported)
```xml
<FontImageSource FontFamily="{StaticResource IconsFontFamily}"
                 Glyph="&#xE5D2;"
                 Color="White"
                 Size="34" />
```

### Material Design Icons Reference

Common Material Design icon codes from the example XAML:
- `&#xe5d2;` → Menu/Hamburger icon (U+E5D2)
- `&#xe8b1;` → Lightbulb/Torch icon (U+E8B1)
- `&#xe241;` → Label icon (U+E241)
- `&#xe86c;` → Done/Check icon (U+E86C)
- `&#xe000;` → Error icon (U+E000)
- `&#xe5cc;` → Chevron right icon (U+E5CC)
- `&#xef4b;` → Barcode scanner icon (U+EF4B)

## Example XAML Analysis

From the provided LoadPage.xaml, all icon instances need correction:

### Menu Icon (Line 30-34)
```xml
<!-- BEFORE (broken) -->
<FontImageSource FontFamily="{StaticResource IconsFontFamily}"
                 Glyph="&#xe5d2;"
                 Color="White"
                 Size="34" />

<!-- AFTER (fixed) -->
<FontImageSource FontFamily="{StaticResource IconsFontFamily}"
                 Glyph="󰍜"
                 Color="White"
                 Size="34" />
```

### Torch Icon (Line 138-141)
```xml
<!-- BEFORE (broken) -->
<FontImageSource FontFamily="{StaticResource IconsFontFamily}"
                 Glyph="&#xe8b1;"
                 Color="White"
                 Size="28" />

<!-- AFTER (fixed) -->
<FontImageSource FontFamily="{StaticResource IconsFontFamily}"
                 Glyph="󰢱"
                 Color="White"
                 Size="28" />
```

## Implementation Strategy

### Phase 1: Locate Icon Generation Code (30 minutes)
1. Find where `zeplin-to-maui` generates `FontImageSource` XAML
2. Identify icon code extraction from Zeplin design data
3. Understand current icon code transformation logic

### Phase 2: Implement Fix (1 hour)
1. Add icon code conversion function
2. Update XAML generation to use converted icon codes
3. Add validation for Material Design icon codes
4. Add error handling for invalid icon codes

### Phase 3: Testing (1 hour)
1. Test with all icons from LoadPage.xaml example
2. Verify rendering on iOS simulator
3. Verify rendering on Android emulator
4. Create test suite for icon conversion logic

### Phase 4: Documentation (30 minutes)
1. Update `/zeplin-to-maui` command docs
2. Add troubleshooting guide
3. Document Material Design Icons setup
4. Provide migration guide for existing generated code

## Files to Modify

1. **Icon Generation Logic**
   - `installer/global/agents/zeplin-maui-orchestrator.md` - Icon extraction
   - `.claude/stacks/maui/agents/maui-ux-specialist.md` - XAML generation

2. **Command Documentation**
   - `installer/global/commands/zeplin-to-maui.md` - Usage examples
   - `installer/global/commands/mcp-zeplin.md` - Icon extraction reference

3. **Tests**
   - `tests/unit/zeplin-maui-icon-conversion.test.ts` - Icon conversion tests
   - `tests/integration/zeplin-to-maui-icons.test.ts` - End-to-end icon tests

## Success Metrics

### Functional Requirements
- ✅ All Material Design icons render correctly (not as Chinese characters)
- ✅ Icon conversion handles all Zeplin icon code formats
- ✅ Icons display identically across iOS, Android platforms
- ✅ Clear error messages for invalid/missing icon codes

### Quality Requirements
- ✅ 100% of icon test cases pass
- ✅ No regression in existing Zeplin-to-MAUI functionality
- ✅ Documentation clearly explains icon setup requirements
- ✅ Code passes architectural review (SOLID/DRY/YAGNI)

### Performance Requirements
- ✅ Icon conversion adds <10ms to generation time
- ✅ No impact on overall workflow performance (<2 minutes end-to-end)

## Risks & Mitigations

### Risk 1: Platform-Specific Rendering Differences
**Impact**: Medium
**Mitigation**: Test on all target platforms, document platform-specific quirks, provide platform overrides if needed

### Risk 2: Material Design Icons Font Not Installed
**Impact**: High (icons won't render at all)
**Mitigation**: Add verification step in command, clear setup instructions, automated font installation check

### Risk 3: Breaking Existing Generated Code
**Impact**: Low
**Mitigation**: Add migration guide, backward compatibility for old format, version detection

### Risk 4: Zeplin Icon Code Format Variations
**Impact**: Medium
**Mitigation**: Support multiple input formats, comprehensive parsing logic, clear error messages

## Dependencies

**Depends On**:
- TASK-004 (Zeplin-to-MAUI implementation - completed)
- Material Design Icons font package for .NET MAUI

**Blocks**:
- MyDrive app UI implementation (icons currently broken)

## Related Documentation

### Internal References
- [TASK-004: Zeplin-to-MAUI Integration](../in_review/TASK-004-zeplin-maui-ux-design-integration.md)
- [Zeplin-to-MAUI Command](../../installer/global/commands/zeplin-to-maui.md)
- [Zeplin MCP Setup Guide](../../docs/mcp-setup/zeplin-mcp-setup.md)

### External References
- [Material Design Icons Codepoints](https://github.com/google/material-design-icons/blob/master/font/MaterialIcons-Regular.codepoints)
- [.NET MAUI Fonts Documentation](https://learn.microsoft.com/en-us/dotnet/maui/user-interface/fonts)
- [XAML Unicode Character Support](https://learn.microsoft.com/en-us/dotnet/desktop/xaml-services/escape-sequence-markup-extension)

## Implementation Notes

### Current Behavior Analysis

The example XAML shows consistent use of `&#xABCD;` format for all icons. This suggests:
1. Zeplin provides icon codes in this format, OR
2. The code generation template uses this format by default

**Need to verify**: Where does `&#xABCD;` format come from?
- [ ] Check Zeplin API response format for icon data
- [ ] Check maui-ux-specialist template for icon Glyph generation
- [ ] Review zeplin-maui-orchestrator icon extraction logic

### Material Design Icons Font Setup

**Required in MAUI Project**:
```xml
<!-- MauiProgram.cs -->
.ConfigureFonts(fonts =>
{
    fonts.AddFont("MaterialIcons-Regular.ttf", "MaterialIcons");
});

<!-- App.xaml -->
<Application.Resources>
    <ResourceDictionary>
        <FontFamily x:Key="IconsFontFamily">MaterialIcons</FontFamily>
    </ResourceDictionary>
</Application.Resources>
```

**Font File Location**: `Resources/Fonts/MaterialIcons-Regular.ttf`

### Test Cases to Cover

1. **Single Icon Conversion**
   - Input: `&#xe5d2;`
   - Expected: Valid Unicode character or `\uE5D2`

2. **Multiple Icons in Same XAML**
   - Verify all icons convert correctly
   - No interference between conversions

3. **Invalid Icon Codes**
   - Input: `&#xZZZZ;`
   - Expected: Clear error message

4. **Missing Icon Codes**
   - Input: Empty or null
   - Expected: Graceful fallback or error

5. **Platform Rendering**
   - iOS: Icon displays correctly
   - Android: Icon displays correctly
   - Windows: Icon displays correctly (if applicable)

---

**Estimated Effort**: 3 hours
**Priority**: High (blocks MyDrive app development)
**Complexity**: 4/10 (Focused fix, clear root cause, localized change)

---

## Next Steps After Task Creation

1. Review TASK-004 implementation to locate icon generation code
2. Test current behavior with sample Zeplin design
3. Implement icon code conversion fix
4. Validate with LoadPage.xaml example
5. Update documentation and tests
