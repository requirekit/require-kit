# Architecture Summary: UX Design Sub-Agents System
## TASK-002 Implementation

**Version**: 1.0
**Date**: 2025-10-08
**Status**: Ready for Implementation

---

## Executive Summary

This document summarizes the architectural design for implementing Figma and Zeplin UX Design Specialist Sub-Agents within the AI Engineer SDLC system. The solution delivers a **three-tier agent architecture** that achieves:

- **Zero scope creep** through automated prohibition checklists
- **Pixel-perfect fidelity** via visual regression testing (>95% similarity)
- **Technology stack agnostic** design extraction
- **Seamless integration** with existing Agentecflow Stage 3 workflow

## Architecture Overview

### Three-Tier Design

```
┌─────────────────────────────────────────────────────┐
│  TIER 1: Global Design Layer                        │
│  • Figma Design Specialist                          │
│  • Zeplin Design Specialist                         │
│  • Design extraction & boundary documentation       │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│  TIER 2: Design Orchestration Layer                 │
│  • Design System Orchestrator                       │
│  • System detection & routing                       │
│  • Constraint enforcement & validation              │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│  TIER 3: Tech Stack Implementation Layer            │
│  • React UX Specialist                              │
│  • React Native UX Specialist                       │
│  • .NET MAUI UX Specialist                          │
│  • Flutter UX Specialist                            │
└─────────────────────────────────────────────────────┘
```

### Key Architectural Decisions

| Decision | Rationale | Trade-off |
|----------|-----------|-----------|
| **Three-tier separation** | High cohesion, low coupling | Additional indirection layer |
| **Orchestrator pattern** | Centralized control & validation | Potential bottleneck (mitigated) |
| **Data contract-based** | Type-safe, versionable communication | Schema maintenance overhead |
| **Multi-layer validation** | Defense in depth for constraints | Some duplication of checks |

## Core Components

### 1. Design System Orchestrator
**Location**: `.claude/agents/design-system-orchestrator.md`

**Responsibilities**:
- Detect configured design system (Figma/Zeplin)
- Convert node IDs (URL format → API format)
- Route to appropriate specialist
- Detect tech stack
- Enforce quality gates

**Key Innovation**: Centralized validation ensures consistent constraint enforcement across all tech stacks.

### 2. Figma Design Specialist
**Location**: `.claude/agents/figma-design-specialist.md`

**Responsibilities**:
- MCP tool orchestration (figma-dev-mode)
- Visible element extraction
- Design boundary documentation
- Prohibition checklist generation

**Key Innovation**: Automated prohibition checklist prevents scope creep by documenting what's NOT present.

### 3. Tech Stack UX Specialists (4x)
**Locations**:
- `.claude/stacks/react/agents/react-ux-specialist.md`
- `.claude/stacks/react-native/agents/react-native-ux-specialist.md`
- `.claude/stacks/maui/agents/maui-ux-specialist.md`
- `.claude/stacks/flutter/agents/flutter-ux-specialist.md`

**Responsibilities**:
- Convert DesignData to stack-specific components
- Apply styling (Tailwind, StyleSheet, XAML, Widgets)
- Generate visual regression tests
- Validate constraint adherence

**Key Innovation**: Unified DesignData format enables code reuse across all stacks.

## Design Patterns

### 1. Delegation with Validation Pattern
```
Orchestrator validates input
    ↓
Specialist processes request
    ↓
Orchestrator validates output
    ↓
Next specialist in chain
```

**Benefit**: Multiple checkpoints catch errors early.

### 2. Prohibition Checklist Pattern
```typescript
interface ProhibitionChecklist {
  elementsNotPresent: string[];      // "No loading spinner"
  interactionsNotShown: string[];    // "No click handler"
  statesNotDefined: string[];        // "No empty state"
  validationNotSpecified: string[];  // "No email validation"
}
```

**Benefit**: Explicit documentation of boundaries prevents scope creep.

### 3. Visual Regression First Pattern
```
Extract design screenshot from Figma
    ↓
Generate Playwright test with baseline
    ↓
Implement component
    ↓
Run test (validates >95% similarity)
```

**Benefit**: Design serves as single source of truth.

## Data Contracts

### DesignData Interface
```typescript
interface DesignData {
  version: "1.0";
  source: "figma" | "zeplin";
  nodeId: string;
  fileKey: string;
  extractedElements: ExtractedElement[];
  designBoundary: {
    visibleElements: string[];
    prohibitedElements: string[];
    explicitText: string[];
  };
  metadata: {
    extractedAt: string;
    extractedBy: string;
    validatedBy: string;
  };
}
```

**Benefit**: Type-safe communication between tiers.

## Quality Gates

### Three-Tier Quality Enforcement

**Tier 1: Design Extraction**
- ✅ All visible elements extracted (100%)
- ✅ Text matches design exactly (100%)
- ✅ Measurements accurate (±2px)
- ✅ Prohibition checklist complete (≥5 items)

**Tier 2: Data Validation**
- ✅ DesignData schema valid
- ✅ Node ID format correct
- ✅ Design boundary defined
- ✅ Data freshness (<24 hours)

**Tier 3: Implementation**
- ✅ Zero constraint violations
- ✅ Visual fidelity >95%
- ✅ Code quality (0 errors)
- ✅ Test coverage (Visual 100%, Unit 80%)

## Integration with Existing System

### Enhanced Task Workflow
```bash
/gather-requirements → /formalize-ears → /generate-bdd → /task-work
                                                              ↓
                                              [NEW] Detect design references
                                                              ↓
                                              [NEW] Invoke design-system-orchestrator
                                                              ↓
                                              [EXISTING] Run all tests (unit + visual)
                                                              ↓
                                              [EXISTING] Update task state
```

**Key Integration Points**:
1. Task Manager: Detects design URLs in task content
2. Test Orchestrator: Executes visual regression tests
3. Quality Gates: Includes visual fidelity metrics

## Implementation Phases

### Phase 1: Foundation (Weeks 1-2)
**Goal**: Core orchestration and Figma extraction working

**Deliverables**:
- Design system orchestrator agent
- Figma design specialist agent
- MCP tool integration
- Node ID conversion logic

**Success Criteria**:
- Orchestrator detects Figma: 100%
- Node ID conversion accuracy: 100%
- MCP tools functional: Yes

### Phase 2: Tech Stack Specialists (Weeks 2-3)
**Goal**: All four tech stacks can implement from DesignData

**Deliverables**:
- React UX specialist
- React Native UX specialist
- MAUI UX specialist
- Flutter UX specialist

**Success Criteria**:
- Component generation success: >90%
- Visual fidelity: >95%
- Constraint violations: 0

### Phase 3: Commands & Integration (Weeks 3-4)
**Goal**: End-to-end workflow functional

**Deliverables**:
- /figma-design command
- Visual testing infrastructure
- Integration with /task-work

**Success Criteria**:
- Command success rate: >95%
- Average implementation time: <2 minutes
- User experience: Smooth

### Phase 4: Zeplin Support (Weeks 4-5)
**Goal**: Zeplin design system supported (Optional/Deferred)

### Phase 5: Testing & Refinement (Weeks 5-6)
**Goal**: Production-ready system

**Deliverables**:
- End-to-end testing
- Performance optimization
- Complete documentation

## Risk Mitigation

### Critical Risks Addressed

| Risk | Mitigation Strategy | Monitoring |
|------|---------------------|------------|
| Node ID conversion failures | Automated validation + clear error messages | Track conversion success rate (target >95%) |
| Scope creep detection gaps | Multi-layer prohibition checklist enforcement | Track violations (target: 0) |
| Visual fidelity false positives | Threshold tuning + diff image generation | Track FP rate (target <5%) |
| MCP tool configuration issues | Comprehensive setup docs + diagnostics command | Track setup success rate (target >90%) |
| Tech stack detection errors | Multiple detection methods + user confirmation | Track detection accuracy (target 100%) |

## Success Metrics

### Primary KPIs

| Metric | Target | Measurement |
|--------|--------|-------------|
| Design extraction accuracy | >95% | Successful extractions / Total attempts |
| Visual fidelity score | >95% | Average Playwright similarity |
| Constraint compliance rate | 100% | Implementations with 0 violations / Total |
| End-to-end success rate | >90% | Successful /figma-design completions / Total |
| Time to implementation | <2 minutes | End timestamp - Start timestamp |

### Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| False positive rate | <5% | False positives / Total visual test runs |
| Scope creep detection accuracy | >95% | True positives / (TP + FN) |
| User-reported issues | <5% | Issues / Total implementations |

## Files to Create

### Agents (6 files)
1. `.claude/agents/design-system-orchestrator.md` (Phase 1)
2. `.claude/agents/figma-design-specialist.md` (Phase 1)
3. `.claude/stacks/react/agents/react-ux-specialist.md` (Phase 2)
4. `.claude/stacks/react-native/agents/react-native-ux-specialist.md` (Phase 2)
5. `.claude/stacks/maui/agents/maui-ux-specialist.md` (Phase 2)
6. `.claude/stacks/flutter/agents/flutter-ux-specialist.md` (Phase 2)

### Commands (3 files)
7. `.claude/commands/figma-design.md` (Phase 3)
8. `.claude/commands/mcp-figma.md` (Phase 1)
9. `.claude/commands/mcp-testing.md` (Phase 3)

### Configuration (5 files)
10. `.claude/settings.json` (Update - Phase 1)
11. `.claude/stacks/react/config.json` (Update - Phase 2)
12. `.claude/stacks/react-native/config.json` (Update - Phase 2)
13. `.claude/stacks/maui/config.json` (Update - Phase 2)
14. `.claude/stacks/flutter/config.json` (Create - Phase 2)

### Testing Infrastructure (2 files)
15. `tests/visual/playwright.config.ts` (Phase 3)
16. Visual test templates (Phase 3)

### Optional (Deferred to Phase 4)
17. `.claude/agents/zeplin-design-specialist.md`
18. `.claude/commands/zeplin-design.md`

## Next Actions

### Immediate (Next 24 hours)
1. ✅ Review and approve architecture plan
2. Create TASK-002 sub-tasks for each phase
3. Set up development environment with MCP tools
4. Begin Phase 1 implementation

### Week 1 Goals
- [ ] Create design-system-orchestrator agent
- [ ] Adapt figma-design-specialist from uk-probate-agent
- [ ] Implement node ID conversion with validation
- [ ] Set up MCP tool integration tests
- [ ] Update .claude/settings.json

### Success Criteria for Week 1
- Orchestrator detects Figma correctly (100%)
- Node ID conversion works flawlessly (100%)
- MCP tools callable and returning data
- Basic error handling provides actionable messages
- 3-5 test designs successfully extracted

## Conclusion

This architecture delivers a **production-ready, scalable solution** that:

✅ Enforces zero scope creep through automated constraints
✅ Ensures pixel-perfect fidelity via visual regression testing
✅ Works across all technology stacks with minimal duplication
✅ Integrates seamlessly with existing Agentecflow workflow
✅ Provides clear error handling and actionable feedback
✅ Enables progressive implementation with working functionality at each phase

**The system is ready for immediate implementation.**

---

**Full Implementation Plan**: [ux-design-subagents-implementation-plan.md](./ux-design-subagents-implementation-plan.md)

**Related Documents**:
- Research: `/docs/research/ux-design-subagent-recommendations.md`
- Requirements: TASK-002 (31 functional requirements, 11 non-functional)
- Testing Strategy: Phase 3 deliverables

**Status**: ✅ APPROVED FOR IMPLEMENTATION
**Next Review**: 2025-10-15 (1 week)
