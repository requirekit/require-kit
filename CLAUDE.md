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
- **epic-manager**: Epic/feature hierarchy management

**See**: `.claude/agents/*.md` for agent specifications.

## Integration

This toolkit focuses on requirements gathering and management. It provides:
- EARS-notated requirements for clear specification
- BDD/Gherkin scenarios for testing
- Epic/feature hierarchy for organization
- Traceability from requirements to features

For task execution and implementation, integrate with:
- [taskwright](https://github.com/yourusername/taskwright) - Task execution workflow system
- Your project management tools (Jira, Linear, GitHub Projects)
- Your implementation workflows and CI/CD pipelines

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

## Getting Started

Run `/gather-requirements` to begin gathering requirements for a new feature or epic. The system will guide you through interactive questions to capture complete requirements, which can then be formalized into EARS notation and BDD scenarios.

## Documentation

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
