# FEAT-RK-001: RequireKit v2 Refinement Commands

## Problem Statement

RequireKit's `/epic-create` and `/feature-create` are one-shot operations with no way to iterate. James (product owner) couldn't distinguish commands from conversation, and there was no guided refinement mode. Additionally, the rigid Epic → Feature → Task hierarchy forced artificial feature layers on small epics.

## Solution

Add iterative refinement commands (`/epic-refine`, `/feature-refine`), optional hierarchy flexibility, Graphiti knowledge graph integration, and completeness scoring. This makes RequireKit usable for product owners and enables the RequireKit → Graphiti → GuardKit pipeline.

## Feature Spec

See: `docs/research/refinement_commands/FEAT-RK-001-requirekit-v2-refinement-commands.md`

## Subtask Summary

| ID | Task | Wave | Complexity | Dependencies |
|----|------|------|------------|--------------|
| TASK-RK01-001 | Add refinement mode + completeness scoring to requirements-analyst agent | 1 | 7 | - |
| TASK-RK01-002 | Add organisation pattern schema to epic-create | 1 | 5 | - |
| TASK-RK01-003 | Create Graphiti configuration template | 1 | 3 | - |
| TASK-RK01-004 | Create /epic-refine command | 2 | 7 | 001, 002 |
| TASK-RK01-005 | Create /feature-refine command | 2 | 6 | 001 |
| TASK-RK01-006 | Create /requirekit-sync command | 2 | 5 | 003 |
| TASK-RK01-007 | Update epic-status for org patterns | 3 | 5 | 002 |
| TASK-RK01-008 | Update hierarchy-view for org patterns | 3 | 6 | 002 |
| TASK-RK01-009 | Update feature-create with Graphiti push | 3 | 3 | 003 |
| TASK-RK01-010 | Update overview instructions | 3 | 3 | 001 |
| TASK-RK01-011 | Update docs site command pages | 4 | 4 | 004-008 |
| TASK-RK01-012 | Update hierarchy docs + CLAUDE.md | 4 | 4 | 002, 007, 008 |
| TASK-RK01-013 | Integration tests (technology seams) | 5 | 7 | 004-009 |
| TASK-RK01-014 | E2E tests (command pipelines) | 5 | 6 | 004-006, 011-012 |

## Review Context

- **Review Task**: TASK-REV-RK01
- **Approach**: Wave-based implementation (5 waves)
- **Trade-off Priority**: Quality
- **Execution**: Maximize parallel (Waves 2-3 can overlap)
- **Testing**: Standard quality gates + dedicated Wave 5 test tasks
