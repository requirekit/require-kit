# require-kit

**Requirements management toolkit with EARS notation, BDD scenarios, and epic/feature hierarchy.**

## Overview

require-kit provides a structured approach to capturing, formalizing, and organizing software requirements. It uses proven methodologies including EARS notation for clear requirements, BDD/Gherkin for test specifications, and a hierarchical structure for project organization.

## Features

- **Interactive Requirements Gathering**: Conversational approach to capturing complete requirements
- **EARS Notation Formalization**: Convert natural language to structured, unambiguous requirements
- **BDD/Gherkin Scenario Generation**: Create testable scenarios from requirements
- **Epic/Feature Hierarchy Management**: Organize requirements into logical project structures
- **Requirements Traceability**: Clear links from epics to features to requirements
- **Technology Agnostic**: Works with any implementation system or project management tool

## Quick Start

### Gather Requirements

Start with an interactive Q&A session to capture requirements:

```bash
/gather-requirements
```

The system will guide you through questions to capture complete requirements for your feature or epic.

### Formalize with EARS

Convert your gathered requirements into structured EARS notation:

```bash
/formalize-ears
```

This creates clear, unambiguous requirements following five proven patterns.

### Generate BDD Scenarios

Create testable Gherkin scenarios from your requirements:

```bash
/generate-bdd
```

These scenarios provide acceptance criteria and can drive test implementation.

## EARS Notation Patterns

require-kit uses five EARS (Easy Approach to Requirements Syntax) patterns:

1. **Ubiquitous**: `The [system] shall [behavior]`
   - For requirements that always apply

2. **Event-Driven**: `When [trigger], the [system] shall [response]`
   - For requirements triggered by specific events

3. **State-Driven**: `While [state], the [system] shall [behavior]`
   - For requirements that apply in certain states

4. **Unwanted Behavior**: `If [error], then the [system] shall [recovery]`
   - For error handling and recovery requirements

5. **Optional Feature**: `Where [feature], the [system] shall [behavior]`
   - For optional or conditional features

## Epic/Feature Hierarchy

Organize your requirements hierarchically:

### Create an Epic

```bash
/epic-create "User Authentication System"
```

### Create a Feature

```bash
/feature-create "Login Functionality" epic:EPIC-001
```

### View Hierarchy

```bash
/hierarchy-view EPIC-001
```

## Project Structure

```
docs/
├── epics/                 # Epic specifications
├── features/              # Feature specifications
├── requirements/          # EARS requirements
└── bdd/                   # BDD/Gherkin scenarios

.claude/
├── agents/                # Specialized AI agents
│   ├── requirements-analyst.md
│   └── bdd-generator.md
└── commands/              # Command specifications
```

## Example Workflow

### 1. Gather Requirements

```bash
/gather-requirements
```

**System**: What feature would you like to specify?
**You**: User login functionality

**System**: What triggers this feature?
**You**: When a user enters credentials and clicks login

**System**: What should happen on success?
**You**: The user should be authenticated and redirected to dashboard

### 2. Formalize with EARS

```bash
/formalize-ears
```

**Output**:
```
REQ-001: When a user submits valid credentials, the system shall authenticate
         the user and redirect to the dashboard.

REQ-002: If authentication fails, then the system shall display an error
         message and remain on the login page.

REQ-003: While the user is authenticated, the system shall maintain the
         session for 24 hours.
```

### 3. Generate BDD Scenarios

```bash
/generate-bdd
```

**Output**:
```gherkin
Feature: User Authentication

  Scenario: Successful login
    Given a registered user with valid credentials
    When the user submits the login form
    Then the user should be authenticated
    And the user should be redirected to the dashboard

  Scenario: Failed login
    Given a user with invalid credentials
    When the user submits the login form
    Then an error message should be displayed
    And the user should remain on the login page
```

## Integration

require-kit focuses on requirements gathering and management. It provides structured requirements that can be integrated with:

- **Task Execution Systems**: Like [taskwright](https://github.com/yourusername/taskwright) for task workflow management
- **Project Management Tools**: Jira, Linear, GitHub Projects, Azure DevOps
- **Implementation Workflows**: Your team's development process
- **CI/CD Pipelines**: Automated testing from BDD scenarios

## Available Commands

### Requirements Management
- `/gather-requirements` - Interactive requirements gathering
- `/formalize-ears` - Convert to EARS notation
- `/generate-bdd` - Generate BDD scenarios

### Epic Management
- `/epic-create` - Create a new epic
- `/epic-status` - View epic status
- `/epic-sync` - Sync with external PM tools

### Feature Management
- `/feature-create` - Create a new feature
- `/feature-status` - View feature status
- `/feature-sync` - Sync with external PM tools

### Hierarchy
- `/hierarchy-view` - View epic/feature hierarchy

## Documentation

- [EARS Notation Guide](docs/guides/ears-notation.md) - Understanding EARS patterns
- [BDD Scenarios Guide](docs/guides/bdd-scenarios.md) - Writing effective scenarios
- [Epic/Feature Hierarchy](docs/guides/epic-feature-hierarchy.md) - Project organization

## Core Principles

1. **Start with Questions**: Use interactive gathering to capture complete requirements
2. **Formalize Early**: Convert to EARS notation while context is fresh
3. **Generate Scenarios**: Create BDD scenarios to validate understanding
4. **Organize Logically**: Structure into meaningful epics and features
5. **Maintain Traceability**: Always link requirements to features and epics

## Benefits

### Clear Requirements
- Unambiguous EARS notation
- Consistent format across projects
- Easy to review and validate

### Testable Specifications
- BDD scenarios provide acceptance criteria
- Can drive automated testing
- Clear definition of "done"

### Organized Structure
- Epic → Feature → Requirement hierarchy
- Complete traceability
- Easy navigation and maintenance

### Technology Agnostic
- Works with any implementation approach
- Integrates with any project management tool
- Supports any technology stack

## Best Practices

1. **Gather Requirements Interactively**: Don't skip the Q&A process - it captures crucial context
2. **One Requirement Per Statement**: Keep EARS requirements focused and atomic
3. **Link BDD to Requirements**: Always trace scenarios back to requirements
4. **Review Before Implementation**: Validate requirements with stakeholders early
5. **Update Documentation**: Keep requirements in sync with implementation changes

## Contributing

We welcome contributions! To add new features or improvements:

1. Use `/gather-requirements` to capture your proposed feature
2. Create EARS requirements with `/formalize-ears`
3. Generate BDD scenarios with `/generate-bdd`
4. Submit a PR with your changes

## License

MIT License - See LICENSE file for details

## Support

For questions or issues:
- Create a GitHub issue
- Check the documentation in `docs/guides/`
- Review example requirements in `docs/requirements/`

---

Built for clear requirements and structured specification.
