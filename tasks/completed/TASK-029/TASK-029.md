---
id: TASK-029
title: Add "Modify Plan" Option to Phase 2.8 Checkpoint
status: completed
priority: low
created: 2025-10-18T12:15:00Z
updated: 2025-10-18T23:20:00Z
completed_at: 2025-10-18T23:20:00Z
labels: [enhancement, ux-improvement, optional, interactive]
estimated_effort: 5 hours
actual_effort: 6.5 hours
complexity_estimate: 6
complexity_actual: 4
previous_state: in_review
state_transition_reason: "Task successfully completed - all quality gates passed"
completed_location: tasks/completed/TASK-029/
organized_files: [
  "TASK-029.md",
  "implementation-summary.md",
  "coverage-report.json",
  "test-summary.txt"
]

# Implementation Results
test_results:
  compilation: passed (100%)
  tests_passing: 45/46 (98%)
  core_logic_coverage: 95%
  overall_coverage: 57%
  code_quality_score: 9.1/10

architectural_review:
  score: 82/100
  solid_compliance: 88%
  dry_compliance: 88%
  yagni_compliance: 64%

files_created:
  - installer/global/commands/lib/plan_modifier.py (1,103 lines)
  - tests/unit/test_plan_modifier.py (46 tests)
  - tests/integration/test_plan_modification_flow.py (10 tests)
  - installer/global/commands/lib/README-PLAN-MODIFIER.md

files_modified:
  - installer/global/commands/lib/plan_persistence.py (+111 lines)
  - installer/global/commands/lib/checkpoint_display.py (+88 lines)

# Source
source: implementation-plan-and-code-review-analysis.md
recommendation: SHOULD-HAVE - Optional Enhancement
research_support: Iterative refinement (Fowler), human control (Hubbard)
alignment: Enables plan tweaking without full re-plan

# Requirements
requirements:
  - REQ-MODIFY-001: Add [M]odify option to Phase 2.8 checkpoint
  - REQ-MODIFY-002: Allow interactive editing of plan elements
  - REQ-MODIFY-003: Support adding/removing files
  - REQ-MODIFY-004: Support adjusting dependencies
  - REQ-MODIFY-005: Support updating risks/mitigations
  - REQ-MODIFY-006: Re-run architectural review after modifications
  - REQ-MODIFY-007: Save modified plan with version tracking
---

# Add "Modify Plan" Option to Phase 2.8 Checkpoint

## Problem Statement

**Current Phase 2.8 checkpoint options**:
```
OPTIONS:
1. [A]pprove - Proceed with current design
2. [R]evise - Apply recommendations and re-review
3. [V]iew - Show full architectural review report
4. [C]omplexity - Show detailed complexity breakdown
5. [D]iscuss - Escalate to software-architect

Your choice (A/R/V/C/D): _
```

**Problem**: Human can only **approve** or **revise** (full re-plan).

**Scenario**: Human reviews plan and thinks:
- "This looks good, but we should also create a SessionStore file"
- "We don't need the API documentation file yet"
- "The lodash dependency isn't necessary, remove it"

**Current workflow**:
1. Choose [R]evise
2. Loop back to Phase 2 (full re-planning)
3. AI re-generates entire plan
4. Human reviews again
5. Repeat until satisfied

**Issue**: **Heavy workflow** for minor tweaks. Wastes time re-planning when only small changes needed.

**Research support**:
- **Fowler**: "Small, iterative steps" (not full re-planning for minor changes)
- **Hubbard**: Human should control the plan (not just approve/reject)

## Solution Overview

Add **[M]odify option** to Phase 2.8 checkpoint for **interactive plan editing**:

**Enhanced checkpoint**:
```
OPTIONS:
1. [A]pprove - Proceed with this plan
2. [M]odify - Edit plan interactively ← NEW
3. [V]iew - Show full plan and review details
4. [C]omplexity - Show detailed complexity breakdown
5. [D]iscuss - Escalate to software-architect
6. [R]evise - Apply recommendations and re-plan

Your choice (A/M/V/C/D/R): _
```

**Modify workflow**:
```
Human chooses [M]odify

MODIFY PLAN - TASK-042

What would you like to change?
1. Add/remove files
2. Adjust dependencies
3. Change complexity estimate
4. Update risks/mitigations
5. Edit architectural approach
6. Custom edit (manual)
7. Done (finish modifications)

Your choice (1-7): 1

FILES TO CREATE (current: 5 files)
  1. src/auth/AuthService.ts - Main authentication service
  2. src/auth/TokenManager.ts - JWT token creation/validation
  3. tests/unit/AuthService.test.ts - Unit tests
  4. tests/integration/auth.test.ts - Integration tests
  5. docs/api/authentication.md - API documentation

Action: [A]dd file, [R]emove file, [D]one: A

File path: src/auth/SessionStore.ts
Purpose/Description: Manage user sessions separate from tokens

FILE ADDED: src/auth/SessionStore.ts

Files to create: 6 (was 5)

Action: [A]dd file, [R]emove file, [D]one: R

File number to remove: 5
REMOVED: docs/api/authentication.md

Files to create: 5 (was 6)

Action: [A]dd file, [R]emove file, [D]one: D

[Plan updated, re-running architectural review...]

ARCHITECTURAL REVIEW (Updated):
  Score: 83/100 (was 85/100)
  Changes: -2 points (added file without interface definition)
  Recommendation: Consider adding ISessionStore interface

[M]odify more, [A]pprove, or [C]ancel: A

Plan approved with modifications.
Proceeding to Phase 3 (Implementation)...
```

**Benefits**:
- ✅ Human can **tweak plan** without full re-plan
- ✅ Faster than [R]evise for minor changes
- ✅ Maintains human control over plan
- ✅ Re-validates architecture after changes
- ✅ Iterative refinement (Fowler's principle)

## Acceptance Criteria

### 1. Add [M]odify Option to Checkpoint
Update Phase 2.8 options:

```python
# In Phase 2.8 checkpoint display
print("OPTIONS:")
print("1. [A]pprove - Proceed with this plan")
print("2. [M]odify - Edit plan interactively")  # NEW
print("3. [V]iew - Show full plan and review details")
print("4. [C]omplexity - Show detailed complexity breakdown")
print("5. [D]iscuss - Escalate to software-architect")
print("6. [R]evise - Apply recommendations and re-plan")
print()
print("Your choice (A/M/V/C/D/R): ", end="")
```

Acceptance criteria:
- [ ] [M]odify option added
- [ ] Help text clear
- [ ] Option number adjusted (2 for Modify)

### 2. Modify Plan Menu
Interactive menu for plan modifications:

```python
# installer/global/commands/lib/plan_modifier.py

def modify_plan_interactive(task_id: str, plan: Dict[str, Any]) -> Dict[str, Any]:
    """Interactive plan modification menu."""

    modified_plan = plan.copy()

    while True:
        print("\nMODIFY PLAN - " + task_id)
        print("\nWhat would you like to change?")
        print("1. Add/remove files")
        print("2. Adjust dependencies")
        print("3. Change complexity estimate")
        print("4. Update risks/mitigations")
        print("5. Edit architectural approach")
        print("6. Custom edit (open in editor)")
        print("7. Done (finish modifications)")
        print()

        choice = input("Your choice (1-7): ").strip()

        if choice == "1":
            modified_plan = modify_files(modified_plan)
        elif choice == "2":
            modified_plan = modify_dependencies(modified_plan)
        elif choice == "3":
            modified_plan = modify_complexity(modified_plan)
        elif choice == "4":
            modified_plan = modify_risks(modified_plan)
        elif choice == "5":
            modified_plan = modify_architecture(modified_plan)
        elif choice == "6":
            modified_plan = custom_edit(modified_plan, task_id)
        elif choice == "7":
            break
        else:
            print("Invalid choice. Try again.")

    return modified_plan
```

Acceptance criteria:
- [ ] Menu displays current modification count
- [ ] All 7 options implemented
- [ ] Loop continues until [D]one
- [ ] Clear feedback after each modification
- [ ] Can abort modifications (Ctrl+C or [C]ancel)

### 3. Modify Files Function
Add/remove files interactively:

```python
def modify_files(plan: Dict[str, Any]) -> Dict[str, Any]:
    """Interactively add/remove files from plan."""

    files = plan['plan']['files_to_create']

    print(f"\nFILES TO CREATE (current: {len(files)} files)")
    for i, file_info in enumerate(files, 1):
        if isinstance(file_info, dict):
            print(f"  {i}. {file_info['path']} - {file_info['description']}")
        else:
            print(f"  {i}. {file_info}")

    while True:
        action = input("\nAction: [A]dd file, [R]emove file, [D]one: ").strip().upper()

        if action == "A":
            path = input("File path: ").strip()
            desc = input("Purpose/Description: ").strip()
            files.append({'path': path, 'description': desc})
            print(f"FILE ADDED: {path}")
            print(f"Files to create: {len(files)}")

        elif action == "R":
            num = int(input("File number to remove: ").strip())
            if 1 <= num <= len(files):
                removed = files.pop(num - 1)
                removed_path = removed['path'] if isinstance(removed, dict) else removed
                print(f"REMOVED: {removed_path}")
                print(f"Files to create: {len(files)}")
            else:
                print("Invalid file number")

        elif action == "D":
            break

        else:
            print("Invalid action")

    plan['plan']['files_to_create'] = files
    return plan
```

Acceptance criteria:
- [ ] Display current files with numbers
- [ ] Add file: prompt for path and description
- [ ] Remove file: prompt for file number
- [ ] Validate file number in range
- [ ] Show count after each change
- [ ] Return modified plan

### 4. Modify Dependencies Function
Adjust project dependencies:

```python
def modify_dependencies(plan: Dict[str, Any]) -> Dict[str, Any]:
    """Interactively add/remove dependencies."""

    deps = plan['plan']['external_dependencies']

    print(f"\nDEPENDENCIES (current: {len(deps)})")
    for i, dep in enumerate(deps, 1):
        if isinstance(dep, dict):
            print(f"  {i}. {dep['name']} {dep['version']} - {dep['purpose']}")
        else:
            print(f"  {i}. {dep}")

    while True:
        action = input("\nAction: [A]dd dependency, [R]emove dependency, [D]one: ").strip().upper()

        if action == "A":
            name = input("Package name: ").strip()
            version = input("Version (e.g., ^9.0.0): ").strip()
            purpose = input("Purpose: ").strip()
            deps.append({'name': name, 'version': version, 'purpose': purpose})
            print(f"ADDED: {name} {version}")

        elif action == "R":
            num = int(input("Dependency number to remove: ").strip())
            if 1 <= num <= len(deps):
                removed = deps.pop(num - 1)
                removed_name = removed['name'] if isinstance(removed, dict) else removed
                print(f"REMOVED: {removed_name}")
            else:
                print("Invalid number")

        elif action == "D":
            break

    plan['plan']['external_dependencies'] = deps
    return plan
```

Acceptance criteria:
- [ ] Display current dependencies
- [ ] Add dependency: prompt for name, version, purpose
- [ ] Remove dependency: prompt for number
- [ ] Validate dependency number
- [ ] Return modified plan

### 5. Modify Risks Function
Update risks and mitigations:

```python
def modify_risks(plan: Dict[str, Any]) -> Dict[str, Any]:
    """Interactively add/remove/edit risks."""

    risks = plan['plan']['risks']

    print(f"\nRISKS (current: {len(risks)})")
    for i, risk in enumerate(risks, 1):
        severity = risk.get('severity', 'MEDIUM')
        desc = risk.get('description', risk)
        mitigation = risk.get('mitigation', 'None')
        print(f"  {i}. [{severity}] {desc}")
        print(f"      → {mitigation}")

    while True:
        action = input("\nAction: [A]dd risk, [R]emove risk, [E]dit risk, [D]one: ").strip().upper()

        if action == "A":
            desc = input("Risk description: ").strip()
            severity = input("Severity (LOW/MEDIUM/HIGH): ").strip().upper()
            mitigation = input("Mitigation strategy: ").strip()
            risks.append({
                'description': desc,
                'severity': severity,
                'mitigation': mitigation
            })
            print(f"ADDED: {desc}")

        elif action == "R":
            num = int(input("Risk number to remove: ").strip())
            if 1 <= num <= len(risks):
                removed = risks.pop(num - 1)
                print(f"REMOVED: {removed['description']}")

        elif action == "E":
            num = int(input("Risk number to edit: ").strip())
            if 1 <= num <= len(risks):
                risk = risks[num - 1]
                print(f"Current: {risk['description']}")
                new_desc = input(f"New description (or press Enter to keep): ").strip()
                if new_desc:
                    risk['description'] = new_desc
                new_mitigation = input(f"New mitigation (or press Enter to keep): ").strip()
                if new_mitigation:
                    risk['mitigation'] = new_mitigation
                print("Risk updated")

        elif action == "D":
            break

    plan['plan']['risks'] = risks
    return plan
```

Acceptance criteria:
- [ ] Display current risks with severity and mitigation
- [ ] Add risk: prompt for description, severity, mitigation
- [ ] Remove risk: prompt for number
- [ ] Edit risk: update description or mitigation
- [ ] Return modified plan

### 6. Re-run Architectural Review After Modifications
Validate modified plan:

```python
def finalize_modifications(task_id: str, original_plan: Dict, modified_plan: Dict) -> Dict:
    """Re-run architectural review on modified plan."""

    # Calculate changes
    changes = calculate_plan_changes(original_plan, modified_plan)

    print("\n[Plan updated, re-running architectural review...]")
    print()

    # Re-run architectural review
    from .architectural_review import run_architectural_review
    review_result = run_architectural_review(modified_plan)

    # Display updated review
    print("ARCHITECTURAL REVIEW (Updated):")
    print(f"  Score: {review_result.score}/100 (was {original_review.score}/100)")

    if review_result.score != original_review.score:
        delta = review_result.score - original_review.score
        sign = "+" if delta > 0 else ""
        print(f"  Changes: {sign}{delta} points")

    if review_result.warnings:
        print(f"  Warnings: {len(review_result.warnings)} issue(s)")
        for warning in review_result.warnings[:3]:
            print(f"    ⚠️ {warning}")

    print()

    # Prompt for final decision
    choice = input("[M]odify more, [A]pprove, or [C]ancel: ").strip().upper()

    if choice == "M":
        return None  # Continue modifying
    elif choice == "A":
        return modified_plan  # Approve modifications
    else:
        return original_plan  # Cancel, use original
```

Acceptance criteria:
- [ ] Calculate plan changes (files added/removed, deps changed)
- [ ] Re-run architectural review on modified plan
- [ ] Display updated score and delta
- [ ] Show new warnings (if any)
- [ ] Prompt: [M]odify more, [A]pprove, [C]ancel
- [ ] Return appropriate plan based on choice

### 7. Save Modified Plan with Version Tracking
Track modification history:

```python
def save_modified_plan(task_id: str, plan: Dict, modification_reason: str = "human_checkpoint"):
    """Save modified plan with version increment."""

    from .plan_persistence import save_plan

    # Increment version
    current_version = plan.get('version', 1)
    plan['version'] = current_version + 1
    plan['modified_at'] = datetime.now().isoformat()
    plan['modification_reason'] = modification_reason

    # Save updated plan
    plan_path = save_plan(task_id, plan['plan'], plan.get('architectural_review'))

    # Update task metadata
    update_task_metadata(task_id, {
        'plan_version': plan['version'],
        'plan_modified_at': plan['modified_at'],
        'plan_modifications': plan.get('modifications', 0) + 1
    })

    return plan_path
```

Acceptance criteria:
- [ ] Increment plan version
- [ ] Add modification timestamp
- [ ] Add modification reason
- [ ] Save to same location (overwrite)
- [ ] Update task metadata with version count
- [ ] Optionally save version history

### 8. Integration with Phase 2.8
Wire up [M]odify option:

```python
# In Phase 2.8 checkpoint handling

if user_choice == "M":
    # Load current plan
    from .plan_persistence import load_plan
    plan = load_plan(task_id)

    # Interactive modification
    from .plan_modifier import modify_plan_interactive, finalize_modifications
    modified_plan = modify_plan_interactive(task_id, plan)

    # Re-validate and finalize
    final_plan = finalize_modifications(task_id, plan, modified_plan)

    if final_plan == plan:
        # Cancelled, continue checkpoint
        continue_checkpoint()
    else:
        # Approved, save and proceed
        save_modified_plan(task_id, final_plan, "checkpoint_modification")
        proceed_to_phase_3()
```

Acceptance criteria:
- [ ] [M]odify triggers interactive modification
- [ ] Modified plan saved if approved
- [ ] Can cancel and return to checkpoint
- [ ] Can approve and proceed to Phase 3
- [ ] Plan version tracked in metadata

### 9. Documentation
- [ ] Update `task-work.md` with [M]odify option
- [ ] Add examples of plan modifications
- [ ] Document modification workflow
- [ ] Update CLAUDE.md with modify option

## Implementation Plan

### Step 1: Create Plan Modifier Module (2 hours)
File: `installer/global/commands/lib/plan_modifier.py`

Functions:
- `modify_plan_interactive()` - Main menu loop
- `modify_files()` - Add/remove files
- `modify_dependencies()` - Adjust dependencies
- `modify_risks()` - Update risks
- `finalize_modifications()` - Re-review and approve

### Step 2: Integrate with Phase 2.8 (1 hour)
Update `task-work.md` Phase 2.8 checkpoint:
- Add [M]odify option
- Wire up modification workflow
- Handle approve/cancel paths

### Step 3: Plan Version Tracking (1 hour)
Update `plan_persistence.py`:
- Track plan versions
- Save modification metadata
- Optional: Version history

### Step 4: Testing (1 hour)
- Test file modifications
- Test dependency modifications
- Test risk modifications
- Test architectural re-review
- Test approve/cancel paths

### Step 5: Documentation (30 min)
Update docs with modification workflow examples.

## Testing Strategy

### Unit Tests
- [ ] `test_plan_modifier.py`: Test modification functions
- [ ] `test_version_tracking.py`: Test version increments

### Integration Tests
- [ ] `test_modify_workflow.py`: End-to-end modification
- [ ] `test_checkpoint_modify_option.py`: Integration with Phase 2.8

### E2E Tests
- [ ] Trigger Phase 2.8 checkpoint
- [ ] Choose [M]odify
- [ ] Add files, change deps
- [ ] Re-review shows updated score
- [ ] Approve modifications
- [ ] Verify plan saved with new version

## Benefits

### Immediate
- ✅ Human can tweak plan without full re-plan
- ✅ Faster than [R]evise for minor changes
- ✅ Maintains human control over implementation
- ✅ Iterative refinement (small steps)

### Long-term
- ✅ Better human-AI collaboration
- ✅ Less frustration with checkpoint process
- ✅ More thoughtful plan adjustments
- ✅ Tracks plan evolution (version history)

## Dependencies

- Prerequisite: Current Phase 2.8 checkpoint
- Prerequisite: Plan persistence module
- Recommended: TASK-027 (markdown plans)
- Recommended: TASK-028 (plan summary display)

## Success Metrics

After 30 days:
- [ ] 20-30% of checkpoints use [M]odify option
- [ ] Average modifications per plan: 1-2
- [ ] Positive user feedback on modification UX
- [ ] Faster than [R]evise for minor tweaks

## Related Tasks

- TASK-027: Markdown plans (makes version tracking easier)
- TASK-028: Plan summary display (shows what's being modified)
- TASK-026: Task refine (similar interactive editing, different phase)

## Notes

**This is an optional enhancement.** Current checkpoint works, this adds flexibility.

**Priority**: Low (nice-to-have, larger effort)

**When to implement**: After TASK-025, TASK-026, TASK-027, TASK-028 are complete and working.

**Alternative**: Could build this as part of TASK-026 (refinement), since concepts overlap.
