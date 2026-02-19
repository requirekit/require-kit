---
complexity: 6
dependencies:
- TASK-RK01-004
- TASK-RK01-005
- TASK-RK01-006
- TASK-RK01-011
- TASK-RK01-012
feature_id: FEAT-RK-001
id: TASK-RK01-014
implementation_mode: task-work
parent_review: TASK-REV-RK01
priority: high
status: design_approved
tags:
- testing
- e2e
- pipeline
- commands
task_type: testing
title: Create E2E tests for complete command pipelines
wave: 5
---

# Task: Create E2E Tests for Complete Command Pipelines

## Description

Create end-to-end tests that verify complete command pipelines work together, simulating real user workflows from epic creation through refinement to sync. These tests validate the full stack works as an integrated system.

## Files to Create

- `tests/e2e/test_epic_refinement_pipeline.py` - Full epic lifecycle E2E
- `tests/e2e/test_feature_refinement_pipeline.py` - Full feature lifecycle E2E
- `tests/e2e/test_hierarchy_with_patterns.py` - Multi-pattern hierarchy E2E
- `tests/e2e/test_docs_build.py` - Documentation site build verification
- `tests/e2e/conftest.py` - E2E fixtures (temp directories, sample data)

## Test Scenarios

### 1. Epic Refinement Pipeline (`test_epic_refinement_pipeline.py`)

Full lifecycle: create → refine → sync → status → refine again

- **test_epic_create_refine_sync_pipeline**:
  1. Create epic with `/epic-create "Test Epic"` → verify file created
  2. Verify initial completeness score (low)
  3. Run `/epic-refine EPIC-XXX` simulating answers for success criteria + risks
  4. Verify markdown updated in-place
  5. Verify refinement_history entry added
  6. Verify completeness score improved
  7. Run `/requirekit-sync EPIC-XXX` → verify Graphiti episode created (if enabled)
  8. Run `/epic-status EPIC-XXX` → verify all updated fields displayed

- **test_epic_create_direct_pattern_pipeline**:
  1. Create epic with `--pattern direct`
  2. Verify organisation_pattern = "direct" in frontmatter
  3. Run `/epic-status` → verify direct task display
  4. Run `/hierarchy-view` → verify tree rendering without features
  5. Run `/epic-refine` → verify organisation awareness (no "add features" suggestion for small epic)

- **test_epic_refine_multiple_sessions**:
  1. Create epic
  2. First refinement session (add success criteria)
  3. Second refinement session (add risks)
  4. Verify two refinement_history entries
  5. Verify cumulative completeness improvement
  6. Verify no data lost between sessions

### 2. Feature Refinement Pipeline (`test_feature_refinement_pipeline.py`)

Full lifecycle: create feature → refine → verify cross-command integration

- **test_feature_create_refine_pipeline**:
  1. Create epic, then feature linked to epic
  2. Verify initial feature completeness
  3. Run `/feature-refine FEAT-XXX` simulating acceptance criteria improvements
  4. Verify markdown updated
  5. Verify parent epic's hierarchy reflects changes
  6. Run `/hierarchy-view EPIC-XXX` → feature status shown correctly

- **test_feature_refine_bdd_integration**:
  1. Create feature with no BDD scenarios
  2. Run `/feature-refine FEAT-XXX --focus bdd`
  3. Verify system suggests `/generate-bdd`
  4. Verify BDD coverage dimension in completeness score

- **test_feature_refine_ears_integration**:
  1. Create feature with no EARS requirements
  2. Run `/feature-refine FEAT-XXX --focus acceptance`
  3. Verify system suggests `/formalize-ears`
  4. Verify requirements traceability dimension

### 3. Multi-Pattern Hierarchy E2E (`test_hierarchy_with_patterns.py`)

- **test_mixed_hierarchy_rendering**:
  1. Create 3 epics: one direct, one features, one mixed
  2. Run `/hierarchy-view` → verify all three patterns render
  3. Run `/epic-status` → verify each displays correctly
  4. Verify progress calculation works for all three

- **test_pattern_evolution**:
  1. Create direct-pattern epic with 3 tasks
  2. Add tasks until 8+
  3. Run `/epic-refine` → verify suggestion to add features
  4. Verify mixed pattern if feature added alongside direct tasks

### 4. Documentation Build E2E (`test_docs_build.py`)

- **test_mkdocs_build_succeeds**:
  1. Run `mkdocs build` → verify exit code 0
  2. Verify no critical errors in output
  3. Verify new command pages accessible

- **test_internal_links_valid**:
  1. Build docs
  2. Scan for internal links
  3. Verify all targets exist

- **test_new_pages_in_navigation**:
  1. Parse mkdocs.yml navigation
  2. Verify new commands appear in Commands Reference
  3. Verify hierarchy page reflects new patterns

## User Workflow Simulations

These E2E tests simulate James's (product owner) workflow:

1. **Happy Path**: Create epic → refine iteratively → get completeness to 80%+ → sync to Graphiti
2. **Quick Mode**: Create epic → `/epic-refine EPIC-XXX --quick` → verify AI suggestions applied
3. **Focus Mode**: Create epic → `/epic-refine EPIC-XXX --focus risks` → only risk questions asked
4. **Standalone Mode**: Create epic → refine → no Graphiti configured → everything works fine
5. **Recovery Mode**: Manual markdown edit → `/requirekit-sync` → Graphiti matches

## Acceptance Criteria

- [ ] Epic pipeline test covers create → refine → sync → status full cycle
- [ ] Feature pipeline test covers create → refine → cross-command suggestions
- [ ] Multi-pattern test verifies all three patterns in one hierarchy view
- [ ] Documentation build test verifies no broken links
- [ ] User workflow simulations cover James's use cases
- [ ] Tests use temporary directories (no side effects on real data)
- [ ] Tests document the user scenario they simulate

## Test Requirements

- [ ] All E2E tests pass
- [ ] Tests clean up temporary data
- [ ] Pipeline tests verify intermediate states (not just final state)
- [ ] Documentation build test actually runs mkdocs