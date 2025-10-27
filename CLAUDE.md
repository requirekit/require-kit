# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## AI Engineer - Complete Agentecflow Implementation

This is the **AI-Engineer** project - a comprehensive implementation of the **Agentecflow software engineering lifecycle system** that transforms specifications into production-ready solutions through AI-augmented workflows.

**Full Agentecflow Implementation:**
- **Stage 1: Specification** - Interactive requirements gathering with EARS notation
- **Stage 2: Tasks Definition** - Epic/feature breakdown with automatic PM tool export
- **Stage 3: Engineering** - AI/human collaboration with comprehensive quality gates
- **Stage 4: Deployment & QA** - Production readiness with automated validation

### Core Principles

1. **Complete Agentecflow Workflow**: Full Stage 1-4 implementation with human checkpoints
2. **Epic → Feature → Task Hierarchy**: Three-tier project management with automatic progress rollup
3. **External PM Tool Integration**: Seamless sync with Jira, Linear, GitHub, Azure DevOps
4. **Quality-First Engineering**: Built-in testing, validation, and enterprise-grade quality gates
5. **Technology-Agnostic Base**: Core methodology works across all technology stacks
6. **AI/Human Collaboration**: Intelligent delegation with full human control retention

## Essential Commands

### Stage 1: Specification
```bash
/gather-requirements   # Interactive requirements gathering (Q&A)
/formalize-ears       # Convert requirements to EARS notation
/generate-bdd         # Generate BDD/Gherkin scenarios
```

### Stage 2: Tasks Definition
```bash
# Epic Management
/epic-create "Title" [export:jira,linear] [priority:high]
/epic-status [EPIC-XXX] [--hierarchy]

# Feature Management
/feature-create "Title" epic:EPIC-XXX [requirements:[REQ-001]]
/feature-generate-tasks FEAT-XXX [--interactive]

# Task Management
/task-create "Title" epic:EPIC-XXX feature:FEAT-XXX
```

### Stage 3: Engineering
```bash
/task-work TASK-XXX [--mode=standard|tdd|bdd]
/task-status [TASK-XXX] [--hierarchy]
/task-sync [TASK-XXX] [--rollup-progress]
```

**Enhanced Quality Assurance**:
- **Architectural Review (Phase 2.5)**: Evaluates SOLID, DRY, YAGNI before implementation (saves 40-50% time)
- **Test Enforcement (Phase 4.5)**: Auto-fixes failing tests (up to 3 attempts), ensures 100% pass rate
- **Context7 MCP Integration**: Automatically retrieves up-to-date library documentation during implementation, ensuring latest patterns and best practices are used (not just training data)

### Stage 4: Deployment & QA
```bash
/task-complete TASK-XXX [--interactive]
```

### Project Visualization
```bash
/hierarchy-view [EPIC-XXX] [--timeline] [--agentecflow]
/portfolio-dashboard [--business-value] [--risks]
```

**See**: `installer/global/commands/*.md` for complete command specifications.

## Agentecflow Lite: The Sweet Spot Workflow

**Agentecflow Lite** provides **80% of benefits with 20% of complexity** via `/task-work`.

**Key Features:**
- Automatic architectural review (Phase 2.5B)
- Zero-tolerance test enforcement (Phase 4.5)
- Complexity-based routing (simple auto-proceed, complex get checkpoints)
- Human approval for critical decisions (Phase 2.8)
- Plan auditing for scope creep detection (Phase 5.5)
- Markdown plans for human review

**When to Use:**
- Individual tasks (not full epics)
- Team size 1-3 developers
- Small-to-medium projects
- Speed with safety

**Upgrade to Full Agentecflow when:**
- Multi-epic projects (10+ features)
- Team size >5 developers
- Enterprise compliance required

**Complete Guide**: [Agentecflow Lite Workflow](docs/guides/agentecflow-lite-workflow.md)

### Task-Work Workflow Phases

```
Phase 1: Requirements Analysis
Phase 2: Implementation Planning (Markdown format)
Phase 2.5: Architectural Review (SOLID/DRY/YAGNI scoring)
Phase 2.7: Complexity Evaluation (0-10 scale)
Phase 2.8: Human Checkpoint (if complexity ≥7 or review required)
Phase 3: Implementation
Phase 4: Testing (compilation + coverage)
Phase 4.5: Test Enforcement Loop (auto-fix up to 3 attempts)
Phase 5: Code Review
Phase 5.5: Plan Audit (scope creep detection)
```

**Key Decision Points:**
- **Phase 2.7**: Auto-proceed (1-3) vs checkpoint (7-10)
- **Phase 2.8**: Approve/Modify/Simplify/Reject/Postpone
- **Phase 4.5**: Auto-fix vs block task
- **Phase 5.5**: Approve vs escalate

## Complexity Evaluation

**Two-Stage System:**
1. **Upfront (task-create)**: Decide if task should be split (threshold: 7/10)
2. **Planning (task-work)**: Decide review mode (auto/quick/full)

**Scoring (0-10 scale):**
- File Complexity (0-3): Based on number of files
- Pattern Familiarity (0-2): Known vs new patterns
- Risk Assessment (0-3): Low/medium/high risk
- Dependencies (0-2): Number of external dependencies

**Complexity Levels:**
- **1-3 (Simple)**: <4 hours, AUTO_PROCEED
- **4-6 (Medium)**: 4-8 hours, QUICK_OPTIONAL (30s timeout)
- **7-10 (Complex)**: >8 hours, FULL_REQUIRED (mandatory checkpoint)

**See**: [Complexity Management Workflow](docs/workflows/complexity-management-workflow.md)

## UX Design Integration

Converts design system files (Figma, Zeplin) into components with **zero scope creep**.

**Supported:**
- `/figma-to-react` - Figma → TypeScript React + Tailwind + Playwright
- `/zeplin-to-maui` - Zeplin → XAML + C# + platform tests

**6-Phase Saga:**
1. MCP Verification
2. Design Extraction
3. Boundary Documentation (12-category prohibition checklist)
4. Component Generation
5. Visual Regression Testing (>95% similarity)
6. Constraint Validation (zero tolerance)

**Quality Gates:**
- Visual fidelity: >95%
- Constraint violations: 0
- Compilation: 100%

**See**: [UX Design Integration Workflow](docs/workflows/ux-design-integration-workflow.md)

## Design-First Workflow

Optional flags for complex tasks requiring upfront design approval.

**Flags:**
- `--design-only`: Phases 1-2.8, stops at checkpoint, saves plan
- `--implement-only`: Phases 3-5, requires `design_approved` state
- (default): All phases 1-5 in sequence

**Use `--design-only` when:**
- Complexity ≥7
- High-risk changes (security, breaking, schema)
- Multi-person teams (architect designs, dev implements)
- Multi-day tasks

**See**: [Design-First Workflow](docs/workflows/design-first-workflow.md)

## Project Structure

```
.claude/                    # Configuration
├── agents/                # Specialized AI agents
├── commands/              # Command specifications
└── task-plans/            # Implementation plans (Markdown)

tasks/                      # Task management
├── backlog/
├── in_progress/
├── in_review/
├── blocked/
└── completed/

docs/                       # Documentation
├── epics/                 # Epic specifications
├── features/              # Feature specifications
├── requirements/          # EARS requirements
├── bdd/                   # BDD/Gherkin scenarios
├── guides/                # Workflow guides
└── workflows/             # Detailed workflows

installer/global/           # Global resources
├── agents/                # Core AI agents
├── commands/              # Command specs
├── instructions/          # Methodology
└── templates/             # Stack templates
```

## Installation & Setup

```bash
# Install
chmod +x installer/scripts/install.sh
./installer/scripts/install.sh

# Initialize with template
agentic-init [react|python|typescript-api|maui-appshell|maui-navigationpage|dotnet-microservice|default]
```

**Available Templates:**
- **default**: Language-agnostic with complete Agentecflow
- **react**: React + TypeScript + Next.js + Tailwind + Vitest + Playwright
- **python**: FastAPI + pytest + LangGraph + Pydantic
- **typescript-api**: NestJS + Result patterns + domain modeling
- **maui-appshell**: .NET MAUI + AppShell + MVVM + ErrorOr
- **maui-navigationpage**: .NET MAUI + NavigationPage + MVVM
- **dotnet-microservice**: .NET + FastEndpoints + REPR pattern

**Template Documentation:**
- [Domain Layer Pattern](docs/patterns/domain-layer-pattern.md) - Verb-based Domain operations
- [MAUI Template Selection](docs/guides/maui-template-selection.md) - AppShell vs NavigationPage
- [Creating Local Templates](docs/guides/creating-local-templates.md) - Team-specific templates

## Conductor Integration

Fully compatible with [Conductor.build](https://conductor.build) for parallel development.

**State Persistence Solved (TASK-031):** ✅
- Symlink architecture + auto-commit
- 100% state preservation across worktrees
- Zero manual intervention required

**Setup:**
```bash
./installer/scripts/install.sh  # Creates symlinks automatically
agentecflow doctor              # Verify integration
```

**How It Works:**
- Commands/agents: `~/.claude/* → ~/.agentecflow/*`
- State: `{worktree}/.claude/state → {main-repo}/.claude/state`
- All commands available in every worktree
- Automatic state sync across parallel sessions

**See**: [agentecflow_platform/docs/CONDUCTOR-INTEGRATION.md](../agentecflow_platform/docs/CONDUCTOR-INTEGRATION.md)

## Testing by Stack

**Python:**
```bash
pytest tests/ -v --cov=src --cov-report=term --cov-report=json
```

**TypeScript/JavaScript:**
```bash
npm test -- --coverage
```

**.NET:**
```bash
dotnet test --collect:"XPlat Code Coverage" --logger:"json"
```

## Quality Gates (Automatic with `/task-work`)

| Gate | Threshold | Action if Failed |
|------|-----------|-----------------|
| Compilation | 100% | Task → BLOCKED |
| Tests Pass | 100% | Auto-fix (3 attempts) then BLOCKED |
| Line Coverage | ≥80% | Request more tests |
| Branch Coverage | ≥75% | Request more tests |
| Architectural Review | ≥60/100 | Human checkpoint |
| Plan Audit | 0 violations | Variance review |

**Phase 4.5 Test Enforcement:**
1. Compilation check
2. Test execution
3. Failure analysis (if needed)
4. Auto-fix + re-run (up to 3 attempts)
5. Block if all attempts fail

**Phase 5.5 Plan Audit:**
- File count match (100%)
- Implementation completeness (100%)
- Scope creep detection (0 violations)
- LOC variance (±20% acceptable)
- Duration variance (±30% acceptable)

## Task States & Transitions

```
BACKLOG
   ├─ (task-work) ──────→ IN_PROGRESS ──→ IN_REVIEW ──→ COMPLETED
   │                            ↓              ↓
   │                        BLOCKED        BLOCKED
   │
   └─ (task-work --design-only) ─→ DESIGN_APPROVED
                                        │
                                        └─ (task-work --implement-only) ─→ IN_PROGRESS ──→ IN_REVIEW
```

**States:**
- **BACKLOG**: New task, not started
- **DESIGN_APPROVED**: Design approved (design-first workflow)
- **IN_PROGRESS**: Active development
- **IN_REVIEW**: All quality gates passed
- **BLOCKED**: Tests failed or quality gates not met
- **COMPLETED**: Finished and archived

## EARS Notation Patterns

1. **Ubiquitous**: `The [system] shall [behavior]`
2. **Event-Driven**: `When [trigger], the [system] shall [response]`
3. **State-Driven**: `While [state], the [system] shall [behavior]`
4. **Unwanted Behavior**: `If [error], then the [system] shall [recovery]`
5. **Optional Feature**: `Where [feature], the [system] shall [behavior]`

## Core AI Agents

**Global Agents:**
- **requirements-analyst**: EARS notation requirements
- **bdd-generator**: BDD/Gherkin scenarios
- **architectural-reviewer**: SOLID/DRY/YAGNI compliance review
- **task-manager**: Unified workflow management
- **test-verifier/orchestrator**: Test execution and quality gates
- **code-reviewer**: Code quality enforcement
- **software-architect**: System design decisions
- **devops-specialist**: Infrastructure patterns
- **security-specialist**: Security validation
- **database-specialist**: Data architecture

**Stack-Specific Agents:**
- API/Domain/Testing/UI specialists per technology stack

**See**: `installer/global/agents/*.md` for agent specifications.

## MCP Integration Best Practices

The system integrates with 4 MCP servers for enhanced capabilities:
- **context7**: Library documentation (automatically retrieved during implementation)
- **design-patterns**: Pattern recommendations (Phase 2.5A)
- **figma-dev-mode**: Figma design extraction (/figma-to-react)
- **zeplin**: Zeplin design extraction (/zeplin-to-maui)

**Optimization Status**: ✅ All MCPs optimized (4.5-12% context window usage)

**Token Budgets**:
- context7: 2000-6000 tokens (phase-dependent)
- design-patterns: ~5000 tokens (5 results), ~3000 per detailed pattern
- figma-dev-mode: Image-based (minimal token impact)
- zeplin: Design-based (minimal token impact)

**For detailed MCP usage guidelines**: [MCP Optimization Guide](docs/guides/mcp-optimization-guide.md)

## Development Best Practices

**Quality Standards:**
1. **NEVER implement** features not explicitly specified (zero scope creep)
2. **ALWAYS use `/task-work`** for implementation (handles review, testing, gates automatically)
3. **Trust architectural review** (Phase 2.5 catches issues before implementation)
4. **Trust test enforcement** (Phase 4.5 ensures 100% pass rate)
5. **Track everything in tasks** (complete traceability)

**Development Mode Selection:**
- **TDD**: Complex business logic (Red → Green → Refactor)
- **BDD**: User-facing features (Scenarios → Implementation)
- **Standard**: Straightforward implementations

**Architecture Compliance:**
- EARS notation for requirements
- BDD scenarios for user features
- Pattern consistency per stack
- Self-documenting code

## Key Workflows

**Epic-to-Implementation:**
```bash
# Stage 1: Specification
/gather-requirements → /formalize-ears

# Stage 2: Tasks Definition
/epic-create → /feature-create → /feature-generate-tasks → /task-create

# Stage 3: Engineering (Phases 1-5.5 automatic)
/task-work TASK-XXX

# Stage 4: Deployment
/task-complete TASK-XXX
```

**Team Collaboration:**
```bash
# Team lead
/task-status --dev-dashboard
/hierarchy-view --agentecflow
/portfolio-dashboard --resources

# Developer
/task-work TASK-XXX --with-context
/task-sync TASK-XXX --rollup-progress
```

**See**: [Complete Agentecflow Workflows](docs/workflows/complete-workflows.md)

## System Capabilities

✅ **Complete Agentecflow**: All 4 stages with human checkpoints
✅ **Epic → Feature → Task**: Three-tier hierarchy with progress rollup
✅ **Enterprise QA**: Multi-level gates, comprehensive testing, security
✅ **Visual Management**: Executive dashboards, hierarchy visualization
✅ **Multi-Stack Support**: React, Python, TypeScript, .NET MAUI, microservices
✅ **PM Tool Integration**: Jira, Linear, GitHub Projects, Azure DevOps

## External PM Tool Integration

**Supported Platforms:**
- **Jira**: Epic → Story → Sub-task
- **Linear**: Initiative → Feature → Issue
- **GitHub Projects**: Milestone → Issue → Linked Issue
- **Azure DevOps**: Epic → Feature → Task

**Capabilities:**
- Bidirectional sync
- Hierarchy preservation
- Progress rollup
- Conflict resolution

**MCP Integration:**
- Requirements MCP (EARS/BDD)
- PM Tools MCP (orchestration)
- Testing MCP (quality gates)
- Deployment MCP (Stage 4)
- Code Analysis MCP (metrics)

## Iterative Refinement

**`/task-refine`**: Lightweight improvement without full re-work.

**Use for:**
- Minor code improvements
- Linting fixes
- Renaming/formatting
- Adding comments

**Don't use for:**
- New features (use `/task-work`)
- Architecture changes
- Major refactoring

**See**: [Iterative Refinement Guide](docs/guides/iterative-refinement-guide.md)

## Markdown Implementation Plans

All plans saved as human-readable Markdown in `.claude/task-plans/{task_id}-implementation-plan.md`.

**Benefits:**
- Human-reviewable (plain text)
- Git-friendly (meaningful diffs)
- Searchable (grep, ripgrep, IDE)
- Editable (manual edits before `--implement-only`)

## Quick Reference

**Command Specifications:** `installer/global/commands/*.md`
**Agent Definitions:** `installer/global/agents/*.md`
**Workflow Guides:** `docs/guides/*.md` and `docs/workflows/*.md`
**Stack Templates:** `installer/global/templates/*/`
**Testing Guides:** `docs/testing.md`

## Production Readiness ✅

Enterprise-ready with:
- Complete 4-stage Agentecflow implementation
- Scalable architecture (1 dev → enterprise portfolio)
- Enterprise-grade QA (testing, security, compliance)
- Business intelligence (ROI, resources, risk)
- Multi-stack support with specialized agents

**Ready for immediate deployment across teams of any size.**
