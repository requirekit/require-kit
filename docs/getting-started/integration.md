# Integration with taskwright

Learn how RequireKit integrates with taskwright for complete requirements-to-implementation workflow.

## Overview

RequireKit is a **standalone requirements management toolkit** that optionally integrates with [taskwright](https://github.com/taskwright-dev/taskwright) for task execution, quality gates, and automated testing.

## Standalone vs Integrated

### RequireKit Standalone

Use RequireKit alone when you:
- Need requirements documentation
- Want EARS notation for clarity
- Need BDD scenarios for testing
- Export to PM tools (Jira, Linear, GitHub Projects)
- Have existing implementation workflow

**Provides:**
- ✅ EARS requirements formalization
- ✅ BDD/Gherkin scenario generation
- ✅ Epic/feature hierarchy management
- ✅ Requirements traceability
- ✅ PM tool metadata export

### RequireKit + taskwright Integration

Add taskwright when you need:
- Task execution workflow with quality gates
- TDD-driven implementation
- Automated test execution and coverage
- Code review and architectural compliance
- Requirements-to-code traceability

**Provides everything above PLUS:**
- ✅ Task execution from requirements
- ✅ Automated quality gates (tests, coverage, review)
- ✅ Full traceability: REQ → BDD → FEAT → TASK → Code
- ✅ Test orchestration
- ✅ Complexity evaluation

## Installation

### Install RequireKit Only

```bash
git clone https://github.com/yourusername/require-kit.git
cd require-kit
./installer/scripts/install.sh
```

### Add taskwright Integration

```bash
# After installing RequireKit
git clone https://github.com/taskwright-dev/taskwright.git
cd taskwright
./installer/scripts/install.sh

# Verify integration
ls ~/.agentecflow/*.marker
# Should show both: require-kit.marker + taskwright.marker
```

## Integrated Workflow

When both packages are installed:

```
RequireKit (Requirements) → taskwright (Execution)
     ↓                            ↓
REQ-001 (EARS)               TASK-001 (Implementation)
     ↓                            ↓
BDD-001 (Scenarios)          Tests + Code
     ↓                            ↓
FEAT-001 (Feature)           Quality Gates
     ↓                            ↓
  Complete Traceability      Verified Implementation
```

### Step 1: Gather Requirements (RequireKit)

```bash
/gather-requirements
/formalize-ears
/generate-bdd
```

**Output:**
- `docs/requirements/REQ-001.md` (EARS notation)
- `docs/bdd/BDD-001.feature` (Gherkin scenarios)

### Step 2: Create Epic/Feature (RequireKit)

```bash
/epic-create "User Authentication System"
/feature-create "Login Functionality" epic:EPIC-001
```

**Output:**
- `docs/epics/EPIC-001.md`
- `docs/features/FEAT-001.md`

### Step 3: Generate Task Specifications (RequireKit)

```bash
/feature-generate-tasks FEAT-001
```

**Output:**
- `tasks/backlog/TASK-001.md` (with links to REQ-001, BDD-001, FEAT-001)

### Step 4: Execute Task (taskwright)

```bash
/task-work TASK-001
```

!!! note "BDD Mode Temporarily Removed"
    The `--mode=BDD` option has been temporarily removed from the `/task-work` command to maintain taskwright's independence from require-kit. This will be reintroduced in a future release with proper dependency inversion. For now, BDD scenarios are manually referenced during task execution.

**taskwright loads:**
- Requirements context from REQ-001
- BDD scenarios as acceptance criteria from BDD-001
- Feature specifications from FEAT-001

**taskwright provides:**
- TDD workflow with quality gates
- Automated testing and coverage
- Code review for SOLID/DRY principles
- Plan audit to prevent scope creep

### Step 5: Complete Task (taskwright)

```bash
/task-complete TASK-001
```

**Verification:**
- ✅ All tests passing
- ✅ Coverage ≥80%
- ✅ Code review passed
- ✅ BDD scenarios satisfied

## Bidirectional Detection

Both packages detect each other automatically:

```bash
# Check integration status
ls ~/.agentecflow/*.marker

# RequireKit only:  require-kit.marker
# taskwright only:  taskwright.marker
# Both integrated:  require-kit.marker + taskwright.marker
```

**How it works:**
- Each package creates a marker file during installation
- Commands check for marker files at runtime
- Integration features activate when both present
- No code dependencies - graceful degradation

## Feature Availability

| Feature | RequireKit Only | + taskwright |
|---------|----------------|--------------|
| EARS Requirements | ✅ | ✅ |
| BDD Generation | ✅ | ✅ |
| Epic/Feature Hierarchy | ✅ | ✅ |
| Task Specifications | ⚠️ Specs Only | ✅ Execution |
| Task Execution | ❌ | ✅ |
| Quality Gates | ❌ | ✅ |
| Test Orchestration | ❌ | ✅ |
| Requirements Context in Tasks | ❌ | ✅ Auto-loaded |
| Full Traceability | ⚠️ REQ→FEAT | ✅ REQ→FEAT→TASK→Code |

## Dependency Inversion Principle

The integration follows DIP (Dependency Inversion Principle):

**Correct flow:**
```
RequireKit (Higher-level)
    ↓ generates
Requirements, BDD, Specs
    ↓ consumed by
taskwright (Lower-level)
```

**Key principle:** taskwright never calls RequireKit commands. Data flows one direction through artifacts (markdown files).

## PM Tool Integration

RequireKit works with any PM tool:

### Export to Jira

```bash
/feature-sync FEAT-001 --jira
```

Creates Jira ticket with:
- User story from feature description
- Acceptance criteria from BDD scenarios
- Linked requirements (REQ-001)
- Linked epic (EPIC-001)

### Export to Linear

```bash
/feature-sync FEAT-001 --linear
```

### Export to GitHub Projects

```bash
/feature-sync FEAT-001 --github
```

**Note:** PM tool export provides structured metadata. Actual API integration requires MCP server or custom implementation.

## When to Use Each Approach

### Use RequireKit Standalone When:
- You have an existing PM tool workflow
- You need requirements documentation only
- You're in early planning/design phase
- You export to Jira/Linear for implementation
- Your team uses different implementation tools

### Use RequireKit + taskwright When:
- You need complete requirements-to-code workflow
- You want TDD with quality gates
- You need requirements context during implementation
- You want automated testing and coverage
- You need full traceability from requirements to code

## Migration Path

### From RequireKit to Integrated

1. Install taskwright
2. Existing requirements/BDD/features remain unchanged
3. New capabilities available immediately
4. No breaking changes

### From taskwright to Integrated

1. Install RequireKit
2. Add requirements retroactively (optional)
3. Link existing tasks to features
4. Continue with full workflow for new features

## Detailed Integration Guide

For complete integration documentation, see:

📖 **[Complete Integration Guide](../INTEGRATION-GUIDE.md)** (927 lines)

Covers:
- Installation scenarios
- Feature availability matrix
- Common workflows
- Troubleshooting
- Migration guides

## What's Next?

- 📖 [Read the Complete Integration Guide](../INTEGRATION-GUIDE.md)
- 🔗 [Learn about PM Tool Export](../integration/pm-tools.md)
- 📚 [Explore taskwright Documentation](https://github.com/taskwright-dev/taskwright)

---

**Questions?** Check the [Integration Guide FAQ](../INTEGRATION-GUIDE.md#troubleshooting)
