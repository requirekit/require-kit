# TASK-003E Phase 5 Day 3: Boundary & State Edge Cases
## Requirements Analysis Report

**Date**: 2025-10-10
**Task ID**: TASK-003E
**Phase**: Phase 5 Day 3 - Boundary & State Edge Cases Testing
**Status**: Requirements Analysis Complete
**Priority**: HIGH

---

## Executive Summary

This document provides a comprehensive requirements analysis for TASK-003E Phase 5 Day 3, focusing on **Boundary Conditions** and **Concurrency & State Management** edge cases. The analysis extracts testable requirements from the task acceptance criteria and identifies gaps that need clarification before implementation.

### Scope Overview
- **Boundary Conditions**: 5 edge cases (file counts, dependencies, plan sections)
- **Concurrency & State**: 4 edge cases (versioning, complexity changes, Q&A limits, timeouts)
- **Total Edge Cases**: 9 test scenarios
- **Estimated Tests**: 18-22 tests (2-3 tests per edge case)
- **Implementation Time**: 1 day

---

## Part 1: Boundary Conditions Requirements

### REQ-BC-001: Task with 0 Files Edge Case

**EARS Notation** (Boundary Condition):
```
When a task has zero files to create, the system shall calculate a minimum complexity score of 1
```

**Rationale**: A task with no files is an edge case that could cause division by zero or null pointer issues in scoring logic. The system must handle this gracefully with a minimum viable score.

**Current Implementation Status**:
✅ **IMPLEMENTED**: `complexity_calculator.py` line 196 enforces `max(final_score, 1)`

**Acceptance Criteria**:
- [ ] Task with `files_to_create = []` returns score ≥ 1
- [ ] Task with `files_to_create = []` returns score ≤ 10
- [ ] Score calculation does not crash or raise exception
- [ ] Score is deterministic (same input = same output)

**Test Scenarios**:
1. **test_task_with_zero_files_minimum_score** - Verify score ≥ 1
2. **test_task_with_zero_files_does_not_crash** - No exceptions raised
3. **test_task_with_zero_files_deterministic** - Consistent scoring

**Technical Considerations**:
- File complexity factor evaluation with empty list
- Pattern familiarity evaluation with no files to analyze
- Risk assessment with no implementation surface area

**Implementation Notes**:
```python
# Current implementation in complexity_calculator.py (line 196)
final_score = max(final_score, 1)  # ✅ Already enforced
```

**Validation Approach**:
```python
def test_task_with_zero_files_minimum_score():
    """Test task with 0 files defaults to minimum score."""
    plan = ImplementationPlan(
        task_id="TASK-ZERO-FILES",
        files_to_create=[],  # Empty
        patterns_used=[],
        external_dependencies=[]
    )

    calculator = ComplexityCalculator()
    context = EvaluationContext(
        task_id="TASK-ZERO-FILES",
        technology_stack="python",
        implementation_plan=plan
    )

    score = calculator.calculate(context)

    # Assertions
    assert score.total_score >= 1, "Score must be at least 1"
    assert score.total_score <= 10, "Score must not exceed 10"
    assert score.review_mode in [ReviewMode.AUTO_PROCEED, ReviewMode.QUICK_OPTIONAL, ReviewMode.FULL_REQUIRED]
```

---

### REQ-BC-002: Task with 50+ Files (Very Complex)

**EARS Notation** (Boundary Condition):
```
When a task has 50 or more files to create, the system shall cap the complexity score at 10
```

**Rationale**: Tasks with extreme file counts should not result in unbounded complexity scores. A maximum cap of 10 ensures consistency and prevents score overflow.

**Current Implementation Status**:
✅ **IMPLEMENTED**: `complexity_calculator.py` line 190 caps at `MAX_TOTAL_SCORE = 10`

**Acceptance Criteria**:
- [ ] Task with 50 files returns score = 10 (capped)
- [ ] Task with 100 files returns score = 10 (capped)
- [ ] Task with 500 files returns score = 10 (capped)
- [ ] Review mode for 50+ files = FULL_REQUIRED

**Test Scenarios**:
1. **test_task_with_50_plus_files_capped_at_10** - Verify score = 10
2. **test_task_with_100_files_still_capped** - Extreme stress test
3. **test_task_with_50_files_forces_full_review** - Verify FULL_REQUIRED mode

**Technical Considerations**:
- File complexity factor scoring algorithm
- Performance of complexity calculation with large file lists
- Memory usage for large plan objects

**Implementation Notes**:
```python
# Current implementation in complexity_calculator.py (line 190)
capped_total = min(raw_total, self.MAX_TOTAL_SCORE)  # ✅ Already enforced
```

**Validation Approach**:
```python
def test_task_with_50_plus_files_very_complex():
    """Test task with 50+ files is capped at max complexity."""
    plan = ImplementationPlan(
        task_id="TASK-LARGE",
        files_to_create=[f"file_{i}.py" for i in range(50)],  # 50 files
        patterns_used=["event_sourcing", "saga", "cqrs"],  # Complex patterns
        external_dependencies=["kafka", "redis", "postgres"]
    )

    calculator = ComplexityCalculator()
    context = EvaluationContext(
        task_id="TASK-LARGE",
        technology_stack="python",
        implementation_plan=plan
    )

    score = calculator.calculate(context)

    # Assertions
    assert score.total_score == 10, "Score should be capped at 10"
    assert score.review_mode == ReviewMode.FULL_REQUIRED, "Should require full review"
    assert len(score.factor_scores) > 0, "Should have factor scores"
```

**Performance Requirement**:
- Complexity calculation for 50+ files must complete in <1 second

---

### REQ-BC-003: Task with No Dependencies

**EARS Notation** (Ubiquitous):
```
The system shall score a task with zero external dependencies as having zero dependency complexity
```

**Rationale**: Self-contained tasks with no external dependencies have lower integration risk and should not be penalized with dependency complexity.

**Current Implementation Status**:
⚠️ **PARTIALLY IMPLEMENTED**: Dependency complexity factor is documented as "future implementation" (not yet scored)

**Acceptance Criteria**:
- [ ] Task with `external_dependencies = []` does not fail
- [ ] Dependency factor score = 0 (if factor is implemented)
- [ ] Overall complexity score is unaffected by missing dependencies
- [ ] No exceptions raised during calculation

**Test Scenarios**:
1. **test_task_with_no_dependencies_handles_gracefully** - No crash
2. **test_task_with_no_dependencies_zero_penalty** - Verify no penalty applied
3. **test_task_with_no_dependencies_valid_score** - Score in valid range 1-10

**Technical Considerations**:
- Dependency complexity factor is currently a stub (future implementation)
- Empty dependency list should be valid input
- No penalty should be applied for self-contained tasks

**Implementation Notes**:
```python
# Dependency complexity factor is documented as future implementation
# Currently not evaluated, so empty list is handled gracefully by default
```

**Validation Approach**:
```python
def test_task_with_no_dependencies():
    """Test task with no external dependencies scores correctly."""
    plan = ImplementationPlan(
        task_id="TASK-SELF-CONTAINED",
        files_to_create=["main.py"],
        patterns_used=["singleton"],
        external_dependencies=[]  # No dependencies
    )

    calculator = ComplexityCalculator()
    context = EvaluationContext(
        task_id="TASK-SELF-CONTAINED",
        technology_stack="python",
        implementation_plan=plan
    )

    score = calculator.calculate(context)

    # Assertions
    assert score.total_score >= 1
    assert score.total_score <= 10

    # If dependency factor is implemented, verify it's 0
    dep_factor = next((f for f in score.factor_scores if "dependency" in f.factor_name.lower()), None)
    if dep_factor:
        assert dep_factor.score == 0, "Dependency score should be 0 for self-contained tasks"
```

---

### REQ-BC-004: Task with 10+ Dependencies

**EARS Notation** (Boundary Condition):
```
When a task has 10 or more external dependencies, the system shall handle the calculation gracefully without exceeding score limits
```

**Rationale**: Tasks with many external dependencies have higher integration complexity. The system must handle high dependency counts without overflow or performance issues.

**Current Implementation Status**:
⚠️ **PARTIALLY IMPLEMENTED**: Dependency complexity factor is documented as "future implementation" (not yet scored)

**Acceptance Criteria**:
- [ ] Task with 10 dependencies does not crash
- [ ] Task with 15 dependencies returns valid score (1-10)
- [ ] Calculation completes in <1 second
- [ ] Score reflects high integration complexity (if factor implemented)

**Test Scenarios**:
1. **test_task_with_10_plus_dependencies_handles_gracefully** - No crash
2. **test_task_with_15_dependencies_valid_score** - Score in valid range
3. **test_task_with_20_dependencies_performance** - Calculation time <1s

**Technical Considerations**:
- Future dependency complexity factor will need dependency count scoring
- High dependency count could indicate microservice integration complexity
- Performance impact of processing large dependency lists

**Implementation Notes**:
```python
# Dependency complexity factor is documented as future implementation
# When implemented, should cap dependency contribution to avoid overflow
# Example: min(dependency_count / 5, 3) for max +3 score contribution
```

**Validation Approach**:
```python
def test_task_with_10_plus_dependencies():
    """Test task with 10+ external dependencies."""
    plan = ImplementationPlan(
        task_id="TASK-MANY-DEPS",
        files_to_create=["integration.py"],
        patterns_used=["adapter"],
        external_dependencies=[f"lib_{i}" for i in range(15)]  # 15 dependencies
    )

    calculator = ComplexityCalculator()
    context = EvaluationContext(
        task_id="TASK-MANY-DEPS",
        technology_stack="python",
        implementation_plan=plan
    )

    import time
    start_time = time.time()

    score = calculator.calculate(context)

    end_time = time.time()
    calculation_time = end_time - start_time

    # Assertions
    assert score.total_score >= 1
    assert score.total_score <= 10
    assert calculation_time < 1.0, f"Calculation took {calculation_time}s, should be <1s"
```

---

### REQ-BC-005: Empty Plan Sections Display

**EARS Notation** (State-Driven):
```
While displaying a plan with empty sections, the system shall show "Not specified" instead of "None" or empty values
```

**Rationale**: User-facing displays should show friendly messages for missing data instead of technical null/None values.

**Current Implementation Status**:
❌ **NOT IMPLEMENTED**: Current display code may show "None" for empty plan fields (per edge case review document line 151)

**Acceptance Criteria**:
- [ ] Empty `phases` field displays "No implementation phases specified"
- [ ] Empty `estimated_loc` displays "Not specified" instead of "None"
- [ ] Empty `estimated_duration` displays "Not specified" instead of "None"
- [ ] Empty `test_summary` displays "Not specified" instead of "None"
- [ ] No "None" text appears in user-facing output

**Test Scenarios**:
1. **test_empty_plan_sections_display_not_specified** - Verify friendly messages
2. **test_empty_phases_display_friendly_message** - Verify phases handling
3. **test_empty_estimates_display_not_specified** - Verify estimates handling

**Technical Considerations**:
- Review mode display rendering in `review_modes.py`
- Pager display rendering in `pager_display.py`
- Template-based display generation

**Implementation Gap**:
```python
# In review_modes.py - FullReviewDisplay._display_implementation_order()
# Current code may display None values directly
# Need to add None checks and friendly fallbacks

def _display_implementation_order(self) -> None:
    print("\n📋 IMPLEMENTATION ORDER:")

    if self.plan.phases:
        for i, phase in enumerate(self.plan.phases, 1):
            print(f"\n  {i}. {phase}")
    else:
        # ❌ Current: May show "None" or empty
        # ✅ Should show: "No implementation phases specified"
        print("\n  No implementation phases specified")

    # Show estimated LOC if available
    if self.plan.estimated_loc:
        print(f"\n  Estimated Lines of Code: ~{self.plan.estimated_loc}")
    else:
        # ❌ Current: May show "None"
        # ✅ Should show: "Not specified"
        print(f"\n  Estimated Lines of Code: Not specified")
```

**Validation Approach**:
```python
def test_empty_plan_sections_display_not_specified(capsys):
    """Test empty plan sections show 'Not specified' instead of None."""
    plan = ImplementationPlan(
        task_id="TASK-EMPTY",
        files_to_create=["main.py"],
        patterns_used=[],
        external_dependencies=[],
        phases=None,  # Empty
        estimated_loc=None,  # Empty
        estimated_duration=None,  # Empty
        test_summary=None  # Empty
    )

    display = FullReviewDisplay(
        plan=plan,
        complexity_score=mock_score,
        task_metadata={"id": "TASK-EMPTY"}
    )

    display.render()

    captured = capsys.readouterr()

    # Assertions - should NOT contain "None" text
    assert "None" not in captured.out, "Should not display 'None' to user"

    # Should contain friendly messages
    assert "No implementation phases specified" in captured.out or "Not specified" in captured.out
    assert "Not specified" in captured.out or "Not set" in captured.out
```

---

## Part 2: Concurrency & State Management Requirements

### REQ-CS-001: Multiple Modifications (v1 → v2 → v3 → v4)

**EARS Notation** (Event-Driven):
```
When a user makes multiple modifications to a plan, the system shall create a sequential version history (v1 → v2 → v3 → v4) with change tracking
```

**Rationale**: Users may iteratively refine plans through multiple modification cycles. The system must track version history for auditability and rollback capability.

**Current Implementation Status**:
✅ **IMPLEMENTED**: `VersionManager` tracks unlimited version history (per edge case review document line 223)

**Acceptance Criteria**:
- [ ] Multiple modifications create sequential versions (v1, v2, v3, v4)
- [ ] Version history is preserved across modifications
- [ ] Each version has unique version number, timestamp, change reason
- [ ] Latest version is retrievable
- [ ] Version history is retrievable
- [ ] Version comparison works across multiple versions

**Test Scenarios**:
1. **test_multiple_modifications_v1_to_v4_creates_history** - Verify 4 versions created
2. **test_version_history_preserves_all_changes** - Verify history integrity
3. **test_version_numbers_are_sequential** - Verify v1, v2, v3, v4 numbering

**Technical Considerations**:
- Version persistence across modification sessions
- Memory usage with large version histories
- Version comparison performance

**Implementation Notes**:
```python
# Current implementation in version_manager.py
# Handles unlimited versions with proper sequencing
# ✅ Already tested in Phase 2 integration tests (test_modification_workflow.py)
```

**Validation Approach**:
```python
def test_multiple_modifications_v1_to_v4():
    """Test multiple plan modifications create correct version history."""
    plan = create_test_plan()
    version_manager = VersionManager("TASK-VERSIONS")

    # Create v1
    v1 = version_manager.create_version(plan, "Initial plan")
    assert v1.version_number == 1

    # Modify and create v2
    plan.files_to_create.append("new_file.py")
    v2 = version_manager.create_version(plan, "Added file")
    assert v2.version_number == 2

    # Modify and create v3
    plan.external_dependencies.append("new_lib")
    v3 = version_manager.create_version(plan, "Added dependency")
    assert v3.version_number == 3

    # Modify and create v4
    plan.phases = ["Phase 1", "Phase 2"]
    v4 = version_manager.create_version(plan, "Added phases")
    assert v4.version_number == 4

    # Verify history
    history = version_manager.get_version_history()
    assert len(history) == 4
    assert history[0].version_number == 1
    assert history[3].version_number == 4

    # Verify latest
    latest = version_manager.get_latest_version()
    assert latest.version_number == 4
    assert "Added phases" in latest.change_reason
```

---

### REQ-CS-002: Modification That Increases Complexity

**EARS Notation** (Event-Driven):
```
When a user modification increases the complexity score, the system shall display a warning message with old and new scores
```

**Rationale**: Users should be informed when their modifications make the task more complex, allowing them to reconsider simplification strategies.

**Current Implementation Status**:
❌ **NOT IMPLEMENTED**: No warning for complexity increases (per edge case review document line 224)

**Acceptance Criteria**:
- [ ] Modification that adds files increases complexity score
- [ ] System detects score increase (new_score > old_score)
- [ ] Warning message displayed with ⚠️ emoji
- [ ] Warning shows old score (e.g., "Old score: 5/10")
- [ ] Warning shows new score (e.g., "New score: 8/10")
- [ ] Warning suggests simplification consideration
- [ ] Workflow continues (warning is non-blocking)

**Test Scenarios**:
1. **test_modification_increases_complexity_shows_warning** - Verify warning displayed
2. **test_modification_increases_complexity_shows_scores** - Verify score display
3. **test_modification_decreases_complexity_no_warning** - No warning for improvements

**Technical Considerations**:
- Complexity recalculation after modifications
- Score comparison logic
- Warning message formatting

**Implementation Gap**:
```python
# In review_modes.py - FullReviewHandler._apply_modifications_and_return()
# Need to add complexity comparison and warning logic

def _apply_modifications_and_return(
    self,
    session: "ModificationSession"
) -> Optional[FullReviewResult]:
    try:
        # ... apply changes ...
        modified_plan = applier.apply()

        # Recalculate complexity
        new_complexity = calculator.calculate(context)
        old_score = self.complexity_score.total_score
        new_score = new_complexity.total_score

        # ❌ Missing: Complexity increase warning
        # ✅ Should add:
        if new_score > old_score:
            print(f"\n⚠️  Warning: Modifications increased complexity!")
            print(f"   Old score: {old_score}/10")
            print(f"   New score: {new_score}/10")
            print(f"   Consider simplifying further.\n")

        # ... create version ...
```

**Validation Approach**:
```python
def test_modification_that_increases_complexity_warns_user(mocker, capsys):
    """Test modification that increases complexity shows warning."""
    # Initial plan with score=5 (moderate)
    plan = ImplementationPlan(
        task_id="TASK-MODIFY",
        files_to_create=["file1.py", "file2.py"],  # 2 files
        patterns_used=["repository"],
        external_dependencies=[]
    )

    # Calculate initial complexity
    calculator = ComplexityCalculator()
    initial_context = EvaluationContext(
        task_id="TASK-MODIFY",
        technology_stack="python",
        implementation_plan=plan
    )
    initial_score = calculator.calculate(initial_context)
    assert initial_score.total_score == 5  # Moderate complexity

    # User adds 8 more files (increases complexity)
    session = ModificationSession(plan, "TASK-MODIFY", "user")
    session.start()
    for i in range(8):
        session.change_tracker.record_file_added(f"file{i+3}.py")

    # Apply modifications
    handler = FullReviewHandler(
        complexity_score=initial_score,
        plan=plan,
        task_metadata={"id": "TASK-MODIFY"},
        task_file_path=Path("/tmp/TASK-MODIFY.md")
    )

    result = handler._apply_modifications_and_return(session)

    captured = capsys.readouterr()

    # Assertions
    assert "⚠️" in captured.out, "Should show warning emoji"
    assert "Warning: Modifications increased complexity" in captured.out
    assert "Old score: 5/10" in captured.out
    assert "New score:" in captured.out  # Should be higher (8-10)
    assert "Consider simplifying" in captured.out or "simplify" in captured.out.lower()
```

---

### REQ-CS-003: Long Q&A Session (10+ Questions)

**EARS Notation** (Boundary Condition):
```
When a user asks more than 20 questions in a Q&A session, the system shall limit the session and return to the review checkpoint
```

**Rationale**: Unlimited Q&A sessions could consume excessive time, API credits, and memory. A reasonable limit (20 questions) prevents runaway sessions while allowing thorough exploration.

**Current Implementation Status**:
❌ **NOT IMPLEMENTED**: No question limit in Q&A sessions (per edge case review document line 226)

**Acceptance Criteria**:
- [ ] Q&A session accepts up to 20 questions
- [ ] Question 21 triggers limit warning
- [ ] Session automatically returns to review checkpoint after limit
- [ ] Warning message explains limit reached (⚠️ emoji)
- [ ] All answered questions are saved in Q&A history
- [ ] User can exit early with "back" command

**Test Scenarios**:
1. **test_long_qa_session_10_questions_accepted** - Verify 10 questions work
2. **test_qa_session_limit_20_questions_enforced** - Verify limit at 20
3. **test_qa_session_limit_warning_displayed** - Verify warning message

**Technical Considerations**:
- Q&A session state management
- Question counter implementation
- API cost control for AI responses
- Memory usage for Q&A history

**Implementation Gap**:
```python
# In qa_manager.py - QAManager.run_qa_session()
# Need to add question limit enforcement

def run_qa_session(self, max_questions: int = 20) -> Optional[QASession]:
    """Run interactive Q&A session with question limit."""
    session = QASession(...)

    question_count = 0  # ❌ Missing: Question counter
    while True:
        user_input = input("\nYour question (or 'back' to return): ").strip()

        if user_input.lower() == "back":
            break

        # ❌ Missing: Question limit enforcement
        question_count += 1
        if question_count > max_questions:
            print(f"\n⚠️  Maximum questions reached ({max_questions})")
            print("   Returning to review checkpoint...\n")
            break

        # ... handle question ...
```

**Validation Approach**:
```python
def test_long_qa_session_10_plus_questions_limited(mocker, capsys):
    """Test Q&A session with 10+ questions respects limit."""
    # Simulate user asking 25 questions
    questions = [f"Question {i}" for i in range(25)]
    questions.append("back")  # Try to exit

    user_inputs = iter(questions)
    mocker.patch('builtins.input', side_effect=lambda _: next(user_inputs))

    # Mock AI responses
    mocker.patch(
        'installer.global.commands.lib.agent_utils.invoke_qa_agent',
        return_value="Mocked answer"
    )

    qa_manager = QAManager(
        plan=create_test_plan(),
        task_id="TASK-QA",
        task_metadata={}
    )

    session = qa_manager.run_qa_session(max_questions=20)

    # Assertions
    assert session is not None
    assert len(session.qa_history) == 20, "Should stop at 20 questions"
    assert len(session.qa_history) < 25, "Should NOT process all 25"

    captured = capsys.readouterr()
    assert "⚠️" in captured.out or "Warning" in captured.out
    assert "Maximum questions reached" in captured.out or "20" in captured.out
```

**Performance Requirement**:
- Q&A session with 20 questions should complete in <60 seconds (3s per question average)

---

### REQ-CS-004: Timeout During File Write

**EARS Notation** (Unwanted Behavior):
```
If a file write operation times out after 1 second, then the system shall handle the timeout gracefully without hanging
```

**Rationale**: File write operations can hang on network filesystems or slow disks. A timeout ensures the system remains responsive.

**Current Implementation Status**:
⚠️ **PARTIALLY IMPLEMENTED**: Atomic write helps prevent corruption, but no explicit timeout handling (per edge case review document line 227)

**Acceptance Criteria**:
- [ ] File write operations complete in <1 second (normal case)
- [ ] File write operations don't hang indefinitely
- [ ] Timeout error is caught and logged
- [ ] System continues execution after timeout
- [ ] User is informed of write failure

**Test Scenarios**:
1. **test_file_write_timeout_handled_gracefully** - Verify timeout handling
2. **test_atomic_write_performance** - Verify <1s for normal writes
3. **test_timeout_does_not_hang_system** - Verify system remains responsive

**Technical Considerations**:
- OS-level file system timeouts are hard to test
- Atomic write implementation in `user_interaction.py`
- Signal-based timeout (POSIX) vs thread-based timeout (Windows)
- Network filesystem considerations

**Implementation Gap**:
```python
# In user_interaction.py - FileOperations.atomic_write()
# Current implementation uses os.replace() which can hang on network filesystems
# Could add signal-based timeout on POSIX systems

import signal

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("File write timeout")

@staticmethod
def atomic_write(file_path: Path, content: str, encoding: str = "utf-8") -> None:
    """Atomic file write with 1-second timeout (POSIX only)."""
    # ❌ Missing: Timeout protection
    # ✅ Could add (POSIX):
    if hasattr(signal, 'SIGALRM'):  # POSIX only
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(1)  # 1-second timeout

    try:
        # ... existing atomic write logic ...
        os.replace(tmp_path, str(file_path))

        if hasattr(signal, 'SIGALRM'):
            signal.alarm(0)  # Cancel alarm
    except TimeoutError:
        logger.error(f"File write timeout after 1 second: {file_path}")
        print(f"\n⚠️  Warning: File write timed out")
    finally:
        if hasattr(signal, 'SIGALRM'):
            signal.alarm(0)  # Ensure alarm is cancelled
```

**Validation Approach**:
```python
def test_timeout_during_file_write_handled_gracefully():
    """Test file write timeout is handled (if possible)."""
    # Note: This is hard to test as OS-level timeouts are rare
    # But we can test that atomic write doesn't hang

    import signal
    import pytest

    if not hasattr(signal, 'SIGALRM'):
        pytest.skip("Test requires POSIX signals (not available on Windows)")

    def timeout_handler(signum, frame):
        raise TimeoutError("File write timeout")

    # Set 1-second timeout
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(1)

    try:
        # Attempt write (should complete quickly)
        temp_file = Path("/tmp/test_timeout.txt")
        FileOperations.atomic_write(temp_file, "Test content")

        signal.alarm(0)  # Cancel alarm

        # Verify file was written
        assert temp_file.exists()
        assert temp_file.read_text() == "Test content"

    except TimeoutError:
        pytest.fail("File write took longer than 1 second")
    finally:
        signal.alarm(0)  # Ensure alarm is cancelled
```

**Performance Requirement**:
- Normal file write operations must complete in <100ms
- Timeout threshold: 1 second

---

## Part 3: Test Implementation Plan

### Test File Organization

```
tests/
├── edge_cases/
│   ├── __init__.py
│   ├── test_boundary_conditions.py       # NEW - REQ-BC-001 to REQ-BC-005 (5 edge cases)
│   └── test_concurrency_state.py         # NEW - REQ-CS-001 to REQ-CS-004 (4 edge cases)
```

### Test Coverage Matrix

| Edge Case | Requirement ID | Tests Planned | Implementation Status | Priority |
|-----------|----------------|---------------|----------------------|----------|
| 0 files | REQ-BC-001 | 3 tests | ✅ Implemented | Low (validation) |
| 50+ files | REQ-BC-002 | 3 tests | ✅ Implemented | Low (validation) |
| No dependencies | REQ-BC-003 | 3 tests | ⚠️ Partial (stub) | Medium |
| 10+ dependencies | REQ-BC-004 | 3 tests | ⚠️ Partial (stub) | Medium |
| Empty plan sections | REQ-BC-005 | 3 tests | ❌ Missing | **HIGH** |
| Multiple modifications | REQ-CS-001 | 3 tests | ✅ Implemented | Low (validation) |
| Complexity increase | REQ-CS-002 | 3 tests | ❌ Missing | **HIGH** |
| Long Q&A session | REQ-CS-003 | 3 tests | ❌ Missing | **HIGH** |
| File write timeout | REQ-CS-004 | 3 tests | ⚠️ Partial | Medium |

**Total Planned Tests**: 27 tests (3 per edge case × 9 edge cases)

### Implementation Priorities

#### Priority 1: HIGH - Missing Features (6 tests)
1. **REQ-BC-005**: Empty plan sections display (3 tests)
2. **REQ-CS-002**: Complexity increase warning (3 tests)

#### Priority 2: HIGH - Missing Features (3 tests)
3. **REQ-CS-003**: Q&A session limit (3 tests)

#### Priority 3: MEDIUM - Validation (12 tests)
4. **REQ-BC-001**: 0 files edge case validation (3 tests)
5. **REQ-BC-002**: 50+ files edge case validation (3 tests)
6. **REQ-BC-003**: No dependencies validation (3 tests)
7. **REQ-BC-004**: 10+ dependencies validation (3 tests)

#### Priority 4: MEDIUM - Enhancement (3 tests)
8. **REQ-CS-004**: File write timeout handling (3 tests)

#### Priority 5: LOW - Already Tested (3 tests)
9. **REQ-CS-001**: Multiple modifications validation (3 tests - may already exist in Phase 2)

---

## Part 4: Gap Analysis & Clarifications Needed

### Implementation Gaps Identified

#### Gap 1: Empty Plan Sections Display (REQ-BC-005)
**Status**: ❌ NOT IMPLEMENTED
**Impact**: HIGH - User-facing display issue
**Effort**: 2 hours
**Files to Modify**:
- `installer/global/commands/lib/review_modes.py` (FullReviewDisplay class)
- `installer/global/commands/lib/pager_display.py` (PagerDisplay class)

**Clarifications Needed**:
1. Which plan fields need None-to-friendly-message conversion?
   - `phases` (list) → "No implementation phases specified"
   - `estimated_loc` (int) → "Not specified"
   - `estimated_duration` (str) → "Not specified"
   - `test_summary` (str) → "Not specified"
   - `risk_details` (list) → "No risks identified"
2. Should we apply this to all display modes (quick, full, pager)?
3. What about empty lists vs None values?

---

#### Gap 2: Complexity Increase Warning (REQ-CS-002)
**Status**: ❌ NOT IMPLEMENTED
**Impact**: HIGH - User experience issue
**Effort**: 3 hours
**Files to Modify**:
- `installer/global/commands/lib/review_modes.py` (FullReviewHandler._apply_modifications_and_return)

**Clarifications Needed**:
1. At what threshold should we warn? (Any increase? +2 or more?)
2. Should we block modification if increase is significant? (e.g., +3 or more)
3. What if modifications reduce complexity? Should we show positive feedback?
4. Should we log complexity changes to metrics?

---

#### Gap 3: Q&A Session Limit (REQ-CS-003)
**Status**: ❌ NOT IMPLEMENTED
**Impact**: HIGH - Resource control issue
**Effort**: 2 hours
**Files to Modify**:
- `installer/global/commands/lib/qa_manager.py` (QAManager.run_qa_session)

**Clarifications Needed**:
1. What is the appropriate question limit? (Recommended: 20)
2. Should limit be configurable? (via settings.json)
3. Should we warn at 15 questions before hitting limit at 20?
4. Should we track API costs and limit based on cost instead?

---

#### Gap 4: Dependency Complexity Factor (REQ-BC-003, REQ-BC-004)
**Status**: ⚠️ PARTIAL - Documented as "future implementation"
**Impact**: MEDIUM - Feature incompleteness
**Effort**: 4 hours
**Files to Modify**:
- `installer/global/commands/lib/complexity_factors.py` (new DependencyComplexityFactor class)
- `installer/global/commands/lib/complexity_calculator.py` (register new factor)

**Clarifications Needed**:
1. Should we implement dependency complexity factor as part of this task?
2. If yes, what scoring algorithm should we use?
   - Option 1: Linear (1 dep = +0.5, 2 deps = +1, 4 deps = +2, max +3)
   - Option 2: Tiered (0 deps = 0, 1-2 = +1, 3-5 = +2, 6+ = +3)
3. Or should we defer to a separate task (TASK-003F)?

---

#### Gap 5: File Write Timeout (REQ-CS-004)
**Status**: ⚠️ PARTIAL - Atomic write exists, no timeout
**Impact**: LOW - Rare edge case
**Effort**: 3 hours
**Files to Modify**:
- `installer/global/commands/lib/user_interaction.py` (FileOperations.atomic_write)

**Clarifications Needed**:
1. Is timeout handling necessary for this phase? (Nice-to-have vs must-have)
2. Platform support: POSIX only (signal.SIGALRM) or Windows too (threading)?
3. What timeout threshold? (Recommended: 1 second)
4. Should we retry on timeout? (Recommended: No, just log and continue)

---

### Ambiguities to Resolve

#### Ambiguity 1: Dependency Factor Implementation Scope
**Question**: Should REQ-BC-003 and REQ-BC-004 implement the dependency complexity factor, or just validate that empty/large dependency lists don't crash?

**Options**:
- **Option A**: Validation only - Test that empty/large lists work with current stub implementation (Low effort: 2 hours)
- **Option B**: Full implementation - Implement dependency complexity factor with scoring algorithm (High effort: 6 hours)

**Recommendation**: Option A for this task (Phase 5 Day 3 focuses on edge cases, not new features)

---

#### Ambiguity 2: File Write Timeout Platform Support
**Question**: Should file write timeout be implemented for all platforms or just POSIX?

**Options**:
- **Option A**: POSIX only (signal-based) - Works on macOS/Linux (Medium effort: 3 hours)
- **Option B**: Cross-platform (threading-based) - Works on Windows too (High effort: 5 hours)
- **Option C**: No timeout, rely on OS defaults (Low effort: 0 hours)

**Recommendation**: Option C for this task (OS-level timeouts are rare, atomic write provides corruption protection)

---

#### Ambiguity 3: Empty Plan Sections - List vs None Handling
**Question**: How should we handle empty lists ([]) vs None values?

**Examples**:
- `phases = None` → "No implementation phases specified"
- `phases = []` → "No implementation phases specified" (same message?)
- `risk_details = None` → "No risks identified"
- `risk_details = []` → "No risks identified" (same message?)

**Recommendation**: Treat `None` and empty list `[]` the same for user-facing displays (both are "missing data")

---

## Part 5: Non-Functional Requirements

### Performance Requirements

| Requirement | Target | Measurement |
|-------------|--------|-------------|
| Complexity calculation (0 files) | <100ms | Timer in test |
| Complexity calculation (50+ files) | <1s | Timer in test |
| Complexity calculation (15 dependencies) | <1s | Timer in test |
| File write operation | <100ms | Timer in test |
| Q&A session (20 questions) | <60s | 3s per question avg |

### Usability Requirements

| Requirement | Description |
|-------------|-------------|
| Error messages | User-friendly, actionable, with emoji (⚠️ ❌) |
| Empty data display | "Not specified" instead of "None" |
| Warning messages | Clear, concise, non-blocking |
| Question limits | Communicated before enforcement |

### Reliability Requirements

| Requirement | Description |
|-------------|-------------|
| No crashes on edge cases | All boundary conditions handled gracefully |
| Deterministic scoring | Same input always produces same output |
| Data integrity | Version history preserved across modifications |
| Graceful degradation | System continues on non-critical failures |

---

## Part 6: Test Implementation Checklist

### Phase 5 Day 3 Implementation Checklist

#### Step 1: Implement Missing Features (Priority 1 - HIGH)
- [ ] **Empty Plan Sections Display** (REQ-BC-005) - 2 hours
  - [ ] Modify `FullReviewDisplay._display_implementation_order()`
  - [ ] Modify `FullReviewDisplay._display_testing_approach()`
  - [ ] Modify `PagerDisplay.format_section()` for None handling
  - [ ] Add tests: `test_empty_plan_sections_display_not_specified`

- [ ] **Complexity Increase Warning** (REQ-CS-002) - 3 hours
  - [ ] Modify `FullReviewHandler._apply_modifications_and_return()`
  - [ ] Add score comparison logic (old vs new)
  - [ ] Add warning message formatting
  - [ ] Add tests: `test_modification_increases_complexity_warns_user`

#### Step 2: Implement Missing Features (Priority 2 - HIGH)
- [ ] **Q&A Session Limit** (REQ-CS-003) - 2 hours
  - [ ] Modify `QAManager.run_qa_session()` to add `max_questions` parameter
  - [ ] Add question counter and limit enforcement
  - [ ] Add warning message at limit
  - [ ] Add tests: `test_long_qa_session_10_plus_questions_limited`

#### Step 3: Validation Tests (Priority 3 - MEDIUM)
- [ ] **0 Files Edge Case** (REQ-BC-001) - 1 hour
  - [ ] Test: `test_task_with_zero_files_minimum_score`
  - [ ] Test: `test_task_with_zero_files_does_not_crash`
  - [ ] Test: `test_task_with_zero_files_deterministic`

- [ ] **50+ Files Edge Case** (REQ-BC-002) - 1 hour
  - [ ] Test: `test_task_with_50_plus_files_very_complex`
  - [ ] Test: `test_task_with_100_files_still_capped`
  - [ ] Test: `test_task_with_50_files_forces_full_review`

- [ ] **No Dependencies Edge Case** (REQ-BC-003) - 1 hour
  - [ ] Test: `test_task_with_no_dependencies_handles_gracefully`
  - [ ] Test: `test_task_with_no_dependencies_zero_penalty`
  - [ ] Test: `test_task_with_no_dependencies_valid_score`

- [ ] **10+ Dependencies Edge Case** (REQ-BC-004) - 1 hour
  - [ ] Test: `test_task_with_10_plus_dependencies_handles_gracefully`
  - [ ] Test: `test_task_with_15_dependencies_valid_score`
  - [ ] Test: `test_task_with_20_dependencies_performance`

#### Step 4: Enhancement Tests (Priority 4 - MEDIUM)
- [ ] **File Write Timeout** (REQ-CS-004) - 1 hour
  - [ ] Test: `test_file_write_timeout_handled_gracefully` (POSIX only)
  - [ ] Test: `test_atomic_write_performance` (<100ms)
  - [ ] Test: `test_timeout_does_not_hang_system`

#### Step 5: Already Implemented Validation (Priority 5 - LOW)
- [ ] **Multiple Modifications** (REQ-CS-001) - 0.5 hours
  - [ ] Verify existing tests in `test_modification_workflow.py` cover this
  - [ ] Add missing edge case tests if needed

### Estimated Time Breakdown

| Priority | Description | Tests | Implementation | Total |
|----------|-------------|-------|----------------|-------|
| P1 (HIGH) | Empty sections + Complexity warning | 6 tests | 5 hours | 5 hours |
| P2 (HIGH) | Q&A session limit | 3 tests | 2 hours | 2 hours |
| P3 (MEDIUM) | Validation tests | 12 tests | 4 hours | 4 hours |
| P4 (MEDIUM) | File timeout enhancement | 3 tests | 1 hour | 1 hour |
| P5 (LOW) | Existing validation | 3 tests | 0.5 hours | 0.5 hours |
| **TOTAL** | | **27 tests** | **12.5 hours** | **12.5 hours** |

**Estimated Delivery**: 1.5 days (assuming 8-hour work days)

---

## Part 7: Success Criteria

### Acceptance Criteria Summary

**Phase 5 Day 3 is complete when**:
- [ ] All 9 edge cases have test coverage (27 tests total)
- [ ] All HIGH priority implementations complete (empty sections, complexity warning, Q&A limit)
- [ ] All tests pass (100% pass rate)
- [ ] No regressions in existing tests
- [ ] Code review score ≥ 85/100
- [ ] Test coverage ≥ 90% on modified modules

### Quality Gates

| Gate | Threshold | Measurement |
|------|-----------|-------------|
| Test Pass Rate | 100% | pytest output |
| Code Coverage | ≥90% | pytest-cov |
| Performance | All edge cases <1s | Timer assertions |
| Code Review | ≥85/100 | Manual review |
| Architectural Review | No regressions | Compare to 82/100 baseline |

---

## Part 8: Risk Assessment

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Dependency factor scope creep | Medium | High | Clarify: validation only, not full implementation |
| File timeout cross-platform issues | Low | Medium | Implement POSIX only or skip timeout handling |
| Q&A limit breaks existing workflows | Low | High | Make limit configurable (default 20) |
| Empty section handling breaks pager | Low | Medium | Test all display modes thoroughly |

### Schedule Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Implementation takes >1.5 days | Medium | Medium | Prioritize HIGH items, defer MEDIUM if needed |
| Edge case tests reveal new bugs | Medium | High | Allocate 0.5 days for bug fixing |
| Clarifications delay start | High | Low | Proceed with validation tests while awaiting clarifications |

---

## Part 9: Recommendations

### Immediate Actions (Day 3 Start)

1. **Clarify Scope** (30 minutes)
   - Confirm: REQ-BC-003/004 are validation only (not full dependency factor implementation)
   - Confirm: REQ-CS-004 file timeout is optional (defer if time-constrained)
   - Confirm: Q&A limit default value (recommend 20)

2. **Implement HIGH Priority Features** (7 hours)
   - REQ-BC-005: Empty plan sections display (2 hours)
   - REQ-CS-002: Complexity increase warning (3 hours)
   - REQ-CS-003: Q&A session limit (2 hours)

3. **Write Validation Tests** (4 hours)
   - REQ-BC-001 to REQ-BC-004: Boundary condition validation (4 hours)

4. **Optional Enhancements** (1 hour)
   - REQ-CS-004: File write timeout (if time permits)

### Deferred to Future Tasks

1. **Dependency Complexity Factor Implementation**
   - Full scoring algorithm implementation
   - Recommended as separate task (TASK-003F)
   - Estimated effort: 6 hours

2. **Cross-Platform File Timeout**
   - Windows-compatible timeout implementation
   - Low priority (rare edge case)
   - Estimated effort: 5 hours

---

## Conclusion

This requirements analysis provides a comprehensive breakdown of TASK-003E Phase 5 Day 3 boundary and state edge cases. The analysis identifies:

- **9 edge cases** requiring testing (5 boundary, 4 concurrency/state)
- **27 planned tests** (3 per edge case)
- **3 HIGH priority implementations** (empty sections, complexity warning, Q&A limit)
- **5 clarifications needed** (dependency factor scope, timeout platform support, empty data handling)

**Estimated Effort**: 1.5 days (12.5 hours)
**Risk Level**: LOW (clear requirements, well-defined scope)
**Readiness**: READY TO IMPLEMENT (pending clarifications on dependency factor scope)

---

**Document Version**: 1.0
**Author**: Requirements Engineering Specialist
**Review Status**: Ready for Implementation
**Next Steps**: Clarify scope questions, begin HIGH priority implementations
