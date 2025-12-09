# Progressive Disclosure Implementation for RequireKit

**Source Review**: TASK-REV-PD01 (GuardKit)
**Decision**: [I]mplement with [C]ustomize approach
**Total Effort**: 3-4 hours
**Expected Token Savings**: ~32%

## Overview

This folder contains implementation tasks to apply progressive disclosure techniques from GuardKit to RequireKit. The implementation splits large agent files into core + extended files to reduce context window usage while maintaining quality.

## Implementation Waves

Tasks are organized into waves for parallel execution via Conductor workspaces. Each wave contains independent tasks that can be executed simultaneously.

### Wave 1: Foundation (Prerequisites)
**Parallel Execution**: No - must complete before Wave 2
**Conductor Workspace**: N/A (sequential)

| Task ID | Title | Mode | Effort |
|---------|-------|------|--------|
| TASK-PD-RK01 | Consolidate duplicate agent files | Direct | 15 min |
| TASK-PD-RK02 | Copy reusable scripts from GuardKit | Direct | 15 min |

### Wave 2: Agent Splitting (Parallel)
**Parallel Execution**: Yes - all tasks independent
**Conductor Workspaces**: `progressive-disclosure-bdd`, `progressive-disclosure-analyst`

| Task ID | Title | Mode | Effort |
|---------|-------|------|--------|
| TASK-PD-RK03 | Split bdd-generator.md into core + extended | /task-work | 1 hour |
| TASK-PD-RK04 | Split requirements-analyst.md into core + extended | /task-work | 45 min |

### Wave 3: Integration & Testing (Parallel)
**Parallel Execution**: Yes - test tasks independent
**Conductor Workspaces**: `progressive-disclosure-test-bdd`, `progressive-disclosure-test-ears`

| Task ID | Title | Mode | Effort |
|---------|-------|------|--------|
| TASK-PD-RK05 | Test /generate-bdd with split files | Direct | 30 min |
| TASK-PD-RK06 | Test /formalize-ears with split files | Direct | 30 min |

### Wave 4: Documentation (Final)
**Parallel Execution**: No - depends on all previous waves
**Conductor Workspace**: N/A (sequential)

| Task ID | Title | Mode | Effort |
|---------|-------|------|--------|
| TASK-PD-RK07 | Update RequireKit documentation | Direct | 30 min |

## Execution Modes

### /task-work Mode
Use for complex tasks requiring:
- Quality gates (compilation, tests)
- Architectural review
- Multiple file changes
- Code generation with patterns

**Tasks**: TASK-PD-RK03, TASK-PD-RK04

### Direct Claude Code Mode
Use for straightforward tasks:
- File copying/moving
- Simple edits
- Manual testing
- Documentation updates

**Tasks**: TASK-PD-RK01, TASK-PD-RK02, TASK-PD-RK05, TASK-PD-RK06, TASK-PD-RK07

## Conductor Parallel Execution

### Wave 2 Parallel Setup
```bash
# Create workspaces for parallel agent splitting
conductor create progressive-disclosure-bdd
conductor create progressive-disclosure-analyst

# In workspace progressive-disclosure-bdd:
/task-work TASK-PD-RK03

# In workspace progressive-disclosure-analyst:
/task-work TASK-PD-RK04
```

### Wave 3 Parallel Setup
```bash
# Create workspaces for parallel testing
conductor create progressive-disclosure-test-bdd
conductor create progressive-disclosure-test-ears

# In workspace progressive-disclosure-test-bdd:
# Execute TASK-PD-RK05 directly

# In workspace progressive-disclosure-test-ears:
# Execute TASK-PD-RK06 directly
```

## File Structure After Implementation

```
require-kit/
├── installer/global/
│   ├── agents/
│   │   ├── bdd-generator.md              # Core (~6KB)
│   │   ├── bdd-generator-ext.md          # Extended (~12KB) [NEW]
│   │   ├── requirements-analyst.md       # Core (~5KB)
│   │   └── requirements-analyst-ext.md   # Extended (~7KB) [NEW]
│   └── lib/
│       └── agent_enhancement/            # [NEW]
│           ├── models.py                 # From GuardKit
│           └── applier.py                # Adapted for RequireKit
```

## Dependencies

### From GuardKit
- `installer/global/lib/agent_enhancement/models.py` - Direct copy
- `installer/global/lib/agent_enhancement/applier.py` - Adapt paths
- `installer/global/lib/agent_enhancement/boundary_utils.py` - Direct copy
- `installer/global/lib/utils/file_io.py` - Direct copy

### Section Categorization
Uses GuardKit's proven categorization:

**CORE_SECTIONS** (always loaded):
- frontmatter, title, quick_start, boundaries, capabilities, phase_integration

**EXTENDED_SECTIONS** (on-demand):
- detailed_examples, best_practices, anti_patterns, cross_stack, troubleshooting

## Success Criteria

- [ ] BDD generation (`/generate-bdd`) works correctly with split files
- [ ] EARS formalization (`/formalize-ears`) maintains quality
- [ ] Token usage reduced by ≥30% for typical tasks
- [ ] No regression in command functionality
- [ ] Loading instructions followed by Claude consistently
- [ ] All tests pass

## Related Tasks

- **TASK-PD-001** (GuardKit) - Original progressive disclosure implementation
- **TASK-REV-PD01** (GuardKit) - Analysis review that spawned this implementation

## Timeline

| Wave | Duration | Cumulative |
|------|----------|------------|
| Wave 1 | 30 min | 30 min |
| Wave 2 | 1 hour (parallel) | 1h 30m |
| Wave 3 | 30 min (parallel) | 2h |
| Wave 4 | 30 min | 2h 30m |

**Total wall-clock time with parallel execution**: ~2.5 hours
**Total effort (sequential)**: ~3.5 hours
**Speedup from parallelization**: ~29%
