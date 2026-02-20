# Feature: Session Preparation & Adaptive Conversations

> **Feature ID**: FEAT-RK-002
> **Priority**: P1 (Phase 2 — Highest impact)
> **Estimated Effort**: 5-8 days
> **Target Repo**: RequireKit
> **Dependencies**: Benefits from FEAT-RK-001 (refinement commands share adaptive conversation UX), independent of Graphiti
> **Personas**: James (PM/Product Owner via CoWork), Rich (Developer via Claude Code)

---

## Summary

Add pre-session preparation and adaptive conversation patterns to RequireKit, directly addressing why James abandoned the structured workflow and drifted into normal AI chat. A new `/gather-prep` command generates a fillable briefing template that James completes asynchronously — at his own pace, potentially with stakeholder input — before starting a requirements session. When he then runs `/gather-requirements --from-prep`, the system skips answered questions, focuses on gaps, and uses context from the prep file to intelligently reduce and adapt the remaining conversation.

Additionally, this spec introduces the **"You Decide" pattern** as a first-class interaction across all RequireKit commands: at any question, the user can ask the AI to infer a sensible default and confirm it inline. Combined with progress indicators, skip/done controls, and context-aware question reduction, this transforms RequireKit from a rigid Q&A interrogation into an adaptive conversation that meets product owners where they are.

---

## Problem Statement

James's core feedback: he ended up "drifting into normal AI chat instead" of using RequireKit's structured commands. Root causes identified from the feedback analysis:

1. **No preparation guidance** — `/gather-requirements` jumps straight into questions with no indication of what to prepare, what information to have to hand, or how long the session will take
2. **No escape hatches** — Every question demands an answer. No way to skip, delegate to AI, or say "I don't know this, but here's related context"
3. **No progress visibility** — James had no sense of where he was in the process or how much remained
4. **No context awareness** — Even when James provides rich information early, the system doesn't use it to reduce or adapt later questions
5. **Terminal intimidation** — The slash-command interface felt alien to a PM (addressed by CoWork deployment, but the UX patterns in this spec make both surfaces work)

---

## Current State

### What Exists
- `/gather-requirements` — Starts an interactive Q&A session with Discovery → Exploration → Validation phases. No prep stage, no adaptive skipping, no progress indicators.
- `/epic-refine` and `/feature-refine` (FEAT-RK-001) — Have skip/done controls and one-at-a-time question flow, but only in refinement mode. Not applied to initial gathering.
- `requirements-analyst` agent — Has refinement mode with completeness scoring and question templates. No "You Decide" pattern, no prep file integration, no context-aware reduction.
- `requirements-analyst-ext.md` — Contains question templates by category with example answers and skip guidance. Good foundation but not exposed as a pre-session briefing.

### What's Missing
1. **Pre-session briefing** — No way to see questions upfront, prepare answers offline, or involve stakeholders before the live session
2. **"You Decide" pattern** — No mechanism for the user to delegate a decision to AI with contextual inference
3. **Progress indicators** — No visibility into session progress (question N of ~M, category tracking)
4. **Context-aware question reduction** — No intelligence to skip questions already answered by prep files, imported documents, or earlier answers
5. **Adaptive conversation controls** — skip/done exist in refinement but not in `/gather-requirements` or other commands
6. **Cheat sheet / info checklist** — No guidance on what information to have ready before starting

---

## New Commands

### `/gather-prep`

#### Purpose
Generate a pre-session briefing template that the user fills in at their own pace before starting a requirements gathering session. This is an asynchronous preparation step — not a live conversation.

#### Arguments
```bash
/gather-prep [options]

# Examples
/gather-prep                                    # Generic template
/gather-prep --project "PoA Platform"           # Named project, generic template
/gather-prep --context docs/proposal.md         # Generate template informed by existing doc
/gather-prep --sections "scope,users,security"  # Only include specific sections
```

#### Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--project <name>` | Project name included in template header | None |
| `--context <path>` | Path to existing document. AI reads it and pre-fills answers where possible, leaving gaps for the user | None |
| `--sections <list>` | Comma-separated list of sections to include. Omitted sections are excluded from the template | All sections |
| `--output <path>` | Output path for the generated template | `docs/requirements/prep/[project-or-date]-prep.md` |

#### Generated Template Structure

The template is a markdown file with YAML frontmatter and clearly structured sections. Each section contains numbered questions with example answers and a space for the user's response.

```markdown
---
id: PREP-[TIMESTAMP]
project: [Project Name or "Untitled"]
created: [DATE]
status: draft
sections_included: [list]
context_source: [path if --context used, null otherwise]
---

# Requirements Preparation — [Project Name]

> Fill in what you can. Leave blanks for anything you're unsure about — the live session
> will focus on gaps. Partial answers are valuable. For any question, you can write
> "you decide" and the AI will infer a sensible default during the session.
>
> **Estimated session time**: ~15-25 minutes (less if this prep is thorough)

## Info Checklist

Before starting, it helps to have these to hand:
- [ ] Names and roles of key stakeholders
- [ ] Any existing documents (proposals, spreadsheets, specs)
- [ ] Known constraints (budget, timeline, compliance, tech stack)
- [ ] Target users and their primary pain points
- [ ] Success metrics or KPIs if known
- [ ] Examples of similar products or features (if applicable)

---

## Section 1: Project Overview (4 questions)

### 1.1 What problem does this project solve?
> **Example**: "Our legal team spends 3 hours per case manually checking Power of Attorney
> documents against regulatory requirements. We need to automate the validation."

**Your answer**:


### 1.2 Who are the primary users?
> **Example**: "Paralegals who process 20-30 PoA documents per day, and senior solicitors
> who review flagged cases."

**Your answer**:


### 1.3 What does success look like?
> **Example**: "Document processing time reduced from 3 hours to 30 minutes per case,
> with 95% accuracy on automated checks."

**Your answer**:


### 1.4 What is the project timeline or key deadline?
> **Example**: "MVP needed by Q3 2026 to meet regulatory deadline. Full launch Q1 2027."

**Your answer**:


---

## Section 2: Scope & Boundaries (3 questions)

### 2.1 What must be included in the first release?
> **Example**: "Document upload, automated validation against OPG rules, flagging of
> issues, and a dashboard showing processing status."

**Your answer**:


### 2.2 What is explicitly out of scope?
> **Example**: "Integration with court filing systems. Multi-language support.
> Mobile app — web only for MVP."

**Your answer**:


### 2.3 Are there related systems or projects this connects to?
> **Example**: "Integrates with our existing case management system (Clio) and the
> OPG's online registration portal."

**Your answer**:


---

## Section 3: Users & Stakeholders (3 questions)

### 3.1 Who are the stakeholders and what are their interests?
> **Example**: "Sarah (Head of Legal) — sponsor, cares about compliance. Tom (IT Director)
> — needs it to run on existing Azure infrastructure. James (Product) — owns the roadmap."

**Your answer**:


### 3.2 What are the different user roles and their needs?
> **Example**: "Paralegal: needs fast document processing. Solicitor: needs review dashboard
> with flagged items. Admin: needs user management and audit logs."

**Your answer**:


### 3.3 How technically confident are the end users?
> **Example**: "Paralegals are comfortable with web apps but not technical. Solicitors
> prefer simple interfaces. No one wants to use a terminal."

**Your answer**:


---

## Section 4: Constraints & Requirements (4 questions)

### 4.1 What technical constraints exist?
> **Example**: "Must run on Azure UK South for data sovereignty. Must use .NET for
> backend (existing team skills). No new SaaS dependencies without IT approval."

**Your answer**:


### 4.2 What compliance or regulatory requirements apply?
> **Example**: "GDPR — all personal data stays in UK. Must meet OPG's digital
> submission standards. Audit trail required for all document processing."

**Your answer**:


### 4.3 What is the budget or resource situation?
> **Example**: "2 developers for 6 months. £50k infrastructure budget. No budget for
> additional hires but can use contractors for frontend."

**Your answer**:


### 4.4 Are there security requirements?
> **Example**: "you decide — our users are legal professionals handling sensitive
> personal data including health information"

**Your answer**:


---

## Section 5: Features & Priorities (3 questions)

### 5.1 What are the key features you envision?
> **Example**: "1. Document upload and parsing, 2. Automated validation rules engine,
> 3. Review dashboard with issue flagging, 4. Export/reporting for compliance audits"

**Your answer**:


### 5.2 How would you rank these features by importance?
> **Example**: "Upload & validation are must-haves. Dashboard is important. Reporting
> is nice-to-have for MVP."

**Your answer**:


### 5.3 Are there features from a competitor or similar product you'd like to emulate?
> **Example**: "The way DocuSign handles document routing is close to what we need
> for the approval workflow."

**Your answer**:


---

## Section 6: Risks & Unknowns (2 questions)

### 6.1 What could go wrong or block this project?
> **Example**: "OPG might change their digital submission rules mid-project.
> The Clio API might not support the data we need to extract."

**Your answer**:


### 6.2 What don't you know yet that you need to find out?
> **Example**: "Not sure if OPG has an API or if we need to screen-scrape.
> Don't know the volume of documents at peak (holiday periods)."

**Your answer**:

---

## Notes

_Add anything else that doesn't fit the sections above._


```

#### Context-Aware Pre-Fill (`--context`)

When `--context` is provided, the AI reads the referenced document and:

1. Extracts information that maps to template questions
2. Pre-fills answers with `[From: document.md]` attribution
3. Marks pre-filled answers with a review indicator: `✅ Pre-filled — review and edit if needed`
4. Leaves questions unanswerable from the document blank
5. Adds a summary at the top: "Pre-filled 8 of 19 questions from proposal.md. 11 remaining."

Example pre-filled answer:
```markdown
### 1.1 What problem does this project solve?
> ✅ Pre-filled from proposal.md — review and edit if needed

**Your answer**: Legal teams spend an average of 3 hours per Power of Attorney case
manually validating documents against OPG requirements. The error rate on manual
checks is approximately 12%, leading to rejected submissions and delays.
[From: proposal.md, Section 2.1]
```

#### Output Location

Default: `docs/requirements/prep/[project-slug]-prep.md`

If `--project` is not specified: `docs/requirements/prep/[YYYY-MM-DD]-prep.md`

---

### Modified Command: `/gather-requirements`

#### New Flag: `--from-prep`

```bash
/gather-requirements --from-prep docs/requirements/prep/poa-platform-prep.md
```

When `--from-prep` is provided:

1. **Load and parse** the prep file, extracting all answered questions
2. **Calculate coverage**: "Prep file covers 14 of 19 questions. Focusing on 5 gaps."
3. **Skip answered questions** — Do not re-ask questions that have substantive answers in the prep file
4. **Use prep context for inference** — If the prep mentions "legal professionals handling sensitive personal data", use that to inform security-related questions and defaults
5. **Handle "you decide" markers** — Any prep answer containing "you decide" triggers the AI inference pattern (see below) during the live session, with the prep context informing the inference
6. **Validate pre-filled answers** — Briefly confirm key pre-filled answers: "Your prep says this is a B2B SaaS for financial services — should I base security assumptions on that?" (one confirmation, not re-asking every question)

#### Progress Indicators (All Modes)

Whether or not `--from-prep` is used, `/gather-requirements` now displays progress:

```
[GATHER] Section 2 of 6: Scope & Boundaries — Question 1 of 3
─────────────────────────────────────────────────────────────
What must be included in the first release?

(skip | explain more | give me an example | you decide | done)
─────────────────────────────────────────────────────────────
```

Progress elements:
- **Section N of M**: Which category group is active
- **Question N of ~M**: Approximate question count (may adapt based on answers)
- **Category name**: What area the current question covers
- **Available actions**: Always shown as a reminder on every question

---

## The "You Decide" Pattern

This is the signature UX innovation of FEAT-RK-002 — a first-class interaction pattern where the user delegates a decision to the AI, which infers a sensible default using available context and presents it inline for confirmation.

### How It Works

At any question in any RequireKit command, the user types "you decide" (or variants: "AI decide", "your call", "best guess", "infer this").

The AI then:

1. **Gathers context** from the current session, prep file, and any imported documents
2. **Infers a recommendation** based on the available information
3. **Presents it inline** with reasoning and a confidence indicator
4. **Asks for confirmation** with options to accept, modify, or override

### Inline Response Format

```
[GATHER] Section 4 of 6: Constraints — Question 4 of 4
─────────────────────────────────────────────────────────────
Are there security requirements?

(skip | explain more | give me an example | you decide | done)
─────────────────────────────────────────────────────────────

> you decide — our users are legal professionals handling sensitive personal data

🤖 AI Recommendation (confidence: high):
   Based on your context — legal professionals, sensitive personal data including
   health information, UK-based B2B — I'd recommend:

   • Authentication: Multi-factor authentication required
   • Data encryption: At rest (AES-256) and in transit (TLS 1.3)
   • Data residency: UK only (GDPR + legal data sovereignty)
   • Access control: Role-based with audit logging
   • Compliance: GDPR, potentially ICO certification
   • Session management: 30-minute timeout, no persistent sessions

   Reasoning: Legal + health data = high sensitivity. UK B2B = GDPR mandatory.
   Regulatory environment (OPG) implies audit requirements.

   ✅ Accept  |  ✏️ Modify  |  ❌ Override with my own answer
─────────────────────────────────────────────────────────────
```

### Confidence Levels

| Level | When Used | Display |
|-------|-----------|---------|
| **High** | Strong contextual signals (e.g., "legal + health data" → security = high) | 🤖 confidence: high |
| **Medium** | Reasonable inference but assumptions involved | 🤖 confidence: medium — please review |
| **Low** | Weak signals, mostly defaults | 🤖 confidence: low — consider providing more context |

### Accepted Trigger Phrases

The pattern activates on any of these (case-insensitive):
- "you decide"
- "AI decide" / "ai decide"
- "your call"
- "best guess"
- "infer this"
- "default"
- "suggest something"
- "I don't know, but..." (followed by context)

### Context Sources for Inference

When making a recommendation, the AI draws from (in priority order):

1. **Explicit context in the current answer** — "you decide — our users handle sensitive health data"
2. **Prep file answers** — Previously filled sections that provide project context
3. **Earlier session answers** — Questions already answered in the current session
4. **Imported documents** — If document import (FEAT-RK-003) has been used
5. **Domain knowledge** — General best practices for the inferred project type
6. **Graphiti knowledge** — If available, project-level context from the knowledge graph

### Recording "You Decide" Decisions

All AI-inferred decisions are marked in the output requirements document:

```markdown
### NFR-004: Security Requirements
**Source**: AI-inferred (accepted by user)
**Confidence**: High
**Context used**: "legal professionals handling sensitive personal data including health information"
**Inferred**:
- Multi-factor authentication required
- Data encryption at rest (AES-256) and in transit (TLS 1.3)
- UK data residency (GDPR + legal data sovereignty)
- Role-based access control with audit logging
```

This attribution ensures traceability — anyone reviewing the requirements can see which decisions were human-provided and which were AI-inferred.

---

## Adaptive Conversation Controls

These controls apply to **all** RequireKit interactive commands — not just `/gather-requirements`. This includes `/epic-create`, `/feature-create`, `/epic-refine`, `/feature-refine`, `/formalize-ears`, and `/generate-bdd`.

### Standard Controls (Every Question)

| Control | Trigger | Behaviour |
|---------|---------|-----------|
| **skip** | "skip", "next", "pass" | Move to next question, mark as unanswered |
| **done** | "done", "that's enough", "finish" | End the interactive session, proceed to summary |
| **explain more** | "explain", "what do you mean", "?" | Provide additional context about the question |
| **give me an example** | "example", "show me" | Display a concrete example answer |
| **you decide** | See trigger phrases above | AI inference pattern |
| **go back** | "back", "previous", "undo" | Return to the previous question |

### Category Navigation

In addition to linear flow, users can jump between categories:

```
> jump to risks

[GATHER] Jumping to Section 6: Risks & Unknowns — Question 1 of 2
```

### Session Persistence

If the user types **done** or the session is interrupted:

1. All answers so far are saved to a session file: `docs/requirements/sessions/[session-id].md`
2. The session can be resumed: `/gather-requirements --resume [session-id]`
3. Session files include progress state (which questions were answered, skipped, or pending)

Session file structure:
```yaml
---
session_id: SESSION-20260220-143000
project: poa-platform
started: 2026-02-20T14:30:00Z
last_updated: 2026-02-20T14:45:00Z
status: in_progress
prep_file: docs/requirements/prep/poa-platform-prep.md
progress:
  total_questions: 19
  answered: 11
  skipped: 2
  ai_inferred: 3
  remaining: 3
  current_section: 4
  current_question: 2
---
```

---

## Context-Aware Question Reduction

When the session has access to prior context (prep files, imported documents, earlier answers), the system intelligently reduces the question set.

### Reduction Rules

1. **Direct answer match**: If a prep file directly answers a question, skip it (with brief confirmation of the pre-filled value)
2. **Implicit answer**: If earlier answers imply the answer to a later question, skip and confirm. Example: if Section 1 says "B2B SaaS for UK financial services" and Section 4 asks about compliance, the system can say "Based on your earlier answer, I'm assuming FCA compliance is relevant — correct?"
3. **"You decide" pre-fills**: If the prep file says "you decide" for a question, the AI runs the inference at session start and presents the inferred answer for confirmation rather than re-asking the question
4. **Redundant questions**: If multiple questions would elicit the same information, ask only the most comprehensive one
5. **Follow-up adaptation**: After each answer, evaluate whether upcoming questions are still relevant. If the user says "no external integrations", skip all integration-related questions

### Reduction Summary

At session start (when `--from-prep` is used):

```
[GATHER] Session Preparation Summary
═══════════════════════════════════════

📄 Loaded prep file: poa-platform-prep.md
✅ Pre-answered: 14 of 19 questions
🤖 AI will infer: 2 questions (marked "you decide" in prep)
❓ Remaining gaps: 3 questions

Estimated session time: ~5-8 minutes (reduced from ~20 minutes)

Starting with gap questions...
═══════════════════════════════════════
```

---

## Integration Points

### With FEAT-RK-001 (Refinement Commands)

FEAT-RK-001's `/epic-refine` and `/feature-refine` already implement skip/done and one-at-a-time question flow. FEAT-RK-002 extends this by adding:

- **"You Decide" pattern** — Available in refinement questions, not just gathering
- **Progress indicators** — "Question 2 of ~5 (Scope Clarity)" in refinement mode
- **explain more / example** — Additional controls beyond skip/done

The adaptive conversation controls defined here become the shared UX pattern across all interactive RequireKit commands. The requirements-analyst agent is updated once, and all commands benefit.

### With FEAT-RK-003 (Document Import — Future)

When document import is implemented:
- Imported documents become a context source for `/gather-prep --context`
- Imported structure feeds into context-aware question reduction
- `/gather-requirements` can use imported documents alongside prep files

### With FEAT-RK-004 (Project Conventions — Future)

When project conventions are implemented:
- Prep templates can incorporate project-specific question sections
- "You Decide" inferences can respect project priority rules and conventions
- Generated requirements follow the project's ticket style

### CoWork Interaction Surface

For James using CoWork (not Claude Code):

- **Prep workflow**: "I need to plan a new feature" → CoWork generates the prep template as a file James fills in → He drops it back and the guided session begins conversationally
- **"You Decide" in conversation**: James says "I don't know the security level, but here's my audience" → CoWork responds with the inline inference, James confirms or adjusts
- **Progress visibility**: CoWork shows progress naturally in conversation flow

The underlying logic is identical — the commands and agent encode the methodology, and both Claude Code and CoWork consume the same patterns.

### Requirements-Analyst Agent

The requirements-analyst agent (`requirements-analyst.md`) is the primary integration point. All adaptive conversation behaviour is encoded in the agent so that any command invoking it gets the full FEAT-RK-002 UX. Changes to the agent propagate to all commands.

---

## Acceptance Criteria

### `/gather-prep` Command

- [ ] Running `/gather-prep` generates a valid markdown prep template with all 6 default sections
- [ ] Template includes YAML frontmatter with id, project, created, status, sections_included
- [ ] Every question includes an example answer showing what "good" looks like
- [ ] Info checklist at the top lists what information to have ready
- [ ] `--project` flag sets the project name in header and filename
- [ ] `--sections` flag limits output to specified sections only
- [ ] `--context` flag reads the provided document and pre-fills answerable questions with `[From: filename]` attribution
- [ ] `--context` pre-fill reports coverage: "Pre-filled N of M questions from document.md"
- [ ] Template saves to `docs/requirements/prep/` by default
- [ ] `--output` flag overrides the save location
- [ ] Template is valid markdown that renders correctly in any markdown viewer

### `/gather-requirements --from-prep`

- [ ] Loading a prep file correctly parses all answered and unanswered questions
- [ ] Answered questions are skipped in the live session
- [ ] "you decide" markers in the prep file trigger AI inference at session start
- [ ] Pre-filled answers receive brief confirmation ("Your prep says X — correct?") not re-asking
- [ ] Coverage summary displayed at session start: questions answered, to infer, remaining
- [ ] Estimated session time adjusts based on prep coverage
- [ ] Session works correctly with no prep file (standard `/gather-requirements` behaviour preserved)

### Adaptive Conversation Controls

- [ ] All 6 controls (skip, done, explain more, example, you decide, go back) work in `/gather-requirements`
- [ ] All 6 controls work in `/epic-create` interactive flow
- [ ] All 6 controls work in `/feature-create` interactive flow
- [ ] skip/done/you decide work in `/epic-refine` and `/feature-refine` (extending existing skip/done)
- [ ] Controls accept natural language variants (e.g., "next" for skip, "?" for explain)
- [ ] Available actions reminder displayed with every question prompt

### Progress Indicators

- [ ] "Section N of M: [Category Name]" displayed with each question
- [ ] "Question N of ~M" displayed with each question (approximate, as count may adapt)
- [ ] Progress updates correctly when questions are skipped
- [ ] Progress updates correctly when context-aware reduction removes questions

### "You Decide" Pattern

- [ ] Typing "you decide" triggers AI inference with contextual recommendation
- [ ] Recommendation includes confidence level (high/medium/low)
- [ ] Recommendation shows reasoning and context sources used
- [ ] User can accept, modify, or override the recommendation
- [ ] All accepted trigger phrases work (you decide, your call, best guess, etc.)
- [ ] AI-inferred decisions are attributed in the output document with source, confidence, and context
- [ ] "you decide" works in all interactive commands, not just gather-requirements
- [ ] When context is thin, AI shows low confidence and suggests providing more information

### Context-Aware Question Reduction

- [ ] Questions directly answered in prep file are skipped with brief confirmation
- [ ] Implicit answers from earlier questions reduce later questions (e.g., B2B SaaS → infer compliance)
- [ ] "you decide" pre-fills from prep are resolved at session start, not re-asked
- [ ] Redundant questions are merged — only the most comprehensive version is asked
- [ ] Follow-up questions adapt based on previous answers (e.g., "no integrations" → skip integration questions)

### Session Persistence

- [ ] Interrupted sessions save progress to `docs/requirements/sessions/[session-id].md`
- [ ] `/gather-requirements --resume [session-id]` restores session state correctly
- [ ] Session file includes progress metadata (answered, skipped, remaining, current position)
- [ ] Completed sessions have status: completed in the session file

---

## Testing Approach

### Unit Tests

- **Prep template generation**: Verify template contains all sections, correct frontmatter, valid markdown
- **Prep template with `--sections`**: Verify only specified sections are included
- **Prep template with `--context`**: Verify pre-fill extraction from sample documents (markdown, text)
- **Prep file parsing**: Verify answered vs unanswered questions are correctly identified
- **"You decide" marker detection**: Verify all trigger phrases are recognised
- **Progress calculation**: Verify section/question counters are correct across skip, answer, reduction scenarios
- **Session file serialisation/deserialisation**: Verify session state round-trips correctly
- **Context-aware reduction logic**: Given a set of answered questions, verify correct questions are marked for skipping

### Integration Tests

- **Full prep → gather flow**: Generate prep, fill in answers, run `--from-prep`, verify skipped questions and gap focus
- **"You Decide" end-to-end**: Trigger "you decide" with context, verify inference quality, accept, verify attribution in output
- **Session resume**: Start session, interrupt at question 8, resume, verify state is correct
- **Adaptive controls across commands**: Verify skip/done/explain/example/you-decide/back work in gather-requirements, epic-create, feature-create
- **Context-aware reduction**: Provide prep file with 14/19 answers, verify session only asks ~5 questions
- **No prep fallback**: Verify `/gather-requirements` without `--from-prep` works identically to current behaviour

### Manual Testing (James UX — Critical)

These are the make-or-break tests. James should be able to:

1. **Run `/gather-prep`** and understand what to fill in without any guidance from Rich
2. **Fill in the prep template** at his own pace, leaving gaps and marking "you decide" where uncertain
3. **Run `/gather-requirements --from-prep`** and experience a significantly shorter session focused on gaps
4. **Use "you decide"** during the live session and receive useful AI inferences based on his context
5. **See progress** at all times and feel in control of the pace
6. **Skip questions** without guilt or friction
7. **Resume an interrupted session** without losing progress
8. **Not confuse** the structured interaction with free-form chat — mode indicators should make it clear

---

## File Changes

### New Files

| File | Purpose |
|------|---------|
| `installer/global/commands/gather-prep.md` | Pre-session briefing template generation command |
| `installer/global/templates/prep/generic-prep-template.md` | Base template with all sections and example answers |
| `docs/commands/gather-prep.md` | Documentation for the `/gather-prep` command |

### Modified Files

| File | Changes |
|------|---------|
| `installer/global/commands/gather-requirements.md` | Add `--from-prep` and `--resume` flags. Add progress indicators. Add adaptive controls (skip, done, explain more, example, you decide, go back). Add session persistence. |
| `installer/global/commands/epic-create.md` | Add adaptive conversation controls to interactive question flow (skip, done, explain more, example, you decide, go back). Add progress indicators. |
| `installer/global/commands/feature-create.md` | Add adaptive conversation controls to interactive question flow. Add progress indicators. |
| `installer/global/commands/epic-refine.md` | Add "you decide", "explain more", "example", "go back" controls (skip/done already exist). Add progress indicators. |
| `installer/global/commands/feature-refine.md` | Add "you decide", "explain more", "example", "go back" controls (skip/done already exist). Add progress indicators. |
| `installer/global/agents/requirements-analyst.md` | Add "You Decide" pattern specification. Add context-aware question reduction logic. Add progress indicator format. Add session persistence schema. Update interaction controls to include full adaptive set. |
| `installer/global/agents/requirements-analyst-ext.md` | Add prep file parsing instructions. Add context inference patterns for "You Decide". Add question reduction rules. Add session file format specification. |
| `installer/global/instructions/core/00-overview.md` | Document prep → gather workflow. Document adaptive conversation pattern. |
| `CLAUDE.md` | Add `/gather-prep` to command list. Document `--from-prep` and `--resume` flags. |
| `docs/commands/requirements.md` | Update `/gather-requirements` documentation with new flags and adaptive controls. |

### New Directories

| Path | Purpose |
|------|---------|
| `docs/requirements/prep/` | Storage for generated prep templates |
| `docs/requirements/sessions/` | Storage for session state files (interrupted/resumable sessions) |
| `installer/global/templates/prep/` | Prep template source files |

---

## Design Decisions

### DD-001: Separate `/gather-prep` Command
**Chosen over**: `--prep` flag on `/gather-requirements`
**Rationale**: Prep is a fundamentally asynchronous workflow step. James fills it over hours or days, potentially involving stakeholders. A separate command makes this a distinct, nameable action that maps cleanly to CoWork ("prepare me for a planning session") and doesn't muddy `/gather-requirements` with two operational modes.

### DD-002: Inline "You Decide" with Immediate Confirmation
**Chosen over**: Collected summary at end; Hybrid inline + summary
**Rationale**: James needs immediate confidence that the AI understood his context. Seeing the inference right away lets him correct misunderstandings in-place rather than discovering them in a review at the end. This matches the conversational flow James naturally expects — he says something, AI responds, he confirms.

### DD-003: Generic Template with Optional Sections
**Chosen over**: Project-type-specific templates; Generic base + type add-ons
**Rationale**: Avoids maintenance burden of multiple templates. Stays true to "progressive complexity" — works out of the box with zero configuration. The AI adapts section depth based on what James tells it about the project via `--context`, rather than requiring him to categorise the project upfront. If project-type templates become valuable later, they can be added as `--type` flag options without changing the core workflow.

### DD-004: Session Persistence via Markdown Files
**Chosen over**: In-memory only; Database-backed sessions
**Rationale**: Markdown session files are inspectable, editable, and git-trackable — consistent with RequireKit's markdown-first philosophy. No infrastructure dependency. Users can manually edit session files if needed. The tradeoff is no concurrent session support, which isn't needed for the target workflow.

### DD-005: Adaptive Controls in Agent, Not Commands
**Chosen over**: Duplicating control logic in each command file
**Rationale**: The requirements-analyst agent is invoked by all interactive commands. Encoding the adaptive conversation pattern in the agent means updating it once propagates to all commands. Command files reference the agent for interaction handling rather than reimplementing controls. This matches FEAT-RK-001's approach where the agent owns refinement logic.

---

## Key Questions for James's Review

1. **Prep template length**: The generic template has 19 questions across 6 sections. Is this the right level of detail, or would James prefer fewer questions with more depth?

2. **"You Decide" confidence**: When AI confidence is low, should it still make a recommendation (with caveats) or should it say "I need more context — can you tell me about X?"

3. **Session interruption**: If James closes CoWork mid-session, should the system auto-save (assuming he wants to resume) or should it prompt "Save progress before leaving?"

4. **Prep stakeholder sharing**: Would James want to share the prep template with other stakeholders to fill in their sections? If so, should we add section ownership (e.g., "Section 4: Constraints — assigned to Tom, IT Director")?

5. **Question ordering**: Should the live session always follow the template order, or should it dynamically reorder based on what gaps remain and their priority?

---

## Implementation Notes

### Phasing Within FEAT-RK-002

If the full scope is too large for a single implementation pass, it can be phased:

**Phase A (Core — 3-4 days)**:
- `/gather-prep` command with generic template
- `/gather-requirements --from-prep` with question skipping
- Progress indicators on all interactive commands
- Adaptive controls (skip, done, explain more, example, go back) on all interactive commands

**Phase B (Intelligence — 2-3 days)**:
- "You Decide" pattern with inline inference
- Context-aware question reduction (implicit answers, redundancy removal)
- `--context` flag on `/gather-prep` for document-informed pre-fill

**Phase C (Persistence — 1 day)**:
- Session save/resume
- `--resume` flag on `/gather-requirements`

### Token Budget Considerations

The prep template and session files are lightweight (< 2K tokens each). The main token consideration is the "You Decide" pattern, which requires the AI to load context from multiple sources for inference. Recommendation: cap context assembly for inference at 4K tokens, prioritising explicit user context over domain knowledge.

---

## References

- `docs/reviews/james_feedback/james-feedback-analysis-v2.md` — Source feedback analysis and feature mapping
- `docs/research/refinement_commands/FEAT-RK-001-requirekit-v2-refinement-commands.md` — Shared UX patterns, refinement mode, Graphiti integration
- `installer/global/agents/requirements-analyst.md` — Agent that owns interaction logic
- `installer/global/agents/requirements-analyst-ext.md` — Question templates and refinement patterns
- `installer/global/commands/epic-refine.md` — Existing skip/done and three-phase flow patterns
- `installer/global/commands/gather-requirements.md` — Command being extended
