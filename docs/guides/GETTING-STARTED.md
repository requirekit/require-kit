# Getting Started with AI Engineer v2.0

## 🎉 Welcome to the Unified Workflow!

AI Engineer v2.0 introduces a revolutionary unified task workflow that combines implementation, testing, and verification into a single command with support for Standard, TDD, and BDD development modes.

## 🚀 Quick Start (3 Minutes!)

### Step 1: Initialize Your Project
```bash
# Clone and setup
git clone https://github.com/yourusername/ai-engineer.git
cd ai-engineer
chmod +x .claude/setup.sh
.claude/setup.sh
```

### Step 2: Create Your First Task (in Claude Code)
```bash
# Create a task
/task-create "Add user authentication"

# Work on it (THIS DOES EVERYTHING!)
/task-work TASK-001

# Complete it
/task-complete TASK-001
```

That's it! The `/task-work` command handles implementation, testing, and quality verification automatically.

## 📚 Documentation Structure

```
docs/guides/
├── README.md                                    # Index and navigation
├── AI-ENGINEER-USER-GUIDE.md                   # Complete guide (START HERE!)
├── MIGRATION-GUIDE.md                          # NEW: v1.0 to v2.0 migration
├── task-work-practical-example.md              # NEW: Real examples
├── TASK-WORKFLOW-QUICK-REFERENCE-V2.md         # NEW: Quick command reference
├── KANBAN-WORKFLOW-GUIDE.md                    # Task management details
├── COMMAND_USAGE_GUIDE.md                      # All commands reference
└── [other guides...]
```

## 🎯 What's New in v2.0

### The One Command That Does Everything
```bash
/task-work TASK-XXX [--mode=standard|tdd|bdd]
```

This single command replaces the old 7-step process:
- ✅ Generates implementation
- ✅ Creates comprehensive tests
- ✅ Runs tests automatically
- ✅ Checks quality gates
- ✅ Updates task state
- ✅ Provides actionable feedback

### Three Development Modes

#### Standard Mode (Default)
```bash
/task-work TASK-001
```
Traditional approach - implementation and tests together.

#### TDD Mode
```bash
/task-work TASK-001 --mode=tdd
```
Red → Green → Refactor cycle for complex logic.

#### BDD Mode
```bash
/task-work TASK-001 --mode=bdd
```
From Gherkin scenarios to implementation.

## 🔄 The Complete Development Flow

### 1. Requirements Phase
```bash
# Gather requirements interactively
/gather-requirements

# Formalize into EARS notation
/formalize-ears

# Generate BDD scenarios
/generate-bdd
```

### 2. Task Phase (NEW SIMPLIFIED!)
```bash
# Create task
/task-create "Feature name"

# Link specifications (if needed)
/task-link-requirements TASK-001 REQ-001
/task-link-bdd TASK-001 BDD-001

# WORK ON IT (one command!)
/task-work TASK-001 --mode=tdd

# Complete after review
/task-complete TASK-001
```

## ✨ Key Features

### Automatic Quality Gates
| Gate | Threshold | Enforcement |
|------|-----------|-------------|
| Tests Pass | 100% | Required |
| Line Coverage | ≥80% | Required |
| Branch Coverage | ≥75% | Required |
| Performance | <30s | Warning |

### Smart State Management
```
Tests Pass + Coverage Good → IN_REVIEW
Tests Fail → BLOCKED
Coverage Low → Stay IN_PROGRESS
```

### Clear Feedback
```
✅ Task Work Complete - TASK-001
Tests: 15/15 passing
Coverage: 92%
Status: IN_PROGRESS → IN_REVIEW
Next: /task-complete TASK-001
```

## 💡 Real-World Example

### Implementing User Authentication with TDD

```bash
# 1. Create the task
/task-create "Implement user authentication" priority:high

# 2. Link requirements (if you have them)
/task-link-requirements TASK-042 REQ-001 REQ-002 REQ-003

# 3. Work on it with TDD
/task-work TASK-042 --mode=tdd

# Claude's response:
# 🔴 RED Phase: Creating 8 failing tests...
#    ❌ All tests failing (expected)
# 
# 🟢 GREEN Phase: Implementing code...
#    ✅ 8/8 tests passing
#
# 🔵 REFACTOR Phase: Improving quality...
#    ✅ All tests still passing
#
# 📊 Coverage: 92%
# ✅ Task moved to IN_REVIEW

# 4. Complete the task
/task-complete TASK-042
```

Total time: ~2 minutes (vs ~10 minutes with old workflow)

## 🔧 Common Scenarios

### Scenario 1: Simple Feature
```bash
/task-create "Add user profile page"
/task-work TASK-050              # Standard mode by default
/task-complete TASK-050
```

### Scenario 2: Complex Business Logic
```bash
/task-create "Calculate tax rates"
/task-work TASK-051 --mode=tdd   # TDD for complex logic
/task-complete TASK-051
```

### Scenario 3: User Story
```bash
/task-create "User checkout flow"
/task-link-bdd TASK-052 BDD-001
/task-work TASK-052 --mode=bdd   # BDD for user features
/task-complete TASK-052
```

### Scenario 4: Bug Fix
```bash
/task-create "Fix login timeout" priority:critical
/task-work TASK-053               # Quick fix
/task-complete TASK-053
```

## 📊 Migration from v1.0

If you're using the old workflow:

### Old Way (7 commands)
```bash
/task-create
/task-start
/task-implement
/task-test
/task-review
/task-complete
```

### New Way (3 commands)
```bash
/task-create
/task-work      # Does everything!
/task-complete
```

See [Migration Guide](MIGRATION-GUIDE.md) for details.

## 🎯 Decision Tree

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

## 📋 Essential Commands

### Task Commands
```bash
/task-create "name"        # Create task
/task-work TASK-XXX       # Implement + test + verify
/task-complete TASK-XXX   # Mark done
/task-status              # View board
```

### Requirements Commands
```bash
/gather-requirements      # Interactive Q&A
/formalize-ears          # Create EARS
/generate-bdd            # Create scenarios
```

### Options for task-work
```bash
--mode=standard          # Default
--mode=tdd              # Test-driven
--mode=bdd              # Behavior-driven
--fix-only              # Just fix and test
--coverage-threshold=90 # Custom coverage
```

## 🏆 Best Practices

1. **Start with requirements** - Don't skip the specification phase
2. **Choose the right mode** - TDD for logic, BDD for features
3. **Trust the process** - Let `/task-work` complete all phases
4. **Fix immediately** - Use `--fix-only` for quick iterations
5. **Keep tasks small** - 1-2 hour chunks work best

## 🚦 Quality Standards

All enforced automatically by `/task-work`:
- ✅ 100% of tasks have tests
- ✅ ≥80% code coverage
- ✅ All tests must pass
- ✅ Performance <30s
- ✅ Proper documentation

## 📚 Learning Path

### For New Users
1. **Read** [User Guide](AI-ENGINEER-USER-GUIDE.md) - Complete overview
2. **Try** [Practical Examples](task-work-practical-example.md) - Real scenarios
3. **Reference** [Quick Guide](../../.claude/TASK-WORKFLOW-QUICK-REFERENCE-V2.md) - Commands

### For Existing Users
1. **Read** [Migration Guide](MIGRATION-GUIDE.md) - What's changed
2. **Try** new `/task-work` command - See the difference
3. **Adopt** development modes - TDD and BDD support

## 🛠 Technology Support

Works with all major stacks:
- **Python**: pytest, FastAPI, LangGraph
- **TypeScript/React**: Vitest, Playwright
- **.NET**: xUnit, NUnit, SpecFlow
- **Java**: JUnit, Cucumber
- **MAUI**: Platform testing

## 💡 Key Benefits

### Developer Experience
- **70% fewer commands** to remember
- **50% faster** task completion
- **Zero** manual quality checks

### Code Quality
- **100%** test coverage enforcement
- **Automatic** quality gates
- **Built-in** TDD/BDD support

### Team Collaboration
- **Clear** task states
- **Transparent** progress
- **Consistent** standards

## 🆘 Getting Help

### Quick Help
```bash
/task-work --help           # Command help
/task-work --examples       # See examples
/task-work --mode-help=tdd  # Mode details
```

### Documentation
- [Complete User Guide](AI-ENGINEER-USER-GUIDE.md)
- [Migration Guide](MIGRATION-GUIDE.md)
- [Command Reference](COMMAND_USAGE_GUIDE.md)
- [Quick Reference](../../.claude/TASK-WORKFLOW-QUICK-REFERENCE-V2.md)

### Common Issues
| Problem | Solution |
|---------|----------|
| Tests failing | Use `/task-work --fix-only` |
| Wrong mode | Re-run with different `--mode` |
| Low coverage | Check uncovered lines |

## 🎉 Start Building!

You now have everything you need to use AI Engineer v2.0:

1. **Create** tasks with clear requirements
2. **Work** on them with your preferred mode
3. **Complete** with confidence knowing quality is built-in

The unified workflow ensures every piece of code is tested, verified, and ready for production.

---

*"Implementation and testing are inseparable" - Start with `/task-create` and let `/task-work` handle the rest!*
