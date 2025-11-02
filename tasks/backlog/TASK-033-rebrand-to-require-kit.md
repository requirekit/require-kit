---
id: TASK-033
title: Rebrand to require-kit - update init command and documentation
status: backlog
created: 2025-10-26T10:00:00Z
updated: 2025-11-02T15:45:00Z
priority: high
tags: [branding, documentation, cli, require-kit, requirements-management]
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

# Task: Rebrand to require-kit

## Context

We're splitting the main repository into two focused products:
1. **taskwright**: Task execution product (lightweight task workflow) - separate repo
2. **require-kit**: Requirements gathering product (EARS/BDD) - this repo

This task focuses on **require-kit** - rebranding the requirements management subset as a standalone product.

## Key Decisions

### What STAYS the same
- ✅ Configuration folder: `.agentecflow/` (keep this name)
- ✅ Global installation folder: `~/.agentecflow/` (keep this name)
- ✅ Core workflow and commands (just branding changes)

### What CHANGES
- 🔄 CLI command: `agentecflow init` → `require-kit init` (if applicable)
- 🔄 Product name in documentation: References to full Agentecflow → "require-kit"
- 🔄 Product positioning: Focus on requirements management (EARS/BDD)
- 🔄 Remove task execution references (those belong in taskwright)

## Description

Update documentation to reflect the new "require-kit" branding for the requirements management product, focusing on EARS notation, BDD scenarios, and epic/feature hierarchy - while keeping all configuration folder names as `.agentecflow/`.

## Acceptance Criteria

### 1. Product Positioning
- [ ] README.md: Focus on requirements management (EARS/BDD/Epic/Feature)
- [ ] CLAUDE.md: Update to require-kit context
- [ ] Clear positioning: "Requirements management toolkit" not "task workflow"
- [ ] Remove references to task execution (that's taskwright)

### 2. Documentation Updates
- [ ] Product name: "require-kit" consistently used
- [ ] Focus areas highlighted: EARS notation, BDD scenarios, Epic/Feature hierarchy
- [ ] Remove task execution guides (move to taskwright if needed)
- [ ] Update examples to focus on requirements gathering
- [ ] Clear separation from taskwright (task execution product)

### 3. Configuration Folder (NO CHANGE)
- [ ] `.agentecflow/` folder name stays the same
- [ ] `~/.agentecflow/` global folder stays the same
- [ ] All internal references to `.agentecflow/` remain unchanged
- [ ] Documentation clarifies: "require-kit uses `.agentecflow/` for configuration"

### 4. Command References (If Applicable)
- [ ] Update init command references to "require-kit init" (if exists)
- [ ] Update command examples to focus on requirements commands
- [ ] `/gather-requirements`, `/formalize-ears`, `/generate-bdd` emphasized
- [ ] Remove or clarify task execution commands (those are taskwright)

### 5. Content Cleanup
- [ ] Remove Agentecflow Lite references
- [ ] Remove task workflow documentation (belongs in taskwright)
- [ ] Remove quality gates, Phase 2.5, 4.5 references (taskwright features)
- [ ] Keep only: Requirements, EARS, BDD, Epic/Feature management

## Implementation Notes

### Files to Update

**Core Documentation:**
- `/CLAUDE.md` - Update to require-kit context (requirements focus)
- `/README.md` - Update to require-kit branding and positioning
- Remove or relocate task execution documentation

**Content to Keep** (Requirements Management):
- EARS notation guides
- BDD/Gherkin scenario guides
- Epic/Feature hierarchy documentation
- Requirements gathering workflows
- `/gather-requirements`, `/formalize-ears`, `/generate-bdd` commands

**Content to Remove/Relocate** (Task Execution - belongs in taskwright):
- Task workflow guides (Agentecflow Lite workflow)
- Quality gates (Phase 2.5, 4.5)
- `/task-create`, `/task-work`, `/task-complete` references
- Complexity evaluation, test enforcement
- Template/stack-specific guides (if task-focused)

**Additional Documentation:**
- Search all `.md` files for "Agentecflow" and evaluate context
- Update positioning to "requirements management toolkit"
- Clarify separation: require-kit (requirements) vs taskwright (execution)

### What NOT to Change

**Keep These:**
- `.agentecflow/` folder references
- `~/.agentecflow/` global installation path
- Internal configuration file paths
- Variable names in code (unless they're user-facing)
- Requirements management commands (those are core to require-kit)

### Search Strategy

```bash
# Find references to evaluate
grep -r "Agentecflow" . --include="*.md" | grep -v archived | grep -v ".git"

# Find task execution references (to remove/relocate)
grep -r "task-work\|task-create\|Phase 2.5\|Phase 4.5\|quality gate" . --include="*.md"

# Find requirements commands (to keep and emphasize)
grep -r "gather-requirements\|formalize-ears\|generate-bdd" . --include="*.md"

# Verify configuration paths NOT changed
grep -r "\.agentecflow" . --include="*.md" | wc -l  # Should stay same count
```

## Test Requirements

### 1. Documentation Consistency Tests
- [ ] Product consistently referred to as "require-kit"
- [ ] Focus on requirements management is clear
- [ ] No task execution references (except as external integration with taskwright)
- [ ] `.agentecflow/` references intact (not changed)

### 2. Content Scope Tests
- [ ] EARS notation documentation present and clear
- [ ] BDD/Gherkin scenario guides present
- [ ] Epic/Feature hierarchy documentation present
- [ ] No quality gates, Phase 2.5, 4.5 references (taskwright features)
- [ ] No task workflow guides (belongs in taskwright)

### 3. User Journey Tests
- [ ] New user understands: require-kit = requirements management
- [ ] Clear examples of EARS formalization workflow
- [ ] Clear examples of BDD scenario generation
- [ ] Integration with taskwright explained (if applicable)
- [ ] No confusion about product boundaries

## Related Tasks

### require-kit (This Repo)
- REQ-001 series: Extraction tasks (archived - obsolete)
- REQ-002 series: Cleanup tasks (in progress)
- REQ-004: Optional feature layer (research)

### taskwright (Separate Repo)
- Task execution rebranding happens separately
- TASK-007: Epic → Task hierarchy implementation

## Definition of Done

- [ ] Product name "require-kit" used consistently
- [ ] README.md clearly positions as requirements management toolkit
- [ ] CLAUDE.md updated with require-kit context
- [ ] Focus areas clear: EARS, BDD, Epic/Feature hierarchy
- [ ] Task execution references removed or clarified as taskwright integration
- [ ] Configuration folder paths (`.agentecflow/`) unchanged
- [ ] Documentation clarifies config folder naming
- [ ] No broken references or inconsistencies
- [ ] User-facing examples focus on requirements gathering
- [ ] Clear separation from taskwright (task execution product)
