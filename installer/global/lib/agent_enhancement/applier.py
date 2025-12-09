"""
Enhancement Applier

Applies enhancement content to agent files.

TASK-PHASE-8-INCREMENTAL: Shared module for agent enhancement
TASK-PD-001: Added progressive disclosure support with split file methods
TASK-PD-RK02: Adapted for RequireKit from GuardKit
"""

from pathlib import Path
from typing import Dict, Any, Tuple, Optional
import logging
import difflib
import re

# TASK-FIX-7C3D: Import file I/O utilities
import importlib
_file_io_module = importlib.import_module('installer.global.lib.utils.file_io')
safe_read_file = _file_io_module.safe_read_file
safe_write_file = _file_io_module.safe_write_file

# TASK-UX-6581: Import shared boundary utilities
# Handle both package import and direct import
# TASK-FIX-PD04: Added is_generic_boundaries for boundary replacement logic
try:
    from .boundary_utils import find_boundaries_insertion_point, is_generic_boundaries
except ImportError:
    from boundary_utils import find_boundaries_insertion_point, is_generic_boundaries

# TASK-PD-001: Import new data models
try:
    from .models import AgentEnhancement, SplitContent
except ImportError:
    from models import AgentEnhancement, SplitContent

logger = logging.getLogger(__name__)

# TASK-PD-001: Content categorization constants
CORE_SECTIONS = [
    'frontmatter',
    'title',
    'quick_start',
    'boundaries',
    'capabilities',
    'phase_integration',
    'loading_instruction',
]

EXTENDED_SECTIONS = [
    'detailed_examples',
    'examples',              # TASK-FIX-PD04: AI may use this instead of detailed_examples
    'best_practices',
    'anti_patterns',
    'cross_stack',
    'mcp_integration',
    'troubleshooting',
    'technology_specific',
    'related_templates',     # TASK-FIX-PD04: AI-generated template references
]


class EnhancementApplier:
    """Applies enhancement content to agent markdown files."""

    def apply(self, agent_file: Path, enhancement: Dict[str, Any]) -> None:
        """
        Modify agent file in-place with enhancement content.

        Inserts sections (related_templates, examples, best_practices) into
        the agent file while preserving frontmatter and existing content.

        Args:
            agent_file: Path to agent markdown file
            enhancement: Enhancement dict with sections and content

        Raises:
            PermissionError: If file is not writable
            ValueError: If enhancement data is invalid
        """
        if not agent_file.exists():
            raise FileNotFoundError(f"Agent file not found: {agent_file}")

        if not agent_file.is_file():
            raise ValueError(f"Path is not a file: {agent_file}")

        # Read current content with error handling (TASK-FIX-7C3D)
        success, original_content = safe_read_file(agent_file)
        if not success:
            # original_content contains error message
            raise PermissionError(f"Cannot read agent file: {original_content}")

        # TASK-ENH-DM01: Merge frontmatter metadata first (if present)
        if "frontmatter_metadata" in enhancement:
            self._merge_frontmatter_metadata(agent_file, enhancement["frontmatter_metadata"])
            # Re-read content after metadata merge
            success, original_content = safe_read_file(agent_file)
            if not success:
                raise PermissionError(f"Cannot re-read agent file: {original_content}")

        # Generate new content with enhancements
        new_content = self._merge_content(original_content, enhancement)

        # Write back to file with error handling (TASK-FIX-7C3D)
        success, error_msg = safe_write_file(agent_file, new_content)
        if not success:
            raise PermissionError(f"Cannot write to agent file: {error_msg}")

    def generate_diff(self, agent_file: Path, enhancement: Dict[str, Any]) -> str:
        """
        Create unified diff showing changes.

        Does NOT modify file.

        Args:
            agent_file: Path to agent markdown file
            enhancement: Enhancement dict with sections and content

        Returns:
            String in unified diff format (like `diff -u`)

        Example Output:
            ```
            --- agent-file.md
            +++ agent-file.md (enhanced)
            @@ -10,3 +10,15 @@
             Existing content...

            +## Related Templates
            +
            +- template1.template
            +- template2.template
            ```
        """
        if not agent_file.exists():
            return f"Error: File not found: {agent_file}"

        try:
            original_content = agent_file.read_text()
        except Exception as e:
            return f"Error reading file: {e}"

        # Generate new content
        new_content = self._merge_content(original_content, enhancement)

        # Generate unified diff
        original_lines = original_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)

        diff = difflib.unified_diff(
            original_lines,
            new_lines,
            fromfile=str(agent_file),
            tofile=f"{agent_file} (enhanced)",
            lineterm=''
        )

        return ''.join(diff)

    def _merge_content(self, original: str, enhancement: Dict[str, Any]) -> str:
        """
        Merge original content with enhancement sections.

        Strategy:
        1. Preserve frontmatter (YAML between ---...---)
        2. Preserve existing content
        3. Insert boundaries after "Quick Start", before next section (targets lines 80-150)
        4. Fallback to line 50-80 if no Quick Start found
        5. Append other sections at the end

        Args:
            original: Original file content
            enhancement: Enhancement dict with sections

        Returns:
            Merged content string
        """
        sections_to_add = enhancement.get("sections", [])

        # Split content into lines
        lines = original.split('\n')

        # Find end of frontmatter (if exists)
        frontmatter_end = 0
        in_frontmatter = False
        frontmatter_count = 0

        for i, line in enumerate(lines):
            if line.strip() == '---':
                frontmatter_count += 1
                if frontmatter_count == 1:
                    in_frontmatter = True
                elif frontmatter_count == 2:
                    in_frontmatter = False
                    frontmatter_end = i + 1
                    break

        # Build new content - preserve all original content
        new_lines = lines.copy()

        # Check if sections already exist (avoid duplicates)
        existing_content = '\n'.join(new_lines)

        # Separate boundaries from other sections for special placement
        boundaries_content = None
        other_sections = []

        for section_name in sections_to_add:
            if section_name == "boundaries":
                boundaries_content = enhancement.get("boundaries", "")
            else:
                other_sections.append(section_name)

        # Handle boundaries special placement (after Quick Start, before Capabilities)
        # TASK-FIX-PD04: Replace generic boundaries with AI-specific boundaries
        if boundaries_content and boundaries_content.strip():
            existing_has_boundaries = "## Boundaries" in existing_content

            # Decide whether to insert/replace boundaries
            should_insert = False
            if not existing_has_boundaries:
                # No existing boundaries - insert new ones
                should_insert = True
            elif not is_generic_boundaries(boundaries_content):
                # New boundaries are AI-specific, check if existing are generic
                existing_boundaries = self._extract_boundaries_section(existing_content)
                if existing_boundaries and is_generic_boundaries(existing_boundaries):
                    # Replace generic with AI-specific
                    logger.info("Replacing generic boundaries with AI-specific boundaries")
                    new_lines = self._remove_boundaries_section(new_lines)
                    should_insert = True

            if should_insert:
                # TASK-UX-6581: Use shared boundary utilities
                # find_boundaries_insertion_point now NEVER returns None
                insertion_point = find_boundaries_insertion_point(new_lines)
                # Insert at specific location
                if new_lines[insertion_point - 1].strip():
                    new_lines.insert(insertion_point, "")
                new_lines.insert(insertion_point, boundaries_content.strip())
                new_lines.insert(insertion_point, "")

        # Update existing_content for duplicate check
        existing_content = '\n'.join(new_lines)

        # Append other enhancement sections at the end
        for section_name in other_sections:
            section_content = enhancement.get(section_name, "")

            if section_content and section_content.strip():
                # Check if this section already exists
                section_header = f"## {section_name.replace('_', ' ').title()}"

                # TASK-FIX-AE01: Use fuzzy matching to prevent duplicate sections
                if not self._section_exists(existing_content, section_name):
                    # Add blank line before section if content exists
                    if new_lines and new_lines[-1].strip():
                        new_lines.append("")

                    # Add section content
                    new_lines.append(section_content.strip())

        return '\n'.join(new_lines)

    # TASK-UX-6581: Removed _find_boundaries_insertion_point() and _find_post_description_position()
    # These methods have been moved to boundary_utils.py for shared use between
    # /agent-enhance and /agent-format commands.

    def _normalize_section_name(self, section_name: str) -> str:
        """
        Normalize section name for comparison.

        Converts snake_case to lowercase with spaces for fuzzy matching.

        Args:
            section_name: Section name (e.g., "why_this_agent_exists")

        Returns:
            Normalized string (e.g., "why this agent exists")
        """
        return section_name.replace('_', ' ').strip().lower()

    def _section_exists(self, content: str, section_name: str) -> bool:
        """
        Check if section already exists in content (case-insensitive, fuzzy).

        TASK-FIX-AE01: Prevents duplicate sections by matching:
        - Case variations: "## Technologies" vs "## TECHNOLOGIES"
        - Underscore variations: "Why_This_Agent_Exists" vs "Why This Agent Exists"
        - Partial matches: "## Technologies Used" contains "Technologies"

        Args:
            content: Full file content to search
            section_name: Section name from enhancement (e.g., "technologies")

        Returns:
            True if similar section header found, False otherwise
        """
        normalized = self._normalize_section_name(section_name)

        for line in content.split('\n'):
            stripped = line.strip()
            # Match only H2 headers ("## Section" or "##Section"), NOT H3+ ("### Section")
            if stripped.startswith('##') and not stripped.startswith('###'):
                # Extract header text (skip "##" and any leading spaces)
                header_text = stripped[2:].lstrip()
                existing = self._normalize_section_name(header_text)

                # Fuzzy match: normalized is substring of existing or vice versa
                if normalized in existing or existing in normalized:
                    logger.debug(f"Section '{section_name}' matches existing header: '{stripped}'")
                    return True

        return False

    # ========================================================================
    # TASK-FIX-PD04: Boundary Section Helper Methods
    # ========================================================================

    def _extract_boundaries_section(self, content: str) -> Optional[str]:
        """
        Extract the boundaries section from content.

        TASK-FIX-PD04: Used to detect if existing boundaries are generic.

        Args:
            content: Full file content

        Returns:
            Boundaries section content (from "## Boundaries" to next "##"), or None
        """
        lines = content.split('\n')
        in_boundaries = False
        boundaries_lines = []

        for line in lines:
            if line.strip().startswith('## Boundaries'):
                in_boundaries = True
                boundaries_lines.append(line)
            elif in_boundaries:
                # Check if we've hit the next section
                if line.strip().startswith('## ') and not line.strip().startswith('### '):
                    break
                boundaries_lines.append(line)

        if boundaries_lines:
            return '\n'.join(boundaries_lines)
        return None

    def _remove_boundaries_section(self, lines: list) -> list:
        """
        Remove the boundaries section from lines.

        TASK-FIX-PD04: Used to remove generic boundaries before inserting AI-specific.

        Args:
            lines: List of lines from content

        Returns:
            List of lines with boundaries section removed
        """
        new_lines = []
        in_boundaries = False

        for line in lines:
            if line.strip().startswith('## Boundaries'):
                in_boundaries = True
                continue
            elif in_boundaries:
                # Check if we've hit the next section
                if line.strip().startswith('## ') and not line.strip().startswith('### '):
                    in_boundaries = False
                    new_lines.append(line)
                # Skip lines while in boundaries section
                continue
            else:
                new_lines.append(line)

        return new_lines

    # ========================================================================
    # TASK-ENH-DM01: Frontmatter Metadata Merge Methods
    # ========================================================================

    def _merge_frontmatter_metadata_content(
        self,
        content: str,
        metadata: Dict[str, Any]
    ) -> str:
        """
        Merge discovery metadata into frontmatter content (pure function).

        TASK-ENH-DM01: Adds stack/phase/capabilities/keywords without
        overwriting existing fields.

        Args:
            content: Original file content with frontmatter
            metadata: Dict with stack, phase, capabilities, keywords

        Returns:
            Updated content with merged frontmatter
        """
        import frontmatter

        # Parse existing frontmatter
        post = frontmatter.loads(content)

        # Discovery metadata fields to merge
        discovery_fields = ["stack", "phase", "capabilities", "keywords"]

        fields_added = []
        fields_preserved = []

        for field in discovery_fields:
            if field in metadata:
                if field not in post.metadata:
                    # Field doesn't exist - add it
                    post.metadata[field] = metadata[field]
                    fields_added.append(field)
                else:
                    # Field exists - preserve original
                    fields_preserved.append(field)

        if fields_added:
            logger.info(f"Added discovery metadata: {', '.join(fields_added)}")
        if fields_preserved:
            logger.debug(f"Preserved existing metadata: {', '.join(fields_preserved)}")

        return frontmatter.dumps(post)

    def _merge_frontmatter_metadata(
        self,
        agent_file: Path,
        metadata: Dict[str, Any]
    ) -> None:
        """
        Merge discovery metadata into agent YAML frontmatter.

        TASK-ENH-DM01: I/O wrapper for frontmatter metadata merging.

        Args:
            agent_file: Path to agent markdown file
            metadata: Dict with stack, phase, capabilities, keywords

        Raises:
            PermissionError: If file cannot be read/written
            ValueError: If file exceeds size limit (security)
        """
        # Read existing content
        success, content = safe_read_file(agent_file)
        if not success:
            raise PermissionError(f"Cannot read agent file: {content}")

        # Security: Guard against YAML bombs (per architectural review)
        if len(content) > 100_000:  # 100KB limit for agent files
            raise ValueError(f"Agent file too large: {len(content)} bytes (max 100KB)")

        # Merge metadata using pure function
        updated_content = self._merge_frontmatter_metadata_content(content, metadata)

        # Write back
        success, error_msg = safe_write_file(agent_file, updated_content)
        if not success:
            raise PermissionError(f"Cannot write agent file: {error_msg}")

    # ========================================================================
    # TASK-PD-001: Progressive Disclosure Methods (Split File Architecture)
    # ========================================================================

    def create_extended_file(self, agent_path: Path, extended_content: str) -> Path:
        """
        Create extended content file ({name}-ext.md).

        Used by apply_with_split() to create companion files for detailed
        agent documentation while keeping core files concise.

        Args:
            agent_path: Path to core agent file (e.g., fastapi-specialist.md)
            extended_content: Complete markdown content for extended file

        Returns:
            Path to created extended file (e.g., fastapi-specialist-ext.md)

        Raises:
            PermissionError: If file cannot be written
            ValueError: If agent_path is invalid

        Example:
            >>> applier = EnhancementApplier()
            >>> core_path = Path("fastapi-specialist.md")
            >>> ext_content = "## Detailed Examples\\n\\nExample 1..."
            >>> ext_path = applier.create_extended_file(core_path, ext_content)
            >>> print(ext_path)
            fastapi-specialist-ext.md
        """
        if not agent_path.name.endswith('.md'):
            raise ValueError(f"Agent path must be markdown file: {agent_path}")

        # Generate extended file path: agent-name.md → agent-name-ext.md
        stem = agent_path.stem  # "fastapi-specialist"
        ext_path = agent_path.with_stem(f"{stem}-ext")

        # Write extended content with error handling
        success, error_msg = safe_write_file(ext_path, extended_content)
        if not success:
            raise PermissionError(f"Cannot write extended file: {error_msg}")

        logger.info(f"Created extended file: {ext_path.name}")
        return ext_path

    def apply_with_split(
        self,
        agent_path: Path,
        enhancement: AgentEnhancement
    ) -> SplitContent:
        """
        Apply enhancement with progressive disclosure (split files).

        Creates two files:
        1. Core file (agent-name.md): Essential content (150-300 lines)
        2. Extended file (agent-name-ext.md): Detailed content (500-800 lines)

        Core file includes link to extended file for deeper learning.

        Args:
            agent_path: Path to agent file to enhance
            enhancement: Enhancement content (categorized into core/extended)

        Returns:
            SplitContent with paths and section distribution

        Raises:
            FileNotFoundError: If agent_path doesn't exist
            PermissionError: If files cannot be written
            ValueError: If enhancement is invalid

        Example:
            >>> applier = EnhancementApplier()
            >>> enhancement: AgentEnhancement = {
            ...     "sections": ["quick_start", "boundaries", "detailed_examples"],
            ...     "quick_start": "## Quick Start\\n\\nExample...",
            ...     "boundaries": "## Boundaries\\n\\n### ALWAYS...",
            ...     "detailed_examples": "## Detailed Examples\\n\\n..."
            ... }
            >>> split = applier.apply_with_split(Path("agent.md"), enhancement)
            >>> print(f"Core: {split.core_path}, Extended: {split.extended_path}")
            Core: agent.md, Extended: agent-ext.md
        """
        if not agent_path.exists():
            raise FileNotFoundError(f"Agent file not found: {agent_path}")

        # Step 1: Categorize sections into core and extended
        core_sections, extended_sections = self._categorize_sections(enhancement)

        # Step 2: Read original content for merging
        success, original_content = safe_read_file(agent_path)
        if not success:
            raise PermissionError(f"Cannot read agent file: {original_content}")

        # TASK-ENH-DM01: Merge frontmatter metadata before building content
        if "frontmatter_metadata" in enhancement:
            self._merge_frontmatter_metadata(agent_path, enhancement["frontmatter_metadata"])
            # Re-read content after metadata merge
            success, original_content = safe_read_file(agent_path)
            if not success:
                raise PermissionError(f"Cannot re-read agent file: {original_content}")

        # Step 3: Build and write core content (preserves original + adds core sections)
        has_extended = bool(extended_sections)
        core_content = self._build_core_content(
            agent_path.stem,
            original_content,
            core_sections,
            has_extended
        )

        success, error_msg = safe_write_file(agent_path, core_content)
        if not success:
            raise PermissionError(f"Cannot write core file: {error_msg}")

        # Step 4: Build and write extended content (if any)
        extended_path = None
        if extended_sections:
            extended_content = self._build_extended_content(
                agent_path.stem,
                extended_sections
            )
            extended_path = self.create_extended_file(agent_path, extended_content)

        logger.info(
            f"Split content: {len(core_sections)} core sections, "
            f"{len(extended_sections)} extended sections"
        )

        return SplitContent(
            core_path=agent_path,
            extended_path=extended_path,
            core_sections=list(core_sections.keys()),
            extended_sections=list(extended_sections.keys())
        )

    def _categorize_sections(
        self,
        enhancement: AgentEnhancement
    ) -> Tuple[Dict[str, str], Dict[str, str]]:
        """
        Split enhancement sections into core and extended categories.

        Core sections (essential, shown in main file):
        - frontmatter, title, quick_start (2-3 examples), boundaries,
          capabilities, phase_integration

        Extended sections (detailed, shown in -ext.md file):
        - detailed_examples, best_practices, anti_patterns, cross_stack,
          mcp_integration, troubleshooting, technology_specific

        Args:
            enhancement: Enhancement data with all sections

        Returns:
            Tuple of (core_dict, extended_dict) with section content

        Example:
            >>> enhancement = {
            ...     "sections": ["quick_start", "boundaries", "detailed_examples"],
            ...     "quick_start": "## Quick Start\\n...",
            ...     "boundaries": "## Boundaries\\n...",
            ...     "detailed_examples": "## Detailed Examples\\n..."
            ... }
            >>> core, extended = applier._categorize_sections(enhancement)
            >>> print(core.keys())
            dict_keys(['quick_start', 'boundaries'])
            >>> print(extended.keys())
            dict_keys(['detailed_examples'])
        """
        core: Dict[str, str] = {}
        extended: Dict[str, str] = {}

        # Iterate through all sections in enhancement
        for section_name in enhancement.get("sections", []):
            content = enhancement.get(section_name, "")

            if not content or not content.strip():
                continue  # Skip empty sections

            if section_name in CORE_SECTIONS:
                core[section_name] = content
            elif section_name in EXTENDED_SECTIONS:
                extended[section_name] = content
            else:
                # Unknown section - log warning and add to extended (safe default)
                logger.warning(
                    f"Unknown section '{section_name}' categorized as extended"
                )
                extended[section_name] = content

        # Special handling: Limit Quick Start to first 3 examples
        if 'quick_start' in core:
            core['quick_start'] = self._truncate_quick_start(
                core['quick_start'],
                max_examples=3
            )

        logger.debug(
            f"Categorized {len(core)} core sections, {len(extended)} extended sections"
        )

        return core, extended

    def _truncate_quick_start(self, quick_start_content: str, max_examples: int = 3) -> str:
        """
        Limit Quick Start section to first N examples.

        Preserves section header and first N code blocks/examples.
        Adds note about extended file if examples were truncated.

        Args:
            quick_start_content: Original Quick Start section content
            max_examples: Maximum number of examples to keep (default: 3)

        Returns:
            Truncated Quick Start content

        Example:
            >>> content = '''## Quick Start
            ... Example 1
            ... ```python
            ... code1
            ... ```
            ... Example 2
            ... ```python
            ... code2
            ... ```
            ... Example 3
            ... ```python
            ... code3
            ... ```
            ... Example 4
            ... ```python
            ... code4
            ... ```
            ... '''
            >>> truncated = applier._truncate_quick_start(content, max_examples=2)
            >>> assert "Example 1" in truncated
            >>> assert "Example 2" in truncated
            >>> assert "Example 3" not in truncated
        """
        lines = quick_start_content.split('\n')

        # Find code block boundaries (``` markers)
        code_blocks = []
        in_code_block = False
        block_start = None

        for i, line in enumerate(lines):
            if line.strip().startswith('```'):
                if not in_code_block:
                    # Start of code block
                    in_code_block = True
                    block_start = i
                else:
                    # End of code block
                    in_code_block = False
                    if block_start is not None:
                        code_blocks.append((block_start, i))
                        block_start = None

        # If we have more examples than max, truncate
        if len(code_blocks) <= max_examples:
            return quick_start_content  # No truncation needed

        # Find the end of the last example we want to keep
        # (include some context lines after the code block)
        last_block_end = code_blocks[max_examples - 1][1]
        truncate_line = last_block_end + 2  # Include 1-2 lines after code block

        # Build truncated content
        truncated_lines = lines[:truncate_line]
        truncated_lines.append("")
        truncated_lines.append(
            "*See the extended file for additional examples and detailed usage.*"
        )

        logger.debug(
            f"Truncated Quick Start from {len(code_blocks)} to {max_examples} examples"
        )

        return '\n'.join(truncated_lines)

    def _build_core_content(
        self,
        agent_name: str,
        original_content: str,
        core_sections: Dict[str, str],
        has_extended: bool
    ) -> str:
        """
        Build core file content by merging original with core sections.

        Strategy:
        1. Preserve original frontmatter and structure
        2. Merge core sections using existing _merge_content logic
        3. Add loading instruction link to extended file (if exists)

        Args:
            agent_name: Name of agent (from file stem, e.g., "fastapi-specialist")
            original_content: Original agent file content
            core_sections: Dict of core section names to content
            has_extended: Whether extended file will be created

        Returns:
            Complete core file content

        Example:
            >>> core_sections = {
            ...     "quick_start": "## Quick Start\\n...",
            ...     "boundaries": "## Boundaries\\n..."
            ... }
            >>> content = applier._build_core_content(
            ...     agent_name="test-agent",
            ...     original_content="---\\nname: Agent\\n---\\n# Agent",
            ...     core_sections=core_sections,
            ...     has_extended=True
            ... )
            >>> assert "## Quick Start" in content
            >>> assert "## Extended Documentation" in content
        """
        # Convert core sections dict to enhancement format for _merge_content
        enhancement = {
            "sections": list(core_sections.keys()),
            **core_sections
        }

        # Use existing merge logic to preserve structure
        merged_content = self._merge_content(original_content, enhancement)

        # TASK-FIX-PD04: Add loading instruction if extended file exists
        # Only add if not already present (prevents duplicates)
        if has_extended and "## Extended Documentation" not in merged_content:
            loading_instruction = self._format_loading_instruction(agent_name)
            merged_content = self._append_section(merged_content, loading_instruction)

        return merged_content

    def _build_extended_content(
        self,
        agent_name: str,
        extended_sections: Dict[str, str]
    ) -> str:
        """
        Build extended file content from extended sections.

        Structure:
        1. Header linking back to core file
        2. Extended sections in order
        3. Footer with contribution guidelines

        Args:
            agent_name: Name of agent (from core file stem)
            extended_sections: Dict of extended section names to content

        Returns:
            Complete extended file content

        Example:
            >>> extended_sections = {
            ...     "detailed_examples": "## Detailed Examples\\n...",
            ...     "best_practices": "## Best Practices\\n..."
            ... }
            >>> content = applier._build_extended_content(
            ...     "fastapi-specialist",
            ...     extended_sections
            ... )
            >>> assert "fastapi-specialist.md" in content
            >>> assert "## Detailed Examples" in content
        """
        lines = []

        # Header
        lines.append(f"# {agent_name.replace('-', ' ').title()} - Extended Documentation")
        lines.append("")
        lines.append(
            f"This file contains detailed examples, best practices, and in-depth "
            f"guidance for the **{agent_name}** agent."
        )
        lines.append("")
        lines.append(f"**Core documentation**: See [{agent_name}.md](./{agent_name}.md)")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Extended sections in consistent order
        # TASK-FIX-PD04: Added 'related_templates' and 'examples' to match AI response formats
        section_order = [
            'related_templates',     # Templates first for context
            'detailed_examples',
            'examples',              # AI alternate name for detailed_examples
            'best_practices',
            'anti_patterns',
            'cross_stack',
            'mcp_integration',
            'troubleshooting',
            'technology_specific',
        ]

        for section_name in section_order:
            if section_name in extended_sections:
                content = extended_sections[section_name]
                if content and content.strip():
                    lines.append(content.strip())
                    lines.append("")  # Blank line between sections

        # Footer - TASK-PD-RK02: Updated for RequireKit
        lines.append("---")
        lines.append("")
        lines.append("*This extended documentation is part of RequireKit's progressive disclosure system.*")
        lines.append("")

        return '\n'.join(lines)

    def _format_loading_instruction(self, agent_name: str) -> str:
        """
        Generate loading instruction section linking to extended file.

        TASK-PD-RK02: Updated for RequireKit with appropriate agent paths.

        Args:
            agent_name: Name of agent (from file stem, e.g., "bdd-generator")

        Returns:
            Markdown section with link to extended documentation

        Example:
            >>> instruction = applier._format_loading_instruction("bdd-generator")
            >>> assert "## Extended Documentation" in instruction
            >>> assert "bdd-generator-ext.md" in instruction
        """
        return f"""## Extended Documentation

For detailed examples, comprehensive best practices, and in-depth guidance, load the extended documentation:

```bash
cat agents/{agent_name}-ext.md
```

The extended file contains:
- Detailed code examples with explanations
- Framework-specific step definitions
- Common anti-patterns and how to avoid them
- Cross-stack considerations
- Troubleshooting guides

*Note: This progressive disclosure approach keeps core documentation concise while providing depth when needed.*"""

    def _append_section(self, content: str, section: str) -> str:
        """
        Append section to end of content with proper spacing.

        Args:
            content: Existing content
            section: Section to append

        Returns:
            Content with appended section
        """
        lines = content.split('\n')

        # Add blank line if content doesn't end with one
        if lines and lines[-1].strip():
            lines.append("")

        lines.append(section.strip())
        return '\n'.join(lines)

    def _format_section_title(self, section_name: str) -> str:
        """
        Convert snake_case section name to Title Case header.

        Args:
            section_name: Section name in snake_case (e.g., "best_practices")

        Returns:
            Title Case header (e.g., "Best Practices")

        Example:
            >>> applier._format_section_title("best_practices")
            'Best Practices'
            >>> applier._format_section_title("mcp_integration")
            'Mcp Integration'
        """
        return section_name.replace('_', ' ').title()

    # ========================================================================
    # End of TASK-PD-001 Methods
    # ========================================================================

    def remove_sections(
        self,
        agent_file: Path,
        section_names: list[str]
    ) -> None:
        """
        Remove specific sections from agent file (utility method).

        Args:
            agent_file: Path to agent markdown file
            section_names: List of section names to remove (e.g., ["related_templates"])

        Raises:
            PermissionError: If file is not writable
        """
        if not agent_file.exists():
            raise FileNotFoundError(f"Agent file not found: {agent_file}")

        content = agent_file.read_text()
        lines = content.split('\n')
        new_lines = []

        in_section_to_remove = False
        current_section = None

        for line in lines:
            # Check if this is a section header
            if line.startswith('## '):
                section_name = line[3:].strip().lower().replace(' ', '_')

                if section_name in section_names:
                    in_section_to_remove = True
                    current_section = section_name
                    continue
                else:
                    in_section_to_remove = False
                    current_section = None

            # Skip lines in sections to remove
            if not in_section_to_remove:
                new_lines.append(line)

        agent_file.write_text('\n'.join(new_lines))
