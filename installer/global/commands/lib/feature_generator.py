"""
Feature task file generator module.

This module generates task markdown files with complexity metadata,
maintaining proper hierarchical IDs and ensuring no duplicates.

Key Features:
- Hierarchical task ID generation (TASK-001.2.05 format)
- Markdown file generation with frontmatter
- Complexity metadata embedding
- Sub-task relationship tracking
- Automatic file placement in correct directories

Usage:
    from feature_generator import TaskFileGenerator

    generator = TaskFileGenerator()
    generator.generate_task_files(subtasks, feature_id, epic_id)
"""

import logging
import os
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class TaskFileMetadata:
    """Metadata for generated task file.

    Attributes:
        task_id: Generated task ID
        file_path: Path where file was created
        title: Task title
        complexity: Complexity level
        parent_task: Parent task ID (if subtask)
        status: Initial task status
    """
    task_id: str
    file_path: str
    title: str
    complexity: str
    parent_task: Optional[str]
    status: str


class TaskFileGenerator:
    """Generates task markdown files with proper formatting and metadata.

    This generator creates task files following the project's markdown format
    with YAML frontmatter and maintains hierarchical task relationships.
    """

    # Task directories
    BACKLOG_DIR = "tasks/backlog"
    IN_PROGRESS_DIR = "tasks/in_progress"

    # Default task template
    TASK_TEMPLATE = """---
id: {task_id}
title: {title}
status: {status}
created: {created}
updated: {updated}
feature_id: {feature_id}
epic_id: {epic_id}
parent_task: {parent_task}
complexity: {complexity}
estimated_hours: {estimated_hours}
priority: {priority}
tags: {tags}
---

# {title}

## Description
{description}

## Files to Create/Modify
{files_section}

## Acceptance Criteria
{acceptance_criteria}

## Dependencies
{dependencies}

## Implementation Notes
{implementation_notes}

## Complexity Analysis
- **Complexity Level**: {complexity}
- **Estimated Hours**: {estimated_hours}
- **Breakdown Strategy**: {breakdown_strategy}

{complexity_details}
"""

    def __init__(self, project_root: Optional[str] = None):
        """Initialize task file generator.

        Args:
            project_root: Project root directory (default: current directory)
        """
        self.project_root = Path(project_root or os.getcwd())
        logger.info(f"TaskFileGenerator initialized at {self.project_root}")

    def generate_task_files(
        self,
        subtasks: List[Dict[str, Any]],
        feature_id: str,
        epic_id: str,
        output_dir: str = BACKLOG_DIR
    ) -> List[TaskFileMetadata]:
        """Generate markdown files for all subtasks.

        Args:
            subtasks: List of subtask dictionaries
            feature_id: Parent feature ID (e.g., FEAT-001)
            epic_id: Parent epic ID (e.g., EPIC-001)
            output_dir: Directory to create files in (default: backlog)

        Returns:
            List of TaskFileMetadata for generated files
        """
        logger.info(
            f"Generating {len(subtasks)} task files for feature {feature_id}"
        )

        generated_files = []
        output_path = self.project_root / output_dir

        # Ensure output directory exists
        output_path.mkdir(parents=True, exist_ok=True)

        for i, subtask in enumerate(subtasks, 1):
            try:
                # Generate task ID if not present
                if "id" not in subtask:
                    subtask["id"] = self._generate_next_task_id(
                        epic_id, feature_id, existing_ids=[s.get("id") for s in subtasks if "id" in s]
                    )

                # Generate file
                file_metadata = self._generate_single_file(
                    subtask, feature_id, epic_id, output_path
                )
                generated_files.append(file_metadata)

                logger.info(f"Generated file: {file_metadata.file_path}")

            except Exception as e:
                logger.error(
                    f"Error generating file for subtask {i}: {e}",
                    exc_info=True
                )

        logger.info(f"Successfully generated {len(generated_files)} task files")
        return generated_files

    def _generate_single_file(
        self,
        subtask: Dict[str, Any],
        feature_id: str,
        epic_id: str,
        output_path: Path
    ) -> TaskFileMetadata:
        """Generate a single task file.

        Args:
            subtask: Subtask data dictionary
            feature_id: Parent feature ID
            epic_id: Parent epic ID
            output_path: Output directory path

        Returns:
            TaskFileMetadata for the generated file
        """
        task_id = subtask["id"]
        title = subtask.get("title", "Untitled Task")

        # Generate filename
        filename = self._generate_filename(task_id, title)
        file_path = output_path / filename

        # Generate file content
        content = self._generate_file_content(subtask, feature_id, epic_id)

        # Write file
        file_path.write_text(content, encoding="utf-8")

        return TaskFileMetadata(
            task_id=task_id,
            file_path=str(file_path),
            title=title,
            complexity=subtask.get("complexity", "medium"),
            parent_task=subtask.get("parent_task"),
            status=subtask.get("status", "backlog")
        )

    def _generate_file_content(
        self,
        subtask: Dict[str, Any],
        feature_id: str,
        epic_id: str
    ) -> str:
        """Generate markdown content for task file.

        Args:
            subtask: Subtask data
            feature_id: Parent feature ID
            epic_id: Parent epic ID

        Returns:
            Formatted markdown content
        """
        now = datetime.now().isoformat()

        # Format files section
        files = subtask.get("files", [])
        if files:
            files_section = "\n".join(f"- `{f}`" for f in files)
        else:
            files_section = "- _(No specific files listed)_"

        # Format acceptance criteria
        criteria = subtask.get("acceptance_criteria", [])
        if criteria:
            acceptance_criteria = "\n".join(f"- [ ] {c}" for c in criteria)
        else:
            acceptance_criteria = "- [ ] Implementation complete\n- [ ] Tests passing\n- [ ] Code reviewed"

        # Format dependencies
        deps = subtask.get("dependencies", [])
        if deps:
            dependencies = "\n".join(f"- {d}" for d in deps)
        else:
            dependencies = "- _(No dependencies)_"

        # Format complexity details
        complexity_details = self._format_complexity_details(subtask)

        # Fill template
        content = self.TASK_TEMPLATE.format(
            task_id=subtask["id"],
            title=subtask.get("title", "Untitled Task"),
            status=subtask.get("status", "backlog"),
            created=now,
            updated=now,
            feature_id=feature_id,
            epic_id=epic_id,
            parent_task=subtask.get("parent_task", ""),
            complexity=subtask.get("complexity", "medium"),
            estimated_hours=subtask.get("estimated_hours", 4),
            priority=subtask.get("priority", "medium"),
            tags=", ".join(subtask.get("tags", ["generated", "breakdown"])),
            description=subtask.get("description", "_(Auto-generated from feature breakdown)_"),
            files_section=files_section,
            acceptance_criteria=acceptance_criteria,
            dependencies=dependencies,
            implementation_notes=subtask.get("implementation_notes", "_(See parent feature for context)_"),
            breakdown_strategy=subtask.get("breakdown_strategy", "automatic"),
            complexity_details=complexity_details
        )

        return content

    def _format_complexity_details(self, subtask: Dict[str, Any]) -> str:
        """Format complexity analysis details.

        Args:
            subtask: Subtask data

        Returns:
            Formatted complexity details section
        """
        details = []

        # Component type
        if "component_type" in subtask:
            details.append(f"- **Component Type**: {subtask['component_type']}")

        # Phase information
        if "phase_name" in subtask:
            details.append(f"- **Phase**: {subtask['phase']} - {subtask['phase_name']}")

        # Module information
        if "module" in subtask:
            details.append(f"- **Module**: {subtask['module']}")

        # File count
        files = subtask.get("files", [])
        if files:
            details.append(f"- **Files**: {len(files)} file(s)")

        if not details:
            return ""

        return "\n" + "\n".join(details)

    def _generate_filename(self, task_id: str, title: str) -> str:
        """Generate filename from task ID and title.

        Args:
            task_id: Task ID (e.g., TASK-001.2.05)
            title: Task title

        Returns:
            Filename string (e.g., TASK-001.2.05-implement-authentication.md)
        """
        # Convert title to slug
        slug = title.lower()
        slug = slug.replace(" ", "-")
        slug = "".join(c for c in slug if c.isalnum() or c == "-")
        slug = slug[:50]  # Limit length

        return f"{task_id}-{slug}.md"

    def _generate_next_task_id(
        self,
        epic_id: str,
        feature_id: str,
        existing_ids: List[str]
    ) -> str:
        """Generate next hierarchical task ID.

        Format: TASK-{epic_num}.{feature_num}.{task_num}
        Example: TASK-001.2.05

        Args:
            epic_id: Epic ID (e.g., EPIC-001)
            feature_id: Feature ID (e.g., FEAT-001.2)
            existing_ids: List of existing task IDs for this feature

        Returns:
            Next available task ID
        """
        # Extract numbers
        epic_num = self._extract_number(epic_id, "EPIC-")
        feature_num = self._extract_number(feature_id, r"FEAT-\d+\.")

        # Find highest task number
        max_task_num = 0
        pattern_prefix = f"TASK-{epic_num}.{feature_num}."

        for task_id in existing_ids:
            if task_id and task_id.startswith(pattern_prefix):
                try:
                    task_num_str = task_id.replace(pattern_prefix, "").split("-")[0]
                    task_num = int(task_num_str)
                    max_task_num = max(max_task_num, task_num)
                except (ValueError, IndexError):
                    continue

        # Also check existing files
        for directory in [self.BACKLOG_DIR, self.IN_PROGRESS_DIR]:
            dir_path = self.project_root / directory
            if dir_path.exists():
                for file_path in dir_path.glob(f"{pattern_prefix}*.md"):
                    try:
                        task_num_str = file_path.stem.replace(pattern_prefix, "").split("-")[0]
                        task_num = int(task_num_str)
                        max_task_num = max(max_task_num, task_num)
                    except (ValueError, IndexError):
                        continue

        # Generate next ID
        next_num = max_task_num + 1
        return f"TASK-{epic_num}.{feature_num}.{next_num:02d}"

    def _extract_number(self, id_string: str, prefix: str) -> str:
        """Extract numeric portion from ID string.

        Args:
            id_string: ID string (e.g., EPIC-001 or FEAT-001.2)
            prefix: Prefix pattern to remove

        Returns:
            Numeric portion as string
        """
        import re
        # Remove prefix
        no_prefix = re.sub(f"^{prefix}", "", id_string)
        # Extract first number
        match = re.search(r"(\d+)", no_prefix)
        return match.group(1) if match else "001"

    def generate_summary_file(
        self,
        generated_files: List[TaskFileMetadata],
        feature_id: str,
        output_path: Optional[Path] = None
    ) -> str:
        """Generate summary file for all generated tasks.

        Args:
            generated_files: List of generated file metadata
            feature_id: Feature ID
            output_path: Optional output path (default: project root)

        Returns:
            Path to generated summary file
        """
        if not output_path:
            output_path = self.project_root

        summary_filename = f"{feature_id}-breakdown-summary.md"
        summary_path = output_path / summary_filename

        # Generate summary content
        lines = [
            f"# Task Breakdown Summary - {feature_id}",
            "",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            f"## Generated Tasks ({len(generated_files)})",
            ""
        ]

        for metadata in generated_files:
            lines.append(f"### {metadata.task_id}: {metadata.title}")
            lines.append(f"- **Complexity**: {metadata.complexity}")
            lines.append(f"- **Status**: {metadata.status}")
            if metadata.parent_task:
                lines.append(f"- **Parent Task**: {metadata.parent_task}")
            lines.append(f"- **File**: `{metadata.file_path}`")
            lines.append("")

        # Statistics
        complexity_dist = {}
        for metadata in generated_files:
            complexity_dist[metadata.complexity] = complexity_dist.get(metadata.complexity, 0) + 1

        lines.append("## Statistics")
        lines.append(f"- Total tasks: {len(generated_files)}")
        lines.append("- Complexity distribution:")
        for complexity, count in complexity_dist.items():
            lines.append(f"  - {complexity.capitalize()}: {count}")

        content = "\n".join(lines)
        summary_path.write_text(content, encoding="utf-8")

        logger.info(f"Generated summary file: {summary_path}")
        return str(summary_path)
