---
id: TASK-028
title: Enhance Phase 2.8 Checkpoint Display with Plan Summary
status: completed
priority: low
created: 2025-10-18T12:00:00Z
updated: 2025-10-18T13:45:00Z
completed: 2025-10-18T13:45:00Z
labels: [enhancement, ux-improvement, optional, hubbard-workflow]
estimated_effort: 2 hours
actual_effort: 2 hours
complexity_estimate: 3
complexity_actual: 1
previous_state: in_review
state_transition_reason: "Task completion: All acceptance criteria met, quality gates passed"
completed_location: tasks/completed/TASK-028/
organized_files:
  - TASK-028.md
  - implementation-summary.md
  - completion-report.md

# Quality Gates (Final)
tests_passed: 139/139 (100%)
compilation: success
architectural_review: 85/100 (APPROVED)
code_review: APPROVED
coverage_estimate: 85-90%
all_acceptance_criteria: met
documentation: complete

# Source
source: implementation-plan-and-code-review-analysis.md
recommendation: SHOULD-HAVE - Optional Enhancement
research_support: Hubbard's workflow (review Plan.md before execution)
alignment: Improves human decision-making at checkpoint

# Requirements
requirements:
  - REQ-CHECKPOINT-001: Display plan summary in Phase 2.8 checkpoint
  - REQ-CHECKPOINT-002: Show files to be created/modified
  - REQ-CHECKPOINT-003: Show dependencies to be added
  - REQ-CHECKPOINT-004: Show estimated effort (LOC, duration)
  - REQ-CHECKPOINT-005: Show key risks with mitigations
  - REQ-CHECKPOINT-006: Show link to full plan file
---

# Enhance Phase 2.8 Checkpoint Display with Plan Summary

## Problem Statement

**Current Phase 2.8 checkpoint** shows:
```
═══════════════════════════════════════════════════════
🔍 PHASE 2.8 - HUMAN CHECKPOINT REQUIRED
═══════════════════════════════════════════════════════

COMPLEXITY EVALUATION (Phase 2.7):
  Score: 8/10 (FULL_REQUIRED)
  Triggers: schema_changes, breaking_changes

ARCHITECTURAL REVIEW (Phase 2.5B):
  Score: 72/100 (Acceptable with recommendations)
  Issues: 3 warnings

OPTIONS:
1. [A]pprove - Proceed with current design
2. [R]evise - Apply recommendations and re-review
3. [V]iew - Show full architectural review report
4. [C]omplexity - Show detailed complexity breakdown
5. [D]iscuss - Escalate to software-architect

Your choice (A/R/V/C/D): _
```

**What's missing**: The **implementation plan details** that help human make an informed decision.

**Hubbard's workflow**: "Plan (write this as a .md file, save in plans/ directory)"
- Implies human **reviews the plan** before proceeding to execution
- Current checkpoint doesn't show what will be implemented

**Problem**: Human must choose [V]iew to see full report, interrupting flow. Better to show **plan summary inline** for quick decision-making.

## Solution Overview

Enhance Phase 2.8 checkpoint to include **implementation plan summary**:

**Enhanced checkpoint**:
```
═══════════════════════════════════════════════════════
🔍 PHASE 2.8 - HUMAN CHECKPOINT REQUIRED
═══════════════════════════════════════════════════════

TASK: TASK-042 - Implement JWT authentication

IMPLEMENTATION PLAN SUMMARY:
  Files: 5 files to create
    • src/auth/AuthService.ts - Main authentication service
    • src/auth/TokenManager.ts - JWT token creation/validation
    • tests/unit/AuthService.test.ts - Unit tests for AuthService
    • tests/integration/auth.test.ts - Integration tests
    • docs/api/authentication.md - API documentation

  Dependencies: 2 new
    • jsonwebtoken ^9.0.0 - JWT token handling
    • bcrypt ^5.1.0 - Password hashing

  Estimated Effort:
    • Duration: 4 hours
    • Lines of Code: 245

  Key Risks:
    🔴 JWT secret management (HIGH)
       → Mitigation: Use environment variables
    🟡 Token expiration handling (MEDIUM)
       → Mitigation: Implement refresh token mechanism

COMPLEXITY EVALUATION:
  Score: 7/10 (Complex - Review Required)
  Triggers: security_keywords (auth, password)

ARCHITECTURAL REVIEW:
  Score: 85/100 (Good)
  Issues: 1 warning
    ⚠️ Consider extracting validation logic into separate class

PLAN FILE:
  Location: docs/state/TASK-042/implementation_plan.md
  View: cat docs/state/TASK-042/implementation_plan.md

OPTIONS:
1. [A]pprove - Proceed with this plan
2. [V]iew - Show full plan and review details
3. [C]omplexity - Show detailed complexity breakdown
4. [D]iscuss - Escalate to software-architect
5. [R]evise - Apply recommendations and re-plan

Your choice (A/V/C/D/R): _
```

**Benefits**:
- ✅ Human sees **what will be implemented** at a glance
- ✅ Matches Hubbard's "review plan" step
- ✅ Informed decision without interruption
- ✅ Key risks visible upfront
- ✅ Link to full plan if more detail needed

## Acceptance Criteria

### 1. Plan Summary Extraction
Extract plan summary from saved implementation plan:

```python
# installer/global/commands/lib/checkpoint_display.py

from pathlib import Path
from typing import Dict, Any, Optional

def load_plan_summary(task_id: str) -> Optional[Dict[str, Any]]:
    """Load plan summary for checkpoint display."""
    from .plan_persistence import load_plan

    plan = load_plan(task_id)
    if not plan:
        return None

    return {
        'files_to_create': plan['plan'].get('files_to_create', []),
        'files_to_modify': plan['plan'].get('files_to_modify', []),
        'dependencies': plan['plan'].get('external_dependencies', []),
        'estimated_duration': plan['plan'].get('estimated_duration'),
        'estimated_loc': plan['plan'].get('estimated_loc'),
        'risks': plan['plan'].get('risks', [])[:3],  # Top 3 risks only
        'plan_path': f"docs/state/{task_id}/implementation_plan.md"
    }
```

Acceptance criteria:
- [ ] Extract files to create (with descriptions)
- [ ] Extract files to modify (if any)
- [ ] Extract dependencies (name, version, purpose)
- [ ] Extract estimated effort (duration, LOC)
- [ ] Extract top 3 risks (prioritize by severity)
- [ ] Include plan file path

### 2. Format Plan Summary for Display
Create human-readable format:

```python
def format_plan_summary(summary: Dict[str, Any]) -> str:
    """Format plan summary for checkpoint display."""
    lines = [
        "IMPLEMENTATION PLAN SUMMARY:",
        f"  Files: {len(summary['files_to_create'])} files to create"
    ]

    # Show first 5 files (truncate if more)
    files = summary['files_to_create'][:5]
    for file_info in files:
        if isinstance(file_info, dict):
            path = file_info.get('path', file_info)
            desc = file_info.get('description', '')
            lines.append(f"    • {path} - {desc}")
        else:
            lines.append(f"    • {file_info}")

    if len(summary['files_to_create']) > 5:
        remaining = len(summary['files_to_create']) - 5
        lines.append(f"    ... and {remaining} more files")

    # Dependencies
    if summary['dependencies']:
        lines.append("")
        lines.append(f"  Dependencies: {len(summary['dependencies'])} new")
        for dep in summary['dependencies'][:3]:
            if isinstance(dep, dict):
                name = dep.get('name', dep)
                version = dep.get('version', '')
                purpose = dep.get('purpose', '')
                lines.append(f"    • {name} {version} - {purpose}")
            else:
                lines.append(f"    • {dep}")

    # Estimated effort
    lines.append("")
    lines.append("  Estimated Effort:")
    if summary['estimated_duration']:
        lines.append(f"    • Duration: {summary['estimated_duration']}")
    if summary['estimated_loc']:
        lines.append(f"    • Lines of Code: {summary['estimated_loc']}")

    # Key risks
    if summary['risks']:
        lines.append("")
        lines.append("  Key Risks:")
        for risk in summary['risks']:
            severity = risk.get('severity', 'MEDIUM').upper()
            icon = '🔴' if severity == 'HIGH' else '🟡' if severity == 'MEDIUM' else '🟢'
            desc = risk.get('description', risk)
            mitigation = risk.get('mitigation', '')
            lines.append(f"    {icon} {desc} ({severity})")
            if mitigation:
                lines.append(f"       → Mitigation: {mitigation}")

    return "\n".join(lines)
```

Acceptance criteria:
- [ ] Format files list (show first 5, truncate rest)
- [ ] Format dependencies (show first 3)
- [ ] Format estimated effort (duration, LOC)
- [ ] Format risks (with severity icons, mitigations)
- [ ] Truncate long lists with "... and N more"
- [ ] Clean, readable alignment

### 3. Update Phase 2.8 Checkpoint Display
Integrate plan summary into checkpoint:

```python
# In task-work.md Phase 2.8 execution

def display_phase_2_8_checkpoint(task_id: str, complexity_result, review_result):
    """Display enhanced Phase 2.8 checkpoint with plan summary."""

    # Load plan summary
    plan_summary = load_plan_summary(task_id)

    print("═" * 60)
    print("🔍 PHASE 2.8 - HUMAN CHECKPOINT REQUIRED")
    print("═" * 60)
    print()
    print(f"TASK: {task_id} - {task_title}")
    print()

    # NEW: Display plan summary
    if plan_summary:
        print(format_plan_summary(plan_summary))
        print()

    # Existing: Complexity evaluation
    print("COMPLEXITY EVALUATION:")
    print(f"  Score: {complexity_result.score}/10 ({complexity_result.level})")
    if complexity_result.triggers:
        print(f"  Triggers: {', '.join(complexity_result.triggers)}")
    print()

    # Existing: Architectural review
    print("ARCHITECTURAL REVIEW:")
    print(f"  Score: {review_result.score}/100 ({review_result.status})")
    if review_result.issues:
        print(f"  Issues: {len(review_result.issues)} warning(s)")
        for issue in review_result.issues[:3]:
            print(f"    ⚠️ {issue}")
    print()

    # NEW: Plan file link
    if plan_summary:
        print("PLAN FILE:")
        print(f"  Location: {plan_summary['plan_path']}")
        print(f"  View: cat {plan_summary['plan_path']}")
        print()

    # Options
    print("OPTIONS:")
    print("1. [A]pprove - Proceed with this plan")
    print("2. [V]iew - Show full plan and review details")
    print("3. [C]omplexity - Show detailed complexity breakdown")
    print("4. [D]iscuss - Escalate to software-architect")
    print("5. [R]evise - Apply recommendations and re-plan")
    print()
    print("Your choice (A/V/C/D/R): ", end="")
```

Acceptance criteria:
- [ ] Plan summary displayed before complexity/review
- [ ] Formatted cleanly with proper spacing
- [ ] Plan file link shown
- [ ] Works for markdown plans (TASK-027)
- [ ] Works for legacy JSON plans
- [ ] Gracefully handles missing plan (skip summary section)

### 4. Conditional Display Logic
Only show plan summary for tasks with plans:

```python
def should_show_plan_summary(task_id: str) -> bool:
    """Check if plan summary should be displayed."""
    from .plan_persistence import plan_exists
    return plan_exists(task_id)
```

Acceptance criteria:
- [ ] Check if plan exists before loading
- [ ] Skip plan summary section if no plan
- [ ] No errors if plan file missing
- [ ] Log warning if plan expected but missing

### 5. Integration with TASK-027
Works with markdown plans once TASK-027 is complete:

```python
# After TASK-027:
# Plan path will be: docs/state/TASK-042/implementation_plan.md
# Parser will extract sections from markdown
# Summary display works identically
```

Acceptance criteria:
- [ ] Compatible with markdown plan format
- [ ] Parses frontmatter metadata
- [ ] Extracts sections correctly
- [ ] Plan file link points to .md file

### 6. Update Documentation
Document enhanced checkpoint:

- [ ] Update `task-work.md` with enhanced Phase 2.8 format
- [ ] Add examples to docs
- [ ] Update CLAUDE.md with checkpoint description
- [ ] Add screenshots/examples to workflow docs

## Implementation Plan

### Step 1: Create Checkpoint Display Module (30 min)
File: `installer/global/commands/lib/checkpoint_display.py`

Functions:
- `load_plan_summary(task_id)` - Extract plan summary
- `format_plan_summary(summary)` - Format for display
- `format_file_list(files, max_items)` - Format file list
- `format_dependency_list(deps, max_items)` - Format dependencies
- `format_risk_list(risks)` - Format risks with icons

### Step 2: Update Phase 2.8 Display Logic (1 hour)
File: `installer/global/commands/task-work.md`

Modify Phase 2.8 checkpoint section:
- Add plan summary loading
- Add plan summary formatting
- Add plan file link
- Test with and without plan

### Step 3: Testing (30 min)
- Test with tasks that have plans
- Test with tasks without plans
- Test with truncated file lists (>5 files)
- Test with multiple dependencies
- Test with high/medium/low risk items

### Step 4: Documentation (15 min)
- Update task-work.md examples
- Add to workflow documentation

## Testing Strategy

### Unit Tests
- [ ] `test_checkpoint_display.py`: Test formatting functions
- [ ] `test_plan_summary_loading.py`: Test plan extraction

### Integration Tests
- [ ] `test_phase_2_8_with_plan.py`: Checkpoint with plan summary
- [ ] `test_phase_2_8_without_plan.py`: Checkpoint without plan
- [ ] `test_truncation.py`: Long file lists truncate correctly

### E2E Tests
- [ ] Create task with plan
- [ ] Trigger Phase 2.8 checkpoint (complexity 7+)
- [ ] Verify plan summary displayed
- [ ] Verify plan file link shown
- [ ] Verify human can view full plan

## Benefits

### Immediate
- ✅ Human sees what will be implemented upfront
- ✅ Informed decision without breaking flow
- ✅ Matches Hubbard's "review plan" step
- ✅ Key risks visible at decision point

### Long-term
- ✅ Better human-in-the-loop experience
- ✅ Fewer surprises during implementation
- ✅ More thoughtful approval decisions
- ✅ Faster checkpoint review (no need for [V]iew)

## Dependencies

- Prerequisite: Current Phase 2.8 checkpoint implementation
- Recommended: TASK-027 (markdown plans make this nicer)
- Enables: Better human decision-making

## Success Metrics

After 30 days:
- [ ] 80%+ of checkpoint decisions made without [V]iew option
- [ ] Positive user feedback on plan summary usefulness
- [ ] Faster average checkpoint decision time
- [ ] No regression in checkpoint quality

## Related Tasks

- TASK-027: Markdown plans (makes plan file link nicer)
- TASK-029: Add "Modify" option to checkpoint (larger enhancement)
- Phase 2.8: Current checkpoint implementation

## Notes

**This is an optional enhancement.** Current checkpoint works fine, this just makes it better.

**Priority**: Low (nice-to-have, not critical)

**When to implement**: After TASK-025, TASK-026, TASK-027 are complete and working well.

**Quick win**: The plan file link (15 minutes) could be done separately from full summary.
