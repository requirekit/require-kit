# Context7 MCP Integration Workflow

## Overview

This workflow describes how Context7 MCP is integrated into the `/task-work` command to automatically retrieve up-to-date library documentation during implementation. Context7 ensures that implementations use the latest library patterns and best practices, not just training data which may be outdated.

## Quick Start (2 minutes)

**For AI Agents executing `/task-work`:**

1. **Phase 2 (Planning)**: If task requires specific library → resolve library ID → fetch docs → incorporate into plan
2. **Phase 3 (Implementation)**: If implementing with library API → fetch docs with topic → implement with latest patterns
3. **Phase 4 (Testing)**: If using testing framework → fetch testing docs → implement tests with framework best practices

**Always inform user when fetching:**
```
📚 Fetching latest documentation for [library]...
✅ Retrieved [library] documentation (topic: [topic])
```

## When to Use Context7

### Phase 2: Implementation Planning

**Trigger conditions:**
- Task requires specific library or framework (fastapi, react, nestjs, etc.)
- Implementation plan references library APIs
- Best practices for library are needed

**Example scenario:**
```
Task: "Implement JWT authentication endpoint using FastAPI"

Context7 Usage:
1. Identify library: "fastapi"
2. Resolve ID: mcp__context7__resolve-library-id("fastapi")
   → Returns: /tiangolo/fastapi or /tiangolo/fastapi/v0.104.0
3. Get docs: mcp__context7__get-library-docs(
     context7CompatibleLibraryID="/tiangolo/fastapi",
     topic="dependency-injection",
     tokens=5000
   )
4. Incorporate latest FastAPI patterns into implementation plan
```

### Phase 3: Implementation

**Trigger conditions:**
- Implementing with library-specific patterns (React hooks, FastAPI dependencies, NestJS decorators)
- Unfamiliar with library API details
- Need current documentation (not just training data from 2023)

**Example scenario:**
```
Task: "Implement custom React hook for form validation"

Context7 Usage:
1. Resolve: mcp__context7__resolve-library-id("react")
   → Returns: /facebook/react/v18.2.0
2. Get docs: mcp__context7__get-library-docs(
     context7CompatibleLibraryID="/facebook/react/v18.2.0",
     topic="hooks",
     tokens=5000
   )
3. Implement useFormValidation hook following latest patterns
4. Ensure proper dependency array usage (common pitfall)
```

### Phase 4: Testing

**Trigger conditions:**
- Using testing framework (pytest, Vitest, xUnit, Jest)
- Implementing test patterns (fixtures, mocks, assertions)
- Setting up test infrastructure

**Example scenario:**
```
Task: "Write tests for authentication service"

Context7 Usage:
1. Resolve: mcp__context7__resolve-library-id("pytest")
   → Returns: /pytest-dev/pytest
2. Get docs: mcp__context7__get-library-docs(
     context7CompatibleLibraryID="/pytest-dev/pytest",
     topic="fixtures",
     tokens=5000
   )
3. Implement tests with proper fixture usage
4. Use latest pytest patterns (not deprecated approaches)
```

## Context7 Workflow

### Step 1: Resolve Library ID

**Always resolve library name first** - Don't assume library path format.

```python
# Use mcp__context7__resolve-library-id tool
result = mcp__context7__resolve_library_id("fastapi")

# Returns Context7-compatible ID:
# - /tiangolo/fastapi (latest)
# - /tiangolo/fastapi/v0.104.0 (specific version)
```

**Multiple matches:**
If multiple libraries match, Context7 returns list with trust scores. Select highest trust score.

### Step 2: Get Library Documentation

**Use resolved ID to fetch documentation:**

```python
# Use mcp__context7__get-library-docs tool
docs = mcp__context7__get_library_docs(
  context7CompatibleLibraryID="/tiangolo/fastapi",
  topic="dependency-injection",  # Optional: focus area
  tokens=5000                     # Optional: max tokens (default: 5000)
)
```

**Parameters:**
- `context7CompatibleLibraryID` (required): ID from resolve step
- `topic` (optional): Narrow to specific area (e.g., "hooks", "testing", "validation")
- `tokens` (optional): Max documentation tokens (default: 5000, max: 10000)

### Step 3: Apply Documentation

**In implementation plan (Phase 2):**
- Incorporate library best practices
- Reference latest API patterns
- Note any deprecated approaches to avoid

**In implementation (Phase 3):**
- Follow latest patterns from documentation
- Use current API methods (not deprecated)
- Implement error handling as documented

**In tests (Phase 4):**
- Use framework-specific testing patterns
- Apply latest assertion/fixture patterns
- Follow framework's testing best practices

## Stack-Specific Library Mappings

### React/TypeScript Stack

**Common libraries:**
- react
- next.js
- tailwindcss
- vitest
- playwright

**Common topics:**
- hooks (useState, useEffect, custom hooks)
- routing (App Router, Pages Router)
- styling (Tailwind utilities, responsive design)
- testing (component testing, E2E testing)

**Example:**
```
Task: "Implement server component with data fetching"

Context7 Queries:
1. resolve-library-id("next.js") → /vercel/next.js/v14.0.0
2. get-library-docs(
     context7CompatibleLibraryID="/vercel/next.js/v14.0.0",
     topic="server-components",
     tokens=5000
   )
```

### Python Stack

**Common libraries:**
- fastapi
- pytest
- pydantic
- langchain
- streamlit

**Common topics:**
- dependency-injection (FastAPI dependencies)
- testing (pytest fixtures, async testing)
- validation (Pydantic models, validators)
- agents (LangGraph, ReAct patterns)

**Example:**
```
Task: "Implement async API endpoint with validation"

Context7 Queries:
1. resolve-library-id("fastapi") → /tiangolo/fastapi
2. get-library-docs(
     context7CompatibleLibraryID="/tiangolo/fastapi",
     topic="dependency-injection",
     tokens=5000
   )
3. resolve-library-id("pydantic") → /pydantic/pydantic
4. get-library-docs(
     context7CompatibleLibraryID="/pydantic/pydantic",
     topic="validation",
     tokens=5000
   )
```

### TypeScript API Stack

**Common libraries:**
- nestjs
- typeorm
- jest
- supertest

**Common topics:**
- dependency-injection (NestJS providers)
- decorators (@Controller, @Injectable)
- testing (unit tests, integration tests)
- validation (class-validator, DTOs)

**Example:**
```
Task: "Implement REST controller with DTOs"

Context7 Queries:
1. resolve-library-id("nestjs") → /@nestjs/core
2. get-library-docs(
     context7CompatibleLibraryID="/@nestjs/core",
     topic="controllers",
     tokens=5000
   )
```

### .NET MAUI Stack

**Common libraries:**
- maui
- xamarin
- xunit
- moq

**Common topics:**
- mvvm (ViewModels, data binding)
- data-binding (INotifyPropertyChanged, two-way binding)
- navigation (Shell navigation, page navigation)
- testing (view model testing, UI testing)

**Example:**
```
Task: "Implement ViewModel with command pattern"

Context7 Queries:
1. resolve-library-id("maui") → /dotnet/maui
2. get-library-docs(
     context7CompatibleLibraryID="/dotnet/maui",
     topic="mvvm",
     tokens=5000
   )
```

### .NET Microservice Stack

**Common libraries:**
- fastendpoints
- fluentvalidation
- xunit
- testcontainers

**Common topics:**
- repr-pattern (Request-Endpoint-Response)
- validation (FluentValidation rules)
- testing (integration tests, test containers)

**Example:**
```
Task: "Implement endpoint with validation"

Context7 Queries:
1. resolve-library-id("fastendpoints") → /FastEndpoints/FastEndpoints
2. get-library-docs(
     context7CompatibleLibraryID="/FastEndpoints/FastEndpoints",
     topic="validation",
     tokens=5000
   )
```

## Best Practices

### 1. Always Resolve First

**DON'T** assume library path format:
```python
# ❌ Bad: Assuming path format
docs = mcp__context7__get_library_docs(
  context7CompatibleLibraryID="/react",  # Wrong format
  ...
)
```

**DO** resolve library ID first:
```python
# ✅ Good: Resolve first
library_id = mcp__context7__resolve_library_id("react")
docs = mcp__context7__get_library_docs(
  context7CompatibleLibraryID=library_id,
  ...
)
```

### 2. Use Topic Parameter

**Narrow documentation to relevant sections:**

```python
# Instead of fetching all docs (may exceed token limit)
docs = mcp__context7__get_library_docs(
  context7CompatibleLibraryID="/facebook/react",
  tokens=5000
)

# Narrow to specific topic
docs = mcp__context7__get_library_docs(
  context7CompatibleLibraryID="/facebook/react",
  topic="hooks",  # Only fetch hooks documentation
  tokens=5000
)
```

### 3. Limit Token Usage

**Default 5000 tokens is usually sufficient:**

```python
# For most cases, default is fine
docs = mcp__context7__get_library_docs(
  context7CompatibleLibraryID="/tiangolo/fastapi",
  topic="dependency-injection",
  tokens=5000  # Default
)

# Only increase if documentation is truncated
docs = mcp__context7__get_library_docs(
  context7CompatibleLibraryID="/tiangolo/fastapi",
  topic="dependency-injection",
  tokens=8000  # Increased
)
```

### 4. Cache Library IDs

**Reuse resolved IDs within same task session:**

```python
# At start of Phase 2
fastapi_id = mcp__context7__resolve_library_id("fastapi")
pytest_id = mcp__context7__resolve_library_id("pytest")

# Reuse in Phase 3
fastapi_docs = mcp__context7__get_library_docs(
  context7CompatibleLibraryID=fastapi_id,  # Reuse
  ...
)

# Reuse in Phase 4
pytest_docs = mcp__context7__get_library_docs(
  context7CompatibleLibraryID=pytest_id,  # Reuse
  ...
)
```

### 5. Version Awareness

**Use specific versions when available:**

```python
# Resolve may return version-specific ID
library_id = mcp__context7__resolve_library_id("react")
# Returns: /facebook/react/v18.2.0

# Use specific version ID for consistency
docs = mcp__context7__get_library_docs(
  context7CompatibleLibraryID="/facebook/react/v18.2.0",
  ...
)
```

### 6. Always Inform User

**Display what documentation is being fetched:**

```python
print("📚 Fetching latest documentation for FastAPI...")

docs = mcp__context7__get_library_docs(...)

print("✅ Retrieved FastAPI documentation (topic: dependency-injection)")
```

## When NOT to Use Context7

**Skip Context7 for:**

1. **Standard language features**
   - JavaScript syntax (const, let, arrow functions)
   - Python syntax (list comprehensions, decorators)
   - TypeScript types (interfaces, generics)

2. **Well-established patterns**
   - SOLID principles
   - DRY principle
   - Design patterns (Factory, Repository, Observer)

3. **General software engineering concepts**
   - REST API principles
   - Database normalization
   - Async/await concepts

4. **Standard library functions**
   - JavaScript: Array.map, Promise.all
   - Python: json.loads, datetime.now
   - C#: LINQ, Task.Run

**These are already in training data and don't need current documentation.**

## Error Handling

### Library Not Found

```python
try:
    library_id = mcp__context7__resolve_library_id("unknown-library")
except LibraryNotFoundError:
    # Proceed with general knowledge
    print("⚠️  Library 'unknown-library' not found in Context7")
    print("   Proceeding with general knowledge")
    # Continue implementation without Context7 docs
```

### Documentation Retrieval Failed

```python
try:
    docs = mcp__context7__get_library_docs(...)
except DocumentationRetrievalError as e:
    # Log error and proceed
    print(f"⚠️  Failed to retrieve documentation: {e}")
    print("   Using training data for implementation")
    # Continue with available knowledge
```

### API Rate Limiting

```python
try:
    docs = mcp__context7__get_library_docs(...)
except RateLimitError:
    # Wait and retry once
    time.sleep(2)
    docs = mcp__context7__get_library_docs(...)
```

## Integration with task-work Phases

### Phase 2: Implementation Planning

```python
def execute_phase_2(task_context):
    # ... planning logic ...

    # Detect required libraries from task requirements
    libraries = detect_required_libraries(task_context)

    # Fetch documentation for each library
    library_docs = {}
    for lib_name in libraries:
        print(f"📚 Fetching latest documentation for {lib_name}...")

        # Resolve library ID
        lib_id = mcp__context7__resolve_library_id(lib_name)

        # Get documentation
        docs = mcp__context7__get_library_docs(
            context7CompatibleLibraryID=lib_id,
            tokens=5000
        )

        library_docs[lib_name] = docs
        print(f"✅ Retrieved {lib_name} documentation")

    # Incorporate docs into implementation plan
    plan = generate_implementation_plan(task_context, library_docs)

    return plan
```

### Phase 3: Implementation

```python
def execute_phase_3(task_context, implementation_plan):
    # ... implementation logic ...

    # For each library-specific feature
    for feature in implementation_plan.features:
        if feature.requires_library_knowledge:
            lib_name = feature.library
            topic = feature.specific_topic

            print(f"📚 Fetching latest documentation for {lib_name} ({topic})...")

            # Resolve and fetch with topic
            lib_id = mcp__context7__resolve_library_id(lib_name)
            docs = mcp__context7__get_library_docs(
                context7CompatibleLibraryID=lib_id,
                topic=topic,
                tokens=5000
            )

            print(f"✅ Retrieved {lib_name} documentation (topic: {topic})")

            # Implement using latest patterns
            implement_feature(feature, docs)
```

### Phase 4: Testing

```python
def execute_phase_4(task_context, implementation):
    # Detect testing framework
    framework = detect_testing_framework(task_context)

    print(f"📚 Fetching latest documentation for {framework}...")

    # Resolve testing framework
    framework_id = mcp__context7__resolve_library_id(framework)

    # Get testing docs
    docs = mcp__context7__get_library_docs(
        context7CompatibleLibraryID=framework_id,
        topic="testing",
        tokens=5000
    )

    print(f"✅ Retrieved {framework} documentation (topic: testing)")

    # Generate tests using framework best practices
    tests = generate_tests(implementation, docs)

    return tests
```

## Success Metrics

**Context7 integration is successful when:**

1. ✅ Library documentation automatically fetched during planning
2. ✅ Implementation uses latest library patterns (not deprecated)
3. ✅ Tests follow current testing framework best practices
4. ✅ No manual documentation lookup required
5. ✅ Clear user feedback when fetching docs
6. ✅ Graceful fallback when library not found

## FAQ

**Q: How is Context7 different from training data?**

A: Training data has a cutoff (January 2025). Libraries like React, FastAPI, Next.js have frequent updates. Context7 provides current documentation, ensuring implementations use latest patterns and avoid deprecated APIs.

**Q: What if Context7 doesn't have the library?**

A: The system falls back to general knowledge from training data. It logs a warning and continues without blocking the workflow.

**Q: How often should Context7 be used?**

A: Every time you're implementing with a specific library's API. For general programming (loops, conditionals, basic syntax), training data is sufficient.

**Q: Does Context7 slow down task-work?**

A: Minimal impact (<2 seconds per fetch). The quality improvement (latest patterns, no deprecated code) outweighs the slight delay.

**Q: Can I skip Context7 for simple tasks?**

A: Yes. If a task uses only standard language features (no library-specific APIs), Context7 can be skipped.

**Q: What if I want a specific library version?**

A: Context7 supports version-specific IDs (e.g., `/facebook/react/v18.2.0`). Use specific versions for consistency.

## Related Documentation

- [task-work.md](../../installer/global/commands/task-work.md) - Full command specification with Context7 integration
- [task-manager.md](../../installer/global/agents/task-manager.md) - Task manager agent with Context7 usage instructions
- [CLAUDE.md](../../CLAUDE.md) - Project overview with Context7 reference

## Changelog

**2025-10-25**: Initial Context7 MCP integration workflow documentation (TASK-014)
