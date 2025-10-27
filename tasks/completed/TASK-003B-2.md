---
id: TASK-003B-2
title: Full Review Mode - Display & Basic Actions (Approve/Cancel)
status: completed
created: 2025-10-09T16:35:00Z
updated: 2025-10-09T17:20:00Z
completed_date: 2025-10-09T17:20:00Z
assignee: null
priority: high
tags: [workflow-enhancement, user-interaction, full-review, checkpoint, phase-2.8]
requirements: []
bdd_scenarios: []
parent_task: TASK-003B
dependencies: [TASK-003B-1]
blocks: [TASK-003B-3, TASK-003B-4, TASK-003C]
test_results:
  status: passed
  last_run: 2025-10-09T17:10:00Z
  coverage:
    complexity_models: 87%
    review_modes: 71%
    user_interaction: 43%
  passed: 34
  failed: 0
  execution_log: TEST_REPORT_TASK-003B-2.md
blocked_reason: null
implementation_plan:
  approved: true
  approved_by: code-reviewer
  approved_at: 2025-10-09T17:12:00Z
  review_mode: full_required
  architectural_review_score: 73
  code_review_status: approved
completion_summary:
  duration_hours: 0.75
  acceptance_criteria_met: true
  quality_gates_passed: true
  documentation_complete: true
  tests_passing: true
  code_reviewed: true
---

# TASK-003B-2: Full Review Mode - Display & Basic Actions

## Parent Context

This is **Sub-Task 2 of 4** for TASK-003B (Review Modes & User Interaction).

**Parent Task**: TASK-003B - Review Modes & User Interaction
**Depends On**: TASK-003B-1 (quick review mode - escalation target)
**Blocks**: TASK-003B-3 (modification mode), TASK-003B-4 (Q&A mode), TASK-003C (integration)
**Parallel**: Can parallelize with TASK-003B-3/003B-4 if needed after completion

## Description

Implement the **Full Review Mode** for complex tasks (score 7-10) or escalated tasks (from quick review). This mode provides a comprehensive checkpoint that displays all relevant information and allows users to:
1. **[A]pprove** the plan and proceed to implementation (most common for well-designed plans)
2. **[C]ancel** the task (rare but necessary safety valve)
3. **[M]odify** the plan interactively (implemented in TASK-003B-3)
4. **[V]iew** the complete plan in detail (implemented in TASK-003B-3)
5. **[Q]uestion** the plan rationale (implemented in TASK-003B-4)

This sub-task focuses on the **display infrastructure** and the two simplest actions: **Approve** and **Cancel**. The more complex actions (M/V/Q) are deferred to subsequent sub-tasks.

## Acceptance Criteria

### Phase 1: Full Checkpoint Display ✅ MUST HAVE

- [ ] **Header Section**
  - [ ] Task ID, title, and context
  - [ ] Complexity score with visual indicator (🔴 7-10 / 🟡 4-6 / 🟢 1-3)
  - [ ] Review mode (FULL_REQUIRED or ESCALATED)
  - [ ] Estimated implementation time

- [ ] **Complexity Factors Breakdown**
  - [ ] Display each factor with score and rationale:
    ```
    COMPLEXITY BREAKDOWN:
      📁 File Complexity: 2/3 points
         → 6 files to create/modify (moderate scope)

      🎨 Pattern Familiarity: 1/2 points
         → Uses Strategy pattern (familiar)

      ⚠️  Risk Level: 3/3 points 🔴
         → High risk: Authentication changes
         → High risk: Database schema modification
    ```
  - [ ] Use color indicators for high-risk factors (🔴 = 3, 🟡 = 2, 🟢 = 0-1)
  - [ ] Show force-review triggers if any

- [ ] **Changes Summary Section**
  - [ ] Complete file list (all new files, all modified files)
  - [ ] Each file with brief purpose/changes description
  - [ ] Dependency additions with version info
  - [ ] Test strategy summary

- [ ] **Risk Assessment Section**
  - [ ] List all identified risks by severity (High → Medium → Low)
  - [ ] Mitigation strategy for each risk
  - [ ] Impact and likelihood estimates

- [ ] **Implementation Order Section**
  - [ ] Phased approach with numbered steps
  - [ ] Time estimate per step
  - [ ] Dependencies between steps
  - [ ] Rationale for ordering

- [ ] **Decision Prompt**
  - [ ] Clear list of options with descriptions:
    ```
    DECISION OPTIONS:
      [A] Approve  - Proceed with this plan as-is
      [M] Modify   - Interactively edit the plan (Coming in TASK-003B-3)
      [V] View     - See full implementation plan (Coming in TASK-003B-3)
      [Q] Question - Ask about plan rationale (Coming in TASK-003B-4)
      [C] Cancel   - Return task to backlog

    Your choice (A/M/V/Q/C):
    ```

### Phase 2: Display Infrastructure ✅ MUST HAVE

- [ ] **Formatting Functions**
  - [ ] `display_full_checkpoint(complexity_score, plan, task)` → formatted output
  - [ ] Section rendering with proper spacing and alignment
  - [ ] Box-drawing characters for visual hierarchy
  - [ ] Color support with fallback for plain terminals
  - [ ] Terminal width adaptation (min 80, ideal 120 chars)

- [ ] **Data Extraction**
  - [ ] Extract all data from `ComplexityScore` object
  - [ ] Extract all data from `ImplementationPlan` object
  - [ ] Extract task metadata (ID, title, requirements links)
  - [ ] Extract risk assessment from plan

- [ ] **Scrolling/Paging**
  - [ ] Detect if display exceeds terminal height
  - [ ] Option to use pager (less/more) for long displays
  - [ ] Clear pagination controls if used

### Phase 3: [A]pprove Handler ✅ MUST HAVE

- [ ] **Approval Flow**
  - [ ] Validate 'A' or 'a' input
  - [ ] Display approval confirmation:
    ```
    ✅ Plan approved!
    Proceeding to Phase 3 (Implementation)...
    ```
  - [ ] Update task metadata:
    ```yaml
    implementation_plan:
      approved: true
      approved_by: "user"  # or system username
      approved_at: "2025-10-09T10:30:00Z"
      review_mode: "full_required"  # or "escalated"
      review_duration_seconds: 120  # time spent in review
    ```
  - [ ] Set proceed flag: `proceed_to_phase_3=True`
  - [ ] Log approval decision with all context

- [ ] **Metadata Updates**
  - [ ] Atomic write to task file
  - [ ] Preserve existing metadata
  - [ ] Add approval section to frontmatter
  - [ ] Include complexity evaluation results

### Phase 4: [C]ancel Handler ✅ MUST HAVE

- [ ] **Cancellation Confirmation**
  - [ ] Display confirmation prompt:
    ```
    ⚠️  Are you sure you want to cancel this task?
    All work completed so far will be saved.

    Confirm cancellation? [y/N]:
    ```
  - [ ] Accept 'y'/'Y' for confirmation, anything else aborts
  - [ ] If confirmed:
    - Display "❌ Task cancelled. Moving to backlog..."
    - Update task metadata: `status=backlog`, `cancelled=True`
    - Move task file from `in_progress/` to `backlog/`
    - Save all work (plan file, complexity evaluation)
    - Exit task-work command
  - [ ] If aborted:
    - Display "Cancellation aborted. Returning to checkpoint..."
    - Return to decision prompt

- [ ] **State Management**
  - [ ] Move task file correctly (atomic operation)
  - [ ] Preserve all metadata and history
  - [ ] Update timestamps (cancelled_at)
  - [ ] Clean exit from task-work command

### Phase 5: Input Validation ✅ MUST HAVE

- [ ] **Valid Input Handling**
  - [ ] Accept A/a → route to approve handler
  - [ ] Accept C/c → route to cancel handler
  - [ ] Accept M/m → display "Coming soon (TASK-003B-3)" message
  - [ ] Accept V/v → display "Coming soon (TASK-003B-3)" message
  - [ ] Accept Q/q → display "Coming soon (TASK-003B-4)" message
  - [ ] Trim whitespace from input
  - [ ] Case-insensitive matching

- [ ] **Invalid Input Handling**
  - [ ] Display clear error for unrecognized input:
    ```
    ❌ Invalid choice: 'X'
    Please enter A (Approve), M (Modify), V (View), Q (Question), or C (Cancel)
    ```
  - [ ] Re-display decision prompt
  - [ ] No loss of state or context
  - [ ] Track invalid input attempts (log after 3+ attempts)

- [ ] **Special Key Handling**
  - [ ] Ctrl+C → prompt for confirmation, same as [C]ancel
  - [ ] Empty input (just ENTER) → display help, re-prompt
  - [ ] Multi-character input → use first character only

### Phase 6: Integration with Quick Review Escalation ✅ MUST HAVE

- [ ] **Escalation Context Preservation**
  - [ ] Receive escalation flag from TASK-003B-1
  - [ ] Preserve complexity score from Phase 2.7
  - [ ] Preserve plan reference
  - [ ] Track escalation in metadata:
    ```yaml
    escalation:
      from_mode: "quick_optional"
      escalated_at: "2025-10-09T10:15:00Z"
      reason: "user_requested"
    ```

- [ ] **Display Modifications for Escalated Tasks**
  - [ ] Note at top: "⬆️ Escalated from quick review"
  - [ ] Show escalation timestamp
  - [ ] Otherwise identical display

### Phase 7: Error Handling ✅ MUST HAVE

- [ ] **Display Rendering Errors**
  - [ ] Handle missing plan data gracefully
  - [ ] Handle missing complexity score gracefully
  - [ ] Fallback to simplified display if data incomplete

- [ ] **File System Errors**
  - [ ] Handle task file read errors
  - [ ] Handle task file write errors (approval/cancellation)
  - [ ] Handle task file move errors (cancellation)
  - [ ] Retry logic for transient errors

- [ ] **Terminal Errors**
  - [ ] Handle terminal resize during display
  - [ ] Handle terminal disconnect
  - [ ] Restore terminal state on any error

## Technical Specifications

### Full Review Handler

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Optional

@dataclass
class FullReviewResult:
    """Result of full review interaction"""
    action: Literal["approve", "modify", "view", "question", "cancel"]
    timestamp: datetime
    approved: bool
    metadata_updates: dict
    proceed_to_phase_3: bool

class FullReviewHandler:
    """Handles full review mode for complex tasks"""

    def __init__(
        self,
        complexity_score: ComplexityScore,
        plan: ImplementationPlan,
        task_metadata: dict,
        escalated: bool = False
    ):
        self.complexity_score = complexity_score
        self.plan = plan
        self.task_metadata = task_metadata
        self.escalated = escalated
        self.review_start_time = datetime.now()

    def execute(self) -> FullReviewResult:
        """Execute full review flow"""
        # Display comprehensive checkpoint
        self._display_full_checkpoint()

        # Get user decision
        while True:
            choice = self._prompt_for_decision()

            if choice == 'a':
                return self._handle_approval()
            elif choice == 'c':
                return self._handle_cancellation()
            elif choice == 'm':
                print("⚠️  Modify mode coming soon (TASK-003B-3)")
                # For now, re-prompt
                continue
            elif choice == 'v':
                print("⚠️  View mode coming soon (TASK-003B-3)")
                continue
            elif choice == 'q':
                print("⚠️  Q&A mode coming soon (TASK-003B-4)")
                continue
            else:
                print(f"❌ Invalid choice: '{choice}'")
                print("Please enter A, M, V, Q, or C")
                continue

    def _display_full_checkpoint(self):
        """Display comprehensive checkpoint"""
        print("\n" + "="*70)
        print("🔍 IMPLEMENTATION PLAN REVIEW")
        print("="*70)

        # Header
        self._display_header()

        # Complexity breakdown
        self._display_complexity_breakdown()

        # Changes summary
        self._display_changes_summary()

        # Risk assessment
        self._display_risk_assessment()

        # Implementation order
        self._display_implementation_order()

        print("\n" + "="*70)
        self._display_decision_options()

    def _display_header(self):
        """Display header section"""
        score = self.complexity_score.total_score
        indicator = "🔴" if score >= 7 else "🟡" if score >= 4 else "🟢"

        print(f"\nTask: {self.task_metadata['id']} - {self.task_metadata['title']}")
        print(f"Complexity: {indicator} {score}/10")

        if self.escalated:
            print("⬆️  Escalated from quick review")

        print(f"Estimated Time: ~{self.plan.estimated_duration}")

    def _display_complexity_breakdown(self):
        """Display complexity factors"""
        print("\n📊 COMPLEXITY BREAKDOWN:")

        for factor_score in self.complexity_score.factor_scores:
            max_score = factor_score.max_score
            severity = "🔴" if factor_score.score == max_score else \
                      "🟡" if factor_score.score > 0 else "🟢"

            print(f"\n  {severity} {factor_score.factor_name}: {factor_score.score}/{max_score} points")
            print(f"     → {factor_score.rationale}")

        # Force-review triggers
        if self.complexity_score.forced_review_triggers:
            print("\n  ⚡ FORCE-REVIEW TRIGGERS:")
            for trigger in self.complexity_score.forced_review_triggers:
                print(f"     - {trigger.name}: {trigger.reason}")

    def _display_changes_summary(self):
        """Display changes summary"""
        print("\n📁 CHANGES SUMMARY:")

        print(f"\n  New Files: {len(self.plan.files_to_create)}")
        for file in self.plan.files_to_create:
            print(f"    - {file.path}")
            if file.purpose:
                print(f"      Purpose: {file.purpose}")

        print(f"\n  Modified Files: {len(self.plan.files_to_modify)}")
        for file in self.plan.files_to_modify:
            print(f"    - {file.path}")
            if file.changes:
                print(f"      Changes: {file.changes}")

        if self.plan.new_dependencies:
            print(f"\n  New Dependencies: {len(self.plan.new_dependencies)}")
            for dep in self.plan.new_dependencies:
                print(f"    - {dep.name} ({dep.version})")

        print(f"\n  Tests: {self.plan.test_strategy.total_count} planned")
        print(f"    - Unit: {self.plan.test_strategy.unit_count}")
        print(f"    - Integration: {self.plan.test_strategy.integration_count}")

    def _display_risk_assessment(self):
        """Display risk assessment"""
        print("\n⚠️  RISK ASSESSMENT:")

        risks = self.plan.risks
        for risk in risks:
            severity_icon = "🔴" if risk.severity == "high" else \
                           "🟡" if risk.severity == "medium" else "🟢"

            print(f"\n  {severity_icon} {risk.severity.upper()}: {risk.description}")
            print(f"     Mitigation: {risk.mitigation}")

    def _display_implementation_order(self):
        """Display implementation order"""
        print("\n📋 IMPLEMENTATION ORDER:")

        for i, step in enumerate(self.plan.implementation_steps, 1):
            print(f"\n  {i}. {step.description} (~{step.duration})")
            if step.dependencies:
                print(f"     Dependencies: {', '.join(step.dependencies)}")

    def _display_decision_options(self):
        """Display decision options"""
        print("\nDECISION OPTIONS:")
        print("  [A] Approve  - Proceed with this plan as-is")
        print("  [M] Modify   - Interactively edit the plan (Coming soon)")
        print("  [V] View     - See full implementation plan (Coming soon)")
        print("  [Q] Question - Ask about plan rationale (Coming soon)")
        print("  [C] Cancel   - Return task to backlog")
        print()

    def _prompt_for_decision(self) -> str:
        """Prompt user for decision"""
        choice = input("Your choice (A/M/V/Q/C): ").strip().lower()
        return choice

    def _handle_approval(self) -> FullReviewResult:
        """Handle plan approval"""
        print("\n✅ Plan approved!")
        print("Proceeding to Phase 3 (Implementation)...\n")

        review_duration = (datetime.now() - self.review_start_time).total_seconds()

        return FullReviewResult(
            action="approve",
            timestamp=datetime.now(),
            approved=True,
            metadata_updates={
                "implementation_plan": {
                    "approved": True,
                    "approved_by": "user",
                    "approved_at": datetime.now().isoformat(),
                    "review_mode": "escalated" if self.escalated else "full_required",
                    "review_duration_seconds": int(review_duration)
                }
            },
            proceed_to_phase_3=True
        )

    def _handle_cancellation(self) -> FullReviewResult:
        """Handle task cancellation with confirmation"""
        print("\n⚠️  Are you sure you want to cancel this task?")
        print("All work completed so far will be saved.\n")
        confirm = input("Confirm cancellation? [y/N]: ").strip().lower()

        if confirm == 'y':
            print("\n❌ Task cancelled. Moving to backlog...")
            return FullReviewResult(
                action="cancel",
                timestamp=datetime.now(),
                approved=False,
                metadata_updates={
                    "status": "backlog",
                    "cancelled": True,
                    "cancelled_at": datetime.now().isoformat()
                },
                proceed_to_phase_3=False
            )
        else:
            print("\nCancellation aborted. Returning to checkpoint...")
            # Return to main loop (re-display not needed)
            return None  # Signals to re-prompt
```

## Test Requirements

### Unit Tests

- [ ] **Display Formatting Tests**
  - [ ] Test header rendering with all data
  - [ ] Test complexity breakdown formatting
  - [ ] Test changes summary formatting
  - [ ] Test risk assessment formatting
  - [ ] Test implementation order formatting
  - [ ] Test decision options display

- [ ] **Data Extraction Tests**
  - [ ] Test extraction from ComplexityScore
  - [ ] Test extraction from ImplementationPlan
  - [ ] Test handling of missing data
  - [ ] Test handling of empty lists

- [ ] **Approval Handler Tests**
  - [ ] Test approval flow with valid input
  - [ ] Test metadata updates structure
  - [ ] Test review duration calculation
  - [ ] Test proceed flag set correctly

- [ ] **Cancellation Handler Tests**
  - [ ] Test cancellation with confirmation ('y')
  - [ ] Test cancellation abort ('n' or other)
  - [ ] Test metadata updates for cancellation
  - [ ] Test proceed flag not set

- [ ] **Input Validation Tests**
  - [ ] Test valid inputs (A, M, V, Q, C)
  - [ ] Test case-insensitive (a, A)
  - [ ] Test invalid inputs (X, 123, empty)
  - [ ] Test whitespace handling

### Integration Tests

- [ ] **Full Review Approval Flow**
  - [ ] Task with score=8 → full review displayed
  - [ ] User selects [A]pprove
  - [ ] Metadata updated correctly
  - [ ] Task proceeds to Phase 3

- [ ] **Full Review Cancellation Flow**
  - [ ] Task with score=9 → full review displayed
  - [ ] User selects [C]ancel
  - [ ] Confirmation prompted
  - [ ] User confirms ('y')
  - [ ] Task moved to backlog
  - [ ] Work saved

- [ ] **Escalation from Quick Review**
  - [ ] Task with score=5 → quick review
  - [ ] User escalates (ENTER)
  - [ ] Full review displayed with escalation note
  - [ ] User approves
  - [ ] Metadata includes escalation details

- [ ] **Invalid Input Handling**
  - [ ] User enters invalid choice
  - [ ] Error displayed
  - [ ] Re-prompted without losing state
  - [ ] Eventually enters valid choice

## Success Metrics

### User Experience
- Full review approval rate: 80-90% (target)
- Cancellation rate: <5%
- Invalid input rate: <10%
- Escalation-to-approval rate: 70-80%

### Performance
- Full checkpoint display: <2 seconds
- Metadata update: <500ms
- Task file operations: <1 second

### Quality
- Unit test coverage: ≥85%
- Integration test coverage: 100% of paths (approve, cancel, escalate)
- No data loss on any path
- Atomic state transitions

## File Structure

### Files to Modify (from TASK-003B-1)

```
installer/global/commands/lib/
├── review_modes.py (UPDATE)
│   └── Add FullReviewHandler class
└── user_interaction.py (UPDATE)
    ├── display_full_checkpoint()
    ├── _display_header()
    ├── _display_complexity_breakdown()
    └── ... other display functions

tests/unit/
├── test_full_review.py (NEW)
└── test_display_formatting.py (NEW)

tests/integration/
├── test_full_review_flow.py (NEW)
└── test_escalation_flow.py (NEW)
```

## Dependencies

### Internal Dependencies
- ✅ TASK-003A: ComplexityScore, ImplementationPlan models
- ✅ TASK-003B-1: QuickReviewHandler (escalation source)

### External Dependencies
- Python 3.8+ standard library only

## Blocks

### Immediate
- ⏸️ TASK-003B-3 (Modification/View) - needs [M] and [V] handler targets
- ⏸️ TASK-003B-4 (Q&A) - needs [Q] handler target
- ⏸️ TASK-003C (Integration) - needs full review mode functional

## Out of Scope

Explicitly **NOT** in this sub-task:
- ❌ [M]odify handler implementation (TASK-003B-3)
- ❌ [V]iew handler implementation (TASK-003B-3)
- ❌ [Q]uestion handler implementation (TASK-003B-4)
- ❌ Plan editing/versioning (TASK-003B-3)
- ❌ Interactive Q&A (TASK-003B-4)

**For now**: M/V/Q display "Coming soon" message and re-prompt

## Estimated Effort

**1 day** (6-8 hours):
- Display infrastructure: 2 hours
- Approve handler: 1 hour
- Cancel handler: 1 hour
- Input validation: 1 hour
- Escalation integration: 1 hour
- Unit tests: 1.5 hours
- Integration tests: 1 hour
- Documentation: 30 minutes

**Complexity**: 5/10 (Moderate-Complex)
- Display formatting requires care
- Many display sections to implement
- State management for cancellation
- Otherwise straightforward

---

**Ready for implementation after TASK-003B-1 completion** ✅
