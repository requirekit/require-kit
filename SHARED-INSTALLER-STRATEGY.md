# Shared Installer Strategy

## Overview

Create a modular installation architecture where **require-kit** (requirements management) and **dev-tasker** (task execution) can be installed standalone or together, sharing the `~/.agentecflow` directory.

## Architecture

### Shared Directory Structure

```
~/.agentecflow/
├── commands/
│   ├── require-kit/              # Requirements commands (11-12 commands)
│   │   ├── gather-requirements.md
│   │   ├── formalize-ears.md
│   │   ├── generate-bdd.md
│   │   ├── epic-create.md
│   │   ├── epic-status.md
│   │   ├── epic-sync.md
│   │   ├── epic-generate-features.md
│   │   ├── feature-create.md
│   │   ├── feature-status.md
│   │   ├── feature-sync.md
│   │   ├── feature-generate-tasks.md
│   │   └── hierarchy-view.md
│   ├── dev-tasker/               # Task execution commands
│   │   ├── task-create.md
│   │   ├── task-work.md
│   │   ├── task-complete.md
│   │   ├── task-status.md
│   │   ├── task-refine.md
│   │   ├── debug.md
│   │   ├── figma-to-react.md
│   │   └── zeplin-to-maui.md
│   ├── gather-requirements.md    # Symlink → require-kit/gather-requirements.md
│   ├── task-create.md            # Symlink → dev-tasker/task-create.md
│   └── ...                       # Other symlinks
├── agents/
│   ├── require-kit/              # Requirements agents (2 agents)
│   │   ├── requirements-analyst.md
│   │   └── bdd-generator.md
│   ├── dev-tasker/               # Execution agents (15+ agents)
│   │   ├── architectural-reviewer.md
│   │   ├── test-verifier.md
│   │   ├── code-reviewer.md
│   │   ├── task-manager.md
│   │   ├── complexity-evaluator.md
│   │   └── ...
│   ├── requirements-analyst.md   # Symlink → require-kit/requirements-analyst.md
│   ├── task-manager.md           # Symlink → dev-tasker/task-manager.md
│   └── ...
├── lib/
│   └── dev-tasker/               # Only dev-tasker needs library
│       ├── checkpoint_display.py
│       ├── plan_persistence.py
│       ├── complexity_evaluator.py
│       └── ...
├── templates/                    # Only dev-tasker has templates
│   ├── react/
│   ├── python/
│   ├── maui-appshell/
│   └── ...
└── .installed/                   # Version tracking
    ├── require-kit.version       # "1.0.0"
    ├── require-kit.timestamp     # Unix timestamp
    ├── dev-tasker.version        # "1.0.0"
    └── dev-tasker.timestamp      # Unix timestamp
```

## Installation Scenarios

### 1. Install require-kit Only

```bash
cd require-kit
./installer/scripts/install.sh
```

**Result**:
```
~/.agentecflow/
├── commands/
│   ├── require-kit/                    ✅ Installed
│   │   ├── gather-requirements.md
│   │   ├── formalize-ears.md
│   │   └── ...
│   ├── gather-requirements.md          ✅ Symlink
│   ├── formalize-ears.md              ✅ Symlink
│   └── ...
├── agents/
│   ├── require-kit/                    ✅ Installed
│   │   ├── requirements-analyst.md
│   │   └── bdd-generator.md
│   ├── requirements-analyst.md         ✅ Symlink
│   └── bdd-generator.md               ✅ Symlink
└── .installed/
    └── require-kit.version             ✅ "1.0.0"
```

**Available commands**:
- /gather-requirements
- /formalize-ears
- /generate-bdd
- /epic-create
- /feature-create
- /hierarchy-view
- (11-12 requirements commands total)

**NOT available**:
- /task-create, /task-work, /task-complete, /task-status
- No quality gates, no templates

### 2. Install dev-tasker Only

```bash
cd dev-tasker
./installer/scripts/install.sh
```

**Result**:
```
~/.agentecflow/
├── commands/
│   ├── dev-tasker/                     ✅ Installed
│   │   ├── task-create.md
│   │   ├── task-work.md
│   │   └── ...
│   ├── task-create.md                  ✅ Symlink
│   ├── task-work.md                   ✅ Symlink
│   └── ...
├── agents/
│   ├── dev-tasker/                     ✅ Installed
│   │   ├── architectural-reviewer.md
│   │   ├── test-verifier.md
│   │   └── ...
│   ├── architectural-reviewer.md       ✅ Symlink
│   └── ...
├── lib/
│   └── dev-tasker/                     ✅ Installed
├── templates/                          ✅ Installed
│   ├── react/
│   └── ...
└── .installed/
    └── dev-tasker.version              ✅ "1.0.0"
```

**Available commands**:
- /task-create
- /task-work
- /task-complete
- /task-status
- All quality gate features
- All templates

**NOT available**:
- /gather-requirements, /formalize-ears, /generate-bdd
- No EARS notation, no BDD generation

### 3. Install Both (Complete System)

```bash
# Install require-kit first
cd require-kit
./installer/scripts/install.sh

# Install dev-tasker
cd ../dev-tasker
./installer/scripts/install.sh
```

**Result**:
```
~/.agentecflow/
├── commands/
│   ├── require-kit/                    ✅ Requirements commands
│   ├── dev-tasker/                     ✅ Task execution commands
│   ├── gather-requirements.md          ✅ → require-kit/
│   ├── task-create.md                  ✅ → dev-tasker/
│   └── ... (all commands available)
├── agents/
│   ├── require-kit/                    ✅ 2 requirements agents
│   ├── dev-tasker/                     ✅ 15+ execution agents
│   └── ... (all agents available)
├── lib/dev-tasker/                     ✅
├── templates/                          ✅
└── .installed/
    ├── require-kit.version             ✅ "1.0.0"
    └── dev-tasker.version              ✅ "1.0.0"
```

**Available**: Everything! Full requirements + execution system.

### 4. Upgrade Scenarios

#### Upgrade require-kit Only

```bash
cd require-kit
git pull
./installer/scripts/install.sh --upgrade
```

**Result**:
- Updates only `~/.agentecflow/commands/require-kit/`
- Updates only `~/.agentecflow/agents/require-kit/`
- Updates `~/.agentecflow/.installed/require-kit.version` to new version
- Leaves dev-tasker files completely untouched
- dev-tasker continues working without interruption

#### Upgrade dev-tasker Only

```bash
cd dev-tasker
git pull
./installer/scripts/install.sh --upgrade
```

**Result**:
- Updates only `~/.agentecflow/commands/dev-tasker/`
- Updates only `~/.agentecflow/agents/dev-tasker/`
- Updates `~/.agentecflow/lib/dev-tasker/`
- Updates `~/.agentecflow/templates/`
- Updates `~/.agentecflow/.installed/dev-tasker.version`
- Leaves require-kit files completely untouched

### 5. Uninstallation Scenarios

#### Uninstall require-kit Only

```bash
cd require-kit
./installer/scripts/uninstall.sh
```

**Result**:
- Removes `~/.agentecflow/commands/require-kit/`
- Removes `~/.agentecflow/agents/require-kit/`
- Removes symlinks pointing to require-kit files
- Removes `~/.agentecflow/.installed/require-kit.*`
- Leaves dev-tasker files completely intact
- dev-tasker continues working

#### Uninstall dev-tasker Only

```bash
cd dev-tasker
./installer/scripts/uninstall.sh
```

**Result**:
- Removes `~/.agentecflow/commands/dev-tasker/`
- Removes `~/.agentecflow/agents/dev-tasker/`
- Removes `~/.agentecflow/lib/dev-tasker/`
- Removes `~/.agentecflow/templates/`
- Removes symlinks pointing to dev-tasker files
- Removes `~/.agentecflow/.installed/dev-tasker.*`
- Leaves require-kit files completely intact

#### Uninstall Both (Complete Removal)

```bash
cd require-kit
./installer/scripts/uninstall.sh

cd ../dev-tasker
./installer/scripts/uninstall.sh
```

**Result**:
- `~/.agentecflow/` is empty
- Installer automatically removes empty `~/.agentecflow/` directory
- System is completely clean

## Project Initialization

### require-kit Project Setup

```bash
cd your-project/
require-kit init
```

**Creates**:
```
your-project/
├── docs/
│   ├── requirements/
│   │   ├── draft/
│   │   ├── approved/
│   │   └── implemented/
│   ├── epics/
│   │   ├── active/
│   │   ├── completed/
│   │   └── cancelled/
│   ├── features/
│   │   ├── active/
│   │   ├── in_progress/
│   │   └── completed/
│   └── bdd/
└── .claude/
    └── CLAUDE.md (requirements-focused)
```

### dev-tasker Project Setup

```bash
cd your-project/
dev-tasker init react
```

**Creates**:
```
your-project/
├── tasks/
│   ├── backlog/
│   ├── in_progress/
│   ├── in_review/
│   ├── blocked/
│   └── completed/
├── .claude/
│   ├── agents/ (React specialists)
│   └── CLAUDE.md (task execution focused)
└── [React-specific files]
```

### Combined Initialization

```bash
cd your-project/

# Initialize requirements
require-kit init

# Initialize task execution with React
dev-tasker init react
```

**Creates**:
```
your-project/
├── docs/
│   ├── requirements/      # From require-kit
│   ├── epics/            # From require-kit
│   ├── features/         # From require-kit
│   └── bdd/              # From require-kit
├── tasks/                # From dev-tasker
│   ├── backlog/
│   ├── in_progress/
│   └── ...
├── .claude/
│   ├── agents/           # React specialists from dev-tasker
│   └── CLAUDE.md         # Merged configuration
└── [React-specific files]
```

**Workflow**:
1. Use require-kit for requirements: /gather-requirements → /formalize-ears → /generate-bdd
2. Create epics/features: /epic-create → /feature-create
3. Use dev-tasker for execution: /task-create → /task-work → /task-complete
4. Full traceability: Requirements → Features → Tasks

## Command Discovery

Claude Code automatically discovers commands from:

1. **Primary source** (namespaced):
   - `~/.agentecflow/commands/require-kit/*.md`
   - `~/.agentecflow/commands/dev-tasker/*.md`

2. **Secondary source** (backwards compatibility):
   - `~/.agentecflow/commands/*.md` (symlinks)

Both approaches work identically from user's perspective.

## Manifest Files

### require-kit/installer/global/manifest.json

```json
{
  "name": "require-kit",
  "version": "1.0.0",
  "description": "Requirements Management Toolkit with EARS, BDD, and Epic/Feature Hierarchy",
  "system": {
    "install_dir": "~/.agentecflow",
    "package_name": "require-kit",
    "namespace": "require-kit"
  },
  "capabilities": [
    "requirements-engineering",
    "ears-notation",
    "bdd-generation",
    "epic-feature-hierarchy"
  ],
  "compatible_with": {
    "dev-tasker": ">=1.0.0"
  }
}
```

### dev-tasker/installer/global/manifest.json

```json
{
  "name": "dev-tasker",
  "version": "1.0.0",
  "description": "Task Execution System with Quality Gates and Stack Templates",
  "system": {
    "install_dir": "~/.agentecflow",
    "package_name": "dev-tasker",
    "namespace": "dev-tasker"
  },
  "capabilities": [
    "task-management",
    "quality-gates",
    "test-verification",
    "architectural-review"
  ],
  "compatible_with": {
    "require-kit": ">=1.0.0"
  }
}
```

## Benefits

1. **Modularity**: Install only what you need
2. **Clean Separation**: Each system in its own namespace
3. **Independence**: Upgrade/uninstall one without affecting the other
4. **Compatibility**: Work together seamlessly when both installed
5. **Backwards Compatible**: Symlinks maintain existing workflows
6. **Version Tracking**: `.installed/` directory tracks versions
7. **Discoverable**: Claude Code finds all commands automatically
8. **Safe**: Uninstall one system, other keeps working

## Implementation Tasks

- **REQ-003**: Shared installer strategy (parent task)
- **REQ-003A**: Update require-kit installer (2 hours)
  - Modify install.sh for namespaced installation
  - Update manifest.json
  - Create uninstall.sh
  - Create init-project.sh
- **REQ-003B**: Update dev-tasker installer (2 hours)
  - Same modifications for dev-tasker
- **REQ-003C**: Test combined installation (1 hour)
  - Test all scenarios
  - Verify command discovery
  - Document integration

**Total**: 5 hours

## Next Steps

1. Execute REQ-002 series (delete agentecflow features from require-kit)
2. Execute REQ-003A (update require-kit installer)
3. Split dev-tasker repository from ai-engineer
4. Execute REQ-003B (update dev-tasker installer)
5. Execute REQ-003C (test combined installation)
6. Document usage patterns

## Summary

This architecture provides:
- **Standalone require-kit**: Requirements management only
- **Standalone dev-tasker**: Task execution with quality gates
- **Combined system**: Full requirements + execution workflow
- **Modular upgrades**: Update one without affecting the other
- **Clean uninstallation**: Remove one, other keeps working
- **Shared installation**: Both use `~/.agentecflow` without conflicts
