---
id: TASK-DOC-001
title: Update command_usage_guide.md with FEAT-498F commands
status: completed
task_type: implementation
created: 2026-02-20T00:00:00Z
completed: 2026-02-20T00:00:00Z
priority: high
complexity: 6
parent_review: TASK-REV-9480
feature_id: feat-498f-docs-update
wave: 1
implementation_mode: task-work
tags: [documentation, mkdocs, feat-498f]
completed_location: tasks/completed/TASK-DOC-001/
---

# Task: Update command_usage_guide.md with FEAT-498F Commands

## Description

Update `docs/guides/command_usage_guide.md` from v1.0.0 to v2.0.0 to include all FEAT-498F changes. This is the detailed command reference guide that users rely on for comprehensive command documentation.

## Changes Required

### 1. Quick Command Reference Table (lines 20-46)
Add to Epic Management Commands table:
- `/epic-refine` | Interactively refine epic | `/epic-refine EPIC-001`

Add to Feature Management Commands table:
- `/feature-refine` | Interactively refine feature | `/feature-refine FEAT-001`

Add new Sync Commands table:
- `/requirekit-sync` | Sync to Graphiti knowledge graph | `/requirekit-sync --all`

### 2. Epic Management Commands Section
- Update `/epic-create` (lines 248-299): Add `--pattern` flag documentation with examples for Standard, Direct, and Mixed patterns
- Update `/epic-status` (lines 301-354): Add organisation pattern awareness, completeness score display, and pattern-specific rendering to the output example
- Add new `/epic-refine` detailed section with:
  - Usage and examples
  - `--focus` and `--quick` flags
  - Three-phase flow explanation
  - 9-dimension completeness scoring table
  - Organisation pattern awareness
  - Example output

### 3. Feature Management Commands Section
- Add new `/feature-refine` detailed section with:
  - Usage and examples
  - `--focus` and `--quick` flags
  - Three-phase flow explanation
  - 7-dimension completeness scoring table
  - Cross-command integration (suggests /formalize-ears, /generate-bdd)
  - Example output

### 4. New Sync Commands Section
- Add `/requirekit-sync` detailed section with:
  - Usage and examples
  - `--all`, `--dry-run`, `--verbose` flags
  - Markdown-authoritative design explanation
  - When to use table
  - Error handling
  - Relationship to auto-sync commands

### 5. Hierarchy Commands Section (lines 629-704)
- Update `/hierarchy-view` with `--pattern` filter and `--graphiti-status` filter flags
- Add pattern-aware output examples

### 6. Complete Workflow Examples (lines 772-888)
- Add "Example: Iterative Refinement Workflow" showing refinement loop:
  - `/epic-create` -> `/epic-refine` -> assess completeness -> refine again -> `/feature-create` -> `/feature-refine`

### 7. Version Update
- Update version header from 1.0.0 to 2.0.0
- Update last updated date

## Source Material

Reference these already-updated command reference pages for content:
- `docs/commands/epics.md` (lines 39-91) - `/epic-refine` section
- `docs/commands/features.md` (lines 39-87) - `/feature-refine` section
- `docs/commands/sync.md` (lines 1-77) - `/requirekit-sync` section
- `docs/core-concepts/hierarchy.md` - Organisation patterns reference

## Acceptance Criteria

- [x] All 3 new commands documented with detailed sections
- [x] `/epic-create` updated with `--pattern` flag
- [x] `/epic-status` updated with pattern awareness and completeness scores
- [x] `/hierarchy-view` updated with new filter flags
- [x] Quick Command Reference table includes all new commands
- [x] At least one new workflow example demonstrating refinement loop
- [x] Version bumped to 2.0.0
- [x] Tone and style consistent with existing content
