"""
Plan Markdown Renderer - Renders implementation plans as human-readable markdown.

Part of TASK-027: Convert Implementation Plan Storage from JSON to Markdown.

This module renders implementation plans from Python dictionaries to markdown format
using Jinja2 templates and frontmatter metadata. This improves human readability,
git diffs, and aligns with John Hubbard's proven workflow pattern.

Author: Claude (Anthropic)
Created: 2025-10-18
"""

from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader
import frontmatter
from datetime import datetime


class PlanMarkdownRendererError(Exception):
    """Raised when markdown rendering operations fail."""
    pass


class PlanMarkdownRenderer:
    """Renders implementation plans as human-readable markdown with frontmatter."""

    def __init__(self):
        """Initialize the renderer with Jinja2 template environment."""
        template_dir = Path(__file__).parent / "templates"
        if not template_dir.exists():
            raise PlanMarkdownRendererError(
                f"Template directory not found: {template_dir}"
            )

        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )

        # Register helper functions
        self.env.globals['status_icon'] = self._status_icon

        try:
            self.template = self.env.get_template("implementation_plan.md.j2")
        except Exception as e:
            raise PlanMarkdownRendererError(
                f"Failed to load implementation plan template: {e}"
            ) from e

    def render(self, plan: Dict[str, Any]) -> str:
        """
        Render plan dict as markdown string with frontmatter.

        Args:
            plan: Implementation plan dictionary with structure:
                {
                    "task_id": "TASK-XXX",
                    "saved_at": "ISO timestamp",
                    "version": 1,
                    "plan": {
                        "files_to_create": [...],
                        "files_to_modify": [...],
                        "external_dependencies": [...],
                        "estimated_duration": "...",
                        "estimated_loc": 123,
                        "complexity_score": 5,
                        "risks": [...]
                    },
                    "architectural_review": {
                        "score": 85,
                        "solid_compliance": {...},
                        "warnings": [...]
                    }
                }

        Returns:
            Markdown string with frontmatter metadata

        Raises:
            PlanMarkdownRendererError: If rendering fails

        Example:
            >>> renderer = PlanMarkdownRenderer()
            >>> plan = {"task_id": "TASK-042", "plan": {...}}
            >>> markdown = renderer.render(plan)
            >>> print(markdown[:50])
            ---
            task_id: TASK-042
            saved_at: 2025-10-18...
        """
        try:
            # Extract metadata for frontmatter
            metadata = self._extract_metadata(plan)

            # Prepare template context (flattened for easier template access)
            context = self._prepare_context(plan)

            # Render template
            body = self.template.render(**context)

            # Combine frontmatter + body
            post = frontmatter.Post(body, **metadata)
            markdown = frontmatter.dumps(post)

            return markdown

        except Exception as e:
            raise PlanMarkdownRendererError(
                f"Failed to render plan as markdown: {e}"
            ) from e

    def save_markdown(self, plan: Dict[str, Any], output_path: Path) -> None:
        """
        Render and save plan as markdown file.

        Args:
            plan: Implementation plan dictionary
            output_path: Path where markdown file should be saved

        Raises:
            PlanMarkdownRendererError: If save operation fails

        Example:
            >>> renderer = PlanMarkdownRenderer()
            >>> plan = {"task_id": "TASK-042", "plan": {...}}
            >>> renderer.save_markdown(plan, Path("plan.md"))
        """
        try:
            markdown = self.render(plan)

            # Ensure parent directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Write markdown to file
            output_path.write_text(markdown, encoding='utf-8')

        except Exception as e:
            raise PlanMarkdownRendererError(
                f"Failed to save markdown to {output_path}: {e}"
            ) from e

    def _extract_metadata(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract metadata for frontmatter from plan dict.

        Args:
            plan: Full plan dictionary

        Returns:
            Metadata dictionary for frontmatter
        """
        plan_data = plan.get('plan', {})
        arch_review = plan.get('architectural_review', {})

        metadata = {
            'task_id': plan.get('task_id'),
            'saved_at': plan.get('saved_at'),
            'version': plan.get('version', 1),
            'complexity_score': plan_data.get('complexity_score'),
            'architectural_review_score': arch_review.get('score'),
            'status': plan.get('status', 'draft')
        }

        # Include empty_plan marker if present
        if plan.get('empty_plan'):
            metadata['empty_plan'] = True

        return metadata

    def _prepare_context(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare template context by flattening plan structure.

        Args:
            plan: Full plan dictionary

        Returns:
            Flattened context dict for template rendering
        """
        plan_data = plan.get('plan', {})

        # Start with top-level fields
        context = {
            'task_id': plan.get('task_id'),
            'created_at': plan.get('saved_at', datetime.now().isoformat()),
            'status': plan.get('status', 'Draft'),
        }

        # Add all plan fields
        context.update({
            'summary': plan_data.get('summary', ''),
            'files_to_create': plan_data.get('files_to_create', []),
            'files_to_modify': plan_data.get('files_to_modify', []),
            'external_dependencies': plan_data.get('external_dependencies', []),
            'estimated_duration': plan_data.get('estimated_duration'),
            'estimated_loc': plan_data.get('estimated_loc'),
            'complexity_score': plan_data.get('complexity_score'),
            'complexity_level': self._get_complexity_level(
                plan_data.get('complexity_score')
            ),
            'risks': plan_data.get('risks', []),
            'implementation_notes': plan_data.get('implementation_notes', []),
            'phases': plan_data.get('phases', []),
            'test_summary': plan_data.get('test_summary'),
        })

        # Add architectural review if present
        if 'architectural_review' in plan:
            context['architectural_review'] = plan['architectural_review']

        return context

    def _get_complexity_level(self, score: Any) -> str:
        """
        Convert numeric complexity score to descriptive level.

        Args:
            score: Complexity score (0-10)

        Returns:
            Descriptive level (Simple, Medium, Complex, Very Complex)
        """
        if score is None:
            return 'Unknown'

        try:
            score = int(score)
            if score <= 3:
                return 'Simple'
            elif score <= 6:
                return 'Medium'
            elif score <= 8:
                return 'Complex'
            else:
                return 'Very Complex'
        except (ValueError, TypeError):
            return 'Unknown'

    def _status_icon(self, status: str) -> str:
        """
        Convert status string to emoji icon.

        Args:
            status: Status string (pass, warn, fail, info)

        Returns:
            Emoji icon for status
        """
        icons = {
            'pass': '✅',
            'warn': '⚠️',
            'fail': '❌',
            'info': 'ℹ️',
            'good': '✅',
            'warning': '⚠️',
            'error': '❌',
        }
        return icons.get(status.lower() if isinstance(status, str) else '', '•')


# Module exports
__all__ = [
    "PlanMarkdownRenderer",
    "PlanMarkdownRendererError"
]
