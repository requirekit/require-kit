# Task State Storage

This directory stores task-specific state information including implementation plans, complexity evaluations, and design approval metadata.

## Purpose

The `docs/state/` directory provides persistent storage for:
- Implementation plans generated during design phases
- Complexity evaluation results
- Architectural review scores
- Design-first workflow metadata

## Directory Structure

```
docs/state/
├── README.md (this file)
├── TASK-001/
│   ├── implementation_plan.json
│   ├── complexity_score.json
│   └── architectural_review.json (optional)
├── TASK-002/
│   ├── implementation_plan.json
│   └── complexity_score.json
└── ...
```

## File Formats

### implementation_plan.json

Stores the structured implementation plan generated in Phase 2 and saved during design-first workflow.

**Created by**: Phase 2.7 (Complexity Evaluation & Plan Persistence)
**Used by**: --implement-only flag to load approved design

**Schema**:
```json
{
  "task_id": "TASK-006",
  "saved_at": "2025-10-11T14:30:00Z",
  "version": 1,
  "plan": {
    "files_to_create": [
      "installer/global/commands/lib/phase_execution.py",
      "installer/global/commands/lib/plan_persistence.py"
    ],
    "files_to_modify": [
      "installer/global/commands/task-work.md",
      "installer/global/agents/task-manager.md",
      "installer/global/commands/lib/flag_validator.py"
    ],
    "external_dependencies": [],
    "estimated_duration": "4-6 hours",
    "estimated_loc": 500,
    "phases": [
      "Phase 1: Create plan persistence module",
      "Phase 2: Create phase execution module",
      "Phase 3: Update task-work command spec",
      "Phase 4: Update agent documentation"
    ],
    "test_summary": "Unit tests for flag validation, plan persistence, and phase routing",
    "risks": [
      {
        "severity": "low",
        "description": "Backward compatibility with existing tasks",
        "mitigation": "No flags = existing behavior, new flags are additive"
      }
    ]
  },
  "architectural_review": {
    "overall_score": 85,
    "status": "approved_with_recommendations",
    "principles": {
      "solid": 88,
      "dry": 85,
      "yagni": 82
    },
    "recommendations": [
      "Consider extracting state transition logic into separate module in future",
      "Document plan storage location in README"
    ],
    "reviewed_at": "2025-10-11T14:25:00Z"
  }
}
```

### complexity_score.json (optional)

Stores detailed complexity evaluation results.

**Created by**: Phase 2.7 (Complexity Evaluation)
**Used by**: Phase 2.8 (Human Checkpoint) for review routing

**Schema**:
```json
{
  "task_id": "TASK-006",
  "calculated_at": "2025-10-11T14:20:00Z",
  "total_score": 7,
  "level": "complex",
  "review_mode": "FULL_REQUIRED",
  "factor_scores": {
    "file_complexity": {
      "score": 2.0,
      "max_score": 3,
      "justification": "5 files to create/modify"
    },
    "pattern_familiarity": {
      "score": 1.0,
      "max_score": 2,
      "justification": "Using familiar functional patterns"
    },
    "risk_level": {
      "score": 1.5,
      "max_score": 3,
      "justification": "Medium risk - workflow changes, backward compatibility"
    },
    "dependency_complexity": {
      "score": 0.0,
      "max_score": 2,
      "justification": "No new external dependencies"
    }
  },
  "forced_review_triggers": []
}
```

## Design-First Workflow Integration (TASK-006)

This directory is central to the design-first workflow introduced in TASK-006:

### --design-only Flag

When a task is run with `--design-only`:
1. Design phases execute (Phases 1-2.8)
2. Implementation plan is saved to `docs/state/{task_id}/implementation_plan.json`
3. Task moves to `design_approved` state
4. Workflow stops (does not proceed to implementation)

### --implement-only Flag

When a task is run with `--implement-only`:
1. System validates task is in `design_approved` state
2. Implementation plan is loaded from `docs/state/{task_id}/implementation_plan.json`
3. Implementation phases execute (Phases 3-5) using loaded plan
4. Design phases (1-2.8) are skipped

### State Lifecycle

```
1. Task created → BACKLOG
2. /task-work TASK-XXX --design-only → Saves to docs/state/TASK-XXX/ → DESIGN_APPROVED
3. /task-work TASK-XXX --implement-only → Loads from docs/state/TASK-XXX/ → IN_PROGRESS → IN_REVIEW
4. Task completed → State files remain for historical reference
```

## Persistence Guarantees

- **Atomic writes**: Plans are written atomically (no partial files)
- **Idempotent**: Running --design-only multiple times overwrites previous plan
- **Version tracking**: Each plan includes `version` field for future versioning support
- **Immutable after approval**: Once in design_approved state, plan should not be modified (re-run --design-only to revise)

## File Lifecycle

### Creation
- Created by `plan_persistence.save_plan()` in Phase 2.7
- Directory created automatically if doesn't exist
- JSON formatted with 2-space indentation

### Reading
- Loaded by `plan_persistence.load_plan()` in implement-only workflow
- Returns `None` if file doesn't exist
- Raises `PlanPersistenceError` if file exists but is corrupted

### Deletion
- Generally not deleted (kept for historical reference)
- Can be deleted manually if task is cancelled
- Use `plan_persistence.delete_plan()` for programmatic deletion

## Migration Guide

### Existing Tasks (Pre-TASK-006)

Existing tasks without design_approved state or saved plans:
- ✅ Can still use `/task-work TASK-XXX` (standard workflow)
- ✅ Not affected by new flags (backward compatible)
- ❌ Cannot use `--implement-only` (no saved plan)
- ✅ Can use `--design-only` to create plan retroactively

### New Tasks (Post-TASK-006)

New tasks created after TASK-006 implementation:
- ✅ Can use all three workflow modes
- ✅ Plans automatically saved when using --design-only
- ✅ Plans automatically loaded when using --implement-only

## Cleanup

State files are retained indefinitely for historical reference and audit trail. To clean up:

```bash
# Remove state for specific task
rm -rf docs/state/TASK-XXX/

# Remove state for all completed tasks (example)
for task in tasks/completed/*.md; do
    task_id=$(basename "$task" .md | cut -d'-' -f1-2)
    rm -rf "docs/state/$task_id/"
done
```

## Implementation Details

### Modules

- **plan_persistence.py**: Save/load/delete implementation plans
- **phase_execution.py**: Route to appropriate workflow based on flags
- **flag_validator.py**: Validate flag combinations and mutual exclusivity

### Integration Points

- **task-work.md**: Phase 2.9 (Workflow Routing) uses these modules
- **task-manager.md**: Phase 2.8 integration for design-first workflow
- **Phase 2.7**: Saves plans automatically during complexity evaluation

## Testing

Unit tests verify:
- Plan persistence (save/load/delete)
- Workflow routing based on flags
- State validation for implement-only
- Backward compatibility (no flags)

Integration tests verify:
- Complete design-only → implement-only sequence
- Error handling for missing/corrupted plans
- State transitions between workflow modes

## Troubleshooting

### Error: "Implementation plan not found"

**Cause**: Task is in design_approved state but plan file is missing.

**Solutions**:
1. Re-run design phase: `/task-work TASK-XXX --design-only`
2. Check if file was accidentally deleted
3. Verify docs/state/{task_id}/ directory exists

### Error: "Design metadata missing or invalid"

**Cause**: Task frontmatter doesn't have complete design section.

**Solutions**:
1. Re-run design phase: `/task-work TASK-XXX --design-only`
2. Manually add design section to task frontmatter
3. Move task back to backlog and re-run full workflow

### Plans not being saved

**Cause**: Permission issues or disk space.

**Solutions**:
1. Check directory permissions: `ls -la docs/state/`
2. Verify disk space: `df -h`
3. Check for write errors in logs

## Future Enhancements

Potential future enhancements (not in TASK-006 scope):

1. **Plan Versioning**: Track multiple versions of implementation plans
   - implementation_plan_v1.json, implementation_plan_v2.json
   - Compare versions to track design evolution

2. **Design Diff Tool**: Compare implementation to approved design
   - Highlight deviations from plan
   - Generate deviation report

3. **Automatic Cleanup**: Archive old state files
   - Move to docs/state/archive/ after task completion
   - Compress old plans

4. **Design Templates**: Pre-approved patterns
   - REST API template
   - Database migration template
   - Common workflow templates

## Related Documentation

- [/installer/global/commands/task-work.md](../../installer/global/commands/task-work.md) - Task work command spec
- [/installer/global/agents/task-manager.md](../../installer/global/agents/task-manager.md) - Task manager agent
- [/installer/global/commands/lib/plan_persistence.py](../../installer/global/commands/lib/plan_persistence.py) - Plan persistence module
- [/installer/global/commands/lib/phase_execution.py](../../installer/global/commands/lib/phase_execution.py) - Phase execution module
- [/tasks/in_progress/TASK-006-design-first-workflow-flags.md](../../tasks/in_progress/TASK-006-design-first-workflow-flags.md) - Original task specification

## Support

For issues or questions about task state storage:
1. Check this README for troubleshooting steps
2. Review TASK-006 specification for design rationale
3. Examine plan_persistence.py module for implementation details
4. Test with simple task first to verify setup

---

**Last Updated**: 2025-10-11 (TASK-006 implementation)
**Version**: 1.0
**Status**: Production-ready
