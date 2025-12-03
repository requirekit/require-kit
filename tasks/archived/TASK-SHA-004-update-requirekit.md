---
id: TASK-SHA-004
title: Update RequireKit installer to use shared-agents
status: archived
created: 2025-11-28T21:00:00Z
updated: 2025-12-03T17:40:00Z
archived: 2025-12-03T17:40:00Z
archived_reason: "No longer required - TASK-8632 removed unused agents from RequireKit. RequireKit now only has 2 core agents (bdd-generator, requirements-analyst) which are RequireKit-specific, not shared. Implementation agents are provided by GuardKit."
priority: high
tags: [shared-agents, requirekit, installer, lean, archived]
complexity: 3
estimated_effort: 2h
depends_on: [TASK-SHA-002]
blocks: [TASK-SHA-005]
parent_task: TASK-ARCH-DC05
task_type: implementation
superseded_by: TASK-8632
---

# Task: Update RequireKit Installer

## Context

Update RequireKit's installer to download shared-agents from the new repository. Same approach as TASK-SHA-003, but for RequireKit.

## Acceptance Criteria

- [ ] Version pinning file created: `installer/shared-agents-version.txt`
- [ ] Installer function added to download shared-agents
- [ ] Agents installed to `.claude/agents/universal/`
- [ ] Duplicate agents removed from `.claude/agents/`
- [ ] Installer tested successfully

## Implementation

### 1. Create Version Pinning File

```bash
# In RequireKit repository
cd ../require-kit

# Create pinning file
echo "v1.0.0" > installer/shared-agents-version.txt
git add installer/shared-agents-version.txt
```

### 2. Add Install Function

Add to `installer/scripts/install.sh` (same as GuardKit):

```bash
install_shared_agents() {
    echo ""
    echo "📦 Installing shared agents..."

    local version=$(cat "$SCRIPT_DIR/../shared-agents-version.txt" 2>/dev/null || echo "v1.0.0")
    local url="https://github.com/guardkit/shared-agents/releases/download/$version/shared-agents.tar.gz"
    local target_dir="$PROJECT_ROOT/.claude/agents/universal"

    mkdir -p "$target_dir"

    if curl -sL "$url" | tar -xz -C "$target_dir" --strip-components=1 2>/dev/null; then
        echo "✅ Shared agents $version installed"
    else
        echo "❌ Failed to install shared agents"
        return 1
    fi
}

# Call during installation
install_shared_agents || echo "Warning: Shared agents installation failed"
```

### 3. Remove Duplicate Agents

```bash
# Remove agents that are now in shared-agents
# (Based on verified list from TASK-SHA-001)

# Example:
rm .claude/agents/code-reviewer.md
rm .claude/agents/test-orchestrator.md
# ... remove others from verified list

git add .claude/agents/
git commit -m "refactor: Move universal agents to shared-agents repo"
```

### 4. Test Installation

```bash
# Create fresh test project
mkdir test-requirekit
cd test-requirekit

# Run installer
../require-kit/installer/scripts/install.sh

# Verify
ls -la .claude/agents/universal/
# Should contain shared agents

# Test RequireKit commands
# (Whatever RequireKit's main commands are)
```

## Test Requirements

- [ ] Version file readable
- [ ] Download succeeds
- [ ] Extraction works
- [ ] Agents accessible in `.claude/agents/universal/`
- [ ] RequireKit commands work normally
- [ ] No regression in functionality

## Estimated Effort

**2 hours** (same as GuardKit)
- Code changes: 1 hour
- Testing: 30 minutes
- Cleanup: 30 minutes

## Success Criteria

- [ ] Installer downloads shared-agents successfully
- [ ] Shared agents installed to correct location
- [ ] Duplicate agents removed from repository
- [ ] All tests pass
- [ ] No regression in RequireKit commands

## Notes

**Parallel execution**: This task can run in parallel with TASK-SHA-003 (GuardKit update). Both download from the same shared-agents v1.0.0 release.

**Same approach**: Implementation is identical to GuardKit, just in different repository.

**Keep it simple**: Same philosophy as TASK-SHA-003 - basic functionality, no elaborate error handling.
