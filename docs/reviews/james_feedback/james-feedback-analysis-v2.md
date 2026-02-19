# James Guest Feedback Analysis → Feature Specs for RequireKit

> **Context**: James (CEO/Product Owner) provided initial feedback after using RequireKit on a real project. He ended up "drifting into normal AI chat instead" — which is the critical insight. RequireKit needs to meet PMs where they are, not ask them to become terminal users.
> **Goal**: Map feedback items to feature specs suitable for `/feature-plan` consumption.
> **Related**: `requirekit-cowork-plugin-analysis.md` (CoWork deployment strategy)

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

Four feature specs, ordered by impact on James's "drift to normal chat" problem:

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

**Interaction Surfaces**:
- **Claude Code**: `/gather-prep` command, `--from-prep` flag on `/gather-requirements`
- **CoWork**: James types "I need to plan a new feature" → CoWork produces the prep template as a file he fills in → he drops it back in and the guided session begins conversationally

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

**Interaction Surfaces**:
- **Claude Code**: `/import-requirements path/to/proposal.pdf`
- **CoWork**: James drags a proposal PDF into Cowork, gives the project folder access, says "create requirements from this proposal" → Cowork parses, shows structure, iterates conversationally

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

**Interaction Surfaces**:
- **Claude Code**: `/project-config` command, `.requirekit/config.yaml` file
- **CoWork**: "Show me an example ticket from the last project" → James drops one in → "Use this style for all tickets" → methodology skill learns the pattern

---

### FEAT-RK-005: PM Tool Export & Change Reconciliation

**Why this matters**: The output needs to go somewhere useful. Tickets sitting in markdown files aren't actionable for a PM who lives in Jira/Linear. And when the team changes tickets in sprint planning, RequireKit needs to know.

**Scope**:

**A) Export to PM Tools (`/export-tickets`)**
- Phase 1 (MVP): CSV export compatible with Jira and Linear import formats
- Phase 2: JSON export for GitHub Issues API, Azure DevOps
- Phase 3: Direct API integration via MCP connectors (Jira REST, Linear GraphQL)
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
- MCP connectors for direct integration (aligns with CoWork Phase 2/3)

**Key Design Decisions to Resolve**:
1. MVP: CSV-only or include at least one API integration?
2. Which PM tools to prioritise? James uses Linear in the CoWork analysis — should that be the first-class citizen?
3. How does reconciliation handle conflicts when both RequireKit and the PM tool changed the same ticket?

**Interaction Surfaces**:
- **Claude Code**: `/export-tickets --format linear-csv`, `/reconcile-changes path/to/export.csv`
- **CoWork Phase 1**: "Export my tickets for Linear" → saves CSV to project folder
- **CoWork Phase 2+**: MCP connector to Linear → "Create these tickets in Linear" → done directly, no CSV intermediary

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

**"You Decide" Pattern**: This appears in James's feedback for one specific case (security levels) but it's a universal PM need. It should be a first-class interaction pattern across all RequireKit commands, not buried in one feature spec. Recommended home: baked into FEAT-RK-002 as the primary spec, with the pattern documented in the requirements-analyst agent so it propagates to all commands.

**Progressive Complexity**: James shouldn't need to configure anything to get started. Defaults should be sensible, prep templates optional, and conventions only needed when he wants the output to match an existing team process.

---

## Deployment Strategy: Claude Code First → CoWork Plugin for PMs

James's "scary terminal" problem isn't just a UX issue — it's a fundamental persona mismatch. RequireKit has two distinct user types:

| | Rich (Developer) | James (PM/Product Owner) |
|---|---|---|
| **Primary tool** | Claude Code (terminal) | CoWork (desktop, conversational) |
| **Comfort level** | Slash commands, config files, git | Drag-and-drop, chat, file upload |
| **What they need** | Commands that integrate with dev workflow | Guided conversations that produce structured output |
| **Where they work** | In the codebase | In documents, spreadsheets, Slack, Linear |

### The CoWork Plugin Architecture

From the `requirekit-cowork-plugin-analysis.md`, the plugin structure is already defined:

```
requirekit-plugin/
├── .claude-plugin/
│   └── plugin.json              # Manifest: name, version, description
├── .mcp.json                    # Connectors: Linear, GitHub, NATS (future)
├── commands/
│   ├── feature-plan.md          # /requirekit:feature-plan
│   ├── system-plan.md           # /requirekit:system-plan
│   └── feature-build.md         # /requirekit:feature-build
└── skills/
    └── requirements-engineering/
        └── SKILL.md             # Core methodology, spec format,
                                 # task decomposition rules
```

The critical insight: **plugins are just markdown files and folders — no compiled code, no build step.** The SKILL.md encodes our methodology so Claude understands how to decompose epics, structure waves, score complexity, and produce properly formatted specs.

### Three-Phase Deployment

**Phase 1: Skill + Commands (~1-2 days effort)**
- Plugin with RequireKit methodology encoded as a CoWork skill
- Claude reads system plan from the project folder, applies methodology, generates specs locally
- James's workflow: Use CoWork → generate specs → Rich reviews and feeds into pipeline
- **This is where FEAT-RK-002 and FEAT-RK-003 have the most impact** — the prep template and document import are natural CoWork interactions

**Phase 2: MCP Server Integration (alongside pipeline work)**
- MCP server wrapping RequireKit's core functions, running on the Dell ProMax via Tailscale
- James's CoWork session can trigger real `feature_plan` executions, create Linear tickets, publish NATS events
- **This is where FEAT-RK-005 comes alive** — export isn't a CSV download, it's a direct Linear integration

**Phase 3: Full Pipeline Integration (future)**
- MCP server exposes complete pipeline status back into CoWork
- James tracks features from ideation through to "In Review" without leaving CoWork
- **This is where FEAT-RK-004's conventions really matter** — consistent ticket formatting across the full pipeline

### How This Changes the Implementation Sequencing

```
Step 1: Claude Code commands (FEAT-RK-002, 003)
    ↓  Core logic proven, methodology encoded, tests passing
    
Step 2: CoWork plugin Phase 1 (SKILL.md + commands wrapping same methodology)
    ↓  James tests against real feature planning scenario
    ↓  ~1-2 days effort because it's just markdown wrapping proven logic
    
Step 3: Claude Code commands (FEAT-RK-004, 005)
    ↓  Conventions and export working in developer workflow
    
Step 4: CoWork plugin Phase 2 (MCP connectors for Linear, pipeline events)
    ↓  James gets direct integration, no more CSV intermediary
```

The key principle: **the SKILL.md in the CoWork plugin and the command markdown in Claude Code encode the same methodology.** When we improve the requirements-analyst agent or add the "you decide" pattern in FEAT-RK-002, both surfaces benefit because they share the underlying approach.

### Content & Release Opportunity

A RequireKit CoWork plugin could be released publicly as part of the "building in public" strategy. Requirements engineering plugins don't yet exist in the CoWork marketplace — this would be the first opinionated, methodology-driven approach to AI-assisted feature planning. This aligns with the Product Management plugin Anthropic already ships, but goes deeper into the technical planning side.

---

## Next Steps

1. **Flesh out FEAT-RK-002 and FEAT-RK-003** into full feature spec format (matching the FEAT-SP-001 / FEAT-RK-001 pattern) with acceptance criteria, testing approach, file changes, and design decisions
2. **Define both interaction surfaces** (Claude Code commands + CoWork skill triggers) for each spec
3. **Run through `/feature-plan`** to decompose into implementation tasks
4. **Scaffold the CoWork plugin** in parallel — the SKILL.md can start encoding methodology immediately while the Claude Code commands are being built
5. **James tests CoWork plugin Phase 1** against a real feature planning scenario to validate the approach before investing in Phase 2 MCP work
