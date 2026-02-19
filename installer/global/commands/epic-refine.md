# Epic Refine - Interactive Guided Refinement of Existing Epics

Iteratively improve an existing epic through completeness scoring, targeted questions, and change summaries. Works in both Claude Code and Claude Desktop environments.

## Usage
```bash
/epic-refine <epic-id> [options]
```

## Examples
```bash
# Basic refinement of an epic
/epic-refine EPIC-001

# Focus on scope questions only
/epic-refine EPIC-001 --focus scope

# Focus on success criteria refinement
/epic-refine EPIC-001 --focus criteria

# Focus on risk assessment
/epic-refine EPIC-001 --focus risks

# Focus on dependency identification
/epic-refine EPIC-001 --focus dependencies

# Focus on constraint capture
/epic-refine EPIC-001 --focus constraints

# Focus on organisation pattern assessment
/epic-refine EPIC-001 --focus organisation

# Quick mode: skip prompts, apply AI-suggested improvements automatically
/epic-refine EPIC-001 --quick

# Combine focus and quick for targeted automatic improvements
/epic-refine EPIC-001 --focus scope --quick
```

## Process

When refining an epic, the command follows a three-phase flow:

1. **Phase 1 — Current State Display**: Load the epic markdown file by ID, parse frontmatter and content sections, calculate the current completeness score using the 9-dimension model (from requirements-analyst agent), and display the completeness assessment with visual indicators. Show refinement recommendations based on identified gaps.

2. **Phase 2 — Targeted Questions**: Present questions organised by category, starting with the weakest-scoring categories first. Questions are presented one at a time with clear `[REFINE]` prefix and visual separators. The user can type **skip** to move to the next question or **done** to end the session at any point. Each question includes an example good answer. Natural language is accepted for all answers. After each answer, confirm what was captured.

3. **Phase 3 — Change Summary and Commit**: Display all changes before writing. Show before/after completeness score comparison. Offer apply options: **Yes** (update markdown + Graphiti push), **No** (discard all changes), or **Edit** (manual adjustment). Update the epic markdown in-place, append a `refinement_history` entry to the frontmatter, and push to Graphiti if enabled (with graceful degradation — if Graphiti is unavailable or not configured, the markdown is still saved and the refinement succeeds).

## Phase 1: Current State Display

When the command is invoked:

1. **Load Epic**: Read the epic markdown file from `docs/epics/` by the provided ID
2. **Parse Content**: Extract frontmatter (YAML) and content sections (markdown body)
3. **Calculate Completeness Score**: Evaluate the epic against the 9-dimension model:

| Dimension | Weight | Visual Indicator |
|---|---|---|
| Business Objective | 15% | ✅ Fully addressed / ⚠️ Partially / ❌ Missing |
| Scope | 15% | ✅ Fully addressed / ⚠️ Partially / ❌ Missing |
| Success Criteria | 20% | ✅ Fully addressed / ⚠️ Partially / ❌ Missing |
| Acceptance Criteria | 15% | ✅ Fully addressed / ⚠️ Partially / ❌ Missing |
| Risk | 10% | ✅ Fully addressed / ⚠️ Partially / ❌ Missing |
| Constraints | 10% | ✅ Fully addressed / ⚠️ Partially / ❌ Missing |
| Dependencies | 5% | ✅ Fully addressed / ⚠️ Partially / ❌ Missing |
| Stakeholders | 5% | ✅ Fully addressed / ⚠️ Partially / ❌ Missing |
| Organisation | 5% | ✅ Fully addressed / ⚠️ Partially / ❌ Missing |

4. **Display Assessment**: Present the current score with visual indicators for each dimension
5. **Recommend Refinement**: Highlight the weakest dimensions and suggest starting there

### Score Interpretation

| Score Range | Interpretation |
|---|---|
| 80-100% | ✅ Well-specified, ready for implementation |
| 60-79% | ⚠️ Adequate, refinement recommended |
| 40-59% | ⚠️ Needs significant refinement |
| 0-39% | ❌ Incomplete, refinement required |

## Phase 2: Targeted Questions

Questions are organised into the following categories. When no `--focus` flag is set, the command presents questions from the weakest-scoring categories first, one question at a time.

### Question Categories

#### 1. Scope

**Question**: "What is explicitly out of scope for this epic?"
- **Example good answer**: "Integration with third-party payment providers is out of scope. We will only support our internal billing system for this release."
- **Skip guidance**: Skip if scope boundaries are already well-defined.

**Question**: "Can you describe the boundary between this epic and adjacent epics or features?"
- **Example good answer**: "This epic handles user onboarding only. Account management is covered by EPIC-003 and billing by EPIC-004."
- **Skip guidance**: Skip if the epic has clear, non-overlapping boundaries.

#### 2. Success Criteria

**Question**: "What measurable outcome would indicate this epic is successful?"
- **Example good answer**: "User onboarding completion rate increases from 60% to 85% within 3 months of launch."
- **Skip guidance**: Skip if success criteria already have specific, quantified targets.

**Question**: "How will you know when this epic is done?"
- **Example good answer**: "All 5 features are deployed to production, onboarding funnel conversion exceeds 80%, and zero critical bugs remain open."
- **Skip guidance**: Skip if completion definition is already specific and measurable.

#### 3. Acceptance Criteria

**Question**: "What testable conditions must be met for this epic to be accepted?"
- **Example good answer**: "All user registration paths must complete in under 3 seconds. Email verification must work for Gmail, Outlook, and Yahoo domains. Error messages must be displayed for all validation failures."
- **Skip guidance**: Skip if acceptance criteria are already specific and testable.

#### 4. Dependencies

**Question**: "What external systems, teams, or services does this epic depend on?"
- **Example good answer**: "Depends on the Identity Service team to expose a new /verify endpoint by March 15. Also requires the staging environment to support Redis 7+."
- **Skip guidance**: Skip if all dependencies are already mapped with owners and timelines.

**Question**: "Are there any epics or features that must be completed before this can start?"
- **Example good answer**: "EPIC-002 (database schema migration) must be complete first, as this epic relies on the new user_preferences table."
- **Skip guidance**: Skip if dependency ordering is already established.

#### 5. Risks

**Question**: "What could prevent this epic from being delivered successfully?"
- **Example good answer**: "The upstream authentication API has no SLA, so if it goes down during peak hours, our login flow fails. Mitigation: implement a cached token strategy with 5-minute TTL."
- **Skip guidance**: Skip if risks are already identified with mitigation strategies.

**Question**: "Are there any technical unknowns or unproven approaches?"
- **Example good answer**: "We haven't tested the Graphiti integration at scale. We plan a spike in week 1 to validate performance with 10K episodes."
- **Skip guidance**: Skip if all technical approaches are proven and well-understood.

#### 6. Constraints

**Question**: "What technical, budget, timeline, or regulatory constraints apply to this epic?"
- **Example good answer**: "Must comply with GDPR data residency requirements (EU data stays in EU). Budget limited to 2 engineers for 6 weeks. No new third-party SaaS dependencies allowed."
- **Skip guidance**: Skip if constraints are already documented.

#### 7. Organisation

**Question**: "Does this epic decompose into features, or does it contain tasks directly?"
- **Example good answer**: "This epic has two features (FEAT-001 for UI and FEAT-002 for API), plus two direct tasks for documentation updates that don't warrant a feature wrapper."
- **Skip guidance**: Skip if organisation pattern (direct, features, or mixed) is already defined.

### Organisation Awareness

During the organisation category assessment, the command detects structural patterns and makes recommendations:

- **Large direct-pattern epics (8+ tasks)**: Suggests adding features to group related tasks
- **Single-feature epics**: Suggests flattening to direct pattern since the feature layer adds unnecessary ceremony
- **Mixed pattern**: Suggests consolidation — either group all tasks under features or use direct pattern consistently

### Question UX Design

- **[REFINE] prefix**: Every question prompt is prefixed with `[REFINE]` for clear mode indication
- **Visual separators**: Horizontal rules (`───`) separate each question/answer cycle
- **One question at a time**: Questions are never presented as a list — always single question with clear prompt
- **Natural language accepted**: Users can answer in any format — sentences, bullets, structured text
- **Skip and Done always available**: Every question prompt includes reminder: `(Type 'skip' to skip, 'done' to finish)`
- **Confirmation after capture**: After each answer, display what was captured and how it will update the spec

### --focus Flag

The `--focus` flag restricts questions to a single category. When set, only questions from the specified category are presented. This is useful for targeted refinement sessions:

| Focus Value | Category | Questions |
|---|---|---|
| `--focus scope` | Scope | Scope boundary, adjacent epic boundaries |
| `--focus criteria` | Success Criteria | Measurable outcomes, completion definition |
| `--focus acceptance` | Acceptance Criteria | Testable conditions for epic acceptance |
| `--focus dependencies` | Dependencies | External dependencies, ordering |
| `--focus risks` | Risks | Delivery risks, technical unknowns |
| `--focus constraints` | Constraints | Technical, budget, timeline, regulatory |
| `--focus organisation` | Organisation | Pattern assessment, decomposition |

### --quick Flag

The `--quick` flag enables non-interactive mode. When set, the command:

1. Analyses the current epic content
2. Identifies gaps using the 9-dimension model
3. Generates AI-suggested improvements for each gap
4. Applies all improvements automatically without prompts
5. Displays the before/after comparison for review

This is useful for rapid refinement when the epic has obvious gaps that can be addressed with reasonable defaults.

## Phase 3: Change Summary and Commit

After the question phase completes (user types **done** or all questions answered):

### Change Display
```
[REFINE] Change Summary for EPIC-XXX
═══════════════════════════════════════

Before Completeness: 45%  →  After Completeness: 72%

Changes:
  ✅ Scope: Added out-of-scope items (3 items)
  ✅ Success Criteria: Added 2 measurable outcomes
  ✅ Risks: Added 2 risks with mitigations
  ⚠️ Constraints: No changes (skipped)
  ⚠️ Dependencies: No changes (skipped)

═══════════════════════════════════════
Apply changes? (Yes / No / Edit)
```

### Apply Options
- **Yes**: Update the epic markdown in-place and push to Graphiti (if enabled)
- **No**: Discard all changes — no modifications to the epic file
- **Edit**: Open the changes for manual adjustment before applying

### Markdown Update

When changes are applied:
1. Update the relevant content sections in the epic markdown
2. Update the `completeness_score` in frontmatter
3. Update the `updated` timestamp
4. Append a new entry to `refinement_history` in frontmatter

### Refinement History Schema

Each refinement session appends an entry:

```yaml
refinement_history:
  - date: 2026-02-19T14:30:00Z
    changes:
      - "Added scope boundaries (3 items)"
      - "Added success criteria (2 measurable outcomes)"
      - "Added risk assessment (2 risks with mitigations)"
    completeness_before: 45
    completeness_after: 72
```

### Graphiti Push

After markdown update, push the updated epic to Graphiti knowledge graph:

- **If Graphiti is enabled and available**: Sync the updated epic episode with updated metadata including the new completeness score and refinement history
- **If Graphiti is unavailable or not configured**: Log a warning, save the markdown update, and continue. The refinement succeeds regardless of Graphiti status. This graceful degradation ensures the command works in standalone mode.

## Options

### Refinement Flags
- `--focus <category>` — Restricts questions to a single category (scope, criteria, acceptance, dependencies, risks, constraints, organisation). Limits questions to only those relevant to the specified focus area.
- `--quick` — Skip interactive prompts and apply AI-suggested improvements automatically. Analyses gaps and generates reasonable defaults without user input.

## Output Format

### Successful Refinement
```
[REFINE] Epic Refinement: EPIC-001
═══════════════════════════════════════

📊 Current Completeness: 45%

Dimension Assessment:
  ✅ Business Objective (15%): Clear problem statement
  ⚠️ Scope (15%): Missing out-of-scope items
  ❌ Success Criteria (20%): No measurable outcomes defined
  ⚠️ Acceptance Criteria (15%): Criteria not testable
  ❌ Risk (10%): No risks identified
  ❌ Constraints (10%): No constraints documented
  ✅ Dependencies (5%): External dependencies mapped
  ✅ Stakeholders (5%): Key stakeholders identified
  ⚠️ Organisation (5%): Pattern defined but may need review

═══════════════════════════════════════
Starting targeted questions (weakest areas first)...

[REFINE] Scope — Question 1 of 2
───────────────────────────────────
What is explicitly out of scope for this epic?

Example: "Integration with third-party payment providers is out of scope."
(Type 'skip' to skip, 'done' to finish)
───────────────────────────────────

> User answers...

✓ Captured: Added 3 out-of-scope items to Scope section.

───────────────────────────────────

[... more questions ...]

[REFINE] Change Summary for EPIC-001
═══════════════════════════════════════

Before Completeness: 45%  →  After Completeness: 72%

Changes:
  ✅ Scope: Added out-of-scope items (3 items)
  ✅ Success Criteria: Added 2 measurable outcomes
  ✅ Risks: Added 2 risks with mitigations

═══════════════════════════════════════
Apply changes? (Yes / No / Edit)

> Yes

✅ Epic EPIC-001 updated successfully

📁 File: docs/epics/EPIC-001-user-management.md
📊 Completeness: 45% → 72%
🧠 Graphiti Sync: ✅ Synced (or ⚠️ Skipped — Graphiti not configured)

refinement_history entry appended.

Next Steps:
1. Continue refining: /epic-refine EPIC-001
2. Focus on specific area: /epic-refine EPIC-001 --focus risks
3. View epic status: /epic-status EPIC-001
4. Create features: /feature-create "Feature Name" epic:EPIC-001
```

### Quick Mode Output
```
[REFINE] Quick Refinement: EPIC-001
═══════════════════════════════════════

📊 Before Completeness: 45%

AI-Suggested Improvements:
  ✅ Scope: Added recommended out-of-scope items based on title and context
  ✅ Success Criteria: Generated 2 measurable outcomes from business objective
  ✅ Risks: Identified 3 potential risks from dependency analysis

📊 After Completeness: 68%

═══════════════════════════════════════
Changes applied automatically.

📁 File: docs/epics/EPIC-001-user-management.md
🧠 Graphiti Sync: ✅ Synced
```

### No Changes Needed
```
[REFINE] Epic Refinement: EPIC-001
═══════════════════════════════════════

📊 Current Completeness: 92%

✅ This epic is well-specified and ready for implementation.

All dimensions scored above threshold:
  ✅ Business Objective (15%): Clear and specific
  ✅ Scope (15%): Well-defined boundaries
  ✅ Success Criteria (20%): Measurable outcomes defined
  ✅ Acceptance Criteria (15%): Testable conditions specified
  ✅ Risk (10%): Risks identified with mitigations
  ✅ Constraints (10%): Constraints documented
  ✅ Dependencies (5%): Dependencies mapped
  ✅ Stakeholders (5%): Stakeholders identified
  ✅ Organisation (5%): Pattern defined

No refinement needed. Consider running /epic-status EPIC-001 for full overview.
```

## Validation

Before starting refinement:
- ✅ Epic ID must match an existing epic file in `docs/epics/`
- ✅ Epic file must have valid YAML frontmatter
- ✅ `--focus` value must be one of: `scope`, `criteria`, `acceptance`, `dependencies`, `risks`, `constraints`, `organisation`
- ✅ Epic status must not be `completed` or `cancelled` (warn if refinement attempted)

## Platform Compatibility

This command works in both **Claude Code** and **Claude Desktop** environments:

- **Claude Code**: Full interactive experience with terminal prompts and inline editing
- **Claude Desktop**: Conversational interaction — questions presented as chat messages, answers collected through conversation

The command adapts its interaction style to the platform while maintaining the same three-phase flow and refinement logic.

## Integration with Existing Commands

### Requirements Analyst Agent
The command delegates completeness scoring and question generation to the `requirements-analyst` agent, which has built-in refinement mode support.

### Related Commands
```bash
# Create a new epic (then refine it)
/epic-create "Title" → /epic-refine EPIC-XXX

# View epic status after refinement
/epic-status EPIC-XXX

# Create features for a refined epic
/feature-create "Feature Name" epic:EPIC-XXX

# Formalize requirements linked to the epic
/formalize-ears requirements:[REQ-001,REQ-002]

# Generate BDD scenarios from requirements
/generate-bdd EPIC-XXX
```

## Best Practices

1. **Refine early**: Run `/epic-refine` shortly after `/epic-create` while context is fresh
2. **Use --focus for targeted sessions**: When you know a specific area needs work, use `--focus` to avoid unnecessary questions
3. **Review the change summary**: Always review before applying — the before/after comparison helps validate improvements
4. **Track refinement history**: Each session is recorded in `refinement_history` for audit and progress tracking
5. **Iterate as needed**: Multiple refinement sessions are expected — aim for 80%+ completeness before implementation
6. **Use --quick for obvious gaps**: When the epic has clear missing sections, `--quick` can rapidly fill them in
