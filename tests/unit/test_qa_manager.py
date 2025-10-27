"""
Unit tests for Q&A Manager implementation.

Tests cover:
    - QAExchange and QASession dataclasses
    - KeywordMatcher keyword-based matching
    - PlanSectionExtractor section extraction
    - QAManager interactive session workflow
    - Metadata persistence
"""

import pytest
import yaml
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call
from typing import Dict, Any

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "installer/global/commands/lib"))

from complexity_models import (
    ComplexityScore,
    FactorScore,
    ForceReviewTrigger,
    ReviewMode,
    ImplementationPlan,
)
from qa_manager import (
    QAExchange,
    QASession,
    KeywordMatcher,
    PlanSectionExtractor,
    QAManager,
)


# Test Fixtures
@pytest.fixture
def mock_complexity_score():
    """Create mock ComplexityScore for testing."""
    factor_scores = [
        FactorScore(
            factor_name="File Complexity",
            score=2.0,
            max_score=3.0,
            justification="6 files to create/modify"
        ),
        FactorScore(
            factor_name="Pattern Familiarity",
            score=1.0,
            max_score=2.0,
            justification="Uses Strategy pattern"
        ),
    ]

    return ComplexityScore(
        total_score=5,
        factor_scores=factor_scores,
        forced_review_triggers=[],
        review_mode=ReviewMode.QUICK_OPTIONAL,
        calculation_timestamp=datetime.utcnow(),
        metadata={}
    )


@pytest.fixture
def mock_implementation_plan(mock_complexity_score):
    """Create mock ImplementationPlan for testing."""
    plan = ImplementationPlan(
        task_id="TASK-001",
        files_to_create=[
            "src/auth/login.py",
            "src/auth/session.py",
            "tests/test_auth.py"
        ],
        patterns_used=["Strategy", "Factory"],
        external_dependencies=["jwt", "bcrypt"],
        estimated_loc=350,
        risk_indicators=["authentication"],
        raw_plan="Implement login system with JWT authentication using Strategy pattern",
        test_summary="Unit tests for auth logic, integration tests for API",
        risk_details=[
            {
                "severity": "high",
                "description": "Authentication bypass vulnerability",
                "mitigation": "Use established JWT library"
            }
        ],
        phases=[
            "Phase 1: JWT token generation",
            "Phase 2: Login endpoint implementation",
            "Phase 3: Session management"
        ],
        implementation_instructions="Create JWT-based authentication with Strategy pattern for flexibility",
        estimated_duration="2-3 hours"
    )
    plan.complexity_score = mock_complexity_score
    return plan


@pytest.fixture
def mock_task_metadata():
    """Create mock task metadata for testing."""
    return {
        "id": "TASK-001",
        "title": "Implement JWT Authentication",
        "priority": "high",
        "status": "in_progress"
    }


# QAExchange Tests
class TestQAExchange:
    """Test QAExchange dataclass."""

    def test_qa_exchange_creation(self):
        """Test creating QAExchange instance."""
        timestamp = datetime.utcnow()
        exchange = QAExchange(
            question="Why Strategy pattern?",
            answer="Strategy pattern provides flexibility...",
            confidence=8,
            timestamp=timestamp
        )

        assert exchange.question == "Why Strategy pattern?"
        assert exchange.answer == "Strategy pattern provides flexibility..."
        assert exchange.confidence == 8
        assert exchange.timestamp == timestamp

    def test_qa_exchange_to_dict(self):
        """Test QAExchange serialization to dict."""
        timestamp = datetime(2025, 10, 10, 10, 15, 0)
        exchange = QAExchange(
            question="Why Strategy pattern?",
            answer="Strategy pattern provides flexibility...",
            confidence=8,
            timestamp=timestamp
        )

        result = exchange.to_dict()

        assert result["question"] == "Why Strategy pattern?"
        assert result["answer"] == "Strategy pattern provides flexibility..."
        assert result["confidence"] == 8
        assert result["timestamp"] == "2025-10-10T10:15:00Z"


# QASession Tests
class TestQASession:
    """Test QASession dataclass."""

    def test_qa_session_creation(self):
        """Test creating QASession instance."""
        started = datetime.utcnow()
        session = QASession(
            session_id="qa-001",
            task_id="TASK-001",
            started_at=started
        )

        assert session.session_id == "qa-001"
        assert session.task_id == "TASK-001"
        assert session.started_at == started
        assert session.exchanges == []
        assert session.ended_at is None
        assert session.exit_reason is None

    def test_qa_session_with_exchanges(self):
        """Test QASession with exchanges."""
        started = datetime.utcnow()
        session = QASession(
            session_id="qa-001",
            task_id="TASK-001",
            started_at=started
        )

        # Add exchanges
        exchange1 = QAExchange(
            question="Why?",
            answer="Because...",
            confidence=8,
            timestamp=datetime.utcnow()
        )
        session.exchanges.append(exchange1)

        assert len(session.exchanges) == 1
        assert session.exchanges[0].question == "Why?"

    def test_qa_session_to_dict(self):
        """Test QASession serialization to dict."""
        started = datetime(2025, 10, 10, 10, 15, 0)
        ended = datetime(2025, 10, 10, 10, 20, 0)

        session = QASession(
            session_id="qa-001",
            task_id="TASK-001",
            started_at=started,
            ended_at=ended,
            exit_reason="back"
        )

        exchange = QAExchange(
            question="Why?",
            answer="Because...",
            confidence=8,
            timestamp=datetime(2025, 10, 10, 10, 16, 0)
        )
        session.exchanges.append(exchange)

        result = session.to_dict()

        assert result["session_id"] == "qa-001"
        assert result["task_id"] == "TASK-001"
        assert result["started_at"] == "2025-10-10T10:15:00Z"
        assert result["ended_at"] == "2025-10-10T10:20:00Z"
        assert result["exit_reason"] == "back"
        assert len(result["exchanges"]) == 1


# KeywordMatcher Tests
class TestKeywordMatcher:
    """Test KeywordMatcher keyword-based matching."""

    def test_match_rationale_keywords(self):
        """Test matching rationale-related questions."""
        matcher = KeywordMatcher()

        category, keywords = matcher.match_question("Why was this approach chosen?")

        assert category == "rationale"
        assert "why" in keywords
        assert "chosen" in keywords

    def test_match_testing_keywords(self):
        """Test matching testing-related questions."""
        matcher = KeywordMatcher()

        category, keywords = matcher.match_question("How will this be tested?")

        assert category == "testing"
        assert "tested" in keywords

    def test_match_risk_keywords(self):
        """Test matching risk-related questions."""
        matcher = KeywordMatcher()

        category, keywords = matcher.match_question("What are the risks?")

        assert category == "risks"
        assert "risks" in keywords

    def test_match_duration_keywords(self):
        """Test matching duration-related questions."""
        matcher = KeywordMatcher()

        category, keywords = matcher.match_question("How long will this take?")

        assert category == "duration"
        assert "long" in keywords

    def test_match_files_keywords(self):
        """Test matching files-related questions."""
        matcher = KeywordMatcher()

        category, keywords = matcher.match_question("What files will be created?")

        assert category == "files"
        assert "files" in keywords
        assert "create" in keywords

    def test_match_dependencies_keywords(self):
        """Test matching dependency-related questions."""
        matcher = KeywordMatcher()

        category, keywords = matcher.match_question("What dependencies are needed?")

        assert category == "dependencies"
        assert "depend" in keywords

    def test_match_phases_keywords(self):
        """Test matching phase-related questions."""
        matcher = KeywordMatcher()

        category, keywords = matcher.match_question("What are the implementation phases?")

        assert category == "phases"
        assert "phase" in keywords

    def test_match_complexity_keywords(self):
        """Test matching complexity-related questions."""
        matcher = KeywordMatcher()

        category, keywords = matcher.match_question("How complex is this?")

        assert category == "complexity"
        assert "complex" in keywords

    def test_match_no_keywords_general(self):
        """Test matching question with no specific keywords."""
        matcher = KeywordMatcher()

        category, keywords = matcher.match_question("Tell me about the plan")

        assert category == "general"
        assert keywords == []

    def test_match_case_insensitive(self):
        """Test keyword matching is case insensitive."""
        matcher = KeywordMatcher()

        category1, _ = matcher.match_question("WHY WAS THIS CHOSEN?")
        category2, _ = matcher.match_question("why was this chosen?")

        assert category1 == category2 == "rationale"

    def test_match_multiple_keywords(self):
        """Test matching with multiple keywords from same category."""
        matcher = KeywordMatcher()

        category, keywords = matcher.match_question("Why was this rationale chosen?")

        assert category == "rationale"
        assert "why" in keywords
        assert "rationale" in keywords
        assert "chosen" in keywords


# PlanSectionExtractor Tests
class TestPlanSectionExtractor:
    """Test PlanSectionExtractor section extraction."""

    def test_extract_rationale(self, mock_implementation_plan):
        """Test extracting rationale section."""
        extractor = PlanSectionExtractor()

        section = extractor.extract_section(mock_implementation_plan, "rationale")

        assert section["section_title"] == "Rationale & Approach"
        assert "Strategy" in section["content"]
        assert "Factory" in section["content"]
        assert section["source"] == "Implementation Plan"

    def test_extract_testing(self, mock_implementation_plan):
        """Test extracting testing section."""
        extractor = PlanSectionExtractor()

        section = extractor.extract_section(mock_implementation_plan, "testing")

        assert section["section_title"] == "Test Strategy"
        assert "Unit tests for auth logic" in section["content"]
        assert section["source"] == "Implementation Plan"

    def test_extract_risks(self, mock_implementation_plan):
        """Test extracting risks section."""
        extractor = PlanSectionExtractor()

        section = extractor.extract_section(mock_implementation_plan, "risks")

        assert section["section_title"] == "Risk Assessment"
        assert "Authentication bypass vulnerability" in section["content"]
        assert "HIGH" in section["content"]
        assert section["source"] == "Implementation Plan"

    def test_extract_duration(self, mock_implementation_plan):
        """Test extracting duration section."""
        extractor = PlanSectionExtractor()

        section = extractor.extract_section(mock_implementation_plan, "duration")

        assert section["section_title"] == "Time Estimates"
        assert "2-3 hours" in section["content"]
        assert "350" in section["content"]  # LOC
        assert section["source"] == "Implementation Plan"

    def test_extract_files(self, mock_implementation_plan):
        """Test extracting files section."""
        extractor = PlanSectionExtractor()

        section = extractor.extract_section(mock_implementation_plan, "files")

        assert section["section_title"] == "Files"
        assert "3 files" in section["content"]
        assert "src/auth/login.py" in section["content"]
        assert section["source"] == "Implementation Plan"

    def test_extract_dependencies(self, mock_implementation_plan):
        """Test extracting dependencies section."""
        extractor = PlanSectionExtractor()

        section = extractor.extract_section(mock_implementation_plan, "dependencies")

        assert section["section_title"] == "Dependencies"
        assert "2 dependencies" in section["content"]
        assert "jwt" in section["content"]
        assert "bcrypt" in section["content"]
        assert section["source"] == "Implementation Plan"

    def test_extract_phases(self, mock_implementation_plan):
        """Test extracting phases section."""
        extractor = PlanSectionExtractor()

        section = extractor.extract_section(mock_implementation_plan, "phases")

        assert section["section_title"] == "Implementation Order"
        assert "3 phases" in section["content"]
        assert "Phase 1: JWT token generation" in section["content"]
        assert section["source"] == "Implementation Plan"

    def test_extract_complexity(self, mock_implementation_plan):
        """Test extracting complexity section."""
        extractor = PlanSectionExtractor()

        section = extractor.extract_section(mock_implementation_plan, "complexity")

        assert section["section_title"] == "Complexity Analysis"
        assert "5/10" in section["content"]
        assert "File Complexity" in section["content"]
        assert section["source"] == "Complexity Score"

    def test_extract_general(self, mock_implementation_plan):
        """Test extracting general section."""
        extractor = PlanSectionExtractor()

        section = extractor.extract_section(mock_implementation_plan, "general")

        assert section["section_title"] == "Plan Overview"
        assert "TASK-001" in section["content"]
        assert "3 files" in section["content"]
        assert "Tip" in section["content"]
        assert section["source"] == "Implementation Plan"

    def test_build_section_result(self):
        """Test _build_section_result helper method."""
        extractor = PlanSectionExtractor()

        result = extractor._build_section_result(
            "Test Title",
            "Test content",
            "Test Source"
        )

        assert result["section_title"] == "Test Title"
        assert result["content"] == "Test content"
        assert result["source"] == "Test Source"


# QAManager Tests
class TestQAManager:
    """Test QAManager interactive session workflow."""

    def test_qa_manager_initialization(self, mock_implementation_plan, mock_task_metadata):
        """Test QAManager initialization."""
        manager = QAManager(
            plan=mock_implementation_plan,
            task_id="TASK-001",
            task_metadata=mock_task_metadata
        )

        assert manager.plan == mock_implementation_plan
        assert manager.task_id == "TASK-001"
        assert manager.task_metadata == mock_task_metadata
        assert isinstance(manager.matcher, KeywordMatcher)
        assert isinstance(manager.extractor, PlanSectionExtractor)
        assert manager.session is None

    def test_qa_manager_with_injected_dependencies(self, mock_implementation_plan, mock_task_metadata):
        """Test QAManager with dependency injection."""
        mock_matcher = Mock(spec=KeywordMatcher)
        mock_extractor = Mock(spec=PlanSectionExtractor)

        manager = QAManager(
            plan=mock_implementation_plan,
            task_id="TASK-001",
            task_metadata=mock_task_metadata,
            matcher=mock_matcher,
            extractor=mock_extractor
        )

        assert manager.matcher == mock_matcher
        assert manager.extractor == mock_extractor

    @patch('builtins.input', side_effect=['Why Strategy pattern?', 'back'])
    @patch('builtins.print')
    def test_run_qa_session_single_question(
        self,
        mock_print,
        mock_input,
        mock_implementation_plan,
        mock_task_metadata
    ):
        """Test running Q&A session with single question."""
        manager = QAManager(
            plan=mock_implementation_plan,
            task_id="TASK-001",
            task_metadata=mock_task_metadata
        )

        session = manager.run_qa_session()

        assert session is not None
        assert session.task_id == "TASK-001"
        assert len(session.exchanges) == 1
        assert session.exchanges[0].question == "Why Strategy pattern?"
        assert session.exit_reason == "back"
        assert session.ended_at is not None

    @patch('builtins.input', side_effect=['What are the risks?', 'How long will this take?', 'back'])
    @patch('builtins.print')
    def test_run_qa_session_multiple_questions(
        self,
        mock_print,
        mock_input,
        mock_implementation_plan,
        mock_task_metadata
    ):
        """Test running Q&A session with multiple questions."""
        manager = QAManager(
            plan=mock_implementation_plan,
            task_id="TASK-001",
            task_metadata=mock_task_metadata
        )

        session = manager.run_qa_session()

        assert session is not None
        assert len(session.exchanges) == 2
        assert session.exchanges[0].question == "What are the risks?"
        assert session.exchanges[1].question == "How long will this take?"

    @patch('builtins.input', side_effect=['help', 'back'])
    @patch('builtins.print')
    def test_run_qa_session_help_command(
        self,
        mock_print,
        mock_input,
        mock_implementation_plan,
        mock_task_metadata
    ):
        """Test help command in Q&A session."""
        manager = QAManager(
            plan=mock_implementation_plan,
            task_id="TASK-001",
            task_metadata=mock_task_metadata
        )

        session = manager.run_qa_session()

        assert session is not None
        assert len(session.exchanges) == 0  # Help doesn't create exchange

    @patch('builtins.input', side_effect=['', '   ', 'back'])
    @patch('builtins.print')
    def test_run_qa_session_empty_questions(
        self,
        mock_print,
        mock_input,
        mock_implementation_plan,
        mock_task_metadata
    ):
        """Test that empty questions are ignored."""
        manager = QAManager(
            plan=mock_implementation_plan,
            task_id="TASK-001",
            task_metadata=mock_task_metadata
        )

        session = manager.run_qa_session()

        assert session is not None
        assert len(session.exchanges) == 0  # Empty questions not recorded

    @patch('builtins.input', side_effect=['Why?', KeyboardInterrupt()])
    @patch('builtins.print')
    def test_run_qa_session_keyboard_interrupt(
        self,
        mock_print,
        mock_input,
        mock_implementation_plan,
        mock_task_metadata
    ):
        """Test handling keyboard interrupt (Ctrl+C)."""
        manager = QAManager(
            plan=mock_implementation_plan,
            task_id="TASK-001",
            task_metadata=mock_task_metadata
        )

        session = manager.run_qa_session()

        assert session is not None
        assert session.exit_reason == "interrupt"
        assert session.ended_at is not None

    def test_generate_answer(self, mock_implementation_plan, mock_task_metadata):
        """Test answer generation with keyword matching."""
        manager = QAManager(
            plan=mock_implementation_plan,
            task_id="TASK-001",
            task_metadata=mock_task_metadata
        )

        answer_data = manager._generate_answer("Why Strategy pattern?")

        assert "answer" in answer_data
        assert "confidence" in answer_data
        assert "category" in answer_data
        assert "matched_keywords" in answer_data
        assert answer_data["category"] == "rationale"
        assert "Strategy" in answer_data["answer"]
        assert answer_data["confidence"] >= 1
        assert answer_data["confidence"] <= 10

    def test_generate_answer_multiple_keywords(self, mock_implementation_plan, mock_task_metadata):
        """Test answer generation with multiple keyword matches."""
        manager = QAManager(
            plan=mock_implementation_plan,
            task_id="TASK-001",
            task_metadata=mock_task_metadata
        )

        answer_data = manager._generate_answer("Why was this rationale chosen?")

        assert answer_data["confidence"] == 8  # High confidence for multiple keywords

    def test_generate_answer_single_keyword(self, mock_implementation_plan, mock_task_metadata):
        """Test answer generation with single keyword match."""
        manager = QAManager(
            plan=mock_implementation_plan,
            task_id="TASK-001",
            task_metadata=mock_task_metadata
        )

        answer_data = manager._generate_answer("What is the duration?")

        assert answer_data["confidence"] == 6  # Medium confidence for single keyword

    def test_generate_answer_general(self, mock_implementation_plan, mock_task_metadata):
        """Test answer generation with no keyword matches."""
        manager = QAManager(
            plan=mock_implementation_plan,
            task_id="TASK-001",
            task_metadata=mock_task_metadata
        )

        answer_data = manager._generate_answer("Tell me about the plan")

        assert answer_data["category"] == "general"
        assert answer_data["confidence"] == 4  # Low confidence for general

    @patch('builtins.print')
    def test_display_answer(self, mock_print, mock_implementation_plan, mock_task_metadata):
        """Test answer display formatting."""
        manager = QAManager(
            plan=mock_implementation_plan,
            task_id="TASK-001",
            task_metadata=mock_task_metadata
        )

        answer_data = {
            "answer": "Test answer content",
            "confidence": 8,
            "matched_keywords": ["why", "chosen"]
        }

        manager._display_answer(answer_data)

        # Verify print was called with formatted content
        mock_print.assert_called()

    @patch('builtins.print')
    def test_display_help(self, mock_print, mock_implementation_plan, mock_task_metadata):
        """Test help display."""
        manager = QAManager(
            plan=mock_implementation_plan,
            task_id="TASK-001",
            task_metadata=mock_task_metadata
        )

        manager._display_help()

        # Verify print was called with help content
        mock_print.assert_called()

    @patch('builtins.input', side_effect=['Why?', 'back'])
    @patch('builtins.print')
    def test_save_to_metadata(
        self,
        mock_print,
        mock_input,
        mock_implementation_plan,
        mock_task_metadata,
        tmp_path
    ):
        """Test saving Q&A session to task metadata."""
        # Create temporary task file
        task_file = tmp_path / "TASK-001.md"
        task_content = """---
id: TASK-001
title: Test Task
status: in_progress
---

# Task Content
"""
        task_file.write_text(task_content, encoding="utf-8")

        manager = QAManager(
            plan=mock_implementation_plan,
            task_id="TASK-001",
            task_metadata=mock_task_metadata
        )

        # Run session
        session = manager.run_qa_session()

        # Save to metadata
        manager.save_to_metadata(str(task_file))

        # Verify file was updated
        updated_content = task_file.read_text(encoding="utf-8")
        assert "qa_session:" in updated_content
        assert "session_id:" in updated_content
        assert "exchanges:" in updated_content

    def test_save_to_metadata_no_session(
        self,
        mock_implementation_plan,
        mock_task_metadata,
        tmp_path
    ):
        """Test save_to_metadata with no session (should be no-op)."""
        task_file = tmp_path / "TASK-001.md"
        task_file.write_text("---\nid: TASK-001\n---\nContent", encoding="utf-8")

        manager = QAManager(
            plan=mock_implementation_plan,
            task_id="TASK-001",
            task_metadata=mock_task_metadata
        )

        # Don't run session, just try to save
        manager.save_to_metadata(str(task_file))

        # File should be unchanged
        content = task_file.read_text(encoding="utf-8")
        assert "qa_session" not in content

    def test_save_to_metadata_file_not_found(
        self,
        mock_implementation_plan,
        mock_task_metadata,
        capsys
    ):
        """Test save_to_metadata with non-existent file."""
        manager = QAManager(
            plan=mock_implementation_plan,
            task_id="TASK-001",
            task_metadata=mock_task_metadata
        )
        manager.session = QASession(
            session_id="qa-001",
            task_id="TASK-001",
            started_at=datetime.utcnow(),
            ended_at=datetime.utcnow()
        )

        manager.save_to_metadata("/nonexistent/task.md")

        # Should print warning
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower()


# Integration Tests
class TestQAManagerIntegration:
    """Integration tests for complete Q&A workflow."""

    @patch('builtins.input', side_effect=[
        'Why Strategy pattern?',
        'What are the risks?',
        'How long will this take?',
        'back'
    ])
    @patch('builtins.print')
    def test_complete_qa_workflow(
        self,
        mock_print,
        mock_input,
        mock_implementation_plan,
        mock_task_metadata,
        tmp_path
    ):
        """Test complete Q&A workflow from start to metadata save."""
        # Create task file
        task_file = tmp_path / "TASK-001.md"
        task_content = """---
id: TASK-001
title: Implement JWT Authentication
status: in_progress
---

# Task Content
"""
        task_file.write_text(task_content, encoding="utf-8")

        # Run Q&A session
        manager = QAManager(
            plan=mock_implementation_plan,
            task_id="TASK-001",
            task_metadata=mock_task_metadata
        )

        session = manager.run_qa_session()

        # Verify session
        assert session is not None
        assert len(session.exchanges) == 3
        assert session.exit_reason == "back"

        # Save to metadata
        manager.save_to_metadata(str(task_file))

        # Verify saved content
        updated_content = task_file.read_text(encoding="utf-8")
        updated_yaml = yaml.safe_load(updated_content.split("---")[1])

        assert "qa_session" in updated_yaml
        assert len(updated_yaml["qa_session"]["exchanges"]) == 3
        assert updated_yaml["qa_session"]["exit_reason"] == "back"
