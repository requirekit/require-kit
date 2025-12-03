---
id: TASK-036
title: Harmonize ID Generation - Adopt Hash-Based IDs with Metadata Hierarchy
status: backlog
created: 2025-11-29T16:50:00Z
updated: 2025-11-29T16:50:00Z
priority: high
tags: [architecture, migration, id-generation, integration]
complexity: 7
related_to: TASK-035
parent_review: TASK-035
estimated_effort: 3-4 days
test_results:
  status: pending
  coverage: null
  last_run: null
---

# Task: Harmonize ID Generation - Adopt Hash-Based IDs with Metadata Hierarchy

## Context

This task implements the architectural decision from [TASK-035 Review](file:///Users/richardwoollcott/Projects/appmilla_github/require-kit/.claude/reviews/TASK-035-review-report.md) to harmonize task ID generation between require-kit and taskwright.

**Decision**: Adopt **Option D - Hash-Based IDs with Metadata Hierarchy**

**Rationale**:
- Collision-free IDs (SHA-256 hashing)
- Production-proven implementation (taskwright's 703 tasks)
- Hierarchy preserved in metadata
- Single source of truth (DRY compliance)
- Low migration effort (250 tasks vs taskwright's 703 already migrated)

## Objectives

1. ✅ Adopt taskwright's `id_generator.py` for collision-free ID generation
2. ✅ Preserve epic/feature hierarchy in task metadata
3. ✅ Migrate existing 250 tasks with zero data loss
4. ✅ Update commands to use new ID format
5. ✅ Maintain backward compatibility with legacy IDs

## Target ID Format

**Before**:
```
ID: TASK-035 (simple sequential)
Format: TASK-{seq}
Hierarchy: Not embedded in ID
```

**After**:
```
ID: TASK-A3F2 (hash-based)
Format: TASK-{hash} or TASK-{prefix}-{hash}
Hierarchy: Stored in frontmatter metadata
```

**Example Task Frontmatter**:
```yaml
---
id: TASK-A3F2
title: Implement login form validation
epic: EPIC-001
feature: FEAT-001.2
epic_title: User Authentication
feature_title: Login Page
hierarchy_path: "EPIC-001 > FEAT-001.2 > TASK-A3F2"
legacy_id: TASK-035  # Preserved for backward compatibility
---
```

## Acceptance Criteria

### Phase 1: ID Generation Implementation (2-3 days)

- [ ] **1.1**: Copy `id_generator.py` from taskwright to require-kit
  - Source: `taskwright/installer/global/lib/id_generator.py`
  - Destination: `require-kit/installer/global/lib/id_generator.py`
  - Mark as shared file (keep in sync with taskwright)
  - Verify all 16 public functions copied

- [ ] **1.2**: Create Python wrapper for `/feature-generate-tasks`
  - Replace bash shell ID logic (lines 42-97)
  - Use `generate_task_id(prefix=infer_prefix(epic=epic_id))`
  - Add epic/feature metadata to generated tasks
  - Preserve backward compatibility for manual invocation

- [ ] **1.3**: Update `/task-create` command (if exists in require-kit)
  - Use `id_generator.generate_task_id()`
  - Add epic/feature metadata fields
  - Enable prefix inference from epic/tags/title
  - Validate generated IDs before file creation

- [ ] **1.4**: Create migration script: `migrate_to_hash_ids.py`
  - Pre-migration backup to `.claude/state/backup/tasks-pre-hash-migration-{timestamp}/`
  - Scan all 250 tasks in tasks/ directories
  - Generate new hash-based ID for each task
  - Preserve original ID in `legacy_id` frontmatter field
  - Add `epic`, `feature`, `hierarchy_path` metadata where determinable
  - Rename files: `TASK-035-title.md` → `TASK-A3F2-title.md`
  - Update cross-references in other tasks
  - Validation: Ensure all tasks migrated without data loss

- [ ] **1.5**: Execute migration
  - Run migration script on all task directories
  - Verify backup created successfully
  - Validate zero data loss (250 tasks in, 250 tasks out)
  - Check all frontmatter fields preserved
  - Verify cross-references updated

### Phase 2: Command Updates (1 day)

- [ ] **2.1**: Update `/epic-status` command
  - Query by `epic` frontmatter field instead of parsing ID
  - Display hierarchy with new hash-based IDs
  - Show legacy IDs for reference

- [ ] **2.2**: Update `/feature-status` command
  - Query by `feature` frontmatter field
  - Display feature hierarchy
  - Group tasks by feature

- [ ] **2.3**: Update `/hierarchy-view` command
  - Build hierarchy from metadata (`epic`, `feature` fields)
  - Display `hierarchy_path` for each task
  - Show both new and legacy IDs

- [ ] **2.4**: Update `/task-status` command
  - Display hierarchy context from metadata
  - Show epic and feature relationships
  - Include legacy ID if present

### Phase 3: Documentation (1 day)

- [ ] **3.1**: Update `/feature-generate-tasks` documentation
  - Document new hash-based ID format
  - Explain metadata hierarchy approach
  - Provide migration examples
  - Update code examples

- [ ] **3.2**: Create migration guide
  - File: `docs/guides/hash-id-migration-guide.md`
  - Explain rationale (link to TASK-035 review)
  - Provide before/after examples
  - Document backward compatibility
  - FAQ section

- [ ] **3.3**: Update integration guide
  - Update `docs/INTEGRATION-GUIDE.md`
  - Document ID format alignment with taskwright
  - Explain metadata-based hierarchy
  - Show integration workflow examples

- [ ] **3.4**: Update CLAUDE.md
  - Update project instructions
  - Document new ID format
  - Reference migration guide

## Test Requirements

### Unit Tests
- [ ] Test `id_generator.py` functions (copy tests from taskwright)
- [ ] Test migration script on sample tasks
- [ ] Test prefix inference from epic/tags/title
- [ ] Test collision detection and resolution

### Integration Tests
- [ ] Test `/feature-generate-tasks` with new IDs
- [ ] Test epic/feature queries with metadata
- [ ] Test hierarchy view with hash-based IDs
- [ ] Test backward compatibility (legacy IDs still readable)

### Migration Validation
- [ ] Backup directory created successfully
- [ ] All 250 tasks migrated
- [ ] No data loss (frontmatter preserved)
- [ ] Cross-references updated
- [ ] Legacy IDs preserved
- [ ] New IDs are unique (no collisions)

## Implementation Notes

### Code Reuse from taskwright

Leverage taskwright's proven migration experience:

1. **Migration Script Pattern**:
   ```python
   # From taskwright's successful migration (Nov 2025)
   from installer.global.lib.id_generator import generate_task_id, check_duplicate
   from pathlib import Path
   import shutil
   import yaml

   def migrate_task(task_file: Path) -> None:
       # 1. Backup
       backup_dir = Path(f".claude/state/backup/tasks-pre-hash-migration-{timestamp}")
       shutil.copy(task_file, backup_dir)

       # 2. Read frontmatter
       content = task_file.read_text()
       # ... parse YAML frontmatter

       # 3. Generate new ID
       new_id = generate_task_id(prefix=infer_from_metadata(frontmatter))

       # 4. Update frontmatter
       frontmatter['legacy_id'] = frontmatter['id']
       frontmatter['id'] = new_id

       # 5. Write back
       task_file.write_text(updated_content)

       # 6. Rename file
       new_path = task_file.parent / f"{new_id}-{title}.md"
       task_file.rename(new_path)
   ```

2. **Prefix Inference Logic**:
   ```python
   from installer.global.lib.id_generator import infer_prefix

   # Priority: epic > tags > title > None
   prefix = infer_prefix(
       epic=frontmatter.get('epic'),
       tags=frontmatter.get('tags', []),
       title=frontmatter.get('title')
   )
   # Returns: "E01" (from EPIC-001), "DOC" (from docs tag), etc.
   ```

3. **Metadata Enhancement**:
   ```python
   # Add hierarchy context to each task
   if 'epic' in frontmatter and 'feature' in frontmatter:
       epic_title = get_epic_title(frontmatter['epic'])
       feature_title = get_feature_title(frontmatter['feature'])
       frontmatter['hierarchy_path'] = (
           f"{frontmatter['epic']} > {frontmatter['feature']} > {new_id}"
       )
       frontmatter['epic_title'] = epic_title
       frontmatter['feature_title'] = feature_title
   ```

### Backward Compatibility Strategy

1. **Legacy ID Preservation**:
   - All tasks keep `legacy_id` field
   - Command parsers accept both formats
   - Search supports both ID formats

2. **Graceful Degradation**:
   - Commands work if hierarchy metadata missing
   - Fallback to filename parsing if needed
   - Clear error messages for missing metadata

3. **Cross-Reference Updates**:
   - Scan all markdown files for task references
   - Update `related_to:`, `parent:`, `blocks:` fields
   - Update links in documentation

### Risk Mitigation

**Risk 1: Migration Failure**
- Mitigation: Pre-migration backup, rollback script
- Validation: Checksum verification before/after

**Risk 2: Cross-Reference Breakage**
- Mitigation: Automated cross-reference scanner and updater
- Validation: Test all task relationships post-migration

**Risk 3: User Confusion**
- Mitigation: Clear migration guide, FAQ
- Communication: GitHub announcement, changelog

## Success Criteria

This task is complete when:

1. ✅ All 250 tasks migrated to hash-based IDs
2. ✅ Zero data loss verified
3. ✅ Backup created successfully
4. ✅ Legacy IDs preserved in metadata
5. ✅ Epic/feature hierarchy queries work via metadata
6. ✅ `/feature-generate-tasks` uses `id_generator.py`
7. ✅ All commands updated to use metadata hierarchy
8. ✅ Documentation updated (migration guide, integration guide)
9. ✅ Tests passing (unit, integration, migration validation)
10. ✅ Backward compatibility verified

## Dependencies

- taskwright's `id_generator.py` (863 lines, production-ready)
- taskwright migration experience (703 tasks successfully migrated Nov 2025)
- TASK-035 architectural review (decision rationale)

## Estimated Timeline

- **Phase 1** (ID Generation Implementation): 2-3 days
- **Phase 2** (Command Updates): 1 day
- **Phase 3** (Documentation): 1 day
- **Total**: 3-4 days

**Priority**: High (strategic architectural alignment)
**Complexity**: 7/10 (migration complexity, cross-reference updates)

## References

- [TASK-035 Architectural Review Report](file:///Users/richardwoollcott/Projects/appmilla_github/require-kit/.claude/reviews/TASK-035-review-report.md)
- [taskwright id_generator.py](file:///Users/richardwoollcott/Projects/appmilla_github/taskwright/installer/global/lib/id_generator.py)
- [feature-generate-tasks.md](file:///Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/global/commands/feature-generate-tasks.md)
- [Bidirectional Integration Architecture](file:///Users/richardwoollcott/Projects/appmilla_github/require-kit/docs/architecture/bidirectional-integration.md)

## Next Steps

When ready to implement:

```bash
# Review the architectural decision
cat .claude/reviews/TASK-035-review-report.md

# Begin implementation
/task-work TASK-036
```

**Important**: This task follows the recommended approach from TASK-035 architectural review (Option D: Hash-based IDs with Metadata Hierarchy, scored 10/11).
