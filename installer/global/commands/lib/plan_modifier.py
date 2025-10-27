"""
Plan Modifier Module - Interactive modification of implementation plans.

Part of TASK-029: Add "Modify Plan" Option to Phase 2.8 Checkpoint.

This module provides interactive modification capabilities for implementation plans
during Phase 2.8 checkpoint. Allows users to modify files, dependencies, risks, and
effort estimates through a menu-driven interface with undo support.

Storage location: docs/state/{task_id}/implementation_plan.md
Version history: docs/state/{task_id}/versions/

Author: Claude (Anthropic)
Created: 2025-10-18
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional
from pathlib import Path
import logging

try:
    from .plan_persistence import load_plan, save_plan, PlanPersistenceError
    from .plan_markdown_parser import PlanMarkdownParser
except ImportError:
    # Fallback for direct execution (tests)
    from plan_persistence import load_plan, save_plan, PlanPersistenceError
    from plan_markdown_parser import PlanMarkdownParser

# Configure logging
logger = logging.getLogger(__name__)


class PlanModificationError(Exception):
    """Raised when plan modification operations fail."""
    pass


class ModificationCategory(Enum):
    """Categories of plan modifications available."""
    FILES = "files"
    DEPENDENCIES = "dependencies"
    RISKS = "risks"
    EFFORT = "effort"

    @property
    def display_name(self) -> str:
        """Get display name for menu."""
        return {
            ModificationCategory.FILES: "Files (add/remove)",
            ModificationCategory.DEPENDENCIES: "Dependencies",
            ModificationCategory.RISKS: "Risks",
            ModificationCategory.EFFORT: "Effort Estimate"
        }[self]


@dataclass
class ModificationRecord:
    """Records a single modification to the plan.

    Attributes:
        category: Type of modification (FILES, DEPENDENCIES, RISKS, EFFORT)
        action: Action performed (add, remove, modify)
        details: Human-readable description of the change
        previous_value: Value before modification (for undo)
        new_value: Value after modification
    """
    category: ModificationCategory
    action: str
    details: str
    previous_value: Any = None
    new_value: Any = None

    def __str__(self) -> str:
        """Format modification record for display."""
        return f"{self.category.value.upper()}: {self.action} - {self.details}"


@dataclass
class ModificationSession:
    """Manages a modification session state.

    Attributes:
        task_id: Task identifier
        original_plan: Original plan data (for reference)
        current_plan: Current plan data (with modifications)
        modifications: List of modifications made
        version: Plan version number
    """
    task_id: str
    original_plan: Dict[str, Any]
    current_plan: Dict[str, Any]
    modifications: List[ModificationRecord] = field(default_factory=list)
    version: int = 1

    @property
    def has_modifications(self) -> bool:
        """Check if any modifications have been made."""
        return len(self.modifications) > 0

    @property
    def modification_count(self) -> int:
        """Get total number of modifications."""
        return len(self.modifications)


class PlanModifier:
    """Interactive plan modification orchestrator.

    Provides menu-driven interface for modifying implementation plans
    during Phase 2.8 checkpoint. Supports undo functionality and maintains
    modification history.

    Example:
        >>> modifier = PlanModifier("TASK-029")
        >>> updated_plan = modifier.run_interactive_session()
        >>> if updated_plan:
        ...     print(f"Plan modified with {len(updated_plan['modifications'])} changes")
    """

    def __init__(self, task_id: str):
        """
        Initialize plan modifier.

        Args:
            task_id: Task identifier (e.g., "TASK-029")

        Raises:
            PlanModificationError: If plan cannot be loaded
        """
        self.task_id = task_id
        self.session: Optional[ModificationSession] = None

    def run_interactive_session(self) -> Optional[Dict[str, Any]]:
        """
        Run interactive modification session.

        Main entry point for plan modification. Loads the plan, displays
        modification menu, processes user choices, and saves the updated plan.

        Returns:
            Updated plan dictionary if modifications were made and saved,
            None if session was cancelled or no modifications made

        Raises:
            PlanModificationError: If critical errors occur

        Example:
            >>> modifier = PlanModifier("TASK-029")
            >>> updated_plan = modifier.run_interactive_session()
            Plan Modification Session for TASK-029
            ========================================

            Current Modifications: 0

            What would you like to modify?
            1. Files (add/remove)
            2. Dependencies
            3. Risks
            4. Effort Estimate
            5. Undo Last Change
            6. Save and Exit
            7. Cancel (discard changes)

            Choice:
        """
        try:
            # Load current plan
            plan_data = load_plan(self.task_id)
            if not plan_data:
                raise PlanModificationError(
                    f"No implementation plan found for {self.task_id}"
                )

            # Initialize session
            self.session = ModificationSession(
                task_id=self.task_id,
                original_plan=plan_data.copy(),
                current_plan=plan_data,
                version=plan_data.get('version', 1)
            )

            # Run modification loop
            while True:
                choice = self._display_modification_menu()

                if choice == '6':  # Save and Exit
                    return self._finalize_modifications()
                elif choice == '7':  # Cancel
                    print("\nModifications cancelled. Original plan unchanged.")
                    return None
                elif choice == '5':  # Undo
                    self._handle_undo()
                elif choice in ['1', '2', '3', '4']:
                    category_map = {
                        '1': ModificationCategory.FILES,
                        '2': ModificationCategory.DEPENDENCIES,
                        '3': ModificationCategory.RISKS,
                        '4': ModificationCategory.EFFORT
                    }
                    self._handle_category_modification(category_map[choice])
                else:
                    print("Invalid choice. Please try again.")

        except PlanPersistenceError as e:
            logger.error(f"Failed to load plan: {e}")
            raise PlanModificationError(f"Cannot load plan: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error in modification session: {e}")
            raise PlanModificationError(f"Modification session failed: {e}") from e

    def _display_modification_menu(self) -> str:
        """
        Display modification menu and get user choice.

        Returns:
            User's menu choice as string

        Example output:
            Plan Modification Session for TASK-029
            ========================================

            Current Modifications: 3
            - FILES: add - Added src/new_module.py
            - DEPENDENCIES: add - Added requests 2.28.0
            - RISKS: modify - Updated security risk severity

            What would you like to modify?
            1. Files (add/remove)
            2. Dependencies
            3. Risks
            4. Effort Estimate
            5. Undo Last Change
            6. Save and Exit
            7. Cancel (discard changes)

            Choice:
        """
        print("\n" + "=" * 60)
        print(f"Plan Modification Session for {self.task_id}")
        print("=" * 60)
        print()

        # Display current modifications
        if self.session.has_modifications:
            print(f"Current Modifications: {self.session.modification_count}")
            for mod in self.session.modifications[-3:]:  # Show last 3
                print(f"  - {mod}")
            if self.session.modification_count > 3:
                print(f"  ... and {self.session.modification_count - 3} more")
            print()
        else:
            print("Current Modifications: 0")
            print()

        # Display menu options
        print("What would you like to modify?")
        print("  1. Files (add/remove)")
        print("  2. Dependencies")
        print("  3. Risks")
        print("  4. Effort Estimate")
        print("  5. Undo Last Change")
        print("  6. Save and Exit")
        print("  7. Cancel (discard changes)")
        print()

        return self._get_user_choice("Choice: ")

    def _get_user_choice(self, prompt: str) -> str:
        """
        Get and validate user input.

        Args:
            prompt: Input prompt to display

        Returns:
            User's input (stripped and lowercased)
        """
        try:
            choice = input(prompt).strip().lower()
            return choice
        except (EOFError, KeyboardInterrupt):
            print("\nSession interrupted. Cancelling modifications.")
            return '7'  # Cancel

    def _handle_category_modification(self, category: ModificationCategory) -> None:
        """
        Handle modification for a specific category.

        Dispatches to appropriate handler based on category type.

        Args:
            category: Modification category
        """
        handlers = {
            ModificationCategory.FILES: self._modify_files,
            ModificationCategory.DEPENDENCIES: self._modify_dependencies,
            ModificationCategory.RISKS: self._modify_risks,
            ModificationCategory.EFFORT: self._modify_effort
        }

        handler = handlers.get(category)
        if handler:
            handler()
        else:
            print(f"Modification for {category.value} not yet implemented.")

    def _modify_files(self) -> None:
        """
        Handle file modifications (add/remove).

        Displays current files and provides options to add or remove files
        from the implementation plan.

        Example:
            Files in Plan
            =============

            Files to Create (2):
            1. src/feature.py
            2. tests/test_feature.py

            Files to Modify (1):
            1. src/existing.py

            Options:
            1. Add file to create
            2. Remove file to create
            3. Add file to modify
            4. Remove file to modify
            5. Back to main menu

            Choice:
        """
        plan = self.session.current_plan.get('plan', {})

        while True:
            print("\n" + "=" * 60)
            print("Files in Plan")
            print("=" * 60)
            print()

            # Display current files
            files_to_create = plan.get('files_to_create', [])
            files_to_modify = plan.get('files_to_modify', [])

            print(f"Files to Create ({len(files_to_create)}):")
            if files_to_create:
                for i, file_path in enumerate(files_to_create, 1):
                    print(f"  {i}. {file_path}")
            else:
                print("  (none)")
            print()

            print(f"Files to Modify ({len(files_to_modify)}):")
            if files_to_modify:
                for i, file_path in enumerate(files_to_modify, 1):
                    print(f"  {i}. {file_path}")
            else:
                print("  (none)")
            print()

            # Display options
            print("Options:")
            print("  1. Add file to create")
            print("  2. Remove file to create")
            print("  3. Add file to modify")
            print("  4. Remove file to modify")
            print("  5. Back to main menu")
            print()

            choice = self._get_user_choice("Choice: ")

            if choice == '1':
                self._add_file(files_to_create, 'create')
            elif choice == '2':
                self._remove_file(files_to_create, 'create')
            elif choice == '3':
                self._add_file(files_to_modify, 'modify')
            elif choice == '4':
                self._remove_file(files_to_modify, 'modify')
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")

    def _add_file(self, file_list: List[str], change_type: str) -> None:
        """
        Add a file to the plan.

        Args:
            file_list: List to add file to (files_to_create or files_to_modify)
            change_type: "create" or "modify"
        """
        print()
        file_path = input(f"Enter file path to {change_type}: ").strip()

        if not file_path:
            print("File path cannot be empty.")
            return

        if file_path in file_list:
            print(f"File '{file_path}' already in list.")
            return

        # Add to list
        file_list.append(file_path)

        # Record modification
        modification = ModificationRecord(
            category=ModificationCategory.FILES,
            action='add',
            details=f"Added {file_path} to {change_type}",
            previous_value=None,
            new_value=file_path
        )
        self.session.modifications.append(modification)

        print(f"✓ Added '{file_path}' to files to {change_type}")

    def _remove_file(self, file_list: List[str], change_type: str) -> None:
        """
        Remove a file from the plan.

        Args:
            file_list: List to remove file from
            change_type: "create" or "modify"
        """
        if not file_list:
            print(f"No files to {change_type} in plan.")
            return

        print()
        print(f"Files to {change_type}:")
        for i, file_path in enumerate(file_list, 1):
            print(f"  {i}. {file_path}")
        print()

        choice = self._get_user_choice("Enter number to remove (or 'c' to cancel): ")

        if choice == 'c':
            return

        try:
            index = int(choice) - 1
            if 0 <= index < len(file_list):
                removed_file = file_list.pop(index)

                # Record modification
                modification = ModificationRecord(
                    category=ModificationCategory.FILES,
                    action='remove',
                    details=f"Removed {removed_file} from {change_type}",
                    previous_value=removed_file,
                    new_value=None
                )
                self.session.modifications.append(modification)

                print(f"✓ Removed '{removed_file}'")
            else:
                print("Invalid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def _modify_dependencies(self) -> None:
        """
        Handle dependency modifications.

        Displays current dependencies and provides options to add or remove
        external dependencies.

        Example:
            Dependencies in Plan
            ====================

            External Dependencies (2):
            1. requests 2.28.0 - HTTP client
            2. pytest 7.0.0 - Testing framework

            Options:
            1. Add dependency
            2. Remove dependency
            3. Back to main menu

            Choice:
        """
        plan = self.session.current_plan.get('plan', {})
        dependencies = plan.get('external_dependencies', [])

        while True:
            print("\n" + "=" * 60)
            print("Dependencies in Plan")
            print("=" * 60)
            print()

            # Display current dependencies
            print(f"External Dependencies ({len(dependencies)}):")
            if dependencies:
                for i, dep in enumerate(dependencies, 1):
                    print(f"  {i}. {dep}")
            else:
                print("  (none)")
            print()

            # Display options
            print("Options:")
            print("  1. Add dependency")
            print("  2. Remove dependency")
            print("  3. Back to main menu")
            print()

            choice = self._get_user_choice("Choice: ")

            if choice == '1':
                self._add_dependency(dependencies)
            elif choice == '2':
                self._remove_dependency(dependencies)
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

    def _add_dependency(self, dependencies: List[str]) -> None:
        """
        Add a dependency to the plan.

        Args:
            dependencies: List of dependencies
        """
        print()
        print("Enter dependency information:")
        name = input("  Package name: ").strip()
        if not name:
            print("Package name cannot be empty.")
            return

        version = input("  Version (optional): ").strip()
        purpose = input("  Purpose (optional): ").strip()

        # Format dependency string
        dep_str = name
        if version:
            dep_str += f" {version}"
        if purpose:
            dep_str += f" - {purpose}"

        if dep_str in dependencies:
            print(f"Dependency '{dep_str}' already in list.")
            return

        # Add to list
        dependencies.append(dep_str)

        # Record modification
        modification = ModificationRecord(
            category=ModificationCategory.DEPENDENCIES,
            action='add',
            details=f"Added dependency: {dep_str}",
            previous_value=None,
            new_value=dep_str
        )
        self.session.modifications.append(modification)

        print(f"✓ Added dependency '{dep_str}'")

    def _remove_dependency(self, dependencies: List[str]) -> None:
        """
        Remove a dependency from the plan.

        Args:
            dependencies: List of dependencies
        """
        if not dependencies:
            print("No dependencies in plan.")
            return

        print()
        print("Dependencies:")
        for i, dep in enumerate(dependencies, 1):
            print(f"  {i}. {dep}")
        print()

        choice = self._get_user_choice("Enter number to remove (or 'c' to cancel): ")

        if choice == 'c':
            return

        try:
            index = int(choice) - 1
            if 0 <= index < len(dependencies):
                removed_dep = dependencies.pop(index)

                # Record modification
                modification = ModificationRecord(
                    category=ModificationCategory.DEPENDENCIES,
                    action='remove',
                    details=f"Removed dependency: {removed_dep}",
                    previous_value=removed_dep,
                    new_value=None
                )
                self.session.modifications.append(modification)

                print(f"✓ Removed dependency '{removed_dep}'")
            else:
                print("Invalid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def _modify_risks(self) -> None:
        """
        Handle risk modifications.

        Displays current risks and provides options to add, remove, or modify
        implementation risks.

        Example:
            Risks in Plan
            =============

            Risks (2):
            1. HIGH: Security vulnerability in authentication
               Mitigation: Use industry-standard libraries
            2. MEDIUM: Performance degradation with large datasets

            Options:
            1. Add risk
            2. Remove risk
            3. Modify risk severity/mitigation
            4. Back to main menu

            Choice:
        """
        plan = self.session.current_plan.get('plan', {})
        risks = plan.get('risks', [])

        while True:
            print("\n" + "=" * 60)
            print("Risks in Plan")
            print("=" * 60)
            print()

            # Display current risks
            print(f"Risks ({len(risks)}):")
            if risks:
                for i, risk in enumerate(risks, 1):
                    if isinstance(risk, dict):
                        level = risk.get('level', 'MEDIUM').upper()
                        desc = risk.get('description', '')
                        mitigation = risk.get('mitigation', '')
                        print(f"  {i}. {level}: {desc}")
                        if mitigation:
                            print(f"     Mitigation: {mitigation}")
                    else:
                        print(f"  {i}. {risk}")
            else:
                print("  (none)")
            print()

            # Display options
            print("Options:")
            print("  1. Add risk")
            print("  2. Remove risk")
            print("  3. Modify risk severity/mitigation")
            print("  4. Back to main menu")
            print()

            choice = self._get_user_choice("Choice: ")

            if choice == '1':
                self._add_risk(risks)
            elif choice == '2':
                self._remove_risk(risks)
            elif choice == '3':
                self._modify_risk(risks)
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

    def _add_risk(self, risks: List) -> None:
        """
        Add a risk to the plan.

        Args:
            risks: List of risks
        """
        print()
        print("Enter risk information:")
        description = input("  Risk description: ").strip()
        if not description:
            print("Risk description cannot be empty.")
            return

        level = input("  Severity (high/medium/low) [medium]: ").strip().lower()
        if not level:
            level = "medium"
        elif level not in ["high", "medium", "low"]:
            print("Invalid severity. Using 'medium'.")
            level = "medium"

        mitigation = input("  Mitigation strategy (optional): ").strip()

        # Create risk dict
        risk_dict = {
            'description': description,
            'level': level
        }
        if mitigation:
            risk_dict['mitigation'] = mitigation

        # Add to list
        risks.append(risk_dict)

        # Record modification
        modification = ModificationRecord(
            category=ModificationCategory.RISKS,
            action='add',
            details=f"Added {level.upper()} risk: {description}",
            previous_value=None,
            new_value=risk_dict
        )
        self.session.modifications.append(modification)

        print(f"✓ Added risk '{description}'")

    def _remove_risk(self, risks: List) -> None:
        """
        Remove a risk from the plan.

        Args:
            risks: List of risks
        """
        if not risks:
            print("No risks in plan.")
            return

        print()
        print("Risks:")
        for i, risk in enumerate(risks, 1):
            if isinstance(risk, dict):
                desc = risk.get('description', str(risk))
            else:
                desc = str(risk)
            print(f"  {i}. {desc}")
        print()

        choice = self._get_user_choice("Enter number to remove (or 'c' to cancel): ")

        if choice == 'c':
            return

        try:
            index = int(choice) - 1
            if 0 <= index < len(risks):
                removed_risk = risks.pop(index)

                # Record modification
                if isinstance(removed_risk, dict):
                    desc = removed_risk.get('description', str(removed_risk))
                else:
                    desc = str(removed_risk)

                modification = ModificationRecord(
                    category=ModificationCategory.RISKS,
                    action='remove',
                    details=f"Removed risk: {desc}",
                    previous_value=removed_risk,
                    new_value=None
                )
                self.session.modifications.append(modification)

                print(f"✓ Removed risk")
            else:
                print("Invalid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def _modify_risk(self, risks: List) -> None:
        """
        Modify an existing risk's severity or mitigation.

        Args:
            risks: List of risks
        """
        if not risks:
            print("No risks in plan.")
            return

        print()
        print("Risks:")
        for i, risk in enumerate(risks, 1):
            if isinstance(risk, dict):
                desc = risk.get('description', str(risk))
            else:
                desc = str(risk)
            print(f"  {i}. {desc}")
        print()

        choice = self._get_user_choice("Enter number to modify (or 'c' to cancel): ")

        if choice == 'c':
            return

        try:
            index = int(choice) - 1
            if 0 <= index < len(risks):
                risk = risks[index]

                # Convert string risk to dict if needed
                if isinstance(risk, str):
                    risk = {'description': risk, 'level': 'medium'}
                    risks[index] = risk

                previous_risk = risk.copy()

                print()
                print("Modify risk (press Enter to keep current value):")

                # Modify severity
                current_level = risk.get('level', 'medium')
                new_level = input(f"  Severity ({current_level}): ").strip().lower()
                if new_level and new_level in ["high", "medium", "low"]:
                    risk['level'] = new_level

                # Modify mitigation
                current_mitigation = risk.get('mitigation', '')
                print(f"  Current mitigation: {current_mitigation if current_mitigation else '(none)'}")
                new_mitigation = input("  New mitigation: ").strip()
                if new_mitigation:
                    risk['mitigation'] = new_mitigation

                # Record modification
                modification = ModificationRecord(
                    category=ModificationCategory.RISKS,
                    action='modify',
                    details=f"Updated risk: {risk.get('description', '')}",
                    previous_value=previous_risk,
                    new_value=risk.copy()
                )
                self.session.modifications.append(modification)

                print("✓ Risk updated")
            else:
                print("Invalid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def _modify_effort(self) -> None:
        """
        Handle effort estimate modifications.

        Allows updating estimated duration, lines of code, and complexity score.

        Example:
            Effort Estimate
            ===============

            Current Estimate:
            - Duration: 4 hours
            - Lines of Code: ~300
            - Complexity: 5/10

            Enter new values (press Enter to keep current):
            Duration (4 hours): 6 hours
            Lines of Code (300): 400
            Complexity (5): 6

            ✓ Effort estimate updated
        """
        plan = self.session.current_plan.get('plan', {})

        print("\n" + "=" * 60)
        print("Effort Estimate")
        print("=" * 60)
        print()

        # Display current effort
        current_duration = plan.get('estimated_duration', 'Unknown')
        current_loc = plan.get('estimated_loc', 0)
        current_complexity = plan.get('complexity_score', 5)

        print("Current Estimate:")
        print(f"  Duration: {current_duration}")
        print(f"  Lines of Code: ~{current_loc}")
        print(f"  Complexity: {current_complexity}/10")
        print()

        # Get new values
        print("Enter new values (press Enter to keep current):")

        duration = input(f"  Duration ({current_duration}): ").strip()
        if not duration:
            duration = current_duration

        loc_str = input(f"  Lines of Code ({current_loc}): ").strip()
        if loc_str:
            try:
                loc = int(loc_str)
            except ValueError:
                print("Invalid number for LOC. Keeping current value.")
                loc = current_loc
        else:
            loc = current_loc

        complexity_str = input(f"  Complexity ({current_complexity}): ").strip()
        if complexity_str:
            try:
                complexity = int(complexity_str)
                if not (1 <= complexity <= 10):
                    print("Complexity must be 1-10. Keeping current value.")
                    complexity = current_complexity
            except ValueError:
                print("Invalid number for complexity. Keeping current value.")
                complexity = current_complexity
        else:
            complexity = current_complexity

        # Update plan
        previous_effort = {
            'duration': current_duration,
            'loc': current_loc,
            'complexity': current_complexity
        }

        plan['estimated_duration'] = duration
        plan['estimated_loc'] = loc
        plan['complexity_score'] = complexity

        new_effort = {
            'duration': duration,
            'loc': loc,
            'complexity': complexity
        }

        # Record modification
        modification = ModificationRecord(
            category=ModificationCategory.EFFORT,
            action='modify',
            details=f"Updated effort: {duration}, ~{loc} LOC, complexity {complexity}/10",
            previous_value=previous_effort,
            new_value=new_effort
        )
        self.session.modifications.append(modification)

        print("✓ Effort estimate updated")

    def _handle_undo(self) -> None:
        """
        Undo the last modification.

        Reverts the most recent change and updates the plan state accordingly.
        """
        if not self.session.has_modifications:
            print("\nNo modifications to undo.")
            return

        # Get last modification
        last_mod = self.session.modifications.pop()

        # Revert the change
        plan = self.session.current_plan.get('plan', {})

        if last_mod.category == ModificationCategory.FILES:
            # Undo file modification
            if last_mod.action == 'add':
                # Remove the added file
                file_list_key = 'files_to_create' if 'create' in last_mod.details else 'files_to_modify'
                file_list = plan.get(file_list_key, [])
                if last_mod.new_value in file_list:
                    file_list.remove(last_mod.new_value)
            elif last_mod.action == 'remove':
                # Re-add the removed file
                file_list_key = 'files_to_create' if 'create' in last_mod.details else 'files_to_modify'
                file_list = plan.get(file_list_key, [])
                if last_mod.previous_value not in file_list:
                    file_list.append(last_mod.previous_value)

        elif last_mod.category == ModificationCategory.DEPENDENCIES:
            dependencies = plan.get('external_dependencies', [])
            if last_mod.action == 'add':
                if last_mod.new_value in dependencies:
                    dependencies.remove(last_mod.new_value)
            elif last_mod.action == 'remove':
                if last_mod.previous_value not in dependencies:
                    dependencies.append(last_mod.previous_value)

        elif last_mod.category == ModificationCategory.RISKS:
            risks = plan.get('risks', [])
            if last_mod.action == 'add':
                if last_mod.new_value in risks:
                    risks.remove(last_mod.new_value)
            elif last_mod.action == 'remove':
                if last_mod.previous_value not in risks:
                    risks.append(last_mod.previous_value)
            elif last_mod.action == 'modify':
                # Find and revert the modified risk
                for i, risk in enumerate(risks):
                    if risk == last_mod.new_value:
                        risks[i] = last_mod.previous_value
                        break

        elif last_mod.category == ModificationCategory.EFFORT:
            # Revert effort estimate
            if last_mod.previous_value:
                plan['estimated_duration'] = last_mod.previous_value['duration']
                plan['estimated_loc'] = last_mod.previous_value['loc']
                plan['complexity_score'] = last_mod.previous_value['complexity']

        print(f"\n✓ Undone: {last_mod}")

    def _finalize_modifications(self) -> Optional[Dict[str, Any]]:
        """
        Finalize modifications and save updated plan.

        Displays modification summary, increments version, saves the plan,
        and returns the updated plan data.

        Returns:
            Updated plan dictionary, or None if no modifications were made

        Example:
            Modification Summary
            ====================

            Total Modifications: 4
            - FILES: add - Added src/new_module.py to create
            - DEPENDENCIES: add - Added requests 2.28.0 - HTTP client
            - RISKS: add - Added HIGH risk: Security vulnerability
            - EFFORT: modify - Updated effort: 6 hours, ~400 LOC, complexity 6/10

            Plan version incremented: 1 → 2

            Save modifications? (y/n):
        """
        if not self.session.has_modifications:
            print("\nNo modifications made. Plan unchanged.")
            return None

        # Display modification summary
        self._display_modification_summary()

        # Confirm save
        print()
        confirm = self._get_user_choice("Save modifications? (y/n): ")

        if confirm not in ['y', 'yes']:
            print("Modifications discarded. Plan unchanged.")
            return None

        # Increment version
        new_version = self.session.version + 1
        self.session.current_plan['version'] = new_version

        # Save updated plan
        try:
            from .plan_persistence import save_plan_version
            save_path = save_plan_version(
                self.task_id,
                self.session.current_plan,
                modifications=self.session.modifications
            )
            print(f"\n✓ Plan saved to: {save_path}")
            print(f"✓ Version incremented: {self.session.version} → {new_version}")

            return self.session.current_plan

        except Exception as e:
            logger.error(f"Failed to save modified plan: {e}")
            raise PlanModificationError(f"Failed to save plan: {e}") from e

    def _display_modification_summary(self) -> None:
        """
        Display summary of all modifications made.

        Example:
            Modification Summary
            ====================

            Total Modifications: 4
            - FILES: add - Added src/new_module.py to create
            - DEPENDENCIES: add - Added requests 2.28.0 - HTTP client
            - RISKS: add - Added HIGH risk: Security vulnerability
            - EFFORT: modify - Updated effort: 6 hours, ~400 LOC, complexity 6/10
        """
        print("\n" + "=" * 60)
        print("Modification Summary")
        print("=" * 60)
        print()

        print(f"Total Modifications: {self.session.modification_count}")
        for mod in self.session.modifications:
            print(f"  - {mod}")


# Module exports
__all__ = [
    "ModificationCategory",
    "ModificationRecord",
    "ModificationSession",
    "PlanModifier",
    "PlanModificationError"
]
