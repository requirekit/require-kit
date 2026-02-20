# Epic Commands

Commands for creating and managing strategic business objectives.

## /epic-create

Create a new epic.

**Usage:**
```bash
/epic-create "Epic Title" [options]
```

**Examples:**
```bash
/epic-create "User Management System"
/epic-create "Config Refactor" --pattern direct
```

**Options:**

| Flag | Description |
|---|---|
| `--pattern <pattern>` | Set organisation pattern: `standard` (default), `direct`, or `mixed` |

> **Note:** If Graphiti is configured, epics are automatically synced to the knowledge graph on creation.

[See detailed documentation →](../guides/command_usage_guide.md#epic-create)

## /epic-status

View epic progress and linked features.

**Usage:**
```bash
/epic-status EPIC-XXX
```

[See detailed documentation →](../guides/command_usage_guide.md#epic-status)

## /epic-generate-features

Generate features from epic scope.

**Usage:**
```bash
/epic-generate-features EPIC-XXX
```

[See detailed documentation →](../guides/command_usage_guide.md#epic-generate-features)

## /epic-refine

Interactively refine an existing epic through completeness scoring, targeted questions, and change summaries.

**Usage:**
```bash
/epic-refine <epic-id> [options]
```

**Examples:**
```bash
/epic-refine EPIC-001
/epic-refine EPIC-001 --focus scope
/epic-refine EPIC-001 --focus risks
/epic-refine EPIC-001 --quick
```

**Options:**

| Flag | Description |
|---|---|
| `--focus <category>` | Restrict refinement to a single category: `scope`, `criteria`, `acceptance`, `dependencies`, `risks`, `constraints`, or `organisation` |
| `--quick` | Skip interactive prompts and apply AI-suggested improvements automatically |

**Three-Phase Flow:**

1. **Current State Display** — Loads the epic, calculates a 9-dimension completeness score, and displays the assessment with visual indicators.
2. **Targeted Questions** — Presents questions one at a time starting from the weakest categories, with options to skip or finish early.
3. **Change Summary and Commit** — Displays a summary of proposed changes, offers apply options (Yes / No / Edit), updates the markdown file, and appends a `refinement_history` entry to the frontmatter.

**Completeness Dimensions:**

| Dimension | Weight |
|---|---|
| Business Objective | 15% |
| Scope | 15% |
| Success Criteria | 20% |
| Acceptance Criteria | 15% |
| Risk | 10% |
| Constraints | 10% |
| Dependencies | 5% |
| Stakeholders | 5% |
| Organisation | 5% |

**Organisation Pattern Awareness:**

The command detects organisation patterns and provides targeted suggestions:

- **Large direct-pattern epics** (8+ tasks without features) — suggests grouping tasks into features
- **Single-feature epics** — suggests flattening to simplify hierarchy
- **Mixed patterns** — suggests consolidation for consistency

[See detailed documentation →](../guides/command_usage_guide.md#epic-refine)

## /epic-sync

Sync epic with PM tools.

**Usage:**
```bash
/epic-sync EPIC-XXX --jira
```

[See detailed documentation →](../guides/command_usage_guide.md#epic-sync)

For complete command documentation, see the [Command Usage Guide](../guides/command_usage_guide.md).
