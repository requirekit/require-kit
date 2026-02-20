---
id: TASK-DOC-006
title: Update cross-references and integration pages
status: backlog
task_type: implementation
created: 2026-02-20T00:00:00Z
priority: low
complexity: 4
parent_review: TASK-REV-9480
feature_id: feat-498f-docs-update
wave: 2
implementation_mode: task-work
dependencies: [TASK-DOC-001, TASK-DOC-002, TASK-DOC-003, TASK-DOC-004, TASK-DOC-005]
tags: [documentation, mkdocs, feat-498f]
---

# Task: Update Cross-References and Integration Pages

## Description

Update cross-references across existing pages to link to new FEAT-498F content, and add Graphiti integration section to the Integration Guide. This task should run after Tasks 1-5 to ensure cross-references point to updated content.

## Files to Update

### 1. `docs/index.md` (Home page)

**Typical Workflow** (lines 54-70): Add refinement step:
```bash
# 4.5. Refine iteratively
/epic-refine EPIC-001
/feature-refine FEAT-001
```

### 2. `docs/core-concepts/traceability.md`

**Traceability paths** (lines 12-23): Add organisation pattern variants:
- Forward traceability for Direct pattern (Epic -> REQ -> BDD -> Task)
- Mention that pattern choice affects traceability depth

**Commands section** (lines 112-123): Add `/requirekit-sync` as a tool for maintaining Graphiti-based traceability

### 3. `docs/integration/pm-tools.md`

Add cross-reference to pattern-specific PM mapping documented in `docs/core-concepts/hierarchy.md` (lines 79-115). Currently pm-tools.md doesn't mention that different organisation patterns map differently to PM tools.

### 4. `docs/INTEGRATION-GUIDE.md`

Add new section: "Graphiti Knowledge Graph Integration" covering:
- What Graphiti provides
- Configuration via `graphiti.yaml`
- `/requirekit-sync` for manual sync
- Auto-sync on create/refine when configured
- Standalone mode (default, no Graphiti required)
- Place this section after the guardkit integration content, before Troubleshooting

Update Common Workflows to include refinement commands in the full integration workflow example.

## Acceptance Criteria

- [ ] Home page workflow includes refinement step
- [ ] Traceability page covers pattern-specific traceability paths
- [ ] PM tools page cross-references pattern-specific mapping
- [ ] Integration Guide includes Graphiti section
- [ ] All cross-reference links resolve correctly
- [ ] No broken internal links introduced
