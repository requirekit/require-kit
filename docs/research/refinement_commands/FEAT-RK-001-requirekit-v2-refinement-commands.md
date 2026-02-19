# Feature: RequireKit v2 Refinement Commands

> **Feature ID**: FEAT-RK-001
> **Priority**: P1 (Phase 2)
> **Estimated Effort**: 3-5 days
> **Target Repo**: RequireKit
> **Dependencies**: Graphiti infrastructure (FEAT-GR prerequisites), benefits from FEAT-GE-001 (Graphiti entities)

---

## Summary

Add iterative refinement commands (`/epic-refine`, `/feature-refine`) and optional hierarchy flexibility to RequireKit, backed by Graphiti for queryable requirements knowledge. This makes RequireKit usable for James as a product owner — addressing the core problem that `/epic-create` felt like a one-shot operation with no way to iterate — and enables the RequireKit → Graphiti → GuardKit pipeline where refined requirements flow downstream to inform feature planning and task execution.

Additionally, this spec incorporates REQ-004 (Optional Feature Layer), making the feature layer optional so epics can contain tasks directly without an intermediate feature grouping. This matches real-world PM tool behaviour (Jira, Linear, GitHub Projects all support epic → task patterns) and reduces ceremony for small, focused epics.

## Current State

### What Exists
- `/epic-create` — Creates epic markdown files with frontmatter and clarifying questions. Works but feels like a one-shot operation.
- `/feature-create` — Creates feature specifications linked to epics. Good structure but no way to refine after creation.
- `/epic-status`, `/feature-status`, `/hierarchy-view` — Read-only status and visualisation commands.
- `/generate-bdd`, `/formalize-ears`, `/gather-requirements` — Requirements analysis commands (in `.claude/commands/`).
- Agent files: `requirements-analyst.md` (core + ext), `bdd-generator.md` (core + ext).
- File-based storage only — no Graphiti integration, no queryable knowledge graph.

### What's Missing
1. **No refinement capability** — Once created, epics and features can only be manually edited. No guided iterative refinement.
2. **No Graphiti backing** — Requirements exist only as markdown files. GuardKit cannot query them during `/feature-plan` or task execution.
3. **James's UX problem** — James (product owner) couldn't distinguish commands from conversation. No clear "refinement mode" with structured prompts.
4. **Rigid hierarchy** — `EPIC → FEATURE → TASK` is always required. Small epics (3-5 tasks) are forced to create artificial features.
5. **No change tracking** — No summary of what changed during a refinement session.

---

## New Commands

### `/epic-refine`

#### Purpose
Interactive, guided refinement of an existing epic. Shows current state and asks targeted questions about gaps, making it natural for a product owner to start rough and iterate.

#### Arguments
```bash
/epic-refine <epic-id> [options]

# Examples
/epic-refine EPIC-001
/epic-refine EPIC-001 --focus scope        # Focus on scope questions only
/epic-refine EPIC-001 --focus criteria     # Focus on success criteria
/epic-refine EPIC-001 --focus risks        # Focus on risk assessment
/epic-refine EPIC-001 --quick              # Skip prompts, apply AI-suggested improvements
```

#### Interactive Flow

The command operates as a guided conversation in three phases:

**Phase 1: Current State Display**
```
📋 Epic: EPIC-001 — User Management System

Status: planning | Priority: high | Quarter: Q1-2026
Features: 3 defined | Direct Tasks: 0
Last Refined: Never

📊 Completeness Assessment
✅ Business Objective: Defined
✅ Scope (In/Out): Defined
⚠️  Success Criteria: 2 defined (recommend 3-5 measurable criteria)
⚠️  Acceptance Criteria: Generic — need specificity
❌ Risk Assessment: Not defined
❌ Constraints: Not captured
✅ Stakeholders: Defined
⚠️  Dependencies: None listed (verify this is correct)

🔍 Refinement Recommendations:
1. Success criteria need measurable outcomes
2. No risks identified — consider technical and business risks
3. Missing constraints (regulatory, technical, timeline)
```

**Phase 2: Targeted Questions**

Questions are organised into categories and presented based on the completeness assessment. The system asks questions from the weakest categories first.

**Question Categories:**

| Category | When Asked | Example Questions |
|----------|-----------|-------------------|
| **Scope Clarity** | Scope boundaries are vague | "What is explicitly out of scope? Are there grey areas that need a decision?" |
| **Success Criteria** | Fewer than 3 measurable criteria | "How will you know this epic is done? What metrics matter?" |
| **Acceptance Criteria** | Criteria aren't testable | "Can you make this criterion specific enough to test? What does 'fast' mean — under 200ms?" |
| **Dependency Identification** | No dependencies listed | "Does this epic depend on other work completing first? Does it block other epics?" |
| **Risk Assessment** | No risks captured | "What could go wrong? Technical risks? Business risks? Third-party dependencies?" |
| **Constraint Capture** | No constraints listed | "Are there regulatory requirements? Performance budgets? Compliance needs?" |
| **Organisation** | Large epic without features | "This epic has 8+ tasks and no features. Would grouping into features help?" |

Questions are presented **one at a time** with clear prompts, not as a list. Each question includes an example of a good answer and a "skip" option.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Success Criteria Refinement (1 of 3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current criteria:
  1. "System handles user registration"
  2. "Authentication works correctly"

These aren't measurable. A good success criterion includes a metric:
  Example: "User registration completion rate exceeds 85%"
  Example: "Login response time under 500ms at P95"

❓ Can you refine criterion 1 with a measurable target?
   (Type your answer, or 'skip' to move on, or 'done' to finish)
```

**Phase 3: Change Summary and Commit**

After the question phase, display a summary of all changes before writing:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Refinement Summary for EPIC-001
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Changes Made:
  ✏️  Success Criteria: Updated 2 criteria with measurable targets
  ➕ Risk Assessment: Added 3 risks (1 high, 2 medium)
  ➕ Constraints: Added regulatory constraint (GDPR compliance)
  ✏️  Scope: Clarified out-of-scope items

Completeness Score: 45% → 78%

Apply these changes?
  [Y] Yes, update epic and push to Graphiti
  [N] No, discard changes
  [E] Edit — make manual adjustments first
```

#### Output (Markdown + Graphiti)

**Markdown Update**: The epic markdown file is updated in-place. A `refinement_history` block is appended to frontmatter:

```yaml
refinement_history:
  - date: 2026-02-10T14:30:00Z
    changes: ["success_criteria_updated", "risks_added", "constraints_added", "scope_clarified"]
    completeness_before: 45
    completeness_after: 78
```

**Graphiti Update**: Epic content pushed as episode to Graphiti (see Graphiti Integration section below).

---

### `/feature-refine`

#### Purpose
Interactive refinement of an existing feature, with a focus on acceptance criteria specificity, requirements traceability, and BDD scenario coverage.

#### Arguments
```bash
/feature-refine <feature-id> [options]

# Examples
/feature-refine FEAT-001
/feature-refine FEAT-001 --focus acceptance    # Focus on acceptance criteria
/feature-refine FEAT-001 --focus technical     # Focus on technical design
/feature-refine FEAT-001 --focus bdd           # Focus on BDD scenario gaps
```

#### Interactive Flow

Same three-phase pattern as `/epic-refine` (display → questions → summary), with feature-specific question categories:

| Category | When Asked | Example Questions |
|----------|-----------|-------------------|
| **Acceptance Criteria** | Criteria aren't testable or specific | "AC-002 says 'handles errors properly' — what specific errors? What's the expected behaviour?" |
| **Requirements Traceability** | Features lack EARS requirement links | "Which EARS requirements does this feature implement? Should we run `/formalize-ears` to create them?" |
| **BDD Coverage** | Missing or incomplete scenarios | "No BDD scenarios cover the error path. Should we generate scenarios with `/generate-bdd`?" |
| **Technical Considerations** | Architecture decisions missing | "What API endpoints does this feature need? Any performance requirements?" |
| **Dependencies** | No dependency analysis | "Does this feature depend on other features? What must exist first?" |
| **Scope Within Epic** | Scope overlaps with other features | "How does this differ from FEAT-002? Is there overlap to resolve?" |

#### Output
Same pattern as `/epic-refine` — updates feature markdown in-place, appends refinement history, pushes to Graphiti.

---

## Optional Feature Layer (REQ-004 Integration)

### Design Decision

Epics can now organise their work in three ways:

| Pattern | When to Use | Example |
|---------|-------------|---------|
| **Epic → Feature → Task** | Large epics (10+ tasks), natural groupings, team coordination | User Management system with Auth, Profiles, Permissions |
| **Epic → Task** | Small epics (3-5 tasks), bug fixes, tech debt, spikes, solo dev | Fix Auth Bugs epic with 3 direct tasks |
| **Epic → Mixed** | Evolving epics that start simple and grow | Epic starts with direct tasks, features added later |

### Implementation Changes

#### Epic Metadata Schema Update

Add `organisation_pattern` and `direct_tasks` fields to epic frontmatter:

```yaml
---
id: EPIC-002
title: Fix Auth Bugs
status: in_progress
organisation_pattern: direct  # direct | features | mixed
direct_tasks: [TASK-004, TASK-005, TASK-006]
features: []
---
```

Valid combinations:
- `organisation_pattern: direct` → `features: []`, `direct_tasks: [...]`
- `organisation_pattern: features` → `features: [...]`, `direct_tasks: []`
- `organisation_pattern: mixed` → both populated (warning issued recommending consistency)

#### `/epic-status` Enhancement

Update to show both features and direct tasks:

```
📋 Epic: EPIC-002 — Fix Auth Bugs
Status: in_progress | Priority: high | Pattern: direct

Direct Tasks (3):
  🔄 TASK-004: Debug session timeout [in_progress]
  ⏳ TASK-005: Fix password reset [backlog]
  ⏳ TASK-006: Update tests [backlog]

Progress: 33% (1/3 tasks in progress)
```

For mixed epics:
```
📋 Epic: EPIC-003 — Platform Upgrade
Status: in_progress | Pattern: mixed
⚠️  Mixed organisation — consider grouping tasks into features for clarity

Features (1):
  🔄 FEAT-002: UI Redesign (1 task)

Direct Tasks (1):
  ⏳ TASK-008: Upgrade dependencies [backlog]
```

#### `/hierarchy-view` Enhancement

Update tree display to handle all three patterns:

```
EPIC-001: User Management System (features pattern)
├── FEAT-001: User Authentication
│   ├── TASK-001: Implement login [completed]
│   └── TASK-002: Add session handling [in_progress]
└── FEAT-002: Profile Management
    └── TASK-003: Create profile form [backlog]

EPIC-002: Fix Auth Bugs (direct pattern)
├── TASK-004: Debug session timeout [in_progress]
├── TASK-005: Fix password reset [backlog]
└── TASK-006: Update tests [backlog]

EPIC-003: Platform Upgrade (mixed pattern)
├── FEAT-002: UI Redesign
│   └── TASK-007: Update logo [backlog]
└── [Direct Tasks]
    └── TASK-008: Upgrade dependencies [backlog]
```

#### `/epic-refine` Organisation Awareness

During refinement, the system assesses epic organisation and suggests changes:

- **Large direct-pattern epic (8+ tasks)**: "This epic has 12 direct tasks. Consider grouping related tasks into features for better traceability."
- **Single-feature epic**: "This epic has one feature with 3 tasks. Consider flattening to direct tasks to reduce overhead."
- **Mixed pattern**: "This epic has both features and direct tasks. Would you like to consolidate?"

#### Validation Rules

- Task must specify **either** `epic:EPIC-XXX` **or** `feature:FEAT-XXX`, never both
- If `epic:EPIC-XXX` specified, task becomes a direct task of that epic
- If `feature:FEAT-XXX` specified, task belongs to the feature (and transitively to the feature's epic)
- Mixed-pattern epics produce a warning but are valid

#### PM Tool Mapping

| RequireKit Pattern | Jira | Linear | GitHub Projects |
|-------------------|------|--------|-----------------|
| Epic → Feature → Task | Epic → Story → Sub-task | Initiative → Feature → Issue | Milestone → Issue → Linked Issue |
| Epic → Task (direct) | Epic → Story (task promoted) | Initiative → Issue | Milestone → Issue |
| Epic → Mixed | Epic → Stories (both types) | Initiative → mixed Issues | Milestone → Issues |

---

## Graphiti Integration

### Episode Schema for Epics

```python
{
    "name": f"Epic: {epic_title}",
    "episode_body": epic_markdown_content,  # Full epic markdown
    "group_id": f"{project}__requirements",
    "source": EpisodeType.text,
    "source_description": f"RequireKit epic {epic_id}",
    "reference_time": datetime.now(),
    "_metadata": {
        "entity_type": "epic",
        "epic_id": epic_id,
        "status": epic_status,
        "priority": epic_priority,
        "organisation_pattern": "direct|features|mixed",
        "completeness_score": 78,
        "last_refined": "2026-02-10T14:30:00Z",
        "refinement_count": 2,
        "feature_ids": ["FEAT-001", "FEAT-002"],
        "direct_task_ids": [],
        "success_criteria_count": 4,
        "risk_count": 3,
        "has_constraints": True
    }
}
```

### Episode Schema for Features

```python
{
    "name": f"Feature: {feature_title}",
    "episode_body": feature_markdown_content,
    "group_id": f"{project}__requirements",
    "source": EpisodeType.text,
    "source_description": f"RequireKit feature {feature_id}",
    "reference_time": datetime.now(),
    "_metadata": {
        "entity_type": "feature",
        "feature_id": feature_id,
        "epic_id": parent_epic_id,
        "status": feature_status,
        "priority": feature_priority,
        "completeness_score": 65,
        "last_refined": "2026-02-10T15:00:00Z",
        "acceptance_criteria_count": 5,
        "bdd_scenario_ids": ["BDD-001", "BDD-002"],
        "requirement_ids": ["REQ-001", "REQ-002"],
        "task_count": 4
    }
}
```

### Group ID Strategy

Use a single `{project}__requirements` group ID with `entity_type` metadata differentiation rather than separate groups per entity type. Rationale:

- **Simpler**: One group to query for all requirements context
- **Discoverable**: GuardKit's `/feature-plan` queries one group ID
- **Filterable**: `entity_type` metadata enables filtering (epics only, features only, etc.)
- **Consistent**: Matches the pattern established in FEAT-GR-001 where `{project}__feature_specs` uses a single group

Entity types within the group: `epic`, `feature`, `requirement`, `bdd_scenario` (future, from Spec 5).

### Cross-Tool Query Pattern

GuardKit discovers RequireKit's Graphiti data through shared Graphiti instance with project-namespaced group IDs:

```
RequireKit writes → {project}__requirements (epics, features, EARS, BDD)
GuardKit reads  ← {project}__requirements (during /feature-plan, task-work)
```

**Technical implementation**: Both tools connect to the same Graphiti/Neo4j instance. Project namespace (`{project}__`) provides isolation. GuardKit's `/feature-plan` queries:

```python
# In GuardKit's feature-plan command
results = graphiti_client.search(
    query=f"epic {epic_id} requirements acceptance criteria",
    group_ids=[f"{project}__requirements"],
    num_results=5
)
```

This is **read-only from GuardKit's perspective** — GuardKit never writes to the requirements group. RequireKit owns the requirements data.

### RequireKit Standalone Mode

RequireKit can operate with or without Graphiti:

- **Without Graphiti**: All commands work normally using markdown files only. No Graphiti reads or writes. This is the default for users who haven't set up Graphiti.
- **With Graphiti**: Refinement commands additionally push to Graphiti after updating markdown. A `graphiti_enabled` flag in RequireKit config controls this.

```yaml
# .requirekit/config.yaml (or equivalent)
graphiti:
  enabled: false  # Default: off. Set true when Graphiti is available.
  endpoint: "bolt://localhost:7687"
  project_namespace: "my_project"
```

When Graphiti is disabled, refinement commands still work — they just update markdown without the Graphiti push. A message notes: "Tip: Enable Graphiti integration for queryable requirements in GuardKit."

---

## Markdown-Graphiti Sync Strategy

**Principle**: Markdown is authoritative. Graphiti provides queryability.

### Write Flow (Refinement)
1. User runs `/epic-refine EPIC-001`
2. Interactive refinement session produces changes
3. **Markdown updated first** (always)
4. **Graphiti updated second** (if enabled) — upserts the episode using epic_id as the deduplication key
5. If Graphiti write fails, markdown changes are preserved. Warning shown: "Changes saved to markdown. Graphiti sync failed — run `/requirekit-sync` to retry."

### Resync Flow (Recovery)
When markdown and Graphiti drift (e.g., manual markdown edits, Graphiti outage):

```bash
/requirekit-sync [epic-id|feature-id|--all]

# Re-reads markdown files, pushes current state to Graphiti
# Uses upsert logic from FEAT-GR-PRE-003
```

This is a simple, conservative approach — no conflict detection, no merge logic. Markdown wins. Graphiti is rebuilt from markdown.

### When Sync Happens
- **Automatic**: After every `/epic-refine` or `/feature-refine` session
- **Automatic**: After `/epic-create` or `/feature-create` (new in v2)
- **Manual**: Via `/requirekit-sync` for recovery or after manual edits
- **On-demand**: GuardKit can trigger a sync before `/feature-plan` if it detects stale data (future enhancement)

---

## UX Design for Product Owners

### Problem Statement
James couldn't distinguish commands from conversation. He typed free-form text when the system expected a command, and vice versa. The refinement commands must be unambiguous.

### Design Principles for James

1. **Clear Mode Indicators**: Every prompt shows `[REFINE]` prefix and visual separators. The user always knows they're in refinement mode.
2. **One Question at a Time**: Never present a list of questions. Ask one, wait for answer, then ask the next.
3. **Natural Language Accepted**: Questions accept free-form answers. The system parses intent, not syntax.
4. **Skip and Done Are Always Available**: Every question can be skipped. "Done" exits refinement at any point.
5. **Show What Changed**: After each answer, briefly confirm what was captured before moving on.
6. **No CLI Knowledge Required**: The only thing James needs to know is `/epic-refine EPIC-001`. Everything else is guided.

### Command Differentiation

Clear visual separation between command prompts and conversational responses:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[REFINE] Success Criteria (2 of 4)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current: "System handles user registration"

This needs a measurable target. For example:
  "Registration completes in under 3 seconds"

❓ How would you make this measurable?
   (or type 'skip' | 'done')

> User registration should complete end-to-end in under 5 seconds,
  with a 95% success rate on first attempt.

✅ Captured: "Registration completion < 5s, 95% first-attempt success rate"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[REFINE] Success Criteria (3 of 4)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Claude Desktop Compatibility

These commands work in **both Claude Code and Claude Desktop**:
- In Claude Code: Standard slash command invocation
- In Claude Desktop: The command markdown is loaded as context. The interactive flow works via the natural conversation interface — the structured prompts guide the conversation.

The key difference: Claude Code can write files directly. Claude Desktop produces the updated markdown as output that James copies into the file (or a future MCP integration handles the write).

---

## Completeness Scoring

Both `/epic-refine` and `/feature-refine` compute a completeness score to guide the user toward well-defined specifications.

### Epic Completeness Score

| Dimension | Weight | Criteria for Full Score |
|-----------|--------|------------------------|
| Business Objective | 15% | Defined, specific, not generic |
| Scope (In/Out) | 15% | Both in-scope and out-of-scope defined |
| Success Criteria | 20% | 3+ measurable criteria with targets |
| Acceptance Criteria | 15% | Testable, specific criteria |
| Risk Assessment | 10% | At least 2 risks identified with mitigations |
| Constraints | 10% | Regulatory, technical, or timeline constraints captured |
| Dependencies | 5% | Identified or explicitly marked "none" |
| Stakeholders | 5% | Product owner and tech lead identified |
| Organisation | 5% | Features or direct tasks defined (not empty) |

### Feature Completeness Score

| Dimension | Weight | Criteria for Full Score |
|-----------|--------|------------------------|
| Scope Within Epic | 10% | Clear differentiation from other features |
| Acceptance Criteria | 25% | 3+ testable criteria with specific thresholds |
| Requirements Traceability | 20% | Linked to EARS requirements |
| BDD Coverage | 15% | At least 1 scenario per acceptance criterion |
| Technical Considerations | 15% | API, performance, dependencies noted |
| Dependencies | 10% | Feature dependencies identified |
| Test Strategy | 5% | Unit/integration/E2E approach defined |

---

## Acceptance Criteria

### Refinement Commands
- [ ] `/epic-refine EPIC-XXX` launches interactive refinement showing current state and completeness assessment
- [ ] `/feature-refine FEAT-XXX` launches interactive refinement with feature-specific questions
- [ ] Both commands present questions one at a time with skip/done options
- [ ] Both commands display a change summary before applying updates
- [ ] Refinement updates the markdown file in-place and appends refinement history to frontmatter
- [ ] Completeness score is calculated and displayed before and after refinement
- [ ] `--focus` flag restricts questions to a single category
- [ ] Refinement works in both Claude Code and Claude Desktop

### Graphiti Integration
- [ ] When Graphiti is enabled, refinement pushes updated epic/feature episodes after markdown update
- [ ] Episodes use `{project}__requirements` group ID with entity_type metadata differentiation
- [ ] `/requirekit-sync` command re-pushes all markdown content to Graphiti for recovery
- [ ] Graphiti failure does not prevent markdown updates (graceful degradation)
- [ ] RequireKit works fully without Graphiti (standalone mode)

### Optional Feature Layer (REQ-004)
- [ ] Epic frontmatter supports `organisation_pattern: direct|features|mixed` and `direct_tasks` field
- [ ] `/epic-status` displays both features and direct tasks appropriately
- [ ] `/hierarchy-view` renders all three organisation patterns (direct, features, mixed)
- [ ] Mixed-pattern epics produce a warning suggesting consistency
- [ ] `/epic-refine` includes organisation assessment and suggests pattern changes for large or artificial groupings
- [ ] Validation prevents specifying both `epic:` and `feature:` on a task

### James's UX
- [ ] Refinement mode is visually distinct from normal conversation (separators, [REFINE] prefix)
- [ ] Questions accept natural language — no CLI syntax required in answers
- [ ] Each question includes an example of a good answer
- [ ] Change summary shows before/after for each modified field

---

## Testing Approach

### Unit Tests
- Completeness score calculation for epics and features (edge cases: empty fields, partial data)
- Frontmatter parsing and updating (preserve existing fields, add refinement_history)
- Validation logic for organisation patterns (direct, features, mixed, invalid combinations)
- Graphiti episode construction from markdown content

### Integration Tests
- Full refinement flow: load epic → answer questions → verify markdown updated correctly
- Graphiti push: verify episode created/updated with correct metadata after refinement
- Standalone mode: verify refinement works without Graphiti configured
- Sync recovery: manually edit markdown → run `/requirekit-sync` → verify Graphiti matches
- `/epic-status` and `/hierarchy-view` with all three organisation patterns

### Manual Testing (James UX)
- Product owner can run `/epic-refine` and successfully improve an epic without CLI knowledge
- Refinement mode is clearly distinguishable from free conversation
- Skip and done work at every question
- Change summary is accurate and understandable

---

## File Changes

### New Files

| File | Purpose |
|------|---------|
| `installer/global/commands/epic-refine.md` | Epic refinement command definition |
| `installer/global/commands/feature-refine.md` | Feature refinement command definition |
| `installer/global/commands/requirekit-sync.md` | Graphiti sync/recovery command |

### Modified Files

| File | Changes |
|------|---------|
| `installer/global/commands/epic-create.md` | Add `organisation_pattern` and `direct_tasks` to epic template. Add Graphiti push on create. |
| `installer/global/commands/feature-create.md` | Add Graphiti push on create. |
| `installer/global/commands/epic-status.md` | Display direct tasks alongside features. Handle all three organisation patterns. |
| `installer/global/commands/hierarchy-view.md` | Render direct-pattern and mixed-pattern epics in tree view. |
| `installer/global/agents/requirements-analyst.md` | Add refinement mode instructions and completeness scoring logic. |
| `installer/global/agents/requirements-analyst-ext.md` | Add Graphiti integration patterns and sync instructions. |
| `installer/global/instructions/core/00-overview.md` | Document refinement workflow and optional feature layer. |
| `CLAUDE.md` | Add refinement commands and organisation patterns to RequireKit overview. |
| `docs/commands/epics.md` | Document `/epic-refine` and organisation patterns for docs site. |
| `docs/commands/features.md` | Document `/feature-refine` for docs site. |
| `docs/core-concepts/hierarchy.md` | Update hierarchy docs with optional feature layer patterns. |

### New Config File

| File | Purpose |
|------|---------|
| `installer/global/config/graphiti.yaml` (template) | Graphiti configuration template with `enabled: false` default |

---

## Design Decisions and Rationale

### Decision 1: Single `{project}__requirements` Group ID
**Chosen over**: Separate groups per entity type (`{project}__epics`, `{project}__features`)
**Rationale**: Simpler querying for GuardKit — one group retrieves all requirements context. Entity type filtering via metadata handles the rare case where only epics or only features are needed. Consistent with FEAT-GR-001's single-group pattern.

### Decision 2: Markdown Authoritative, Graphiti Secondary
**Chosen over**: Graphiti as primary store, bidirectional sync
**Rationale**: Markdown is human-readable, git-versioned, and works without infrastructure. Graphiti adds queryability but shouldn't be a single point of failure. This matches the established principle from the evolution strategy.

### Decision 3: Graphiti Optional (Standalone Mode)
**Chosen over**: Requiring Graphiti for RequireKit to function
**Rationale**: RequireKit must work independently for users who don't have Graphiti set up. The evolution strategy explicitly says "Don't require RequireKit for GuardKit to work" — the reverse applies too. Graphiti is an enhancement, not a dependency.

### Decision 4: One Question at a Time
**Chosen over**: Presenting all questions in a list, or a form-like interface
**Rationale**: James's UX problem was confusion between commands and conversation. A single-question flow is conversational and unambiguous. It also works naturally in Claude Desktop's chat interface.

### Decision 5: Optional Feature Layer Built into Refinement
**Chosen over**: Separate `/epic-flatten` or `/epic-restructure` commands
**Rationale**: Organisation assessment happens naturally during refinement. The system can suggest flattening or adding features based on epic size and structure. This avoids adding more commands and keeps the workflow guided.

### Decision 6: Completeness Score as Guide, Not Gate
**Chosen over**: Blocking epic/feature progression below a score threshold
**Rationale**: Walk before running. A low completeness score is informational — it shows what's missing and guides the next refinement session. Mandatory gates add friction for solo developers and simple projects.

---

## References

- `guardkit-requirekit-evolution-strategy.md` — Sections 4.2 (RequireKit v2), 6 (DDD), 8 (what not to do)
- `guardkit-evolution-spec-kickoff.md` — Spec 4 definition, key questions, output structure
- `TASK-REV-1505-review-report.md` — Graphiti group ID reference (Appendix B), context budget considerations
- `REQ-004-optional-feature-layer.md` — Full specification for optional feature layer with PM tool mappings
- `installer/global/commands/epic-create.md` — Current epic creation command (pattern reference)
- `installer/global/commands/feature-create.md` — Current feature creation command (pattern reference)
