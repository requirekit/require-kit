# RequireKit

**Requirements management toolkit using EARS notation, BDD/Gherkin, and epic/feature hierarchy.**

RequireKit provides a structured approach to capturing, formalizing, and organizing software requirements. It uses proven methodologies including EARS notation for clear requirements, BDD/Gherkin for test specifications, and a hierarchical structure for project organization.

## Key Features

- **EARS Notation**: Five clear patterns for unambiguous requirements specification
- **BDD/Gherkin Generation**: Automatic test scenarios from requirements
- **Epic/Feature Hierarchy**: Structured organization with full traceability
- **Technology Agnostic**: Markdown-driven, works with any implementation system
- **Optional Integration**: Pairs with [guardkit](https://github.com/guardkit/guardkit) for task execution workflow

## Quick Start

New to RequireKit? Start here:

- **[Quickstart Guide](getting-started/quickstart.md)** - Get up and running in 5 minutes
- **[Installation](getting-started/installation.md)** - Install RequireKit in your environment
- **[EARS Notation](core-concepts/ears-notation.md)** - Learn the five requirement patterns

## Documentation Sections

### 📚 [Getting Started](getting-started/index.md)
Installation, quickstart, and your first requirements workflow.

### 🎯 [Core Concepts](core-concepts/index.md)
Learn EARS notation, BDD generation, epic/feature hierarchy, and requirements traceability.

### 📖 [User Guides](guides/README.md)
Comprehensive guides for requirements gathering, EARS formalization, and BDD scenario generation.

### ⌨️ [Commands Reference](commands/index.md)
Detailed documentation for all RequireKit commands: requirements, epics, features, and hierarchy.

### 🔗 [Integration](INTEGRATION-GUIDE.md)
Standalone use or integration with guardkit and PM tools (Jira, Linear, GitHub Projects, Azure DevOps).

### 📋 [Quick Reference](quick-reference/README.md)
Cheat sheets and quick reference cards for common workflows.

### 💡 [Examples](examples/index.md)
Sample requirements, BDD scenarios, and epic/feature structures.

### 🛠️ [Developer Docs](developer/index.md)
Architecture, ADRs, contributing guidelines, and templates.

### 🔧 [Troubleshooting & FAQ](troubleshooting/index.md)
Common issues, solutions, and frequently asked questions.

## Typical Workflow

```bash
# 1. Gather requirements through interactive Q&A
/gather-requirements

# 2. Formalize with EARS notation
/formalize-ears

# 3. Generate BDD scenarios
/generate-bdd

# 4. Organize into epics and features
/epic-create "User Management System"
/feature-create "User Authentication" epic:EPIC-001

# 4.5. Refine iteratively
/epic-refine EPIC-001
/feature-refine FEAT-001

# 5. View hierarchy
/hierarchy-view EPIC-001
```

## EARS Notation Patterns

RequireKit uses five EARS (Easy Approach to Requirements Syntax) patterns:

1. **Ubiquitous**: `The [system] shall [behavior]` - For requirements that always apply
2. **Event-Driven**: `When [trigger], the [system] shall [response]` - For event-triggered requirements
3. **State-Driven**: `While [state], the [system] shall [behavior]` - For state-dependent requirements
4. **Unwanted Behavior**: `If [error], then the [system] shall [recovery]` - For error handling
5. **Optional Feature**: `Where [feature], the [system] shall [behavior]` - For optional features

[Learn more about EARS notation →](core-concepts/ears-notation.md)

## Package Status

RequireKit is a **standalone requirements management toolkit** with no dependencies:

- ✅ Fully functional independently
- ✅ No required dependencies
- ✅ Optional integration with [guardkit](https://github.com/guardkit/guardkit)
- ✅ Bidirectional detection for enhanced workflows
- ✅ Technology agnostic outputs

Use RequireKit standalone for requirements management, or pair it with guardkit when you need task execution, quality gates, and automated testing workflows.

## Links

- [GitHub Repository](https://github.com/yourusername/require-kit)
- [Report an Issue](https://github.com/yourusername/require-kit/issues)
- [guardkit](https://github.com/guardkit/guardkit) - Task execution workflow system

## What's Next?

- 📖 [Read the Quickstart Guide](getting-started/quickstart.md)
- 🎯 [Learn EARS Notation](core-concepts/ears-notation.md)
- 📝 [Explore User Guides](guides/README.md)
- 💡 [See Examples](examples/index.md)

---

**Start with clear requirements. Ship with confidence.**
