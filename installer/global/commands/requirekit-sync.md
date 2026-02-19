# RequireKit Sync - Graphiti Sync/Recovery Command

Re-read markdown files and push current state to Graphiti. Markdown is the **authoritative source of truth** — this command rebuilds Graphiti's knowledge graph from local files using a one-way upsert pattern. There is no conflict detection; markdown always wins.

## Usage
```bash
/requirekit-sync [epic-id|feature-id|--all] [options]
```

## Examples
```bash
# Sync a specific epic
/requirekit-sync EPIC-001

# Sync a specific feature
/requirekit-sync FEAT-002

# Sync all epics and features
/requirekit-sync --all

# Preview what would be synced without writing to Graphiti
/requirekit-sync --dry-run

# Dry-run for a specific epic
/requirekit-sync EPIC-001 --dry-run

# Sync all with verbose output
/requirekit-sync --all --verbose
```

## Process Flow

### 1. Check Graphiti Configuration

Read `installer/global/config/graphiti.yaml` and verify Graphiti is enabled.

```yaml
# graphiti.yaml
graphiti:
  enabled: true              # Must be true for sync to proceed
  endpoint: "bolt://localhost:7687"
  project_namespace: "my_project"
  group_id_pattern: "{project}__requirements"
```

If `enabled: false`, the command exits gracefully with setup guidance (see Error Handling below).

### 2. Scan Markdown Files

Scan the following directories for markdown files:

- **`docs/epics/`** — All subdirectories (`active/`, `completed/`, `cancelled/`)
- **`docs/features/`** — All subdirectories (`active/`, `in_progress/`, `completed/`, `cancelled/`)

When a specific ID is provided (e.g., `EPIC-001` or `FEAT-002`), only scan for that entity's file.

### 3. Parse Frontmatter and Content

For each markdown file:
1. Extract YAML frontmatter (between `---` delimiters)
2. Parse the `id`, `title`, `status`, `priority`, and other metadata fields
3. Capture the full markdown body as `episode_body`
4. Validate that required fields (`id`, `title`) are present
5. Skip files with invalid or missing frontmatter (log a warning, continue with remaining files)

### 4. Construct Episode Objects

Build Graphiti episode objects following the schema from the RequireKit specification.

**Epic Episode:**
```python
{
    "name": f"Epic: {epic_title}",
    "episode_body": epic_markdown_content,
    "group_id": f"{project_namespace}__requirements",
    "source": "text",
    "source_description": f"RequireKit epic {epic_id}",
    "_metadata": {
        "entity_type": "epic",
        "epic_id": epic_id,
        "status": epic_status,
        "priority": epic_priority,
        "organisation_pattern": organisation_pattern,
        "feature_ids": [...],
        "direct_task_ids": [...]
    }
}
```

**Feature Episode:**
```python
{
    "name": f"Feature: {feature_title}",
    "episode_body": feature_markdown_content,
    "group_id": f"{project_namespace}__requirements",
    "source": "text",
    "source_description": f"RequireKit feature {feature_id}",
    "_metadata": {
        "entity_type": "feature",
        "feature_id": feature_id,
        "epic_id": parent_epic_id,
        "status": feature_status,
        "priority": feature_priority,
        "acceptance_criteria_count": n,
        "bdd_scenario_ids": [...],
        "requirement_ids": [...]
    }
}
```

### 5. Upsert to Graphiti

Upsert each episode to Graphiti using the `{project}__requirements` group ID.

- **Deduplication key**: Use `epic_id` or `feature_id` from the `_metadata` field
- **Upsert semantics**: If an episode with a matching entity ID already exists, update it; otherwise create a new episode
- **No conflict detection**: This is a one-way sync — markdown content overwrites whatever is in Graphiti

### 6. Display Summary

Show progress during sync and a summary at completion (see Output Format below).

## Dry-Run Mode

When `--dry-run` is specified, the command previews what would be synced without writing any data to Graphiti:

```
🔍 RequireKit Sync (dry-run)
Endpoint: bolt://localhost:7687
Group: my_project__requirements

Would sync epics:
  EPIC-001: User Management System (exists in Graphiti → would update)
  EPIC-002: Fix Auth Bugs (not in Graphiti → would create)

Would sync features:
  FEAT-001: User Authentication (exists in Graphiti → would update)
  FEAT-002: Profile Management (not in Graphiti → would create)

Dry-run complete: 2 epics, 2 features would be synced
No changes written to Graphiti.
```

## Output Format

### Sync Progress Display

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

### Status Indicators

| Icon | Meaning |
|------|---------|
| ✅ | Successfully synced (new or updated) |
| ⚠️ | Skipped (invalid frontmatter or parse error) |
| ❌ | Failed (connection error, Graphiti rejection) |

## Error Handling

### Graphiti Not Configured

When `graphiti.enabled` is `false` or the config file is missing:

```
ℹ️  Graphiti integration is not enabled.

RequireKit works in standalone mode using markdown files only.
To enable Graphiti sync:

1. Edit installer/global/config/graphiti.yaml
2. Set enabled: true
3. Update endpoint to your Neo4j/Graphiti instance
4. Run /requirekit-sync --all

See the Graphiti configuration guide for details.
```

### Connection Failure

When the Graphiti endpoint is unreachable or the connection times out:

```
❌ Cannot connect to Graphiti at bolt://localhost:7687

Possible causes:
  - Neo4j/Graphiti is not running
  - Endpoint URL is incorrect
  - Network/firewall issues

Suggestion: Verify your Graphiti instance is running, then retry:
  /requirekit-sync --all
```

### Partial Failure

When some files sync successfully but others fail, the command continues syncing remaining files and reports all failures at the end:

```
🔄 RequireKit Sync
Endpoint: bolt://localhost:7687
Group: my_project__requirements

Syncing epics...
  ✅ EPIC-001: User Management System (updated)
  ❌ EPIC-002: Fix Auth Bugs (Graphiti error: schema validation failed)
  ✅ EPIC-003: Mobile Redesign (new)

Syncing features...
  ✅ FEAT-001: User Authentication (updated)
  ⚠️  FEAT-002: Invalid frontmatter, skipped

Summary:
  Epics: 2 synced, 0 skipped, 1 failed
  Features: 1 synced, 1 skipped, 0 failed
  Duration: 2.1s

Failed items:
  EPIC-002: Schema validation error — check frontmatter fields
```

### Invalid Markdown

Files with missing or invalid YAML frontmatter are skipped with a warning. The sync continues processing all remaining valid files:

```
⚠️  FEAT-003: Could not parse frontmatter (missing 'id' field), skipped
```

## Configuration Reference

The sync command reads configuration from `installer/global/config/graphiti.yaml`:

| Field | Description | Used By Sync |
|-------|-------------|--------------|
| `enabled` | Whether Graphiti integration is active | Pre-flight check |
| `endpoint` | Bolt URI for Neo4j/Graphiti | Connection target |
| `project_namespace` | Project identifier | Group ID construction |
| `group_id_pattern` | Template: `{project}__requirements` | Episode group_id |

## Sync Behavior Details

### Markdown-Authoritative Design

This command implements a **one-way sync** from markdown to Graphiti:

1. **Read**: Scan and parse local markdown files
2. **Push**: Upsert parsed content as Graphiti episodes
3. **Overwrite**: Any existing Graphiti data for the entity is replaced

There is no pull, no bidirectional merge, and no conflict detection. The markdown files under `docs/epics/` and `docs/features/` are always the canonical source. Graphiti serves as a queryable index rebuilt from those files.

### When to Use This Command

- **Recovery**: Rebuild Graphiti after data loss or corruption
- **Initial population**: Push all existing markdown to a fresh Graphiti instance
- **Manual sync**: When `sync_on_create` or `sync_on_refine` are disabled
- **Verification**: Use `--dry-run` to confirm what Graphiti would contain

### Relationship to Other Commands

| Command | Sync Behavior |
|---------|---------------|
| `/epic-create` | Auto-syncs if `sync_on_create: true` in config |
| `/feature-create` | Auto-syncs if `sync_on_create: true` in config |
| `/epic-refine` | Auto-syncs if `sync_on_refine: true` in config |
| `/feature-refine` | Auto-syncs if `sync_on_refine: true` in config |
| `/requirekit-sync` | Manual full or selective sync (this command) |

## Best Practices

1. **Run `--dry-run` first**: Preview before syncing to verify scan results
2. **Sync after bulk edits**: When multiple markdown files are updated outside of RequireKit commands
3. **Use selective sync**: Sync individual entities when possible for faster execution
4. **Monitor failures**: Check the summary for skipped/failed items and fix frontmatter issues
5. **Recovery workflow**: After Graphiti database reset, run `/requirekit-sync --all` to rebuild
