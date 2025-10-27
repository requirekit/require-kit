---
id: TASK-001
title: "Create Agentecflow Lite Repository - Core Component Transfer"
created: 2025-10-19
status: backlog
priority: high
complexity: 8
epic: none
feature: none
requirements: []
parent_task: none
subtasks:
  - TASK-001A
  - TASK-001B
  - TASK-001C
  - TASK-001D
  - TASK-001E
  - TASK-001F
  - TASK-001G
  - TASK-001H
---

# TASK-001: Create Agentecflow Lite Repository - Core Component Transfer

## Overview

Create a new `agentecflow` repository containing ONLY the lightweight task workflow components, removing all requirements management features (EARS, BDD, Epic/Feature hierarchy) to reduce perceived complexity for open source adoption.

## Strategic Context

**Problem**: The full ai-engineer repo includes enterprise requirements features that create perceived complexity, potentially deterring pragmatic developers (as identified in the ThoughtWorks honest assessment).

**Solution**: Split into two repositories:
1. **agentecflow** (this task) - Lightweight task workflow with quality gates
2. **agentecflow-requirements** (future) - Full enterprise requirements management

**Target Audience**: Solo developers, small teams, pragmatic engineers who want AI-assisted development with quality guarantees but not formal requirements management.

## Architecture Decision

**Repository Strategy**: Create fresh repo with cherry-picked components (NOT full clone)

**Why Cherry-Pick vs Clone**:
- ✅ Clean git history without requirements feature commits
- ✅ Simpler file structure (no epic/feature directories)
- ✅ Smaller repository size
- ✅ Clear separation of concerns from day one

**Shared Code Strategy**: Core components will later be managed via git subtree in agentecflow-requirements repo.

## Subtask Breakdown

This task is broken into 8 subtasks, each suitable for `task-work --micro`:

### TASK-001A: Repository Setup and Basic Structure
- Create new GitHub repository `agentecflow`
- Initialize with README, LICENSE, .gitignore
- Create basic directory structure
- Set up branch protection rules

### TASK-001B: Transfer Core Commands
- Copy task-work.md, task-create.md, task-complete.md, task-status.md
- Remove all references to epic/feature linking
- Update command documentation for lite workflow

### TASK-001C: Transfer Core Agents
- Copy architectural-reviewer, test-verifier, code-reviewer, task-manager
- Copy supporting agents: complexity-evaluator, build-validator, test-orchestrator
- Remove references to requirements/BDD in agent prompts

### TASK-001D: Transfer Implementation Library
- Copy installer/global/commands/lib/ directory
- Remove requirements-related modules (feature_generator, etc.)
- Keep quality gate implementation (Phase 2.5, 4.5)
- Update imports and dependencies

### TASK-001E: Transfer Stack Templates
- Copy all template directories (react, python, maui-appshell, etc.)
- Update CLAUDE.md in each template (remove requirements references)
- Keep stack-specific agents
- Remove epic/feature directory structures from templates

### TASK-001F: Transfer Installer Scripts
- Copy install.sh, install-global.sh, init-project.sh
- Modify to install only lite components
- Remove epic/feature/requirements directory creation
- Update symlink creation logic

### TASK-001G: Create Lite Documentation
- Write new README.md (lite-focused, 5-minute quickstart)
- Create docs/QUICKSTART.md
- Create docs/QUALITY-GATES.md (Phase 2.5, 4.5 explained)
- Create docs/STACK-TEMPLATES.md
- NO mention of EARS, BDD, epics, or features

### TASK-001H: Testing and Validation
- Test installation on fresh system
- Verify all commands work without requirements features
- Test each stack template
- Run quality gate tests
- Document any issues found

## Component Classification

### ✅ INCLUDE (Lite Core)

**Commands**:
- task-create.md
- task-work.md
- task-complete.md
- task-status.md
- task-refine.md (optional, evaluate if needed)
- figma-to-react.md (UX integration)
- zeplin-to-maui.md (UX integration)
- debug.md (development tool)

**Agents**:
- architectural-reviewer.md ⭐ (Phase 2.5)
- test-verifier.md ⭐ (Phase 4.5)
- test-orchestrator.md ⭐ (Phase 4.5 support)
- code-reviewer.md ⭐ (Phase 5)
- task-manager.md ⭐ (core orchestration)
- complexity-evaluator.md (Phase 2.7)
- build-validator.md (quality gates)
- debugging-specialist.md
- devops-specialist.md
- database-specialist.md
- security-specialist.md
- pattern-advisor.md
- python-mcp-specialist.md
- figma-react-orchestrator.md
- zeplin-maui-orchestrator.md

**Library Modules** (installer/global/commands/lib/):
- checkpoint_display.py (Phase 2.6)
- plan_persistence.py (design-first workflow)
- plan_modifier.py (Phase 2.7)
- review_modes.py (quick/full review)
- user_interaction.py (human checkpoints)
- git_state_helper.py (task state management)
- agent_utils.py (agent coordination)
- micro_task_workflow.py (--micro flag)
- version_manager.py (compatibility)
- error_messages.py (user feedback)
- upfront_complexity_adapter.py (complexity evaluation)
- plan_markdown_parser.py (plan parsing)
- visualization.py (progress display)
- spec_drift_detector.py (quality monitoring)
- plan_audit.py (plan validation)
- metrics/ (usage tracking)

**Templates**:
- default/
- react/
- python/
- typescript-api/
- maui-appshell/
- maui-navigationpage/
- dotnet-microservice/
- fullstack/

**Installer Scripts**:
- install.sh (MODIFIED for lite)
- install-global.sh (MODIFIED for lite)
- init-project.sh (MODIFIED for lite)
- uninstall.sh
- deploy-agents.sh

**Configuration**:
- manifest.json (MODIFIED - remove requirements capabilities)

### ❌ EXCLUDE (Requirements Features)

**Commands**:
- epic-create.md
- epic-status.md
- epic-sync.md
- epic-generate-features.md
- feature-create.md
- feature-status.md
- feature-sync.md
- feature-generate-tasks.md
- gather-requirements.md
- formalize-ears.md
- generate-bdd.md
- hierarchy-view.md
- portfolio-dashboard.md
- task-sync.md (PM tool integration)
- mcp-zeplin.md (if requirements-focused)

**Agents**:
- requirements-analyst.md
- bdd-generator.md

**Library Modules**:
- feature_generator.py
- (Any other requirements-specific modules)

**Documentation**:
- All references to EARS notation
- All references to BDD/Gherkin
- All references to Epic/Feature hierarchy
- All references to PM tool sync

## File Modifications Required

### manifest.json Changes

**REMOVE capabilities**:
```json
"capabilities": [
  "requirements-engineering",  ← REMOVE
  "bdd-generation",           ← REMOVE
  "quality-gates",            ← KEEP
  "state-tracking",           ← KEEP
  "kanban-workflow",          ← KEEP
  "task-management",          ← KEEP
  "test-verification"         ← KEEP
]
```

**UPDATE metadata**:
```json
{
  "name": "agentecflow",
  "version": "1.0.0",
  "description": "Lightweight AI-Assisted Development with Quality Gates",
  "homepage": "https://github.com/yourusername/agentecflow"
}
```

### task-create.md Changes

**REMOVE from frontmatter template**:
```yaml
epic: none          ← REMOVE this line
feature: none       ← REMOVE this line
requirements: []    ← REMOVE this line
```

**SIMPLIFY to**:
```yaml
id: TASK-XXX
title: ""
created: YYYY-MM-DD
status: backlog
priority: medium
complexity: 0
parent_task: none
subtasks: []
```

### task-work.md Changes

**REMOVE references to**:
- Epic/feature context loading
- Requirements linking
- BDD scenario validation
- PM tool synchronization prompts

**KEEP**:
- All phase execution (1, 2, 2.5, 2.6, 2.7, 3, 4, 4.5, 5)
- Quality gates
- Design-first workflow flags (--design-only, --implement-only)
- Micro task flag (--micro)
- All specialized agent orchestration

### Template CLAUDE.md Changes

**REMOVE sections**:
- Requirements Management
- EARS Notation
- BDD/Gherkin Scenarios
- Epic/Feature Hierarchy
- External PM Tool Integration

**KEEP sections**:
- Task Workflow
- Quality Gates (Phase 2.5, 4.5)
- Testing Patterns
- Stack-Specific Patterns
- Architecture Principles

### install.sh Changes

**REMOVE directory creation**:
```bash
# DELETE these lines:
mkdir -p docs/epics/{active,completed,cancelled}
mkdir -p docs/features/{active,in_progress,completed}
mkdir -p docs/requirements/{draft,approved,implemented}
mkdir -p docs/bdd
mkdir -p docs/state
```

**KEEP directory creation**:
```bash
mkdir -p tasks/{backlog,in_progress,in_review,blocked,completed}
mkdir -p .claude/{agents,commands,instructions}
mkdir -p docs/adr
```

## Success Criteria

### Functional Requirements

- [ ] Repository created and publicly accessible
- [ ] Installation completes without errors on macOS, Linux, Windows (WSL)
- [ ] All core commands work (`/task-create`, `/task-work`, `/task-complete`, `/task-status`)
- [ ] Quality gates execute correctly (Phase 2.5, 4.5)
- [ ] All stack templates initialize successfully
- [ ] No references to epic/feature/requirements in user-facing documentation
- [ ] No broken links or missing dependencies

### Quality Requirements

- [ ] README.md positioned for pragmatic developers (not enterprise)
- [ ] Documentation emphasizes "5-minute quickstart"
- [ ] Zero mentions of EARS, BDD, epics, features in core docs
- [ ] Installation completes in <2 minutes
- [ ] Learning curve: <1 hour for first task completion
- [ ] Git history clean (no requirements feature commits)

### Performance Requirements

- [ ] Repository size <50MB (excluding git history)
- [ ] Installation downloads <10MB
- [ ] Command execution <2 seconds (excluding implementation time)

## Testing Checklist

### Installation Testing

- [ ] Fresh macOS installation
- [ ] Fresh Ubuntu installation
- [ ] Fresh Windows WSL installation
- [ ] Installation with existing Claude Code setup
- [ ] Uninstall and reinstall (verify cleanup)

### Command Testing

- [ ] `/task-create "Simple feature"` - Creates task without epic/feature
- [ ] `/task-work TASK-001` - Executes all phases correctly
- [ ] `/task-work TASK-001 --micro` - Simplified workflow works
- [ ] `/task-work TASK-001 --design-only` - Design phase checkpoint
- [ ] `/task-work TASK-001 --implement-only` - Implementation from saved plan
- [ ] `/task-complete TASK-001` - Moves to completed/
- [ ] `/task-status` - Shows kanban board

### Quality Gate Testing

- [ ] Phase 2.5 (Architectural Review) - Evaluates SOLID/DRY/YAGNI
- [ ] Phase 2.6 (Human Checkpoint) - Triggers for complex tasks
- [ ] Phase 2.7 (Complexity Evaluation) - Routes to correct review mode
- [ ] Phase 4.5 (Test Enforcement) - Auto-fixes failing tests
- [ ] Phase 5 (Code Review) - Reviews implementation

### Template Testing

- [ ] React template: Initializes, compiles, tests pass
- [ ] Python template: Initializes, lints, tests pass
- [ ] TypeScript API template: Initializes, compiles, tests pass
- [ ] MAUI AppShell template: Initializes, compiles, tests pass
- [ ] MAUI NavigationPage template: Initializes, compiles, tests pass
- [ ] .NET Microservice template: Initializes, compiles, tests pass
- [ ] Default template: Initializes with language-agnostic structure

## Risk Mitigation

### Risk: Missing Dependencies

**Mitigation**: Each subtask includes explicit file lists and verification steps

### Risk: Broken Quality Gates

**Mitigation**: TASK-001D specifically focuses on lib/ transfer with testing

### Risk: Template Issues

**Mitigation**: TASK-001E includes per-template validation

### Risk: Documentation Gaps

**Mitigation**: TASK-001G creates comprehensive lite-focused docs

### Risk: Installation Failures

**Mitigation**: TASK-001H includes cross-platform testing matrix

## Timeline Estimate

**Per Subtask** (with `--micro`):
- TASK-001A: 1 hour (repo setup)
- TASK-001B: 2 hours (commands + testing)
- TASK-001C: 2 hours (agents + verification)
- TASK-001D: 3 hours (lib/ + dependencies)
- TASK-001E: 4 hours (templates + validation)
- TASK-001F: 2 hours (installer + testing)
- TASK-001G: 3 hours (documentation)
- TASK-001H: 3 hours (cross-platform testing)

**Total**: ~20 hours (2-3 days with focused work)

## Next Steps After Completion

1. **Public Announcement**: Announce agentecflow on relevant forums/communities
2. **Gather Feedback**: Track GitHub issues, discussions, user questions
3. **Iterate**: Use 30-60 days of feedback to refine
4. **Validate Metrics**: Track installation count, usage patterns, reported issues
5. **Plan Phase 2**: Only create agentecflow-requirements if lite version proves valuable

## Notes

- This task uses the **cherry-pick approach** (not clone) for clean git history
- Each subtask is designed for `task-work --micro` (complexity 3-4)
- Testing is distributed across subtasks rather than all at end
- Documentation emphasizes simplicity and pragmatism
- No enterprise positioning - that stays in agentecflow-requirements (future)

## Related Documents

- `/docs/research/honest-assessment-sdd-vs-ai-engineer.md` - Strategic rationale
- `/CLAUDE.md` - Current full system (reference for what to exclude)
- `/installer/global/manifest.json` - Current capabilities manifest
