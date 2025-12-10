# require-kit - Requirements Management System

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Context

This is a requirements management toolkit using EARS notation for requirements, BDD/Gherkin for test specifications, and epic/feature hierarchy for organization. The system provides structured requirements gathering and formalization capabilities.

## Core Principles

1. **Requirements First**: Every feature starts with EARS-notated requirements
2. **BDD Scenarios**: Generate testable Gherkin scenarios from requirements
3. **Traceability**: Clear links between epics, features, and requirements
4. **Technology Agnostic**: Works with any implementation system
5. **Human Readable**: Markdown-driven for clarity and version control

## Essential Commands

### Requirements Gathering
```bash
/gather-requirements   # Interactive Q&A
/formalize-ears       # Convert to EARS notation
/generate-bdd         # Generate Gherkin scenarios
```

### Epic/Feature Management
```bash
/epic-create "Title"                        # Create an epic
/feature-create "Title" epic:EPIC-XXX       # Create a feature
/hierarchy-view EPIC-XXX                    # View hierarchy
```

## Interactive Clarification

Commands `/epic-create`, `/feature-create`, and `/formalize-ears` include optional clarifying questions to improve specifications. Use `--quick` flag to skip questions when parameters are provided directly.

See `docs/INTEGRATION-GUIDE.md` for clarification philosophy details.

## EARS Notation Patterns

1. **Ubiquitous**: `The [system] shall [behavior]`
2. **Event-Driven**: `When [trigger], the [system] shall [response]`
3. **State-Driven**: `While [state], the [system] shall [behavior]`
4. **Unwanted Behavior**: `If [error], then the [system] shall [recovery]`
5. **Optional Feature**: `Where [feature], the [system] shall [behavior]`

## Project Structure

```
docs/                       # Documentation
├── epics/                 # Epic specifications
├── features/              # Feature specifications
├── requirements/          # EARS requirements
├── bdd/                   # BDD/Gherkin scenarios
└── guides/                # User guides

.claude/                    # Configuration
├── agents/                # Specialized AI agents
└── commands/              # Command specifications
```

## Core AI Agents

**Requirements Agents:**
- **requirements-analyst**: EARS notation requirements gathering and formalization
- **bdd-generator**: BDD/Gherkin scenario generation from requirements

**Note**: Epic/feature hierarchy management is handled through slash commands (`/epic-create`, `/feature-create`, etc.) rather than a dedicated agent.

**See**: `installer/global/agents/*.md` for agent specifications.

## Package Status

require-kit is a **standalone requirements management toolkit** with no dependencies:

- **Fully Functional Independently**: Complete requirements gathering, EARS formalization, BDD generation, and epic/feature hierarchy management
- **No Required Dependencies**: Works entirely on its own without external packages
- **Optional Integration**: Can optionally integrate with [guardkit](https://github.com/guardkit/guardkit) for task execution workflow
- **Bidirectional Detection**: Automatically detects guardkit if installed for enhanced workflow
- **Technology Agnostic**: Outputs work with any implementation system or project management tool

Use require-kit standalone for requirements management, or pair it with guardkit when you need task execution, quality gates, and automated testing workflows.

## Integration and Standalone Use

**Standalone Capabilities:**
- ✅ EARS-notated requirements for clear specification
- ✅ BDD/Gherkin scenarios for testing
- ✅ Epic/feature hierarchy for organization
- ✅ Task specification generation from features
- ✅ Structured metadata for PM tool integration (specification ready)
- ✅ Traceability from requirements to features

**Optional Integration (No Hard Dependencies):**
- **Task Execution**: Install [guardkit](https://github.com/guardkit/guardkit) for TDD workflow, quality gates, and automated testing
- **PM Tools**: Epic/feature files include structured metadata ready for PM tool export. Actual API integration requires user implementation or MCP server integration
- **CI/CD**: BDD scenarios can drive automated testing pipelines
- **Bidirectional Detection**: Packages detect each other automatically via marker files

## System Philosophy

- **Start with clear requirements**: Use EARS notation for unambiguous specifications
- **Generate testable scenarios**: BDD/Gherkin for validation
- **Organize hierarchically**: Epic → Feature → Requirement structure
- **Maintain traceability**: Clear links throughout the hierarchy
- **Stay technology agnostic**: Focus on specification, not implementation

## Workflow Overview

1. **Gather Requirements**: Interactive Q&A sessions using `/gather-requirements`
2. **Formalize with EARS**: Convert to structured notation using `/formalize-ears`
3. **Generate BDD**: Create testable scenarios using `/generate-bdd`
4. **Organize**: Structure into epics/features using epic/feature commands
5. **Export**: Provide requirements to implementation systems

## Progressive Disclosure

RequireKit uses progressive disclosure to optimize context window usage while maintaining comprehensive documentation.

### How It Works

Agent files are split into:
1. **Core files** (`{name}.md`): Essential content always loaded
   - Quick Start examples
   - Boundaries (ALWAYS/NEVER/ASK)
   - EARS patterns
   - Core capabilities

2. **Extended files** (`{name}-ext.md`): Detailed reference loaded on-demand
   - Framework-specific examples
   - Domain patterns
   - Advanced techniques
   - Troubleshooting

### Loading Extended Content

When implementing detailed code or needing framework-specific guidance:

```bash
# For BDD generator extended content
cat installer/global/agents/bdd-generator-ext.md

# For requirements analyst extended content
cat installer/global/agents/requirements-analyst-ext.md
```

### Benefits

- **Reduced context size** - Core files contain essential content only
- **On-demand detail** - Extended content loaded when needed
- **Same comprehensive content** available when needed

## Getting Started

Run `/gather-requirements` to begin gathering requirements for a new feature or epic. The system will guide you through interactive questions to capture complete requirements, which can then be formalized into EARS notation and BDD scenarios.

## Documentation

- Integration guide: `docs/INTEGRATION-GUIDE.md` - Using with guardkit
- Requirements stored in `docs/requirements/`
- BDD scenarios stored in `docs/bdd/`
- Epic specifications stored in `docs/epics/`
- Feature specifications stored in `docs/features/`

## Best Practices

1. **Start with questions**: Use interactive gathering to capture complete requirements
2. **Formalize early**: Convert to EARS notation while context is fresh
3. **Generate scenarios**: Create BDD scenarios to validate understanding
4. **Organize logically**: Structure into meaningful epics and features
5. **Maintain traceability**: Always link requirements to features and epics
