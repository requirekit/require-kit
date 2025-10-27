---
id: TASK-014
title: Ensure Context7 MCP integration in task-work command
status: completed
created: 2025-10-14T10:30:00Z
updated: 2025-10-25T01:00:00Z
completed_at: 2025-10-25T17:35:27Z
priority: high
tags: [mcp, context7, task-work, library-documentation, enhancement]
epic: null
feature: null
requirements: []
external_ids:
  jira: null
  linear: null
bdd_scenarios: []
test_results:
  status: n/a
  coverage: n/a
  last_run: null
completion_metrics:
  total_duration: 11 days
  implementation_time: 2 hours
  files_modified: 4
  files_created: 1
  total_lines_added: 781
  documentation_created: true
  acceptance_criteria_met: 8/8
---

# Task: Ensure Context7 MCP integration in task-work command

## Description

Verify and enhance the `/task-work` command to ensure it properly utilizes the Context7 MCP server for retrieving up-to-date library documentation during implementation. The Context7 MCP should be invoked automatically when the implementation requires library-specific knowledge.

## Context

User request: "ensure that we've got instructions to use context7 MCP to make sure that that's used when executing the task-work command."

**Context7 MCP capabilities:**
- `resolve-library-id`: Resolves package/product name to Context7-compatible library ID
- `get-library-docs`: Fetches up-to-date documentation for a library

**Current status**: Unknown if Context7 is explicitly integrated in task-work workflow

**task-work phases:**
1. Requirements Analysis
2. Implementation Planning
3. Implementation
4. Testing (with compilation check)
5. Code Review

**Where Context7 should be used:**
- Phase 2 (Implementation Planning) - When selecting libraries/frameworks
- Phase 3 (Implementation) - When implementing with specific libraries
- Phase 4 (Testing) - When writing tests using testing frameworks

## Acceptance Criteria

- [x] Document Context7 MCP usage in task-work command specification
- [x] Add explicit instructions for when to invoke Context7
- [x] Provide examples of Context7 usage in task-work workflow
- [x] Ensure Context7 is called for library-specific implementations
- [x] Add guidance on which libraries warrant Context7 lookup
- [x] Document how to use resolve-library-id before get-library-docs
- [x] Verify Context7 integration works across all development modes (TDD/BDD/standard)
- [x] Add Context7 usage to architectural review phase (Phase 2.5) if relevant

## Implementation Strategy

### 1. Update task-work.md Command Specification

**Location**: `installer/global/commands/task-work.md`

**Sections to add/update:**

#### Section: MCP Integration

Add explicit Context7 MCP instructions:

```markdown
## Context7 MCP Integration (Library Documentation)

During task implementation, **automatically use Context7 MCP** to retrieve up-to-date library documentation when:

### When to Use Context7

1. **Phase 2: Implementation Planning**
   - When selecting libraries or frameworks for the implementation
   - When planning API usage patterns
   - When determining best practices for a library

2. **Phase 3: Implementation**
   - When implementing features using specific libraries
   - When unfamiliar with a library's API
   - When library documentation is needed for correct usage
   - When implementing patterns specific to a framework (React hooks, FastAPI patterns, etc.)

3. **Phase 4: Testing**
   - When writing tests using testing frameworks (pytest, Vitest, xUnit)
   - When setting up test fixtures or mocks
   - When implementing test patterns specific to the stack

### Context7 Workflow

**Step 1: Resolve Library ID**
```bash
# Always resolve library name to Context7-compatible ID first
mcp__context7__resolve-library-id("react")
# Returns: /facebook/react or /facebook/react/v18.2.0
```

**Step 2: Get Library Documentation**
```bash
# Use resolved ID to fetch documentation
mcp__context7__get-library-docs(
  context7CompatibleLibraryID: "/facebook/react",
  topic: "hooks",              # Optional: focus area
  tokens: 5000                 # Optional: max tokens (default: 5000)
)
```

### Examples by Stack

**React/TypeScript:**
- Resolve: "react", "next.js", "tailwindcss", "vitest", "playwright"
- Topics: "hooks", "routing", "styling", "testing"

**Python:**
- Resolve: "fastapi", "pytest", "pydantic", "langchain", "streamlit"
- Topics: "dependency-injection", "testing", "validation", "agents"

**.NET MAUI:**
- Resolve: "maui", "xamarin", "xunit", "moq"
- Topics: "mvvm", "data-binding", "navigation", "testing"

**TypeScript API:**
- Resolve: "nestjs", "typeorm", "jest", "supertest"
- Topics: "dependency-injection", "decorators", "testing", "validation"

### Integration Points

**Phase 2: Implementation Planning**
```
When task requires library usage:
1. Identify required libraries from requirements
2. Use Context7 to resolve library IDs
3. Fetch documentation for implementation approach
4. Incorporate library best practices into implementation plan
```

**Phase 3: Implementation**
```
When implementing with unfamiliar library APIs:
1. Use Context7 to get current documentation
2. Focus documentation on relevant topics (use `topic` parameter)
3. Implement according to latest library patterns
4. Verify implementation matches library best practices
```

**Phase 4: Testing**
```
When writing tests:
1. Use Context7 to get testing framework docs
2. Focus on testing patterns and assertions
3. Implement tests using framework best practices
```

### Best Practices

1. **Always resolve library ID first** - Don't assume library path format
2. **Use topic parameter** - Narrow documentation to relevant sections
3. **Limit token usage** - Default 5000 tokens is usually sufficient
4. **Cache library IDs** - Reuse resolved IDs within same task session
5. **Version awareness** - Use specific versions when available (/library/vX.Y.Z)
6. **Framework-specific patterns** - Always check library-specific patterns for the stack

### Error Handling

If Context7 library is not found:
- Proceed with general knowledge
- Document that library docs were unavailable
- Note in implementation for human review
```

### 2. Update task-manager Agent Specification

**Location**: `installer/global/agents/task-manager.md`

**Section to add:**

```markdown
## Context7 MCP Usage in Task Workflow

As the task-manager agent, you MUST use Context7 MCP when:

1. **Planning implementation** (Phase 2)
   - Task requires specific library or framework
   - Implementation plan references library APIs
   - Best practices for library are needed

2. **During implementation** (Phase 3)
   - Implementing with library-specific patterns
   - Unfamiliar with library API details
   - Need current documentation (not just training data)

3. **Writing tests** (Phase 4)
   - Using testing framework (pytest, Vitest, xUnit)
   - Implementing test patterns
   - Setting up test infrastructure

### Context7 Invocation Pattern

**Before implementing library-specific code:**

```
1. Identify library: "fastapi"
2. Resolve ID: mcp__context7__resolve-library-id("fastapi")
3. Get docs: mcp__context7__get-library-docs(
     context7CompatibleLibraryID: "/tiangolo/fastapi",
     topic: "dependency-injection",
     tokens: 5000
   )
4. Implement using latest patterns from documentation
```

**Always inform the user:**
```
📚 Fetching latest documentation for [library]...
✅ Retrieved [library] documentation (topic: [topic])
```

### Stack-Specific Library Mappings

Include table of common libraries per stack template.
```

### 3. Add Context7 Examples to Workflow Documentation

**Location**: `docs/workflows/task-work-workflow.md` (create if doesn't exist)

Add real-world examples showing Context7 integration.

### 4. Update Stack-Specific Agent Specifications

For each stack-specific agent (if they exist):
- `installer/global/agents/react-state-specialist.md`
- `installer/global/agents/python-api-specialist.md`
- `installer/global/agents/maui-viewmodel-specialist.md`
- etc.

Add Context7 usage guidance specific to that stack.

## Test Requirements

### Manual Testing
- [ ] Create test task requiring React hooks implementation
- [ ] Execute `/task-work TASK-XXX --mode=standard`
- [ ] Verify Context7 is invoked for React documentation
- [ ] Confirm documentation is used in implementation
- [ ] Test with Python/FastAPI task
- [ ] Test with .NET MAUI task
- [ ] Test with TypeScript/NestJS task

### Automated Testing
- [ ] Create test scenario with library-specific requirements
- [ ] Mock Context7 MCP responses
- [ ] Verify Context7 called at appropriate phases
- [ ] Confirm implementation uses fetched documentation

## Success Metrics

- [ ] Context7 MCP explicitly documented in task-work command
- [ ] Clear guidance on when to use Context7
- [ ] Examples provided for all stack templates
- [ ] Stack-specific agents reference Context7 usage
- [ ] User confirmation that Context7 is being used in task-work executions
- [ ] Documentation searches use latest library patterns (not just training data)

## Implementation Notes

### Files to Update

1. **Command Specification** (Critical)
   - `installer/global/commands/task-work.md` - Add MCP Integration section

2. **Agent Specifications** (High Priority)
   - `installer/global/agents/task-manager.md` - Add Context7 usage instructions
   - Stack-specific agents (if they exist)

3. **Workflow Documentation** (Medium Priority)
   - `docs/workflows/task-work-workflow.md` - Add examples
   - `docs/guides/mcp-integration.md` - Create MCP usage guide

4. **CLAUDE.md** (Optional - if space allows)
   - Add brief mention of Context7 integration in task-work section
   - Link to detailed documentation

### Context7 vs. Training Data

**Why Context7 matters:**
- Training data may be outdated (cutoff date: January 2025)
- Library APIs change frequently
- Best practices evolve
- New features added regularly
- Context7 provides **current, authoritative documentation**

**When NOT to use Context7:**
- Standard language features (JavaScript, Python syntax)
- Well-established patterns (SOLID principles)
- General software engineering concepts
- Standard library functions (already in training data)

### Integration with Phase 2.5 (Architectural Review)

Consider adding Context7 to architectural review phase:
- Verify library selection aligns with best practices
- Check that proposed patterns match library recommendations
- Validate architectural decisions against library documentation

## Related Tasks

- TASK-012: Review MCP usage and optimize context window
- TASK-013: Optimize CLAUDE.md for context window efficiency

## Dependencies

- Context7 MCP server must be configured and accessible
- User must have Context7 installed and running

## Estimated Effort

3-5 hours (documentation updates + testing + examples)

## Priority Justification

**HIGH** - User explicitly requested this integration, and it significantly improves implementation quality by ensuring latest library documentation is used.
