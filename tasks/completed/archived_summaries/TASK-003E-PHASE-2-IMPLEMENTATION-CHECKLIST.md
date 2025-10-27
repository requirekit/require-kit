# TASK-003E Phase 2: Implementation Checklist

**Quick Start Guide for Implementation**

---

## Pre-Implementation Verification ✅

**Run these checks before starting implementation:**

```bash
# 1. Verify Phase 1 foundation exists
pytest tests/unit/test_complexity_calculation_comprehensive.py -v
# Expected: 45+ tests passing

pytest tests/unit/test_review_modes_quick.py -v
# Expected: 60+ tests passing

pytest tests/unit/test_review_router.py -v
# Expected: 40+ tests passing

# 2. Verify dependency modules exist
ls -la installer/global/commands/lib/review_modes.py
ls -la installer/global/commands/lib/review_router.py
ls -la installer/global/commands/lib/complexity_models.py

# 3. Verify fixtures exist
ls -la tests/fixtures/data_fixtures.py
ls -la tests/fixtures/mock_fixtures.py

# 4. Create integration test directory
mkdir -p tests/integration
```

---

## Day 1: Factory Fixtures + Simple Workflows (6-8 hours)

### Morning Session (3-4 hours)

#### Task 1.1: Create Factory Fixtures (1.5-2 hours)

**File**: `tests/fixtures/factory_fixtures.py`

**Checklist**:
- [ ] Create file with module docstring
- [ ] Import required dependencies (Mock, ImplementationPlan, etc.)
- [ ] Implement `display_factory()` function (~25 lines)
  ```python
  def display_factory(plan, output_writer=None, template_renderer=None):
      """Factory for QuickReviewDisplay with injectable dependencies."""
      # Implementation...
  ```
- [ ] Implement `session_factory()` function (~25 lines)
  ```python
  def session_factory(input_provider=None, output_writer=None, timeout_seconds=10):
      """Factory for user interaction session with injectable I/O."""
      # Implementation...
  ```
- [ ] Implement `version_manager_factory()` function (~25 lines)
  ```python
  def version_manager_factory(storage_backend=None, versioning_strategy="sequential"):
      """Factory for plan version manager with injectable storage."""
      # Implementation...
  ```
- [ ] Implement `router_factory()` function (~25 lines)
  ```python
  def router_factory(routing_strategy=None, thresholds=None):
      """Factory for ReviewRouter with injectable routing strategy."""
      # Implementation...
  ```
- [ ] Add helper function `create_implementation_plan()` (~10 lines)
- [ ] Test imports: `python -c "from tests.fixtures.factory_fixtures import *"`

**Time Estimate**: 1.5-2 hours

---

#### Task 1.2: Create Integration conftest.py (0.5 hours)

**File**: `tests/integration/conftest.py`

**Checklist**:
- [ ] Create file with module docstring
- [ ] Import factory functions from `tests.fixtures.factory_fixtures`
- [ ] Import data fixtures from `tests.fixtures.data_fixtures`
- [ ] Import mock fixtures from `tests.fixtures.mock_fixtures`
- [ ] Add pytest plugin registration
  ```python
  pytest_plugins = [
      "tests.fixtures.data_fixtures",
      "tests.fixtures.mock_fixtures",
      "tests.fixtures.factory_fixtures",
  ]
  ```
- [ ] Add integration-specific markers
  ```python
  def pytest_configure(config):
      config.addinivalue_line("markers", "integration: Integration tests")
      config.addinivalue_line("markers", "slow: Slow-running integration tests")
  ```

**Time Estimate**: 0.5 hours

---

#### Task 1.3: Auto-Proceed Workflow Tests (2 hours)

**File**: `tests/integration/test_workflow_auto_proceed.py`

**Checklist**:
- [ ] Create file with module docstring and imports
- [ ] Test 1: Happy path (score 1-3 → auto-proceed)
  ```python
  @pytest.mark.integration
  def test_auto_proceed_happy_path():
      """Test auto-proceed workflow for low complexity (score 1-3)."""
      # Arrange: Create plan with score 2
      # Act: Execute review workflow
      # Assert: Auto-proceeds to Phase 3, no user interaction
  ```
- [ ] Test 2: Boundary test (score exactly 3)
- [ ] Test 3: No user interaction verification
- [ ] Test 4: Metadata updated with complexity score
- [ ] Test 5: Performance (<1 second)
- [ ] Optional Test 6: Display error recovery (if time permits)
- [ ] Run tests: `pytest tests/integration/test_workflow_auto_proceed.py -v`
- [ ] Verify all pass, coverage ≥80%

**Time Estimate**: 2 hours

**Target**: 5-6 tests passing

---

### Afternoon Session (3-4 hours)

#### Task 1.4: Force Override Workflow Tests (1.5-2 hours)

**File**: `tests/integration/test_workflow_force_override.py`

**Checklist**:
- [ ] Create file with module docstring and imports
- [ ] Test 1: Security trigger forces full review (score 2 + trigger → full)
- [ ] Test 2: Multiple triggers displayed
- [ ] Test 3: User flag override (--review-plan)
- [ ] Optional Test 4: Force trigger metadata (if time permits)
- [ ] Run tests: `pytest tests/integration/test_workflow_force_override.py -v`
- [ ] Verify all pass, coverage ≥75%

**Time Estimate**: 1.5-2 hours

**Target**: 3-4 tests passing

---

#### Task 1.5: Quick Timeout Workflow Tests (2-2.5 hours)

**File**: `tests/integration/test_workflow_quick_timeout.py`

**Checklist**:
- [ ] Create file with module docstring and imports
- [ ] Test 1: Happy path (score 4-6 → display → countdown → timeout → auto-proceed)
- [ ] Test 2: Countdown completes (10 seconds)
- [ ] Test 3: Timeout action triggers auto-approval
- [ ] Test 4: Metadata includes timeout event
- [ ] Test 5: Performance (countdown updates ~100ms)
- [ ] Test 6: Error during countdown → escalate
- [ ] Optional Test 7: Custom timeout duration (if time permits)
- [ ] Run tests: `pytest tests/integration/test_workflow_quick_timeout.py -v`
- [ ] Verify all pass, coverage ≥80%

**Time Estimate**: 2-2.5 hours

**Target**: 6-7 tests passing

---

### End of Day 1 Checklist

- [ ] Factory fixtures complete (4 factories + helper)
- [ ] Integration conftest.py configured
- [ ] Auto-proceed workflow: 5-6 tests passing
- [ ] Force override workflow: 3-4 tests passing
- [ ] Quick timeout workflow: 6-7 tests passing
- [ ] **Total: 14-17 tests passing**
- [ ] Coverage report generated: `pytest tests/integration/ --cov --cov-report=html`
- [ ] All tests pass: `pytest tests/integration/ -v`
- [ ] Commit progress: `git add tests/ && git commit -m "Phase 2 Day 1: Factory fixtures + simple workflows"`

---

## Day 2: Escalation + Q&A + Full Review (7-8 hours)

### Morning Session (3-4 hours)

#### Task 2.1: Quick Escalation Workflow Tests (2.5-3 hours)

**File**: `tests/integration/test_workflow_quick_escalation.py`

**Checklist**:
- [ ] Create file with module docstring and imports
- [ ] Test 1: Happy path (ENTER during countdown → escalate to full)
- [ ] Test 2: Countdown interrupted immediately
- [ ] Test 3: Mode transition (QUICK → FULL)
- [ ] Test 4: Full review displays after escalation
- [ ] Test 5: Metadata includes escalation event + timestamp
- [ ] Optional Test 6: Escalation at various times (if time permits)
- [ ] Run tests: `pytest tests/integration/test_workflow_quick_escalation.py -v`
- [ ] Verify all pass, coverage ≥80%

**Time Estimate**: 2.5-3 hours

**Target**: 5-6 tests passing

---

#### Task 2.2: Q&A Mode Workflow Tests (2-2.5 hours)

**File**: `tests/integration/test_workflow_qa_mode.py`

**Checklist**:
- [ ] Create file with module docstring and imports
- [ ] Test 1: Happy path (Q&A → ask question → answer → return to review)
- [ ] Test 2: Multiple questions in sequence (3 questions)
- [ ] Test 3: Q&A history saved to metadata
- [ ] Test 4: Return to review after Q&A
- [ ] Test 5: Q&A then approve workflow
- [ ] Run tests: `pytest tests/integration/test_workflow_qa_mode.py -v`
- [ ] Verify all pass, coverage ≥75%

**Time Estimate**: 2-2.5 hours

**Target**: 4-5 tests passing

---

### Afternoon Session (4 hours)

#### Task 2.3: Full Review Workflow Tests (4-4.5 hours)

**File**: `tests/integration/test_workflow_full_review.py`

**Checklist**:
- [ ] Create file with module docstring and imports
- [ ] Test 1: Happy path - Approve (score 7-10 → approve → Phase 3)
- [ ] Test 2: Happy path - Modify (user requests modification)
- [ ] Test 3: Happy path - Q&A (ask questions → return to review)
- [ ] Test 4: Happy path - Cancel (cancel → save work → backlog)
- [ ] Test 5: Invalid input handling (re-prompt with error)
- [ ] Test 6: Metadata with decision + timestamp
- [ ] Test 7: Force trigger display (if trigger present)
- [ ] Optional Test 8: Multiple retries (if time permits)
- [ ] Run tests: `pytest tests/integration/test_workflow_full_review.py -v`
- [ ] Verify all pass, coverage ≥80%

**Time Estimate**: 4-4.5 hours

**Target**: 7-8 tests passing

---

### End of Day 2 Checklist

- [ ] Quick escalation workflow: 5-6 tests passing
- [ ] Q&A mode workflow: 4-5 tests passing
- [ ] Full review workflow: 7-8 tests passing
- [ ] **Day 2 Total: 16-19 tests passing**
- [ ] **Cumulative: 30-36 tests passing**
- [ ] Coverage report: `pytest tests/integration/ --cov --cov-report=html`
- [ ] All tests pass: `pytest tests/integration/ -v`
- [ ] Commit progress: `git add tests/ && git commit -m "Phase 2 Day 2: Escalation + Q&A + Full Review workflows"`

---

## Day 3: Modification Loop + Quality Gates (7-8 hours)

### Morning Session (5-6 hours)

#### Task 3.1: Modification Loop Workflow Tests (5-6.5 hours)

**File**: `tests/integration/test_workflow_modification_loop.py`

**Checklist**:
- [ ] Create file with module docstring and imports
- [ ] Test 1: Happy path (modify → re-calculate → review again)
- [ ] Test 2: Complexity decreases (9 → 7 after modification)
- [ ] Test 3: Complexity increases (7 → 9 after modification)
- [ ] Test 4: Version increment (v1 → v2 → v3)
- [ ] Test 5: Multiple modifications (v1 → v2 → v3 → v4 loop)
- [ ] Test 6: Modification then approve
- [ ] Test 7: Modification then cancel (save all versions)
- [ ] Test 8: Metadata with all modification events
- [ ] Optional Test 9: File change tracking (if time permits)
- [ ] Optional Test 10: Plan regeneration (if time permits)
- [ ] Run tests: `pytest tests/integration/test_workflow_modification_loop.py -v`
- [ ] Verify all pass, coverage ≥80%

**Time Estimate**: 5-6.5 hours

**Target**: 8-10 tests passing

---

### Afternoon Session (2-3 hours)

#### Task 3.2: Coverage Verification (0.5 hours)

**Checklist**:
- [ ] Run full integration suite with coverage:
  ```bash
  pytest tests/integration/ -v \
      --cov=installer/global/commands/lib \
      --cov-report=term-missing \
      --cov-report=html \
      --cov-report=json \
      --cov-fail-under=80
  ```
- [ ] Verify line coverage ≥80%
- [ ] Verify branch coverage ≥75%
- [ ] Identify any coverage gaps
- [ ] Document coverage results

**Time Estimate**: 0.5 hours

---

#### Task 3.3: Fix Coverage Gaps (1-1.5 hours)

**Checklist**:
- [ ] Review coverage report HTML: `open htmlcov/index.html`
- [ ] Identify uncovered lines in:
  - `review_modes.py`
  - `review_router.py`
  - `plan_templates.py`
- [ ] Add targeted tests for uncovered paths
- [ ] Re-run coverage: `pytest tests/integration/ --cov --cov-fail-under=80`
- [ ] Verify all coverage targets met

**Time Estimate**: 1-1.5 hours

---

#### Task 3.4: Quality Gates (0.5 hours)

**Checklist**:
- [ ] Test count verification:
  ```bash
  pytest tests/integration/ --collect-only | grep "test session"
  # Expected: "collected 40 items" to "collected 45 items"
  ```
- [ ] All tests pass:
  ```bash
  pytest tests/integration/ -v
  # Expected: 40-45 tests passed
  ```
- [ ] Test execution time:
  ```bash
  time pytest tests/integration/
  # Expected: <3 minutes
  ```
- [ ] No flaky tests (run 3x):
  ```bash
  for i in {1..3}; do pytest tests/integration/ -v; done
  ```
- [ ] Factory fixtures working:
  ```bash
  python -c "from tests.fixtures.factory_fixtures import *; print('✅')"
  ```
- [ ] Generate final coverage report:
  ```bash
  pytest tests/integration/ --cov --cov-report=html --cov-report=json
  ```

**Time Estimate**: 0.5 hours

---

#### Task 3.5: Documentation (0.5 hours)

**Checklist**:
- [ ] Update TASK-003E-PYTHON-PYTEST-IMPLEMENTATION-PLAN.md:
  - [ ] Mark Phase 2 as complete
  - [ ] Update test counts (actual vs planned)
  - [ ] Update coverage results
  - [ ] Note any deviations from plan
- [ ] Create Phase 2 completion report:
  - [ ] Test count: X tests (target: 40-45)
  - [ ] Coverage: X% line, Y% branch (target: ≥80%, ≥75%)
  - [ ] Execution time: X seconds (target: <180s)
  - [ ] Architectural improvements implemented
  - [ ] Quality gates passed

**Time Estimate**: 0.5 hours

---

### End of Day 3 Checklist

- [ ] Modification loop workflow: 8-10 tests passing
- [ ] **Day 3 Total: 8-10 tests passing**
- [ ] **Phase 2 Total: 40-45 tests passing** ✅
- [ ] Coverage targets met: ≥80% line, ≥75% branch ✅
- [ ] All quality gates passed ✅
- [ ] Documentation updated ✅
- [ ] Final commit: `git add tests/ docs/ && git commit -m "Phase 2 COMPLETE: Integration tests + factory fixtures"`

---

## Final Verification

### Run Complete Test Suite

```bash
# 1. Run all integration tests
pytest tests/integration/ -v

# 2. Run with coverage
pytest tests/integration/ \
    --cov=installer/global/commands/lib \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-fail-under=80

# 3. Check test count
pytest tests/integration/ --collect-only | grep "test session"

# 4. Check execution time
time pytest tests/integration/

# 5. Verify no flaky tests
for i in {1..3}; do
    echo "=== Run $i ==="
    pytest tests/integration/ -v
done
```

### Expected Results

| Metric | Target | Status |
|--------|--------|--------|
| Test count | 40-45 tests | ⬜ |
| Line coverage | ≥80% | ⬜ |
| Branch coverage | ≥75% | ⬜ |
| All tests pass | 100% | ⬜ |
| Execution time | <3 minutes | ⬜ |
| No flaky tests | 100% reliable (3 runs) | ⬜ |
| Factory fixtures | 4 factories working | ⬜ |
| Architectural score | ≥78/100 (projected) | ⬜ |

---

## Troubleshooting

### Common Issues

#### Issue 1: Import Errors
```bash
# Error: ModuleNotFoundError: No module named 'review_modes'
# Solution: Verify path setup in conftest.py
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "installer" / "global" / "commands" / "lib"))
```

#### Issue 2: Coverage Below Target
```bash
# Error: Coverage 78%, target 80%
# Solution: Add targeted tests for uncovered paths
open htmlcov/index.html  # Find uncovered lines
pytest tests/integration/ --cov --cov-report=html
```

#### Issue 3: Flaky Tests
```bash
# Error: Test passes sometimes, fails other times
# Solution: Check for:
# - Shared state between tests (use fixtures for isolation)
# - Time-dependent assertions (mock time)
# - File system dependencies (use tmp_path)
```

#### Issue 4: Slow Tests
```bash
# Error: Tests take >3 minutes
# Solution: Check for:
# - Real sleep() calls (should be mocked)
# - Unnecessary test duplication (consolidate)
# - Expensive setup (use module-scoped fixtures)
```

---

## Success Criteria

### Phase 2 is COMPLETE when:

- ✅ All 40-45 integration tests implemented and passing
- ✅ Factory fixtures complete (4 factories + helper function)
- ✅ Coverage targets met: ≥80% line, ≥75% branch
- ✅ All quality gates passed
- ✅ Test execution time <3 minutes
- ✅ No flaky tests (3 consecutive runs pass)
- ✅ Documentation updated
- ✅ Code committed and pushed

**Then proceed to Phase 3: E2E Tests**

---

## Quick Reference

### File Locations
```
tests/
├── fixtures/
│   └── factory_fixtures.py              # NEW (Day 1)
├── integration/
│   ├── conftest.py                      # NEW (Day 1)
│   ├── test_workflow_auto_proceed.py    # NEW (Day 1)
│   ├── test_workflow_force_override.py  # NEW (Day 1)
│   ├── test_workflow_quick_timeout.py   # NEW (Day 1)
│   ├── test_workflow_quick_escalation.py # NEW (Day 2)
│   ├── test_workflow_qa_mode.py         # NEW (Day 2)
│   ├── test_workflow_full_review.py     # NEW (Day 2)
│   └── test_workflow_modification_loop.py # NEW (Day 3)
```

### Key Commands
```bash
# Run integration tests
pytest tests/integration/ -v

# Run with coverage
pytest tests/integration/ --cov --cov-report=html

# Check test count
pytest tests/integration/ --collect-only | grep "test session"

# Check execution time
time pytest tests/integration/

# Check for flaky tests
for i in {1..3}; do pytest tests/integration/ -v; done
```

### Test Distribution
- Day 1: 14-17 tests (auto-proceed, force override, quick timeout)
- Day 2: 16-19 tests (quick escalation, Q&A mode, full review)
- Day 3: 8-10 tests (modification loop)
- **Total: 40-45 tests**

---

**Checklist Created**: 2025-10-10
**Ready for Implementation**: ✅ YES
**Estimated Time**: 21.5-26 hours (3-3.5 days)
