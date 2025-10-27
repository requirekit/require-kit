# Design-to-Code Common Patterns

**Purpose**: Shared documentation for design system integration commands (Figma, Zeplin) to maintain DRY principles and consistency across all design-to-code workflows.

**Referenced By**:
- `installer/global/commands/figma-to-react.md`
- `installer/global/commands/zeplin-to-maui.md`

---

## Prerequisites (All Design Systems)

### MCP Server Setup

All design-to-code workflows require properly configured MCP servers. Follow these setup guides:

**Figma MCP**:
- Guide: `docs/mcp-setup/figma-mcp-setup.md`
- Required: Figma Personal Access Token
- Test command: Verify Figma MCP tools respond correctly

**Zeplin MCP**:
- Guide: `docs/mcp-setup/zeplin-mcp-setup.md`
- Required: Zeplin Personal Access Token
- Test command: Verify Zeplin MCP tools respond correctly

### Environment Configuration

**Required Environment Variables**:
```bash
# Figma
FIGMA_ACCESS_TOKEN=your_token_here
FIGMA_FILE_KEY=your_default_file_key  # Optional

# Zeplin
ZEPLIN_ACCESS_TOKEN=your_token_here
ZEPLIN_PROJECT_ID=your_default_project_id  # Optional
```

**Settings File**: Update `.claude/settings.json`:
```json
{
  "design_systems": {
    "figma": {
      "enabled": true,
      "mcp_server": "@figma/mcp-server",
      "default_framework": "react"
    },
    "zeplin": {
      "enabled": true,
      "mcp_server": "@zeplin/mcp-server",
      "default_framework": "maui"
    }
  }
}
```

### Technology Stack Requirements

**Figma → React**:
- Node.js 18+
- React 18+
- TypeScript 5+
- Tailwind CSS 3+
- Playwright (for visual regression testing)

**Zeplin → MAUI**:
- .NET 8+
- .NET MAUI workload installed
- Visual Studio 2022+ or VS Code with C# extension
- Platform SDKs (iOS, Android, Windows, macOS as needed)

---

## Common Quality Gates

All design-to-code workflows enforce these quality gates:

### Gate 1: MCP Verification (Phase 0)

**Purpose**: Ensure MCP tools are available before attempting design extraction

**Checks**:
- MCP server installed and running
- Authentication token valid
- All required MCP tools respond
- Connection latency < 2 seconds

**Failure Action**: Display setup guide, abort workflow

**Example Error**:
```
❌ MCP Verification Failed

Figma MCP server not responding.

Please complete setup:
1. Install: npm install -g @figma/mcp-server
2. Configure token: export FIGMA_ACCESS_TOKEN=xxx
3. Test connection: figma-mcp-test

See: docs/mcp-setup/figma-mcp-setup.md
```

### Gate 2: Design Extraction (Phase 1)

**Purpose**: Successfully extract design elements from design system

**Checks**:
- Valid design URL/ID provided
- Design exists and is accessible
- All design elements extracted
- Design metadata complete

**Failure Action**: Retry with exponential backoff (max 3 attempts), then error

**Retry Pattern**:
```
Attempt 1: Immediate
Attempt 2: Wait 1 second
Attempt 3: Wait 2 seconds
All failed: Error with diagnostics
```

### Gate 3: Component Generation (Phase 3)

**Purpose**: Generate pixel-perfect, constraint-compliant component code

**Checks**:
- Code compiles without errors
- All visible design elements represented
- Styling matches design specs exactly (±2px tolerance)
- No prohibited features added (see Prohibition Checklist)

**Failure Action**: Display constraint violations, block generation

### Gate 4: Visual Regression (Phase 4)

**Purpose**: Verify generated component matches design visually

**Figma → React**:
- Playwright visual regression tests
- Screenshot comparison >95% similarity threshold
- Diff images generated on failure

**Zeplin → MAUI**:
- XAML structure validation
- Property value verification
- Platform-specific rendering checks
- Manual screenshot comparison

**Failure Action**: Display diff images, provide remediation steps

### Gate 5: Constraint Validation (Phase 5)

**Purpose**: Ensure zero scope creep - only implement what's in the design

**Two-Tier Validation**:
1. **Pattern Matching**: Check for prohibited keywords in code
2. **AST Analysis**: Verify no extra props, state, or logic added

**Failure Action**: Block component creation, display violations

---

## Prohibition Checklist (12 Categories)

**CRITICAL**: These features must NEVER be implemented without explicit design specification. This list applies to ALL design-to-code workflows.

### Category 1: State Management
**Prohibited**:
- Loading states (spinners, skeleton screens)
- Error states (error messages, retry buttons)
- Empty states (no data placeholders)
- Success states (confirmation messages)

**Exception**: If visible in the design, implement ONLY that specific state

### Category 2: Form Behavior
**Prohibited**:
- Client-side validation beyond what's shown
- Additional validation rules
- "Smart" form behavior (auto-fill, suggestions)
- Form submission handling not in design

**Exception**: Implement validation ONLY if validation messages are visible in design

### Category 3: Data & API
**Prohibited**:
- API integrations
- Data fetching logic
- Sample data beyond what's shown
- Mock data generation

**Exception**: Use exact sample data shown in design, no more, no less

### Category 4: Navigation
**Prohibited**:
- Routing logic
- Link targets not specified
- Navigation guards
- Breadcrumbs or back buttons not in design

**Exception**: Implement navigation ONLY if links/buttons are visible in design

### Category 5: Interactions
**Prohibited**:
- Hover effects not specified
- Click handlers beyond visual feedback
- Keyboard shortcuts
- Touch gestures not shown

**Exception**: Basic accessibility interactions (focus states) are allowed

### Category 6: Animations
**Prohibited**:
- Transitions not specified
- Entrance/exit animations
- Loading animations
- Scroll-based animations

**Exception**: Implement animation ONLY if specified in design system tokens or visible in prototype

### Category 7: Responsive Behavior
**Prohibited**:
- Breakpoints not shown in design
- Mobile adaptations not specified
- Reflow behavior assumptions
- "Smart" responsive behavior

**Exception**: Implement responsive breakpoints ONLY if design includes mobile/tablet/desktop variants

### Category 8: Accessibility (Beyond Basics)
**Prohibited**:
- ARIA attributes not required for visible elements
- Screen reader text beyond visible labels
- Advanced keyboard navigation
- Accessibility enhancements not in design

**Exception**: Basic accessibility (semantic HTML, alt text for visible images) is required

### Category 9: Component API
**Prohibited**:
- Extra props for "flexibility"
- Optional variants not in design
- Configuration options not needed
- "Future-proofing" props

**Exception**: Props ONLY for visible design elements (text content, image URLs, etc.)

### Category 10: Error Handling
**Prohibited**:
- Try-catch blocks (unless design shows error states)
- Fallback UI
- Error logging
- Retry logic

**Exception**: Basic error handling to prevent crashes, but no user-facing error UI

### Category 11: Performance Optimization
**Prohibited**:
- Memoization
- Code splitting
- Lazy loading
- Image optimization beyond standard practice

**Exception**: Basic performance best practices (optimized images, efficient rendering) are allowed

### Category 12: "Best Practices"
**Prohibited**:
- Features not in design justified as "best practice"
- "Users expect this" additions
- "Industry standard" features
- "Nice to have" enhancements

**Exception**: NONE. If it's not in the design, it doesn't get implemented. Period.

### Validation Enforcement

**Pattern Matching** (Tier 1):
```typescript
const PROHIBITED_PATTERNS = [
  /loading\s*=\s*true/i,
  /error\s*=\s*true/i,
  /isLoading/i,
  /showError/i,
  /onSubmit.*async/i,
  /fetch\(/i,
  /axios\./i,
  /useEffect.*fetch/i,
  /@keyframes/i,
  /transition:/i,
  /animation:/i
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

**AST Analysis** (Tier 2):
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

---

## Common Error Handling

### Error Categories

**Category 1: Configuration Errors**
- Missing MCP server
- Invalid access token
- Missing environment variables

**Resolution**: Display setup guide, provide exact commands to fix

**Category 2: Design Access Errors**
- Invalid design URL/ID
- Design not found
- Permission denied

**Resolution**: Validate URL format, check access permissions, suggest alternative IDs

**Category 3: Extraction Failures**
- MCP tool timeout
- Partial extraction
- Missing design elements

**Resolution**: Retry with exponential backoff, display partial results, suggest manual review

**Category 4: Generation Failures**
- Code compilation errors
- Style conversion failures
- Platform-specific issues

**Resolution**: Display specific errors, suggest fixes, provide fallback code

**Category 5: Constraint Violations**
- Prohibited features detected
- Extra props/state added
- Scope creep detected

**Resolution**: Display violation details, block generation, suggest design updates

### Error Message Template

```
❌ {ERROR_CATEGORY}: {ERROR_TITLE}

WHAT WENT WRONG:
{detailed_description}

POSSIBLE CAUSES:
1. {cause_1}
2. {cause_2}
3. {cause_3}

RECOMMENDED ACTIONS:
1. {action_1_with_command}
2. {action_2_with_command}
3. {action_3_with_command}

NEED MORE HELP?
- Documentation: {doc_link}
- Troubleshooting: {troubleshooting_link}
- Common Issues: {faq_link}
```

### Retry Strategy

**Exponential Backoff Pattern**:
```typescript
async function retryWithBackoff<T>(
  operation: () => Promise<T>,
  maxAttempts: number = 3
): Promise<T> {
  let lastError: Error;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await operation();
    } catch (error) {
      lastError = error;

      if (attempt < maxAttempts) {
        const delayMs = Math.pow(2, attempt - 1) * 1000; // 1s, 2s, 4s
        console.log(`Attempt ${attempt} failed, retrying in ${delayMs}ms...`);
        await sleep(delayMs);
      }
    }
  }

  throw new Error(
    `Operation failed after ${maxAttempts} attempts. Last error: ${lastError.message}`
  );
}
```

---

## Common Workflow Patterns

### Pattern 1: Saga Workflow (6 Phases)

All design-to-code commands follow this orchestration pattern:

**Phase 0: MCP Verification**
- Verify MCP server availability
- Test authentication
- Validate tool access
- Display setup guidance if needed

**Phase 1: Design Extraction**
- Parse design URL/ID
- Call MCP tools to extract design
- Retry on failures (exponential backoff)
- Validate extraction completeness

**Phase 2: Boundary Documentation**
- Document ALL visible elements
- Define design boundaries clearly
- Generate prohibition checklist
- Create design metadata

**Phase 3: Component Generation**
- Delegate to stack-specific generator agent
- Apply styling from design tokens
- Implement ONLY visible elements
- Generate with proper TypeScript/C# types

**Phase 4: Visual Regression Testing**
- Generate automated tests (Playwright for web, validation for mobile)
- Compare generated component to design
- Calculate similarity score
- Generate diff images on failure

**Phase 5: Constraint Validation**
- Pattern matching (Tier 1)
- AST analysis (Tier 2)
- Display violations if any
- Block generation if constraints violated

**Phase 6: Artifact Generation**
- Generate component files
- Generate test files
- Generate documentation
- Generate task metadata update

### Pattern 2: Facade Pattern (MCP Complexity Hiding)

**Purpose**: Hide MCP tool complexity from consumers

**Implementation**:
```typescript
class DesignSystemFacade {
  async extractDesign(url: string): Promise<DesignData> {
    // Parse URL
    const designId = this.parseUrl(url);

    // Extract via MCP tools (complex internals)
    const elements = await this.mcpClient.getElements(designId);
    const styles = await this.mcpClient.getStyles(designId);
    const tokens = await this.mcpClient.getTokens(designId);

    // Combine into simple interface
    return {
      elements,
      styles,
      tokens,
      metadata: this.buildMetadata(designId)
    };
  }
}
```

**Benefits**:
- Simple interface for consumers
- Encapsulates MCP complexity
- Easy to swap MCP implementations
- Centralized error handling

### Pattern 3: Data Contracts (ISP Compliance)

**Purpose**: Segregated interfaces following Interface Segregation Principle

**Design Elements Contract**:
```typescript
interface DesignElements {
  elements: ExtractedElement[];
  boundary: DesignBoundary;
}

interface ExtractedElement {
  type: 'text' | 'image' | 'button' | 'input' | 'container';
  id: string;
  properties: Record<string, any>;
  children?: ExtractedElement[];
}

interface DesignBoundary {
  description: string;
  includesOnly: string[];
  excludes: string[];
}
```

**Design Constraints Contract**:
```typescript
interface DesignConstraints {
  prohibitions: ProhibitionChecklist;
}

interface ProhibitionChecklist {
  categories: ProhibitionCategory[];
  validationRules: ValidationRule[];
}

interface ProhibitionCategory {
  name: string;
  prohibited: string[];
  exceptions: string[];
}
```

**Design Metadata Contract**:
```typescript
interface DesignMetadata {
  source: 'figma' | 'zeplin';
  designId: string;
  extractedAt: string;
  version?: string;
  // Design-system specific fields (not shared)
  figma?: {
    fileKey: string;
    nodeId: string;
  };
  zeplin?: {
    projectId: string;
    screenId?: string;
    componentId?: string;
  };
}
```

---

## Progressive Disclosure Documentation Pattern

All design-to-code command documentation follows this structure:

### Level 1: Quick Start (2 minutes)

**Purpose**: Get users running the command immediately

**Content**:
- Single command example
- Minimal explanation
- Link to Level 2 for details

**Example**:
```bash
# Quick Start: Convert Figma design to React component

/figma-to-react https://figma.com/design/abc?node-id=2-2

# That's it! Component generated in src/components/

# Learn more: See "Core Concepts" below
```

### Level 2: Core Concepts (10 minutes)

**Purpose**: Explain key concepts and common usage

**Content**:
- Command syntax and flags
- Common use cases (3-5 examples)
- Key features and benefits
- Link to Level 3 for complete reference

**Example**:
```markdown
## Core Concepts

### Command Syntax
```bash
/figma-to-react <figma-url> [options]
```

### Common Use Cases

**Use Case 1: Convert single component**
```bash
/figma-to-react https://figma.com/design/abc?node-id=2-2
```

**Use Case 2: Specify output directory**
```bash
/figma-to-react https://figma.com/design/abc?node-id=2-2 --output src/components/auth
```

**Use Case 3: Generate with tests**
```bash
/figma-to-react https://figma.com/design/abc?node-id=2-2 --with-tests
```

### Key Features
- Pixel-perfect component generation
- Automatic visual regression tests
- Zero scope creep enforcement
- TypeScript + Tailwind CSS
```

### Level 3: Complete Reference (Full documentation)

**Purpose**: Comprehensive documentation for all features

**Content**:
- All flags and options
- Advanced usage patterns
- Troubleshooting guide
- Architecture and design decisions
- Integration with other commands

**Example**:
```markdown
## Complete Reference

### All Command Options

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--output` | string | `src/components` | Output directory |
| `--with-tests` | boolean | `true` | Generate Playwright tests |
| `--framework` | string | `react` | Target framework |
| `--styling` | string | `tailwind` | CSS approach |

### Advanced Usage

#### Custom Component Name
```bash
/figma-to-react <url> --name MyCustomComponent
```

#### Skip Visual Tests
```bash
/figma-to-react <url> --skip-visual-tests
```

### Architecture

[Detailed architectural documentation...]

### Troubleshooting

[Common issues and solutions...]
```

### Level 4: Examples (Learning by doing)

**Purpose**: Real-world examples with commentary

**Content**:
- Complete workflows from start to finish
- Commentary explaining decisions
- Multiple complexity levels
- Links to generated code

**Example**:
```markdown
## Examples

### Example 1: Simple Button Component

**Design**: https://figma.com/design/abc?node-id=2-2

**Command**:
```bash
/figma-to-react https://figma.com/design/abc?node-id=2-2
```

**Generated Files**:
- `src/components/Button.tsx` (28 lines)
- `src/components/Button.test.tsx` (15 lines)

**Commentary**:
- Design shows single button with hover state
- Generator created TypeScript component with proper types
- Tailwind classes match design specs exactly
- Visual regression test ensures >95% similarity

**View Generated Code**: [Button.tsx](examples/Button.tsx)
```

---

## Published Language (Consistent Terminology)

**Term Standardization**: All design-to-code documentation must use these exact terms.

| Standard Term | Avoid These Terms | Definition |
|--------------|-------------------|------------|
| **Design System** | Design tool, design app | Figma, Zeplin, or other source of truth for designs |
| **MCP Server** | MCP tool, MCP service | Model Context Protocol server that provides design access |
| **Component Generator** | Code generator, builder | Stack-specific agent that generates component code |
| **Visual Regression Test** | Visual test, screenshot test | Automated test comparing generated component to design |
| **Prohibition Checklist** | Constraint list, scope rules | 12-category list of features not to implement |
| **Design Boundary** | Design scope, component boundary | Clear definition of what's included/excluded in design |
| **Constraint Violation** | Scope creep, added feature | When prohibited feature is detected in generated code |
| **Extraction Phase** | Design fetch, design pull | Phase 1 of Saga workflow - getting design from MCP |
| **Generation Phase** | Code creation, component building | Phase 3 of Saga workflow - creating component code |
| **Validation Phase** | Checking phase, verification | Phase 5 of Saga workflow - ensuring constraints met |
| **Orchestrator Agent** | Coordinator, manager | Global agent that orchestrates the 6-phase workflow |
| **Specialist Agent** | Generator agent, builder | Stack-specific agent (react-component-generator, maui-ux-specialist) |

**Usage Example**:
```markdown
✅ CORRECT:
"The orchestrator agent delegates to the component generator in Phase 3."

❌ INCORRECT:
"The coordinator tool sends work to the code builder in the creation step."
```

---

## Cross-Reference Resolution

**Internal References** (within ai-engineer project):
- Use relative paths from project root
- Example: `docs/mcp-setup/figma-mcp-setup.md`

**Command References**:
- Format: `/command-name` (with forward slash)
- Example: `/figma-to-react`, `/task-work`

**Agent References**:
- Format: `agent-name` (no path, markdown-based)
- Example: `figma-react-orchestrator`, `test-orchestrator`

**File References**:
- Use absolute paths from project root
- Example: `installer/global/commands/figma-to-react.md`

**External References**:
- Full URLs with link text
- Example: `[Figma MCP Announcement](https://www.figma.com/blog/...)`

---

## Quality Checklist (Self-Validation)

When creating or updating design-to-code documentation:

**Checklist**:
- [ ] References this shared module for common patterns (DRY)
- [ ] Uses Progressive Disclosure structure (Quick Start → Core Concepts → Complete Reference → Examples)
- [ ] Uses Published Language terms consistently
- [ ] Cross-references resolve correctly
- [ ] All code examples are tested and work
- [ ] Error messages follow template format
- [ ] Prohibition checklist is referenced (not duplicated)
- [ ] Quality gates are documented
- [ ] Workflow diagrams show all 6 phases
- [ ] Success criteria are measurable

---

## Maintenance

**Update Frequency**: Review every 3 months or when:
- New design system added
- MCP tools change significantly
- Prohibition categories evolve
- New quality gates introduced

**Version Control**: Track changes in git commits with clear messages:
```bash
git commit -m "docs(shared): Add Category 13 to Prohibition Checklist"
```

**Breaking Changes**: If common patterns change, update all referencing documents simultaneously.

---

**Last Updated**: 2025-10-11
**Maintained By**: AI Engineer Team
**Version**: 1.0.0
