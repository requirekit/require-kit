# TASK-003C: Implementation Checklist
## Phase 2.7 & 2.8 Integration - Developer Reference

**Purpose**: Step-by-step checklist for implementing TASK-003C
**Created**: 2025-10-10
**Estimated Duration**: 3-4 days (24-32 hours)

---

## Pre-Implementation Checklist

### Prerequisites Verification

- [ ] **TASK-003A completed** ✅
  - [ ] `complexity_calculator.py` exists and tested
  - [ ] `complexity_models.py` exists with ComplexityScore, ImplementationPlan, ReviewMode
  - [ ] Unit tests passing for complexity calculation

- [ ] **TASK-003B-1 completed** ✅
  - [ ] `user_interaction.py` exists with countdown_timer
  - [ ] `review_modes.py` exists with QuickReviewHandler, FullReviewHandler
  - [ ] Unit tests passing for quick review mode

- [ ] **Development Environment Setup**
  - [ ] Python 3.8+ installed
  - [ ] pytest installed (`pip install pytest pytest-cov`)
  - [ ] All dependencies installed from requirements.txt
  - [ ] Git repository clean (no uncommitted changes)

- [ ] **Documentation Review**
  - [ ] Read full architecture document (`TASK-003C-implementation-architecture.md`)
  - [ ] Read executive summary (`TASK-003C-executive-summary.md`)
  - [ ] Review architecture diagrams (`TASK-003C-architecture-diagrams.md`)
  - [ ] Understand existing task-work.md workflow

---

## Day 1: Foundation & Phase 2.7 (8 hours)

### Morning: Foundation Components (4 hours)

#### 1. Create task_context.py (2 hours)

**File**: `/installer/global/commands/lib/task_context.py`

- [ ] **Create TaskContext dataclass**
  - [ ] Add fields: task_id, task_file_path, task_metadata
  - [ ] Add fields: detected_stack, phase_2_output
  - [ ] Add fields: implementation_plan, complexity_score, review_mode
  - [ ] Add fields: plan_version, modification_count
  - [ ] Add fields: auto_approved, escalated, approved, cancelled
  - [ ] Add fields: proceed_to_phase_3, state_dir

- [ ] **Add state path helper methods**
  - [ ] `get_plan_path(version: Optional[int] = None) -> Path`
  - [ ] `get_complexity_path(version: Optional[int] = None) -> Path`
  - [ ] `increment_plan_version()` method
  - [ ] `to_metadata_dict() -> Dict[str, Any]` method

- [ ] **Add __post_init__ for state_dir creation**
  - [ ] Create `docs/state/{task_id}/` directory
  - [ ] Ensure directory exists before proceeding

- [ ] **Write unit tests** (`tests/unit/test_task_context.py`)
  - [ ] Test TaskContext creation with required fields
  - [ ] Test get_plan_path() returns correct path
  - [ ] Test increment_plan_version() increments correctly
  - [ ] Test to_metadata_dict() returns valid metadata
  - [ ] Test state_dir creation in __post_init__
  - [ ] **Run tests**: `pytest tests/unit/test_task_context.py -v`
  - [ ] **Target coverage**: ≥80%

**Validation**:
```bash
# Run tests
pytest tests/unit/test_task_context.py -v --cov=installer/global/commands/lib/task_context

# Expected: All tests passing, coverage ≥80%
```

#### 2. Create plan_parser.py (4 hours)

**File**: `/installer/global/commands/lib/plan_parser.py`

- [ ] **Create PlanParser base class (Template Pattern)**
  - [ ] Define `parse(raw_plan: str, task_id: str) -> ImplementationPlan` template method
  - [ ] Define abstract methods:
    - [ ] `extract_files(raw_plan: str) -> List[str]`
    - [ ] `extract_patterns(raw_plan: str) -> List[str]`
    - [ ] `extract_dependencies(raw_plan: str) -> List[str]`
    - [ ] `extract_loc_estimate(raw_plan: str) -> Optional[int]`
    - [ ] `extract_risks(raw_plan: str) -> List[str]`
    - [ ] `extract_phases(raw_plan: str) -> Optional[List[str]]`
    - [ ] `extract_duration(raw_plan: str) -> Optional[str]`

- [ ] **Create PythonPlanParser**
  - [ ] Implement `extract_files()` (regex for `.py` files)
  - [ ] Implement `extract_patterns()` (look for "Pattern:" keywords)
  - [ ] Implement `extract_dependencies()` (Python package names)
  - [ ] Implement `extract_loc_estimate()` (look for "LOC:" or "lines:")
  - [ ] Implement all other abstract methods

- [ ] **Create ReactPlanParser**
  - [ ] Implement `extract_files()` (regex for `.tsx?` files)
  - [ ] Implement `extract_patterns()` (React-specific patterns)
  - [ ] Implement `extract_dependencies()` (npm package names)
  - [ ] Implement all other abstract methods

- [ ] **Create GenericPlanParser**
  - [ ] Implement basic regex-based extraction
  - [ ] Fallback for unknown formats
  - [ ] Extract what's possible, leave rest empty

- [ ] **Create factory function**
  - [ ] `create_plan_parser(stack: str) -> PlanParser`
  - [ ] Map stack names to parser classes
  - [ ] Default to GenericPlanParser for unknown stacks

- [ ] **Write unit tests** (`tests/unit/test_plan_parser.py`)
  - [ ] Test PythonPlanParser with sample Python plan
  - [ ] Test ReactPlanParser with sample React plan
  - [ ] Test GenericPlanParser with unstructured plan
  - [ ] Test factory function returns correct parser
  - [ ] Test parser accuracy (files, patterns, dependencies)
  - [ ] **Run tests**: `pytest tests/unit/test_plan_parser.py -v`
  - [ ] **Target coverage**: ≥85%

**Sample Test Data** (add to test file):
```python
SAMPLE_PYTHON_PLAN = """
Implementation Plan

Files to create:
- src/api/routes/users.py
- src/services/user_service.py
- tests/test_users.py

Patterns:
- Repository Pattern for data access
- Service Layer for business logic

Dependencies:
- fastapi
- pydantic
- sqlalchemy

Estimated LOC: 250 lines
Estimated Duration: 2-3 hours
"""
```

**Validation**:
```bash
# Run tests
pytest tests/unit/test_plan_parser.py -v --cov=installer/global/commands/lib/plan_parser

# Expected: All tests passing, coverage ≥85%
```

### Afternoon: Phase 2.7 Handler (4 hours)

#### 3. Create phase_27_handler.py (4 hours)

**File**: `/installer/global/commands/lib/phase_27_handler.py`

- [ ] **Create Phase27Handler class**
  - [ ] Add `__init__(self)` method
  - [ ] Add `handle(self, context: TaskContext) -> TaskContext` method

- [ ] **Implement plan parsing**
  - [ ] Detect stack from context.detected_stack
  - [ ] Create parser: `parser = create_plan_parser(context.detected_stack)`
  - [ ] Parse plan: `plan = parser.parse(context.phase_2_output, context.task_id)`
  - [ ] Handle PlanParsingError (try GenericPlanParser fallback)

- [ ] **Implement complexity calculation**
  - [ ] Create EvaluationContext from TaskContext
  - [ ] Call ComplexityCalculator: `complexity_score = calculator.calculate(eval_context)`
  - [ ] Handle ComplexityCalculationError (escalate to FULL_REQUIRED)

- [ ] **Implement state persistence**
  - [ ] Save ImplementationPlan to JSON: `context.get_plan_path()`
  - [ ] Save ComplexityScore to JSON: `context.get_complexity_path()`
  - [ ] Use atomic write (FileOperations.atomic_write if needed)
  - [ ] Log errors if save fails (continue anyway)

- [ ] **Update context**
  - [ ] Set `context.implementation_plan = plan`
  - [ ] Set `context.complexity_score = complexity_score`
  - [ ] Set `context.review_mode = complexity_score.review_mode`

- [ ] **Error handling**
  - [ ] Wrap in try/except for all operations
  - [ ] On PlanParsingError: Try GenericPlanParser, then escalate to FULL_REQUIRED
  - [ ] On ComplexityCalculationError: Set review_mode to FULL_REQUIRED
  - [ ] On FileSystemError: Log error, continue (don't block workflow)

- [ ] **Write unit tests** (`tests/unit/test_phase_27_handler.py`)
  - [ ] Test successful plan parsing and complexity calculation
  - [ ] Test parser error fallback to GenericPlanParser
  - [ ] Test complexity calculation error escalates to FULL_REQUIRED
  - [ ] Test state file creation
  - [ ] Test context updates (plan, complexity_score, review_mode)
  - [ ] **Run tests**: `pytest tests/unit/test_phase_27_handler.py -v`
  - [ ] **Target coverage**: ≥90%

**Validation**:
```bash
# Run tests
pytest tests/unit/test_phase_27_handler.py -v --cov=installer/global/commands/lib/phase_27_handler

# Expected: All tests passing, coverage ≥90%

# Manual test: Run handler with sample plan
python -c "
from phase_27_handler import Phase27Handler
from task_context import TaskContext
context = TaskContext(task_id='TEST-001', detected_stack='python', ...)
handler = Phase27Handler()
result = handler.handle(context)
print(f'Complexity Score: {result.complexity_score.total_score}')
print(f'Review Mode: {result.review_mode}')
"
```

**Day 1 End-of-Day Validation**:
- [ ] All Day 1 tests passing
- [ ] Coverage reports generated
- [ ] No linting errors (`flake8 installer/global/commands/lib/`)
- [ ] Git commit: "Day 1: Implemented task_context, plan_parser, phase_27_handler"

---

## Day 2: Phase 2.8 Foundation (8 hours)

### Morning: State Machine & Commands (6 hours)

#### 4. Create review_state_machine.py (3 hours)

**File**: `/installer/global/commands/lib/review_state_machine.py`

- [ ] **Create ReviewState enum**
  - [ ] AUTO_PROCEED = "auto_proceed"
  - [ ] QUICK_OPTIONAL = "quick_optional"
  - [ ] FULL_REQUIRED = "full_required"
  - [ ] PHASE_3 = "phase_3"
  - [ ] BACKLOG = "backlog"

- [ ] **Create ReviewStateMachine class**
  - [ ] `__init__(self, initial_state: ReviewState)`
  - [ ] `current_state` attribute
  - [ ] `history` list to track transitions

- [ ] **Implement transition method**
  - [ ] `transition(self, action: str, context: TaskContext) -> ReviewState`
  - [ ] Define transition table dictionary
  - [ ] Map (state, action) tuples to handler methods

- [ ] **Implement transition handlers**
  - [ ] `_auto_proceed(context) -> ReviewState` → Returns PHASE_3
  - [ ] `_quick_timeout(context) -> ReviewState` → Returns PHASE_3
  - [ ] `_quick_escalate(context) -> ReviewState` → Returns FULL_REQUIRED
  - [ ] `_approve(context) -> ReviewState` → Returns PHASE_3
  - [ ] `_cancel(context) -> ReviewState` → Returns BACKLOG

- [ ] **Add validation**
  - [ ] Raise ValueError for invalid transitions
  - [ ] Log state transitions

- [ ] **Write unit tests** (`tests/unit/test_review_state_machine.py`)
  - [ ] Test valid transitions (all paths)
  - [ ] Test invalid transitions raise ValueError
  - [ ] Test state history tracking
  - [ ] Test context updates during transitions
  - [ ] **Run tests**: `pytest tests/unit/test_review_state_machine.py -v`
  - [ ] **Target coverage**: ≥95%

**Validation**:
```bash
pytest tests/unit/test_review_state_machine.py -v --cov=installer/global/commands/lib/review_state_machine
```

#### 5. Create review_commands.py (3 hours)

**File**: `/installer/global/commands/lib/review_commands.py`

- [ ] **Create ReviewCommand base class**
  - [ ] Define abstract `execute(context: TaskContext) -> TaskContext` method
  - [ ] Define abstract `undo(context: TaskContext) -> TaskContext` method (for rollback)

- [ ] **Create ApproveCommand**
  - [ ] Implement `execute()`: Set `context.approved = True`, `proceed_to_phase_3 = True`
  - [ ] Update task metadata with approval timestamp
  - [ ] Implement `undo()`: Revert approval (no-op for approve)

- [ ] **Create CancelCommand**
  - [ ] Implement `execute()`: Set `context.cancelled = True`, `status = 'backlog'`
  - [ ] Update task metadata with cancellation timestamp
  - [ ] Move task file to backlog directory
  - [ ] Implement `undo()`: Restore task to in_progress (if needed)

- [ ] **Create ModifyCommand (STUB)**
  - [ ] Implement `execute()`: Print "Modification mode coming soon (TASK-003B-3)"
  - [ ] Return None (signals re-prompt in Phase 2.8)
  - [ ] Full implementation deferred to TASK-003B-3

- [ ] **Write unit tests** (`tests/unit/test_review_commands.py`)
  - [ ] Test ApproveCommand sets correct flags
  - [ ] Test CancelCommand moves task to backlog
  - [ ] Test ModifyCommand stub returns None
  - [ ] Test command execution updates context
  - [ ] **Run tests**: `pytest tests/unit/test_review_commands.py -v`
  - [ ] **Target coverage**: ≥85%

**Validation**:
```bash
pytest tests/unit/test_review_commands.py -v --cov=installer/global/commands/lib/review_commands
```

### Afternoon: Phase 2.8 Handler (2 hours)

#### 6. Create phase_28_handler.py (2 hours)

**File**: `/installer/global/commands/lib/phase_28_handler.py`

- [ ] **Create Phase28Handler class**
  - [ ] Add `__init__(self)` method
  - [ ] Add `handle(self, context: TaskContext) -> TaskContext` method

- [ ] **Implement routing logic**
  - [ ] Check `context.review_mode`
  - [ ] Route to appropriate handler:
    - [ ] AUTO_PROCEED → `_handle_auto_proceed()`
    - [ ] QUICK_OPTIONAL → `_handle_quick_review()`
    - [ ] FULL_REQUIRED → `_handle_full_review()`

- [ ] **Implement _handle_auto_proceed()**
  - [ ] Display complexity summary
  - [ ] Update context: `auto_approved = True`
  - [ ] Update task metadata
  - [ ] Set `proceed_to_phase_3 = True`

- [ ] **Implement _handle_quick_review()**
  - [ ] Create QuickReviewHandler (from TASK-003B-1)
  - [ ] Execute: `result = handler.execute()`
  - [ ] Handle result:
    - [ ] `result.action == "timeout"` → Auto-approve, proceed to Phase 3
    - [ ] `result.action == "enter"` → Escalate to `_handle_full_review()`
    - [ ] `result.action == "cancel"` → Cancel task, move to backlog
  - [ ] Update context with result metadata

- [ ] **Implement _handle_full_review()**
  - [ ] Create FullReviewHandler (from TASK-003B-1)
  - [ ] Execute: `result = handler.execute()`
  - [ ] Handle result:
    - [ ] `result.action == "approve"` → Approve, proceed to Phase 3
    - [ ] `result.action == "cancel"` → Cancel task, move to backlog
    - [ ] `result.action == "modify"` → Stub message, re-prompt (defer to TASK-003B-3)
  - [ ] Update context with result metadata

- [ ] **Error handling**
  - [ ] Wrap QuickReviewHandler in try/except
  - [ ] On error: Escalate to FullReviewHandler (fail-safe)
  - [ ] On KeyboardInterrupt: Treat as cancellation

- [ ] **Write unit tests** (`tests/unit/test_phase_28_handler.py`)
  - [ ] Test AUTO_PROCEED routing
  - [ ] Test QUICK_OPTIONAL routing (timeout, escalate, cancel)
  - [ ] Test FULL_REQUIRED routing (approve, cancel)
  - [ ] Test error escalation from quick to full review
  - [ ] Test context updates after each path
  - [ ] **Run tests**: `pytest tests/unit/test_phase_28_handler.py -v`
  - [ ] **Target coverage**: ≥90%

**Validation**:
```bash
pytest tests/unit/test_phase_28_handler.py -v --cov=installer/global/commands/lib/phase_28_handler

# Expected: All tests passing, coverage ≥90%
```

**Day 2 End-of-Day Validation**:
- [ ] All Day 2 tests passing
- [ ] Coverage reports show ≥85% overall
- [ ] No linting errors
- [ ] Git commit: "Day 2: Implemented review state machine, commands, phase_28_handler"

---

## Day 3: Integration & Testing (8 hours)

### Morning: Command Integration (5 hours)

#### 7. Update task-manager.md (3 hours)

**File**: `/installer/global/agents/task-manager.md`

- [ ] **Add Phase 2.7 orchestration section** (after Phase 2.5)
  - [ ] Document Phase 2.7 responsibilities
  - [ ] Add step: Invoke plan generation specialist
  - [ ] Add step: Parse plan into ImplementationPlan
  - [ ] Add step: Calculate complexity score
  - [ ] Add step: Detect force-review triggers
  - [ ] Add step: Determine ReviewMode
  - [ ] Add step: Save state to filesystem
  - [ ] Add step: Return ComplexityScore + ReviewMode

- [ ] **Add Phase 2.8 orchestration section**
  - [ ] Document Phase 2.8 responsibilities
  - [ ] Add routing logic:
    - [ ] AUTO_PROCEED path documentation
    - [ ] QUICK_OPTIONAL path documentation
    - [ ] FULL_REQUIRED path documentation
  - [ ] Add modification loop documentation (stub for now)
  - [ ] Add error handling patterns

- [ ] **Add metadata schema documentation**
  - [ ] Document new frontmatter fields:
    - [ ] `implementation_plan` structure
    - [ ] `complexity_evaluation` structure
    - [ ] `phase_28_session` structure

- [ ] **Review and validate**
  - [ ] Read updated task-manager.md end-to-end
  - [ ] Ensure clear, actionable instructions for Claude
  - [ ] No contradictions with existing phases
  - [ ] Git commit: "Updated task-manager.md with Phase 2.7/2.8 orchestration"

#### 8. Update task-work.md (2 hours)

**File**: `/installer/global/commands/task-work.md`

- [ ] **Insert Phase 2.7 invocation** (after Phase 2.5B)
  - [ ] Add section header: `#### Phase 2.7: Plan Generation & Complexity Evaluation (NEW)`
  - [ ] Add INVOKE Task tool instruction:
    - [ ] `subagent_type: "task-manager"`
    - [ ] `description: "Generate structured plan and evaluate complexity"`
    - [ ] Detailed prompt with Phase 2.7 steps
  - [ ] Add WAIT instruction
  - [ ] Add EXTRACT complexity_score and review_mode

- [ ] **Insert Phase 2.8 invocation** (after Phase 2.7)
  - [ ] Add section header: `#### Phase 2.8: Human Plan Checkpoint (NEW)`
  - [ ] Add ROUTE instruction based on review_mode
  - [ ] Add IF/ELSE IF/ELSE blocks for three review modes
  - [ ] For each mode:
    - [ ] INVOKE Task tool with appropriate handler
    - [ ] WAIT for result
    - [ ] Handle result (proceed/escalate/cancel)

- [ ] **Update Phase 3 preconditions**
  - [ ] Add check: `IF context.proceed_to_phase_3 == True`
  - [ ] Only invoke Phase 3 after Phase 2.8 approval

- [ ] **Review and validate**
  - [ ] Read updated task-work.md end-to-end
  - [ ] Ensure execution protocol intact
  - [ ] No breaking changes to existing phases
  - [ ] Git commit: "Updated task-work.md with Phase 2.7/2.8 invocations"

### Afternoon: Integration Testing (3 hours)

#### 9. Create integration tests (3 hours)

**File**: `/tests/integration/test_phase_27_28_integration.py`

- [ ] **Setup test fixtures**
  - [ ] Create `create_test_task()` helper
  - [ ] Create sample plans (low, medium, high complexity)
  - [ ] Create mock task files in temporary directory

- [ ] **Test auto-proceed workflow**
  - [ ] Test name: `test_auto_proceed_workflow()`
  - [ ] Setup: Create low complexity task (1 file, no patterns)
  - [ ] Execute Phase 2.7
  - [ ] Assert: `review_mode == AUTO_PROCEED`
  - [ ] Execute Phase 2.8
  - [ ] Assert: `auto_approved == True`, `proceed_to_phase_3 == True`

- [ ] **Test quick review timeout**
  - [ ] Test name: `test_quick_review_timeout()`
  - [ ] Setup: Create medium complexity task
  - [ ] Execute Phase 2.7
  - [ ] Assert: `review_mode == QUICK_OPTIONAL`
  - [ ] Mock countdown_timer to return "timeout"
  - [ ] Execute Phase 2.8
  - [ ] Assert: `auto_approved == True`, `proceed_to_phase_3 == True`

- [ ] **Test quick review escalation**
  - [ ] Test name: `test_quick_review_escalation()`
  - [ ] Setup: Create medium complexity task
  - [ ] Mock countdown_timer to return "enter"
  - [ ] Mock full review input to return 'a' (approve)
  - [ ] Execute Phase 2.8
  - [ ] Assert: `escalated == True`, `approved == True`, `proceed_to_phase_3 == True`

- [ ] **Test full review approve**
  - [ ] Test name: `test_full_review_approve()`
  - [ ] Setup: Create high complexity task
  - [ ] Execute Phase 2.7
  - [ ] Assert: `review_mode == FULL_REQUIRED`
  - [ ] Mock full review input to return 'a'
  - [ ] Execute Phase 2.8
  - [ ] Assert: `approved == True`, `proceed_to_phase_3 == True`

- [ ] **Test full review cancel**
  - [ ] Test name: `test_full_review_cancel()`
  - [ ] Setup: Create high complexity task
  - [ ] Mock full review input to return 'c', then 'y' (confirm)
  - [ ] Execute Phase 2.8
  - [ ] Assert: `cancelled == True`, `proceed_to_phase_3 == False`
  - [ ] Assert: Task file moved to backlog

- [ ] **Test force-review triggers**
  - [ ] Test name: `test_force_review_triggers()`
  - [ ] Setup: Create task with security keywords (score would be 3)
  - [ ] Execute Phase 2.7
  - [ ] Assert: `review_mode == FULL_REQUIRED` (overridden by trigger)

- [ ] **Run integration tests**
  - [ ] `pytest tests/integration/test_phase_27_28_integration.py -v`
  - [ ] **Target**: 100% of user paths covered
  - [ ] Fix any failures

**Validation**:
```bash
# Run all integration tests
pytest tests/integration/ -v

# Expected: All tests passing, 100% user path coverage
```

**Day 3 End-of-Day Validation**:
- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] task-work.md and task-manager.md updated
- [ ] Git commit: "Day 3: Integrated Phase 2.7/2.8 into task-work workflow + integration tests"

---

## Day 4: Polish & Documentation (8 hours)

### Morning: Error Handling & Manual Testing (5 hours)

#### 10. Error handling refinement (2 hours)

**Files**: Various (`phase_27_handler.py`, `phase_28_handler.py`, etc.)

- [ ] **Review error handling in Phase 2.7**
  - [ ] Ensure PlanParsingError caught and handled
  - [ ] Ensure ComplexityCalculationError caught and handled
  - [ ] Ensure FileSystemError logged but doesn't block
  - [ ] Add logging statements for debugging

- [ ] **Review error handling in Phase 2.8**
  - [ ] Ensure QuickReviewHandler errors escalate to full review
  - [ ] Ensure FullReviewHandler errors logged
  - [ ] Ensure KeyboardInterrupt treated as cancellation
  - [ ] Add error recovery instructions in messages

- [ ] **Add graceful degradation**
  - [ ] On any critical error: Display message, escalate to full review
  - [ ] Never auto-proceed on errors
  - [ ] Preserve all work completed so far

- [ ] **Test error scenarios**
  - [ ] Manually trigger plan parsing error (invalid format)
  - [ ] Manually trigger complexity calculation error (corrupt data)
  - [ ] Verify escalation to full review
  - [ ] Verify work is preserved

**Validation**:
```bash
# Run tests with error injection
pytest tests/ -v --cov

# Manually test error scenarios (corrupt plan format, etc.)
```

#### 11. Documentation updates (2 hours)

**File**: `/CLAUDE.md`

- [ ] **Add Phase 2.7/2.8 to workflow overview**
  - [ ] Update "Complete Agentecflow Workflows" section
  - [ ] Add Phase 2.7 step
  - [ ] Add Phase 2.8 step with three routing modes

- [ ] **Update command reference**
  - [ ] Document Phase 2.7 outputs (state files)
  - [ ] Document Phase 2.8 user interactions
  - [ ] Add examples of each review mode

- [ ] **Add state file documentation**
  - [ ] Document `docs/state/{task_id}/` structure
  - [ ] Document JSON file formats
  - [ ] Add examples

**File**: `/README.md` (if exists)

- [ ] Update with Phase 2.7/2.8 information
- [ ] Add complexity scoring explanation
- [ ] Add review mode routing table

**Validation**:
- [ ] Read updated CLAUDE.md end-to-end
- [ ] Ensure clarity and completeness
- [ ] No contradictions

#### 12. Manual testing (3 hours)

**Test across technology stacks**:

- [ ] **Python stack**
  - [ ] Create test task: `TASK-TEST-PY-001`
  - [ ] Run `/task-work TASK-TEST-PY-001`
  - [ ] Verify Phase 2.7 parses plan correctly
  - [ ] Verify Phase 2.8 routing based on complexity
  - [ ] Test all three review modes (create 3 tasks with different complexities)

- [ ] **React stack**
  - [ ] Create test task: `TASK-TEST-REACT-001`
  - [ ] Run `/task-work TASK-TEST-REACT-001`
  - [ ] Verify React-specific plan parsing
  - [ ] Test quick review mode

- [ ] **TypeScript API stack** (if available)
  - [ ] Create test task: `TASK-TEST-TS-001`
  - [ ] Verify TypeScript plan parsing
  - [ ] Test full review mode

- [ ] **Generic stack (fallback)**
  - [ ] Create task with unusual plan format
  - [ ] Verify GenericPlanParser fallback
  - [ ] Verify still routes to correct review mode

**Test error scenarios**:

- [ ] Invalid plan format → GenericPlanParser fallback
- [ ] Missing plan data → Escalate to full review
- [ ] Ctrl+C during countdown → Treat as cancellation
- [ ] Ctrl+C during full review → Confirm cancellation

**Test state persistence**:

- [ ] Run Phase 2.7 → Check `docs/state/TASK-XXX/implementation_plan_v1.json` exists
- [ ] Check `complexity_score_v1.json` exists
- [ ] Verify JSON content is valid
- [ ] Modify plan (stub) → Verify version increment (deferred to TASK-003B-3)

**Validation**:
- [ ] All manual tests pass
- [ ] State files created correctly
- [ ] No crashes or errors
- [ ] User experience is smooth

### Afternoon: Code Review & Deployment (3 hours)

#### 13. Code review & cleanup (2 hours)

- [ ] **Self-review all code**
  - [ ] Read all new files end-to-end
  - [ ] Check for code smells, duplications
  - [ ] Ensure consistent naming conventions
  - [ ] Remove debug print statements
  - [ ] Add docstrings where missing

- [ ] **Run linting**
  - [ ] `flake8 installer/global/commands/lib/`
  - [ ] Fix all linting errors
  - [ ] `mypy installer/global/commands/lib/` (if type hints used)
  - [ ] Fix type errors

- [ ] **Run full test suite**
  - [ ] `pytest tests/ -v --cov`
  - [ ] Ensure ≥85% overall coverage
  - [ ] Fix any failing tests

- [ ] **Performance check**
  - [ ] Run Phase 2.7 on sample task, measure duration
  - [ ] Target: <2 seconds
  - [ ] If >2s, profile and optimize

**Validation**:
```bash
# Linting
flake8 installer/global/commands/lib/ --max-line-length=120

# Type checking
mypy installer/global/commands/lib/ --ignore-missing-imports

# Full test suite
pytest tests/ -v --cov=installer/global/commands/lib --cov-report=html

# Open coverage report
open htmlcov/index.html
```

#### 14. Prepare for deployment (1 hour)

- [ ] **Create feature flag** (optional)
  - [ ] Add to `.claude/settings.json`:
    ```json
    {
      "features": {
        "phase_27_28_enabled": true
      }
    }
    ```
  - [ ] Add check in task-work.md to skip if disabled

- [ ] **Create rollback plan**
  - [ ] Document rollback steps in `/docs/adr/TASK-003C-rollback-plan.md`
  - [ ] Test feature flag disable → Verify Phase 2 → Phase 3 direct transition

- [ ] **Final Git commits**
  - [ ] Review all changes: `git diff main`
  - [ ] Create final commit: `git commit -m "TASK-003C: Complete Phase 2.7/2.8 integration"`
  - [ ] Create branch: `git checkout -b task-003c-phase-27-28-integration`
  - [ ] Push: `git push origin task-003c-phase-27-28-integration`

- [ ] **Create pull request**
  - [ ] Title: "TASK-003C: Integrate Phase 2.7 and Phase 2.8 into task-work workflow"
  - [ ] Description: Link to architecture doc, summary of changes
  - [ ] Assign reviewers
  - [ ] Add labels: `enhancement`, `workflow`, `phase-2.7`, `phase-2.8`

**Day 4 End-of-Day Validation**:
- [ ] All tests passing (unit + integration)
- [ ] Coverage ≥85%
- [ ] No linting errors
- [ ] Documentation complete
- [ ] Pull request created
- [ ] Ready for review and deployment

---

## Post-Implementation Checklist

### Pre-Deployment Validation

- [ ] **All tests passing**
  - [ ] Unit tests: `pytest tests/unit/ -v`
  - [ ] Integration tests: `pytest tests/integration/ -v`
  - [ ] Coverage report: ≥85%

- [ ] **Code quality**
  - [ ] Linting: 0 errors (`flake8`)
  - [ ] Type checking: 0 errors (`mypy`)
  - [ ] Code review approved

- [ ] **Documentation**
  - [ ] CLAUDE.md updated
  - [ ] Architecture document complete
  - [ ] Executive summary complete
  - [ ] Diagrams created

- [ ] **Manual testing**
  - [ ] Tested on ≥3 technology stacks
  - [ ] All review modes tested
  - [ ] Error scenarios tested

### Deployment Steps

- [ ] **Alpha deployment**
  - [ ] Deploy to dev environment
  - [ ] Feature flag enabled for alpha users only
  - [ ] Monitor for 24 hours
  - [ ] Collect initial feedback

- [ ] **Beta deployment**
  - [ ] Enable for larger user group
  - [ ] Monitor error rates (target: <1%)
  - [ ] Track complexity score distribution
  - [ ] Gather usage metrics

- [ ] **Production deployment**
  - [ ] Enable for all users
  - [ ] Monitor closely for first week
  - [ ] Document any issues
  - [ ] Plan iteration based on feedback

### Post-Deployment Monitoring

- [ ] **Metrics collection**
  - [ ] Track review mode distribution (auto/quick/full)
  - [ ] Track auto-proceed rate (target: 40-50%)
  - [ ] Track escalation rate (target: 20-30%)
  - [ ] Track cancellation rate (target: <5%)

- [ ] **Error monitoring**
  - [ ] Monitor error logs for Phase 2.7/2.8
  - [ ] Track fail-safe escalations
  - [ ] Monitor state file corruption rate (target: 0%)

- [ ] **User feedback**
  - [ ] Collect user feedback on review modes
  - [ ] Adjust complexity scoring if needed
  - [ ] Iterate on UI/UX based on feedback

---

## Common Issues & Solutions

### Issue: Plan parsing fails for specific stack

**Solution**:
- Check GenericPlanParser fallback is working
- Add stack-specific parser if pattern is common
- Improve regex patterns in existing parser

### Issue: Complexity calculation returns unexpected scores

**Solution**:
- Review factor calculations in ComplexityCalculator
- Adjust thresholds if needed (1-3 / 4-6 / 7-10 ranges)
- Add logging to see factor breakdown

### Issue: State files not created

**Solution**:
- Check filesystem permissions
- Verify `docs/state/` directory exists
- Check FileOperations.atomic_write implementation

### Issue: Quick review countdown doesn't work on Windows

**Solution**:
- Verify WindowsInputStrategy is used
- Check msvcrt import
- Test with polling interval adjustments

### Issue: Integration tests fail intermittently

**Solution**:
- Check for timing issues (countdown tests)
- Use mocks consistently
- Ensure test isolation (clean temp files)

---

## Success Criteria (Final Validation)

### Functional Requirements ✅

- [ ] Phase 2.7 parses plans for all supported stacks
- [ ] Phase 2.7 calculates complexity scores correctly
- [ ] Phase 2.8 routes to correct review mode based on score
- [ ] Auto-proceed path works (low complexity)
- [ ] Quick review path works (timeout and escalation)
- [ ] Full review path works (approve and cancel)
- [ ] State files created and persisted
- [ ] Task metadata updated correctly

### Non-Functional Requirements ✅

- [ ] Phase 2.7 execution time: <2 seconds
- [ ] Phase 2.8 auto-proceed overhead: <1 second
- [ ] Quick review countdown accuracy: ±1 second
- [ ] Unit test coverage: ≥85%
- [ ] Integration test coverage: 100% of user paths
- [ ] Code review approved
- [ ] Documentation complete

### User Experience ✅

- [ ] Low complexity tasks proceed smoothly (no friction)
- [ ] Medium complexity tasks offer optional review (user control)
- [ ] High complexity tasks require review (safety)
- [ ] Error messages are clear and actionable
- [ ] Cancellation works smoothly
- [ ] Work is preserved on errors

---

## Estimated Hours Breakdown

| Day | Task | Estimated Hours | Actual Hours |
|-----|------|----------------|--------------|
| 1 | task_context.py | 2h | |
| 1 | plan_parser.py | 4h | |
| 1 | phase_27_handler.py | 2h | |
| 2 | review_state_machine.py | 3h | |
| 2 | review_commands.py | 3h | |
| 2 | phase_28_handler.py | 2h | |
| 3 | task-manager.md updates | 3h | |
| 3 | task-work.md updates | 2h | |
| 3 | Integration tests | 3h | |
| 4 | Error handling | 2h | |
| 4 | Documentation | 2h | |
| 4 | Manual testing | 3h | |
| 4 | Code review & deployment | 3h | |
| **Total** | | **32h** | |

---

**Document Version**: 1.0
**Created**: 2025-10-10
**Last Updated**: 2025-10-10

**Ready to start implementation!** 🚀
