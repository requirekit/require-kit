# Task Complexity Guide

## Overview

Task complexity evaluation prevents oversized tasks and improves predictability by scoring tasks on a 0-10 scale. The system evaluates complexity both during task creation (upfront) and during implementation planning (Phase 2.7).

## Quick Reference

### Complexity Scale
| Score | Level | Characteristics | Action |
|-------|-------|-----------------|--------|
| 1-3 | Simple | Single developer, <4h, clear approach | Implement as-is |
| 4-6 | Medium | Single developer, 4-8h, may need research | Consider breakdown |
| 7-8 | Complex | >8h, multiple sub-systems | Recommend breakdown |
| 9-10 | Very Complex | Unclear scope, high risk | **MUST** break down |

### Scoring Factors (0-10 Total)

**File Complexity (0-3 points)**
- 1-2 files: 1 point
- 3-5 files: 2 points
- 6+ files: 3 points

**Pattern Familiarity (0-2 points)**
- All familiar patterns: 0 points
- Mixed familiar/unfamiliar: 1 point
- New/complex patterns: 2 points

**Risk Assessment (0-3 points)**
- Low risk (UI updates, simple logic): 0 points
- Medium risk (external APIs, moderate changes): 1 point
- High risk (security, schema changes, breaking changes): 3 points

**External Dependencies (0-2 points)**
- 0 dependencies: 0 points
- 1-2 dependencies: 1 point
- 3+ dependencies: 2 points

### Review Modes by Complexity
| Complexity | Review Mode | Phase 2.8 Checkpoint |
|------------|-------------|---------------------|
| 1-3 | AUTO_PROCEED | No (auto-approve) |
| 4-6 | QUICK_OPTIONAL | Optional (10s timeout) |
| 7-10 | FULL_REQUIRED | Mandatory (blocks until approved) |

## Decision Guide

### Breakdown Thresholds

**Default Threshold**: 7/10 (configurable)

**When to Break Down**:
- Complexity ≥ 7 (automatic recommendation)
- Multiple architectural layers (UI + API + Database)
- New patterns unfamiliar to team
- High-risk changes requiring staged rollout
- Estimated effort >8 hours

**When to Keep As-Is**:
- Complexity 1-6 (within acceptable range)
- Straightforward implementation with clear approach
- All patterns familiar to team
- Low risk changes
- Team has relevant expertise

### Breakdown Strategies

**Vertical Split** (By User Stories)
```
Original: TASK-042 - User authentication system (9/10)
Breakdown:
├── TASK-042.1: Login flow (5/10)
├── TASK-042.2: Registration flow (4/10)
├── TASK-042.3: Password reset flow (5/10)
└── TASK-042.4: Session management (6/10)
```

**Horizontal Split** (By Architectural Layers)
```
Original: TASK-050 - Product catalog (8/10)
Breakdown:
├── TASK-050.1: Database models (4/10)
├── TASK-050.2: API endpoints (5/10)
├── TASK-050.3: UI components (5/10)
└── TASK-050.4: Integration tests (4/10)
```

**Technical Split** (By Technical Concerns)
```
Original: TASK-060 - Payment processing (9/10)
Breakdown:
├── TASK-060.1: Payment gateway integration (6/10)
├── TASK-060.2: Payment validation logic (5/10)
├── TASK-060.3: Transaction error handling (5/10)
└── TASK-060.4: Payment webhooks (6/10)
```

**Temporal Split** (By Implementation Phases)
```
Original: TASK-070 - Event sourcing (10/10)
Breakdown:
├── TASK-070.1: Phase 1 - Event store setup (5/10)
├── TASK-070.2: Phase 2 - Event handlers (6/10)
├── TASK-070.3: Phase 3 - CQRS implementation (6/10)
├── TASK-070.4: Phase 4 - Event replay (5/10)
└── TASK-070.5: Phase 5 - Testing suite (5/10)
```

## Examples

### Example 1: Simple Task (Complexity 2/10)
```
Task: Fix typo in error message
Files: 1 file (AuthService.py)
Patterns: None (simple text change)
Risk: Low (cosmetic change)
Dependencies: 0

Score Calculation:
├── File complexity: 1/3 (1 file)
├── Pattern familiarity: 0/2 (no patterns)
├── Risk level: 0/3 (low risk)
└── Dependencies: 0/2 (no dependencies)
Total: 1/10 (Simple)

Decision: Implement as-is (--micro flag suggested)
```

### Example 2: Medium Task (Complexity 5/10)
```
Task: Implement user profile API endpoint
Files: 4 files (model, repository, service, controller)
Patterns: Repository, DTO mapping
Risk: Medium (external database dependency)
Dependencies: 1 (database ORM)

Score Calculation:
├── File complexity: 2/3 (3-5 files)
├── Pattern familiarity: 1/2 (familiar patterns)
├── Risk level: 1/3 (medium risk)
└── Dependencies: 1/2 (1-2 dependencies)
Total: 5/10 (Medium)

Decision: Implement as-is with optional checkpoint
```

### Example 3: Complex Task (Complexity 8/10)
```
Task: Implement OAuth2 authentication
Files: 12 files (tokens, grants, clients, validators)
Patterns: OAuth2 flow, JWT, Strategy pattern
Risk: High (security-critical)
Dependencies: 3 (oauth library, jwt, redis)

Score Calculation:
├── File complexity: 3/3 (6+ files)
├── Pattern familiarity: 2/2 (new OAuth2 patterns)
├── Risk level: 3/3 (high security risk)
└── Dependencies: 2/2 (3+ dependencies)
Total: 10/10 (Very Complex) ← Exceeds threshold!

Recommendation: MUST break down into subtasks
Suggested breakdown:
├── TASK-XXX.1: OAuth2 authorization flow (6/10)
├── TASK-XXX.2: Token management (5/10)
├── TASK-XXX.3: Client authentication (6/10)
└── TASK-XXX.4: Security tests (5/10)
```

### Example 4: Borderline Task (Complexity 7/10)
```
Task: Add pagination to products API
Files: 6 files (API, service, repository, tests)
Patterns: Repository, pagination strategy
Risk: Medium (performance impact)
Dependencies: 1 (pagination library)

Score Calculation:
├── File complexity: 3/3 (6+ files)
├── Pattern familiarity: 1/2 (familiar patterns)
├── Risk level: 1/3 (medium risk)
└── Dependencies: 1/2 (1-2 dependencies)
Total: 6/10 (Medium-High)

Decision: Borderline - user choice at Phase 2.8
Options:
1. Implement as-is (with mandatory checkpoint)
2. Break down into smaller tasks
```

## See Also

**Full Documentation**:
- Task creation: `installer/global/commands/task-create.md` (Phase 2.5)
- Feature generation: `installer/global/commands/feature-generate-tasks.md`
- Complexity workflow: `docs/guides/complexity-management-workflow.md`

**Related Cards**:
- [task-work-cheat-sheet.md](task-work-cheat-sheet.md) - Phase 2.7 complexity evaluation
- [design-first-workflow-card.md](design-first-workflow-card.md) - Complex task patterns
- [quality-gates-card.md](quality-gates-card.md) - Quality requirements
