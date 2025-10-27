# Agentecflow Terminology Glossary
## Canonical Definitions for Consistent Documentation

**Created**: October 25, 2025
**Purpose**: Ensure consistent terminology across all documentation
**Source**: Extracted from command specifications and core documentation
**Status**: Complete

---

## Core Workflow Terms

### Agentecflow Lite
**Definition**: Lightweight AI-augmented development workflow embedded in `/task-work` command that provides 80% of enterprise SDD benefits with 20% of the ceremony overhead.

**Usage**: Use when referring to the embedded workflow (not the full Epic→Feature→Task hierarchy).

**Related Terms**: Full Agentecflow, Enterprise SDD

**Example**:
```markdown
Agentecflow Lite is the sweet spot between plain AI coding and full specification-driven development.
```

---

### Full Agentecflow
**Definition**: Complete specification-driven development system including Epic→Feature→Task hierarchy, EARS requirements, BDD/Gherkin scenarios, and PM tool integration.

**Usage**: Use when referring to the complete enterprise system with all features.

**Related Terms**: Agentecflow Lite, Enterprise Features

**Example**:
```markdown
Upgrade to Full Agentecflow when team size exceeds 5 developers or PM tool integration is required.
```

---

## Phase Terminology

### Phase 1: Requirements Analysis
**Definition**: Load task context, requirements, and acceptance criteria for implementation planning.

**Duration**: 5-10 seconds

**Inputs**: Task file (markdown), linked requirements, BDD scenarios

**Outputs**: Requirements summary, dependency list

**Example**:
```markdown
Phase 1 analyzes task requirements and identifies dependencies before planning begins.
```

---

### Phase 2: Implementation Planning
**Definition**: Generate detailed implementation plan including files to create/modify, patterns, dependencies, risks, and estimated duration.

**Duration**: 15-30 seconds

**Outputs**: Markdown implementation plan saved to `.claude/task-plans/{task_id}-implementation-plan.md`

**Related**: Phase 2.5B (Architectural Review), Phase 2.7 (Complexity Evaluation), Phase 2.8 (Checkpoint)

**Example**:
```markdown
Phase 2 creates a human-readable Markdown plan that serves as the implementation guide.
```

---

### Phase 2.5B: Architectural Review
**Definition**: Evaluate implementation plan for SOLID, DRY, and YAGNI compliance **before code is written**.

**Scoring**: 0-100 scale
- 80-100: Auto-approved (excellent design)
- 60-79: Approved with recommendations (good design)
- 0-59: Rejected (major flaws, redesign required)

**Purpose**: Catch design issues early, prevent over-engineering, save 40-50% time

**Example**:
```yaml
architectural_review:
  score: 85
  status: approved
  recommendations:
    - "Consider caching strategy for performance"
```

---

### Phase 2.7: Complexity Evaluation
**Definition**: Calculate task complexity (0-10 scale) and determine appropriate review mode.

**Scoring Factors**:
- File complexity (1-3 points)
- Pattern familiarity (0-2 points)
- Risk assessment (0-3 points)
- External dependencies (0-2 points)

**Review Modes**:
- **1-3 (Simple)**: AUTO_PROCEED - no checkpoint
- **4-6 (Medium)**: QUICK_OPTIONAL - 30s timeout, auto-proceed if no input
- **7-10 (Complex)**: FULL_REQUIRED - mandatory human checkpoint

**Example**:
```yaml
complexity_evaluation:
  score: 5
  level: medium
  review_mode: QUICK_OPTIONAL
```

---

### Phase 2.8: Enhanced Checkpoint
**Definition**: Interactive plan review with modification options when complexity or risk requires human approval.

**Triggered By**:
- Complexity ≥ 7/10
- Architectural review < 80/100
- Security-sensitive changes
- `--review` flag

**Options**:
- **[A] Approve**: Proceed to implementation
- **[M] Modify**: Interactive plan editing
- **[S] Simplify**: Break down into smaller tasks
- **[R] Reject**: Cancel and return to backlog
- **[P] Postpone**: Save plan for later (design_approved state)

**Example**:
```markdown
Phase 2.8 provides interactive plan modification for complex tasks requiring human oversight.
```

---

### Phase 3: Implementation
**Definition**: Execute implementation according to approved plan.

**Duration**: Variable (depends on task complexity)

**Inputs**: Implementation plan (Markdown), task requirements

**Outputs**: Source code files, modified files, new files

**Example**:
```markdown
Phase 3 generates code following the implementation plan created in Phase 2.
```

---

### Phase 4: Testing
**Definition**: Verify code compiles, run test suite, collect coverage metrics.

**Quality Gates**:
- Compilation: 100% success required
- Tests: 100% pass rate required
- Line coverage: ≥80% required
- Branch coverage: ≥75% required

**Example**:
```yaml
test_results:
  status: passed
  total_tests: 25
  passed: 25
  coverage_line: 92
  coverage_branch: 87
```

---

### Phase 4.5: Test Enforcement Loop
**Definition**: Automatically fix failing tests with up to 3 retry attempts. Zero-tolerance for failing tests.

**Process**:
1. Compilation check (must pass before testing)
2. Run tests
3. If failures detected:
   a. Analyze failure patterns
   b. Generate fixes
   c. Apply fixes
   d. Re-run tests
   e. Repeat up to 3 attempts
4. If still failing → Task moves to BLOCKED state

**Impact**: 100% test pass rate enforced across all completed tasks

**Example**:
```markdown
Phase 4.5 ensures tasks cannot complete with failing tests - zero-tolerance enforcement.
```

---

### Phase 5: Code Review
**Definition**: Check code quality for SOLID/DRY principles, verify test coverage, generate recommendations.

**Scoring**: 0-10 scale
- **9-10 (A/A+)**: Excellent quality
- **7-8 (B/B+)**: Good quality
- **5-6 (C)**: Acceptable with improvements
- **<5 (D/F)**: Poor quality, requires significant rework

**Example**:
```yaml
code_review:
  score: 9.2
  grade: A
  status: approved_for_production
  blockers: 0
```

---

### Phase 5.5: Plan Audit
**Definition**: Compare implementation against original plan to detect scope creep and variances.

**Audit Checks**:
- **File Count Match**: 100% of planned files created
- **LOC Variance**: Actual vs estimated (±20% acceptable)
- **Duration Variance**: Actual vs estimated (±30% acceptable)
- **Scope Creep**: No unplanned features added
- **Implementation Completeness**: All planned work completed

**Example**:
```yaml
plan_audit:
  file_match: 100%
  implementation_complete: true
  scope_creep: none_detected
  loc_variance: "+14.8%"
  duration_variance: "+15%"
  verdict: approved
```

---

## Task States

### BACKLOG
**Definition**: Task created but not started. Waiting in queue for implementation.

**Transitions**:
- → IN_PROGRESS (when `/task-work` starts)
- → DESIGN_APPROVED (when `/task-work --design-only` completes)

---

### DESIGN_APPROVED
**Definition**: Design phase complete (Phases 1-2.8), implementation plan approved, ready for implementation.

**Transitions**:
- → IN_PROGRESS (when `/task-work --implement-only` starts)

**Usage**: Used in design-first workflow for complex tasks requiring separate design approval.

---

### IN_PROGRESS
**Definition**: Active development in progress.

**Transitions**:
- → IN_REVIEW (when all quality gates pass)
- → BLOCKED (when quality gates fail)

---

### IN_REVIEW
**Definition**: All quality gates passed, ready for human review or deployment.

**Quality Gates Met**:
- ✅ Compilation: 100%
- ✅ Tests: 100% pass rate
- ✅ Coverage: ≥80% line, ≥75% branch
- ✅ Code quality: ≥7/10
- ✅ Plan audit: No scope creep

**Transitions**:
- → COMPLETED (when `/task-complete` runs)
- → BLOCKED (if issues found during review)

---

### BLOCKED
**Definition**: Quality gates failed or issues found. Requires fixes before continuing.

**Common Causes**:
- Failing tests (Phase 4/4.5)
- Compilation errors (Phase 4)
- Coverage below threshold (Phase 4)
- Major code quality issues (Phase 5)

**Resolution**: Fix issues, then run `/task-work --fix-only`

---

### COMPLETED
**Definition**: Task finished, archived, and moved to `tasks/completed/` directory.

**Files Preserved**:
- Task markdown file with complete metadata
- Implementation plan
- Test results
- Code review
- Plan audit results

---

## Development Modes

### Standard Mode (Default)
**Definition**: Traditional development - implementation and tests created together.

**Usage**: Default when no `--mode` flag specified

**Process**:
1. Generate implementation
2. Create comprehensive test suite
3. Run tests and verify quality
4. Update task state

**Example**:
```bash
/task-work TASK-042
# Uses standard mode by default
```

---

### TDD Mode (Test-Driven Development)
**Definition**: Follow Red→Green→Refactor cycle - tests written before implementation.

**Usage**: Use `--mode=tdd` flag

**Process**:
1. **RED**: Generate failing tests based on requirements
2. **GREEN**: Write minimal code to pass tests
3. **REFACTOR**: Improve code while keeping tests green
4. Verify coverage and quality gates

**Example**:
```bash
/task-work TASK-042 --mode=tdd
```

---

### BDD Mode (Behavior-Driven Development)
**Definition**: Start from user scenarios (Gherkin) and generate step definitions.

**Usage**: Use `--mode=bdd` flag

**Process**:
1. Load linked BDD scenarios (Gherkin)
2. Generate step definitions
3. Implement features to satisfy scenarios
4. Add unit tests for completeness
5. Verify all scenarios pass

**Example**:
```bash
/task-work TASK-042 --mode=bdd
```

---

## Quality Gates

### Quality Gate
**Definition**: Automated check that enforces quality standards before task can progress.

**Types**:
1. **Compilation Gate**: Code must compile (100%)
2. **Test Gate**: Tests must pass (100%)
3. **Coverage Gate**: Line ≥80%, Branch ≥75%
4. **Code Quality Gate**: Score ≥7/10
5. **Architectural Gate**: Score ≥60/100
6. **Plan Audit Gate**: No scope creep detected

**Usage**: Always use singular "quality gate" for single check, plural "quality gates" for multiple checks.

**Example**:
```markdown
All quality gates passed - task ready for review.
```

---

## Workflow Features

### Design-First Workflow
**Definition**: Two-phase execution where design (Phases 1-2.8) and implementation (Phases 3-5) are separated.

**Flags**:
- `--design-only`: Execute design phases only
- `--implement-only`: Execute implementation phases only

**Usage**: Complex tasks (complexity ≥7), high-risk changes, multi-day tasks, team collaboration

**Example**:
```bash
# Day 1: Design
/task-work TASK-042 --design-only

# Day 2: Implement
/task-work TASK-042 --implement-only
```

---

### Iterative Refinement
**Definition**: Lightweight iterative improvement using `/task-refine` command without full re-work.

**Use For**:
- Minor code improvements
- Fixing linting issues
- Renaming for clarity
- Adjusting formatting

**Do NOT Use For**:
- Adding new features
- Changing architecture
- Major refactoring
- Breaking changes

**Example**:
```bash
/task-refine TASK-042 "Improve variable naming and add inline comments"
```

---

### Markdown Implementation Plans
**Definition**: Human-readable implementation plans saved as `.md` files instead of JSON.

**Location**: `.claude/task-plans/{task_id}-implementation-plan.md`

**Benefits**:
- Human-reviewable (any text editor)
- Git-friendly (meaningful diffs)
- Searchable (grep, ripgrep, IDE search)
- Editable (can be modified before `--implement-only`)

**Example**:
```markdown
# Implementation Plan: TASK-042

**Task**: Implement JWT authentication endpoint
**Complexity**: 5/10 (Medium)
**Estimated Duration**: 4 hours

## Files to Create
...
```

---

### Complexity-Based Routing
**Definition**: Automatic complexity evaluation and routing to appropriate review mode.

**Review Modes**:
- **AUTO_PROCEED**: Simple tasks (1-3), no checkpoint
- **QUICK_OPTIONAL**: Medium tasks (4-6), 30s timeout, auto-proceed if no input
- **FULL_REQUIRED**: Complex tasks (7-10), mandatory human checkpoint

**Impact**: 34% of tasks auto-proceed (zero ceremony overhead), 15% get proper oversight

---

## Integration Terms

### Conductor Integration
**Definition**: Compatibility with Conductor.build for parallel development using git worktrees.

**Status**: Production-ready (TASK-031 resolved state persistence)

**Features**:
- State persistence across worktrees (100% reliable)
- Auto-commit functionality (git_state_helper.py)
- Full path resolution (no workarounds needed)

**Example**:
```bash
# Conductor worktree - works seamlessly
/task-work TASK-042
```

---

### PM Tool Integration
**Definition**: Synchronization with external project management tools (Jira, Linear, GitHub, Azure DevOps).

**Availability**:
- **Agentecflow Lite**: Not required (optional via Full Agentecflow)
- **Full Agentecflow**: Full bidirectional sync available

**Commands**: `/epic-sync`, `/feature-sync`, `/task-sync`

---

## Metric Terms

### Time Savings
**Definition**: Quantified reduction in task duration compared to manual estimates.

**Measurement**: `(Estimated Duration - Actual Duration) / Estimated Duration × 100%`

**Example**: TASK-031 saved 5.25 hours (87.5% faster than 6-hour estimate)

---

### Coverage
**Definition**: Percentage of code lines/branches executed by tests.

**Types**:
- **Line Coverage**: Percentage of code lines executed
- **Branch Coverage**: Percentage of conditional branches tested

**Thresholds**:
- Line coverage: ≥80% required
- Branch coverage: ≥75% required

**Example**:
```yaml
coverage_line: 92
coverage_branch: 87
```

---

### ROI (Return on Investment)
**Definition**: Financial or time value gained relative to investment.

**Calculation**: `(Benefit - Cost) / Cost × 100%`

**Example**: TASK-031 ROI = $516.67 net savings / $8.33 setup = 6,200%

---

## Anti-Pattern Terms

### Spec-Kit Maximalism
**Definition**: Anti-pattern of excessive specification ceremony that creates "more overhead than value" (ThoughtWorks finding).

**Characteristics**:
- Mandatory EARS notation
- Required BDD/Gherkin upfront
- Forced epic/feature hierarchy
- Heavy approval processes
- 50-100% ceremony overhead

**Usage**: Use when contrasting Agentecflow Lite with heavyweight approaches.

---

### Scope Creep
**Definition**: Unplanned features or functionality added during implementation that weren't in the original plan.

**Detection**: Phase 5.5 (Plan Audit) uses pattern matching and AST analysis

**Enforcement**: Zero-tolerance in design-to-code workflows (Figma, Zeplin)

**Example**:
```yaml
plan_audit:
  scope_creep: "Added error handling not in plan"
  verdict: requires_review
```

---

### YAGNI (You Aren't Gonna Need It)
**Definition**: Principle of not adding functionality until it's actually needed.

**Enforcement**: Phase 2.5B (Architectural Review) validates YAGNI compliance

**Example**: TASK-031 - Architectural review prevented complex facade pattern, recommended simple utility functions (90% code reduction)

---

## Research Terms

### Hubbard's 6-Step Workflow
**Definition**: Proven AI coding workflow from Jordan Hubbard (Nvidia) after 6 months production use.

**Steps**:
1. Plan (write as .md file)
2. Execute (write code)
3. Write tests
4. Run tests
5. Re-execute as necessary until tests pass
6. Audit - check code against Plan.md

**Alignment**: Agentecflow Lite implements all 6 steps (Phase mapping documented)

---

### ThoughtWorks Research
**Definition**: Real-world testing by ThoughtWorks team (coordinated by Birgitta Böckeler) comparing elaborate SDD tools to plain AI coding.

**Finding**: "I could have implemented the feature with 'plain' AI-assisted coding in the same time it took to create all these markdown files."

**Impact**: Validates Agentecflow Lite approach (lightweight specs, not elaborate tools)

---

### Martin Fowler SDD Principles
**Definition**: Four core principles for Specification-Driven Development from Martin Fowler's research.

**Principles**:
1. Specifications should be executable
2. Keep specifications close to code
3. Specifications should be lightweight
4. Iterate specifications with implementation

**Alignment**: Agentecflow Lite complies with all 4 principles

---

## Usage Guidelines

### Consistency Rules

**1. Phase References**:
- ✅ **CORRECT**: "Phase 2.5B (Architectural Review)"
- ❌ **INCORRECT**: "Phase 2.5b", "Architectural Review Phase", "Phase 2.5-B"

**2. Quality Gates**:
- ✅ **CORRECT**: "quality gate", "quality gates" (lowercase unless start of sentence)
- ❌ **INCORRECT**: "Quality Gate", "QA gate", "quality-gate"

**3. Task States**:
- ✅ **CORRECT**: "IN_PROGRESS", "in_progress" (all caps in YAML, lowercase in prose)
- ❌ **INCORRECT**: "In Progress", "in-progress", "InProgress"

**4. Development Modes**:
- ✅ **CORRECT**: "TDD mode", "BDD mode", "standard mode"
- ❌ **INCORRECT**: "TDD-mode", "tdd mode", "Standard Mode"

**5. Commands**:
- ✅ **CORRECT**: "`/task-work`", "`/task-refine`" (always with backticks and slash)
- ❌ **INCORRECT**: "task-work", "/task work", "task_work"

**6. Product Names**:
- ✅ **CORRECT**: "Agentecflow Lite", "Full Agentecflow"
- ❌ **INCORRECT**: "AgentecFlow Lite", "Agentic Flow Lite", "agentecflow-lite"

---

## Validation Checklist

When writing or reviewing documentation:

- [ ] Phase names use consistent format (Phase X.YZ: Name)
- [ ] Quality gate terminology is lowercase
- [ ] Task states use canonical names (BACKLOG, IN_PROGRESS, etc.)
- [ ] Command references use backticks with slash (`/command`)
- [ ] Product names use proper capitalization
- [ ] Development mode names are consistent
- [ ] Metric terms are properly defined
- [ ] No anti-pattern terms used inappropriately
- [ ] Research citations are accurate
- [ ] Cross-references use correct section names

---

**Document Version**: 1.0
**Last Updated**: October 25, 2025
**Next Review**: As needed when new terms introduced
**Status**: Complete - Ready for validation
