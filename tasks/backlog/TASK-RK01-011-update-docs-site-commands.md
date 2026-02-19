---
id: TASK-RK01-011
title: "Update documentation site command pages and navigation"
task_type: documentation
parent_review: TASK-REV-RK01
feature_id: FEAT-RK-001
wave: 4
implementation_mode: task-work
complexity: 4
dependencies: [TASK-RK01-004, TASK-RK01-005, TASK-RK01-006, TASK-RK01-007, TASK-RK01-008]
status: pending
priority: normal
tags: [documentation, mkdocs, github-pages, commands]
---

# Task: Update Documentation Site Command Pages and Navigation

## Description

Update the GitHub Pages/mkdocs documentation site with new refinement commands, updated epic/feature command docs, and navigation changes.

## Files to Modify

- `docs/commands/epics.md` - Add /epic-refine documentation
- `docs/commands/features.md` - Add /feature-refine documentation
- `docs/commands/index.md` - Add new commands to quick reference
- `mkdocs.yml` - Update navigation if needed (new pages)

## Changes Required

### docs/commands/epics.md
Add `/epic-refine` section with:
- Usage syntax and examples
- Description of three-phase flow
- `--focus` and `--quick` flags
- Organisation pattern awareness
- Completeness scoring explanation
- Link to detailed documentation

### docs/commands/features.md
Add `/feature-refine` section with:
- Usage syntax and examples
- Feature-specific question categories
- Cross-command integration (/formalize-ears, /generate-bdd)
- Completeness scoring for features
- Link to detailed documentation

### docs/commands/index.md
- Add `/epic-refine` to Epic Commands quick reference
- Add `/feature-refine` to Feature Commands quick reference
- Add `/requirekit-sync` to new "Sync Commands" section
- Update workflow examples to include refinement step

### mkdocs.yml
- Evaluate if new pages are needed or if existing pages suffice
- Add any new navigation entries under Commands Reference

## Acceptance Criteria

- [ ] /epic-refine documented in docs/commands/epics.md
- [ ] /feature-refine documented in docs/commands/features.md
- [ ] Both new commands in docs/commands/index.md quick reference
- [ ] /requirekit-sync documented
- [ ] Workflow examples updated with refinement step
- [ ] Navigation works correctly (no broken links)
- [ ] mkdocs builds without errors

## Test Requirements

- [ ] Verify mkdocs build succeeds: `mkdocs build --strict` (or non-strict for warnings)
- [ ] Verify no broken internal links
- [ ] Verify new pages accessible in navigation
