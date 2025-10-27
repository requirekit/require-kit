# TASK-030D EARS Requirements - Individual Specifications

**Format**: EARS (Easy Approach to Requirements Syntax)
**Task**: TASK-030D - Create Quick Reference Cards (8 Cards)
**Total Requirements**: 11 functional + 4 non-functional

---

## EARS Requirement Templates

### REQ-030D-001: Card Format and Structure
---
```
PATTERN: Ubiquitous (Always Active)
FORMAT: The [system] shall [behavior]
```

**EARS Statement**:
> The system shall create each quick reference card as a single Markdown file with a standardized template structure that fits on one printable page.

**Acceptance Criteria**:
- [ ] Each card file is named: `{card-name}.md`
- [ ] Card content fits on single printed page (8.5" x 11" with standard margins)
- [ ] Template structure identical across all 8 cards:
  - `# Card Title` (main heading)
  - `## Overview` (1-2 sentences)
  - `## Quick Reference` (table or list)
  - `## Decision Guide` (visual or decision tree)
  - `## Examples` (2-3 scenarios)
  - `## See Also` (cross-references)
- [ ] All sections present in all cards
- [ ] Line count target: 100-150 lines per card
- [ ] Markdown formatting valid and renders correctly

**Rationale**: Ensures consistent, predictable structure across all cards for user navigation

**Metrics**: 100% of cards comply with structure

---

### REQ-030D-002: Content Extraction from Authoritative Sources
---
```
PATTERN: Event-Driven (Trigger → Response)
FORMAT: When [trigger event], the [system] shall [response]
```

**EARS Statement**:
> When a quick reference card is created, the system shall extract content from corresponding command specifications and workflow documentation, ensuring technical accuracy and verifiable consistency.

**Acceptance Criteria**:
- [ ] All content sourced from TASK-030A command specifications
- [ ] Content sourced from workflow guide documentation
- [ ] Source documentation explicitly referenced in card
- [ ] Card content matches source documentation (word-for-word for technical terms)
- [ ] Examples use actual command syntax from source specs
- [ ] No paraphrasing that changes technical meaning
- [ ] Flag combinations verified against source documentation
- [ ] Phase descriptions match command specs exactly

**Rationale**: Guarantees cards remain accurate and synchronized with actual implementation

**Verification**: Cross-reference each card against source documentation

**Related**: REQ-030D-010 (Feature Integration)

---

### REQ-030D-003: Visual Diagrams in Quick Reference Cards
---
```
PATTERN: Ubiquitous with Specification
FORMAT: The [system] shall [behavior], where [optional condition]
```

**EARS Statement**:
> The system shall include visual diagrams (ASCII art, flowcharts, or decision trees) in at least 6 of the 8 quick reference cards to illustrate workflows, state transitions, or decision processes.

**Acceptance Criteria**:
- [ ] Minimum 6 of 8 cards include visual diagrams (75% requirement met)
- [ ] Diagrams are clear and understandable in Markdown format
- [ ] Diagram types appropriate to content:
  - State machine diagrams (cards 1, 3)
  - Flowchart/decision trees (cards 2, 4, 5, 8)
  - Process flow (card 7)
  - Comparison table (card 6)
- [ ] Diagrams render properly in both digital and printed format
- [ ] ASCII formatting consistent across all diagrams
- [ ] Legend provided if diagram uses symbols
- [ ] Each diagram has caption explaining its purpose

**Ambiguity Note**: Specific format not specified (ASCII vs Mermaid)
**Recommendation**: Use ASCII art for universal Markdown compatibility

**Success Metric**: 75%+ of cards (6/8) include visual diagrams

---

### REQ-030D-004: Decision Trees and Quick Decision Guides
---
```
PATTERN: Ubiquitous
FORMAT: The [system] shall [behavior]
```

**EARS Statement**:
> The system shall include decision trees or quick decision guides in at least 4 of the 8 quick reference cards to help developers make workflow choices without consulting full documentation.

**Acceptance Criteria**:
- [ ] Minimum 4 of 8 cards include decision guidance (50% requirement met)
- [ ] Decision trees use clear if-then logic
- [ ] Each branch leads to actionable decision
- [ ] Decision guides answer common questions:
  - "When should I use this flag?"
  - "Which option is right for my scenario?"
  - "What happens if I choose this path?"
- [ ] Decision trees have clear entry points and exit points
- [ ] Terminology consistent with main documentation
- [ ] Visual formatting makes decision path obvious

**Required in Cards**:
- Card 1: Phase selection decision tree
- Card 2: Complexity threshold decision guide
- Card 3: Flag selection decision tree
- Card 4: Escalation decision path
- Card 5: Refine vs re-work decision tree
- Card 8: When to modify decision framework

**Success Metric**: 50%+ of cards (4/8) include decision guidance

---

### REQ-030D-005: Common Scenarios and Real-World Examples
---
```
PATTERN: Ubiquitous
FORMAT: The [system] shall [behavior]
```

**EARS Statement**:
> The system shall include 2-3 common scenario examples in each of the 8 quick reference cards, demonstrating realistic usage patterns and expected outcomes.

**Acceptance Criteria**:
- [ ] Every card includes minimum 2 scenarios (preferably 3)
- [ ] Scenarios are realistic and based on actual usage patterns
- [ ] Each scenario format consistent:
  - **Scenario**: Describe the situation
  - **Action**: What command/flag to use
  - **Expected Result**: What happens next
- [ ] Scenarios cover both:
  - Common case (happy path)
  - Edge case or special consideration
- [ ] Scenarios are concise (2-5 lines each)
- [ ] Command syntax is accurate and executable
- [ ] Output examples provided where helpful

**Example Format**:
```
**Scenario**: Complex task requiring human checkpoint
  Action: /task-work TASK-042
  Result: Phase 2.8 checkpoint displays, options: [A]pprove/[M]odify/[R]eject
```

**Success Metric**: 100% of cards have scenarios; average 2.5+ per card

---

### REQ-030D-006: Cross-References and Navigation
---
```
PATTERN: Ubiquitous
FORMAT: The [system] shall [behavior]
```

**EARS Statement**:
> The system shall include "See Also" sections in each of the 8 quick reference cards with references to related cards and full documentation, creating a navigable network.

**Acceptance Criteria**:
- [ ] Every card has "See Also" section
- [ ] References include related quick reference cards (if applicable)
- [ ] References include links to workflow guides (docs/workflows/*.md)
- [ ] References include command specifications when relevant
- [ ] All cross-references are valid (no broken links)
- [ ] References use consistent format (Markdown links)
- [ ] Maximum 7 references per card (avoid information overload)
- [ ] References organized by category:
  - Related Cards
  - Full Guides
  - Command References

**Ambiguity Note**: Reference depth not fully specified
**Recommendation**: Standard scope (5-7 references per card)

**Link Format**:
```markdown
## See Also
- [Card Name](../quick-reference/card-name.md)
- [Workflow Guide](../workflows/workflow-name.md)
- [Command Spec](../../installer/global/commands/command-name.md)
```

---

### REQ-030D-007: Complete Coverage of All 8 Cards
---
```
PATTERN: Ubiquitous (Mandatory Completeness)
FORMAT: The [system] shall [behavior]
```

**EARS Statement**:
> The system shall create all 8 specified quick reference cards with accurate, complete content reflecting recently implemented features.

**Acceptance Criteria**:
- [ ] **Card 1**: task-work-cheat-sheet.md (150 lines)
  - All 6 phases of /task-work command
  - All flags: --design-only, --implement-only, --micro, --with-context, --sync-progress
  - Common errors and resolution paths
  - State transitions: BACKLOG → IN_PROGRESS → IN_REVIEW → COMPLETED
  - Sources: TASK-005, 006, 007, 025, 026, 027, 028, 029

- [ ] **Card 2**: complexity-guide.md (100 lines)
  - Complexity scoring factors (file count, patterns, risk, dependencies)
  - Score ranges and thresholds (1-3 simple, 4-6 medium, 7-8 complex, 9-10 very complex)
  - Breakdown strategies (when to split)
  - Examples by complexity level
  - Sources: TASK-005, 008

- [ ] **Card 3**: design-first-workflow-card.md (100 lines)
  - When to use --design-only flag
  - When to use --implement-only flag
  - State prerequisites (design_approved state)
  - Multi-day workflow patterns
  - Architect-developer handoff patterns
  - Source: TASK-006

- [ ] **Card 4**: quality-gates-card.md (100 lines)
  - All quality gates (compilation, tests, coverage, architectural review, audit)
  - Pass/fail criteria for each gate
  - Phase 4.5: Fix loop details (up to 3 attempts)
  - Phase 5.5: Plan audit scope creep detection
  - Escalation decision tree
  - Sources: TASK-007, 025

- [ ] **Card 5**: refinement-workflow-card.md (100 lines)
  - /task-refine command usage
  - When to refine vs re-work decision tree
  - Refinement workflow (maintains context)
  - Multiple refinement cycles
  - Context preservation (plan, review, audit)
  - Source: TASK-026

- [ ] **Card 6**: markdown-plans-card.md (100 lines)
  - Markdown plan format and benefits
  - Git diff improvements vs JSON
  - Manual editing workflow
  - Human-readable planning
  - File location: .claude/task-plans/
  - Source: TASK-027

- [ ] **Card 7**: phase28-checkpoint-card.md (100 lines)
  - Enhanced Phase 2.8 checkpoint display
  - Plan summary sections (files, dependencies, risks, effort)
  - Truncation rules and formatting
  - Complexity-based review mode display (AUTO/QUICK/FULL)
  - Integration with Markdown plans
  - Source: TASK-028

- [ ] **Card 8**: plan-modification-card.md (100 lines)
  - [M]odify option at Phase 2.8 checkpoint
  - 4 modification categories: Files, Dependencies, Risks, Effort
  - Version management system (automatic backups with timestamps)
  - Undo functionality (revert last modification)
  - When to modify vs approve/cancel decision
  - Integration with checkpoint workflow
  - Source: TASK-029

**Success Metric**: All 8 cards created with specified content

---

### REQ-030D-008: Consistent Template Structure
---
```
PATTERN: Ubiquitous
FORMAT: The [system] shall [behavior]
```

**EARS Statement**:
> Each quick reference card shall follow the standard template structure to ensure consistent organization and user experience across all cards.

**Template Structure** (Mandatory):
```markdown
# [Card Title]

## Overview
[1-2 sentence summary of what card covers]

## Quick Reference
[Table or bullet list of key information]

## Decision Guide
[Flowchart, decision tree, or selection guide]

## Examples
[2-3 common scenarios demonstrating usage]

## See Also
[Cross-references to related cards and documentation]
```

**Acceptance Criteria**:
- [ ] All 8 cards use identical section structure
- [ ] Main heading uses `# Card Title` (H1)
- [ ] Section headings use `## Section Name` (H2)
- [ ] No additional headings between sections
- [ ] Sections appear in specified order
- [ ] Overview is exactly 1-2 sentences
- [ ] Quick Reference uses table or bullet format
- [ ] Decision Guide uses visual format
- [ ] Examples follow consistent format
- [ ] See Also section present with minimum 3 references

---

### REQ-030D-009: Visual Formatting and Readability
---
```
PATTERN: Ubiquitous
FORMAT: The [system] shall [behavior]
```

**EARS Statement**:
> The system shall format all quick reference cards for maximum readability and visual hierarchy, using Markdown formatting features appropriately.

**Acceptance Criteria**:
- [ ] Heading hierarchy: H1 (#) for main title, H2 (##) for sections
- [ ] Tables used for structured data (not walls of text)
- [ ] Bullet lists used for sequential or grouped items
- [ ] Code blocks (` ``` `) used for commands and syntax
- [ ] Inline code (`backticks`) used for flags, commands, variables
- [ ] **Bold** used for key terms and decisions
- [ ] *Italic* used for emphasis on important concepts
- [ ] Proper spacing between sections (blank line minimum)
- [ ] No paragraphs longer than 3 lines
- [ ] No excessive nested lists (max 2 levels)
- [ ] Links use Markdown format: `[text](url)`

**Readability Checklist**:
- [ ] Content scannable (skimmable) in 1-2 minutes
- [ ] Key information stands out visually
- [ ] Diagrams are clear and visible
- [ ] Examples are distinct from explanatory text
- [ ] Font-friendly formatting (works in monospace and proportional fonts)

---

### REQ-030D-010: Feature Integration from Completed Tasks
---
```
PATTERN: State-Driven
FORMAT: While [system state], the [system] shall [behavior]
```

**EARS Statement**:
> While each quick reference card is being created, the system shall ensure content accurately reflects the features from its corresponding completed implementation task, maintaining currency with actual functionality.

**Acceptance Criteria**:
- [ ] Card references correct source task(s)
- [ ] Feature descriptions match implementation specs exactly
- [ ] No outdated features mentioned
- [ ] All recent changes and enhancements included
- [ ] Examples use actual command syntax from implementation
- [ ] Flags match actual implementation (no planned-but-not-shipped features)
- [ ] Examples work as shown (tested if possible)

**Content Verification Matrix**:

| Card | Task(s) | Key Features Verified |
|------|---------|----------------------|
| 1 | TASK-005,006,007,025,026,027,028,029 | 8 features integrated |
| 2 | TASK-005,008 | Complexity scoring system |
| 3 | TASK-006 | Design-first flags and state machine |
| 4 | TASK-007,025 | Fix loop and plan audit |
| 5 | TASK-026 | /task-refine command |
| 6 | TASK-027 | Markdown plans format |
| 7 | TASK-028 | Enhanced checkpoint display |
| 8 | TASK-029 | Interactive plan modification |

---

### REQ-030D-011: Printability and Page Formatting
---
```
PATTERN: State-Driven
FORMAT: While [system state], the [system] shall [behavior]
```

**EARS Statement**:
> While formatted for digital viewing, each quick reference card shall be printable as a complete single page (8.5" × 11" with standard margins) for physical reference during development.

**Acceptance Criteria**:
- [ ] Card content fits completely on single printed page
- [ ] No content cut off at page breaks
- [ ] Margins respect standard print boundaries (0.5" minimum)
- [ ] Font size equivalent to 10pt or larger when printed
- [ ] Tables fit within page width without truncation
- [ ] Diagrams render properly in print (not distorted)
- [ ] No color dependency (works in black and white)
- [ ] Page fits standard printer (no special paper size)
- [ ] Actual print test completed successfully

**Print Testing**:
- [ ] Print each card on 8.5" × 11" white paper
- [ ] Verify all content visible
- [ ] Verify diagrams readable
- [ ] Verify tables properly formatted
- [ ] Verify text not too small (readable at arm's length)

---

## Non-Functional Requirements

### NFR-030D-001: Content Accuracy
---
```
PATTERN: Ubiquitous
FORMAT: The [system] shall [behavior]
```

**Statement**:
> All technical content in quick reference cards shall match source documentation exactly to ensure developers can trust information without verification.

**Verification**: Cross-reference each card against source task specifications and command documentation line by line

**Acceptance**: 100% accuracy (zero discrepancies)

**Impact**: CRITICAL - Inaccurate information undermines entire purpose of cards

---

### NFR-030D-002: Consistency
---
```
PATTERN: Ubiquitous
FORMAT: The [system] shall [behavior]
```

**Statement**:
> All 8 quick reference cards shall use consistent terminology, formatting conventions, and structural patterns to create unified user experience.

**Verification**:
- Visual inspection of all cards
- Terminology cross-check across cards
- Structure validation against template
- Format consistency review

**Acceptance**: Zero inconsistencies in terminology or formatting

**Impact**: HIGH - Inconsistency confuses users and reduces effectiveness

---

### NFR-030D-003: Maintainability
---
```
PATTERN: Ubiquitous
FORMAT: The [system] shall [behavior]
```

**Statement**:
> Quick reference cards shall be easily updatable when underlying features change, with clear source references and organized file structure.

**Requirements**:
- [ ] Source task referenced at top of each card
- [ ] Clear comment in card indicating last update
- [ ] File structure organized in docs/quick-reference/ directory
- [ ] Cards follow consistent naming convention: `{feature}-{type}.md`
- [ ] Cards link to source documentation for detailed updates

**Impact**: MEDIUM - Supports long-term documentation maintenance

---

### NFR-030D-004: Usability
---
```
PATTERN: Ubiquitous
FORMAT: The [system] shall [behavior]
```

**Statement**:
> Quick reference cards shall answer common developer questions without requiring external references, providing self-contained guidance.

**Acceptance Criteria**:
- [ ] Typical user can find needed information in <2 minutes
- [ ] Card answers intended use-case questions
- [ ] Sufficient detail to make decisions without full docs
- [ ] Examples show clear usage patterns
- [ ] See Also section directs to deeper documentation

**Validation**: User testing with target audience (developers familiar with Agentecflow Lite)

**Impact**: HIGH - Primary purpose of quick reference cards

---

## Summary Table

| ID | Requirement | Type | Priority | Status | Clarity |
|----|-------------|------|----------|--------|---------|
| REQ-030D-001 | Format & Structure | Ubiquitous | High | Clear | ✅ |
| REQ-030D-002 | Content Extraction | Event-Driven | High | Clear | ✅ |
| REQ-030D-003 | Visual Diagrams | Ubiquitous | High | **⚠️ Ambiguous** | Format unclear |
| REQ-030D-004 | Decision Guides | Ubiquitous | High | Clear | ✅ |
| REQ-030D-005 | Scenarios & Examples | Ubiquitous | High | Clear | ✅ |
| REQ-030D-006 | Cross-References | Ubiquitous | Medium | **⚠️ Ambiguous** | Scope unclear |
| REQ-030D-007 | Card Completeness | Ubiquitous | Critical | Clear | ✅ |
| REQ-030D-008 | Template Consistency | Ubiquitous | High | Clear | ✅ |
| REQ-030D-009 | Visual Formatting | Ubiquitous | Medium | Clear | ✅ |
| REQ-030D-010 | Feature Integration | State-Driven | Critical | Clear | ✅ |
| REQ-030D-011 | Printability | State-Driven | High | Clear | ✅ |
| NFR-001 | Content Accuracy | — | Critical | Clear | ✅ |
| NFR-002 | Consistency | — | High | Clear | ✅ |
| NFR-003 | Maintainability | — | Medium | Clear | ✅ |
| NFR-004 | Usability | — | High | Clear | ✅ |

---

## Document Information

**Format**: EARS (Easy Approach to Requirements Syntax)
**Total Requirements**: 15 (11 functional + 4 non-functional)
**Clarity Level**: 85% clear / 15% ambiguous
**Status**: Analysis Complete - Ready for Implementation
**Created**: 2025-10-24
**Last Updated**: 2025-10-24
