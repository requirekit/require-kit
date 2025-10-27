# TASK-030D Implementation Guide
## Quick Reference Cards - Developer Handbook

**Purpose**: Practical guide for implementing TASK-030D quick reference cards
**Audience**: Developer assigned to create the 8 cards
**Status**: Ready for implementation

---

## Quick Start Checklist

Before you start, confirm you have:
- [ ] Task description (TASK-030D-create-quick-reference-cards.md)
- [ ] Full requirements analysis (TASK-030D-REQUIREMENTS-ANALYSIS.md)
- [ ] EARS requirements (TASK-030D-EARS-REQUIREMENTS.md)
- [ ] This implementation guide
- [ ] Source documentation access:
  - [ ] TASK-030A (command specifications)
  - [ ] TASK-005 through TASK-029 (implementation specs)
  - [ ] docs/guides/agentecflow-lite-workflow.md
  - [ ] docs/workflows/*.md files
  - [ ] installer/global/commands/*.md files

---

## Content Sources by Card

### Card 1: task-work-cheat-sheet.md (150 lines)
**Scope**: Most comprehensive - covers ALL phases and flags

**Source Material**:
- installer/global/commands/task-work.md (primary)
- TASK-005: Complexity evaluation (Phase 2.7 details)
- TASK-006: Design-first flags (--design-only, --implement-only)
- TASK-007: Test enforcement (Phase 4.5 details)
- TASK-025: Plan audit (Phase 5.5 details)
- TASK-026: Task-refine command (Phase 6)
- TASK-027: Markdown plans (plan format)
- TASK-028: Enhanced checkpoint display (Phase 2.8)
- TASK-029: Plan modification (Phase 2.8 [M]odify option)

**Key Content Sections**:
1. **Phase Overview Table** (6 phases)
   - Phase 1: Load Task Context
   - Phase 2: Implementation Planning
   - Phase 2.5A: Pattern Suggestion
   - Phase 2.5B: Architectural Review
   - Phase 2.7: Complexity Evaluation
   - Phase 2.8: Human Checkpoint
   - Phase 3: Implementation
   - Phase 4: Testing
   - Phase 4.5: Fix Loop
   - Phase 5: Code Review
   - Phase 5.5: Plan Audit

2. **Flags Quick Reference** (table format)
   - --design-only
   - --implement-only
   - --micro
   - --with-context
   - --sync-progress
   - --review
   - Combinations that work together

3. **State Transitions** (diagram or table)
   - BACKLOG → IN_PROGRESS → IN_REVIEW → COMPLETED
   - DESIGN_APPROVED state
   - BLOCKED state transitions
   - When each state occurs

4. **Common Errors** (quick resolution table)
   - Compilation failures
   - Test failures
   - Missing plan files
   - State issues

**Challenge**: Fitting all 8 features into 150 lines
**Strategy**: Use reference tables; link to other cards for detailed info

**Template Suggestion**:
```markdown
# Task Work Cheat Sheet

## Overview
Quick reference for all /task-work phases, flags, and state transitions.

## Phase Overview
| Phase | Purpose | Trigger | Outcome |
|-------|---------|---------|---------|
| 1 | Load context | Command start | Context loaded |
| 2 | Plan implementation | Phase 1 complete | .md plan created |
| ... | | | |

## Flags Quick Reference
| Flag | Use Case | Prerequisites | Incompatible With |
|------|----------|---|---|
| --design-only | Design without impl | — | --implement-only |
| ... | | | |

## State Transitions
BACKLOG → IN_PROGRESS → IN_REVIEW → COMPLETED
Special: DESIGN_APPROVED (after --design-only)

## See Also
[Other 7 cards]
```

---

### Card 2: complexity-guide.md (100 lines)
**Scope**: Deep dive on complexity scoring (clearest source material)

**Source Material**:
- TASK-005: Complexity evaluation in task-create
- TASK-008: Feature-generate-tasks with complexity control
- CLAUDE.md "Task Complexity Evaluation" section

**Key Content Sections**:
1. **Complexity Scoring Factors** (0-10 scale)
   - File complexity (0-3 points)
   - Pattern familiarity (0-2 points)
   - Risk assessment (0-3 points)
   - External dependencies (0-2 points)

2. **Complexity Levels and Thresholds**
   - 1-3: Simple (🟢)
   - 4-6: Medium (🟡)
   - 7-8: Complex (🔴)
   - 9-10: Very Complex (🔴)

3. **Breakdown Strategies**
   - Horizontal (by layers)
   - Vertical (by features)
   - Technical (by concern)
   - Temporal (by phases)

4. **Examples by Complexity**
   - Simple (complexity 2): Typo fix, doc update
   - Medium (complexity 5): API endpoint, feature
   - Complex (complexity 8): Event sourcing, migration
   - Very complex (complexity 10): Multi-system refactor

**Visual**: Complexity scoring table or flowchart

**Straightforward**: Good source documentation exists; no ambiguity

---

### Card 3: design-first-workflow-card.md (100 lines)
**Scope**: When to use --design-only vs --implement-only

**Source Material**:
- TASK-006: Design-first workflow (primary)
- CLAUDE.md "Design-First Workflow" section
- docs/guides/agentecflow-lite-workflow.md (if exists)

**Key Content Sections**:
1. **Flag Usage Decision Tree**
   - When to use --design-only (complexity ≥7)
   - When to use --implement-only (design pre-approved)
   - Default workflow (no flags)

2. **State Machine**
   - BACKLOG → DESIGN_APPROVED (via --design-only)
   - DESIGN_APPROVED → IN_PROGRESS (via --implement-only)
   - Normal path: BACKLOG → IN_PROGRESS

3. **Common Patterns**
   - Architect-led design (architect uses --design-only, developer uses --implement-only)
   - Multi-day workflow (design day 1, implement day 2)
   - High-risk changes (design approval before implementation)

4. **Examples**
   - Complex task (complexity 8): Use --design-only first
   - Pre-designed task: Use --implement-only
   - Simple task: Use default workflow

**Visual**: State transition diagram

---

### Card 4: quality-gates-card.md (100 lines)
**Scope**: All quality gates and fix loop (combines TASK-007 and TASK-025)

**Source Material**:
- TASK-007: 100% test pass enforcement
- TASK-025: Phase 5.5 plan audit
- CLAUDE.md "Quality Gates" section

**Key Content Sections**:
1. **Quality Gates Overview** (table format)
   - Compilation (100% success)
   - Tests Pass (100%)
   - Line Coverage (≥80%)
   - Architectural Review (≥60/100)
   - Plan Audit (0 violations)

2. **Phase 4.5: Fix Loop** (critical feature)
   - Automatic test failure analysis
   - Up to 3 fix attempts
   - Compilation verification before testing
   - BLOCKED if all attempts fail

3. **Phase 5.5: Plan Audit** (scope creep detection)
   - Planned vs actual comparison
   - File count variance
   - LOC variance thresholds
   - Decision options: Approve/Review/Escalate

4. **Escalation Decision Tree**
   - When to approve
   - When to request revisions
   - When to escalate
   - When to reject

**Visual**: Fix loop flowchart, escalation decision tree

**Challenge**: Combining two phases (4.5 and 5.5) in one card
**Strategy**: Use subsections; phase 4.5 is automatic, phase 5.5 is manual decision

---

### Card 5: refinement-workflow-card.md (100 lines)
**Scope**: /task-refine command (lightest dependency - single source)

**Source Material**:
- TASK-026: /task-refine command (primary)
- CLAUDE.md "Iterative Refinement" section
- docs/guides/iterative-refinement-guide.md (if exists)

**Key Content Sections**:
1. **/task-refine Usage**
   - Command syntax: `/task-refine TASK-XXX "description"`
   - When to use refinement vs re-work
   - Preserves context (plan, review, audit)

2. **When to Refine vs Re-Work Decision Tree**
   - Refine: Minor improvements, linting, naming
   - Re-work: New features, architecture changes, breaking changes

3. **Refinement Workflow**
   - Current state requirement: IN_REVIEW or COMPLETED
   - Multiple refinement cycles supported
   - Each refinement cycle re-runs quality gates
   - Context preserved between cycles

4. **Examples**
   - Scenario 1: Improve variable naming and add comments
   - Scenario 2: Extract helper functions
   - Scenario 3: Add type hints
   - Scenario 4: Fix linting issues

**Straightforward**: Single source, clear purpose, limited scope

---

### Card 6: markdown-plans-card.md (100 lines)
**Scope**: Markdown plan format and benefits (single source)

**Source Material**:
- TASK-027: Markdown plans (primary)
- CLAUDE.md "Markdown Implementation Plans" section

**Key Content Sections**:
1. **Markdown Plan Format**
   - Human-readable vs JSON
   - File location: .claude/task-plans/{task_id}-implementation-plan.md
   - Sections: Files to Create, Implementation Phases, Risks

2. **Benefits of Markdown Plans**
   - Git diffs show meaningful changes
   - Easy to read and review
   - Can be manually edited before implementation
   - Searchable with standard tools

3. **Manual Editing Workflow**
   - Load plan with --design-only
   - Edit plan file manually
   - Run /task-work with --implement-only
   - System uses edited plan

4. **Examples**
   - Example plan structure
   - Git diff improvements (before/after JSON vs Markdown)
   - Migration from JSON (if applicable)

**Simple and Clear**: Good existing documentation

---

### Card 7: phase28-checkpoint-card.md (100 lines) - NEW
**Scope**: Enhanced Phase 2.8 checkpoint display (TASK-028)

**Source Material**:
- TASK-028: Enhanced Phase 2.8 checkpoint display
- Example output from TASK-028 implementation

**Key Content Sections**:
1. **Enhanced Checkpoint Display**
   - Rich visual format showing plan details
   - File summary section
   - Dependencies section
   - Risks section
   - Effort estimates section

2. **Plan Summary Format**
   - Files to create/modify
   - Dependencies and versions
   - Risk level assessment
   - Time/LOC estimates

3. **Truncation Rules**
   - Long file lists truncated with "...and X more"
   - Dependency list truncation
   - Risk severity levels

4. **Review Mode Display**
   - AUTO_PROCEED (simple tasks, no checkpoint)
   - QUICK_OPTIONAL (medium tasks, 30s timeout)
   - FULL_REQUIRED (complex tasks, must approve)

5. **Integration with Markdown Plans**
   - Display works with both JSON and Markdown plans
   - Markdown plans show clearer formatting
   - Graceful handling of missing plans

**Challenge**: Feature is newer; may need example extraction from tests
**Source**: TASK-028 implementation and test files

---

### Card 8: plan-modification-card.md (100 lines) - NEW
**Scope**: Interactive plan modification at Phase 2.8 (TASK-029)

**Source Material**:
- TASK-029: Interactive plan modification
- Example output from TASK-029 implementation

**Key Content Sections**:
1. **[M]odify Option at Phase 2.8 Checkpoint**
   - Phase 2.8 menu options: [A]pprove, [M]odify, [S]implify, [R]eject, [P]ostpone
   - [M]odify triggers interactive modification mode

2. **4 Modification Categories**
   - **Files**: Add/remove files to create or modify
   - **Dependencies**: Add/remove/modify external dependencies
   - **Risks**: Add/remove/modify identified risks with severity
   - **Effort**: Adjust estimates (duration, LOC, complexity score)

3. **Version Management**
   - Automatic version increment on save
   - Timestamped backups: plan-TASK-XXX-v1.md, plan-TASK-XXX-v2.md, etc.
   - Undo functionality: revert to previous version

4. **When to Modify vs Other Options**
   - Modify: Plan needs adjustment but concept is sound
   - Approve: Plan is ready as-is
   - Simplify: Plan is too complex, request breakdown
   - Reject: Plan needs fundamental redesign
   - Postpone: Save design for later

5. **Examples**
   - Scenario 1: Add missing dependency during review
   - Scenario 2: Adjust effort estimates based on clarification
   - Scenario 3: Update identified risks with new information
   - Scenario 4: Undo modification that wasn't quite right

**Challenge**: Newer feature; need examples from implementation
**Source**: TASK-029 implementation and test files

---

## Implementation Steps

### Step 1: Preparation (15 minutes)
```
1. Get answers to clarification questions (from FINDINGS-SUMMARY)
   [ ] Diagram format preference (ASCII, Mermaid, tables?)
   [ ] See Also reference scope (minimal, standard, comprehensive?)
   [ ] Acceptable overlap between cards? (recommend: yes)
   [ ] Task-work card line limit flexible? (recommend: yes to 175)

2. Organize source materials
   [ ] Create /tmp/task-030d-sources/ directory
   [ ] Download/copy all source documentation
   [ ] Note page/section references for each card

3. Set up directory
   [ ] Create docs/quick-reference/ (if doesn't exist)
   [ ] Create .claude/task-plans/ (for implementation plan if needed)
```

### Step 2: Create Infrastructure Cards (45 minutes)
**Start with clearest sources - builds momentum**

Cards in order of source clarity:
1. **Card 2** (complexity-guide.md): Single clean source, clear structure
2. **Card 3** (design-first-workflow-card.md): Single source, clear purpose
3. **Card 6** (markdown-plans-card.md): Single source, straightforward
4. **Card 5** (refinement-workflow-card.md): Single source, well-documented

**Process for each card**:
```
a) Extract content from source documentation
b) Organize into template structure:
   - Overview (1-2 sentences)
   - Quick Reference (table or bullets)
   - Decision Guide (tree or flowchart)
   - Examples (2-3 scenarios)
   - See Also (references)

c) Add visual diagram if needed (6+ cards required)
d) Verify against acceptance criteria
e) Commit with message: "Create {card-name}.md - Extract from TASK-XXX"
```

### Step 3: Create Complex Integration Cards (30 minutes)
**Cards that combine multiple sources**

1. **Card 4** (quality-gates-card.md): Combines TASK-007 (Phase 4.5) + TASK-025 (Phase 5.5)
   - Use subsections to separate phases
   - Phase 4.5 is automatic; Phase 5.5 is decision point
   - Include decision trees for escalation

2. **Card 7** (phase28-checkpoint-card.md): New feature TASK-028
   - Extract example output from TASK-028 tests if available
   - Document display format and truncation
   - Show integration with Markdown plans

3. **Card 8** (plan-modification-card.md): New feature TASK-029
   - Extract example interaction from TASK-029 implementation
   - Document 4 modification categories clearly
   - Include version management details

### Step 4: Create Integration Card (20 minutes)
**Most complex - integrates all other cards**

**Card 1** (task-work-cheat-sheet.md): All features integrated
- Use reference tables for space efficiency
- Link to cards 2-8 for detailed information
- Include state machine diagram
- Common errors troubleshooting table

**Tight space constraint** (150 lines for 8 features):
- Keep Overview minimal (2 lines)
- Use tables extensively
- Use See Also to reference deeper content
- Focus on quick lookup, not complete information

### Step 5: Quality Review (10 minutes)

**Cross-Reference Validation**:
```markdown
For each card:
- [ ] Verify all See Also links are valid
- [ ] Test links in Markdown viewer
- [ ] Check for circular references
- [ ] Links use consistent format
```

**Print Test**:
```
1. Print each card on 8.5" x 11" paper
2. Verify all content visible (nothing cut off)
3. Verify diagrams readable in print
4. Verify font size adequate (≥10pt equivalent)
5. Works in black and white
```

**Completeness Check**:
```
For each card:
- [ ] Template structure complete
- [ ] All required sections present
- [ ] Overview is 1-2 sentences
- [ ] Quick Reference uses table or bullets
- [ ] Decision Guide is visual (tree or flowchart)
- [ ] Examples are 2-3 scenarios
- [ ] See Also has 3-7 references
- [ ] Line count is 100-150 lines (except card 1: 150)
```

---

## Content Extraction Examples

### Example 1: Extracting Complexity Levels (For Card 2)

**Source** (CLAUDE.md):
```
Complexity Levels:
- 1-3 (Simple): Single developer, <4 hours, clear approach
- 4-6 (Medium): Single developer, 4-8 hours, may need research
- 7-8 (Complex): Consider breakdown, >8 hours, multiple sub-systems
- 9-10 (Very Complex): MUST break down, unclear scope, high risk
```

**Card Format** (Quick Reference table):
```markdown
## Quick Reference

| Complexity | Level | Typical Task | Review Mode |
|------------|-------|--------------|------------|
| 1-3 | 🟢 Simple | Typo fix, doc update | AUTO_PROCEED |
| 4-6 | 🟡 Medium | API endpoint, feature | QUICK_OPTIONAL |
| 7-8 | 🔴 Complex | Refactor, migration | FULL_REQUIRED |
| 9-10 | 🔴 Very Complex | Architecture, split needed | MUST SPLIT |
```

### Example 2: Extracting Decision Tree (For Card 3)

**Source** (task-work.md):
```
Workflow Flags:
- --design-only: Design without implementation (task → design_approved)
- --implement-only: Implement pre-approved design (design_approved → in_progress)
- Neither: Full workflow (backlog → in_progress)
```

**Card Format** (Decision Tree):
```markdown
## Decision Guide

Start at "About to start task"

Is the task complex (complexity ≥ 7)?
├─ YES → Are you the architect or need architect approval?
│        ├─ YES → Use /task-work --design-only (design phase only)
│        └─ NO → Use /task-work (full workflow with checkpoint)
└─ NO → Use /task-work (default workflow)

After --design-only design approval:
└─ Use /task-work --implement-only (implementation only)
```

### Example 3: Extracting Real Examples (For Card 5)

**Source** (task-refine.md or CLAUDE.md):
```
When to Use Refinement:
- Minor code improvements (yes)
- Fixing linting issues (yes)
- Adding type hints (yes)
- Renaming for clarity (yes)
- Adding new features (no)
- Changing architecture (no)
- Major refactoring (no)
```

**Card Format** (Scenarios):
```markdown
## Examples

**Scenario 1**: Improve variable naming
  Command: /task-refine TASK-042 "Rename variables for clarity"
  Result: Existing implementation reviewed, variables renamed, tests re-run

**Scenario 2**: Add inline comments
  Command: /task-refine TASK-042 "Add inline comments to complex sections"
  Result: Comments added, all tests pass, task stays IN_REVIEW

**Scenario 3**: Fix linting issues
  Command: /task-refine TASK-042 "Fix linting errors (unused imports, etc)"
  Result: Linting issues fixed, full test suite passes
```

---

## Common Pitfalls to Avoid

1. **Card 1 is too ambitious**
   - Problem: Trying to cover all details in 150 lines
   - Solution: Use tables for space efficiency; reference other cards

2. **Diagrams don't render in Markdown**
   - Problem: Using unsupported diagram syntax
   - Solution: Use ASCII art or Markdown tables (native support)

3. **Content doesn't match source documentation**
   - Problem: Paraphrasing changes technical meaning
   - Solution: Use exact quotes for technical details; cite source

4. **Incomplete content extraction**
   - Problem: Card 4 missing Phase 5.5 plan audit details
   - Solution: Verify both TASK-007 AND TASK-025 content included

5. **Poor readability**
   - Problem: Long paragraphs, no visual hierarchy
   - Solution: Use tables, bullets, bold text, short sentences

6. **Broken cross-references**
   - Problem: See Also links to non-existent cards
   - Solution: Verify all links exist before finalizing

---

## File Checklist

**Before submitting, verify each card has**:

```markdown
# Card Title (H1)

## Overview
[1-2 sentences] ✓

## Quick Reference
[Table or bullets] ✓

## Decision Guide
[Tree or flowchart] ✓

## Examples
[2-3 scenarios] ✓

## See Also
[3-7 references] ✓

EOF (proper ending)
```

---

## Success Criteria Validation

Before marking cards as complete:

### Content Validation
- [ ] Each card extracted from correct source(s)
- [ ] Technical accuracy verified against source
- [ ] Examples use correct command syntax
- [ ] No deprecated features mentioned
- [ ] Terminology matches main documentation

### Format Validation
- [ ] All 8 cards created
- [ ] Template structure consistent
- [ ] Markdown renders without errors
- [ ] Line count: 100-150 (Card 1: 150 allowed)
- [ ] Heading hierarchy: H1 for title, H2 for sections

### Completeness Validation
- [ ] Diagrams in 6+ cards (75%)
- [ ] Decision guides in 4+ cards (50%)
- [ ] Examples in all 8 cards (2-3 per card)
- [ ] No incomplete sentences or TODO markers
- [ ] All features from TASK-005 through TASK-029 covered

### Cross-Reference Validation
- [ ] All See Also links are valid
- [ ] Links use consistent Markdown format
- [ ] No circular references
- [ ] No broken links

### Printability Validation
- [ ] Print test successful (8.5" x 11" paper)
- [ ] All content visible when printed
- [ ] Font size readable (≥10pt equivalent)
- [ ] Tables fit on page width
- [ ] Diagrams render properly

---

## Time Tracking

**Estimate**: 1.5-2 hours total

- Prep & source gathering: 15 min
- Infrastructure cards (2,3,5,6): 45 min (11 min each)
- Integration cards (4,7,8): 30 min (10 min each)
- Integration card (1): 20 min
- Quality review & print test: 10 min

**Actual time may vary** based on:
- Source documentation clarity
- Diagram creation time
- Revision iterations
- Print testing complexity

---

## Questions?

If you encounter ambiguities or questions during implementation:

1. **Check FINDINGS-SUMMARY.md** for known gaps and recommendations
2. **Check REQUIREMENTS-ANALYSIS.md** for detailed requirement rationale
3. **Check EARS-REQUIREMENTS.md** for specific acceptance criteria
4. **Reference source task specifications** for technical accuracy
5. **Ask for clarification** on Priority 1 items before starting (if not done)

---

**Guide Version**: 1.0
**Created**: 2025-10-24
**Status**: Ready for Implementation
