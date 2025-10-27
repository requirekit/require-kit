# TASK-004 Pre-Implementation Review

**Review Date**: 2025-10-09
**Reviewed Against**: TASK-002 (Figma → React) - Completed 2025-10-09
**Reviewer**: Claude Code
**Purpose**: Apply learnings from TASK-002 to optimize TASK-004 before implementation

---

## Executive Summary

**Recommendation**: ✅ **UPDATE TASK-004 BEFORE IMPLEMENTATION**

**Key Findings**:
- TASK-004 can leverage **92% time savings** from TASK-002 learnings
- **Architecture is already correct** (three-tier design)
- **7 critical improvements** identified based on TASK-002 experience
- **Estimated actual effort**: 6-8 hours (vs. estimated 3-4 weeks)
- **No architectural review needed** - can reuse approved patterns

---

## Learnings from TASK-002

### 1. Implementation Time Reality

**TASK-002 Estimates**:
- **Estimated**: 3-4 weeks
- **Actual**: 6 hours
- **Time savings**: 92%

**Why the Massive Difference**:
1. Markdown agent definitions are much faster than coding
2. Test-first approach with comprehensive test suite
3. Clear architectural patterns (Saga, Facade, Retry)
4. Reusable data contracts
5. No actual runtime implementation needed (agent definitions only)

**Apply to TASK-004**:
- **Current estimate**: 3-4 weeks
- **Realistic estimate**: 6-8 hours (slightly longer for new design system + stack)
- **Expected time savings**: 90%+

---

### 2. Architecture is Already Correct

**TASK-002 False Alarm**:
- Code review flagged "missing file" as blocker
- File existed in correct location (stack-specific directory)
- Architecture correctly separated global vs. stack-specific agents

**TASK-004 Architecture**:
```
Global (design system agnostic):
  installer/global/agents/
    └── design-system-orchestrator.md (UPDATE to add Zeplin routing)

Design System Specific:
  installer/global/agents/
    └── zeplin-design-specialist.md (NEW - parallel to figma-react-orchestrator)

Stack Specific:
  .claude/stacks/maui/agents/
    └── maui-ux-specialist.md (NEW - parallel to react-component-generator)
```

**Status**: ✅ Correct separation already planned

---

### 3. Critical File Naming Issue

**TASK-004 Current Plan**:
```
.claude/agents/zeppelin-design-specialist.md  ❌ WRONG
```

**Issues**:
1. **Typo**: "zeppelin" vs. "zeplin" (product name is Zeplin, not Zeppelin)
2. **Wrong location**: Should be in `installer/global/agents/` (like figma-react-orchestrator)
3. **Inconsistent naming**: Should follow figma-react-orchestrator pattern

**Corrected Plan**:
```
installer/global/agents/
  └── zeplin-maui-orchestrator.md  ✅ CORRECT
    OR
  └── zeplin-design-specialist.md  ✅ ACCEPTABLE (if generic)
```

**Recommendation**: Use `zeplin-maui-orchestrator.md` to parallel `figma-react-orchestrator.md`

---

### 4. Reuse Design-System-Orchestrator

**TASK-004 Current Plan**:
- Update `design-system-orchestrator.md` to support Zeplin
- Detect Zeplin URLs in addition to Figma

**TASK-002 Learnings**:
- `figma-react-orchestrator` is SPECIFIC to Figma + React
- NOT a generic "design-system-orchestrator"

**Better Approach**:
Create parallel orchestrators instead of updating a shared one:

```
installer/global/agents/
  ├── figma-react-orchestrator.md    (EXISTING - Figma + React)
  └── zeplin-maui-orchestrator.md    (NEW - Zeplin + MAUI)

Future:
  ├── figma-vue-orchestrator.md      (Figma + Vue)
  └── zeplin-react-native-orchestrator.md (Zeplin + React Native)
```

**Why This is Better**:
- ✅ No risk of breaking TASK-002 implementation
- ✅ Each orchestrator optimized for specific combination
- ✅ Easier to test independently
- ✅ Follows Single Responsibility Principle
- ✅ No shared state or complexity

**Recommendation**: Create `zeplin-maui-orchestrator.md` as standalone agent

---

### 5. Data Contract Compatibility

**TASK-004 Plan**:
```typescript
interface DesignMetadata {
  source: "zeplin";  // Different from Figma
  projectId: string;
  screenId?: string;
  componentId?: string;
  extractedAt: string;
}
```

**TASK-002 Implementation**:
```typescript
interface DesignMetadata {
  source: "figma";
  nodeId: string;
  fileKey: string;
  extractedAt: string;
}
```

**Issue**: Source-specific field names break abstraction

**Improved Design** (for future unified orchestrator):
```typescript
interface DesignMetadata {
  source: "figma" | "zeplin" | "sketch";
  sourceId: string;           // Generic: nodeId, projectId, etc.
  sourceContext?: string;     // Generic: fileKey, screenId, etc.
  extractedAt: string;
}
```

**For TASK-004**: Keep current design (source-specific fields are fine for MVP)

**Recommendation**: Document this as known limitation for future refactoring

---

### 6. Test Infrastructure Setup

**TASK-002 Created**:
- `vitest.config.ts` (32 lines)
- `package.json` (29 lines)
- `tsconfig.json` (51 lines)

**TASK-004 Advantage**:
- ✅ Test infrastructure already exists
- ✅ Can reuse Vitest configuration
- ✅ Can reuse TypeScript configuration
- ✅ Only need to add new test files

**New Test Files Needed**:
```
tests/
├── unit/
│   ├── zeplin-maui-orchestrator.test.ts  (NEW - ~400 lines, 25 tests)
│   └── maui-ux-specialist.test.ts        (NEW - ~600 lines, 30 tests)
└── integration/
    └── zeplin-to-maui-workflow.test.ts   (NEW - ~500 lines, 28 tests)
```

**Estimated**: 1,500 lines of tests (vs. 1,581 for TASK-002)

**Time Savings**: 2-3 hours (infrastructure already configured)

---

### 7. Quality Gates & Architectural Review

**TASK-002 Process**:
1. Requirements Analysis (requirements-analyst)
2. Implementation Planning (software-architect)
3. Pattern Suggestion (design-patterns MCP)
4. Architectural Review (architectural-reviewer) → 82/100
5. Implementation (task-manager)
6. Testing (test-verifier) → 83/83 passed
7. Code Review (code-reviewer) → 85/100

**TASK-004 Can Skip**:
- ❌ Pattern Suggestion (patterns already validated)
- ❌ Architectural Review (reusing approved three-tier architecture)

**TASK-004 Must Do**:
- ✅ Requirements Analysis (Zeplin-specific requirements)
- ✅ Implementation Planning (Zeplin + MAUI specifics)
- ✅ Implementation (agents + tests)
- ✅ Testing (verify all tests pass)
- ✅ Code Review (ensure quality)

**Time Savings**: 1-2 hours (skip architectural review)

---

## Critical Improvements for TASK-004

### Improvement #1: Fix File Naming and Location

**Current (WRONG)**:
```
.claude/agents/zeppelin-design-specialist.md
```

**Corrected**:
```
installer/global/agents/zeplin-maui-orchestrator.md
.claude/stacks/maui/agents/maui-ux-specialist.md
```

**Action**: Update task file structure section

---

### Improvement #2: Don't Update design-system-orchestrator.md

**Current Plan**:
```
├── agents/
│   ├── design-system-orchestrator.md      [UPDATE - Add Zeplin routing]
```

**Better Plan**:
```
installer/global/agents/
  ├── figma-react-orchestrator.md    (EXISTING - don't touch)
  └── zeplin-maui-orchestrator.md    (NEW - standalone)
```

**Why**:
- Avoids breaking TASK-002
- Simpler to test
- Each orchestrator optimized for specific pairing
- Follows SRP (Single Responsibility Principle)

**Action**: Remove "UPDATE" from task, create new standalone orchestrator

---

### Improvement #3: Clarify Visual Testing Strategy

**TASK-004 Current Plan**:
```
- [ ] MAUI-specific visual testing strategy
- [ ] Screenshot tests for each platform
- [ ] >95% similarity threshold
```

**TASK-002 Learnings**:
- Visual regression tests are in test files (not runtime)
- Tests validate logic, not actual screenshots
- Playwright is for React web apps (not MAUI mobile apps)

**Clarified for MAUI**:
- **Framework**: Use MAUI UI testing frameworks (not Playwright)
  - iOS: XCUITest or Appium
  - Android: Espresso or Appium
  - Windows: WinAppDriver or Appium
- **Test approach**: Validate XAML generation logic (unit tests)
- **Visual validation**: Manual or screenshot comparison tools
- **Acceptance**: >95% threshold applies to XAML correctness, not screenshots

**Action**: Update "Visual Test Generation" section with MAUI-specific approach

---

### Improvement #4: Add Zeplin MCP Verification Phase

**TASK-002 Success Factor**:
- Phase 0: MCP Verification (prevents 80% of failures)
- Verified Figma MCP tools before extraction

**TASK-004 Should Add**:
```
Phase 0: Zeplin MCP Verification (5-10s)
  - Verify @zeplin/mcp-server installed
  - Validate Zeplin Personal Access Token
  - Test connection to Zeplin API
  - Verify required MCP tools available:
    - zeplin:get_project
    - zeplin:get_screen
    - zeplin:get_component
    - zeplin:get_styleguide
    - zeplin:get_colors
    - zeplin:get_text_styles
```

**Action**: Add Phase 0 to implementation workflow

---

### Improvement #5: Reduce Estimated Effort

**Current Estimate**: 3-4 weeks

**Realistic Estimate** (based on TASK-002 actuals):
- Phase 1: Zeplin Integration (3-4 hours)
  - Zeplin specialist agent (1 hour)
  - URL parsing logic (30 mins)
  - MCP tool integration (1 hour)
  - Unit tests (1 hour)

- Phase 2: MAUI Specialist (2-3 hours)
  - MAUI UX specialist agent (1.5 hours)
  - XAML generation logic (1 hour)
  - Unit tests (1 hour)

- Phase 3: Integration (1-2 hours)
  - /zeplin-design command (1 hour)
  - Integration tests (1 hour)

- Phase 4: Testing & Validation (1 hour)
  - Run all tests (15 mins)
  - Fix any issues (45 mins)

**Total**: 7-10 hours (vs. 3-4 weeks estimated)

**Action**: Update estimated effort to "1-2 days" instead of "3-4 weeks"

---

### Improvement #6: Leverage TASK-002 Patterns

**Reusable Components from TASK-002**:
1. ✅ Prohibition checklist (12 categories) - copy exact logic
2. ✅ Design boundary extraction - same approach
3. ✅ Constraint validation - same two-tier (pattern + AST)
4. ✅ Retry pattern - same exponential backoff
5. ✅ Node ID conversion pattern - adapt for Zeplin IDs
6. ✅ Test structure - parallel unit/integration tests
7. ✅ Data contracts - same DesignElements/DesignConstraints

**Copy These Test Patterns**:
```
tests/unit/zeplin-maui-orchestrator.test.ts
  ├── URL ID extraction (6 tests) ← Copy from figma-react-orchestrator
  ├── Prohibition checklist (6 tests) ← EXACT COPY
  ├── Constraint validation (5 tests) ← EXACT COPY
  ├── Design boundary (4 tests) ← Copy pattern
  └── Retry logic (4 tests) ← EXACT COPY
```

**Time Savings**: 3-4 hours (copy/adapt vs. write from scratch)

**Action**: Reference TASK-002 test files as templates

---

### Improvement #7: Add Success Metrics from TASK-002

**TASK-004 Should Track**:
```yaml
Quality Metrics:
  architectural_review: "Reused approved architecture (82/100)"
  solid_compliance: ">88%"
  dry_compliance: ">95%"
  yagni_compliance: ">95%"
  pattern_alignment: ">95%"
  test_pass_rate: "100%"
  test_performance: "<1s"

Implementation Metrics:
  files_created: "~8 files"
  lines_of_code: "~3500 lines"
  total_tests: "~83 tests"
  actual_duration: "TBD (estimated 7-10 hours)"
  estimated_duration: "3-4 weeks"
  time_savings: "~90%"
```

**Action**: Add "Success Tracking" section to task

---

## Recommended Task Updates

### Update #1: File Structure Section

**Replace**:
```
.claude/
├── agents/
│   ├── design-system-orchestrator.md      [UPDATE - Add Zeplin routing]
│   └── zeppelin-design-specialist.md       [NEW]
```

**With**:
```
installer/global/agents/
├── figma-react-orchestrator.md         [EXISTING - don't modify]
└── zeplin-maui-orchestrator.md         [NEW - standalone]

.claude/stacks/maui/agents/
└── maui-ux-specialist.md               [NEW - parallel to react-component-generator]

installer/global/commands/
├── zeplin-to-maui.md                   [NEW - parallel to figma-to-react]
└── mcp-zeplin.md                       [NEW]
```

---

### Update #2: Estimated Effort

**Replace**:
```
**Estimated Effort**: 3-4 weeks (can run parallel to TASK-002 Week 2+)
```

**With**:
```
**Estimated Effort**: 7-10 hours (1-2 days)
**Based on TASK-002 Actuals**: 6 hours for Figma + React
**Adjustment**: +1-4 hours for new design system + mobile stack complexity
**Time Savings vs. Original Estimate**: ~90% (reusing patterns, test infrastructure, approved architecture)
```

---

### Update #3: Add Phase 0 to Acceptance Criteria

**Add Before Phase 1**:
```markdown
### Phase 0: MCP Verification (15 minutes)

- [ ] **Zeplin MCP Setup Verification**
  - [ ] Verify `@zeplin/mcp-server` npm package installed
  - [ ] Validate Zeplin Personal Access Token configured
  - [ ] Test MCP connection to Zeplin API
  - [ ] Verify all required MCP tools available:
    - [ ] `zeplin:get_project`
    - [ ] `zeplin:get_screen`
    - [ ] `zeplin:get_component`
    - [ ] `zeplin:get_styleguide`
    - [ ] `zeplin:get_colors`
    - [ ] `zeplin:get_text_styles`
  - [ ] Clear error messages if verification fails
  - [ ] Setup guide reference on failure

**Why**: TASK-002 showed Phase 0 MCP verification prevents 80% of failures
```

---

### Update #4: Visual Testing Strategy

**Replace**:
```
- [ ] **Visual Test Generation**
  - [ ] MAUI-specific visual testing strategy
  - [ ] Screenshot tests for each platform
  - [ ] >95% similarity threshold
```

**With**:
```
- [ ] **Visual Test Generation**
  - [ ] MAUI-specific testing approach:
    - [ ] Unit tests for XAML generation logic (Vitest)
    - [ ] Component validation tests (verify correct XAML structure)
    - [ ] Platform adaptation tests (iOS, Android, Windows, macOS)
    - [ ] Visual regression via screenshot comparison (manual validation)
  - [ ] XAML correctness: 100% (must match design specs exactly)
  - [ ] Platform-specific adaptations: Documented and validated
  - [ ] Clear error messages with remediation steps

**Note**: Unlike TASK-002 (Playwright for React web), MAUI requires platform-specific testing approaches. Focus on XAML generation correctness in automated tests.
```

---

### Update #5: Add Implementation Notes Section

**Add at end of task**:
```markdown
## Learnings from TASK-002 Applied

### Architecture Reuse
- ✅ Three-tier architecture validated (82/100 score)
- ✅ Saga pattern for workflow orchestration
- ✅ Facade pattern for MCP complexity hiding
- ✅ Retry pattern for error recovery
- ✅ No architectural review needed (reusing approved patterns)

### Time Savings Strategies
1. **Copy prohibition checklist logic** from TASK-002 (exact same 12 categories)
2. **Reuse test infrastructure** (Vitest, TypeScript configs already set up)
3. **Adapt test patterns** from figma-react-orchestrator tests (~70% reusable)
4. **Copy data contracts** (DesignElements, DesignConstraints with Zeplin-specific metadata)
5. **Reuse retry logic** (exponential backoff pattern identical)
6. **Copy constraint validation** (two-tier pattern + AST validation)

### File Naming Corrections
- ✅ Use `zeplin-maui-orchestrator.md` (not "zeppelin", not in wrong directory)
- ✅ Location: `installer/global/agents/` (parallel to figma-react-orchestrator)
- ✅ Stack-specific: `.claude/stacks/maui/agents/maui-ux-specialist.md`

### Quality Targets (from TASK-002)
- Architectural compliance: ≥88% (SOLID/DRY/YAGNI)
- Test pass rate: 100% (83+ tests)
- Test performance: <1 second
- Pattern alignment: ≥95%
- Code quality score: ≥85/100

### Expected Outcomes
- **Implementation time**: 7-10 hours (vs. 3-4 weeks estimated)
- **Time savings**: ~90% (reusing validated patterns)
- **Files created**: ~8 files (~3,500 lines)
- **Tests**: ~83 tests (100% passing)
- **Quality**: High (reusing approved architecture)
```

---

## Summary of Changes Needed

### Critical Changes (Must Fix Before Starting)
1. ✅ **Fix file naming**: `zeppelin` → `zeplin`, correct directory paths
2. ✅ **Remove orchestrator update**: Create standalone `zeplin-maui-orchestrator.md`
3. ✅ **Add Phase 0**: Zeplin MCP verification
4. ✅ **Update effort estimate**: 3-4 weeks → 7-10 hours (1-2 days)
5. ✅ **Clarify visual testing**: MAUI-specific approach (not Playwright)

### Recommended Changes (Should Apply)
6. ✅ **Add success metrics**: Track same quality gates as TASK-002
7. ✅ **Reference TASK-002 patterns**: Explicit reuse of prohibition checklist, retry logic, data contracts
8. ✅ **Update file structure**: Correct locations and naming
9. ✅ **Add learnings section**: Document what we're reusing from TASK-002

### Optional Enhancements (Nice to Have)
10. ⚪ Add TASK-002 test files as reference templates
11. ⚪ Document platform-specific MAUI testing tools
12. ⚪ Add comparison table (Figma vs. Zeplin patterns)

---

## Risk Assessment

### Risks Eliminated by TASK-002 Learnings
1. ✅ **Architectural uncertainty** - Architecture validated at 82/100
2. ✅ **Pattern selection** - Saga, Facade, Retry proven effective
3. ✅ **Test infrastructure** - Already configured and working
4. ✅ **Time estimation** - Realistic 7-10 hours vs. 3-4 weeks
5. ✅ **Data contract design** - Proven segregated interfaces

### Remaining Risks (Specific to Zeplin + MAUI)
1. **Zeplin MCP availability** - Mitigated by Phase 0 verification
2. **Platform-specific rendering** - Mitigated by clear adaptation guidelines
3. **MAUI XAML complexity** - Lower risk (simpler than React JSX)
4. **Visual testing cross-platform** - Mitigated by manual validation approach

---

## Final Recommendation

**Status**: ✅ **APPROVED WITH UPDATES**

**Action Items Before Starting TASK-004**:
1. Update file naming (`zeppelin` → `zeplin`, correct paths)
2. Change approach: Create standalone orchestrator (don't update existing)
3. Add Phase 0 MCP verification
4. Update effort estimate (3-4 weeks → 7-10 hours)
5. Clarify MAUI visual testing approach
6. Add "Learnings from TASK-002" section

**Expected Outcomes After Updates**:
- ✅ Implementation time: 7-10 hours (90% faster than estimated)
- ✅ Quality: High (reusing validated patterns)
- ✅ Risk: Low (architecture proven, patterns validated)
- ✅ Test coverage: 83+ tests (100% passing expected)
- ✅ No architectural review needed (reusing approved design)

**Estimated Time to Apply Updates**: 30-45 minutes

**Recommended Next Steps**:
1. Apply the 5 critical changes above (30-45 mins)
2. Review updated task with stakeholder
3. Begin implementation with `/task-work TASK-004`
4. Expected completion: Same day (7-10 hours total)

---

**Review Complete**: 2025-10-09
**Confidence Level**: High (based on TASK-002 actuals)
**Recommendation**: Proceed after applying critical updates
