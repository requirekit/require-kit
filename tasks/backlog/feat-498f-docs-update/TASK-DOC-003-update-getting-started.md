---
id: TASK-DOC-003
title: Update Getting Started pages with refinement workflow
status: backlog
task_type: implementation
created: 2026-02-20T00:00:00Z
priority: medium
complexity: 4
parent_review: TASK-REV-9480
feature_id: feat-498f-docs-update
wave: 1
implementation_mode: task-work
tags: [documentation, mkdocs, feat-498f]
---

# Task: Update Getting Started Pages with Refinement Workflow

## Description

Update the 3 Getting Started pages to mention the iterative refinement workflow introduced by FEAT-498F. These pages are the entry point for new users and should introduce refinement as a natural step.

## Files to Update

### 1. `docs/getting-started/quickstart.md`

**Workflow diagram** (lines 100-130): Add step between "4. ORGANIZE Hierarchy" and "5. EXPORT Integration":
```
4.5. REFINE      Iterative improvement
     Hierarchy   /epic-refine, /feature-refine
```

**"Organizing with Epics and Features" section** (lines 142-155): Add after `/hierarchy-view`:
```bash
# Iteratively improve your epic
/epic-refine EPIC-001
# Check completeness score, answer targeted questions
```

### 2. `docs/getting-started/first-requirements.md`

**Add Step 7: Refine and Iterate** after Step 6 (Organize into Hierarchy, line 159):
- Show `/epic-refine EPIC-001` with brief explanation of completeness scoring
- Show `/feature-refine FEAT-001` as natural follow-up
- Mention that refinement improves quality iteratively
- Keep it brief (10-15 lines) to maintain progressive disclosure

### 3. `docs/getting-started/index.md`

**Core Workflow listing** (lines 30-38): Add after step 5 (Create Feature):
```
5.5. Refine Epic/Feature         -> /epic-refine, /feature-refine
```

**Learning Path > Intermediate** (lines 53-56): Add:
- Learn [Iterative Refinement](../commands/epics.md#epic-refine) - or appropriate link

## Acceptance Criteria

- [ ] Quickstart workflow diagram includes refinement step
- [ ] First requirements page includes Step 7 for refinement
- [ ] Getting started index includes refinement in core workflow and learning path
- [ ] Content is brief and maintains progressive disclosure (not overwhelming for beginners)
- [ ] Links to detailed refinement documentation work correctly
