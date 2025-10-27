# Zeplin to MAUI - UX Design Integration Command

Convert Zeplin designs to pixel-perfect .NET MAUI XAML components with platform-specific testing.

**Common Patterns**: This command follows shared design-to-code patterns documented in [Design-to-Code Common Patterns](../../docs/shared/design-to-code-common.md). This document covers Zeplin and MAUI-specific implementation details.

## Quick Start

```bash
# Convert Zeplin design to MAUI XAML component (2 minutes)
/zeplin-to-maui https://app.zeplin.io/project/abc123/screen/def456

# XAML component generated in Views/ with platform validation tests
```

**Learn More**: See "Core Concepts" below for common use cases and complete reference.

---

## Usage

```bash
/zeplin-to-maui <zeplin-url-or-ids> [options]
```

## Examples

### Basic Usage (Zeplin URL)
```bash
# Full Zeplin URL with project and screen
/zeplin-to-maui https://app.zeplin.io/project/abc123/screen/def456

# Zeplin URL with project and component
/zeplin-to-maui https://app.zeplin.io/project/abc123/component/ghi789

# Project only
/zeplin-to-maui https://app.zeplin.io/project/abc123
```

### Using IDs Only
```bash
# Requires ZEPLIN_PROJECT_ID configured in .env
/zeplin-to-maui --screen-id def456

# Specify project and screen IDs
/zeplin-to-maui --project-id abc123 --screen-id def456

# Component ID
/zeplin-to-maui --project-id abc123 --component-id ghi789
```

### With Options
```bash
# Specify component name
/zeplin-to-maui https://app.zeplin.io/project/abc123/screen/def456 --name LoginForm

# Skip platform tests
/zeplin-to-maui <url> --skip-platform-tests

# Use custom output directory
/zeplin-to-maui <url> --output Views/Auth

# Verbose mode for debugging
/zeplin-to-maui <url> --verbose
```

## Prerequisites

### Required MCP Servers

1. **Zeplin MCP Server**
   ```bash
   npm install -g @zeplin/mcp-server
   ```

### Environment Configuration

Create or update `.env` file:
```bash
# Zeplin Configuration
ZEPLIN_ACCESS_TOKEN=zplnt_your_access_token_here
ZEPLIN_PROJECT_ID=abc123  # Optional: default project ID
```

### Get Zeplin Access Token
1. Go to https://app.zeplin.io/profile/developer
2. Click "Generate new token"
3. Copy token and add to `.env` as `ZEPLIN_ACCESS_TOKEN`
4. Token must have `read` scope

### Verify Setup
```bash
# Check MCP servers are available
/mcp-zeplin verify

# Test Zeplin connection
/mcp-zeplin test-connection
```

## Workflow Overview

This command executes a 6-phase Saga pattern workflow:

```
Phase 0: MCP Verification
   ├─ Verify Zeplin MCP tools available
   ├─ Verify Zeplin access token
   └─ Validate project/screen/component IDs

Phase 1: Design Extraction
   ├─ Extract IDs from URL
   ├─ Extract project metadata via zeplin:get_project
   ├─ Extract screen/component via zeplin:get_screen or zeplin:get_component
   ├─ Extract styleguide via zeplin:get_styleguide
   ├─ Extract colors via zeplin:get_colors
   └─ Extract text styles via zeplin:get_text_styles

Phase 2: Boundary Documentation
   ├─ Identify elements in design
   ├─ Generate prohibition checklist
   └─ Document design constraints

Phase 3: Component Generation
   ├─ Generate MAUI XAML ContentView
   ├─ Generate C# code-behind
   ├─ Generate ViewModel (if needed)
   ├─ Apply exact styling from Zeplin
   ├─ Platform-specific adaptations
   └─ Validate against constraints

Phase 4: Platform Testing
   ├─ Generate xUnit tests
   ├─ Validate XAML structure
   ├─ Verify platform adaptations (iOS, Android, Windows, macOS)
   └─ XAML correctness validation (100% threshold)

Phase 5: Constraint Validation
   ├─ Pattern matching validation
   ├─ AST analysis (if violations detected)
   └─ Generate violation report
```

## ID Extraction from URL

**CRITICAL**: Zeplin URLs contain project, screen, and component IDs.

### Automatic Extraction
The command automatically extracts IDs from URLs:

| Input Format | Extracted IDs | Status |
|--------------|---------------|--------|
| `https://app.zeplin.io/project/abc123` | `projectId: abc123` | ✅ Auto |
| `https://app.zeplin.io/project/abc123/screen/def456` | `projectId: abc123, screenId: def456` | ✅ Auto |
| `https://app.zeplin.io/project/abc123/component/ghi789` | `projectId: abc123, componentId: ghi789` | ✅ Auto |
| `invalid` | Error | ❌ Invalid |

### Examples
```bash
# All of these work:
/zeplin-to-maui https://app.zeplin.io/project/abc123
/zeplin-to-maui https://app.zeplin.io/project/abc123/screen/def456
/zeplin-to-maui https://app.zeplin.io/project/abc123/component/ghi789

# Or use IDs directly:
/zeplin-to-maui --project-id abc123 --screen-id def456
```

## Output Files

### Generated Component (XAML)
```
Views/ZeplinComponent.xaml
```

**Structure**:
```xml
<?xml version="1.0" encoding="utf-8" ?>
<ContentView xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             x:Class="MyApp.Views.ZeplinComponent">

    <!--
    ZeplinComponent

    Generated from Zeplin design
    Project ID: abc123
    Screen ID: def456
    Extracted: 2025-10-09T12:00:00Z

    Design Boundary:
    Documented: [elements in design]
    Prohibited: [features not in design]
    -->

    <Frame BackgroundColor="#FFFFFF"
           CornerRadius="12"
           Padding="24">
        <!-- Component XAML -->
    </Frame>
</ContentView>
```

### Code-Behind
```
Views/ZeplinComponent.xaml.cs
```

**Structure**:
```csharp
using Microsoft.Maui.Controls;

namespace MyApp.Views
{
    public partial class ZeplinComponent : ContentView
    {
        public ZeplinComponent()
        {
            InitializeComponent();
            // Minimal logic - ONLY for visible interactions
        }
    }
}
```

### ViewModel (if needed)
```
ViewModels/ZeplinComponentViewModel.cs
```

**Structure**:
```csharp
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

namespace MyApp.ViewModels
{
    public partial class ZeplinComponentViewModel : ObservableObject
    {
        // ONLY properties for visible design elements

        [RelayCommand]
        private void Submit()
        {
            // Minimal logic
        }
    }
}
```

### Unit Tests
```
Tests/Unit/ZeplinComponentTests.cs
```

**Structure**:
```csharp
using Xunit;
using FluentAssertions;

namespace MyApp.Tests.Unit
{
    public class ZeplinComponentTests
    {
        [Fact]
        public void Component_ShouldInitialize_WithoutErrors()
        {
            // Test implementation
        }

        [Fact]
        public void XamlStructure_ShouldMatch_DesignSpecification()
        {
            // Test implementation
        }

        [Theory]
        [InlineData("iOS")]
        [InlineData("Android")]
        [InlineData("Windows")]
        [InlineData("macOS")]
        public void Component_ShouldAdaptTo_Platform(string platform)
        {
            // Test implementation
        }
    }
}
```

## Icon Handling

The command automatically converts icon codes from Zeplin format to XAML-compatible format.

### Icon Conversion

**Automatic Conversion**: Icon codes are automatically converted during Phase 1 (Design Extraction).

**Input Format** (from Zeplin):
```
&#xe5d2; (lowercase HTML entity)
```

**Output Format** (XAML):
```xml
<FontImageSource FontFamily="{StaticResource IconsFontFamily}"
                 Glyph="&#xE5D2;"
                 Color="White"
                 Size="34" />
```

**Key Change**: Hex digits converted to uppercase (e5d2 → E5D2) for XAML compatibility.

### Icon Conversion Report

After extraction, a conversion summary is displayed:

```
Icon Conversion Summary:
  ✅ Successful: 7 icons converted
     - &#xe5d2; → &#xE5D2; (Menu icon)
     - &#xe8b1; → &#xE8B1; (Lightbulb icon)
     - &#xe241; → &#xE241; (Label icon)
     - &#xe86c; → &#xE86C; (Check icon)
     - &#xe000; → &#xE000; (Error icon)
     - &#xe5cc; → &#xE5CC; (Chevron icon)
     - &#xef4b; → &#xEF4B; (Barcode icon)

  ⚠️  Warnings: 0
  ❌ Failed: 0
```

### Icon Validation

Icons are validated against Material Design Icons range (U+E000 to U+F8FF):

- **Valid**: Icon codes within range are accepted
- **Warning**: Icons outside range generate warnings but don't block workflow
- **Error**: Malformed icon codes are logged but don't stop generation

### Troubleshooting Icons

If icons don't render correctly, see:
- [Icon Rendering Issues Guide](../../docs/troubleshooting/zeplin-maui-icon-issues.md)
- [Icon Code Conversion Pattern](../../docs/patterns/icon-code-conversion-pattern.md)

## Success Report

### All Phases Pass
```
✅ ZEPLIN → MAUI WORKFLOW COMPLETE

📋 Workflow Summary
Duration: 95 seconds
Project ID: abc123
Screen ID: def456
Component: LoginForm
Platform: Multi-platform (iOS, Android, Windows, macOS)

🔍 Phase Results
✅ Phase 0: MCP Verification (2s)
✅ Phase 1: Design Extraction (15s)
  ├─ Icon Conversion: 7 successful, 0 failed, 0 warnings
✅ Phase 2: Boundary Documentation (6s)
✅ Phase 3: Component Generation (32s)
✅ Phase 4: Platform Testing (35s)
✅ Phase 5: Constraint Validation (5s)

📊 Quality Metrics
XAML Correctness: 100% (threshold: 100%)
Constraint Violations: 0 (zero tolerance)
Bindable Properties: 4 (all from design)
ViewModel Properties: 2 (minimal)
Icons Converted: 7 (all successful)
Lines of XAML: 185
Lines of C#: 68
Platform Adaptations: iOS ✅, Android ✅, Windows ✅, macOS ✅

📁 Generated Files
✅ Views/LoginForm.xaml (185 lines)
✅ Views/LoginForm.xaml.cs (42 lines)
✅ ViewModels/LoginFormViewModel.cs (68 lines)
✅ Tests/Unit/LoginFormTests.cs (95 lines)

🎯 Design Adherence
Documented Elements: 12 (email entry, password entry, submit button, 7 icons)
Implemented Elements: 12
Prohibited Features: 10
Violations: 0

Next Steps:
1. Review component: Views/LoginForm.xaml
2. Verify icons render correctly
3. Run unit tests: dotnet test
4. Test on platforms: iOS, Android, Windows, macOS
5. Integrate into application
```

## Failure Reports

### MCP Verification Failure (Phase 0)
```
❌ ZEPLIN → MAUI WORKFLOW FAILED

Phase Failed: Phase 0 - MCP Verification

📋 Error Details
Missing MCP Tools:
- zeplin (required)

🔧 Setup Instructions:

1. Install Zeplin MCP Server:
   npm install -g @zeplin/mcp-server

2. Configure Zeplin access token in .env:
   ZEPLIN_ACCESS_TOKEN=zplnt_your_token

3. Verify setup:
   /mcp-zeplin verify

Documentation: docs/mcp-setup/zeplin-mcp-setup.md
```

### Design Extraction Failure (Phase 1)
```
❌ ZEPLIN → MAUI WORKFLOW FAILED

Phase Failed: Phase 1 - Design Extraction

📋 Error Details
MCP Call Failed: zeplin:get_screen
Error: Invalid screen ID

Input: "invalid-format"
Expected: Valid Zeplin screen ID

🔧 Remediation Steps:

Examples of valid formats:
✅ https://app.zeplin.io/project/abc123/screen/def456
✅ --project-id abc123 --screen-id def456

How to find IDs:
1. Open design in Zeplin
2. Copy URL from browser
3. Use full URL with command
```

### Constraint Violation (Phase 5)
```
❌ ZEPLIN → MAUI WORKFLOW FAILED

Phase Failed: Phase 5 - Constraint Validation

📋 Constraint Violations Detected
Zero scope creep tolerance exceeded.

Violations (3):
1. Loading state detected (prohibited - not in design)
   Location: Line 52, Views/LoginForm.xaml.cs
   Code: public bool IsBusy { get; set; }

2. API integration detected (ALWAYS prohibited)
   Location: Line 85, Views/LoginForm.xaml.cs
   Code: await _httpClient.GetAsync(...)

3. Extra bindable property (prohibited - not in design)
   Location: Line 18, Views/LoginForm.xaml
   Code: BindableProperty.Create("OnError", ...)

🔧 Remediation Steps:

1. Remove IsBusy property
   Why: Loading state not visible in Zeplin design

2. Remove API integration
   Why: API calls never implemented from design alone

3. Remove OnError bindable property
   Why: Error handling not shown in design

📚 Design Boundary Reference:
Documented Elements:
- Submit button
- Email entry field
- Password entry field

Prohibited (not in design):
- Loading states
- Error states
- API integrations
- Additional validation
- Extra properties

Action: Fix violations automatically or manually edit component
```

## Command Options

### Required Arguments
- `<zeplin-url-or-ids>`: Zeplin URL with project/screen/component, or use flags

### Optional Flags

#### `--project-id <id>`
Specify project ID directly
```bash
/zeplin-to-maui --project-id abc123 --screen-id def456
```

#### `--screen-id <id>`
Specify screen ID directly
```bash
/zeplin-to-maui --project-id abc123 --screen-id def456
```

#### `--component-id <id>`
Specify component ID directly
```bash
/zeplin-to-maui --project-id abc123 --component-id ghi789
```

#### `--name <ComponentName>`
Specify custom component name (default: auto-generated from Zeplin)
```bash
/zeplin-to-maui <url> --name LoginForm
```

#### `--output <directory>`
Specify output directory for component (default: `Views`)
```bash
/zeplin-to-maui <url> --output Views/Auth
```

#### `--skip-platform-tests`
Skip Phase 4 (Platform Testing)
```bash
/zeplin-to-maui <url> --skip-platform-tests
```

#### `--skip-viewmodel`
Don't generate ViewModel
```bash
/zeplin-to-maui <url> --skip-viewmodel
```

#### `--force-refresh`
Force re-extraction even if cached
```bash
/zeplin-to-maui <url> --force-refresh
```

#### `--verbose`
Show detailed debug output
```bash
/zeplin-to-maui <url> --verbose
```

#### `--dry-run`
Show what would be generated without writing files
```bash
/zeplin-to-maui <url> --dry-run
```

## Design Constraints (Zero Scope Creep)

### What Gets Implemented
✅ Elements **visible** in Zeplin design
✅ Styling **exactly** as shown in design
✅ Bindable properties for **visible** interactive elements
✅ Properties for **visible** interactions
✅ Text content **exactly** as shown

### What Does NOT Get Implemented
❌ Loading states (unless shown in design)
❌ Error states (unless shown in design)
❌ Additional form validation (unless shown)
❌ Complex state management (unless required)
❌ API integrations (NEVER from design)
❌ Navigation (unless in design)
❌ Additional buttons/controls (unless in design)
❌ Sample data beyond design
❌ Responsive breakpoints (unless shown)
❌ Animations (unless specified)
❌ "Best practice" additions
❌ Extra bindable properties for "flexibility"

### Prohibition Checklist
Every generated component is validated against a 12-category prohibition checklist:

1. Loading states: ❌
2. Error states: ❌
3. Additional form validation: ❌
4. Complex state management: ❌
5. API integrations: ❌ (ALWAYS)
6. Navigation beyond design: ❌
7. Additional buttons: ❌
8. Sample data beyond design: ❌ (ALWAYS)
9. Responsive breakpoints: ❌
10. Animations not specified: ❌
11. "Best practice" additions: ❌ (ALWAYS)
12. Extra bindable properties: ❌ (ALWAYS)

**Zero tolerance**: If ANY violations detected, component generation is rejected.

## Quality Metrics

### XAML Correctness
- **Target**: 100% correctness
- **Measurement**: XAML structure and property validation
- **Tolerance**: Zero deviation from design

### Performance
- **Phase 0 (MCP Verification)**: <5 seconds
- **Phase 1 (Design Extraction)**: <20 seconds
- **Phase 2 (Boundary Documentation)**: <10 seconds
- **Phase 3 (Component Generation)**: <35 seconds
- **Phase 4 (Platform Testing)**: <30 seconds
- **Phase 5 (Constraint Validation)**: <10 seconds
- **Total End-to-End**: <2 minutes

### Code Quality
- **XAML**: 100% structure correctness
- **C#**: Type-safe with proper patterns
- **MVVM**: CommunityToolkit.Mvvm compliance
- **Constraint Adherence**: Zero violations

## Troubleshooting

### "Invalid project/screen/component ID"
**Problem**: ID not recognized

**Solution**:
```bash
# Find IDs in Zeplin:
1. Open design in Zeplin
2. Copy URL from browser
3. Extract IDs from URL pattern:
   https://app.zeplin.io/project/{PROJECT_ID}/screen/{SCREEN_ID}

# Use full URL:
/zeplin-to-maui https://app.zeplin.io/project/abc123/screen/def456
```

### "Zeplin authentication failed"
**Problem**: Invalid or missing Zeplin access token

**Solution**:
```bash
1. Generate token: https://app.zeplin.io/profile/developer
2. Add to .env: ZEPLIN_ACCESS_TOKEN=zplnt_your_token
3. Verify: /mcp-zeplin verify
```

### "XAML correctness below threshold"
**Problem**: Generated XAML doesn't match design specification

**Solution**:
```bash
1. Review generated XAML: Views/{Component}.xaml
2. Check properties match Zeplin design specs
3. Verify colors are exact hex values
4. Verify spacing matches design
5. Re-extract if needed: /zeplin-to-maui <url> --force-refresh
```

### "MCP tools not available"
**Problem**: Zeplin MCP server not installed

**Solution**:
```bash
# Install Zeplin MCP
npm install -g @zeplin/mcp-server

# Verify
/mcp-zeplin verify
```

### "Constraint violations detected"
**Problem**: Generated component includes prohibited features

**Solution**:
```bash
# Review violation report
# Common issues:
- Loading states: Remove unless shown in design
- Error handling: Remove unless shown in design
- API calls: ALWAYS remove (never from design)
- Extra properties: Remove properties not in design

# The orchestrator will automatically reject
# Fix and re-run workflow
```

## Integration with Task Workflow

### Automatic Zeplin Detection
When a task description contains a Zeplin URL, the system automatically detects and offers to run this command:

```markdown
# In task description:
Implement login form from Zeplin design:
https://app.zeplin.io/project/abc123/screen/def456

# System detects and suggests:
🔍 Zeplin design detected in task description
Run: /zeplin-to-maui https://app.zeplin.io/project/abc123/screen/def456
```

### Quality Gate Integration
Platform tests are included in task quality gates:
- ✅ XAML correctness: 100%
- ✅ Constraint violations: 0
- ✅ Platform coverage: iOS, Android, Windows, macOS
- ✅ All tests passing: 100%

## Best Practices

### 1. Start with Simple Designs
Begin with simple components (buttons, entries) before complex layouts

### 2. Verify MCP Setup First
Always run `/mcp-zeplin verify` before starting

### 3. Use Exact URLs
Copy URLs directly from Zeplin to avoid errors

### 4. Review Generated XAML
Always review generated XAML for correctness

### 5. Understand Design Boundaries
Know what's in the design and what's not before generating

### 6. Test on All Platforms
Test generated components on iOS, Android, Windows, and macOS

### 7. Keep Zeplin Organized
Use clear naming in Zeplin for better component names

### 8. Document Deviations
If you must deviate from design, document why

## Related Commands

- `/mcp-zeplin verify` - Verify Zeplin MCP setup
- `/mcp-zeplin test-connection` - Test Zeplin API connection
- `/task-work TASK-XXX` - Integrate with task workflow
- `/task-complete TASK-XXX` - Complete task after review

## Future Enhancements

**Post-MVP** (after Zeplin + MAUI validation):
1. React Native support
2. Flutter integration
3. Design token extraction
4. Component library generation
5. Multi-variant design handling
6. Animation specifications

## Links & Documentation

### Setup Guides
- [Zeplin MCP Setup](../docs/mcp-setup/zeplin-mcp-setup.md)

### Architecture
- [UX Design Subagent Recommendations](../docs/research/ux-design-subagent-recommendations.md)
- [Implementation Plan](../docs/architecture/ux-design-subagents-implementation-plan.md)

### External Documentation
- [Zeplin MCP Server](https://mcp.so/server/mcp-server/zeplin)
- [Zeplin MCP Setup](https://support.zeplin.io/en/articles/11559086-zeplin-mcp-server)

---

**Command Philosophy**: "Design fidelity is not negotiable. Implement exactly what's in the design, nothing more, nothing less."
