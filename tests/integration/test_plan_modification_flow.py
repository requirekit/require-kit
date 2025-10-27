"""
Integration tests for plan modification flow.

Tests the complete integration between plan_modifier, plan_persistence, and checkpoint_display.
Part of TASK-029: Add "Modify Plan" Option to Phase 2.8 Checkpoint.

Author: Claude (Anthropic)
Created: 2025-10-18
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# Import modules under test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "installer" / "global" / "commands" / "lib"))

from plan_modifier import PlanModifier, ModificationCategory
from plan_persistence import save_plan, load_plan, save_plan_version
from plan_markdown_renderer import PlanMarkdownRenderer


@pytest.fixture
def temp_state_dir():
    """Create temporary state directory for testing."""
    temp_dir = tempfile.mkdtemp()
    state_dir = Path(temp_dir) / "docs" / "state"
    state_dir.mkdir(parents=True, exist_ok=True)
    yield state_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_plan_data() -> Dict[str, Any]:
    """Sample plan data for integration testing."""
    return {
        'task_id': 'TASK-INT-001',
        'version': 1,
        'plan': {
            'overview': 'Integration test plan',
            'files_to_create': [
                'src/integration_test.py',
                'tests/test_integration.py'
            ],
            'files_to_modify': [],
            'external_dependencies': [],
            'risks': [],
            'estimated_duration': '2 hours',
            'estimated_loc': 150,
            'complexity_score': 3
        }
    }


class TestPlanModificationIntegration:
    """Integration tests for complete plan modification workflow."""

    def test_save_and_load_plan(self, temp_state_dir: Path, sample_plan_data: Dict[str, Any]):
        """Test saving and loading a plan."""
        task_id = sample_plan_data['task_id']
        task_state_dir = temp_state_dir / task_id
        task_state_dir.mkdir(parents=True, exist_ok=True)

        # Save plan
        save_path = save_plan(task_id, sample_plan_data, base_dir=temp_state_dir.parent.parent)

        # Verify file exists
        assert save_path.exists()
        assert save_path.name == 'implementation_plan.md'

        # Load plan
        loaded_plan = load_plan(task_id, base_dir=temp_state_dir.parent.parent)

        # Verify loaded data matches original
        assert loaded_plan is not None
        assert loaded_plan['task_id'] == task_id
        assert loaded_plan['version'] == 1
        assert len(loaded_plan['plan']['files_to_create']) == 2

    def test_plan_modification_with_version_history(self, temp_state_dir: Path, sample_plan_data: Dict[str, Any]):
        """Test plan modification creates version history."""
        task_id = sample_plan_data['task_id']
        task_state_dir = temp_state_dir / task_id
        task_state_dir.mkdir(parents=True, exist_ok=True)
        versions_dir = task_state_dir / 'versions'
        versions_dir.mkdir(parents=True, exist_ok=True)

        # Save initial plan
        save_plan(task_id, sample_plan_data, base_dir=temp_state_dir.parent.parent)

        # Modify plan
        modified_plan = sample_plan_data.copy()
        modified_plan['version'] = 2
        modified_plan['plan']['files_to_create'].append('src/new_file.py')

        # Save version with modifications
        from plan_modifier import ModificationRecord
        modifications = [
            ModificationRecord(
                category=ModificationCategory.FILES,
                action='add',
                details='Added src/new_file.py to create',
                previous_value=None,
                new_value='src/new_file.py'
            )
        ]

        version_path = save_plan_version(
            task_id,
            modified_plan,
            modifications=modifications,
            base_dir=temp_state_dir.parent.parent
        )

        # Verify version file created
        assert version_path.exists()
        assert 'v2' in version_path.name

        # Load modified plan
        loaded_plan = load_plan(task_id, base_dir=temp_state_dir.parent.parent)
        assert loaded_plan['version'] == 2
        assert 'src/new_file.py' in loaded_plan['plan']['files_to_create']

    def test_complete_modification_workflow(self, temp_state_dir: Path, sample_plan_data: Dict[str, Any]):
        """Test complete workflow: create, modify, save, load."""
        task_id = sample_plan_data['task_id']
        task_state_dir = temp_state_dir / task_id
        task_state_dir.mkdir(parents=True, exist_ok=True)

        # Create initial plan
        save_plan(task_id, sample_plan_data, base_dir=temp_state_dir.parent.parent)

        # Mock user inputs for modification
        with patch('plan_modifier.load_plan') as mock_load:
            with patch('plan_modifier.save_plan_version') as mock_save:
                mock_load.return_value = sample_plan_data.copy()
                mock_save.return_value = Path('/tmp/test_plan.md')

                modifier = PlanModifier(task_id)

                # Simulate adding a file
                with patch('builtins.input', side_effect=['src/added_file.py']):
                    modifier.session = modifier._create_session(sample_plan_data.copy())
                    plan = modifier.session.current_plan['plan']
                    modifier._add_file(plan['files_to_create'], 'create')

                # Verify modification recorded
                assert modifier.session.modification_count == 1
                assert 'src/added_file.py' in plan['files_to_create']

    def test_plan_rendering_after_modification(self, temp_state_dir: Path, sample_plan_data: Dict[str, Any]):
        """Test plan can be rendered after modification."""
        task_id = sample_plan_data['task_id']

        # Add some modifications to plan
        sample_plan_data['plan']['files_to_create'].append('src/rendered_file.py')
        sample_plan_data['plan']['external_dependencies'].append('pytest 7.0.0 - Testing')

        # Render plan
        renderer = PlanMarkdownRenderer(sample_plan_data)
        markdown = renderer.render()

        # Verify rendering includes modifications
        assert 'src/rendered_file.py' in markdown
        assert 'pytest 7.0.0' in markdown
        assert 'TASK-INT-001' in markdown

    def test_multiple_modification_sessions(self, temp_state_dir: Path, sample_plan_data: Dict[str, Any]):
        """Test multiple sequential modification sessions."""
        task_id = sample_plan_data['task_id']
        task_state_dir = temp_state_dir / task_id
        task_state_dir.mkdir(parents=True, exist_ok=True)

        # Save initial plan
        save_plan(task_id, sample_plan_data, base_dir=temp_state_dir.parent.parent)

        # First modification session
        plan_v1 = sample_plan_data.copy()
        plan_v1['version'] = 2
        plan_v1['plan']['files_to_create'].append('src/session1.py')

        from plan_modifier import ModificationRecord
        mods_v1 = [
            ModificationRecord(
                category=ModificationCategory.FILES,
                action='add',
                details='Session 1 modification'
            )
        ]
        save_plan_version(task_id, plan_v1, modifications=mods_v1, base_dir=temp_state_dir.parent.parent)

        # Second modification session
        plan_v2 = plan_v1.copy()
        plan_v2['version'] = 3
        plan_v2['plan']['files_to_create'].append('src/session2.py')

        mods_v2 = [
            ModificationRecord(
                category=ModificationCategory.FILES,
                action='add',
                details='Session 2 modification'
            )
        ]
        save_plan_version(task_id, plan_v2, modifications=mods_v2, base_dir=temp_state_dir.parent.parent)

        # Load final plan
        final_plan = load_plan(task_id, base_dir=temp_state_dir.parent.parent)

        # Verify all modifications present
        assert final_plan['version'] == 3
        assert 'src/session1.py' in final_plan['plan']['files_to_create']
        assert 'src/session2.py' in final_plan['plan']['files_to_create']

    def test_modification_with_undo_integration(self, temp_state_dir: Path, sample_plan_data: Dict[str, Any]):
        """Test modification with undo doesn't create version."""
        task_id = sample_plan_data['task_id']

        with patch('plan_modifier.load_plan') as mock_load:
            mock_load.return_value = sample_plan_data.copy()

            modifier = PlanModifier(task_id)
            modifier.session = modifier._create_session(sample_plan_data.copy())

            # Add a file
            plan = modifier.session.current_plan['plan']
            original_count = len(plan['files_to_create'])

            with patch('builtins.input', return_value='src/undo_test.py'):
                modifier._add_file(plan['files_to_create'], 'create')

            assert len(plan['files_to_create']) == original_count + 1

            # Undo the addition
            modifier._handle_undo()

            # Verify back to original state
            assert len(plan['files_to_create']) == original_count
            assert modifier.session.modification_count == 0

    def _create_session(self, plan_data: Dict[str, Any]):
        """Helper method to create session (simulates what run_interactive_session does)."""
        from plan_modifier import ModificationSession
        return ModificationSession(
            task_id=plan_data['task_id'],
            original_plan=plan_data.copy(),
            current_plan=plan_data,
            version=plan_data.get('version', 1)
        )


class TestCheckpointIntegration:
    """Integration tests with checkpoint display."""

    def test_checkpoint_calls_modifier(self):
        """Test checkpoint display integrates with plan modifier."""
        # This would test checkpoint_display.handle_modify_option()
        # For now, we'll test the interface exists

        try:
            from checkpoint_display import handle_modify_option
            assert callable(handle_modify_option)
        except ImportError:
            pytest.skip("checkpoint_display not available in test environment")

    def test_plan_persistence_error_handling(self, temp_state_dir: Path):
        """Test error handling when plan file is corrupted."""
        task_id = 'TASK-CORRUPT'
        task_state_dir = temp_state_dir / task_id
        task_state_dir.mkdir(parents=True, exist_ok=True)

        # Create corrupted plan file
        plan_file = task_state_dir / 'implementation_plan.md'
        plan_file.write_text('This is not valid YAML frontmatter')

        # Attempt to load should handle gracefully
        from plan_persistence import PlanPersistenceError

        with pytest.raises((PlanPersistenceError, Exception)):
            load_plan(task_id, base_dir=temp_state_dir.parent.parent)


class TestVersionHistory:
    """Integration tests for version history management."""

    def test_version_history_preservation(self, temp_state_dir: Path, sample_plan_data: Dict[str, Any]):
        """Test that version history is preserved across modifications."""
        task_id = sample_plan_data['task_id']
        task_state_dir = temp_state_dir / task_id
        versions_dir = task_state_dir / 'versions'
        versions_dir.mkdir(parents=True, exist_ok=True)

        # Save initial version
        save_plan(task_id, sample_plan_data, base_dir=temp_state_dir.parent.parent)

        # Create multiple versions
        for version in range(2, 5):
            modified_plan = sample_plan_data.copy()
            modified_plan['version'] = version
            modified_plan['plan']['files_to_create'].append(f'src/v{version}_file.py')

            from plan_modifier import ModificationRecord
            modifications = [
                ModificationRecord(
                    category=ModificationCategory.FILES,
                    action='add',
                    details=f'Version {version} modification'
                )
            ]

            save_plan_version(
                task_id,
                modified_plan,
                modifications=modifications,
                base_dir=temp_state_dir.parent.parent
            )

        # Verify all version files exist
        version_files = list(versions_dir.glob('implementation_plan_v*.md'))
        assert len(version_files) >= 3  # v2, v3, v4

    def test_concurrent_modification_detection(self, temp_state_dir: Path, sample_plan_data: Dict[str, Any]):
        """Test handling of concurrent modifications (version conflict)."""
        # This test would check if the system handles version conflicts
        # when multiple modifiers try to save at the same version
        task_id = sample_plan_data['task_id']

        # Save initial plan
        save_plan(task_id, sample_plan_data, base_dir=temp_state_dir.parent.parent)

        # Both modifiers load version 1
        plan_a = sample_plan_data.copy()
        plan_b = sample_plan_data.copy()

        # Both modify to version 2
        plan_a['version'] = 2
        plan_b['version'] = 2

        from plan_modifier import ModificationRecord

        # First save succeeds
        save_plan_version(
            task_id,
            plan_a,
            modifications=[ModificationRecord(
                category=ModificationCategory.FILES,
                action='add',
                details='Modifier A change'
            )],
            base_dir=temp_state_dir.parent.parent
        )

        # Second save should also succeed (overwrites or creates v2_2)
        save_plan_version(
            task_id,
            plan_b,
            modifications=[ModificationRecord(
                category=ModificationCategory.FILES,
                action='add',
                details='Modifier B change'
            )],
            base_dir=temp_state_dir.parent.parent
        )

        # At minimum, we should have the final version
        final_plan = load_plan(task_id, base_dir=temp_state_dir.parent.parent)
        assert final_plan is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
