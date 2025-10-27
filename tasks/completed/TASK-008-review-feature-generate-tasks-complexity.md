---
id: TASK-008
title: Review and Enhance /feature-generate-tasks for Complexity Control
status: completed
created: 2025-10-11T14:45:00Z
updated: 2025-10-11T15:35:00Z
completed_at: 2025-10-11T15:35:00Z
priority: high
tags: [command-enhancement, complexity-control, task-generation, feature-management]
epic: null
feature: null
requirements: []
external_ids:
  epic_jira: null
  epic_linear: null
  jira: null
  linear: null
bdd_scenarios: []
test_results:
  status: passed
  total_tests: 54
  passed: 54
  failed: 0
  coverage_line: 81.6
  coverage_branch: 87
  execution_time: 0.65
  last_run: 2025-10-11T15:25:00Z
previous_state: in_review
state_transition_reason: "Task completed - all quality gates passed, implementation complete"
completion_summary:
  duration_days: 0.5
  estimated_days: 1.0
  variance: -50%
  quality_score: 5
  files_created: 11
  lines_of_code: 1700
  test_coverage: 81.6
complexity_evaluation:
  score: 5
  level: moderate
  review_mode: quick_optional
  auto_approved: true
  approved_by: timeout
  approved_at: 2025-10-11T15:05:00Z
architectural_review:
  score: 87
  status: approved
  solid_score: 44
  dry_score: 24
  yagni_score: 19
code_review:
  status: approved
  rating: 5
  reviewer: code-reviewer
  reviewed_at: 2025-10-11T15:28:00Z
  blockers: 0
  critical_issues: 0
  major_issues: 0
  minor_issues: 4
---

# Task: Review and Enhance /feature-generate-tasks for Complexity Control

## Context

We've recently made significant enhancements to both `/task-create` and `/task-work` commands:

### Recent `/task-create` Enhancements (TASK-005)
- **Complexity evaluation** - Automatic assessment of task complexity (1-10 scale)
- **Complexity-based warnings** - Alerts when tasks may be too complex
- **Task breakdown suggestions** - Recommends splitting complex tasks (complexity ≥ 7)
- **Enhanced metadata** - Tracks complexity scores and breakdown recommendations

### Recent `/task-work` Enhancements (TASK-006)
- **Design-first workflow** - `--design-only` and `--implement-only` flags
- **Complexity-based routing** - Auto-triggers human checkpoint for complex tasks
- **Phase 2.7** - Complexity evaluation and plan persistence
- **Phase 2.8** - Human checkpoint with approval/rejection workflow

### The Problem

The `/feature-generate-tasks` command currently generates tasks from features without considering the complexity controls added to `/task-create`. This leads to:

1. **Tasks too complex for single implementation** - Some generated tasks have too much scope
2. **Missed complexity warnings** - Generated tasks bypass complexity evaluation
3. **No breakdown suggestions** - Complex tasks aren't automatically flagged for splitting
4. **Inconsistent workflow** - Manual task creation benefits from complexity checks, auto-generation doesn't

### Real-World Impact

When we've run `/feature-generate-tasks` in the past, we've encountered situations where:
- A generated task looked reasonable in scope
- During implementation with `/task-work`, we discovered it was actually too complex
- Had to manually break down the task mid-implementation
- Lost time and context from the interruption

## Objective

Enhance `/feature-generate-tasks` to integrate with the new complexity controls, ensuring all generated tasks are appropriately scoped and ready for implementation.

## Requirements

### 1. Integration with /task-create Complexity Logic

**Requirement**: `/feature-generate-tasks` must use the same complexity evaluation logic as `/task-create`.

**Implementation**:
- Import or reference the complexity evaluation module from `/task-create`
- Apply complexity scoring to each proposed task before creation
- Store complexity metadata in generated task files

### 2. Automatic Task Breakdown for Complex Tasks

**Requirement**: When a proposed task has complexity ≥ 7, automatically break it down into smaller sub-tasks.

**Implementation**:
- Detect complex tasks during generation phase
- Apply AI-driven task decomposition
- Generate 2-4 smaller sub-tasks instead of 1 complex task
- Ensure sub-tasks maintain clear dependencies and logical flow

**Example**:
```
Original Complex Task (Complexity: 8):
"Implement complete authentication system with JWT, OAuth2, and session management"

Broken Down Into (Complexity: 4-5 each):
├── TASK-XXX.1: Implement JWT token generation and validation
├── TASK-XXX.2: Add OAuth2 provider integration (Google, GitHub)
├── TASK-XXX.3: Create session management with Redis
└── TASK-XXX.4: Integrate authentication middleware across endpoints
```

### 3. Complexity Visualization in Generation Output

**Requirement**: Display complexity scores and warnings during task generation preview.

**Implementation**:
- Show complexity score next to each proposed task
- Add visual indicators for complexity levels:
  - 🟢 Simple (1-3)
  - 🟡 Medium (4-6)
  - 🔴 Complex (7-10) - with auto-breakdown note
- Provide summary statistics (average complexity, distribution)

**Example Output**:
```bash
/feature-generate-tasks FEAT-001

🔄 Generating Tasks for FEAT-001: User Authentication

📋 Complexity-Aware Task Generation

🎨 UI/UX Tasks
✅ TASK-043: Design authentication UI components
   Complexity: 🟡 5 (Medium) | Timeline: 2 days

✅ TASK-044: Implement responsive login form
   Complexity: 🟢 4 (Medium) | Timeline: 1 day

🔌 API/Backend Tasks
⚠️  Original: "Complete authentication backend with JWT, OAuth2, and sessions"
   Complexity: 🔴 9 (Too Complex) - Auto-broken down into:

   ✅ TASK-045.1: Implement JWT authentication endpoint
      Complexity: 🟡 5 (Medium) | Timeline: 1.5 days

   ✅ TASK-045.2: Add OAuth2 provider integration
      Complexity: 🟡 6 (Medium) | Timeline: 2 days

   ✅ TASK-045.3: Create session management system
      Complexity: 🟡 5 (Medium) | Timeline: 1.5 days

📊 Complexity Analysis
Total Tasks: 5 (after breakdown from 3 original)
Complexity Distribution:
  🟢 Simple (1-3): 0 tasks
  🟡 Medium (4-6): 5 tasks
  🔴 Complex (7-10): 0 tasks (all broken down)
Average Complexity: 5.0
Recommended for immediate implementation: ✅ All tasks ready
```

### 4. Interactive Complexity Adjustment

**Requirement**: In `--interactive` mode, allow users to adjust complexity thresholds and review breakdown suggestions.

**Implementation**:
- Prompt for complexity threshold override (default: 7)
- Show breakdown suggestions for borderline tasks (complexity 6-7)
- Allow manual approval/rejection of automatic breakdowns
- Option to merge simple tasks if too granular

**Example Interactive Flow**:
```bash
/feature-generate-tasks FEAT-001 --interactive

🔄 Interactive Complexity-Aware Task Generation

⚠️ Complex Task Detected
Task: "Complete authentication backend"
Complexity Score: 9/10
Recommended Action: Break down into smaller tasks

Suggested Breakdown (3 sub-tasks):
1. JWT authentication (Complexity: 5)
2. OAuth2 integration (Complexity: 6)
3. Session management (Complexity: 5)

Accept breakdown? [y/n/customize]: y

✅ Breakdown accepted - generating 3 sub-tasks
```

### 5. Quality Gate Integration

**Requirement**: Ensure generated tasks align with quality gates and testing requirements.

**Implementation**:
- Calculate estimated test coverage needs based on complexity
- Add appropriate testing tasks for complex features
- Link test tasks to implementation tasks
- Validate acceptance criteria can be verified

### 6. Validation Against Existing Tasks

**Requirement**: Prevent duplicate or overlapping tasks during generation.

**Implementation**:
- Check existing tasks in all directories (backlog, in_progress, completed)
- Detect similar task titles and scopes
- Warn about potential duplicates before creation
- Suggest linking to existing tasks instead of creating new ones

## Acceptance Criteria

- [ ] `/feature-generate-tasks` applies complexity evaluation to all proposed tasks
- [ ] Tasks with complexity ≥ 7 are automatically broken down into smaller sub-tasks
- [ ] Complexity scores are displayed in generation output with visual indicators
- [ ] Average complexity and distribution statistics are shown
- [ ] `--interactive` mode allows complexity threshold customization
- [ ] Generated tasks include complexity metadata in frontmatter
- [ ] No tasks with complexity > 7 are created without breakdown
- [ ] Documentation is updated with complexity control examples
- [ ] Testing tasks are auto-generated for high-complexity features
- [ ] Duplicate task detection works across all task directories

## Technical Approach

### 1. Complexity Evaluation Module

**Location**: `installer/global/commands/lib/complexity_evaluator.py` (if exists) or create new module

**Interface**:
```python
def evaluate_task_complexity(task_title: str,
                             description: str,
                             requirements: List[str],
                             acceptance_criteria: List[str]) -> ComplexityScore:
    """
    Evaluate task complexity on 1-10 scale.

    Returns:
        ComplexityScore with score, factors, and breakdown recommendation
    """
    pass

def suggest_task_breakdown(task: Task,
                          complexity: ComplexityScore) -> List[SubTask]:
    """
    Suggest sub-task breakdown for complex tasks.

    Returns:
        List of sub-tasks with estimated complexity for each
    """
    pass
```

### 2. Feature Generation Flow

**Updated Algorithm**:
```
1. Parse feature requirements and acceptance criteria
2. Generate initial task proposals (existing logic)
3. FOR EACH proposed task:
   a. Evaluate complexity score
   b. IF complexity >= 7:
      - Generate breakdown suggestions
      - Create sub-tasks
      - Link sub-tasks to parent
   c. ELSE:
      - Keep original task
4. Display complexity analysis
5. IF interactive mode:
   - Allow user review of breakdowns
   - Accept/reject/customize suggestions
6. Create final task files with metadata
7. Output summary with complexity statistics
```

### 3. File Updates Required

- [x] `installer/global/commands/feature-generate-tasks.md` - Add complexity control documentation
- [ ] `installer/global/commands/lib/feature_task_generator.py` (if exists) - Integrate complexity logic
- [ ] `installer/global/commands/lib/complexity_evaluator.py` - Create if doesn't exist, or reference from task-create
- [ ] `docs/adr/` - Document decision on complexity thresholds and breakdown strategies
- [ ] Test coverage for complexity-aware generation

## Test Requirements

### Unit Tests
- [ ] Test complexity evaluation for various task scopes
- [ ] Test automatic breakdown for complex tasks (complexity ≥ 7)
- [ ] Test breakdown suggestion algorithm produces valid sub-tasks
- [ ] Test complexity score calculation is consistent with `/task-create`

### Integration Tests
- [ ] Test full feature-to-tasks generation with complexity checks
- [ ] Test interactive mode complexity customization
- [ ] Test generated tasks include proper metadata
- [ ] Test duplicate detection across task directories

### E2E Tests
- [ ] Test complete workflow: feature creation → task generation → task work
- [ ] Verify complex tasks are broken down automatically
- [ ] Verify breakdown suggestions are sensible and implementable
- [ ] Test complexity warnings appear correctly

## Implementation Notes

### Reuse Existing Complexity Logic

If TASK-005 created a complexity evaluation module, **REUSE IT** rather than duplicating logic. The complexity scoring should be consistent between:
- Manual task creation (`/task-create`)
- Automatic task generation (`/feature-generate-tasks`)
- Task work complexity evaluation (`/task-work` Phase 2.7)

### Breakdown Strategies

**Rule of thumb for breaking down complex tasks**:
1. **Horizontal split** - Separate by architectural layers (UI, API, Database)
2. **Vertical split** - Separate by user stories or features
3. **Technical split** - Separate by technical concerns (auth, validation, error handling)
4. **Temporal split** - Separate by implementation phases (setup, core logic, edge cases)

**Example**: "Complete user authentication system" (Complexity: 9)
- Horizontal: UI components, API endpoints, database schema
- Vertical: Login flow, registration flow, password reset flow
- Technical: Authentication logic, authorization logic, session management
- Temporal: Basic auth, token management, security hardening

Choose split strategy based on feature structure and team collaboration needs.

### Complexity Thresholds

**Recommended defaults**:
- **1-3 (Simple)**: Single developer, < 4 hours, clear approach
- **4-6 (Medium)**: Single developer, 4-8 hours, may need some research
- **7-8 (Complex)**: Consider breakdown, > 8 hours, multiple sub-systems
- **9-10 (Very Complex)**: MUST break down, unclear scope, high risk

**Customization**: Allow projects to override thresholds in `.claude/settings.json`:
```json
{
  "complexity_thresholds": {
    "auto_breakdown": 7,
    "warning_threshold": 6,
    "simple_max": 3
  }
}
```

## Success Metrics

### Quantitative
- **Reduction in mid-implementation task breakdowns**: Target 80% reduction
- **Average task complexity**: Target 4-5 (medium range)
- **Tasks requiring breakdown in `/task-work`**: Target < 5%
- **Time saved**: Estimate 2-4 hours per complex task caught early

### Qualitative
- Developers feel more confident starting tasks
- Tasks feel "right-sized" for single implementation sessions
- Fewer surprises during implementation
- Better sprint planning due to accurate complexity estimates

## Dependencies

- **TASK-005**: Complexity evaluation logic in `/task-create`
- **TASK-006**: Design-first workflow flags in `/task-work`
- Access to feature requirements and acceptance criteria
- Task ID generation logic for sub-tasks

## Related Commands

This enhancement affects the workflow:
1. `/feature-create` - Creates features with requirements
2. `/feature-generate-tasks` - **THIS TASK** - Generates complexity-aware tasks
3. `/task-work` - Implements tasks with complexity checkpoints
4. `/task-complete` - Finalizes tasks

## Notes

- This is a **high-priority enhancement** because it directly affects developer productivity
- Consider adding telemetry to track breakdown acceptance rates and actual vs estimated complexity
- May want to add a `--skip-complexity-check` flag for advanced users who want to bypass automatic breakdown
- Consider exposing complexity evaluation as a standalone command: `/task-evaluate-complexity TASK-XXX`

## Test Execution Log

_Automatically populated by /task-work_
