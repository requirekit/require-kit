# Implementation Guide: FEAT-RK-001 RequireKit v2 Refinement Commands

## Execution Strategy

5 waves with parallel execution where safe. Waves 2 and 3 can run in parallel since they modify different files.

## Wave Breakdown

### Wave 1: Foundation (No Dependencies)

All three tasks can run in **parallel**.

| Task | Method | Files | Workspace |
|------|--------|-------|-----------|
| TASK-RK01-001: Agent refinement mode | task-work | requirements-analyst.md, requirements-analyst-ext.md | wave1-1 |
| TASK-RK01-002: Org pattern schema | task-work | epic-create.md | wave1-2 |
| TASK-RK01-003: Graphiti config | direct | installer/global/config/graphiti.yaml | wave1-3 |

**Key**: Establishes the completeness scoring model, organisation pattern schema, and Graphiti config that all subsequent waves depend on.

### Wave 2: New Commands (Depends on Wave 1)

All three tasks can run in **parallel** (different new files).

| Task | Method | Files | Workspace |
|------|--------|-------|-----------|
| TASK-RK01-004: /epic-refine | task-work | installer/global/commands/epic-refine.md | wave2-1 |
| TASK-RK01-005: /feature-refine | task-work | installer/global/commands/feature-refine.md | wave2-2 |
| TASK-RK01-006: /requirekit-sync | task-work | installer/global/commands/requirekit-sync.md | wave2-3 |

**Key**: Creates the three new command definition files. Most complex wave.

### Wave 3: Existing Command Updates (Depends on Wave 1)

Can run in **parallel with Wave 2** (different files). All four tasks within Wave 3 can also run in parallel.

| Task | Method | Files | Workspace |
|------|--------|-------|-----------|
| TASK-RK01-007: epic-status org patterns | task-work | epic-status.md | wave3-1 |
| TASK-RK01-008: hierarchy-view org patterns | task-work | hierarchy-view.md | wave3-2 |
| TASK-RK01-009: feature-create Graphiti | direct | feature-create.md | wave3-3 |
| TASK-RK01-010: overview instructions | direct | 00-overview.md | wave3-4 |

**Key**: Updates existing commands to support new patterns.

### Wave 4: Documentation (Depends on Waves 2 + 3)

Two tasks can run in **parallel** (different doc files).

| Task | Method | Files | Workspace |
|------|--------|-------|-----------|
| TASK-RK01-011: Docs site commands | task-work | docs/commands/{epics,features,index}.md, mkdocs.yml | wave4-1 |
| TASK-RK01-012: Hierarchy docs + CLAUDE.md | task-work | docs/core-concepts/hierarchy.md, CLAUDE.md | wave4-2 |

**Key**: Updates GitHub Pages site and project-level docs.

### Wave 5: Testing (Depends on All Previous)

Two tasks can run in **parallel** (different test types).

| Task | Method | Files | Workspace |
|------|--------|-------|-----------|
| TASK-RK01-013: Integration tests | task-work | tests/integration/*.py | wave5-1 |
| TASK-RK01-014: E2E tests | task-work | tests/e2e/*.py | wave5-2 |

**Key**: Validates all technology seams and full command pipelines.

## Dependency Graph

```
Wave 1 (Foundation):
  001 ─┐
  002 ─┤
  003 ─┘

Wave 2 (New Commands):       Wave 3 (Updates):
  004 ← 001, 002               007 ← 002
  005 ← 001                    008 ← 002
  006 ← 003                    009 ← 003
                                010 ← 001

Wave 4 (Documentation):
  011 ← 004, 005, 006, 007, 008
  012 ← 002, 007, 008

Wave 5 (Testing):
  013 ← 004, 005, 006, 007, 008, 009
  014 ← 004, 005, 006, 011, 012
```

## Technology Seams to Test

These seams are where errors most commonly occur:

1. **Markdown ↔ Frontmatter parsing** - YAML parse errors, field preservation
2. **Frontmatter ↔ Completeness scoring** - Missing fields, wrong weights
3. **Refinement ↔ Graphiti push** - Sync failures, schema mismatch
4. **Organisation pattern ↔ Display** - Wrong pattern rendering
5. **Cross-command ↔ Consistency** - Terminology alignment, calculation match
6. **Config ↔ Standalone mode** - Feature works without Graphiti

## Files Changed Summary

### New Files (5)
- `installer/global/commands/epic-refine.md`
- `installer/global/commands/feature-refine.md`
- `installer/global/commands/requirekit-sync.md`
- `installer/global/config/graphiti.yaml`
- `tests/` (integration + e2e test files)

### Modified Files (10)
- `installer/global/commands/epic-create.md`
- `installer/global/commands/feature-create.md`
- `installer/global/commands/epic-status.md`
- `installer/global/commands/hierarchy-view.md`
- `installer/global/agents/requirements-analyst.md`
- `installer/global/agents/requirements-analyst-ext.md`
- `installer/global/instructions/core/00-overview.md`
- `docs/commands/epics.md`
- `docs/commands/features.md`
- `docs/commands/index.md`
- `docs/core-concepts/hierarchy.md`
- `CLAUDE.md`

## Next Steps

1. Review this guide and the README.md
2. Start with Wave 1 tasks (all can run in parallel)
3. Use Conductor for parallel Wave 1 execution
4. After Wave 1 completes, start Waves 2 and 3 simultaneously
