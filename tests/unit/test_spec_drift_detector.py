"""
Unit tests for spec_drift_detector.py

Tests cover:
1. Requirements loading and parsing
2. Coverage analysis
3. Scope creep detection
4. Compliance scoring
5. Report formatting
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
import tempfile
import shutil
import os

# Import the module under test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "installer" / "global" / "commands"))

from lib.spec_drift_detector import (
    SpecDriftDetector,
    Requirement,
    ScopeCreepItem,
    DriftReport,
    format_drift_report
)


@pytest.fixture
def temp_workspace():
    """Create a temporary workspace for testing."""
    temp_dir = tempfile.mkdtemp()
    workspace = Path(temp_dir)

    # Create directory structure
    (workspace / "docs" / "requirements" / "approved").mkdir(parents=True)
    (workspace / "tasks" / "in_progress").mkdir(parents=True)
    (workspace / "src").mkdir(parents=True)

    yield workspace

    # Cleanup
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_task(temp_workspace):
    """Create a sample task file."""
    task_content = """---
id: TASK-042
title: Implement JWT Authentication
status: in_progress
requirements:
  - REQ-042-1
  - REQ-042-2
implementation_files:
  - src/auth_service.py
  - src/token_config.py
---

# Implement JWT Authentication

## Description
Implement JWT token generation with 24-hour expiration.
"""
    task_file = temp_workspace / "tasks" / "in_progress" / "TASK-042.md"
    task_file.write_text(task_content)
    return task_file


@pytest.fixture
def sample_requirements(temp_workspace):
    """Create sample requirement files."""
    req1_content = """---
id: REQ-042-1
title: JWT Token Generation
---

## Requirement

The system shall generate JWT tokens for authenticated users.
"""

    req2_content = """---
id: REQ-042-2
title: Token Expiration
---

## Requirement

When a JWT token is generated, the system shall set expiration to 24 hours.
"""

    req1_file = temp_workspace / "docs" / "requirements" / "approved" / "REQ-042-1.md"
    req2_file = temp_workspace / "docs" / "requirements" / "approved" / "REQ-042-2.md"

    req1_file.write_text(req1_content)
    req2_file.write_text(req2_content)

    return [req1_file, req2_file]


@pytest.fixture
def sample_implementation(temp_workspace):
    """Create sample implementation files."""
    auth_service_content = """
class AuthService:
    def generate_token(self, user_id):
        # Generate JWT token for authenticated users
        token = jwt.encode({'user_id': user_id}, secret_key)
        return token

    def set_expiration(self, token):
        # Set token expiration to 24 hours
        expiration = datetime.now() + timedelta(hours=24)
        return expiration
"""

    token_config_content = """
TOKEN_EXPIRATION_HOURS = 24

class TokenConfig:
    expiration_hours = TOKEN_EXPIRATION_HOURS
"""

    auth_file = temp_workspace / "src" / "auth_service.py"
    config_file = temp_workspace / "src" / "token_config.py"

    auth_file.write_text(auth_service_content)
    config_file.write_text(token_config_content)

    return [auth_file, config_file]


class TestRequirement:
    """Test Requirement dataclass."""

    def test_requirement_creation(self):
        req = Requirement(
            id="REQ-001",
            text="The system shall do something",
            type="ubiquitous"
        )
        assert req.id == "REQ-001"
        assert req.implemented is False
        assert req.implementation_files == []

    def test_requirement_with_implementation(self):
        req = Requirement(
            id="REQ-001",
            text="The system shall do something",
            type="ubiquitous",
            implemented=True,
            implementation_files=["src/feature.py"]
        )
        assert req.implemented is True
        assert len(req.implementation_files) == 1


class TestScopeCreepItem:
    """Test ScopeCreepItem dataclass."""

    def test_scope_creep_creation(self):
        item = ScopeCreepItem(
            file_path="src/extra.py",
            line_number=42,
            description="Unexpected feature",
            code_snippet="class UnexpectedFeature:",
            severity="high"
        )
        assert item.file_path == "src/extra.py"
        assert item.line_number == 42
        assert item.severity == "high"


class TestDriftReport:
    """Test DriftReport dataclass."""

    def test_drift_report_no_issues(self):
        req1 = Requirement("REQ-001", "Test", "ubiquitous", implemented=True)
        report = DriftReport(
            requirements_coverage={"REQ-001": req1},
            scope_creep_items=[],
            compliance_score=100,
            requirements_implemented_percent=100.0,
            scope_creep_percent=0.0
        )
        assert not report.has_issues()

    def test_drift_report_with_scope_creep(self):
        req1 = Requirement("REQ-001", "Test", "ubiquitous", implemented=True)
        creep = ScopeCreepItem("src/extra.py", 1, "Extra", "code", "medium")
        report = DriftReport(
            requirements_coverage={"REQ-001": req1},
            scope_creep_items=[creep],
            compliance_score=95,
            requirements_implemented_percent=100.0,
            scope_creep_percent=5.0
        )
        assert report.has_issues()

    def test_drift_report_with_missing_requirements(self):
        req1 = Requirement("REQ-001", "Test", "ubiquitous", implemented=False)
        report = DriftReport(
            requirements_coverage={"REQ-001": req1},
            scope_creep_items=[],
            compliance_score=90,
            requirements_implemented_percent=0.0,
            scope_creep_percent=0.0
        )
        assert report.has_issues()


class TestSpecDriftDetector:
    """Test SpecDriftDetector main functionality."""

    def test_detector_initialization(self, temp_workspace):
        detector = SpecDriftDetector(temp_workspace)
        assert detector.workspace_root == temp_workspace
        assert detector.requirements_dir == temp_workspace / "docs" / "requirements"
        assert detector.tasks_dir == temp_workspace / "tasks"

    def test_load_task(self, temp_workspace, sample_task):
        detector = SpecDriftDetector(temp_workspace)
        task_data = detector._load_task("TASK-042")

        assert task_data['id'] == "TASK-042"
        assert task_data['title'] == "Implement JWT Authentication"
        assert "REQ-042-1" in task_data['requirements']
        assert "REQ-042-2" in task_data['requirements']

    def test_load_task_not_found(self, temp_workspace):
        detector = SpecDriftDetector(temp_workspace)

        with pytest.raises(FileNotFoundError):
            detector._load_task("TASK-999")

    def test_load_requirements(self, temp_workspace, sample_task, sample_requirements):
        detector = SpecDriftDetector(temp_workspace)
        task_data = detector._load_task("TASK-042")
        requirements = detector._load_requirements(task_data)

        assert len(requirements) == 2
        assert requirements[0].id in ["REQ-042-1", "REQ-042-2"]
        assert requirements[1].id in ["REQ-042-1", "REQ-042-2"]

    def test_extract_keywords(self, temp_workspace):
        detector = SpecDriftDetector(temp_workspace)
        text = "The system shall generate JWT tokens for authenticated users"

        keywords = detector._extract_keywords(text)

        assert "generate" in keywords
        assert "tokens" in keywords
        assert "authenticated" in keywords
        assert "users" in keywords
        # Stop words should be filtered
        assert "the" not in keywords
        assert "shall" not in keywords

    def test_file_implements_requirement(self, temp_workspace, sample_implementation):
        detector = SpecDriftDetector(temp_workspace)
        keywords = {"generate", "token", "authenticated", "users"}

        auth_file = sample_implementation[0]
        result = detector._file_implements_requirement(auth_file, keywords)

        # Should find at least 50% of keywords
        assert result is True

    def test_calculate_coverage_full(
        self,
        temp_workspace,
        sample_task,
        sample_requirements,
        sample_implementation
    ):
        detector = SpecDriftDetector(temp_workspace)
        task_data = detector._load_task("TASK-042")
        requirements = detector._load_requirements(task_data)
        impl_files = detector._get_implementation_files(task_data)

        coverage = detector._calculate_coverage(requirements, impl_files)

        # Both requirements should be implemented
        assert all(req.implemented for req in coverage.values())

    def test_detect_scope_creep_none(
        self,
        temp_workspace,
        sample_task,
        sample_requirements,
        sample_implementation
    ):
        detector = SpecDriftDetector(temp_workspace)
        task_data = detector._load_task("TASK-042")
        requirements = detector._load_requirements(task_data)
        impl_files = detector._get_implementation_files(task_data)

        scope_creep = detector._detect_scope_creep(requirements, impl_files)

        # No scope creep in sample implementation
        assert len(scope_creep) == 0

    def test_detect_scope_creep_with_refresh(self, temp_workspace, sample_task, sample_requirements):
        """Test detection of token refresh mechanism (common scope creep)."""
        # Create implementation with scope creep
        creep_content = """
class AuthService:
    def generate_token(self, user_id):
        return jwt.encode({'user_id': user_id}, secret_key)

    class TokenRefresh:
        def refresh_token(self, old_token):
            # This is scope creep - not in requirements
            return new_token
"""
        creep_file = temp_workspace / "src" / "auth_service.py"
        creep_file.write_text(creep_content)

        detector = SpecDriftDetector(temp_workspace)
        task_data = detector._load_task("TASK-042")
        requirements = detector._load_requirements(task_data)
        impl_files = [creep_file]

        scope_creep = detector._detect_scope_creep(requirements, impl_files)

        # Should detect TokenRefresh as scope creep
        assert len(scope_creep) > 0
        assert any("refresh" in item.description.lower() for item in scope_creep)

    def test_calculate_compliance_perfect(self, temp_workspace):
        detector = SpecDriftDetector(temp_workspace)

        req1 = Requirement("REQ-001", "Test", "ubiquitous", implemented=True)
        req2 = Requirement("REQ-002", "Test", "ubiquitous", implemented=True)
        coverage = {"REQ-001": req1, "REQ-002": req2}
        scope_creep = []

        score = detector._calculate_compliance(coverage, scope_creep)

        assert score == 100

    def test_calculate_compliance_missing_requirement(self, temp_workspace):
        detector = SpecDriftDetector(temp_workspace)

        req1 = Requirement("REQ-001", "Test", "ubiquitous", implemented=True)
        req2 = Requirement("REQ-002", "Test", "ubiquitous", implemented=False)
        coverage = {"REQ-001": req1, "REQ-002": req2}
        scope_creep = []

        score = detector._calculate_compliance(coverage, scope_creep)

        # -10 for unimplemented requirement
        assert score == 90

    def test_calculate_compliance_with_scope_creep(self, temp_workspace):
        detector = SpecDriftDetector(temp_workspace)

        req1 = Requirement("REQ-001", "Test", "ubiquitous", implemented=True)
        coverage = {"REQ-001": req1}
        creep = ScopeCreepItem("src/extra.py", 1, "Extra", "code", "medium")
        scope_creep = [creep]

        score = detector._calculate_compliance(coverage, scope_creep)

        # -5 for scope creep
        assert score == 95

    def test_calculate_requirements_percent_full(self, temp_workspace):
        detector = SpecDriftDetector(temp_workspace)

        req1 = Requirement("REQ-001", "Test", "ubiquitous", implemented=True)
        req2 = Requirement("REQ-002", "Test", "ubiquitous", implemented=True)
        coverage = {"REQ-001": req1, "REQ-002": req2}

        percent = detector._calculate_requirements_percent(coverage)

        assert percent == 100.0

    def test_calculate_requirements_percent_partial(self, temp_workspace):
        detector = SpecDriftDetector(temp_workspace)

        req1 = Requirement("REQ-001", "Test", "ubiquitous", implemented=True)
        req2 = Requirement("REQ-002", "Test", "ubiquitous", implemented=False)
        coverage = {"REQ-001": req1, "REQ-002": req2}

        percent = detector._calculate_requirements_percent(coverage)

        assert percent == 50.0

    def test_full_drift_analysis(
        self,
        temp_workspace,
        sample_task,
        sample_requirements,
        sample_implementation
    ):
        """Integration test of full drift analysis."""
        detector = SpecDriftDetector(temp_workspace)
        report = detector.analyze_drift("TASK-042")

        assert isinstance(report, DriftReport)
        assert len(report.requirements_coverage) == 2
        assert report.requirements_implemented_percent >= 0
        assert report.scope_creep_percent >= 0
        assert 0 <= report.compliance_score <= 100


class TestFormatDriftReport:
    """Test report formatting."""

    def test_format_report_perfect(self):
        req1 = Requirement(
            "REQ-001",
            "The system shall do something",
            "ubiquitous",
            implemented=True,
            implementation_files=["src/feature.py"]
        )
        report = DriftReport(
            requirements_coverage={"REQ-001": req1},
            scope_creep_items=[],
            compliance_score=100,
            requirements_implemented_percent=100.0,
            scope_creep_percent=0.0
        )

        output = format_drift_report(report, "TASK-042")

        assert "TASK-042" in output
        assert "REQ-001" in output
        assert "✅" in output
        assert "100/100" in output
        assert "EXCELLENT" in output

    def test_format_report_with_issues(self):
        req1 = Requirement(
            "REQ-001",
            "The system shall do something",
            "ubiquitous",
            implemented=False
        )
        creep = ScopeCreepItem(
            "src/extra.py",
            42,
            "Token refresh mechanism",
            "class TokenRefresh:",
            "medium"
        )
        report = DriftReport(
            requirements_coverage={"REQ-001": req1},
            scope_creep_items=[creep],
            compliance_score=85,
            requirements_implemented_percent=0.0,
            scope_creep_percent=5.0
        )

        output = format_drift_report(report, "TASK-042")

        assert "TASK-042" in output
        assert "REQ-001" in output
        assert "NOT IMPLEMENTED" in output
        assert "SCOPE CREEP DETECTED" in output
        assert "Token refresh" in output
        assert "85/100" in output

    def test_format_report_sections(self):
        """Test that all report sections are present."""
        req1 = Requirement("REQ-001", "Test", "ubiquitous", implemented=True)
        report = DriftReport(
            requirements_coverage={"REQ-001": req1},
            scope_creep_items=[],
            compliance_score=100,
            requirements_implemented_percent=100.0,
            scope_creep_percent=0.0
        )

        output = format_drift_report(report, "TASK-042")

        # Check for required sections
        assert "REQUIREMENTS COVERAGE" in output
        assert "COMPLIANCE SCORECARD" in output
        assert "Requirements Implemented:" in output
        assert "Scope Creep:" in output
        assert "Overall Compliance:" in output


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_requirements(self, temp_workspace):
        """Test handling of task with no requirements."""
        task_content = """---
id: TASK-999
title: Task with no requirements
status: in_progress
requirements: []
implementation_files: []
---
"""
        task_file = temp_workspace / "tasks" / "in_progress" / "TASK-999.md"
        task_file.write_text(task_content)

        detector = SpecDriftDetector(temp_workspace)
        task_data = detector._load_task("TASK-999")
        requirements = detector._load_requirements(task_data)

        assert len(requirements) == 0

    def test_missing_implementation_files(self, temp_workspace, sample_task):
        """Test handling of missing implementation files."""
        detector = SpecDriftDetector(temp_workspace)
        task_data = detector._load_task("TASK-042")

        # Implementation files don't exist yet
        impl_files = detector._get_implementation_files(task_data)

        # Should not crash, just return empty results
        assert isinstance(impl_files, list)

    def test_binary_file_handling(self, temp_workspace):
        """Test that binary files don't crash the detector."""
        # Create a binary file
        binary_file = temp_workspace / "src" / "image.png"
        binary_file.write_bytes(b'\x89PNG\r\n\x1a\n\x00\x00\x00')

        detector = SpecDriftDetector(temp_workspace)
        keywords = {"test", "image"}

        # Should handle gracefully
        result = detector._file_implements_requirement(binary_file, keywords)
        assert result is False

    def test_requirement_type_detection(self, temp_workspace):
        """Test detection of different EARS requirement types."""
        detector = SpecDriftDetector(temp_workspace)

        # Event-driven
        req_event = """
## Requirement

When a user clicks submit, the system shall validate the form.
"""
        req_file = temp_workspace / "docs" / "requirements" / "approved" / "REQ-EVENT.md"
        req_file.write_text(req_event)
        parsed = detector._parse_requirement_file(req_file, "REQ-EVENT")
        assert parsed.type == "event"

        # State-driven
        req_state = """
## Requirement

While the user is logged in, the system shall display their profile.
"""
        req_file2 = temp_workspace / "docs" / "requirements" / "approved" / "REQ-STATE.md"
        req_file2.write_text(req_state)
        parsed = detector._parse_requirement_file(req_file2, "REQ-STATE")
        assert parsed.type == "state"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
