---
id: TASK-003B-1
title: Quick Review Mode - Countdown Timer & Basic Input
status: completed
created: 2025-10-09T16:30:00Z
updated: 2025-10-09T17:45:00Z
completed: 2025-10-09T17:45:00Z
assignee: null
priority: high
tags: [workflow-enhancement, user-interaction, quick-review, countdown-timer, phase-2.8]
requirements: []
bdd_scenarios: []
parent_task: TASK-003B
dependencies: [TASK-003A]
blocks: [TASK-003B-2]
test_results:
  status: passed
  last_run: 2025-10-09T17:30:00Z
  coverage:
    line: 100
    branch: 84
  passed: 14
  failed: 0
  execution_log: "All 14 tests passed. Component coverage: 100%, Branch coverage: 84%"
blocked_reason: null
quality_gates:
  compilation: passed
  tests_passing: passed
  line_coverage: passed
  branch_coverage: passed
  code_review: passed
  architectural_review: passed
implementation_summary:
  files_created:
    - installer/global/commands/lib/user_interaction.py
    - installer/global/commands/lib/review_modes.py
    - installer/global/commands/lib/test_quick_review.py
  lines_of_code: 1135
  quality_score: 94
  architecture_score: 95
---

# TASK-003B-1: Quick Review Mode - Countdown Timer & Basic Input

## Parent Context

This is **Sub-Task 1 of 4** for TASK-003B (Review Modes & User Interaction).

**Parent Task**: TASK-003B - Review Modes & User Interaction
**Depends On**: TASK-003A (complexity calculation - completed ✅)
**Blocks**: TASK-003B-2 (full review mode)
**Parallel**: None (foundation sub-task)

## Description

Implement the **Quick Review Mode** for medium-complexity tasks (score 4-6). This mode provides a 10-second countdown timer that allows users to:
1. **Auto-proceed** to implementation if no input (most common path)
2. **Escalate** to full review by pressing ENTER (for closer inspection)
3. **Cancel** the task by pressing 'c' (rare but necessary)

**Key Innovation**: Non-blocking countdown that respects user agency while optimizing for the common case (auto-proceed).

## Acceptance Criteria

### Phase 1: Countdown Timer Implementation ✅ MUST HAVE

- [ ] **Non-Blocking Countdown Timer**
  - [ ] Count down from 10 to 0, displaying each second
  - [ ] Update display every second: "⏰ Proceeding in 10... 9... 8..."
  - [ ] Use `select()` (Unix/Linux/macOS) or `msvcrt` (Windows) for non-blocking I/O
  - [ ] Detect user input at any point during countdown
  - [ ] Maintain accurate timing (±100ms tolerance per second)
  - [ ] Return user input character or 'timeout' string

- [ ] **Display Formatting**
  - [ ] Clear, visible countdown indicator
  - [ ] Updates on same line (using `\r` carriage return)
  - [ ] No screen flicker or artifacts
  - [ ] Restore terminal state on exit

- [ ] **Platform Compatibility**
  - [ ] Works on macOS (using `select()`)
  - [ ] Works on Linux (using `select()`)
  - [ ] Works on Windows (using `msvcrt.kbhit()` and `msvcrt.getch()`)
  - [ ] Graceful fallback if non-blocking I/O unavailable

### Phase 2: Quick Review Display ✅ MUST HAVE

- [ ] **Summary Card Rendering**
  - [ ] Display complexity score: "📊 Complexity: 5/10 (Medium)"
  - [ ] Box-drawing characters for visual separation
  - [ ] Changes summary section:
    ```
    CHANGES SUMMARY:
      📁 New Files: 3
         - src/features/auth/AuthService.ts
         - src/features/auth/TokenService.ts
      ✏️  Modified Files: 1
         - src/api/routes/index.ts (add auth routes)
      🧪 Tests Planned: 8
      ⏱️  Estimated: ~40 minutes
    ```
  - [ ] Clear instruction: "[Press ENTER to review plan in detail]"
  - [ ] Cancel instruction: "[Press 'c' to cancel]"

- [ ] **Data Extraction from Phase 2.7**
  - [ ] Read `ComplexityScore` from Phase 2.7 output
  - [ ] Read `ImplementationPlan` reference
  - [ ] Extract file counts (new vs. modified)
  - [ ] Extract test count estimate
  - [ ] Extract time estimate

### Phase 3: Input Handling ✅ MUST HAVE

- [ ] **ENTER Key Handler**
  - [ ] Detect ENTER press during countdown
  - [ ] Stop countdown immediately
  - [ ] Preserve all context (complexity score, plan reference)
  - [ ] Set escalation flag: `escalated=True`
  - [ ] Return control to task-manager for full review display
  - [ ] Log escalation action with timestamp

- [ ] **'c' Key Handler (Cancel)**
  - [ ] Detect 'c' key press (case-insensitive)
  - [ ] Stop countdown immediately
  - [ ] Display cancellation confirmation
  - [ ] Move task from `in_progress/` to `backlog/`
  - [ ] Update task metadata: `status=backlog`, `cancelled=True`
  - [ ] Save all work completed (plan file, complexity evaluation)
  - [ ] Exit task-work command cleanly

- [ ] **Timeout Handler (Auto-Proceed)**
  - [ ] Detect countdown reaching 0 with no input
  - [ ] Display "⚡ Auto-proceeding to implementation..."
  - [ ] Update task metadata: `auto_approved=True`, `approved_at=<timestamp>`
  - [ ] Set proceed flag: `proceed_to_phase_3=True`
  - [ ] Return control to task-manager for Phase 3
  - [ ] Log auto-proceed decision

- [ ] **Invalid Key Handler**
  - [ ] Detect other key presses (not ENTER or 'c')
  - [ ] Ignore silently (continue countdown)
  - [ ] No error message displayed (avoid clutter during countdown)

### Phase 4: Integration with Phase 2.7 ✅ MUST HAVE

- [ ] **Input from complexity-evaluator**
  - [ ] Receive `ComplexityScore` object
  - [ ] Receive `ReviewDecision` with mode=QUICK_OPTIONAL
  - [ ] Receive `ImplementationPlan` reference
  - [ ] Receive task metadata

- [ ] **Output to task-manager**
  - [ ] Return decision: `proceed`, `escalate`, or `cancel`
  - [ ] Return updated task metadata
  - [ ] Return context for next phase (full review or implementation)

### Phase 5: Error Handling ✅ MUST HAVE

- [ ] **Terminal State Recovery**
  - [ ] Restore terminal mode on exit
  - [ ] Handle Ctrl+C gracefully (confirm cancellation)
  - [ ] Handle terminal resize without crash
  - [ ] Handle terminal disconnect gracefully

- [ ] **Timing Edge Cases**
  - [ ] Handle system clock changes during countdown
  - [ ] Handle very slow terminals (>1s render time)
  - [ ] Handle rapid key presses (buffer overflow)

- [ ] **File System Errors**
  - [ ] Handle task file read errors
  - [ ] Handle task file write errors (cancellation)
  - [ ] Ensure atomic metadata updates

## Technical Specifications

### Countdown Timer Implementation

```python
import select
import sys
import time
from typing import Literal

def countdown_timer(
    seconds: int = 10,
    prompt: str = "⏰ Proceeding in"
) -> Literal["timeout", "enter", "cancel"]:
    """
    Non-blocking countdown timer with user input detection.

    Args:
        seconds: Countdown duration in seconds
        prompt: Display message before countdown

    Returns:
        "timeout" if countdown completes
        "enter" if user presses ENTER
        "cancel" if user presses 'c'
    """
    # Platform-specific implementation
    if sys.platform == 'win32':
        return _countdown_windows(seconds, prompt)
    else:
        return _countdown_unix(seconds, prompt)

def _countdown_unix(seconds: int, prompt: str) -> str:
    """Unix/Linux/macOS implementation using select()"""
    import termios
    import tty

    # Save terminal settings
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        # Set terminal to raw mode (no buffering)
        tty.setraw(fd)

        for remaining in range(seconds, 0, -1):
            sys.stdout.write(f"\r{prompt} {remaining}... ")
            sys.stdout.flush()

            # Wait for input or 1 second timeout
            readable, _, _ = select.select([sys.stdin], [], [], 1.0)

            if readable:
                char = sys.stdin.read(1)
                if char == '\r' or char == '\n':  # ENTER
                    return "enter"
                elif char.lower() == 'c':  # Cancel
                    return "cancel"
                # Other keys ignored

        return "timeout"

    finally:
        # Restore terminal settings
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        sys.stdout.write("\n")
        sys.stdout.flush()

def _countdown_windows(seconds: int, prompt: str) -> str:
    """Windows implementation using msvcrt"""
    import msvcrt

    for remaining in range(seconds, 0, -1):
        sys.stdout.write(f"\r{prompt} {remaining}... ")
        sys.stdout.flush()

        # Check for key press every 100ms (total 1 second)
        for _ in range(10):
            if msvcrt.kbhit():
                char = msvcrt.getch().decode('utf-8', errors='ignore')
                if char == '\r' or char == '\n':
                    return "enter"
                elif char.lower() == 'c':
                    return "cancel"
            time.sleep(0.1)

    return "timeout"
```

### Quick Review Handler

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Literal

@dataclass
class QuickReviewResult:
    """Result of quick review interaction"""
    action: Literal["proceed", "escalate", "cancel"]
    timestamp: datetime
    auto_approved: bool
    metadata_updates: dict

class QuickReviewHandler:
    """Handles quick review mode for medium-complexity tasks"""

    def __init__(self, complexity_score: ComplexityScore, plan: ImplementationPlan):
        self.complexity_score = complexity_score
        self.plan = plan

    def execute(self) -> QuickReviewResult:
        """Execute quick review flow"""
        # Display summary
        self._display_summary()

        # Start countdown
        result = countdown_timer(seconds=10)

        # Handle result
        if result == "timeout":
            return self._handle_timeout()
        elif result == "enter":
            return self._handle_escalation()
        elif result == "cancel":
            return self._handle_cancellation()

    def _display_summary(self):
        """Display quick review summary card"""
        print(f"\n📊 Complexity: {self.complexity_score.total_score}/10 (Medium)")
        print("\n╔═══════════════════════════════════════════════════════╗")
        print("║ 📋 QUICK IMPLEMENTATION REVIEW                        ║")
        print("╚═══════════════════════════════════════════════════════╝")
        print("\nCHANGES SUMMARY:")

        # Files
        new_files = len(self.plan.files_to_create)
        modified_files = len(self.plan.files_to_modify)
        print(f"  📁 New Files: {new_files}")
        for file in self.plan.files_to_create[:3]:  # Show first 3
            print(f"     - {file}")
        if new_files > 3:
            print(f"     ... and {new_files - 3} more")

        print(f"  ✏️  Modified Files: {modified_files}")
        # ... similar display logic

        print(f"  🧪 Tests Planned: {self.plan.test_count}")
        print(f"  ⏱️  Estimated: ~{self.plan.estimated_duration}")
        print("\n  [Press ENTER to review plan in detail]")
        print("  [Press 'c' to cancel]")

    def _handle_timeout(self) -> QuickReviewResult:
        """Handle countdown timeout (auto-proceed)"""
        print("\n⚡ Auto-proceeding to implementation...")
        return QuickReviewResult(
            action="proceed",
            timestamp=datetime.now(),
            auto_approved=True,
            metadata_updates={
                "auto_approved": True,
                "approved_at": datetime.now().isoformat(),
                "review_mode": "quick_optional",
                "review_duration_seconds": 10
            }
        )

    def _handle_escalation(self) -> QuickReviewResult:
        """Handle ENTER press (escalate to full review)"""
        print("\n🔍 Escalating to full review...")
        return QuickReviewResult(
            action="escalate",
            timestamp=datetime.now(),
            auto_approved=False,
            metadata_updates={
                "escalated": True,
                "escalated_at": datetime.now().isoformat(),
                "review_mode": "full_required"
            }
        )

    def _handle_cancellation(self) -> QuickReviewResult:
        """Handle 'c' press (cancel task)"""
        print("\n❌ Task cancelled. Moving to backlog...")
        return QuickReviewResult(
            action="cancel",
            timestamp=datetime.now(),
            auto_approved=False,
            metadata_updates={
                "cancelled": True,
                "cancelled_at": datetime.now().isoformat(),
                "status": "backlog"
            }
        )
```

## Test Requirements

### Unit Tests

- [ ] **Countdown Timer Tests**
  - [ ] Test full countdown with no input → returns "timeout"
  - [ ] Test ENTER press at 5 seconds → returns "enter"
  - [ ] Test 'c' press at 7 seconds → returns "cancel"
  - [ ] Test 'C' press (uppercase) → returns "cancel"
  - [ ] Test invalid key press → ignored, countdown continues
  - [ ] Test rapid key presses → first recognized, others buffered
  - [ ] Test timing accuracy (±100ms tolerance)

- [ ] **Display Tests**
  - [ ] Test summary card formatting
  - [ ] Test file list truncation (show first 3, "... and X more")
  - [ ] Test Unicode box-drawing characters render correctly
  - [ ] Test terminal width handling (min 80 chars)

- [ ] **Handler Tests**
  - [ ] Test timeout handler → action="proceed", auto_approved=True
  - [ ] Test escalation handler → action="escalate", escalated=True
  - [ ] Test cancellation handler → action="cancel", cancelled=True
  - [ ] Test metadata updates structure and content

### Integration Tests

- [ ] **End-to-End Quick Review Flow**
  - [ ] Task with score=5 → quick review displayed
  - [ ] Timeout occurs → task proceeds to Phase 3
  - [ ] Task metadata updated correctly

- [ ] **Escalation Flow**
  - [ ] Quick review displayed
  - [ ] User presses ENTER within 10s
  - [ ] Control returned to task-manager
  - [ ] Context preserved (complexity score, plan reference)
  - [ ] Metadata includes escalation timestamp

- [ ] **Cancellation Flow**
  - [ ] Quick review displayed
  - [ ] User presses 'c' within 10s
  - [ ] Task moved from in_progress/ to backlog/
  - [ ] Task file updated with cancelled=True
  - [ ] Work saved (plan file exists)

## Success Metrics

### Performance
- Countdown timing accuracy: ±100ms per second (±1s over 10s)
- Display render time: <500ms
- Input detection latency: <50ms

### User Experience
- Auto-proceed rate: 60-70% (target - most users skip)
- Escalation rate: 30-40% (some users review)
- Cancellation rate: <5%

### Quality
- Unit test coverage: ≥85%
- Integration test coverage: 100% of user paths
- No terminal state corruption on exit
- No input buffering issues

## File Structure

### Files to Create

```
installer/global/commands/lib/
├── review_modes.py (NEW)
│   └── QuickReviewHandler class
└── user_interaction.py (NEW)
    ├── countdown_timer()
    ├── _countdown_unix()
    └── _countdown_windows()

tests/unit/
├── test_countdown_timer.py (NEW)
└── test_quick_review.py (NEW)

tests/integration/
└── test_quick_review_flow.py (NEW)
```

### Files to Modify

```
installer/global/agents/task-manager.md (UPDATE)
└── Add Phase 2.8 invocation (quick review mode)
```

## Dependencies

### External Dependencies
- Python 3.8+ standard library:
  - `select` (Unix/Linux/macOS)
  - `msvcrt` (Windows)
  - `termios`, `tty` (Unix terminal control)
  - `time`, `sys`

### Internal Dependencies
- ✅ TASK-003A: `ComplexityScore`, `ImplementationPlan`, `ReviewDecision` models

## Blocks

### Immediate
- ⏸️ TASK-003B-2 (Full Review Mode) - needs escalation target

## Out of Scope

Explicitly **NOT** in this sub-task:
- ❌ Full review mode display (TASK-003B-2)
- ❌ Modify/View handlers (TASK-003B-3)
- ❌ Q&A mode (TASK-003B-4)
- ❌ Plan modification (TASK-003B-3)
- ❌ Plan versioning (TASK-003B-3)

## Estimated Effort

**1 day** (6-8 hours):
- Countdown timer implementation: 2 hours
- Quick review display: 1 hour
- Input handlers: 2 hours
- Unit tests: 2 hours
- Integration tests: 1 hour
- Documentation: 30 minutes

**Complexity**: 4/10 (Moderate)
- Countdown timer is tricky (non-blocking I/O)
- Platform compatibility requires care
- Otherwise straightforward

---

**Ready for implementation after TASK-003A completion** ✅
