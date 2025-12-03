---
id: TASK-038
title: Create Migration Communication and Release Plan
status: backlog
created: 2025-11-29T17:05:00Z
updated: 2025-11-29T17:05:00Z
priority: medium
tags: [documentation, communication, release, migration]
complexity: 3
related_to: TASK-035, TASK-036
parent_review: TASK-035
dependencies: [TASK-036]
estimated_effort: 0.5 day
test_results:
  status: pending
  coverage: null
  last_run: null
---

# Task: Create Migration Communication and Release Plan

## Context

This task implements **Phase 3 (Communication)** from [TASK-035 Review](file:///Users/richardwoollcott/Projects/appmilla_github/require-kit/.claude/reviews/TASK-035-review-report.md):

**Objective**: Communicate hash-based ID migration to users effectively

**From Review**:
> **Phase 3: Communication (Ongoing)**
> - GitHub release notes
> - Migration guide
> - Breaking change notice (if any)
> - Rationale (link to this review)

## Objectives

1. ✅ Create user-facing migration guide
2. ✅ Draft GitHub release notes
3. ✅ Prepare breaking change notice
4. ✅ Document rollback procedure
5. ✅ Create FAQ for common migration questions

## Acceptance Criteria

### 1. Migration Guide Creation (0.25 day)

- [ ] **1.1**: Create comprehensive migration guide
  - File: `docs/guides/hash-id-migration-guide.md`
  - Target audience: Existing require-kit users
  - Before/after examples with screenshots
  - Step-by-step migration walkthrough
  - Troubleshooting section

- [ ] **1.2**: Migration guide sections
  ```markdown
  ## Why We're Migrating
  - Collision-free IDs (link to TASK-035 review)
  - Alignment with taskwright
  - Production-proven approach (703 tasks migrated successfully)

  ## What's Changing
  - ID format: TASK-001 → TASK-A3F2
  - Hierarchy: Embedded → Metadata
  - Commands: Same functionality, metadata queries

  ## What's NOT Changing
  - File structure (tasks/ directories)
  - Task content (descriptions, acceptance criteria)
  - Command names and usage

  ## Migration Timeline
  - When: [Release date TBD]
  - Automatic: Yes (migration script runs during upgrade)
  - Backup: Automatic (`.claude/state/backup/...`)

  ## Backward Compatibility
  - Legacy IDs preserved in `legacy_id` field
  - Old task references still work
  - Rollback available if needed

  ## FAQ
  - Q: Will my existing tasks be deleted?
    A: No, all tasks are backed up and migrated automatically

  - Q: Can I still reference tasks by old IDs?
    A: Yes, legacy IDs are preserved in metadata

  - Q: What if something goes wrong?
    A: Rollback script available, backup preserved
  ```

### 2. Release Notes (0.125 day)

- [ ] **2.1**: Draft GitHub release notes
  - File: `docs/releases/RELEASE-NOTES-v2.0.0.md`
  - Highlight: Hash-based IDs (breaking change)
  - Rationale: Link to TASK-035 architectural review
  - Migration: Link to migration guide
  - Rollback: Link to rollback procedure

- [ ] **2.2**: Release notes template
  ```markdown
  # require-kit v2.0.0 - Hash-Based ID Migration

  ## 🎯 Major Changes

  ### Hash-Based Task IDs (Breaking Change)

  We've migrated from sequential IDs to hash-based IDs for collision-free
  task identification. This aligns require-kit with taskwright's proven
  approach (703 tasks migrated successfully).

  **Before**: `TASK-001`, `TASK-035`
  **After**: `TASK-A3F2`, `TASK-E01-B2C4`

  **Why**: [Architectural Review](../reviews/TASK-035-review-report.md)

  ### Automatic Migration

  ✅ All existing tasks automatically migrated during upgrade
  ✅ Backup created: `.claude/state/backup/tasks-pre-hash-migration-{timestamp}/`
  ✅ Legacy IDs preserved in `legacy_id` frontmatter field
  ✅ Rollback available if needed

  ### What's Preserved

  - ✅ All task content (descriptions, criteria, metadata)
  - ✅ File organization (tasks/ directory structure)
  - ✅ Command functionality (same commands, metadata queries)
  - ✅ Integration with taskwright (enhanced alignment)

  ## 📚 Documentation

  - [Migration Guide](../guides/hash-id-migration-guide.md)
  - [Architectural Review](../reviews/TASK-035-review-report.md)
  - [Rollback Procedure](#rollback)

  ## 🐛 Known Issues

  None identified during migration of 703 taskwright tasks.

  ## ⬆️ Upgrade Instructions

  ```bash
  cd require-kit
  git pull origin main
  ./installer/scripts/install.sh
  # Migration runs automatically, backup created
  ```

  ## ⬇️ Rollback Procedure

  If needed, rollback using the backup:

  ```bash
  ./installer/scripts/rollback-migration.sh
  ```

  See [Rollback Guide](../guides/rollback-migration.md) for details.
  ```

### 3. Breaking Change Notice (0.0625 day)

- [ ] **3.1**: Create breaking change notice
  - File: `BREAKING-CHANGES-v2.0.0.md`
  - Clear headline: "Task ID Format Change"
  - Impact assessment: High (all tasks affected)
  - Mitigation: Automatic migration + backup
  - Timeline: Immediate (upgrade triggers migration)

- [ ] **3.2**: Breaking change template
  ```markdown
  # Breaking Changes in v2.0.0

  ## Task ID Format Change

  **Severity**: High
  **Impact**: All existing tasks
  **Mitigation**: Automatic migration with backup

  ### What Changed

  Task IDs changed from sequential to hash-based format.

  ### Before
  ```
  TASK-001
  TASK-035
  TASK-100
  ```

  ### After
  ```
  TASK-A3F2
  TASK-B7D1
  TASK-E01-C4F8
  ```

  ### Why

  Hash-based IDs eliminate collision risk and align with taskwright's
  proven approach. See [Architectural Review](docs/reviews/TASK-035-review-report.md).

  ### Migration Path

  Migration is automatic during upgrade:
  1. Backup created (`.claude/state/backup/...`)
  2. Tasks migrated to hash-based IDs
  3. Legacy IDs preserved in metadata
  4. Cross-references updated

  ### Compatibility

  ✅ Legacy IDs preserved in `legacy_id` field
  ✅ Commands work with both old and new IDs
  ✅ Rollback available if needed

  ### Action Required

  None - migration is automatic. Review backup after upgrade.
  ```

### 4. Rollback Documentation (0.0625 day)

- [ ] **4.1**: Create rollback guide
  - File: `docs/guides/rollback-migration.md`
  - Prerequisites: Backup exists
  - Step-by-step rollback procedure
  - Verification steps
  - When to rollback vs report issue

- [ ] **4.2**: Create rollback script
  - File: `installer/scripts/rollback-migration.sh`
  - Detect latest backup
  - Restore tasks from backup
  - Verify restoration
  - Clear success/failure messages

### 5. FAQ and Troubleshooting (0.125 day)

- [ ] **5.1**: Common migration questions
  ```markdown
  ## FAQ

  **Q: Will I lose any data?**
  A: No. All tasks are backed up before migration, and all content
     is preserved during migration.

  **Q: Can I keep using old task IDs?**
  A: Legacy IDs are preserved in metadata for reference, but new
     operations should use hash-based IDs.

  **Q: What if the migration fails?**
  A: Use the rollback script to restore from backup. Report the
     issue on GitHub.

  **Q: Do I need to update my PM tools (Jira, Linear)?**
  A: No. PM tool integration uses metadata, not IDs directly.

  **Q: Will this affect taskwright integration?**
  A: Yes - positively! Both packages now use the same ID format,
     improving integration.

  **Q: How long does migration take?**
  A: ~1-2 minutes for 250 tasks (based on taskwright's 703 task
     migration experience).

  **Q: Can I preview the migration?**
  A: Run in dry-run mode: `./installer/scripts/install.sh --dry-run`
  ```

- [ ] **5.2**: Troubleshooting guide
  ```markdown
  ## Troubleshooting

  **Issue: Migration script fails**
  - Check disk space (need ~2x task storage)
  - Check permissions on tasks/ directories
  - Review error log: `.claude/state/migration-error.log`

  **Issue: Cross-references broken**
  - Migration script updates references automatically
  - If missed, manually update using legacy_id field
  - Report missing references as GitHub issue

  **Issue: Commands not finding tasks**
  - Verify migration completed: Check for hash-based IDs in tasks/
  - Check frontmatter has `epic`, `feature` metadata
  - Rollback if persistent issues
  ```

## Files to Create

1. `docs/guides/hash-id-migration-guide.md` (NEW)
2. `docs/releases/RELEASE-NOTES-v2.0.0.md` (NEW)
3. `BREAKING-CHANGES-v2.0.0.md` (NEW)
4. `docs/guides/rollback-migration.md` (NEW)
5. `installer/scripts/rollback-migration.sh` (NEW)

## Dependencies

- **TASK-036**: Must be implemented first (migration logic exists)
- **TASK-035**: Architectural review provides rationale

## Success Criteria

This task is complete when:

1. ✅ Migration guide created with examples
2. ✅ Release notes drafted with all sections
3. ✅ Breaking change notice documented
4. ✅ Rollback guide and script created
5. ✅ FAQ covers common questions
6. ✅ Troubleshooting guide addresses known issues
7. ✅ All documentation reviewed and proofread

## Estimated Timeline

- **Migration Guide**: 0.25 day
- **Release Notes**: 0.125 day
- **Breaking Change Notice**: 0.0625 day
- **Rollback Documentation**: 0.0625 day
- **FAQ and Troubleshooting**: 0.125 day
- **Total**: ~0.5 day

**Priority**: Medium (needed before release of TASK-036)
**Complexity**: 3/10 (documentation-heavy, straightforward)

## References

- [TASK-035 Review Report](file:///Users/richardwoollcott/Projects/appmilla_github/require-kit/.claude/reviews/TASK-035-review-report.md)
- [TASK-036 Implementation](file:///Users/richardwoollcott/Projects/appmilla_github/require-kit/tasks/backlog/TASK-036-harmonize-id-generation-hash-based.md)
- taskwright migration experience (Nov 2025, 703 tasks)

## Notes

This task should be completed BEFORE releasing TASK-036 to ensure users have
clear communication and support during the migration process.
