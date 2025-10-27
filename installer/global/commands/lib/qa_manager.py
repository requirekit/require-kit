"""
Q&A Manager for implementation plan interactive questioning.

This module implements a simplified keyword-based Q&A system that allows users
to ask questions about implementation plans and receive contextual answers by
extracting relevant sections from the plan.

Architecture:
    - QAExchange: Single question-answer pair dataclass
    - QASession: Q&A session tracking with history
    - KeywordMatcher: Maps user questions to plan sections via keyword patterns
    - PlanSectionExtractor: Extracts relevant plan sections based on category
    - QAManager: Main coordinator for Q&A mode workflow

Example:
    >>> from qa_manager import QAManager
    >>> from complexity_models import ImplementationPlan
    >>>
    >>> manager = QAManager(
    ...     plan=plan,
    ...     task_id="TASK-001",
    ...     task_metadata=metadata
    ... )
    >>> session = manager.run_qa_session()
    >>> if session:
    ...     manager.save_to_metadata("tasks/in_progress/TASK-001.md")
"""

import re
import yaml
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .complexity_models import ImplementationPlan, ComplexityScore


@dataclass
class QAExchange:
    """
    Single question-answer pair in Q&A session.

    Attributes:
        question: User's question text
        answer: Generated answer text
        confidence: Confidence level 1-10 (based on keyword match quality)
        timestamp: When the exchange occurred

    Example:
        >>> exchange = QAExchange(
        ...     question="Why Strategy pattern?",
        ...     answer="The plan uses Strategy pattern because...",
        ...     confidence=8,
        ...     timestamp=datetime.utcnow()
        ... )
    """
    question: str
    answer: str
    confidence: int  # 1-10
    timestamp: datetime

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert exchange to dictionary for YAML serialization.

        Returns:
            Dict[str, Any]: Serializable dictionary

        Example:
            >>> exchange.to_dict()
            {
                "question": "Why Strategy pattern?",
                "answer": "...",
                "confidence": 8,
                "timestamp": "2025-10-10T10:15:00Z"
            }
        """
        return {
            "question": self.question,
            "answer": self.answer,
            "confidence": self.confidence,
            "timestamp": self.timestamp.isoformat() + "Z"
        }


@dataclass
class QASession:
    """
    Q&A session tracking with conversation history.

    Attributes:
        session_id: Unique session identifier
        task_id: Associated task identifier
        started_at: Session start timestamp
        exchanges: List of question-answer exchanges
        ended_at: Session end timestamp (None if active)
        exit_reason: Why session ended ("back", "error", "interrupt")

    Example:
        >>> session = QASession(
        ...     session_id="qa-001",
        ...     task_id="TASK-001",
        ...     started_at=datetime.utcnow()
        ... )
        >>> session.exchanges.append(exchange)
    """
    session_id: str
    task_id: str
    started_at: datetime
    exchanges: List[QAExchange] = field(default_factory=list)
    ended_at: Optional[datetime] = None
    exit_reason: Optional[str] = None  # "back", "error", "interrupt"

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert session to dictionary for YAML serialization.

        Returns:
            Dict[str, Any]: Serializable dictionary

        Example:
            >>> session.to_dict()
            {
                "session_id": "qa-001",
                "task_id": "TASK-001",
                "started_at": "2025-10-10T10:15:00Z",
                "exchanges": [...],
                "ended_at": "2025-10-10T10:20:00Z",
                "exit_reason": "back"
            }
        """
        return {
            "session_id": self.session_id,
            "task_id": self.task_id,
            "started_at": self.started_at.isoformat() + "Z",
            "exchanges": [ex.to_dict() for ex in self.exchanges],
            "ended_at": self.ended_at.isoformat() + "Z" if self.ended_at else None,
            "exit_reason": self.exit_reason
        }


class KeywordMatcher:
    """
    Maps user questions to plan sections via keyword patterns.

    Uses simplified keyword matching to categorize questions without
    requiring AI agent integration. Each category maps to a specific
    plan section extractor.

    Example:
        >>> matcher = KeywordMatcher()
        >>> category, keywords = matcher.match_question("Why was this approach chosen?")
        >>> print(category)  # "rationale"
        >>> print(keywords)  # ["why"]
    """

    # Simplified keyword mappings structure (architectural review recommendation)
    KEYWORD_MAPPINGS = {
        "rationale": ["why", "rationale", "reason", "because", "chose", "chosen"],
        "testing": ["test", "testing", "tested", "tests", "verify", "validation"],
        "risks": ["risk", "risks", "concern", "danger", "problem", "fail", "what if"],
        "duration": ["time", "duration", "long", "hours", "estimate", "how long"],
        "files": ["file", "files", "create", "modify", "change", "touch"],
        "dependencies": ["depend", "dependency", "library", "package", "import"],
        "phases": ["phase", "order", "step", "sequence", "first", "next"],
        "complexity": ["complex", "score", "difficult", "simple", "simplify"]
    }

    def match_question(self, question: str) -> Tuple[str, List[str]]:
        """
        Match question to category and return matched keywords.

        Args:
            question: User's question text

        Returns:
            Tuple of (category, matched_keywords)
            - category: Best matching category or "general" if no match
            - matched_keywords: List of keywords that matched

        Example:
            >>> matcher = KeywordMatcher()
            >>> category, keywords = matcher.match_question("Why Strategy pattern?")
            >>> assert category == "rationale"
            >>> assert "why" in keywords
        """
        question_lower = question.lower()
        best_category = "general"
        best_keywords = []
        max_matches = 0

        # Find category with most keyword matches
        for category, keywords in self.KEYWORD_MAPPINGS.items():
            matched = [kw for kw in keywords if kw in question_lower]

            if len(matched) > max_matches:
                max_matches = len(matched)
                best_category = category
                best_keywords = matched

        return best_category, best_keywords


class PlanSectionExtractor:
    """
    Extracts relevant plan sections based on keyword category.

    Uses strategy pattern to delegate extraction to category-specific
    methods. Each extractor method returns a standardized section result
    dictionary with title, content, and source.

    Example:
        >>> extractor = PlanSectionExtractor()
        >>> section = extractor.extract_section(plan, "rationale")
        >>> print(section["section_title"])
        >>> print(section["content"])
    """

    def __init__(self):
        """
        Initialize extractor with category-to-method mappings.
        """
        # Map categories to extractor methods (strategy pattern)
        self.extractors = {
            "rationale": self._extract_rationale,
            "testing": self._extract_testing,
            "risks": self._extract_risks,
            "duration": self._extract_duration,
            "files": self._extract_files,
            "dependencies": self._extract_dependencies,
            "phases": self._extract_phases,
            "complexity": self._extract_complexity,
        }

    def extract_section(
        self,
        plan: "ImplementationPlan",
        category: str
    ) -> Dict[str, str]:
        """
        Extract relevant section based on category.

        Args:
            plan: ImplementationPlan to extract from
            category: Category determined by keyword matching

        Returns:
            Dict with keys: section_title, content, source

        Example:
            >>> section = extractor.extract_section(plan, "risks")
            >>> assert "section_title" in section
            >>> assert "content" in section
            >>> assert "source" in section
        """
        extractor = self.extractors.get(category, self._extract_general)
        return extractor(plan)

    def _build_section_result(
        self,
        title: str,
        content: str,
        source: str
    ) -> Dict[str, str]:
        """
        Build standardized section result dictionary (DRY improvement).

        Args:
            title: Section title for display
            content: Main content text
            source: Source reference (e.g., "Implementation Plan", "Complexity Score")

        Returns:
            Standardized section dictionary

        Example:
            >>> result = extractor._build_section_result(
            ...     "Rationale",
            ...     "Strategy pattern chosen because...",
            ...     "Implementation Plan"
            ... )
        """
        return {
            "section_title": title,
            "content": content,
            "source": source,
        }

    def _extract_rationale(self, plan: "ImplementationPlan") -> Dict[str, str]:
        """
        Extract rationale/reasoning from implementation plan.

        Looks for patterns_used and raw_plan sections that explain
        architectural decisions and approach reasoning.

        Args:
            plan: ImplementationPlan to extract from

        Returns:
            Section dictionary with rationale information
        """
        content_parts = []

        if plan.patterns_used:
            content_parts.append(
                f"**Design Patterns Used**: {', '.join(plan.patterns_used)}"
            )

        if plan.implementation_instructions:
            # Extract first few sentences as rationale
            instructions = plan.implementation_instructions[:500]
            content_parts.append(f"\n**Approach**: {instructions}...")
        elif plan.raw_plan:
            # Fallback to raw plan snippet
            raw_snippet = plan.raw_plan[:500]
            content_parts.append(f"\n**Plan Details**: {raw_snippet}...")

        content = "\n".join(content_parts) if content_parts else \
                  "No specific rationale documented in plan."

        return self._build_section_result(
            "Rationale & Approach",
            content,
            "Implementation Plan"
        )

    def _extract_testing(self, plan: "ImplementationPlan") -> Dict[str, str]:
        """
        Extract test strategy from implementation plan.

        Args:
            plan: ImplementationPlan to extract from

        Returns:
            Section dictionary with test strategy information
        """
        content_parts = []

        if plan.test_summary:
            content_parts.append(f"**Test Strategy**: {plan.test_summary}")

        # Infer testing approach from plan
        if plan.patterns_used:
            content_parts.append(
                f"\n**Patterns to Test**: {', '.join(plan.patterns_used)}"
            )

        content = "\n".join(content_parts) if content_parts else \
                  "No explicit test strategy documented. Standard unit and integration tests recommended."

        return self._build_section_result(
            "Test Strategy",
            content,
            "Implementation Plan"
        )

    def _extract_risks(self, plan: "ImplementationPlan") -> Dict[str, str]:
        """
        Extract risk assessment from implementation plan.

        Args:
            plan: ImplementationPlan to extract from

        Returns:
            Section dictionary with risk information
        """
        content_parts = []

        # Check for detailed risk assessment
        if plan.risk_details:
            for risk in plan.risk_details:
                severity = risk.get("severity", "unknown").upper()
                description = risk.get("description", "No description")
                mitigation = risk.get("mitigation", "No mitigation specified")

                content_parts.append(
                    f"\n**{severity}**: {description}\n"
                    f"  Mitigation: {mitigation}"
                )

        # Fallback to risk indicators
        elif plan.risk_indicators:
            content_parts.append(
                f"**Risk Indicators Detected**: {', '.join(plan.risk_indicators)}"
            )

        # Check for security/schema keywords
        if plan.has_security_keywords:
            content_parts.append(
                "\n**Security Sensitive**: This plan involves authentication, "
                "authorization, or security-related functionality."
            )

        if plan.has_schema_changes:
            content_parts.append(
                "\n**Schema Changes**: This plan modifies database schema. "
                "Ensure proper migration and rollback strategies."
            )

        content = "\n".join(content_parts) if content_parts else \
                  "No specific risks identified in plan."

        return self._build_section_result(
            "Risk Assessment",
            content,
            "Implementation Plan"
        )

    def _extract_duration(self, plan: "ImplementationPlan") -> Dict[str, str]:
        """
        Extract time/duration estimates from implementation plan.

        Args:
            plan: ImplementationPlan to extract from

        Returns:
            Section dictionary with duration information
        """
        content_parts = []

        if plan.estimated_duration:
            content_parts.append(f"**Estimated Duration**: {plan.estimated_duration}")

        if plan.estimated_loc:
            content_parts.append(f"**Estimated Lines of Code**: ~{plan.estimated_loc}")

        # Infer from complexity if available
        if hasattr(plan, 'complexity_score') and plan.complexity_score:
            score = plan.complexity_score.total_score
            if score <= 3:
                complexity_estimate = "Low complexity, quick implementation expected"
            elif score <= 6:
                complexity_estimate = "Medium complexity, moderate time investment"
            else:
                complexity_estimate = "High complexity, significant time investment"

            content_parts.append(f"\n**Complexity Assessment**: {complexity_estimate}")

        content = "\n".join(content_parts) if content_parts else \
                  "No time estimates provided in plan."

        return self._build_section_result(
            "Time Estimates",
            content,
            "Implementation Plan"
        )

    def _extract_files(self, plan: "ImplementationPlan") -> Dict[str, str]:
        """
        Extract files to create/modify from implementation plan.

        Args:
            plan: ImplementationPlan to extract from

        Returns:
            Section dictionary with file information
        """
        content_parts = []

        if plan.files_to_create:
            file_count = len(plan.files_to_create)
            content_parts.append(f"**Files to Create/Modify**: {file_count} files\n")

            # List files (limit to first 10)
            for i, file_path in enumerate(plan.files_to_create[:10], 1):
                content_parts.append(f"  {i}. {file_path}")

            if file_count > 10:
                content_parts.append(f"  ... and {file_count - 10} more files")

        content = "\n".join(content_parts) if content_parts else \
                  "No files specified in plan."

        return self._build_section_result(
            "Files",
            content,
            "Implementation Plan"
        )

    def _extract_dependencies(self, plan: "ImplementationPlan") -> Dict[str, str]:
        """
        Extract external dependencies from implementation plan.

        Args:
            plan: ImplementationPlan to extract from

        Returns:
            Section dictionary with dependency information
        """
        content_parts = []

        if plan.external_dependencies:
            dep_count = len(plan.external_dependencies)
            content_parts.append(
                f"**External Dependencies**: {dep_count} dependencies\n"
            )

            # List dependencies
            for i, dep in enumerate(plan.external_dependencies, 1):
                content_parts.append(f"  {i}. {dep}")

        content = "\n".join(content_parts) if content_parts else \
                  "No external dependencies specified in plan."

        return self._build_section_result(
            "Dependencies",
            content,
            "Implementation Plan"
        )

    def _extract_phases(self, plan: "ImplementationPlan") -> Dict[str, str]:
        """
        Extract implementation phases/order from implementation plan.

        Args:
            plan: ImplementationPlan to extract from

        Returns:
            Section dictionary with phase information
        """
        content_parts = []

        if plan.phases:
            content_parts.append(f"**Implementation Phases**: {len(plan.phases)} phases\n")

            # List phases
            for i, phase in enumerate(plan.phases, 1):
                content_parts.append(f"  {i}. {phase}")

        content = "\n".join(content_parts) if content_parts else \
                  "No explicit phases defined in plan."

        return self._build_section_result(
            "Implementation Order",
            content,
            "Implementation Plan"
        )

    def _extract_complexity(self, plan: "ImplementationPlan") -> Dict[str, str]:
        """
        Extract complexity score details from implementation plan.

        Args:
            plan: ImplementationPlan to extract from

        Returns:
            Section dictionary with complexity information
        """
        content_parts = []

        if hasattr(plan, 'complexity_score') and plan.complexity_score:
            score = plan.complexity_score
            content_parts.append(
                f"**Complexity Score**: {score.total_score}/10\n"
            )

            # Add factor breakdown
            if score.factor_scores:
                content_parts.append("**Factor Breakdown**:")
                for factor in score.factor_scores:
                    content_parts.append(
                        f"  - {factor.factor_name}: {factor.score}/{factor.max_score}"
                    )
                    content_parts.append(f"    {factor.justification}")
        else:
            # Fallback to basic metrics
            content_parts.append(f"**Files to Create**: {plan.file_count}")
            content_parts.append(f"**Dependencies**: {plan.dependency_count}")

            if plan.estimated_loc:
                content_parts.append(f"**Estimated LOC**: {plan.estimated_loc}")

        content = "\n".join(content_parts) if content_parts else \
                  "Complexity information not available."

        return self._build_section_result(
            "Complexity Analysis",
            content,
            "Complexity Score" if hasattr(plan, 'complexity_score') else "Implementation Plan"
        )

    def _extract_general(self, plan: "ImplementationPlan") -> Dict[str, str]:
        """
        Extract general information when no specific category matches.

        Args:
            plan: ImplementationPlan to extract from

        Returns:
            Section dictionary with general information
        """
        content_parts = []

        content_parts.append(f"**Task**: {plan.task_id}")
        content_parts.append(f"**Files**: {plan.file_count} files to create/modify")

        if plan.external_dependencies:
            content_parts.append(
                f"**Dependencies**: {len(plan.external_dependencies)} external"
            )

        if plan.estimated_duration:
            content_parts.append(f"**Duration**: {plan.estimated_duration}")

        content_parts.append(
            "\n💡 **Tip**: Ask more specific questions about:\n"
            "  - 'Why was this approach chosen?' (rationale)\n"
            "  - 'What are the risks?' (risk assessment)\n"
            "  - 'How is this tested?' (test strategy)\n"
            "  - 'What files are created?' (file details)"
        )

        content = "\n".join(content_parts)

        return self._build_section_result(
            "Plan Overview",
            content,
            "Implementation Plan"
        )


class QAManager:
    """
    Manages Q&A mode for implementation plan interactive questioning.

    Coordinates the Q&A session workflow including display rendering,
    user input handling, answer generation via keyword matching, and
    session persistence to task metadata.

    Example:
        >>> manager = QAManager(
        ...     plan=implementation_plan,
        ...     task_id="TASK-001",
        ...     task_metadata={"id": "TASK-001", "title": "Add feature"}
        ... )
        >>> session = manager.run_qa_session()
        >>> if session:
        ...     manager.save_to_metadata("tasks/in_progress/TASK-001.md")
    """

    def __init__(
        self,
        plan: "ImplementationPlan",
        task_id: str,
        task_metadata: Dict[str, Any],
        matcher: Optional[KeywordMatcher] = None,
        extractor: Optional[PlanSectionExtractor] = None
    ):
        """
        Initialize Q&A manager.

        Args:
            plan: ImplementationPlan to answer questions about
            task_id: Task identifier (e.g., "TASK-001")
            task_metadata: Task metadata dictionary
            matcher: Optional KeywordMatcher for dependency injection
            extractor: Optional PlanSectionExtractor for dependency injection

        Example:
            >>> manager = QAManager(plan, "TASK-001", metadata)
        """
        self.plan = plan
        self.task_id = task_id
        self.task_metadata = task_metadata
        self.matcher = matcher or KeywordMatcher()
        self.extractor = extractor or PlanSectionExtractor()
        self.session: Optional[QASession] = None

    def run_qa_session(self) -> Optional[QASession]:
        """
        Execute Q&A mode interactive session.

        Main workflow:
            1. Display Q&A introduction
            2. Loop: prompt for question → generate answer → display
            3. Handle 'back' and 'help' commands
            4. Track all exchanges in session
            5. Return completed session or None if interrupted

        Returns:
            QASession if completed normally, None if interrupted

        Example:
            >>> session = manager.run_qa_session()
            >>> if session:
            ...     print(f"Asked {len(session.exchanges)} questions")
        """
        # Generate unique session ID
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        session_id = f"qa-{self.task_id}-{timestamp}"

        # Initialize session
        self.session = QASession(
            session_id=session_id,
            task_id=self.task_id,
            started_at=datetime.utcnow()
        )

        try:
            # Display introduction
            self._display_qa_intro()

            # Main Q&A loop
            while True:
                question = self._prompt_for_question()

                # Handle commands
                if question.lower() == 'back':
                    self.session.exit_reason = "back"
                    break
                elif question.lower() == 'help':
                    self._display_help()
                    continue
                elif not question.strip():
                    # Ignore empty questions
                    continue

                # Generate answer
                answer_data = self._generate_answer(question)

                # Display answer
                self._display_answer(answer_data)

                # Save exchange
                exchange = QAExchange(
                    question=question,
                    answer=answer_data["answer"],
                    confidence=answer_data["confidence"],
                    timestamp=datetime.utcnow()
                )
                self.session.exchanges.append(exchange)

            # Mark session as complete
            self.session.ended_at = datetime.utcnow()

            print(f"\n✅ Q&A session complete. Asked {len(self.session.exchanges)} questions.")
            print("Returning to checkpoint...\n")

            return self.session

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\n\n⚠️ Q&A session interrupted.")
            self.session.ended_at = datetime.utcnow()
            self.session.exit_reason = "interrupt"
            print("Returning to checkpoint...\n")
            return self.session

        except Exception as e:
            # Handle unexpected errors
            print(f"\n❌ Error during Q&A session: {e}")
            self.session.ended_at = datetime.utcnow()
            self.session.exit_reason = "error"
            print("Returning to checkpoint...\n")
            return self.session

    def save_to_metadata(self, task_file_path: str) -> None:
        """
        Save Q&A session to task metadata in YAML format.

        Appends qa_session to task frontmatter for audit trail
        and future reference.

        Args:
            task_file_path: Path to task markdown file

        Raises:
            OSError: On file system errors

        Example:
            >>> manager.save_to_metadata("tasks/in_progress/TASK-001.md")
        """
        if not self.session:
            return

        task_path = Path(task_file_path)

        if not task_path.exists():
            print(f"⚠️ Task file not found: {task_file_path}")
            return

        try:
            # Read current task file
            content = task_path.read_text(encoding="utf-8")

            # Parse frontmatter and body
            match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)

            if not match:
                print("⚠️ Could not parse task frontmatter. Q&A session not saved.")
                return

            frontmatter = yaml.safe_load(match.group(1))
            body = match.group(2)

            # Add or update qa_session
            frontmatter["qa_session"] = self.session.to_dict()
            frontmatter["updated"] = datetime.utcnow().isoformat() + "Z"

            # Rebuild content
            updated_content = f"---\n{yaml.dump(frontmatter, default_flow_style=False)}---\n{body}"

            # Write back atomically
            task_path.write_text(updated_content, encoding="utf-8")

            print(f"✅ Q&A session saved to task metadata")

        except Exception as e:
            print(f"⚠️ Error saving Q&A session: {e}")

    def _display_qa_intro(self) -> None:
        """
        Display Q&A mode introduction.

        Shows instructions, example questions, and available commands.
        """
        print("\n" + "=" * 70)
        print("Q&A MODE - Ask about the implementation plan")
        print("=" * 70)
        print("\nYou can ask questions like:")
        print("  - Why was this approach chosen?")
        print("  - What are the risks?")
        print("  - How long will this take?")
        print("  - What files will be created?")
        print("  - What if [scenario] happens?")
        print("\nCommands:")
        print("  - Type your question and press ENTER")
        print("  - Type 'back' to return to checkpoint")
        print("  - Type 'help' for more examples")
        print()

    def _prompt_for_question(self) -> str:
        """
        Prompt user for question input.

        Returns:
            str: User's question text (may be empty)

        Example:
            >>> question = manager._prompt_for_question()
        """
        try:
            return input("\nQuestion: ").strip()
        except EOFError:
            # Handle EOF (Ctrl+D)
            return "back"

    def _generate_answer(self, question: str) -> Dict[str, Any]:
        """
        Generate answer using keyword matching.

        Workflow:
            1. Match question to category via keywords
            2. Extract relevant plan section
            3. Format answer with confidence score
            4. Return structured answer data

        Args:
            question: User's question text

        Returns:
            Dict with keys: answer, confidence, category, matched_keywords

        Example:
            >>> answer_data = manager._generate_answer("Why Strategy pattern?")
            >>> print(answer_data["answer"])
            >>> print(answer_data["confidence"])
        """
        # Match question to category
        category, matched_keywords = self.matcher.match_question(question)

        # Extract relevant section
        section = self.extractor.extract_section(self.plan, category)

        # Calculate confidence based on match quality
        if category == "general":
            confidence = 4  # Low confidence for general match
        elif len(matched_keywords) >= 2:
            confidence = 8  # High confidence for multiple keyword matches
        elif len(matched_keywords) == 1:
            confidence = 6  # Medium confidence for single keyword match
        else:
            confidence = 5  # Default confidence

        # Format answer
        answer = (
            f"**{section['section_title']}** (from {section['source']})\n\n"
            f"{section['content']}\n\n"
            f"💡 **Note**: This is a keyword-based answer. "
            f"For detailed questions, review the full plan or consult your team architect."
        )

        return {
            "answer": answer,
            "confidence": confidence,
            "category": category,
            "matched_keywords": matched_keywords,
            "section": section
        }

    def _display_answer(self, answer_data: Dict[str, Any]) -> None:
        """
        Display formatted answer to user.

        Args:
            answer_data: Answer dictionary from _generate_answer

        Example:
            >>> manager._display_answer(answer_data)
        """
        print("\n" + "-" * 70)
        print("ANSWER:")
        print("-" * 70)
        print(f"\n{answer_data['answer']}")
        print(f"\n**Confidence**: {answer_data['confidence']}/10")

        if answer_data['matched_keywords']:
            print(f"**Matched Keywords**: {', '.join(answer_data['matched_keywords'])}")

        print("\n" + "-" * 70)

    def _display_help(self) -> None:
        """
        Display help with example questions.

        Shows categorized example questions to guide users.
        """
        print("\n" + "=" * 70)
        print("EXAMPLE QUESTIONS BY CATEGORY:")
        print("=" * 70)

        print("\n**Rationale & Approach**:")
        print("  - Why was this approach chosen?")
        print("  - What's the rationale for using [pattern]?")

        print("\n**Risk Assessment**:")
        print("  - What are the risks?")
        print("  - What if [component] fails?")
        print("  - What could go wrong?")

        print("\n**Testing Strategy**:")
        print("  - How will this be tested?")
        print("  - What tests are needed?")

        print("\n**Time & Complexity**:")
        print("  - How long will this take?")
        print("  - How complex is this?")
        print("  - Could we simplify this?")

        print("\n**Files & Dependencies**:")
        print("  - What files will be created?")
        print("  - What dependencies are needed?")

        print("\n**Implementation Order**:")
        print("  - What are the implementation phases?")
        print("  - What should be done first?")

        print("\n" + "=" * 70)


# Module exports
__all__ = [
    "QAExchange",
    "QASession",
    "KeywordMatcher",
    "PlanSectionExtractor",
    "QAManager",
]
