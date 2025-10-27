# UX Design Integration Workflow

**Purpose**: Complete guide to converting Figma and Zeplin designs into pixel-perfect, constraint-compliant components with zero scope creep.

**Learn UX design integration in**:
- **2 minutes**: Quick Start
- **10 minutes**: Core Concepts
- **30 minutes**: Complete Reference

---

## Quick Start (2 minutes)

### Get Started Immediately

**Figma → React**:
```bash
# Convert Figma design to TypeScript React component
/figma-to-react https://figma.com/design/abc123?node-id=2-2

# Component generated in src/components/ with:
# ✅ Pixel-perfect styling (Tailwind CSS)
# ✅ Visual regression tests (>95% similarity)
# ✅ Zero scope creep (prohibition checklist enforced)
```

**Zeplin → MAUI**:
```bash
# Convert Zeplin design to .NET MAUI XAML component
/zeplin-to-maui https://app.zeplin.io/project/abc123/screen/def456

# XAML component generated in Views/ with:
# ✅ Exact styling from Zeplin
# ✅ Platform-specific validation (iOS, Android, Windows, macOS)
# ✅ Zero scope creep (prohibition checklist enforced)
```

**That's it!** Components are production-ready with automated tests.

**Learn More**: See "Core Concepts" below for the 6-phase workflow and prohibition checklist.

---

## Core Concepts (10 minutes)

### Supported Design Systems

#### Figma → React
- **Target**: TypeScript React components with Tailwind CSS
- **Testing**: Playwright visual regression (>95% similarity)
- **MCP**: `@figma/mcp-server`
- **Prerequisites**: See [figma-to-react.md](../../installer/global/commands/figma-to-react.md#prerequisites)

#### Zeplin → .NET MAUI
- **Target**: XAML ContentView components with C# code-behind
- **Testing**: Platform-specific validation (iOS, Android, Windows, macOS)
- **MCP**: `@zeplin/mcp-server`
- **Prerequisites**: See [zeplin-to-maui.md](../../installer/global/commands/zeplin-to-maui.md#prerequisites)

### 6-Phase Saga Workflow

All design-to-code commands follow this orchestration pattern:

```
Phase 0: MCP Verification
├─ Verify design system MCP server available
├─ Validate authentication tokens
└─ Test tool connectivity

Phase 1: Design Extraction
├─ Parse design URL/ID
├─ Extract design elements via MCP tools
├─ Apply retry pattern (exponential backoff)
└─ Validate extraction completeness

Phase 2: Boundary Documentation
├─ Document ALL visible elements
├─ Define design boundaries
├─ Generate prohibition checklist (12 categories)
└─ Create design metadata

Phase 3: Component Generation
├─ Delegate to stack-specific generator
├─ Apply styling from design tokens
├─ Implement ONLY visible elements
└─ Generate with proper types

Phase 4: Visual Regression Testing
├─ Generate automated tests
├─ Compare component to design
├─ Calculate similarity score
└─ Generate diff images on failure

Phase 5: Constraint Validation
├─ Pattern matching (Tier 1)
├─ AST analysis (Tier 2)
├─ Display violations if any
└─ Block generation if constraints violated
```

### Prohibition Checklist (Zero Scope Creep)

The system enforces a **12-category prohibition checklist** to ensure ONLY what's in the design gets implemented.

See [design-to-code-common.md](../shared/design-to-code-common.md#prohibition-checklist-12-categories) for complete checklist.

**Summary** (implement ONLY if visible in design):
1. **State Management** - No loading/error/empty states
2. **Form Behavior** - No extra validation
3. **Data & API** - No API integrations
4. **Navigation** - No routing logic
5. **Interactions** - No extra handlers
6. **Animations** - No transitions
7. **Responsive Behavior** - No extra breakpoints
8. **Accessibility** - Basic only
9. **Component API** - No extra props
10. **Error Handling** - No try-catch blocks
11. **Performance Optimization** - No premature optimization
12. **"Best Practices"** - No additions justified as "best practice"

**Enforcement**: Two-tier validation (Pattern Matching + AST Analysis) with zero tolerance.

### Quality Gates

See [common-thresholds.md](../shared/common-thresholds.md#ux-design-integration) for threshold details.

**All design-to-code workflows enforce**:
- **Visual Fidelity**: >95% similarity to design
- **Constraint Violations**: 0 (zero tolerance)
- **Compilation**: 100% success before testing
- **Component Props**: Only for visible design elements

### Common Use Cases

#### Use Case 1: Convert Figma Button to React

```bash
/figma-to-react https://figma.com/design/abc?node-id=2-2 --name PrimaryButton

# Generated Files:
src/components/PrimaryButton.tsx    # TypeScript React component
src/components/PrimaryButton.test.tsx  # Playwright visual test

# Component contains:
✅ Exact colors from Figma (#3B82F6)
✅ Exact dimensions (120px × 40px)
✅ Exact border radius (8px)
✅ Exact font (Inter, 14px, 600 weight)
❌ No hover effects (not in design)
❌ No loading state (not in design)
❌ No onClick handler (not in design)
```

#### Use Case 2: Convert Zeplin Form to MAUI

```bash
/zeplin-to-maui https://app.zeplin.io/project/abc/screen/def --name LoginForm

# Generated Files:
Views/LoginForm.xaml              # XAML ContentView
Views/LoginForm.xaml.cs           # C# code-behind
Tests/LoginFormTests.cs           # xUnit validation tests

# Component contains:
✅ Exact Zeplin colors (#FF6B6B)
✅ Exact spacing (Padding="24,16,24,16")
✅ Exact fonts (System fonts from Zeplin)
✅ Platform adaptations (if specified in Zeplin)
❌ No form validation (not in design)
❌ No submit logic (not in design)
```

#### Use Case 3: Constraint Violation Example

```bash
/figma-to-react https://figma.com/design/abc?node-id=2-2

# Phase 5: Constraint Validation
❌ Constraint Violations Detected (2)

VIOLATION 1: Prohibited State Management
File: src/components/Button.tsx
Line: 12
Code: const [isLoading, setIsLoading] = useState(false);

Reason: Design does not show loading state
Category: State Management (Category 1)
Fix: Remove loading state, implement only visible button

VIOLATION 2: Extra Component Props
File: src/components/Button.tsx
Line: 5
Code: interface ButtonProps { onClick?: () => void; disabled?: boolean; loading?: boolean; }

Reason: Design shows only text and styling props
Category: Component API (Category 9)
Fix: Remove onClick, disabled, loading props (not in design)

❌ Generation BLOCKED until violations fixed
```

**Learn More**: See "Complete Reference" below for phase-by-phase details and error handling.

---

## Complete Reference (30+ minutes)

### Phase-by-Phase Deep Dive

#### Phase 0: MCP Verification

**Purpose**: Ensure MCP tools are available before attempting design extraction

**Checks**:
1. MCP server installed and running
2. Authentication token valid
3. All required MCP tools respond
4. Connection latency <2 seconds

**Figma MCP Tools**:
- `figma-dev-mode:get_code` - Extract design code
- `figma-dev-mode:get_image` - Extract design images
- `figma-dev-mode:get_variable_defs` - Extract design tokens

**Zeplin MCP Tools**:
- `zeplin:get_project` - Get project metadata
- `zeplin:get_screen` - Get screen details
- `zeplin:get_styleguide` - Get style tokens
- `zeplin:get_colors` - Get color palette
- `zeplin:get_text_styles` - Get typography

**Failure Action**: Display setup guide, abort workflow

**Example Error**:
```
❌ MCP Verification Failed

Figma MCP server not responding.

Please complete setup:
1. Install: npm install -g @figma/mcp-server
2. Configure token: export FIGMA_ACCESS_TOKEN=xxx
3. Test connection: /mcp-figma verify

See: docs/mcp-setup/figma-mcp-setup.md
```

#### Phase 1: Design Extraction

**Purpose**: Successfully extract design elements from design system

**Figma Extraction**:
```bash
# Node ID conversion (URL format → API format)
Input:  https://figma.com/design/abc?node-id=2-2
Parsed: fileKey="abc", nodeId="2-2"
Convert: nodeId="2:2" (API format)

# MCP Tool Invocations
1. figma-dev-mode:get_code(fileKey="abc", nodeId="2:2")
   → Returns: Design code and metadata
2. figma-dev-mode:get_image(fileKey="abc", nodeId="2:2")
   → Returns: PNG baseline image
3. figma-dev-mode:get_variable_defs(fileKey="abc")
   → Returns: Design tokens (colors, spacing, typography)
```

**Zeplin Extraction**:
```bash
# ID extraction from URL
Input:  https://app.zeplin.io/project/abc123/screen/def456
Parsed: projectId="abc123", screenId="def456"

# MCP Tool Invocations
1. zeplin:get_project(projectId="abc123")
   → Returns: Project metadata
2. zeplin:get_screen(projectId="abc123", screenId="def456")
   → Returns: Screen design details
3. zeplin:get_styleguide(projectId="abc123")
   → Returns: Style guide
4. zeplin:get_colors(projectId="abc123")
   → Returns: Color palette
5. zeplin:get_text_styles(projectId="abc123")
   → Returns: Typography tokens
```

**Retry Pattern**:
```
Attempt 1: Immediate
Attempt 2: Wait 1 second
Attempt 3: Wait 2 seconds
All failed: Error with diagnostics
```

See [design-to-code-common.md](../shared/design-to-code-common.md#common-error-handling) for retry strategy details.

#### Phase 2: Boundary Documentation

**Purpose**: Document exactly what's in the design to prevent scope creep

**Generated Documentation**:
```markdown
## Design Boundary

### Visible Elements
- Button with text "Sign In"
- Background color: #3B82F6 (blue)
- Text color: #FFFFFF (white)
- Font: Inter, 14px, weight 600
- Border radius: 8px
- Padding: 12px 24px
- Dimensions: 120px × 40px

### Prohibited Features (Not Visible in Design)
❌ Loading states (no spinner shown)
❌ Error states (no error message shown)
❌ Disabled state (not shown in design)
❌ Hover effects (not specified)
❌ Click handlers (behavior not defined)
❌ Form validation (no validation rules shown)
❌ API integration (no data flow shown)
❌ Navigation logic (no routing shown)

### Component Constraints
✅ Implement: Visual button with exact styling
✅ Props: Only `text` prop (for button label)
❌ Do NOT add: State, handlers, logic, extra props
```

**Prohibition Checklist Generation**:

See [design-to-code-common.md](../shared/design-to-code-common.md#prohibition-checklist-12-categories) for complete checklist.

The system generates a design-specific checklist:
- Reviews each of 12 categories
- Identifies what's NOT in the design
- Documents explicit prohibitions
- Used in Phase 5 validation

#### Phase 3: Component Generation

**Purpose**: Generate pixel-perfect, constraint-compliant component code

**Figma → React Generation**:
```typescript
// src/components/PrimaryButton.tsx
import React from 'react';

/**
 * PrimaryButton
 *
 * Generated from Figma design
 * Node ID: 2:2
 * Extracted: 2025-10-12T14:30:00Z
 *
 * Design Boundary:
 * ✅ Implements: Button with exact styling from Figma
 * ❌ Excludes: State management, handlers, extra props
 */

interface PrimaryButtonProps {
  text: string;  // ONLY prop for visible element
}

export const PrimaryButton: React.FC<PrimaryButtonProps> = ({ text }) => {
  return (
    <button
      className="bg-blue-500 text-white font-semibold text-sm rounded-lg px-6 py-3 w-30 h-10"
      data-testid="primary-button"
    >
      {text}
    </button>
  );
};
```

**Key Characteristics**:
- ✅ Exact Tailwind classes matching Figma styles
- ✅ Only props for visible elements (`text`)
- ✅ No state management
- ✅ No event handlers
- ✅ data-testid for testing
- ❌ No extra props (disabled, loading, onClick)

**Zeplin → MAUI Generation**:
```xml
<!-- Views/PrimaryButton.xaml -->
<?xml version="1.0" encoding="utf-8" ?>
<ContentView xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             x:Class="MyApp.Views.PrimaryButton">

    <!--
    PrimaryButton

    Generated from Zeplin design
    Screen ID: def456
    Extracted: 2025-10-12T14:30:00Z

    Design Boundary:
    ✅ Implements: Button with exact styling from Zeplin
    ❌ Excludes: Commands, validation, extra properties
    -->

    <Frame BackgroundColor="#3B82F6"
           CornerRadius="8"
           Padding="12,24"
           WidthRequest="120"
           HeightRequest="40">
        <Label Text="{Binding Text}"
               TextColor="#FFFFFF"
               FontFamily="Inter"
               FontSize="14"
               FontAttributes="Bold"
               HorizontalTextAlignment="Center"
               VerticalTextAlignment="Center" />
    </Frame>
</ContentView>
```

**Key Characteristics**:
- ✅ Exact colors from Zeplin (#3B82F6)
- ✅ Exact dimensions (120×40)
- ✅ Exact fonts (Inter, 14px, Bold)
- ✅ Bindable Text property only
- ❌ No Command property
- ❌ No validation logic

#### Phase 4: Visual Regression Testing

**Purpose**: Verify generated component matches design visually

**Figma → React Testing (Playwright)**:
```typescript
// src/components/PrimaryButton.test.tsx
import { test, expect } from '@playwright/test';
import { PrimaryButton } from './PrimaryButton';

test.describe('PrimaryButton Visual Regression', () => {
  test('matches Figma design with >95% similarity', async ({ page }) => {
    // Render component
    await page.goto('/components/primary-button');

    // Capture baseline from Figma
    const figmaBaseline = await getFigmaImage('2:2');

    // Capture component screenshot
    const componentScreenshot = await page.screenshot();

    // Compare with 95% threshold
    const similarity = await compareImages(
      figmaBaseline,
      componentScreenshot
    );

    expect(similarity).toBeGreaterThan(0.95);
  });

  test('has correct dimensions', async ({ page }) => {
    await page.goto('/components/primary-button');
    const button = page.getByTestId('primary-button');

    await expect(button).toHaveCSS('width', '120px');
    await expect(button).toHaveCSS('height', '40px');
  });

  test('has correct colors', async ({ page }) => {
    await page.goto('/components/primary-button');
    const button = page.getByTestId('primary-button');

    await expect(button).toHaveCSS('background-color', 'rgb(59, 130, 246)');
    await expect(button).toHaveCSS('color', 'rgb(255, 255, 255)');
  });
});
```

**Visual Similarity Threshold**: >95% (see [common-thresholds.md](../shared/common-thresholds.md#visual-regression-thresholds))

**Zeplin → MAUI Testing (xUnit)**:
```csharp
// Tests/PrimaryButtonTests.cs
using Xunit;
using MyApp.Views;

public class PrimaryButtonTests
{
    [Fact]
    public void PrimaryButton_XamlStructure_IsValid()
    {
        // Validate XAML structure
        var xaml = LoadXaml("Views/PrimaryButton.xaml");

        Assert.NotNull(xaml);
        Assert.Equal("ContentView", xaml.RootElement);
    }

    [Fact]
    public void PrimaryButton_Properties_MatchZeplinDesign()
    {
        var button = new PrimaryButton();

        // Verify exact Zeplin values
        Assert.Equal("#3B82F6", button.Frame.BackgroundColor);
        Assert.Equal(8, button.Frame.CornerRadius);
        Assert.Equal(new Thickness(12, 24), button.Frame.Padding);
        Assert.Equal(120, button.Frame.WidthRequest);
        Assert.Equal(40, button.Frame.HeightRequest);
    }

    [Theory]
    [InlineData("iOS")]
    [InlineData("Android")]
    [InlineData("Windows")]
    [InlineData("MacOS")]
    public void PrimaryButton_RendersCorrectly_OnAllPlatforms(string platform)
    {
        // Platform-specific rendering validation
        var button = new PrimaryButton();
        var renderer = GetRenderer(platform);

        var view = renderer.Render(button);

        Assert.NotNull(view);
        Assert.True(renderer.ValidateLayout(view));
    }
}
```

**XAML Correctness Threshold**: 100% (see [common-thresholds.md](../shared/common-thresholds.md#visual-regression-thresholds))

#### Phase 5: Constraint Validation

**Purpose**: Ensure zero scope creep - only implement what's in the design

**Two-Tier Validation**:

**Tier 1: Pattern Matching**
```typescript
const PROHIBITED_PATTERNS = [
  /loading\s*=\s*true/i,
  /isLoading/i,
  /error\s*=\s*true/i,
  /showError/i,
  /onSubmit.*async/i,
  /fetch\(/i,
  /axios\./i,
  /useEffect.*fetch/i,
  /@keyframes/i,
  /transition:/i,
  /animation:/i,
  /useState.*loading/i,
  /useState.*error/i
];

function validateNoProhibitedPatterns(code: string): ValidationResult {
  const violations = [];
  for (const pattern of PROHIBITED_PATTERNS) {
    if (pattern.test(code)) {
      violations.push({
        pattern: pattern.source,
        category: categorize(pattern),
        severity: 'ERROR'
      });
    }
  }
  return { passed: violations.length === 0, violations };
}
```

**Tier 2: AST Analysis**
```typescript
function validateComponentStructure(ast: AST): ValidationResult {
  const violations = [];

  // Check props match design elements only
  const actualProps = extractProps(ast);
  const designProps = extractDesignElements();
  const extraProps = actualProps.filter(p => !designProps.includes(p));

  if (extraProps.length > 0) {
    violations.push({
      type: 'EXTRA_PROPS',
      props: extraProps,
      message: 'Component has props not in design specification'
    });
  }

  // Check for state management
  const hasState = astContainsStateHooks(ast);
  if (hasState && !designSpecifiesState()) {
    violations.push({
      type: 'PROHIBITED_STATE',
      message: 'Component uses state management not in design'
    });
  }

  return { passed: violations.length === 0, violations };
}
```

**Failure Action**: Block component creation, display violations with remediation

### Error Handling

See [design-to-code-common.md](../shared/design-to-code-common.md#common-error-handling) for complete error handling guide.

**Category 1: Configuration Errors**
- Missing MCP server
- Invalid access token
- Missing environment variables

**Category 2: Design Access Errors**
- Invalid design URL/ID
- Design not found
- Permission denied

**Category 3: Extraction Failures**
- MCP tool timeout
- Partial extraction
- Missing design elements

**Category 4: Generation Failures**
- Code compilation errors
- Style conversion failures
- Platform-specific issues

**Category 5: Constraint Violations**
- Prohibited features detected
- Extra props/state added
- Scope creep detected

### Integration with Task Workflow

When task descriptions contain design URLs, the system automatically detects and suggests:

```bash
/task-work TASK-042

# Task description contains:
# "Implement login form from Figma design: https://figma.com/design/abc?node-id=2-2"

# System detects and suggests:
🎨 Figma Design Detected

Design URL: https://figma.com/design/abc?node-id=2-2

RECOMMENDATION: Use design-to-code workflow

Suggested command:
  /figma-to-react https://figma.com/design/abc?node-id=2-2 --name LoginForm

This will:
✅ Generate pixel-perfect component with visual tests
✅ Enforce zero scope creep (prohibition checklist)
✅ Validate >95% visual similarity to design

[Y] Run design-to-code workflow
[N] Continue with standard implementation

Your choice: _
```

**Visual regression tests integrated in task quality gates**:
```
Task TASK-042: Quality Gates

✅ Code compiles (100%)
✅ Tests passing (100%)
✅ Line coverage (85% ≥ 80%)
✅ Branch coverage (78% ≥ 75%)
✅ Visual fidelity (97% > 95%)  ← Design integration gate
✅ Constraint violations (0)    ← Design integration gate
```

---

## Examples (Real-World Scenarios)

### Example 1: Figma Button → React (Success)

**Command**:
```bash
/figma-to-react https://figma.com/design/abc?node-id=2-2 --name PrimaryButton
```

**Phase Execution**:
```
Phase 0: MCP Verification
✅ Figma MCP available
✅ Token valid
✅ Playwright MCP available

Phase 1: Design Extraction
✅ Node ID converted: 2-2 → 2:2
✅ Code extracted
✅ Image extracted (baseline.png)
✅ Variables extracted

Phase 2: Boundary Documentation
✅ Elements documented: Button, Text, Background
✅ Prohibition checklist generated (12 categories)
✅ Constraints defined

Phase 3: Component Generation
✅ React component generated (src/components/PrimaryButton.tsx)
✅ Tailwind classes applied
✅ TypeScript types added

Phase 4: Visual Regression Testing
✅ Playwright test generated
✅ Baseline captured
✅ Component rendered
✅ Similarity: 98.2% (>95% threshold) ✅

Phase 5: Constraint Validation
✅ Pattern matching: No violations
✅ AST analysis: No extra props
✅ Constraint validation: PASSED

✅ Generation Complete

Files Created:
- src/components/PrimaryButton.tsx (42 lines)
- src/components/PrimaryButton.test.tsx (28 lines)

Quality Metrics:
- Visual fidelity: 98.2%
- Constraint violations: 0
- Props: 1 (text only)
```

### Example 2: Zeplin Form → MAUI (Success)

**Command**:
```bash
/zeplin-to-maui https://app.zeplin.io/project/abc/screen/def --name LoginForm
```

**Phase Execution**:
```
Phase 0: MCP Verification
✅ Zeplin MCP available
✅ Token valid
✅ Project accessible

Phase 1: Design Extraction
✅ IDs extracted: project=abc, screen=def
✅ Screen metadata retrieved
✅ Styleguide extracted
✅ Colors extracted (5 colors)
✅ Text styles extracted (3 styles)

Phase 2: Boundary Documentation
✅ Elements documented: 2 TextFields, 1 Button
✅ Prohibition checklist generated
✅ Platform notes: iOS and Android only

Phase 3: Component Generation
✅ XAML ContentView generated (Views/LoginForm.xaml)
✅ C# code-behind generated (Views/LoginForm.xaml.cs)
✅ Exact Zeplin colors applied
✅ Platform adaptations applied

Phase 4: Platform Testing
✅ xUnit tests generated (Tests/LoginFormTests.cs)
✅ XAML structure validated
✅ Property values verified
✅ iOS rendering validated
✅ Android rendering validated

Phase 5: Constraint Validation
✅ Pattern matching: No violations
✅ AST analysis: No extra bindings
✅ Constraint validation: PASSED

✅ Generation Complete

Files Created:
- Views/LoginForm.xaml (68 lines)
- Views/LoginForm.xaml.cs (24 lines)
- Tests/LoginFormTests.cs (42 lines)

Quality Metrics:
- XAML correctness: 100%
- Constraint violations: 0
- Platform support: iOS, Android
```

### Example 3: Constraint Violation (Failure)

**Command**:
```bash
/figma-to-react https://figma.com/design/abc?node-id=5-5 --name SearchForm
```

**Phase Execution**:
```
Phase 0-4: ✅ All passed

Phase 5: Constraint Validation
❌ VALIDATION FAILED

Constraint Violations Detected (3):

VIOLATION 1: Prohibited State Management
──────────────────────────────────────
File: src/components/SearchForm.tsx
Line: 15
Code: const [searchTerm, setSearchTerm] = useState('');

Category: State Management (Category 1)
Reason: Design does not show search state or behavior
Rationale: Design shows only static search input field

Recommended Fix:
Remove state management. Component should be controlled:
  interface SearchFormProps {
    value: string;
    onChange: (value: string) => void;
  }

VIOLATION 2: Extra Event Handler
──────────────────────────────────────
File: src/components/SearchForm.tsx
Line: 23
Code: const handleSubmit = async (e) => { ... }

Category: Data & API (Category 3)
Reason: Design does not show search submission or results
Rationale: Design shows only input field, no submit button

Recommended Fix:
Remove async handler. If needed, parent component should handle submission.

VIOLATION 3: Extra Component Props
──────────────────────────────────────
File: src/components/SearchForm.tsx
Line: 8
Code: interface SearchFormProps { onSearch: (term: string) => void; loading?: boolean; }

Category: Component API (Category 9)
Reason: Design shows only placeholder text prop
Rationale: No search behavior or loading state visible in design

Recommended Fix:
Remove onSearch and loading props. Keep only:
  interface SearchFormProps {
    placeholder?: string;
  }

❌ GENERATION BLOCKED

Next Steps:
1. Review design to confirm no search behavior shown
2. Remove state management and handlers
3. Simplify props to match visible elements only
4. Re-run: /figma-to-react https://figma.com/design/abc?node-id=5-5 --name SearchForm

Need help? See docs/workflows/ux-design-integration-workflow.md
```

### Example 4: MCP Configuration Error (Failure)

**Command**:
```bash
/figma-to-react https://figma.com/design/abc?node-id=2-2
```

**Error**:
```
Phase 0: MCP Verification
❌ VERIFICATION FAILED

MCP Error: Figma MCP server not responding

Possible Causes:
1. Figma MCP server not installed
2. Figma access token not configured
3. MCP server not running

Recommended Actions:

Step 1: Install Figma MCP Server
  npm install -g @figma/mcp-server

Step 2: Configure Access Token
  1. Go to https://www.figma.com/developers/api#access-tokens
  2. Generate new token with file:read scope
  3. Add to .env file:
     FIGMA_ACCESS_TOKEN=figd_your_token_here

Step 3: Verify Setup
  /mcp-figma verify

Step 4: Test Connection
  /mcp-figma test-connection

Need More Help?
- MCP Setup Guide: docs/mcp-setup/figma-mcp-setup.md
- Common Issues: docs/troubleshooting/mcp-issues.md
- Support: https://github.com/ai-engineer/support

❌ Workflow Aborted (Phase 0 failed)
```

---

## FAQ

### Q: What if I need features not in the design (like onClick handlers)?

**A**: The prohibition checklist enforces that ONLY visible elements are implemented. If you need handlers, state, or behavior:
1. Add these features to the design first (prototype interactions)
2. Re-extract the updated design
3. OR implement the visual component first, then add behavior in parent component

**Example**:
```tsx
// Generated component (no handlers)
export const PrimaryButton = ({ text }) => (
  <button className="...">{text}</button>
);

// Parent component (adds behavior)
export const LoginPage = () => {
  const handleLogin = async () => { /* ... */ };

  return <PrimaryButton text="Sign In" onClick={handleLogin} />;
};
```

### Q: Can I customize the prohibition checklist per project?

**A**: Yes, customize in `.claude/settings.json`:
```json
{
  "design_integration": {
    "prohibition_checklist": {
      "state_management": "strict",
      "component_api": "relaxed",
      "accessibility": "enhanced"
    }
  }
}
```

Levels: `strict` (default), `relaxed` (warnings only), `enhanced` (stricter checks)

### Q: What if visual similarity is between 90-95%?

**A**: The system generates a warning but allows proceeding:
```
⚠️  Visual Similarity Below Optimal Threshold

Actual: 93.2%
Target: >95%

Differences detected in:
- Border radius (8px vs 7px)
- Padding (12px vs 11px)

Options:
[A]ccept - Proceed with current component (93.2%)
[F]ix - Adjust styling to match design exactly
[V]iew - Show diff image

Your choice: _
```

### Q: How do I handle responsive designs with multiple breakpoints?

**A**: If design shows multiple breakpoints (mobile, tablet, desktop):
1. Figma: Extract each frame separately, generate components for each
2. Zeplin: Extract platform variants, system generates platform-specific code
3. System automatically adds responsive classes based on design variants

**Not shown in design** → No responsive behavior generated (prohibition checklist)

### Q: Can I skip visual regression tests for faster iteration?

**A**: Yes, use `--skip-visual-tests` flag:
```bash
/figma-to-react <url> --skip-visual-tests

# Skips Phase 4 (Visual Regression Testing)
# Constraint validation (Phase 5) still runs
```

**Warning**: Visual tests catch pixel-level differences. Skipping may result in imperfect components.

### Q: What if my design system uses custom fonts not on my system?

**A**:
- **Figma**: System uses Tailwind's font fallbacks automatically
- **Zeplin**: System maps Zeplin fonts to MAUI system fonts
- **Custom fonts**: Add font files to project, system detects and applies

See design system documentation for font configuration.

---

## Related Documentation

- [Figma to React Command](../../installer/global/commands/figma-to-react.md) - Figma-specific implementation details
- [Zeplin to MAUI Command](../../installer/global/commands/zeplin-to-maui.md) - Zeplin and MAUI-specific details
- [Design-to-Code Common Patterns](../shared/design-to-code-common.md) - Shared patterns across all design systems
- [Common Thresholds](../shared/common-thresholds.md) - Quality threshold definitions
- [Task Work Command](../../installer/global/commands/task-work.md) - Integration with task workflow

---

**Last Updated**: 2025-10-12
**Version**: 1.0.0
**Maintained By**: AI Engineer Team
