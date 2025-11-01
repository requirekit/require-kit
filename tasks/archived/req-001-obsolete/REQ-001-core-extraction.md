---
id: REQ-001
title: "Extract Requirements Features to require-kit Repository"
created: 2025-10-27
status: backlog
priority: high
complexity: 7
parent_task: none
subtasks:
  - REQ-001A
  - REQ-001B
  - REQ-001C
  - REQ-001D
  - REQ-001E
---

# REQ-001: Extract Requirements Features to require-kit Repository

## Overview

Extract ONLY the requirements management features (EARS notation, BDD/Gherkin, Epic/Feature hierarchy) from the ai-engineer repository into a new standalone require-kit repository.

## Strategic Context

**Goal**: Create a focused requirements management toolkit that can be used independently of the full Agentecflow system.

**Scope**: Requirements gathering, EARS formalization, BDD scenario generation, epic/feature hierarchy - NO task execution, templates, or quality gates.

## What to Include (Requirements Features ONLY)

### Commands
- ✅ gather-requirements.md
- ✅ formalize-ears.md
- ✅ generate-bdd.md
- ✅ epic-create.md
- ✅ epic-status.md
- ✅ epic-sync.md (if not PM tool dependent)
- ✅ feature-create.md
- ✅ feature-status.md
- ✅ feature-sync.md (if not PM tool dependent)
- ✅ hierarchy-view.md (epic/feature visualization)

### Agents
- ✅ requirements-analyst.md
- ✅ bdd-generator.md

### Library Modules
- ✅ Any EARS-specific utilities
- ✅ Any BDD generation utilities
- ✅ Epic/feature generators

### Documentation Templates
- ✅ EARS requirement templates
- ✅ BDD scenario templates
- ✅ Epic specification templates
- ✅ Feature specification templates

## What to Exclude (Agentecflow Execution Features)

### Commands
- ❌ task-create.md
- ❌ task-work.md
- ❌ task-complete.md
- ❌ task-status.md
- ❌ task-refine.md
- ❌ All UX integration commands (figma-to-react, zeplin-to-maui)
- ❌ debug.md

### Agents
- ❌ architectural-reviewer.md
- ❌ test-verifier.md
- ❌ test-orchestrator.md
- ❌ code-reviewer.md
- ❌ task-manager.md
- ❌ complexity-evaluator.md
- ❌ build-validator.md
- ❌ All stack-specific agents
- ❌ All UX integration agents

### Library Modules
- ❌ checkpoint_display.py
- ❌ plan_persistence.py
- ❌ test enforcement modules
- ❌ quality gate modules
- ❌ All task workflow modules

### Templates
- ❌ All stack templates (react, python, maui, etc.)
- ❌ Project-specific configurations

## Subtask Breakdown

### REQ-001A: Repository Setup
- Create require-kit repository structure
- Basic README focused on requirements management
- LICENSE and .gitignore

### REQ-001B: Extract Requirements Commands
- Copy gather-requirements.md, formalize-ears.md, generate-bdd.md
- Copy epic/feature management commands
- Remove any task workflow dependencies

### REQ-001C: Extract Requirements Agents
- Copy requirements-analyst.md, bdd-generator.md
- Remove references to task execution

### REQ-001D: Extract Documentation Templates
- Copy EARS, BDD, epic, feature templates
- Create docs/templates/ structure

### REQ-001E: Create Requirements-Focused Documentation
- README focused on requirements gathering
- EARS notation guide
- BDD scenario guide
- Epic/feature hierarchy guide

## Success Criteria

- [ ] Repository contains ONLY requirements features
- [ ] No references to task execution, quality gates, or templates
- [ ] Clear documentation for requirements workflow
- [ ] Can be used standalone without Agentecflow
- [ ] All requirements commands work independently

## Timeline Estimate

- REQ-001A: 1 hour
- REQ-001B: 2 hours
- REQ-001C: 1 hour
- REQ-001D: 2 hours
- REQ-001E: 2 hours

**Total**: ~8 hours (1 day)

## Notes

- This is the INVERSE of TASK-001 (Agentecflow Lite)
- Focus on requirements gathering, not execution
- Keep it simple and focused on requirements management
- Can integrate with Agentecflow OR be used standalone
