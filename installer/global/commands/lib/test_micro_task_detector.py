"""
Unit tests for MicroTaskDetector

Tests cover:
- Micro-task detection heuristics
- High-risk keyword detection
- File count estimation
- Effort parsing
- Confidence scoring
- Documentation-only exception
- Auto-suggestion behavior
"""

import pytest
from micro_task_detector import (
    MicroTaskDetector,
    MicroTaskAnalysis,
    analyze_micro_task,
    validate_micro_mode,
    suggest_micro_mode,
)


class TestMicroTaskDetector:
    """Test suite for MicroTaskDetector class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.detector = MicroTaskDetector()

    # === Basic Micro-Task Detection ===

    def test_micro_task_typo_fix(self):
        """Test that simple typo fix is identified as micro-task."""
        task_metadata = {
            'id': 'TASK-042',
            'title': 'Fix typo in error message',
            'description': 'Change "sucessful" to "successful" in UserService.cs',
            'complexity_estimate': 1,
            'estimated_effort': '5 minutes',
            'labels': []
        }

        analysis = self.detector.analyze(task_metadata)

        assert analysis.is_micro_task is True
        assert analysis.confidence_score >= 0.9
        assert len(analysis.blocking_reasons) == 0

    def test_micro_task_documentation_update(self):
        """Test that documentation update is identified as micro-task."""
        task_metadata = {
            'id': 'TASK-043',
            'title': 'Update README with installation instructions',
            'description': 'Add section about npm install requirements',
            'complexity_estimate': 1,
            'estimated_effort': '15 minutes',
            'labels': ['documentation']
        }

        analysis = self.detector.analyze(task_metadata)

        assert analysis.is_micro_task is True
        assert analysis.confidence_score >= 0.9  # Doc-only override

    def test_not_micro_task_api_endpoint(self):
        """Test that new API endpoint is NOT a micro-task."""
        task_metadata = {
            'id': 'TASK-044',
            'title': 'Add GET /api/users endpoint',
            'description': 'Create new endpoint to fetch all users',
            'complexity_estimate': 4,
            'estimated_effort': '2 hours',
            'labels': ['backend']
        }

        analysis = self.detector.analyze(task_metadata)

        assert analysis.is_micro_task is False
        assert len(analysis.blocking_reasons) > 0

    def test_not_micro_task_high_complexity(self):
        """Test that high complexity blocks micro-task mode."""
        task_metadata = {
            'id': 'TASK-050',
            'title': 'Refactor database layer',
            'description': 'Refactor to use repository pattern',
            'complexity_estimate': 7,
            'estimated_effort': '30 minutes',  # Short effort to isolate complexity check
            'labels': []
        }

        analysis = self.detector.analyze(task_metadata)

        assert analysis.is_micro_task is False
        assert any('Complexity too high' in reason for reason in analysis.blocking_reasons)

    # === High-Risk Keyword Detection ===

    def test_high_risk_security_keywords(self):
        """Test that security keywords block micro-task mode."""
        security_tasks = [
            {
                'id': 'TASK-051',
                'title': 'Add authentication to API',
                'description': 'Implement JWT authentication',
                'complexity_estimate': 1,
                'estimated_effort': '30 minutes'
            },
            {
                'id': 'TASK-052',
                'title': 'Update password hashing',
                'description': 'Switch to bcrypt',
                'complexity_estimate': 1,
                'estimated_effort': '30 minutes'
            },
            {
                'id': 'TASK-053',
                'title': 'Add OAuth2 provider',
                'description': 'Integrate with Google OAuth',
                'complexity_estimate': 1,
                'estimated_effort': '30 minutes'
            }
        ]

        for task in security_tasks:
            analysis = self.detector.analyze(task)
            assert analysis.is_micro_task is False
            assert any('security' in reason.lower() for reason in analysis.blocking_reasons)

    def test_high_risk_database_keywords(self):
        """Test that database keywords block micro-task mode."""
        db_tasks = [
            {
                'id': 'TASK-054',
                'title': 'Add database migration',
                'description': 'Create migration for new column',
                'complexity_estimate': 1,
                'estimated_effort': '30 minutes'
            },
            {
                'id': 'TASK-055',
                'title': 'Update schema',
                'description': 'Alter table to add index',
                'complexity_estimate': 1,
                'estimated_effort': '30 minutes'
            }
        ]

        for task in db_tasks:
            analysis = self.detector.analyze(task)
            assert analysis.is_micro_task is False
            assert any('data' in reason.lower() for reason in analysis.blocking_reasons)

    def test_high_risk_breaking_change_keywords(self):
        """Test that breaking change keywords block micro-task mode."""
        task_metadata = {
            'id': 'TASK-056',
            'title': 'Update API contract',
            'description': 'Breaking change to /api/users endpoint',
            'complexity_estimate': 1,
            'estimated_effort': '30 minutes'
        }

        analysis = self.detector.analyze(task_metadata)

        assert analysis.is_micro_task is False
        assert any('api' in reason.lower() for reason in analysis.blocking_reasons)

    # === File Count Estimation ===

    def test_estimate_file_count_single_file(self):
        """Test file count estimation for single file."""
        task_metadata = {
            'id': 'TASK-057',
            'title': 'Fix bug in UserService.cs',
            'description': 'Fix null reference in GetUser method',
            'complexity_estimate': 1
        }

        file_count = self.detector._estimate_file_count(task_metadata)

        assert file_count == 1

    def test_estimate_file_count_multiple_files(self):
        """Test file count estimation for multiple files."""
        task_metadata = {
            'id': 'TASK-058',
            'title': 'Update service layer',
            'description': 'Update UserService.cs, ProductService.cs, and OrderService.cs',
            'complexity_estimate': 1
        }

        file_count = self.detector._estimate_file_count(task_metadata)

        assert file_count >= 2  # Should detect multiple .cs mentions

    def test_estimate_file_count_explicit_list(self):
        """Test file count estimation with explicit file list."""
        task_metadata = {
            'id': 'TASK-059',
            'title': 'Update multiple files',
            'description': 'Update user-related files',
            'complexity_estimate': 1,
            'files': ['UserService.cs', 'UserRepository.cs', 'UserController.cs']
        }

        file_count = self.detector._estimate_file_count(task_metadata)

        assert file_count == 3

    # === Effort Parsing ===

    def test_parse_estimated_hours_minutes(self):
        """Test parsing effort in minutes."""
        test_cases = [
            ('15 minutes', 0.25),
            ('30 mins', 0.5),
            ('45m', 0.75),
        ]

        for effort_str, expected_hours in test_cases:
            hours = self.detector._parse_estimated_hours(effort_str)
            assert hours == expected_hours

    def test_parse_estimated_hours_hours(self):
        """Test parsing effort in hours."""
        test_cases = [
            ('1 hour', 1.0),
            ('2 hours', 2.0),
            ('3h', 3.0),
        ]

        for effort_str, expected_hours in test_cases:
            hours = self.detector._parse_estimated_hours(effort_str)
            assert hours == expected_hours

    def test_parse_estimated_hours_range(self):
        """Test parsing effort ranges."""
        hours = self.detector._parse_estimated_hours('1-2 hours')
        assert hours == 2.0  # Should use upper bound

    def test_parse_estimated_hours_invalid(self):
        """Test parsing invalid effort strings."""
        hours = self.detector._parse_estimated_hours('unknown')
        assert hours is None

    # === Confidence Scoring ===

    def test_confidence_high_for_simple_task(self):
        """Test that simple tasks get high confidence."""
        task_metadata = {
            'id': 'TASK-060',
            'title': 'Fix typo',
            'description': 'Change "teh" to "the"',
            'complexity_estimate': 1,
            'estimated_effort': '5 minutes'
        }

        analysis = self.detector.analyze(task_metadata)

        assert analysis.confidence_score >= 0.9

    def test_confidence_low_for_multiple_files(self):
        """Test that multiple files reduce confidence."""
        task_metadata = {
            'id': 'TASK-061',
            'title': 'Update services',
            'description': 'Update UserService.cs, ProductService.cs, OrderService.cs',
            'complexity_estimate': 1,
            'estimated_effort': '30 minutes'
        }

        analysis = self.detector.analyze(task_metadata)

        # Multiple files should block micro-task mode
        assert analysis.is_micro_task is False

    def test_confidence_very_low_for_high_risk(self):
        """Test that high-risk keywords reduce confidence significantly."""
        task_metadata = {
            'id': 'TASK-062',
            'title': 'Add authentication',
            'description': 'Implement JWT authentication',
            'complexity_estimate': 1,
            'estimated_effort': '30 minutes'
        }

        analysis = self.detector.analyze(task_metadata)

        assert analysis.confidence_score < 0.5

    def test_confidence_override_for_doc_only(self):
        """Test that documentation-only tasks get confidence override."""
        task_metadata = {
            'id': 'TASK-063',
            'title': 'Update README',
            'description': 'Update installation instructions in README.md',
            'complexity_estimate': 1,
            'estimated_effort': '15 minutes'
        }

        analysis = self.detector.analyze(task_metadata)

        assert analysis.confidence_score >= 0.95  # Doc-only override

    # === Documentation-Only Detection ===

    def test_is_documentation_only_markdown_files(self):
        """Test detection of documentation-only tasks with .md files."""
        task_metadata = {
            'id': 'TASK-064',
            'title': 'Update docs',
            'description': 'Update README.md and CONTRIBUTING.md',
            'files': ['README.md', 'CONTRIBUTING.md']
        }

        is_doc_only = self.detector._is_documentation_only(task_metadata)

        assert is_doc_only is True

    def test_is_documentation_only_mixed_files(self):
        """Test that mixed files don't qualify as doc-only."""
        task_metadata = {
            'id': 'TASK-065',
            'title': 'Update code and docs',
            'description': 'Update UserService.cs and README.md',
            'files': ['UserService.cs', 'README.md']
        }

        is_doc_only = self.detector._is_documentation_only(task_metadata)

        assert is_doc_only is False

    def test_is_documentation_only_heuristic(self):
        """Test heuristic detection of doc-only tasks."""
        task_metadata = {
            'id': 'TASK-066',
            'title': 'Update documentation',
            'description': 'Update API documentation for user endpoints'
        }

        is_doc_only = self.detector._is_documentation_only(task_metadata)

        assert is_doc_only is True

    def test_is_documentation_only_code_mention(self):
        """Test that code mentions prevent doc-only classification."""
        task_metadata = {
            'id': 'TASK-067',
            'title': 'Update documentation',
            'description': 'Update docs and refactor UserService.cs implementation'
        }

        is_doc_only = self.detector._is_documentation_only(task_metadata)

        assert is_doc_only is False

    # === Auto-Suggestion Behavior ===

    def test_suggest_micro_mode_high_confidence(self):
        """Test that high-confidence micro-tasks get suggestion."""
        task_metadata = {
            'id': 'TASK-068',
            'title': 'Fix typo',
            'description': 'Fix typo in error message',
            'complexity_estimate': 1,
            'estimated_effort': '5 minutes'
        }

        suggestion = self.detector.suggest_micro_mode(task_metadata)

        assert suggestion is not None
        assert '--micro' in suggestion
        assert 'TASK-068' in suggestion

    def test_suggest_micro_mode_low_confidence(self):
        """Test that low-confidence tasks don't get suggestion."""
        task_metadata = {
            'id': 'TASK-069',
            'title': 'Add new feature',
            'description': 'Add user registration endpoint',
            'complexity_estimate': 5,
            'estimated_effort': '4 hours'
        }

        suggestion = self.detector.suggest_micro_mode(task_metadata)

        assert suggestion is None

    # === Validation ===

    def test_validate_micro_mode_valid(self):
        """Test validation accepts valid micro-tasks."""
        task_metadata = {
            'id': 'TASK-070',
            'title': 'Fix typo',
            'description': 'Fix typo in comment',
            'complexity_estimate': 1,
            'estimated_effort': '5 minutes'
        }

        is_valid = self.detector.validate_micro_mode(task_metadata)

        assert is_valid is True

    def test_validate_micro_mode_invalid(self):
        """Test validation rejects invalid micro-tasks."""
        task_metadata = {
            'id': 'TASK-071',
            'title': 'Add authentication',
            'description': 'Implement JWT authentication',
            'complexity_estimate': 5,
            'estimated_effort': '4 hours'
        }

        is_valid = self.detector.validate_micro_mode(task_metadata)

        assert is_valid is False

    # === Public API Functions ===

    def test_public_api_analyze(self):
        """Test public API analyze_micro_task function."""
        task_metadata = {
            'id': 'TASK-072',
            'title': 'Fix typo',
            'description': 'Fix typo in error message',
            'complexity_estimate': 1,
            'estimated_effort': '5 minutes'
        }

        analysis = analyze_micro_task(task_metadata)

        assert isinstance(analysis, MicroTaskAnalysis)
        assert analysis.is_micro_task is True

    def test_public_api_validate(self):
        """Test public API validate_micro_mode function."""
        task_metadata = {
            'id': 'TASK-073',
            'title': 'Fix typo',
            'description': 'Fix typo in comment',
            'complexity_estimate': 1,
            'estimated_effort': '5 minutes'
        }

        is_valid = validate_micro_mode(task_metadata)

        assert is_valid is True

    def test_public_api_suggest(self):
        """Test public API suggest_micro_mode function."""
        task_metadata = {
            'id': 'TASK-074',
            'title': 'Fix typo',
            'description': 'Fix typo in error message',
            'complexity_estimate': 1,
            'estimated_effort': '5 minutes'
        }

        suggestion = suggest_micro_mode(task_metadata)

        assert suggestion is not None
        assert 'TASK-074' in suggestion

    # === Edge Cases ===

    def test_edge_case_no_metadata(self):
        """Test handling of minimal task metadata."""
        task_metadata = {
            'id': 'TASK-075',
            'title': 'Fix bug'
        }

        analysis = self.detector.analyze(task_metadata)

        # Should not crash, should have reasonable defaults
        assert isinstance(analysis, MicroTaskAnalysis)
        assert analysis.confidence_score >= 0

    def test_edge_case_zero_complexity(self):
        """Test handling of zero complexity."""
        task_metadata = {
            'id': 'TASK-076',
            'title': 'Fix typo',
            'description': 'Fix typo in comment',
            'complexity_estimate': 0,
            'estimated_effort': '5 minutes'
        }

        analysis = self.detector.analyze(task_metadata)

        assert isinstance(analysis, MicroTaskAnalysis)
        # Zero complexity should not block
        assert not any('Complexity' in reason for reason in analysis.blocking_reasons)

    def test_edge_case_exact_threshold(self):
        """Test handling of values at exact thresholds."""
        task_metadata = {
            'id': 'TASK-077',
            'title': 'Update file',
            'description': 'Update UserService.cs',
            'complexity_estimate': 3,  # Exactly at max_complexity
            'estimated_effort': '1 hour'  # Exactly at max_hours
        }

        analysis = self.detector.analyze(task_metadata)

        # At threshold should be blocked (>= comparison)
        assert analysis.is_micro_task is False


class TestMicroTaskAnalysis:
    """Test suite for MicroTaskAnalysis dataclass."""

    def test_can_use_micro_mode_true(self):
        """Test can_use_micro_mode when eligible."""
        analysis = MicroTaskAnalysis(
            is_micro_task=True,
            blocking_reasons=[],
            confidence_score=0.95,
            suggested_flags=['--micro'],
            metadata={}
        )

        assert analysis.can_use_micro_mode is True

    def test_can_use_micro_mode_false_not_micro(self):
        """Test can_use_micro_mode when not a micro-task."""
        analysis = MicroTaskAnalysis(
            is_micro_task=False,
            blocking_reasons=['Multiple files'],
            confidence_score=0.3,
            suggested_flags=[],
            metadata={}
        )

        assert analysis.can_use_micro_mode is False

    def test_can_use_micro_mode_false_blocking_reasons(self):
        """Test can_use_micro_mode with blocking reasons."""
        analysis = MicroTaskAnalysis(
            is_micro_task=False,
            blocking_reasons=['Security keywords detected'],
            confidence_score=0.1,
            suggested_flags=[],
            metadata={}
        )

        assert analysis.can_use_micro_mode is False

    def test_should_escalate(self):
        """Test should_escalate property."""
        analysis = MicroTaskAnalysis(
            is_micro_task=False,
            blocking_reasons=['High-risk security keywords detected'],
            confidence_score=0.05,
            suggested_flags=[],
            metadata={'risk_analysis': {'has_risks': True}}
        )

        assert analysis.should_escalate is True
