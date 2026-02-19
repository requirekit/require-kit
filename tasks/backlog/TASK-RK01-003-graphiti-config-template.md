---
id: TASK-RK01-003
title: "Create Graphiti configuration template"
task_type: scaffolding
parent_review: TASK-REV-RK01
feature_id: FEAT-RK-001
wave: 1
implementation_mode: direct
complexity: 3
dependencies: []
status: pending
priority: normal
tags: [graphiti, config, scaffolding]
---

# Task: Create Graphiti Configuration Template

## Description

Create the Graphiti configuration template file that controls whether Graphiti integration is enabled. This is the config that refinement commands and sync check to determine standalone vs Graphiti mode.

## Files to Create

- `installer/global/config/graphiti.yaml` - Configuration template with defaults

## Changes Required

1. **Create Configuration Template**:
   ```yaml
   # RequireKit Graphiti Integration Configuration
   # Set enabled: true when Graphiti/Neo4j is available
   graphiti:
     enabled: false  # Default: off (standalone mode)
     endpoint: "bolt://localhost:7687"
     project_namespace: "my_project"
     group_id_pattern: "{project}__requirements"
     sync_on_create: true   # Auto-push on /epic-create and /feature-create
     sync_on_refine: true   # Auto-push after /epic-refine and /feature-refine
   ```

2. **Document Configuration Options**:
   - Each field with description and valid values
   - How to enable Graphiti integration
   - What happens in standalone mode (all commands work, just no Graphiti push)
   - Tip message for standalone users

## Acceptance Criteria

- [ ] Config file exists at `installer/global/config/graphiti.yaml`
- [ ] Default is `enabled: false` (standalone mode)
- [ ] All fields documented with comments
- [ ] Group ID pattern uses `{project}__requirements` convention from FEAT-RK-001 spec

## Test Requirements

- [ ] Verify YAML parses correctly
- [ ] Verify default values are sensible
