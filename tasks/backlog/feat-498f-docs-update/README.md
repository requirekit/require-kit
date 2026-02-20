# FEAT-498F Documentation Update

## Problem Statement

FEAT-498F "RequireKit v2 Refinement Commands" was successfully merged (14/14 tasks, all approved in 1 turn). While the AutoBuild process updated core command reference pages well, the user-facing guides (`require_kit_user_guide.md`, `command_usage_guide.md`), getting-started pages, and cross-references were not updated.

**Review Score**: 68/100 - Good coverage of command reference pages, significant gaps in user guides.

## Solution Approach

Extend existing documentation pages (no new pages needed) to cover:
- 3 new commands: `/epic-refine`, `/feature-refine`, `/requirekit-sync`
- New concepts: Organisation patterns, completeness scoring, Graphiti integration
- Updates to existing commands: `/epic-create --pattern`, `/epic-status`, `/hierarchy-view`

## Subtask Summary

| Task | Description | Priority | Effort | Wave |
|---|---|---|---|---|
| TASK-DOC-001 | Update command_usage_guide.md | High | Large | 1 |
| TASK-DOC-002 | Update require_kit_user_guide.md | High | Large | 1 |
| TASK-DOC-003 | Update Getting Started pages (3 files) | Medium | Medium | 1 |
| TASK-DOC-004 | Update commands/hierarchy.md | Medium | Small | 1 |
| TASK-DOC-005 | Update commands/epics.md /epic-create | Medium | Small | 1 |
| TASK-DOC-006 | Update cross-references (4 files) | Low | Medium | 2 |

**Total**: 6 tasks, 11 files modified, 0 new files

## Parent Review

- **Review**: [TASK-REV-9480](./../TASK-REV-9480-review-feat-498f-docs-update.md)
- **Report**: [Review Report](../../../.claude/reviews/TASK-REV-9480-review-report.md)
