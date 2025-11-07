# PM Tool Integration

Export RequireKit requirements, features, and epics to project management tools.

## Supported PM Tools

### Jira
```bash
/feature-sync FEAT-001 --jira
```

### Linear
```bash
/feature-sync FEAT-001 --linear
```

### GitHub Projects
```bash
/feature-sync FEAT-001 --github
```

### Azure DevOps
```bash
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

**API Integration**: Requires MCP server or custom implementation. The structured format makes integration straightforward.

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
