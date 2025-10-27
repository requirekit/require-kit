# Kanban Task Workflow - Quick Reference Card

## 🚀 Quick Start Commands

### Basic Workflow
```bash
/task-create "Task title" priority:high        # Create task → BACKLOG
/task-start TASK-XXX                          # Start work → IN_PROGRESS
/task-implement TASK-XXX test-first:true      # Generate code & tests
/task-test TASK-XXX                           # Run tests → IN_TESTING
/task-review TASK-XXX                         # Code review → IN_REVIEW
/task-complete TASK-XXX                       # Finish → COMPLETED
```

### View & Manage
```bash
/task-status                                  # View kanban board
/task-status filter:mine                      # Your tasks only
/task-view TASK-XXX                          # Task details
/task-block TASK-XXX "reason"                # Block task
/task-unblock TASK-XXX                       # Remove block
```

## 📊 Task States

```
BACKLOG → IN_PROGRESS → IN_TESTING → IN_REVIEW → COMPLETED
            ↓              ↓            ↓
         BLOCKED        BLOCKED      BLOCKED
```

## ✅ Quality Gates

| Gate | Threshold | Required |
|------|-----------|----------|
| Test Coverage | ≥80% | Yes |
| All Tests Pass | 100% | Yes |
| Performance | <30s | Yes |
| Documentation | Complete | No |

## 🔗 Linking Commands

```bash
/task-link-requirements TASK-XXX REQ-YYY      # Link EARS requirements
/task-link-bdd TASK-XXX BDD-YYY              # Link BDD scenarios
/task-link-github TASK-XXX issue:123         # Link GitHub issue
```

## 🧪 Test Commands by Language

### Python
```bash
/task-test TASK-XXX                          # Uses pytest automatically
mcp-code-checker:run_pytest_check            # Alternative MCP method
```

### JavaScript/TypeScript
```bash
/task-test TASK-XXX                          # Uses npm test
playwright:browser_snapshot                   # For E2E tests
```

### .NET
```bash
/task-test TASK-XXX                          # Uses dotnet test
```

## 📈 Status Indicators

- 📋 **BACKLOG** - Not started
- 🔄 **IN_PROGRESS** - Active work
- 🧪 **IN_TESTING** - Running tests
- 👀 **IN_REVIEW** - Awaiting approval
- ❌ **BLOCKED** - Cannot proceed
- ✅ **COMPLETED** - Done

## 🚦 Priority Levels

- 🔴 **CRITICAL** - Drop everything
- 🟠 **HIGH** - Important
- 🟡 **MEDIUM** - Normal
- 🟢 **LOW** - Nice to have

## 📝 Task File Location

```
tasks/
├── backlog/        # New tasks
├── in_progress/    # Active development
├── in_testing/     # Running tests
├── in_review/      # Code review
├── blocked/        # Failed tests or blocked
└── completed/      # Finished tasks
```

## ⚡ Common Workflows

### Feature Development
```bash
/task-create "New feature" → /task-start → /task-implement → /task-test → /task-review → /task-complete
```

### Bug Fix (Fast Track)
```bash
/task-create "Fix bug" priority:critical → /task-start → /task-test → /task-review checklist:quick → /task-complete
```

### Refactoring
```bash
/task-create "Refactor" → /task-test (baseline) → /task-start → /task-test (verify) → /task-review → /task-complete
```

## 🔥 Pro Tips

1. **Always run tests before marking complete**
2. **Link requirements for traceability**
3. **Use `test-first:true` for TDD**
4. **Document blockers immediately**
5. **Check `/task-status` daily**

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Tests not found | Check test file locations |
| Coverage too low | Add more tests or adjust threshold |
| Task stuck in blocked | Review blocking reason and resolve |
| Can't complete task | Ensure all tests pass first |

## 📊 Reports

```bash
/task-status report:standup              # Daily standup format
/task-status report:sprint               # Sprint summary
/task-status report:weekly               # Weekly metrics
/task-status export:csv                  # Export to spreadsheet
```

## 💡 Remember

**"No task is complete until tests pass!"** 

The system enforces quality through mandatory test verification. This prevents "implemented but not working" code from being marked as done.
