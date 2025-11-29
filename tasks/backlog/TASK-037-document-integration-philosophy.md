---
id: TASK-037
title: Document and Validate Bidirectional Optional Integration Philosophy
status: backlog
created: 2025-11-29T17:00:00Z
updated: 2025-11-29T17:00:00Z
priority: medium
tags: [documentation, architecture, integration, philosophy]
complexity: 4
related_to: TASK-035
parent_review: TASK-035
estimated_effort: 1 day
test_results:
  status: pending
  coverage: null
  last_run: null
---

# Task: Document and Validate Bidirectional Optional Integration Philosophy

## Context

This task implements the **Integration Philosophy Recommendation** from [TASK-035 Review](file:///Users/richardwoollcott/Projects/appmilla_github/require-kit/.claude/reviews/TASK-035-review-report.md):

**Decision**: **Maintain Bidirectional Optional Integration** (Current Architecture)

**Key Findings from Review**:
- ✅ Architecture is sound (348 lines of docs, 320 lines of implementation)
- ✅ BDD mode is exception, not pattern (feature-specific requirement)
- ✅ Real users have distinct needs (30% taskwright-only, 20% require-kit-only, 50% both)
- ✅ Prevents lock-in and enables future extensibility

## Objectives

1. ✅ Validate current integration architecture is correctly implemented
2. ✅ Document BDD mode precedent as feature-specific exception
3. ✅ Create clear guidelines for when feature-specific guards are justified
4. ✅ Ensure graceful degradation is consistent across commands
5. ✅ Update documentation to reinforce bidirectional optional model

## Acceptance Criteria

### 1. Architecture Validation (0.5 day)

- [ ] **1.1**: Audit all require-kit commands for proper feature detection
  - Commands that should work standalone: `/gather-requirements`, `/formalize-ears`, `/generate-bdd`, `/epic-create`, `/feature-create`
  - Commands that may warn about taskwright: `/feature-generate-tasks` (can create specs without execution)
  - Verify graceful degradation (warnings, not errors)

- [ ] **1.2**: Verify marker file implementation
  - Check `.requirekit-marker` creation during installation
  - Check `feature_detection.py` is shared and in sync with taskwright
  - Validate `supports_*()` functions work correctly

- [ ] **1.3**: Test standalone functionality
  - Install require-kit WITHOUT taskwright
  - Verify all core commands work (gather, formalize, BDD, epic, feature)
  - Verify warnings are informational, not blocking

### 2. BDD Mode Precedent Documentation (0.25 day)

- [ ] **2.1**: Create ADR (Architecture Decision Record)
  - File: `docs/adr/ADR-002-bdd-mode-requires-requirekit.md`
  - Document why BDD mode in taskwright requires require-kit
  - Explain this is feature-specific, not architectural precedent
  - Clarify other modes (standard, tdd) remain standalone

- [ ] **2.2**: Update integration guide
  - Add section: "Feature-Specific Requirements vs Hard Dependencies"
  - Document BDD mode as justified exception
  - Provide decision criteria for future feature-specific guards

### 3. Feature-Specific Guard Guidelines (0.25 day)

- [ ] **3.1**: Create guidelines document
  - File: `docs/architecture/feature-specific-guards.md`
  - Define when feature-specific guards are justified
  - Provide decision tree for adding new guards
  - Examples: Justified (BDD mode) vs Not Justified (general task execution)

- [ ] **3.2**: Decision criteria for future guards
  ```markdown
  ## When Feature-Specific Guards Are Justified

  ✅ **Justified** if:
  - Feature is conceptually dependent (BDD requires requirements)
  - Functionality is impossible without the other package
  - Other package provides core methodology (not just data)
  - Clear error message guides user to install missing package
  - Other modes/commands remain functional without guard

  ❌ **Not Justified** if:
  - Convenience/preference rather than requirement
  - Workaround exists without other package
  - Would create hard dependency for entire package
  - Reduces user flexibility unnecessarily
  ```

### 4. Documentation Updates (0.5 day)

- [ ] **4.1**: Update `CLAUDE.md`
  - Reinforce "No Required Dependencies" principle
  - Document BDD mode as feature-specific exception
  - Add reference to feature-specific guard guidelines

- [ ] **4.2**: Update `docs/INTEGRATION-GUIDE.md`
  - Add "Philosophy: Why Both Packages Are Optional" section
  - Document user personas (solo dev, requirements analyst, enterprise)
  - Show usage statistics (30% / 20% / 50% distribution)

- [ ] **4.3**: Update `README.md`
  - Emphasize standalone capability upfront
  - Add "Works standalone or with taskwright" badge
  - Link to integration guide for full workflow

- [ ] **4.4**: Update `installer/README-REQUIRE-KIT.md`
  - Clarify optional taskwright integration
  - Add "What you get standalone" section
  - Add "What you get with taskwright" section

### 5. Validation Testing (0.5 day)

- [ ] **5.1**: Standalone installation test
  - Fresh environment (no taskwright)
  - Install require-kit only
  - Verify core workflow: gather → formalize → BDD → epic → feature
  - Verify no errors (only informational warnings if any)

- [ ] **5.2**: Integration installation test
  - Fresh environment
  - Install both packages
  - Verify enhanced features work
  - Verify feature detection works correctly

- [ ] **5.3**: Graceful degradation test
  - Install require-kit first
  - Run commands (should work)
  - Install taskwright
  - Verify enhanced features now available
  - Uninstall taskwright
  - Verify require-kit still works

## Recommendations to Document

### DO (from review)

- ✅ Keep marker file detection
- ✅ Maintain graceful degradation
- ✅ Continue documenting integration benefits
- ✅ Add more feature-specific guards where justified (like BDD mode)

### DO NOT (from review)

- ❌ Make require-kit require taskwright
- ❌ Make taskwright require require-kit
- ❌ Merge into single package
- ❌ Use BDD mode guard as justification for hard dependencies

## Files to Update

1. `docs/adr/ADR-002-bdd-mode-requires-requirekit.md` (NEW)
2. `docs/architecture/feature-specific-guards.md` (NEW)
3. `CLAUDE.md` (UPDATE)
4. `docs/INTEGRATION-GUIDE.md` (UPDATE)
5. `README.md` (UPDATE)
6. `installer/README-REQUIRE-KIT.md` (UPDATE)

## Success Criteria

This task is complete when:

1. ✅ All require-kit commands work standalone (verified by testing)
2. ✅ BDD mode precedent documented as feature-specific exception
3. ✅ Feature-specific guard guidelines created
4. ✅ Documentation reinforces bidirectional optional model
5. ✅ User personas documented with usage statistics
6. ✅ Graceful degradation tested and validated
7. ✅ README emphasizes standalone capability
8. ✅ Integration guide updated with philosophy section

## Dependencies

- TASK-035 architectural review (decision rationale)
- Existing `feature_detection.py` implementation
- Existing `docs/architecture/bidirectional-integration.md`

## Estimated Timeline

- **Architecture Validation**: 0.5 day
- **BDD Precedent Documentation**: 0.25 day
- **Guard Guidelines**: 0.25 day
- **Documentation Updates**: 0.5 day
- **Validation Testing**: 0.5 day
- **Total**: ~1 day

**Priority**: Medium (reinforces current architecture, prevents drift)
**Complexity**: 4/10 (mostly documentation and validation)

## References

- [TASK-035 Review Report](file:///Users/richardwoollcott/Projects/appmilla_github/require-kit/.claude/reviews/TASK-035-review-report.md)
- [Bidirectional Integration Architecture](file:///Users/richardwoollcott/Projects/appmilla_github/require-kit/docs/architecture/bidirectional-integration.md)
- [feature_detection.py](file:///Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/global/lib/feature_detection.py)
- [taskwright BDD mode guards](file:///Users/richardwoollcott/Projects/appmilla_github/taskwright/installer/global/commands/task-work.md)

## Notes

This task ensures the architectural decision from TASK-035 is properly documented and enforced, preventing future architectural drift toward hard dependencies.
