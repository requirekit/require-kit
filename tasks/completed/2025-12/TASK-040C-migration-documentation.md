---
id: TASK-040C
title: Create taskwright to guardkit migration documentation
status: completed
completed: 2025-12-03T12:00:00Z
completion_note: Not needed - rename completed without migration docs required
created: 2025-12-03T11:00:00Z
updated: 2025-12-03T11:00:00Z
priority: medium
tags: [documentation, migration, branding]
task_type: documentation
complexity: 2
parent_task: TASK-040
related_tasks: [TASK-040A, TASK-040B]
blocked_by: [TASK-040A, TASK-040B]
---

# Task: Create taskwright to guardkit migration documentation

## Description

Create migration documentation to help existing users transition from taskwright to guardkit. This includes updating the INTEGRATION-GUIDE.md migration section and creating any necessary announcements.

**Blocked by**: TASK-040A and TASK-040B must complete first.

## Scope

### New Documentation to Create

1. **Migration section in INTEGRATION-GUIDE.md**
   - Add "From taskwright to guardkit" migration guide
   - Document marker file transition
   - Provide step-by-step upgrade instructions

2. **CHANGELOG entry**
   - Document the rename
   - Note backward compatibility period
   - List breaking changes (if any)

### Content to Include

#### Migration Guide Content

```markdown
### From taskwright to guardkit

**Context**: The taskwright package has been renamed to guardkit due to a naming conflict.

**What Changed**:
- Package name: taskwright → guardkit
- Marker file: taskwright.marker.json → guardkit.marker.json
- GitHub org: taskwright-dev → guardkit-dev (if applicable)

**Migration Steps**:

1. **Uninstall old taskwright**:
   ```bash
   cd /path/to/taskwright
   ./installer/scripts/uninstall.sh
   ```

2. **Clone and install guardkit**:
   ```bash
   git clone https://github.com/guardkit-dev/guardkit.git
   cd guardkit
   ./installer/scripts/install.sh
   ```

3. **Verify installation**:
   ```bash
   ls ~/.agentecflow/guardkit.marker.json
   # Should exist
   ```

**Backward Compatibility**:
- require-kit v1.x will detect BOTH taskwright.marker and guardkit.marker
- Deprecation warnings shown for old marker file
- Full compatibility removed in require-kit v2.0

**No Data Migration Required**:
- Task files remain unchanged
- Configuration files remain unchanged
- Only the package name and marker file change
```

## Acceptance Criteria

- [ ] Migration guide added to INTEGRATION-GUIDE.md
- [ ] CHANGELOG.md updated with rename entry
- [ ] Clear step-by-step migration instructions
- [ ] Backward compatibility period documented
- [ ] Breaking changes clearly listed

## Dependencies

- **Blocked by**: TASK-040A, TASK-040B (need final URLs and details)
- **Blocks**: None (final task in sequence)

## Verification

- [ ] Migration guide is accurate and tested
- [ ] Links to guardkit repo work
- [ ] Instructions are complete and clear

## Next Steps

1. Wait for TASK-040A and TASK-040B to complete
2. Gather final details (URLs, version numbers)
3. Write migration documentation
4. Update CHANGELOG
5. Mark TASK-040 parent as complete
