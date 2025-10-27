# MCP Optimization Guide

## Overview

**Model Context Protocol (MCP)** servers provide specialized capabilities to AI agents in the Agentecflow system. This guide covers best practices for integrating and optimizing MCP usage to maximize value while minimizing context window consumption.

### What are MCPs?

MCPs are specialized servers that provide domain-specific tools and data to AI agents:
- **context7**: Up-to-date library documentation
- **design-patterns**: Pattern recommendations and implementation guidance
- **figma-dev-mode**: Figma design extraction and analysis
- **zeplin**: Zeplin design extraction and code conversion

### Current System Status

**Audit Results (TASK-012)**: ✅ All MCPs optimized

| MCP Server | Context Usage | Verdict |
|------------|---------------|---------|
| **context7** | 4.5-12% | ✅ OPTIMIZED |
| **design-patterns** | 4.5-9% | ✅ OPTIMIZED |
| **figma-dev-mode** | 2.5-5% | ✅ OPTIMIZED |
| **zeplin** | 2.5-5% | ✅ OPTIMIZED |

**Total Context Window Impact**: <15% across all active MCPs

### Why Optimize?

**Benefits**:
- ✅ Reduced token costs (lower API expenses)
- ✅ Faster response times (less data to process)
- ✅ Better context utilization (more room for task-specific data)
- ✅ Improved reliability (fewer timeout errors)

**Risks of Poor Optimization**:
- ❌ Context window exhaustion (task failures)
- ❌ Slow agent responses (degraded UX)
- ❌ High operational costs (wasted tokens)
- ❌ Information overload (too much data to process effectively)

---

## 8-Point Integration Checklist

Use this checklist when integrating new MCPs or auditing existing integrations:

### ✅ 1. Lazy Loading (Command-Specific or Phase-Specific)

**Principle**: Only load MCP when actually needed, not globally.

**Anti-Pattern** (❌ DON'T DO THIS):
```python
# ❌ BAD: Load all MCPs at agent initialization
class TaskManager:
    def __init__(self):
        self.context7 = Context7MCP()
        self.patterns = DesignPatternsMCP()
        self.figma = FigmaMCP()
        self.zeplin = ZeplinMCP()
```

**Best Practice** (✅ DO THIS):
```python
# ✅ GOOD: Load MCPs only when needed
class TaskManager:
    def execute_phase_3(self, task):
        # Only load Context7 if task requires library docs
        if self._requires_library_docs(task):
            context7 = Context7MCP()  # Lazy initialization
            docs = context7.get_library_docs(...)
```

**Real Example** (from `figma-react-orchestrator.md`):
```markdown
### Phase 0: MCP Verification
- Check if figma-dev-mode MCP is available
- ONLY load MCP if /figma-to-react command invoked
- Fail fast if MCP unavailable (don't waste time on subsequent phases)
```

**Implementation Pattern**:
```python
def verify_mcp_availability(mcp_name: str) -> bool:
    """Phase 0: Verify MCP before starting workflow"""
    try:
        # Quick health check (don't fetch data yet)
        mcp = get_mcp_client(mcp_name)
        return mcp.ping()
    except MCPNotAvailableError:
        logger.error(f"{mcp_name} MCP not available")
        return False
```

---

### ✅ 2. Scoped Queries (Use Topic, Filter, Category Parameters)

**Principle**: Request only the specific data you need, not entire documentation sets.

**Anti-Pattern** (❌ DON'T DO THIS):
```python
# ❌ BAD: Fetch entire FastAPI documentation (~50k tokens)
docs = context7.get_library_docs("/tiangolo/fastapi")
```

**Best Practice** (✅ DO THIS):
```python
# ✅ GOOD: Scope to specific topic (~5k tokens)
docs = context7.get_library_docs(
    library_id="/tiangolo/fastapi",
    topic="dependency-injection",  # Narrow scope
    tokens=5000  # Explicit limit
)
```

**Scoping Parameters by MCP**:

| MCP | Scoping Parameters | Example |
|-----|-------------------|---------|
| **context7** | `topic`, `tokens` | `topic="fixtures"`, `tokens=3000` |
| **design-patterns** | `category`, `tags`, `maxResults` | `category=["Resilience"]`, `maxResults=5` |
| **figma-dev-mode** | `component_ids`, `frame_ids` | Fetch specific frames, not entire file |
| **zeplin** | `screen_ids`, `component_ids` | Fetch specific screens, not entire project |

**Token Budget Comparison**:
```
Full FastAPI docs:     ~50,000 tokens ❌
Scoped to DI topic:     ~5,000 tokens ✅ (90% reduction)

All design patterns:   ~30,000 tokens ❌
Top 5 patterns:         ~5,000 tokens ✅ (83% reduction)
```

---

### ✅ 3. Token Limits (Default 5000, Adjust Per Use Case)

**Principle**: Always set explicit token limits based on phase and complexity.

**Token Budgets by Phase** (from `task-manager.md`):

| Phase | Token Budget | Rationale | Example Query |
|-------|--------------|-----------|---------------|
| **Phase 2: Planning** | 3000-4000 | High-level architecture, pattern overview | "fastapi dependency injection overview" |
| **Phase 3: Implementation** | 5000 (default) | Detailed API documentation, code examples | "fastapi dependency injection detailed examples" |
| **Phase 4: Testing** | 2000-3000 | Framework-specific testing patterns | "pytest fixtures and parametrize" |

**When to Adjust**:

```python
# ✅ Increase to 6000 tokens
if task.complexity >= 7:  # High complexity task
    tokens = 6000
elif task.is_unfamiliar_framework():  # Team new to library
    tokens = 6000

# ✅ Decrease to 3000 tokens
elif phase == "planning":  # Planning phase
    tokens = 3000
elif library.is_well_known():  # React, Express (familiar)
    tokens = 3000

# ✅ Decrease to 2000 tokens
elif phase == "testing":  # Testing frameworks are concise
    tokens = 2000
```

**Example Usage**:
```python
# Phase 2: Planning
docs = context7.get_library_docs(
    library_id="/tiangolo/fastapi",
    topic="architecture-overview",
    tokens=3500  # Planning phase budget
)

# Phase 3: Implementation
docs = context7.get_library_docs(
    library_id="/tiangolo/fastapi",
    topic="dependency-injection",
    tokens=5000  # Implementation phase budget
)

# Phase 4: Testing
docs = context7.get_library_docs(
    library_id="/pytest-dev/pytest",
    topic="fixtures",
    tokens=2500  # Testing phase budget
)
```

---

### ✅ 4. Caching Implementation (1-Hour TTL for Static Data)

**Principle**: Cache MCP responses to avoid redundant API calls.

**What to Cache**:
- ✅ Library documentation (rarely changes)
- ✅ Design pattern details (static reference data)
- ❌ Real-time design data (Figma, Zeplin)

**Caching Pattern**:
```python
from datetime import datetime, timedelta
from typing import Optional

class MCPCache:
    def __init__(self, ttl_minutes: int = 60):
        self.cache = {}
        self.ttl = timedelta(minutes=ttl_minutes)

    def get(self, key: str) -> Optional[dict]:
        """Get cached value if not expired"""
        if key not in self.cache:
            return None

        entry = self.cache[key]
        if datetime.now() - entry["timestamp"] > self.ttl:
            del self.cache[key]  # Expired
            return None

        return entry["data"]

    def set(self, key: str, data: dict):
        """Store value with timestamp"""
        self.cache[key] = {
            "data": data,
            "timestamp": datetime.now()
        }

# Usage
cache = MCPCache(ttl_minutes=60)

def get_library_docs_cached(library_id: str, topic: str) -> dict:
    cache_key = f"{library_id}:{topic}"

    # Check cache first
    cached = cache.get(cache_key)
    if cached:
        logger.info(f"Cache HIT: {cache_key}")
        return cached

    # Cache miss, fetch from MCP
    logger.info(f"Cache MISS: {cache_key}")
    docs = context7.get_library_docs(library_id, topic=topic)
    cache.set(cache_key, docs)

    return docs
```

**TTL Recommendations**:
- **context7**: 60 minutes (library docs change infrequently)
- **design-patterns**: 24 hours (static reference data)
- **figma-dev-mode**: NO CACHE (designs change frequently)
- **zeplin**: NO CACHE (designs change frequently)

---

### ✅ 5. Retry Logic (3 Attempts, Exponential Backoff)

**Principle**: Handle transient MCP failures gracefully.

**Retry Pattern**:
```python
import time
from typing import TypeVar, Callable

T = TypeVar('T')

def retry_with_backoff(
    func: Callable[[], T],
    max_attempts: int = 3,
    base_delay: float = 1.0
) -> T:
    """Retry function with exponential backoff"""

    for attempt in range(1, max_attempts + 1):
        try:
            return func()
        except MCPTransientError as e:
            if attempt == max_attempts:
                raise  # Final attempt failed

            # Exponential backoff: 1s, 2s, 4s
            delay = base_delay * (2 ** (attempt - 1))
            logger.warning(
                f"MCP call failed (attempt {attempt}/{max_attempts}), "
                f"retrying in {delay}s: {e}"
            )
            time.sleep(delay)

    raise RuntimeError("Retry logic failed")  # Should never reach

# Usage
docs = retry_with_backoff(
    lambda: context7.get_library_docs(library_id, topic=topic),
    max_attempts=3,
    base_delay=1.0
)
```

**When to Retry**:
- ✅ Network timeouts
- ✅ HTTP 429 (Rate Limit)
- ✅ HTTP 503 (Service Unavailable)
- ❌ HTTP 400 (Bad Request)
- ❌ HTTP 401 (Unauthorized)
- ❌ HTTP 404 (Not Found)

---

### ✅ 6. Fail Fast (Phase 0 Verification)

**Principle**: Verify MCP availability BEFORE starting workflow.

**Anti-Pattern** (❌ DON'T DO THIS):
```python
# ❌ BAD: Discover MCP unavailable in Phase 3 (waste of time)
def execute_workflow(task):
    plan = generate_plan(task)  # 5 minutes
    review = review_architecture(plan)  # 10 minutes
    # NOW discover Context7 is unavailable!
    docs = context7.get_library_docs(...)  # FAILS
```

**Best Practice** (✅ DO THIS):
```python
# ✅ GOOD: Verify MCP in Phase 0 (fail immediately)
def execute_workflow(task):
    # Phase 0: Pre-flight checks
    if task.requires_library_docs and not verify_mcp("context7"):
        raise WorkflowError("context7 MCP required but unavailable")

    # Continue with confidence
    plan = generate_plan(task)
    review = review_architecture(plan)
    docs = context7.get_library_docs(...)  # Will succeed
```

**Verification Pattern** (from `figma-react-orchestrator.md`):
```python
def phase_0_verify_mcp(command: str) -> bool:
    """Phase 0: Verify MCP before starting workflow"""

    required_mcps = {
        "/figma-to-react": "figma-dev-mode",
        "/zeplin-to-maui": "zeplin",
        "/task-work": None  # Conditional (context7)
    }

    mcp_name = required_mcps.get(command)
    if not mcp_name:
        return True  # No MCP required

    try:
        mcp = get_mcp_client(mcp_name)
        mcp.ping()  # Quick health check
        return True
    except MCPNotAvailableError:
        logger.error(
            f"Command '{command}' requires '{mcp_name}' MCP, "
            f"but it is not available. Please install and configure."
        )
        return False
```

---

### ✅ 7. Parallel Calls (When Possible)

**Principle**: Make independent MCP calls concurrently to reduce latency.

**Sequential Calls** (Slow):
```python
# ❌ SLOW: Sequential calls = 3 seconds total
docs1 = context7.get_library_docs("/react")         # 1s
docs2 = context7.get_library_docs("/tailwindcss")   # 1s
patterns = design_patterns.find_patterns(query)     # 1s
# Total: 3 seconds
```

**Parallel Calls** (Fast):
```python
# ✅ FAST: Parallel calls = 1 second total
import asyncio

async def fetch_all_resources():
    results = await asyncio.gather(
        context7.get_library_docs_async("/react"),
        context7.get_library_docs_async("/tailwindcss"),
        design_patterns.find_patterns_async(query)
    )
    return results

docs1, docs2, patterns = asyncio.run(fetch_all_resources())
# Total: 1 second (66% faster)
```

**Real Example** (from `zeplin-maui-orchestrator.md`):
```python
# Phase 2: Parallel design extraction
async def extract_designs(screen_ids: list[str]):
    """Fetch multiple screen designs in parallel"""
    tasks = [
        zeplin.get_screen_design(screen_id)
        for screen_id in screen_ids
    ]
    return await asyncio.gather(*tasks)

# Extract 5 screens in parallel (1s) vs sequential (5s)
designs = asyncio.run(extract_designs(screen_ids))
```

**When to Use Parallel Calls**:
- ✅ Multiple library documentations (React + Tailwind + Next.js)
- ✅ Multiple design screens (Figma frames, Zeplin screens)
- ✅ Pattern search + pattern details (if fetching multiple)
- ❌ Dependent calls (must wait for first result)

---

### ✅ 8. Token Budget Documentation

**Principle**: Document expected token usage for transparency and auditing.

**Documentation Template**:
```markdown
### Context7 MCP Usage

**When Invoked**: Phase 3 (Implementation)

**Query**:
- library_id: "/tiangolo/fastapi"
- topic: "dependency-injection"
- tokens: 5000 (Phase 3 budget)

**Token Estimate**:
- Expected: 4500-5000 tokens
- Context Window Impact: 4.5-5% (100k window)

**Caching**: Yes, 60-minute TTL

**Fallback**: If unavailable, use training data with warning
```

**Agent Specification Pattern** (see `task-manager.md` lines 23-73):
```markdown
## Context7 MCP Usage

### Token Budget Guidelines

**Token limits by phase** (optimize context window usage):

| Phase | Token Budget | Rationale |
|-------|--------------|-----------|
| Phase 2: Planning | 3000-4000 | High-level overview |
| Phase 3: Implementation | 5000 | Detailed examples |
| Phase 4: Testing | 2000-3000 | Testing patterns |
```

---

## MCP Server Reference

### context7 (Library Documentation)

**Purpose**: Retrieve up-to-date library documentation during implementation.

**When to Use**:
- ✅ Implementing with specific library/framework
- ✅ Unfamiliar with library API details
- ✅ Need current documentation (not just training data)
- ✅ Writing tests with testing framework

**When to Skip**:
- ❌ Standard language features (JavaScript syntax, Python builtins)
- ❌ Well-established patterns (SOLID principles)
- ❌ General software engineering concepts

**Token Budgets**:

| Phase | Budget | Example |
|-------|--------|---------|
| Planning | 3000-4000 | "fastapi architecture overview" |
| Implementation | 5000 | "fastapi dependency injection examples" |
| Testing | 2000-3000 | "pytest fixtures and parametrize" |

**Scoping with Topic Parameter**:
```python
# ✅ GOOD: Scoped queries
context7.get_library_docs(
    library_id="/tiangolo/fastapi",
    topic="dependency-injection",  # Narrow scope
    tokens=5000
)

# ⚠️ EXCESSIVE: No topic scoping
context7.get_library_docs(
    library_id="/tiangolo/fastapi",
    tokens=10000  # Will fetch broad documentation
)
```

**Stack-Specific Library Mappings**:

| Stack | Common Libraries | Topics |
|-------|------------------|--------|
| **react** | react, next.js, tailwindcss, vitest, playwright | hooks, routing, styling, testing |
| **python** | fastapi, pytest, pydantic, langchain | dependency-injection, testing, validation |
| **typescript-api** | nestjs, typeorm, jest | dependency-injection, decorators, testing |
| **maui** | maui, xamarin, xunit | mvvm, data-binding, navigation, testing |
| **dotnet-microservice** | fastendpoints, fluentvalidation | repr-pattern, validation, testing |

**Example (Good vs. Bad)**:

```python
# ❌ BAD: Fetching too much data
docs = context7.get_library_docs("/tiangolo/fastapi", tokens=10000)
# Returns: 10k tokens of general FastAPI docs (architecture, routing, DI, testing, deployment)

# ✅ GOOD: Scoped to specific need
docs = context7.get_library_docs(
    library_id="/tiangolo/fastapi",
    topic="dependency-injection",
    tokens=5000
)
# Returns: 5k tokens focused on DI patterns, Depends(), providers
```

**Reference**: See `task-manager.md` lines 23-73 for complete usage guidelines.

---

### design-patterns (Pattern Recommendations)

**Purpose**: Suggest appropriate design patterns based on requirements and constraints.

**When to Use**:
- ✅ Implementing complex business logic
- ✅ Need resilience patterns (Circuit Breaker, Retry)
- ✅ Architecting scalable systems
- ✅ Solving known problem classes (caching, event-driven, etc.)

**When to Skip**:
- ❌ Simple CRUD operations
- ❌ Trivial utility functions
- ❌ Team lacks expertise in suggested pattern
- ❌ YAGNI applies (pattern is over-engineered)

**Token Budget and Result Limiting**:

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

**Total Token Budget**: ~8-16k tokens (vs. 30k+ for naive approach)

**Anti-Pattern** (❌ DON'T DO THIS):
```python
# ❌ BAD: Fetching details for all 10 patterns = 30k tokens!
patterns = await find_patterns(query, maxResults=10)  # 10k tokens
for pattern in patterns:
    details = await get_pattern_details(pattern.id)  # 3k tokens each
# Total: 10k + (10 * 3k) = 40k tokens (40% of context window!)
```

**Best Practice** (✅ DO THIS):
```python
# ✅ GOOD: Only fetch top pattern details = 8k tokens total
patterns = await find_patterns(query, maxResults=5)  # 5k tokens
top_pattern = patterns[0]  # Highest confidence
details = await get_pattern_details(top_pattern.id)  # 3k tokens
# Total: 8k tokens (8% of context window)
```

**maxResults Guidance**:

| Use Case | maxResults | Token Cost | When to Use |
|----------|-----------|------------|-------------|
| **High Confidence Needed** | 3 | ~3k | Simple problems with clear solutions |
| **Standard (Recommended)** | 5 | ~5k | Most use cases, good diversity |
| **Exploration** | 10 | ~10k | Complex problems, uncertain solution |

**Example Usage**:
```python
# Phase 2.5A: Pattern recommendation
patterns = design_patterns.find_patterns(
    problem_description="Handle external API failures gracefully with <200ms timeout",
    context="Payment validation service",
    preferences={
        "language": "python",
        "complexity": "low-to-medium"
    },
    maxResults=5  # Get top 5 patterns
)

# Analyze confidence scores
# patterns[0]: Circuit Breaker (confidence: 0.95)
# patterns[1]: Retry Pattern (confidence: 0.82)
# patterns[2]: Timeout Pattern (confidence: 0.75)

# Get details only for top 2 patterns
circuit_breaker_details = design_patterns.get_pattern_details(
    pattern_name="Circuit Breaker Pattern",
    language="python"
)

retry_details = design_patterns.get_pattern_details(
    pattern_name="Retry Pattern",
    language="python"
)
```

**Reference**: See `pattern-advisor.md` lines 82-151 for complete usage guidelines.

---

### figma-dev-mode (Design Extraction)

**Purpose**: Extract design specifications from Figma files for component generation.

**When to Use**:
- ✅ Command: `/figma-to-react`
- ✅ Converting Figma designs to React components
- ✅ Extracting design tokens (colors, typography, spacing)

**Token Budget**: N/A (image-based, not text)

**Optimization Strategies**:

1. **Command-Specific Loading** (Lazy):
   - Only load when `/figma-to-react` invoked
   - NOT loaded for general task-work

2. **Parallel Call Pattern**:
   ```python
   # Extract multiple frames in parallel
   frames = await asyncio.gather(
       figma.get_frame(frame_id_1),
       figma.get_frame(frame_id_2),
       figma.get_frame(frame_id_3)
   )
   ```

3. **Caching Strategy**:
   - ❌ DO NOT cache (designs change frequently)
   - Exception: Design tokens (cache for 5 minutes during active session)

4. **Fail Fast** (Phase 0):
   ```python
   if not verify_mcp("figma-dev-mode"):
       raise CommandError("/figma-to-react requires figma-dev-mode MCP")
   ```

**Best Practices**:
- ✅ Fetch only specified frames/components (not entire file)
- ✅ Parallelize frame extraction when possible
- ✅ Use frame IDs, not names (more reliable)
- ❌ Don't fetch design history (only latest version)

**Reference**: See `figma-react-orchestrator.md` for complete workflow.

---

### zeplin (Design Extraction)

**Purpose**: Extract design specifications from Zeplin projects for MAUI component generation.

**When to Use**:
- ✅ Command: `/zeplin-to-maui`
- ✅ Converting Zeplin designs to XAML components
- ✅ Extracting iOS/Android-specific design specs

**Token Budget**: N/A (design-based, not text)

**Optimization Strategies**:

1. **Command-Specific Loading** (Lazy):
   - Only load when `/zeplin-to-maui` invoked
   - NOT loaded for general task-work

2. **Parallel Screen Extraction**:
   ```python
   # Extract multiple screens in parallel
   screens = await asyncio.gather(
       zeplin.get_screen(screen_id_1),
       zeplin.get_screen(screen_id_2),
       zeplin.get_screen(screen_id_3)
   )
   ```

3. **Icon Code Conversion**:
   - Zeplin provides icon SVG code
   - Convert to platform-specific format (PNG, vector drawable)

4. **Caching Strategy**:
   - ❌ DO NOT cache (designs change frequently)
   - Exception: Design tokens (cache for 5 minutes during active session)

**Best Practices**:
- ✅ Fetch only specified screens (not entire project)
- ✅ Parallelize screen extraction when possible
- ✅ Use screen IDs, not names (more reliable)
- ✅ Extract platform-specific assets (iOS, Android)

**Reference**: See `zeplin-maui-orchestrator.md` for complete workflow.

---

## Decision Tree: Which MCP to Use?

```
┌─────────────────────────────────────────┐
│ Need library/framework documentation?  │
└──────────────┬──────────────────────────┘
               │ YES
               ▼
       ┌───────────────┐
       │   context7    │
       └───────────────┘
       Tokens based on phase:
       - Planning: 3000-4000
       - Implementation: 5000
       - Testing: 2000-3000

┌─────────────────────────────────────────┐
│ Need design pattern recommendations?   │
└──────────────┬──────────────────────────┘
               │ YES
               ▼
       ┌───────────────┐
       │design-patterns│
       └───────────────┘
       maxResults: 5 (default)
       get_pattern_details: top 1-2 only

┌─────────────────────────────────────────┐
│ Have Figma design URL?                 │
└──────────────┬──────────────────────────┘
               │ YES
               ▼
       ┌───────────────┐
       │figma-dev-mode │
       └───────────────┘
       Automatic via /figma-to-react
       Fetch specific frames (parallel)

┌─────────────────────────────────────────┐
│ Have Zeplin design URL?                │
└──────────────┬──────────────────────────┘
               │ YES
               ▼
       ┌───────────────┐
       │    zeplin     │
       └───────────────┘
       Automatic via /zeplin-to-maui
       Fetch specific screens (parallel)
```

---

## Token Budget Reference Table

| MCP Server | Default Tokens | Min | Max | Adjust When |
|------------|----------------|-----|-----|-------------|
| **context7** | 5000 | 2000 | 6000 | Phase, complexity, familiarity |
| **design-patterns** (find_patterns) | ~5000 (5 results) | ~1000 (1 result) | ~10000 (10 results) | Number of patterns needed |
| **design-patterns** (get_pattern_details) | ~3000 per pattern | N/A | N/A | Top 1-2 patterns only |
| **figma-dev-mode** | N/A (image-based) | - | - | Not applicable |
| **zeplin** | N/A (design-based) | - | - | Not applicable |

**Context Window Impact**:

| Scenario | Token Usage | % of 100k Window | Verdict |
|----------|-------------|------------------|---------|
| **context7 (planning)** | 3500 | 3.5% | ✅ OPTIMIZED |
| **context7 (implementation)** | 5000 | 5.0% | ✅ OPTIMIZED |
| **design-patterns (5 patterns)** | 5000 | 5.0% | ✅ OPTIMIZED |
| **design-patterns (5 patterns + 2 details)** | 11000 | 11% | ⚠️ ACCEPTABLE |
| **design-patterns (10 patterns + all details)** | 40000 | 40% | ❌ EXCESSIVE |
| **Combined (context7 + patterns)** | 10000-16000 | 10-16% | ✅ OPTIMIZED |

---

## Anti-Patterns to Avoid

### ❌ Don't Fetch Unnecessary Documentation

**Problem**: Requesting broad documentation when you only need specific topic.

**Example**:
```python
# ❌ BAD: 50k tokens for entire FastAPI docs
docs = context7.get_library_docs("/tiangolo/fastapi")

# ✅ GOOD: 5k tokens for specific topic
docs = context7.get_library_docs(
    library_id="/tiangolo/fastapi",
    topic="dependency-injection",
    tokens=5000
)
```

**Impact**: 10x token usage, slower response, wasted context window.

---

### ❌ Don't Call get_pattern_details for All Patterns

**Problem**: Fetching detailed documentation for every pattern found.

**Example**:
```python
# ❌ BAD: 40k tokens (10 patterns × 3k each + 10k for find_patterns)
patterns = find_patterns(query, maxResults=10)  # 10k tokens
for pattern in patterns:
    details = get_pattern_details(pattern.id)  # 3k tokens each

# ✅ GOOD: 8k tokens (5 patterns + 1 detailed)
patterns = find_patterns(query, maxResults=5)  # 5k tokens
top_pattern = patterns[0]
details = get_pattern_details(top_pattern.id)  # 3k tokens
```

**Impact**: 5x token usage, 80% wasted (most patterns won't be used).

---

### ❌ Don't Skip Caching

**Problem**: Repeatedly fetching the same documentation/patterns.

**Example**:
```python
# ❌ BAD: Fetch docs 5 times during implementation
for file in files_to_implement:
    docs = context7.get_library_docs("/react")  # Same docs each time

# ✅ GOOD: Fetch once, cache, reuse
docs = get_cached_library_docs("/react")  # Fetch once
for file in files_to_implement:
    # Use cached docs
    implement_file(file, docs)
```

**Impact**: 5x API calls, 5x latency, 5x token costs.

---

### ❌ Don't Load MCPs Globally

**Problem**: Loading all MCPs at agent initialization.

**Example**:
```python
# ❌ BAD: All MCPs loaded, even if not needed
class Agent:
    def __init__(self):
        self.context7 = Context7MCP()
        self.patterns = DesignPatternsMCP()
        self.figma = FigmaMCP()
        self.zeplin = ZeplinMCP()

# ✅ GOOD: Lazy loading per command
class Agent:
    def execute_command(self, command):
        if command == "/figma-to-react":
            figma = FigmaMCP()  # Only load when needed
```

**Impact**: Slower startup, wasted resources, MCPs never used.

---

### ❌ Don't Ignore Token Budgets

**Problem**: No explicit token limits, allowing unbounded context consumption.

**Example**:
```python
# ❌ BAD: No token limit (could return 50k+ tokens)
docs = context7.get_library_docs("/tiangolo/fastapi")

# ✅ GOOD: Explicit budget based on phase
docs = context7.get_library_docs(
    library_id="/tiangolo/fastapi",
    topic="dependency-injection",
    tokens=5000  # Phase 3 budget
)
```

**Impact**: Unpredictable token usage, context window exhaustion, task failures.

---

## Monitoring MCP Usage

### How to Measure Context Window Impact

**Token Counting**:
```python
def count_tokens(text: str) -> int:
    """Approximate token count (1 token ≈ 4 characters)"""
    return len(text) // 4

# Measure MCP response size
docs = context7.get_library_docs(...)
token_count = count_tokens(docs)
percentage = (token_count / 100000) * 100  # Assuming 100k window

logger.info(
    f"context7 response: {token_count} tokens "
    f"({percentage:.1f}% of context window)"
)
```

**Metrics to Track**:
- Token count per MCP call
- Total tokens per task
- Cache hit rate
- MCP call latency
- MCP failure rate

### When to Investigate High Token Usage

**Thresholds**:
- ✅ Single MCP call: <10k tokens (10% of window)
- ⚠️ Single MCP call: 10-20k tokens (investigate)
- ❌ Single MCP call: >20k tokens (optimization needed)

**Investigation Checklist**:
1. Is `topic` parameter being used? (context7)
2. Is `maxResults` set appropriately? (design-patterns)
3. Are results being cached?
4. Is the query too broad?
5. Could the query be split into smaller, more focused queries?

### Tools for Debugging MCP Responses

**Logging Pattern**:
```python
import logging

logger = logging.getLogger(__name__)

def get_library_docs_with_logging(library_id: str, topic: str, tokens: int):
    logger.info(
        f"Fetching library docs: {library_id}, "
        f"topic={topic}, tokens={tokens}"
    )

    start_time = time.time()
    docs = context7.get_library_docs(library_id, topic=topic, tokens=tokens)
    duration = time.time() - start_time

    actual_tokens = count_tokens(docs)
    logger.info(
        f"Received {actual_tokens} tokens in {duration:.2f}s "
        f"({actual_tokens/tokens*100:.1f}% of budget)"
    )

    if actual_tokens > tokens * 1.1:  # 10% over budget
        logger.warning(
            f"Token budget exceeded: requested {tokens}, "
            f"received {actual_tokens}"
        )

    return docs
```

---

## Future Enhancements

### Dynamic Token Budgeting (TASK-012 Priority 2)

**Concept**: Adjust token budgets dynamically based on task complexity and phase.

```python
def calculate_dynamic_token_budget(task, phase):
    base_budget = {
        "planning": 3500,
        "implementation": 5000,
        "testing": 2500
    }[phase]

    # Adjust for complexity
    if task.complexity >= 7:
        base_budget *= 1.2  # +20% for high complexity
    elif task.complexity <= 3:
        base_budget *= 0.8  # -20% for low complexity

    # Adjust for familiarity
    if task.is_unfamiliar_framework():
        base_budget *= 1.2  # +20% for unfamiliar tech

    return int(base_budget)
```

**Benefits**:
- Automatic optimization (no manual tuning)
- Better resource utilization
- Adapts to task characteristics

---

### MCP Response Size Monitoring (TASK-012 Priority 2)

**Concept**: Track actual vs. expected token usage for auditing.

```python
class MCPMonitor:
    def __init__(self):
        self.metrics = []

    def record_call(self, mcp_name, query, expected_tokens, actual_tokens):
        variance = (actual_tokens - expected_tokens) / expected_tokens

        self.metrics.append({
            "mcp": mcp_name,
            "query": query,
            "expected_tokens": expected_tokens,
            "actual_tokens": actual_tokens,
            "variance": variance,
            "timestamp": datetime.now()
        })

        if variance > 0.2:  # >20% over budget
            logger.warning(
                f"{mcp_name} over budget: expected {expected_tokens}, "
                f"received {actual_tokens} (+{variance*100:.1f}%)"
            )

    def generate_report(self):
        """Generate token usage report"""
        avg_variance = sum(m["variance"] for m in self.metrics) / len(self.metrics)

        return {
            "total_calls": len(self.metrics),
            "average_variance": avg_variance,
            "over_budget_calls": sum(1 for m in self.metrics if m["variance"] > 0.2)
        }
```

---

### Extended Caching for context7/design-patterns

**Concept**: Persistent cache across task sessions.

```python
import json
from pathlib import Path

class PersistentMCPCache:
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)

    def get(self, key: str) -> Optional[dict]:
        cache_file = self.cache_dir / f"{key}.json"
        if not cache_file.exists():
            return None

        with open(cache_file) as f:
            entry = json.load(f)

        # Check expiration
        cached_at = datetime.fromisoformat(entry["cached_at"])
        if datetime.now() - cached_at > timedelta(hours=24):
            cache_file.unlink()  # Expired
            return None

        return entry["data"]

    def set(self, key: str, data: dict):
        cache_file = self.cache_dir / f"{key}.json"
        with open(cache_file, "w") as f:
            json.dump({
                "data": data,
                "cached_at": datetime.now().isoformat()
            }, f)
```

**Benefits**:
- Faster task execution (no redundant MCP calls)
- Lower API costs
- Offline capability (cached docs available)

---

## References

- **TASK-012**: MCP Usage Audit Report (`tasks/in_review/TASK-012-MCP-AUDIT-REPORT.md`)
- **task-manager.md**: Context7 usage guidelines (`installer/global/agents/task-manager.md`)
- **pattern-advisor.md**: Design Patterns usage guidelines (`installer/global/agents/pattern-advisor.md`)
- **figma-react-orchestrator.md**: Figma MCP workflow (`installer/global/agents/figma-react-orchestrator.md`)
- **zeplin-maui-orchestrator.md**: Zeplin MCP workflow (`installer/global/agents/zeplin-maui-orchestrator.md`)

---

## Summary

**Key Takeaways**:

1. **Lazy load MCPs** (command-specific, not global)
2. **Scope queries aggressively** (topic, category, filters)
3. **Set explicit token budgets** (3k-6k based on phase/complexity)
4. **Cache static data** (60-minute TTL for docs, 24-hour for patterns)
5. **Retry transient failures** (3 attempts, exponential backoff)
6. **Fail fast** (Phase 0 verification before workflow starts)
7. **Parallelize when possible** (multiple independent MCP calls)
8. **Document token budgets** (transparency and auditability)

**Current System Status**: ✅ All MCPs optimized (<15% context window usage)

**Future Work**: Dynamic budgeting, response monitoring, persistent caching
