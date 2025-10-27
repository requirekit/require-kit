"""
Breakdown strategies using Strategy pattern.

This module implements different task breakdown strategies based on complexity levels.
Each strategy follows the Strategy pattern for extensibility and testability.

Strategies:
- NoBreakdownStrategy: Complexity 1-3, no breakdown needed
- LogicalBreakdownStrategy: Complexity 4-6, break by logical components
- FileBasedBreakdownStrategy: Complexity 7-8, break by file groupings
- PhaseBasedBreakdownStrategy: Complexity 9-10, break by implementation phases

All strategies follow the BreakdownStrategy protocol for type safety.
"""

import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Protocol
from dataclasses import dataclass

try:
    from .complexity_models import ComplexityScore
except ImportError:
    from complexity_models import ComplexityScore


logger = logging.getLogger(__name__)


class BreakdownStrategy(Protocol):
    """Protocol for task breakdown strategies.

    Each strategy implements a different approach to breaking down
    complex tasks into manageable subtasks.
    """

    def breakdown(
        self,
        task_data: Dict[str, Any],
        complexity_score: ComplexityScore
    ) -> List[Dict[str, Any]]:
        """Break down a task into subtasks.

        Args:
            task_data: Original task data
            complexity_score: Calculated complexity score

        Returns:
            List of subtask dictionaries (empty list if no breakdown)
        """
        ...


class NoBreakdownStrategy:
    """Strategy for simple tasks (complexity 1-3).

    For simple tasks, no breakdown is needed. The task can be
    implemented as-is without additional decomposition.

    Scoring:
    - Complexity 1-3: Simple, single-responsibility task
    - 0-2 files, familiar patterns, low risk
    """

    def breakdown(
        self,
        task_data: Dict[str, Any],
        complexity_score: ComplexityScore
    ) -> List[Dict[str, Any]]:
        """Return empty list - no breakdown needed.

        Args:
            task_data: Original task data
            complexity_score: Complexity score (should be 1-3)

        Returns:
            Empty list (no subtasks)
        """
        logger.info(
            f"No breakdown needed for {task_data['id']} "
            f"(complexity={complexity_score.total_score})"
        )
        return []


class LogicalBreakdownStrategy:
    """Strategy for moderate complexity tasks (complexity 4-6).

    Breaks down tasks by logical components or responsibilities.
    Suitable for multi-file changes with clear separation of concerns.

    Breakdown approach:
    - Identify logical components (UI, business logic, data access)
    - Create one subtask per major component
    - Maintain component dependencies

    Example:
        Original: "Implement user authentication"
        Subtasks:
        1. Implement authentication service (business logic)
        2. Create user repository (data access)
        3. Build login form (UI)
        4. Add authentication tests
    """

    def breakdown(
        self,
        task_data: Dict[str, Any],
        complexity_score: ComplexityScore
    ) -> List[Dict[str, Any]]:
        """Break down by logical components.

        Args:
            task_data: Original task data
            complexity_score: Complexity score (should be 4-6)

        Returns:
            List of component-based subtasks
        """
        logger.info(
            f"Applying logical breakdown for {task_data['id']} "
            f"(complexity={complexity_score.total_score})"
        )

        subtasks = []
        task_id = task_data["id"]
        base_title = task_data["title"]

        # Identify components from patterns and files
        files = task_data.get("files", [])
        patterns = task_data.get("patterns", [])

        # Stub: Simple component detection
        components = self._identify_components(files, patterns)

        for i, component in enumerate(components, 1):
            subtask = {
                "id": f"{task_id}.{i}",
                "title": f"{base_title} - {component['name']}",
                "description": component["description"],
                "files": component["files"],
                "complexity": "medium",
                "estimated_hours": component.get("estimated_hours", 4),
                "parent_task": task_id,
                "component_type": component["type"]
            }
            subtasks.append(subtask)

        logger.info(f"Generated {len(subtasks)} logical component subtasks")
        return subtasks

    def _identify_components(
        self,
        files: List[str],
        patterns: List[str]
    ) -> List[Dict[str, Any]]:
        """Identify logical components from files and patterns.

        Args:
            files: List of files to be created/modified
            patterns: Design patterns used

        Returns:
            List of component definitions
        """
        # Stub implementation - simplified logic
        components = []

        # Group files by type
        ui_files = [f for f in files if any(x in f.lower() for x in ["view", "ui", "component", "page"])]
        logic_files = [f for f in files if any(x in f.lower() for x in ["service", "manager", "handler"])]
        data_files = [f for f in files if any(x in f.lower() for x in ["repository", "model", "entity"])]
        test_files = [f for f in files if "test" in f.lower()]

        if ui_files:
            components.append({
                "name": "UI Components",
                "type": "ui",
                "files": ui_files,
                "description": "User interface components and views",
                "estimated_hours": len(ui_files) * 2
            })

        if logic_files:
            components.append({
                "name": "Business Logic",
                "type": "logic",
                "files": logic_files,
                "description": "Core business logic and services",
                "estimated_hours": len(logic_files) * 3
            })

        if data_files:
            components.append({
                "name": "Data Access",
                "type": "data",
                "files": data_files,
                "description": "Data models and repository layer",
                "estimated_hours": len(data_files) * 2
            })

        if test_files:
            components.append({
                "name": "Tests",
                "type": "test",
                "files": test_files,
                "description": "Unit and integration tests",
                "estimated_hours": len(test_files) * 1.5
            })

        # Fallback if no clear grouping
        if not components:
            components.append({
                "name": "Implementation",
                "type": "implementation",
                "files": files,
                "description": "Implementation of all components",
                "estimated_hours": len(files) * 2
            })

        return components


class FileBasedBreakdownStrategy:
    """Strategy for high complexity tasks (complexity 7-8).

    Breaks down tasks by file groupings or modules.
    Suitable for complex multi-component changes.

    Breakdown approach:
    - Group related files together
    - Create subtasks per file group (2-3 files per subtask)
    - Maintain file dependencies and order

    Example:
        Original: "Build user management system" (15 files)
        Subtasks:
        1. User entity and models (user.py, user_dto.py, user_schema.py)
        2. User repository and database (user_repository.py, migrations/)
        3. User service and validation (user_service.py, validators.py)
        4. User API endpoints (user_routes.py, user_handlers.py)
        5. User tests (test_user.py, test_user_api.py)
    """

    def breakdown(
        self,
        task_data: Dict[str, Any],
        complexity_score: ComplexityScore
    ) -> List[Dict[str, Any]]:
        """Break down by file groupings.

        Args:
            task_data: Original task data
            complexity_score: Complexity score (should be 7-8)

        Returns:
            List of file-based subtasks
        """
        logger.info(
            f"Applying file-based breakdown for {task_data['id']} "
            f"(complexity={complexity_score.total_score})"
        )

        subtasks = []
        task_id = task_data["id"]
        base_title = task_data["title"]
        files = task_data.get("files", [])

        # Group files by module/package
        file_groups = self._group_files_by_module(files)

        for i, group in enumerate(file_groups, 1):
            subtask = {
                "id": f"{task_id}.{i}",
                "title": f"{base_title} - {group['module_name']}",
                "description": f"Implement {group['module_name']} module",
                "files": group["files"],
                "complexity": "medium",
                "estimated_hours": len(group["files"]) * 2,
                "parent_task": task_id,
                "module": group["module_name"]
            }
            subtasks.append(subtask)

        logger.info(f"Generated {len(subtasks)} file-based subtasks")
        return subtasks

    def _group_files_by_module(self, files: List[str]) -> List[Dict[str, Any]]:
        """Group files by module or package.

        Args:
            files: List of file paths

        Returns:
            List of file groups with metadata
        """
        # Stub implementation - simplified grouping
        groups = {}

        for file in files:
            # Extract module name (directory or prefix)
            parts = file.split("/")
            module_name = parts[0] if len(parts) > 1 else "core"

            if module_name not in groups:
                groups[module_name] = {
                    "module_name": module_name.capitalize(),
                    "files": []
                }

            groups[module_name]["files"].append(file)

        # Convert to list and limit files per group (max 3)
        result = []
        for group_data in groups.values():
            files_in_group = group_data["files"]

            # Split large groups
            if len(files_in_group) > 3:
                for i in range(0, len(files_in_group), 3):
                    chunk = files_in_group[i:i+3]
                    result.append({
                        "module_name": f"{group_data['module_name']} (Part {i//3 + 1})",
                        "files": chunk
                    })
            else:
                result.append(group_data)

        return result


class PhaseBasedBreakdownStrategy:
    """Strategy for very high complexity tasks (complexity 9-10).

    Breaks down tasks by implementation phases.
    Suitable for complex features requiring staged implementation.

    Breakdown approach:
    - Identify implementation phases (foundation → core → advanced)
    - Create sequential subtasks per phase
    - Each phase builds on previous phases

    Phases:
    1. Foundation: Core data models, interfaces, basic structure
    2. Core Implementation: Main functionality, business logic
    3. Integration: External services, APIs, database integration
    4. Advanced Features: Optional features, optimizations, edge cases
    5. Testing & Documentation: Comprehensive tests, documentation

    Example:
        Original: "Build payment processing system"
        Subtasks:
        1. Phase 1: Payment models and interfaces
        2. Phase 2: Payment service core logic
        3. Phase 3: Payment gateway integration
        4. Phase 4: Advanced features (refunds, webhooks)
        5. Phase 5: Payment tests and documentation
    """

    # Standard implementation phases
    PHASES = [
        {
            "name": "Foundation",
            "description": "Core data models, interfaces, and basic structure",
            "complexity": "medium",
            "estimated_hours": 8
        },
        {
            "name": "Core Implementation",
            "description": "Main functionality and business logic",
            "complexity": "high",
            "estimated_hours": 12
        },
        {
            "name": "Integration",
            "description": "External services, APIs, and database integration",
            "complexity": "high",
            "estimated_hours": 10
        },
        {
            "name": "Advanced Features",
            "description": "Optional features, optimizations, edge cases",
            "complexity": "medium",
            "estimated_hours": 8
        },
        {
            "name": "Testing & Documentation",
            "description": "Comprehensive tests and documentation",
            "complexity": "medium",
            "estimated_hours": 6
        }
    ]

    def breakdown(
        self,
        task_data: Dict[str, Any],
        complexity_score: ComplexityScore
    ) -> List[Dict[str, Any]]:
        """Break down by implementation phases.

        Args:
            task_data: Original task data
            complexity_score: Complexity score (should be 9-10)

        Returns:
            List of phase-based subtasks
        """
        logger.info(
            f"Applying phase-based breakdown for {task_data['id']} "
            f"(complexity={complexity_score.total_score})"
        )

        subtasks = []
        task_id = task_data["id"]
        base_title = task_data["title"]
        files = task_data.get("files", [])

        # Distribute files across phases
        files_per_phase = self._distribute_files_to_phases(files)

        for i, phase in enumerate(self.PHASES, 1):
            phase_files = files_per_phase.get(phase["name"], [])

            # Skip empty phases
            if not phase_files and i not in [1, len(self.PHASES)]:
                continue

            subtask = {
                "id": f"{task_id}.{i}",
                "title": f"{base_title} - Phase {i}: {phase['name']}",
                "description": phase["description"],
                "files": phase_files,
                "complexity": phase["complexity"],
                "estimated_hours": phase["estimated_hours"],
                "parent_task": task_id,
                "phase": i,
                "phase_name": phase["name"],
                "dependencies": [f"{task_id}.{i-1}"] if i > 1 else []
            }
            subtasks.append(subtask)

        logger.info(f"Generated {len(subtasks)} phase-based subtasks")
        return subtasks

    def _distribute_files_to_phases(self, files: List[str]) -> Dict[str, List[str]]:
        """Distribute files to implementation phases.

        Args:
            files: List of file paths

        Returns:
            Dictionary mapping phase names to file lists
        """
        # Stub implementation - simplified distribution
        distribution = {
            "Foundation": [],
            "Core Implementation": [],
            "Integration": [],
            "Advanced Features": [],
            "Testing & Documentation": []
        }

        for file in files:
            file_lower = file.lower()

            # Categorize by file type
            if any(x in file_lower for x in ["model", "entity", "dto", "interface"]):
                distribution["Foundation"].append(file)
            elif "test" in file_lower:
                distribution["Testing & Documentation"].append(file)
            elif any(x in file_lower for x in ["api", "client", "integration"]):
                distribution["Integration"].append(file)
            elif any(x in file_lower for x in ["service", "handler", "manager"]):
                distribution["Core Implementation"].append(file)
            else:
                distribution["Advanced Features"].append(file)

        return distribution


# Strategy registry for easy lookup
STRATEGY_REGISTRY: Dict[str, BreakdownStrategy] = {
    "none": NoBreakdownStrategy(),
    "logical": LogicalBreakdownStrategy(),
    "file_based": FileBasedBreakdownStrategy(),
    "phase_based": PhaseBasedBreakdownStrategy()
}


def get_strategy(complexity_score: int) -> BreakdownStrategy:
    """Get appropriate strategy for complexity score.

    Args:
        complexity_score: Task complexity score (1-10)

    Returns:
        Appropriate BreakdownStrategy instance
    """
    if complexity_score <= 3:
        return STRATEGY_REGISTRY["none"]
    elif complexity_score <= 6:
        return STRATEGY_REGISTRY["logical"]
    elif complexity_score <= 8:
        return STRATEGY_REGISTRY["file_based"]
    else:
        return STRATEGY_REGISTRY["phase_based"]
