---
id: TASK-001F
title: "Transfer Installer Scripts"
created: 2025-10-19
status: backlog
priority: high
complexity: 4
parent_task: TASK-001
subtasks: []
estimated_hours: 2
---

# TASK-001F: Transfer Installer Scripts

## Description

Copy installer scripts and modify to install only lite components (no epic/feature/requirements directories).

## Files to Transfer

```bash
installer/scripts/install.sh           # MODIFY
installer/scripts/install-global.sh    # MODIFY
installer/scripts/init-project.sh      # MODIFY
installer/scripts/uninstall.sh         # KEEP
installer/scripts/deploy-agents.sh     # KEEP
```

## Key Modifications

### install.sh

**Remove directory creation**:
```bash
# DELETE:
mkdir -p docs/epics/{active,completed,cancelled}
mkdir -p docs/features/{active,in_progress,completed}
mkdir -p docs/requirements/{draft,approved,implemented}
mkdir -p docs/bdd
mkdir -p docs/state
```

**Keep directory creation**:
```bash
mkdir -p tasks/{backlog,in_progress,in_review,blocked,completed}
mkdir -p .claude/{agents,commands,instructions}
mkdir -p docs/adr
```

**Update symlinks** (change paths):
```bash
# From:
ln -sf ~/.agentic-flow/commands ~/.claude/commands

# To:
ln -sf ~/.agentecflow/commands ~/.claude/commands
```

### install-global.sh

**Update installation paths**:
```bash
# From:
INSTALL_DIR="$HOME/.agentic-flow"

# To:
INSTALL_DIR="$HOME/.agentecflow"
```

### init-project.sh

**Remove requirements setup**:
- Don't create requirements templates
- Don't create BDD templates
- Don't create epic/feature templates

**Keep**:
- Task templates
- Stack-specific setup
- Quality gate configuration

### manifest.json

**Update**:
```json
{
  "name": "agentecflow",
  "version": "1.0.0",
  "description": "Lightweight AI-Assisted Development with Quality Gates",
  "capabilities": [
    "quality-gates",
    "state-tracking",
    "kanban-workflow",
    "task-management",
    "test-verification"
  ]
}
```

**Remove capabilities**:
- "requirements-engineering"
- "bdd-generation"

## Implementation

```bash
cd ai-engineer/installer/scripts

# Copy scripts
cp install.sh install-global.sh init-project.sh \
   uninstall.sh deploy-agents.sh \
   ../../agentecflow/installer/scripts/

# Copy manifest
cp ../global/manifest.json ../../agentecflow/installer/global/
```

## Testing

```bash
# Test in clean environment
cd /tmp
mkdir test-agentecflow
cd test-agentecflow

# Run installer
bash /path/to/agentecflow/installer/scripts/install.sh

# Verify structure
tree -L 2 ~/.agentecflow
tree -L 3 .claude

# Should NOT see:
# - docs/epics/
# - docs/features/
# - docs/requirements/
# - docs/bdd/

# Should see:
# - tasks/{backlog,in_progress,in_review,blocked,completed}
# - .claude/{agents,commands}
```

## Acceptance Criteria

- [ ] All 5 scripts copied
- [ ] install.sh modified (no requirements dirs)
- [ ] install-global.sh modified (agentecflow paths)
- [ ] init-project.sh modified (no requirements setup)
- [ ] manifest.json updated (lite capabilities)
- [ ] Installation test passes
- [ ] No epic/feature/requirements directories created

## Estimated Time

2 hours
