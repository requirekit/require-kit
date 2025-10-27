# AI Engineer Complete User Guide - v2.0

## 📚 Table of Contents

1. [What's New in v2.0](#whats-new-in-v20)
2. [System Overview](#system-overview)
3. [The Unified Workflow](#the-unified-workflow)
4. [Development Modes](#development-modes)
5. [The Complete Pipeline](#the-complete-pipeline)
6. [Task Management System](#task-management-system)
7. [Command Reference](#command-reference)
8. [Workflow Examples](#workflow-examples)
9. [Stack-Specific Guides](#stack-specific-guides)
10. [Best Practices](#best-practices)

## What's New in v2.0

### 🎉 Unified Task Workflow
The biggest change in v2.0 is the introduction of the `/task-work` command that unifies implementation, testing, and verification into a single workflow with three development modes:

- **Standard Mode**: Traditional development approach
- **TDD Mode**: Test-Driven Development with Red-Green-Refactor
- **BDD Mode**: Behavior-Driven Development from scenarios

### Key Improvements
- **70% fewer commands** - From 7+ to just 3 primary commands
- **Automatic quality gates** - Tests run automatically, coverage enforced
- **Smart state management** - Tasks progress based on test results
- **Development flexibility** - Choose your preferred approach (TDD/BDD/Standard)

## System Overview

The AI Engineer system is a comprehensive specification-driven development platform that combines:
- **EARS Requirements Engineering** - Formal requirements specification
- **BDD/Gherkin Scenarios** - Behavior-driven development
- **Unified Task Workflow** - Single command for implementation and testing
- **Automatic Quality Gates** - Enforced testing and coverage standards
- **Stack Templates** - Production-ready patterns for React, Python, .NET, and MAUI

### Core Philosophy

**"Implementation and testing are inseparable"**

Every feature follows this unified pipeline:
1. **Gather** requirements through interactive Q&A
2. **Formalize** into EARS notation for precision
3. **Generate** BDD scenarios for testing
4. **Work** on tasks with automatic testing and verification
5. **Complete** only when all quality gates pass

## The Unified Workflow

### Simplified Task Lifecycle (3 Commands!)

```bash
# 1. Create task with requirements
/task-create "User authentication feature" priority:high

# 2. Work on it (THIS DOES EVERYTHING!)
/task-work TASK-001 --mode=tdd    # or standard, or bdd

# 3. Complete after review
/task-complete TASK-001
```

### What `/task-work` Does Automatically

1. **Analyzes** task requirements and linked specifications
2. **Generates** implementation based on chosen mode
3. **Creates** comprehensive test suite
4. **Executes** tests automatically
5. **Evaluates** quality gates (coverage, performance)
6. **Updates** task state based on results
7. **Provides** actionable feedback for failures

## Development Modes

### Standard Mode (Default)
```bash
/task-work TASK-001
```

**When to use**: Straightforward features where you want to create implementation and tests together.

**Workflow**:
1. Generate implementation from requirements
2. Create comprehensive tests alongside
3. Run tests and check quality
4. Update state based on results

### TDD Mode (Test-Driven Development)
```bash
/task-work TASK-001 --mode=tdd
```

**When to use**: Complex business logic where tests should drive the design.

**Workflow**:
1. 🔴 **RED**: Generate failing tests based on requirements
2. 🟢 **GREEN**: Write minimal code to pass tests
3. 🔵 **REFACTOR**: Improve code while keeping tests green
4. ✅ Verify coverage and quality gates

### BDD Mode (Behavior-Driven Development)
```bash
/task-work TASK-001 --mode=bdd
```

**When to use**: User-facing features with Gherkin scenarios.

**Workflow**:
1. 📖 Parse linked BDD scenarios
2. 🎭 Generate step definitions
3. 🏗️ Implement features to satisfy scenarios
4. 📝 Add unit tests for internal logic
5. ✅ Verify all scenarios pass

## The Complete Pipeline

### Phase 1: Requirements Gathering

```bash
# Start interactive requirements session
/gather-requirements

# Claude asks targeted questions:
# - What problem are we solving?
# - Who are the users?
# - What are the key capabilities?
# - What are the performance requirements?
# - What are the security constraints?
```

**Output**: Natural language requirements document

### Phase 2: EARS Formalization

```bash
# Convert to formal EARS notation
/formalize-ears

# Generates requirements like:
# REQ-001: When user submits valid credentials, the system shall authenticate within 1 second
# REQ-002: If login fails 3 times, then the system shall lock the account for 15 minutes
# REQ-003: While session is active, the system shall validate tokens on each request
```

**Output**: `docs/requirements/REQ-XXX.md` files with formal specifications

### Phase 3: BDD Generation

```bash
# Create Gherkin scenarios from requirements
/generate-bdd

# Creates feature files with scenarios:
# Feature: User Authentication
#   Scenario: Successful login
#     Given a registered user exists
#     When they submit valid credentials
#     Then they should be authenticated
```

**Output**: `docs/bdd/features/*.feature` files with test scenarios

### Phase 4: Task Creation and Linking

```bash
# Create task linked to requirements and BDD
/task-create "Implement user authentication" priority:high

# Link to specifications (if not done automatically)
/task-link-requirements TASK-001 REQ-001 REQ-002 REQ-003
/task-link-bdd TASK-001 BDD-001 BDD-002
```

**Output**: `tasks/backlog/TASK-001.md` with full traceability

### Phase 5: Implementation with Unified Workflow

```bash
# THE NEW WAY - One command does everything!
/task-work TASK-001 --mode=tdd

# This single command:
# - Starts the task (moves to IN_PROGRESS)
# - Generates implementation based on mode
# - Creates comprehensive test suite
# - Runs tests automatically
# - Checks quality gates
# - Updates task state
# - Provides feedback
```

**Output**: Implementation code, tests, and automatic state updates

### Phase 6: Completion

```bash
# Review if needed (optional with new workflow)
/task-review TASK-001

# Complete when ready
/task-complete TASK-001
```

**Output**: Task archived with full verification history

## Task Management System

### Task States with Automatic Management

```
BACKLOG → IN_PROGRESS → IN_REVIEW → COMPLETED
             ↓              ↓
          BLOCKED        BLOCKED
```

**NEW: Automatic State Transitions**
- ✅ All tests pass + coverage good → `IN_REVIEW`
- ❌ Tests fail → `BLOCKED`
- ⚠️ Low coverage → Stay `IN_PROGRESS` with feedback
- 🔄 Fixed issues → Back to `IN_PROGRESS`

### Quality Gates (Enforced Automatically)

| Gate | Threshold | Action if Failed |
|------|-----------|-----------------|
| Tests Pass | 100% | Task → BLOCKED |
| Line Coverage | ≥80% | Request more tests |
| Branch Coverage | ≥75% | Request more tests |
| Performance | <30s | Warning only |

### Task File Structure
```yaml
---
id: TASK-001
title: Implement user authentication
status: in_review  # Updated automatically!
mode: tdd          # Development mode used
requirements: [REQ-001, REQ-002, REQ-003]
bdd_scenarios: [BDD-001, BDD-002]
test_results:      # Captured automatically!
  status: passed
  mode: tdd
  coverage:
    lines: 92
    branches: 88
  tests_total: 15
  tests_passed: 15
  tests_failed: 0
  duration: 2.3
---
```

## Command Reference

### Primary Commands (v2.0)

| Command | Purpose | Example |
|---------|---------|---------|
| `/task-create` | Create new task | `/task-create "Add login"` |
| **`/task-work`** | **Implement, test, and verify** | **`/task-work TASK-001 --mode=tdd`** |
| `/task-complete` | Mark as done | `/task-complete TASK-001` |

### Requirements & BDD Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/gather-requirements` | Interactive requirements gathering | `/gather-requirements auth` |
| `/formalize-ears` | Convert to EARS notation | `/formalize-ears` |
| `/generate-bdd` | Create BDD scenarios | `/generate-bdd REQ-001` |

### Linking Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/task-link-requirements` | Link EARS to task | `/task-link-requirements TASK-001 REQ-001` |
| `/task-link-bdd` | Link BDD to task | `/task-link-bdd TASK-001 BDD-001` |

### Status & Management Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/task-status` | View task board | `/task-status` |
| `/task-view` | View task details | `/task-view TASK-001` |
| `/task-review` | Optional review | `/task-review TASK-001` |

### Task-Work Options

| Option | Purpose | Example |
|--------|---------|---------|
| `--mode` | Development approach | `--mode=tdd` or `--mode=bdd` |
| `--coverage-threshold` | Custom coverage | `--coverage-threshold=90` |
| `--fix-only` | Just fix and re-test | `--fix-only` |
| `--dry-run` | Preview without executing | `--dry-run` |

## Workflow Examples

### Example 1: Standard Development

```bash
# 1. Create and link task
/task-create "Add user profile page"
/task-link-requirements TASK-050 REQ-050 REQ-051

# 2. Work on it (standard mode is default)
/task-work TASK-050

# Output:
# ✅ Implementation generated
# ✅ Tests created
# ✅ Tests executed: 12/12 passing
# ✅ Coverage: 85%
# ✅ Quality gates: PASSED
# 📊 Status: IN_PROGRESS → IN_REVIEW

# 3. Complete
/task-complete TASK-050
```

### Example 2: TDD for Complex Logic

```bash
# 1. Create task for complex calculation
/task-create "Tax calculation engine" priority:high

# 2. Work with TDD approach
/task-work TASK-051 --mode=tdd

# Output:
# 🔴 RED Phase: Creating 8 failing tests...
#    ❌ All tests failing (expected)
# 
# 🟢 GREEN Phase: Implementing minimal code...
#    ✅ 6/8 tests passing
#    🔧 Fixing remaining failures...
#    ✅ 8/8 tests passing
#
# 🔵 REFACTOR Phase: Improving code quality...
#    ♻️ Extracting methods
#    ♻️ Adding type hints
#    ✅ All tests still passing
#
# 📊 Coverage: 94%
# ✅ Task moved to IN_REVIEW

# 3. Complete
/task-complete TASK-051
```

### Example 3: BDD for User Story

```bash
# 1. Create user story task
/task-create "User checkout flow"

# 2. Link BDD scenarios
/task-link-bdd TASK-052 BDD-010 BDD-011 BDD-012

# 3. Work with BDD approach
/task-work TASK-052 --mode=bdd

# Output:
# 📖 Loading 3 BDD scenarios...
# 🎭 Generating step definitions...
# 🏗️ Implementing checkout service...
# 🧪 Running scenarios...
#    ✅ 3/3 scenarios passing
# 📝 Adding unit tests...
#    ✅ 15 unit tests passing
# 📊 Coverage: 88%
# ✅ Task moved to IN_REVIEW

# 4. Complete
/task-complete TASK-052
```

### Example 4: Fixing Failed Tests

```bash
# Scenario: Tests failed during work
/task-work TASK-053

# Output:
# ❌ Tests Failed - TASK-053 Blocked
# Failed: 2/10 tests
# 
# test_auth.py::test_login_timeout
#   TimeoutError: Exceeded 5s limit
#
# Suggested fix:
#   Add timeout parameter to login method
#
# After fixing, run:
# /task-work TASK-053 --fix-only

# After fixing the code:
/task-work TASK-053 --fix-only

# Output:
# ✅ All tests passing
# ✅ Coverage: 82%
# ✅ Task moved to IN_REVIEW
```

## Stack-Specific Implementation

### React Development
```bash
/task-work TASK-060 --mode=standard

# Generates:
# - Components with hooks and error boundaries
# - TypeScript interfaces
# - Comprehensive test suite
# - Accessibility compliance
# - Performance optimizations
```

### Python Development
```bash
/task-work TASK-061 --mode=tdd

# Generates:
# - Service classes with factory pattern
# - FastAPI endpoints
# - pytest test suite
# - LangGraph workflows (if needed)
# - Async support
```

### .NET Development
```bash
/task-work TASK-062 --mode=bdd

# Generates:
# - Services with Either monad
# - FastEndpoints
# - xUnit/NUnit tests
# - SpecFlow scenarios
# - OpenTelemetry integration
```

## Best Practices

### Choosing the Right Mode

| Scenario | Recommended Mode | Why |
|----------|-----------------|-----|
| Simple CRUD operations | Standard | Fast, straightforward |
| Complex business logic | TDD | Tests drive design |
| User-facing features | BDD | Scenarios guide implementation |
| Bug fixes | Standard with `--fix-only` | Quick iteration |
| Algorithm development | TDD | Ensure correctness |
| API endpoints | Standard | Well-understood patterns |

### Task Creation Best Practices

1. **Clear descriptions**: Be specific about what needs to be done
2. **Link early**: Connect requirements and BDD before starting
3. **Set priority**: Use priority levels appropriately
4. **Small scope**: Break large features into smaller tasks
5. **Acceptance criteria**: Define clear success conditions

### Working with `/task-work`

1. **Trust the process**: Let the command complete all phases
2. **Read feedback**: Error messages are actionable
3. **Fix promptly**: Use `--fix-only` for quick iterations
4. **Check coverage**: Review uncovered lines
5. **Verify quality**: Ensure all gates pass

### Common Patterns

#### Pattern: Feature Development
```bash
/gather-requirements → /formalize-ears → /generate-bdd → 
/task-create → /task-work → /task-complete
```

#### Pattern: Bug Fix
```bash
/task-create "Fix: [description]" priority:critical →
/task-work --mode=standard → /task-complete
```

#### Pattern: Refactoring
```bash
/task-create "Refactor: [component]" →
/task-work --mode=tdd → /task-complete
```

## Troubleshooting

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Tests not found | Check test file naming and location |
| Coverage too low | Review uncovered lines, add more tests |
| Task stuck in BLOCKED | Check test failures, use `--fix-only` |
| Wrong mode used | Re-run with correct mode |
| Quality gates failing | Review thresholds, improve tests |

### Recovery Commands

```bash
# Re-run with different mode
/task-work TASK-001 --mode=tdd

# Just fix and test
/task-work TASK-001 --fix-only

# Custom coverage threshold
/task-work TASK-001 --coverage-threshold=90

# Preview what would happen
/task-work TASK-001 --dry-run
```

## Migration from v1.0

If you're still using the old multi-command workflow:

### Old Way (7 commands)
```bash
/task-create → /task-start → /task-implement → 
/task-test → /task-review → /task-complete
```

### New Way (3 commands)
```bash
/task-create → /task-work → /task-complete
```

See [Migration Guide](MIGRATION-GUIDE.md) for detailed instructions.

## Quick Reference Card

### Task Lifecycle (v2.0)
```
Create → Work (implement+test+verify) → Complete
```

### Development Mode Decision Tree
```
Is it user-facing with scenarios?
  Yes → --mode=bdd
  No → Is it complex logic?
    Yes → --mode=tdd
    No → Standard (default)
```

### Quality Checklist (Automatic!)
- [x] Tests written (automatic)
- [x] Tests executed (automatic)
- [x] Coverage checked (automatic)
- [x] Performance verified (automatic)
- [x] State updated (automatic)
- [ ] Review completed (manual)
- [ ] Task completed (manual)

## Additional Resources

### Essential Guides
- [Quick Reference v2.0](../../.claude/TASK-WORKFLOW-QUICK-REFERENCE-V2.md) - Commands at a glance
- [Migration Guide](MIGRATION-GUIDE.md) - Moving from v1.0 to v2.0
- [Task Work Examples](task-work-practical-example.md) - Real-world scenarios
- [Task System Review](TASK-SYSTEM-REVIEW-AND-PLAN.md) - Design decisions

### Stack Documentation
- [React Patterns](../../installer/global/templates/react/PATTERNS.md)
- [Python Templates](../../installer/global/templates/python/CLAUDE.md)
- [.NET Microservice](../../installer/global/templates/dotnet-microservice/README.md)
- [.NET MAUI](../../installer/global/templates/maui/CLAUDE.md)

## Summary

The v2.0 AI Engineer system revolutionizes the development workflow with:

1. **Unified Command** - `/task-work` does everything
2. **Development Flexibility** - Choose TDD, BDD, or Standard
3. **Automatic Quality** - Tests and coverage enforced
4. **Smart State Management** - Progress based on results
5. **Clear Feedback** - Actionable error messages

The key innovation is making **implementation and testing inseparable** through a single command that handles the complete workflow, ensuring quality while reducing complexity.

Start with `/task-create`, then `/task-work` with your preferred mode, and let the system handle the rest!
