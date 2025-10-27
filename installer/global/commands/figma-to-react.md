# Figma to React - UX Design Integration Command

Convert Figma designs to pixel-perfect TypeScript React components with visual regression testing.

**Common Patterns**: This command follows shared design-to-code patterns documented in [Design-to-Code Common Patterns](../../docs/shared/design-to-code-common.md). This document covers Figma-specific implementation details.

## Quick Start

```bash
# Convert Figma design to React component (2 minutes)
/figma-to-react https://figma.com/design/abc123?node-id=2-2

# Component generated in src/components/ with visual regression tests
```

**Learn More**: See "Core Concepts" below for common use cases and complete reference.

---

## Usage

```bash
/figma-to-react <figma-url-or-node-id> [options]
```

## Examples

### Basic Usage (Figma URL)
```bash
# Full Figma URL with node-id
/figma-to-react https://figma.com/design/abc123?node-id=2-2

# Figma URL with complex node ID
/figma-to-react https://figma.com/design/abc123?node-id=123-456
```

### Using Node ID Only
```bash
# Requires FIGMA_FILE_KEY configured in .env
/figma-to-react 2:2

/figma-to-react 123:456

# Hyphen format (will be auto-converted)
/figma-to-react 2-2
```

### With Options
```bash
# Specify component name
/figma-to-react 2:2 --name LoginForm

# Skip visual regression tests
/figma-to-react 2:2 --skip-visual-tests

# Use custom output directory
/figma-to-react 2:2 --output src/components/auth

# Verbose mode for debugging
/figma-to-react 2:2 --verbose
```

## Prerequisites

### Required MCP Servers

1. **Figma Dev Mode MCP Server**
   ```bash
   npm install -g @figma/mcp-server
   ```

2. **Playwright MCP Server** (for visual regression testing)
   ```bash
   npm install -g @playwright/mcp-server
   ```

### Environment Configuration

Create or update `.env` file:
```bash
# Figma Configuration
FIGMA_ACCESS_TOKEN=figd_your_access_token_here
FIGMA_FILE_KEY=abc123def456  # Optional: default file key

# Playwright Configuration (optional)
PLAYWRIGHT_ENABLED=true
```

### Get Figma Access Token
1. Go to https://www.figma.com/developers/api#access-tokens
2. Click "Generate new token"
3. Copy token and add to `.env` as `FIGMA_ACCESS_TOKEN`
4. Token must have `file:read` scope

### Verify Setup
```bash
# Check MCP servers are available
/mcp-figma verify

# Test Figma connection
/mcp-figma test-connection
```

## Workflow Overview

This command executes a 6-phase Saga pattern workflow:

```
Phase 0: MCP Verification
   ├─ Verify Figma MCP tools available
   ├─ Verify Playwright MCP tools available
   └─ Validate Figma access token

Phase 1: Design Extraction
   ├─ Convert node ID format (URL → API)
   ├─ Extract code via figma-dev-mode:get_code
   ├─ Extract image via figma-dev-mode:get_image
   └─ Extract variables via figma-dev-mode:get_variable_defs

Phase 2: Boundary Documentation
   ├─ Identify elements in design
   ├─ Generate prohibition checklist
   └─ Document design constraints

Phase 3: Component Generation
   ├─ Generate TypeScript React component
   ├─ Apply Tailwind CSS styling
   ├─ Add data-testid attributes
   └─ Validate against constraints

Phase 4: Visual Regression Testing
   ├─ Generate Playwright test
   ├─ Capture baseline from Figma
   ├─ Render React component
   └─ Compare screenshots (95% threshold)

Phase 5: Constraint Validation
   ├─ Pattern matching validation
   ├─ AST analysis (if violations detected)
   └─ Generate violation report
```

## Node ID Format Conversion

**CRITICAL**: Figma URLs use hyphen format, MCP API requires colon format.

### Automatic Conversion
The command automatically converts between formats:

| Input Format | Converted To | Status |
|--------------|--------------|--------|
| `https://figma.com/...?node-id=2-2` | `2:2` | ✅ Auto |
| `2-2` | `2:2` | ✅ Auto |
| `2:2` | `2:2` | ✅ Pass-through |
| `123-456` | `123:456` | ✅ Auto |
| `invalid` | Error | ❌ Invalid |

### Examples
```bash
# All of these work:
/figma-to-react https://figma.com/design/abc?node-id=2-2
/figma-to-react 2-2
/figma-to-react 2:2

# All convert to: nodeId: "2:2" for MCP API
```

## Output Files

### Generated Component
```
src/components/FigmaComponent.tsx
```

**Structure**:
```typescript
import React from 'react';

/**
 * FigmaComponent
 *
 * Generated from Figma design
 * Node ID: 123:456
 * Extracted: 2024-10-09T12:00:00Z
 *
 * Design Boundary:
 * Documented: [elements in design]
 * Prohibited: [features not in design]
 */

interface FigmaComponentProps {
  // ONLY props for visible design elements
}

export const FigmaComponent: React.FC<FigmaComponentProps> = ({
  // ...props
}) => {
  // Minimal state - ONLY for visible interactions

  return (
    <div data-testid="figma-component-container">
      {/* Component JSX */}
    </div>
  );
};
```

### Visual Regression Test
```
tests/FigmaComponent.visual.spec.ts
```

**Structure**:
```typescript
import { test, expect } from '@playwright/test';

test.describe('FigmaComponent - Visual Regression', () => {
  test('matches Figma design exactly', async ({ page }) => {
    await page.goto('/demo/figma-component');

    await expect(page.locator('[data-testid="figma-component-container"]'))
      .toHaveScreenshot('figma-component.png', {
        threshold: 0.05,  // 95% similarity
      });
  });
});
```

### Demo Page
```
src/demos/FigmaComponentDemo.tsx
```

**Structure**:
```typescript
import React from 'react';
import { FigmaComponent } from '../components/FigmaComponent';

export const FigmaComponentDemo: React.FC = () => {
  return (
    <div style={{ padding: '20px' }}>
      <h1>FigmaComponent Demo</h1>
      <FigmaComponent />
    </div>
  );
};
```

### Visual Baselines
```
tests/visual-baselines/
├── figma-component.png          # Figma design baseline
├── react-component.png          # React component screenshot
└── component-diff.png           # Diff (if similarity < 95%)
```

## Success Report

### All Phases Pass
```
✅ FIGMA → REACT WORKFLOW COMPLETE

📋 Workflow Summary
Duration: 87 seconds
Node ID: 123:456
File Key: abc123def456
Component: LoginForm

🔍 Phase Results
✅ Phase 0: MCP Verification (2s)
✅ Phase 1: Design Extraction (12s)
✅ Phase 2: Boundary Documentation (5s)
✅ Phase 3: Component Generation (28s)
✅ Phase 4: Visual Regression Testing (35s)
✅ Phase 5: Constraint Validation (5s)

📊 Quality Metrics
Visual Fidelity: 97.3% (threshold: 95%)
Constraint Violations: 0 (zero tolerance)
Component Props: 4 (all from design)
State Variables: 2 (minimal)
Lines of Code: 183
Tailwind Classes: 24

📁 Generated Files
✅ src/components/LoginForm.tsx (183 lines)
✅ tests/LoginForm.visual.spec.ts (42 lines)
✅ src/demos/LoginFormDemo.tsx (28 lines)
✅ tests/visual-baselines/login-form.png

🎯 Design Adherence
Documented Elements: 12 (email input, password input, submit button, ...)
Implemented Elements: 12
Prohibited Features: 10
Violations: 0

Next Steps:
1. Review component: src/components/LoginForm.tsx
2. Run visual tests: npm run test:visual
3. View demo: npm run dev (navigate to /demo/login-form)
4. Integrate into application
```

## Failure Reports

### MCP Verification Failure (Phase 0)
```
❌ FIGMA → REACT WORKFLOW FAILED

Phase Failed: Phase 0 - MCP Verification

📋 Error Details
Missing MCP Tools:
- figma-dev-mode (required)
- playwright (required for visual testing)

🔧 Setup Instructions:

1. Install Figma MCP Server:
   npm install -g @figma/mcp-server

2. Install Playwright MCP Server:
   npm install -g @playwright/mcp-server

3. Configure Figma access token in .env:
   FIGMA_ACCESS_TOKEN=figd_your_token_here

4. Verify setup:
   /mcp-figma verify

Documentation: docs/mcp-setup/figma-mcp-setup.md
```

### Design Extraction Failure (Phase 1)
```
❌ FIGMA → REACT WORKFLOW FAILED

Phase Failed: Phase 1 - Design Extraction

📋 Error Details
MCP Call Failed: figma-dev-mode:get_code
Error: Invalid node ID format

Input: "invalid-format"
Expected: "2:2" or "2-2" or URL with node-id parameter

🔧 Remediation Steps:

Examples of valid formats:
✅ /figma-to-react 123:456
✅ /figma-to-react 123-456
✅ /figma-to-react https://figma.com/design/abc?node-id=123-456

How to find node ID:
1. Open design in Figma
2. Select element
3. Copy link from context menu
4. Extract node-id parameter from URL
```

### Constraint Violation (Phase 5)
```
❌ FIGMA → REACT WORKFLOW FAILED

Phase Failed: Phase 5 - Constraint Validation

📋 Constraint Violations Detected
Zero scope creep tolerance exceeded.

Violations (3):
1. Loading state detected (prohibited - not in design)
   Location: Line 45, src/components/LoginForm.tsx
   Code: const [isLoading, setIsLoading] = useState(false);

2. API integration detected (ALWAYS prohibited)
   Location: Line 78, src/components/LoginForm.tsx
   Code: fetch('/api/login', { ... })

3. Extra prop detected (prohibited - not in design)
   Location: Line 12, src/components/LoginForm.tsx
   Code: onError?: (error: Error) => void

🔧 Remediation Steps:

1. Remove isLoading state
   Why: Loading state not visible in Figma design

2. Remove API integration
   Why: API calls never implemented from design alone

3. Remove onError prop
   Why: Error handling not shown in design

📚 Design Boundary Reference:
Documented Elements:
- Submit button
- Email input field
- Password input field

Prohibited (not in design):
- Loading states
- Error states
- API integrations
- Additional validation
- Extra props

Action: Fix violations automatically or manually edit component
```

### Visual Regression Failure (Phase 4)
```
❌ FIGMA → REACT WORKFLOW FAILED

Phase Failed: Phase 4 - Visual Regression Testing

📋 Visual Fidelity Below Threshold

Required: 95% similarity
Actual: 89.2%
Pixel Difference: 1,234 pixels (EXCEEDS tolerance)

Diff Image: tests/visual-diffs/login-form-diff.png

🔍 Possible Causes:

1. Tailwind CSS classes not matching design
   Check: background colors, text colors
   Verify: spacing (padding, margin, gap)
   Validate: border radius, border width

2. Typography differences
   Font size mismatch: Check text-[Npx] classes
   Font weight mismatch: Check font-[N] classes
   Line height differences

3. Layout issues
   Flexbox alignment incorrect
   Element positioning off
   Dimensions not matching design

4. Missing design tokens
   Colors not extracted correctly
   Spacing values incorrect

🔧 Remediation Steps:

1. Review diff image:
   open tests/visual-diffs/login-form-diff.png

2. Compare Tailwind classes with Figma design specs:
   - Colors: Use arbitrary values bg-[#HEX]
   - Spacing: Use arbitrary values p-[Npx]
   - Fonts: Match sizes exactly text-[Npx]

3. Re-extract design if needed:
   /figma-to-react {nodeId} --force-refresh

4. Re-run visual test:
   npm run test:visual
```

## Command Options

### Required Arguments
- `<figma-url-or-node-id>`: Figma URL with node-id parameter, or direct node ID

### Optional Flags

#### `--name <ComponentName>`
Specify custom component name (default: auto-generated from Figma node name)
```bash
/figma-to-react 2:2 --name LoginForm
```

#### `--output <directory>`
Specify output directory for component (default: `src/components`)
```bash
/figma-to-react 2:2 --output src/features/auth/components
```

#### `--skip-visual-tests`
Skip Phase 4 (Visual Regression Testing)
```bash
/figma-to-react 2:2 --skip-visual-tests
```

#### `--skip-demo`
Don't generate demo page
```bash
/figma-to-react 2:2 --skip-demo
```

#### `--force-refresh`
Force re-extraction even if cached
```bash
/figma-to-react 2:2 --force-refresh
```

#### `--threshold <number>`
Custom visual similarity threshold (default: 0.05 = 95%)
```bash
/figma-to-react 2:2 --threshold 0.10  # 90% similarity
```

#### `--verbose`
Show detailed debug output
```bash
/figma-to-react 2:2 --verbose
```

#### `--dry-run`
Show what would be generated without writing files
```bash
/figma-to-react 2:2 --dry-run
```

## Design Constraints (Zero Scope Creep)

### What Gets Implemented
✅ Elements **visible** in Figma design
✅ Styling **exactly** as shown in design
✅ Props for **visible** interactive elements
✅ State for **visible** interactions
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
❌ Extra props for "flexibility"

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
12. Extra props for flexibility: ❌ (ALWAYS)

**Zero tolerance**: If ANY violations detected, component generation is rejected.

## Quality Metrics

### Visual Fidelity
- **Target**: >95% similarity to Figma design
- **Measurement**: Pixel-by-pixel screenshot comparison
- **Tolerance**: ±2px for anti-aliasing differences

### Performance
- **Phase 0 (MCP Verification)**: <5 seconds
- **Phase 1 (Design Extraction)**: <15 seconds
- **Phase 2 (Boundary Documentation)**: <10 seconds
- **Phase 3 (Component Generation)**: <30 seconds
- **Phase 4 (Visual Regression Testing)**: <30 seconds
- **Phase 5 (Constraint Validation)**: <10 seconds
- **Total End-to-End**: <2 minutes

### Code Quality
- **TypeScript**: 100% type coverage
- **Tailwind CSS**: Arbitrary values for pixel-perfect matching
- **Data TestIDs**: All interactive elements
- **Constraint Adherence**: Zero violations

## Troubleshooting

### "Invalid node ID format"
**Problem**: Node ID not recognized

**Solution**:
```bash
# Find node ID in Figma:
1. Select element in Figma
2. Right-click → Copy link
3. Extract node-id parameter from URL

# Example URL:
https://figma.com/design/abc123?node-id=2-2

# Use any format:
/figma-to-react 2-2
/figma-to-react 2:2
/figma-to-react https://figma.com/design/abc123?node-id=2-2
```

### "Figma authentication failed"
**Problem**: Invalid or missing Figma access token

**Solution**:
```bash
1. Generate token: https://www.figma.com/developers/api#access-tokens
2. Add to .env: FIGMA_ACCESS_TOKEN=figd_your_token
3. Verify: /mcp-figma verify
```

### "Visual similarity below threshold"
**Problem**: React component doesn't match Figma design

**Solution**:
```bash
1. Review diff image: tests/visual-diffs/{component}-diff.png
2. Check Tailwind classes match design specs
3. Verify colors are exact: bg-[#HEX] not bg-blue-500
4. Verify spacing is exact: p-[16px] not p-4
5. Re-extract if needed: /figma-to-react {nodeId} --force-refresh
```

### "MCP tools not available"
**Problem**: Figma or Playwright MCP servers not installed

**Solution**:
```bash
# Install Figma MCP
npm install -g @figma/mcp-server

# Install Playwright MCP
npm install -g @playwright/mcp-server

# Verify
/mcp-figma verify
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
- Extra props: Remove props not in design

# The orchestrator will automatically reject
# Fix and re-run workflow
```

## Integration with Task Workflow

### Automatic Figma Detection
When a task description contains a Figma URL, the system automatically detects and offers to run this command:

```markdown
# In task description:
Implement login form from Figma design:
https://figma.com/design/abc?node-id=123-456

# System detects and suggests:
🔍 Figma design detected in task description
Run: /figma-to-react https://figma.com/design/abc?node-id=123-456
```

### Quality Gate Integration
Visual regression tests are included in task quality gates:
- ✅ Visual fidelity: >95%
- ✅ Constraint violations: 0
- ✅ All tests passing: 100%

## Best Practices

### 1. Start with Simple Designs
Begin with simple components (buttons, inputs) before complex layouts

### 2. Verify MCP Setup First
Always run `/mcp-figma verify` before starting

### 3. Use Exact Node IDs
Copy node IDs directly from Figma to avoid errors

### 4. Review Diff Images
If visual tests fail, always review the diff image first

### 5. Understand Design Boundaries
Know what's in the design and what's not before generating

### 6. Iterate on Threshold
Start with 95% threshold, adjust if needed for your design system

### 7. Keep Figma Organized
Use clear naming in Figma for better component names

### 8. Document Deviations
If you must deviate from design, document why

## Related Commands

- `/mcp-figma verify` - Verify Figma MCP setup
- `/mcp-figma test-connection` - Test Figma API connection
- `/task-work TASK-XXX` - Integrate with task workflow
- `/task-complete TASK-XXX` - Complete task after review

## Future Enhancements

**Post-MVP** (after Figma + React validation):
1. Zeplin integration (TASK-004)
2. React Native support (TASK-005)
3. .NET MAUI integration (TASK-006)
4. Design token extraction
5. Component library generation
6. Multi-variant design handling

## Links & Documentation

### Setup Guides
- [Figma MCP Setup](../docs/mcp-setup/figma-mcp-setup.md)
- [Playwright Visual Testing](../docs/mcp-setup/playwright-visual-testing.md)

### Architecture
- [UX Design Subagent Recommendations](../docs/research/ux-design-subagent-recommendations.md)
- [Implementation Plan](../docs/architecture/ux-design-subagents-implementation-plan.md)

### External Documentation
- [Figma MCP Announcement](https://www.figma.com/blog/introducing-figma-mcp-server/)
- [Figma MCP Guide](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server)
- [Figma API Documentation](https://www.figma.com/developers/api)

---

**Command Philosophy**: "Design fidelity is not negotiable. Implement exactly what's in the design, nothing more, nothing less."
