# TASK-003C: Implementation Architecture Design
## Integration of Phase 2.7 and Phase 2.8 into task-work Workflow

**Status**: Draft
**Created**: 2025-10-10
**Author**: Software Architect
**Scope**: Phase 2.7 (Plan Generation + Complexity Evaluation) and Phase 2.8 (Human Plan Checkpoint) integration

---

## Executive Summary

This document provides the complete implementation architecture for integrating Phase 2.7 (Plan Generation + Complexity Evaluation) and Phase 2.8 (Human Plan Checkpoint) into the existing task-work workflow. The design leverages existing implementations from TASK-003A (complexity models) and TASK-003B-1 (quick review mode) while adding new orchestration logic and routing components.

**Key Innovation**: Phase 2.7 routes tasks based on complexity score (1-10 scale) to three different review modes:
- **AUTO_PROCEED (score 1-3)**: Display summary, proceed to Phase 3 immediately
- **QUICK_OPTIONAL (score 4-6)**: 10-second countdown with optional escalation (IMPLEMENTED ✅)
- **FULL_REQUIRED (score 7-10 or triggers)**: Mandatory comprehensive review checkpoint

**Implementation Complexity**: 6/10 (Medium-High)
**Estimated Duration**: 3-4 days
**Risk Level**: Medium (integration complexity, state management)

---

## Table of Contents

1. [Architecture Decisions](#1-architecture-decisions)
2. [Pattern Selection](#2-pattern-selection)
3. [Component Structure](#3-component-structure)
4. [Key Integration Points](#4-key-integration-points)
5. [Critical Dependencies](#5-critical-dependencies)
6. [Implementation Plan](#6-implementation-plan)
7. [Risk Assessment](#7-risk-assessment)
8. [Testing Strategy](#8-testing-strategy)
9. [Success Metrics](#9-success-metrics)

---

## 1. Architecture Decisions

### 1.1 Orchestration Strategy

**Decision**: Extend task-manager.md with Phase 2.7 and Phase 2.8 orchestration logic

**Rationale**:
- task-manager.md is already the orchestrator for all task-work phases
- Maintains single point of control for workflow transitions
- Existing pattern: task-work.md → task-manager.md → specialized agents
- Minimizes changes to task-work.md (only add Phase 2.7/2.8 invocations)

**Alternative Considered**: Create separate orchestrator agent
- **Rejected**: Adds complexity, splits responsibility, harder to maintain

**Implementation Approach**:
```markdown
# task-manager.md (UPDATED)

## Phase 2.7 Orchestration

After Phase 2 (Implementation Planning) completes:

1. **Invoke Plan Generation Specialist** (if not already formatted)
   - Parse Phase 2 output into structured ImplementationPlan
   - Extract: files, dependencies, patterns, risks, phases
   - Save to: `docs/state/{task_id}/implementation_plan_v1.json`

2. **Invoke Complexity Calculator**
   - Use complexity_calculator.py (from TASK-003A)
   - Calculate score (1-10 scale) based on:
     - File complexity factor (0-3 points)
     - Pattern familiarity factor (0-2 points)
     - Risk level factor (0-3 points)
     - External dependencies factor (0-2 points)
   - Detect force-review triggers
   - Determine ReviewMode (AUTO_PROCEED/QUICK_OPTIONAL/FULL_REQUIRED)
   - Save to: `docs/state/{task_id}/complexity_score_v1.json`

3. **Route to Phase 2.8** based on ReviewMode
   - AUTO_PROCEED → Display summary → Phase 3
   - QUICK_OPTIONAL → QuickReviewHandler → (timeout → Phase 3) OR (enter → Full review) OR (cancel → backlog)
   - FULL_REQUIRED → FullReviewHandler → (approve → Phase 3) OR (modify → Phase 2.7 loop) OR (cancel → backlog)

## Phase 2.8 Orchestration

### Auto-Proceed Path (ReviewMode.AUTO_PROCEED)

Display complexity summary:
```
✅ Low Complexity Task (Score: 2/10)

CHANGES SUMMARY:
  📁 Files: 1 file (~50 lines)
  🎯 Patterns: Simple CRUD operation
  ⏱️  Estimated: ~30 minutes

Auto-proceeding to implementation...
```

Update task metadata:
- `review_mode: "auto_proceed"`
- `auto_approved: true`
- `complexity_score: 2`

Proceed directly to Phase 3 (Implementation)

### Quick Optional Path (ReviewMode.QUICK_OPTIONAL)

Invoke QuickReviewHandler (from TASK-003B-1):
- Display summary card
- Start 10-second countdown
- Handle user input:
  - timeout → auto-approve → Phase 3
  - enter → escalate to FullReviewHandler
  - cancel → move to backlog, exit

### Full Required Path (ReviewMode.FULL_REQUIRED)

Invoke FullReviewHandler:
- Display comprehensive checkpoint (from TASK-003B-2)
- Prompt for decision [A/M/V/Q/C]
- Handle decision:
  - [A] Approve → Phase 3
  - [M] Modify → Enter modification session → Apply changes → Re-run Phase 2.7 → Phase 2.8 again
  - [V] View → Show plan in pager → Re-prompt
  - [Q] Question → Q&A session → Re-prompt
  - [C] Cancel → Move to backlog, exit

### Modification Loop

When user chooses [M]odify:
1. Enter ModificationSession (interactive editor)
2. Apply modifications → Create new ImplementationPlan version
3. Re-run complexity calculator → New ComplexityScore
4. Re-enter Phase 2.8 with modified plan
5. Display updated checkpoint
6. User makes final decision (approve/cancel)

**Critical**: Modification loop prevents infinite cycles:
- Track modification count in task metadata
- Warn after 3 modification cycles
- Force decision after 5 modification cycles
```

### 1.2 State Management Strategy

**Decision**: Use filesystem-based state management with JSON persistence

**Rationale**:
- Consistent with existing system (task files in tasks/*, docs/requirements/*, etc.)
- Version-controllable (git-friendly)
- Easy to inspect and debug
- No database dependency
- Atomic writes via temp file pattern (already implemented in user_interaction.py)

**State Storage Locations**:
```
docs/state/{task_id}/
├── implementation_plan_v1.json        # Original plan from Phase 2
├── implementation_plan_v2.json        # After first modification (if modified)
├── complexity_score_v1.json           # Original complexity evaluation
├── complexity_score_v2.json           # Re-evaluated after modification
├── review_session.json                # Phase 2.8 session metadata
├── modification_sessions/
│   ├── session_001.json              # First modification session
│   └── session_002.json              # Second modification session
└── qa_sessions/
    ├── qa_001.json                   # Q&A session transcripts
    └── qa_002.json
```

**Alternative Considered**: In-memory state with task file frontmatter only
- **Rejected**: Too much data for frontmatter, harder to version, harder to debug

### 1.3 Routing Logic Design

**Decision**: Three-tier routing based on complexity score + force triggers

**Routing Table**:
| Complexity Score | Force Triggers | Review Mode | Phase 2.8 Path |
|-----------------|----------------|-------------|----------------|
| 1-3 | None | AUTO_PROCEED | Display summary → Phase 3 |
| 1-3 | Any trigger | FULL_REQUIRED | Mandatory checkpoint |
| 4-6 | None | QUICK_OPTIONAL | 10s countdown (optional escalation) |
| 4-6 | Any trigger | FULL_REQUIRED | Mandatory checkpoint |
| 7-10 | Any/None | FULL_REQUIRED | Mandatory checkpoint |

**Force Triggers** (from complexity_models.py):
- USER_FLAG (`--review` flag)
- SECURITY_KEYWORDS (auth, password, encryption, etc.)
- BREAKING_CHANGES (public API modifications)
- SCHEMA_CHANGES (database migrations)
- HOTFIX (production hotfix tag)

**Rationale**:
- Clear, predictable routing based on objective criteria
- Safety-first: any risk indicator → full review
- Optimizes common case (low complexity → auto-proceed)
- Respects user intent (`--review` flag)

### 1.4 Error Handling Strategy

**Decision**: Fail-safe escalation with graceful degradation

**Error Handling Hierarchy**:
```python
# Phase 2.7 Errors
try:
    plan = parse_implementation_plan(phase_2_output)
    complexity_score = calculate_complexity(plan)
    review_mode = determine_review_mode(complexity_score)
except PlanParsingError:
    # Fail-safe: Escalate to full review
    review_mode = ReviewMode.FULL_REQUIRED
    log_error("Plan parsing failed, escalating to full review for safety")
except ComplexityCalculationError:
    # Fail-safe: Assume high complexity
    review_mode = ReviewMode.FULL_REQUIRED
    log_error("Complexity calculation failed, assuming high complexity")

# Phase 2.8 Errors
try:
    if review_mode == ReviewMode.QUICK_OPTIONAL:
        result = quick_review_handler.execute()
except CountdownError:
    # Fail-safe: Escalate to full review
    result = full_review_handler.execute()
    log_error("Quick review failed, escalating to full review")
except KeyboardInterrupt:
    # User interrupt: Treat as cancellation request
    handle_cancellation()
    sys.exit(0)
```

**Rationale**:
- Never auto-proceed on errors (safety-first)
- Always give user final control
- Log all errors for debugging
- Preserve all work completed so far

---

## 2. Pattern Selection

### 2.1 Orchestration Pattern: Chain of Responsibility

**Pattern**: Chain of Responsibility with conditional routing

**Implementation**:
```python
class Phase27Handler:
    """Handler for Phase 2.7 - Plan Generation + Complexity Evaluation"""

    def __init__(self, next_handler: Optional['Phase28Handler'] = None):
        self.next_handler = next_handler

    def handle(self, context: TaskContext) -> TaskContext:
        # Step 1: Generate structured plan
        plan = self.generate_plan(context.phase_2_output)
        context.implementation_plan = plan

        # Step 2: Calculate complexity
        complexity_score = self.calculate_complexity(plan, context)
        context.complexity_score = complexity_score

        # Step 3: Determine review mode
        review_mode = self.determine_review_mode(complexity_score)
        context.review_mode = review_mode

        # Step 4: Persist state
        self.save_state(context)

        # Step 5: Pass to next handler
        if self.next_handler:
            return self.next_handler.handle(context)
        return context

class Phase28Handler:
    """Handler for Phase 2.8 - Human Plan Checkpoint"""

    def __init__(self, next_handler: Optional['Phase3Handler'] = None):
        self.next_handler = next_handler

    def handle(self, context: TaskContext) -> TaskContext:
        # Route based on review mode
        if context.review_mode == ReviewMode.AUTO_PROCEED:
            return self.handle_auto_proceed(context)
        elif context.review_mode == ReviewMode.QUICK_OPTIONAL:
            return self.handle_quick_review(context)
        elif context.review_mode == ReviewMode.FULL_REQUIRED:
            return self.handle_full_review(context)

    def handle_full_review(self, context: TaskContext) -> TaskContext:
        result = FullReviewHandler(...).execute()

        if result.action == "approve":
            # Proceed to Phase 3
            return self.next_handler.handle(context)
        elif result.action == "modify":
            # Loop back to Phase 2.7 with modified plan
            phase_27_handler = Phase27Handler(next_handler=self)
            context.implementation_plan = result.modified_plan
            return phase_27_handler.handle(context)
        elif result.action == "cancel":
            # Exit workflow
            context.status = "cancelled"
            return context
```

**Rationale**:
- Clear separation of concerns (each phase is a handler)
- Easy to test in isolation
- Supports modification loop (handler can call previous handler)
- Extensible (easy to add Phase 2.9, etc.)

### 2.2 State Machine Pattern: ReviewMode Routing

**Pattern**: State Machine with three states and transition table

**State Diagram**:
```
┌─────────────────────────────────────────────────────────┐
│                    Phase 2.7                            │
│          (Plan Generation + Complexity)                 │
└──────────────┬──────────────────────────────────────────┘
               │
               ▼
        ┌──────────────┐
        │ ReviewMode?  │
        └──────┬───────┘
               │
       ┌───────┴────────┬────────────────────┐
       │                │                    │
       ▼                ▼                    ▼
┌─────────────┐  ┌─────────────┐   ┌─────────────────┐
│AUTO_PROCEED │  │QUICK_OPT    │   │FULL_REQUIRED    │
│(score 1-3)  │  │(score 4-6)  │   │(score 7-10 or   │
│             │  │             │   │ force triggers) │
└──────┬──────┘  └──────┬──────┘   └────────┬────────┘
       │                │                    │
       ▼                ▼                    ▼
  Display        QuickReviewHandler    FullReviewHandler
  Summary                │                   │
       │          ┌──────┴─────┬────────────┼────────────┐
       │          │            │            │            │
       │          ▼            ▼            ▼            ▼            ▼
       │      timeout      enter      [A]pprove    [M]odify    [C]ancel
       │          │            │            │            │            │
       │          │            │            │            ▼            │
       │          │            │            │    ModificationSession  │
       │          │            │            │            │            │
       │          │            └────────────┼────────────┘            │
       │          │                         │                         │
       └──────────┴─────────────────────────┼─────────────────────────┤
                                            │                         │
                                            ▼                         ▼
                                      Phase 3 (Implementation)    Backlog
```

**Transition Table**:
| Current State | User Action | Next State | Side Effects |
|--------------|-------------|------------|--------------|
| AUTO_PROCEED | (automatic) | Phase 3 | Update metadata: auto_approved=true |
| QUICK_OPTIONAL | timeout | Phase 3 | Update metadata: auto_approved=true |
| QUICK_OPTIONAL | enter | FULL_REQUIRED | Escalate: escalated=true |
| QUICK_OPTIONAL | cancel | Backlog | Move task file, update status |
| FULL_REQUIRED | approve | Phase 3 | Update metadata: approved=true |
| FULL_REQUIRED | modify | Phase 2.7 | Create plan version, re-calculate complexity |
| FULL_REQUIRED | view | FULL_REQUIRED (same) | Display in pager, re-prompt |
| FULL_REQUIRED | question | FULL_REQUIRED (same) | Q&A session, re-prompt |
| FULL_REQUIRED | cancel | Backlog | Move task file, update status |

**Implementation**:
```python
from enum import Enum

class ReviewState(Enum):
    AUTO_PROCEED = "auto_proceed"
    QUICK_OPTIONAL = "quick_optional"
    FULL_REQUIRED = "full_required"
    PHASE_3 = "phase_3"
    BACKLOG = "backlog"

class ReviewStateMachine:
    def __init__(self, initial_state: ReviewState):
        self.current_state = initial_state
        self.history = [initial_state]

    def transition(self, action: str, context: TaskContext) -> ReviewState:
        # Define transition table
        transitions = {
            (ReviewState.AUTO_PROCEED, "auto"): self._auto_proceed,
            (ReviewState.QUICK_OPTIONAL, "timeout"): self._quick_timeout,
            (ReviewState.QUICK_OPTIONAL, "enter"): self._quick_escalate,
            (ReviewState.QUICK_OPTIONAL, "cancel"): self._cancel,
            (ReviewState.FULL_REQUIRED, "approve"): self._approve,
            (ReviewState.FULL_REQUIRED, "modify"): self._modify,
            (ReviewState.FULL_REQUIRED, "view"): self._view,
            (ReviewState.FULL_REQUIRED, "question"): self._question,
            (ReviewState.FULL_REQUIRED, "cancel"): self._cancel,
        }

        handler = transitions.get((self.current_state, action))
        if handler:
            new_state = handler(context)
            self.history.append(new_state)
            self.current_state = new_state
            return new_state
        else:
            raise ValueError(f"Invalid transition: {self.current_state} + {action}")
```

### 2.3 Command Pattern: Decision Handlers

**Pattern**: Command Pattern for Phase 2.8 user decisions

**Implementation**:
```python
from abc import ABC, abstractmethod

class ReviewCommand(ABC):
    """Abstract base for review decision commands"""

    @abstractmethod
    def execute(self, context: TaskContext) -> TaskContext:
        """Execute the command and return updated context"""
        pass

    @abstractmethod
    def undo(self, context: TaskContext) -> TaskContext:
        """Undo the command (for modification rollback)"""
        pass

class ApproveCommand(ReviewCommand):
    def execute(self, context: TaskContext) -> TaskContext:
        context.approved = True
        context.proceed_to_phase_3 = True
        context.update_metadata({
            "approved": True,
            "approved_at": datetime.utcnow().isoformat(),
        })
        return context

class ModifyCommand(ReviewCommand):
    def __init__(self, modification_session: ModificationSession):
        self.modification_session = modification_session

    def execute(self, context: TaskContext) -> TaskContext:
        # Apply modifications
        modified_plan = self.modification_session.apply()

        # Re-calculate complexity
        new_complexity = calculate_complexity(modified_plan)

        # Update context
        context.implementation_plan = modified_plan
        context.complexity_score = new_complexity
        context.plan_version += 1

        # Loop back to Phase 2.8
        context.proceed_to_phase_28 = True
        return context

    def undo(self, context: TaskContext) -> TaskContext:
        # Restore previous plan version
        context.implementation_plan = self.modification_session.original_plan
        context.complexity_score = self.modification_session.original_complexity
        context.plan_version -= 1
        return context

class CancelCommand(ReviewCommand):
    def execute(self, context: TaskContext) -> TaskContext:
        context.status = "backlog"
        context.cancelled = True
        context.update_metadata({
            "cancelled": True,
            "cancelled_at": datetime.utcnow().isoformat(),
        })
        # Move task file
        move_task_to_backlog(context.task_file_path)
        return context

# Usage
commands = {
    "approve": ApproveCommand(),
    "modify": ModifyCommand(modification_session),
    "cancel": CancelCommand(),
}

command = commands[user_choice]
context = command.execute(context)
```

**Rationale**:
- Encapsulates decision logic
- Easy to test (each command is independent)
- Supports undo (for modification rollback)
- Clean separation of concerns

### 2.4 Template Pattern: Stack-Specific Specialists

**Pattern**: Template Method for stack-specific plan generation

**Current Challenge**: Phase 2 planning agents (python-api-specialist, react-state-specialist, etc.) output free-form markdown. We need structured ImplementationPlan objects.

**Solution**: Introduce PlanParser template with stack-specific implementations

**Implementation**:
```python
from abc import ABC, abstractmethod

class PlanParser(ABC):
    """Template for parsing stack-specific plan output"""

    def parse(self, raw_plan: str, task_id: str) -> ImplementationPlan:
        """Template method - calls steps in order"""
        files = self.extract_files(raw_plan)
        patterns = self.extract_patterns(raw_plan)
        dependencies = self.extract_dependencies(raw_plan)
        loc = self.extract_loc_estimate(raw_plan)
        risks = self.extract_risks(raw_plan)
        phases = self.extract_phases(raw_plan)
        duration = self.extract_duration(raw_plan)

        return ImplementationPlan(
            task_id=task_id,
            files_to_create=files,
            patterns_used=patterns,
            external_dependencies=dependencies,
            estimated_loc=loc,
            risk_indicators=risks,
            phases=phases,
            estimated_duration=duration,
            raw_plan=raw_plan,
        )

    @abstractmethod
    def extract_files(self, raw_plan: str) -> List[str]:
        """Extract file list from plan (stack-specific format)"""
        pass

    # ... other abstract methods

class PythonPlanParser(PlanParser):
    def extract_files(self, raw_plan: str) -> List[str]:
        # Look for patterns like:
        # - src/api/routes/users.py
        # - tests/test_users.py
        pattern = r'^[-*]\s+([\w/_.]+\.py)$'
        matches = re.findall(pattern, raw_plan, re.MULTILINE)
        return list(set(matches))

    def extract_patterns(self, raw_plan: str) -> List[str]:
        # Look for "Pattern: Repository Pattern" or "Using: Factory Pattern"
        pattern = r'(?:Pattern|Using):\s*([A-Z]\w+(?:\s+\w+)*)'
        matches = re.findall(pattern, raw_plan)
        return list(set(matches))

class ReactPlanParser(PlanParser):
    def extract_files(self, raw_plan: str) -> List[str]:
        # Look for patterns like:
        # - src/components/UserList.tsx
        # - src/hooks/useAuth.ts
        pattern = r'^[-*]\s+([\w/_.]+\.tsx?)$'
        matches = re.findall(pattern, raw_plan, re.MULTILINE)
        return list(set(matches))

# Factory
def create_plan_parser(stack: str) -> PlanParser:
    parsers = {
        "python": PythonPlanParser(),
        "python-mcp": PythonPlanParser(),
        "react": ReactPlanParser(),
        "typescript-api": TypeScriptPlanParser(),
        "maui": DotNetPlanParser(),
        "dotnet-microservice": DotNetPlanParser(),
        "default": GenericPlanParser(),
    }
    return parsers.get(stack, GenericPlanParser())
```

**Rationale**:
- Handles variation across stack-specific planning agents
- Extensible (add new parser for new stack)
- Fallback to generic parser for unknown stacks
- Each parser focuses on its stack's conventions

---

## 3. Component Structure

### 3.1 New Files to Create

```
installer/global/commands/lib/
├── complexity_calculator.py          # ✅ ALREADY EXISTS (TASK-003A)
├── complexity_models.py              # ✅ ALREADY EXISTS (TASK-003A)
├── user_interaction.py               # ✅ ALREADY EXISTS (TASK-003B-1)
├── review_modes.py                   # ✅ ALREADY EXISTS (TASK-003B-1)
├── plan_parser.py                    # 🆕 NEW - Stack-specific plan parsers
├── phase_27_handler.py               # 🆕 NEW - Phase 2.7 orchestration
├── phase_28_handler.py               # 🆕 NEW - Phase 2.8 orchestration
├── review_state_machine.py           # 🆕 NEW - State machine for routing
├── review_commands.py                # 🆕 NEW - Command pattern for decisions
└── task_context.py                   # 🆕 NEW - Shared context object

tests/unit/
├── test_plan_parser.py               # 🆕 NEW
├── test_phase_27_handler.py          # 🆕 NEW
├── test_phase_28_handler.py          # 🆕 NEW
├── test_review_state_machine.py      # 🆕 NEW
└── test_review_commands.py           # 🆕 NEW

tests/integration/
└── test_phase_27_28_integration.py   # 🆕 NEW - End-to-end workflow tests
```

### 3.2 Existing Files to Modify

```
installer/global/commands/task-work.md
└── ADD: Phase 2.7 and Phase 2.8 invocation steps
    Between Phase 2 (Planning) and Phase 3 (Implementation)

installer/global/agents/task-manager.md
└── ADD: Phase 2.7 and Phase 2.8 orchestration logic
    Including routing, error handling, modification loop

.claude/settings.json (if doesn't exist)
└── ADD: Project configuration with stack detection
```

### 3.3 Component Dependencies

```
Phase 2.7 Handler Dependencies:
├── plan_parser.py → complexity_models.py (ImplementationPlan)
├── complexity_calculator.py → complexity_models.py (ComplexityScore, ReviewMode)
└── task_context.py → complexity_models.py (for type hints)

Phase 2.8 Handler Dependencies:
├── review_state_machine.py → complexity_models.py (ReviewMode)
├── review_commands.py → task_context.py
├── review_modes.py (QuickReviewHandler, FullReviewHandler) → user_interaction.py
└── user_interaction.py → (no internal dependencies, uses stdlib)

Integration Dependencies:
task-work.md → task-manager.md → phase_27_handler.py → phase_28_handler.py → Phase 3
```

### 3.4 Metadata Schema Extensions

**Task File Frontmatter** (tasks/in_progress/TASK-XXX.md):
```yaml
---
id: TASK-XXX
title: Task title
status: in_progress

# EXISTING FIELDS (unchanged)
created: 2025-10-09T10:00:00Z
updated: 2025-10-10T12:00:00Z
assignee: null
priority: medium
tags: [feature, api]
requirements: [REQ-001]
bdd_scenarios: [BDD-001]

# NEW FIELDS (Phase 2.7/2.8)
implementation_plan:
  version: 2  # Incremented on modification
  file_path: docs/state/TASK-XXX/implementation_plan_v2.json
  approved: true
  approved_by: user
  approved_at: 2025-10-10T12:30:00Z
  review_mode: "full_required"  # or "quick_optional" or "auto_proceed"
  review_duration_seconds: 45
  modification_count: 1  # Number of plan modifications

complexity_evaluation:
  score: 7  # 1-10 scale
  file_path: docs/state/TASK-XXX/complexity_score_v2.json
  calculated_at: 2025-10-10T12:25:00Z
  forced_review_triggers:
    - SECURITY_KEYWORDS
  review_mode: "full_required"

phase_28_session:
  started_at: 2025-10-10T12:20:00Z
  completed_at: 2025-10-10T12:30:00Z
  escalated: false  # true if escalated from quick to full review
  decisions:
    - action: "modify"
      timestamp: 2025-10-10T12:25:00Z
    - action: "approve"
      timestamp: 2025-10-10T12:30:00Z

# EXISTING FIELDS (unchanged)
test_results:
  status: pending
  last_run: null
  coverage: null
blocked_reason: null
---

# Task content...
```

---

## 4. Key Integration Points

### 4.1 Phase 2 → Phase 2.7 Transition

**Current**: task-work.md invokes Phase 2 (Implementation Planning) → Phase 2.5 (Architectural Review) → Phase 3 (Implementation)

**Change**: Insert Phase 2.7 and Phase 2.8 between Phase 2.5 and Phase 3

**task-work.md Update**:
```markdown
#### Phase 2.5B: Architectural Review
[... existing code ...]

**WAIT** for agent to complete before proceeding.

#### Phase 2.7: Plan Generation & Complexity Evaluation (NEW)

**INVOKE** Task tool:
```
subagent_type: "task-manager"
description: "Generate structured plan and evaluate complexity for TASK-XXX"
prompt: "Execute Phase 2.7 for TASK-XXX:
         1. Parse Phase 2 implementation plan into structured ImplementationPlan object
         2. Calculate complexity score (1-10 scale) using ComplexityCalculator
         3. Detect force-review triggers (security, schema changes, etc.)
         4. Determine ReviewMode: AUTO_PROCEED, QUICK_OPTIONAL, or FULL_REQUIRED
         5. Save state to docs/state/TASK-XXX/
         6. Return ComplexityScore and ReviewMode for Phase 2.8 routing

         Stack: {detected_stack}
         Phase 2 Output: {phase_2_output_summary}
         Task Metadata: {task_metadata}"
```

**WAIT** for agent to complete before proceeding.

**EXTRACT** Phase 2.7 results:
```python
complexity_score = extract_complexity_score(phase_27_output)
review_mode = complexity_score.review_mode
implementation_plan_path = f"docs/state/{task_id}/implementation_plan_v1.json"
```

#### Phase 2.8: Human Plan Checkpoint (NEW)

**ROUTE** based on ReviewMode from Phase 2.7:

**IF** review_mode == AUTO_PROCEED:
- Display complexity summary
- Update task metadata: auto_approved=true
- Automatically proceed to Phase 3 (no human intervention)

**ELSE IF** review_mode == QUICK_OPTIONAL:
- **INVOKE** Task tool (QuickReviewHandler):
  ```
  subagent_type: "task-manager"
  description: "Execute quick review checkpoint for TASK-XXX"
  prompt: "Execute Phase 2.8 Quick Review for TASK-XXX:
           1. Load ImplementationPlan from {implementation_plan_path}
           2. Display summary card (complexity score, files, patterns)
           3. Start 10-second countdown
           4. Handle user input:
              - timeout → auto-approve → return 'proceed'
              - enter → escalate to full review → return 'escalate'
              - cancel → move to backlog → return 'cancel'
           5. Update task metadata with review results"
  ```

  **WAIT** for result

  **IF** result == 'proceed':
    - Proceed to Phase 3
  **ELSE IF** result == 'escalate':
    - Fall through to FULL_REQUIRED handling below
  **ELSE IF** result == 'cancel':
    - Exit task-work (task moved to backlog)

**ELSE IF** review_mode == FULL_REQUIRED (or escalated from QUICK_OPTIONAL):
- **INVOKE** Task tool (FullReviewHandler):
  ```
  subagent_type: "task-manager"
  description: "Execute full review checkpoint for TASK-XXX"
  prompt: "Execute Phase 2.8 Full Review for TASK-XXX:
           1. Load ImplementationPlan and ComplexityScore from docs/state/
           2. Display comprehensive checkpoint (complexity breakdown, changes, risks, phases)
           3. Prompt for decision: [A]pprove / [M]odify / [V]iew / [Q]uestion / [C]ancel
           4. Handle decision:
              - Approve → return 'approve' (proceed to Phase 3)
              - Modify → Enter ModificationSession → Apply → Re-run Phase 2.7 → Loop back to Phase 2.8
              - View → Show plan in pager → Re-prompt
              - Question → Q&A session → Re-prompt
              - Cancel → Move to backlog → return 'cancel'
           5. Update task metadata with review results

           Stack: {detected_stack}
           Escalated: {true if escalated from quick review}"
  ```

  **WAIT** for result

  **IF** result == 'approve':
    - Proceed to Phase 3
  **ELSE IF** result == 'cancel':
    - Exit task-work (task moved to backlog)
  **ELSE IF** result == 'modify_and_loop':
    - Modified plan saved, complexity re-calculated
    - Loop back to Phase 2.8 with new plan version
    - Continue until user approves or cancels

#### Phase 3: Implementation
[... existing code, proceeds only after Phase 2.8 approval ...]
```

**Key Changes**:
1. Two new phase invocations (2.7 and 2.8)
2. Conditional routing based on ReviewMode
3. Modification loop support (Phase 2.8 → Phase 2.7 → Phase 2.8)
4. State persistence before proceeding to Phase 3

### 4.2 Phase 2.7 → Phase 2.8 Transition with Context Passing

**Context Object** (task_context.py):
```python
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from pathlib import Path
from complexity_models import ComplexityScore, ImplementationPlan, ReviewMode

@dataclass
class TaskContext:
    """Shared context passed between phases"""

    # Task identity
    task_id: str
    task_file_path: Path
    task_metadata: Dict[str, Any]

    # Technology stack
    detected_stack: str

    # Phase outputs
    phase_2_output: str  # Raw planning agent output
    implementation_plan: Optional[ImplementationPlan] = None
    complexity_score: Optional[ComplexityScore] = None

    # Review state
    review_mode: Optional[ReviewMode] = None
    plan_version: int = 1
    modification_count: int = 0

    # Decisions
    auto_approved: bool = False
    escalated: bool = False  # Quick → Full escalation
    approved: bool = False
    cancelled: bool = False
    proceed_to_phase_3: bool = False

    # State paths
    state_dir: Optional[Path] = None

    def __post_init__(self):
        if self.state_dir is None:
            self.state_dir = Path(f"docs/state/{self.task_id}")
            self.state_dir.mkdir(parents=True, exist_ok=True)

    def get_plan_path(self, version: Optional[int] = None) -> Path:
        """Get path to implementation plan JSON file"""
        v = version or self.plan_version
        return self.state_dir / f"implementation_plan_v{v}.json"

    def get_complexity_path(self, version: Optional[int] = None) -> Path:
        """Get path to complexity score JSON file"""
        v = version or self.plan_version
        return self.state_dir / f"complexity_score_v{v}.json"

    def increment_plan_version(self):
        """Increment plan version after modification"""
        self.plan_version += 1
        self.modification_count += 1

    def to_metadata_dict(self) -> Dict[str, Any]:
        """Convert to metadata dictionary for task file update"""
        metadata = {
            "implementation_plan": {
                "version": self.plan_version,
                "file_path": str(self.get_plan_path()),
                "approved": self.approved,
                "review_mode": self.review_mode.value if self.review_mode else None,
                "modification_count": self.modification_count,
            }
        }

        if self.complexity_score:
            metadata["complexity_evaluation"] = {
                "score": self.complexity_score.total_score,
                "file_path": str(self.get_complexity_path()),
                "calculated_at": self.complexity_score.calculation_timestamp.isoformat(),
                "review_mode": self.complexity_score.review_mode.value,
            }

        if self.auto_approved:
            metadata["implementation_plan"]["auto_approved"] = True

        if self.escalated:
            metadata["phase_28_session"] = metadata.get("phase_28_session", {})
            metadata["phase_28_session"]["escalated"] = True

        return metadata
```

**Phase 2.7 Output → Phase 2.8 Input**:
```python
# Phase 2.7 Handler
class Phase27Handler:
    def handle(self, context: TaskContext) -> TaskContext:
        # Parse plan
        parser = create_plan_parser(context.detected_stack)
        plan = parser.parse(context.phase_2_output, context.task_id)

        # Calculate complexity
        calculator = ComplexityCalculator()
        eval_context = EvaluationContext(
            task_id=context.task_id,
            technology_stack=context.detected_stack,
            implementation_plan=plan,
            task_metadata=context.task_metadata,
        )
        complexity_score = calculator.calculate(eval_context)

        # Save state
        plan_path = context.get_plan_path()
        complexity_path = context.get_complexity_path()

        with open(plan_path, 'w') as f:
            json.dump(plan.__dict__, f, indent=2)

        with open(complexity_path, 'w') as f:
            json.dump(complexity_score_to_dict(complexity_score), f, indent=2)

        # Update context
        context.implementation_plan = plan
        context.complexity_score = complexity_score
        context.review_mode = complexity_score.review_mode

        return context

# Phase 2.8 Handler (receives context from Phase 2.7)
class Phase28Handler:
    def handle(self, context: TaskContext) -> TaskContext:
        # Context already contains:
        # - implementation_plan
        # - complexity_score
        # - review_mode

        # Route based on review_mode
        if context.review_mode == ReviewMode.AUTO_PROCEED:
            return self._handle_auto_proceed(context)
        elif context.review_mode == ReviewMode.QUICK_OPTIONAL:
            return self._handle_quick_review(context)
        elif context.review_mode == ReviewMode.FULL_REQUIRED:
            return self._handle_full_review(context)
```

### 4.3 Phase 2.8 → Phase 3 Transition (All Review Paths)

**After Approval** (any path):
```python
# All paths converge here after approval
def proceed_to_phase_3(context: TaskContext) -> TaskContext:
    # Update task file metadata
    update_task_metadata(
        task_file_path=context.task_file_path,
        metadata_updates=context.to_metadata_dict()
    )

    # Set proceed flag
    context.proceed_to_phase_3 = True

    # Log transition
    log_phase_transition(
        task_id=context.task_id,
        from_phase="2.8",
        to_phase="3",
        review_mode=context.review_mode.value,
        approved=context.approved,
        auto_approved=context.auto_approved
    )

    return context

# task-work.md checks this flag before Phase 3
if context.proceed_to_phase_3:
    # Invoke Phase 3 (Implementation)
    ...
```

### 4.4 Modification Loop: Phase 2.8 → Phase 2.7 → Phase 2.8

**Modification Flow**:
```python
class FullReviewHandler:
    def _handle_modify(self, context: TaskContext) -> Optional[FullReviewResult]:
        # Enter modification session
        session = ModificationSession(
            plan=context.implementation_plan,
            task_id=context.task_id,
        )
        session.start()

        # Interactive modification (user adds/removes files, deps, etc.)
        modified_plan = session.run_interactive_editor()

        if session.cancelled:
            return None  # Return to checkpoint

        # Apply modifications
        applier = ModificationApplier(context.implementation_plan, session.change_tracker)
        modified_plan = applier.apply()

        # Increment version
        context.increment_plan_version()

        # Re-calculate complexity
        calculator = ComplexityCalculator()
        eval_context = EvaluationContext(
            task_id=context.task_id,
            technology_stack=context.detected_stack,
            implementation_plan=modified_plan,
            task_metadata=context.task_metadata,
        )
        new_complexity = calculator.calculate(eval_context)

        # Save new versions
        plan_path = context.get_plan_path()
        complexity_path = context.get_complexity_path()

        with open(plan_path, 'w') as f:
            json.dump(modified_plan.__dict__, f, indent=2)

        with open(complexity_path, 'w') as f:
            json.dump(complexity_score_to_dict(new_complexity), f, indent=2)

        # Update context
        context.implementation_plan = modified_plan
        context.complexity_score = new_complexity
        context.review_mode = new_complexity.review_mode

        # Check for infinite loop (safety)
        if context.modification_count >= 5:
            print("⚠️ Warning: 5 modifications reached. Please make final decision.")
            # Don't allow more modifications

        # Re-display checkpoint with modified plan
        display = FullReviewDisplay(
            complexity_score=new_complexity,
            plan=modified_plan,
            task_metadata=context.task_metadata,
            escalated=context.escalated
        )
        display.render_full_checkpoint()

        # Re-prompt for decision
        return None  # Signals to continue decision loop
```

**Loop Prevention**:
- Track modification count in context
- Warn after 3 modifications
- Force decision after 5 modifications (no more modify option)
- Each modification creates new plan version (auditability)

---

## 5. Critical Dependencies

### 5.1 Address TASK-003A/003B Dependency Gap

**Problem Identified**: TASK-003A implemented ComplexityCalculator but didn't connect it to task-work workflow.

**Solution**:
1. **TASK-003A Artifacts** (✅ COMPLETED):
   - complexity_calculator.py
   - complexity_models.py (ComplexityScore, ImplementationPlan, ReviewMode)
   - Unit tests for calculation logic

2. **TASK-003B-1 Artifacts** (✅ COMPLETED):
   - user_interaction.py (countdown_timer)
   - review_modes.py (QuickReviewHandler, FullReviewHandler)
   - Unit tests for quick review

3. **TASK-003C Missing Links** (🚧 THIS TASK):
   - **plan_parser.py**: Parse free-form Phase 2 output → ImplementationPlan
   - **phase_27_handler.py**: Orchestrate plan generation + complexity calculation
   - **phase_28_handler.py**: Orchestrate review routing (auto/quick/full)
   - **task-work.md updates**: Invoke Phase 2.7 and 2.8
   - **task-manager.md updates**: Add orchestration logic

**Dependency Resolution**:
```
TASK-003A (Complexity Calculation) ────┐
                                       │
TASK-003B-1 (Quick Review Mode) ──────┼─→ TASK-003C (Integration)
                                       │
Phase 2 Planning Agents (Existing) ────┘
```

### 5.2 Propose Solution for Complexity Calculation Logic

**Already Solved** by TASK-003A ✅

See: `/installer/global/commands/lib/complexity_calculator.py`

**Calculation Logic**:
```python
class ComplexityCalculator:
    def calculate(self, context: EvaluationContext) -> ComplexityScore:
        # Factor 1: File Complexity (0-3 points)
        file_score = self._calculate_file_complexity(context.implementation_plan)

        # Factor 2: Pattern Familiarity (0-2 points)
        pattern_score = self._calculate_pattern_complexity(context.implementation_plan)

        # Factor 3: Risk Level (0-3 points)
        risk_score = self._calculate_risk_level(context.implementation_plan)

        # Factor 4: External Dependencies (0-2 points)
        dep_score = self._calculate_dependency_complexity(context.implementation_plan)

        # Total: 0-10 scale
        total_score = file_score + pattern_score + risk_score + dep_score

        # Detect force-review triggers
        triggers = self._detect_force_review_triggers(context)

        # Determine review mode
        if triggers:
            review_mode = ReviewMode.FULL_REQUIRED
        elif total_score >= 7:
            review_mode = ReviewMode.FULL_REQUIRED
        elif total_score >= 4:
            review_mode = ReviewMode.QUICK_OPTIONAL
        else:
            review_mode = ReviewMode.AUTO_PROCEED

        return ComplexityScore(
            total_score=total_score,
            factor_scores=[file_score, pattern_score, risk_score, dep_score],
            forced_review_triggers=triggers,
            review_mode=review_mode,
            calculation_timestamp=datetime.utcnow(),
        )
```

**No Additional Work Needed** - Just integrate existing logic.

### 5.3 Propose Solution for Review Mode Interaction Handlers

**Partially Solved** by TASK-003B-1 ✅

**Implemented**:
- QuickReviewHandler (10-second countdown, timeout/enter/cancel)
- user_interaction.py (countdown_timer, input strategies)

**Still Needed in TASK-003C**:
- FullReviewHandler integration (already stubbed in review_modes.py)
- Modification session handlers (TASK-003B-3 dependency)
- View handler (pager display - TASK-003B-3 dependency)
- Q&A handler (TASK-003B-4 dependency)

**TASK-003C Scope** (Minimal Viable Integration):
1. **Use QuickReviewHandler as-is** ✅ (no changes needed)
2. **Use FullReviewHandler with [A]pprove and [C]ancel only**
3. **Stub [M]odify, [V]iew, [Q]uestion** with "Coming soon" messages
4. **Full implementation** deferred to TASK-003B-2, TASK-003B-3, TASK-003B-4

**FullReviewHandler Minimal Integration**:
```python
class FullReviewHandler:
    def execute(self) -> FullReviewResult:
        # Display checkpoint (already implemented)
        self.display.render_full_checkpoint()

        # Prompt for decision
        choice = input("Your choice (A/M/V/Q/C): ").strip().lower()

        if choice == 'a':
            return self._handle_approval()  # ✅ IMPLEMENTED
        elif choice == 'c':
            return self._handle_cancellation()  # ✅ IMPLEMENTED
        elif choice == 'm':
            print("\n⚠️ Modification mode coming soon (TASK-003B-3)")
            print("Returning to checkpoint...\n")
            return self.execute()  # Re-prompt
        elif choice == 'v':
            print("\n⚠️ View mode coming soon (TASK-003B-3)")
            print("Returning to checkpoint...\n")
            return self.execute()  # Re-prompt
        elif choice == 'q':
            print("\n⚠️ Q&A mode coming soon (TASK-003B-4)")
            print("Returning to checkpoint...\n")
            return self.execute()  # Re-prompt
        else:
            print(f"\n❌ Invalid choice: '{choice}'")
            return self.execute()  # Re-prompt
```

**Phased Delivery**:
- **TASK-003C**: [A]pprove and [C]ancel only (core workflow functional)
- **TASK-003B-2**: Complete [M]odify, [V]iew implementations
- **TASK-003B-3**: Modification session, versioning, applier
- **TASK-003B-4**: Q&A mode implementation

---

## 6. Implementation Plan

### 6.1 Implementation Order (Prioritized)

**Day 1: Foundation & Phase 2.7**
1. **Create task_context.py** (2 hours)
   - TaskContext dataclass
   - State path helpers
   - Metadata conversion
   - Unit tests

2. **Create plan_parser.py** (4 hours)
   - PlanParser base class (Template Pattern)
   - GenericPlanParser (regex-based)
   - PythonPlanParser
   - ReactPlanParser
   - Factory function
   - Unit tests (parser accuracy)

3. **Create phase_27_handler.py** (2 hours)
   - Phase27Handler class
   - Integrate plan_parser and complexity_calculator
   - State persistence
   - Error handling
   - Unit tests

**Day 2: Phase 2.8 Foundation**
4. **Create review_state_machine.py** (3 hours)
   - ReviewStateMachine class
   - Transition table
   - State validation
   - History tracking
   - Unit tests

5. **Create review_commands.py** (3 hours)
   - ReviewCommand base class
   - ApproveCommand
   - CancelCommand
   - ModifyCommand (stub for TASK-003B-3)
   - Unit tests

6. **Create phase_28_handler.py** (2 hours)
   - Phase28Handler class
   - Route to QuickReviewHandler
   - Route to FullReviewHandler
   - Handle results
   - Unit tests

**Day 3: Integration & Testing**
7. **Update task-manager.md** (3 hours)
   - Add Phase 2.7 orchestration section
   - Add Phase 2.8 orchestration section
   - Add modification loop logic
   - Add error handling patterns

8. **Update task-work.md** (2 hours)
   - Add Phase 2.7 invocation
   - Add Phase 2.8 routing logic
   - Update Phase 3 preconditions
   - Add state persistence steps

9. **Create integration tests** (3 hours)
   - test_phase_27_28_integration.py
   - End-to-end workflow tests:
     - Low complexity (auto-proceed)
     - Medium complexity (quick review, timeout)
     - Medium complexity (quick review, escalate)
     - High complexity (full review, approve)
     - High complexity (full review, cancel)
   - Modification loop test (stub)

**Day 4: Polish & Documentation**
10. **Error handling refinement** (2 hours)
    - Add fail-safe escalation
    - Improve error messages
    - Add recovery instructions

11. **Documentation** (2 hours)
    - Update CLAUDE.md with Phase 2.7/2.8 details
    - Create example walkthrough
    - Document state file locations

12. **Manual testing** (3 hours)
    - Test on actual tasks across stacks (python, react)
    - Verify state persistence
    - Verify modification loop (when implemented)
    - Test error scenarios

13. **Code review & cleanup** (1 hour)
    - Review all code
    - Fix linting issues
    - Optimize performance

### 6.2 Task Breakdown Structure

```
TASK-003C: Phase 2.7 & 2.8 Integration (Parent)
├── TASK-003C-1: Foundation Components (Day 1 Morning)
│   ├── task_context.py
│   └── plan_parser.py
│
├── TASK-003C-2: Phase 2.7 Handler (Day 1 Afternoon)
│   └── phase_27_handler.py
│
├── TASK-003C-3: Phase 2.8 Foundation (Day 2)
│   ├── review_state_machine.py
│   ├── review_commands.py
│   └── phase_28_handler.py
│
├── TASK-003C-4: Workflow Integration (Day 3 Morning)
│   ├── task-manager.md updates
│   └── task-work.md updates
│
├── TASK-003C-5: Testing & Validation (Day 3 Afternoon)
│   ├── Integration tests
│   └── Manual testing
│
└── TASK-003C-6: Documentation & Polish (Day 4)
    ├── Documentation updates
    ├── Error handling
    └── Code review
```

### 6.3 Testing Approach

**Unit Tests** (Coverage Target: ≥85%):
```python
# tests/unit/test_plan_parser.py
def test_python_parser_extracts_files():
    raw_plan = """
    Implementation Plan:

    Files to create:
    - src/api/routes/users.py
    - src/models/user.py
    - tests/test_users.py
    """
    parser = PythonPlanParser()
    files = parser.extract_files(raw_plan)
    assert set(files) == {
        "src/api/routes/users.py",
        "src/models/user.py",
        "tests/test_users.py"
    }

def test_generic_parser_fallback():
    raw_plan = "Random plan text without structure"
    parser = GenericPlanParser()
    plan = parser.parse(raw_plan, "TASK-001")
    assert plan.task_id == "TASK-001"
    assert plan.raw_plan == raw_plan

# tests/unit/test_phase_27_handler.py
def test_phase_27_generates_plan_and_complexity():
    context = TaskContext(
        task_id="TASK-001",
        detected_stack="python",
        phase_2_output=SAMPLE_PLAN_OUTPUT,
        ...
    )
    handler = Phase27Handler()
    result = handler.handle(context)

    assert result.implementation_plan is not None
    assert result.complexity_score is not None
    assert result.review_mode in [ReviewMode.AUTO_PROCEED, ...]
    assert result.get_plan_path().exists()

# tests/unit/test_review_state_machine.py
def test_state_machine_transitions():
    sm = ReviewStateMachine(ReviewState.QUICK_OPTIONAL)

    # Timeout transition
    new_state = sm.transition("timeout", context)
    assert new_state == ReviewState.PHASE_3

    # Escalation transition
    sm = ReviewStateMachine(ReviewState.QUICK_OPTIONAL)
    new_state = sm.transition("enter", context)
    assert new_state == ReviewState.FULL_REQUIRED
```

**Integration Tests** (Coverage Target: 100% of user paths):
```python
# tests/integration/test_phase_27_28_integration.py
def test_auto_proceed_workflow():
    """Test low complexity task auto-proceeds to Phase 3"""
    # Setup task with simple plan (1 file, no patterns, no risks)
    task = create_test_task(complexity="low")

    # Run Phase 2.7
    context = execute_phase_27(task)
    assert context.review_mode == ReviewMode.AUTO_PROCEED

    # Run Phase 2.8
    context = execute_phase_28(context)
    assert context.auto_approved == True
    assert context.proceed_to_phase_3 == True
    assert context.task_metadata["implementation_plan"]["auto_approved"] == True

def test_quick_review_timeout():
    """Test medium complexity task with quick review timeout"""
    task = create_test_task(complexity="medium")

    context = execute_phase_27(task)
    assert context.review_mode == ReviewMode.QUICK_OPTIONAL

    # Simulate timeout (no user input for 10 seconds)
    with patch('user_interaction.countdown_timer', return_value="timeout"):
        context = execute_phase_28(context)

    assert context.auto_approved == True
    assert context.proceed_to_phase_3 == True

def test_quick_review_escalation():
    """Test medium complexity task with escalation to full review"""
    task = create_test_task(complexity="medium")

    context = execute_phase_27(task)
    assert context.review_mode == ReviewMode.QUICK_OPTIONAL

    # Simulate user pressing ENTER
    with patch('user_interaction.countdown_timer', return_value="enter"):
        with patch('builtins.input', return_value='a'):  # Then approve in full review
            context = execute_phase_28(context)

    assert context.escalated == True
    assert context.approved == True
    assert context.proceed_to_phase_3 == True

def test_full_review_approve():
    """Test high complexity task with full review approval"""
    task = create_test_task(complexity="high")

    context = execute_phase_27(task)
    assert context.review_mode == ReviewMode.FULL_REQUIRED

    with patch('builtins.input', return_value='a'):
        context = execute_phase_28(context)

    assert context.approved == True
    assert context.proceed_to_phase_3 == True

def test_full_review_cancel():
    """Test high complexity task with cancellation"""
    task = create_test_task(complexity="high")

    context = execute_phase_27(task)

    with patch('builtins.input', side_effect=['c', 'y']):  # Cancel + confirm
        context = execute_phase_28(context)

    assert context.cancelled == True
    assert context.proceed_to_phase_3 == False
    assert Path(f"tasks/backlog/{task.task_id}.md").exists()
```

**Manual Testing Checklist**:
- [ ] Low complexity task (1-2 files) → Auto-proceed
- [ ] Medium complexity task (3-5 files) → Quick review → Timeout
- [ ] Medium complexity task → Quick review → Escalate → Approve
- [ ] High complexity task (7+ files) → Full review → Approve
- [ ] Task with security keywords → Full review (forced)
- [ ] Task with schema changes → Full review (forced)
- [ ] User cancels during quick review
- [ ] User cancels during full review
- [ ] State files created correctly
- [ ] Task metadata updated correctly
- [ ] Error handling (invalid plan format, calculation error)

---

## 7. Risk Assessment

### 7.1 High-Risk Areas

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| **Plan parsing fails for some stack formats** | High | Medium | Fallback to GenericPlanParser, add stack-specific tests |
| **State file corruption** | High | Low | Atomic writes (already implemented), backup on modification |
| **Infinite modification loop** | Medium | Low | Limit to 5 modifications, warn after 3 |
| **Quick review countdown hangs** | Medium | Low | Timeout safety, Ctrl+C handling (already implemented) |
| **Integration breaks existing workflow** | High | Medium | Comprehensive integration tests, backward compatibility |
| **Complexity calculation edge cases** | Medium | Medium | Extensive unit tests, logging for debugging |

### 7.2 Critical Integration Points

**Highest Risk Integration**:
1. **task-work.md → Phase 2.7 invocation**
   - Risk: Breaking existing Phase 2 → Phase 3 flow
   - Mitigation: Insert between existing phases, test with/without new phases

2. **Phase 2.8 → Phase 3 transition**
   - Risk: Phase 3 starts without approval
   - Mitigation: Explicit `proceed_to_phase_3` flag check

3. **Modification loop convergence**
   - Risk: User stuck in modify → re-calculate → modify cycle
   - Mitigation: Hard limit on modifications, force decision

### 7.3 Rollback Strategy

**If Integration Fails**:
1. **Revert task-work.md and task-manager.md changes**
   - Remove Phase 2.7/2.8 invocations
   - Restore direct Phase 2 → Phase 3 transition

2. **Disable new features via feature flag**
   ```python
   # .claude/settings.json
   {
       "features": {
           "phase_27_28_enabled": false  # Disable new phases
       }
   }
   ```

3. **Preserve state files for debugging**
   - Don't delete docs/state/ directory
   - Allows post-mortem analysis

**Graceful Degradation**:
- If Phase 2.7 fails → Skip to Phase 3 (log error)
- If Phase 2.8 fails → Auto-approve and proceed (log warning)
- If state save fails → Continue anyway (log error)

---

## 8. Testing Strategy

### 8.1 Test Coverage Requirements

| Component | Unit Test Coverage | Integration Test Coverage |
|-----------|-------------------|---------------------------|
| plan_parser.py | ≥85% | N/A |
| phase_27_handler.py | ≥90% | 100% (via integration tests) |
| phase_28_handler.py | ≥90% | 100% (via integration tests) |
| review_state_machine.py | ≥95% | N/A |
| review_commands.py | ≥85% | N/A |
| task_context.py | ≥80% | N/A |
| **Overall** | **≥85%** | **100% of user paths** |

### 8.2 Test Data Requirements

**Sample Plans** (for parser testing):
```python
SAMPLE_PYTHON_PLAN = """
Implementation Plan for TASK-042

Files to Create:
- src/api/routes/auth.py
- src/services/auth_service.py
- src/models/user.py
- tests/test_auth.py

Patterns:
- Repository Pattern for data access
- Service Layer for business logic
- Dependency Injection for testability

External Dependencies:
- bcrypt for password hashing
- jwt for token generation

Estimated LOC: 250 lines
Estimated Duration: 2-3 hours

Risks:
- Security: Password storage and token handling
- Performance: Token validation on every request
"""

SAMPLE_REACT_PLAN = """
Implementation Plan for TASK-043

Files:
- src/components/UserList.tsx
- src/components/UserCard.tsx
- src/hooks/useUsers.ts
- src/api/userApi.ts
- src/types/user.ts

Patterns:
- Custom Hooks for data fetching
- Component Composition for UI

Dependencies:
- react-query for data fetching
- axios for HTTP

Estimated: ~180 lines
Time: 1-2 hours
"""
```

**Test Tasks**:
```yaml
# Low complexity (auto-proceed)
low_complexity_task:
  task_id: TASK-TEST-001
  files: 1
  patterns: []
  dependencies: []
  risks: []
  expected_score: 2
  expected_mode: AUTO_PROCEED

# Medium complexity (quick review)
medium_complexity_task:
  task_id: TASK-TEST-002
  files: 4
  patterns: ["Repository Pattern"]
  dependencies: ["axios"]
  risks: []
  expected_score: 5
  expected_mode: QUICK_OPTIONAL

# High complexity (full review)
high_complexity_task:
  task_id: TASK-TEST-003
  files: 8
  patterns: ["CQRS", "Event Sourcing"]
  dependencies: ["kafka", "redis", "postgres"]
  risks: ["schema_changes", "breaking_changes"]
  expected_score: 9
  expected_mode: FULL_REQUIRED
```

### 8.3 Performance Benchmarks

| Operation | Target Duration | Maximum Duration |
|-----------|----------------|------------------|
| Plan parsing | <500ms | <2s |
| Complexity calculation | <200ms | <1s |
| State file save | <100ms | <500ms |
| Quick review display | <200ms | <1s |
| Full review display | <500ms | <2s |
| Modification application | <1s | <5s |

### 8.4 Test Execution Plan

**Pre-Commit Tests** (fast feedback):
```bash
# Run unit tests only (fast)
pytest tests/unit/ -v --cov=installer/global/commands/lib --cov-report=term

# Expected runtime: <10 seconds
```

**Pre-Push Tests** (comprehensive):
```bash
# Run all tests (unit + integration)
pytest tests/ -v --cov=installer/global/commands/lib --cov-report=html

# Expected runtime: <30 seconds
```

**CI/CD Pipeline Tests**:
```yaml
# .github/workflows/test.yml
name: Test Phase 2.7/2.8 Integration

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run unit tests
        run: pytest tests/unit/ -v --cov --cov-report=xml
      - name: Run integration tests
        run: pytest tests/integration/ -v
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

---

## 9. Success Metrics

### 9.1 Functional Metrics

**Phase 2.7 Success** ✅:
- [ ] 100% of tasks have ImplementationPlan generated
- [ ] 100% of tasks have ComplexityScore calculated
- [ ] State files created for 100% of tasks
- [ ] Plan parsing success rate: ≥95% (across all stacks)

**Phase 2.8 Success** ✅:
- [ ] Routing accuracy: 100% (correct mode for given score)
- [ ] Auto-proceed tasks: 0 unnecessary reviews
- [ ] Quick review escalations: User has option 100% of the time
- [ ] Full review decisions: All options functional ([A], [C] at minimum)

**Integration Success** ✅:
- [ ] Zero regressions in existing workflow
- [ ] Phase 3 only starts after approval (100% enforcement)
- [ ] Modification loop converges (max 5 iterations)
- [ ] Error handling: 100% fail-safe escalation

### 9.2 Performance Metrics

| Metric | Target | Stretch Goal |
|--------|--------|--------------|
| Phase 2.7 execution time | <2s | <1s |
| Phase 2.8 auto-proceed time | <1s | <500ms |
| Quick review countdown accuracy | ±1s over 10s | ±500ms |
| Full review display render | <1s | <500ms |
| State file I/O overhead | <10% of phase duration | <5% |

### 9.3 Quality Metrics

| Metric | Requirement | Target |
|--------|------------|--------|
| Unit test coverage | ≥85% | ≥90% |
| Integration test coverage | 100% of user paths | 100% |
| Code review approval | 100% | N/A |
| Linting errors | 0 | 0 |
| Type safety (mypy) | 0 errors | 0 |

### 9.4 User Experience Metrics

**Auto-Proceed Path** (Low Complexity):
- Time from Phase 2 to Phase 3: <5 seconds
- User interaction: 0 clicks
- User satisfaction: High (no unnecessary friction)

**Quick Review Path** (Medium Complexity):
- Time from Phase 2 to Phase 3 (timeout): ~10 seconds
- User interaction: 0-1 clicks (optional escalation)
- User satisfaction: High (optional control)

**Full Review Path** (High Complexity):
- Time from Phase 2 to Phase 3: User-dependent (1-5 minutes)
- User interaction: 1 decision ([A] or [C])
- User satisfaction: High (comprehensive information)

### 9.5 Business Metrics

| Metric | Baseline (Without Phase 2.7/2.8) | Target (With Phase 2.7/2.8) |
|--------|--------------------------------|---------------------------|
| Time to implementation start | Variable | Consistent (auto-proceed <5s) |
| Over-engineered tasks | Unknown | Reduced (complexity awareness) |
| Under-reviewed high-risk tasks | Possible | 0% (force triggers) |
| User confidence in implementation | Unknown | Improved (plan visibility) |

---

## 10. Future Enhancements (Out of Scope for TASK-003C)

### 10.1 TASK-003B-2: Full Review Mode Complete

**Scope**:
- Implement [M]odify mode fully (modification session)
- Implement [V]iew mode (pager display)
- Create comprehensive checkpoint display

**Dependencies**: TASK-003C (this task)

### 10.2 TASK-003B-3: Modification Session & Versioning

**Scope**:
- ModificationSession class
- ModificationApplier (apply changes to plan)
- VersionManager (plan versioning)
- ModificationPersistence (audit trail)

**Dependencies**: TASK-003C, TASK-003B-2

### 10.3 TASK-003B-4: Q&A Mode

**Scope**:
- QAManager class
- Keyword-based plan extraction
- Q&A session persistence

**Dependencies**: TASK-003C, TASK-003B-2

### 10.4 Machine Learning Enhancements

**Future Vision**:
- Train ML model on historical complexity scores
- Predict complexity before planning phase
- Suggest patterns based on task requirements
- Auto-detect breaking changes via code diff analysis

**Dependencies**: Significant data collection, ML infrastructure

---

## Appendices

### A. File Structure Summary

```
installer/global/commands/lib/
├── complexity_calculator.py          # ✅ EXISTS (TASK-003A)
├── complexity_models.py              # ✅ EXISTS (TASK-003A)
├── user_interaction.py               # ✅ EXISTS (TASK-003B-1)
├── review_modes.py                   # ✅ EXISTS (TASK-003B-1)
├── plan_parser.py                    # 🆕 NEW (TASK-003C)
├── phase_27_handler.py               # 🆕 NEW (TASK-003C)
├── phase_28_handler.py               # 🆕 NEW (TASK-003C)
├── review_state_machine.py           # 🆕 NEW (TASK-003C)
├── review_commands.py                # 🆕 NEW (TASK-003C)
└── task_context.py                   # 🆕 NEW (TASK-003C)

installer/global/commands/
└── task-work.md                      # 📝 UPDATE (TASK-003C)

installer/global/agents/
└── task-manager.md                   # 📝 UPDATE (TASK-003C)

tests/unit/
├── test_plan_parser.py               # 🆕 NEW (TASK-003C)
├── test_phase_27_handler.py          # 🆕 NEW (TASK-003C)
├── test_phase_28_handler.py          # 🆕 NEW (TASK-003C)
├── test_review_state_machine.py      # 🆕 NEW (TASK-003C)
├── test_review_commands.py           # 🆕 NEW (TASK-003C)
└── test_task_context.py              # 🆕 NEW (TASK-003C)

tests/integration/
└── test_phase_27_28_integration.py   # 🆕 NEW (TASK-003C)

docs/state/{task_id}/
├── implementation_plan_v1.json       # 💾 GENERATED at runtime
├── complexity_score_v1.json          # 💾 GENERATED at runtime
└── review_session.json               # 💾 GENERATED at runtime
```

### B. Complexity Score Examples

**Low Complexity (Score: 2/10)**:
```json
{
  "total_score": 2,
  "factor_scores": [
    {"factor_name": "file_complexity", "score": 0.5, "max_score": 3},
    {"factor_name": "pattern_familiarity", "score": 0, "max_score": 2},
    {"factor_name": "risk_level", "score": 0.5, "max_score": 3},
    {"factor_name": "dependency_complexity", "score": 0, "max_score": 2}
  ],
  "forced_review_triggers": [],
  "review_mode": "auto_proceed",
  "calculation_timestamp": "2025-10-10T12:00:00Z"
}
```

**Medium Complexity (Score: 5/10)**:
```json
{
  "total_score": 5,
  "factor_scores": [
    {"factor_name": "file_complexity", "score": 1.5, "max_score": 3},
    {"factor_name": "pattern_familiarity", "score": 1, "max_score": 2},
    {"factor_name": "risk_level", "score": 1.5, "max_score": 3},
    {"factor_name": "dependency_complexity", "score": 1, "max_score": 2}
  ],
  "forced_review_triggers": [],
  "review_mode": "quick_optional",
  "calculation_timestamp": "2025-10-10T12:00:00Z"
}
```

**High Complexity (Score: 9/10)**:
```json
{
  "total_score": 9,
  "factor_scores": [
    {"factor_name": "file_complexity", "score": 3, "max_score": 3},
    {"factor_name": "pattern_familiarity", "score": 2, "max_score": 2},
    {"factor_name": "risk_level", "score": 3, "max_score": 3},
    {"factor_name": "dependency_complexity", "score": 2, "max_score": 2}
  ],
  "forced_review_triggers": ["SECURITY_KEYWORDS", "SCHEMA_CHANGES"],
  "review_mode": "full_required",
  "calculation_timestamp": "2025-10-10T12:00:00Z"
}
```

### C. Implementation Timeline

**Total Duration**: 3-4 days (24-32 hours)

```
Day 1 (8 hours):
├── task_context.py (2 hours)
├── plan_parser.py (4 hours)
└── phase_27_handler.py (2 hours)

Day 2 (8 hours):
├── review_state_machine.py (3 hours)
├── review_commands.py (3 hours)
└── phase_28_handler.py (2 hours)

Day 3 (8 hours):
├── task-manager.md updates (3 hours)
├── task-work.md updates (2 hours)
└── Integration tests (3 hours)

Day 4 (8 hours):
├── Error handling refinement (2 hours)
├── Documentation (2 hours)
├── Manual testing (3 hours)
└── Code review & cleanup (1 hour)
```

**Milestones**:
- Day 1 EOD: Phase 2.7 functional in isolation
- Day 2 EOD: Phase 2.8 functional in isolation
- Day 3 EOD: Full integration tested
- Day 4 EOD: Production-ready, documented

---

## Summary & Recommendation

This implementation architecture provides a **comprehensive, production-ready design** for integrating Phase 2.7 (Plan Generation + Complexity Evaluation) and Phase 2.8 (Human Plan Checkpoint) into the task-work workflow.

**Key Strengths**:
1. **Leverages Existing Work**: Builds on TASK-003A and TASK-003B-1 implementations
2. **Clear Separation of Concerns**: Each phase has dedicated handler, clean interfaces
3. **Fail-Safe Design**: Always escalates on errors, never auto-proceeds unsafely
4. **Extensible Architecture**: Easy to add modification mode, view mode, Q&A mode later
5. **Testable**: High unit test coverage, comprehensive integration tests
6. **User-Centric**: Optimizes for common case (auto-proceed) while preserving control

**Recommended Approach**:
1. Implement in the order specified (foundation first, integration last)
2. Test each component in isolation before integration
3. Use stubs for [M]/[V]/[Q] commands in Phase 2.8 (defer to TASK-003B-2/3/4)
4. Deploy with feature flag initially for safe rollout
5. Collect metrics to validate success

**Risk Mitigation**:
- Comprehensive testing at all levels
- Fail-safe error handling
- Rollback strategy documented
- Modification loop limits to prevent infinite cycles

**Next Steps After TASK-003C**:
1. TASK-003B-2: Complete [M]odify and [V]iew implementations
2. TASK-003B-3: Full modification session with versioning
3. TASK-003B-4: Q&A mode implementation
4. Collect usage metrics and refine complexity scoring

**Production Readiness**: ✅ This design is ready for implementation and deployment.

---

**Document Version**: 1.0
**Last Updated**: 2025-10-10
**Next Review**: After TASK-003C implementation completion
