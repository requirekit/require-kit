---
id: TASK-001E
title: "Transfer Stack Templates"
created: 2025-10-19
status: backlog
priority: high
complexity: 5
parent_task: TASK-001
subtasks: []
estimated_hours: 4
---

# TASK-001E: Transfer Stack Templates

## Description

Copy all stack templates, updating CLAUDE.md in each to remove requirements references while keeping all stack-specific patterns and agents.

## Templates to Transfer

```
default/
react/
python/
typescript-api/
maui-appshell/
maui-navigationpage/
dotnet-microservice/
fullstack/
```

## Implementation

```bash
cd ai-engineer/installer/global/templates

# Copy all templates
cp -r default/ react/ python/ typescript-api/ \
      maui-appshell/ maui-navigationpage/ \
      dotnet-microservice/ fullstack/ \
      ../../agentecflow/installer/global/templates/
```

## Modifications for Each Template

### Update CLAUDE.md (All Templates)

**Remove sections**:
- Requirements Management
- EARS Notation
- BDD/Gherkin Scenarios
- Epic/Feature Hierarchy
- External PM Tool Integration

**Keep sections**:
- Task Workflow
- Quality Gates (Phase 2.5, 4.5)
- Testing Patterns
- Stack-Specific Patterns
- Architecture Principles

**Update task creation examples** from:
```bash
/task-create "Feature" epic:EPIC-001 feature:FEAT-001 requirements:[REQ-001]
```

To:
```bash
/task-create "Feature name"
```

### Update settings.json (If Present)

**Remove**:
```json
{
  "requirements_dir": "docs/requirements",
  "bdd_dir": "docs/bdd",
  "epics_dir": "docs/epics",
  "features_dir": "docs/features"
}
```

**Keep**:
```json
{
  "tasks_dir": "tasks",
  "stack": "react",  // or appropriate stack
  "quality_gates": {...}
}
```

## Per-Template Checklist

### default/

- [ ] CLAUDE.md updated (remove requirements references)
- [ ] agents/ directory copied as-is
- [ ] templates/ directory copied as-is

### react/

- [ ] CLAUDE.md updated
- [ ] PATTERNS.md kept as-is
- [ ] agents/react-state-specialist.md kept
- [ ] agents/react-testing-specialist.md kept

### python/

- [ ] CLAUDE.md updated
- [ ] agents/python-api-specialist.md kept
- [ ] agents/python-testing-specialist.md kept

### typescript-api/

- [ ] CLAUDE.md updated
- [ ] agents/nestjs-api-specialist.md kept
- [ ] agents/typescript-domain-specialist.md kept

### maui-appshell/, maui-navigationpage/

- [ ] CLAUDE.md updated
- [ ] agents/maui-domain-specialist.md kept
- [ ] agents/maui-viewmodel-specialist.md kept
- [ ] Domain layer patterns kept
- [ ] MAUI template selection guide kept

### dotnet-microservice/

- [ ] CLAUDE.md updated
- [ ] agents/dotnet-api-specialist.md kept
- [ ] FastEndpoints patterns kept

### fullstack/

- [ ] CLAUDE.md updated (both frontend and backend)
- [ ] Integration patterns kept

## Verification

```bash
cd agentecflow/installer/global/templates

# Verify all templates exist
for template in default react python typescript-api maui-appshell \
                maui-navigationpage dotnet-microservice fullstack; do
  [ -d "$template" ] && echo "✓ $template" || echo "✗ $template MISSING"
done

# Check no requirements references in CLAUDE.md files
for template in */CLAUDE.md; do
  echo "Checking $template..."
  grep -i "epic\|requirements.*EARS\|BDD.*scenario" "$template" | \
    grep -v "# Historical" && echo "⚠ Found references in $template"
done
```

## Acceptance Criteria

- [ ] 8 templates copied
- [ ] All CLAUDE.md files updated
- [ ] All stack-specific agents preserved
- [ ] No epic/feature/requirements references in templates
- [ ] settings.json files cleaned (if present)
- [ ] All templates initialize successfully

## Estimated Time

4 hours
