# TASK-003B-4: Q&A Mode - Interactive Plan Questions
## Implementation Design Document (Simplified Version)

**Status**: Design Phase
**Priority**: LOW (optional enhancement)
**Estimated Effort**: 3 hours
**Approach**: Simplified keyword matching (no AI agent dependency)
**Created**: 2025-10-10

---

## 1. Executive Summary

### 1.1 Scope
Implement **simplified Q&A mode** for TASK-003B-4 using keyword-based pattern matching instead of full AI agent integration. This provides 80% of value with 20% of effort.

### 1.2 Implementation Strategy
- **Phases Implemented**: 1, 2 (simplified), 4, 5
- **Phases Deferred**: Phase 3 (inline history display - minimal value)
- **Key Innovation**: Keyword mapping to plan sections instead of AI query processing

### 1.3 Integration Point
- **Target File**: `/installer/global/commands/lib/review_modes.py`
- **Target Class**: `FullReviewHandler._handle_question()` (currently stub)
- **Entry Point**: User presses [Q] at full review checkpoint

---

## 2. Architecture Design

### 2.1 Class Structure

```python
# File: installer/global/commands/lib/qa_manager.py

from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import List, Dict, Optional, Tuple

@dataclass
class QAExchange:
    """
    Single question-answer exchange in Q&A session.

    Attributes:
        question: User's question text
        answer: System-generated answer
        timestamp: When question was asked
        matched_keywords: Keywords that triggered this answer
        plan_sections: Plan sections referenced in answer
    """
    question: str
    answer: str
    timestamp: datetime
    matched_keywords: List[str] = field(default_factory=list)
    plan_sections: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Serialize for YAML metadata persistence."""
        return {
            "question": self.question,
            "answer": self.answer,
            "timestamp": self.timestamp.isoformat() + "Z",
            "matched_keywords": self.matched_keywords,
            "plan_sections": self.plan_sections,
        }


@dataclass
class QASession:
    """
    Complete Q&A session metadata.

    Tracks all exchanges, duration, and outcome of Q&A session.
    """
    task_id: str
    session_id: str
    start_time: datetime
    end_time: Optional[datetime]
    exchanges: List[QAExchange] = field(default_factory=list)
    exit_reason: str = "pending"  # "back", "error", "interrupt"

    def add_exchange(self, exchange: QAExchange) -> None:
        """Add Q&A exchange to session."""
        self.exchanges.append(exchange)

    def end_session(self, reason: str) -> None:
        """End session with reason."""
        self.end_time = datetime.now(UTC)
        self.exit_reason = reason

    def to_dict(self) -> Dict:
        """Serialize session for metadata persistence."""
        return {
            "task_id": self.task_id,
            "session_id": self.session_id,
            "start_time": self.start_time.isoformat() + "Z",
            "end_time": self.end_time.isoformat() + "Z" if self.end_time else None,
            "exchange_count": len(self.exchanges),
            "exchanges": [ex.to_dict() for ex in self.exchanges],
            "exit_reason": self.exit_reason,
        }


class KeywordMatcher:
    """
    Maps user questions to plan sections via keyword patterns.

    Uses 8 high-coverage keywords to route questions to relevant
    plan sections without requiring AI agent integration.

    Keyword Categories (covering ~80% of expected questions):
    1. "why" / "rationale" → Implementation rationale
    2. "test" / "testing" → Test strategy
    3. "risk" / "concern" → Risk assessment
    4. "time" / "duration" → Time estimates
    5. "file" / "files" → Files to create
    6. "depend" / "dependency" → External dependencies
    7. "phase" / "order" / "step" → Implementation order
    8. "complex" / "score" → Complexity factors
    """

    KEYWORD_MAPPINGS = {
        # Category 1: Rationale questions
        ("why", "rationale", "reason", "because"): "rationale",

        # Category 2: Testing questions
        ("test", "testing", "tested", "tests"): "testing",

        # Category 3: Risk questions
        ("risk", "concern", "danger", "problem", "issue"): "risks",

        # Category 4: Time questions
        ("time", "duration", "long", "hours", "estimate"): "duration",

        # Category 5: File questions
        ("file", "files", "create", "modify"): "files",

        # Category 6: Dependency questions
        ("depend", "dependency", "dependencies", "library", "package"): "dependencies",

        # Category 7: Phase/order questions
        ("phase", "order", "step", "sequence", "first", "start"): "phases",

        # Category 8: Complexity questions
        ("complex", "score", "difficult", "hard"): "complexity",
    }

    def match_question(self, question: str) -> Tuple[str, List[str]]:
        """
        Match question to plan section category.

        Args:
            question: User's question text (case-insensitive)

        Returns:
            Tuple of (category, matched_keywords)
            Returns ("general", []) if no specific match
        """
        question_lower = question.lower()

        for keywords, category in self.KEYWORD_MAPPINGS.items():
            matched = [kw for kw in keywords if kw in question_lower]
            if matched:
                return category, matched

        return "general", []


class PlanSectionExtractor:
    """
    Extracts relevant plan sections based on keyword category.

    Maps categories to specific ImplementationPlan attributes
    and formats them for user-friendly display.
    """

    def extract_section(
        self,
        plan: "ImplementationPlan",
        category: str
    ) -> Dict[str, str]:
        """
        Extract plan section by category.

        Args:
            plan: ImplementationPlan to extract from
            category: Matched category from KeywordMatcher

        Returns:
            Dict with:
                - section_title: Display title
                - content: Extracted content
                - source: Where content came from (for transparency)
        """
        extractors = {
            "rationale": self._extract_rationale,
            "testing": self._extract_testing,
            "risks": self._extract_risks,
            "duration": self._extract_duration,
            "files": self._extract_files,
            "dependencies": self._extract_dependencies,
            "phases": self._extract_phases,
            "complexity": self._extract_complexity,
            "general": self._extract_general,
        }

        extractor = extractors.get(category, self._extract_general)
        return extractor(plan)

    def _extract_rationale(self, plan) -> Dict[str, str]:
        """Extract implementation rationale from raw plan."""
        # Look for "Rationale:" or "Why:" sections in raw plan
        raw_plan = plan.raw_plan
        rationale_section = self._find_section(raw_plan, ["Rationale", "Why", "Approach"])

        if rationale_section:
            content = rationale_section
        else:
            # Fallback: First paragraph of plan
            content = raw_plan.split("\n\n")[0] if raw_plan else "No rationale explicitly documented."

        return {
            "section_title": "Implementation Rationale",
            "content": content,
            "source": "raw_plan",
        }

    def _extract_testing(self, plan) -> Dict[str, str]:
        """Extract test strategy."""
        content = plan.test_summary or "No test strategy documented."
        return {
            "section_title": "Test Strategy",
            "content": content,
            "source": "test_summary",
        }

    def _extract_risks(self, plan) -> Dict[str, str]:
        """Extract risk assessment."""
        if plan.risk_details:
            risk_lines = []
            for risk in plan.risk_details:
                severity = risk.get("severity", "unknown").upper()
                desc = risk.get("description", "No description")
                mitigation = risk.get("mitigation", "No mitigation")
                risk_lines.append(f"[{severity}] {desc}")
                risk_lines.append(f"  → Mitigation: {mitigation}")
            content = "\n".join(risk_lines)
        else:
            content = "No specific risks identified."

        return {
            "section_title": "Risk Assessment",
            "content": content,
            "source": "risk_details",
        }

    def _extract_duration(self, plan) -> Dict[str, str]:
        """Extract time estimates."""
        duration = plan.estimated_duration or "Not estimated"
        loc = plan.estimated_loc or "Not estimated"

        content = f"Estimated Duration: {duration}\nEstimated Lines of Code: {loc}"

        return {
            "section_title": "Time Estimates",
            "content": content,
            "source": "estimated_duration, estimated_loc",
        }

    def _extract_files(self, plan) -> Dict[str, str]:
        """Extract files to create/modify."""
        if plan.files_to_create:
            file_list = "\n".join(f"  - {f}" for f in plan.files_to_create[:20])
            if len(plan.files_to_create) > 20:
                file_list += f"\n  ... and {len(plan.files_to_create) - 20} more"
            content = f"Files to Create/Modify ({len(plan.files_to_create)} total):\n{file_list}"
        else:
            content = "No files specified."

        return {
            "section_title": "Files to Create/Modify",
            "content": content,
            "source": "files_to_create",
        }

    def _extract_dependencies(self, plan) -> Dict[str, str]:
        """Extract external dependencies."""
        if plan.external_dependencies:
            dep_list = "\n".join(f"  - {d}" for d in plan.external_dependencies)
            content = f"External Dependencies ({len(plan.external_dependencies)} total):\n{dep_list}"
        else:
            content = "No external dependencies."

        return {
            "section_title": "External Dependencies",
            "content": content,
            "source": "external_dependencies",
        }

    def _extract_phases(self, plan) -> Dict[str, str]:
        """Extract implementation phases."""
        if plan.phases:
            phase_list = "\n".join(f"  {i}. {p}" for i, p in enumerate(plan.phases, 1))
            content = f"Implementation Phases ({len(plan.phases)} total):\n{phase_list}"
        else:
            content = "No phases documented."

        return {
            "section_title": "Implementation Order",
            "content": content,
            "source": "phases",
        }

    def _extract_complexity(self, plan) -> Dict[str, str]:
        """Extract complexity analysis."""
        if plan.complexity_score:
            score = plan.complexity_score.total_score
            mode = plan.complexity_score.review_mode.value

            factors = []
            for fs in plan.complexity_score.factor_scores:
                factors.append(f"  - {fs.factor_name}: {fs.score}/{fs.max_score}")
                factors.append(f"    {fs.justification}")

            factor_text = "\n".join(factors) if factors else "  No factors detailed"

            content = f"Complexity Score: {score}/10\nReview Mode: {mode}\n\nFactors:\n{factor_text}"
        else:
            content = "No complexity analysis available."

        return {
            "section_title": "Complexity Analysis",
            "content": content,
            "source": "complexity_score",
        }

    def _extract_general(self, plan) -> Dict[str, str]:
        """Extract general overview."""
        content = plan.raw_plan[:500] + "..." if len(plan.raw_plan) > 500 else plan.raw_plan

        return {
            "section_title": "Implementation Plan Overview",
            "content": content,
            "source": "raw_plan (truncated)",
        }

    def _find_section(self, text: str, headers: List[str]) -> Optional[str]:
        """
        Find section in text by header keywords.

        Args:
            text: Full text to search
            headers: List of header keywords to match

        Returns:
            Section text if found, None otherwise
        """
        lines = text.split("\n")

        for i, line in enumerate(lines):
            for header in headers:
                if header.lower() in line.lower() and (":" in line or "#" in line):
                    # Found header, extract until next section or end
                    section_lines = []
                    for j in range(i + 1, len(lines)):
                        # Stop at next header (starts with # or ends with :)
                        if lines[j].strip().startswith("#") or (lines[j].strip().endswith(":") and len(lines[j].strip()) < 50):
                            break
                        section_lines.append(lines[j])

                    return "\n".join(section_lines).strip()

        return None


class QAManager:
    """
    Main coordinator for Q&A mode.

    Orchestrates question input, keyword matching, answer generation,
    and session persistence. Integrates with FullReviewHandler.

    Example:
        >>> manager = QAManager(plan, task_id="TASK-001")
        >>> session = manager.run_qa_session()
        >>> print(f"Questions asked: {len(session.exchanges)}")
    """

    def __init__(
        self,
        plan: "ImplementationPlan",
        task_id: str,
        task_metadata: Dict
    ):
        """
        Initialize Q&A manager.

        Args:
            plan: ImplementationPlan to query
            task_id: Task identifier
            task_metadata: Task metadata dict
        """
        self.plan = plan
        self.task_id = task_id
        self.task_metadata = task_metadata

        self.matcher = KeywordMatcher()
        self.extractor = PlanSectionExtractor()

        self.session: Optional[QASession] = None

    def run_qa_session(self) -> QASession:
        """
        Run interactive Q&A session.

        Returns:
            QASession: Completed session with all exchanges

        Raises:
            KeyboardInterrupt: On Ctrl+C (handled gracefully)
        """
        # Initialize session
        self.session = QASession(
            task_id=self.task_id,
            session_id=self._generate_session_id(),
            start_time=datetime.now(UTC),
            end_time=None,
        )

        try:
            # Display Q&A interface
            self._display_header()

            # Main Q&A loop
            while True:
                question = self._prompt_for_question()

                # Check for exit command
                if question.lower() == 'back':
                    self.session.end_session("back")
                    print("\n✅ Returning to checkpoint...\n")
                    break

                # Skip empty questions
                if not question.strip():
                    print("⚠️  Please enter a question or 'back' to return.\n")
                    continue

                # Process question and generate answer
                answer, metadata = self._generate_answer(question)

                # Display answer
                self._display_answer(answer, metadata)

                # Record exchange
                exchange = QAExchange(
                    question=question,
                    answer=answer,
                    timestamp=datetime.now(UTC),
                    matched_keywords=metadata["matched_keywords"],
                    plan_sections=metadata["plan_sections"],
                )
                self.session.add_exchange(exchange)

        except KeyboardInterrupt:
            print("\n\n⚠️  Q&A interrupted. Returning to checkpoint...\n")
            self.session.end_session("interrupt")

        except Exception as e:
            print(f"\n❌ Error in Q&A session: {e}\n")
            self.session.end_session("error")

        return self.session

    def _display_header(self) -> None:
        """Display Q&A mode header."""
        print("\n" + "=" * 70)
        print("❓ IMPLEMENTATION PLAN Q&A")
        print("=" * 70)
        print("\nAsk questions about the implementation plan.")
        print("Type 'back' to return to checkpoint.\n")
        print("Examples:")
        print("  - Why are we using this approach?")
        print("  - What are the main risks?")
        print("  - How long will this take?")
        print("  - What files will be created?")
        print()

    def _prompt_for_question(self) -> str:
        """
        Prompt user for question input.

        Returns:
            str: User's question text
        """
        return input("Your question: ").strip()

    def _generate_answer(self, question: str) -> Tuple[str, Dict]:
        """
        Generate answer to user question.

        Args:
            question: User's question text

        Returns:
            Tuple of (answer_text, metadata_dict)
        """
        # Match question to category
        category, matched_keywords = self.matcher.match_question(question)

        # Extract relevant plan section
        section_data = self.extractor.extract_section(self.plan, category)

        # Build answer
        answer = self._format_answer(section_data, question)

        # Build metadata
        metadata = {
            "matched_keywords": matched_keywords,
            "plan_sections": [section_data["source"]],
            "category": category,
        }

        return answer, metadata

    def _format_answer(self, section_data: Dict, question: str) -> str:
        """
        Format answer from section data.

        Args:
            section_data: Extracted section data
            question: Original question

        Returns:
            str: Formatted answer text
        """
        lines = []

        # Add section title
        lines.append(f"📖 {section_data['section_title']}:")
        lines.append("-" * 70)

        # Add content
        lines.append(section_data["content"])

        # Add source reference
        lines.append("")
        lines.append(f"(Source: {section_data['source']})")

        return "\n".join(lines)

    def _display_answer(self, answer: str, metadata: Dict) -> None:
        """
        Display answer to user.

        Args:
            answer: Formatted answer text
            metadata: Answer metadata
        """
        print()
        print(answer)
        print()

    def _generate_session_id(self) -> str:
        """Generate unique session ID."""
        timestamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S%f")
        return f"qa-{self.task_id}-{timestamp}"

    def save_to_metadata(self) -> Dict:
        """
        Save Q&A session to task metadata format.

        Returns:
            Dict: Metadata updates for task YAML
        """
        if not self.session:
            return {}

        return {
            "qa_session": self.session.to_dict()
        }


# Module exports
__all__ = [
    "QAExchange",
    "QASession",
    "KeywordMatcher",
    "PlanSectionExtractor",
    "QAManager",
]
```

### 2.2 Integration with FullReviewHandler

**File**: `/installer/global/commands/lib/review_modes.py`

```python
# Modify FullReviewHandler._handle_question() method (currently stub at line 873)

def _handle_question(self) -> Optional[FullReviewResult]:
    """
    Handle [Q]uestion action - interactive Q&A about plan.

    Enters Q&A mode where user can ask questions about the
    implementation plan and receive answers based on plan content.

    Returns:
        Optional[FullReviewResult]: None (always returns to checkpoint)

    Example:
        >>> result = handler._handle_question()
        >>> # User asks questions, then returns to checkpoint
        >>> assert result is None
    """
    try:
        from .qa_manager import QAManager
    except ImportError:
        from qa_manager import QAManager

    print("\n❓ Entering Q&A mode...\n")

    try:
        # Create Q&A manager
        qa_manager = QAManager(
            plan=self.plan,
            task_id=self.task_id,
            task_metadata=self.task_metadata
        )

        # Run Q&A session
        session = qa_manager.run_qa_session()

        # Update task metadata with Q&A history
        # (This will be persisted by caller when task state is updated)
        metadata_updates = qa_manager.save_to_metadata()
        if metadata_updates:
            self.task_metadata.update(metadata_updates)

        print(f"✅ Q&A session completed: {len(session.exchanges)} question(s) asked")
        print("Returning to checkpoint...\n")

        # Always return None to re-display checkpoint
        return None

    except KeyboardInterrupt:
        print("\n\n⚠️  Q&A interrupted. Returning to checkpoint...\n")
        return None

    except Exception as e:
        print(f"\n❌ Error in Q&A mode: {e}")
        print("Returning to checkpoint...\n")
        return None
```

---

## 3. File Structure

### 3.1 New Files

```
installer/global/commands/lib/
├── qa_manager.py                    [NEW - 400 lines]
│   ├── QAExchange (dataclass)
│   ├── QASession (dataclass)
│   ├── KeywordMatcher
│   ├── PlanSectionExtractor
│   └── QAManager
```

### 3.2 Modified Files

```
installer/global/commands/lib/
├── review_modes.py                  [MODIFY - 1 method]
│   └── FullReviewHandler._handle_question()  (line 873)
│       - Replace stub with QAManager integration
│       - Add metadata persistence
│       - Handle errors gracefully
```

### 3.3 Test Files

```
tests/
├── unit/
│   └── test_qa_manager.py           [NEW - 300 lines]
│       ├── TestKeywordMatcher
│       ├── TestPlanSectionExtractor
│       └── TestQAManager
│
└── integration/
    └── test_qa_workflow.py          [NEW - 200 lines]
        ├── TestQASessionWorkflow
        └── TestFullReviewQAIntegration
```

---

## 4. Data Structures

### 4.1 Keyword Mapping Table

| Category | Keywords | Plan Section | Example Questions |
|----------|----------|-------------|-------------------|
| rationale | why, rationale, reason, because | raw_plan (rationale section) | "Why this approach?" |
| testing | test, testing, tested, tests | test_summary | "How will this be tested?" |
| risks | risk, concern, danger, problem | risk_details | "What are the risks?" |
| duration | time, duration, long, hours | estimated_duration | "How long will this take?" |
| files | file, files, create, modify | files_to_create | "What files are created?" |
| dependencies | depend, dependency, library | external_dependencies | "What dependencies?" |
| phases | phase, order, step, sequence | phases | "What's the implementation order?" |
| complexity | complex, score, difficult | complexity_score | "Why is this complex?" |

### 4.2 YAML Metadata Format

```yaml
# Added to task metadata after Q&A session
qa_session:
  task_id: "TASK-001"
  session_id: "qa-TASK-001-20251010103045123456"
  start_time: "2025-10-10T10:30:45Z"
  end_time: "2025-10-10T10:35:22Z"
  exchange_count: 3
  exchanges:
    - question: "Why are we using event sourcing?"
      answer: |
        📖 Implementation Rationale:
        ----------------------------------------------------------------------
        Event sourcing provides complete audit trail and supports...

        (Source: raw_plan)
      timestamp: "2025-10-10T10:31:12Z"
      matched_keywords: ["why"]
      plan_sections: ["raw_plan"]

    - question: "What are the main risks?"
      answer: |
        📖 Risk Assessment:
        ----------------------------------------------------------------------
        [HIGH] Event replay consistency
          → Mitigation: Comprehensive event replay tests

        (Source: risk_details)
      timestamp: "2025-10-10T10:33:05Z"
      matched_keywords: ["risk"]
      plan_sections: ["risk_details"]

    - question: "How long will this take?"
      answer: |
        📖 Time Estimates:
        ----------------------------------------------------------------------
        Estimated Duration: 3-4 hours
        Estimated Lines of Code: 850

        (Source: estimated_duration, estimated_loc)
      timestamp: "2025-10-10T10:34:50Z"
      matched_keywords: ["long"]
      plan_sections: ["estimated_duration", "estimated_loc"]

  exit_reason: "back"
```

---

## 5. Error Handling Strategy

### 5.1 Error Categories

1. **User Input Errors**
   - Empty question → Prompt to re-enter or type 'back'
   - No keyword match → Return general overview section
   - Special characters → Sanitize before processing

2. **Plan Data Missing**
   - Section not available → Return "Not documented" message
   - Empty plan → Return "Plan incomplete" message
   - Malformed plan → Log error, return general section

3. **System Errors**
   - Keyboard interrupt → Save session, return to checkpoint
   - Import error → Display error, return to checkpoint
   - File I/O error → Log error, continue session

### 5.2 Error Handling Patterns

```python
# Pattern 1: Graceful degradation
try:
    section_data = self.extractor.extract_section(plan, category)
except Exception as e:
    logger.error(f"Error extracting section: {e}")
    section_data = {
        "section_title": "Error",
        "content": "Unable to extract plan section. Please view full plan.",
        "source": "error"
    }

# Pattern 2: User-friendly fallback
if not question.strip():
    print("⚠️  Please enter a question or 'back' to return.\n")
    continue  # Re-prompt

# Pattern 3: Always return to checkpoint
except KeyboardInterrupt:
    print("\n\n⚠️  Q&A interrupted. Returning to checkpoint...\n")
    session.end_session("interrupt")
    return None  # Always None to re-display checkpoint
```

---

## 6. Testing Approach

### 6.1 Unit Tests

**File**: `tests/unit/test_qa_manager.py`

```python
import pytest
from datetime import datetime, UTC
from installer.global.commands.lib.qa_manager import (
    KeywordMatcher,
    PlanSectionExtractor,
    QAManager,
    QAExchange,
    QASession,
)
from installer.global.commands.lib.complexity_models import ImplementationPlan


class TestKeywordMatcher:
    """Test keyword matching logic."""

    def test_match_why_question(self):
        matcher = KeywordMatcher()
        category, keywords = matcher.match_question("Why are we using this approach?")
        assert category == "rationale"
        assert "why" in keywords

    def test_match_risk_question(self):
        matcher = KeywordMatcher()
        category, keywords = matcher.match_question("What are the main risks?")
        assert category == "risks"
        assert "risk" in keywords

    def test_match_multiple_keywords(self):
        matcher = KeywordMatcher()
        category, keywords = matcher.match_question("Why is this risky?")
        # Should match first category found (rationale)
        assert category in ["rationale", "risks"]
        assert len(keywords) > 0

    def test_match_no_keywords(self):
        matcher = KeywordMatcher()
        category, keywords = matcher.match_question("Tell me more")
        assert category == "general"
        assert keywords == []

    def test_case_insensitive(self):
        matcher = KeywordMatcher()
        category1, _ = matcher.match_question("WHY?")
        category2, _ = matcher.match_question("why?")
        assert category1 == category2 == "rationale"


class TestPlanSectionExtractor:
    """Test plan section extraction."""

    @pytest.fixture
    def sample_plan(self):
        return ImplementationPlan(
            task_id="TASK-001",
            raw_plan="Implementation plan...",
            files_to_create=["file1.py", "file2.py"],
            external_dependencies=["pytest", "requests"],
            test_summary="Unit tests with pytest",
            estimated_duration="2 hours",
            estimated_loc=200,
            phases=["Phase 1", "Phase 2"],
            risk_details=[
                {"severity": "high", "description": "Risk 1", "mitigation": "Mitigation 1"}
            ],
        )

    def test_extract_testing_section(self, sample_plan):
        extractor = PlanSectionExtractor()
        result = extractor.extract_section(sample_plan, "testing")
        assert result["section_title"] == "Test Strategy"
        assert "pytest" in result["content"]
        assert result["source"] == "test_summary"

    def test_extract_files_section(self, sample_plan):
        extractor = PlanSectionExtractor()
        result = extractor.extract_section(sample_plan, "files")
        assert "file1.py" in result["content"]
        assert "file2.py" in result["content"]
        assert "2 total" in result["content"]

    def test_extract_missing_section(self):
        plan = ImplementationPlan(
            task_id="TASK-001",
            raw_plan="Plan",
            files_to_create=[],
        )
        extractor = PlanSectionExtractor()
        result = extractor.extract_section(plan, "dependencies")
        assert "No external dependencies" in result["content"]


class TestQAExchange:
    """Test QAExchange dataclass."""

    def test_exchange_creation(self):
        exchange = QAExchange(
            question="Why?",
            answer="Because...",
            timestamp=datetime.now(UTC),
            matched_keywords=["why"],
            plan_sections=["rationale"],
        )
        assert exchange.question == "Why?"
        assert exchange.answer == "Because..."
        assert len(exchange.matched_keywords) == 1

    def test_exchange_to_dict(self):
        exchange = QAExchange(
            question="Why?",
            answer="Because...",
            timestamp=datetime(2025, 10, 10, 10, 30, 45, tzinfo=UTC),
        )
        data = exchange.to_dict()
        assert data["question"] == "Why?"
        assert data["timestamp"] == "2025-10-10T10:30:45Z"


class TestQASession:
    """Test QASession management."""

    def test_session_creation(self):
        session = QASession(
            task_id="TASK-001",
            session_id="qa-001",
            start_time=datetime.now(UTC),
            end_time=None,
        )
        assert session.task_id == "TASK-001"
        assert session.exit_reason == "pending"
        assert len(session.exchanges) == 0

    def test_add_exchange(self):
        session = QASession(
            task_id="TASK-001",
            session_id="qa-001",
            start_time=datetime.now(UTC),
            end_time=None,
        )
        exchange = QAExchange(
            question="Why?",
            answer="Because...",
            timestamp=datetime.now(UTC),
        )
        session.add_exchange(exchange)
        assert len(session.exchanges) == 1

    def test_end_session(self):
        session = QASession(
            task_id="TASK-001",
            session_id="qa-001",
            start_time=datetime.now(UTC),
            end_time=None,
        )
        session.end_session("back")
        assert session.exit_reason == "back"
        assert session.end_time is not None
```

### 6.2 Integration Tests

**File**: `tests/integration/test_qa_workflow.py`

```python
import pytest
from unittest.mock import patch, MagicMock
from installer.global.commands.lib.qa_manager import QAManager
from installer.global.commands.lib.complexity_models import ImplementationPlan


class TestQASessionWorkflow:
    """Test complete Q&A session workflow."""

    @pytest.fixture
    def sample_plan(self):
        return ImplementationPlan(
            task_id="TASK-001",
            raw_plan="Rationale: We are using event sourcing for audit trail...",
            files_to_create=["EventStore.py", "Event.py"],
            test_summary="Comprehensive event replay tests",
            estimated_duration="3 hours",
        )

    @pytest.fixture
    def qa_manager(self, sample_plan):
        return QAManager(
            plan=sample_plan,
            task_id="TASK-001",
            task_metadata={"id": "TASK-001", "title": "Test Task"},
        )

    @patch('builtins.input')
    def test_single_question_session(self, mock_input, qa_manager):
        """Test session with one question."""
        # Simulate user asking one question then exiting
        mock_input.side_effect = [
            "Why are we using event sourcing?",  # Question
            "back",  # Exit
        ]

        session = qa_manager.run_qa_session()

        assert len(session.exchanges) == 1
        assert session.exit_reason == "back"
        assert "why" in session.exchanges[0].matched_keywords[0].lower()

    @patch('builtins.input')
    def test_multiple_questions_session(self, mock_input, qa_manager):
        """Test session with multiple questions."""
        mock_input.side_effect = [
            "Why this approach?",  # Q1
            "What are the risks?",  # Q2
            "How long will it take?",  # Q3
            "back",  # Exit
        ]

        session = qa_manager.run_qa_session()

        assert len(session.exchanges) == 3
        assert session.exit_reason == "back"

    @patch('builtins.input')
    def test_empty_question_handling(self, mock_input, qa_manager):
        """Test handling of empty questions."""
        mock_input.side_effect = [
            "",  # Empty
            "   ",  # Whitespace
            "Why?",  # Valid
            "back",  # Exit
        ]

        session = qa_manager.run_qa_session()

        # Should only record the valid question
        assert len(session.exchanges) == 1

    def test_metadata_persistence(self, qa_manager):
        """Test Q&A session saves to metadata."""
        # Create a completed session
        qa_manager.session = MagicMock()
        qa_manager.session.to_dict.return_value = {
            "task_id": "TASK-001",
            "exchange_count": 2,
        }

        metadata = qa_manager.save_to_metadata()

        assert "qa_session" in metadata
        assert metadata["qa_session"]["exchange_count"] == 2
```

---

## 7. Implementation Order (Critical Path)

### Phase 1: Core Classes (1 hour)
1. Create `qa_manager.py`
2. Implement `QAExchange` dataclass
3. Implement `QASession` dataclass
4. Implement `KeywordMatcher` class
5. **Milestone**: Keyword matching works

### Phase 2: Section Extraction (1 hour)
1. Implement `PlanSectionExtractor` base
2. Implement 8 extraction methods
3. Add `_find_section` helper
4. **Milestone**: All plan sections extractable

### Phase 3: Q&A Manager (45 minutes)
1. Implement `QAManager.__init__`
2. Implement `run_qa_session` loop
3. Implement answer generation
4. Add metadata persistence
5. **Milestone**: Interactive Q&A works end-to-end

### Phase 4: Integration (30 minutes)
1. Modify `FullReviewHandler._handle_question()`
2. Add import statements
3. Add error handling
4. Test integration
5. **Milestone**: [Q] option works in full review

### Phase 5: Testing (45 minutes)
1. Write unit tests for KeywordMatcher
2. Write unit tests for PlanSectionExtractor
3. Write integration tests for QAManager
4. Run all tests and fix issues
5. **Milestone**: All tests pass

### Phase 6: Documentation & Polish (15 minutes)
1. Add docstrings
2. Update CLAUDE.md
3. Create usage examples
4. **Milestone**: Implementation complete

**Total Estimated Time**: 3 hours

---

## 8. Success Criteria

### 8.1 Functional Requirements
- ✅ User can enter Q&A mode from full review checkpoint
- ✅ System accepts questions and provides relevant answers
- ✅ 'back' command returns to checkpoint without breaking flow
- ✅ Q&A history persisted to task metadata
- ✅ All 8 keyword categories work correctly
- ✅ Graceful handling of missing plan sections

### 8.2 Quality Requirements
- ✅ Unit test coverage ≥80%
- ✅ Integration tests pass
- ✅ No crashes on edge cases (empty questions, missing data)
- ✅ Response time <1 second per question
- ✅ Code follows existing patterns (dataclasses, error handling)

### 8.3 User Experience
- ✅ Clear instructions on how to use Q&A mode
- ✅ Answers are relevant and easy to understand
- ✅ Easy to exit (type 'back' at any time)
- ✅ No confusion about state (always returns to checkpoint)

---

## 9. Deferred Features (Future Tasks)

### 9.1 Phase 3: Inline History Display
**Effort**: 1 hour
**Value**: Low (minimal UX improvement)
**Reason for Deferral**: Not essential for MVP, adds complexity

```python
# Future enhancement: Show Q&A history inline
def _display_qa_history(self):
    if self.session and self.session.exchanges:
        print("\n📜 Previous Questions:")
        for i, ex in enumerate(self.session.exchanges[-3:], 1):
            print(f"  {i}. Q: {ex.question[:50]}...")
```

### 9.2 Full AI Agent Integration
**Effort**: 8 hours
**Value**: High (better answers, follow-up reasoning)
**Reason for Deferral**: Requires agent infrastructure, MCP integration

```python
# Future enhancement: Use implementation-planner agent
def _generate_answer_with_agent(self, question: str):
    from .agent_client import AgentClient

    client = AgentClient("implementation-planner")
    response = client.query(
        question=question,
        context={
            "plan": self.plan.to_dict(),
            "task": self.task_metadata,
        }
    )
    return response.answer, response.metadata
```

### 9.3 Natural Language Understanding
**Effort**: 4 hours
**Value**: Medium (handles complex questions)
**Reason for Deferral**: Current keyword matching covers 80% of cases

---

## 10. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Keyword matching too simplistic | Medium | Low | Cover 80% with 8 keywords, fallback to general |
| User asks unanswerable questions | High | Low | Return general section, suggest view full plan |
| Q&A loop confuses state | Low | High | Always return None to re-display checkpoint |
| Performance with large plans | Low | Low | Extract only needed sections, limit content length |

---

## 11. Dependencies

### 11.1 Internal Dependencies
- ✅ `complexity_models.py` - ImplementationPlan dataclass
- ✅ `review_modes.py` - FullReviewHandler integration point
- ✅ Existing error handling patterns from `modification_session.py`

### 11.2 External Dependencies
- ✅ Python 3.9+ (project standard)
- ✅ Standard library only (datetime, dataclasses, typing)
- ✅ No new pip packages required

### 11.3 Test Dependencies
- ✅ pytest (already in project)
- ✅ pytest mocks (unittest.mock)

---

## 12. Rollout Plan

### 12.1 Development
1. Create feature branch: `feature/task-003b-4-qa-mode`
2. Implement in order: Core → Extraction → Manager → Integration → Tests
3. Self-test with manual Q&A sessions
4. Code review before merge

### 12.2 Testing
1. Run unit tests: `pytest tests/unit/test_qa_manager.py -v`
2. Run integration tests: `pytest tests/integration/test_qa_workflow.py -v`
3. Manual E2E test: `/task-work TASK-XXX` → Full review → [Q] → Ask questions → back → [A]pprove

### 12.3 Documentation
1. Update `CLAUDE.md` with Q&A mode documentation
2. Add examples to `review_modes.py` docstrings
3. Create usage guide in `docs/qa-mode-guide.md`

### 12.4 Deployment
1. Merge to main branch
2. Update TASK-003B-parent.md progress (4/4 completed)
3. Mark TASK-003B-4 as COMPLETED
4. Enable [Q] option in full review (remove "Coming soon" message)

---

## 13. Appendix

### 13.1 Example User Interactions

**Scenario 1: Why Question**
```
Your question: Why are we using event sourcing?

📖 Implementation Rationale:
----------------------------------------------------------------------
Event sourcing provides complete audit trail for all order state
changes, enabling time-travel debugging and regulatory compliance.
This approach ensures we never lose historical data and can replay
events to reconstruct state at any point in time.

(Source: raw_plan)

Your question: back

✅ Returning to checkpoint...
```

**Scenario 2: Risk Question**
```
Your question: What are the main risks?

📖 Risk Assessment:
----------------------------------------------------------------------
[HIGH] Event replay consistency
  → Mitigation: Comprehensive event replay tests

[MEDIUM] Learning curve for team
  → Mitigation: Detailed documentation and pair programming

(Source: risk_details)

Your question: back
```

**Scenario 3: No Match**
```
Your question: Tell me more

📖 Implementation Plan Overview:
----------------------------------------------------------------------
This task implements event sourcing for order management...
[First 500 characters of plan]

(Source: raw_plan (truncated))

Your question: back
```

### 13.2 Performance Benchmarks

| Operation | Target | Expected |
|-----------|--------|----------|
| Keyword matching | <10ms | 1-2ms |
| Section extraction | <50ms | 10-20ms |
| Answer formatting | <50ms | 5-10ms |
| Total per question | <200ms | 50-100ms |

### 13.3 Code Metrics

| Metric | Target | Expected |
|--------|--------|----------|
| Lines of code | <500 | ~400 |
| Cyclomatic complexity | <10 | 6-8 |
| Test coverage | ≥80% | 85-90% |
| Public API surface | <10 classes | 5 classes |

---

**End of Implementation Plan**

**Status**: Ready for implementation
**Reviewer**: Awaiting approval
**Next Steps**: Begin Phase 1 (Core Classes)
