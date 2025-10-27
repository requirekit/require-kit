"""
Unit tests for plan_modifier.py module.

Tests the PlanModifier class and related components for interactive plan modification.
Part of TASK-029: Add "Modify Plan" Option to Phase 2.8 Checkpoint.

Author: Claude (Anthropic)
Created: 2025-10-18
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from typing import Dict, Any, List

# Import the module under test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "installer" / "global" / "commands" / "lib"))

from plan_modifier import (
    ModificationCategory,
    ModificationRecord,
    ModificationSession,
    PlanModifier,
    PlanModificationError
)


# Test Fixtures

@pytest.fixture
def sample_plan() -> Dict[str, Any]:
    """Sample implementation plan for testing."""
    return {
        'task_id': 'TASK-029',
        'version': 1,
        'plan': {
            'files_to_create': [
                'src/module1.py',
                'tests/test_module1.py'
            ],
            'files_to_modify': [
                'src/existing.py'
            ],
            'external_dependencies': [
                'pytest 7.0.0 - Testing framework'
            ],
            'risks': [
                {
                    'description': 'Integration complexity',
                    'level': 'medium',
                    'mitigation': 'Incremental testing'
                }
            ],
            'estimated_duration': '4 hours',
            'estimated_loc': 300,
            'complexity_score': 5
        }
    }


@pytest.fixture
def modifier(sample_plan: Dict[str, Any]) -> PlanModifier:
    """Create PlanModifier instance with mocked load_plan."""
    with patch('plan_modifier.load_plan', return_value=sample_plan):
        modifier = PlanModifier('TASK-029')
        # Pre-initialize session for non-interactive tests
        modifier.session = ModificationSession(
            task_id='TASK-029',
            original_plan=sample_plan.copy(),
            current_plan=sample_plan,
            version=1
        )
        return modifier


# ModificationCategory Tests

class TestModificationCategory:
    """Test ModificationCategory enum."""

    def test_category_values(self):
        """Test category enum values."""
        assert ModificationCategory.FILES.value == "files"
        assert ModificationCategory.DEPENDENCIES.value == "dependencies"
        assert ModificationCategory.RISKS.value == "risks"
        assert ModificationCategory.EFFORT.value == "effort"

    def test_display_names(self):
        """Test display name property."""
        assert ModificationCategory.FILES.display_name == "Files (add/remove)"
        assert ModificationCategory.DEPENDENCIES.display_name == "Dependencies"
        assert ModificationCategory.RISKS.display_name == "Risks"
        assert ModificationCategory.EFFORT.display_name == "Effort Estimate"


# ModificationRecord Tests

class TestModificationRecord:
    """Test ModificationRecord dataclass."""

    def test_record_creation(self):
        """Test creating a modification record."""
        record = ModificationRecord(
            category=ModificationCategory.FILES,
            action='add',
            details='Added new file',
            previous_value=None,
            new_value='src/new_file.py'
        )

        assert record.category == ModificationCategory.FILES
        assert record.action == 'add'
        assert record.details == 'Added new file'
        assert record.previous_value is None
        assert record.new_value == 'src/new_file.py'

    def test_record_str_representation(self):
        """Test string representation of modification record."""
        record = ModificationRecord(
            category=ModificationCategory.DEPENDENCIES,
            action='remove',
            details='Removed old dependency'
        )

        expected = "DEPENDENCIES: remove - Removed old dependency"
        assert str(record) == expected


# ModificationSession Tests

class TestModificationSession:
    """Test ModificationSession dataclass."""

    def test_session_creation(self, sample_plan: Dict[str, Any]):
        """Test creating a modification session."""
        session = ModificationSession(
            task_id='TASK-029',
            original_plan=sample_plan.copy(),
            current_plan=sample_plan,
            version=1
        )

        assert session.task_id == 'TASK-029'
        assert session.version == 1
        assert session.modifications == []
        assert not session.has_modifications
        assert session.modification_count == 0

    def test_has_modifications_property(self, sample_plan: Dict[str, Any]):
        """Test has_modifications property."""
        session = ModificationSession(
            task_id='TASK-029',
            original_plan=sample_plan.copy(),
            current_plan=sample_plan
        )

        # Initially no modifications
        assert not session.has_modifications

        # Add a modification
        session.modifications.append(
            ModificationRecord(
                category=ModificationCategory.FILES,
                action='add',
                details='Test modification'
            )
        )

        assert session.has_modifications
        assert session.modification_count == 1


# PlanModifier Tests

class TestPlanModifier:
    """Test PlanModifier class."""

    def test_initialization(self):
        """Test PlanModifier initialization."""
        modifier = PlanModifier('TASK-029')
        assert modifier.task_id == 'TASK-029'
        assert modifier.session is None

    def test_initialization_with_invalid_task(self):
        """Test initialization handles invalid task gracefully."""
        modifier = PlanModifier('')
        assert modifier.task_id == ''

    @patch('plan_modifier.load_plan')
    def test_run_interactive_session_plan_not_found(self, mock_load: Mock):
        """Test session fails gracefully when plan not found."""
        mock_load.return_value = None

        modifier = PlanModifier('TASK-999')

        with pytest.raises(PlanModificationError, match="No implementation plan found"):
            modifier.run_interactive_session()

    @patch('plan_modifier.load_plan')
    def test_run_interactive_session_load_error(self, mock_load: Mock):
        """Test session handles plan loading errors."""
        from plan_modifier import PlanPersistenceError
        mock_load.side_effect = PlanPersistenceError("Load failed")

        modifier = PlanModifier('TASK-029')

        with pytest.raises(PlanModificationError, match="Cannot load plan"):
            modifier.run_interactive_session()

    def test_get_user_choice_normal_input(self, modifier: PlanModifier):
        """Test getting user choice with normal input."""
        with patch('builtins.input', return_value='  1  '):
            choice = modifier._get_user_choice("Choose: ")
            assert choice == '1'

    def test_get_user_choice_keyboard_interrupt(self, modifier: PlanModifier):
        """Test handling keyboard interrupt during input."""
        with patch('builtins.input', side_effect=KeyboardInterrupt):
            choice = modifier._get_user_choice("Choose: ")
            assert choice == '7'  # Should return cancel option

    def test_get_user_choice_eof_error(self, modifier: PlanModifier):
        """Test handling EOF error during input."""
        with patch('builtins.input', side_effect=EOFError):
            choice = modifier._get_user_choice("Choose: ")
            assert choice == '7'  # Should return cancel option


# File Modification Tests

class TestFileModifications:
    """Test file modification operations."""

    def test_add_file_to_create(self, modifier: PlanModifier):
        """Test adding a file to create list."""
        plan = modifier.session.current_plan['plan']
        files_to_create = plan['files_to_create']
        initial_count = len(files_to_create)

        with patch('builtins.input', return_value='src/new_file.py'):
            modifier._add_file(files_to_create, 'create')

        assert len(files_to_create) == initial_count + 1
        assert 'src/new_file.py' in files_to_create
        assert modifier.session.modification_count == 1
        assert modifier.session.modifications[0].action == 'add'

    def test_add_file_empty_path(self, modifier: PlanModifier):
        """Test adding file with empty path is rejected."""
        plan = modifier.session.current_plan['plan']
        files_to_create = plan['files_to_create']
        initial_count = len(files_to_create)

        with patch('builtins.input', return_value=''):
            modifier._add_file(files_to_create, 'create')

        assert len(files_to_create) == initial_count
        assert modifier.session.modification_count == 0

    def test_add_duplicate_file(self, modifier: PlanModifier):
        """Test adding duplicate file is rejected."""
        plan = modifier.session.current_plan['plan']
        files_to_create = plan['files_to_create']
        existing_file = files_to_create[0]
        initial_count = len(files_to_create)

        with patch('builtins.input', return_value=existing_file):
            modifier._add_file(files_to_create, 'create')

        assert len(files_to_create) == initial_count
        assert modifier.session.modification_count == 0

    def test_remove_file_valid(self, modifier: PlanModifier):
        """Test removing a valid file."""
        plan = modifier.session.current_plan['plan']
        files_to_create = plan['files_to_create']
        initial_count = len(files_to_create)

        with patch('builtins.input', return_value='1'):
            modifier._remove_file(files_to_create, 'create')

        assert len(files_to_create) == initial_count - 1
        assert modifier.session.modification_count == 1
        assert modifier.session.modifications[0].action == 'remove'

    def test_remove_file_cancel(self, modifier: PlanModifier):
        """Test cancelling file removal."""
        plan = modifier.session.current_plan['plan']
        files_to_create = plan['files_to_create']
        initial_count = len(files_to_create)

        with patch('builtins.input', return_value='c'):
            modifier._remove_file(files_to_create, 'create')

        assert len(files_to_create) == initial_count
        assert modifier.session.modification_count == 0

    def test_remove_file_invalid_number(self, modifier: PlanModifier):
        """Test removing file with invalid number."""
        plan = modifier.session.current_plan['plan']
        files_to_create = plan['files_to_create']
        initial_count = len(files_to_create)

        with patch('builtins.input', return_value='999'):
            modifier._remove_file(files_to_create, 'create')

        assert len(files_to_create) == initial_count
        assert modifier.session.modification_count == 0

    def test_remove_file_from_empty_list(self, modifier: PlanModifier):
        """Test removing file from empty list."""
        empty_list = []

        modifier._remove_file(empty_list, 'create')

        assert len(empty_list) == 0
        assert modifier.session.modification_count == 0


# Dependency Modification Tests

class TestDependencyModifications:
    """Test dependency modification operations."""

    def test_add_dependency_full_info(self, modifier: PlanModifier):
        """Test adding dependency with all information."""
        plan = modifier.session.current_plan['plan']
        dependencies = plan['external_dependencies']
        initial_count = len(dependencies)

        inputs = ['requests', '2.28.0', 'HTTP client']
        with patch('builtins.input', side_effect=inputs):
            modifier._add_dependency(dependencies)

        assert len(dependencies) == initial_count + 1
        assert 'requests 2.28.0 - HTTP client' in dependencies
        assert modifier.session.modification_count == 1

    def test_add_dependency_name_only(self, modifier: PlanModifier):
        """Test adding dependency with name only."""
        plan = modifier.session.current_plan['plan']
        dependencies = plan['external_dependencies']
        initial_count = len(dependencies)

        inputs = ['pandas', '', '']
        with patch('builtins.input', side_effect=inputs):
            modifier._add_dependency(dependencies)

        assert len(dependencies) == initial_count + 1
        assert 'pandas' in dependencies

    def test_add_dependency_empty_name(self, modifier: PlanModifier):
        """Test adding dependency with empty name is rejected."""
        plan = modifier.session.current_plan['plan']
        dependencies = plan['external_dependencies']
        initial_count = len(dependencies)

        with patch('builtins.input', return_value=''):
            modifier._add_dependency(dependencies)

        assert len(dependencies) == initial_count
        assert modifier.session.modification_count == 0

    def test_remove_dependency_valid(self, modifier: PlanModifier):
        """Test removing a valid dependency."""
        plan = modifier.session.current_plan['plan']
        dependencies = plan['external_dependencies']
        initial_count = len(dependencies)

        with patch('builtins.input', return_value='1'):
            modifier._remove_dependency(dependencies)

        assert len(dependencies) == initial_count - 1
        assert modifier.session.modification_count == 1


# Risk Modification Tests

class TestRiskModifications:
    """Test risk modification operations."""

    def test_add_risk_full_info(self, modifier: PlanModifier):
        """Test adding risk with all information."""
        plan = modifier.session.current_plan['plan']
        risks = plan['risks']
        initial_count = len(risks)

        inputs = ['Security vulnerability', 'high', 'Use encryption']
        with patch('builtins.input', side_effect=inputs):
            modifier._add_risk(risks)

        assert len(risks) == initial_count + 1
        assert risks[-1]['description'] == 'Security vulnerability'
        assert risks[-1]['level'] == 'high'
        assert risks[-1]['mitigation'] == 'Use encryption'
        assert modifier.session.modification_count == 1

    def test_add_risk_default_severity(self, modifier: PlanModifier):
        """Test adding risk with default severity."""
        plan = modifier.session.current_plan['plan']
        risks = plan['risks']

        inputs = ['Performance issue', '', '']
        with patch('builtins.input', side_effect=inputs):
            modifier._add_risk(risks)

        assert risks[-1]['level'] == 'medium'

    def test_add_risk_invalid_severity(self, modifier: PlanModifier):
        """Test adding risk with invalid severity defaults to medium."""
        plan = modifier.session.current_plan['plan']
        risks = plan['risks']

        inputs = ['Performance issue', 'critical', '']
        with patch('builtins.input', side_effect=inputs):
            modifier._add_risk(risks)

        assert risks[-1]['level'] == 'medium'

    def test_add_risk_empty_description(self, modifier: PlanModifier):
        """Test adding risk with empty description is rejected."""
        plan = modifier.session.current_plan['plan']
        risks = plan['risks']
        initial_count = len(risks)

        with patch('builtins.input', return_value=''):
            modifier._add_risk(risks)

        assert len(risks) == initial_count
        assert modifier.session.modification_count == 0

    def test_remove_risk_valid(self, modifier: PlanModifier):
        """Test removing a valid risk."""
        plan = modifier.session.current_plan['plan']
        risks = plan['risks']
        initial_count = len(risks)

        with patch('builtins.input', return_value='1'):
            modifier._remove_risk(risks)

        assert len(risks) == initial_count - 1
        assert modifier.session.modification_count == 1

    def test_modify_risk_severity(self, modifier: PlanModifier):
        """Test modifying risk severity."""
        plan = modifier.session.current_plan['plan']
        risks = plan['risks']

        inputs = ['1', 'high', '']
        with patch('builtins.input', side_effect=inputs):
            modifier._modify_risk(risks)

        assert risks[0]['level'] == 'high'
        assert modifier.session.modification_count == 1

    def test_modify_risk_mitigation(self, modifier: PlanModifier):
        """Test modifying risk mitigation."""
        plan = modifier.session.current_plan['plan']
        risks = plan['risks']

        inputs = ['1', '', 'New mitigation strategy']
        with patch('builtins.input', side_effect=inputs):
            modifier._modify_risk(risks)

        assert risks[0]['mitigation'] == 'New mitigation strategy'


# Effort Modification Tests

class TestEffortModifications:
    """Test effort estimate modification operations."""

    def test_modify_effort_all_fields(self, modifier: PlanModifier):
        """Test modifying all effort fields."""
        plan = modifier.session.current_plan['plan']

        inputs = ['6 hours', '500', '7']
        with patch('builtins.input', side_effect=inputs):
            modifier._modify_effort()

        assert plan['estimated_duration'] == '6 hours'
        assert plan['estimated_loc'] == 500
        assert plan['complexity_score'] == 7
        assert modifier.session.modification_count == 1

    def test_modify_effort_keep_current_values(self, modifier: PlanModifier):
        """Test keeping current values when empty input."""
        plan = modifier.session.current_plan['plan']
        original_duration = plan['estimated_duration']
        original_loc = plan['estimated_loc']
        original_complexity = plan['complexity_score']

        inputs = ['', '', '']
        with patch('builtins.input', side_effect=inputs):
            modifier._modify_effort()

        assert plan['estimated_duration'] == original_duration
        assert plan['estimated_loc'] == original_loc
        assert plan['complexity_score'] == original_complexity

    def test_modify_effort_invalid_loc(self, modifier: PlanModifier):
        """Test invalid LOC input keeps current value."""
        plan = modifier.session.current_plan['plan']
        original_loc = plan['estimated_loc']

        inputs = ['6 hours', 'not-a-number', '7']
        with patch('builtins.input', side_effect=inputs):
            modifier._modify_effort()

        assert plan['estimated_loc'] == original_loc

    def test_modify_effort_invalid_complexity_range(self, modifier: PlanModifier):
        """Test complexity out of range keeps current value."""
        plan = modifier.session.current_plan['plan']
        original_complexity = plan['complexity_score']

        inputs = ['6 hours', '500', '15']  # Out of 1-10 range
        with patch('builtins.input', side_effect=inputs):
            modifier._modify_effort()

        assert plan['complexity_score'] == original_complexity


# Undo Tests

class TestUndoFunctionality:
    """Test undo operations."""

    def test_undo_no_modifications(self, modifier: PlanModifier):
        """Test undo with no modifications."""
        modifier._handle_undo()
        assert modifier.session.modification_count == 0

    def test_undo_file_addition(self, modifier: PlanModifier):
        """Test undoing file addition."""
        plan = modifier.session.current_plan['plan']
        files_to_create = plan['files_to_create']
        initial_count = len(files_to_create)

        # Add a file
        with patch('builtins.input', return_value='src/undo_test.py'):
            modifier._add_file(files_to_create, 'create')

        assert len(files_to_create) == initial_count + 1

        # Undo
        modifier._handle_undo()

        assert len(files_to_create) == initial_count
        assert 'src/undo_test.py' not in files_to_create

    def test_undo_file_removal(self, modifier: PlanModifier):
        """Test undoing file removal."""
        plan = modifier.session.current_plan['plan']
        files_to_create = plan['files_to_create']
        removed_file = files_to_create[0]

        # Remove a file
        with patch('builtins.input', return_value='1'):
            modifier._remove_file(files_to_create, 'create')

        assert removed_file not in files_to_create

        # Undo
        modifier._handle_undo()

        assert removed_file in files_to_create

    def test_undo_dependency_addition(self, modifier: PlanModifier):
        """Test undoing dependency addition."""
        plan = modifier.session.current_plan['plan']
        dependencies = plan['external_dependencies']
        initial_count = len(dependencies)

        # Add dependency
        inputs = ['new-package', '1.0.0', 'Testing']
        with patch('builtins.input', side_effect=inputs):
            modifier._add_dependency(dependencies)

        # Undo
        modifier._handle_undo()

        assert len(dependencies) == initial_count

    def test_undo_effort_modification(self, modifier: PlanModifier):
        """Test undoing effort modification."""
        plan = modifier.session.current_plan['plan']
        original_duration = plan['estimated_duration']
        original_loc = plan['estimated_loc']
        original_complexity = plan['complexity_score']

        # Modify effort
        inputs = ['8 hours', '600', '8']
        with patch('builtins.input', side_effect=inputs):
            modifier._modify_effort()

        # Undo
        modifier._handle_undo()

        assert plan['estimated_duration'] == original_duration
        assert plan['estimated_loc'] == original_loc
        assert plan['complexity_score'] == original_complexity


# Finalization Tests

class TestFinalization:
    """Test plan modification finalization."""

    def test_finalize_no_modifications(self, modifier: PlanModifier):
        """Test finalization with no modifications."""
        result = modifier._finalize_modifications()
        assert result is None

    def test_finalize_with_modifications_confirmed(self, modifier: PlanModifier):
        """Test finalization with confirmed modifications."""
        # Add a modification
        plan = modifier.session.current_plan['plan']
        files_to_create = plan['files_to_create']

        with patch('builtins.input', return_value='src/test_file.py'):
            modifier._add_file(files_to_create, 'create')

        # Mock save_plan_version at the plan_persistence module level
        with patch('plan_persistence.save_plan_version', return_value=Path('/tmp/test')):
            with patch('builtins.input', return_value='y'):
                result = modifier._finalize_modifications()

        assert result is not None
        assert result['version'] == 2  # Version incremented

    def test_finalize_with_modifications_cancelled(self, modifier: PlanModifier):
        """Test finalization with cancelled modifications."""
        # Add a modification
        plan = modifier.session.current_plan['plan']
        files_to_create = plan['files_to_create']

        with patch('builtins.input', return_value='src/test_file.py'):
            modifier._add_file(files_to_create, 'create')

        # Cancel save
        with patch('builtins.input', return_value='n'):
            result = modifier._finalize_modifications()

        assert result is None

    def test_finalize_save_error(self, modifier: PlanModifier):
        """Test finalization handles save errors."""
        # Add a modification
        plan = modifier.session.current_plan['plan']
        files_to_create = plan['files_to_create']

        with patch('builtins.input', return_value='src/test_file.py'):
            modifier._add_file(files_to_create, 'create')

        # Mock save failure at the plan_persistence module level
        with patch('plan_persistence.save_plan_version', side_effect=Exception("Save failed")):
            with patch('builtins.input', return_value='y'):
                with pytest.raises(PlanModificationError, match="Failed to save plan"):
                    modifier._finalize_modifications()


# Integration-like Tests

class TestModificationWorkflows:
    """Test complete modification workflows."""

    def test_multiple_modifications_workflow(self, modifier: PlanModifier):
        """Test workflow with multiple modifications."""
        plan = modifier.session.current_plan['plan']

        # Add file
        with patch('builtins.input', return_value='src/workflow_test.py'):
            modifier._add_file(plan['files_to_create'], 'create')

        # Add dependency
        inputs = ['workflow-lib', '1.0.0', 'Workflow support']
        with patch('builtins.input', side_effect=inputs):
            modifier._add_dependency(plan['external_dependencies'])

        # Add risk
        inputs = ['Workflow complexity', 'high', 'Careful testing']
        with patch('builtins.input', side_effect=inputs):
            modifier._add_risk(plan['risks'])

        # Modify effort
        inputs = ['8 hours', '800', '7']
        with patch('builtins.input', side_effect=inputs):
            modifier._modify_effort()

        # Verify all modifications recorded
        assert modifier.session.modification_count == 4
        assert len(plan['files_to_create']) == 3  # Original 2 + 1 new
        assert len(plan['external_dependencies']) == 2  # Original 1 + 1 new
        assert len(plan['risks']) == 2  # Original 1 + 1 new
        assert plan['estimated_duration'] == '8 hours'

    def test_modification_with_multiple_undos(self, modifier: PlanModifier):
        """Test workflow with modifications and undos."""
        plan = modifier.session.current_plan['plan']
        original_file_count = len(plan['files_to_create'])

        # Add three files
        for i in range(3):
            with patch('builtins.input', return_value=f'src/test{i}.py'):
                modifier._add_file(plan['files_to_create'], 'create')

        assert modifier.session.modification_count == 3
        assert len(plan['files_to_create']) == original_file_count + 3

        # Undo twice
        modifier._handle_undo()
        modifier._handle_undo()

        assert modifier.session.modification_count == 1
        assert len(plan['files_to_create']) == original_file_count + 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
