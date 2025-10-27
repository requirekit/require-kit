# Agentecflow Lite Creation Strategy

**Created**: 2025-10-19
**Purpose**: Comprehensive strategy for creating agentecflow (lite) repository from ai-engineer
**Status**: Implementation Ready

---

## Executive Summary

Create two clean repositories from the current ai-engineer codebase:

1. **agentecflow** (Lite) - Lightweight task workflow with quality gates
2. **agentecflow-requirements** (Full) - Enterprise requirements management

**Key Decision**: Use **cherry-pick approach** (not clone) for clean git history and **git subtree** for shared code management.

**Timeline**: ~20 hours across 8 discrete tasks, each executable with `task-work --micro`

---

## Concrete Recommendation

### Two-Repository Strategy

#### Repository 1: `agentecflow` (Lite - Open Source)

**Scope**: Pure task workflow with quality gates

**Target Audience**: Solo developers, small teams, pragmatic engineers

**Positioning**: "AI-assisted development with architectural review (Phase 2.5) and test enforcement (Phase 4.5). Add one task, implement with quality guarantees."

**What's Included**:
- ✅ Task workflow commands (task-create, task-work, task-complete, task-status)
- ✅ Quality gate agents (architectural-reviewer, test-verifier, code-reviewer)
- ✅ All Phase 2.5, 4.5, 2.6, 2.7 implementations
- ✅ Stack templates (React, Python, .NET MAUI, TypeScript, etc.)
- ✅ Design integration (Figma, Zeplin)
- ✅ Specialized stack agents

**What's Excluded**:
- ❌ Epic/feature hierarchy
- ❌ EARS requirements
- ❌ BDD scenarios
- ❌ PM tool sync
- ❌ Portfolio dashboards

**Pitch**: "No ceremony, just quality gates. 5-minute quickstart."

#### Repository 2: `agentecflow-requirements` (Full - Enterprise)

**Scope**: Complete requirements management + task workflow

**Target Audience**: Regulated industries, enterprise teams, compliance-heavy organizations

**Positioning**: "Complete requirements-to-implementation traceability for regulated industries and enterprises. EARS notation, BDD scenarios, epic/feature hierarchy."

**What's Included**:
- ✅ Everything from agentecflow (via git subtree)
- ✅ EARS requirements management
- ✅ BDD/Gherkin scenarios
- ✅ Epic → Feature → Task hierarchy
- ✅ PM tool synchronization (Jira, Linear, GitHub, Azure DevOps)
- ✅ Portfolio dashboards
- ✅ Requirements traceability

**Pitch**: "Full requirements management for teams that need formal specifications."

---

## Quick Reference Checklist

### Pre-Execution Checklist

**Before Starting TASK-001A**:
- [ ] Read this entire strategy document
- [ ] Understand git subtree concept (review diagrams below)
- [ ] Decide execution strategy (Sequential/Parallel/Batch)
- [ ] Set up GitHub account and configure gh CLI
- [ ] Verify Python 3.7+ installed (`python3 --version`)
- [ ] Verify git installed (`git --version`)
- [ ] Clone ai-engineer repository for reference
- [ ] Allocate 20 hours (or distribute across team)

### Task Execution Checklist

**TASK-001A: Repository Setup** (1 hour)
- [ ] Create GitHub repository `agentecflow`
- [ ] Initialize directory structure
- [ ] Write lite-focused README.md
- [ ] Add LICENSE (MIT)
- [ ] Configure .gitignore
- [ ] Enable branch protection
- [ ] Verify: Repository public and accessible

**TASK-001B: Transfer Commands** (2 hours)
- [ ] Copy 8 core commands
- [ ] Modify task-create.md (remove epic/feature/requirements)
- [ ] Modify task-work.md (remove requirements loading)
- [ ] Modify task-status.md (remove epic/feature filters)
- [ ] Simplify task-refine.md
- [ ] Keep task-complete.md, debug.md, figma-to-react.md, zeplin-to-maui.md unchanged
- [ ] Verify: `grep -i "epic\|feature\|requirement" *.md` returns empty

**TASK-001C: Transfer Agents** (2 hours)
- [ ] Copy 15 core agents (exclude requirements-analyst, bdd-generator)
- [ ] Update agent prompts (remove EARS/BDD references)
- [ ] Verify: 15 agents present
- [ ] Verify: No requirements references in active instructions

**TASK-001D: Transfer Library** (3 hours)
- [ ] Copy lib/ directory
- [ ] Remove feature_generator.py
- [ ] Test Python imports
- [ ] Verify: All Phase 2.5, 4.5 modules present
- [ ] Verify: No broken imports

**TASK-001E: Transfer Templates** (4 hours)
- [ ] Copy all 8 templates
- [ ] Update CLAUDE.md in each template
- [ ] Update settings.json (if present)
- [ ] Keep all stack-specific agents
- [ ] Verify: No epic/feature/requirements references in CLAUDE.md
- [ ] Verify: All templates initialize successfully

**TASK-001F: Transfer Installer** (2 hours)
- [ ] Copy installer scripts
- [ ] Modify install.sh (remove requirements directories)
- [ ] Modify install-global.sh (update paths to ~/.agentecflow)
- [ ] Update manifest.json (remove requirements capabilities)
- [ ] Test installation in clean environment
- [ ] Verify: No epic/feature/requirements directories created

**TASK-001G: Create Documentation** (3 hours)
- [ ] Create docs/QUICKSTART.md
- [ ] Create docs/QUALITY-GATES.md
- [ ] Create docs/STACK-TEMPLATES.md
- [ ] Create docs/DESIGN-FIRST-WORKFLOW.md
- [ ] Create CONTRIBUTING.md
- [ ] Create CODE_OF_CONDUCT.md
- [ ] Verify: No EARS/BDD/epic references in core docs

**TASK-001H: Testing & Validation** (3 hours)
- [ ] Test installation on macOS
- [ ] Test installation on Linux
- [ ] Test installation on Windows WSL
- [ ] Initialize all 8 templates
- [ ] Run command execution tests
- [ ] Verify quality gates (Phase 2.5, 4.5)
- [ ] Test compilation for each stack
- [ ] Document issues in GitHub
- [ ] Create test results report

### Post-Completion Checklist

**Release Preparation**:
- [ ] All 8 tasks completed and verified
- [ ] No outstanding GitHub issues (critical)
- [ ] Documentation reviewed and polished
- [ ] README.md compelling for target audience
- [ ] Installation tested on all platforms
- [ ] Tag v1.0.0 release
- [ ] Create release notes

**Soft Launch** (Week 1):
- [ ] Invite 5-10 trusted developers
- [ ] Gather initial feedback
- [ ] Fix critical issues
- [ ] Add screenshots/GIFs to README
- [ ] Create video walkthrough (optional)

**Public Launch** (Week 2-3):
- [ ] Announce on Hacker News
- [ ] Post to Reddit (r/programming, r/MachineLearning)
- [ ] Share on Twitter/LinkedIn
- [ ] Write blog post
- [ ] Monitor GitHub issues/discussions

**Validation Period** (30-60 days):
- [ ] Track GitHub stars, forks, issues
- [ ] Document common user questions
- [ ] Iterate based on feedback
- [ ] Decide: Create agentecflow-requirements? (if validated)

### Git Subtree Future Checklist

**When Creating agentecflow-requirements** (Future):
- [ ] agentecflow stable (v1.0+)
- [ ] Positive user feedback collected
- [ ] Clear demand for requirements features
- [ ] Clone ai-engineer to agentecflow-requirements
- [ ] Add remote: `git remote add agentecflow-core <url>`
- [ ] Add subtree: `git subtree add --prefix=core agentecflow-core main --squash`
- [ ] Test subtree pull/push workflow
- [ ] Update installer to install core + requirements
- [ ] Position for enterprise audience
- [ ] Soft launch to regulated/enterprise users

---

## Git Subtree Architecture Diagram

### Visual Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         AGENTECFLOW (LITE)                              │
│                     github.com/you/agentecflow                          │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────┐     │
│  │  installer/global/                                            │     │
│  │  ├── commands/                                                │     │
│  │  │   ├── task-create.md        ◄─── CORE COMPONENT           │     │
│  │  │   ├── task-work.md          ◄─── CORE COMPONENT           │     │
│  │  │   ├── task-complete.md      ◄─── CORE COMPONENT           │     │
│  │  │   └── task-status.md        ◄─── CORE COMPONENT           │     │
│  │  ├── agents/                                                  │     │
│  │  │   ├── architectural-reviewer.md  ◄─── CORE (Phase 2.5)    │     │
│  │  │   ├── test-verifier.md          ◄─── CORE (Phase 4.5)    │     │
│  │  │   ├── code-reviewer.md          ◄─── CORE (Phase 5)      │     │
│  │  │   └── task-manager.md           ◄─── CORE                 │     │
│  │  ├── lib/                       ◄─── CORE (Python modules)   │     │
│  │  │   ├── checkpoint_display.py                               │     │
│  │  │   ├── plan_persistence.py                                 │     │
│  │  │   └── review_modes.py                                     │     │
│  │  └── templates/                 ◄─── CORE (All stacks)       │     │
│  │      ├── react/                                               │     │
│  │      ├── python/                                              │     │
│  │      └── maui-appshell/                                       │     │
│  └──────────────────────────────────────────────────────────────┘     │
│                                                                         │
│  Focus: Lightweight, quality gates, 5-minute quickstart                │
│  Target: Solo developers, small teams, pragmatic engineers             │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ git subtree
                                    │ pull/push
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                   AGENTECFLOW-REQUIREMENTS (FULL)                       │
│               github.com/you/agentecflow-requirements                   │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────┐     │
│  │  core/  ◄─── GIT SUBTREE from agentecflow                    │     │
│  │  │                                                            │     │
│  │  ├── installer/global/                                        │     │
│  │  │   ├── commands/         (task-*.md from agentecflow)       │     │
│  │  │   ├── agents/           (core agents from agentecflow)     │     │
│  │  │   ├── lib/              (Python modules from agentecflow)  │     │
│  │  │   └── templates/        (stack templates from agentecflow) │     │
│  └──────────────────────────────────────────────────────────────┘     │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────┐     │
│  │  requirements/  ◄─── REQUIREMENTS-SPECIFIC                   │     │
│  │  │                                                            │     │
│  │  ├── commands/                                                │     │
│  │  │   ├── gather-requirements.md                              │     │
│  │  │   ├── formalize-ears.md                                   │     │
│  │  │   ├── generate-bdd.md                                     │     │
│  │  │   ├── epic-create.md                                      │     │
│  │  │   ├── feature-create.md                                   │     │
│  │  │   ├── hierarchy-view.md                                   │     │
│  │  │   └── portfolio-dashboard.md                              │     │
│  │  └── agents/                                                  │     │
│  │      ├── requirements-analyst.md                             │     │
│  │      └── bdd-generator.md                                    │     │
│  └──────────────────────────────────────────────────────────────┘     │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────┐     │
│  │  installer/scripts/install-full.sh                           │     │
│  │  │                                                            │     │
│  │  ├─► bash core/installer/scripts/install.sh  (installs core) │     │
│  │  └─► cp requirements/commands/* ~/.agentecflow/commands/     │     │
│  └──────────────────────────────────────────────────────────────┘     │
│                                                                         │
│  Focus: Complete traceability, EARS, BDD, epic/feature hierarchy       │
│  Target: Regulated industries, enterprise teams, compliance             │
└─────────────────────────────────────────────────────────────────────────┘
```

### Git Subtree Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CODE FLOW DIAGRAM                                │
└─────────────────────────────────────────────────────────────────────────┘

Scenario 1: Bug Fix in Agentecflow (Lite)
─────────────────────────────────────────────────────────────────────────

1. Fix bug in agentecflow
   ┌────────────────────┐
   │  agentecflow       │
   │  fix bug in        │
   │  task-work.md      │
   └────────┬───────────┘
            │ git commit
            │ git push
            ▼
   ┌────────────────────┐
   │  GitHub:           │
   │  agentecflow       │
   │  main branch       │
   └────────┬───────────┘
            │
            │ 2. Pull to agentecflow-requirements
            │
            ▼
   ┌────────────────────────────────┐
   │  agentecflow-requirements      │
   │                                │
   │  $ git subtree pull \          │
   │      --prefix=core \           │
   │      agentecflow-core main \   │
   │      --squash                  │
   └────────┬───────────────────────┘
            │
            ▼
   ┌────────────────────────────────┐
   │  core/installer/global/        │
   │  commands/task-work.md         │
   │  ← NOW HAS BUG FIX             │
   └────────────────────────────────┘


Scenario 2: Bug Fix in Agentecflow-Requirements (affects core)
───────────────────────────────────────────────────────────────────────

1. Fix bug in core/ directory
   ┌─────────────────────────────────┐
   │  agentecflow-requirements       │
   │  fix bug in                     │
   │  core/installer/global/agents/  │
   │  test-verifier.md               │
   └────────┬────────────────────────┘
            │ git commit
            │
            ▼
   ┌─────────────────────────────────┐
   │  $ git subtree push \           │
   │      --prefix=core \            │
   │      agentecflow-core main      │
   └────────┬────────────────────────┘
            │
            │ 2. Pushed to agentecflow
            │
            ▼
   ┌────────────────────┐
   │  GitHub:           │
   │  agentecflow       │
   │  main branch       │
   └────────┬───────────┘
            │
            ▼
   ┌────────────────────────────────┐
   │  installer/global/agents/      │
   │  test-verifier.md              │
   │  ← NOW HAS BUG FIX             │
   └────────────────────────────────┘


Scenario 3: Requirements-Specific Feature (doesn't affect core)
─────────────────────────────────────────────────────────────────────

1. Add new requirements feature
   ┌─────────────────────────────────┐
   │  agentecflow-requirements       │
   │  add new feature in             │
   │  requirements/commands/         │
   │  epic-dashboard.md              │
   └────────┬────────────────────────┘
            │ git commit
            │ git push
            ▼
   ┌─────────────────────────────────┐
   │  GitHub:                        │
   │  agentecflow-requirements       │
   │  main branch                    │
   └─────────────────────────────────┘
            │
            │ ◄─── NO PUSH TO CORE
            │      (requirements/ is separate)
            ▼
   ┌─────────────────────────────────┐
   │  agentecflow (lite)             │
   │  ← UNAFFECTED                   │
   │  (stays lightweight)            │
   └─────────────────────────────────┘
```

### Directory Structure Comparison

```
┌─────────────────────────────────────┬─────────────────────────────────────┐
│     AGENTECFLOW (LITE)              │   AGENTECFLOW-REQUIREMENTS (FULL)   │
├─────────────────────────────────────┼─────────────────────────────────────┤
│                                     │                                     │
│  agentecflow/                       │  agentecflow-requirements/          │
│  ├── installer/                     │  ├── core/  ◄── SUBTREE             │
│  │   ├── global/                    │  │   └── installer/                 │
│  │   │   ├── commands/               │  │       ├── global/                │
│  │   │   │   ├── task-create.md     │  │       │   ├── commands/          │
│  │   │   │   ├── task-work.md       │  │       │   │   ├── task-*.md     │
│  │   │   │   ├── task-complete.md   │  │       │   │   └── ...           │
│  │   │   │   └── task-status.md     │  │       │   ├── agents/           │
│  │   │   ├── agents/                │  │       │   ├── lib/              │
│  │   │   │   ├── architectural-     │  │       │   └── templates/        │
│  │   │   │   │   reviewer.md        │  │       └── scripts/              │
│  │   │   │   ├── test-verifier.md   │  │                                 │
│  │   │   │   ├── code-reviewer.md   │  ├── requirements/  ◄── NEW        │
│  │   │   │   └── task-manager.md    │  │   ├── commands/                 │
│  │   │   ├── lib/                   │  │   │   ├── epic-create.md        │
│  │   │   │   ├── checkpoint_        │  │   │   ├── feature-create.md     │
│  │   │   │   │   display.py         │  │   │   ├── gather-               │
│  │   │   │   ├── plan_persistence   │  │   │   │   requirements.md       │
│  │   │   │   │   .py                │  │   │   ├── formalize-ears.md     │
│  │   │   │   └── review_modes.py    │  │   │   ├── generate-bdd.md       │
│  │   │   └── templates/             │  │   │   └── hierarchy-view.md     │
│  │   │       ├── react/             │  │   └── agents/                   │
│  │   │       ├── python/            │  │       ├── requirements-          │
│  │   │       └── maui-appshell/     │  │       │   analyst.md            │
│  │   └── scripts/                   │  │       └── bdd-generator.md      │
│  │       └── install.sh             │  │                                 │
│  ├── docs/                          │  ├── installer/                    │
│  │   ├── QUICKSTART.md              │  │   └── scripts/                  │
│  │   ├── QUALITY-GATES.md           │  │       └── install-full.sh       │
│  │   └── STACK-TEMPLATES.md         │  │                                 │
│  ├── README.md                      │  ├── docs/                         │
│  └── LICENSE                        │  │   ├── REQUIREMENTS-              │
│                                     │  │   │   MANAGEMENT.md              │
│  SIZE: ~30MB                        │  │   ├── EARS-NOTATION.md          │
│  FILES: ~150                        │  │   └── TRACEABILITY.md           │
│  FOCUS: Simple, fast, quality      │  │                                  │
│                                     │  ├── README.md                      │
│                                     │  └── LICENSE                        │
│                                     │                                     │
│                                     │  SIZE: ~50MB                        │
│                                     │  FILES: ~250                        │
│                                     │  FOCUS: Complete, traceable         │
└─────────────────────────────────────┴─────────────────────────────────────┘
```

---

## Git Subtree Strategy for Code Sharing

### Why Git Subtree?

**Problem**: Both repos share core functionality:
- Phase 2.5 (Architectural Review)
- Phase 4.5 (Test Enforcement)
- Core agents (task-manager, test-verifier, code-reviewer)
- Stack templates
- Quality gate implementations

**Solutions Compared**:

| Approach | Pros | Cons | Verdict |
|----------|------|------|---------|
| **Duplicate Code** | Simple, independent repos | Maintenance nightmare, bug fixes twice | ❌ No |
| **Git Submodules** | Proper separation | Complex, checkout issues, version hell | ❌ No |
| **Git Subtree** | Simple workflow, merged history | Slightly more complex setup | ✅ **YES** |
| **Monorepo** | Single codebase | Defeats purpose of separation | ❌ No |
| **NPM/PyPI Package** | Proper versioning | Overhead for markdown/config files | ❌ Overkill |

**Winner: Git Subtree** - Balance of simplicity and maintainability.

### Git Subtree Architecture

```
agentecflow/                          # Lite repo (source of truth for core)
├── installer/
│   ├── global/
│   │   ├── commands/
│   │   │   ├── task-create.md       ← CORE
│   │   │   ├── task-work.md         ← CORE
│   │   │   ├── task-complete.md     ← CORE
│   │   │   └── task-status.md       ← CORE
│   │   ├── agents/
│   │   │   ├── architectural-reviewer.md  ← CORE
│   │   │   ├── test-verifier.md           ← CORE
│   │   │   ├── code-reviewer.md           ← CORE
│   │   │   └── task-manager.md            ← CORE
│   │   ├── lib/                     ← CORE (Python modules)
│   │   └── templates/               ← CORE (all stack templates)
│   └── scripts/
│       └── install.sh               ← CORE
└── docs/
    └── QUICKSTART.md                ← LITE-SPECIFIC


agentecflow-requirements/             # Full repo (includes core via subtree)
├── core/                             ← GIT SUBTREE from agentecflow
│   ├── installer/global/
│   │   ├── commands/                 (task-*.md from agentecflow)
│   │   ├── agents/                   (core agents from agentecflow)
│   │   ├── lib/                      (Python modules from agentecflow)
│   │   └── templates/                (stack templates from agentecflow)
│   └── installer/scripts/
│       └── install.sh
├── requirements/                     ← REQUIREMENTS-SPECIFIC
│   ├── commands/
│   │   ├── gather-requirements.md
│   │   ├── formalize-ears.md
│   │   ├── generate-bdd.md
│   │   ├── epic-create.md
│   │   ├── feature-create.md
│   │   └── hierarchy-view.md
│   └── agents/
│       ├── requirements-analyst.md
│       └── bdd-generator.md
├── installer/
│   └── scripts/
│       └── install-full.sh           ← Installs core + requirements
└── docs/
    └── REQUIREMENTS-MANAGEMENT.md    ← REQUIREMENTS-SPECIFIC
```

### Git Subtree Workflow

#### Initial Setup (One-Time)

```bash
# Step 1: Create agentecflow-requirements repo
git clone https://github.com/you/agentecflow-requirements.git
cd agentecflow-requirements

# Step 2: Add agentecflow as subtree remote
git remote add agentecflow-core https://github.com/you/agentecflow.git

# Step 3: Pull agentecflow as subtree into core/ directory
git subtree add --prefix=core agentecflow-core main --squash

# Result: core/ directory now contains entire agentecflow repo
# --squash: Combines all commits into one (cleaner history)
```

#### Ongoing: Pull Updates from Core

```bash
# When agentecflow gets updates (bug fixes, new features)
cd agentecflow-requirements

# Pull latest from agentecflow into core/ subtree
git subtree pull --prefix=core agentecflow-core main --squash

# Resolve any conflicts (if requirements features touched core files)
git add .
git commit -m "Update core from agentecflow v1.2.0"
git push
```

#### Ongoing: Push Improvements Back to Core

```bash
# If you fix a bug in core/ while working in agentecflow-requirements
cd agentecflow-requirements

# Make changes in core/installer/global/commands/task-work.md
vim core/installer/global/commands/task-work.md
git add core/installer/global/commands/task-work.md
git commit -m "Fix: Task state transition bug in task-work"

# Push changes back to agentecflow repo
git subtree push --prefix=core agentecflow-core main

# Now the fix is in both repos:
# - agentecflow: Has the fix directly
# - agentecflow-requirements: Has the fix in core/
```

#### Installer Integration

**agentecflow-requirements/installer/scripts/install-full.sh**:

```bash
#!/bin/bash

# Install core components (from subtree)
echo "Installing agentecflow core..."
bash core/installer/scripts/install.sh

# Install requirements features
echo "Installing requirements management features..."

# Copy requirements commands
cp -r requirements/commands/* ~/.agentecflow/commands/

# Copy requirements agents
cp -r requirements/agents/* ~/.agentecflow/agents/

# Create requirements directories
mkdir -p docs/epics/{active,completed,cancelled}
mkdir -p docs/features/{active,in_progress,completed}
mkdir -p docs/requirements/{draft,approved,implemented}
mkdir -p docs/bdd
mkdir -p docs/state

# Update manifest
cat > ~/.agentecflow/manifest.json <<EOF
{
  "name": "agentecflow-requirements",
  "version": "2.0.0",
  "description": "Complete Requirements Management + Agentecflow Core",
  "capabilities": [
    "requirements-engineering",
    "bdd-generation",
    "quality-gates",
    "state-tracking",
    "kanban-workflow",
    "task-management",
    "test-verification"
  ]
}
EOF

echo "✅ Agentecflow Requirements installed successfully"
echo "Includes: Core (lite) + Requirements management"
```

### Benefits of Git Subtree Approach

1. **Single Source of Truth**: agentecflow is authoritative for core code
2. **Automatic Sync**: Pull updates from core with one command
3. **Bidirectional Fixes**: Bug fixes flow both directions
4. **Simple Cloning**: `git clone` works normally, no submodule initialization
5. **Clear Separation**: core/ directory visually separates shared code
6. **Independent Releases**: Each repo can version independently

### Maintenance Workflow

**When you fix a bug in agentecflow (lite)**:
```bash
cd agentecflow
# Fix bug in task-work.md
git commit -m "Fix: Phase 4.5 test enforcement edge case"
git push

# Update agentecflow-requirements
cd ../agentecflow-requirements
git subtree pull --prefix=core agentecflow-core main --squash
git push
```

**When you fix a bug in agentecflow-requirements that affects core**:
```bash
cd agentecflow-requirements
# Fix bug in core/installer/global/agents/test-verifier.md
git commit -m "Fix: Test verifier timeout handling"
git subtree push --prefix=core agentecflow-core main

# Bug fix is now in agentecflow too
```

### Version Management

**agentecflow (Lite)**:
```json
{
  "name": "agentecflow",
  "version": "1.2.0",
  "description": "Lightweight AI-Assisted Development with Quality Gates"
}
```

**agentecflow-requirements (Full)**:
```json
{
  "name": "agentecflow-requirements",
  "version": "2.1.0",
  "description": "Complete Requirements Management + Agentecflow Core",
  "dependencies": {
    "agentecflow-core": "1.2.0"
  }
}
```

Track core version dependency in manifest.json.

---

## Summary of Task Structure

### Main Task: TASK-001-core-transfer.md

**Complexity**: 8 (Complex - requires breakdown)
**Total Estimate**: ~20 hours (2-3 days focused work)

**Overview**: Create agentecflow repository containing ONLY lightweight task workflow components, removing all requirements management features to reduce perceived complexity for open source adoption.

**Strategic Context**:
- **Problem**: Full ai-engineer repo includes enterprise requirements features creating perceived complexity
- **Solution**: Split into two repositories with clear separation
- **Target**: Pragmatic developers who want quality gates without ceremony

**Architecture Decision**:
- ✅ **Cherry-pick approach** (not full clone) for clean git history
- ✅ **Git subtree** for shared code management in agentecflow-requirements (future)
- ✅ Each subtask suitable for `task-work --micro` execution

### 8 Subtasks (Each `--micro` Compatible)

#### TASK-001A: Repository Setup and Basic Structure

**Complexity**: 3 (Simple)
**Estimate**: 1 hour

**Deliverables**:
- GitHub repository created (`agentecflow`)
- Basic directory structure (installer/global/{commands,agents,templates}, docs/, tests/)
- README.md (lite-focused, 5-minute quickstart)
- LICENSE (MIT)
- .gitignore configured
- Branch protection rules enabled

**Key Actions**:
```bash
gh repo create agentecflow --public
mkdir -p installer/global/{commands,agents,instructions,templates}
mkdir -p installer/scripts docs tests .github/workflows
# Create README emphasizing "No ceremony, just quality gates"
```

**Verification**:
- Repository public and accessible
- Directory structure matches plan
- README positions for pragmatic developers (not enterprise)

---

#### TASK-001B: Transfer Core Commands

**Complexity**: 4 (Medium)
**Estimate**: 2 hours

**Files to Transfer**:
```
✓ task-create.md       - MODIFY (remove epic/feature/requirements)
✓ task-work.md         - MODIFY (remove requirements context)
✓ task-complete.md     - KEEP AS-IS
✓ task-status.md       - MODIFY (remove epic/feature filters)
✓ task-refine.md       - SIMPLIFY
✓ debug.md             - KEEP AS-IS
✓ figma-to-react.md    - KEEP AS-IS
✓ zeplin-to-maui.md    - KEEP AS-IS
```

**Key Modifications**:
- **task-create.md**: Remove `epic:`, `feature:`, `requirements:` from frontmatter
- **task-work.md**: Remove Phase 1 requirements loading, keep all quality gate phases
- **task-status.md**: Remove epic/feature/requirements filters

**Verification**:
```bash
grep -i "epic\|feature\|requirement\|ears\|bdd" task-*.md
# Should return NO active references
```

---

#### TASK-001C: Transfer Core Agents

**Complexity**: 4 (Medium)
**Estimate**: 2 hours

**Agents to Include** (15 total):
```
✓ architectural-reviewer.md     # Phase 2.5 (CRITICAL)
✓ test-verifier.md             # Phase 4.5 (CRITICAL)
✓ test-orchestrator.md         # Phase 4.5 support
✓ code-reviewer.md             # Phase 5
✓ task-manager.md              # Core orchestration
✓ complexity-evaluator.md      # Phase 2.7
✓ build-validator.md           # Quality gates
✓ debugging-specialist.md
✓ devops-specialist.md
✓ database-specialist.md
✓ security-specialist.md
✓ pattern-advisor.md
✓ python-mcp-specialist.md
✓ figma-react-orchestrator.md
✓ zeplin-maui-orchestrator.md
```

**Agents to Exclude**:
```
❌ requirements-analyst.md     # Requirements management
❌ bdd-generator.md            # BDD scenarios
```

**Key Modifications**:
- Remove EARS/BDD references from agent prompts
- Update task context loading (use description, not requirements)

**Verification**:
```bash
ls -1 *.md | wc -l  # Should be 15
grep -i "requirements\|ears\|bdd.*scenario" *.md  # Should be empty
```

---

#### TASK-001D: Transfer Implementation Library

**Complexity**: 5 (Medium-Complex)
**Estimate**: 3 hours

**Modules to Include**:
```python
# Phase 2.5, 2.6, 2.7 (Architectural Review)
checkpoint_display.py
plan_persistence.py
plan_modifier.py
review_modes.py
user_interaction.py
upfront_complexity_adapter.py
plan_markdown_parser.py
plan_audit.py

# Task Management
git_state_helper.py
agent_utils.py
micro_task_workflow.py
version_manager.py
error_messages.py
visualization.py
spec_drift_detector.py

# Metrics
metrics/__init__.py
metrics/plan_audit_metrics.py
```

**Modules to Exclude**:
```python
feature_generator.py          # Feature generation from epics
test_feature_generator.py     # Tests for feature generation
```

**Key Actions**:
```bash
cp -r lib/ ../../agentecflow/installer/global/commands/
cd ../../agentecflow/installer/global/commands/lib
rm -f feature_generator.py test_feature_generator.py
```

**Verification**:
```bash
python3 -c "
import sys
sys.path.insert(0, '.')
from checkpoint_display import *
from plan_persistence import *
from review_modes import *
print('✅ All imports successful')
"
```

---

#### TASK-001E: Transfer Stack Templates

**Complexity**: 5 (Medium-Complex)
**Estimate**: 4 hours

**Templates to Transfer** (8 total):
```
default/
react/
python/
typescript-api/
maui-appshell/
maui-navigationpage/
dotnet-microservice/
fullstack/
```

**Key Modifications for Each Template**:

1. **Update CLAUDE.md**:
   - Remove: Requirements Management, EARS Notation, BDD/Gherkin, Epic/Feature Hierarchy
   - Keep: Task Workflow, Quality Gates, Testing Patterns, Stack-Specific Patterns

2. **Update settings.json** (if present):
   - Remove: `requirements_dir`, `bdd_dir`, `epics_dir`, `features_dir`
   - Keep: `tasks_dir`, `stack`, `quality_gates`

3. **Keep all stack-specific agents**:
   - React: react-state-specialist.md, react-testing-specialist.md
   - Python: python-api-specialist.md, python-testing-specialist.md
   - MAUI: maui-domain-specialist.md, maui-viewmodel-specialist.md
   - Etc.

**Verification**:
```bash
for template in */CLAUDE.md; do
  grep -i "epic\|requirements.*EARS\|BDD.*scenario" "$template" && \
    echo "⚠ Found references in $template"
done
# Should return nothing
```

---

#### TASK-001F: Transfer Installer Scripts

**Complexity**: 4 (Medium)
**Estimate**: 2 hours

**Scripts to Transfer**:
```
install.sh           - MODIFY
install-global.sh    - MODIFY
init-project.sh      - MODIFY
uninstall.sh         - KEEP AS-IS
deploy-agents.sh     - KEEP AS-IS
```

**Key Modifications**:

**install.sh** - Remove directory creation:
```bash
# DELETE these lines:
mkdir -p docs/epics/{active,completed,cancelled}
mkdir -p docs/features/{active,in_progress,completed}
mkdir -p docs/requirements/{draft,approved,implemented}
mkdir -p docs/bdd
mkdir -p docs/state

# KEEP these lines:
mkdir -p tasks/{backlog,in_progress,in_review,blocked,completed}
mkdir -p .claude/{agents,commands,instructions}
mkdir -p docs/adr
```

**install-global.sh** - Update paths:
```bash
# From:
INSTALL_DIR="$HOME/.agentic-flow"

# To:
INSTALL_DIR="$HOME/.agentecflow"
```

**manifest.json** - Update capabilities:
```json
{
  "name": "agentecflow",
  "version": "1.0.0",
  "capabilities": [
    "quality-gates",
    "state-tracking",
    "kanban-workflow",
    "task-management",
    "test-verification"
  ]
}
```

Remove: `"requirements-engineering"`, `"bdd-generation"`

**Verification**:
```bash
cd /tmp/test-install
bash /path/to/agentecflow/installer/scripts/install.sh
tree -L 2 ~/.agentecflow
# Should NOT see epic/feature/requirements directories
```

---

#### TASK-001G: Create Lite Documentation

**Complexity**: 4 (Medium)
**Estimate**: 3 hours

**Documents to Create**:

1. **docs/QUICKSTART.md** - 5-minute getting started guide
2. **docs/QUALITY-GATES.md** - Phase 2.5, 4.5 explained in detail
3. **docs/STACK-TEMPLATES.md** - Template customization guide
4. **docs/DESIGN-FIRST-WORKFLOW.md** - --design-only / --implement-only flags
5. **CONTRIBUTING.md** - Contribution guidelines
6. **CODE_OF_CONDUCT.md** - Community standards

**Key Requirements**:
- ✅ Emphasize simplicity and 5-minute quickstart
- ✅ Explain quality gates clearly (Phase 2.5, 4.5 unique value)
- ✅ NO mention of EARS, BDD, epics, features in core docs
- ✅ Optional links to agentecflow-requirements for those who need full system

**Forbidden Topics**:
- ❌ EARS notation
- ❌ BDD/Gherkin scenarios
- ❌ Epic/feature hierarchy
- ❌ Requirements management
- ❌ PM tool synchronization

**Verification**:
```bash
grep -r "EARS\|epic.*hierarchy\|requirements.*management" docs/ \
  | grep -v "agentecflow-requirements" | grep -v "Historical"
# Should be empty
```

---

#### TASK-001H: Testing and Validation

**Complexity**: 4 (Medium)
**Estimate**: 3 hours

**Test Matrix**:

**Platforms** (6):
- macOS (Intel)
- macOS (Apple Silicon)
- Ubuntu 22.04
- Ubuntu 24.04
- Windows WSL (Ubuntu)
- Windows WSL (Debian)

**Templates** (8):
- default, react, python, typescript-api
- maui-appshell, maui-navigationpage
- dotnet-microservice, fullstack

**Test Scenarios**:

1. **Fresh Installation Test**
   ```bash
   rm -rf ~/.agentecflow ~/.claude
   git clone https://github.com/you/agentecflow.git
   ./installer/scripts/install.sh
   # Should complete in <2 minutes
   ```

2. **Template Initialization Test**
   ```bash
   agentecflow init react
   tree -L 2
   # Should create tasks/, .claude/
   # Should NOT create docs/epics/, docs/features/, docs/requirements/
   ```

3. **Command Execution Test**
   ```bash
   /task-create "Test feature"
   cat tasks/backlog/TASK-001-test-feature.md
   # Should NOT contain epic:, feature:, requirements:
   ```

4. **Quality Gate Test**
   ```bash
   /task-work TASK-001 --micro
   # Verify Phase 2.5, 4.5 execute correctly
   ```

5. **Compilation Test** (per stack)
   ```bash
   # React
   npm install && npm run build && npm test

   # Python
   python -m pytest tests/

   # .NET MAUI
   dotnet build && dotnet test
   ```

**Issue Tracking**: Create GitHub issues for any failures

**Test Results Template**: Document platform/template matrix results

**Acceptance Criteria**:
- [ ] Installs in <2 minutes on all platforms
- [ ] All 8 templates initialize successfully
- [ ] Commands work without epic/feature flags
- [ ] Quality gates function correctly
- [ ] No broken links or references

---

## Component Classification Summary

### ✅ INCLUDE in Agentecflow Lite

**Commands** (8):
- task-create.md, task-work.md, task-complete.md, task-status.md
- task-refine.md, debug.md
- figma-to-react.md, zeplin-to-maui.md

**Agents** (15):
- architectural-reviewer.md (Phase 2.5) ⭐
- test-verifier.md (Phase 4.5) ⭐
- test-orchestrator.md (Phase 4.5 support) ⭐
- code-reviewer.md (Phase 5) ⭐
- task-manager.md (core) ⭐
- complexity-evaluator.md, build-validator.md
- debugging-specialist.md, devops-specialist.md, database-specialist.md
- security-specialist.md, pattern-advisor.md, python-mcp-specialist.md
- figma-react-orchestrator.md, zeplin-maui-orchestrator.md

**Library Modules** (~20 Python files):
- All Phase 2.5, 2.6, 2.7 modules (checkpoint, plan, review modes)
- All task management modules (git state, agents, micro workflow)
- All supporting modules (metrics, visualization, error messages)

**Templates** (8):
- default, react, python, typescript-api
- maui-appshell, maui-navigationpage
- dotnet-microservice, fullstack

**Installer Scripts** (5):
- install.sh, install-global.sh, init-project.sh
- uninstall.sh, deploy-agents.sh

**Configuration**:
- manifest.json (modified - remove requirements capabilities)

### ❌ EXCLUDE from Agentecflow Lite

**Commands** (9):
- epic-create.md, epic-status.md, epic-sync.md, epic-generate-features.md
- feature-create.md, feature-status.md, feature-sync.md, feature-generate-tasks.md
- gather-requirements.md, formalize-ears.md, generate-bdd.md
- hierarchy-view.md, portfolio-dashboard.md, task-sync.md

**Agents** (2):
- requirements-analyst.md
- bdd-generator.md

**Library Modules**:
- feature_generator.py
- Any epic/feature/requirements-specific modules

**Directories**:
- docs/epics/, docs/features/, docs/requirements/, docs/bdd/, docs/state/

---

## Execution Strategies

### Option 1: Sequential Execution with `--micro`

**Recommended for**: Solo execution, learning the codebase

```bash
# Day 1: Setup & Core Components (5 hours)
/task-work TASK-001A --micro  # Repo setup (1 hour)
/task-work TASK-001B --micro  # Commands (2 hours)
/task-work TASK-001C --micro  # Agents (2 hours)

# Day 2: Complex Components (7 hours)
/task-work TASK-001D --micro  # Library (3 hours)
/task-work TASK-001E --micro  # Templates (4 hours)

# Day 3: Integration & Testing (8 hours)
/task-work TASK-001F --micro  # Installer (2 hours)
/task-work TASK-001G --micro  # Documentation (3 hours)
/task-work TASK-001H --micro  # Testing (3 hours)
```

**Total**: 3 days (focused work), ~20 hours

### Option 2: Parallel Execution (with Conductor.build)

**Recommended for**: Team execution, faster completion

**Worktree 1** (Developer A):
```bash
/task-work TASK-001A --micro
/task-work TASK-001B --micro
/task-work TASK-001F --micro
```

**Worktree 2** (Developer B):
```bash
/task-work TASK-001C --micro
/task-work TASK-001D --micro
/task-work TASK-001E --micro
```

**Worktree 3** (Developer C):
```bash
/task-work TASK-001G --micro
/task-work TASK-001H --micro
```

**Total**: 1 day (parallel work), ~8 hours per person

### Option 3: Batch Execution

**Recommended for**: Balanced approach, checkpoint validation

**Batch 1 - Foundation** (Day 1):
- TASK-001A (repo setup)
- TASK-001B (commands)
- TASK-001C (agents)
- **Checkpoint**: Verify commands and agents work

**Batch 2 - Implementation** (Day 2):
- TASK-001D (library)
- TASK-001E (templates)
- **Checkpoint**: Verify imports and template initialization

**Batch 3 - Release** (Day 3):
- TASK-001F (installer)
- TASK-001G (documentation)
- TASK-001H (testing)
- **Checkpoint**: Full system validation

---

## Success Metrics

### Functional Completeness

- [ ] Repository created and publicly accessible
- [ ] Installation completes in <2 minutes
- [ ] All core commands work (task-create, task-work, task-complete, task-status)
- [ ] Quality gates execute correctly (Phase 2.5, 4.5, 2.6, 2.7)
- [ ] All 8 stack templates initialize successfully
- [ ] Cross-platform compatibility (macOS, Linux, Windows WSL)

### Quality Standards

- [ ] No references to epic/feature/requirements in user-facing docs
- [ ] No broken links or missing dependencies
- [ ] Git history clean (no requirements feature commits)
- [ ] README emphasizes pragmatism (not enterprise)
- [ ] Documentation clear and concise
- [ ] 5-minute quickstart achievable

### Performance Targets

- [ ] Repository size <50MB (excluding .git)
- [ ] Installation downloads <10MB
- [ ] Command execution <2 seconds (excluding implementation)
- [ ] Learning curve <1 hour for first task completion

---

## Risk Mitigation

### Risk: Missing Dependencies

**Probability**: Medium
**Impact**: High (broken installation)

**Mitigation**:
- TASK-001D includes explicit import testing
- Each subtask has verification steps
- TASK-001H includes cross-platform testing

### Risk: Broken Quality Gates

**Probability**: Low
**Impact**: Critical (core value proposition)

**Mitigation**:
- Phase 2.5, 4.5 modules explicitly listed in TASK-001D
- TASK-001H includes quality gate smoke tests
- Testing distributed across subtasks (continuous validation)

### Risk: Template Issues

**Probability**: Medium
**Impact**: Medium (user experience)

**Mitigation**:
- TASK-001E includes per-template validation
- TASK-001H includes compilation tests per stack
- Template-specific agents preserved

### Risk: Documentation Gaps

**Probability**: Low
**Impact**: Medium (adoption barrier)

**Mitigation**:
- TASK-001G creates comprehensive lite docs
- Forbidden topics list prevents scope creep
- Verification checks for requirements references

### Risk: Installation Failures

**Probability**: Low
**Impact**: High (first impression)

**Mitigation**:
- TASK-001F includes installation testing
- TASK-001H includes 6-platform test matrix
- Issue tracking template prepared

---

## Next Steps After Completion

### Phase 1: Soft Launch (Week 1)

1. **Internal Testing** (5-10 users)
   - Invite trusted developers
   - Gather initial feedback
   - Fix critical issues

2. **Documentation Polish**
   - Add screenshots/GIFs
   - Create video walkthrough
   - Improve quickstart based on feedback

3. **GitHub Setup**
   - Configure issue templates
   - Set up GitHub Actions for testing
   - Add contributor guidelines

### Phase 2: Public Launch (Week 2-3)

1. **Announcement**
   - Post to Hacker News, Reddit (r/programming, r/MachineLearning)
   - Share on Twitter/LinkedIn
   - Write blog post

2. **Community Building**
   - Respond to issues promptly
   - Engage with early adopters
   - Document common questions

3. **Metrics Tracking**
   - GitHub stars, forks, issues
   - Installation counts (if possible)
   - User feedback themes

### Phase 3: Validation Period (30-60 days)

1. **Usage Metrics**
   - Track adoption patterns
   - Identify most-used features
   - Identify pain points

2. **Iteration**
   - Fix reported bugs
   - Improve documentation
   - Add quality-of-life improvements

3. **Validation Decision**
   - If successful: Proceed to create agentecflow-requirements
   - If unsuccessful: Pivot or merge features back

### Phase 4: Create agentecflow-requirements (If Validated)

**Prerequisites**:
- agentecflow stable (v1.0+)
- Positive user feedback
- Clear demand for requirements features

**Execution**:
1. Clone ai-engineer to agentecflow-requirements
2. Set up git subtree (pull from agentecflow)
3. Test subtree workflow
4. Position for enterprise audience
5. Soft launch to regulated/enterprise users

---

## Maintenance Strategy

### Agentecflow (Lite) - Long Term

**Release Cadence**: Monthly minor releases, weekly patches

**Focus Areas**:
- Quality gate improvements
- Stack template updates
- Performance optimizations
- Bug fixes

**Community Engagement**:
- Active GitHub issues/discussions
- Monthly community calls (if adoption warrants)
- Contributor recognition

### Agentecflow-Requirements (Full) - Long Term

**Release Cadence**: Quarterly minor releases

**Subtree Updates**:
```bash
# Every agentecflow release
cd agentecflow-requirements
git subtree pull --prefix=core agentecflow-core main --squash
git tag "v2.1.0-core-1.2.0"  # Track core version
git push --tags
```

**Focus Areas**:
- Requirements traceability
- PM tool integrations
- Enterprise features
- Compliance requirements

---

## Conclusion

This strategy provides a clear, executable path to creating agentecflow (lite) while maintaining a future path to agentecflow-requirements through git subtree.

**Key Advantages**:
1. ✅ Clean separation reduces perceived complexity
2. ✅ Git subtree enables efficient code sharing
3. ✅ Each subtask is `--micro` executable (complexity 3-5)
4. ✅ Continuous validation (testing in each subtask)
5. ✅ Clear upgrade path (lite → full)

**Estimated Timeline**:
- **Solo**: 3 days (20 hours)
- **Team**: 1 day (8 hours parallel)
- **Batch**: 3 days (with checkpoints)

**Ready to Execute**: All tasks defined, all files identified, all modifications specified.

---

## Appendix: Quick Reference

### File Count Summary

| Category | Lite Count | Full Count | Excluded |
|----------|-----------|-----------|----------|
| Commands | 8 | 17 | 9 |
| Agents | 15 | 17 | 2 |
| Lib Modules | ~18 | ~20 | ~2 |
| Templates | 8 | 8 | 0 |
| Scripts | 5 | 5 | 0 |

### Critical Dependencies

**Must Have** (for quality gates to work):
- checkpoint_display.py (Phase 2.6)
- plan_modifier.py (Phase 2.7)
- review_modes.py (auto/quick/full)
- architectural-reviewer.md (Phase 2.5)
- test-verifier.md (Phase 4.5)

**Cannot Remove Without Breaking Core Functionality**

### Git Subtree Cheat Sheet

```bash
# Initial setup
git remote add agentecflow-core https://github.com/you/agentecflow.git
git subtree add --prefix=core agentecflow-core main --squash

# Pull updates
git subtree pull --prefix=core agentecflow-core main --squash

# Push changes back
git subtree push --prefix=core agentecflow-core main

# Split and create separate branch (advanced)
git subtree split --prefix=core --branch core-updates
```

### Verification Commands

```bash
# Check no requirements features
grep -r "epic\|feature\|requirement.*EARS" commands/ agents/
grep -r "BDD.*scenario" commands/ agents/ | grep -v "mode=bdd"

# Check imports work
python3 -c "from lib.checkpoint_display import *; print('✅')"

# Check installation
tree -L 2 ~/.agentecflow
ls -la ~/.claude/commands  # Should be symlink

# Check templates
for t in default react python; do
  agentecflow init $t && echo "✅ $t" || echo "❌ $t"
done
```

---

## One-Page Quick Reference

### The Big Picture

```
┌────────────────────────────────────────────────────────────────────────┐
│ CREATE AGENTECFLOW LITE (20 hours, 8 tasks)                           │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│ FROM: ai-engineer (current repo)                                      │
│   ├─ Task workflow ✅                                                  │
│   ├─ Quality gates ✅                                                  │
│   ├─ Stack templates ✅                                                │
│   ├─ Requirements features ❌ (EXCLUDE)                                │
│   └─ Epic/Feature hierarchy ❌ (EXCLUDE)                               │
│                                                                        │
│ TO: agentecflow (new repo)                                            │
│   ├─ Task workflow ONLY ✅                                             │
│   ├─ Quality gates ✅                                                  │
│   ├─ Stack templates ✅                                                │
│   ├─ Lite-focused docs ✅                                              │
│   └─ 5-minute quickstart ✅                                            │
│                                                                        │
│ METHOD: Cherry-pick (NOT clone) for clean git history                 │
│ FUTURE: Git subtree for agentecflow-requirements                      │
└────────────────────────────────────────────────────────────────────────┘
```

### 8 Tasks at a Glance

| Task | What | Time | Complexity | Key Output |
|------|------|------|------------|------------|
| **001A** | Repo Setup | 1h | 3 | GitHub repo, README, structure |
| **001B** | Commands | 2h | 4 | 8 commands (no epic/feature) |
| **001C** | Agents | 2h | 4 | 15 agents (no requirements) |
| **001D** | Library | 3h | 5 | Python modules (Phase 2.5, 4.5) |
| **001E** | Templates | 4h | 5 | 8 stack templates (cleaned) |
| **001F** | Installer | 2h | 4 | Scripts (lite install only) |
| **001G** | Docs | 3h | 4 | 6 docs (lite-focused) |
| **001H** | Testing | 3h | 4 | Cross-platform validation |
| **TOTAL** | | **20h** | | **agentecflow v1.0** |

### Component Counts

```
┌──────────────────┬──────────┬──────────┬────────────┐
│ Component        │ ai-eng   │ lite     │ Excluded   │
├──────────────────┼──────────┼──────────┼────────────┤
│ Commands         │ 17       │ 8        │ 9          │
│ Agents           │ 17       │ 15       │ 2          │
│ Lib Modules      │ ~20      │ ~18      │ ~2         │
│ Templates        │ 8        │ 8        │ 0          │
│ Scripts          │ 5        │ 5        │ 0          │
├──────────────────┼──────────┼──────────┼────────────┤
│ Total Files      │ ~300     │ ~150     │ ~150       │
│ Repo Size        │ ~60MB    │ ~30MB    │ ~30MB      │
└──────────────────┴──────────┴──────────┴────────────┘
```

### Critical Files to Include/Exclude

**✅ MUST INCLUDE** (Core value):
```
commands/task-work.md                    ← Core workflow
agents/architectural-reviewer.md         ← Phase 2.5 (unique!)
agents/test-verifier.md                  ← Phase 4.5 (unique!)
lib/checkpoint_display.py                ← Phase 2.6
lib/plan_modifier.py                     ← Phase 2.7
lib/review_modes.py                      ← Auto/quick/full
ALL templates/                           ← Stack support
```

**❌ MUST EXCLUDE** (Requirements features):
```
commands/epic-*.md                       ← Remove
commands/feature-*.md                    ← Remove
commands/gather-requirements.md          ← Remove
commands/formalize-ears.md               ← Remove
commands/generate-bdd.md                 ← Remove
agents/requirements-analyst.md           ← Remove
agents/bdd-generator.md                  ← Remove
lib/feature_generator.py                 ← Remove
```

### Execution Options

**Option 1: Solo Sequential** (3 days)
```
Day 1: TASK-001A → 001B → 001C (5 hours)
Day 2: TASK-001D → 001E (7 hours)
Day 3: TASK-001F → 001G → 001H (8 hours)
```

**Option 2: Team Parallel** (1 day)
```
Dev A: 001A, 001B, 001F (5 hours)
Dev B: 001C, 001D, 001E (9 hours)
Dev C: 001G, 001H (6 hours)
```

**Option 3: Batch with Checkpoints** (3 days)
```
Batch 1: 001A, 001B, 001C + Checkpoint
Batch 2: 001D, 001E + Checkpoint
Batch 3: 001F, 001G, 001H + Validation
```

### Git Subtree Commands (Future Use)

**Setup agentecflow-requirements** (after lite is validated):
```bash
git clone https://github.com/you/agentecflow-requirements.git
cd agentecflow-requirements
git remote add agentecflow-core https://github.com/you/agentecflow.git
git subtree add --prefix=core agentecflow-core main --squash
```

**Pull updates from lite to full**:
```bash
cd agentecflow-requirements
git subtree pull --prefix=core agentecflow-core main --squash
```

**Push fixes from full back to lite**:
```bash
cd agentecflow-requirements
# Fix bug in core/...
git subtree push --prefix=core agentecflow-core main
```

### Success Criteria Checklist

**Must Have** (blocking release):
- [ ] Installs in <2 minutes on macOS, Linux, Windows WSL
- [ ] All 8 templates initialize successfully
- [ ] Commands work without epic/feature/requirements flags
- [ ] Phase 2.5 (architectural review) executes correctly
- [ ] Phase 4.5 (test enforcement) executes correctly
- [ ] No broken links or missing dependencies
- [ ] Zero references to EARS/BDD/epic in user-facing docs

**Should Have** (quality improvements):
- [ ] README compelling for pragmatic developers
- [ ] 5-minute quickstart achievable
- [ ] Documentation clear and concise
- [ ] Command execution <2 seconds
- [ ] Learning curve <1 hour

**Nice to Have** (enhancements):
- [ ] Screenshots/GIFs in README
- [ ] Video walkthrough
- [ ] Example projects per template
- [ ] GitHub Actions for testing

### Next Steps After Completion

```
Week 1: Soft Launch
  ├─ Invite 5-10 trusted developers
  ├─ Gather feedback
  └─ Fix critical issues

Week 2-3: Public Launch
  ├─ Announce on Hacker News, Reddit
  ├─ Share on social media
  └─ Monitor GitHub issues

30-60 Days: Validation
  ├─ Track stars, forks, issues
  ├─ Document user feedback
  └─ Decide: Create agentecflow-requirements?

If Validated:
  └─ Create agentecflow-requirements with git subtree
```

### Emergency Contacts

**Stuck on a task?**
1. Review task file: `tasks/backlog/TASK-001X-*.md`
2. Check verification commands in task
3. Review this strategy doc (section for that task)
4. Ask for help (create GitHub issue in ai-engineer)

**Common Issues**:
- **Import errors**: Check Python path, verify lib/ copied completely
- **Missing references**: Use grep to find lingering epic/feature mentions
- **Installation fails**: Check symlink paths, verify ~/.agentecflow exists
- **Template won't init**: Check CLAUDE.md syntax, verify settings.json

### Key Principles

1. **Cherry-pick, don't clone** - Clean git history matters
2. **Test continuously** - Don't wait until end
3. **Verify thoroughly** - Use grep to find hidden references
4. **Keep it simple** - When in doubt, exclude complexity
5. **Document clearly** - Target pragmatic developers, not enterprise
6. **5-minute quickstart** - Make onboarding trivial
7. **Quality gates are the value** - Phase 2.5 and 4.5 are unique

### File Size Targets

```
Component Size Limits:
  README.md: <5KB (concise, not comprehensive)
  QUICKSTART.md: <3KB (literally 5 minutes to read)
  QUALITY-GATES.md: <8KB (detailed but focused)
  Total docs: <30KB (lightweight documentation)
  Total repo: <50MB (fast clone)
```

---

**Document Version**: 1.0
**Last Updated**: 2025-10-19
**Status**: Implementation Ready
**Related Tasks**: TASK-001, TASK-001A through TASK-001H

---

## Ready to Start?

1. **Read this entire document** (30 minutes)
2. **Review Task-001A** in `tasks/backlog/TASK-001A-repo-setup.md`
3. **Execute**: `/task-work TASK-001A --micro`
4. **Follow the 8-task sequence**
5. **Celebrate** when v1.0 launches! 🎉
