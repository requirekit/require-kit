# Integration Guide: require-kit and guardkit

**Version**: 1.0.0
**Last Updated**: 2025-11-03
**Status**: Production

## Prerequisites

- **Python 3.10 or later** (required by both require-kit and guardkit)
- pip (Python package installer)
- git (for repository cloning)
- bash shell (macOS, Linux, or Windows WSL2)

Both packages require Python 3.10+ for ecosystem consistency. This ensures compatibility with modern Python features (PEP 604 union types) and alignment with AI/ML tooling standards.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Overview](#overview)
- [Integration Architecture](#integration-architecture)
- [Installation Scenarios](#installation-scenarios)
- [Feature Availability Matrix](#feature-availability-matrix)
- [Common Workflows](#common-workflows)
- [Troubleshooting](#troubleshooting)
- [Migration Guides](#migration-guides)

---

## Overview

### What is require-kit?

**require-kit** is a standalone requirements management toolkit that helps teams capture, formalize, and organize software requirements using industry-proven methodologies:

- **EARS Notation**: Clear, unambiguous requirements specification
- **BDD/Gherkin Scenarios**: Testable acceptance criteria
- **Epic/Feature Hierarchy**: Structured project organization
- **Technology Agnostic**: Works with any implementation system or PM tool

**Use require-kit when you need**:
- Clear requirements documentation
- Requirements traceability
- BDD scenario generation
- PM tool export capabilities
- Requirements-driven development process

### What is guardkit?

**guardkit** is a standalone task execution workflow system that provides structured implementation, testing, and quality gates:

- **Task Execution**: TDD-driven implementation workflow
- **Quality Gates**: Automated testing, coverage, and code review
- **Architectural Review**: Pattern compliance and design validation
- **Test Orchestration**: Comprehensive test execution and reporting

**Use guardkit when you need**:
- Structured implementation workflow
- Automated quality gates
- Test-driven development
- Code review and architectural compliance
- Rapid task execution

### When to Use Which?

```
Decision Tree:
├── Do you need requirements documentation?
│   ├── Yes → Start with require-kit
│   └── No → Consider guardkit only
│
├── Do you need task execution workflow?
│   ├── Yes → Use guardkit
│   └── No → require-kit only is sufficient
│
└── Do you need full requirements-to-implementation traceability?
    ├── Yes → Use both (full integration)
    └── No → Use standalone package(s)
```

### Bidirectional Optional Integration

Both packages are **fully functional independently** with **no hard dependencies**:

- **require-kit**: Works standalone, optionally enhanced by guardkit
- **guardkit**: Works standalone, optionally enhanced by require-kit
- **Integration**: Automatic detection via marker files when both installed
- **No Lock-In**: Install or remove either package without affecting the other

This architecture provides maximum flexibility for teams to adopt the workflow that fits their needs.

---

## Integration Architecture

### Marker File Detection

Both packages detect each other automatically using marker files in `~/.agentecflow/`:

```bash
~/.agentecflow/
├── require-kit.marker          # Created when require-kit installed
├── guardkit.marker           # Created when guardkit installed
├── bin/                        # Shared command executables
└── lib/                        # Shared library code
```

**How it works**:

1. **Installation**: Each package creates its marker file during installation
2. **Detection**: Commands check for marker files at runtime
3. **Feature Enhancement**: When both markers exist, integration features activate
4. **Graceful Degradation**: Missing marker = standalone mode, no errors

**Check your installation**:

```bash
# List installed packages
ls ~/.agentecflow/*.marker

# Expected outputs:
# require-kit only:  require-kit.marker
# guardkit only:   guardkit.marker
# Both integrated:   require-kit.marker + guardkit.marker
```

### Dependency Inversion Principle

The integration follows the Dependency Inversion Principle (DIP) to avoid circular dependencies:

```
High-Level Module: require-kit
    ├── Requirements Gathering
    ├── EARS Formalization
    ├── BDD Scenario Generation
    ├── Task Specification Generation
    └── Outputs → PM Tools, guardkit (when installed)

Low-Level Module: guardkit
    ├── Task Execution
    ├── Quality Gates
    ├── Test Orchestration
    └── Inputs ← Task Specifications (from require-kit or PM tools)
```

**Key Principle**: guardkit does NOT look "up" to require-kit. The data flows one direction:

1. **require-kit** generates requirements, BDD scenarios, and task specifications
2. **guardkit** executes tasks using specifications from any source
3. **No circular dependency**: guardkit never calls require-kit commands

### Why BDD Mode was Removed from guardkit

**Historical Context**: Early versions of guardkit included a "BDD mode" that would call require-kit commands to generate feature files during task execution.

**Problem**: This violated DIP by making the lower-level module (guardkit) depend on the higher-level module (require-kit):

```
VIOLATION (Old Design):
guardkit → calls → require-kit commands
(lower)               (higher)
```

**Solution**: BDD mode was removed. The correct flow is:

```
CORRECT (Current Design):
require-kit → generates → BDD scenarios → consumed by → guardkit tests
(higher)                  (artifact)                     (lower)
```

**For Users**: If you need BDD-driven workflows:

1. Use `/generate-bdd` in require-kit to create scenarios
2. Export scenarios to your test framework
3. Execute tests with `/task-work` in guardkit
4. guardkit uses the BDD scenarios as acceptance criteria (data flow, not code dependency)

### Unidirectional Data Flow

```
┌─────────────────────────────────────────────────────────┐
│ require-kit (Requirements Management)                   │
│ ┌─────────────┐   ┌──────────────┐   ┌──────────────┐ │
│ │Requirements │──→│ BDD Scenarios│──→│Task Specs    │ │
│ └─────────────┘   └──────────────┘   └──────────────┘ │
└────────────────────────────┬────────────────────────────┘
                             │ (data artifacts)
                             ↓
┌─────────────────────────────────────────────────────────┐
│ guardkit (Task Execution)                             │
│ ┌─────────────┐   ┌──────────────┐   ┌──────────────┐ │
│ │Task Work    │──→│ Quality Gates│──→│Completion    │ │
│ └─────────────┘   └──────────────┘   └──────────────┘ │
└─────────────────────────────────────────────────────────┘

Alternative Sources:
┌─────────────────┐
│ PM Tools        │──→ Task Specs ──→ guardkit
│ (Jira, Linear) │
└─────────────────┘
```

---

## Installation Scenarios

### Scenario 1: require-kit Only

**Use Case**: Requirements team without implementation workflow, or teams using external PM tools for task execution.

**Installation**:

```bash
git clone https://github.com/requirekit/require-kit.git
cd require-kit
./installer/scripts/install.sh
```

**Verification**:

```bash
ls ~/.agentecflow/require-kit.marker
# Should exist

/gather-requirements --version
# Should show require-kit version
```

**Available Commands**:

```bash
# Requirements Management
/gather-requirements          # Interactive Q&A
/formalize-ears              # Convert to EARS notation
/generate-bdd                # Generate Gherkin scenarios

# Epic/Feature Management
/epic-create "Title"
/feature-create "Title" epic:EPIC-XXX
/hierarchy-view EPIC-XXX

# Export
/feature-sync FEAT-XXX --jira        # Export to Jira
/feature-sync FEAT-XXX --linear      # Export to Linear
```

**Output Artifacts**:

- `docs/requirements/REQ-XXX.md` - EARS requirements
- `docs/bdd/BDD-XXX.feature` - Gherkin scenarios
- `docs/epics/EPIC-XXX.md` - Epic specifications
- `docs/features/FEAT-XXX.md` - Feature specifications
- PM tool exports (Jira tickets, Linear issues, etc.)

**What's NOT Available**:

- Task execution workflow (`/task-work` command)
- Automated quality gates
- Test orchestration
- Code review automation

### Scenario 2: guardkit Only

**Use Case**: Lean startup, rapid iteration, teams without formal requirements process.

**Installation**:

```bash
git clone https://github.com/guardkit/guardkit.git
cd guardkit
./installer/scripts/install.sh
```

**Verification**:

```bash
ls ~/.agentecflow/guardkit.marker
# Should exist

/task-work --version
# Should show guardkit version
```

**Available Commands**:

```bash
# Task Management
/task-create "Title"
/task-work TASK-XXX
/task-work TASK-XXX --micro          # Micro-task workflow
/task-complete TASK-XXX

# Task States
/task-status                         # Show all tasks
/task-status TASK-XXX               # Show specific task
/task-block TASK-XXX "reason"       # Block task
/task-unblock TASK-XXX              # Unblock task
```

**Output Artifacts**:

- `tasks/backlog/TASK-XXX.md` - Task files
- `tasks/in_progress/TASK-XXX.md` - Active tasks
- `tasks/completed/TASK-XXX.md` - Completed tasks
- Test results and coverage reports
- Code review reports

**What's NOT Available**:

- EARS requirements formalization
- BDD scenario generation
- Epic/feature hierarchy
- Requirements traceability
- PM tool export

### Scenario 3: Full Integration

**Use Case**: Enterprise teams needing complete requirements-to-implementation traceability.

**Installation (Either Order)**:

```bash
# Option A: Install require-kit first
git clone https://github.com/requirekit/require-kit.git
cd require-kit
./installer/scripts/install.sh

cd ..
git clone https://github.com/guardkit/guardkit.git
cd guardkit
./installer/scripts/install.sh

# Option B: Install guardkit first (same result)
```

**Verification**:

```bash
ls ~/.agentecflow/*.marker
# Should show: require-kit.marker + guardkit.marker

/gather-requirements --version
/task-work --version
# Both should respond
```

**Available Commands**: ALL commands from both packages

**Enhanced Features**:

- `/task-work` loads requirements context from require-kit
- `/feature-generate-tasks` automatically creates executable tasks
- Full traceability: REQ → BDD → FEAT → TASK → Code
- Quality gates verify against BDD acceptance criteria

**Output Artifacts**: All artifacts from both packages, fully linked

---

## Feature Availability Matrix

| Feature | require-kit Only | guardkit Only | Both Integrated |
|---------|------------------|-----------------|-----------------|
| **Requirements Management** |
| EARS Requirements | ✅ Full | ❌ | ✅ Full |
| Requirements Gathering | ✅ Interactive | ❌ | ✅ Interactive |
| Requirements Traceability | ✅ Full | ❌ | ✅ Enhanced |
| **BDD/Testing** |
| BDD Scenario Generation | ✅ Gherkin | ❌ | ✅ Gherkin |
| BDD-Driven Testing | ⚠️ Manual | ⚠️ Manual | ✅ Automated |
| Test Execution | ❌ | ✅ Full | ✅ Full |
| Test Coverage | ❌ | ✅ ≥80% | ✅ ≥80% |
| **Project Organization** |
| Epic Management | ✅ Full | ❌ | ✅ Full |
| Feature Management | ✅ Full | ❌ | ✅ Full |
| Task Management | ⚠️ Specs Only | ✅ Full | ✅ Enhanced |
| Hierarchy View | ✅ Epic→Feature | ⚠️ Task Only | ✅ Epic→Feature→Task |
| **Task Execution** |
| Task Workflow | ❌ | ✅ Full | ✅ Full |
| TDD Mode | ❌ | ✅ | ✅ |
| Micro-Task Mode | ❌ | ✅ | ✅ |
| Quality Gates | ❌ | ✅ Full | ✅ Enhanced |
| **Code Quality** |
| Architectural Review | ❌ | ✅ Full | ✅ Enhanced |
| Code Review | ❌ | ✅ SOLID/DRY | ✅ SOLID/DRY |
| Plan Audit | ❌ | ✅ Scope Creep | ✅ Scope Creep |
| Complexity Evaluation | ❌ | ✅ 1-10 | ✅ 1-10 |
| **Integration** |
| PM Tool Export | ✅ Jira, Linear, GitHub, Azure | ❌ | ✅ Full |
| Requirements Context | ✅ Local | ❌ | ✅ Injected to Tasks |
| BDD → Task Link | ⚠️ Manual | ❌ | ✅ Automatic |

**Legend**:
- ✅ = Fully available
- ⚠️ = Partially available or manual process
- ❌ = Not available

---

## Common Workflows

### Workflow 1: Requirements-Driven Development (Full Integration)

**Prerequisites**: Both require-kit and guardkit installed

**Complete Workflow**:

```bash
# Phase 1: Requirements Gathering (require-kit)
/gather-requirements
# Interactive Q&A captures complete requirements

# Phase 2: Formalize Requirements (require-kit)
/formalize-ears
# Output: docs/requirements/REQ-001.md (EARS notation)

# Phase 3: Create Epic (require-kit)
/epic-create "User Authentication System"
# Output: docs/epics/EPIC-001.md

# Phase 4: Create Feature (require-kit)
/feature-create "Login Functionality" epic:EPIC-001
# Output: docs/features/FEAT-001.md

# Phase 5: Generate BDD Scenarios (require-kit)
/generate-bdd FEAT-001
# Output: docs/bdd/BDD-001.feature (Gherkin scenarios)

# Phase 6: Generate Task Specifications (require-kit)
/feature-generate-tasks FEAT-001
# Output: tasks/backlog/TASK-001.md (with links to REQ, BDD, FEAT)

# Phase 7: Execute Task (guardkit)
/task-work TASK-001
# - Loads requirements context from REQ-001
# - References BDD-001 for acceptance criteria
# - Implements with TDD workflow
# - Runs quality gates
# Output: Implementation with test coverage

# Phase 8: Complete Task (guardkit)
/task-complete TASK-001
# - Verifies all tests passing
# - Confirms coverage ≥80%
# - Archives with full traceability
```

**Result**: Complete traceability chain:

```
REQ-001 → BDD-001 → FEAT-001 → TASK-001 → Implementation
(EARS)    (Gherkin) (Feature)  (Task)     (Code + Tests)
```

### Workflow 2: Lean Startup (guardkit Only)

**Prerequisites**: guardkit only

**Rapid Iteration Workflow**:

```bash
# Create task from user story or issue
/task-create "Add email validation to signup form"
# Output: tasks/backlog/TASK-042.md

# Execute immediately
/task-work TASK-042
# - TDD implementation
# - Quality gates (tests, coverage)
# - No requirements overhead

# Complete quickly
/task-complete TASK-042
# Output: Working feature with tests

# Iterate fast
/task-create "Improve validation error messages"
/task-work TASK-043
/task-complete TASK-043
```

**When to Add require-kit**: When you need to scale, add compliance, or require traceability:

```bash
# Install require-kit
cd ../require-kit
./installer/scripts/install.sh

# Now add requirements retroactively
/gather-requirements  # Document existing features
/formalize-ears      # Create EARS requirements
/epic-create "User Management"
/feature-create "Signup Validation" epic:EPIC-001

# Link existing tasks to features
# Edit tasks/completed/TASK-042.md frontmatter:
# feature: FEAT-001

# Continue with full workflow for new features
```

### Workflow 3: Requirements Export to PM Tools (require-kit Only)

**Prerequisites**: require-kit only

**PM Tool Integration Workflow**:

```bash
# Gather and formalize requirements
/gather-requirements
/formalize-ears
# Output: docs/requirements/REQ-001.md

# Create epic and features
/epic-create "E-Commerce Platform"
/feature-create "Shopping Cart" epic:EPIC-001
/feature-create "Checkout Process" epic:EPIC-001

# Generate BDD acceptance criteria
/generate-bdd FEAT-001
/generate-bdd FEAT-002

# Generate task specifications
/feature-generate-tasks FEAT-001
/feature-generate-tasks FEAT-002

# Export to Jira
/feature-sync FEAT-001 --jira
/feature-sync FEAT-002 --jira
# Output: Jira tickets with:
# - User story from feature description
# - Acceptance criteria from BDD scenarios
# - Linked requirements (REQ-001)
# - Linked epic (EPIC-001)

# Export to Linear
/feature-sync FEAT-001 --linear
# Output: Linear issue with full traceability

# Your team implements in Jira/Linear
# No need for guardkit if you have existing PM workflow
```

**Result**: Requirements managed in require-kit, execution in external PM tool.

---

## Troubleshooting

### Integration Not Detected

**Symptoms**:
- Commands from one package don't recognize the other
- Feature availability doesn't show integration features
- Commands work but lack enhanced context

**Solutions**:

1. **Check marker files exist**:

```bash
ls -la ~/.agentecflow/*.marker

# Should see both:
# require-kit.marker
# guardkit.marker
```

2. **Verify marker file format**:

```bash
cat ~/.agentecflow/require-kit.marker

# Expected content:
# {
#   "package": "require-kit",
#   "version": "1.0.0",
#   "installed_at": "2025-11-03T10:00:00Z"
# }
```

3. **Re-run installers if marker files missing**:

```bash
cd /path/to/require-kit
./installer/scripts/install.sh --repair

cd /path/to/guardkit
./installer/scripts/install.sh --repair
```

4. **Check for conflicting installations**:

```bash
# Only one installation should exist
find ~ -name "require-kit.marker" -o -name "guardkit.marker"

# If multiple found, uninstall and reinstall
```

### Commands Not Available

**Symptoms**:
- `/command-name` responds with "command not found"
- Shell doesn't recognize commands

**Solutions**:

1. **Verify PATH includes agentecflow bin**:

```bash
echo $PATH | grep agentecflow

# Should show: ...:/Users/yourusername/.agentecflow/bin:...
```

2. **Add to PATH if missing** (add to `~/.bashrc` or `~/.zshrc`):

```bash
export PATH="$HOME/.agentecflow/bin:$PATH"

# Reload shell
source ~/.bashrc  # or source ~/.zshrc
```

3. **Check command executables exist**:

```bash
ls -la ~/.agentecflow/bin/

# Should show command wrappers for both packages
```

4. **Restart shell/terminal**:

```bash
# Sometimes needed for PATH changes
exec $SHELL
```

### BDD Mode Questions

**Question**: "Why doesn't guardkit have a BDD mode anymore?"

**Answer**: BDD mode was intentionally removed to respect the Dependency Inversion Principle and avoid circular dependencies between packages.

**The Old Design (Violated DIP)**:

```
guardkit /task-work --bdd
    ↓ (calls)
require-kit /generate-bdd
    ↓ (generates)
BDD scenarios
    ↓ (used by)
guardkit tests
```

This made guardkit (lower-level) depend on require-kit (higher-level), which is a DIP violation.

**The Correct Design (Current)**:

```
require-kit /generate-bdd
    ↓ (generates)
BDD scenarios (artifact)
    ↓ (consumed by)
guardkit tests (data dependency only)
```

**How to Use BDD with Integration**:

1. **Generate BDD scenarios first** (require-kit):

```bash
/generate-bdd FEAT-001
# Output: docs/bdd/BDD-001.feature
```

2. **Reference in task specifications**:

```yaml
# tasks/backlog/TASK-001.md frontmatter
bdd_scenarios: [BDD-001]
```

3. **Execute task** (guardkit loads BDD as acceptance criteria):

```bash
/task-work TASK-001
# guardkit reads BDD-001.feature for acceptance criteria
# implements tests based on scenarios
# no code dependency on require-kit
```

**Restoration Documentation**: If your team requires the old BDD mode behavior (accepting the DIP violation tradeoff), see `docs/architecture/bdd-mode-restoration.md` (coming in future release).

### Feature Detection Issues

**Symptoms**:
- Feature matrix shows incorrect availability
- Commands behave unexpectedly

**Diagnostic Commands**:

```bash
# Check feature detection
python3 -c "
import sys
sys.path.insert(0, '$HOME/.agentecflow/lib')
from feature_detection import get_available_features
import json
print(json.dumps(get_available_features(), indent=2))
"

# Expected output:
# {
#   "require_kit": true,
#   "guardkit": true,
#   "integration": true,
#   "features": {
#     "requirements": true,
#     "bdd": true,
#     "task_execution": true,
#     ...
#   }
# }
```

**Solutions**:

1. **If feature detection fails**, verify Python path:

```bash
ls ~/.agentecflow/lib/feature_detection.py
# Should exist
```

2. **Check for multiple installations**:

```bash
find ~ -type d -name ".agentecflow" 2>/dev/null

# Should only find one: ~/.agentecflow
```

3. **Clear and reinstall**:

```bash
rm -rf ~/.agentecflow
# Reinstall both packages
```

---

## Migration Guides

### From Monolithic ai-engineer to Split Packages

**Context**: The original `ai-engineer` system was split into `require-kit` and `guardkit` to provide standalone, composable packages.

**Migration Steps**:

1. **Uninstall old system**:

```bash
# If you have old ai-engineer installed
rm -rf ~/.agentecflow
# or use uninstaller if provided
```

2. **Determine your needs**:

- Requirements + Implementation → Install both packages
- Requirements only → Install require-kit
- Implementation only → Install guardkit

3. **Install new packages** (see Installation Scenarios above)

4. **Migrate existing files**:

```bash
# Old structure:
# .ai-engineer/requirements/
# .ai-engineer/bdd/
# .ai-engineer/tasks/

# New structure:
# docs/requirements/
# docs/bdd/
# tasks/

# Copy files if needed
cp -r ~/.ai-engineer/requirements docs/
cp -r ~/.ai-engineer/bdd docs/
cp -r ~/.ai-engineer/tasks tasks/
```

5. **Verify commands work**:

```bash
/gather-requirements --version
/task-work --version
```

**Backward Compatibility**: Old marker files and command names are NOT compatible. Clean installation required.

### From require-kit Standalone to Full Integration

**When to Migrate**: When you want to add implementation workflow and quality gates to your requirements process.

**Migration Steps**:

1. **Install guardkit**:

```bash
cd /path/to/guardkit
./installer/scripts/install.sh
```

2. **Verify integration**:

```bash
ls ~/.agentecflow/*.marker
# Should show both markers
```

3. **No data migration needed**: All existing requirements, BDD, epics, and features remain unchanged.

4. **New capabilities available immediately**:

```bash
# Tasks now link to requirements
/feature-generate-tasks FEAT-001
# Output: tasks with requirements context

# Execute with full context
/task-work TASK-001
# Loads REQ-001 and BDD-001 automatically
```

5. **Update workflows**: Start using combined workflow (see Workflow 1 above).

**No Breaking Changes**: All existing require-kit commands continue to work identically.

### From guardkit Standalone to Full Integration

**When to Migrate**: When you want to add requirements traceability and BDD scenarios to your task execution workflow.

**Migration Steps**:

1. **Install require-kit**:

```bash
cd /path/to/require-kit
./installer/scripts/install.sh
```

2. **Verify integration**:

```bash
ls ~/.agentecflow/*.marker
# Should show both markers
```

3. **Optionally add requirements to existing tasks**:

```bash
# For critical/completed tasks, add requirements retroactively
/gather-requirements
# Answer questions about existing feature

/formalize-ears
# Output: docs/requirements/REQ-010.md

# Edit completed task frontmatter
# tasks/completed/TASK-042.md:
# requirements: [REQ-010]
```

4. **Use full workflow for new features**:

```bash
# New features start with requirements
/gather-requirements
/formalize-ears
/epic-create "Feature Area"
/feature-create "New Feature" epic:EPIC-001
/generate-bdd FEAT-001
/feature-generate-tasks FEAT-001

# Execute as before, now with context
/task-work TASK-043
```

**No Breaking Changes**: All existing guardkit commands continue to work identically. Existing tasks without requirements continue to execute normally.

---

## Additional Resources

### Documentation

- **require-kit**: [README.md](../README.md), [CLAUDE.md](../CLAUDE.md)
- **guardkit**: [guardkit README](https://github.com/guardkit/guardkit)
- **Architecture**: [docs/architecture/bidirectional-integration.md](architecture/bidirectional-integration.md)

### Command References

- **require-kit Commands**: See `.claude/commands/` for command specifications
- **guardkit Commands**: See guardkit repository `.claude/commands/`

### Support

- **GitHub Issues**: [require-kit issues](https://github.com/requirekit/require-kit/issues)
- **GitHub Issues**: [guardkit issues](https://github.com/guardkit/guardkit/issues)
- **Email**: support@yourorganization.com

---

## Terminology

**Consistent terminology across documentation**:

- **Package names**: require-kit, guardkit (lowercase, hyphenated)
- **Files**: lowercase-with-hyphens.md
- **Package**: Use "package" not "tool" or "system"
- **Integration**: Bidirectional optional integration (not "dependency")
- **Marker**: Detection mechanism (not "flag" or "config")

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-03
**Authoritative Source**: This guide in require-kit repository
**guardkit Copy**: Linked from guardkit repository (not duplicated)
