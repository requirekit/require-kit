# Task Workflow Quick Reference - v2.0

## 🎉 NEW: Unified Workflow with Development Modes!

### The One Command You Need
```bash
/task-work TASK-XXX [--mode=standard|tdd|bdd]
```

This single command replaces the old multi-step process and supports three development styles!

## 🚀 Quick Start - Choose Your Style

### Standard Development (Default)
```bash
/task-create "Feature name"       # Create task
/task-work TASK-XXX              # Implement + test + verify
/task-complete TASK-XXX          # Mark done after review
```

### Test-Driven Development (TDD)
```bash
/task-create "Complex logic"
/task-work TASK-XXX --mode=tdd   # RED → GREEN → REFACTOR
/task-complete TASK-XXX
```

### Behavior-Driven Development (BDD)
```bash
/task-create "User story"
/task-link-bdd TASK-XXX BDD-001  # Link scenarios
/task-work TASK-XXX --mode=bdd   # Scenarios → Implementation
/task-complete TASK-XXX
```

## 📊 Development Modes Explained

### Standard Mode ⚡
```bash
/task-work TASK-XXX
```
- ✅ Implementation and tests together
- ✅ Fastest approach
- ✅ Good for straightforward features

### TDD Mode 🔴🟢🔵
```bash
/task-work TASK-XXX --mode=tdd
```
- 🔴 **RED**: Write failing tests first
- 🟢 **GREEN**: Minimal code to pass
- 🔵 **REFACTOR**: Improve quality
- ✅ Best for complex business logic

### BDD Mode 📖
```bash
/task-work TASK-XXX --mode=bdd
```
- 📖 Start from Gherkin scenarios
- 🎭 Generate step definitions
- 🏗️ Implement features
- ✅ Best for user-facing features

## 📋 Task States (Automatic Management!)

```
BACKLOG → IN_PROGRESS → IN_REVIEW → COMPLETED
             ↓              ↓
          BLOCKED        BLOCKED
```

**NEW**: States update automatically based on test results!
- ✅ Tests pass + coverage good → `IN_REVIEW`
- ❌ Tests fail → `BLOCKED`
- ⚠️ Low coverage → Stay in `IN_PROGRESS`

## ✅ Quality Gates (Automatic!)

| Gate | Threshold | Enforcement |
|------|-----------|-------------|
| Tests Pass | 100% | Required |
| Line Coverage | ≥80% | Required |
| Branch Coverage | ≥75% | Required |
| Performance | <30s | Warning |

**No need to check manually - `/task-work` handles everything!**

## 🔥 Common Workflows

### Feature Development (Standard)
```bash
/task-create "New feature"
/task-work TASK-XXX              # Everything automatic!
/task-complete TASK-XXX          # After review
```

### Bug Fix (Hotfix)
```bash
/task-create "Fix critical bug" priority:critical
/task-work TASK-XXX --mode=hotfix --coverage-threshold=70
/task-complete TASK-XXX
```

### Complex Logic (TDD)
```bash
/task-create "Payment calculator"
/task-work TASK-XXX --mode=tdd   # Ensures test-first approach
/task-complete TASK-XXX
```

### User Story (BDD)
```bash
/task-create "User checkout flow"
/task-link-bdd TASK-XXX BDD-001 BDD-002
/task-work TASK-XXX --mode=bdd   # From scenarios to code
/task-complete TASK-XXX
```

## 📈 Status Commands (Unchanged)

```bash
/task-status                     # View kanban board
/task-status filter:mine         # Your tasks
/task-view TASK-XXX             # Task details
/task-status report:daily        # Daily standup format
```

## 🔧 Advanced Options

### Fix Only (After failures)
```bash
/task-work TASK-XXX --fix-only   # Just fix and re-test
```

### Custom Coverage
```bash
/task-work TASK-XXX --coverage-threshold=90
```

### Dry Run
```bash
/task-work TASK-XXX --dry-run    # See what would happen
```

### Watch Mode
```bash
/task-work TASK-XXX --watch      # Continuous testing
```

## 📝 Output Examples

### Success Output
```
✅ Task Work Complete - TASK-XXX

Mode: TDD
Tests: 15/15 passing ✅
Coverage: 92% ✅
Duration: 45 seconds

Status: IN_PROGRESS → IN_REVIEW
Next: /task-review TASK-XXX
```

### Failure Output
```
❌ Task Work Failed - TASK-XXX

Tests: 12/15 passing ⚠️
Failed: 3 tests ❌
Coverage: 75% (min: 80%)

Status: IN_PROGRESS → BLOCKED
Fix and run: /task-work TASK-XXX --fix-only
```

## 🆚 Old vs New Comparison

| Action | Old Way (v1.0) | New Way (v2.0) |
|--------|---------------|----------------|
| Start work | `/task-start` | Automatic |
| Implement | `/task-implement` | `/task-work` |
| Test | `/task-test` | `/task-work` |
| Fix tests | `/task-test` again | `/task-work --fix-only` |
| TDD | Not supported | `/task-work --mode=tdd` |
| BDD | Manual process | `/task-work --mode=bdd` |

## 💡 Pro Tips

1. **Choose the right mode**:
   - Most tasks: Standard (default)
   - Complex logic: TDD
   - User features: BDD

2. **Let automation work**:
   - Don't manually manage states
   - Trust the quality gates
   - Follow the feedback

3. **Fix failures fast**:
   - Use `--fix-only` for quick iterations
   - Read error messages carefully
   - Check uncovered lines

4. **Document as you go**:
   - Task descriptions matter
   - Link requirements early
   - Keep acceptance criteria clear

## 🚨 Important Changes

### Deprecated Commands
These still work but show warnings:
- `/task-implement` → Use `/task-work`
- `/task-test` → Use `/task-work`
- `/task-start` → Automatic now

### Removed Manual Steps
- No need to manually run tests
- No need to check coverage
- No need to update task state
- No need to verify quality gates

## 📊 Task File Location (Unchanged)

```
tasks/
├── backlog/        # New tasks
├── in_progress/    # Active work
├── in_review/      # Passed all gates
├── blocked/        # Failed gates
└── completed/      # Finished
```

## 🎯 Quick Decision Tree

```
Need to implement a task?
    ↓
Is it user-facing with scenarios?
    Yes → /task-work --mode=bdd
    No ↓
Is it complex business logic?
    Yes → /task-work --mode=tdd
    No → /task-work (standard)
```

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Tests not found | Check test file locations |
| Coverage too low | `/task-work` generates more tests |
| Task stuck | Check `/task-view TASK-XXX` |
| Wrong mode used | Re-run with correct mode |

## 📚 Learn More

- Full guide: `/docs/guides/task-work-guide.md`
- Migration help: `/docs/guides/MIGRATION-GUIDE.md`
- Examples: `/task-work --examples`
- Mode details: `/task-work --mode-help=tdd`

## 🎉 Remember

**"One command to rule them all!"**

`/task-work` does everything - implementation, testing, verification, and state management. Just tell it which development style you prefer!

---
*Version 2.0 - Unified Workflow with Development Modes*
