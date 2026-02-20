---
id: TASK-DOC-002
title: Update require_kit_user_guide.md with FEAT-498F content
status: backlog
task_type: implementation
created: 2026-02-20T00:00:00Z
priority: high
complexity: 6
parent_review: TASK-REV-9480
feature_id: feat-498f-docs-update
wave: 1
implementation_mode: task-work
tags: [documentation, mkdocs, feat-498f]
---

# Task: Update require_kit_user_guide.md with FEAT-498F Content

## Description

Update `docs/guides/require_kit_user_guide.md` from v1.0.0 to v2.0.0 to include all FEAT-498F concepts and commands. This is the comprehensive user guide that explains RequireKit's philosophy, features, and workflows.

## Changes Required

### 1. Epic/Feature Hierarchy Section (lines 590-730)
Currently shows only Standard pattern (Epic -> Feature -> Requirement). Must be updated to cover:
- Three organisation patterns (Standard, Direct, Mixed)
- Pattern selection guidance (3-5 tasks = Direct, 6-7 = Either, 8+ = Standard)
- Pattern-specific examples
- When to migrate between patterns
- Reference to `/epic-refine` for pattern migration

### 2. New Section: Iterative Refinement
Add a new section after Epic/Feature Hierarchy covering:
- Why iterative refinement matters
- `/epic-refine` command overview with example session
- `/feature-refine` command overview with example session
- Completeness scoring explained:
  - 9-dimension model for epics (with weights table)
  - 7-dimension model for features (with weights table)
  - Score thresholds: 80% (good), 60% (needs work), 40% (incomplete)
- Three-phase flow (Current State -> Questions -> Change Summary)
- How refinement integrates with other commands

### 3. New Section: Knowledge Graph Integration (Graphiti)
Add a section covering:
- What Graphiti provides (queryable index of requirements)
- Standalone vs connected modes
- `/requirekit-sync` command overview
- Auto-sync on create/refine (when configured)
- Markdown-authoritative design principle

### 4. Command Reference Table (lines 733-765)
Add to Epic Commands table:
- `/epic-refine` | Iteratively refine epic | `/epic-refine EPIC-001`

Add to Feature Commands table:
- `/feature-refine` | Iteratively refine feature | `/feature-refine FEAT-001`

Add new Sync Commands table:
- `/requirekit-sync` | Sync to Graphiti | `/requirekit-sync --all`

Update `/epic-create` entry to show `--pattern` flag

### 5. Workflow Examples Section (lines 769-870)
Add new workflow example showing the refinement loop:
```
Example: Iterative Requirements Development
/gather-requirements -> /formalize-ears -> /epic-create -> /epic-refine (check score) ->
/feature-create -> /feature-refine (check score) -> /generate-bdd -> /hierarchy-view
```

### 6. Integration Section (lines 873-895)
- Mention Graphiti as an optional integration alongside guardkit
- Brief note about `/requirekit-sync` for knowledge graph population

### 7. Core Capabilities List (lines 30-36)
Add:
- **Iterative Refinement**: Completeness scoring with targeted improvement suggestions
- **Knowledge Graph**: Optional Graphiti integration for queryable requirements

### 8. Version Update
- Update version from 1.0.0 to 2.0.0
- Update last updated date

## Source Material

- `docs/commands/epics.md` lines 39-91 (epic-refine documentation)
- `docs/commands/features.md` lines 39-87 (feature-refine documentation)
- `docs/commands/sync.md` lines 1-77 (requirekit-sync documentation)
- `docs/core-concepts/hierarchy.md` (organisation patterns)

## Acceptance Criteria

- [ ] Organisation patterns section covers all 3 patterns with examples
- [ ] Refinement section explains both commands with completeness scoring
- [ ] Graphiti section explains standalone vs connected modes
- [ ] Command reference table includes all new commands
- [ ] At least one new workflow example showing refinement loop
- [ ] Version bumped to 2.0.0
- [ ] Content style consistent with existing guide
