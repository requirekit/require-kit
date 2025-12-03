# require-kit - Requirements Management System

## Project Context

This is a requirements management toolkit that uses EARS notation for clear requirements specification, BDD/Gherkin for test scenarios, and epic/feature hierarchy for project organization. The system focuses on requirements gathering and formalization, providing outputs that integrate with any implementation system.

## Core Principles

1. **Requirements First**: Clear, unambiguous EARS-notated requirements
2. **BDD Scenarios**: Generate testable Gherkin scenarios from requirements
3. **Traceability**: Clear links between epics, features, and requirements
4. **Technology Agnostic**: Works with any implementation system or PM tool
5. **Human Readable**: Markdown-driven for clarity and version control

## System Philosophy

- Start with clear requirements using EARS notation
- Generate testable BDD scenarios for validation
- Organize hierarchically: Epic → Feature → Requirement
- Maintain complete traceability
- Stay technology agnostic - focus on specification, not implementation

## Workflow Overview

1. **Gather Requirements**: Interactive Q&A sessions using `/gather-requirements`
2. **Formalize with EARS**: Convert to structured notation using `/formalize-ears`
3. **Generate BDD**: Create testable scenarios using `/generate-bdd`
4. **Organize**: Structure into epics/features using epic/feature commands
5. **Export**: Provide requirements to implementation systems

## Integration

require-kit focuses on requirements management. For task execution and implementation, integrate with:
- [guardkit](https://github.com/yourusername/guardkit) - Task execution workflow system
- Your project management tools (Jira, Linear, GitHub Projects)
- Your implementation workflows and CI/CD pipelines

## Getting Started

Run `/gather-requirements` to begin gathering requirements for a new feature or epic.
