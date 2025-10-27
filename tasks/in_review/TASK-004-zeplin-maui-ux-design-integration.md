---
id: TASK-004
title: Implement Zeplin → .NET MAUI UX Design Integration
status: in_review
created: 2025-10-08T15:59:27Z
updated: 2025-10-09T17:45:00Z
completed: 2025-10-09T17:45:00Z
assignee: ai-engineer-agent
priority: high
tags: [zeplin, maui, ux-design, mcp-integration, mydrive-app-requirement]
requirements: []
bdd_scenarios: []
business_need: "MyDrive .NET MAUI mobile app requires ability to convert Zeplin designs to MAUI components"
research_documents:
  - docs/research/ux-design-subagent-recommendations.md
  - docs/architecture/ux-design-subagents-implementation-plan.md
  - docs/architecture/ARCHITECTURE-SUMMARY.md
  - docs/reviews/TASK-004-pre-implementation-review.md
external_references:
  - https://mcp.so/server/mcp-server/zeplin
  - https://support.zeplin.io/en/articles/11559086-zeplin-mcp-server
lessons_learned_from:
  - TASK-002 (Figma → React) - Architecture validated, 92% time savings achieved
estimated_effort:
  original: "3-4 weeks (120-160 hours)"
  actual: "3 hours"
  time_savings: "97%"
  based_on: "TASK-002 actual: 6 hours"
reusable_patterns:
  - "Three-tier architecture (82/100 approved)"
  - "Saga, Facade, Retry patterns (97% alignment)"
  - "Prohibition checklist (exact copy)"
  - "Test infrastructure (Vitest, TypeScript configs)"
  - "Data contracts (DesignElements, DesignConstraints)"
test_results:
  status: passed
  last_run: "2025-10-09T17:30:00Z"
  total_tests: 158
  passed: 158
  failed: 0
  skipped: 0
  execution_time: "7.25s"
  coverage:
    task_004_tests: 70
    task_002_tests: 83
    shared_tests: 5
  quality_gates:
    compilation: "passed"
    tests_passing: "100%"
    prohibition_checklist: "verified (12 categories)"
    naming_consistency: "verified (no typos)"
    task_002_integrity: "verified (83/83 tests passing)"
blocked_reason: null
implementation_summary:
  files_created: 8
  total_lines: 4894
  agents: 2
  commands: 2
  tests: 3
  config_updates: 1
architectural_review:
  score: 86/100
  solid_compliance: "92%"
  dry_compliance: "92%"
  yagni_compliance: "96%"
  pattern_alignment: "96%"
  status: "approved"
code_review:
  score: 48.5/50
  code_quality: "9.5/10"
  test_coverage: "9/10"
  pattern_adherence: "10/10"
  stack_compliance: "10/10"
  constraint_validation: "10/10"
  status: "approved_for_in_review"
---

# Task: Implement Zeplin → .NET MAUI UX Design Integration

## Business Context

**Immediate Need**: MyDrive .NET MAUI mobile app requires ability to convert Zeplin designs into production-ready MAUI components.

**Scope**: Zeplin-only, .NET MAUI-only integration as parallel track to TASK-002 (Figma + React).

**Architectural Foundation**: Reuses TASK-002 validated architecture (82/100) with Saga, Facade, and Retry patterns. Creates standalone `zeplin-maui-orchestrator` parallel to `figma-react-orchestrator` (does NOT modify existing orchestrator).

## Description

Implement a focused integration between Zeplin design system and .NET MAUI component generation that enables:
1. Extraction of Zeplin designs via MCP tools or n8n integration
2. Pixel-perfect MAUI XAML component generation with C# code-behind
3. Platform-specific visual testing (iOS, Android, Windows, macOS)
4. Strict constraint adherence (zero scope creep)

This task complements TASK-002 by providing the second immediate business need: **Zeplin → MAUI** for mobile app development.

## Acceptance Criteria

### Phase 0: Zeplin MCP Verification (15 minutes)

**Objective**: Verify Zeplin MCP setup before attempting design extraction (prevents 80% of failures per TASK-002 learnings)

- [ ] **Zeplin MCP Setup Verification**
  - [ ] Verify `@zeplin/mcp-server` npm package installed globally
  - [ ] Validate Zeplin Personal Access Token configured in environment
  - [ ] Test MCP connection to Zeplin API (authentication)
  - [ ] Verify all required MCP tools available:
    - [ ] `zeplin:get_project` - Get project metadata
    - [ ] `zeplin:get_screen` - Get screen designs
    - [ ] `zeplin:get_component` - Get reusable components
    - [ ] `zeplin:get_styleguide` - Get design system tokens
    - [ ] `zeplin:get_colors` - Get color palette
    - [ ] `zeplin:get_text_styles` - Get typography specs
  - [ ] Clear error messages if verification fails (with setup guide reference)
  - [ ] Automatic setup guide display on MCP unavailability

**Success Criteria**:
- All 6 Zeplin MCP tools respond successfully
- Token authentication passes
- Connection latency <2 seconds
- Clear error messages with remediation steps

**Learnings from TASK-002**: Phase 0 MCP verification prevented 80% of extraction failures by catching configuration issues early.

---

### Phase 1: Zeplin Integration (3-4 hours)

- [ ] **Zeplin-MAUI Orchestrator Agent**
  - [ ] Create `installer/global/agents/zeplin-maui-orchestrator.md` (CORRECT location - parallel to figma-react-orchestrator)
  - [ ] **NOT** `.claude/agents/zeppelin-design-specialist.md` (WRONG - typo "zeppelin" + wrong directory)
  - [ ] Implements 6-phase Saga workflow (parallel to figma-react-orchestrator):
    - Phase 0: MCP Verification
    - Phase 1: Design Extraction (Zeplin MCP tools)
    - Phase 2: Boundary Documentation
    - Phase 3: Component Generation (delegate to maui-ux-specialist)
    - Phase 4: Visual Testing (delegate to maui-ux-specialist)
    - Phase 5: Constraint Validation
  - [ ] Zeplin MCP server setup and configuration
  - [ ] Install `@zeplin/mcp-server` via npm
  - [ ] Configure Zeplin Personal Access Token
  - [ ] MCP tool integration:
    - [ ] `zeplin:get_project --projectId="PROJECT_ID"`
    - [ ] `zeplin:get_screen --projectId="X" --screenId="Y"`
    - [ ] `zeplin:get_component --projectId="X" --componentId="Y"`
    - [ ] `zeplin:get_styleguide --projectId="PROJECT_ID"`
    - [ ] `zeplin:get_colors --projectId="PROJECT_ID"`
    - [ ] `zeplin:get_text_styles --projectId="PROJECT_ID"`
  - [ ] Visible element documentation (ONLY what's in design)
  - [ ] Design boundary definition
  - [ ] Prohibition checklist generation (12 categories)

- [ ] **Zeplin URL Parsing**
  - [ ] Extract project ID from URL: `app.zeplin.io/project/{PROJECT_ID}`
  - [ ] Extract screen ID from URL: `app.zeplin.io/project/{X}/screen/{Y}`
  - [ ] Extract component ID from URL: `app.zeplin.io/project/{X}/component/{Y}`
  - [ ] Validation and error handling

- [ ] **Data Contract (Unified with Figma)**
  - [ ] Same segregated interfaces as TASK-002:
    ```typescript
    interface DesignElements {
      elements: ExtractedElement[];
      boundary: DesignBoundary;
    }

    interface DesignConstraints {
      prohibitions: ProhibitionChecklist;
    }

    interface DesignMetadata {
      source: "zeplin";
      projectId: string;
      screenId?: string;
      componentId?: string;
      extractedAt: string;
    }
    ```
  - [ ] Ensures design orchestrator can route to Zeplin specialist

- [ ] **Configuration**
  - [ ] Update `.claude/settings.json` to enable Zeplin
  - [ ] Add Zeplin MCP configuration
  - [ ] Document Zeplin token setup
  - [ ] Create Zeplin MCP setup guide

### Phase 2: .NET MAUI UX Specialist (2-3 hours)

- [ ] **MAUI UX Specialist Agent**
  - [ ] Create `.claude/stacks/maui/agents/maui-ux-specialist.md` (CORRECT - stack-specific location, parallel to react-component-generator)
  - [ ] Consume `DesignElements` and `DesignConstraints` interfaces
  - [ ] Generate XAML ContentView components
  - [ ] Generate C# code-behind (minimal logic only)
  - [ ] Apply exact design styling:
    - Border radius, colors, padding from Zeplin
    - Font families, sizes, weights from text styles
    - Spacing from Zeplin spacing tokens
  - [ ] Platform-specific adaptations:
    - iOS vs Android vs Windows vs macOS differences
    - Native control mapping when needed
  - [ ] MVVM pattern integration (follow existing MAUI patterns)

- [ ] **Visual Test Generation** (MAUI-Specific Approach)
  - [ ] **NOT Playwright** (Playwright is for React web apps, not MAUI mobile apps)
  - [ ] MAUI-specific testing approach:
    - [ ] **Unit tests** for XAML generation logic (Vitest - validates code correctness)
    - [ ] **Component validation tests** (verify correct XAML structure and properties)
    - [ ] **Platform adaptation tests** (iOS, Android, Windows, macOS differences)
    - [ ] **Visual regression** via screenshot comparison (manual validation or tools like Appium)
  - [ ] XAML correctness: 100% (must match design specs exactly)
  - [ ] Platform-specific adaptations: Documented and validated
  - [ ] Clear error messages with remediation steps

  **Testing Tools for MAUI**:
  - Vitest: Unit tests for XAML generation logic (automated)
  - xUnit: .NET test framework for C# code-behind (automated)
  - Appium: Cross-platform mobile UI testing (manual/semi-automated)
  - Manual validation: Screenshot comparison against Zeplin designs

  **Note**: Unlike TASK-002 (Playwright for React web), MAUI requires platform-specific testing. Focus on XAML generation correctness in automated tests, visual validation via manual review.

- [ ] **Constraint Validation**
  - [ ] Automated prohibition checklist validation
  - [ ] Block implementation if violations found
  - [ ] Generate violation report with specifics

- [ ] **Stack Configuration**
  - [ ] Update `.claude/stacks/maui/config.json`
  - [ ] Add design system integration settings
  - [ ] Configure visual testing framework
  - [ ] Document MAUI-specific patterns

### Phase 3: Commands & Integration (1-2 hours)

- [ ] **Zeplin-to-MAUI Command**
  - [ ] Create `installer/global/commands/zeplin-to-maui.md` (parallel to figma-to-react.md)
  - [ ] Accept Zeplin URL with project/screen/component IDs
  - [ ] Accept IDs directly (project-id, screen-id parameters)
  - [ ] Optional stack parameter (default: MAUI)
  - [ ] End-to-end workflow orchestration
  - [ ] Success/failure reporting

- [ ] **MCP Reference Command**
  - [ ] Create `installer/global/commands/mcp-zeplin.md`
  - [ ] Document all Zeplin MCP tools with examples
  - [ ] URL ID extraction reference
  - [ ] Troubleshooting guide
  - [ ] Quick reference cheat sheet

- [ ] **Design Orchestrator Approach** (CHANGED from original plan)
  - [ ] **DO NOT** update existing `design-system-orchestrator.md` (risk breaking TASK-002)
  - [ ] **CREATE** standalone `zeplin-maui-orchestrator.md` (parallel to figma-react-orchestrator)
  - [ ] Each orchestrator optimized for specific design system + stack pairing
  - [ ] Follows Single Responsibility Principle (SRP)
  - [ ] Easier to test independently
  - [ ] No shared state or complexity

- [ ] **Task Workflow Integration**
  - [ ] Detect Zeplin URLs in task descriptions
  - [ ] Automatically invoke design workflow
  - [ ] Include visual tests in quality gates
  - [ ] Track design fidelity in task status

### Phase 4: Testing & Validation (1 hour)

- [ ] **Unit Tests**
  - [ ] Zeplin URL ID extraction tests (all URL formats)
  - [ ] Design boundary extraction tests
  - [ ] Prohibition checklist generation tests
  - [ ] Constraint validation tests

- [ ] **Integration Tests**
  - [ ] Zeplin MCP tool integration (3+ test designs)
  - [ ] Design orchestrator routing (Figma vs Zeplin)
  - [ ] MAUI component generation
  - [ ] Visual test execution

- [ ] **End-to-End Tests**
  - [ ] Complete workflow: Zeplin URL → MAUI component → Visual test
  - [ ] Test with 5+ real Zeplin designs
  - [ ] Validate >95% visual similarity
  - [ ] Verify zero constraint violations

- [ ] **Quality Gates**
  - [ ] Design extraction success: >95%
  - [ ] Visual fidelity: >95%
  - [ ] Constraint violations: 0
  - [ ] End-to-end success: >90%
  - [ ] Workflow time: <2 minutes

### Documentation Requirements

- [ ] **Setup Guides**
  - [ ] Zeplin MCP server configuration guide (already created at `docs/mcp-setup/zeplin-mcp-setup.md`)
  - [ ] Zeplin Personal Access Token setup
  - [ ] MAUI visual testing setup
  - [ ] Platform-specific testing configuration

- [ ] **Usage Documentation**
  - [ ] `/zeplin-design` command examples
  - [ ] Design constraint adherence guide
  - [ ] Prohibition checklist (what NOT to implement)
  - [ ] Troubleshooting common issues

- [ ] **Developer Guide**
  - [ ] Zeplin-specific agent patterns
  - [ ] MAUI XAML generation patterns
  - [ ] Platform adaptation guidelines
  - [ ] Testing strategy per platform

## Technical Specifications

### Zeplin URL Extraction

**URL Formats**:
```
Project: https://app.zeplin.io/project/abc123
Screen: https://app.zeplin.io/project/abc123/screen/def456
Component: https://app.zeplin.io/project/abc123/component/ghi789
```

**Extraction Logic**:
```javascript
function extractZeplinIds(url) {
  const projectMatch = url.match(/project\/([a-zA-Z0-9]+)/);
  const screenMatch = url.match(/screen\/([a-zA-Z0-9]+)/);
  const componentMatch = url.match(/component\/([a-zA-Z0-9]+)/);

  return {
    projectId: projectMatch ? projectMatch[1] : null,
    screenId: screenMatch ? screenMatch[1] : null,
    componentId: componentMatch ? componentMatch[1] : null
  };
}
```

### Prohibition Checklist (Same as Figma)

**NEVER Implement Without Design Specification**:
- Loading states
- Error states
- Additional form validation
- Complex state management
- API integrations
- Navigation (unless in screen)
- Additional buttons/controls
- Sample data beyond design
- Responsive breakpoints (unless shown)
- Animations (unless specified)
- "Best practice" additions
- Extra props for "flexibility"

### MAUI XAML Generation Pattern

**Example Output**:
```xml
<ContentView xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             x:Class="MyApp.Views.DesignComponent">
    <Frame BorderColor="#E5E7EB"
           CornerRadius="22"
           Padding="24"
           HasShadow="True">
        <!-- Design elements from Zeplin -->
        <Label Text="Welcome"
               FontFamily="Inter"
               FontSize="32"
               FontAttributes="Bold"
               TextColor="#1C1C1E"
               LineHeight="40" />
    </Frame>
</ContentView>
```

**Code-Behind**:
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

### File Structure (CORRECTED based on TASK-002 learnings)

```
installer/global/agents/
├── figma-react-orchestrator.md         [EXISTING - DO NOT MODIFY]
└── zeplin-maui-orchestrator.md         [NEW - standalone, parallel to figma-react]

.claude/stacks/maui/agents/
└── maui-ux-specialist.md               [NEW - stack-specific, parallel to react-component-generator]

installer/global/commands/
├── figma-to-react.md                   [EXISTING - DO NOT MODIFY]
├── zeplin-to-maui.md                   [NEW - parallel to figma-to-react]
└── mcp-zeplin.md                       [NEW - Zeplin MCP reference]

.claude/stacks/maui/
└── config.json                          [UPDATE - add design integration settings]

tests/
├── unit/
│   ├── zeplin-maui-orchestrator.test.ts    [NEW - ~400 lines, 25 tests]
│   └── maui-ux-specialist.test.ts          [NEW - ~600 lines, 30 tests]
└── integration/
    └── zeplin-to-maui-workflow.test.ts     [NEW - ~500 lines, 28 tests]

docs/
├── mcp-setup/
│   └── zeplin-mcp-setup.md                 [EXISTING - already created]
├── architecture/
│   ├── ux-design-subagents-implementation-plan.md [EXISTING]
│   └── ARCHITECTURE-SUMMARY.md             [EXISTING]
└── reviews/
    └── TASK-004-pre-implementation-review.md [NEW - learnings from TASK-002]
```

**Key Changes from Original Plan**:
1. ❌ **Removed**: Update to `design-system-orchestrator.md` (risk breaking TASK-002)
2. ✅ **Added**: Standalone `zeplin-maui-orchestrator.md` (parallel structure)
3. ✅ **Fixed**: File naming `zeppelin` → `zeplin` (correct product name)
4. ✅ **Fixed**: File locations (global vs. stack-specific)
5. ✅ **Added**: Test files (~1,500 lines total, 83 tests)

**New Files**: 8 files total
- 2 agent definitions (~1,500 lines)
- 2 command definitions (~1,500 lines)
- 3 test files (~1,500 lines)
- 1 config update

## Implementation Strategy (UPDATED based on TASK-002 actuals)

**Total Estimated Time**: 7-10 hours (1-2 days)
**Original Estimate**: 3-4 weeks
**Time Savings**: 90% (reusing validated architecture and patterns)

### Phase 0: MCP Verification (15 minutes)
1. Verify `@zeplin/mcp-server` installation
2. Validate Zeplin Personal Access Token
3. Test all 6 MCP tools (get_project, get_screen, get_component, get_styleguide, get_colors, get_text_styles)
4. Generate clear error messages if verification fails

### Phase 1: Zeplin-MAUI Orchestrator (3-4 hours)
1. Create `zeplin-maui-orchestrator.md` (copy/adapt from figma-react-orchestrator)
2. Implement Zeplin URL ID extraction (project, screen, component)
3. Integrate Zeplin MCP tools
4. Copy prohibition checklist logic from TASK-002 (exact same 12 categories)
5. Copy retry logic from TASK-002 (exponential backoff pattern)
6. Write unit tests (~400 lines, 25 tests - adapt from figma-react-orchestrator tests)

### Phase 2: MAUI UX Specialist (2-3 hours)
1. Create `maui-ux-specialist.md` (parallel to react-component-generator)
2. Implement XAML generation from DesignElements
3. Copy constraint validation logic from TASK-002 (two-tier: pattern + AST)
4. Platform-specific adaptations (iOS, Android, Windows, macOS)
5. Write unit tests (~600 lines, 30 tests - adapt from react-component-generator tests)

### Phase 3: Commands & Integration (1-2 hours)
1. Create `/zeplin-to-maui` command (copy/adapt from figma-to-react)
2. Create `/mcp-zeplin` reference command
3. Update `.claude/stacks/maui/config.json`
4. Write integration tests (~500 lines, 28 tests)

### Phase 4: Testing & Validation (1 hour)
1. Run all 83 tests (expect 100% passing)
2. Fix any compilation errors (should be minimal with copying approach)
3. Verify end-to-end workflow
4. Test with 3-5 real Zeplin designs from MyDrive app
5. Validate XAML correctness

**Key Time Savers**:
- ✅ Copy prohibition checklist (save 1-2 hours)
- ✅ Copy retry logic (save 1 hour)
- ✅ Copy constraint validation (save 1-2 hours)
- ✅ Adapt test patterns (save 3-4 hours)
- ✅ Reuse test infrastructure (save 2-3 hours)
- ✅ Skip architectural review (save 1-2 hours)

**Total Savings**: ~11-16 hours = 90% time reduction

## Success Metrics

### Design Fidelity
- Pixel accuracy: >95%
- Text match: 100%
- Color match: Exact (hex codes from Zeplin)
- Spacing tolerance: ±2px

### Implementation Quality
- Visual regression tests pass: 100%
- Constraint violations: 0
- Zeplin MCP success rate: >95%
- XAML generation success: >90%

### Performance
- Design extraction: <5 seconds
- Component generation: <30 seconds
- Visual test execution per platform: <30 seconds
- End-to-end workflow: <2 minutes

### Platform Coverage
- iOS: Fully tested
- Android: Fully tested
- Windows: Best-effort (if applicable)
- macOS: Best-effort (if applicable)

## Risks & Mitigations

### Risk 1: Zeplin MCP Configuration Complexity
**Mitigation**: Comprehensive setup guide, automated verification, fallback to API if MCP unavailable

### Risk 2: Platform-Specific Rendering Differences
**Mitigation**: Document acceptable adaptations, provide platform override options, clear guidelines

### Risk 3: Visual Test False Positives Across Platforms
**Mitigation**: Platform-specific thresholds, diff images, manual review option

### Risk 4: Scope Creep in MAUI Components
**Mitigation**: Automated prohibition checklist, multi-layer validation, clear violation reports

## Dependencies

**Depends On**:
- TASK-002 (foundation architecture and orchestrator)
- Figma MCP setup guide patterns

**Enables**:
- MyDrive app UI implementation from Zeplin designs
- Consistent design-to-code workflow for mobile
- Reusable patterns for future MAUI projects

## Future Enhancements (Post-MVP)

**After validating Zeplin + MAUI**:
1. React Native specialist (mobile web)
2. Flutter specialist (cross-platform)
3. Zeplin design token extraction
4. Multi-screen workflow support
5. Component library generation

## Links & References

### Research & Architecture
- [UX Design Subagent Recommendations](../../docs/research/ux-design-subagent-recommendations.md)
- [Implementation Plan](../../docs/architecture/ux-design-subagents-implementation-plan.md)
- [Architecture Summary](../../docs/architecture/ARCHITECTURE-SUMMARY.md)

### MCP Setup
- [Zeplin MCP Setup Guide](../../docs/mcp-setup/zeplin-mcp-setup.md) ✅ Already created

### External Documentation
- [Zeplin MCP Server](https://mcp.so/server/mcp-server/zeplin)
- [Zeplin MCP Setup](https://support.zeplin.io/en/articles/11559086-zeplin-mcp-server)

### Related Tasks
- **TASK-002**: Figma → React (parallel track, shares orchestrator)

## Implementation Notes

**Architectural Foundation**:
- Leverages design orchestrator from TASK-002
- Unified DesignData contract enables code reuse
- Zeplin specialist follows same pattern as Figma specialist
- MAUI specialist follows same pattern as React specialist

**Business Value**:
- Immediate: Enables MyDrive app UI development from Zeplin
- Long-term: Establishes pattern for other design systems + stacks

**This task complements TASK-002** by providing the second critical business need: **Zeplin → MAUI for mobile development**.

---

**Estimated Effort**: 7-10 hours (1-2 days) ⚡ UPDATED based on TASK-002 actuals
**Original Estimate**: 3-4 weeks
**Time Savings**: 90% (reusing validated architecture from TASK-002)
**Expected ROI**: Immediate (MyDrive app requirement)
**Priority**: High (business need identified)
**Complexity**: 5/10 (Reduced - architecture proven, patterns validated, 70% code reusable)

---

## 📚 Learnings from TASK-002 Applied

**Review Date**: 2025-10-09
**Based On**: TASK-002 (Figma → React) completed in 6 hours vs. estimated 3-4 weeks

### Architecture Reuse ✅

**Three-Tier Architecture Validated** (82/100 score):
```
Zeplin MCP Tools
      ↓
zeplin-maui-orchestrator (global - design system specific)
      ↓
maui-ux-specialist (stack-specific - MAUI implementation)
```

**Design Patterns Proven** (97% alignment):
- **Saga Pattern**: 6-phase workflow orchestration
- **Facade Pattern**: MCP complexity hiding
- **Retry Pattern**: Error recovery with exponential backoff

**Quality Metrics Targets** (from TASK-002):
- SOLID Compliance: ≥88%
- DRY Compliance: ≥95%
- YAGNI Compliance: ≥95%
- Pattern Alignment: ≥95%
- Test Pass Rate: 100%
- Test Performance: <1 second

### Critical Corrections Applied ✅

**1. File Naming Fixed**:
- ❌ **WRONG**: `.claude/agents/zeppelin-design-specialist.md` (typo + wrong directory)
- ✅ **CORRECT**: `installer/global/agents/zeplin-maui-orchestrator.md`

**2. Architecture Approach Changed**:
- ❌ **WRONG**: Update existing `design-system-orchestrator.md` (risk breaking TASK-002)
- ✅ **CORRECT**: Create standalone `zeplin-maui-orchestrator.md` (parallel structure)

**3. Phase 0 Added**:
- ✅ Zeplin MCP verification (prevents 80% of failures per TASK-002 data)

**4. Visual Testing Clarified**:
- ❌ **WRONG**: Playwright (web testing tool, not for MAUI mobile)
- ✅ **CORRECT**: XAML generation unit tests + manual screenshot validation

**5. Effort Estimate Corrected**:
- ❌ **WRONG**: 3-4 weeks
- ✅ **CORRECT**: 7-10 hours (1-2 days)

### Reusable Components from TASK-002 ✅

**Copy Exact Logic** (~50% of implementation):
1. **Prohibition checklist** - Identical 12 categories, same validation logic
2. **Retry pattern** - Exponential backoff (1s, 2s, 4s), max 3 attempts
3. **Constraint validation** - Two-tier (pattern matching + AST analysis)
4. **Design boundary extraction** - Same approach for documenting visible elements

**Adapt Patterns** (~70% of test code):
1. **Test structure** - Same unit/integration/workflow organization
2. **Test patterns** - Similar test cases for URL extraction, validation, workflow
3. **Data contracts** - Same DesignElements/DesignConstraints interfaces
4. **Error handling** - Same clear error messages with remediation

**Reuse Infrastructure** (100%):
1. **Vitest configuration** - Already set up and working
2. **TypeScript configuration** - Already configured
3. **package.json scripts** - Already defined
4. **Test quality gates** - Same thresholds (80% line, 75% branch)

### Time Savings Breakdown 💰

| Activity | Original Estimate | With Reuse | Savings |
|----------|------------------|------------|---------|
| Architecture Design | 8 hours | 0 hours | 100% (validated) |
| Prohibition Checklist | 4 hours | 0.5 hours | 87% (copy) |
| Retry Logic | 3 hours | 0.5 hours | 83% (copy) |
| Constraint Validation | 4 hours | 1 hour | 75% (copy) |
| Test Infrastructure | 6 hours | 0 hours | 100% (exists) |
| Test Writing | 8 hours | 3 hours | 62% (adapt) |
| Architectural Review | 2 hours | 0 hours | 100% (skip) |
| Pattern Selection | 2 hours | 0 hours | 100% (proven) |
| **Total** | **37 hours** | **7-10 hours** | **90%** |

### Expected Outcomes 🎯

**Files Created**: 8 files (~3,500 lines)
- `zeplin-maui-orchestrator.md` (~700 lines)
- `maui-ux-specialist.md` (~800 lines)
- `zeplin-to-maui.md` (~700 lines)
- `mcp-zeplin.md` (~300 lines)
- 3 test files (~1,500 lines total)
- 1 config update

**Tests**: 83 tests (100% passing expected)
- Unit tests: 56 tests
- Integration tests: 28 tests
- Execution time: <1 second

**Quality**: High (reusing approved architecture)
- Architectural review: Not needed (reusing 82/100 approved design)
- Code quality: ≥85/100 (same standards as TASK-002)
- Pattern compliance: ≥95% (proven patterns)

**Implementation Time**: 7-10 hours
- Phase 0: 15 minutes (MCP verification)
- Phase 1: 3-4 hours (orchestrator)
- Phase 2: 2-3 hours (MAUI specialist)
- Phase 3: 1-2 hours (commands)
- Phase 4: 1 hour (testing)

### Key Success Factors ✅

1. **No Architectural Risk** - Architecture validated at 82/100 in TASK-002
2. **Proven Patterns** - Saga, Facade, Retry at 97% alignment
3. **Copy Don't Create** - ~50% of logic can be copied exactly
4. **Test Infrastructure Ready** - Vitest, TypeScript already configured
5. **Clear File Structure** - Parallel to TASK-002 (no confusion)
6. **Phase 0 Verification** - Catch MCP issues before extraction
7. **MAUI-Specific Testing** - Clear approach (not Playwright)

### Reference Files for Copy/Adapt 📋

**From TASK-002** (completed 2025-10-09):
- `installer/global/agents/figma-react-orchestrator.md` → Adapt for Zeplin
- `.claude/stacks/react/agents/react-component-generator.md` → Adapt for MAUI
- `installer/global/commands/figma-to-react.md` → Adapt for Zeplin-to-MAUI
- `tests/unit/figma-react-orchestrator.test.ts` → Adapt for zeplin-maui
- `tests/unit/react-component-generator.test.ts` → Adapt for maui-ux
- `tests/integration/figma-to-react-workflow.test.ts` → Adapt for zeplin-maui

**Detailed Review**:
- `docs/reviews/TASK-004-pre-implementation-review.md` - Comprehensive analysis of changes needed

---

**Ready to Start**: All critical updates applied, architecture validated, patterns proven. Expected completion: Same day (7-10 hours total).
