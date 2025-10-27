# TASK-030E-1: Quick Reference - Key Requirements

**Purpose**: 1-page summary of critical requirements for implementation
**For**: Developers executing TASK-030E-1
**Format**: Concise, scannable, action-oriented

---

## The Task at a Glance

Update 2 existing workflow guide files with new content (~200 lines total):
1. `docs/workflows/complexity-management-workflow.md` (+100 lines)
2. `docs/workflows/design-first-workflow.md` (+100 lines)

**Complexity**: 3/10 | **Effort**: 40 minutes | **Risk**: Low

---

## File 1: Complexity Management Workflow Updates

### Section 1: Upfront Evaluation (TASK-005)
**What**: Document complexity evaluation during task creation (`/task-create`)
**Key Points**:
- Timing: Stage 2, before work starts
- Input: task title, description, requirements
- Output: complexity score (0-10) with factor breakdown
- Threshold: >= 7 triggers split recommendation
- Benefit: saves 2-4 hours vs. mid-implementation breakdown
**Length**: 25-30 lines

**Example Output Format**:
```
ESTIMATED COMPLEXITY: 7/10
  File Complexity: 2/3 (4-6 files)
  Pattern Familiarity: 1/2 (mixed familiar/unfamiliar)
  Risk Level: 2/3 (external dependencies, moderate risk)
  Dependencies: 2/2 (3+ new dependencies)
```

### Section 2: Feature-Level Evaluation (TASK-008)
**What**: Document complexity during task generation (`/feature-generate-tasks`)
**Key Points**:
- When: During `/feature-generate-tasks FEAT-XXX`
- Automatic breakdown: tasks with complexity >= 7 split into subtasks
- Configurable: `--threshold N`, `--interactive` flags
- Strategies: horizontal (layers), vertical (stories), technical (concerns), temporal (phases)
- Shows distribution: simple/medium/complex count in output
**Length**: 35-40 lines

**Example**: 1 complex task → 5 right-sized subtasks

### Section 3: Three Complexity Touchpoints
**What**: Distinguish all 3 evaluation points with clear table/list
**Critical Distinction Table**:

| Aspect | Touchpoint 1 (Upfront) | Touchpoint 2 (Feature-Level) | Touchpoint 3 (Phase 2.7) |
|--------|---|---|---|
| **When** | During `/task-create` | During `/feature-generate-tasks` | During `/task-work` Phase 2.7 |
| **Stage** | Stage 2 | Stage 2 | Stage 3 |
| **Input** | Task desc, requirements | Feature scope | Implementation plan |
| **Output** | Score, split rec. | Refined task list | Score, review mode |
| **Purpose** | Prevent oversized tasks | Right-size generated tasks | Determine human checkpoint |
| **Threshold** | >= 7 suggests split | >= 7 triggers breakdown | >= 7 requires Phase 2.8 |

**Length**: 30-35 lines

---

## File 2: Design-First Workflow Updates

### Section 1: Real Examples from TASK-006
**What**: Show 2 realistic scenarios using design-first workflow
**Example 1: Architect-Led Complex Feature**
- Scenario: 7-8/10 complexity, multiple team members
- Workflow: Architect designs (2 hrs) → approved → Developer implements (4 hrs)
- State path: BACKLOG → DESIGN_APPROVED → IN_PROGRESS → IN_REVIEW
- Trigger: complexity >= 7 or multiple people involved

**Example 2: Security-Sensitive Feature**
- Scenario: 7-8/10 complexity, security/breaking changes
- Workflow: Design with security review → approved → Implementation with test enforcement
- State path: Shows Plan Modification (Phase 2.8) and test enforcement (Phase 4.5)
- Trigger: Security implications or regulatory impact

**Length**: 75-85 lines total (35-40 each example)

### Section 2: State Transition Diagram
**What**: ASCII diagram showing both standard and design-first workflows
**Must Show**:
- Standard path: BACKLOG → IN_PROGRESS → IN_REVIEW → COMPLETED (with BLOCKED exits)
- Design-first path: BACKLOG → DESIGN_APPROVED → IN_PROGRESS → IN_REVIEW → COMPLETED
- Branch point: decision to use design-first
- Blocking states: BLOCKED reachable from multiple states
- Triggers: show commands (`--design-only`, `--implement-only`)

**Format Example**:
```
BACKLOG
├─ (task-work) → IN_PROGRESS → IN_REVIEW → COMPLETED
│                     ↓            ↓
└─ (task-work --design-only) → DESIGN_APPROVED → (task-work --implement-only) → IN_PROGRESS → IN_REVIEW
```

**Length**: 35-45 lines (diagram + description table)

### Section 3: Decision Framework
**What**: Help users decide design-first vs. default workflow
**Mandatory Triggers** (use design-first if ANY true):
- [ ] Complexity >= 7
- [ ] Multiple team members involved
- [ ] Unfamiliar architectural patterns
- [ ] Security implications or breaking changes
- [ ] Database schema changes
- [ ] High-risk infrastructure changes

**Optional Factors** (consider if multiple true):
- [ ] Effort > 4 hours
- [ ] 5+ files affected
- [ ] New dependencies
- [ ] Multiple subsystems affected

**Default Workflow** (suitable if ALL true):
- Complexity < 7
- Single developer
- Familiar technology
- Low risk
- No external dependencies
- Effort < 4 hours

**Benefit**: Design-first adds 1-2 hours but saves 2-4 hours vs. mid-implementation breakdown

**Length**: 40-50 lines

### Section 4: Multi-Day Workflow Example
**What**: Show complete 2-day workflow (design day 1, implement day 2)
**Day 1: Design Phase (14:00-16:00)**
- Actor: Tech Lead/Architect
- State: BACKLOG
- Command: `/task-work TASK-042 --design-only`
- Executes: Phases 1-2.8 (stops at checkpoint)
- Outputs:
  - Implementation plan saved (.claude/task-plans/TASK-042-implementation-plan.md)
  - Complexity score: 7/10
  - Architectural review: 85/100
  - State transitions to: DESIGN_APPROVED

**Day 1 Evening: Approval**
- Stakeholders review plan
- Approval comments added to task
- Mark as APPROVED_FOR_IMPLEMENTATION

**Day 2: Implementation Phase (10:00-14:00)**
- Actor: Developer (possibly different from Day 1)
- State: DESIGN_APPROVED
- Command: `/task-work TASK-042 --implement-only`
- Executes: Phases 3-5.5 (load saved plan, implement, test, audit)
- Outputs:
  - Implementation completed per plan
  - Tests passing (Phase 4)
  - Code reviewed (Phase 5)
  - Plan audit passed (Phase 5.5)
  - State transitions to: IN_REVIEW

**Day 2 Afternoon: QA Review**
- QA reviews implementation
- Approval or refinement request
- Status: COMPLETED or needs refinement

**Benefits Highlighted**:
- Enables parallel work
- Approval gates before coding
- Clear role handoff
- Risk mitigation through design review
- State preservation across days

**Length**: 35-45 lines

---

## Acceptance Criteria Checklist

### Critical Must-Haves (FAIL if any missing)
- [ ] All 3 complexity touchpoints clearly distinguished with table
- [ ] State machine diagram shows DESIGN_APPROVED state
- [ ] Decision framework is actionable (users can apply it)
- [ ] Examples are realistic (grounded in TASK-005/006/008)
- [ ] All command names and flags are correct

### Important Quality Standards
- [ ] Terminology matches CLAUDE.md (Complexity Evaluation, not "assessment")
- [ ] Cross-references valid or marked [LINK TBD]
- [ ] Total output: 190-210 lines (target 200 ±10%)
- [ ] No formatting errors, markdown is clean
- [ ] No [TODO], [FIXME], or placeholder text

### Reader Comprehension Tests
- [ ] Reader can identify all 3 complexity touchpoints
- [ ] Reader can apply decision framework to a scenario
- [ ] Reader can trace state transitions for design-first workflow
- [ ] Reader understands multi-day workflow handoff points

---

## Common Implementation Patterns

### Cross-Reference Format
```
See [CLAUDE.md: Task Complexity Evaluation (lines 534-621)](https://path/to/CLAUDE.md)
or
[LINK TBD - Updated in TASK-030E-2: Quality Gates Workflow]
```

### Terminology to Use Consistently
- "Complexity Evaluation" (not "assessment")
- "Upfront Evaluation" (not "initial estimation")
- "Implementation Planning" (not "design planning")
- "Phase 2.7" (not "complexity phase")
- "Human Checkpoint" (not "approval step")
- "Test Enforcement Loop" (not "test fixing")
- "Plan Audit" (not "scope check")

### Example Scenario Names
- Payment Processing System
- User Authentication Service
- Notification Queue Integration
- E-commerce Order Management
- Real-time Dashboard
- Data Migration Pipeline

---

## Output Validation Checklist

**Before Marking Complete**:
1. [ ] File 1: All 3 sections added (~100 lines)
2. [ ] File 2: All 4 sections added (~100 lines)
3. [ ] Total: 190-210 lines (check line count)
4. [ ] No broken links or [TODO] markers
5. [ ] Complexity table distinct and clear
6. [ ] State diagram readable in markdown
7. [ ] Decision framework actionable
8. [ ] Examples grounded in TASK-005/006/008
9. [ ] All terminology consistent with CLAUDE.md
10. [ ] Cross-references validated

---

## If You Get Stuck

**Question**: How detailed should Phase 2.7 explanation be?
**Answer**: Summary with key concepts + pointer to task-work command docs (avoid duplication)

**Question**: Should examples use generic names or specific domains?
**Answer**: Use specific domains (Payment Processing, User Authentication) for realism

**Question**: What if TASK-005/006/008 aren't available?
**Answer**: Use examples from CLAUDE.md + create representative (but realistic) scenarios

**Question**: How to handle forward references to TASK-030E-2?
**Answer**: Use format: `[LINK TBD - See TASK-030E-2: Quality Gates Workflow]`

**Question**: Line count is slightly over 210 - what do I do?
**Answer**: Acceptable if within 220. If >220, cut least important details or create minimal subtask.

---

**Task Overview**: See full requirements analysis in `TASK-030E-1-REQUIREMENTS-ANALYSIS.md`
**Parent Task**: TASK-030E (Create/Update Workflow Guides)
**Next Tasks**: TASK-030E-2 (Core Workflow Guides), TASK-030E-3 (Phase 2.8 Enhancements), TASK-030E-4 (Conductor Success Story)
