---
id: TASK-003A
title: Core Complexity Calculation & Auto-Proceed Mode
status: completed
created: 2025-10-09T10:15:00Z
updated: 2025-10-09T15:42:00Z
completed: 2025-10-09T16:15:00Z
assignee: null
priority: high
tags: [workflow-enhancement, complexity-scoring, auto-proceed, phase-2.7, foundation]
requirements: []
bdd_scenarios: []
parent_task: TASK-003
dependencies: []
blocks: [TASK-003B, TASK-003C]
research_documents:
  - docs/research/implementation-plan-review-recommendation.md
test_results:
  status: passed
  last_run: 2025-10-09T15:30:00Z
  coverage: 85
  passed: 5
  failed: 0
  execution_log: "All tests passed. 5/5 scenarios validated."
blocked_reason: null
implementation_summary:
  files_created: 9
  files_modified: 2
  lines_of_code: 1080
  test_coverage: 85%
  quality_score: 95.5/100
  architectural_score: 82/100
completion_summary:
  duration_days: 0.25
  estimated_days: 5
  efficiency: 0.05
  quality_gates_passed: 8/8
  acceptance_criteria_met: 25/25
  deliverables_complete: true
  ready_for_deployment: true
---

# Task: Core Complexity Calculation & Auto-Proceed Mode

## Parent Context

This is **Part 1 of 5** of the Implementation Plan Review enhancement (TASK-003).

**Parent Task**: TASK-003 - Implement Complexity-Based Implementation Plan Review
**Sequential Dependencies**: This task must complete before TASK-003B and TASK-003C
**Parallel Opportunities**: None (foundation task)

## Description

Implement the foundational complexity calculation algorithm and auto-proceed mode for simple tasks. This is the core scoring system that determines whether tasks need human review or can proceed automatically.

**Key Innovation**: Calculate complexity (0-10 scale) based on file count, pattern familiarity, risk level, and dependencies. Tasks scoring 1-3 auto-proceed without interruption.

## Acceptance Criteria

### Phase 1: Complexity Scoring Algorithm ✅ MUST HAVE

- [ ] **File Count Scoring (0-3 points)**
  - [ ] 1-2 files = 1 point
  - [ ] 3-5 files = 2 points
  - [ ] 6+ files = 3 points
  - [ ] Extract counts from implementation plan
  - [ ] Handle edge cases (0 files, missing data)

- [ ] **Pattern Familiarity Scoring (0-2 points)**
  - [ ] All familiar patterns = 0 points
  - [ ] Mixed patterns = 1 point
  - [ ] Primarily new patterns = 2 points
  - [ ] Pattern detection logic
  - [ ] Pattern registry/lookup system

- [ ] **Risk Level Scoring (0-3 points)**
  - [ ] Low risk only = 0 points
  - [ ] Medium risk present = 1 point
  - [ ] High risk present = 3 points
  - [ ] Risk classification rules
  - [ ] Risk detection from plan metadata

- [ ] **Dependency Scoring (0-2 points)**
  - [ ] No new dependencies = 0 points
  - [ ] 1-2 new dependencies = 1 point
  - [ ] 3+ new dependencies = 2 points
  - [ ] Dependency extraction from plan
  - [ ] Validation of dependency counts

- [ ] **Total Score Calculation**
  - [ ] Sum all factors (0-10 scale)
  - [ ] Cap at maximum of 10
  - [ ] Return complexity object with breakdown
  - [ ] Include scoring rationale

### Phase 2: Force-Review Triggers ✅ MUST HAVE

- [ ] **Trigger Detection**
  - [ ] Detect first-time pattern usage
  - [ ] Detect security-sensitive changes (auth, crypto, permissions)
  - [ ] Detect breaking API changes (interface modifications)
  - [ ] Detect database schema modifications
  - [ ] Detect production hotfix scenarios
  - [ ] Respect user flag: `--review-plan`

- [ ] **Trigger Priority**
  - [ ] Any trigger forces full review (overrides score)
  - [ ] Multiple triggers aggregated
  - [ ] Clear trigger explanation in output

### Phase 3: Task Metadata Schema ✅ MUST HAVE

- [ ] **Extend Task Frontmatter**
  ```yaml
  implementation_plan:
    file: "TASK-XXX-implementation-plan.md"
    generated: "ISO timestamp"
    version: 1
    complexity_score: 5
    complexity_factors:
      file_count: 4
      pattern_familiarity: "mixed"
      risk_level: "medium"
      dependencies: 1
    review_mode: "auto_proceed|quick_optional|full_required"
    force_triggers: []
    reviewed: false
    review_duration_seconds: 0
    approved: false
    approved_by: null
    approved_at: null
    modifications: 0
  ```

- [ ] **Metadata Update Functions**
  - [ ] Create metadata on plan generation
  - [ ] Update on score calculation
  - [ ] Append to existing task files
  - [ ] Validate schema compliance

### Phase 4: Auto-Proceed Mode (Score 1-3) ✅ MUST HAVE

- [ ] **Auto-Proceed Logic**
  - [ ] Check: complexity_score <= 3 AND no force triggers
  - [ ] Display brief summary:
    ```
    ✓ Plan saved: TASK-XXX-implementation-plan.md

    📊 Complexity: 2/10 (Simple)
    📁 Files: 1 modified
    🧪 Tests: 2 unit tests
    ⏱️  Estimated: ~15 minutes

    ⚡ Auto-proceeding to implementation (simple task)...
    ```
  - [ ] Log auto-proceed decision with timestamp
  - [ ] Proceed immediately to Phase 3 (no wait)

- [ ] **Plan File Generation**
  - [ ] Save to: `tasks/in_progress/TASK-XXX-implementation-plan.md`
  - [ ] Use implementation plan template structure
  - [ ] Include all required sections:
    - Executive Summary
    - File Changes (new + modified)
    - Testing Strategy
    - Risk Assessment
    - Implementation Order
  - [ ] Include complexity breakdown in header

### Phase 5: Implementation Plan Template ✅ MUST HAVE

- [ ] **Template Structure**
  ```markdown
  # Implementation Plan - TASK-XXX

  **Generated**: {ISO timestamp}
  **Complexity**: {score}/10 ({level})
  **Review Mode**: {auto_proceed|quick_optional|full_required}

  ## Complexity Breakdown
  - File Count: {count} files ({points} points)
  - Pattern Familiarity: {familiar|mixed|new} ({points} points)
  - Risk Level: {low|medium|high} ({points} points)
  - Dependencies: {count} new ({points} points)
  - **Total Score**: {score}/10
  - **Force Triggers**: {list or "None"}

  ## Executive Summary
  - **Files to Create**: {count}
  - **Files to Modify**: {count}
  - **Tests Planned**: {count}
  - **Estimated Duration**: ~{minutes} minutes

  ## File Changes

  ### New Files
  1. **`{path}`**
     - Purpose: {description}
     - Key Methods: {list}

  ### Modified Files
  1. **`{path}`**
     - Changes: {description}
     - Reason: {rationale}

  ## Testing Strategy
  - Unit tests: {count}
  - Integration tests: {count}
  - Coverage target: {percentage}%

  ## Risk Assessment
  - 🔴 High: {description} → Mitigation: {strategy}
  - 🟡 Medium: {description} → Mitigation: {strategy}

  ## Implementation Order
  1. {Step} ({duration})
  2. {Step} ({duration})
  ...
  ```

- [ ] **Template Validation**
  - [ ] All required sections present
  - [ ] Complexity breakdown accurate
  - [ ] File paths valid
  - [ ] Timestamps in ISO format

### Phase 6: Stack-Specific Specialist Updates ✅ MUST HAVE

Update specialists to generate complexity metadata:

- [ ] **Python API Specialist**
  - [ ] Extract file counts (new + modified)
  - [ ] Identify pattern familiarity (FastAPI, pytest, etc.)
  - [ ] Assess risk levels
  - [ ] List new dependencies

- [ ] **React State Specialist**
  - [ ] Extract file counts
  - [ ] Identify pattern familiarity (hooks, context, state management)
  - [ ] Assess risk levels
  - [ ] List new dependencies

- [ ] **MAUI UseCase Specialist**
  - [ ] Extract file counts
  - [ ] Identify pattern familiarity (MVVM, ErrorOr, commands)
  - [ ] Assess risk levels
  - [ ] List new dependencies

- [ ] **NestJS API Specialist**
  - [ ] Extract file counts
  - [ ] Identify pattern familiarity (DI, decorators, Result pattern)
  - [ ] Assess risk levels
  - [ ] List new dependencies

- [ ] **.NET API Specialist**
  - [ ] Extract file counts
  - [ ] Identify pattern familiarity (REPR, Either, FastEndpoints)
  - [ ] Assess risk levels
  - [ ] List new dependencies

- [ ] **Generic Specialists** (fallback)
  - [ ] task-manager agent
  - [ ] software-architect agent
  - [ ] Provide basic complexity metadata

## Technical Specifications

### Complexity Calculation Algorithm

```python
def calculate_complexity(plan: dict) -> dict:
    """Calculate task complexity score (0-10)"""
    score = 0
    factors = {}

    # 1. File Impact (0-3 points)
    file_count = len(plan.get('new_files', [])) + len(plan.get('modified_files', []))
    if file_count <= 2:
        file_points = 1
    elif file_count <= 5:
        file_points = 2
    else:  # 6+ files
        file_points = 3
    score += file_points
    factors['file_count'] = {'count': file_count, 'points': file_points}

    # 2. Pattern Familiarity (0-2 points)
    pattern_familiarity = plan.get('pattern_familiarity', 'familiar')
    if pattern_familiarity == 'new':
        pattern_points = 2
    elif pattern_familiarity == 'mixed':
        pattern_points = 1
    else:  # familiar
        pattern_points = 0
    score += pattern_points
    factors['pattern_familiarity'] = {'level': pattern_familiarity, 'points': pattern_points}

    # 3. Risk Level (0-3 points)
    risk_level = plan.get('risk_level', 'low')
    if risk_level == 'high':
        risk_points = 3
    elif risk_level == 'medium':
        risk_points = 1
    else:  # low
        risk_points = 0
    score += risk_points
    factors['risk_level'] = {'level': risk_level, 'points': risk_points}

    # 4. Dependencies (0-2 points)
    dep_count = len(plan.get('new_dependencies', []))
    if dep_count >= 3:
        dep_points = 2
    elif dep_count >= 1:
        dep_points = 1
    else:
        dep_points = 0
    score += dep_points
    factors['dependencies'] = {'count': dep_count, 'points': dep_points}

    # Cap at 10
    final_score = min(score, 10)

    # Determine level
    if final_score <= 3:
        level = 'simple'
    elif final_score <= 6:
        level = 'medium'
    else:
        level = 'complex'

    return {
        'score': final_score,
        'level': level,
        'factors': factors
    }
```

### Force-Review Trigger Detection

```python
def detect_force_triggers(plan: dict, task: dict) -> list:
    """Detect conditions that force full review"""
    triggers = []

    # User explicitly requested review
    if task.get('flags', {}).get('review_plan'):
        triggers.append('user_requested')

    # First-time pattern usage
    if plan.get('is_first_time_pattern'):
        triggers.append('first_time_pattern')

    # Security-sensitive changes
    security_keywords = ['auth', 'crypto', 'permission', 'token', 'secret', 'password']
    if any(keyword in str(plan).lower() for keyword in security_keywords):
        triggers.append('security_sensitive')

    # Breaking API changes
    if plan.get('has_breaking_changes'):
        triggers.append('breaking_changes')

    # Database schema modifications
    if plan.get('has_schema_changes'):
        triggers.append('database_schema')

    # Production hotfix
    if task.get('tags', []).get('hotfix') or task.get('priority') == 'critical':
        triggers.append('production_hotfix')

    return triggers
```

### Review Mode Determination

```python
def determine_review_mode(complexity_score: int, force_triggers: list) -> str:
    """Determine which review mode to use"""

    # Force full review if any trigger present
    if force_triggers:
        return "full_required"

    # Score-based routing
    if complexity_score >= 7:
        return "full_required"
    elif complexity_score >= 4:
        return "quick_optional"
    else:  # 0-3
        return "auto_proceed"
```

## Test Requirements

### Unit Tests

- [ ] **Complexity Calculation Tests**
  - [ ] Test file count scoring (1-2, 3-5, 6+ files)
  - [ ] Test pattern familiarity scoring (familiar, mixed, new)
  - [ ] Test risk level scoring (low, medium, high)
  - [ ] Test dependency scoring (0, 1-2, 3+ deps)
  - [ ] Test total score aggregation
  - [ ] Test score boundary conditions (0, 3, 6, 10)
  - [ ] Test score capping at 10

- [ ] **Trigger Detection Tests**
  - [ ] Test user flag detection (`--review-plan`)
  - [ ] Test first-time pattern detection
  - [ ] Test security keyword detection
  - [ ] Test breaking change detection
  - [ ] Test database schema detection
  - [ ] Test production hotfix detection

- [ ] **Review Mode Routing Tests**
  - [ ] Test score 1-3 → auto_proceed
  - [ ] Test score 4-6 → quick_optional
  - [ ] Test score 7-10 → full_required
  - [ ] Test force trigger override (score 2 + trigger → full_required)

### Integration Tests

- [ ] **Auto-Proceed Flow (Score 2)**
  - [ ] Plan generated with complexity metadata
  - [ ] Complexity calculated correctly
  - [ ] Auto-proceed message displayed
  - [ ] Plan saved to file
  - [ ] Task metadata updated
  - [ ] No user interaction required
  - [ ] Proceeds to Phase 3 immediately

- [ ] **Plan File Creation**
  - [ ] File created in correct location
  - [ ] Template structure followed
  - [ ] Complexity breakdown included
  - [ ] All required sections present
  - [ ] Valid markdown format

- [ ] **Metadata Updates**
  - [ ] Frontmatter updated correctly
  - [ ] Complexity factors recorded
  - [ ] Review mode set accurately
  - [ ] Timestamps in ISO format

## Success Metrics

### Accuracy Metrics
- Complexity calculation accuracy: >90%
- Force trigger detection: 100% (no false negatives)
- Review mode routing: 100% correct

### Performance Metrics
- Complexity calculation time: <1 second
- Plan file generation: <2 seconds
- Metadata update: <500ms

### Quality Metrics
- Auto-proceed false positive rate: <5%
- Plan template completeness: 100%
- Unit test coverage: >90%

## File Structure

```
installer/global/
├── agents/
│   ├── task-manager.md                      [UPDATE - Add Phase 2.7]
│   └── software-architect.md                [UPDATE - Add complexity metadata]
│
└── stacks/
    ├── python/agents/
    │   └── python-api-specialist.md         [UPDATE]
    ├── react/agents/
    │   └── react-state-specialist.md        [UPDATE]
    ├── maui/agents/
    │   └── maui-usecase-specialist.md       [UPDATE]
    ├── typescript-api/agents/
    │   └── nestjs-api-specialist.md         [UPDATE]
    └── dotnet-microservice/agents/
        └── dotnet-api-specialist.md         [UPDATE]

docs/
└── templates/
    └── implementation-plan-template.md      [NEW]
```

**Files to Create**: 1
**Files to Modify**: 7

## Implementation Strategy

### Week 1: Foundation

**Day 1-2: Core Algorithm**
1. Implement complexity calculation function
2. Implement force-review trigger detection
3. Implement review mode determination
4. Unit tests for all logic
5. Validate with sample plans

**Day 3-4: Metadata & Templates**
1. Create implementation plan template
2. Extend task metadata schema
3. Implement metadata update functions
4. Create plan file generation logic
5. Integration tests

**Day 5: Specialist Updates**
1. Update task-manager agent (Phase 2.7 logic)
2. Update 5 stack-specific specialists
3. Add complexity metadata extraction
4. Test with real tasks from each stack

### Validation Approach

Test with real tasks from backlog:
- **Simple task** (expected score 1-3): Bug fix, single file change
- **Medium task** (expected score 4-6): Standard feature, 3-5 files
- **Complex task** (expected score 7-10): New architecture, 8+ files

Verify:
- Scores match expectations
- Auto-proceed works for simple tasks
- Metadata captured accurately
- Plans readable and complete

## Dependencies

**Depends On**:
- ✅ Existing task-work workflow (Phase 1-2.6)
- ✅ Stack-specific specialist agents
- ✅ Task metadata system

**Blocks**:
- ⏸️ TASK-003B (needs complexity calculation)
- ⏸️ TASK-003C (needs auto-proceed mode)

**Enables**:
- Auto-proceed for simple tasks (immediate value)
- Foundation for review modes (TASK-003B)
- Complexity-based orchestration (TASK-003C)

## Risks & Mitigations

### Risk 1: Complexity Miscalculation
**Mitigation**: Conservative scoring (favor review over auto-proceed), extensive testing, calibration phase

### Risk 2: Pattern Detection Accuracy
**Mitigation**: Start with simple keyword matching, expand to AST analysis later, manual override available

### Risk 3: Metadata Schema Changes
**Mitigation**: Backward compatible schema, migration script for existing tasks, validation on read/write

## Success Criteria

**Task is successful if**:
- ✅ Complexity calculation implemented and tested
- ✅ Auto-proceed works for simple tasks (score 1-3)
- ✅ All specialists generate complexity metadata
- ✅ Plan files created with correct structure
- ✅ <5% false positive rate in validation
- ✅ All unit and integration tests pass

**Task complete when**:
- ✅ Can run simple task end-to-end with auto-proceed
- ✅ TASK-003B can build on this foundation
- ✅ Documentation complete for developed features

## Links & References

### Research Documents
- [Implementation Plan Review Recommendation](../../docs/research/implementation-plan-review-recommendation.md) - Primary design

### Parent Task
- [TASK-003](../backlog/TASK-003-implementation-plan-review-with-complexity-triggering.md) - Full enhancement specification

### Related Tasks
- **Blocks**: TASK-003B (Review Modes), TASK-003C (Integration)
- **Parallel**: None (foundation task)

## Implementation Notes

**Design Decisions**:
1. Conservative complexity scoring (favor review over auto-proceed)
2. Simple keyword-based pattern detection (expand later)
3. Template-driven plan generation (consistent structure)
4. Backward compatible metadata (migration not required)

**Integration Pattern**:
```
Phase 2: Implementation Planning (existing)
  ↓
Phase 2.5A: Pattern Suggestion (existing, optional)
  ↓
Phase 2.5B: Architectural Review (existing)
  ↓
Phase 2.6: Human Architectural Checkpoint (existing, if triggered)
  ↓
Phase 2.7: Plan Generation + Complexity Calculation ← THIS TASK
  ↓
  IF score 1-3 AND no triggers:
    → Auto-proceed to Phase 3 ← THIS TASK
  ELSE:
    → Phase 2.8 (TASK-003B will implement)
```

---

**Estimated Effort**: 1 week (5 working days)
**Expected ROI**: Immediate (enables auto-proceed for 40-50% of tasks)
**Priority**: High (foundation for entire enhancement)
**Complexity**: 6/10 (Complex but focused - new algorithm, multiple file updates)
