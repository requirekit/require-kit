# Design-First Workflow

**Purpose**: Complete guide to separating design and implementation phases for complex tasks requiring upfront design approval.

**Learn design-first workflow in**:
- **2 minutes**: Quick Start
- **10 minutes**: Core Concepts
- **30 minutes**: Complete Reference

---

## Quick Start (2 minutes)

### Get Started Immediately

```bash
# Complex task workflow (separate design and implementation)

# Step 1: Design-only (stops at approval checkpoint)
/task-work TASK-042 --design-only

# → System executes Phases 1-2.8
# → Creates implementation plan
# → Stops at human checkpoint
# → Task moves to design_approved state

# Step 2: Human reviews design, approves
# (Review saved implementation plan)

# Step 3: Implement approved design (different day/person)
/task-work TASK-042 --implement-only

# → System loads saved plan
# → Executes Phases 3-5 (implementation, testing, review)
# → Task moves to in_review state
```

**That's it!** Design and implementation are cleanly separated.

**Learn More**: See "Core Concepts" below for when to use design-first and state machine details.

---

## Core Concepts (10 minutes)

### Workflow Flags

#### Flag: `--design-only`

**Purpose**: Execute design phases only, stop at approval checkpoint

**Phases Executed**: 1 → 2 → 2.5A → 2.5B → 2.7 → 2.8

**Phases Skipped**: 3 (Implementation), 4 (Testing), 4.5 (Fix Loop), 5 (Code Review)

**Outcome**: Task moves to `design_approved` state with saved implementation plan

**Example**:
```bash
/task-work TASK-006 --design-only

# System output:
Phase 1: Requirements Analysis ✅
Phase 2: Implementation Planning ✅
Phase 2.5A: Pattern Suggestion ✅
Phase 2.5B: Architectural Review ✅ (Score: 85/100)
Phase 2.7: Complexity Evaluation ✅ (Score: 7/10)
Phase 2.8: Human Checkpoint

🎨 Design Approval Required

Complexity: 7/10 (Complex)
Architectural Score: 85/100 (Approved with recommendations)
Files: 6 files to create
Estimated: 12 hours

Implementation Plan:
- phase_1: Setup infrastructure (2h)
- phase_2: Core implementation (6h)
- phase_3: Testing (4h)

[A]pprove  [M]odify  [V]iew Full Plan  [C]ancel

Your choice: A

✅ Design Approved

Task State: BACKLOG → DESIGN_APPROVED
Implementation plan saved: docs/state/TASK-006/implementation_plan.json

Next Steps:
1. Review saved plan: cat docs/state/TASK-006/implementation_plan.json
2. Schedule implementation session
3. Run: /task-work TASK-006 --implement-only
```

#### Flag: `--implement-only`

**Purpose**: Execute implementation phases using previously approved design

**Prerequisite**: Task MUST be in `design_approved` state

**Phases Executed**: 3 (Implementation), 4 (Testing), 4.5 (Fix Loop), 5 (Code Review)

**Phases Skipped**: 1-2.8 (uses saved design)

**Outcome**: Task moves to `in_review` (success) or `blocked` (tests failed)

**Example**:
```bash
/task-work TASK-006 --implement-only

# System output:
🚀 Implement-Only Workflow: Loading Approved Design

TASK: TASK-006 - Implement OAuth2 authentication

APPROVED DESIGN:
  Approved: 2025-10-11T14:30:00Z
  Approved by: human
  Architectural score: 85/100
  Complexity: 7/10

IMPLEMENTATION PLAN:
  Files: 6 files to create
  Dependencies: 2 new packages
  Estimated: 12 hours
  Test strategy: Unit + Integration + E2E

Beginning implementation phases (3 → 4 → 4.5 → 5)...

Phase 3: Implementation ✅
Phase 4: Testing ✅
Phase 4.5: Fix Loop ✅ (All tests passing)
Phase 5: Code Review ✅

✅ Task Complete

Task State: DESIGN_APPROVED → IN_REVIEW
Tests: 100% passing
Coverage: 85% (line), 78% (branch)
```

#### No Flags (Default Behavior)

**Purpose**: Execute complete workflow in single session

**Phases Executed**: All phases (1 → 2 → 2.5A → 2.5B → 2.7 → 2.8 → 3 → 4 → 4.5 → 5)

**Phase 2.8 Checkpoint**: Triggered based on complexity evaluation

See [complexity-management-workflow.md](./complexity-management-workflow.md) for checkpoint details.

**Example**:
```bash
/task-work TASK-006

# System executes all phases
# Checkpoint behavior depends on complexity:
# - 1-3: AUTO_PROCEED (no checkpoint)
# - 4-6: QUICK_OPTIONAL (30s timeout)
# - 7-10: FULL_REQUIRED (mandatory checkpoint)
```

### When to Use Design-First Workflow

#### Use `--design-only` When:

**High Complexity** (Score ≥7):
```bash
# System recommends design-first for complex tasks
/task-create "Implement event sourcing for orders" requirements:[REQ-042]

# Output:
ESTIMATED COMPLEXITY: 9/10 (Very Complex)

⚠️  RECOMMENDATION: Use design-first workflow

This task should be designed separately before implementation.

Suggested workflow:
  /task-work TASK-XXX --design-only
  # Review and approve design
  /task-work TASK-XXX --implement-only
```

**High-Risk Changes**:
- Security-sensitive changes (authentication, encryption)
- Breaking changes (public API modifications)
- Schema changes (database migrations with data)
- Production hotfixes

**Multiple Team Members Involved**:
- Architect designs, developer implements
- Design review by team lead, implementation by junior dev
- Cross-functional review required

**Unclear Requirements**:
- Requirements need design exploration
- Multiple implementation approaches possible
- Architecture decision needed

**Multi-Day Tasks**:
- Design on Day 1, implement on Day 2+
- Design during planning sprint, implement in execution sprint
- Asynchronous workflows (different timezones)

#### Use `--implement-only` When:

**Task Has Approved Design**:
- Task is in `design_approved` state
- Implementation plan exists and is approved

**Different Person Implementing**:
- Architect created design, developer implements
- Team lead designed, team member implements

**Continuing After Design Approval**:
- Design approved yesterday, implementing today
- Design approved in planning meeting, implementing in sprint

#### Use Default Workflow (No Flags) When:

**Simple to Medium Complexity** (Score ≤6):
- Straightforward implementation with clear approach
- Familiar patterns and low risk
- Single developer handling both design and implementation

**Low Risk Changes**:
- Bug fixes
- UI text changes
- Minor feature additions

**Same-Day Tasks**:
- Design and implementation happen in same session
- No need for separate approval process

### State Machine

```
BACKLOG
   ├─ (task-work) ──────────────────→ IN_PROGRESS ──→ IN_REVIEW
   │                                         ↓
   │                                     BLOCKED
   │
   └─ (task-work --design-only) ─→ DESIGN_APPROVED
                                        │
                                        └─ (task-work --implement-only) ─→ IN_PROGRESS ──→ IN_REVIEW
                                                                                   ↓
                                                                               BLOCKED
```

**State Transitions**:
- `BACKLOG` → `IN_PROGRESS` (default workflow)
- `BACKLOG` → `DESIGN_APPROVED` (--design-only workflow)
- `DESIGN_APPROVED` → `IN_PROGRESS` (--implement-only workflow)
- `IN_PROGRESS` → `IN_REVIEW` (tests passing)
- `IN_PROGRESS` → `BLOCKED` (tests failing)

### Real-World Scenarios

#### Scenario 1: Architect-Developer Handoff

**Context**: Senior architect designs, junior developer implements

**Workflow**:
```bash
# Senior Architect (Day 1)
/task-work TASK-042 --design-only
# Reviews architectural patterns, approves design
# Task → DESIGN_APPROVED

# Junior Developer (Day 2)
/task-work TASK-042 --implement-only
# Follows approved plan exactly
# Task → IN_REVIEW
```

**Outcome**: Junior developer has clear guidance, senior architect ensures quality design

#### Scenario 2: Security-Sensitive Changes

**Context**: Password hashing algorithm update requiring security review

**Workflow**:
```bash
# Developer (Day 1)
/task-work TASK-301 --design-only
# System detects security keywords → FULL_REQUIRED review
# Design approved by security team
# Task → DESIGN_APPROVED

# Developer (Day 3, after security approval)
/task-work TASK-301 --implement-only
# Implements approved security design
# Task → IN_REVIEW
```

**Outcome**: Security review before code written, cheaper to change design than code

#### Scenario 3: Multi-Day Complex Task

**Context**: Event sourcing implementation requiring 12+ hours

**Workflow**:
```bash
# Monday (2 hours)
/task-work TASK-401 --design-only
# Explore CQRS vs Event Sourcing approaches
# Select approach, approve design
# Task → DESIGN_APPROVED

# Tuesday-Wednesday (10 hours)
/task-work TASK-401 --implement-only
# Implement approved CQRS design
# Clear path forward, no design changes mid-implementation
# Task → IN_REVIEW
```

**Outcome**: Design decisions separate from implementation, better time estimation

**Learn More**: See "Complete Reference" below for design metadata schema and detailed examples.

---

## Complete Reference (30+ minutes)

### Flag Validation Rules

#### Mutual Exclusivity

`--design-only` and `--implement-only` cannot be used together:

```bash
# ❌ Invalid usage
/task-work TASK-006 --design-only --implement-only

# Error:
❌ Cannot use both --design-only and --implement-only flags together

Choose one workflow mode:
  --design-only     Execute design phases only (Phases 1-2.8)
  --implement-only  Execute implementation phases only (Phases 3-5)
  (no flags)        Execute complete workflow (default)
```

#### State Validation for `--implement-only`

`--implement-only` requires task to be in `design_approved` state:

```bash
# ❌ Invalid usage (task in backlog state)
/task-work TASK-006 --implement-only

# Error:
❌ Cannot execute --implement-only workflow

Task TASK-006 is in 'backlog' state.
Required state: design_approved

To approve design first, run:
  /task-work TASK-006 --design-only

Or run complete workflow without flags:
  /task-work TASK-006
```

### Design Metadata Schema

Design-only runs save comprehensive metadata in task frontmatter:

```yaml
design:
  status: approved
  approved_at: "2025-10-11T14:30:00Z"
  approved_by: "human"
  implementation_plan_version: "v1"
  architectural_review_score: 85
  complexity_score: 7
  design_session_id: "design-TASK-006-20251011143000"
  design_notes: "Reviewed by lead architect, approved for implementation"
  approval_timestamp: "2025-10-11T14:35:00Z"
  approval_duration_seconds: 300
```

**Metadata Fields**:
- `status`: approved | pending | rejected | n/a
- `approved_at`: ISO8601 timestamp of approval
- `approved_by`: human | auto (for simple tasks)
- `implementation_plan_version`: Version of saved plan (v1, v2, etc.)
- `architectural_review_score`: Score from Phase 2.5B (0-100)
- `complexity_score`: Score from Phase 2.7 (0-10)
- `design_session_id`: Unique identifier for design session
- `design_notes`: Human-entered notes during approval

### Implementation Plan Storage

Design plans are saved to: `docs/state/{task_id}/implementation_plan.json`

**Plan Structure**:
```json
{
  "task_id": "TASK-006",
  "created_at": "2025-10-11T14:30:00Z",
  "version": "v1",
  "complexity_score": 7,
  "architectural_review": {
    "overall_score": 85,
    "status": "approved_with_recommendations",
    "principles": {
      "solid": 90,
      "dry": 85,
      "yagni": 80
    },
    "recommendations": [
      "Consider using Strategy pattern for auth providers",
      "Extract token management into separate service"
    ]
  },
  "plan": {
    "files_to_create": [
      {
        "path": "src/auth/oauth2_service.py",
        "purpose": "OAuth2 authentication service",
        "estimated_loc": 120,
        "dependencies": ["requests", "jwt"]
      },
      {
        "path": "src/auth/token_manager.py",
        "purpose": "Token management and validation",
        "estimated_loc": 80,
        "dependencies": ["jwt", "redis"]
      },
      {
        "path": "tests/test_oauth2_service.py",
        "purpose": "Unit tests for OAuth2 service",
        "estimated_loc": 150,
        "dependencies": ["pytest", "pytest-mock"]
      }
    ],
    "files_to_modify": [],
    "external_dependencies": [
      {
        "name": "PyJWT",
        "version": "2.8.0",
        "purpose": "JWT token handling"
      },
      {
        "name": "redis",
        "version": "5.0.0",
        "purpose": "Token storage and caching"
      }
    ],
    "estimated_duration": "12 hours",
    "estimated_total_loc": 350,
    "implementation_phases": [
      {
        "phase": 1,
        "name": "Setup infrastructure",
        "tasks": [
          "Install dependencies (PyJWT, redis)",
          "Create module structure",
          "Setup configuration"
        ],
        "estimated_duration": "2 hours"
      },
      {
        "phase": 2,
        "name": "Core implementation",
        "tasks": [
          "Implement OAuth2Service class",
          "Implement TokenManager class",
          "Add error handling"
        ],
        "estimated_duration": "6 hours"
      },
      {
        "phase": 3,
        "name": "Testing and validation",
        "tasks": [
          "Write unit tests",
          "Write integration tests",
          "Manual testing"
        ],
        "estimated_duration": "4 hours"
      }
    ],
    "test_summary": {
      "unit_tests": 15,
      "integration_tests": 5,
      "e2e_tests": 2,
      "target_coverage": 85
    },
    "risks": [
      {
        "description": "OAuth2 provider rate limiting",
        "severity": "medium",
        "mitigation": "Implement exponential backoff and caching"
      },
      {
        "description": "Token storage security",
        "severity": "high",
        "mitigation": "Use Redis with encryption, expire tokens after 1 hour"
      }
    ]
  }
}
```

### Human Checkpoint Details (Phase 2.8)

When using `--design-only`, Phase 2.8 is ALWAYS executed (mandatory checkpoint).

**Checkpoint Display**:
```
═══════════════════════════════════════════════════════
🎨 PHASE 2.8 - DESIGN APPROVAL CHECKPOINT
═══════════════════════════════════════════════════════

TASK: TASK-006 - Implement OAuth2 authentication

COMPLEXITY EVALUATION (Phase 2.7):
  Score: 7/10 (Complex)
  Review Mode: FULL_REQUIRED
  Factors:
    - File Complexity: 3/3 (6 files)
    - Pattern Familiarity: 2/2 (OAuth2 unfamiliar)
    - Risk Level: 2/3 (security-sensitive)
    - Dependencies: 0/2 (no new deps)

ARCHITECTURAL REVIEW (Phase 2.5B):
  Overall Score: 85/100 (Approved with recommendations)
  SOLID: 90/100 ✅
  DRY: 85/100 ✅
  YAGNI: 80/100 ✅

  Recommendations (2):
  1. Consider using Strategy pattern for auth providers
  2. Extract token management into separate service

IMPLEMENTATION PLAN:
  Files: 6 files to create
  Dependencies: 2 new packages (PyJWT, redis)
  Estimated: 12 hours (3 phases)
  Tests: 22 tests planned (unit, integration, e2e)

RISKS IDENTIFIED (2):
  🟡 Medium: OAuth2 provider rate limiting
     Mitigation: Implement exponential backoff and caching

  🔴 High: Token storage security
     Mitigation: Use Redis with encryption, expire tokens

OPTIONS:
1. [A]pprove - Save design and move to DESIGN_APPROVED state
2. [M]odify - Edit plan (Coming soon - TASK-003B-3)
3. [V]iew - Show full implementation plan in pager
4. [C]ancel - Cancel and return task to BACKLOG

Your choice (A/M/V/C): _
═══════════════════════════════════════════════════════
```

**User Actions**:

**[A]pprove**:
- Saves implementation plan to `docs/state/TASK-006/implementation_plan.json`
- Updates task frontmatter with design metadata
- Moves task file from `tasks/backlog/` to `tasks/design_approved/`
- Displays success message with next steps

**[M]odify** (Coming soon):
- Opens interactive plan editor
- Allows modifying files, dependencies, phases
- Recalculates complexity after modifications
- Loops back to Phase 2.8 with updated plan

**[V]iew**:
- Displays full implementation plan in pager (less/more)
- Shows complete file list, all dependencies, full phases
- Returns to prompt after viewing

**[C]ancel**:
- Discards design session
- Task remains in BACKLOG state
- No plan saved, no state transition

### Implementing with Saved Plan

When using `--implement-only`, the system loads and executes the saved plan:

**Step 1: Load Context**
```bash
# System loads from saved plan
plan_path = "docs/state/TASK-006/implementation_plan.json"
saved_plan = load_plan(plan_path)

# Extracts:
files_to_create = saved_plan["plan"]["files_to_create"]
dependencies = saved_plan["plan"]["external_dependencies"]
phases = saved_plan["plan"]["implementation_phases"]
test_strategy = saved_plan["plan"]["test_summary"]
```

**Step 2: Display Implementation Context**
```
🚀 Implement-Only Workflow: Loading Approved Design

TASK: TASK-006 - Implement OAuth2 authentication

APPROVED DESIGN:
  Design approved: 2025-10-11T14:30:00Z
  Approved by: human
  Architectural score: 85/100
  Complexity score: 7/10

IMPLEMENTATION PLAN:
  Files to create: 6 files
  External dependencies: 2 packages
  Estimated duration: 12 hours
  Test strategy: 22 tests (unit, integration, e2e)

PHASES:
  Phase 1: Setup infrastructure (2h)
  Phase 2: Core implementation (6h)
  Phase 3: Testing and validation (4h)

Beginning implementation phases (3 → 4 → 4.5 → 5)...
```

**Step 3: Execute Phases 3-5**

See [task-work.md](../../installer/global/commands/task-work.md) for phase execution details.

- Phase 3: Implementation (using saved plan)
- Phase 4: Testing (using saved test strategy)
- Phase 4.5: Fix Loop (ensures all tests pass)
- Phase 5: Code Review

### Multi-Day Task Handling

Design-first workflow is ideal for tasks spanning multiple days or work sessions.

**Feature**: Multi-day task workflow support (TASK-006)

**Use Case**: Complex implementation requiring separate design and coding sessions

**Example: Day-by-Day Workflow**

**Day 1 - Monday (Design Phase)**:
```bash
# Lead architect designs solution
/task-work TASK-042 --design-only

# Phase 1-2.8 execute (design phases only)
# Architect reviews:
# - Complexity: 7/10 (complex)
# - Architectural score: 88/100
# - Files: 6 files planned
# - Duration estimate: 12 hours

# Architect approves design at checkpoint
[A]pprove

✅ Design Approved
Task State: BACKLOG → DESIGN_APPROVED
Implementation plan saved
```

**Day 2-3 - Tuesday-Wednesday (Implementation Phase)**:
```bash
# Developer implements approved design
/task-work TASK-042 --implement-only

# System loads saved plan
# Phase 3-5 execute (implementation phases only)
# All tests pass
# Task → IN_REVIEW

✅ Implementation Complete
Duration: 11.5 hours (vs. 12 hour estimate, -4% variance)
```

**Benefits**:
- Design review separate from implementation pressure
- Different team members can handle different phases
- Clear handoff points with documented plans
- Better time estimation (design time + implementation time)
- Reduced context switching

### Integration with Complexity Management

Design-first workflow integrates seamlessly with complexity evaluation:

**Automatic Recommendation**:
```bash
/task-create "Implement microservices architecture" requirements:[REQ-050]

# System evaluates:
ESTIMATED COMPLEXITY: 10/10 (Very Complex)

⚠️  CRITICAL: This task is too complex for single implementation

RECOMMENDATIONS:
1. Break down into smaller subtasks (RECOMMENDED)
2. Use design-first workflow with phased implementation

If proceeding as-is, use design-first workflow:
  /task-work TASK-XXX --design-only
  # Review design thoroughly
  /task-work TASK-XXX --implement-only

[S]plit into subtasks  [C]reate as-is with design-first  [A]bort
```

**Complexity Threshold Integration**:

See [complexity-management-workflow.md](./complexity-management-workflow.md#feature-level-complexity-control) for threshold details.

- Complexity ≥7: System recommends design-first workflow
- Complexity ≥9: System strongly recommends breakdown OR design-first
- Force-review triggers: Always require design-first workflow

**Three-Tier Safety Net**:
- **Tier 1**: Feature generation (TASK-008) - Complexity evaluation during `/feature-generate-tasks`
- **Tier 2**: Task creation (TASK-005) - Upfront complexity check during `/task-create`
- **Tier 3**: Implementation planning (TASK-006) - Final check during `/task-work` Phase 2.7

This prevents oversized tasks at every creation and implementation point.

---

## Examples (Real-World Scenarios)

### Example 1: Architect-Led Design, Developer Implementation

**Day 1: Architect designs (--design-only)**
```bash
# Lead architect designs the solution
/task-work TASK-101 --design-only

# Architect reviews:
# - Complexity: 8/10 (complex)
# - Architectural score: 92/100 (excellent)
# - Files: 8 files planned
# - Risks: Identified and mitigated

# Architect approves design
[A]pprove

# Design saved, task → DESIGN_APPROVED
```

**Day 2: Developer implements (--implement-only)**
```bash
# Different developer implements approved design
/task-work TASK-101 --implement-only

# System loads architect's approved plan
# Developer follows plan exactly
# All tests pass
# Task → IN_REVIEW
```

**Benefits**:
- Architect ensures quality design upfront
- Developer has clear implementation guidance
- No mid-implementation design changes
- Junior developers can implement senior designs

### Example 2: Multi-Day Sprint Workflow

**Planning Day (Monday): Design multiple tasks**
```bash
# Sprint planning: Design all sprint tasks
/task-work TASK-201 --design-only
/task-work TASK-202 --design-only
/task-work TASK-203 --design-only

# Team reviews all designs together
# Approves all three

# Tasks → DESIGN_APPROVED
# Ready for sprint execution
```

**Execution Days (Tuesday-Friday): Implement approved designs**
```bash
# Tuesday: Implement TASK-201
/task-work TASK-201 --implement-only

# Wednesday: Implement TASK-202
/task-work TASK-202 --implement-only

# Thursday-Friday: Implement TASK-203
/task-work TASK-203 --implement-only
```

**Benefits**:
- Design decisions made together (planning day)
- Implementation parallelizable (execution days)
- No blockers during implementation
- Velocity predictable (design time + implementation time)

### Example 3: High-Risk Security Change

**Security Review Required**
```bash
/task-work TASK-301 --design-only
# Task: "Update password hashing algorithm"

# Phase 2.5B: Architectural Review
# → Security patterns evaluated
# → Score: 88/100

# Phase 2.7: Complexity Evaluation
# → Force trigger: Security keyword ("password")
# → Review mode: FULL_REQUIRED

# Phase 2.8: Human Checkpoint
SECURITY-SENSITIVE TASK

This task requires security review before implementation.

Design includes:
- Bcrypt with cost factor 12
- Salt generation with os.urandom(16)
- Migration strategy for existing passwords

Risks:
🔴 High: Incorrect hashing breaks all logins
   Mitigation: Implement alongside old hashing, gradual migration

Recommendation: Security team review before implementation

[A]pprove  [C]ancel for security review

# Choose [C]ancel
# Send design to security team for review
# After approval, implement:

/task-work TASK-301 --implement-only
```

**Benefits**:
- Security review before code is written
- Design changes cheaper than code changes
- No wasted implementation time if design rejected
- Security patterns validated upfront

### Example 4: Unclear Requirements Exploration

**Day 1: Explore implementation approach**
```bash
/task-work TASK-401 --design-only
# Task: "Add real-time collaboration to document editor"

# Phase 2: Implementation Planning
# → Multiple approaches explored:
#   A. WebSockets with operational transforms
#   B. CRDT (Conflict-free Replicated Data Types)
#   C. Server-side locking with delta sync

# Phase 2.5B: Architectural Review
# → CRDT approach scored highest (90/100)

# Phase 2.8: Human Checkpoint
IMPLEMENTATION APPROACH SELECTED: CRDT

Rationale:
- Handles offline editing
- No central server bottleneck
- Conflict resolution built-in

Trade-offs:
- More complex initial implementation
- Larger client-side library
- But: Better long-term scalability

Files: 12 files planned
Estimated: 20 hours

[A]pprove selected approach
[M]odify to explore alternative
[C]ancel to research further

# Choose [A]pprove
```

**Day 2: Implement approved approach**
```bash
/task-work TASK-401 --implement-only

# Implementation follows approved CRDT approach
# No design changes during implementation
# Clear path forward
```

**Benefits**:
- Requirements clarified through design exploration
- Approach selected before implementation begins
- Team alignment on complex technical decisions
- No wasted implementation on wrong approach

### Example 5: Invalid State Transition (Error)

**Attempting --implement-only without approved design**
```bash
/task-work TASK-501 --implement-only

# Error:
❌ Cannot execute --implement-only workflow

Task TASK-501 is in 'backlog' state.
Required state: design_approved

CAUSE: No design has been approved for this task

TO FIX:
Option 1: Approve design first
  /task-work TASK-501 --design-only
  # Review and approve
  /task-work TASK-501 --implement-only

Option 2: Use complete workflow (no flags)
  /task-work TASK-501
  # Executes design and implementation in single session

Workflow aborted (invalid state transition)
```

---

## FAQ

### Q: When should I use design-first vs. default workflow?

**A**: Use design-first when:
- **Complexity ≥7** (system recommends automatically)
- **High risk** (security, breaking changes, production)
- **Multiple people** (architect designs, developer implements)
- **Multi-day** (design Day 1, implement Day 2+)
- **Unclear approach** (need to explore design options)

Use default workflow when:
- **Complexity ≤6** (simple to medium tasks)
- **Low risk** (bug fixes, minor features)
- **Single person** (you design and implement)
- **Same day** (design and implement in one session)

### Q: Can I modify the design after approval?

**A**: Yes, but requires re-approval:
```bash
# Load task in design-only mode again
/task-work TASK-XXX --design-only

# System detects existing design:
⚠️  Existing design detected (approved 2025-10-11)

This will create a new design version (v2).

[C]ontinue with new design
[K]eep existing design and implement
[A]bort

# Choose [C]ontinue
# Make design changes
# Re-approve → Creates v2 plan
```

### Q: What if tests fail during --implement-only?

**A**: The fix loop (Phase 4.5) handles test failures automatically:
```bash
/task-work TASK-XXX --implement-only

# Phase 4: Testing
❌ Tests failing (3 failures)

# Phase 4.5: Fix Loop (Attempt 1/3)
🔧 Fixing test failures...
✅ All tests passing

# Proceeds to Phase 5
```

If fix loop exhausted (3 attempts), task → BLOCKED:
```bash
❌ Unable to fix tests after 3 attempts

Task moved to: BLOCKED
Reason: Test failures persist after fixes

Next steps:
1. Review test failure details
2. Check if design needs revision
3. Re-run: /task-work TASK-XXX --implement-only
```

See [complexity-management-workflow.md](./complexity-management-workflow.md) for fix loop details.

### Q: Can I skip the design phase for urgent hotfixes?

**A**: Yes, use `--skip-design-check` flag (caution advised):
```bash
/task-work TASK-HOTFIX-001 --skip-design-check

# Warning:
⚠️  Design checkpoint skipped

This is an URGENT HOTFIX.
Quality gates still enforced (tests, review).

Proceeding directly to implementation...
```

**Recommendation**: Even for hotfixes, `--design-only` takes <10 minutes and catches design issues before implementation.

### Q: How do I view the saved implementation plan?

**A**: Several options:

**Option 1: View in terminal**
```bash
cat docs/state/TASK-XXX/implementation_plan.json | jq
```

**Option 2: During checkpoint**
```bash
/task-work TASK-XXX --design-only

# At checkpoint, choose [V]iew
[V]iew

# System displays full plan in pager
```

**Option 3: Task status command**
```bash
/task-status TASK-XXX --show-design

# Displays:
# - Design metadata
# - Approval status
# - Complexity score
# - Architectural score
# - Link to full plan
```

### Q: Can the system generate designs automatically without human approval?

**A**: For simple tasks (complexity 1-3), yes:
```bash
/task-work TASK-SIMPLE --design-only

# Phase 2.7: Complexity Evaluation
Score: 2/10 (Simple)
Review Mode: AUTO_PROCEED

# Phase 2.8: Auto-approval (no checkpoint)
✅ Design auto-approved (simple task)

Task → DESIGN_APPROVED
Approved by: system (auto)
```

For complex tasks (≥7), human approval always required.

---

## Related Documentation

- [Task Work Command](../../installer/global/commands/task-work.md) - Complete phase execution details
- [Complexity Management Workflow](./complexity-management-workflow.md) - Complexity evaluation and routing
- [Common Thresholds](../shared/common-thresholds.md) - Quality threshold definitions
- [Feature Generate Tasks](../../installer/global/commands/feature-generate-tasks.md) - Automatic task generation with complexity control

---

**Last Updated**: 2025-10-12
**Version**: 1.0.0
**Maintained By**: AI Engineer Team
