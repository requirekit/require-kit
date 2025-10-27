# FEAT-001: Visual Architecture Diagrams

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DESIGN TOOL LAYER                           │
│                      (External Integration)                         │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                     Figma MCP Server                          │ │
│  │                                                               │ │
│  │  Tools:                                                       │ │
│  │    • get_file        (retrieve Figma file metadata)          │ │
│  │    • get_node        (extract specific node)                 │ │
│  │    • get_images      (download design images)                │ │
│  │    • export_assets   (export design assets)                  │ │
│  └───────────────────────────────────────────────────────────────┘ │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ MCP Protocol
                               │
┌──────────────────────────────▼──────────────────────────────────────┐
│                    ORCHESTRATION LAYER                              │
│              (figma-react-orchestrator agent)                       │
│                                                                     │
│  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │   Phase 0       │  │   Phase 1        │  │   Phase 2        │  │
│  │   MCP Setup     │  │   Design         │  │   Boundary       │  │
│  │   Verification  │  │   Extraction     │  │   Documentation  │  │
│  │                 │  │                  │  │                  │  │
│  │  • Config check │  │  • Node ID       │  │  • Identify      │  │
│  │  • Token valid  │  │    conversion    │  │    boundaries    │  │
│  │  • Connectivity │  │  • 100% accuracy │  │  • Store         │  │
│  │  • Tool check   │  │  • Bidirectional │  │    metadata      │  │
│  └─────────────────┘  └──────────────────┘  └──────────────────┘  │
│                                                                     │
│  ┌─────────────────┐  ┌──────────────────┐                        │
│  │   Phase 5       │  │   Error          │                        │
│  │   Constraint    │  │   Recovery       │                        │
│  │   Validation    │  │                  │                        │
│  │                 │  │  • Retry logic   │                        │
│  │  • Prohibition  │  │  • Exponential   │                        │
│  │    patterns     │  │    backoff       │                        │
│  │  • AST analysis │  │  • Phase-        │                        │
│  │  • 0 violations │  │    specific      │                        │
│  └─────────────────┘  └──────────────────┘                        │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ Data Contracts
                               │
┌──────────────────────────────▼──────────────────────────────────────┐
│                  STACK IMPLEMENTATION LAYER                         │
│              (react-component-generator agent)                      │
│                                                                     │
│  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │   Phase 3       │  │   Phase 4        │  │   Output         │  │
│  │   Component     │  │   Visual         │  │   Structure      │  │
│  │   Generation    │  │   Regression     │  │                  │  │
│  │                 │  │                  │  │  • Component.tsx │  │
│  │  • React TSX    │  │  • Baseline      │  │  • .types.ts     │  │
│  │  • TypeScript   │  │    capture       │  │  • .stories.tsx  │  │
│  │  • Tailwind CSS │  │  • Pixel match   │  │  • .test.tsx     │  │
│  │  • Storybook    │  │  • Playwright    │  │  • .figma-       │  │
│  │                 │  │  • ≥95% fidelity │  │    metadata/     │  │
│  └─────────────────┘  └──────────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## Workflow Phase Sequence

```
┌──────────────────────────────────────────────────────────────────────┐
│                    /figma-to-react Command                           │
│                                                                      │
│  Input: --file {figmaFileId} --node {nodeId}                        │
└──────────────────────────┬───────────────────────────────────────────┘
                           │
                           ▼
        ┌──────────────────────────────────────┐
        │  Phase 0: MCP Setup Verification     │
        │  Duration: 5-10 seconds              │
        │                                      │
        │  1. Check config exists              │
        │  2. Validate API token               │
        │  3. Test connectivity                │
        │  4. Verify tools available           │
        │                                      │
        │  Output: McpConfig | SetupError      │
        └──────────────┬───────────────────────┘
                       │ ✓ MCP Ready
                       ▼
        ┌──────────────────────────────────────┐
        │  Phase 1: Design Extraction          │
        │  Duration: 30-45 seconds             │
        │                                      │
        │  1. Connect to Figma file            │
        │  2. Extract design nodes             │
        │  3. Convert node IDs                 │
        │     "123:456" → "node_123_456"       │
        │  4. Store bidirectional mapping      │
        │                                      │
        │  Output: DesignElements              │
        └──────────────┬───────────────────────┘
                       │ ✓ Elements extracted
                       ▼
        ┌──────────────────────────────────────┐
        │  Phase 2: Boundary Documentation     │
        │  Duration: 10-15 seconds             │
        │                                      │
        │  1. Identify boundaries              │
        │  2. Define conversion zone           │
        │  3. Store metadata                   │
        │                                      │
        │  Output: DesignConstraints           │
        └──────────────┬───────────────────────┘
                       │ ✓ Boundaries defined
                       ▼
        ┌──────────────────────────────────────┐
        │  Phase 3: Component Generation       │
        │  Duration: 30-45 seconds             │
        │                                      │
        │  1. Generate React TSX               │
        │  2. Create TypeScript interfaces     │
        │  3. Apply Tailwind styling           │
        │  4. Generate Storybook story         │
        │                                      │
        │  Output: Component files             │
        └──────────────┬───────────────────────┘
                       │ ✓ Component generated
                       ▼
        ┌──────────────────────────────────────┐
        │  Phase 4: Visual Regression          │
        │  Duration: 20-30 seconds             │
        │                                      │
        │  1. Capture baseline screenshot      │
        │  2. Store in .figma-metadata/        │
        │  3. Generate visual test             │
        │  4. Initial comparison (100%)        │
        │                                      │
        │  Output: Baseline + Visual test      │
        └──────────────┬───────────────────────┘
                       │ ✓ Visual test ready
                       ▼
        ┌──────────────────────────────────────┐
        │  Phase 5: Constraint Validation      │
        │  Duration: 10-15 seconds             │
        │                                      │
        │  1. Run prohibition patterns         │
        │  2. AST analysis                     │
        │  3. Check pixel-perfect threshold    │
        │  4. Generate compliance report       │
        │                                      │
        │  Output: ProhibitionCheck[]          │
        └──────────────┬───────────────────────┘
                       │ ✓ All gates passed
                       ▼
        ┌──────────────────────────────────────┐
        │  Success Report                      │
        │                                      │
        │  ✓ Node ID conversion: 100%          │
        │  ✓ Visual fidelity: ≥95%             │
        │  ✓ Prohibition violations: 0         │
        │  ✓ Performance: <2 minutes           │
        └──────────────────────────────────────┘
```

## Node ID Conversion Flow

```
┌────────────────────────────────────────────────────────────────┐
│                   Figma Node ID Conversion                     │
└────────────────────────────────────────────────────────────────┘

  Figma Node ID              Conversion Process          Code Identifier
  ─────────────              ──────────────────          ───────────────

  "123:456"         ──────►   Replace : with _    ──────►  "node_123_456"
                              Add "node_" prefix

                    Bidirectional Mapping Stored
                    ────────────────────────────
                    .figma-metadata/{Component}/node-id-mapping.json

                    {
                      "forward": {
                        "123:456": "node_123_456",
                        "789:012": "node_789_012"
                      },
                      "reverse": {
                        "node_123_456": "123:456",
                        "node_789_012": "789:012"
                      }
                    }

                    Benefits:
                    ✓ 100% accurate (deterministic)
                    ✓ Reversible (bidirectional)
                    ✓ Traceable (stored mapping)
                    ✓ Valid identifiers (no colons)
```

## Prohibition Checking Flow

```
┌────────────────────────────────────────────────────────────────┐
│               Two-Tier Prohibition Validation                  │
└────────────────────────────────────────────────────────────────┘

  Generated Component Code
  ────────────────────────
       │
       ▼
  ┌───────────────────────┐
  │   TIER 1              │
  │   Pattern Matching    │ ◄─── Fast (milliseconds)
  │                       │
  │   Regex patterns:     │
  │   • /fetch\(/         │
  │   • /useState/        │
  │   • /onClick/         │
  │   • /useEffect/       │
  └───────────┬───────────┘
              │
              ├─► Violations found? ──► FAIL (exit immediately)
              │
              ▼ No violations
  ┌───────────────────────┐
  │   TIER 2              │
  │   AST Analysis        │ ◄─── Accurate (100% detection)
  │                       │
  │   Parse TypeScript:   │
  │   • CallExpression    │
  │   • Hook usage        │
  │   • Event handlers    │
  │   • Side effects      │
  └───────────┬───────────┘
              │
              ├─► Violations found? ──► FAIL (detailed report)
              │
              ▼ No violations
        ✓ PASS (proceed)

  Violation Report Example:
  ─────────────────────────
  ❌ Prohibition Violation Detected

  Item: API_CALL
  Check: ast_analysis
  File: LoginForm.tsx
  Line: 42
  Pattern: CallExpression -> fetch()

  Message: Backend API integration detected
  Prohibition: No backend API calls allowed (static UI only)
```

## Visual Regression Testing Flow

```
┌────────────────────────────────────────────────────────────────┐
│                 Visual Regression Testing                      │
└────────────────────────────────────────────────────────────────┘

  Initial Baseline Capture
  ────────────────────────
       │
       ▼
  ┌───────────────────────┐
  │   Playwright          │
  │   Render Component    │
  │                       │
  │   • Desktop (1920px)  │
  │   • Tablet (768px)    │
  │   • Mobile (375px)    │
  └───────────┬───────────┘
              │
              ▼
  ┌───────────────────────┐
  │   Capture Screenshots │
  └───────────┬───────────┘
              │
              ▼
  ┌───────────────────────┐
  │   Store Baselines     │
  │                       │
  │   .figma-metadata/    │
  │   └── LoginForm/      │
  │       ├── baseline.png│
  │       └── baseline-   │
  │           variants/   │
  │           ├── mobile  │
  │           ├── tablet  │
  │           └── desktop │
  └───────────────────────┘

  Future Test Runs
  ────────────────
       │
       ▼
  ┌───────────────────────┐
  │   Render Component    │
  └───────────┬───────────┘
              │
              ▼
  ┌───────────────────────┐
  │   Capture Current     │
  └───────────┬───────────┘
              │
              ▼
  ┌───────────────────────┐
  │   Pixel Comparison    │
  │                       │
  │   pixelMatch(         │
  │     baseline,         │
  │     current,          │
  │     threshold: 0.95   │
  │   )                   │
  └───────────┬───────────┘
              │
              ├─► Similarity ≥ 95% ──► ✓ PASS
              │
              └─► Similarity < 95% ──► ❌ FAIL
                                         │
                                         ▼
                                    Generate diff image
                                    Highlight differences
                                    Require manual review
```

## Error Recovery Strategy

```
┌────────────────────────────────────────────────────────────────┐
│                   Phase-Specific Error Recovery                │
└────────────────────────────────────────────────────────────────┘

  Phase 0: MCP Verification
  ─────────────────────────
  Error: Config not found
    └─► Retry: 0 (fail immediately)
        └─► Action: Display setup instructions

  Error: Connection failed
    └─► Retry: 3x with exponential backoff (1s, 2s, 4s)
        └─► Action: Check network, verify MCP running


  Phase 1: Design Extraction
  ──────────────────────────
  Error: Node not found
    └─► Retry: 0 (fail immediately)
        └─► Action: Verify Figma file ID and node ID

  Error: Network timeout
    └─► Retry: 2x with fixed backoff (2s, 2s)
        └─► Action: Check Figma API status


  Phase 2: Boundary Documentation
  ───────────────────────────────
  Error: Ambiguous boundaries
    └─► Retry: 0 (needs clarification)
        └─► Action: Prompt user to specify boundaries


  Phase 3: Component Generation
  ─────────────────────────────
  Error: Generation failed
    └─► Retry: 0 (fail immediately)
        └─► Action: Log error, manual review needed


  Phase 4: Visual Regression
  ─────────────────────────
  Error: Screenshot timeout
    └─► Retry: 3x with exponential backoff (500ms, 1s, 2s)
        └─► Action: Check component renders correctly


  Phase 5: Constraint Validation
  ──────────────────────────────
  Error: Prohibition violation
    └─► Retry: 0 (design issue)
        └─► Action: Display violation report, exit

┌────────────────────────────────────────────────────────────────┐
│  Retry Strategy Formula                                        │
│                                                                │
│  delay = exponential                                           │
│          ? baseDelay * Math.pow(2, attempt - 1)                │
│          : baseDelay                                           │
│                                                                │
│  Example (exponential, 1000ms base):                           │
│    Attempt 1: 1000ms (1s)                                      │
│    Attempt 2: 2000ms (2s)                                      │
│    Attempt 3: 4000ms (4s)                                      │
└────────────────────────────────────────────────────────────────┘
```

## File Structure Output

```
Project Root
│
├── src/
│   ├── components/
│   │   └── LoginForm/                      ← Component directory
│   │       ├── LoginForm.tsx               ← React component (Phase 3)
│   │       ├── LoginForm.types.ts          ← TypeScript interfaces (Phase 3)
│   │       ├── LoginForm.stories.tsx       ← Storybook story (Phase 3)
│   │       └── __tests__/
│   │           └── LoginForm.visual.test.tsx ← Visual test (Phase 4)
│   │
│   └── .figma-metadata/
│       └── LoginForm/                      ← Metadata directory
│           ├── design-boundaries.json      ← Boundaries (Phase 2)
│           │   {
│           │     "boundaries": {
│           │       "top": "node_123_456",
│           │       "bottom": "node_789_012",
│           │       "left": "node_345_678",
│           │       "right": "node_901_234"
│           │     },
│           │     "conversionZone": {
│           │       "nodeIds": ["node_123_456", "..."],
│           │       "excludedNodes": []
│           │     }
│           │   }
│           │
│           ├── node-id-mapping.json        ← Node mapping (Phase 1)
│           │   {
│           │     "forward": {
│           │       "123:456": "node_123_456"
│           │     },
│           │     "reverse": {
│           │       "node_123_456": "123:456"
│           │     }
│           │   }
│           │
│           ├── baseline.png                ← Primary baseline (Phase 4)
│           └── baseline-variants/          ← Responsive baselines
│               ├── mobile.png
│               ├── tablet.png
│               └── desktop.png
│
├── installer/global/
│   ├── agents/
│   │   ├── figma-react-orchestrator.md    ← NEW agent
│   │   └── react-component-generator.md   ← NEW agent
│   │
│   └── commands/
│       └── figma-to-react.md              ← NEW command
│
└── docs/
    └── adr/
        └── ADR-002-figma-react-architecture.md ← Architecture decisions
```

## Data Flow Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                      Data Flow Sequence                        │
└────────────────────────────────────────────────────────────────┘

User Command
    │
    │  /figma-to-react --file abc123 --node 456:789
    │
    ▼
┌─────────────────────────────┐
│  figma-react-orchestrator   │
│  (Phase 0)                  │
└──────────────┬──────────────┘
               │
               │  MCP verification request
               ▼
         ┌──────────┐
         │ Figma    │
         │ MCP      │ ──► Config validated ✓
         └──────────┘
               │
               │  get_file, get_node
               ▼
┌─────────────────────────────┐
│  figma-react-orchestrator   │
│  (Phase 1)                  │
└──────────────┬──────────────┘
               │
               │  DesignElements {
               │    nodeId: "123:456",
               │    convertedId: "node_123_456",
               │    properties: {...}
               │  }
               ▼
┌─────────────────────────────┐
│  figma-react-orchestrator   │
│  (Phase 2)                  │
└──────────────┬──────────────┘
               │
               │  DesignConstraints {
               │    boundaries: {...},
               │    conversionZone: {...}
               │  }
               ▼
┌─────────────────────────────┐
│  react-component-generator  │
│  (Phase 3)                  │
└──────────────┬──────────────┘
               │
               │  Component files:
               │    • LoginForm.tsx
               │    • LoginForm.types.ts
               │    • LoginForm.stories.tsx
               ▼
┌─────────────────────────────┐
│  react-component-generator  │
│  (Phase 4)                  │
└──────────────┬──────────────┘
               │
               │  Visual regression:
               │    • baseline.png
               │    • LoginForm.visual.test.tsx
               ▼
┌─────────────────────────────┐
│  figma-react-orchestrator   │
│  (Phase 5)                  │
└──────────────┬──────────────┘
               │
               │  ProhibitionCheck[] {
               │    status: "pass",
               │    violations: []
               │  }
               ▼
         Success Report
         ──────────────
         ✓ All quality gates passed
         ✓ Component generated
         ✓ Tests created
         ✓ <2 minutes
```

## Quality Gate Decision Tree

```
                    Start Task
                        │
                        ▼
             ┌──────────────────────┐
             │  Phase 0: MCP Setup  │
             └──────────┬───────────┘
                        │
          ┌─────────────┴─────────────┐
          │ MCP configured?           │
          └─────────────┬─────────────┘
                        │
           ┌────────────┼────────────┐
           │ No         │ Yes        │
           ▼            ▼
    ❌ FAIL          ✓ Continue
    Exit with           │
    instructions        ▼
                 ┌──────────────────────┐
                 │ Phase 1-3: Generate  │
                 └──────────┬───────────┘
                            │
              ┌─────────────┴─────────────┐
              │ Node ID conversion 100%?  │
              └─────────────┬─────────────┘
                            │
                 ┌──────────┼──────────┐
                 │ No       │ Yes      │
                 ▼          ▼
              ❌ FAIL    ✓ Continue
              Retry 2x      │
                            ▼
                     ┌──────────────────────┐
                     │ Phase 4: Visual Test │
                     └──────────┬───────────┘
                                │
                  ┌─────────────┴─────────────┐
                  │ Visual fidelity ≥95%?     │
                  └─────────────┬─────────────┘
                                │
                     ┌──────────┼──────────┐
                     │ No       │ Yes      │
                     ▼          ▼
                  ❌ FAIL    ✓ Continue
                  Manual       │
                  review       ▼
                        ┌──────────────────────┐
                        │ Phase 5: Prohibition │
                        └──────────┬───────────┘
                                   │
                     ┌─────────────┴─────────────┐
                     │ Zero violations?          │
                     └─────────────┬─────────────┘
                                   │
                        ┌──────────┼──────────┐
                        │ No       │ Yes      │
                        ▼          ▼
                     ❌ FAIL    ✅ SUCCESS
                     Exit        Task complete
                     report      <2 minutes
```

## SOLID Principles Compliance Map

```
┌────────────────────────────────────────────────────────────────┐
│                  SOLID Principles Compliance                   │
└────────────────────────────────────────────────────────────────┘

Single Responsibility Principle (SRP) ✓
─────────────────────────────────────
  figma-react-orchestrator:    Workflow coordination ONLY
  react-component-generator:   Component generation ONLY
  NodeIdConverter:             Node ID conversion ONLY
  ProhibitionChecker:          Constraint validation ONLY


Open/Closed Principle (OCP) ✓
──────────────────────────
  Three-tier architecture allows extension:
    • Add Zeplin support → New design tool layer
    • Add Vue support → New stack implementation layer
    • Core orchestrator remains unchanged


Liskov Substitution Principle (LSP) ✓
────────────────────────────────────
  Stack layers are substitutable:
    react-component-generator ←→ vue-component-generator
    All consume same DesignElements interface
    All produce compatible output structure


Interface Segregation Principle (ISP) ✓
──────────────────────────────────────
  Focused data contracts:
    DesignElements:     Design data only
    DesignConstraints:  Boundary data only
    ProhibitionCheck:   Validation data only
    DesignMetadata:     Traceability data only


Dependency Inversion Principle (DIP) ✓
────────────────────────────────────
  Orchestrator depends on:
    • MCP protocol (abstraction), not Figma specifics
    • Data contracts (interfaces), not implementations
    • Stack layer interface, not concrete React generator
```

---

**These diagrams provide visual representations of:**
- System architecture and component relationships
- Workflow phase execution sequence
- Node ID conversion mechanism
- Prohibition checking two-tier validation
- Visual regression testing process
- Error recovery strategies
- File structure and data flow
- Quality gate decision logic
- SOLID principles compliance

**Reference these diagrams during implementation to maintain architectural alignment.**
