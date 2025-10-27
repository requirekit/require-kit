---
id: TASK-003B
title: Review Modes & User Interaction (Quick Review + Full Review)
status: completed
created: 2025-10-09T10:20:00Z
updated: 2025-10-10T12:45:00Z
completed: 2025-10-10T12:45:00Z
assignee: null
priority: high
tags: [workflow-enhancement, human-in-the-loop, user-interaction, phase-2.8, review-modes]
requirements: []
bdd_scenarios: []
parent_task: TASK-003
dependencies: [TASK-003A]
blocks: [TASK-003C]
research_documents:
  - docs/research/implementation-plan-review-recommendation.md
test_results:
  status: passed
  last_run: 2025-10-10T12:45:00Z
  coverage: 92.31
  passed: 53
  failed: 0
  execution_log: "All subtasks completed - parent task complete"
blocked_reason: null
progress:
  total_subtasks: 4
  completed_subtasks: 4
  percentage: 100
  subtasks:
    - id: TASK-003B-1
      title: Quick Review Mode - Countdown Timer & Basic Input
      status: completed
      completed_date: 2025-10-09T17:45:00Z
    - id: TASK-003B-2
      title: Full Review Mode Display & Basic Actions
      status: completed
      completed_date: 2025-10-09T17:20:00Z
    - id: TASK-003B-3
      title: Modification & View Modes
      status: completed
      completed_date: 2025-10-09T18:45:00Z
    - id: TASK-003B-4
      title: Q&A Mode - Interactive Plan Questions
      status: completed
      completed_date: 2025-10-10T12:45:00Z
---

# Task: Review Modes & User Interaction

## Parent Context

This is **Part 2 of 5** of the Implementation Plan Review enhancement (TASK-003).

**Parent Task**: TASK-003 - Implement Complexity-Based Implementation Plan Review
**Depends On**: TASK-003A (complexity calculation and auto-proceed mode)
**Blocks**: TASK-003C (integration with task-work workflow)

## Description

Implement the interactive review modes for medium and complex tasks. This includes:
1. **Quick Review Mode** (score 4-6): 10-second timeout with option to escalate
2. **Full Review Mode** (score 7-10): Comprehensive checkpoint with decision options
3. **User Interaction Handlers**: Approve, Modify, View, Question, Cancel

**Key Innovation**: Complexity-based interruption - only show full checkpoint when necessary, but always provide escape hatch for user control.

## Acceptance Criteria

### Phase 1: Quick Review Mode (Score 4-6) ✅ MUST HAVE

- [ ] **Quick Review Display**
  - [ ] Show summary card with:
    ```
    📊 Complexity: 5/10 (Medium)

    ╔═══════════════════════════════════════════════════════╗
    ║ 📋 QUICK IMPLEMENTATION REVIEW                        ║
    ╚═══════════════════════════════════════════════════════╝

    CHANGES SUMMARY:
      📁 New Files: 3
         - src/features/auth/AuthService.ts
         - src/features/auth/TokenService.ts
         - src/features/auth/AuthController.ts

      ✏️  Modified Files: 1
         - src/api/routes/index.ts (add auth routes)

      🧪 Tests Planned: 8
         - Unit tests: 6
         - Integration tests: 2

      ⏱️  Estimated: ~40 minutes

    ⏰ Proceeding in 10 seconds...
       [Press ENTER to review plan in detail]
       [Press 'c' to cancel]
    ```

- [ ] **10-Second Countdown Timer**
  - [ ] Display countdown: "10... 9... 8... 7..."
  - [ ] Visual progress indicator
  - [ ] Non-blocking (can be interrupted)
  - [ ] Clear display of time remaining

- [ ] **User Input Handlers During Countdown**
  - [ ] **ENTER pressed**: Stop countdown, escalate to full review
  - [ ] **'c' pressed**: Stop countdown, cancel task
  - [ ] **Timeout (no input)**: Auto-proceed to Phase 3
  - [ ] Handle other keys gracefully (ignore or warn)

- [ ] **Escalation to Full Review**
  - [ ] Transition smoothly from quick to full review
  - [ ] Preserve context and plan data
  - [ ] Show full checkpoint display
  - [ ] Provide all decision options (A/M/V/Q/C)

- [ ] **Cancellation Handler**
  - [ ] Stop countdown immediately
  - [ ] Move task back to BACKLOG
  - [ ] Save all work done (plan, metadata)
  - [ ] Display cancellation confirmation
  - [ ] Exit task-work command

### Phase 2: Full Review Mode (Score 7-10 or Escalated) ✅ MUST HAVE

- [ ] **Full Review Checkpoint Display**
  - [ ] Show comprehensive review:
    ```
    🛑 HUMAN REVIEW REQUIRED

    ╔═══════════════════════════════════════════════════════╗
    ║ 📋 IMPLEMENTATION PLAN REVIEW - HUMAN CHECKPOINT      ║
    ╚═══════════════════════════════════════════════════════╝

    TASK: TASK-047 - Implement event sourcing for orders
    COMPLEXITY: 8/10 (Complex)
    ESTIMATED TIME: ~3 hours

    ⚠️  COMPLEXITY FACTORS:
      🔴 Using unfamiliar pattern: Event Sourcing
      🔴 8 new files, 3 modified files
      🔴 High risk: State consistency and event replay
      🟡 2 new dependencies: EventStore, EventBridge

    CHANGES SUMMARY:
      📁 New Files: 8
         [detailed file list with purposes]

      ✏️  Modified Files: 3
         [detailed file list with changes]

      🧪 Tests Planned: 18
         - Unit tests: 12 (aggregate, events, handlers)
         - Integration tests: 4 (event store, event replay)
         - E2E tests: 2 (complete order flow)

      📦 New Dependencies:
         - event-store-client@^2.0.0
         - event-bridge-sdk@^1.5.0

    ARCHITECTURE ALIGNMENT:
      ✅ SOLID compliance: 82/100
      ⚠️  Consider: Interface segregation for event handlers

    RISK ASSESSMENT:
      🔴 High Risk: Event replay consistency
         → Mitigation: Comprehensive event replay tests

      🟡 Medium Risk: Learning curve for team
         → Mitigation: Detailed documentation

    IMPLEMENTATION ORDER:
      1. Domain Layer (45 min)
      2. Infrastructure Layer (60 min)
      3. Application Layer (45 min)
      4. Testing (60 min)
      5. Documentation (30 min)

    QUESTIONS FOR REVIEW:
      1. Event versioning: Use migration or multiple versions?
      2. Snapshot frequency: Every 50 events or time-based?
      3. Event storage: PostgreSQL or dedicated event store?

    OPTIONS:
    1. [A]pprove - Proceed with implementation as planned
    2. [M]odify - Adjust plan before implementing
    3. [V]iew - Show complete implementation plan document
    4. [Q]uestion - Ask questions about the approach
    5. [C]ancel - Cancel task and return to BACKLOG

    ⚠️  Note: This is a complex task. Please review carefully.

    Your choice (A/M/V/Q/C):
    ```

- [ ] **Input Validation**
  - [ ] Accept case-insensitive input (A/a, M/m, etc.)
  - [ ] Handle invalid input gracefully
  - [ ] Provide clear error messages
  - [ ] Re-prompt on invalid choice

- [ ] **Block Until User Responds**
  - [ ] No timeout on full review
  - [ ] Wait for explicit user decision
  - [ ] Preserve state during wait
  - [ ] Handle interruption signals (Ctrl+C)

### Phase 3: Decision Option Handlers ✅ MUST HAVE

- [ ] **[A]pprove Handler**
  - [ ] Update task metadata:
    ```yaml
    implementation_plan:
      reviewed: true
      approved: true
      approved_by: "user"
      approved_at: "{ISO timestamp}"
      review_duration_seconds: {elapsed}
    ```
  - [ ] Display approval confirmation
  - [ ] Proceed to Phase 3 (Implementation)
  - [ ] Log approval decision

- [ ] **[M]odify Handler**
  - [ ] Enter interactive modification mode
  - [ ] Display editable plan sections:
    - Files to create/modify
    - Testing strategy
    - Dependencies
    - Implementation order
  - [ ] Accept modifications
  - [ ] Validate changes
  - [ ] Regenerate plan with modifications
  - [ ] Recalculate complexity score
  - [ ] Save as new version (v2, v3, etc.)
  - [ ] Return to checkpoint with updated plan
  - [ ] Track modification count in metadata

- [ ] **[V]iew Handler**
  - [ ] Display complete plan file in pager
  - [ ] Syntax highlighting for markdown
  - [ ] Allow scrolling through document
  - [ ] Return to checkpoint menu after viewing
  - [ ] Track view action in metadata

- [ ] **[Q]uestion Handler**
  - [ ] Enter Q&A mode
  - [ ] Display Q&A interface:
    ```
    ╔═══════════════════════════════════════════════════════╗
    ║ ❓ IMPLEMENTATION PLAN Q&A                            ║
    ╚═══════════════════════════════════════════════════════╝

    Type your question or 'back' to return to options.

    Your question:
    ```
  - [ ] Accept natural language questions
  - [ ] Query implementation planner agent
  - [ ] Display answers with context
  - [ ] Support multiple rounds of Q&A
  - [ ] 'back' command returns to checkpoint
  - [ ] Track Q&A history in metadata

- [ ] **[C]ancel Handler**
  - [ ] Confirm cancellation
  - [ ] Move task back to BACKLOG
  - [ ] Save all work done:
    - Requirements analysis
    - Implementation plan
    - Architectural review
    - Complexity calculation
  - [ ] Update task metadata (cancelled=true)
  - [ ] Exit task-work command cleanly
  - [ ] Display cancellation summary

### Phase 4: Interactive Modification Mode ✅ MUST HAVE

- [ ] **Modification Interface**
  - [ ] Display current plan sections
  - [ ] Highlight editable areas
  - [ ] Accept section-by-section edits:
    ```
    SECTION: Files to Create
    Current: 8 files
    1. src/domain/Order.ts
    2. src/domain/events/OrderCreated.ts
    ...

    [R]emove file, [A]dd file, [E]dit file, [D]one editing this section
    Your choice:
    ```

- [ ] **Modification Options**
  - [ ] Add file to plan
  - [ ] Remove file from plan
  - [ ] Edit file purpose/description
  - [ ] Modify testing strategy
  - [ ] Add/remove dependencies
  - [ ] Adjust implementation order
  - [ ] Update time estimates

- [ ] **Validation & Regeneration**
  - [ ] Validate modifications:
    - File paths valid
    - Dependencies installable
    - Test counts reasonable
  - [ ] Regenerate plan incorporating changes
  - [ ] Recalculate complexity score
  - [ ] Update complexity factors
  - [ ] Save as new version (increment version number)
  - [ ] Display updated complexity

- [ ] **Return to Checkpoint**
  - [ ] Show updated plan summary
  - [ ] Display new complexity score
  - [ ] Offer checkpoint options again
  - [ ] Track modification iteration

### Phase 5: Q&A Mode Implementation ✅ MUST HAVE

- [ ] **Q&A Interface**
  - [ ] Accept question input
  - [ ] Parse question intent
  - [ ] Context extraction (task, plan, requirements)
  - [ ] Query implementation planner agent
  - [ ] Display formatted answer

- [ ] **Answer Generation**
  - [ ] Provide rationale for plan decisions
  - [ ] Reference requirements when relevant
  - [ ] Explain trade-offs considered
  - [ ] Suggest alternatives if asked
  - [ ] Include confidence level (1-10)

- [ ] **Multi-Turn Conversation**
  - [ ] Maintain conversation context
  - [ ] Allow follow-up questions
  - [ ] Reference previous Q&A in session
  - [ ] Clear "back" command to exit

- [ ] **Q&A History**
  - [ ] Save Q&A exchanges in metadata
  - [ ] Track questions asked
  - [ ] Include in plan documentation
  - [ ] Help future developers understand decisions

### Phase 6: Plan Versioning ✅ MUST HAVE

- [ ] **Version Management**
  - [ ] Create v1 on initial generation (TASK-003A)
  - [ ] Create v2 on first modification
  - [ ] Increment version on each modification
  - [ ] Format: `TASK-XXX-implementation-plan-v2.md`
  - [ ] Update metadata with current version

- [ ] **Version Comparison**
  - [ ] Track what changed between versions
  - [ ] Display diff summary when returning to checkpoint
  - [ ] Allow viewing previous versions
  - [ ] Keep version history accessible

- [ ] **Version Metadata**
  ```yaml
  implementation_plan:
    file: "TASK-XXX-implementation-plan-v3.md"
    version: 3
    version_history:
      - version: 1
        created: "2025-10-09T10:00:00Z"
        reason: "Initial generation"
      - version: 2
        created: "2025-10-09T10:15:00Z"
        reason: "User modified: Removed 2 files"
        complexity_before: 8
        complexity_after: 6
      - version: 3
        created: "2025-10-09T10:30:00Z"
        reason: "User modified: Added integration tests"
        complexity_before: 6
        complexity_after: 7
  ```

## Technical Specifications

### Quick Review Countdown Implementation

```python
import time
import sys
import select

def quick_review_countdown(timeout_seconds: int = 10) -> str:
    """
    Display countdown and listen for user input
    Returns: 'timeout' | 'escalate' | 'cancel'
    """
    print(f"⏰ Proceeding in {timeout_seconds} seconds...")
    print("   [Press ENTER to review plan in detail]")
    print("   [Press 'c' to cancel]")
    print()

    for remaining in range(timeout_seconds, 0, -1):
        # Print countdown
        sys.stdout.write(f"\r  {remaining}... ")
        sys.stdout.flush()

        # Check for input (non-blocking)
        if sys.stdin in select.select([sys.stdin], [], [], 1)[0]:
            key = sys.stdin.read(1)
            if key == '\n':  # ENTER
                print("\n\n🔍 Escalating to full review...\n")
                return 'escalate'
            elif key.lower() == 'c':
                print("\n\n❌ Cancelling task...\n")
                return 'cancel'

    print("\n\n⚡ Timeout - proceeding to implementation...\n")
    return 'timeout'
```

### Full Review Checkpoint Implementation

```python
def full_review_checkpoint(plan: dict, complexity: dict) -> str:
    """
    Display full review and get user decision
    Returns: 'approve' | 'modify' | 'view' | 'question' | 'cancel'
    """
    display_full_review(plan, complexity)

    while True:
        choice = input("Your choice (A/M/V/Q/C): ").strip().upper()

        if choice in ['A', 'M', 'V', 'Q', 'C']:
            return {
                'A': 'approve',
                'M': 'modify',
                'V': 'view',
                'Q': 'question',
                'C': 'cancel'
            }[choice]
        else:
            print(f"❌ Invalid choice: '{choice}'. Please enter A, M, V, Q, or C.")
```

### Interactive Modification Mode

```python
def interactive_modification(plan: dict) -> dict:
    """
    Allow user to modify plan interactively
    Returns: modified plan
    """
    modified_plan = plan.copy()
    sections = ['files', 'tests', 'dependencies', 'order']

    for section in sections:
        print(f"\n📝 Editing: {section.upper()}")
        display_section(modified_plan, section)

        while True:
            action = input("[A]dd, [R]emove, [E]dit, [D]one: ").strip().upper()

            if action == 'D':
                break
            elif action == 'A':
                modified_plan = add_to_section(modified_plan, section)
            elif action == 'R':
                modified_plan = remove_from_section(modified_plan, section)
            elif action == 'E':
                modified_plan = edit_section_item(modified_plan, section)
            else:
                print(f"❌ Invalid action: '{action}'")

    return modified_plan
```

### Q&A Mode Implementation

```python
def qa_mode(plan: dict, task: dict) -> list:
    """
    Interactive Q&A about the implementation plan
    Returns: List of Q&A exchanges
    """
    qa_history = []

    print("\n╔═══════════════════════════════════════════════════════╗")
    print("║ ❓ IMPLEMENTATION PLAN Q&A                            ║")
    print("╚═══════════════════════════════════════════════════════╝\n")
    print("Type your question or 'back' to return to options.\n")

    while True:
        question = input("Your question: ").strip()

        if question.lower() == 'back':
            break

        if not question:
            continue

        # Query implementation planner agent
        answer = query_planner_agent(question, plan, task)

        # Display answer
        print(f"\n🤖 Implementation Planner:\n")
        print(answer)
        print()

        # Save Q&A
        qa_history.append({
            'question': question,
            'answer': answer,
            'timestamp': datetime.now().isoformat()
        })

    return qa_history
```

## Test Requirements

### Unit Tests

- [ ] **Countdown Timer Tests**
  - [ ] Test full countdown (no input)
  - [ ] Test ENTER press during countdown
  - [ ] Test 'c' press during countdown
  - [ ] Test invalid input during countdown
  - [ ] Test countdown display formatting

- [ ] **Input Handler Tests**
  - [ ] Test approve handler (A/a)
  - [ ] Test modify handler (M/m)
  - [ ] Test view handler (V/v)
  - [ ] Test question handler (Q/q)
  - [ ] Test cancel handler (C/c)
  - [ ] Test invalid input handling

- [ ] **Modification Tests**
  - [ ] Test add file to plan
  - [ ] Test remove file from plan
  - [ ] Test edit file properties
  - [ ] Test modify dependencies
  - [ ] Test validation of modifications

- [ ] **Versioning Tests**
  - [ ] Test version increment (v1 → v2 → v3)
  - [ ] Test version metadata tracking
  - [ ] Test version file creation
  - [ ] Test version history preservation

### Integration Tests

- [ ] **Quick Review Timeout Path**
  - [ ] Display quick review
  - [ ] Countdown runs to completion
  - [ ] Auto-proceed to Phase 3
  - [ ] Metadata updated correctly

- [ ] **Quick Review Escalation Path**
  - [ ] Display quick review
  - [ ] User presses ENTER
  - [ ] Escalate to full review
  - [ ] Show all options (A/M/V/Q/C)

- [ ] **Full Review Approval Path**
  - [ ] Display full review
  - [ ] User selects [A]pprove
  - [ ] Metadata updated
  - [ ] Proceed to Phase 3

- [ ] **Modification Loop**
  - [ ] User selects [M]odify
  - [ ] Enter modification mode
  - [ ] Make changes
  - [ ] Regenerate plan
  - [ ] Recalculate complexity
  - [ ] Return to checkpoint
  - [ ] Version incremented

- [ ] **Q&A Mode**
  - [ ] User selects [Q]uestion
  - [ ] Enter Q&A loop
  - [ ] Ask multiple questions
  - [ ] Receive answers
  - [ ] Type 'back' to return
  - [ ] Q&A history saved

- [ ] **Cancellation**
  - [ ] User selects [C]ancel
  - [ ] Task moved to BACKLOG
  - [ ] Work saved (plan, metadata)
  - [ ] Task-work exits cleanly

### End-to-End Tests

- [ ] **Medium Task with Timeout**
  - Task with score 5/10
  - Quick review displayed
  - Wait for timeout
  - Auto-proceed to implementation

- [ ] **Medium Task with Escalation**
  - Task with score 5/10
  - Quick review displayed
  - Press ENTER within 10s
  - Full review shown
  - Approve and proceed

- [ ] **Complex Task with Modification**
  - Task with score 8/10
  - Full review displayed
  - Select [M]odify
  - Remove 2 files
  - Recalculated: score 6/10
  - Approve modified plan

- [ ] **Complex Task with Q&A**
  - Task with score 9/10
  - Full review displayed
  - Select [Q]uestion
  - Ask 3 questions
  - Get detailed answers
  - Return and approve

## Success Metrics

### User Experience Metrics
- Quick review timeout rate: 60-70% (most skip)
- Quick review escalation rate: 30-40% (some review)
- Full review approval rate: 80-90%
- Modification usage: 10-20%
- Q&A usage: 20-30%
- Cancellation rate: <5%

### Performance Metrics
- Countdown display latency: <100ms
- Full review display time: <2 seconds
- Q&A response time: <3 seconds
- Modification regeneration: <5 seconds

### Quality Metrics
- Input handling accuracy: 100%
- Version tracking accuracy: 100%
- Metadata update accuracy: 100%

## File Structure

```
installer/global/
├── agents/
│   ├── task-manager.md                      [UPDATE - Add Phase 2.8]
│   └── implementation-planner.md            [NEW - Q&A responses]
│
└── templates/
    └── implementation-plan-template.md      [UPDATE - Add Q&A section]

tests/
└── integration/
    └── test_review_modes.py                 [NEW]
```

**Files to Create**: 2
**Files to Modify**: 2

## Dependencies

**Depends On**:
- ✅ TASK-003A (complexity calculation, auto-proceed, plan generation)

**Blocks**:
- ⏸️ TASK-003C (needs review modes for orchestration)

**Enables**:
- Quick review for medium tasks (immediate value)
- Full review for complex tasks (safety net)
- User control at appropriate times

## Risks & Mitigations

### Risk 1: Timeout Too Short
**Mitigation**: Configurable timeout (default 10s, can increase), clear visual countdown, easy to escalate

### Risk 2: Q&A Response Quality
**Mitigation**: Provide context to agent (plan + requirements + task), fallback to "I don't have enough information" if uncertain

### Risk 3: Modification Complexity
**Mitigation**: Start with simple modifications (add/remove files), expand later, validation before regeneration

## Success Criteria

**Task is successful if**:
- ✅ Quick review mode works with timeout and escalation
- ✅ Full review mode displays all necessary information
- ✅ All 5 decision options (A/M/V/Q/C) work correctly
- ✅ Modification mode allows plan changes
- ✅ Q&A mode provides helpful answers
- ✅ Plan versioning tracks changes
- ✅ All integration tests pass

**Task complete when**:
- ✅ Medium tasks can use quick review (timeout or escalate)
- ✅ Complex tasks show full review checkpoint
- ✅ TASK-003C can integrate review modes into workflow

## Links & References

### Research Documents
- [Implementation Plan Review Recommendation](../../docs/research/implementation-plan-review-recommendation.md)

### Parent & Related Tasks
- [TASK-003](../backlog/TASK-003-implementation-plan-review-with-complexity-triggering.md) - Parent task
- [TASK-003A](../backlog/TASK-003A-complexity-calculation-auto-proceed.md) - Depends on this
- **Blocks**: TASK-003C (Integration)

## Implementation Notes

**Design Decisions**:
1. 10-second timeout balances speed and control
2. Escalation always available (ENTER key)
3. Modification loop allows iterative refinement
4. Q&A provides context without forcing modification
5. Version tracking maintains full audit trail

**User Flow**:
```
Medium Task (score 4-6):
  Quick Review Display
    ↓
  10-Second Countdown
    ↓
  User Input?
    - No input → Timeout → Auto-proceed ⚡
    - ENTER → Escalate → Full Review 🔍
    - 'c' → Cancel → BACKLOG ❌

Complex Task (score 7-10):
  Full Review Display 🛑
    ↓
  Block for User Decision
    ↓
  [A]pprove → Proceed
  [M]odify → Edit → Regenerate → Return to Review
  [V]iew → Show Plan → Return to Review
  [Q]uestion → Q&A → Return to Review
  [C]ancel → BACKLOG
```

---

**Estimated Effort**: 1 week (5 working days)
**Expected ROI**: Immediate (enables review for 30-50% of tasks)
**Priority**: High (core user interaction)
**Complexity**: 7/10 (Complex - user interaction, state management, multiple paths)
