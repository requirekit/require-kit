# Architecture

RequireKit system architecture and design overview.

## System Overview

RequireKit is a requirements management toolkit using:
- **EARS notation** for clear requirements
- **BDD/Gherkin** for test scenarios
- **Markdown files** for storage
- **Claude agents** for automation

## Architecture Layers

### 1. User Interface Layer
- Slash commands (`/gather-requirements`, `/formalize-ears`)
- Interactive Q&A sessions
- Command-line interface

### 2. Agent Layer
- **requirements-analyst**: Gathers and formalizes requirements
- **bdd-generator**: Generates Gherkin scenarios
- Specialized agents for EARS patterns

### 3. Storage Layer
- Markdown files with YAML frontmatter
- Git-friendly plain text format
- Hierarchical directory structure

### 4. Integration Layer
- Marker file detection for taskwright
- PM tool metadata in frontmatter
- Bidirectional package detection

## Data Flow

```
User Command
    ↓
Claude Agent
    ↓
Process/Generate
    ↓
Markdown Files
    ↓
PM Tools / taskwright
```

## Design Principles

1. **Technology Agnostic**: Markdown outputs work with any system
2. **No Hard Dependencies**: Standalone with optional integration
3. **Version Control Friendly**: Plain text, Git-compatible
4. **Human Readable**: Markdown is readable without tools
5. **Composable**: Works alone or with taskwright

## Key Decisions

See [Architecture Decision Records](adr.md) for detailed decision rationale.

For complete architecture details, see `docs/architecture/ARCHITECTURE-SUMMARY.md`.
