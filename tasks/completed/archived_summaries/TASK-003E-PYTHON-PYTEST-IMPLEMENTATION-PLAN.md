# TASK-003E Python/Pytest Implementation Plan

**Date**: 2025-10-10
**Task**: TASK-003E - Comprehensive Testing & Documentation
**Stack**: Python with pytest testing framework
**Current Status**: Phase 1 Complete (25%), Phase 2 Ready to Start
**Estimated Total Effort**: 8-10 days (Phase 1 complete in 1 day, 7-9 days remaining)

---

## Executive Summary

This implementation plan provides a detailed, phase-by-phase approach to implementing comprehensive testing and documentation for the complexity-based plan review system using Python and pytest. Phase 1 (Infrastructure) is complete with 45+ tests passing. This plan focuses on Phases 2-4, building on the solid foundation established.

**Key Success Factors**:
- ✅ Proven infrastructure from Phase 1 (2x faster than estimated)
- ✅ Clear fixture patterns established (data_fixtures.py, mock_fixtures.py)
- ✅ Centralized coverage configuration (coverage_config.py)
- ✅ Architectural recommendations already applied
- 🔄 Dependency verification needed before Phase 2 start

---

## Table of Contents

1. [Phase-by-Phase Overview](#phase-by-phase-overview)
2. [File Structure & Organization](#file-structure--organization)
3. [Test Strategy by Phase](#test-strategy-by-phase)
4. [Mock & Fixture Architecture](#mock--fixture-architecture)
5. [Documentation Structure](#documentation-structure)
6. [Component Dependencies](#component-dependencies)
7. [Implementation Order](#implementation-order)
8. [Effort Estimates](#effort-estimates)
9. [Risk Mitigation](#risk-mitigation)
10. [Quality Gates](#quality-gates)

---

## Phase-by-Phase Overview

### Phase 1: Infrastructure ✅ COMPLETE
**Duration**: 1 day (Actual)
**Status**: ✅ COMPLETE
**Deliverables**:
- ✅ Test data fixtures (11 fixtures)
- ✅ Mock object fixtures (10 mocks)
- ✅ Coverage configuration (single source of truth)
- ✅ Unit tests for complexity calculation (45+ tests)
- ✅ Zero blocking issues

**Coverage Achieved**:
- Expected: ≥95% for complexity_calculator.py
- Test count: 45+ unit tests
- Execution time: ~0.22s (fast)

---

### Phase 2: Core Testing (Unit & Integration)
**Duration**: 4-5 days (Estimated)
**Status**: 🔄 READY TO START
**Goal**: 765+ unit tests, 105+ integration tests, 90%+ unit coverage

**Sub-Phases**:

#### Phase 2A: Review Mode Testing (Days 2-3)
**Files**:
1. `tests/unit/test_review_modes_quick.py` (60+ tests)
2. `tests/unit/test_review_modes_full.py` (100+ tests)
3. `tests/unit/test_mode_selector.py` (45+ tests)

**Coverage Target**: ≥92% for review mode modules

**Test Categories**:
- **Quick Mode Handler**:
  - Summary card display format
  - Countdown timer (5 seconds default)
  - Auto-proceed after timeout
  - Optional human review flow
  - Escalation to full review
  - User cancellation

- **Full Mode Handler**:
  - Comprehensive plan display
  - Section-by-section review
  - Modification request flow
  - Q&A interaction flow
  - Approval/rejection flow
  - Re-evaluation after changes

- **Mode Selector**:
  - Score-to-mode routing logic
  - Threshold boundary testing (3, 4, 6, 7)
  - Force trigger override logic
  - Multiple trigger handling

#### Phase 2B: Force Trigger & Template Testing (Day 3)
**Files**:
1. `tests/unit/test_force_triggers.py` (40+ tests)
2. `tests/unit/test_plan_templates.py` (90+ tests)

**Coverage Target**: ≥90% for trigger and template modules

**Test Categories**:
- **Force Triggers**:
  - USER_FLAG detection (--review-plan)
  - SECURITY_KEYWORDS detection (auth, crypto, token)
  - SCHEMA_CHANGES detection (migration, alter table)
  - BREAKING_CHANGES detection (remove endpoint, change contract)
  - HOTFIX detection (task metadata)
  - Multiple triggers simultaneously
  - Trigger priority/override logic

- **Plan Templates**:
  - Auto-proceed template (summary card)
  - Quick review template (summary + countdown)
  - Full review template (comprehensive)
  - Section rendering (markdown validity)
  - Phase generation
  - Risk section formatting
  - Checkpoint section formatting
  - Missing data graceful handling

#### Phase 2C: Metrics & Complexity Factors (Day 4)
**Files**:
1. `tests/unit/test_metrics_collector.py` (55+ tests)
2. `tests/unit/test_complexity_factors.py` (50+ tests)

**Coverage Target**: ≥93% for factors, ≥90% for metrics

**Test Categories**:
- **Metrics Collection**:
  - Countdown metrics (time remaining, interruptions)
  - Decision metrics (approve, reject, modify, cancel)
  - Performance metrics (calculation time, rendering time)
  - Persistence (file storage, JSON format)
  - Retrieval (load by task_id, date range)
  - Reporting (aggregation, trends)

- **Complexity Factors**:
  - File count factor (0-10 scale)
  - File size factor (LOC estimation)
  - Pattern complexity factor (new vs familiar)
  - External dependency factor (API, DB, services)
  - Risk indicator factor (auth, payment, crypto)
  - Technology stack factor (Python, TypeScript, etc.)
  - Factor evaluation error handling
  - Factor weight configuration

#### Phase 2D: Integration Testing (Day 5)
**Files**:
1. `tests/integration/test_complexity_to_review.py` (40+ tests)
2. `tests/integration/test_review_workflows.py` (35+ tests)
3. `tests/integration/test_modification_loop.py` (30+ tests)

**Coverage Target**: ≥80% line, ≥75% branch

**Integration Scenarios**:
- **Complexity → Review Routing**:
  - Score 1-3 → Auto-proceed flow
  - Score 4-6 → Quick optional flow
  - Score 7-10 → Full required flow
  - Force trigger → Full required override
  - Boundary score routing (3→4, 6→7)

- **Complete Workflows**:
  - Auto-proceed: Calculate → Display → Proceed (1s)
  - Quick review: Calculate → Display → Countdown → Proceed (5s)
  - Full review: Calculate → Display → Review → Approve → Proceed
  - Escalation: Quick → User interrupt → Full review
  - Modification: Full → Request changes → Re-calculate → Review

- **Modification Loop**:
  - Request modification
  - Q&A session
  - Re-evaluation of complexity
  - Plan regeneration
  - Second review cycle
  - Approval after changes
  - Cancellation flow

---

### Phase 3: E2E & Documentation (Days 6-8)
**Duration**: 3 days (Estimated)
**Status**: ⏳ PENDING (starts after Phase 2)
**Goal**: 60+ E2E scenarios, 12 documentation files

**Sub-Phases**:

#### Phase 3A: E2E BDD Scenarios (Days 6-7)
**Files**:
1. `tests/e2e/simple_task.feature` + `test_simple_task_flow.py` (15 scenarios)
2. `tests/e2e/complex_task.feature` + `test_complex_task_flow.py` (20 scenarios)
3. `tests/e2e/edge_cases.feature` + `test_multi_mode_scenarios.py` (25 scenarios)

**Coverage Target**: ≥70% line, ≥65% branch

**BDD Scenarios**:
- **Simple Task Flow** (15 scenarios):
  ```gherkin
  Feature: Simple Task Processing
    Scenario: Low complexity task auto-proceeds
      Given a task with complexity score of 2
      And no force review triggers
      When the plan review phase starts
      Then the system displays summary card
      And auto-proceeds to Phase 3 within 1 second
      And no user interaction required
  ```

- **Complex Task Flow** (20 scenarios):
  ```gherkin
  Feature: Complex Task Processing
    Scenario: High complexity requires full review
      Given a task with complexity score of 8
      When the plan review phase starts
      Then the system displays comprehensive plan
      And waits for human review decision
      And allows plan modification requests
      And supports Q&A session
  ```

- **Multi-Mode Scenarios** (25 scenarios):
  - Escalation from quick to full review
  - De-escalation (not supported, should error)
  - Cancellation at any stage
  - Timeout behavior
  - Multiple modification rounds
  - Force trigger override
  - Concurrent review sessions

#### Phase 3B: User Documentation (Day 7)
**Files** (6 files, ~11,500 words):
1. `docs/user-guides/01-getting-started.md` (~2000 words)
   - Installation and setup
   - First complexity review (walkthrough)
   - Understanding the output
   - Common workflows
   - Quick reference

2. `docs/user-guides/02-understanding-complexity.md` (~2500 words)
   - Complexity scoring explained
   - Factor breakdown
   - Score ranges and thresholds
   - Review mode mapping
   - Examples by complexity level

3. `docs/user-guides/03-review-modes-guide.md` (~2000 words)
   - Auto-proceed mode (1-3)
   - Quick optional mode (4-6)
   - Full required mode (7-10)
   - Force triggers
   - User interactions

4. `docs/user-guides/04-plan-interpretation.md` (~1500 words)
   - Reading implementation plans
   - Phase breakdown
   - Risk assessment
   - Checkpoints
   - Recommendations

5. `docs/user-guides/05-metrics-dashboard.md` (~1500 words)
   - Available metrics
   - Viewing reports
   - Trend analysis
   - Performance data

6. `docs/user-guides/06-troubleshooting.md` (~1500 words)
   - Common issues
   - Debug commands
   - Error messages
   - Getting help

#### Phase 3C: Developer Documentation (Day 8)
**Files** (6 files, ~14,300 words):
1. `docs/developer-guides/01-architecture-overview.md` (~2500 words)
   - System architecture
   - Component interactions
   - Data flow
   - Technology stack
   - Design decisions

2. `docs/developer-guides/02-complexity-engine.md` (~3000 words)
   - Factor evaluation
   - Score aggregation
   - Force trigger detection
   - Review mode routing
   - Fail-safe logic
   - Extending factors

3. `docs/developer-guides/03-planning-system.md` (~2500 words)
   - Plan parsing
   - Template rendering
   - Phase generation
   - Checkpoint logic
   - Customizing templates

4. `docs/developer-guides/04-extension-points.md` (~2000 words)
   - Adding complexity factors
   - Custom review modes
   - Template customization
   - Metrics extension
   - Integration hooks

5. `docs/developer-guides/05-testing-guide.md` (~2500 words)
   - Test organization
   - Fixture usage
   - Mock strategy
   - Coverage targets
   - Running tests
   - Writing new tests

6. `docs/developer-guides/06-contributing.md` (~1500 words)
   - Code standards
   - PR process
   - Quality gates
   - Documentation requirements
   - Review checklist

---

### Phase 4: Validation & Production (Days 9-10)
**Duration**: 2 days (Estimated)
**Status**: ⏳ PENDING (starts after Phase 3)
**Goal**: Production-ready with CI/CD, validation, security audit

**Sub-Phases**:

#### Phase 4A: Automation & CI/CD (Day 9)
**Deliverables**:
1. `.github/workflows/test.yml` - Test execution workflow
2. `.github/workflows/docs.yml` - Documentation validation
3. `.pre-commit-config.yaml` - Pre-commit hooks
4. `scripts/validate_docs.py` - Documentation validation script
5. `requirements.txt` - Test dependencies
6. `pytest.ini` - Pytest configuration (generated from coverage_config.py)

**CI/CD Workflow**:
```yaml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest -v --cov --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

**Pre-commit Hooks**:
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
  - repo: local
    hooks:
      - id: pytest-coverage
        name: pytest coverage check
        entry: pytest --cov --cov-fail-under=85
        language: system
        pass_filenames: false
      - id: validate-docs
        name: validate documentation
        entry: python scripts/validate_docs.py
        language: system
        files: ^docs/.*\.md$
```

**Documentation Validation Script**:
- Check for broken links
- Validate code examples compile
- Verify table of contents
- Check freshness timestamps
- Cross-reference validation

#### Phase 4B: Performance & Security (Day 10)
**Deliverables**:
1. `tests/performance/test_complexity_benchmarks.py`
2. `tests/performance/test_planning_benchmarks.py`
3. Security audit report
4. Performance benchmark report
5. Final QA sign-off

**Performance Benchmarks**:
```python
import pytest

@pytest.mark.benchmark
def test_complexity_calculation_performance(benchmark, complexity_calculator, context):
    """Complexity calculation should complete in <1s (95th percentile)."""
    result = benchmark(complexity_calculator.calculate, context)

    # Performance targets
    assert benchmark.stats['mean'] < 0.5  # 500ms mean
    assert benchmark.stats['stddev'] < 0.1  # Low variance
    assert result.total_score >= 1  # Valid result
```

**Performance Targets**:
- Complexity calculation: <1s (95th percentile)
- Plan generation: <5s (95th percentile)
- Countdown timer: 100ms ± 50ms update interval
- Metrics write: <50ms (99th percentile)

**Security Checks**:
```bash
# Run security scanners
bandit -r installer/global/commands/lib/
safety check
pip-audit
```

---

## File Structure & Organization

### Test Directory Structure
```
tests/
├── __init__.py
├── conftest.py                                  # Shared pytest configuration
├── coverage_config.py                           # ✅ Coverage configuration (Phase 1)
│
├── fixtures/                                    # ✅ Test fixtures (Phase 1)
│   ├── __init__.py
│   ├── data_fixtures.py                        # ✅ Test data (11 fixtures)
│   └── mock_fixtures.py                        # ✅ Mock objects (10 mocks)
│
├── unit/                                        # Unit tests (≥90% coverage)
│   ├── __init__.py
│   ├── test_complexity_calculation_comprehensive.py  # ✅ Phase 1 (45+ tests)
│   ├── test_complexity_factors.py              # 🔄 Phase 2C (50+ tests)
│   ├── test_review_modes_quick.py              # 🔄 Phase 2A (60+ tests)
│   ├── test_review_modes_full.py               # 🔄 Phase 2A (100+ tests)
│   ├── test_mode_selector.py                   # 🔄 Phase 2A (45+ tests)
│   ├── test_force_triggers.py                  # 🔄 Phase 2B (40+ tests)
│   ├── test_plan_templates.py                  # 🔄 Phase 2B (90+ tests)
│   └── test_metrics_collector.py               # 🔄 Phase 2C (55+ tests)
│
├── integration/                                 # Integration tests (≥80% coverage)
│   ├── __init__.py
│   ├── test_complexity_to_review.py            # 🔄 Phase 2D (40+ tests)
│   ├── test_review_workflows.py                # 🔄 Phase 2D (35+ tests)
│   └── test_modification_loop.py               # 🔄 Phase 2D (30+ tests)
│
├── e2e/                                         # E2E tests (≥70% coverage)
│   ├── __init__.py
│   ├── simple_task.feature                     # ⏳ Phase 3A (BDD scenarios)
│   ├── test_simple_task_flow.py                # ⏳ Phase 3A (15 scenarios)
│   ├── complex_task.feature
│   ├── test_complex_task_flow.py               # ⏳ Phase 3A (20 scenarios)
│   ├── edge_cases.feature
│   └── test_multi_mode_scenarios.py            # ⏳ Phase 3A (25 scenarios)
│
├── edge_cases/                                  # Edge case tests (100% coverage)
│   ├── __init__.py
│   ├── test_boundary_conditions.py             # 🔄 Phase 2 (50+ tests)
│   ├── test_error_scenarios.py                 # 🔄 Phase 2 (40+ tests)
│   └── test_concurrent_execution.py            # 🔄 Phase 2 (30+ tests)
│
└── performance/                                 # Performance benchmarks
    ├── __init__.py
    ├── test_complexity_benchmarks.py           # ⏳ Phase 4B
    ├── test_planning_benchmarks.py             # ⏳ Phase 4B
    └── test_metrics_benchmarks.py              # ⏳ Phase 4B
```

### Documentation Directory Structure
```
docs/
├── user-guides/                                 # End-user documentation
│   ├── 01-getting-started.md                  # ⏳ Phase 3B (~2000 words)
│   ├── 02-understanding-complexity.md          # ⏳ Phase 3B (~2500 words)
│   ├── 03-review-modes-guide.md                # ⏳ Phase 3B (~2000 words)
│   ├── 04-plan-interpretation.md               # ⏳ Phase 3B (~1500 words)
│   ├── 05-metrics-dashboard.md                 # ⏳ Phase 3B (~1500 words)
│   └── 06-troubleshooting.md                   # ⏳ Phase 3B (~1500 words)
│
├── developer-guides/                            # Developer documentation
│   ├── 01-architecture-overview.md            # ⏳ Phase 3C (~2500 words)
│   ├── 02-complexity-engine.md                 # ⏳ Phase 3C (~3000 words)
│   ├── 03-planning-system.md                   # ⏳ Phase 3C (~2500 words)
│   ├── 04-extension-points.md                  # ⏳ Phase 3C (~2000 words)
│   ├── 05-testing-guide.md                     # ⏳ Phase 3C (~2500 words)
│   └── 06-contributing.md                      # ⏳ Phase 3C (~1500 words)
│
├── api/                                         # API reference (auto-generated)
│   ├── complexity-api.md                       # ⏳ Phase 3 (from docstrings)
│   └── planning-api.md                         # ⏳ Phase 3 (from docstrings)
│
├── configuration/                               # Configuration guides
│   ├── configuration-reference.md              # ⏳ Phase 3
│   └── complexity-thresholds.md                # ⏳ Phase 3
│
└── adr/                                         # Architecture Decision Records
    ├── 001-complexity-scoring-algorithm.md     # ⏳ Phase 3
    ├── 002-review-mode-thresholds.md           # ⏳ Phase 3
    ├── 003-force-trigger-strategy.md           # ⏳ Phase 3
    └── 004-test-infrastructure-design.md       # ⏳ Phase 3
```

### Production Code Structure (for reference)
```
installer/global/commands/lib/
├── complexity_calculator.py                     # ✅ Core calculation engine
├── complexity_models.py                         # ✅ Data models
├── complexity_factors.py                        # ⚠️ VERIFY BEFORE PHASE 2
├── review_modes.py                              # ⚠️ VERIFY BEFORE PHASE 2
├── plan_templates.py                            # ⚠️ VERIFY BEFORE PHASE 2
├── metrics_collector.py                         # ⚠️ VERIFY BEFORE PHASE 2
├── countdown_timer.py                           # ⚠️ VERIFY BEFORE PHASE 2
└── user_interaction.py                          # ⚠️ VERIFY BEFORE PHASE 2
```

---

## Test Strategy by Phase

### Unit Testing Strategy

#### Pytest Best Practices Applied
```python
# 1. Use descriptive test names
def test_auto_proceed_for_score_below_threshold():
    """Should route to AUTO_PROCEED mode when score is 1-3."""
    pass

# 2. Use fixtures for test data
@pytest.fixture
def simple_task_context(simple_task_data):
    """Create evaluation context for simple task."""
    return EvaluationContext(
        task_id="TASK-001",
        technology_stack="Python",
        implementation_plan=simple_task_data
    )

# 3. Parametrize for multiple cases
@pytest.mark.parametrize("score,expected_mode", [
    (1, ReviewMode.AUTO_PROCEED),
    (3, ReviewMode.AUTO_PROCEED),
    (4, ReviewMode.QUICK_OPTIONAL),
    (6, ReviewMode.QUICK_OPTIONAL),
    (7, ReviewMode.FULL_REQUIRED),
    (10, ReviewMode.FULL_REQUIRED),
])
def test_review_mode_routing(score, expected_mode, calculator):
    mode = calculator._determine_review_mode(score, [])
    assert mode == expected_mode

# 4. Use markers for organization
@pytest.mark.unit
@pytest.mark.complexity
def test_complexity_calculation():
    pass

# 5. Mock external dependencies
def test_metrics_persistence(mock_file_system):
    collector = MetricsCollector(file_system=mock_file_system)
    collector.save_metric("test", {"value": 42})
    assert mock_file_system.exists("metrics/test.json")

# 6. Use tmp_path for file isolation
def test_metrics_storage(tmp_path):
    metrics_dir = tmp_path / "metrics"
    collector = MetricsCollector(metrics_dir=metrics_dir)
    # Test uses real filesystem but isolated
```

#### Coverage Strategy
```python
# Use coverage_config.py helpers
from tests.coverage_config import (
    get_target_for_test_type,
    validate_coverage,
    format_coverage_report
)

def test_coverage_meets_targets():
    """Verify test coverage meets targets."""
    coverage_data = {
        'line': 92.5,
        'branch': 88.3,
        'function': 95.0
    }

    assert validate_coverage(coverage_data, 'unit')

    report = format_coverage_report(coverage_data)
    print(report)
```

### Integration Testing Strategy

#### Integration Test Patterns
```python
# 1. Test component interactions
@pytest.mark.integration
def test_complexity_to_review_flow():
    """Test complete flow from complexity calculation to review mode."""
    # Given: A task with medium complexity
    calculator = ComplexityCalculator()
    review_handler = ReviewModeHandler()

    context = create_medium_complexity_context()

    # When: Calculate complexity and route to review
    score = calculator.calculate(context)
    review_result = review_handler.handle(score)

    # Then: Should route to quick optional mode
    assert score.review_mode == ReviewMode.QUICK_OPTIONAL
    assert review_result.displayed_summary
    assert review_result.countdown_started

# 2. Test state transitions
@pytest.mark.integration
def test_modification_loop_workflow():
    """Test complete modification loop."""
    workflow = ComplexityReviewWorkflow()

    # Initial review
    initial_result = workflow.start_review(task_id="TASK-001")
    assert initial_result.state == "REVIEWING"

    # Request modification
    mod_result = workflow.request_modification(
        task_id="TASK-001",
        reason="Need more detail on error handling"
    )
    assert mod_result.state == "MODIFYING"

    # Complete modification
    final_result = workflow.complete_modification(
        task_id="TASK-001",
        updated_plan=new_plan
    )
    assert final_result.state == "REVIEWING"
    assert final_result.complexity_recalculated

# 3. Test error propagation
@pytest.mark.integration
def test_error_handling_across_components():
    """Verify errors propagate correctly through workflow."""
    workflow = ComplexityReviewWorkflow()

    # Simulate calculation error
    with patch('complexity_calculator.ComplexityCalculator.calculate') as mock_calc:
        mock_calc.side_effect = Exception("Calculation failed")

        result = workflow.start_review(task_id="TASK-001")

        # Should create fail-safe score
        assert result.complexity_score.total_score == 10
        assert result.complexity_score.metadata['failsafe'] is True
        assert result.review_mode == ReviewMode.FULL_REQUIRED
```

### E2E Testing Strategy (BDD)

#### BDD Scenario Structure
```gherkin
# File: tests/e2e/simple_task.feature

Feature: Simple Task Processing
  As a developer
  I want low-complexity tasks to auto-proceed
  So that I can implement quickly without interruption

  Background:
    Given the complexity review system is initialized
    And the task file exists with valid metadata

  Scenario: Auto-proceed for very simple task
    Given a task with the following characteristics:
      | File count | 1 |
      | Patterns   | Familiar CRUD |
      | Dependencies | 0 |
      | LOC estimate | 50 |
    When the complexity is calculated
    Then the complexity score should be 2
    And the review mode should be "auto_proceed"
    And the system should display a summary card
    And the system should auto-proceed within 1 second
    And no user interaction should be required

  Scenario: Boundary case - score exactly 3
    Given a task with complexity score of exactly 3
    When the plan review phase starts
    Then the review mode should be "auto_proceed"
    And the system should proceed automatically

  Scenario: Error in calculation - fail-safe
    Given a task with invalid metadata
    When the complexity calculation fails
    Then the system should create a fail-safe score of 10
    And the review mode should be "full_required"
    And an error should be logged
```

#### Step Implementation
```python
# File: tests/e2e/test_simple_task_flow.py

from pytest_bdd import scenarios, given, when, then, parsers
import pytest

scenarios('simple_task.feature')

@given('the complexity review system is initialized')
def complexity_system():
    """Initialize the complexity review system."""
    return ComplexityReviewSystem()

@given(parsers.parse('a task with complexity score of exactly {score:d}'))
def task_at_boundary(score):
    """Create task data with specific score."""
    return create_task_with_score(score)

@when('the complexity is calculated')
def calculate_complexity(complexity_system, task_data):
    """Calculate complexity for the task."""
    context = EvaluationContext(
        task_id="E2E-001",
        technology_stack="Python",
        implementation_plan=task_data
    )
    return complexity_system.calculate(context)

@then(parsers.parse('the complexity score should be {expected_score:d}'))
def verify_score(calculation_result, expected_score):
    """Verify calculated score matches expected."""
    assert calculation_result.total_score == expected_score

@then(parsers.parse('the review mode should be "{expected_mode}"'))
def verify_review_mode(calculation_result, expected_mode):
    """Verify review mode matches expected."""
    expected_enum = ReviewMode(expected_mode)
    assert calculation_result.review_mode == expected_enum
```

---

## Mock & Fixture Architecture

### Fixture Hierarchy
```
conftest.py (root)
├── Session-scoped fixtures
│   ├── test_data_dir (tmp_path_factory)
│   └── coverage_config
│
├── Module-scoped fixtures
│   ├── complexity_calculator (default instance)
│   └── review_handler (default instance)
│
└── Function-scoped fixtures (from data_fixtures.py, mock_fixtures.py)
    ├── simple_task_data
    ├── medium_task_data
    ├── complex_task_data
    ├── mock_file_system
    ├── mock_task_context
    └── ... (21 total fixtures)
```

### Conftest Configuration
```python
# File: tests/conftest.py

import pytest
import sys
from pathlib import Path

# Add installer lib to path
installer_lib_path = Path(__file__).parent.parent / "installer" / "global" / "commands" / "lib"
sys.path.insert(0, str(installer_lib_path))

# Import all fixtures
pytest_plugins = [
    "tests.fixtures.data_fixtures",
    "tests.fixtures.mock_fixtures",
]

@pytest.fixture(scope="session")
def test_data_dir(tmp_path_factory):
    """Session-scoped temporary directory for test data."""
    return tmp_path_factory.mktemp("test_data")

@pytest.fixture(scope="session")
def coverage_config():
    """Load coverage configuration."""
    from tests.coverage_config import COVERAGE_TARGETS, MINIMUM_TOTAL_COVERAGE
    return {
        'targets': COVERAGE_TARGETS,
        'minimum': MINIMUM_TOTAL_COVERAGE
    }

@pytest.fixture
def complexity_calculator():
    """Create ComplexityCalculator instance with default factors."""
    from complexity_calculator import ComplexityCalculator
    return ComplexityCalculator()

@pytest.fixture
def review_handler():
    """Create ReviewModeHandler instance."""
    from review_modes import ReviewModeHandler
    return ReviewModeHandler()

# Markers
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "edge_case: Edge case tests")
    config.addinivalue_line("markers", "slow: Slow-running tests")
    config.addinivalue_line("markers", "benchmark: Performance benchmarks")
```

### Mock Strategy

#### When to Mock
✅ **DO Mock**:
- External APIs and services
- File system operations (use mock_file_system)
- Network calls
- Database queries
- User input (use mock_user_input)
- Time-based operations (use mock_countdown_timer)
- System clock (use freezegun)

❌ **DON'T Mock**:
- Core calculation logic (test real implementation)
- Data models (use real dataclasses)
- Pure functions (test real implementation)
- Simple utilities (test real implementation)

#### Mock Examples
```python
# Good: Mock external dependencies
def test_metrics_save_to_file(mock_file_system):
    collector = MetricsCollector(file_system=mock_file_system)
    collector.save_metric("test", {"value": 42})
    assert mock_file_system.exists("metrics/test.json")

# Good: Mock user interaction
def test_review_approval(mock_user_input):
    mock_user_input.set_sequence(["y", "approve"])
    handler = FullReviewHandler(user_input=mock_user_input)
    result = handler.handle_review(score)
    assert result.action == "approved"

# Bad: Don't mock core logic
def test_complexity_calculation():
    # DON'T do this:
    # mock_calculator = Mock()
    # mock_calculator.calculate.return_value = ComplexityScore(...)

    # DO this:
    calculator = ComplexityCalculator()  # Real implementation
    result = calculator.calculate(context)  # Test real behavior
```

---

## Documentation Structure

### Documentation Template
```markdown
# [Document Title]

**Last Updated**: 2025-10-10
**Status**: Draft | Review | Published
**Audience**: User | Developer | Both

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Main Content](#main-content)
4. [Common Pitfalls](#common-pitfalls)
5. [Related Documentation](#related-documentation)

---

## Overview

Brief 2-3 sentence description of what this document covers.

**What you'll learn**:
- Key concept 1
- Key concept 2
- Key concept 3

**Estimated reading time**: X minutes

---

## Prerequisites

Before reading this guide, you should:
- Have prerequisite 1
- Understand prerequisite 2
- Complete prerequisite 3

---

## Main Content

### Section 1

Content with:
- Code examples
- Diagrams (ASCII art or mermaid)
- Tables
- Numbered steps

### Section 2

...

---

## Common Pitfalls

### Pitfall 1: Description
**Problem**: What goes wrong
**Solution**: How to fix it
**Prevention**: How to avoid it

---

## Related Documentation

- [Related Doc 1](../path/to/doc1.md)
- [Related Doc 2](../path/to/doc2.md)

---

## Changelog

| Date | Change | Author |
|------|--------|--------|
| 2025-10-10 | Initial version | Author Name |

---

*This document is part of the TASK-003E documentation suite.*
```

### API Documentation (Auto-Generated)

#### Using Sphinx
```bash
# Install Sphinx
pip install sphinx sphinx-rtd-theme

# Generate API docs
sphinx-apidoc -o docs/api installer/global/commands/lib

# Build HTML docs
cd docs
make html
```

#### Docstring Format (Google Style)
```python
def calculate_complexity(context: EvaluationContext) -> ComplexityScore:
    """Calculate complexity score for a task implementation plan.

    This function evaluates multiple complexity factors and aggregates
    them into a single score (1-10 scale). It also detects force-review
    triggers and determines the appropriate review mode.

    Args:
        context: Evaluation context containing task details, technology stack,
            implementation plan, and user flags.

    Returns:
        ComplexityScore object containing:
            - total_score (int): Aggregated complexity score (1-10)
            - factor_scores (List[FactorScore]): Individual factor scores
            - forced_review_triggers (List[ForceReviewTrigger]): Active triggers
            - review_mode (ReviewMode): Determined review mode
            - calculation_timestamp (datetime): When calculated
            - metadata (Dict): Additional context

    Raises:
        ValueError: If context is invalid or missing required fields.
        CalculationError: If factor evaluation fails critically.

    Example:
        >>> context = EvaluationContext(
        ...     task_id="TASK-001",
        ...     technology_stack="Python",
        ...     implementation_plan=plan
        ... )
        >>> score = calculate_complexity(context)
        >>> print(f"Score: {score.total_score}, Mode: {score.review_mode}")
        Score: 5, Mode: ReviewMode.QUICK_OPTIONAL

    Note:
        If calculation fails, a fail-safe score of 10 (full review) is
        returned to ensure safety. The error is logged and included in
        the metadata with 'failsafe': True.

    See Also:
        - :func:`_evaluate_factors`: Individual factor evaluation
        - :func:`_aggregate_scores`: Score aggregation logic
        - :func:`_determine_review_mode`: Review mode routing
    """
    pass
```

---

## Component Dependencies

### Dependency Graph
```
┌─────────────────────────────────────────────┐
│         ComplexityCalculator                │
│  (complexity_calculator.py)                 │
└──────────────┬──────────────────────────────┘
               │
               ├─── Depends on ───┐
               │                  │
               ▼                  ▼
┌──────────────────────┐  ┌──────────────────────┐
│  ComplexityFactors   │  │  ComplexityModels    │
│ (complexity_factors  │  │ (complexity_models   │
│  .py)                │  │  .py)                │
└──────────────────────┘  └──────────────────────┘
               │                  │
               │                  │
               ▼                  ▼
┌──────────────────────────────────────────────┐
│         ReviewModeHandler                    │
│  (review_modes.py)                           │
└──────────────┬──────────────────────────────┘
               │
               ├─── Depends on ───┐
               │                  │
               ▼                  ▼
┌──────────────────────┐  ┌──────────────────────┐
│  PlanTemplates       │  │  UserInteraction     │
│ (plan_templates.py)  │  │ (user_interaction    │
│                      │  │  .py)                │
└──────────────────────┘  └──────────────────────┘
               │                  │
               │                  │
               ▼                  ▼
┌──────────────────────────────────────────────┐
│         MetricsCollector                     │
│  (metrics_collector.py)                      │
└──────────────────────────────────────────────┘
```

### Dependency Verification Checklist

**CRITICAL**: Run before starting Phase 2

```bash
# Navigate to project root
cd /Users/richardwoollcott/Projects/appmilla_github/ai-engineer

# Check if critical files exist
echo "Checking critical dependencies..."

files=(
    "installer/global/commands/lib/complexity_calculator.py"
    "installer/global/commands/lib/complexity_models.py"
    "installer/global/commands/lib/complexity_factors.py"
    "installer/global/commands/lib/review_modes.py"
    "installer/global/commands/lib/plan_templates.py"
    "installer/global/commands/lib/metrics_collector.py"
    "installer/global/commands/lib/countdown_timer.py"
    "installer/global/commands/lib/user_interaction.py"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file MISSING"
    fi
done

# List all files in lib directory
echo -e "\nAll files in installer/global/commands/lib/:"
ls -la installer/global/commands/lib/
```

### Dependency Actions

| File | Status | Action if Missing |
|------|--------|-------------------|
| `complexity_calculator.py` | ✅ EXISTS | - |
| `complexity_models.py` | ✅ EXISTS | - |
| `complexity_factors.py` | ⚠️ VERIFY | Skip factor tests, use mocks |
| `review_modes.py` | ⚠️ VERIFY | Skip review mode tests |
| `plan_templates.py` | ⚠️ VERIFY | Skip template tests |
| `metrics_collector.py` | ⚠️ VERIFY | Skip metrics tests |
| `countdown_timer.py` | ⚠️ VERIFY | Use mock timer only |
| `user_interaction.py` | ⚠️ VERIFY | Use mock input only |

---

## Implementation Order

### Day-by-Day Breakdown

#### Day 2: Review Mode Testing (Phase 2A Part 1)
**Morning (4 hours)**:
1. Verify dependencies (complexity_factors.py, review_modes.py)
2. Create `test_mode_selector.py` (45+ tests)
   - Score-to-mode routing
   - Threshold boundaries
   - Force trigger overrides

**Afternoon (4 hours)**:
3. Create `test_review_modes_quick.py` (60+ tests)
   - Summary card display
   - Countdown timer behavior
   - Auto-proceed flow
   - Optional review flow

**Evening (1 hour)**:
4. Run tests, verify coverage ≥90%
5. Update progress tracker

#### Day 3: Review Mode Testing (Phase 2A Part 2) + Templates
**Morning (4 hours)**:
1. Create `test_review_modes_full.py` (100+ tests)
   - Comprehensive display
   - Section-by-section review
   - Modification flow
   - Q&A flow
   - Approval/rejection

**Afternoon (4 hours)**:
2. Create `test_plan_templates.py` (90+ tests)
   - Auto-proceed template
   - Quick review template
   - Full review template
   - Markdown validity
   - Section rendering

**Evening (1 hour)**:
3. Run tests, verify coverage ≥90%

#### Day 4: Force Triggers + Metrics + Factors (Phase 2B + 2C)
**Morning (4 hours)**:
1. Create `test_force_triggers.py` (40+ tests)
   - All 5 trigger types
   - Multiple triggers
   - Override logic

2. Create `test_complexity_factors.py` (50+ tests)
   - File count factor
   - File size factor
   - Pattern complexity
   - Dependencies
   - Risk indicators

**Afternoon (4 hours)**:
3. Create `test_metrics_collector.py` (55+ tests)
   - Countdown metrics
   - Decision metrics
   - Performance metrics
   - Persistence
   - Reporting

**Evening (1 hour)**:
4. Run all unit tests, verify ≥90% coverage

#### Day 5: Integration Testing (Phase 2D)
**Morning (4 hours)**:
1. Create `test_complexity_to_review.py` (40+ tests)
   - Score 1-3 → Auto-proceed
   - Score 4-6 → Quick optional
   - Score 7-10 → Full required
   - Force trigger override

**Afternoon (4 hours)**:
2. Create `test_review_workflows.py` (35+ tests)
   - Complete auto-proceed flow
   - Complete quick review flow
   - Complete full review flow
   - Escalation flow

3. Create `test_modification_loop.py` (30+ tests)
   - Request modification
   - Q&A session
   - Re-calculation
   - Second review

**Evening (1 hour)**:
4. Run all integration tests, verify ≥80% coverage
5. Phase 2 complete, prepare for Phase 3

#### Day 6: E2E Scenarios Part 1 (Phase 3A)
**Morning (4 hours)**:
1. Create `simple_task.feature` (Gherkin)
2. Create `test_simple_task_flow.py` (15 scenarios)
   - Low complexity auto-proceed
   - Boundary cases (score 3)
   - Error handling (fail-safe)

**Afternoon (4 hours)**:
3. Create `complex_task.feature` (Gherkin)
4. Create `test_complex_task_flow.py` (20 scenarios)
   - High complexity full review
   - All review outcomes
   - Modification flow
   - Cancellation flow

**Evening (1 hour)**:
5. Run E2E tests, verify scenarios pass

#### Day 7: E2E Part 2 + User Docs (Phase 3A + 3B)
**Morning (4 hours)**:
1. Create `edge_cases.feature` (Gherkin)
2. Create `test_multi_mode_scenarios.py` (25 scenarios)
   - Escalation
   - Multiple modifications
   - Concurrent reviews
   - Timeout behavior

**Afternoon (4 hours)**:
3. Create user documentation (6 files)
   - `01-getting-started.md`
   - `02-understanding-complexity.md`
   - `03-review-modes-guide.md`

**Evening (1 hour)**:
4. Continue user docs
   - `04-plan-interpretation.md`
   - `05-metrics-dashboard.md`
   - `06-troubleshooting.md`

#### Day 8: Developer Documentation (Phase 3C)
**All Day (8 hours)**:
1. Create developer documentation (6 files)
   - `01-architecture-overview.md`
   - `02-complexity-engine.md`
   - `03-planning-system.md`
   - `04-extension-points.md`
   - `05-testing-guide.md`
   - `06-contributing.md`

**Evening (1 hour)**:
2. Create ADRs (4 files)
3. Create configuration docs (2 files)

#### Day 9: CI/CD & Automation (Phase 4A)
**Morning (4 hours)**:
1. Create `.github/workflows/test.yml`
2. Create `.github/workflows/docs.yml`
3. Create `.pre-commit-config.yaml`
4. Create `requirements.txt`
5. Generate `pytest.ini` from coverage_config.py

**Afternoon (4 hours)**:
6. Create `scripts/validate_docs.py`
   - Check broken links
   - Validate code examples
   - Verify TOC
   - Check freshness

7. Test CI/CD pipeline locally
8. Fix any issues

**Evening (1 hour)**:
9. Push and verify CI/CD runs successfully

#### Day 10: Performance & Final QA (Phase 4B)
**Morning (4 hours)**:
1. Create performance benchmarks
   - `test_complexity_benchmarks.py`
   - `test_planning_benchmarks.py`
   - `test_metrics_benchmarks.py`

2. Run security scans
   - bandit
   - safety
   - pip-audit

**Afternoon (4 hours)**:
3. Final test suite execution
4. Coverage validation (all targets met)
5. Documentation review
6. Performance benchmark validation

**Evening (1 hour)**:
7. Create final report
8. Sign off on quality gates
9. TASK-003E COMPLETE

---

## Effort Estimates

### Phase-by-Phase Estimates

| Phase | Sub-Phase | Duration | Complexity | Risk |
|-------|-----------|----------|------------|------|
| **Phase 1** | Infrastructure | ✅ 1 day (actual) | Medium | Low |
| **Phase 2A** | Review Mode Tests | 2 days | Medium | Medium |
| **Phase 2B** | Triggers & Templates | 1 day | Low | Low |
| **Phase 2C** | Metrics & Factors | 1 day | Medium | Medium |
| **Phase 2D** | Integration Tests | 1 day | High | Medium |
| **Phase 3A** | E2E Scenarios | 2 days | High | High |
| **Phase 3B** | User Docs | 1 day | Low | Low |
| **Phase 3C** | Developer Docs | 1 day | Low | Low |
| **Phase 4A** | CI/CD & Automation | 1 day | Medium | Medium |
| **Phase 4B** | Performance & QA | 1 day | Medium | Low |
| **TOTAL** | **All Phases** | **10 days** | - | - |

### Test Count by Category

| Category | Tests | Coverage Target | Effort (hours) |
|----------|-------|-----------------|----------------|
| Unit - Complexity Calc | 45 | ✅ DONE | ✅ DONE |
| Unit - Review Modes | 205 | ≥92% | 16 hours |
| Unit - Triggers | 40 | ≥90% | 4 hours |
| Unit - Templates | 90 | ≥90% | 8 hours |
| Unit - Metrics | 55 | ≥90% | 6 hours |
| Unit - Factors | 50 | ≥93% | 6 hours |
| Integration | 105 | ≥80% | 12 hours |
| E2E | 60 scenarios | ≥70% | 16 hours |
| Edge Cases | 120 | 100% | 8 hours |
| Performance | 15 benchmarks | N/A | 4 hours |
| **TOTAL** | **785 tests** | **≥85%** | **80 hours** |

### Documentation Effort

| Document Type | File Count | Word Count | Effort (hours) |
|---------------|-----------|------------|----------------|
| User Guides | 6 | ~11,500 | 6 hours |
| Developer Guides | 6 | ~14,300 | 8 hours |
| API Docs (auto-gen) | 2 | ~4,500 | 2 hours |
| Configuration | 2 | ~3,300 | 2 hours |
| ADRs | 4 | ~3,000 | 2 hours |
| **TOTAL** | **20 files** | **~36,600 words** | **20 hours** |

---

## Risk Mitigation

### High-Risk Areas

#### RISK-001: Dependency Implementation Gaps
**Severity**: HIGH
**Probability**: MEDIUM (60%)
**Impact**: Phase 2 testing blocked

**Mitigation**:
1. **Action**: Run dependency verification before Phase 2 (Day 2 morning)
2. **Contingency**: If missing, adjust test scope:
   - Skip tests for missing modules
   - Use mock-only approach
   - Document gaps for future work
3. **Prevention**: Create dependency verification script

**Verification Script**:
```bash
#!/bin/bash
# File: scripts/verify_dependencies.sh

echo "Verifying TASK-003E dependencies..."

missing_files=()

check_file() {
    if [ -f "$1" ]; then
        echo "✅ $1"
    else
        echo "❌ $1 MISSING"
        missing_files+=("$1")
    fi
}

check_file "installer/global/commands/lib/complexity_factors.py"
check_file "installer/global/commands/lib/review_modes.py"
check_file "installer/global/commands/lib/plan_templates.py"
check_file "installer/global/commands/lib/metrics_collector.py"
check_file "installer/global/commands/lib/countdown_timer.py"

if [ ${#missing_files[@]} -eq 0 ]; then
    echo -e "\n✅ All dependencies verified"
    exit 0
else
    echo -e "\n❌ Missing ${#missing_files[@]} dependencies"
    echo "Continue with mock-only testing for missing modules"
    exit 1
fi
```

#### RISK-002: Test Maintenance Overhead
**Severity**: HIGH
**Probability**: MEDIUM (50%)
**Impact**: Test quality degrades over time

**Mitigation**:
1. **Centralized fixtures**: ✅ Already implemented (data_fixtures.py, mock_fixtures.py)
2. **Single coverage config**: ✅ Already implemented (coverage_config.py)
3. **Clear patterns**: ✅ Established in Phase 1 (test_complexity_calculation_comprehensive.py)
4. **Quarterly audits**: Schedule test quality reviews
5. **Mutation testing**: Plan for Phase 2+ (post-MVP)

**Monitoring**:
- Test-to-code ratio: Monitor in CI/CD (target ≥1.5:1)
- Test execution time: Track trends (<5 minutes total)
- Flaky test rate: Monitor and fix (<1% tolerance)

#### RISK-003: Documentation Drift
**Severity**: HIGH
**Probability**: HIGH (70%)
**Impact**: Documentation becomes stale and untrusted

**Mitigation**:
1. **Automated validation**: Create `scripts/validate_docs.py` (Phase 4A)
2. **Pre-commit hooks**: Validate docs on every commit
3. **CI/CD checks**: Run validation in GitHub Actions
4. **Freshness timestamps**: Include "Last updated" in every doc
5. **Quarterly reviews**: Schedule documentation audits

**Validation Checks**:
```python
# File: scripts/validate_docs.py

import re
from pathlib import Path
from datetime import datetime, timedelta

def validate_documentation():
    """Validate all documentation files."""
    errors = []

    # 1. Check for broken links
    for doc_file in Path("docs").rglob("*.md"):
        content = doc_file.read_text()
        links = re.findall(r'\[.*?\]\((.*?)\)', content)
        for link in links:
            if link.startswith('http'):
                continue  # Skip external links (validate with linkcheck)
            target = (doc_file.parent / link).resolve()
            if not target.exists():
                errors.append(f"Broken link in {doc_file}: {link}")

    # 2. Check for missing Table of Contents
    for doc_file in Path("docs").rglob("*.md"):
        content = doc_file.read_text()
        if len(content) > 1000 and "## Table of Contents" not in content:
            errors.append(f"Missing TOC in {doc_file}")

    # 3. Check freshness (>30 days old)
    for doc_file in Path("docs").rglob("*.md"):
        content = doc_file.read_text()
        match = re.search(r'\*\*Last Updated\*\*: (\d{4}-\d{2}-\d{2})', content)
        if match:
            last_updated = datetime.strptime(match.group(1), '%Y-%m-%d')
            if datetime.now() - last_updated > timedelta(days=30):
                errors.append(f"Stale documentation (>30 days): {doc_file}")
        else:
            errors.append(f"Missing 'Last Updated' timestamp in {doc_file}")

    # 4. Validate code examples compile
    for doc_file in Path("docs").rglob("*.md"):
        content = doc_file.read_text()
        code_blocks = re.findall(r'```python\n(.*?)```', content, re.DOTALL)
        for i, code in enumerate(code_blocks):
            try:
                compile(code, f"{doc_file}:block{i}", 'exec')
            except SyntaxError as e:
                errors.append(f"Invalid Python code in {doc_file}, block {i}: {e}")

    return errors

if __name__ == '__main__':
    errors = validate_documentation()
    if errors:
        print("Documentation validation FAILED:")
        for error in errors:
            print(f"  - {error}")
        exit(1)
    else:
        print("✅ Documentation validation PASSED")
        exit(0)
```

### Medium-Risk Areas

#### RISK-004: Performance Degradation
**Severity**: MEDIUM
**Probability**: MEDIUM (40%)
**Impact**: Slow test execution, poor user experience

**Mitigation**:
1. **Early benchmarking**: Create performance tests in Phase 2C
2. **Continuous monitoring**: Track performance in CI/CD
3. **Optimization guidelines**: Document performance patterns
4. **Caching strategy**: Implement for complexity calculation

**Performance Monitoring**:
```python
# Add to conftest.py
import pytest

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Track slow tests."""
    if call.when == "call":
        duration = call.stop - call.start
        if duration > 1.0:  # Slow test threshold
            print(f"\n⚠️  Slow test: {item.nodeid} took {duration:.2f}s")
```

#### RISK-005: Flaky Tests
**Severity**: MEDIUM
**Probability**: LOW (20%)
**Impact**: CI/CD unreliable, developer frustration

**Mitigation**:
1. **Mock external dependencies**: ✅ Already implemented
2. **Use tmp_path for isolation**: ✅ Pattern established
3. **No real timers**: ✅ Use mock_countdown_timer
4. **Retry logic**: Add pytest-rerunfailures plugin
5. **Flaky test monitoring**: Track and fix immediately

**Flaky Test Detection**:
```bash
# Install pytest-rerunfailures
pip install pytest-rerunfailures

# Run tests with retry
pytest --reruns 3 --reruns-delay 1

# Track flaky tests
pytest --count=10 tests/  # Run 10 times to detect flakiness
```

---

## Quality Gates

### Phase 2 Quality Gates

| Gate | Threshold | Verification | Blocker |
|------|-----------|--------------|---------|
| Unit test count | ≥765 tests | `pytest --collect-only \| grep "test session"` | Yes |
| Unit coverage - line | ≥90% | `pytest --cov --cov-report=term` | Yes |
| Unit coverage - branch | ≥85% | `pytest --cov --cov-branch` | Yes |
| Integration test count | ≥105 tests | `pytest tests/integration/ --collect-only` | Yes |
| Integration coverage | ≥80% | `pytest tests/integration/ --cov` | Yes |
| Edge case test count | ≥120 tests | `pytest tests/edge_cases/ --collect-only` | Yes |
| Edge case coverage | 100% | `pytest tests/edge_cases/ --cov` | Yes |
| Test execution time | <5 minutes | `time pytest tests/` | No (warning) |
| Zero test failures | 100% pass | `pytest tests/` | Yes |
| Flaky test rate | <1% | Run suite 10x | No (warning) |

**Verification Command**:
```bash
# Run complete Phase 2 quality gate check
pytest tests/ -v \
    --cov=installer/global/commands/lib \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-report=json \
    --cov-fail-under=85 \
    --tb=short \
    -m "unit or integration or edge_case"

# Check test count
pytest --collect-only | grep "test session"

# Expected output:
# collected 990 items (765 unit + 105 integration + 120 edge_case)
```

### Phase 3 Quality Gates

| Gate | Threshold | Verification | Blocker |
|------|-----------|--------------|---------|
| E2E scenario count | ≥60 scenarios | Count `.feature` files | Yes |
| E2E coverage | ≥70% | `pytest tests/e2e/ --cov` | Yes |
| Documentation file count | 12 files | `find docs/ -name "*.md" \| wc -l` | Yes |
| Broken links | 0 | `scripts/validate_docs.py` | Yes |
| Invalid code examples | 0 | `scripts/validate_docs.py` | Yes |
| Missing TOC | 0 | `scripts/validate_docs.py` | No (warning) |
| Stale docs (>30 days) | 0 | `scripts/validate_docs.py` | No (warning) |

**Verification Command**:
```bash
# Run E2E tests
pytest tests/e2e/ -v --cov --cov-fail-under=70

# Validate documentation
python scripts/validate_docs.py

# Count documentation files
find docs/ -name "*.md" | wc -l
# Expected: 12 core files minimum
```

### Phase 4 Quality Gates

| Gate | Threshold | Verification | Blocker |
|------|-----------|--------------|---------|
| CI/CD pipeline functional | All jobs pass | GitHub Actions UI | Yes |
| Pre-commit hooks installed | Hooks run | `pre-commit run --all-files` | Yes |
| Coverage reporting automated | Codecov integration | Check Codecov UI | No |
| Performance targets met | All benchmarks pass | `pytest tests/performance/ --benchmark-only` | Yes |
| Security audit clean | No high/critical | `bandit -r installer/` | Yes |
| Documentation validation | All checks pass | `scripts/validate_docs.py` | Yes |
| Final QA sign-off | Manual approval | QA review | Yes |

**Verification Commands**:
```bash
# Test CI/CD locally
act -l  # List workflows
act -j test  # Run test workflow locally

# Run pre-commit hooks
pre-commit run --all-files

# Run performance benchmarks
pytest tests/performance/ --benchmark-only --benchmark-min-rounds=10

# Run security scans
bandit -r installer/global/commands/lib/ -ll
safety check
pip-audit

# Final validation
scripts/validate_docs.py
pytest tests/ --cov --cov-fail-under=85
```

---

## Summary Checklist

### Pre-Phase 2 Actions ✅❌
- [ ] Install test dependencies (`pip install pytest pytest-cov pytest-mock coverage`)
- [ ] Run dependency verification script (`scripts/verify_dependencies.sh`)
- [ ] Verify Phase 1 tests pass (`pytest tests/unit/test_complexity_calculation_comprehensive.py -v`)
- [ ] Review coverage config (`python tests/coverage_config.py`)
- [ ] Create Phase 2 branch (`git checkout -b task-003e-phase-2`)

### Phase 2 Checklist (Days 2-5)
- [ ] Day 2: Review mode tests (mode selector + quick mode) - 105 tests
- [ ] Day 3: Review mode tests (full mode) + templates - 190 tests
- [ ] Day 4: Triggers + metrics + factors - 145 tests
- [ ] Day 5: Integration tests - 105 tests
- [ ] Coverage verification: ≥90% unit, ≥80% integration

### Phase 3 Checklist (Days 6-8)
- [ ] Day 6: E2E simple + complex flows - 35 scenarios
- [ ] Day 7: E2E edge cases + user docs - 25 scenarios + 6 files
- [ ] Day 8: Developer docs + ADRs - 6 files + 4 ADRs
- [ ] Documentation validation passes

### Phase 4 Checklist (Days 9-10)
- [ ] Day 9: CI/CD setup + pre-commit hooks + validation script
- [ ] Day 10: Performance benchmarks + security audit + final QA
- [ ] All quality gates pass
- [ ] Production ready

---

## Conclusion

This implementation plan provides a comprehensive, phase-by-phase approach to completing TASK-003E using Python and pytest. The plan builds on the successful Phase 1 foundation (completed 2x faster than estimated) and provides clear guidance for the remaining 7-9 days of work.

**Key Success Factors**:
- ✅ Proven infrastructure from Phase 1
- ✅ Clear patterns and examples established
- ✅ Realistic estimates based on Phase 1 actuals
- ✅ Comprehensive risk mitigation strategies
- ✅ Well-defined quality gates at each phase

**Next Actions**:
1. Run dependency verification (Day 2 morning)
2. Start Phase 2A: Review mode testing
3. Follow day-by-day implementation order
4. Monitor progress against quality gates

**Estimated Completion**: Day 10 (8-10 days from Phase 1 completion)

**Confidence Level**: HIGH (85%) - Based on Phase 1 success and clear roadmap

---

**Plan Created**: 2025-10-10
**Phase 1 Status**: ✅ COMPLETE
**Ready for Phase 2**: ✅ YES
**Total Remaining Effort**: 80 hours testing + 20 hours documentation = 100 hours (8-10 days)

---

*This implementation plan is part of TASK-003E and follows the architectural review recommendations.*
