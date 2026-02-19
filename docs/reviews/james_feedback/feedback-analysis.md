# James Guest Feedback Analysis → Feature Specs for RequireKit

> **Context**: James (CEO/Product Owner) provided initial feedback after using RequireKit on a real project. He ended up "drifting into normal AI chat instead" — which is the critical insight. RequireKit needs to meet PMs where they are, not ask them to become terminal users.
> **Goal**: Map feedback items to feature specs suitable for `/feature-plan` consumption.

---

## Feedback Item Mapping

### What James Asked For vs. What Exists

| # | James's Need | Current State | Covered by FEAT-RK-001? | New Spec Needed? |
|---|---|---|---|---|
| 1 | Pre-session prep template — know questions upfront | `/gather-requirements` jumps straight in with no prep guidance | ❌ No | ✅ Yes |
| 2 | Skip questions, ask for clarity, say "you decide" | No skip/delegate in current commands | ✅ Partly (skip/done in refinement) | ✅ Extend to all commands |
| 3 | Provide example ticket style — "follow this" | No ticket style configuration | ❌ No | ✅ Yes |
| 4 | Feed in existing epics/features for task creation within that structure | `/epic-create` is greenfield only | ❌ No | ✅ Yes |
| 5 | Import proposals, spreadsheets, or existing docs as starting point | No document import capability | ❌ No | ✅ Yes |
| 6 | Define priority defaults/rules for the project | No project-level configuration | ❌ No | ✅ Yes |
| 7 | Jira/Linear ticket import files or direct API | Docs site mentions PM tool export but not implemented | ❌ No | ✅ Yes |
| 8 | Process for updating AI when humans change tickets | FEAT-RK-001 has `/requirekit-sync` for Graphiti | ✅ Partly | ✅ Extend |

---

## Proposed Feature Specs

I'd recommend grouping into **4 feature specs**, ordered by impact on James's "drift to normal chat" problem:

---

### FEAT-RK-002: Session Preparation & Adaptive Conversations

**Why this is #1**: This directly addresses why James drifted away. He didn't know what to prepare, got overwhelmed, and abandoned the structured workflow for free chat. If we solve nothing else, solve this.

**Scope**:

**A) Pre-Session Briefing Pack (`/gather-prep`)**
- New command that generates a markdown template showing every question the session will ask, grouped by category
- James fills it in at his own pace before starting — even partially
- When he then runs `/gather-requirements --from-prep docs/prep.md`, the system skips answered questions and focuses on gaps
- Template includes example answers for each question so James knows what "good" looks like
- Could include a "cheat sheet" of info he should have to hand (stakeholder names, compliance requirements, known constraints etc.)

**B) Adaptive Q&A Across All Commands**
- Every question in every RequireKit command accepts: skip, "explain more", "give me an example", "you decide" (AI makes a sensible default and flags for review)
- "You decide" is the killer feature for James — he described wanting to say "I don't know security levels, but here's my audience" and have the AI infer appropriate defaults
- Progress indicator: "Question 4 of ~12 (Scope Clarity)" so James knows where he is and how much is left
- Category-based flow (from FEAT-RK-001's refinement) applied to initial gathering too

**C) Context-Aware Question Reduction**
- If James provides a prep file or an imported document, the system should recognise what's already answered and skip those questions
- Intelligent follow-up: if the prep file says "B2B SaaS for financial services", don't ask about security level — infer "high" and confirm

**Key Design Decisions to Resolve**:
1. Is `/gather-prep` a separate command or a `--prep` flag on `/gather-requirements`?
2. How does "you decide" work — inline suggestion or collected into a "decisions for review" summary?
3. Should prep templates be project-type-specific (SaaS, mobile app, API) or generic?

---

### FEAT-RK-003: Document Import & Structure Bootstrap

**Why this matters**: James's reality is that projects already have proposals, spreadsheets, and existing structures before RequireKit enters the picture. Forcing him to re-enter everything is a non-starter.

**Scope**:

**A) Document Ingestion (`/import-requirements`)**
- Accepts: markdown, PDF, Word docs, spreadsheets (CSV/XLSX), plain text
- AI parses the document and extracts: project overview, epics/features/tasks, requirements, constraints, stakeholders
- Produces a structured RequireKit hierarchy as draft epics/features
- Shows extracted structure for human review before committing: "I found 3 epics and 12 features — does this look right?"

**B) Existing Structure Adoption**
- `/epic-create --from-import` that takes an imported structure and creates the RequireKit files
- Preserves the original document's organisation so progress tracking aligns with the proposal
- Maps imported items to RequireKit hierarchy: Proposal sections → Epics, Deliverables → Features, Line items → Tasks

**C) Incremental Import**
- Add new documents to an existing project: "Here's the updated proposal with 2 new features"
- Diff against existing structure and propose additions/changes

**Key Design Decisions to Resolve**:
1. What's the minimum viable set of input formats? (Suggest: markdown + PDF + CSV for MVP)
2. How do we handle ambiguous structures — interactive disambiguation or best-guess with review?
3. Should imported documents be stored as reference material alongside the RequireKit files?

---

### FEAT-RK-004: Project Conventions & Configuration

**Why this matters**: James wants RequireKit to conform to his team's existing processes, not the other way around. Ticket style, priority rules, and team conventions should be project-level settings.

**Scope**:

**A) Ticket Style Templates**
- Provide an example ticket and say "follow this style" — the AI learns the format
- `/project-config --ticket-example docs/example-ticket.md`
- Supports: naming conventions, description format, acceptance criteria style, label taxonomy
- The system applies the learned style to all generated tickets

**B) Priority Classification Rules**
- Project-level priority definitions that match the team's conventions
- James's exact example is the default: Normal = most tickets, High = blocking/foundational only, Critical = production issues, Low = nice-to-have
- `/project-config --priorities` with interactive setup or a config file
- Applied automatically during `/feature-plan` task generation

**C) Project Configuration File**
- `.requirekit/config.yaml` (or similar) storing all project conventions
- Ticket style, priority rules, naming patterns, team roles, sprint structure
- Shareable across team members so everyone's AI sessions produce consistent output
- Sensible defaults that work out of the box — configuration is optional enhancement

**Key Design Decisions to Resolve**:
1. Config file format — YAML, TOML, or frontmatter in a markdown file (matching RequireKit's markdown-first philosophy)?
2. Should ticket style be learned from examples or explicitly configured?
3. How granular do priority rules get — just defaults, or conditional rules like "API endpoints are always high priority"?

---

### FEAT-RK-005: PM Tool Export & Change Reconciliation

**Why this matters**: The output needs to go somewhere useful. Tickets sitting in markdown files aren't actionable for a PM who lives in Jira/Linear. And when the team changes tickets in sprint planning, RequireKit needs to know.

**Scope**:

**A) Export to PM Tools (`/export-tickets`)**
- Phase 1 (MVP): CSV export compatible with Jira and Linear import formats
- Phase 2: JSON export for GitHub Issues API, Azure DevOps
- Phase 3: Direct API integration (Jira REST, Linear GraphQL)
- Export should respect the project's priority configuration and ticket style
- Includes epic/feature hierarchy mapping to each PM tool's structure (from FEAT-RK-001's PM tool mapping table)

**B) Change Reconciliation (`/reconcile-changes`)**
- After sprint planning, team takes a CSV/export from their PM tool and feeds it back
- System diffs against RequireKit's state and shows: new tickets, modified tickets, removed tickets, priority changes, status updates
- PM confirms which changes to apply to RequireKit's source of truth
- Optionally updates Graphiti knowledge graph (building on FEAT-RK-001's sync)

**C) Bidirectional Awareness (Future)**
- Track which tickets have been exported and where
- When RequireKit refinement changes tickets that are already in a PM tool, flag them for re-export
- Webhook or polling for direct API integrations to detect external changes

**Key Design Decisions to Resolve**:
1. MVP: CSV-only or include at least one API integration?
2. Which PM tools to prioritise? James uses Jira — should that be the first-class citizen?
3. How does reconciliation handle conflicts when both RequireKit and the PM tool changed the same ticket?

---

## Recommended Implementation Order

```
FEAT-RK-002 (Session Prep & Adaptive) ←── Highest impact, solves the "drift" problem
    ↓
FEAT-RK-003 (Document Import)         ←── Removes the biggest friction: re-entering existing work
    ↓
FEAT-RK-004 (Project Conventions)     ←── Polish: makes output match team expectations
    ↓
FEAT-RK-005 (Export & Reconciliation) ←── Completes the loop: RequireKit ↔ PM tools
```

**FEAT-RK-001** (already specced — refinement commands) can be implemented in parallel with FEAT-RK-002, as they touch different commands but share the adaptive conversation UX pattern.

---

## Cross-Cutting Concerns

**"You Decide" Pattern**: This appears in James's feedback for one specific case (security levels) but it's a universal PM need. It should be a first-class interaction pattern across all RequireKit commands, not buried in one feature spec.

**Progressive Complexity**: James shouldn't need to configure anything to get started. Defaults should be sensible, prep templates optional, and conventions only needed when he wants the output to match an existing team process.

---

## Deployment Strategy: Claude Code First → CoWork for PMs

James's "scary terminal" problem isn't just a UX issue — it's a fundamental persona mismatch. RequireKit has two distinct user types with different needs:

| | Rich (Developer) | James (PM/Product Owner) |
|---|---|---|
| **Primary tool** | Claude Code (terminal) | Doesn't want a terminal at all |
| **Comfort level** | Slash commands, config files, git | Drag-and-drop, chat, file upload |
| **What they need** | Commands that integrate with dev workflow | Guided conversations that produce structured output |
| **Where they work** | In the codebase | In documents, spreadsheets, Slack, Jira |

### Phase 1: Claude Code Plugin (Core Implementation)

All RequireKit commands are implemented as Claude Code plugin components first. This is where the logic lives and where the developer persona consumes them:

- Slash commands (`/gather-requirements`, `/gather-prep`, `/import-requirements`, etc.)
- Agent files (requirements-analyst, bdd-generator)
- Skills (SKILL.md for workflow automation)
- Hooks (quality validation on requirement changes)
- MCP configuration (Graphiti integration, PM tool export)

This matches the plugin architecture analysis from December 2025 — RequireKit already maps cleanly to Claude Code plugin components.

### Phase 2: CoWork Skill/Plugin (James's Interface)

CoWork is Anthropic's beta desktop tool for non-developers. It's oriented around file operations and task management — which is exactly what James needs. A CoWork skill wraps RequireKit's core capabilities in a PM-friendly interface:

**What CoWork gives James that Claude Code doesn't:**
- Drag-and-drop file import (proposals, spreadsheets, existing docs)
- No terminal, no slash commands — just natural conversation
- Desktop-native file management (save requirements to specific folders)
- Visual, non-intimidating interface

**Potential CoWork Skills for RequireKit:**

| Skill | What James Does | What Happens Behind the Scenes |
|---|---|---|
| "Start a new project" | Drags in a proposal PDF, answers guided questions | CoWork runs `/gather-requirements --from-prep` against the parsed document |
| "Refine requirements" | Opens existing epic, answers targeted questions | CoWork runs `/epic-refine` with the conversation mapped to structured inputs |
| "Export to Jira" | Clicks export, reviews tickets | CoWork runs `/export-tickets --format jira-csv` and saves the file |
| "Import sprint changes" | Drags in Jira CSV export | CoWork runs `/reconcile-changes` and shows diff for review |

### How This Changes the Spec Design

Every feature spec should define two interaction surfaces:

1. **Claude Code surface**: Slash command with flags, structured output, developer-friendly
2. **CoWork surface**: Natural language trigger, file-based I/O, guided conversation

The core logic is shared — the difference is the interaction layer. This means:

- FEAT-RK-002 (Session Prep): Claude Code gets `/gather-prep` command; CoWork gets a "Prepare for requirements session" skill that produces the same prep template as a downloadable file
- FEAT-RK-003 (Document Import): Claude Code gets `/import-requirements path/to/file.pdf`; CoWork gets drag-and-drop import with the same parsing engine
- FEAT-RK-004 (Conventions): Claude Code gets `.requirekit/config.yaml`; CoWork gets "Show me an example ticket" with the AI learning from it
- FEAT-RK-005 (Export): Claude Code gets `/export-tickets --format jira-csv`; CoWork gets "Export my tickets for Jira" → saves CSV to desktop

### Implementation Sequencing

```
Phase 1: Claude Code Plugin (all four features)
    ↓
    Core logic proven, commands working, tests passing
    ↓
Phase 2: CoWork Skill Layer
    ↓
    Thin wrapper over same core, file-based I/O,
    natural language triggers, James-tested
```

This follows your established "walk before running" pattern — get the core right in the tool you control (Claude Code), then wrap it for the persona who needs a different interface (CoWork).

### Open Questions for CoWork Integration

1. **CoWork skill authoring**: Is the CoWork skill format documented enough to build custom skills today, or is it still too early in beta?
2. **MCP access from CoWork**: Can CoWork skills invoke MCP servers (needed for Graphiti integration and PM tool APIs)?
3. **Shared state**: If James refines requirements in CoWork and Rich runs `/feature-plan` in Claude Code, do they see the same data? (Answer: yes, if both read from the same markdown files and Graphiti instance)
4. **CoWork marketplace**: Is there a distribution mechanism for CoWork skills similar to Claude Code plugins?

---

## Next Steps

1. **Pick 1-2 specs to develop first** — I'd recommend FEAT-RK-002 and FEAT-RK-003 as the highest-impact pair
2. **Flesh out the chosen specs** into full feature spec format (matching the FEAT-SP-001 / FEAT-RK-001 pattern) with acceptance criteria, testing approach, file changes, and design decisions
3. **Define the Claude Code command surface AND CoWork skill surface** for each spec
4. **Run through `/feature-plan`** to decompose into implementation tasks
5. **Research current CoWork skill authoring** — confirm feasibility for Phase 2 before locking in the architecture
