# TASK-003E Phase 2: Python pytest Implementation Plan
## Integration Test Suite Design

**Date**: 2025-10-10
**Task**: TASK-003E - Comprehensive Testing & Documentation
**Phase**: 2 of 4 (Integration Test Suite)
**Technology Stack**: Python with pytest, pytest-mock, pytest-asyncio
**Target Coverage**: ≥80% line, ≥75% branch

---

## Executive Summary

This document provides a comprehensive implementation plan for Phase 2 Integration Tests following pytest best practices and Python testing patterns. The plan builds on the Phase 1 infrastructure (fixtures, mocks, coverage config) to create 7 integration test workflows with 54 total tests.

**Key Design Decisions**:
- ✅ Use existing `data_fixtures.py` and `mock_fixtures.py` from Phase 1
- ✅ Leverage pytest-mock for clean mocking patterns
- ✅ Implement fast tests using mock timers (no actual delays)
- ✅ Use `tmp_path` fixture for file I/O isolation
- ✅ Apply AAA (Arrange-Act-Assert) pattern consistently
- ✅ Parametrize tests for comprehensive coverage with minimal code

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [File Structure](#file-structure)
3. [Fixture Design](#fixture-design)
4. [Mocking Strategy](#mocking-strategy)
5. [Test Implementation Plan](#test-implementation-plan)
6. [Pattern Examples](#pattern-examples)
7. [Implementation Order](#implementation-order)
8. [Risk Mitigation](#risk-mitigation)
9. [Time Estimates](#time-estimates)

---

## Architecture Overview

### Testing Architecture Layers

```
Integration Tests (Phase 2)
├── Workflow Tests (7 workflows)
│   ├── Auto-Proceed Workflow
│   ├── Quick Review + Timeout
│   ├── Quick Review + Escalation
│   ├── Full Review + Approval
│   ├── Modification Loop
│   ├── Q&A Mode
│   └── Force Override
│
├── Fixture Layer (from Phase 1)
│   ├── data_fixtures.py (11 test data fixtures)
│   └── mock_fixtures.py (10 mock objects)
│
├── Helper Layer (NEW)
│   ├── workflow_fixtures.py (workflow-specific fixtures)
│   ├── assertion_helpers.py (workflow validation)
│   └── workflow_builders.py (test scenario builders)
│
└── Mock Strategy Layer (NEW)
    ├── Time simulation (mock countdown, timers)
    ├── User input injection (keyboard events, input())
    └── File I/O mocking (tmp_path, pathlib mocks)
```

### Integration Test Scope

**What We Test**:
- ✅ End-to-end workflow execution (complexity → review → decision → state change)
- ✅ Component integration (calculator + router + review handlers)
- ✅ State transitions (backlog → in_progress → in_review → completed)
- ✅ User interaction flows (timeout, escalation, approval, cancellation)
- ✅ File system operations (task file movement, metadata updates)
- ✅ Timer and countdown behavior (mock-based, no actual delays)

**What We Don't Test** (Unit test scope):
- ❌ Individual component logic (covered by Phase 1 unit tests)
- ❌ Pure calculation functions (covered by `test_complexity_calculation_comprehensive.py`)
- ❌ Display rendering details (covered by `test_review_modes_quick.py`)

### Performance Targets

| Workflow | Max Execution Time | Mock Strategy |
|----------|-------------------|---------------|
| Auto-Proceed | <2 seconds | Direct execution (score 1-3) |
| Quick Timeout | <2 seconds | Mock timer (instant timeout) |
| Quick Escalation | <2 seconds | Mock input ("enter" key) |
| Full Approval | <3 seconds | Mock input ("a" key) |
| Modification Loop | <5 seconds | Mock input sequence |
| Q&A Mode | <3 seconds | Mock input sequence |
| Force Override | <2 seconds | Force trigger detection |

**Total Suite Target**: <5 minutes for all 54 tests

---

## File Structure

### Directory Layout

```
tests/
├── fixtures/                          # Phase 1 (EXISTING)
│   ├── __init__.py                   # Fixture exports
│   ├── data_fixtures.py              # Test data (11 fixtures)
│   └── mock_fixtures.py              # Mock objects (10 mocks)
│
├── helpers/                           # NEW for Phase 2
│   ├── __init__.py                   # Helper exports
│   ├── workflow_fixtures.py          # Workflow-specific fixtures
│   ├── assertion_helpers.py          # Validation utilities
│   └── workflow_builders.py          # Test scenario builders
│
├── integration/                       # NEW for Phase 2
│   ├── __init__.py
│   ├── conftest.py                   # Integration-specific config
│   ├── test_workflow_auto_proceed.py          # 6 tests
│   ├── test_workflow_quick_timeout.py         # 8 tests
│   ├── test_workflow_quick_escalation.py      # 8 tests
│   ├── test_workflow_full_approval.py         # 10 tests
│   ├── test_workflow_modification_loop.py     # 12 tests
│   ├── test_workflow_qa_mode.py               # 6 tests
│   └── test_workflow_force_override.py        # 4 tests
│
├── coverage_config.py                 # Phase 1 (EXISTING)
└── unit/                              # Phase 1 (EXISTING)
    ├── test_complexity_calculation_comprehensive.py
    └── test_review_modes_quick.py
```

### Import Dependencies

```python
# Integration test imports (common pattern)
import pytest
import sys
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock, call
from typing import List, Dict, Any, Optional

# Add lib to path (consistent with Phase 1)
installer_lib_path = Path(__file__).parent.parent.parent / "installer" / "global" / "commands" / "lib"
if installer_lib_path.exists():
    sys.path.insert(0, str(installer_lib_path))

    # Import system under test
    from complexity_calculator import ComplexityCalculator
    from review_router import ReviewRouter
    from review_modes import QuickReviewHandler, FullReviewHandler
    from complexity_models import (
        ComplexityScore, ImplementationPlan, ReviewMode,
        EvaluationContext, ReviewDecision
    )

    # Import helpers and fixtures
    from tests.fixtures.data_fixtures import *
    from tests.fixtures.mock_fixtures import *
    from tests.helpers.workflow_fixtures import *
    from tests.helpers.assertion_helpers import *

    sys.path.pop(0)
```

---

## Mocking Strategy

### 1. Time Simulation

**Challenge**: Countdown timers wait 10 seconds - too slow for tests.

**Solution**: Mock `countdown_timer` to return instantly.

```python
# Mock Implementation (in workflow_fixtures.py)
@pytest.fixture
def countdown_mock(mocker):
    """Mock countdown_timer with instant result."""
    mock = mocker.patch('review_modes.countdown_timer')
    mock.return_value = "timeout"  # Default to timeout
    return mock

# Test Usage
def test_quick_timeout(countdown_mock, workflow_context):
    """Should auto-approve after timeout."""
    # Arrange
    countdown_mock.return_value = "timeout"

    # Act
    result = workflow_context.execute_quick_review()

    # Assert
    assert result.action == "timeout"
    assert result.auto_approved is True
```

**Performance**: <100ms vs 10+ seconds (100x faster)

### 2. User Input Injection

**Challenge**: Tests need to simulate user keyboard input.

**Solution**: Mock `input()` with predefined sequences.

```python
# Mock Implementation (in workflow_fixtures.py)
@pytest.fixture
def user_input_sequence(mocker):
    """Mock input() with sequence."""
    inputs = []
    input_index = [0]

    def mock_input(prompt=""):
        if input_index[0] < len(inputs):
            result = inputs[input_index[0]]
            input_index[0] += 1
            return result
        return ""

    mock = mocker.patch('builtins.input', side_effect=mock_input)

    def set_inputs(input_list):
        nonlocal inputs
        inputs = input_list
        input_index[0] = 0

    mock.set_inputs = set_inputs
    return mock

# Test Usage
def test_full_approval(user_input_sequence, workflow_context):
    """Should approve plan when user types 'a'."""
    # Arrange
    user_input_sequence.set_inputs(['a'])

    # Act
    result = workflow_context.execute_full_review()

    # Assert
    assert result.action == "approve"
    assert result.approved is True
```

### 3. File I/O Mocking

**Challenge**: Tests need isolated file system for task file operations.

**Solution**: Use `tmp_path` fixture (built-in pytest).

```python
# Test Usage (tmp_path is built-in)
def test_task_state_transition(tmp_path, task_file_factory):
    """Should move task file from in_progress to in_review."""
    # Arrange
    task_file = task_file_factory(
        task_id="TASK-001",
        status="in_progress"
    )

    # Act
    move_task_to_review(task_file)

    # Assert
    in_progress_file = tmp_path / "tasks" / "in_progress" / "TASK-001.md"
    in_review_file = tmp_path / "tasks" / "in_review" / "TASK-001.md"

    assert not in_progress_file.exists()
    assert in_review_file.exists()
```

**Benefits**:
- ✅ Automatic cleanup (pytest handles it)
- ✅ Isolated per test
- ✅ Works on all platforms

---

## Implementation Order

### Priority 1: Core Workflows (Days 1-2)

**Estimated Time**: 8 hours

1. **`workflow_fixtures.py`** (2 hours)
   - Core fixtures needed by all tests
   - Blocking dependency for all test files

2. **`test_workflow_auto_proceed.py`** (1.5 hours)
   - Simplest workflow
   - Tests basic integration
   - Validates fixture architecture

3. **`test_workflow_quick_timeout.py`** (2 hours)
   - Tests mock timer strategy
   - Validates countdown mocking
   - Important performance baseline

4. **`assertion_helpers.py`** (1.5 hours)
   - Validation utilities
   - Used by all tests
   - Centralizes common assertions

5. **`workflow_builders.py`** (1 hour)
   - Scenario builders
   - Simplifies complex test setup

### Priority 2: User Interaction Workflows (Days 3-4)

**Estimated Time**: 7.5 hours

6. **`test_workflow_quick_escalation.py`** (2 hours)
   - Tests user input mocking
   - Validates escalation flow

7. **`test_workflow_full_approval.py`** (2.5 hours)
   - Tests full review display
   - Input validation testing

8. **`test_workflow_qa_mode.py`** (1.5 hours)
   - Q&A session testing
   - Session persistence

9. **`test_workflow_force_override.py`** (1 hour)
   - Force trigger testing
   - Simple but important

10. **`conftest.py`** (0.5 hours)
    - Integration configuration
    - Markers and hooks

### Priority 3: Advanced Workflows (Day 5)

**Estimated Time**: 3 hours

11. **`test_workflow_modification_loop.py`** (3 hours)
    - Most complex workflow
    - Tests modification session
    - Versioning and re-review

---

## Risk Mitigation

### Risk 1: Missing Dependencies

**Risk**: `modification_session.py`, `qa_manager.py`, `version_manager.py` may not exist.

**Mitigation**:
1. **Verify existence first**:
   ```bash
   ls installer/global/commands/lib/modification_session.py
   ls installer/global/commands/lib/qa_manager.py
   ls installer/global/commands/lib/version_manager.py
   ```

2. **If missing, create stubs**:
   ```python
   # tests/helpers/module_stubs.py
   class ModificationSessionStub:
       """Stub for missing ModificationSession."""
       def __init__(self, plan, task_id, user_name):
           self.plan = plan
           self.task_id = task_id

       def start(self): pass
       def end(self, save): pass
   ```

3. **Use conditional imports**:
   ```python
   try:
       from modification_session import ModificationSession
   except ImportError:
       from tests.helpers.module_stubs import ModificationSessionStub as ModificationSession
   ```

**Impact**: Low (can test with stubs initially)

### Risk 2: Performance Degradation

**Risk**: Tests may run slower than expected.

**Mitigation**:
1. **Monitor execution time** with `workflow_metrics`
2. **Parallelize with pytest-xdist**:
   ```bash
   pytest tests/integration/ -n auto
   ```
3. **Mark slow tests**:
   ```python
   @pytest.mark.slow
   def test_complex_workflow(): ...
   ```

**Impact**: Medium (affects developer experience)

### Risk 3: Flaky Tests

**Risk**: Tests may be non-deterministic due to timing issues.

**Mitigation**:
1. **Use mocks exclusively** for timing
2. **Avoid actual time.sleep()** calls
3. **Mock threading.Timer** completely
4. **Deterministic input sequences**

**Impact**: High (flaky tests destroy confidence)

---

## Time Estimates

### Per-File Estimates

| File | Lines | Tests | Time (hrs) | Priority |
|------|-------|-------|------------|----------|
| `workflow_fixtures.py` | 350 | 6 fixtures | 2.0 | P1 |
| `assertion_helpers.py` | 300 | N/A | 1.5 | P1 |
| `workflow_builders.py` | 350 | N/A | 2.0 | P1 |
| `test_workflow_auto_proceed.py` | 280 | 6 | 1.5 | P1 |
| `test_workflow_quick_timeout.py` | 380 | 8 | 2.0 | P1 |
| `test_workflow_quick_escalation.py` | 400 | 8 | 2.0 | P2 |
| `test_workflow_full_approval.py` | 500 | 10 | 2.5 | P2 |
| `test_workflow_modification_loop.py` | 600 | 12 | 3.0 | P3 |
| `test_workflow_qa_mode.py` | 320 | 6 | 1.5 | P2 |
| `test_workflow_force_override.py` | 240 | 4 | 1.0 | P2 |
| `conftest.py` | 150 | N/A | 0.5 | P2 |
| **TOTAL** | **3,870** | **54** | **19.5** | |

### Daily Breakdown (5-Day Plan)

- **Day 1** (4 hours): Fixtures + auto-proceed + timeout tests
- **Day 2** (4 hours): Escalation + full approval tests
- **Day 3** (4 hours): Q&A mode + force override tests
- **Day 4** (4 hours): Modification loop workflow
- **Day 5** (3.5 hours): Integration, debugging, documentation

**Total**: 19.5 hours across 5 days

---

## Success Criteria

### Functional Success ✅

- [ ] All 54 integration tests pass
- [ ] All 7 workflows tested end-to-end
- [ ] State transitions verified (backlog → in_progress → in_review)
- [ ] User interactions tested (timeout, escalation, approval, cancel)
- [ ] File operations verified (task file movement, metadata updates)

### Performance Success ✅

- [ ] Auto-proceed workflow: <2 seconds
- [ ] Quick review workflows: <2 seconds each
- [ ] Full review workflows: <3 seconds each
- [ ] Modification workflow: <5 seconds
- [ ] Total suite: <5 minutes (300 seconds)

### Coverage Success ✅

- [ ] Line coverage: ≥80%
- [ ] Branch coverage: ≥75%
- [ ] All critical paths tested
- [ ] All error conditions tested

---

## Conclusion

This implementation plan provides a comprehensive, Python-specific approach to building the Phase 2 Integration Test Suite using pytest best practices. The plan:

✅ **Builds on Phase 1 infrastructure** (fixtures, mocks, coverage config)
✅ **Leverages pytest-mock** for clean mocking patterns
✅ **Uses AAA pattern** consistently
✅ **Implements fast tests** with mock timers (no actual delays)
✅ **Provides clear implementation order** (Priority 1-3)
✅ **Includes detailed examples** and patterns
✅ **Estimates realistic timelines** (19.5 hours total)
✅ **Mitigates key risks** (missing deps, flaky tests, coverage gaps)

**Ready for implementation**: All architectural decisions made, patterns established, and dependencies identified.

---

**Plan Status**: ✅ **READY FOR IMPLEMENTATION**
**Estimated Delivery**: 5 days (19.5 hours)
**Risk Level**: Low (clear plan, proven patterns, Phase 1 precedent)
**Quality Confidence**: High (comprehensive coverage, performance targets, isolation)

---

*Implementation plan generated: 2025-10-10*
*Next action: Begin Priority 1 implementation (workflow_fixtures.py)*
