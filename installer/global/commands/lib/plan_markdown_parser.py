"""
Plan Markdown Parser - Parse markdown implementation plans back into structured data.

Part of TASK-027: Convert Implementation Plan Storage from JSON to Markdown.

This module parses markdown-formatted implementation plans (with frontmatter) back
into Python dictionaries for programmatic access. Supports both new markdown format
and legacy JSON format for backward compatibility.

Author: Claude (Anthropic)
Created: 2025-10-18
"""

import frontmatter
from pathlib import Path
from typing import Dict, Any, Optional, List
import json
import re


class PlanMarkdownParserError(Exception):
    """Raised when markdown parsing operations fail."""
    pass


class PlanMarkdownParser:
    """Parse markdown implementation plans back into structured data."""

    def parse_file(self, md_path: Path) -> Dict[str, Any]:
        """
        Parse markdown file into plan dict.

        Tries markdown first, then falls back to JSON if markdown doesn't exist.
        This provides backward compatibility with legacy JSON-only plans.

        Args:
            md_path: Path to markdown plan file

        Returns:
            Plan dictionary with structure matching original save format

        Raises:
            FileNotFoundError: If neither markdown nor JSON file exists
            PlanMarkdownParserError: If parsing fails

        Example:
            >>> parser = PlanMarkdownParser()
            >>> plan = parser.parse_file(Path("docs/state/TASK-042/implementation_plan.md"))
            >>> print(plan['task_id'])
            TASK-042
        """
        # Try markdown first (primary format)
        if md_path.exists():
            return self._parse_markdown(md_path)

        # Fall back to JSON (legacy format)
        json_path = md_path.with_suffix('.json')
        if json_path.exists():
            return self._parse_json(json_path)

        # Neither exists
        raise FileNotFoundError(
            f"No plan found at {md_path} or {json_path}"
        )

    def _parse_markdown(self, md_path: Path) -> Dict[str, Any]:
        """
        Parse markdown file into structured dict.

        Args:
            md_path: Path to markdown file

        Returns:
            Plan dictionary

        Raises:
            PlanMarkdownParserError: If parsing fails
        """
        try:
            content = md_path.read_text(encoding='utf-8')

            # Parse frontmatter
            try:
                post = frontmatter.loads(content)
                metadata = dict(post.metadata)
                body = post.content
            except Exception:
                # No frontmatter, treat entire content as body
                metadata = {}
                body = content

            # Parse markdown sections into structured data
            plan_data = self._extract_sections(body)

            # Reconstruct plan structure matching original save format
            plan = {
                "task_id": metadata.get('task_id'),
                "saved_at": metadata.get('saved_at'),
                "version": metadata.get('version', 1),
                "status": metadata.get('status', 'draft'),
                "plan": plan_data
            }

            # Add architectural review if score present in metadata
            if 'architectural_review_score' in metadata:
                plan['architectural_review'] = {
                    'score': metadata.get('architectural_review_score')
                }

            # Preserve empty_plan marker if present
            if metadata.get('empty_plan'):
                plan['empty_plan'] = True

            return plan

        except Exception as e:
            raise PlanMarkdownParserError(
                f"Failed to parse markdown from {md_path}: {e}"
            ) from e

    def _parse_json(self, json_path: Path) -> Dict[str, Any]:
        """
        Parse JSON file (legacy format).

        Args:
            json_path: Path to JSON file

        Returns:
            Plan dictionary

        Raises:
            PlanMarkdownParserError: If parsing fails
        """
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise PlanMarkdownParserError(
                f"Failed to parse JSON from {json_path}: {e}"
            ) from e

    def _extract_sections(self, markdown_body: str) -> Dict[str, Any]:
        """
        Extract structured data from markdown sections.

        Parses markdown content to extract:
        - Files to create
        - Files to modify
        - Dependencies
        - Estimated effort
        - Risks
        - Implementation notes
        - Phases
        - Test summary

        Args:
            markdown_body: Markdown content (without frontmatter)

        Returns:
            Plan data dictionary
        """
        plan = {}

        # Extract summary (content before first ## heading after title)
        summary_match = re.search(
            r'## Summary\s*\n\s*(.*?)\s*(?=\n##|\Z)',
            markdown_body,
            re.DOTALL
        )
        if summary_match:
            plan['summary'] = summary_match.group(1).strip()

        # Extract files to create (always add key to distinguish from missing)
        files_to_create = self._extract_list_section(
            markdown_body,
            r'## Files to Create\s*\n(.*?)(?=\n##|\Z)'
        )
        plan['files_to_create'] = files_to_create

        # Extract files to modify (always add key to distinguish from missing)
        files_to_modify = self._extract_list_section(
            markdown_body,
            r'## Files to Modify\s*\n(.*?)(?=\n##|\Z)'
        )
        plan['files_to_modify'] = files_to_modify

        # Extract dependencies (always add key to distinguish from missing)
        dependencies = self._extract_list_section(
            markdown_body,
            r'## Dependencies\s*\n(.*?)(?=\n##|\Z)'
        )
        plan['external_dependencies'] = dependencies

        # Extract estimated effort
        effort_section = re.search(
            r'## Estimated Effort\s*\n(.*?)(?=\n##|\Z)',
            markdown_body,
            re.DOTALL
        )
        if effort_section:
            effort_text = effort_section.group(1)

            # Extract duration
            duration_match = re.search(r'\*\*Duration\*\*:\s*(.+?)(?:\n|$)', effort_text)
            if duration_match:
                plan['estimated_duration'] = duration_match.group(1).strip()

            # Extract lines of code
            loc_match = re.search(r'\*\*Lines of Code\*\*:\s*(\d+)', effort_text)
            if loc_match:
                plan['estimated_loc'] = int(loc_match.group(1))

            # Extract complexity score
            complexity_match = re.search(r'\*\*Complexity\*\*:\s*(\d+)/10', effort_text)
            if complexity_match:
                plan['complexity_score'] = int(complexity_match.group(1))

        # Extract risks (always add key to distinguish from missing)
        risks = self._extract_risks(markdown_body)
        plan['risks'] = risks

        # Extract implementation notes
        notes = self._extract_numbered_list(
            markdown_body,
            r'## Implementation Notes\s*\n(.*?)(?=\n##|\Z)'
        )
        if notes:
            plan['implementation_notes'] = notes

        # Extract phases
        phases = self._extract_numbered_list(
            markdown_body,
            r'## Implementation Phases\s*\n(.*?)(?=\n##|\Z)'
        )
        if phases:
            plan['phases'] = phases

        # Extract test summary
        test_match = re.search(
            r'## Test Summary\s*\n\s*(.*?)\s*(?=\n##|\n---|\Z)',
            markdown_body,
            re.DOTALL
        )
        if test_match:
            plan['test_summary'] = test_match.group(1).strip()

        return plan

    def _extract_list_section(self, content: str, pattern: str) -> List[str]:
        """
        Extract list items from a markdown section.

        Args:
            content: Markdown content
            pattern: Regex pattern to match section

        Returns:
            List of items (without bullet points)
        """
        match = re.search(pattern, content, re.DOTALL)
        if not match:
            return []

        section_text = match.group(1)
        items = []

        # Extract bullet list items
        for line in section_text.split('\n'):
            # Match list items: - `file.py` - description
            # or just: - `file.py`
            # or: - some text
            line = line.strip()
            if line.startswith('-') or line.startswith('*'):
                # Remove bullet
                item = line[1:].strip()

                # Skip "No files" or "Not specified" messages
                if item.startswith('*') or item.lower().startswith('no '):
                    continue

                # Extract code-quoted paths if present, but keep description after dash
                code_match = re.match(r'`([^`]+)`\s*-\s*(.+)', item)
                if code_match:
                    # Format: `name version` - purpose
                    # Return full string: "name version - purpose"
                    items.append(f"{code_match.group(1)} - {code_match.group(2)}")
                else:
                    # Try without description
                    code_match = re.match(r'`([^`]+)`', item)
                    if code_match:
                        items.append(code_match.group(1))
                    elif item:
                        items.append(item)

        return items

    def _extract_numbered_list(self, content: str, pattern: str) -> List[str]:
        """
        Extract numbered list items from a markdown section.

        Args:
            content: Markdown content
            pattern: Regex pattern to match section

        Returns:
            List of items (without numbers)
        """
        match = re.search(pattern, content, re.DOTALL)
        if not match:
            return []

        section_text = match.group(1)
        items = []

        # Extract numbered list items
        for line in section_text.split('\n'):
            line = line.strip()
            # Match: 1. Some text
            num_match = re.match(r'\d+\.\s*(.+)', line)
            if num_match:
                items.append(num_match.group(1).strip())

        return items

    def _extract_risks(self, content: str) -> List:
        """
        Extract risks and mitigation strategies.

        Args:
            content: Markdown content

        Returns:
            List of risk dictionaries or strings (mixed format supported)
        """
        risks = []

        # Find risks section
        match = re.search(
            r'## Risks & Mitigation\s*\n(.*?)(?=\n##|\Z)',
            content,
            re.DOTALL
        )
        if not match:
            return risks

        section_text = match.group(1)

        # Track which lines are part of structured risks
        processed_lines = set()

        # First pass: Extract structured risk blocks: - **Risk**: description
        #                                              - **Mitigation**: strategy
        #                                              - **Severity**: level
        risk_blocks = re.finditer(
            r'-\s*\*\*Risk\*\*:\s*(.+?)(?:\n|$)((?:\s+-\s+\*\*(?:Mitigation|Severity)\*\*:.+?(?:\n|$))*)',
            section_text,
            re.DOTALL
        )

        for block in risk_blocks:
            risk_desc = block.group(1).strip()
            metadata_text = block.group(2)

            mitigation = ''
            level = ''

            if metadata_text:
                mit_match = re.search(r'\*\*Mitigation\*\*:\s*(.+?)(?:\n|$)', metadata_text)
                if mit_match:
                    mitigation = mit_match.group(1).strip()

                sev_match = re.search(r'\*\*Severity\*\*:\s*(.+?)(?:\n|$)', metadata_text)
                if sev_match:
                    level = sev_match.group(1).strip()

            risk_dict = {
                'description': risk_desc,
                'mitigation': mitigation
            }
            if level:
                risk_dict['level'] = level

            risks.append(risk_dict)

            # Mark these lines as processed
            processed_lines.add(block.start())

        # Second pass: Extract simple list items (string risks)
        for line in section_text.split('\n'):
            line_stripped = line.strip()
            if line_stripped.startswith('-') and '**Risk**' not in line_stripped:
                # Simple list item, not a structured risk
                # Remove bullet point and asterisks
                item = line_stripped[1:].strip()
                if item and not item.startswith('*'):  # Skip "*No risks" type lines
                    risks.append(item)

        return risks


# Module exports
__all__ = [
    "PlanMarkdownParser",
    "PlanMarkdownParserError"
]
