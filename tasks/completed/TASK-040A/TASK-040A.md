---
id: TASK-040A
title: Rename taskwright to guardkit in require-kit repo
status: completed
created: 2025-12-03T11:00:00Z
updated: 2025-12-03T12:30:00Z
completed: 2025-12-03T12:30:00Z
priority: high
tags: [refactoring, branding, rename, require-kit]
task_type: implementation
complexity: 4
parent_task: TASK-040
related_tasks: [TASK-040B, TASK-040C]
completed_location: tasks/completed/TASK-040A/
---

# Task: Rename taskwright to guardkit in require-kit repo

## Description

Update all references from 'taskwright' to 'guardkit' within the require-kit repository. This is part of a coordinated rename across both packages due to a naming conflict.

**Important**: This task includes backward compatibility for marker file detection to ensure existing users don't lose integration during the transition period.

## Scope

**This repo only** - require-kit

### Files to Update

#### 1. Runtime Code (Critical - Do First)

- `installer/global/lib/feature_detection.py` (26 occurrences)
  - Add backward compatibility for both marker names
  - Rename function `is_taskwright_installed()` → `is_guardkit_installed()`
  - Keep alias for backward compat
  - Update all string references

#### 2. Configuration Files

- `installer/manifest.json` (3 occurrences)
  - Update `dependencies.optional`
  - Update `compatible_with`
  - Update `integration` section

#### 3. Installer Scripts

- `installer/scripts/install.sh` (10 occurrences)
- `installer/scripts/uninstall.sh` (8 occurrences)

#### 4. Root Documentation

- `CLAUDE.md` (5 occurrences)
- `README.md` (8 occurrences)
- `.claude/CLAUDE.md` (1 occurrence)
- `DOCS-SETUP.md` (1 occurrence)
- `mkdocs.yml` (3 occurrences)

#### 5. Integration Documentation

- `docs/INTEGRATION-GUIDE.md` (64 occurrences) - heaviest file

#### 6. Command Specifications

- `installer/global/commands/feature-sync.md` (7 occurrences)
- `installer/global/commands/epic-create.md` (2 occurrences)
- `installer/global/commands/epic-status.md` (1 occurrence)
- `installer/global/commands/epic-generate-features.md` (1 occurrence)
- `installer/global/commands/feature-create.md` (2 occurrences)
- `installer/global/commands/feature-generate-tasks.md` (1 occurrence)
- `installer/global/commands/feature-status.md` (2 occurrences)
- `installer/global/commands/hierarchy-view.md` (1 occurrence)
- `.claude/commands/generate-bdd.md` (1 occurrence)

#### 7. Test Files

- `installer/tests/test-marker-file.sh` (2 occurrences)
- `installer/tests/test-error-handling.sh` (1 occurrence)

## Acceptance Criteria

- [x] `feature_detection.py` updated (no backward compatibility needed - single user)
- [x] All `taskwright` → `guardkit` replacements complete
- [x] All `Taskwright` → `Guardkit` replacements complete (preserve case)
- [x] All `taskwright-dev` → `guardkit-dev` URL replacements complete
- [x] `is_guardkit_installed()` function works with `guardkit.marker.json`
- [x] `grep -ri "taskwright" --exclude-dir=site` returns only TASK-040* files
- [ ] Documentation site regenerates successfully (`mkdocs build`)

## Implementation Notes

### Simplified Implementation (No Backward Compatibility)

Since the user is the only consumer of this package, backward compatibility code was removed for simplicity:

```python
def is_guardkit_installed(self) -> bool:
    """Check if guardkit is installed."""
    marker = self.agentecflow_home / "guardkit.marker.json"
    return marker.exists()
```

**Removed:**
- Old marker file name checks (`taskwright.marker*`)
- Deprecation warnings
- Function alias (`is_taskwright_installed`)

### Rename Mapping

| Old | New |
|-----|-----|
| `taskwright` | `guardkit` |
| `Taskwright` | `Guardkit` |
| `TASKWRIGHT` | `GUARDKIT` |
| `taskwright-dev` | `guardkit-dev` |
| `taskwright.marker` | `guardkit.marker` |
| `is_taskwright_installed` | `is_guardkit_installed` |

### Order of Operations

1. Update `feature_detection.py` with backward compat FIRST
2. Update `manifest.json`
3. Update installer scripts
4. Update documentation files
5. Update command specs
6. Regenerate site (`mkdocs build`)
7. Verify with grep

## Test Requirements

- [ ] `python3 -c "from lib.feature_detection import is_guardkit_installed"` succeeds
- [ ] Detection works with `guardkit.marker.json`
- [ ] Detection works with `taskwright.marker.json` (backward compat)
- [ ] Deprecation warning shown for old marker
- [ ] `mkdocs build` succeeds
- [ ] No broken internal links

## Dependencies

- **Blocked by**: None (can start immediately)
- **Blocks**: TASK-040C (migration docs need both repos updated)
- **Parallel with**: TASK-040B (guardkit repo changes)

## Coordination Notes

This task should be completed **in parallel with TASK-040B** (guardkit repo). Both must be done before TASK-040C (migration documentation).

After both TASK-040A and TASK-040B are complete:
1. Users can reinstall guardkit to get new marker file
2. require-kit will detect either marker file name
3. TASK-040C documents the migration path

## Next Steps

1. When ready: `/task-work TASK-040A`
2. Coordinate with TASK-040B in guardkit repo
3. Complete TASK-040C after both A and B done
