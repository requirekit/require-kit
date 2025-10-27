"""
Basic sanity tests for micro-task modules (no pytest required)

This script can be run directly with python3 to verify basic functionality.
"""

import sys
from micro_task_detector import MicroTaskDetector, MicroTaskAnalysis
from micro_task_workflow import MicroTaskWorkflow, MicroWorkflowResult


def test_detector_basic():
    """Test basic detector functionality."""
    print("Testing MicroTaskDetector basic functionality...")

    detector = MicroTaskDetector()

    # Test 1: Simple typo fix (should be micro-task)
    task1 = {
        'id': 'TASK-001',
        'title': 'Fix typo in error message',
        'description': "Change 'occured' to 'occurred'",
        'complexity_estimate': 1,
        'estimated_effort': '15 minutes',
        'labels': []
    }

    analysis1 = detector.analyze(task1)
    assert analysis1.is_micro_task is True, "Simple typo should be micro-task"
    assert len(analysis1.blocking_reasons) == 0, "No blocking reasons expected"
    print("  ✓ Simple typo fix correctly identified as micro-task")

    # Test 2: Security task (should NOT be micro-task)
    task2 = {
        'id': 'TASK-002',
        'title': 'Add authentication endpoint',
        'description': 'Implement JWT authentication',
        'complexity_estimate': 5,
        'estimated_effort': '4 hours',
        'labels': ['security']
    }

    analysis2 = detector.analyze(task2)
    assert analysis2.is_micro_task is False, "Security task should NOT be micro-task"
    assert len(analysis2.blocking_reasons) > 0, "Should have blocking reasons"
    print("  ✓ Security task correctly blocked from micro-task mode")

    # Test 3: Documentation update (should be micro-task)
    task3 = {
        'id': 'TASK-003',
        'title': 'Update README',
        'description': 'Add installation instructions',
        'complexity_estimate': 1,
        'estimated_effort': '30 minutes'
    }

    analysis3 = detector.analyze(task3)
    assert analysis3.is_micro_task is True, "Doc update should be micro-task"
    print("  ✓ Documentation update correctly identified as micro-task")

    print("✅ MicroTaskDetector basic tests passed\n")


def test_workflow_basic():
    """Test basic workflow functionality."""
    print("Testing MicroTaskWorkflow basic functionality...")

    workflow = MicroTaskWorkflow()

    # Test: Execute workflow with simple task
    task_id = 'TASK-100'
    task_metadata = {
        'id': task_id,
        'title': 'Fix typo',
        'description': 'Fix spelling error',
        'complexity_estimate': 1
    }

    result = workflow.execute(task_id, task_metadata)

    assert isinstance(result, MicroWorkflowResult), "Should return MicroWorkflowResult"
    assert result.task_id == task_id, "Task ID should match"
    assert result.success is True, "Workflow should succeed"
    assert result.final_state == 'in_review', "Should transition to in_review"
    assert len(result.phases_executed) > 0, "Should execute some phases"
    assert len(result.phases_skipped) == 5, "Should skip 5 planning phases"
    assert result.duration_minutes < 5, "Should complete quickly"
    print("  ✓ Workflow execution completed successfully")
    print(f"  ✓ Executed {len(result.phases_executed)} phases, skipped {len(result.phases_skipped)} phases")
    print(f"  ✓ Duration: {result.duration_minutes:.2f} minutes")

    print("✅ MicroTaskWorkflow basic tests passed\n")


def test_effort_parsing():
    """Test effort parsing functionality."""
    print("Testing effort parsing...")

    detector = MicroTaskDetector()

    test_cases = [
        ('15 minutes', 0.25),
        ('30 mins', 0.5),
        ('1 hour', 1.0),
        ('2 hours', 2.0),
        ('1-2 hours', 2.0),  # Takes max
        ('45m', 0.75),
    ]

    for effort_str, expected_hours in test_cases:
        parsed = detector._parse_estimated_hours(effort_str)
        assert abs(parsed - expected_hours) < 0.01, f"Failed to parse '{effort_str}'"
        print(f"  ✓ Parsed '{effort_str}' as {parsed:.2f} hours")

    print("✅ Effort parsing tests passed\n")


def test_high_risk_detection():
    """Test high-risk keyword detection."""
    print("Testing high-risk keyword detection...")

    detector = MicroTaskDetector()

    high_risk_keywords = [
        ('Add authentication', True),
        ('Update database schema', True),
        ('Breaking API change', True),
        ('Fix typo in comment', False),
        ('Update documentation', False),
    ]

    for description, should_be_risky in high_risk_keywords:
        task = {
            'id': 'TEST',
            'title': description,
            'description': description,
            'complexity_estimate': 1
        }
        result = detector._detect_high_risk(task)
        is_risky = result['has_risks']

        assert is_risky == should_be_risky, f"Risk detection failed for: {description}"
        status = "risky" if is_risky else "safe"
        print(f"  ✓ '{description}' correctly identified as {status}")

    print("✅ High-risk detection tests passed\n")


def test_confidence_scoring():
    """Test confidence scoring."""
    print("Testing confidence scoring...")

    detector = MicroTaskDetector()

    # High confidence: simple, single file, no risk
    conf1 = detector._calculate_confidence(
        file_count=1,
        hours=0.25,
        complexity=1,
        has_risks=False,
        is_doc_only=False
    )
    assert conf1 >= 0.8, "Should have high confidence for simple task"
    print(f"  ✓ Simple task confidence: {conf1:.2%}")

    # Low confidence: multiple files, high risk
    conf2 = detector._calculate_confidence(
        file_count=5,
        hours=2.0,
        complexity=5,
        has_risks=True,
        is_doc_only=False
    )
    assert conf2 < 0.2, "Should have low confidence for complex task"
    print(f"  ✓ Complex task confidence: {conf2:.2%}")

    # Override: doc-only should be high confidence
    conf3 = detector._calculate_confidence(
        file_count=10,
        hours=2.0,
        complexity=5,
        has_risks=False,
        is_doc_only=True
    )
    assert conf3 >= 0.9, "Doc-only should override other penalties"
    print(f"  ✓ Doc-only override confidence: {conf3:.2%}")

    print("✅ Confidence scoring tests passed\n")


def run_all_tests():
    """Run all basic tests."""
    print("\n" + "="*70)
    print("MICRO-TASK MODULE BASIC SANITY TESTS")
    print("="*70 + "\n")

    try:
        test_detector_basic()
        test_workflow_basic()
        test_effort_parsing()
        test_high_risk_detection()
        test_confidence_scoring()

        print("="*70)
        print("✅ ALL TESTS PASSED")
        print("="*70)
        return 0

    except AssertionError as e:
        print("\n" + "="*70)
        print(f"❌ TEST FAILED: {e}")
        print("="*70)
        return 1

    except Exception as e:
        print("\n" + "="*70)
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("="*70)
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
