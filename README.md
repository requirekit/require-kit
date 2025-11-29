# require-kit

![Version](https://img.shields.io/badge/version-1.0.0-0366d6)
![License](https://img.shields.io/badge/license-MIT-28a745)
![Standalone](https://img.shields.io/badge/standalone-no%20dependencies-6f42c1)
![Optional Integration](https://img.shields.io/badge/integration-taskwright%20optional-ffd33d)
![Bidirectional Detection](https://img.shields.io/badge/detection-automatic-6f42c1)
[![Documentation](https://img.shields.io/badge/docs-online-blue)](https://requirekit.github.io/require-kit/)

**Requirements management toolkit with EARS notation, BDD scenarios, and epic/feature hierarchy.**

## Overview

require-kit provides a structured approach to capturing, formalizing, and organizing software requirements. It uses proven methodologies including EARS notation for clear requirements, BDD/Gherkin for test specifications, and a hierarchical structure for project organization.

## Package Status

require-kit is a **standalone requirements management toolkit** with no dependencies:

- **Fully Functional Independently**: Complete requirements gathering, EARS formalization, BDD generation, and epic/feature hierarchy management
- **No Required Dependencies**: Works entirely on its own without external packages
- **Optional Integration**: Can optionally integrate with [taskwright](https://github.com/taskwright-dev/taskwright) for task execution workflow
- **Bidirectional Detection**: Automatically detects taskwright if installed for enhanced workflow
- **Technology Agnostic**: Outputs work with any implementation system or project management tool

Use require-kit standalone for requirements management, or pair it with taskwright when you need task execution, quality gates, and automated testing workflows.

## Features

- **Interactive Requirements Gathering**: Conversational approach to capturing complete requirements
- **EARS Notation Formalization**: Convert natural language to structured, unambiguous requirements
- **BDD/Gherkin Scenario Generation**: Create testable scenarios from requirements
- **Epic/Feature Hierarchy Management**: Organize requirements into logical project structures
- **Requirements Traceability**: Clear links from epics to features to requirements
- **Technology Agnostic**: Works with any implementation system or project management tool

### PM Tool Integration Status

**Specification Ready**: Epic and feature files include structured frontmatter with metadata fields for PM tool integration (Jira, Linear, GitHub Projects, Azure DevOps). Command specifications define the integration patterns. Actual API integration requires:
- User implementation of API connectors
- MCP server for PM tool integration
- Custom export scripts using the structured metadata

The structured format makes it straightforward to build custom integrations or use MCP servers when available.

## Documentation

📚 **[View Full Documentation](https://requirekit.github.io/require-kit/)**

Comprehensive guides for requirements management:
- [Getting Started](https://requirekit.github.io/require-kit/getting-started/) - Quick setup and first steps
- [EARS Notation](https://requirekit.github.io/require-kit/core-concepts/ears-notation/) - Understanding requirement patterns
- [BDD/Gherkin Generation](https://requirekit.github.io/require-kit/core-concepts/bdd-generation/) - Creating test scenarios
- [Epic/Feature Hierarchy](https://requirekit.github.io/require-kit/core-concepts/hierarchy/) - Organizing your requirements
- [Command Reference](https://requirekit.github.io/require-kit/commands/) - All available commands
- [Integration Guide](https://requirekit.github.io/require-kit/integration/pm-tools/) - PM tool integration
- [Troubleshooting](https://requirekit.github.io/require-kit/troubleshooting/) - Common issues and solutions

## 5 Minute Quickstart

### Quick Install (Recommended)

**For macOS/Linux:**

```bash
curl -sSL https://raw.githubusercontent.com/requirekit/require-kit/main/installer/scripts/install.sh | bash
```

**Windows (via WSL2):** First ensure WSL2 is installed, then run the same curl command in your WSL2 terminal.

### Clone Repository Method

Prefer to clone the source code?

```bash
git clone https://github.com/requirekit/require-kit.git
cd require-kit
chmod +x installer/scripts/install.sh
./installer/scripts/install.sh
```

### Initialize Your Project

Navigate to your project directory and create the documentation structure:

```bash
cd /path/to/your/project
mkdir -p docs/{epics,features,requirements,bdd}
```

Alternatively, require-kit commands (`/gather-requirements`, `/formalize-ears`, etc.) are automatically available in Claude Code after installation - no manual project initialization needed.

---

📚 **For detailed setup instructions, see the [Getting Started Guide](https://requirekit.github.io/require-kit/getting-started/)**

## Usage

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

## Integration and Standalone Use

require-kit is a **standalone requirements management toolkit** that works independently or integrates seamlessly with other tools:

### Standalone Capabilities
- ✅ Requirements gathering and EARS notation formalization
- ✅ Epic/Feature hierarchy management
- ✅ BDD/Gherkin scenario generation
- ✅ Task specification generation from features
- ✅ Structured metadata for PM tool integration (specification ready)
- ✅ Requirements traceability and documentation

### Optional Integration
When you need task execution workflow (implementation, testing, quality gates):
- **Task Execution**: Install [taskwright](https://github.com/taskwright-dev/taskwright) for TDD workflow, automated testing, and quality gates
- **Bidirectional Detection**: Both packages detect each other automatically via marker files
- **No Hard Dependencies**: Each package works fully independently

### Integration Flow
```
require-kit (Standalone)          taskwright (Optional)
├── Requirements Gathering
├── EARS Formalization
├── BDD Scenario Generation
├── Epic/Feature Hierarchy
├── Task Specifications    ─────► Task Execution (/task-work)
└── Structured PM Metadata ─────► Quality Gates & Testing
```

## Available Commands

### Requirements Management
- `/gather-requirements` - Interactive requirements gathering
- `/formalize-ears` - Convert to EARS notation
- `/generate-bdd` - Generate BDD scenarios

### Epic Management
- `/epic-create` - Create a new epic with structured metadata
- `/epic-status` - View epic status and hierarchy
- `/epic-sync` - PM tool sync (specification provided, implementation required)

### Feature Management
- `/feature-create` - Create a new feature linked to epic
- `/feature-status` - View feature status and progress
- `/feature-sync` - PM tool sync (specification provided, implementation required)

### Hierarchy
- `/hierarchy-view` - View epic/feature hierarchy

## Documentation

- [Integration Guide](docs/INTEGRATION-GUIDE.md) - Using require-kit with taskwright
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
