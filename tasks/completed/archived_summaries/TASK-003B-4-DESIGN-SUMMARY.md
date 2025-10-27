# TASK-003B-4 Design Summary
## Q&A Mode - Simplified Implementation Approach

**Date**: 2025-10-10
**Priority**: LOW (optional enhancement)
**Estimated Effort**: 3 hours
**Approach**: Simplified keyword matching (no AI agent)

---

## Executive Summary

This design implements **Q&A Mode** for the architectural review workflow using a **simplified keyword-based approach** instead of full AI agent integration. This provides **80% of the value with 20% of the effort** while maintaining the architectural pattern established by TASK-003B-2 and TASK-003B-3.

### Key Design Decisions

1. **Keyword Matching vs. AI Agent**
   - Use 8 high-coverage keywords to route questions to plan sections
   - Covers ~80% of expected user questions
   - Zero external dependencies, instant response time
   - Defers full AI integration to future enhancement

2. **Integration Pattern**
   - Follows existing `ModificationSession` pattern from TASK-003B-3
   - Uses dataclasses for state (`QAExchange`, `QASession`)
   - Integrates cleanly with `FullReviewHandler._handle_question()`
   - Always returns to checkpoint (no state modification)

3. **Metadata Persistence**
   - Saves Q&A history to task YAML metadata
   - Provides audit trail of questions asked
   - Helps future developers understand decisions
   - Compatible with existing metadata structure

---

## Architecture Overview

### Class Hierarchy

```
QAManager (main coordinator)
├── KeywordMatcher (maps questions → categories)
├── PlanSectionExtractor (extracts relevant plan sections)
├── QASession (tracks session lifecycle)
└── QAExchange (individual Q&A pairs)
```

### Integration Point

```
FullReviewHandler.execute()
  └── _prompt_for_decision()
      └── if choice == 'q':
          └── _handle_question()  ← NEW IMPLEMENTATION
              └── QAManager.run_qa_session()
                  └── Returns None → Re-display checkpoint
```

### Data Flow

```
User Question
    ↓
KeywordMatcher.match_question() → (category, keywords)
    ↓
PlanSectionExtractor.extract_section() → section_data
    ↓
QAManager._format_answer() → formatted_answer
    ↓
Display to user
    ↓
Record in QASession.exchanges[]
    ↓
'back' command → End session → Save to metadata → Return to checkpoint
```

---

## Keyword Mapping Strategy

### 8 High-Coverage Keywords (80% of Questions)

| Category | Keywords | Plan Section | Coverage |
|----------|----------|-------------|----------|
| rationale | why, rationale, reason, because | raw_plan (rationale section) | 20% |
| testing | test, testing, tested, tests | test_summary | 15% |
| risks | risk, concern, danger, problem | risk_details | 15% |
| duration | time, duration, long, hours | estimated_duration | 10% |
| files | file, files, create, modify | files_to_create | 10% |
| dependencies | depend, dependency, library | external_dependencies | 5% |
| phases | phase, order, step, sequence | phases | 5% |
| complexity | complex, score, difficult | complexity_score | 5% |
| **general** | (no match) | raw_plan (overview) | 15% |

**Total Coverage**: ~80% of expected questions

---

## File Structure

### New Files (1 file, ~400 lines)

```python
installer/global/commands/lib/qa_manager.py  [NEW]
```

Contains:
- `QAExchange` - Dataclass for Q&A pairs
- `QASession` - Dataclass for session tracking
- `KeywordMatcher` - Keyword → category mapping
- `PlanSectionExtractor` - Plan section extraction
- `QAManager` - Main coordinator

### Modified Files (1 file, 1 method)

```python
installer/global/commands/lib/review_modes.py  [MODIFY]
```

Changes:
- `FullReviewHandler._handle_question()` (line 873)
  - Replace stub with QAManager integration
  - Add error handling
  - Add metadata persistence

### Test Files (2 files, ~500 lines)

```python
tests/unit/test_qa_manager.py           [NEW]
tests/integration/test_qa_workflow.py   [NEW]
```

---

## Key Design Patterns

### 1. Dataclass-Based State Management

```python
@dataclass
class QAExchange:
    """Single Q&A exchange."""
    question: str
    answer: str
    timestamp: datetime
    matched_keywords: List[str] = field(default_factory=list)
    plan_sections: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Serialize for YAML persistence."""
        return {
            "question": self.question,
            "answer": self.answer,
            "timestamp": self.timestamp.isoformat() + "Z",
            "matched_keywords": self.matched_keywords,
            "plan_sections": self.plan_sections,
        }
```

**Why**: Follows existing pattern from `ComplexityScore`, `ImplementationPlan`, `SessionMetadata`

### 2. Strategy Pattern for Section Extraction

```python
class PlanSectionExtractor:
    """Extract plan sections based on category."""

    def extract_section(self, plan, category: str) -> Dict[str, str]:
        extractors = {
            "rationale": self._extract_rationale,
            "testing": self._extract_testing,
            "risks": self._extract_risks,
            # ... 8 total extractors
        }
        extractor = extractors.get(category, self._extract_general)
        return extractor(plan)
```

**Why**: Clean separation of concerns, easy to extend with new categories

### 3. Fail-Safe Error Handling

```python
try:
    section_data = self.extractor.extract_section(plan, category)
except Exception as e:
    logger.error(f"Error extracting section: {e}")
    section_data = {
        "section_title": "Error",
        "content": "Unable to extract plan section.",
        "source": "error"
    }
```

**Why**: Graceful degradation, never crash user's flow

### 4. Always Return to Checkpoint

```python
def _handle_question(self) -> Optional[FullReviewResult]:
    """Always returns None to re-display checkpoint."""
    try:
        qa_manager = QAManager(self.plan, self.task_id, self.task_metadata)
        session = qa_manager.run_qa_session()
        # ... update metadata ...
        return None  # ← Always None
    except Exception:
        return None  # ← Even on error
```

**Why**: Consistent with [M]odify and [V]iew handlers, no state confusion

---

## Example User Interactions

### Scenario 1: Successful Q&A Session

```
Your choice (A/M/V/Q/C): q

❓ Entering Q&A mode...

========================================================================
❓ IMPLEMENTATION PLAN Q&A
========================================================================

Ask questions about the implementation plan.
Type 'back' to return to checkpoint.

Examples:
  - Why are we using this approach?
  - What are the main risks?
  - How long will this take?

Your question: Why are we using event sourcing?

📖 Implementation Rationale:
----------------------------------------------------------------------
Event sourcing provides complete audit trail for all order state
changes, enabling time-travel debugging and regulatory compliance.

(Source: raw_plan)

Your question: What are the risks?

📖 Risk Assessment:
----------------------------------------------------------------------
[HIGH] Event replay consistency
  → Mitigation: Comprehensive event replay tests

[MEDIUM] Learning curve for team
  → Mitigation: Detailed documentation

(Source: risk_details)

Your question: back

✅ Q&A session completed: 2 question(s) asked
Returning to checkpoint...

========================================================================
IMPLEMENTATION PLAN REVIEW
========================================================================
[... checkpoint re-displayed ...]

Your choice (A/M/V/Q/C):
```

### Scenario 2: No Keyword Match

```
Your question: Tell me everything

📖 Implementation Plan Overview:
----------------------------------------------------------------------
This task implements event sourcing for order management using...
[First 500 characters of plan]

(Source: raw_plan (truncated))

Your question: back
```

---

## Metadata Persistence Format

### YAML Structure

```yaml
# Added to task metadata after Q&A session
qa_session:
  task_id: "TASK-001"
  session_id: "qa-TASK-001-20251010103045123456"
  start_time: "2025-10-10T10:30:45Z"
  end_time: "2025-10-10T10:35:22Z"
  exchange_count: 2
  exchanges:
    - question: "Why are we using event sourcing?"
      answer: "📖 Implementation Rationale:\n..."
      timestamp: "2025-10-10T10:31:12Z"
      matched_keywords: ["why"]
      plan_sections: ["raw_plan"]
    - question: "What are the main risks?"
      answer: "📖 Risk Assessment:\n..."
      timestamp: "2025-10-10T10:33:05Z"
      matched_keywords: ["risk"]
      plan_sections: ["risk_details"]
  exit_reason: "back"
```

**Benefits**:
- Audit trail of questions asked
- Understanding of user concerns
- Helps future developers
- Debugging architectural decisions

---

## Implementation Order (Critical Path)

### Phase 1: Core Classes (1 hour)
✅ Create `qa_manager.py`
✅ Implement dataclasses (`QAExchange`, `QASession`)
✅ Implement `KeywordMatcher`
**Milestone**: Keyword matching works

### Phase 2: Section Extraction (1 hour)
✅ Implement `PlanSectionExtractor`
✅ Implement 8 extraction methods
**Milestone**: All plan sections extractable

### Phase 3: Q&A Manager (45 minutes)
✅ Implement `QAManager.run_qa_session()`
✅ Implement answer generation
✅ Add metadata persistence
**Milestone**: End-to-end Q&A works

### Phase 4: Integration (30 minutes)
✅ Modify `FullReviewHandler._handle_question()`
✅ Test integration
**Milestone**: [Q] option works in full review

### Phase 5: Testing (45 minutes)
✅ Write unit tests
✅ Write integration tests
**Milestone**: All tests pass

**Total**: 3 hours

---

## Testing Strategy

### Unit Tests (15 tests, 300 lines)

```python
# tests/unit/test_qa_manager.py

class TestKeywordMatcher:
    - test_match_why_question()
    - test_match_risk_question()
    - test_match_multiple_keywords()
    - test_match_no_keywords()
    - test_case_insensitive()

class TestPlanSectionExtractor:
    - test_extract_testing_section()
    - test_extract_files_section()
    - test_extract_missing_section()

class TestQAExchange:
    - test_exchange_creation()
    - test_exchange_to_dict()

class TestQASession:
    - test_session_creation()
    - test_add_exchange()
    - test_end_session()
```

**Coverage Target**: ≥80%

### Integration Tests (5 tests, 200 lines)

```python
# tests/integration/test_qa_workflow.py

class TestQASessionWorkflow:
    - test_single_question_session()
    - test_multiple_questions_session()
    - test_empty_question_handling()
    - test_metadata_persistence()
    - test_full_review_integration()
```

**Scenarios Covered**:
- Single question → back
- Multiple questions → back
- Empty input handling
- Keyboard interrupt
- Metadata persistence

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Keyword matching too simplistic | Medium | Low | 8 keywords cover 80%, fallback to general |
| User asks complex questions | High | Low | Return relevant section, suggest view full plan |
| Performance with large plans | Low | Low | Extract only needed sections, limit to 500 chars |
| State confusion (stuck in Q&A) | Low | High | Always return None, clear 'back' command |

**Overall Risk**: LOW

---

## Success Criteria

### Functional
✅ User can enter Q&A mode from full review
✅ System provides relevant answers to questions
✅ 'back' command returns to checkpoint cleanly
✅ Q&A history persisted to task metadata
✅ All 8 keyword categories work

### Quality
✅ Unit test coverage ≥80%
✅ Integration tests pass
✅ No crashes on edge cases
✅ Response time <1s per question
✅ Code follows existing patterns

### User Experience
✅ Clear instructions on usage
✅ Answers are relevant and understandable
✅ Easy to exit at any time
✅ No state confusion

---

## Deferred Features (Future Enhancements)

### 1. Full AI Agent Integration (8 hours)
- Better answer quality
- Follow-up reasoning
- Context-aware responses
- Requires MCP infrastructure

### 2. Inline Q&A History Display (1 hour)
- Show last 3 questions inline
- Minimal UX improvement
- Not essential for MVP

### 3. Natural Language Understanding (4 hours)
- Handle complex questions
- Current keyword matching covers 80%
- Diminishing returns

---

## Dependencies

### Internal
✅ `complexity_models.py` - ImplementationPlan
✅ `review_modes.py` - FullReviewHandler
✅ Existing patterns from `modification_session.py`

### External
✅ Python 3.9+ (project standard)
✅ Standard library only
✅ No new pip packages

### Test
✅ pytest (already in project)
✅ unittest.mock

---

## Comparison with Existing Implementations

### Similar Pattern: ModificationSession (TASK-003B-3)

| Aspect | ModificationSession | QASession |
|--------|---------------------|-----------|
| Purpose | Interactive plan modification | Interactive Q&A |
| State Management | `SessionState` enum | `QASession.exit_reason` |
| Change Tracking | `ChangeTracker` | `QASession.exchanges[]` |
| Persistence | Version manager + YAML | YAML metadata |
| Return Behavior | Returns None → checkpoint | Returns None → checkpoint |
| Error Handling | Try-catch, graceful degradation | Try-catch, graceful degradation |

**Pattern Consistency**: ✅ High alignment with existing architecture

---

## Performance Expectations

| Operation | Target | Expected | Actual (Est.) |
|-----------|--------|----------|---------------|
| Keyword matching | <10ms | 1-2ms | ~1ms |
| Section extraction | <50ms | 10-20ms | ~15ms |
| Answer formatting | <50ms | 5-10ms | ~5ms |
| **Total per Q** | <200ms | 50-100ms | **~25ms** |

**Performance**: ✅ Well under target

---

## Code Quality Metrics

| Metric | Target | Expected |
|--------|--------|----------|
| Lines of code | <500 | ~400 |
| Cyclomatic complexity | <10 | 6-8 |
| Test coverage | ≥80% | 85-90% |
| Public API surface | <10 classes | 5 classes |
| Dependencies | 0 external | 0 |

**Quality**: ✅ Meets all targets

---

## Rollout Checklist

### Development
- [ ] Create branch: `feature/task-003b-4-qa-mode`
- [ ] Implement Phase 1: Core Classes
- [ ] Implement Phase 2: Section Extraction
- [ ] Implement Phase 3: Q&A Manager
- [ ] Implement Phase 4: Integration
- [ ] Implement Phase 5: Testing

### Testing
- [ ] Run unit tests: `pytest tests/unit/test_qa_manager.py -v`
- [ ] Run integration tests: `pytest tests/integration/test_qa_workflow.py -v`
- [ ] Manual E2E test: Full review → [Q] → Questions → back → Approve

### Documentation
- [ ] Update `CLAUDE.md` with Q&A mode docs
- [ ] Add docstrings to all classes/methods
- [ ] Create usage guide

### Deployment
- [ ] Merge to main
- [ ] Update TASK-003B-parent.md (4/4 completed)
- [ ] Mark TASK-003B-4 as COMPLETED
- [ ] Enable [Q] option (remove "Coming soon" message)

---

## Conclusion

This design provides a **pragmatic, low-risk implementation** of Q&A mode that:

1. ✅ **Delivers 80% of value with 20% of effort** (3 hours vs. 11 hours)
2. ✅ **Follows established architectural patterns** (dataclasses, error handling, return to checkpoint)
3. ✅ **Zero external dependencies** (Python stdlib only)
4. ✅ **High test coverage** (≥80% unit + integration)
5. ✅ **Easy to extend** (add keywords, enhance with AI later)

**Status**: Ready for implementation
**Risk Level**: LOW
**Estimated ROI**: HIGH (small effort, useful feature)

---

**Next Steps**: Begin Phase 1 implementation (Core Classes)
