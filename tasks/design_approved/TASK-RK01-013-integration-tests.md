---
complexity: 7
dependencies:
- TASK-RK01-004
- TASK-RK01-005
- TASK-RK01-006
- TASK-RK01-007
- TASK-RK01-008
- TASK-RK01-009
feature_id: FEAT-RK-001
id: TASK-RK01-013
implementation_mode: task-work
parent_review: TASK-REV-RK01
priority: high
status: design_approved
tags:
- testing
- integration
- refinement
- graphiti
- technology-seams
task_type: testing
title: Create integration tests for refinement flows and Graphiti sync
wave: 5
---

# Task: Create Integration Tests for Refinement Flows and Graphiti Sync

## Description

Create comprehensive integration tests covering the technology seams between refinement commands, markdown file handling, Graphiti sync, completeness scoring, and organisation patterns. This directly addresses the user's request to "reduce errors at technology seams."

## Files to Create

- `tests/integration/test_refinement_flows.py` - Refinement command flow tests
- `tests/integration/test_graphiti_sync.py` - Graphiti sync integration tests
- `tests/integration/test_org_patterns.py` - Organisation pattern tests
- `tests/integration/test_completeness_scoring.py` - Completeness scoring tests
- `tests/integration/conftest.py` - Shared fixtures and helpers

## Test Categories

### 1. Refinement Flow Integration (`test_refinement_flows.py`)

Tests that verify the complete refinement cycle works across command boundaries:

- **test_epic_refine_load_and_display**: Load epic markdown → parse frontmatter → calculate completeness → verify display format
- **test_epic_refine_update_in_place**: Load epic → apply changes → verify markdown updated correctly → verify existing fields preserved
- **test_epic_refine_refinement_history_append**: Refine epic → verify refinement_history added → refine again → verify history appended (not replaced)
- **test_feature_refine_cross_command_suggestions**: Load feature with missing BDD → verify /generate-bdd suggested
- **test_feature_refine_completeness_before_after**: Verify completeness score changes from answers reflect correctly
- **test_refine_with_focus_flag**: Verify --focus restricts questions to single category
- **test_refine_preserves_frontmatter**: Existing frontmatter fields (external_ids, export_config) preserved after refinement

### 2. Graphiti Sync Integration (`test_graphiti_sync.py`)

Tests that verify Graphiti sync works correctly and degrades gracefully:

- **test_sync_standalone_mode**: Graphiti disabled → refinement works → no sync attempted → markdown saved
- **test_sync_after_refinement**: Graphiti enabled → refine epic → verify episode pushed with correct metadata
- **test_sync_graceful_degradation**: Graphiti enabled but unavailable → refinement works → markdown saved → warning shown
- **test_sync_episode_schema_epic**: Verify epic episode matches schema from FEAT-RK-001 spec (group_id, metadata fields)
- **test_sync_episode_schema_feature**: Verify feature episode matches spec schema
- **test_requirekit_sync_recovery**: Manually edit markdown → run /requirekit-sync → verify Graphiti matches markdown
- **test_sync_upsert_dedup**: Push same epic twice → verify single episode (dedup by epic_id)
- **test_sync_group_id**: Verify group ID follows `{project}__requirements` convention

### 3. Organisation Pattern Integration (`test_org_patterns.py`)

Tests for cross-command consistency of organisation patterns:

- **test_epic_create_default_pattern**: Create epic without --pattern → verify default is "features"
- **test_epic_create_direct_pattern**: Create epic with --pattern direct → verify frontmatter
- **test_epic_status_direct_display**: Direct-pattern epic → verify task list shown (not features)
- **test_epic_status_mixed_warning**: Mixed-pattern epic → verify warning displayed
- **test_hierarchy_view_all_patterns**: Three epics (direct, features, mixed) → verify tree renders all correctly
- **test_validation_task_epic_xor_feature**: Task specifies both epic: and feature: → verify validation error
- **test_pattern_terminology_consistency**: Same terminology used across epic-create, epic-status, hierarchy-view
- **test_backward_compatibility**: Existing epic without organisation_pattern → verify treated as "features"

### 4. Completeness Scoring Integration (`test_completeness_scoring.py`)

Tests for scoring edge cases and accuracy:

- **test_epic_completeness_empty_epic**: Brand new epic → verify score reflects missing fields
- **test_epic_completeness_full_epic**: Fully specified epic → verify 100% or near-100%
- **test_epic_completeness_partial**: Partial epic → verify weights applied correctly
- **test_epic_weights_sum_to_100**: Verify 9 dimension weights sum to exactly 100%
- **test_feature_completeness_empty**: New feature → verify baseline score
- **test_feature_completeness_full**: Complete feature → verify 100% or near-100%
- **test_feature_weights_sum_to_100**: Verify 7 dimension weights sum to exactly 100%
- **test_score_after_refinement**: Score before → refine → score after → verify improvement
- **test_score_calculation_deterministic**: Same input → same score always

## Technology Seams Being Tested

| Seam | What Can Go Wrong | Tests Covering It |
|------|-------------------|-------------------|
| Markdown ↔ Frontmatter parsing | YAML parse errors, field loss | test_refine_preserves_frontmatter, test_epic_refine_update_in_place |
| Frontmatter ↔ Completeness scoring | Missing fields, wrong weights | test_completeness_* suite |
| Refinement ↔ Graphiti push | Sync failures, schema mismatch | test_sync_* suite |
| Organisation pattern ↔ Display | Wrong pattern rendering | test_org_patterns_* suite |
| Cross-command ↔ Consistency | Different terminology, calculations | test_pattern_terminology_consistency |
| Config ↔ Standalone mode | Feature fails without Graphiti | test_sync_standalone_mode |

## Acceptance Criteria

- [ ] All test files created with clear test names
- [ ] Technology seam tests cover all 6 identified seams
- [ ] Graphiti tests include both enabled and disabled modes
- [ ] Organisation pattern tests cover all three patterns
- [ ] Completeness scoring tests cover edge cases (empty, partial, full)
- [ ] Tests use fixtures for common setup (conftest.py)
- [ ] Tests are independent and can run in any order

## Test Requirements

- [ ] All tests pass
- [ ] Coverage of technology seam scenarios is comprehensive
- [ ] Tests document what they verify (clear docstrings)