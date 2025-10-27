---
id: TASK-033
title: Rebrand agentecflow-lite to dev-tasker - update init command and documentation
status: backlog
created: 2025-10-26T10:00:00Z
updated: 2025-10-26T10:00:00Z
priority: high
tags: [branding, documentation, cli, dev-tasker]
epic: null
feature: null
requirements: []
external_ids:
  jira: null
  linear: null
bdd_scenarios: []
test_results:
  status: pending
  coverage: null
  last_run: null
---

# Task: Rebrand agentecflow-lite to dev-tasker

## Context

We're splitting the main repository into two focused products:
1. **dev-tasker**: Agentecflow Lite product (lightweight task workflow)
2. **require-kit**: Requirements gathering product (EARS/BDD)

This task focuses on **dev-tasker only** - rebranding the Agentecflow Lite subset.

## Key Decisions

### What STAYS the same
- ✅ Configuration folder: `.agentecflow/` (keep this name)
- ✅ Global installation folder: `~/.agentecflow/` (keep this name)
- ✅ Core workflow and commands (just branding changes)

### What CHANGES
- 🔄 CLI command: `agentecflow init` → `dev-tasker init`
- 🔄 Product name in documentation: "Agentecflow Lite" → "dev-tasker"
- 🔄 References to the product positioning

## Description

Update the init command name and all documentation references to reflect the new "dev-tasker" branding for Agentecflow Lite, while keeping all configuration folder names as `.agentecflow/`.

## Acceptance Criteria

### 1. Init Command Branding
- [ ] Command renamed: `dev-tasker init` (was `agentecflow init`)
- [ ] Help text updated to reference "dev-tasker"
- [ ] Example output shows "dev-tasker" product name
- [ ] Error messages use "dev-tasker" branding

### 2. Documentation Updates
- [ ] CLAUDE.md: Update product name references
- [ ] README.md: Update to "dev-tasker" branding
- [ ] docs/guides/agentecflow-lite-workflow.md: Update title and references
- [ ] docs/research/agentecflow-lite-positioning-summary.md: Update product name
- [ ] All other markdown files referencing "agentecflow init" command

### 3. Configuration Folder (NO CHANGE)
- [ ] `.agentecflow/` folder name stays the same
- [ ] `~/.agentecflow/` global folder stays the same
- [ ] All internal references to `.agentecflow/` remain unchanged
- [ ] Documentation clarifies: "dev-tasker uses `.agentecflow/` for configuration"

### 4. Template References
- [ ] Template initialization examples use "dev-tasker init"
- [ ] Stack-specific guides updated (react, python, typescript-api, maui, dotnet-microservice)
- [ ] Installation guides reference "dev-tasker"

### 5. Positioning Documents
- [ ] Agentecflow Lite → dev-tasker in positioning summary
- [ ] Product comparison tables updated
- [ ] Marketing/description text updated

## Implementation Notes

### Files to Update

**Core Documentation:**
- `/CLAUDE.md` - Main project instructions
- `/README.md` - Repository readme
- `/docs/guides/agentecflow-lite-workflow.md` - Main workflow guide
- `/docs/research/agentecflow-lite-positioning-summary.md` - Positioning doc

**Command/Script Files:**
- `installer/scripts/init-project.sh` - If it contains command references
- Any CLI command definitions (to be identified)

**Additional Documentation:**
- Search all `.md` files for "agentecflow init" and update to "dev-tasker init"
- Search all `.md` files for "Agentecflow Lite" and update to "dev-tasker"

### What NOT to Change

**Keep These:**
- `.agentecflow/` folder references
- `~/.agentecflow/` global installation path
- Internal configuration file paths
- Variable names in code (unless they're user-facing)

### Search Strategy

```bash
# Find all references to update
grep -r "agentecflow init" . --include="*.md" --include="*.sh"
grep -r "Agentecflow Lite" . --include="*.md"

# Verify configuration paths NOT changed
grep -r "\.agentecflow" . --include="*.md" | wc -l  # Should stay same count
```

## Test Requirements

### 1. Command Execution Tests
- [ ] `dev-tasker init` command works (if implemented)
- [ ] Help output shows "dev-tasker" branding
- [ ] Error messages use "dev-tasker" name

### 2. Documentation Consistency Tests
- [ ] No remaining "agentecflow init" references (except historical/archived)
- [ ] "Agentecflow Lite" replaced with "dev-tasker" in active docs
- [ ] `.agentecflow/` references intact (not changed)

### 3. User Journey Tests
- [ ] New user can follow installation guide with "dev-tasker" branding
- [ ] Template initialization examples are clear
- [ ] No confusion between product name and config folder name

## Related Tasks

- TASK-034 (future): Rebrand to "require-kit" for requirements product
- TASK-001A: Original repo setup (for context)

## Definition of Done

- [ ] All "agentecflow init" → "dev-tasker init" in active documentation
- [ ] All "Agentecflow Lite" → "dev-tasker" in active documentation
- [ ] Configuration folder paths (`.agentecflow/`) unchanged
- [ ] Documentation clarifies config folder naming
- [ ] No broken references or inconsistencies
- [ ] User-facing examples use new branding consistently
