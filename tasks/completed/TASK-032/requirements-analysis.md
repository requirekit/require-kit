# TASK-032 Requirements Analysis: MCP Documentation Updates

**Task**: Implement MCP documentation updates from audit recommendations
**Status**: In Progress
**Analysis Date**: 2025-10-25
**Parent Task**: TASK-012 (MCP Usage Audit - Completed)

---

## Executive Summary

TASK-032 is a documentation-only task that implements Priority 1 recommendations from the TASK-012 MCP audit. The audit confirmed all MCPs are already optimized but identified opportunities to document token budgets and best practices more explicitly.

**Scope**: 4 files (3 updates + 1 new file), ~400 lines of documentation
**Complexity**: Low (documentation only, no code changes)
**Risk**: Minimal (documentation updates don't affect runtime behavior)

---

## Current State Analysis

### What We Know
From TASK-032 task file and task-manager.md agent spec:

1. **TASK-012 Status**: ✅ COMPLETED
   - Audit verdict: OPTIMIZED (no code changes needed)
   - Finding: All MCPs use 4.5-12% of context window
   - Recommendations: Document existing best practices

2. **Current Implementation Status**:
   - `task-manager.md`: Has basic Context7 MCP usage section (lines 21-73)
   - `pattern-advisor.md`: Lacks token budget guidance
   - `mcp-optimization-guide.md`: Does NOT exist
   - `CLAUDE.md`: No MCP cross-references

3. **Documentation Gaps Identified**:
   - No explicit token budget tables by phase
   - No Design Patterns MCP guidance (maxResults limits)
   - No consolidated MCP best practices guide
   - No cross-references between related documents

---

## Functional Requirements (EARS Format)

### Requirement Category 1: Context7 Token Budget Documentation

#### REQ-032-001: Document Token Budget Guidelines in task-manager.md
**Type**: Event-Driven
**Priority**: High
**Status**: Draft

**EARS Statement**:
When a developer implements a library-specific feature using Context7 MCP, the system documentation SHALL provide clear token budget recommendations organized by implementation phase (Planning, Implementation, Testing).

**Rationale**:
Developers need explicit guidance on appropriate Context7 token allocation during each phase to optimize context window usage and prevent excessive token consumption.

**Acceptance Criteria**:
- [ ] Token budget table added to task-manager.md with columns: Phase, Budget, Rationale, Example Query
- [ ] Three phase rows documented:
  - Planning (Phase 2): 3000-4000 tokens with rationale
  - Implementation (Phase 3): 5000 tokens (default) with examples
  - Testing (Phase 4): 2000-3000 tokens with specifics
- [ ] "When to adjust token budget" guidance provided
- [ ] At least 2 examples of appropriate queries (marked with ✅)
- [ ] At least 1 example of excessive query (marked with ⚠️)
- [ ] Table is scannable with clear formatting

**Measurable Outcomes**:
- Token budget documentation completes within 20 minutes
- Documentation is 100% accurate (verified against TASK-012 findings)
- Documentation reduces developer questions about Context7 limits

---

#### REQ-032-002: Provide Adjustment Guidance for Token Budgets
**Type**: Ubiquitous
**Priority**: Medium
**Status**: Draft

**EARS Statement**:
The documentation SHALL provide explicit guidance on when to increase, maintain, or decrease Context7 token budgets beyond default recommendations.

**Rationale**:
Default budgets don't fit all scenarios. Developers need decision criteria for adjusting budgets based on task complexity, framework familiarity, and project phase.

**Acceptance Criteria**:
- [ ] Increase scenarios documented (complexity ≥7, unfamiliar framework)
- [ ] Decrease scenarios documented (planning phase, well-known library, specific topic)
- [ ] Special cases noted (testing frameworks need focused docs only)
- [ ] Examples provided for each adjustment scenario
- [ ] Guidance is actionable (not vague)

**Measurable Outcomes**:
- Developers can independently adjust token budgets for their context
- Adjustment decisions are traceable to documented guidance

---

### Requirement Category 2: Design Patterns MCP Guidance

#### REQ-032-003: Document Design Patterns MCP Token Limits
**Type**: Ubiquitous
**Priority**: High
**Status**: Draft

**EARS Statement**:
The documentation SHALL specify recommended maxResults parameter limits for Design Patterns MCP operations (find_patterns and get_pattern_details) with explicit token cost estimates.

**Rationale**:
The Design Patterns MCP can consume significant context if misused (e.g., fetching details for all 10 patterns = ~30k tokens). Developers need clear guidance on efficient usage patterns.

**Acceptance Criteria**:
- [ ] find_patterns limits documented: Default 5 results, maximum 10 results
- [ ] get_pattern_details limits documented: Only for top 1-2 patterns
- [ ] Token cost estimates provided:
  - ~1000 tokens per pattern summary
  - ~3000 tokens per detailed pattern
- [ ] Efficient query pattern explained with steps
- [ ] Anti-pattern section shows ❌ example (fetching all pattern details)
- [ ] Corrected example shows ✅ approach (fetch top 1-2 only)
- [ ] Code examples provided (TypeScript or language-agnostic)

**Measurable Outcomes**:
- Developers follow documented query pattern naturally
- Anti-pattern example prevents common mistakes
- Token consumption for pattern queries stays within budget

---

#### REQ-032-004: Create Comprehensive Pattern Advisory in pattern-advisor.md
**Type**: Ubiquitous
**Priority**: High
**Status**: Draft

**EARS Statement**:
The pattern-advisor agent specification SHALL include a dedicated section explaining token budget management and result limiting with efficiency/anti-pattern comparisons.

**Rationale**:
The pattern-advisor.md file is where developers and agents look for Design Patterns MCP guidance. Integrating token/efficiency guidance directly into this spec ensures consistent usage.

**Acceptance Criteria**:
- [ ] "Token Budget and Result Limiting" section added after find_patterns description
- [ ] Efficiency guidance structured as numbered steps (1. Use find_patterns, 2. Analyze top patterns, 3. Call get_pattern_details only for #1)
- [ ] Anti-pattern section shows inefficient approach with token calculation (10 patterns × 3k = 30k tokens)
- [ ] Corrected pattern shows efficient approach with total estimate (8k tokens)
- [ ] Section is approximately 40-50 lines (balanced detail)
- [ ] Markdown formatting includes code blocks and YAML blocks

**Measurable Outcomes**:
- Pattern-advisor.md becomes comprehensive MCP usage guide
- Developers reference this section when optimizing pattern queries
- Pattern query efficiency improves across team

---

### Requirement Category 3: MCP Optimization Comprehensive Guide

#### REQ-032-005: Create New MCP Optimization Guide File
**Type**: Ubiquitous
**Priority**: High
**Status**: Draft

**EARS Statement**:
The system SHALL provide a comprehensive MCP Optimization Guide at `docs/guides/mcp-optimization-guide.md` that consolidates MCP integration best practices, token budgets, and anti-patterns in a single reference document.

**Rationale**:
Developers need a single, authoritative source for MCP integration best practices. Scattered guidance across multiple agent specs makes it hard to discover and apply optimizations consistently.

**Acceptance Criteria**:
- [ ] File created at correct path: `docs/guides/mcp-optimization-guide.md`
- [ ] Overview section explains what MCPs are and why optimization matters
- [ ] Current optimization status documented (4.5-12% context window usage)
- [ ] Guide purpose clearly stated
- [ ] File is approximately 300 lines of content
- [ ] Markdown formatting is consistent with other guides

**Measurable Outcomes**:
- New guide appears in docs/guides/ directory
- File is valid Markdown with no syntax errors
- File is discoverable and referenced from CLAUDE.md

---

#### REQ-032-006: Implement 8-Point MCP Integration Checklist
**Type**: Ubiquitous
**Priority**: High
**Status**: Draft

**EARS Statement**:
The MCP Optimization Guide SHALL include an 8-point checklist covering lazy loading, scoped queries, token limits, caching, retry logic, fail-fast, parallel calls, and documentation.

**Rationale**:
The checklist provides a concrete reference that future MCP integrations must follow, ensuring consistency and preventing regressions.

**Acceptance Criteria**:
- [ ] 8-point checklist included with all items:
  1. Lazy loading (command-specific or phase-specific)
  2. Scoped queries (topic, filter, category parameters)
  3. Token limits (default 5000, adjust per use case)
  4. Caching implementation (1-hour TTL)
  5. Retry logic (3 attempts, exponential backoff)
  6. Fail fast (verify in Phase 0)
  7. Parallel calls (when possible)
  8. Token budget documentation
- [ ] Each checklist item includes brief explanation (1-2 sentences)
- [ ] Examples provided from existing implementations (Figma, Zeplin, Context7)
- [ ] Each example links to relevant agent file

**Measurable Outcomes**:
- Checklist is clear enough for future developers to follow independently
- Examples are realistic and actionable
- Checklist covers all critical MCP integration aspects

---

#### REQ-032-007: Document MCP Server Reference Section
**Type**: Ubiquitous
**Priority**: High
**Status**: Draft

**EARS Statement**:
The MCP Optimization Guide SHALL include detailed reference sections for each of the 4 MCP servers (context7, design-patterns, figma-dev-mode, zeplin) covering when to use, token budgets, scoping strategies, and best practices.

**Rationale**:
Different MCPs have different characteristics and optimization strategies. Developers need specific guidance for each to make informed decisions.

**Acceptance Criteria**:
- [ ] context7 section documents:
  - When to use (library documentation lookup)
  - Token budgets by phase (table)
  - Scoping with topic parameter
  - Examples (good and bad queries)
- [ ] design-patterns section documents:
  - When to use (pattern recommendations)
  - maxResults guidance (5 default, 10 max)
  - Efficient query patterns (steps 1-4)
  - Anti-patterns (don't fetch all details)
- [ ] figma-dev-mode section documents:
  - When to use (design extraction)
  - Command-specific loading
  - Parallel call pattern
  - Caching strategy
  - Best practices from orchestrator
- [ ] zeplin section documents:
  - When to use (design extraction)
  - Command-specific loading
  - Parallel call pattern
  - Icon code conversion
  - Best practices from orchestrator
- [ ] All 4 sections follow consistent template structure
- [ ] Examples reference actual agent implementations

**Measurable Outcomes**:
- Developers can quickly find guidance for specific MCP
- Reference sections are comprehensive but concise
- All sections are equally detailed and helpful

---

#### REQ-032-008: Create MCP Selection Decision Tree
**Type**: Ubiquitous
**Priority**: Medium
**Status**: Draft

**EARS Statement**:
The MCP Optimization Guide SHALL include a decision tree that guides developers to the appropriate MCP based on their use case (library documentation, design patterns, Figma design, or Zeplin design).

**Rationale**:
Developers new to the system need help selecting which MCP to use for their specific task. A decision tree provides quick, unambiguous guidance.

**Acceptance Criteria**:
- [ ] Decision tree covers all 4 MCPs
- [ ] Each path leads to exactly one MCP
- [ ] Questions are binary or limited options (not open-ended)
- [ ] Tree is ASCII art or clear text format
- [ ] Example: "Need library documentation? → context7"
- [ ] Example: "Need design pattern recommendations? → design-patterns"
- [ ] Example: "Have Figma design URL? → figma-dev-mode"
- [ ] Example: "Have Zeplin design URL? → zeplin"

**Measurable Outcomes**:
- Decision tree is easy to follow
- New developers use tree to select correct MCP
- Tree eliminates confusion about which MCP to use

---

#### REQ-032-009: Document Token Budget Reference Table
**Type**: Ubiquitous
**Priority**: High
**Status**: Draft

**EARS Statement**:
The MCP Optimization Guide SHALL include a summary table showing token budgets for each MCP server with default, minimum, and maximum values, and conditions for adjustment.

**Rationale**:
Developers need a quick reference table for token budgets across all MCPs to make rapid decisions during implementation.

**Acceptance Criteria**:
- [ ] Table includes columns: MCP Server, Default Tokens, Min, Max, Adjust When
- [ ] context7 row: 5000 default | 2000 min | 6000 max | "Phase, complexity, familiarity"
- [ ] design-patterns row: ~5000 (5 results) | ~1000 (1 result) | ~10000 (10 results) | "Number of patterns needed"
- [ ] figma-dev-mode row: "N/A (image-based)" | "-" | "-" | "Not applicable"
- [ ] zeplin row: "N/A (design-based)" | "-" | "-" | "Not applicable"
- [ ] Table is formatted for easy scanning (markdown table)
- [ ] Rationale for each adjustment trigger is clear

**Measurable Outcomes**:
- Developers can quickly reference token budgets
- Table is accurate and complete
- Token budget decisions are made in seconds, not minutes

---

#### REQ-032-010: Document Anti-Patterns to Avoid
**Type**: Ubiquitous
**Priority**: Medium
**Status**: Draft

**EARS Statement**:
The MCP Optimization Guide SHALL document anti-patterns with ❌ markers, explaining what NOT to do when integrating MCPs.

**Rationale**:
Anti-patterns are often more memorable than best practices. Explicitly listing what to avoid helps developers internalize optimization guidance.

**Acceptance Criteria**:
- [ ] At least 5 anti-patterns documented:
  - Don't fetch unnecessary documentation
  - Don't call get_pattern_details for all patterns
  - Don't skip caching
  - Don't load MCPs globally
  - Don't ignore token budgets
- [ ] Each anti-pattern includes:
  - ❌ marker for visual clarity
  - Explanation of why it's wrong
  - Reference to correct pattern
- [ ] Anti-patterns section is approximately 20-30 lines
- [ ] Each entry is 2-3 sentences

**Measurable Outcomes**:
- Developers quickly recognize bad MCP patterns
- Anti-patterns section becomes reference during code review
- Team uses anti-pattern markers consistently

---

### Requirement Category 4: Cross-Reference and Integration

#### REQ-032-011: Update CLAUDE.md with MCP Cross-References
**Type**: Ubiquitous
**Priority**: Medium
**Status**: Draft

**EARS Statement**:
The CLAUDE.md main documentation file SHALL include a new "MCP Integration Best Practices" section that summarizes the 4 MCP servers, their optimization status, and links to the comprehensive MCP Optimization Guide.

**Rationale**:
CLAUDE.md is the primary entry point for developers. Adding MCP cross-references ensures developers discover the optimization guide naturally.

**Acceptance Criteria**:
- [ ] New section titled "MCP Integration Best Practices" added
- [ ] Section location: After "Core AI Agents" section (around line 180)
- [ ] 4 MCPs listed with brief descriptions:
  - context7: Library documentation (automatically retrieved during implementation)
  - design-patterns: Pattern recommendations (Phase 2.5A)
  - figma-dev-mode: Figma design extraction (/figma-to-react)
  - zeplin: Zeplin design extraction (/zeplin-to-maui)
- [ ] Optimization status noted: "✅ All MCPs optimized (4.5-12% context window usage)"
- [ ] Link provided: "For detailed MCP usage guidelines: [MCP Optimization Guide](docs/guides/mcp-optimization-guide.md)"
- [ ] Section is approximately 10 lines

**Measurable Outcomes**:
- CLAUDE.md readers discover MCP optimization guide
- Cross-reference is prominent and easy to find
- Link is valid and resolves correctly

---

#### REQ-032-012: Add MCP References to Agent Specifications
**Type**: Ubiquitous
**Priority**: Medium
**Status**: Draft

**EARS Statement**:
Agent specification files that use MCPs (task-manager.md, pattern-advisor.md) SHALL include cross-references or links to relevant sections of the MCP Optimization Guide.

**Rationale**:
Developers reading agent specs should have easy access to MCP best practices without having to search multiple documents.

**Acceptance Criteria**:
- [ ] task-manager.md: Link added from Context7 section to MCP Optimization Guide
- [ ] task-manager.md: Reference indicates "See MCP Optimization Guide for detailed Context7 patterns"
- [ ] pattern-advisor.md: Link added from Design Patterns MCP section to MCP Optimization Guide
- [ ] pattern-advisor.md: Reference indicates "See MCP Optimization Guide for token budget guidance"
- [ ] All links are markdown format and valid
- [ ] Links use relative paths (e.g., `../../docs/guides/mcp-optimization-guide.md`)

**Measurable Outcomes**:
- Agent files are discoverable entry points to MCP guidance
- Developers don't need to search for cross-references
- Links resolve correctly from all file locations

---

#### REQ-032-013: Ensure Cross-Reference Consistency
**Type**: Ubiquitous
**Priority**: High
**Status**: Draft

**EARS Statement**:
All cross-references between documentation files (CLAUDE.md, task-manager.md, pattern-advisor.md, mcp-optimization-guide.md) SHALL use consistent relative paths and valid markdown link syntax.

**Rationale**:
Broken links create poor developer experience and reduce trust in documentation. Consistency makes maintenance easier.

**Acceptance Criteria**:
- [ ] All markdown links use valid syntax: `[text](path)`
- [ ] All paths are relative (not absolute URLs)
- [ ] All referenced files exist at specified paths
- [ ] Manual link verification completed (test each link)
- [ ] Links work from both parent and sibling directories
- [ ] No circular references detected
- [ ] Link text is descriptive (not just "here" or "click here")

**Measurable Outcomes**:
- Zero broken links in final documentation
- Link validation test passes 100%
- Developers can navigate between documents easily

---

## Non-Functional Requirements

### NFR-032-001: Documentation Clarity and Readability
**Requirement**: Documentation SHALL be clear enough for intermediate developers to understand without external context.

**Acceptance Criteria**:
- Technical terms are defined on first use
- Acronyms expanded on first reference (e.g., "Token Length Optimization (TLO)")
- Sentences are short and declarative (under 20 words)
- Code examples are syntactically valid and copy-pasteable
- Tables are properly formatted with clear headers

**Measurement**:
- Readability test: 3+ developers read sections and report comprehension level
- No questions about basic terminology
- Code examples execute without modification

---

### NFR-032-002: Documentation Accuracy
**Requirement**: All token budget numbers, default values, and recommendations SHALL match TASK-012 audit findings.

**Acceptance Criteria**:
- Context7 budgets: 3000-4000 (Phase 2), 5000 (Phase 3), 2000-3000 (Phase 4)
- Design Patterns defaults: 5 results, 10 max
- Token costs: ~1k per pattern summary, ~3k per detailed pattern
- All numbers verified against TASK-012 audit report
- No contradictions between sections

**Measurement**:
- Audit trail: Compare documentation numbers to TASK-012 findings
- Consistency check: Search for duplicated guidance and verify consistency
- Expert review: TASK-012 author reviews updated documentation

---

### NFR-032-003: Documentation Usability
**Requirement**: Documentation SHALL be organized to support quick lookups and enable developers to find relevant information in under 30 seconds.

**Acceptance Criteria**:
- Consistent heading hierarchy (H1=main, H2=section, H3=subsection)
- Table of contents at top of new guide
- Search-friendly keywords in headings
- Examples immediately follow concepts
- Related sections cross-linked
- Visual markers (✅, ❌, ⚠️) for quick scanning

**Measurement**:
- Time test: Measure time for developers to find specific guidance
- Discoverability test: Can developers find relevant sections from different entry points?
- Usability test: 3+ developers navigate guide and report ease of use

---

### NFR-032-004: Documentation Formatting Consistency
**Requirement**: All documentation SHALL follow consistent markdown formatting, style, and structure across all files.

**Acceptance Criteria**:
- Consistent header levels and naming conventions
- Consistent code block syntax highlighting (```typescript, ```yaml, etc.)
- Consistent table formatting
- Consistent example formatting (✅ GOOD, ❌ BAD, ⚠️ WARNING)
- Consistent link formatting (markdown links, not HTML)
- Consistent line wrapping (80 characters recommended)

**Measurement**:
- Automated markdown linting (markdownlint or similar)
- Manual review for style consistency
- Zero formatting errors or inconsistencies

---

### NFR-032-005: Documentation Completeness
**Requirement**: Documentation SHALL comprehensively cover all aspects of MCP integration without gaps or ambiguities.

**Acceptance Criteria**:
- All 4 MCP servers documented with equal depth
- All 8 checklist items explained clearly
- Token budgets provided for all scenarios
- Examples provided for all major use cases
- Anti-patterns documented for all MCPs
- No "to be completed later" placeholders

**Measurement**:
- Completeness checklist from acceptance criteria
- Section length analysis (no orphaned sections)
- Example coverage (at least 2 examples per MCP)

---

## Test Requirements (Validation Checklist)

### Documentation Quality Tests

**TEST-032-001: Token Budget Accuracy**
- [ ] Context7 budgets match TASK-012 audit findings exactly
- [ ] Design Patterns token costs verified (1k per summary, 3k per detail)
- [ ] Examples show correct token calculations
- [ ] All numbers are consistent across all 4 files

**TEST-032-002: Cross-Reference Validation**
- [ ] All markdown links resolve correctly
- [ ] Links use relative paths from all file locations
- [ ] No circular references detected
- [ ] Links from CLAUDE.md, agent specs, and new guide all work

**TEST-032-003: Example Validity**
- [ ] Code examples are syntactically valid
- [ ] Examples can be copy-pasted without modification
- [ ] Examples reference real APIs and libraries
- [ ] Query examples use actual library/service names

**TEST-032-004: Markdown Formatting**
- [ ] All files pass markdown syntax validation
- [ ] Tables render correctly in markdown
- [ ] Code blocks have proper syntax highlighting
- [ ] No unclosed tags or brackets

**TEST-032-005: Content Consistency**
- [ ] Token budget numbers consistent across files
- [ ] Terminology consistent throughout
- [ ] Examples follow consistent style
- [ ] Visual markers (✅, ❌, ⚠️) used consistently

### Completeness Tests

**TEST-032-006: Checklist Coverage**
- [ ] All 8 checklist items present and explained
- [ ] Each checklist item has practical explanation
- [ ] Examples provided for at least 6 of 8 items
- [ ] Examples reference actual agent implementations

**TEST-032-007: MCP Server Coverage**
- [ ] All 4 MCPs documented with equal detail
- [ ] Each MCP has "when to use" section
- [ ] Each MCP has token budget or resource guidance
- [ ] Each MCP has best practices documented

**TEST-032-008: Phase Coverage**
- [ ] Planning phase (Phase 2) guidance documented
- [ ] Implementation phase (Phase 3) guidance documented
- [ ] Testing phase (Phase 4) guidance documented
- [ ] Adjustment criteria clear for each phase

### Usability Tests

**TEST-032-009: Developer Navigation**
- [ ] Developers can find token budgets in under 30 seconds
- [ ] Developers can find anti-patterns in under 30 seconds
- [ ] Developers can find MCP selection guidance in under 30 seconds
- [ ] Index/table of contents is clear and complete

**TEST-032-010: Example Discoverability**
- [ ] Good examples (✅) are easy to spot
- [ ] Bad examples (❌) are clearly marked
- [ ] Examples appear immediately after concepts
- [ ] Examples are copy-pasteable

### Accuracy Tests

**TEST-032-011: File Path Validation**
- [ ] task-manager.md path correct: installer/global/agents/task-manager.md
- [ ] pattern-advisor.md path correct: installer/global/agents/pattern-advisor.md
- [ ] New guide path correct: docs/guides/mcp-optimization-guide.md
- [ ] CLAUDE.md path correct: CLAUDE.md (repo root)

**TEST-032-012: Context7 Accuracy**
- [ ] Phase 2 budget: 3000-4000 tokens documented
- [ ] Phase 3 budget: 5000 tokens (default) documented
- [ ] Phase 4 budget: 2000-3000 tokens documented
- [ ] Adjustment criteria match TASK-012 findings

**TEST-032-013: Design Patterns Accuracy**
- [ ] find_patterns default: 5 results documented
- [ ] find_patterns maximum: 10 results documented
- [ ] get_pattern_details guidance: top 1-2 patterns only
- [ ] Token cost: ~1k per summary, ~3k per detail

---

## Identified Gaps and Ambiguities

### Gap 1: TASK-012 Audit Report Location
**Issue**: Task file references `tasks/in_review/TASK-012-MCP-AUDIT-REPORT.md` but this file was not located.
**Impact**: Token budget numbers in TASK-032 are documented without reference to source audit.
**Mitigation**:
- [ ] Locate or confirm TASK-012 audit report location
- [ ] Verify all token budget numbers against actual audit findings
- [ ] Document audit report location in new guide

**Recommendation**: Add "References" section to mcp-optimization-guide.md linking to TASK-012 audit report.

---

### Gap 2: Figma and Zeplin MCP Optimization Details
**Issue**: Task outline references "best practices from orchestrator" but orchestrator files not reviewed.
**Impact**: May miss actual implementation details from figma-react-orchestrator and zeplin-maui-orchestrator.
**Mitigation**:
- [ ] Read figma-react-orchestrator.md (if exists) before writing Figma section
- [ ] Read zeplin-maui-orchestrator.md (if exists) before writing Zeplin section
- [ ] Extract actual patterns used (lazy loading, parallel calls, caching)

**Recommendation**: Create subtask to review orchestrator files before finalizing guide.

---

### Gap 3: Caching Implementation Details
**Issue**: Checklist item #4 mentions "1-hour TTL for static data" but no implementation examples provided.
**Impact**: Developers may not understand how to implement caching.
**Mitigation**:
- [ ] Provide pseudocode example of caching implementation
- [ ] Reference standard caching libraries/patterns
- [ ] Include TTL justification explanation

**Recommendation**: Add "Caching Implementation Example" section showing pseudo-code pattern.

---

### Gap 4: Anti-Pattern Examples Clarity
**Issue**: Task shows list of anti-patterns but no detailed explanations in actual documentation format.
**Impact**: Anti-patterns may be too abstract without concrete context.
**Mitigation**:
- [ ] Provide code example for each anti-pattern (even if pseudocode)
- [ ] Show token cost impact (how many tokens wasted?)
- [ ] Compare to correct pattern side-by-side

**Recommendation**: Anti-patterns section should include code-based examples, not just text descriptions.

---

### Gap 5: Future Enhancements Section
**Issue**: Task outline mentions Priority 2 recommendations but no guidance on how to document them.
**Impact**: May blur scope between Priority 1 (this task) and Priority 2 (future tasks).
**Mitigation**:
- [ ] "Future Enhancements" section should be marked as "TASK-012 Priority 2" references
- [ ] Don't implement Priority 2 features (out of scope)
- [ ] Only reference them as future work

**Recommendation**: Create explicit "Future Work (TASK-012 Priority 2)" section to keep scope clear.

---

### Gap 6: Developer Skill Level Assumptions
**Issue**: Documentation doesn't specify target developer experience level (junior, senior, specialized).
**Impact**: Documentation may be too basic for seniors or too advanced for juniors.
**Mitigation**:
- [ ] Target audience: Intermediate developers (1+ year experience)
- [ ] Assume familiarity with MCPs and APIs
- [ ] Explain only MCP-specific concepts, not general software engineering
- [ ] Provide stack-specific examples (Python, TypeScript, .NET)

**Recommendation**: Add "Audience" statement at top of mcp-optimization-guide.md.

---

## Interdependencies and Traceability

### Related Requirements
- **TASK-012**: MCP Usage Audit (parent task, provides token budget data)
- **TASK-013**: CLAUDE.md Optimization (related documentation focus)
- **TASK-014**: Context7 MCP Integration (implementation that follows this guidance)

### Downstream Dependencies
Future MCP integrations will:
- Reference mcp-optimization-guide.md during design phase
- Follow 8-point checklist during implementation
- Use token budgets from guide for Phase 2.7 complexity evaluation

### File Dependencies
```
CLAUDE.md (references)
├── docs/guides/mcp-optimization-guide.md (new)
│   └── (references)
│       ├── installer/global/agents/task-manager.md
│       ├── installer/global/agents/pattern-advisor.md
│       ├── figma-react-orchestrator.md (if exists)
│       └── zeplin-maui-orchestrator.md (if exists)
├── installer/global/agents/task-manager.md
│   └── (references)
│       └── docs/guides/mcp-optimization-guide.md
└── installer/global/agents/pattern-advisor.md
    └── (references)
        └── docs/guides/mcp-optimization-guide.md
```

---

## Quality Metrics and Success Criteria

### Quantitative Metrics
- **File count**: 4 files (3 updates + 1 new)
- **Lines added**: ~400 total lines of documentation
- **Cross-references**: Minimum 5 links between files
- **Examples provided**: Minimum 8 examples across all files
- **Anti-patterns documented**: Minimum 5 anti-patterns
- **Token budget entries**: Minimum 4 MCPs with budgets

### Qualitative Metrics
- **Clarity**: 3+ developers understand guidance without clarification
- **Accuracy**: 100% match with TASK-012 audit findings
- **Completeness**: All acceptance criteria from task file met
- **Usability**: Developers can find answers in under 30 seconds
- **Consistency**: Zero formatting inconsistencies or contradictions

### Success Definition
**TASK-032 is complete when**:
1. All 13 requirements (REQ-032-001 through REQ-032-013) are fully satisfied
2. All 13 test requirements pass (TEST-032-001 through TEST-032-013)
3. All 5 non-functional requirements met (NFR-032-001 through NFR-032-005)
4. All identified gaps and ambiguities are resolved
5. Documentation is accurate, complete, clear, and usable
6. All cross-references are valid and working

---

## Implementation Recommendations

### Phase 1: Preparation (5-10 minutes)
1. Locate and review TASK-012 audit report to verify token budget numbers
2. Review figma-react-orchestrator.md and zeplin-maui-orchestrator.md (if exist)
3. Confirm file paths are correct and accessible
4. Gather all token budget values and create master list

### Phase 2: Context7 Documentation (15-20 minutes)
1. Update task-manager.md with token budget table
2. Add "When to adjust" guidance section
3. Provide examples of appropriate vs. excessive queries
4. Cross-reference to new mcp-optimization-guide.md

### Phase 3: Pattern Advisor Documentation (10-15 minutes)
1. Add "Token Budget and Result Limiting" section to pattern-advisor.md
2. Provide efficient query pattern steps
3. Include anti-pattern with token calculation
4. Include corrected pattern with efficiency estimate

### Phase 4: New MCP Optimization Guide (40-50 minutes)
1. Create mcp-optimization-guide.md with outline
2. Write overview section (why MCPs matter, optimization status)
3. Implement 8-point checklist with examples
4. Write 4 MCP server reference sections
5. Create decision tree for MCP selection
6. Add token budget reference table
7. Document anti-patterns with explanations
8. Add monitoring and future enhancements sections

### Phase 5: CLAUDE.md Integration (5 minutes)
1. Add "MCP Integration Best Practices" section
2. Summarize the 4 MCPs with links
3. Add reference to mcp-optimization-guide.md
4. Verify link formatting and accuracy

### Phase 6: Cross-Reference Validation (10 minutes)
1. Test all markdown links in all files
2. Verify relative paths work from different directories
3. Check for broken references
4. Validate consistency of token budget numbers
5. Confirm examples are copy-pasteable

### Phase 7: Final Validation (5-10 minutes)
1. Run markdown linting on all files
2. Manual review for grammar and clarity
3. Verify formatting consistency
4. Confirm all acceptance criteria met
5. Sign off on completion

**Estimated Total Time**: 90-130 minutes (1.5-2.2 hours)
**Task Effort Estimate**: 1.5 hours (matches task file)

---

## Sign-Off Checklist

- [ ] All 13 functional requirements fully specified in EARS format
- [ ] All 5 non-functional requirements documented
- [ ] All 13 test requirements defined and testable
- [ ] All gaps and ambiguities identified and documented
- [ ] Implementation recommendations clear and actionable
- [ ] Success criteria defined and measurable
- [ ] Traceability chain established (TASK-012 → TASK-032 → future tasks)

**Requirements Analysis Completed By**: AI Requirements Specialist
**Analysis Status**: READY FOR IMPLEMENTATION
**Confidence Level**: HIGH (task is well-defined, straightforward, low-risk)

---

## Appendix A: File Modification Summary

### File 1: installer/global/agents/task-manager.md
**Change Type**: Addition
**Location**: After line 73 (end of Context7 MCP Usage section)
**Lines Added**: ~30-40 lines
**Content**:
- Context7 Token Budget Guidelines table
- When to adjust token budget section
- Adjustment rationale and examples

### File 2: installer/global/agents/pattern-advisor.md
**Change Type**: Addition
**Location**: After line 109 (in find_patterns section)
**Lines Added**: ~40-50 lines
**Content**:
- Token Budget and Result Limiting section
- Recommended limits for find_patterns and get_pattern_details
- Efficient query pattern with numbered steps
- Anti-pattern example with token calculation
- Corrected pattern example

### File 3: docs/guides/mcp-optimization-guide.md
**Change Type**: New File
**Sections**:
1. Overview (20 lines)
2. 8-Point Integration Checklist (40 lines)
3. MCP Server Reference - context7 (30 lines)
4. MCP Server Reference - design-patterns (30 lines)
5. MCP Server Reference - figma-dev-mode (25 lines)
6. MCP Server Reference - zeplin (25 lines)
7. Decision Tree (15 lines)
8. Token Budget Reference Table (15 lines)
9. Anti-Patterns (20 lines)
10. Monitoring MCP Usage (15 lines)
11. Future Enhancements (10 lines)
12. References (5 lines)
**Total Lines**: ~310 lines

### File 4: CLAUDE.md
**Change Type**: Addition
**Location**: After "Core AI Agents" section (around line 180)
**Lines Added**: ~10-12 lines
**Content**:
- MCP Integration Best Practices section
- Summary of 4 MCPs with descriptions
- Optimization status notation
- Link to mcp-optimization-guide.md

---

## Appendix B: Token Budget Numbers (Source: TASK-012)

**Context7**:
- Phase 2 (Planning): 3000-4000 tokens
- Phase 3 (Implementation): 5000 tokens (default)
- Phase 4 (Testing): 2000-3000 tokens

**Design Patterns**:
- find_patterns: Default 5 results (~5k tokens), Max 10 results (~10k tokens)
- get_pattern_details: Top 1-2 patterns only (~3k tokens per pattern)
- Anti-pattern: Fetching all 10 patterns = ~30k tokens ❌

**Figma/Zeplin**:
- Image-based, token costs not directly applicable
- Context consumption depends on design complexity

**Current System Usage**: 4.5-12% of context window (optimized)

---

## Appendix C: 8-Point MCP Integration Checklist

1. **Lazy Loading**: Load MCPs command-specific or phase-specific (not globally)
2. **Scoped Queries**: Use topic, filter, category parameters to limit results
3. **Token Limits**: Default 5000, adjust per use case based on phase/complexity
4. **Caching Implementation**: Implement 1-hour TTL for static data
5. **Retry Logic**: 3 attempts with exponential backoff on failures
6. **Fail Fast**: Verify MCP availability in Phase 0 before proceeding
7. **Parallel Calls**: Use concurrency when querying multiple MCPs
8. **Token Budget Documentation**: Explicitly document budget for each MCP call

---

**End of TASK-032 Requirements Analysis**
