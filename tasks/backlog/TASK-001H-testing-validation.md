---
id: TASK-001H
title: "Testing and Validation"
created: 2025-10-19
status: backlog
priority: high
complexity: 4
parent_task: TASK-001
subtasks: []
estimated_hours: 3
---

# TASK-001H: Testing and Validation

## Description

Comprehensive testing of agentecflow installation and functionality across platforms and templates.

## Test Matrix

### Platform Testing

- [ ] macOS (Intel)
- [ ] macOS (Apple Silicon)
- [ ] Ubuntu 22.04
- [ ] Ubuntu 24.04
- [ ] Windows WSL (Ubuntu)
- [ ] Windows WSL (Debian)

### Template Testing

- [ ] default template
- [ ] react template
- [ ] python template
- [ ] typescript-api template
- [ ] maui-appshell template
- [ ] maui-navigationpage template
- [ ] dotnet-microservice template
- [ ] fullstack template

## Test Scenarios

### 1. Fresh Installation Test

```bash
# On each platform
cd /tmp
rm -rf ~/.agentecflow ~/.claude  # Clean state

# Install
git clone https://github.com/you/agentecflow.git
cd agentecflow
chmod +x installer/scripts/install.sh
./installer/scripts/install.sh

# Verify
ls -la ~/.agentecflow
ls -la ~/.claude
which agentecflow  # Should return path

# Expected time: <2 minutes
```

### 2. Template Initialization Test

```bash
# For EACH template
cd /tmp
mkdir test-{template}
cd test-{template}

agentecflow init {template}

# Verify structure
tree -L 2
ls -la .claude
ls -la tasks

# Should create:
# - tasks/{backlog,in_progress,in_review,blocked,completed}
# - .claude/{agents,commands,CLAUDE.md}
# - Stack-specific files

# Should NOT create:
# - docs/epics/
# - docs/features/
# - docs/requirements/
# - docs/bdd/
```

### 3. Command Execution Test

```bash
# In initialized project
/task-create "Test feature"

# Verify
cat tasks/backlog/TASK-001-test-feature.md

# Check frontmatter does NOT contain:
# - epic:
# - feature:
# - requirements:

# Run task-status
/task-status

# Should show kanban board without epic/feature columns
```

### 4. Quality Gate Test

```bash
# Create simple implementation task
/task-create "Add hello world function"

# Work on it (this is a smoke test, not full implementation)
# Just verify it starts correctly
/task-work TASK-001 --micro

# Verify phases execute:
# - Phase 1: Task Analysis
# - Phase 2: Implementation Planning
# - Phase 2.7: Complexity Evaluation
# Expected: AUTO_PROCEED mode (complexity 1)

# Don't need to complete - just verify it starts
```

### 5. Compilation Test (Per Stack)

```bash
# React
cd test-react
npm install
npm run build
npm test

# Python
cd test-python
python -m pytest tests/

# TypeScript API
cd test-typescript-api
npm install
npm run build
npm test

# .NET MAUI (AppShell)
cd test-maui-appshell
dotnet build
dotnet test

# .NET MAUI (NavigationPage)
cd test-maui-navigationpage
dotnet build
dotnet test

# .NET Microservice
cd test-dotnet-microservice
dotnet build
dotnet test

# Fullstack
cd test-fullstack
npm install  # Frontend
cd backend && pip install -r requirements.txt  # Backend
npm run build && python -m pytest
```

### 6. Uninstall Test

```bash
cd agentecflow
./installer/scripts/uninstall.sh

# Verify cleanup
[ ! -d ~/.agentecflow ] && echo "✓ Cleaned" || echo "✗ Not cleaned"
[ ! -L ~/.claude/commands ] && echo "✓ Symlinks removed" || echo "✗ Symlinks remain"
```

## Issue Tracking Template

Create GitHub issues for any failures:

```markdown
**Platform**: macOS 14.1 / Ubuntu 22.04 / Windows WSL
**Template**: react / python / etc.
**Test**: Installation / Template Init / Command Execution / etc.

**Expected**:
[What should happen]

**Actual**:
[What actually happened]

**Steps to Reproduce**:
1. ...
2. ...

**Error Output**:
```
[Paste error]
```

**Environment**:
- OS:
- Shell: bash / zsh / fish
- Python: 3.x
- Node: v20.x (if applicable)
- .NET: 8.0 (if applicable)
```

## Acceptance Criteria

### Installation

- [ ] Installs in <2 minutes on all platforms
- [ ] No errors during installation
- [ ] Symlinks created correctly
- [ ] `agentecflow` command available

### Templates

- [ ] All 8 templates initialize successfully
- [ ] Correct directory structure (no epic/feature/requirements)
- [ ] Stack-specific files created
- [ ] Compilation succeeds (where applicable)

### Commands

- [ ] `/task-create` works without epic/feature flags
- [ ] `/task-status` shows simplified kanban
- [ ] `/task-work` executes phases correctly
- [ ] Quality gates function (Phase 2.5, 4.5)
- [ ] Design-first flags work (--design-only, --implement-only)

### Quality

- [ ] No broken links in documentation
- [ ] No references to removed features
- [ ] Error messages clear and helpful
- [ ] Performance acceptable (<2s command response)

## Test Results Template

```markdown
# Agentecflow Testing Results

**Date**: YYYY-MM-DD
**Version**: 1.0.0
**Tester**: Name

## Platform Results

| Platform | Installation | Templates | Commands | Issues |
|----------|-------------|-----------|----------|--------|
| macOS Intel | ✅ | ✅ | ✅ | 0 |
| macOS M1 | ✅ | ⚠️ (1 issue) | ✅ | 1 |
| Ubuntu 22.04 | ✅ | ✅ | ✅ | 0 |
| Ubuntu 24.04 | ✅ | ✅ | ✅ | 0 |
| Windows WSL | ✅ | ❌ (2 issues) | ⚠️ (1 issue) | 3 |

## Template Results

| Template | Init | Build | Tests | Issues |
|----------|------|-------|-------|--------|
| default | ✅ | N/A | N/A | 0 |
| react | ✅ | ✅ | ✅ | 0 |
| python | ✅ | ✅ | ✅ | 0 |
| typescript-api | ✅ | ✅ | ⚠️ | 1 |
| maui-appshell | ✅ | ✅ | ✅ | 0 |
| maui-navigationpage | ✅ | ✅ | ✅ | 0 |
| dotnet-microservice | ✅ | ✅ | ✅ | 0 |
| fullstack | ✅ | ⚠️ | ⚠️ | 2 |

## Issues Found

[List all issues with links to GitHub issues]

## Recommendations

[Any improvements needed before release]
```

## Estimated Time

3 hours (across all platforms and templates)

## Notes

- **Don't block on minor issues** - Create GitHub issues, move forward
- **Focus on critical path** - Installation, task-create, task-work
- **Automate where possible** - Create test scripts for repeated runs
- **Document thoroughly** - Test results inform v1.0 release decision
