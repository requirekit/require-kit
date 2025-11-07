# Documentation Setup Guide

This guide explains how to set up, build, and deploy the RequireKit documentation.

## Quick Start

```bash
# Install dependencies
pip install -r requirements-docs.txt

# Serve locally
mkdocs serve

# Build for production
mkdocs build --strict
```

## Installation

### Option 1: Using requirements-docs.txt (Recommended)

```bash
pip install -r requirements-docs.txt
```

### Option 2: Manual Installation

```bash
pip install mkdocs>=1.5.0
pip install mkdocs-material>=9.5.0
```

### Verify Installation

```bash
mkdocs --version
# Should show: mkdocs, version 1.5.x or higher
```

## Local Development

### Start Development Server

```bash
mkdocs serve
```

This starts a local server at http://localhost:8000 with live reload. Any changes to documentation files will automatically refresh the browser.

### Custom Port

```bash
mkdocs serve --dev-addr=127.0.0.1:8080
```

### Strict Mode (Recommended for Development)

```bash
mkdocs serve --strict
```

This fails on warnings, helping you catch issues early.

## Building the Site

### Standard Build

```bash
mkdocs build
```

This creates the static site in the `site/` directory.

### Strict Build (Recommended)

```bash
mkdocs build --strict
```

Fails if there are warnings (broken links, missing files, etc.). Use this before committing changes.

### Clean Build

```bash
rm -rf site/
mkdocs build --strict
```

## Configuration

The documentation configuration is in `mkdocs.yml` at the repository root.

### Key Configuration Sections

- **Site Metadata**: Site name, description, URLs
- **Theme**: Material for MkDocs with enabled features
- **Navigation**: Complete site navigation structure
- **Markdown Extensions**: Syntax, admonitions, code highlighting
- **Plugins**: Search and other plugins
- **Exclusions**: Files/directories excluded from build

### Updating Configuration

1. Edit `mkdocs.yml`
2. Test with `mkdocs serve --strict`
3. Verify changes in browser
4. Commit if everything works

## Navigation Structure

The navigation follows the structure defined in `docs/planning/documentation-organization-plan.md`:

```
Home
├── Getting Started
│   ├── Overview
│   ├── Quickstart
│   ├── Installation
│   ├── Your First Requirements
│   └── Integration with taskwright
├── Core Concepts
│   ├── Overview
│   ├── EARS Notation Patterns
│   ├── BDD/Gherkin Scenarios
│   ├── Epic/Feature Hierarchy
│   └── Requirements Traceability
├── User Guides
│   ├── Overview
│   ├── Complete User Guide
│   ├── Getting Started Guide
│   └── Command Usage Guide
└── ... (8 more top-level sections)
```

## Adding New Pages

### 1. Create the Markdown File

```bash
# Example: Adding a new guide
touch docs/guides/my-new-guide.md
```

### 2. Add to Navigation

Edit `mkdocs.yml` and add to the `nav` section:

```yaml
nav:
  - User Guides:
      - Overview: guides/README.md
      - My New Guide: guides/my-new-guide.md  # Add here
      - Complete User Guide: guides/require_kit_user_guide.md
```

### 3. Write Content

Use existing pages as templates. Include:
- Clear title (# heading)
- Introduction paragraph
- Sections with ## headings
- Code examples
- Links to related pages

### 4. Test Locally

```bash
mkdocs serve --strict
```

Navigate to your new page and check:
- Page renders correctly
- Navigation link works
- No broken links
- Code highlighting works

### 5. Commit

```bash
git add docs/guides/my-new-guide.md mkdocs.yml
git commit -m "docs: add new guide for X"
```

## Markdown Features

### Admonitions (Callouts)

```markdown
!!! note
    This is a note.

!!! warning
    This is a warning.

!!! tip
    This is a tip.

!!! example
    This is an example.
```

### Code Blocks with Syntax Highlighting

````markdown
```bash
/gather-requirements
```

```python
def hello():
    print("Hello, RequireKit!")
```

```yaml
site_name: RequireKit
theme:
  name: material
```
````

### Tables

```markdown
| Command | Description | Example |
|---------|-------------|---------|
| `/gather-requirements` | Gather requirements | Basic usage |
| `/formalize-ears` | Formalize with EARS | Convert requirements |
```

### Task Lists

```markdown
- [x] Completed task
- [ ] Pending task
- [ ] Another pending task
```

### Links

```markdown
[Link text](path/to/page.md)
[External link](https://example.com)
[Section link](#heading-id)
```

### Footnotes

```markdown
This is a statement[^1].

[^1]: This is the footnote.
```

## Excluded Content

The following directories are excluded from the site build:

- `research/` - Research documents
- `analysis/` - Analysis documents
- `state/` - State tracking
- `implementation-plans/` - Implementation artifacts
- `test_reports/` - Test results
- `tests/` - Test files
- `reviews/` - Reviews
- `fixes/` - Fix summaries
- `proposals/` - Proposals
- `migration/` - Migration docs
- `planning/` - Planning documents
- `requirements-gathering-api/` - Internal APIs

These remain in the repository but are not built into the public documentation site.

## Troubleshooting

### "mkdocs: command not found"

**Solution**: Install MkDocs:
```bash
pip install mkdocs mkdocs-material
```

### "WARNING: Documentation file 'path/to/file.md' contains a link to 'other.md' which is not found"

**Solution**: Either create the missing file or update the link.

### "ERROR: Config value 'nav': Expected a list, got..."

**Solution**: Check `mkdocs.yml` syntax. Ensure proper YAML indentation (2 spaces).

### "Port 8000 already in use"

**Solution**: Either:
- Stop the other process using port 8000
- Use a different port: `mkdocs serve --dev-addr=127.0.0.1:8080`

### "ImportError: No module named 'mkdocs'"

**Solution**: Activate your Python virtual environment or install globally:
```bash
pip install --user mkdocs mkdocs-material
```

### Build Warnings

Run with strict mode to see all warnings:
```bash
mkdocs build --strict
```

Fix warnings before deploying:
- Broken links → Fix or remove links
- Missing files → Create files or update navigation
- Invalid YAML → Check indentation and syntax

## Deployment

### GitHub Pages (Automated)

Documentation is automatically deployed via GitHub Actions when changes are pushed to `main`.

See `.github/workflows/docs.yml` (created in TASK-DOCS-004).

### Manual Deployment to GitHub Pages

```bash
mkdocs gh-deploy
```

This builds the site and pushes to the `gh-pages` branch.

### Custom Deployment

Build the site and deploy the `site/` directory to your hosting provider:

```bash
mkdocs build --strict
# Deploy site/ directory to your web server
```

## Best Practices

### Before Committing

1. Run `mkdocs build --strict` → zero warnings
2. Run `mkdocs serve` → visually check changes
3. Test all new/modified links
4. Check responsive design (resize browser)
5. Spell check content

### Writing Documentation

1. **Be Clear**: Use simple, direct language
2. **Be Concise**: Get to the point quickly
3. **Use Examples**: Code examples help users understand
4. **Cross-Link**: Link to related pages
5. **Test Code**: Ensure code examples actually work
6. **Update Navigation**: Add new pages to `mkdocs.yml`

### File Naming

- Use lowercase with hyphens: `my-page.md`
- Use `index.md` for section landing pages
- Be descriptive: `installation.md` not `install.md`

### Navigation Depth

- Keep max 3 levels deep
- Too deep = hard to navigate
- Too shallow = long nav menus

## Resources

- **MkDocs Documentation**: https://www.mkdocs.org/
- **Material for MkDocs**: https://squidfunk.github.io/mkdocs-material/
- **Material Reference**: https://squidfunk.github.io/mkdocs-material/reference/
- **Markdown Guide**: https://www.markdownguide.org/
- **Planning Document**: `docs/planning/documentation-organization-plan.md`

## Support

For documentation issues:

1. Check this guide
2. Check the planning document
3. Review Material for MkDocs documentation
4. Open a GitHub issue with label `documentation`

---

**Last Updated**: 2025-11-06
**MkDocs Version**: ≥1.5.0
**Material Version**: ≥9.5.0
