---
id: REQ-002
title: "Delete Agentecflow Features from require-kit"
created: 2025-10-27
status: backlog
priority: high
complexity: 6
parent_task: none
subtasks:
  - REQ-002A
  - REQ-002B
  - REQ-002C
  - REQ-002D
  - REQ-002E
---

# REQ-002: Delete Agentecflow Features from require-kit

## Overview

The require-kit repository currently contains the ENTIRE ai-engineer/agentecflow codebase. We need to **delete** all task execution, quality gates, templates, and stack-specific features, keeping ONLY requirements management features.

## Current State

The repo contains everything:
- ✅ Requirements commands (gather-requirements, formalize-ears, generate-bdd)
- ❌ Task execution commands (task-create, task-work, task-complete)
- ❌ Quality gate agents (architectural-reviewer, test-verifier, etc.)
- ❌ Stack templates (react, python, maui, etc.)
- ❌ UX integration (figma-to-react, zeplin-to-maui)

## Target State

After deletion, repo should contain ONLY:
- ✅ Requirements commands (8 commands)
- ✅ Requirements agents (2 agents)
- ✅ Epic/feature management
- ✅ Requirements documentation templates
- ❌ No task execution
- ❌ No quality gates
- ❌ No stack templates
- ❌ No UX integration

## What to Delete

### Commands to DELETE (6 commands)

```bash
❌ task-create.md
❌ task-work.md
❌ task-complete.md
❌ task-status.md
❌ task-refine.md
❌ task-sync.md
❌ debug.md
❌ figma-to-react.md
❌ zeplin-to-maui.md
❌ mcp-zeplin.md
❌ portfolio-dashboard.md (if task-focused)
```

### Commands to KEEP (8-9 commands)

```bash
✅ gather-requirements.md
✅ formalize-ears.md
✅ generate-bdd.md
✅ epic-create.md
✅ epic-status.md
✅ epic-sync.md
✅ epic-generate-features.md (?)
✅ feature-create.md
✅ feature-status.md
✅ feature-sync.md
✅ feature-generate-tasks.md (?) - evaluate
✅ hierarchy-view.md
```

### Agents to DELETE (14 agents)

```bash
❌ architectural-reviewer.md
❌ test-verifier.md
❌ test-orchestrator.md
❌ code-reviewer.md
❌ task-manager.md
❌ complexity-evaluator.md
❌ build-validator.md
❌ debugging-specialist.md
❌ devops-specialist.md
❌ database-specialist.md
❌ security-specialist.md
❌ pattern-advisor.md
❌ python-mcp-specialist.md
❌ figma-react-orchestrator.md
❌ zeplin-maui-orchestrator.md
```

### Agents to KEEP (2 agents)

```bash
✅ requirements-analyst.md
✅ bdd-generator.md
```

### Templates to DELETE (ALL stack templates)

```bash
❌ installer/global/templates/react/
❌ installer/global/templates/python/
❌ installer/global/templates/typescript-api/
❌ installer/global/templates/maui-appshell/
❌ installer/global/templates/maui-navigationpage/
❌ installer/global/templates/dotnet-microservice/
❌ installer/global/templates/fullstack/
❌ installer/global/templates/default/ (if contains task workflow)
```

### Library Modules to DELETE

```bash
❌ installer/global/commands/lib/ (entire directory if task-focused)
   Or selectively delete:
   ❌ checkpoint_display.py
   ❌ plan_persistence.py
   ❌ plan_modifier.py
   ❌ review_modes.py
   ❌ upfront_complexity_adapter.py
   ❌ plan_audit.py
   ❌ git_state_helper.py (if task-specific)
   ❌ micro_task_workflow.py
   ❌ spec_drift_detector.py
   ❌ All quality gate modules

   ✅ Keep only: feature_generator.py (if exists)
```

### Documentation to DELETE

```bash
❌ docs/guides/agentecflow-lite-workflow.md
❌ docs/guides/creating-local-templates.md
❌ docs/guides/iterative-refinement-guide.md
❌ docs/guides/maui-template-selection.md
❌ docs/guides/mcp-optimization-guide.md
❌ docs/workflows/complexity-management-workflow.md
❌ docs/workflows/design-first-workflow.md
❌ docs/workflows/ux-design-integration-workflow.md
❌ docs/patterns/domain-layer-pattern.md
❌ All template-specific documentation
```

### Documentation to KEEP

```bash
✅ docs/requirements/ (if exists)
✅ docs/epics/ (if exists)
✅ docs/features/ (if exists)
✅ docs/bdd/ (if exists)
✅ Any EARS/BDD focused guides
```

### Other Files to DELETE

```bash
❌ tests/ (entire directory - will rebuild tests for requirements only)
❌ coverage/ (test coverage from task execution)
❌ coverage*.json (test coverage files)
❌ test_*.py (all test files)
❌ pytest.ini (if not needed)
❌ vitest.config.ts (JavaScript testing)
❌ tsconfig.json (TypeScript compilation)
❌ package.json / package-lock.json (Node.js dependencies)
❌ ai-engineer.sln (.NET solution file)
❌ agentic-flow/ (if contains execution features)
❌ scripts/ (if contains task execution scripts)
❌ examples/ (if task-focused)
```

### Files to KEEP

```bash
✅ .gitignore
✅ README.md (will update)
✅ CLAUDE.md (will update)
✅ requirements.txt (Python dependencies - minimal)
✅ installer/scripts/ (will modify)
✅ installer/global/manifest.json (will update)
```

## Subtask Breakdown

### REQ-002A: Delete Task Execution Commands
- Delete 11 command files
- Verify only requirements commands remain

### REQ-002B: Delete Execution Agents
- Delete 14 agent files
- Verify only requirements agents remain

### REQ-002C: Delete Stack Templates and Library
- Delete all stack templates
- Delete task execution library modules
- Keep only requirements-related modules

### REQ-002D: Delete Tests and Build Artifacts
- Delete tests/ directory
- Delete coverage files
- Delete build configuration files
- Delete language-specific config (package.json, tsconfig, etc.)

### REQ-002E: Clean Documentation
- Delete task execution guides
- Delete workflow guides (unless requirements-focused)
- Update README.md and CLAUDE.md
- Remove task-focused examples

## Success Criteria

- [ ] Only 8-9 requirements commands remain
- [ ] Only 2 requirements agents remain
- [ ] No stack templates remain
- [ ] No task execution library modules
- [ ] No test files (will rebuild later)
- [ ] Documentation focuses on requirements management
- [ ] Repository size significantly reduced
- [ ] Clean git history (commit deletions)

## Timeline Estimate

- REQ-002A: 0.5 hours
- REQ-002B: 0.5 hours
- REQ-002C: 1 hour
- REQ-002D: 0.5 hours
- REQ-002E: 1 hour

**Total**: ~3.5 hours

## Notes

- **This is destructive** - make sure parent repo is backed up
- Delete files permanently (not just move)
- Commit after each subtask
- Update .gitignore if needed
- This creates a clean requirements-focused repository
