# Developer Documentation

Documentation for contributors and developers working on RequireKit.

## For Contributors

### [Architecture](architecture.md)
System architecture, design patterns, and technical decisions.

### [Architecture Decision Records](adr.md)
Historical record of important architectural decisions.

### [Contributing](contributing.md)
Guidelines for contributing code, documentation, or examples.

### [Templates](templates.md)
Templates and patterns for extending RequireKit.

## Quick Links

- **[System Architecture](architecture.md)** - High-level architecture overview
- **[ADR Index](adr.md)** - All architecture decisions
- **[Contributing Guide](contributing.md)** - How to contribute
- **[Templates](templates.md)** - Implementation templates

## Repository Structure

```
require-kit/
├── docs/                    # Documentation
│   ├── requirements/        # EARS requirements
│   ├── bdd/                # BDD scenarios
│   ├── epics/              # Epic specifications
│   ├── features/           # Feature specifications
│   └── guides/             # User guides
├── installer/              # Installation scripts
│   └── global/
│       ├── agents/         # Global agents
│       └── commands/       # Global commands
└── .claude/               # User-specific config (gitignored)
```

## Development Setup

1. Fork and clone the repository
2. Review architecture documentation
3. Check contributing guidelines
4. Make changes and test
5. Submit pull request

## Key Components

### Requirements Analyst Agent
Interactive Q&A for gathering requirements.

**Location:** `installer/global/agents/requirements-analyst.md`

### BDD Generator Agent
Generates Gherkin scenarios from EARS requirements.

**Location:** `installer/global/agents/bdd-generator.md`

### Epic/Feature Commands
Commands for hierarchy management.

**Location:** `installer/global/commands/`

## Next Steps

- 📐 [Review Architecture](architecture.md)
- 📋 [Read ADRs](adr.md)
- 🤝 [Contributing Guide](contributing.md)
- 📚 [Explore Templates](templates.md)
