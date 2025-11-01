# require-kit

**Requirements management toolkit with EARS notation, BDD scenarios, and epic/feature hierarchy.**

## Overview

require-kit provides a structured approach to gathering, formalizing, and managing software requirements. It uses industry-standard EARS notation for requirements specification and generates BDD/Gherkin scenarios for testing.

## Features

- **Interactive Requirements Gathering**: Guided Q&A sessions to capture complete requirements
- **EARS Notation Formalization**: Convert requirements to standardized EARS patterns
- **BDD/Gherkin Scenario Generation**: Automatically generate testable scenarios from requirements
- **Epic/Feature Hierarchy Management**: Organize requirements into structured hierarchies
- **Requirements Traceability**: Clear links between epics, features, and requirements
- **Technology Agnostic**: Works with any implementation system

## Quick Start

### Gather Requirements

Interactive requirements gathering through Q&A:

```bash
/gather-requirements
```

### Formalize with EARS

Convert gathered requirements to EARS notation:

```bash
/formalize-ears
```

### Generate BDD Scenarios

Create Gherkin scenarios from EARS requirements:

```bash
/generate-bdd
```

## EARS Notation Patterns

The system uses five EARS patterns for requirements:

1. **Ubiquitous**: `The [system] shall [behavior]`
2. **Event-Driven**: `When [trigger], the [system] shall [response]`
3. **State-Driven**: `While [state], the [system] shall [behavior]`
4. **Unwanted Behavior**: `If [error], then the [system] shall [recovery]`
5. **Optional Feature**: `Where [feature], the [system] shall [behavior]`

## Epic/Feature Hierarchy

Organize requirements into structured hierarchies:

```bash
# Create an epic
/epic-create "User Authentication System"

# Create a feature within the epic
/feature-create "Login Functionality" epic:EPIC-001

# View the hierarchy
/hierarchy-view EPIC-001
```

## Documentation Structure

```
docs/
├── requirements/         # EARS requirements
├── epics/               # Epic specifications
├── features/            # Feature specifications
└── bdd/                # BDD/Gherkin scenarios
```

## Integration

require-kit can be used standalone or integrated with task execution systems. It focuses on the specification phase of software development, providing clear, testable requirements that can feed into any implementation workflow.

### Integration with Task Systems

When integrated with task execution systems (like Agentecflow), require-kit provides:
- Requirements context for task implementation
- BDD scenarios for behavior-driven development
- Epic/feature hierarchy for project organization
- Traceability from requirements to implementation

## Core Principles

1. **Requirements First**: Every feature starts with clear EARS-notated requirements
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

## Example Workflow

```bash
# 1. Gather requirements interactively
/gather-requirements

# 2. Formalize into EARS notation
/formalize-ears

# 3. Generate BDD scenarios
/generate-bdd

# 4. Organize into epics/features
/epic-create "User Management"
/feature-create "Authentication" epic:EPIC-001

# 5. Export to task system or use requirements directly
```

## Documentation

- [EARS Notation Guide](docs/guides/ears-notation.md) - Understanding EARS patterns
- [BDD Scenarios Guide](docs/guides/bdd-scenarios.md) - Creating effective scenarios
- [Epic/Feature Hierarchy](docs/guides/epic-feature-hierarchy.md) - Organizing requirements

## Benefits

### Clear Requirements
- **Standardized notation** (EARS) for consistency
- **Unambiguous specifications** reduce implementation errors
- **Testable scenarios** (BDD/Gherkin) for validation

### Better Organization
- **Epic/feature hierarchy** provides structure
- **Traceability** from requirements to implementation
- **Version control** friendly (markdown-based)

### Team Collaboration
- **Shared understanding** through clear requirements
- **Stakeholder communication** via BDD scenarios
- **Integration ready** for task systems

## License

MIT License - See LICENSE file for details

## Support

For questions or issues, please create a GitHub issue.

---

Built for clear, testable, traceable requirements.
