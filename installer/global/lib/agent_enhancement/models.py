"""
Agent Enhancement Data Models

Type-safe data structures for agent enhancement and progressive disclosure.

TASK-PD-001: Created for split file architecture support
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict, List, Optional


class AgentEnhancement(TypedDict, total=False):
    """
    Type-safe enhancement data structure.

    Used to pass enhancement content between parser, applier, and orchestrator.
    All fields are optional to support partial enhancements.

    Attributes:
        sections: List of section names included in enhancement
        frontmatter: YAML metadata (priority, stack, phase, etc.)
        title: Agent name and purpose
        quick_start: 2-3 usage examples (core content)
        boundaries: ALWAYS/NEVER/ASK framework (required)
        capabilities: Bullet list of agent capabilities
        phase_integration: When agent is used in workflow
        detailed_examples: 5-10 comprehensive examples (extended)
        best_practices: Detailed best practice recommendations (extended)
        anti_patterns: Common mistakes to avoid (extended)
        cross_stack: Multi-language examples (extended)
        mcp_integration: Optional MCP server integration (extended)
        troubleshooting: Debug guides and solutions (extended)
        technology_specific: Per-technology guidance (extended)
        loading_instruction: Reference to extended file (generated)
    """
    sections: List[str]
    frontmatter: str
    title: str
    quick_start: str
    boundaries: str
    capabilities: str
    phase_integration: str
    detailed_examples: str
    best_practices: str
    anti_patterns: str
    cross_stack: str
    mcp_integration: str
    troubleshooting: str
    technology_specific: str
    loading_instruction: str


@dataclass
class SplitContent:
    """
    Represents content split between core and extended agent files.

    Used by apply_with_split() to return information about created files
    and section distribution for progressive disclosure.

    Attributes:
        core_path: Path to core agent file (e.g., agent-name.md)
        extended_path: Path to extended file (e.g., agent-name-ext.md) or None
        core_sections: List of section names in core file
        extended_sections: List of section names in extended file

    Example:
        >>> split = SplitContent(
        ...     core_path=Path("fastapi-specialist.md"),
        ...     extended_path=Path("fastapi-specialist-ext.md"),
        ...     core_sections=["frontmatter", "title", "quick_start", "boundaries"],
        ...     extended_sections=["detailed_examples", "best_practices"]
        ... )
    """
    core_path: Path
    extended_path: Optional[Path]
    core_sections: List[str]
    extended_sections: List[str]


@dataclass
class EnhancementResult:
    """
    Result of agent enhancement operation.

    TASK-PD-003: Enhanced to support split-file output mode.
    TASK-FIX-PD03: Added enhancement_data for passing structured content.

    This dataclass represents the outcome of enhancing an agent file,
    including both success/error state and information about created files.

    Attributes:
        success: Whether enhancement succeeded
        agent_name: Name of enhanced agent
        sections: List of section names added/modified
        templates: List of template files referenced
        examples: List of code examples included
        diff: Unified diff showing changes
        error: Error message if failed (None if successful)
        strategy_used: Enhancement strategy (ai/static/hybrid)
        core_file: Path to core agent file (None on error)
        extended_file: Path to extended file or None (split mode only)
        split_output: Whether split-file mode was used
        enhancement_data: Raw enhancement dict from AI/static strategy (for debugging/passthrough)

    Example (split mode):
        >>> result = EnhancementResult(
        ...     success=True,
        ...     agent_name="fastapi-specialist",
        ...     core_file=Path("fastapi-specialist.md"),
        ...     extended_file=Path("fastapi-specialist-ext.md"),
        ...     split_output=True,
        ...     ...
        ... )
        >>> result.files
        [Path('fastapi-specialist.md'), Path('fastapi-specialist-ext.md')]

    Example (single-file mode):
        >>> result = EnhancementResult(
        ...     success=True,
        ...     agent_name="fastapi-specialist",
        ...     core_file=Path("fastapi-specialist.md"),
        ...     extended_file=None,
        ...     split_output=False,
        ...     ...
        ... )
        >>> result.files
        [Path('fastapi-specialist.md')]
    """
    success: bool
    agent_name: str
    sections: List[str]
    templates: List[str]
    examples: List[str]
    diff: str
    error: Optional[str] = None
    strategy_used: Optional[str] = None
    core_file: Optional[Path] = None
    extended_file: Optional[Path] = None
    split_output: bool = False
    enhancement_data: Optional[dict] = None  # TASK-FIX-PD03: Raw enhancement dict

    @property
    def files(self) -> List[Path]:
        """
        Return all created/modified files as a list.

        Returns:
            List of Path objects for files affected by enhancement.
            Empty list if core_file is None (error case).

        Example:
            >>> result.files
            [Path('core.md'), Path('ext.md')]  # Split mode
            >>> result.files
            [Path('core.md')]  # Single-file mode
            >>> result.files
            []  # Error case
        """
        if self.core_file is None:
            return []

        if self.extended_file is not None:
            return [self.core_file, self.extended_file]

        return [self.core_file]
