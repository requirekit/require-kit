# TASK-006: Revised Implementation Plan (Simplified)

## Executive Summary

**Original Complexity:**
- 12 new files (~1,740 LOC)
- 4 design patterns simultaneously
- Repository pattern for JSON I/O
- Versioning system
- 14 total files affected

**Revised Complexity:**
- 5 files total (3 modified, 2 new)
- ~450-500 LOC
- Functional approach with clean architecture
- Simple JSON persistence
- Clear upgrade path to patterns

**Architectural Review Score:** 68/100 → Target 85+/100

---

## Core Design Philosophy

### YAGNI-First Approach
1. **Start Functional**: Use functions and simple modules initially
2. **Add Patterns Incrementally**: Introduce patterns when complexity justifies them
3. **Maintain Extensibility**: Design for future pattern migration
4. **Keep It Simple**: Solve the immediate problem elegantly

### Key Simplifications
1. **No Strategy Pattern** → Conditional routing with clear functions
2. **No Repository Pattern** → Simple save/load utilities
3. **No Versioning** → Direct JSON persistence (add later if needed)
4. **No Multiple Coordinators** → Single coordinator with mode parameter

---

## Simplified Architecture

### File Structure (5 files total)

```
installer/global/agents/
├── task-manager.md                    # Modified: Add phase 2.5 support
└── architectural-reviewer.md          # Modified: Clarify integration

src/utils/
├── phase-execution.ts                 # NEW: Core phase execution logic
├── plan-persistence.ts                # NEW: Simple JSON save/load
└── task-manager.ts                    # Modified: Integration point
```

### Estimated LOC Breakdown

| File | Type | LOC | Purpose |
|------|------|-----|---------|
| phase-execution.ts | New | ~250 | Phase execution with routing |
| plan-persistence.ts | New | ~80 | JSON save/load utilities |
| task-manager.ts | Modified | +120 | Integration of new features |
| task-manager.md | Modified | +30 | Documentation updates |
| architectural-reviewer.md | Modified | +20 | Clarify workflow integration |
| **TOTAL** | | **~500** | |

---

## Implementation Details

### 1. Phase Execution Module (`phase-execution.ts`)

**Purpose:** Centralized phase execution logic with mode support

```typescript
// Core types
interface PhaseExecutionOptions {
  mode: 'standard' | 'design-only' | 'implement-only';
  taskId: string;
  taskPath: string;
  withContext?: boolean;
}

interface PhaseExecutionResult {
  success: boolean;
  phasesExecuted: string[];
  planPath?: string;
  errors?: string[];
}

// Main execution function
async function executePhases(options: PhaseExecutionOptions): Promise<PhaseExecutionResult> {
  const { mode, taskId, taskPath } = options;

  // Route based on mode
  switch (mode) {
    case 'design-only':
      return executeDesignPhases(taskId, taskPath, options);
    case 'implement-only':
      return executeImplementationPhases(taskId, taskPath, options);
    default:
      return executeStandardPhases(taskId, taskPath, options);
  }
}

// Design-only phases (1 → 2 → 2.5 → 2.6)
async function executeDesignPhases(
  taskId: string,
  taskPath: string,
  options: PhaseExecutionOptions
): Promise<PhaseExecutionResult> {
  const result: PhaseExecutionResult = {
    success: true,
    phasesExecuted: []
  };

  try {
    // Phase 1: Requirements Analysis
    await executePhase1(taskId, taskPath, options);
    result.phasesExecuted.push('Phase 1: Requirements Analysis');

    // Phase 2: Implementation Planning
    const plan = await executePhase2(taskId, taskPath, options);
    result.phasesExecuted.push('Phase 2: Implementation Planning');

    // Phase 2.5: Architectural Review
    const reviewResult = await executePhase25(taskId, plan, options);
    result.phasesExecuted.push('Phase 2.5: Architectural Review');

    if (reviewResult.requiresHumanCheckpoint) {
      // Phase 2.6: Human Checkpoint
      const approved = await executePhase26(taskId, reviewResult, options);
      result.phasesExecuted.push('Phase 2.6: Human Checkpoint');

      if (!approved) {
        result.success = false;
        result.errors = ['Design rejected at human checkpoint'];
        return result;
      }
    }

    // Save plan and update state
    const planPath = await savePlan(taskId, plan, reviewResult);
    result.planPath = planPath;
    await updateTaskState(taskPath, 'design_approved');

    return result;
  } catch (error) {
    result.success = false;
    result.errors = [error.message];
    return result;
  }
}

// Implementation-only phases (3 → 4 → 4.5 → 5)
async function executeImplementationPhases(
  taskId: string,
  taskPath: string,
  options: PhaseExecutionOptions
): Promise<PhaseExecutionResult> {
  const result: PhaseExecutionResult = {
    success: true,
    phasesExecuted: []
  };

  try {
    // Validate state
    await validateStateForImplementation(taskPath);

    // Load approved plan
    const plan = await loadPlan(taskId);
    if (!plan) {
      throw new Error('No approved plan found. Run with --design-only first.');
    }

    // Phase 3: Implementation
    await executePhase3(taskId, plan, options);
    result.phasesExecuted.push('Phase 3: Implementation');

    // Phase 4: Testing
    const testResult = await executePhase4(taskId, options);
    result.phasesExecuted.push('Phase 4: Testing');

    // Phase 4.5: Fix Loop (if tests fail)
    if (!testResult.allPassed) {
      const fixResult = await executePhase45(taskId, testResult, options);
      result.phasesExecuted.push('Phase 4.5: Fix Loop');

      if (!fixResult.success) {
        result.success = false;
        result.errors = ['Tests still failing after fix attempts'];
        return result;
      }
    }

    // Phase 5: Code Review
    await executePhase5(taskId, options);
    result.phasesExecuted.push('Phase 5: Code Review');

    return result;
  } catch (error) {
    result.success = false;
    result.errors = [error.message];
    return result;
  }
}

// Standard phases (1 → 2 → 2.5 → 2.6? → 3 → 4 → 4.5? → 5)
async function executeStandardPhases(
  taskId: string,
  taskPath: string,
  options: PhaseExecutionOptions
): Promise<PhaseExecutionResult> {
  // Combines both design and implementation phases
  const designResult = await executeDesignPhases(taskId, taskPath, options);
  if (!designResult.success) {
    return designResult;
  }

  const implResult = await executeImplementationPhases(taskId, taskPath, options);
  return {
    success: implResult.success,
    phasesExecuted: [...designResult.phasesExecuted, ...implResult.phasesExecuted],
    planPath: designResult.planPath,
    errors: implResult.errors
  };
}

// Helper: Validate state for implement-only
async function validateStateForImplementation(taskPath: string): Promise<void> {
  const state = await getTaskState(taskPath);

  if (state !== 'design_approved') {
    throw new Error(
      `Task must be in 'design_approved' state to use --implement-only. ` +
      `Current state: ${state}. Run with --design-only first.`
    );
  }
}
```

**Key Features:**
- Single entry point: `executePhases()`
- Clear routing logic based on mode
- State validation built-in
- Error handling at each phase
- Returns detailed execution result

**Complexity:** ~250 LOC (vs. 600+ LOC in original Strategy pattern approach)

---

### 2. Plan Persistence Module (`plan-persistence.ts`)

**Purpose:** Simple JSON save/load for implementation plans

```typescript
import fs from 'fs/promises';
import path from 'path';

interface ImplementationPlan {
  taskId: string;
  createdAt: string;
  requirements: any;
  design: any;
  architecturalReview: {
    score: number;
    recommendations: string[];
    requiresHumanCheckpoint: boolean;
    humanApproval?: {
      approved: boolean;
      timestamp: string;
      comments?: string;
    };
  };
}

// Simple save function
async function savePlan(
  taskId: string,
  plan: any,
  reviewResult: any
): Promise<string> {
  const planDir = path.join(process.cwd(), '.task-work', 'plans');
  await fs.mkdir(planDir, { recursive: true });

  const planPath = path.join(planDir, `${taskId}-plan.json`);

  const planData: ImplementationPlan = {
    taskId,
    createdAt: new Date().toISOString(),
    requirements: plan.requirements,
    design: plan.design,
    architecturalReview: {
      score: reviewResult.score,
      recommendations: reviewResult.recommendations,
      requiresHumanCheckpoint: reviewResult.requiresHumanCheckpoint,
      humanApproval: reviewResult.humanApproval
    }
  };

  await fs.writeFile(planPath, JSON.stringify(planData, null, 2), 'utf-8');
  return planPath;
}

// Simple load function
async function loadPlan(taskId: string): Promise<ImplementationPlan | null> {
  const planPath = path.join(process.cwd(), '.task-work', 'plans', `${taskId}-plan.json`);

  try {
    const content = await fs.readFile(planPath, 'utf-8');
    return JSON.parse(content);
  } catch (error) {
    if (error.code === 'ENOENT') {
      return null;
    }
    throw error;
  }
}

// Check if plan exists
async function planExists(taskId: string): Promise<boolean> {
  const plan = await loadPlan(taskId);
  return plan !== null;
}

// Delete plan (cleanup)
async function deletePlan(taskId: string): Promise<void> {
  const planPath = path.join(process.cwd(), '.task-work', 'plans', `${taskId}-plan.json`);

  try {
    await fs.unlink(planPath);
  } catch (error) {
    if (error.code !== 'ENOENT') {
      throw error;
    }
  }
}

export { savePlan, loadPlan, planExists, deletePlan };
export type { ImplementationPlan };
```

**Key Features:**
- Direct JSON file operations
- No versioning (YAGNI)
- Simple error handling
- Easy to extend later with Repository pattern if needed

**Complexity:** ~80 LOC (vs. 300+ LOC with Repository pattern + versioning)

---

### 3. Task Manager Integration (`task-manager.ts`)

**Purpose:** Integrate new features into existing task-work command

```typescript
// Add to existing task-manager.ts

import { executePhases } from './phase-execution';
import { loadPlan, planExists } from './plan-persistence';

interface TaskWorkOptions {
  mode?: 'standard' | 'tdd' | 'bdd';
  withContext?: boolean;
  syncProgress?: boolean;
  // NEW FLAGS
  designOnly?: boolean;
  implementOnly?: boolean;
}

async function executeTaskWork(taskId: string, options: TaskWorkOptions): Promise<void> {
  // Validate mutual exclusivity
  if (options.designOnly && options.implementOnly) {
    throw new Error('Cannot use --design-only and --implement-only together');
  }

  // Determine execution mode
  let executionMode: 'standard' | 'design-only' | 'implement-only' = 'standard';
  if (options.designOnly) {
    executionMode = 'design-only';
  } else if (options.implementOnly) {
    executionMode = 'implement-only';
  }

  // Get task path
  const taskPath = await findTaskFile(taskId);
  if (!taskPath) {
    throw new Error(`Task ${taskId} not found`);
  }

  // Execute phases
  const result = await executePhases({
    mode: executionMode,
    taskId,
    taskPath,
    withContext: options.withContext
  });

  // Handle result
  if (!result.success) {
    console.error('Task execution failed:');
    result.errors?.forEach(err => console.error(`  - ${err}`));
    throw new Error('Task execution failed');
  }

  // Report results
  console.log('Task execution completed successfully:');
  result.phasesExecuted.forEach(phase => console.log(`  ✓ ${phase}`));

  if (result.planPath) {
    console.log(`\nImplementation plan saved: ${result.planPath}`);
  }

  // Sync progress if requested
  if (options.syncProgress) {
    await syncTaskProgress(taskId);
  }
}

// Export for CLI integration
export { executeTaskWork };
```

**Key Features:**
- Clean integration with existing code
- Flag validation built-in
- Clear error messages
- Maintains backward compatibility

**Complexity:** ~120 LOC added (vs. 400+ LOC with multiple coordinators)

---

### 4. Agent Documentation Updates

#### task-manager.md (Modified)

Add section describing new flags:

```markdown
## Split Design and Implementation

The task-work command now supports splitting the design and implementation phases
for better control and review cycles.

### Design-Only Mode

Execute only the design phases (1 → 2 → 2.5 → 2.6):

```bash
/task-work TASK-XXX --design-only
```

**Phases Executed:**
1. Requirements Analysis
2. Implementation Planning
3. Architectural Review (Phase 2.5)
4. Human Checkpoint (Phase 2.6, if triggered)

**Output:**
- Implementation plan saved to `.task-work/plans/TASK-XXX-plan.json`
- Task state updated to `design_approved`
- Ready for implementation phase

### Implement-Only Mode

Execute only the implementation phases (3 → 4 → 4.5 → 5):

```bash
/task-work TASK-XXX --implement-only
```

**Requirements:**
- Task must be in `design_approved` state
- Implementation plan must exist

**Phases Executed:**
1. Implementation (using approved plan)
2. Testing (Phase 4)
3. Fix Loop (Phase 4.5, if tests fail)
4. Code Review (Phase 5)

### Standard Mode (Default)

Execute all phases in sequence (backward compatible):

```bash
/task-work TASK-XXX
```

This executes both design and implementation phases in a single run.
```

**Complexity:** ~30 LOC added

#### architectural-reviewer.md (Modified)

Add section clarifying integration with task-work:

```markdown
## Integration with Task-Work Workflow

The architectural reviewer is automatically invoked during Phase 2.5 of the
task-work command. It can be run in two modes:

### Integrated Mode (Standard)

Automatically runs as part of `/task-work TASK-XXX`:
- Executes after Phase 2 (Implementation Planning)
- Reviews the generated plan
- Triggers Phase 2.6 (Human Checkpoint) if score < 80
- Blocks implementation if design is rejected

### Split Mode (Design-Only)

Runs as part of `/task-work TASK-XXX --design-only`:
- Executes at the end of design phases
- Saves review results with implementation plan
- Updates task to `design_approved` state
- Implementation can proceed later with `--implement-only`

### Review Thresholds

- **≥80**: Auto-approved, proceed to implementation
- **60-79**: Approved with recommendations, optional human checkpoint
- **<60**: Rejected, requires redesign
```

**Complexity:** ~20 LOC added

---

## State Management

### New Task State: `design_approved`

**State Transition Diagram:**

```
BACKLOG
  ↓
IN_PROGRESS
  ↓
  ├─ (--design-only) → design_approved → (--implement-only) → IN_REVIEW
  └─ (standard) ────────────────────────────────────────────→ IN_REVIEW
  ↓
COMPLETED
```

**State Validation Rules:**

| Mode | Required State | Resulting State |
|------|----------------|-----------------|
| design-only | in_progress | design_approved |
| implement-only | design_approved | in_progress (during), in_review (after) |
| standard | in_progress | in_review |

---

## Implementation Phases

### Phase 1: Core Modules (2-3 hours)

**Files:**
1. `phase-execution.ts`: Core execution logic
2. `plan-persistence.ts`: JSON save/load utilities

**Deliverables:**
- Phase routing logic implemented
- State validation working
- Plan persistence functional
- Unit tests for both modules

**Testing Focus:**
- Mode routing correctness
- State validation edge cases
- JSON save/load reliability
- Error handling

### Phase 2: Integration (1-2 hours)

**Files:**
3. `task-manager.ts`: Integrate new features

**Deliverables:**
- Flag parsing and validation
- Integration with existing workflow
- Backward compatibility verified
- End-to-end tests

**Testing Focus:**
- Flag mutual exclusivity
- Backward compatibility
- Error messages
- Full workflow execution

### Phase 3: Documentation (30 min)

**Files:**
4. `task-manager.md`: Document new flags
5. `architectural-reviewer.md`: Clarify integration

**Deliverables:**
- User documentation complete
- Integration guide updated
- Examples provided

---

## Testing Strategy

### Unit Tests (~150 LOC)

```typescript
// phase-execution.test.ts
describe('Phase Execution', () => {
  describe('executePhases', () => {
    it('routes to design phases for design-only mode');
    it('routes to implementation phases for implement-only mode');
    it('routes to standard phases for default mode');
  });

  describe('executeDesignPhases', () => {
    it('executes phases 1, 2, 2.5 in sequence');
    it('triggers phase 2.6 when score < 80');
    it('saves plan and updates state');
    it('handles rejection at human checkpoint');
  });

  describe('executeImplementationPhases', () => {
    it('validates design_approved state');
    it('throws error if no approved plan exists');
    it('executes phases 3, 4, 4.5, 5 in sequence');
    it('handles test failures with fix loop');
  });

  describe('validateStateForImplementation', () => {
    it('passes for design_approved state');
    it('throws error for other states');
  });
});

// plan-persistence.test.ts
describe('Plan Persistence', () => {
  describe('savePlan', () => {
    it('creates plan directory if not exists');
    it('saves plan as JSON with correct structure');
    it('returns plan path');
  });

  describe('loadPlan', () => {
    it('loads existing plan');
    it('returns null for non-existent plan');
    it('throws error for invalid JSON');
  });

  describe('planExists', () => {
    it('returns true for existing plan');
    it('returns false for non-existent plan');
  });

  describe('deletePlan', () => {
    it('deletes existing plan');
    it('does not throw for non-existent plan');
  });
});
```

### Integration Tests (~100 LOC)

```typescript
// task-work-integration.test.ts
describe('Task Work Integration', () => {
  describe('Flag Validation', () => {
    it('throws error for both --design-only and --implement-only');
    it('accepts --design-only alone');
    it('accepts --implement-only alone');
    it('accepts no flags (standard mode)');
  });

  describe('Design-Only Workflow', () => {
    it('executes design phases successfully');
    it('saves implementation plan');
    it('updates task state to design_approved');
  });

  describe('Implement-Only Workflow', () => {
    it('validates design_approved state');
    it('loads approved plan');
    it('executes implementation phases');
    it('throws error if no plan exists');
  });

  describe('Backward Compatibility', () => {
    it('standard mode works as before');
    it('existing tasks continue to work');
  });
});
```

---

## Migration Path to Patterns

When complexity justifies it, the simplified design can be refactored to patterns:

### Step 1: Extract Strategy Pattern (When adding 3rd mode)

```typescript
// When we add a third mode like --review-only
interface PhaseExecutionStrategy {
  execute(taskId: string, taskPath: string, options: any): Promise<PhaseExecutionResult>;
}

class DesignOnlyStrategy implements PhaseExecutionStrategy { ... }
class ImplementOnlyStrategy implements PhaseExecutionStrategy { ... }
class StandardStrategy implements PhaseExecutionStrategy { ... }

// Refactor executePhases to use strategies
function executePhases(options: PhaseExecutionOptions): Promise<PhaseExecutionResult> {
  const strategy = getStrategy(options.mode);
  return strategy.execute(options.taskId, options.taskPath, options);
}
```

### Step 2: Add Repository Pattern (When adding versioning)

```typescript
// When we need plan versioning or multiple storage backends
interface PlanRepository {
  save(plan: ImplementationPlan): Promise<string>;
  load(taskId: string, version?: number): Promise<ImplementationPlan | null>;
  listVersions(taskId: string): Promise<number[]>;
}

class FilePlanRepository implements PlanRepository { ... }
class DatabasePlanRepository implements PlanRepository { ... } // Future
```

### Step 3: Add Versioning (When rollback is needed)

```typescript
// When we need to rollback to previous plan versions
interface VersionedPlan extends ImplementationPlan {
  version: number;
  previousVersion?: number;
}

async function savePlanWithVersion(plan: ImplementationPlan): Promise<string> {
  const latestVersion = await getLatestVersion(plan.taskId);
  const versionedPlan: VersionedPlan = {
    ...plan,
    version: latestVersion + 1,
    previousVersion: latestVersion
  };
  return repository.save(versionedPlan);
}
```

**Refactoring Triggers:**
- **Strategy Pattern**: When 3rd execution mode is added
- **Repository Pattern**: When versioning or alternate storage is needed
- **Versioning**: When plan rollback functionality is required

---

## Comparison: Original vs. Simplified

| Aspect | Original Plan | Simplified Plan | Reduction |
|--------|---------------|-----------------|-----------|
| **Files** | 12 new + 2 modified | 2 new + 3 modified | 64% fewer |
| **LOC** | ~1,740 | ~500 | 71% reduction |
| **Patterns** | 4 (Strategy, Repository, Factory, Chain) | 0 (functional) | -4 patterns |
| **Complexity** | High (multiple abstractions) | Low (direct logic) | Significant |
| **Test LOC** | ~600 | ~250 | 58% reduction |
| **Implementation Time** | 8-10 hours | 3-4 hours | 60% faster |
| **Maintainability** | Harder (many files/classes) | Easier (fewer files) | Much better |

---

## Risk Assessment

### Simplified Approach Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| Need to add patterns later | Medium | Low | Clear migration path defined |
| Conditional logic complexity | Low | Low | Well-structured switch/case |
| File size growth | Low | Low | Can split into modules if needed |

### Benefits of Simplification

| Benefit | Impact |
|---------|--------|
| Faster implementation | High |
| Easier to understand | High |
| Easier to test | High |
| Easier to debug | High |
| Less code to maintain | High |
| Faster onboarding | Medium |

---

## Validation Checklist

### Functional Requirements ✓
- [ ] Two flags: --design-only, --implement-only
- [ ] New state: design_approved
- [ ] Plan persistence (JSON)
- [ ] 100% backward compatibility
- [ ] State validation for implement-only
- [ ] Mutual exclusivity validation

### Architectural Principles ✓
- [ ] YAGNI: No unnecessary patterns
- [ ] DRY: Common phase logic extracted
- [ ] OCP: Easy to extend with new modes
- [ ] SRP: Clear module responsibilities
- [ ] SOLID: Can refactor to patterns later

### Quality Standards ✓
- [ ] <500 LOC total
- [ ] 5 files or fewer
- [ ] 80%+ test coverage
- [ ] Clear documentation
- [ ] Migration path defined

---

## Conclusion

This simplified design:
1. **Reduces complexity by 71%** (1,740 → 500 LOC)
2. **Maintains all functional requirements**
3. **Follows YAGNI, DRY, OCP principles**
4. **Provides clear migration path to patterns**
5. **Faster to implement and test** (60% time reduction)
6. **Easier to understand and maintain**

The key insight: **Start simple, add complexity only when justified by requirements.**

**Estimated Implementation Time:** 3-4 hours
**Estimated Testing Time:** 1-2 hours
**Total:** 4-6 hours (vs. 10-12 hours for original plan)

**Recommended Next Steps:**
1. Review and approve this simplified plan
2. Implement Phase 1 (core modules)
3. Implement Phase 2 (integration)
4. Implement Phase 3 (documentation)
5. Run full test suite
6. Deploy and monitor

---

## Appendix: File Structure Visualization

```
Before (Original Plan):
├── src/
│   ├── strategies/              # NEW (4 files, ~600 LOC)
│   │   ├── PhaseExecutionStrategy.ts
│   │   ├── DesignOnlyStrategy.ts
│   │   ├── ImplementOnlyStrategy.ts
│   │   └── StandardStrategy.ts
│   ├── repositories/            # NEW (3 files, ~300 LOC)
│   │   ├── PlanRepository.ts
│   │   ├── FilePlanRepository.ts
│   │   └── PlanVersionManager.ts
│   ├── coordinators/            # NEW (3 files, ~400 LOC)
│   │   ├── WorkflowCoordinator.ts
│   │   ├── DesignCoordinator.ts
│   │   └── ImplementationCoordinator.ts
│   └── factories/               # NEW (2 files, ~240 LOC)
│       ├── StrategyFactory.ts
│       └── RepositoryFactory.ts
└── ...
Total: 12 new files, ~1,740 LOC

After (Simplified Plan):
├── src/utils/
│   ├── phase-execution.ts       # NEW (~250 LOC)
│   ├── plan-persistence.ts      # NEW (~80 LOC)
│   └── task-manager.ts          # MODIFIED (+120 LOC)
└── installer/global/agents/
    ├── task-manager.md          # MODIFIED (+30 LOC)
    └── architectural-reviewer.md # MODIFIED (+20 LOC)

Total: 2 new files + 3 modified, ~500 LOC
```

---

**Document Version:** 1.0
**Last Updated:** 2025-10-11
**Author:** Software Architect (AI)
**Status:** Ready for Review
