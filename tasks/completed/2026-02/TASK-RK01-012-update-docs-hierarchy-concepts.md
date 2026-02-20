---
complexity: 4
dependencies:
- TASK-RK01-002
- TASK-RK01-007
- TASK-RK01-008
feature_id: FEAT-RK-001
id: TASK-RK01-012
implementation_mode: task-work
parent_review: TASK-REV-RK01
priority: normal
status: completed
tags:
- documentation
- hierarchy
- organisation-pattern
- core-concepts
task_type: documentation
title: Update hierarchy docs with optional feature layer patterns
wave: 4
---

# Task: Update Hierarchy Docs with Optional Feature Layer Patterns

## Description

Update the core concepts hierarchy documentation and CLAUDE.md files to reflect the optional feature layer, three organisation patterns, and refinement commands.

## Files to Modify

- `docs/core-concepts/hierarchy.md` - Major update with three patterns
- `CLAUDE.md` - Add refinement commands and org patterns to overview

## Changes Required

### docs/core-concepts/hierarchy.md

1. **Rewrite Hierarchy Structure** to show three patterns:
   - Standard: Epic → Feature → Task
   - Direct: Epic → Task (new)
   - Mixed: Epic → Feature + Task (new)

2. **Add Organisation Patterns Section**:
   - When to use each pattern
   - Visual diagrams for each
   - PM tool equivalents (Jira, Linear, GitHub mapping)
   - Migration between patterns

3. **Update Real-World Examples**:
   - Large epic with features pattern
   - Small epic with direct pattern
   - Mixed pattern with warning

4. **Update Traceability**:
   - Forward traceability for direct-pattern epics
   - Backward traceability for direct tasks

5. **Update Best Practices**:
   - Pattern selection guidance (direct: 3-5 tasks, features: 8+)
   - "Avoid mixed unless transitioning"
   - Refinement to improve hierarchy

6. **Update Commands Section**:
   - Add `/epic-refine` for changing patterns
   - Add `--pattern` flag examples

### CLAUDE.md (Root)

1. **Add to Essential Commands**:
   ```
   ### Requirements Refinement
   /epic-refine EPIC-XXX     # Iteratively improve epic
   /feature-refine FEAT-XXX  # Iteratively improve feature
   /requirekit-sync          # Sync to Graphiti knowledge graph
   ```

2. **Update Project Structure**:
   - Note that epics can use three organisation patterns

3. **Update Workflow Overview**:
   - Add refinement step between formalization and organization

## Acceptance Criteria

- [ ] hierarchy.md shows all three organisation patterns with diagrams
- [ ] PM tool mapping table for all patterns
- [ ] Traceability updated for direct-pattern epics
- [ ] Best practices include pattern selection guidance
- [ ] CLAUDE.md includes refinement commands
- [ ] CLAUDE.md workflow updated with refinement step

## Test Requirements

- [ ] Verify mkdocs build succeeds
- [ ] Verify hierarchy.md renders correctly
- [ ] Verify no broken links in updated pages