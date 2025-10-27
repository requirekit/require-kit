# AI Engineer Documentation Guides

## 📚 Guide Index

Welcome to the AI Engineer documentation! These guides will help you understand and use the complete **Agentecflow Enterprise Software Engineering Lifecycle System** - a comprehensive specification-driven development platform with Epic → Feature → Task hierarchy, PM tool integration, and portfolio management.

## Core Guides

### 🎤 [Markdown Spec-Driven Development Presentation](MARKDOWN-SPEC-DRIVEN-DEVELOPMENT-PRESENTATION.md) **NEW!**
**Present to Your Team!** - Comprehensive presentation document explaining:
- What is markdown spec-driven development and why we use it
- Complete system overview with real examples
- Key advantages: parallel development, quality gates, traceability
- Competitive landscape (replaces 8 tools)
- Future enhancements roadmap
- Getting started guide for all roles
- **Perfect for team onboarding and stakeholder presentations**

### 🎯 [AI Engineer Complete User Guide](AI-ENGINEER-USER-GUIDE.md)
**Start Here!** - Comprehensive overview of the entire system including:
- System philosophy and architecture
- Complete development pipeline
- Task management with verification
- Requirements and BDD integration
- All commands with examples
- Best practices and troubleshooting

### 📋 [Kanban Workflow Guide](KANBAN-WORKFLOW-GUIDE.md)
Complete guide to the kanban task management system:
- Task lifecycle and states
- Mandatory test verification
- File organization
- Dashboard views
- Quality gates
- Workflow examples

### 🔄 [Task Integration Guide](TASK-INTEGRATION-GUIDE.md)
How tasks integrate with requirements and BDD:
- Requirements → BDD → Tasks pipeline
- Linking and traceability
- Test generation from specifications
- Coverage verification
- Integration patterns

## Reference Guides

### 📖 [Command Usage Guide](COMMAND_USAGE_GUIDE.md)
Detailed command reference with examples:
- All commands with full syntax
- Complete workflow examples
- Stack-specific commands
- Tips and best practices
- Troubleshooting

### ⚡ [Quick Reference](QUICK_REFERENCE.md)
Quick lookup for common tasks:
- Installation commands
- Stack features summary
- Quality gates
- Key patterns by stack
- Command shortcuts

## Enterprise Guides (New in v2.0)

### 🏢 [Enterprise Features Guide](ENTERPRISE-FEATURES-GUIDE.md)
**Complete enterprise capabilities overview:**
- Epic → Feature → Task hierarchy management
- PM tool integration (Jira, Linear, GitHub, Azure DevOps)
- Portfolio dashboard and executive reporting
- Progress rollup and stakeholder management
- Quality gates and validation workflows
- Agentecflow Stage 1-4 implementation

### 🔄 [v2.0 Migration Guide](V2-MIGRATION-GUIDE.md)
**Upgrade from v1.x to enterprise v2.0:**
- Migration strategies and timelines
- Command mapping and evolution
- Project structure changes
- PM tool integration setup
- Team migration best practices
- Troubleshooting common issues

## Specialized Guides

### 🔧 [.NET Stacks Integration](NET_STACKS_INTEGRATION.md)
Guide for .NET development:
- Microservice stack with FastEndpoints
- MAUI mobile development
- Either monad patterns
- Integration testing

### 📦 [Template Integration Summary](TEMPLATE_INTEGRATION_SUMMARY.md)
Overview of all stack templates:
- React with advanced patterns
- Python with LangGraph
- .NET microservices
- .NET MAUI mobile
- TypeScript API with NestJS (New)
- Full Stack React + Python (New)

### 🚀 [Agentecflow Task Management](agentic-flow-task-management-with-verification.md)
Detailed task management with verification:
- Test verification requirements
- Multi-language support
- Failure handling
- Implementation strategy

### 📝 [Task Creation Workflow](task-creation-implementation-workflow.md)
Step-by-step task creation:
- Creating tasks from requirements
- Implementation workflow
- Testing and verification
- Completion criteria

## Getting Started

### For Team Presentations
1. **Present** the **[Markdown Spec-Driven Development Presentation](MARKDOWN-SPEC-DRIVEN-DEVELOPMENT-PRESENTATION.md)** to your team
2. Explain the advantages: parallel development, quality guarantees, tool consolidation
3. Show the competitive landscape (replaces 8 tools, saves $10,000+/year)

### For New Users
1. Start with the **[AI Engineer Complete User Guide](AI-ENGINEER-USER-GUIDE.md)**
2. Review the **[Quick Reference](QUICK_REFERENCE.md)** for commands
3. Follow the examples in **[Command Usage Guide](COMMAND_USAGE_GUIDE.md)**

### For Task Management
1. Read the **[Kanban Workflow Guide](KANBAN-WORKFLOW-GUIDE.md)**
2. Understand **[Task Integration Guide](TASK-INTEGRATION-GUIDE.md)**
3. Practice with examples in the guides

### For Specific Stacks
- **React**: See React sections in guides
- **Python**: See Python sections in guides
- **.NET**: Read **[.NET Stacks Integration](NET_STACKS_INTEGRATION.md)**
- **MAUI**: Check MAUI sections in .NET guide

## Key Concepts

### The Agentecflow Pipeline
```
Stage 1: Requirements & Planning
  └─ Requirements → EARS → Epics → PM Tool Export

Stage 2: Feature & Task Definition
  └─ Features → BDD → Tasks → Automatic Generation

Stage 3: Engineering & Implementation
  └─ Development → Testing → Quality Gates → Progress Rollup

Stage 4: Deployment & QA
  └─ Validation → Completion → Portfolio Metrics → Sync
```

### Core Enterprise Commands
```bash
# Stage 1: Requirements & Planning
/gather-requirements    # Interactive requirements session
/formalize-ears        # Convert to EARS notation
/epic-create           # Create epic with PM tool integration

# Stage 2: Feature & Task Definition
/feature-create        # Create feature with epic linkage
/generate-bdd          # Create BDD scenarios
/task-create           # Create implementation tasks

# Stage 3: Engineering & Implementation
/task-work             # Unified implementation + testing
/task-status           # Monitor progress with hierarchy context

# Stage 4: Deployment & QA
/task-complete         # Complete with validation + rollup
/hierarchy-view        # View complete project hierarchy
/portfolio-dashboard   # Executive portfolio overview
```

### Quality Gates
- **Test Coverage**: ≥80%
- **Test Pass Rate**: 100%
- **Performance**: <30s execution
- **Complexity**: ≤10

## System Philosophy

> **"No task is complete until tests pass"**

The AI Engineer system enforces quality through:
1. **Formal specifications** (EARS requirements)
2. **Behavioral scenarios** (BDD/Gherkin)
3. **Mandatory verification** (tests must pass)
4. **Full traceability** (requirements → tests → results)

## Quick Links

### Installation
```bash
curl -sSL https://raw.githubusercontent.com/appmilla/ai-engineer/main/installer/scripts/install.sh | bash
```

### Initialize Project
```bash
agentecflow init [stack-name]
```

### Start Development
```bash
/gather-requirements
```

## Support

For issues or questions:
1. Check the troubleshooting sections in guides
2. Review examples in [Command Usage Guide](COMMAND_USAGE_GUIDE.md)
3. See recovery commands in [Kanban Workflow Guide](KANBAN-WORKFLOW-GUIDE.md)

## Contributing

To improve these guides:
1. Follow the existing structure
2. Include practical examples
3. Test all commands
4. Update the index

---

*These guides represent a complete specification-driven development system that ensures quality through mandatory test verification at every stage.*
