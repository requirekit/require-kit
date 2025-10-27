---
id: TASK-003B-3
title: Modification & View Modes - Plan Editing and Versioning
status: completed
created: 2025-10-09T16:40:00Z
updated: 2025-10-09T18:45:00Z
completed: 2025-10-09T18:45:00Z
assignee: null
priority: medium
tags: [workflow-enhancement, plan-modification, versioning, interactive-editing, phase-2.8]
requirements: []
bdd_scenarios: []
parent_task: TASK-003B
dependencies: [TASK-003B-2]
blocks: []
test_results:
  status: passed
  last_run: 2025-10-09T18:30:00Z
  coverage: 93.7%
  passed: 143
  failed: 0
  execution_log: "All TASK-003B-3 tests passing. Coverage: 93.7% (exceeds 80% target)"
blocked_reason: null
---

# TASK-003B-3: Modification & View Modes

## Parent Context

This is **Sub-Task 3 of 4** for TASK-003B (Review Modes & User Interaction).

**Parent Task**: TASK-003B - Review Modes & User Interaction
**Depends On**: TASK-003B-2 (full review mode - action target)
**Blocks**: None (enhancement feature)
**Parallel**: Can work in parallel with TASK-003B-4 (Q&A mode)

## Description

Implement **[M]odify** and **[V]iew** handlers for full review mode. These features allow users to:

1. **[M]odify Mode**: Interactively edit implementation plans
   - Add/remove/edit files in the plan
   - Adjust test strategy
   - Modify implementation order
   - Recalculate complexity after changes
   - Generate new version of plan (v1 → v2)

2. **[V]iew Mode**: Display complete implementation plan
   - Show full plan in pager (less/more)
   - Support scrolling and search
   - Syntax highlighting for markdown
   - Return to checkpoint after viewing

**Key Innovation**: Plan versioning with complexity recalculation enables iterative refinement without losing history.

## Acceptance Criteria

### Phase 1: [V]iew Handler ✅ MUST HAVE

- [ ] **Plan Display in Pager**
  - [ ] Detect if plan file exists
  - [ ] Use system pager (less preferred, fall back to more)
  - [ ] Pass plan file to pager
  - [ ] Support scrolling (up/down, page up/down)
  - [ ] Support search (/ in less)
  - [ ] Restore terminal state after pager exits

- [ ] **Cross-Platform Support**
  - [ ] Unix/Linux: Use `less -R` (preserve colors)
  - [ ] macOS: Use `less -R`
  - [ ] Windows: Use `more` or built-in pager
  - [ ] Fallback: Print to stdout if no pager available

- [ ] **Post-View Behavior**
  - [ ] Return to full review checkpoint
  - [ ] Display "Press any key to return to checkpoint..."
  - [ ] Re-display decision prompt
  - [ ] Track view action in metadata

### Phase 2: [M]odify Mode Entry ✅ MUST HAVE

- [ ] **Modification Mode Display**
  - [ ] Clear display of current plan summary
  - [ ] List of modifiable sections:
    ```
    PLAN MODIFICATION MODE

    Current Plan: TASK-XXX-implementation-plan.md (v1)
    Complexity: 8/10 (Complex)

    EDITABLE SECTIONS:
      [1] Files (3 new, 2 modified)
      [2] Tests (8 planned)
      [3] Dependencies (1 new)
      [4] Implementation Order (5 steps)
      [5] Done (save changes and recalculate)

    Select section to modify (1-5):
    ```

- [ ] **Section Navigation**
  - [ ] Accept numeric input (1-5)
  - [ ] Display selected section for editing
  - [ ] Allow return to section list
  - [ ] Track modification state (unsaved changes)

### Phase 3: File Section Modification ✅ MUST HAVE

- [ ] **File List Display**
  - [ ] Show numbered list of files:
    ```
    FILES SECTION

    NEW FILES:
      [1] src/auth/AuthService.ts (Purpose: Handle authentication)
      [2] src/auth/TokenService.ts (Purpose: JWT token management)
      [3] src/auth/AuthController.ts (Purpose: Auth API endpoints)

    MODIFIED FILES:
      [4] src/api/routes/index.ts (Changes: Add auth routes)
      [5] src/config/database.ts (Changes: Add user table)

    ACTIONS:
      [A] Add new file
      [R] Remove file (enter number)
      [E] Edit file (enter number)
      [B] Back to section list

    Your choice:
    ```

- [ ] **Add File Operation**
  - [ ] Prompt for file path
  - [ ] Validate path format (no spaces, valid extension)
  - [ ] Prompt for file purpose/changes
  - [ ] Prompt for file type (new/modified)
  - [ ] Add to plan
  - [ ] Mark plan as modified

- [ ] **Remove File Operation**
  - [ ] Prompt for file number
  - [ ] Confirm removal
  - [ ] Remove from plan
  - [ ] Mark plan as modified

- [ ] **Edit File Operation**
  - [ ] Prompt for file number
  - [ ] Display current details
  - [ ] Prompt for new purpose/changes (keep if empty)
  - [ ] Update plan
  - [ ] Mark plan as modified

### Phase 4: Test Section Modification ✅ MUST HAVE

- [ ] **Test Strategy Display**
  - [ ] Show current test counts:
    ```
    TESTS SECTION

    Current Strategy:
      Unit Tests: 6
      Integration Tests: 2
      Total: 8 tests

    ACTIONS:
      [U] Update unit test count
      [I] Update integration test count
      [B] Back to section list

    Your choice:
    ```

- [ ] **Update Test Counts**
  - [ ] Prompt for new count
  - [ ] Validate (positive integer)
  - [ ] Update plan
  - [ ] Mark as modified

### Phase 5: Dependency Section Modification ✅ SHOULD HAVE

- [ ] **Dependency List Display**
  - [ ] Show numbered dependency list
  - [ ] Display package name and version

- [ ] **Add Dependency**
  - [ ] Prompt for package name
  - [ ] Prompt for version (optional, default: "latest")
  - [ ] Validate package name format
  - [ ] Add to plan

- [ ] **Remove Dependency**
  - [ ] Prompt for number
  - [ ] Confirm removal
  - [ ] Remove from plan

### Phase 6: Implementation Order Modification ✅ SHOULD HAVE

- [ ] **Step List Display**
  - [ ] Show numbered implementation steps
  - [ ] Display duration and dependencies

- [ ] **Reorder Steps**
  - [ ] Prompt for step number to move
  - [ ] Prompt for new position
  - [ ] Validate dependencies still satisfied
  - [ ] Reorder in plan

- [ ] **Edit Step**
  - [ ] Prompt for step number
  - [ ] Allow editing description and duration
  - [ ] Update plan

### Phase 7: Plan Regeneration & Recalculation ✅ MUST HAVE

- [ ] **Save Modifications**
  - [ ] User selects [5] Done
  - [ ] Display summary of changes:
    ```
    MODIFICATIONS SUMMARY:
      - Added 1 new file (src/auth/SessionService.ts)
      - Removed 1 file (src/auth/TokenService.ts)
      - Updated test count: 8 → 10

    Regenerating plan and recalculating complexity...
    ```

- [ ] **Complexity Recalculation**
  - [ ] Count files in modified plan
  - [ ] Recalculate file complexity factor
  - [ ] Recalculate other factors if affected
  - [ ] Calculate new total complexity score
  - [ ] Determine new review mode:
    - If score drops to 1-3: AUTO_PROCEED
    - If score drops to 4-6: QUICK_OPTIONAL
    - If score stays 7-10: FULL_REQUIRED

- [ ] **Display Complexity Change**
  - [ ] Show before/after comparison:
    ```
    ✅ Plan updated!

    Complexity Change:
      Before: 8/10 (Complex) → Full Review Required
      After:  6/10 (Medium) → Quick Optional Review

    The plan is now simpler! Review mode changed.
    ```

- [ ] **Version Increment**
  - [ ] Increment plan version: v1 → v2
  - [ ] Save new version: `TASK-XXX-implementation-plan-v2.md`
  - [ ] Preserve old version (v1)
  - [ ] Update task metadata with version history

### Phase 8: Version Management ✅ MUST HAVE

- [ ] **Version History Tracking**
  - [ ] Store version history in task metadata:
    ```yaml
    implementation_plan:
      file: "TASK-XXX-implementation-plan-v3.md"
      version: 3
      version_history:
        - version: 1
          created: "2025-10-09T10:00:00Z"
          reason: "Initial generation"
          complexity_before: null
          complexity_after: 8
        - version: 2
          created: "2025-10-09T10:15:00Z"
          reason: "User modified: Removed 1 file"
          complexity_before: 8
          complexity_after: 6
          modified_by: "user"
        - version: 3
          created: "2025-10-09T10:30:00Z"
          reason: "User modified: Added 2 tests"
          complexity_before: 6
          complexity_after: 7
          modified_by: "user"
    ```

- [ ] **Version File Naming**
  - [ ] v1: `TASK-XXX-implementation-plan.md` (no suffix)
  - [ ] v2: `TASK-XXX-implementation-plan-v2.md`
  - [ ] v3+: `TASK-XXX-implementation-plan-v3.md`, etc.

- [ ] **Version Comparison (Optional)**
  - [ ] Allow viewing previous versions
  - [ ] Display diff summary
  - [ ] Track version lineage

### Phase 9: Return to Checkpoint ✅ MUST HAVE

- [ ] **Post-Modification Flow**
  - [ ] After modification complete, return to full review
  - [ ] Display updated complexity score
  - [ ] If review mode changed:
    - Notify user of mode change
    - If now auto-proceed: Skip checkpoint, go to Phase 3
    - If now quick optional: Switch to quick review countdown
    - If still full required: Stay in full review
  - [ ] If review mode unchanged: Re-display checkpoint with updated data

## Technical Specifications

### Modification Manager

```python
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class ModificationSession:
    """Track modifications during session"""
    started_at: datetime
    files_added: List[str] = field(default_factory=list)
    files_removed: List[str] = field(default_factory=list)
    files_edited: List[str] = field(default_factory=list)
    tests_changed: Optional[dict] = None
    dependencies_changed: bool = False
    has_modifications: bool = False

class ModificationManager:
    """Manages interactive plan modification"""

    def __init__(self, plan: ImplementationPlan, task_id: str):
        self.plan = plan
        self.task_id = task_id
        self.session = ModificationSession(started_at=datetime.now())
        self.modified_plan = deepcopy(plan)

    def execute(self) -> ModifiedPlanResult:
        """Execute modification flow"""
        while True:
            self._display_section_list()
            choice = self._prompt_for_section()

            if choice == '1':
                self._modify_files_section()
            elif choice == '2':
                self._modify_tests_section()
            elif choice == '3':
                self._modify_dependencies_section()
            elif choice == '4':
                self._modify_implementation_order()
            elif choice == '5':  # Done
                if self.session.has_modifications:
                    return self._save_and_recalculate()
                else:
                    print("No modifications made.")
                    return None
            else:
                print(f"Invalid choice: '{choice}'")

    def _modify_files_section(self):
        """Interactive file modification"""
        while True:
            self._display_files()
            action = input("\nYour choice (A/R/E/B): ").strip().lower()

            if action == 'a':
                self._add_file()
            elif action == 'r':
                self._remove_file()
            elif action == 'e':
                self._edit_file()
            elif action == 'b':
                break
            else:
                print(f"Invalid action: '{action}'")

    def _add_file(self):
        """Add new file to plan"""
        path = input("Enter file path: ").strip()
        if not self._validate_file_path(path):
            print("Invalid file path format")
            return

        purpose = input("Enter file purpose: ").strip()
        file_type = input("New or Modified? (n/m): ").strip().lower()

        if file_type == 'n':
            self.modified_plan.files_to_create.append({
                'path': path,
                'purpose': purpose
            })
        else:
            self.modified_plan.files_to_modify.append({
                'path': path,
                'changes': purpose
            })

        self.session.files_added.append(path)
        self.session.has_modifications = True
        print(f"✅ Added {path}")

    def _save_and_recalculate(self) -> ModifiedPlanResult:
        """Save modifications and recalculate complexity"""
        print("\nRegenerating plan and recalculating complexity...")

        # Recalculate complexity
        new_score = self._recalculate_complexity()

        # Generate new plan version
        new_version = self._generate_new_version()

        # Display change summary
        self._display_complexity_change(new_score)

        return ModifiedPlanResult(
            new_plan=self.modified_plan,
            new_complexity_score=new_score,
            version=new_version,
            modifications=self.session
        )

    def _recalculate_complexity(self) -> ComplexityScore:
        """Recalculate complexity based on modified plan"""
        # Use existing calculator
        calculator = ComplexityCalculator()
        context = build_evaluation_context(
            task_id=self.task_id,
            plan=self.modified_plan
        )
        return calculator.calculate(context)
```

### Version Manager

```python
class VersionManager:
    """Manages plan versioning"""

    @staticmethod
    def increment_version(task_id: str, current_version: int) -> int:
        """Increment plan version and return new version number"""
        return current_version + 1

    @staticmethod
    def get_version_filename(task_id: str, version: int) -> str:
        """Get filename for given version"""
        if version == 1:
            return f"{task_id}-implementation-plan.md"
        else:
            return f"{task_id}-implementation-plan-v{version}.md"

    @staticmethod
    def save_version(
        task_id: str,
        version: int,
        plan: ImplementationPlan,
        reason: str,
        complexity_before: int,
        complexity_after: int
    ):
        """Save new plan version with metadata"""
        filename = VersionManager.get_version_filename(task_id, version)
        filepath = f"tasks/in_progress/{filename}"

        # Generate plan content
        plan_content = generate_implementation_plan_markdown(plan)

        # Add version header
        version_header = f"""# Implementation Plan - {task_id} (v{version})

**Generated**: {datetime.now().isoformat()}
**Version**: {version}
**Reason**: {reason}
**Complexity Before**: {complexity_before}/10
**Complexity After**: {complexity_after}/10

---

{plan_content}
"""

        # Write file
        with open(filepath, 'w') as f:
            f.write(version_header)

        return filepath
```

## Test Requirements

### Unit Tests

- [ ] **File Modification Tests**
  - [ ] Add file → plan updated, marked as modified
  - [ ] Remove file → plan updated, count decreases
  - [ ] Edit file → details updated
  - [ ] Invalid file path → rejected with error

- [ ] **Test Strategy Tests**
  - [ ] Update unit test count → plan updated
  - [ ] Update integration test count → plan updated
  - [ ] Invalid count (negative, non-numeric) → rejected

- [ ] **Complexity Recalculation Tests**
  - [ ] Remove 2 files → complexity decreases
  - [ ] Add 3 files → complexity increases
  - [ ] File count factor recalculated correctly
  - [ ] Total score recalculated correctly

- [ ] **Versioning Tests**
  - [ ] v1 → v2 increment correct
  - [ ] v2 filename has "-v2" suffix
  - [ ] Version history metadata complete
  - [ ] Old version preserved

### Integration Tests

- [ ] **Modification Loop**
  - [ ] Enter modify mode
  - [ ] Remove 2 files
  - [ ] Save changes
  - [ ] Complexity recalculated (8 → 6)
  - [ ] New version created (v2)
  - [ ] Return to checkpoint with updated data

- [ ] **Review Mode Change**
  - [ ] Start with score=7 (full required)
  - [ ] Modify to remove files
  - [ ] New score=5 (quick optional)
  - [ ] Mode changed notification
  - [ ] Quick review countdown displayed

- [ ] **View Then Modify**
  - [ ] View plan in pager
  - [ ] Return to checkpoint
  - [ ] Select modify
  - [ ] Make changes
  - [ ] Save and recalculate

## Success Metrics

### User Experience
- Modification usage rate: 10-20% of full reviews
- View usage rate: 30-40% before modification
- Complexity reduction success: 60-70% of modifications

### Quality
- Version tracking accuracy: 100%
- Complexity recalculation accuracy: 100%
- No data loss on modifications

## File Structure

### Files to Modify

```
installer/global/commands/lib/
├── review_modes.py (UPDATE)
│   ├── Add ModificationManager class
│   └── Update FullReviewHandler with [M]/[V] handlers
└── version_manager.py (NEW)
    └── VersionManager class

tests/unit/
├── test_modification.py (NEW)
└── test_versioning.py (NEW)

tests/integration/
└── test_modification_loop.py (NEW)
```

## Dependencies

- ✅ TASK-003A: ComplexityCalculator (for recalculation)
- ✅ TASK-003B-2: FullReviewHandler (for [M]/[V] handler integration)

## Estimated Effort

**1.5 days** (10-12 hours):
- View handler: 1 hour
- Modification interface: 3 hours
- File section editing: 2 hours
- Recalculation logic: 2 hours
- Versioning system: 2 hours
- Tests: 2 hours
- Integration: 1 hour

**Complexity**: 6/10 (Complex - interactive editing, validation, versioning)

---

**Ready for implementation after TASK-003B-2 completion** ✅
