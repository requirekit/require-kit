# Design Patterns MCP Setup Guide

**Purpose**: Enhance `/task-work` command with intelligent design pattern recommendations during architectural review (Phase 2.5A).

**MCP Server**: `apolosan/design_patterns_mcp` (TypeScript-based, 200+ patterns)

---

## Prerequisites

Before installing, ensure you have:
- **Node.js** v18 or later ([download here](https://nodejs.org/))
- **npm** (comes with Node.js)
- **Git** ([download here](https://git-scm.com/))

Verify installations:
```bash
node --version  # Should show v18.0.0 or later
npm --version   # Should show v8.0.0 or later
git --version   # Should show v2.0.0 or later
```

---

## Quick Start

### 1. Clone and Install Design Patterns MCP Server

**Step 1: Choose installation location**

Pick where you want to install the MCP server. Recommended locations:

- **macOS/Linux**: `~/mcp-servers/design-patterns-mcp`
- **Windows**: `C:\mcp-servers\design-patterns-mcp`

**Step 2: Clone the repository**

```bash
# macOS/Linux
mkdir -p ~/mcp-servers
cd ~/mcp-servers
git clone https://github.com/apolosan/design_patterns_mcp.git
cd design_patterns_mcp

# Windows (PowerShell)
New-Item -Path "C:\mcp-servers" -ItemType Directory -Force
cd C:\mcp-servers
git clone https://github.com/apolosan/design_patterns_mcp.git
cd design_patterns_mcp
```

**Step 3: Install dependencies**

```bash
npm install
```

This will download all required Node.js packages (may take 1-2 minutes).

**Step 4: Build the TypeScript project**

```bash
npm run build
```

This compiles the TypeScript code to JavaScript in the `dist/` folder.

**Step 5: Setup pattern database**

```bash
npm run db:setup
```

This downloads and indexes 200+ design patterns into a local SQLite database.

**⚠️ If you encounter "Cannot find module 'generate-embeddings.js'" error**:

The embeddings generation script may be missing in some versions. Run the setup steps individually instead:

```bash
# Run migration and seed only (skip embeddings)
npm run migrate
npm run seed
```

This will create the database and load patterns. The MCP server will work without embeddings (keyword and category search still function, just no semantic search optimization).

**Expected output (successful)**:
```
> design-patterns-mcp@0.2.1 migrate
> node dist/src/db/init.js migrate
Database migration complete

> design-patterns-mcp@0.2.1 seed
> node dist/src/db/init.js seed
✓ Seeding patterns...
✓ Loaded 243 patterns
Database seeded successfully
```

**Step 6: Verify database was created**

```bash
# Check that the database exists (it's in the data/ directory)
ls -lh data/design-patterns.db

# Should show the database file with pattern data
```

If the file exists, the database setup was successful!

**Step 7: Test the server (optional)**

```bash
npm run start
```

If successful, you should see:
```
Design Patterns MCP Server running on stdio
Ready to accept pattern queries
```

Press `Ctrl+C` to stop the test server (Claude Code will start it automatically).

---

### 2. Get Absolute Path

You'll need the absolute path to the installation directory for configuration.

**macOS/Linux**:
```bash
pwd
# Example output: /Users/yourname/mcp-servers/design_patterns_mcp
```

**Windows (PowerShell)**:
```powershell
Get-Location
# Example output: C:\mcp-servers\design_patterns_mcp
```

**Copy this path** - you'll need it in the next step.

---

### 3. Configure for Claude Code

**Step 1: Locate Claude Code MCP configuration file**

- **macOS/Linux**: `~/.config/claude-code/mcp.json`
- **Windows**: `%APPDATA%\claude-code\mcp.json`

**Step 2: Edit or create the configuration file**

If the file doesn't exist, create it:

```bash
# macOS/Linux
mkdir -p ~/.config/claude-code
touch ~/.config/claude-code/mcp.json

# Windows (PowerShell)
New-Item -Path "$env:APPDATA\claude-code" -ItemType Directory -Force
New-Item -Path "$env:APPDATA\claude-code\mcp.json" -ItemType File -Force
```

**Step 3: Add Design Patterns MCP configuration**

Edit `mcp.json` and add (or merge with existing content):

**macOS/Linux Example**:
```json
{
  "mcpServers": {
    "design-patterns": {
      "command": "node",
      "args": [
        "/Users/yourname/mcp-servers/design_patterns_mcp/dist/src/mcp-server.js"
      ],
      "env": {
        "DB_PATH": "/Users/yourname/mcp-servers/design_patterns_mcp/data/design-patterns.db"
      }
    }
  }
}
```

**Windows Example**:
```json
{
  "mcpServers": {
    "design-patterns": {
      "command": "node",
      "args": [
        "C:\\mcp-servers\\design_patterns_mcp\\dist\\src\\mcp-server.js"
      ],
      "env": {
        "DB_PATH": "C:\\mcp-servers\\design_patterns_mcp\\data\\design-patterns.db"
      }
    }
  }
}
```

**⚠️ IMPORTANT**:
- Replace paths with YOUR actual installation path from Step 2
- Use **forward slashes** `/` on macOS/Linux
- Use **double backslashes** `\\` on Windows (escape character)
- Ensure paths are **absolute** (full path from root), not relative

**Step 4: Verify configuration syntax**

Ensure the JSON is valid (no trailing commas, proper quotes):

```bash
# macOS/Linux - validate JSON
python3 -m json.tool ~/.config/claude-code/mcp.json

# Windows (PowerShell) - validate JSON
Get-Content "$env:APPDATA\claude-code\mcp.json" | ConvertFrom-Json
```

If valid, you'll see formatted JSON output. If invalid, fix syntax errors.

---

### 4. Restart Claude Code

**Completely quit and restart Claude Code** to load the new MCP server configuration.

The MCP server will start automatically when Claude Code launches and will be available as `mcp__design-patterns__*` tools.

---

### 5. Verify Installation

Run a test query in Claude Code:

```
Can you search for resilience patterns using the Design Patterns MCP?
```

Expected response:
- Claude should use `mcp__design-patterns__find_patterns` or `mcp__design-patterns__search_patterns`
- Should return patterns like Circuit Breaker, Retry, Bulkhead, etc.

---

## Available MCP Tools

Once installed, the following tools are available:

### 1. `mcp__design-patterns__find_patterns`

**Purpose**: Semantic search for patterns based on problem description

**Use Case**: Primary tool for `/task-work` Phase 2.5A pattern suggestions

**Parameters**:
```typescript
{
  problem_description: string,  // "I need a pattern for handling API failures with timeout constraints"
  context?: string,             // "Payment processing service with external gateway"
  preferences?: {
    language?: string,          // "Python", "TypeScript", "C#", etc.
    complexity?: string,        // "low", "medium", "high"
    category?: string           // "Resilience", "Performance", etc.
  }
}
```

**Example**:
```
Query: "I need a pattern for handling external API failures gracefully with timeout constraints under 200ms"

Response:
1. Circuit Breaker Pattern (Confidence: 0.95)
   - Category: Resilience
   - Why: Handles failures, enforces timeout
   - Implementation: Polly library (.NET), resilience4j (Java)

2. Retry Pattern (Confidence: 0.82)
   - Category: Resilience
   - Why: Handles transient failures
   - Implementation: Exponential backoff
```

### 2. `mcp__design-patterns__search_patterns`

**Purpose**: Keyword or category-based search with filters

**Use Case**: When you know the category or have specific keywords

**Parameters**:
```typescript
{
  query: string,                // "caching" or "resilience"
  filters?: {
    category?: string[],        // ["Microservices", "Cloud"]
    tags?: string[],            // ["performance", "scalability"]
    complexity?: string         // "low", "medium", "high"
  },
  limit?: number                // Max results (default: 10)
}
```

**Example**:
```
Query: search_patterns({ query: "resilience", filters: { category: ["Cloud"] } })

Response:
- Circuit Breaker Pattern
- Retry Pattern
- Bulkhead Pattern
- Timeout Pattern
- Fallback Pattern
```

### 3. `mcp__design-patterns__get_pattern_details`

**Purpose**: Get comprehensive information about a specific pattern

**Use Case**: Deep dive into implementation details, examples, trade-offs

**Parameters**:
```typescript
{
  pattern_name: string,         // "Circuit Breaker Pattern"
  language?: string             // "Python", "TypeScript", "C#" for code examples
}
```

**Example**:
```
Query: get_pattern_details({ pattern_name: "Circuit Breaker Pattern", language: "C#" })

Response:
- Detailed description
- When to use / when NOT to use
- Code examples in C#
- Similar patterns (Retry, Bulkhead, Timeout)
- Known implementations (Polly, Resilience4j)
- Trade-offs and considerations
```

### 4. `mcp__design-patterns__count_patterns`

**Purpose**: Get statistics about available patterns

**Use Case**: Reporting, coverage analysis

**Parameters**:
```typescript
{
  detailed?: boolean            // Include breakdown by category
}
```

**Example**:
```
Query: count_patterns({ detailed: true })

Response:
Total patterns: 243
- Creational: 23 (GoF + variations)
- Structural: 28 (GoF + variations)
- Behavioral: 31 (GoF + variations)
- Architectural: 45 (MVC, MVVM, Clean Architecture, etc.)
- Microservices: 38 (Circuit Breaker, CQRS, Event Sourcing, etc.)
- Cloud: 42 (Auto-scaling, Load Balancing, etc.)
- Performance: 36 (Caching, Lazy Loading, etc.)
```

---

## Integration with `/task-work` Command

The Design Patterns MCP is integrated into Phase 2.5A of the `/task-work` command:

### Workflow

```
Phase 2: Implementation Planning
    ↓
Phase 2.5A: Pattern Suggestion (NEW)
    - Query Design Patterns MCP with problem description
    - Extract constraints from EARS requirements
    - Display recommended patterns with confidence scores
    ↓
Phase 2.5B: Architectural Review
    - architectural-reviewer validates pattern suggestions
    - Checks SOLID/DRY/YAGNI compliance
    - May suggest simpler alternatives (YAGNI)
    ↓
Phase 3: Implementation
    - Patterns guide implementation approach
    - Stack-specific implementation from MCP
```

### Example Task Execution

**Task**: TASK-042 - Implement payment validation service

**EARS Requirement**: "When payment is submitted, the system SHALL validate funds within 200ms"

**Phase 2.5A Output**:
```
🎯 Design Pattern Recommendations

Based on task requirements and constraints:

1. **Circuit Breaker Pattern** (Confidence: 95%)
   Category: Resilience
   Why: Handles external API failures, enforces timeout constraints
   Stack guidance: Use Polly library (.NET) with 150ms timeout

2. **Retry Pattern** (Confidence: 82%)
   Category: Resilience
   Why: Handles transient failures, works with Circuit Breaker
   Stack guidance: Exponential backoff with 3 retries max
```

**Phase 2.5B** (architectural-reviewer validates):
```
✅ Circuit Breaker is appropriate for external payment gateway
✅ Retry Pattern complements Circuit Breaker well
⚠️ RECOMMENDATION: Ensure Circuit Breaker opens AFTER retries exhausted
⚠️ YAGNI CHECK: For MVP, consider simpler timeout-only approach first
```

---

## Pattern Categories Available

The MCP server covers 200+ patterns across 20+ categories:

### 1. Gang of Four (GoF) Patterns
- **Creational**: Singleton, Factory, Builder, Prototype, Abstract Factory
- **Structural**: Adapter, Bridge, Composite, Decorator, Facade, Proxy, Flyweight
- **Behavioral**: Observer, Strategy, Command, State, Template Method, Iterator, Mediator, Memento, Chain of Responsibility, Visitor, Interpreter

### 2. Architectural Patterns
- MVC, MVP, MVVM
- Clean Architecture, Hexagonal Architecture, Onion Architecture
- Layered Architecture, Microservices Architecture
- Event-Driven Architecture, CQRS

### 3. Microservices Patterns
- Circuit Breaker, Retry, Bulkhead, Timeout
- Event Sourcing, CQRS, Saga
- API Gateway, Service Discovery, Load Balancing
- Strangler Fig, Backend for Frontend

### 4. Cloud Patterns (Azure/AWS)
- Auto-scaling, Load Balancing
- Cache-Aside, Content Delivery Network
- Health Endpoint Monitoring
- Throttling, Queue-Based Load Leveling
- Competing Consumers, Priority Queue

### 5. Enterprise Integration Patterns
- Message Queue, Publish-Subscribe
- Message Router, Message Translator
- Request-Reply, Event Bus
- Dead Letter Queue, Idempotent Receiver

### 6. Performance Patterns
- Caching (Cache-Aside, Read-Through, Write-Through, Write-Behind)
- Lazy Loading, Eager Loading
- Connection Pooling, Object Pool
- Database Index Strategy
- Materialized View

### 7. Security Patterns
- Authentication (JWT, OAuth, SAML)
- Authorization (RBAC, ABAC, Claims-based)
- Encryption at Rest, Encryption in Transit
- Token-Based Authentication
- Federated Identity

### 8. Data Patterns
- Repository, Unit of Work
- Active Record, Data Mapper
- Query Object, Specification
- Sharding, Partitioning
- Database per Service (Microservices)

### 9. Testing Patterns
- Test Double (Mock, Stub, Spy, Fake)
- Page Object, Screen Object
- Builder Pattern for Test Data
- Test Fixture, Test Factory

### 10. Concurrency Patterns
- Producer-Consumer, Thread Pool
- Actor Model, Async/Await
- Lock, Semaphore, Monitor
- Read-Write Lock

---

## Best Practices

### 1. When to Query Design Patterns MCP

**✅ DO** query when:
- Task has non-trivial requirements (not simple CRUD)
- Performance, scalability, or reliability constraints exist
- External dependencies involved (APIs, databases, message queues)
- Security or compliance requirements present
- Team is unsure of best architectural approach

**❌ DON'T** query when:
- Task is trivial (simple CRUD, basic validation)
- Requirements are well-understood and straightforward
- Pattern is already established in codebase (follow existing patterns)
- YAGNI applies (don't over-engineer MVPs)

### 2. Interpreting Confidence Scores

- **90-100%**: Very strong match, pattern directly solves stated problem
- **75-89%**: Good match, pattern addresses key constraints
- **60-74%**: Moderate match, pattern may help but consider alternatives
- **< 60%**: Weak match, likely not the best fit

### 3. Balancing Pattern Suggestions with YAGNI

Pattern suggestions are **guidance, not requirements**.

**architectural-reviewer may downgrade pattern suggestions**:
- "Circuit Breaker suggested BUT for MVP, simple timeout is sufficient"
- "Event Sourcing suggested BUT adds unnecessary complexity at this stage"
- "CQRS suggested BUT single database is fine for current scale"

**Trust the architectural review process**:
- Phase 2.5A suggests patterns (based on ideal solutions)
- Phase 2.5B validates patterns (based on YAGNI, team expertise, project maturity)

### 4. Stack-Specific Implementation

Always request stack-specific guidance:

```
DON'T: "Use Circuit Breaker Pattern"
DO: "Use Circuit Breaker Pattern with Polly library (.NET) or resilience4j (Java)"
```

The MCP provides implementation guidance, but architectural-reviewer ensures it aligns with your stack.

---

## Troubleshooting

### "Cannot find module 'generate-embeddings.js'" Error

**Symptom**: During `npm run db:setup`, you see:
```
Error: Cannot find module '/path/to/design_patterns_mcp/dist/src/generate-embeddings.js'
```

**Cause**: The embeddings generation script is missing or not built in some versions of the MCP server.

**Solution**: Run migration and seed individually (skip embeddings):
```bash
cd /path/to/design_patterns_mcp

# Run just migration and seed
npm run migrate
npm run seed

# Verify database was created (it's in data/ directory)
ls -lh data/design-patterns.db
```

**Impact**: The MCP server will work fine without embeddings. You'll still have full pattern search via keywords and categories, just without semantic search optimization.

**Verification**: Test the server still works:
```bash
npm run start
# If it starts without errors, you're good to go!
```

**Important**: When configuring Claude Code (Step 3), use the correct database path:
- `DB_PATH`: `/path/to/design_patterns_mcp/data/design-patterns.db` (not `patterns.db`)

### MCP Server Not Available

**Symptom**: `/task-work` skips Phase 2.5A, tools not found

**Check**:
```bash
# Verify MCP server is running
ps aux | grep mcp-server

# Check Claude Code MCP configuration
cat ~/.config/claude-code/mcp.json

# Restart Claude Code
```

**Solution**:
- Ensure `mcp.json` has correct path to `mcp-server.js`
- Ensure `node` is in PATH
- Restart Claude Code completely (quit and relaunch)

### Database Not Found

**Symptom**: Error: "Database file not found" when MCP server starts

**Check**:
```bash
# Verify database exists
ls /path/to/design_patterns_mcp/patterns.db

# If missing, create it
cd /path/to/design_patterns_mcp
npm run migrate
npm run seed
```

**Solution**:
- Set `DB_PATH` environment variable correctly in `mcp.json`
- Ensure path is absolute (not relative)
- Re-run database setup if file missing

### No Patterns Returned

**Symptom**: MCP query returns empty results

**Check**:
- Query may be too specific (try broader terms)
- Database may be empty (re-run `npm run db:setup`)
- Language filter may be too restrictive (try without language filter)

**Solution**:
```
Instead of: "I need a pattern for validating JWT tokens with RSA-256 encryption in Rust"
Try: "I need a pattern for JWT token validation"
Then filter by language after getting results
```

### MCP Server Crashes

**Symptom**: MCP server exits unexpectedly

**Check**:
```bash
# Check logs
cat ~/.config/claude-code/mcp.log

# Common issues:
# - Node.js version incompatibility (requires Node 18+)
# - Database corruption (re-run db:setup)
# - Memory issues (large query results)
```

**Solution**:
- Update Node.js to v18 or later
- Re-run `npm run db:setup`
- Restart Claude Code

---

## Advanced Usage

### Custom Query Patterns

You can craft more specific queries:

**Combine constraints**:
```
"I need a pattern for handling high-volume message processing (10,000 msg/sec)
with guaranteed delivery and fault tolerance in a distributed system"

Expected: Event Sourcing, CQRS, Competing Consumers, Message Queue
```

**Focus on trade-offs**:
```
"I need a caching pattern that balances performance and consistency,
where stale data for up to 5 minutes is acceptable"

Expected: Cache-Aside with TTL, Read-Through Cache
```

**Stack-specific**:
```
"I need a dependency injection pattern for Python FastAPI
that supports request-scoped services"

Expected: Dependency Injection with FastAPI's Depends, Service Locator
```

### Combining Multiple Tools

**Workflow for deep analysis**:

1. **find_patterns**: Get initial recommendations
2. **get_pattern_details**: Deep dive into top 2-3 patterns
3. **search_patterns**: Find similar patterns (alternatives)
4. **Compare trade-offs**: Make informed decision

---

## Future Enhancements

When Agentecflow builds its own Python-based Design Patterns MCP:

**Additional Features**:
- EARS constraint extraction (automatic from requirements)
- Knowledge graph relationships (OFTEN_USED_WITH, CONFLICTS_WITH)
- Pattern validation (check for conflicts)
- LangGraph-powered data curation (auto-update from authoritative sources)

**Migration Path**:
1. Continue using existing MCP (immediate value)
2. Build Python MCP in parallel (informed by real usage)
3. Swap MCP connection when ready (seamless transition)
4. No changes to `/task-work` command or agent specifications

---

## Summary

**Installation**: `npm install` + `npm run db:setup` + configure `mcp.json`

**Usage**: Automatic in `/task-work` Phase 2.5A when MCP available

**Value**: Intelligent pattern suggestions based on 200+ proven patterns

**Integration**: Seamless with architectural-reviewer validation

**Optional**: System works fine without MCP (degraded gracefully)

**Future**: Agentecflow will build superior Python-based MCP, seamless migration

---

**Next Steps**:
1. Install Design Patterns MCP server
2. Configure Claude Code MCP connection
3. Test with a sample task
4. Use `/task-work` to see pattern suggestions in action
