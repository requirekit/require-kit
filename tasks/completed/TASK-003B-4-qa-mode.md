---
id: TASK-003B-4
title: Q&A Mode - Interactive Plan Questions
status: completed
created: 2025-10-09T16:45:00Z
updated: 2025-10-10T12:45:00Z
completed: 2025-10-10T12:45:00Z
previous_state: in_review
state_transition_reason: "Task completed - all acceptance criteria met"
assignee: null
priority: low
tags: [workflow-enhancement, qa-mode, agent-integration, optional-enhancement, phase-2.8]
requirements: []
bdd_scenarios: []
parent_task: TASK-003B
dependencies: [TASK-003B-2]
blocks: []
test_results:
  status: passed
  last_run: 2025-10-10T12:15:00Z
  coverage: 92.31
  passed: 53
  failed: 0
  execution_log: "All tests passed. Line coverage: 92.31% (264/286 lines), Branch coverage: ~85%"
blocked_reason: null
complexity_evaluation:
  total_score: 1
  review_mode: auto_proceed
  action: proceed
  routing: Phase 3 (Implementation)
  auto_approved: true
  timestamp: 2025-10-10T12:00:00Z
  factor_scores:
    - name: file_complexity
      score: 0
      max: 3
      justification: Simple change (2 files) - minimal complexity
    - name: pattern_familiarity
      score: 0
      max: 2
      justification: Simple patterns - strategy, dataclass, session management
    - name: risk_level
      score: 0
      max: 3
      justification: No significant risk indicators - low risk
  forced_triggers: []
  summary: Score 1/10 → auto_proceed
architectural_review:
  score: 88
  status: approved
  critical_issues: 0
  timestamp: 2025-10-10T11:00:00Z
code_review:
  status: approved
  quality_gates_passed: 5
  quality_gates_failed: 0
  timestamp: 2025-10-10T12:20:00Z
---

# TASK-003B-4: Q&A Mode - Interactive Plan Questions

## Parent Context

This is **Sub-Task 4 of 4** for TASK-003B (Review Modes & User Interaction).

**Parent Task**: TASK-003B - Review Modes & User Interaction
**Depends On**: TASK-003B-2 (full review mode - action target)
**Blocks**: None (optional enhancement)
**Parallel**: Can work in parallel with TASK-003B-3 (modification mode)

**Priority**: LOW - This is an **optional enhancement**. Can be deferred or simplified.

## Description

Implement **[Q]uestion** handler for full review mode. This feature allows users to ask natural language questions about the implementation plan and receive contextual answers from an AI agent.

**Use Cases**:
- "Why did you choose Strategy pattern over Observer?"
- "What happens if the authentication service is down?"
- "Could we use simpler approach without new dependencies?"
- "What's the rollback strategy if this fails in production?"

**Key Innovation**: Provides plan rationale on-demand without cluttering the checkpoint display. Helps users make informed approval decisions.

**Simplification Option**: If time-constrained, can implement as simple keyword-based FAQ or placeholder for future enhancement.

## Acceptance Criteria

### Phase 1: Q&A Mode Entry ✅ MUST HAVE (even if simplified)

- [ ] **Q&A Mode Display**
  - [ ] Clear entry into Q&A mode
  - [ ] Display instructions:
    ```
    🤖 Q&A MODE - Ask about the implementation plan

    You can ask questions like:
    - Why was this approach chosen?
    - What are the risks?
    - Could we simplify this?
    - What if [scenario] happens?

    Commands:
    - Type your question and press ENTER
    - Type 'back' to return to checkpoint
    - Type 'help' for more examples

    Question:
    ```

- [ ] **Question Input**
  - [ ] Accept natural language input
  - [ ] Support multi-line questions (optional)
  - [ ] Validate non-empty input
  - [ ] Handle 'back' command to exit
  - [ ] Handle 'help' command for examples

### Phase 2: Answer Generation ✅ SHOULD HAVE (or simplify to FAQ)

**Option A: Full AI Integration** (if time allows)
- [ ] **Agent Query**
  - [ ] Select appropriate agent (implementation-planner or software-architect)
  - [ ] Build context:
    - Task requirements
    - Implementation plan
    - Complexity evaluation
    - Architectural review notes
  - [ ] Send question with context to agent
  - [ ] Receive structured answer

- [ ] **Answer Display**
  - [ ] Format answer for readability:
    ```
    🤖 Answer:

    [Main answer paragraph]

    **Requirements Analysis**:
    From REQ-XXX: [requirement that influenced this]

    **Why This Approach**:
    1. [Reason 1]
    2. [Reason 2]

    **Trade-offs**:
    - Pro: [benefit]
    - Con: [cost]

    **Confidence**: 8/10
    ```
  - [ ] Display loading indicator during generation
  - [ ] Handle timeout (>30 seconds)
  - [ ] Handle agent errors gracefully

**Option B: Simplified FAQ** (minimal viable)
- [ ] **Keyword Matching**
  - [ ] Match common question patterns:
    - "why [pattern]" → Explain pattern choice from plan
    - "what if [risk]" → Show risk mitigation from plan
    - "could we simplify" → Show complexity breakdown
  - [ ] Display relevant section from plan
  - [ ] Add note: "For detailed questions, contact your team architect"

### Phase 3: Multi-Turn Conversation ✅ SHOULD HAVE

- [ ] **Context Preservation**
  - [ ] Maintain conversation history
  - [ ] Allow follow-up questions:
    - "What about the alternative you mentioned?"
    - "Can you elaborate on reason 2?"
  - [ ] Track question/answer pairs in session

- [ ] **Conversation Display**
  - [ ] Show previous Q&A at top
  - [ ] Scroll to see history
  - [ ] Clear indication of current question

### Phase 4: Q&A History Persistence ✅ SHOULD HAVE

- [ ] **Save Q&A Exchanges**
  - [ ] Store in task metadata:
    ```yaml
    qa_session:
      started_at: "2025-10-09T10:15:00Z"
      ended_at: "2025-10-09T10:20:00Z"
      exchanges:
        - question: "Why Strategy pattern?"
          answer: "[Full answer]"
          confidence: 9
          timestamp: "2025-10-09T10:16:00Z"
        - question: "What about performance?"
          answer: "[Full answer]"
          confidence: 7
          timestamp: "2025-10-09T10:18:00Z"
    ```

- [ ] **Q&A Documentation**
  - [ ] Append Q&A to implementation plan (optional section)
  - [ ] Makes rationale discoverable for future developers
  - [ ] Helps with onboarding and maintenance

### Phase 5: Return to Checkpoint ✅ MUST HAVE

- [ ] **Exit Q&A Mode**
  - [ ] User types 'back'
  - [ ] Display "Returning to checkpoint..."
  - [ ] Preserve Q&A history
  - [ ] Return to full review decision prompt
  - [ ] No loss of state or context

## Technical Specifications

### Q&A Manager (Full Implementation)

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class QAExchange:
    """Single question-answer pair"""
    question: str
    answer: str
    confidence: int  # 1-10
    timestamp: datetime

@dataclass
class QASession:
    """Q&A session tracking"""
    started_at: datetime
    exchanges: List[QAExchange] = field(default_factory=list)
    ended_at: Optional[datetime] = None

class QAManager:
    """Manages Q&A mode for implementation plan"""

    def __init__(
        self,
        plan: ImplementationPlan,
        complexity_score: ComplexityScore,
        task_metadata: dict
    ):
        self.plan = plan
        self.complexity_score = complexity_score
        self.task_metadata = task_metadata
        self.session = QASession(started_at=datetime.now())

    def execute(self) -> QASession:
        """Execute Q&A mode"""
        self._display_qa_intro()

        while True:
            question = self._prompt_for_question()

            if question.lower() == 'back':
                break
            elif question.lower() == 'help':
                self._display_help()
                continue
            elif not question.strip():
                continue

            # Generate answer
            answer = self._generate_answer(question)

            # Display answer
            self._display_answer(answer)

            # Save exchange
            self.session.exchanges.append(QAExchange(
                question=question,
                answer=answer.text,
                confidence=answer.confidence,
                timestamp=datetime.now()
            ))

        self.session.ended_at = datetime.now()
        return self.session

    def _display_qa_intro(self):
        """Display Q&A mode introduction"""
        print("\n" + "="*70)
        print("🤖 Q&A MODE - Ask about the implementation plan")
        print("="*70)
        print("\nYou can ask questions like:")
        print("  - Why was this approach chosen?")
        print("  - What are the risks?")
        print("  - Could we simplify this?")
        print("  - What if [scenario] happens?")
        print("\nCommands:")
        print("  - Type your question and press ENTER")
        print("  - Type 'back' to return to checkpoint")
        print("  - Type 'help' for more examples")
        print()

    def _prompt_for_question(self) -> str:
        """Prompt for user question"""
        return input("\nQuestion: ").strip()

    def _generate_answer(self, question: str) -> Answer:
        """Generate answer using AI agent"""
        # Build context
        context = self._build_context()

        # Query agent
        agent_prompt = f"""
        User Question: {question}

        Context:
        - Task: {self.task_metadata['id']} - {self.task_metadata['title']}
        - Complexity: {self.complexity_score.total_score}/10
        - Implementation Plan: [See attached]

        Provide a detailed answer that:
        1. Addresses the question directly
        2. References relevant requirements if applicable
        3. Explains trade-offs considered
        4. Suggests alternatives if asked
        5. Includes confidence level (1-10)
        """

        # TODO: Integrate with actual agent
        # For now, placeholder
        return Answer(
            text="Answer generation not yet implemented. Coming soon!",
            confidence=5,
            context_used=[]
        )

    def _display_answer(self, answer: Answer):
        """Display formatted answer"""
        print("\n🤖 Answer:")
        print(answer.text)
        print(f"\n**Confidence**: {answer.confidence}/10")

    def _display_help(self):
        """Display help with example questions"""
        print("\nEXAMPLE QUESTIONS:")
        print("  - Why did you choose [pattern] over [alternative]?")
        print("  - What happens if [component] fails?")
        print("  - Could we use a simpler approach?")
        print("  - What's the rollback strategy?")
        print("  - How does this scale?")
        print("  - What are the security implications?")
```

### Q&A Manager (Simplified FAQ Version)

```python
class SimplifiedQAManager:
    """Simplified Q&A using keyword matching and plan sections"""

    KEYWORDS = {
        'why pattern': 'pattern_rationale',
        'why approach': 'approach_rationale',
        'risk': 'risk_assessment',
        'what if': 'risk_assessment',
        'simplify': 'complexity_breakdown',
        'alternative': 'alternatives_considered',
        'test': 'testing_strategy',
        'security': 'security_considerations'
    }

    def __init__(self, plan: ImplementationPlan, complexity_score: ComplexityScore):
        self.plan = plan
        self.complexity_score = complexity_score

    def execute(self) -> QASession:
        """Execute simplified Q&A"""
        print("\n🤖 Q&A MODE (Simplified)")
        print("Ask questions about the plan, or type 'back' to exit.\n")

        while True:
            question = input("Question: ").strip()

            if question.lower() == 'back':
                break

            # Match keywords
            matched_section = self._match_keyword(question)

            if matched_section:
                self._display_plan_section(matched_section)
            else:
                print("\n💡 Suggested sections to review:")
                print("  - Complexity Breakdown (why this approach)")
                print("  - Risk Assessment (what could go wrong)")
                print("  - Implementation Order (how it will be built)")
                print("\nFor detailed questions, contact your team architect.")

    def _match_keyword(self, question: str) -> Optional[str]:
        """Match question to plan section"""
        question_lower = question.lower()
        for keyword, section in self.KEYWORDS.items():
            if keyword in question_lower:
                return section
        return None

    def _display_plan_section(self, section: str):
        """Display relevant plan section"""
        print(f"\n📋 Relevant section: {section}")
        # Display section from plan
        # (Implementation depends on plan structure)
```

## Test Requirements

### Unit Tests (Full Version)

- [ ] **Question Input Tests**
  - [ ] Valid question → accepted
  - [ ] Empty question → ignored
  - [ ] 'back' command → exits mode
  - [ ] 'help' command → displays help

- [ ] **Answer Generation Tests**
  - [ ] Context building includes all relevant data
  - [ ] Agent query formatted correctly
  - [ ] Answer parsed and formatted
  - [ ] Confidence extracted

- [ ] **Session Tracking Tests**
  - [ ] Exchanges saved correctly
  - [ ] Timestamps accurate
  - [ ] Session metadata complete

### Unit Tests (Simplified Version)

- [ ] **Keyword Matching Tests**
  - [ ] "why pattern" → matches pattern_rationale
  - [ ] "what if" → matches risk_assessment
  - [ ] No match → displays suggestions

### Integration Tests

- [ ] **Full Q&A Flow**
  - [ ] Enter Q&A mode
  - [ ] Ask 3 questions
  - [ ] Receive answers
  - [ ] Type 'back'
  - [ ] Q&A saved in metadata

- [ ] **Return to Checkpoint**
  - [ ] Q&A mode complete
  - [ ] Checkpoint re-displayed
  - [ ] Decision prompt shown
  - [ ] Q&A history accessible

## Success Metrics

### User Experience
- Q&A usage rate: 20-30% of full reviews (target)
- Questions per session: 2-4 average
- Satisfaction with answers: >70% (if measurable)

### Quality (Full Version)
- Answer relevance: >80% (user feedback)
- Confidence accuracy: ±2 points
- Response time: <5 seconds

### Quality (Simplified Version)
- Keyword match rate: >60%
- User finds answer in plan: >70%

## Implementation Options

### Recommended Approach

**Phase 1 (MVP)**: Implement **Simplified FAQ Version**
- Fast to implement (2-3 hours)
- Provides value (directs users to plan sections)
- No external agent dependencies
- Can enhance later

**Phase 2 (Enhancement)**: Upgrade to **Full AI Integration**
- Requires agent integration (6-8 hours)
- Better user experience
- Handles arbitrary questions
- Deferred to future sprint if needed

## File Structure

### Files to Modify

```
installer/global/commands/lib/
├── review_modes.py (UPDATE)
│   └── Update FullReviewHandler with [Q] handler
└── qa_manager.py (NEW)
    ├── QAManager class (full version)
    └── SimplifiedQAManager class (simplified)

tests/unit/
└── test_qa_mode.py (NEW)

tests/integration/
└── test_qa_workflow.py (NEW)
```

## Dependencies

- ✅ TASK-003B-2: FullReviewHandler (for [Q] handler integration)
- ⚠️ Agent integration (if full version) - may need new agent or extend existing

## Estimated Effort

**Simplified Version**: 3 hours
- Keyword matching: 1 hour
- Plan section display: 1 hour
- Tests: 1 hour

**Full Version**: 1 day (8 hours)
- Agent integration: 3 hours
- Answer formatting: 2 hours
- Multi-turn conversation: 1 hour
- History persistence: 1 hour
- Tests: 1 hour

**Complexity**: 5/10 (Moderate-Complex for full version, 3/10 for simplified)

## Out of Scope

- ❌ Advanced NLP (just use agent or simple keywords)
- ❌ Voice input (text only)
- ❌ Multi-language support (English only)
- ❌ Answer caching (generate fresh each time)

## Recommendation

**Start with Simplified Version**:
- Implement FAQ-style keyword matching
- Display relevant plan sections
- Add note about contacting architect for complex questions
- Can enhance to full AI integration later if needed

**Advantages**:
- ✅ Fast implementation
- ✅ No external dependencies
- ✅ Still provides value
- ✅ Easy to test
- ✅ Can upgrade later without rewrite

---

**Optional enhancement - Can defer to future sprint** ⏸️
**Start with simplified version if implementing** ✅
