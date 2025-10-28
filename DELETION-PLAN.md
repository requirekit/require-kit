# require-kit Deletion Plan

## Current Situation

The require-kit repository currently contains the **ENTIRE ai-engineer/agentecflow codebase**. We need to **DELETE** all task execution features and keep ONLY requirements management.

## What We Have Now

### Commands (24 total)
- ✅ 12 Requirements commands (gather-requirements, formalize-ears, generate-bdd, epic/feature management)
- ❌ 11 Task execution commands (task-create, task-work, task-complete, figma-to-react, etc.)
- ❌ 1 Debug command

### Agents (17 total)
- ✅ 2 Requirements agents (requirements-analyst, bdd-generator)
- ❌ 15 Execution agents (architectural-reviewer, test-verifier, task-manager, etc.)

### Templates
- ❌ 8 Stack templates (react, python, maui, typescript-api, dotnet-microservice, fullstack, default)

### Library
- ❌ Full task execution library (checkpoint, plan, complexity, quality gates)

### Tests
- ❌ Complete test suite for task execution

### Documentation
- ✅ Some requirements docs
- ❌ Extensive task execution guides, workflow docs, pattern docs

## What We Want (Target State)

### Commands (11-12 total)
- ✅ gather-requirements.md
- ✅ formalize-ears.md
- ✅ generate-bdd.md
- ✅ epic-create.md
- ✅ epic-status.md
- ✅ epic-sync.md
- ✅ epic-generate-features.md
- ✅ feature-create.md
- ✅ feature-status.md
- ✅ feature-sync.md
- ✅ feature-generate-tasks.md (evaluate)
- ✅ hierarchy-view.md

### Agents (2 total)
- ✅ requirements-analyst.md
- ✅ bdd-generator.md

### Templates
- (None - requirements toolkit doesn't need code templates)

### Library
- (Minimal or none - requirements logic in agents)

### Tests
- (Will rebuild minimal tests for requirements features later)

### Documentation
- ✅ EARS notation guide
- ✅ BDD scenarios guide
- ✅ Epic/feature hierarchy guide
- ✅ Integration guide
- ✅ Updated README focused on requirements
- ✅ Updated CLAUDE.md focused on requirements

## Deletion Task Series

### REQ-002: Delete Agentecflow Features (Parent)
- Overview of entire deletion process
- Estimated time: 3.5 hours total

### REQ-002A: Delete Task Execution Commands (0.5 hours)
**Delete**:
- task-create.md, task-work.md, task-complete.md, task-status.md, task-refine.md, task-sync.md
- figma-to-react.md, zeplin-to-maui.md, mcp-zeplin.md
- portfolio-dashboard.md, debug.md

**Keep**: 11-12 requirements/epic/feature commands

### REQ-002B: Delete Execution Agents (0.5 hours)
**Delete**:
- architectural-reviewer.md, test-verifier.md, test-orchestrator.md, code-reviewer.md
- task-manager.md, complexity-evaluator.md, build-validator.md
- debugging-specialist.md, devops-specialist.md, database-specialist.md
- security-specialist.md, pattern-advisor.md, python-mcp-specialist.md
- figma-react-orchestrator.md, zeplin-maui-orchestrator.md

**Keep**: requirements-analyst.md, bdd-generator.md

### REQ-002C: Delete Stack Templates and Library (1 hour)
**Delete**:
- ALL templates: react/, python/, typescript-api/, maui-appshell/, maui-navigationpage/, dotnet-microservice/, fullstack/, default/
- Entire lib/ directory (checkpoint, plan, complexity, quality gate modules)

**Keep**: None (requirements logic lives in agents)

### REQ-002D: Delete Tests and Build Artifacts (0.5 hours)
**Delete**:
- tests/ directory (entire test suite)
- coverage/ directory and coverage*.json files
- Build configs: package.json, tsconfig.json, vitest.config.ts, ai-engineer.sln, pytest.ini
- Test scripts: test_*.py, test-*.sh, validate-*.py, verify_*.py
- Development artifacts: DEVELOPMENT/, examples/, migrations/

**Keep**: .gitignore, requirements.txt (minimal)

### REQ-002E: Clean Documentation (1 hour)
**Delete**:
- Workflow guides: agentecflow-lite-workflow.md, complexity-management-workflow.md, design-first-workflow.md
- Template guides: creating-local-templates.md, maui-template-selection.md
- Pattern docs: domain-layer-pattern.md
- Task docs: TASK-*.md files
- workflows/ and patterns/ directories

**Update**:
- README.md → Focus on requirements management
- CLAUDE.md → Focus on requirements management

**Keep**:
- docs/requirements/, docs/epics/, docs/features/, docs/bdd/
- EXTRACTION-SUMMARY.md (historical record)

## Before/After Comparison

| Aspect | Before (ai-engineer) | After (require-kit) |
|--------|---------------------|-------------------|
| Commands | 24 | 11-12 |
| Agents | 17 | 2 |
| Templates | 8 stacks | 0 |
| Library | Full (20+ modules) | None or minimal |
| Tests | Full suite | Rebuild later |
| Focus | Task execution + requirements | Requirements only |
| Size | ~100MB+ | ~10MB |

## Expected Deletions Summary

- **Commands**: Delete 11-12 files (~50%)
- **Agents**: Delete 15 files (~88%)
- **Templates**: Delete 8 directories (100%)
- **Library**: Delete entire lib/ directory (100%)
- **Tests**: Delete entire tests/ directory (100%)
- **Build files**: Delete 10+ files (100%)
- **Documentation**: Delete ~10 guides, update 2 core files

## Repository Size Reduction

**Current**: ~100MB+ (full agentecflow with tests, coverage, templates)
**Target**: ~10MB (requirements management only)
**Reduction**: ~90% smaller

## Next Steps

1. Review REQ-002 series tasks (REQ-002A through REQ-002E)
2. Execute deletions in sequence:
   - REQ-002A: Delete task commands
   - REQ-002B: Delete execution agents
   - REQ-002C: Delete templates and library
   - REQ-002D: Delete tests and build artifacts
   - REQ-002E: Clean documentation
3. Commit after each subtask
4. Verify final state
5. Update README and CLAUDE.md
6. Test requirements workflow

## Safety Notes

- ✅ Parent repo at `/Users/richardwoollcott/Projects/appmilla_github/require-kit` has full backup
- ✅ Working in conductor worktree at `.conductor/geneva/`
- ✅ Can always recover from git history
- ✅ Committing after each deletion subtask for safety

## Timeline

**Total estimated time**: 3.5 hours
- REQ-002A: 0.5 hours
- REQ-002B: 0.5 hours
- REQ-002C: 1 hour
- REQ-002D: 0.5 hours
- REQ-002E: 1 hour

Ready to execute!
