# Common Quality Thresholds

**Purpose**: Shared quality threshold definitions used across all agentecflow workflows to maintain consistency and DRY principles.

**Referenced By**:
- Task complexity evaluation workflows
- UX design integration workflows
- Testing and quality gate enforcement
- Architectural review processes

---

## Complexity Scoring Thresholds

### Task Complexity Scale (0-10)

| Score Range | Level | Description | Review Mode | Recommended Action |
|-------------|-------|-------------|-------------|-------------------|
| **1-3** | 🟢 Simple | Single developer, <4 hours, clear approach | AUTO_PROCEED | Implement immediately |
| **4-6** | 🟡 Medium | Single developer, 4-8 hours, may need research | QUICK_OPTIONAL | Quick checkpoint (10s timeout) |
| **7-8** | 🟡 Complex | Consider breakdown, >8 hours, multiple sub-systems | FULL_REQUIRED | Mandatory human review |
| **9-10** | 🔴 Very Complex | MUST break down, unclear scope, high risk | FULL_REQUIRED | Split into subtasks |

### Complexity Factor Scoring

**File Complexity** (0-3 points):
- 1-2 files: 1 point
- 3-5 files: 2 points
- 6+ files: 3 points

**Pattern Familiarity** (0-2 points):
- All familiar patterns: 0 points
- Mixed familiar/unfamiliar: 1 point
- New/unfamiliar patterns: 2 points

**Risk Assessment** (0-3 points):
- Low risk: 0 points
- Medium risk (external dependencies, moderate changes): 1 point
- High risk (security, breaking changes, data migration): 3 points

**External Dependencies** (0-2 points):
- 0 dependencies: 0 points
- 1-2 dependencies: 1 point
- 3+ dependencies: 2 points

---

## Quality Gate Thresholds

### Test Coverage Requirements

| Metric | Threshold | Action if Below Threshold |
|--------|-----------|--------------------------|
| **Code Compilation** | 100% (MANDATORY) | BLOCKED - Fix compilation errors |
| **Tests Passing** | 100% (MANDATORY) | BLOCKED - Fix failing tests |
| **Line Coverage** | ≥80% | Generate additional tests |
| **Branch Coverage** | ≥75% | Generate additional tests |
| **Test Execution Time** | <30s | Warning only (suggest optimization) |

### UX Design Integration

| Quality Gate | Threshold | Action if Below Threshold |
|--------------|-----------|--------------------------|
| **Visual Fidelity** | >95% similarity | Generate diff images, provide remediation |
| **Constraint Violations** | 0 (zero tolerance) | Block generation, display violations |
| **Compilation Success** | 100% | Block testing, fix compilation errors |
| **Component Props** | Only for visible elements | Validation failure, block generation |

---

## Architectural Review Scoring

### Overall Score (0-100 scale)

| Score Range | Status | Action |
|-------------|--------|--------|
| **≥80** | ✅ Auto-approve | Proceed to implementation |
| **60-79** | ⚠️ Approve with recommendations | Proceed with warnings |
| **<60** | ❌ Reject | Revise design, loop to Phase 2 |

### Principle-Specific Scoring

Each architectural principle (SOLID, DRY, YAGNI) is scored individually on 0-100 scale:

**SOLID Principles** (0-100):
- Single Responsibility
- Open/Closed
- Liskov Substitution
- Interface Segregation
- Dependency Inversion

**DRY Principle** (0-100):
- No code duplication
- Abstraction appropriateness
- Reusability

**YAGNI Principle** (0-100):
- No premature optimization
- No unnecessary complexity
- Implementation only what's needed

---

## Breakdown Thresholds

### Task Breakdown Strategies

| Complexity | Strategy | Max Subtasks | Estimated Time |
|-----------|----------|--------------|----------------|
| **1-3** | No breakdown | 1 (original task) | <4 hours |
| **4-6** | Logical breakdown | 3-4 subtasks | 4-8 hours per subtask |
| **7-8** | File-based breakdown | 4-6 subtasks | 8-16 hours total |
| **9-10** | Phase-based breakdown | 5-7 subtasks | 16+ hours total |

### Breakdown Decision Factors

| Factor | Threshold | Breakdown Triggered |
|--------|-----------|---------------------|
| **File Count** | ≥6 files | Yes |
| **Pattern Complexity** | New/unfamiliar patterns | Yes |
| **Risk Level** | High risk (security, breaking changes) | Yes |
| **Dependencies** | ≥3 external dependencies | Yes |
| **Estimated Duration** | >8 hours | Yes |

---

## Test Enforcement Thresholds

### Fix Loop Limits

| Attempt | Max Attempts | Action if Exceeded |
|---------|-------------|-------------------|
| **Initial Test Run** | N/A | Proceed to Phase 4.5 if failures |
| **Fix Attempts** | 3 attempts | Move to BLOCKED state |
| **Total Time** | 30 minutes | Warning, suggest manual review |

### Test Success Criteria

**ABSOLUTE REQUIREMENTS** (zero tolerance):
- ✅ Code compiles with ZERO errors
- ✅ ALL tests pass (100% pass rate)
- ✅ NO tests skipped, ignored, or commented out
- ✅ Coverage thresholds met (≥80% line, ≥75% branch)

---

## Design-First Workflow Thresholds

### Checkpoint Triggers

| Complexity Score | Workflow Mode | Checkpoint Requirement |
|------------------|---------------|----------------------|
| **1-3** | Standard (default) | AUTO_PROCEED - No checkpoint |
| **4-6** | Standard (default) | QUICK_OPTIONAL - 30s timeout |
| **7-10** | Design-first recommended | FULL_REQUIRED - Mandatory review |

### Force-Review Triggers

Tasks with ANY of these triggers require FULL_REQUIRED review mode regardless of complexity score:

- Security keywords (auth, password, encryption, token, etc.)
- Schema changes (database migrations, model changes)
- Breaking changes (public API modifications)
- User flag (`--review` command-line option)
- Hotfix or production deployment tags

---

## Visual Regression Thresholds

### Figma → React

| Quality Gate | Threshold | Validation Method |
|--------------|-----------|------------------|
| **Visual Similarity** | >95% | Playwright screenshot comparison |
| **Pixel Tolerance** | ±2px | Layout comparison |
| **Color Accuracy** | Exact match | Design token verification |

### Zeplin → MAUI

| Quality Gate | Threshold | Validation Method |
|--------------|-----------|------------------|
| **XAML Correctness** | 100% | Structure validation |
| **Property Values** | Exact match | Property comparison |
| **Platform Rendering** | All platforms | iOS, Android, Windows, macOS |

---

## Usage Guidelines

### When to Reference These Thresholds

**DO reference this file when**:
- Implementing complexity evaluation
- Creating quality gate validation
- Building architectural review systems
- Developing test enforcement logic

**DO NOT duplicate threshold values**:
- Always link to this file for threshold definitions
- Update thresholds centrally in this file only
- Use inline references: "See [common-thresholds.md](../shared/common-thresholds.md) for scoring details"

### Threshold Customization

Projects can override these thresholds in `.claude/settings.json`:

```json
{
  "quality_thresholds": {
    "complexity_breakdown_threshold": 7,
    "coverage_line_threshold": 80,
    "coverage_branch_threshold": 75,
    "architectural_review_auto_approve": 80,
    "visual_similarity_threshold": 95,
    "max_fix_attempts": 3
  }
}
```

---

**Last Updated**: 2025-10-12
**Version**: 1.0.0
**Maintained By**: AI Engineer Team
