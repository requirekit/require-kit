# Frequently Asked Questions

Common questions about RequireKit.

## General Questions

### What is RequireKit?

RequireKit is a requirements management toolkit using EARS notation for clear requirements, BDD/Gherkin for test scenarios, and epic/feature hierarchy for organization.

### Do I need taskwright to use RequireKit?

No. RequireKit is fully functional standalone. taskwright is optional and adds task execution workflow, quality gates, and automated testing.

[Learn more about integration →](getting-started/integration.md)

### What are EARS patterns?

EARS (Easy Approach to Requirements Syntax) provides five patterns for writing unambiguous requirements: Ubiquitous, Event-Driven, State-Driven, Unwanted Behavior, and Optional Feature.

[Learn more about EARS →](core-concepts/ears-notation.md)

## Installation & Setup

### How do I install RequireKit?

```bash
git clone https://github.com/yourusername/require-kit.git
cd require-kit
./installer/scripts/install.sh
```

[Full installation guide →](getting-started/installation.md)

### Where are requirements stored?

Requirements are stored as markdown files in your project's `docs/` directory:
- `docs/requirements/` - EARS requirements
- `docs/bdd/` - BDD scenarios
- `docs/epics/` - Epic specifications
- `docs/features/` - Feature specifications

### Can I use RequireKit with existing projects?

Yes. Run `/require-kit init` in your project to create the directory structure, then start gathering requirements.

## Usage Questions

### How do I gather requirements?

Use the `/gather-requirements` command for interactive Q&A:

```bash
/gather-requirements feature-name
```

[Complete workflow guide →](getting-started/quickstart.md)

### How do I generate BDD scenarios?

After formalizing requirements with EARS notation, run:

```bash
/generate-bdd
```

[Learn about BDD →](core-concepts/bdd-scenarios.md)

### Can I export to Jira/Linear?

Yes. RequireKit provides structured metadata for PM tool export:

```bash
/feature-sync FEAT-001 --jira
/feature-sync FEAT-001 --linear
```

[Learn about PM tool integration →](integration/pm-tools.md)

## Integration Questions

### How does RequireKit integrate with taskwright?

Both packages detect each other via marker files. When both are installed, RequireKit can generate task specifications, and taskwright can load requirement context during execution.

[Complete integration guide →](INTEGRATION-GUIDE.md)

### Do I need MCP servers?

No. MCP servers are optional and only needed if you want to extract requirements from design tools (Figma, Zeplin).

[Learn about MCP setup →](mcp-setup/index.md)

## Technical Questions

### What file format does RequireKit use?

Markdown files with YAML frontmatter. This is:
- Human-readable
- Version-control friendly (Git)
- Tool-agnostic
- Easy to parse

### Can I edit requirements manually?

Yes. All files are plain markdown and can be edited with any text editor.

### How does traceability work?

Requirements link to features via frontmatter metadata, creating a traceable hierarchy from epics to implementation.

[Learn about traceability →](core-concepts/traceability.md)

## Troubleshooting

### Commands not found after installation

Add `~/.agentecflow/bin` to your PATH and reload your shell.

[Installation troubleshooting →](getting-started/installation.md#troubleshooting)

### Integration not detected

Verify both marker files exist:
```bash
ls ~/.agentecflow/*.marker
```

[Integration troubleshooting →](INTEGRATION-GUIDE.md#troubleshooting)

## More Questions?

- Check the [Troubleshooting Guide](troubleshooting/index.md)
- Review the [Integration Guide](INTEGRATION-GUIDE.md)
- Open an issue on [GitHub](https://github.com/yourusername/require-kit/issues)

---

**Can't find your question?** Open an issue on [GitHub](https://github.com/yourusername/require-kit/issues)
