---
id: TASK-026
title: Create `/task-refine` Command for Iterative Code Refinement
status: completed
priority: critical
created: 2025-10-18T10:15:00Z
completed_at: 2025-10-18T13:42:00Z
labels: [enhancement, sdd-alignment, critical-gap, hubbard-workflow, human-in-loop]
estimated_effort: 8 hours
actual_effort: 6 hours
complexity_estimate: 6
actual_complexity: 6

# Source
source: implementation-plan-and-code-review-analysis.md
recommendation: MUST-HAVE - Critical Gap
research_support: John Hubbard's workflow (Step 5), Martin Fowler (iterative steps)
alignment: Enables human-in-the-loop iteration

# Implementation Summary
implemented_via: git worktree (Conductor)
commit_hash: 3f2ac0e0b8252e3a488cf86e2096035b56c7628c
merged_at: 2025-10-18T13:42:26Z
branch: Rich/TASK-026

# Requirements - All Met ✅
requirements:
  - REQ-REFINE-001: Allow refinement of tasks in IN_REVIEW or BLOCKED state ✅
  - REQ-REFINE-002: Apply targeted fixes without re-running full workflow ✅
  - REQ-REFINE-003: Preserve full context (plan, review comments, existing code) ✅
  - REQ-REFINE-004: Re-run testing and code review after refinement ✅
  - REQ-REFINE-005: Support multiple refinement iterations ✅
  - REQ-REFINE-006: Track refinement history ✅

# Deliverables
files_created:
  - installer/global/commands/task-refine.md (17,177 bytes)
  - installer/global/commands/lib/refinement_handler.py
  - installer/global/commands/lib/refinement_session.py
  - tests/unit/test_refinement_handler.py
---

# Create `/task-refine` Command for Iterative Code Refinement

## Problem Statement

**Hubbard's workflow** includes a critical iteration step:
> "5. Re-execute as necessary until tests pass"

**Fowler's research** emphasizes:
> "The best way for us to stay in control of what we're building are small, iterative steps"

**Current gap in AI-Engineer Lite**:
When a task reaches `IN_REVIEW` state and code review identifies issues, there's **no easy mechanism** for humans to request refinements:

```
Current workflow:
Task reaches IN_REVIEW
  → Code review runs (Phase 5)
  → Issues found: "Error handling incomplete in AuthService"
  → Human sees issues
  → ??? (What now?)

Current painful options:
1. Manually edit code (loses AI assistance, context)
2. Re-run /task-work TASK-XXX (re-does ENTIRE workflow, expensive)
3. Create new task (heavyweight, loses context, fragments work)
```

**Result**: Human-in-the-loop iteration is **difficult and inefficient**.

## Solution Overview

Create `/task-refine` command that enables **lightweight, iterative refinement** for tasks in review:

```bash
/task-refine TASK-042 "Add input validation to login endpoint"

# Workflow:
1. Validate task is in IN_REVIEW or BLOCKED state
2. Load implementation plan (Phase 2.7 output)
3. Load code review comments (Phase 5 output)
4. Load plan audit report (Phase 5.5 output)
5. Apply human's refinement request
6. Re-run Phase 4 (tests)
7. Re-run Phase 4.5 (fix loop)
8. Re-run Phase 5 (code review)
9. Re-run Phase 5.5 (plan audit)
10. Update task state based on results
11. Loop: Stay in IN_REVIEW (iterate further if needed)
```

**Key benefits**:
- ✅ Lightweight (doesn't re-plan or re-review architecture)
- ✅ Preserves context (plan, review, code)
- ✅ AI-assisted (human doesn't manually edit)
- ✅ Iterative (can refine multiple times)
- ✅ Tracked (refinement history saved)

## Acceptance Criteria

### 1. Command Specification
File: `installer/global/commands/task-refine.md`

```markdown
# Task Refine - Iterative Code Refinement Command

## Syntax
/task-refine TASK-XXX "refinement request" [--interactive]

## State Requirements
- Task MUST be in IN_REVIEW or BLOCKED state
- Task MUST have implementation plan (from Phase 2.7)
- Task MUST have code files created

## Refinement Request
Human-readable description of what to fix/improve:
- "Add input validation to login endpoint"
- "Extract token logic into separate class"
- "Fix memory leak in session manager"
- "Improve error messages in auth flow"

## Workflow
1. Load task context (plan, code, review comments, audit)
2. Apply refinement request
3. Re-run quality gates (tests, review, audit)
4. Update task state
5. Create refinement session record

## Interactive Mode
/task-refine TASK-042 --interactive

Opens chat-like interface for back-and-forth refinement.
```

Acceptance criteria:
- [ ] Command spec written and documented
- [ ] Examples provided for common refinement scenarios
- [ ] Integration with task-work workflow documented

### 2. Refinement Handler Module
File: `installer/global/commands/lib/refinement_handler.py`

```python
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
import json

@dataclass
class RefinementRequest:
    task_id: str
    refinement_description: str
    requested_by: str  # "human" or username
    requested_at: str
    context: Dict[str, Any]  # plan, review, audit

@dataclass
class RefinementResult:
    success: bool
    refinement_id: str  # e.g., "TASK-042-refine-001"
    files_modified: List[str]
    tests_passed: bool
    review_passed: bool
    audit_passed: bool
    new_state: str  # "in_review" or "blocked"
    timestamp: str

class RefinementHandler:
    def refine(self, request: RefinementRequest) -> RefinementResult:
        # 1. Validate state
        self._validate_state(request.task_id)

        # 2. Load context
        context = self._load_context(request.task_id)

        # 3. Apply refinement
        modified_files = self._apply_refinement(
            request.task_id,
            request.refinement_description,
            context
        )

        # 4. Re-run quality gates
        test_result = self._run_tests(request.task_id)
        review_result = self._run_code_review(request.task_id)
        audit_result = self._run_plan_audit(request.task_id)

        # 5. Determine new state
        new_state = self._calculate_state(
            test_result, review_result, audit_result
        )

        # 6. Save refinement session
        session = self._save_refinement_session(
            request, modified_files, new_state
        )

        return RefinementResult(...)
```

Acceptance criteria:
- [ ] `RefinementHandler` class implemented
- [ ] State validation (only IN_REVIEW/BLOCKED allowed)
- [ ] Context loading (plan, review, audit, code)
- [ ] Refinement application (invoke implementation agent)
- [ ] Quality gate re-execution
- [ ] State transition logic
- [ ] Refinement session tracking

### 3. State Validation
Enforce state requirements:

```python
def _validate_state(self, task_id: str) -> None:
    task_file = find_task_file(task_id)
    metadata = parse_frontmatter(task_file)

    if metadata['status'] not in ['in_review', 'blocked']:
        raise InvalidStateError(
            f"Task {task_id} is in {metadata['status']} state. "
            f"Refinement only allowed for tasks in IN_REVIEW or BLOCKED."
        )

    # Check for implementation plan
    if not plan_exists(task_id):
        raise MissingPlanError(
            f"Task {task_id} has no implementation plan. "
            f"Run /task-work first."
        )
```

Acceptance criteria:
- [ ] Validate task state (IN_REVIEW or BLOCKED only)
- [ ] Check for implementation plan existence
- [ ] Check for created code files
- [ ] Clear error messages for invalid states

### 4. Context Loading
Load full context for refinement:

```python
def _load_context(self, task_id: str) -> Dict[str, Any]:
    return {
        'plan': load_plan(task_id),
        'code_review': load_code_review_results(task_id),
        'plan_audit': load_plan_audit_report(task_id),
        'task_metadata': load_task_metadata(task_id),
        'files_created': find_task_files(task_id),
        'test_results': load_test_results(task_id)
    }
```

Acceptance criteria:
- [ ] Load implementation plan
- [ ] Load code review comments
- [ ] Load plan audit report (if exists)
- [ ] Load task metadata
- [ ] Load list of created files
- [ ] Load previous test results

### 5. Refinement Application
Invoke AI agent to apply refinement:

```python
def _apply_refinement(
    self,
    task_id: str,
    refinement_description: str,
    context: Dict[str, Any]
) -> List[str]:
    # Build refinement prompt
    prompt = self._build_refinement_prompt(
        task_id,
        refinement_description,
        context
    )

    # Invoke task-manager agent (or specialized agent)
    agent = get_agent("task-manager")
    result = agent.execute(prompt)

    # Extract modified files
    modified_files = extract_modified_files(result)

    return modified_files
```

Refinement prompt template:
```
You are refining an existing implementation.

TASK: {task_id} - {task_title}

ORIGINAL PLAN:
{implementation_plan}

CODE REVIEW COMMENTS:
{review_comments}

PLAN AUDIT ISSUES:
{audit_issues}

REFINEMENT REQUEST:
{refinement_description}

INSTRUCTIONS:
1. Apply ONLY the requested refinement
2. Do NOT change unrelated code
3. Preserve existing patterns and style
4. Update tests if necessary
5. Do NOT add scope creep

CONSTRAINTS:
- Modify existing files only (no new files unless requested)
- Follow original architectural decisions
- Maintain test coverage
- Fix the specific issue mentioned
```

Acceptance criteria:
- [ ] Build context-rich refinement prompt
- [ ] Invoke appropriate agent
- [ ] Extract modified files
- [ ] Validate changes were targeted (not wholesale rewrite)

### 6. Quality Gate Re-execution
Re-run phases 4, 4.5, 5, 5.5:

```python
def _run_tests(self, task_id: str) -> TestResult:
    # Re-run Phase 4
    return execute_phase_4_testing(task_id)

def _run_code_review(self, task_id: str) -> ReviewResult:
    # Re-run Phase 5
    return execute_phase_5_code_review(task_id)

def _run_plan_audit(self, task_id: str) -> AuditResult:
    # Re-run Phase 5.5 (if TASK-025 implemented)
    if phase_5_5_available():
        return execute_phase_5_5_plan_audit(task_id)
    else:
        return None
```

Acceptance criteria:
- [ ] Re-run Phase 4 (testing)
- [ ] Re-run Phase 4.5 (fix loop if tests fail)
- [ ] Re-run Phase 5 (code review)
- [ ] Re-run Phase 5.5 (plan audit, if available)
- [ ] Collect all results

### 7. State Transition Logic
Determine new state based on quality gate results:

```python
def _calculate_state(
    self,
    test_result: TestResult,
    review_result: ReviewResult,
    audit_result: Optional[AuditResult]
) -> str:
    # All gates pass → IN_REVIEW
    if (test_result.passed and
        review_result.passed and
        (audit_result is None or audit_result.passed)):
        return "in_review"

    # Any gate fails → BLOCKED
    else:
        return "blocked"
```

Acceptance criteria:
- [ ] Calculate state based on quality gates
- [ ] Update task frontmatter
- [ ] Move task file if state changes directory

### 8. Refinement Session Tracking
Track refinement history:

```python
def _save_refinement_session(
    self,
    request: RefinementRequest,
    modified_files: List[str],
    new_state: str
) -> str:
    session_id = f"{request.task_id}-refine-{get_next_refine_number()}"

    session = {
        "session_id": session_id,
        "task_id": request.task_id,
        "refinement_description": request.refinement_description,
        "requested_by": request.requested_by,
        "requested_at": request.requested_at,
        "modified_files": modified_files,
        "new_state": new_state,
        "tests_passed": test_result.passed,
        "review_passed": review_result.passed,
        "audit_passed": audit_result.passed if audit_result else None
    }

    # Save to docs/state/{task_id}/refinements/{session_id}.json
    save_refinement_session(session)

    # Update task metadata
    update_task_metadata(request.task_id, {
        "refinement_sessions": append_session(session_id)
    })

    return session_id
```

Acceptance criteria:
- [ ] Generate unique session ID
- [ ] Save refinement session metadata
- [ ] Store in `docs/state/{task_id}/refinements/`
- [ ] Update task frontmatter with session list
- [ ] Track: request, files changed, outcomes

### 9. Interactive Mode (Optional Enhancement)
Support back-and-forth refinement:

```bash
/task-refine TASK-042 --interactive

# Opens chat interface
Refinement Chat - TASK-042

You: Add input validation to login endpoint

AI: I've added validation for email and password fields.
    - Email: regex validation for format
    - Password: minimum 8 characters

    Would you like me to add anything else?

You: Also add rate limiting

AI: Added rate limiting:
    - Max 5 attempts per 15 minutes per IP
    - Using in-memory store (consider Redis for production)

    Tests updated and passing. Review the changes?

You: Yes, looks good

AI: Running quality gates...
    ✅ Tests: 15/15 passed
    ✅ Code review: No issues
    ✅ Plan audit: 1 extra dependency (rate-limiter)

    Refinement complete. Task TASK-042 → IN_REVIEW
```

Acceptance criteria:
- [ ] `--interactive` flag support
- [ ] Chat-like interface
- [ ] Multi-turn conversation
- [ ] Quality gates run after confirmation
- [ ] Exit command to complete refinement

### 10. Task Metadata Updates
Update task file with refinement info:

```yaml
---
id: TASK-042
status: in_review
refinements:
  - session_id: TASK-042-refine-001
    description: "Add input validation to login endpoint"
    requested_at: "2025-10-18T11:30:00Z"
    outcome: success
  - session_id: TASK-042-refine-002
    description: "Fix memory leak in session manager"
    requested_at: "2025-10-18T14:15:00Z"
    outcome: success
refinement_count: 2
---
```

Acceptance criteria:
- [ ] Add `refinements` array to frontmatter
- [ ] Track each refinement session
- [ ] Include description and outcome
- [ ] Add `refinement_count` metric

### 11. Documentation
- [ ] Create `installer/global/commands/task-refine.md`
- [ ] Update `docs/workflows/task-workflow.md` with refinement section
- [ ] Add examples to `docs/research/implementation-plan-and-code-review-analysis.md`
- [ ] Update CLAUDE.md with refinement workflow

## Implementation Plan

### Step 1: Create Command Spec (1 hour)
Write `task-refine.md` with full specification and examples.

### Step 2: Create Refinement Handler (3 hours)
Implement `refinement_handler.py` with core logic.

### Step 3: State Validation (1 hour)
Add state checking and error messages.

### Step 4: Context Loading (1 hour)
Load plan, review, audit, code context.

### Step 5: Quality Gate Re-execution (1 hour)
Wire up phases 4, 4.5, 5, 5.5.

### Step 6: Session Tracking (1 hour)
Save refinement history and metadata.

### Step 7: Documentation (30 min)
Update command docs and workflow guides.

## Testing Strategy

### Unit Tests
- [ ] `test_refinement_handler.py`: Core logic
- [ ] `test_state_validation.py`: State checking
- [ ] `test_context_loading.py`: Context assembly

### Integration Tests
- [ ] `test_refinement_workflow.py`: End-to-end refinement
- [ ] `test_quality_gate_rerun.py`: Phase re-execution
- [ ] `test_session_tracking.py`: History tracking

### E2E Tests
- [ ] Create task, implement, review
- [ ] Refine with `/task-refine`
- [ ] Verify quality gates re-run
- [ ] Verify state transitions
- [ ] Refine again (multiple iterations)

## Benefits

### Immediate
- ✅ Easy human-in-the-loop iteration
- ✅ Preserves full context (plan, review, code)
- ✅ Lightweight (doesn't re-run full workflow)
- ✅ Matches Hubbard's "re-execute as necessary" pattern

### Long-term
- ✅ Supports Fowler's "small, iterative steps" approach
- ✅ Reduces frustration with code review process
- ✅ Tracks refinement patterns (data for improvement)
- ✅ Enables true human-AI collaboration

## Dependencies

- Prerequisite: None (uses existing phase execution)
- Recommended: TASK-025 (plan audit provides context)
- Recommended: TASK-027 (markdown plans easier to read)

## Success Metrics (30-day pilot)

After 30 days:
- [ ] % of tasks requiring refinement
- [ ] Average refinement iterations per task
- [ ] Time per refinement vs manual editing
- [ ] Time saved vs re-running full workflow
- [ ] User satisfaction (easier iteration?)

Target:
- 50% of tasks use refinement (at least once)
- Average 1-2 refinements per task
- 10-15 min saved per refinement (vs re-running)

## Related Tasks

- TASK-025: Plan audit (provides context for refinement)
- TASK-027: Markdown plans (easier to read during refinement)
- TASK-021: Requirement versioning (similar iteration concept)

## References

- John Hubbard LinkedIn post (Step 5 - Re-execute as necessary)
- Martin Fowler SDD research (small, iterative steps)
- `docs/research/implementation-plan-and-code-review-analysis.md`
- ThoughtWorks findings (agents don't always follow instructions)
