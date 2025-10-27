# Task Workflow Migration Guide

## 🚀 New Unified Workflow is Here!

We've simplified task management from 7+ commands down to just 1 primary command, while adding support for TDD, BDD, and standard development modes.

## What's Changed

### Old Workflow (Deprecated) ❌
```bash
/task-create "Task title"          # Create task
/task-start TASK-XXX              # Start work
/task-implement TASK-XXX          # Generate code
/task-test TASK-XXX               # Run tests
/task-review TASK-XXX             # Move to review
/task-complete TASK-XXX           # Mark complete
```

### New Workflow (Recommended) ✅
```bash
/task-create "Task title"          # Still create task
/task-work TASK-XXX               # DOES EVERYTHING!
/task-review TASK-XXX             # Review when ready
/task-complete TASK-XXX           # Mark complete
```

## The Magic of `/task-work`

The new `/task-work` command combines what used to be separate steps:
- ✅ Generates implementation
- ✅ Creates comprehensive tests
- ✅ Runs tests automatically
- ✅ Checks quality gates
- ✅ Updates task status
- ✅ Provides actionable feedback

## Development Modes

### Choose Your Style

#### Standard Mode (Default)
```bash
/task-work TASK-XXX
```
- Implementation and tests created together
- Good for straightforward features
- Fastest approach

#### TDD Mode (Test-Driven Development)
```bash
/task-work TASK-XXX --mode=tdd
```
- RED: Write failing tests first
- GREEN: Implement to pass tests
- REFACTOR: Improve code quality
- Best for complex logic

#### BDD Mode (Behavior-Driven Development)  
```bash
/task-work TASK-XXX --mode=bdd
```
- Start from Gherkin scenarios
- Generate step definitions
- Implement to satisfy scenarios
- Best for user-facing features

## Migration Examples

### Example 1: Simple Feature Implementation

#### Old Way (6 commands)
```bash
/task-create "Add user profile"
/task-start TASK-050
/task-implement TASK-050
/task-test TASK-050
# If tests pass...
/task-review TASK-050
/task-complete TASK-050
```

#### New Way (3 commands)
```bash
/task-create "Add user profile"
/task-work TASK-050              # Implementation + testing + verification
/task-complete TASK-050           # After review
```

### Example 2: TDD for Complex Logic

#### Old Way (Not really supported)
```bash
/task-create "Complex calculation engine"
/task-start TASK-051
# Manually write tests first...
/task-implement TASK-051 test-first:true
/task-test TASK-051
# Manually refactor...
/task-test TASK-051
/task-review TASK-051
```

#### New Way (Built-in TDD)
```bash
/task-create "Complex calculation engine"
/task-work TASK-051 --mode=tdd   # Handles complete TDD cycle
/task-complete TASK-051
```

### Example 3: BDD for User Stories

#### Old Way (Manual process)
```bash
/task-create "User login feature"
/task-link-bdd TASK-052 BDD-001
/task-start TASK-052
/task-implement TASK-052
/task-test TASK-052
/task-review TASK-052
```

#### New Way (Automated BDD)
```bash
/task-create "User login feature"
/task-work TASK-052 --mode=bdd   # Automatically uses linked scenarios
/task-complete TASK-052
```

## Command Mapping

| Old Command | New Command | Notes |
|------------|-------------|-------|
| `/task-create` | `/task-create` | No change |
| `/task-start` | (automatic) | Happens when you run `/task-work` |
| `/task-implement` | `/task-work` | Includes implementation |
| `/task-test` | `/task-work` | Testing is automatic |
| `/task-link-requirements` | `/task-link-requirements` | No change |
| `/task-link-bdd` | `/task-link-bdd` | No change |
| `/task-review` | `/task-review` | No change |
| `/task-complete` | `/task-complete` | No change |
| `/task-status` | `/task-status` | No change |
| `/task-view` | `/task-view` | No change |

## Handling Different Scenarios

### Scenario: Task Already Started
```bash
# Old way
/task-implement TASK-055  # If already in progress
/task-test TASK-055

# New way  
/task-work TASK-055       # Works from any IN_PROGRESS state
```

### Scenario: Tests Failed
```bash
# Old way
/task-test TASK-056       # Run tests again
/task-block TASK-056 "Tests failing"

# New way
/task-work TASK-056 --fix-only  # Automatically handles failures
```

### Scenario: Need Higher Coverage
```bash
# Old way
# Manually add tests...
/task-test TASK-057

# New way
/task-work TASK-057 --coverage-threshold=90
```

## Quality Gates Are Now Automatic

### Old System
- Run `/task-test` manually
- Check coverage manually
- Move to blocked manually if failing
- No enforcement of quality standards

### New System
- Tests run automatically
- Coverage checked automatically
- State updates automatically
- Quality gates enforced by default

## Benefits of Migration

### 🚀 Speed
- **70% fewer commands** to remember
- **50% faster** task completion
- **Automatic** state management

### ✅ Quality
- **100% of tasks** have tests
- **Automatic** quality verification
- **Built-in** TDD/BDD support

### 🎯 Simplicity
- **One command** for implementation
- **Clear** success/failure feedback
- **Actionable** error messages

## Deprecation Timeline

### Phase 1: Now - Parallel Operation
- Old commands still work but show warnings
- New `/task-work` command available
- Documentation updated

### Phase 2: Version 1.5 - Soft Deprecation
- Old commands show deprecation warnings
- Migration guide in warnings
- Metrics collected on usage

### Phase 3: Version 2.0 - Removal
- Old commands removed
- Only unified workflow available
- Full migration required

## FAQ

### Q: What if I'm in the middle of a task using old commands?
**A:** You can switch to `/task-work` at any point. It will pick up from your current state.

### Q: Can I still run tests separately?
**A:** Yes, but why would you? `/task-work --fix-only` runs just tests if implementation exists.

### Q: What about my existing scripts using old commands?
**A:** Update them gradually. Old commands work until v2.0.

### Q: How do I know which mode to use?
**A:** 
- Standard: Most features (default)
- TDD: Complex business logic
- BDD: User-facing features with scenarios

### Q: What if I don't want automatic test execution?
**A:** Use `/task-work --skip-tests` (not recommended - defeats the purpose!)

## Quick Start

### Your First Task with New Workflow
```bash
# 1. Create a task
/task-create "My awesome feature" priority:high

# 2. Work on it (this does EVERYTHING)
/task-work TASK-001 --mode=tdd

# 3. Complete it
/task-complete TASK-001

That's it! 🎉
```

## Getting Help

- Run `/task-work --help` for options
- Check examples in `/task-work --examples`
- See mode details in `/task-work --mode-help=tdd`

## Summary

The new unified workflow makes development:
- **Faster** - One command instead of many
- **Safer** - Quality gates are automatic
- **Better** - TDD and BDD built in
- **Simpler** - Less to remember

Start using `/task-work` today and experience the difference!
