# TASK-003E Continuation Guide
**For Next Developer/Session**

## Quick Start
```bash
cd /Users/richardwoollcott/Projects/appmilla_github/ai-engineer
source .venv/bin/activate
python -m pytest tests/unit/ -v
```

## Current State Summary
- **Phase 1**: Complete ✅ (47 tests)
- **Phase 2**: 50% complete (84 tests total, 10 need mock fixes)
- **Phases 3-10**: Not started

## Immediate Tasks (Priority Order)

### Task 1: Fix Mock Issues (30 minutes)
**File**: `tests/unit/test_review_modes_quick.py`
**Issue**: 10 tests failing due to Mock attribute access

#### Problem
```python
# Current (broken):
plan.complexity_score = Mock(
    total_score=5,
    patterns_detected=[],
    warnings=[],
    metadata={}
)
```

#### Solution
```python
# Fixed (working):
score = ComplexityScore(
    total_score=5,
    factor_scores=[],
    forced_review_triggers=[],
    review_mode=ReviewMode.QUICK_OPTIONAL,
    calculation_timestamp=datetime.now(),
    metadata={
        "patterns_detected": [],
        "warnings": []
    }
)
plan.complexity_score = score
plan.display_score = 50  # Required for badge formatting
```

#### Tests to Fix
1. `test_render_summary_card_output`
2. `test_render_summary_card_truncates_long_instructions`
3. `test_render_summary_card_shows_key_patterns`
4. `test_render_summary_card_shows_warnings`
5. `test_execute_timeout_flow`
6. `test_execute_cancel_flow`
7. `test_execute_calls_countdown_with_correct_params`
8. `test_execute_keyboard_interrupt_propagates`
9. `test_display_with_no_patterns`
10. `test_display_with_no_warnings`

#### Patch Fix
The countdown_timer patching needs correct path:
```python
# Try these patch paths:
@patch('installer.global.commands.lib.review_modes.countdown_timer')
# OR
@patch('installer.global.commands.lib.user_interaction.countdown_timer')
```

### Task 2: Complete Full Review Mode (2-3 hours)
**Create**: `tests/unit/test_review_modes_full.py`
**Target**: 60 tests

#### Structure
```python
class TestFullReviewDisplay:
    """Test display rendering (12 tests)"""
    # Header display
    # Complexity breakdown
    # Changes summary
    # Risk assessment
    # Implementation order
    # Decision options

class TestFullReviewHandler:
    """Test handler execution (15 tests)"""
    # Initialization
    # Execute workflow
    # Input validation
    # Error handling

class TestFullReviewApproval:
    """Test approval workflow (8 tests)"""
    # Approval creation
    # Metadata updates
    # Phase 3 transition

class TestFullReviewCancellation:
    """Test cancellation workflow (8 tests)"""
    # Confirmation prompt
    # File moving
    # Metadata updates

class TestFullReviewModify:
    """Test modify mode (10 tests)"""
    # Modification session
    # File operations
    # Dependency operations
    # Phase operations
    # Metadata operations

class TestFullReviewView:
    """Test view mode (3 tests)"""
    # Pager display
    # Fallback rendering
    # Error handling

class TestFullReviewQuestion:
    """Test Q&A mode (4 tests)"""
    # Session creation
    # Question handling
    # Session saving
```

#### Copy Patterns From
- `test_review_modes_quick.py` for structure
- Use same fixture patterns
- Follow AAA structure

### Task 3: Integration Tests (3-4 hours)
**Create**:
1. `tests/integration/test_review_workflows.py` (35 tests)
2. `tests/integration/test_complexity_to_review.py` (25 tests)
3. `tests/integration/test_modification_loop.py` (20 tests)

#### Directory Setup
```bash
mkdir -p tests/integration
touch tests/integration/__init__.py
```

#### Workflow Tests Structure
```python
class TestAutoProceedWorkflow:
    """Complete auto-proceed flow (7 tests)"""

class TestQuickOptionalWorkflow:
    """Quick review with timeout/escalate (8 tests)"""

class TestFullRequiredWorkflow:
    """Full review with approve/modify (10 tests)"""

class TestErrorRecovery:
    """Error handling workflows (5 tests)"""

class TestStateTransitions:
    """State management (5 tests)"""
```

## Test Patterns to Follow

### Fixture Pattern
```python
@pytest.fixture
def simple_plan():
    """Create simple implementation plan."""
    score = ComplexityScore(
        total_score=5,
        factor_scores=[...],
        forced_review_triggers=[],
        review_mode=ReviewMode.QUICK_OPTIONAL,
        calculation_timestamp=datetime.now(),
        metadata={}
    )

    plan = ImplementationPlan(
        task_id="TASK-001",
        files_to_create=["file1.py", "file2.py"],
        patterns_used=["pattern1"],
        external_dependencies=["dep1"],
        estimated_loc=100,
        raw_plan="Test plan"
    )
    plan.complexity_score = score
    plan.display_score = 50  # IMPORTANT!
    return plan
```

### Test Pattern
```python
def test_feature_when_condition_then_expected_result(self, fixture):
    """
    Clear description of what this test verifies.

    Covers: [specific functionality]
    Edge cases: [if applicable]
    """
    # Arrange
    input_data = prepare_test_data()
    expected_result = define_expectation()

    # Act
    actual_result = system_under_test.method(input_data)

    # Assert
    assert actual_result == expected_result
    assert additional_conditions
```

### Mock Pattern
```python
@patch('module.external_function')
def test_with_mock(self, mock_external, fixture):
    """Test with mocked external dependency."""
    mock_external.return_value = "mocked_value"

    # Act
    result = function_under_test()

    # Assert
    mock_external.assert_called_once()
    assert result.uses_mocked_value
```

## Running Tests

### Run Specific File
```bash
pytest tests/unit/test_review_router.py -v
```

### Run with Coverage
```bash
pytest tests/unit/ -v --cov=installer/global/commands/lib --cov-report=term
```

### Run Specific Test
```bash
pytest tests/unit/test_review_router.py::TestAutoProceedRouting::test_routes_to_auto_proceed_for_low_score -v
```

### Watch Mode (install pytest-watch)
```bash
pip install pytest-watch
ptw tests/unit/ -- -v
```

## Quality Checklist

### Before Committing Tests
- [ ] All tests pass locally
- [ ] Test names follow convention
- [ ] Docstrings present and clear
- [ ] AAA structure followed
- [ ] Fixtures used appropriately
- [ ] Mocks properly configured
- [ ] No hardcoded paths
- [ ] Coverage ≥85%

### Test File Template
```python
"""
Module docstring describing test scope.

Tests the [SystemUnderTest] [specific aspect].
Covers [list of features].

Target Coverage: ≥[XX]% ([scope])
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Import system under test
try:
    installer_lib_path = Path(__file__).parent.parent.parent / "installer" / "global" / "commands" / "lib"
    if installer_lib_path.exists():
        sys.path.insert(0, str(installer_lib_path))

        import module_under_test

        sys.path.pop(0)
except ImportError as e:
    pytest.skip(f"Module not found: {e}", allow_module_level=True)

# Fixtures
@pytest.fixture
def fixture_name():
    """Fixture description."""
    return create_test_data()

# Test Classes
class TestFeatureCategory:
    """Test specific feature category."""

    def test_specific_behavior(self, fixture):
        """Test description."""
        # AAA structure here
```

## Coverage Targets

### Phase 2 (Unit Tests)
- Complexity calculation: ≥95% ✅
- Review router: ≥95% ✅
- Quick review mode: ≥90% (needs mock fixes)
- Full review mode: ≥90% (not started)
- **Overall Phase 2 Target**: ≥90%

### Phase 3 (Integration Tests)
- **Target**: ≥80%
- Focus on workflow coverage
- Less granular than unit tests
- Test component interactions

### Phase 4 (E2E Tests)
- **Target**: ≥70%
- Full scenario coverage
- User journey validation
- Critical path verification

## Common Gotchas

### 1. Import Path Issues
Always use the installer lib path pattern:
```python
installer_lib_path = Path(__file__).parent.parent.parent / "installer" / "global" / "commands" / "lib"
```

### 2. ComplexityScore Mocking
Don't use raw Mock() - use actual ComplexityScore objects or properly configured Mocks with all attributes.

### 3. Datetime in Tests
Use fixed timestamps or mock datetime.now():
```python
@patch('module.datetime')
def test_with_time(self, mock_datetime):
    mock_datetime.now.return_value = datetime(2025, 10, 10)
```

### 4. File Operations
Mock file operations, don't create actual files:
```python
@patch('pathlib.Path.write_text')
@patch('pathlib.Path.read_text')
def test_file_ops(self, mock_read, mock_write):
    # Test logic
```

## Project Structure
```
tests/
├── unit/                           # Phase 1-2
│   ├── test_complexity_calculation_comprehensive.py  ✅
│   ├── test_review_router.py                        ✅
│   ├── test_review_modes_quick.py                   ⚠️ (10 tests need fixes)
│   └── test_review_modes_full.py                    ⬜ (next to create)
├── integration/                    # Phase 3
│   ├── test_review_workflows.py                     ⬜
│   ├── test_complexity_to_review.py                 ⬜
│   └── test_modification_loop.py                    ⬜
├── e2e/                           # Phase 4
│   └── test_scenarios.py                            ⬜
├── edge_cases/                    # Phase 5
│   ├── test_error_handling.py                       ⬜
│   ├── test_boundary_conditions.py                  ⬜  (property-based here)
│   └── test_configuration_edge_cases.py             ⬜
├── fixtures/                      # Shared test data
│   └── __init__.py
└── coverage_config.py             # Coverage settings
```

## Progress Tracking

### Day 1: ✅ Complete
- 84 tests created
- 84 tests passing (with known mock issues)

### Day 2: In Progress
- Fix 10 mock issues (30 min)
- Complete full review mode (60 tests, 2-3 hours)
- Start integration tests (35 tests, 3-4 hours)
- **Target**: 200+ total tests

### Day 3: Planned
- Complete integration tests (80 tests)
- Start E2E tests (50 tests)
- **Target**: 300+ total tests

### Day 4: Planned
- Complete E2E tests
- Start edge cases (70 tests)
- **Target**: 380+ total tests

### Day 5: Planned
- Complete edge cases
- Documentation (6 files)
- Quality gates validation
- **Target**: 400 tests, all docs complete

## Questions & Support

### Where to Find Examples
- Good test structure: `test_review_router.py`
- Fixture patterns: `test_complexity_calculation_comprehensive.py`
- Mock patterns: `test_review_modes_quick.py`

### Documentation References
- TASK-003E-PHASE-2-PROGRESS-REPORT.md
- TASK-003E-DAY-1-DELIVERY-SUMMARY.md
- installer/global/commands/lib/*.py (source modules)

### If Stuck
1. Check similar test in existing files
2. Review source module being tested
3. Check pytest documentation
4. Run single test with -vv for verbose output

## Success Criteria Reminder
- ✅ 350-400 tests total
- ✅ 6 documentation files
- ✅ ≥90/80/70% coverage (unit/integration/e2e)
- ✅ <5 min test execution
- ✅ Property-based testing pilot (Phase 5)
- ✅ Zero failing tests

**Current Progress**: 84/400 tests (21%) - On track for 4-5 day completion
