---
id: TASK-005
title: Add Complexity Evaluation to task-create Command
status: completed
created: 2025-10-09T18:00:00Z
updated: 2025-10-11T00:00:00Z
completed: 2025-10-11T00:00:00Z
assignee: null
priority: high
tags: [workflow-enhancement, complexity-scoring, task-creation, task-splitting, user-experience]
requirements: []
bdd_scenarios: []
parent_task: null
dependencies: [TASK-003A]
blocks: []
related_tasks: [TASK-003A, TASK-003B, TASK-003C]
research_documents:
  - docs/research/implementation-plan-review-recommendation.md
  - installer/global/commands/task-create.md
test_results:
  status: passed
  last_run: 2025-10-11T00:00:00Z
  coverage:
    line: 93.1
    branch: 88.9
  passed: 69
  failed: 0
  execution_log: "All 69 tests passing (100%). Coverage: 93.1% line, 88.9% branch."
blocked_reason: null
estimated_effort:
  original: "1 week"
  actual: "4-5 hours"
  complexity: "6/10 (Medium)"
  justification: "Reuses TASK-003 complexity algorithms, moderate UI integration"
completion_summary:
  quality_gates_passed: 5
  code_review_score: 88
  architecture_compliance: 100
  dry_violation_resolved: true
  files_created: 7
  lines_of_code: 510
  test_coverage: 93.1
---

# Task: Add Complexity Evaluation to task-create Command

## Business Context

**Problem**: Users often create tasks that are too large or complex, leading to:
- Mid-implementation realization that the task should be split
- Wasted time on planning and starting oversized tasks
- Inconsistent task granularity across the project
- Difficulty tracking progress on large tasks

**Solution**: Add upfront complexity evaluation during task creation to identify oversized tasks BEFORE work begins, with automatic split recommendations.

**Business Value**:
- Save 2-4 hours per oversized task (early detection vs. mid-implementation split)
- Improve task granularity and predictability
- Better sprint planning with right-sized tasks
- Consistent complexity across all tasks

## Description

Enhance the `/task-create` command with **Phase 2.5: Upfront Complexity Evaluation** that analyzes task requirements and suggests splitting oversized tasks before implementation begins.

**Key Innovation**: Reuse TASK-003's complexity scoring algorithm but apply it UPFRONT based on requirements/description rather than after implementation planning.

### Two-Stage Complexity System

**Stage 1 (TASK-005 - Upfront)**: Estimate complexity from requirements BEFORE work starts
- Input: Task title, description, requirements (EARS notation)
- Purpose: Decide if task should be split
- When: During `/task-create`

**Stage 2 (TASK-003 - Implementation)**: Calculate complexity from implementation plan AFTER planning
- Input: Implementation plan (files, patterns, risks, dependencies)
- Purpose: Decide review mode (auto-proceed/quick/full)
- When: During `/task-work` Phase 2.7

### User Experience

```bash
$ /task-create "Implement event sourcing for orders" requirements:[REQ-042,REQ-043]

✅ Task metadata created
✅ Requirements validated
⏳ Analyzing task complexity...

╔════════════════════════════════════════════════════════════╗
║ 📊 TASK COMPLEXITY ANALYSIS                                ║
╚════════════════════════════════════════════════════════════╝

ESTIMATED COMPLEXITY: 9/10 (Very Complex)

COMPLEXITY FACTORS:
  🔴 Requirements suggest 8+ files (Event Sourcing pattern)
  🔴 New architecture pattern (Event Sourcing unfamiliar)
  🔴 High risk: State consistency, event replay
  🟡 Multiple new dependencies (event store libraries)

⚠️  RECOMMENDATION: Consider splitting this task

SUGGESTED BREAKDOWN:
1. TASK-005.1: Design Event Sourcing architecture (2 days)
   - Create ADR, design event schema
   - Complexity: 5/10 (Medium)

2. TASK-005.2: Implement EventStore infrastructure (3 days)
   - EventStore, EventBus, EventRepository
   - Complexity: 6/10 (Medium)

3. TASK-005.3: Implement Order aggregate with events (2 days)
   - Order aggregate root, domain events
   - Complexity: 5/10 (Medium)

4. TASK-005.4: Implement CQRS handlers (2 days)
   - Command and query handlers
   - Complexity: 5/10 (Medium)

5. TASK-005.5: Testing and integration (2 days)
   - Event replay tests, integration tests
   - Complexity: 6/10 (Medium)

OPTIONS:
1. [C]reate - Create this task as-is (complexity 9/10)
2. [S]plit - Create 5 subtasks instead (recommended)
3. [M]odify - Adjust task scope to reduce complexity
4. [A]bort - Cancel task creation

Your choice (C/S/M/A): _
```

## Acceptance Criteria

### Phase 1: Upfront Complexity Estimation (Week 1 - Days 1-3)

- [ ] **Complexity Estimation Algorithm**
  - [ ] Reuse TASK-003A complexity scoring (0-10 scale)
  - [ ] Adapt for requirements-based estimation (not implementation plan)
  - [ ] File count estimation from requirements keywords
    - CRUD → 4 files
    - API endpoint → 3 files
    - Event Sourcing → 8+ files
    - Authentication → 5 files
  - [ ] Pattern familiarity detection from requirements
    - Known patterns: CRUD, REST API, validation
    - New patterns: Event Sourcing, CQRS, GraphQL
  - [ ] Risk assessment from requirements
    - Security keywords → High risk
    - Database schema → High risk
    - External API → Medium risk
  - [ ] Dependency estimation from requirements
    - New authentication → 2 deps
    - New database → 1 dep
    - New framework → 3+ deps

- [ ] **Split Threshold Configuration**
  - [ ] Default threshold: 7/10 (same as TASK-003 full review)
  - [ ] Configurable in `.claude/settings.json`
  - [ ] Command-line override: `--split-threshold N`

- [ ] **Integration with task-create Command**
  - [ ] Add Phase 2.5 after metadata creation
  - [ ] Run complexity estimation automatically
  - [ ] Display complexity score and factors
  - [ ] Show split recommendation if score ≥ 7

### Phase 2: Interactive Split Recommendation (Week 1 - Days 4-5)

- [ ] **Split Recommendation UI**
  - [ ] Display complexity score with color coding
    - 1-3: Green (Simple)
    - 4-6: Yellow (Medium)
    - 7-10: Red (Complex - recommend split)
  - [ ] Show complexity factors breakdown
  - [ ] List suggested subtasks (if score ≥ 7)
  - [ ] Provide decision options (C/S/M/A)

- [ ] **Decision Option Handlers**
  - [ ] **[C]reate**: Create task as-is
    - Save complexity score in metadata
    - Proceed with single task creation
  - [ ] **[S]plit**: Create subtasks
    - Generate subtask IDs (TASK-XXX.1, TASK-XXX.2, etc.)
    - Create parent task in `archived` state
    - Create N subtasks in `backlog` state
    - Link subtasks to parent
  - [ ] **[M]odify**: Adjust scope
    - Interactive scope reduction
    - Re-calculate complexity
    - Return to decision prompt
  - [ ] **[A]bort**: Cancel creation
    - No files created
    - Return to command prompt

- [ ] **Automatic Subtask Generation**
  - [ ] Analyze requirements for logical splits
  - [ ] Generate subtask titles and descriptions
  - [ ] Estimate complexity for each subtask
  - [ ] Ensure subtasks total < original complexity
  - [ ] Link requirements to appropriate subtasks

### Phase 3: Configuration & Flags (Week 1 - Day 5)

- [ ] **Settings.json Configuration**
  - [ ] Add `task_creation.complexity_analysis` section
  - [ ] Configure `enabled`: true/false
  - [ ] Configure `split_threshold`: 7 (default)
  - [ ] Configure `auto_suggest_breakdown`: true/false
  - [ ] Configure `interactive_mode`: true/false

- [ ] **Command-Line Flags**
  - [ ] `--skip-complexity-check`: Skip analysis
  - [ ] `--force-split-check`: Always show even if <7
  - [ ] `--split-threshold N`: Custom threshold
  - [ ] `--auto-split`: Auto-create subtasks if ≥ threshold

### Phase 4: Testing & Validation (Week 1 - Days 3-5, parallel)

- [ ] **Unit Tests**
  - [ ] Test complexity estimation from requirements
  - [ ] Test file count estimation by pattern
  - [ ] Test pattern familiarity detection
  - [ ] Test risk assessment logic
  - [ ] Test dependency estimation
  - [ ] Test threshold evaluation

- [ ] **Integration Tests**
  - [ ] Test full task-create flow with complexity check
  - [ ] Test Create option (C) - single task
  - [ ] Test Split option (S) - multiple subtasks
  - [ ] Test Modify option (M) - scope reduction
  - [ ] Test Abort option (A) - cancel
  - [ ] Test skip flag behavior

- [ ] **Edge Cases**
  - [ ] Task with no requirements (use title only)
  - [ ] Task with minimal description
  - [ ] Task with very high complexity (10/10)
  - [ ] Task exactly at threshold (7/10)
  - [ ] Invalid split recommendations

### Phase 5: Documentation (Week 1 - Day 5)

- [ ] **Update task-create.md Command**
  - [ ] Document Phase 2.5: Complexity Analysis
  - [ ] Document complexity scoring factors
  - [ ] Document split recommendations
  - [ ] Document decision options
  - [ ] Add usage examples

- [ ] **Update CLAUDE.md**
  - [ ] Add section on task complexity evaluation
  - [ ] Document two-stage complexity system
  - [ ] Explain when to use vs. skip
  - [ ] Best practices for task sizing

- [ ] **Create User Guide**
  - [ ] How to interpret complexity scores
  - [ ] When to split vs. keep tasks
  - [ ] How to reduce task complexity
  - [ ] Examples of good task granularity

## Technical Specifications

### Complexity Estimation Algorithm (Upfront Version)

```python
def estimate_task_complexity_upfront(task_data: dict) -> dict:
    """
    Estimate complexity BEFORE implementation planning.
    Based on requirements and task description.
    """
    score = 0

    # 1. Estimate file impact from requirements (0-3 points)
    estimated_files = estimate_files_from_requirements(
        task_data['requirements'],
        task_data['title']
    )
    if estimated_files <= 2:
        score += 1
    elif estimated_files <= 5:
        score += 2
    else:  # 6+ files
        score += 3

    # 2. Pattern familiarity from requirements (0-2 points)
    patterns = detect_patterns_from_requirements(
        task_data['requirements'],
        task_data['title']
    )
    if patterns['unfamiliar_count'] > 0:
        score += 2
    elif patterns['mixed']:
        score += 1

    # 3. Risk assessment from requirements (0-3 points)
    risks = assess_risk_from_requirements(task_data['requirements'])
    if risks['high_risk_count'] > 0:
        score += 3
    elif risks['medium_risk_count'] > 0:
        score += 1

    # 4. Estimated dependencies (0-2 points)
    estimated_deps = estimate_dependencies_from_requirements(
        task_data['requirements']
    )
    if estimated_deps >= 3:
        score += 2
    elif estimated_deps >= 1:
        score += 1

    return {
        'score': min(score, 10),
        'level': get_complexity_level(score),
        'estimated_files': estimated_files,
        'patterns': patterns,
        'risks': risks,
        'dependencies': estimated_deps,
        'should_split': score >= 7,
        'confidence': calculate_estimation_confidence(task_data)
    }

def get_complexity_level(score: int) -> str:
    """Map score to level"""
    if score <= 3:
        return "Simple"
    elif score <= 6:
        return "Medium"
    else:
        return "Complex"
```

### File Count Estimation Heuristics

```python
PATTERN_FILE_ESTIMATES = {
    # CRUD operations
    'crud': 4,              # Model, Service, Controller, Tests
    'create': 2,            # Service + Tests
    'read': 1,              # Query only
    'update': 2,            # Service + Tests
    'delete': 2,            # Service + Tests

    # API patterns
    'rest_api': 3,          # Route, Controller, Tests
    'graphql': 4,           # Schema, Resolver, Tests, Types
    'websocket': 3,         # Handler, Event, Tests

    # Architecture patterns
    'event_sourcing': 8,    # Events, Store, Bus, Repository, Tests
    'cqrs': 6,              # Commands, Queries, Handlers, Tests
    'microservice': 10,     # Full service structure
    'authentication': 5,    # Auth service, middleware, guards, tests

    # UI patterns
    'react_component': 2,   # Component + Tests
    'form': 3,              # Form, Validation, Tests
    'page': 2,              # Page + Tests

    # Infrastructure
    'database_schema': 3,   # Migration, Seeds, Tests
    'api_client': 4,        # Client, Types, Error handling, Tests
}

def estimate_files_from_requirements(requirements: list, title: str) -> int:
    """Estimate file count from requirements and title"""

    # Check title for pattern keywords
    title_lower = title.lower()
    estimated_files = 1  # Default minimum

    for pattern, file_count in PATTERN_FILE_ESTIMATES.items():
        if pattern in title_lower:
            estimated_files = max(estimated_files, file_count)

    # Adjust based on requirements complexity
    if len(requirements) > 5:
        estimated_files += 2  # More requirements = more files

    return estimated_files
```

### Split Recommendation Generator

```python
def generate_split_recommendations(
    task_data: dict,
    complexity: dict
) -> list[dict]:
    """
    Generate suggested task splits based on complexity analysis.
    """

    if complexity['score'] < 7:
        return []  # No split needed

    recommendations = []

    # Split strategies by pattern
    if 'event_sourcing' in complexity['patterns']['detected']:
        recommendations = [
            {
                'title': 'Design Event Sourcing architecture',
                'description': 'Create ADR, design event schema',
                'estimated_duration': '2 days',
                'estimated_complexity': 5
            },
            {
                'title': 'Implement EventStore infrastructure',
                'description': 'EventStore, EventBus, EventRepository',
                'estimated_duration': '3 days',
                'estimated_complexity': 6
            },
            {
                'title': 'Implement domain aggregates with events',
                'description': 'Aggregate roots, domain events',
                'estimated_duration': '2 days',
                'estimated_complexity': 5
            },
            {
                'title': 'Implement CQRS handlers',
                'description': 'Command and query handlers',
                'estimated_duration': '2 days',
                'estimated_complexity': 5
            },
            {
                'title': 'Testing and integration',
                'description': 'Event replay tests, integration tests',
                'estimated_duration': '2 days',
                'estimated_complexity': 6
            }
        ]
    elif 'microservice' in complexity['patterns']['detected']:
        # Microservice split strategy
        pass
    elif complexity['estimated_files'] > 8:
        # Generic split by layer
        recommendations = generate_layered_split(task_data, complexity)
    else:
        # Generic split by feature
        recommendations = generate_feature_split(task_data, complexity)

    return recommendations
```

### Task Metadata Extension

Add to task frontmatter:

```yaml
---
id: TASK-XXX
# ... existing fields ...

complexity_analysis:
  upfront_estimate:
    score: 9
    level: "Complex"
    estimated_files: 8
    patterns:
      detected: ["event_sourcing"]
      unfamiliar: ["event_sourcing"]
    risks:
      high: ["state_consistency", "event_replay"]
      medium: []
    dependencies: 2
    should_split: true
    confidence: 0.75
    estimated_at: "2025-10-09T18:00:00Z"

  split_decision:
    user_choice: "split"  # or "create", "modify", "abort"
    subtasks_created: 5
    parent_task: "TASK-005"
    decided_at: "2025-10-09T18:01:30Z"
---
```

## Implementation Strategy

### Week 1 Breakdown

**Day 1-2: Core Estimation Logic**
- Implement complexity estimation algorithm (reuse TASK-003A)
- Adapt for requirements-based input (not implementation plan)
- Create file count estimation heuristics
- Create pattern detection logic
- Unit tests for estimation

**Day 3: Integration with task-create**
- Add Phase 2.5 to task-create command
- Display complexity analysis UI
- Integrate decision prompts
- Basic end-to-end test

**Day 4: Split Recommendation**
- Implement split recommendation generator
- Create subtask title/description generation
- Implement automatic subtask creation
- Link parent/child tasks properly

**Day 5: Configuration, Testing, Documentation**
- Add settings.json configuration
- Add command-line flags
- Complete integration tests
- Write documentation
- Update CLAUDE.md

### Dependency on TASK-003A

This task DEPENDS on TASK-003A being completed first because:
1. Reuses the same complexity calculation algorithm
2. Uses same complexity factor definitions
3. Shares configuration schema structure

**If TASK-003A not done yet**: Implement minimal complexity calculation in TASK-005, then refactor both to share code later.

## Success Metrics

### Immediate Metrics (First 30 Days)

**Usage Metrics**:
- % tasks analyzed for complexity: Target 100%
- % tasks flagged as complex (≥7): Expected 15-20%
- % users accepting split recommendations: Target 60%+
- % users using skip flag: <10% (means feature is useful)

**Quality Metrics**:
- Estimation accuracy: Compare upfront estimate to actual Phase 2.7 score
- False positives: Tasks flagged but didn't need split
- False negatives: Tasks not flagged but should have split

**Efficiency Metrics**:
- Time saved per oversized task: Target 2-4 hours
- Reduction in mid-implementation task splits: Target 50%

### Long-Term Metrics (6+ Months)

**Task Quality Metrics**:
- Average task complexity: Target 4-6 (medium range)
- Task completion time variability: Reduced by 30%
- Oversized tasks created: Reduced by 70%

**Developer Experience**:
- Satisfaction with task sizing: Target 80%+
- Usefulness of split recommendations: Target 75%+

## Risks & Mitigations

### Risk 1: Estimation Inaccuracy

**Risk**: Upfront estimates differ significantly from actual complexity

**Mitigation**:
- Track estimation accuracy and calibrate
- Show confidence level with estimate
- Allow easy override with flags
- Improve heuristics based on data

### Risk 2: Poor Split Recommendations

**Risk**: Suggested splits don't make logical sense

**Mitigation**:
- Use pattern-based split strategies
- Allow user to modify splits
- Learn from user modifications
- Improve recommendation logic iteratively

### Risk 3: User Fatigue from Interruptions

**Risk**: Users annoyed by complexity checks

**Mitigation**:
- Only show for complex tasks (≥7)
- Configurable threshold
- Skip flag available
- Fast analysis (<2 seconds)

### Risk 4: Dependency on TASK-003A

**Risk**: TASK-003A not completed, blocking this task

**Mitigation**:
- Implement minimal version independently
- Refactor to share code later
- Document shared components
- Plan joint refactoring task

## Dependencies

**Depends On**:
- TASK-003A (Core Complexity Calculation) - Preferred but not blocking

**Enables**:
- Better task granularity across project
- More predictable sprint planning
- Reduced wasted time on oversized tasks

## Related Tasks

- **TASK-003A**: Core Complexity Calculation (shares algorithm)
- **TASK-003B**: Review Modes (shares threshold concepts)
- **TASK-003C**: Integration with task-work (two-stage complexity)

## Future Enhancements

### Enhancement 1: Machine Learning for Estimation

Train model on historical data to improve upfront estimates.

### Enhancement 2: Epic-Level Complexity Analysis

Analyze entire epics for overall complexity and suggest feature breakdown.

### Enhancement 3: Team Pattern Learning

Learn from past task splits to improve recommendations.

### Enhancement 4: IDE Integration

Show complexity estimate directly in IDE when creating tasks via UI.

## Implementation Notes

[To be filled during implementation]

---

**Estimated Effort**: 1 week (5 days)
**Complexity**: 6/10 (Medium - reuses TASK-003 logic, moderate UI integration)
**Priority**: High (improves task quality and developer productivity)
**Expected ROI**: 2-4 hours saved per oversized task detected

---

## Test Execution Log

[Automatically populated when tests are run]
