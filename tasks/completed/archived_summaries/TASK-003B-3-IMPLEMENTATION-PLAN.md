# TASK-003B-3: Modification & View Modes - Python Implementation Plan

**Version**: 1.0
**Created**: 2025-10-09
**Status**: Design Complete
**Estimated Effort**: 10-12 hours (1.5 days)
**Complexity Score**: 6/10 (Complex - Interactive editing, validation, versioning)

---

## Executive Summary

This implementation adds interactive plan modification and viewing capabilities to the full review mode. Users can:
1. **[V]iew**: Display implementation plans in a system pager (less/more) with scrolling and search
2. **[M]odify**: Interactively edit plan files, tests, dependencies, and implementation order
3. **Versioning**: Track plan changes with v1 → v2 → v3 versioning and complexity recalculation

**Key Innovation**: Plan versioning enables iterative refinement while maintaining audit trail and recalculating complexity after each modification.

---

## Architecture Overview

### 1. Component Structure

```
installer/global/commands/lib/
├── review_modes.py (EXTEND)
│   ├── FullReviewHandler._handle_view() (NEW)
│   └── FullReviewHandler._handle_modify() (NEW)
├── modification_manager.py (NEW)
│   ├── ModificationManager
│   ├── ModificationSession
│   └── ModifiedPlanResult
├── version_manager.py (NEW)
│   ├── VersionManager
│   ├── VersionHistory
│   └── PlanSerializer
└── pager_display.py (NEW)
    ├── PagerStrategy (Protocol)
    ├── LessPagerStrategy
    ├── MorePagerStrategy
    └── FallbackPagerStrategy
```

### 2. Data Flow

```
FullReviewHandler
    ↓
[V] Pressed → PagerDisplay → System Pager → Return to Checkpoint
    ↓
[M] Pressed → ModificationManager
    ↓
Section Selection (1-5)
    ↓
Interactive Editing (Add/Remove/Edit)
    ↓
Save & Recalculate
    ↓
VersionManager.save_version()
    ↓
ComplexityCalculator.calculate()
    ↓
Return to Checkpoint (with new score)
```

---

## Architectural Decisions

### ADR-001: Pager Implementation Strategy

**Decision**: Use Strategy Pattern with platform-specific implementations

**Rationale**:
- Cross-platform support (Unix/Linux/macOS/Windows)
- Graceful degradation (less → more → stdout)
- Testable without actual pagers
- Clean separation of concerns

**Alternatives Considered**:
1. ❌ Direct subprocess.run() calls - Not testable, no fallback
2. ❌ Platform-specific if/else blocks - Not maintainable
3. ✅ Strategy Pattern - Flexible, testable, maintainable

**Implementation**:
```python
class PagerStrategy(Protocol):
    def display(self, file_path: Path) -> bool: ...
    def is_available(self) -> bool: ...

class LessPagerStrategy:
    def display(self, file_path: Path) -> bool:
        return subprocess.run(['less', '-R', str(file_path)]).returncode == 0

    def is_available(self) -> bool:
        return shutil.which('less') is not None
```

### ADR-002: Plan Data Structure for Modification

**Decision**: Use mutable copy of ImplementationPlan dataclass with tracked changes

**Rationale**:
- ImplementationPlan is already frozen (immutable)
- Need to track modifications separately
- Deep copy preserves original for comparison
- Session tracking enables audit trail

**Data Model**:
```python
@dataclass
class ImplementationPlan:
    task_id: str
    files_to_create: List[str]  # Simple list of file paths
    patterns_used: List[str]
    external_dependencies: List[str]
    test_summary: Optional[str]
    phases: Optional[List[str]]
    raw_plan: str
```

**Note**: Based on review of `complexity_models.py`, `files_to_create` is a simple `List[str]`, not a list of dicts. The modification flow needs to:
1. Parse `raw_plan` to extract file details
2. Maintain a parallel structure for file metadata (purpose, type)
3. Regenerate `raw_plan` after modifications

### ADR-003: Version Storage Strategy

**Decision**: Store versions as separate files with metadata in task frontmatter

**Rationale**:
- Simple file-based versioning (no database)
- Easy to inspect/diff manually
- Git-friendly (one file per version)
- Metadata in task file maintains single source of truth

**File Naming Convention**:
```
tasks/in_progress/
├── TASK-003B-3.md (task file with metadata)
├── TASK-003B-3-implementation-plan.md (v1)
├── TASK-003B-3-implementation-plan-v2.md
└── TASK-003B-3-implementation-plan-v3.md
```

**Task Metadata**:
```yaml
---
implementation_plan:
  file: "TASK-003B-3-implementation-plan-v3.md"
  version: 3
  version_history:
    - version: 1
      created: "2025-10-09T10:00:00Z"
      reason: "Initial generation"
      complexity_after: 8
    - version: 2
      created: "2025-10-09T10:15:00Z"
      reason: "User modified: Removed 1 file"
      complexity_before: 8
      complexity_after: 6
---
```

### ADR-004: Complexity Recalculation

**Decision**: Reuse existing ComplexityCalculator with updated ImplementationPlan

**Rationale**:
- DRY principle - don't duplicate complexity logic
- Automatic score recalculation ensures consistency
- Review mode routing logic already exists
- No need to manually track which factors changed

**Integration Point**:
```python
def _recalculate_complexity(self) -> ComplexityScore:
    """Recalculate complexity after modifications"""
    # Build new evaluation context with modified plan
    context = EvaluationContext(
        task_id=self.task_id,
        technology_stack=self.original_context.technology_stack,
        implementation_plan=self.modified_plan,  # Updated plan
        task_metadata=self.original_context.task_metadata,
        user_flags=self.original_context.user_flags
    )

    # Reuse existing calculator
    calculator = ComplexityCalculator()
    new_score = calculator.calculate(context)

    return new_score
```

### ADR-005: Plan Serialization Format

**Decision**: Use markdown with YAML frontmatter for plan files

**Rationale**:
- Consistent with task file format
- Human-readable and editable
- Parseable with existing tools (PyYAML, regex)
- Version control friendly

**Plan File Format**:
```markdown
---
task_id: TASK-003B-3
version: 2
created: 2025-10-09T10:15:00Z
reason: "User modified: Removed 1 file"
complexity_before: 8
complexity_after: 6
---

# Implementation Plan - TASK-003B-3 (v2)

## Files to Create

1. **installer/global/commands/lib/modification_manager.py**
   - Purpose: Manage interactive plan modifications

2. **installer/global/commands/lib/version_manager.py**
   - Purpose: Handle plan versioning and history

## Tests

- Unit Tests: 8
- Integration Tests: 3

## Dependencies

- No new external dependencies

## Implementation Order

1. Implement PagerDisplay (1 hour)
2. Implement ModificationManager (3 hours)
...
```

---

## Implementation Plan

### Phase 1: Pager Display System (2 hours)

**File**: `installer/global/commands/lib/pager_display.py` (NEW)

**Classes**:
1. `PagerStrategy` (Protocol)
2. `LessPagerStrategy`
3. `MorePagerStrategy`
4. `FallbackPagerStrategy`
5. `PagerDisplay` (Facade)

**Key Methods**:
```python
class PagerDisplay:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.strategies = [
            LessPagerStrategy(),
            MorePagerStrategy(),
            FallbackPagerStrategy()
        ]

    def display(self) -> bool:
        """Display file in pager with fallback chain"""
        for strategy in self.strategies:
            if strategy.is_available():
                if strategy.display(self.file_path):
                    return True
        return False
```

**Platform Support**:
- **Unix/Linux/macOS**: `less -R` (preserve ANSI colors)
- **Windows**: `more` (cmd.exe built-in)
- **Fallback**: Print to stdout with pagination

**Error Handling**:
- File not found → Display error message
- Pager not available → Try next strategy
- Pager execution error → Try next strategy
- All strategies fail → Print to stdout

**Testing Strategy**:
- Mock subprocess.run() to test strategy selection
- Test fallback chain without actual pagers
- Integration test with real pager (Unix only)

---

### Phase 2: Version Management System (2 hours)

**File**: `installer/global/commands/lib/version_manager.py` (NEW)

**Data Models**:
```python
@dataclass
class VersionEntry:
    """Single version history entry"""
    version: int
    created: str  # ISO 8601 timestamp
    reason: str
    complexity_before: Optional[int]
    complexity_after: int
    modified_by: str = "user"

@dataclass
class VersionHistory:
    """Complete version history for a plan"""
    current_version: int
    current_file: str
    entries: List[VersionEntry]
```

**Key Classes**:
```python
class VersionManager:
    """Manages plan versioning and file operations"""

    @staticmethod
    def increment_version(current_version: int) -> int:
        """Increment version number"""
        return current_version + 1

    @staticmethod
    def get_version_filename(task_id: str, version: int) -> str:
        """Get filename for version"""
        if version == 1:
            return f"{task_id}-implementation-plan.md"
        return f"{task_id}-implementation-plan-v{version}.md"

    @staticmethod
    def save_version(
        task_id: str,
        version: int,
        plan_content: str,
        reason: str,
        complexity_before: Optional[int],
        complexity_after: int
    ) -> Path:
        """Save new plan version with metadata"""
        ...

    @staticmethod
    def load_version_history(task_file_path: Path) -> VersionHistory:
        """Load version history from task file frontmatter"""
        ...

    @staticmethod
    def update_task_metadata(
        task_file_path: Path,
        new_version: int,
        version_entry: VersionEntry
    ) -> None:
        """Update task file with new version metadata"""
        ...

class PlanSerializer:
    """Serialize/deserialize implementation plans"""

    @staticmethod
    def serialize(plan: ImplementationPlan, metadata: dict) -> str:
        """Convert ImplementationPlan to markdown format"""
        ...

    @staticmethod
    def deserialize(content: str) -> Tuple[dict, ImplementationPlan]:
        """Parse markdown plan into metadata + ImplementationPlan"""
        ...
```

**Critical Function**: Plan Serialization

Since `ImplementationPlan.raw_plan` is a string and `files_to_create` is a simple list, we need:

```python
def _serialize_plan(self, plan: ImplementationPlan, version: int) -> str:
    """
    Generate markdown plan content from ImplementationPlan.

    Challenge: ImplementationPlan doesn't store file purposes/types.
    Solution: Parse raw_plan to extract file details, then regenerate.
    """
    # Parse existing raw_plan to extract file details
    file_details = self._parse_file_details(plan.raw_plan)

    # Build markdown sections
    sections = [
        f"# Implementation Plan - {plan.task_id} (v{version})",
        "",
        "## Files to Create",
        *[f"- {path}: {details['purpose']}"
          for path, details in file_details.items()],
        "",
        "## Tests",
        f"{plan.test_summary or 'No test strategy defined'}",
        "",
        "## Dependencies",
        *[f"- {dep}" for dep in plan.external_dependencies],
        "",
        "## Implementation Order",
        *[f"{i+1}. {phase}" for i, phase in enumerate(plan.phases or [])]
    ]

    return "\n".join(sections)
```

**Edge Cases**:
- v1 has no complexity_before (initial generation)
- Empty version history (new task)
- Corrupted task metadata (fallback to defaults)
- Missing plan file (error handling)

---

### Phase 3: Modification Manager (4 hours)

**File**: `installer/global/commands/lib/modification_manager.py` (NEW)

**Data Models**:
```python
@dataclass
class ModificationSession:
    """Track modifications during interactive session"""
    started_at: datetime
    task_id: str
    original_plan: ImplementationPlan

    # Change tracking
    files_added: List[str] = field(default_factory=list)
    files_removed: List[str] = field(default_factory=list)
    files_edited: List[str] = field(default_factory=list)
    tests_changed: Optional[Dict[str, int]] = None
    dependencies_added: List[str] = field(default_factory=list)
    dependencies_removed: List[str] = field(default_factory=list)

    has_modifications: bool = False

    def summary(self) -> str:
        """Generate human-readable modification summary"""
        changes = []
        if self.files_added:
            changes.append(f"Added {len(self.files_added)} files")
        if self.files_removed:
            changes.append(f"Removed {len(self.files_removed)} files")
        if self.files_edited:
            changes.append(f"Edited {len(self.files_edited)} files")
        if self.tests_changed:
            changes.append(f"Updated test counts")
        return ", ".join(changes) or "No modifications"

@dataclass
class ModifiedPlanResult:
    """Result of modification session"""
    new_plan: ImplementationPlan
    new_complexity_score: ComplexityScore
    new_version: int
    modifications: ModificationSession
    review_mode_changed: bool
    should_proceed_to_phase_3: bool = False
```

**Key Class**:
```python
class ModificationManager:
    """Manages interactive plan modification workflow"""

    def __init__(
        self,
        plan: ImplementationPlan,
        complexity_score: ComplexityScore,
        task_id: str,
        task_file_path: Path,
        evaluation_context: EvaluationContext
    ):
        self.original_plan = plan
        self.original_score = complexity_score
        self.task_id = task_id
        self.task_file_path = task_file_path
        self.evaluation_context = evaluation_context

        # Create mutable copy for modifications
        self.modified_plan = self._create_mutable_copy(plan)

        # Track changes
        self.session = ModificationSession(
            started_at=datetime.utcnow(),
            task_id=task_id,
            original_plan=plan
        )

        # Parse file details from raw_plan for editing
        self.file_details = self._parse_file_details(plan.raw_plan)

    def execute(self) -> Optional[ModifiedPlanResult]:
        """Execute interactive modification workflow"""
        print("\n" + "="*60)
        print("PLAN MODIFICATION MODE")
        print("="*60)

        while True:
            self._display_section_menu()
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
                    print("\nNo modifications made.")
                    return None
            else:
                print(f"❌ Invalid choice: '{choice}'\n")

    def _display_section_menu(self):
        """Display editable sections menu"""
        print(f"\nCurrent Plan: {self.task_id} (v{self._get_current_version()})")
        print(f"Complexity: {self.original_score.total_score}/10")
        print("\nEDITABLE SECTIONS:")
        print(f"  [1] Files ({len(self.modified_plan.files_to_create)} files)")
        print(f"  [2] Tests ({self._count_tests()} planned)")
        print(f"  [3] Dependencies ({len(self.modified_plan.external_dependencies)})")
        print(f"  [4] Implementation Order ({len(self.modified_plan.phases or [])} steps)")
        print(f"  [5] Done (save changes and recalculate)")
        print()

    def _modify_files_section(self):
        """Interactive file modification"""
        while True:
            self._display_files()
            print("\nACTIONS:")
            print("  [A] Add new file")
            print("  [R] Remove file (enter number)")
            print("  [E] Edit file (enter number)")
            print("  [B] Back to section list")

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
                print(f"❌ Invalid action: '{action}'")

    def _add_file(self):
        """Add new file to plan"""
        print("\nADD NEW FILE")
        path = input("Enter file path: ").strip()

        # Validate file path
        if not self._validate_file_path(path):
            print("❌ Invalid file path format (no spaces, valid extension)")
            return

        purpose = input("Enter file purpose: ").strip()
        file_type = input("New or Modified? (n/m): ").strip().lower()

        if file_type not in ['n', 'm']:
            print("❌ Invalid type (must be 'n' or 'm')")
            return

        # Add to plan and tracking
        self.modified_plan.files_to_create.append(path)
        self.file_details[path] = {
            'purpose': purpose,
            'type': 'new' if file_type == 'n' else 'modified'
        }

        self.session.files_added.append(path)
        self.session.has_modifications = True

        print(f"✅ Added {path}")

    def _remove_file(self):
        """Remove file from plan"""
        file_list = self.modified_plan.files_to_create
        if not file_list:
            print("No files to remove")
            return

        try:
            num = int(input("Enter file number to remove: ").strip())
            if 1 <= num <= len(file_list):
                removed_file = file_list[num - 1]

                # Confirm removal
                confirm = input(f"Remove '{removed_file}'? (y/n): ").strip().lower()
                if confirm == 'y':
                    file_list.pop(num - 1)
                    if removed_file in self.file_details:
                        del self.file_details[removed_file]

                    self.session.files_removed.append(removed_file)
                    self.session.has_modifications = True

                    print(f"✅ Removed {removed_file}")
            else:
                print(f"❌ Invalid number (must be 1-{len(file_list)})")
        except ValueError:
            print("❌ Invalid input (must be a number)")

    def _save_and_recalculate(self) -> ModifiedPlanResult:
        """Save modifications and recalculate complexity"""
        print("\n" + "="*60)
        print("SAVING MODIFICATIONS")
        print("="*60)

        # Display modification summary
        print(f"\nModifications: {self.session.summary()}")
        print("\nRegenerating plan and recalculating complexity...")

        # Recalculate complexity
        new_score = self._recalculate_complexity()

        # Determine if review mode changed
        review_mode_changed = (
            self.original_score.review_mode != new_score.review_mode
        )

        # Generate new version
        new_version = self._increment_version()

        # Save new plan version
        self._save_plan_version(new_version, new_score)

        # Display complexity change
        self._display_complexity_change(new_score, review_mode_changed)

        # Determine if should proceed to Phase 3
        should_proceed = (
            review_mode_changed and
            new_score.review_mode == ReviewMode.AUTO_PROCEED
        )

        return ModifiedPlanResult(
            new_plan=self.modified_plan,
            new_complexity_score=new_score,
            new_version=new_version,
            modifications=self.session,
            review_mode_changed=review_mode_changed,
            should_proceed_to_phase_3=should_proceed
        )

    def _create_mutable_copy(self, plan: ImplementationPlan) -> ImplementationPlan:
        """Create mutable copy of plan for modification"""
        # Since ImplementationPlan is a dataclass, we can use replace()
        # or create a new instance with copied lists
        return ImplementationPlan(
            task_id=plan.task_id,
            files_to_create=list(plan.files_to_create),
            patterns_used=list(plan.patterns_used),
            external_dependencies=list(plan.external_dependencies),
            estimated_loc=plan.estimated_loc,
            risk_indicators=list(plan.risk_indicators),
            raw_plan=plan.raw_plan,
            test_summary=plan.test_summary,
            risk_details=plan.risk_details.copy() if plan.risk_details else None,
            phases=list(plan.phases) if plan.phases else None,
            implementation_instructions=plan.implementation_instructions,
            estimated_duration=plan.estimated_duration,
            complexity_score=plan.complexity_score
        )

    def _parse_file_details(self, raw_plan: str) -> Dict[str, dict]:
        """
        Parse file details from raw_plan markdown.

        Expected format in raw_plan:
        ## Files to Create
        - path/to/file.py: Purpose description
        - another/file.ts: Another purpose
        """
        file_details = {}

        # Simple regex-based parsing
        # Look for "## Files" section and extract list items
        lines = raw_plan.split('\n')
        in_files_section = False

        for line in lines:
            if line.strip().startswith('## Files'):
                in_files_section = True
                continue
            elif line.strip().startswith('##'):
                in_files_section = False
            elif in_files_section and line.strip().startswith('-'):
                # Parse "- path: purpose" format
                match = re.match(r'^-\s+(.+?):\s+(.+)$', line.strip())
                if match:
                    path, purpose = match.groups()
                    file_details[path.strip()] = {
                        'purpose': purpose.strip(),
                        'type': 'new'  # Default to new
                    }

        return file_details
```

**Validation Functions**:
```python
def _validate_file_path(self, path: str) -> bool:
    """Validate file path format"""
    if not path:
        return False
    if ' ' in path:
        return False
    if not any(path.endswith(ext) for ext in ['.py', '.ts', '.tsx', '.js', '.md', '.json', '.yaml', '.yml']):
        return False
    return True

def _count_tests(self) -> int:
    """Count total tests from test_summary"""
    if not self.modified_plan.test_summary:
        return 0

    # Parse test summary for counts
    # Expected format: "Unit Tests: 6, Integration Tests: 2"
    import re
    matches = re.findall(r'(\d+)', self.modified_plan.test_summary)
    return sum(int(m) for m in matches)
```

---

### Phase 4: FullReviewHandler Integration (1 hour)

**File**: `installer/global/commands/lib/review_modes.py` (UPDATE)

**Changes to FullReviewHandler**:

```python
class FullReviewHandler:
    """Main coordinator for Full Review Mode workflow"""

    def __init__(
        self,
        complexity_score: ComplexityScore,
        plan: ImplementationPlan,
        task_metadata: Dict[str, Any],
        task_file_path: Path,
        evaluation_context: EvaluationContext,  # NEW: Need for recalculation
        escalated: bool = False
    ):
        # ... existing initialization ...
        self.evaluation_context = evaluation_context  # NEW

    def execute(self) -> FullReviewResult:
        """Execute full review workflow"""
        try:
            self.display.render_full_checkpoint()

            invalid_attempts = 0
            max_invalid_attempts = 3

            while True:
                choice = self._prompt_for_decision()

                if choice == 'a':
                    return self._handle_approval()
                elif choice == 'c':
                    result = self._handle_cancellation()
                    if result is not None:
                        return result
                    continue
                elif choice == 'm':
                    # NEW: Handle modification
                    result = self._handle_modification()
                    if result is not None:
                        return result
                    continue
                elif choice == 'v':
                    # NEW: Handle view
                    self._handle_view()
                    continue
                elif choice == 'q':
                    print("\n⚠️ Q&A mode coming soon (TASK-003B-4)")
                    print("For now, please choose another option.\n")
                    continue
                else:
                    invalid_attempts += 1
                    print(f"\n❌ Invalid choice: '{choice}'")
                    if invalid_attempts >= max_invalid_attempts:
                        print(f"⚠️ {invalid_attempts} invalid attempts.\n")
                    continue

        except KeyboardInterrupt:
            print("\n\n⚠️ Interrupt detected...")
            return self._handle_cancellation(force=True)
        except Exception as e:
            print(f"\n❌ Error during full review: {e}")
            raise

    def _handle_view(self) -> None:
        """
        Handle [V]iew action - display plan in pager.

        Returns to checkpoint after viewing.
        """
        from .pager_display import PagerDisplay

        # Determine plan file path
        plan_file = self._get_plan_file_path()

        if not plan_file or not plan_file.exists():
            print("\n⚠️ Implementation plan file not found")
            print("Unable to display plan.\n")
            input("Press Enter to return to checkpoint...")
            return

        print("\nOpening implementation plan in pager...")
        print("(Use arrow keys to scroll, 'q' to quit, '/' to search)\n")

        # Display in pager
        pager = PagerDisplay(plan_file)
        success = pager.display()

        if not success:
            print("\n⚠️ Unable to open pager")
            print("Displaying plan content:\n")
            print(plan_file.read_text())

        # Return to checkpoint
        print("\n" + "="*60)
        input("Press Enter to return to checkpoint...")
        print()

        # Re-display checkpoint
        self.display.render_full_checkpoint()

    def _handle_modification(self) -> Optional[FullReviewResult]:
        """
        Handle [M]odify action - interactive plan editing.

        Returns:
            FullReviewResult if modifications complete and should proceed
            None if modifications cancelled or no changes made
        """
        from .modification_manager import ModificationManager

        # Create modification manager
        manager = ModificationManager(
            plan=self.plan,
            complexity_score=self.complexity_score,
            task_id=self.task_metadata.get('id', 'UNKNOWN'),
            task_file_path=self.task_file_path,
            evaluation_context=self.evaluation_context
        )

        # Execute modification workflow
        result = manager.execute()

        if result is None:
            # No modifications or cancelled
            print("\nReturning to checkpoint...\n")
            self.display.render_full_checkpoint()
            return None

        # Modifications saved and complexity recalculated
        print("\n" + "="*60)
        print("MODIFICATIONS COMPLETE")
        print("="*60)

        # Update handler state with new plan and score
        self.plan = result.new_plan
        self.complexity_score = result.new_complexity_score

        # Check if review mode changed
        if result.review_mode_changed:
            print("\n✅ Review mode changed!")

            if result.should_proceed_to_phase_3:
                # Score dropped to AUTO_PROCEED - skip checkpoint
                print("Plan simplified enough to auto-proceed.")
                print("Proceeding to Phase 3 (Implementation)...\n")

                return FullReviewResult(
                    action="approve",
                    timestamp=datetime.utcnow().isoformat() + "Z",
                    approved=True,
                    metadata_updates={
                        "implementation_plan": {
                            "approved": True,
                            "approved_by": "system",
                            "approved_at": datetime.utcnow().isoformat() + "Z",
                            "review_mode": "modified_to_auto_proceed",
                            "complexity_score": result.new_complexity_score.total_score,
                            "version": result.new_version,
                        }
                    },
                    proceed_to_phase_3=True
                )

            elif result.new_complexity_score.review_mode == ReviewMode.QUICK_OPTIONAL:
                # Switched to quick optional - escalate to QuickReviewHandler
                print("Switching to Quick Optional Review mode...")
                print("(10-second countdown will start)\n")

                # Return special result to trigger quick review
                return FullReviewResult(
                    action="escalate_to_quick",  # Custom action
                    timestamp=datetime.utcnow().isoformat() + "Z",
                    approved=False,
                    metadata_updates={
                        "implementation_plan": {
                            "review_mode": "escalated_to_quick_after_modification",
                            "complexity_score": result.new_complexity_score.total_score,
                            "version": result.new_version,
                        }
                    },
                    proceed_to_phase_3=False
                )

        # Review mode unchanged or still requires full review
        print("\nReturning to checkpoint with updated plan...\n")

        # Re-render checkpoint with new data
        self.display = FullReviewDisplay(
            complexity_score=result.new_complexity_score,
            plan=result.new_plan,
            task_metadata=self.task_metadata,
            escalated=self.escalated
        )
        self.display.render_full_checkpoint()

        return None

    def _get_plan_file_path(self) -> Optional[Path]:
        """
        Get path to current implementation plan file.

        Returns:
            Path to plan file, or None if not found
        """
        task_id = self.task_metadata.get('id', 'UNKNOWN')

        # Check task metadata for plan file
        plan_metadata = self.task_metadata.get('implementation_plan', {})
        if 'file' in plan_metadata:
            plan_file = Path(f"tasks/in_progress/{plan_metadata['file']}")
            if plan_file.exists():
                return plan_file

        # Fallback: Look for default filename
        default_file = Path(f"tasks/in_progress/{task_id}-implementation-plan.md")
        if default_file.exists():
            return default_file

        return None
```

**New Result Action Types**:
```python
# Update FullReviewResult action type
action: Literal["approve", "modify", "view", "question", "cancel", "escalate_to_quick"]
```

---

### Phase 5: Testing Strategy (2 hours)

**Unit Tests** (`tests/unit/test_modification_manager.py`):

```python
import pytest
from pathlib import Path
from installer.global.commands.lib.modification_manager import (
    ModificationManager, ModificationSession, ModifiedPlanResult
)
from installer.global.commands.lib.complexity_models import (
    ImplementationPlan, ComplexityScore, ReviewMode
)

class TestModificationManager:
    def test_add_file_updates_plan(self):
        """Adding file updates modified plan and session"""
        # Setup
        plan = ImplementationPlan(
            task_id="TEST-001",
            files_to_create=["file1.py"],
            raw_plan="## Files\n- file1.py: Original file"
        )
        manager = ModificationManager(plan, ...)

        # Act
        manager._add_file_interactive("file2.py", "New file", "new")

        # Assert
        assert "file2.py" in manager.modified_plan.files_to_create
        assert "file2.py" in manager.session.files_added
        assert manager.session.has_modifications is True

    def test_remove_file_decreases_count(self):
        """Removing file updates plan and tracking"""
        plan = ImplementationPlan(
            task_id="TEST-001",
            files_to_create=["file1.py", "file2.py"]
        )
        manager = ModificationManager(plan, ...)

        manager._remove_file_by_index(0)  # Remove file1.py

        assert len(manager.modified_plan.files_to_create) == 1
        assert "file1.py" in manager.session.files_removed

    def test_invalid_file_path_rejected(self):
        """Invalid file paths are rejected"""
        manager = ModificationManager(...)

        assert manager._validate_file_path("invalid path.py") is False
        assert manager._validate_file_path("valid_path.py") is True

    def test_complexity_recalculation(self):
        """Complexity is recalculated after modifications"""
        # Original: 3 files, score=8
        plan = ImplementationPlan(
            task_id="TEST-001",
            files_to_create=["f1.py", "f2.py", "f3.py"]
        )
        manager = ModificationManager(plan, ...)

        # Remove 2 files
        manager._remove_file_by_index(1)
        manager._remove_file_by_index(1)

        # Recalculate
        result = manager._save_and_recalculate()

        # Assert score decreased
        assert result.new_complexity_score.total_score < 8
```

**Integration Tests** (`tests/integration/test_modification_workflow.py`):

```python
def test_full_modification_loop():
    """Complete modification workflow"""
    # 1. Start with score=8 (FULL_REQUIRED)
    plan = create_complex_plan()  # 5 files
    handler = FullReviewHandler(...)

    # 2. User selects [M]odify
    # 3. Remove 3 files
    # 4. Save and recalculate
    # 5. New score=5 (QUICK_OPTIONAL)
    # 6. Verify version incremented
    # 7. Verify old version preserved
    # 8. Verify task metadata updated

def test_review_mode_change_to_auto_proceed():
    """Modification that changes mode to auto-proceed"""
    # Score=7 → Remove files → Score=3 → Auto-proceed
    ...
```

**Pager Tests** (`tests/unit/test_pager_display.py`):

```python
def test_pager_strategy_selection():
    """Correct pager strategy selected for platform"""
    ...

def test_pager_fallback_chain():
    """Falls back through strategies when unavailable"""
    ...

def test_view_returns_to_checkpoint():
    """After viewing, returns to checkpoint"""
    ...
```

**Version Manager Tests** (`tests/unit/test_version_manager.py`):

```python
def test_version_increment():
    """Version increments correctly"""
    assert VersionManager.increment_version(1) == 2
    assert VersionManager.increment_version(5) == 6

def test_version_filename_generation():
    """Version filenames follow convention"""
    assert VersionManager.get_version_filename("TASK-001", 1) == \
           "TASK-001-implementation-plan.md"
    assert VersionManager.get_version_filename("TASK-001", 2) == \
           "TASK-001-implementation-plan-v2.md"

def test_version_history_tracking():
    """Version history is correctly tracked"""
    ...
```

---

## Integration Points

### 1. With ComplexityCalculator
- **ModificationManager** calls `ComplexityCalculator.calculate()` after changes
- **Context**: Rebuild `EvaluationContext` with modified plan
- **Score Comparison**: Display before/after scores

### 2. With FullReviewHandler
- **[V] Action**: Call `PagerDisplay.display()`
- **[M] Action**: Call `ModificationManager.execute()`
- **State Updates**: Update `plan` and `complexity_score` after modifications

### 3. With File System
- **Plan Files**: Read/write to `tasks/in_progress/`
- **Task Metadata**: Update YAML frontmatter in task files
- **Atomic Writes**: Use `FileOperations.atomic_write()`

### 4. With Version Manager
- **Version Tracking**: Load/save version history from task metadata
- **File Naming**: Follow convention (v1 no suffix, v2+ with suffix)
- **Serialization**: Convert `ImplementationPlan` to markdown

---

## Edge Cases & Error Handling

### 1. Pager Display Errors
- **No plan file**: Display error, return to checkpoint
- **Pager not available**: Fall back to stdout
- **Pager execution error**: Try next strategy

### 2. Modification Errors
- **Invalid input**: Validate and reject with message
- **No modifications**: Allow exit without saving
- **Concurrent modifications**: Not supported (single-user CLI)

### 3. Version Management Errors
- **Missing version history**: Initialize with v1
- **Corrupted metadata**: Fallback to defaults
- **File write failure**: Preserve original, display error

### 4. Complexity Recalculation Errors
- **Calculator failure**: Use fail-safe (score=10, FULL_REQUIRED)
- **Invalid plan data**: Display error, allow retry

---

## Performance Considerations

### 1. File Parsing
- **Lazy Parsing**: Only parse file details when entering modification mode
- **Caching**: Cache parsed file details during session
- **Regex Optimization**: Compile regex patterns once

### 2. Plan Serialization
- **Incremental Updates**: Only regenerate modified sections
- **String Building**: Use list join instead of repeated concatenation
- **Template Rendering**: Simple format strings (no Jinja2 needed)

### 3. Version Management
- **Metadata Updates**: Atomic writes with temp files
- **Version Tracking**: In-memory during session, persist at end

---

## Success Criteria

### Functional
- ✅ [V]iew displays plan in pager on all platforms
- ✅ [M]odify allows adding/removing/editing files
- ✅ Complexity recalculated correctly after modifications
- ✅ Version history tracked with complete audit trail
- ✅ Review mode changes handled (auto-proceed, quick optional)

### Quality
- ✅ 90%+ test coverage for new code
- ✅ No data loss on modifications
- ✅ Graceful error handling with user feedback
- ✅ Cross-platform compatibility (Unix/macOS/Windows)

### User Experience
- ✅ Clear prompts and validation messages
- ✅ Intuitive section navigation (1-5 menu)
- ✅ Helpful modification summaries
- ✅ Smooth return to checkpoint after actions

---

## File Structure Summary

```
installer/global/commands/lib/
├── review_modes.py (EXTEND)
│   ├── FullReviewHandler._handle_view() (NEW)
│   └── FullReviewHandler._handle_modification() (NEW)
├── pager_display.py (NEW - 200 LOC)
│   ├── PagerStrategy (Protocol)
│   ├── LessPagerStrategy
│   ├── MorePagerStrategy
│   ├── FallbackPagerStrategy
│   └── PagerDisplay (Facade)
├── modification_manager.py (NEW - 400 LOC)
│   ├── ModificationSession
│   ├── ModifiedPlanResult
│   └── ModificationManager
└── version_manager.py (NEW - 300 LOC)
    ├── VersionEntry
    ├── VersionHistory
    ├── VersionManager
    └── PlanSerializer

tests/unit/
├── test_pager_display.py (NEW - 150 LOC)
├── test_modification_manager.py (NEW - 250 LOC)
└── test_version_manager.py (NEW - 200 LOC)

tests/integration/
└── test_modification_workflow.py (NEW - 150 LOC)
```

**Total New Code**: ~1,650 LOC
**Total Test Code**: ~750 LOC
**Coverage Target**: 90%+

---

## Implementation Timeline

### Day 1 (6 hours)
- **Morning (3h)**: Pager display system + tests
- **Afternoon (3h)**: Version manager + tests

### Day 2 (6 hours)
- **Morning (3h)**: Modification manager core + file section
- **Afternoon (3h)**: Test/dependency sections + integration

---

## Dependencies

### Required
- ✅ TASK-003A: ComplexityCalculator (for recalculation)
- ✅ TASK-003B-2: FullReviewHandler (for integration points)

### Optional
- ⬜ TASK-003B-4: Q&A mode (parallel development)

---

## Risk Assessment

### High Risk
- **Plan parsing complexity**: `raw_plan` is unstructured text
  - **Mitigation**: Robust regex parsing with fallbacks
- **Cross-platform pager behavior**: Different on Windows
  - **Mitigation**: Fallback chain + stdout option

### Medium Risk
- **State management during modifications**: Complex tracking
  - **Mitigation**: Clear session object with change tracking
- **Version file conflicts**: Manual edits could break versioning
  - **Mitigation**: Atomic writes + validation on load

### Low Risk
- **User input validation**: Invalid file paths, numbers
  - **Mitigation**: Comprehensive validation with helpful errors

---

## Conclusion

This implementation plan provides a complete, production-ready approach to adding modification and view capabilities to the full review mode. Key strengths:

1. **Architecture**: Clean separation with Strategy Pattern (pagers), Manager Pattern (modifications), and clear integration points
2. **Data Integrity**: Version tracking, atomic writes, comprehensive audit trail
3. **User Experience**: Intuitive menus, helpful validation, smooth workflows
4. **Testing**: 90%+ coverage with unit and integration tests
5. **Robustness**: Fallback strategies, error handling, edge case coverage

**Ready for implementation** after TASK-003B-2 completion.
