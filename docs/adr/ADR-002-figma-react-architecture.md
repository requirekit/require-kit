# ADR-002: Figma → React UX Design Integration Architecture

## Status
Proposed

## Context

TASK-002 requires implementing a Figma → React UX design integration system that enables seamless conversion of Figma designs into React components with visual regression testing. The requirements analyst identified 16 functional requirements across 5 core areas, with 4 critical gaps that must be addressed.

**Key Constraints:**
- Node ID conversion must be 100% accurate (primary MCP failure cause)
- Visual fidelity threshold: >95% pixel-perfect
- Zero tolerance for scope creep (prohibition checklist validation)
- Performance: <2 minutes end-to-end workflow
- Simplified scope: Figma + React only (per architectural review)

**Identified Gaps:**
1. **GAP-1**: MCP Tool Configuration (needs Phase 0 verification)
2. **GAP-2**: Visual Regression Baseline Storage
3. **GAP-3**: Prohibition Checklist Validation Mechanism
4. **GAP-4**: Error Recovery Strategy

## Decision

### Architecture Pattern: Three-Tier Orchestration

```
┌─────────────────────────────────────────────────────────────┐
│                    Design Tool Layer                        │
│         (Figma MCP - External Integration)                  │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              Orchestration Layer                            │
│   (figma-react-orchestrator - Core Intelligence)           │
│                                                             │
│   ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│   │   Design    │  │ Constraint   │  │  Prohibition    │  │
│   │ Extraction  │  │ Validation   │  │    Checker      │  │
│   └─────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              Stack Implementation Layer                     │
│       (react-component-generator - Stack-Specific)          │
│                                                             │
│   ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│   │  Component  │  │    Visual    │  │   Storybook     │  │
│   │ Generation  │  │  Regression  │  │   Integration   │  │
│   └─────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Component Breakdown

#### 1. Design Tool Layer (Existing MCP)
- **Figma MCP**: External tool, assumed functional
- **Responsibilities**: Provide design access, node traversal, asset export

#### 2. Orchestration Layer (New Agent)

**Agent**: `figma-react-orchestrator`
**Location**: `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/agents/figma-react-orchestrator.md`

**Responsibilities:**
- Phase 0: MCP tool verification and setup validation
- Design extraction and boundary documentation
- Node ID conversion with 100% accuracy verification
- Constraint validation and prohibition checking
- Workflow orchestration across all phases
- Error handling and retry coordination

**Data Contracts:**

```typescript
// Core design elements extracted from Figma
interface DesignElements {
  nodeId: string;                    // Original Figma node ID
  convertedId: string;               // Converted to valid identifier
  type: 'frame' | 'component' | 'text' | 'image';
  name: string;
  properties: {
    width: number;
    height: number;
    x: number;
    y: number;
    fills?: Fill[];
    strokes?: Stroke[];
    effects?: Effect[];
    constraints?: LayoutConstraints;
  };
  children: DesignElements[];
  metadata: DesignMetadata;
}

// Design constraints and boundaries
interface DesignConstraints {
  boundaries: {
    top: string;                     // Node ID of top boundary
    bottom: string;                  // Node ID of bottom boundary
    left: string;                    // Node ID of left boundary
    right: string;                   // Node ID of right boundary
  };
  conversionZone: {
    nodeIds: string[];               // All nodes within conversion zone
    excludedNodes: string[];         // Explicitly excluded nodes
  };
  validationRules: {
    pixelPerfectThreshold: number;   // Default: 0.95 (95%)
    maxComponentDepth: number;       // Prevent over-nesting
  };
}

// Prohibition checklist tracking
interface ProhibitionCheck {
  itemId: string;
  description: string;
  checkType: 'pattern_match' | 'ast_analysis';
  status: 'pass' | 'fail';
  violationDetails?: {
    file: string;
    line: number;
    pattern: string;
  };
}

// Design metadata for traceability
interface DesignMetadata {
  figmaFileId: string;
  figmaNodeId: string;
  conversionTimestamp: string;
  designVersion: string;
  componentName: string;
  designBoundaries: DesignConstraints['boundaries'];
}
```

#### 3. Stack Implementation Layer (New Agent)

**Agent**: `react-component-generator`
**Location**: `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/agents/react-component-generator.md`

**Responsibilities:**
- React component code generation
- TypeScript interface creation
- Tailwind CSS styling
- Storybook story generation
- Visual regression test creation
- Baseline image management

**Output Structure:**

```
src/
├── components/
│   └── {ComponentName}/
│       ├── {ComponentName}.tsx          # React component
│       ├── {ComponentName}.types.ts     # TypeScript interfaces
│       ├── {ComponentName}.stories.tsx  # Storybook story
│       └── __tests__/
│           └── {ComponentName}.visual.test.tsx
└── .figma-metadata/
    └── {ComponentName}/
        ├── design-boundaries.json       # Boundary documentation
        ├── node-id-mapping.json         # Node ID conversions
        └── baseline.png                 # Visual regression baseline
```

### Command Structure

**New Command**: `/figma-to-react`
**Location**: `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/commands/figma-to-react.md`

**Workflow Phases:**

```yaml
Phase 0: MCP Setup Verification (GAP-1)
  - Verify Figma MCP is configured
  - Test MCP connectivity
  - Validate access tokens
  - Check required MCP tools availability

Phase 1: Design Extraction (FR-1)
  - Connect to Figma file
  - Extract design nodes
  - Convert node IDs to valid identifiers
  - Validate conversion accuracy (100%)

Phase 2: Boundary Documentation (FR-2)
  - Identify design boundaries
  - Document boundary nodes
  - Create conversion zone definition
  - Store boundary metadata

Phase 3: React Component Generation (FR-3)
  - Generate React component code
  - Create TypeScript interfaces
  - Apply Tailwind CSS styling
  - Generate Storybook story

Phase 4: Visual Regression Setup (FR-4)
  - Capture baseline screenshot
  - Store baseline image
  - Generate visual test
  - Configure Playwright test

Phase 5: Constraint Validation (FR-5)
  - Run prohibition checklist
  - Validate pixel-perfect threshold
  - Check component complexity
  - Verify no scope creep
```

## Architecture Decisions

### AD-1: Node ID Conversion Strategy

**Problem**: Figma node IDs contain special characters (e.g., `123:456`) that are invalid in code identifiers.

**Decision**: Use deterministic conversion with bidirectional mapping storage.

**Implementation**:
```typescript
class NodeIdConverter {
  private mapping: Map<string, string> = new Map();
  private reverseMapping: Map<string, string> = new Map();

  convert(figmaNodeId: string): string {
    // Deterministic conversion: replace : with _ and add prefix
    const converted = `node_${figmaNodeId.replace(/:/g, '_')}`;

    // Store bidirectional mapping
    this.mapping.set(figmaNodeId, converted);
    this.reverseMapping.set(converted, figmaNodeId);

    return converted;
  }

  reverse(convertedId: string): string {
    return this.reverseMapping.get(convertedId) || '';
  }

  exportMapping(): NodeIdMapping {
    return {
      forward: Object.fromEntries(this.mapping),
      reverse: Object.fromEntries(this.reverseMapping)
    };
  }
}
```

**Storage**: `/src/.figma-metadata/{ComponentName}/node-id-mapping.json`

**Rationale**: Deterministic, reversible, 100% accurate, stored for traceability.

### AD-2: Prohibition Checklist Validation (GAP-3)

**Problem**: Must prevent implementing features not in design scope.

**Decision**: Two-tier validation using pattern matching + AST analysis.

**Implementation**:

**Tier 1: Pattern Matching** (Fast, catches obvious violations)
```typescript
const PROHIBITION_PATTERNS = [
  // Backend integration
  { pattern: /fetch\(|axios\.|http\./i, message: 'No backend API calls allowed' },
  { pattern: /localStorage|sessionStorage/i, message: 'No local storage allowed' },

  // State management
  { pattern: /useState|useReducer|Redux/i, message: 'No state management allowed' },
  { pattern: /useContext|createContext/i, message: 'No context API allowed' },

  // Complex interactions
  { pattern: /onClick|onSubmit|onChange/i, message: 'No event handlers allowed (static UI only)' },
  { pattern: /useEffect|useLayoutEffect/i, message: 'No side effects allowed' },

  // Routing
  { pattern: /useNavigate|useRouter|Link to=/i, message: 'No routing allowed' },
];
```

**Tier 2: AST Analysis** (Accurate, catches hidden violations)
```typescript
import { parse } from '@typescript-eslint/parser';
import { TSESTree } from '@typescript-eslint/types';

function analyzeProhibitions(code: string): ProhibitionCheck[] {
  const ast = parse(code, { loc: true });
  const violations: ProhibitionCheck[] = [];

  // Traverse AST looking for prohibited patterns
  traverse(ast, {
    CallExpression(node: TSESTree.CallExpression) {
      // Detect API calls
      if (isApiCall(node)) {
        violations.push({
          itemId: 'API_CALL',
          description: 'Backend API integration detected',
          checkType: 'ast_analysis',
          status: 'fail',
          violationDetails: {
            file: 'component.tsx',
            line: node.loc!.start.line,
            pattern: 'CallExpression -> fetch/axios'
          }
        });
      }
    },

    // Similar checks for state management, effects, etc.
  });

  return violations;
}
```

**Rationale**: Two-tier approach balances speed (pattern matching) with accuracy (AST analysis).

### AD-3: Visual Regression Baseline Storage (GAP-2)

**Problem**: Where to store baseline images for visual regression tests?

**Decision**: Store in `.figma-metadata/` directory with component-specific subdirectories.

**Structure**:
```
src/
└── .figma-metadata/
    └── {ComponentName}/
        ├── baseline.png                  # Full component baseline
        ├── baseline-variants/            # Responsive/state variants
        │   ├── mobile.png
        │   ├── tablet.png
        │   └── desktop.png
        ├── design-boundaries.json
        └── node-id-mapping.json
```

**Storage Strategy**:
```typescript
interface BaselineStorage {
  // Capture baseline
  async captureBaseline(componentName: string, viewport: Viewport): Promise<void> {
    const screenshot = await page.screenshot();
    const path = `.figma-metadata/${componentName}/baseline-${viewport.name}.png`;
    await fs.writeFile(path, screenshot);
  }

  // Compare against baseline
  async compareToBaseline(componentName: string, viewport: Viewport): Promise<number> {
    const baseline = await fs.readFile(`.figma-metadata/${componentName}/baseline-${viewport.name}.png`);
    const current = await page.screenshot();

    const similarity = await pixelMatch(baseline, current);
    return similarity; // 0.0 to 1.0 (1.0 = identical)
  }
}
```

**Rationale**:
- Keeps baselines close to components
- Version controlled (committed to git)
- Easy to review in PRs
- Supports multiple viewport sizes

### AD-4: Error Recovery Strategy (GAP-4)

**Problem**: How to handle failures at each phase?

**Decision**: Implement phase-specific retry strategies with exponential backoff.

**Implementation**:
```typescript
interface RetryStrategy {
  maxAttempts: number;
  backoffMs: number;
  exponential: boolean;
}

const PHASE_RETRY_STRATEGIES: Record<string, RetryStrategy> = {
  'mcp_verification': { maxAttempts: 3, backoffMs: 1000, exponential: true },
  'design_extraction': { maxAttempts: 2, backoffMs: 2000, exponential: false },
  'component_generation': { maxAttempts: 1, backoffMs: 0, exponential: false }, // No retry, fails fast
  'visual_regression': { maxAttempts: 3, backoffMs: 500, exponential: true },
};

async function executeWithRetry<T>(
  phase: string,
  operation: () => Promise<T>
): Promise<Result<T, Error>> {
  const strategy = PHASE_RETRY_STRATEGIES[phase];
  let attempt = 0;
  let lastError: Error | null = null;

  while (attempt < strategy.maxAttempts) {
    try {
      const result = await operation();
      return Result.ok(result);
    } catch (error) {
      lastError = error as Error;
      attempt++;

      if (attempt < strategy.maxAttempts) {
        const delay = strategy.exponential
          ? strategy.backoffMs * Math.pow(2, attempt - 1)
          : strategy.backoffMs;

        await sleep(delay);
      }
    }
  }

  return Result.fail(lastError || new Error('Unknown error'));
}
```

**Error Handling Matrix**:

| Phase | Failure Type | Recovery Action |
|-------|-------------|-----------------|
| Phase 0 | MCP not configured | Exit with setup instructions |
| Phase 0 | MCP connectivity | Retry 3x with backoff, then fail |
| Phase 1 | Node ID conversion error | Retry 2x, then manual review |
| Phase 1 | Invalid Figma file | Exit immediately (no retry) |
| Phase 2 | Boundary detection ambiguous | Prompt user for clarification |
| Phase 3 | Component generation error | Log and fail (no retry, review needed) |
| Phase 4 | Screenshot capture timeout | Retry 3x with exponential backoff |
| Phase 5 | Prohibition violation | Exit immediately with violation report |

**Rationale**:
- Transient errors (network) get retries
- Configuration errors fail fast with clear messages
- Validation errors never retry (design issues)
- User guidance for ambiguous cases

### AD-5: MCP Setup Verification (GAP-1 - Phase 0)

**Problem**: Cannot proceed if Figma MCP is not configured.

**Decision**: Implement comprehensive Phase 0 verification before design extraction.

**Implementation**:
```typescript
interface McpVerification {
  async verifySetup(): Promise<Result<McpConfig, McpSetupError>> {
    // Step 1: Check MCP configuration file exists
    const configPath = path.join(os.homedir(), '.figma-mcp', 'config.json');
    if (!fs.existsSync(configPath)) {
      return Result.fail({
        code: 'MCP_NOT_CONFIGURED',
        message: 'Figma MCP not configured',
        instructions: `
          Setup instructions:
          1. Install Figma MCP: npm install -g figma-mcp
          2. Configure access: figma-mcp init
          3. Add Figma API token: figma-mcp auth
        `
      });
    }

    // Step 2: Validate configuration
    const config = await this.loadConfig(configPath);
    if (!config.apiToken) {
      return Result.fail({
        code: 'MISSING_API_TOKEN',
        message: 'Figma API token not found',
        instructions: 'Run: figma-mcp auth'
      });
    }

    // Step 3: Test MCP connectivity
    try {
      await this.testConnection(config);
    } catch (error) {
      return Result.fail({
        code: 'MCP_CONNECTION_FAILED',
        message: 'Cannot connect to Figma MCP',
        error: error.message
      });
    }

    // Step 4: Verify required MCP tools
    const requiredTools = ['get_file', 'get_node', 'get_images', 'export_assets'];
    const availableTools = await this.listMcpTools();
    const missingTools = requiredTools.filter(tool => !availableTools.includes(tool));

    if (missingTools.length > 0) {
      return Result.fail({
        code: 'MISSING_MCP_TOOLS',
        message: `Required MCP tools not available: ${missingTools.join(', ')}`,
        instructions: 'Update Figma MCP to latest version'
      });
    }

    return Result.ok(config);
  }
}
```

**User Experience**:
```bash
# Successful verification
$ /figma-to-react --file abc123 --node 456:789

✓ Phase 0: MCP Setup Verification
  ✓ Figma MCP configured
  ✓ API token valid
  ✓ MCP connection established
  ✓ Required tools available: get_file, get_node, get_images, export_assets

Proceeding to Phase 1...

# Failed verification
$ /figma-to-react --file abc123 --node 456:789

✗ Phase 0: MCP Setup Verification FAILED
  ✗ Figma MCP not configured

Setup Instructions:
1. Install Figma MCP: npm install -g figma-mcp
2. Configure access: figma-mcp init
3. Add Figma API token: figma-mcp auth

Run '/figma-to-react --verify-setup' to test configuration.
```

**Rationale**:
- Fail fast if MCP is not ready
- Clear, actionable error messages
- Prevents wasted time in later phases
- Reduces primary MCP failure cause

## File Structure

### New Files to Create

```
installer/global/
├── agents/
│   ├── figma-react-orchestrator.md         # Orchestration layer agent
│   └── react-component-generator.md        # Stack implementation agent
└── commands/
    └── figma-to-react.md                   # User-facing command

src/
├── components/                             # Generated components
│   └── {ComponentName}/
│       ├── {ComponentName}.tsx
│       ├── {ComponentName}.types.ts
│       ├── {ComponentName}.stories.tsx
│       └── __tests__/
│           └── {ComponentName}.visual.test.tsx
└── .figma-metadata/                        # Design metadata
    └── {ComponentName}/
        ├── design-boundaries.json
        ├── node-id-mapping.json
        └── baseline.png

docs/
└── adr/
    └── ADR-002-figma-react-architecture.md # This document
```

## Implementation Phases

### Phase 0: MCP Setup Verification (NEW - addresses GAP-1)
**Duration**: 5-10 minutes
**Deliverables**:
- MCP configuration validation
- Connectivity testing
- Tool availability check
- Clear error messages with setup instructions

### Phase 1: Orchestrator Agent
**Duration**: 2-3 hours
**Deliverables**:
- `figma-react-orchestrator.md` agent definition
- Node ID conversion implementation
- Boundary documentation logic
- Prohibition checking framework

### Phase 2: React Generator Agent
**Duration**: 2-3 hours
**Deliverables**:
- `react-component-generator.md` agent definition
- React component templates
- TypeScript interface generation
- Tailwind CSS styling logic
- Storybook story templates

### Phase 3: Visual Regression Testing
**Duration**: 1-2 hours
**Deliverables**:
- Playwright visual test templates
- Baseline capture and storage
- Pixel comparison logic
- Regression test execution

### Phase 4: Command Integration
**Duration**: 1 hour
**Deliverables**:
- `/figma-to-react` command definition
- CLI parameter handling
- Phase orchestration
- Error handling and reporting

### Phase 5: Testing and Validation
**Duration**: 2-3 hours
**Deliverables**:
- End-to-end workflow testing
- Node ID conversion accuracy validation
- Prohibition checklist verification
- Visual fidelity testing

## Quality Gates

### Gate 1: Node ID Conversion Accuracy
- **Threshold**: 100% accuracy
- **Validation**: Bidirectional mapping verification
- **Test**: Convert 100 random Figma node IDs, verify round-trip conversion

### Gate 2: Visual Fidelity
- **Threshold**: ≥95% pixel-perfect
- **Validation**: Playwright visual comparison
- **Test**: Compare generated component to Figma design baseline

### Gate 3: Prohibition Compliance
- **Threshold**: Zero violations
- **Validation**: AST analysis + pattern matching
- **Test**: Run prohibition checker on all generated components

### Gate 4: Performance
- **Threshold**: <2 minutes end-to-end
- **Validation**: Workflow execution timing
- **Test**: Measure time from command invocation to test completion

### Gate 5: Constraint Adherence
- **Threshold**: 100% compliance
- **Validation**: Manual checklist verification
- **Test**: Verify no scope creep, no prohibited features

## Success Metrics

```yaml
accuracy_metrics:
  node_id_conversion_accuracy: 100%
  visual_fidelity: ≥95%
  prohibition_violations: 0

performance_metrics:
  end_to_end_workflow: <120 seconds
  mcp_verification_time: <5 seconds
  component_generation_time: <30 seconds
  visual_test_execution: <45 seconds

quality_metrics:
  design_boundary_documentation: 100%
  metadata_traceability: 100%
  test_coverage: ≥80%

reliability_metrics:
  mcp_connection_success_rate: ≥95%
  component_generation_success_rate: ≥98%
  visual_test_pass_rate: ≥90%
```

## Alternatives Considered

### Alternative 1: Direct MCP Integration (Rejected)
**Approach**: Components directly call Figma MCP tools
**Rejection Reason**: Violates separation of concerns, tight coupling, difficult to test

### Alternative 2: Single Monolithic Agent (Rejected)
**Approach**: One agent handles all responsibilities
**Rejection Reason**: Violates SRP, difficult to maintain, not reusable for other design tools

### Alternative 3: Manual Node ID Mapping (Rejected)
**Approach**: User manually maps Figma node IDs to code identifiers
**Rejection Reason**: Error-prone, time-consuming, doesn't scale

### Alternative 4: Git LFS for Baselines (Rejected)
**Approach**: Store baseline images in Git LFS
**Rejection Reason**: Adds complexity, requires LFS setup, not all teams use LFS

## Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Figma API rate limiting | Medium | High | Implement caching, batch requests |
| Node ID format changes | Low | High | Version check, conversion validation |
| Visual regression false positives | High | Medium | Configurable threshold, ignore regions |
| MCP connectivity issues | Medium | High | Phase 0 verification, retry strategy |
| Prohibition checker false negatives | Medium | High | Two-tier validation (pattern + AST) |
| Baseline image conflicts | Medium | Low | Component-specific directories |

## Dependencies

### External Dependencies
- **Figma MCP**: External tool (assumed functional)
- **Playwright**: Visual testing framework
- **TypeScript ESLint Parser**: AST analysis for prohibition checking
- **Pixel Match**: Image comparison library

### Internal Dependencies
- **task-manager**: Task workflow orchestration
- **test-verifier**: Test execution and validation
- **architectural-reviewer**: Design validation before implementation

## Success Criteria

✅ **Phase 0 MCP verification detects setup issues before extraction**
✅ **Node ID conversion achieves 100% accuracy with bidirectional mapping**
✅ **Visual fidelity meets ≥95% threshold**
✅ **Prohibition checker catches all scope creep violations**
✅ **End-to-end workflow completes in <2 minutes**
✅ **Design boundaries fully documented with metadata**
✅ **Generated components pass all quality gates**
✅ **Error recovery handles all failure scenarios gracefully**

## Consequences

### Positive
- ✅ Three-tier architecture supports future design tool integrations (Sketch, Zeplin)
- ✅ Phase 0 verification prevents wasted effort from MCP setup issues
- ✅ Node ID conversion provides 100% traceability
- ✅ Prohibition checking enforces zero scope creep
- ✅ Visual regression ensures pixel-perfect fidelity
- ✅ Modular design enables independent testing

### Negative
- ⚠️ Initial implementation complexity (5 agents + 1 command)
- ⚠️ Requires Figma MCP setup (external dependency)
- ⚠️ Baseline images add to repository size
- ⚠️ AST analysis adds computational overhead

### Neutral
- ℹ️ Supports only Figma + React initially (by design)
- ℹ️ Requires Playwright for visual testing
- ℹ️ Developers must understand node ID conversion

## Future Extensions

### Phase 2 (If Needed)
- Support for Zeplin design tool
- Support for Vue.js components
- Support for Angular components

### Phase 3 (If Needed)
- AI-powered design-to-code optimization
- Responsive variant generation
- Accessibility annotation extraction

## References

- EARS Requirements: `/docs/requirements/approved/REQ-FIGMA-*.md`
- Requirements Analysis: Task file frontmatter (16 functional requirements identified)
- Agentecflow Workflow: `/installer/global/commands/task-work.md`
- Architectural Review: `/installer/global/agents/architectural-reviewer.md`

---

**Review Status**: Ready for Phase 2.5 Architectural Review
**Next Step**: Invoke architectural-reviewer agent for SOLID/DRY/YAGNI validation
