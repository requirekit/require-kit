---
complexity: 5
dependencies:
- TASK-RK01-003
feature_id: FEAT-RK-001
id: TASK-RK01-006
implementation_mode: task-work
parent_review: TASK-REV-RK01
priority: normal
status: design_approved
tags:
- requirekit-sync
- graphiti
- sync
- command
task_type: feature
title: Create /requirekit-sync command
wave: 2
---

# Task: Create /requirekit-sync Command

## Description

Create the `/requirekit-sync` command at `installer/global/commands/requirekit-sync.md`. This is the Graphiti sync/recovery command that re-reads markdown files and pushes current state to Graphiti.

## Files to Create

- `installer/global/commands/requirekit-sync.md` - Graphiti sync/recovery command

## Changes Required

### Command Structure
```bash
/requirekit-sync [epic-id|feature-id|--all]

# Examples
/requirekit-sync EPIC-001          # Sync specific epic
/requirekit-sync FEAT-002          # Sync specific feature
/requirekit-sync --all             # Sync all epics and features
/requirekit-sync --dry-run         # Show what would be synced
```

### Sync Logic
- **Markdown authoritative**: Re-read markdown files, push to Graphiti
- **Upsert pattern**: Use epic_id/feature_id as deduplication key
- **No conflict detection**: Simple overwrite - markdown always wins
- **Progress display**: Show sync progress with counts

### Process Flow
1. Check Graphiti enabled in config
2. Scan docs/epics/ and docs/features/ for markdown files
3. Parse each file's frontmatter and content
4. Construct episode objects (epic/feature schema from spec)
5. Upsert episodes to Graphiti using `{project}__requirements` group ID
6. Display summary: synced count, errors, warnings

### Error Handling
- Graphiti not configured: Show helpful message with setup instructions
- Connection failure: Show error with retry suggestion
- Partial failure: Continue syncing remaining files, report failures
- Invalid markdown: Skip with warning, continue with valid files

### Output Format
```
🔄 RequireKit Sync
Endpoint: bolt://localhost:7687
Group: my_project__requirements

Syncing epics...
  ✅ EPIC-001: User Management System (updated)
  ✅ EPIC-002: Fix Auth Bugs (new)
  ⚠️  EPIC-003: Invalid frontmatter, skipped

Syncing features...
  ✅ FEAT-001: User Authentication (updated)
  ✅ FEAT-002: Profile Management (new)

Summary:
  Epics: 2 synced, 1 skipped
  Features: 2 synced, 0 skipped
  Duration: 1.2s
```

## Acceptance Criteria

- [ ] Command supports individual sync (by ID) and full sync (--all)
- [ ] Markdown is authoritative (Graphiti rebuilt from markdown)
- [ ] Upsert uses entity ID as deduplication key
- [ ] Graceful handling when Graphiti not configured
- [ ] Partial failure doesn't stop remaining syncs
- [ ] `--dry-run` shows what would be synced without writing
- [ ] Output shows clear progress and summary

## Test Requirements

- [ ] Verify command file has valid structure
- [ ] Verify sync patterns documented
- [ ] Verify error handling covers all failure modes