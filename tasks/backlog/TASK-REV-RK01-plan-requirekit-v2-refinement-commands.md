---
id: TASK-REV-RK01
title: "Plan: RequireKit v2 Refinement Commands"
status: review_complete
created: 2026-02-10T10:00:00Z
updated: 2026-02-10T10:00:00Z
priority: high
task_type: review
tags: [refinement, graphiti, epic-refine, feature-refine, requirekit-sync, optional-feature-layer, completeness-scoring]
complexity: 8
feature_spec: docs/research/refinement_commands/FEAT-RK-001-requirekit-v2-refinement-commands.md
clarification:
  context_a:
    timestamp: 2026-02-10T10:00:00Z
    decisions:
      focus: all
      tradeoff: quality
      graphiti_integration: include_now
      test_scope: full_coverage
---

# Plan: RequireKit v2 Refinement Commands

## Description

Feature planning review for FEAT-RK-001: Add iterative refinement commands (`/epic-refine`, `/feature-refine`), optional hierarchy flexibility (epic → task direct pattern), Graphiti integration for queryable requirements, completeness scoring, integration/E2E tests, and documentation updates for GitHub Pages/mkdocs.

## Feature Spec Reference

See: `docs/research/refinement_commands/FEAT-RK-001-requirekit-v2-refinement-commands.md`

## Scope

### New Commands
1. `/epic-refine` - Interactive epic refinement with completeness scoring
2. `/feature-refine` - Interactive feature refinement with acceptance criteria focus
3. `/requirekit-sync` - Graphiti sync/recovery command

### Modified Files
- `epic-create.md` - Add organisation_pattern, direct_tasks, Graphiti push
- `feature-create.md` - Add Graphiti push on create
- `epic-status.md` - Display direct tasks, handle all organisation patterns
- `hierarchy-view.md` - Render direct/mixed patterns
- `requirements-analyst.md` - Refinement mode, completeness scoring
- `requirements-analyst-ext.md` - Graphiti integration patterns
- `00-overview.md` - Document refinement workflow
- `CLAUDE.md` - Add refinement commands

### Documentation Updates
- `docs/commands/epics.md` - Document /epic-refine and organisation patterns
- `docs/commands/features.md` - Document /feature-refine
- `docs/core-concepts/hierarchy.md` - Optional feature layer patterns
- `docs/commands/index.md` - Add new commands to reference
- `mkdocs.yml` - Navigation updates if needed

### Testing
- Integration tests for refinement flows
- E2E tests for command pipelines
- Graphiti sync tests with graceful degradation
- Completeness scoring edge case tests

## Review Scope (from Context A)

- **Focus**: All aspects (comprehensive review)
- **Trade-off Priority**: Quality
- **Graphiti**: Include in first iteration
- **Test Coverage**: Full coverage at all technology seams

## Acceptance Criteria

- [ ] Review identifies technical options for implementing all 3 new commands
- [ ] Review assesses architecture for Graphiti integration (optional/standalone)
- [ ] Review proposes task breakdown with dependencies
- [ ] Review addresses integration testing strategy for technology seams
- [ ] Review considers UX design for product owners (James's problem)

## Implementation Notes

[To be populated by /task-review analysis]
