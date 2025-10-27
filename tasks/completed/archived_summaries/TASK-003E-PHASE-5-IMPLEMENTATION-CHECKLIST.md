# TASK-003E Phase 5 Implementation Checklist

**Status**: NOT STARTED
**Estimated Effort**: 5 days
**Priority**: HIGH (7 tests failing, 7 edge cases missing)

---

## Overview

This checklist tracks the implementation of all Phase 5 edge case acceptance criteria and test failure fixes for TASK-003E.

**Reference Documents**:
- Edge Case Review: `/TASK-003E-PHASE-5-EDGE-CASE-REVIEW.md`
- Task Definition: `/tasks/in_progress/TASK-003E-testing-documentation.md`
- Phase 5 Criteria: Lines 333-380 of task definition

---

## Priority 1: Fix Test Failures (Day 1)

### Path Resolver Tests (9 failures) - HIGH PRIORITY

- [ ] **Fix macOS symlink resolution** (`/private/var` vs `/var`)
  - **File**: `tests/unit/test_path_resolver.py`
  - **Solution**: Use `Path.resolve()` to resolve symlinks
  - **Tests**:
    - `test_resolve_project_root_with_git`
    - `test_resolve_project_root_without_git`
    - `test_resolve_project_root_from_various_depths`
    - `test_get_settings_path`
    - `test_get_settings_path_from_nested`
    - `test_get_metrics_dir`
    - `test_get_metrics_dir_from_nested`
    - `test_get_metrics_file_default`
    - `test_get_metrics_file_custom_filename`
  - **Estimated Time**: 2 hours
  - **Code Changes**:
    ```python
    # Expected change in test assertions
    expected = Path(tmp_path).resolve()  # Add .resolve()
    actual = result.resolve()            # Add .resolve()
    assert actual == expected
    ```

### File Operation Tests (2 failures) - MEDIUM PRIORITY

- [ ] **Fix parent directory creation in atomic_write**
  - **File**: `installer/global/commands/lib/user_interaction.py`
  - **Test**: `test_safe_save_file_creates_parent_dir`
  - **Solution**: Ensure `mkdir(parents=True)` runs before tempfile creation
  - **Estimated Time**: 1 hour
  - **Code Changes**:
    ```python
    def atomic_write(file_path: Path, content: str, encoding: str = "utf-8") -> None:
        file_dir = file_path.parent
        file_dir.mkdir(parents=True, exist_ok=True)  # ← Ensure this runs first

        with tempfile.NamedTemporaryFile(...) as tmp_file:
            # ... rest
    ```

- [ ] **Fix task backlog move test**
  - **File**: `tests/unit/test_full_review.py`
  - **Test**: `test_move_task_to_backlog`
  - **Solution**: Add file existence check with retry
  - **Estimated Time**: 1 hour
  - **Code Changes**:
    ```python
    def test_move_task_to_backlog(self, tmp_path):
        # ... setup ...
        handler._move_task_to_backlog()

        # Add retry loop for file system timing
        import time
        for _ in range(5):
            if backlog_path.exists():
                break
            time.sleep(0.1)

        assert backlog_path.exists()
    ```

### Stub Tests (3 failures) - LOW PRIORITY

- [ ] **Update test_execute_modify_stub**
  - **File**: `tests/unit/test_full_review.py`
  - **Issue**: Modification mode fully implemented, test expects stub
  - **Solution**: Mock `ModificationSession` and test actual flow
  - **Estimated Time**: 1 hour
  - **Code Changes**:
    ```python
    def test_execute_modify_stub(self, mocker):
        # Remove stub expectation
        # Mock modification session
        mocker.patch('..ModificationSession')
        # Test actual flow
    ```

- [ ] **Update test_execute_view_stub**
  - **File**: `tests/unit/test_full_review.py`
  - **Issue**: View mode fully implemented, test expects stub message
  - **Solution**: Mock `PagerDisplay` and test actual flow
  - **Estimated Time**: 30 minutes
  - **Code Changes**:
    ```python
    def test_execute_view_stub(self, mocker):
        # Remove "coming soon" assertion
        mocker.patch('..PagerDisplay.show_plan', return_value=True)
        # Test actual view functionality
    ```

- [ ] **Update test_execute_question_stub**
  - **File**: `tests/unit/test_full_review.py`
  - **Issue**: Q&A mode fully implemented, test uses wrong mocks
  - **Solution**: Mock `QAManager` properly
  - **Estimated Time**: 30 minutes

### Metrics Test (1 failure) - LOW PRIORITY

- [ ] **Fix test_append_metric_failure_handling**
  - **File**: `tests/unit/test_metrics_storage.py`
  - **Issue**: Error message format changed in implementation
  - **Solution**: Update test to match actual error format
  - **Estimated Time**: 30 minutes
  - **Code Changes**:
    ```python
    def test_append_metric_failure_handling(self, capsys):
        # ... setup ...
        captured = capsys.readouterr()
        # Update assertion to match actual format
        assert "Warning: Failed to append" in captured.out  # Changed
    ```

**Day 1 Total**: 7 hours (all test failures fixed)

---

## Priority 2: Implement Missing Edge Cases (Days 2-3)

### Day 2: Error Handling Edge Cases

#### 1. File Write Failure Graceful Degradation (2 hours)

- [ ] **Implement graceful degradation for file write failures**
  - **File**: `installer/global/commands/lib/review_modes.py`
  - **Function**: `FullReviewHandler._move_task_to_backlog()`
  - **Acceptance Criteria**:
    - File write failure logs error
    - Workflow continues (doesn't crash)
    - User sees warning message
  - **Code Changes**:
    ```python
    def _move_task_to_backlog(self) -> None:
        try:
            # ... existing logic ...
            FileOperations.atomic_write(backlog_path, updated_content)
            self.task_file_path.unlink()
        except OSError as e:
            logger.error(f"Failed to move task file: {e}")
            print(f"\n⚠️ Warning: Could not move task file (saved in place)")
            # Continue - task state updated even if file move fails
    ```

#### 2. Configuration Flag Conflict Detection (2 hours)

- [ ] **Implement flag validation function**
  - **File**: `installer/global/commands/lib/review_router.py` (or new `flag_validator.py`)
  - **Function**: `validate_user_flags(user_flags: Dict[str, bool]) -> None`
  - **Acceptance Criteria**:
    - Detects `--skip-review` + `--force-review` conflict
    - Raises `ValueError` with helpful message
    - Logs warning for `--auto-proceed` + `--force-review`
  - **Code Changes**:
    ```python
    def validate_user_flags(user_flags: Dict[str, bool]) -> None:
        """Validate user flags for conflicts."""
        if user_flags.get("skip_review") and user_flags.get("force_review"):
            raise ValueError(
                "Conflicting flags: --skip-review and --force-review "
                "cannot be used together. Please specify only one."
            )

        if user_flags.get("auto_proceed") and user_flags.get("force_review"):
            logger.warning(
                "Flag conflict: --force-review overrides --auto-proceed"
            )
            user_flags["auto_proceed"] = False
    ```

- [ ] **Integrate validation into task-work command**
  - **File**: `installer/global/commands/task-work.py` (or entry point)
  - **Call**: `validate_user_flags(user_flags)` before workflow starts
  - **Test Coverage**: Add tests for all conflict scenarios

#### 3. Corrupted Metrics File Skipping (1 hour)

- [ ] **Implement corrupted line skipping**
  - **File**: `installer/global/commands/lib/metrics_storage.py`
  - **Function**: `MetricsStorage.read_all_metrics()`
  - **Acceptance Criteria**:
    - Skips lines with invalid JSON
    - Logs warning for each corrupted line
    - Returns valid metrics only
  - **Code Changes**:
    ```python
    def read_all_metrics(self) -> List[Dict[str, Any]]:
        if not self.metrics_file.exists():
            return []

        metrics = []
        with open(self.metrics_file, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                try:
                    metric = json.loads(line)
                    metrics.append(metric)
                except json.JSONDecodeError as e:
                    logger.warning(
                        f"Skipping corrupted metric at line {line_num}: {e}"
                    )
                    continue  # ← ADD THIS

        return metrics
    ```

#### 4. User-Friendly Error Message Wrappers (3 hours)

- [ ] **Create error message formatter**
  - **File**: `installer/global/commands/lib/error_messages.py` (new)
  - **Functions**:
    - `format_file_error(error: OSError, context: str) -> str`
    - `format_validation_error(error: ValueError, field: str) -> str`
    - `format_calculation_error(error: Exception, task_id: str) -> str`
  - **Acceptance Criteria**:
    - All user-facing errors wrapped with context
    - Include actionable guidance
    - No raw exception traces shown to users
  - **Code Changes**:
    ```python
    def format_file_error(error: OSError, context: str) -> str:
        """Format file operation error with context."""
        if error.errno == 30:  # Read-only file system
            return (
                f"Cannot write to {context}: File system is read-only.\n"
                f"Solution: Check disk permissions or free up space."
            )
        elif error.errno == 28:  # No space left
            return (
                f"Cannot write to {context}: No space left on device.\n"
                f"Solution: Free up disk space and try again."
            )
        else:
            return (
                f"Cannot write to {context}: {error}\n"
                f"Solution: Check file permissions and try again."
            )
    ```

- [ ] **Apply error formatters to all user-facing errors**
  - **Files**: `review_modes.py`, `complexity_calculator.py`, `user_interaction.py`
  - **Replace**: Raw `print(f"Error: {e}")` with formatted messages
  - **Test Coverage**: Verify error messages are helpful

**Day 2 Total**: 8 hours (error handling edge cases complete)

### Day 3: Boundary & State Edge Cases

#### 1. Empty Plan Section Display (1 hour)

- [ ] **Update display functions to handle None values**
  - **File**: `installer/global/commands/lib/review_modes.py`
  - **Functions**:
    - `FullReviewDisplay._display_implementation_order()`
    - `FullReviewDisplay._display_risk_assessment()`
  - **Acceptance Criteria**:
    - No "None" text displayed
    - Shows "Not specified" or similar friendly message
  - **Code Changes**:
    ```python
    def _display_implementation_order(self) -> None:
        print("\n📋 IMPLEMENTATION ORDER:")

        if self.plan.phases:
            for i, phase in enumerate(self.plan.phases, 1):
                print(f"\n  {i}. {phase}")
        else:
            print("\n  No implementation phases specified")  # ← CHANGE

        if self.plan.estimated_loc:
            print(f"\n  Estimated Lines of Code: ~{self.plan.estimated_loc}")
        else:
            print(f"\n  Estimated Lines of Code: Not specified")  # ← ADD
    ```

#### 2. Modification Complexity Increase Warning (2 hours)

- [ ] **Add complexity comparison in apply modifications**
  - **File**: `installer/global/commands/lib/review_modes.py`
  - **Function**: `FullReviewHandler._apply_modifications_and_return()`
  - **Acceptance Criteria**:
    - Compare old vs new complexity scores
    - Display warning if score increases
    - Show old and new scores
  - **Code Changes**:
    ```python
    def _apply_modifications_and_return(self, session) -> Optional[FullReviewResult]:
        # ... apply changes ...
        modified_plan = applier.apply()

        # Recalculate complexity
        new_complexity = calculator.calculate(context)
        old_score = self.complexity_score.total_score
        new_score = new_complexity.total_score

        # ← ADD THIS: Warn if complexity increased
        if new_score > old_score:
            print(f"\n⚠️ Warning: Modifications increased complexity!")
            print(f"   Old score: {old_score}/10")
            print(f"   New score: {new_score}/10")
            print(f"   Consider simplifying further.\n")

        # ... rest
    ```

#### 3. Q&A Session Question Limit (2 hours)

- [ ] **Add max_questions parameter to Q&A session**
  - **File**: `installer/global/commands/lib/qa_manager.py`
  - **Function**: `QAManager.run_qa_session()`
  - **Acceptance Criteria**:
    - Default limit of 20 questions
    - Stop accepting questions after limit
    - Show warning message at limit
  - **Code Changes**:
    ```python
    def run_qa_session(self, max_questions: int = 20) -> Optional[QASession]:
        """Run interactive Q&A session with question limit."""
        session = QASession(...)

        question_count = 0
        while True:
            user_input = input("\nYour question (or 'back'): ").strip()

            if user_input.lower() == "back":
                break

            question_count += 1
            if question_count > max_questions:
                print(f"\n⚠️ Maximum questions reached ({max_questions})")
                print("Returning to review checkpoint...\n")
                break

            # ... handle question ...
    ```

#### 4. Zero-File Task Validation (1 hour)

- [ ] **Verify minimum score enforcement for zero-file tasks**
  - **File**: `installer/global/commands/lib/complexity_calculator.py`
  - **Function**: `ComplexityCalculator._aggregate_scores()`
  - **Acceptance Criteria**:
    - Score never < 1
    - Log warning for zero-file tasks
  - **Verification**:
    ```python
    # Line 196 in complexity_calculator.py - ALREADY IMPLEMENTED ✅
    final_score = max(final_score, 1)  # Ensure minimum score of 1

    # Just need to verify behavior in tests
    ```

- [ ] **Add test for zero-file task**
  - **File**: `tests/edge_cases/test_boundary_conditions.py`
  - **Test**: `test_task_with_zero_files()`

**Day 3 Total**: 6 hours (boundary & state edge cases complete)

---

## Priority 3: Write Edge Case Tests (Day 4)

### Create Edge Case Test Directory

- [ ] **Create directory structure**
  ```bash
  mkdir -p tests/edge_cases
  touch tests/edge_cases/__init__.py
  touch tests/edge_cases/conftest.py
  ```

### Test File 1: Error Handling (3 hours)

- [ ] **Create test_error_handling.py**
  - **File**: `tests/edge_cases/test_error_handling.py`
  - **Tests** (5 total):
    - `test_plan_generation_failure_graceful_degradation`
    - `test_complexity_calculation_error_defaults_to_score_5`
    - `test_user_interrupt_ctrl_c_clean_exit`
    - `test_invalid_user_input_reprompt_with_error_message`
    - `test_file_write_failure_logs_error_continues`

### Test File 2: Boundary Conditions (2 hours)

- [ ] **Create test_boundary_conditions.py**
  - **File**: `tests/edge_cases/test_boundary_conditions.py`
  - **Tests** (5 total):
    - `test_task_with_zero_files`
    - `test_task_with_50_plus_files_very_complex`
    - `test_task_with_no_dependencies`
    - `test_task_with_10_plus_dependencies`
    - `test_empty_plan_sections_display_not_specified`

### Test File 3: Configuration Edge Cases (2 hours)

- [ ] **Create test_configuration_edge.py**
  - **File**: `tests/edge_cases/test_configuration_edge.py`
  - **Tests** (4 total):
    - `test_invalid_threshold_values_use_defaults`
    - `test_conflicting_flags_display_error`
    - `test_missing_settings_json_uses_built_in_defaults`
    - `test_corrupted_metrics_file_creates_new`

### Test File 4: Concurrency & State (1 hour)

- [ ] **Create test_concurrency_state.py**
  - **File**: `tests/edge_cases/test_concurrency_state.py`
  - **Tests** (4 total):
    - `test_multiple_modifications_v1_to_v4`
    - `test_modification_that_increases_complexity_warns_user`
    - `test_long_qa_session_10_plus_questions_limited`
    - `test_timeout_during_file_write_handled_gracefully`

**Day 4 Total**: 8 hours (18 edge case tests complete)

---

## Priority 4: Documentation Updates (Day 5)

### Update Technical Documentation (4 hours)

- [ ] **Update README.md with error handling patterns**
  - **File**: `installer/global/commands/lib/README.md`
  - **Sections**:
    - Error Handling Patterns
    - Fail-Safe Defaults
    - Graceful Degradation Examples
    - Edge Case Behaviors

- [ ] **Document edge case behaviors in API docs**
  - **Files**: Module docstrings in:
    - `complexity_calculator.py`
    - `review_modes.py`
    - `user_interaction.py`
    - `metrics_storage.py`
  - **Add**: Edge case handling documentation

### Create Troubleshooting Guide (2 hours)

- [ ] **Create troubleshooting guide**
  - **File**: `docs/TROUBLESHOOTING.md` (new)
  - **Sections**:
    - Common Edge Cases
    - Error Messages and Solutions
    - Configuration Issues
    - File Operation Errors
    - Platform-Specific Issues (macOS symlinks)

### Update User Documentation (2 hours)

- [ ] **Update CLAUDE.md with edge case examples**
  - **File**: `CLAUDE.md`
  - **Add Section**: "Edge Case Handling"
  - **Examples**:
    - What happens if plan generation fails?
    - What happens if file write fails?
    - What happens with conflicting flags?
    - What happens with zero-file tasks?

**Day 5 Total**: 8 hours (documentation complete)

---

## Success Criteria Checklist

### Test Coverage

- [ ] All 7 test failures fixed
- [ ] 18 new edge case tests passing
- [ ] Unit test coverage ≥ 90% (currently 69%)
- [ ] Integration test coverage ≥ 80%

### Edge Case Implementation

- [ ] All 5 error handling edge cases implemented
- [ ] All 5 boundary condition edge cases implemented
- [ ] All 4 configuration edge cases implemented
- [ ] All 4 concurrency/state edge cases implemented

### Code Quality

- [ ] All modules < 10 cyclomatic complexity
- [ ] Error messages are user-friendly
- [ ] All file operations are atomic
- [ ] All user inputs are validated

### Documentation

- [ ] Error handling patterns documented
- [ ] Troubleshooting guide created
- [ ] Edge case examples in user docs
- [ ] API docs updated with edge case behaviors

---

## Execution Plan Summary

| Day | Priority | Tasks | Hours | Status |
|-----|----------|-------|-------|--------|
| **1** | Fix Tests | Path resolver, file ops, stubs | 7h | ⬜ Not Started |
| **2** | Error Handling | File write, flags, metrics, messages | 8h | ⬜ Not Started |
| **3** | Boundary & State | Display, complexity, Q&A, validation | 6h | ⬜ Not Started |
| **4** | Edge Case Tests | 18 new tests across 4 files | 8h | ⬜ Not Started |
| **5** | Documentation | README, troubleshooting, CLAUDE.md | 8h | ⬜ Not Started |

**Total Effort**: 37 hours (5 days @ 7-8 hours/day)

---

## Risk Assessment

### Low Risk Items
- Test failure fixes (clear solutions)
- Empty plan section display (simple changes)
- Zero-file task validation (already implemented)

### Medium Risk Items
- File write failure handling (needs careful testing)
- Configuration flag validation (needs integration testing)
- Q&A question limit (needs UX consideration)

### High Risk Items
- None identified (all changes are low-complexity)

---

## Notes for Implementation

### Testing Strategy
1. Fix all test failures first (validates platform behavior)
2. Implement error handling edge cases (prevents production issues)
3. Write edge case tests (ensures edge cases stay fixed)
4. Update documentation last (reflects final implementation)

### Code Review Checkpoints
- After Day 1: Verify all test failures fixed
- After Day 3: Verify all edge cases implemented
- After Day 4: Verify edge case test coverage ≥ 90%
- After Day 5: Final review before merge

### Deployment Checklist
- [ ] All tests passing (569 → 580+ tests)
- [ ] Coverage ≥ 90% unit, ≥ 80% integration
- [ ] Documentation updated
- [ ] CHANGELOG.md updated with edge case improvements
- [ ] Ready for production deployment

---

**Created**: 2025-10-10
**Last Updated**: 2025-10-10
**Status**: READY FOR IMPLEMENTATION
