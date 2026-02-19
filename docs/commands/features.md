# Feature Commands

Commands for creating and managing implementation units.

## /feature-create

Create a new feature.

**Usage:**
```bash
/feature-create "Feature Title" epic:EPIC-XXX
```

[See detailed documentation →](../guides/command_usage_guide.md#feature-create)

## /feature-status

View feature progress and linked requirements.

**Usage:**
```bash
/feature-status FEAT-XXX
```

[See detailed documentation →](../guides/command_usage_guide.md#feature-status)

## /feature-generate-tasks

Generate task specifications from feature.

**Usage:**
```bash
/feature-generate-tasks FEAT-XXX
```

[See detailed documentation →](../guides/command_usage_guide.md#feature-generate-tasks)

## /feature-refine

Interactively refine an existing feature specification with focus on acceptance criteria specificity, requirements traceability, and BDD scenario coverage.

**Usage:**
```bash
/feature-refine <feature-id> [options]
```

**Examples:**
```bash
/feature-refine FEAT-001
/feature-refine FEAT-001 --focus acceptance
/feature-refine FEAT-001 --focus bdd
/feature-refine FEAT-001 --focus traceability
/feature-refine FEAT-001 --quick
```

**Options:**

| Flag | Description |
|---|---|
| `--focus <category>` | Restrict refinement to a single category: `acceptance`, `traceability`, `bdd`, `technical`, `dependencies`, or `scope` |
| `--quick` | Skip interactive prompts and apply AI-suggested improvements automatically |

**Three-Phase Flow:**

1. **Current State Display** — Loads the feature, parses content, calculates a 7-dimension completeness score, and shows linked epic context.
2. **Targeted Questions** — Presents feature-specific questions one at a time from the weakest categories first.
3. **Change Summary and Commit** — Displays proposed changes, updates the markdown file, and appends a `refinement_history` entry.

**Completeness Dimensions:**

| Dimension | Weight |
|---|---|
| Scope Within Epic | 10% |
| Acceptance Criteria | 25% |
| Requirements Traceability | 20% |
| BDD Coverage | 15% |
| Technical Considerations | 15% |
| Dependencies | 10% |
| Test Strategy | 5% |

**Cross-Command Integration:**

- Suggests [`/formalize-ears`](requirements.md#formalize-ears) when linked EARS requirements are missing
- Suggests [`/generate-bdd`](requirements.md#generate-bdd) when BDD scenario coverage is low
- Displays parent epic completeness for context

[See detailed documentation →](../guides/command_usage_guide.md#feature-refine)

## /feature-sync

Sync feature with PM tools.

**Usage:**
```bash
/feature-sync FEAT-XXX --jira
```

[See detailed documentation →](../guides/command_usage_guide.md#feature-sync)

For complete command documentation, see the [Command Usage Guide](../guides/command_usage_guide.md).
