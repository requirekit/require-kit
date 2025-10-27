# Analysis: JSON vs Markdown-Only for Implementation Plans

**Date**: October 18, 2025
**Question**: Do we need dual format (JSON + Markdown) or is markdown-only sufficient?
**Context**: TASK-027 currently includes REQ-PLAN-MD-002 (maintain JSON for programmatic access)

---

## TL;DR Recommendation

**Drop the JSON backup. Go markdown-only.**

**Reasons**:
1. ❌ No code currently does programmatic parsing of plans
2. ❌ Dual format = 2x storage, 2x sync issues, 2x maintenance
3. ✅ Markdown can be parsed programmatically if needed (frontmatter, python-markdown)
4. ✅ Simpler is better (Lite approach philosophy)
5. ✅ Matches Hubbard's pattern (just .md files)

---

## Current State Analysis

### What Uses Plans Today

**Current usage** (from `plan_persistence.py`):
```python
def load_plan(task_id: str) -> Optional[Dict[str, Any]]:
    """Load implementation plan from disk."""
    plan_path = Path("docs/state") / task_id / "implementation_plan.json"

    if not plan_path.exists():
        return None

    with open(plan_path, 'r') as f:
        return json.load(f)  # Returns dict
```

**Who calls `load_plan()`?**
Based on grep results:
- `plan_persistence.py` itself (internal usage)
- Likely called by Phase 5.5 plan audit (TASK-025, not yet implemented)
- Likely called by `/task-refine` (TASK-026, not yet implemented)
- Possibly Phase 2.8 checkpoint display

**Key finding**: The returned `Dict[str, Any]` is used for:
1. **Displaying plan summary** (convert to string anyway)
2. **Comparing files** (can extract from markdown)
3. **Checking dependencies** (can extract from markdown)
4. **Calculating LOC variance** (can extract from markdown)

**None of these require JSON specifically.**

---

## Dual Format Problems

### Problem 1: Synchronization Issues
```
# Scenario: Human edits markdown plan
docs/state/TASK-042/
  implementation_plan.md   # Human edited, added SessionStore.ts
  implementation_plan.json # Stale, doesn't include SessionStore.ts

# Which is source of truth?
# If we re-save, do we overwrite human's markdown edits?
# If we don't, JSON and markdown diverge
```

**Complexity**: Need sync logic, conflict resolution, dirty tracking

### Problem 2: Storage Bloat
```
# Current: ~100 tasks with plans
docs/state/
  TASK-001/
    implementation_plan.json (2KB)
    implementation_plan.md   (2KB)
  TASK-002/
    implementation_plan.json (3KB)
    implementation_plan.md   (3KB)
  ...
  TASK-100/
    implementation_plan.json (2.5KB)
    implementation_plan.md   (2.5KB)

Total: ~500KB (100 tasks × 5KB average × 2 formats)
With markdown only: ~250KB (50% reduction)
```

**Impact**: 2x storage for questionable benefit

### Problem 3: Maintenance Burden
```python
# With dual format:
def save_plan(task_id, plan):
    # Save JSON
    save_as_json(plan)

    # Save Markdown
    render_and_save_as_markdown(plan)

    # What if one fails and other succeeds?
    # What if formats diverge?

# With markdown only:
def save_plan(task_id, plan):
    render_and_save_as_markdown(plan)
    # Done. Simple.
```

### Problem 4: Unclear Source of Truth
```python
# Which to load?
def load_plan(task_id):
    md_path = get_markdown_path(task_id)
    json_path = get_json_path(task_id)

    # Both exist - which is newer?
    # Human edited markdown - do we trust it?
    # JSON has metadata markdown doesn't - how to merge?

    # Complexity explosion
```

---

## Markdown-Only Benefits

### Benefit 1: Single Source of Truth
```
docs/state/TASK-042/
  implementation_plan.md   # The plan. Period.

# Clear, unambiguous, simple
```

### Benefit 2: Markdown IS Programmable
```python
# Example: Parse markdown to extract files
import frontmatter
import re

def parse_plan(md_path: Path) -> Dict[str, Any]:
    """Parse markdown plan into structured data."""

    content = md_path.read_text()
    post = frontmatter.loads(content)

    # Extract from frontmatter (if present)
    metadata = post.metadata

    # Extract from markdown sections
    files = extract_section(post.content, "## Files to Create")
    deps = extract_section(post.content, "## Dependencies")
    risks = extract_section(post.content, "## Risks")

    return {
        'files_to_create': files,
        'dependencies': deps,
        'risks': risks,
        **metadata
    }

def extract_section(content: str, heading: str) -> List[str]:
    """Extract list items from markdown section."""
    # Find section
    match = re.search(f"{heading}\n(.*?)\n##", content, re.DOTALL)
    if not match:
        return []

    section = match.group(1)

    # Extract list items
    items = re.findall(r"^- `(.+?)`", section, re.MULTILINE)
    return items
```

**Libraries available**:
- `python-frontmatter` - Parse frontmatter + markdown
- `python-markdown` - Full markdown parsing
- `mistune` - Fast markdown parser
- `marko` - CommonMark parser

**Conclusion**: Markdown is just as programmable as JSON, with better human experience.

### Benefit 3: Simpler Implementation
```python
# Markdown-only save_plan
def save_plan(task_id: str, plan: Dict[str, Any]) -> str:
    """Save plan as markdown."""
    state_dir = Path("docs/state") / task_id
    state_dir.mkdir(parents=True, exist_ok=True)

    # Render template
    renderer = PlanMarkdownRenderer()
    markdown = renderer.render(plan)

    # Save
    md_path = state_dir / "implementation_plan.md"
    md_path.write_text(markdown)

    return str(md_path)

# That's it. No dual-format logic, no sync issues.
```

### Benefit 4: Human Editability
```markdown
<!-- Human can just edit this -->
## Files to Create
- `src/auth/AuthService.ts` - Main auth service
- `src/auth/TokenManager.ts` - JWT handling
- `src/auth/SessionStore.ts` - NEW: Session persistence

<!-- Git commit, Claude reads updated plan, implements all 3 files -->
```

**With JSON backup**: Risk of divergence, unclear which to trust

**Markdown-only**: Edit is source of truth, no ambiguity

### Benefit 5: Aligns with Research
**Hubbard**: "Plan (write this as a .md file, save in plans/ directory)"
- ✅ Uses .md
- ❌ No JSON backup mentioned

**Simplicity principle**: Don't add complexity without proven need

---

## Counterarguments & Rebuttals

### Argument 1: "JSON is faster to parse"
**Rebuttal**:
- Plans are small (2-5KB)
- Parsing markdown takes <10ms
- Not a bottleneck (done once per task)
- Not worth 2x storage + sync complexity

### Argument 2: "JSON guarantees structure"
**Rebuttal**:
- Frontmatter in markdown provides structure
- Template ensures consistent format
- Parser can validate structure
- If markdown is malformed, parser fails gracefully
- Human-edited markdown is a feature, not a bug

### Argument 3: "What if we need complex queries?"
**Rebuttal**:
- Current usage: Display, compare files, extract deps
- None require complex queries
- If future needs arise, can parse markdown
- Or add SQLite index (separate from storage format)
- JSON backup doesn't help with queries anyway

### Argument 4: "Backward compatibility"
**Rebuttal**:
- Keep JSON reading in `load_plan()` for legacy
- New plans: markdown only
- Old plans: Still readable (JSON)
- Gradual migration, no breaking changes
- Can add migration script if needed

---

## Recommended Approach: Markdown-Only

### Implementation (Simplified TASK-027)

**REQ-PLAN-MD-002 REMOVED**

New requirements:
```yaml
requirements:
  - REQ-PLAN-MD-001: Save plans as markdown (.md) files
  - REQ-PLAN-MD-002-REVISED: Read legacy JSON plans for backward compatibility
  - REQ-PLAN-MD-003: Human-readable format with proper structure
  - REQ-PLAN-MD-004: Git diffs show meaningful plan changes
  - REQ-PLAN-MD-005: Enable easy manual editing
  - REQ-PLAN-MD-006: Programmatic parsing via markdown parser
```

### Code Changes

#### save_plan() - Markdown only
```python
def save_plan(
    task_id: str,
    plan: Dict[str, Any],
    review_result: Optional[Dict[str, Any]] = None
) -> str:
    """Save implementation plan as markdown."""

    state_dir = Path("docs/state") / task_id
    state_dir.mkdir(parents=True, exist_ok=True)

    # Add metadata
    plan_with_metadata = {
        "task_id": task_id,
        "saved_at": datetime.now().isoformat(),
        "version": 1,
        "plan": plan,
        "architectural_review": review_result
    }

    # Render and save markdown
    renderer = PlanMarkdownRenderer()
    markdown = renderer.render(plan_with_metadata)

    md_path = state_dir / "implementation_plan.md"
    md_path.write_text(markdown)

    return str(md_path.absolute())
```

#### load_plan() - Markdown with JSON fallback
```python
def load_plan(task_id: str) -> Optional[Dict[str, Any]]:
    """Load implementation plan, preferring markdown."""

    md_path = Path("docs/state") / task_id / "implementation_plan.md"
    json_path = Path("docs/state") / task_id / "implementation_plan.json"

    # Try markdown first (new format)
    if md_path.exists():
        parser = PlanMarkdownParser()
        return parser.parse_file(md_path)

    # Fall back to JSON (legacy format)
    elif json_path.exists():
        with open(json_path) as f:
            return json.load(f)

    # No plan found
    else:
        return None
```

#### PlanMarkdownParser
```python
class PlanMarkdownParser:
    """Parse markdown plans back to structured data."""

    def parse_file(self, md_path: Path) -> Dict[str, Any]:
        """Parse markdown file into plan dict."""
        import frontmatter

        content = md_path.read_text()

        # Parse frontmatter + content
        post = frontmatter.loads(content)

        # Build plan dict from markdown sections
        plan = {
            'task_id': self._extract_from_frontmatter(post, 'task_id'),
            'saved_at': self._extract_from_frontmatter(post, 'saved_at'),
            'plan': {
                'files_to_create': self._extract_files(post.content),
                'dependencies': self._extract_dependencies(post.content),
                'estimated_loc': self._extract_loc(post.content),
                'estimated_duration': self._extract_duration(post.content),
                'risks': self._extract_risks(post.content)
            },
            'architectural_review': self._extract_review(post.content)
        }

        return plan

    def _extract_files(self, content: str) -> List[str]:
        """Extract files from '## Files to Create' section."""
        section = self._get_section(content, "## Files to Create")
        # Parse list items: - `path/to/file.ts` - Description
        files = re.findall(r"^- `(.+?)`", section, re.MULTILINE)
        return files

    # Similar methods for other sections...
```

### Storage Structure (Markdown-Only)
```
docs/state/TASK-042/
  implementation_plan.md      # The plan (source of truth)
  plan_audit.json             # Audit results (separate)
  complexity_score.json       # Complexity eval (separate)
  refinements/                # Refinement sessions (separate)
    refine-001.md
    refine-002.md
```

**Benefits**:
- ✅ One plan file (clear)
- ✅ Related data in separate files (organized)
- ✅ No dual-format sync issues
- ✅ Human-readable throughout

---

## Migration Strategy

### Phase 1: Add Markdown Support (Week 1)
- Implement `PlanMarkdownRenderer`
- Implement `PlanMarkdownParser`
- Update `save_plan()` to save markdown only
- Update `load_plan()` to read markdown first, fall back to JSON

### Phase 2: Test with New Tasks (Week 2-3)
- All new tasks save markdown only
- Legacy JSON plans still readable
- Monitor for issues

### Phase 3: Optional Cleanup (Week 4+)
- Add migration script (convert JSON → markdown)
- Run on backlog if desired
- Delete JSON files once migrated
- Not required, can coexist indefinitely

---

## Effort Comparison

### Original TASK-027 (Dual Format)
**Components**:
1. Markdown renderer (2h)
2. Markdown parser (1h)
3. Dual-format save logic (1h)
4. Dual-format load logic (1h)
5. Sync/conflict resolution (2h)
6. Testing dual-format edge cases (2h)

**Total**: ~9 hours

### Simplified TASK-027 (Markdown-Only)
**Components**:
1. Markdown renderer (2h)
2. Markdown parser (1h)
3. Simple save logic (30min)
4. Simple load logic (30min)
5. Testing (1h)

**Total**: ~5 hours

**Savings**: 4 hours (44% reduction)

---

## Decision Matrix

| Factor | Dual Format | Markdown-Only | Winner |
|--------|-------------|---------------|---------|
| **Complexity** | High (sync logic) | Low (single file) | ✅ MD |
| **Storage** | 2x files | 1x files | ✅ MD |
| **Human Readability** | .md readable | .md readable | ✅ Tie |
| **Git Diffs** | Good (md) | Good (md) | ✅ Tie |
| **Programmatic Access** | Native (json) | Parse needed | ⚠️ JSON |
| **Editability** | Risky (divergence) | Safe (source of truth) | ✅ MD |
| **Maintenance** | Complex | Simple | ✅ MD |
| **Research Alignment** | Partial | Full (Hubbard) | ✅ MD |
| **Implementation Time** | 9h | 5h | ✅ MD |

**Score**: Markdown-Only wins 6-1 (with 2 ties)

---

## Conclusion & Recommendation

### Drop REQ-PLAN-MD-002 (Dual Format)

**Reasons**:
1. ❌ **No proven need** for JSON programmatic access
2. ❌ **Sync complexity** outweighs benefits
3. ❌ **2x storage** for marginal gain
4. ✅ **Markdown is programmable** (frontmatter, parsers)
5. ✅ **Simpler is better** (Lite philosophy)
6. ✅ **Matches research** (Hubbard uses .md only)
7. ✅ **Saves 4 hours** implementation time

### Updated TASK-027 Scope

**Remove**:
- Dual-format save logic
- Dual-format load logic
- Sync/conflict resolution
- JSON backup maintenance

**Keep**:
- Markdown rendering
- Markdown parsing
- Legacy JSON reading (backward compat)
- All human-readability benefits

**Effort**: 5 hours (down from 9 hours)

### Next Steps

1. Update TASK-027 to remove REQ-PLAN-MD-002
2. Simplify acceptance criteria (no dual-format)
3. Implement markdown-only approach
4. Keep JSON fallback for legacy plans
5. Monitor usage, confirm no issues

**If future needs arise** (unlikely):
- Can always add JSON export function
- Can index plans in SQLite for queries
- Can add JSON API endpoint
- Markdown doesn't prevent these options

---

## Final Verdict

**Markdown-only is the right choice.**

Go simple. Match Hubbard's pattern. Avoid unnecessary complexity. The Lite approach doesn't need enterprise dual-format storage.

**Recommendation**: Update TASK-027 to drop dual-format requirement.
