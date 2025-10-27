# Agentecflow Lite vs Full: Comparison and Decision Guide

## Overview

Agentecflow comes in two flavors: **Lite** (embedded in `/task-work`) and **Full** (complete specification-driven development). This guide helps you choose the right approach for your project and understand the tradeoffs.

**Think of it as a spectrum:**

```
Plain AI Coding ←──────── Agentecflow Lite ──────────→ Full Agentecflow
(Cursor, Claude)        (SWEET SPOT)              (Enterprise SDD)

✗ No structure          ✓ Structured workflow      ✓ Complete traceability
✗ No quality gates      ✓ Quality gates           ✓ Comprehensive gates
✗ No verification       ✓ Automated testing       ✓ Multi-level validation
✓ Zero overhead         ✓ Minimal overhead        ✗ Heavy overhead
✓ Fast iteration        ✓ Fast with safety        ✗ Slow iteration
```

## Side-by-Side Comparison

| Feature | Agentecflow Lite | Full Agentecflow | Recommendation |
|---------|------------------|------------------|----------------|
| **Setup Time** | 5 minutes | 2-4 hours | Lite for quick start |
| **Per-Task Overhead** | 10-15 minutes | 30-60 minutes | Lite for agile teams |
| **EARS Requirements** | Optional | Required | Full for compliance |
| **BDD Scenarios** | Optional | Required | Full for behavior specs |
| **Epic/Feature Hierarchy** | Optional | Required | Full for large projects |
| **PM Tool Integration** | Manual | Automatic | Full for enterprise |
| **Quality Gate Coverage** | 80% (core gates) | 100% (all gates) | Lite for most teams |
| **Architectural Review** | Phase 2.5B only | Multi-phase | Lite sufficient |
| **Test Enforcement** | Phase 4.5 (3 attempts) | Phase 4.5 + Manual QA | Same in both |
| **Plan Audit** | Phase 5.5 (basic) | Phase 5.5 + Compliance | Lite for most |
| **Documentation Output** | Markdown plans | EARS + BDD + Plans | Full for regulation |
| **Agent Orchestration** | Single agent | Multi-agent | Full for complex |
| **MCP Server Required** | No | Yes (optional) | Lite for simplicity |
| **Team Size** | 1-5 developers | 5+ developers | Lite for small teams |
| **Project Scale** | 1-10 features | 10+ features, 3+ epics | Depends on complexity |
| **Compliance Needs** | Low | High (FDA, SOX, etc.) | Full for regulation |
| **Ideal For** | Startups, MVPs, agile | Enterprise, regulated | Match to context |

## When to Use Agentecflow Lite

### ✅ Perfect For

**Small to Medium Projects:**
- 1-10 features total
- 1-2 epics
- <50 tasks
- Single product or service

**Agile Development:**
- Fast iteration cycles (1-2 week sprints)
- Frequent releases
- MVP development
- Rapid prototyping

**Small Teams:**
- 1-5 developers
- Single team, co-located or remote
- No cross-functional dependencies
- Direct communication

**Minimal Compliance:**
- No regulatory requirements
- Internal tools
- SaaS products (non-healthcare, non-financial)
- Open source projects

**Quick Wins:**
- Bug fixes and hotfixes
- Feature enhancements
- Refactoring tasks
- Documentation updates

### Example: Startup SaaS Product

**Context:**
- 3 developers
- Building MVP for B2B SaaS
- 2-week sprints
- No compliance requirements

**Workflow:**
```bash
# Sprint planning: Create tasks
/task-create "Add OAuth2 authentication" requirements:[REQ-001]
/task-create "Implement user dashboard" requirements:[REQ-002]
/task-create "Add billing integration" requirements:[REQ-003]

# Development: Use Agentecflow Lite
/task-work TASK-001  # Auto-proceeds, quality gates enforced
/task-work TASK-002  # Architectural review, test enforcement
/task-work TASK-003  # Plan audit, scope creep detection

# Sprint review: All tasks completed with quality assurance
```

**Benefits:**
- ✅ Minimal overhead (10-15 min per task)
- ✅ Quality gates ensure no broken code
- ✅ Fast iteration (complete tasks in hours, not days)
- ✅ No heavy process (EARS/BDD optional)

**Tradeoffs:**
- ⚠️ Less formal documentation (no EARS requirements)
- ⚠️ Manual PM tool sync (no automatic Jira/Linear updates)
- ⚠️ Limited traceability (task → code, not requirement → code)

## When to Use Full Agentecflow

### ✅ Perfect For

**Large-Scale Projects:**
- 10+ features
- 3+ epics
- 100+ tasks
- Multiple products/services

**Enterprise Development:**
- Formal release cycles (quarterly, annually)
- Change control boards
- Architecture review boards
- Formal QA process

**Large Teams:**
- 5+ developers
- Multiple teams (frontend, backend, QA, DevOps)
- Cross-functional dependencies
- Remote or distributed teams

**High Compliance:**
- FDA regulated (medical devices, healthcare)
- SOX compliance (financial services)
- HIPAA compliance (healthcare data)
- ISO 27001, SOC 2 (security standards)

**Complex Requirements:**
- Safety-critical systems
- High-security systems
- Multi-tenant architectures
- Distributed systems

### Example: Healthcare Platform

**Context:**
- 20 developers across 4 teams
- FDA Class II medical device software
- Quarterly releases
- HIPAA compliance required
- Change control board approval

**Workflow:**
```bash
# Stage 1: Requirements gathering
/gather-requirements  # Interactive Q&A
/formalize-ears      # Convert to EARS notation (required for FDA)

# Stage 2: Epic/Feature planning
/epic-create "Patient Data Management" export:jira priority:critical
/feature-create "Secure Patient Records" epic:EPIC-001 requirements:[REQ-001,REQ-002]
/feature-generate-tasks FEAT-001 --interactive

# Stage 3: Implementation with full traceability
/task-work TASK-001 --mode=bdd --with-context --sync-progress
# Automatic Jira sync, full EARS → BDD → Code traceability

# Stage 4: QA and compliance validation
/task-complete TASK-001 --stage-transition --prepare-deployment
# Generates compliance artifacts, QA reports, deployment checklist
```

**Benefits:**
- ✅ Complete traceability (EARS → BDD → Code → Tests)
- ✅ Automatic PM tool sync (Jira, Linear)
- ✅ Compliance documentation (FDA audit trail)
- ✅ Multi-level quality gates (architectural, security, compliance)

**Tradeoffs:**
- ⚠️ Higher overhead (30-60 min per task)
- ⚠️ Slower iteration (requires approvals, reviews)
- ⚠️ Complex setup (2-4 hours initial configuration)
- ⚠️ Requires MCP servers (for PM tool integration)

## Decision Matrix

Use this matrix to determine which approach fits your needs:

### Project Scale

| Criteria | Lite | Full |
|----------|------|------|
| **Features** | <10 | ≥10 |
| **Epics** | <3 | ≥3 |
| **Tasks** | <50 | ≥50 |
| **Duration** | <6 months | ≥6 months |

### Team Size

| Criteria | Lite | Full |
|----------|------|------|
| **Developers** | 1-5 | 5+ |
| **Teams** | 1 | 2+ |
| **Locations** | Co-located | Distributed |
| **Communication** | Direct | Formal |

### Regulatory Requirements

| Criteria | Lite | Full |
|----------|------|------|
| **FDA** | No | Yes (required) |
| **SOX** | No | Yes (required) |
| **HIPAA** | No | Yes (required) |
| **ISO 27001** | No | Yes (required) |
| **SOC 2** | No | Yes (recommended) |

### Documentation Needs

| Criteria | Lite | Full |
|----------|------|------|
| **Requirements Docs** | Optional | Required |
| **BDD Scenarios** | Optional | Required |
| **Epic Specs** | Optional | Required |
| **Traceability Matrix** | Manual | Automatic |
| **Audit Trail** | Basic | Comprehensive |

### Example Decision Path

**Scenario 1: Early-Stage Startup**
- Features: 5 planned
- Team: 2 developers
- Compliance: None
- **Decision**: ✅ Agentecflow Lite

**Scenario 2: Healthcare SaaS (Mature)**
- Features: 25 across 4 epics
- Team: 12 developers
- Compliance: HIPAA
- **Decision**: ✅ Full Agentecflow

**Scenario 3: Enterprise Internal Tool**
- Features: 8 planned
- Team: 6 developers
- Compliance: SOX
- **Decision**: ✅ Full Agentecflow (compliance required)

**Scenario 4: Open Source Project**
- Features: 15 planned
- Team: 3 core contributors
- Compliance: None
- **Decision**: ✅ Agentecflow Lite (low overhead)

## Migration Path: Lite → Full

### Graduation Triggers

You should migrate from Lite to Full when ANY of these criteria are met:

**Scale Triggers:**
- ✅ 10+ features implemented
- ✅ 3+ epics created
- ✅ 50+ tasks completed
- ✅ Project duration >6 months

**Team Triggers:**
- ✅ 5+ developers join team
- ✅ 2+ teams working on same codebase
- ✅ Cross-functional dependencies increase
- ✅ Remote/distributed team structure

**Compliance Triggers:**
- ✅ Regulatory audit required
- ✅ Customer requests traceability
- ✅ Security certification needed (ISO, SOC 2)
- ✅ Contract requires formal documentation

**Quality Triggers:**
- ✅ Production incidents increase
- ✅ Scope creep becomes frequent
- ✅ Manual PM tool sync becomes burden
- ✅ Need for better project visibility

### Hybrid Approach (Recommended)

Instead of full migration, consider a **hybrid approach**:

**Use Lite for:**
- Individual tasks within epics
- Bug fixes and hotfixes
- Refactoring and technical debt
- Documentation updates

**Use Full for:**
- Epic and feature planning
- Requirements gathering and formalization
- PM tool synchronization
- Compliance documentation

**Example Hybrid Workflow:**

```bash
# Full Agentecflow: Epic/Feature level
/gather-requirements               # EARS notation (full)
/formalize-ears                   # Formal requirements
/epic-create "User Management"    # Epic planning (full)
/feature-create "Authentication"  # Feature specs (full)
/feature-generate-tasks FEAT-001  # Task breakdown

# Agentecflow Lite: Task level
/task-work TASK-001               # Lite workflow (fast)
/task-work TASK-002               # Lite workflow (fast)
/task-work TASK-003               # Lite workflow (fast)

# Full Agentecflow: Sync and reporting
/task-sync TASK-001 --rollup-progress  # Sync to Jira
/epic-status EPIC-001 --hierarchy      # Portfolio view
```

**Benefits of Hybrid:**
- ✅ Fast iteration at task level (Lite)
- ✅ Formal planning at epic level (Full)
- ✅ Traceability when needed (Full)
- ✅ Minimal overhead day-to-day (Lite)

### Migration Steps

**Step 1: Assess Current State**
```bash
# Count features and tasks
ls docs/features/active/ | wc -l
ls tasks/completed/ | wc -l

# Check team size
# Review compliance requirements
```

**Step 2: Install Full Agentecflow (if needed)**
```bash
# Install MCP servers for PM tools
npm install -g @agentecflow/jira-mcp
npm install -g @agentecflow/linear-mcp

# Configure settings
cp .claude/settings.json .claude/settings-full.json
# Edit settings-full.json with PM tool credentials
```

**Step 3: Migrate Existing Tasks (Optional)**
```bash
# Generate EARS requirements from completed tasks
/task-status --completed --export-ears > docs/requirements/migrated.md

# Generate feature specs from task groups
# This is manual but can be semi-automated
```

**Step 4: Start Using Full Workflow**
```bash
# New work uses full workflow
/gather-requirements
/formalize-ears
/epic-create "..." export:jira
```

**Step 5: Continue Lite for Task Execution**
```bash
# Task execution still uses Lite
/task-work TASK-XXX
# Benefits: Fast iteration, quality gates, no overhead change
```

## ROI Analysis

### Ceremony vs Value Tradeoff

**Agentecflow Lite:**
- **Ceremony**: 10-15 min per task (planning + execution)
- **Value**: Quality gates, architectural review, test enforcement
- **Net**: 80% of quality benefits, 20% of overhead

**Full Agentecflow:**
- **Ceremony**: 30-60 min per task (requirements + BDD + execution + sync)
- **Value**: Complete traceability, compliance docs, automated sync
- **Net**: 100% of quality benefits, 100% of overhead

**Break-Even Analysis:**

For a 50-task project:
- **Lite**: 50 tasks × 15 min = 12.5 hours overhead
- **Full**: 50 tasks × 45 min = 37.5 hours overhead
- **Difference**: 25 hours (3.1 days)

**When Full is Worth It:**
- Compliance audit saves 40+ hours
- PM tool sync saves 10+ hours
- Traceability prevents 1 production incident (saves days)

**When Lite is Better:**
- Fast iteration critical (MVP, startup)
- Low compliance needs (no audit, no regulation)
- Small team (direct communication)

### Data from Recent Tasks

**Agentecflow Lite Performance (TASK-007, TASK-025):**
- Average task completion: 45 minutes
- Quality gate pass rate: 92%
- Architectural review catch rate: 15% (prevented bad designs)
- Test enforcement success rate: 88% (12% required human fix)

**Full Agentecflow Performance (Healthcare Project):**
- Average task completion: 2.5 hours
- Compliance documentation: 100% generated
- PM tool sync: 100% automatic
- Audit trail: Complete (EARS → BDD → Code → Tests)

## Related Workflows

- **[Agentecflow Lite Workflow](../guides/agentecflow-lite-workflow.md)** - Complete Lite workflow guide
- **[Quality Gates Workflow](./quality-gates-workflow.md)** - Quality enforcement details
- **[Complexity Management Workflow](./complexity-management-workflow.md)** - Complexity evaluation
- **[Design-First Workflow](./design-first-workflow.md)** - Design approval process

## FAQ

**Q: Can I start with Lite and upgrade later?**
A: Yes! Hybrid approach is recommended. Use Lite for tasks, Full for epics as project grows.

**Q: Do I lose quality benefits with Lite?**
A: No. Lite has 80% of quality gates (architectural review, test enforcement, plan audit). Only missing: formal EARS/BDD docs and automatic PM sync.

**Q: Is Full Agentecflow required for FDA compliance?**
A: Yes. FDA requires formal requirements (EARS) and traceability. Lite doesn't generate these artifacts.

**Q: Can I use Lite with Jira/Linear?**
A: Yes, but sync is manual. Use `/task-sync` command or hybrid approach (Full for epic level, Lite for task level).

**Q: What's the minimum project size for Full?**
A: 10+ features, 3+ epics, or any compliance requirement. Below that, Lite is recommended.

**Q: Does Lite support multi-agent orchestration?**
A: No. Lite uses single agent per phase. Full supports multi-agent orchestration for complex scenarios.

**Q: Can I customize Lite workflow?**
A: Yes, via flags: `--design-only`, `--implement-only`, `--micro`. But core workflow is fixed.

**Q: Is there Agentecflow Medium?**
A: No, but hybrid approach achieves this: Full for planning, Lite for execution.
