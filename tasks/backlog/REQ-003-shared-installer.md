---
id: REQ-003
title: "Create Shared Installer Strategy for require-kit and dev-tasker"
created: 2025-10-27
status: backlog
priority: high
complexity: 6
parent_task: none
subtasks:
  - REQ-003A
  - REQ-003B
  - REQ-003C
---

# REQ-003: Create Shared Installer Strategy

## Overview

Create separate installers for **require-kit** (requirements management) and **taskwright** (task execution) that both install to the same `~/.agentecflow` directory, allowing them to be installed standalone or together.

**Integration Model**: Bidirectional Optional Integration
- Each package works independently
- Both detect each other when installed
- Enhanced features automatically available when both present
- No hard dependencies either way

## Current Situation

- Both repositories currently install to `~/.agentecflow`
- Installer assumes all features (requirements + execution) are bundled
- No way to install requirements or execution separately
- Installation scripts are monolithic

## Target Architecture

### Shared Directory Structure

```
~/.agentecflow/
├── commands/
│   ├── require-kit/           # Requirements commands (from require-kit)
│   │   ├── gather-requirements.md
│   │   ├── formalize-ears.md
│   │   ├── generate-bdd.md
│   │   ├── epic-create.md
│   │   ├── feature-create.md
│   │   └── hierarchy-view.md
│   └── dev-tasker/            # Task execution commands (from dev-tasker)
│       ├── task-create.md
│       ├── task-work.md
│       ├── task-complete.md
│       └── task-status.md
├── agents/
│   ├── require-kit/           # Requirements agents
│   │   ├── requirements-analyst.md
│   │   └── bdd-generator.md
│   └── dev-tasker/            # Execution agents
│       ├── architectural-reviewer.md
│       ├── test-verifier.md
│       ├── code-reviewer.md
│       └── task-manager.md
├── lib/
│   ├── require-kit/           # Requirements library (if needed)
│   └── dev-tasker/            # Task execution library
│       ├── checkpoint_display.py
│       ├── plan_persistence.py
│       └── ...
├── templates/                 # Only in dev-tasker
│   ├── react/
│   ├── python/
│   └── ...
└── .installed                 # Tracks what's installed
    ├── require-kit.version
    └── dev-tasker.version
```

### Installation Scenarios

#### Scenario 1: Install require-kit Only
```bash
cd require-kit
./installer/scripts/install.sh

Result:
~/.agentecflow/commands/require-kit/    ✅
~/.agentecflow/agents/require-kit/      ✅
~/.agentecflow/lib/feature_detection.py ✅
~/.agentecflow/require-kit.marker       ✅

Capabilities:
✅ Requirements engineering (EARS notation)
✅ Epic/Feature hierarchy
✅ BDD scenario generation
✅ Requirements traceability
❌ Task execution (install taskwright for this)
❌ Quality gates (install taskwright for this)
```

#### Scenario 2: Install taskwright Only
```bash
cd taskwright
./installer/scripts/install.sh

Result:
~/.agentecflow/commands/taskwright/     ✅
~/.agentecflow/agents/taskwright/       ✅
~/.agentecflow/templates/               ✅
~/.agentecflow/lib/                     ✅
~/.agentecflow/taskwright.marker        ✅

Capabilities:
✅ Task management workflow
✅ Quality gates (architectural review, test enforcement)
✅ Stack templates
✅ Implementation execution
❌ EARS requirements (install require-kit for this)
❌ Epic/Feature hierarchy (install require-kit for this)
```

#### Scenario 3: Install Both (Full Integration)
```bash
cd taskwright
./installer/scripts/install.sh

cd ../require-kit
./installer/scripts/install.sh

Result:
~/.agentecflow/commands/require-kit/    ✅
~/.agentecflow/agents/require-kit/      ✅
~/.agentecflow/commands/taskwright/     ✅
~/.agentecflow/agents/taskwright/       ✅
~/.agentecflow/templates/               ✅
~/.agentecflow/lib/                     ✅
~/.agentecflow/require-kit.marker       ✅
~/.agentecflow/taskwright.marker        ✅

Capabilities (Full Agentecflow):
✅ Complete requirements-to-implementation workflow
✅ Requirements → Epics → Features → Tasks → Code
✅ EARS notation + BDD scenarios
✅ Task execution with quality gates
✅ Full traceability
✅ Integrated status reporting
```

#### Scenario 4: Upgrade One System
```bash
# Upgrade just require-kit
cd require-kit
./installer/scripts/install.sh --upgrade

Result:
- Updates only require-kit files
- Leaves dev-tasker files untouched
- Updates ~/.agentecflow/.installed/require-kit.version
```

## Installer Architecture

### require-kit/installer/scripts/install.sh

```bash
#!/bin/bash
# require-kit Installation Script

INSTALL_DIR="$HOME/.agentecflow"
PACKAGE_NAME="require-kit"
PACKAGE_VERSION="1.0.0"

# Create base structure
mkdir -p "$INSTALL_DIR/commands/$PACKAGE_NAME"
mkdir -p "$INSTALL_DIR/agents/$PACKAGE_NAME"
mkdir -p "$INSTALL_DIR/.installed"

# Install require-kit files
cp -r installer/global/commands/* "$INSTALL_DIR/commands/$PACKAGE_NAME/"
cp -r installer/global/agents/* "$INSTALL_DIR/agents/$PACKAGE_NAME/"

# Create symlinks for commands (backwards compatibility)
for cmd in "$INSTALL_DIR/commands/$PACKAGE_NAME"/*.md; do
    ln -sf "$cmd" "$INSTALL_DIR/commands/$(basename "$cmd")"
done

# Track installation
echo "$PACKAGE_VERSION" > "$INSTALL_DIR/.installed/$PACKAGE_NAME.version"

echo "✓ require-kit installed to ~/.agentecflow"
```

### dev-tasker/installer/scripts/install.sh

```bash
#!/bin/bash
# dev-tasker Installation Script

INSTALL_DIR="$HOME/.agentecflow"
PACKAGE_NAME="dev-tasker"
PACKAGE_VERSION="1.0.0"

# Create base structure
mkdir -p "$INSTALL_DIR/commands/$PACKAGE_NAME"
mkdir -p "$INSTALL_DIR/agents/$PACKAGE_NAME"
mkdir -p "$INSTALL_DIR/lib/$PACKAGE_NAME"
mkdir -p "$INSTALL_DIR/templates"
mkdir -p "$INSTALL_DIR/.installed"

# Install dev-tasker files
cp -r installer/global/commands/* "$INSTALL_DIR/commands/$PACKAGE_NAME/"
cp -r installer/global/agents/* "$INSTALL_DIR/agents/$PACKAGE_NAME/"
cp -r installer/global/lib/* "$INSTALL_DIR/lib/$PACKAGE_NAME/"
cp -r installer/global/templates/* "$INSTALL_DIR/templates/"

# Create symlinks for commands (backwards compatibility)
for cmd in "$INSTALL_DIR/commands/$PACKAGE_NAME"/*.md; do
    ln -sf "$cmd" "$INSTALL_DIR/commands/$(basename "$cmd")"
done

# Track installation
echo "$PACKAGE_VERSION" > "$INSTALL_DIR/.installed/$PACKAGE_NAME.version"

echo "✓ dev-tasker installed to ~/.agentecflow"
```

## Manifest Files

### require-kit/installer/global/manifest.json

```json
{
  "name": "require-kit",
  "version": "1.0.0",
  "description": "Requirements Management Toolkit with EARS, BDD, and Epic/Feature Hierarchy",
  "homepage": "https://github.com/yourusername/require-kit",
  "system": {
    "install_dir": "~/.agentecflow",
    "package_name": "require-kit",
    "namespace": "require-kit"
  },
  "capabilities": [
    "requirements-engineering",
    "ears-notation",
    "bdd-generation",
    "epic-feature-hierarchy",
    "requirements-traceability"
  ],
  "dependencies": {
    "required": ["bash", "git"],
    "optional": ["taskwright"]
  },
  "compatible_with": {
    "taskwright": ">=1.0.0"
  },
  "integration": {
    "taskwright": {
      "type": "bidirectional-optional",
      "provides": "Requirements can be linked to tasks",
      "description": "When both installed, enable full requirements-to-implementation traceability"
    }
  }
}
```

### taskwright/installer/global/manifest.json

```json
{
  "name": "taskwright",
  "version": "1.0.0",
  "description": "Task Execution System with Quality Gates and Stack Templates",
  "homepage": "https://github.com/yourusername/taskwright",
  "system": {
    "install_dir": "~/.agentecflow",
    "package_name": "taskwright",
    "namespace": "taskwright"
  },
  "capabilities": [
    "task-management",
    "quality-gates",
    "test-verification",
    "architectural-review",
    "stack-templates"
  ],
  "dependencies": {
    "required": ["bash", "git", "python3"],
    "optional": ["require-kit"]
  },
  "compatible_with": {
    "require-kit": ">=1.0.0"
  },
  "integration": {
    "require-kit": {
      "type": "bidirectional-optional",
      "provides": "Tasks can reference requirements, epics, and features",
      "description": "When both installed, enable full requirements-to-implementation traceability"
    }
  }
}
```

## Project Initialization

### require-kit Project Initialization

```bash
cd your-project/
require-kit init

Creates:
- docs/requirements/
- docs/epics/
- docs/features/
- docs/bdd/
- .claude/CLAUDE.md (requirements-focused)
```

### dev-tasker Project Initialization

```bash
cd your-project/
dev-tasker init react

Creates:
- tasks/{backlog,in_progress,in_review,blocked,completed}
- .claude/agents/ (stack-specific)
- .claude/CLAUDE.md (task-focused)
- Stack-specific files
```

### Combined Initialization

```bash
cd your-project/

# Initialize requirements management
require-kit init

# Initialize task execution with React stack
dev-tasker init react

Result:
- docs/requirements/, docs/epics/, docs/features/, docs/bdd/
- tasks/
- .claude/ (merged configuration)
- Stack-specific files
```

## Command Discovery

Claude Code discovers commands from:
1. `~/.agentecflow/commands/require-kit/*.md` (if require-kit installed)
2. `~/.agentecflow/commands/dev-tasker/*.md` (if dev-tasker installed)
3. Symlinks in `~/.agentecflow/commands/*.md` (backwards compatibility)

## Uninstallation

### Uninstall require-kit Only

```bash
cd require-kit
./installer/scripts/uninstall.sh

Result:
- Removes ~/.agentecflow/commands/require-kit/
- Removes ~/.agentecflow/agents/require-kit/
- Removes symlinks for require-kit commands
- Leaves dev-tasker files untouched
```

### Uninstall dev-tasker Only

```bash
cd dev-tasker
./installer/scripts/uninstall.sh

Result:
- Removes ~/.agentecflow/commands/dev-tasker/
- Removes ~/.agentecflow/agents/dev-tasker/
- Removes ~/.agentecflow/lib/dev-tasker/
- Removes ~/.agentecflow/templates/
- Leaves require-kit files untouched
```

### Uninstall Both

```bash
cd require-kit
./installer/scripts/uninstall.sh

cd ../dev-tasker
./installer/scripts/uninstall.sh

Result:
- ~/.agentecflow/ is empty (can be deleted)
```

## Subtask Breakdown

### REQ-003A: Update require-kit Installer
- Modify install.sh to install to namespaced directory
- Update manifest.json
- Create uninstall.sh
- Test standalone installation

### REQ-003B: Update dev-tasker Installer
- Modify install.sh to install to namespaced directory
- Update manifest.json
- Create uninstall.sh
- Test standalone installation

### REQ-003C: Test Combined Installation
- Test require-kit + dev-tasker together
- Test upgrade scenarios
- Test uninstall scenarios
- Verify command discovery
- Document integration

## Benefits

1. **Modular**: Install only what you need (requirements-only or tasks-only)
2. **No Hard Dependencies**: Each package works standalone
3. **Bidirectional Integration**: Enhanced features when both installed
4. **Clean Separation**: Each system has its own namespace
5. **Backwards Compatible**: Symlinks maintain existing workflows
6. **Upgradeable**: Update one system without affecting the other
7. **Discoverable**: Claude Code finds all commands regardless of source
8. **Progressive Enhancement**: Start simple, add capabilities later

## Success Criteria

- [ ] require-kit can be installed standalone (no taskwright required)
- [ ] taskwright can be installed standalone (no require-kit required)
- [ ] Both can be installed together (full integration)
- [ ] Feature detection works correctly (marker files)
- [ ] Commands gracefully detect missing packages
- [ ] Upgrading one doesn't affect the other
- [ ] Uninstalling one doesn't affect the other
- [ ] Command discovery works for both systems
- [ ] Version tracking works (`.installed/` directory)
- [ ] Documentation clear for all scenarios
- [ ] Bidirectional optional integration documented

## Timeline Estimate

- REQ-003A: 2 hours
- REQ-003B: 2 hours
- REQ-003C: 1 hour

**Total**: 5 hours

## Notes

- Use namespace directories to avoid conflicts
- Symlinks maintain backwards compatibility
- Version tracking enables smart upgrades
- Both systems share ~/.agentecflow but remain independent
