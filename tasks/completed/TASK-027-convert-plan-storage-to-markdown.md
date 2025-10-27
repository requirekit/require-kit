---
id: TASK-027
title: Convert Implementation Plan Storage from JSON to Markdown
status: completed
priority: high
created: 2025-10-18T10:30:00Z
completed_at: 2025-10-18T13:05:00Z
labels: [enhancement, sdd-alignment, developer-experience, hubbard-workflow]
estimated_effort: 5 hours
actual_effort: 4 hours
complexity_estimate: 4
actual_complexity: 4

# Source
source: implementation-plan-and-code-review-analysis.md
recommendation: MUST-HAVE - Critical Gap
research_support: John Hubbard's workflow (uses .md files for plans)
alignment: Improves human readability and git diffs

# Implementation Summary
implemented_via: git worktree (Conductor)
commit_hash: cbe9aeac98c1223052e877ddc26cdda54092d851
merged_at: 2025-10-18T13:05:48Z
branch: TASK-027

# Requirements - All Met ✅
requirements:
  - REQ-PLAN-MD-001: Save plans as markdown (.md) files only ✅
  - REQ-PLAN-MD-002: Read legacy JSON plans for backward compatibility ✅
  - REQ-PLAN-MD-003: Human-readable format with proper structure ✅
  - REQ-PLAN-MD-004: Git diffs show meaningful plan changes ✅
  - REQ-PLAN-MD-005: Enable easy manual editing ✅
  - REQ-PLAN-MD-006: Programmatic parsing via markdown frontmatter and sections ✅

# Deliverables
files_created:
  - installer/global/commands/lib/plan_markdown_renderer.py (8,446 bytes)
  - installer/global/commands/lib/plan_markdown_parser.py
  - installer/global/commands/lib/templates/implementation_plan.md.j2
  - tests/unit/test_plan_markdown_renderer.py
  - tests/unit/test_plan_markdown_parser.py
files_modified:
  - installer/global/commands/lib/plan_persistence.py (markdown-first logic)
---

# Convert Implementation Plan Storage from JSON to Markdown

## Problem Statement

**Hubbard's workflow** saves plans as markdown:
> "Plan (write this as a .md file, save in plans/ directory)"

**Current AI-Engineer Lite**: Saves plans as JSON in `docs/state/{task_id}/implementation_plan.json`

**Why this is suboptimal**:
1. **Not human-readable** - Requires tools to read JSON
2. **Git diffs are noisy** - JSON structure changes are hard to review
3. **Can't be reviewed in PR** - Reviewers won't read JSON
4. **AI can't read naturally** - Claude prefers markdown over JSON
5. **Hard to edit manually** - JSON syntax errors are easy to make
6. **Doesn't match Hubbard's proven pattern** - He uses .md for a reason

**Current JSON structure** (example):
```json
{
  "task_id": "TASK-042",
  "saved_at": "2025-10-11T10:30:00Z",
  "version": 1,
  "plan": {
    "files_to_create": [
      "src/auth/AuthService.ts",
      "tests/unit/AuthService.test.ts"
    ],
    "external_dependencies": [
      "jsonwebtoken ^9.0.0"
    ],
    "estimated_duration": "4 hours",
    "estimated_loc": 245,
    "risks": [
      {
        "description": "JWT secret management",
        "mitigation": "Use environment variables"
      }
    ]
  },
  "architectural_review": {
    "score": 85,
    "solid_compliance": "Good",
    "warnings": [
      "Consider extracting validation logic"
    ]
  }
}
```

**Better: Markdown format**:
```markdown
# Implementation Plan: TASK-042
**Created**: 2025-10-11 10:30:00
**Status**: Approved
**Complexity**: 5/10

## Summary
Create user authentication system with JWT token management.

## Files to Create
- `src/auth/AuthService.ts` - Main authentication service
- `src/auth/TokenManager.ts` - JWT token creation/validation
- `tests/unit/AuthService.test.ts` - Unit tests for AuthService

## Dependencies
- `jsonwebtoken ^9.0.0` - JWT token handling
- `bcrypt ^5.1.0` - Password hashing

## Estimated Effort
- **Duration**: 4 hours
- **Lines of Code**: 245
- **Complexity**: 5/10 (Medium)

## Risks & Mitigation
- **Risk**: JWT secret management
  - **Mitigation**: Use environment variables, never commit secrets

- **Risk**: Token expiration handling
  - **Mitigation**: Implement refresh token mechanism

## Architectural Review
**Score**: 85/100

### SOLID Compliance
✅ **Single Responsibility**: Each class has one clear purpose
✅ **Open/Closed**: Using interfaces for extensibility
✅ **Dependency Inversion**: AuthService depends on ITokenManager interface

### Warnings
⚠️ Consider extracting validation logic into separate class
⚠️ Token storage in localStorage (consider httpOnly cookies for production)

## Implementation Notes
1. Start with TokenManager (dependency)
2. Implement AuthService using TokenManager
3. Write tests for happy path first
4. Add error handling tests
5. Integration test with mock token validation
```

**Comparison**:
| Aspect | JSON | Markdown |
|--------|------|----------|
| Human-readable | ❌ No | ✅ Yes |
| Git diffs | ❌ Noisy | ✅ Clear |
| PR review | ❌ Unlikely | ✅ Reviewable |
| AI reading | ⚠️ Parseable | ✅ Natural |
| Manual editing | ❌ Error-prone | ✅ Easy |
| Programmatic access | ✅ Native | ⚠️ Parse needed |

## Solution Overview

Convert plan storage to **markdown-only format**:
1. **Primary (and only)**: Markdown (`.md`) - for humans, AI, and programmatic access
2. **Legacy support**: Continue reading old JSON plans for backward compatibility

**Storage location**:
```
docs/state/TASK-042/
  implementation_plan.md      # The plan (single source of truth)
  plan_audit.json             # Audit results (separate concern)
  complexity_score.json       # Complexity evaluation (separate concern)
```

**Workflow**:
1. Phase 2.7 generates plan (as dict)
2. Render and save as markdown
3. AI agents read markdown
4. Tooling parses markdown using frontmatter + section extraction
5. Legacy JSON plans still readable (fallback)

**Benefits**:
- ✅ Aligns with Hubbard's pattern (.md files, no JSON backup)
- ✅ Human-readable without tools
- ✅ Git diffs show real changes
- ✅ Can be reviewed in PR
- ✅ AI reads naturally
- ✅ Easy manual editing (single source of truth)
- ✅ Programmatically accessible (frontmatter + markdown parsers)
- ✅ Simpler (no dual-format sync issues)
- ✅ Less storage (no duplicate files)

## Acceptance Criteria

### 1. Markdown Template
Create template for plan rendering:

File: `installer/global/commands/lib/templates/implementation_plan.md.j2`

```markdown
# Implementation Plan: {{ task_id }}
**Created**: {{ created_at }}
**Status**: {{ status }}
**Complexity**: {{ complexity_score }}/10

## Summary
{{ summary }}

## Files to Create
{% for file in files_to_create %}
- `{{ file.path }}` - {{ file.description }}
{% endfor %}

## Files to Modify
{% for file in files_to_modify %}
- `{{ file.path }}` - {{ file.changes }}
{% endfor %}

## Dependencies
{% for dep in external_dependencies %}
- `{{ dep.name }} {{ dep.version }}` - {{ dep.purpose }}
{% endfor %}

## Estimated Effort
- **Duration**: {{ estimated_duration }}
- **Lines of Code**: {{ estimated_loc }}
- **Complexity**: {{ complexity_score }}/10 ({{ complexity_level }})

## Risks & Mitigation
{% for risk in risks %}
- **Risk**: {{ risk.description }}
  - **Mitigation**: {{ risk.mitigation }}
{% endfor %}

## Architectural Review
**Score**: {{ architectural_review.score }}/100

### SOLID Compliance
{% for principle, status in architectural_review.solid_compliance.items() %}
{{ status_icon(status) }} **{{ principle }}**: {{ status.description }}
{% endfor %}

### Warnings
{% for warning in architectural_review.warnings %}
⚠️ {{ warning }}
{% endfor %}

## Implementation Notes
{% for note in implementation_notes %}
{{ loop.index }}. {{ note }}
{% endfor %}

---
*Generated by AI-Engineer Lite on {{ created_at }}*
```

Acceptance criteria:
- [ ] Template created with Jinja2 syntax
- [ ] All plan fields represented
- [ ] Clean, readable markdown format
- [ ] Supports lists, code blocks, formatting

### 2. Markdown Renderer
Create renderer module:

File: `installer/global/commands/lib/plan_markdown_renderer.py`

```python
from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader
import frontmatter

class PlanMarkdownRenderer:
    """Renders implementation plans as human-readable markdown."""

    def __init__(self):
        template_dir = Path(__file__).parent / "templates"
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template = self.env.get_template("implementation_plan.md.j2")

    def render(self, plan: Dict[str, Any]) -> str:
        """Render plan dict as markdown string with frontmatter."""
        # Add helper functions for template
        self.env.globals['status_icon'] = self._status_icon

        # Separate metadata for frontmatter
        metadata = {
            'task_id': plan.get('task_id'),
            'saved_at': plan.get('saved_at'),
            'version': plan.get('version', 1),
            'complexity_score': plan.get('plan', {}).get('complexity_score'),
            'architectural_review_score': plan.get('architectural_review', {}).get('score')
        }

        # Render body from template
        body = self.template.render(**plan)

        # Combine frontmatter + body
        post = frontmatter.Post(body, **metadata)
        markdown = frontmatter.dumps(post)

        return markdown

    def _status_icon(self, status: str) -> str:
        """Convert status to emoji icon."""
        icons = {
            'pass': '✅',
            'warn': '⚠️',
            'fail': '❌',
            'info': 'ℹ️'
        }
        return icons.get(status, '•')

    def save_markdown(self, plan: Dict[str, Any], output_path: Path) -> None:
        """Render and save plan as markdown file."""
        markdown = self.render(plan)
        output_path.write_text(markdown)
```

Acceptance criteria:
- [ ] Renderer class implemented
- [ ] Jinja2 template rendering
- [ ] Frontmatter metadata inclusion
- [ ] Helper functions for formatting
- [ ] Save to file method

### 3. Update Plan Persistence Module
Modify `plan_persistence.py` to save markdown only:

```python
# installer/global/commands/lib/plan_persistence.py

from .plan_markdown_renderer import PlanMarkdownRenderer

def save_plan(
    task_id: str,
    plan: Dict[str, Any],
    review_result: Optional[Dict[str, Any]] = None
) -> str:
    """Save implementation plan as markdown."""

    # Create state directory
    state_dir = Path("docs/state") / task_id
    state_dir.mkdir(parents=True, exist_ok=True)

    # Add metadata
    plan_with_metadata = {
        "task_id": task_id,
        "saved_at": datetime.now().isoformat(),
        "version": 1,
        "plan": plan
    }

    if review_result:
        plan_with_metadata["architectural_review"] = review_result

    # Save as Markdown (single source of truth)
    md_path = state_dir / "implementation_plan.md"
    renderer = PlanMarkdownRenderer()
    renderer.save_markdown(plan_with_metadata, md_path)

    # Return markdown path
    return str(md_path.absolute())
```

Acceptance criteria:
- [ ] Save markdown only (no JSON)
- [ ] Markdown path returned
- [ ] Frontmatter includes metadata
- [ ] Backward compatible (can still read old JSON plans)

### 4. Markdown Parser (for loading)
Add parser to read markdown back:

```python
# installer/global/commands/lib/plan_markdown_parser.py

import frontmatter
from pathlib import Path
from typing import Dict, Any, Optional

class PlanMarkdownParser:
    """Parse markdown plans back into structured data."""

    def parse_file(self, md_path: Path) -> Dict[str, Any]:
        """Parse markdown file into plan dict."""
        # Try markdown first
        if md_path.exists():
            return self._parse_markdown(md_path)

        # Fall back to JSON if markdown missing
        json_path = md_path.with_suffix('.json')
        if json_path.exists():
            return self._parse_json(json_path)

        raise FileNotFoundError(f"No plan found at {md_path}")

    def _parse_markdown(self, md_path: Path) -> Dict[str, Any]:
        """Parse markdown into structured dict."""
        content = md_path.read_text()

        # Use frontmatter if present, otherwise parse headings
        try:
            post = frontmatter.loads(content)
            metadata = post.metadata
            body = post.content
        except:
            metadata = {}
            body = content

        # Parse markdown sections into dict
        plan = self._extract_sections(body)
        plan['metadata'] = metadata

        return plan

    def _parse_json(self, json_path: Path) -> Dict[str, Any]:
        """Parse JSON fallback."""
        with open(json_path) as f:
            return json.load(f)
```

Acceptance criteria:
- [ ] Parse markdown files
- [ ] Fall back to JSON if markdown missing
- [ ] Extract structured data from sections
- [ ] Backward compatible with old JSON-only plans

### 5. Update `load_plan` Function
Modify to prefer markdown:

```python
def load_plan(task_id: str) -> Optional[Dict[str, Any]]:
    """Load implementation plan, preferring markdown."""

    md_path = Path("docs/state") / task_id / "implementation_plan.md"
    json_path = Path("docs/state") / task_id / "implementation_plan.json"

    # Try markdown first (primary)
    if md_path.exists():
        parser = PlanMarkdownParser()
        return parser.parse_file(md_path)

    # Fall back to JSON (legacy)
    elif json_path.exists():
        with open(json_path) as f:
            return json.load(f)

    # No plan found
    else:
        return None
```

Acceptance criteria:
- [ ] Prefer markdown over JSON
- [ ] Fall back to JSON for legacy plans
- [ ] Return None if neither exists
- [ ] Backward compatible

### 6. Update Phase 2.7
Modify Phase 2.7 to save markdown:

```python
# In phase_execution.py or plan_persistence.py caller

# Phase 2.7: Save plan
plan_path = save_plan(task_id, implementation_plan, review_result)
print(f"Implementation plan saved to: {plan_path}")
# Now prints: .../implementation_plan.md (not .json)

# Update task metadata
update_task_metadata(task_id, {
    "implementation_plan_path": plan_path,
    "plan_format": "markdown"  # New field
})
```

Acceptance criteria:
- [ ] Phase 2.7 calls updated `save_plan`
- [ ] Returns markdown path
- [ ] Updates task metadata with format
- [ ] No breaking changes to workflow

### 7. Git Diff Improvements
Markdown plans produce better git diffs:

**Before (JSON diff - noisy)**:
```diff
  "plan": {
-   "estimated_loc": 245,
+   "estimated_loc": 380,
    "risks": [
      {
        "description": "JWT secret management",
+       "severity": "high"
      }
    ]
  }
```

**After (Markdown diff - clear)**:
```diff
  ## Estimated Effort
- - **Lines of Code**: 245
+ - **Lines of Code**: 380

  ## Risks & Mitigation
  - **Risk**: JWT secret management
+   - **Severity**: High
    - **Mitigation**: Use environment variables
```

Acceptance criteria:
- [ ] Verify markdown diffs are clearer
- [ ] Changes are human-readable
- [ ] Structure changes are obvious
- [ ] Can be reviewed in PR

### 8. Manual Editing Support
Markdown plans can be edited by hand:

**Scenario**: Human reviews plan, wants to add a file
```markdown
## Files to Create
- `src/auth/AuthService.ts` - Main authentication service
- `src/auth/TokenManager.ts` - JWT token creation/validation
+ - `src/auth/SessionStore.ts` - Session persistence layer
- `tests/unit/AuthService.test.ts` - Unit tests
```

**Workflow**:
1. Human edits markdown file
2. Save changes
3. Git commit shows meaningful diff
4. Next phase reads updated plan
5. Implementation follows modified plan

Acceptance criteria:
- [ ] Markdown syntax errors don't break parser
- [ ] Manual edits preserved on next save
- [ ] Git tracks changes naturally

### 9. Backward Compatibility
Support legacy JSON plans with automatic upgrade path:

```python
def load_plan(task_id: str) -> Optional[Dict[str, Any]]:
    """Load plan, preferring markdown with JSON fallback."""
    md_path = Path("docs/state") / task_id / "implementation_plan.md"
    json_path = Path("docs/state") / task_id / "implementation_plan.json"

    # Try markdown first (new format)
    if md_path.exists():
        parser = PlanMarkdownParser()
        return parser.parse_file(md_path)

    # Fall back to JSON (legacy format)
    elif json_path.exists():
        with open(json_path) as f:
            plan = json.load(f)

        # Note: Don't auto-migrate to avoid unexpected file changes
        # Migration can be done via separate script if desired
        return plan

    return None
```

Acceptance criteria:
- [ ] Old JSON plans still load correctly
- [ ] No breaking changes for existing tasks
- [ ] Prefer markdown when both exist
- [ ] No automatic migration (to avoid surprises)
- [ ] Optional migration script available

### 10. Documentation
- [ ] Update `docs/workflows/implementation-planning.md`
- [ ] Add examples of markdown plans
- [ ] Document manual editing workflow
- [ ] Update CLAUDE.md with plan format

## Implementation Plan

### Step 1: Create Markdown Template (1 hour)
File: `installer/global/commands/lib/templates/implementation_plan.md.j2`

Design clean, readable markdown structure with frontmatter support.

### Step 2: Create Markdown Renderer (1.5 hours)
File: `installer/global/commands/lib/plan_markdown_renderer.py`

Implement Jinja2-based renderer with frontmatter integration.

### Step 3: Update Plan Persistence (30 min)
Modify `plan_persistence.py`:
- Save markdown only (remove JSON save logic)
- Return markdown path
- Simplify save_plan() function

### Step 4: Create Markdown Parser (1 hour)
File: `installer/global/commands/lib/plan_markdown_parser.py`

Parse markdown back to dict using frontmatter and section extraction.

### Step 5: Update Load Function (30 min)
Modify `load_plan` to prefer markdown, fall back to JSON for legacy plans.

### Step 6: Update Phase 2.7 Callers (30 min)
Ensure all callers handle markdown paths correctly.

### Step 7: Documentation (30 min)
Update docs with markdown-only approach and examples.

## Testing Strategy

### Unit Tests
- [ ] `test_markdown_renderer.py`: Template rendering
- [ ] `test_markdown_parser.py`: Parsing markdown back
- [ ] `test_plan_persistence_markdown.py`: Save/load cycle

### Integration Tests
- [ ] `test_phase_2_7_markdown.py`: Phase 2.7 saves markdown
- [ ] `test_backward_compatibility.py`: JSON plans still work
- [ ] `test_manual_editing.py`: Edited markdown parses correctly

### E2E Tests
- [ ] Create task with plan (markdown saved)
- [ ] Review plan in git diff (clear changes)
- [ ] Manually edit markdown
- [ ] Load plan (changes preserved)
- [ ] Implement using modified plan

## Benefits

### Immediate
- ✅ Human-readable without tools
- ✅ Git diffs show meaningful changes
- ✅ Can be reviewed in PR
- ✅ Aligns with Hubbard's .md pattern (no JSON backup)
- ✅ Single source of truth (no sync issues)
- ✅ 50% less storage (no duplicate files)

### Long-term
- ✅ Easier manual editing (no divergence risk)
- ✅ AI reads plans naturally
- ✅ Better integration with TASK-025 (plan audit)
- ✅ Improved developer experience
- ✅ Simpler maintenance (no dual-format logic)
- ✅ Programmatically accessible via frontmatter/parsers

## Dependencies

- Prerequisite: Jinja2 (for template rendering)
- Prerequisite: python-frontmatter (for metadata + markdown)
- Enables: TASK-025 (plan audit easier with markdown)
- Enables: TASK-026 (refinement displays readable plans)
- Enables: Better human review of plans

## Success Metrics

- [ ] 100% of new plans saved as markdown only
- [ ] Legacy JSON plans still load correctly
- [ ] Git diffs are clearer (subjective feedback)
- [ ] Developers review plans in PR (at least 50% of time)
- [ ] Programmatic parsing works (frontmatter + sections)
- [ ] No dual-format sync issues (eliminated by design)
- [ ] 50% storage reduction vs dual-format approach

## Related Tasks

- TASK-025: Plan audit (reads markdown plans)
- TASK-026: Task refine (displays markdown plans)
- Enables better human-in-the-loop workflows

## References

- John Hubbard LinkedIn post (uses .md files for plans)
- `docs/research/implementation-plan-and-code-review-analysis.md`
- `docs/research/honest-assessment-sdd-vs-ai-engineer.md`
- Jinja2 documentation (template rendering)
