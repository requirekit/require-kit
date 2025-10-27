# TASK-032 Implementation Roadmap

**Task**: Implement MCP documentation updates from audit recommendations
**Status**: Requirements Analysis Complete
**Next Phase**: Ready for `/task-work TASK-032` Execution

---

## Phase 1: Preparation (5-10 minutes)

### 1.1 Verify Token Budget Numbers
**Objective**: Ensure all token numbers match TASK-012 audit findings

**Actions**:
1. Locate TASK-012 MCP audit report
2. Extract Context7 budgets: 3000-4000 (Phase 2), 5000 (Phase 3), 2000-3000 (Phase 4)
3. Extract Design Patterns costs: ~1k per summary, ~3k per detail
4. Verify current system usage: 4.5-12% context window
5. Document source in mcp-optimization-guide.md References section

**Deliverable**: Verified token budget master list

---

### 1.2 Review Orchestrator Implementations
**Objective**: Extract actual best practices from figma and zeplin orchestrators

**Files to Review**:
- [ ] `installer/global/agents/figma-react-orchestrator.md` (if exists)
- [ ] `installer/global/agents/zeplin-maui-orchestrator.md` (if exists)

**Information to Extract**:
- Lazy loading patterns (command-specific loading)
- Parallel call patterns (concurrent MCP invocations)
- Caching strategies (what gets cached, TTL values)
- Error handling patterns (retry logic, fail-fast)
- Best practices unique to each orchestrator

**Deliverable**: Extracted patterns documented for use in guide

---

### 1.3 Confirm File Paths
**Objective**: Verify all file paths are correct and accessible

**Files to Verify**:
- [ ] `installer/global/agents/task-manager.md` (existing)
- [ ] `installer/global/agents/pattern-advisor.md` (existing)
- [ ] `docs/guides/mcp-optimization-guide.md` (will create)
- [ ] `CLAUDE.md` (existing, at repo root)

**Actions**:
1. Verify each file exists at specified path
2. Read current content to understand structure
3. Identify insertion points for new content
4. Note current line counts for reference

**Deliverable**: File preparation checklist completed

---

## Phase 2: Context7 Documentation (15-20 minutes)

### 2.1 Update task-manager.md
**Objective**: Add Context7 Token Budget Guidelines section

**Location**: After line 73 (end of current Context7 MCP Usage section)

**Content to Add** (~30-40 lines):

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

**Acceptance Criteria**:
- [ ] Table inserted at correct location
- [ ] All three phases documented
- [ ] Examples show good, good, and excessive patterns
- [ ] Adjustment guidance provided
- [ ] Markdown formatting is correct

---

### 2.2 Verify Cross-References
**Objective**: Ensure task-manager.md links to mcp-optimization-guide.md

**Content to Add**:
At end of Context7 section, add:
```markdown
**See also**: [MCP Optimization Guide - Context7 Section](../../docs/guides/mcp-optimization-guide.md#context7-library-documentation)
```

**Acceptance Criteria**:
- [ ] Link syntax is valid markdown
- [ ] Path is relative from agent location
- [ ] Link text is descriptive

---

## Phase 3: Pattern Advisor Documentation (10-15 minutes)

### 3.1 Update pattern-advisor.md
**Objective**: Add Token Budget and Result Limiting section

**Location**: After line 109 (after find_patterns tool description)

**Content to Add** (~40-50 lines):

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

**Acceptance Criteria**:
- [ ] YAML syntax is valid
- [ ] Efficient pattern includes 4 numbered steps
- [ ] Anti-pattern shows ❌ marker and explains the problem
- [ ] Corrected pattern shows ✅ marker and calculates total tokens
- [ ] Code examples are syntactically valid TypeScript

---

### 3.2 Add Cross-Reference
**Objective**: Link to mcp-optimization-guide.md

**Content to Add**:
```markdown
**See also**: [MCP Optimization Guide - Design Patterns Section](../../docs/guides/mcp-optimization-guide.md#design-patterns-pattern-recommendations)
```

---

## Phase 4: New MCP Optimization Guide (40-50 minutes)

### 4.1 Create File Structure
**Objective**: Create mcp-optimization-guide.md with complete outline

**File Path**: `docs/guides/mcp-optimization-guide.md`

**Total Size**: ~310 lines

**Section Breakdown**:

#### 4.1.1 Overview (20 lines)
```markdown
# MCP Optimization Guide

## Overview

### What are MCPs?
Model Context Protocol (MCP) servers extend the system with specialized capabilities:
- **context7**: Real-time library documentation retrieval
- **design-patterns**: Design pattern recommendations
- **figma-dev-mode**: Figma design system extraction
- **zeplin**: Zeplin design system extraction

### Why Optimize MCPs?

MCPs consume context window tokens. Unoptimized usage can:
- ❌ Reduce available context for implementation code
- ❌ Slow down response times
- ❌ Increase costs (in token-based systems)

### Current Status

✅ **All MCPs are optimized** (4.5-12% context window usage)
Result from TASK-012 MCP Usage Audit - no code changes needed

### Purpose of This Guide

This guide documents:
1. Best practices for each MCP
2. Token budgets for responsible usage
3. Anti-patterns to avoid
4. 8-point integration checklist for new implementations
```

---

#### 4.1.2 8-Point Integration Checklist (40 lines)
```markdown
## 8-Point MCP Integration Checklist

Use this checklist when integrating any new MCP or optimizing existing usage:

### 1. Lazy Loading
**What**: Load MCPs only when needed
**Why**: Saves startup tokens and reduces baseline consumption
**How**: Load in command-specific handlers or phase-specific agents
**Examples**:
- Load context7 only in Phase 3 (implementation)
- Load design-patterns only in Phase 2.5A (pattern suggestion)
- Load figma-dev-mode only in /figma-to-react command

---

### 2. Scoped Queries
**What**: Use topic/filter/category parameters to limit results
**Why**: Prevents broad searches that return irrelevant results
**How**: Always use filtering parameters
**Examples**:
- `context7`: Use `topic="dependency-injection"` instead of no topic
- `design-patterns`: Use `category="Resilience"` to focus results
- `figma-dev-mode`: Query specific components, not entire design

---

### 3. Token Limits
**What**: Set appropriate token budgets based on phase/complexity
**Why**: Controls context window consumption
**How**: Use defaults, adjust for phase
**Defaults**:
- Phase 2 (Planning): 3000-4000 tokens
- Phase 3 (Implementation): 5000 tokens
- Phase 4 (Testing): 2000-3000 tokens

---

### 4. Caching Implementation
**What**: Cache MCP responses to prevent redundant calls
**Why**: Reduces duplicate token consumption
**How**: Implement cache with appropriate TTL
**Pattern**:
- Key: Query parameters (library, topic, etc.)
- Value: MCP response
- TTL: 1 hour for static data (library docs), 5 min for dynamic (patterns)

---

### 5. Retry Logic
**What**: Implement exponential backoff for transient failures
**Why**: Improves reliability without tight coupling to MCP availability
**How**: Use standard retry pattern
**Implementation**:
- Max 3 attempts
- Backoff: 100ms, 200ms, 400ms
- Jitter: Add random component to prevent thundering herd

---

### 6. Fail Fast
**What**: Verify MCP availability before proceeding
**Why**: Prevents error propagation and wasted tokens
**How**: Health check in Phase 0
**Examples**:
- Verify context7 has target library (resolve-library-id)
- Verify design-patterns server responds to test query

---

### 7. Parallel Calls
**What**: Use concurrency when querying multiple MCPs
**Why**: Improves response time and resource utilization
**How**: Use async/await or concurrent patterns
**Examples**:
- Fetch context7 docs AND design-patterns simultaneously
- Load multiple pattern details in parallel

---

### 8. Token Budget Documentation
**What**: Document token budget for each MCP call
**Why**: Enables optimization tracking and prevents regression
**How**: Comment in code with budget rationale
**Example**:
```python
# Context7 query: Planning phase (Phase 2), scoped to dependency injection
# Token budget: 3500 tokens (3000-4000 range)
docs = context7.get_library_docs(
    library="/tiangolo/fastapi",
    topic="dependency-injection",
    tokens=3500
)
```
```

---

#### 4.1.3 MCP Server Reference Sections (110 lines)

**context7 (Library Documentation)**
- When to use: Implementation needs specific library API
- Token budgets by phase (3-4k, 5k, 2-3k)
- Scoping strategy (topic parameter)
- 3+ examples (good and bad)

**design-patterns (Pattern Recommendations)**
- When to use: Need architecture pattern guidance
- maxResults limits (5 default, 10 max)
- get_pattern_details limits (1-2 only)
- 3+ examples with token costs

**figma-dev-mode (Design Extraction)**
- When to use: Converting Figma designs to code
- Command-specific loading (only in /figma-to-react)
- Parallel call pattern
- Caching strategy (components, tokens)
- Best practices from orchestrator

**zeplin (Design Extraction)**
- When to use: Converting Zeplin designs to code
- Command-specific loading (only in /zeplin-to-maui)
- Parallel call pattern
- Icon code conversion
- Best practices from orchestrator

---

#### 4.1.4 Decision Tree (15 lines)
```markdown
## Which MCP Should I Use?

```
┌─ Need library documentation (API, examples)?
│  └─→ Use **context7**
│     - Token budget: 3-6k (phase-dependent)
│     - When: Implementing with unfamiliar library
│
├─ Need design pattern guidance?
│  └─→ Use **design-patterns**
│     - Token budget: 5-10k (5-10 patterns)
│     - When: Phase 2.5A (architecture planning)
│
├─ Converting Figma design to React?
│  └─→ Use **figma-dev-mode**
│     - Automatic via `/figma-to-react` command
│     - When: Have Figma design file
│
└─ Converting Zeplin design to MAUI?
   └─→ Use **zeplin**
      - Automatic via `/zeplin-to-maui` command
      - When: Have Zeplin design file
```
```

---

#### 4.1.5 Token Budget Reference Table (15 lines)
```markdown
## Token Budget Reference Table

| MCP Server | Default Tokens | Min | Max | When to Adjust |
|------------|----------------|-----|-----|-----------------|
| **context7** | 5000 | 2000 | 6000 | Phase, complexity, familiarity |
| **design-patterns** | ~5000 (5 results) | ~1000 (1 result) | ~10000 (10 results) | Number of patterns needed |
| **figma-dev-mode** | N/A (image-based) | - | - | Not applicable |
| **zeplin** | N/A (design-based) | - | - | Not applicable |

**Adjustment Rules**:
- **Increase**: High complexity (≥7), unfamiliar framework, new patterns needed
- **Decrease**: Planning phase only, well-known library, testing phase
- **Use defaults**: When in doubt, use default for your phase
```

---

#### 4.1.6 Anti-Patterns to Avoid (20 lines)
```markdown
## Anti-Patterns to Avoid

### ❌ Don't Fetch Unnecessary Documentation
**Problem**: Request full library docs without topic scoping
**Token Cost**: 10,000+ tokens wasted
**Correct**: Use `topic="dependency-injection"` to scope query
**Reference**: Task-manager.md Context7 section

---

### ❌ Don't Call get_pattern_details for All Patterns
**Problem**: Fetch details for all 10 found patterns
**Token Cost**: ~30,000 tokens (10 × 3k) vs 8k optimal
**Correct**: Only fetch top 1-2 patterns by confidence score
**Reference**: Pattern-advisor.md Token Budget section

---

### ❌ Don't Skip Caching
**Problem**: Call MCP repeatedly for same data
**Token Cost**: Multiple calls with same cost (no reduction)
**Correct**: Implement cache with 1-hour TTL
**Reference**: 8-Point Checklist item #4

---

### ❌ Don't Load MCPs Globally
**Problem**: Initialize all MCPs on startup
**Token Cost**: Baseline tokens consumed even when MCPs not needed
**Correct**: Load MCPs command-specific or phase-specific
**Reference**: 8-Point Checklist item #1

---

### ❌ Don't Ignore Token Budgets
**Problem**: No tracking of token usage per MCP call
**Token Cost**: Uncontrolled context window growth
**Correct**: Document and monitor budget per call
**Reference**: 8-Point Checklist item #8
```

---

#### 4.1.7 Monitoring and Future Work (25 lines)
```markdown
## Monitoring MCP Usage

### How to Measure Impact
1. Track token consumption per MCP call
2. Log query parameters (library, topic, maxResults)
3. Log response time and token cost
4. Aggregate by phase and MCP server

### When to Investigate
- Token cost exceeds documented budget by >20%
- Response time exceeds expected threshold
- Query returns >100 results unexpectedly
- Cache miss rate >50%

### Tools for Debugging
- MCP logs (token cost per call)
- Agent logs (query parameters)
- Performance metrics (response time)
- Dashboard (token usage trend)

---

## Future Enhancements (TASK-012 Priority 2)

### Dynamic Token Budgeting
Automatically adjust budgets based on:
- Task complexity (score 1-10)
- Developer skill level
- Project maturity
- Token availability

### MCP Response Size Monitoring
Track and alert on:
- Response size (bytes)
- Pattern count (design-patterns)
- Documentation size (context7)

### Extended Caching
Implement multi-tier caching:
- Local memory (5 min TTL)
- Shared Redis (1 hour TTL)
- Persistent disk (24 hour TTL)

---

## References

- **TASK-012 MCP Usage Audit Report**: [Link to audit findings]
- **task-manager.md**: Context7 token budget guidelines
- **pattern-advisor.md**: Design Patterns MCP usage
- **figma-react-orchestrator.md**: Figma MCP best practices
- **zeplin-maui-orchestrator.md**: Zeplin MCP best practices
```

---

### 4.2 Validation Steps

**Checklist**:
- [ ] File created at `docs/guides/mcp-optimization-guide.md`
- [ ] All 12 sections included
- [ ] Total file size ~310 lines
- [ ] All markdown formatting valid
- [ ] All code examples syntactically correct
- [ ] Table formatting renders properly
- [ ] Visual markers (✅, ❌) used consistently

---

## Phase 5: CLAUDE.md Integration (5 minutes)

### 5.1 Add MCP Integration Best Practices Section

**Location**: After "Core AI Agents" section (around line 326 in current file)

**Content to Add** (~12 lines):

```markdown
## MCP Integration Best Practices

The system integrates with 4 specialized MCP servers:

- **context7**: Retrieves up-to-date library documentation (Phase 3 implementation)
- **design-patterns**: Recommends architectural patterns (Phase 2.5A)
- **figma-dev-mode**: Extracts Figma design systems (automatic in /figma-to-react)
- **zeplin**: Extracts Zeplin design systems (automatic in /zeplin-to-maui)

**Optimization Status**: ✅ All MCPs optimized (4.5-12% context window usage)

**For detailed MCP usage guidelines and best practices**:
See [MCP Optimization Guide](docs/guides/mcp-optimization-guide.md)
```

**Acceptance Criteria**:
- [ ] Section inserted after Core AI Agents
- [ ] All 4 MCPs listed with brief descriptions
- [ ] Optimization status noted
- [ ] Link to new guide provided
- [ ] Markdown formatting correct

---

## Phase 6: Cross-Reference Validation (10 minutes)

### 6.1 Test All Links

**Links to Verify**:

1. **CLAUDE.md** → `docs/guides/mcp-optimization-guide.md`
   - [ ] Link syntax valid: `[text](path)`
   - [ ] Path resolves from CLAUDE.md location
   - [ ] File exists at target path

2. **task-manager.md** → `docs/guides/mcp-optimization-guide.md` (new link)
   - [ ] Path correct: `../../docs/guides/mcp-optimization-guide.md`
   - [ ] Link text descriptive
   - [ ] Target section exists

3. **pattern-advisor.md** → `docs/guides/mcp-optimization-guide.md` (new link)
   - [ ] Path correct: `../../docs/guides/mcp-optimization-guide.md`
   - [ ] Link text descriptive
   - [ ] Target section exists

4. **mcp-optimization-guide.md** → External references
   - [ ] TASK-012 audit report reference (placeholder if needed)
   - [ ] agent file references
   - [ ] All paths relative

---

### 6.2 Verify Content Consistency

**Token Budget Numbers**:
- [ ] Context7 Phase 2: 3000-4000 (all files)
- [ ] Context7 Phase 3: 5000 (all files)
- [ ] Context7 Phase 4: 2000-3000 (all files)
- [ ] Design Patterns default: 5 results (all files)
- [ ] Design Patterns max: 10 results (all files)
- [ ] Pattern detail cost: ~3k tokens (all files)

**Terminology**:
- [ ] "MCP" used consistently (not "MCP server", "MCP tool", etc.)
- [ ] "Token budget" vs "token limit" usage consistent
- [ ] "Context window" used consistently

**Visual Markers**:
- [ ] ✅ used for good patterns
- [ ] ❌ used for anti-patterns
- [ ] ⚠️ used for warnings
- [ ] Consistent across all files

---

## Phase 7: Final Validation (5-10 minutes)

### 7.1 Markdown Linting

**Tools to Use**:
- `markdownlint` (if available)
- Or manual check for:
  - Unclosed code blocks
  - Invalid table formatting
  - Inconsistent heading levels
  - Broken HTML entities

---

### 7.2 Content Quality Review

**Checklist**:
- [ ] No typos or grammatical errors
- [ ] No overly long paragraphs (keep under 3 sentences)
- [ ] No jargon without definition
- [ ] Examples are realistic and correct
- [ ] All acceptance criteria addressed

---

### 7.3 Acceptance Criteria Verification

**13 Functional Requirements**:
- [ ] REQ-032-001: Context7 budgets documented
- [ ] REQ-032-002: Adjustment guidance provided
- [ ] REQ-032-003: Design Patterns limits documented
- [ ] REQ-032-004: Pattern advisory section complete
- [ ] REQ-032-005: New guide file created
- [ ] REQ-032-006: 8-point checklist included
- [ ] REQ-032-007: MCP server references complete
- [ ] REQ-032-008: Decision tree provided
- [ ] REQ-032-009: Budget reference table included
- [ ] REQ-032-010: Anti-patterns documented
- [ ] REQ-032-011: CLAUDE.md section added
- [ ] REQ-032-012: Agent spec links added
- [ ] REQ-032-013: Cross-references consistent

**Non-Functional Requirements**:
- [ ] NFR-032-001: Clarity (readable for intermediate developers)
- [ ] NFR-032-002: Accuracy (matches TASK-012)
- [ ] NFR-032-003: Usability (find answers in <30 seconds)
- [ ] NFR-032-004: Formatting (consistent markdown)
- [ ] NFR-032-005: Completeness (no gaps)

---

## Success Criteria

### Quantitative
- ✅ 4 files modified/created
- ✅ ~400 lines of documentation
- ✅ 0 broken links
- ✅ 0 token budget discrepancies
- ✅ 100% test pass rate

### Qualitative
- ✅ Documentation is clear and actionable
- ✅ Examples are realistic and copy-pasteable
- ✅ Anti-patterns are memorable
- ✅ Cross-references support navigation
- ✅ Developer experience improved

---

## Time Budget

| Phase | Duration | Activity |
|-------|----------|----------|
| 1 | 5-10m | Preparation & verification |
| 2 | 15-20m | Context7 documentation |
| 3 | 10-15m | Pattern Advisor updates |
| 4 | 40-50m | New MCP Optimization Guide |
| 5 | 5m | CLAUDE.md integration |
| 6 | 10m | Cross-reference validation |
| 7 | 5-10m | Final validation & sign-off |
| **TOTAL** | **90-130m** | **1.5-2.2 hours** |

---

## Ready for Implementation

**Status**: ✅ Requirements analysis complete
**Next Command**: `/task-work TASK-032`

**Pre-Implementation Checklist**:
- [ ] TASK-032 task file available
- [ ] All requirements documents prepared
- [ ] Token budget numbers verified
- [ ] File paths confirmed
- [ ] Ready to implement Phase 1-7

---

**Roadmap prepared by**: AI Requirements Specialist
**Date**: 2025-10-25
**Confidence**: Very High
