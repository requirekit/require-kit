---
id: REQ-002E
title: "Clean Documentation"
created: 2025-10-27
status: backlog
priority: high
complexity: 4
parent_task: REQ-002
subtasks: []
estimated_hours: 1
---

# REQ-002E: Clean Documentation

## Description

Delete task execution and stack-specific documentation, update core documentation files to focus on requirements management.

## Documentation to DELETE

### Workflow Guides

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit/docs/

# Delete task execution guides
rm -f guides/agentecflow-lite-workflow.md
rm -f guides/iterative-refinement-guide.md
rm -f guides/mcp-optimization-guide.md

# Delete template guides
rm -f guides/creating-local-templates.md
rm -f guides/maui-template-selection.md

# Delete workflow docs
rm -f workflows/complexity-management-workflow.md
rm -f workflows/design-first-workflow.md
rm -f workflows/ux-design-integration-workflow.md
rm -f workflows/complete-workflows.md

# Delete patterns
rm -f patterns/domain-layer-pattern.md
```

### Root-Level Task Documentation

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit/

# Delete task-specific documentation
rm -f TASK-030-*.md
rm -f TASK-*-SUMMARY.md
rm -f TASK-*-ANALYSIS*.md
rm -f PRESENTATION-README.md

# Delete scripts if task-focused
rm -f update-branding.sh
```

## Documentation to KEEP

```bash
# Keep requirements documentation
✅ docs/requirements/ (if exists)
✅ docs/epics/ (if exists)
✅ docs/features/ (if exists)
✅ docs/bdd/ (if exists)

# Keep core files (will update)
✅ README.md
✅ CLAUDE.md
```

## Files to UPDATE

### 1. README.md

Update to focus on requirements management:

```markdown
# require-kit

**Requirements management toolkit with EARS notation, BDD scenarios, and epic/feature hierarchy.**

## Features

- Interactive requirements gathering
- EARS notation formalization
- BDD/Gherkin scenario generation
- Epic/feature hierarchy management
- Requirements traceability

## Quick Start

### Gather Requirements
\`\`\`bash
/gather-requirements
\`\`\`

### Formalize with EARS
\`\`\`bash
/formalize-ears
\`\`\`

### Generate BDD Scenarios
\`\`\`bash
/generate-bdd
\`\`\`

## Documentation

- [EARS Notation Guide](docs/guides/ears-notation.md)
- [BDD Scenarios Guide](docs/guides/bdd-scenarios.md)
- [Epic/Feature Hierarchy](docs/guides/epic-feature-hierarchy.md)

## Integration

Can be used standalone or integrated with task execution systems like Agentecflow.
```

### 2. CLAUDE.md

Update to focus on requirements:

```markdown
# require-kit - Requirements Management System

## Project Context

This is a requirements management toolkit using EARS notation for requirements, BDD/Gherkin for test specifications, and epic/feature hierarchy for organization.

## Core Principles

1. **Requirements First**: Every feature starts with EARS-notated requirements
2. **BDD Scenarios**: Generate testable Gherkin scenarios from requirements
3. **Traceability**: Clear links between epics, features, and requirements
4. **Technology Agnostic**: Works with any implementation system

## Essential Commands

### Requirements Gathering
\`\`\`bash
/gather-requirements   # Interactive Q&A
/formalize-ears       # Convert to EARS notation
/generate-bdd         # Generate Gherkin scenarios
\`\`\`

### Epic/Feature Management
\`\`\`bash
/epic-create "Title"
/feature-create "Title" epic:EPIC-XXX
/hierarchy-view EPIC-XXX
\`\`\`

## EARS Notation Patterns

1. **Ubiquitous**: \`The [system] shall [behavior]\`
2. **Event-Driven**: \`When [trigger], the [system] shall [response]\`
3. **State-Driven**: \`While [state], the [system] shall [behavior]\`
4. **Unwanted Behavior**: \`If [error], then the [system] shall [recovery]\`
5. **Optional Feature**: \`Where [feature], the [system] shall [behavior]\`

## Integration

This toolkit focuses on requirements gathering and management. For task execution and implementation, integrate with:
- [Agentecflow](https://github.com/yourusername/agentecflow)
- Your project management tools (Jira, Linear, GitHub Projects)
```

## Implementation

```bash
# Delete workflow guides
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit/docs/
rm -f guides/agentecflow-lite-workflow.md guides/iterative-refinement-guide.md
rm -f guides/mcp-optimization-guide.md guides/creating-local-templates.md
rm -f guides/maui-template-selection.md

# Delete workflows
rm -rf workflows/

# Delete patterns
rm -rf patterns/

# Delete root task docs
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit/
rm -f TASK-*.md
rm -f PRESENTATION-README.md
rm -f update-branding.sh

# Keep extraction summary for reference
# ✅ Keep EXTRACTION-SUMMARY.md (documents this migration)
```

## Update Core Files

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit/

# Backup current README and CLAUDE.md
cp README.md README.md.bak
cp CLAUDE.md CLAUDE.md.bak

# Edit README.md - focus on requirements management
# Edit CLAUDE.md - focus on requirements management
# (Manual editing required - use content from "Files to UPDATE" section)
```

## Verification

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit/

# Verify task docs deleted
! ls TASK-*.md 2>/dev/null && echo "✓ Task docs deleted" || echo "✗ Task docs remain"

# Verify workflow guides deleted
! ls docs/workflows/ 2>/dev/null && echo "✓ Workflows deleted" || echo "✗ Workflows remain"

# Verify patterns deleted
! ls docs/patterns/ 2>/dev/null && echo "✓ Patterns deleted" || echo "✗ Patterns remain"

# Check README focuses on requirements
grep -q "requirements management" README.md && echo "✓ README updated" || echo "✗ README needs update"

# Check CLAUDE.md focuses on requirements
grep -q "Requirements Management" CLAUDE.md && echo "✓ CLAUDE.md updated" || echo "✗ CLAUDE.md needs update"
```

## Acceptance Criteria

- [ ] Workflow guides deleted
- [ ] Task-specific documentation deleted
- [ ] Patterns documentation deleted
- [ ] Root TASK-*.md files deleted
- [ ] README.md updated to focus on requirements
- [ ] CLAUDE.md updated to focus on requirements
- [ ] No references to task execution in core docs
- [ ] No references to quality gates in core docs
- [ ] Documentation emphasizes requirements management
- [ ] Verification tests pass

## Estimated Time

1 hour

## Notes

- Keep docs/epics/, docs/features/, docs/requirements/, docs/bdd/ if they exist
- Update rather than rewrite README and CLAUDE.md
- Keep EXTRACTION-SUMMARY.md as historical record
- Commit after verification
