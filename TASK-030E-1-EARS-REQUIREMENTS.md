# TASK-030E-1: EARS-Formatted Requirements

**Document Purpose**: Formal requirements specification using EARS notation
**Task**: TASK-030E-1 - Update Existing Workflow Guides (2 Files)
**Format**: EARS Notation (Easy Approach to Requirements Syntax)
**Total Requirements**: 24 specified below

---

## Part 1: Ubiquitous Requirements (Always Active)

### REQ-UBQ-001: Content Structure Consistency
**EARS**: The workflow guide documentation shall maintain consistent structural hierarchy with headings, subheadings, code blocks, and lists matching established patterns from existing guides.
**Rationale**: Ensures consistency across documentation suite; improves scannability and user comprehension
**Acceptance**: Manual verification against existing workflow guide patterns

### REQ-UBQ-002: Cross-Reference Validation
**EARS**: The documentation shall include only valid cross-references to CLAUDE.md, command specifications, and other workflow guides, with all broken links marked as [LINK TBD] pending completion.
**Rationale**: Ensures readers can follow references without dead links
**Acceptance**: Automated link checking + manual review

### REQ-UBQ-003: Terminology Consistency
**EARS**: The documentation shall use consistent terminology aligned with CLAUDE.md glossary, including "Complexity Evaluation" (not "assessment"), "Implementation Planning" (not "design planning"), and proper phase numbering (Phase 2.7, Phase 2.8).
**Rationale**: Prevents confusion from synonymous terms; improves discoverability
**Acceptance**: Terminology audit against CLAUDE.md

### REQ-UBQ-004: Technical Accuracy
**EARS**: The documentation shall accurately represent complexity scoring factors (file complexity, pattern familiarity, risk level, dependencies), Phase 2.7 workflow mechanics, and state machine transitions as specified in CLAUDE.md.
**Rationale**: Incorrect technical details mislead readers and reduce documentation credibility
**Acceptance**: Cross-verification against CLAUDE.md source (lines 534-621, 185-190, 1287-1298)

### REQ-UBQ-005: Markdown Quality
**EARS**: The documentation shall be syntactically valid markdown with no formatting errors, all code blocks having language specifiers, and all tables properly aligned.
**Rationale**: Ensures documentation renders correctly across all platforms
**Acceptance**: Markdown linting + visual validation in viewer

### REQ-UBQ-006: No Placeholder Content
**EARS**: The documentation shall contain no [TODO], [FIXME], incomplete examples, or unresolved references in the final submitted version.
**Rationale**: Incomplete content frustrates readers and reduces professionalism
**Acceptance**: Text search for placeholder markers; manual review

---

## Part 2: Event-Driven Requirements

### REQ-EV-001: Complexity Touchpoint Documentation
**EARS**: When the complexity management workflow is referenced by users, the system documentation shall identify and distinguish three distinct complexity evaluation touchpoints: (1) upfront during task creation, (2) feature-level during task generation, (3) implementation planning during Phase 2.7.
**Rationale**: Understanding when complexity is evaluated is critical for preventing oversized tasks
**Acceptance**: Table showing all 3 touchpoints with timing, input, output, purpose, threshold

### REQ-EV-002: Upfront Evaluation Context
**EARS**: When a user reads about upfront complexity evaluation, the documentation shall explain its occurrence during `/task-create` command execution, its purpose of preventing oversized tasks before work starts, and the split recommendation threshold of complexity >= 7.
**Rationale**: Users need to understand when and why upfront evaluation prevents waste
**Acceptance**: Section with timing, purpose, inputs, outputs, threshold, and example

### REQ-EV-003: Feature-Level Complexity Breakdown
**EARS**: When the `/feature-generate-tasks` command is executed, the documentation shall explain how it evaluates task complexity and automatically breaks down tasks with complexity >= 7 into right-sized subtasks.
**Rationale**: Users need to understand automatic breakdown during task generation
**Acceptance**: Section documenting command, threshold, breakdown strategies, and example

### REQ-EV-004: Phase 2.7 Integration
**EARS**: When task work enters Phase 2.7 (implementation planning), the documentation shall explain how complexity is evaluated based on planned files, patterns, risks, and dependencies, and how this score determines the need for Phase 2.8 human checkpoint.
**Rationale**: Users need to understand third complexity evaluation point
**Acceptance**: Section explaining Phase 2.7, scoring factors, output, and link to Phase 2.8

### REQ-EV-005: Real-World Examples from TASK-006
**EARS**: When users read about design-first workflow, the documentation shall include minimum two realistic examples grounded in TASK-006 research, showing actual complexity scores, effort estimates, and state transitions.
**Rationale**: Abstract explanations are less useful than concrete examples
**Acceptance**: Two complete scenario descriptions with realistic metrics

### REQ-EV-006: State Machine Visualization
**EARS**: When users need to understand task state transitions with design-first workflow, the documentation shall provide an ASCII state diagram showing both standard (BACKLOG → IN_PROGRESS) and design-first (BACKLOG → DESIGN_APPROVED) paths with labeled transitions.
**Rationale**: Visual representation helps users understand complex workflow paths
**Acceptance**: Readable ASCII diagram + state description table

### REQ-EV-007: Decision Framework Application
**EARS**: When developers must choose between design-first and default workflow, the documentation shall provide actionable decision criteria including mandatory triggers, optional factors, and default workflow conditions.
**Rationale**: Users need objective guidance, not subjective recommendations
**Acceptance**: Decision framework that can be applied to hypothetical tasks

### REQ-EV-008: Multi-Day Workflow Demonstration
**EARS**: When users plan a complex task spanning multiple days, the documentation shall provide a detailed example showing Day 1 design phase (architect, 2 hours, phases 1-2.8), approval period, and Day 2 implementation phase (developer, 4 hours, phases 3-5.5).
**Rationale**: Multi-day workflows are important for large teams but less obvious than single-day
**Acceptance**: Complete timeline with state transitions and handoff points

---

## Part 3: State-Driven Requirements

### REQ-ST-001: Complexity Touchpoint Progression
**EARS**: While task development progresses from creation through implementation, the documentation shall explain how the three complexity evaluation touchpoints work together (redundancy, progression, refinement).
**Rationale**: Understanding touchpoint interaction prevents over-evaluation or under-evaluation
**Acceptance**: Explanation of touchpoint synergy in three-touchpoint section

### REQ-ST-002: Design-First State Transitions
**EARS**: While a task uses the design-first workflow, the state machine diagram shall show valid transitions including BACKLOG → DESIGN_APPROVED → IN_PROGRESS → IN_REVIEW → COMPLETED, with BLOCKED reachable from any non-terminal state.
**Rationale**: Incorrect state transitions confuse users about valid workflows
**Acceptance**: State diagram accuracy verified against CLAUDE.md lines 1287-1298

### REQ-ST-003: Human Checkpoint Triggering
**EARS**: While task complexity is >= 7 or architectural review score is < 80, the documentation shall indicate that Phase 2.8 human checkpoint is required (not optional).
**Rationale**: Users need to understand when human review is mandatory
**Acceptance**: Clear statement of checkpoint triggers in complexity sections

### REQ-ST-004: Phase 2.7 Output Determination
**EARS**: While Phase 2.7 complexity evaluation is in progress, the system documentation shall explain how the output (complexity score and review mode) determines whether Phase 2.8 checkpoint occurs or implementation proceeds automatically.
**Rationale**: Understanding Phase 2.7 output is critical to understanding checkpoint routing
**Acceptance**: Clear explanation of complexity → review mode mapping

---

## Part 4: Optional Feature Requirements

### REQ-OPT-001: Conductor Integration Reference
**EARS**: Where design-first workflow enables parallel development with multiple team members, the documentation may reference (but not elaborate on) compatibility with Conductor.build for parallel task execution.
**Rationale**: Design-first workflow is useful for Conductor use cases; awareness helps users
**Acceptance**: 1-2 line mention that design-first is compatible with parallel development

---

## Part 5: Specific Content Requirements

### REQ-CONT-001: File 1 - Complexity Management Workflow Updates
**EARS**: The file `docs/workflows/complexity-management-workflow.md` shall be updated with three new sections totaling approximately 100 lines.

**Section 1.1 - Upfront Evaluation**:
- Documents `/task-create` command complexity evaluation
- Explains timing, inputs (task description, requirements), outputs (complexity score with factors)
- Threshold: complexity >= 7 triggers split recommendation
- Benefit: prevents 2-4 hours of wasted work on oversized tasks
- Length: 25-30 lines
- Example output shown with complexity factor breakdown

**Section 1.2 - Feature-Level Complexity**:
- Documents `/feature-generate-tasks` automatic task breakdown
- Explains automatic decomposition for tasks with complexity >= 7
- Shows example: 1 complex task decomposed into 5 right-sized subtasks
- Documents configuration: `--threshold N`, `--interactive` flags
- Lists 4 breakdown strategies (horizontal, vertical, technical, temporal)
- Includes complexity distribution metrics in output example
- Length: 35-40 lines

**Section 1.3 - Three Touchpoint Distinction**:
- Creates table or list distinguishing all 3 complexity evaluation points
- For each touchpoint: timing, stage, inputs, outputs, purpose, threshold
- Explains touchpoint synergy (progression and redundancy)
- Includes Phase 2.7 specific factors (file complexity, patterns, risk, dependencies)
- Shows example contrasting low vs. high complexity task handling
- Length: 30-35 lines

**Total File 1**: ~100 lines (acceptable: 95-105)

### REQ-CONT-002: File 2 - Design-First Workflow Updates
**EARS**: The file `docs/workflows/design-first-workflow.md` shall be updated with four new sections totaling approximately 100 lines.

**Section 2.1 - Real Examples from TASK-006**:
- Includes minimum 2 realistic, grounded examples
- Example 1: Architect-led complex feature (7-8/10 complexity, multiple roles)
- Example 2: Security-sensitive feature (7-8/10 complexity, mandatory design-first)
- Each example shows: scenario description, complexity score, effort timeline, workflow path, state transitions
- Examples grounded in actual research (TASK-006) not purely hypothetical
- Length: 75-85 lines total (35-40 each)

**Section 2.2 - State Transition Diagrams**:
- ASCII or markdown diagram showing:
  - Standard workflow path (BACKLOG → IN_PROGRESS → IN_REVIEW → COMPLETED)
  - Design-first path (BACKLOG → DESIGN_APPROVED → IN_PROGRESS → ...)
  - BLOCKED state reachable from multiple states
  - Transitions labeled with triggering commands (`--design-only`, `--implement-only`)
- State description table with: state name, purpose, entry conditions, exit conditions
- All 6 states defined: BACKLOG, DESIGN_APPROVED, IN_PROGRESS, IN_REVIEW, BLOCKED, COMPLETED
- Diagram readable in any markdown viewer (ASCII-friendly)
- Length: 35-45 lines (diagram + table)

**Section 2.3 - Decision Framework**:
- Actionable decision method (checklist, decision tree, or both)
- Mandatory triggers (use design-first if ANY true):
  - Complexity >= 7
  - Multiple team members involved
  - Unfamiliar architectural patterns
  - Security implications or breaking changes
  - Database schema changes
  - High-risk infrastructure changes
  - Total: minimum 3-6 triggers documented with rationale
- Optional factors (consider if multiple true):
  - Effort > 4 hours
  - Affects 5+ files
  - Requires new dependencies
  - Affects multiple subsystems
  - Total: minimum 4 factors
- Default workflow conditions (suitable if ALL true):
  - Complexity < 7
  - Single developer
  - Familiar technology
  - Low risk
  - No external dependencies
  - Effort < 4 hours
  - Total: minimum 5-6 conditions
- Time savings benefit: design-first adds 1-2 hours but saves 2-4 hours vs. mid-implementation breakdown
- Cross-references to complexity evaluation (TASK-005)
- Length: 40-50 lines

**Section 2.4 - Multi-Day Workflow Example**:
- Complete 2-day scenario: architect-led or security-sensitive task
- Day 1 Design Phase (documented):
  - Time slot (e.g., 14:00-16:00, 2 hours)
  - Actor (Tech Lead, Architect)
  - Task state (BACKLOG)
  - Command: `/task-work TASK-XXX --design-only`
  - Phases executed: 1-2.8
  - Outputs: implementation plan file path, complexity score, architectural review, DESIGN_APPROVED state
- Day 1 Evening Approval (documented):
  - Review stakeholders
  - Approval process
  - Design notes added to task
- Day 2 Implementation Phase (documented):
  - Time slot (e.g., 10:00-14:00, 4 hours)
  - Actor (Developer, possibly different from Day 1)
  - Task state (DESIGN_APPROVED)
  - Command: `/task-work TASK-XXX --implement-only`
  - Phases executed: 3-5.5
  - Outputs: implementation complete, tests passing, code review, plan audit, IN_REVIEW state
- Day 2 Afternoon QA Review (documented):
  - Final review and approval
  - Transition to COMPLETED or refinement
- Benefits highlighted:
  - Enables parallel work by separate team members
  - Design approval gates prevent bad assumptions in code
  - Clear role handoff and responsibility boundaries
  - Risk mitigation through design review before implementation
  - State preservation across days/sessions
- Realistic scenario name (Payment Processing, User Authentication, etc.)
- Length: 35-45 lines

**Total File 2**: ~100 lines (acceptable: 95-105)

---

## Part 6: Quality and Validation Requirements

### REQ-QUAL-001: Example Realism
**EARS**: All examples presented in the documentation shall be grounded in actual research or realistic scenarios derived from TASK-005, TASK-006, or TASK-008, rather than purely hypothetical or generic examples.
**Rationale**: Realistic examples are more credible and more useful for reader application
**Acceptance**: Examples marked with source reference or [REPRESENTATIVE EXAMPLE] notation

### REQ-QUAL-002: Reader Comprehension
**EARS**: The documentation shall be written at a comprehension level accessible to developers with varying experience, with technical jargon explained on first use and acronyms spelled out (EARS, SOLID, DRY, YAGNI, TDD, BDD).
**Rationale**: Increases accessibility and usability across developer experience levels
**Acceptance**: Peer review for clarity; reader comprehension testing

### REQ-QUAL-003: Actionability
**EARS**: The decision framework shall provide step-by-step guidance that enables users to make workflow choices without external reference, with objective criteria rather than subjective recommendations.
**Rationale**: Subjective guidance leads to inconsistent decisions; objective criteria are reproducible
**Acceptance**: Test scenarios where users can apply framework independently

### REQ-QUAL-004: Diagram Clarity
**EARS**: All visual elements (ASCII state diagrams, tables) shall be clear, readable in plain markdown viewers, and not cluttered with unnecessary detail.
**Rationale**: Poor diagram quality reduces comprehension and looks unprofessional
**Acceptance**: Visual validation in markdown viewer + peer review

---

## Part 7: Integration and Scope Requirements

### REQ-INT-001: CLAUDE.md Integration
**EARS**: The documentation shall integrate with existing CLAUDE.md content, including cross-references to sections 534-621 (Task Complexity Evaluation), 185-190 (Phase 2.7), and 1287-1298 (State Machine), without duplicating content.
**Rationale**: Reduces duplication; directs users to comprehensive source for details
**Acceptance**: Cross-reference accuracy; no substantial duplication

### REQ-INT-002: Agentecflow Lite Positioning
**EARS**: The documentation shall position complexity evaluation and design-first workflow as components of the broader Agentecflow Lite workflow (referenced in TASK-030B), not as standalone features.
**Rationale**: Contextualizes these features within complete system; improves coherence
**Acceptance**: Mentions Agentecflow Lite and cross-references TASK-030B guide

### REQ-INT-003: Forward Reference Handling
**EARS**: Where documentation references content created in subsequent subtasks (TASK-030E-2, TASK-030E-3, TASK-030E-4), cross-references shall be marked as [LINK TBD - See TASK-XXX description] or as placeholders, with automatic update contingent on completion of dependent tasks.
**Rationale**: Prevents broken links; enables sequential task execution
**Acceptance**: Placeholder format consistent across both files

### REQ-INT-004: Output Line Count
**EARS**: The total output from both files shall not exceed 230 lines, with target range of 190-210 lines (each file approximately 100 ±10%).
**Rationale**: Keeps output within safe token limits to prevent context window overflow during validation
**Acceptance**: Line count verification; if >230, creates minimal subtask

### REQ-INT-005: Scope Boundaries
**EARS**: The task shall be limited to updating two existing workflow guide files only, and shall NOT include creating new workflow guides (TASK-030E-2), updating CLAUDE.md main file (TASK-030C), creating quick reference cards (TASK-030D), or updating Conductor documentation (TASK-030E-4).
**Rationale**: Maintains clear task boundaries; prevents scope creep
**Acceptance**: Verification that only 2 files updated; no new files created

---

## Summary of Requirements by Type

| Type | Count | Key Examples |
|------|-------|--------------|
| Ubiquitous | 6 | Consistency, accuracy, validation, terminology, quality |
| Event-Driven | 8 | Touchpoint documentation, real examples, framework, visualization |
| State-Driven | 4 | Progression, transitions, triggering, output determination |
| Optional | 1 | Conductor reference (optional mention) |
| Content-Specific | 2 | File 1 (3 sections), File 2 (4 sections) |
| Quality | 4 | Realism, comprehension, actionability, clarity |
| Integration | 5 | CLAUDE.md, Agentecflow Lite, forward refs, line count, scope |
| **TOTAL** | **30** | **30 distinct requirements** |

---

## Requirement Traceability

**Mapped to Task Acceptance Criteria** (14 from task description):
- Criteria 1-3 (content quality, real examples, consistency) → REQ-UBQ-001-006, REQ-QUAL-001-004
- Criteria 4-7 (complexity guide specifics) → REQ-EV-001-004, REQ-CONT-001
- Criteria 8-11 (design-first guide specifics) → REQ-EV-005-008, REQ-CONT-002
- Criteria 12-14 (integration and references) → REQ-INT-001-005

**Dependencies**:
- Upstream: TASK-030A (command specs), TASK-030B (Agentecflow Lite guide), CLAUDE.md
- Downstream: TASK-030E-2, TASK-030E-3, TASK-030E-4, TASK-030F

---

**Document Status**: Requirements finalized for TASK-030E-1 execution
**Created**: 2025-10-24
**Format**: EARS Notation (Ubiquitous, Event-Driven, State-Driven, Optional, Unwanted, Temporary)
**Completeness**: 30 distinct requirements covering all aspects of task
