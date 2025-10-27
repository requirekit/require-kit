# FEAT-001: Figma → React UX Design Integration - Implementation Plan

## Overview

This document provides the complete implementation approach for TASK-002: Figma → React UX Design Integration, addressing all 16 functional requirements and 4 identified gaps.

## Executive Summary

**Architecture Pattern**: Three-Tier Orchestration (Design Tool → Orchestrator → Stack Implementation)

**New Components**:
- 2 new agents: `figma-react-orchestrator`, `react-component-generator`
- 1 new command: `/figma-to-react`
- 5 data contract interfaces
- Phase 0 MCP verification system

**Key Decisions**:
- Deterministic node ID conversion with bidirectional mapping (100% accuracy)
- Two-tier prohibition validation (pattern matching + AST analysis)
- `.figma-metadata/` directory for baseline storage and traceability
- Phase-specific retry strategies with exponential backoff
- Phase 0 MCP setup verification (addresses primary failure cause)

**Quality Gates**:
- Node ID conversion: 100% accuracy
- Visual fidelity: ≥95% pixel-perfect
- Prohibition violations: 0
- End-to-end performance: <2 minutes

## Architecture Overview

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
│   │   Phase 0   │  │ Constraint   │  │  Prohibition    │  │
│   │     MCP     │  │ Validation   │  │    Checker      │  │
│   │ Verification│  │              │  │                 │  │
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

## Component Responsibilities

### 1. figma-react-orchestrator (Orchestration Layer)

**Location**: `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/agents/figma-react-orchestrator.md`

**Core Responsibilities**:
- ✅ **Phase 0**: MCP setup verification and tool availability checking
- ✅ **Phase 1**: Design extraction with 100% accurate node ID conversion
- ✅ **Phase 2**: Boundary documentation and conversion zone definition
- ✅ **Phase 5**: Constraint validation and prohibition checking
- ✅ **Orchestration**: Workflow coordination across all phases
- ✅ **Error Handling**: Phase-specific retry strategies

**Key Capabilities**:

```typescript
// Phase 0: MCP Verification (GAP-1)
interface McpVerification {
  verifySetup(): Result<McpConfig, McpSetupError>;
  testConnection(): Result<void, ConnectionError>;
  checkRequiredTools(): Result<string[], MissingToolsError>;
}

// Phase 1: Node ID Conversion
class NodeIdConverter {
  convert(figmaNodeId: string): string;      // Figma ID → Code identifier
  reverse(convertedId: string): string;      // Code identifier → Figma ID
  exportMapping(): NodeIdMapping;            // Bidirectional mapping
}

// Phase 2: Boundary Documentation
interface BoundaryDocumenter {
  identifyBoundaries(nodes: DesignElements[]): DesignConstraints;
  documentConversionZone(boundaries: DesignConstraints): void;
  storeMetadata(metadata: DesignMetadata): void;
}

// Phase 5: Prohibition Checking (GAP-3)
interface ProhibitionChecker {
  checkPatterns(code: string): ProhibitionCheck[];      // Tier 1: Fast pattern matching
  analyzeAst(code: string): ProhibitionCheck[];         // Tier 2: Accurate AST analysis
  generateReport(violations: ProhibitionCheck[]): void;
}
```

### 2. react-component-generator (Stack Implementation Layer)

**Location**: `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/agents/react-component-generator.md`

**Core Responsibilities**:
- ✅ **Phase 3**: React component code generation
- ✅ **Phase 3**: TypeScript interface creation
- ✅ **Phase 3**: Tailwind CSS styling application
- ✅ **Phase 3**: Storybook story generation
- ✅ **Phase 4**: Visual regression test creation
- ✅ **Phase 4**: Baseline image capture and storage (GAP-2)

**Output Structure**:

```
src/
├── components/
│   └── {ComponentName}/
│       ├── {ComponentName}.tsx              # React component with Tailwind
│       ├── {ComponentName}.types.ts         # TypeScript interfaces
│       ├── {ComponentName}.stories.tsx      # Storybook story
│       └── __tests__/
│           └── {ComponentName}.visual.test.tsx  # Playwright visual test
└── .figma-metadata/
    └── {ComponentName}/
        ├── design-boundaries.json           # Boundary documentation
        ├── node-id-mapping.json             # Bidirectional node ID mapping
        └── baseline.png                     # Visual regression baseline
```

**Key Capabilities**:

```typescript
// Phase 3: Component Generation
interface ComponentGenerator {
  generateReactComponent(elements: DesignElements): string;
  generateTypeScriptInterfaces(elements: DesignElements): string;
  applyTailwindStyling(properties: DesignProperties): string;
  generateStorybookStory(component: string): string;
}

// Phase 4: Visual Regression
interface VisualRegressionTester {
  captureBaseline(componentName: string, viewport: Viewport): void;
  storeBaseline(image: Buffer, path: string): void;
  generateVisualTest(componentName: string): string;
  compareToBaseline(current: Buffer, baseline: Buffer): number;
}
```

### 3. /figma-to-react Command

**Location**: `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/commands/figma-to-react.md`

**Command Syntax**:
```bash
/figma-to-react --file {figmaFileId} --node {nodeId} [options]

Options:
  --file, -f          Figma file ID (required)
  --node, -n          Figma node ID to convert (required)
  --output, -o        Output directory (default: src/components)
  --threshold, -t     Visual fidelity threshold (default: 0.95)
  --verify-setup      Verify MCP setup without extraction
  --dry-run           Show plan without execution
  --skip-tests        Skip visual regression tests (not recommended)
```

**Workflow Phases**:

```yaml
Phase 0: MCP Setup Verification (NEW - 5-10 seconds)
  - Check Figma MCP configuration exists
  - Validate API token
  - Test MCP connectivity
  - Verify required tools: get_file, get_node, get_images, export_assets
  - Exit with clear instructions if setup incomplete

Phase 1: Design Extraction (30-45 seconds)
  - Connect to Figma file using MCP
  - Extract design nodes
  - Convert node IDs with 100% accuracy
  - Store bidirectional mapping
  - Validate conversion accuracy

Phase 2: Boundary Documentation (10-15 seconds)
  - Identify top/bottom/left/right boundaries
  - Document conversion zone nodes
  - Create boundary metadata
  - Store in .figma-metadata/{ComponentName}/design-boundaries.json

Phase 3: React Component Generation (30-45 seconds)
  - Generate React component with TypeScript
  - Apply Tailwind CSS styling
  - Create TypeScript interfaces
  - Generate Storybook story
  - Run prohibition checker (Tier 1 + Tier 2)

Phase 4: Visual Regression Setup (20-30 seconds)
  - Capture baseline screenshot with Playwright
  - Store baseline in .figma-metadata/{ComponentName}/baseline.png
  - Generate visual regression test
  - Execute initial comparison (should be 100% match)

Phase 5: Constraint Validation (10-15 seconds)
  - Run prohibition checklist (pattern + AST)
  - Validate pixel-perfect threshold
  - Check component complexity
  - Verify no scope creep
  - Generate compliance report

Total Duration: ~120 seconds (meets <2 minute requirement)
```

## Data Contracts

### 1. DesignElements
```typescript
interface DesignElements {
  nodeId: string;                    // Original Figma node ID
  convertedId: string;               // Converted identifier (node_123_456)
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
```

### 2. DesignConstraints
```typescript
interface DesignConstraints {
  boundaries: {
    top: string;                     // Node ID of top boundary
    bottom: string;                  // Node ID of bottom boundary
    left: string;                    // Node ID of left boundary
    right: string;                   // Node ID of right boundary
  };
  conversionZone: {
    nodeIds: string[];               // All nodes within zone
    excludedNodes: string[];         // Explicitly excluded
  };
  validationRules: {
    pixelPerfectThreshold: number;   // Default: 0.95
    maxComponentDepth: number;       // Prevent over-nesting
  };
}
```

### 3. ProhibitionCheck
```typescript
interface ProhibitionCheck {
  itemId: string;                    // Unique prohibition item ID
  description: string;               // Human-readable description
  checkType: 'pattern_match' | 'ast_analysis';
  status: 'pass' | 'fail';
  violationDetails?: {
    file: string;
    line: number;
    pattern: string;
  };
}
```

### 4. DesignMetadata
```typescript
interface DesignMetadata {
  figmaFileId: string;               // Figma file identifier
  figmaNodeId: string;               // Original node ID
  conversionTimestamp: string;       // ISO 8601 timestamp
  designVersion: string;             // Figma file version
  componentName: string;             // Generated component name
  designBoundaries: DesignConstraints['boundaries'];
}
```

### 5. NodeIdMapping
```typescript
interface NodeIdMapping {
  forward: Record<string, string>;   // Figma ID → Code identifier
  reverse: Record<string, string>;   // Code identifier → Figma ID
}
```

## Key Architectural Decisions

### AD-1: Node ID Conversion (100% Accuracy Requirement)

**Problem**: Figma node IDs contain `:` which are invalid in code identifiers.

**Solution**: Deterministic conversion with bidirectional mapping storage.

```typescript
// Conversion strategy
class NodeIdConverter {
  convert(figmaNodeId: string): string {
    // Example: "123:456" → "node_123_456"
    return `node_${figmaNodeId.replace(/:/g, '_')}`;
  }

  reverse(convertedId: string): string {
    // Example: "node_123_456" → "123:456"
    return this.reverseMapping.get(convertedId) || '';
  }
}

// Storage: .figma-metadata/{ComponentName}/node-id-mapping.json
{
  "forward": { "123:456": "node_123_456" },
  "reverse": { "node_123_456": "123:456" }
}
```

**Benefits**:
- ✅ 100% accurate and reversible
- ✅ Deterministic (same input always produces same output)
- ✅ Stored for traceability
- ✅ Supports bidirectional navigation

### AD-2: Prohibition Checklist Validation (Zero Scope Creep)

**Problem**: Must prevent implementing features not in design scope.

**Solution**: Two-tier validation (fast pattern matching + accurate AST analysis).

**Tier 1: Pattern Matching** (Fast, catches obvious violations)
```typescript
const PROHIBITION_PATTERNS = [
  { pattern: /fetch\(|axios\.|http\./i, message: 'No backend API calls' },
  { pattern: /useState|useReducer|Redux/i, message: 'No state management' },
  { pattern: /onClick|onSubmit/i, message: 'No event handlers (static UI)' },
  { pattern: /useEffect|useLayoutEffect/i, message: 'No side effects' },
  { pattern: /useNavigate|useRouter/i, message: 'No routing' },
];
```

**Tier 2: AST Analysis** (Accurate, catches hidden violations)
```typescript
import { parse } from '@typescript-eslint/parser';

function analyzeProhibitions(code: string): ProhibitionCheck[] {
  const ast = parse(code, { loc: true });
  const violations: ProhibitionCheck[] = [];

  traverse(ast, {
    CallExpression(node) {
      if (isApiCall(node)) {
        violations.push({
          itemId: 'API_CALL',
          checkType: 'ast_analysis',
          status: 'fail',
          violationDetails: { file: 'component.tsx', line: node.loc.start.line }
        });
      }
    }
  });

  return violations;
}
```

**Benefits**:
- ✅ Fast initial screening (pattern matching)
- ✅ Accurate deep analysis (AST)
- ✅ Zero false negatives
- ✅ Detailed violation reporting

### AD-3: Visual Regression Baseline Storage (GAP-2)

**Problem**: Where to store baseline images?

**Solution**: `.figma-metadata/` directory structure.

```
src/
└── .figma-metadata/
    └── {ComponentName}/
        ├── baseline.png                  # Primary baseline
        ├── baseline-variants/            # Responsive variants
        │   ├── mobile.png
        │   ├── tablet.png
        │   └── desktop.png
        ├── design-boundaries.json
        └── node-id-mapping.json
```

**Benefits**:
- ✅ Version controlled (committed to git)
- ✅ Component-specific organization
- ✅ Easy to review in PRs
- ✅ Supports multiple viewport sizes
- ✅ Co-located with metadata

### AD-4: Error Recovery Strategy (GAP-4)

**Problem**: How to handle failures at each phase?

**Solution**: Phase-specific retry strategies with exponential backoff.

```typescript
const RETRY_STRATEGIES: Record<string, RetryStrategy> = {
  'mcp_verification': { maxAttempts: 3, backoffMs: 1000, exponential: true },
  'design_extraction': { maxAttempts: 2, backoffMs: 2000, exponential: false },
  'component_generation': { maxAttempts: 1, backoffMs: 0, exponential: false },
  'visual_regression': { maxAttempts: 3, backoffMs: 500, exponential: true },
};
```

**Error Handling Matrix**:

| Phase | Failure Type | Recovery Action |
|-------|-------------|-----------------|
| Phase 0 | MCP not configured | Exit with setup instructions |
| Phase 0 | MCP connectivity | Retry 3x with backoff, then fail |
| Phase 1 | Node conversion error | Retry 2x, then manual review |
| Phase 2 | Boundary ambiguous | Prompt user for clarification |
| Phase 3 | Generation error | Log and fail (no retry) |
| Phase 4 | Screenshot timeout | Retry 3x with exponential backoff |
| Phase 5 | Prohibition violation | Exit immediately with report |

**Benefits**:
- ✅ Transient errors get retries
- ✅ Configuration errors fail fast
- ✅ Validation errors never retry
- ✅ Clear error messages

### AD-5: MCP Setup Verification (GAP-1 - Phase 0)

**Problem**: Primary MCP failure cause is misconfiguration.

**Solution**: Comprehensive Phase 0 verification before design extraction.

```typescript
interface McpVerification {
  async verifySetup(): Promise<Result<McpConfig, McpSetupError>> {
    // Step 1: Check config file exists
    if (!fs.existsSync(configPath)) {
      return Result.fail({
        code: 'MCP_NOT_CONFIGURED',
        instructions: 'Run: npm install -g figma-mcp && figma-mcp init'
      });
    }

    // Step 2: Validate API token
    if (!config.apiToken) {
      return Result.fail({
        code: 'MISSING_API_TOKEN',
        instructions: 'Run: figma-mcp auth'
      });
    }

    // Step 3: Test connectivity
    await this.testConnection(config);

    // Step 4: Verify required tools
    const requiredTools = ['get_file', 'get_node', 'get_images', 'export_assets'];
    const availableTools = await this.listMcpTools();
    const missingTools = requiredTools.filter(t => !availableTools.includes(t));

    if (missingTools.length > 0) {
      return Result.fail({
        code: 'MISSING_MCP_TOOLS',
        message: `Missing: ${missingTools.join(', ')}`
      });
    }

    return Result.ok(config);
  }
}
```

**User Experience**:
```bash
# Failed verification
$ /figma-to-react --file abc123 --node 456:789

✗ Phase 0: MCP Setup Verification FAILED
  ✗ Figma MCP not configured

Setup Instructions:
1. Install Figma MCP: npm install -g figma-mcp
2. Configure: figma-mcp init
3. Authenticate: figma-mcp auth

Run '/figma-to-react --verify-setup' to test.
```

**Benefits**:
- ✅ Fail fast if MCP not ready
- ✅ Clear, actionable error messages
- ✅ Prevents wasted time
- ✅ Addresses primary failure cause

## Implementation Sequence

### Phase 1: Orchestrator Agent (2-3 hours)
**File**: `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/agents/figma-react-orchestrator.md`

**Deliverables**:
- Agent definition with Phase 0-5 responsibilities
- Node ID converter implementation
- Boundary documenter
- Prohibition checker (Tier 1 + Tier 2)
- Error retry strategies

**Acceptance Criteria**:
- ✅ Agent file follows standard agent template
- ✅ Node ID conversion achieves 100% accuracy
- ✅ Phase 0 MCP verification detects setup issues
- ✅ Prohibition checker catches all violations
- ✅ Error handling covers all failure scenarios

### Phase 2: React Generator Agent (2-3 hours)
**File**: `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/agents/react-component-generator.md`

**Deliverables**:
- Agent definition with Phase 3-4 responsibilities
- React component templates
- TypeScript interface generation
- Tailwind CSS styling logic
- Storybook story templates
- Visual regression test templates

**Acceptance Criteria**:
- ✅ Generates valid React TypeScript components
- ✅ Applies Tailwind CSS correctly
- ✅ Creates Storybook stories
- ✅ Captures baseline images
- ✅ Generates Playwright visual tests

### Phase 3: Visual Regression Testing (1-2 hours)
**Components**: Baseline storage, pixel comparison, test execution

**Deliverables**:
- Baseline capture and storage logic
- Pixel comparison with configurable threshold
- Visual test execution with Playwright
- `.figma-metadata/` directory structure

**Acceptance Criteria**:
- ✅ Baselines stored in correct location
- ✅ Pixel comparison achieves ≥95% threshold
- ✅ Visual tests execute successfully
- ✅ Metadata properly organized

### Phase 4: Command Integration (1 hour)
**File**: `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/commands/figma-to-react.md`

**Deliverables**:
- Command definition
- CLI parameter handling
- Phase orchestration
- Error reporting
- User-facing documentation

**Acceptance Criteria**:
- ✅ Command syntax well-documented
- ✅ All options properly handled
- ✅ Phases execute in correct order
- ✅ Error messages are clear and actionable
- ✅ Examples provided

### Phase 5: End-to-End Testing (2-3 hours)
**Focus**: Complete workflow validation

**Test Scenarios**:
1. **Happy Path**: Successful conversion with all quality gates passed
2. **MCP Setup Failure**: Phase 0 detects missing configuration
3. **Node ID Conversion**: 100 random node IDs converted accurately
4. **Prohibition Violations**: Catches all prohibited patterns
5. **Visual Regression**: Achieves ≥95% pixel-perfect threshold
6. **Error Recovery**: Retry strategies work correctly
7. **Performance**: End-to-end completes in <2 minutes

**Acceptance Criteria**:
- ✅ All test scenarios pass
- ✅ Quality gates enforced correctly
- ✅ Performance requirements met
- ✅ Error handling verified

## Quality Gates

### Gate 1: Node ID Conversion Accuracy
- **Threshold**: 100% accuracy
- **Validation**: Bidirectional mapping verification
- **Test**: Convert 100 random Figma node IDs, verify round-trip

### Gate 2: Visual Fidelity
- **Threshold**: ≥95% pixel-perfect
- **Validation**: Playwright visual comparison
- **Test**: Compare generated component to Figma baseline

### Gate 3: Prohibition Compliance
- **Threshold**: 0 violations
- **Validation**: AST analysis + pattern matching
- **Test**: Run prohibition checker on all generated components

### Gate 4: Performance
- **Threshold**: <2 minutes end-to-end
- **Validation**: Workflow execution timing
- **Test**: Measure time from command invocation to completion

### Gate 5: MCP Setup Detection
- **Threshold**: 100% detection rate
- **Validation**: Phase 0 verification accuracy
- **Test**: Simulate missing config, token, tools - verify detection

## Success Metrics

```yaml
accuracy_metrics:
  node_id_conversion: 100%
  visual_fidelity: ≥95%
  prohibition_detection: 100%
  mcp_setup_detection: 100%

performance_metrics:
  phase_0_verification: <5 seconds
  phase_1_extraction: <45 seconds
  phase_2_boundaries: <15 seconds
  phase_3_generation: <45 seconds
  phase_4_visual_test: <30 seconds
  phase_5_validation: <15 seconds
  total_workflow: <155 seconds (target: <120)

quality_metrics:
  boundary_documentation: 100%
  metadata_traceability: 100%
  test_coverage: ≥80%
  prohibition_false_negatives: 0%

reliability_metrics:
  mcp_connection_success: ≥95%
  generation_success: ≥98%
  visual_test_pass: ≥90%
```

## Risk Mitigation

| Risk | Mitigation Strategy |
|------|-------------------|
| Figma API rate limiting | Cache requests, implement batch processing |
| Node ID format changes | Version validation, conversion accuracy checks |
| Visual regression false positives | Configurable threshold, ignore regions support |
| MCP connectivity issues | Phase 0 verification, retry with backoff |
| Prohibition false negatives | Two-tier validation (pattern + AST) |
| Baseline conflicts | Component-specific directories, versioning |

## Dependencies

### External
- Figma MCP (external tool)
- Playwright (visual testing)
- TypeScript ESLint Parser (AST analysis)
- Pixel Match (image comparison)

### Internal
- task-manager (workflow orchestration)
- test-verifier (test execution)
- architectural-reviewer (design validation)

## File Structure Reference

```
installer/global/
├── agents/
│   ├── figma-react-orchestrator.md         # NEW - Orchestration agent
│   └── react-component-generator.md        # NEW - Stack implementation agent
└── commands/
    └── figma-to-react.md                   # NEW - User-facing command

src/
├── components/                             # Generated components
│   └── {ComponentName}/
│       ├── {ComponentName}.tsx
│       ├── {ComponentName}.types.ts
│       ├── {ComponentName}.stories.tsx
│       └── __tests__/
│           └── {ComponentName}.visual.test.tsx
└── .figma-metadata/                        # Design metadata and baselines
    └── {ComponentName}/
        ├── design-boundaries.json          # Boundary documentation
        ├── node-id-mapping.json            # Node ID conversions
        └── baseline.png                    # Visual regression baseline

docs/
└── adr/
    └── ADR-002-figma-react-architecture.md # This architecture decision record
```

## Next Steps

1. **Architectural Review**: Submit ADR-002 to architectural-reviewer agent
2. **Implementation**: Begin with Phase 1 (Orchestrator Agent)
3. **Testing**: Implement comprehensive test suite
4. **Validation**: Run against real Figma designs
5. **Documentation**: Complete user-facing documentation

## References

- **ADR**: `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/docs/adr/ADR-002-figma-react-architecture.md`
- **Requirements Analysis**: Task file frontmatter (16 functional requirements)
- **Agentecflow Workflow**: `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/commands/task-work.md`
- **Architectural Reviewer**: `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/agents/architectural-reviewer.md`

---

**Status**: Ready for Phase 2.5 Architectural Review
**Next Action**: Invoke architectural-reviewer agent for SOLID/DRY/YAGNI validation
**Estimated Total Implementation Time**: 8-12 hours
