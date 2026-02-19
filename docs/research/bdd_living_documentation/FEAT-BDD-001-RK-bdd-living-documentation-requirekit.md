# Feature: BDD Living Documentation — RequireKit Side

> **Feature ID**: FEAT-BDD-001-RK
> **Priority**: P1 (Phase 3)
> **Estimated Effort**: 2-3 days
> **Target Repo**: RequireKit
> **Dependencies**: FEAT-GE-001 (Graphiti entities), FEAT-RK-001 (RequireKit Graphiti integration)

---

## Summary

Enhance RequireKit's existing `/generate-bdd` command to push BDD scenarios to Graphiti as queryable living documentation, and add a `/feature-status` command that displays scenario verification state per feature. This is the **write side** of the BDD feedback loop — RequireKit creates and maintains BDD scenarios in both markdown files and Graphiti, making them discoverable by GuardKit during task execution and validation.

Today, `/generate-bdd` produces `.feature` files and stops there. Those files sit inert in the repository. This feature turns them into active knowledge: every scenario becomes a queryable episode in Graphiti with metadata linking it to its requirement, feature, and epic. When GuardKit later verifies scenarios during `/task-complete`, their status flows back to Graphiti — and `/feature-status` surfaces that state to the product owner.

---

## Current State

### What Exists

- **`/generate-bdd`** — Transforms EARS requirements into Gherkin `.feature` files. Supports generation per requirement ID, per epic, or with tag filters. Produces well-structured scenarios with happy path, edge cases, error handling, performance, and security coverage. Output goes to `docs/bdd/features/`.
- **`bdd-generator.md`** agent (core + ext) — Handles the EARS → Gherkin transformation patterns (Event-Driven → Given-When-Then, State-Driven → Scenario with State, Unwanted Behaviour → Error Scenario).
- **Tag convention** — Scenarios are tagged with `@requirement-REQ-XXX`, `@epic-EPIC-XXX`, `@feature-FEAT-XXX`, `@priority-high`, `@smoke`, `@regression`, etc.
- **No Graphiti integration** — BDD scenarios exist only as `.feature` files.
- **No verification tracking** — No way to know which scenarios pass, fail, or have never been run.
- **No feature-level status view** — Product owner has no dashboard showing BDD coverage or health.

### What's Missing

1. **Graphiti push after generation** — `/generate-bdd` should write scenario episodes to Graphiti alongside `.feature` files.
2. **Per-scenario episode structure** — Each scenario needs its own Graphiti episode for granular queryability.
3. **Verification status tracking** — Scenarios need a `status` field (generated, verified, failed, stale) that GuardKit can update.
4. **`/feature-status` command** — A read-only view showing scenario health per feature for product owners.
5. **Bulk import for existing `.feature` files** — Projects with existing BDD files need a migration path.

---

## Enhanced `/generate-bdd` Command

### Current Arguments (Preserved)

```bash
/generate-bdd                           # Generate for all requirements
/generate-bdd REQ-001                   # Generate for specific requirement
/generate-bdd --epic EPIC-001           # Generate for an epic
/generate-bdd --tags critical,smoke     # Generate with specific tags
```

### New Arguments

```bash
/generate-bdd --no-graphiti             # Skip Graphiti push (markdown only)
/generate-bdd --sync                    # Re-push all existing .feature files to Graphiti
/generate-bdd --dry-run                 # Show what would be generated/pushed without writing
```

### Enhanced Output Flow

The command now operates in two stages:

**Stage 1: Generate `.feature` files** (existing behaviour, unchanged)

Produces Gherkin scenarios in `docs/bdd/features/` following the established transformation patterns. Tags, scenario outlines, backgrounds, and integration hints all work as before.

**Stage 2: Push to Graphiti** (new)

After writing `.feature` files, each individual scenario is pushed as a Graphiti episode:

```
For each .feature file generated:
  Parse into individual scenarios
  For each scenario:
    Construct episode content (scenario text + metadata)
    Upsert to Graphiti with group_id: "{project}__bdd_scenarios"
    Set entity_type: "bdd_scenario"
    Set status: "generated"
```

If Graphiti is not configured or the push fails, the command still succeeds (`.feature` files are written) and shows a warning: "BDD scenarios saved to markdown. Graphiti sync skipped — enable Graphiti for living documentation features."

### Graphiti Episode Schema for BDD Scenarios

Each scenario becomes one episode:

```yaml
# Episode content structure
group_id: "{project}__bdd_scenarios"
name: "BDD: {feature_name} - {scenario_name}"
entity_type: "bdd_scenario"

# Episode metadata
metadata:
  scenario_id: "BDD-{feature}-{scenario_hash}"     # Stable ID for upsert deduplication
  feature_file: "docs/bdd/features/authentication.feature"
  feature_name: "User Authentication"
  scenario_name: "Successful login with valid credentials"
  requirement_ref: "REQ-001"                         # From @requirement tag
  epic_ref: "EPIC-001"                               # From @epic tag
  feature_ref: "FEAT-001"                             # From @feature tag
  tags: ["happy-path", "smoke", "authentication", "critical"]
  status: "generated"                                 # generated | verified | failed | stale
  last_verified: null                                 # ISO timestamp, set by GuardKit
  last_verified_by: null                              # "task-complete:TASK-XXX" or "manual"
  generated_date: "2026-02-10T14:30:00Z"
  scenario_type: "happy-path"                         # happy-path | edge-case | error-handling | security | performance

# Episode body: the full Gherkin scenario text
content: |
  @happy-path @smoke @requirement-REQ-001
  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter "user@example.com" as email
    And I enter "Pass123!" as password
    And I click the login button
    Then I should be authenticated successfully
    And I should be redirected to the dashboard
    And the authentication should complete within 1 second
```

### Design Decision: One Episode Per Scenario

**Chosen over**: One episode per `.feature` file

**Rationale**: Per-scenario episodes enable GuardKit to query "which specific scenarios are relevant to this task?" rather than retrieving entire feature files. The tag-based metadata (`requirement_ref`, `feature_ref`, `tags`) gives Graphiti's semantic search precise filtering. The trade-off is more Graphiti entries, but typical projects have 50-200 scenarios — well within Graphiti's comfortable range. Feature file path is retained as metadata for grouping when needed.

### Scenario ID Generation

Scenario IDs must be stable for upsert deduplication (so re-running `/generate-bdd` updates rather than duplicates):

```
scenario_id = "BDD-{feature_slug}-{hash(scenario_name)}"

# Example:
# Feature: "User Authentication"
# Scenario: "Successful login with valid credentials"
# → scenario_id: "BDD-user-authentication-a3f7c2"
```

The hash uses the first 6 characters of a SHA-256 of the scenario name. This is stable across regeneration (same name → same ID) but unique enough to avoid collisions within a project.

---

## `/feature-status` Command

### Purpose

A read-only command that shows BDD scenario health per feature, designed for product owners (James) who want to see "is this feature's behaviour validated?" without running tests themselves.

### Arguments

```bash
/feature-status                          # Show all features with BDD coverage
/feature-status FEAT-001                 # Show scenarios for a specific feature
/feature-status --epic EPIC-001          # Show all features in an epic
/feature-status --failing                # Show only features with failing scenarios
/feature-status --stale                  # Show scenarios not verified in 7+ days
```

### Output Format

**Overview mode** (no feature specified):

```
📊 BDD Scenario Status

EPIC-001: User Management System
  FEAT-001: User Authentication
    ✅ 4/6 verified  ⚠️ 1 failing  ❓ 1 never verified
    Last verified: 2026-02-09 (TASK-042)
  
  FEAT-002: User Registration
    ✅ 8/8 verified
    Last verified: 2026-02-10 (TASK-045)
  
  FEAT-003: Password Recovery
    ❓ 5/5 generated (never verified)

EPIC-002: Payment Processing
  FEAT-004: Checkout Flow
    ✅ 3/7 verified  ⚠️ 2 failing  ⏳ 2 stale (>7 days)
    Last verified: 2026-02-03 (TASK-038)

Summary: 15/26 verified (58%) | 3 failing | 5 never verified | 2 stale
```

**Detail mode** (specific feature):

```
📊 FEAT-001: User Authentication — BDD Scenarios

  ✅ Successful login with valid credentials
     Verified: 2026-02-09 by task-complete:TASK-042
     Tags: @happy-path @smoke

  ✅ Login with remember me option
     Verified: 2026-02-09 by task-complete:TASK-042
     Tags: @edge-case

  ⚠️ Account lockout after failed attempts
     FAILED: 2026-02-09 by task-complete:TASK-042
     Tags: @security
     Note: Lockout threshold changed from 3→5, scenario expects 3

  ✅ Login with invalid credentials
     Verified: 2026-02-09 by task-complete:TASK-042
     Tags: @error-handling

  ✅ Session timeout handling
     Verified: 2026-02-08 by task-complete:TASK-039
     Tags: @edge-case

  ❓ Multi-factor authentication flow
     Status: generated (never verified)
     Tags: @security @happy-path
     Generated: 2026-02-07

Coverage: 4/6 verified (67%) | 1 failing | 1 unverified
Requirement coverage: REQ-001 (4/4 ✅), REQ-007 (0/1 ❓), REQ-012 (0/1 ⚠️)
```

### Data Source

`/feature-status` queries Graphiti for BDD scenario episodes:

```python
# Query all scenarios for a feature
results = graphiti_client.search(
    query=f"BDD scenarios for feature {feature_id}",
    group_ids=[f"{project}__bdd_scenarios"],
    num_results=50
)

# Or for an epic
results = graphiti_client.search(
    query=f"BDD scenarios for epic {epic_id}",
    group_ids=[f"{project}__bdd_scenarios"],
    num_results=100
)
```

### Graceful Degradation

If Graphiti is not configured, `/feature-status` falls back to scanning `.feature` files on disk and displaying scenario counts without verification status:

```
📊 FEAT-001: User Authentication — BDD Scenarios (file-based, no verification tracking)

  📄 6 scenarios found in docs/bdd/features/authentication.feature
  Tags: @happy-path(2), @edge-case(2), @error-handling(1), @security(1)

  ℹ️ Enable Graphiti for verification tracking and status updates.
```

---

## `/generate-bdd --sync` (Bulk Import)

### Purpose

For existing projects with `.feature` files that predate Graphiti integration, `--sync` reads all existing feature files and pushes them to Graphiti as "generated" episodes.

### Flow

```
1. Scan docs/bdd/features/**/*.feature
2. Parse each file into individual scenarios
3. Extract tags, requirement refs, feature refs from Gherkin
4. Upsert each scenario as a Graphiti episode with status: "generated"
5. Report: "Synced N scenarios from M feature files to Graphiti"
```

### Idempotency

Uses the stable `scenario_id` for upsert, so running `--sync` multiple times is safe. Changed scenarios are updated; removed scenarios are not deleted (they become "stale" naturally when their feature file no longer contains them).

### Stale Scenario Detection

When `--sync` runs, it can detect scenarios in Graphiti that no longer exist in `.feature` files:

```
⚠️ 2 scenarios in Graphiti not found in current .feature files:
  - BDD-user-auth-b4e2c1: "Legacy SSO login flow" (last verified: 2026-01-15)
  - BDD-user-auth-d8f3a9: "LDAP authentication" (never verified)

These may have been intentionally removed. Use --prune to remove them from Graphiti.
```

The `--prune` flag is intentionally separate to avoid accidental deletion.

---

## Graphiti Integration Details

### Group ID Strategy

All BDD scenarios share one group ID per project:

```
group_id: "{project}__bdd_scenarios"
```

This follows the pattern established in FEAT-RK-001 where `{project}__requirements` uses a single group with `entity_type` differentiation. Within the BDD group, scenarios are differentiated by their metadata fields (`feature_ref`, `epic_ref`, `scenario_type`).

### Write Ownership

RequireKit owns BDD scenario creation (writes). GuardKit owns verification status updates (reads + status writes). This is the same ownership model as `{project}__requirements` — RequireKit writes requirements, GuardKit reads them.

However, GuardKit needs to update the `status`, `last_verified`, and `last_verified_by` fields on BDD episodes. This is a **targeted write** — GuardKit updates metadata on existing episodes but never creates or deletes BDD episodes.

### Cross-Tool Coordination

RequireKit and GuardKit connect to the same Graphiti/Neo4j instance. Project namespace provides isolation:

```
RequireKit writes → {project}__bdd_scenarios (full episodes)
GuardKit reads   ← {project}__bdd_scenarios (during task-work, coach validation)
GuardKit updates → {project}__bdd_scenarios (status fields only, during task-complete)
```

### RequireKit Standalone Mode

When Graphiti is not configured (standalone mode), all BDD commands work normally using `.feature` files only:

- `/generate-bdd` produces `.feature` files (no Graphiti push)
- `/feature-status` scans `.feature` files for counts only (no verification tracking)
- `--sync` is a no-op with a message suggesting Graphiti configuration

The `graphiti_enabled` flag from FEAT-RK-001's config controls this:

```yaml
# .requirekit/config.yaml
graphiti:
  enabled: false  # Default: off
  endpoint: "bolt://localhost:7687"
  project_namespace: "my_project"
```

---

## BDD Agent Enhancements

### Modified Agent: `bdd-generator.md`

The BDD generator agent needs additional instructions for Graphiti integration:

**Core file additions:**
- After generating `.feature` files, construct Graphiti episode payloads
- Parse Gherkin tags to extract requirement/feature/epic references
- Generate stable scenario IDs from feature name + scenario name

**Ext file additions:**
- Graphiti episode schema reference
- Upsert patterns and error handling
- `--sync` mode file scanning logic
- Stale scenario detection logic

### New Agent: `feature-status-reporter.md`

A lightweight agent for the `/feature-status` command:

**Core file:**
- Query Graphiti for BDD scenario episodes
- Format output for product owner readability
- Calculate coverage percentages and identify gaps

**Ext file:**
- Graphiti query patterns for filtering by feature, epic, status
- Fallback logic for file-based mode when Graphiti is unavailable

---

## Markdown-Graphiti Sync for BDD

**Principle**: `.feature` files are authoritative. Graphiti provides queryability and verification tracking.

### Sync Direction

```
/generate-bdd  → writes .feature files → pushes to Graphiti (markdown-first)
/generate-bdd --sync → reads .feature files → pushes to Graphiti (recovery/migration)
GuardKit task-complete → updates Graphiti status fields only (never touches .feature files)
```

### Drift Handling

If `.feature` files are manually edited (common — developers tweak scenarios during implementation), the Graphiti episodes become stale. Running `/generate-bdd --sync` re-syncs. This is intentionally manual rather than automatic to keep the system predictable.

### What Graphiti Adds Beyond `.feature` Files

- **Verification status** — Which scenarios pass, fail, or have never been run
- **Temporal history** — When was each scenario last verified, by which task
- **Semantic queryability** — GuardKit can ask "which BDD scenarios relate to authentication?" rather than parsing `.feature` files
- **Cross-reference** — Scenarios linked to requirements, features, and epics via metadata

---

## Acceptance Criteria

### `/generate-bdd` Enhancement
- [ ] Existing `/generate-bdd` behaviour unchanged when Graphiti is not configured
- [ ] When Graphiti is enabled, each generated scenario is pushed as a Graphiti episode
- [ ] Episodes use `{project}__bdd_scenarios` group ID with correct metadata schema
- [ ] Scenario IDs are stable (re-running `/generate-bdd` upserts, not duplicates)
- [ ] `--no-graphiti` flag skips Graphiti push even when configured
- [ ] `--sync` reads existing `.feature` files and pushes all scenarios to Graphiti
- [ ] `--sync` detects and reports stale scenarios (in Graphiti but not in files)
- [ ] `--dry-run` shows what would be generated/pushed without writing anything
- [ ] Graphiti failure does not prevent `.feature` file creation (graceful degradation)
- [ ] Warning message shown when Graphiti is configured but push fails

### `/feature-status` Command
- [ ] Overview mode shows all features with BDD coverage percentages
- [ ] Detail mode shows individual scenario status for a specific feature
- [ ] `--epic` flag filters to features within an epic
- [ ] `--failing` flag shows only features with failing scenarios
- [ ] `--stale` flag shows scenarios not verified recently (configurable threshold, default 7 days)
- [ ] Fallback to file-based mode when Graphiti is unavailable
- [ ] Output uses status icons (✅ ⚠️ ❓ ⏳) for quick scanning
- [ ] Requirement coverage shown in detail mode

### Integration
- [ ] GuardKit can read BDD episodes from `{project}__bdd_scenarios` (verified via integration test)
- [ ] GuardKit can update `status`, `last_verified`, `last_verified_by` fields on BDD episodes
- [ ] `/feature-status` correctly reflects status updates made by GuardKit

---

## Testing Approach

### Unit Tests
- Gherkin parser: extract individual scenarios from `.feature` files with tags and metadata
- Scenario ID generation: stable hashing, collision resistance, slug generation
- Episode construction: correct metadata schema, group ID, entity type
- Status aggregation: coverage percentages, filtering by status/feature/epic
- Fallback logic: file-based mode when Graphiti unavailable

### Integration Tests
- Full flow: `/generate-bdd REQ-001` → verify `.feature` file created → verify Graphiti episode exists with correct metadata
- Sync flow: create `.feature` files manually → run `--sync` → verify episodes match files
- Stale detection: add scenario to Graphiti → remove from `.feature` file → run `--sync` → verify stale warning
- Cross-tool: push BDD episodes from RequireKit → query from GuardKit client → verify episodes readable
- Standalone mode: Graphiti disabled → verify all commands work with file-based fallback

### Manual Testing (James UX)
- Product owner can run `/feature-status` and understand the output without technical knowledge
- Status icons are immediately clear (green = good, red = problem, grey = unknown)
- `/feature-status --failing` quickly surfaces problems

---

## File Changes

### New Files

| File | Purpose |
|------|---------|
| `installer/global/commands/feature-status.md` | Feature status command definition |
| `installer/global/agents/feature-status-reporter.md` | Agent for status reporting (core) |
| `installer/global/agents/feature-status-reporter-ext.md` | Agent extension with Graphiti patterns |

### Modified Files

| File | Changes |
|------|---------|
| `installer/global/commands/generate-bdd.md` | Add `--no-graphiti`, `--sync`, `--dry-run`, `--prune` flags. Add Stage 2 Graphiti push instructions. |
| `installer/global/agents/bdd-generator.md` | Add Graphiti episode construction and scenario ID generation. |
| `installer/global/agents/bdd-generator-ext.md` | Add Graphiti upsert patterns, sync logic, stale detection. |
| `installer/global/instructions/core/00-overview.md` | Document BDD living documentation workflow and `/feature-status`. |
| `CLAUDE.md` | Add BDD living documentation and `/feature-status` to RequireKit overview. |
| `docs/commands/bdd.md` | Document enhanced `/generate-bdd` and new `/feature-status` for docs site. |

---

## Design Decisions

### Decision 1: Status Updates by GuardKit, Not RequireKit
**Chosen over**: RequireKit running tests and updating status itself
**Rationale**: RequireKit is a requirements tool, not a test runner. GuardKit owns the execution workflow (task-work, task-complete, AutoBuild). Verification happens naturally during GuardKit's quality gates. RequireKit reads the status back via `/feature-status`.

### Decision 2: `/feature-status` in RequireKit, Not GuardKit
**Chosen over**: Making it a GuardKit command, or available in both
**Rationale**: The product owner (James) uses RequireKit. He shouldn't need to switch tools to see if features are healthy. GuardKit developers can query Graphiti directly or check test results. If needed, a future GuardKit `/feature-status` can be added trivially since the data is in Graphiti.

### Decision 3: Stale Detection Without Auto-Deletion
**Chosen over**: Automatically removing scenarios from Graphiti when missing from `.feature` files
**Rationale**: Scenarios might be temporarily removed during refactoring. Auto-deletion risks losing verification history. The `--prune` flag makes deletion explicit and intentional.

### Decision 4: File-Based Fallback for `/feature-status`
**Chosen over**: Requiring Graphiti for `/feature-status` to work at all
**Rationale**: Walk before running. Even without Graphiti, product owners get value from seeing scenario counts and tag distribution. This lowers the barrier to adoption and provides a natural upgrade path.

---

## References

- `guardkit-requirekit-evolution-strategy.md` — Sections 4.3 (BDD Living Documentation), 7 (Phase 3)
- `guardkit-evolution-spec-kickoff.md` — Spec 5 definition, key questions, output structure
- `generate-bdd.md` — Current `/generate-bdd` command specification (uploaded)
- `FEAT-RK-001-requirekit-v2-refinement-commands.md` — Graphiti integration patterns, group ID strategy, standalone mode
- `TASK-REV-1505-review-report.md` — Graphiti group ID reference, context budget
- `FEAT-GE-001-critical-graphiti-entity-additions.md` — Graphiti entity schema patterns
