# Architecture Decision Records

Index of all architecture decisions for RequireKit.

## What are ADRs?

Architecture Decision Records document important architectural decisions, their context, and their consequences.

## ADR Index

For the complete list of ADRs, see the `docs/adr/` directory:

- ADR-002: Figma React Architecture
- ADR-005: Upfront Complexity Refactored Architecture
- And more...

## Accessing ADRs

All ADR files are located in:
```
docs/adr/*.md
```

Each ADR follows the format:
- **Context**: The situation and problem
- **Decision**: The chosen solution
- **Consequences**: Impact of the decision

## Key Architectural Decisions

### Requirements Format
**Decision**: Use EARS notation with markdown storage
**Rationale**: Clear, version-controllable, tool-agnostic

### BDD Generation
**Decision**: Automatic generation from EARS requirements
**Rationale**: Reduce manual work, ensure consistency

### Integration Approach
**Decision**: Marker file detection for optional integration
**Rationale**: No hard dependencies, graceful degradation

For complete ADR files, browse the `docs/adr/` directory.
