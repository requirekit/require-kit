# PM Tool Integration

Export RequireKit requirements, features, and epics to project management tools.

> **Status: Specification Ready - Implementation Required**
>
> The sync commands documented below describe the **intended integration behavior**.
> RequireKit provides structured metadata ready for export, but **actual API integration
> requires MCP server or custom implementation**.
>
> **What IS provided:**
> - Structured YAML frontmatter in epic/feature files
> - Field mappings for Jira, Linear, GitHub Projects, Azure DevOps
> - Detailed specifications for sync behavior
>
> **What IS NOT provided:**
> - Working `/feature-sync` or `/epic-sync` commands
> - MCP server for PM tool APIs
> - Automated synchronization

## Supported PM Tools (Specification)

### Jira
```bash
# When implemented:
/feature-sync FEAT-001 --jira
```

### Linear
```bash
# When implemented:
/feature-sync FEAT-001 --linear
```

### GitHub Projects
```bash
# When implemented:
/feature-sync FEAT-001 --github
```

### Azure DevOps
```bash
# When implemented:
/feature-sync FEAT-001 --azure
```

## What Gets Exported

- Feature description → User story
- Requirements → Acceptance criteria
- BDD scenarios → Test specifications
- Epic links → Parent issue links
- Metadata → Custom fields

## Integration Status

**Specification Ready**: Epic and feature files include structured metadata for PM tool export.

**API Integration Not Implemented**: Actual API integration requires MCP server or custom implementation. The structured format makes building integrations straightforward, but no working implementation is currently provided.

## Structured Metadata Example

```yaml
---
id: FEAT-001
title: User Authentication
epic: EPIC-001
requirements: [REQ-001, REQ-002]
pm_metadata:
  jira:
    project: PROJ
    issue_type: Story
    priority: High
  linear:
    team: Engineering
    priority: 1
---
```

## Custom Integration

Use the structured markdown files to build custom integrations:

1. Parse frontmatter YAML
2. Extract requirements and BDD scenarios
3. Call PM tool APIs
4. Create issues with traceability links

## Next Steps

For complete integration details, see the [Integration Guide](../INTEGRATION-GUIDE.md).
