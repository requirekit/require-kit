# Micro-Task Mode Implementation

**Implementation for TASK-020: Add Micro-Task Mode to Task Work Command**

## Overview

Micro-task mode provides a streamlined workflow for trivial tasks (typo fixes, documentation updates, cosmetic changes) that don't require full architectural review. Completes in 3-5 minutes vs 15+ minutes for standard workflow.

## Components

### 1. MicroTaskDetector (`micro_task_detector.py`)

**Purpose**: Heuristic-based detection to identify micro-tasks eligible for streamlined workflow.

**Key Features**:
- Analyzes task metadata (title, description, estimated effort, complexity)
- Detects high-risk keywords (security, database, API, breaking changes)
- Estimates file count from task description
- Parses estimated effort strings (minutes/hours)
- Calculates confidence score (0.0-1.0)
- Special handling for documentation-only tasks

**Micro-Task Criteria** (ALL must be true):
- Single file modification (or documentation-only)
- Estimated effort <1 hour
- Complexity ≤ 1/10
- No high-risk keywords detected

**High-Risk Keywords** (block micro-task mode):
- **Security**: auth, password, token, jwt, oauth, encryption
- **Data**: database, migration, schema, sql, table, transaction
- **API**: breaking change, api change, public api, interface change
- **External**: integration, third-party, external api, webhook, payment

**Documentation-Only Exception**:
Tasks affecting only documentation files (.md, .txt, .rst, .adoc) automatically qualify for micro-task mode, even if they affect multiple files.

**Usage**:
```python
from micro_task_detector import MicroTaskDetector

detector = MicroTaskDetector()
analysis = detector.analyze(task_metadata)

if analysis.can_use_micro_mode:
    print("✅ Micro-task mode eligible")
else:
    print("❌ Blocked:", analysis.blocking_reasons)
```

**Public API**:
- `analyze_micro_task(task_metadata)` - Analyze eligibility
- `validate_micro_mode(task_metadata)` - Validate --micro flag usage
- `suggest_micro_mode(task_metadata)` - Generate auto-suggestion message

### 2. MicroTaskWorkflow (`micro_task_workflow.py`)

**Purpose**: Execute streamlined workflow for micro-tasks.

**Phases Executed**:
- Phase 1: Load Task Context (standard)
- Phase 3: Implementation (simplified)
- Phase 4: Quick Testing (compilation + tests, no coverage)
- Phase 4.5: Fix Loop (1 attempt max, vs 3 in standard)
- Phase 5: Quick Review (lint only, skip SOLID/DRY/YAGNI)

**Phases Skipped**:
- Phase 2: Implementation Planning
- Phase 2.5A: Pattern Suggestion
- Phase 2.5B: Architectural Review
- Phase 2.6: Human Checkpoint
- Phase 2.7: Complexity Evaluation

**Quality Gates**:
| Gate | Standard | Micro-Task |
|------|----------|------------|
| Compilation | REQUIRED | REQUIRED |
| Tests Pass | REQUIRED | REQUIRED |
| Coverage (80%+) | REQUIRED | **SKIPPED** |
| Architectural Review | REQUIRED | **SKIPPED** |
| Code Review (SOLID/DRY) | REQUIRED | **SKIPPED** |
| Lint Check | Optional | REQUIRED |

**Usage**:
```python
from micro_task_workflow import MicroTaskWorkflow

workflow = MicroTaskWorkflow()
result = workflow.execute(task_id, task_metadata)

if result.success:
    print(f"✅ Completed in {result.duration_minutes:.2f} minutes")
    print(f"State: {result.final_state}")
else:
    print(f"❌ Failed: {result.error_message}")
```

**Public API**:
- `execute_micro_workflow(task_id, task_metadata)` - Execute workflow

### 3. Documentation Updates

**task-work.md**:
- Added `--micro` flag documentation
- Documented auto-detection behavior
- Added examples (success, auto-detection, escalation)
- Listed use cases and exclusions

**task-manager.md**:
- Added micro-task workflow orchestration
- Documented pre-flight validation
- Added phase skipping logic
- Included integration points

## Testing

### Unit Tests

**test_micro_task_detector.py** (comprehensive pytest suite):
- Basic detection tests (typo fix, doc update, API endpoint)
- High-risk keyword detection (security, database, breaking changes)
- File count estimation (single, multiple, explicit list)
- Effort parsing (minutes, hours, ranges)
- Confidence scoring (simple, complex, doc-only override)
- Documentation-only detection
- Auto-suggestion behavior
- Validation tests
- Public API tests
- Edge cases

**test_micro_workflow.py** (comprehensive pytest suite):
- Workflow execution tests
- Phase execution tests
- Quality gate tests
- Fix loop tests (max 1 attempt)
- Configuration tests
- State transition tests
- Error handling tests
- Performance tests

**test_micro_basic.py** (no pytest required):
- Basic sanity tests that can run with just python3
- Detector functionality
- Workflow execution
- Effort parsing
- Risk detection
- Confidence scoring

### Running Tests

**With pytest** (if available):
```bash
cd installer/global/commands/lib
pytest test_micro_task_detector.py -v
pytest test_micro_workflow.py -v
```

**Without pytest** (basic sanity tests):
```bash
cd installer/global/commands/lib
python3 test_micro_basic.py
```

**Compile check**:
```bash
cd installer/global/commands/lib
python3 -m py_compile micro_task_detector.py micro_task_workflow.py
```

## Integration Points

### Entry Point: task-work.md

1. Parse `--micro` flag from command line
2. Validate flag with `MicroTaskDetector.validate_micro_mode()`
3. Route to `MicroTaskWorkflow.execute()` if valid
4. Otherwise escalate to standard workflow

### Auto-Detection Flow

1. User runs `/task-work TASK-XXX` (without --micro)
2. System analyzes task with `MicroTaskDetector.suggest_micro_mode()`
3. If confidence ≥ 90%, show suggestion with 10-second timeout
4. User can accept (y/yes) or decline (N/default)
5. On timeout or decline, continue with standard workflow

### State Transitions

Same as standard workflow:
- BACKLOG → IN_PROGRESS → IN_REVIEW (if quality gates pass)
- BACKLOG → IN_PROGRESS → BLOCKED (if quality gates fail)

## Architecture Decisions

### Design Principles

1. **Single Responsibility**: Detector vs Executor vs Orchestrator
2. **Conservative Blocking**: False negative better than false positive
3. **Zero External Dependencies**: Uses only Python standard library
4. **Dataclass-Based**: Structured results with type hints
5. **Performance**: Compiled regex patterns for keyword detection
6. **Strategy Pattern**: Workflow routing based on task characteristics

### Key Architectural Choices

**From Phase 2.5B Review (Score: 88/100)**:

1. **Dataclasses over dictionaries** for structured results
   - Type safety
   - Clear interfaces
   - Immutability with `frozen=True`

2. **Compiled regex patterns** for performance
   - Pre-compile risk keyword patterns
   - Reuse across multiple analyses
   - Case-insensitive matching with word boundaries

3. **Single responsibility separation**:
   - `MicroTaskDetector` - Detection only
   - `MicroTaskWorkflow` - Execution only
   - `task-manager.md` - Orchestration

4. **Strategy pattern** for workflow routing:
   - Detector provides analysis
   - Orchestrator routes to appropriate workflow
   - Workflows are self-contained

5. **No external dependencies**:
   - Uses only Python standard library
   - No external APIs or databases
   - Portable across environments

## Usage Examples

### Example 1: Micro-Task (Typo Fix)

```bash
/task-work TASK-047 --micro

Micro-Task Mode Enabled
Validation: PASSED (confidence: 95%)

Phase 1: Load Task Context                        [0.3s]
  ✓ Loaded TASK-047
  ✓ Title: Fix typo in error message
  ✓ File: src/services/AuthService.py

Phases 2-2.7: SKIPPED (micro-task mode)

Phase 3: Implementation                           [1.2s]
  ✓ Updated src/services/AuthService.py:45
  ✓ Changed 'occured' → 'occurred'

Phase 4: Quick Testing                            [0.8s]
  ✓ Compilation: PASSED
  ✓ Tests: 5/5 PASSED (coverage skipped)

Phase 4.5: Fix Loop                               [SKIPPED - tests passed]

Phase 5: Quick Review                             [0.4s]
  ✓ Lint: PASSED (no issues)

Quality Gates: 3/3 PASSED
Task State: BACKLOG → IN_REVIEW
Duration: 2 minutes 34 seconds
```

### Example 2: Auto-Detection

```bash
/task-work TASK-047

Detected micro-task (confidence: 95%)
This task appears to be trivial (complexity 1/10, single file, <1 hour).

Suggest using: /task-work TASK-047 --micro
Saves ~12 minutes by skipping optional phases.

Auto-apply micro-mode? [y/N] (10s timeout): y

Applying micro-task mode...
[continues with micro-task workflow]
```

### Example 3: Escalation

```bash
/task-work TASK-048 --micro

Task does not qualify as micro-task:
  - Complexity: 5/10 (threshold: 1/10)
  - High-risk keywords detected: authentication, database
  - Estimated effort: 4 hours (threshold: <1 hour)

Escalating to full workflow...

Phase 1: Load Task Context
Phase 2: Implementation Planning
Phase 2.5B: Architectural Review
[continues with full workflow]
```

## Performance Targets

- **Execution Time**: 3-5 minutes (vs 15+ minutes for standard workflow)
- **Time Savings**: 70-80% reduction for trivial tasks
- **Accuracy**: 95%+ correct micro-task detection
- **False Escalation**: <5% (incorrectly escalated to full workflow)

## Future Enhancements

1. **Machine Learning Classification**: Train classifier on historical task data
2. **Custom Risk Keywords**: Allow per-project configuration of blocking keywords
3. **Integration with PM Tools**: Auto-tag micro-tasks in Jira/Linear
4. **Metrics Dashboard**: Track micro-task usage and time savings
5. **Force-Micro Flag**: `--force-micro` to override safety checks (advanced users)

## Success Metrics

**From TASK-020 Requirements**:
- ✅ Complexity score = 1/10
- ✅ Single file modification (or docs-only)
- ✅ Estimated time <1 hour
- ✅ Low risk (no security/database/API keywords)
- ✅ Complete in ≤5 minutes
- ✅ Skip all optional/complex phases
- ✅ Minimal quality gates (compilation + basic tests)
- ✅ Auto-detection with 10-second timeout
- ✅ Manual override with `--micro` flag
- ✅ Comprehensive test coverage

## Related Tasks

- TASK-019: Concise Mode for EARS
- TASK-018: Spec Drift Detection
- TASK-006: Design-First Workflow

## Files Created/Modified

### New Files
- `installer/global/commands/lib/micro_task_detector.py` (300 lines)
- `installer/global/commands/lib/micro_task_workflow.py` (250 lines)
- `installer/global/commands/lib/test_micro_task_detector.py` (comprehensive pytest suite)
- `installer/global/commands/lib/test_micro_workflow.py` (comprehensive pytest suite)
- `installer/global/commands/lib/test_micro_basic.py` (basic sanity tests)
- `installer/global/commands/lib/MICRO_TASK_README.md` (this file)

### Modified Files
- `installer/global/commands/task-work.md` (added --micro flag documentation)
- `installer/global/agents/task-manager.md` (added micro-task workflow orchestration)

## License

Part of the Agentecflow software engineering lifecycle system.
