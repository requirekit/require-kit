# RequireKit Documentation

This directory contains the source files for the RequireKit documentation site, built with [MkDocs](https://www.mkdocs.org/) and [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

## Documentation Structure

The documentation is organized according to the plan in `docs/planning/documentation-organization-plan.md`:

- **Getting Started**: Installation, quickstart, first requirements
- **Core Concepts**: EARS notation, BDD/Gherkin, hierarchy, traceability
- **User Guides**: Comprehensive guides for using RequireKit
- **Commands Reference**: Detailed command documentation
- **MCP Setup**: MCP server configuration guides
- **Integration**: Integration with taskwright and PM tools
- **Quick Reference**: Cheat sheets and quick reference cards
- **Examples**: Example requirements, features, and BDD scenarios
- **Developer Docs**: Architecture, ADRs, contributing guides
- **Troubleshooting & FAQ**: Common issues and questions

## Building the Documentation

### Prerequisites

Install the documentation build dependencies:

```bash
pip install -r requirements-docs.txt
```

Or install manually:

```bash
pip install mkdocs mkdocs-material
```

### Local Development

Serve the documentation locally with live reload:

```bash
mkdocs serve
```

Then open http://localhost:8000 in your browser.

### Building for Production

Build the static site:

```bash
mkdocs build
```

This creates the site in the `site/` directory.

### Strict Build (Recommended)

Build with strict mode to catch warnings:

```bash
mkdocs build --strict
```

## Documentation Guidelines

### File Organization

- All documentation source files are in the `docs/` directory
- Landing pages use `index.md` naming convention
- Keep max 3 levels of navigation depth
- Use descriptive filenames with hyphens (e.g., `getting-started.md`)

### Writing Style

- Use clear, concise language
- Include code examples where helpful
- Use admonitions for notes, warnings, tips
- Link to related sections for cross-references

### Markdown Extensions

The site supports many Markdown extensions:

- **Admonitions**: `!!! note`, `!!! warning`, `!!! tip`
- **Code blocks**: Syntax highlighting for bash, python, yaml, json, etc.
- **Tables**: Standard Markdown tables
- **Task lists**: `- [ ]` and `- [x]` checkboxes
- **Footnotes**: `[^1]` references
- **Emojis**: `:smile:` → 😊

### Code Examples

Use fenced code blocks with language specifiers:

````markdown
```bash
/gather-requirements
```

```python
def example():
    pass
```
````

## Navigation Structure

The navigation is defined in `mkdocs.yml` and follows the structure from the planning document:

1. **Home** - Landing page
2. **Getting Started** - Onboarding content
3. **Core Concepts** - Fundamental concepts
4. **User Guides** - Step-by-step guides
5. **Commands Reference** - Command documentation
6. **MCP Setup** - MCP configuration
7. **Integration** - Integration guides
8. **Quick Reference** - Quick lookups
9. **Examples** - Example content
10. **Developer Docs** - Contributing and architecture
11. **Troubleshooting & FAQ** - Support content

## Missing Pages

Several landing pages need to be created (see TASK-DOCS-003):

### Priority P0 (Critical)
- `docs/index.md` - Site home page
- `getting-started/index.md` - Getting Started section home
- `getting-started/quickstart.md` - 5-minute quickstart
- `getting-started/installation.md` - Installation guide
- `core-concepts/index.md` - Core Concepts section home
- `core-concepts/ears-notation.md` - EARS patterns
- `core-concepts/bdd-scenarios.md` - BDD explanation
- `core-concepts/hierarchy.md` - Hierarchy explanation
- `commands/index.md` - Commands overview

See `docs/planning/documentation-organization-plan.md` for the complete list.

## Excluded Content

The following directories are excluded from the site build (but remain in the repository):

- `research/` - Research documents
- `analysis/` - Analysis documents
- `state/` - State tracking
- `implementation-plans/` - Implementation artifacts
- `test_reports/` - Test reports
- `tests/` - Test files
- `reviews/` - Review documents
- `fixes/` - Fix summaries
- `proposals/` - Proposals
- `migration/` - Migration docs
- `planning/` - Planning documents
- `requirements-gathering-api/` - Internal API docs

These are development artifacts not relevant to end users.

## Configuration

The site configuration is in `mkdocs.yml` at the repository root. Key configuration sections:

- **Site Metadata**: name, description, URL, repository links
- **Theme**: Material theme with features enabled
- **Navigation**: Complete navigation structure
- **Markdown Extensions**: Enabled extensions and plugins
- **Exclusions**: Files/directories excluded from build

## GitHub Pages Deployment

The documentation is automatically deployed to GitHub Pages via GitHub Actions (see TASK-DOCS-004).

Manual deployment:

```bash
mkdocs gh-deploy
```

This builds the site and pushes to the `gh-pages` branch.

## Contributing to Documentation

### Adding New Pages

1. Create the markdown file in the appropriate directory
2. Add it to the `nav` section in `mkdocs.yml`
3. Use the existing pages as templates for formatting
4. Test locally with `mkdocs serve`
5. Submit a pull request

### Updating Existing Pages

1. Edit the markdown file
2. Test locally with `mkdocs serve`
3. Run `mkdocs build --strict` to check for warnings
4. Submit a pull request

### Fixing Broken Links

1. Run `mkdocs build --strict` to find broken links
2. Fix the links in the source files
3. Re-test and submit a pull request

## Resources

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Planning Document](planning/documentation-organization-plan.md)

## Support

For documentation issues:

1. Check existing docs for guidance
2. Review the planning document
3. Open a GitHub issue with the `documentation` label
4. Contact the RequireKit team

---

**Last Updated**: 2025-11-06
**MkDocs Version**: ≥1.5.0
**Material Version**: ≥9.5.0
