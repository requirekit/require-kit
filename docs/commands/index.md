# Commands Reference

Complete reference for all RequireKit commands.

## Quick Reference

### Requirements Commands
- [`/gather-requirements`](requirements.md#gather-requirements) - Interactive requirements gathering
- [`/formalize-ears`](requirements.md#formalize-ears) - Convert to EARS notation
- [`/generate-bdd`](requirements.md#generate-bdd) - Generate BDD scenarios

### Epic Commands
- [`/epic-create`](epics.md#epic-create) - Create new epic
- [`/epic-status`](epics.md#epic-status) - View epic progress
- [`/epic-generate-features`](epics.md#epic-generate-features) - Generate features
- [`/epic-sync`](epics.md#epic-sync) - Sync with PM tools

### Feature Commands
- [`/feature-create`](features.md#feature-create) - Create new feature
- [`/feature-status`](features.md#feature-status) - View feature progress
- [`/feature-generate-tasks`](features.md#feature-generate-tasks) - Generate task specifications
- [`/feature-sync`](features.md#feature-sync) - Sync with PM tools

### Hierarchy Commands
- [`/hierarchy-view`](hierarchy.md#hierarchy-view) - View epic/feature hierarchy

## Command Categories

### [Requirements Commands](requirements.md)
Gather, formalize, and generate test scenarios from requirements.

### [Epic Commands](epics.md)
Create and manage strategic business objectives.

### [Feature Commands](features.md)
Create and manage implementation units.

### [Hierarchy Commands](hierarchy.md)
Visualize and navigate requirement hierarchies.

## Common Workflows

### Basic Workflow
```bash
/gather-requirements
/formalize-ears
/generate-bdd
```

### Full Workflow
```bash
/gather-requirements
/formalize-ears
/epic-create "Title"
/feature-create "Title" epic:EPIC-001
/generate-bdd
/hierarchy-view EPIC-001
```

## Next Steps

- 📖 [Learn Requirements Commands](requirements.md)
- 🎯 [Learn Epic Commands](epics.md)
- 📝 [Learn Feature Commands](features.md)
- 📚 [Try the Quickstart](../getting-started/quickstart.md)

For detailed command documentation, see the [Complete User Guide](../guides/command_usage_guide.md).
