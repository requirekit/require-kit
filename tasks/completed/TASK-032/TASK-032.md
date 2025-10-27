---
id: TASK-032
title: Implement MCP documentation updates from audit recommendations
status: completed
created: 2025-10-25T14:45:00Z
updated: 2025-10-25T19:15:00Z
completed: 2025-10-25T19:30:00Z
previous_state: in_review
state_transition_reason: "Task completed successfully - all quality gates passed"
completion_location: tasks/completed/TASK-032/
priority: medium
quality_gates:
  compilation: passed
  tests: passed (50/50 checks)
  coverage: not_applicable (documentation-only)
  architectural_review: 88/100 (approved)
  code_review: 95/100 (approved)
complexity_evaluation:
  total_score: 1
  review_mode: auto_proceed
  auto_approved: true
organized_files:
  - TASK-032.md
  - visual-summary.md
  - analysis-complete.md
  - requirements-summary.md
  - ears-requirements.md
  - requirements-analysis.md
  - analysis-readme.md
  - implementation-roadmap.md
completion_metrics:
  duration: "2.5 hours"
  files_created: 1
  files_modified: 3
  lines_added: 400
  quality_score: 95/100
tags: [documentation, mcp, optimization, best-practices]
epic: null
feature: null
requirements: []
external_ids:
  jira: null
  linear: null
bdd_scenarios: []
test_results:
  status: pending
  coverage: null
  last_run: null
parent_task: TASK-012
related_tasks:
  - TASK-012 (MCP Usage Audit)
  - TASK-013 (CLAUDE.md Optimization)
  - TASK-014 (Context7 Integration)
estimated_effort: "1.5 hours"
---

# Task: Implement MCP Documentation Updates from Audit Recommendations

## Description

Implement the Priority 1 documentation updates identified in the TASK-012 MCP usage audit. The audit confirmed that all MCP integrations are already optimized with no code changes needed. However, several documentation enhancements will improve developer guidance and ensure consistent MCP usage patterns.

**Context**: TASK-012 audit found all MCPs optimized (4.5-12% context window usage), but identified opportunities to document token budgets and best practices more explicitly.

## Parent Task Reference

**TASK-012**: Review MCP usage and optimize context window consumption
- Audit Status: ✅ COMPLETED
- Verdict: OPTIMIZED (no code changes needed)
- Report: `tasks/in_review/TASK-012-MCP-AUDIT-REPORT.md`

## Acceptance Criteria

### 1. Context7 Token Budget Documentation
- [x] Add token budget guidelines to `task-manager.md`
- [x] Document recommended token limits by phase:
  - Planning (Phase 2): 3000-4000 tokens
  - Implementation (Phase 3): 5000 tokens (current default)
  - Testing (Phase 4): 2000-3000 tokens
- [x] Include rationale for each budget
- [x] Add examples of appropriate vs. excessive documentation requests

### 2. Design Patterns MCP Guidance
- [x] Add maxResults parameter guidance to `pattern-advisor.md`
- [x] Document recommended limits:
  - `find_patterns`: Default 5 results, max 10
  - `get_pattern_details`: Only for top 1-2 patterns (not all)
- [x] Explain token cost per detailed pattern (~3k tokens)
- [x] Add examples of efficient vs. inefficient pattern queries

### 3. MCP Optimization Guide
- [x] Create new file: `docs/guides/mcp-optimization-guide.md`
- [x] Include 8-point MCP integration checklist:
  1. Lazy loading (command-specific or phase-specific)
  2. Scoped queries (topic, filter, category parameters)
  3. Token limits (default 5000, adjust per use case)
  4. Caching implementation (1-hour TTL for static data)
  5. Retry logic (3 attempts, exponential backoff)
  6. Fail fast (verify in Phase 0)
  7. Parallel calls (when possible)
  8. Token budget documentation
- [x] Add "when to use each MCP" decision tree
- [x] Include anti-patterns to avoid
- [x] Provide examples from existing implementations (Figma, Zeplin, Context7)

### 4. Cross-Reference Updates
- [x] Update CLAUDE.md to reference new MCP optimization guide
- [x] Add links from agent specs to relevant sections of optimization guide
- [x] Ensure all MCP-using agents reference token budgets

## Implementation Plan

### File 1: `installer/global/agents/task-manager.md`

**Location**: Lines 21-73 (Context7 MCP Usage section)

**Changes**:
```markdown
### Context7 Token Budget Guidelines

**Token limits by phase** (optimize context window usage):

| Phase | Token Budget | Rationale | Example Query |
|-------|--------------|-----------|---------------|
| **Phase 2: Planning** | 3000-4000 | High-level architecture, pattern overview | "fastapi dependency injection overview" |
| **Phase 3: Implementation** | 5000 (default) | Detailed API documentation, code examples | "fastapi dependency injection detailed examples" |
| **Phase 4: Testing** | 2000-3000 | Framework-specific testing patterns | "pytest fixtures and parametrize" |

**Appropriate Usage**:
- ✅ GOOD: `get-library-docs("/tiangolo/fastapi", topic="dependency-injection", tokens=5000)`
- ✅ GOOD: `get-library-docs("/pytest-dev/pytest", topic="fixtures", tokens=2500)`
- ⚠️ EXCESSIVE: `get-library-docs("/tiangolo/fastapi", tokens=10000)` (no topic scoping)

**When to adjust token budget**:
- **Increase to 6000**: High complexity tasks (score ≥7), unfamiliar framework
- **Decrease to 3000**: Planning phase, well-known library, specific topic
- **Decrease to 2000**: Testing frameworks (focused docs only)
```

### File 2: `installer/global/agents/pattern-advisor.md`

**Location**: After line 109 (in "find_patterns" section)

**Changes**:
```markdown
#### Token Budget and Result Limiting

**Recommended limits** (prevent context window bloat):
```yaml
find_patterns:
  maxResults: 5 (recommended) | 10 (maximum)
  token_cost_estimate: ~1000 tokens per pattern summary

get_pattern_details:
  usage: "Only for top 1-2 patterns (not all found patterns)"
  token_cost_estimate: ~3000 tokens per detailed pattern
```

**Efficient Query Pattern**:
1. Use `find_patterns` to get 5-10 pattern recommendations (5-10k tokens)
2. Analyze top 2-3 patterns by confidence score
3. Call `get_pattern_details` ONLY for the #1 pattern (3k tokens)
4. If #1 pattern insufficient, get details for #2 pattern (3k tokens)

**Anti-Pattern** (❌ DON'T DO THIS):
```typescript
// ❌ BAD: Fetching details for all 10 patterns = 30k tokens!
const patterns = await find_patterns(query, { maxResults: 10 });
for (const pattern of patterns) {
  await get_pattern_details(pattern.id);  // 3k tokens each
}

// ✅ GOOD: Only fetch top pattern details = 8k tokens total
const patterns = await find_patterns(query, { maxResults: 5 });  // 5k tokens
const topPattern = patterns[0];
const details = await get_pattern_details(topPattern.id);  // 3k tokens
```
```

### File 3: `docs/guides/mcp-optimization-guide.md` (NEW FILE)

**Full content** (see Test Requirements below for outline)

### File 4: `CLAUDE.md`

**Location**: After "Core AI Agents" section (around line 180)

**Changes**:
```markdown
## MCP Integration Best Practices

The system integrates with 4 MCP servers for enhanced capabilities:
- **context7**: Library documentation (automatically retrieved during implementation)
- **design-patterns**: Pattern recommendations (Phase 2.5A)
- **figma-dev-mode**: Figma design extraction (/figma-to-react)
- **zeplin**: Zeplin design extraction (/zeplin-to-maui)

**Optimization Status**: ✅ All MCPs optimized (4.5-12% context window usage)

**For detailed MCP usage guidelines**: [MCP Optimization Guide](docs/guides/mcp-optimization-guide.md)
```

## Test Requirements

### Validation Checklist

**Documentation Quality**:
- [ ] All token budgets clearly documented with rationale
- [ ] Examples provided for each MCP usage pattern
- [ ] Anti-patterns explicitly called out with ❌ markers
- [ ] Cross-references between files are accurate
- [ ] Markdown formatting is correct (tables, code blocks, lists)

**Completeness**:
- [ ] All 3 Priority 1 recommendations implemented
- [ ] MCP optimization guide includes all 8 checklist items
- [ ] Decision tree covers all 4 MCP servers
- [ ] Examples reference actual agent implementations

**Accuracy**:
- [ ] Token budget numbers match TASK-012 audit findings
- [ ] File paths and line numbers are correct
- [ ] Links between documents resolve correctly
- [ ] Technical details verified against agent specs

**Usability**:
- [ ] New developers can follow MCP integration checklist
- [ ] Token budgets are easy to reference during implementation
- [ ] Examples are copy-pasteable
- [ ] Guide is searchable (good headings, keywords)

## MCP Optimization Guide Outline

**File**: `docs/guides/mcp-optimization-guide.md`

```markdown
# MCP Optimization Guide

## Overview
- What are MCPs and why optimize?
- Current system status (4.5-12% context window usage)
- This guide's purpose

## 8-Point Integration Checklist
1. Lazy Loading (with examples from figma-react-orchestrator)
2. Scoped Queries (with examples from pattern-advisor)
3. Token Limits (table of defaults by MCP server)
4. Caching Implementation (1-hour TTL pattern)
5. Retry Logic (exponential backoff code example)
6. Fail Fast (Phase 0 verification pattern)
7. Parallel Calls (example from zeplin-maui-orchestrator)
8. Token Budget Documentation (reference to task-manager.md)

## MCP Server Reference

### context7 (Library Documentation)
- When to use
- Token budgets by phase
- Scoping with topic parameter
- Examples (good and bad)

### design-patterns (Pattern Recommendations)
- When to use
- maxResults guidance
- Efficient query patterns
- Anti-patterns

### figma-dev-mode (Design Extraction)
- Command-specific loading
- Parallel call pattern
- Caching strategy
- Best practices from orchestrator

### zeplin (Design Extraction)
- Command-specific loading
- Parallel call pattern
- Icon code conversion
- Best practices from orchestrator

## Decision Tree: Which MCP to Use?

```
Need library documentation?
  └─> context7 (tokens based on phase)

Need design pattern recommendations?
  └─> design-patterns (maxResults: 5)

Have Figma design URL?
  └─> figma-dev-mode (automatic via /figma-to-react)

Have Zeplin design URL?
  └─> zeplin (automatic via /zeplin-to-maui)
```

## Token Budget Reference Table

| MCP Server | Default Tokens | Min | Max | Adjust When |
|------------|----------------|-----|-----|-------------|
| context7 | 5000 | 2000 | 6000 | Phase, complexity, familiarity |
| design-patterns | ~5000 (5 results) | ~1000 (1 result) | ~10000 (10 results) | Number of patterns needed |
| figma-dev-mode | N/A (image-based) | - | - | Not applicable |
| zeplin | N/A (design-based) | - | - | Not applicable |

## Anti-Patterns to Avoid

### ❌ Don't Fetch Unnecessary Documentation
### ❌ Don't Call get_pattern_details for All Patterns
### ❌ Don't Skip Caching
### ❌ Don't Load MCPs Globally
### ❌ Don't Ignore Token Budgets

## Monitoring MCP Usage

- How to measure context window impact
- When to investigate high token usage
- Tools for debugging MCP responses

## Future Enhancements

- Dynamic token budgeting (TASK-012 Priority 2)
- MCP response size monitoring (TASK-012 Priority 2)
- Extended caching for context7/design-patterns

## References

- TASK-012 MCP Usage Audit Report
- task-manager.md (Context7 usage)
- pattern-advisor.md (Design Patterns usage)
- figma-react-orchestrator.md (Figma MCP usage)
- zeplin-maui-orchestrator.md (Zeplin MCP usage)
```

## Implementation Notes

### Approach
1. **Review Existing Documentation**: Read current agent specs to understand context
2. **Add Token Budgets**: Update task-manager.md and pattern-advisor.md in place
3. **Create Optimization Guide**: Write comprehensive new guide
4. **Cross-Reference**: Update CLAUDE.md and agent specs with links
5. **Validate**: Check all links, examples, and token numbers

### Files to Modify
1. `installer/global/agents/task-manager.md` (~30 lines added)
2. `installer/global/agents/pattern-advisor.md` (~40 lines added)
3. `docs/guides/mcp-optimization-guide.md` (~300 lines, new file)
4. `CLAUDE.md` (~10 lines added)

### Style Guidelines
- Use tables for token budgets (easy scanning)
- Use ✅/❌/⚠️ markers for visual clarity
- Include code examples in appropriate language (TypeScript for MCP calls, YAML for config)
- Cross-reference liberally (help navigation)
- Keep examples realistic (from actual agent implementations)

### Potential Issues
- **Line number drift**: Agent specs may be updated, verify line numbers before editing
- **Token number accuracy**: Double-check all token estimates against TASK-012 audit
- **Link validation**: Test all markdown links after creation

## Success Metrics

**Documentation Quality**:
- All token budgets documented with clear rationale
- 3+ examples per MCP server
- Zero broken links
- Consistent formatting throughout

**Developer Experience**:
- New MCP integrations follow checklist (future tasks)
- Developers reference guide when optimizing MCP calls
- Reduced context window bloat in future implementations

**Validation**:
- All acceptance criteria met
- No regression in existing MCP functionality
- Documentation is accurate and up-to-date

## Related Tasks

- **TASK-012**: MCP Usage Audit (parent task, provides recommendations)
- **TASK-013**: CLAUDE.md Optimization (similar documentation focus)
- **TASK-014**: Context7 MCP Integration (referenced in documentation)

## Estimated Effort

**Total**: 1.5 hours

**Breakdown**:
- task-manager.md updates: 20 minutes
- pattern-advisor.md updates: 15 minutes
- mcp-optimization-guide.md creation: 45 minutes
- CLAUDE.md updates: 5 minutes
- Cross-reference validation: 5 minutes

## Next Steps

After task creation:
1. ✅ Task created (this file)
2. ⏸️ Wait for TASK-012 to be marked complete
3. 🔜 `/task-work TASK-032` to implement documentation updates
4. 🔜 `/task-complete TASK-032` to finalize and archive

**Note**: This is a documentation-only task. No code changes required, only markdown file updates.
