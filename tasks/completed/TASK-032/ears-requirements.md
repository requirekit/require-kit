# TASK-032 EARS-Formatted Requirements Quick Reference

---

## Ubiquitous Requirements (Always Active)

### REQ-032-002: Provide Adjustment Guidance for Token Budgets
```
The documentation SHALL provide explicit guidance on when to increase,
maintain, or decrease Context7 token budgets beyond default recommendations.
```

**Priority**: Medium | **Type**: Ubiquitous | **Status**: Draft

---

### REQ-032-003: Document Design Patterns MCP Token Limits
```
The documentation SHALL specify recommended maxResults parameter limits
for Design Patterns MCP operations (find_patterns and get_pattern_details)
with explicit token cost estimates.
```

**Priority**: High | **Type**: Ubiquitous | **Status**: Draft

---

### REQ-032-004: Create Comprehensive Pattern Advisory in pattern-advisor.md
```
The pattern-advisor agent specification SHALL include a dedicated section
explaining token budget management and result limiting with efficiency/anti-pattern
comparisons.
```

**Priority**: High | **Type**: Ubiquitous | **Status**: Draft

---

### REQ-032-005: Create New MCP Optimization Guide File
```
The system SHALL provide a comprehensive MCP Optimization Guide at
`docs/guides/mcp-optimization-guide.md` that consolidates MCP integration
best practices, token budgets, and anti-patterns in a single reference document.
```

**Priority**: High | **Type**: Ubiquitous | **Status**: Draft

---

### REQ-032-006: Implement 8-Point MCP Integration Checklist
```
The MCP Optimization Guide SHALL include an 8-point checklist covering
lazy loading, scoped queries, token limits, caching, retry logic, fail-fast,
parallel calls, and documentation.
```

**Priority**: High | **Type**: Ubiquitous | **Status**: Draft

---

### REQ-032-007: Document MCP Server Reference Section
```
The MCP Optimization Guide SHALL include detailed reference sections for
each of the 4 MCP servers (context7, design-patterns, figma-dev-mode, zeplin)
covering when to use, token budgets, scoping strategies, and best practices.
```

**Priority**: High | **Type**: Ubiquitous | **Status**: Draft

---

### REQ-032-008: Create MCP Selection Decision Tree
```
The MCP Optimization Guide SHALL include a decision tree that guides developers
to the appropriate MCP based on their use case (library documentation, design patterns,
Figma design, or Zeplin design).
```

**Priority**: Medium | **Type**: Ubiquitous | **Status**: Draft

---

### REQ-032-009: Document Token Budget Reference Table
```
The MCP Optimization Guide SHALL include a summary table showing token budgets
for each MCP server with default, minimum, and maximum values, and conditions
for adjustment.
```

**Priority**: High | **Type**: Ubiquitous | **Status**: Draft

---

### REQ-032-010: Document Anti-Patterns to Avoid
```
The MCP Optimization Guide SHALL document anti-patterns with ❌ markers,
explaining what NOT to do when integrating MCPs.
```

**Priority**: Medium | **Type**: Ubiquitous | **Status**: Draft

---

### REQ-032-011: Update CLAUDE.md with MCP Cross-References
```
The CLAUDE.md main documentation file SHALL include a new "MCP Integration
Best Practices" section that summarizes the 4 MCP servers, their optimization
status, and links to the comprehensive MCP Optimization Guide.
```

**Priority**: Medium | **Type**: Ubiquitous | **Status**: Draft

---

### REQ-032-012: Add MCP References to Agent Specifications
```
Agent specification files that use MCPs (task-manager.md, pattern-advisor.md)
SHALL include cross-references or links to relevant sections of the MCP
Optimization Guide.
```

**Priority**: Medium | **Type**: Ubiquitous | **Status**: Draft

---

### REQ-032-013: Ensure Cross-Reference Consistency
```
All cross-references between documentation files (CLAUDE.md, task-manager.md,
pattern-advisor.md, mcp-optimization-guide.md) SHALL use consistent relative paths
and valid markdown link syntax.
```

**Priority**: High | **Type**: Ubiquitous | **Status**: Draft

---

## Event-Driven Requirements

### REQ-032-001: Document Token Budget Guidelines in task-manager.md
```
When a developer implements a library-specific feature using Context7 MCP,
the system documentation SHALL provide clear token budget recommendations
organized by implementation phase (Planning, Implementation, Testing).
```

**Priority**: High | **Type**: Event-Driven | **Status**: Draft

**Trigger**: Developer begins Context7 usage
**Response**: Access clear, phase-appropriate token budget table
**Timing**: Immediate (documentation lookup <5 seconds)

---

## Requirement Mapping Matrix

| ID | EARS Type | Title | Priority | File | Lines | Status |
|---|-----------|-------|----------|------|-------|--------|
| REQ-032-001 | Event-Driven | Context7 Token Budget Guidelines | HIGH | task-manager.md | 30-40 | Draft |
| REQ-032-002 | Ubiquitous | Adjustment Guidance | MEDIUM | task-manager.md | 10-15 | Draft |
| REQ-032-003 | Ubiquitous | Design Patterns Token Limits | HIGH | pattern-advisor.md | 15-20 | Draft |
| REQ-032-004 | Ubiquitous | Pattern Advisory Section | HIGH | pattern-advisor.md | 40-50 | Draft |
| REQ-032-005 | Ubiquitous | New MCP Guide File | HIGH | mcp-optimization-guide.md | 310 | Draft |
| REQ-032-006 | Ubiquitous | 8-Point Checklist | HIGH | mcp-optimization-guide.md | 40 | Draft |
| REQ-032-007 | Ubiquitous | MCP Server Reference | HIGH | mcp-optimization-guide.md | 110 | Draft |
| REQ-032-008 | Ubiquitous | Decision Tree | MEDIUM | mcp-optimization-guide.md | 15 | Draft |
| REQ-032-009 | Ubiquitous | Budget Reference Table | HIGH | mcp-optimization-guide.md | 15 | Draft |
| REQ-032-010 | Ubiquitous | Anti-Patterns | MEDIUM | mcp-optimization-guide.md | 20 | Draft |
| REQ-032-011 | Ubiquitous | CLAUDE.md Integration | MEDIUM | CLAUDE.md | 10-12 | Draft |
| REQ-032-012 | Ubiquitous | Agent Spec Links | MEDIUM | task-manager.md, pattern-advisor.md | 5 | Draft |
| REQ-032-013 | Ubiquitous | Cross-Reference Consistency | HIGH | All files | N/A | Draft |

---

## Requirement Categories

### Category A: Token Budget Documentation (REQ-032-001, REQ-032-002, REQ-032-009)
**Focus**: Clear, phase-appropriate token allocation guidance
**Files**: task-manager.md, mcp-optimization-guide.md
**Lines**: ~55-70 total

### Category B: Design Patterns Guidance (REQ-032-003, REQ-032-004)
**Focus**: Prevent token waste in pattern queries
**Files**: pattern-advisor.md, mcp-optimization-guide.md
**Lines**: ~55-70 total

### Category C: Comprehensive Guide (REQ-032-005, REQ-032-006, REQ-032-007, REQ-032-008, REQ-032-010)
**Focus**: Single source of truth for MCP integration
**Files**: mcp-optimization-guide.md (NEW)
**Lines**: ~200 total

### Category D: Integration & Cross-References (REQ-032-011, REQ-032-012, REQ-032-013)
**Focus**: Discoverability and navigation
**Files**: CLAUDE.md, task-manager.md, pattern-advisor.md, mcp-optimization-guide.md
**Lines**: ~25-30 total

---

## Dependency Map

```
REQ-032-001 (Context7 Budget)
    └─→ REQ-032-002 (Adjustment Guidance)
        └─→ REQ-032-009 (Budget Reference Table)
            └─→ REQ-032-011 (CLAUDE.md Integration)

REQ-032-003 (Design Patterns Limits)
    └─→ REQ-032-004 (Pattern Advisory)
        └─→ REQ-032-010 (Anti-Patterns)
            └─→ REQ-032-012 (Agent Spec Links)

REQ-032-005 (New Guide File)
    ├─→ REQ-032-006 (8-Point Checklist)
    ├─→ REQ-032-007 (MCP Server Reference)
    ├─→ REQ-032-008 (Decision Tree)
    └─→ REQ-032-009 (Budget Reference Table)

REQ-032-013 (Cross-Reference Consistency)
    └─→ APPLIES_TO: REQ-032-011, REQ-032-012
```

---

## Acceptance Criteria Summary

### HIGH Priority Requirements (9 total)
- REQ-032-001: Token budgets by phase
- REQ-032-003: Design Patterns limits
- REQ-032-004: Pattern advisory section
- REQ-032-005: New guide file
- REQ-032-006: 8-point checklist
- REQ-032-007: MCP server reference
- REQ-032-009: Budget table
- REQ-032-011: CLAUDE.md integration
- REQ-032-013: Cross-reference consistency

### MEDIUM Priority Requirements (4 total)
- REQ-032-002: Adjustment guidance
- REQ-032-008: Decision tree
- REQ-032-010: Anti-patterns
- REQ-032-012: Agent spec links

**Distribution**: 69% High, 31% Medium (balanced across both categories)

---

## Context7 Budget Requirements Detail

### REQ-032-001 Acceptance Criteria

**Planning Phase (Phase 2)**:
- [ ] Budget documented: 3000-4000 tokens
- [ ] Rationale: High-level architecture, pattern overview
- [ ] Example: "fastapi dependency injection overview"

**Implementation Phase (Phase 3)**:
- [ ] Budget documented: 5000 tokens (default)
- [ ] Rationale: Detailed API documentation, code examples
- [ ] Example: "fastapi dependency injection detailed examples"

**Testing Phase (Phase 4)**:
- [ ] Budget documented: 2000-3000 tokens
- [ ] Rationale: Framework-specific testing patterns
- [ ] Example: "pytest fixtures and parametrize"

---

## Design Patterns Budget Requirements Detail

### REQ-032-003 & REQ-032-004 Acceptance Criteria

**find_patterns**:
- [ ] Default: 5 results
- [ ] Maximum: 10 results
- [ ] Token cost: ~1000 per pattern summary

**get_pattern_details**:
- [ ] Recommended: Only top 1-2 patterns
- [ ] Token cost: ~3000 per detailed pattern
- [ ] Anti-pattern: Fetching all 10 = ~30k tokens ❌

**Efficient Pattern** (8k total):
- [ ] Step 1: Use find_patterns (5 results, ~5k tokens)
- [ ] Step 2: Analyze top patterns by confidence
- [ ] Step 3: Call get_pattern_details for #1 (~3k tokens)
- [ ] Step 4: If needed, get details for #2 (~3k tokens)

---

## MCP Optimization Guide Requirements Detail

### REQ-032-006: 8-Point Checklist Items

```
1. ✓ Lazy Loading
   - Load MCPs command-specific or phase-specific
   - NOT globally (saves tokens on startup)

2. ✓ Scoped Queries
   - Use topic, filter, category parameters
   - Prevent broad searches that waste tokens

3. ✓ Token Limits
   - Default 5000, adjust per use case
   - Phase 2: 3000-4000 | Phase 3: 5000 | Phase 4: 2000-3000

4. ✓ Caching Implementation
   - Implement 1-hour TTL for static data
   - Prevent redundant MCP calls

5. ✓ Retry Logic
   - 3 attempts with exponential backoff
   - Improve reliability for transient failures

6. ✓ Fail Fast
   - Verify MCP availability in Phase 0
   - Prevent propagating MCP failures

7. ✓ Parallel Calls
   - Use concurrency when querying multiple MCPs
   - Improve response time

8. ✓ Token Budget Documentation
   - Document budget for each MCP call
   - Enable optimization tracking
```

---

## Anti-Patterns Documentation

### REQ-032-010: Five Core Anti-Patterns

```
❌ ANTI-PATTERN 1: Fetch Unnecessary Documentation
   Problem: Request full library docs without topic scoping
   Token Cost: 10000+ tokens
   Correct: Use topic parameter to scope to "dependency-injection"

❌ ANTI-PATTERN 2: Call get_pattern_details for All Patterns
   Problem: Fetch details for all 10 found patterns
   Token Cost: ~30,000 tokens (10 × 3k)
   Correct: Only fetch top 1-2 patterns (~8k tokens)

❌ ANTI-PATTERN 3: Skip Caching
   Problem: Call MCP repeatedly for same data
   Token Cost: Multiple calls with same token cost
   Correct: Implement cache with 1-hour TTL

❌ ANTI-PATTERN 4: Load MCPs Globally
   Problem: Initialize all MCPs on startup
   Token Cost: Baseline tokens consumed upfront
   Correct: Load MCPs command-specific or phase-specific

❌ ANTI-PATTERN 5: Ignore Token Budgets
   Problem: No tracking of token usage per MCP call
   Token Cost: Uncontrolled context window growth
   Correct: Document and monitor budget per call
```

---

## Cross-Reference Structure

### REQ-032-011: CLAUDE.md Integration

**Location**: After "Core AI Agents" section

**Content**:
```markdown
## MCP Integration Best Practices

The system integrates with 4 MCP servers:
- context7: Library documentation
- design-patterns: Pattern recommendations
- figma-dev-mode: Figma design extraction
- zeplin: Zeplin design extraction

Status: ✅ All MCPs optimized (4.5-12% context window usage)

[Link to MCP Optimization Guide]
```

---

### REQ-032-012: Agent Spec Links

**task-manager.md**:
- Add link from Context7 section to mcp-optimization-guide.md
- Text: "See MCP Optimization Guide for detailed Context7 patterns"

**pattern-advisor.md**:
- Add link from Design Patterns section to mcp-optimization-guide.md
- Text: "See MCP Optimization Guide for token budget guidance"

---

### REQ-032-013: Consistency Check

**Link Format Validation**:
- [ ] All links use markdown syntax: `[text](path)`
- [ ] All paths are relative (not absolute URLs)
- [ ] All referenced files exist
- [ ] No circular references
- [ ] Link text is descriptive

**Content Consistency**:
- [ ] Token numbers match across all files
- [ ] Terminology consistent (e.g., "MCP" not "MCP server")
- [ ] Examples follow same style
- [ ] Visual markers used consistently (✅, ❌, ⚠️)

---

## Verification Checklist

### Before Implementation
- [ ] TASK-012 audit report located and reviewed
- [ ] All token budget numbers verified
- [ ] orchestrator files reviewed (if they exist)
- [ ] File paths confirmed accessible
- [ ] Current agent specs read and understood

### During Implementation
- [ ] Each requirement addressed explicitly
- [ ] Examples provided for each MCP
- [ ] Code examples tested for syntax validity
- [ ] Markdown formatting validated
- [ ] Cross-references created and tested

### After Implementation
- [ ] All 13 functional requirements satisfied
- [ ] All 13 test requirements pass
- [ ] All 5 non-functional requirements met
- [ ] All 6 identified gaps resolved
- [ ] Zero broken links
- [ ] Zero formatting inconsistencies
- [ ] Zero token budget discrepancies

---

## Quick Reference: 13 Requirements at a Glance

```
GROUP 1: Context7 Budgets
├─ REQ-032-001: Document by phase (3-4k, 5k, 2-3k tokens)
└─ REQ-032-002: Explain adjustments (complexity, familiarity)

GROUP 2: Design Patterns
├─ REQ-032-003: Limits (find=5 default/10 max, details=1-2 only)
└─ REQ-032-004: Patterns & anti-patterns (8k good, 30k bad)

GROUP 3: New Guide File
├─ REQ-032-005: Create mcp-optimization-guide.md (310 lines)
├─ REQ-032-006: 8-point checklist (lazy, scope, tokens, cache, retry, fail-fast, parallel, docs)
├─ REQ-032-007: 4 MCP server references (context7, design-patterns, figma, zeplin)
├─ REQ-032-008: Decision tree (which MCP to use)
├─ REQ-032-009: Budget reference table
└─ REQ-032-010: Anti-patterns (5 core patterns documented)

GROUP 4: Integration
├─ REQ-032-011: CLAUDE.md section (MCP overview + link)
├─ REQ-032-012: Agent spec links (task-manager, pattern-advisor)
└─ REQ-032-013: Cross-reference consistency (relative paths, valid links)

TOTAL: 13 Requirements (9 High Priority, 4 Medium Priority)
```

---

**EARS Requirements Analysis Complete**
**Status**: Ready for Implementation
**Confidence**: Very High
