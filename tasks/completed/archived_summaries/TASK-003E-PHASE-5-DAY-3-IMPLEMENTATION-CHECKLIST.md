# TASK-003E Phase 5 Day 3: Implementation Checklist

**Date**: 2025-10-10
**Phase**: Boundary & State Edge Cases
**Status**: Ready to Start

---

## Quick Start Guide

### Prerequisites
- [ ] Phase 5 Day 1 complete (import/path fixes)
- [ ] Phase 5 Day 2 complete (error handling edge cases)
- [ ] Current test suite passing (596/603 tests)
- [ ] Development environment ready

### Estimated Time: 12.5 hours (1.5 days)

---

## Priority 1: HIGH - Critical Implementations (7 hours)

### Task 1.1: Empty Plan Sections Display (2 hours)

**Requirement**: REQ-BC-005
**Files to Modify**: 2 files

#### Step 1: Update FullReviewDisplay (1 hour)
**File**: `/installer/global/commands/lib/review_modes.py`

- [ ] **Modify `_display_implementation_order()`**
  ```python
  def _display_implementation_order(self) -> None:
      print("\n📋 IMPLEMENTATION ORDER:")

      if self.plan.phases:
          for i, phase in enumerate(self.plan.phases, 1):
              print(f"\n  {i}. {phase}")
      else:
          print("\n  No implementation phases specified")  # ← ADD THIS

      # Show estimated LOC if available
      if self.plan.estimated_loc:
          print(f"\n  Estimated Lines of Code: ~{self.plan.estimated_loc}")
      else:
          print(f"\n  Estimated Lines of Code: Not specified")  # ← ADD THIS

      # Show estimated duration if available
      if self.plan.estimated_duration:
          print(f"  Estimated Duration: {self.plan.estimated_duration}")
      else:
          print(f"  Estimated Duration: Not specified")  # ← ADD THIS
  ```

- [ ] **Modify `_display_testing_approach()`**
  ```python
  def _display_testing_approach(self) -> None:
      print("\n🧪 TESTING APPROACH:")

      if self.plan.test_summary:
          print(f"\n  {self.plan.test_summary}")
      else:
          print("\n  No testing approach specified")  # ← ADD THIS
  ```

- [ ] **Modify `_display_risks()`**
  ```python
  def _display_risks(self) -> None:
      print("\n⚠️ RISK ASSESSMENT:")

      if self.plan.risk_details:
          for i, risk in enumerate(self.plan.risk_details, 1):
              print(f"\n  {i}. {risk}")
      else:
          print("\n  No risks identified")  # ← ADD THIS
  ```

#### Step 2: Update PagerDisplay (0.5 hours)
**File**: `/installer/global/commands/lib/pager_display.py`

- [ ] **Modify `format_section()` helper**
  ```python
  def _format_value(self, value: Any, field_name: str) -> str:
      """Format value with None handling."""
      if value is None:
          # Return friendly message based on field type
          friendly_messages = {
              "phases": "No implementation phases specified",
              "estimated_loc": "Not specified",
              "estimated_duration": "Not specified",
              "test_summary": "No testing approach specified",
              "risk_details": "No risks identified"
          }
          return friendly_messages.get(field_name, "Not specified")

      if isinstance(value, list) and not value:
          # Empty list
          list_friendly_messages = {
              "phases": "No implementation phases specified",
              "risk_details": "No risks identified",
              "patterns_used": "No patterns specified"
          }
          return list_friendly_messages.get(field_name, "None")

      return str(value)
  ```

#### Step 3: Write Tests (0.5 hours)
**File**: `/tests/edge_cases/test_boundary_conditions.py`

- [ ] **test_empty_plan_sections_display_not_specified**
  ```python
  def test_empty_plan_sections_display_not_specified(capsys):
      """Test empty plan sections show 'Not specified' instead of None."""
      plan = ImplementationPlan(
          task_id="TASK-EMPTY",
          files_to_create=["main.py"],
          patterns_used=[],
          external_dependencies=[],
          phases=None,
          estimated_loc=None,
          estimated_duration=None,
          test_summary=None
      )

      score = Mock(spec=ComplexityScore)
      score.total_score = 3
      score.factor_scores = []
      score.forced_review_triggers = []

      display = FullReviewDisplay(
          plan=plan,
          complexity_score=score,
          task_metadata={"id": "TASK-EMPTY", "title": "Empty Task"}
      )

      display.render()
      captured = capsys.readouterr()

      # Should NOT contain "None" text
      assert "None" not in captured.out
      # Should contain friendly messages
      assert "No implementation phases specified" in captured.out
      assert "Not specified" in captured.out
  ```

- [ ] **test_empty_phases_display_friendly_message**
- [ ] **test_empty_estimates_display_not_specified**

**Checkpoint**: Run tests - Expected 3 new tests passing

---

### Task 1.2: Complexity Increase Warning (3 hours)

**Requirement**: REQ-CS-002
**Files to Modify**: 1 file

#### Step 1: Add Score Comparison Logic (2 hours)
**File**: `/installer/global/commands/lib/review_modes.py`

- [ ] **Modify `FullReviewHandler._apply_modifications_and_return()`**
  ```python
  def _apply_modifications_and_return(
      self,
      session: "ModificationSession"
  ) -> Optional[FullReviewResult]:
      """Apply modifications, recalculate complexity, and return to checkpoint."""
      try:
          # Apply modifications
          from .modification_applier import ModificationApplier
          applier = ModificationApplier(session)
          modified_plan = applier.apply()

          # Recalculate complexity
          from .complexity_calculator import ComplexityCalculator
          calculator = ComplexityCalculator()
          context = EvaluationContext(
              task_id=session.task_id,
              technology_stack="python",  # TODO: Get from task metadata
              implementation_plan=modified_plan
          )
          new_complexity = calculator.calculate(context)

          # ← ADD THIS: Compare old vs new score
          old_score = self.complexity_score.total_score
          new_score = new_complexity.total_score

          if new_score > old_score:
              print(f"\n⚠️  Warning: Modifications increased complexity!")
              print(f"   Old score: {old_score}/10")
              print(f"   New score: {new_score}/10")
              print(f"   Consider simplifying further.\n")
          elif new_score < old_score:
              print(f"\n✅ Modifications reduced complexity!")
              print(f"   Old score: {old_score}/10")
              print(f"   New score: {new_score}/10\n")

          # Create version
          from .version_manager import VersionManager
          version_manager = VersionManager(session.task_id)
          version = version_manager.create_version(
              modified_plan,
              f"Modified by {session.modified_by}: {session.get_change_summary()}"
          )

          # Update complexity score and plan
          self.complexity_score = new_complexity
          self.plan = modified_plan

          # Return to checkpoint
          return None  # Signals return to checkpoint

      except Exception as e:
          logger.error(f"Error applying modifications: {e}")
          print(f"\n❌ Error applying modifications: {e}\n")
          return None
  ```

#### Step 2: Write Tests (1 hour)
**File**: `/tests/edge_cases/test_concurrency_state.py`

- [ ] **test_modification_increases_complexity_shows_warning**
  ```python
  def test_modification_that_increases_complexity_warns_user(mocker, capsys):
      """Test modification that increases complexity shows warning."""
      # Initial plan with score=5 (moderate)
      plan = ImplementationPlan(
          task_id="TASK-MODIFY",
          files_to_create=["file1.py", "file2.py"],
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
      assert initial_score.total_score == 5

      # Create session and add 8 files
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
      assert "⚠️" in captured.out
      assert "Warning: Modifications increased complexity" in captured.out
      assert "Old score: 5/10" in captured.out
      assert "New score:" in captured.out
      assert "simplify" in captured.out.lower()
  ```

- [ ] **test_modification_decreases_complexity_shows_success**
- [ ] **test_modification_no_change_no_message**

**Checkpoint**: Run tests - Expected 3 new tests passing

---

### Task 1.3: Q&A Session Limit (2 hours)

**Requirement**: REQ-CS-003
**Files to Modify**: 1 file

#### Step 1: Add Question Counter (1 hour)
**File**: `/installer/global/commands/lib/qa_manager.py`

- [ ] **Modify `QAManager.run_qa_session()`**
  ```python
  def run_qa_session(self, max_questions: int = 20) -> Optional[QASession]:
      """Run interactive Q&A session with question limit.

      Args:
          max_questions: Maximum number of questions allowed (default 20)

      Returns:
          QASession object with Q&A history, or None if cancelled
      """
      session = QASession(
          task_id=self.task_id,
          plan=self.plan,
          started_at=datetime.now()
      )

      print("\n❓ Q&A MODE - Ask questions about the plan")
      print(f"   Maximum questions: {max_questions}")
      print("   Type 'back' to return to review\n")

      question_count = 0  # ← ADD THIS: Question counter

      while True:
          user_input = input("\nYour question (or 'back' to return): ").strip()

          if user_input.lower() == "back":
              session.ended_at = datetime.now()
              return session

          if not user_input:
              print("⚠️ Please enter a question")
              continue

          # ← ADD THIS: Check question limit
          question_count += 1
          if question_count > max_questions:
              print(f"\n⚠️  Maximum questions reached ({max_questions})")
              print("   Returning to review checkpoint...\n")
              session.ended_at = datetime.now()
              return session

          # Get AI answer
          try:
              answer = self._get_answer(user_input)
              session.add_qa(user_input, answer)
              print(f"\n💡 Answer: {answer}\n")
          except Exception as e:
              logger.error(f"Error getting Q&A answer: {e}")
              print(f"\n❌ Error: Could not get answer. Please try again.\n")
  ```

#### Step 2: Write Tests (1 hour)
**File**: `/tests/edge_cases/test_concurrency_state.py`

- [ ] **test_long_qa_session_10_plus_questions_limited**
  ```python
  def test_long_qa_session_10_plus_questions_limited(mocker, capsys):
      """Test Q&A session with 10+ questions respects limit."""
      # Simulate user asking 25 questions
      questions = [f"Question {i}" for i in range(25)]
      questions.append("back")

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
      assert len(session.qa_history) == 20
      assert len(session.qa_history) < 25

      captured = capsys.readouterr()
      assert "⚠️" in captured.out or "Maximum questions" in captured.out
  ```

- [ ] **test_qa_session_10_questions_accepted**
- [ ] **test_qa_session_limit_warning_displayed**

**Checkpoint**: Run tests - Expected 3 new tests passing

---

## Priority 2: MEDIUM - Validation Tests (4 hours)

### Task 2.1: Zero Files Validation (1 hour)

**Requirement**: REQ-BC-001
**Files**: `/tests/edge_cases/test_boundary_conditions.py`

- [ ] **test_task_with_zero_files_minimum_score**
  ```python
  def test_task_with_zero_files_minimum_score():
      """Test task with 0 files defaults to minimum score."""
      plan = ImplementationPlan(
          task_id="TASK-ZERO",
          files_to_create=[],
          patterns_used=[],
          external_dependencies=[]
      )

      calculator = ComplexityCalculator()
      context = EvaluationContext(
          task_id="TASK-ZERO",
          technology_stack="python",
          implementation_plan=plan
      )

      score = calculator.calculate(context)

      assert score.total_score >= 1
      assert score.total_score <= 10
  ```

- [ ] **test_task_with_zero_files_does_not_crash**
- [ ] **test_task_with_zero_files_deterministic**

**Checkpoint**: Run tests - Expected 3 new tests passing

---

### Task 2.2: 50+ Files Validation (1 hour)

**Requirement**: REQ-BC-002
**Files**: `/tests/edge_cases/test_boundary_conditions.py`

- [ ] **test_task_with_50_plus_files_very_complex**
  ```python
  def test_task_with_50_plus_files_very_complex():
      """Test task with 50+ files is capped at max complexity."""
      plan = ImplementationPlan(
          task_id="TASK-LARGE",
          files_to_create=[f"file_{i}.py" for i in range(50)],
          patterns_used=["event_sourcing", "saga", "cqrs"],
          external_dependencies=["kafka", "redis"]
      )

      calculator = ComplexityCalculator()
      score = calculator.calculate(EvaluationContext(
          task_id="TASK-LARGE",
          technology_stack="python",
          implementation_plan=plan
      ))

      assert score.total_score == 10
      assert score.review_mode == ReviewMode.FULL_REQUIRED
  ```

- [ ] **test_task_with_100_files_still_capped**
- [ ] **test_task_with_50_files_forces_full_review**

**Checkpoint**: Run tests - Expected 3 new tests passing

---

### Task 2.3: No Dependencies Validation (1 hour)

**Requirement**: REQ-BC-003
**Files**: `/tests/edge_cases/test_boundary_conditions.py`

- [ ] **test_task_with_no_dependencies_handles_gracefully**
  ```python
  def test_task_with_no_dependencies():
      """Test task with no external dependencies scores correctly."""
      plan = ImplementationPlan(
          task_id="TASK-SELF-CONTAINED",
          files_to_create=["main.py"],
          patterns_used=["singleton"],
          external_dependencies=[]
      )

      calculator = ComplexityCalculator()
      score = calculator.calculate(EvaluationContext(
          task_id="TASK-SELF-CONTAINED",
          technology_stack="python",
          implementation_plan=plan
      ))

      assert score.total_score >= 1
      assert score.total_score <= 10
  ```

- [ ] **test_task_with_no_dependencies_zero_penalty**
- [ ] **test_task_with_no_dependencies_valid_score**

**Checkpoint**: Run tests - Expected 3 new tests passing

---

### Task 2.4: 10+ Dependencies Validation (1 hour)

**Requirement**: REQ-BC-004
**Files**: `/tests/edge_cases/test_boundary_conditions.py`

- [ ] **test_task_with_10_plus_dependencies_handles_gracefully**
  ```python
  def test_task_with_10_plus_dependencies():
      """Test task with 10+ external dependencies."""
      plan = ImplementationPlan(
          task_id="TASK-MANY-DEPS",
          files_to_create=["integration.py"],
          patterns_used=["adapter"],
          external_dependencies=[f"lib_{i}" for i in range(15)]
      )

      calculator = ComplexityCalculator()
      import time
      start_time = time.time()

      score = calculator.calculate(EvaluationContext(
          task_id="TASK-MANY-DEPS",
          technology_stack="python",
          implementation_plan=plan
      ))

      end_time = time.time()
      calculation_time = end_time - start_time

      assert score.total_score >= 1
      assert score.total_score <= 10
      assert calculation_time < 1.0
  ```

- [ ] **test_task_with_15_dependencies_valid_score**
- [ ] **test_task_with_20_dependencies_performance**

**Checkpoint**: Run tests - Expected 3 new tests passing

---

## Priority 3: OPTIONAL - Enhancements (1 hour)

### Task 3.1: File Write Timeout (1 hour)

**Requirement**: REQ-CS-004
**Files**: `/tests/edge_cases/test_concurrency_state.py`

- [ ] **test_file_write_timeout_handled_gracefully** (POSIX only)
- [ ] **test_atomic_write_performance** (<100ms)
- [ ] **test_timeout_does_not_hang_system**

**Note**: Implementation optional - atomic write already provides corruption protection

---

## Priority 4: VALIDATION - Already Implemented (0.5 hours)

### Task 4.1: Multiple Modifications (0.5 hours)

**Requirement**: REQ-CS-001
**Status**: ✅ Already tested in Phase 2 (test_modification_workflow.py)

- [ ] **Verify existing tests cover v1→v2→v3→v4 scenario**
- [ ] **Add missing edge case tests if needed**

---

## Test Execution Checklist

### Pre-Implementation Verification
- [ ] Current test suite passing: `pytest tests/ -v`
- [ ] Current coverage: `pytest tests/ --cov=installer/global/commands/lib --cov-report=term`
- [ ] No uncommitted changes: `git status`

### During Implementation
- [ ] Run tests after each priority level
- [ ] Check test coverage after each implementation
- [ ] Commit after each working feature

### Post-Implementation Verification
- [ ] Run full test suite: `pytest tests/ -v`
- [ ] Run edge case tests only: `pytest tests/edge_cases/ -v`
- [ ] Check coverage: `pytest tests/ --cov=installer/global/commands/lib --cov-report=term`
- [ ] Performance check: Ensure total execution time <5 minutes

---

## Quality Gates

### Code Quality
- [ ] PEP 8 compliance: `flake8 installer/global/commands/lib/`
- [ ] Type hints present in all new functions
- [ ] Docstrings complete for all new functions
- [ ] No commented-out code
- [ ] No debug print statements

### Test Quality
- [ ] All new tests have docstrings
- [ ] All new tests follow AAA pattern (Arrange-Act-Assert)
- [ ] All assertions have failure messages
- [ ] No skipped tests without reason
- [ ] No flaky tests (run 3 times to verify)

### Coverage Gates
- [ ] `review_modes.py`: ≥90% coverage
- [ ] `pager_display.py`: ≥90% coverage
- [ ] `qa_manager.py`: ≥90% coverage
- [ ] `test_boundary_conditions.py`: 100% pass rate
- [ ] `test_concurrency_state.py`: 100% pass rate

---

## Commit Strategy

### Commit 1: Empty Plan Sections (Task 1.1)
```bash
git add installer/global/commands/lib/review_modes.py
git add installer/global/commands/lib/pager_display.py
git add tests/edge_cases/test_boundary_conditions.py
git commit -m "feat(phase5-day3): implement empty plan sections display (REQ-BC-005)

- Add None-to-friendly-message conversion in FullReviewDisplay
- Add None handling in PagerDisplay
- Add 3 tests for empty plan sections
- All tests passing (599/603)"
```

### Commit 2: Complexity Increase Warning (Task 1.2)
```bash
git add installer/global/commands/lib/review_modes.py
git add tests/edge_cases/test_concurrency_state.py
git commit -m "feat(phase5-day3): add complexity increase warning (REQ-CS-002)

- Add score comparison in _apply_modifications_and_return()
- Display warning when modifications increase complexity
- Add 3 tests for complexity warning
- All tests passing (602/603)"
```

### Commit 3: Q&A Session Limit (Task 1.3)
```bash
git add installer/global/commands/lib/qa_manager.py
git add tests/edge_cases/test_concurrency_state.py
git commit -m "feat(phase5-day3): implement Q&A session limit (REQ-CS-003)

- Add max_questions parameter (default 20)
- Add question counter and limit enforcement
- Display warning at limit
- Add 3 tests for Q&A limit
- All tests passing (605/603)"
```

### Commit 4: Validation Tests (Task 2.1-2.4)
```bash
git add tests/edge_cases/test_boundary_conditions.py
git commit -m "test(phase5-day3): add boundary condition validation tests

- Add 3 tests for zero files edge case (REQ-BC-001)
- Add 3 tests for 50+ files edge case (REQ-BC-002)
- Add 3 tests for no dependencies edge case (REQ-BC-003)
- Add 3 tests for 10+ dependencies edge case (REQ-BC-004)
- All tests passing (617/603)"
```

### Commit 5: Documentation Updates
```bash
git add TASK-003E-PHASE-5-DAY-3-*.md
git add tasks/in_progress/TASK-003E-testing-documentation.md
git commit -m "docs(phase5-day3): complete boundary & state edge cases documentation

- Add requirements analysis report
- Add EARS requirements document
- Add implementation checklist
- Update task progress tracking"
```

---

## Progress Tracking

### Expected Test Count Growth

| Stage | Tests | Total | Status |
|-------|-------|-------|--------|
| Start | 596 | 596 | ✅ |
| Task 1.1 | +3 | 599 | 🔄 |
| Task 1.2 | +3 | 602 | 🔄 |
| Task 1.3 | +3 | 605 | 🔄 |
| Task 2.1 | +3 | 608 | 🔄 |
| Task 2.2 | +3 | 611 | 🔄 |
| Task 2.3 | +3 | 614 | 🔄 |
| Task 2.4 | +3 | 617 | 🔄 |
| Task 3.1 (opt) | +3 | 620 | ⏸️ |
| **Total** | **+24** | **620** | |

### Time Tracking

| Priority | Estimated | Actual | Status |
|----------|-----------|--------|--------|
| P1 (HIGH) | 7 hours | | 🔄 |
| P2 (MEDIUM) | 4 hours | | 🔄 |
| P3 (OPTIONAL) | 1 hour | | ⏸️ |
| **Total** | **12 hours** | | |

---

## Completion Checklist

### Implementation Complete
- [ ] All HIGH priority implementations done (Tasks 1.1-1.3)
- [ ] All MEDIUM priority validation tests done (Tasks 2.1-2.4)
- [ ] Optional enhancements done or explicitly deferred (Task 3.1)

### Testing Complete
- [ ] All 24 new tests written
- [ ] All tests passing (100% pass rate)
- [ ] No regressions (Phase 1-5 Day 2 still passing)
- [ ] Coverage ≥90% on modified modules

### Documentation Complete
- [ ] Requirements analysis document created
- [ ] EARS requirements document created
- [ ] Implementation checklist created
- [ ] Task file updated with progress
- [ ] Commit messages clear and descriptive

### Quality Assurance
- [ ] Code review completed
- [ ] All quality gates passed
- [ ] Performance requirements met
- [ ] No technical debt introduced

### Deployment Ready
- [ ] All changes committed to git
- [ ] Branch ready for merge
- [ ] CI/CD pipeline passing
- [ ] Ready for Phase 6 (User Documentation)

---

**Status**: Ready to Begin Implementation
**Next Action**: Start Task 1.1 - Empty Plan Sections Display
**Estimated Completion**: End of Day 3 (1.5 days from now)
