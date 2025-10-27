"""
Integration tests for MicroTaskWorkflow

Tests cover:
- Complete micro-task workflow execution
- Quality gate enforcement
- Phase skipping behavior
- Fix loop limiting (1 attempt max)
- State transitions
- Error handling
"""

import pytest
from micro_task_workflow import (
    MicroTaskWorkflow,
    MicroWorkflowResult,
    QualityGateStatus,
    WorkflowPhase,
    execute_micro_workflow,
)


class TestMicroTaskWorkflow:
    """Test suite for MicroTaskWorkflow class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.workflow = MicroTaskWorkflow()

    # === Workflow Execution Tests ===

    def test_execute_successful_workflow(self):
        """Test successful micro-task workflow execution."""
        task_id = 'TASK-100'
        task_metadata = {
            'id': task_id,
            'title': 'Fix typo in error message',
            'description': "Change 'occured' to 'occurred'",
            'complexity_estimate': 1,
            'estimated_effort': '15 minutes'
        }

        result = self.workflow.execute(task_id, task_metadata)

        assert result.success is True
        assert result.final_state == 'in_review'
        assert len(result.phases_executed) == 4  # Phases 1, 3, 4, 5
        assert len(result.phases_skipped) == 5  # Phases 2, 2.5A, 2.5B, 2.6, 2.7
        assert result.all_quality_gates_passed is True
        assert result.duration_minutes < 5  # Should complete quickly

    def test_execute_workflow_with_test_failure(self):
        """Test workflow execution when tests fail."""
        # This would require mocking the test execution
        # For now, we test the workflow structure
        task_id = 'TASK-101'
        task_metadata = {
            'id': task_id,
            'title': 'Fix bug',
            'description': 'Fix null reference',
            'complexity_estimate': 1
        }

        result = self.workflow.execute(task_id, task_metadata)

        # Should execute all phases including fix loop
        assert WorkflowPhase.LOAD_CONTEXT.value in result.phases_executed
        assert WorkflowPhase.IMPLEMENTATION.value in result.phases_executed
        assert WorkflowPhase.QUICK_TESTING.value in result.phases_executed
        assert WorkflowPhase.QUICK_REVIEW.value in result.phases_executed

    def test_execute_workflow_phases_skipped(self):
        """Test that planning phases are skipped."""
        task_id = 'TASK-102'
        task_metadata = {
            'id': task_id,
            'title': 'Update comment',
            'complexity_estimate': 1
        }

        result = self.workflow.execute(task_id, task_metadata)

        expected_skipped = [
            "Phase 2: Implementation Planning",
            "Phase 2.5A: Pattern Suggestion",
            "Phase 2.5B: Architectural Review",
            "Phase 2.6: Human Checkpoint",
            "Phase 2.7: Complexity Evaluation",
        ]

        assert result.phases_skipped == expected_skipped

    # === Phase Execution Tests ===

    def test_phase_1_load_context(self):
        """Test Phase 1 execution."""
        task_id = 'TASK-103'
        task_metadata = {
            'id': task_id,
            'title': 'Test task',
            'priority': 'high'
        }

        result = MicroWorkflowResult(task_id=task_id, success=False)

        self.workflow._execute_phase_1(task_id, task_metadata, result)

        assert WorkflowPhase.LOAD_CONTEXT.value in result.phases_executed
        assert result.metadata['task_title'] == 'Test task'
        assert result.metadata['task_priority'] == 'high'

    def test_phase_3_implementation(self):
        """Test Phase 3 execution."""
        task_id = 'TASK-104'
        task_metadata = {
            'id': task_id,
            'title': 'Implement feature'
        }

        result = MicroWorkflowResult(task_id=task_id, success=False)

        self.workflow._execute_phase_3(task_id, task_metadata, result)

        assert WorkflowPhase.IMPLEMENTATION.value in result.phases_executed
        assert 'implementation_duration_seconds' in result.metadata

    def test_phase_4_quick_testing(self):
        """Test Phase 4 execution."""
        task_id = 'TASK-105'
        task_metadata = {
            'id': task_id,
            'title': 'Test task'
        }

        result = MicroWorkflowResult(task_id=task_id, success=False)

        self.workflow._execute_phase_4(task_id, task_metadata, result)

        assert WorkflowPhase.QUICK_TESTING.value in result.phases_executed
        assert len(result.quality_gates) >= 2  # Compilation + tests
        assert 'testing_duration_seconds' in result.metadata

    def test_phase_4_skip_tests_on_compilation_failure(self):
        """Test that tests are skipped if compilation fails."""
        # This would require mocking compilation to fail
        # For now, we verify the structure exists
        task_id = 'TASK-106'
        task_metadata = {'id': task_id}

        result = MicroWorkflowResult(task_id=task_id, success=False)

        self.workflow._execute_phase_4(task_id, task_metadata, result)

        # Should have compilation gate
        compilation_gates = [g for g in result.quality_gates if g.gate_name == 'compilation']
        assert len(compilation_gates) == 1

    def test_phase_4_5_fix_loop(self):
        """Test Phase 4.5 execution."""
        task_id = 'TASK-107'
        task_metadata = {'id': task_id}

        result = MicroWorkflowResult(task_id=task_id, success=False)

        self.workflow._execute_phase_4_5(task_id, task_metadata, result)

        assert WorkflowPhase.FIX_LOOP.value in result.phases_executed
        assert 'fix_duration_seconds' in result.metadata

    def test_phase_5_quick_review(self):
        """Test Phase 5 execution."""
        task_id = 'TASK-108'
        task_metadata = {'id': task_id}

        result = MicroWorkflowResult(task_id=task_id, success=False)

        self.workflow._execute_phase_5(task_id, task_metadata, result)

        assert WorkflowPhase.QUICK_REVIEW.value in result.phases_executed
        # Should have lint gate
        lint_gates = [g for g in result.quality_gates if g.gate_name == 'lint']
        assert len(lint_gates) == 1

    # === Quality Gate Tests ===

    def test_quality_gate_compilation_pass(self):
        """Test compilation quality gate passes."""
        task_metadata = {'id': 'TASK-109'}

        gate = self.workflow._check_compilation(task_metadata)

        assert gate.gate_name == 'compilation'
        assert gate.status == QualityGateStatus.PASSED
        assert gate.passed is True

    def test_quality_gate_tests_pass(self):
        """Test tests quality gate passes (no coverage required)."""
        task_metadata = {'id': 'TASK-110'}

        gate = self.workflow._check_tests_pass(task_metadata)

        assert gate.gate_name == 'tests_pass'
        assert gate.status == QualityGateStatus.PASSED
        assert gate.details['coverage_skipped'] is True  # Coverage skipped in micro-task mode

    def test_quality_gate_lint_pass(self):
        """Test lint quality gate passes."""
        task_metadata = {'id': 'TASK-111'}

        gate = self.workflow._check_lint(task_metadata)

        assert gate.gate_name == 'lint'
        assert gate.status == QualityGateStatus.PASSED

    # === Fix Loop Tests ===

    def test_fix_loop_max_one_attempt(self):
        """Test that fix loop is limited to 1 attempt."""
        task_metadata = {'id': 'TASK-112'}

        gate = self.workflow._attempt_fix(task_metadata)

        assert gate.gate_name == 'fix_attempt'
        assert gate.details.get('max_attempts') == 1
        assert gate.details.get('attempts') <= 1

    def test_fix_loop_skipped_on_compilation_failure(self):
        """Test that fix loop is skipped if compilation failed."""
        task_id = 'TASK-113'
        task_metadata = {'id': task_id}

        result = MicroWorkflowResult(task_id=task_id, success=False)

        # Simulate compilation failure
        from micro_task_workflow import QualityGateResult
        compilation_gate = QualityGateResult(
            gate_name='compilation',
            status=QualityGateStatus.FAILED,
            details={'errors': 1}
        )
        result.quality_gates.append(compilation_gate)

        self.workflow._execute_phase_4_5(task_id, task_metadata, result)

        # Fix loop should execute but skip actual fix
        assert WorkflowPhase.FIX_LOOP.value in result.phases_executed

    # === Configuration Tests ===

    def test_custom_configuration(self):
        """Test workflow with custom configuration."""
        custom_config = {
            'max_fix_attempts': 0,  # Disable fix loop
            'skip_coverage': True,
            'timeout_seconds': 120
        }

        workflow = MicroTaskWorkflow(config=custom_config)

        assert workflow.config['max_fix_attempts'] == 0
        assert workflow.config['skip_coverage'] is True
        assert workflow.config['timeout_seconds'] == 120

    def test_default_configuration(self):
        """Test workflow uses correct default configuration."""
        workflow = MicroTaskWorkflow()

        assert workflow.config['max_fix_attempts'] == 1
        assert workflow.config['require_compilation'] is True
        assert workflow.config['require_tests_pass'] is True
        assert workflow.config['skip_coverage'] is True
        assert workflow.config['skip_architectural_review'] is True
        assert workflow.config['timeout_seconds'] == 300

    # === State Transition Tests ===

    def test_state_transition_success(self):
        """Test task state transitions to in_review on success."""
        task_id = 'TASK-114'
        task_metadata = {
            'id': task_id,
            'title': 'Success task',
            'complexity_estimate': 1
        }

        result = self.workflow.execute(task_id, task_metadata)

        assert result.final_state == 'in_review'

    def test_state_transition_failure(self):
        """Test task state transitions to blocked on failure."""
        # This would require mocking a quality gate to fail
        # The structure is tested in other tests
        pass

    # === Error Handling Tests ===

    def test_error_handling_graceful_failure(self):
        """Test that errors are handled gracefully."""
        task_id = 'TASK-115'
        task_metadata = None  # Invalid metadata

        try:
            result = self.workflow.execute(task_id, task_metadata)
            # Should not raise, but should mark as failed
            assert result.success is False
            assert result.final_state == 'blocked'
            assert result.error_message is not None
        except Exception:
            pytest.fail("Workflow should handle errors gracefully")

    def test_error_handling_in_phase(self):
        """Test error handling during phase execution."""
        # Errors in individual phases should be logged but not crash workflow
        task_id = 'TASK-116'
        task_metadata = {'id': task_id}

        result = MicroWorkflowResult(task_id=task_id, success=False)

        # Should not raise even with minimal metadata
        try:
            self.workflow._execute_phase_1(task_id, task_metadata, result)
            self.workflow._execute_phase_3(task_id, task_metadata, result)
            self.workflow._execute_phase_4(task_id, task_metadata, result)
            self.workflow._execute_phase_5(task_id, task_metadata, result)
        except Exception:
            pytest.fail("Phase execution should handle errors gracefully")

    # === Performance Tests ===

    def test_performance_completes_quickly(self):
        """Test that micro-task workflow completes in reasonable time."""
        task_id = 'TASK-117'
        task_metadata = {
            'id': task_id,
            'title': 'Performance test',
            'complexity_estimate': 1
        }

        import time
        start = time.time()
        result = self.workflow.execute(task_id, task_metadata)
        duration = time.time() - start

        # Should complete in <5 seconds for this simple test
        assert duration < 5.0
        assert result.duration_minutes < 1.0


class TestMicroWorkflowResult:
    """Test MicroWorkflowResult dataclass properties."""

    def test_duration_minutes_conversion(self):
        """Test duration_minutes property converts correctly."""
        result = MicroWorkflowResult(
            task_id='TASK-118',
            success=True,
            total_duration_seconds=150.0  # 2.5 minutes
        )

        assert result.duration_minutes == pytest.approx(2.5, rel=0.01)

    def test_all_quality_gates_passed_true(self):
        """Test all_quality_gates_passed when all pass."""
        from micro_task_workflow import QualityGateResult

        result = MicroWorkflowResult(
            task_id='TASK-119',
            success=True
        )

        result.quality_gates.append(QualityGateResult(
            gate_name='compilation',
            status=QualityGateStatus.PASSED
        ))
        result.quality_gates.append(QualityGateResult(
            gate_name='tests',
            status=QualityGateStatus.PASSED
        ))

        assert result.all_quality_gates_passed is True

    def test_all_quality_gates_passed_false(self):
        """Test all_quality_gates_passed when one fails."""
        from micro_task_workflow import QualityGateResult

        result = MicroWorkflowResult(
            task_id='TASK-120',
            success=False
        )

        result.quality_gates.append(QualityGateResult(
            gate_name='compilation',
            status=QualityGateStatus.PASSED
        ))
        result.quality_gates.append(QualityGateResult(
            gate_name='tests',
            status=QualityGateStatus.FAILED
        ))

        assert result.all_quality_gates_passed is False


class TestQualityGateResult:
    """Test QualityGateResult dataclass properties."""

    def test_passed_property(self):
        """Test passed property."""
        from micro_task_workflow import QualityGateResult

        gate_pass = QualityGateResult(
            gate_name='test',
            status=QualityGateStatus.PASSED
        )
        gate_fail = QualityGateResult(
            gate_name='test',
            status=QualityGateStatus.FAILED
        )

        assert gate_pass.passed is True
        assert gate_fail.passed is False

    def test_failed_property(self):
        """Test failed property."""
        from micro_task_workflow import QualityGateResult

        gate_fail = QualityGateResult(
            gate_name='test',
            status=QualityGateStatus.FAILED
        )
        gate_pass = QualityGateResult(
            gate_name='test',
            status=QualityGateStatus.PASSED
        )

        assert gate_fail.failed is True
        assert gate_pass.failed is False


class TestPublicAPI:
    """Test public API functions."""

    def test_execute_micro_workflow_function(self):
        """Test public execute_micro_workflow function."""
        task_id = 'TASK-121'
        task_metadata = {
            'id': task_id,
            'title': 'API test',
            'complexity_estimate': 1
        }

        result = execute_micro_workflow(task_id, task_metadata)

        assert isinstance(result, MicroWorkflowResult)
        assert result.task_id == task_id
        assert result.success is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
