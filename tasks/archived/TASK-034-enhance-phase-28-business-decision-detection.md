---
id: TASK-034
title: Enhance Phase 2.8 with Business Decision Detection
status: archived
created: 2025-10-28T10:00:00Z
updated: 2025-12-03T17:45:00Z
archived: 2025-12-03T17:45:00Z
archived_reason: "Transferred to GuardKit - This task enhances Phase 2.8 workflow checkpoint which is part of the /task-work implementation workflow. This belongs to GuardKit, not RequireKit."
transferred_to: "guardkit"
priority: high
tags: [workflow, phase-2.8, decision-detection, human-in-the-loop, enhancement, archived]
epic: null
feature: null
requirements: []
bdd_scenarios: []
estimated_time: 4-6 hours
complexity_evaluation:
  score: 6
  level: "medium"
  factors:
    - name: "requirements_complexity"
      score: 2
      justification: "Multiple decision point categories to handle"
    - name: "pattern_complexity"
      score: 2
      justification: "Heuristic detection + LLM analysis integration"
    - name: "risk_level"
      score: 1
      justification: "Medium risk - affects core workflow checkpoint"
    - name: "dependencies"
      score: 1
      justification: "Integrates with existing Phase 2.8 checkpoint"
  breakdown_suggested: false
test_results:
  status: pending
  coverage: null
  last_run: null
---

# Task: Enhance Phase 2.8 with Business Decision Detection

## Description

Enhance the Phase 2.8 (Human Checkpoint) in `/task-work` workflow to automatically detect and surface **business logic decision points** that require stakeholder input, in addition to existing technical complexity and architectural review checks.

**Current Phase 2.8 Behavior**:
- Triggered when complexity ≥7 OR architectural review flags issues
- Displays Markdown implementation plan
- User options: Approve/Modify/Simplify/Reject/Postpone

**Enhanced Phase 2.8 Behavior**:
- Also triggered when **business decision points** are detected during planning
- Displays implementation plan + **decision points section**
- New option: **Make Decisions** (inline decision capture)
- Decisions are documented in task file for traceability

## Motivation

Real-world usage revealed that teams need human intervention for a different class of decisions beyond technical complexity:
- **Business Logic**: Validation rules, domain constraints, business rules
- **Domain Model**: Entity property changes, data model contracts
- **API Contracts**: Error codes, return types, external interfaces
- **Data Integrity**: Null handling strategies, transformation rules

These decisions require **stakeholder or product owner input** and cannot be made by AI or developers alone.

## Code Review Context

This enhancement addresses patterns observed in production usage where:
1. Tasks with clear technical implementation still had **ambiguous business requirements**
2. Mid-implementation pauses occurred when assumptions about business logic were incorrect
3. Developers wanted explicit "decision needed" flags in task specifications
4. Refactoring tasks especially needed business logic clarification (e.g., "Is this method still needed?", "What should validation rules be?")

## Acceptance Criteria

### 1. Decision Point Detection (Phase 2: Implementation Planning)

- [ ] During Phase 2 (Implementation Planning), analyze task description + requirements for decision points
- [ ] Detect decision point categories:
  - **Business Logic**: Validation rules, constraints, business rules
  - **Domain Model**: Entity changes, property additions/removals
  - **API Contracts**: Error codes, return types, interface changes
  - **Data Integrity**: Null handling, data transformations, mappings
- [ ] Use keyword-based heuristics for initial detection (see Implementation Guide)
- [ ] Store detected decision points in temporary structure for Phase 2.8

### 2. Phase 2.8 Checkpoint Enhancement

- [ ] Trigger Phase 2.8 checkpoint if:
  - Complexity ≥7 (existing), OR
  - Architectural review score <60 (existing), OR
  - **Business decision points detected ≥1 (NEW)**
- [ ] Display enhanced checkpoint UI:
  - Implementation plan (existing)
  - Architectural review summary (existing)
  - **⚠️ DECISION POINTS section (NEW)**
- [ ] Add new checkpoint option: **[D]ecisions - Review and make business decisions**

### 3. Decision Point Display Format

- [ ] Display each decision point with:
  - Decision category (Business Logic/Domain Model/API Contract/Data Integrity)
  - Clear question requiring answer
  - Context from code or requirements
  - Multiple options with trade-offs (when obvious)
  - Impact statement (why this decision matters)
- [ ] Format matches template (see Implementation Guide)
- [ ] Decision points are numbered and easy to navigate

### 4. Interactive Decision Capture

- [ ] When user selects **[D]ecisions** option:
  - Display decision points one by one
  - Prompt for user input/selection
  - Allow deferral ("skip this decision for now")
  - Allow "defer all" option
- [ ] Capture decisions in structured format:
  - Decision point ID
  - User's choice/answer
  - Timestamp
  - Rationale (optional user input)

### 5. Task File Updates

- [ ] Add decision points to task file frontmatter:
  ```yaml
  has_decision_points: true
  decision_points_count: 3
  decision_points:
    - id: "dp-001"
      category: "business_logic"
      question: "What validation rules should apply?"
      status: "resolved"
      decision: "Require route assignment"
      rationale: "Business requirement from stakeholder"
      decided_at: "2025-10-28T10:15:00Z"
  ```
- [ ] Add `## ⚠️ DECISION POINTS` section to task Markdown body
- [ ] Mark task with `[decisions-needed]` tag if unresolved decision points exist
- [ ] Remove tag when all decisions resolved

### 6. Integration with Implementation Phase

- [ ] If user proceeds to implementation with unresolved decisions:
  - Add comments/TODOs in implementation plan: `// TODO: DECISION NEEDED - [question]`
  - Log warning that assumptions are being made
  - Track assumption points for later review
- [ ] If all decisions resolved:
  - Use decisions to enhance implementation plan
  - Generate validation code from business rules
  - Document decisions in code comments

### 7. Decision Point Heuristics

- [ ] Implement keyword-based detection for decision categories:
  - **Business Logic**: "validate", "validation", "rule", "constraint", "allowed", "required"
  - **Domain Model**: "add property", "remove field", "entity", "domain model", "contract"
  - **API Contract**: "error code", "return type", "interface", "API", "endpoint"
  - **Data Integrity**: "null handling", "mapping", "transform", "conversion"
- [ ] Detect ambiguity keywords: "might", "could", "should we", "unclear", "TBD", "?"
- [ ] Detect entity changes in requirements (property additions/removals)
- [ ] Confidence scoring: High/Medium/Low
- [ ] Only flag High confidence by default

### 8. Testing Requirements

- [ ] Unit tests for decision point detection logic
- [ ] Integration tests for Phase 2.8 enhanced checkpoint flow
- [ ] Test decision capture and storage
- [ ] Test task file updates with decision points
- [ ] Test workflow with 0, 1, and multiple decision points
- [ ] Test defer/skip decision functionality
- [ ] Achieve ≥85% test coverage

### 9. Documentation Updates

- [ ] Update `/task-work` command documentation with decision point handling
- [ ] Add decision point template to best practices
- [ ] Document decision categories and examples
- [ ] Add workflow diagram showing decision detection flow
- [ ] Create example tasks with decision points

### 10. Build & Validation

- [ ] Solution builds successfully
- [ ] All tests pass
- [ ] Integration test with sample task containing decision points
- [ ] Phase 2.8 checkpoint displays correctly
- [ ] Decision capture works end-to-end

---

## Decision Point Categories & Examples

### Business Logic Decisions

**Characteristics**:
- Require product owner or stakeholder input
- Define "correct" system behavior
- May have multiple valid interpretations

**Examples**:
- "What validation rules should the engine enforce?"
- "Should drivers be required to have routes assigned?"
- "What constitutes a 'valid' entity state?"
- "When should the system return an error vs warning?"

**Detection Keywords**: validate, validation, rule, constraint, business rule, enforce, allowed, required, permitted

---

### Domain Model Decisions

**Characteristics**:
- Affect entity contracts and data structures
- May be breaking changes to API/interfaces
- Impact downstream consumers

**Examples**:
- "Should we add `CurrentRoute` property to entity?"
- "Should entity include both `DefaultRoute` and `CurrentRoute`?"
- "How should missing properties be handled (null vs exception)?"

**Detection Patterns**:
- "add property", "remove field", "entity change"
- Mentions of entity names in task description
- Requirements mentioning data model changes

**Detection Keywords**: entity, domain model, property, field, contract, data structure

---

### API Contract Decisions

**Characteristics**:
- Define external-facing interfaces
- Require consistency across system
- Impact API consumers

**Examples**:
- "What error codes should be returned?"
- "Should method return `ErrorOr<Entity>` or `ErrorOr<bool>`?"
- "What HTTP status codes for different error scenarios?"
- "What should error messages say?"

**Detection Keywords**: error code, return type, API, endpoint, interface, contract, response, status code

---

### Data Integrity Decisions

**Characteristics**:
- Define data transformation and validation rules
- Affect data consistency guarantees
- May have subtle edge cases

**Examples**:
- "How should null values be mapped (null → empty string or vice versa)?"
- "Should empty strings be treated as null?"
- "How should duplicate records be handled (update/skip/error)?"

**Detection Keywords**: null handling, mapping, transform, conversion, duplicate, data integrity

---

## Implementation Guide

### Phase 1: Add Decision Detection to Planning Phase

**File**: `installer/global/commands/lib/task_work_orchestrator.py` (or equivalent)

**Location**: Phase 2 (Implementation Planning) - after plan is generated but before Phase 2.8 checkpoint

```python
def detect_decision_points(task_context, implementation_plan):
    """
    Analyze task and plan for business decision points.

    Returns: List of DecisionPoint objects
    """
    decision_points = []

    # 1. Keyword-based heuristic detection
    business_logic_keywords = ["validate", "validation", "rule", "constraint",
                                "allowed", "required", "enforce"]
    domain_model_keywords = ["add property", "remove field", "entity",
                             "domain model", "contract"]
    api_contract_keywords = ["error code", "return type", "API", "endpoint",
                             "interface", "status code"]
    data_integrity_keywords = ["null handling", "mapping", "transform",
                               "conversion", "duplicate"]
    ambiguity_keywords = ["might", "could", "should we", "unclear", "TBD", "?"]

    # 2. Analyze task description
    task_description = task_context.get('description', '')

    # 3. Analyze requirements
    requirements = task_context.get('requirements', [])

    # 4. Analyze implementation plan for assumptions
    plan_text = implementation_plan.get('markdown_content', '')

    # 5. Check for entity changes
    if has_entity_changes(task_description, requirements):
        decision_points.append(DecisionPoint(
            category="domain_model",
            question="Entity contract changes detected - confirm property additions/removals",
            confidence="high"
        ))

    # 6. Check for validation mentions
    if contains_keywords(task_description, business_logic_keywords):
        decision_points.append(DecisionPoint(
            category="business_logic",
            question="Validation rules mentioned - clarify specific constraints",
            confidence="medium"
        ))

    # 7. Check for ambiguity
    if contains_keywords(task_description, ambiguity_keywords):
        decision_points.append(DecisionPoint(
            category="general",
            question="Ambiguous language detected - clarify intent",
            confidence="medium"
        ))

    # Filter to high confidence only by default
    return [dp for dp in decision_points if dp.confidence == "high"]
```

### Phase 2: Enhance Phase 2.8 Checkpoint Display

**Current Phase 2.8 Output**:
```
🔍 CHECKPOINT: Review Implementation Plan

COMPLEXITY: 7/10 (Complex - Full review required)
ARCHITECTURAL REVIEW: 65/100 (Acceptable - Minor issues)

[Implementation plan display]

OPTIONS:
[A]pprove - Proceed with implementation
[M]odify - Edit plan before proceeding
[S]implify - Request simplified approach
[R]eject - Cancel and return to backlog
[P]ostpone - Save plan and defer to later
```

**Enhanced Phase 2.8 Output**:
```
🔍 CHECKPOINT: Review Implementation Plan

COMPLEXITY: 7/10 (Complex - Full review required)
ARCHITECTURAL REVIEW: 65/100 (Acceptable - Minor issues)
⚠️  DECISION POINTS: 3 detected (see below)

[Implementation plan display]

---

⚠️  DECISION POINTS REQUIRING INPUT

BUSINESS LOGIC (2 points):
  1. Validation rules for entity state - clarify constraints
  2. Error handling strategy - confirm error codes

DOMAIN MODEL (1 point):
  3. Entity property additions - confirm breaking change acceptable

OPTIONS:
[A]pprove - Proceed with implementation (defer decisions)
[D]ecisions - Review and make business decisions
[M]odify - Edit plan before proceeding
[S]implify - Request simplified approach
[R]eject - Cancel and return to backlog
[P]ostpone - Save plan and defer to later
```

### Phase 3: Interactive Decision Workflow

**When user selects [D]ecisions**:
```
⚠️  DECISION POINT 1/3

Category: Business Logic
Question: What validation rules should apply to entity state?

Context:
  Task mentions "validate driver details" but specific rules not defined.

Current assumption in plan:
  - Validate route is not null or empty
  - No other validation

Options:
  A) Route required only (current assumption)
  B) Route + Location required
  C) Route + Location + Device required
  D) Custom (specify rules)

Impact: Determines what constitutes "valid" entity state

Your decision [A/B/C/D/Skip]: _
```

**If user selects option**:
```
✅ Decision captured: Route required only

Rationale (optional - press Enter to skip): Business requirement from product owner
[User input]: Confirmed with stakeholder - only route is mandatory

✅ Decision 1/3 saved

[Proceed to decision 2/3]
```

**If user selects Skip**:
```
⏭️  Decision deferred

This decision will be flagged in implementation with TODO marker.

[Proceed to decision 2/3]
```

### Phase 4: Task File Update

**Frontmatter Addition**:
```yaml
has_decision_points: true
decision_points_count: 3
decision_points:
  - id: "dp-001"
    category: "business_logic"
    question: "What validation rules should apply to entity state?"
    status: "resolved"
    decision: "Route required only"
    rationale: "Confirmed with stakeholder - only route is mandatory"
    decided_at: "2025-10-28T10:15:00Z"
    decided_by: "user"
  - id: "dp-002"
    category: "business_logic"
    question: "Error handling strategy - confirm error codes"
    status: "deferred"
    decision: null
    rationale: "Will determine during implementation"
    decided_at: null
    decided_by: null
  - id: "dp-003"
    category: "domain_model"
    question: "Entity property additions - confirm breaking change acceptable"
    status: "resolved"
    decision: "Add properties - breaking change accepted"
    rationale: "Only internal API, no external consumers"
    decided_at: "2025-10-28T10:18:00Z"
    decided_by: "user"
```

**Markdown Section Addition**:
```markdown
## ⚠️ DECISION POINTS

### ✅ 1. Business Logic: Entity Validation Rules
**Status**: Resolved

**Question**: What validation rules should apply to entity state?

**Decision**: Route required only

**Rationale**: Confirmed with stakeholder - only route is mandatory field

**Decided**: 2025-10-28 by user

---

### ⏭️ 2. Business Logic: Error Handling Strategy
**Status**: Deferred

**Question**: Error handling strategy - confirm error codes

**Decision**: TBD during implementation

**Rationale**: Will determine during implementation

---

### ✅ 3. Domain Model: Entity Property Additions
**Status**: Resolved

**Question**: Entity property additions - confirm breaking change acceptable

**Decision**: Add properties - breaking change accepted

**Rationale**: Only internal API, no external consumers

**Decided**: 2025-10-28 by user
```

### Phase 5: Implementation Plan Enhancement

**If decisions resolved**, enhance implementation plan:
```markdown
## Phase 3: Implementation

### Step 1: Add Validation Logic
```csharp
// DECISION: dp-001 - Route validation only
if (string.IsNullOrWhiteSpace(entity.Route))
{
    return Error.Validation("Entity.NoRoute", "Route is required");
}
// Note: Location and Device are optional per stakeholder decision
```
```

**If decisions deferred**, add TODO markers:
```csharp
// TODO: DECISION NEEDED (dp-002) - Error handling strategy
// Current assumption: Use generic error codes
// Confirm with stakeholder: Should we use domain-specific codes?
return Error.Failure("Generic.Error", "Operation failed");
```

---

## Decision Point Data Structure

```python
@dataclass
class DecisionPoint:
    """Represents a business decision point requiring human input."""

    id: str  # e.g., "dp-001"
    category: str  # business_logic, domain_model, api_contract, data_integrity
    question: str  # Clear question requiring answer
    context: Optional[str] = None  # Context from code/requirements
    options: List[str] = field(default_factory=list)  # Possible choices
    impact: Optional[str] = None  # Why this decision matters
    confidence: str = "medium"  # high, medium, low
    status: str = "pending"  # pending, resolved, deferred
    decision: Optional[str] = None  # User's decision
    rationale: Optional[str] = None  # User's explanation
    decided_at: Optional[datetime] = None
    decided_by: Optional[str] = None
```

---

## Test Requirements

### Unit Tests

```python
def test_detect_decision_points_business_logic():
    """Should detect business logic decision points from keywords."""
    task_context = {
        'description': 'Add validation rules for driver entity',
        'requirements': []
    }
    plan = {'markdown_content': ''}

    decision_points = detect_decision_points(task_context, plan)

    assert len(decision_points) >= 1
    assert any(dp.category == 'business_logic' for dp in decision_points)

def test_detect_decision_points_entity_changes():
    """Should detect domain model decisions for entity changes."""
    task_context = {
        'description': 'Add CurrentRoute property to DriverDetails entity',
        'requirements': []
    }
    plan = {'markdown_content': ''}

    decision_points = detect_decision_points(task_context, plan)

    assert any(dp.category == 'domain_model' for dp in decision_points)

def test_phase28_triggers_on_decision_points():
    """Phase 2.8 should trigger when decision points detected."""
    complexity_score = 5  # Below threshold
    review_score = 80  # Above threshold
    decision_points = [DecisionPoint(category='business_logic', question='Test')]

    should_trigger = should_trigger_phase28_checkpoint(
        complexity_score, review_score, decision_points
    )

    assert should_trigger is True

def test_decision_capture_workflow():
    """Should capture user decisions and update task file."""
    decision_point = DecisionPoint(
        id='dp-001',
        category='business_logic',
        question='What validation rules?'
    )

    user_choice = 'A'
    user_rationale = 'Stakeholder confirmed'

    resolved_decision = capture_decision(
        decision_point, user_choice, user_rationale
    )

    assert resolved_decision.status == 'resolved'
    assert resolved_decision.decision == 'A'
    assert resolved_decision.rationale == 'Stakeholder confirmed'
    assert resolved_decision.decided_at is not None
```

### Integration Tests

```python
def test_full_workflow_with_decision_points():
    """Test complete workflow from detection to task file update."""
    # Create test task
    task = create_test_task(description='Add validation to entity')

    # Run task-work through Phase 2
    result = run_task_work_phase2(task)

    # Should detect decision points
    assert result.decision_points_detected > 0

    # Trigger Phase 2.8
    assert result.phase28_triggered is True

    # Simulate user making decisions
    decisions = simulate_user_decisions(result.decision_points)

    # Update task file
    updated_task = apply_decisions_to_task(task, decisions)

    # Verify task file updated
    assert updated_task.frontmatter['has_decision_points'] is True
    assert len(updated_task.frontmatter['decision_points']) > 0
    assert '⚠️ DECISION POINTS' in updated_task.markdown_content
```

---

## Files to Create (Estimated)

1. `installer/global/commands/lib/decision_detection.py` - Decision point detection logic
2. `installer/global/commands/lib/decision_capture.py` - Interactive decision capture workflow
3. `tests/unit/test_decision_detection.py` - Unit tests for detection
4. `tests/unit/test_decision_capture.py` - Unit tests for capture workflow
5. `tests/integration/test_decision_workflow.py` - End-to-end integration tests

## Files to Modify (Estimated)

1. `installer/global/commands/lib/task_work_orchestrator.py` - Add decision detection to Phase 2
2. `installer/global/commands/lib/phase_28_checkpoint.py` - Enhance checkpoint display and options
3. `installer/global/commands/lib/task_file_manager.py` - Add decision points to frontmatter
4. `installer/global/commands/task-work.md` - Update documentation
5. `docs/guides/agentecflow-lite-workflow.md` - Document decision handling

---

## Dependencies

- ✅ Existing Phase 2.8 checkpoint implementation
- ✅ Task file frontmatter management
- ✅ Markdown plan generation

## Blocks

- None (can start immediately)

## Success Criteria

- ✅ Decision points detected automatically during Phase 2
- ✅ Phase 2.8 triggers when decision points found
- ✅ Enhanced checkpoint displays decision points clearly
- ✅ User can make decisions interactively
- ✅ Decisions captured and stored in task file
- ✅ Deferred decisions flagged with TODO in implementation
- ✅ All tests pass with ≥85% coverage
- ✅ Documentation updated with decision workflow
- ✅ Integration test proves end-to-end functionality

## Risk Assessment

**Risk Level**: Medium

**Risks**:
- **False Positives**: Heuristics might detect "decisions" that aren't actually ambiguous
  - *Mitigation*: Use high-confidence threshold by default, allow tuning
- **User Friction**: Adding checkpoint steps might slow down workflow
  - *Mitigation*: Only trigger when genuine decision points found, allow skip
- **Complexity Creep**: Decision tracking adds complexity to task files
  - *Mitigation*: Keep frontmatter structure simple, collapse resolved decisions

**Benefits Outweigh Risks**:
- Prevents mid-implementation blocking on business decisions
- Improves stakeholder communication
- Documents decision rationale for future reference
- Reduces rework from incorrect assumptions

## Time Estimate

- **Decision Detection Logic**: 1.5 hours
- **Phase 2.8 Enhancement**: 2 hours
- **Decision Capture Workflow**: 1.5 hours
- **Task File Integration**: 1 hour
- **Testing**: 2 hours
- **Documentation**: 1 hour
- **Integration Testing**: 1 hour
- **Total**: 4-6 hours

## Complexity Breakdown

**File Complexity**: Medium (5 new files, 5 modified files)
**Pattern Familiarity**: High (extends existing Phase 2.8 pattern)
**Risk Assessment**: Medium (affects core workflow checkpoint)
**Dependencies**: Low (builds on existing infrastructure)

**Overall**: 6/10 (Medium complexity - single focused enhancement)

---

## Next Steps After Completion

1. Monitor usage patterns to refine heuristics
2. Gather feedback on decision point detection accuracy
3. Consider adding LLM-powered decision detection (future enhancement)
4. Build decision point library for common patterns
5. Add decision point templates by domain (API, data model, validation)

---

## References

- Analysis Document: `docs/research/ANALYSIS-human-in-the-loop-pattern.md`
- Current Phase 2.8: `installer/global/commands/lib/phase_28_checkpoint.py` (if exists)
- Agentecflow Lite Guide: `docs/guides/agentecflow-lite-workflow.md`
- Task Work Command: `installer/global/commands/task-work.md`
