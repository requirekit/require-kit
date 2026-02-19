# Sync Commands

Commands for synchronising RequireKit markdown files with the Graphiti knowledge graph.

## /requirekit-sync

Re-read markdown files and push current state to Graphiti. Markdown is the authoritative source of truth — this command rebuilds the Graphiti knowledge graph from local files.

**Usage:**
```bash
/requirekit-sync [epic-id|feature-id|--all] [options]
```

**Examples:**
```bash
/requirekit-sync EPIC-001
/requirekit-sync FEAT-002
/requirekit-sync --all
/requirekit-sync --dry-run
/requirekit-sync EPIC-001 --dry-run
/requirekit-sync --all --verbose
```

**Options:**

| Flag | Description |
|---|---|
| `--all` | Sync all epics and features found in `docs/epics/` and `docs/features/` |
| `--dry-run` | Preview what would be synced without writing to Graphiti |
| `--verbose` | Show detailed sync output for each entity |

**How It Works:**

1. Checks that Graphiti is enabled in configuration
2. Scans `docs/epics/` and `docs/features/` for markdown files
3. Parses frontmatter and content from each file
4. Constructs episode objects following the epic/feature schema
5. Upserts episodes to Graphiti using the configured group ID
6. Displays a summary with sync results

**Markdown-Authoritative Design:**

- **One-way sync** from markdown to Graphiti (markdown always wins)
- No conflict detection or bidirectional merge
- Graphiti serves as a queryable index rebuilt from markdown

**When to Use:**

| Scenario | Command |
|---|---|
| Rebuild Graphiti after data loss | `/requirekit-sync --all` |
| Populate a fresh Graphiti instance | `/requirekit-sync --all` |
| Manual sync when auto-sync is disabled | `/requirekit-sync EPIC-001` |
| Verify what Graphiti would contain | `/requirekit-sync --all --dry-run` |

**Error Handling:**

- **Graphiti not configured** — Shows a helpful setup message
- **Connection failure** — Shows error with retry suggestion
- **Partial failure** — Continues with valid files, reports failures at end
- **Invalid markdown** — Skips with warning, continues with valid files

**Relationship to Other Commands:**

The following commands auto-sync to Graphiti when configured:

- `/epic-create` — auto-syncs if `sync_on_create: true`
- `/feature-create` — auto-syncs if `sync_on_create: true`
- `/epic-refine` — auto-syncs if `sync_on_refine: true`
- `/feature-refine` — auto-syncs if `sync_on_refine: true`

Use `/requirekit-sync` for manual or full sync operations.

[See detailed documentation →](../guides/command_usage_guide.md#requirekit-sync)

For complete command documentation, see the [Command Usage Guide](../guides/command_usage_guide.md).
