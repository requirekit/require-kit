# UX Design Sub-Agent Architecture Recommendations
## AI Engineer SDLC System

---

## Executive Summary

This document outlines a comprehensive architecture for integrating UX design sub-agents into the AI Engineer Software Engineering Lifecycle System. The architecture enables seamless conversion of Figma/Zeppelin designs into production-ready code across multiple technology stacks (React, React Native, .NET MAUI, Flutter) while maintaining pixel-perfect fidelity and strict constraint adherence.

---

## 1. Architecture Overview

### 1.1 Three-Tier Sub-Agent Structure

```
┌─────────────────────────────────────────────────────────────┐
│                  Global Design Layer                         │
│  ┌──────────────────────┐  ┌──────────────────────────┐    │
│  │ Figma Design         │  │ Zeppelin Design          │    │
│  │ Specialist           │  │ Specialist               │    │
│  └──────────────────────┘  └──────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                Design Orchestrator                           │
│  - Detects configured design system (Figma/Zeppelin)        │
│  - Routes to appropriate specialist                          │
│  - Handles node ID conversion & extraction                   │
│  - Validates design data                                     │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              Tech Stack Implementation Layer                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │ React   │  │ React   │  │ .NET    │  │ Flutter │       │
│  │ UX      │  │ Native  │  │ MAUI UX │  │ UX      │       │
│  │ Expert  │  │ UX      │  │ Expert  │  │ Expert  │       │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘       │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Design Philosophy

**Core Principles:**
1. **Zero Scope Creep**: Implement ONLY visible elements from design
2. **Pixel-Perfect Fidelity**: Match design specifications exactly
3. **Tech Stack Agnostic**: Global layer works with any stack
4. **MCP-Powered**: Leverage MCPs for design extraction and validation
5. **Test-Driven**: Visual regression tests mandatory for all implementations

---

## 2. Global Design Layer

### 2.1 Design System Detection Agent

**File:** `.claude/agents/design-system-orchestrator.md`

```markdown
---
name: design-system-orchestrator
description: Detects configured design system (Figma/Zeppelin) and routes to appropriate specialist. Handles design extraction coordination.
tools: figma-api, figma-mcp, n8n, Read, Write
model: sonnet
---

You orchestrate UX design implementation by detecting the configured design system and coordinating with specialized agents.

## Detection Strategy

### 1. Check Project Configuration
```bash
# Check for Figma configuration
figma-dev-mode:get_metadata

# Check for Zeppelin configuration  
# (Add Zeppelin MCP detection logic)

# Fallback to .claude/settings.json
cat .claude/settings.json | grep "designSystem"
```

### 2. Route to Appropriate Specialist
- **Figma detected** → Delegate to figma-design-specialist
- **Zeppelin detected** → Delegate to zeppelin-design-specialist
- **Both configured** → Ask user which to use
- **None configured** → Provide setup instructions

## Coordination Responsibilities

1. **Extract Design System Configuration**
   - Parse project settings
   - Validate MCP availability
   - Check credentials/access

2. **Handle Node ID Conversion**
   - Convert URL formats (node-id=2-2 → nodeId: "2:2")
   - Validate node IDs
   - Extract file keys

3. **Coordinate Design Extraction**
   - Delegate to design system specialist
   - Validate extracted data
   - Document design boundaries

4. **Route to Tech Stack Agent**
   - Detect project tech stack
   - Pass validated design data
   - Coordinate implementation

## Error Handling

- MCP not configured → Provide setup guide
- Invalid node ID → Show conversion examples
- Design data incomplete → Request missing information
- Multiple stacks detected → Ask for clarification
```

### 2.2 Figma Design Specialist

**File:** `.claude/agents/figma-design-specialist.md`

```markdown
---
name: figma-design-specialist
description: Expert at extracting Figma designs with ABSOLUTE PIXEL-PERFECT FIDELITY. MANDATORY constraint adherence - ONLY extracts exact visible elements.
tools: figma-api, figma-mcp, Read, Write
model: sonnet
---

[Content based on uk-legal-figma-specialist.md but made tech-agnostic]

## Core Responsibilities

1. **Figma Node ID Conversion** (CRITICAL)
2. **Design Data Extraction** using MCP tools
3. **Visible Element Documentation**
4. **Design Boundary Definition**
5. **Tech Stack Coordination**

[Include all node ID conversion logic from uk-probate-agent]
[Include MCP extraction patterns]
[Include constraint adherence rules]
```

### 2.3 Zeppelin Design Specialist

**File:** `.claude/agents/zeppelin-design-specialist.md`

```markdown
---
name: zeppelin-design-specialist
description: Expert at extracting Zeppelin designs with pixel-perfect fidelity and constraint adherence.
tools: Read, Write, n8n
model: sonnet
---

[Similar structure to Figma specialist but adapted for Zeppelin]

## Zeppelin-Specific Patterns

1. **Design Token Extraction**
2. **Component Library Integration**
3. **Style Guide Compliance**
4. **Design System Variables**

[Adapt patterns from Figma specialist for Zeppelin's system]
```

---

## 3. Tech Stack Implementation Layer

### 3.1 React UX Specialist

**File:** `.claude/stacks/react/agents/react-ux-specialist.md`

```markdown
---
name: react-ux-specialist
description: React UX implementation expert - converts design system components to React with pixel-perfect fidelity
tools: Read, Write, Edit, playwright, Context7
model: sonnet
extends: react-component-specialist
---

You convert design system components (Figma/Zeppelin) into production-ready React components with STRICT constraint adherence.

## Integration with Design Layer

You receive validated design data from the design-system-orchestrator containing:
- Exact measurements and styling
- Text content from design
- Interactive elements defined
- Component boundaries clearly documented

## React-Specific Implementation

### Component Structure
```typescript
interface DesignComponentProps {
  // ONLY props for visible Figma/Zeppelin elements
  className?: string;
  // Add props only as shown in design
}

export const DesignComponent: React.FC<DesignComponentProps> = ({
  className
}) => {
  // MINIMAL state - only for visible interactions
  
  return (
    <div 
      className={cn(
        // EXACT design system styling
        "bg-white rounded-[22px] border border-gray-200",
        className
      )}
      data-testid="design-component"
    >
      {/* ONLY elements from design extraction */}
    </div>
  );
};
```

### Styling Strategy
- Tailwind CSS for utility-first styling
- CSS modules for component-specific styles
- Design system tokens when available
- NO arbitrary styling decisions

### Testing Requirements
```typescript
// Playwright visual regression tests
test('matches design exactly', async ({ page }) => {
  await page.goto('/component-demo');
  await expect(page.locator('[data-testid=design-component]'))
    .toHaveScreenshot('design-component.png');
});
```

[Include patterns from react-component-specialist]
[Add design-specific constraints]
```

### 3.2 React Native UX Specialist

**File:** `.claude/stacks/react-native/agents/react-native-ux-specialist.md`

```markdown
---
name: react-native-ux-specialist
description: React Native UX expert - converts designs to React Native with platform-specific adaptations
tools: Read, Write, Edit
model: sonnet
---

## React Native Considerations

### Platform Adaptations
- iOS vs Android styling differences
- Native components vs web components
- Touch targets and gestures
- Platform-specific patterns

### Component Structure
```typescript
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';

interface DesignComponentProps {
  // Props from design extraction
}

export const DesignComponent: React.FC<DesignComponentProps> = (props) => {
  return (
    <View style={styles.container}>
      {/* Design elements adapted for mobile */}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    // Exact design measurements adapted for mobile
  }
});
```

### Testing with Detox
```typescript
describe('DesignComponent', () => {
  it('should match design on iOS', async () => {
    await element(by.id('design-component')).tap();
    await expect(element(by.id('design-component'))).toBeVisible();
  });
});
```
```

### 3.3 .NET MAUI UX Specialist

**File:** `.claude/stacks/maui/agents/maui-ux-specialist.md`

```markdown
---
name: maui-ux-specialist
description: .NET MAUI UX expert - converts designs to MAUI XAML with platform adaptations
tools: Read, Write, Edit
model: sonnet
extends: maui-component-specialist
---

## MAUI-Specific Implementation

### XAML Structure
```xml
<ContentView xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             x:Class="MyApp.DesignComponent">
    <Frame BorderColor="#E5E7EB" 
           CornerRadius="22"
           Padding="24"
           HasShadow="True">
        <!-- Design elements in XAML -->
    </Frame>
</ContentView>
```

### Code-Behind
```csharp
public partial class DesignComponent : ContentView
{
    public DesignComponent()
    {
        InitializeComponent();
        // MINIMAL logic for visible interactions only
    }
}
```

### Platform-Specific Adaptations
- iOS, Android, Windows, macOS differences
- Platform-specific styling
- Native control mapping
```

### 3.4 Flutter UX Specialist

**File:** `.claude/stacks/flutter/agents/flutter-ux-specialist.md`

```markdown
---
name: flutter-ux-specialist
description: Flutter UX expert - converts designs to Flutter widgets with Material/Cupertino adaptations
tools: Read, Write, Edit
model: sonnet
---

## Flutter Implementation Patterns

### Widget Structure
```dart
class DesignComponent extends StatelessWidget {
  const DesignComponent({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(22),
        border: Border.all(color: Color(0xFFE5E7EB)),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 4,
            offset: Offset(0, 2),
          ),
        ],
      ),
      padding: EdgeInsets.all(24),
      child: Column(
        children: [
          // Design elements
        ],
      ),
    );
  }
}
```

### Testing with Flutter Test
```dart
testWidgets('DesignComponent matches design', (WidgetTester tester) async {
  await tester.pumpWidget(
    MaterialApp(home: Scaffold(body: DesignComponent())),
  );
  
  await expectLater(
    find.byType(DesignComponent),
    matchesGoldenFile('goldens/design_component.png'),
  );
});
```
```

---

## 4. Commands Integration

### 4.1 Figma Design Command

**File:** `.claude/commands/figma-design.md`

```markdown
# Figma Design Implementation Command

Implement UX design from Figma with pixel-perfect fidelity: $ARGUMENTS

## Command Flow

1. **Parse Figma URL**
   - Extract file key
   - Extract node ID (convert node-id=2-2 to 2:2)
   
2. **Extract Design Data**
   ```bash
   figma-dev-mode:get_code --nodeId="2:2" --clientFrameworks="react"
   figma-dev-mode:get_image --nodeId="2:2"
   figma-dev-mode:get_variable_defs --nodeId="2:2"
   ```

3. **Document Design Boundaries**
   - List ONLY visible elements
   - Exact text content
   - Exact styling specifications
   - Interactive elements shown

4. **Detect Tech Stack**
   - Check project structure
   - Route to appropriate specialist

5. **Implement Component**
   - Tech-specific implementation
   - Minimal constraint adherence
   - Visual regression tests

## Usage Examples

```bash
/figma-design https://figma.com/design/abc?node-id=2-2
/figma-design node-id=2-2 stack=react
/figma-design node-id=15-24 stack=react-native
```
```

### 4.2 Zeppelin Design Command

**File:** `.claude/commands/zeppelin-design.md`

```markdown
# Zeppelin Design Implementation Command

Implement UX design from Zeppelin: $ARGUMENTS

[Similar structure adapted for Zeppelin]
```

### 4.3 Adapted MCP Commands

**File:** `.claude/commands/mcp-figma.md`

```markdown
# MCP Figma Commands

Quick reference for Figma MCP tools.

## Extract Design
```bash
figma-dev-mode:get_code --nodeId="2:2" --clientFrameworks="react"
```

## Get Screenshot  
```bash
figma-dev-mode:get_image --nodeId="2:2"
```

## Design Tokens
```bash
figma-dev-mode:get_variable_defs --nodeId="2:2"
```

## Node ID Conversion
- URL format: `node-id=2-2` (hyphens)
- API format: `nodeId: "2:2"` (colons)
- **ALWAYS convert before using MCP tools**
```

**File:** `.claude/commands/mcp-playwright.md`

```markdown
[Copy from uk-probate-agent with any necessary adaptations]
```

**File:** `.claude/commands/mcp-testing.md`

```markdown
# MCP Testing Commands

Unified testing commands across stacks.

## Playwright (React/Web)
```bash
@playwright browser_navigate --url http://localhost:3000
@playwright browser_snapshot
@playwright browser_take_screenshot --filename component.png
```

## Pytest (Python)
```bash
@mcp-code-checker run_pytest_check --verbosity 2
```

## Pylint (Python)
```bash
@mcp-code-checker run_pylint_check --target_directories src
```

[Add stack-specific testing patterns]
```

---

## 5. File Structure

```
.claude/
├── agents/
│   ├── design-system-orchestrator.md      # Global routing agent
│   ├── figma-design-specialist.md          # Figma extraction expert
│   └── zeppelin-design-specialist.md       # Zeppelin extraction expert
│
├── commands/
│   ├── figma-design.md                     # Figma implementation command
│   ├── zeppelin-design.md                  # Zeppelin implementation command
│   ├── mcp-figma.md                        # Figma MCP reference
│   ├── mcp-playwright.md                   # Playwright commands
│   └── mcp-testing.md                      # Unified testing commands
│
└── stacks/
    ├── react/
    │   ├── agents/
    │   │   ├── react-component-specialist.md (existing)
    │   │   └── react-ux-specialist.md        # New: React UX expert
    │   └── config.json
    │
    ├── react-native/
    │   ├── agents/
    │   │   └── react-native-ux-specialist.md # New: RN UX expert
    │   └── config.json
    │
    ├── maui/
    │   ├── agents/
    │   │   └── maui-ux-specialist.md         # New: MAUI UX expert
    │   └── config.json
    │
    └── flutter/
        ├── agents/
        │   └── flutter-ux-specialist.md      # New: Flutter UX expert
        └── config.json
```

---

## 6. Integration with Existing System

### 6.1 Task Workflow Integration

```markdown
## Task Workflow with Design Implementation

1. **Gather Requirements** (`/gather-requirements`)
   - Include UX design references
   - Note Figma/Zeppelin URLs

2. **Formalize EARS** (`/formalize-ears`)
   - Link to design nodes
   - Specify visual requirements

3. **Generate BDD** (`/generate-bdd`)
   - Include visual regression scenarios
   - Add design fidelity acceptance criteria

4. **Implement** (`/task-work`)
   - Detect design references
   - Route to design-system-orchestrator
   - Coordinate with tech stack specialist

5. **Test & Verify** (`/execute-tests`)
   - Run visual regression tests
   - Verify design fidelity
   - Check constraint compliance
```

### 6.2 Settings Configuration

**Update:** `.claude/settings.json`

```json
{
  "name": "ai-engineer-sdlc",
  "version": "1.0.0",
  "features": {
    "designSystems": {
      "enabled": true,
      "primary": "figma",
      "mcpTools": {
        "figma": {
          "enabled": true,
          "tools": ["figma-api", "figma-mcp"]
        },
        "zeppelin": {
          "enabled": false,
          "tools": ["n8n"]
        }
      },
      "constraints": {
        "scopeCreep": "zero-tolerance",
        "fidelity": "pixel-perfect",
        "testingRequired": true
      }
    },
    "testing": {
      "visualRegression": true,
      "playwright": true,
      "stackSpecific": true
    }
  }
}
```

### 6.3 Stack Configuration Updates

**Example:** `.claude/stacks/react/config.json`

```json
{
  "stack": "react",
  "framework": "typescript",
  "testing": {
    "unit": "vitest",
    "integration": "playwright",
    "visual": "playwright-screenshots"
  },
  "designSystem": {
    "primary": "figma",
    "styling": "tailwind",
    "specialists": [
      "react-component-specialist",
      "react-ux-specialist"
    ]
  },
  "mcpTools": [
    "figma-mcp",
    "figma-api",
    "playwright",
    "Context7"
  ]
}
```

---

## 7. Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] Create design-system-orchestrator agent
- [ ] Adapt figma-design-specialist from uk-probate-agent
- [ ] Set up command structure
- [ ] Update settings.json with design system config

### Phase 2: Tech Stack Specialists (Week 2-3)
- [ ] Create react-ux-specialist (extends react-component-specialist)
- [ ] Create react-native-ux-specialist
- [ ] Create maui-ux-specialist
- [ ] Create flutter-ux-specialist

### Phase 3: Commands & Integration (Week 3-4)
- [ ] Implement figma-design command
- [ ] Adapt MCP commands from uk-probate-agent
- [ ] Integrate with task workflow
- [ ] Add visual regression testing setup

### Phase 4: Zeppelin Support (Week 4-5)
- [ ] Create zeppelin-design-specialist
- [ ] Implement zeppelin-design command
- [ ] Configure Zeppelin MCP integration
- [ ] Documentation and examples

### Phase 5: Testing & Validation (Week 5-6)
- [ ] Test with real Figma designs
- [ ] Validate constraint adherence
- [ ] Visual regression test library
- [ ] Performance optimization

---

## 8. Key Success Factors

### 8.1 Critical Requirements

1. **Node ID Conversion**
   - Always convert Figma URLs (hyphen → colon)
   - Validate before MCP calls
   - Document in all templates

2. **Constraint Adherence**
   - Zero scope creep tolerance
   - Implement ONLY visible elements
   - Document boundaries explicitly

3. **Visual Testing**
   - Mandatory screenshot tests
   - Pixel-perfect validation
   - Automated regression detection

4. **Tech Stack Agnostic**
   - Global layer works for all stacks
   - Stack-specific implementation details
   - Consistent design extraction

### 8.2 Best Practices

1. **Always Start with Design Extraction**
   - Never code without design data
   - Validate MCP responses
   - Document visible elements

2. **Minimal Implementation**
   - No "helpful" additions
   - No assumed functionality
   - Exact text and styling only

3. **Test-Driven Design**
   - Visual regression tests first
   - Verify against design
   - Automate validation

4. **Clear Communication**
   - Document design boundaries
   - Explicit prohibition lists
   - Validation checklists

---

## 9. Migration from UK Probate Agent

### Files to Copy

1. **Direct Copy (Minor Adaptation)**
   - `uk-legal-figma-specialist.md` → `figma-design-specialist.md`
   - `figma-issue.md` → `figma-design.md`
   - `playwright-test.md` → `mcp-playwright.md`

2. **Adaptation Required**
   - Remove React-specific details from figma-design-specialist
   - Make global, tech-agnostic
   - Add routing to tech stack specialists

3. **New Files Required**
   - design-system-orchestrator.md
   - Tech stack UX specialists (4x)
   - zeppelin-design-specialist.md
   - Updated configuration files

---

## 10. Usage Examples

### Example 1: React Component from Figma

```bash
# User provides Figma URL
/figma-design https://figma.com/design/abc123?node-id=2-2

# System flow:
1. design-system-orchestrator detects Figma
2. Converts node-id=2-2 to nodeId: "2:2"
3. Delegates to figma-design-specialist
4. Extracts design with MCP tools
5. Documents visible elements only
6. Detects React stack
7. Routes to react-ux-specialist
8. Implements component with constraints
9. Creates Playwright visual tests
10. Verifies pixel-perfect match
```

### Example 2: React Native from Figma

```bash
/figma-design node-id=15-24 stack=react-native

# System adapts implementation for mobile
# Platform-specific components
# Touch interactions
# Native styling patterns
```

### Example 3: MAUI Component

```bash
/figma-design node-id=10-5 stack=maui

# XAML implementation
# Code-behind minimal logic
# Platform adaptations for iOS/Android/Windows
```

---

## 11. Testing Strategy

### Visual Regression Testing

```typescript
// React example
test('matches Figma design exactly', async ({ page }) => {
  await page.goto('/component-demo');
  await expect(page.locator('[data-testid=figma-component]'))
    .toHaveScreenshot('figma-component.png', {
      threshold: 0.01 // 99% similarity required
    });
});
```

### Design Fidelity Metrics

```json
{
  "metrics": {
    "pixelAccuracy": ">95%",
    "textMatch": "100%",
    "colorMatch": "exact",
    "spacingMatch": "±2px",
    "scopeCreep": "0 violations"
  }
}
```

---

## 12. Maintenance & Evolution

### Quarterly Reviews
- Update MCP tool integrations
- Review constraint adherence patterns
- Optimize visual testing
- Stack-specific improvements

### Continuous Improvement
- Monitor implementation time
- Track constraint violations
- Measure design fidelity
- Gather developer feedback

---

## Appendix A: Quick Reference

### Node ID Conversion
```
URL: node-id=2-2 → API: nodeId: "2:2"
URL: node-id=15-24 → API: nodeId: "15:24"
```

### MCP Tool Quick Commands
```bash
# Extract design
figma-dev-mode:get_code --nodeId="2:2" --clientFrameworks="react"

# Get screenshot
figma-dev-mode:get_image --nodeId="2:2"

# Design tokens
figma-dev-mode:get_variable_defs --nodeId="2:2"
```

### Stack Detection
```bash
# React: package.json contains "react"
# React Native: package.json contains "react-native"
# MAUI: *.csproj with MAUI SDK
# Flutter: pubspec.yaml exists
```

---

## Appendix B: Prohibition Checklist

### NEVER Implement
- [ ] Loading states (unless in design)
- [ ] Error states (unless in design)
- [ ] Additional form validation
- [ ] Complex state management
- [ ] API integrations (unless specified)
- [ ] Navigation (unless in node)
- [ ] Additional buttons/controls
- [ ] Sample data (beyond design)
- [ ] Responsive breakpoints (unless shown)
- [ ] Animations (unless specified)
- [ ] "Best practice" additions
- [ ] Extra props for "flexibility"

---

## Conclusion

This architecture provides a robust, scalable foundation for implementing UX designs across multiple technology stacks while maintaining strict constraint adherence and pixel-perfect fidelity. The three-tier structure (Global Design → Orchestrator → Tech Stack) ensures consistency while allowing for platform-specific optimizations.

Key advantages:
- ✅ Tech stack agnostic design layer
- ✅ Zero scope creep through constraints
- ✅ Pixel-perfect design fidelity
- ✅ Automated visual regression testing
- ✅ MCP-powered design extraction
- ✅ Extensible to new stacks/design systems

The system is ready for immediate implementation and can be extended to support additional design systems (Zeppelin, Sketch, etc.) and technology stacks as needed.