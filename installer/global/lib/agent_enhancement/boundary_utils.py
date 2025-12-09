"""
Shared Boundary Section Utilities

Used by both /agent-enhance (AI content) and /agent-format (generic content).
Provides consistent placement and validation across commands.

EXTRACTED FROM:
- applier.py lines 203-329 (placement logic) - TASK-STND-0B1A
- parser.py lines 153-258 (validation logic) - TASK-STND-8B4C

CREATED BY: TASK-UX-6581 (2025-11-23)
"""

from typing import Optional
import re


# Exports
__all__ = [
    'find_boundaries_insertion_point',
    'validate_boundaries_format',
    'generate_generic_boundaries',
    'is_generic_boundaries',  # TASK-FIX-PD04: Added to detect generic vs AI boundaries
]


def find_boundaries_insertion_point(lines: list[str]) -> int:
    """
    Find optimal insertion point for boundaries section.

    EXTRACTED FROM: applier.py lines 199-240 (TASK-STND-0B1A)

    Target: Lines 80-150 (GitHub recommendation for authority clarity).
    NEVER returns None - always finds suitable insertion point.

    Strategy:
    1. Find "## Quick Start" section
    2. Find next ## section after Quick Start
    3. Insert boundaries before that next section
    4. Fallback: Use 5-tier fallback strategy if no Quick Start found

    Args:
        lines: List of content lines

    Returns:
        int: Line index for insertion (NEVER None)
    """
    # Step 1: Find Quick Start
    quick_start_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("## Quick Start"):
            quick_start_idx = i
            break

    if quick_start_idx is None:
        # Fallback: No Quick Start, use 5-tier fallback strategy
        return _find_post_description_position(lines)

    # Step 2: Find next ## section after Quick Start
    for i in range(quick_start_idx + 1, len(lines)):
        if lines[i].strip().startswith("## "):
            return i  # Insert before this section

    # Step 3: No next section, insert at reasonable position
    # Target: ~30 lines after Quick Start (hits 80-150 range)
    target_line = quick_start_idx + 30
    return min(target_line, len(lines))


def _find_post_description_position(lines: list[str]) -> int:
    """
    Fallback: Find position after description/purpose section.

    EXTRACTED FROM: applier.py lines 242-329 (TASK-STND-0B1A)

    Used when "## Quick Start" doesn't exist.
    Implements 5-tier bulletproof fallback strategy that NEVER returns None.

    Priority Order:
    1. Before first "content" section (Code Examples, Best Practices, etc.)
    2. After last "early" section (Purpose, Technologies, etc.)
    3. Before "## Code Examples" (catches 92% of failures)
    4. Before "## Related Templates" (safety net)
    5. Frontmatter + 50 lines (absolute last resort)

    GitHub recommendation: lines 80-150, before Code Examples.

    Args:
        lines: List of content lines

    Returns:
        int: Line index for insertion (NEVER None)
    """
    # Find end of frontmatter
    frontmatter_end = 0
    frontmatter_count = 0

    for i, line in enumerate(lines):
        if line.strip() == '---':
            frontmatter_count += 1
            if frontmatter_count == 2:
                frontmatter_end = i + 1
                break

    # Find sections after frontmatter to determine best insertion point
    # We want to insert EARLY, after initial metadata sections but before content
    early_sections = ["Purpose", "Why This Agent Exists", "Technologies", "Usage", "When to Use"]
    content_sections = ["Code Examples", "Examples", "Related Templates", "Best Practices", "Capabilities"]

    sections_found = []
    for i in range(frontmatter_end, min(frontmatter_end + 100, len(lines))):
        if lines[i].strip().startswith("## "):
            section_name = lines[i].strip()[3:].strip()
            sections_found.append((i, section_name))

    # Strategy: Insert before the first "content" section OR after the last "early" section
    last_early_section_idx = None
    first_content_section_idx = None

    for idx, name in sections_found:
        # Check if this is an early section (metadata)
        if any(early in name for early in early_sections):
            last_early_section_idx = idx
        # Check if this is a content section
        elif any(content in name for content in content_sections):
            if first_content_section_idx is None:
                first_content_section_idx = idx
            break  # Stop at first content section

    # Priority 1: If we found a content section, insert before it
    if first_content_section_idx is not None:
        return first_content_section_idx

    # Priority 2: If we found early sections but no content sections, insert after last early section
    if last_early_section_idx is not None:
        # Find next section after last early section
        for idx, name in sections_found:
            if idx > last_early_section_idx:
                return idx

    # Priority 3: Before "## Code Examples" (fixes 92% of failures)
    for i, line in enumerate(lines):
        if line.strip().startswith("## Code Examples"):
            return i

    # Priority 4: Before "## Related Templates" (safety net)
    for i, line in enumerate(lines):
        if line.strip().startswith("## Related Templates"):
            return i

    # Priority 5: Frontmatter + 50 lines (absolute last resort)
    insertion_point = min(frontmatter_end + 50, len(lines))

    # Find next section boundary at or after insertion_point
    for i in range(insertion_point, len(lines)):
        if lines[i].strip().startswith("## "):
            return i

    return insertion_point  # Never None


def validate_boundaries_format(boundaries_content: str) -> tuple[bool, list[str]]:
    """
    Validate boundaries section structure and rule counts.

    EXTRACTED FROM: parser.py lines 153-258 (TASK-STND-8B4C)

    Ensures ALWAYS/NEVER/ASK framework compliance:
    - ALWAYS: 5-7 rules with ✅ prefix
    - NEVER: 5-7 rules with ❌ prefix
    - ASK: 3-5 scenarios with ⚠️ prefix

    Args:
        boundaries_content: Markdown content of boundaries section

    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []

    if not boundaries_content or not boundaries_content.strip():
        issues.append("Boundaries section is empty")
        return False, issues

    # Check for required subsections
    if "### ALWAYS" not in boundaries_content:
        issues.append("Boundaries section missing '### ALWAYS' subsection")
    if "### NEVER" not in boundaries_content:
        issues.append("Boundaries section missing '### NEVER' subsection")
    if "### ASK" not in boundaries_content:
        issues.append("Boundaries section missing '### ASK' subsection")

    if issues:
        return False, issues

    # Extract sections
    always_section = _extract_subsection(boundaries_content, "### ALWAYS", "### NEVER")
    never_section = _extract_subsection(boundaries_content, "### NEVER", "### ASK")
    ask_section = _extract_subsection(boundaries_content, "### ASK", None)

    # Count rules
    always_count = _count_rules(always_section, "✅")
    never_count = _count_rules(never_section, "❌")
    ask_count = _count_rules(ask_section, "⚠️")

    # Validate counts
    if not (5 <= always_count <= 7):
        issues.append(
            f"ALWAYS section must have 5-7 rules, found {always_count}. "
            f"Each rule should start with '- ✅'"
        )

    if not (5 <= never_count <= 7):
        issues.append(
            f"NEVER section must have 5-7 rules, found {never_count}. "
            f"Each rule should start with '- ❌'"
        )

    if not (3 <= ask_count <= 5):
        issues.append(
            f"ASK section must have 3-5 scenarios, found {ask_count}. "
            f"Each scenario should start with '- ⚠️'"
        )

    is_valid = len(issues) == 0
    return is_valid, issues


def _extract_subsection(content: str, start_marker: str, end_marker: Optional[str]) -> str:
    """
    Extract content between two section markers.

    EXTRACTED FROM: parser.py lines 213-239 (TASK-STND-8B4C)

    Args:
        content: Full markdown content
        start_marker: Start section header (e.g., "### ALWAYS")
        end_marker: End section header or None for end of content

    Returns:
        Extracted subsection content
    """
    start_idx = content.find(start_marker)
    if start_idx == -1:
        return ""

    # Start after the marker line
    start_idx = content.find('\n', start_idx) + 1

    if end_marker is None:
        return content[start_idx:]

    end_idx = content.find(end_marker, start_idx)
    if end_idx == -1:
        return content[start_idx:]

    return content[start_idx:end_idx]


def _count_rules(section_content: str, emoji: str) -> int:
    """
    Count rules in a section by counting lines with specific emoji prefix.

    EXTRACTED FROM: parser.py lines 241-258 (TASK-STND-8B4C)

    Args:
        section_content: Section markdown content
        emoji: Expected emoji prefix (✅, ❌, or ⚠️)

    Returns:
        Number of rules found
    """
    count = 0
    for line in section_content.split('\n'):
        stripped = line.strip()
        # Match: "- [emoji] ..." or "-[emoji] ..."
        if stripped.startswith(f"- {emoji}") or stripped.startswith(f"-{emoji}"):
            count += 1
    return count


def generate_generic_boundaries(agent_name: str, agent_description: str) -> str:
    """
    Generate generic boundary content for pattern-based formatting.

    NOT AI-powered - uses templates that work for ANY agent.
    For domain-specific content, use /agent-enhance instead.

    NEW FUNCTIONALITY: Created for TASK-UX-6581 to enable /agent-format
    to generate compliant boundaries instead of placeholders.

    Args:
        agent_name: Name of agent (e.g., "architectural-reviewer")
        agent_description: Agent description from frontmatter

    Returns:
        Markdown content with ALWAYS/NEVER/ASK sections (passes validation)
    """
    # Infer agent role category
    role_category = _infer_role_category(agent_name, agent_description)

    # Select template based on category
    templates = {
        "testing": _testing_boundaries_template(),
        "architecture": _architecture_boundaries_template(),
        "code_review": _code_review_boundaries_template(),
        "orchestration": _orchestration_boundaries_template(),
        "default": _default_boundaries_template()
    }

    return templates.get(role_category, templates["default"])


def _infer_role_category(agent_name: str, agent_description: str) -> str:
    """
    Infer agent role category from name/description.

    Uses keyword matching to determine appropriate boundary template.

    Args:
        agent_name: Agent name
        agent_description: Agent description

    Returns:
        Role category (testing, architecture, code_review, orchestration, default)
    """
    combined = (agent_name + " " + agent_description).lower()

    if any(kw in combined for kw in ["test", "coverage", "verification", "pytest", "vitest"]):
        return "testing"
    elif any(kw in combined for kw in ["architect", "design", "solid", "pattern", "structure"]):
        return "architecture"
    elif any(kw in combined for kw in ["review", "quality", "lint", "format", "style"]):
        return "code_review"
    elif any(kw in combined for kw in ["orchestrat", "workflow", "phase", "task", "manage"]):
        return "orchestration"
    else:
        return "default"


def _testing_boundaries_template() -> str:
    """Testing-focused generic boundaries."""
    return """## Boundaries

### ALWAYS
- ✅ Run build verification before tests (block if compilation fails)
- ✅ Execute in technology-specific test runner (pytest/vitest/dotnet test)
- ✅ Report failures with actionable error messages (aid debugging)
- ✅ Enforce 100% test pass rate (zero tolerance for failures)
- ✅ Validate test coverage thresholds (ensure quality gates met)

### NEVER
- ❌ Never approve code with failing tests (zero tolerance policy)
- ❌ Never skip compilation check (prevents false positive test runs)
- ❌ Never modify test code to make tests pass (integrity violation)
- ❌ Never ignore coverage below threshold (quality gate bypass prohibited)
- ❌ Never run tests without dependency installation (environment consistency required)

### ASK
- ⚠️ Coverage 70-79%: Ask if acceptable given task complexity and risk level
- ⚠️ Performance tests failing: Ask if acceptable for non-production changes
- ⚠️ Flaky tests detected: Ask if quarantine or fix immediately
"""


def _architecture_boundaries_template() -> str:
    """Architecture-focused generic boundaries."""
    return """## Boundaries

### ALWAYS
- ✅ Evaluate against SOLID principles (detect violations early)
- ✅ Assess design patterns for appropriateness (prevent over-engineering)
- ✅ Check for separation of concerns (enforce clean architecture)
- ✅ Review dependency management (minimize coupling)
- ✅ Validate testability of proposed design (enable quality assurance)

### NEVER
- ❌ Never approve tight coupling between layers (violates maintainability)
- ❌ Never accept violations of established patterns (consistency required)
- ❌ Never skip assessment of design complexity (prevent technical debt)
- ❌ Never approve design without considering testability (quality gate)
- ❌ Never ignore dependency injection opportunities (enable flexibility)

### ASK
- ⚠️ New pattern introduction: Ask if justified given team familiarity
- ⚠️ Trade-off between performance and maintainability: Ask for priority
- ⚠️ Refactoring scope exceeds task boundary: Ask if should split task
"""


def _code_review_boundaries_template() -> str:
    """Code review-focused generic boundaries."""
    return """## Boundaries

### ALWAYS
- ✅ Run linters before review (catch mechanical issues early)
- ✅ Check for code duplication (enforce DRY principle)
- ✅ Validate error handling completeness (ensure robustness)
- ✅ Verify consistent naming conventions (maintain readability)
- ✅ Ensure adequate code comments (support maintainability)

### NEVER
- ❌ Never approve code with linting errors (quality baseline)
- ❌ Never skip security vulnerability checks (safety critical)
- ❌ Never accept copy-paste duplication (technical debt source)
- ❌ Never approve missing error handling (reliability violation)
- ❌ Never ignore inconsistent formatting (team standard breach)

### ASK
- ⚠️ Style preference conflicts with project standards: Ask for clarification
- ⚠️ Refactoring suggestion exceeds scope: Ask if should defer
- ⚠️ Performance optimization needed but complex: Ask for priority
"""


def _orchestration_boundaries_template() -> str:
    """Orchestration-focused generic boundaries."""
    return """## Boundaries

### ALWAYS
- ✅ Execute phases in defined sequence (ensure workflow integrity)
- ✅ Validate prerequisites before phase execution (prevent failures)
- ✅ Capture state transitions in task metadata (enable traceability)
- ✅ Enforce quality gates at checkpoints (maintain standards)
- ✅ Provide clear progress indicators (support transparency)

### NEVER
- ❌ Never skip required phases (workflow integrity violation)
- ❌ Never proceed if prerequisites not met (dependency failure)
- ❌ Never bypass quality gates (standard erosion)
- ❌ Never lose state during transitions (data integrity issue)
- ❌ Never execute out-of-sequence phases (workflow corruption)

### ASK
- ⚠️ Quality gate failure with borderline metrics: Ask if acceptable
- ⚠️ Workflow customization requested: Ask if deviates from standard
- ⚠️ Phase timeout but progress visible: Ask if should extend
"""


def _default_boundaries_template() -> str:
    """Default generic boundaries for unrecognized agent types."""
    return """## Boundaries

### ALWAYS
- ✅ Execute core responsibilities as defined in Purpose section (role clarity)
- ✅ Follow established patterns in technology stack (consistency)
- ✅ Validate inputs before processing (error prevention)
- ✅ Provide clear, actionable feedback (user guidance)
- ✅ Document assumptions and constraints (transparency)

### NEVER
- ❌ Never skip validation steps (quality assurance)
- ❌ Never modify code without understanding context (safety)
- ❌ Never generate content without verification (accuracy)
- ❌ Never ignore user constraints (respect requirements)
- ❌ Never proceed if prerequisites missing (dependency management)

### ASK
- ⚠️ High-risk changes requiring approval (risk management)
- ⚠️ Conflicting requirements or constraints (decision needed)
- ⚠️ Uncertain approach with multiple valid options (human judgment)
"""


# TASK-FIX-PD04: Generic boundary detection markers
# These phrases appear in generic boundaries but not in AI-specific boundaries
_GENERIC_BOUNDARY_MARKERS = [
    "Execute core responsibilities as defined in Purpose section",
    "Follow established patterns in technology stack",
    "Validate inputs before processing",
    "Provide clear, actionable feedback",
    "Document assumptions and constraints",
    # From testing template
    "Run build verification before tests",
    "Execute in technology-specific test runner",
    # From architecture template
    "Evaluate against SOLID principles",
    "Assess design patterns for appropriateness",
    # From code_review template
    "Verify all tests pass before approval",
    "Check code style consistency",
    # From orchestration template
    "Execute phases in defined sequence",
    "Validate prerequisites before phase execution",
]


def is_generic_boundaries(boundaries_content: str) -> bool:
    """
    Detect if boundaries content is generic (template-based) or AI-specific.

    TASK-FIX-PD04: Used to determine if AI-generated boundaries should replace
    existing generic boundaries during merge.

    Generic boundaries contain recognizable template phrases that are not
    technology-specific. AI-generated boundaries contain domain-specific
    terminology (e.g., "onMount", "reactive declarations", "Firestore listeners").

    Args:
        boundaries_content: The boundaries section content to analyze

    Returns:
        True if boundaries appear to be generic (template-based)
        False if boundaries appear to be AI-generated (technology-specific)

    Example:
        >>> generic = "## Boundaries\\n### ALWAYS\\n- ✅ Execute core responsibilities..."
        >>> is_generic_boundaries(generic)
        True

        >>> ai_specific = "## Boundaries\\n### ALWAYS\\n- ✅ Use onMount lifecycle hook..."
        >>> is_generic_boundaries(ai_specific)
        False
    """
    if not boundaries_content:
        return False

    # Check if any generic marker phrases appear in the content
    content_lower = boundaries_content.lower()

    for marker in _GENERIC_BOUNDARY_MARKERS:
        if marker.lower() in content_lower:
            return True

    return False
